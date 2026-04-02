# Paper drafting strategy — all mind maps in one place

This local paper document keeps the main mind maps together in one place so it is easier to spot:

- patterns
- weak points
- missing links
- repeated issues across drafts

We are using the term:

- **mind map**

---

## 1) High-level mind map — all drafts to the final paper

```text
                               [ Final paper ]
                                       |
        -----------------------------------------------------------------
        |                         |                      |                |
        v                         v                      v                v
 [ High-level planning ]   [ Draft 1 ]            [ Draft 2 ]      [ Draft 3 ]
        |                         |                      |                |
        |                         |                      |                |
        v                         v                      v                v
 - define the overall      - establish the         - expand the      - complete the
   paper direction           main paper story        paper             full paper
 - align the team          - choose the main       - strengthen      - refine flow
 - define what each          results/story           logic           - close gaps
   draft should do         - decide what is        - add more        - polish wording
                             central vs support      support         - finalize figures
                           - use the Draft 1       - improve           and tables
                             mind map                connections
                                       |
                                       v
                              [ Full paper submission ]
```

### Meaning

- **High-level planning** sets the direction
- **Draft 1** locks the main story
- **Draft 2** strengthens and expands it
- **Draft 3** completes and polishes it
- all drafts build toward the **final paper**

---

## 2) High-level mind map — Draft 1

```text
                                [ Draft 1 ]
                                     |
        -------------------------------------------------------------------------
        |                      |                    |                 |            |
        v                      v                    v                 v            v
 [ Paper goal ]     [ First mouse path ]   [ Why it was weak ] [ mouse_new ] [ Drafting goal ]
        |                      |                    |                 |            |
        |                      |                    |                 |            |
        v                      v                    v                 v            v
 - journal-style paper   - first pipeline      - no clean main   - contingency  - turn the
 - DE-centered paper       was built/run         story              path           project into
 - meaningful analysis   - QC, trimming,       - uneven results   - new QC        a strong
   story                   alignment, DE       - structural       - fastp         paper story
                                                complexity        - alignment
                                                                   - DE
                                     |                                 |
                                     |                                 |
                                     v                                 v
                         [ Need a better paper path ]      [ One usable DE family ]
                                     |                                 |
                                     v                                 v
                      [ SRP618841 / mouse_new becomes main path ]   [ family_drg_novaseqx ]
                                                                      |
                                                                      v
                                                        [ Strongest paper results ]
                                                        - ipsi_vs_contra_in_ff
                                                        - ipsi_vs_contra_in_cre
                                                                      |
                                         -----------------------------------------------
                                         |                                             |
                                         v                                             v
                            [ Supporting evidence ]                         [ Secondary results ]
                            - QC improved data                             - geno_in_contra
                            - alignment supports DE                        - geno_in_ipsi
                            - count handoff is usable                      - interaction
                                         |                                             |
                                         ------------------+--------------------------
                                                           |
                                                           v
                                                [ Draft 1 writing story ]
                                                - first path did real work
                                                - but did not yield the
                                                  strongest paper story
                                                - mouse_new produced the
                                                  usable main paper path
                                                - paper centers the DRG
                                                  side-specific DE signal
                                                - QC/alignment stay
                                                  supporting evidence
```

### Meaning

- the **first mouse path** matters because it was the first real attempt
- it produced real work, but **not the strongest paper story**
- that led to **`mouse_new` / `SRP618841`**
- `mouse_new` gave the usable main paper path
- the main Draft 1 paper story is:
  - **DRG family**
  - **side-specific contrasts**
  - **DE-centered**
  - **QC/alignment as support**

---

## 3) Detailed working mind map — Draft 1

This is the fuller Draft 1 working map for the actual `mouse_new` paper story.

```text
                                    [ BIOL550 journal-style paper ]
                                                   |
                                                   v
                               [ Need a strong and defensible analysis story ]
                                                   |
                 -------------------------------------------------------------------
                 |                                                                 |
                 v                                                                 v
      [ First mouse branch ]                                           [ Writing target ]
                 |                                                     - DE-centered paper
                 |                                                     - journal-style story
                 |                                                     - not a pipeline report
                 v
      [ First pipeline built and run ]
      - raw QC
      - trimming
      - alignment
      - DE
                 |
                 v
      [ First path produced outputs ]
                 |
                 v
      [ But not the cleanest main paper story ]
      - mixed structure
      - uneven contrast strength
      - harder to center one strong narrative
                 |
                 v
      [ Need a cleaner analytical path ]
                 |
                 v
      [ Bring in contingency dataset: SRP618841 / mouse_new ]
                 |
                 v
      [ Rebuild the workflow on mouse_new ]
      - raw QC
      - fastp cleanup
      - post-trim QC
      - STAR alignment
      - DESeq2
                 |
                 v
      [ New dataset is usable ]
      - cleaner main path
      - alignment supports DE
      - still not perfect
                 |
                 v
      [ Complexity remains ]
      - residual QC concerns
      - not all contrasts equally informative
      - interpretation still requires judgment
                 |
                 v
      [ One valid main family emerges ]
      - family_drg_novaseqx
                 |
                 v
      [ Main signal is side-specific DRG expression ]
      - ipsi_vs_contra_in_ff
      - ipsi_vs_contra_in_cre
                 |
                 +------------------------------+
                 |                              |
                 v                              v
      [ Secondary contrasts ]         [ Visual support ]
      - geno_in_contra                - PCA
      - geno_in_ipsi                  - volcano plots
      - interaction                   - heatmaps
                 |                              |
                 +---------------+--------------+
                                 |
                                 v
                 [ Final paper framing ]
                 - structure-aware DE analysis
                 - side is the main signal
                 - genotype is secondary
                 - QC/alignment are supporting evidence
```

### Meaning

- this is the fuller working story map for the first paper
- it keeps the first mouse branch visible
- it shows why `mouse_new` became the main paper path
- it keeps the final framing centered on DE, not pipeline setup

---

## 4) Mind map — Draft 2

```text
                                  [ Draft 2 ]
                                       |
        ----------------------------------------------------------------
        |                         |                    |                |
        v                         v                    v                v
 [ Draft 1 base ]        [ Add support ]      [ Strengthen logic ] [ Improve flow ]
        |                         |                    |                |
        v                         v                    v                v
 - main story exists      - add stronger        - connect claims    - improve section
 - main results chosen      support for main      to evidence          transitions
 - central vs support       results             - reduce weak or     - improve figure/
   already defined        - refine figures        distracting parts    table order
                          - add interpretation  - make hierarchy     - make the paper
                                                  clearer              easier to read
                                       |
                                       v
                              [ Stronger full draft ]
```

### Meaning

- Draft 2 should strengthen the paper that Draft 1 established
- main job:
  - improve support
  - improve logic
  - improve flow

---

## 5) Mind map — Draft 3

```text
                                  [ Draft 3 ]
                                       |
        ----------------------------------------------------------------
        |                         |                    |                |
        v                         v                    v                v
 [ Draft 2 base ]        [ Close gaps ]       [ Polish language ] [ Finalize package ]
        |                         |                    |                |
        v                         v                    v                v
 - strong main story      - fill missing        - tighten wording   - finalize figures
 - stronger support         sections            - improve tone      - finalize tables
 - clearer flow           - resolve weak links  - remove repetition - prepare near-final
                          - finish discussion   - improve clarity     submission draft
                                       |
                                       v
                              [ Near-final paper ]
```

### Meaning

- Draft 3 should make the paper near-final
- main job:
  - close gaps
  - polish language
  - finalize the package

---

## Quick pattern check

Looking across all maps together:

- Draft 1 is where the **real story is chosen**
- Draft 2 is where the **argument gets stronger**
- Draft 3 is where the **paper gets finished**
- the biggest risk area is still Draft 1:
  - if the main story is not clean there, later drafts only polish confusion

---

## Current use

Use this file when you want:

- one place to compare all drafting stages
- one place to see repeated weak points
- one place to check whether the paper story is staying consistent across drafts
