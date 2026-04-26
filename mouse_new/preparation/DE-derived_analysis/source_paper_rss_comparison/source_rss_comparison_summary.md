# Source-paper RSS gene-set comparison

Nature article: https://www.nature.com/articles/s41586-026-10295-z

This output compares Nature Supplementary Table 5 RSS genes against the local `mouse_new` DESeq2, bend-point, and retained GO follow-up outputs.

## Why this revision uses more than one figure

The first count-only plot was useful as an audit, but it did not make the source-study-versus-local-workflow comparison easy to understand. The revised figure set follows the transcript guidance to keep the story focused, compare at gene-support level where possible, and use only visuals that clarify the interpretation.

## Paper-ready count table

| metric | count | interpretation |
| --- | --- | --- |
| Source-paper AhR/RSS-prioritized genes | 1431 | Genes identified by the source paper using |RSS| >= 0.3 in Supplementary Table 5. |
| Found in our DESeq2-tested gene universe | 1025 | Confirms identifier matching/overlap with the count matrix used for our DESeq2 side-specific contrasts. |
| Significant in our WT side-specific contrast | 473 | Source-paper RSS genes with adjusted p-value support in our WT/FF ipsilateral-vs-contralateral branch. |
| Significant in our cKO side-specific contrast | 577 | Source-paper RSS genes with adjusted p-value support in our CRE/cKO ipsilateral-vs-contralateral branch. |
| Present in WT bend-point set | 43 | Source-paper RSS genes recovered in the 709-gene WT/FF bend-point follow-up set. |
| Present in cKO bend-point set | 45 | Source-paper RSS genes recovered in the 870-gene CRE/cKO bend-point follow-up set. |
| Present in WT/cKO shared 620-gene set | 34 | RSS genes that fall in the shared injury-response backbone retained by both bend-point branches. |
| Present in cKO-only 250-gene set | 11 | RSS genes that may support cKO-specific interpretation beyond the shared injury-response core. |
| Present in WT-only 89-gene set | 9 | RSS genes that appear only in the WT/FF bend-point follow-up subset. |
| Directionally consistent with RSS sign | 987 | Matched genes where sign(source RSS) agrees with sign(our cKO/CRE log2FC minus our WT/FF log2FC). |
| Appearing in retained GO follow-up terms | 47 | RSS genes that appear in at least one retained g:Profiler/GO membership table used for pathway-level interpretation. |
| Appearing in anchor-gene follow-up tables | 3 | RSS genes that overlap the branch-level anchor-gene tables used to explain leading signals. |

## Direction breakdown

| source_rss_sign | source_genes | found_in_our_universe | wt_bendpoint | cko_bendpoint | shared_bendpoint | cko_only_bendpoint | wt_only_bendpoint | direction_consistent | in_go_terms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| negative | 898 | 679 | 14 | 9 | 7 | 2 | 7 | 662 | 13 |
| positive | 533 | 346 | 29 | 36 | 27 | 9 | 2 | 325 | 34 |

## Recommended figure set

| figure | role | what_it_shows | paper_use |
| --- | --- | --- | --- |
| source_rss_apples_to_apples_comparison_panel.png | Recommended main comparison figure | Source control/cKO/RSS values against our WT/cKO DESeq2 values, plus bend-point overlap in one compact panel. | Use when explaining direct validation of the pathway-level framework against source-paper RSS genes. |
| source_rss_bendpoint_venn_style.png | Overlap explanation figure | How source RSS genes overlap WT/FF and cKO/CRE bend-point follow-up sets. | Use if the paper needs a simpler visual than the full multi-panel comparison. |
| source_rss_membership_matrix.png | Interpretation matrix | Where positive and negative RSS genes land: shared bend-point, branch-specific bend-point, significant-only, tested-only, or unmatched. | Use in discussion/supporting material to explain why the comparison is meaningful but not a full reproduction. |
| source_rss_go_term_overlap_scatter.png | Pathway-level bridge | Which non-generic retained GO/pathway terms contain source-paper RSS genes and how concentrated that support is. | Use when connecting source-study stress/growth themes to our retained GO interpretation. |
| source_rss_overlap_counts.png | Audit/check figure | Simple count recovery across workflow stages. | Keep as a sanity-check output; not recommended as the main paper figure. |

## Agreement statistics

| comparison | n_gene_id_rows | pearson_r | spearman_r | directional_agreement_fraction | directionally_consistent_symbols |
| --- | --- | --- | --- | --- | --- |
| Source control log2FC vs our WT/FF log2FC | 1027 | 0.9738 | 0.9636 |  |  |
| Source cKO log2FC vs our cKO/CRE log2FC | 1027 | 0.9786 | 0.9627 |  |  |
| Source RSS shift vs our cKO-minus-WT log2FC delta | 1027 | 0.941 | 0.9162 |  |  |
| RSS sign agreement among matched source symbols | 1025 |  |  | 0.9629 | 987.0 |

## Branch-membership matrix

| analysis_membership | positive | negative |
| --- | --- | --- |
| shared WT/cKO bend-point | 27 | 7 |
| cKO-only bend-point | 9 | 2 |
| WT-only bend-point | 2 | 7 |
| DE-significant outside bend-point | 225 | 544 |
| tested, not significant | 83 | 119 |
| not in our tested universe | 187 | 219 |

## Interpretation guardrail

This is a direct gene-set comparison, not proof that our pipeline reproduces the source paper exactly. The source study used RSS over PL-DEGs, whereas this project used DESeq2 side-specific contrasts, bend-point narrowing, and retained GO memberships. The appropriate paper claim is that the source-paper RSS set is largely present in our tested universe, directionally consistent with our RSS-like cKO-minus-WT delta for most matched genes, only partly retained by bend-point follow-up, and strongest as a validation/interpretation bridge rather than a replacement for our pathway-level analysis.

## Checklist status

OPEN / IN PROGRESS - The real analysis table and comparison figures have now been generated, but the manuscript item should remain open until a Results/Discussion paragraph is inserted and reviewed in the paper draft.