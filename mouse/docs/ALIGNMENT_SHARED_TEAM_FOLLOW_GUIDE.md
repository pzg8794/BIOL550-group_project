# Mouse alignment — shared follow guide (simple version)

Purpose:
- give the team the minimum they need to follow the alignment phase
- show where the shared reference, index, inputs, logs, and outputs live
- reduce repeated questions about what to run and what not to touch

## Short version

The cleanup decision is already made:
- use the `fastp` outputs as the alignment inputs

The alignment is being done in two places:
- private first: `/home/pzg8794/mouse_qc_remediation/`
- shared second: `/home/zebrafish/mouse/PRJNA1017789_parallel/`

The shared run is chained to start automatically after the private run finishes.

## What the team will get in the shared tree

### Shared trimmed inputs
- `/home/zebrafish/mouse/PRJNA1017789_parallel/fastp_out/`

Expected naming:
- mate 1: `SRR*_1.trim.fastq.gz`
- mate 2: `SRR*_2.trim.fastq.gz`

### Shared reference bundle
- `/home/zebrafish/mouse/PRJNA1017789_parallel/reference/grcm39_ensembl/`

This shared reference bundle will contain:
- the chosen mouse FASTA
- the matching Ensembl GTF
- the STAR index
- reference metadata

### Shared alignment outputs
- `/home/zebrafish/mouse/PRJNA1017789_parallel/alignment/star_grcm39_ensembl_all26_fastp/`

### Shared logs
- `/home/zebrafish/mouse/PRJNA1017789_parallel/logs/`

## What is the reference choice?

Chosen reference pair:
- assembly: `GRCm39`
- annotation: matching `Ensembl` GTF

Reason:
- modern mouse assembly
- matching annotation set
- one consistent reference/index for the full alignment

## How the shared run starts

The shared run does **not** start by hand right now.

It waits for this private completion flag:
- `/home/pzg8794/mouse_qc_remediation/alignment/star_grcm39_ensembl_all26_fastp/all26_fastp_alignment.completed`

Once that file exists, the shared launcher will:
1. copy the finished reference/index bundle into the shared tree
2. write the shared metadata files
3. start the shared STAR alignment

## What not to ask before checking the paths above

- where are the cleaned files?
- where is the reference?
- where is the STAR index?
- where are the logs?
- where are the alignment outputs?

All of those are answered in this file.

## What not to do

- do not build another mouse index in a random directory
- do not point STAR at old FASTX outputs
- do not rename files in `fastp_out/`
- do not start a second shared alignment manually unless we decide to replace the current one

## If you only need the practical status

Current status:
- `fastp` is the chosen cleanup stage
- private alignment is the canonical first run
- shared alignment is queued to start automatically after the private run finishes

## If you want the fuller explanation

Read these next:
- `ALIGNMENT_SHARED_FOLLOWON_SETUP_2026-03-18.md`
- `MOUSE_GROUP_FOLLOW_GUIDE.md`
- `TODO_mouse.md`
