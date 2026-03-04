# Mouse dataset — repeatable FASTQ → FastQC → FASTX → FastQC workflow

This is the same end-to-end process we used for the zebrafish dataset, but **scoped to the mouse dataset** and kept **separate** so files never mix across organisms/projects.

> Note (2026-03-02): this workflow assumes **bulk RNA-seq** (one FASTQ pair per sample/replicate). If the “mouse dataset” you’re evaluating turns out to be **single-cell RNA-seq**, do not proceed with this bulk-style DE pipeline—pick a bulk dataset and reuse the same steps there.

Work log (what/steps/why): `Semester5/BIOL550/group_project/WORKLOG.md`

## Current mouse dataset (active)

- BioProject: `PRJNA1017789` (mouse; GEO: `GSE243308`)
- Runs list (local): `Semester5/BIOL550/group_project/mouse/runs/PRJNA1017789_runs.all.txt` (26 SRRs)
- Runs list (server): `/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt`
- Server dataset root (active run): `/home/zebrafish/mouse/PRJNA1017789_parallel/`
- TODO list (keep updated): `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`

## 0) Fill in dataset identifiers (required)

Set these once at the top of your terminal session (or write them into a small `env.sh` you can `source`):

```bash
# Dataset identifiers (edit these)
ACC="<BIOPROJECT_OR_PROJECT_ID>"        # e.g., PRJNAxxxxxx (preferred if available)
GEO="<GSE_ID_IF_ANY>"                   # optional
SPECIES="mouse"
```

If you only have a GEO series, first confirm the linked SRA BioProject / SRR list (GEO → SRA). Store the final SRR list locally as a text file (one SRR per line).

## 1) Decide the directory layout (don’t mix datasets)

### Local (Mac) layout (recommended)

```bash
BASE="/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse"
RAW_BUNDLE="$BASE/qc_bundle_raw"                 # raw FastQC html/zip
TRIM_BUNDLE="$BASE/qc_bundle_trimmed"            # trimmed FastQC html/zip
ANALYSIS="$BASE/qc_analysis_raw_vs_trimmed"      # summary tables + plots
RUNS_DIR="$BASE/runs"                            # SRR lists (all + per-member)
mkdir -p "$RAW_BUNDLE" "$TRIM_BUNDLE" "$ANALYSIS" "$RUNS_DIR"
```

### Server (shared) layout (choose a shared root)

Pick a shared folder that the team can access (examples below). Keep mouse data in its own subtree:

```bash
SHARED_ROOT="/home/zebrafish"   # OR: /home/biol550 OR another shared area your team uses
DATA_ROOT="$SHARED_ROOT/mouse/$ACC"

RUNS="$DATA_ROOT/sra_runs"                # raw FASTQs
FASTQC_RAW="$DATA_ROOT/fastqc_out"        # raw FastQC outputs
FASTX="$DATA_ROOT/fastx_out"              # trimmed FASTQs
FASTQC_TRIM="$DATA_ROOT/fastqc_out_trimmed"
PIPESTATE="$DATA_ROOT/.pipeline"          # pipeline logs/state
mkdir -p "$RUNS" "$FASTQC_RAW" "$FASTX" "$FASTQC_TRIM" "$PIPESTATE"
```

## 2) Create the run list (SRRs)

Create the canonical list (one SRR per line):

```bash
RUNS_ALL="$RUNS_DIR/runs.all.txt"
# Put SRR IDs in $RUNS_ALL (one per line). Example:
# SRR123...
# SRR124...
```

Optional: split across members (keep reproducible, one file per member):

```bash
RUNS_PITER="$RUNS_DIR/runs.member.piter.txt"
RUNS_NIKHI="$RUNS_DIR/runs.member.nikhi.txt"
RUNS_SAMUEL="$RUNS_DIR/runs.member.samuel.txt"
```

Sanity check:

```bash
wc -l "$RUNS_ALL"
head -n 5 "$RUNS_ALL"
```

## 3) Download FASTQs (server) — SRA Toolkit

Use the same “one run at a time” approach if you want to be gentle on shared resources.

### Option A: manual (one SRR)

Example (per SRR):

```bash
fastq-dump --split-files --gzip -O "$RUNS" SRRXXXXXXX
```

Sanity checks:

```bash
ls -1 "$RUNS"/SRR*_1.fastq.gz 2>/dev/null | wc -l
ls -1 "$RUNS"/SRR*_2.fastq.gz 2>/dev/null | wc -l
```

### Option B: automated download + FastQC (recommended on server)

Reuse the existing pipeline wrapper (resumable, logs, one SRR at a time):

`Semester5/BIOL550/group_project/pipelines/sra_runs_pipeline_sra3.sh`

On Sequoia, the same scripts are also kept here (so you don’t need the repo checkout on the server):
- `/home/pzg8794/pipelines/sra_runs_pipeline_sra3.sh`
- `/home/pzg8794/pipelines/fastx_trim_fastqc_pipeline.sh`
- `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh`

Minimal setup on server (run lists in the same structure the script expects):

```bash
RUNS_FILE="$HOME/zebrafish/metadata/$ACC/splits/runs.member.piter.txt"  # adjust member name
mkdir -p "$(dirname "$RUNS_FILE")"
```

Start:

```bash
ACC="$ACC" MEMBER="piter" RUNS_FILE="$RUNS_FILE" \
SHARED_RUN_DIR="$RUNS" FASTQC_OUT="$FASTQC_RAW" PIPE_DIR="$PIPESTATE" \
DUMP_THREADS=1 FASTQC_THREADS=1 \
bash Semester5/BIOL550/group_project/pipelines/sra_runs_pipeline_sra3.sh start
```

Monitor:

```bash
bash Semester5/BIOL550/group_project/pipelines/sra_runs_pipeline_sra3.sh status
tail -f "$PIPESTATE"/fastqc.nohup.log
tail -f "$PIPESTATE"/download.nohup.log
```

### Option C: end-to-end runner (recommended when catching up)

This runs the full sequence **download → FastQC (raw) → FASTX trim → FastQC (trimmed)** sequentially and writes all logs under a single dataset root:

`Semester5/BIOL550/group_project/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh`

Example (server):

```bash
ACC="$ACC"
RUNS_FILE="$RUNS_FILE"
DATA_ROOT="/home/zebrafish/mouse/$ACC"

mkdir -p "$DATA_ROOT"

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" \
  DUMP_THREADS=2 FASTQC_THREADS_RAW=1 FASTQC_THREADS_TRIM=2 TRIM_QUAL=20 MIN_LEN=30 \
  bash Semester5/BIOL550/group_project/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh start

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" \
  bash Semester5/BIOL550/group_project/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh status
```

Same command using the server-local copy of the script:

```bash
ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh start
```

Monitor:

```bash
tail -f "$DATA_ROOT/.pipeline/end_to_end.nohup.log"
```

### Option D: end-to-end runner with parallel raw stage (recommended when server is idle)

This variant runs multiple SRRs concurrently during Stage 1 (download + raw FastQC) and uses multi-core compression via `pigz` when available.

Server-local script:
- `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh`

Example (server):

```bash
ACC="PRJNA1017789"
RUNS_FILE="/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.remaining_no_SRR30333743.txt"
DATA_ROOT="/home/zebrafish/mouse/${ACC}_parallel"

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" MEMBER=piter \
  DOWNLOAD_WORKERS=2 FASTQC_WORKERS=2 PIGZ_THREADS=8 \
  DUMP_THREADS=2 FASTQC_THREADS_RAW=2 FASTQC_THREADS_TRIM=2 TRIM_QUAL=20 MIN_LEN=30 \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh start
```

Notes:
- The current run list filename says `remaining_no_SRR30333743` but it contains all 26 SRRs (we re-added SRR30333743 so trim covers the full dataset).
- If you increase workers, do it gradually (e.g., 2 → 3) to avoid disk thrash.

## 4) FastQC on raw reads (server)

```bash
fastqc -t 1 -o "$FASTQC_RAW" "$RUNS"/SRRXXXXXXX_1.fastq.gz "$RUNS"/SRRXXXXXXX_2.fastq.gz
```

Sanity checks:

```bash
ls -1 "$FASTQC_RAW"/*_fastqc.zip  2>/dev/null | wc -l
ls -1 "$FASTQC_RAW"/*_fastqc.html 2>/dev/null | wc -l
```

## 5) Trim reads (server) — FASTX

Keep trimmed reads in a separate directory (don’t overwrite raw):

```bash
# quality trim (example parameters; adjust if needed)
fastq_quality_trimmer -Q33 -t 20 -l 30 < in.fastq > out.fastq
```

If you do adapter clipping, document the adapter sequence and parameters (FASTX `fastx_clipper`).

### Automated trim + trimmed FastQC (recommended on server)

Reuse the existing FASTX+FastQC pipeline:

`Semester5/BIOL550/group_project/pipelines/fastx_trim_fastqc_pipeline.sh`

Start:

```bash
RAW_DIR="$RUNS" OUT_DIR="$FASTX" FASTQC_OUT_DIR="$FASTQC_TRIM" RUNS_FILE="$RUNS_FILE" \
TRIM_QUAL=20 MIN_LEN=30 FASTQC_THREADS=2 DO_FASTQC=yes \
bash Semester5/BIOL550/group_project/pipelines/fastx_trim_fastqc_pipeline.sh start
```

Monitor:

```bash
bash Semester5/BIOL550/group_project/pipelines/fastx_trim_fastqc_pipeline.sh status
tail -f "$FASTX"/.pipeline/fastx.nohup.log
```

## 6) FastQC on trimmed reads (server)

```bash
fastqc -t 1 -o "$FASTQC_TRIM" "$FASTX"/SRRXXXXXXX_1.trim.fastq.gz "$FASTX"/SRRXXXXXXX_2.trim.fastq.gz
```

Sanity checks:

```bash
ls -1 "$FASTQC_TRIM"/*.trim_fastqc.zip  2>/dev/null | wc -l
ls -1 "$FASTQC_TRIM"/*.trim_fastqc.html 2>/dev/null | wc -l
```

## 7) Copy FastQC artifacts to local (Mac) bundles

### Raw FastQC → local

```bash
scp 'USER@HOST:'\"$FASTQC_RAW\"'/SRR*_fastqc.zip'  "$RAW_BUNDLE"/
scp 'USER@HOST:'\"$FASTQC_RAW\"'/SRR*_fastqc.html' "$RAW_BUNDLE"/
```

### Trimmed FastQC → local

```bash
scp 'USER@HOST:'\"$FASTQC_TRIM\"'/*.trim_fastqc.zip'  "$TRIM_BUNDLE"/
scp 'USER@HOST:'\"$FASTQC_TRIM\"'/*.trim_fastqc.html' "$TRIM_BUNDLE"/
```

Important (zsh gotcha): **quote the remote glob** (`'user@host:/path/*.zip'`) or zsh will try to expand it locally and you’ll get `zsh: no matches found`.

Local sanity checks:

```bash
ls -1 "$RAW_BUNDLE"/SRR*_fastqc.zip 2>/dev/null | wc -l
ls -1 "$TRIM_BUNDLE"/SRR*.trim_fastqc.zip 2>/dev/null | wc -l
```

## 8) Summarize FastQC (local) — tables + plots

Reuse the same summarizer script and just point it at your mouse bundles:

```bash
python3 Semester5/BIOL550/group_project/pipelines/fastqc_bundle_summarize.py \
  --qc-bundle "$RAW_BUNDLE" \
  --out-dir   "$ANALYSIS/raw" \
  --stage raw

python3 Semester5/BIOL550/group_project/pipelines/fastqc_bundle_summarize.py \
  --qc-bundle "$TRIM_BUNDLE" \
  --out-dir   "$ANALYSIS/trimmed" \
  --stage trimmed
```

## 9) Notebook (local) — raw vs trimmed comparison

Use the comparison notebook pattern and point its two directories to:

- `mouse/qc_bundle_raw`
- `mouse/qc_bundle_trimmed`

Notebook (mouse-scoped; already created):

```bash
Semester5/BIOL550/group_project/mouse/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse.ipynb
```

Then update the two path variables in the setup cell (raw/trim bundle paths) and run top-to-bottom.

Notebook outputs (tables + plots) are written to:
- `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/`

Note: if trimming/FastQC is still running on the server, your local trimmed bundle will be incomplete; re-copy the trimmed FastQC ZIP/HTML bundle and re-run the notebook once you reach 26/26.

## 10) Monitoring (server)

If you run long jobs with `nohup`, monitor with:

```bash
tail -f "$PIPESTATE"/fastx.nohup.log
tail -f "$PIPESTATE"/fastqc.nohup.log
tail -f "$PIPESTATE"/download.nohup.log
```

## 11) Minimal “done” checklist

- [ ] SRR list saved (`runs.all.txt`) and reviewed
- [ ] Raw FASTQs downloaded (paired counts match)
- [ ] Raw FastQC complete (paired ZIP/HTML counts match)
- [ ] Trimming complete (trimmed FASTQs exist for all SRRs/mates)
- [ ] Trimmed FastQC complete (paired counts match)
- [ ] Local bundles copied (raw + trimmed)
- [ ] Summary tables/plots generated
- [ ] Notebook comparison generated (raw vs trimmed)

## 12) Troubleshooting notes

- **zsh scp globbing**: always quote remote globs: `scp 'user@host:/path/*.zip' dest/`
- **Server maintenance**: design steps to be resumable; rerun only missing SRRs
- **Large SRRs / long runtime**: reduce concurrency; download/QC one SRR at a time; log progress by counting outputs
