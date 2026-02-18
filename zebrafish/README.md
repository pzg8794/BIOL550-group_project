# Zebrafish (Danio rerio) group project workspace

This folder centralizes everything we create for the **zebrafish** dataset, while keeping **downloaded sequencing data out of Git**.

## Dataset

- BioProject: `PRJNA1277581`
- SRA study: `SRP592470`
- Organism: *Danio rerio*

## What lives where

- Scripts (API / downloads): `scripts/`
- Run metadata + SRR lists (safe to keep): `metadata/`
- Downloaded data (FASTQ/SRA; **not committed**): `data/`
- Downloaded tools (SRA Toolkit; **not committed**): `tools/`
- Notes/writeups: `notes/`

## Quick start

Generate RunInfo + SRR lists (via Entrez / E-utilities):

```bash
python3 scripts/get_zebrafish_data_sra.py
```

Split a run list among team members:

```bash
python3 scripts/split_runs_among_members.py \
  --runs-file metadata/PRJNA1277581/runs.filtered.txt \
  --members piter nikhi samuel \
  --out-dir metadata/PRJNA1277581/splits
```

Download run files (no toolkit) using `download_path` from `runinfo.csv`:

```bash
python3 scripts/download_runfiles_ncbi_download_path.py \
  --acc PRJNA1277581 \
  --runs-file metadata/PRJNA1277581/runs.filtered.txt \
  --runinfo-csv metadata/PRJNA1277581/runinfo.csv \
  --base-dir data/runfiles
```

Notebook walkthrough (recommended):

- `zebrafish_sra_api_test_download.ipynb`
- `zebrafish_github_setup_and_script_walkthrough.ipynb`

Install SRA Toolkit reproducibly (server or local; downloads official prebuilt tarball, does not commit binaries):

```bash
python3 scripts/ensure_sratoolkit.py --print-bin
```

This writes:

- `metadata/PRJNA1277581/runinfo.csv`
- `metadata/PRJNA1277581/runinfo.filtered.csv`
- `metadata/PRJNA1277581/runs.all.txt`
- `metadata/PRJNA1277581/runs.filtered.txt`

Download a *small test subset* (5 runs, first N spots; avoids multi‑GB downloads):

```bash
MAX_SPOTS=10000 bash scripts/download_test_5_runs_fastq.sh
```

If you’re ready to download full FASTQs on a machine with SRA Toolkit:

```bash
bash scripts/download_fastq_sratoolkit.sh
```
