# Dataset notes (zebrafish)

## Target dataset

- BioProject: `PRJNA1277581`
- SRA study: `SRP592470`
- Organism: *Danio rerio* (zebrafish)
- Description: Müller glia–microglia cross talk reprograms the Müller glia transcriptome during retina regeneration.

Strengths:
- Strong depth and long reads across all runs.
- Clear biological focus (retina regeneration) with many samples.

Weaknesses:
- Zebrafish model; may not fit projects requiring mammalian/human context.

## Validation criteria we’ve been using (class baseline)

- `LibraryStrategy == RNA-Seq`
- `LibraryLayout == PAIRED`
- `avgLength >= 150`
- `spots >= 40,000,000`

For this dataset (per the existing validation notes in `BIOL550-Lab/task_n_desc.md`):

- Runs: 30 total, 30/30 pass the filters above
- Read characteristics: `avgLength ~302`, `spots ~50.9M–173.3M`

## Where the SRR list + run metadata lives

- `metadata/PRJNA1277581/runinfo.csv`
- `metadata/PRJNA1277581/runinfo.filtered.csv`
- `metadata/PRJNA1277581/runs.all.txt`
- `metadata/PRJNA1277581/runs.filtered.txt`

## References (in this repo)

- Validation notes: `Semester5/BIOL550/BIOL550-Lab/task_n_desc.md`
- Group project plan: `Semester5/BIOL550/group_project/BIOL550 Group Project Plan Outline.md`
- Project-pick notebook: `Semester5/BIOL550/BIOL550-Lab/project_pic/BIOL550-Project-Pick.ipynb`
