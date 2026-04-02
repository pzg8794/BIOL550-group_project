# Mouse project — TODO (`SRP618841` parallel candidate)

## Documentation links

- Dataset process doc: [SRP618841_PROCESS_fastq_fastqc_fastp.md](SRP618841_PROCESS_fastq_fastqc_fastp.md)
- Dataset intake note: [SRP618841_DATASET_INTAKE_2026-03-25.md](SRP618841_DATASET_INTAKE_2026-03-25.md)
- Parent mouse TODO: [TODO_mouse.md](TODO_mouse.md)
- Group project work log: [../WORKLOG.md](../WORKLOG.md)
- Group project documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)

## Intake + setup

- [x] Pull `SRP618841` RunInfo snapshot.
- [x] Create canonical run list (`20` runs).
- [x] Reserve isolated server roots for runtime data and metadata.
- [x] Add a dataset-specific launcher for staged execution.

## Stage A — download + raw FastQC

- [x] Copy canonical run list to the server metadata root.
- [x] Copy the dataset-specific launcher to `/home/pzg8794/pipelines/`.
- [x] Create the isolated server dataset root.
- [x] Add a local monitor helper for quick progress checks.
- [x] Start the raw download + FastQC stage.
- [x] Confirm the raw download + FastQC PIDs and logs appear under `.pipeline/`.
- [x] Watch for the first completed FASTQ pairs and first raw FastQC outputs.
- [x] Copy raw `FastQC` + raw `MultiQC` back to the local `mouse_new/` tree.
- [x] Create the local raw-vs-trimmed-style QC notebook for `mouse_new`.

## Stage B — `fastp` + post-`fastp` FastQC

- [x] Scaffold the `fastp` stage launcher.
- [x] Run `fastp` across all 20 SRRs after Stage A completes.
- [x] Confirm post-`fastp` FastQC outputs.
- [x] Copy the completed post-`fastp` `FastQC`, `fastp` reports, and post-`fastp` `MultiQC` back into the local `mouse_new/` tree.

## Stage C — alignment prep

- [x] Scaffold the STAR stage launcher.
- [x] Freeze the exact reference genome + annotation pair for this dataset.
- [x] Start alignment only after Stage B outputs are verified.
- [x] Confirm server-side STAR alignment completion for all 20 SRRs.
- [x] Remove the stale `_star_tmp` directory left by the bad rerun on `SRR35329996`.

## Stage D — alignment summaries

- [x] Export the sample-level alignment summary.
- [x] Export the reverse-stranded count matrix.
- [x] Export platform / design summary tables.
- [x] Copy the completed alignment-side summary outputs back into the local `mouse_new/` tree.

## Stage E — DE scaffolding

- [x] Build the cleaned DE design table.
- [x] Build the family manifest.
- [x] Run the local `mouse_new` DESeq2 workflow for the 20-sample DRG design.
- [x] Keep the DE outputs local under `mouse_new/differential_expression_all20/`.

## Local analysis structure

- [x] Keep the candidate dataset isolated under `mouse_new/`.
- [x] Mirror the current mouse notebook structure with a canonical notebook under `mouse_new/notebooks/`.
- [x] Standardize local outputs under `mouse_new/qc_analysis_raw_vs_trimmed/`.
- [x] Mirror the main stage directories from `mouse/` so `mouse_new/` is easy to follow.
- [x] Prepare mouse-style notebook replicas for QC, remediation, alignment, and DE under `mouse_new/notebooks/`.
- [x] Clean the replica notebook wording once the corresponding stage data is actually present locally.
- [x] Finish the remediation/alignment/DE notebook tailoring right after each stage lands locally.

## 2026-03-29 status note

- Alignment now appears complete server-side for `SRP618841`.
- Current server evidence:
  - `all20_fastp_alignment.completed` exists
  - `20` per-sample `.completed` markers exist
  - `20` sorted BAMs exist
  - `20` `ReadsPerGene.out.tab` files exist
- One STAR log (`SRR35329996.star.log`) was overwritten during the earlier bad rerun, so only `19` logs currently contain the terminal `finished successfully` line even though the full output set is present.
- No active STAR process remained at the completion check.
- Local `mouse_new` alignment notebook now runs successfully and exports the same alignment handoff tables used by `mouse/`.
- Local `mouse_new` DE notebook now runs successfully against the new `family_drg_novaseqx` design.
- Current local DE output set includes:
  - `mouse_new/differential_expression_all20/tables/mouse_de_design_table.tsv`
  - `mouse_new/differential_expression_all20/tables/family_manifest.tsv`
  - `mouse_new/differential_expression_all20/tables/contrast_manifest.tsv`
  - family-specific figures/tables under `mouse_new/differential_expression_all20/family_drg_novaseqx/`

## 2026-04-02 transcript-driven DE follow-up

- [x] Keep `mouse_new/notebooks/mouse_differential_expression_all20.ipynb` as the canonical local DE notebook for the `SRP618841` candidate dataset.
- [x] Add a PCA-first interpretation block so the notebook explicitly starts from the dominant side-driven family structure.
- [x] Add cumulative / bend-point filtering for the two main side-specific contrasts:
  - `ipsi_vs_contra_in_ff`
  - `ipsi_vs_contra_in_cre`
- [x] Add a stronger genotype-focused follow-up centered on `geno_in_contra`, with `geno_in_ipsi` retained as a comparison branch.
- [x] Add GO/pathway enrichment for:
  - bend-point-selected `ipsi_vs_contra_in_ff` genes
  - bend-point-selected `ipsi_vs_contra_in_cre` genes
  - `geno_in_contra` genes with `padj < 0.05`
- [x] Save reusable derived outputs under:
  - `mouse_new/differential_expression_all20/derived_analysis/`
- [x] Keep this pass local-only for now; use it to choose the strongest next weekly-report story rather than treating it as the weekly report itself.

### 2026-04-02 findings

- The transcript-guided reading remains consistent: PCA should be interpreted first because side (`ipsi` vs `contra`) is the dominant visible split in the `family_drg_novaseqx` design.
- The two main side-specific contrasts still drive the Draft 1 paper story, but both produce very large significant-gene sets:
  - `ipsi_vs_contra_in_ff` = `7023` genes with `padj < 0.05`
  - `ipsi_vs_contra_in_cre` = `7541` genes with `padj < 0.05`
- Bend-point filtering gives a less-arbitrary narrowing rule than a fixed top-`N` cutoff:
  - `ipsi_vs_contra_in_ff` bend-point set = `709` genes
  - `ipsi_vs_contra_in_cre` bend-point set = `870` genes
- `geno_in_contra` remains the strongest secondary genotype branch:
  - `891` significant genes
- `geno_in_ipsi` stays much smaller:
  - `2` significant genes
- Enrichment outputs are now available for the two bend-point-filtered side-specific sets and for the `geno_in_contra` significant-gene set.

### 2026-04-02 extension — genotype + interaction bend-point

- [x] Extend the bend-point method to:
  - `geno_in_contra`
  - `geno_in_ipsi`
  - `interaction`
- [x] Regenerate `mouse_new/differential_expression_all20/derived_analysis/analysis_summary.tsv` with real bend-point counts and thresholds for all exported contrasts.
- [x] Update the canonical local notebook so the transcript-driven overview, bend-point method note, artifact index, story-selection criteria, risk checks, and weekly-report takeaways are all documented in one place.
- [x] Update the local weekly DE report HTML under `mouse_new/reports/` so it explains the bend-point method, the gene sets used for enrichment, and the currently recommended story.
