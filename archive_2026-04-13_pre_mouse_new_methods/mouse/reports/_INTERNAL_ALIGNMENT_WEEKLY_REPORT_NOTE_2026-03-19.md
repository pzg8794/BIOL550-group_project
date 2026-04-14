# Internal note — Mouse weekly report angle (2026-03-19)

## Chosen angle

- Weekly report focus = alignment validation, not environment setup and not DE-first.
- Local environment setup is included only as enabling context for independent validation of the canonical STAR run.
- Core claim:
  - the all-26 mouse dataset aligns well enough to proceed to DE
  - remaining platform and GC differences should be carried forward as metadata, not treated as immediate blockers

## Included figures

- `../alignment_analysis_star_all26/figures/unique_mapping_by_sample.png`
- `../alignment_analysis_star_all26/figures/unique_mapping_by_platform.png`
- `../alignment_analysis_star_all26/figures/unique_mapping_by_gc_status.png`
- `../alignment_analysis_star_all26/figures/assignment_burden_by_platform.png`

## Included table

- compact median summary for:
  - unique mapping
  - multi-mapping
  - `N_noFeature`
  - `N_ambiguous`
  - grouped by platform and GC status

## Intentionally excluded

- `input_reads_by_platform.png`
  - useful, but not needed for the main claim once alignment quality is already clear
- DE figures/tables
  - generated already, but left out of this weekly report to keep the report alignment-first
- large QC remediation dashboards / figure galleries
  - excluded because the professor’s last feedback explicitly criticized tiny figures and unclear figure meaning

## Drafting rule used

- every figure must answer:
  - what does this panel show?
  - why does it matter for downstream readiness?
- no panel is allowed to appear without immediate interpretation text below it

## Transcript-driven note folded into the draft

- The recent `2026-03-18` class discussion suggested checking whether the GC-content split tracks sequencing instrument and whether the alignment statistics remain reasonably consistent across those instrument-linked subsets.
- The current alignment notebook supports that explanation:
  - `NovaSeq X` aligns somewhat better than `NovaSeq 6000`
  - the GC-WARN subset aligns somewhat worse than GC-PASS
  - neither subset behaves like a failed-sample cluster
- The report therefore frames the GC shift as a likely platform-linked / batch-like effect that should be modeled downstream rather than treated as a reason to discard the full dataset.
