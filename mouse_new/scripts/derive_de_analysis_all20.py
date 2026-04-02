from __future__ import annotations

import base64
import io
import json
import math
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path("/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse_new")
DE_ROOT = ROOT / "differential_expression_all20"
FAMILY_TABLES = DE_ROOT / "family_drg_novaseqx" / "tables"
OUT_ROOT = DE_ROOT / "derived_analysis"

MAIN_CONTRASTS = ["ipsi_vs_contra_in_ff", "ipsi_vs_contra_in_cre"]
GENO_CONTRASTS = ["geno_in_contra", "geno_in_ipsi"]
ALL_CONTRASTS = MAIN_CONTRASTS + GENO_CONTRASTS + ["interaction"]
BENDPOINT_CONTRASTS = ALL_CONTRASTS


FAMILY_ROOT = DE_ROOT / "family_drg_novaseqx"
FAMILY_FIGURES = FAMILY_ROOT / "figures"
FAMILY_VST = FAMILY_TABLES / "vst_matrix.tsv"
FAMILY_SAMPLE_TABLE = FAMILY_TABLES / "sample_table.tsv"


def compute_pca_coordinates(vst: pd.DataFrame, sample_table: pd.DataFrame) -> pd.DataFrame:
    matrix = vst.set_index("gene_id")
    centered = matrix.sub(matrix.mean(axis=1), axis=0)
    samples_by_genes = centered.T.to_numpy()
    u, s, vt = np.linalg.svd(samples_by_genes, full_matrices=False)
    coords = u[:, :2] * s[:2]
    explained = (s**2) / np.sum(s**2)
    frame = sample_table.copy()
    frame["PC1"] = coords[:, 0]
    frame["PC2"] = coords[:, 1]
    frame["PC1_var_explained"] = explained[0] if len(explained) > 0 else np.nan
    frame["PC2_var_explained"] = explained[1] if len(explained) > 1 else np.nan
    return frame


def save_family_structure_outputs() -> pd.DataFrame:
    outdir = OUT_ROOT / "family_structure"
    ensure_dir(outdir)

    sample_table = pd.read_csv(FAMILY_SAMPLE_TABLE, sep="	")
    vst = pd.read_csv(FAMILY_VST, sep="	")
    coords = compute_pca_coordinates(vst, sample_table)
    coords.to_csv(outdir / "pca_side_genotype_coordinates.tsv", sep="	", index=False)

    color_map = {"ipsi": "#1f77b4", "contra": "#d62728"}
    marker_map = {"ff": "o", "cre": "s"}

    fig, ax = plt.subplots(figsize=(8, 6))
    for (_, row) in coords.iterrows():
        ax.scatter(
            row["PC1"],
            row["PC2"],
            s=90,
            color=color_map.get(row["side_class"], "#7f7f7f"),
            marker=marker_map.get(row["geno_class"], "o"),
            edgecolor="black",
            linewidth=0.5,
            alpha=0.9,
        )
        ax.text(row["PC1"] + 0.12, row["PC2"] + 0.12, row["srr"].replace("SRR", ""), fontsize=7)

    ax.set_xlabel(f"PC1 ({coords['PC1_var_explained'].iloc[0]*100:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({coords['PC2_var_explained'].iloc[0]*100:.1f}% variance)")
    ax.set_title("DRG family PCA: side color, genotype shape")

    from matplotlib.lines import Line2D
    legend_handles = [
        Line2D([0], [0], marker='o', color='w', label='ipsi', markerfacecolor=color_map['ipsi'], markeredgecolor='black', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='contra', markerfacecolor=color_map['contra'], markeredgecolor='black', markersize=8),
        Line2D([0], [0], marker='o', color='black', label='ff', markerfacecolor='white', markersize=8),
        Line2D([0], [0], marker='s', color='black', label='cre', markerfacecolor='white', markersize=8),
    ]
    ax.legend(handles=legend_handles, loc='best', frameon=True)
    fig.tight_layout()
    fig.savefig(outdir / "pca_side_genotype_annotated.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    collision_rows = []
    for side in sorted(coords["side_class"].unique()):
        subset = coords[coords["side_class"] == side].copy()
        ff = subset[subset["geno_class"] == "ff"]
        cre = subset[subset["geno_class"] == "cre"]
        for _, ff_row in ff.iterrows():
            for _, cre_row in cre.iterrows():
                dist = float(np.hypot(ff_row["PC1"] - cre_row["PC1"], ff_row["PC2"] - cre_row["PC2"]))
                collision_rows.append({
                    "side_class": side,
                    "ff_srr": ff_row["srr"],
                    "cre_srr": cre_row["srr"],
                    "pca_distance": dist,
                })
    if collision_rows:
        collisions = pd.DataFrame(collision_rows).sort_values("pca_distance")
        collisions.to_csv(outdir / "pca_ff_cre_collision_pairs.tsv", sep="	", index=False)
    return coords


def save_selection_comparison_plots(name: str, df: pd.DataFrame) -> None:
    outdir = OUT_ROOT / name
    ensure_dir(outdir)
    ranked = pd.read_csv(outdir / "ordered_pvalues_with_bendpoint.tsv", sep="	")
    selected_ids = set(ranked.loc[ranked["selected_by_bend"], "gene_id"].astype(str))
    working = df.copy()
    working = working.replace([np.inf, -np.inf], np.nan)
    working = working[working["pvalue"].notna()].copy()
    working["neglog10_pvalue"] = -np.log10(np.clip(working["pvalue"].astype(float), 1e-300, 1.0))
    working["abs_log2FoldChange"] = working["log2FoldChange"].abs()
    working["selection_class"] = np.where(
        working["gene_id"].astype(str).isin(selected_ids),
        "bend-point selected",
        np.where(working["padj"].fillna(1).lt(0.05), "padj < 0.05 only", "not selected"),
    )
    class_order = ["not selected", "padj < 0.05 only", "bend-point selected"]
    color_map = {
        "not selected": "#c7c7c7",
        "padj < 0.05 only": "#f0ad4e",
        "bend-point selected": "#d62728",
    }
    before_color_map = {
        "not significant": "#c7c7c7",
        "significant": "#b14a5c",
    }

    counts = working["selection_class"].value_counts().reindex(class_order, fill_value=0)
    before_counts = pd.Series(
        {
            "not significant": int((~working["padj"].fillna(1).lt(0.05)).sum()),
            "significant": int(working["padj"].fillna(1).lt(0.05).sum()),
        }
    )
    threshold = float(pd.read_csv(outdir / "bendpoint_summary.tsv", sep="	")["bend_pvalue_threshold"].iloc[0])
    bend_y = -np.log10(max(threshold, 1e-300))

    standalone_fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    for label in class_order:
        subset = working[working["selection_class"] == label]
        axes[0].scatter(
            subset["log2FoldChange"],
            subset["neglog10_pvalue"],
            s=10 if label == "not selected" else 16,
            alpha=0.45 if label == "not selected" else 0.8,
            c=color_map[label],
            label=label,
            edgecolors="none",
        )
    axes[0].axhline(bend_y, color="#2ca02c", linestyle="--", linewidth=1.2)
    axes[0].set_title(f"{name}: standalone volcano with threshold classes")
    axes[0].set_xlabel("log2 fold change")
    axes[0].set_ylabel("-log10(p-value)")
    axes[0].text(
        0.98,
        0.97,
        f"bend-point p = {threshold:.2e}\nselected = {int(counts['bend-point selected']):,}",
        transform=axes[0].transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "#2ca02c"},
    )
    axes[0].legend(frameon=True, fontsize=8)

    axes[1].bar(class_order, counts.values, color=[color_map[c] for c in class_order])
    axes[1].set_title(f"{name}: count change after bend-point filtering")
    axes[1].set_ylabel("genes")
    axes[1].tick_params(axis='x', rotation=18)
    ymax = max(counts.values) if len(counts.values) else 1
    for idx, val in enumerate(counts.values):
        axes[1].text(idx, val + max(ymax * 0.02, 1), f"{int(val):,}", ha="center", va="bottom", fontsize=9)
    axes[1].text(
        2,
        counts.values[2] + max(ymax * 0.08, 1),
        "core set after\nbend-point",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color="#b22222",
        fontweight="bold",
    )
    standalone_fig.tight_layout()
    standalone_png = outdir / "volcano_with_counts.png"
    standalone_fig.savefig(standalone_png, dpi=180, bbox_inches="tight")
    plt.close(standalone_fig)

    encoded = base64.b64encode(standalone_png.read_bytes()).decode("ascii")
    (outdir / "volcano_with_counts.html").write_text(
        "\n".join(
            [
                "<div style='font-family: Arial, sans-serif;'>",
                f"<img src='data:image/png;base64,{encoded}' style='max-width:100%; height:auto;' />",
                "</div>",
            ]
        )
    )

    comparison_fig, axes = plt.subplots(2, 2, figsize=(13.5, 9), height_ratios=[3.2, 1.6])
    before_sig = working["padj"].fillna(1).lt(0.05)
    axes[0, 0].scatter(
        working.loc[~before_sig, "log2FoldChange"],
        working.loc[~before_sig, "neglog10_pvalue"],
        s=10,
        alpha=0.35,
        c=before_color_map["not significant"],
        label="not significant",
        edgecolors="none",
    )
    axes[0, 0].scatter(
        working.loc[before_sig, "log2FoldChange"],
        working.loc[before_sig, "neglog10_pvalue"],
        s=12,
        alpha=0.8,
        c=before_color_map["significant"],
        label="padj < 0.05",
        edgecolors="none",
    )
    axes[0, 0].axhline(-np.log10(0.05), color="#7f7f7f", linestyle="--", linewidth=1.0)
    axes[0, 0].set_title(f"{name}: before bend-point")
    axes[0, 0].set_xlabel("log2 fold change")
    axes[0, 0].set_ylabel("-log10(p-value)")
    axes[0, 0].text(
        0.98,
        0.97,
        f"significant = {int(before_counts['significant']):,}",
        transform=axes[0, 0].transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": before_color_map["significant"]},
    )
    axes[0, 0].legend(frameon=True, fontsize=8)

    for label in class_order:
        subset = working[working["selection_class"] == label]
        axes[0, 1].scatter(
            subset["log2FoldChange"],
            subset["neglog10_pvalue"],
            s=10 if label == "not selected" else 16,
            alpha=0.45 if label == "not selected" else 0.8,
            c=color_map[label],
            label=label,
            edgecolors="none",
        )
    axes[0, 1].axhline(bend_y, color="#2ca02c", linestyle="--", linewidth=1.2)
    axes[0, 1].set_title(f"{name}: after bend-point")
    axes[0, 1].set_xlabel("log2 fold change")
    axes[0, 1].set_ylabel("-log10(p-value)")
    axes[0, 1].text(
        0.98,
        0.97,
        f"bend-point p = {threshold:.2e}\nselected = {int(counts['bend-point selected']):,}",
        transform=axes[0, 1].transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "#2ca02c"},
    )
    axes[0, 1].legend(frameon=True, fontsize=8)

    before_labels = list(before_counts.index)
    before_vals = before_counts.values
    axes[1, 0].bar(before_labels, before_vals, color=[before_color_map[x] for x in before_labels])
    axes[1, 0].set_title(f"{name}: counts before bend-point")
    axes[1, 0].set_ylabel("genes")
    axes[1, 0].tick_params(axis="x", rotation=16)
    before_ymax = max(before_vals) if len(before_vals) else 1
    for idx, val in enumerate(before_vals):
        axes[1, 0].text(idx, val + max(before_ymax * 0.02, 1), f"{int(val):,}", ha="center", va="bottom", fontsize=9)

    axes[1, 1].bar(class_order, counts.values, color=[color_map[c] for c in class_order])
    axes[1, 1].set_title(f"{name}: counts after bend-point")
    axes[1, 1].set_ylabel("genes")
    axes[1, 1].tick_params(axis="x", rotation=18)
    after_ymax = max(counts.values) if len(counts.values) else 1
    for idx, val in enumerate(counts.values):
        axes[1, 1].text(idx, val + max(after_ymax * 0.02, 1), f"{int(val):,}", ha="center", va="bottom", fontsize=9)

    comparison_fig.suptitle(f"{name}: before vs after bend-point filtering", fontsize=13, y=0.98)
    comparison_fig.tight_layout()
    comparison_fig.savefig(outdir / "before_after_selection_comparison.png", dpi=180, bbox_inches="tight")
    plt.close(comparison_fig)


def save_genotype_comparison_plots(geno_frames: dict[str, pd.DataFrame]) -> None:
    outdir = OUT_ROOT / "genotype_comparison"
    ensure_dir(outdir)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, name in zip(axes, ["geno_in_contra", "geno_in_ipsi"]):
        df = geno_frames[name].copy()
        df = df[df["pvalue"].notna()].copy()
        df["neglog10_pvalue"] = -np.log10(np.clip(df["pvalue"].astype(float), 1e-300, 1.0))
        df["sig"] = df["padj"].fillna(1).lt(0.05)
        ax.scatter(df.loc[~df["sig"], "log2FoldChange"], df.loc[~df["sig"], "neglog10_pvalue"], s=10, alpha=0.35, c="#bdbdbd", edgecolors="none")
        ax.scatter(df.loc[df["sig"], "log2FoldChange"], df.loc[df["sig"], "neglog10_pvalue"], s=12, alpha=0.8, c="#b14a5c", edgecolors="none")
        ax.set_title(name)
        ax.set_xlabel("log2 fold change")
        ax.set_ylabel("-log10(p-value)")
    fig.suptitle("Genotype contrasts: weaker is not zero")
    fig.tight_layout()
    fig.savefig(outdir / "geno_volcano_side_by_side.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    bins = np.linspace(-2.5, 2.5, 80)
    for name, color in [("geno_in_contra", "#1f77b4"), ("geno_in_ipsi", "#ff7f0e")]:
        vals = geno_frames[name]["log2FoldChange"].dropna().astype(float)
        ax.hist(vals, bins=bins, density=True, alpha=0.4, label=name, color=color)
    ax.set_title("Genotype effect-size distributions")
    ax.set_xlabel("log2 fold change")
    ax.set_ylabel("density")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(outdir / "geno_log2fc_density.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9), height_ratios=[3, 1.5])
    stats = []
    for col, name in enumerate(["geno_in_contra", "geno_in_ipsi"]):
        df = geno_frames[name].copy()
        df = df[df["pvalue"].notna()].copy()
        df["neglog10_pvalue"] = -np.log10(np.clip(df["pvalue"].astype(float), 1e-300, 1.0))
        df["sig"] = df["padj"].fillna(1).lt(0.05)
        sig_count = int(df["sig"].sum())
        nonsig_count = int((~df["sig"]).sum())
        stats.append((name, nonsig_count, sig_count))

        ax = axes[0, col]
        ax.scatter(df.loc[~df["sig"], "log2FoldChange"], df.loc[~df["sig"], "neglog10_pvalue"], s=10, alpha=0.35, c="#bdbdbd", edgecolors="none")
        ax.scatter(df.loc[df["sig"], "log2FoldChange"], df.loc[df["sig"], "neglog10_pvalue"], s=12, alpha=0.8, c="#b14a5c", edgecolors="none")
        ax.set_title(name)
        ax.set_xlabel("log2 fold change")
        ax.set_ylabel("-log10(p-value)")

    for col, (name, nonsig_count, sig_count) in enumerate(stats):
        ax = axes[1, col]
        ax.bar(["not significant", "significant"], [nonsig_count, sig_count], color=["#9ca3af", "#b14a5c"])
        ax.set_title(f"{name}: gene counts")
        ax.set_ylabel("genes")
        ax.tick_params(axis="x", rotation=18)
        ymax = max(nonsig_count, sig_count, 1)
        for idx, val in enumerate([nonsig_count, sig_count]):
            ax.text(idx, val + max(ymax * 0.03, 1), f"{val:,}", ha="center", va="bottom", fontsize=9)

    fig.suptitle("Genotype contrasts: side-by-side volcanoes and gene-count breakdowns")
    fig.tight_layout()
    fig.savefig(outdir / "geno_volcano_and_counts_grid.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    box_rows = []
    for name in ["geno_in_contra", "geno_in_ipsi"]:
        df = geno_frames[name].copy()
        df["sig"] = df["padj"].fillna(1).lt(0.05)
        for subset_name, subset in {
            "all tested genes": df,
            "padj < 0.05 genes": df[df["sig"]],
        }.items():
            vals = subset["log2FoldChange"].dropna().abs().astype(float)
            for val in vals.tolist():
                box_rows.append(
                    {
                        "contrast_id": name,
                        "subset": subset_name,
                        "abs_log2FoldChange": val,
                    }
                )
    box_df = pd.DataFrame(box_rows)
    box_df.to_csv(outdir / "geno_abs_log2fc_boxplot_source.tsv", sep="\t", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5))
    summary = pd.read_csv(outdir / "geno_in_contra_vs_geno_in_ipsi_summary.tsv", sep="\t")
    axes[0].bar(summary["contrast_id"], summary["significant_padj_lt_0_05"], color=["#1f77b4", "#ff7f0e"])
    axes[0].set_title("Significant-gene counts")
    axes[0].set_ylabel("genes")
    ymax = max(summary["significant_padj_lt_0_05"].max(), 1)
    for idx, val in enumerate(summary["significant_padj_lt_0_05"]):
        axes[0].text(idx, val + max(ymax * 0.03, 1), f"{int(val):,}", ha="center", va="bottom", fontsize=9)

    plotted = []
    labels = []
    colors = []
    for contrast, color in [("geno_in_contra", "#1f77b4"), ("geno_in_ipsi", "#ff7f0e")]:
        for subset in ["all tested genes", "padj < 0.05 genes"]:
            vals = box_df[(box_df["contrast_id"] == contrast) & (box_df["subset"] == subset)]["abs_log2FoldChange"].to_numpy()
            if len(vals):
                plotted.append(vals)
                labels.append(f"{contrast}\n{subset.replace(' genes', '')}")
                colors.append(color)
    bp = axes[1].boxplot(plotted, patch_artist=True, showfliers=False)
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)
    axes[1].set_title("Effect-size spread (zoom on genotype differences)")
    axes[1].set_ylabel("|log2 fold change|")
    axes[1].set_xticklabels(labels, rotation=18, ha="right")
    fig.suptitle("Genotype contrasts: counts plus effect-size zoom")
    fig.tight_layout()
    fig.savefig(outdir / "geno_counts_and_boxplot_zoom.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_contrast(name: str) -> pd.DataFrame:
    df = pd.read_csv(FAMILY_TABLES / f"{name}_full.tsv", sep="\t")
    df = df.replace([np.inf, -np.inf], np.nan)
    return df


def bend_threshold(df: pd.DataFrame) -> tuple[float, pd.DataFrame]:
    working = df[["gene_id", "pvalue", "padj", "log2FoldChange", "baseMean"]].copy()
    working = working[np.isfinite(working["pvalue"])].copy()
    working = working.sort_values("pvalue", kind="mergesort").reset_index(drop=True)
    working["rank"] = np.arange(1, len(working) + 1)
    working["rank_frac"] = (working["rank"] - 1) / max(len(working) - 1, 1)

    pvals = working["pvalue"].to_numpy()
    clipped = np.clip(pvals, 1e-300, 1.0)
    working["neglog10_pvalue"] = -np.log10(clipped)

    x = working["rank_frac"].to_numpy()
    y = working["neglog10_pvalue"].to_numpy()
    x1, y1 = x[0], y[0]
    x2, y2 = x[-1], y[-1]
    denom = math.hypot(y2 - y1, x2 - x1)
    if denom == 0:
        working["distance_to_line"] = 0.0
        idx = 0
    else:
        working["distance_to_line"] = np.abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / denom
        idx = int(working["distance_to_line"].idxmax())

    threshold = float(working.loc[idx, "pvalue"])
    working["selected_by_bend"] = working["pvalue"] <= threshold
    return threshold, working


def save_pvalue_outputs(name: str, df: pd.DataFrame) -> dict[str, float]:
    outdir = OUT_ROOT / name
    ensure_dir(outdir)

    threshold, ranked = bend_threshold(df)
    ranked.to_csv(outdir / "ordered_pvalues_with_bendpoint.tsv", sep="\t", index=False)

    selected = ranked[ranked["selected_by_bend"]].copy()
    selected.to_csv(outdir / "selected_genes_bendpoint.tsv", sep="\t", index=False)

    significant = int(df["padj"].fillna(1).lt(0.05).sum())
    selected_count = int(selected.shape[0])

    summary = pd.DataFrame(
        [
            {
                "contrast_id": name,
                "genes_tested": int(df["pvalue"].notna().sum()),
                "significant_padj_lt_0_05": significant,
                "bend_pvalue_threshold": threshold,
                "genes_below_bendpoint": selected_count,
            }
        ]
    )
    summary.to_csv(outdir / "bendpoint_summary.tsv", sep="\t", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(ranked["rank"], ranked["neglog10_pvalue"], color="#1f77b4", linewidth=1.5)
    bend_rank = int(ranked.loc[ranked["selected_by_bend"].idxmax(), "rank"]) if not selected.empty else 1
    axes[0].axvline(bend_rank, color="#d62728", linestyle="--", linewidth=1.5)
    axes[0].axvspan(1, bend_rank, color="#fdd0a2", alpha=0.25)
    axes[0].set_title(f"{name}: ordered p-values")
    axes[0].set_xlabel("Rank (smallest p-value to largest)")
    axes[0].set_ylabel("-log10(p-value)")
    axes[0].text(
        bend_rank,
        ranked["neglog10_pvalue"].max() * 0.95,
        f"bend rank = {bend_rank:,}\nthreshold = {threshold:.2e}",
        color="#b22222",
        fontsize=8.5,
        ha="right",
        va="top",
        bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "#d62728"},
    )

    axes[1].plot(ranked["pvalue"], ranked["rank"], color="#2ca02c", linewidth=1.5)
    axes[1].axvline(threshold, color="#d62728", linestyle="--", linewidth=1.5)
    axes[1].set_title(f"{name}: cumulative count by p-value")
    axes[1].set_xlabel("p-value")
    axes[1].set_ylabel("Cumulative genes")
    axes[1].set_xlim(left=0, right=min(0.5, max(0.05, float(ranked["pvalue"].quantile(0.95)))))
    axes[1].text(
        threshold,
        ranked["rank"].max() * 0.15,
        f"bend-point\np = {threshold:.2e}\nselected = {selected_count:,}",
        color="#b22222",
        fontsize=8.5,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "#d62728"},
    )

    fig.tight_layout()
    fig.savefig(outdir / "ordered_pvalue_and_cumulative_curve.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    return {
        "threshold": threshold,
        "significant": significant,
        "selected": selected_count,
    }


def save_top_gene_tables(name: str, df: pd.DataFrame) -> None:
    outdir = OUT_ROOT / name
    ensure_dir(outdir)

    valid = df[df["padj"].notna()].copy()
    top_padj = valid.sort_values(["padj", "pvalue", "gene_id"]).head(25)
    top_padj.to_csv(outdir / "top_genes_by_padj.tsv", sep="\t", index=False)

    valid["abs_log2FoldChange"] = valid["log2FoldChange"].abs()
    top_lfc = valid.sort_values(["abs_log2FoldChange", "padj"], ascending=[False, True]).head(25)
    top_lfc.to_csv(outdir / "top_genes_by_abs_log2fc.tsv", sep="\t", index=False)


def call_gprofiler(gene_ids: list[str]) -> list[dict]:
    payload = json.dumps(
        {
            "organism": "mmusculus",
            "query": gene_ids,
            "sources": ["GO:BP", "KEGG", "REAC"],
            "user_threshold": 0.05,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://biit.cs.ut.ee/gprofiler/api/gost/profile/",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        data = json.load(response)
    return data.get("result", [])


def save_enrichment(name: str, gene_ids: list[str], gene_set_label: str) -> None:
    outdir = OUT_ROOT / name
    ensure_dir(outdir)

    if not gene_ids:
        pd.DataFrame(
            [{"contrast_id": name, "gene_set_used": gene_set_label, "note": "No genes available for enrichment"}]
        ).to_csv(outdir / "gprofiler_enrichment.tsv", sep="\t", index=False)
        return

    results = call_gprofiler(gene_ids)
    if not results:
        pd.DataFrame(
            [{"contrast_id": name, "gene_set_used": gene_set_label, "note": "No enrichment results returned"}]
        ).to_csv(outdir / "gprofiler_enrichment.tsv", sep="\t", index=False)
        return

    frame = pd.DataFrame(results)
    keep = [
        "source",
        "native",
        "name",
        "p_value",
        "term_size",
        "query_size",
        "intersection_size",
        "effective_domain_size",
        "parents",
    ]
    frame = frame[keep].copy()
    frame.insert(0, "gene_set_used", gene_set_label)
    frame.insert(0, "contrast_id", name)
    frame.sort_values(["p_value", "source", "name"]).to_csv(outdir / "gprofiler_enrichment.tsv", sep="\t", index=False)

    top = frame.sort_values("p_value").head(12).copy()
    top = top.iloc[::-1]
    top["neglog10_p"] = -np.log10(np.clip(top["p_value"], 1e-300, 1.0))
    top["overlap_fraction"] = top["intersection_size"] / top["query_size"].replace(0, np.nan)
    source_colors = {"GO:BP": "#4c78a8", "KEGG": "#f58518", "REAC": "#54a24b"}

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["source"] + " | " + top["name"], top["neglog10_p"], color="#4c78a8")
    ax.set_xlabel("-log10(p-value)")
    ax.set_title(f"{name}: top enrichment terms")
    fig.tight_layout()
    fig.savefig(outdir / "gprofiler_top_terms.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"width_ratios": [1.2, 1]})
    axes[0].barh(
        top["source"] + " | " + top["name"],
        top["neglog10_p"],
        color=[source_colors.get(x, "#7f7f7f") for x in top["source"]],
    )
    axes[0].set_xlabel("-log10(p-value)")
    axes[0].set_title(f"{name}: strongest enrichment terms")

    y_positions = np.arange(len(top))
    axes[1].scatter(
        top["overlap_fraction"],
        y_positions,
        s=np.clip(top["intersection_size"] * 6, 40, 450),
        c=[source_colors.get(x, "#7f7f7f") for x in top["source"]],
        alpha=0.8,
        edgecolors="black",
        linewidths=0.4,
    )
    axes[1].set_yticks(y_positions)
    axes[1].set_yticklabels(top["name"])
    axes[1].set_xlabel("gene-set overlap fraction")
    axes[1].set_title(f"{name}: how much of the selected set each term covers")
    axes[1].grid(axis="x", alpha=0.25)
    for xpos, ypos, count in zip(top["overlap_fraction"], y_positions, top["intersection_size"]):
        axes[1].text(float(xpos) + 0.005, ypos, f"{int(count)} genes", va="center", fontsize=8)

    from matplotlib.lines import Line2D
    legend_handles = [
        Line2D([0], [0], marker="o", color="w", label=source, markerfacecolor=color, markeredgecolor="black", markersize=8)
        for source, color in source_colors.items()
        if source in set(top["source"])
    ]
    if legend_handles:
        axes[1].legend(handles=legend_handles, title="source", loc="lower right", frameon=True)
    fig.tight_layout()
    fig.savefig(outdir / "gprofiler_terms_and_overlap.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    source_summary = (
        frame.assign(neglog10_p=-np.log10(np.clip(frame["p_value"], 1e-300, 1.0)))
        .groupby("source", as_index=False)
        .agg(
            total_terms=("name", "count"),
            strongest_term_neglog10=("neglog10_p", "max"),
            median_overlap_fraction=("intersection_size", lambda s: float(np.median(s / frame.loc[s.index, "query_size"]))),
        )
        .sort_values("strongest_term_neglog10", ascending=False)
    )
    source_summary.to_csv(outdir / "gprofiler_source_summary.tsv", sep="\t", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(
        source_summary["source"],
        source_summary["total_terms"],
        color=[source_colors.get(x, "#7f7f7f") for x in source_summary["source"]],
    )
    axes[0].set_title(f"{name}: terms returned per source")
    axes[0].set_ylabel("enriched terms")
    for idx, val in enumerate(source_summary["total_terms"]):
        axes[0].text(idx, val + 0.5, f"{int(val)}", ha="center", va="bottom", fontsize=8)

    axes[1].bar(
        source_summary["source"],
        source_summary["strongest_term_neglog10"],
        color=[source_colors.get(x, "#7f7f7f") for x in source_summary["source"]],
    )
    axes[1].set_title(f"{name}: strongest signal by source")
    axes[1].set_ylabel("best -log10(p-value)")
    for idx, val in enumerate(source_summary["strongest_term_neglog10"]):
        axes[1].text(idx, val + max(source_summary["strongest_term_neglog10"].max() * 0.02, 0.5), f"{val:.1f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    fig.savefig(outdir / "gprofiler_source_summary.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def genotype_summary(geno_frames: dict[str, pd.DataFrame]) -> None:
    outdir = OUT_ROOT / "genotype_comparison"
    ensure_dir(outdir)

    rows = []
    for name, df in geno_frames.items():
        valid = df.copy()
        rows.append(
            {
                "contrast_id": name,
                "genes_tested": int(valid["padj"].notna().sum()),
                "significant_padj_lt_0_05": int(valid["padj"].fillna(1).lt(0.05).sum()),
                "top_abs_log2fc": float(valid["log2FoldChange"].abs().max()),
                "median_abs_log2fc": float(valid["log2FoldChange"].abs().median()),
            }
        )
    summary = pd.DataFrame(rows).sort_values("significant_padj_lt_0_05", ascending=False)
    summary.to_csv(outdir / "geno_in_contra_vs_geno_in_ipsi_summary.tsv", sep="\t", index=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(summary["contrast_id"], summary["significant_padj_lt_0_05"], color=["#1f77b4", "#ff7f0e"])
    ax.set_ylabel("Significant genes (padj < 0.05)")
    ax.set_title("Genotype contrasts: significance counts")
    fig.tight_layout()
    fig.savefig(outdir / "geno_significant_gene_counts.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_dir(OUT_ROOT)

    summaries = []
    geno_frames: dict[str, pd.DataFrame] = {}

    for contrast in ALL_CONTRASTS:
        df = load_contrast(contrast)
        save_top_gene_tables(contrast, df)

        if contrast in BENDPOINT_CONTRASTS:
            curve = save_pvalue_outputs(contrast, df)
            selected_ids = (
                pd.read_csv(OUT_ROOT / contrast / "selected_genes_bendpoint.tsv", sep="\t")["gene_id"].dropna().astype(str).tolist()
            )
            save_enrichment(contrast, selected_ids, "bend-point selected genes")
            summaries.append(
                {
                    "contrast_id": contrast,
                    "analysis_focus": (
                        "main_side_specific"
                        if contrast in MAIN_CONTRASTS
                        else "genotype" if contrast in GENO_CONTRASTS else "interaction"
                    ),
                    "significant_padj_lt_0_05": curve["significant"],
                    "bendpoint_selected": curve["selected"],
                    "bendpoint_threshold": curve["threshold"],
                }
            )

        if contrast in GENO_CONTRASTS:
            geno_frames[contrast] = df

    save_family_structure_outputs()
    genotype_summary(geno_frames)
    save_genotype_comparison_plots(geno_frames)
    for contrast in BENDPOINT_CONTRASTS:
        save_selection_comparison_plots(contrast, load_contrast(contrast))
    pd.DataFrame(summaries).to_csv(OUT_ROOT / "analysis_summary.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
