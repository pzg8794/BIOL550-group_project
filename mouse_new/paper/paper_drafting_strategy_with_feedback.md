# Paper drafting strategy — final team guide

This guide keeps the useful parts of the earlier mind maps, but organizes them as a clearer **story-first paper-writing strategy** for a team that has not written a paper before.

The goal is to help the team move from **choosing the story** in **Draft 1**, to **strengthening the argument** in **Draft 2**, to **finishing the paper** in **Draft 3** for the BIOL550 final paper.

In BIOL550, this guide maps to the course paper schedule:

- **Draft 1 / Week 13** = outline of the paper
- **Draft 2 / Week 14** = draft of half of the text
- **Draft 3 / Week 15** = draft of the rest of the paper

We are using the term:

- **mind map**

---

## Main recommendation

Use a **story-first drafting strategy**.

That means the team should not organize the paper mainly around:

- the order in which analyses happened
- the history of failed and improved paths
- pipeline chronology

Instead, the team should organize the paper around:

- the **main claim** of the paper
- the **strongest evidence** supporting that claim
- the **supporting evidence** that strengthens confidence in that claim
- the **secondary results** that add context but do not lead the story

Mind maps are still useful, but they should support the paper story rather than replace it.

If needed, one mind map can sit inside another, as long as the levels stay clear:

- high-level paper map
- draft-level map
- section or story map

---

## Core rule for this team

Before writing sections, the team should agree on five things:

1. **What is the paper's main claim?**
2. **Which result is the strongest support for that claim?**
3. **Which results are support only, rather than the center of the story?**
4. **Which results are secondary and should not lead the paper?**
5. **What does each draft need to accomplish?**

If those five points are clear, the paper becomes much easier to draft.

A practical rule for this team:

- write the **one-sentence main claim** early
- revise it as the draft improves
- use it to decide what stays central, supporting, secondary, or out

---

## 1) High-level mind map — from planning to final paper

```text
## 1) High-level strategy map — from planning to final paper

```text
                               [ Final paper ]
                                       |
        -----------------------------------------------------------------
        |                         |                      |                |
        v                         v                      v                v
 [ High-level planning ]    [ Draft 1 ]            [ Draft 2 ]      [ Draft 3 ]
        |                         |                      |                |
        |                         |                      |                |
        v                         v                      v                v
 - define the overall      - establish the         - expand the      - complete the
   paper direction           main paper story        paper             full paper
 - align the team          - choose the main       - strengthen      - refine flow
 - define what each          results/story           logic           - close gaps
   draft should do         - decide what is        - add more        - polish wording
                           central vs support        support         - finalize figures
                           - use the Draft 1       - improve           and tables
                             story map               connections
```

### Meaning

- **High-level planning** sets the writing target before section drafting starts.
- **Draft 1** is the most important stage because it fixes the main story.
- **Draft 2** strengthens the argument and improves the paper's internal logic.
- **Draft 3** closes gaps and prepares the near-final submission version.
- The work order should read in the same direction as the drafting process:
  - **High-level planning -> Draft 1 -> Draft 2 -> Draft 3 -> Final paper**

Across all drafts, this planning layer still feeds a standard journal-style paper with the usual required sections:

- Introduction
- Materials and Methods
- Results
- Discussion
- References

The **Materials and Methods** section should describe the main analysis path clearly and only mention earlier exploratory paths when they help explain a design choice.

---

## 2) Draft 1 framework — how to build the paper story

This is the **generic Draft 1 framework**. It explains how Draft 1 should work for any project.

```text
                         [ Draft 1: build the paper story ]
                                        |
        -----------------------------------------------------------------
        |                       |                      |                 |
        v                       v                      v                 v
 [ Main claim ]         [ Strongest evidence ]  [ Supporting evidence ] [ Secondary results ]
        |                       |                      |                 |
        v                       v                      v                 v
 - one clear paper       - result family that    - data-quality and    - useful, but not the
   message                 best supports claim     analysis checks       main paper driver
 - central biological    - should lead figures     strengthen trust    - can appear later or
   or analytical signal  - should anchor the     - supporting results   in support sections
   is explicit             Results section         increase confidence - should not compete
 - story is focused      - should appear early     in the main result    with the main claim
                                        |
                                        v
                           [ Section and figure outline ]
                           - Introduction sets up the question
                           - Results lead with strongest evidence
                           - supporting analyses follow
                           - Discussion explains meaning and limits
```

### Meaning

Draft 1 should not begin with **what happened first in the project**.

Draft 1 should begin with:

- the **main claim**
- the **best evidence**
- the **supporting evidence**
- the **secondary evidence**
- the section and figure order that follows this logic

For the current DRG mouse project, this likely means a **DE-centered story** in which the **side-specific DRG signal** is central. Other projects should substitute their own main signal here.

### Checklist for Draft 1 (any project)

By the end of Draft 1, the team should have:

- one main claim written in 1 sentence
- one main result family or analysis path locked
- 1 to 2 core figures selected
- one short statement explaining what counts as supporting evidence only
- one short statement explaining what is secondary and should not lead the paper
- one Results outline in the order the reader should encounter the story
- one short PCA interpretation that explains the dominant sample structure before gene-level claims
- one clear rule for narrowing very large significant-gene lists without relying only on an arbitrary top-N cutoff

Write the current one-sentence main claim here:

- `__________________________________________________`

---

## 3) Draft 1 application — this project

This is the **project-specific Draft 1 map**. It applies the generic Draft 1 framework above to the current mouse and DRG paper story.

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
                                                              support confidence
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
                           - reserve GO/pathway analysis as a later interpretive
                             step after narrowing
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

### Decision points that should be locked by Draft 1

These should not change in later drafts unless there is a very strong new reason:

- **Decision:** `mouse_new` / `SRP618841` is the main paper path.
- **Decision:** `family_drg_novaseqx` is the main family.
- **Decision:** side-specific DRG differential expression is the primary signal.
- **Decision:** QC and alignment are support, not the paper center.

### Checklist for this project's Draft 1

By the end of Draft 1, the team should have:

- the main claim written in 1 sentence
- `ipsi_vs_contra_in_ff` and `ipsi_vs_contra_in_cre` named as the central results
- 1 to 2 hero figures selected
- a short PCA interpretation showing that side-class structure is the first thing to explain
- a short paragraph explaining why the first mouse path is not the main Results center
- a short paragraph defining what stays **supporting** vs **secondary**
- a short note explaining how very large significant-gene lists will be narrowed without using only an arbitrary cutoff

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

- **Draft 2** should strengthen the paper that Draft 1 established.
- Main jobs:
  - improve support
  - improve logic
  - improve flow

### Draft 2 checklist

By the end of Draft 2, the team should have:

- stronger links between claims and figures
- cleaner transitions between Results subsections
- clearer hierarchy between central, supporting, and secondary evidence
- revised figures and tables that support the main claim more directly

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

- **Draft 3** should make the paper near-final.
- Main jobs:
  - close gaps
  - polish language
  - finalize the package

### Draft 3 checklist

By the end of Draft 3, the team should have:

- all required sections present
- no placeholder or TODO language remaining
- consistent terminology across text, figures, and tables
- a coherent argument from title through conclusion

---

## 6) Where the first mouse path belongs

The first mouse path still matters, but it should not dominate the paper map.

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
- limited manuscript framing if needed

It should **not** become the main structure of the Results section.

One practical rule:

- each important box in the Draft 1 map should connect to at least one concrete project artifact:
  - figure
  - table
  - notebook output
  - methods paragraph

For this course, that means connecting boxes to the actual scripts, notebooks, figures, tables, and manuscript files the team is creating in its working repositories and writing folders.

---

## 7) Working rule for the team

When deciding whether to include a result, ask:

**Does this result define the main claim, strengthen confidence in the main claim, add useful context, or distract from the main claim?**

Use the answers this way:

- if it **defines the claim**, it is central
- if it **strengthens confidence**, it is supporting evidence
- if it adds context but is not essential, it is secondary
- if it distracts from the story, remove it from the main draft

---

## 8) Recommended use of this document

Use this file as the team's main drafting guide when:

- deciding what the paper is really about
- choosing the Results section order
- deciding what belongs in Draft 1, Draft 2, and Draft 3
- checking whether a new analysis strengthens or weakens the current story
- deciding whether a result belongs in the main paper, a support section, or outside the draft entirely

Keep older, more chronological maps as supporting planning documents, not as the main writing structure.
