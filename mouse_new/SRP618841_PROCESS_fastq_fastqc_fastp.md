# SRP618841 — repeatable FASTQ → FastQC → fastp → FastQC workflow

This is the staged process doc for the `SRP618841` parallel mouse candidate. It follows the same local-truth / minimal-server rule as the active mouse dataset, but keeps all runtime paths separate from `PRJNA1017789`.

## Documentation links

- Parent mouse workflow: [PROCESS_mouse_fastq_fastqc_fastx.md](../mouse/PROCESS_mouse_fastq_fastqc_fastx.md)
- Dataset intake note: [SRP618841_DATASET_INTAKE_2026-03-25.md](SRP618841_DATASET_INTAKE_2026-03-25.md)
- Dataset TODO: [TODO_srp618841.md](TODO_srp618841.md)
- Group project work log: [../WORKLOG.md](../WORKLOG.md)
- Group project documentation map: [../DOCUMENTATION_MAP.md](../DOCUMENTATION_MAP.md)
- Server minimum policy: [../SERVER_MINIMUM_POLICY.md](../SERVER_MINIMUM_POLICY.md)

## Current dataset facts

- SRA study: `SRP618841`
- BioProject: `PRJNA1322439`
- Runs: `20`
- Species: `Mus musculus`
- Strategy: `RNA-Seq`
- Layout: `PAIRED`
- Platform/model: `Illumina NovaSeq X`

## Canonical local files

- RunInfo snapshot:
  - `Semester5/BIOL550/group_project/mouse_new/runs/SRP618841_runinfo.csv`
- Canonical run list:
  - `Semester5/BIOL550/group_project/mouse_new/runs/SRP618841_runs.all.txt`
- Canonical raw/trimmed-style QC notebook:
  - `Semester5/BIOL550/group_project/mouse_new/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse_new.ipynb`
- Mouse-style remediation replica:
  - `Semester5/BIOL550/group_project/mouse_new/notebooks/qc_remediation_experiments_mouse_new.ipynb`
- Mouse-style team-follow remediation replica:
  - `Semester5/BIOL550/group_project/mouse_new/notebooks/qc_remediation_experiments_mouse_new_team_follow.ipynb`
- Mouse-style alignment replica:
  - `Semester5/BIOL550/group_project/mouse_new/notebooks/mouse_alignment_analysis_star_all20.ipynb`
- Mouse-style DE replica:
  - `Semester5/BIOL550/group_project/mouse_new/notebooks/mouse_differential_expression_all20.ipynb`
- Canonical local QC outputs:
  - `Semester5/BIOL550/group_project/mouse_new/qc_analysis_raw_vs_trimmed/`
- Canonical launcher:
  - `Semester5/BIOL550/group_project/pipelines/srp618841_pipeline.sh`
- Canonical monitor:
  - `Semester5/BIOL550/group_project/pipelines/srp618841_monitor.sh`
- Canonical local sync watcher:
  - `Semester5/BIOL550/group_project/pipelines/srp618841_sync_completed_outputs_to_local.sh`

## Canonical local structure

The `mouse_new/` branch now mirrors the main stage directories we already use under `mouse/`:

- `runs/`
- `notebooks/`
- `qc_bundle_raw/`
- `qc_bundle_trimmed/`
- `qc_bundle_fastp_full/`
- `qc_analysis_raw_vs_trimmed/`
- `qc_analysis_remediation/`
- `fastp_reports_full/`
- `alignment_analysis_star_all20/`
- `differential_expression_all20/`
- `reports/`
- `multiqc/`

## Canonical server paths

- Data root:
  - `/home/zebrafish/mouse/SRP618841_parallel/`
- Metadata root:
  - `/home/pzg8794/metadata/SRP618841/`
- Server runs file:
  - `/home/pzg8794/metadata/SRP618841/SRP618841_runs.all.txt`
- Server launcher:
  - `/home/pzg8794/pipelines/srp618841_pipeline.sh`

## Runtime layout

Under `/home/zebrafish/mouse/SRP618841_parallel/`:

- `sra_runs/` — raw FASTQs
- `fastqc_out/` — raw FastQC
- `qc_remediation/fastp/out/` — `fastp` outputs
- `qc_remediation/fastqc_after/fastp/` — post-`fastp` FastQC
- `alignment/` — alignment outputs when we reach that stage
- `.pipeline/` — pipeline logs and markers
- `logs/` — short launcher logs / summaries

## Staged workflow

### Stage A — download + raw FastQC

Purpose:
- get the 20 FASTQ pairs
- generate the raw FastQC bundle
- confirm the server tree is isolated and resumable

Start:

```bash
source /home/zebrafish/mouse/PRJNA1017789_parallel/scripts/mouse_deseq2_activate_shared.sh 2>/dev/null || true
bash /home/pzg8794/pipelines/srp618841_pipeline.sh download-start
```

Status:

```bash
bash /home/pzg8794/pipelines/srp618841_pipeline.sh download-status
```

Monitor from local:

```bash
bash Semester5/BIOL550/group_project/pipelines/srp618841_monitor.sh
```

Stop:

```bash
bash /home/pzg8794/pipelines/srp618841_pipeline.sh download-stop
```

### Stage B — `fastp` + post-`fastp` FastQC

Purpose:
- generate cleaned inputs without building a FASTX baseline branch

Run:

```bash
bash /home/pzg8794/pipelines/srp618841_pipeline.sh fastp-run
```

### Stage C — alignment prep

Purpose:
- freeze the exact reference choice
- prepare the STAR index
- run staged alignment after Stage B is verified

Planned launcher:

```bash
bash /home/pzg8794/pipelines/srp618841_pipeline.sh star-run
```

## Step

- Created the canonical `SRP618841` run list and RunInfo snapshot.
- Added a dataset-specific launcher to keep the runtime isolated and copy/paste-ready.
- Copied the raw `FastQC` bundle and raw `MultiQC` back into the local `mouse_new/` tree.
- Replaced the earlier raw-only notebook with the same raw-vs-trimmed notebook pattern we used for the current mouse dataset.
- Copied the main mouse notebook set into `mouse_new/notebooks/` and retargeted the paths so the new dataset already has QC, remediation, alignment, and DE-stage notebook replicas ready to go.
- Added a local watcher script so completed server outputs can be copied back into `mouse_new/` automatically instead of one stage at a time.

## Status

- Stage A launcher ready.
- Stage B and Stage C launchers scaffolded.
- Raw download + raw `FastQC` complete on `sequoia`.
- Raw `MultiQC` complete and copied locally.
- Local notebook analysis now runs from `mouse_new/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse_new.ipynb`.
- `fastp` is the active running stage on `sequoia`.
- A local sync watcher can now keep pulling completed stage outputs from `sequoia` into `mouse_new/` while the pipeline runs.

## Finding

- The current reusable SRA / `fastp` / STAR scripts can be reused with dataset-specific path overrides.
- No new long analytical code needs to stay permanently on the server.
- The `mouse_new/` branch needed the same fixed notebook/output structure as `mouse/`, otherwise the analysis paths were too ad hoc to rerun cleanly.
- The raw `MultiQC` HTML contains embedded plot data, so we can analyze the consolidated report directly in the notebook instead of only linking out to the HTML.
- Mirroring the stage directories from `mouse/` makes it much easier to tell where future `fastp`, alignment, and DE artifacts should land.
- A local watcher is the cleanest way to avoid repeated manual copies while still keeping the server as a minimal runtime environment.

## Decision

- Launch this candidate through the short dataset-specific wrapper.
- Keep the local repo as the source of truth and the server wrapper operational only.
- Use the local monitor script for quick status checks instead of retyping the SSH/status commands.
- Treat `mouse_new/notebooks/fastqc_qc_bundle_analysis_raw_vs_trimmed_mouse_new.ipynb` as the canonical local QC notebook for this dataset.
- Let the watcher copy completed stage outputs back into `mouse_new/`, then finish notebook wording/tailoring as each stage becomes locally available.
