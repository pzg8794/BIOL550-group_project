from __future__ import annotations

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
    axes[0].set_title(f"{name}: ordered p-values")
    axes[0].set_xlabel("Rank (smallest p-value to largest)")
    axes[0].set_ylabel("-log10(p-value)")

    axes[1].plot(ranked["pvalue"], ranked["rank"], color="#2ca02c", linewidth=1.5)
    axes[1].axvline(threshold, color="#d62728", linestyle="--", linewidth=1.5)
    axes[1].set_title(f"{name}: cumulative count by p-value")
    axes[1].set_xlabel("p-value")
    axes[1].set_ylabel("Cumulative genes")
    axes[1].set_xlim(left=0, right=min(0.5, max(0.05, float(ranked["pvalue"].quantile(0.95)))))

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

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["source"] + " | " + top["name"], top["neglog10_p"], color="#4c78a8")
    ax.set_xlabel("-log10(p-value)")
    ax.set_title(f"{name}: top enrichment terms")
    fig.tight_layout()
    fig.savefig(outdir / "gprofiler_top_terms.png", dpi=180, bbox_inches="tight")
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

    genotype_summary(geno_frames)
    pd.DataFrame(summaries).to_csv(OUT_ROOT / "analysis_summary.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
