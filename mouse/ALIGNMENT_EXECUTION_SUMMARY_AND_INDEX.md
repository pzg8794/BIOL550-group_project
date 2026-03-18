# Mouse alignment execution summary + detail index

Purpose:
- give one concise document that explains how the alignment was set up
- show the current execution structure
- point to the exact files for deeper detail

## One-paragraph summary

We moved into alignment after the QC remediation phase established `fastp` as the cleaned input stage for the mouse dataset. We locked the reference decision first (`GRCm39` + matching `Ensembl` `GTF`), then built the `STAR` index in the private server-side workspace under `/home/pzg8794/mouse_qc_remediation/`, and launched the first full `all 26` alignment there using the same parallel split logic that worked for SRR download. After that, we set up the shared tree under `/home/zebrafish/mouse/PRJNA1017789_parallel/` to run the same alignment automatically after the private run finished, using a shared-side copy of the finished reference/index bundle so the team has its own readable version.

## Alignment decisions that were locked before launch

- cleaned inputs: `fastp` outputs
- reference assembly: `GRCm39`
- annotation source: matching `Ensembl` `GTF`
- first-pass scope: align all `26` SRRs first
- execution pattern: one shared `STAR` index + three parallel batch splits

## Execution layout

### Private canonical run
- workspace:
  - `/home/pzg8794/mouse_qc_remediation/`
- cleaned inputs:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
- reference root:
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/`
- STAR index:
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/star_index_sjdb150/`
- alignment root:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`

### Shared follow-on run
- workspace:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/`
- cleaned inputs:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/fastp_out/`
- shared reference root:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/reference/grcm39_ensembl/`
- shared alignment root:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_fastp/`

### Shared canonical copies for team use
- canonical MultiQC copy:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/full_fastp_canonical_privatecopy/`
- canonical alignment copy:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_full_fastp_canonical_privatecopy/`

## Why private first, then shared

- one correct index build is cheaper than two simultaneous builds
- the private run served as the canonical first launch
- the shared tree still gets its own readable copy of:
  - FASTA
  - GTF
  - STAR index
  - manifest / metadata
- this gives the team a usable shared version without making the first launch slower

## Parallel approach used

We reused the same practical idea that worked for parallel SRR download:
- keep one shared reference/index
- split the SRRs into three member-style files
- run one sequential alignment batch per split
- let the three batches run in parallel

Split files:
- `PRJNA1017789_runs.member.nikhi.txt`
- `PRJNA1017789_runs.member.piter.txt`
- `PRJNA1017789_runs.member.samuel.txt`

## Important execution notes

- the first private launch exposed a real issue:
  - `STAR genomeGenerate` does not accept a compressed FASTA
- that was fixed by changing the reference-prep script to unzip the FASTA and GTF before index generation
- the first shared handoff exposed a second issue:
  - `rsync` was not installed on `sequoia`
- that was fixed by adding a `cp -a` fallback in the shared handoff script

## Note on the remaining GC shift

The remaining `Per Sequence GC Content` shift does not map cleanly to one biological condition. It clusters more like a cohort/batch-style subset, and one plausible contributor is the sequencing-platform boundary in the run metadata (`Illumina NovaSeq 6000` vs `NovaSeq X`). That is a reasonable explanation for part of the MultiQC shift, but it is not proven to be the only cause from QC/metadata alone.

## What to read if someone asks “how did you do alignment?”

### Best single narrative
- [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md`](ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md)

### Shared-side handoff design
- [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md`](ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md)

### Canonical shared-side copy
- [`Semester5/BIOL550/group_project/mouse/CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md`](CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md)

### Team-simple version
- [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_SHARED_TEAM_FOLLOW_GUIDE.md`](ALIGNMENT_SHARED_TEAM_FOLLOW_GUIDE.md)

## Detailed reference index

### Decision and justification docs
- alignment start note:
  - [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md`](ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md)
- shared follow-on setup:
  - [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md`](ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md)
- canonical shared handoff:
  - [`Semester5/BIOL550/group_project/mouse/CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md`](CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md)
- GC WARN / metadata follow-up:
  - [`Semester5/BIOL550/group_project/mouse/GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md`](GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md)
- project task tracker:
  - [`Semester5/BIOL550/group_project/mouse/TODO_mouse.md`](TODO_mouse.md)
- remediation + handoff reasoning:
  - [`Semester5/BIOL550/group_project/mouse/TODO_qc_remediation.md`](TODO_qc_remediation.md)
- dated execution log:
  - [`Semester5/BIOL550/group_project/WORKLOG.md`](../WORKLOG.md)

### Pipeline scripts
- reference prep / STAR index:
  - [`Semester5/BIOL550/group_project/pipelines/mouse_star_prepare_reference.sh`](../pipelines/mouse_star_prepare_reference.sh)
- per-sample STAR runner:
  - [`Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr.sh`](../pipelines/mouse_star_align_one_srr.sh)
- private batch runner:
  - [`Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch.sh`](../pipelines/mouse_star_align_batch.sh)
- private orchestrator:
  - [`Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_parallel.sh`](../pipelines/mouse_run_star_all26_fastp_parallel.sh)
- shared per-sample runner:
  - [`Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr_shared.sh`](../pipelines/mouse_star_align_one_srr_shared.sh)
- shared batch runner:
  - [`Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch_shared.sh`](../pipelines/mouse_star_align_batch_shared.sh)
- shared chained launcher:
  - [`Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_shared_after_private.sh`](../pipelines/mouse_run_star_all26_fastp_shared_after_private.sh)

### Evidence that led to alignment
- weekly report:
  - [`Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`](reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html)
- remediation notebook:
  - [`Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`](notebooks/qc_remediation_experiments_mouse.ipynb)
- team-follow notebook:
  - [`Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`](notebooks/qc_remediation_experiments_mouse_team_follow.ipynb)
- full FASTX-vs-`fastp` comparison outputs:
  - [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/full_fastx_vs_fastp_full/`](qc_analysis_remediation/full_fastx_vs_fastp_full/)
- shared trimmed-only MultiQC copy:
  - [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/`](qc_analysis_remediation/multiqc_fastp_trim_only_shared/)

## Short explanation to reuse

We first resolved QC remediation and selected `fastp` as the cleaned input stage. Before alignment, we locked the reference pair (`GRCm39` + matching `Ensembl` `GTF`), the cleaned input root, and the parallel execution plan. We then built the `STAR` index once in the private server-side workspace, ran the first full `all 26` alignment there, and set up the shared tree to start the same alignment automatically afterward using its own shared copy of the finished reference/index bundle.
