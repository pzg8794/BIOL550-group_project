# BIOL550 Group Project — Agent Instructions

These instructions apply to everything under `Semester5/BIOL550/group_project/`.

## Read order before doing any work

Start here, in this order:

1. `START_HERE_AGENT.md`
2. `DOCUMENTATION_MAP.md`
3. `SERVER_MINIMUM_POLICY.md`
4. The active mouse workflow docs:
   - `mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
   - `mouse/TODO_mouse.md`
   - `mouse/TODO_qc_remediation.md`
5. `WORKLOG.md`

If the task is about reports or course requirements, also read:
- `../BIOL550-Notes.md`
- `../BIOL550-Lab/task_n_desc.md`

## Operating rules

- Keep the server footprint minimal.
- Keep long/custom code local by default.
- Copy long code to `/home/pzg8794` only when needed to run it.
- Delete long server-side code after the run and verification.
- Use `/Users/pitergarcia/DataScience/Semester5/BIOL550/biol550_env` for local Python/Jupyter work tied to BIOL550.

## Documentation rules

When changing project state, update the relevant docs with:
- **step** — what was done
- **status** — current state / completion state
- **finding** — what was learned
- **decision** — what follows from that result

At minimum, keep these consistent when work changes:
- `mouse/TODO_mouse.md`
- `mouse/TODO_qc_remediation.md`
- `WORKLOG.md`

If process or policy changes, also update:
- `mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
- `SERVER_MINIMUM_POLICY.md`
- `DOCUMENTATION_MAP.md` if navigation changed

## Workflow intent

This project is run as:
- local repo = source of truth for code, notebooks, analysis logic, and documentation
- server home (`/home/pzg8794`) = minimum execution layer, logs, required outputs, and short wrappers only

Do not leave long analytical or experimental code on the server.

## Notebook caution

- Do not make broad notebook layout changes unless explicitly requested.
- Prefer generating or updating artifacts from scripts, then showing them in notebooks.
- Keep explanations clear and comparison-driven.

## Current project context

- Zebrafish work is retired.
- Mouse dataset is the active dataset.
- `fastp` is the chosen default cleanup tool.
- `cutadapt` is the targeted fallback.

