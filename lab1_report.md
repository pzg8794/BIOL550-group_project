# BIOL550 Lab 1 — Trapnell Data QC + Alignment (FastQC, FastX, STAR)

**Date:** 2026-02-05  
**Dataset:** “Trapnell Data” (course bundle on `sequoia`)  
**Goal:** Run QC on raw reads, attempt cleanup using FastX based on QC findings, and run one end-to-end alignment example with STAR.

## Data Locations

**On `sequoia` (server):**
- Raw reads: `/home/pzg8794/BIOL550/Lab1/Trapnell_Data/Trapnell Data/Raw reads/`
- Reference used for STAR index (downloaded via NCBI `datasets`): `~/refs/GCF_000001215/ncbi_dataset/data/GCF_000001215.4/`
- STAR index output: `~/star_index/droso_refseq_ncbi/`
- Outputs (examples): `~/BIOL550/Lab1/fastqc_out/`, `~/BIOL550/Lab1/fastx_trimmed/`, `~/BIOL550/Lab1/star_align/`

**On local machine (Mac):**
- Exported artifacts: `Semester5/BIOL550/BIOL550-Lab/server_exports/2026-02-05/`
- Extracted bundle for reporting: `Semester5/BIOL550/BIOL550-Lab/qc_bundle/`
- MultiQC report: `Semester5/BIOL550/BIOL550-Lab/multiqc_report/multiqc_report.html`

## Step 1 — QC With FastQC (Raw Reads)

**What was run:** FastQC on all 12 gzipped FASTQ files (`*.fq.gz`) in the “Raw reads” folder (6 paired-end samples × 2 mates).

**Example command (single file):**
```bash
/usr/local/bin/FASTQC_11.9/fastqc -t 1 -o ~/BIOL550/Lab1/fastqc_out \
  "/home/pzg8794/BIOL550/Lab1/Trapnell_Data/Trapnell Data/Raw reads/GSM794486_C2_R1_1.fq.gz"
```

**Expected outputs (written under `~/BIOL550/Lab1/fastqc_out/`):**
```text
fastqc_out/
  GSM794486_C2_R1_1_fastqc.html
  GSM794486_C2_R1_1_fastqc.zip
```

**Batch execution approach used (conceptually):** looped over `Raw reads/*.fq.gz` and ran FastQC per file, writing `*_fastqc.html` and `*_fastqc.zip` outputs.

**Quantitative observations:**
- FastQC reports generated (raw): **12** (`qc_bundle/fastqc_out/*_fastqc.zip`).
- Read length (example mate file): **75 bp**.
- Read count (example mate file `GSM794486_C2_R1_1.fq.gz`): **11,607,325 reads**.
- GC fraction estimate (example mate file, first 10k reads): **~0.4198**.

**FastQC summary (raw):**
- Across all 12 raw FASTQs, **3/12 modules failed for 12/12 files**:
  - `Per base sequence quality`
  - `Per sequence quality scores`
  - `Per sequence GC content`

## Step 1b — Cleanup Attempt With FastX

**What was run:** `fastq_quality_trimmer` on each gzipped FASTQ to trim low-quality tails (Phred+33), writing **uncompressed** trimmed FASTQs (`*.trim.fq`).

**Command used:**
```bash
READS="/home/pzg8794/BIOL550/Lab1/Trapnell_Data/Trapnell Data/Raw reads"
TRIM=~/BIOL550/Lab1/fastx_trimmed
mkdir -p "$TRIM"

for f in "$READS"/*.fq.gz; do
  base="$(basename "$f" .fq.gz)"
  zcat "$f" | /usr/local/bin/FastX/0.0.13/fastq_quality_trimmer -Q33 -t 20 -l 0 \
    -o "$TRIM/${base}.trim.fq"
done
```

**Expected outputs (written under `~/BIOL550/Lab1/fastx_trimmed/`):**
```text
fastx_trimmed/
  GSM794483_C1_R1_1.trim.fq
  GSM794483_C1_R1_2.trim.fq
  GSM794484_C1_R2_1.trim.fq
  GSM794484_C1_R2_2.trim.fq
  ...
  GSM794488_C2_R3_1.trim.fq
  GSM794488_C2_R3_2.trim.fq
```

**Quantitative observations:**
- Trimmed FASTQs produced: **12** (`~/BIOL550/Lab1/fastx_trimmed/*.trim.fq`).
- Disk footprint of trimmed outputs: **~22 GB** total (trimmed files are uncompressed).

## Step 1c — QC With FastQC (Trimmed Reads)

**What was run:** FastQC on the 12 trimmed FASTQs in `~/BIOL550/Lab1/fastx_trimmed/`.

**Command used:**
```bash
TRIM=~/BIOL550/Lab1/fastx_trimmed
TRIM_QC=~/BIOL550/Lab1/fastqc_trimmed_out
mkdir -p "$TRIM_QC"

nohup /usr/local/bin/FASTQC_11.9/fastqc -t 1 -o "$TRIM_QC" "$TRIM"/*.trim.fq \
  > "$TRIM_QC/fastqc_trimmed.nohup.log" 2>&1 &
```

**Expected outputs (written under `~/BIOL550/Lab1/fastqc_trimmed_out/`):**
```text
fastqc_trimmed_out/
  fastqc_trimmed.nohup.log
  GSM794483_C1_R1_1.trim_fastqc.html
  GSM794483_C1_R1_1.trim_fastqc.zip
  ...
  GSM794488_C2_R3_2.trim_fastqc.html
  GSM794488_C2_R3_2.trim_fastqc.zip
```

**FastQC summary (trimmed):**
- Trimmed FastQC reports generated: **12** (`qc_bundle/fastqc_trimmed_out/*.trim_fastqc.zip`).
- The same 3 modules **still failed for all 12 trimmed files**:
  - `Per base sequence quality`
  - `Per sequence quality scores`
  - `Per sequence GC content`

**Interpretation:** Trimming at `-t 20` reduced/trimmed low-quality tails but did not change FastQC’s PASS/FAIL status for these modules under its default thresholds. Next iteration could include (a) more aggressive trimming parameters, (b) filtering low-quality reads (e.g., `fastq_quality_filter`), and/or (c) adapter clipping if adapter contamination is present.

## Step 2 — STAR Alignment (One Worked Example)

**STAR index inputs (Drosophila, NCBI assembly):**
- FASTA: `.../GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna`
- GTF: `.../genomic.gtf`

**Index build (genomeGenerate):**
```bash
nohup /usr/local/bin/STAR/STAR --runMode genomeGenerate \
  --genomeDir ~/star_index/droso_refseq_ncbi \
  --genomeFastaFiles "/home/pzg8794/refs/GCF_000001215/ncbi_dataset/data/GCF_000001215.4/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna" \
  --sjdbGTFfile "/home/pzg8794/refs/GCF_000001215/ncbi_dataset/data/GCF_000001215.4/genomic.gtf" \
  --sjdbOverhang 74 \
  --runThreadN 8 \
  > ~/star_index/droso_refseq_ncbi/genomeGenerate.nohup.log 2>&1 &
```

### What is the STAR “genomeDir” (and why your folder name may differ)

The STAR genome directory (passed as `--genomeDir`) is the **reference index folder** STAR reads during alignment. It is created by the `--runMode genomeGenerate` command above.

Different students may have this folder named differently depending on where they built it (or if a prebuilt index was provided). Examples of valid “genomeDir” paths include:
- `~/star_index/droso_refseq_ncbi/`
- `~/BIOL550/Lab1/star_index/...`
- `~/_STARgenome/` (common naming convention: a folder ending in `_STARgenome`)

**How to tell you found the right folder:** it should contain the large STAR index files (`Genome`, `SA`, `SAindex`) *and* the annotation-derived tables (like `geneInfo.tab`). If `Genome/SA/SAindex` are missing, it is likely an incomplete/partial directory and STAR alignment will fail.

**Quick verification commands:**
```bash
GENOMEDIR="~/_STARgenome"   # replace with your path
ls -lh "$GENOMEDIR"/{Genome,SA,SAindex,geneInfo.tab} 2>/dev/null
```

**Example (from our server):** `geneInfo.tab` in one STAR genome directory was `210,462` bytes (~206 KB).

**Expected outputs (written under `~/star_index/droso_refseq_ncbi/`):**
```text
droso_refseq_ncbi/
  genomeGenerate.nohup.log
  Genome
  SA
  SAindex
  genomeParameters.txt
  chrName.txt
  chrLength.txt
  chrStart.txt
  chrNameLength.txt
  exonInfo.tab
  exonGeTrInfo.tab
  geneInfo.tab
  transcriptInfo.tab
  sjdbInfo.txt
  sjdbList.fromGTF.out.tab
```

**How it is used (alignment):** the STAR alignment command references this folder via `--genomeDir` (STAR reads these index files; it does *not* rebuild them during alignment).

**Alignment command (paired-end; 1 thread):**
```bash
READS="/home/pzg8794/BIOL550/Lab1/Trapnell_Data/Trapnell Data/Raw reads"
OUT=~/BIOL550/Lab1/star_align
SAMPLE="GSM794486_C2_R1"
mkdir -p "$OUT/$SAMPLE"

nohup /usr/local/bin/STAR/STAR \
  --genomeDir ~/star_index/droso_refseq_ncbi \
  --runThreadN 1 \
  --readFilesIn "$READS/${SAMPLE}_1.fq.gz" "$READS/${SAMPLE}_2.fq.gz" \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --limitBAMsortRAM 6000000000 \
  --outFileNamePrefix "$OUT/$SAMPLE/" \
  > "$OUT/$SAMPLE/star.nohup.log" 2>&1 &
```

**Expected outputs (written under `~/BIOL550/Lab1/star_align/GSM794486_C2_R1/`):**
```text
star_align/GSM794486_C2_R1/
  Aligned.sortedByCoord.out.bam
  Log.final.out
  Log.out
  Log.progress.out
  SJ.out.tab
  star.nohup.log
```

**Quantitative observations (from `Log.final.out`):**
- Input reads: **11,607,325**
- Uniquely mapped: **11,516,696 (99.22%)**
- Multi-mapped: **80,358 (0.69%)**
- Too many loci: **9,996 (0.09%)**
- Output BAM: **409 MB** (`Aligned.sortedByCoord.out.bam`)

**Note:** STAR initially failed at BAM sorting due to insufficient memory; adding `--limitBAMsortRAM 6000000000` resolved the error.

## Reporting Artifact

MultiQC summary report (local):
- `Semester5/BIOL550/BIOL550-Lab/multiqc_report/multiqc_report.html`
