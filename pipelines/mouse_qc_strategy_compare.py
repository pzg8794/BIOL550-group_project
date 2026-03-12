#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PILOT_CASES = [
    {"srr": "SRR30333754", "focus_read": "SRR30333754_2", "issue_type": "poly-G dominated read 2"},
    {"srr": "SRR30333756", "focus_read": "SRR30333756_2", "issue_type": "poly-G dominated read 2"},
    {"srr": "SRR30333743", "focus_read": "SRR30333743_1", "issue_type": "explicit TruSeq adapter in read 1"},
]

STAGE_CONFIG = {
    "raw": {"label": "Raw FASTQ", "suffix": "_fastqc.zip"},
    "fastx": {"label": "Current FASTX trimmed", "suffix": ".trim_fastqc.zip"},
    "fastp": {"label": "fastp", "suffix": ".fastp_fastqc.zip"},
    "cutadapt": {"label": "cutadapt", "suffix": ".cutadapt_fastqc.zip"},
}

STATUS_MODULES = [
    "Adapter Content",
    "Overrepresented sequences",
    "Per base sequence content",
    "Sequence Length Distribution",
]


@dataclass
class StageDirs:
    raw_dir: Path
    fastx_dir: Path
    fastp_dir: Path
    cutadapt_dir: Path
    fastp_reports: Path
    cutadapt_reports: Path
    out_dir: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--fastx-dir", required=True, type=Path)
    parser.add_argument("--fastp-dir", required=True, type=Path)
    parser.add_argument("--cutadapt-dir", required=True, type=Path)
    parser.add_argument("--fastp-reports", required=True, type=Path)
    parser.add_argument("--cutadapt-reports", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def read_fastqc_zip(path: Path) -> dict[str, dict[str, object]]:
    with zipfile.ZipFile(path) as zf:
        member = next(name for name in zf.namelist() if name.endswith("fastqc_data.txt"))
        lines = zf.read(member).decode("utf-8", errors="replace").splitlines()
    modules: dict[str, dict[str, object]] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith(">>") and line != ">>END_MODULE":
            name, status = line[2:].split("\t", 1)
            index += 1
            rows: list[dict[str, str]] = []
            if index < len(lines) and lines[index].startswith("#"):
                headers = [col.lstrip("#") for col in lines[index].split("\t")]
                index += 1
                while index < len(lines) and lines[index] != ">>END_MODULE":
                    if lines[index]:
                        values = lines[index].split("\t")
                        rows.append(dict(zip(headers, values)))
                    index += 1
            else:
                while index < len(lines) and lines[index] != ">>END_MODULE":
                    index += 1
            modules[name] = {"status": status, "rows": rows}
        index += 1
    return modules


def parse_length_span(value: str) -> tuple[int, int]:
    text = str(value)
    if "-" in text:
        left, right = text.split("-", 1)
        return int(left), int(right)
    parsed = int(text)
    return parsed, parsed


def classify_signal(sequence: str, source: str) -> str:
    seq = sequence or ""
    src = source or ""
    if "truseq" in src.lower():
        return "TruSeq adapter"
    if seq and (set(seq) == {"G"} or (seq.startswith("T") and set(seq[1:]) == {"G"})):
        return "poly-G artifact"
    return src or "not detected"


def adapter_max(rows: list[dict[str, str]]) -> float | None:
    if not rows:
        return None
    values: list[float] = []
    for row in rows:
        for key, value in row.items():
            if key == "Position" or value == "":
                continue
            try:
                values.append(float(value))
            except ValueError:
                continue
    return max(values) if values else None


def top_overrep(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {"sequence": "", "percentage": None, "source": "", "signal_label": "not detected"}
    top = rows[0]
    percentage = None
    if top.get("Percentage"):
        percentage = float(top["Percentage"])
    sequence = top.get("Sequence", "")
    source = top.get("Possible Source", "")
    return {
        "sequence": sequence,
        "percentage": percentage,
        "source": source,
        "signal_label": classify_signal(sequence, source),
    }


def stage_zip_path(stage_dir: Path, focus_read: str, suffix: str) -> Path:
    return stage_dir / f"{focus_read}{suffix}"


def collect_stage_metrics(stage_name: str, stage_dir: Path, focus_read: str, issue_type: str) -> dict[str, object]:
    zip_path = stage_zip_path(stage_dir, focus_read, STAGE_CONFIG[stage_name]["suffix"])
    modules = read_fastqc_zip(zip_path)
    basic_stats = {row["Measure"]: row["Value"] for row in modules["Basic Statistics"]["rows"]}  # type: ignore[index]
    length_min, length_max = parse_length_span(basic_stats["Sequence length"])
    overrep = top_overrep(modules.get("Overrepresented sequences", {"rows": []})["rows"])  # type: ignore[index]
    result = {
        "stage": stage_name,
        "stage_label": STAGE_CONFIG[stage_name]["label"],
        "focus_read": focus_read,
        "issue_type": issue_type,
        "zip_path": str(zip_path),
        "sequence_length": basic_stats["Sequence length"],
        "length_min": length_min,
        "length_max": length_max,
        "total_sequences": int(basic_stats["Total Sequences"]),
        "adapter_max": adapter_max(modules.get("Adapter Content", {"rows": []})["rows"]),  # type: ignore[index]
        "dominant_overrep_pct": overrep["percentage"],
        "dominant_sequence": overrep["sequence"],
        "dominant_source": overrep["source"],
        "dominant_signal_label": overrep["signal_label"],
    }
    for module in STATUS_MODULES:
        key = module.lower().replace(" ", "_")
        result[f"status_{key}"] = modules.get(module, {}).get("status", "")
    return result


def collect_adapter_curve_rows(stage_name: str, stage_dir: Path, focus_read: str) -> list[dict[str, object]]:
    zip_path = stage_zip_path(stage_dir, focus_read, STAGE_CONFIG[stage_name]["suffix"])
    modules = read_fastqc_zip(zip_path)
    rows = modules.get("Adapter Content", {"rows": []})["rows"]  # type: ignore[index]
    curve_rows: list[dict[str, object]] = []
    for row in rows:
        position = row["Position"]
        position_end = int(position.split("-", 1)[1]) if "-" in position else int(position)
        numeric = []
        for key, value in row.items():
            if key == "Position" or value == "":
                continue
            try:
                numeric.append(float(value))
            except ValueError:
                continue
        curve_rows.append(
            {
                "focus_read": focus_read,
                "stage": stage_name,
                "stage_label": STAGE_CONFIG[stage_name]["label"],
                "position": position,
                "position_end": position_end,
                "max_adapter_pct": max(numeric) if numeric else None,
            }
        )
    return curve_rows


def parse_fastp_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    before = data.get("summary", {}).get("before_filtering", {})
    after = data.get("summary", {}).get("after_filtering", {})
    before_reads = before.get("total_reads")
    after_reads = after.get("total_reads")
    retained_pct = None
    if before_reads and after_reads is not None:
        retained_pct = 100.0 * float(after_reads) / float(before_reads)
    return {
        "tool": "fastp",
        "report_path": str(path),
        "input_reads": before_reads,
        "output_reads": after_reads,
        "retained_pct": retained_pct,
        "input_bases": before.get("total_bases"),
        "output_bases": after.get("total_bases"),
        "q20_rate_after": after.get("q20_rate"),
        "q30_rate_after": after.get("q30_rate"),
    }


def parse_cutadapt_log(path: Path) -> dict[str, object]:
    text = path.read_text(errors="replace")

    def number(pattern: str) -> int | None:
        match = re.search(pattern, text, re.MULTILINE)
        if not match:
            return None
        return int(match.group(1).replace(",", ""))

    def percent(pattern: str) -> float | None:
        match = re.search(pattern, text, re.MULTILINE)
        if not match:
            return None
        return float(match.group(1))

    total_pairs = number(r"Total read pairs processed:\s+([\d,]+)")
    written_pairs = number(r"Pairs written \(passing filters\):\s+([\d,]+)")
    retained_pct = percent(r"Pairs written \(passing filters\):\s+[\d,]+\s+\(([\d.]+)%\)")
    return {
        "tool": "cutadapt",
        "report_path": str(path),
        "input_pairs": total_pairs,
        "output_pairs": written_pairs,
        "retained_pct": retained_pct,
    }


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_wide_rows(stage_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_read: dict[str, list[dict[str, object]]] = {}
    for row in stage_rows:
        by_read.setdefault(str(row["focus_read"]), []).append(row)

    wide_rows: list[dict[str, object]] = []
    stage_order = ["raw", "fastx", "fastp", "cutadapt"]
    for case in PILOT_CASES:
        focus_read = case["focus_read"]
        grouped = {row["stage"]: row for row in by_read.get(focus_read, [])}
        wide = {"srr": case["srr"], "focus_read": focus_read, "issue_type": case["issue_type"]}
        for stage in stage_order:
            row = grouped.get(stage, {})
            wide[f"{stage}_sequence_length"] = row.get("sequence_length")
            wide[f"{stage}_adapter_max"] = row.get("adapter_max")
            wide[f"{stage}_dominant_overrep_pct"] = row.get("dominant_overrep_pct")
            wide[f"{stage}_dominant_signal_label"] = row.get("dominant_signal_label")
        if grouped.get("raw") and grouped.get("fastx"):
            wide["fastx_adapter_delta_vs_raw"] = _delta(grouped["fastx"].get("adapter_max"), grouped["raw"].get("adapter_max"))
            wide["fastx_overrep_delta_vs_raw"] = _delta(
                grouped["fastx"].get("dominant_overrep_pct"), grouped["raw"].get("dominant_overrep_pct")
            )
        if grouped.get("fastx") and grouped.get("fastp"):
            wide["fastp_adapter_delta_vs_fastx"] = _delta(grouped["fastp"].get("adapter_max"), grouped["fastx"].get("adapter_max"))
            wide["fastp_overrep_delta_vs_fastx"] = _delta(
                grouped["fastp"].get("dominant_overrep_pct"), grouped["fastx"].get("dominant_overrep_pct")
            )
        if grouped.get("fastx") and grouped.get("cutadapt"):
            wide["cutadapt_adapter_delta_vs_fastx"] = _delta(
                grouped["cutadapt"].get("adapter_max"), grouped["fastx"].get("adapter_max")
            )
            wide["cutadapt_overrep_delta_vs_fastx"] = _delta(
                grouped["cutadapt"].get("dominant_overrep_pct"), grouped["fastx"].get("dominant_overrep_pct")
            )
        wide_rows.append(wide)
    return wide_rows


def _delta(current: object, previous: object) -> float | None:
    if current in ("", None) or previous in ("", None):
        return None
    return float(current) - float(previous)


def stage_dirs_from_args(args: argparse.Namespace) -> StageDirs:
    return StageDirs(
        raw_dir=args.raw_dir,
        fastx_dir=args.fastx_dir,
        fastp_dir=args.fastp_dir,
        cutadapt_dir=args.cutadapt_dir,
        fastp_reports=args.fastp_reports,
        cutadapt_reports=args.cutadapt_reports,
        out_dir=args.out_dir,
    )


def build_summary(stage_rows: list[dict[str, object]], fastp_metrics: list[dict[str, object]], cutadapt_metrics: list[dict[str, object]]) -> str:
    grouped_rows: dict[str, dict[str, dict[str, object]]] = {}
    for row in stage_rows:
        grouped_rows.setdefault(str(row["focus_read"]), {})[str(row["stage"])] = row

    fastp_by_srr = {Path(row["report_path"]).stem.split(".")[0]: row for row in fastp_metrics}
    cutadapt_by_srr = {Path(row["report_path"]).stem.split(".")[0]: row for row in cutadapt_metrics}

    lines = [
        "# Mouse pilot QC strategy comparison",
        "",
        "This report compares the pilot reads across four stages where available:",
        "- raw",
        "- current FASTX trimmed baseline",
        "- fastp",
        "- cutadapt",
        "",
    ]
    for case in PILOT_CASES:
        focus_read = case["focus_read"]
        srr = case["srr"]
        rows = grouped_rows.get(focus_read, {})
        lines.append(f"## {focus_read} ({case['issue_type']})")
        for stage in ["raw", "fastx", "fastp", "cutadapt"]:
            row = rows.get(stage)
            if not row:
                lines.append(f"- {STAGE_CONFIG[stage]['label']}: not available")
                continue
            lines.append(
                "- "
                f"{STAGE_CONFIG[stage]['label']}: length `{row['sequence_length']}`, "
                f"adapter_max `{_fmt(row['adapter_max'])}`, "
                f"dominant signal `{row['dominant_signal_label']}` at `{_fmt(row['dominant_overrep_pct'])}%`"
            )
        raw = rows.get("raw")
        fastx = rows.get("fastx")
        fastp = rows.get("fastp")
        cutadapt = rows.get("cutadapt")
        if raw and fastx:
            lines.append(
                "- "
                f"raw → FASTX: length `{raw['sequence_length']} → {fastx['sequence_length']}`, "
                f"adapter_max `{_fmt(raw['adapter_max'])} → {_fmt(fastx['adapter_max'])}`, "
                f"dominant signal `{_fmt(raw['dominant_overrep_pct'])}% → {_fmt(fastx['dominant_overrep_pct'])}%`"
            )
        if fastx and fastp:
            lines.append(
                "- "
                f"FASTX → fastp: adapter_max `{_fmt(fastx['adapter_max'])} → {_fmt(fastp['adapter_max'])}`, "
                f"dominant signal `{_fmt(fastx['dominant_overrep_pct'])}% → {_fmt(fastp['dominant_overrep_pct'])}%`, "
                f"retained `{_fmt(fastp_by_srr.get(srr, {}).get('retained_pct'))}%`"
            )
        if fastx and cutadapt:
            lines.append(
                "- "
                f"FASTX → cutadapt: adapter_max `{_fmt(fastx['adapter_max'])} → {_fmt(cutadapt['adapter_max'])}`, "
                f"dominant signal `{_fmt(fastx['dominant_overrep_pct'])}% → {_fmt(cutadapt['dominant_overrep_pct'])}%`, "
                f"retained `{_fmt(cutadapt_by_srr.get(srr, {}).get('retained_pct'))}%`"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def _fmt(value: object) -> str:
    if value in ("", None):
        return "NA"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def main() -> None:
    args = parse_args()
    dirs = stage_dirs_from_args(args)
    dirs.out_dir.mkdir(parents=True, exist_ok=True)

    stage_rows: list[dict[str, object]] = []
    curve_rows: list[dict[str, object]] = []
    for case in PILOT_CASES:
        focus_read = case["focus_read"]
        issue_type = case["issue_type"]
        for stage_name, stage_dir in [
            ("raw", dirs.raw_dir),
            ("fastx", dirs.fastx_dir),
            ("fastp", dirs.fastp_dir),
            ("cutadapt", dirs.cutadapt_dir),
        ]:
            zip_path = stage_zip_path(stage_dir, focus_read, STAGE_CONFIG[stage_name]["suffix"])
            if not zip_path.exists():
                continue
            stage_rows.append(collect_stage_metrics(stage_name, stage_dir, focus_read, issue_type))
            curve_rows.extend(collect_adapter_curve_rows(stage_name, stage_dir, focus_read))

    fastp_metrics = []
    for case in PILOT_CASES:
        report = dirs.fastp_reports / f"{case['srr']}.fastp.json"
        if report.exists():
            metrics = parse_fastp_json(report)
            metrics["srr"] = case["srr"]
            fastp_metrics.append(metrics)

    cutadapt_metrics = []
    for case in PILOT_CASES:
        report = dirs.cutadapt_reports / f"{case['srr']}.cutadapt.log"
        if report.exists():
            metrics = parse_cutadapt_log(report)
            metrics["srr"] = case["srr"]
            cutadapt_metrics.append(metrics)

    wide_rows = build_wide_rows(stage_rows)
    write_csv(
        dirs.out_dir / "pilot_read_stage_metrics.csv",
        stage_rows,
        [
            "stage",
            "stage_label",
            "focus_read",
            "issue_type",
            "zip_path",
            "sequence_length",
            "length_min",
            "length_max",
            "total_sequences",
            "adapter_max",
            "dominant_overrep_pct",
            "dominant_sequence",
            "dominant_source",
            "dominant_signal_label",
            *[f"status_{module.lower().replace(' ', '_')}" for module in STATUS_MODULES],
        ],
    )
    write_csv(
        dirs.out_dir / "pilot_adapter_curve_data.csv",
        curve_rows,
        ["focus_read", "stage", "stage_label", "position", "position_end", "max_adapter_pct"],
    )
    write_csv(
        dirs.out_dir / "pilot_srr_comparison_wide.csv",
        wide_rows,
        sorted({key for row in wide_rows for key in row.keys()}),
    )
    write_csv(
        dirs.out_dir / "pilot_fastp_run_metrics.csv",
        fastp_metrics,
        ["srr", "tool", "report_path", "input_reads", "output_reads", "retained_pct", "input_bases", "output_bases", "q20_rate_after", "q30_rate_after"],
    )
    write_csv(
        dirs.out_dir / "pilot_cutadapt_run_metrics.csv",
        cutadapt_metrics,
        ["srr", "tool", "report_path", "input_pairs", "output_pairs", "retained_pct"],
    )
    (dirs.out_dir / "pilot_summary.md").write_text(build_summary(stage_rows, fastp_metrics, cutadapt_metrics))


if __name__ == "__main__":
    main()
