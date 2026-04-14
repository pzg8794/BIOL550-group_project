#!/usr/bin/env bash
set -euo pipefail

# Parallel variant of sra_runs_pipeline_sra3.sh
#  - Multiple download workers (prefetch + fasterq-dump + compress)
#  - Multiple FastQC workers
#  - Uses simple per-SRR claim directories to avoid duplicate work
#
# This is intended for Sequoia-style installs where tools live under:
#   /usr/local/bin/sra_3.0.0
#   /usr/local/bin/FASTQC_11.9/fastqc
#
# NOTE: claims are cleared on start; outputs are still treated as source-of-truth for skipping.

ACC_DEFAULT="PRJNA1277581"
MEMBER_DEFAULT="piter"

SHARED_RUN_DIR_DEFAULT="/home/zebrafish/sra_runs"     # flat: SRRxxxx_1.fastq.gz, SRRxxxx_2.fastq.gz
FASTQC_OUT_DEFAULT="/home/zebrafish/fastqc_out"       # FastQC outputs
PIPE_DIR_DEFAULT="/home/zebrafish/sra_runs_pipeline"  # pids + logs + temp + failure markers

FASTQC_BIN_DEFAULT="/usr/local/bin/FASTQC_11.9/fastqc"
SRA_TOOLKIT_BIN_SERVER_DEFAULT="/usr/local/bin/sra_3.0.0"
SRA_TOOLKIT_BIN_HOME_FALLBACK_DEFAULT="$HOME/zebrafish/tools/sratoolkit/bin"

DOWNLOAD_WORKERS_DEFAULT="2"
FASTQC_WORKERS_DEFAULT="2"
PIGZ_THREADS_DEFAULT="8"

MAX_PREFETCH_ATTEMPTS_DEFAULT="3"
MAX_DUMP_ATTEMPTS_DEFAULT="2"
MAX_GZIP_ATTEMPTS_DEFAULT="1"
RETRY_SLEEP_SECONDS_DEFAULT="120"

usage() {
  cat <<USAGE
Usage:
  $0 start
  $0 status
  $0 stop

Optional environment overrides:
  ACC (default: ${ACC_DEFAULT})
  MEMBER (default: ${MEMBER_DEFAULT})
  RUNS_FILE (default: \$HOME/zebrafish/metadata/\$ACC/splits/runs.member.\$MEMBER.txt)
  SHARED_RUN_DIR (default: ${SHARED_RUN_DIR_DEFAULT})
  FASTQC_OUT (default: ${FASTQC_OUT_DEFAULT})
  PIPE_DIR (default: ${PIPE_DIR_DEFAULT})

  FASTQC_BIN (default: ${FASTQC_BIN_DEFAULT})
  SRA_TOOLKIT_BIN (default: auto-detect; prefers ${SRA_TOOLKIT_BIN_SERVER_DEFAULT})

  DOWNLOAD_WORKERS (default: ${DOWNLOAD_WORKERS_DEFAULT})
  FASTQC_WORKERS (default: ${FASTQC_WORKERS_DEFAULT})
  PIGZ_THREADS (default: ${PIGZ_THREADS_DEFAULT})   # pigz -p threads (if pigz available)

  DUMP_THREADS (default: 1)     # fasterq-dump threads (if used)
  FASTQC_THREADS (default: 1)   # fastqc -t
  SLEEP_SECONDS (default: 60)   # QC polling interval

  MAX_PREFETCH_ATTEMPTS (default: ${MAX_PREFETCH_ATTEMPTS_DEFAULT})
  MAX_DUMP_ATTEMPTS (default: ${MAX_DUMP_ATTEMPTS_DEFAULT})
  MAX_GZIP_ATTEMPTS (default: ${MAX_GZIP_ATTEMPTS_DEFAULT})
  RETRY_SLEEP_SECONDS (default: ${RETRY_SLEEP_SECONDS_DEFAULT})
USAGE
}

log() { echo "[$(date '+%F %T')] $*"; }
die() { echo "ERROR: $*" >&2; exit 2; }

detect_sra_bin() {
  if [[ -d "${SRA_TOOLKIT_BIN_SERVER_DEFAULT}" ]]; then
    echo "${SRA_TOOLKIT_BIN_SERVER_DEFAULT}"
    return 0
  fi
  if [[ -d "${SRA_TOOLKIT_BIN_HOME_FALLBACK_DEFAULT}" ]]; then
    echo "${SRA_TOOLKIT_BIN_HOME_FALLBACK_DEFAULT}"
    return 0
  fi
  echo "${SRA_TOOLKIT_BIN_SERVER_DEFAULT}"
}

mark_failed() {
  local pipe_dir="$1"
  local srr="$2"
  local step="$3"
  local rc="$4"
  local msg="$5"

  local failed_dir="$pipe_dir/failed"
  mkdir -p "$failed_dir"
  chgrp zebrafish "$failed_dir" 2>/dev/null || true
  chmod 2775 "$failed_dir" 2>/dev/null || true

  local marker="$failed_dir/${srr}.${step}.failed"
  {
    echo "time: $(date '+%F %T')"
    echo "srr: $srr"
    echo "step: $step"
    echo "rc: $rc"
    echo "msg: $msg"
  } >"$marker"

  chgrp zebrafish "$marker" 2>/dev/null || true
  chmod 664 "$marker" 2>/dev/null || true

  printf '%s\t%s\t%s\trc=%s\t%s\n' "$(date '+%F %T')" "$srr" "$step" "$rc" "$msg" >>"$failed_dir/failed.tsv" 2>/dev/null || true
}

is_marked_failed() {
  local pipe_dir="$1"
  local srr="$2"
  compgen -G "$pipe_dir/failed/${srr}.*.failed" >/dev/null 2>&1
}

is_running() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] || return 1
  local pid
  pid="$(cat "$pid_file" 2>/dev/null || true)"
  [[ -n "$pid" ]] || return 1
  kill -0 "$pid" 2>/dev/null
}

start_job() {
  local name="$1"; shift
  local pid_file="$1"; shift
  local log_file="$1"; shift

  if is_running "$pid_file"; then
    log "$name already running (pid=$(cat "$pid_file"))"
    return 0
  fi

  nohup "$@" >"$log_file" 2>&1 &
  local pid=$!
  echo "$pid" >"$pid_file"
  log "started $name (pid=$pid)"
}

stop_job() {
  local name="$1"; shift
  local pid_file="$1"; shift

  if ! [[ -f "$pid_file" ]]; then
    log "$name not running (no pid file)"
    return 0
  fi

  local pid
  pid="$(cat "$pid_file" 2>/dev/null || true)"
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    log "stopped $name (pid=$pid)"
  else
    log "$name not running (stale pid file)"
  fi
  rm -f "$pid_file" || true
}

ensure_dirs() {
  local shared_run_dir="$1"
  local fastqc_out="$2"
  local pipe_dir="$3"

  umask 002
  mkdir -p "$shared_run_dir" "$fastqc_out" "$pipe_dir" "$pipe_dir/tmp" "$pipe_dir/failed"

  chgrp zebrafish "$shared_run_dir" 2>/dev/null || true
  chmod 2770 "$shared_run_dir" 2>/dev/null || true

  chgrp zebrafish "$pipe_dir" 2>/dev/null || true
  chmod 2775 "$pipe_dir" 2>/dev/null || true

  chgrp zebrafish "$pipe_dir/failed" 2>/dev/null || true
  chmod 2775 "$pipe_dir/failed" 2>/dev/null || true
}

compress_pair() {
  local f1="$1" f2="$2"
  local max_attempts="$3"
  local retry_sleep_seconds="$4"

  local attempt="1"
  local rc="0"
  local pigz_threads="${PIGZ_THREADS:-$PIGZ_THREADS_DEFAULT}"

  while [[ "$attempt" -le "$max_attempts" ]]; do
    log "compress attempt ${attempt}/${max_attempts}: $(basename "$f1" .fastq)"
    rm -f "${f1}.gz" "${f2}.gz" 2>/dev/null || true
    if command -v pigz >/dev/null 2>&1; then
      if pigz -p "$pigz_threads" -f "$f1" "$f2"; then
        return 0
      fi
    else
      if gzip -f "$f1" "$f2"; then
        return 0
      fi
    fi
    rc="$?"
    log "compress failed rc=$rc"
    sleep "$((retry_sleep_seconds * attempt))"
    attempt="$((attempt + 1))"
  done
  return "${rc:-1}"
}

claim_once() {
  local claim_dir="$1"
  mkdir -p "$(dirname "$claim_dir")" 2>/dev/null || true
  mkdir "$claim_dir" 2>/dev/null
}

download_worker_parallel() {
  local worker_id="$1"
  local acc="$2" member="$3" runs_file="$4" shared_run_dir="$5" pipe_dir="$6"

  local sra_bin="$SRA_TOOLKIT_BIN"
  local prefetch="$sra_bin/prefetch"
  local fasterq="$sra_bin/fasterq-dump"
  local fastq_dump_bin=""

  if [[ -x "$sra_bin/fastq-dump-orig.3.0.0" ]]; then
    fastq_dump_bin="$sra_bin/fastq-dump-orig.3.0.0"
  elif [[ -x "$sra_bin/fastq-dump" ]]; then
    fastq_dump_bin="$sra_bin/fastq-dump"
  fi

  [[ -f "$runs_file" ]] || die "missing runs file: $runs_file"

  local dump_threads="${DUMP_THREADS:-1}"
  local max_prefetch_attempts="${MAX_PREFETCH_ATTEMPTS:-$MAX_PREFETCH_ATTEMPTS_DEFAULT}"
  local max_dump_attempts="${MAX_DUMP_ATTEMPTS:-$MAX_DUMP_ATTEMPTS_DEFAULT}"
  local max_gzip_attempts="${MAX_GZIP_ATTEMPTS:-$MAX_GZIP_ATTEMPTS_DEFAULT}"
  local retry_sleep_seconds="${RETRY_SLEEP_SECONDS:-$RETRY_SLEEP_SECONDS_DEFAULT}"

  local method=""
  if [[ -x "$prefetch" && -x "$fasterq" ]]; then
    method="prefetch+fasterq-dump"
  elif [[ -n "$fastq_dump_bin" ]]; then
    method="fastq-dump"
  else
    die "missing SRA tools under $sra_bin (need prefetch+fasterq-dump OR fastq-dump)"
  fi

  log "download_worker[$worker_id]: acc=$acc member=$member method=$method dump_threads=$dump_threads"

  while read -r SRR; do
    SRR="$(echo "$SRR" | tr -d '\r' | xargs || true)"
    [[ -n "$SRR" ]] || continue
    [[ "$SRR" != \#* ]] || continue

    local r1="$shared_run_dir/${SRR}_1.fastq.gz"
    local r2="$shared_run_dir/${SRR}_2.fastq.gz"

    if [[ -f "$r1" && -f "$r2" ]]; then
      continue
    fi
    if is_marked_failed "$pipe_dir" "$SRR"; then
      continue
    fi
    if ! claim_once "$pipe_dir/claims/download/$SRR"; then
      continue
    fi

    log "== DOWNLOAD[$worker_id] $SRR =="

    local tmp_root="$pipe_dir/tmp"
    local tmp_dir
    tmp_dir="$(mktemp -d "$tmp_root/${SRR}.XXXXXX")"
    mkdir -p "$tmp_dir/sra" "$tmp_dir/fastq" "$tmp_dir/tmp"

    if [[ "$method" == "prefetch+fasterq-dump" ]]; then
      local prefetch_ok="0"
      local attempt="1"
      local rc="0"
      while [[ "$attempt" -le "$max_prefetch_attempts" ]]; do
        log "prefetch[$worker_id] attempt ${attempt}/${max_prefetch_attempts}: $SRR"
        rm -rf "$tmp_dir/sra"/* 2>/dev/null || true
        if NCBI_VDB_REMOTE_PROTOCOLS=https "$prefetch" --transport http -O "$tmp_dir/sra" "$SRR"; then
          prefetch_ok="1"
          break
        fi
        rc="$?"
        log "prefetch[$worker_id] failed rc=$rc: $SRR"
        sleep "$((retry_sleep_seconds * attempt))"
        attempt="$((attempt + 1))"
      done
      if [[ "$prefetch_ok" != "1" ]]; then
        mark_failed "$pipe_dir" "$SRR" "prefetch" "${rc:-1}" "prefetch failed after ${max_prefetch_attempts} attempt(s)"
        rm -rf "$tmp_dir" || true
        continue
      fi

      local sra_input="$SRR"
      if [[ -d "$tmp_dir/sra/$SRR" ]]; then
        local sra_file
        sra_file="$(find "$tmp_dir/sra/$SRR" -maxdepth 1 -type f 2>/dev/null | head -n 1 || true)"
        if [[ -n "$sra_file" ]]; then
          sra_input="$sra_file"
        fi
      fi

      local dump_ok="0"
      attempt="1"
      while [[ "$attempt" -le "$max_dump_attempts" ]]; do
        log "fasterq-dump[$worker_id] attempt ${attempt}/${max_dump_attempts}: $SRR"
        rm -f "$tmp_dir/fastq/${SRR}"_*.fastq "$tmp_dir/fastq/${SRR}"_*.fastq.gz 2>/dev/null || true
        rm -rf "$tmp_dir/tmp"/* 2>/dev/null || true
        if "$fasterq" --split-files --threads "$dump_threads" --outdir "$tmp_dir/fastq" --temp "$tmp_dir/tmp" "$sra_input"; then
          dump_ok="1"
          break
        fi
        rc="$?"
        log "fasterq-dump[$worker_id] failed rc=$rc: $SRR"
        sleep "$((retry_sleep_seconds * attempt))"
        attempt="$((attempt + 1))"
      done
      if [[ "$dump_ok" != "1" ]]; then
        mark_failed "$pipe_dir" "$SRR" "fasterq-dump" "${rc:-1}" "fasterq-dump failed after ${max_dump_attempts} attempt(s)"
        rm -rf "$tmp_dir" || true
        continue
      fi

      if ! compress_pair "$tmp_dir/fastq/${SRR}_1.fastq" "$tmp_dir/fastq/${SRR}_2.fastq" "$max_gzip_attempts" "$retry_sleep_seconds"; then
        rc="$?"
        mark_failed "$pipe_dir" "$SRR" "compress" "${rc:-1}" "compression failed after ${max_gzip_attempts} attempt(s)"
        rm -rf "$tmp_dir" || true
        continue
      fi

    else
      local dump_ok="0"
      local attempt="1"
      local rc="0"
      while [[ "$attempt" -le "$max_dump_attempts" ]]; do
        log "fastq-dump[$worker_id] attempt ${attempt}/${max_dump_attempts}: $SRR"
        rm -f "$tmp_dir/fastq/${SRR}"_*.fastq.gz 2>/dev/null || true
        if NCBI_VDB_REMOTE_PROTOCOLS=https "$fastq_dump_bin" --split-files --origfmt --gzip -O "$tmp_dir/fastq" "$SRR"; then
          dump_ok="1"
          break
        fi
        rc="$?"
        log "fastq-dump[$worker_id] failed rc=$rc: $SRR"
        sleep "$((retry_sleep_seconds * attempt))"
        attempt="$((attempt + 1))"
      done
      if [[ "$dump_ok" != "1" ]]; then
        mark_failed "$pipe_dir" "$SRR" "fastq-dump" "${rc:-1}" "fastq-dump failed after ${max_dump_attempts} attempt(s)"
        rm -rf "$tmp_dir" || true
        continue
      fi
    fi

    if [[ ! -f "$tmp_dir/fastq/${SRR}_1.fastq.gz" || ! -f "$tmp_dir/fastq/${SRR}_2.fastq.gz" ]]; then
      mark_failed "$pipe_dir" "$SRR" "outputs" "1" "missing expected paired outputs under tmp_dir/fastq"
      rm -rf "$tmp_dir" || true
      continue
    fi

    mv -f "$tmp_dir/fastq/${SRR}_1.fastq.gz" "$r1"
    mv -f "$tmp_dir/fastq/${SRR}_2.fastq.gz" "$r2"

    chgrp zebrafish "$r1" "$r2" 2>/dev/null || true
    chmod 660 "$r1" "$r2" 2>/dev/null || true

    rm -rf "$tmp_dir" || true
    log "done[$worker_id]: $SRR"

  done < "$runs_file"
}

download_controller() {
  local acc="$1" member="$2" runs_file="$3" shared_run_dir="$4" pipe_dir="$5"
  local workers="${DOWNLOAD_WORKERS:-$DOWNLOAD_WORKERS_DEFAULT}"

  rm -rf "$pipe_dir/claims/download" 2>/dev/null || true
  mkdir -p "$pipe_dir/claims/download" 2>/dev/null || true

  log "download_controller: workers=$workers"
  trap 'jobs -p | xargs -r kill 2>/dev/null || true' EXIT INT TERM

  local i
  for i in $(seq 1 "$workers"); do
    download_worker_parallel "$i" "$acc" "$member" "$runs_file" "$shared_run_dir" "$pipe_dir" &
  done
  wait || true
  touch "$pipe_dir/download.completed" || true
  log "download_controller complete"
}

fastqc_worker_parallel() {
  local worker_id="$1"
  local acc="$2" member="$3" runs_file="$4" shared_run_dir="$5" fastqc_out="$6" pipe_dir="$7"

  local fastqc_bin="$FASTQC_BIN"
  [[ -x "$fastqc_bin" ]] || die "missing fastqc at $fastqc_bin"
  [[ -f "$runs_file" ]] || die "missing runs file: $runs_file"

  local fastqc_threads="${FASTQC_THREADS:-1}"
  local sleep_seconds="${SLEEP_SECONDS:-60}"

  log "fastqc_worker[$worker_id]: acc=$acc member=$member fastqc_threads=$fastqc_threads"

  while read -r SRR; do
    SRR="$(echo "$SRR" | tr -d '\r' | xargs || true)"
    [[ -n "$SRR" ]] || continue
    [[ "$SRR" != \#* ]] || continue

    if is_marked_failed "$pipe_dir" "$SRR"; then
      continue
    fi

    local r1="$shared_run_dir/${SRR}_1.fastq.gz"
    local r2="$shared_run_dir/${SRR}_2.fastq.gz"

    local out1_zip="$fastqc_out/${SRR}_1_fastqc.zip"
    local out2_zip="$fastqc_out/${SRR}_2_fastqc.zip"

    if [[ -f "$out1_zip" && -f "$out2_zip" ]]; then
      continue
    fi
    if ! claim_once "$pipe_dir/claims/fastqc/$SRR"; then
      continue
    fi

    while [[ ! -f "$r1" || ! -f "$r2" ]]; do
      if is_marked_failed "$pipe_dir" "$SRR"; then
        break
      fi
      if [[ -f "$pipe_dir/download.completed" ]]; then
        log "missing inputs after download.completed: $SRR"
        break
      fi
      sleep "$sleep_seconds"
    done

    [[ -f "$r1" && -f "$r2" ]] || continue

    log "== FASTQC[$worker_id] $SRR =="
    "$fastqc_bin" -t "$fastqc_threads" -o "$fastqc_out" "$r1" "$r2"
    log "qc done[$worker_id]: $SRR"

  done < "$runs_file"
}

fastqc_controller() {
  local acc="$1" member="$2" runs_file="$3" shared_run_dir="$4" fastqc_out="$5" pipe_dir="$6"
  local workers="${FASTQC_WORKERS:-$FASTQC_WORKERS_DEFAULT}"

  rm -rf "$pipe_dir/claims/fastqc" 2>/dev/null || true
  mkdir -p "$pipe_dir/claims/fastqc" 2>/dev/null || true

  log "fastqc_controller: workers=$workers"
  trap 'jobs -p | xargs -r kill 2>/dev/null || true' EXIT INT TERM

  local i
  for i in $(seq 1 "$workers"); do
    fastqc_worker_parallel "$i" "$acc" "$member" "$runs_file" "$shared_run_dir" "$fastqc_out" "$pipe_dir" &
  done
  wait || true
  touch "$pipe_dir/fastqc.completed" || true
  log "fastqc_controller complete"
}

main() {
  local cmd="${1:-}"

  local acc="${ACC:-$ACC_DEFAULT}"
  local member="${MEMBER:-$MEMBER_DEFAULT}"

  local runs_file_default="$HOME/zebrafish/metadata/$acc/splits/runs.member.${member}.txt"
  local runs_file="${RUNS_FILE:-$runs_file_default}"

  local shared_run_dir="${SHARED_RUN_DIR:-$SHARED_RUN_DIR_DEFAULT}"
  local fastqc_out="${FASTQC_OUT:-$FASTQC_OUT_DEFAULT}"
  local pipe_dir="${PIPE_DIR:-$PIPE_DIR_DEFAULT}"

  local download_pid="$pipe_dir/download.pid"
  local fastqc_pid="$pipe_dir/fastqc.pid"
  local download_log="$pipe_dir/download.nohup.log"
  local fastqc_log="$pipe_dir/fastqc.nohup.log"

  case "$cmd" in
    _download_controller)
      shift
      ensure_dirs "$shared_run_dir" "$fastqc_out" "$pipe_dir"
      download_controller "$acc" "$member" "$runs_file" "$shared_run_dir" "$pipe_dir"
      ;;
    _fastqc_controller)
      shift
      ensure_dirs "$shared_run_dir" "$fastqc_out" "$pipe_dir"
      fastqc_controller "$acc" "$member" "$runs_file" "$shared_run_dir" "$fastqc_out" "$pipe_dir"
      ;;
    start)
      ensure_dirs "$shared_run_dir" "$fastqc_out" "$pipe_dir"
      : >"$download_log" || true
      : >"$fastqc_log" || true
      rm -f "$pipe_dir/download.completed" "$pipe_dir/fastqc.completed" || true
      start_job "download" "$download_pid" "$download_log" bash "$0" _download_controller
      start_job "fastqc" "$fastqc_pid" "$fastqc_log" bash "$0" _fastqc_controller
      log "logs:"
      log "  download: $download_log"
      log "  fastqc:   $fastqc_log"
      ;;
    status)
      if is_running "$download_pid"; then
        log "download running (pid=$(cat "$download_pid"))"
      else
        log "download not running"
      fi
      if is_running "$fastqc_pid"; then
        log "fastqc running (pid=$(cat "$fastqc_pid"))"
      else
        log "fastqc not running"
      fi
      log "config: download_workers=${DOWNLOAD_WORKERS:-$DOWNLOAD_WORKERS_DEFAULT} fastqc_workers=${FASTQC_WORKERS:-$FASTQC_WORKERS_DEFAULT} pigz_threads=${PIGZ_THREADS:-$PIGZ_THREADS_DEFAULT}"
      log "recent download log:"
      tail -n 12 "$download_log" 2>/dev/null || true
      log "recent fastqc log:"
      tail -n 12 "$fastqc_log" 2>/dev/null || true
      [[ -f "$pipe_dir/download.completed" ]] && log "download.completed present" || true
      [[ -f "$pipe_dir/fastqc.completed" ]] && log "fastqc.completed present" || true
      ;;
    stop)
      stop_job "download" "$download_pid"
      stop_job "fastqc" "$fastqc_pid"
      ;;
    -h|--help|help|"")
      usage
      ;;
    *)
      die "unknown command: $cmd"
      ;;
  esac
}

export FASTQC_BIN="${FASTQC_BIN:-$FASTQC_BIN_DEFAULT}"
export SRA_TOOLKIT_BIN="${SRA_TOOLKIT_BIN:-$(detect_sra_bin)}"

main "$@"

