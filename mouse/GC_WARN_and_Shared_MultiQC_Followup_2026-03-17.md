# GC WARN follow-up + shared MultiQC correction (2026-03-17)

This note captures the full technical thread from the 2026-03-17 follow-up discussion about the shared MultiQC runs, the remaining `Per Sequence GC Content` WARN pattern after `fastp`, and the decision logic for what should happen next.

## Why this note exists

We needed one place that records:
- what was requested on the shared server
- what was run incorrectly first
- what was corrected afterward
- what the post-`fastp` GC WARN subset actually is
- whether that subset maps to a specific biological group in the mouse dataset
- what the current recommendation is for alignment

## 1) Shared MultiQC correction

### Step
- A shared-drive MultiQC run was requested specifically for the `fastp`-trimmed FastQC outputs on `sequoia`.
- The first shared run was mistakenly generated as a combined comparison report from both:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_out`
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_fastp_trim`
- That produced a mixed report at:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/shared_fastqc/mouse_shared_fastqc_multiqc.html`
- After the mismatch was identified, the shared report was rerun correctly using only the trimmed FastQC directory:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_fastp_trim`
- A separate raw-only report was also generated so the two stages can be inspected independently.

### Status
- Correct trimmed-only shared report exists.
- Correct raw-only shared report exists.
- The earlier combined shared report still exists as a comparison artifact, but it is not the trimmed-only answer.

### Finding
- Correct **trimmed-only** shared report:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/fastp_trim_only/mouse_fastp_trim_only_multiqc.html`
- Correct **before-trimming** shared report:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/before_trimming_only/mouse_before_trimming_only_multiqc.html`
- The trimmed-only shared report used `52` FastQC reports from `fastqc_fastp_trim` only.

### Decision
- Treat the shared `fastp_trim_only` report as the authoritative post-`fastp` shared MultiQC report.
- Treat the shared `before_trimming_only` report as the authoritative pre-trim shared MultiQC report.
- Do not use the mixed `shared_fastqc` run when the question is specifically “what do the `fastp`-trimmed files look like?”

### How we actually ran MultiQC

Dummy version:
- pick **one folder type only**
- point MultiQC at that folder
- write the report into a separate output folder
- name the report clearly so nobody confuses stages

The important rule is:
- if the question is **after trimming**, use only the trimmed FastQC folder
- if the question is **before trimming**, use only the raw FastQC folder
- do **not** mix both folders unless you intentionally want a comparison-style report

#### Mouse example — trimmed only

This is the command pattern for the corrected shared trimmed-only report:

```bash
multiqc \
  --force \
  --dirs \
  --dirs-depth 1 \
  /home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_fastp_trim \
  --outdir /home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/fastp_trim_only \
  --filename mouse_fastp_trim_only_multiqc.html
```

What each part means:
- `multiqc` = run MultiQC
- `--force` = overwrite an old report if the folder already has one
- `--dirs` = keep directory names in the labels so we know where inputs came from
- `--dirs-depth 1` = only keep one directory level in those labels
- input folder:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_fastp_trim`
- output folder:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/fastp_trim_only`
- output file name:
  - `mouse_fastp_trim_only_multiqc.html`

#### Mouse example — before trimming only

```bash
multiqc \
  --force \
  --dirs \
  --dirs-depth 1 \
  /home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_out \
  --outdir /home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/before_trimming_only \
  --filename mouse_before_trimming_only_multiqc.html
```

This is the same idea, but now the input folder is the raw FastQC folder instead of the trimmed FastQC folder.

#### Zebrafish example — same logic

If we were doing the same thing for zebrafish, the structure would be identical:

```bash
multiqc \
  --force \
  --dirs \
  --dirs-depth 1 \
  /home/zebrafish/zebrafish/PROJECT_NAME/fastqc_fastp_trim \
  --outdir /home/zebrafish/zebrafish/PROJECT_NAME/multiqc/fastp_trim_only \
  --filename zebrafish_fastp_trim_only_multiqc.html
```

The logic does not change:
- one stage
- one matching FastQC input folder
- one clearly named output folder

#### Private canonical full-`fastp` example

The canonical private full-`fastp` report used one more input type, because it included both:
- post-`fastp` FastQC outputs
- `fastp` JSON reports

That command pattern was:

```bash
multiqc \
  --force \
  --dirs \
  --dirs-depth 1 \
  /home/pzg8794/mouse_qc_remediation/output/fastqc_after/fastp \
  /home/pzg8794/mouse_qc_remediation/output/fastp/reports \
  --outdir /home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/report \
  --filename mouse_fastp_all_srrs_multiqc.html
```

That is why the private canonical MultiQC includes:
- FastQC sections
- `fastp` report sections

while the shared trimmed-only report includes:
- FastQC sections only

#### Step-by-step summary

1. Decide which stage you want to summarize.
2. Pick the matching FastQC folder for that stage.
3. Create a separate output folder for that exact report.
4. Run MultiQC on only that intended input set.
5. Name the report clearly so it is obvious what stage it summarizes.

That is the whole workflow.

## 2) Local copy of the corrected shared trimmed-only report

### Step
- Copied the corrected shared trimmed-only MultiQC report from `sequoia` to the local repo for direct inspection on the local machine.

### Status
- Local copy is present.

### Finding
- Local copied path:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/`
- Main local HTML:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/mouse_fastp_trim_only_multiqc.html`

### Decision
- Use the copied local report when discussing the trimmed-only shared result locally.

## 3) Post-`fastp` GC WARN pattern

### Step
- Examined the corrected trimmed-only shared MultiQC report for the remaining `Per Sequence GC Content` signal.
- Extracted the sample list for the yellow/WARN entries from the trimmed-only MultiQC data bundle.

### Status
- Sample list identified.

### Finding
- Post-`fastp` `Per Sequence GC Content` status:
  - `27 PASS`
  - `25 WARN`
  - `0 FAIL`
- WARN entries in the trimmed-only report:
  - `SRR30333756_1`
  - `SRR30333757_1`, `SRR30333757_2`
  - `SRR30333758_1`, `SRR30333758_2`
  - `SRR30333759_1`, `SRR30333759_2`
  - `SRR30333760_1`, `SRR30333760_2`
  - `SRR30333761_1`, `SRR30333761_2`
  - `SRR30333762_1`, `SRR30333762_2`
  - `SRR30333763_1`, `SRR30333763_2`
  - `SRR30333764_1`, `SRR30333764_2`
  - `SRR30333765_1`, `SRR30333765_2`
  - `SRR30333766_1`, `SRR30333766_2`
  - `SRR30333767_1`, `SRR30333767_2`
  - `SRR30333768_1`, `SRR30333768_2`
- This WARN subset is not random. It clusters mainly in a contiguous accession block:
  - `SRR30333757` through `SRR30333768`
  - plus `SRR30333756_1`

### Decision
- Treat the remaining GC WARN pattern as a real subset effect worth documenting.
- Do not assume it is random noise.

## 4) Metadata check: does the GC WARN subset map to one biological group?

### Step
- Pulled GEO/SRA metadata for `GSE243308` / `PRJNA1017789` and mapped the WARN SRR block against the published sample labels.
- Checked whether the WARN subset corresponds to one simple experimental group such as control vs injury or WT vs conditional knockout.

### Status
- Quick metadata mapping completed.

### Finding
The WARN subset **does map to a real subset of the study**, but **not to one simple biological condition**.

The study design includes at least these groups among the matching SRRs:
- `Control DRG`, replicates 1–3
- `Conditional Knockout DRG`, replicates 1–3
- `Control DRG, injury`, replicates 1–3
- `Conditional Knockout DRG, injury`, replicates 1–3

Example mappings checked during the follow-up:
- `SRR30333768` -> `GSM8476473` -> `Control DRG, replicate 1`
- `SRR30333758` -> `GSM8476483` -> `Conditional Knockout DRG, injury, replicate 2`
- `SRR30333757` -> `GSM8476484` -> `Conditional Knockout DRG, injury, replicate 3`
- `SRR30333756` -> `GSM8476485` -> `Conditional Knockout DRG, contralateral, replicate 1`
- `SRR30333755` -> `GSM8476486` -> `Conditional Knockout DRG, contralateral, replicate 2`
- `SRR30333743` -> `GSM8476498` -> `Control DRG, ipsilateral, replicate 2`

Interpretation from the metadata check:
- the WARN block is **not** “all injured”
- it is **not** “all control”
- it is **not** “all conditional knockout”
- it is **not** a simple sick-vs-control split
- it looks more like a broader cohort / sample-block / hidden-batch style subset than a single clean condition label

### Decision
- Do not justify sample removal solely by claiming the WARN subset belongs to one biological condition, because the quick metadata check does not support that.

## 5) How the remaining GC signal should be interpreted

### Step
- Compared the remaining GC issue against the earlier transcript-guided interpretation already recorded in the report and remediation notes.
- Rechecked the professor-related notes around GC/content-style QC interpretation.

### Status
- Interpretation checkpoint completed.

### Finding
What remains after `fastp` is a GC/content-style WARN pattern, not the original adapter problem.

Already-supported internal interpretation:
- adapters were the main technical cleanup target
- those adapter-related modules improved strongly after `fastp`
- the remaining GC signal appears narrower and much closer to the pass-state curves than the original technical artifact signal
- the remaining GC WARN subset does not cleanly correspond to one simple experimental condition

This is consistent with the working interpretation already documented elsewhere:
- GC bell-shape plots are sanity checks, not the primary decision metric
- small GC-shape differences should be monitored rather than automatically over-corrected

### Decision
- Do not treat the remaining `Per Sequence GC Content` WARN pattern as proof that more trimming is required.
- Treat it as a monitored issue unless downstream alignment metrics show that this subset is genuinely underperforming.

## 6) Current recommendation

### Step
- Evaluated the practical options discussed during the follow-up:
  - remove samples
  - trim more aggressively
  - subset immediately
  - proceed to alignment and evaluate alignment metrics by subgroup

### Status
- Recommendation recorded.

### Finding
The strongest current option is:
- **do not remove samples yet**
- **do not trim further just to chase the GC curve**
- **proceed to alignment with the `fastp` outputs**
- **capture alignment metrics by sample and compare the GC-WARN subset vs the GC-PASS subset**

Why this is currently the best choice:
- the main adapter-related technical problem was fixed
- the remaining signal is `WARN`, not `FAIL`
- the WARN subset does not map cleanly to one biological condition
- there is no direct evidence yet that additional trimming would be the correct fix
- there is no direct evidence yet that the WARN samples are technically unreliable enough to exclude before alignment

### Decision
Use alignment as the next decision layer.

Capture per-sample STAR metrics at minimum:
- uniquely mapped
- multi-mapped
- unmapped / too many loci
- unmapped / too short

Then compare those metrics between:
- the GC-WARN subset
- the GC-PASS subset

Only escalate to exclusion/subsetting if the WARN subset also shows meaningful downstream alignment problems.

## 7) Practical file references from this follow-up

### Shared reports
- before trimming:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/before_trimming_only/mouse_before_trimming_only_multiqc.html`
- after trimming:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/fastp_trim_only/mouse_fastp_trim_only_multiqc.html`

### Local copied trimmed-only report
- `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/mouse_fastp_trim_only_multiqc.html`

### Related docs
- `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`
- `Semester5/BIOL550/group_project/mouse/TODO_qc_remediation.md`
- `Semester5/BIOL550/group_project/WORKLOG.md`
- `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`
