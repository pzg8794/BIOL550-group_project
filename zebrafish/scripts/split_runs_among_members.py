#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def read_runs(path: Path) -> list[str]:
    runs: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            runs.append(s)
    if not runs:
        raise SystemExit(f"No runs found in {path}")
    return runs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Split a run list into per-member files (round-robin).")
    p.add_argument("--runs-file", required=True, help="Input runs file (one SRR per line).")
    p.add_argument(
        "--members",
        nargs="+",
        required=True,
        help="Member names (e.g., piter nikhi samuel). Output filenames use these.",
    )
    p.add_argument(
        "--out-dir",
        required=True,
        help="Output directory for per-member run lists.",
    )
    p.add_argument(
        "--prefix",
        default="runs.member",
        help="Output filename prefix (default: runs.member).",
    )
    args = p.parse_args(argv)

    runs_file = Path(args.runs_file)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    runs = read_runs(runs_file)
    members = [m.strip() for m in args.members if m.strip()]
    if not members:
        raise SystemExit("No members provided.")

    buckets: dict[str, list[str]] = {m: [] for m in members}
    for i, run in enumerate(runs):
        buckets[members[i % len(members)]].append(run)

    for m in members:
        out = out_dir / f"{args.prefix}.{m}.txt"
        out.write_text("".join(f"{r}\n" for r in buckets[m]), encoding="utf-8")
        print(f"{m}: {len(buckets[m])} -> {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

