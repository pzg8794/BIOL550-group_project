#!/usr/bin/env bash
set -euo pipefail

# End-to-end runner:
#   download/convert (SRA) -> FastQC (raw) -> FASTX trim -> FastQC (trimmed)
#
# This script is dataset-agnostic; set ACC + RUNS_FILE + DATA_ROOT to point it at a dataset.
#
# Commands:
#   start   -> launches nohup end-to-end job (writes pid + log under $PIPE_TOP)
#   status  -> shows progress + tails logs
#   stop    -> stops underlying jobs + this wrapper
#
# Required env:
#   ACC, RUNS_FILE, DATA_ROOT
#
# Optional env (sane defaults):
#   MEMBER, DUMP_THREADS, FASTQC_THREADS_RAW, FASTQC_THREADS_TRIM, TRIM_QUAL, MIN_LEN
#

cmd="${1:-}"

ts() { date '+%F %T'; }
log() { printf '[%s] %s\n' "$(ts)" "$*"; }
die() { log "ERROR: $*"; exit 2; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRA_PIPE="$SCRIPT_DIR/sra_runs_pipeline_sra3.sh"
FASTX_PIPE="$SCRIPT_DIR/fastx_trim_fastqc_pipeline.sh"

ACC="${ACC:-}"
RUNS_FILE="${RUNS_FILE:-}"
DATA_ROOT="${DATA_ROOT:-}"
MEMBER="${MEMBER:-piter}"

DUMP_THREADS="${DUMP_THREADS:-2}"
FASTQC_THREADS_RAW="${FASTQC_THREADS_RAW:-1}"
FASTQC_THREADS_TRIM="${FASTQC_THREADS_TRIM:-2}"
TRIM_QUAL="${TRIM_QUAL:-20}"
MIN_LEN="${MIN_LEN:-30}"

SHARED_RUN_DIR="$DATA_ROOT/sra_runs"
FASTQC_OUT_RAW="$DATA_ROOT/fastqc_out"
FASTX_OUT="$DATA_ROOT/fastx_out"
FASTQC_OUT_TRIM="$DATA_ROOT/fastqc_out_trimmed"

PIPE_TOP="$DATA_ROOT/.pipeline"
PIPE_RAW="$PIPE_TOP/raw"
PIPE_TRIM="$PIPE_TOP/trim"

WRAP_PID="$PIPE_TOP/end_to_end.pid"
WRAP_LOG="$PIPE_TOP/end_to_end.nohup.log"
WRAP_COMPLETED="$PIPE_TOP/end_to_end.completed"

require_env() {
  [[ -n "$ACC" ]] || die "ACC is required"
  [[ -n "$RUNS_FILE" ]] || die "RUNS_FILE is required"
  [[ -n "$DATA_ROOT" ]] || die "DATA_ROOT is required"
  [[ -f "$RUNS_FILE" ]] || die "RUNS_FILE not found: $RUNS_FILE"
  [[ -x "$SRA_PIPE" ]] || die "missing $SRA_PIPE"
  [[ -x "$FASTX_PIPE" ]] || die "missing $FASTX_PIPE"
}

ensure_dirs() {
  umask 002
  mkdir -p "$SHARED_RUN_DIR" "$FASTQC_OUT_RAW" "$FASTX_OUT" "$FASTQC_OUT_TRIM" "$PIPE_RAW" "$PIPE_TRIM"
  mkdir -p "$(dirname "$WRAP_PID")"

  # Best-effort: make dataset root group-friendly if group exists.
  chgrp -R zebrafish "$DATA_ROOT" 2>/dev/null || true
  chmod 2770 "$DATA_ROOT" 2>/dev/null || true
  chmod 2770 "$SHARED_RUN_DIR" 2>/dev/null || true
  chmod 2770 "$FASTQC_OUT_RAW" "$FASTX_OUT" "$FASTQC_OUT_TRIM" 2>/dev/null || true
  chmod 2775 "$PIPE_TOP" "$PIPE_RAW" "$PIPE_TRIM" 2>/dev/null || true
}

is_running_pidfile() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] || return 1
  local pid
  pid="$(cat "$pid_file" 2>/dev/null || true)"
  [[ -n "$pid" ]] || return 1
  kill -0 "$pid" 2>/dev/null
}

count_expected() {
  # number of SRRs (non-empty, non-comment)
  awk 'NF && $1 !~ /^#/{print $1}' "$RUNS_FILE" | wc -l | tr -d ' '
}

progress_raw() {
  local expected
  expected="$(count_expected)"
  local fastq_pairs=0 fastqc_pairs=0

  while read -r srr; do
    [[ -n "$srr" ]] || continue
    [[ "$srr" != \#* ]] || continue

    [[ -s "$SHARED_RUN_DIR/${srr}_1.fastq.gz" && -s "$SHARED_RUN_DIR/${srr}_2.fastq.gz" ]] && fastq_pairs=$((fastq_pairs+1))
    [[ -s "$FASTQC_OUT_RAW/${srr}_1_fastqc.zip" && -s "$FASTQC_OUT_RAW/${srr}_2_fastqc.zip" ]] && fastqc_pairs=$((fastqc_pairs+1))
  done < "$RUNS_FILE"

  printf 'raw_fastq_pairs=%s/%s raw_fastqc_pairs=%s/%s\n' "$fastq_pairs" "$expected" "$fastqc_pairs" "$expected"
}

progress_trim() {
  local expected
  expected="$(count_expected)"
  local trim_pairs=0 fastqc_pairs=0

  while read -r srr; do
    [[ -n "$srr" ]] || continue
    [[ "$srr" != \#* ]] || continue

    [[ -s "$FASTX_OUT/${srr}_1.trim.fastq.gz" && -s "$FASTX_OUT/${srr}_2.trim.fastq.gz" ]] && trim_pairs=$((trim_pairs+1))
    [[ -s "$FASTQC_OUT_TRIM/${srr}_1.trim_fastqc.zip" && -s "$FASTQC_OUT_TRIM/${srr}_2.trim_fastqc.zip" ]] && fastqc_pairs=$((fastqc_pairs+1))
  done < "$RUNS_FILE"

  printf 'trim_fastq_pairs=%s/%s trim_fastqc_pairs=%s/%s\n' "$trim_pairs" "$expected" "$fastqc_pairs" "$expected"
}

wait_for_file() {
  local f="$1"
  local label="$2"
  local sleep_s="${3:-60}"
  while [[ ! -f "$f" ]]; do
    log "waiting: $label"
    sleep "$sleep_s"
  done
}

run_end_to_end() {
  require_env
  ensure_dirs

  rm -f "$WRAP_COMPLETED" 2>/dev/null || true
  : >"$PIPE_TOP/runs.used.txt" 2>/dev/null || true
  cp -p "$RUNS_FILE" "$PIPE_TOP/runs.used.txt" 2>/dev/null || true

  log "ACC=$ACC MEMBER=$MEMBER"
  log "RUNS_FILE=$RUNS_FILE"
  log "DATA_ROOT=$DATA_ROOT"
  log "expected_srrs=$(count_expected)"
  log "params: DUMP_THREADS=$DUMP_THREADS FASTQC_THREADS_RAW=$FASTQC_THREADS_RAW FASTQC_THREADS_TRIM=$FASTQC_THREADS_TRIM TRIM_QUAL=$TRIM_QUAL MIN_LEN=$MIN_LEN"

  log "== STAGE 1: download + FastQC (raw) =="
  ACC="$ACC" MEMBER="$MEMBER" RUNS_FILE="$RUNS_FILE" \
  SHARED_RUN_DIR="$SHARED_RUN_DIR" FASTQC_OUT="$FASTQC_OUT_RAW" PIPE_DIR="$PIPE_RAW" \
  DUMP_THREADS="$DUMP_THREADS" FASTQC_THREADS="$FASTQC_THREADS_RAW" \
  bash "$SRA_PIPE" start

  # Wait for the workers to mark completion.
  wait_for_file "$PIPE_RAW/download.completed" "raw download.completed"
  wait_for_file "$PIPE_RAW/fastqc.completed" "raw fastqc.completed"
  log "raw progress: $(progress_raw)"

  # Best-effort cleanup of pid files.
  ACC="$ACC" MEMBER="$MEMBER" RUNS_FILE="$RUNS_FILE" \
  SHARED_RUN_DIR="$SHARED_RUN_DIR" FASTQC_OUT="$FASTQC_OUT_RAW" PIPE_DIR="$PIPE_RAW" \
  bash "$SRA_PIPE" stop || true

  log "== STAGE 2: FASTX trim + FastQC (trimmed) =="
  RAW_DIR="$SHARED_RUN_DIR" OUT_DIR="$FASTX_OUT" FASTQC_OUT_DIR="$FASTQC_OUT_TRIM" PIPE_DIR="$PIPE_TRIM" \
  RUNS_FILE="$RUNS_FILE" TRIM_QUAL="$TRIM_QUAL" MIN_LEN="$MIN_LEN" FASTQC_THREADS="$FASTQC_THREADS_TRIM" DO_FASTQC=yes \
  bash "$FASTX_PIPE" start

  wait_for_file "$PIPE_TRIM/fastx.completed" "trim fastx.completed"
  log "trim progress: $(progress_trim)"

  : >"$WRAP_COMPLETED" 2>/dev/null || true
  log "end-to-end completed"
}

start() {
  require_env
  ensure_dirs
  if is_running_pidfile "$WRAP_PID"; then
    log "end-to-end already running (pid=$(cat "$WRAP_PID"))"
    exit 0
  fi
  : >"$WRAP_LOG" || true
  rm -f "$WRAP_COMPLETED" 2>/dev/null || true
  nohup bash "$0" run >"$WRAP_LOG" 2>&1 &
  echo "$!" >"$WRAP_PID"
  log "started end-to-end (pid=$(cat "$WRAP_PID"))"
  log "log: $WRAP_LOG"
}

status() {
  require_env
  ensure_dirs

  if is_running_pidfile "$WRAP_PID"; then
    log "end-to-end running (pid=$(cat "$WRAP_PID"))"
  else
    log "end-to-end not running"
  fi

  log "raw pipeline status:"
  ACC="$ACC" MEMBER="$MEMBER" RUNS_FILE="$RUNS_FILE" SHARED_RUN_DIR="$SHARED_RUN_DIR" FASTQC_OUT="$FASTQC_OUT_RAW" PIPE_DIR="$PIPE_RAW" \
    bash "$SRA_PIPE" status || true
  log "raw progress: $(progress_raw)"

  log "trim pipeline status:"
  RAW_DIR="$SHARED_RUN_DIR" OUT_DIR="$FASTX_OUT" FASTQC_OUT_DIR="$FASTQC_OUT_TRIM" PIPE_DIR="$PIPE_TRIM" RUNS_FILE="$RUNS_FILE" \
    bash "$FASTX_PIPE" status || true
  log "trim progress: $(progress_trim)"

  [[ -f "$WRAP_COMPLETED" ]] && log "end_to_end.completed present" || true

  log "recent wrapper log:"
  tail -n 12 "$WRAP_LOG" 2>/dev/null || true
}

stop() {
  require_env
  ensure_dirs

  log "stopping raw pipeline..."
  ACC="$ACC" MEMBER="$MEMBER" RUNS_FILE="$RUNS_FILE" SHARED_RUN_DIR="$SHARED_RUN_DIR" FASTQC_OUT="$FASTQC_OUT_RAW" PIPE_DIR="$PIPE_RAW" \
    bash "$SRA_PIPE" stop || true

  log "stopping trim pipeline..."
  RAW_DIR="$SHARED_RUN_DIR" OUT_DIR="$FASTX_OUT" FASTQC_OUT_DIR="$FASTQC_OUT_TRIM" PIPE_DIR="$PIPE_TRIM" RUNS_FILE="$RUNS_FILE" \
    bash "$FASTX_PIPE" stop || true

  if [[ -f "$WRAP_PID" ]]; then
    local pid
    pid="$(cat "$WRAP_PID" 2>/dev/null || true)"
    if [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
    rm -f "$WRAP_PID" || true
  fi
  log "stopped end-to-end"
}

case "$cmd" in
  start) start ;;
  status) status ;;
  stop) stop ;;
  run) run_end_to_end ;;
  *) cat <<EOF
Usage:
  ACC=... RUNS_FILE=... DATA_ROOT=... $0 start
  ACC=... RUNS_FILE=... DATA_ROOT=... $0 status
  ACC=... RUNS_FILE=... DATA_ROOT=... $0 stop

Notes:
  - This launches a nohup end-to-end job and logs under: \$DATA_ROOT/.pipeline/
  - It runs stages sequentially (raw completes, then trim starts).
EOF
     exit 2
     ;;
esac

