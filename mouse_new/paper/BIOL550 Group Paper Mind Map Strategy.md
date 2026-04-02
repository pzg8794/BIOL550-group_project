# BIOL550 Group Paper Mind Map Strategy

## Overview

This document lays out a simple, repeatable mind‑map strategy your team can use to plan and write the BIOL550 group paper, especially for teammates who have not written scientific papers before. The goal is to help everyone see the whole story at once, then turn that visual map into the required IMRAD‑style manuscript (Introduction, Materials and Methods, Results, Discussion).[^1]

## Why this strategy fits BIOL550

The BIOL550 syllabus specifies that the final paper is a group-written, journal‑style manuscript with standard scientific sections and substantial prose, not just figures. Drafts are due in three stages (outline, half text, nearly complete), so a visual planning tool that becomes an outline is especially useful.[^2][^1]

The analysis work in BIOL550 is organized into stages (first, second, and third‑stage analyses), which naturally become major branches in a mind map tied to your figures and results. Connecting those stages to a single biological question in the center of the map keeps the paper focused instead of reading like a methods tour.[^1]

## Core idea: "Story‑first IMRAD" mind map

This strategy combines two widely used writing practices:

- Start from a single-sentence central message and the key figures/tables that support it.
- Organize everything into the standard IMRAD structure that BIOL550 requires.[^1]

In the mind map, there is one root node in the center and four major content branches around it, plus a branch for project management:

1. Central question and take‑home message.
2. Data and analysis pipeline (aligned with BIOL550 analysis stages).
3. Figures and tables.
4. Paper sections (IMRAD + title/abstract).
5. Project management (who owns what, and by when).

## Recommended mind map structure

Below is a suggested structure written as a Mermaid mind map that you can paste directly into a `.md` file on GitHub (for example, in the `BIOL550` or `mouse_group_project_work` repositories). Many markdown renderers on GitHub understand Mermaid diagrams.

```mermaid
mindmap
  root((Group Paper: Biological Story))
    Central_question[Central biological question]
      System[Study system and phenotype]
      Gap[What is not known (knowledge gap)]
      Hypothesis[Main hypothesis or guiding question]
    Data_and_Design[Data & experimental design]
      Samples[Samples and conditions]
      Sequencing[Sequencing platform & library prep]
      Design_notes[Key design choices (replicates, controls)]
    Analysis_pipeline[Analysis pipeline (course stages)]
      Stage1[Stage 1: QC & preprocessing]
      Stage2[Stage 2: Alignment / assembly]
      Stage3[Stage 3: Quantification & differential analyses]
      Extras[Optional: bonus or exploratory analyses]
    Figures_Tables[Figures & tables]
      Fig1[Figure 1: Study system / experimental design]
      Fig2[Figure 2: QC and alignment summaries]
      Fig3[Figure 3: Key biological result 1]
      Fig4[Figure 4: Key biological result 2]
      Table1[Table 1: Samples, libraries, or parameter settings]
    Paper_Sections[Paper sections (IMRAD)]
      Intro[Introduction: context, gap, question]
      Methods[Materials & Methods: data and pipeline]
      Results[Results: organized around Figures 2–4]
      Discussion[Discussion: interpret results, limitations, future work]
      Title_Abstract[Title & Abstract: written last]
    Project_Management[Project management]
      Roles[Assign section owners and figure leads]
      Deadlines[Internal deadlines aligned to course drafts]
      Versioning[Git workflow: branches, pull requests, review]
```

If your existing mind map already follows this basic structure, it is a solid strategy and can be kept with minor refinements. If it is currently method‑or tool‑centric (e.g., each branch is "FastQC", "STAR", "DESeq2"), consider realigning it to this story‑first layout so that analysis choices are always attached to a biological question and a specific result figure.

## How to use the map with your team

### Step 1: Agree on the central node

- In a meeting, force the team to agree on a one‑sentence answer to: "What is the main biological question and take‑home message of this paper?"  
- Put that sentence (or a short version of it) in the central node and do not change it lightly; this keeps later writing decisions consistent.

### Step 2: Populate the data and analysis branches

- Under **Data & experimental design**, list concrete details: sample types, treatments, time points, and any constraints from the original dataset.
- Under **Analysis pipeline**, mirror the stages of analysis you actually completed (e.g., QC, alignment, quantification, differential expression, variant calling, assembly) and attach key commands or tools only where they matter for interpretation.

### Step 3: Draft figures and tables before prose

- For each major result you want in the paper, create a node under **Figures & tables** and write a one‑line caption describing what the reader should learn from that figure.
- Check that every analysis step on the pipeline branch leads to at least one figure/table; if not, either drop that analysis from the paper or decide what concrete evidence it contributes.

### Step 4: Map figures to sections

- Draw mental (or explicit) connections between each figure node and the **Results** subsection that will describe it.
- Ensure that:
  - The **Introduction** justifies why each result matters (link to central question and gap).
  - The **Methods** contain enough detail for a reader to reproduce how each figure was generated.
  - The **Discussion** revisits the central question and interprets each key figure.

### Step 5: Turn the mind map into an outline

Once the map feels stable, export it as a linear outline that can become Draft 1 for the course:

- Each first‑level branch (Central question, Data & design, Analysis, Figures, Sections) becomes a top‑level bullet in a text outline.
- Sub‑nodes under **Paper sections** become section and subsection headings (e.g., "Results – Differential expression between X and Y").
- The bullet under each figure node becomes the topic sentence of the corresponding Results paragraph.

This outline can directly satisfy the Week 13 "outline" draft requirement and set you up for the later drafts that add prose around this structure.[^2][^1]

## Using the map for collaboration and Git workflows

Because your work lives in repositories like `BIOL550` and `mouse_group_project_work`, the mind map and this strategy can be used to coordinate code and writing:

- Store this `.md` file in the repo (for example, `doc/paper_mindmap_strategy.md`) so everyone has a shared reference.
- Add a simple checklist under **Project management** mapping each section/figure node to a specific person and a branch name.
- Before a teammate opens a pull request, they verify that their changes clearly attach to one or more nodes on the map (e.g., "implements Figure 2: QC summary").

Keeping analysis, figures, and prose all tied back to the same map reduces duplicated work and makes it easier for newer writers to see how their piece fits into the whole manuscript.

---

## References

1. [BIOL550-Syllabus-High-Throughput-Sequencing-Analysis.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_416f7a35-e40e-4375-a80e-9a5ae07af411/9237f744-6ecd-4a66-bd1f-2b9ca9d13ea2/BIOL550-Syllabus-High-Throughput-Sequencing-Analysis.pdf?AWSAccessKeyId=ASIA2F3EMEYESFSK4DZN&Signature=Gcoc5%2FInirwtnzheQjXyMrwnBJE%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIG2UOHgrcVlB1DHJgfYE1pFWqJEvAWUWPzzaMRCAiq4%2BAiAZWHoaitFK8RdYT3zeUjp%2FtUxToETGCP9q7CaCUXD6WirzBAhNEAEaDDY5OTc1MzMwOTcwNSIMrEZZR3rjF9U8NZskKtAE0qyRLp7nEgl%2BzFhe5WaFgA0s3%2FGWIr6EWkmLOM7HURM1kNjP8XyE0uIywQqkTbF26tUOdvl69IK75ujtk57iSnAOthIcMqiQNCSI3UV5gB6OCEaRYdQEK%2FfpB7vl1UrjJ%2FCuirRSyZ0b8oP67R5ZSRjzvtY6V4uDqYJALxtLToPBL5dV28C8k09XeUEHjMZmGBxXIy11tgDWRJCkf2G68QhgkULkDgm9H7zpfgBg0MBGFV7%2FfNlHVlB4rzRQhun4lVrhYZUiwXw0Xu2nN1iamu%2FRNaW8ggxix1uwH3JiC%2B0Yp%2BQL3CEDzBvptvVz0AHpitWZY1Nnv3RAAqV4S8GC2CQQzoMjOdgBQFHWGP%2Bfl1FbLWs%2BfRkS7I2ccy1pqmyYkL14JbOgMCMBBDOosDinvTlMN6JfSdr3G3o2erIGbfjWcJNJZuwonIdMdqiJYM2KmL2fUi8JxEXNjIOKYSKZhMKFBfmWeZD%2BF6y23BVJDweG8hXLl1KHWci1KXbrRwDmXTDJHRHqvfPt8Os%2FE%2FhjkF96JghfBjofbZIwOcaXm%2FjJpV52CYYxK%2F8RoQ4bR3nLD2sPU76kttEhvwGn%2F0NzdstVslvUObchNbTTxH4YRUJgplV%2FFXaqt5eelLi9AscwkZYQN7w1osR93Z%2BeVxZ1qAjSe29zVecsY5jVK5X6ASVj2QOSGLErlVEBaARM0Dx6O8s3V9i4FCuMKBoEOYYiBL9VMMwCFGWlZiXlDLClpjDAFtQeBpwjIon%2B%2BZdb4dK3Hdy1WdMhKfEQ23YbChjG5jCMprLOBjqZAS%2Bh0OD%2B0hpBq08Cz2DgFSiZEXMbDXSIDwNFP5Lfj5E3AfgiHOPf7xHluoMGZKA6M9PnH%2Bmf6QINyzEtM9%2BilQyg9KW1v9vzKRd14q9gMa22wSseWsIJZUhxuVhZQZH8XJAEABWJRkoDebGorys86S31jNKU8vtSNe%2FGdOkC9kv%2Fkol6OkNGlujBs6cneNjvw2%2B1KxCHlKhOuw%3D%3D&Expires=1775018207) - HTS Analysis High Throughput Sequencing Analysis Spring 2026 Evolving syllabus Subject to some chang...

2. [Spring-2026-Academic-Strategy-Plan.docx](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_416f7a35-e40e-4375-a80e-9a5ae07af411/ce030495-c2de-4980-9040-e5a53e8153ca/Spring-2026-Academic-Strategy-Plan.docx?AWSAccessKeyId=ASIA2F3EMEYESFSK4DZN&Signature=yXfqVnRP94bSsGCO5ZzgRbq2C1w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIG2UOHgrcVlB1DHJgfYE1pFWqJEvAWUWPzzaMRCAiq4%2BAiAZWHoaitFK8RdYT3zeUjp%2FtUxToETGCP9q7CaCUXD6WirzBAhNEAEaDDY5OTc1MzMwOTcwNSIMrEZZR3rjF9U8NZskKtAE0qyRLp7nEgl%2BzFhe5WaFgA0s3%2FGWIr6EWkmLOM7HURM1kNjP8XyE0uIywQqkTbF26tUOdvl69IK75ujtk57iSnAOthIcMqiQNCSI3UV5gB6OCEaRYdQEK%2FfpB7vl1UrjJ%2FCuirRSyZ0b8oP67R5ZSRjzvtY6V4uDqYJALxtLToPBL5dV28C8k09XeUEHjMZmGBxXIy11tgDWRJCkf2G68QhgkULkDgm9H7zpfgBg0MBGFV7%2FfNlHVlB4rzRQhun4lVrhYZUiwXw0Xu2nN1iamu%2FRNaW8ggxix1uwH3JiC%2B0Yp%2BQL3CEDzBvptvVz0AHpitWZY1Nnv3RAAqV4S8GC2CQQzoMjOdgBQFHWGP%2Bfl1FbLWs%2BfRkS7I2ccy1pqmyYkL14JbOgMCMBBDOosDinvTlMN6JfSdr3G3o2erIGbfjWcJNJZuwonIdMdqiJYM2KmL2fUi8JxEXNjIOKYSKZhMKFBfmWeZD%2BF6y23BVJDweG8hXLl1KHWci1KXbrRwDmXTDJHRHqvfPt8Os%2FE%2FhjkF96JghfBjofbZIwOcaXm%2FjJpV52CYYxK%2F8RoQ4bR3nLD2sPU76kttEhvwGn%2F0NzdstVslvUObchNbTTxH4YRUJgplV%2FFXaqt5eelLi9AscwkZYQN7w1osR93Z%2BeVxZ1qAjSe29zVecsY5jVK5X6ASVj2QOSGLErlVEBaARM0Dx6O8s3V9i4FCuMKBoEOYYiBL9VMMwCFGWlZiXlDLClpjDAFtQeBpwjIon%2B%2BZdb4dK3Hdy1WdMhKfEQ23YbChjG5jCMprLOBjqZAS%2Bh0OD%2B0hpBq08Cz2DgFSiZEXMbDXSIDwNFP5Lfj5E3AfgiHOPf7xHluoMGZKA6M9PnH%2Bmf6QINyzEtM9%2BilQyg9KW1v9vzKRd14q9gMa22wSseWsIJZUhxuVhZQZH8XJAEABWJRkoDebGorys86S31jNKU8vtSNe%2FGdOkC9kv%2Fkol6OkNGlujBs6cneNjvw2%2B1KxCHlKhOuw%3D%3D&Expires=1775018207) - Piter Garcia PhD Bridge Program Spring 2026 University of Rochester Warner School of Education RIT D...

