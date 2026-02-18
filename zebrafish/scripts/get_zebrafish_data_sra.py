#!/usr/bin/env python3
"""
Fetch zebrafish (Danio rerio) RNA-seq runs from NCBI SRA via the Entrez API and
produce reproducible run metadata + run lists for downstream downloading.

Default dataset: PRJNA1277581 (zebrafish retina regeneration; SRP592470).

Outputs (in --out-dir):
  - runinfo.csv                (raw runinfo from SRA)
  - runinfo.filtered.csv       (filtered subset)
  - runs.all.txt               (SRR accessions)
  - runs.filtered.txt          (filtered SRR accessions)
  - download_urls.filtered.txt (optional; direct SRA "download_path" URLs)

This script does NOT require the SRA Toolkit, but you can use the produced SRR
lists with prefetch/fasterq-dump if those are installed.
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

@dataclass(frozen=True)
class Filters:
    organism: Optional[str]
    library_strategy: Optional[str]
    library_layout: Optional[str]
    min_spots: Optional[int]
    min_avg_length: Optional[int]


def _which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def _run_edirect_runinfo(acc: str) -> str:
    esearch = _which("esearch")
    efetch = _which("efetch")
    if not esearch or not efetch:
        raise RuntimeError("Entrez Direct not found (need `esearch` and `efetch` in PATH).")

    p1 = subprocess.run(
        [esearch, "-db", "sra", "-query", acc],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    p2 = subprocess.run(
        [efetch, "-format", "runinfo"],
        check=True,
        input=p1.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if not p2.stdout.strip():
        raise RuntimeError(f"Empty runinfo returned for accession/query: {acc}")
    return p2.stdout


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "biol550-sra-fetch/1.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        body = resp.read()
    return body.decode("utf-8", errors="replace")


def _run_eutils_runinfo(acc: str) -> str:
    term = urllib.parse.quote(acc)
    esearch_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=sra&term={term}&usehistory=y&retmax=100000"
    )
    xml = _http_get(esearch_url)
    root = ET.fromstring(xml)
    webenv = root.findtext("./WebEnv")
    query_key = root.findtext("./QueryKey")
    count = root.findtext("./Count")
    if not webenv or not query_key:
        raise RuntimeError(f"Failed to resolve WebEnv/QueryKey from ESearch for: {acc}")

    efetch_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=sra&query_key={urllib.parse.quote(query_key)}&WebEnv={urllib.parse.quote(webenv)}"
        "&rettype=runinfo&retmode=text"
    )
    txt = _http_get(efetch_url, timeout_s=120)
    if not txt.strip():
        raise RuntimeError(f"Empty runinfo returned from EFetch for: {acc} (Count={count})")
    return txt


def fetch_runinfo(acc: str) -> str:
    # Prefer edirect when available (it uses the same Entrez API but is stable in class setups).
    if _which("esearch") and _which("efetch"):
        return _run_edirect_runinfo(acc)
    return _run_eutils_runinfo(acc)


def parse_runinfo_csv(text: str) -> list[dict[str, str]]:
    reader = csv.DictReader(text.splitlines())
    rows = [r for r in reader]
    if not rows:
        raise RuntimeError("RunInfo CSV parsed to zero rows (unexpected).")
    if "Run" not in rows[0]:
        raise RuntimeError("RunInfo CSV missing expected `Run` column.")
    return rows


def _to_int(value: str) -> Optional[int]:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except Exception:
        return None


def filter_rows(rows: Iterable[dict[str, str]], f: Filters) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for r in rows:
        if f.organism and (r.get("ScientificName") or "").strip() != f.organism:
            continue
        if f.library_strategy and (r.get("LibraryStrategy") or "").strip() != f.library_strategy:
            continue
        if f.library_layout and (r.get("LibraryLayout") or "").strip() != f.library_layout:
            continue

        if f.min_avg_length is not None:
            avg_len = _to_int(r.get("avgLength", ""))
            if avg_len is None or avg_len < f.min_avg_length:
                continue

        if f.min_spots is not None:
            spots = _to_int(r.get("spots", ""))
            if spots is None or spots < f.min_spots:
                continue

        out.append(r)
    return out


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_lines(path: Path, lines: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        prog="get_zebrafish_data_sra.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Fetch SRA RunInfo and SRR lists for zebrafish (Danio rerio) RNA-seq data.",
        epilog=textwrap.dedent(
            """
            Examples:
              # Fetch runinfo + SRR lists (default dataset)
              python3 get_zebrafish_data_sra.py

              # Fetch a different BioProject and write to a custom dir
              python3 get_zebrafish_data_sra.py --acc PRJNA717662 --out-dir ./out/PRJNA717662

              # Produce URLs for direct SRA downloads (lite .sra files)
              python3 get_zebrafish_data_sra.py --write-download-urls
            """
        ),
    )
    p.add_argument("--acc", default="PRJNA1277581", help="SRA query/accession (e.g., PRJNA..., SRP..., SRX...).")
    p.add_argument(
        "--out-dir",
        default=str((Path(__file__).resolve().parent.parent / "metadata" / "PRJNA1277581")),
        help="Output directory.",
    )
    p.add_argument("--organism", default="Danio rerio", help="ScientificName filter (exact match).")
    p.add_argument("--library-strategy", default="RNA-Seq", help="LibraryStrategy filter (exact match).")
    p.add_argument("--library-layout", default="PAIRED", help="LibraryLayout filter (exact match).")
    p.add_argument("--min-spots", type=int, default=40_000_000, help="Minimum `spots`.")
    p.add_argument("--min-avg-length", type=int, default=150, help="Minimum `avgLength`.")
    p.add_argument(
        "--max-runs",
        type=int,
        default=0,
        help="If >0, truncate filtered run list to first N runs (for testing).",
    )
    p.add_argument(
        "--write-download-urls",
        action="store_true",
        help="Write download URLs (from `download_path`) for filtered runs.",
    )
    args = p.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    runinfo_text = fetch_runinfo(args.acc)
    (out_dir / "runinfo.csv").write_text(runinfo_text, encoding="utf-8")

    rows = parse_runinfo_csv(runinfo_text)
    all_runs = [r["Run"].strip() for r in rows if (r.get("Run") or "").strip()]
    write_lines(out_dir / "runs.all.txt", all_runs)

    filters = Filters(
        organism=(args.organism or None),
        library_strategy=(args.library_strategy or None),
        library_layout=(args.library_layout or None),
        min_spots=args.min_spots,
        min_avg_length=args.min_avg_length,
    )
    filtered = filter_rows(rows, filters)
    if args.max_runs and args.max_runs > 0:
        filtered = filtered[: args.max_runs]

    if not filtered:
        raise RuntimeError(
            "No runs matched filters. Try relaxing filters (e.g., --organism '' --min-spots 0)."
        )

    write_csv(out_dir / "runinfo.filtered.csv", filtered)
    filtered_runs = [r["Run"].strip() for r in filtered if (r.get("Run") or "").strip()]
    write_lines(out_dir / "runs.filtered.txt", filtered_runs)

    if args.write_download_urls:
        urls = []
        for r in filtered:
            u = (r.get("download_path") or "").strip()
            if u:
                urls.append(u)
        write_lines(out_dir / "download_urls.filtered.txt", urls)

    print(f"Accession/query: {args.acc}")
    print(f"Output dir: {out_dir}")
    print(f"Runs (all): {len(all_runs)} -> {out_dir / 'runs.all.txt'}")
    print(f"Runs (filtered): {len(filtered_runs)} -> {out_dir / 'runs.filtered.txt'}")
    print(f"RunInfo: {out_dir / 'runinfo.csv'}")
    print(f"RunInfo (filtered): {out_dir / 'runinfo.filtered.csv'}")
    if args.write_download_urls:
        print(f"Download URLs: {out_dir / 'download_urls.filtered.txt'}")

    # Helpful next-step hints (don’t run anything heavy automatically).
    if shutil.which("prefetch") and shutil.which("fasterq-dump"):
        print("\nSRA Toolkit detected. Example download loop:")
        print(
            f"  while read -r SRR; do prefetch \"$SRR\" && fasterq-dump --split-files --threads 4 \"$SRR\"; done < {out_dir / 'runs.filtered.txt'}"
        )
    else:
        print("\nSRA Toolkit not detected in PATH (prefetch/fasterq-dump).")
        print("You can still use the SRR list to download later on the class server.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
