# Source-constrained RSS bend-point comparison

This output answers the stricter apples-to-apples question: after matching the source paper RSS genes to our DESeq2-tested universe, which source genes survive when the same local ordered-p-value bend-point rule is rerun inside that source-gene subset?

## Main count table

| metric | count | interpretation |
| --- | --- | --- |
| Source RSS genes found in our DESeq2-tested universe | 1025 | Matched source-paper RSS genes available for source-constrained bend-point selection. |
| WT/FF selected after source-constrained bend-point | 37 | Source RSS genes prioritized when the WT/FF bend-point rule is rerun inside the matched source-gene subset. |
| cKO/CRE selected after source-constrained bend-point | 53 | Source RSS genes prioritized when the cKO/CRE bend-point rule is rerun inside the matched source-gene subset. |
| Shared source-constrained WT/cKO selected genes | 32 | Source RSS genes selected by the source-constrained bend-point rule in both side-specific branches. |
| cKO-only source-constrained selected genes | 21 | Source RSS genes selected only under the cKO/CRE source-constrained branch. |
| WT-only source-constrained selected genes | 5 | Source RSS genes selected only under the WT/FF source-constrained branch. |
| Source-constrained selected genes also in original WT/FF bend-point | 37 | All WT/FF source-constrained selections are contained within the original full-universe WT/FF bend-point set. |
| Source-constrained selected genes also in original cKO/CRE bend-point | 45 | Most cKO/CRE source-constrained selections are also in the original full-universe cKO/CRE bend-point set. |
| cKO/CRE source-constrained selections outside original full cKO/CRE bend-point | 8 | Additional source RSS genes prioritized only after reranking within the source-gene subset. |
| Directionally consistent selected source RSS symbols | 55 | Selected source genes where sign(source RSS) agrees with sign(our local cKO-minus-WT log2FC delta). |
| Source-constrained selected genes appearing in retained GO terms | 46 | Selected source RSS gene IDs that appear in retained WT/FF or cKO/CRE GO/pathway membership tables. |

## Branch-level bend-point details

| branch | source_rss_gene_id_rows_ranked | source_rss_symbols_ranked | significant_padj_lt_0_05_within_source_subset | source_constrained_bend_pvalue_threshold | source_constrained_bend_rank | source_constrained_selected_gene_ids | source_constrained_selected_symbols | selected_up_log2fc_gt_0 | selected_down_log2fc_lt_0 | selected_positive_source_rss | selected_negative_source_rss | selected_direction_consistent_symbols | overlap_with_original_full_branch_bendpoint | selected_outside_original_full_branch_bendpoint |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WT/FF | 1027 | 1025 | 474 | 6.388e-19 | 37 | 37 | 37 | 36 | 1 | 26 | 11 | 35 | 37 | 0 |
| cKO/CRE | 1027 | 1025 | 578 | 3.018e-14 | 53 | 53 | 53 | 51 | 2 | 41 | 12 | 50 | 45 | 8 |

## Source-constrained RSS sign membership

| source_constrained_membership | positive | negative |
| --- | --- | --- |
| shared source-constrained bend-point | 25 | 7 |
| cKO-only source-constrained bend-point | 16 | 5 |
| WT-only source-constrained bend-point | 1 | 4 |
| tested source RSS, not source-constrained selected | 304 | 663 |
| not in our tested universe | 187 | 219 |

## Recommended figure set

| figure | role | what_it_shows | paper_use |
| --- | --- | --- | --- |
| source_rss_constrained_apples_to_apples_panel.png | Recommended main source-constrained comparison figure | The source RSS genes reranked by our bend-point process, then compared by branch overlap, RSS-like direction, and RSS sign membership. | Use to explain the stricter apples-to-apples method-level comparison. |
| source_rss_constrained_bendpoint_curves.png | Method figure | The exact bend-point selection curves for WT/FF and cKO/CRE after restricting to matched source RSS genes. | Use if reviewers/readers need to see how the source-constrained gene counts were generated. |
| source_rss_constrained_bendpoint_venn_style.png | Overlap figure | The source-constrained WT/cKO overlap and how each constrained set relates to the original full-universe bend-point sets. | Use to explain why the cKO source-constrained branch adds eight genes outside the original full cKO bend-point set. |
| source_rss_constrained_delta_scatter.png | Direction/agreement figure | Source RSS shifts against our local cKO-minus-WT delta, highlighting genes selected after source-constrained bend-point reranking. | Use to support the statement that selected source genes mostly preserve RSS-like direction. |
| source_rss_constrained_go_term_overlap_scatter.png | Pathway bridge figure | Retained GO terms that include source-constrained selected RSS genes. | Use to connect the method-level comparison back to pathway-level interpretation. |

## Interpretation

Within the 1,027 matched source RSS gene-id rows, rerunning the local bend-point rule selected 37 WT/FF genes and 53 cKO/CRE genes. These source-constrained sets shared 32 genes, with 21 cKO-only and 5 WT-only genes. The selected union contained 58 gene IDs, 55 of which were directionally consistent at the source-symbol level with the source RSS sign. This supports a stronger apples-to-apples claim than the first membership audit because the source-paper genes were passed through the same local bend-point narrowing process before comparison.