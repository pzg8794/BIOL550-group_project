# BIOL550 Group Project — Work Log (dataset + pipeline)

This log captures **what we did**, **the steps**, and **why** (so we can reproduce work and keep the shared server + repo organized).

## Documentation links

- Parent group-project hub: [README.md](README.md)
- Group project documentation map: [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)
- Agent start guide: [START_HERE_AGENT.md](START_HERE_AGENT.md)
- Server minimum policy: [SERVER_MINIMUM_POLICY.md](SERVER_MINIMUM_POLICY.md)
- Course notes: [../BIOL550-Notes.md](../BIOL550-Notes.md)
- Lab task hub: [../BIOL550-Lab/task_n_desc.md](../BIOL550-Lab/task_n_desc.md)
- Original group project plan: [BIOL550_group_project_outline.md](BIOL550_group_project_outline.md)
- Presentation / research summary: [deep-research-report.md](deep-research-report.md)
- Active mouse workflow: [mouse/PROCESS_mouse_fastq_fastqc_fastx.md](mouse/PROCESS_mouse_fastq_fastqc_fastx.md)
- Active mouse TODO: [mouse/TODO_mouse.md](mouse/TODO_mouse.md)
- Active mouse remediation plan: [mouse/TODO_qc_remediation.md](mouse/TODO_qc_remediation.md)

Use this file as the dated change log. For exact current commands or pending tasks, follow the linked mouse docs.

> Server policy: keep the minimum on `sequoia`; keep most code and analysis local. See [SERVER_MINIMUM_POLICY.md](SERVER_MINIMUM_POLICY.md).

## 2026-04-08 — Materials and Methods LaTeX draft enriched for `mouse_new`

### Step
- Built a standalone LaTeX draft for the `Materials and Methods` section at:
  - `mouse_new/paper/materials_methods_piter_draft.tex`
- Compiled the draft locally to:
  - `mouse_new/paper/materials_methods_piter_draft.pdf`
- Expanded the draft beyond plain prose by adding:
  - a TikZ pipeline figure comparing a generic NGS workflow to the project-specific path
  - a second workflow/design schematic for the post-alignment analysis logic
  - color-coded tables for pipeline stages, sample design, QC transitions, DE filtering, bend-point summaries, enrichment summary, and representative target genes
  - embedded figures pulled from existing local `mouse_new` QC notebook outputs rather than reusing the main biological result panels

### Status
- The draft compiles successfully as a standalone PDF.
- Formatting follows the course paper requirements in the local notes:
  - `12pt`
  - double-spaced
  - `1in` margins
  - Times-like LaTeX font
- The draft is still a working paper section, not the final submission format for Word/LibreOffice.

### Finding
- The current `mouse_new` project tree already contains enough polished local artifacts to make the Methods section more concrete without inventing placeholder results.
- The most reusable visual assets for the Methods section came from:
  - `mouse_new/qc_analysis_raw_vs_trimmed/`
  - `mouse_new/differential_expression_all20/derived_analysis/`
- Transcript guidance was especially useful for structuring the section around:
  - clear subsections
  - PCA-before-interpretation logic
  - bend-point explanation as a data-derived narrowing rule
  - pathways as support after gene identification, not before
- Bioinformatics-journal figure conventions were used as a style cue:
  - Methods figures should behave like workflow/QC support figures, not like duplicated Results figures

### Decision
- Keep this LaTeX draft as the computational-biology source draft for the section.
- Next paper-draft work should focus on:
  - replacing any remaining oversized tables with final journal-style versions if needed
  - deciding which Methods visuals stay in the main paper versus Supplemental
  - porting the approved section back into the required Word/LibreOffice group draft format when the team is ready

## 2026-03-02 — Dataset pivot + cleanup (zebrafish → mouse)

### What changed
- We pivoted away from the zebrafish dataset work area and started a **mouse dataset** run using the same workflow (**download → FastQC (raw) → FASTX trim → FastQC (trimmed) → compare**).

> Tooling note (2026-03-05): if trimming is specifically to remove adapters/known end-sequences, prefer `fastp` over FASTX; for primer/amplicon trimming, use `cutadapt`. See `Semester5/BIOL550/BIOL550-Notes.md` (“fastp vs FASTX Toolkit”) for examples.

- We **archived zebrafish artifacts** locally and on the server into clearly named temp folders so they can be deleted later without hunting.
- We extracted the reusable scripts/notebook into a dataset-agnostic `pipelines/` location (local + server).
- We added an end-to-end runner script to chain the pipeline sequentially when we need to catch up quickly.

### Why
- Avoid mixing outputs across datasets/organisms (prevents confusion and accidental analysis on the wrong files).
- Keep the work resumable and auditable (run lists + logs + consistent directories).
- Make deletion safe later (everything zebrafish goes into one temp folder).

### Local (Mac) actions
1) Created a reusable pipelines directory:
  - `Semester5/BIOL550/group_project/pipelines/` (scripts)
  - `Semester5/BIOL550/group_project/pipelines/notebooks/` (raw vs trimmed notebook template)
2) Created mouse process doc:
   - `Semester5/BIOL550/group_project/mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
3) Archived zebrafish dataset outputs + workspace:
   - Moved into: `Semester5/BIOL550/group_project/_tmp_zebrafish_2026-03-02/`
   - Contents:
     - `qc_bundle/` (raw FastQC bundle)
     - `qc_bundle_trimmed/` (trimmed FastQC bundle)
     - `qc_bundle_non_zebrafish/` (non-project artifacts)
     - `zebrafish/` (old dataset-scoped workspace)

### Server (Sequoia) actions
1) Verified no pipeline processes were running (PID files were stale / processes not running).
2) Kept reusable scripts:
  - `/home/pzg8794/pipelines/`
  - End-to-end runner (local repo): `Semester5/BIOL550/group_project/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh`
3) Archived zebrafish artifacts in home (deletable later):
   - `/home/pzg8794/_tmp_zebrafish_2026-03-02/`
   - Contents:
     - `fastqc_out_trimmed/`
     - `sra_runs_pipeline*/`
     - `zebrafish/` (including the large `tools/` dir)

### Deleting later (when we’re sure)
- Local: `rm -rf Semester5/BIOL550/group_project/_tmp_zebrafish_2026-03-02`
- Server: `rm -rf /home/pzg8794/_tmp_zebrafish_2026-03-02`

---

## 2026-03-02 — Mouse run started (end-to-end)

### Dataset
- BioProject (mouse): `PRJNA1017789` (GEO: `GSE243308`)
- Runs: 26 SRRs (paired-end)

### Run lists
- Local: `Semester5/BIOL550/group_project/mouse/runs/PRJNA1017789_runs.all.txt`
- Server: `/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt`

### Server paths (all outputs under one dataset root)
- `DATA_ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel`
- Raw FASTQs: `/home/zebrafish/mouse/PRJNA1017789_parallel/sra_runs/`
- Raw FastQC: `/home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_out/`
- Trimmed FASTQs: `/home/zebrafish/mouse/PRJNA1017789_parallel/fastx_out/`
- Trimmed FastQC: `/home/zebrafish/mouse/PRJNA1017789_parallel/fastqc_out_trimmed/`
- Logs: `/home/zebrafish/mouse/PRJNA1017789_parallel/.pipeline/`

### Command used (Sequoia)
```bash
ACC=PRJNA1017789
RUNS_FILE=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt
DATA_ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" MEMBER=piter \
  DUMP_THREADS=2 FASTQC_THREADS_RAW=1 FASTQC_THREADS_TRIM=2 TRIM_QUAL=20 MIN_LEN=30 \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh start
```

### Monitor
```bash
tail -f /home/zebrafish/mouse/PRJNA1017789_parallel/.pipeline/end_to_end.nohup.log
tail -f /home/zebrafish/mouse/PRJNA1017789_parallel/.pipeline/raw/download.nohup.log
tail -f /home/zebrafish/mouse/PRJNA1017789_parallel/.pipeline/raw/fastqc.nohup.log
```

### Stop (if needed)
```bash
ACC=PRJNA1017789
RUNS_FILE=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.all.txt
DATA_ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh stop
```

---

## 2026-03-02 → 2026-03-03 — Parallelized mouse run (faster) + baseline merged

### Why
- The server was idle, and the main bottleneck was **compression + per-run sequencing** (one SRR at a time).
- We kept the baseline job running as a safe fallback, then launched a **parallel raw stage** run (multiple SRRs at once). Once the parallel run proved stable, we stopped the baseline to avoid duplicate work.

### What changed (server)
- New parallel scripts were added under:
  - `/home/pzg8794/pipelines/sra_runs_pipeline_sra3_parallel.sh`
  - `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh`
- New (active) dataset root used for the parallel run:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/`

### Local analysis artifacts (Mac)
- Raw FastQC bundle: `Semester5/BIOL550/group_project/mouse/qc_bundle_raw/` (52 ZIP + 52 HTML)
- Trimmed FastQC bundle: `Semester5/BIOL550/group_project/mouse/qc_bundle_trimmed/` (partial until server reaches 26/26)
- Notebook (raw vs trimmed): `Semester5/BIOL550/group_project/mouse/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse.ipynb`
- Notebook outputs: `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/`

### Important note (run list file name)
- The run list file name still says `remaining_no_SRR30333743`, but we re-added SRR30333743 so **trim runs across all 26 SRRs**:
  - `/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.remaining_no_SRR30333743.txt`

### Parallel run command (server)
```bash
ACC=PRJNA1017789
RUNS_FILE=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.remaining_no_SRR30333743.txt
DATA_ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel

ACC="$ACC" RUNS_FILE="$RUNS_FILE" DATA_ROOT="$DATA_ROOT" MEMBER=piter \
  DOWNLOAD_WORKERS=2 FASTQC_WORKERS=2 PIGZ_THREADS=8 \
  DUMP_THREADS=2 FASTQC_THREADS_RAW=2 FASTQC_THREADS_TRIM=2 TRIM_QUAL=20 MIN_LEN=30 \
  /home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh start
```

### Baseline merge step (server)
- We copied SRR30333743 raw FASTQs + raw FastQC outputs into the parallel dataset root (so the parallel root contains the full dataset), then stopped the baseline pipeline.

### Quick status checks (server)
```bash
ROOT=/home/zebrafish/mouse/PRJNA1017789_parallel
RUNS=/home/pzg8794/metadata/PRJNA1017789/splits/PRJNA1017789_runs.remaining_no_SRR30333743.txt

awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/sra_runs/${s}_1.fastq.gz" && -s "$ROOT/sra_runs/${s}_2.fastq.gz" ]] && echo "$s"; done | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/fastqc_out/${s}_1_fastqc.zip" && -s "$ROOT/fastqc_out/${s}_2_fastqc.zip" ]] && echo "$s"; done | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/fastx_out/${s}_1.trim.fastq.gz" && -s "$ROOT/fastx_out/${s}_2.trim.fastq.gz" ]] && echo "$s"; done | wc -l
awk 'NF && $1 !~ /^#/{print $1}' "$RUNS" | while read -r s; do [[ -s "$ROOT/fastqc_out_trimmed/${s}_1.trim_fastqc.zip" && -s "$ROOT/fastqc_out_trimmed/${s}_2.trim_fastqc.zip" ]] && echo "$s"; done | wc -l
```

---

## 2026-03-04 — Mouse run completed + report draft

### Server completion (PRJNA1017789_parallel)
- Confirmed final counts: 26/26 SRRs for raw FASTQs, raw FastQC, trimmed FASTQs, and trimmed FastQC.
- Completion marker present: `/home/zebrafish/mouse/PRJNA1017789_parallel/.pipeline/end_to_end.completed`

### Local (Mac) completion
- Copied the full trimmed FastQC bundle to: `Semester5/BIOL550/group_project/mouse/qc_bundle_trimmed/` (52 ZIP + 52 HTML).
- Re-ran the comparison notebook to refresh plots + CSV exports under: `Semester5/BIOL550/group_project/mouse/qc_analysis_raw_vs_trimmed/`.
- Drafted the mouse weekly report: `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_SRA_FastQC_2026-03-04.html`.

---

## 2026-03-09 — QC remediation plan formalized

### Why
- The baseline QC comparison answered what **FASTX quality trimming** changed, but it also showed that the remaining dominant issues are **technical sequence cleanup** problems, not “more trimming” problems.
- We need a clean exploration phase before alignment so we can learn the available cleanup tools, test them on the right SRRs, and pick the alignment input based on evidence.

### What changed
- Documented a dedicated remediation plan in:
  - `Semester5/BIOL550/group_project/mouse/TODO_qc_remediation.md`
- Added a separate remediation notebook scaffold so the baseline notebook stays focused:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
- Updated the mouse process doc with a remediation section:
  - `Semester5/BIOL550/group_project/mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
- Updated the mouse TODO so the pilot/tool-choice work is tracked explicitly:
  - `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`
- Standardized the active mouse workflow on the single BIOL550 Python environment:
  - `/Users/pitergarcia/DataScience/Semester5/BIOL550/biol550_env`

### Tooling updates
- `qc_remed_fastp_one_srr.sh`
  - default root now points to `/home/zebrafish/mouse/PRJNA1017789_parallel/`
  - adds `--trim_poly_g`
  - uses tail-focused quality trimming to stay closer to the original FASTX intent
- `qc_remed_cutadapt_one_srr.sh`
  - default root now points to `/home/zebrafish/mouse/PRJNA1017789_parallel/`
  - now supports either explicit adapters, `NEXTSEQ_TRIM`, or both

### Planned pilot
- First-pass SRRs:
  - `SRR30333754`
  - `SRR30333756`
  - `SRR30333743`
- First-pass tools:
  - `fastp` for paired-end adapter + poly-G cleanup
  - `cutadapt` for explicit-sequence / `NEXTSEQ_TRIM` comparison

---

## 2026-04-02 — `SRP618841` project reconstruction

### What we did
- Reconstructed the public records and local design details tied to the active `mouse_new` contingency dataset so the team can answer study-design and interpretation questions more directly.
- Cross-checked the local `mouse_new` design table against the public identifiers already recorded in BIOL550 docs.

### Finding
- The active `mouse_new` dataset is the `SRP618841` slice of the public mouse project:
  - SRA study: `SRP618841`
  - GEO series: `GSE243308`
  - BioProject: `PRJNA1017789`
- The local working subset currently used for DE is:
  - `20` runs (`SRR35329977`–`SRR35329996`)
  - one balanced `DRG` family on `NovaSeq X`
  - `Spinal Cord Injury - 1dpi`
  - `10` `ipsi` + `10` `contra`
  - `10` `ff` + `10` `cre`
- The source study/paper context linked to `GSE243308` is the DRG injury/regeneration study:
  - “Aryl hydrocarbon receptor restricts axon regeneration of DRG neurons in response to injury”

### Decision
- Use the public study design to explain what the PCA split means biologically:
  - `ipsi` = injury side
  - `contra` = opposite side
- Use our DE contrasts plus enrichment outputs to explain what likely drives that split:
  - `ipsi_vs_contra_in_ff`
  - `ipsi_vs_contra_in_cre`
- Treat paper-level genes/pathways such as `Ahr`, `Hif1a`, `Arnt`, injury-response signaling, and regeneration programs as contextual anchors that still need to be checked directly against our subset before we claim they are the main drivers in our current analysis.

---

## 2026-04-02 — From PCA separation to driver-gene interpretation

### What we did
- Used the bend-point-selected side-specific gene sets from:
  - `ipsi_vs_contra_in_ff`
  - `ipsi_vs_contra_in_cre`
- Computed their overlap and checked whether the shared genes move in the same direction across both genotype backgrounds.
- Resolved the strongest shared Ensembl gene IDs to gene symbols and wrote a compact interpretation note under the `mouse_new/reference/SRP618841/` bundle.

### Finding
- The two bend-point-selected side-specific sets overlap strongly:
  - `709` genes in `ipsi_vs_contra_in_ff`
  - `870` genes in `ipsi_vs_contra_in_cre`
  - `620` shared genes
- The strongest shared genes are consistently `ipsi_up` in both contrasts.
- The strongest shared genes resolved so far include:
  - `Atf3`
  - `Gadd45a`
  - `Flrt3`
  - `Sox11`
  - `Jun`
  - `Sema6a`
  - `Tubb6`
  - `Gpr151`
  - `Hspb1`
  - `Plin2`
- These genes support a biological reading of the PCA split as injury/stress/regeneration biology on the `ipsi` side rather than a purely geometric separation.

### Decision
- Use the PCA plus the shared side-driver genes together when explaining the data:
  - PCA = shows the dominant injury-side vs opposite-side structure
  - shared side-driver genes = explain what biological programs likely produce that structure
- Keep the new reference artifacts as the local source-of-truth bundle for professor/class questions:
  - `mouse_new/reference/SRP618841/text/pca_gene_interpretation_note_2026-04-02.md`
  - `mouse_new/reference/SRP618841/metadata/shared_side_driver_overlap.tsv`
  - `mouse_new/reference/SRP618841/metadata/top_shared_side_driver_genes.tsv`

---

## 2026-04-02 — Two-hybrid screening reference added

### What we did
- Added `two-hybrid screening` to the `SRP618841` reference bundle as a conceptual biology reference for interaction-oriented interpretation.

### Finding
- This reference is useful when discussing interaction-centered biological hypotheses involving:
  - `Ahr`
  - `Hif1a`
  - `Arnt`
- It helps frame questions about shared partners, regulatory coupling, and pathway crosstalk.

### Decision
- Keep `two-hybrid screening` as a conceptual reference only.
- Do not describe the current RNA-seq dataset as if it were a two-hybrid assay.

---

## 2026-03-17 → 2026-03-18 — STAR alignment launch (private first, shared chained after)

### Why
- The remediation decision is complete enough to start production alignment:
  - `fastp` is the chosen cleanup stage
  - the remaining `Per Sequence GC Content` WARN subset is documented as a cohort/batch-style follow-up, not a blocking adapter problem
- The most efficient execution path is:
  1. build the `GRCm39` + `Ensembl` STAR reference once in the private workspace
  2. launch the full `all 26` alignment there first
  3. chain the same alignment in the shared tree so it starts automatically after the private run finishes

### Reference decision
- Assembly: `GRCm39`
- Annotation source: matching `Ensembl` `GTF`
- Private reference root:
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/`
- Private STAR index:
  - `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/star_index_sjdb150/`

### Private alignment launch
- Input root:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
- Output root:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`
- Scripts added locally:
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_prepare_reference.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_parallel.sh`
- Synced server targets:
  - `/home/pzg8794/mouse_qc_remediation/scripts/`
- Launcher state:
  - PID `71166`
  - log: `/home/pzg8794/mouse_qc_remediation/logs/run_star_all26_fastp_parallel.2026-03-17_233805.log`

### Important correction during launch
- The first private alignment attempt failed at the reference step because `STAR genomeGenerate` does not accept a compressed FASTA.
- The reference-prep script was fixed to unzip the FASTA and GTF before index generation.
- The private launcher was restarted after that correction and the index completed successfully.

### Shared follow-on alignment setup
- Shared input root:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/fastp_out/`
- Shared output root:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_fastp/`
- Shared scripts added locally:
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr_shared.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch_shared.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_shared_after_private.sh`
- Synced shared targets:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/scripts/`
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/runs/`

### Shared-run decision
- We did **not** build a second shared index immediately.
- Instead, the shared launcher waits for the private completion flag:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/all26_fastp_alignment.completed`
- Once that file appears, the shared launcher will:
  - sync the finished private reference/index bundle into the shared tree
  - write shared metadata
  - start the three shared STAR batch jobs

### Shared waiting launcher state
- first shared waiting PID `72403`
- first shared waiting log:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/run_star_all26_fastp_shared_after_private.2026-03-18_020015.log`
- initial handoff issue after the private run completed:
  - the shared launcher failed because `rsync` is not installed on `sequoia`
- correction:
  - patched `mouse_run_star_all26_fastp_shared_after_private.sh` to use `cp -a` when `rsync` is unavailable
  - re-synced the script to the shared tree
  - relaunched the shared handoff
- current shared launcher PID `75809`
- current shared launcher log:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/run_star_all26_fastp_shared_after_private.2026-03-18_095656.log`
- current status from the new log:
  - `Private run completed; syncing shared reference/index`
  - `rsync not found; using cp -a fallback`
- later shared-load adjustment:
  - the shared side was reduced from three concurrent STAR jobs to **serial one-sample-at-a-time** execution
  - shared `STAR_THREADS` was reduced to `1`
  - the shared launcher was restarted after clearing the partial shared alignment state
  - current serial shared launcher PID `77729`
- current serial shared launcher log:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/run_star_all26_fastp_shared_after_private.2026-03-18_110908.log`

### Shared vs private trimmed-output audit
- We copied the private `final_fastp_all_srrs` MultiQC locally so it could be compared directly against the shared trimmed-only MultiQC.
- Audit result:
  - the shared and private trimmed outputs are **not equivalent**
  - they have the same `52` sample set
  - they retain the same broad GC-warning pattern
  - but they differ in sequence counts, sequence-length ranges, `fastp` after-filtering read totals, and one remaining `Overrepresented Sequences` warning on the shared side
- Canonical decision:
  - use the private cleaned-input root for alignment
  - do not treat the shared trimmed output as interchangeable without further validation
- Audit note:
  - `Semester5/BIOL550/group_project/mouse/SHARED_VS_PRIVATE_FASTP_TRIM_AUDIT_2026-03-18.md`

### Supporting notes
- Private launch note:
  - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md`
- Shared follow-on note:
  - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md`
- Canonical shared handoff note:
  - `Semester5/BIOL550/group_project/mouse/CANONICAL_FULL_FASTP_SHARED_HANDOFF_2026-03-18.md`

### Canonical `full_fastp` copied into the shared tree
- We copied the canonical `full_fastp` MultiQC into the shared tree so the team can read the same cleaned-input QC summary that matches the canonical alignment input.
- Shared canonical MultiQC path:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/full_fastp_canonical_privatecopy/`
- We also started copying the completed canonical all-26 alignment into a separate shared-side path so the team can use the same alignment outputs for downstream analysis.
- Shared canonical alignment path:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_full_fastp_canonical_privatecopy/`
- Why the extra copy exists:
  - the earlier shared trimmed-only QC output did not exactly match the canonical private `full_fastp` output
  - a clearly named canonical shared-side copy avoids repeating the same ambiguity during downstream analysis
- Process takeaway:
  - group work still requires independent verification of shared derived outputs before they are treated as canonical

---

## 2026-03-09 → 2026-03-10 — Trusted remediation workspace + pilot comparison setup

### Why
- The shared dataset root is still the correct source for **raw input FASTQs**, but the shared derived outputs are no longer a trustworthy place to run or compare remediation experiments.
- We need one remediation workspace that we control, one frozen baseline copied from the local project, and one repeatable comparison script that can score `raw` vs `FASTX` vs `fastp` vs `cutadapt`.
- The notebook should not be the source of truth for this phase. The source of truth should be terminal-generated artifacts that the notebook can display later.

### What we verified on the server
- Shared raw inputs under `/home/zebrafish/mouse/PRJNA1017789_parallel/` were still intact:
  - `sra_runs/` contained `52` FASTQ files (`26` paired-end SRRs)
  - `fastqc_out/` contained `104` FastQC files (`52` ZIP + `52` HTML)
  - file ownership and dates were consistent with the original run (`pzg8794:zebrafish`, dated `2026-03-02`)
  - the raw sample set and raw FastQC sample set matched exactly
- Shared derived outputs were **not** safe to use as the remediation baseline:
  - `fastp_out/` only contained a manual rerun for `SRR30333743`
  - `fastqc_fastp_trim/` only contained the matching FastQC for that one rerun
  - those files were owned by `nb6672` and dated `2026-03-05`
  - `fastx_out/` and `fastqc_out_trimmed/` were missing from the shared tree at the time of the audit

### Decision
- Keep using `/home/zebrafish/mouse/PRJNA1017789_parallel/` as the **shared raw input source**.
- Do **not** trust shared derived outputs for remediation comparisons.
- Freeze the trusted baseline from the local project and copy it into a home-owned remediation workspace under `/home/pzg8794/`.
- Run remediation experiments and comparisons from that home workspace only.

### Home remediation workspace created
- Root: `/home/pzg8794/mouse_qc_remediation/`
- Baseline copies:
  - `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_raw/`
  - `/home/pzg8794/mouse_qc_remediation/baseline/qc_bundle_trimmed/`
- Support directories:
  - `/home/pzg8794/mouse_qc_remediation/scripts/`
  - `/home/pzg8794/mouse_qc_remediation/logs/`
  - `/home/pzg8794/mouse_qc_remediation/compare/`
  - `/home/pzg8794/mouse_qc_remediation/output/`

### What we copied and checked
- Copied the trusted local FastQC bundles into the home baseline workspace.
- Verified that both baseline bundles contain `104` files each.
- Verified that the three pilot SRRs are present in both baseline stages:
  - `SRR30333754`
  - `SRR30333756`
  - `SRR30333743`

### Comparison tooling added
- New repo script:
  - `Semester5/BIOL550/group_project/pipelines/mouse_qc_strategy_compare.py`
- Server copies:
  - `/home/pzg8794/mouse_qc_remediation/scripts/mouse_qc_strategy_compare.py`
  - `/home/pzg8794/mouse_qc_remediation/scripts/run_compare.sh`
- Purpose:
  - parse FastQC ZIP bundles for `raw`, `FASTX`, `fastp`, and `cutadapt`
  - parse `fastp` JSON and `cutadapt` logs
  - write one comparison package with stage-level metrics, adapter curves, tool metrics, and a readable summary

### Preliminary outputs already generated
- Directory:
  - `/home/pzg8794/mouse_qc_remediation/compare/preliminary/`
- Files:
  - `pilot_read_stage_metrics.csv`
  - `pilot_adapter_curve_data.csv`
  - `pilot_srr_comparison_wide.csv`
  - `pilot_fastp_run_metrics.csv`
  - `pilot_cutadapt_run_metrics.csv`
  - `pilot_summary.md`

### Findings from the preliminary compare (`raw` vs current `FASTX`)
- The current FASTX trim changed read length / tail quality, but it did **not** materially resolve the dominant technical-sequence signal in the pilot runs.
- The main unresolved patterns remained:
  - poly-G dominated read 2 signal in `SRR30333754` and `SRR30333756`
  - explicit TruSeq adapter signal in `SRR30333743_1`
- This confirmed the earlier interpretation: the next step is **targeted technical cleanup**, not more generic quality trimming.

### Pilot remediation runs launched in the home workspace
- Wrapper:
  - `/home/pzg8794/mouse_qc_remediation/scripts/run_pilot_remediation.sh`
- Log:
  - `/home/pzg8794/mouse_qc_remediation/logs/run_pilot_remediation.2026-03-09_232002.log`
- Tool plan inside the wrapper:
  - `fastp` on `SRR30333754`, `SRR30333756`, `SRR30333743`
  - `cutadapt` with `NEXTSEQ_TRIM=20` on the poly-G dominated SRRs
  - `cutadapt` with `NEXTSEQ_TRIM=20` + explicit `ADAPTER_R1` on `SRR30333743`

### Last verified live run state (2026-03-10 00:32 EDT)
- The `fastp` pilot phase completed for all three SRRs:
  - `SRR30333754`
  - `SRR30333756`
  - `SRR30333743`
- Evidence on the server:
  - `3` `fastp` report pairs (`.html` + `.json`)
  - `12` post-`fastp` FastQC artifacts (`6` ZIP + `6` HTML)
  - `6` trimmed `fastp` FASTQ files (`3` paired-end SRRs)
- The pipeline had moved into the `cutadapt` phase:
  - trimming for `SRR30333754` completed and wrote `/home/pzg8794/mouse_qc_remediation/output/cutadapt/reports/SRR30333754.cutadapt.log`
  - `FastQC` was still running on `/home/pzg8794/mouse_qc_remediation/output/cutadapt/out/SRR30333754_1.cutadapt.fastq.gz` and `/home/pzg8794/mouse_qc_remediation/output/cutadapt/out/SRR30333754_2.cutadapt.fastq.gz`
- The final all-stage compare had **not** been generated yet:
  - `/home/pzg8794/mouse_qc_remediation/compare/preliminary/` contained `6` files
  - `/home/pzg8794/mouse_qc_remediation/compare/final/` was still empty

### Documentation decision for this phase
- Server/terminal artifacts are the primary record for remediation.
- Markdown files must record:
  - what was run
  - why it was run
  - what changed
  - what decision followed
- The notebook should only become a presentation layer after the comparison artifacts exist.

---

## 2026-03-10 — Pilot remediation completed + first tool decision

### What changed
- The `cutadapt` pilot phase completed for all three pilot SRRs:
  - `SRR30333754`
  - `SRR30333756`
  - `SRR30333743`
- The final comparison package was generated in:
  - `/home/pzg8794/mouse_qc_remediation/compare/final/`
- Final files produced:
  - `pilot_adapter_curve_data.csv`
  - `pilot_cutadapt_run_metrics.csv`
  - `pilot_fastp_run_metrics.csv`
  - `pilot_read_stage_metrics.csv`
  - `pilot_srr_comparison_wide.csv`
  - `pilot_summary.md`

### Findings
- For the two dominant poly-G read 2 cases, `fastp` clearly outperformed `cutadapt` on residual adapter signal:
  - `SRR30333754_2`
    - current `FASTX` adapter_max `45.0897`
    - `fastp` adapter_max `0.0589`, retained `95.5758%`
    - `cutadapt` adapter_max `45.0601`, retained `97.5000%`
  - `SRR30333756_2`
    - current `FASTX` adapter_max `32.4893`
    - `fastp` adapter_max `0.0434`, retained `95.7836%`
    - `cutadapt` adapter_max `31.8831`, retained `97.7000%`
- For the explicit TruSeq adapter case, both tools removed the dominant overrepresented signal, but `fastp` still drove adapter_max lower:
  - `SRR30333743_1`
    - current `FASTX` adapter_max `49.1768`
    - `fastp` adapter_max `0.0054`, retained `96.7674%`
    - `cutadapt` adapter_max `0.0338`, retained `98.2000%`
- Overall pattern:
  - `cutadapt` preserved slightly more reads
  - `fastp` removed the dominant technical signal much more effectively across the pilot set

### Decision
- Choose `fastp` as the **default batch remediation tool** for the mouse project.
- Keep `cutadapt` as the **targeted explicit-sequence fallback** when a known adapter/primer sequence needs direct control.

### Why this decision is defensible
- The main unresolved dataset-wide problem was poly-G / adapter-like technical signal, especially in read 2.
- `fastp` reduced adapter_max from large baseline values to near zero in all three pilot cases.
- `cutadapt` improved retention, but it did not materially reduce adapter_max in the two poly-G dominated pilot reads.

### Next step
- Copy or sync the final comparison package into the local mouse workspace.
- Update the remediation notebook and weekly report so the final tool comparison is visible outside the server workspace.

### Local sync completed
- Copied the final comparison package from `/home/pzg8794/mouse_qc_remediation/compare/final/` into:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/`
- The local remediation analysis folder now has the server-generated CSV/summary files needed for notebook display and report writing.

### Notebook rebuilt around the actual comparison questions
- Rebuilt:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
- New notebook structure now follows the real decision flow:
  - what problem remained after `FASTX`
  - what each tested solution did (`fastp`, `cutadapt`)
  - how all stages compare on the same page
  - which tool wins and why
- The notebook’s dataset-level signal sections now use **all-SRR GC bell-shape composites**:
  - start from the full `52`-report current `FASTX` bundle
  - materialize a copy for each tool-specific stage
  - replace the `6` pilot report ZIPs in that copy with the corresponding `fastp` or `cutadapt` FastQC ZIPs
  - then render the FastQC `Per sequence GC content` bell shape so the stage view stays dataset-level rather than pilot-only
- Executed the notebook successfully in:
  - `/Users/pitergarcia/DataScience/Semester5/BIOL550/biol550_env`
- New local comparison figures written to:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/final_problem_raw_vs_fastx.png`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/final_fastp_vs_baseline.png`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/final_cutadapt_vs_baseline.png`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/final_all_tools_comparison.png`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/final_fastp_gc_bellshape_all_srrs.png`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/final_cutadapt_gc_bellshape_all_srrs.png`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/final_all_tools_gc_bellshape_all_srrs.png`

---

## 2026-03-11 — Documentation sync for remediation results + current notebook state

### Step
- Reviewed the current local remediation workspace and synchronized the documentation entry points:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/`
  - `Semester5/BIOL550/group_project/mouse/TODO_qc_remediation.md`
  - `Semester5/BIOL550/group_project/mouse/PROCESS_mouse_fastq_fastqc_fastx.md`
  - `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`
  - `Semester5/BIOL550/BIOL550-Notes.md`
  - `Semester5/BIOL550/BIOL550-Lab/task_n_desc.md`

### Finding
- The local remediation workspace now has one clear set of comparison artifacts:
  - notebook: `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
  - summary CSVs: `pilot_srr_comparison_wide.csv`, `pilot_read_stage_metrics.csv`, `pilot_fastp_run_metrics.csv`, `pilot_cutadapt_run_metrics.csv`
  - plots: `final_problem_raw_vs_fastx.png`, `final_fastp_vs_baseline.png`, `final_cutadapt_vs_baseline.png`, `final_all_tools_comparison.png`, and the three `final_*_gc_bellshape_all_srrs.png` figures
- The documented scientific conclusion remains unchanged:
  - use `fastp` as the default remediation tool for the mouse dataset
  - keep `cutadapt` as the targeted fallback when explicit sequence-level trimming control is needed
- The current notebook file should be treated as the authoritative presentation artifact for the remediation comparison; the CSVs and PNGs in `mouse/qc_analysis_remediation/` are the supporting evidence files behind it.

### Decision
- Keep all active BIOL550 mouse docs pointed at the current notebook + remediation analysis folder as the canonical local deliverables.
- Leave the weekly-report update as the last remaining mouse remediation write-up task.

### Added interpretation guidance
- Documented how to read the GC bell-shape plots:
  - shaded band = `25th` to `75th` percentile spread
  - bold line = stage median
  - `Current FASTX` = trimmed baseline
  - the bell plots are a dataset-level sanity check; the final tool choice still comes from the remediation metrics
- Added two notebook-level visual aids:
  - a baseline bell plot for `raw` vs `Current FASTX` trimmed baseline
  - a `2x2` bell-plot gallery so the baseline, `fastp`, `cutadapt`, and all-stage views can be compared on one page

---

## 2026-03-11 — Plotting research for remediation comparisons

### Step
- Reviewed official documentation for MultiQC reports and custom content, the MultiQC FastQC module, seaborn `pointplot` / `lineplot` / `heatmap`, seaborn error-bar guidance, Plotly line / heatmap / box plots, and the `fastp` README:
  - https://docs.seqera.io/multiqc/reports
  - https://docs.seqera.io/multiqc/custom_content
  - https://docs.seqera.io/multiqc/modules/fastqc
  - https://seaborn.pydata.org/generated/seaborn.pointplot.html
  - https://seaborn.pydata.org/generated/seaborn.lineplot.html
  - https://seaborn.pydata.org/generated/seaborn.heatmap.html
  - https://seaborn.pydata.org/tutorial/error_bars.html
  - https://plotly.com/python/line-charts/
  - https://plotly.com/python/heatmaps/
  - https://plotly.com/python/box-plots/
  - https://github.com/OpenGene/fastp

### Finding
- MultiQC is the best single interactive report layer for many-sample QC review and can host remediation summaries through custom content.
- `pointplot`-style comparisons are a better fit than plain bars when the question is category-to-category change.
- `lineplot` with percentile intervals is a good fit for stage-level QC curves because these data are not guaranteed to be symmetric or normal.
- Heatmaps are the most compact way to summarize pass / warn / fail changes across many samples and modules.
- The GC bell plot remains useful, but only as a sanity check; it is not the strongest plot for ranking `FASTX` vs `fastp` vs `cutadapt`.
- MultiQC supports a mouse theoretical GC overlay (`mm10_txome`), which would improve interpretation if we keep the GC panel.
- `fastp` already emits before/after summaries, which makes it easy to support slope, scatter, and summary-table views.

### Decision
- Keep the current bell plots, but do not use them as the primary ranking plot.
- Prioritize delta-vs-`Current FASTX` plots, a retention-vs-cleanup scatter plot, and a sample/module/stage heatmap as the next best explanation layer.
- Preserve this plotting guidance in the mouse process and remediation tracking docs so the rationale survives outside the notebook.

---

## 2026-03-11 — Implemented research-backed decision plots in the notebook

### Step
- Updated the remediation notebook builder to add three decision-focused figures:
  - `final_adapter_delta_vs_fastx.png`
  - `final_retention_vs_adapter_tradeoff.png`
  - `final_status_heatmap_focus_reads.png`
- Rebuilt and executed:
  - `Semester5/BIOL550/group_project/pipelines/build_mouse_qc_remediation_notebook.py`
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`

### Finding
- The notebook now separates the roles of the plots clearly:
  - ranking plots answer whether each tool improves `Current FASTX`
  - tradeoff plot shows cleanup vs retention cost
  - status heatmap shows categorical FastQC state transitions
  - bell plots remain as the final dataset-level sanity check
- This matches what we learned from the documentation review:
  - direct stage-to-stage comparisons should drive the tool decision
  - bell plots should validate that the library shape still looks reasonable

### Decision
- Keep the new decision plots as the primary comparison layer in the notebook.
- Keep the bell plots as validation plots only.
- Leave MultiQC as the final server-side validation report after the workflow is fully frozen.

---

## 2026-03-11 — Server-side MultiQC pilot validation

### Step
- Reconnected to `sequoia` and verified the current remediation workspace:
  - `raw` FastQC zips: `52`
  - `Current FASTX` FastQC zips: `52`
  - `fastp` FastQC zips: `6`
  - `cutadapt` FastQC zips: `6`
- Chose the MultiQC scope based on those counts:
  - pilot comparison report now
  - full chosen-tool report later
- Added two reusable helper scripts locally and copied them to the server:
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_pilot_compare.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_final_fastp.sh`
- Installed MultiQC in the user-local server path because it was not present:
  - `python3 -m pip install --user --break-system-packages multiqc`
- Generated the pilot comparison report on the server with:
  - `/home/pzg8794/mouse_qc_remediation/scripts/mouse_multiqc_pilot_compare.sh`

### Finding
- The immediate apples-to-apples validation report is the pilot comparison report, not separate per-tool reports and not a full-dataset all-tools report.
- MultiQC completed successfully on the server:
  - report: `/home/pzg8794/mouse_qc_remediation/multiqc/pilot_compare/report/mouse_pilot_compare_multiqc.html`
  - data: `/home/pzg8794/mouse_qc_remediation/multiqc/pilot_compare/report/mouse_pilot_compare_multiqc_data/`
- MultiQC found:
  - `cutadapt`: `3` reports
  - `fastp`: `3` reports
  - `fastqc`: `24` reports
- `--dirs --dirs-depth 1` was the correct setting because the same pilot reads appear across multiple stage folders and needed stage-prefixed sample names.

### Decision
- Keep the pilot comparison MultiQC report as the current server-side validation artifact.
- Do not generate separate MultiQC reports per approach as the main deliverable.
- Generate the final full-dataset MultiQC report only after `fastp` is run across all SRRs.

---

## 2026-03-11 — Copied MultiQC locally and cleaned server space

### Step
- Copied the server-side MultiQC pilot validation outputs into the local remediation analysis folder:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_pilot_compare_server/`
- Audited server-side disk usage under `/home/pzg8794/mouse_qc_remediation/`
- Deleted the large pilot-only trimmed FASTQ intermediates:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/*.fastq.gz`
  - `/home/pzg8794/mouse_qc_remediation/output/cutadapt/out/*.fastq.gz`
- Deleted the temporary pip cache:
  - `/home/pzg8794/.cache/pip`

### Finding
- The local copy now contains:
  - `mouse_pilot_compare_multiqc.html`
  - `mouse_pilot_compare_multiqc_data/`
- The large removable space consumers were the pilot trimmed FASTQ outputs:
  - `output/fastp/out/`: about `20G`
  - `output/cutadapt/out/`: about `20G`
- After cleanup, the remaining server footprint is much smaller:
  - `mouse_qc_remediation/output`: about `18M`
  - `mouse_qc_remediation/multiqc`: about `11M`
  - `mouse_qc_remediation/baseline`: about `138M`
- The analysis-critical artifacts were preserved:
  - post-tool FastQC zips
  - `fastp` JSON reports
  - `cutadapt` logs
  - MultiQC report + data

### Decision
- Keep the server workspace lean by removing large intermediate FASTQ outputs once the downstream QC artifacts and summaries are secured.
- Keep the local analysis copy as the easiest place to inspect the MultiQC pilot outputs.

---

## 2026-03-11 — Removed remaining zebra temp workspace from server home

### Step
- Searched `/home/pzg8794` for zebra / zebrafish-named artifacts.
- Deleted the remaining temporary zebra directory:
  - `/home/pzg8794/_tmp_zebrafish_2026-03-02`

### Finding
- No zebra / zebrafish-named paths remain under `/home/pzg8794`.
- The removed directory had been using roughly `744M`.

### Decision
- Treat zebra work as retired from the server home workspace.
- Keep any future one-off analysis code local first, copy it to the server only for execution, and remove the server copy afterward.

---

## 2026-03-11 — Removed long custom code from server home

### Step
- Audited code files under:
  - `/home/pzg8794/mouse_qc_remediation/scripts`
  - `/home/pzg8794/pipelines`
- Applied the current cleanup rule:
  - keep short wrappers on the server
  - remove longer custom code (`>~100` lines)

### Finding
- Remaining server-side code is now short wrapper-level only:
  - `run_compare.sh` (`11` lines)
  - `run_pilot_remediation.sh` (`23` lines)
  - `mouse_multiqc_final_fastp.sh` (`29` lines)
  - `mouse_multiqc_pilot_compare.sh` (`70` lines)
  - `qc_remed_cutadapt_one_srr.sh` (`98` lines)
  - `download_fastq_sratoolkit_from_runs.sh` (`98` lines)
  - `qc_remed_fastp_one_srr.sh` (`99` lines)
- Removed longer code from the server:
  - `/home/pzg8794/mouse_qc_remediation/scripts/mouse_qc_strategy_compare.py`
  - `/home/pzg8794/pipelines/download_fastq_sratoolkit.sh`
  - `/home/pzg8794/pipelines/fastx_trim_fastqc_pipeline.sh`
  - `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc.sh`
  - `/home/pzg8794/pipelines/run_end_to_end_fastq_fastqc_fastx_fastqc_parallel.sh`
  - `/home/pzg8794/pipelines/sra_runs_pipeline_sra3.sh`
  - `/home/pzg8794/pipelines/sra_runs_pipeline_sra3_parallel.sh`
- `/home/pzg8794/pipelines` is now reduced to about `8K`.

### Decision
- Long custom code is now local-first by policy.
- If any removed script needs to run again, copy it from the local repo to the server, execute it, and delete the server copy immediately afterward.

---

## 2026-03-11 — Elevated server-minimum policy into a standalone project rule

### Step
- Added a dedicated policy document:
  - `Semester5/BIOL550/group_project/SERVER_MINIMUM_POLICY.md`
- Linked that policy from the main group-project hub, documentation map, mouse process doc, mouse remediation plan, and the work log header.

### Finding
- The server-residency rule is now explicit instead of scattered:
  - server keeps only the minimum needed to run, inspect, and prove work
  - local repo keeps the notebooks, long scripts, analysis logic, and custom code
  - long code may be copied to the server temporarily, then must be removed after use
- Short wrappers and templates are still allowed to remain on the server.

### Decision
- Treat `SERVER_MINIMUM_POLICY.md` as the authoritative statement for what may remain on `sequoia`.
- Before copying new code to the server, check that file first.

---

## 2026-03-11 — Transcript review for pre-alignment next steps

### Step
- Reviewed the BIOL550 transcript notes relevant to QC cleanup and alignment planning:
  - `Semester5/BIOL550/transcripts/2026-02-18 Lecture_ SRA Toolkit Workflows, FastQC, Server Coordination, and Alignment Deliverables-summary.md`
  - `Semester5/BIOL550/transcripts/2026-02-19 Lecture_ Sequencing Data QC Workflow with FastQC and FASTX-Toolkit-summary.md`
  - `Semester5/BIOL550/transcripts/2026-02-26 Analysis of RNA-Seq Quality Control and Methodology Verification-summary.md`
  - `Semester5/BIOL550/transcripts/2026-03-02 Weekly Meeting_ Bulk RNA-seq Dataset Selection, Access Permissions, and QC (Adapters_Duplication)-summary.md`
  - `Semester5/BIOL550/transcripts/2026-03-04 Lecture_ RNA Sequencing Data Analysis and Quality Control-summary.md`
  - `Semester5/BIOL550/transcripts/2026-03-05 Lecture_ RNA-seq QC, Reference Selection, and Differential Expression Tools-transcript.txt`
- Converted those course-level recommendations into an explicit pre-alignment checklist in the mouse TODO docs.

### Finding
- The transcripts are consistent on the main sequence:
  - if adapter/poly-G signal persists after quality trimming, do targeted cleanup and rerun FastQC
  - do not treat every FastQC FAIL as an automatic blocker
  - capture STAR mapping summaries as part of the alignment QC layer
  - choose the reference genome deliberately, not automatically
- For this mouse project, that means the cleanup phase is **not fully done yet** just because the pilot decision is done.
- The remaining alignment-prep work is:
  - full-dataset `fastp` rerun
  - full cleaned-input FastQC + MultiQC validation
  - reference genome + annotation freeze
  - sample sheet / design matrix freeze
  - STAR run manifest + mapping-summary capture template

### Decision
- Treat the pilot remediation result as the tool-selection milestone, not the end of cleaning.
- Use the updated TODOs as the pre-alignment checklist before the report for tomorrow and before launching STAR.

---

## 2026-03-11 — Launched full-dataset fastp cleanup for alignment prep

### Step
- Started the full chosen-tool cleanup run on `sequoia` to cover the first three pre-alignment items in one sequence:
  - full-dataset `fastp` across all `26` SRRs
  - post-`fastp` FastQC for all cleaned files
  - final chosen-tool MultiQC report after the rerun
- Server wrapper used:
  - `/home/pzg8794/mouse_qc_remediation/scripts/mouse_run_full_fastp_alignment_prep.sh`
- Server log:
  - `/home/pzg8794/mouse_qc_remediation/logs/run_full_fastp_alignment_prep.2026-03-11_032611.log`

### Finding
- The run started successfully under PID `2468090`.
- The log shows the first sample (`SRR30333743`) entering the `fastp` step.
- Output directories were reset before launch so the full rerun will produce a clean full-dataset `fastp` bundle and a clean final chosen-tool MultiQC report.

### Decision
- Leave the wrapper running on the server while the full dataset is processed.
- Treat the three pre-alignment items as **in progress** until the completion marker files appear:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/full_fastp_all_srrs.completed`
  - `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/mouse_fastp_all_srrs_multiqc.completed`

---

## 2026-03-11 — Completed full fastp cleanup validation and added long-code staging helper

### Step
- Verified the full chosen-tool server run completed successfully:
  - full-dataset `fastp` across all `26` SRRs
  - post-`fastp` FastQC for all `52` read files
  - final chosen-tool MultiQC report
- Added a local-only helper for temporary long-code staging:
  - `Semester5/BIOL550/group_project/pipelines/sync_long_code_to_sequoia.sh`

### Finding
- Completion markers now exist:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/full_fastp_all_srrs.completed`
  - `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/mouse_fastp_all_srrs_multiqc.completed`
- Final chosen-tool MultiQC report exists:
  - `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/report/mouse_fastp_all_srrs_multiqc.html`
- The server-side execution phase for the first three pre-alignment tasks is now complete.
- The next useful analysis step is no longer more cleanup execution; it is comparison of the full `fastp` post-QC bundle against the current FASTX baseline.
- The new helper centralizes the approved long-code manifest and supports `list`, `push`, `status`, and `remove`, so we do not need to rewrite copy/delete commands each time.

### Decision
- Treat the full `fastp` rerun as the validated cleaned-input stage for the mouse dataset.
- Keep using `sync_long_code_to_sequoia.sh` whenever long custom code must be staged to `/home/pzg8794`, then remove those copies immediately after use.
- Next: copy the final post-`fastp` QC artifacts locally as needed and write the full-dataset `FASTX` vs `fastp` comparison for the report.

---

## 2026-03-11 — Added future-agent startup protocol

### Step
- Added a scoped agent instruction file for the BIOL550 group-project subtree:
  - `Semester5/BIOL550/group_project/AGENTS.md`
- Added a read-first handoff guide:
  - `Semester5/BIOL550/group_project/START_HERE_AGENT.md`
- Linked the new guide from:
  - `Semester5/BIOL550/group_project/README.md`
  - `Semester5/BIOL550/group_project/DOCUMENTATION_MAP.md`
  - `Semester5/BIOL550/group_project/WORKLOG.md`

### Finding
- Future Codex sessions working anywhere under `Semester5/BIOL550/group_project/` now have an explicit startup order instead of relying on scattered context.
- The startup protocol captures:
  - what to read first
  - the local-vs-server working model
  - the documentation update pattern
  - the current mouse-project state and next-step sequence

### Decision
- Treat `AGENTS.md` plus `START_HERE_AGENT.md` as the standard onboarding path for future sessions.
- Keep those two files updated whenever the project workflow or priorities change.

---

## 2026-03-11 — Generated supplemental FASTX MultiQC reports

### Step
- Added two short local/server MultiQC wrappers:
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_fastx_baseline.sh`
  - `Semester5/BIOL550/group_project/pipelines/mouse_multiqc_fastx_vs_fastp.sh`
- Ran both on `sequoia` inside `/home/pzg8794/mouse_qc_remediation/scripts/`.
- Copied the resulting report folders into the local remediation analysis workspace.

### Finding
- The server now has:
  - FASTX-only full-dataset report:
    - `/home/pzg8794/mouse_qc_remediation/multiqc/fastx_baseline_all_srrs/report/mouse_fastx_baseline_all_srrs_multiqc.html`
  - FASTX-vs-fastp full-dataset comparison report:
    - `/home/pzg8794/mouse_qc_remediation/multiqc/fastx_vs_fastp_all_srrs/report/mouse_fastx_vs_fastp_all_srrs_multiqc.html`
- Local analysis copies now exist:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_baseline_server/`
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastx_vs_fastp_server/`
- These reports are useful supporting evidence because the full `fastp` rerun is now complete across all `26` SRRs.
- They do not replace the notebook/custom comparison workflow; they complement it.

### Decision
- Use the new MultiQC reports as secondary validation for the report discussion:
  - FASTX-only report for baseline context
  - FASTX-vs-fastp report for side-by-side QC review
- Keep the custom comparison tables/plots as the primary basis for the final interpretation.

---

## 2026-03-11 — Standardized reporting language for custom QC workflow vs MultiQC

### Step
- Reused the wording pattern from the earlier weekly report and updated the BIOL550 notes plus mouse workflow docs to describe the QC layers consistently.

### Finding
- The most accurate framing for this project is:
  - the custom workflow reads the underlying FastQC outputs directly and compares them across stages
  - this is effectively an automated file-by-file QC review, matching the professor’s preferred manual inspection logic
  - MultiQC is then used as a supplementary aggregation and confirmation layer
- This wording is stronger than saying only “validate MultiQC,” because it explains that the file-level comparison is the primary evidence and MultiQC is the corroborating summary.

### Decision
- Use the following reporting position going forward:
  - custom comparison workflow = primary validation layer
  - MultiQC = supplementary aggregation / confirmation layer
- Reuse the prior-report language where possible so the report sounds consistent with earlier work.

---

## 2026-03-11 — Completed full-dataset FASTX vs fastp comparison

### Step
- Copied the full post-`fastp` FastQC zip bundle and `fastp` JSON reports locally:
  - `Semester5/BIOL550/group_project/mouse/qc_bundle_fastp_full/`
  - `Semester5/BIOL550/group_project/mouse/fastp_reports_full/`
- Added a local comparison script:
  - `Semester5/BIOL550/group_project/pipelines/mouse_fastx_vs_fastp_full_compare.py`
- Generated the full-dataset comparison outputs:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/full_fastx_vs_fastp_full/`

### Finding
- The comparison covers all `52` read-level FastQC reports (`26` paired-end SRRs).
- Headline full-dataset changes from FASTX -> fastp:
  - `Adapter Content`: `52 fail` -> `52 pass`
  - `Overrepresented sequences`: `37 pass / 13 warn / 2 fail` -> `52 pass`
  - median `adapter_max`: `31.8806` -> `0.0051`
  - median `adapter_max` delta (`fastp - FASTX`): `-31.8737`
  - median retained reads after `fastp`: `97.52%`
  - median post-fastp `Q30` rate: `93.83%`
- No read reports remain in `fail` for `Adapter Content` or `Overrepresented sequences` after the full `fastp` rerun.

### Decision
- Treat the full-dataset `FASTX` vs `fastp` comparison as complete and report-ready.
- Use the generated markdown summary plus the supporting CSVs as the primary evidence for the report section that explains why `fastp` beat the previous FASTX-trimmed baseline.

---

## 2026-03-11 — Added full-dataset comparison references to the remediation notebook

### Step
- Updated the notebook builder:
  - `Semester5/BIOL550/group_project/pipelines/build_mouse_qc_remediation_notebook.py`
- Rebuilt and executed:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`

### Finding
- The notebook now includes **Step 5C. Bring in the full-dataset validation pass**.
- That section points directly to:
  - the full-dataset `FASTX` vs `fastp` summary markdown
  - the full-dataset status-count table
  - the supporting MultiQC FASTX and FASTX-vs-fastp reports
- This closes the gap between the pilot narrative and the full-dataset validation outputs.

### Decision
- Treat the remediation notebook as the complete QC analysis notebook:
  - pilot decision logic
  - full-dataset validation references
  - supporting MultiQC references

---

## 2026-03-11 — Added full-dataset QC plots to Step 5C

### Step
- Updated the remediation notebook builder again so **Step 5C** includes actual full-dataset plots, not just tables and file references.
- Rebuilt and executed:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`

### Finding
- The full-dataset comparison section now includes:
  - `full_fastx_vs_fastp_adapter_comparison.png`
  - `full_fastx_vs_fastp_retention_tradeoff.png`
  - `full_fastx_vs_fastp_status_counts.png`
- Those plots live in:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/full_fastx_vs_fastp_full/`
- This makes the full-dataset section visually parallel to the pilot decision section above it.

### Decision
- Treat Step 5C as the full-dataset visualization layer for the QC notebook, not just a reference block.
- Keep the baseline notebook unchanged; keep the full-dataset comparison visuals in the dedicated QC/remediation notebook.

---

## 2026-03-11 — Drafted team-share version of the next two alignment-prep decisions

### Step
- Confirmed the proposed cleaned-input root on `sequoia`:
  - `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
- Verified:
  - `52` cleaned FASTQ files exist there
  - the full rerun completion marker exists
- Used the full-dataset `FASTX` vs `fastp` comparison to assess whether any SRR still needs targeted `cutadapt`.
- Wrote a shareable draft:
  - `Semester5/BIOL550/group_project/mouse/ALIGNMENT_PREP_TEAM_DRAFT.md`

### Finding
- The proposed cleaned-input root is operationally ready to freeze for STAR.
- The full-dataset comparison shows no remaining `warn`/`fail` rows for:
  - `Adapter Content`
  - `Overrepresented sequences`
- That means there is no current file-level QC evidence that any SRR still needs a targeted `cutadapt` fallback before alignment.

### Decision
- Keep both TODO items open until the team agrees.
- Use `ALIGNMENT_PREP_TEAM_DRAFT.md` as the version to share while the team is still catching up.

---

## 2026-03-11 — Added notebook-ready alignment-prep discussion draft

### Step
- Extended the remediation notebook:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse.ipynb`
- Added **Step 6. Alignment-prep discussion draft** through the local builder:
  - `Semester5/BIOL550/group_project/pipelines/build_mouse_qc_remediation_notebook.py`
- Rebuilt and executed the notebook in:
  - `/Users/pitergarcia/DataScience/Semester5/BIOL550/biol550_env`

### Finding
- The notebook now contains a discussion package for the remaining alignment-prep items that are already supported by QC evidence:
  - proposed cleaned-input root + naming convention
  - evidence that no SRR currently needs targeted `cutadapt`
  - an alignment-manifest preview with SRR + mate paths ready for team metadata fill-in
  - a non-blocking QC table for modules we should monitor rather than keep trying to “fix”
- The truly open items left outside this notebook section are:
  - reference + annotation freeze
  - STAR manifest / QC template finalization after the reference choice

### Decision
- Use **Step 6** as the notebook-ready discussion layer for the team meeting/report.
- Keep the TODO items open until the team confirms the cleaned-input freeze and the no-`cutadapt` position.

---

## 2026-03-11 — Created new weekly report draft for remediation + full fastp validation

### Step
- Created a new HTML weekly report draft:
  - `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`
- Reused the previous report’s structure and formatting model instead of inventing a new layout.
- Kept the report compact by slightly reducing font/table/image sizes and using the full-dataset remediation figures already generated locally.

### Finding
- The new draft now reflects the current project state instead of the older raw-vs-trimmed-only checkpoint:
  - pilot `fastp` vs `cutadapt` decision already made
  - full-dataset `fastp` rerun completed
  - full post-`fastp` FastQC and supplementary MultiQC completed
  - notebook-based alignment-prep discussion items available for team review
- The report uses the same four syllabus-style sections:
  - what I accomplished
  - methods used
  - problems encountered
  - goals for the coming week

### Decision
- Keep the weekly report TODO items open until the user finishes arranging/customizing the final report wording.
- Use the new HTML file as the working draft for tomorrow’s submission/update.

---

## 2026-03-11 — Transcript review for remaining alignment-prep items + report wording correction

### Step
- Reviewed the BIOL550 transcript summaries again, focusing on:
  - `2026-03-04 Lecture_ RNA Sequencing Data Analysis and Quality Control-summary.md`
  - `2026-02-26 Analysis of RNA-Seq Quality Control and Methodology Verification-summary.md`
  - `2026-03-02 Weekly Meeting_ Bulk RNA-seq Dataset Selection, Access Permissions, and QC (Adapters_Duplication)-summary.md`
  - `2026-03-05 Lecture_ RNA-seq QC, Reference Selection, and Differential Expression Tools-transcript.txt`
- Corrected the new weekly report draft so it says the work was done **in communication with the team**, not “in collaboration with the team.”

### Finding
- The remaining transcript-driven action items that still matter are:
  - explicitly capture STAR mapping summary metrics for downstream troubleshooting
  - make the reference choice explicit as a decision between paper replication and the most recent well-annotated strain-appropriate reference
  - if more than one mouse reference is available, compare annotation/completeness rather than picking blindly
  - if alignment underperforms later, revisit QC/sample assignment before assuming more trimming is needed
- The user also clarified the earlier team-agreed pilot direction:
  - focus initially on `SRR30333743`
  - trim the adapter and poly-G signals in the affected forward/reverse reads respectively

### Decision
- Keep those transcript-derived items visible in the active TODO rather than burying them only in notes.
- Keep the report wording precise: “in communication with my team” for this phase.

---

## 2026-03-12 — Finalized weekly report wording/layout for remediation + alignment-prep handoff

### Step
- Finished the working weekly report draft:
  - `Semester5/BIOL550/group_project/mouse/reports/BIOL550_Weekly_Report_Mouse_QC_Remediation_2026-03-11.html`
- Tightened the language section by section so each figure is explicitly tied to the evidence it supports.
- Reworked the report layout so the main comparison figures, methods figure, problems evidence, and goals evidence all follow the same compact left/right pattern.

### Finding
- The report now presents the remediation story in the same order as the actual analysis:
  - full-dataset outcome summary
  - dataset-level stage overview
  - FASTX vs `fastp` comparison
  - why `fastp` is better
  - focused pilot-read closeout
  - methods, problems, and next-step evidence
- The wording is now more concrete:
  - removes repeated planning text from accomplishments
  - ties `Problems encountered` directly to the validation summary image
  - ties `Goals for the coming week` directly to the remaining-post-`fastp` reads image
  - uses the QC comparison language consistently when describing the methods figure

### Decision
- Treat the current HTML as the finalized local draft for submission/review.
- Mark the weekly report TODO items complete and keep the report alongside the supporting notebook/artifacts for reference.

---

## 2026-03-12 — Final documentation sync before commit/push

### Step
- Rechecked the active mouse documentation before the final repo handoff:
  - `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`
  - `Semester5/BIOL550/group_project/mouse/TODO_qc_remediation.md`
  - `Semester5/BIOL550/group_project/WORKLOG.md`
- Updated the remediation tracker so its alignment-prep section matches the completed full-dataset `fastp` validation and the final report state.

### Finding
- The active docs now agree on the current state:
  - cleanup decision is complete (`fastp` won)
  - full-dataset `fastp` validation is complete
  - the remaining work is alignment preparation (`inputs`, `reference`, `design sheet`, `STAR manifest`), not unresolved cleanup work
- The weekly report, remediation notebook, and TODOs now point at the same evidence package.

### Decision
- Commit the documentation/report/notebook state as the current project snapshot.
- Push both the nested `group_project` repo and the parent `BIOL550` repo after the commits complete.

---

## 2026-03-16 — Added team-facing handoff docs and simplified notebook copy

### Step
- Added two team-facing markdown handoff files:
  - `Semester5/BIOL550/group_project/mouse/MOUSE_GROUP_STATUS_FULL.md`
  - `Semester5/BIOL550/group_project/mouse/MOUSE_GROUP_FOLLOW_GUIDE.md`
- Created a simplified notebook copy for team follow-along:
  - `Semester5/BIOL550/group_project/mouse/notebooks/qc_remediation_experiments_mouse_team_follow.ipynb`
- Linked these files from:
  - `Semester5/BIOL550/group_project/README.md`
  - `Semester5/BIOL550/group_project/DOCUMENTATION_MAP.md`
  - `Semester5/BIOL550/group_project/mouse/TODO_mouse.md`

### Finding
- The project now has two different share modes for the team:
  - one complete status snapshot with full paths, evidence files, and current decisions
  - one dummified follow guide that reduces the project to the minimum they need to understand and follow the work
- The team-follow notebook copy gives them a stable notebook entry point without changing the main remediation notebook.

### Decision
- Use `MOUSE_GROUP_STATUS_FULL.md` when someone needs the full project state.
- Use `MOUSE_GROUP_FOLLOW_GUIDE.md` and `qc_remediation_experiments_mouse_team_follow.ipynb` when someone only needs the simplified version.


---

## 2026-03-17 — Shared MultiQC correction, GC WARN metadata check, and alignment recommendation

### Step
- Re-ran the shared MultiQC outputs on `sequoia` as stage-specific reports instead of a combined mixed report:
  - before trimming only
  - after trimming only (`fastp` only)
- Copied the corrected shared trimmed-only report into the local repo:
  - `Semester5/BIOL550/group_project/mouse/qc_analysis_remediation/multiqc_fastp_trim_only_shared/`
- Extracted the post-`fastp` `Per Sequence GC Content` WARN sample list from the trimmed-only MultiQC data bundle.
- Mapped the WARN subset against `GSE243308` / `PRJNA1017789` sample metadata to see whether it corresponded to one biological group.

### Finding
- Correct shared reports now exist at:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/before_trimming_only/mouse_before_trimming_only_multiqc.html`
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/fastp_trim_only/mouse_fastp_trim_only_multiqc.html`
- The post-`fastp` GC status in the trimmed-only report is `27 PASS / 25 WARN / 0 FAIL`.
- The WARN subset clusters mainly in `SRR30333757` through `SRR30333768` plus `SRR30333756_1`.
- Metadata check shows that this WARN subset does not belong to one simple biological condition; it spans control and conditional knockout, and spans multiple DRG sample groups.
- That makes the remaining GC WARN pattern look more like a study-subset / cohort effect than a simple sick-vs-control signal.

### Decision
- Keep the corrected trimmed-only shared MultiQC report as the authoritative post-`fastp` shared report.
- Do not remove samples or trim further based on the GC curve alone.
- Use alignment metrics as the next decision layer by comparing the GC-WARN subset against the GC-PASS subset after STAR.
- Preserve the full conversation outcome in a dedicated note:
  - `Semester5/BIOL550/group_project/mouse/GC_WARN_and_Shared_MultiQC_Followup_2026-03-17.md`

---

## 2026-03-17 — STAR alignment bootstrap on local server

### Step
- Converted the alignment discussion into explicit pre-run decisions:
  - `GRCm39` + matching `Ensembl` `GTF`
  - cleaned input root = `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`
  - shared STAR index under `/home/pzg8794/mouse_qc_remediation/reference/grcm39_ensembl/star_index_sjdb150/`
  - first-pass run scope = all `26` SRRs
- Added server-oriented STAR scripts to the repo:
  - `pipelines/mouse_star_prepare_reference.sh`
  - `pipelines/mouse_star_align_one_srr.sh`
  - `pipelines/mouse_star_align_batch.sh`
  - `pipelines/mouse_run_star_all26_fastp_parallel.sh`
- Added a dedicated note that explains how the project moved from QC remediation into alignment launch:
  - `mouse/ALIGNMENT_LOCAL_SERVER_START_2026-03-17.md`

### Finding
- The project now has a concrete alignment bootstrap path that stays consistent with the earlier remediation decisions and with the “document every major action” rule.
- The safest first-pass alignment scope is all `26`, because downstream subsetting can still happen after alignment without forcing a second mapping run.
- The resolved Ensembl files at launch were:
  - `Mus_musculus.GRCm39.dna.primary_assembly.fa.gz`
  - `Mus_musculus.GRCm39.115.gtf.gz`
- The local server-side launcher was started with log:
  - `/home/pzg8794/mouse_qc_remediation/logs/run_star_all26_fastp_parallel.2026-03-17_233805.log`
- Alignment output root:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`
- The first launch attempt failed quickly because STAR requires an uncompressed FASTA for `genomeGenerate`.
- The reference-prep script was corrected, re-synced to `sequoia`, and the launcher was restarted.

### Decision
- Monitor the STAR index build first, then the three parallel batch logs.
- Use this all-26 run as the base alignment layer; defer any subsetting decision until the alignment metrics are available.

## 2026-03-18 — Peer review version cleanup and internal reasoning capture
- **step** — Archived superseded peer-review HTML drafts into `_delete_temp_peer_review_versions_2026-03-18/` and renamed the selected version to `Peer_Review_BIOL550_Final.html`.
- **status** — One final active peer-review HTML remains at top level; prior drafts are retained in a local archive folder.
- **finding** — The strongest version balanced candid peer evaluation with explicit acknowledgment that process and environment also shaped the group outcome.
- **decision** — Keep `Peer_Review_BIOL550_Final.html` as the active submission file and store personal score/reasoning context only in `PEER_REVIEW_INTERNAL_REASONING_2026-03-18.md`.

## 2026-03-19 — Mouse alignment notebook, STAR summary exports, and local BAM sync start

### Step
- Created a new alignment-stage notebook under:
  - `Semester5/BIOL550/group_project/mouse/notebooks/mouse_alignment_analysis_star_all26.ipynb`
- Executed the notebook in the shared BIOL550 environment so it parsed the local canonical STAR outputs and wrote figures/tables into:
  - `Semester5/BIOL550/group_project/mouse/alignment_analysis_star_all26/`
- Built a sample-level summary by merging:
  - STAR `Log.final.out` metrics
  - STAR `ReadsPerGene.out.tab` special rows
  - SRA run metadata
  - GEO sample metadata
  - post-`fastp` GC-WARN / GC-PASS labels
- Started the local BAM/BAM-index sync from:
  - `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`
  - into:
  - `Semester5/BIOL550/group_project/mouse/alignment_local_server_private_copy/star_grcm39_ensembl_all26_fastp/`

### Finding
- All `26/26` STAR `Log.final.out` files and `26/26` `ReadsPerGene.out.tab` files were already present locally, so the alignment notebook could run immediately even before the BAM sync finished.
- The notebook exported:
  - `mouse_alignment_sample_summary.tsv`
  - `mouse_star_gene_counts_reverse_stranded.tsv`
  - `star_log_alignment_metrics.tsv`
  - `alignment_metric_by_platform_median.tsv`
  - `alignment_metric_by_gc_status_median.tsv`
  - five report-ready figures under `mouse/alignment_analysis_star_all26/figures/`
- First-pass alignment interpretation from the notebook:
  - median unique mapping is approximately `94%`
  - `NovaSeq X` vs `NovaSeq 6000` differences are visible but not catastrophic
  - `GC-WARN` samples show lower median unique mapping and higher multi-mapping than `GC-PASS`, but they do not collapse as a failed subset
- The BAM transfer is much larger than the log/count bundle; the sync has started and is verified progressing locally, but it remains separate from the completed log/count notebook analysis.

### Decision
- Use the new notebook + `alignment_analysis_star_all26/` outputs as the current alignment-stage evidence package for the mouse project.
- Proceed with the full dataset into the next count/report phase while carrying `platform` and `GC status` as explicit metadata labels.
- Use the reverse-stranded STAR count matrix as the next handoff artifact for the individual report and later DE-focused notebook work.

## 2026-03-19 — Mouse DESeq2 notebook, family manifests, and contrast export package

### Step
- Added a dedicated DESeq2 driver script:
  - `pipelines/mouse_deseq2_all26.R`
- Created and executed the mouse DE notebook:
  - `mouse/notebooks/mouse_differential_expression_all26.ipynb`
- Built the DE design table from:
  - `mouse/alignment_analysis_star_all26/tables/mouse_star_gene_counts_reverse_stranded.tsv`
  - `mouse/alignment_analysis_star_all26/tables/mouse_alignment_sample_summary.tsv`
- Split the downstream analysis into three valid model families and exported all interpretable contrasts into:
  - `mouse/differential_expression_all26/`

### Finding
- The count matrix and alignment sample summary matched cleanly across all `26` samples, so no manual sample exclusion was required for the first-pass DE workflow.
- The family manifest confirms three valid DE families:
  - tissue / `NovaSeq 6000` / naive vs injury = `12` samples
  - tissue / `NovaSeq X` / sham side = `8` samples
  - neurons / `NovaSeq X` = `6` samples
- The DE package now includes:
  - `mouse_de_design_table.tsv`
  - `family_manifest.tsv`
  - `contrast_manifest.tsv`
  - family-level PCA / dispersion / sample-distance figures
  - per-contrast full tables, significant tables, top-gene tables, MA plots, volcano plots, and heatmaps
- First-pass contrast summary:
  - `injury_in_control` = `4667` significant genes
  - `injury_in_cko` = `4088` significant genes
  - `geno_in_ipsilateral_sham` = `144`
  - `ipsilateral_vs_contralateral_in_cko` = `131`
  - `geno_in_neurons` = `139`
  - tissue genotype effects in the `NovaSeq 6000` family remained small (`2` significant genes in naive; `2` in injury)

### Decision
- Keep the family-specific DESeq2 approach as the default downstream model strategy.
- Do not fit a single global DE model across tissue, neurons, and both platforms because the design is structurally confounded.
- Use the tissue injury contrasts as the main report candidate set, with sham-side and neuron genotype contrasts kept as secondary report-ready results.
- Treat `mouse/notebooks/mouse_differential_expression_all26.ipynb` plus `mouse/differential_expression_all26/` as the current DE evidence package for the mouse project.

## 2026-03-19 — Alignment-first weekly report draft built from the local STAR notebook

### Step
- Drafted the new mouse weekly report as an alignment-first report:
  - `mouse/reports/BIOL550_Weekly_Report_Mouse_Alignment_Validation_2026-03-19.html`
- Rendered the matching PDF:
  - `mouse/reports/BIOL550 Weekly Report — Mouse Alignment Validation + Local Reproducible Analysis.pdf`
- Added a short internal note documenting the report angle, included figures, excluded figures, and core claim:
  - `mouse/reports/_INTERNAL_ALIGNMENT_WEEKLY_REPORT_NOTE_2026-03-19.md`

### Finding
- The report now uses the alignment notebook as the main analytical source of truth rather than treating local environment setup as the main accomplishment.
- The figure set is smaller and more readable than the prior QC-remediation report:
  - per-sample unique mapping
  - platform comparison
  - GC-status comparison
  - assignment-burden comparison
  - one compact summary table
- The recent transcript discussion about GC bimodality and sequencing-instrument effects is folded into the report narrative, and the alignment notebook supports that explanation:
  - the GC-WARN subset aligns somewhat worse
  - the older platform also aligns somewhat worse
  - neither subset behaves like a failed-sample cluster

### Decision
- Keep this report aligned to the technical readiness question:
  - is the full dataset strong enough to proceed beyond alignment?
- Use the weekly report to bridge from alignment validation into the DE notebook rather than returning to a cleanup-heavy narrative.

## 2026-03-19 — Shared non-canonical STAR alignment stopped and archived

### Step
- Checked the active server-side shared alignment processes under:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_fastp/`
- Stopped the shared-side STAR launcher, batch, per-sample wrapper, and active STAR subprocesses on `sequoia`.
- Moved the local copy of the shared-side alignment tree out of the active local alignment area into:
  - `mouse/_delete_temp_bad_shared_alignment_2026-03-19/`
- Added an archive note:
  - `mouse/_delete_temp_bad_shared_alignment_2026-03-19/README.txt`

### Finding
- The shared-side alignment was still running even though the shared `fastp_out` tree had already been documented as non-equivalent to the private canonical validated `fastp` output.
- Leaving that run active would keep consuming server resources for a non-canonical output set and increase the chance of later confusion about which alignment should be used downstream.

### Decision
- Stop using the shared-side STAR run as an active workflow.
- Preserve the local copy only as retained evidence.
- Keep the private validated `fastp` alignment as the sole canonical source for notebook analysis, reports, and downstream DE modeling.

## 2026-03-20 — Shared-tree team DESeq2 environment created on sequoia

### Step
- Created a shared-tree team micromamba environment on `sequoia`:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/.local/share/micromamba/envs/biol550_deseq2`
- Installed:
  - `R 4.3.3`
  - `DESeq2`
  - `BiocManager`
  - supporting plotting / CLI packages needed by the existing DE driver
- Added a short shared-server wrapper locally:
  - `pipelines/mouse_deseq2_shared_server_run.sh`
- Added a detailed internal setup note:
  - `mouse/DESEQ2_SHARED_SERVER_SETUP_2026-03-20.md`
- Added a simplified teammate guide in the share repo:
  - `mouse_group_project_work/docs/DESEQ2_SHARED_TEAM_GUIDE.md`

### Finding
- The server’s current `/usr/local/bin/R` was not usable because it failed at runtime with:
  - missing `libreadline.so.7`
- That made a direct install into the current server R stack the wrong fix.
- A self-contained shared-tree micromamba environment fixed the runtime problem without changing the server’s existing/global setup.
- Reusing the private home-directory environment as the team-facing runtime was rejected because teammates should not depend on `/home/pzg8794/.local/...`.
- Copying an already-built micromamba environment tree was also rejected as the final fix because these environments can be prefix-bound; the safer fix was to create the environment directly at the final shared path.
- One package-name issue also surfaced during setup:
  - `bioconductor-biocmanager` did not resolve in the chosen channels
  - `r-biocmanager` was the correct package name

### Decision
- Keep the DESeq2 runtime private to `/home/pzg8794` and use it as the team environment.
- Keep the long DESeq2 driver local as canonical code.
- Keep only the short wrapper and shared input/output artifacts in the team-facing shared directory on the server.

## 2026-04-02 — Transcript-driven `mouse_new` DE expansion for weekly-report story selection

### Step
- Read the `2026-03-31` and `2026-04-01` BIOL550 transcript notes and translated that guidance into a deeper local-only `mouse_new` DE follow-up pass.
- Added a reusable local analysis script:
  - `mouse_new/scripts/derive_de_analysis_all20.py`
- Generated a structured derived-analysis output tree under:
  - `mouse_new/differential_expression_all20/derived_analysis/`
- Extended the canonical local DE notebook:
  - `mouse_new/notebooks/mouse_differential_expression_all20.ipynb`
- Re-executed the canonical notebook after the new sections were added so the notebook remains the single valid local notebook for this dataset.

### Finding
- The transcript guidance pushed the notebook toward a stronger interpretation order:
  - interpret PCA first
  - keep the side-specific DRG contrasts as the main story
  - avoid arbitrary top-`100` style narrowing when the significant sets are very large
- The new derived-analysis tree now includes:
  - ordered-`pvalue` / cumulative curves for `ipsi_vs_contra_in_ff` and `ipsi_vs_contra_in_cre`
  - bend-point summary tables and selected-gene manifests for those two main contrasts
  - genotype comparison summaries for `geno_in_contra` vs `geno_in_ipsi`
  - top-gene tables by `padj` and absolute `log2FoldChange`
  - GO/pathway enrichment result tables and top-term plots for the selected main and secondary contrast sets
- Main counts from this pass:
  - `ipsi_vs_contra_in_ff`: `7023` significant genes, bend-point-selected set = `709`
  - `ipsi_vs_contra_in_cre`: `7541` significant genes, bend-point-selected set = `870`
  - `geno_in_contra`: `891` significant genes
  - `geno_in_ipsi`: `2` significant genes
- The enrichment outputs now give several candidate biological themes we can compare before choosing the next weekly report angle.

### Decision
- Keep `mouse_new/notebooks/mouse_differential_expression_all20.ipynb` as the canonical local notebook for this dataset.
- Keep the new transcript-driven outputs local under `mouse_new/differential_expression_all20/derived_analysis/`.
- Use this expanded analysis pass to choose the strongest next weekly-report story rather than treating every derived result as automatically report-ready.
- Continue treating the two side-specific contrasts as the main story and `geno_in_contra` as the strongest secondary genotype branch.

## 2026-04-02 — Bend-point extension to genotype + interaction and report addendum

### Step
- Expanded `mouse_new/scripts/derive_de_analysis_all20.py` so bend-point outputs are now generated for every exported contrast, including:
  - `geno_in_contra`
  - `geno_in_ipsi`
  - `interaction`
- Re-ran the derived-analysis script to regenerate:
  - `mouse_new/differential_expression_all20/derived_analysis/analysis_summary.tsv`
  - contrast-specific bend-point tables, selected-gene manifests, and enrichment outputs
- Extended the canonical local notebook with transcript-driven planning notes, method notes, artifact indexing, risk checks, and a weekly-report takeaway section.
- Added a transcript-driven method addendum to:
  - `mouse_new/reports/BIOL550_Weekly_Report_Mouse_Differential_Expression_2026-03-25.html`

### Finding
- The bend-point logic now applies consistently across the full contrast set instead of only the two side-specific contrasts.
- Updated bend-point-selected counts are now available for the secondary branches:
  - `geno_in_contra` = `267`
  - `geno_in_ipsi` = `113`
  - `interaction` = `1823`
- This makes the genotype and interaction branches easier to compare, but it also makes the caution point clearer: a large bend-point-selected set does not automatically make a branch report-ready if the strict padj-significant core is still small.

### Decision
- Keep the side-specific DRG contrasts as the recommended lead story for the next weekly report.
- Keep `geno_in_contra` as the strongest secondary genotype branch.
- Treat `geno_in_ipsi` and `interaction` as exploratory until their bend-point-selected outputs hold up under stricter plot and enrichment sanity checks.

## 2026-04-02 — Informative plot upgrade for DE interpretation

### Step
- Extended the local `mouse_new` DE follow-up script to generate more interpretable plots under `mouse_new/differential_expression_all20/derived_analysis/`.
- Added:
  - annotated PCA with side color and genotype shape
  - PCA `ff` / `cre` collision summary table
  - before/after bend-point comparison plots for each contrast
  - genotype side-by-side volcanoes and log2 fold-change density plots
- Updated and re-executed the canonical notebook so those plots now appear with supporting markdown.

### Finding
- The new visuals make two key points much clearer:
  - genotype is weaker than the main side-specific signal, but not zero
  - some `ff` and `cre` samples occupy nearby PCA space, which supports treating genotype as secondary to side rather than as the dominant structure

### Decision
- Use the new before/after and comparison plots as the default interpretation layer when deciding which contrast should lead the next weekly report.

## 2026-04-02 — Standalone plus comparison volcano layout cleanup

### Step
- Updated `mouse_new/scripts/derive_de_analysis_all20.py` so each contrast now writes both:
  - a standalone volcano-plus-count view
  - a separate before/after bend-point comparison grid
- Re-generated the derived-analysis artifacts for:
  - `ipsi_vs_contra_in_ff`
  - `ipsi_vs_contra_in_cre`
  - `geno_in_contra`
  - `geno_in_ipsi`
  - `interaction`
- Re-executed the canonical notebook to keep the standalone sections and the comparison sections together with matching markdown.

### Finding
- The notebook now shows the raw contrast view and the threshold-comparison view as separate layers instead of forcing them into one role.
- This makes it easier to read each contrast on its own and then see how bend-point filtering changes the interpretation.

### Decision
- Keep both plot types in the notebook:
  - standalone for the result itself
  - combined before/after for threshold explanation
- Use the combined comparison figure only as an added explanatory layer, not as a replacement for the standalone section.

## 2026-04-02 — Enrichment companion plot expansion

### Step
- Extended the enrichment output step in `mouse_new/scripts/derive_de_analysis_all20.py` to generate extra companion views for each contrast:
  - ranked top-term summary
  - term-strength plus overlap-coverage panel
  - source-level enrichment summary
- Re-generated the enrichment artifacts under `mouse_new/differential_expression_all20/derived_analysis/`.
- Updated and re-executed the canonical notebook so the enrichment section now shows multiple companion views instead of only one summary plot.

### Finding
- The top-term bar plot is useful for ranking, but it does not explain term coverage or whether the story is carried mostly by `GO:BP`, `KEGG`, or `REAC`.
- The new companion views make it easier to compare:
  - which terms are strongest
  - how much of the selected gene set they actually cover
  - how the signal is distributed across enrichment sources

### Decision
- Keep the original top-term plot as the quick summary.
- Use the new companion views next to it when deciding which enrichment figure best explains the biology for the weekly report.

## 2026-04-02 — `mouse_new` DE weekly report rewrite

### Step
- Rewrote `mouse_new/reports/BIOL550_Weekly_Report_Mouse_Differential_Expression_2026-03-25.html` as a transcript-guided follow-up report for `SRP618841`.
- Replaced the older `all26` / family-package framing with the current `mouse_new` interpretation path.
- Rebuilt the report narrative around:
  - PCA-first interpretation,
  - side-specific DRG contrasts as the main story,
  - bend-point narrowing,
  - `geno_in_contra` as the main supporting genotype branch,
  - and the link from this weekly report into Draft 1 planning.

### Finding
- The updated report now matches the current notebook and derived-analysis outputs instead of the retired package-first framing.
- The report also reflects this week’s class feedback more directly by explaining what the data tells us, how thresholds shape the interpretation, and why the main story is side-specific rather than genotype-led.

### Decision
- Keep the `mouse_new` weekly report as the active DE follow-up document for the contingency dataset.
- Use this report as the bridge between the current DE interpretation work and the Draft 1 paper story.

## 2026-04-02 — Apr 2 DE report cleanup

### Step
- Revised the Apr 2 `mouse_new` follow-up report so it behaves like a true continuation of the earlier report instead of repeating the old summary structure.
- Removed the repeated high-level results table from the Apr 2 report and rewrote that section as a “what changed in our reading of the data” interpretation section.

### Finding
- The follow-up report reads more cleanly when it focuses on the delta from last week:
  - what class feedback changed,
  - what the plots now make clearer,
  - and what that means for the paper story.

### Decision
- Keep the Mar 25 report as the baseline DE package report.
- Keep the Apr 2 report as the interpretation-focused follow-up, not as a second version of the same summary table.

## 2026-04-02 — Apr 2 report visual simplification

### Step
- Simplified the Apr 2 follow-up report layout to remove repeated side-by-side figure pairs that were not adding interpretation value.
- Kept one purposeful figure per section:
  - PCA structure
  - main side-specific before/after contrast
  - secondary `geno_in_contra` before/after contrast
  - enrichment terms-plus-overlap companion view

### Finding
- The follow-up report is easier to scan when each section uses a single, decision-focused figure rather than duplicated paired image blocks.

### Decision
- Keep the Apr 2 report in this single-figure-per-section format unless a specific side-by-side comparison is explicitly needed for interpretation.

## 2026-04-02 — Apr 2 report compact multi-plot revision

### Step
- Reworked the Apr 2 report figure layout again to avoid oversized single panels.
- Added compact multi-plot blocks per section so each section now shows more informative context at smaller size:
  - main side-specific section now includes before/after, ordered-curve, and standalone volcano/count views
  - genotype section now includes before/after plus genotype comparison and zoom views
  - enrichment section now includes overlap, top-terms, and source-summary views

### Finding
- Smaller, multi-plot blocks improve readability and reduce the “one huge plot says too little” problem.

### Decision
- Keep compact multi-plot blocks as the default report style for this follow-up report.

## 2026-04-02 — Apr 2 PCA clarity fix

### Step
- Revised the PCA section in the Apr 2 report to directly address the `ff`/`cre` overlap concern.
- Reduced PCA image size and added a compact table of closest cross-genotype sample pairs from the collision summary output.

### Finding
- The PCA section now shows explicit evidence for why genotype is treated as secondary in this dataset instead of only describing it in prose.

### Decision
- Keep the PCA evidence block (plot + compact collision table) as the default format for this report.

## 2026-04-08 — Materials and Methods draft rebuilt as staged bioinformatics pipeline

### Step
- Rebuilt `mouse_new/paper/materials_methods_piter_draft.tex` around four explicit pipeline stages:
  - Data Collection
  - Data Cleaning
  - Data Preparation
  - Data Mining and Interpretation
- Replaced the earlier crowded mixed-layout Methods draft with four stage-oriented figures and four stage-summary tables.
- Kept Methods visuals workflow-focused and preprocessing-focused, while leaving PCA/volcano/heatmap-style biological result figures for later sections.
- Recompiled the LaTeX draft and refreshed `materials_methods_piter_draft.pdf`.

### Finding
- The staged pipeline framing produces a cleaner, more paper-like Methods section than the earlier draft because figures now explain stage flow and tables carry stage outputs and metrics.

### Decision
- Keep this paper-style rule for the Methods section:
  - figures document stage workflow
  - tables summarize stage outputs/artifacts
  - result-heavy analytical plots stay out of Methods unless explicitly needed.

## 2026-04-08 — Methods visuals rebuilt from real stage artifacts

### Step
- Added new stage-specific Methods figures under `mouse_new/paper/assets_methods/` using project-derived artifacts and summaries:
  - `data_collection_stage.png`
  - `data_cleaning_stage.png`
  - `data_preparation_stage.png`
  - `data_mining_stage.png`
- Replaced the generic Data Collection, Data Preparation, and Data Mining placeholder diagrams in `mouse_new/paper/materials_methods_piter_draft.tex` with artifact-based visuals.
- Upgraded the Data Cleaning figure from a single QC heatmap to a composite built from retained QC and MultiQC outputs.
- Recompiled the Methods draft PDF after the figure replacement.

### Finding
- The Methods section reads more like a project-backed paper workflow when each stage is represented by a real or reconstructed project artifact instead of repeated generic TikZ diagrams.

### Decision
- Continue using artifact-backed stage visuals for Methods whenever a real project output exists; only use abstract schematics for the one high-level orienting pipeline figure.

## 2026-04-08 — Methods draft upgraded with stage-owned assets and checkpoint tables

### Step
- Added `mouse_new/paper/build_methods_assets.py` to reproducibly rebuild the Methods-stage figures from saved project artifacts and summary tables.
- Reworked `mouse_new/paper/materials_methods_piter_draft.tex` again so the section now opens with:
  - one overview ribbon figure
  - one compact pipeline checkpoint table
  - four stage figures
  - four stage tables
- Tightened the table language so the weekly-report style carries over into the paper draft:
  - shorter checkpoint phrases
  - stage-colored labels and metric cells
  - denser but less squeezed handoff summaries
- Regenerated the stage figures and recompiled `mouse_new/paper/materials_methods_piter_draft.pdf`.

### Finding
- The section looks stronger when the Methods figures are owned by real pipeline evidence and the tables act like compact checkpoint summaries instead of narrative paragraphs forced into columns.
- The biggest layout improvement came from treating the pipeline checkpoint table as a short evidence matrix and keeping the stage figures focused on one real retained artifact set per stage.

### Decision
- Keep `build_methods_assets.py` as the canonical way to regenerate the Methods figures.
- Keep the paper draft aligned to this rule:
  - overview figure first
  - compact checkpoint table second
  - one evidence-driven figure plus one dense summary table per stage.

## 2026-04-08 — Data Mining stage strengthened in the Methods draft

### Step
- Extended the Methods-stage asset builder to create an additional Data Mining figure:
  - `mouse_new/paper/assets_methods/data_mining_selection_stage.png`
- Used the saved ordered-\(p\)-value / cumulative bend-point artifacts from the two primary side-specific branches as retained workflow evidence.
- Added that second Data Mining figure to `mouse_new/paper/materials_methods_piter_draft.tex` and added a compact branch-summary table for the `ff` and `cre` side-specific follow-up sets.
- Recompiled `materials_methods_piter_draft.pdf` and visually checked the final Data Mining pages.

### Finding
- The Data Mining section reads more like the earlier stages when it has both:
  - a stage-level summary figure, and
  - a retained bend-point checkpoint figure plus a compact primary-branch summary table.

### Decision
- Keep the Data Mining stage in this two-figure format:
  - one figure for overall modeling/enrichment outputs
  - one figure for the bend-point narrowing checkpoint
  - plus a compact branch-summary table for the two primary side-specific contrasts.

## 2026-04-08 — Shared bend-point tool moved into the repo pipelines folder

### Step
- Moved the standalone bend-point CLI into the shared repo tool location:
  - `pipelines/mouse_bendpoint_from_table.py`
- Added a very simple team-facing guide at:
  - `mouse/BENDPOINT_TOOL_SIMPLE_GUIDE.md`
- Recorded the method provenance in the bend-point guides:
  - the standalone Python tool is a project-specific implementation of a standard elbow/knee heuristic
  - closest documented R reference used for writeup alignment: `LOMAR::find_elbow`
- Validated the shared command from the group-project repo root against:
  - `mouse_new/differential_expression_all20/family_drg_novaseqx/tables/ipsi_vs_contra_in_ff_full.tsv`
- Wrote the example outputs to:
  - `mouse_new/differential_expression_all20/shared_bendpoint_runs/ipsi_vs_contra_in_ff`

### Finding
- The bend-point logic is simple enough to share as one standalone script as long as teammates are pointed to the `*_full.tsv` DE tables and given the exact repo-root command.
- Keeping the tool in `pipelines/` makes it easier to share than leaving it buried under the `mouse_new/scripts/` analysis subtree.
- The provenance note matters because the tool was custom-coded by us, but the underlying method is not ad hoc; it matches a standard elbow/knee-style maximum-distance-to-line approach.

### Decision
- Treat `pipelines/mouse_bendpoint_from_table.py` as the canonical shared bend-point tool.
- Use `mouse/BENDPOINT_TOOL_SIMPLE_GUIDE.md` as the simple handoff doc for teammates and server use.
- When describing the method in class, Slack, or the paper, refer to it as a custom Python implementation of a standard elbow/knee heuristic and cite `LOMAR::find_elbow` as the closest documented R reference.
