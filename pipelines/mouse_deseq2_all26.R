#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(DESeq2)
  library(ggplot2)
  library(pheatmap)
  library(RColorBrewer)
})

args <- commandArgs(trailingOnly = TRUE)
arg_value <- function(flag, default = NULL) {
  idx <- match(flag, args)
  if (is.na(idx) || idx == length(args)) default else args[[idx + 1]]
}

counts_path <- arg_value("--counts", "/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/alignment_analysis_star_all26/tables/mouse_star_gene_counts_reverse_stranded.tsv")
meta_path <- arg_value("--meta", "/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/alignment_analysis_star_all26/tables/mouse_alignment_sample_summary.tsv")
out_dir <- arg_value("--outdir", "/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/differential_expression_all26")

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
tables_dir <- file.path(out_dir, "tables")
dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)

write_tsv <- function(df, path) {
  write.table(df, path, sep = "\t", quote = FALSE, row.names = FALSE)
}

safe_slug <- function(x) {
  gsub("[^A-Za-z0-9_]+", "_", x)
}

counts_df <- read.delim(counts_path, check.names = FALSE)
meta_df <- read.delim(meta_path, check.names = FALSE, stringsAsFactors = FALSE)

count_matrix <- as.matrix(counts_df[, -1, drop = FALSE])
rownames(count_matrix) <- counts_df$gene_id
storage.mode(count_matrix) <- "integer"

meta_df$source_class <- ifelse(grepl("neurons", meta_df$group_label, ignore.case = TRUE), "neurons", "tissue")
meta_df$platform_family <- meta_df$platform_short
meta_df$geno_class <- ifelse(grepl("Conditional Knockout", meta_df$group_label), "cko", "control")
meta_df$condition_family <- ifelse(
  grepl(", injury", meta_df$group_label),
  "injury",
  ifelse(
    grepl(", ipsilateral", meta_df$group_label),
    "ipsilateral_sham",
    ifelse(
      grepl(", contralateral", meta_df$group_label),
      "contralateral_sham",
      ifelse(grepl("neurons", meta_df$group_label, ignore.case = TRUE), "neuron_culture", "naive")
    )
  )
)

meta_df$family_id <- ifelse(
  meta_df$source_class == "tissue" & meta_df$platform_family == "NovaSeq 6000" & meta_df$condition_family %in% c("naive", "injury"),
  "family_tissue_novaseq6000",
  ifelse(
    meta_df$source_class == "tissue" & meta_df$platform_family == "NovaSeq X" & meta_df$condition_family %in% c("ipsilateral_sham", "contralateral_sham"),
    "family_tissue_sham_novaseqx",
    ifelse(
      meta_df$source_class == "neurons" & meta_df$platform_family == "NovaSeq X" & meta_df$condition_family == "neuron_culture",
      "family_neurons_novaseqx",
      NA_character_
    )
  )
)

meta_df$include_in_de <- !is.na(meta_df$family_id)
meta_df$excluded_reason <- ifelse(meta_df$include_in_de, "", "No valid DE family")
meta_df <- meta_df[match(colnames(count_matrix), meta_df$srr), ]
stopifnot(identical(meta_df$srr, colnames(count_matrix)))

design_export <- meta_df[, c(
  "srr", "sample_title", "group_label", "source_name", "platform_family", "source_class",
  "geno_class", "condition_family", "family_id", "gc_status", "sex", "genotype", "treatment",
  "include_in_de", "excluded_reason"
)]
write_tsv(design_export, file.path(tables_dir, "mouse_de_design_table.tsv"))

contrast_manifest <- list()
family_manifest <- list()

save_plot_png <- function(path, width = 8, height = 6, expr) {
  png(path, width = width, height = height, units = "in", res = 200)
  on.exit(dev.off(), add = TRUE)
  force(expr)
}

make_volcano <- function(res_df, title, out_path) {
  plot_df <- res_df
  plot_df$neglog10_padj <- -log10(pmax(plot_df$padj, 1e-300))
  plot_df$significant <- ifelse(!is.na(plot_df$padj) & plot_df$padj <= 0.05, "padj <= 0.05", "not significant")
  p <- ggplot(plot_df, aes(x = log2FoldChange, y = neglog10_padj, color = significant)) +
    geom_point(alpha = 0.55, size = 1.1) +
    scale_color_manual(values = c("padj <= 0.05" = "#b14a5c", "not significant" = "grey65")) +
    labs(title = title, x = "log2 fold change", y = "-log10 adjusted p-value", color = NULL) +
    theme_bw(base_size = 12) +
    theme(legend.position = "top")
  ggsave(out_path, plot = p, width = 8, height = 6, dpi = 200)
}

make_pca_plot <- function(vsd, family_meta, title, out_path) {
  mat <- t(assay(vsd))
  pca <- prcomp(mat, scale. = FALSE)
  percent_var <- round(100 * (pca$sdev^2 / sum(pca$sdev^2)), 1)
  pca_df <- data.frame(
    sample = rownames(pca$x),
    PC1 = pca$x[, 1],
    PC2 = pca$x[, 2],
    geno_class = family_meta$geno_class,
    condition_family = family_meta$condition_family
  )
  p <- ggplot(pca_df, aes(x = PC1, y = PC2, color = geno_class, shape = condition_family, label = sample)) +
    geom_point(size = 3.2, alpha = 0.9) +
    labs(
      title = title,
      x = paste0("PC1 (", percent_var[1], "%)"),
      y = paste0("PC2 (", percent_var[2], "%)")
    ) +
    theme_bw(base_size = 12)
  ggsave(out_path, plot = p, width = 8, height = 6, dpi = 200)
}

make_distance_heatmap <- function(vsd, family_meta, title, out_path) {
  dmat <- as.matrix(dist(t(assay(vsd))))
  anno <- data.frame(
    genotype = family_meta$geno_class,
    condition = family_meta$condition_family,
    row.names = family_meta$srr
  )
  save_plot_png(out_path, width = 8, height = 7, expr = {
    pheatmap(
      dmat,
      annotation_col = anno,
      annotation_row = anno,
      color = colorRampPalette(rev(brewer.pal(9, "Blues")))(100),
      main = title
    )
  })
}

make_gene_heatmap <- function(vsd, family_meta, genes, title, out_path) {
  if (length(genes) < 2) {
    return(FALSE)
  }
  mat <- assay(vsd)[genes, , drop = FALSE]
  mat_scaled <- t(scale(t(mat)))
  mat_scaled[is.na(mat_scaled)] <- 0
  anno <- data.frame(
    genotype = family_meta$geno_class,
    condition = family_meta$condition_family,
    row.names = family_meta$srr
  )
  save_plot_png(out_path, width = 9, height = 10, expr = {
    pheatmap(
      mat_scaled,
      annotation_col = anno,
      color = colorRampPalette(rev(brewer.pal(11, "RdBu")))(100),
      main = title,
      show_rownames = TRUE,
      fontsize_row = 7
    )
  })
  TRUE
}

get_interaction_coef <- function(dds) {
  rn <- resultsNames(dds)
  hit <- grep("^condition_family.*\\.geno_class", rn, value = TRUE)
  if (length(hit) != 1) stop("Could not identify unique interaction coefficient")
  hit
}

run_contrast <- function(dds, vsd, family_id, family_meta, contrast_id, contrast_label, result_spec, out_base) {
  if (result_spec$type == "coef") {
    res <- results(dds, name = result_spec$name)
    result_method <- paste("coef:", result_spec$name)
  } else if (result_spec$type == "list") {
    res <- results(dds, contrast = list(result_spec$names))
    result_method <- paste("list:", paste(result_spec$names, collapse = " + "))
  } else {
    stop("Unknown result specification type")
  }

  res_df <- as.data.frame(res)
  res_df$gene_id <- rownames(res_df)
  res_df <- res_df[, c("gene_id", "baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj")]
  res_df <- res_df[order(ifelse(is.na(res_df$padj), Inf, res_df$padj), ifelse(is.na(res_df$pvalue), Inf, res_df$pvalue)), ]
  sig_df <- subset(res_df, !is.na(padj) & padj <= 0.05)
  top_df <- head(if (nrow(sig_df) > 0) sig_df else subset(res_df, !is.na(pvalue)), 25)

  write_tsv(res_df, paste0(out_base, "_full.tsv"))
  write_tsv(sig_df, paste0(out_base, "_significant.tsv"))
  write_tsv(top_df, paste0(out_base, "_top_genes.tsv"))

  make_volcano(res_df, contrast_label, paste0(out_base, "_volcano.png"))
  save_plot_png(paste0(out_base, "_ma.png"), width = 7, height = 6, expr = {
    plotMA(res, ylim = c(-8, 8), main = contrast_label)
  })

  heatmap_genes <- head(if (nrow(sig_df) >= 2) sig_df$gene_id else subset(res_df, !is.na(pvalue))$gene_id, 30)
  heatmap_ok <- make_gene_heatmap(vsd, family_meta, heatmap_genes, paste0(contrast_label, " — top genes"), paste0(out_base, "_heatmap.png"))

  contrast_manifest[[length(contrast_manifest) + 1]] <<- data.frame(
    family_id = family_id,
    contrast_id = contrast_id,
    contrast_label = contrast_label,
    result_method = result_method,
    n_tested = sum(!is.na(res_df$pvalue)),
    n_significant = nrow(sig_df),
    full_table = paste0(out_base, "_full.tsv"),
    sig_table = paste0(out_base, "_significant.tsv"),
    top_table = paste0(out_base, "_top_genes.tsv"),
    volcano_png = paste0(out_base, "_volcano.png"),
    ma_png = paste0(out_base, "_ma.png"),
    heatmap_png = if (heatmap_ok) paste0(out_base, "_heatmap.png") else "",
    stringsAsFactors = FALSE
  )
}

run_family <- function(family_id, family_label, subset_expr, condition_levels, geno_levels, design_formula, min_samples_for_count, contrast_builder) {
  family_meta <- subset(meta_df, eval(parse(text = subset_expr)))
  family_meta <- family_meta[order(family_meta$condition_family, family_meta$geno_class, family_meta$srr), ]
  family_counts <- count_matrix[, family_meta$srr, drop = FALSE]
  keep <- rowSums(family_counts >= 10) >= min_samples_for_count
  filtered_counts <- family_counts[keep, , drop = FALSE]

  family_dir <- file.path(out_dir, family_id)
  family_tables <- file.path(family_dir, "tables")
  family_figures <- file.path(family_dir, "figures")
  dir.create(family_tables, recursive = TRUE, showWarnings = FALSE)
  dir.create(family_figures, recursive = TRUE, showWarnings = FALSE)

  family_meta$condition_family <- factor(family_meta$condition_family, levels = condition_levels)
  family_meta$geno_class <- factor(family_meta$geno_class, levels = geno_levels)
  rownames(family_meta) <- family_meta$srr

  dds <- DESeqDataSetFromMatrix(
    countData = round(filtered_counts),
    colData = family_meta,
    design = design_formula
  )
  dds <- DESeq(dds)
  vsd <- vst(dds, blind = FALSE)

  write_tsv(
    family_meta[, c("srr", "sample_title", "geno_class", "condition_family", "platform_family", "gc_status")],
    file.path(family_tables, "sample_table.tsv")
  )
  write_tsv(
    data.frame(
      family_id = family_id,
      family_label = family_label,
      samples_total = ncol(family_counts),
      genes_before_filter = nrow(family_counts),
      genes_after_filter = nrow(filtered_counts),
      min_samples_count_ge_10 = min_samples_for_count
    ),
    file.path(family_tables, "filtering_summary.tsv")
  )
  write_tsv(
    data.frame(sample = names(sizeFactors(dds)), size_factor = sizeFactors(dds)),
    file.path(family_tables, "size_factors.tsv")
  )
  write_tsv(
    data.frame(result_name = resultsNames(dds)),
    file.path(family_tables, "results_names.tsv")
  )
  norm_df <- data.frame(gene_id = rownames(dds), counts(dds, normalized = TRUE), check.names = FALSE)
  vst_df <- data.frame(gene_id = rownames(vsd), assay(vsd), check.names = FALSE)
  write_tsv(norm_df, file.path(family_tables, "normalized_counts.tsv"))
  write_tsv(vst_df, file.path(family_tables, "vst_matrix.tsv"))

  save_plot_png(file.path(family_figures, "dispersion.png"), width = 7, height = 6, expr = {
    plotDispEsts(dds, main = paste(family_label, "dispersion"))
  })
  make_pca_plot(vsd, family_meta, paste(family_label, "PCA"), file.path(family_figures, "pca.png"))
  make_distance_heatmap(vsd, family_meta, paste(family_label, "sample distance"), file.path(family_figures, "sample_distance_heatmap.png"))

  contrast_builder(dds, vsd, family_meta, family_tables, family_figures)

  family_manifest[[length(family_manifest) + 1]] <<- data.frame(
    family_id = family_id,
    family_label = family_label,
    samples_total = ncol(family_counts),
    genes_before_filter = nrow(family_counts),
    genes_after_filter = nrow(filtered_counts),
    design = deparse(design_formula),
    stringsAsFactors = FALSE
  )
}

run_family(
  family_id = "family_tissue_novaseq6000",
  family_label = "Tissue / NovaSeq 6000 / naive vs injury",
  subset_expr = "family_id == 'family_tissue_novaseq6000'",
  condition_levels = c("naive", "injury"),
  geno_levels = c("control", "cko"),
  design_formula = ~ condition_family + geno_class + condition_family:geno_class,
  min_samples_for_count = 3,
  contrast_builder = function(dds, vsd, family_meta, family_tables, family_figures) {
    coef_geno <- grep("^geno_class_", resultsNames(dds), value = TRUE)
    coef_cond <- grep("^condition_family_", resultsNames(dds), value = TRUE)
    coef_inter <- get_interaction_coef(dds)
    run_contrast(dds, vsd, "family_tissue_novaseq6000", family_meta, "geno_in_naive", "Genotype effect in naive tissue (CKO vs control)", list(type = "coef", name = coef_geno), file.path(family_tables, "geno_in_naive"))
    run_contrast(dds, vsd, "family_tissue_novaseq6000", family_meta, "geno_in_injury", "Genotype effect in injury tissue (CKO vs control)", list(type = "list", names = c(coef_geno, coef_inter)), file.path(family_tables, "geno_in_injury"))
    run_contrast(dds, vsd, "family_tissue_novaseq6000", family_meta, "injury_in_control", "Injury effect in control tissue", list(type = "coef", name = coef_cond), file.path(family_tables, "injury_in_control"))
    run_contrast(dds, vsd, "family_tissue_novaseq6000", family_meta, "injury_in_cko", "Injury effect in CKO tissue", list(type = "list", names = c(coef_cond, coef_inter)), file.path(family_tables, "injury_in_cko"))
    run_contrast(dds, vsd, "family_tissue_novaseq6000", family_meta, "interaction", "Interaction term: extra injury effect in CKO tissue", list(type = "coef", name = coef_inter), file.path(family_tables, "interaction"))
  }
)

run_family(
  family_id = "family_tissue_sham_novaseqx",
  family_label = "Tissue / NovaSeq X / ipsilateral vs contralateral sham",
  subset_expr = "family_id == 'family_tissue_sham_novaseqx'",
  condition_levels = c("contralateral_sham", "ipsilateral_sham"),
  geno_levels = c("control", "cko"),
  design_formula = ~ condition_family + geno_class + condition_family:geno_class,
  min_samples_for_count = 2,
  contrast_builder = function(dds, vsd, family_meta, family_tables, family_figures) {
    coef_geno <- grep("^geno_class_", resultsNames(dds), value = TRUE)
    coef_cond <- grep("^condition_family_", resultsNames(dds), value = TRUE)
    coef_inter <- get_interaction_coef(dds)
    run_contrast(dds, vsd, "family_tissue_sham_novaseqx", family_meta, "geno_in_contralateral_sham", "Genotype effect in contralateral sham tissue (CKO vs control)", list(type = "coef", name = coef_geno), file.path(family_tables, "geno_in_contralateral_sham"))
    run_contrast(dds, vsd, "family_tissue_sham_novaseqx", family_meta, "geno_in_ipsilateral_sham", "Genotype effect in ipsilateral sham tissue (CKO vs control)", list(type = "list", names = c(coef_geno, coef_inter)), file.path(family_tables, "geno_in_ipsilateral_sham"))
    run_contrast(dds, vsd, "family_tissue_sham_novaseqx", family_meta, "ipsilateral_vs_contralateral_in_control", "Ipsilateral vs contralateral sham effect in control tissue", list(type = "coef", name = coef_cond), file.path(family_tables, "ipsilateral_vs_contralateral_in_control"))
    run_contrast(dds, vsd, "family_tissue_sham_novaseqx", family_meta, "ipsilateral_vs_contralateral_in_cko", "Ipsilateral vs contralateral sham effect in CKO tissue", list(type = "list", names = c(coef_cond, coef_inter)), file.path(family_tables, "ipsilateral_vs_contralateral_in_cko"))
    run_contrast(dds, vsd, "family_tissue_sham_novaseqx", family_meta, "interaction", "Interaction term: extra sham-side effect in CKO tissue", list(type = "coef", name = coef_inter), file.path(family_tables, "interaction"))
  }
)

run_family(
  family_id = "family_neurons_novaseqx",
  family_label = "Neurons / NovaSeq X / genotype effect",
  subset_expr = "family_id == 'family_neurons_novaseqx'",
  condition_levels = c("neuron_culture"),
  geno_levels = c("control", "cko"),
  design_formula = ~ geno_class,
  min_samples_for_count = 3,
  contrast_builder = function(dds, vsd, family_meta, family_tables, family_figures) {
    coef_geno <- grep("^geno_class_", resultsNames(dds), value = TRUE)
    run_contrast(dds, vsd, "family_neurons_novaseqx", family_meta, "geno_in_neurons", "Genotype effect in neuron culture (CKO vs control)", list(type = "coef", name = coef_geno), file.path(family_tables, "geno_in_neurons"))
  }
)

contrast_manifest_df <- do.call(rbind, contrast_manifest)
family_manifest_df <- do.call(rbind, family_manifest)

write_tsv(family_manifest_df, file.path(tables_dir, "family_manifest.tsv"))
write_tsv(contrast_manifest_df, file.path(tables_dir, "contrast_manifest.tsv"))

cat("Output directory:", out_dir, "\n")
cat("Families completed:", nrow(family_manifest_df), "\n")
cat("Contrasts completed:", nrow(contrast_manifest_df), "\n")
