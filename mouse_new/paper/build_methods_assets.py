#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib import patches
from matplotlib.gridspec import GridSpec
from PIL import Image


PAPER_DIR = Path(__file__).resolve().parent
ROOT = PAPER_DIR.parent
ASSET_DIR = PAPER_DIR / "assets_methods"

QC_DIR = ROOT / "qc_analysis_raw_vs_trimmed"
ALIGN_DIR = Path(
    "/Users/pitergarcia/DataScience/Semester5/BIOL550/mouse_group_project_work/data/alignment_analysis_star_all20"
)
DE_DIR = ROOT / "differential_expression_all20"

STAGE_COLORS = {
    "collect": "#365C8D",
    "clean": "#2E7D6E",
    "prep": "#C97A2B",
    "mine": "#7B4FA0",
}
LIGHT_COLORS = {
    "collect": "#EAF1F8",
    "clean": "#E8F4F1",
    "prep": "#FBF1E4",
    "mine": "#F1E9F8",
}
SIDE_COLORS = {"ipsi": "#1F77B4", "contra": "#FF7F0E"}
GENO_COLORS = {"ff": "#2CA02C", "cre": "#D62728"}
TEXT_DARK = "#1F1F1F"
GRID = "#D9D9D9"


def ensure_assets_dir() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)


def load_image(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"))


def rounded_panel(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    edgecolor: str,
    facecolor: str = "white",
    lw: float = 1.8,
    radius: float = 0.02,
):
    panel = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        linewidth=lw,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(panel)
    return panel


def add_card(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    color: str,
    title: str,
    body: str,
    title_size: int = 17,
    body_size: int = 12,
):
    rounded_panel(ax, x, y, w, h, edgecolor=color, facecolor="#FCFCFC", lw=1.9, radius=0.024)
    ax.add_patch(
        patches.Rectangle((x, y + h * 0.72), w, h * 0.28, linewidth=0, facecolor=color)
    )
    ax.add_patch(
        patches.Rectangle((x, y), w, h * 0.09, linewidth=0, facecolor=color)
    )
    ax.text(
        x + w / 2,
        y + h * 0.86,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color="white",
    )
    ax.text(
        x + w / 2,
        y + h * 0.38,
        body,
        ha="center",
        va="center",
        fontsize=body_size,
        color=TEXT_DARK,
        linespacing=1.34,
    )


def add_stage_banner(
    ax,
    title: str,
    subtitle: str,
    color: str,
    *,
    y: float = 0.89,
    h: float = 0.075,
    title_x: float = 0.18,
    subtitle_x: float = 0.955,
    title_size: float = 15.4,
    subtitle_size: float = 10.0,
):
    rounded_panel(ax, 0.02, y, 0.96, h, edgecolor=color, facecolor="white", lw=0)
    ax.add_patch(
        patches.FancyBboxPatch(
            (0.02, y),
            0.96,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            linewidth=0,
            edgecolor=color,
            facecolor=color,
        )
    )
    y_center = y + h * 0.5
    ax.text(
        title_x,
        y_center,
        title,
        ha="left",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color="white",
    )
    ax.text(
        subtitle_x,
        y_center,
        subtitle,
        ha="right",
        va="center",
        fontsize=subtitle_size,
        color="white",
    )


def add_panel_title(ax, text: str, color: str) -> None:
    ax.text(
        0.02,
        1.02,
        text,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=13.8,
        fontweight="bold",
        color="white",
        bbox={
            "facecolor": color,
            "edgecolor": color,
            "boxstyle": "round,pad=0.28,rounding_size=0.06",
        },
        zorder=10,
    )


def save_figure(fig: plt.Figure, filename: str, dpi: int = 220) -> None:
    fig.savefig(
        ASSET_DIR / filename,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )
    plt.close(fig)


def build_overview() -> None:
    fig, ax = plt.subplots(figsize=(16, 5.8))
    ax.set_axis_off()
    add_stage_banner(
        ax,
        "Mouse DRG RNA-seq pipeline",
        "Overview rebuilt from project-defined stage outputs",
        STAGE_COLORS["collect"],
    )

    cards = [
        (
            "collect",
            "Data Collection",
            "SRP618841 / PRJNA1017789\nGSE243308\n20 paired-end SRRs retained\nbalanced side × genotype\ndesign",
        ),
        (
            "clean",
            "Data Cleaning",
            "FastQC + MultiQC baseline\nfastp v0.23.2 trimming\npost-trim QC checkpoint",
        ),
        (
            "prep",
            "Data Preparation",
            "GRCm39 + Ensembl v115\nSTAR index and\npaired-end alignment\nBAM + GeneCounts handoff",
        ),
        (
            "mine",
            "Data Analysis\n& Interpretation",
            "DESeq2 modeling\nbend-point narrowing\ng:Profiler summaries",
        ),
    ]
    w = 0.21
    h = 0.56
    gap = 0.04
    x0 = 0.02
    y = 0.20
    x_positions = [x0 + idx * (w + gap) for idx in range(len(cards))]

    for (stage_key, title, body), x in zip(cards, x_positions, strict=True):
        title_size = 18 if stage_key != "mine" else 16.5
        body_size = 12.5 if stage_key != "mine" else 12.5
        add_card(
            ax,
            x,
            y,
            w,
            h,
            color=STAGE_COLORS[stage_key],
            title=title,
            body=body,
            title_size=title_size,
            body_size=body_size,
        )

    arrow_style = dict(
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=2.0,
        color="#7A7A7A",
    )
    arrow_y = 0.48
    arrow_pad = 0.007
    for idx in range(len(x_positions) - 1):
        ax.add_patch(
            patches.FancyArrowPatch(
                (x_positions[idx] + w + arrow_pad, arrow_y),
                (x_positions[idx + 1] - arrow_pad, arrow_y),
                transform=ax.transAxes,
                **arrow_style,
            )
        )

    ax.text(
        0.5,
        0.09,
        "Public accessions and metadata → cleaned read pairs → count-ready alignments → contrast tables and enrichment products",
        ha="center",
        va="center",
        fontsize=12.5,
        color=TEXT_DARK,
    )
    save_figure(fig, "overview_pipeline_stage.png")


def build_data_collection() -> None:
    sample_table = pd.read_csv(
        DE_DIR / "family_drg_novaseqx" / "tables" / "sample_table.tsv",
        sep="\t",
    )
    grouped = (
        sample_table.sort_values("srr")
        .groupby(["geno_class", "side_class"])["srr"]
        .apply(list)
        .to_dict()
    )

    fig, ax = plt.subplots(figsize=(16, 7.0))
    ax.set_axis_off()
    add_stage_banner(
        ax,
        "Data Collection",
        "Rebuilt from project metadata and the saved design tables",
        STAGE_COLORS["collect"],
    )

    provenance_x = [0.05, 0.27, 0.49, 0.71]
    provenance = [
        ("SRA study", "SRP618841"),
        ("BioProject", "PRJNA1017789"),
        ("GEO series", "GSE243308"),
        ("Local subset", "20 SRRs retained"),
    ]
    for idx, ((title, body), x) in enumerate(zip(provenance, provenance_x, strict=True)):
        add_card(ax, x, 0.62, 0.19, 0.18, color=STAGE_COLORS["collect"], title=title, body=body, title_size=15, body_size=14)
        if idx < len(provenance_x) - 1:
            ax.add_patch(
                patches.FancyArrowPatch(
                    (x + 0.19, 0.71),
                    (provenance_x[idx + 1] - 0.01, 0.71),
                    transform=ax.transAxes,
                    arrowstyle="-|>",
                    mutation_scale=16,
                    linewidth=1.8,
                    color="#7A7A7A",
                )
            )

    add_card(
        ax,
        0.05,
        0.34,
        0.36,
        0.18,
        color=STAGE_COLORS["collect"],
        title="Acquisition handoff",
        body="paired-end FASTQ.gz files\nrun manifest + design table\nNovaSeq X / DRG / 1 dpi",
        title_size=15,
        body_size=13,
    )
    add_card(
        ax,
        0.05,
        0.10,
        0.36,
        0.17,
        color=STAGE_COLORS["collect"],
        title="Metadata fields carried forward",
        body="srr • sample_title • side_class • geno_class\ncondition_family • family_id • include_in_de",
        title_size=15,
        body_size=12.5,
    )

    rounded_panel(ax, 0.48, 0.10, 0.47, 0.42, edgecolor=STAGE_COLORS["collect"], facecolor="white")
    ax.text(0.505, 0.495, "Balanced analysis design", ha="left", va="center", fontsize=16.5, fontweight="bold", color=STAGE_COLORS["collect"])

    grid_x = [0.58, 0.76]
    grid_y = [0.31, 0.17]
    cell_w = 0.16
    cell_h = 0.11
    for x, side in zip(grid_x, ["ipsi", "contra"], strict=True):
        ax.add_patch(
            patches.Rectangle((x, 0.39), cell_w, 0.065, facecolor=SIDE_COLORS[side], linewidth=0)
        )
        ax.text(x + cell_w / 2, 0.422, side, ha="center", va="center", fontsize=14.5, color="white", fontweight="bold")
    for y, geno in zip(grid_y, ["ff", "cre"], strict=True):
        ax.add_patch(
            patches.Rectangle((0.505, y), 0.055, cell_h, facecolor=GENO_COLORS[geno], linewidth=0)
        )
        ax.text(0.5325, y + cell_h / 2, geno, ha="center", va="center", fontsize=14.5, color="white", fontweight="bold")

    for row_idx, geno in enumerate(["ff", "cre"]):
        for col_idx, side in enumerate(["ipsi", "contra"]):
            x = grid_x[col_idx]
            y = grid_y[row_idx]
            rounded_panel(ax, x, y, cell_w, cell_h, edgecolor=GRID, facecolor="#FBFBFB", lw=1.1, radius=0.012)
            srrs = grouped[(geno, side)]
            srr_text = ", ".join(srr.replace("SRR", "") for srr in srrs[:3]) + "\n" + ", ".join(
                srr.replace("SRR", "") for srr in srrs[3:]
            )
            ax.text(
                x + cell_w / 2,
                y + cell_h * 0.68,
                f"n = {len(srrs)}",
                ha="center",
                va="center",
                fontsize=13.5,
                fontweight="bold",
                color=TEXT_DARK,
            )
            ax.text(
                x + cell_w / 2,
                y + cell_h * 0.32,
                srr_text,
                ha="center",
                va="center",
                fontsize=9.4,
                color="#4A4A4A",
                linespacing=1.15,
            )

    ax.text(0.505, 0.115, "10 ipsi / 10 contra  •  10 ff / 10 cre  •  20 samples retained for DE", ha="left", va="center", fontsize=12.5, color=TEXT_DARK)
    save_figure(fig, "data_collection_stage.png")


def build_data_cleaning() -> None:
    heatmap = load_image(QC_DIR / "fastqc_module_status_heatmap_raw_vs_trimmed.png")
    severity = load_image(QC_DIR / "fastqc_severity_delta_by_srr.png")

    fig = plt.figure(figsize=(16, 10.2))
    gs = GridSpec(
        2,
        2,
        figure=fig,
        height_ratios=[1.18, 3.7],
        width_ratios=[1.78, 1.02],
        hspace=0.18,
        wspace=0.08,
    )

    ax_header = fig.add_subplot(gs[0, :])
    ax_header.set_axis_off()
    add_stage_banner(
        ax_header,
        "Data Cleaning",
        "Retained QC artifacts paired with a rebuilt checkpoint strip",
        STAGE_COLORS["clean"],
        y=0.81,
        h=0.18,
        title_size=17.2,
        subtitle_size=11.2,
    )
    card_y = 0.08
    card_h = 0.74
    add_card(
        ax_header,
        0.03,
        card_y,
        0.21,
        card_h,
        color=STAGE_COLORS["clean"],
        title="QC inputs",
        body="20 paired libraries\n40 raw read files",
        title_size=14.2,
        body_size=13.2,
    )
    add_card(
        ax_header,
        0.275,
        card_y,
        0.21,
        card_h,
        color=STAGE_COLORS["clean"],
        title="Canonical cleanup",
        body="fastp v0.23.2\nPE adapter detect\nQ20 • min 30 bp",
        title_size=14.2,
        body_size=12.4,
    )
    add_card(
        ax_header,
        0.52,
        card_y,
        0.21,
        card_h,
        color=STAGE_COLORS["clean"],
        title="Checkpoint metric",
        body="adapter-content failures\nresolved after trimming",
        title_size=14.2,
        body_size=12.6,
    )
    add_card(
        ax_header,
        0.765,
        card_y,
        0.21,
        card_h,
        color=STAGE_COLORS["clean"],
        title="Stage handoff",
        body="trimmed FASTQ.gz pairs\nFastQC + MultiQC reports",
        title_size=14.2,
        body_size=12.8,
    )

    ax_left = fig.add_subplot(gs[1, 0])
    ax_left.imshow(heatmap)
    ax_left.axis("off")
    add_panel_title(ax_left, "Retained project artifact: FastQC module-status heatmap", STAGE_COLORS["clean"])
    for spine in ax_left.spines.values():
        spine.set_visible(True)
        spine.set_color(STAGE_COLORS["clean"])
        spine.set_linewidth(1.4)

    ax_right = fig.add_subplot(gs[1, 1])
    ax_right.imshow(severity)
    ax_right.axis("off")
    add_panel_title(ax_right, "Retained project artifact: SRR-level severity delta", STAGE_COLORS["clean"])
    for spine in ax_right.spines.values():
        spine.set_visible(True)
        spine.set_color(STAGE_COLORS["clean"])
        spine.set_linewidth(1.4)

    save_figure(fig, "data_cleaning_stage.png")


def build_data_preparation() -> None:
    unique_mapping = load_image(ALIGN_DIR / "figures" / "unique_mapping_by_sample.png")
    metrics = pd.read_csv(ALIGN_DIR / "tables" / "alignment_metric_by_platform_median.tsv", sep="\t").iloc[0]

    fig = plt.figure(figsize=(16, 10.0))
    gs = GridSpec(
        2,
        2,
        figure=fig,
        height_ratios=[1.18, 3.35],
        width_ratios=[1.48, 1.02],
        hspace=0.18,
        wspace=0.10,
    )

    ax_header = fig.add_subplot(gs[0, :])
    ax_header.set_axis_off()
    add_stage_banner(
        ax_header,
        "Data Preparation",
        "Retained STAR artifact plus rebuilt alignment checkpoint metrics",
        STAGE_COLORS["prep"],
        y=0.81,
        h=0.18,
        title_size=17.2,
        subtitle_size=11.2,
    )
    card_y = 0.08
    card_h = 0.74
    add_card(
        ax_header,
        0.03,
        card_y,
        0.22,
        card_h,
        color=STAGE_COLORS["prep"],
        title="Reference",
        body="GRCm39 primary assembly\nMus_musculus.GRCm39.115.gtf",
        title_size=14.2,
        body_size=12.4,
    )
    add_card(
        ax_header,
        0.29,
        card_y,
        0.18,
        card_h,
        color=STAGE_COLORS["prep"],
        title="Index",
        body="STAR\nsjdbOverhang = 150",
        title_size=14.2,
        body_size=13.0,
    )
    add_card(
        ax_header,
        0.51,
        card_y,
        0.20,
        card_h,
        color=STAGE_COLORS["prep"],
        title="Alignment",
        body="paired-end STAR run\nsorted BAM + GeneCounts",
        title_size=14.2,
        body_size=12.4,
    )
    add_card(
        ax_header,
        0.75,
        card_y,
        0.22,
        card_h,
        color=STAGE_COLORS["prep"],
        title="Stage outputs",
        body="Log.final.out\nReadsPerGene.out.tab\nfamily count handoff",
        title_size=14.2,
        body_size=12.4,
    )

    ax_plot = fig.add_subplot(gs[1, 0])
    ax_plot.imshow(unique_mapping)
    ax_plot.axis("off")
    add_panel_title(ax_plot, "Retained project artifact: unique mapping by sample", STAGE_COLORS["prep"])
    for spine in ax_plot.spines.values():
        spine.set_visible(True)
        spine.set_color(STAGE_COLORS["prep"])
        spine.set_linewidth(1.4)

    ax_metrics = fig.add_subplot(gs[1, 1])
    ax_metrics.set_axis_off()
    ax_metrics.text(
        0.0,
        0.98,
        "Rebuilt from STAR summary tables",
        ha="left",
        va="top",
        fontsize=15.4,
        fontweight="bold",
        color=STAGE_COLORS["prep"],
    )

    card_positions = [
        (0.00, 0.54, "Median unique\nmapping", f"{metrics['unique_pct']:.2f}%"),
        (0.52, 0.54, "Median multi-\nmapping", f"{metrics['multi_pct']:.2f}%"),
        (0.00, 0.22, "Median noFeature\nburden", f"{metrics['N_noFeature_pct_of_input']:.2f}%"),
        (0.52, 0.22, "Median ambiguous\nburden", f"{metrics['N_ambiguous_pct_of_input']:.2f}%"),
    ]
    for x, y, title, body in card_positions:
        add_card(ax_metrics, x, y, 0.44, 0.22, color=STAGE_COLORS["prep"], title=title, body=body, title_size=12.5, body_size=18)
    ax_metrics.text(
        0.0,
        0.04,
        "Count-ready handoff:\n"
        "sorted BAMs, per-sample alignment logs,\n"
        "reverse-stranded GeneCounts tables merged\n"
        "into the 20-sample family_drg_novaseqx\n"
        "matrix.",
        transform=ax_metrics.transAxes,
        ha="left",
        va="bottom",
        fontsize=11.6,
        color=TEXT_DARK,
        linespacing=1.18,
        clip_on=True,
    )

    save_figure(fig, "data_preparation_stage.png")


def build_data_mining() -> None:
    filtering = pd.read_csv(DE_DIR / "family_drg_novaseqx" / "tables" / "filtering_summary.tsv", sep="\t").iloc[0]
    analysis = pd.read_csv(DE_DIR / "derived_analysis" / "analysis_summary.tsv", sep="\t")
    ff_sources = pd.read_csv(
        DE_DIR / "derived_analysis" / "ipsi_vs_contra_in_ff" / "gprofiler_source_summary.tsv",
        sep="\t",
    )
    cre_sources = pd.read_csv(
        DE_DIR / "derived_analysis" / "ipsi_vs_contra_in_cre" / "gprofiler_source_summary.tsv",
        sep="\t",
    )

    fig = plt.figure(figsize=(16.4, 10.8))
    gs = GridSpec(
        2,
        2,
        figure=fig,
        height_ratios=[1.18, 3.65],
        width_ratios=[1.34, 1.20],
        hspace=0.20,
        wspace=0.10,
    )

    ax_header = fig.add_subplot(gs[0, :])
    ax_header.set_axis_off()
    add_stage_banner(
        ax_header,
        "Data Analysis and Interpretation",
        "Rebuilt from DESeq2, bend-point, and g:Profiler summary tables",
        STAGE_COLORS["mine"],
        y=0.81,
        h=0.18,
        title_size=17.2,
        subtitle_size=11.2,
    )
    card_y = 0.08
    card_h = 0.74
    add_card(
        ax_header,
        0.03,
        card_y,
        0.22,
        card_h,
        color=STAGE_COLORS["mine"],
        title="Model inputs",
        body="20 samples retained\n~ side + geno + side:geno",
        title_size=14.2,
        body_size=13.0,
    )
    add_card(
        ax_header,
        0.29,
        card_y,
        0.22,
        card_h,
        color=STAGE_COLORS["mine"],
        title="Filtering checkpoint",
        body=f"{int(filtering['genes_after_filter']):,} of\n{int(filtering['genes_before_filter']):,} genes retained",
        title_size=14.2,
        body_size=14.2,
    )
    add_card(
        ax_header,
        0.55,
        card_y,
        0.18,
        card_h,
        color=STAGE_COLORS["mine"],
        title="Contrasts",
        body="5 modeled branches\n2 primary side-specific",
        title_size=14.2,
        body_size=13.0,
    )
    add_card(
        ax_header,
        0.77,
        card_y,
        0.20,
        card_h,
        color=STAGE_COLORS["mine"],
        title="Stage outputs",
        body="DE tables\nbend-point gene sets\nenrichment summaries",
        title_size=14.2,
        body_size=12.6,
    )

    ax_bar = fig.add_subplot(gs[1, 0])
    contrast_labels = {
        "ipsi_vs_contra_in_ff": "ipsi vs\ncontra (ff)",
        "ipsi_vs_contra_in_cre": "ipsi vs\ncontra (cre)",
        "geno_in_contra": "geno in\ncontra",
        "geno_in_ipsi": "geno in\nipsi",
        "interaction": "interaction",
    }
    x = np.arange(len(analysis))
    width = 0.36
    ax_bar.bar(x - width / 2, analysis["significant_padj_lt_0_05"], width=width, color=STAGE_COLORS["mine"], label="padj < 0.05")
    ax_bar.bar(x + width / 2, analysis["bendpoint_selected"], width=width, color="#B38ADF", label="bend-point output")
    ax_bar.set_xticks(x, [contrast_labels[row] for row in analysis["contrast_id"]], rotation=18, ha="right")
    ax_bar.set_ylabel("Gene count")
    add_panel_title(ax_bar, "Contrast-level outputs retained for follow-up", STAGE_COLORS["mine"])
    ax_bar.grid(axis="y", alpha=0.22)
    ax_bar.legend(frameon=False, loc="upper right")
    ax_bar.margins(x=0.03)
    ax_bar.text(
        0.01,
        -0.28,
        "Bend-point outputs are workflow-derived follow-up sets; they are reported alongside, not in place of, the full padj < 0.05 result lists.",
        transform=ax_bar.transAxes,
        ha="left",
        va="top",
        fontsize=11.3,
        color="#555555",
    )

    ax_heat = fig.add_subplot(gs[1, 1])
    ax_heat.set_axis_off()
    add_panel_title(ax_heat, "Main side-specific enrichment products", STAGE_COLORS["mine"])
    sources = ["GO:BP", "KEGG", "REAC"]
    ff_map = ff_sources.set_index("source")
    cre_map = cre_sources.set_index("source")
    rows = [
        ("ipsi vs contra in ff", ff_map),
        ("ipsi vs contra in cre", cre_map),
    ]
    max_terms = max(ff_map["total_terms"].max(), cre_map["total_terms"].max())
    start_x = 0.11
    start_y = 0.73
    cell_w = 0.275
    cell_h = 0.22
    for col_idx, source in enumerate(sources):
        ax_heat.text(start_x + col_idx * cell_w + (cell_w - 0.018) / 2, 0.92, source, ha="center", va="center", fontsize=13, fontweight="bold")
    for row_idx, (label, frame) in enumerate(rows):
        y = start_y - row_idx * 0.28
        ax_heat.text(0.0, y + cell_h / 2, label, ha="left", va="center", fontsize=12.3, color=TEXT_DARK)
        for col_idx, source in enumerate(sources):
            x0 = start_x + col_idx * cell_w
            terms = int(frame.loc[source, "total_terms"])
            peak = frame.loc[source, "strongest_term_neglog10"]
            alpha = 0.18 + 0.72 * (terms / max_terms)
            face = (123 / 255, 79 / 255, 160 / 255, alpha)
            rect = patches.FancyBboxPatch(
                (x0, y),
                cell_w - 0.018,
                cell_h,
                boxstyle="round,pad=0.01,rounding_size=0.02",
                facecolor=face,
                edgecolor=STAGE_COLORS["mine"],
                linewidth=1.15,
            )
            ax_heat.add_patch(rect)
            ax_heat.text(
                x0 + (cell_w - 0.018) / 2,
                y + cell_h * 0.58,
                f"{terms} terms",
                ha="center",
                va="center",
                fontsize=13.2,
                fontweight="bold",
                color="white" if alpha > 0.5 else TEXT_DARK,
            )
            ax_heat.text(
                x0 + (cell_w - 0.018) / 2,
                y + cell_h * 0.28,
                f"peak {peak:.1f}",
                ha="center",
                va="center",
                fontsize=11.0,
                color="white" if alpha > 0.5 else TEXT_DARK,
            )
    ax_heat.text(
        0.0,
        0.03,
        "Right panel rebuilt from the saved g:Profiler source-summary\ntables for the two primary side-specific contrasts.\nGO:BP dominates both branches, with smaller KEGG and\nReactome layers.",
        ha="left",
        va="bottom",
        fontsize=11.5,
        color=TEXT_DARK,
        linespacing=1.2,
    )

    save_figure(fig, "data_mining_stage.png")


def build_data_mining_selection() -> None:
    ff_ranked = pd.read_csv(
        DE_DIR / "derived_analysis" / "ipsi_vs_contra_in_ff" / "ordered_pvalues_with_bendpoint.tsv",
        sep="\t",
    )
    ff_summary = pd.read_csv(
        DE_DIR / "derived_analysis" / "ipsi_vs_contra_in_ff" / "bendpoint_summary.tsv",
        sep="\t",
    ).iloc[0]
    cre_summary = pd.read_csv(
        DE_DIR / "derived_analysis" / "ipsi_vs_contra_in_cre" / "bendpoint_summary.tsv",
        sep="\t",
    ).iloc[0]

    ff_ranked["pvalue"] = pd.to_numeric(ff_ranked["pvalue"], errors="coerce")
    ff_ranked["rank"] = pd.to_numeric(ff_ranked["rank"], errors="coerce")
    ff_ranked["neglog10_pvalue"] = pd.to_numeric(ff_ranked["neglog10_pvalue"], errors="coerce")

    threshold = float(ff_summary["bend_pvalue_threshold"])
    selected_count = int(ff_summary["genes_below_bendpoint"])

    selected_mask = ff_ranked["pvalue"] <= threshold
    if selected_count > 0 and selected_mask.any():
        bend_rank = int(ff_ranked.loc[selected_mask, "rank"].max())
    else:
        bend_rank = 1

    fig = plt.figure(figsize=(16, 9.9))
    gs = GridSpec(
        2,
        2,
        figure=fig,
        height_ratios=[1.24, 3.0],
        width_ratios=[1, 1],
        hspace=0.24,
        wspace=0.18,
    )

    ax_header = fig.add_subplot(gs[0, :])
    ax_header.set_axis_off()
    add_stage_banner(
        ax_header,
        "Bend-point checkpoint",
        "Cards summarize both branches; plots shown for ipsi_vs_contra_in_ff",
        STAGE_COLORS["mine"],
        y=0.81,
        h=0.18,
        title_size=17.2,
        subtitle_size=11.2,
    )

    card_y = 0.08
    card_h = 0.74
    add_card(
        ax_header,
        0.05,
        card_y,
        0.40,
        card_h,
        color=STAGE_COLORS["mine"],
        title="ipsi vs contra in ff",
        body=(
            f"padj < 0.05: {int(ff_summary['significant_padj_lt_0_05']):,} genes\n"
            f"bend-point: {int(ff_summary['genes_below_bendpoint']):,} genes\n"
            f"threshold = {ff_summary['bend_pvalue_threshold']:.2e}"
        ),
        title_size=14.6,
        body_size=13.2,
    )
    add_card(
        ax_header,
        0.55,
        card_y,
        0.40,
        card_h,
        color=STAGE_COLORS["mine"],
        title="ipsi vs contra in cre",
        body=(
            f"padj < 0.05: {int(cre_summary['significant_padj_lt_0_05']):,} genes\n"
            f"bend-point: {int(cre_summary['genes_below_bendpoint']):,} genes\n"
            f"threshold = {cre_summary['bend_pvalue_threshold']:.2e}"
        ),
        title_size=14.6,
        body_size=13.2,
    )

    ax_left = fig.add_subplot(gs[1, 0])
    ax_left.plot(
        ff_ranked["rank"],
        ff_ranked["neglog10_pvalue"],
        color=SIDE_COLORS["ipsi"],
        linewidth=1.6,
    )
    ax_left.axvline(bend_rank, color=GENO_COLORS["cre"], linestyle="--", linewidth=1.5)
    ax_left.axvspan(1, bend_rank, color=LIGHT_COLORS["mine"], alpha=0.5)
    add_panel_title(ax_left, "ipsi_vs_contra_in_ff: ordered p-values", STAGE_COLORS["mine"])
    ax_left.set_xlabel("Rank (smallest p-value to largest)")
    ax_left.set_ylabel("-log10(p-value)")
    ax_left.text(
        0.985,
        0.96,
        f"bend rank = {bend_rank:,}\nthreshold = {threshold:.2e}",
        transform=ax_left.transAxes,
        color=GENO_COLORS["cre"],
        fontsize=10.0,
        ha="right",
        va="top",
        bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": GENO_COLORS["cre"]},
    )

    ax_right = fig.add_subplot(gs[1, 1])

    p_zoom_max = 0.01
    ff_zoom = ff_ranked.loc[ff_ranked["pvalue"] <= p_zoom_max, ["pvalue", "rank"]].dropna()

    ax_right.plot(
        ff_zoom["pvalue"],
        ff_zoom["rank"],
        color=GENO_COLORS["ff"],
        linewidth=3.0,
        label="Cumulative genes (sorted by p)",
    )
    ax_right.axvline(
        threshold,
        color=GENO_COLORS["cre"],
        linestyle="--",
        linewidth=4.0,
        label="Bend-point threshold (vertical line)",
    )
    add_panel_title(ax_right, "ipsi_vs_contra_in_ff: cumulative count by p-value (p ≤ 0.01)", STAGE_COLORS["mine"])
    ax_right.set_xlabel("p-value")
    ax_right.set_ylabel("Cumulative genes")
    ax_right.set_xlim(left=-0.0001, right=p_zoom_max)
    ax_right.set_ylim(bottom=0)
    ax_right.set_xticks(np.linspace(0, p_zoom_max, 5))
    ax_right.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.4f"))
    ax_right.legend(loc="lower right", frameon=True, framealpha=0.92, fontsize=10.0)
    ax_right.text(
        0.06,
        0.93,
        f"bend-point\np = {threshold:.2e}\nselected = {selected_count:,}",
        transform=ax_right.transAxes,
        color=GENO_COLORS["cre"],
        fontsize=12.0,
        ha="left",
        va="top",
        bbox={
            "facecolor": "white",
            "alpha": 0.9,
            "edgecolor": GENO_COLORS["cre"],
            "boxstyle": "square,pad=0.4",
        },
    )

    for ax in (ax_left, ax_right):
        ax.tick_params(labelsize=10)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(STAGE_COLORS["mine"])
            spine.set_linewidth(1.2)

    save_figure(fig, "data_mining_selection_stage.png")


def main() -> None:
    ensure_assets_dir()
    build_overview()
    build_data_collection()
    build_data_cleaning()
    build_data_preparation()
    build_data_mining()
    build_data_mining_selection()
    print(f"Methods assets written to {ASSET_DIR}")


if __name__ == "__main__":
    main()
