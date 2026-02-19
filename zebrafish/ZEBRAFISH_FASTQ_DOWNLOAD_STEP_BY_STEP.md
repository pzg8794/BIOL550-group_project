# Zebrafish FASTQ download (step-by-step)

Each step below is **copy/paste** plus **one line** saying what it does.

## Index

- [Zebrafish FASTQ download (step-by-step)](#zebrafish-fastq-download-step-by-step)
  - [Index](#index)
  - [Step 1 — Log into the server](#step-1--log-into-the-server)
  - [Step 2 — Go to the project folder](#step-2--go-to-the-project-folder)
  - [Step 3 — Select your dataset (your SRR list)](#step-3--select-your-dataset-your-srr-list)
  - [Step 3.1 — How the dataset was split (collaboration)](#step-31--how-the-dataset-was-split-collaboration)
  - [Step 4 — Count your runs + view the SRR IDs](#step-4--count-your-runs--view-the-srr-ids)
  - [Step 4.1 — What gets downloaded each time you run the script](#step-41--what-gets-downloaded-each-time-you-run-the-script)
  - [Step 5 — Heart of the script (what it runs under the hood)](#step-5--heart-of-the-script-what-it-runs-under-the-hood)
    - [The commands the script runs (the professor’s SRA Toolkit commands)](#the-commands-the-script-runs-the-professors-sra-toolkit-commands)
    - [Script options you will use](#script-options-you-will-use)
    - [Note: `fastq-dump` vs `fasterq-dump`](#note-fastq-dump-vs-fasterq-dump)
    - [Equivalence: `fastq-dump` vs `fasterq-dump` (same goal, different tool)](#equivalence-fastq-dump-vs-fasterq-dump-same-goal-different-tool)
      - [The “same thing” in practice (paired-end FASTQ)](#the-same-thing-in-practice-paired-end-fastq)
      - [Parameter equivalence (quick mapping)](#parameter-equivalence-quick-mapping)
      - [Why we use `fasterq-dump` in the team script](#why-we-use-fasterq-dump-in-the-team-script)
      - [When `fastq-dump` is still useful](#when-fastq-dump-is-still-useful)
  - [Step 6 — Recommended test: download 1 run](#step-6--recommended-test-download-1-run)
  - [Step 7 — Download N runs (YOU must set the number)](#step-7--download-n-runs-you-must-set-the-number)
  - [Step 8 — Check results (what “good” looks like)](#step-8--check-results-what-good-looks-like)
  - [Step 9 — Monitor progress (optional)](#step-9--monitor-progress-optional)
  - [TO-DO checklist](#to-do-checklist)
    - [After you run the TO-DO block (what it does / why / how it looks)](#after-you-run-the-to-do-block-what-it-does--why--how-it-looks)

---

## Step 1 — Log into the server

Type this in your terminal to log into sequoia (replace `<YOUR_NETID>` with your NetID):

```bash
ssh <YOUR_NETID>@sequoia.rit.edu
```

## Step 2 — Go to the project folder

Copy/paste (this puts you in the shared repo where the scripts are):

```bash
cd /home/zebrafish
pwd
ls -la
```

Important (performance):
- Keep large downloads **outside** the git repo folder when possible. Putting big FASTQ data under the repo can make the server feel slow.
- In this guide we set `OUT_DIR` under your `$HOME` (your personal space) so the repo stays lightweight.

## Step 3 — Select your dataset (your SRR list)

What “dataset” means here:
- The zebrafish project dataset is identified by **BioProject** `PRJNA1277581`.
- The actual download units are **SRR runs** (example run ID: `SRR34002427`).
- Your `RUNS_FILE` is a plain text file with **one SRR per line**. The download script will download whatever SRRs are listed in that file.

Why we do this for collaboration:
- The dataset is large. If everyone downloads the same runs, we waste time + disk space and overload the server.
- So we split the SRR list across team members (Piter / Nikhi / Samuel) so each person downloads a different subset.

Copy/paste (this sets `ACC`, your `NAME`, and your `RUNS_FILE`):

```bash
ACC=PRJNA1277581

# YOU MUST CHANGE THIS to your name: piter / nikhi / samuel
NAME=piter

RUNS_FILE="zebrafish/metadata/$ACC/splits/runs.member.${NAME}.txt"
ls -la "$RUNS_FILE"
```

What this does / why:
- `ACC=...` is the dataset ID (we use it to keep outputs organized).
- `NAME=...` chooses *your* run list file.
- `RUNS_FILE=...` points to the file containing the SRR IDs you will download.

## Step 3.1 — How the dataset was split (collaboration)

Where the shared metadata lives (created once and re-used):
- `zebrafish/metadata/PRJNA1277581/runinfo.csv` (run metadata table)
- `zebrafish/metadata/PRJNA1277581/runs.all.txt` (all SRR IDs, one per line)

Where your assigned SRR list lives (this is what you use):
- `zebrafish/metadata/PRJNA1277581/splits/runs.member.<name>.txt`

Copy/paste (this shows everyone’s split files and how many SRRs each person has):

```bash
ls -la "zebrafish/metadata/$ACC/splits"
for f in "zebrafish/metadata/$ACC/splits"/runs.member.*.txt; do
  echo
  echo "FILE: $f"
  wc -l "$f"
  head -n 3 "$f"
done
```

Important:
- Do **not** edit the split files. If something looks wrong (empty file, weird SRR IDs), tell the team lead.

## Step 4 — Count your runs + view the SRR IDs

Copy/paste (this shows how many runs you have, plus the first 10 SRR IDs):

```bash
wc -l "$RUNS_FILE"
head -n 10 "$RUNS_FILE"
```

If you want to see *all* SRR IDs (can be long), copy/paste:

```bash
cat "$RUNS_FILE"
```

## Step 4.1 — What gets downloaded each time you run the script

The script downloads the runs listed in your `RUNS_FILE` (one SRR per line). If you run the script again with the **same** `RUNS_FILE`, you are asking it to download/convert the **same SRR list** again.

Important notes:
- The script does **not** “know” your dataset automatically — the `--runs-file` you pass in is the dataset list.
- Re-running with the same `RUNS_FILE` and same `OUT_DIR` usually **skips work** because the `.fastq.gz` files already exist.
- If you change `OUT_DIR`, you can create **duplicate outputs** (even if the SRA cache download is reused).
- Use `--force` only if you truly want to re-create FASTQs even when they already exist.

## Step 5 — Heart of the script (what it runs under the hood)

Copy/paste (this shows the script usage and options):

```bash
bash zebrafish/scripts/download_fastq_sratoolkit_from_runs.sh --help
```

Copy/paste (this prints the script so you can see the “heart” of it):

```bash
sed -n '1,220p' zebrafish/scripts/download_fastq_sratoolkit_from_runs.sh
```

### The commands the script runs (the professor’s SRA Toolkit commands)

For each SRR in your `RUNS_FILE`, the wrapper runs:

1) Download the run (resumable download):

```bash
prefetch <SRR>
```

2) Convert to FASTQ using a “dump” command:

```bash
fasterq-dump --split-files --threads <THREADS> --outdir <RUN_DIR> <SRR>
```

Meaning of each parameter:
- `--split-files` → paired-end output: `<SRR>_1.fastq` and `<SRR>_2.fastq`
- `--threads <THREADS>` → CPU threads to use (example: `4`)
- `--outdir <RUN_DIR>` → output folder for that SRR
- `<SRR>` → the SRR you are downloading (example: `SRR34002427`)

3) Compress the FASTQs (saves space):

```bash
gzip -f <SRR>_1.fastq <SRR>_2.fastq
```

Final files you should see:
- `<SRR>_1.fastq.gz`
- `<SRR>_2.fastq.gz`

### Script options you will use

When you run the wrapper script, these are the options:
- `--runs-file <FILE>` → your SRR list file (one SRR per line)
- `--out-dir <DIR>` → where outputs go (script creates `<DIR>/<SRR>/...`)
- `--threads <N>` → how many threads `fasterq-dump` uses
- `--force` → re-download/re-create FASTQs even if files already exist

### Note: `fastq-dump` vs `fasterq-dump`

- This wrapper uses `fasterq-dump` (fast/modern) for **full FASTQ** downloads.
- In our **subset test notebook**, we sometimes use `fastq-dump` because it supports `-N/-X` (extract only the first N spots), which is useful for quick tests.

### Equivalence: `fastq-dump` vs `fasterq-dump` (same goal, different tool)

Both commands are from **SRA Toolkit** and both convert an SRR run into FASTQ files. The difference is mostly performance and options.

#### The “same thing” in practice (paired-end FASTQ)

What our script does (modern path):

```bash
prefetch <SRR>
fasterq-dump --split-files --threads 4 --outdir <RUN_DIR> <SRR>
gzip -f <RUN_DIR>/<SRR>_1.fastq <RUN_DIR>/<SRR>_2.fastq
```

The equivalent “classic” single-step conversion (paired-end) is:

```bash
fastq-dump --split-files --gzip -O <RUN_DIR> <SRR>
```

What you should end up with (either way):
- `<RUN_DIR>/<SRR>_1.fastq.gz`
- `<RUN_DIR>/<SRR>_2.fastq.gz`

#### Parameter equivalence (quick mapping)

- Paired-end split:
  - `fasterq-dump --split-files` ⇔ `fastq-dump --split-files`
- Output directory:
  - `fasterq-dump --outdir <DIR>` ⇔ `fastq-dump -O <DIR>`
- Speed / threads:
  - `fasterq-dump --threads 4` (fast + multi-threaded)
  - `fastq-dump` is typically slower and does not use `--threads` the same way
- Compression:
  - `fasterq-dump` writes `.fastq` (uncompressed) → we run `gzip -f ...`
  - `fastq-dump --gzip` writes `.fastq.gz` directly

#### Why we use `fasterq-dump` in the team script

- It is usually **faster** and supports **multi-threading** (`--threads`), which matters for large datasets.
- We still produce the same final paired FASTQs (R1/R2), just more efficiently.

#### When `fastq-dump` is still useful

For quick tests where you only want the first N “spots/reads”, `fastq-dump` supports spot subsetting:

```bash
# Extract spots 1..10000 (paired-end) to gzipped FASTQs
fastq-dump --split-files --gzip -N 1 -X 10000 -O <RUN_DIR> <SRR>
```

## Step 6 — Recommended test: download 1 run

This is the safest start: download **1 SRR** first before downloading many runs.

Why we do a 1-run test:
- It proves you are using the correct `RUNS_FILE` (right SRR IDs for you).
- It proves the script can download + convert on this server (permissions, tools, disk).
- It avoids wasting hours/disk space if something is misconfigured.

What it does (high level):
1) Creates a tiny file `RUNS_1` that contains only the first SRR from your `RUNS_FILE`.
2) Runs the wrapper script on that 1-SRR list:
   - downloads the SRR (`prefetch`)
   - converts it to paired FASTQ (`fasterq-dump --split-files`)
   - compresses to `.fastq.gz` (`gzip`)

How it looks when it runs (example output pattern):
- You will see it print your settings (runs file, output dir, threads).
- You will see a section like `== SRRxxxxxxxx ==` for the run it is processing.
- When it finishes, you should see two files for that SRR: `_1.fastq.gz` and `_2.fastq.gz`.

Copy/paste (this creates a 1-run file from your SRR list):

```bash
RUNS_1="zebrafish/metadata/$ACC/splits/runs.member.${NAME}.test1.txt"
head -n 1 "$RUNS_FILE" > "$RUNS_1"
```

Copy/paste (this prints the SRR you are about to download):

```bash
echo "Test SRR:"
cat "$RUNS_1"
```

Copy/paste (this runs the download and writes FASTQs into your folder):

```bash
DATA_ROOT="$HOME/biol550_zebrafish_data"
OUT_DIR="$DATA_ROOT/$ACC"
THREADS=4

bash zebrafish/scripts/download_fastq_sratoolkit_from_runs.sh \
  --runs-file "$RUNS_1" \
  --out-dir "$OUT_DIR" \
  --threads "$THREADS"
```

What you should see after it finishes (files created):

```text
$OUT_DIR/
  SRRxxxxxxxx/
    SRRxxxxxxxx_1.fastq.gz
    SRRxxxxxxxx_2.fastq.gz
```

Copy/paste (this shows you the output folder and confirms the two FASTQs exist):

```bash
ls -la "$OUT_DIR"
SRR="$(cat "$RUNS_1" | head -n 1 | tr -d '\r' | xargs)"
ls -lh "$OUT_DIR/$SRR"
```

Copy/paste (cleanup right after the test so the tutorial doesn’t leave data behind):

```bash
# Delete the FASTQs we just created for the test run (keeps your main OUT_DIR clean).
rm -rf "$OUT_DIR/$SRR"

# Delete the temporary 1-run list file we created for the test.
rm -f "$RUNS_1"
```

## Step 7 — Download N runs (YOU must set the number)

This downloads FASTQ for the first **N** SRRs from your list. You **must** edit the `N_RUNS=` line.

Copy/paste (this sets the number of runs to download):

```bash
# YOU MUST CHANGE THIS NUMBER:
N_RUNS=5
```

Copy/paste (this creates a file with exactly N SRR IDs and prints them):

```bash
RUNS_N="zebrafish/metadata/$ACC/splits/runs.member.${NAME}.first${N_RUNS}.txt"
head -n "$N_RUNS" "$RUNS_FILE" > "$RUNS_N"
echo "These SRRs will be downloaded:"
cat "$RUNS_N"
```

Copy/paste (this runs the download for those N runs):

```bash
DATA_ROOT="$HOME/biol550_zebrafish_data"
OUT_DIR="$DATA_ROOT/$ACC"
THREADS=4

bash zebrafish/scripts/download_fastq_sratoolkit_from_runs.sh \
  --runs-file "$RUNS_N" \
  --out-dir "$OUT_DIR" \
  --threads "$THREADS"
```

## Step 8 — Check results (what “good” looks like)

This confirms your output files exist and are valid `.fastq.gz` files.

Why we do this check:
- Downloads can silently fail or produce partial/corrupted files if a job is interrupted.
- You want to confirm you got **paired-end** output (R1 and R2) for each SRR.
- You want a quick “looks correct” check before moving on to alignment/analysis.

How “good output” looks (folder structure):

```text
$OUT_DIR/
  SRRxxxxxxxx/
    SRRxxxxxxxx_1.fastq.gz
    SRRxxxxxxxx_2.fastq.gz
  SRRyyyyyyyy/
    SRRyyyyyyyy_1.fastq.gz
    SRRyyyyyyyy_2.fastq.gz
```

What “good output” looks like (common signs):
- Each SRR folder contains **two** files: `_1.fastq.gz` and `_2.fastq.gz`
- File sizes are **not** 0 bytes (they will usually be MB to GB depending on run size)
- `gzip -t` runs with no error and prints `gzip OK`

Copy/paste (this lists the SRR folders created under your `OUT_DIR`):

```bash
ls -la "$OUT_DIR" | head
```

Copy/paste (this picks one SRR folder and shows file sizes):

```bash
SRR="$(ls -1 "$OUT_DIR" | head -n 1)"
ls -lh "$OUT_DIR/$SRR"
```

Copy/paste (this checks gzip integrity; it should print `gzip OK`):

```bash
gzip -t "$OUT_DIR/$SRR/${SRR}_1.fastq.gz"
gzip -t "$OUT_DIR/$SRR/${SRR}_2.fastq.gz"
echo "gzip OK"
```

Copy/paste (this shows the first FASTQ record: 4 lines):

```bash
zcat "$OUT_DIR/$SRR/${SRR}_1.fastq.gz" | head -n 4
zcat "$OUT_DIR/$SRR/${SRR}_2.fastq.gz" | head -n 4
```

## Step 9 — Monitor progress (optional)

Copy/paste (this shows whether you are downloading or converting right now):

```bash
ps -u "$USER" -o pid,etime,pcpu,pmem,cmd | egrep 'prefetch|fasterq-dump|fastq-dump' | head
```

Why you might use this (optional):
- If a download is taking a long time, this tells you whether it is still running.
- It tells you *what stage* you are in:
  - `prefetch` = downloading the SRR run data
  - `fasterq-dump` / `fastq-dump` = converting the run to FASTQ

What it does:
- Shows your running processes and filters to only SRA Toolkit commands.
- Prints:
  - `pid` = process ID
  - `etime` = how long it has been running
  - `pcpu` / `pmem` = CPU and memory usage
  - `cmd` = the command name (`prefetch`, `fasterq-dump`, etc.)

How it looks (example):

```text
  PID     ELAPSED %CPU %MEM CMD
1755088     02:06 51.7  0.0 prefetch-orig.3 SRR34002427
1678821     38:17 89.4  0.1 fastq-dump-orig SRR34002427
```

## TO-DO checklist

This is the “put the pieces together” block: it runs Steps 1–9 in the correct order so you don’t have to guess what to do next.

You only change **two** lines: `NAME=` and `N_RUNS=`.

Copy/paste this whole block:

```bash
cd /home/zebrafish

# YOU MUST CHANGE THIS: piter / nikhi / samuel
NAME=piter

ACC=PRJNA1277581

RUNS_FILE="zebrafish/metadata/$ACC/splits/runs.member.${NAME}.txt"
ls -la "$RUNS_FILE"
wc -l "$RUNS_FILE"
head -n 10 "$RUNS_FILE"

# TEST: 1 run only
RUNS_1="zebrafish/metadata/$ACC/splits/runs.member.${NAME}.test1.txt"
head -n 1 "$RUNS_FILE" > "$RUNS_1"
echo "Test SRR:"
cat "$RUNS_1"

OUT_DIR="zebrafish/data/$ACC"
THREADS=4
bash zebrafish/scripts/download_fastq_sratoolkit_from_runs.sh --runs-file "$RUNS_1" --out-dir "$OUT_DIR" --threads "$THREADS"

echo "Check output:"
ls -la "$OUT_DIR" | head
SRR="$(cat "$RUNS_1" | head -n 1 | tr -d '\r' | xargs)"
ls -lh "$OUT_DIR/$SRR"
gzip -t "$OUT_DIR/$SRR/${SRR}_1.fastq.gz"
gzip -t "$OUT_DIR/$SRR/${SRR}_2.fastq.gz"
echo "gzip OK"

# # DOWNLOAD MORE: YOU MUST CHANGE THIS NUMBER
# N_RUNS=5
#
# RUNS_N="zebrafish/metadata/$ACC/splits/runs.member.${NAME}.first${N_RUNS}.txt"
# head -n "$N_RUNS" "$RUNS_FILE" > "$RUNS_N"
# echo "These SRRs will be downloaded:"
# cat "$RUNS_N"
#
# OUT_DIR="zebrafish/data/$ACC"
# bash zebrafish/scripts/download_fastq_sratoolkit_from_runs.sh --runs-file "$RUNS_N" --out-dir "$OUT_DIR" --threads "$THREADS"
```

### After you run the TO-DO block (what it does / why / how it looks)

What it does:
- Runs a **1-run test download** first (safe test).
- If that works, it downloads **N runs** (you choose `N_RUNS`) from your assigned SRR list.

Why this is useful:
- You confirm the pipeline works *before* running a big multi‑GB download.
- You get the exact paired FASTQ files you need for alignment (`*_1.fastq.gz` and `*_2.fastq.gz`).

How it looks (example output for `N_RUNS=1`):

```text
runs_file_base: zebrafish/metadata/PRJNA1277581/splits/runs.member.piter.txt
runs_file_use:  zebrafish/metadata/PRJNA1277581/splits/runs.member.piter.first1.txt
out_dir:        zebrafish/data/PRJNA1277581
threads:        4

Starting download (N_RUNS=1)...
runs_file: zebrafish/metadata/PRJNA1277581/splits/runs.member.piter.first1.txt
out_dir:   zebrafish/data/PRJNA1277581
threads:   4
force:     0

== SRR34002439 ==
... prefetch downloads the SRR run data ...
... fasterq-dump converts it to FASTQ ...
reads written   : 241,524,444
```

What you should see on disk after it finishes:

```text
zebrafish/data/PRJNA1277581/
  SRR34002439/
    SRR34002439_1.fastq.gz
    SRR34002439_2.fastq.gz
```
