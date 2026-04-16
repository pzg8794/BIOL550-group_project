# HTSA Paper Asset Inventory

This file is the quick-share inventory for figures and tables that are already available from the `mouse_new` notebook workflow and are most useful for the HTSA paper.

## Main paper candidates

### Quality control

- **Adapter content before/after trimming**
  - Source notebook: `mouse_new/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse_new.ipynb`
  - Shareable paper asset: `mouse_new/paper/assets_htsa/qc_adapter_pre_post.png`
  - Upstream data support:
    - `mouse_new/qc_analysis_raw_vs_trimmed/fastqc_module_counts_compare_and_delta.csv`
    - `mouse_new/qc_analysis_raw_vs_trimmed/fastqc_severity_delta_by_report.csv`

- **FastQC module status heatmap**
  - Source notebook: `mouse_new/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse_new.ipynb`
  - Asset: `mouse_new/qc_analysis_raw_vs_trimmed/fastqc_module_status_heatmap_raw_vs_trimmed.png`

- **QC severity delta by SRR**
  - Source notebook: `mouse_new/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse_new.ipynb`
  - Asset: `mouse_new/qc_analysis_raw_vs_trimmed/fastqc_severity_delta_by_srr.png`

### Alignment and sample structure

- **PCA of the 20-sample DRG cohort**
  - Source notebook: `mouse_new/notebooks/mouse_differential_expression_all20.ipynb`
  - Paper asset: `mouse_new/paper/assets_htsa/results_pca.png`
  - Alternate annotated version: `mouse_new/differential_expression_all20/derived_analysis/family_structure/pca_side_genotype_annotated.png`

- **Sample-to-sample distance heatmap**
  - Source notebook: `mouse_new/notebooks/mouse_differential_expression_all20.ipynb`
  - Paper asset: `mouse_new/paper/assets_htsa/results_sample_distance_heatmap.png`
  - Alternate source path: `mouse_new/differential_expression_all20/family_drg_novaseqx/figures/sample_distance_heatmap.png`

- **Unique mapping summary**
  - Source notebook: `mouse_new/notebooks/mouse_alignment_analysis_star_all20.ipynb`
  - Paper assets:
    - `mouse_new/paper/assets_htsa/alignment_unique_mapping_bar.png`
    - `mouse_new/paper/assets_htsa/alignment_unique_mapping_box.png`

### Differential expression and bend-point narrowing

- **Volcano + bend-point comparison for the main FF branch**
  - Source notebook: `mouse_new/notebooks/mouse_differential_expression_all20.ipynb`
  - Paper asset: `mouse_new/paper/assets_htsa/results_bendpoint_volcano.png`
  - Closest upstream summary:
    - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/before_after_selection_comparison.png`
    - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/ordered_pvalue_and_cumulative_curve.png`

- **Ordered adjusted-p-value curve (FF)**
  - Source notebook: `mouse_new/notebooks/mouse_differential_expression_all20.ipynb`
  - Asset: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/ordered_pvalue_and_cumulative_curve.png`

- **Bend-point summary tables**
  - FF: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/bendpoint_summary.tsv`
  - CRE: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/bendpoint_summary.tsv`

### GO / pathway interpretation

- **Composite GO figure used in the HTSA paper draft**
  - Source notebooks:
    - `mouse_new/notebooks/mouse_differential_expression_ff_go_followup.ipynb`
    - `mouse_new/notebooks/mouse_differential_expression_ff_shinygo_style.ipynb`
  - Paper asset: `mouse_new/paper/assets_htsa/results_go_composite.png`

- **FF upregulated GO network with GO IDs**
  - Source notebook: `mouse_new/notebooks/mouse_differential_expression_ff_shinygo_style.ipynb`
  - Asset: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/shinygo_style/ff_up_network_view.png`

- **FF GO tree / chart / grouped views**
  - Tree: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/shinygo_style/ff_up_tree_view.png`
  - Chart: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/shinygo_style/ff_up_chart_view.png`
  - Groups: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/shinygo_style/ff_up_groups_view.png`

- **CRE matching network view**
  - Source notebook family: CRE GO follow-up outputs
  - Asset: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/shinygo_style_shared/cre_up_network_view.png`

## Strong supporting / comparison figures

- **WT vs cKO overlap summaries**
  - `mouse_new/differential_expression_all20/derived_analysis/ff_cre_branch_comparison/wt_cko_gene_overlap_venn_style.png`
  - `mouse_new/differential_expression_all20/derived_analysis/ff_cre_branch_comparison/wt_cko_shared_go_term_scatter.png`

- **FF vs CRE overlap summaries**
  - `mouse_new/differential_expression_all20/derived_analysis/ff_cre_branch_comparison/ff_cre_gene_overlap_venn_style.png`
  - `mouse_new/differential_expression_all20/derived_analysis/ff_cre_branch_comparison/ff_cre_shared_go_term_scatter.png`

- **Genotype comparison panel set**
  - `mouse_new/differential_expression_all20/derived_analysis/genotype_comparison/geno_volcano_and_counts_grid.png`
  - `mouse_new/differential_expression_all20/derived_analysis/genotype_comparison/geno_volcano_side_by_side.png`
  - `mouse_new/differential_expression_all20/derived_analysis/genotype_comparison/geno_significant_gene_counts.png`
  - `mouse_new/differential_expression_all20/derived_analysis/genotype_comparison/geno_log2fc_density.png`

## Tables most useful to share directly

- **Global sample / design tables**
  - `mouse_new/differential_expression_all20/family_drg_novaseqx/tables/sample_table.tsv`
  - `mouse_new/differential_expression_all20/tables/mouse_de_design_table.tsv`
  - `mouse_new/differential_expression_all20/tables/contrast_manifest.tsv`

- **Primary DE result tables**
  - `mouse_new/differential_expression_all20/family_drg_novaseqx/tables/ipsi_vs_contra_in_ff_significant.tsv`
  - `mouse_new/differential_expression_all20/family_drg_novaseqx/tables/ipsi_vs_contra_in_cre_significant.tsv`
  - `mouse_new/differential_expression_all20/family_drg_novaseqx/tables/ipsi_vs_contra_in_ff_top_genes.tsv`
  - `mouse_new/differential_expression_all20/family_drg_novaseqx/tables/ipsi_vs_contra_in_cre_top_genes.tsv`

- **FF branch selected-gene tables**
  - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/selected_genes_bendpoint.tsv`
  - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/selected_genes_bendpoint_gene_symbols.tsv`
  - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/top_genes_by_padj.tsv`
  - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/top_genes_by_abs_log2fc.tsv`

- **CRE branch selected-gene tables**
  - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/selected_genes_bendpoint.tsv`
  - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/top_genes_by_padj.tsv`
  - `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/top_genes_by_abs_log2fc.tsv`

- **GO enrichment tables**
  - FF: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/gprofiler_enrichment.tsv`
  - FF up: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/gprofiler_enrichment_up.tsv`
  - FF down: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/gprofiler_enrichment_down.tsv`
  - CRE: `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/gprofiler_enrichment.tsv`

## Easiest package to send the team right now

If we only want to send the cleanest, most paper-ready set tonight, start with:

1. `mouse_new/paper/assets_htsa/qc_adapter_pre_post.png`
2. `mouse_new/paper/assets_htsa/alignment_unique_mapping_bar.png`
3. `mouse_new/paper/assets_htsa/alignment_unique_mapping_box.png`
4. `mouse_new/paper/assets_htsa/results_pca.png`
5. `mouse_new/paper/assets_htsa/results_sample_distance_heatmap.png`
6. `mouse_new/paper/assets_htsa/results_bendpoint_volcano.png`
7. `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/shinygo_style/ff_up_network_view.png`
8. `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/shinygo_style/ff_up_tree_view.png`
9. `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/shinygo_style_shared/cre_up_network_view.png`
10. `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_ff/bendpoint_summary.tsv`
11. `mouse_new/differential_expression_all20/derived_analysis/ipsi_vs_contra_in_cre/bendpoint_summary.tsv`
12. `mouse_new/differential_expression_all20/family_drg_novaseqx/tables/sample_table.tsv`
