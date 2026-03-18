#!/usr/bin/env bash
set -euo pipefail

umask 002

PRIVATE_BASE="${PRIVATE_BASE:-/home/pzg8794/mouse_qc_remediation}"
PRIVATE_DONE="${PRIVATE_DONE:-$PRIVATE_BASE/alignment/star_grcm39_ensembl_all26_fastp/all26_fastp_alignment.completed}"
PRIVATE_REF="${PRIVATE_REF:-$PRIVATE_BASE/reference/grcm39_ensembl}"

ROOT="${ROOT:-/home/zebrafish/mouse/PRJNA1017789_parallel}"
SCRIPT_DIR="${SCRIPT_DIR:-$ROOT/scripts}"
RUNS_DIR="${RUNS_DIR:-$ROOT/runs}"
ALIGN_ROOT="${ALIGN_ROOT:-$ROOT/alignment/star_grcm39_ensembl_all26_fastp}"
REF_ROOT="${REF_ROOT:-$ROOT/reference/grcm39_ensembl}"
INDEX_DIR="$REF_ROOT/star_index_sjdb150"
INPUT_DIR="${INPUT_DIR:-$ROOT/fastp_out}"
LOG_DIR="${LOG_DIR:-$ROOT/logs}"
LAUNCHER_LOG_DIR="$ALIGN_ROOT/launcher_logs"

mkdir -p "$SCRIPT_DIR" "$RUNS_DIR" "$ALIGN_ROOT" "$LOG_DIR" "$LAUNCHER_LOG_DIR" "$ROOT/reference"

echo "Waiting for private alignment completion flag: $PRIVATE_DONE"
while [[ ! -f "$PRIVATE_DONE" ]]; do
  sleep 120
done

echo "Private run completed; syncing shared reference/index"
mkdir -p "$REF_ROOT"
if command -v rsync >/dev/null 2>&1; then
  rsync -a "$PRIVATE_REF/" "$REF_ROOT/"
else
  echo "rsync not found; using cp -a fallback"
  cp -a "$PRIVATE_REF"/. "$REF_ROOT"/
fi
chmod -R g+rwX "$REF_ROOT"

{
  echo -e "srr\tmate1\tmate2"
  while read -r srr; do
    [[ -n "$srr" ]] || continue
    echo -e "${srr}\t${INPUT_DIR}/${srr}_1.trim.fastq.gz\t${INPUT_DIR}/${srr}_2.trim.fastq.gz"
  done < "$RUNS_DIR/PRJNA1017789_runs.all.txt"
} > "$ALIGN_ROOT/all26_fastp_manifest.tsv"

cat > "$ALIGN_ROOT/run_metadata.tsv" <<EOF
key	value
decision_scope	all26_first_shared
trigger	private_alignment_completed
private_done_flag	$PRIVATE_DONE
shared_input_root	$INPUT_DIR
shared_reference_index	$INDEX_DIR
execution_mode	serial_one_sample_at_a_time
runs_file	$RUNS_DIR/PRJNA1017789_runs.all.txt
EOF

bash "$SCRIPT_DIR/mouse_star_align_batch_shared.sh" "$RUNS_DIR/PRJNA1017789_runs.all.txt" \
  > "$LAUNCHER_LOG_DIR/all26.serial.log" 2>&1

date > "$ALIGN_ROOT/all26_fastp_alignment.completed"
chmod -R g+rwX "$ALIGN_ROOT" "$LOG_DIR"
