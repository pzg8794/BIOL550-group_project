# HTSA Google Doc draft — prioritized feedback checklist with suggested replacements

This document is a review checklist for the current Google Doc draft of the HTSA paper. It is organized by priority so the team can fix the most submission-critical problems first.

For each item, use the **Highlight this** text to locate the place in the Google Doc, use **Comment to leave** as the feedback text, use **Suggested replacement** when a direct rewrite is possible, and use **Why this change is needed** to explain the rationale to the team.

When an exact rewrite depends on final figure order, accession verification, or unresolved team choices, the **Suggested replacement** is given as the exact action to take.

---

## High priority

### 1) Replace the current title with a paper-quality title
**Highlight this:**
`NGS Reanalysis Study On Identification Using Global DEG Discovery of DRG Mouse Dataset`

**Comment to leave:**
Replace this with a cleaner, publication-style title. The current title reads like a working placeholder rather than a final scientific paper title.

**Suggested replacement:**
Use one of these:
- `Transcriptome-Wide Reanalysis of a Mouse DRG RNA-seq Dataset Reveals Global Differential Expression After Sciatic Nerve Injury`
- `Global Differential Expression and Pathway Reanalysis of Mouse DRG RNA-seq After Sciatic Nerve Injury`
- `RNA-seq Reanalysis of Mouse DRG After Sciatic Nerve Injury Identifies Global Differential Expression and Injury-Response Pathways`

**Why this change is needed:**
The title is the first thing a reader sees, and right now it is grammatically awkward and scientifically vague.

---

### 2) Tighten the Introduction opening and remove sentence fragments
**Highlight this:**
`To understand the mechanism that balances the stress response and regenerative demands of neurons once injured.`

**Comment to leave:**
This is a sentence fragment. Fold it into the surrounding paragraph and make the transition from general neuro injury to the specific DRG/AhR study more direct.

**Suggested replacement:**
Replace the fragment with:
`This study was motivated by the need to understand how injured neurons balance cellular stress responses with regenerative demands after nerve injury.`

**Why this change is needed:**
The Introduction should open with clean, complete sentences and a clear progression into the dataset being analyzed.

---

### 3) Remove informal / non-scientific phrasing in the Introduction
**Highlight this:**
`The paper we based our RNA-seq analysis on acts as a detective.`

**Comment to leave:**
Please replace this with formal scientific wording. Avoid metaphorical or conversational phrasing here.

**Suggested replacement:**
Replace with:
`The study that guided our RNA-seq reanalysis was designed to clarify the role of the AhR pathway in the neuronal injury response.`

**Why this change is needed:**
This wording weakens the tone of the paper and makes the Introduction read less like a scientific manuscript.

---

### 4) Remove over-claiming language in the Introduction
**Highlight this:**
`This is one step closer to treating spinal cord injuries and peripheral nerve damage.`

**Comment to leave:**
Please soften this claim. The current analysis is a reanalysis of an RNA-seq dataset and does not justify a treatment-oriented conclusion.

**Suggested replacement:**
Replace with:
`These findings improve the mechanistic understanding of neuronal injury responses and may help guide future studies of regeneration-related pathways.`

**Why this change is needed:**
The paper should distinguish between mechanistic interpretation and clinical impact.

---

### 5) Use one genotype terminology system throughout the paper
**Highlight this:**
Any mixture of `FF`, `WT`, `WT-control`, `wildtype`, `cKO`, and `cre`

**Comment to leave:**
Please choose one consistent genotype naming system and apply it throughout the entire paper. Since the Introduction defines ff/fl as the floxed control genotype, later sections should not drift between WT, WT-control, and FF unless that distinction is explicitly justified.

**Suggested replacement:**
Use this system throughout:
- `ff-control` for the floxed control genotype
- `cKO` for the conditional knockout genotype
- comparison phrasing such as `ipsilateral versus contralateral in ff-control` and `ff-control versus cKO`

If the team insists on WT language, add one sentence in Methods or Introduction explicitly stating that the ff/fl control genotype is being referred to as the wild-type control for simplicity, then use `WT-control` consistently everywhere.

**Why this change is needed:**
Terminology drift is currently one of the biggest scientific consistency problems in the draft.

---

### 6) Verify all accession identifiers and keep them consistent everywhere
**Highlight this:**
`SRP618841 (BioProject PRJNA1322439; GEO GSE243308)` and all other accession strings

**Comment to leave:**
Please verify that SRP, BioProject, and GEO identifiers match the retained project metadata and are consistent everywhere in the paper.

**Suggested replacement:**
Replace every accession block with the single verified accession trio from the retained dataset metadata. Use the same exact wording everywhere, for example:
`SRP618841 (BioProject [verified PRJNA]; GEO GSE243308)`

Do not finalize this sentence until the PRJNA is verified against the retained manifest and repo metadata.

**Why this change is needed:**
Accession inconsistency creates immediate credibility problems in Methods and makes the workflow harder to reproduce.

---

### 7) Fix the merged Methods heading / caption formatting error
**Highlight this:**
`Materials and MethodsFigure 1. Overview ribbon summarizing the four computational stages and their stage in the mouse`

**Comment to leave:**
The section heading and the figure caption are running together. Separate the heading from the figure caption and rewrite the caption so it is complete.

**Suggested replacement:**
Replace with:
`Materials and Methods`

Then place the caption below the figure as:
`Figure 1. Overview ribbon summarizing the four computational stages of the mouse RNA-seq workflow.`

**Why this change is needed:**
This is a visible formatting problem that makes the draft look unfinished.

---

### 8) Eliminate duplicated section framing in Methods
**Highlight this:**
Both occurrences of `Representative Command Examples`

**Comment to leave:**
There are two different table blocks that currently use the same framing. Keep the command/example table under “Representative Command Examples,” but rename the second one to something like “Software, reference resources, and version tracking.”

**Suggested replacement:**
Keep the first heading as:
`Representative Command Examples`

Rename the second heading to:
`Software, Reference Resources, and Version Tracking`

**Why this change is needed:**
Repeated section titles make Methods feel disorganized and can confuse the reader about what each table is doing.

---

### 9) Fix duplicate table numbering
**Highlight this:**
`Table 2. Representative command examples...`
`Table 2. Summary of the 20-sample mouse DRG RNA-seq subset...`

**Comment to leave:**
Please renumber all tables sequentially. Table 2 is currently used twice.

**Suggested replacement:**
If the current table order stays the same, use:
- `Table 1. Representative command examples for the tools used in the mouse RNA-seq workflow.`
- `Table 2. Summary of the 20-sample mouse DRG RNA-seq subset used for reanalysis.`
- `Table 3. Software, reference resources, and releases used in the mouse RNA-seq workflow.`
- later Results/GO tables numbered after those in order of appearance

**Why this change is needed:**
Duplicate table numbering breaks figure/table cross-referencing and makes the draft look incomplete.

---

### 10) Replace all unresolved placeholders before submission
**Highlight this:**
All remaining `Figure X`, `Table X`, and `[Waiting on figure]`

**Comment to leave:**
Please resolve all remaining placeholders and remove the waiting note before submission.

**Suggested replacement:**
Use final sequential numbering once the figure order is frozen. Replace `[Waiting on figure]` with either:
- the final cKO bend-point figure and caption, or
- delete the sentence if the figure is not being kept

**Why this change is needed:**
These are direct signs that the paper is still in draft form.

---

### 11) Fix Methods wording about GO follow-up tools
**Highlight this:**
`enrichment outputs were further summarized using ShinyGO to develop shared-gene charts, tree, and network views`

**Comment to leave:**
Please verify and revise this wording. The workflow appears to use g:Profiler with ShinyGO-style reduction/visualization logic rather than ShinyGO itself as the primary enrichment engine.

**Suggested replacement:**
Replace with:
`The resulting follow-up sets were submitted to g:Profiler for enrichment analysis, and the retained GO outputs were then reduced with chart, tree, and shared-gene network views to summarize redundancy among overlapping terms.`

If the team wants to preserve the ShinyGO connection, use:
`...were then summarized using ShinyGO-style chart, tree, and shared-gene network views...`

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

**Suggested replacement:**
Use the following style replacements:
- `these are fairly accurate` -> `these results were supported by strong statistical significance`
- `The paper's findings state... (Link).` -> `The original study interpreted the knockout condition as shifting neurons away from a stress-preservation state and toward a more growth-permissive state (insert verified citation).`
- `Unexpectedly, the scatter plot appears to contradict the findings of the paper.` -> `The scatter-plot comparison suggested a more complex relationship between stress-response and regeneration-associated terms than would be expected from a simple knockout-versus-control model.`

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

**Suggested replacement:**
Use this structure:
1. paragraph on retained term-gene membership
2. full-width chart figure with its own caption
3. one-sentence downregulated-branch note
4. ff-control/cKO overlap paragraph
5. overlap table
6. full-width network figure with its own caption
7. anchor-gene paragraph
8. anchor-gene table

Number the pieces sequentially once the full Results order is frozen.

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

**Suggested replacement:**
If cutting:
- delete the one-sentence overlap note entirely
- delete the `Alternative Splicing Analysis` heading entirely

If keeping the overlap section, replace the current sentence with:
`The limited overlap between the original paper’s highlighted genes and the bend-point-selected follow-up sets in this reanalysis likely reflects the difference between the paper’s targeted filtering strategy and the tighter global differential-expression narrowing used here.`

**Why this change is needed:**
Unfinished sections interrupt the flow of Results more than any other current issue.

---

### 15) Complete the References section in real APA format
**Highlight this:**
`References`
`Intro sources: ...`

**Comment to leave:**
The References section is still incomplete and contains note-style placeholders. Please convert all references into full APA entries and make sure every in-text citation has a matching reference.

**Suggested replacement:**
Replace note-style placeholders with full APA references. For example, each source should follow this pattern:
`Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. Journal Title, Volume(Issue), pages. https://doi.org/...`

For database citations, use one verified format consistently for SRA, BioProject, GEO, Ensembl, and tool citations.

**Why this change is needed:**
Incomplete references alone can make the draft non-submittable.

---

### 16) Move the final paper out of Google Docs before submission
**Highlight this:**
The requirement block at the top that says `Do not use Google Docs which creates formatting issues.`

**Comment to leave:**
Before final submission, export and finalize this paper in Word / LibreOffice / OpenOffice as required.

**Suggested replacement:**
Action rather than text replacement:
- export the Google Doc to `.docx`
- finalize spacing, margins, headings, page breaks, tables, and figure placement in Word / LibreOffice
- submit the `.docx` or required final format, not the Google Doc

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

**Suggested replacement:**
Use this hierarchy consistently:
- Heading 1: `Introduction`, `Materials and Methods`, `Results`, `Discussion`, `References`
- Heading 2: major subsections such as `Data Cleaning: Quality Control and Read Trimming`
- Heading 3 only if needed for smaller subsections

**Why this change is needed:**
Consistent heading levels improve readability and make the manuscript structure clearer.

---

### 18) Standardize bend-point wording and notation
**Highlight this:**
`The bend-point in the ipsilateral vs contralateral in the WT branch occurred at a p-value of 1.37e-17`
`8.40 × 10-17`

**Comment to leave:**
Please standardize this to “adjusted p-value threshold” and use consistent scientific notation formatting throughout.

**Suggested replacement:**
Replace with:
`The bend point in the ipsilateral-versus-contralateral ff-control branch occurred at an adjusted p-value threshold of 1.37 × 10^-17, retaining approximately 709 genes from the larger significant set.`

Use the same formatting style everywhere, for example `8.40 × 10^-17`.

**Why this change is needed:**
The paper currently shifts between p-value wording styles and notation styles.

---

### 19) Keep Results and Discussion from repeating the same claim too many times
**Highlight this:**
Any repeated statements that `side-specific injury contrasts carried the strongest signal` or that the `WT/FF branch remained the clearest pathway-level result`

**Comment to leave:**
This point is important, but it appears multiple times in Results and again in Discussion. Keep the full explanation in one place and shorten the repeated versions.

**Suggested replacement:**
In Results, keep the full version.
In Discussion, shorten to:
`Consistent with the PCA-first and bend-point-guided analysis, the side-specific branches remained the strongest basis for interpretation.`

**Why this change is needed:**
Too much repetition makes the paper feel longer without making it stronger.

---

### 20) Keep GO redundancy-reduction language in Results, not repeated in full in Discussion
**Highlight this:**
`Once shared-gene structure was examined through the chart, tree, and network views...`

**Comment to leave:**
The detailed redundancy-reduction explanation belongs primarily in Results. Discussion should keep only the take-home interpretation.

**Suggested replacement:**
In Results, keep the detailed explanation.
In Discussion, reduce to:
`The later GO follow-up showed that the apparent abundance of enriched terms was driven largely by overlapping gene membership rather than by many unrelated pathways.`

**Why this change is needed:**
This helps separate observation from interpretation.

---

### 21) Clarify the transition from general neuro injury to the actual dataset
**Highlight this:**
The first three Introduction paragraphs

**Comment to leave:**
Please tighten the transition from broad neurological injury background to the specific mouse DRG sciatic nerve injury dataset.

**Suggested replacement:**
Add a transition sentence such as:
`To investigate this question in a defined experimental system, we reanalyzed a published mouse DRG RNA-seq dataset generated one day after sciatic nerve injury.`

**Why this change is needed:**
Right now the paper starts broadly, then shifts abruptly into the Ahr paper and the experimental design.

---

### 22) Clean up the explanation of FF / floxed controls
**Highlight this:**
`This tag by itself has no effect-- de facto acting as a wildtype--`

**Comment to leave:**
Please rewrite this more formally and consistently with the genotype terminology used elsewhere.

**Suggested replacement:**
Replace with:
`The floxed control genotype retains the loxP sites without deleting the target gene and therefore serves as the control condition in the present analysis.`

**Why this change is needed:**
The explanation is useful, but the wording is still conversational.

---

### 23) Rename or rewrite the scatter-plot comparison paragraph if kept
**Highlight this:**
`Unexpectedly, the scatter plot appears to contradict the findings of the paper.`

**Comment to leave:**
If this analysis stays, please frame it more carefully. State what the plot shows first, then explain the possible interpretation, rather than opening with “contradict.”

**Suggested replacement:**
Replace with:
`The scatter-plot comparison suggested that several stress-response and apoptotic-process terms remained comparatively strong in the cKO branch, indicating a more complex relationship between genotype and pathway-level interpretation than expected from the original study alone.`

**Why this change is needed:**
That wording sounds too strong for a comparison result that still needs careful interpretation.

---

### 24) Keep table titles above tables consistently
**Highlight this:**
Any table whose title appears after the table or is visually separated from it

**Comment to leave:**
Please place all table titles above the corresponding tables and keep the formatting consistent across the paper.

**Suggested replacement:**
Action rather than wording change:
- move every `Table N.` title immediately above its table
- keep one blank line between the title and the table body
- keep caption style consistent for all tables

**Why this change is needed:**
Consistent table placement makes the Results and Methods easier to scan.

---

### 25) Make figure captions describe the actual image shown
**Highlight this:**
Any caption that combines multiple panels or says `A/B/C` when the image placement does not clearly match that structure

**Comment to leave:**
Please check each caption against the actual displayed figure layout. Some captions still describe multi-panel structures more clearly than the document layout does.

**Suggested replacement:**
If a figure is now full-width and single-panel, rewrite the caption as a single-panel caption. For example:
`Figure X. Shared-gene network view for the ff-control upregulated GO Biological Process follow-up.`

Do not keep `A/B/C` references unless the figure is visibly arranged as A/B/C panels.

**Why this change is needed:**
Mismatched captions confuse the reader and weaken the credibility of the figure.

---

### 26) Add final numbering and consistent cross-references for GO Follow-up tables
**Highlight this:**
`Table X. Overlap summary for the two narrowed side-specific branches`
`Table X. Anchor-gene companion summary for the FF GO follow-up`

**Comment to leave:**
These are useful additions. Please give them final table numbers and refer to them explicitly in the surrounding Results text.

**Suggested replacement:**
Once numbering is final, revise the surrounding text to say things like:
`As summarized in Table 4, the two narrowed side-specific branches shared 620 genes...`
`The recurring anchor-gene patterns are summarized in Table 5.`

**Why this change is needed:**
The new section will read more like an integrated manuscript section and less like a pasted add-on.

---

### 27) Verify all citations attached to Methods statements
**Highlight this:**
Any sentence that pairs workflow implementation details with citations, especially the opening Methods paragraphs and tool descriptions

**Comment to leave:**
Please verify that each citation supports the exact claim it is attached to. Tool citations, dataset citations, and workflow rationale citations should stay distinct.

**Suggested replacement:**
Action rather than wording change:
- dataset claims -> cite Halawani et al. and the accession/database sources
- tool descriptions -> cite FastQC, MultiQC, fastp, STAR, DESeq2, g:Profiler, etc.
- workflow rationale statements -> keep citations only if they truly support the claim

**Why this change is needed:**
This helps avoid citation drift where references are correct in general but not precise for the sentence.

---

## Low priority

### 28) Standardize species, gene, and protein styling
**Highlight this:**
Occurrences of `Mus musculus`, `Ahr`, `ATF3`, `Jun`, `Sox11`, etc.

**Comment to leave:**
Please make gene/protein/species formatting consistent throughout the paper.

**Suggested replacement:**
Adopt one consistent style, for example:
- *Mus musculus* in italics for species
- *Ahr*, *Jun*, *Sox11* in italics for mouse gene symbols if using gene-style formatting
- ATF3 protein naming only where protein is actually meant

**Why this change is needed:**
This is a polish issue, but it helps the manuscript look more professional.

---

### 29) Standardize hyphenation and comparison wording
**Highlight this:**
Mixed uses of `ipsilateral vs contralateral`, `ipsilateral-versus-contralateral`, `WT vs cKO`, `WT versus cKO`

**Comment to leave:**
Please choose one style for comparison wording and use it consistently.

**Suggested replacement:**
Use prose style in text:
- `ipsilateral versus contralateral`
- `ff-control versus cKO`

Use compact style only in code names or saved contrast labels:
- `ipsi_vs_contra_in_ff`
- `geno_in_contra`

**Why this change is needed:**
Consistency improves readability and reduces copy-editing noise.

---

### 30) Replace casual wording in Results where possible
**Highlight this:**
Phrases like `these are fairly accurate`, `de facto acting as a wildtype`, `Basically, our bendpoint approach...`

**Comment to leave:**
Please replace informal phrasing with formal scientific wording.

**Suggested replacement:**
Use these replacements:
- `these are fairly accurate` -> `these results were supported by strong statistical significance`
- `de facto acting as a wildtype` -> `serving as the control genotype`
- `Basically, our bendpoint approach...` -> `The bend-point approach used in this reanalysis was more restrictive than the filtering strategy used in the original paper...`

**Why this change is needed:**
The paper already has enough strong content that it does not need casual language.

---

### 31) Keep workflow table colors aligned with the Methods stage palette
**Highlight this:**
Stage-based tables in Methods and the two new GO follow-up tables

**Comment to leave:**
Please keep the workflow tables color-coded consistently: Collection = blue, Cleaning = orange, Preparation = green, Analysis = lavender. The GO follow-up tables should use the Analysis palette.

**Suggested replacement:**
Use these exact fills:
- Collection: `#EAF3FF`
- Cleaning: `#FFF2E6`
- Preparation: `#EAF7EA`
- Analysis: `#F1EAFF`
- Neutral header gray: `#F5F5F5`

**Why this change is needed:**
The visual design is stronger when the stage logic is consistent across the whole paper.

---

### 32) Add a final author-color note if the instructor still expects it
**Highlight this:**
The requirement text at the top that says to include one comment identifying each person’s revision color

**Comment to leave:**
Before submission, make sure the required author-contribution color note is still present in the final exported file if the assignment still expects it.

**Suggested replacement:**
Add a short opening comment such as:
`Piter Garcia — light red contributions`

Repeat the same pattern for each group member using the agreed color.

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
