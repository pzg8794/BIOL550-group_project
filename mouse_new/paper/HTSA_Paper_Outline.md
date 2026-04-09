Nikhi Boggavarapu
Sam Kopelev
Piter Garcia

**HTSA Group Paper Outline**
**BIOL550 Group Project (Draft 1)**

* Nikhi Boggavarapu
* Sam Kopelev
* Piter Garcia

**Introduction**

* Brief intro about high-throughput sequencing
  * RNA-seq as a transcriptome-wide method for detecting gene expression changes
  * Types of NGS
    * Organized by read length
    * Applications
  * Benefits of NGS
    * High throughput
    * Fast
  * What our goal was in utilizing NGS
    * Unbiased, transcriptome-wide detection of gene expression changes
* Introduce paper/dataset
  * Experimental design
  * DRG after spinal cord injury
  * Goals of the paper
    * Why did they analyze DRG with cKO
    * Ipsilateral vs contralateral
    * FF / cre context
* How we wanted to use the paper
  * Explore and confirm suggested pathways
    * FF / cre
  * Examine gene expression changes beyond the genes emphasized in the original paper
* Claim
  * *Differential expression (DE):* transcriptome-wide RNA-seq helps identify genes involved beyond the ones the paper discussed
  * *Key contrasts:* expression differences were quantified across the main experimental comparisons, especially ipsilateral vs contralateral DRG, and genotype where relevant
  * *GO / pathway enrichment:* DE gene sets were interpreted in terms of broader biological processes and pathways linked to injury response and the cKO context

**Materials and Methods**

* Dataset and study design
  * Public dataset accession
  * Tissue and injury context
  * Sample groups and contrasts
  * Why was this subset retained
* Pipeline Steps
  * Data Collection and Preprocessing
    * Download SRR files (`.gz`)
    * FASTQ organization
    * Sample manifest / metadata table
    * Tools used
  * Data Quality Control and Trimming
    * Raw FastQC / MultiQC
    * FASTP trimming
    * Post-trim FastQC / MultiQC
    * Key QC checkpoint metrics
  * Data Preparation (Alignment and count generation)
    * Reference genome and annotation
      * (mm39)
    * STAR index and alignment
      * Building the STAR genome
      * Paired-end alignment
    * GeneCounts output
    * BAM / log / count outputs
    * Family count matrix assembly
  * Data Analysis and Interpretation
    * MultiQC
    * Differential Expression Analysis
      * DESeq2 setup
      * DESeq2
        * Volcano plot
        * Heatmap of top DEGs (Regeneration-Enhancing)
        * MA plot
        * Target validation (gene expression boxplots)
      * Filtering rule
      * Modeled contrasts
      * Thresholds / significance criteria
    * Follow-up selection for functional interpretation
      * Bend-point rule
      * GO analysis
      * GSEA analysis
      * Panther analysis
      * Extra analysis, if finalized

**Results**

* Dataset quality supported downstream analysis
  * Number of samples and read structure
  * Pre-trim
    * GC content
    * Adapter sequences
  * Alignment stats
    * Unique mapping
* The sample structure showed the strongest separation by the main biological contrast
  * PCA (key figure)
  * Interpretation of PC1 / PC2
  * Genotype analysis
* Differential expression identified the strongest transcriptomic changes
  * PCA (key figure)
    * Explain how it is separated, PC1 and PC2
  * MA plot
  * Cumulative Distribution Plot (bend-point / elbow rule)
  * Volcano Plot (Important Genes)
    * Include a secondary Volcano Plot with a new threshold
  * Heatmap
    * Including the interpretation of the distance heatmap between the two conditions
* Bend-point selection narrowed the main follow-up sets
  * Cumulative plot
  * Selected gene counts
  * Why this helped interpretation
  * Secondary volcano plot, if you keep it
* Functional enrichment connected DE results to broader biology
  * GO / pathway results
  * Pathway level / Panther analysis
    * Go through the plots listed by Panther
  * Proteostasis
  * Translation
  * Metabolism
  * Extra analysis, once finalized

**Discussion**

* Main biological interpretation (what does the data show)
  * What the data show overall
  * Strongest supported signal
  * What is primary vs secondary
  * Gene expression differences
    * Injury vs control
  * Pathways being affected
    * Proteostasis (AhR activation)
    * Translation (suppression / upregulation of genes)
    * Metabolism (energy output)
* What was unusual or needs caution (things that were weird about the dataset to consider)
  * Odd volcano plots
  * The genotype signal appears weaker / secondary
  * PCA collisions / overlap
  * Interpretation vs causation
* What this adds beyond the original paper
  * Expands the analysis beyond the paper’s candidate genes
    * Helps link pathways
      * Proposed and new
  * Helps link the pathways already proposed in the paper with additional transcriptomic signals
  * Connects newly identified genes to the genes highlighted in the paper through broader transcriptomic patterns
  * Moves interpretation from single-gene emphasis toward pathway- and network-level context
* NGS in the context of this paper
  * Global discovery
  * Reproducibility
  * External applications / biological relevance
    * How does our global discovery connect to the genes found in the paper
    * Two-hybrid screening
* Future validation (what it suggests for future validation)
  * qPCR for key differentially expressed genes
  * Functional follow-up experiments for injury-response candidates
  * Two-hybrid screening only if it remains biologically justified
* Limitations and cautions
  * Weaker genotype signal
  * PCA overlap / collisions
  * Dependence on the original dataset design
  * Interpretation vs causation

**References (APA)**

* [Main Paper](https://www.nature.com/articles/s41586-026-10295-z#code-availability)
* NGS overview / background sources
* Additional papers using or reviewing NGS
* Background sources for the mouse study
* Minimum of 15 primary sources in the final paper

**Code Availability**

* Git repository
* Notebook(s)

**Source Data**

* CSVs / tables supporting plots
* Data frames / exported tables

**Supplemental Material**

* Full figure set
* Additional supporting outputs
