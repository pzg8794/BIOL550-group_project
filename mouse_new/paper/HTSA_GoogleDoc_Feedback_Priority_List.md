# HTSA Google Doc draft — prioritized feedback checklist

This document is a review checklist for the current Google Doc draft of the HTSA paper. It is organized by priority so the team can fix the most submission-critical problems first.

For each item, use the **Highlight this** text to locate the place in the Google Doc, use **Comment to leave** as the feedback text, and use **Why this change is needed** to explain the rationale to the team.

---

## High priority

### 1) Replace the current title with a paper-quality title
**Highlight this:**
`NGS Reanalysis Study On Identification Using Global DEG Discovery of DRG Mouse Dataset`

**Comment to leave:**
Replace this with a cleaner, publication-style title. The current title reads like a working placeholder rather than a final scientific paper title.

**Why this change is needed:**
The title is the first thing a reader sees, and right now it is grammatically awkward and scientifically vague.

---

### 2) Tighten the Introduction opening and remove sentence fragments
**Highlight this:**
`To understand the mechanism that balances the stress response and regenerative demands of neurons once injured.`

**Comment to leave:**
This is a sentence fragment. Fold it into the surrounding paragraph and make the transition from general neuro injury to the specific DRG/AhR study more direct.

**Why this change is needed:**
The Introduction should open with clean, complete sentences and a clear progression into the dataset being analyzed.

---

### 3) Remove informal / non-scientific phrasing in the Introduction
**Highlight this:**
`The paper we based our RNA-seq analysis on acts as a detective.`

**Comment to leave:**
Please replace this with formal scientific wording. Avoid metaphorical or conversational phrasing here.

**Why this change is needed:**
This wording weakens the tone of the paper and makes the Introduction read less like a scientific manuscript.

---

### 4) Remove over-claiming language in the Introduction
**Highlight this:**
`This is one step closer to treating spinal cord injuries and peripheral nerve damage.`

**Comment to leave:**
Please soften this claim. The current analysis is a reanalysis of an RNA-seq dataset and does not justify a treatment-oriented conclusion.

**Why this change is needed:**
The paper should distinguish between mechanistic interpretation and clinical impact.

---

### 5) Use one genotype terminology system throughout the paper
**Highlight this:**
Any mixture of `FF`, `WT`, `WT-control`, `wildtype`, `cKO`, and `cre`

**Comment to leave:**
Please choose one consistent genotype naming system and apply it throughout the entire paper. Since the Introduction defines ff/fl as the floxed control genotype, later sections should not drift between WT, WT-control, and FF unless that distinction is explicitly justified.

**Why this change is needed:**
Terminology drift is currently one of the biggest scientific consistency problems in the draft.

---

### 6) Verify all accession identifiers and keep them consistent everywhere
**Highlight this:**
`SRP618841 (BioProject PRJNA1322439; GEO GSE243308)` and all other accession strings

**Comment to leave:**
Please verify that SRP, BioProject, and GEO identifiers match the retained project metadata and are consistent everywhere in the paper.

**Why this change is needed:**
Accession inconsistency creates immediate credibility problems in Methods and makes the workflow harder to reproduce.

---

### 7) Fix the merged Methods heading / caption formatting error
**Highlight this:**
`Materials and MethodsFigure 1. Overview ribbon summarizing the four computational stages and their stage in the mouse`

**Comment to leave:**
The section heading and the figure caption are running together. Separate the heading from the figure caption and rewrite the caption so it is complete.

**Why this change is needed:**
This is a visible formatting problem that makes the draft look unfinished.

---

### 8) Eliminate duplicated section framing in Methods
**Highlight this:**
Both occurrences of `Representative Command Examples`

**Comment to leave:**
There are two different table blocks that currently use the same framing. Keep the command/example table under “Representative Command Examples,” but rename the second one to something like “Software, reference resources, and version tracking.”

**Why this change is needed:**
Repeated section titles make Methods feel disorganized and can confuse the reader about what each table is doing.

---

### 9) Fix duplicate table numbering
**Highlight this:**
`Table 2. Representative command examples...`
`Table 2. Summary of the 20-sample mouse DRG RNA-seq subset...`

**Comment to leave:**
Please renumber all tables sequentially. Table 2 is currently used twice.

**Why this change is needed:**
Duplicate table numbering breaks figure/table cross-referencing and makes the draft look incomplete.

---

### 10) Replace all unresolved placeholders before submission
**Highlight this:**
All remaining `Figure X`, `Table X`, and `[Waiting on figure]`

**Comment to leave:**
Please resolve all remaining placeholders and remove the waiting note before submission.

**Why this change is needed:**
These are direct signs that the paper is still in draft form.

---

### 11) Fix Methods wording about GO follow-up tools
**Highlight this:**
`enrichment outputs were further summarized using ShinyGO to develop shared-gene charts, tree, and network views`

**Comment to leave:**
Please verify and revise this wording. The workflow appears to use g:Profiler with ShinyGO-style reduction/visualization logic rather than ShinyGO itself as the primary enrichment engine.

**Why this change is needed:**
The Methods section should describe the actual analysis path precisely.

---

### 12) Tighten the broad GO Results and remove weak / unsupported language
**Highlight this:**
`these are fairly accurate`
`The paper's findings state that cKO should have a reduced stress response and should also be higher in axon regeneration. (Link).`
`Unexpectedly, the scatter plot appears to contradict the findings of the paper.`

**Comment to leave:**
Please rewrite this section in more formal scientific language, remove the placeholder link, and make the interpretation more careful. Right now the GO Results mix description, speculation, and contradiction too loosely.

**Why this change is needed:**
The GO section is currently the most vulnerable part of the paper scientifically.

---

### 13) Keep the GO Follow-up section, but finalize its numbering and figure logic
**Highlight this:**
`GO Follow-up of the Main Side-Specific Branches`
`Figure X. FF upregulated GO Biological Process follow-up shown as a ranked chart and shared-gene network.`
`Table X. Overlap summary...`
`Table X. Anchor-gene companion summary...`

**Comment to leave:**
This subsection is worth keeping, but the figures and tables still need final numbering, and the chart/network should be treated as separate full-width figure blocks if they are not shown side by side.

**Why this change is needed:**
This is one of the strongest late additions, so it should look finished and intentional.

---

### 14) Remove or finish incomplete Results sections
**Highlight this:**
`Overlap between the analysis in the paper and this project`
`Basically, our bendpoint approach for filtering DEGs is much tighter...`
`Alternative Splicing Analysis`

**Comment to leave:**
These sections are not ready for the main paper. Either finish them with real prose, figures, and citations, or remove them for now.

**Why this change is needed:**
Unfinished sections interrupt the flow of Results more than any other current issue.

---

### 15) Complete the References section in real APA format
**Highlight this:**
`References`
`Intro sources: ...`

**Comment to leave:**
The References section is still incomplete and contains note-style placeholders. Please convert all references into full APA entries and make sure every in-text citation has a matching reference.

**Why this change is needed:**
Incomplete references alone can make the draft non-submittable.

---

### 16) Move the final paper out of Google Docs before submission
**Highlight this:**
The requirement block at the top that says `Do not use Google Docs which creates formatting issues.`

**Comment to leave:**
Before final submission, export and finalize this paper in Word / LibreOffice / OpenOffice as required.

**Why this change is needed:**
This is explicitly listed in the assignment requirements.

---

## Medium priority

### 17) Make all main section headings consistent
**Highlight this:**
`Data Preparation: Reference Selection and Alignment`
`Results`
`Discussion`

**Comment to leave:**
Please make sure all main and subsection headings use a consistent heading hierarchy. Some section titles are still plain body text instead of proper headings.

**Why this change is needed:**
Consistent heading levels improve readability and make the manuscript structure clearer.

---

### 18) Standardize bend-point wording and notation
**Highlight this:**
`The bend-point in the ipsilateral vs contralateral in the WT branch occurred at a p-value of 1.37e-17`
`8.40 × 10-17`

**Comment to leave:**
Please standardize this to “adjusted p-value threshold” and use consistent scientific notation formatting throughout.

**Why this change is needed:**
The paper currently shifts between p-value wording styles and notation styles.

---

### 19) Keep Results and Discussion from repeating the same claim too many times
**Highlight this:**
Any repeated statements that `side-specific injury contrasts carried the strongest signal` or that the `WT/FF branch remained the clearest pathway-level result`

**Comment to leave:**
This point is important, but it appears multiple times in Results and again in Discussion. Keep the full explanation in one place and shorten the repeated versions.

**Why this change is needed:**
Too much repetition makes the paper feel longer without making it stronger.

---

### 20) Keep GO redundancy-reduction language in Results, not repeated in full in Discussion
**Highlight this:**
`Once shared-gene structure was examined through the chart, tree, and network views...`

**Comment to leave:**
The detailed redundancy-reduction explanation belongs primarily in Results. Discussion should keep only the take-home interpretation.

**Why this change is needed:**
This helps separate observation from interpretation.

---

### 21) Clarify the transition from general neuro injury to the actual dataset
**Highlight this:**
The first three Introduction paragraphs

**Comment to leave:**
Please tighten the transition from broad neurological injury background to the specific mouse DRG sciatic nerve injury dataset.

**Why this change is needed:**
Right now the paper starts broadly, then shifts abruptly into the Ahr paper and the experimental design.

---

### 22) Clean up the explanation of FF / floxed controls
**Highlight this:**
`This tag by itself has no effect-- de facto acting as a wildtype--`

**Comment to leave:**
Please rewrite this more formally and consistently with the genotype terminology used elsewhere.

**Why this change is needed:**
The explanation is useful, but the wording is still conversational.

---

### 23) Rename or rewrite the scatter-plot comparison paragraph if kept
**Highlight this:**
`Unexpectedly, the scatter plot appears to contradict the findings of the paper.`

**Comment to leave:**
If this analysis stays, please frame it more carefully. State what the plot shows first, then explain the possible interpretation, rather than opening with “contradict.”

**Why this change is needed:**
That wording sounds too strong for a comparison result that still needs careful interpretation.

---

### 24) Keep table titles above tables consistently
**Highlight this:**
Any table whose title appears after the table or is visually separated from it

**Comment to leave:**
Please place all table titles above the corresponding tables and keep the formatting consistent across the paper.

**Why this change is needed:**
Consistent table placement makes the Results and Methods easier to scan.

---

### 25) Make figure captions describe the actual image shown
**Highlight this:**
Any caption that combines multiple panels or says `A/B/C` when the image placement does not clearly match that structure

**Comment to leave:**
Please check each caption against the actual displayed figure layout. Some captions still describe multi-panel structures more clearly than the document layout does.

**Why this change is needed:**
Mismatched captions confuse the reader and weaken the credibility of the figure.

---

### 26) Add final numbering and consistent cross-references for GO Follow-up tables
**Highlight this:**
`Table X. Overlap summary for the two narrowed side-specific branches`
`Table X. Anchor-gene companion summary for the FF GO follow-up`

**Comment to leave:**
These are useful additions. Please give them final table numbers and refer to them explicitly in the surrounding Results text.

**Why this change is needed:**
The new section will read more like an integrated manuscript section and less like a pasted add-on.

---

### 27) Verify all citations attached to Methods statements
**Highlight this:**
Any sentence that pairs workflow implementation details with citations, especially the opening Methods paragraphs and tool descriptions

**Comment to leave:**
Please verify that each citation supports the exact claim it is attached to. Tool citations, dataset citations, and workflow rationale citations should stay distinct.

**Why this change is needed:**
This helps avoid citation drift where references are correct in general but not precise for the sentence.

---

## Low priority

### 28) Standardize species, gene, and protein styling
**Highlight this:**
Occurrences of `Mus musculus`, `Ahr`, `ATF3`, `Jun`, `Sox11`, etc.

**Comment to leave:**
Please make gene/protein/species formatting consistent throughout the paper.

**Why this change is needed:**
This is a polish issue, but it helps the manuscript look more professional.

---

### 29) Standardize hyphenation and comparison wording
**Highlight this:**
Mixed uses of `ipsilateral vs contralateral`, `ipsilateral-versus-contralateral`, `WT vs cKO`, `WT versus cKO`

**Comment to leave:**
Please choose one style for comparison wording and use it consistently.

**Why this change is needed:**
Consistency improves readability and reduces copy-editing noise.

---

### 30) Replace casual wording in Results where possible
**Highlight this:**
Phrases like `these are fairly accurate`, `de facto acting as a wildtype`, `Basically, our bendpoint approach...`

**Comment to leave:**
Please replace informal phrasing with formal scientific wording.

**Why this change is needed:**
The paper already has enough strong content that it does not need casual language.

---

### 31) Keep workflow table colors aligned with the Methods stage palette
**Highlight this:**
Stage-based tables in Methods and the two new GO follow-up tables

**Comment to leave:**
Please keep the workflow tables color-coded consistently: Collection = blue, Cleaning = orange, Preparation = green, Analysis = lavender. The GO follow-up tables should use the Analysis palette.

**Why this change is needed:**
The visual design is stronger when the stage logic is consistent across the whole paper.

---

### 32) Add a final author-color note if the instructor still expects it
**Highlight this:**
The requirement text at the top that says to include one comment identifying each person’s revision color

**Comment to leave:**
Before submission, make sure the required author-contribution color note is still present in the final exported file if the assignment still expects it.

**Why this change is needed:**
This is a small compliance detail, but it is explicitly mentioned in the assignment notes.

---

## Recommended fix order

1. Title
2. Introduction cleanup and tone fixes
3. Genotype terminology consistency
4. Methods formatting / numbering / accession verification
5. Resolve all placeholders, missing figures, and incomplete sections
6. Tighten the broad GO Results
7. Finalize the GO Follow-up section and its numbering
8. Clean repetition in Discussion
9. Complete APA References
10. Final formatting polish in Word / LibreOffice
