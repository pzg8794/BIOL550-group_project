# Project Pipeline Presentation

## Slide 1: Project Overview  
- **Approach:** We spent Week 2–3 learning the NCBI SRA Toolkit (prefetch, fastq-dump, fasterq-dump), FastQC, and FASTX-Toolkit by following the course lab guide.  
- **Manual Testing:** Each member independently tested data download and QC on a few runs to understand the workflow.  
- **Automation Design:** We then designed an **automated pipeline**. We organized shared directories (`sra_runs/`, `fastqc_out/`, `trimmed_out/`), split the 30 SRA runs evenly across the 3 team members, and agreed on a producer-consumer flow: (a) download one run at a time, (b) in parallel run FastQC on the downloaded run, (c) then trim its reads (using FASTX) before moving to the next run.  
- *Speaker notes:* Introduce overall strategy. Explain that learning the tools manually ensured team familiarity. Emphasize the pipelined workflow (download → QC → trim) and even workload split. Mention the shared directory structure and run list split.

## Slide 2: Implementation Details  
- **Data Download:** We use `prefetch` + `fasterq-dump` (from SRA Toolkit v3.0) for speed. Unlike the older `fastq-dump`, `fasterq-dump` uses parallel threads under the hood, so it completes much faster (often ~2–3× quicker)【841†L36-L41】. Each run’s FASTQ goes into `sra_runs/`.  
- **Quality Control:** As soon as a run finishes downloading, a background task runs FastQC on it, outputting to `fastqc_out/`. This overlapping schedule keeps CPUs busy (download/analysis pipelined). FastQC is the standard QC tool for raw reads【841†L36-L41】.  
- **Trimming:** After QC, we trim reads with the FASTX toolkit (e.g. `fastx_trimmer`) to remove low-quality ends. Trimmed reads go to `trimmed_out/`.  
- **Roles:** (Nikhi) wrote the sequential download+FastQC script and managed one queue thread. (Samuel) set up the parallelization logic and monitored his subset of runs. (Piter) created the run ID split lists and integrated each member’s progress.  
- *Speaker notes:* Walk through one example run: discuss the commands (no need to show code). Mention the choice of tools (Cite that FastQC is widely used【841†L36-L41】). Highlight how we achieved concurrency (producer-consumer with background jobs). 

## Slide 3: Results & Next Steps  
- **Progress:** To date we have processed *20 of 30 runs* on the server (66% done), generating 36 FASTQ files and corresponding QC reports. 10 runs remain (work continued after splitting; see [BIOL550-Notes.md](#) for run inventory). We also backed up 13 runs on Drive.  
- **Outcome:** We now have raw reads (and QC reports) for most samples. All trimmed FASTQs are ready for downstream steps (alignment and differential expression).  
- **Next Steps:** Finalize the remaining downloads and trimming. Plan to align reads (e.g. with STAR), then run `cuffdiff` for DE analysis. Prepare next week’s lab report on preliminary QC findings. Each member will write up their 2-minute section (one slide) on these points.  
- *Speaker notes:* Summarize team output (run counts, files generated). Emphasize that the automated pipeline works. Outline what comes next (STAR mapping, DE). Encourage questions about pipeline design or results.

**References:** NCBI SRA Toolkit documentation and FastQC manual were used to choose tools and justify our approach (e.g. [sratoolkit](https://www.ncbi.nlm.nih.gov/sra/docs/sradownload/) for `fasterq-dump` and [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) for read QC). These confirm that our use of `fasterq-dump` and parallel QC is standard practice. (Project notes from our lab repository were also referenced for run lists and status.)