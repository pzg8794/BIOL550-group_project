# Mouse project — follow guide (simple version)

Purpose:
- give the team a simple version of what was done
- show what to read, what the decision was, and what still needs attention
- reduce repeated “what happened?” or “what do I do next?” questions

## Short version

We already did the cleanup comparison work.

We tested:
- `FASTX`
- `FASTX + cutadapt`
- `fastp`

We first tested them on the most problematic reads, then checked the result against the full dataset.

Current answer:
- use `fastp` as the main cleanup tool
- keep `cutadapt` only as a fallback if a later sample-specific problem appears

## What you should look at first

### If you want the simple explanation
- `notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`

### If you want the full explanation
- `notebooks/qc_remediation_experiments_mouse.ipynb`

### If you want the report version
- `reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`

## What was the actual problem?

The first trimming strategy (`FASTX`) did not fully remove the adapter-related technical signal.

That is why we did the remediation comparison.

## What did we compare?

### First: pilot reads
We started with the worst/problematic reads to learn:
- which tool cleaned better
- which tool kept more reads
- which tool made the most sense for the dataset

### Second: full dataset
After that, we checked the chosen cleanup approach against the full FASTX baseline.

That gave us the full-dataset answer, not just the pilot answer.

## What did we learn?

Main findings:
- `fastp` cleaned the residual adapter signal much better than FASTX
- `fastp` also outperformed `cutadapt` as the default cleanup tool for this dataset
- `cutadapt` is still useful, but not as the main batch cleanup tool here
- the remaining low-level warnings are mostly things to monitor, not things to keep trimming forever

## The easiest evidence files to open

If you only want the key evidence, open these:
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_summary.md`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_adapter_comparison.png`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_summary_dashboard.png`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_retention_tradeoff.png`

## What is already done

Already done:
- raw download + raw FastQC
- FASTX trimming + post-FASTX FastQC
- raw-vs-trimmed baseline QC review
- pilot remediation comparison
- full `fastp` rerun
- post-`fastp` FastQC
- FASTX-vs-`fastp` full-dataset comparison
- updated weekly report and notebook

## What still needs to be decided

Still open:
- confirm the final cleaned-input root for alignment
- confirm the reference genome + annotation pair
- build the sample/design sheet
- prepare the STAR manifest

## If you need to follow the project without digging through everything

Do this in order:
1. open `notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`
2. open `ALIGNMENT_PREP_TEAM_DRAFT.md`
3. open `TODO_mouse.md`

That is enough to understand:
- what was done
- why `fastp` won
- what the next alignment-prep tasks are

## What not to do

- do not rerun the whole pipeline unless we agree to do that
- do not assume every warning means “trim more”
- do not use old FASTX outputs as the preferred alignment inputs
- do not ask where the evidence is before checking the notebook/report paths above

## One-line project status

Cleanup comparison is done, `fastp` won, and the project is now in alignment-preparation mode.
