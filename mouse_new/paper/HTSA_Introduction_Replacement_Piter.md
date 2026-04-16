# HTSA introduction replacement — Piter section

Date: 2026-04-15

## Paste-ready paragraph

Our paper uses a published mouse dorsal root ganglion (DRG) RNA-seq dataset to re-examine how injury response and regeneration are balanced after peripheral nerve damage, with particular attention to the role of the aryl hydrocarbon receptor (Ahr) ([https://doi.org/10.1101/2023.11.04.565649](https://doi.org/10.1101/2023.11.04.565649); [SRA](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP618841); [BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1322439); [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243308)). The original study used a neuronal conditional Ahr knockout because DRGs provide a useful model for peripheral axon regrowth after sciatic nerve injury, and the conditional design helps isolate neuron-intrinsic effects more cleanly than a constitutive knockout background with broader baseline pathology ([https://doi.org/10.1101/2023.11.04.565649](https://doi.org/10.1101/2023.11.04.565649)). Within this dataset, the main biological comparison is between ipsilateral DRG tissue collected on the injured side and contralateral DRG tissue from the uninjured side, while genotype provides a second layer of comparison between wild-type (`ff`) control animals and the Ahr conditional knockout (`cre`) background ([https://doi.org/10.1101/2023.11.04.565649](https://doi.org/10.1101/2023.11.04.565649)). We use the original paper as a mechanistic anchor, but our analysis extends beyond its candidate-gene emphasis by applying transcriptome-wide differential expression and pathway-level follow-up to the full dataset. In practice, this allows us to test whether the strongest signals in the data remain centered on injury-side differences, determine how strongly genotype contributes relative to that main contrast, and connect the resulting gene sets to broader biological processes such as signaling, stress response, and regeneration-related remodeling; that emphasis is also consistent with the source paper’s own transcriptomic framing, where injury status explained more of the global structure than genotype alone ([https://doi.org/10.1101/2023.11.04.565649](https://doi.org/10.1101/2023.11.04.565649)).

## Rationale / mapping to class feedback

- **Dataset + paper framing:** opens by stating exactly what dataset/paper context the section is about, so the paragraph does not begin as fragmented prompts.
- **Why DRG / why cKO:** explains why DRG is biologically relevant and why a conditional knockout design matters, which the current draft had in scattered question form.
- **Ipsilateral vs contralateral:** gives the main experimental comparison clearly and early.
- **WT / cKO framing:** uses reader-facing biological wording rather than only `FF` / `CRE`, while still staying compatible with the underlying dataset design.
- **What our paper adds:** states that we are extending the original paper with transcriptome-wide DE and pathway interpretation instead of only repeating its candidate-gene framing.
- **Validated analysis story:** keeps side-specific injury response as the main signal and genotype as the secondary layer, consistent with the weekly reports and transcript-guided DE follow-up.

## Notes for handoff

- If the surrounding draft still uses `FF` / `CRE`, this paragraph can be adjusted on first use to:
  - `wild-type (ff)`
  - `Ahr conditional knockout (cre)`
- If the group wants a slightly more formal closing sentence, the last sentence can be split into two shorter sentences without changing the meaning.
- For the manuscript `.tex`, convert the inline links in this paragraph back to the matching bibliography keys listed in `/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse_new/paper/HTSA_Citation_Support_Map.md`.
