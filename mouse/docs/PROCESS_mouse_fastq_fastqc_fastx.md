# Mouse dataset — repeatable FASTQ → FastQC → FASTX → FastQC workflow

This is the same end-to-end process we used for the zebrafish dataset, but **scoped to the mouse dataset** and kept **separate** so files never mix across organisms/projects.

> Note (2026-03-02): this workflow assumes **bulk RNA-seq** (one FASTQ pair per sample/replicate). If the “mouse dataset” you’re evaluating turns out to be **single-cell RNA-seq**, do not proceed with this bulk-style DE pipeline—pick a bulk dataset and reuse the same steps there.

Work log (what/steps/why): `Semester5/BIOL550/group_project/WORKLOG.md`

## Documentation links

- Parent group-project hub: [../README.md](../README.md)
- Group project documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)
- Course notes: [../../BIOL550-Notes.md](../../BIOL550-Notes.md)
- Lab task hub: [../../BIOL550-Lab/task_n_desc.md](../../BIOL550-Lab/task_n_desc.md)
- Group project work log: [../WORKLOG.md](../WORKLOG.md)
- Mouse task tracker: [TODO_mouse.md](TODO_mouse.md)
- Mouse remediation plan: [TODO_qc_remediation.md](TODO_qc_remediation.md)
- Server minimum policy: [../SERVER_MINIMUM_POLICY.md](../SERVER_MINIMUM_POLICY.md)

Use this file for the operational workflow. Use the work log for dated history and the TODO files for active work and remediation decisions.

## IMPORTANT — server must keep the minimum only

**Most of our work must live locally, not on the server.**

Server goal:
- keep the minimum needed to run jobs
- keep the minimum needed to prove and inspect results
- keep the minimum needed to continue the workflow safely

Server non-goal:
- it is **not** the main home for notebooks
- it is **not** the main home for long custom code
- it is **not** the main home for exploratory analysis logic

Working rule:
- long code stays local
- long code is copied to the server only when needed to run
- the server copy is deleted after outputs are verified
- short wrappers/templates are okay to keep on the server

Reason:
- protect our work from being copied, reused, or picked apart
- reduce clutter and disk use
- keep the local repo as the authoritative source of logic

Read first:
- [../SERVER_MINIMUM_POLICY.md](../SERVER_MINIMUM_POLICY.md)

## Current mouse dataset (active)

- BioProject: `PRJNA1017789` (mouse; GEO: `GSE243308`)
- Runs list (local): `Semester5/BIOL550/group_project/mouse/runs/PRJNA1017789_runs.all.txt` (26 SRRs)
- Runs list (server): `/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt`
- Server dataset root (active run): `/home/zebrafish/mouse/PRJNA1017789_parallel/`
- TODO list (keep updated): `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`

## Local Python environment (use one env only)

Use the BIOL550 course environment for all local notebook/script work:

```bash
cd /Users/pitergarcia/DataScience
source Semester5/BIOL550/biol550_env/bin/activate
```

Do not create dataset-specific or notebook-specific BIOL550 virtual environments.

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

> Tooling note (2026-03-05): FASTX is the “class/legacy” trimmer. For adapter-focused targeted trimming on paired-end reads, prefer `fastp` (and for primer/amplicon trimming, prefer `cutadapt`). See `Semester5/BIOL550/BIOL550-Notes.md` (“fastp vs FASTX Toolkit”) for examples.

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

## 10) QC remediation experiments (server + local)

Once the baseline raw-vs-FASTX comparison is frozen, keep remediation experiments in a separate tree and compare them in a separate notebook.

Planning + decisions:
- `Semester5/BIOL550/group_project/mouse/TODO_qc_remediation.md`

Remediation notebook (keep separate from the baseline notebook):
- `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`

### Server workspace rule for remediation

Use two different roots for two different purposes:

- shared raw input source:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/`
- trusted remediation workspace:
  - `/home/pzg8794/mouse_qc_remediation/`

Why:
- the shared raw inputs audited cleanly
- the shared derived outputs did not remain stable enough to use as the remediation baseline
- all controlled remediation runs, logs, and comparisons should therefore live in `/home/pzg8794/mouse_qc_remediation/`

### Freeze the trusted baseline in home

Use these copied baseline bundles as the comparison reference:
- `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_raw/`
- `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_trimmed/`

These should mirror the trusted local project bundles and should not be overwritten during remediation.

### Pilot runs

Start with the three most informative SRRs:
- `SRR30333754`
- `SRR30333756`
- `SRR30333743`

### `fastp` pilot

```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel \
bash Semester5/BIOL550/group_project/pipelines/qc_remed_fastp_one_srr.sh SRR30333754
```

The script writes:
- trimmed FASTQs under `qc_remediation/fastp/out/`
- `fastp` HTML/JSON reports under `qc_remediation/fastp/reports/`
- post-remediation FastQC under `qc_remediation/fastqc_after/fastp/`

Home-workspace equivalent paths used for the controlled pilot:
- `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
- `/home/pzg8794/mouse_qc_remediation/output/fastp/reports/`
- `/home/pzg8794/mouse_qc_remediation/output/fastqc_after/fastp/`

### `cutadapt` pilot

Poly-G / two-color chemistry style cleanup:

```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel \
NEXTSEQ_TRIM=20 \
bash Semester5/BIOL550/group_project/pipelines/qc_remed_cutadapt_one_srr.sh SRR30333754
```

Explicit adapter example (plus optional poly-G cleanup):

```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel \
ADAPTER_R1=GATCGGAAGAGCACACGTCTGAACTCCAGTCACATGAGGCCATCTGGGGG \
NEXTSEQ_TRIM=20 \
bash Semester5/BIOL550/group_project/pipelines/qc_remed_cutadapt_one_srr.sh SRR30333743
```

Home-workspace equivalent paths used for the controlled pilot:
- `/home/pzg8794/mouse_qc_remediation/output/cutadapt/out/`
- `/home/pzg8794/mouse_qc_remediation/output/cutadapt/reports/`
- `/home/pzg8794/mouse_qc_remediation/output/fastqc_after/cutadapt/`

### Controlled pilot wrapper actually used on the server

Script:
- `/home/pzg8794/mouse_qc_remediation/scripts/run_pilot_remediation.sh`

Log:
- `/home/pzg8794/mouse_qc_remediation/logs/run_pilot_remediation.2026-03-09_232002.log`

What it does:
- runs `fastp` on `SRR30333754`, `SRR30333756`, `SRR30333743`
- runs `cutadapt` with `NEXTSEQ_TRIM=20` on the poly-G dominated SRRs
- runs `cutadapt` with explicit `ADAPTER_R1` + `NEXTSEQ_TRIM=20` on `SRR30333743`

Last verified checkpoint from that run:
- `fastp` completed for `SRR30333754`
- the next active step was `FastQC` on the new `SRR30333754` `fastp` outputs

### What to compare after each run

- `Adapter Content` status before vs after
- `Overrepresented sequences` before vs after
- `adapter_max` before vs after
- reads retained / read length after cleanup
- compare each new tool against both:
  - raw
  - the current `FASTX`-trimmed baseline

Do not use duplication alone as the deciding metric; for this bulk RNA-seq dataset it is likely a library/data property rather than a trimming target.

### Terminal-first comparison workflow

Use the terminal to generate the comparison package, then use the notebook only to display it.

Primary script:
- `Semester5/BIOL550/group_project/pipelines/mouse_qc_strategy_compare.py`

Server copy:
- `/home/pzg8794/mouse_qc_remediation/scripts/mouse_qc_strategy_compare.py`

Runner:
- `/home/pzg8794/mouse_qc_remediation/scripts/run_compare.sh`

What this script produces:
- `pilot_read_stage_metrics.csv`
- `pilot_adapter_curve_data.csv`
- `pilot_srr_comparison_wide.csv`
- `pilot_fastp_run_metrics.csv`
- `pilot_cutadapt_run_metrics.csv`
- `pilot_summary.md`

Preliminary compare already generated:
- `/home/pzg8794/mouse_qc_remediation/compare/preliminary/`

What that preliminary compare established:
- `FASTX` changed read length / tail quality behavior
- `FASTX` did not materially remove the dominant technical signal in the pilot runs
- the unresolved targets are still:
  - poly-G dominated read 2 signal in `SRR30333754` and `SRR30333756`
  - explicit TruSeq adapter signal in `SRR30333743_1`

Final compare target:
- `/home/pzg8794/mouse_qc_remediation/compare/final/`

Current pilot outcome:
- `fastp` is the current default remediation choice for this mouse dataset because it reduced adapter/poly-G signal much more strongly than `cutadapt` across the three pilot reads.
- `cutadapt` remains the targeted fallback when we need explicit adapter-sequence control.
- See `TODO_qc_remediation.md` and `../WORKLOG.md` for the per-SRR results and the decision rationale.

### Local notebook + artifact layer

Use the local notebook only as the presentation/view layer for the already-generated comparison package:

- notebook:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
- supporting local artifact folder:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/`

Main files shown in the notebook:
- `final_problem_raw_vs_fastx.png`
- `final_baseline_raw_vs_fastx_gc_bellshape.png`
- `final_fastp_vs_baseline.png`
- `final_cutadapt_vs_baseline.png`
- `final_all_tools_comparison.png`
- `final_adapter_delta_vs_fastx.png`
- `final_retention_vs_adapter_tradeoff.png`
- `final_status_heatmap_focus_reads.png`
- `final_fastp_gc_bellshape_all_srrs.png`
- `final_cutadapt_gc_bellshape_all_srrs.png`
- `final_all_tools_gc_bellshape_all_srrs.png`
- `final_bell_gallery_2x2.png`
- `pilot_srr_comparison_wide.csv`
- `pilot_read_stage_metrics.csv`
- `pilot_fastp_run_metrics.csv`
- `pilot_cutadapt_run_metrics.csv`

Interpretation rule:
- make the tool decision from the per-read comparison metrics (`adapter_max`, status changes, retained reads)
- use the all-SRR GC bell-shape figures as a dataset-level sanity check after the tool-specific swaps

### How to read the GC bell-shape plots

- shaded band:
  - the `25th` to `75th` percentile range at each `%GC` position
  - shows how much the reports vary within that stage
- bold line:
  - the stage median curve
  - used instead of the mean because it is less sensitive to a small number of unusual SRRs
- line styles / colors:
  - `Raw` = gray dashed
  - `Current FASTX` = red solid
  - `FASTX + fastp pilot replacements` = green solid
  - `FASTX + cutadapt pilot replacements` = purple dash-dot
- trimmed baseline:
  - `Current FASTX` is the trimmed baseline
  - compare each remediation stage against that line, not only against raw
- decision rule:
  - if GC bell shapes remain reasonable for both tools, the bell plot does not choose the winner
  - choose the winner from the remediation metrics (`adapter_max`, status changes, retained reads)

### Best plot types for this remediation question

- best ranking plot:
  - delta vs `Current FASTX` (trimmed baseline) for `adapter_max` and retained reads
  - use a dumbbell / slope-style comparison or a compact paired bar chart per SRR
- best summary table:
  - one row per focus SRR with raw, `FASTX`, `fastp`, `cutadapt`, plus delta vs `FASTX`
- best sanity-check plot:
  - the GC bell-shape figures already in the notebook
- best dataset-level comparison panel:
  - the `2x2` bell gallery for baseline + `fastp` + `cutadapt` + all stages together

Reasoning:
- FastQC says the GC-content module is for detecting unusual library-shape deviations and contamination patterns, not for deciding adapter/poly-G cleanup quality by itself.
- Therefore, use the bell plots to confirm that the library shape still looks reasonable, and use the delta-to-baseline remediation metrics to choose the winning tool.

### Research-backed plotting stack for this remediation question

Official references used for this guidance:
- MultiQC reports: https://docs.seqera.io/multiqc/reports
- MultiQC custom content: https://docs.seqera.io/multiqc/custom_content
- MultiQC FastQC module: https://docs.seqera.io/multiqc/modules/fastqc
- seaborn `pointplot`: https://seaborn.pydata.org/generated/seaborn.pointplot.html
- seaborn `lineplot`: https://seaborn.pydata.org/generated/seaborn.lineplot.html
- seaborn `heatmap`: https://seaborn.pydata.org/generated/seaborn.heatmap.html
- seaborn error bars tutorial: https://seaborn.pydata.org/tutorial/error_bars.html
- seaborn color palettes: https://seaborn.pydata.org/generated/seaborn.color_palette.html
- Plotly line charts: https://plotly.com/python/line-charts/
- Plotly heatmaps: https://plotly.com/python/heatmaps/
- Plotly box plots: https://plotly.com/python/box-plots/
- fastp reports / before-vs-after QC: https://github.com/OpenGene/fastp

What these sources support:
- MultiQC is the best single report layer when we want one interactive QC dashboard across many samples.
- MultiQC custom content can render `generalstats`, `table`, `bargraph`, `linegraph`, `boxplot`, `scatter`, `heatmap`, and `violin`, so our custom remediation summaries can live in the same report as the standard FastQC outputs.
- seaborn `pointplot` is preferable to plain bar plots when the goal is comparison across categories.
- seaborn `lineplot` supports aggregated stage curves with explicit interval choices such as percentile intervals.
- seaborn percentile intervals are a good fit for this notebook because QC metrics are often skewed or bounded.
- MultiQC FastQC docs support adding a theoretical GC guide for mouse, including `mm10_txome`, which is the most relevant reference if we keep using GC bell plots as a sanity check.
- fastp provides before/after QC summaries in JSON and HTML, which makes it easy to build stage-to-stage comparison tables and plots.

Recommended plot stack for this notebook and report:
- primary decision plot:
  - delta vs `Current FASTX` for `adapter_max` and retained reads
  - preferred form: dumbbell / slope-style plot per SRR
  - why: this answers the actual decision question directly: did this tool improve the trimmed baseline, and by how much?
- secondary decision plot:
  - retained reads vs residual adapter signal scatter plot
  - x = retained read fraction, y = `adapter_max`, one point per SRR/tool
  - why: this makes the cleanup-vs-retention tradeoff visible in one figure
- status summary plot:
  - sample/module/stage heatmap for pass / warn / fail
  - why: best compact view for what changed globally across modules
- distribution plot:
  - box / violin + strip overlay for per-stage distributions of `adapter_max`, `pbq_min_10th`, and retained reads
  - why: better than bars when we need to show spread, not just a center
- curve plot:
  - line plot with median + percentile band for the all-SRR GC curves
  - why: keep as a sanity check for overall library shape, not as the main tool-ranking plot
- focused pilot plot:
  - small multiples for the problematic pilot SRRs, showing raw -> `FASTX` -> `fastp` -> `cutadapt`
  - why: these are the only reads where fine-grained signal comparisons should drive the explanation

Recommended tool split:
- MultiQC:
  - use for one integrated HTML QC report
  - include standard FastQC modules plus a custom remediation section
- seaborn + matplotlib:
  - use for the notebook and static report figures
  - strongest fit for publication-style comparisons and compact small multiples
- Plotly:
  - use only if we want hover / zoom / interactive faceting for many SRRs
  - especially useful for heatmaps and scatter plots when sample count grows

Plotting rules for this project:
- compare every remediation tool against `Current FASTX`, not only against raw
- do not use bar plots where the real goal is comparing category-to-category changes; use points, slopes, or distributions instead
- use color consistently by stage across all plots
- keep the GC bell plot in the notebook, but treat it as a library-shape sanity check only
- when possible, add the `mm10_txome` theoretical GC guide so the bell plot has a visible reference, not only relative stage curves

Current implementation in the notebook:
- primary ranking plot implemented:
  - `final_adapter_delta_vs_fastx.png`
- tradeoff plot implemented:
  - `final_retention_vs_adapter_tradeoff.png`
- categorical status summary implemented:
  - `final_status_heatmap_focus_reads.png`
- validation layer kept:
  - GC bell-shape plots + `final_bell_gallery_2x2.png`
- final external validation still planned:
  - generate a MultiQC report from the server once the workflow is frozen

### MultiQC validation strategy

Reporting position:
- for this project, the **primary validation layer** is our custom comparison workflow
- that workflow automates the manual file-by-file review process by reading the underlying FastQC outputs directly and comparing them across stages
- MultiQC is the **supplementary aggregation / confirmation layer**
- in report language, describe MultiQC as corroborating and summarizing the file-level findings, not replacing them

What we are doing:
- do **one pilot comparison MultiQC report now**
  - compare `raw`, `Current FASTX`, `fastp`, and `cutadapt` for the 3 pilot SRRs
- do **one final chosen-tool MultiQC report later**
  - generate it after `fastp` is run across all SRRs

What we are not doing:
- we are **not** generating one separate MultiQC report per tool as the main validation layer
- we are **not** generating a full-dataset `fastp` vs `cutadapt` report right now, because only the pilot SRRs have post-tool outputs

What we may do as supporting analysis:
- generate a **FASTX baseline MultiQC** report for the full dataset
- generate a **FASTX vs fastp** full-dataset MultiQC comparison report
- use those as supplementary validation while keeping the notebook + custom comparison workflow as the primary analysis layer

Reasoning:
- right now, `raw` and `FASTX` exist for all `52` FastQC reports, but `fastp` and `cutadapt` exist only for the pilot `6` report zips
- a full-dataset all-tools MultiQC report would therefore be an apples-to-oranges comparison
- the right immediate report is a pilot comparison report
- the right final report is a full-dataset MultiQC for the chosen tool (`fastp`)
- this matches the professor’s preference for file-by-file inspection because our workflow is effectively an automated manual review of each FastQC report before we look at the aggregated MultiQC layer

Current server-side MultiQC implementation:
- install location:
  - `~/.local/bin/multiqc`
- helper scripts:
  - local source: `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_pilot_compare.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_final_fastp.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_fastx_baseline.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_fastx_vs_fastp.sh`
  - server copy: `/home/pzg8794/mouse_qc_remediation/scripts/mouse_multiqc_pilot_compare.sh`
  - server copy: `/home/pzg8794/mouse_qc_remediation/scripts/mouse_multiqc_final_fastp.sh`
  - server copy: `/home/pzg8794/mouse_qc_remediation/scripts/mouse_multiqc_fastx_baseline.sh`
  - server copy: `/home/pzg8794/mouse_qc_remediation/scripts/mouse_multiqc_fastx_vs_fastp.sh`
- current report path:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/pilot_compare/report/mouse_pilot_compare_multiqc.html`
- supplemental baseline report:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/fastx_baseline_all_srrs/report/mouse_fastx_baseline_all_srrs_multiqc.html`
- supplemental comparison report:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/fastx_vs_fastp_all_srrs/report/mouse_fastx_vs_fastp_all_srrs_multiqc.html`
- local analysis copy:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_pilot_compare_server/`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_baseline_server/`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_vs_fastp_server/`

Why `--dirs --dirs-depth 1` is used:
- MultiQC official docs recommend prefixing sample names with directory context when the same sample appears in multiple input folders
- that avoids collisions between `raw`, `FASTX`, `fastp`, and `cutadapt` versions of the same pilot read

Server cleanup rule:
- keep:
  - FastQC zip/html outputs
  - `fastp` JSON reports
  - `cutadapt` logs
  - final compare CSVs / summaries
  - MultiQC HTML + data directory
- delete when no longer needed:
  - large intermediate trimmed FASTQ files under `output/fastp/out/` and `output/cutadapt/out/`
  - temporary package caches such as `~/.cache/pip`

### Server code residency rule

To reduce exposure of our custom code on `sequoia`:
- keep long / custom logic **local only**
- copy it to `/home/pzg8794` only right before execution
- delete the server copy after the run finishes and the outputs are verified

Current working threshold:
- treat scripts longer than about `100` lines as “long code”

What remains on the server:
- short execution wrappers only, for example:
  - `/home/pzg8794/mouse_qc_remediation/scripts/run_compare.sh`
  - `/home/pzg8794/mouse_qc_remediation/scripts/run_pilot_remediation.sh`
  - `/home/pzg8794/mouse_qc_remediation/scripts/qc_remed_fastp_one_srr.sh`
  - `/home/pzg8794/mouse_qc_remediation/scripts/qc_remed_cutadapt_one_srr.sh`
  - `/home/pzg8794/mouse_qc_remediation/scripts/mouse_multiqc_pilot_compare.sh`
  - `/home/pzg8794/mouse_qc_remediation/scripts/mouse_multiqc_final_fastp.sh`

What was removed from the server and must be recopied before reuse:
- `/home/pzg8794/mouse_qc_remediation/scripts/mouse_qc_strategy_compare.py`
  - local source: `Semester5/BIOL550/group_project/pipelines/mouse_qc_strategy_compare.py`
- `/home/pzg8794/pipelines/download_fastq_sratoolkit.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/download_fastq_sratoolkit.sh`
- `/home/pzg8794/pipelines/fastx_trim_fastqc_pipeline.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/fastx_trim_fastqc_pipeline.sh`
- `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh`
- `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh`
- `/home/pzg8794/pipelines/sra_runs_pipeline_sra3.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/sra_runs_pipeline_sra3.sh`
- `/home/pzg8794/pipelines/sra_runs_pipeline_sra3_parallel.sh`
  - local source: `Semester5/BIOL550/group_project/pipelines/sra_runs_pipeline_sra3_parallel.sh`

Minimal reuse pattern:
```bash
scp Semester5/BIOL550/group_project/pipelines/<script> pzg8794@sequoia.rit.edu:/home/pzg8794/<target>/
ssh pzg8794@sequoia.rit.edu 'bash /home/pzg8794/<target>/<script>'
ssh pzg8794@sequoia.rit.edu 'rm -f /home/pzg8794/<target>/<script>'
```

Preferred local helper:
```bash
Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh list
Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh push mouse_qc_strategy_compare.py
Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh remove mouse_qc_strategy_compare.py
```

Use that helper to stage long scripts to `/home/pzg8794` only when a server run requires them.

## 11) Monitoring (server)

If you run long jobs with `nohup`, monitor with:

```bash
tail -f "$PIPESTATE"/fastx.nohup.log
tail -f "$PIPESTATE"/fastqc.nohup.log
tail -f "$PIPESTATE"/download.nohup.log
```

For the home remediation wrapper, monitor with:

```bash
tail -f /home/pzg8794/mouse_qc_remediation/logs/run_pilot_remediation.2026-03-09_232002.log
```

## 12) Minimal “done” checklist

- [ ] SRR list saved (`runs.all.txt`) and reviewed
- [ ] Raw FASTQs downloaded (paired counts match)
- [ ] Raw FastQC complete (paired ZIP/HTML counts match)
- [ ] Trimming complete (trimmed FASTQs exist for all SRRs/mates)
- [ ] Trimmed FastQC complete (paired counts match)
- [ ] Local bundles copied (raw + trimmed)
- [ ] Summary tables/plots generated
- [ ] Notebook comparison generated (raw vs trimmed)
- [ ] Remediation pilot completed and documented
- [ ] Remediation notebook updated with tool comparison and final tool choice

## 13) Troubleshooting notes

- **zsh scp globbing**: always quote remote globs: `scp 'user@host:/path/*.zip' dest/`
- **Server maintenance**: design steps to be resumable; rerun only missing SRRs
- **Large SRRs / long runtime**: reduce concurrency; download/QC one SRR at a time; log progress by counting outputs
