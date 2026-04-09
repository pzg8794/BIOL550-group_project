# Mouse QC remediation and cleanup plan (PRJNA1017789 / GSE243308)

This is an **exploration + cleaning** phase before alignment. The goal is to learn which cleanup tools are appropriate for this dataset, test them on the runs with the clearest technical signals, quantify before/after changes, and then choose the alignment input based on evidence.

## Documentation links

- Parent mouse workflow: [PROCESS_mouse_fastq_fastqc_fastx.md](PROCESS_mouse_fastq_fastqc_fastx.md)
- Mouse task tracker: [TODO_mouse.md](TODO_mouse.md)
- Group project documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)
- Group project work log: [../WORKLOG.md](../WORKLOG.md)
- Course notes: [../../BIOL550-Notes.md](../../BIOL550-Notes.md)
- Lab task hub: [../../BIOL550-Lab/task_n_desc.md](../../BIOL550-Lab/task_n_desc.md)
- Server minimum policy: [../SERVER_MINIMUM_POLICY.md](../SERVER_MINIMUM_POLICY.md)

Use this file for remediation-specific reasoning, tool comparisons, and decision criteria. Use the work log for dated milestones and the TODO file for current task state.

## IMPORTANT — keep server content minimal

**The server must keep the minimum for us to work.  
Most of the real code and analysis must stay local.**

What this means in practice:
- keep notebooks local
- keep long scripts local
- keep analysis / comparison / plotting logic local
- copy long code to the server only when needed to run
- delete the copied server code after the run
- keep only:
  - required inputs
  - required outputs
  - logs
  - reports
  - short wrappers / templates

Why this is policy:
- we want to keep our work from being stolen, copied, or unnecessarily picked on
- we want the server to stay lean
- we want the local repo to remain the single source of truth

Read first:
- [../SERVER_MINIMUM_POLICY.md](../SERVER_MINIMUM_POLICY.md)

## Environment rule

Use the single BIOL550 environment for all local notebook and Python work:
- `/Users/pitergarcia/DataScience/Semester5/BIOL550/biol550_env`

Activate it before running notebooks or local analysis scripts:

```bash
cd /Users/pitergarcia/DataScience
source Semester5/BIOL550/biol550_env/bin/activate
```

Do not create a new BIOL550 remediation venv for this phase.

## Decision question

Which cleanup tool gives the best tradeoff between:
- reducing **technical sequence signal** (`Adapter Content`, technical `Overrepresented sequences`, `adapter_max`)
- preserving enough read length / read count for alignment
- staying reproducible and well-documented for the team notebook + report

## Baseline evidence from the current QC analysis

Sources:
- `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/fastqc_warn_fail_modules_by_srr_full.md`
- `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/fastqc_overrepresented_sequences.csv`
- `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_SRA_FastQC_2026-03-04.html`

Key findings already established:
- `Adapter Content` = FAIL for **26/26 SRRs** in both raw and FASTX-trimmed stages.
- `Sequence Duplication Levels` = FAIL for **26/26 SRRs** in both stages; this is **not** the main cleanup target because it is often expected in bulk RNA-seq.
- `Per sequence GC content` is broadly stable before/after trimming; there is **no strong dataset-wide GC shift** suggesting a separate contamination batch.
- The `Overrepresented sequences` table shows two main technical patterns:
  - long **poly-G** runs in many read 2 files
  - a **TruSeq adapter** hit in `SRR30333743_1`
- FASTX quality trimming improved tail quality, but **did not change the dominant adapter/overrep signals**.

Interpretation:
- This is no longer a “more quality trimming” problem.
- This is a **targeted technical-sequence cleanup** problem.

## Canonical server layout

### Shared input root (read-only baseline source)

Active dataset root:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/`

What this root is for:
- raw FASTQ input (`sra_runs/`)
- original raw FastQC output (`fastqc_out/`)

What this root is **not** for anymore:
- trusted remediation comparisons
- trusted post-tool outputs

Reason:
- the shared raw inputs audited cleanly
- the shared derived outputs did not stay consistent enough to use as the controlled remediation baseline

### Trusted remediation workspace (home-owned)

Use this as the canonical remediation workspace:
- `/home/pzg8794/mouse_qc_remediation/`

Structure:
- baseline copies:
  - `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_raw/`
  - `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_trimmed/`
- scripts:
  - `/home/pzg8794/mouse_qc_remediation/scripts/`
- logs:
  - `/home/pzg8794/mouse_qc_remediation/logs/`
- outputs:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/reports/`
  - `/home/pzg8794/mouse_qc_remediation/output/cutadapt/out/`
  - `/home/pzg8794/mouse_qc_remediation/output/cutadapt/reports/`
  - `/home/pzg8794/mouse_qc_remediation/output/fastqc_after/fastp/`
  - `/home/pzg8794/mouse_qc_remediation/output/fastqc_after/cutadapt/`
- comparisons:
  - `/home/pzg8794/mouse_qc_remediation/compare/preliminary/`
  - `/home/pzg8794/mouse_qc_remediation/compare/final/`

## Verified server state (audit snapshot)

Shared raw inputs were verified as intact:
- `sra_runs/` = `52` FASTQ files
- `fastqc_out/` = `104` FastQC files
- ownership/date pattern matched the original run (`pzg8794:zebrafish`, `2026-03-02`)
- the raw sample set and raw FastQC sample set matched exactly

Shared derived outputs were not accepted as the remediation baseline:
- `fastp_out/` only contained a manual rerun for `SRR30333743`
- `fastqc_fastp_trim/` only contained the matching FastQC for that one rerun
- those files were owned by `nb6672` and dated `2026-03-05`
- `fastx_out/` and `fastqc_out_trimmed/` were missing from the shared tree at the time of the audit

Decision:
- trust shared raw inputs
- distrust shared derived outputs for remediation comparisons
- freeze baseline bundles in `/home/pzg8794/mouse_qc_remediation/baseline/`

## Tools to evaluate

### 1) `fastp` — first-line paired-end remediation

What it does:
- paired-end aware adapter detection
- poly-G trimming
- quality-tail trimming
- HTML/JSON run report

Why it fits this dataset:
- the unresolved issue is mostly **adapter/poly-G**, not just low-quality tails
- the strongest recurring technical signal is **poly-G in read 2**
- it is safer than legacy single-purpose tools for paired-end cleanup

How we will use it:
- script: `Semester5/BIOL550/group_project/pipelines/qc_remed_fastp_one_srr.sh`
- current behavior:
  - adapter detection: `--detect_adapter_for_pe`
  - poly-G cleanup: `--trim_poly_g`
  - quality tail trimming: `--cut_tail --cut_mean_quality 20`
  - minimum length: `--length_required 30`

Decision expectation:
- `fastp` is the likely best default if the pilot lowers adapter/poly-G signal without excessive shortening.

### 2) `cutadapt` — targeted confirmation / explicit sequence handling

What it does:
- explicit adapter trimming (`-a` / `-A`)
- quality trimming
- optional NextSeq/NovaSeq poly-G handling (`--nextseq-trim`)

Why it matters:
- we already have at least one explicit technical sequence (`SRR30333743_1` TruSeq adapter)
- it is the right tool when we want sequence-explicit control instead of auto-detection

How we will use it:
- script: `Semester5/BIOL550/group_project/pipelines/qc_remed_cutadapt_one_srr.sh`
- supported modes:
  - explicit adapters via `ADAPTER_R1` / `ADAPTER_R2`
  - poly-G style cleanup via `NEXTSEQ_TRIM`
  - both together if needed

Decision expectation:
- `cutadapt` is the best comparison tool for explicit adapters or if we want tighter control over a subset of runs.

### 3) `FASTX fastx_clipper` — legacy reference only

What it does:
- clips a known sequence from read ends

Why it is not the main batch choice here:
- not paired-end aware
- not a good primary answer to the widespread read 2 poly-G pattern
- weaker fit for a clean, scalable comparison across many paired-end SRRs

How we will treat it:
- keep it as a historical / class-tool reference
- use only for a narrow one-off sanity check if we need to show why a newer paired-end tool is the better project choice

## Experiment design

### Phase 0 — freeze the baseline

Do not overwrite:
- `mouse/qc_bundle_raw/`
- `mouse/qc_bundle_trimmed/`
- `mouse/qc_analysis_raw_vs_trimmed/`
- `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_raw/`
- `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_trimmed/`

Reason:
- the baseline notebook already answers “what FASTX quality trimming changed”
- remediation experiments must stay separate so the comparison remains clean

### Phase 1 — pilot on the most informative SRRs

Pilot set:
- `SRR30333754` — highest severity, poly-G overrepresented in read 2
- `SRR30333756` — highest severity, poly-G overrepresented in read 2
- `SRR30333743` — high severity, explicit TruSeq adapter in read 1

Pilot tools:
- run `fastp` on all three pilot SRRs
- run `cutadapt` on all three pilot SRRs
  - for `SRR30333743`, include the explicit adapter sequence(s)
  - for the poly-G dominated runs, include `NEXTSEQ_TRIM=20`

Why this pilot is enough to start:
- it covers the two clearest technical patterns seen so far
- it keeps the first pass small enough to inspect carefully before scaling

### Phase 2 — evaluate before/after in a separate notebook

Notebook for remediation only:
- `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`

What belongs in this notebook:
- pilot SRR manifest
- tool/parameter table
- before/after FastQC status deltas
- technical overrepresented sequence changes
- retention / read-length checks
- final tool choice and rationale

Important implementation decision:
- generate the comparison artifacts in the terminal first
- use the notebook only to display those finished tables/plots
- do not make the notebook the primary place where parsing and comparison logic lives

## 2026-03-18 — alignment handoff from remediation into production mapping

The remediation phase now feeds directly into a production alignment setup:
- private alignment root:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`
- private launcher:
  - PID `71166`
  - log: `/home/pzg8794/mouse_qc_remediation/logs/run_star_all26_fastp_parallel.2026-03-17_233805.log`
- shared follow-on launcher:
  - PID `72403`
  - log: `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/run_star_all26_fastp_shared_after_private.2026-03-18_020015.log`

Decision:
- do **not** build a second shared STAR index immediately
- let the private run remain canonical for the first complete index + alignment launch
- once the private completion flag exists, sync the finished `GRCm39` + `Ensembl` reference bundle into the shared tree and start the shared alignment automatically

Why:
- the QC/remediation decision is already settled (`fastp` is the canonical cleaned input)
- the remaining GC WARN issue is being treated as a monitored cohort/batch-style signal, not as a trimming blocker
- rebuilding the same mouse index in two places at the same time adds unnecessary I/O and increases the chance of inconsistent reference state

What does **not** belong in the baseline notebook:
- new experiment-specific outputs
- repeated narrative about raw vs FASTX
- tool-comparison notes that would clutter the original comparison

### Phase 3 — expand to the full flagged set

Expand only after the pilot identifies the best tool.

Expansion set:
- the top-severity SRRs from the baseline ranking
- all SRRs with clear technical overrepresented sequences

Current priority expansion list:
- `SRR30333744`
- `SRR30333745`
- `SRR30333748`
- `SRR30333751`
- `SRR30333752`
- `SRR30333753`
- `SRR30333755`

If `fastp` wins the pilot:
- apply `fastp` to the full flagged set first

If `cutadapt` wins only for explicit-sequence cases:
- keep `cutadapt` restricted to those targeted runs
- do not force it across the whole dataset unless it clearly outperforms `fastp`

## What to measure for each SRR/tool

Primary metrics:
- `Adapter Content` status before vs after
- `adapter_max` before vs after
- `Overrepresented sequences` before vs after
- whether the specific technical sequence (poly-G / TruSeq adapter) drops or disappears

Secondary guardrails:
- reads retained
- median/typical read length after cleanup
- whether trimming creates obvious over-shortening
- whether the new tool is actually better than the current `FASTX`-trimmed baseline, not just better than raw

Do not use as primary decision metrics:
- `Sequence Duplication Levels` alone
- simple severity score alone

Reason:
- duplication is often biology/library-driven in RNA-seq
- trimmed reads naturally add a `Sequence Length Distribution` WARN, which can inflate severity without meaning “worse data”

## How we will decide the winning tool

Choose the tool that:
1. reduces adapter/poly-G signal the most across the pilot SRRs
2. removes or clearly lowers the technical overrepresented sequences
3. preserves reads/length well enough for alignment
4. is easiest to justify and reproduce for the full project

Expected outcome based on current evidence:
- `fastp` is the most likely full-project choice
- `cutadapt` is the strongest targeted comparison / confirmation tool
- `fastx_clipper` is unlikely to be the final batch choice

## Commands to start the pilot

### `fastp`

```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel \
bash Semester5/BIOL550/group_project/pipelines/qc_remed_fastp_one_srr.sh SRR30333754
```

Repeat for:
- `SRR30333756`
- `SRR30333743`

### `cutadapt`

Poly-G focused pilot example:

```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel \
NEXTSEQ_TRIM=20 \
bash Semester5/BIOL550/group_project/pipelines/qc_remed_cutadapt_one_srr.sh SRR30333754
```

Explicit-adapter pilot example:

```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel \
ADAPTER_R1=GATCGGAAGAGCACACGTCTGAACTCCAGTCACATGAGGCCATCTGGGGG \
NEXTSEQ_TRIM=20 \
bash Semester5/BIOL550/group_project/pipelines/qc_remed_cutadapt_one_srr.sh SRR30333743
```

### Home-side batch wrapper used for the controlled pilot

Server wrapper:
- `/home/pzg8794/mouse_qc_remediation/scripts/run_pilot_remediation.sh`

What it runs:
- `fastp` on `SRR30333754`, `SRR30333756`, `SRR30333743`
- `cutadapt` with `NEXTSEQ_TRIM=20` on the poly-G dominated SRRs
- `cutadapt` with explicit `ADAPTER_R1` + `NEXTSEQ_TRIM=20` on `SRR30333743`

Log file:
- `/home/pzg8794/mouse_qc_remediation/logs/run_pilot_remediation.2026-03-09_232002.log`

Last verified live state:
- the `fastp` phase finished for all three pilot SRRs (`SRR30333754`, `SRR30333756`, `SRR30333743`)
- server evidence now includes:
  - `3` `fastp` report pairs (`.html` + `.json`)
  - `12` post-`fastp` FastQC artifacts
  - `6` post-`fastp` FASTQ files
- the pipeline moved into `cutadapt`
- trimming completed for `SRR30333754`, and `FastQC` was running on the new `SRR30333754` `cutadapt` outputs

## Comparison artifacts to generate and keep

Primary comparison script:
- `Semester5/BIOL550/group_project/pipelines/mouse_qc_strategy_compare.py`

Server copy:
- `/home/pzg8794/mouse_qc_remediation/scripts/mouse_qc_strategy_compare.py`

Server runner:
- `/home/pzg8794/mouse_qc_remediation/scripts/run_compare.sh`

Preliminary outputs already generated:
- `/home/pzg8794/mouse_qc_remediation/compare/preliminary/pilot_read_stage_metrics.csv`
- `/home/pzg8794/mouse_qc_remediation/compare/preliminary/pilot_adapter_curve_data.csv`
- `/home/pzg8794/mouse_qc_remediation/compare/preliminary/pilot_srr_comparison_wide.csv`
- `/home/pzg8794/mouse_qc_remediation/compare/preliminary/pilot_fastp_run_metrics.csv`
- `/home/pzg8794/mouse_qc_remediation/compare/preliminary/pilot_cutadapt_run_metrics.csv`
- `/home/pzg8794/mouse_qc_remediation/compare/preliminary/pilot_summary.md`

What the preliminary compare already established:
- current `FASTX` trimming improves read length / tail quality behavior
- current `FASTX` trimming does **not** materially clear the dominant technical signal in the pilot SRRs
- the main unresolved targets remain:
  - poly-G dominated read 2 signal in `SRR30333754` and `SRR30333756`
  - explicit TruSeq adapter signal in `SRR30333743_1`

## Pilot results and current decision

Final comparison package:
- `/home/pzg8794/mouse_qc_remediation/compare/final/pilot_summary.md`
- `/home/pzg8794/mouse_qc_remediation/compare/final/pilot_srr_comparison_wide.csv`
- `/home/pzg8794/mouse_qc_remediation/compare/final/pilot_fastp_run_metrics.csv`
- `/home/pzg8794/mouse_qc_remediation/compare/final/pilot_cutadapt_run_metrics.csv`

Pilot findings:
- `SRR30333754_2` (poly-G dominated read 2)
  - current `FASTX` adapter_max `45.0897`
  - `fastp` adapter_max `0.0589`, retained `95.5758%`
  - `cutadapt` adapter_max `45.0601`, retained `97.5000%`
- `SRR30333756_2` (poly-G dominated read 2)
  - current `FASTX` adapter_max `32.4893`
  - `fastp` adapter_max `0.0434`, retained `95.7836%`
  - `cutadapt` adapter_max `31.8831`, retained `97.7000%`
- `SRR30333743_1` (explicit TruSeq adapter in read 1)
  - current `FASTX` adapter_max `49.1768`
  - `fastp` adapter_max `0.0054`, retained `96.7674%`
  - `cutadapt` adapter_max `0.0338`, retained `98.2000%`

Decision from the pilot:
- choose `fastp` as the default cleanup tool for the mouse project
- keep `cutadapt` as the targeted fallback for explicit adapter/primer-driven cleanup

Why:
- `fastp` was clearly better at collapsing residual adapter/poly-G signal across all three pilot reads
- `cutadapt` retained slightly more reads, but it did not materially reduce adapter_max in the two poly-G dominated pilot cases
- the dominant dataset-wide problem is the poly-G / adapter-like signal, so that criterion matters more than the small retention advantage

## Current local deliverables (authoritative paths)

Use these as the main local references for the remediation work:

- notebook:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
- remediation analysis folder:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/`
- key summary tables:
  - `pilot_srr_comparison_wide.csv`
  - `pilot_read_stage_metrics.csv`
  - `pilot_fastp_run_metrics.csv`
  - `pilot_cutadapt_run_metrics.csv`
  - `pilot_summary.md`
- key final figures:
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

Interpretation rule:
- use the per-stage comparison plots + summary tables to choose the tool
- use the GC bell-shape plots as dataset-level sanity checks, not as the primary decision metric

### Research-backed plot priorities

Best plots now in place:
- overview:
  - `final_problem_raw_vs_fastx.png`
  - `final_fastp_vs_baseline.png`
  - `final_cutadapt_vs_baseline.png`
  - `final_all_tools_comparison.png`
- primary ranking plots:
  - `final_adapter_delta_vs_fastx.png`
  - `final_retention_vs_adapter_tradeoff.png`
  - `final_status_heatmap_focus_reads.png`
- validation plots:
  - GC bell-shape figures + `final_bell_gallery_2x2.png`
- still optional later:
  - theoretical GC overlay using `mm10_txome`
  - final full-dataset MultiQC report for `fastp` after the full rerun

Why these are the right next plots:
- point / slope plots are better than bars for direct category comparison
- box / violin style plots are better than bars when we need to show spread across runs
- heatmaps are the compact way to summarize module-level change across many samples
- GC bell plots should stay, but only as a library-shape sanity check
- MultiQC should come after the notebook-level comparison work, as a final integrated validation report rather than the primary exploration layer

### MultiQC validation status

Reporting language to keep consistent:
- custom comparison workflow = primary validation layer
- custom comparison workflow = automated version of the professor’s manual file-by-file FastQC review
- MultiQC = supplementary aggregation / confirmation layer
- use MultiQC to corroborate and summarize the file-level findings, not as the only basis for interpretation

Done now:
- generated the pilot comparison MultiQC report on `sequoia`:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/pilot_compare/report/mouse_pilot_compare_multiqc.html`
- installed `multiqc` in the user-local server path:
  - `~/.local/bin/multiqc`
- copied the server MultiQC pilot results locally for analysis:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_pilot_compare_server/`
- saved reusable helper scripts:
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_pilot_compare.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_final_fastp.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_fastx_baseline.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_fastx_vs_fastp.sh`
- generated the full-dataset FASTX baseline MultiQC report:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/fastx_baseline_all_srrs/report/mouse_fastx_baseline_all_srrs_multiqc.html`
- generated the full-dataset FASTX vs fastp MultiQC comparison report:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/fastx_vs_fastp_all_srrs/report/mouse_fastx_vs_fastp_all_srrs_multiqc.html`
- copied those server MultiQC results locally for analysis:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_baseline_server/`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_vs_fastp_server/`

Why this is the correct scope:
- `fastp` and `cutadapt` only exist for the pilot SRRs right now
- therefore the right immediate MultiQC report is the pilot comparison report, not a full-dataset all-tools report
- after the full `fastp` rerun completed, a full-dataset `FASTX` baseline report and a `FASTX` vs `fastp` comparison report became valid supporting reports
- these support report-writing and QC interpretation, but they do not replace the custom comparison tables/plots that drive the tool decision

Done now:
- interpreted the full-dataset `FASTX` vs `fastp` differences and folded them into the weekly report narrative

Completed full-dataset comparison output:
- local comparison folder:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/full_fastx_vs_fastp_full/`
- notebook reference section:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
  - see **Step 5C. Bring in the full-dataset validation pass**
- key outputs:
  - `full_fastx_vs_fastp_summary.md`
  - `full_fastx_vs_fastp_read_metrics.csv`
  - `full_fastx_vs_fastp_status_counts.csv`
  - `full_fastx_vs_fastp_status_transitions.csv`
  - `full_fastp_run_metrics.csv`
  - `full_fastx_vs_fastp_adapter_comparison.png`
  - `full_fastx_vs_fastp_retention_tradeoff.png`
  - `full_fastx_vs_fastp_status_counts.png`
- headline findings:
  - `Adapter Content` improved from `52/52 fail` in the FASTX baseline to `52/52 pass` after `fastp`
  - `Overrepresented sequences` improved from `37 pass / 13 warn / 2 fail` to `52/52 pass`
  - median `adapter_max` changed from `31.8806` to `0.0051`
  - median retained reads after `fastp` remained high at `97.52%`

Server cleanup completed:
- deleted the large pilot trimmed FASTQ outputs from:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
  - `/home/pzg8794/mouse_qc_remediation/output/cutadapt/out/`
- deleted the temporary pip cache:
  - `~/.cache/pip`
- kept the small artifacts needed for analysis:
  - FastQC post-tool zips
  - `fastp` JSON reports
  - `cutadapt` logs
  - MultiQC HTML + data folder

Server code policy now in effect:
- keep long custom code local
- copy to server only when needed to run
- delete the server copy after the run
- current practical threshold for “long code”:
  - about `>100` lines

Removed from server and must be recopied before reuse:
- `mouse_qc_strategy_compare.py`
- `download_fastq_sratoolkit.sh`
- `fastx_trim_fastqc_pipeline.sh`
- `run_end_to_end_fastq_fastqc_fastx_fastqc.sh`
- `run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh`
- `sra_runs_pipeline_sra3.sh`
- `sra_runs_pipeline_sra3_parallel.sh`

Local helper for staging/removing those files:
- `Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh`
- default use:
  - `.../sync_long_code_to_sequoia.sh list`
  - `.../sync_long_code_to_sequoia.sh push <script>`
  - `.../sync_long_code_to_sequoia.sh remove <script>`

## Transcript-guided next steps before alignment

Reviewed transcript/summaries used for this checkpoint:
- `Semester5/BIOL550/transcripts/2026-02-18 Lecture_ SRA Toolkit Workflows, FastQC, Server Coordination, and Alignment Deliverables-summary.md`
- `Semester5/BIOL550/transcripts/2026-02-19 Lecture_ Sequencing Data QC Workflow with FastQC and FASTX-Toolkit-summary.md`
- `Semester5/BIOL550/transcripts/2026-02-26 Analysis of RNA-Seq Quality Control and Methodology Verification-summary.md`
- `Semester5/BIOL550/transcripts/2026-03-02 Weekly Meeting_ Bulk RNA-seq Dataset Selection, Access Permissions, and QC (Adapters_Duplication)-summary.md`
- `Semester5/BIOL550/transcripts/2026-03-04 Lecture_ RNA Sequencing Data Analysis and Quality Control-summary.md`
- `Semester5/BIOL550/transcripts/2026-03-05 Lecture_ RNA-seq QC, Reference Selection, and Differential Expression Tools-transcript.txt`

What these transcripts say our next cleaning-to-alignment steps should be:
- finish the **real cleanup pass** with the chosen tool across the dataset, not only on the pilot SRRs
- rerun FastQC after cleanup and use that as the validation layer before alignment
- capture alignment QC from STAR afterward (`unique`, `multi`, `unmapped`) because that is part of the interpretation, not just a technical afterthought
- choose the reference genome carefully:
  - same reference as the paper if we are trying to replicate closely
  - otherwise the most recent, best-annotated, most appropriate mouse reference for the strain/context
- organize the sample-level metadata before alignment so the downstream interpretation is clean

Blocking items before alignment:
- exact mouse reference + annotation pair has not yet been confirmed in the docs
- sample sheet / design matrix and STAR run manifest have not yet been finalized

Current execution status:
- full-dataset `fastp` + post-`fastp` FastQC + final chosen-tool MultiQC were launched on `sequoia` on `2026-03-11 03:26 EDT`
- server wrapper:
  - `/home/pzg8794/mouse_qc_remediation/scripts/mouse_run_full_fastp_alignment_prep.sh`
- server log:
  - `/home/pzg8794/mouse_qc_remediation/logs/run_full_fastp_alignment_prep.2026-03-11_032611.log`
- completion markers reached:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/full_fastp_all_srrs.completed`
  - `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/mouse_fastp_all_srrs_multiqc.completed`

Current completion status:
- full-dataset `fastp` rerun is complete (`26/26` reports)
- post-`fastp` FastQC is complete (`52/52` reports)
- final chosen-tool MultiQC is complete:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/report/mouse_fastp_all_srrs_multiqc.html`

Immediate next analysis step:
- use the finished full-dataset `FASTX` vs `fastp` comparison package in the notebook/report as the evidence layer for the cleanup decision
- move the remaining open items into alignment preparation:
  - confirm the cleaned-input root
  - confirm whether any SRR still needs targeted `cutadapt`
  - confirm the reference + annotation pair
  - finalize the sample/design sheet and STAR manifest

Non-blocking issues (monitor, do not over-fix):
- high duplication by itself in bulk RNA-seq
- expected sequence-length distribution changes after trimming
- minor residual adapter-like signal if it is small after cleanup
- small GC-shape differences that do not suggest a broader systematic problem

Decision for the current report/update:
- present the remediation choice as finished at both the pilot and full-dataset validation levels
- present the remaining work as alignment-prep confirmation items, not unresolved cleanup uncertainty

References:
- MultiQC reports: https://docs.seqera.io/multiqc/reports
- MultiQC custom content: https://docs.seqera.io/multiqc/custom_content
- MultiQC FastQC module: https://docs.seqera.io/multiqc/modules/fastqc
- seaborn `pointplot`: https://seaborn.pydata.org/generated/seaborn.pointplot.html
- seaborn `lineplot`: https://seaborn.pydata.org/generated/seaborn.lineplot.html
- seaborn `heatmap`: https://seaborn.pydata.org/generated/seaborn.heatmap.html
- seaborn error bars tutorial: https://seaborn.pydata.org/tutorial/error_bars.html
- Plotly line charts: https://plotly.com/python/line-charts/
- Plotly heatmaps: https://plotly.com/python/heatmaps/
- Plotly box plots: https://plotly.com/python/box-plots/

### Bell-plot reading guide

- shaded region:
  - `25th` to `75th` percentile spread across the reports in that stage
- bold line:
  - median curve for that stage
- why median:
  - more robust than the mean if a few SRRs are unusual
- trimmed baseline:
  - `Current FASTX` is the trimmed baseline in every remediation bell plot
- what “better than trimmed” means:
  - first check that the tool-specific bell shape stays reasonable relative to the `Current FASTX` line
  - then use the remediation metrics to decide whether the tool is actually better
- final interpretation for this mouse pilot:
  - both `fastp` and `cutadapt` keep an acceptable GC bell shape
  - `fastp` is still better overall because it removes the residual adapter/poly-G signal more effectively

## Documentation requirements

For every tool tested, record:
- what the tool is for
- why it was chosen for this dataset
- exact command / parameters
- which SRRs it was applied to
- what changed in FastQC
- why we kept or rejected it

Files to keep updated:
- `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`
- `Semester5/BIOL550/group_project/mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
- `Semester5/BIOL550/group_project/WORKLOG.md`
- `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`

After every major action, add three things explicitly:
- **step** — the exact command/script/path used
- **finding** — what changed or did not change
- **decision** — what we will do next because of that finding

## Tool references

- `fastp`: https://github.com/OpenGene/fastp
- `cutadapt`: https://cutadapt.readthedocs.io/
- `FASTX Toolkit`: http://hannonlab.cshl.edu/fastx_toolkit/

## 2026-03-17 follow-up — shared MultiQC correction + GC WARN subgroup check

### Step
- Corrected the shared MultiQC output so the trimmed-only shared report uses only `fastqc_fastp_trim`.
- Generated matching before-trimming and after-trimming shared reports.
- Copied the corrected trimmed-only shared report locally.
- Extracted the `Per Sequence GC Content` WARN samples from the trimmed-only MultiQC data.
- Mapped the WARN SRRs against `GSE243308` / `PRJNA1017789` sample metadata.

### Status
- Shared trimmed-only and raw-only reports are complete.
- WARN subset mapping is complete at a quick metadata level.

### Finding
- Post-`fastp` `Per Sequence GC Content` remains `27 PASS / 25 WARN / 0 FAIL`.
- The WARN entries cluster mainly in `SRR30333757` through `SRR30333768` plus `SRR30333756_1`.
- That subset maps to a real cohort within the study, but not to one simple biological condition: it spans control and conditional knockout, and spans naive/control DRG and injury DRG groups.
- This makes the remaining GC WARN pattern look more like a cohort / hidden-batch / study-subset effect than a simple sick-vs-control problem.

### Decision
- Do not remove samples or trim further based on the GC curve alone.
- Proceed to alignment with the `fastp` outputs and use alignment metrics as the next decision layer.
- If the GC-WARN subset also underperforms at alignment, then revisit exclusion/subsetting with stronger evidence.

### Reference
- `Semester5/BIOL550/group_project/mouse/GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md`

## 2026-03-17 follow-up — STAR alignment start on local server

### Step
- Locked the alignment preconditions explicitly before launching STAR:
  - `GRCm39` + matching `Ensembl` `GTF`
  - cleaned inputs from `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
  - one shared STAR index under `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/star_index_sjdb150/`
  - first-pass alignment scope = all `26` SRRs
- Added server-targeted STAR scripts locally:
  - `mouse_star_prepare_reference.sh`
  - `mouse_star_align_one_srr.sh`
  - `mouse_star_align_batch.sh`
  - `mouse_run_star_all26_fastp_parallel.sh`
- Added a dedicated note documenting the full reasoning chain into alignment start.

### Status
- Local scripts and alignment-start note are in place.
- Server sync is complete.
- The `all 26` STAR launcher has started on `sequoia`.

### Finding
- The QC remediation phase is already strong enough to justify using alignment as the next decision layer.
- The remaining GC WARN issue is documented as non-random but not clearly attributable to one simple biological condition.
- That makes alignment metrics more informative than more trimming.
- The resolved Ensembl reference files at launch time were:
  - `Mus_musculus.GRCm39.dna.primary_assembly.fa.gz`
  - `Mus_musculus.GRCm39.115.gtf.gz`
- The launcher log path is:
  - `/home/pzg8794/mouse_qc_remediation/logs/run_star_all26_fastp_parallel.2026-03-17_233805.log`
- The current output root is:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`
- The first launcher attempt exposed a STAR input requirement:
  - STAR rejects compressed FASTA input for `genomeGenerate`
  - the reference-prep script was corrected to unzip the FASTA and GTF before index generation
  - the launcher was restarted after that fix

### Decision
- Keep this all-26 STAR run as the first-pass alignment run.
- Compare GC-WARN vs GC-PASS only after STAR metrics exist.

### Reference
- `Semester5/BIOL550/group_project/mouse/ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md`
