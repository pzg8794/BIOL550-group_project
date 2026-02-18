#!/usr/bin/env bash
set -euo pipefail

# Download a small, fast-to-run subset of reads from 5 SRR runs for PRJNA1277581
# using NCBI SRA Toolkit `fastq-dump` (streaming) spot-range filters.
#
# This is intended as a *test* to validate that organization + tools work
# without downloading full multi-GB runs.
#
# Outputs land under:
#   data/test/PRJNA1277581/spots_<MAX_SPOTS>/<SRR>/
#
# Defaults:
#   - picks the 5 smallest runs (by `size_MB`) from metadata/runinfo.csv
#   - downloads spot IDs 1..MAX_SPOTS (paired-end via --split-3)
#
# You can override:
#   MAX_SPOTS=10000 bash scripts/download_test_5_runs_fastq.sh

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ACC="PRJNA1277581"
MAX_SPOTS="${MAX_SPOTS:-100000}"

command -v fastq-dump >/dev/null 2>&1 || { echo "Missing: fastq-dump (SRA Toolkit)"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Missing: python3"; exit 1; }
command -v gzip >/dev/null 2>&1 || { echo "Missing: gzip"; exit 1; }

META_DIR="$ROOT_DIR/metadata/$ACC"
RUNINFO="$META_DIR/runinfo.csv"
RUNS_FILE="$META_DIR/runs.test5.smallest_sizeMB.txt"

if [[ ! -f "$RUNINFO" ]]; then
  echo "Missing run metadata: $RUNINFO"
  echo "Run: python3 \"$ROOT_DIR/scripts/get_zebrafish_data_sra.py\""
  exit 1
fi

# Generate the 5-run list (smallest size_MB) if it doesn't exist yet.
if [[ ! -f "$RUNS_FILE" ]]; then
  : "${EXCLUDE_RUNS:=SRR34002423,SRR34002425}"
  python3 - <<'PY'
import csv
from pathlib import Path
import os

root = Path(__file__).resolve().parents[2]  # .../zebrafish
acc = "PRJNA1277581"
runinfo = root / "metadata" / acc / "runinfo.csv"
out = root / "metadata" / acc / "runs.test5.smallest_sizeMB.txt"
exclude = {x.strip() for x in (os.environ.get("EXCLUDE_RUNS") or "").split(",") if x.strip()}

rows = list(csv.DictReader(runinfo.read_text(encoding="utf-8").splitlines()))
vals = []
for r in rows:
    run = (r.get("Run") or "").strip()
    if not run:
        continue
    if run in exclude:
        continue
    try:
        size = float(r.get("size_MB") or "nan")
    except Exception:
        size = float("nan")
    if size == size:
        vals.append((size, run))

vals.sort()
small = [run for _, run in vals[:5]]
out.write_text("".join(f"{r}\n" for r in small), encoding="utf-8")
print(str(out))
PY
fi

OUT_ROOT="$ROOT_DIR/data/test/$ACC/spots_${MAX_SPOTS}"
LOG_DIR="$ROOT_DIR/data/test/$ACC/logs"
mkdir -p "$OUT_ROOT" "$LOG_DIR"

echo "Runs list:  $RUNS_FILE"
echo "Max spots:  $MAX_SPOTS (spot IDs 1..$MAX_SPOTS)"
echo "Output dir: $OUT_ROOT"
echo

while read -r SRR; do
  [[ -z "${SRR}" ]] && continue
  OUT_DIR="$OUT_ROOT/$SRR"
  mkdir -p "$OUT_DIR"

  LOG="$LOG_DIR/${SRR}.spots_${MAX_SPOTS}.log"
  echo "==> $SRR"
  echo "    out: $OUT_DIR"

  if ls "$OUT_DIR/${SRR}"_1.fastq.gz "$OUT_DIR/${SRR}"_2.fastq.gz >/dev/null 2>&1; then
    echo "    skip: FASTQ.gz already exists"
    continue
  fi

  # `fastq-dump` supports spot-range filters (-N/-X). This lets us grab a small
  # subset without downloading full runs.
  #
  # --split-3 yields mate-pair files *_1.fastq and *_2.fastq (and a *.fastq for
  # singletons, if any; not expected here but safe).
  fastq-dump --split-3 -N 1 -X "$MAX_SPOTS" -O "$OUT_DIR" "$SRR" 2>&1 | tee "$LOG"

  # Gzip the fastq outputs to keep the test dataset small.
  find "$OUT_DIR" -maxdepth 1 -type f -name "*.fastq" -print0 | xargs -0 gzip -f
done < "$RUNS_FILE"

echo
echo "Done. Test FASTQs are under: $OUT_ROOT"
