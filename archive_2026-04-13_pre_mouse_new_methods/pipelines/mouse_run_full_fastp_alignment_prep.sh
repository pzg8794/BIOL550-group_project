#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

ROOT="${ROOT:-/home/zebrafish/mouse/PRJNA1017789_parallel}"
BASE="${BASE:-/home/pzg8794/mouse_qc_remediation}"
OUT_BASE="${OUT_BASE:-$BASE/output}"
SCRIPT_DIR="${SCRIPT_DIR:-$BASE/scripts}"
RUNS_FILE="${RUNS_FILE:-/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt}"

FASTP_DONE="${FASTP_DONE:-$OUT_BASE/fastp/full_fastp_all_srrs.completed}"
MULTIQC_DONE="${MULTIQC_DONE:-$BASE/multiqc/final_fastp_all_srrs/mouse_fastp_all_srrs_multiqc.completed}"

mkdir -p "$OUT_BASE/fastp/out" "$OUT_BASE/fastp/reports" "$OUT_BASE/fastqc_after/fastp"
find "$OUT_BASE/fastp/out" -maxdepth 1 -type f -delete
find "$OUT_BASE/fastp/reports" -maxdepth 1 -type f -delete
find "$OUT_BASE/fastqc_after/fastp" -maxdepth 1 -type f -delete
rm -rf "$BASE/multiqc/final_fastp_all_srrs"
mkdir -p "$BASE/multiqc/final_fastp_all_srrs"
rm -f "$FASTP_DONE" "$MULTIQC_DONE"

echo "== start $(date '+%F %T') =="
echo "ROOT=$ROOT"
echo "BASE=$BASE"
echo "RUNS_FILE=$RUNS_FILE"

while read -r srr; do
  [[ -n "$srr" ]] || continue
  echo "-- fastp $srr --"
  ROOT="$ROOT" OUT_BASE="$OUT_BASE" FASTP_THREADS="${FASTP_THREADS:-2}" FASTQC_THREADS="${FASTQC_THREADS:-1}" \
    bash "$SCRIPT_DIR/qc_remed_fastp_one_srr.sh" "$srr"
done < "$RUNS_FILE"

date > "$FASTP_DONE"
echo "-- MultiQC final fastp report --"
BASE="$BASE" \
OUT_BASE="$BASE/multiqc/final_fastp_all_srrs" \
REPORT_DIR="$BASE/multiqc/final_fastp_all_srrs/report" \
REPORT_NAME="mouse_fastp_all_srrs_multiqc.html" \
  bash "$SCRIPT_DIR/mouse_multiqc_final_fastp.sh"
date > "$MULTIQC_DONE"

echo "== done $(date '+%F %T') =="
