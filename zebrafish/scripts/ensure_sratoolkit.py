#!/usr/bin/env python3
from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


def _run(cmd: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "biol550-sra-toolkit/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp, dest.open("wb") as f:
        shutil.copyfileobj(resp, f)


def _detect_platform_url() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()

    base = "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current"

    # Official source repo exists on GitHub (https://github.com/ncbi/sra-tools), but
    # building from source is slow and requires extra dependencies. For a reproducible
    # class workflow, we use the official prebuilt toolkit tarballs from NCBI.
    if system == "linux":
        # sequoia is Linux x86_64 in this course setup.
        return f"{base}/sratoolkit.current-ubuntu64.tar.gz"

    if system == "darwin":
        if machine in {"arm64", "aarch64"}:
            return f"{base}/sratoolkit.current-mac-arm64.tar.gz"
        return f"{base}/sratoolkit.current-mac64.tar.gz"

    raise SystemExit(f"Unsupported platform for SRA Toolkit auto-install: {system}/{machine}")


def _find_extracted_dir(tools_dir: Path) -> Path:
    candidates = sorted([p for p in tools_dir.glob("sratoolkit.*") if p.is_dir()])
    if not candidates:
        raise FileNotFoundError(f"No extracted sratoolkit.* directory found under {tools_dir}")
    return candidates[-1]


def main() -> int:
    p = argparse.ArgumentParser(
        description="Ensure NCBI SRA Toolkit is installed under zebrafish/tools/ (downloaded, not committed)."
    )
    p.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Repo root (default: two levels above this script).",
    )
    p.add_argument(
        "--tools-dir",
        default="zebrafish/tools",
        help="Tools directory relative to repo root (default: zebrafish/tools).",
    )
    p.add_argument(
        "--link-name",
        default="sratoolkit",
        help="Symlink name under tools-dir (default: sratoolkit).",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Re-download/re-extract even if toolkit seems installed.",
    )
    p.add_argument(
        "--print-bin",
        action="store_true",
        help="Print the resolved sratoolkit bin directory path (for PATH exports).",
    )
    args = p.parse_args()

    repo_root = Path(args.repo_root).resolve()
    tools_dir = (repo_root / args.tools_dir).resolve()
    link = tools_dir / args.link_name
    bin_dir = link / "bin"

    fasterq = bin_dir / "fasterq-dump"
    fastq = bin_dir / "fastq-dump"

    if not args.force and (fasterq.exists() or fastq.exists()):
        if args.print_bin:
            print(str(bin_dir))
        else:
            print(f"OK: SRA Toolkit already present at {link}")
            _run([str(fasterq if fasterq.exists() else fastq), "--version"])
        return 0

    url = _detect_platform_url()
    tools_dir.mkdir(parents=True, exist_ok=True)
    tarball = tools_dir / Path(url).name

    if tarball.exists() and not args.force:
        print(f"Using existing tarball: {tarball}")
    else:
        print(f"Downloading SRA Toolkit: {url}")
        _download(url, tarball)
        print(f"Saved: {tarball}")

    # Extract into tools_dir; the tarball contains a sratoolkit.<version>/ directory.
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        with tarfile.open(tarball, "r:gz") as tf:
            tf.extractall(path=tmp_path)
        extracted = _find_extracted_dir(tmp_path)
        target = tools_dir / extracted.name

        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(extracted, target)

    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink() or link.exists():
        if link.is_dir() and not link.is_symlink():
            shutil.rmtree(link)
        else:
            link.unlink()
    link.symlink_to(target.name)

    print(f"Installed: {link} -> {target.name}")
    if args.print_bin:
        print(str(bin_dir))
        return 0

    if fasterq.exists():
        _run([str(fasterq), "--version"])
    elif fastq.exists():
        _run([str(fastq), "--version"])
    else:
        raise SystemExit(f"Install completed but no fastq-dump/fasterq-dump found under {bin_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
