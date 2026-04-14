# Mouse alignment prep — team share draft

This file is a **shareable draft**, not the final freeze.

Purpose:
- give the team a concrete proposal for the next alignment-prep decisions
- make it easy to review what is already supported by QC evidence
- keep the official TODO items open until the team agrees

## Documentation links

- Parent process doc: [PROCESS_mouse_fastq_fastqc_fastx.md](PROCESS_mouse_fastq_fastqc_fastx.md)
- Active task tracker: [TODO_mouse.md](TODO_mouse.md)
- Remediation tracker: [TODO_qc_remediation.md](TODO_qc_remediation.md)
- Group project map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)
- Work log: [../WORKLOG.md](../WORKLOG.md)

## 1) Proposed cleaned-input freeze for alignment

### Proposed server root

- `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`

### Proposed naming convention

- mate 1: `SRR*_1.fastp.fastq.gz`
- mate 2: `SRR*_2.fastp.fastq.gz`

### Current evidence

- full chosen-tool rerun completion marker exists:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/full_fastp_all_srrs.completed`
- current file count:
  - `52` cleaned FASTQ files
- first file:
  - `SRR30333743_1.fastp.fastq.gz`
- last file:
  - `SRR30333768_2.fastp.fastq.gz`

### Provisional interpretation

- This path is the cleanest candidate to freeze for STAR because it is:
  - generated from the chosen tool (`fastp`)
  - complete across all `26` SRRs
  - already separated from the older FASTX baseline outputs

### Team decision to confirm

- confirm that STAR should read directly from:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`

## 2) Proposed `cutadapt` fallback decision

### Current evidence

From the full-dataset `FASTX` vs `fastp` comparison:

- `Adapter Content`: `52 fail` under FASTX -> `52 pass` after `fastp`
- `Overrepresented sequences`: `37 pass / 13 warn / 2 fail` under FASTX -> `52 pass` after `fastp`
- no read reports remain in `warn` or `fail` for these two targeted remediation modules after `fastp`

Supporting files:
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_summary.md`
- `qc_analysis_remediation/full_fastx_vs_fastp_full/full_fastx_vs_fastp_status_counts.csv`
- `qc_analysis_remediation/multiqc_fastx_vs_fastp_server/report/mouse_fastx_vs_fastp_all_srrs_multiqc.html`

### Provisional interpretation

- Based on the full-dataset post-`fastp` QC, **no SRR is currently flagged for targeted `cutadapt` fallback**.
- `cutadapt` should remain available only as a contingency if:
  - the team identifies a sample-specific explicit sequence problem
  - a later alignment/QC check reveals a sample that still needs sequence-directed cleanup

### Team decision to confirm

- current draft position:
  - **do not run `cutadapt` on any SRR right now**
  - keep `cutadapt` as a fallback tool, not an active second-pass step

## 3) Why this is still a draft

These two items are evidence-backed, but they are still marked as pending in the TODO until the team reviews them:

- freeze final cleaned FASTQ location + naming convention
- decide whether any SRR still needs targeted `cutadapt`

That is intentional.

## 4) Notebook / evidence references

### Baseline QC notebook

- `/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse.ipynb`

### Remediation + decision notebook

- `/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`

Full-dataset reference section inside the remediation notebook:
- **Step 5C. Bring in the full-dataset validation pass**

## 5) Suggested team-share wording

“During the break, I pushed the pre-alignment QC work forward so we would be ready once everyone is back. I completed the full-dataset FASTX-vs-fastp comparison and drafted two evidence-backed alignment-prep decisions for team review: (1) use `/home/pzg8794/mouse_qc_remediation/output/fastp/out/` as the cleaned-input root for STAR, and (2) do not run a targeted `cutadapt` fallback on any SRR at this point because the full post-fastp QC no longer shows remaining adapter-related file-level failures.” 
