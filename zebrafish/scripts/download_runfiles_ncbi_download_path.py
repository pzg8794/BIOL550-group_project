#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import subprocess
from pathlib import Path


def read_runs(path: Path) -> list[str]:
    runs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            runs.append(s)
    if not runs:
        raise SystemExit(f"No runs found in {path}")
    return runs


def load_download_paths(runinfo_csv: Path) -> dict[str, str]:
    with runinfo_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        out: dict[str, str] = {}
        for row in reader:
            run = (row.get("Run") or "").strip()
            url = (row.get("download_path") or "").strip()
            if run and url:
                out[run] = url
    if not out:
        raise SystemExit(f"No download_path values found in {runinfo_csv}")
    return out


def curl_download(url: str, dest: Path, *, force: bool) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        print("skip (exists):", dest)
        return

    cmd = [
        "curl",
        "-fL",
        "--retry",
        "3",
        "--retry-delay",
        "2",
        "--continue-at",
        "-",
        "-o",
        str(dest),
        url,
    ]
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Download SRA run files using NCBI RunInfo `download_path` URLs (no SRA Toolkit required). "
            "Input: a run list file + runinfo.csv."
        )
    )
    p.add_argument("--acc", required=True, help="BioProject / query label (used only for path defaults).")
    p.add_argument("--runs-file", required=True, help="Text file with one SRR per line.")
    p.add_argument("--runinfo-csv", required=True, help="SRA runinfo.csv containing a `download_path` column.")
    p.add_argument(
        "--base-dir",
        default="zebrafish/data/runfiles",
        help="Base output directory (default: zebrafish/data/runfiles).",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if files exist.",
    )
    args = p.parse_args(argv)

    runs_file = Path(args.runs_file)
    runinfo_csv = Path(args.runinfo_csv)
    base_dir = Path(args.base_dir)

    if not runs_file.exists():
        raise SystemExit(f"Missing runs file: {runs_file}")
    if not runinfo_csv.exists():
        raise SystemExit(f"Missing runinfo CSV: {runinfo_csv}")

    if not shutil_which("curl"):
        raise SystemExit("Missing required tool: curl")

    runs = read_runs(runs_file)
    paths = load_download_paths(runinfo_csv)

    missing = [r for r in runs if r not in paths]
    if missing:
        raise SystemExit(f"Missing download_path for runs: {missing[:10]} (total missing={len(missing)})")

    for run in runs:
        url = paths[run]
        fname = url.split("/")[-1]

        out_dir = base_dir / args.acc / run / "sra"
        dest = out_dir / fname
        curl_download(url, dest, force=args.force)

        # Stable symlink: <run>.sra -> downloaded filename (lite/full)
        link = out_dir / f"{run}.sra"
        try:
            if link.exists() or link.is_symlink():
                link.unlink()
            link.symlink_to(dest.name)
        except Exception as e:
            print("WARN: could not create symlink", link, "->", dest.name, ":", e)

    print("Done.")
    return 0


def shutil_which(cmd: str) -> str | None:
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = Path(d) / cmd
        if p.exists() and os.access(p, os.X_OK):
            return str(p)
    return None


if __name__ == "__main__":
    raise SystemExit(main())

