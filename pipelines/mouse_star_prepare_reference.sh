#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

STAR_BIN="${STAR_BIN:-/usr/local/bin/STAR/STAR}"
BASE="${BASE:-/home/pzg8794/mouse_qc_remediation}"
REF_BASE="${REF_BASE:-$BASE/reference/grcm39_ensembl}"
DNA_DIR="$REF_BASE/dna"
GTF_DIR="$REF_BASE/gtf"
INDEX_DIR="${INDEX_DIR:-$REF_BASE/star_index_sjdb150}"
LOG_DIR="$REF_BASE/logs"
META_DIR="$REF_BASE/meta"

STAR_INDEX_THREADS="${STAR_INDEX_THREADS:-12}"
STAR_INDEX_RAM="${STAR_INDEX_RAM:-48000000000}"
READ_LENGTH="${READ_LENGTH:-151}"
SJDB_OVERHANG="${SJDB_OVERHANG:-150}"

FASTA_LIST_URL="${FASTA_LIST_URL:-https://ftp.ensembl.org/pub/current_fasta/mus_musculus/dna/}"
GTF_LIST_URL="${GTF_LIST_URL:-https://ftp.ensembl.org/pub/current_gtf/mus_musculus/}"

mkdir -p "$DNA_DIR" "$GTF_DIR" "$INDEX_DIR" "$LOG_DIR" "$META_DIR"

FASTA_FILE="$(wget -qO- "$FASTA_LIST_URL" | grep -o 'Mus_musculus\.GRCm39\.dna\.primary_assembly\.fa\.gz' | head -n1)"
GTF_FILE="$(wget -qO- "$GTF_LIST_URL" | grep -o 'Mus_musculus\.GRCm39\.[0-9][0-9]*\.gtf\.gz' | sort -V | tail -n1)"

if [[ -z "$FASTA_FILE" || -z "$GTF_FILE" ]]; then
  echo "Could not resolve Ensembl GRCm39 FASTA/GTF from current listings." >&2
  exit 1
fi

FASTA_URL="${FASTA_LIST_URL}${FASTA_FILE}"
GTF_URL="${GTF_LIST_URL}${GTF_FILE}"
FASTA_PATH_GZ="$DNA_DIR/$FASTA_FILE"
GTF_PATH_GZ="$GTF_DIR/$GTF_FILE"
FASTA_PATH="${FASTA_PATH_GZ%.gz}"
GTF_PATH="${GTF_PATH_GZ%.gz}"

if [[ ! -f "$FASTA_PATH_GZ" ]]; then
  wget -O "$FASTA_PATH_GZ" "$FASTA_URL"
fi

if [[ ! -f "$GTF_PATH_GZ" ]]; then
  wget -O "$GTF_PATH_GZ" "$GTF_URL"
fi

if [[ ! -f "$FASTA_PATH" ]]; then
  gzip -cd "$FASTA_PATH_GZ" > "$FASTA_PATH"
fi

if [[ ! -f "$GTF_PATH" ]]; then
  gzip -cd "$GTF_PATH_GZ" > "$GTF_PATH"
fi

ln -sfn "$FASTA_PATH" "$DNA_DIR/current.primary_assembly.fa"
ln -sfn "$GTF_PATH" "$GTF_DIR/current.annotation.gtf"

cat > "$META_DIR/reference_choice.tsv" <<EOF
key	value
assembly	GRCm39
source	Ensembl current
fasta_url	$FASTA_URL
gtf_url	$GTF_URL
fasta_path_gz	$FASTA_PATH_GZ
gtf_path_gz	$GTF_PATH_GZ
fasta_path	$FASTA_PATH
gtf_path	$GTF_PATH
read_length	$READ_LENGTH
sjdb_overhang	$SJDB_OVERHANG
star_index_dir	$INDEX_DIR
EOF

if [[ -f "$INDEX_DIR/SA" ]]; then
  echo "STAR index already exists at $INDEX_DIR"
  exit 0
fi

rm -rf "$INDEX_DIR"
mkdir -p "$INDEX_DIR"

"$STAR_BIN" --runMode genomeGenerate \
  --runThreadN "$STAR_INDEX_THREADS" \
  --genomeDir "$INDEX_DIR" \
  --genomeFastaFiles "$FASTA_PATH" \
  --sjdbGTFfile "$GTF_PATH" \
  --sjdbOverhang "$SJDB_OVERHANG" \
  --limitGenomeGenerateRAM "$STAR_INDEX_RAM" \
  > "$LOG_DIR/genomeGenerate.log" 2>&1

echo "STAR index ready at $INDEX_DIR"
