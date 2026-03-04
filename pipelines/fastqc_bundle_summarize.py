#!/usr/bin/env python3
import argparse
import csv
import io
import re
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


STATUS_RANK = {"pass": 0, "warn": 1, "fail": 2}
RANK_TO_STATUS = {0: "pass", 1: "warn", 2: "fail"}

MODULE_KEY_MAP = {
    "Adapter Content": "adapter_content",
    "Basic Statistics": "basic_statistics",
    "Overrepresented sequences": "overrepresented_sequences",
    "Per base N content": "per_base_n_content",
    "Per base sequence content": "per_base_sequence_content",
    "Per base sequence quality": "per_base_sequence_quality",
    "Per sequence GC content": "per_sequence_gc_content",
    "Per sequence quality scores": "per_sequence_quality_scores",
    "Per tile sequence quality": "per_tile_sequence_quality",
    "Sequence Duplication Levels": "sequence_duplication_levels",
    "Sequence Length Distribution": "sequence_length_distribution",
}


@dataclass(frozen=True)
class FastQCRecord:
    report_id: str
    srr: str
    read: str
    module: str
    module_key: str
    status: str


def _module_key(module_name: str) -> str:
    if module_name in MODULE_KEY_MAP:
        return MODULE_KEY_MAP[module_name]
    return re.sub(r"[^a-z0-9]+", "_", module_name.lower()).strip("_")


def _read_summary_txt(z: zipfile.ZipFile) -> str:
    summary_paths = [p for p in z.namelist() if p.endswith("/summary.txt")]
    if not summary_paths:
        raise ValueError("missing summary.txt in fastqc zip")
    if len(summary_paths) > 1:
        summary_paths.sort()
    return z.read(summary_paths[0]).decode("utf-8", errors="replace")


def _parse_report_id_from_zip(zip_path: Path) -> str:
    name = zip_path.name
    m = re.match(r"^(SRR\d+_[12])_fastqc\.zip$", name)
    if not m:
        m = re.match(r"^(SRR\d+_[12])\.trim_fastqc\.zip$", name)
    if not m:
        raise ValueError(f"unrecognized FastQC zip name: {name}")
    return m.group(1)


def _srr_read_from_report_id(report_id: str) -> tuple[str, str]:
    m = re.match(r"^(SRR\d+)_([12])$", report_id)
    if not m:
        raise ValueError(f"unrecognized report_id: {report_id}")
    return m.group(1), m.group(2)


def parse_fastqc_zip(zip_path: Path, stage: str) -> list[FastQCRecord]:
    report_id = _parse_report_id_from_zip(zip_path)
    srr, read = _srr_read_from_report_id(report_id)
    out: list[FastQCRecord] = []
    with zipfile.ZipFile(zip_path, "r") as z:
        summary = _read_summary_txt(z)
    for line in summary.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0].strip().lower()
        module = parts[1].strip()
        if status not in STATUS_RANK:
            continue
        out.append(
            FastQCRecord(
                report_id=report_id,
                srr=srr,
                read=read,
                module=module,
                module_key=_module_key(module),
                status=status,
            )
        )
    return out


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def df_to_markdown_table(rows: list[dict], cols: list[str]) -> str:
    out = []
    out.append("| " + " | ".join(cols) + " |")
    out.append("| " + " | ".join(["---"] * len(cols)) + " |")
    for r in rows:
        row = []
        for c in cols:
            v = str(r.get(c, "")).replace("\n", " ").replace("|", "\\|")
            row.append(v)
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qc-bundle", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument(
        "--stage",
        default="raw",
        help="Label for outputs. Also controls which FastQC ZIP naming convention to parse: "
        "'raw' expects SRR*_fastqc.zip, 'trim'/'trimmed' expects SRR*.trim_fastqc.zip.",
    )
    args = ap.parse_args(argv)

    qc_bundle: Path = args.qc_bundle
    out_dir: Path = args.out_dir
    stage: str = args.stage

    stage_norm = stage.strip().lower()
    if stage_norm in {"trim", "trimmed"}:
        zips = sorted(qc_bundle.glob("SRR*.trim_fastqc.zip"))
    else:
        zips = sorted(qc_bundle.glob("SRR*_fastqc.zip"))
    if not zips:
        raise SystemExit(
            f"no FastQC zips found under: {qc_bundle} "
            f"(stage={stage!r}; expected naming: "
            f"{'SRR*.trim_fastqc.zip' if stage_norm in {'trim','trimmed'} else 'SRR*_fastqc.zip'})"
        )

    records: list[FastQCRecord] = []
    for zp in zips:
        records.extend(parse_fastqc_zip(zp, stage=stage))

    status_by_report_rows: list[dict] = []
    for r in records:
        status_by_report_rows.append(
            {
                "stage": stage,
                "report_id": r.report_id,
                "srr": r.srr,
                "read": r.read,
                "module_key": r.module_key,
                "module": r.module,
                "status": r.status,
            }
        )

    write_csv(
        out_dir / "fastqc_status_by_report_long.csv",
        status_by_report_rows,
        ["stage", "report_id", "srr", "read", "module_key", "module", "status"],
    )

    module_counts: dict[str, Counter] = defaultdict(Counter)
    module_label: dict[str, str] = {}
    for r in records:
        module_counts[r.module_key][r.status] += 1
        module_label[r.module_key] = r.module

    module_count_rows: list[dict] = []
    for module_key in sorted(module_counts.keys()):
        c = module_counts[module_key]
        n = sum(c.values())
        module_count_rows.append(
            {
                "module_key": module_key,
                "module": module_label.get(module_key, module_key),
                "pass": c.get("pass", 0),
                "warn": c.get("warn", 0),
                "fail": c.get("fail", 0),
                "n": n,
            }
        )

    write_csv(
        out_dir / "fastqc_module_counts.csv",
        module_count_rows,
        ["module_key", "module", "pass", "warn", "fail", "n"],
    )

    severity_by_report: dict[tuple[str, str], dict] = {}
    for row in status_by_report_rows:
        key = (row["stage"], row["report_id"])
        if key not in severity_by_report:
            severity_by_report[key] = {
                "stage": row["stage"],
                "report_id": row["report_id"],
                "srr": row["srr"],
                "read": row["read"],
                "fail_count": 0,
                "warn_count": 0,
            }
        if row["status"] == "fail":
            severity_by_report[key]["fail_count"] += 1
        elif row["status"] == "warn":
            severity_by_report[key]["warn_count"] += 1

    severity_rows: list[dict] = []
    for v in severity_by_report.values():
        v = dict(v)
        v["severity"] = int(v["fail_count"]) * 3 + int(v["warn_count"])
        severity_rows.append(v)

    severity_rows.sort(key=lambda d: (-int(d["severity"]), d["report_id"]))
    write_csv(
        out_dir / "fastqc_severity_by_report.csv",
        severity_rows,
        ["stage", "report_id", "srr", "read", "fail_count", "warn_count", "severity"],
    )

    write_csv(
        out_dir / "fastqc_top_problematic_reports.csv",
        severity_rows[:30],
        ["stage", "report_id", "srr", "read", "fail_count", "warn_count", "severity"],
    )

    severity_by_srr: dict[tuple[str, str], dict] = {}
    for r in severity_rows:
        key = (r["stage"], r["srr"])
        if key not in severity_by_srr:
            severity_by_srr[key] = {
                "stage": r["stage"],
                "srr": r["srr"],
                "fail_total": 0,
                "warn_total": 0,
                "severity": 0,
            }
        severity_by_srr[key]["fail_total"] += int(r["fail_count"])
        severity_by_srr[key]["warn_total"] += int(r["warn_count"])
        severity_by_srr[key]["severity"] += int(r["severity"])

    severity_srr_rows = list(severity_by_srr.values())
    severity_srr_rows.sort(key=lambda d: (-int(d["severity"]), d["srr"]))

    write_csv(
        out_dir / "fastqc_severity_by_srr.csv",
        severity_srr_rows,
        ["stage", "srr", "fail_total", "warn_total", "severity"],
    )
    write_csv(
        out_dir / "fastqc_top_severity_srrs.csv",
        severity_srr_rows[:20],
        ["stage", "srr", "fail_total", "warn_total", "severity"],
    )

    srr_module_rank: dict[tuple[str, str, str], int] = {}
    for row in status_by_report_rows:
        key = (row["stage"], row["srr"], row["module_key"])
        rank = STATUS_RANK[row["status"]]
        prev = srr_module_rank.get(key, -1)
        if rank > prev:
            srr_module_rank[key] = rank

    srr_status_long_rows: list[dict] = []
    for (st, srr, module_key), rank in sorted(srr_module_rank.items()):
        status = RANK_TO_STATUS.get(rank, "pass")
        srr_status_long_rows.append(
            {
                "stage": st,
                "srr": srr,
                "module_key": module_key,
                "module": module_label.get(module_key, module_key),
                "status": status,
            }
        )

    write_csv(
        out_dir / "fastqc_status_by_srr_module_long.csv",
        srr_status_long_rows,
        ["stage", "srr", "module_key", "module", "status"],
    )
    (out_dir / "fastqc_status_by_srr_module_long.md").write_text(
        df_to_markdown_table(
            srr_status_long_rows,
            ["stage", "srr", "module_key", "module", "status"],
        )
        + "\n"
    )

    by_module_status_srrs: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for r in srr_status_long_rows:
        if r["status"] not in {"warn", "fail"}:
            continue
        key = (r["module_key"], r["module"], r["status"])
        by_module_status_srrs[key].add(r["srr"])

    module_srr_rows: list[dict] = []
    for (module_key, module, status), srrs in sorted(by_module_status_srrs.items()):
        srr_list = sorted(srrs)
        module_srr_rows.append(
            {
                "module_key": module_key,
                "module": module,
                "status": status,
                "srr_count": len(srr_list),
                "srrs": ", ".join(srr_list),
            }
        )

    write_csv(
        out_dir / "fastqc_problem_srrs_by_module.csv",
        module_srr_rows,
        ["module_key", "module", "status", "srr_count", "srrs"],
    )
    (out_dir / "fastqc_problem_srrs_by_module.md").write_text(
        df_to_markdown_table(
            module_srr_rows,
            ["module_key", "module", "status", "srr_count", "srrs"],
        )
        + "\n"
    )

    summary = {
        "fastqc_reports": len({r.report_id for r in records}),
        "srr_runs": len({r.srr for r in records}),
        "modules": len({r.module_key for r in records}),
    }
    (out_dir / "fastqc_bundle_summary.txt").write_text(
        "\n".join([f"{k}: {v}" for k, v in summary.items()]) + "\n"
    )

    print(f"Wrote outputs to: {out_dir}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
