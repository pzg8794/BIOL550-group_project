# DESeq2 shared-server setup — 2026-03-20

## Documentation links

- Parent mouse workflow: [PROCESS_mouse_fastq_fastqc_fastx.md](PROCESS_mouse_fastq_fastqc_fastx.md)
- Active task list: [TODO_mouse.md](TODO_mouse.md)
- DE note: [DIFFERENTIAL_EXPRESSION_NOTEBOOK_2026-03-19.md](DIFFERENTIAL_EXPRESSION_NOTEBOOK_2026-03-19.md)
- Server policy: [../SERVER_MINIMUM_POLICY.md](../SERVER_MINIMUM_POLICY.md)
- Documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)
- Work log: [../WORKLOG.md](../WORKLOG.md)

## Step

- Created a shared-tree team DESeq2 runtime on `sequoia`:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/.local/share/micromamba/envs/biol550_deseq2`
- Installed:
  - `R 4.3.3`
  - `DESeq2`
  - `BiocManager`
  - supporting plotting / CLI packages used by the existing driver
- Added a short shared-server wrapper locally:
  - `Semester5/BIOL550/group_project/pipelines/mouse_deseq2_shared_server_run.sh`
- Added a short shared activation helper locally:
  - `Semester5/BIOL550/group_project/pipelines/mouse_deseq2_activate_shared.sh`
- Kept the long DESeq2 driver local as canonical:
  - `Semester5/BIOL550/group_project/pipelines/mouse_deseq2_all26.R`

## Status

- The shared-tree team DESeq2 environment exists and is the intended runtime.
- The shared-server wrapper is the intended stable entrypoint for team use.
- The long DESeq2 driver remains temporary server-side code when copied for execution.

## Finding

- The existing server `R` was not usable for this workflow.
- Root issue:
  - `/usr/local/bin/R` failed at runtime because `libreadline.so.7` was missing
- That made direct use of the current server/global R stack unreliable.
- A self-contained micromamba environment fixed the runtime issue without changing the server’s current setup.
- One package-spec issue also surfaced during setup:
  - `bioconductor-biocmanager` did not exist in the chosen channels
  - `r-biocmanager` was the correct package name
- Copying an already-built micromamba prefix from one path to another was rejected as the final team solution because these environments can be prefix-bound; the safer fix was to create the team environment directly at the final shared path.

## Decision

- Keep the DESeq2 runtime out of the server-global setup, but place the team-facing environment under the shared mouse tree.
- Use the shared directory only for:
  - count / metadata inputs
  - output artifacts
  - short operational wrapper scripts
  - the team-owned `.local` runtime needed to activate `R 4.3.3` + `DESeq2`
- Keep the long `mouse_deseq2_all26.R` driver local as the source of truth.
- Copy the long driver to `/home/pzg8794/pipelines/` only when a server-side DE run is needed, then remove it after verification.

## Exact server paths

- shared team env:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/.local/share/micromamba/envs/biol550_deseq2`
- shared team micromamba root:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/.local/share/micromamba`
- shared team micromamba binary:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/.local/bin/micromamba`
- shared input root:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/deseq2_shared/inputs/`
- shared output root:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/deseq2_shared/output/`
- shared wrapper path:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_shared_server_run.sh`
- shared activation script:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_activate_shared.sh`
- local canonical activation helper:
  - `Semester5/BIOL550/group_project/pipelines/mouse_deseq2_activate_shared.sh`
- temporary long driver path:
  - `/home/pzg8794/pipelines/mouse_deseq2_all26.R`

## Exact commands

### Shared activation path for teammates

```bash
source /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_activate_shared.sh
```

### Environment check after activation

```bash
R --version | head -n 2
Rscript -e "cat(R.version.string, '\n'); suppressPackageStartupMessages(library(DESeq2)); cat('DESEQ2_OK\n')"
```

### One-command environment check without activation

```bash
export MAMBA_ROOT_PREFIX=/home/zebrafish/mouse/PRJNA1017789_parallel/.local/share/micromamba
/home/zebrafish/mouse/PRJNA1017789_parallel/.local/bin/micromamba run -n biol550_deseq2 \
  Rscript -e "cat(R.version.string, '\n'); suppressPackageStartupMessages(library(DESeq2)); cat('DESEQ2_OK\n')"
```

### Wrapper check

```bash
source /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_activate_shared.sh
bash /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_shared_server_run.sh check
```

### Shared run

```bash
source /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_activate_shared.sh
bash /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_shared_server_run.sh run
```

### Long-code lifecycle

```bash
scp Semester5/BIOL550/group_project/pipelines/mouse_deseq2_all26.R \
  pzg8794@sequoia.rit.edu:/home/pzg8794/pipelines/

scp Semester5/BIOL550/group_project/pipelines/mouse_deseq2_shared_server_run.sh \
  pzg8794@sequoia.rit.edu:/home/zebrafish/mouse/PRJNA1017789_parallel/scripts/

ssh pzg8794@sequoia.rit.edu \
  'bash /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_shared_server_run.sh check'

ssh pzg8794@sequoia.rit.edu \
  'rm -f /home/pzg8794/pipelines/mouse_deseq2_all26.R'
```
