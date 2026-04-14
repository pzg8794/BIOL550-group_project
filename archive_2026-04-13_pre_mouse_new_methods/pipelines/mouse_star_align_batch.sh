#!/usr/bin/env bash
set -euo pipefail

RUNS_FILE="${1:?Usage: mouse_star_align_batch.sh RUNS_FILE}"
SCRIPT_DIR="${SCRIPT_DIR:-/home/pzg8794/mouse_qc_remediation/scripts}"

while read -r srr; do
  [[ -n "$srr" ]] || continue
  bash "$SCRIPT_DIR/mouse_star_align_one_srr.sh" "$srr"
done < "$RUNS_FILE"
