#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

BASE="${BASE:-/home/pzg8794/mouse_qc_remediation}"
OUT_BASE="${OUT_BASE:-$BASE/multiqc/final_fastp_all_srrs}"
REPORT_DIR="${REPORT_DIR:-$OUT_BASE/report}"
REPORT_NAME="${REPORT_NAME:-mouse_fastp_all_srrs_multiqc.html}"

FASTP_FASTQC_DIR="${FASTP_FASTQC_DIR:-$BASE/output/fastqc_after/fastp}"
FASTP_REPORT_DIR="${FASTP_REPORT_DIR:-$BASE/output/fastp/reports}"

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

command -v multiqc >/dev/null 2>&1 || die "multiqc not found in PATH"
[[ -d "$FASTP_FASTQC_DIR" ]] || die "missing fastp FastQC directory: $FASTP_FASTQC_DIR"
[[ -d "$FASTP_REPORT_DIR" ]] || die "missing fastp report directory: $FASTP_REPORT_DIR"

mkdir -p "$REPORT_DIR"

multiqc \
  --force \
  --dirs \
  --dirs-depth 1 \
  "$FASTP_FASTQC_DIR" \
  "$FASTP_REPORT_DIR" \
  --outdir "$REPORT_DIR" \
  --filename "$REPORT_NAME"
