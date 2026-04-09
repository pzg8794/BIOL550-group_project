# Mouse alignment start on local server (`sequoia`) — 2026-03-17

This note records the start of the mouse alignment phase on the local server-side workspace under `/home/pzg8794/`.

## Why alignment is starting now

This alignment start follows the QC remediation phase already documented in:
- `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`
- `Semester5/BIOL550/group_project/mouse/GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md`

The current project state before alignment is:
- `fastp` is the chosen cleanup stage for the mouse dataset.
- The authoritative cleaned-input root is:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
- The remaining `Per Sequence GC Content` WARN pattern was checked against study metadata.
- That GC WARN subset does **not** map to one simple biological condition.
- Current interpretation: the remaining GC pattern is more consistent with a study-subset / cohort / batch-style effect than with unresolved adapter contamination.

## Explicit decisions locked before the run

### Reference pair
- assembly: `GRCm39`
- source: `Ensembl`
- FASTA type: `primary assembly`
- annotation: matching Ensembl `GTF`

### Why this reference choice
- It keeps the reference and annotation in one matching source family.
- It uses the current mouse assembly instead of the older `GRCm38` baseline from the original paper.
- It avoids FASTA/GTF naming mismatches before STAR.
- The resolved Ensembl files at launch time were:
  - FASTA: `Mus_musculus.GRCm39.dna.primary_assembly.fa.gz`
  - GTF: `Mus_musculus.GRCm39.115.gtf.gz`

### Server-side reference/index location
- base reference root:
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/`
- STAR index:
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/star_index_sjdb150/`

### Input root
- cleaned fastq root:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`

### Alignment scope
- decision for the first STAR run:
  - align **all 26 SRRs first**

### Why `all 26` first
- Alignment is lower risk to run broadly than subsetting too early.
- If the team later decides to analyze only a subset (for example a `Golden 12` design), the aligned outputs will already exist.
- This avoids rerunning alignment simply because the downstream DE subset changes.

## Parallel execution approach

The alignment run reuses the same practical idea that worked well for parallel SRR download:
- keep one shared reference/index
- split the SRRs into three member-style run lists
- run one sequential STAR batch per split
- let the three batch jobs run in parallel

Existing run splits reused for the first alignment pass:
- `PRJNA1017789_runs.member.nikhi.txt`
- `PRJNA1017789_runs.member.piter.txt`
- `PRJNA1017789_runs.member.samuel.txt`

## Files added for this alignment start

Local pipeline sources:
- `Semester5/BIOL550/group_project/pipelines/mouse_star_prepare_reference.sh`
- `Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr.sh`
- `Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch.sh`
- `Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_parallel.sh`

These are intended to be copied to:
- `/home/pzg8794/mouse_qc_remediation/scripts/`

## Run start status

### Launcher
- local server-side launcher command was started under `nohup`
- first launcher shell PID:
  - `71014`
- corrected active launcher PID after fixing the reference-prep script:
  - `71166`
- launcher log:
  - `/home/pzg8794/mouse_qc_remediation/logs/run_star_all26_fastp_parallel.2026-03-17_233805.log`

### Current stage when this note was updated
- reference FASTA and GTF were already downloaded into:
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/dna/`
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/gtf/`
- the first launcher attempt failed quickly because STAR does not accept a compressed FASTA input
- the reference-prep script was corrected to unzip the FASTA and GTF before `genomeGenerate`
- the STAR index build was then restarted successfully as the first active long-running step
- the alignment root and all-26 manifest were already created at:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`

## Expected server outputs

### Reference
- `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/dna/`
- `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/gtf/`
- `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/meta/reference_choice.tsv`
- `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/logs/genomeGenerate.log`

### Alignment
- `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`
- per-sample STAR outputs under:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/samples/`
- per-sample logs under:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/logs/`
- launcher logs under:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/launcher_logs/`
- run manifest:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/all26_fastp_manifest.tsv`

## Next decision layer after alignment

After STAR finishes:
- compare alignment metrics between:
  - GC-WARN subset
  - GC-PASS subset
- minimum fields to review:
  - uniquely mapped
  - multi-mapped
  - unmapped / too many loci
  - unmapped / too short

Only revisit exclusion/subsetting if the GC-WARN subset also shows meaningful downstream alignment weakness.
