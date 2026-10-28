#!/usr/bin/env python3
"""Compress PDFs into literature-card skeletons for civmatflow v2.

For each PDF: extract text (pdftotext if available, else PyMuPDF) into text/,
and write a card skeleton with title guess, candidate equation lines, candidate
numeric result lines (with page numbers) and a checklist. The agent must verify
and complete equations/values against the original before marking FULLTEXT.

Usage: pdf2cards.py PDF_DIR --cards CARD_DIR [--text TEXT_DIR]
"""
import argparse
import pathlib
import re
import shutil
import subprocess

NUM = re.compile(r"(R\^?2|R²|RMSE|MAE|CoV|COV|coefficient of variation|error|NRMSE|MAPE)[^.\n]{0,80}?\d+(\.\d+)?\s*%?", re.I)
EQ = re.compile(r"\(\s*\d{1,2}[a-z]?\s*\)\s*$")


def pages_text(pdf):
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
        return out.split("\f")
    import fitz  # PyMuPDF
    return [p.get_text() for p in fitz.open(pdf)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_dir")
    ap.add_argument("--cards", required=True)
    ap.add_argument("--text", default=None)
    a = ap.parse_args()
    pdf_dir = pathlib.Path(a.pdf_dir)
    cards = pathlib.Path(a.cards)
    text_dir = pathlib.Path(a.text) if a.text else cards.parent / "text"
    cards.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(pdf_dir.glob("*.pdf")):
        card = cards / (pdf.stem + ".md")
        if card.exists():
            continue
        pages = pages_text(pdf)
        (text_dir / (pdf.stem + ".txt")).write_text("\f".join(pages))
        first = next((l.strip() for l in pages[0].splitlines() if len(l.strip()) > 25), pdf.stem) if pages else pdf.stem
        eqs, nums = [], []
        for i, p in enumerate(pages, 1):
            for line in p.splitlines():
                s = line.strip()
                if EQ.search(s) and len(s) < 160:
                    eqs.append(f"- p{i}: `{s}`")
                if NUM.search(s):
                    nums.append(f"- p{i}: {s[:160]}")
        card.write_text(
            f"# {first}\n\nsource_pdf: {pdf.name}\nstatus: SKELETON (verify against original, then set FULLTEXT or ABSTRACT-ONLY=UNVERIFIED)\n\n"
            "## Problem\n[TODO]\n\n## Model equations (LaTeX, with original eq. numbers)\n[TODO]\n\n"
            "### Candidate equation lines (auto, unverified)\n" + "\n".join(eqs[:40]) + "\n\n"
            "## Datasets (source / records / licence)\n[TODO]\n\n## Metrics and values (page/table)\n[TODO]\n\n"
            "### Candidate numeric lines (auto, unverified)\n" + "\n".join(nums[:40]) + "\n\n"
            "## Stated limitations\n[TODO]\n\n## Code / data links\n[TODO]\n\n## Spot check (3 values re-read in original)\n[TODO]\n")
        print("card", card)


if __name__ == "__main__":
    main()
