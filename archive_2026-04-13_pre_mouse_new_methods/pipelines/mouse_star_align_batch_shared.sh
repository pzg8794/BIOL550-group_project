#!/usr/bin/env bash
set -euo pipefail

RUNS_FILE="${1:?Usage: mouse_star_align_batch_shared.sh RUNS_FILE}"
SCRIPT_DIR="${SCRIPT_DIR:-/home/zebrafish/mouse/PRJNA1017789_parallel/scripts}"

while read -r srr; do
  [[ -n "$srr" ]] || continue
  bash "$SCRIPT_DIR/mouse_star_align_one_srr_shared.sh" "$srr"
done < "$RUNS_FILE"
