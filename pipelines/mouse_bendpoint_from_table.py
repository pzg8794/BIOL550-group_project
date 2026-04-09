#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute a bend-point threshold from a ranked p-value table and save outputs."
    )
    parser.add_argument("--input", required=True, help="Input table path (.tsv or .csv).")
    parser.add_argument("--outdir", required=True, help="Directory where outputs will be written.")
    parser.add_argument("--name", default=None, help="Optional label used in the plot title and summary.")
    parser.add_argument("--gene-col", default="gene_id", help="Gene identifier column.")
    parser.add_argument("--p-col", default="pvalue", help="P-value column.")
    parser.add_argument("--padj-col", default="padj", help="Adjusted p-value column.")
    parser.add_argument("--lfc-col", default="log2FoldChange", help="Log2 fold-change column.")
    parser.add_argument("--basemean-col", default="baseMean", help="baseMean column.")
    parser.add_argument(
        "--sep",
        default=None,
        help="Column separator. Defaults to tab for .tsv/.txt, comma for .csv.",
    )
    return parser.parse_args()


def infer_sep(path: Path, sep: str | None) -> str:
    if sep is not None:
        return sep
    if path.suffix.lower() in {".tsv", ".txt"}:
        return "\t"
    return ","


def bend_threshold(frame: pd.DataFrame, gene_col: str, p_col: str, padj_col: str, lfc_col: str, basemean_col: str) -> tuple[float, pd.DataFrame]:
    required = [gene_col, p_col]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    working = pd.DataFrame(
        {
            "gene_id": frame[gene_col],
            "pvalue": pd.to_numeric(frame[p_col], errors="coerce"),
            "padj": pd.to_numeric(frame[padj_col], errors="coerce") if padj_col in frame.columns else np.nan,
            "log2FoldChange": pd.to_numeric(frame[lfc_col], errors="coerce") if lfc_col in frame.columns else np.nan,
            "baseMean": pd.to_numeric(frame[basemean_col], errors="coerce") if basemean_col in frame.columns else np.nan,
        }
    )
    working = working[np.isfinite(working["pvalue"])].copy()
    if working.empty:
        raise ValueError("No finite p-values were found in the input table.")

    working = working.sort_values("pvalue", kind="mergesort").reset_index(drop=True)
    working["rank"] = np.arange(1, len(working) + 1)
    working["rank_frac"] = (working["rank"] - 1) / max(len(working) - 1, 1)

    clipped = np.clip(working["pvalue"].to_numpy(), 1e-300, 1.0)
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


def save_outputs(frame: pd.DataFrame, outdir: Path, name: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    threshold, ranked = bend_threshold(frame, "gene_id", "pvalue", "padj", "log2FoldChange", "baseMean")

    ranked.to_csv(outdir / "ordered_pvalues_with_bendpoint.tsv", sep="\t", index=False)
    selected = ranked[ranked["selected_by_bend"]].copy()
    selected.to_csv(outdir / "selected_genes_bendpoint.tsv", sep="\t", index=False)

    significant = int(ranked["padj"].fillna(1).lt(0.05).sum()) if "padj" in ranked else 0
    selected_count = int(selected.shape[0])
    bend_rank = int(ranked.loc[ranked["selected_by_bend"].idxmax(), "rank"]) if selected_count else 1

    summary = pd.DataFrame(
        [
            {
                "contrast_id": name,
                "genes_tested": int(ranked.shape[0]),
                "significant_padj_lt_0_05": significant,
                "bend_pvalue_threshold": threshold,
                "genes_below_bendpoint": selected_count,
                "bend_rank": bend_rank,
            }
        ]
    )
    summary.to_csv(outdir / "bendpoint_summary.tsv", sep="\t", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(ranked["rank"], ranked["neglog10_pvalue"], color="#1f77b4", linewidth=1.5)
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


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    outdir = Path(args.outdir).expanduser().resolve()
    sep = infer_sep(input_path, args.sep)
    frame = pd.read_csv(input_path, sep=sep)

    rename_map = {
        args.gene_col: "gene_id",
        args.p_col: "pvalue",
    }
    if args.padj_col in frame.columns:
        rename_map[args.padj_col] = "padj"
    if args.lfc_col in frame.columns:
        rename_map[args.lfc_col] = "log2FoldChange"
    if args.basemean_col in frame.columns:
        rename_map[args.basemean_col] = "baseMean"
    frame = frame.rename(columns=rename_map)

    name = args.name or input_path.stem
    save_outputs(frame, outdir, name)
    print(f"Bend-point outputs written to {outdir}")


if __name__ == "__main__":
    main()
