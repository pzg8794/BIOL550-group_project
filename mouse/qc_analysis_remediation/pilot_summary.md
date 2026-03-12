# Mouse pilot QC strategy comparison

This report compares the pilot reads across four stages where available:
- raw
- current FASTX trimmed baseline
- fastp
- cutadapt

## SRR30333754_2 (poly-G dominated read 2)
- Raw FASTQ: length `151`, adapter_max `45.1251`, dominant signal `poly-G artifact` at `1.1193%`
- Current FASTX trimmed: length `75-151`, adapter_max `45.0897`, dominant signal `poly-G artifact` at `1.1193%`
- fastp: length `30-151`, adapter_max `0.0589`, dominant signal `not detected` at `NA%`
- cutadapt: length `30-151`, adapter_max `45.0601`, dominant signal `not detected` at `NA%`
- raw → FASTX: length `151 → 75-151`, adapter_max `45.1251 → 45.0897`, dominant signal `1.1193% → 1.1193%`
- FASTX → fastp: adapter_max `45.0897 → 0.0589`, dominant signal `1.1193% → NA%`, retained `95.5758%`
- FASTX → cutadapt: adapter_max `45.0897 → 45.0601`, dominant signal `1.1193% → NA%`, retained `97.5000%`

## SRR30333756_2 (poly-G dominated read 2)
- Raw FASTQ: length `151`, adapter_max `32.5277`, dominant signal `poly-G artifact` at `1.0565%`
- Current FASTX trimmed: length `84-151`, adapter_max `32.4893`, dominant signal `poly-G artifact` at `1.0565%`
- fastp: length `30-151`, adapter_max `0.0434`, dominant signal `not detected` at `NA%`
- cutadapt: length `30-151`, adapter_max `31.8831`, dominant signal `not detected` at `NA%`
- raw → FASTX: length `151 → 84-151`, adapter_max `32.5277 → 32.4893`, dominant signal `1.0565% → 1.0565%`
- FASTX → fastp: adapter_max `32.4893 → 0.0434`, dominant signal `1.0565% → NA%`, retained `95.7836%`
- FASTX → cutadapt: adapter_max `32.4893 → 31.8831`, dominant signal `1.0565% → NA%`, retained `97.7000%`

## SRR30333743_1 (explicit TruSeq adapter in read 1)
- Raw FASTQ: length `151`, adapter_max `49.2101`, dominant signal `TruSeq adapter` at `0.1040%`
- Current FASTX trimmed: length `118-151`, adapter_max `49.1768`, dominant signal `TruSeq adapter` at `0.1040%`
- fastp: length `30-151`, adapter_max `0.0054`, dominant signal `not detected` at `NA%`
- cutadapt: length `30-151`, adapter_max `0.0338`, dominant signal `not detected` at `NA%`
- raw → FASTX: length `151 → 118-151`, adapter_max `49.2101 → 49.1768`, dominant signal `0.1040% → 0.1040%`
- FASTX → fastp: adapter_max `49.1768 → 0.0054`, dominant signal `0.1040% → NA%`, retained `96.7674%`
- FASTX → cutadapt: adapter_max `49.1768 → 0.0338`, dominant signal `0.1040% → NA%`, retained `98.2000%`

