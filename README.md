# BIOL550 Group Project Workspace

This repo contains the **group project workspace** (dataset metadata, scripts, notes) for BIOL550.

LaTeX report sources/build outputs have been removed from this repo and will live in a **separate LaTeX repo** (which can be nested here later as a submodule if desired).

## Documentation hierarchy

- Parent course hub: [../README.md](../README.md)
- Course notes: [../BIOL550-Notes.md](../BIOL550-Notes.md)
- Lab task hub: [../BIOL550-Lab/task_n_desc.md](../BIOL550-Lab/task_n_desc.md)
- Group project documentation map: [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)
- Agent start guide: [START_HERE_AGENT.md](START_HERE_AGENT.md)
- Server minimum policy: [SERVER_MINIMUM_POLICY.md](SERVER_MINIMUM_POLICY.md)
- Group project outline: [BIOL550_group_project_outline.md](BIOL550_group_project_outline.md)
- Deep research / presentation report: [deep-research-report.md](deep-research-report.md)
- Work log: [WORKLOG.md](WORKLOG.md)
- Mouse process doc: [mouse/PROCESS_mouse_fastq_fastqc_fastx.md](mouse/PROCESS_mouse_fastq_fastqc_fastx.md)
- Mouse TODO: [mouse/TODO_mouse.md](mouse/TODO_mouse.md)
- Mouse remediation plan: [mouse/TODO_qc_remediation.md](mouse/TODO_qc_remediation.md)

Use this file as the group-project entry point, then move down the hierarchy into the mouse workflow docs.

If a future Codex session starts here, it should read [START_HERE_AGENT.md](START_HERE_AGENT.md) before making changes.

## Important server note

**The server must keep the minimum needed for execution and proof of work.  
Most code, notebooks, and custom analysis logic must stay local.**

Operational meaning:
- keep long code local
- copy long code to the server only when needed
- run it
- delete the server copy after the outputs are verified
- keep only short wrappers, required inputs, logs, and final outputs on the server

See [SERVER_MINIMUM_POLICY.md](SERVER_MINIMUM_POLICY.md) before copying code to `sequoia`.

## Structure
- `pipelines/`: Reusable scripts + templates (dataset-agnostic)
- `mouse/`: Dataset-scoped workflow notes for the current mouse dataset
- `_tmp_zebrafish_2026-03-02/`: Archived zebrafish workspace + QC bundles (safe to delete later)
- `project_datasets/`: RunInfo CSVs and run lists used during dataset selection/validation
- `starter_pipeline/`: Starter pipeline scripts/configs (older)

## Current status (dataset pivot)
- We used the zebrafish workspace to build and test the repeatable pipeline (download → FastQC → **FASTX** trim → FastQC), then archived it to keep the repo clean.

> Tooling note (2026-03-05): for “targeted trimming” (adapter remnants / known end sequences) on paired-end reads, prefer `fastp` over FASTX; for primer/amplicon trimming, use `cutadapt`. See `Semester5/BIOL550/BIOL550-Notes.md` (“fastp vs FASTX Toolkit”) for commands.

- **Update (2026-03-02):** we are now repeating the same workflow on the **mouse dataset** and keeping mouse outputs separate from zebrafish artifacts.
- Work log: `Semester5/BIOL550/group_project/WORKLOG.md`

## Usage
See the per-project README(s), e.g.:

- `mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
- Notebook template (raw vs trimmed comparison): `Semester5/BIOL550/group_project/pipelines/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed.ipynb`

## Organization Tips
- Keep downloaded sequencing data out of Git (use dataset-scoped folders like `mouse/` + server-side shared directories).
- Prefer scripts + metadata that can reproduce the download/validation steps.

---

_Please keep this repo organized and avoid committing large binary outputs._
