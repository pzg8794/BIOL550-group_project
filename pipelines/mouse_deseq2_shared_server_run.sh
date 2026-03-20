#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  mouse_deseq2_shared_server_run.sh check
  mouse_deseq2_shared_server_run.sh run

Shared paths:
  INPUT_ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel/deseq2_shared/inputs
  OUTPUT_ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel/deseq2_shared/output

Requirements:
  - private team env: /home/pzg8794/.local/share/micromamba/envs/biol550_deseq2
  - temporary long-code copy: /home/pzg8794/pipelines/mouse_deseq2_all26.R
EOF
}

ACTION="${1:-}"
MICROMAMBA_BIN="/home/pzg8794/.local/bin/micromamba"
export MAMBA_ROOT_PREFIX="/home/pzg8794/.local/share/micromamba"
ENV_NAME="biol550_deseq2"
R_DRIVER="/home/pzg8794/pipelines/mouse_deseq2_all26.R"
INPUT_ROOT="/home/zebrafish/mouse/PRJNA1017789_parallel/deseq2_shared/inputs"
OUTPUT_ROOT="/home/zebrafish/mouse/PRJNA1017789_parallel/deseq2_shared/output"
COUNTS_PATH="$INPUT_ROOT/mouse_star_gene_counts_reverse_stranded.tsv"
META_PATH="$INPUT_ROOT/mouse_alignment_sample_summary.tsv"

case "$ACTION" in
  check)
    test -x "$MICROMAMBA_BIN"
    test -f "$R_DRIVER"
    test -f "$COUNTS_PATH"
    test -f "$META_PATH"
    "$MICROMAMBA_BIN" run -n "$ENV_NAME" \
      Rscript -e "suppressPackageStartupMessages(library(DESeq2)); cat('DESEQ2_OK\n')"
    echo "CHECK_OK"
    ;;
  run)
    mkdir -p "$OUTPUT_ROOT"
    "$MICROMAMBA_BIN" run -n "$ENV_NAME" \
      Rscript "$R_DRIVER" \
        --counts "$COUNTS_PATH" \
        --meta "$META_PATH" \
        --outdir "$OUTPUT_ROOT"
    ;;
  -h|--help|help|"")
    usage
    ;;
  *)
    echo "Unknown action: $ACTION" >&2
    usage
    exit 1
    ;;
esac
