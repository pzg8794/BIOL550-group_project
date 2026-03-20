# Mouse project — TODO (PRJNA1017789 / GSE243308)

Keep this list current. Weekly report task must remain last.

## Documentation links

- Parent mouse workflow: [PROCESS_mouse_fastq_fastqc_fastx.md](PROCESS_mouse_fastq_fastqc_fastx.md)
- Mouse remediation plan: [TODO_qc_remediation.md](TODO_qc_remediation.md)
- Team-share draft for next alignment decisions: [ALIGNMENT_PREP_TEAM_DRAFT.md](ALIGNMENT_PREP_TEAM_DRAFT.md)
- Group project documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)
- Group project work log: [../WORKLOG.md](../WORKLOG.md)
- Course notes: [../../BIOL550-Notes.md](../../BIOL550-Notes.md)
- Lab task hub: [../../BIOL550-Lab/task_n_desc.md](../../BIOL550-Lab/task_n_desc.md)
- Shared alignment follow guide: [ALIGNMENT_SHARED_TEAM_FOLLOW_GUIDE.md](ALIGNMENT_SHARED_TEAM_FOLLOW_GUIDE.md)
- Shared vs private trim audit: [SHARED_VS_PRIVATE_FASTP_TRIM_AUDIT_2026-03-18.md](SHARED_VS_PRIVATE_FASTP_TRIM_AUDIT_2026-03-18.md)
- Canonical shared `full_fastp` handoff: [CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md](CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md)

Use this file for the active task checklist. Record dated outcomes in the work log and detailed remediation logic in the remediation plan.

Local Python/Jupyter work should use:
- `/Users/pitergarcia/DataScience/Semester5/BIOL550/biol550_env`

## Pipeline + data
- [x] Confirm pipeline completion markers on server (`fastx.completed`, `end_to_end.completed`).
- [x] Verify final server counts: raw FASTQs + raw FastQC + trimmed FASTQs + trimmed FastQC are all **26/26**.
- [x] Cleanup temp/stale files (confirm no `*.tmp.*` left in `fastx_out/`).

## Local bundles (copy from Sequoia → Mac)
- [x] Copy **raw FastQC** bundle (ZIP + HTML) to `Semester5/BIOL550/group_project/mouse/qc_bundle_raw/` (52 ZIP + 52 HTML).
- [x] Copy **trimmed FastQC** bundle (ZIP + HTML) to `Semester5/BIOL550/group_project/mouse/qc_bundle_trimmed/` (52 ZIP + 52 HTML).
- [x] Re-check local counts (expect 52 ZIP + 52 HTML per stage for 26 paired-end runs).

## QC analysis (notebook + outputs)
- [x] Create mouse notebook (modeled after zebrafish notebook): raw FastQC summary (tables + plots + interpretation).
- [x] Add trimmed FastQC summary (same outputs + interpretation) — runs on whatever trimmed data is currently available.
  - [x] Add raw vs trimmed comparison section:
  - [x] module-level counts deltas (pass/warn/fail)
  - [x] run-level severity deltas (improved vs unchanged vs worse)
  - [x] identify outliers + propose next cleanup tasks
  - [x] Re-run notebook after full trimmed bundle copy (26/26) to refresh plots + exports.
  - [x] Convert the cleanup idea into a documented experiment plan: `Semester5/BIOL550/group_project/mouse/TODO_qc_remediation.md`
  - [x] Create a separate remediation notebook scaffold so the baseline notebook stays clean: `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
  - [x] Audit the shared server tree and confirm which parts are trustworthy for remediation (`sra_runs` + `fastqc_out` yes; shared derived outputs no).
  - [x] Freeze a trusted home-side remediation baseline in `/home/pzg8794/mouse_qc_remediation/baseline/`.
  - [x] Add the terminal comparison workflow: `Semester5/BIOL550/group_project/pipelines/mouse_qc_strategy_compare.py`.
  - [x] Generate the preliminary `raw` vs current `FASTX` comparison in `/home/pzg8794/mouse_qc_remediation/compare/preliminary/`.
  - [x] Finish the controlled pilot remediation set (`SRR30333754`, `SRR30333756`, `SRR30333743`) with `fastp`.
  - [x] Finish the controlled pilot remediation set with `cutadapt` (`NEXTSEQ_TRIM` and explicit adapter where applicable).
  - [x] Run `/home/pzg8794/mouse_qc_remediation/scripts/run_compare.sh` after all pilot outputs exist.
  - [x] Copy or sync the final comparison outputs into the local comparison workspace.
  - [x] Update the remediation notebook so it displays the terminal-generated comparison artifacts.
  - [x] Choose the cleanup tool for alignment input and record the rationale in the work log.

## Next steps before alignment (transcript-guided)
- [x] Run the chosen cleanup tool (`fastp`) across **all 26 SRRs** to generate the real alignment inputs.
  - Completed on `2026-03-11 10:42 EDT`.
  - Server log: `/home/pzg8794/mouse_qc_remediation/logs/run_full_fastp_alignment_prep.2026-03-11_032611.log`
- [x] Run **post-fastp FastQC** for all cleaned files and keep that bundle separate from the current FASTX baseline.
  - Completed as part of the same full-run wrapper.
- [x] Generate the **final cleaned-input MultiQC** report after the full fastp rerun (use the chosen-tool report, not another all-tools pilot report).
  - Completed as part of the same full-run wrapper.
  - Report: `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/report/mouse_fastp_all_srrs_multiqc.html`
- [x] Compare the full-dataset `fastp` post-QC outputs against the current FASTX-trimmed baseline and write the report-ready findings.
  - Local output folder:
    - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/full_fastx_vs_fastp_full/`
  - Report-ready summary:
    - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_summary.md`
  - Headline result:
    - `Adapter Content` changed from `52/52 fail` under FASTX to `52/52 pass` after full-dataset `fastp`.
    - No read reports remain in `fail` for `Adapter Content` or `Overrepresented sequences` after `fastp`.
- [ ] Freeze the final cleaned FASTQ location + naming convention that STAR will read from.
  - Draft/team-share version prepared:
    - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_PREP_TEAM_DRAFT.md`
  - Notebook discussion preview added:
    - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
    - see **Step 6. Alignment-prep discussion draft**
- [ ] Decide whether any sample still needs a **targeted `cutadapt` fallback** after the full fastp rerun; do not assume the pilot fully settles every SRR.
  - Draft/team-share version prepared:
    - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_PREP_TEAM_DRAFT.md`
  - Notebook discussion preview added:
    - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
    - see **Step 6. Alignment-prep discussion draft**
- [ ] Select the exact **mouse reference genome + annotation pair** for alignment and document why that pair was chosen.
  - If we are replicating the paper closely, prefer the same reference they used.
  - If we are not replicating exactly, prefer the most recent well-annotated mouse reference that matches the strain/experimental context as closely as possible.
  - If more than one mouse reference is plausible, compare:
    - strain match to the experiment
    - annotation completeness
    - assembly completeness / BUSCO-style completeness evidence when available
- [ ] Build the **sample sheet / design matrix** for alignment and downstream DE:
  - `SRR`
  - condition / group
  - replicate
  - mate 1 path
  - mate 2 path
- [ ] Prepare the **STAR run manifest** and the post-alignment summary table template.
  - Required STAR QC fields to capture: uniquely mapped, multi-mapped, unmapped / too many loci, unmapped / too short.
  - If alignment is unexpectedly weak, revisit QC and sample assignment before assuming the reference or mapper is the only problem.
- [ ] Mark which QC findings are **non-blocking** for alignment so we do not waste time trying to “fix” expected RNA-seq behavior.
  - Duplication by itself is not a blocker.
  - Variable length after trimming is expected.
  - Minor residual signal at very low levels should be monitored, not treated as an automatic stop.
  - Notebook discussion preview added:
    - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
    - see **Step 6. Alignment-prep discussion draft**

## Organization + cleanup
- [x] Update `PROCESS_mouse_fastq_fastqc_fastx.md` with final server paths, the parallel runner command, and the home-side remediation workflow.
- [x] Update `BIOL550-Notes.md` and `task_n_desc.md` with final completion snapshot + final paths.
- [x] Remove shared-directory symlink; keep one dataset root: `/home/zebrafish/mouse/PRJNA1017789_parallel/`.
- [x] Add a local helper for staging/removing long code on `sequoia`: `Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh`

## 2026-03-17 — shared MultiQC + GC subset follow-up
- [x] Re-run the shared MultiQC reports as stage-specific outputs on `sequoia`:
  - before trimming only: `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/before_trimming_only/mouse_before_trimming_only_multiqc.html`
  - after trimming only: `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/fastp_trim_only/mouse_fastp_trim_only_multiqc.html`
- [x] Copy the corrected shared trimmed-only MultiQC report locally:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/`
- [x] Check whether the post-`fastp` `Per Sequence GC Content` WARN subset maps to one biological group.
  - Finding: the WARN subset clusters in a real study subset, but not in one simple biological condition.
  - Decision note: `Semester5/BIOL550/group_project/mouse/GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md`
- [x] Use STAR alignment metrics to compare the GC-WARN subset vs the GC-PASS subset before considering removal/subsetting.
  - Notebook:
    - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_alignment_analysis_star_all26.ipynb`
  - Output folder:
    - `Semester5/BIOL550/group_project/mouse/alignment_analysis_star_all26/`
  - Decision note:
    - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_ANALYSIS_NOTEBOOK_2026-03-19.md`

## 2026-03-17 — alignment start on local server (`sequoia`)
- [x] Lock the pre-alignment decision set explicitly:
  - `GRCm39` + matching `Ensembl` `GTF`
  - cleaned-input root = `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
  - shared STAR index under `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/star_index_sjdb150/`
  - run `all 26` first, then subset later if needed
- [x] Create local STAR pipeline sources for the server-side run:
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_prepare_reference.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_parallel.sh`
- [x] Create a dedicated alignment-start note that records how we got here and why this alignment launch is justified:
  - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md`
- [ ] Sync the STAR scripts + run lists to `/home/pzg8794/mouse_qc_remediation/` on `sequoia`.
- [x] Sync the STAR scripts + run lists to `/home/pzg8794/mouse_qc_remediation/` on `sequoia`.
- [x] Start the `all 26` STAR run in the local server-side workspace.
- [x] Record the launcher log path, PID(s), and output root after the run starts.
  - active launcher PID: `71166`
  - launcher log: `/home/pzg8794/mouse_qc_remediation/logs/run_star_all26_fastp_parallel.2026-03-17_233805.log`
  - output root: `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`
  - note: the first launcher attempt failed because STAR requires an uncompressed FASTA; the reference-prep script was fixed and the run was restarted.

## 2026-03-18 — shared follow-on alignment setup (`sequoia`)
- [x] Create a shared-directory follow-on note that records why the shared run is chained behind the private run:
  - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md`
- [x] Create a dummified shared alignment follow guide for teammates:
  - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_SHARED_TEAM_FOLLOW_GUIDE.md`
- [x] Create shared-run STAR wrappers:
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr_shared.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch_shared.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_shared_after_private.sh`
- [x] Sync the shared-run STAR wrappers + run lists into the shared tree:
  - scripts: `/home/zebrafish/mouse/PRJNA1017789_parallel/scripts/`
  - run lists: `/home/zebrafish/mouse/PRJNA1017789_parallel/runs/`
- [x] Start the shared waiting launcher so the shared alignment begins automatically after the private run finishes.
  - active waiting PID (first launch): `72403`
  - first waiting log: `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/run_star_all26_fastp_shared_after_private.2026-03-18_020015.log`
  - handoff issue found after private completion: `rsync` is not installed on `sequoia`
  - fix applied: shared launcher now falls back to `cp -a` when `rsync` is unavailable
  - thread/load adjustment requested afterward: switch shared alignment to serial one-sample-at-a-time execution with `STAR_THREADS=1`
  - current shared launcher PID: `77729`
  - current shared launcher log: `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/run_star_all26_fastp_shared_after_private.2026-03-18_110908.log`
- [x] Decide whether to build a second shared index immediately.
  - Decision: **no immediate shared rebuild**
  - Rationale: reuse the finished private `GRCm39` + `Ensembl` STAR index after the private run completes, then launch the shared alignment from that synced reference bundle.

## 2026-03-18 — canonical `full_fastp` copy into the shared tree
- [x] Copy the canonical `full_fastp` MultiQC into the shared tree with a clearly distinguishable name.
  - shared canonical MultiQC:
    - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/full_fastp_canonical_privatecopy/`
- [x] Start copying the canonical `full_fastp` all-26 alignment into the shared tree with a clearly distinguishable name.
  - shared canonical alignment:
    - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_full_fastp_canonical_privatecopy/`
  - note:
    - the copy can take longer because it includes BAM outputs
- [x] Add a handoff note that explains why the canonical shared-side copy exists and which paths the team should use.
  - `Semester5/BIOL550/group_project/mouse/CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md`
- [x] Record the process lesson explicitly.
  - independent verification of shared derived outputs is required before treating them as canonical

## 2026-03-19 — local canonical alignment copy + alignment notebook
- [x] Create the local alignment-analysis notebook for the canonical all-26 STAR run.
  - notebook:
    - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_alignment_analysis_star_all26.ipynb`
  - outputs:
    - `Semester5/BIOL550/group_project/mouse/alignment_analysis_star_all26/`
- [x] Build the first full sample-level alignment summary from `Log.final.out` + `ReadsPerGene.out.tab`.
  - exported tables include:
    - `mouse_alignment_sample_summary.tsv`
    - `mouse_star_gene_counts_reverse_stranded.tsv`
    - `alignment_metric_by_platform_median.tsv`
    - `alignment_metric_by_gc_status_median.tsv`
- [ ] Finish the local BAM / BAI sync from `sequoia` into:
  - `Semester5/BIOL550/group_project/mouse/alignment_local_server_private_copy/star_grcm39_ensembl_all26_fastp/`
  - note:
    - the STAR log/count analysis is complete locally
    - BAM transfer is large and continues separately from the notebook work

## 2026-03-19 — differential expression notebook and DESeq2 export package
- [x] Create and execute the local DE notebook for the all-26 STAR count handoff.
  - notebook:
    - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_differential_expression_all26.ipynb`
  - driver script:
    - `Semester5/BIOL550/group_project/pipelines/mouse_deseq2_all26.R`
- [x] Build the cleaned DE design table and family/contrast manifests.
  - exported tables include:
    - `mouse_de_design_table.tsv`
    - `family_manifest.tsv`
    - `contrast_manifest.tsv`
- [x] Run all valid family-specific DESeq2 contrasts instead of one confounded global model.
  - families:
    - tissue / `NovaSeq 6000` / naive vs injury
    - tissue / `NovaSeq X` / ipsilateral vs contralateral sham
    - neurons / `NovaSeq X`
  - total contrasts exported:
    - `11`
- [x] Generate DE QC figures and per-contrast result packages under:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/`
- [x] Record the DE notebook interpretation and handoff note:
  - `Semester5/BIOL550/group_project/mouse/DIFFERENTIAL_EXPRESSION_NOTEBOOK_2026-03-19.md`

## 2026-03-20 — private team DESeq2 server environment
- [x] Create a private team-only DESeq2 environment on `sequoia` without changing the server’s global R stack.
  - env path:
    - `/home/pzg8794/.local/share/micromamba/envs/biol550_deseq2`
- [x] Record the runtime issue and the fix.
  - issue:
    - `/usr/local/bin/R` failed because `libreadline.so.7` was missing
  - fix:
    - private micromamba environment with `R 4.3.3` + `DESeq2`
- [x] Add a short shared-server wrapper for team execution.
  - local canonical wrapper:
    - `Semester5/BIOL550/group_project/pipelines/mouse_deseq2_shared_server_run.sh`
  - server wrapper target:
    - `/home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_shared_server_run.sh`
- [x] Copy the count matrix and alignment sample summary into a shared DE input directory on `sequoia`.
  - shared input root:
    - `/home/zebrafish/mouse/PRJNA1017789_parallel/deseq2_shared/inputs/`
- [x] Verify that the wrapper can see the environment and the shared input files.
  - wrapper check status:
    - `CHECK_OK`

## Current local deliverables

- Remediation notebook:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
- Team-follow remediation notebook copy:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`
- Alignment notebook:
  - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_alignment_analysis_star_all26.ipynb`
- Differential expression notebook:
  - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_differential_expression_all26.ipynb`
- Remediation artifact folder:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/`
- Alignment analysis artifact folder:
  - `Semester5/BIOL550/group_project/mouse/alignment_analysis_star_all26/`
- Differential expression artifact folder:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/`
- Team full-status handoff doc:
  - `Semester5/BIOL550/group_project/mouse/MOUSE_GROUP_STATUS_FULL.md`
- Team simple follow guide:
  - `Semester5/BIOL550/group_project/mouse/MOUSE_GROUP_FOLLOW_GUIDE.md`
- Full-dataset FASTX vs fastp comparison:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/full_fastx_vs_fastp_full/`
- Supplemental MultiQC local copies:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_baseline_server/`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_vs_fastp_server/`
- Canonical decision:
  - `fastp` = default cleanup tool
  - `cutadapt` = targeted fallback

## Deliverables (collected)
- [x] Keep weekly report HTML/PDF copies together in `Semester5/BIOL550/weekly_reports/_collected/` (with `manifest.csv`) for side-by-side review.

## Weekly report (last)
- [x] Update the weekly report with the final tool-choice rationale.
- [x] Add the transcript-guided **pre-alignment plan** to the report for tomorrow:
  - full fastp rerun
  - full post-fastp QC / MultiQC validation
  - reference + annotation selection
  - sample sheet + STAR alignment metrics capture
- [x] Create a new weekly report draft that reuses the previous formatting but updates the content to the remediation + full-dataset validation phase:
  - `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`
- [x] Draft weekly report paragraph-style using the final raw-vs-trimmed QC comparison insights + next steps (`mouse/reports/BIOL550_Weekly_Report_Mouse_SRA_FastQC_2026-03-04.html`).
- [x] Polish report wording/layout (MultiQC note + figure sizing tweaks).
