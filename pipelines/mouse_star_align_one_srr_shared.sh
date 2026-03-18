#!/usr/bin/env bash
set -euo pipefail

umask 002

STAR_BIN="${STAR_BIN:-/usr/local/bin/STAR/STAR}"
ROOT="${ROOT:-/home/zebrafish/mouse/PRJNA1017789_parallel}"
INPUT_DIR="${INPUT_DIR:-$ROOT/fastp_out}"
INDEX_DIR="${INDEX_DIR:-$ROOT/reference/grcm39_ensembl/star_index_sjdb150}"
ALIGN_ROOT="${ALIGN_ROOT:-$ROOT/alignment/star_grcm39_ensembl_all26_fastp}"
STAR_THREADS="${STAR_THREADS:-1}"

SRR="${1:?Usage: mouse_star_align_one_srr_shared.sh SRR30333743}"
R1="$INPUT_DIR/${SRR}_1.trim.fastq.gz"
R2="$INPUT_DIR/${SRR}_2.trim.fastq.gz"
SAMPLE_DIR="$ALIGN_ROOT/samples/$SRR"
LOG_DIR="$ALIGN_ROOT/logs"
DONE_DIR="$ALIGN_ROOT/completed"

mkdir -p "$SAMPLE_DIR" "$LOG_DIR" "$DONE_DIR"

if [[ ! -f "$R1" || ! -f "$R2" ]]; then
  echo "Missing shared fastp inputs for $SRR" >&2
  exit 1
fi

if [[ ! -f "$INDEX_DIR/SA" ]]; then
  echo "Missing shared STAR index at $INDEX_DIR" >&2
  exit 1
fi

"$STAR_BIN" \
  --runThreadN "$STAR_THREADS" \
  --genomeDir "$INDEX_DIR" \
  --readFilesIn "$R1" "$R2" \
  --readFilesCommand zcat \
  --twopassMode Basic \
  --quantMode GeneCounts \
  --outSAMtype BAM SortedByCoordinate \
  --outFileNamePrefix "$SAMPLE_DIR/${SRR}." \
  --outTmpDir "$SAMPLE_DIR/_star_tmp" \
  > "$LOG_DIR/${SRR}.star.log" 2>&1

date > "$DONE_DIR/${SRR}.completed"
chmod -R g+rwX "$SAMPLE_DIR" "$LOG_DIR" "$DONE_DIR"
