# BIOL550 Group Project Documentation Map

This file is the navigation hub for the active BIOL550 group-project documentation. Use it to move from course-level requirements to project-level execution, then to mouse-specific workflow and remediation details.

## Documentation hierarchy

### Level 1 — Course hubs

- [BIOL550 root README](../README.md)
  - top-level course folder overview
  - entry point to notes, lab tasks, and group-project docs
- [BIOL550 notes](../BIOL550-Notes.md)
  - course notes, current status, tool notes, and high-level project links
- [Lab task hub](../BIOL550-Lab/task_n_desc.md)
  - assignment requirements, weekly report requirements, dataset-validation notes, and historical lab instructions

### Level 2 — Group project hubs

- [Group project README](README.md)
  - workspace structure and current project status
- [Agent start guide](START_HERE_AGENT.md)
  - read-first handoff file for future Codex sessions
- [Server minimum policy](SERVER_MINIMUM_POLICY.md)
  - what stays local, what stays on the server, and why
- [Group project outline](BIOL550_group_project_outline.md)
  - original team plan, roles, phases, and project framing
- [Deep research / presentation report](deep-research-report.md)
  - presentation-style project narrative and high-level execution summary
- [Work log](WORKLOG.md)
  - dated record of steps taken, findings observed, and decisions made

### Level 3 — Active mouse workflow

- [Mouse process doc](mouse/PROCESS_mouse_fastq_fastqc_fastx.md)
  - step-by-step operational workflow
  - server paths, commands, monitoring, and terminal-first remediation flow
- [Mouse TODO](mouse/TODO_mouse.md)
  - active task tracker for the mouse project
- [Mouse remediation plan](mouse/TODO_qc_remediation.md)
  - focused plan for QC remediation experiments and tool selection
- [Mouse full-status share doc](mouse/MOUSE_GROUP_STATUS_FULL.md)
  - complete team-facing snapshot of what was done, what files matter, and what is still open
- [Mouse simple follow guide](mouse/MOUSE_GROUP_FOLLOW_GUIDE.md)
  - dummified version of the current mouse project for team follow-along
- [Mouse shared alignment follow guide](mouse/ALIGNMENT_SHARED_TEAM_FOLLOW_GUIDE.md)
  - dummified alignment-specific guide for the shared server tree
- [Mouse alignment execution summary + index](mouse/ALIGNMENT_EXECUTION_SUMMARY_AND_INDEX.md)
  - one-document alignment summary with references to the detailed notes and scripts
- [Shared vs private fastp-trim audit](mouse/SHARED_VS_PRIVATE_FASTP_TRIM_AUDIT_2026-03-18.md)
  - documented comparison of the shared trimmed MultiQC against the private canonical trimmed MultiQC
- [Canonical `full_fastp` shared handoff](mouse/CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md)
  - exact shared paths for the canonical MultiQC and alignment copies, plus the rationale for using them
- [GC WARN + shared MultiQC follow-up note](mouse/GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md)
  - dated decision note covering the shared trimmed-only MultiQC rerun, GC WARN metadata check, and alignment recommendation
- [Mouse alignment analysis notebook note](mouse/ALIGNMENT_ANALYSIS_NOTEBOOK_2026-03-19.md)
  - alignment-stage note covering the local all-26 STAR notebook, exported tables/figures, and the first-pass interpretation
- [Mouse differential expression notebook note](mouse/DIFFERENTIAL_EXPRESSION_NOTEBOOK_2026-03-19.md)
  - DESeq2-stage note covering the all-26 count handoff, family-specific model design, exported contrasts, and first-pass interpretation
- [Mouse DESeq2 shared-server setup note](mouse/DESEQ2_SHARED_SERVER_SETUP_2026-03-20.md)
- [Mouse DESeq2 environment explainer](mouse/DESEQ2_ENVIRONMENT_EXPLAINER_2026-03-20.md)
  - private team-only DESeq2 environment on `sequoia`, runtime issue/fix, wrapper lifecycle, and shared input/output path setup

### Level 4 — Evidence and outputs

- `mouse/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse.ipynb`
  - baseline raw-vs-FASTX QC exploration
- `mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
  - presentation layer for remediation comparisons after terminal outputs exist
- `mouse/notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`
  - simplified team-follow copy of the remediation notebook
- `mouse/notebooks/mouse_alignment_analysis_star_all26.ipynb`
  - alignment-stage notebook for the canonical all-26 STAR run
- `mouse/notebooks/mouse_differential_expression_all26.ipynb`
  - DESeq2 notebook for the family-specific all-26 mouse count analysis
- `pipelines/mouse_deseq2_shared_server_run.sh`
- `pipelines/mouse_deseq2_activate_shared.sh`
  - short shared-server wrapper that checks the private team DESeq2 environment and launches the DE driver against shared inputs
- `mouse/qc_analysis_raw_vs_trimmed/`
  - baseline comparison tables and plots
- `mouse/alignment_analysis_star_all26/`
  - alignment summary tables, reverse-stranded count handoff matrix, and figures derived from the canonical STAR outputs
- `mouse/differential_expression_all26/`
  - family-level DESeq2 outputs, QC figures, contrast tables, and result manifests for the mouse dataset
- `mouse/reports/BIOL550_Weekly_Report_Mouse_SRA_FastQC_2026-03-04.html`
  - weekly report artifact built from the current mouse QC phase

## How to use this map

- Start at the course hubs if you need requirements, context, or grading constraints.
- Move to the group-project hubs if you need team-level planning, history, or decisions.
- If you are a future agent session, read `START_HERE_AGENT.md` first.
- Read the server policy before copying code to `sequoia`.
- Move to the active mouse workflow docs if you need exact commands, current tasks, or remediation logic.
- Move to the evidence and outputs only after you know which workflow step or decision they support.

## Documentation rule for future updates

Every active documentation file should point to:
- this map
- its parent document in the hierarchy
- the most relevant sibling or child documents

When we update the project, record three things in the relevant doc:
- **step** — what was run or changed
- **finding** — what the result was
- **decision** — what follows from that result
