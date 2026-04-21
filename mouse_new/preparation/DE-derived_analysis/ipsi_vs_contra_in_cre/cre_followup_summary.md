# CRE/cKO side-specific follow-up summary

- Branch: `ipsi_vs_contra_in_cre`.
- Origin: same 20-sample DRG DESeq2 model used for the FF/WT branch.
- Generation: same ordered adjusted-p-value bend-point procedure used for `ipsi_vs_contra_in_ff`.
- Full significant branch size: 870 selected after bend-point; see `bendpoint_summary.tsv` for full branch details.
- Direction split in selected set: 785 upregulated and 85 downregulated genes.
- FF/CRE overlap: 620 shared genes, 89 FF/WT-only genes, and 250 CRE/cKO-only genes.
- Interpretation: the CRE branch supports the same side-specific injury-response backbone while expanding the follow-up set under the cKO background.

Useful generated files:
- `cre_branch_direction_summary.tsv`
- `anchor_genes_up_down.tsv`
- `cre_pathway_theme_table.tsv`
- `cre_followup_overlap_summary.tsv`
