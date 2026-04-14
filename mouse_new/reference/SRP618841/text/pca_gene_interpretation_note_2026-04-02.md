# How we move from PCA to biological interpretation (`SRP618841`)

## Core question

The PCA tells us that the strongest sample split in the active `mouse_new` subset is `ipsi` versus `contra`. To interpret that biologically, we need to identify the genes that consistently distinguish those two sides and then ask what those genes do.

## What we used

### Study-design anchor
- Public study: `SRP618841` / `PRJNA1322439` / `GSE243308`
- Source study title: `Aryl hydrocarbon receptor restricts axon regeneration of DRG neurons in response to injury`
- Local working subset:
  - tissue = `DRG`
   - treatment = `Sciatic Nerve Injury - 1dpi`
  - side groups = `ipsi` and `contra`
  - genotype groups = `ff` and `cre`

### Side-specific contrasts
We used the two main side-specific DE contrasts:
- `ipsi_vs_contra_in_ff`
- `ipsi_vs_contra_in_cre`

### Narrowing rule
We used the bend-point-selected genes for each contrast so we focus on the strongest interpretable core rather than the full long tail of significant genes.

## What we did

1. Took the bend-point-selected gene sets from:
   - `derived_analysis/ipsi_vs_contra_in_ff/selected_genes_bendpoint.tsv`
   - `derived_analysis/ipsi_vs_contra_in_cre/selected_genes_bendpoint.tsv`
2. Computed the overlap between the two sets.
3. Checked whether the overlapping genes change in the same direction in both contrasts.
4. Resolved the strongest shared Ensembl IDs to gene symbols.

## What we found

### Overlap structure
- `ipsi_vs_contra_in_ff` bend-point set: `709` genes
- `ipsi_vs_contra_in_cre` bend-point set: `870` genes
- shared genes between those two sets: `620`
- among the strongest shared genes we checked, direction was consistent across both contrasts
- the strongest shared genes were all `ipsi_up` in both `ff` and `cre`

### Strong shared side-driver genes
Top shared genes resolved so far:
- `Atf3`
- `Gadd45a`
- `Flrt3`
- `Sox11`
- `Jun`
- `Sema6a`
- `Tubb6`
- `Gpr151`
- `Hspb1`
- `Plin2`

Saved tables:
- `../metadata/shared_side_driver_overlap.tsv`
- `../metadata/top_shared_side_driver_genes.tsv`

## Biological reading

These genes are much more informative than the PCA alone because they let us describe what kind of injury-side program the PCA separation likely reflects.

### Injury / stress response examples
- `Atf3` — classic neuronal injury-response transcription factor
- `Jun` — immediate-early stress / regeneration-associated transcription factor
- `Gadd45a` — DNA-damage / stress-response marker
- `Hspb1` — heat-shock / cellular stress response

### Growth / repair / axon program examples
- `Sox11` — regeneration-associated developmental / axon-growth program
- `Gpr151` — often induced in injured sensory neurons
- `Sema6a` — axon guidance / neuronal remodeling context
- `Tubb6` — cytoskeletal remodeling context

## Interpretation

This means the PCA is not just showing an abstract left-versus-right split. In the active subset, the `ipsi` cluster is likely separating because the injury side carries a strong and consistent neuronal injury / stress / regeneration-related transcriptional program that is shared across both genotype backgrounds.

## How this answers the professor question

A stronger answer than “the PCA separates `ipsi` and `contra`” is:

- the PCA shows the main structure is injury side versus opposite side,
- the side-specific DE contrasts identify the genes most associated with that split,
- and those genes are enriched for injury-response, stress-signaling, and regeneration-related biology.

## Recommended next step

To tighten this further, we should:
1. separate the strongest shared genes into
   - injury/stress markers
   - pro-growth/regeneration markers
   - signaling/remodeling markers
2. compare those genes directly against the paper-centered genes/pathways:
   - `Ahr`
   - `Hif1a`
   - `Arnt`
   - ISR / inflammation / regeneration programs
3. add one compact table to the notebook/report with:
   - gene symbol
   - direction (`ipsi_up` or `contra_up`)
   - short biological role
