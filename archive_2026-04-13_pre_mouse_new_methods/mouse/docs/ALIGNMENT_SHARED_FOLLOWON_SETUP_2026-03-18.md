# Shared-directory follow-on alignment setup — 2026-03-18

This note records the shared-directory STAR alignment setup that is chained to start after the private local-server alignment completes.

## Goal

Run the same `all 26` `STAR` alignment in the shared dataset tree:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/`

but only **after** the private run finishes under:
- `/home/pzg8794/mouse_qc_remediation/`

## Why this follow-on design was chosen

- The private run is already active and using the same cleaned dataset logic.
- The `STAR` index is already built once in the private workspace.
- Rebuilding the same mouse index in the shared tree while the private run is active would waste time and add unnecessary I/O.
- The cleaner approach is:
  1. let the private run finish
  2. sync the finished reference/index into the shared tree
  3. start the shared alignment automatically

## Shared inputs confirmed

Shared root:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/`

Shared trimmed read root:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/fastp_out/`

Expected shared trimmed read naming:
- mate 1: `SRR*_1.trim.fastq.gz`
- mate 2: `SRR*_2.trim.fastq.gz`

## Shared output targets

Shared reference root:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/reference/grcm39_ensembl/`

Shared alignment root:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_fastp/`

Shared launcher log root:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/`

## Trigger condition

The shared launcher waits for this private completion flag:
- `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/all26_fastp_alignment.completed`

Once that file exists, the shared launcher:
- syncs the private `GRCm39` + Ensembl reference bundle into the shared tree
- writes the shared manifest + metadata
- starts the three parallel STAR batch jobs in the shared tree

## Shared scripts added

Local sources:
- `Semester5/BIOL550/group_project/pipelines/mouse_star_align_one_srr_shared.sh`
- `Semester5/BIOL550/group_project/pipelines/mouse_star_align_batch_shared.sh`
- `Semester5/BIOL550/group_project/pipelines/mouse_run_star_all26_fastp_shared_after_private.sh`

Server targets:
- `/home/zebrafish/mouse/PRJNA1017789_parallel/scripts/`

## Practical note on the index

Yes, the index can be prepared now in the sense that the shared workflow is already wired to receive it.  
But the chosen implementation does **not** build a second index immediately.

Instead it reuses the already-correct private index after the private run completes, which is the lower-risk and lower-waste option.
