#!/usr/bin/env bash
set -euo pipefail

SRR="${1:-}"
ROOT="${ROOT:-/home/zebrafish/mouse/PRJNA1017789}"

RAW_DIR="${RAW_DIR:-$ROOT/sra_runs}"
OUT_BASE="${OUT_BASE:-$ROOT/qc_remediation}"

CUTADAPT_BIN="${CUTADAPT_BIN:-/usr/bin/cutadapt}"
FASTQC_BIN="${FASTQC_BIN:-/usr/local/bin/FASTQC_11.9/fastqc}"
FASTQC_THREADS="${FASTQC_THREADS:-2}"
CUTADAPT_CORES="${CUTADAPT_CORES:-4}"

TRIM_QUAL="${TRIM_QUAL:-20}"
MIN_LEN="${MIN_LEN:-30}"

# Required: adapters (set these based on FastQC Overrepresented sequences or kit docs)
ADAPTER_R1="${ADAPTER_R1:-}"
ADAPTER_R2="${ADAPTER_R2:-}"

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

set_perms_file() {
  local p="$1"
  chgrp zebrafish "$p" 2>/dev/null || true
  chmod 660 "$p" 2>/dev/null || true
}

ensure_group_dirs() {
  umask 002
  mkdir -p \
    "$OUT_BASE/cutadapt/out" \
    "$OUT_BASE/cutadapt/reports" \
    "$OUT_BASE/fastqc_after/cutadapt"

  chgrp -R zebrafish "$OUT_BASE" 2>/dev/null || true
  chmod -R g+rwX "$OUT_BASE" 2>/dev/null || true
  find "$OUT_BASE" -type d -exec chmod 2770 {} + 2>/dev/null || true
}

[[ -n "$SRR" ]] || die "usage: qc_remed_cutadapt_one_srr.sh <SRR...> (requires ADAPTER_R1/ADAPTER_R2 env vars)"
[[ -x "$CUTADAPT_BIN" ]] || die "cutadapt not found/executable at: $CUTADAPT_BIN"
[[ -x "$FASTQC_BIN" ]] || die "fastqc not found/executable at: $FASTQC_BIN"
[[ -n "$ADAPTER_R1" ]] || die "set ADAPTER_R1 (adapter sequence for read1)"
[[ -n "$ADAPTER_R2" ]] || die "set ADAPTER_R2 (adapter sequence for read2)"

ensure_group_dirs

IN1="$RAW_DIR/${SRR}_1.fastq.gz"
IN2="$RAW_DIR/${SRR}_2.fastq.gz"
[[ -s "$IN1" ]] || die "missing input: $IN1"
[[ -s "$IN2" ]] || die "missing input: $IN2"

OUT1="$OUT_BASE/cutadapt/out/${SRR}_1.cutadapt.fastq.gz"
OUT2="$OUT_BASE/cutadapt/out/${SRR}_2.cutadapt.fastq.gz"
LOG="$OUT_BASE/cutadapt/reports/${SRR}.cutadapt.log"

printf '[%s] cutadapt %s\n' "$(date '+%F %T')" "$SRR"
"$CUTADAPT_BIN" \
  -a "$ADAPTER_R1" -A "$ADAPTER_R2" \
  -q "$TRIM_QUAL" \
  -m "$MIN_LEN" \
  -o "$OUT1" -p "$OUT2" \
  --cores "$CUTADAPT_CORES" \
  "$IN1" "$IN2" | tee "$LOG"

set_perms_file "$OUT1"
set_perms_file "$OUT2"
set_perms_file "$LOG"

printf '[%s] fastqc %s\n' "$(date '+%F %T')" "$SRR"
"$FASTQC_BIN" -t "$FASTQC_THREADS" -o "$OUT_BASE/fastqc_after/cutadapt" --noextract "$OUT1" "$OUT2"

for p in \
  "$OUT_BASE/fastqc_after/cutadapt/${SRR}_1.cutadapt_fastqc.zip" \
  "$OUT_BASE/fastqc_after/cutadapt/${SRR}_2.cutadapt_fastqc.zip" \
  "$OUT_BASE/fastqc_after/cutadapt/${SRR}_1.cutadapt_fastqc.html" \
  "$OUT_BASE/fastqc_after/cutadapt/${SRR}_2.cutadapt_fastqc.html"
do
  [[ -f "$p" ]] && set_perms_file "$p"
done

printf '[%s] done %s\n' "$(date '+%F %T')" "$SRR"

