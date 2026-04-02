# Brain Map — First Draft Paper (`mouse_new`)

This is a **brain/mind map for writing**, not a normal outline.
Each node is meant to become a paragraph or paragraph group in the paper.
The point is to show:

- what happened
- why it mattered
- what it connects to next

---

## Central paper idea

**A usable mouse RNA-seq paper did not emerge from the first analysis path.**
**The meaningful DE story came from the `mouse_new` / `SRP618841` branch, but only after dealing with real QC, alignment, and modeling complexity.**

This connects to:

- dataset selection
- first pipeline path
- failure to get a clean first story
- contingency dataset branch
- structure-aware DE analysis
- main DRG side-specific results

---

## Map view — one-line chain

`Need a BIOL550 journal-style paper`
→ `choose mouse project`
→ `run first pipeline on original mouse branch`
→ `do QC, trimming, alignment, DE`
→ `realize the first dataset/path does not yield a clean, strong paper story`
→ `bring in contingency mouse dataset`
→ `repeat QC + cleanup + alignment + DE on SRP618841`
→ `obtain one usable DRG family with strong side-specific signal`
→ `frame paper around structure-aware DE, with QC/alignment as supporting evidence`

---

## Node 1 — Course goal / paper need

### Core idea

We needed a journal-style BIOL550 group paper, not just a workflow log.

### Why it matters

This sets the writing target:

- not a command diary
- not a weekly report
- not just “the pipeline ran”
- but a paper with a clear analytical story

### Connects to

- why dataset selection mattered
- why weak results from the first path were a real problem

### Writing use

This can become the opening framing paragraph:

- we needed a paper-quality biological/analytical story from a real RNA-seq dataset

---

## Node 2 — Initial mouse dataset path

### Core idea

The project first developed around the original `mouse` branch and its initial pipeline.

### What happened

- dataset was selected
- metadata and run structure were organized
- QC, trimming, alignment, and DE workflows were built
- this branch produced a full analysis package

### Why it matters

This is the first serious attempt to build the paper story.

### Connects to

- first pipeline execution
- first DE results
- later realization that this was not the cleanest paper path

### Writing use

This can become the first background/process paragraph after the introduction:

- the original mouse workflow established the initial analytical path and exposed the main structural problems in the project

---

## Node 3 — First pipeline execution

### Core idea

The first pipeline was not wasted work; it revealed both what was possible and what was problematic.

### What happened

- raw QC was run
- cleanup/trimming decisions were made
- STAR alignment was completed
- count handoff was prepared
- DESeq2 was run across the original mouse branch families

### Why it matters

This path gave us the first serious results package, but it also exposed why the story was hard to write cleanly.

### Connects to

- QC concerns
- structural heterogeneity
- weak or uneven result story

### Writing use

This can become a methods/results transition paragraph:

- the initial pipeline showed that the dataset was processable, but processability alone was not enough to guarantee a good paper story

---

## Node 4 — The first path did not yield a clean main paper story

### Core idea

The first dataset/path produced outputs, but not the strongest or cleanest paper foundation.

### What happened

- the original mouse branch produced multiple DE families
- the results were not equally strong
- some contrasts were much weaker than others
- the full dataset/story remained harder to center cleanly for a journal-style paper

### Why it matters

This is one of the most important events in the paper history:

- the problem was not “the pipeline failed”
- the problem was “the first analysis path did not yield the clearest meaningful paper”

### Key interpretation

The first branch gave:

- useful technical progress
- real evidence about the dataset
- but a paper story that was harder to defend cleanly and coherently

### Connects to

- the decision to seek a cleaner contingency dataset
- the decision to avoid forcing a weak narrative

### Writing use

This can become a strong paragraph in either:

- Introduction end
- Results opening
- or Discussion / rationale for the final analytical path

---

## Node 5 — Why the first path was difficult

### Core idea

The difficulty was not only biological. It was also structural and methodological.

### What made it hard

- mixed dataset structure
- uneven strength across contrasts
- platform/sample-context complexity
- harder-to-center main narrative
- risk of overclaiming if everything were treated equally

### Why it matters

This is where the paper starts to become methodological:

- the project was not just about obtaining DE results
- it was about deciding which results were defensible and worth centering

### Connects to

- contingency branch
- structure-aware framing

### Writing use

This can become the paragraph that explains why a second dataset branch was not random or redundant, but analytically necessary

---

## Node 6 — Contingency dataset decision

### Core idea

Because the first path did not yield the cleanest paper story, the project opened a contingency branch with `SRP618841`.

### What happened

- `SRP618841` was brought in as a parallel candidate dataset
- it was organized under `mouse_new`
- the goal was not to discard prior work, but to secure a more defensible main path if needed

### Why it matters

This was the strategic turning point of the project.

### Connects to

- new QC workflow
- new alignment path
- new DE story

### Writing use

This can become a paragraph about analytical adaptation:

- when the first route did not produce the strongest paper foundation, the project shifted to a cleaner contingency dataset rather than forcing a weak story

---

## Node 7 — `mouse_new` raw QC and cleanup

### Core idea

The new dataset still needed real QC work; it was not magically perfect.

### What happened

- raw `FastQC` and `MultiQC` were run
- `fastp` was used as the canonical cleanup workflow
- raw vs trimmed comparisons were reviewed
- adapter-related signal improved after trimming
- some remaining sequence-content / duplication / overrepresentation concerns persisted

### Why it matters

This gives the paper a realistic data-quality story:

- the final dataset was usable
- but only after explicit QC review and cleanup
- and even then it still had complexities

### Connects to

- alignment as support
- paper framing as “usable but imperfect real data”

### Writing use

This can become part of the Methods + supporting Results framing:

- the dataset improved through cleanup but remained a real biological dataset with residual complexity

---

## Node 8 — `mouse_new` alignment

### Core idea

Alignment validated that the `SRP618841` branch was good enough to support DE.

### What happened

- STAR alignment completed for the 20-sample dataset
- sorted BAMs and count handoff were generated
- alignment metrics were checked

### Why it matters

Alignment is not the topic of the paper, but it is the evidence that:

- the count layer is trustworthy
- proceeding into DE is justified

### Connects to

- DESeq2
- supporting-evidence framing

### Writing use

This becomes a short methods/support paragraph:

- alignment established that the new dataset was analyzable and suitable for downstream DE

---

## Node 9 — `mouse_new` still came with complexity

### Core idea

The second dataset yielded the meaningful paper story, but not by being simple.

### What was complex

- QC issues did not disappear completely
- interpretation still required careful contrast selection
- not all contrasts were equally informative
- genotype effects were not uniformly strong
- the strongest result was side-specific, not everything at once

### Why it matters

This prevents the paper from sounding naive:

- the successful path still required judgment
- the meaningful story came from prioritizing the right contrasts

### Connects to

- DRG family definition
- contrast prioritization

### Writing use

This can become a strong transition paragraph:

- the contingency dataset improved the project’s analytical footing, but the final story still depended on careful interpretation rather than automatic output

---

## Node 10 — The valid DE family

### Core idea

The `mouse_new` dataset resolved into one clear main family:

- `family_drg_novaseqx`

### Meaning

- `drg` = dorsal root ganglion tissue family
- `novaseqx` = `NovaSeq X` platform family

### Why it matters

This gives the paper a cleaner center than the earlier branch:

- one main family
- five interpretable contrasts
- less fragmentation in the story

### Connects to

- PCA
- contrast ranking
- main paper narrative

### Writing use

This can become the key design paragraph:

- the paper’s DE analysis is organized around one DRG / `NovaSeq X` family with interpretable within-family contrasts

---

## Node 11 — The main results that actually matter

### Core idea

The strongest signal in `mouse_new` is side-specific DRG expression.

### Main contrasts

- `ipsi_vs_contra_in_ff` = `7023` significant genes
- `ipsi_vs_contra_in_cre` = `7541` significant genes

### Secondary contrasts

- `geno_in_contra` = `891`
- `geno_in_ipsi` = `2`
- `interaction` = `14`

### Why it matters

This is where the paper gets its main results section:

- side is the dominant signal
- genotype is secondary and context-dependent
- interaction is minimal

### Connects to

- PCA interpretation
- heatmaps / volcano plots
- final paper thesis

### Writing use

This can become the first full results subsection

---

## Node 12 — PCA and visual structure

### Core idea

The PCA supports the interpretation that side is the strongest global source of variation in the DRG family.

### Why it matters

It visually supports the contrast summary:

- side separates the samples most strongly
- genotype is present but not dominant

### Connects to

- main DE contrasts
- heatmaps
- discussion section

### Writing use

This becomes a paragraph that links sample-level structure to gene-level results

---

## Node 13 — Heatmaps / volcano plots / top genes

### Core idea

The paper’s DE evidence should move from:

- sample-level structure
→ strongest contrast plots
→ named gene summaries

### Why it matters

This gives the paper a readable journal flow:

- PCA = global structure
- volcano/heatmap = contrast-level signal
- top genes = specific interpretable examples

### Connects to

- figure set
- table set

### Writing use

This becomes the basis for deciding the order of figures in the Results section

---

## Node 14 — What the paper is really about

### Core idea

The paper is not just “we ran DE on `mouse_new`.”

### The real paper point

The project had to move through:

- an initial path that did not yield a strong clean paper story
- a contingency dataset that became the real analytical path
- real QC/alignment work
- careful DE interpretation

### Final paper claim

A meaningful mouse RNA-seq DE story emerged only after:

- rejecting a weaker first narrative
- moving to a cleaner contingency dataset
- and interpreting the resulting DRG-family contrasts with methodological care

### Connects to

- discussion
- conclusion

### Writing use

This can become the closing sentence of the introduction or the opening sentence of the discussion

---

## Node 15 — Alignment / QC as supporting evidence only

### Core idea

Alignment and QC matter, but they are not the paper’s central topic.

### What they do in the paper

- show the dataset was usable
- show cleanup improved it
- show alignment supported a trustworthy count handoff
- justify moving into DE

### What they should not do

- dominate the Results section
- become the main contribution
- turn the manuscript into a pipeline report

### Writing use

This becomes a restraint/reminder for drafting:

- include enough to justify the DE results, but not enough to displace them

---

## Node 16 — Paragraph-building path for drafting

Use the paper draft in this order:

1. **Need a BIOL550 paper-quality story**
2. **Original mouse path established the first pipeline**
3. **That first path did not yield the strongest meaningful paper**
4. **This led to the `mouse_new` / `SRP618841` contingency branch**
5. **`mouse_new` still required QC, cleanup, and alignment validation**
6. **The resulting usable DE family was `family_drg_novaseqx`**
7. **The strongest signal was ipsilateral vs contralateral DRG expression**
8. **Genotype and interaction were secondary**
9. **Therefore the paper should be DE-centered, structure-aware, and supported by alignment/QC rather than driven by them**

---

## Bottom line

The real paper story is:

**the first analytical path produced work but not the strongest meaningful paper narrative; the final usable paper direction came from `mouse_new`, where a cleaner DRG-family DE analysis yielded strong side-specific signal, supported by QC and alignment but shaped by real methodological complexity.**
