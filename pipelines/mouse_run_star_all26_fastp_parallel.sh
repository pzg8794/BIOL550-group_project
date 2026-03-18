#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-/home/pzg8794/mouse_qc_remediation}"
SCRIPT_DIR="${SCRIPT_DIR:-$BASE/scripts}"
RUNS_DIR="${RUNS_DIR:-$BASE/runs}"
ALIGN_ROOT="${ALIGN_ROOT:-$BASE/alignment/star_grcm39_ensembl_all26_fastp}"
INPUT_DIR="${INPUT_DIR:-$BASE/output/fastp/out}"
INDEX_DIR="${INDEX_DIR:-$BASE/reference/grcm39_ensembl/star_index_sjdb150}"
LOG_DIR="$ALIGN_ROOT/launcher_logs"

mkdir -p "$ALIGN_ROOT" "$LOG_DIR"

cat > "$ALIGN_ROOT/run_metadata.tsv" <<EOF
key	value
decision_scope	all26_first
cleaned_input_root	$INPUT_DIR
reference_index	$INDEX_DIR
parallel_split_files	$RUNS_DIR/PRJNA1017789_runs.member.nikhi.txt,$RUNS_DIR/PRJNA1017789_runs.member.piter.txt,$RUNS_DIR/PRJNA1017789_runs.member.samuel.txt
EOF

{
  echo -e "srr\tmate1\tmate2"
  while read -r srr; do
    [[ -n "$srr" ]] || continue
    echo -e "${srr}\t${INPUT_DIR}/${srr}_1.fastp.fastq.gz\t${INPUT_DIR}/${srr}_2.fastp.fastq.gz"
  done < "$RUNS_DIR/PRJNA1017789_runs.all.txt"
} > "$ALIGN_ROOT/all26_fastp_manifest.tsv"

bash "$SCRIPT_DIR/mouse_star_prepare_reference.sh"

bash "$SCRIPT_DIR/mouse_star_align_batch.sh" "$RUNS_DIR/PRJNA1017789_runs.member.nikhi.txt" \
  > "$LOG_DIR/nikhi.batch.log" 2>&1 &
PID_NIKHI=$!

bash "$SCRIPT_DIR/mouse_star_align_batch.sh" "$RUNS_DIR/PRJNA1017789_runs.member.piter.txt" \
  > "$LOG_DIR/piter.batch.log" 2>&1 &
PID_PITER=$!

bash "$SCRIPT_DIR/mouse_star_align_batch.sh" "$RUNS_DIR/PRJNA1017789_runs.member.samuel.txt" \
  > "$LOG_DIR/samuel.batch.log" 2>&1 &
PID_SAMUEL=$!

wait "$PID_NIKHI" "$PID_PITER" "$PID_SAMUEL"

date > "$ALIGN_ROOT/all26_fastp_alignment.completed"
