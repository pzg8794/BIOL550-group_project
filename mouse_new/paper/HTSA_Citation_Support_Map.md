# HTSA citation support map

Date: 2026-04-15

## Purpose

Use this file as the bridge between the two citation tracks requested for the HTSA paper materials:

- **Teammate-facing markdown / Google-Doc-ready prose** uses inline validation links in the form `... (<link>)`.
- **LaTeX manuscript prose** uses formal bibliography citations such as `\parencite{key}` backed by `materials_methods_piter_draft.bib`.

This file is not a substitute for the bibliography. It is a routing aid so the same claim is supported consistently in both formats.

## Shared citation rule

- For **markdown**, add a link only where a factual claim, dataset identifier, or tool attribution needs validation.
- For **LaTeX**, do not paste raw URLs into the prose when a matching bibliography key exists.
- If a claim is still too vague to support cleanly, rewrite the claim before adding a citation.

## Core source map

| Claim / source type | Preferred inline validation link | Preferred LaTeX citation key(s) | Notes |
| --- | --- | --- | --- |
| Main AhR source paper | [https://doi.org/10.1101/2023.11.04.565649](https://doi.org/10.1101/2023.11.04.565649) | `halawani2023ahr` | Use for mechanism/background claims about AhR, DRG injury context, cKO rationale, proteostasis, translation, HIF-1α, and regeneration. |
| SRA study page | [https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP618841](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP618841) | `sraStudySRP618841` | Use when naming the study accession. |
| BioProject page | [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1322439](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1322439) | `bioprojectPRJNA1322439` | The RunInfo and local intake docs tie `SRP618841` to `PRJNA1322439`. |
| GEO series page | [https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243308](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243308) | `geoGSE243308` | Use this accession consistently across shared docs and LaTeX. |
| SRA Toolkit | [https://github.com/ncbi/sra-tools](https://github.com/ncbi/sra-tools) | `sratoolkit` | Use for `prefetch` / `fasterq-dump`. |
| FastQC | [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) | `fastqc` | QC tool citation. |
| MultiQC | [https://doi.org/10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354) | `multiqc` | Cohort summary citation. |
| fastp | [https://doi.org/10.1093/bioinformatics/bty560](https://doi.org/10.1093/bioinformatics/bty560) | `fastp` | Cleanup / trimming citation. |
| Ensembl mouse reference release | [https://useast.ensembl.org/Mus_musculus/Info/Index](https://useast.ensembl.org/Mus_musculus/Info/Index) | `ensemblRelease115` | Use for the `GRCm39` / release-115 pair. |
| STAR aligner | [https://doi.org/10.1093/bioinformatics/bts635](https://doi.org/10.1093/bioinformatics/bts635) | `star` | Alignment citation. |
| DESeq2 | [https://doi.org/10.1186/s13059-014-0550-8](https://doi.org/10.1186/s13059-014-0550-8) | `deseq2` | Differential expression citation. |
| g:Profiler | [https://doi.org/10.1093/nar/gkaa427](https://doi.org/10.1093/nar/gkaa427) | `gprofiler2021` | Functional enrichment citation. |
| Gene Ontology resource | [https://doi.org/10.1093/nar/gkaa1113](https://doi.org/10.1093/nar/gkaa1113) | `geneOntology2021` | Use when describing GO as a knowledge layer rather than only the software. |
| KEGG | [https://doi.org/10.1093/nar/gkae987](https://doi.org/10.1093/nar/gkae987) | `kegg2025` | Pathway source citation. |
| Reactome | [https://doi.org/10.1093/nar/gkab1028](https://doi.org/10.1093/nar/gkab1028) | `reactome2022` | Pathway source citation. |
| CRISP-DM process framing | no inline link needed unless used in markdown prose | `crispdm2000` | Use only when discussing the four-stage process framing in manuscript prose. |

## Preferred wording patterns

### Paper/background sentence in markdown

- `The source paper identifies AhR as a neuronal brake on axon regeneration and links AhR activity to stress-response and proteostasis programs after axotomy ([https://doi.org/10.1101/2023.11.04.565649](https://doi.org/10.1101/2023.11.04.565649)).`

### Dataset provenance sentence in markdown

- `The working dataset comes from SRA study SRP618841, BioProject PRJNA1322439, and GEO series GSE243308 ([SRA](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP618841); [BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1322439); [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243308)).`

### Matching LaTeX pattern

- `... after sciatic nerve injury \parencite{halawani2023ahr,sraStudySRP618841,bioprojectPRJNA1322439,geoGSE243308}.`

## Outline-use reminder

- `HTSA_Paper_Outline.tex` and `HTSA_Paper_Outline.pdf` are **structure guides**, not citation sources.
- If an outline bullet suggests a topic that belongs in Introduction or Discussion, support it with the AhR paper or validated project outputs rather than citing the outline itself.
