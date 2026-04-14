# Methods truth audit — 2026-04-13

Canonical source checked:
- `/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse_new/paper/methods-improved.tex`
- Source map / version roles: `methods_source_map_2026-04-13.md`

Primary validation sources:
- `mouse_new/reference/SRP618841/metadata/mouse_de_design_table.tsv`
- `mouse_new/differential_expression_all20/derived_analysis/analysis_summary.tsv`
- `mouse_new/differential_expression_all20/derived_analysis/*/bendpoint_summary.tsv`
- `mouse_new` weekly reports from 2026-04-02 and 2026-04-09

## Validated facts kept
- Dataset lineage: `SRP618841` / `PRJNA1322439` / `GSE243308`
- Active subset: 20 DRG NovaSeq X libraries at 1 dpi after sciatic nerve injury, balanced across `ipsi_ff`, `ipsi_cre`, `contra_ff`, `contra_cre`
- DE design formula: `~ side_class + geno_class + side_class:geno_class`
- Tested-gene reduction: `78,334 -> 21,481`
- Contrast order and priority:
  - primary: `ipsi_vs_contra_in_ff`, `ipsi_vs_contra_in_cre`
  - supporting: `geno_in_contra`, `geno_in_ipsi`
  - contextual: `interaction`
- Bend-point counts:
  - `ipsi_vs_contra_in_ff`: `7,023 -> 709`, threshold `1.37401793656806e-17`
  - `ipsi_vs_contra_in_cre`: `7,541 -> 870`, threshold `8.3968379571549e-17`
- Alignment summary retained from the validated weekly-report path:
  - median unique mapping `93.24%`
  - median multi-mapping `5.10%`
  - median `noFeature` `~3.82%`
  - median `ambiguous` `~1.77%`

## Resolved mismatches
- Normalized the final stage name to **Data Analysis and Interpretation** across Methods prose, captions, and asset-generation code.
- Removed stale figure wording such as `Retained project artifact` and reduced internal workflow-style labels.
- Replaced `project metadata` phrasing in figure-generation code with manuscript-facing language (`accession records`, `design tables`, `design fields`).
- Updated the Word mirror builder to use `methods-improved.tex` as the canonical source instead of the older `materials_methods_piter_draft.tex`.
- Resolved the accession conflict in the manuscript-facing sources by moving the validated lineage to `PRJNA1322439` and leaving `PRJNA1017789` as a historical snapshot in the reference bundle.
- Corrected the injury-model label from spinal cord injury to sciatic nerve injury / peripheral axotomy terminology in the manuscript-facing sources and validation notebook.

## Writing decisions locked
- Methods keeps the four-stage workflow.
- PCA is described as the first structure check, not as a Results-style interpretation block.
- GO follow-up is described as a downstream analytical layer; biological meaning stays for Results/Discussion.
- Weekly reports are used to confirm contrast priority and workflow maturity, not copied as report-style prose.
