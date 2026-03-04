# BIOL550 Group Project — Work Log (dataset + pipeline)

This log captures **what we did**, **the steps**, and **why** (so we can reproduce work and keep the shared server + repo organized).

## 2026-03-02 — Dataset pivot + cleanup (zebrafish → mouse)

### What changed
- We pivoted away from the zebrafish dataset work area and started a **mouse dataset** run using the same workflow (**download → FastQC (raw) → FASTX trim → FastQC (trimmed) → compare**).
- We **archived zebrafish artifacts** locally and on the server into clearly named temp folders so they can be deleted later without hunting.
- We extracted the reusable scripts/notebook into a dataset-agnostic `pipelines/` location (local + server).
- We added an end-to-end runner script to chain the pipeline sequentially when we need to catch up quickly.

### Why
- Avoid mixing outputs across datasets/organisms (prevents confusion and accidental analysis on the wrong files).
- Keep the work resumable and auditable (run lists + logs + consistent directories).
- Make deletion safe later (everything zebrafish goes into one temp folder).

### Local (Mac) actions
1) Created a reusable pipelines directory:
  - `Semester5/BIOL550/group_project/pipelines/` (scripts)
  - `Semester5/BIOL550/group_project/pipelines/notebooks/` (raw vs trimmed notebook template)
2) Created mouse process doc:
   - `Semester5/BIOL550/group_project/mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
3) Archived zebrafish dataset outputs + workspace:
   - Moved into: `Semester5/BIOL550/group_project/_tmp_zebrafish_2026-03-02/`
   - Contents:
     - `qc_bundle/` (raw FastQC bundle)
     - `qc_bundle_trimmed/` (trimmed FastQC bundle)
     - `qc_bundle_non_zebrafish/` (non-project artifacts)
     - `zebrafish/` (old dataset-scoped workspace)

### Server (Sequoia) actions
1) Verified no pipeline processes were running (PID files were stale / processes not running).
2) Kept reusable scripts:
  - `/home/pzg8794/pipelines/`
  - End-to-end runner (local repo): `Semester5/BIOL550/group_project/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh`
3) Archived zebrafish artifacts in home (deletable later):
   - `/home/pzg8794/_tmp_zebrafish_2026-03-02/`
   - Contents:
     - `fastqc_out_trimmed/`
     - `sra_runs_pipeline*/`
     - `zebrafish/` (including the large `tools/` dir)

### Deleting later (when we’re sure)
- Local: `rm -rf Semester5/BIOL550/group_project/_tmp_zebrafish_2026-03-02`
- Server: `rm -rf /home/pzg8794/_tmp_zebrafish_2026-03-02`

---

## 2026-03-02 — Mouse run started (end-to-end)

### Dataset
- BioProject (mouse): `PRJNA1017789` (GEO: `GSE243308`)
- Runs: 26 SRRs (paired-end)

### Run lists
- Local: `Semester5/BIOL550/group_project/mouse/runs/PRJNA1017789_runs.all.txt`
- Server: `/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt`

### Server paths (all outputs under one dataset root)
- `DATA_ROOT=/home/zebrafish/mouse/PRJNA1017789`
- Raw FASTQs: `/home/zebrafish/mouse/PRJNA1017789/sra_runs/`
- Raw FastQC: `/home/zebrafish/mouse/PRJNA1017789/fastqc_out/`
- Trimmed FASTQs: `/home/zebrafish/mouse/PRJNA1017789/fastx_out/`
- Trimmed FastQC: `/home/zebrafish/mouse/PRJNA1017789/fastqc_out_trimmed/`
- Logs: `/home/zebrafish/mouse/PRJNA1017789/.pipeline/`

### Command used (Sequoia)
```bash
ACC=PRJNA1017789
RUNS_FILE=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt
DATA_ROOT=/home/zebrafish/mouse/$ACC

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" MEMBER=piter \
  DUMP_THREADS=2 FASTQC_THREADS_RAW=1 FASTQC_THREADS_TRIM=2 TRIM_QUAL=20 MIN_LEN=30 \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh start
```

### Monitor
```bash
tail -f /home/zebrafish/mouse/PRJNA1017789/.pipeline/end_to_end.nohup.log
tail -f /home/zebrafish/mouse/PRJNA1017789/.pipeline/raw/download.nohup.log
tail -f /home/zebrafish/mouse/PRJNA1017789/.pipeline/raw/fastqc.nohup.log
```

### Stop (if needed)
```bash
ACC=PRJNA1017789
RUNS_FILE=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt
DATA_ROOT=/home/zebrafish/mouse/$ACC

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh stop
```

---

## 2026-03-02 → 2026-03-03 — Parallelized mouse run (faster) + baseline merged

### Why
- The server was idle, and the main bottleneck was **compression + per-run sequencing** (one SRR at a time).
- We kept the baseline job running as a safe fallback, then launched a **parallel raw stage** run (multiple SRRs at once). Once the parallel run proved stable, we stopped the baseline to avoid duplicate work.

### What changed (server)
- New parallel scripts were added under:
  - `/home/pzg8794/pipelines/sra_runs_pipeline_sra3_parallel.sh`
  - `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh`
- New (active) dataset root used for the parallel run:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/`

### Local analysis artifacts (Mac)
- Raw FastQC bundle: `Semester5/BIOL550/group_project/mouse/qc_bundle_raw/` (52 ZIP + 52 HTML)
- Trimmed FastQC bundle: `Semester5/BIOL550/group_project/mouse/qc_bundle_trimmed/` (partial until server reaches 26/26)
- Notebook (raw vs trimmed): `Semester5/BIOL550/group_project/mouse/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse.ipynb`
- Notebook outputs: `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/`

### Important note (run list file name)
- The run list file name still says `remaining_no_SRR30333743`, but we re-added SRR30333743 so **trim runs across all 26 SRRs**:
  - `/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.remaining_no_SRR30333743.txt`

### Parallel run command (server)
```bash
ACC=PRJNA1017789
RUNS_FILE=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.remaining_no_SRR30333743.txt
DATA_ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" MEMBER=piter \
  DOWNLOAD_WORKERS=2 FASTQC_WORKERS=2 PIGZ_THREADS=8 \
  DUMP_THREADS=2 FASTQC_THREADS_RAW=2 FASTQC_THREADS_TRIM=2 TRIM_QUAL=20 MIN_LEN=30 \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh start
```

### Baseline merge step (server)
- We copied SRR30333743 raw FASTQs + raw FastQC outputs into the parallel dataset root (so the parallel root contains the full dataset), then stopped the baseline pipeline.

### Quick status checks (server)
```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel
RUNS=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.remaining_no_SRR30333743.txt

awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/sra_runs/${s}_1.fastq.gz" && -s "$ROOT/sra_runs/${s}_2.fastq.gz" ]] && echo "$s"; done | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/fastqc_out/${s}_1_fastqc.zip" && -s "$ROOT/fastqc_out/${s}_2_fastqc.zip" ]] && echo "$s"; done | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/fastx_out/${s}_1.trim.fastq.gz" && -s "$ROOT/fastx_out/${s}_2.trim.fastq.gz" ]] && echo "$s"; done | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/fastqc_out_trimmed/${s}_1.trim_fastqc.zip" && -s "$ROOT/fastqc_out_trimmed/${s}_2.trim_fastqc.zip" ]] && echo "$s"; done | wc -l
```

---

## 2026-03-04 — Mouse run completed + report draft

### Server completion (PRJNA1017789_parallel)
- Confirmed final counts: 26/26 SRRs for raw FASTQs, raw FastQC, trimmed FASTQs, and trimmed FastQC.
- Completion marker present: `/home/zebrafish/mouse/PRJNA1017789_parallel/.pipeline/end_to_end.completed`

### Local (Mac) completion
- Copied the full trimmed FastQC bundle to: `Semester5/BIOL550/group_project/mouse/qc_bundle_trimmed/` (52 ZIP + 52 HTML).
- Re-ran the comparison notebook to refresh plots + CSV exports under: `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/`.
- Drafted the mouse weekly report: `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_SRA_FastQC_2026-03-04.html`.
