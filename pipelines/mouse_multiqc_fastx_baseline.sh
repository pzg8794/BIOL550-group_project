#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

BASE="${BASE:-/home/pzg8794/mouse_qc_remediation}"
OUT_BASE="${OUT_BASE:-$BASE/multiqc/fastx_baseline_all_srrs}"
REPORT_DIR="${REPORT_DIR:-$OUT_BASE/report}"
REPORT_NAME="${REPORT_NAME:-mouse_fastx_baseline_all_srrs_multiqc.html}"

FASTX_DIR="${FASTX_DIR:-$BASE/baseline/qc_bundle_trimmed}"

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

command -v multiqc >/dev/null 2>&1 || die "multiqc not found in PATH"
[[ -d "$FASTX_DIR" ]] || die "missing FASTX FastQC directory: $FASTX_DIR"

mkdir -p "$REPORT_DIR"

multiqc \
  --force \
  --dirs \
  --dirs-depth 1 \
  "$FASTX_DIR" \
  --outdir "$REPORT_DIR" \
  --filename "$REPORT_NAME"
