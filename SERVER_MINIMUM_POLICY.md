# Server Minimum Policy (Read Before Using `sequoia`)

This file defines the working rule for what belongs on the server and what must stay local.

## Core rule

**The server must keep the minimum needed for us to run jobs, preserve results, and show progress.  
Most of our real work must live locally, not on the server.**

Why:
- reduce the chance that long custom code is copied, reused, or picked apart by other people
- reduce accidental edits in shared environments
- reduce clutter and disk usage in `/home/pzg8794`
- keep the local repo as the single source of truth for our logic

## Default split

### Keep locally (default)

These should live in the local repo first and stay there unless we temporarily need them on the server:
- notebooks
- long Python / shell scripts
- comparison code
- analysis code
- plotting code
- custom parsers
- draft or experimental code
- anything with substantial logic

### Keep on the server (minimum only)

These are acceptable to keep in `/home/pzg8794`:
- input data needed to run the current job
- output artifacts needed for analysis or grading
- logs
- summary tables
- report files
- small wrapper scripts
- small templates that launch bigger jobs
- short helper scripts that are operational rather than analytical

## Long-code rule

Use this practical threshold:
- if a script is roughly **more than 100 lines**, treat it as **long code**
- long code should stay local by default

Allowed exception:
- copy long code to the server only right before execution
- run it
- verify the outputs
- delete the server copy

## What short server wrappers are allowed to do

Short server-side wrappers are fine if they mainly:
- define paths
- define environment variables
- call installed tools
- call a copied script
- run a short sequence of commands

In other words:
- **templates and launchers are okay**
- **large custom logic is not**

## Required lifecycle for long code

When a long script must be used on the server:

1. Keep the canonical version local.
2. Copy it to `/home/pzg8794/...` only when needed.
3. Run it.
4. Keep the outputs.
5. Delete the copied server-side code.
6. Log that the script must be recopied before reuse.

Minimal pattern:

```bash
scp /Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/pipelines/<script> \
  pzg8794@sequoia.rit.edu:/home/pzg8794/<target>/

ssh pzg8794@sequoia.rit.edu 'bash /home/pzg8794/<target>/<script>'

ssh pzg8794@sequoia.rit.edu 'rm -f /home/pzg8794/<target>/<script>'
```

Preferred helper for this project:

```bash
/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh list
/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh push mouse_qc_strategy_compare.py
/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh remove mouse_qc_strategy_compare.py
```

This helper keeps the current approved long-code file list in one place and avoids retyping copy/remove commands.

## What the server should look like after cleanup

Good server state:
- data we still need
- outputs we still need
- logs we still need
- reports we still need
- short wrappers only

Bad server state:
- old archived projects we are no longer using
- duplicate outputs
- large intermediate FASTQs after downstream outputs are secured
- old temporary code
- long custom scripts that also exist locally

## Current interpretation for this project

For the current mouse work:
- keep the mouse results and required QC/report artifacts
- keep only short wrappers on the server
- keep notebooks and long custom code local
- treat the local repo as the authoritative source for code

For retired work:
- zebra / zebrafish artifacts in `/home/pzg8794` should be removed unless explicitly needed again

## Documentation links

- Group project documentation map: [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)
- Group project work log: [WORKLOG.md](WORKLOG.md)
- Mouse process doc: [mouse/PROCESS_mouse_fastq_fastqc_fastx.md](mouse/PROCESS_mouse_fastq_fastqc_fastx.md)
- Mouse remediation plan: [mouse/TODO_qc_remediation.md](mouse/TODO_qc_remediation.md)
