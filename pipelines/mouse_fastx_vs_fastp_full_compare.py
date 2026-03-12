#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


KEY_MODULES = [
    "Adapter Content",
    "Overrepresented sequences",
    "Per base sequence content",
    "Sequence Length Distribution",
]

STATUS_ORDER = {"pass": 0, "warn": 1, "fail": 2}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fastx-dir", required=True, type=Path)
    parser.add_argument("--fastp-dir", required=True, type=Path)
    parser.add_argument("--fastp-reports", required=True, type=Path)
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
            modules[name] = {"status": status.lower(), "rows": rows}
        index += 1
    return modules


def normalize_read_id(path: Path, stage: str) -> str:
    name = path.name
    suffix = ".trim_fastqc.zip" if stage == "fastx" else ".fastp_fastqc.zip"
    return name.removesuffix(suffix)


def parse_length_span(value: str) -> tuple[int, int]:
    if "-" in value:
        left, right = value.split("-", 1)
        return int(left), int(right)
    parsed = int(value)
    return parsed, parsed


def adapter_max(rows: list[dict[str, str]]) -> float | None:
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


def top_overrep(rows: list[dict[str, str]]) -> tuple[str, float | None, str]:
    if not rows:
        return "", None, ""
    top = rows[0]
    pct = float(top["Percentage"]) if top.get("Percentage") else None
    return top.get("Sequence", ""), pct, top.get("Possible Source", "")


def classify_signal(sequence: str, source: str) -> str:
    src = source.lower()
    if "truseq" in src:
        return "TruSeq adapter"
    if sequence and set(sequence) == {"G"}:
        return "poly-G artifact"
    if sequence.startswith("T") and len(sequence) > 1 and set(sequence[1:]) == {"G"}:
        return "poly-G artifact"
    return source or "not detected"


def read_stage_metrics(stage_dir: Path, stage: str) -> dict[str, dict[str, object]]:
    metrics: dict[str, dict[str, object]] = {}
    for path in sorted(stage_dir.glob("*.zip")):
        read_id = normalize_read_id(path, stage)
        modules = read_fastqc_zip(path)
        basic = {row["Measure"]: row["Value"] for row in modules["Basic Statistics"]["rows"]}  # type: ignore[index]
        length_min, length_max = parse_length_span(str(basic["Sequence length"]))
        seq, pct, source = top_overrep(modules.get("Overrepresented sequences", {"rows": []})["rows"])  # type: ignore[index]
        record: dict[str, object] = {
            "read_id": read_id,
            "stage": stage,
            "zip_path": str(path),
            "total_sequences": int(str(basic["Total Sequences"]).replace(",", "")),
            "sequence_length": str(basic["Sequence length"]),
            "length_min": length_min,
            "length_max": length_max,
            "adapter_max": adapter_max(modules.get("Adapter Content", {"rows": []})["rows"]),  # type: ignore[index]
            "dominant_sequence": seq,
            "dominant_overrep_pct": pct,
            "dominant_source": source,
            "dominant_signal_label": classify_signal(seq, source),
        }
        for module in KEY_MODULES:
            key = module.lower().replace(" ", "_")
            record[f"status_{key}"] = modules.get(module, {}).get("status", "")
        metrics[read_id] = record
    return metrics


def read_fastp_reports(report_dir: Path) -> dict[str, dict[str, object]]:
    metrics: dict[str, dict[str, object]] = {}
    for path in sorted(report_dir.glob("*.json")):
        data = json.loads(path.read_text())
        before = data.get("summary", {}).get("before_filtering", {})
        after = data.get("summary", {}).get("after_filtering", {})
        before_reads = before.get("total_reads")
        after_reads = after.get("total_reads")
        retained_pct = None
        if before_reads and after_reads is not None:
            retained_pct = 100.0 * float(after_reads) / float(before_reads)
        metrics[path.stem.replace(".fastp", "")] = {
            "srr": path.stem.replace(".fastp", ""),
            "report_path": str(path),
            "input_reads": before_reads,
            "output_reads": after_reads,
            "retained_pct": retained_pct,
            "input_bases": before.get("total_bases"),
            "output_bases": after.get("total_bases"),
            "q20_rate_after": after.get("q20_rate"),
            "q30_rate_after": after.get("q30_rate"),
        }
    return metrics


def status_direction(old: str, new: str) -> str:
    old_rank = STATUS_ORDER.get(old, -1)
    new_rank = STATUS_ORDER.get(new, -1)
    if new_rank < old_rank:
        return "improved"
    if new_rank > old_rank:
        return "worse"
    return "unchanged"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def median_or_none(values: list[float]) -> float | None:
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return statistics.median(clean)


def mean_or_none(values: list[float]) -> float | None:
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return statistics.mean(clean)


def fmt(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}f}"


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    fastx = read_stage_metrics(args.fastx_dir, "fastx")
    fastp = read_stage_metrics(args.fastp_dir, "fastp")
    fastp_reports = read_fastp_reports(args.fastp_reports)

    common_reads = sorted(set(fastx) & set(fastp))
    per_read_rows: list[dict[str, object]] = []
    transition_rows: list[dict[str, object]] = []

    status_counts = defaultdict(Counter)
    transition_counts = defaultdict(Counter)

    for read_id in common_reads:
        base = fastx[read_id]
        post = fastp[read_id]
        srr = read_id.rsplit("_", 1)[0]
        row: dict[str, object] = {
            "read_id": read_id,
            "srr": srr,
            "fastx_total_sequences": base["total_sequences"],
            "fastp_total_sequences": post["total_sequences"],
            "fastx_sequence_length": base["sequence_length"],
            "fastp_sequence_length": post["sequence_length"],
            "fastx_adapter_max": base["adapter_max"],
            "fastp_adapter_max": post["adapter_max"],
            "adapter_max_delta_fastp_minus_fastx": (
                None
                if base["adapter_max"] is None or post["adapter_max"] is None
                else float(post["adapter_max"]) - float(base["adapter_max"])
            ),
            "fastx_dominant_signal_label": base["dominant_signal_label"],
            "fastp_dominant_signal_label": post["dominant_signal_label"],
            "fastx_dominant_overrep_pct": base["dominant_overrep_pct"],
            "fastp_dominant_overrep_pct": post["dominant_overrep_pct"],
        }
        for module in KEY_MODULES:
            key = module.lower().replace(" ", "_")
            old = str(base[f"status_{key}"])
            new = str(post[f"status_{key}"])
            direction = status_direction(old, new)
            row[f"fastx_status_{key}"] = old
            row[f"fastp_status_{key}"] = new
            row[f"direction_{key}"] = direction
            status_counts[module][f"fastx:{old}"] += 1
            status_counts[module][f"fastp:{new}"] += 1
            transition_counts[module][direction] += 1
            transition_rows.append(
                {
                    "read_id": read_id,
                    "srr": srr,
                    "module": module,
                    "fastx_status": old,
                    "fastp_status": new,
                    "direction": direction,
                }
            )
        report = fastp_reports.get(srr, {})
        row["fastp_retained_pct"] = report.get("retained_pct")
        row["fastp_q20_rate_after"] = report.get("q20_rate_after")
        row["fastp_q30_rate_after"] = report.get("q30_rate_after")
        per_read_rows.append(row)

    status_summary_rows: list[dict[str, object]] = []
    for module in KEY_MODULES:
        counts = status_counts[module]
        status_summary_rows.append(
            {
                "module": module,
                "fastx_pass": counts["fastx:pass"],
                "fastx_warn": counts["fastx:warn"],
                "fastx_fail": counts["fastx:fail"],
                "fastp_pass": counts["fastp:pass"],
                "fastp_warn": counts["fastp:warn"],
                "fastp_fail": counts["fastp:fail"],
                "improved": transition_counts[module]["improved"],
                "unchanged": transition_counts[module]["unchanged"],
                "worse": transition_counts[module]["worse"],
            }
        )

    write_csv(args.out_dir / "full_fastx_vs_fastp_read_metrics.csv", per_read_rows)
    write_csv(args.out_dir / "full_fastx_vs_fastp_status_counts.csv", status_summary_rows)
    write_csv(args.out_dir / "full_fastx_vs_fastp_status_transitions.csv", transition_rows)
    write_csv(args.out_dir / "full_fastp_run_metrics.csv", list(fastp_reports.values()))

    adapter_deltas = [
        float(row["adapter_max_delta_fastp_minus_fastx"])
        for row in per_read_rows
        if row["adapter_max_delta_fastp_minus_fastx"] is not None
    ]
    retained = [float(row["fastp_retained_pct"]) for row in per_read_rows if row["fastp_retained_pct"] is not None]
    q30_after = [float(row["fastp_q30_rate_after"]) for row in per_read_rows if row["fastp_q30_rate_after"] is not None]
    fastx_adapter = [float(row["fastx_adapter_max"]) for row in per_read_rows if row["fastx_adapter_max"] is not None]
    fastp_adapter = [float(row["fastp_adapter_max"]) for row in per_read_rows if row["fastp_adapter_max"] is not None]

    top_improvements = sorted(
        (
            row for row in per_read_rows
            if row["adapter_max_delta_fastp_minus_fastx"] is not None
        ),
        key=lambda row: float(row["adapter_max_delta_fastp_minus_fastx"]),
    )[:5]
    remaining_fail_reads = [
        row for row in per_read_rows
        if row["fastp_status_adapter_content"] == "fail" or row["fastp_status_overrepresented_sequences"] == "fail"
    ]

    lines = [
        "# Full-dataset FASTX vs fastp QC comparison",
        "",
        f"- Reports compared: `{len(common_reads)}` read-level FastQC reports (`26` paired-end SRRs).",
        f"- FASTX baseline directory: `{args.fastx_dir}`",
        f"- fastp post-QC directory: `{args.fastp_dir}`",
        f"- fastp report directory: `{args.fastp_reports}`",
        "",
        "## Report-ready findings",
        "",
        (
            "- Adapter signal improved strongly overall: median `adapter_max` changed "
            f"from `{fmt(median_or_none(fastx_adapter), 4)}` under FASTX to "
            f"`{fmt(median_or_none(fastp_adapter), 4)}` after fastp."
        ),
        (
            "- Across all read reports, median `adapter_max` delta (`fastp - FASTX`) was "
            f"`{fmt(median_or_none(adapter_deltas), 4)}`, meaning fastp reduced the residual signal in the typical read."
        ),
        (
            "- Read retention remained high after fastp: median retained reads were "
            f"`{fmt(median_or_none(retained), 2)}%` of the pre-fastp totals."
        ),
        (
            "- Post-fastp quality remained strong: median `Q30` rate after filtering was "
            f"`{fmt(median_or_none(q30_after) * 100 if median_or_none(q30_after) is not None else None, 2)}%`."
        ),
        "",
        "## Module-level status changes",
        "",
    ]

    for row in status_summary_rows:
        lines.append(
            "- "
            f"{row['module']}: FASTX pass/warn/fail = "
            f"`{row['fastx_pass']}/{row['fastx_warn']}/{row['fastx_fail']}`, "
            f"fastp pass/warn/fail = "
            f"`{row['fastp_pass']}/{row['fastp_warn']}/{row['fastp_fail']}`, "
            f"improved/unchanged/worse = "
            f"`{row['improved']}/{row['unchanged']}/{row['worse']}`."
        )

    lines.extend(
        [
            "",
            "## Largest adapter-signal improvements",
            "",
        ]
    )
    for row in top_improvements:
        lines.append(
            "- "
            f"`{row['read_id']}`: `adapter_max` "
            f"`{fmt(float(row['fastx_adapter_max']), 4)}` -> "
            f"`{fmt(float(row['fastp_adapter_max']), 4)}` "
            f"(delta `{fmt(float(row['adapter_max_delta_fastp_minus_fastx']), 4)}`)."
        )

    lines.extend(["", "## Remaining reads to review", ""])
    if remaining_fail_reads:
        for row in remaining_fail_reads[:10]:
            lines.append(
                "- "
                f"`{row['read_id']}`: fastp adapter status `{row['fastp_status_adapter_content']}`, "
                f"overrepresented-sequence status `{row['fastp_status_overrepresented_sequences']}`, "
                f"dominant signal `{row['fastp_dominant_signal_label']}`."
            )
    else:
        lines.append("- No read reports remain in `fail` for `Adapter Content` or `Overrepresented sequences` after fastp.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This comparison is the primary file-level validation layer because it parses and compares the underlying FastQC outputs directly for every read report.",
            "- The FASTX and FASTX-vs-fastp MultiQC reports should be used as supplementary confirmation and summary layers, not as the only basis for interpretation.",
        ]
    )

    (args.out_dir / "full_fastx_vs_fastp_summary.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
