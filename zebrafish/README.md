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
- Notes/writeups: `notes/`

## Quick start

Generate RunInfo + SRR lists (via Entrez / E-utilities):

```bash
python3 scripts/get_zebrafish_data_sra.py
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
