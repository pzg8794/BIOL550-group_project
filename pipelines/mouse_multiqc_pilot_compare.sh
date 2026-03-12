#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

BASE="${BASE:-/home/pzg8794/mouse_qc_remediation}"
OUT_BASE="${OUT_BASE:-$BASE/multiqc/pilot_compare}"
REPORT_DIR="${REPORT_DIR:-$OUT_BASE/report}"
REPORT_NAME="${REPORT_NAME:-mouse_pilot_compare_multiqc.html}"

RAW_DIR="${RAW_DIR:-$BASE/baseline/qc_bundle_raw}"
FASTX_DIR="${FASTX_DIR:-$BASE/baseline/qc_bundle_trimmed}"
FASTP_FASTQC_DIR="${FASTP_FASTQC_DIR:-$BASE/output/fastqc_after/fastp}"
CUTADAPT_FASTQC_DIR="${CUTADAPT_FASTQC_DIR:-$BASE/output/fastqc_after/cutadapt}"
FASTP_REPORT_DIR="${FASTP_REPORT_DIR:-$BASE/output/fastp/reports}"
CUTADAPT_REPORT_DIR="${CUTADAPT_REPORT_DIR:-$BASE/output/cutadapt/reports}"

READS=(
  SRR30333754_1 SRR30333754_2
  SRR30333756_1 SRR30333756_2
  SRR30333743_1 SRR30333743_2
)

SRRS=(
  SRR30333754
  SRR30333756
  SRR30333743
)

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

command -v multiqc >/dev/null 2>&1 || die "multiqc not found in PATH"

mkdir -p "$OUT_BASE/raw" "$OUT_BASE/fastx" "$OUT_BASE/fastp" "$OUT_BASE/cutadapt" "$REPORT_DIR"

find "$OUT_BASE/raw" -maxdepth 1 -type l -delete
find "$OUT_BASE/fastx" -maxdepth 1 -type l -delete
find "$OUT_BASE/fastp" -maxdepth 1 -type l -delete
find "$OUT_BASE/cutadapt" -maxdepth 1 -type l -delete

for read_id in "${READS[@]}"; do
  [[ -f "$RAW_DIR/${read_id}_fastqc.zip" ]] || die "missing raw FastQC zip: $RAW_DIR/${read_id}_fastqc.zip"
  [[ -f "$FASTX_DIR/${read_id}.trim_fastqc.zip" ]] || die "missing FASTX FastQC zip: $FASTX_DIR/${read_id}.trim_fastqc.zip"
  [[ -f "$FASTP_FASTQC_DIR/${read_id}.fastp_fastqc.zip" ]] || die "missing fastp FastQC zip: $FASTP_FASTQC_DIR/${read_id}.fastp_fastqc.zip"
  [[ -f "$CUTADAPT_FASTQC_DIR/${read_id}.cutadapt_fastqc.zip" ]] || die "missing cutadapt FastQC zip: $CUTADAPT_FASTQC_DIR/${read_id}.cutadapt_fastqc.zip"

  ln -sfn "$RAW_DIR/${read_id}_fastqc.zip" "$OUT_BASE/raw/${read_id}_fastqc.zip"
  ln -sfn "$FASTX_DIR/${read_id}.trim_fastqc.zip" "$OUT_BASE/fastx/${read_id}.trim_fastqc.zip"
  ln -sfn "$FASTP_FASTQC_DIR/${read_id}.fastp_fastqc.zip" "$OUT_BASE/fastp/${read_id}.fastp_fastqc.zip"
  ln -sfn "$CUTADAPT_FASTQC_DIR/${read_id}.cutadapt_fastqc.zip" "$OUT_BASE/cutadapt/${read_id}.cutadapt_fastqc.zip"
done

for srr in "${SRRS[@]}"; do
  [[ -f "$FASTP_REPORT_DIR/${srr}.fastp.json" ]] || die "missing fastp JSON report: $FASTP_REPORT_DIR/${srr}.fastp.json"
  [[ -f "$CUTADAPT_REPORT_DIR/${srr}.cutadapt.log" ]] || die "missing cutadapt log: $CUTADAPT_REPORT_DIR/${srr}.cutadapt.log"

  ln -sfn "$FASTP_REPORT_DIR/${srr}.fastp.json" "$OUT_BASE/fastp/${srr}.fastp.json"
  ln -sfn "$CUTADAPT_REPORT_DIR/${srr}.cutadapt.log" "$OUT_BASE/cutadapt/${srr}.cutadapt.log"
done

multiqc \
  --force \
  --dirs \
  --dirs-depth 1 \
  "$OUT_BASE/raw" \
  "$OUT_BASE/fastx" \
  "$OUT_BASE/fastp" \
  "$OUT_BASE/cutadapt" \
  --outdir "$REPORT_DIR" \
  --filename "$REPORT_NAME"
