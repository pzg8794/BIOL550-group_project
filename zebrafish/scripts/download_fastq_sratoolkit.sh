#!/usr/bin/env bash
set -euo pipefail

# Downloads a subset (or all) SRRs from `metadata/PRJNA1277581/runs.filtered.txt`
# and converts to gzipped FASTQs using SRA Toolkit (`prefetch`, `fasterq-dump`).
#
# Intended to run on the class server (or any machine) where sra-tools is installed.
# Output FASTQs go to `data/raw/` (gitignored).

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ACC="PRJNA1277581"
RUNS_FILE="$ROOT_DIR/metadata/$ACC/runs.filtered.txt"
OUT_DIR="$ROOT_DIR/data/raw/$ACC"

command -v prefetch >/dev/null 2>&1 || { echo "Missing: prefetch (SRA Toolkit)"; exit 1; }
command -v fasterq-dump >/dev/null 2>&1 || { echo "Missing: fasterq-dump (SRA Toolkit)"; exit 1; }

mkdir -p "$OUT_DIR"

if [[ ! -f "$RUNS_FILE" ]]; then
  echo "Missing SRR list: $RUNS_FILE"
  echo "Run: python3 \"$ROOT_DIR/scripts/get_zebrafish_data_sra.py\""
  exit 1
fi

echo "Reading runs from: $RUNS_FILE"
echo "Writing FASTQs to:  $OUT_DIR"

while read -r SRR; do
  [[ -z "${SRR}" ]] && continue
  echo "==> $SRR"
  prefetch "$SRR"
  fasterq-dump --split-files --threads 4 --outdir "$OUT_DIR" "$SRR"
  gzip -f "$OUT_DIR/${SRR}"_*.fastq
done < "$RUNS_FILE"

echo "Done."

