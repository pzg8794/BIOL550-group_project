#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Download FASTQs for a list of SRR runs using SRA Toolkit (prefetch + fasterq-dump).

Usage:
  bash scripts/download_fastq_sratoolkit_from_runs.sh \
    --runs-file metadata/PRJNA1277581/runs.filtered.txt \
    --out-dir data/PRJNA1277581 \
    --threads 4

Notes:
  - Requires SRA Toolkit on PATH (prefetch + fasterq-dump).
  - Writes paired FASTQs as <SRR>_1.fastq.gz and <SRR>_2.fastq.gz in --out-dir/<SRR>/.
  - Re-running is safe: it skips runs whose gzipped FASTQs already exist.
USAGE
}

RUNS_FILE=""
OUT_DIR=""
THREADS="4"
FORCE="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --runs-file) RUNS_FILE="$2"; shift 2 ;;
    --out-dir) OUT_DIR="$2"; shift 2 ;;
    --threads) THREADS="$2"; shift 2 ;;
    --force) FORCE="1"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

[[ -n "$RUNS_FILE" ]] || { echo "ERROR: --runs-file is required" >&2; exit 2; }
[[ -n "$OUT_DIR" ]] || { echo "ERROR: --out-dir is required" >&2; exit 2; }
[[ -f "$RUNS_FILE" ]] || { echo "ERROR: missing runs file: $RUNS_FILE" >&2; exit 2; }

command -v prefetch >/dev/null 2>&1 || { echo "ERROR: missing prefetch (SRA Toolkit)" >&2; exit 127; }
command -v fasterq-dump >/dev/null 2>&1 || { echo "ERROR: missing fasterq-dump (SRA Toolkit)" >&2; exit 127; }
command -v gzip >/dev/null 2>&1 || { echo "ERROR: missing gzip" >&2; exit 127; }

mkdir -p "$OUT_DIR"

echo "runs_file: $RUNS_FILE"
echo "out_dir:   $OUT_DIR"
echo "threads:   $THREADS"
echo "force:     $FORCE"
echo

while read -r SRR; do
  SRR="$(echo "$SRR" | tr -d '\r' | xargs || true)"
  [[ -n "$SRR" ]] || continue
  [[ "$SRR" != \#* ]] || continue

  RUN_DIR="$OUT_DIR/$SRR"
  mkdir -p "$RUN_DIR"
  SRA_DIR="$RUN_DIR/sra"
  mkdir -p "$SRA_DIR"

  R1_GZ="$RUN_DIR/${SRR}_1.fastq.gz"
  R2_GZ="$RUN_DIR/${SRR}_2.fastq.gz"

  if [[ -f "$R1_GZ" && -f "$R2_GZ" && "$FORCE" != "1" ]]; then
    echo "skip (exists): $SRR"
    continue
  fi

  echo
  echo "== $SRR =="

  # 1) Download runfile into a per-run folder (avoids creating SRR* dirs in repo root)
  prefetch -O "$SRA_DIR" "$SRR"

  # Prefer dumping from the downloaded file (so we don't re-download and we keep IO local).
  # prefetch typically creates: $SRA_DIR/$SRR/<file>
  SRA_INPUT="$SRR"
  if [[ -d "$SRA_DIR/$SRR" ]]; then
    SRA_FILE="$(find "$SRA_DIR/$SRR" -maxdepth 1 -type f 2>/dev/null | head -n 1 || true)"
    if [[ -n "${SRA_FILE:-}" ]]; then
      SRA_INPUT="$SRA_FILE"
    fi
  fi

  # 2) Convert to FASTQ (paired) into RUN_DIR
  fasterq-dump --split-files --threads "$THREADS" --outdir "$RUN_DIR" "$SRA_INPUT"

  # 3) Gzip outputs (keep originals only temporarily to save space)
  gzip -f "$RUN_DIR/${SRR}_1.fastq" "$RUN_DIR/${SRR}_2.fastq"

  # Cleanup downloaded runfile folder (keeps only FASTQ.gz outputs under data/<ACC>/<SRR>/)
  rm -rf "$SRA_DIR" || true
done < "$RUNS_FILE"

echo
echo "Done."
