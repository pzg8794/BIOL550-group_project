# Canonical `full_fastp` shared handoff — 2026-03-18

Purpose:
- record the shared-side copy of the canonical cleaned-input QC and alignment outputs
- make the canonical paths explicit so the team can use one consistent version
- document why this copy exists

## Short answer

We copied the canonical `full_fastp` outputs from the private server-side workspace into the shared tree so the team can use the same cleaned-input QC summary and the same all-26 alignment for downstream analysis.

Shared canonical paths:
- MultiQC:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/full_fastp_canonical_privatecopy/`
- Alignment:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_full_fastp_canonical_privatecopy/`

These paths are intentionally named with `full_fastp_canonical_privatecopy` so they are easy to distinguish from the earlier shared trimmed-only outputs.

## Why this copy exists

The shared trimmed-only `fastp` outputs did not exactly match the canonical `full_fastp` outputs used in the private workspace.

What was confirmed in the audit:
- same `52` read-level reports
- same broad GC-warning pattern
- different retained-read counts
- different trimmed read-length ranges
- one remaining shared-side `Overrepresented Sequences` warning

That means:
- the shared trimmed-only output should not be treated as interchangeable with the canonical `full_fastp` output
- the team needs a shared-side copy of the canonical QC and alignment outputs

See:
- [Shared vs private `fastp` trim audit](SHARED_VS_PRIVATE_FASTP_TRIM_AUDIT_2026-03-18.md)

## What was copied

### Canonical MultiQC

Source:
- `/home/pzg8794/mouse_qc_remediation/multiqc/final_fastp_all_srrs/report/`

Shared destination:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/full_fastp_canonical_privatecopy/`

Expected contents:
- `mouse_fastp_all_srrs_multiqc.html`
- `mouse_fastp_all_srrs_multiqc_data/`
- `README_CANONICAL.txt`

### Canonical alignment

Source:
- `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/`

Shared destination:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_full_fastp_canonical_privatecopy/`

Expected contents:
- `samples/`
- `launcher_logs/`
- completion markers / manifests copied from the canonical run
- `README_CANONICAL.txt`

## Naming rule

Use the new shared-side paths with `full_fastp_canonical_privatecopy` when you want:
- the canonical cleaned-input QC summary
- the canonical alignment outputs that correspond to `/home/pzg8794/mouse_qc_remediation/output/fastp/out/`

Do not confuse these with:
- the earlier shared trimmed-only QC folder:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/multiqc/fastp_trim_only/`
- the earlier shared serial alignment run:
  - `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_fastp/`

## Decision

For downstream analysis and team comparison:
- treat the canonical `full_fastp` shared copy as the reference version
- treat the earlier shared trimmed-only QC outputs as non-canonical unless someone proves they are equivalent

## Team lesson

The technical takeaway is simple:
- shared outputs still need independent verification
- “group work” does not remove the need to check whether derived outputs are actually equivalent
- if a shared output is going to become the team reference, verify it before alignment starts

This is a process point, not a personal one. The fix is to keep one clearly named canonical output and make the paths explicit.

## Related docs

- [Alignment execution summary + index](ALIGNMENT_EXECUTION_SUMMARY_AND_INDEX.md)
- [Shared vs private `fastp` trim audit](SHARED_VS_PRIVATE_FASTP_TRIM_AUDIT_2026-03-18.md)
- [Shared alignment follow guide](ALIGNMENT_SHARED_TEAM_FOLLOW_GUIDE.md)
- [Mouse TODO](TODO_mouse.md)
- [Group project work log](../WORKLOG.md)
