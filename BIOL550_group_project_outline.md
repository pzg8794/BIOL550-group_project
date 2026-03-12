# outline

# **BIOL550 Group Project Plan Outline**

*January 27, 2026 | BIOL550: High Throughput Sequencing Analysis (Spring 2026\)*

## Documentation links

- Group project documentation map: [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)
- Group project workspace hub: [README.md](README.md)
- Group project work log: [WORKLOG.md](WORKLOG.md)
- Active mouse workflow: [mouse/PROCESS_mouse_fastq_fastqc_fastx.md](mouse/PROCESS_mouse_fastq_fastqc_fastx.md)
- Active mouse TODO: [mouse/TODO_mouse.md](mouse/TODO_mouse.md)
- Active mouse remediation plan: [mouse/TODO_qc_remediation.md](mouse/TODO_qc_remediation.md)

Use this file for the original plan and team responsibilities. Use the work log and mouse docs for what actually happened after the dataset pivot.

## **Team Roster**

| No | Name | Expertise | Role | Key Phases | Lead Deliverable |
| :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | Samuel Kopelev | Bioinformatics | Computational Biology Lead | Weeks 6-11 | Pipeline, aligned reads, Methods (computational) |
| 2 | Piter Garcia | Data Science grad (CS background) | Statistical Analysis & Fairness Lead | Weeks 11-15 | DE results, fairness audit, visualizations, Methods (statistical) |
| 4 | Nikhi Boggavarapu | Undergraduate | Research Support | Weeks 1-16 | GitHub, Data organization, literature coordination, and meeting notes |

## **3-Phase Analysis Pipeline**

* Phase 1 (Weeks 6-8): Primary Analysis \- FastQC, quality trimming, adapter/contamination filtering, clean reads  
* Phase 2 (Weeks 10-11): Secondary Analysis \- Bowtie2/TopHat alignment, BAM files \+ fairness audit (disparate impact)  
* Phase 3 (Weeks 12-15): Tertiary Analysis \- Differential expression, statistical rigor, visuals, fairness metrics in DE results  
* Bonus (Weeks 15-16): Optional \- SNP calling, isoform analysis, network analysis, machine learning classification

**Implementation note (what we actually built):** we implemented a repeatable, low-load pipeline on Sequoia that runs **download → FastQC (raw)**, followed by a second pipeline for **FASTX trim → FastQC (trimmed)**. The exact commands and shared folder paths are captured in `Semester5/BIOL550/BIOL550-Lab/task_n_desc.md`.

> Tooling note (2026-03-05): FASTX is fine for basic quality trimming, but for “targeted trimming” (adapter remnants / known end sequences) on paired-end reads, prefer `fastp`; for primer/amplicon trimming, use `cutadapt`. See `Semester5/BIOL550/BIOL550-Notes.md` (“fastp vs FASTX Toolkit”) for commands.

**Update (2026-03-02):** the instructor confirmed the zebrafish dataset (`PRJNA1277581`) is **single-cell RNA-seq**. Any decision to switch datasets should account for assay type (bulk vs single-cell) and analysis feasibility.

**Update (2026-03-02): mouse dataset reset:** we are repeating the same primary pipeline on a mouse dataset and keeping all artifacts dataset-scoped to avoid mixing. Reusable scripts/notebooks live in `Semester5/BIOL550/group_project/pipelines/`, and zebrafish artifacts were archived to `Semester5/BIOL550/group_project/_tmp_zebrafish_2026-03-02/` so they can be deleted later. Work log: `Semester5/BIOL550/group_project/WORKLOG.md`.

## **Key Responsibilities**

* *Samuel (Computational):* FastQC, CutAdapt/FASTX quality trimming, Bowtie2/TopHat alignment, BAM file generation, GitHub repo management, reproducible pipeline documentation  
* *Piter (Statistical):* Differential expression quantification (Cufflinks/RSEM), statistical tests (FDR, Bonferroni), fairness metrics (disparate impact, equalized odds), publication-quality visualizations (volcano plots, heatmaps, boxplots)  
* *Nikhi (Support):* Data organization and metadata management, literature compilation, coordination support, meeting notes, and decision log tracking

## **Timeline & Key Deadlines**

* Week 3 (Feb 2): Dataset selection with scientific rationale  
* Week 6 (Feb 16): Primary Stage Analysis begins  
* Week 8 (Mar 2): Primary Stage complete; Secondary Analysis ready  
* Week 11 (Mar 23): Fairness Audit Report (Piter lead)  
* Week 12 (Mar 30): Tertiary Stage Analysis begins  
* Week 13 (Apr 6): Paper Draft 1 \- Outline  
* Week 14 (Apr 13): Paper Draft 2 \- 50% complete (Methods \+ half of Results)  
* Week 15 (Apr 20): Paper Draft 3 \- 90% complete (all Results \+ Discussion draft)  
* Week 16 (Apr 27): Final Paper due 11:59 pm

## **Weekly Meeting & Coordination**

Thursday 12:30-2:00 pm (Post-workshop) \- Mandatory for all members  
Decision Log (GitHub): Track analysis decisions, rationale, owner, fairness implications, status  
Communication:

* GitHub Issues: Technical questions and blockers  
* Email: Scheduling and urgent updates  
* Weekly meetings: Progress reports, data handoffs, collaborative problem-solving

##  **BETTER APPROACH: Where to Actually Find Datasets**

## 

## **Option 1: TCGA (Still Good\!) \- Not GEO**

## **TCGA-BRCA (Breast Cancer) \- KEEP THIS ONE**

* Why it's different from GEO:  
  * Professionally curated by NCI  
  * Standardized clinical data  
  * Preprocessed options available  
  * Clear documentation  
  * Multiple download portals

Access Methods (NOT through GEO):

1. GDC Data Portal (Best for TCGA)  
   * Link: [https://portal.gdc.cancer.gov/projects/TCGA-BRCA](https://portal.gdc.cancer.gov/projects/TCGA-BRCA)  
   * Clean interface, filtered downloads  
   * Clinical data standardized  
   * Can select specific files needed  
2. UCSC Xena Browser (Easiest)  
   * Link: [https://xenabrowser.net/datapages/?cohort=TCGA%20Breast%20Cancer%20(BRCA)](https://xenabrowser.net/datapages/?cohort=TCGA%20Breast%20Cancer%20\(BRCA\))  
   * Pre-processed counts available  
   * Visualization tools included  
   * Metadata well-organized  
3. cBioPortal  
   * Link: [https://www.cbioportal.org/study/summary?id=brca\_tcga](https://www.cbioportal.org/study/summary?id=brca_tcga)  
   * Clinical data easy to access  
   * Integrated with expression data

## **Option 2: What Professor Osier ACTUALLY Wants**

## **🔍 Look for These Instead:**

## **A. SRA BioProjects (Not Individual GEO Studies)**

Better search method: Find entire BioProject collections with:

* Complete study design documentation  
* Multiple experiments linked together  
* Clear sample groups  
* Published papers with methods

Example \- COVID-19 Dataset (Better Version):

* BioProject: PRJNA631753  
* Direct SRA Link: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA631753](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA631753)  
* Why better: All experiments grouped, clear study design, linked to publication  
* Paper: Published in Cell, complete methods  
* Metadata: Standardized across all samples

## 

## **B. Recount3 (Pre-Processed RNA-Seq Compendium)**

What it is: Pre-processed RNA-Seq data from SRA, ready to use  
Link: [https://rcount.bioconductor.org/](https://rcount.bioconductor.org/)  
Advantages:

* ✓ Already processed through a consistent pipeline  
* ✓ Quality metrics computed  
* ✓ Metadata extracted and standardized  
* ✓ Count matrices ready to download  
* ✓ Can start at differential expression immediately

How to search:

1. Go to [http://rcount.bioconductor.org/](http://rcount.bioconductor.org/)  
2. Search by organism or keyword  
3. Browse projects with 20+ samples  
4. Download processed count data \+ metadata

Example Recount3 Projects:

* GTEx (Genotype-Tissue Expression) \- multiple tissues, 17,382 samples  
* TCGA (all cancer types)  
* SRA studies that have been reprocessed

## **C. ArrayExpress (European Alternative to GEO)**

Link: [https://www.ebi.ac.uk/biostudies/arrayexpress](https://www.ebi.ac.uk/biostudies/arrayexpress)  
Why it might be better:

* More standardized metadata requirements  
* Better quality control  
* Clearer experimental design annotations  
* Links to ENA (European Nucleotide Archive) for raw data

Search for: "RNA-seq" \+ "Homo sapiens" \+ your topic

## **D. GTEx Portal (Best for Human Tissue Expression)**

Link: [https://gtexportal.org/](https://gtexportal.org/)  
What it is: Multi-tissue gene expression reference from 948 donors  
Potential Projects:

* Compare gene expression across tissues (heart vs. liver vs. brain)  
* Sex differences in tissue expression (54 tissues × sex)  
* Age effects on gene expression  
* Population differences (ancestry data available for donors)

Advantages:

* ✓ Gold standard quality  
* ✓ Consistent processing  
* ✓ Rich metadata (age, sex, ancestry, ischemic time)  
* ✓ Easy download  
* ✓ Pre-computed statistics available

## **REVISED TOP 5 (Non-GEO Sources)**

## **\#1: TCGA Breast Cancer (via GDC Portal)**

* Source: [https://portal.gdc.cancer.gov/projects/TCGA-BRCA](https://portal.gdc.cancer.gov/projects/TCGA-BRCA)  
* NOT GEO: Direct from NIH/NCI  
* Samples: 1,098 tumors \+ normals  
* Metadata: Standardized clinical data (race, ethnicity, stage, subtype)  
* Access: GDC Data Portal or Xena Browser  
* Why it works: Professionally curated, well-documented

## **\#2: GTEx Multi-Tissue Sex Differences**

* Source: [https://gtexportal.org/](https://gtexportal.org/)  
* Project: Genotype-Tissue Expression Consortium  
* Samples: 17,382 samples across 54 tissues  
* Groups:  
  * Males vs. Females (all tissues)  
  * Young vs. Old (age stratification)  
  * Ancestry groups (European, African, Asian)  
* Access: GTEx Portal direct download  
* Fairness goldmine: Sex × tissue × age × ancestry  
* Why it works: Gold standard, fully processed, standardized

## **\#3: COVID-19 via Published BioProject**

* BioProject: PRJNA631753 or PRJNA646224  
* Direct Link: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA631753](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA631753)  
* Paper: Cell 2020 (highly cited)  
* Samples: 100+ samples (severity stratified)  
* Groups: ICU vs. moderate vs. mild vs. healthy, sex, age  
* Access: SRA Run Selector from BioProject page  
* Why it works: Published study, clear methods, complete metadata

## **\#4: Recount3 \- Diabetes Study Collection**

* Source: [http://rcount.bioconductor.org/](http://rcount.bioconductor.org/)  
* Search: "diabetes" OR "T2D" in the Recount3 portal  
* Samples: Multiple studies aggregated, 20-50 samples each  
* Advantage: Pre-processed, count matrices ready  
* Why it works: Osier can verify quality before students start

## **5: Ask Professor Osier for Pre-Selected Options**

## **WHAT WECOULD DO (Optional):**

## **For Professor Osier :**

1. What data repositories do you recommend we use? TCGA? GTEx? Recount3? Specific BioProjects?  
2. Are there datasets you've used in previous years that worked well for this course?  
3. For our interests (COVID host response, cancer disparities, sleep deprivation, diabetes, sickle cell), which repositories would have suitable data with good metadata quality?"

## **Why This Approach Works:**

1. Addresses his concern  
2. Asks for guidance  
3. Still advocates for the group interests  
4. Positions us as thoughtful about data quality  
5. Opens the door for him to share pre-vetted datasets

## **Updated Strategy:**

## **Immediate (In Workshop):**

1. ✓ Get clarification on data sources he's used successfully

## **After Workshop:**

1. ✓ Explore TCGA/GTEx portals  
2. ✓ Find BioProjects (not GEO accessions) for your interests

## **Bottom Line:**

Professor Osier is right that GEO metadata is a disaster for teaching purposes.  
Your best move:

1. Ask for recommended repositories  
2. Check if he has pre-selected datasets  
3. Focus on professionally curated sources (TCGA, GTEx, Recount3, published BioProjects)

## **Datasets that meet all requirements**

### **1\) PRJNA1406761 — iPSC small‑intestine organoids**

* **BioProject:** [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1406761](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1406761)  
* **SRA Study (SRP):** [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP665664](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP665664)  
* **Representative SRR:** SRR36938303 (example run; \~41M spots)  
* **Quick verification:** BioProject shows SRA experiments and run-level data consistent with **2×150** and per‑sample depth ≈30–50M.

*Find & verify runs (web \+ CLI):*

1. Open the BioProject link → click **SRA** or **All experiments** → follow the SRA Run Selector.  
2. In Run Selector, click **Download** → **RunInfo Table (CSV)**.   
3. Inspect columns: Run, LibraryLayout (should be PAIRED), avgSpotLen / avgLength (\~300 for 2×150), spots, bases, Platform.  
4. (CLI) Run:  
   * esearch \+ efetch:  
     esearch \-db sra \-query "SRP665664" | efetch \-format runinfo \> PRJNA1406761\_runinfo.csv  
   * Inspect avgLength / LibraryLayout in the CSV.

### **2\) PRJNA717662 — Long‑term blood transcriptome after SARS‑CoV‑**

* **BioProject:** [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA717662](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA717662)  
* **SRA Study (SRP):** [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* **Representative SRR:** SRR15510543 (example run; \~70M spots)  
* Verification: BioProject lists **152 SRA experiments**, **GEO: GSE169687**, and run info consistent with **2×150** deep runs.

*Find & verify runs:*

1. Open the BioProject → click **SRA** / **All experiments** → use Run Selector → **Download RunInfo CSV**.  
2. Check LibraryLayout \= PAIRED and avgLength ≈300 / spots for depth.  
3. (CLI) Example: esearch \-db sra \-query "SRP312283" | efetch \-format runinfo \> PRJNA717662\_runinfo.csv

## 

## 

## **Dataset Validation Example: PRJNA717662 (Manual Steps)**

Below is a step-by-step guide to manually validate and filter a public SRA dataset (PRJNA717662) for class requirements. This process is fully transparent and reproducible by anyone with basic command-line skills.

### 

### **1\. Download the SRA RunInfo Table (CSV)**

* **Install Entrez Direct** (if not already):  
  * macOS: brew install entrez-direct  
  * Linux: see [https://www.ncbi.nlm.nih.gov/books/NBK179288/](https://www.ncbi.nlm.nih.gov/books/NBK179288/)  
* **Download the RunInfo CSV:**

```shell
cd /Users/pitergarcia/DataScience/Semester5/BIOL550/BIOL550-Lab/project_datasets
esearch -db sra -query "PRJNA717662" | efetch -format runinfo > PRJNA717662_runinfo.csv
```

### 

### **2\. Inspect and Filter the CSV**

* **Open the CSV** in Excel, Google Sheets, or with pandas/csvkit to explore columns:  
  * Run (SRR ID)  
  * LibraryLayout (should be PAIRED)  
  * avgLength (should be ≥300 for 2×150)  
  * spots (should be ≥40,000,000)  
  * ScientificName (should be Homo sapiens)  
* **Manual filtering:**  
  * Keep only rows where:  
    * LibraryLayout \= PAIRED  
    * avgLength ≥ 300  
    * spots ≥ 40,000,000  
    * ScientificName \= Homo sapiens  
  * Randomly select 20 SRR IDs from the filtered list for downstream analysis.  
* **Automated filtering (optional, for reproducibility):**  
  * Use the provided Python script:

```py
python filter_PRJNA717662_runinfo.py PRJNA717662_runinfo.csv PRJNA717662_20srrs.txt
```

  * This will output a text file with 20 qualifying SRR IDs.

### 

### **3\. Document Your Filtering**

* Save the filtered CSV or SRR list as evidence of your selection.  
* Note the exact criteria used (see above) and the date of download.

### 

### **4\. Next Steps**

* Use the resulting SRR list for FASTQ download and FastQC analysis as described in the rest of this document.

Ran FastQC on the test FASTQs

## **Writeup: SRA Dataset Selection & Evaluation**

### **1\. PRJNA717662 — Long-term Blood Transcriptome after SARS-CoV-2**

* **Project Accession:** [PRJNA717662](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA717662)  
* **Description:** This study profiles the blood transcriptome of 152 individuals at multiple time points after SARS-CoV-2 infection, using Illumina NovaSeq 6000 (paired-end, 2×150 bp). *The goal is to understand long-term changes in immune and gene expression post-infection.*  
* **Sample Size:** 152 SRA runs (all human, paired-end).  
* **Read Depth:** Most samples have 40–70 million fragments (spots), with an average spot length of \~300 (2×150 bp). This meets the class requirement for depth and reading length.  
* **Case/Control:** The dataset includes both post-infection and control samples, with metadata indicating time since infection and clinical status.  
* **Strengths:**  
  * Large sample size and deep sequencing.  
  * Publicly available, no access restrictions.  
  * Well-annotated with clinical metadata.  
* **Weaknesses:**  
  * Some samples may have lower depth (\<40M), so filtering is needed.  
  * Case/control definitions may require careful review of metadata.  
    

### **2\. PRJNA292477 — TOPMed / Framingham Heart Study Transcriptome**

* **Project Accession:** [PRJNA292477](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA292477)  
* **Description:** This project is part of the NHLBI TOPMed program, profiling the transcriptome of Framingham Heart *Study participants to investigate genetic and environmental influences on cardiovascular health.*  
* **Sample Size:** Hundreds of samples (exact number depends on filtering).  
* **Read Depth:** Most samples have 40–75 million fragments, paired-end 2×150 bp reads.  
* **Case/Control:** The study includes a range of phenotypes (e.g., cardiovascular disease, controls), but some clinical metadata may be dbGaP-controlled.  
* **Strengths:**  
  * Large, well-characterized cohort with deep sequencing.  
  * Rich phenotype and longitudinal data.  
* **Weaknesses:**  
  * Some metadata is controlled-access (dbGaP), which may limit analysis.  
  * Requires careful selection of samples to match case/control definitions.

## **Validating Chosen Datasets (\~= 40 mins)**

Validation criteria used here (no Human/Public requirement):

* RNA-Seq (LibraryStrategy)  
* ≥20 samples (runs)  
* LibraryLayout \= PAIRED  
* avgLength ≥ 150 bp  
* spots ≥ 40,000,000 (fragments)

**Assay modality note (bulk vs single-cell):** some “RNA-Seq” projects are single-cell. We maintain a dataset modality table (with evidence links) in `Semester5/BIOL550/BIOL550-Lab/task_n_desc.md#dataset-modality-check-bulk-vs-single-cell--double-checked-2026-03-02` and update it when the instructor clarifies assay type.


**PRJNA1184725**

* BioProject: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1184725](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* SRA Study (SRP544461): [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP544461](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* Project Accession: PRJNA1184725  
* Description: QKI dysregulation induces extensive splicing changes in T-Cell Acute Lymphoblastic Leukemia (T-ALL).  
* Sample Size: 40 runs (total)  
* Valid samples (meet criteria above): 40/40  
* Organism (info): Homo sapiens  
* Read Depth: avgLength 297–301; spots 57.9M–221.4M  
* Strengths:  
  * Consistent, long reads (spot length \~300).  
  * All runs exceed the 40M fragment threshold.  
* Weaknesses: Disease-specific context (T-ALL) may constrain topic choices.


**PRJNA1164690**

* BioProject: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1164690](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* SRA Study (SRP534424): [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP534424](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* Project Accession: PRJNA1164690  
* Description: Hyperactive PI3K-delta in Th1 and Th2 differentiation (RNA-seq).  
* Sample Size: 42 runs (total)  
* Valid samples (meet criteria above): 42/42  
* Organism (info): Mus musculus (mouse)  
* Read Depth: avgLength 202; spots 123.4M–231.1M  
* Strengths:  
  * Very deep sequencing across all runs.  
  * Clean, uniform run-level metadata (paired layout, consistent length).  
* Weaknesses: Mouse model; direct translation to human biology may be limited.


**PRJNA1277581**

* BioProject: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1277581](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* SRA Study (SRP592470): [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP592470](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* Project Accession: PRJNA1277581  
* Description: Müller glia–microglia cross-talk reprograms the Müller glia transcriptome during retina regeneration.  
* Sample Size: 30 runs (total)  
* Valid samples (meet criteria above): 30/30  
* Organism (info): Danio rerio (zebrafish)  
* Read Depth: avgLength 302; spots 50.9M–173.3M  
* Workspace: `Semester5/BIOL550/group_project/zebrafish/` (scripts + run lists; downloaded data is gitignored)
* Strengths:  
  * Strong depth and long reads across all runs.  
  * Clear biological focus (retina regeneration) with many samples.  
* Weaknesses: Zebrafish model; may not fit projects requiring mammalian/human context.
  * **Update (2026-03-02):** single-cell RNA-seq per instructor confirmation.

**PRJNA1222833**

* BioProject: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1222833](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* SRA Study (SRP563445): [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP563445](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* Project Accession: PRJNA1222833  
* Description: Systemic lupus cutaneous photoresponses show dysregulated epidermal inflammation and inflammatory myeloid cell infiltration.  
* Sample Size: 30 runs (total)  
* Valid samples (meet criteria above): 30/30  
* Organism (info): Homo sapiens  
* Read Depth: avgLength 179–302 (mixed); spots 98.6M–271.0M  
* Strengths:  
  * Very deep sequencing; all runs exceed 40M fragments.  
  * Good sample count for group comparisons.  
* Weaknesses:  
  * Mixed read length suggests multiple sequencing setups; this can complicate uniform processing.

**PRJNA1331709**

* BioProject: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1331709](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* SRA Study (SRP622479): [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP622479](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* Project Accession: PRJNA1331709  
* Description: Pulmonary fibrosis after COVID-19 is characterized by airway abnormalities and elevated club cell secretory protein-16.  
* Sample Size: 34 runs (total)  
* Valid samples (meet criteria above): 34/34  
* Organism (info): Homo sapiens  
* Read Depth: avgLength 222–322; spots 66.8M–485.9M  
* Strengths:  
  * All runs exceed 40M fragments; wide depth range supports robust analyses.  
  * Good sample count (≥20) and paired layout.  
* Weaknesses:  
  * Large variability in depth (66.8M–485.9M) may require normalization/stratification decisions.

**PRJNA292477**

* BioProject: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA292477](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* SRA Study (SRP058181): [https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP058181](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* Project Accession: PRJNA292477  
* Description: NHLBI TOPMed: The Framingham Heart Study.  
* Sample Size: 73 runs (in our downloaded RunInfo table)  
* Valid samples (meet criteria above): 34/73  
* Organism (info): Homo sapiens  
* Read Depth: avgLength 202; spots 10.0M–83.5M  
* Strengths:  
  * Large cohort context; many potential downstream phenotype-related questions.  
  * Subset of runs meets the 40M fragment depth threshold.  
* Weaknesses:  
  * Many runs are shallow (\<40M): 39/73 fail the depth cutoff.  
  * Some phenotype/clinical metadata may be linked to dbGaP (access/availability can vary).

**PRJNA717662**

* BioProject: [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA717662](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)  
* SRA Study (SRP312283): [https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1184725](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP312283)   
* Project Accession: PRJNA717662  
* Description: Long-term perturbation of the blood transcriptome months after SARS-CoV-2 infection.  
* Sample Size: 152 runs (total)  
* Valid samples (meet criteria above): 152/152  
* Organism (info): Homo sapiens  
* Read Depth: avgLength 287–300; spots 43.8M–108.3M  
* Strengths:  
  * Large sample size with consistent run characteristics.  
  * All runs pass the ≥40M fragment cutoff.  
* Weaknesses:  
  * The study's focus is on post-COVID immune/blood transcriptome; it may not align with unrelated topics.

**Summary Table**

| BioProject | Organism (info) | Total Runs | Valid Runs (≥150bp, ≥40M, paired, RNA-Seq) | ≥20 Samples | ≥150bp | ≥40M Fragments | RNA-Seq | Passes All? |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| PRJNA1184725 | Homo sapiens | 40 | 40 | Yes (40) | Yes | Yes | Yes | Yes |
| PRJNA1164690 | Mus musculus | 42 | 42 | Yes (42) | Yes | Yes | Yes | Yes |
| PRJNA1277581 | Danio rerio | 30 | 30 | Yes (30) | Yes | Yes | Yes | Yes |
| PRJNA1222833 | Homo sapiens | 30 | 30 | Yes (30) | Yes | Yes | Yes | Yes |
| PRJNA1331709 | Homo sapiens | 34 | 34 | Yes (34) | Yes | Yes | Yes | Yes |
| PRJNA292477 | Homo sapiens | 73 | 34 | Yes (73) | Yes | Partial (34/73) | Yes | Partial |
| PRJNA717662 | Homo sapiens | 152 | 152 | Yes (152) | Yes | Yes | Yes | Yes |

# 

# **Write-up Feedback**

Verifying the two specific dataset claims (sample count, depth range, read length) directly from the RunInfo CSVs I downloaded, then verified accuracy and fixes in the write-up.

* The two chosen projects/titles are correct:  
  * The mouse axon regeneration study is BioProject **PRJNA1017789**.  
  * The zebrafish retina regeneration study is BioProject **PRJNA1277581**.  
* **PRJNA1017789 (mouse)**: your write-up is *close*.  
  * Sample count: **26** (correct).  
  * “Fragments between 40 and 60M”: **almost** — RunInfo shows **40.1M–65.4M spots** (upper end is \~65M, not 60M).  
  * “Average fragment length 302 bp”: RunInfo shows **avgLength \= 302** (correct value, but see terminology note below).  
* **PRJNA1277581 (zebrafish)**: The write-up is **wrong on the read depth range**.  
  * Sample count: **30** (correct).  
  * “Fragments between 40 and 60M”: **incorrect** — RunInfo shows **50.9M–173.3M spots** (many runs are far above 60M, up to \~173M).  
  * “Average fragment length 302 bp”: RunInfo shows **avgLength \= 302** (correct value, terminology note below).  
* **Terminology/interpretation fix (important):**  
  * In SRA RunInfo, **spots** are what you’ve been calling “fragments.” For paired-end data, a “spot” is typically a **read pair**.  
  * avgLength in RunInfo is the **average spot length** (sum across reads in the spot). So, avgLength ≈ 302 implies paired-end reads of roughly **2×151 bp**, not a physical DNA/RNA “fragment length” in the library-prep sense.

Change the two dataset summaries to report **spots** exactly as:

* PRJNA1017789: **40.1M–65.4M**  
* PRJNA1277581: **50.9M–173.3M**

Hey @Samuel Kopelev (slk1379) and @Nikhi Boggavarapu (nb6672) — would you be open to a quick 15-minute call tomorrow, **any time on/after 5 pm,** to reset and clear up misunderstandings?

My goal is to align on what happened and how we move forward. I’ll take responsibility for my part and briefly show my workspace so it’s clear what I meant (5 minutes). Then, you each can take the time to share anything I may have misunderstood, or that didn’t sit right (about 5 minutes each). If after that either of you still feels uncomfortable, that’s totally okay—we can be straightforward with the professor about it. 

If we can do this first, it’ll make our meeting with the professor more productive and focused on the next steps rather than confusion. If you’re not available after 5 pm, tell me a time that works, and I’ll try to adjust. If we can’t meet beforehand, we’ll address it when we meet with the professor.

Hi Dr. Osier,

For GSM794483\_C1\_R1\_STAR\_alignment.tgz, I used the NCBI/RefSeq D. melanogaster assembly GCF\_000001215.4 (FASTA+GTF from NCBI datasets) and built the STAR index from that matched pair. The paths on Sequoia were:

* FASTA: /home/pzg8794/refs/GCF\_000001215/ncbi\_dataset/data/GCF\_000001215.4/GCF\_000001215.4\_Release\_6\_plus\_ISO1\_MT\_genomic.fna  
* GTF: /home/pzg8794/refs/GCF\_000001215/ncbi\_dataset/data/GCF\_000001215.4/genomic.gtf  
* STAR \`--genomeDir\`: /home/pzg8794/star\_index/droso\_refseq\_ncbi

To make sure this wasn’t a reference/annotation naming issue, I also ran the same sample with the class BDGP6.84-style naming (a renamed FASTA to match 2L/2R/3L/3R/... \+ the BDGP6.84 GTF) and compared Log.final.out metrics; the alignment rates were essentially the same (99.20% vs 99.19% uniquely mapped). Based on that, I submitted the RefSeq-based BAM.

Best,    
Piter

Hi Dr. Osier,

Thanks for checking. 

For the submitted BAM ([GSM794483\_C1\_R1\_STAR\_alignment.tgz](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#)), I downloaded the reference from NCBI using the datasets tool (similar to how I’ve handled references in BIO630) and used the matched FASTA+GTF to build the STAR index and run alignment.

Reference \+ index paths on Sequoia:

* FASTA (RefSeq): [GCF\_000001215.4\_Release\_6\_plus\_ISO1\_MT\_genomic.fna](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#)  
* GTF (RefSeq): [genomic.gtf](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#)  
* STAR \--genomeDir: /home/pzg8794/star\_index/droso\_refseq\_ncbi

Quick steps I followed:

1. Download matched reference (FASTA+GTF) via NCBI datasets (GCF\_000001215.4).  
2. Build the STAR index with that FASTA+GTF.  
3. Align [GSM794483\_C1\_R1\_1.fq.gz](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#) \+ [GSM794483\_C1\_R1\_2.fq.gz](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#) with STAR using the same GTF.  
4. Submit [Aligned.sortedByCoord.out.bam](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#) \+ [Log.final.out](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#).

At the beginning, I also tested the same sample using the BDGP6.84-style naming approach and compared [Log.final.out](https://file+.vscode-resource.vscode-cdn.net/Users/pitergarcia/.vscode/extensions/openai.chatgpt-0.4.71-darwin-arm64/webview/#); the mapping rates were essentially the same (99.20% vs 99.19% uniquely mapped), so I proceeded with the RefSeq datasets reference since it was the cleanest/fastest to keep consistent.

If this looks “odd” on your end, is there a specific course-provided reference/version you want us to use for this assignment (or any additional STAR parameters you expect beyond those in the Trapnell analyses pdf?

Best,  
Piter

# ideas

**Random ideas**

**Diseases/Disorders**

- Cystic fibrosis  
- Sickle Cell Anemia  
- THC effect on gene expression in the brain  
- Sleep deprivation's effect on gene expression  
- Cancer disparities (e.g., breast cancer by race/ethnicity)   
- Diabetes (Type 1/2 by ancestry/sex)  
- Cardiovascular disease transcriptomics by population

**pathogens**

- Listeria monocytogenes  
- Mycobacterium tuberculosis  
- Pseudomonas aeruginosa  
- SARS‑CoV‑2  
-  

**Organism**

- Archaea  
- PA  
- 

**Misc**

- Drug response studies stratified by ancestry (pharmacogenomics)

---

Requirements

\= Must be RNASeq

\= Should have at least 20 samples in a project

\= Must have at least 150bp per fragment

\= Should have at least 40 million fragments per sample

\= Must be Eukaryotic

## **REVISED TOP 5 (Non-GEO Sources)**

## **~~\#1: TCGA Breast Cancer (via GDC Portal)~~**

* ## ~~Source:~~ 

* ## [~~https://portal.gdc.cancer.gov/projects/TCGA-BRCA~~](https://portal.gdc.cancer.gov/projects/TCGA-BRCA)

* ## ~~NOT GEO: Direct from NIH/NCI~~

* ## ~~Samples: 1,098 tumors \+ normals~~

* ## ~~Metadata: Standardized clinical data (race, ethnicity, stage, subtype)~~

* ## ~~Access: GDC Data Portal or Xena Browser~~

* ## ~~Why it works: Professionally curated, well-documented~~

## 

## **~~\#2: GTEx Multi-Tissue Sex Differences~~**

* ## ~~Source:~~ 

* ## [~~https://gtexportal.org/~~](https://gtexportal.org/)

* ## ~~Project: Genotype-Tissue Expression Consortium~~

* ## ~~Samples: 17,382 samples across 54 tissues~~

* ## ~~Groups:~~

  * ## ~~Males vs. Females (all tissues)~~

  * ## ~~Young vs. Old (age stratification)~~

  * ## ~~Ancestry groups (European, African, Asian)~~

* ## ~~Access: GTEx Portal direct download~~

* ## ~~Fairness goldmine: Sex × tissue × age × ancestry~~

* ## ~~Why it works: Gold standard, fully processed, standardized~~

## 

## **~~\#3: COVID-19 via Published BioProject~~**

* ## ~~BioProject: PRJNA631753 or PRJNA646224~~

* ## ~~Direct Link:~~ 

* ## [~~https://www.ncbi.nlm.nih.gov/bioproject/PRJNA631753~~](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA631753)

* ## ~~Paper: Cell 2020 (highly cited)~~

* ## ~~Samples: 100+ samples (severity stratified)~~

* ## ~~Groups: ICU vs. moderate vs. mild vs. healthy, sex, age~~

* ## ~~Access: SRA Run Selector from BioProject page~~

* ## ~~Why it works: Published study, clear methods, complete metadata~~

## 

## **~~\#4: Recount3 \- Diabetes Study Collection~~**

* ## ~~Source:~~ 

* ## [~~http://rcount.bioconductor.org/~~](http://rcount.bioconductor.org/)

* ## ~~Search: "diabetes" OR "T2D" in Recount3 portal~~

* ## ~~Samples: Multiple studies aggregated, 20-50 samples each~~

* ## ~~Advantage: Pre-processed, count matrices ready~~

* ## ~~Why it works: Osier can verify quality before students start~~

## 

## **~~\#2: Breast Cancer Health Disparities (TCGA) ⭐⭐⭐⭐⭐~~**

~~Why \#2: Group mentioned "cancer disparities" \+ perfect fairness dataset~~

## **~~Dataset: TCGA-BRCA (The Cancer Genome Atlas)~~**

* ~~Accession: TCGA-BRCA~~  
* ~~Direct Link:~~   
* [~~https://portal.gdc.cancer.gov/projects/TCGA-BRCA~~](https://portal.gdc.cancer.gov/projects/TCGA-BRCA)  
* ~~Alternative Access:~~   
* [~~https://xenabrowser.net/datapages/?cohort=TCGA%20Breast%20Cancer%20(BRCA)~~](https://xenabrowser.net/datapages/?cohort=TCGA%20Breast%20Cancer%20\(BRCA\))  
* ~~Organism: *Homo sapiens* (breast tumor \+ normal tissue)~~  
* ~~Samples: 1,098 tumor samples \+ 113 normal~~  
* ~~Groups:~~  
  * ~~Race: White (n=747), Black/African American (n=183), Asian (n=61), Native American (n=6)~~  
  * ~~Ethnicity: Hispanic vs. non-Hispanic~~  
  * ~~Tumor subtype: Luminal A, Luminal B, HER2+, Basal/Triple-negative~~  
  * ~~Stage: I, II, III, IV~~  
  * ~~Sex: Female (+ 12 male breast cancer)~~  
  * ~~Age: Continuous variable~~  
* ~~Platform: Illumina HiSeq 2000/2500, paired-end~~  
* ~~Read depth: 50-100M reads/sample ✓✓✓~~  
* ~~Fairness goldmine: 🎯🎯🎯🎯🎯~~  
  * ~~Triple-negative breast cancer 2-3× higher in Black women~~  
  * ~~Mortality disparities by race~~  
  * ~~Age at diagnosis differences~~  
* ~~Access: Public, preprocessed options available~~  
* ~~Download: Use GDC Data Portal or UCSC Xena Browser~~

~~Clinical Data File:~~   
[~~https://portal.gdc.cancer.gov/exploration?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project\_id%22%2C%22value%22%3A%5B%22TCGA-BRCA%22%5D%7D%7D%5D%7D~~](https://portal.gdc.cancer.gov/exploration?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-BRCA%22%5D%7D%7D%5D%7D)  
~~Why This Wins:~~

* ~~✓ Group specifically listed "cancer disparities"~~  
* ~~✓ Gold standard dataset \- most complete~~  
* ~~✓ All demographic variables included~~  
* ~~✓ Massive literature support~~  
* ~~✓ Easy download, well-documented~~

## 

## **~~\#3: Sleep Deprivation Effects on Gene Expression ⭐⭐⭐⭐~~**~~Why \#3: Group's specific interest \+ controlled experiment \+ sex/age stratification~~

## **~~Dataset: Sleep Deprivation Time Course~~**

* ~~Accession: GSE171571~~  
* ~~Direct Link:~~   
* [~~https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE171571~~](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE171571)  
* ~~Organism: *Homo sapiens* (whole blood)~~  
* ~~Samples: 24 samples (12 subjects × 2 time points)~~  
* ~~Groups:~~  
  * ~~Rested (baseline) vs. Sleep deprived (24hr)~~  
  * ~~Paired design (same individuals)~~  
  * ~~Sex: Males and females~~  
  * ~~Age: Reported~~  
  *   
* ~~Platform: Illumina NovaSeq 6000, paired-end~~  
* ~~Read depth: 40-60M reads/sample ✓✓~~  
* ~~Fairness potential: 🎯🎯 Sex differences, age effects~~  
* ~~Published: 2021~~

## **~~Alternative: Larger Sleep Study~~**

* ~~Accession: GSE48113~~  
* ~~Direct Link:~~   
* [~~https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE48113~~](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE48113)  
* ~~Organism: *Homo sapiens* (whole blood)~~  
* ~~Samples: 36 samples (multiple sleep conditions)~~  
* ~~Platform: Illumina HiSeq 2000~~  
* ~~Note: May need to verify read depth meets 40M requirement~~

~~Why This Wins:~~

* ~~✓ Group specifically listed this interest~~  
* ~~✓ Clean experimental design~~  
* ~~✓ Neuroscience \+ circadian biology (interesting)~~  
* ~~✓ Paired samples \= strong statistics~~  
* ~~✓ Can stratify by sex, age~~

## 

## **~~\#4: Type 2 Diabetes by Ancestry ⭐⭐⭐⭐⭐~~**

~~Why \#4: Group listed "diabetes by ancestry/sex" \+ massive fairness potential~~

## **~~Dataset: Multi-Ethnic T2D Adipose Tissue Study~~**

* ~~Accession: GSE185013~~  
* ~~Direct Link:~~   
* [~~https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE185013~~](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE185013)  
* ~~Organism: *Homo sapiens* (subcutaneous adipose tissue)~~  
* ~~Samples: 49 samples (T2D patients and controls)~~  
* ~~Groups:~~  
  * ~~Type 2 Diabetes vs. Non-diabetic~~  
  * ~~Ancestry: European, Hispanic, African American~~  
  * ~~Sex: Male and female~~  
  * ~~BMI: Stratified (obesity factor)~~  
* ~~Platform: Illumina HiSeq 4000, paired-end~~  
* ~~Read depth: 50-80M reads/sample ✓✓~~  
* ~~Fairness goldmine: 🎯🎯🎯🎯🎯~~  
  * ~~T2D prevalence: Native American (14.7%), Black (12.1%), Hispanic (12.6%), White (7.4%)~~  
  * ~~Complications differ by ancestry~~  
  * ~~Treatment response differences~~  
* ~~Published: 2022~~

## **~~Alternative: Skeletal Muscle T2D Study~~**

* ~~Accession: GSE106089~~  
* ~~Direct Link:~~   
* [~~https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106089~~](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106089)  
* ~~Samples: 24 samples (muscle biopsies)~~  
* ~~Groups: Insulin resistant vs. sensitive, ancestry data~~

~~Why This Wins:~~

* ~~✓ Group specifically listed diabetes by ancestry/sex~~  
* ~~✓ Explicit ancestry stratification~~  
* ~~✓ Major health disparity (2-4× prevalence difference)~~  
* ~~✓ Clear disease vs. healthy comparison~~  
* ~~✓ Strong literature base~~

## 

## **~~\#5: Sickle Cell Anemia Treatment Response ⭐⭐⭐⭐~~**

~~Why \#5: Group's interest \+ inherent population focus \+ health equity~~

## **~~Dataset: Sickle Cell Disease Hydroxyurea Response~~**

* ~~Accession: GSE162133~~  
* ~~Direct Link:~~   
* [~~https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162133~~](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162133)  
* ~~Organism: *Homo sapiens* (peripheral blood)~~  
* ~~Samples: 32 samples (SCD patients)~~  
* ~~Groups:~~  
  * ~~Sickle cell disease vs. healthy controls~~  
  * ~~Hydroxyurea responders vs. non-responders~~  
  * ~~Ancestry: Predominantly African ancestry (disease-related)~~  
  * ~~Disease severity (mild vs. severe)~~  
* ~~Platform: Illumina NovaSeq 6000, paired-end~~  
* ~~Read depth: 45-70M reads/sample ✓✓~~  
* ~~Fairness goldmine: 🎯🎯🎯🎯~~  
  * ~~SCD affects 1 in 365 Black births vs. 1 in 16,000 Hispanic births~~  
  * ~~Treatment access disparities~~  
  * ~~Health outcome inequities~~  
* ~~Published: 2020~~

## **~~Alternative: SCD Pain Crisis Study~~**

* ~~Accession: GSE158393~~  
* ~~Direct Link:~~   
* [~~https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE158393~~](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE158393)  
* ~~Samples: 48 samples (pain crisis vs. steady state)~~

~~Why This Wins:~~

* ~~✓ Group specifically listed sickle cell~~  
* ~~✓ Population-specific disease (African ancestry)~~  
* ~~✓ Treatment response \= interesting biology~~  
* ~~✓ Clear health disparity angle~~  
* ~~✓ Strong clinical relevance~~

# Options

[https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1277581](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1277581)   
[https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1184725](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1184725)   
[https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1017789](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1017789)   
[https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1164690](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1164690)   
[https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1222833](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1222833)   
[https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1331709](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1331709) 

# Lab Notes

## Date Time: 2026-02-05 09:30:31

## 

## **Summary**

## This series of sessions covers a bioinformatics analysis workflow, focusing on the STAR aligner. The instructor, Mr. Garcia, begins by addressing housekeeping for the FastQC assignment, reminding students to zip and upload their HTML files for review. The main topic then shifts to the two-step process of using the STAR aligner: first, generating a genome index from a reference genome and annotation file, and second, aligning paired-end TruSeq sequencing reads to this index. Throughout the technical guidance, instructors emphasize server etiquette, including monitoring system load with the top command and managing long-running processes with nohup and the & operator to avoid overburdening shared resources. A key rule is to keep the server's load average below 15 when running resource-intensive tasks.

## The sessions also involve hands-on work and troubleshooting. Instructors guide students on debugging STAR aligner errors, such as "fatal input file error" or issues opening genome files, and clarify the difference between reportable programmatic errors (like memory allocation) and non-reportable user syntax errors for lab write-ups. They advise on how to manage runaway processes using kill \[PID\] and the importance of providing specific error messages and commands when seeking help. Due to software conflicts on the server (specifically with R), students are advised against using Cufflinks on the shared system. 

## **Knowledge Points**

### **1\. Assignment Administration and Support**

* ## **FastQC Assignment Submission:** Students must complete the FastQC assignment, zip all generated HTML files, and upload the single zip file. The instructor has already reviewed morning submissions, which were of high quality, and will post grades after feedback is addressed.

* ## **Lab Report Guidelines:** For lab write-ups, students should document commands, outputs, and programmatic errors encountered (e.g., memory issues with LimitGenomeGenerateRAM). Basic user errors like typos or incorrect file paths are not to be reported.

* ## **Troubleshooting and Communication:** When seeking help via email, students must provide the exact command line used and the full error message. Vague descriptions are insufficient. Office hours are available for more in-depth support. The instructor uses Slack for internal IT matters only, not for student communication.

### **2\. Server and Process Management**

* ## **Monitoring System Load:** Before running resource-intensive tasks, students must check the server's load using the top command (or htop). The load average should not exceed 15 when running STAR for the TruSeq dataset.

* ## **Understanding System Load:** System load is a composite measure of server business, including CPU usage and drive access. The server has two CPUs, each with 12 threads.

* ## **Managing Long-Running Processes:** Use nohup at the beginning of a command to prevent termination upon network disconnection. Use an ampersand (&) at the end to run the process in the background and regain terminal access. This is recommended for the genome mapping step.

* ## **Managing Runaway Processes:** A process can be terminated using its Process ID (PID) with the kill \[PID\] command. PIDs for running processes can be found using top.

### 

### 

### **3\. STAR Aligner Workflow**

* ## **Two-Step Process:** The analysis involves two main steps: 1\) generating a genome index (\--runMode genomeGenerate), and 2\) aligning sequencing reads to that index.

* ## **Step 1: Genome Index Generation:**

  * ## This step creates a map of the reference genome using a FASTA file and an annotation file (GTF/GFF).

  * ## **Parameters:**

    * ## \--runMode genomeGenerate: Specifies the task.

    * ## \--genomeDir: Defines the output directory for the index.

    * ## \--genomeFastaFiles: Specifies the reference genome FASTA file.

    * ## \--sjdbGTFfile: Specifies the annotation file.

    * ## \--limitGenomeGenerateRAM: Must be increased from the default value to use available memory.

* ## **Step 2: Read Alignment:**

  * ## This step aligns paired-end sequencing reads against the pre-built genome index.

  * ## **Parameters:**

    * ## \--genomeDir: Points to the directory containing the genome index.

    * ## \--runThreadN: Controls the number of threads. Use 4 if the server is not busy; reduce to 1 if the load is high.

    * ## \--readFilesIn: Specifies the input read files (forward and reverse, separated by a space).

    * ## \--sjdbGTFfile: The same annotation file from step 1 must be used.

  * ## **Paired-End Data:** The TruSeq data is paired-end (\_1 and \_2 files). Each pair (e.g., for one replicate) must be aligned together in a single STAR run. The experiment consists of two conditions (C1, C2) with three replicates each, resulting in six separate alignment runs. STAR uses paired-end information for quality filtering. Students need to find an additional parameter in the documentation for this.

### **4\. Software and Environment Notes**

* ## **Cufflinks and R:** Students are advised not to use Cufflinks for this analysis due to conflicting versions of R on the server. Those wishing to experiment with Cufflinks or R should do so on their local machines.

* ## **Trap Analysis:** The trap analysis must be performed on all available samples.

## **Assignments**

* ## Complete the FastQC analysis, combine HTML files into a single zip file, upload it, and review instructor feedback.

* ## Run the first step of the STAR analysis: genomeGenerate. Determine the correct reference genome and annotation file.

* ##  Use nohup and & to run the genome generation process in the background.

* ## Before running alignments, monitor server load with top. If the load average is near 15, wait or reduce thread count.

* ## For the trap analysis, run the analysis for all samples.

* ## Perform the second STAR step: align the paired-end reads for each sample individually (six total runs). Use a low thread count (e.g., 1\) initially.

* ## Search the STAR aligner documentation for the correct parameter for handling paired-end reads.

* ## Proceed to step three (rest of "trapdoor stuff") after completing the alignments.

* ## For the lab write-up, document commands, outputs, and any programmatic error messages encountered and how they were resolved.

* ## Students needing help should attend office hours (3:00 PM on Feb 5, 2026\) or email the instructor with exact commands and full error messages.

# **Clarification on Assignment Submissions and Course Policies**

## A student, who was unable to complete work due to illness, meets with a professor to clarify submission requirements for FastQC HTML files and a weekly report. The professor details the specific instructions for each assignment, explains the course's flexible submission policy, and confirms that the two tasks are separate deliverables.

## 

## **Initial Query and Justification for Delay**

## The student initiated the conversation to check in with the professor, explaining that they had been unable to finish their work the previous day. They had to go to bed early after experiencing chills and taking Tylenol. Before proceeding with the work, the student wanted to ask a clarifying question to ensure they understood the assignment's requirements and could provide the correct deliverables.

## 

## **Task 1: HTML File Submission Guidelines**

## The professor clarified the requirements for submitting the FastQC analysis files, correcting the student's initial assumption that a written interpretation of the findings was needed for this part of the assignment. The instruction is to take all the HTML files generated by FastQC from the travel data, compile them into a single zip file, and upload that file to the "My Courses" platform.

## 

## **Task 2: Weekly Report Details and Policies**

## The professor explained that a separate written report was due that morning before the workshop, a deadline the student had missed. However, the professor noted that the student could treat this as a "gimme week," as submissions are not required every single week. For future reports, the content should include one example of a command line used, followed by a prose description of factual observations from the data. This analysis should emphasize quantitative details, such as the number of spots or data ranges, and highlight any interesting or unusual findings.

## The professor referenced the syllabus, explaining the overall course structure for these reports. Of a total of 12 possible weekly reports (including one for project picks and an optional one during spring break), students are required to submit 10\. With 11 weeks remaining, the student needs to complete another nine reports, affording them some flexibility. The professor also recommended submitting assignments before the night they are due.

## 

## **Confirmation of Separate Deliverables**

## The student sought final confirmation, asking if the zip file submission and the written report were separate tasks. The professor affirmed that they are two distinct deliverables to be submitted to two separate assignment boxes on the course platform. The FastQC HTML files could still be submitted, but the weekly written report has a fixed deadline each week before the morning workshop. This clarification resolved the student's misunderstanding.
