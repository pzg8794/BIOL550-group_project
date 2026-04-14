#!/usr/bin/env bash
set -euo pipefail

STAR_BIN="${STAR_BIN:-/usr/local/bin/STAR/STAR}"
BASE="${BASE:-/home/pzg8794/mouse_qc_remediation}"
INPUT_DIR="${INPUT_DIR:-$BASE/output/fastp/out}"
INDEX_DIR="${INDEX_DIR:-$BASE/reference/grcm39_ensembl/star_index_sjdb150}"
ALIGN_ROOT="${ALIGN_ROOT:-$BASE/alignment/star_grcm39_ensembl_all26_fastp}"
STAR_THREADS="${STAR_THREADS:-4}"

SRR="${1:?Usage: mouse_star_align_one_srr.sh SRR30333743}"
R1="$INPUT_DIR/${SRR}_1.fastp.fastq.gz"
R2="$INPUT_DIR/${SRR}_2.fastp.fastq.gz"
SAMPLE_DIR="$ALIGN_ROOT/samples/$SRR"
LOG_DIR="$ALIGN_ROOT/logs"
DONE_DIR="$ALIGN_ROOT/completed"

mkdir -p "$SAMPLE_DIR" "$LOG_DIR" "$DONE_DIR"

if [[ ! -f "$R1" || ! -f "$R2" ]]; then
  echo "Missing fastp inputs for $SRR" >&2
  exit 1
fi

if [[ ! -f "$INDEX_DIR/SA" ]]; then
  echo "Missing STAR index at $INDEX_DIR" >&2
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
