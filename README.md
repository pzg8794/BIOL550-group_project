# BIOL550 Group Project Workspace

This repo contains the **group project workspace** (dataset metadata, scripts, notes) for BIOL550.

LaTeX report sources/build outputs have been removed from this repo and will live in a **separate LaTeX repo** (which can be nested here later as a submodule if desired).

## Structure
- `project_datasets/`: RunInfo CSVs and run lists used during dataset selection/validation
- `starter_pipeline/`: Starter pipeline scripts/configs
- `zebrafish/`: Zebrafish-specific workspace (scripts, run lists, gitignored data folder)

## Usage
See the per-project README(s), e.g.:

- `zebrafish/README.md`

## Organization Tips
- Keep downloaded sequencing data out of Git (store under `zebrafish/data/` which is gitignored).
- Prefer scripts + metadata that can reproduce the download/validation steps.

---

_Please keep this repo organized and avoid committing large binary outputs._
