#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sync_long_code_to_sequoia.sh list
  sync_long_code_to_sequoia.sh status [all|script ...]
  sync_long_code_to_sequoia.sh push   [all|script ...]
  sync_long_code_to_sequoia.sh remove [all|script ...]

Purpose:
  Keep long custom code local by default, and copy it to /home/pzg8794 on
  sequoia only when it must be run there.

Examples:
  ./sync_long_code_to_sequoia.sh list
  ./sync_long_code_to_sequoia.sh push mouse_qc_strategy_compare.py
  ./sync_long_code_to_sequoia.sh push all
  ./sync_long_code_to_sequoia.sh remove mouse_qc_strategy_compare.py
  ./sync_long_code_to_sequoia.sh status all
EOF
}

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SSH_TARGET="${SEQUOIA_SSH_TARGET:-pzg8794@sequoia.rit.edu}"

ALL_TARGETS=(
  build_mouse_qc_remediation_notebook.py
  download_fastq_sratoolkit.sh
  fastqc_bundle_summarize.py
  fastx_trim_fastqc_pipeline.sh
  mouse_qc_strategy_compare.py
  run_end_to_end_fastq_fastqc_fastx_fastqc.sh
  run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh
  sra_runs_pipeline_sra3.sh
  sra_runs_pipeline_sra3_parallel.sh
)

remote_dir_for() {
  case "$1" in
    build_mouse_qc_remediation_notebook.py) echo "/home/pzg8794/mouse_qc_remediation/scripts" ;;
    download_fastq_sratoolkit.sh) echo "/home/pzg8794/pipelines" ;;
    fastqc_bundle_summarize.py) echo "/home/pzg8794/mouse_qc_remediation/scripts" ;;
    fastx_trim_fastqc_pipeline.sh) echo "/home/pzg8794/pipelines" ;;
    mouse_qc_strategy_compare.py) echo "/home/pzg8794/mouse_qc_remediation/scripts" ;;
    run_end_to_end_fastq_fastqc_fastx_fastqc.sh) echo "/home/pzg8794/pipelines" ;;
    run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh) echo "/home/pzg8794/pipelines" ;;
    sra_runs_pipeline_sra3.sh) echo "/home/pzg8794/pipelines" ;;
    sra_runs_pipeline_sra3_parallel.sh) echo "/home/pzg8794/pipelines" ;;
    *)
      return 1
      ;;
  esac
}

resolve_targets() {
  if [ "$#" -eq 0 ] || [ "$1" = "all" ]; then
    printf '%s\n' "${ALL_TARGETS[@]}"
    return
  fi

  local target
  for target in "$@"; do
    if ! remote_dir_for "$target" >/dev/null; then
      echo "Unknown target: $target" >&2
      echo "Run '$(basename "$0") list' to see supported long-code files." >&2
      exit 1
    fi
    printf '%s\n' "$target"
  done
}

list_targets() {
  local target
  printf '%-45s %-65s %s\n' "SCRIPT" "LOCAL SOURCE" "REMOTE DESTINATION"
  printf '%-45s %-65s %s\n' "------" "------------" "------------------"
  for target in "${ALL_TARGETS[@]}"; do
    local remote_dir
    remote_dir=$(remote_dir_for "$target")
    printf '%-45s %-65s %s\n' \
      "$target" \
      "$SCRIPT_DIR/$target" \
      "$remote_dir/$target"
  done
}

push_target() {
  local target="$1"
  local local_path="$SCRIPT_DIR/$target"
  local remote_dir
  remote_dir=$(remote_dir_for "$target")

  if [ ! -f "$local_path" ]; then
    echo "Local source not found: $local_path" >&2
    exit 1
  fi

  ssh -n "$SSH_TARGET" "mkdir -p '$remote_dir'"
  scp "$local_path" "$SSH_TARGET:$remote_dir/"
  echo "pushed  $target -> $remote_dir/"
}

remove_target() {
  local target="$1"
  local remote_dir
  remote_dir=$(remote_dir_for "$target")
  ssh -n "$SSH_TARGET" "rm -f '$remote_dir/$target'"
  echo "removed $remote_dir/$target"
}

status_targets() {
  local targets=("$@")
  local remote_paths=()
  local target remote_dir

  for target in "${targets[@]}"; do
    remote_dir=$(remote_dir_for "$target")
    remote_paths+=("$remote_dir/$target")
  done

  ssh -n "$SSH_TARGET" 'bash -s' -- "${remote_paths[@]}" <<'EOF'
for path in "$@"; do
  name=$(basename "$path")
  if [ -f "$path" ]; then
    printf '%s\tpresent\n' "$name"
  else
    printf '%s\tmissing\n' "$name"
  fi
done
EOF
}

if [ "$#" -lt 1 ]; then
  usage
  exit 1
fi

ACTION="$1"
shift

case "$ACTION" in
  list)
    list_targets
    ;;
  push)
    while IFS= read -r target; do
      push_target "$target"
    done < <(resolve_targets "$@")
    ;;
  remove)
    while IFS= read -r target; do
      remove_target "$target"
    done < <(resolve_targets "$@")
    ;;
  status)
    printf '%-45s %s\n' "SCRIPT" "SERVER STATE"
    printf '%-45s %s\n' "------" "------------"
    status_list=()
    while IFS= read -r target; do
      status_list+=("$target")
    done < <(resolve_targets "$@")
    while IFS=$'\t' read -r target state; do
      printf '%-45s %s\n' "$target" "$state"
    done < <(status_targets "${status_list[@]}")
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "Unknown action: $ACTION" >&2
    usage
    exit 1
    ;;
esac
