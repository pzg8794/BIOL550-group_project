# Mouse differential expression notebook follow-up — 2026-03-19

## Documentation links

- Parent mouse workflow: [PROCESS_mouse_fastq_fastqc_fastx.md](PROCESS_mouse_fastq_fastqc_fastx.md)
- Active task list: [TODO_mouse.md](TODO_mouse.md)
- Remediation plan: [TODO_qc_remediation.md](TODO_qc_remediation.md)
- Alignment notebook note: [ALIGNMENT_ANALYSIS_NOTEBOOK_2026-03-19.md](ALIGNMENT_ANALYSIS_NOTEBOOK_2026-03-19.md)
- Shared server DE setup: [DESEQ2_SHARED_SERVER_SETUP_2026-03-20.md](DESEQ2_SHARED_SERVER_SETUP_2026-03-20.md)
- Group project documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)
- Work log: [../WORKLOG.md](../WORKLOG.md)

## Step

- Created and executed a dedicated differential-expression notebook for the mouse count layer:
  - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_differential_expression_all26.ipynb`
- Added a reproducible DESeq2 driver script:
  - `Semester5/BIOL550/group_project/pipelines/mouse_deseq2_all26.R`
- Derived one cleaned DE design table from the STAR count handoff and alignment sample summary:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/tables/mouse_de_design_table.tsv`
- Split the analysis into three valid model families instead of fitting one confounded all-sample model:
  - tissue / `NovaSeq 6000` / naive vs injury
  - tissue / `NovaSeq X` / ipsilateral vs contralateral sham
  - neurons / `NovaSeq X`
- Wrote the DE evidence package into:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/`

## Key outputs

- Notebook:
  - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_differential_expression_all26.ipynb`
- DE design table:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/tables/mouse_de_design_table.tsv`
- Family manifest:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/tables/family_manifest.tsv`
- Contrast manifest:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/tables/contrast_manifest.tsv`
- Family output folders:
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/family_tissue_novaseq6000/`
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/family_tissue_sham_novaseqx/`
  - `Semester5/BIOL550/group_project/mouse/differential_expression_all26/family_neurons_novaseqx/`

## Finding

- The count matrix and sample summary matched cleanly across all `26` samples, so the DE design table could be derived without manual sample exclusion.
- The dataset supports three interpretable DE families:
  - `12` tissue samples on `NovaSeq 6000`
  - `8` tissue sham samples on `NovaSeq X`
  - `6` neuron-culture samples on `NovaSeq X`
- The strongest signal is in the tissue injury contrasts:
  - `injury_in_control` produced `4667` significant genes at `padj <= 0.05`
  - `injury_in_cko` produced `4088` significant genes at `padj <= 0.05`
- Genotype-only effects are modest in the tissue `NovaSeq 6000` family:
  - `geno_in_naive` = `2` significant genes
  - `geno_in_injury` = `2` significant genes
- The sham-side and neuron families still show usable genotype / side effects:
  - `geno_in_ipsilateral_sham` = `144` significant genes
  - `ipsilateral_vs_contralateral_in_cko` = `131` significant genes
  - `geno_in_neurons` = `139` significant genes
- The tissue `NovaSeq 6000` interaction term did not produce significant genes in this first-pass model; the sham-side interaction remained small (`11` significant genes).

## Decision

- Keep the family-specific DESeq2 strategy as the default mouse DE workflow.
- Do not fit a single global DE model across tissue, neurons, and both platforms.
- Treat the tissue injury contrasts as the strongest candidates for the individual report figures/tables.
- Keep the sham-side and neuron genotype contrasts as secondary report-ready analyses that help show context-specific effects.
- Use the notebook plus `differential_expression_all26/` as the current local DE evidence package.

## Shared server status

- A private team-only DESeq2 runtime was created on `sequoia` instead of using the broken system `R`.
- Runtime path:
  - `/home/pzg8794/.local/share/micromamba/envs/biol550_deseq2`
- The shared execution path should point to that private environment, not to `/usr/local/bin/R`.
