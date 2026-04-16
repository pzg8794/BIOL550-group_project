# HTSA outline-to-draft alignment notes

Date: 2026-04-15

## Purpose

This note uses `HTSA_Paper_Outline.tex` / `.pdf` as a **coverage guide** for the current drafting pass. It is not a citation source.

## Already covered in `materials_methods_piter_draft.tex`

- Four-stage workflow framing for Data Collection, Data Cleaning, Data Preparation, and Data Analysis and Interpretation.
- Sample accession lineage and retained 20-sample subset.
- Core tools and representative commands.
- QC / trimming checkpoint language.
- STAR alignment and count handoff.
- DESeq2 model design, bend-point narrowing, and g:Profiler follow-up logic.

## Belongs outside Materials and Methods

These outline items are important, but they are not primarily Methods content and should not be forced into the Methods draft just to satisfy the outline:

- Paper / dataset introduction and motivation.
- Why DRG was used biologically.
- Why conditional knockout matters relative to constitutive knockout.
- `ipsilateral` versus `contralateral` biological interpretation.
- `FF` / `CRE` reader-facing explanation.
- What our paper adds beyond the source paper.
- Main biological interpretation, primary vs secondary findings, and limitations.

## Follow-up needed in shared paper prose

- Keep reader-facing prose on first mention aligned to `WT (ff control)` and `cKO (cre conditional knockout)` where that helps clarity.
- Keep the side-specific injury contrast as the main interpretive path and genotype as the secondary layer.
- Make sure any source-paper mechanism claim in Intro/Discussion is supported by the AhR paper summary and not by the outline itself.

## Follow-up needed in LaTeX

- Keep `materials_methods_piter_draft.tex` focused on Methods-only claims.
- Use formal bibliography citations for external tools, dataset pages, and source-paper references.
- Keep any non-Methods additions discovered during this pass in support docs first, then move them later into the correct manuscript section.
