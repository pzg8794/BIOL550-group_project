#!/usr/bin/env bash
set -euo pipefail

SRR="${1:-}"
ROOT="${ROOT:-/home/zebrafish/mouse/PRJNA1017789}"

RAW_DIR="${RAW_DIR:-$ROOT/sra_runs}"
OUT_BASE="${OUT_BASE:-$ROOT/qc_remediation}"

FASTP_BIN="${FASTP_BIN:-/usr/local/bin/fastp}"
FASTQC_BIN="${FASTQC_BIN:-/usr/local/bin/FASTQC_11.9/fastqc}"
FASTQC_THREADS="${FASTQC_THREADS:-2}"
FASTP_THREADS="${FASTP_THREADS:-4}"

TRIM_QUAL="${TRIM_QUAL:-20}"
MIN_LEN="${MIN_LEN:-30}"

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

set_perms_file() {
  local p="$1"
  chgrp zebrafish "$p" 2>/dev/null || true
  chmod 660 "$p" 2>/dev/null || true
}

ensure_group_dirs() {
  umask 002
  mkdir -p \
    "$OUT_BASE/fastp/out" \
    "$OUT_BASE/fastp/reports" \
    "$OUT_BASE/fastqc_after/fastp"

  chgrp -R zebrafish "$OUT_BASE" 2>/dev/null || true
  chmod -R g+rwX "$OUT_BASE" 2>/dev/null || true
  find "$OUT_BASE" -type d -exec chmod 2770 {} + 2>/dev/null || true
}

[[ -n "$SRR" ]] || die "usage: qc_remed_fastp_one_srr.sh <SRR...>"
[[ -x "$FASTP_BIN" ]] || die "fastp not found/executable at: $FASTP_BIN"
[[ -x "$FASTQC_BIN" ]] || die "fastqc not found/executable at: $FASTQC_BIN"

ensure_group_dirs

IN1="$RAW_DIR/${SRR}_1.fastq.gz"
IN2="$RAW_DIR/${SRR}_2.fastq.gz"
[[ -s "$IN1" ]] || die "missing input: $IN1"
[[ -s "$IN2" ]] || die "missing input: $IN2"

OUT1="$OUT_BASE/fastp/out/${SRR}_1.fastp.fastq.gz"
OUT2="$OUT_BASE/fastp/out/${SRR}_2.fastp.fastq.gz"
HTML="$OUT_BASE/fastp/reports/${SRR}.fastp.html"
JSON="$OUT_BASE/fastp/reports/${SRR}.fastp.json"

printf '[%s] fastp %s\n' "$(date '+%F %T')" "$SRR"
"$FASTP_BIN" \
  -i "$IN1" -I "$IN2" \
  -o "$OUT1" -O "$OUT2" \
  --detect_adapter_for_pe \
  --cut_front --cut_tail \
  --cut_mean_quality "$TRIM_QUAL" \
  --length_required "$MIN_LEN" \
  --thread "$FASTP_THREADS" \
  --html "$HTML" --json "$JSON"

set_perms_file "$OUT1"
set_perms_file "$OUT2"
set_perms_file "$HTML"
set_perms_file "$JSON"

printf '[%s] fastqc %s\n' "$(date '+%F %T')" "$SRR"
"$FASTQC_BIN" -t "$FASTQC_THREADS" -o "$OUT_BASE/fastqc_after/fastp" --noextract "$OUT1" "$OUT2"

for p in \
  "$OUT_BASE/fastqc_after/fastp/${SRR}_1.fastp_fastqc.zip" \
  "$OUT_BASE/fastqc_after/fastp/${SRR}_2.fastp_fastqc.zip" \
  "$OUT_BASE/fastqc_after/fastp/${SRR}_1.fastp_fastqc.html" \
  "$OUT_BASE/fastqc_after/fastp/${SRR}_2.fastp_fastqc.html"
do
  [[ -f "$p" ]] && set_perms_file "$p"
done

printf '[%s] done %s\n' "$(date '+%F %T')" "$SRR"

