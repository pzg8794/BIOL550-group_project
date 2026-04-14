# SRP618841 reference bundle

This folder stores the public records and local metadata tied to the active `mouse_new` contingency dataset.

## Core identifiers

- SRA study: `SRP618841`
- BioProject: `PRJNA1322439`
- GEO series: `GSE243308`
- Example run: `SRR35329980`

Saved historical snapshot kept in the bundle:
- `html/bioproject_PRJNA1017789.html`

## Study title

- `Aryl hydrocarbon receptor restricts axon regeneration of DRG neurons in response to injury`

## Public design summary

From the NCBI BioProject / GEO records:
- organism: `Mus musculus`
- tissue: `L4-L6 DRG`
- design: `Ahr cKO` vs control
- injury model: sciatic nerve injury / peripheral axotomy
- side-specific samples: `ipsilateral` and `contralateral`
- collection timing: `1 day later` after injury in the injury arm
- sequencing: Illumina stranded mRNA library prep, `NovaSeq X`, paired-end

## Local working subset

From `metadata/mouse_de_design_table.tsv`:
- `20` runs in the active local subset
- SRRs: `SRR35329977`–`SRR35329996`
- one family: `family_drg_novaseqx`
- balanced by side and genotype:
  - `10` `ipsi`
  - `10` `contra`
  - `10` `ff`
  - `10` `cre`
- treatment label in the local table: `Sciatic Nerve Injury - 1dpi`

## Why this bundle matters

This is the source-of-truth reference set we can use when we need to answer:
- what project `SRP618841` belongs to
- what the study design is
- what the side labels mean biologically
- what external matrices and metadata are available from GEO

## Stored files

### `html/`
- `sra_search.html`
- `sra_study.html`
- `bioproject_PRJNA1017789.html`
- `geo_GSE243308.html`
- `sra_run_SRR35329980.html`

### `data/`
- `GSE243308_counts_genic_matrix.txt.gz`
- `GSE243308_fpkm_genic_matrix.txt.gz`
- `GSE243308_supplemental_counts_genic_matrix.txt.gz`
- `GSE243308_supplemental_fpkm_genic_matrix.txt.gz`

### `metadata/`
- `mouse_de_design_table.tsv`
- `contrast_manifest.tsv`
- `family_manifest.tsv`

## Recommended next use

Use this bundle to:
1. anchor the PCA interpretation in the actual study design,
2. cross-check whether paper-level genes/pathways (for example `Ahr`, `Hif1a`, `Arnt`, ISR, stress/inflammation, regeneration programs) appear in our DE contrasts,
3. decide which side-specific genes best explain the `ipsi` vs `contra` split in our local subset.

## Additional conceptual reference

- We are also keeping `two-hybrid screening` as a reference concept for interaction-oriented biological interpretation:
  - `https://en.wikipedia.org/wiki/Two-hybrid_screening`
- Short use note:
  - this is a conceptual reference for thinking about interaction-driven biology and candidate binding partners,
  - not a claim that our current RNA-seq dataset itself is a two-hybrid experiment.
