#!/usr/bin/env bash
set -euo pipefail

export MAMBA_ROOT_PREFIX=/home/zebrafish/mouse/PRJNA1017789_parallel/.local/share/micromamba
MICROMAMBA_BIN=/home/zebrafish/mouse/PRJNA1017789_parallel/.local/bin/micromamba

if [ ! -x "$MICROMAMBA_BIN" ]; then
  echo "micromamba not found at $MICROMAMBA_BIN" >&2
  return 1 2>/dev/null || exit 1
fi

eval "$($MICROMAMBA_BIN shell hook -s bash)"
micromamba activate biol550_deseq2
