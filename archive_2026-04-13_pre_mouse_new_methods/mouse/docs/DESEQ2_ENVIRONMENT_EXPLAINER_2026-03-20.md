# DESeq2 environment explainer — why this approach was used

## Purpose

This note explains, in plain technical terms, why the mouse DESeq2 setup was built as a self-contained environment, what each tool is doing, and why simply copying an existing environment tree from one location to another can break.

This is **not** the teammate handoff guide.  
This is the internal “be able to defend the setup” note.

## The actual problem

The core problem was **not** “Python packages are missing.”

The core problem was:

- the server already had an `R` binary
- but that `R` binary was **broken at runtime**
- specifically, it failed because a required shared library was missing:
  - `libreadline.so.7`

That means the server’s default `R` could not be trusted as the base for installing or running `DESeq2`.

In practical terms:

- if `R` itself does not start cleanly, then installing `DESeq2` “into that R” is the wrong fix
- the fix has to include a **working R runtime**, not just an R package install

## Why a self-contained environment was the right fix

The goal was to create a runtime that:

- has its **own R binary**
- has its **own libraries**
- has its **own Bioconductor packages**
- does **not** depend on the broken server `R`
- does **not** change the server’s current/global setup

That is what a self-contained environment gives.

For this project, the final target is the shared mouse tree on `sequoia`, not a private home-directory path:

- `/home/zebrafish/mouse/PRJNA1017789_parallel/.local/share/micromamba/envs/biol550_deseq2`

## What tool was used

The environment was created with `micromamba`.

### What `micromamba` is

`micromamba` is a lightweight environment manager in the same family as `conda`.

Conceptually, it does the same kind of job:

- creates isolated environments
- installs pinned package versions
- can install **R**, not just Python
- can install compiled scientific dependencies
- can keep that runtime separate from the system installation

The important point is this:

- this was **not** a Python-only environment
- this was a **self-contained environment manager used to install its own R runtime**

So the real fix was:

- create a private environment
- install `R 4.3.3`
- install `DESeq2`
- run the workflow against that environment instead of `/usr/local/bin/R`

## Why not a plain Python virtual environment

A Python `venv` would not solve this.

Why:

- Python `venv` isolates Python packages
- it does **not** provide a working R runtime
- it does **not** solve missing shared-library issues for the server’s broken `R`

So:

- `python venv` = wrong tool for this specific problem
- self-contained env with its own `R` = correct tool

## Why `DESeq2` required this

`DESeq2` is an **R / Bioconductor** package.

It is not a Python package.

So the actual software stack needed for this task is:

- a working `R`
- Bioconductor-compatible package installation
- `DESeq2`
- the plotting/helper packages used by the driver

That is why the environment setup was driven by the needs of **R**, not Python.

## Why simply copying an existing environment tree can break

This was the key concern with the idea of “copy the `.local/share` env somewhere else.”

The problem is that many environments are **prefix-bound**.

That means the environment was created expecting to live at one exact path, for example:

- `/home/pzg8794/.local/share/micromamba/envs/biol550_deseq2`

If that whole directory is copied to a new place, parts of it may still point back to the old path.

### What can be path-bound

Examples:

- activation metadata
- launcher scripts / shebang lines
- embedded binary paths
- compiled-library lookup paths
- `R` package configuration that assumes a specific `R_HOME`
- symlinks or wrappers that were built against the original prefix

So even if a copied environment “looks complete,” it may fail in subtle ways because:

- executables still reference the old prefix
- libraries are resolved from the wrong location
- activation does not reconstruct the environment the way the original install expected

That is why the safer approach is usually:

- **create the environment directly at the final path**

instead of:

- create it somewhere else and then copy it

In this case, that means:

- better final state:
  - build the environment directly under `/home/zebrafish/mouse/PRJNA1017789_parallel/.local/...`
- weaker transitional state:
  - build it under `/home/pzg8794/.local/...` and ask teammates to depend on that

## Why the original choice used `/home/pzg8794/.local`

The first working version was created under:

- `/home/pzg8794/.local/share/micromamba/envs/biol550_deseq2`

Why that happened:

- it was the fastest low-risk way to get a working DESeq2 runtime after confirming the server `R` was broken
- it avoided modifying the global server setup
- it gave a controlled proof that the DESeq2 stack would work on `sequoia`

That choice solved the runtime problem quickly, but it was not the best final team-facing path because it still depended on a private home-directory location.

## Why that was not the ideal final team setup

From a team/process standpoint, a better final state is:

- team-facing activation and wrappers live in the **shared tree**
- teammates do not have to know or depend on private home-directory paths
- the workflow is easier to teach and defend

That is why the follow-up direction to move the needed activation/runtime pieces into the shared tree was the correct requirement.

## The clean mental model

There are three separate layers here:

### 1) System layer

What the server already has installed globally.

In this case:

- system `R` existed
- but it was broken

### 2) Environment layer

A self-contained runtime that brings its own:

- `R`
- package manager state
- libraries
- Bioconductor packages

This is what was needed to bypass the broken system `R`.

### 3) Workflow layer

The small scripts and commands that teammates actually use:

- activation script
- short run wrapper
- shared input/output paths

This layer should be the simple one.

## What each relevant tool does

### `R`

The language/runtime that `DESeq2` runs on.

### `DESeq2`

An R/Bioconductor package for differential gene expression analysis of count data using the negative binomial framework.

### `BiocManager`

The standard R-side installer/manager for Bioconductor packages.

### `micromamba`

A lightweight environment manager used here to create an isolated runtime that includes its own `R` and package stack.

### `mouse_deseq2_all26.R`

The long canonical DESeq2 driver script.

This is the real analysis logic and should remain local as source-of-truth code.

### `mouse_deseq2_shared_server_run.sh`

A short operational wrapper.

Its job is to:

- point to the correct environment
- point to the correct shared inputs
- launch the canonical DESeq2 driver

### `mouse_deseq2_activate_shared.sh`

A short activation helper for teammates.

Its job is to make the shell use the correct DESeq2 runtime before running anything.

## What to defend if asked

If someone asks why this setup was used, the defensible answer is:

1. `DESeq2` requires a working `R` runtime.
2. The server’s existing `R` was broken because it could not load `libreadline.so.7`.
3. Installing packages into a broken runtime would not solve the real problem.
4. A self-contained environment with its own `R` fixed the runtime cleanly.
5. The long DESeq2 analysis code remained local as source of truth.
6. Only small operational wrappers and shared input/output artifacts were exposed in the team-facing server workflow.

## Final takeaway

The setup was not “using Python to fix R.”

The setup was:

- using an environment manager capable of installing **its own R runtime**
- because the server’s default `R` was broken
- while keeping the analytical code local and the team-facing workflow simple

## Minimal commands to remember

If this has to be explained quickly, the short version is:

### Activate the team environment

```bash
source /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_activate_shared.sh
```

### Run the shared wrapper

```bash
bash /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_shared_server_run.sh run
```

### If asked what those two scripts do

- `mouse_deseq2_activate_shared.sh`
  - points the shell at the shared micromamba root
  - loads shell integration
  - activates the `biol550_deseq2` environment
- `mouse_deseq2_shared_server_run.sh`
  - points to the shared count/metadata inputs
  - runs the canonical DESeq2 driver against those inputs

That is the core logic to defend.
