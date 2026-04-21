
## 2026-04-20 — HTSA_Paper methods/results completion pass

### Step
- Expanded `BIOL550-Project_Paper/HTSA_Paper.tex` to better meet the course draft requirements with additional Piter-owned Methods and Results content.
- Added a balanced 20-sample design table and a software/reference/version table to the Methods section.
- Added explicit bend-point-method explanation and new transition prose linking sample structure, branch-priority logic, and follow-up analysis.
- Added direct Results coverage for the `ipsi_vs_contra_in_cre` branch, including the 7,541-to-870 bend-point narrowing and the shared-core / cKO-extension interpretation.
- Added the ordered adjusted-p-value / cumulative curve figure to explain the bend-point rule more clearly.
- Restored local bibliography resolution in the paper repo and rebuilt `HTSA_Paper.pdf` and `HTSA_Paper.docx` from the updated LaTeX manuscript.
- Fixed `tooling/build_htsa_paper_docx.py` so it resolves the manuscript from the paper-repo root instead of assuming the script directory is the paper root.

### Finding
- The paper already had the main structure in place, but Methods was still too thin for a grad-level bioinformatics manuscript and Results underexplained the second main side-specific branch.
- The 870-gene cKO branch was already supported by validated local outputs and weekly reports, but it was not yet integrated clearly into the manuscript.
- The paper repo no longer had a top-level bibliography file, which prevented bibliography resolution until the file was restored locally.

### Decision
- Keep the paper centered on the side-specific injury signal, with WT as the clearest pathway showcase and cKO as the strongest supporting extension branch.
- Use only APA-formatted LaTeX citations for manuscript claims and rely on weekly reports as source material for validated wording and local-result interpretation, not as final evidentiary citations.
- Keep `main.tex` mirrored from `HTSA_Paper.tex` so the Overleaf compile target stays aligned with the main manuscript.

## 2026-04-20 — CRE/cKO branch follow-up notebook consolidated

### Step
- Added a new consolidated mining notebook for the `ipsi_vs_contra_in_cre` branch:
  - `mouse_new/notebooks/mining/mouse_differential_expression_cre_go_followup.ipynb`
- Recreated the useful structure from the older FF/WT GO follow-up notebook for the newer CRE/cKO branch:
  - PCA-first reminder
  - bend-point checkpoint
  - branch-size and direction summary
  - anchor-gene companion table
  - direction-split GO follow-up
  - ShinyGO-style CRE views
  - FF-vs-CRE overlap comparison
  - paper-ready summary export
- Generated branch summary support files from existing local outputs:
  - `mouse_new/preparation/DE-derived_analysis/ipsi_vs_contra_in_cre/cre_branch_direction_summary.tsv`
  - `mouse_new/preparation/DE-derived_analysis/ipsi_vs_contra_in_cre/anchor_genes_up_down.tsv`
  - `mouse_new/preparation/DE-derived_analysis/ipsi_vs_contra_in_cre/cre_pathway_theme_table.tsv`
  - `mouse_new/preparation/DE-derived_analysis/ipsi_vs_contra_in_cre/cre_followup_summary.md`
  - `mouse_new/preparation/DE-derived_analysis/ff_cre_branch_comparison/cre_followup_overlap_summary.tsv`

### Finding
- The CRE/cKO branch is already supported by existing local outputs and does not require a new dataset or a separate analysis path.
- The branch starts with 7,541 significant genes and narrows to 870 genes using the same ordered adjusted-p-value bend-point logic used for the 709-gene FF/WT branch.
- The narrowed FF and CRE branches share 620 genes, with 89 FF/WT-only genes and 250 CRE/cKO-only genes.

### Decision
- Treat the CRE/cKO branch as the main supporting extension of the side-specific injury story, while keeping FF/WT as the clearest pathway-level showcase.
- Use the new notebook as the single place for CRE/cKO follow-up interpretation instead of scattering the branch across several notebooks.
