# Mouse project — TODO (PRJNA1017789 / GSE243308)

Keep this list current. Weekly report task must remain last.

## Pipeline + data
- [x] Confirm pipeline completion markers on server (`fastx.completed`, `end_to_end.completed`).
- [x] Verify final server counts: raw FASTQs + raw FastQC + trimmed FASTQs + trimmed FastQC are all **26/26**.
- [x] Cleanup temp/stale files (confirm no `*.tmp.*` left in `fastx_out/`).

## Local bundles (copy from Sequoia → Mac)
- [x] Copy **raw FastQC** bundle (ZIP + HTML) to `Semester5/BIOL550/group_project/mouse/qc_bundle_raw/` (52 ZIP + 52 HTML).
- [x] Copy **trimmed FastQC** bundle (ZIP + HTML) to `Semester5/BIOL550/group_project/mouse/qc_bundle_trimmed/` (52 ZIP + 52 HTML).
- [x] Re-check local counts (expect 52 ZIP + 52 HTML per stage for 26 paired-end runs).

## QC analysis (notebook + outputs)
- [x] Create mouse notebook (modeled after zebrafish notebook): raw FastQC summary (tables + plots + interpretation).
- [x] Add trimmed FastQC summary (same outputs + interpretation) — runs on whatever trimmed data is currently available.
- [x] Add raw vs trimmed comparison section:
  - [x] module-level counts deltas (pass/warn/fail)
  - [x] run-level severity deltas (improved vs unchanged vs worse)
  - [x] identify outliers + propose next cleanup tasks
  - [x] Re-run notebook after full trimmed bundle copy (26/26) to refresh plots + exports.

## Organization + cleanup
- [ ] Update `PROCESS_mouse_fastq_fastqc_fastx.md` with final server paths and the parallel runner command.
- [ ] Update `BIOL550-Notes.md` and `task_n_desc.md` with final completion snapshot + final paths.
- [ ] Flatten server directory structure under `/home/zebrafish/mouse/` (remove redundant `PRJNA1017789_parallel` nesting when safe).
- [ ] Archive/delete old baseline folder `/home/zebrafish/mouse/PRJNA1017789/` after verification.

## Deliverables (collected)
- [x] Keep weekly report HTML/PDF copies together in `Semester5/BIOL550/weekly_reports/_collected/` (with `manifest.csv`) for side-by-side review.

## Weekly report (last)
- [x] Draft weekly report paragraph-style using the final raw-vs-trimmed QC comparison insights + next steps (`mouse/reports/BIOL550_Weekly_Report_Mouse_SRA_FastQC_2026-03-04.html`).
- [x] Polish report wording/layout (MultiQC note + figure sizing tweaks).
