# Transcript digest for Methods and paper claim

This digest pulls only the paper-relevant method and interpretation rules from the existing transcript summaries.

## Method rules we are adopting
- **PCA first:** sample structure should be checked before strong gene-level or pathway-level claims are made.
- **Bend-point over arbitrary top-N:** large DE result sets should be narrowed with the ordered-p-value / cumulative-curve bend-point method rather than an arbitrary cutoff beyond `padj < 0.05`.
- **Consistent contrast logic:** the same selection logic should be used across contrasts so story selection is not inconsistent from one branch to another.
- **Pathway follow-up comes after gene-list narrowing:** GO / KEGG / Reactome interpretation should use the narrowed bend-point gene sets rather than the full unstructured DE lists.
- **QC remains a checkpoint, not a paper story by itself:** FastQC / MultiQC / trimming / alignment metrics support the credibility of downstream interpretation but do not replace the main biological signal.

## Interpretation constraints we should respect
- **Intrinsic structure before biology claims:** PCA baseline structure must be described before DE or GO interpretation.
- **Primary vs supporting branches must stay explicit:** the side-specific contrasts are the main analytical branches, while genotype-focused contrasts remain supporting or contextual.
- **GO terms are redundant:** overlapping labels should not be written as independent biological discoveries.
- **Direction matters:** pathway interpretation should respect asymmetry between upregulated and downregulated branches where that asymmetry is present.
- **Pathways should stay gene-supported:** pathway wording should remain connected to the underlying gene set instead of standing alone as a claim.

## Phrases or habits to avoid
- Avoid presenting `padj < 0.05` alone as the final follow-up logic.
- Avoid writing GO output as if every enriched term represents a separate biological story.
- Avoid skipping from QC directly to pathway interpretation without the PCA / DE / bend-point sequence.
- Avoid over-centering weaker genotype or interaction branches when the side-specific signal is stronger.
- Avoid report-style phrasing such as “this week we did…” inside the paper draft.

## Source summaries used
- `2026-03-31 Team Meeting_ RNA-seq NovaSeq 6000 Analysis, Presentation Prep, and Course Participation Decision-summary.md`
- `2026-04-01 Navigating Data Overload in Gene Expression Analysis_ Pivoting from Arbitrary Cutoffs to a P-Value Distribution Method-summary.md`
- `2026-02-26 Analysis of RNA-Seq Quality Control and Methodology Verification-summary.md`
