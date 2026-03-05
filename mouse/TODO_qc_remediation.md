# Mouse QC remediation — adapter signal + duplication (PRJNA1017789)

Goal: test a few *paired-end aware* cleanup approaches to address QC issues that **FASTX quality trimming** did not improve (especially **adapter signal**), while documenting what is *fixable* vs *expected* in bulk RNA-seq.

Key QC exports (local):
- SRR triage (full dataset): `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/fastqc_warn_fail_modules_by_srr_full.md`
- Overrepresented sequences breakdown: `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/fastqc_overrepresented_sequences.csv`

Key QC findings (global vs outlier):
- **Global (most/all SRRs):**
  - `Adapter Content` = FAIL (raw + trimmed) → quality trimming won’t remove adapters.
  - `Sequence Duplication Levels` = FAIL (raw + trimmed) → often expected in RNA-seq; treat as *dataset property* unless extreme outliers.
  - `Sequence Length Distribution` = WARN (trimmed only) → expected side-effect of trimming.
- **Outlier-type issues (subset of SRRs):**
  - `Overrepresented sequences` = FAIL on a small subset → likely the best SRRs to target first for adapter/contaminant confirmation.

## Server layout (shared; group-writable)

Dataset root (canonical):
- `/home/zebrafish/mouse/PRJNA1017789/`

Create a single “experiments” folder so results don’t mix with baseline:
- `/home/zebrafish/mouse/PRJNA1017789/qc_remediation/`
  - `fastp/`
  - `fastx_clipper/`
  - `cutadapt/`
  - `fastqc_after/`
  - `logs/`

## SRR triage (work one-by-one)

Start with the worst SRRs (by severity; raw + trimmed):
- `SRR30333754`, `SRR30333756`, then `SRR30333743`

For each SRR, confirm:
1) Which FastQC modules are WARN/FAIL (worst-of-mates).
2) Whether `Overrepresented sequences` shows a consistent technical sequence (adapter / poly-A / etc).
3) Whether adapter-related modules improve after remediation.

## Approaches to test (paired-end)

### A) `fastp` (recommended first pass; all-in-one)

Why: paired-end aware; can detect/trim adapters + do quality trimming in one pass; emits its own HTML/JSON report.

Minimum test (1 SRR):
- Inputs: `sra_runs/SRRxxxx_1.fastq.gz`, `sra_runs/SRRxxxx_2.fastq.gz`
- Outputs: `qc_remediation/fastp/`
- Run FastQC on fastp outputs into: `qc_remediation/fastqc_after/fastp/`

Success criteria:
- `Adapter Content` and `Overrepresented sequences` move toward WARN/PASS (or at least visibly reduced).
- Read length distribution doesn’t collapse (avoid over-trimming).

### B) `FASTX fastx_clipper` (+ optional quality trim)

Why: “classic” toolchain; requires a known adapter sequence; can be used to mirror course tooling expectations.

Notes:
- `fastx_clipper` exists on Sequoia at: `/usr/local/bin/FastX/0.0.13/fastx_clipper`
- Only do this once you identify an adapter candidate from FastQC.

### C) `cutadapt` (targeted; best when you know sequence/primer)

Why: best for anchored primers/amplicons or known sequences with controlled mismatches; paired-end aware.

Use when:
- You have a clear sequence to remove (from `fastqc_overrepresented_sequences.csv` or kit docs), OR
- You need anchored trimming (e.g., `^PRIMER`).

## Output review checklist (per SRR)

After each approach, run FastQC and record:
- `Adapter Content` (PASS/WARN/FAIL)
- `Overrepresented sequences` (PASS/WARN/FAIL) + top sequences
- `Per base sequence content` (does it improve?)
- `% reads retained` / read-length distribution sanity check

## Decisions log

- If `Adapter Content` improves with `fastp`: adopt `fastp` as the next pipeline stage for the project (replace FASTX-only trimming).
- If adapter signal persists even after `fastp`: treat as library property; proceed but call it out in downstream interpretation.
- Duplication: do **not** try to “fix” with trimming; only flag extreme outliers for possible exclusion.

