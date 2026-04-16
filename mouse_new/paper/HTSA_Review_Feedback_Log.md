# HTSA review feedback log

Date: 2026-04-15

Scope:
- Keep exact highlight spans, comment text, and a short revision cue together
- Prioritize feedback that is directly supported by validated `mouse_new` outputs, weekly reports, and April transcript guidance
- Keep comments simple, specific, and non-picky
- Mark already-addressed items when transcript guidance confirms we have already handled them elsewhere

Transcript anchors used for this pass:
- `Semester5/BIOL550/group_project/mouse_new/reports/2026-04-14 Weekly Meeting_ Draft Submission, Methods Streamlining, Labeling Conventions, and Citations-summary.md`
- `Semester5/BIOL550/transcripts/2026-04-01 Navigating Data Overload in Gene Expression Analysis_ Pivoting from Arbitrary Cutoffs to a P-Value Distribution Method-summary.md`
- `Semester5/BIOL550/transcripts/2026-03-31 Team Meeting_ RNA-seq NovaSeq 6000 Analysis, Presentation Prep, and Course Participation Decision-summary.md`

## High-importance items

### 1) PCA / heatmap overstates genotype story

- Section: `Results` → `Differential Expression Analysis`
- Highlight these PCA sentences together:
  - `PC1 (46.2%) represents the primary variance driven by the response to nerve injury...`
  - `PC2 (20.6%) represents the secondary variance driven by the Ahr genotype...`
- Highlight these heatmap sentences together:
  - `The results demonstrate clear and distinct unsupervised clustering...`
  - `samples were further partitioned by genotype...`
- Comment to leave:
  - `This is a little too strong for the genotype story. Our weekly report supports side as the dominant pattern and genotype as a weaker secondary pattern, with some near-overlapping ff/cre pairs. I’d soften this so we don’t overstate genotype separation.`
- Suggested draft wording:
  - `PC1 (46.2%) primarily reflects variance associated with side (ipsilateral vs contralateral), which is the dominant pattern in the dataset. PC2 (20.6%) captures secondary variance that partly correlates with Ahr genotype; genotype separation is present but weaker and shows some overlapping FF/CRE pairs.`
  - `Unsupervised clustering groups samples mainly by side (ipsilateral vs contralateral). Genotype shows partial partitioning in some pairs but does not produce a clear, uniform separation.`
- Transcript tie-in:
  - `2026-04-01` summary keeps PCA as the first sanity check and warns against over-reading condition effects without baseline structure.

### 2) Bend-point paragraph must name the exact contrast

- Section: `Results` → `Differential Expression Analysis` → volcano / bend-point paragraph
- Highlight this sentence:
  - `The bend point occurred at a p-value of 1.37e-17... At this p-value, about 709 genes appeared.`
- Comment to leave:
  - `Please name the exact contrast here. The 709 genes are from ipsi_vs_contra_in_ff. Without the contrast name, the reader can confuse this with the alternate side-specific branch (ipsi_vs_contra_in_cre, 870 genes).`
- Suggested draft wording:
  - `For the ipsi_vs_contra_in_ff contrast the bend point occurred at a p-value of 1.37e-17, yielding approximately 709 genes.`
- Transcript tie-in:
  - `2026-04-01` summary emphasizes bend-point narrowing per contrast, not as one pooled global gene set.

### 3) GO Results should stay centered on the validated main branch

- Section: `Results` → `Gene Ontology Analysis`
- Highlight the opening GO paragraph.
- If needed, also highlight the starts of the BP, CC, and MF paragraphs.
- Comment to leave:
  - `I think this section should more clearly center the FF side-specific branch as the main validated GO story. Our strongest supported result is the FF branch, especially overlapping BP themes like signaling/regulation, migration or morphogenesis, and injury-response/development. Right now BP, CC, and MF read a bit too equally weighted.`
- Suggested draft wording:
  - `We focus the GO analysis on the FF side-specific branch (ipsi_vs_contra_in_ff), which shows the strongest and most consistent enrichment—particularly in BP terms related to signaling/regulation, migration/morphogenesis, and injury-response/development.`
- Transcript tie-in:
  - `2026-03-31` and `2026-04-01` both support story selection rather than describing every possible branch equally.

### 4) Some Results sentences move from observation to interpretation too fast

- Section: mostly `Gene Ontology Analysis`, secondarily `Differential Expression Analysis`
- Highlight these BP sentences:
  - `With this in mind, it makes sense for all the pathways to be connected...`
- Highlight the unfinished bracketed sentence in CC.
- Highlight the unfinished bracketed sentence in MF.
- Comment to leave:
  - `This moves a little too quickly from what the figure shows to interpretation. I’d first describe the observed pattern, then add a short interpretation. Also, the bracketed sentences need to be completed or cut.`
- Suggested draft wording:
  - `Observed: the top BP terms show overlapping gene membership across several enriched terms. Interpretation: this pattern suggests a connected program of signaling and injury response; additional validation is needed before stronger mechanistic claims are made.`
- Transcript tie-in:
  - `2026-04-01` emphasizes method-driven interpretation order and avoiding narrative bias from arbitrary filtering.

### 5) QC claim overstates what trimming fixed

- Section: `Results` → `Quality Control and Trimming of RNASeq Data`
- Highlight this sentence:
  - `the dataset was trimmed to clear the adapter issues along with overrepresented sequences and sequence duplication.`
- Comment to leave:
  - `This overstates what trimming fixed. Our QC outputs strongly support that adapter-content failures were resolved, but not that overrepresented-sequence and duplication issues were fully cleared. I’d make this more precise.`
- Suggested draft wording:
  - `Trimming resolved adapter-content failures; overrepresented sequences and duplication levels were reduced but not fully eliminated, so we report the adapter fix specifically.`

### 6) Introduction / background needs biologically accurate injury context

- Section: `Introduction`
- Highlight:
  - `DRG after spinal cord injury`
  - any nearby sentence that treats the dataset as spinal cord injury rather than sciatic nerve injury / peripheral nerve injury
- Comment to leave:
  - `This needs to stay aligned with the actual dataset and paper context. The analyzed RNA-seq subset is DRG after sciatic nerve crush injury (peripheral nerve injury), not a spinal cord injury dataset.`
- Suggested draft wording:
  - `DRG after sciatic nerve injury`
  - `The study used dorsal root ganglia after sciatic nerve crush injury to examine the transcriptional response of regenerating peripheral neurons.`
- Note:
  - This is an accuracy issue, not just wording.

### 7) Introduction currently overstates our gene set if it says 709 as a global result

- Section: `Introduction` → `How we wanted to use the paper`
- Highlight:
  - `we did a global differential expression analysis on the genes, and identified 709 statistical significant genes.`
- Comment to leave:
  - `This should be made more precise. The 709 genes are not the total transcriptome-wide DE result; they are the bend-point-selected follow-up set for the ipsi_vs_contra_in_ff contrast.`
- Suggested draft wording:
  - `Rather than following only the paper’s candidate-gene emphasis, we performed a transcriptome-wide differential expression analysis and then used a bend-point rule to narrow the ipsi_vs_contra_in_ff contrast to a 709-gene follow-up set for pathway interpretation.`

## Medium-importance items

### 8) Methods should not be overloaded with figures

- Section: `Materials and Methods`
- Highlight any place where multiple Methods figures or figure-heavy staging are being proposed / retained.
- Comment to leave:
  - `Per the 4/14 meeting, Methods should keep only the most useful visuals. The pipeline figure is the strongest keeper; any figure that just repeats paragraph content should become optional or be removed.`
- Suggested draft wording:
  - No single sentence replacement; this is a figure-retention decision.
- Status:
  - `Partly addressed already in our Methods streamlining work; keep this item as a check against the shared doc version.`

### 9) Methods tables that duplicate prose should be converted or reduced

- Section: `Materials and Methods`
- Highlight long stage tables that simply restate paragraph content.
- Comment to leave:
  - `The 4/14 transcript suggested reducing table-like Methods material when the same point is already explained well in prose. I’d keep only the tables that add real clarity or satisfy a course requirement.`
- Suggested draft wording:
  - No sentence replacement; convert duplicated rows into concise prose where possible.

### 10) Use reader-facing `WT` / `cKO` wording where appropriate

- Section: reader-facing figure captions, Results text, Discussion text, and introduction glosses
- Highlight repeated `FF` / `CRE` usage where the biological meaning is not explained nearby.
- Comment to leave:
  - `The 4/14 meeting suggested using more reader-friendly labels like WT and cKO where appropriate. We can still preserve FF/CRE internally, but the paper should help the reader immediately know what those mean.`
- Suggested draft wording:
  - `WT (ff)` on first use
  - `Ahr cKO (cre)` on first use
- Status:
  - `Related to feedback item 6 in the intro; use cross-reference instead of duplicating the same comment everywhere.`

### 11) Tool citations should include explicit versions

- Section: `Materials and Methods`
- Highlight tool mentions that currently cite the tool but omit version numbers where we know them.
- Comment to leave:
  - `The 4/14 meeting explicitly called out tool versions. Please make sure the named tools include versions where we know them, especially FastQC / MultiQC / fastp / STAR / DESeq2 / g:Profiler.`
- Suggested draft wording:
  - `fastp v0.23.2`
  - similar version formatting for other tools where confirmed
- Status:
  - `Citations are already being added; this item is about version completeness, not whether the tool is cited at all.`

### 12) Alignment paragraph should use exact checkpoint numbers

- Section: `Results` → alignment paragraph under the alignment figure
- Highlight these sentences:
  - `Each read had a uniquely mapped read percentage above 90%, which is a high number for alignment...`
  - `Most of the reads were placed between 93.1% and just a little above 93.4%.`
- Comment to leave:
  - `I’d use the exact alignment checkpoint numbers here instead of broad wording, since we have a validated summary from the report.`
- Suggested draft wording:
  - `Median unique mapping was 93.24% (IQR 93.10–93.42%), with low median noFeature (~3.82%) and ambiguous (~1.77%) assignment burdens, supporting progression to downstream differential expression analysis.`

### 13) PCA should say variance, not “total biological signal”

- Section: `Results` → PCA paragraph
- Highlight this sentence:
  - `The PCA consolidated the ~21,000 genes into two primary components that represent 66.8% of the total biological signal.`
- Comment to leave:
  - `I’d change “total biological signal” to “variance captured by the first two principal components” so the wording stays statistically precise.`
- Suggested draft wording:
  - `The PCA summarized the dataset into two primary components that captured 66.8% of the variance.`

### 14) Figure captions should name the exact contrast when specific gene counts are used

- Section: volcano figure caption and GO figure caption
- Highlight the captions where `709` genes are described without the contrast name.
- Comment to leave:
  - `It would help to name the exact contrast in the caption wherever the 709-gene set is mentioned, so the reader immediately knows this is the ipsi_vs_contra_in_ff follow-up.`
- Suggested draft wording:
  - `Comparison of volcano plots for the ipsi_vs_contra_in_ff contrast before and after bend-point-based narrowing.`
  - `Gene Ontology analysis of the 709-gene bend-point-selected set from the ipsi_vs_contra_in_ff contrast.`

### 15) GO/tool wording should stay tied to the actual retained figures

- Section: Results / Methods / figure captions anywhere GO tools are described
- Highlight places where a tool might be named even though the retained figure set may have changed.
- Comment to leave:
  - `The 4/14 transcript made a good point here: we should only name tools that are actually supporting the retained figures/text. If a figure was cut, the tool language may need to be reduced or moved.`
- Suggested draft wording:
  - No single sentence replacement; this is a consistency pass against the retained figure set.

### 16) Comparison plots should use WT / cKO and show GO IDs

- Section: GO follow-up comparison plots in the notebook / exported figure set
- Update the first plot:
  - relabel the bend-point overlap figure as `WT` vs `cKO`
  - keep the gene overlap summary aligned with those labels
- Update the second plot:
  - annotate each shared GO point with the GO ID plus the term label, the same way the network graph does
  - change the axes / titles to `WT` and `cKO`
- Comment to leave:
  - `Nikhi wants the comparison plots to use more specific GO terminology than a generic label like "transport." Please show the GO IDs directly on the scatter points, and relabel the branches as WT and cKO if that fits the figure.`
- Suggested draft wording:
  - Plot 1 title → `Bend-point-selected gene overlap: WT vs cKO`
  - Plot 2 axis labels → `WT upregulated GO terms: -log10(FDR)` and `cKO upregulated GO terms: -log10(FDR)`
- Status:
  - `Already partly addressed in the updated FF network labeling work; keep this as a follow-up for the comparison plots.`

## Low-importance items

### 17) Keep one clean Results storyline

- Section: overall `Results` flow
- Comment to leave:
  - `The section will read more cleanly if the order stays consistent: QC → alignment → PCA-first structure → bend-point narrowing → GO follow-up.`
- Suggested draft wording:
  - No sentence change needed; this is an organizational pass.
- Transcript tie-in:
  - `2026-03-31` summary explicitly supports that narrative order.

### 18) Replace placeholder interpretation lines with concise validated statements

- Section: `Gene Ontology Analysis`
- Highlight these placeholders:
  - `[This makes sense because…]`
  - `[However, the presence of these specific terms…]`
  - `[These terms are significant because…]`
- Comment to leave:
  - `These placeholders should either be completed with short, evidence-based interpretation or cut if they are not needed. The safest route is to tie them back to the validated recurring FF themes rather than speculate broadly.`
- Suggested draft wording:
  - `Many of these labels appear connected because they share overlapping supporting genes within a broader injury-response and signaling context.`

### 19) Minor wording polish in the alignment paragraph

- Section: alignment paragraph
- Highlight this phrase:
  - `which seems to be more of an outlier`
- Comment to leave:
  - `This reads a little informal for Results. I’d either remove it or replace it with a more neutral phrase.`
- Suggested draft wording:
  - `the lower end of the distribution`

### 20) Keep support notes and final paper prose clearly separated

- Section: draft comments / planning notes / copied summaries
- Comment to leave:
  - `Paper-support notes are useful, but they should stay clearly labeled as notes or support material so they are not mistaken for final draft prose.`
- Suggested draft wording:
  - No sentence change needed; this is a documentation hygiene reminder from the April workflow discussion.
- Transcript tie-in:
  - Derived from the paper/process implications of the 2026-04-07 meeting.
