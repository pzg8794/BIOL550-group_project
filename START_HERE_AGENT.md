# Start Here — BIOL550 Group Project Agent Guide

This is the read-first handoff file for future Codex sessions working in `Semester5/BIOL550/group_project/`.

## Purpose

Use this file to get oriented quickly and avoid breaking the project workflow, documentation standards, or server-minimum policy.

## Required read order

Read these in order before taking action:

1. `AGENTS.md`
2. `DOCUMENTATION_MAP.md`
3. `SERVER_MINIMUM_POLICY.md`
4. `mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
5. `mouse/TODO_mouse.md`
6. `mouse/TODO_qc_remediation.md`
7. `WORKLOG.md`

If the user asks about class requirements, reports, or grading expectations, then also read:
- `../BIOL550-Notes.md`
- `../BIOL550-Lab/task_n_desc.md`

## Working model

- The active dataset is the **mouse dataset**.
- The mouse workflow is the authoritative operational path.
- The remediation decision is already made:
  - `fastp` = default cleanup tool
  - `cutadapt` = targeted fallback

## Local vs server

- Local repo is the source of truth.
- Server usage must stay minimal.
- Long scripts and custom logic stay local unless they must be run on the server.
- If long code is needed on the server:
  1. copy it temporarily
  2. run it
  3. verify outputs
  4. delete the server copy

Helper for staging/removing long code:
- `pipelines/sync_long_code_to_sequoia.sh`

## Documentation discipline

Every meaningful update should leave a trace in the docs.

Use this pattern:
- **step**
- **status**
- **finding / learning**
- **decision**

Primary files to keep current:
- `mouse/TODO_mouse.md`
- `mouse/TODO_qc_remediation.md`
- `WORKLOG.md`

## Local environment

For BIOL550 local Python/Jupyter work, use:
- `/Users/pitergarcia/DataScience/Semester5/BIOL550/biol550_env`

## Current next-step priority

Before alignment, the active remaining sequence is:
1. compare full-dataset `fastp` post-QC vs current FASTX baseline
2. freeze cleaned-input paths / naming
3. determine whether any sample still needs targeted `cutadapt`
4. freeze mouse reference genome + annotation pair
5. finalize sample sheet / design matrix
6. prepare STAR manifest and alignment QC capture plan

## Caution

- Do not make broad cosmetic changes to notebooks unless explicitly requested.
- Prefer script-first generation for comparisons and notebook-as-presentation.
- Keep cross-links intact when updating docs.
