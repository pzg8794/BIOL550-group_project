#!/usr/bin/env bash
set -euo pipefail

cmd="${1:-}"

RAW_DIR="${RAW_DIR:-/home/zebrafish/sra_runs}"
OUT_DIR="${OUT_DIR:-/home/zebrafish/fastx_out}"
FASTQC_OUT_DIR="${FASTQC_OUT_DIR:-$HOME/fastqc_out_trimmed}"
PIPE_DIR="${PIPE_DIR:-$OUT_DIR/.pipeline}"

FASTQC_BIN="${FASTQC_BIN:-/usr/local/bin/FASTQC_11.9/fastqc}"
FASTQC_THREADS="${FASTQC_THREADS:-2}"

FASTX_DIR="${FASTX_DIR:-/usr/local/bin/FastX/0.0.13}"
FASTQ_QUALITY_TRIMMER="${FASTQ_QUALITY_TRIMMER:-$FASTX_DIR/fastq_quality_trimmer}"
TRIM_QUAL="${TRIM_QUAL:-20}"
MIN_LEN="${MIN_LEN:-1}"

GZIP_BIN="${GZIP_BIN:-gzip}"
DO_FASTQC="${DO_FASTQC:-yes}"

RUNS_FILE="${RUNS_FILE:-}"

PID_FILE="$PIPE_DIR/fastx.pid"
LOG_FILE="$PIPE_DIR/fastx.nohup.log"
COMPLETED_FILE="$PIPE_DIR/fastx.completed"

ts() { date '+%F %T'; }
log() { printf '[%s] %s\n' "$(ts)" "$*"; }

die() {
  log "ERROR: $*"
  exit 1
}

is_running() {
  [[ -f "$1" ]] || return 1
  local pid
  pid="$(cat "$1" 2>/dev/null || true)"
  [[ -n "$pid" ]] || return 1
  kill -0 "$pid" 2>/dev/null
}

ensure_dirs() {
  umask 007
  mkdir -p "$OUT_DIR" "$FASTQC_OUT_DIR" "$PIPE_DIR"
}

write_pid() {
  printf '%s\n' "$1" >"$PID_FILE"
}

clear_pid() {
  rm -f "$PID_FILE"
}

start_job() {
  ensure_dirs
  if is_running "$PID_FILE"; then
    log "fastx already running (pid=$(cat "$PID_FILE"))"
    exit 0
  fi
  : >"$LOG_FILE" || true
  rm -f "$COMPLETED_FILE" 2>/dev/null || true
  nohup bash "$0" _run_wrapper >"$LOG_FILE" 2>&1 &
  write_pid "$!"
  log "started fastx (pid=$(cat "$PID_FILE"))"
  log "log: $LOG_FILE"
}

status_job() {
  ensure_dirs
  if is_running "$PID_FILE"; then
    log "fastx running (pid=$(cat "$PID_FILE"))"
  else
    log "fastx not running"
  fi
  [[ -f "$COMPLETED_FILE" ]] && log "fastx.completed present" || true
  log "recent log:"
  tail -n 20 "$LOG_FILE" 2>/dev/null || true
}

stop_job() {
  ensure_dirs
  if ! [[ -f "$PID_FILE" ]]; then
    log "fastx not running (no pid file)"
    exit 0
  fi
  local pid
  pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -z "$pid" ]]; then
    clear_pid
    log "fastx not running (empty pid file)"
    exit 0
  fi
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    sleep 1
    kill -0 "$pid" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
    log "stopped fastx (pid=$pid)"
  else
    log "fastx not running (stale pid=$pid)"
  fi
  clear_pid
}

run_wrapper() {
  ensure_dirs
  run_all
  : >"$COMPLETED_FILE" 2>/dev/null || true
  clear_pid
}

list_srrs() {
  local tmp1 tmp2 tmpi
  tmp1="$(mktemp)"
  tmp2="$(mktemp)"
  tmpi="$(mktemp)"

  ls -1 "$RAW_DIR"/SRR*_1.fastq.gz 2>/dev/null | sed 's#.*/##; s/_1\.fastq\.gz$//' | sort -u >"$tmp1" || true
  ls -1 "$RAW_DIR"/SRR*_2.fastq.gz 2>/dev/null | sed 's#.*/##; s/_2\.fastq\.gz$//' | sort -u >"$tmp2" || true
  comm -12 "$tmp1" "$tmp2" >"$tmpi" || true

  if [[ -n "$RUNS_FILE" ]]; then
    local tmpr
    tmpr="$(mktemp)"
    sed -E 's/\\r$//' "$RUNS_FILE" | awk 'NF{print $1}' | sort -u >"$tmpr"
    comm -12 "$tmpr" "$tmpi"
    rm -f "$tmpr"
  else
    cat "$tmpi"
  fi

  rm -f "$tmp1" "$tmp2" "$tmpi"
}

set_perms() {
  local p="$1"
  chgrp zebrafish "$p" 2>/dev/null || true
  chmod 660 "$p" 2>/dev/null || true
}

trim_one() {
  local in_gz="$1"
  local out_gz="$2"
  local tmp
  tmp="${out_gz}.tmp.$$"
  zcat "$in_gz" | "$FASTQ_QUALITY_TRIMMER" -Q33 -t "$TRIM_QUAL" -l "$MIN_LEN" | "$GZIP_BIN" -c >"$tmp"
  mv -f "$tmp" "$out_gz"
  set_perms "$out_gz"
}

run_fastqc_pair() {
  local srr="$1"
  local in1="$OUT_DIR/${srr}_1.trim.fastq.gz"
  local in2="$OUT_DIR/${srr}_2.trim.fastq.gz"
  local out1_zip="$FASTQC_OUT_DIR/${srr}_1.trim_fastqc.zip"
  local out2_zip="$FASTQC_OUT_DIR/${srr}_2.trim_fastqc.zip"

  [[ -s "$out1_zip" && -s "$out2_zip" ]] && return 0

  "$FASTQC_BIN" -t "$FASTQC_THREADS" -o "$FASTQC_OUT_DIR" --noextract "$in1" "$in2"
  [[ -f "$out1_zip" ]] && set_perms "$out1_zip"
  [[ -f "$out2_zip" ]] && set_perms "$out2_zip"
  [[ -f "${out1_zip%.zip}.html" ]] && set_perms "${out1_zip%.zip}.html"
  [[ -f "${out2_zip%.zip}.html" ]] && set_perms "${out2_zip%.zip}.html"
}

run_all() {
  ensure_dirs
  [[ -x "$FASTQ_QUALITY_TRIMMER" ]] || die "missing fastq_quality_trimmer at $FASTQ_QUALITY_TRIMMER"

  if [[ "$DO_FASTQC" == "yes" ]]; then
    [[ -x "$FASTQC_BIN" ]] || die "missing fastqc at $FASTQC_BIN"
  fi

  local total=0
  local trimmed=0
  local skipped=0
  local qc_done=0

  while read -r srr; do
    [[ -z "$srr" ]] && continue
    total=$((total+1))

    local raw1="$RAW_DIR/${srr}_1.fastq.gz"
    local raw2="$RAW_DIR/${srr}_2.fastq.gz"
    local out1="$OUT_DIR/${srr}_1.trim.fastq.gz"
    local out2="$OUT_DIR/${srr}_2.trim.fastq.gz"

    if [[ -s "$out1" && -s "$out2" ]]; then
      skipped=$((skipped+1))
    else
      log "TRIM $srr"
      [[ -s "$raw1" && -s "$raw2" ]] || die "missing inputs for $srr"
      [[ -s "$out1" ]] || trim_one "$raw1" "$out1"
      [[ -s "$out2" ]] || trim_one "$raw2" "$out2"
      trimmed=$((trimmed+1))
    fi

    if [[ "$DO_FASTQC" == "yes" ]]; then
      log "FASTQC $srr"
      run_fastqc_pair "$srr"
      qc_done=$((qc_done+1))
    fi
  done < <(list_srrs)

  log "done"
  log "total_srrs=$total"
  log "trimmed_now=$trimmed"
  log "already_trimmed=$skipped"
  log "fastqc_pairs_checked=$qc_done"
}

usage() {
  cat <<'EOF'
Usage:
  fastx_trim_fastqc_pipeline.sh start
  fastx_trim_fastqc_pipeline.sh status
  fastx_trim_fastqc_pipeline.sh stop
  fastx_trim_fastqc_pipeline.sh run

Env:
  RAW_DIR=/home/zebrafish/sra_runs
  OUT_DIR=/home/zebrafish/fastx_out
  FASTQC_OUT_DIR=/home/zebrafish/fastqc_out_trimmed
  FASTQC_BIN=/usr/local/bin/FASTQC_11.9/fastqc
  FASTQC_THREADS=2
  FASTX_DIR=/usr/local/bin/FastX/0.0.13
  FASTQ_QUALITY_TRIMMER=$FASTX_DIR/fastq_quality_trimmer
  TRIM_QUAL=20
  MIN_LEN=1
  DO_FASTQC=yes|no
  RUNS_FILE=/path/to/srr_list.txt
EOF
}

case "$cmd" in
  start) start_job ;;
  status) status_job ;;
  stop) stop_job ;;
  _run_wrapper) run_wrapper ;;
  run) run_all ;;
  *) usage; exit 2 ;;
esac
