#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path


def md5_first_records(path: Path, n_records: int) -> tuple[str, int, str]:
    h = hashlib.md5()
    opener = gzip.open if path.name.endswith(".gz") else open
    lines_read = 0
    first_header = ""

    with opener(path, "rb") as f:
        while lines_read < 4 * n_records:
            line = f.readline()
            if not line:
                break
            if lines_read == 0:
                first_header = line.decode("utf-8", "replace").strip()
            h.update(line)
            lines_read += 1

    return h.hexdigest(), lines_read // 4, first_header


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compare FASTQ subsets by hashing the first N records (R1/R2).")
    p.add_argument("--srr", required=True, help="SRR accession (used to locate <SRR>_1.fastq.gz and <SRR>_2.fastq.gz).")
    p.add_argument("--n-records", type=int, required=True, help="Number of FASTQ records to hash (per mate).")
    p.add_argument("--a-dir", required=True, help="Directory containing FASTQs for dataset A.")
    p.add_argument("--b-dir", required=True, help="Directory containing FASTQs for dataset B.")
    args = p.parse_args(argv)

    srr = args.srr.strip()
    n = args.n_records
    a_dir = Path(args.a_dir).expanduser().resolve()
    b_dir = Path(args.b_dir).expanduser().resolve()

    for mate in (1, 2):
        a = a_dir / f"{srr}_{mate}.fastq.gz"
        b = b_dir / f"{srr}_{mate}.fastq.gz"
        if not a.exists():
            raise SystemExit(f"Missing: {a}")
        if not b.exists():
            raise SystemExit(f"Missing: {b}")

        a_md5, a_n, a_hdr = md5_first_records(a, n)
        b_md5, b_n, b_hdr = md5_first_records(b, n)

        print(f"R{mate}:")
        print(f"  A: {a.name}  records_hashed={a_n}  first_header={a_hdr}")
        print(f"  B: {b.name}  records_hashed={b_n}  first_header={b_hdr}")
        print(f"  md5(first {n} records):")
        print(f"    A={a_md5}")
        print(f"    B={b_md5}")
        print(f"    MATCH={a_md5 == b_md5}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

