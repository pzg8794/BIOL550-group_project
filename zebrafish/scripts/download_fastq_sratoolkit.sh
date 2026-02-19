#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Download FASTQs for SRR runs using SRA Toolkit (prefetch + fasterq-dump).

This is the ONE wrapper you should use. Provide runs in exactly one of 3 ways:
  A) Inline list:  --runs "SRR... SRR..."
  B) File:         --runs-file path/to/runs.txt
  C) Member + N:   --member <name> --n-runs N
                  (takes the first N SRRs from your assigned file:
                   metadata/<ACC>/splits/runs.member.<member>.txt)

Recommended (start with 1 run):
  bash scripts/download_fastq_sratoolkit.sh \
    --acc PRJNA1277581 \
    --member piter \
    --n-runs 1 \
    --out-dir data/PRJNA1277581 \
    --threads 4

Other examples:
  # Use a file directly
  bash scripts/download_fastq_sratoolkit.sh \
    --acc PRJNA1277581 \
    --runs-file metadata/PRJNA1277581/splits/runs.member.piter.txt \
    --out-dir data/PRJNA1277581 \
    --threads 4

  # Use an inline list
  bash scripts/download_fastq_sratoolkit.sh \
    --acc PRJNA1277581 \
    --runs "SRR34002427 SRR34002428" \
    --out-dir data/PRJNA1277581 \
    --threads 4

Defaults:
  --out-dir  data/<ACC>
  --threads  4

Notes:
  - Requires SRA Toolkit on PATH (prefetch + fasterq-dump).
  - Writes paired FASTQs as <SRR>_1.fastq.gz and <SRR>_2.fastq.gz in --out-dir/<SRR>/.
  - Re-running is safe: it skips runs whose gzipped FASTQs already exist unless you pass --force.
USAGE
}

ACC=""
MEMBER=""
N_RUNS=""
RUNS_INLINE=""
RUNS_FILE=""
OUT_DIR=""
THREADS="4"
FORCE="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --acc) ACC="$2"; shift 2 ;;
    --member) MEMBER="$2"; shift 2 ;;
    --n-runs) N_RUNS="$2"; shift 2 ;;
    --runs) RUNS_INLINE="$2"; shift 2 ;;
    --runs-file) RUNS_FILE="$2"; shift 2 ;;
    --out-dir) OUT_DIR="$2"; shift 2 ;;
    --threads) THREADS="$2"; shift 2 ;;
    --force) FORCE="1"; shift 1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

[[ -n "$ACC" ]] || { echo "ERROR: --acc is required" >&2; exit 2; }

mode_count=0
[[ -n "$RUNS_INLINE" ]] && mode_count=$((mode_count + 1))
[[ -n "$RUNS_FILE" ]] && mode_count=$((mode_count + 1))
[[ -n "$N_RUNS" ]] && mode_count=$((mode_count + 1))
[[ "$mode_count" -eq 1 ]] || { echo "ERROR: Choose exactly one of: --runs OR --runs-file OR --n-runs" >&2; usage; exit 2; }

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CORE="$ROOT_DIR/scripts/download_fastq_sratoolkit_from_runs.sh"
[[ -x "$CORE" ]] || { echo "ERROR: missing core script: $CORE" >&2; exit 2; }

if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="$ROOT_DIR/data/$ACC"
fi
mkdir -p "$OUT_DIR"

TMP_RUNS_FILE=""
cleanup_tmp() { [[ -n "${TMP_RUNS_FILE:-}" ]] && rm -f "$TMP_RUNS_FILE" || true; }
trap cleanup_tmp EXIT

RUNS_FILE_USE=""
if [[ -n "$RUNS_FILE" ]]; then
  RUNS_FILE_USE="$RUNS_FILE"
elif [[ -n "$RUNS_INLINE" ]]; then
  TMP_RUNS_FILE="$(mktemp "${TMPDIR:-/tmp}/runs.${ACC}.inline.XXXXXX.txt")"
  # Split on whitespace into one SRR per line
  printf '%s\n' $RUNS_INLINE > "$TMP_RUNS_FILE"
  RUNS_FILE_USE="$TMP_RUNS_FILE"
else
  [[ -n "$MEMBER" ]] || { echo "ERROR: --member is required when using --n-runs" >&2; exit 2; }
  [[ "$N_RUNS" =~ ^[0-9]+$ ]] || { echo "ERROR: --n-runs must be an integer (got: $N_RUNS)" >&2; exit 2; }
  [[ "$N_RUNS" -ge 1 ]] || { echo "ERROR: --n-runs must be >= 1 (got: $N_RUNS)" >&2; exit 2; }

  RUNS_FILE_BASE="$ROOT_DIR/metadata/$ACC/splits/runs.member.${MEMBER}.txt"
  [[ -f "$RUNS_FILE_BASE" ]] || { echo "ERROR: missing runs file: $RUNS_FILE_BASE" >&2; exit 2; }

  TMP_RUNS_FILE="$(mktemp "${TMPDIR:-/tmp}/runs.${ACC}.${MEMBER}.first${N_RUNS}.XXXXXX.txt")"
  head -n "$N_RUNS" "$RUNS_FILE_BASE" > "$TMP_RUNS_FILE"
  RUNS_FILE_USE="$TMP_RUNS_FILE"
fi

[[ -f "$RUNS_FILE_USE" ]] || { echo "ERROR: runs file not found: $RUNS_FILE_USE" >&2; exit 2; }

echo "acc:      $ACC"
echo "out_dir:  ${OUT_DIR#$ROOT_DIR/}"
echo "threads:  $THREADS"
echo "force:    $FORCE"
if [[ -n "$MEMBER" ]]; then
  echo "member:   $MEMBER"
fi
if [[ -n "$N_RUNS" ]]; then
  echo "n_runs:   $N_RUNS"
fi
echo

echo "These SRRs will be downloaded:"
cat "$RUNS_FILE_USE"
echo

CMD=(bash "$CORE" --runs-file "$RUNS_FILE_USE" --out-dir "$OUT_DIR" --threads "$THREADS")
[[ "$FORCE" == "1" ]] && CMD+=(--force)

printf '$ %q ' "${CMD[@]}"
echo
"${CMD[@]}"

