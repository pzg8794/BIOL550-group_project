# Paper drafting strategy — recommended team guide

This version keeps the useful parts of the original mind maps, but turns them into a clearer **paper-writing strategy** for a team that has not written a paper before.

## Main recommendation

Use a **story-first drafting strategy**.

That means the team should not organize the paper mainly around:

- the order in which analyses happened
- the history of failed and improved paths
- pipeline chronology

Instead, the team should organize the paper around:

- the **main claim** of the paper
- the **strongest evidence** supporting that claim
- the **supporting evidence** that strengthens confidence
- the **secondary results** that add context but do not lead the story

Mind maps are still useful, but they should support the paper story rather than replace it.

If needed, we can also nest one mind map inside another, as long as the levels stay clear:

- high-level paper map
- draft-level map
- section/story map

---

## Core rule for this team

Before writing sections, the team must agree on four things:

1. **What is the paper's main claim?**
2. **Which result is the strongest support for that claim?**
3. **Which results are support only, not the center of the story?**
4. **What does each draft need to accomplish?**

If those four points are clear, the paper becomes much easier to draft.

---

## 1) High-level strategy map — from planning to final paper

```text
                              [ Final paper ]
                                     ^
                                     |
                     -----------------------------------
                     |                |                |
                     |                |                |
                     |                |                |
                [ Draft 3 ]      [ Draft 2 ]      [ Draft 1 ]
                     ^                ^                ^
                     |                |                |
              - polish text      - strengthen     - lock the main
              - close gaps         argument          paper story
              - finalize         - improve        - choose main claim
                figures/tables     support        - choose main results
              - prepare          - improve flow   - define support vs
                near-final                         secondary results
                version
                                                      ^
                                                      |
                                           [ High-level planning ]
                                           - define paper goal
                                           - align the team
                                           - agree on paper claim
                                           - agree on draft roles
```

### Meaning

- **High-level planning** sets the writing target.
- **Draft 1** is the most important stage because it fixes the main story.
- **Draft 2** strengthens the argument and improves structure.
- **Draft 3** finishes and polishes the paper.
- The paper should move from **claim selection** to **argument strengthening** to **final packaging**.

Across all drafts, this planning layer still feeds a standard journal-style paper with the usual required sections:

- Introduction
- Materials and Methods
- Results
- Discussion
- References

---

## 2) Main paper strategy map — how Draft 1 should actually be built

```text
                         [ Draft 1: build the paper story ]
                                        |
        -----------------------------------------------------------------
        |                       |                      |                 |
        v                       v                      v                 v
 [ Main claim ]         [ Strongest evidence ]  [ Supporting evidence ] [ Secondary results ]
        |                       |                      |                 |
        v                       v                      v                 v
 - one clear paper       - result family that    - QC shows data      - useful, but not the
   message                 best supports claim     quality improved      main paper driver
 - DE-centered story     - must lead figures     - alignment supports - can appear later or
 - DRG side-specific     - should anchor           DE interpretation     in support sections
   signal is central       Results section       - count handoff usable - should not compete
                                                                            with the main claim
                                        |
                                        v
                           [ Section and figure outline ]
                           - Introduction points to the question
                           - Results lead with strongest evidence
                           - supporting analyses follow
                           - Discussion explains meaning and limits
```

### Meaning

Draft 1 should not begin with “what happened first in the project.”

Draft 1 should begin with:

- the **main claim**
- the **best evidence**
- the **supporting evidence**
- the **secondary evidence**
- the section order that follows this logic

### Checklist for Draft 1

By the end of Draft 1, we should have:

- one main claim in 1 sentence
- one main family/result path locked
- 1–2 core figures named
- one short statement explaining what is supporting evidence only
- one short PCA interpretation that explains the dominant sample structure before gene-level interpretation
- one clear rule for narrowing very large significant-gene lists without relying only on an arbitrary top-N cutoff

---

## 3) Draft 1 story map — applied to this project

```text
                           [ Draft 1 paper story for this project ]
                                              |
                 ------------------------------------------------------------------
                 |                         |                        |               |
                 v                         v                        v               v
         [ Paper goal ]          [ Main analytical path ]   [ Supporting evidence ] [ Secondary results ]
                 |                         |                        |               |
                 v                         v                        v               v
      - journal-style paper      - SRP618841 / mouse_new     - QC improved data   - geno_in_contra
      - DE-centered story        - family_drg_novaseqx       - alignment supports - geno_in_ipsi
      - strong analysis claim    - strongest usable path       DE                 - interaction
                                 - cleaner paper story       - PCA interpreted
                                                              first to confirm
                                                              side-driven structure
                                                            - processing steps
                                                              justify confidence
                                              |
                                              v
                               [ Main result to center the paper ]
                               - side-specific DRG expression signal
                               - ipsi_vs_contra_in_ff
                               - ipsi_vs_contra_in_cre
                                              |
                                              v
                           [ Large DE list handling for Draft 1 ]
                           - do not rely only on arbitrary top-100 lists
                           - use p-value distribution / cumulative bend logic
                             if a principled cutoff is needed
                           - use GO/pathway analysis after narrowing, not as a
                             replacement for understanding the main signal
                                              |
                                              v
                                   [ Decision: main paper center ]
                         - center the paper on the side-specific DE signal
                         - keep QC/alignment as support, not the paper's core
                         - treat genotype-related results as secondary unless they
                           become stronger than the side-specific contrasts
```

### Meaning

For this project, the cleanest Draft 1 strategy is:

- center the paper on the **side-specific DRG differential expression signal**
- use **`mouse_new` / `SRP618841`** as the main analysis path
- treat **QC and alignment** as support for trustworthiness
- treat **secondary contrasts** as additional context, not the lead story

### Decision points locked by Draft 1

- **Decision:** `mouse_new` / `SRP618841` is the main paper path
- **Decision:** `family_drg_novaseqx` is the main family
- **Decision:** side-specific DRG DE signal is primary
- **Decision:** QC/alignment are support, not the paper center

### Checklist for this project's Draft 1

By the end of Draft 1, we should have:

- the main claim written in 1 sentence
- `ipsi_vs_contra_in_ff` and `ipsi_vs_contra_in_cre` named as the central results
- 1–2 hero figures selected
- a short PCA interpretation showing that side-class structure is the first thing to explain
- a short paragraph explaining why the first mouse path is not the main Results center
- a short paragraph defining what stays supporting vs secondary
- a short note explaining how very large significant-gene lists will be narrowed without using only an arbitrary cutoff

---

## 4) Where the first mouse path belongs

The first mouse path still matters, but it should not dominate the paper map.

It belongs in the team's background reasoning:

```text
                     [ First mouse path ]
                              |
                              v
                    - important first attempt
                    - real workflow development
                    - real outputs produced
                    - helped reveal weak points
                              |
                              v
                  [ Why it is not the paper center ]
                  - no single clean main story
                  - uneven contrast strength
                  - harder to build a focused narrative
                              |
                              v
                 [ Team lesson, not main Results structure ]
```

### Meaning

This part is useful for team understanding, but it should mostly stay in:

- planning notes
- meeting notes
- methods reasoning
- limited framing in the manuscript if needed

It should **not** become the main structure of the Results section.

One practical rule:

- each important box in the Draft 1 map should connect to at least one concrete repo artifact
  - figure
  - table
  - notebook output
  - methods paragraph

---

## 5) Draft-by-draft writing strategy

### Draft 1 — choose and lock the story

Main job:

- define the paper's main claim
- choose the strongest result path
- interpret the PCA before over-reading gene-level outputs
- separate central evidence from supporting evidence
- build a figure order that matches the story
- define how large significant-gene lists will be narrowed
- produce a usable Results backbone

Success test:

- a reader can say in one sentence what the paper claims
- a reader can identify which result is the main evidence

Checklist:

- one-sentence main claim exists
- main result family is locked
- 1–2 core figures are chosen
- central/supporting/secondary split is explicit

Draft 1 risk:

- if Draft 1 is weak, later drafts will polish confusion instead of clarity

---

### Draft 2 — strengthen the argument

Main job:

- improve links between claims and evidence
- expand interpretation where needed
- remove weak or distracting parts
- improve transitions and section order
- refine figures and tables

Success test:

- the paper feels logically connected
- each section clearly supports the central claim

Checklist:

- every main claim points to at least one figure or table
- every figure is mentioned in the Results text
- transitions explain the “so what”

---

### Draft 3 — finish the paper

Main job:

- close missing gaps
- tighten wording
- reduce repetition
- strengthen discussion and limitations
- finalize the submission package

Success test:

- the paper reads as one coherent argument
- figures, text, and conclusions align cleanly

Checklist:

- all required sections are present
- no placeholder or TODO language remains
- terminology is consistent across text, figures, and tables

---

## 6) Working rule for the team

When deciding whether to include a result, ask:

**Does this result strengthen the main claim, support confidence in the main claim, or distract from the main claim?**

Use the answers this way:

- if it **defines the claim**, it is central
- if it **supports confidence**, it is supporting evidence
- if it is interesting but not essential, it is secondary
- if it distracts from the story, remove it from the main draft

---

## 7) Recommended use of this document

Use this file as the team's main drafting guide when:

- deciding what the paper is really about
- choosing the Results section order
- deciding what belongs in Draft 1, Draft 2, and Draft 3
- checking whether a new analysis strengthens or weakens the current story

Keep older, more chronological maps as supporting planning documents, not as the main writing structure.
