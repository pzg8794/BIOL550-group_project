# Methods Source Map - 2026-04-13

This note keeps the manuscript versions and the evidence sources separated so the Methods section has one canonical home.

## Canonical rule

- The manuscript master is [methods-improved.tex](methods-improved.tex).
- The only accepted factual backing is the validated `mouse_new` data and results already recorded in the audit note and validation hub.
- Older drafts are mirrors or working copies, not independent sources of truth.

## Manuscript inventory

| File | What it is about | Duplicate / overlap | Richness | Status |
| --- | --- | --- | --- | --- |
| [methods-improved.tex](methods-improved.tex) | Current validated Methods manuscript for the `mouse_new` paper. Contains the normalized stage names, validated numbers, and the tightest prose. | Overlaps with both `materials_methods_piter_draft` files, but has the newest audit-aligned wording. | Richest validated manuscript. | Canonical master |
| [materials_methods_piter_draft.tex](materials_methods_piter_draft.tex) | Older, more ornate Methods draft with more presentation scaffolding and extra narrative. | Largely duplicates the same Methods structure; should be treated as a working mirror. | Richer than the pandoc export, but not the master. | Secondary draft |
| [materials_methods_piter_draft_pandoc.tex](materials_methods_piter_draft_pandoc.tex) | Leaner export-oriented version of the same draft, likely used for Pandoc or Word conversion. | Duplicates the piter draft with lighter formatting and slightly less prose. | Leanest manuscript variant. | Delivery mirror |
| [methods_truth_audit_2026-04-13.md](methods_truth_audit_2026-04-13.md) | Validation ledger for the confirmed Methods values and the resolved mismatches. | Overlaps with the notebook validation hub, but only as a factual log. | Richest exact-number record. | Validation source |
| [transcript_digest_for_methods_and_claim.md](transcript_digest_for_methods_and_claim.md) | Claim-selection and interpretation guardrails for the paper. | Overlaps with strategy docs, not with data files. | Rule sheet, not a manuscript. | Support only |
| [PAPER_DRAFTING_STRATEGY.md](PAPER_DRAFTING_STRATEGY.md) and [HTSA_Paper.md](HTSA_Paper.md) | High-level paper planning, story structure, and mind maps. | Overlap is conceptual only. | Useful for structure, not for facts. | Planning only |

## Evidence inventory

| Source | What it supplies to Methods | Notes |
| --- | --- | --- |
| [../reference/SRP618841/metadata/mouse_de_design_table.tsv](../reference/SRP618841/metadata/mouse_de_design_table.tsv) | Accession lineage, sample groups, and the 2x2 design table | Source for the dataset description and sample organization |
| [../differential_expression_all20/derived_analysis/analysis_summary.tsv](../differential_expression_all20/derived_analysis/analysis_summary.tsv) | Gene filtering and the contrast list | Source for tested-gene reduction and model setup |
| `../differential_expression_all20/derived_analysis/*/bendpoint_summary.tsv` | Bend-point thresholds and follow-up gene counts | Source for the reduced follow-up sets |
| [../notebooks/mouse_alignment_analysis_star_all20.ipynb](../notebooks/mouse_alignment_analysis_star_all20.ipynb) | STAR alignment summary metrics | Source for mapping quality values |
| [../notebooks/mouse_new_methods_validation_hub.ipynb](../notebooks/mouse_new_methods_validation_hub.ipynb) | Subsection-by-subsection validation trail | Source for proving each Methods claim points to an artifact |
| `mouse_new` weekly reports from 2026-04-02 and 2026-04-09 | Supportive workflow confirmation | Useful for priority, not for primary numerical claims |

## Fixed values

- Dataset lineage: `SRP618841` / `PRJNA1322439` / `GSE243308`
- Working subset: 20 NovaSeq X DRG libraries at 1 dpi after sciatic nerve injury, balanced 5 per subgroup
- Design formula: `~ side_class + geno_class + side_class:geno_class`
- Filtered genes: `78,334 -> 21,481`
- Alignment median: unique `93.24%`, multi `5.10%`, noFeature `~3.82%`, ambiguous `~1.77%`
- Bend-point follow-up sets: `ipsi_vs_contra_in_ff = 7,023 -> 709`; `ipsi_vs_contra_in_cre = 7,541 -> 870`
- Historical snapshot retained in the reference bundle: `../reference/SRP618841/html/bioproject_PRJNA1017789.html`

## Editing rule

- If a new factual claim is needed, update `methods-improved.tex` first.
- If a mirror needs to stay in sync, copy only the validated text and numbers from the canonical master.
- Do not pull facts from planning docs when a validated `mouse_new` artifact already exists.