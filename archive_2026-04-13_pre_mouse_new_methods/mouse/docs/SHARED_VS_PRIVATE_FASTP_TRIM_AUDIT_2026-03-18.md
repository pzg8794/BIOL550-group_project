# Shared vs private `fastp` trimmed-output audit — 2026-03-18

Purpose:
- document the direct comparison between the shared trimmed-after-`fastp` artifacts and the private canonical trimmed-after-`fastp` artifacts
- show what is actually the same
- show what is different
- make it easy to explain why the private output should be treated as canonical for alignment

## Short answer

The shared trimmed output is **not equivalent** to the private trimmed output.

What stayed the same:
- same `52` read-level reports
- same overall GC-warning pattern (`27 PASS / 25 WARN`)
- same broad module pattern for most FastQC modules

What changed:
- different trimmed FASTQ files
- different `fastp` JSON summaries
- different FastQC-derived sequence counts and length ranges
- shared report still has `1 WARN` in `Overrepresented Sequences`
- private report has `52 PASS` there

So the correct conclusion is:
- the shared output should **not** be treated as interchangeable with the private output
- the private output should be the canonical cleaned-input source for alignment

## What was compared

### Shared trimmed-only MultiQC
- HTML:
  - [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/mouse_fastp_trim_only_multiqc.html`](qc_analysis_remediation/multiqc_fastp_trim_only_shared/mouse_fastp_trim_only_multiqc.html)
- data dir:
  - [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/mouse_fastp_trim_only_multiqc_data`](qc_analysis_remediation/multiqc_fastp_trim_only_shared/mouse_fastp_trim_only_multiqc_data)

### Private trimmed-only MultiQC
- HTML:
  - [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_private/mouse_fastp_all_srrs_multiqc.html`](qc_analysis_remediation/multiqc_fastp_trim_only_private/mouse_fastp_all_srrs_multiqc.html)
- data dir:
  - [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_private/mouse_fastp_all_srrs_multiqc_data`](qc_analysis_remediation/multiqc_fastp_trim_only_private/mouse_fastp_all_srrs_multiqc_data)

### Supporting audit artifacts
- [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/shared_vs_private_fastp_trim_audit/audit_summary.tsv`](qc_analysis_remediation/shared_vs_private_fastp_trim_audit/audit_summary.tsv)
- [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/shared_vs_private_fastp_trim_audit/module_status_counts_shared_vs_private.svg`](qc_analysis_remediation/shared_vs_private_fastp_trim_audit/module_status_counts_shared_vs_private.svg)
- [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/shared_vs_private_fastp_trim_audit/total_sequences_private_vs_shared.svg`](qc_analysis_remediation/shared_vs_private_fastp_trim_audit/total_sequences_private_vs_shared.svg)
- [`Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/shared_vs_private_fastp_trim_audit/avg_length_private_vs_shared.svg`](qc_analysis_remediation/shared_vs_private_fastp_trim_audit/avg_length_private_vs_shared.svg)

## Images

### Module-status counts

![Module status counts](qc_analysis_remediation/shared_vs_private_fastp_trim_audit/module_status_counts_shared_vs_private.svg)

### Total sequences per read report

![Total sequences](qc_analysis_remediation/shared_vs_private_fastp_trim_audit/total_sequences_private_vs_shared.svg)

### Average trimmed read length per report

![Average length](qc_analysis_remediation/shared_vs_private_fastp_trim_audit/avg_length_private_vs_shared.svg)

## Main findings

### 1) The reports were built differently

The shared MultiQC run was built only from:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_fastp_trim`

The private MultiQC run was built from:
- `/home/pzg8794/mouse_qc_remediation/output/fastqc_after/fastp`
- `/home/pzg8794/mouse_qc_remediation/output/fastp/reports`

So the full MultiQC reports are not one-to-one equivalent objects. The private report includes both:
- FastQC-derived content
- `fastp` report-derived content

The shared report includes only:
- FastQC-derived content

This explains some display/layout differences, but **not** the differences in the FastQC values themselves.

## 2) The sample set is the same, but the FastQC values are not

The two `multiqc_fastqc.txt` files cover the same:
- `52` read-level samples

But the shared and private values differ across the read reports.

Examples from the comparison:
- shared `Sequence length` example:
  - `15-151`
- private `Sequence length` example:
  - `30-151`

Across the compared rows, the shared report shows:
- lower `Total Sequences`
- shorter minimum length
- slightly different average sequence lengths

That means the underlying trimmed outputs are not the same.

## 3) The remaining GC issue is similar in both

This part is important:
- the GC-warning pattern is basically the same in both reports
- both show:
  - `27 PASS`
  - `25 WARN`

So the remaining GC issue is **not** the main divergence between the two outputs.

That means:
- the shared output is not “wrong” because it shows the GC issue
- the shared output is problematic because the trimmed read set itself does not match the private canonical run

## 4) One module result is cleaner in the private output

`Overrepresented Sequences`:
- shared:
  - `51 PASS / 1 WARN`
- private:
  - `52 PASS / 0 WARN`

So even at the module-summary level, the private output is slightly cleaner.

## 5) The trimmed FASTQ outputs themselves differ

Spot checks on the server showed that matching shared/private trimmed FASTQ files are not identical in size.

Examples:

| SRR | Mate | Private bytes | Shared bytes |
|---|---:|---:|---:|
| `SRR30333743` | 1 | `3511374716` | `3509814034` |
| `SRR30333743` | 2 | `3481447851` | `3480417608` |
| `SRR30333757` | 1 | `3670339015` | `3669782971` |
| `SRR30333757` | 2 | `3723982380` | `3723765051` |
| `SRR30333768` | 1 | `3318283190` | `3317582072` |
| `SRR30333768` | 2 | `3364210459` | `3363777203` |

That is direct evidence that the trimmed outputs are not the same files.

## 6) The `fastp` JSON summaries also differ

Examples:

### `SRR30333743`
- private after reads:
  - `96952822`
- shared after reads:
  - `96891084`

### `SRR30333757`
- private after reads:
  - `89927674`
- shared after reads:
  - `89896026`

### `SRR30333768`
- private after reads:
  - `82290262`
- shared after reads:
  - `82256406`

The before-read counts match, but the after-filtering counts do not.

That means the shared run and private run did not produce the same filtered output, even when they started from the same raw read totals.

## What is likely right vs wrong here

### What is right
- It is correct that the shared report still shows the same broad GC issue.
- It is correct that this does not automatically block alignment by itself.

### What is wrong
- It is wrong to treat the shared trimmed output as equivalent to the private trimmed output.
- It is wrong to assume the same GC pattern means the trimmed read sets are interchangeable.
- It is wrong to greenlight troubleshooting on the assumption that the shared output is a faithful copy of the private canonical run without checking the trimmed outputs directly.

## What this means for alignment

For alignment, the important point is:

The main problem is **not** that the shared version still shows the GC issue.  
The main problem is that the shared trimmed read set is not the same as the private trimmed read set.

That matters because differences in trimmed outputs can change:
- retained read counts
- read-length distribution
- duplication estimates
- alignment rates
- gene counts

So alignment should use **one canonical cleaned-input root**, not treat the shared and private trimmed outputs as interchangeable.

## Canonical decision

Use the private cleaned-input root as canonical:
- `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`

Treat the shared trimmed output as:
- non-canonical
- not equivalent without further validation

## Related docs

- alignment summary:
  - [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_EXECUTION_SUMMARY_AND_INDEX.md`](ALIGNMENT_EXECUTION_SUMMARY_AND_INDEX.md)
- private alignment start note:
  - [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md`](ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md)
- shared follow-on setup:
  - [`Semester5/BIOL550/group_project/mouse/ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md`](ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md)
- GC follow-up note:
  - [`Semester5/BIOL550/group_project/mouse/GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md`](GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md)
