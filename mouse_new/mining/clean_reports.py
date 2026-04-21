#!/usr/bin/env python3
"""
clean_reports.py

Usage: python3 scripts/clean_reports.py <reports_dir>

- Ensures each .html report in <reports_dir> has a corresponding .pdf (tries Chrome or wkhtmltopdf).
- Moves likely duplicate HTML files into <reports_dir>/archive_duplicates/ (keeps newest file).

This script is conservative: it does not delete files, only creates PDFs (if possible)
and moves duplicates into `archive_duplicates` for review.
"""
import sys
import os
import shutil
import subprocess
import re
from pathlib import Path

VERSION = "0.1"

def find_chrome():
    candidates = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
        '/usr/bin/google-chrome',
        'google-chrome',
        'chrome',
        'chromium',
        'chromium-browser',
    ]
    for c in candidates:
        # if absolute path
        if os.path.isabs(c):
            if os.path.exists(c) and os.access(c, os.X_OK):
                return c
        else:
            p = shutil.which(c)
            if p:
                return p
    return None


def find_wkhtmltopdf():
    return shutil.which('wkhtmltopdf')


def html_to_pdf_chrome(chrome_path, html_path, pdf_path):
    # Use Chrome headless --print-to-pdf on file:// URL
    file_url = Path(html_path).absolute().as_uri()
    cmd = [chrome_path, '--headless', '--disable-gpu', '--no-sandbox', f'--print-to-pdf={str(pdf_path)}', file_url]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, ''
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode(errors='replace')


def html_to_pdf_wkhtmltopdf(wkpath, html_path, pdf_path):
    cmd = [wkpath, html_path, str(pdf_path)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, ''
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode(errors='replace')


def normalize_key(name: str) -> str:
    # Lowercase
    s = name.lower()
    # remove extension
    s = re.sub(r'\.html?$', '', s)
    # remove date patterns like _2026-04-16 or -2026-04-16
    s = re.sub(r'[_\-]\d{4}-\d{2}-\d{2}', '', s)
    # remove common version tokens
    s = re.sub(r'[_\-]?v\d+\b', '', s)
    s = re.sub(r'[_\-]?(final|final2|final3|final_v\d+|fixed|updated|fix|vfinal)\b', '', s)
    s = re.sub(r'\(\d+\)', '', s)
    s = re.sub(r'[_\-]?(copy)\b', '', s)
    s = re.sub(r'[_\-]+', '_', s)
    s = s.strip('_- ')
    return s


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 scripts/clean_reports.py <reports_dir>')
        sys.exit(2)
    reports_dir = Path(sys.argv[1]).resolve()
    if not reports_dir.exists() or not reports_dir.is_dir():
        print(f'Reports directory not found: {reports_dir}')
        sys.exit(1)

    chrome = find_chrome()
    wk = find_wkhtmltopdf()
    print(f'Version: {VERSION}')
    print(f'Reports dir: {reports_dir}')
    print(f'Chrome: {chrome}')
    print(f'wkhtmltopdf: {wk}')

    # 1) Find HTML files (skip archive folders)
    html_files = []
    for p in reports_dir.rglob('*.html'):
        # skip archive and archive_duplicates folders
        if any(part in ('archive', 'archive_duplicates') for part in p.parts):
            continue
        html_files.append(p)

    # 2) Ensure PDF exists for each HTML
    created_pdfs = []
    failed_pdfs = []
    for h in html_files:
        pdf_path = h.with_suffix('.pdf')
        if pdf_path.exists():
            continue
        # try converters
        converted = False
        if chrome:
            ok, err = html_to_pdf_chrome(chrome, str(h), str(pdf_path))
            if ok:
                converted = True
                created_pdfs.append(pdf_path)
            else:
                failed_pdfs.append((h, 'chrome', err))
        if not converted and wk:
            ok, err = html_to_pdf_wkhtmltopdf(wk, str(h), str(pdf_path))
            if ok:
                converted = True
                created_pdfs.append(pdf_path)
            else:
                failed_pdfs.append((h, 'wkhtmltopdf', err))
        if not converted:
            failed_pdfs.append((h, 'none', 'no converter available'))

    # 3) Detect duplicates by normalized key
    groups = {}
    for h in html_files:
        key = normalize_key(h.name)
        groups.setdefault(key, []).append(h)

    archive_dir = reports_dir / 'archive_duplicates'
    archive_dir.mkdir(exist_ok=True)

    moved_files = []
    for key, files in groups.items():
        if len(files) <= 1:
            continue
        # choose newest to keep
        files_sorted = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)
        keep = files_sorted[0]
        duplicates = files_sorted[1:]
        for d in duplicates:
            target = archive_dir / d.name
            # if target exists, append a numeric suffix
            i = 1
            base = target
            while target.exists():
                target = archive_dir / f"{base.stem}_{i}{base.suffix}"
                i += 1
            shutil.move(str(d), str(target))
            moved_files.append((d, target))

    # Summary
    print('--- Summary ---')
    print(f'Total HTML found: {len(html_files)}')
    print(f'PDFs created: {len(created_pdfs)}')
    if created_pdfs:
        for p in created_pdfs:
            print('  +', p)
    print(f'Failed PDF conversions: {len(failed_pdfs)}')
    for h, method, err in failed_pdfs:
        print('  -', h, method, err.splitlines()[0] if err else '')
    print(f'Moved duplicates to {archive_dir}: {len(moved_files)}')
    for src, dst in moved_files:
        print('  mv', src, '->', dst)

if __name__ == '__main__':
    main()
