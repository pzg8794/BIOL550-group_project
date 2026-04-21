# SRP618841 dataset intake (parallel mouse candidate)

## Documentation links

- Parent mouse workflow: [PROCESS_mouse_fastq_fastqc_fastx.md](../mouse/PROCESS_mouse_fastq_fastqc_fastx.md)
- Dataset-specific process doc: [SRP618841_PROCESS_fastq_fastqc_fastp.md](SRP618841_PROCESS_fastq_fastqc_fastp.md)
- Dataset-specific TODO: [TODO_srp618841.md](TODO_srp618841.md)
- Group project work log: [../WORKLOG.md](../WORKLOG.md)
- Group project documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)

## Step

- Pulled the canonical SRA RunInfo table for `SRP618841`.
- Derived a canonical 20-run list for the parallel candidate branch.
- Reserved a separate server root and metadata root so this candidate dataset does not collide with the historical `PRJNA1017789` snapshot.

## Status

- Intake complete.
- Parallel-candidate branch initialized locally.
- Server runtime prepared for staged launch.
- Stage A launch is running on `sequoia`.

## Finding

- `SRP618841` contains `20` runs.
- All runs are:
  - `Mus musculus`
  - `RNA-Seq`
  - `PAIRED`
  - `Illumina NovaSeq X`
- BioProject: `PRJNA1322439`

## Decision

- Treat `SRP618841` as a **parallel candidate dataset**, not a replacement for the active mouse dataset.
- Reuse the current project infrastructure, but keep the runtime isolated under:
  - server data root: `/home/zebrafish/mouse/SRP618841_parallel/`
  - server metadata root: `/home/pzg8794/metadata/SRP618841/`
- Use `fastp` as the default cleanup tool for this branch.
- Stage work in this order:
  1. download + raw FastQC
  2. `fastp` + post-`fastp` FastQC
  3. alignment prep and reference freeze
  4. alignment summaries and count handoff
  5. DE scaffolding after design review

## Launch note

- Stage A start time:
  - `2026-03-25 13:34 EDT`
- Current server PIDs:
  - download: `412454`
  - fastqc: `412456`
- Current logs:
  - `/home/zebrafish/mouse/SRP618841_parallel/.pipeline/raw/download.nohup.log`
  - `/home/zebrafish/mouse/SRP618841_parallel/.pipeline/raw/fastqc.nohup.log`
