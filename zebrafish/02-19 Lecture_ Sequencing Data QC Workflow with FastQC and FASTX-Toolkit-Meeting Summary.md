## Key Points
---
- Meeting began with setup of breakout rooms; one participant was initially missing but later joined.
- Instructor outlined plan for the session: continue project work, start running FastQC on downloaded FASTQ files, and begin tabulating quality results and identifying consistent issues or problematic files.
- Guidance provided on data cleaning tools:
  - FASTX toolkit (older but widely used) available in /usr/local/bin.
  - Use Trimmomatic to trim low-quality ends or remove noise.
  - Use Clipper to remove adapter/linker sequences.
  - Barcode splitter can separate barcoded samples (though most teams likely don’t have barcoded data).
  - Quality trimmer shortens reads based on quality; quality filter removes whole reads below a threshold.
  - Caution: for paired-end reads, removing one mate can break pairs and affect alignment.
- Workflow emphasized: first run FastQC on downloaded data, then decide cleaning steps based on FastQC reports; always retain original files until cleaning is validated.
- Instructor set expectations for next week’s team reports:
  - Reports will occur on Wednesday.
  - PowerPoint is optional; presentations should be 5–10 minutes per group.
  - Focus: What FastQC shows, anticipated problems, and possible cleanup strategies; peer support encouraged.
- Breakout rooms opened; instructor planned to cycle through to check download status and progress.
- Team discussion highlights:
  - A shared project folder on the server exists (created by the professor).
  - Some reads have been downloaded (about five samples) but not all; there were issues viewing or accessing files and a suggestion to re-download.
  - Team will try running FastQC on currently available data and may use SRA Toolkit (fastq-dump) to pull more reads to the server.
  - Communication and screen-sharing issues occurred; participants experienced audio glitches and web sharing limitations.
## Decisions Made
---
- Proceed with running FastQC on currently available FASTQ files and begin tabulating results.
- Use the server’s shared project folder to centralize data and processing rather than individual local downloads.
- Keep original raw data files preserved while experimenting with cleaning tools.
- Prepare a brief team report for the Wednesday session next week, 5–10 minutes per group.
## Action Items
---
### Tasks
| Task | Responsible Party | Deadline | Notes |
| --- | --- | --- | --- |
| Download remaining reads from selected SRA projects to the server shared folder | Team members using SRA Toolkit | 2026-02-25 | Use SRA Toolkit (e.g., fastq-dump); verify file integrity; re-download problematic files if needed |
| Run FastQC on all currently available FASTQ files | Team members | 2026-02-25 | Tabulate key metrics (per-base quality, adapter content, duplication, overrepresented sequences) |
| Identify consistent issues and problematic files from FastQC reports | Team members | 2026-02-25 | Note samples with low-quality tails, adapters, or other warnings |
| Plan and apply tentative cleaning steps (Trimmomatic, Clipper, FASTX quality filter/trimmer) based on FastQC results | Team members | 2026-02-26 | Preserve originals; be cautious with paired-end data to avoid breaking pairs |
| Prepare team report (5–10 minutes) summarizing FastQC findings and proposed cleanup approach | Team lead (with team input) | 2026-02-25 | PowerPoint optional; include key observations, issues, and planned methods |
| Confirm access and organization of shared server folder for the project | Team members | 2026-02-22 | Verify path and permissions; consolidate data there |
### Deadlines
- 2026-02-22: Confirm shared server folder access and organization.
- 2026-02-25: Complete SRA downloads for selected datasets.
- 2026-02-25: Finish running FastQC and tabulating results.
- 2026-02-25: Prepare 5–10 minute team report for Wednesday.
- 2026-02-26: Begin applying data cleaning steps based on FastQC findings.
### Follow-Up Actions
- Instructor to conduct team report session on 2026-02-25 (Wednesday) with 5–10 minute presentations per group.
- Teams to iteratively refine cleaning strategies and re-run FastQC after trimming/filtering.
- Monitor paired-end integrity after filtering; adjust parameters to maintain mate pairing.
- Resolve any ongoing access or sharing issues on the web conferencing platform to ensure effective collaboration.