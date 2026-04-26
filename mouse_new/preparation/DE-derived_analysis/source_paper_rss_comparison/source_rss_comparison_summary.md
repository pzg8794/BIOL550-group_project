# Source-paper RSS gene-set comparison

Nature article: https://www.nature.com/articles/s41586-026-10295-z

This output compares Nature Supplementary Table 5 RSS genes against the local `mouse_new` DESeq2, bend-point, and retained GO follow-up outputs.

## Paper-ready count table

| metric                                        |   count | interpretation                                                                                                       |
|:----------------------------------------------|--------:|:---------------------------------------------------------------------------------------------------------------------|
| Source-paper AhR/RSS-prioritized genes        |    1431 | Genes identified by the source paper using |RSS| >= 0.3 in Supplementary Table 5.                                    |
| Found in our DESeq2-tested gene universe      |    1025 | Confirms identifier matching/overlap with the count matrix used for our DESeq2 side-specific contrasts.              |
| Significant in our WT side-specific contrast  |     473 | Source-paper RSS genes with adjusted p-value support in our WT/FF ipsilateral-vs-contralateral branch.               |
| Significant in our cKO side-specific contrast |     577 | Source-paper RSS genes with adjusted p-value support in our CRE/cKO ipsilateral-vs-contralateral branch.             |
| Present in WT bend-point set                  |      43 | Source-paper RSS genes recovered in the 709-gene WT/FF bend-point follow-up set.                                     |
| Present in cKO bend-point set                 |      45 | Source-paper RSS genes recovered in the 870-gene CRE/cKO bend-point follow-up set.                                   |
| Present in WT/cKO shared 620-gene set         |      34 | RSS genes that fall in the shared injury-response backbone retained by both bend-point branches.                     |
| Present in cKO-only 250-gene set              |      11 | RSS genes that may support cKO-specific interpretation beyond the shared injury-response core.                       |
| Present in WT-only 89-gene set                |       9 | RSS genes that appear only in the WT/FF bend-point follow-up subset.                                                 |
| Directionally consistent with RSS sign        |     987 | Matched genes where sign(source RSS) agrees with sign(our cKO/CRE log2FC minus our WT/FF log2FC).                    |
| Appearing in retained GO follow-up terms      |      47 | RSS genes that appear in at least one retained g:Profiler/GO membership table used for pathway-level interpretation. |
| Appearing in anchor-gene follow-up tables     |       3 | RSS genes that overlap the branch-level anchor-gene tables used to explain leading signals.                          |

## Direction breakdown

| source_rss_sign   |   source_genes |   found_in_our_universe |   wt_bendpoint |   cko_bendpoint |   shared_bendpoint |   cko_only_bendpoint |   wt_only_bendpoint |   direction_consistent |   in_go_terms |
|:------------------|---------------:|------------------------:|---------------:|----------------:|-------------------:|---------------------:|--------------------:|-----------------------:|--------------:|
| negative          |            898 |                     679 |             14 |               9 |                  7 |                    2 |                   7 |                    662 |            13 |
| positive          |            533 |                     346 |             29 |              36 |                 27 |                    9 |                   2 |                    325 |            34 |

## Interpretation guardrail

This is a direct gene-set comparison, not proof that our pipeline reproduces the source paper exactly. The source study used RSS over PL-DEGs, whereas this project used DESeq2 side-specific contrasts, bend-point narrowing, and retained GO memberships. The appropriate paper claim is that the source-paper RSS set is largely present in our tested universe, only partly retained by bend-point follow-up, and strongest as a validation/interpretation bridge rather than a replacement for our pathway-level analysis.

## Checklist status

OPEN / IN PROGRESS - The real analysis table has now been generated, but the manuscript item should remain open until a Results/Discussion paragraph is inserted and reviewed in the paper draft.