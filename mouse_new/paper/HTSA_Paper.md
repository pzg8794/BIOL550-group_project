Nikhi Boggavarapu  
Sam Kopelev  
Piter Garcia

**Introduction**

* Brief intro about high-throughput sequencing  
  * Types of NGS  
    * Organized by read length  
    * application  
  * Benefits of NGS  
    * High throughput  
    * fast  
  * What our goal was: utilizing NGS  
    * Unbiased, transcriptome-wide detection of gene expression changes  
* Introduce paper/dataset   
  * Discussing methods  
    * Experimental design  
  * Goals of the paper   
    * Why did they analyze DRG with cKO  
      * Ipsilateral vs contralateral  
* How we wanted to use the paper  
  * explore/ confirm suggested pathway  
    * FF/cre  
* Claim  
  * *Differential expression (DE):* “Next Gen. Seq. helps us understand what actual genes are at play beyond the ones the paper discussed.”  
  * *Key contrasts:* We quantified expression differences across the main experimental comparisons, especially ipsilateral vs contralateral DRG (and genotype where relevant).  
  * *GO / pathway enrichment:* We interpreted DE gene sets in terms of broader biological processes and pathways linked to injury response and the cKO context.

**Materials and Methods** 

* Dataset and study design  
  * Public dataset accession  
  * Tissue and injury context  
  * Sample groups and contrasts  
  * Why was this subset retained  
* Pipeline Steps  
  * Data collection and preprocessing (Aggregation/Collection)  
    * Download SRR (file type gz)   
      * Tool:   
    * FASTQ organization  
    * sample manifest/metadata table  
  * Quality control and trimming  
    * Raw FASTQC/MultiQC  
    * FASTP (trimming)  
    * post-trim  FASTQC and MultiQC  
    * key QC checkpoint metrics  
  * Alignment and count generation  
    * reference genome and annotation (Selection of the Genome)  
      * (mm39)  
    * STAR index and alignment  
      * Building STAR Genome  
      * Align one paired-end  
    * GeneCounts output  
    * BAM/log/count outputs  
    * family count matrix assembly  
  * Analysis/Interpretation  
    * MultiQC  
    * Differential Expression Analysis  
      * DESeq2 setup  
      * DESeq2  
        * Volcano Plot  
        * Heatmap of Top DEGs (Regeneration-Enhancing)  
        * MA plot  
        * Target Validation (Gene Expression Boxplots)  
      * filtering rule  
      * modeled contrasts  
      * thresholds/significance criteria  
    * Follow-up selection and functional interpretation  
      * bend-point rule  
      * GO Analysis  
      * GSEA Analysis  
      * Panther Analysis  
    * Extra?

**Results**

* Dataset quality supported downstream analysis (Quality control)  
  * Requirements for the dataset  
    * Number of samples, length  
  * Pre-Trim  
    * GC content  
    * Adapter sequences  
  * Alignment stats  
    * Unique mapping  
* The sample structure showed the strongest separation by the main biological contrast  
  * PCA  
  * interpretation of PC1 / PC2  
  * genotype analysis  
* Differential Expression Plots (Discuss biological interpretation) \- Differential expression identified the strongest transcriptomic changes  
  * PCA (VERY IMPORTANT)  
    * Explain how it is separated, PC1 and PC2  
  * Volcano Plot (Important Genes)  
    * Cumulative Distribution Plot (2nd derivative is 0\)  
    * Do a secondary Volcano Plot  
  * Heatmap  
    * Explaining the distance heatmap between the two conditions  
* Bend-point selection narrowed the main follow-up sets  
  * cumulative plot  
  * selected gene counts  
  * why this helped interpretation  
* Functional enrichment connected DE results to broader biology  
  * GO / pathway results  
    * Pathway level/Panther Analysis  
      * Go through the plots listed by Panther  
  * proteostasis  
  * translation  
  * metabolism  
* \*Extra analysis once determined\*

**Discussion \~** Discuss the biological interpretation more

* Main biological interpretation (What does the data show)  
  * What the data show overall  
  * Strongest supported signal  
  * What is primary vs secondary  
  * Gene expression differences  
    * Injury vs control  
  * Pathways being affected  
    * proteostasis (AhR activation),   
    * translation (suppression/upregulation of genes)   
    * metabolism (energy output)  
* Things that were weird about the dataset to consider  
  * Reference Odd volcano plots  
    * The genotype is weaker / secondary  
  * collisions in PCA  
    * interpretation vs causation  
* Discussion about NGS in the context of this paper  
  * Global Discovery  
    * External Application  
    * Reproducibilty  
* External Applications/Biological Relevance  
  * How does our Global discovery (new genes connect to the gene found in the paper)

    * # Two-hybrid screening

* What this adds beyond the original paper  
  * Expands the analysis beyond the paper’s candidate genes  
    * Helps link pathways  
      * Proposed and new  
  * Connects newly identified genes to the genes highlighted in the paper through broader *transcriptomic patterns*  
  * Moves the interpretation from single-gene emphasis to *pathway- and network-level* context  
* Future validation (What it suggests for future validation)  
  * Two-hybrid screening to test possible interactions involving the paper’s genes and newly identified candidates  
  * Targeted expression validation, such as *qPCR*, for key differentially expressed genes  
  * Functional follow-up experiments to test whether these candidate genes affect the *injury-response phenotype*  
* Limitations and cautions  
  * weaker genotype signal  
  * PCA overlap/collisions  
  * dependence on the original dataset design  
  * interpretation vs causation

**References (APA)**

* [Main Paper](https://www.nature.com/articles/s41586-026-10295-z#code-availability)   
* NGSTech overview (paper for my courses)  
* ADD papers that use/review NGS   
* More papers referencing the background of the mouse study

**Code Availability**  
Attach git, notebook

**Source Data**  
Data supporting the graphs/ plots (actual csv)  
Dataframes…

**Supplemental Material**  
All figures