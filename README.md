# BIOL550 Group Project Workspace

This repo contains the **group project workspace** (dataset metadata, scripts, notes) for BIOL550.

LaTeX report sources/build outputs have been removed from this repo and will live in a **separate LaTeX repo** (which can be nested here later as a submodule if desired).

## Structure
- `pipelines/`: Reusable scripts + templates (dataset-agnostic)
- `mouse/`: Dataset-scoped workflow notes for the current mouse dataset
- `_tmp_zebrafish_2026-03-02/`: Archived zebrafish workspace + QC bundles (safe to delete later)
- `project_datasets/`: RunInfo CSVs and run lists used during dataset selection/validation
- `starter_pipeline/`: Starter pipeline scripts/configs (older)

## Current status (dataset pivot)
- We used the zebrafish workspace to build and test the repeatable pipeline (download → FastQC → **FASTX** trim → FastQC), then archived it to keep the repo clean.
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
