# Full-dataset FASTX vs fastp QC comparison

- Reports compared: `52` read-level FastQC reports (`26` paired-end SRRs).
- FASTX baseline directory: `/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/qc_bundle_trimmed`
- fastp post-QC directory: `/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/qc_bundle_fastp_full`
- fastp report directory: `/Users/pitergarcia/DataScience/Semester5/BIOL550/group_project/mouse/fastp_reports_full`

## Report-ready findings

- Adapter signal improved strongly overall: median `adapter_max` changed from `31.8806` under FASTX to `0.0051` after fastp.
- Across all read reports, median `adapter_max` delta (`fastp - FASTX`) was `-31.8737`, meaning fastp reduced the residual signal in the typical read.
- Read retention remained high after fastp: median retained reads were `97.52%` of the pre-fastp totals.
- Post-fastp quality remained strong: median `Q30` rate after filtering was `93.83%`.

## Module-level status changes

- Adapter Content: FASTX pass/warn/fail = `0/0/52`, fastp pass/warn/fail = `52/0/0`, improved/unchanged/worse = `52/0/0`.
- Overrepresented sequences: FASTX pass/warn/fail = `37/13/2`, fastp pass/warn/fail = `52/0/0`, improved/unchanged/worse = `15/37/0`.
- Per base sequence content: FASTX pass/warn/fail = `0/26/26`, fastp pass/warn/fail = `0/26/26`, improved/unchanged/worse = `0/52/0`.
- Sequence Length Distribution: FASTX pass/warn/fail = `0/52/0`, fastp pass/warn/fail = `0/52/0`, improved/unchanged/worse = `0/52/0`.

## Largest adapter-signal improvements

- `SRR30333743_2`: `adapter_max` `49.3904` -> `0.0661` (delta `-49.3243`).
- `SRR30333743_1`: `adapter_max` `49.1768` -> `0.0054` (delta `-49.1715`).
- `SRR30333755_2`: `adapter_max` `48.6043` -> `0.0950` (delta `-48.5093`).
- `SRR30333755_1`: `adapter_max` `48.2808` -> `0.0049` (delta `-48.2759`).
- `SRR30333753_2`: `adapter_max` `46.6565` -> `0.0826` (delta `-46.5739`).

## Remaining reads to review

- No read reports remain in `fail` for `Adapter Content` or `Overrepresented sequences` after fastp.

## Interpretation

- This comparison is the primary file-level validation layer because it parses and compares the underlying FastQC outputs directly for every read report.
- The FASTX and FASTX-vs-fastp MultiQC reports should be used as supplementary confirmation and summary layers, not as the only basis for interpretation.
