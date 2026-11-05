#!/usr/bin/env python3
"""Citation check (V9 / V11): every DOI in the bibliography must resolve.

Extracts DOIs from .bib (doi = {...} fields; entries without a DOI are listed) and
from .md / .tex / .txt files (bare DOIs), then resolves each one:
  Crossref  https://api.crossref.org/works/<doi>      (journal articles)
  DataCite  https://api.datacite.org/dois/<doi>       (Zenodo, figshare, data sets)
  doi.org   HEAD https://doi.org/<doi>                (anything else)
When the .bib entry has a title, a token-Jaccard similarity with the registered title
is reported (WARN below 0.5: wrong DOI pasted?). Results are cached in
<out-dir>/.refcheck_cache.json so re-runs only query new DOIs.

Usage: refcheck.py FILE [FILE ...] [--report CITATION_CHECK.md] [--offline] [--require-doi] [--strict]
Exit 1 when a DOI does not resolve (or, with --strict, when any network error remains).
Standard library only.
"""
import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "civmatflow2-refcheck/1.0 (research)"
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"'<>{}\]\),;]+")
BIB_ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", re.S)
BIB_FIELD = re.compile(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|[^,\n]+)", re.S)


def http(url, method="GET", timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return -1, str(e).encode()


def clean_doi(d):
    d = d.strip().rstrip(".,;:")
    d = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", d, flags=re.I)
    d = re.sub(r"^doi:\s*", "", d, flags=re.I)
    while d.endswith(")") and d.count("(") < d.count(")"):
        d = d[:-1]
    return d


def jaccard(a, b):
    ta = set(re.findall(r"[a-z0-9]{3,}", a.lower()))
    tb = set(re.findall(r"[a-z0-9]{3,}", b.lower()))
    return len(ta & tb) / len(ta | tb) if ta and tb else None


def parse_bib(text):
    items = []
    for m in BIB_ENTRY.finditer(text):
        kind, key, body = m.group(1), m.group(2), m.group(3)
        if kind.lower() in ("comment", "preamble", "string"):
            continue
        fields = {}
        for fm in BIB_FIELD.finditer(body):
            v = fm.group(2).strip().strip("{}\"").strip()
            fields[fm.group(1).lower()] = re.sub(r"\s+", " ", v)
        doi = clean_doi(fields["doi"]) if fields.get("doi") else None
        if not doi and fields.get("url"):
            dm = DOI_RE.search(fields["url"])
            doi = clean_doi(dm.group(0)) if dm else None
        items.append({"key": key, "doi": doi, "title": fields.get("title"), "year": fields.get("year")})
    return items


def resolve(doi):
    q = urllib.parse.quote(doi, safe="")
    st, body = http(f"https://api.crossref.org/works/{q}")
    if st == 200:
        msg = json.loads(body).get("message", {})
        title = (msg.get("title") or [""])[0]
        return {"status": "OK", "registry": "crossref", "title": title, "year": (msg.get("issued", {}).get("date-parts") or [[None]])[0][0],
                "container": (msg.get("container-title") or [""])[0]}
    st2, body2 = http(f"https://api.datacite.org/dois/{q}")
    if st2 == 200:
        attrs = json.loads(body2).get("data", {}).get("attributes", {})
        titles = attrs.get("titles") or [{}]
        return {"status": "OK", "registry": "datacite", "title": titles[0].get("title", ""), "year": attrs.get("publicationYear"),
                "container": attrs.get("publisher", "")}
    st3, _ = http(f"https://doi.org/{q}", method="HEAD")
    if st3 in (200, 301, 302, 303, 307, 308):
        return {"status": "OK", "registry": "doi.org", "title": "", "year": None, "container": ""}
    if 404 in (st, st2, st3):
        return {"status": "NOT_FOUND", "registry": "", "title": "", "year": None, "container": "", "http": [st, st2, st3]}
    return {"status": "NETWORK_ERROR", "registry": "", "title": "", "year": None, "container": "", "http": [st, st2, st3]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--report", default=None)
    ap.add_argument("--offline", action="store_true", help="syntax check only, no network")
    ap.add_argument("--require-doi", action="store_true", help="bib entries without a DOI are failures")
    ap.add_argument("--strict", action="store_true", help="network errors are failures too")
    ap.add_argument("--sleep", type=float, default=0.3)
    a = ap.parse_args()
    items = []
    for f in a.files:
        p = pathlib.Path(f)
        text = p.read_text(encoding="utf-8", errors="replace")
        if p.suffix.lower() == ".bib":
            for it in parse_bib(text):
                it["file"] = p.name
                items.append(it)
        else:
            for d in dict.fromkeys(clean_doi(m.group(0)) for m in DOI_RE.finditer(text)):
                items.append({"key": "", "doi": d, "title": None, "year": None, "file": p.name})
    cache_path = pathlib.Path(a.report).parent / ".refcheck_cache.json" if a.report else pathlib.Path(".refcheck_cache.json")
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    rows, fails = [], 0
    for it in items:
        doi = it["doi"]
        if not doi:
            status = "NO_DOI"
            if a.require_doi:
                fails += 1
            rows.append({**it, "status": status, "registry": "", "reg_title": "", "sim": ""})
            continue
        if not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
            fails += 1
            rows.append({**it, "status": "BAD_SYNTAX", "registry": "", "reg_title": "", "sim": ""})
            continue
        if a.offline:
            rows.append({**it, "status": "SYNTAX_OK", "registry": "", "reg_title": "", "sim": ""})
            continue
        if doi not in cache or cache[doi]["status"] == "NETWORK_ERROR":
            cache[doi] = resolve(doi)
            time.sleep(a.sleep)
        r = cache[doi]
        sim = jaccard(it["title"], r["title"]) if it.get("title") and r.get("title") else None
        status = r["status"]
        if status == "OK" and sim is not None and sim < 0.5:
            status = "OK_TITLE_MISMATCH"
        if status in ("NOT_FOUND",) or (a.strict and status == "NETWORK_ERROR"):
            fails += 1
        rows.append({**it, "status": status, "registry": r.get("registry", ""), "reg_title": r.get("title", ""),
                     "sim": "" if sim is None else f"{sim:.2f}"})
    cache_path.write_text(json.dumps(cache, indent=1))
    order = {"NOT_FOUND": 0, "BAD_SYNTAX": 0, "NETWORK_ERROR": 1, "OK_TITLE_MISMATCH": 2, "NO_DOI": 3, "SYNTAX_OK": 4, "OK": 5}
    rows.sort(key=lambda r: order.get(r["status"], 9))
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = ["# CITATION_CHECK", "", f"files: {', '.join(a.files)}; entries: {len(rows)}; "
             + "; ".join(f"{k}: {v}" for k, v in sorted(counts.items())), "",
             "| status | key | DOI | file | bib title | registered title | sim |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['status']} | {r['key']} | {r['doi'] or ''} | {r['file']} | {(r.get('title') or '')[:70]} | "
                     f"{(r['reg_title'] or '')[:70]} | {r['sim']} |")
    lines += ["", "Rules: NOT_FOUND / BAD_SYNTAX must be fixed before submission; OK_TITLE_MISMATCH means the DOI "
              "resolves to a different title (check the entry); NO_DOI entries need a DOI or a justification "
              "(standards, books, theses)."]
    rep = "\n".join(lines) + "\n"
    if a.report:
        pathlib.Path(a.report).write_text(rep, encoding="utf-8")
    print(rep)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
