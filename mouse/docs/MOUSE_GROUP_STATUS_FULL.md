# Mouse project — full group status

Purpose:
- give the group one complete project snapshot
- show what has already been done, where the files live, and what decisions have already been made
- reduce repeated questions about current status, server paths, and QC cleanup work

## Read this first

If you only read three files, read these in order:
1. `PROCESS_mouse_fastq_fastqc_fastx.md`
2. `TODO_mouse.md`
3. `TODO_qc_remediation.md`

Related docs:
- Group project map: `../DOCUMENTATION_MAP.md`
- Work log: `../WORKLOG.md`
- Team-share alignment draft: `ALIGNMENT_PREP_TEAM_DRAFT.md`
- Main remediation notebook: `notebooks/qc_remediation_experiments_mouse.ipynb`
- Team-follow notebook copy: `notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`

## Dataset in use

- Active dataset: mouse bulk RNA-seq
- BioProject: `PRJNA1017789`
- GEO: `GSE243308`
- The zebrafish work is retired and should not be used for active decisions.

## What has already been done

### 1) Raw pipeline completed
- raw FASTQs downloaded
- raw FastQC completed
- original FASTX trimming completed
- post-FASTX FastQC completed

### 2) Baseline QC review completed
- baseline notebook compares raw vs current FASTX-trimmed data
- this established that FASTX changed quality/length behavior but did not remove the main residual adapter-related signal

Main baseline notebook:
- `notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse.ipynb`

Main baseline outputs:
- `qc_analysis_raw_vs_trimmed/`

### 3) Remediation comparison completed
The remediation stage compared:
- `FASTX` baseline
- `FASTX + cutadapt`
- `fastp`

This was done:
- first on the most problematic pilot reads
- then against the full-dataset FASTX baseline

Main remediation notebook:
- `notebooks/qc_remediation_experiments_mouse.ipynb`

Main remediation outputs:
- `qc_analysis_remediation/`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/`

### 4) Full chosen-tool rerun completed
- `fastp` was run across all `26` paired-end SRRs
- post-`fastp` FastQC was completed across all `52` read-level reports
- MultiQC summaries were generated for:
  - FASTX baseline
  - FASTX vs fastp

## Current decision state

### Cleanup tool
- default cleanup tool: `fastp`
- targeted fallback only if needed later: `cutadapt`

### Why
The file-by-file QC comparison and the full-dataset comparison both show:
- FASTX baseline still had strong adapter-related failures
- `fastp` reduced the residual adapter signal to near zero
- `fastp` preserved strong read retention
- `cutadapt` remained useful as a backup, but it was not the strongest default cleanup tool for this dataset

## Evidence package to use

If someone asks “where is the proof?”, use these:

### Report
- `reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`

### Full-dataset comparison outputs
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_summary.md`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_read_metrics.csv`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_status_counts.csv`

### Main figures
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_adapter_comparison.png`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_summary_dashboard.png`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_retention_tradeoff.png`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_status_table_heatmap.png`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_top_residual_reads.png`

## Server paths that matter

### Shared raw source
- `/home/zebrafish/mouse/PRJNA1017789_parallel/`

### Home-side remediation workspace
- `/home/pzg8794/mouse_qc_remediation/`

### Chosen cleaned FASTQ outputs
- `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`

### Full chosen-tool MultiQC
- `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/report/mouse_fastp_all_srrs_multiqc.html`

## What is still open

These are still active discussion / prep items:
- confirm the final cleaned-input root for alignment
- confirm whether any sample still needs targeted `cutadapt`
- confirm the reference genome + annotation pair
- build the sample/design sheet
- prepare the STAR manifest and alignment-QC capture template

Draft for the first two:
- `ALIGNMENT_PREP_TEAM_DRAFT.md`

## What the group does **not** need to do right now

- do not rerun the full QC remediation from scratch unless we explicitly decide to
- do not treat every remaining FastQC warning as a reason to trim more
- do not use the old FASTX outputs as the preferred alignment input
- do not leave long custom code on the server

## If you want to help without breaking anything

Best places to help next:
1. review the alignment-prep draft
2. verify the reference + annotation choice
3. help complete the sample/design sheet
4. review the report/notebook and use the evidence already generated instead of rerunning the pipeline

## Practical rule

Before asking a workflow question, check:
- `PROCESS_mouse_fastq_fastqc_fastx.md`
- `TODO_mouse.md`
- `TODO_qc_remediation.md`
- `notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`

That should answer most operational questions directly.
