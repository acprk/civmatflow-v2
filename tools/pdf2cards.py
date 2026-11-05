#!/usr/bin/env python3
"""Compress PDFs into literature-card skeletons for civmatflow v2 (V3).

For each PDF: extract text (pdftotext if available, else PyMuPDF) into <text_dir>/,
and write a card skeleton with a title guess, a DOI guess, candidate equation lines,
candidate numeric result lines (with page numbers) and a checklist. The agent must
verify and complete equations / values against the original before setting the card
status to FULLTEXT. Papers that are only available as abstracts stay ABSTRACT-ONLY=UNVERIFIED.

Usage: pdf2cards.py PDF_DIR --cards CARD_DIR [--text TEXT_DIR] [--force] [--max-lines 40]
Requires pdftotext (poppler-utils) or PyMuPDF (pip install pymupdf).
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys

NUM = re.compile(r"(R\^?2|R²|RMSE|MAE|CoV|COV|coefficient of variation|error|NRMSE|MAPE|bias|mean ratio|RMSD)[^.\n]{0,80}?\d+(\.\d+)?\s*%?", re.I)
EQ = re.compile(r"\(\s*\d{1,2}[a-z]?\s*\)\s*$")
DOI = re.compile(r"\b10\.\d{4,9}/[^\s\"<>]+")


def pages_text(pdf):
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
        return out.split("\f")
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("pdf2cards: neither pdftotext (poppler-utils) nor PyMuPDF is available")
    return [p.get_text() for p in fitz.open(pdf)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf_dir")
    ap.add_argument("--cards", required=True)
    ap.add_argument("--text", default=None, help="text output dir (default: <cards>/../text)")
    ap.add_argument("--force", action="store_true", help="overwrite existing cards")
    ap.add_argument("--max-lines", type=int, default=40)
    a = ap.parse_args()
    pdf_dir = pathlib.Path(a.pdf_dir)
    cards = pathlib.Path(a.cards)
    text_dir = pathlib.Path(a.text) if a.text else cards.parent / "text"
    cards.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"pdf2cards: no PDFs in {pdf_dir}")
    for pdf in pdfs:
        card = cards / (pdf.stem + ".md")
        if card.exists() and not a.force:
            print("skip (exists)", card)
            continue
        pages = pages_text(pdf)
        (text_dir / (pdf.stem + ".txt")).write_text("\f".join(pages), encoding="utf-8")
        first = next((l.strip() for l in pages[0].splitlines() if len(l.strip()) > 25), pdf.stem) if pages else pdf.stem
        doi = DOI.search("\n".join(pages[:2])) if pages else None
        doi = doi.group(0).rstrip(".,;)") if doi else "[TODO]"
        eqs, nums = [], []
        for i, p in enumerate(pages, 1):
            for line in p.splitlines():
                s = line.strip()
                if EQ.search(s) and len(s) < 160:
                    eqs.append(f"- p{i}: `{s}`")
                if NUM.search(s):
                    nums.append(f"- p{i}: {s[:160]}")
        card.write_text(
            f"# {first}\n\nsource_pdf: {pdf.name}\ndoi: {doi}\npages: {len(pages)}\n"
            "status: SKELETON (verify against original, then set FULLTEXT or ABSTRACT-ONLY=UNVERIFIED)\n\n"
            "## Problem\n[TODO]\n\n## Model equations (LaTeX, with original eq. numbers)\n[TODO]\n\n"
            "### Candidate equation lines (auto, unverified)\n" + "\n".join(eqs[:a.max_lines]) + "\n\n"
            "## Datasets (source / records / licence)\n[TODO]\n\n## Metrics and values (page/table)\n[TODO]\n\n"
            "### Candidate numeric lines (auto, unverified)\n" + "\n".join(nums[:a.max_lines]) + "\n\n"
            "## Stated limitations\n[TODO]\n\n## Code / data links\n[TODO]\n\n"
            "## Relevance to our direction (baseline? competitor? data source?)\n[TODO]\n\n"
            "## Spot check (3 values re-read in original: value | page | OK?)\n[TODO]\n", encoding="utf-8")
        print("card", card)


if __name__ == "__main__":
    main()
