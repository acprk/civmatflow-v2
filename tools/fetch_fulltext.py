#!/usr/bin/env python3
"""Legal full-text fetcher for civmatflow v2.

Order of candidate sources (all legal, all logged):
  Unpaywall (needs --email)  ->  OpenAlex best_oa_location / locations  ->
  Semantic Scholar openAccessPdf  ->  arXiv (when the DOI maps to an arXiv id)  ->
  CORE (only if ~/.config/core.key exists)  ->
  Elsevier TDM API (only if ~/.config/elsevier.key exists and the DOI is 10.1016/…)  ->
  NEED_FROM_USER.md (the user decides whether to supply the PDF via institutional access).
Never uses shadow libraries. Every attempt is logged to <out>/fetch_log.jsonl and every
successful download is recorded with its licence in <out>/LICENSES.tsv.

Usage: fetch_fulltext.py DOI [DOI ...] --out DIR [--email ADDR] [--list] [--sleep 1]
       fetch_fulltext.py --from-file dois.txt --out DIR
Standard library only.
"""
import argparse
import json
import pathlib
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "civmatflow2-fetch/1.1 (research; legal OA only)"
RETRY_STATUS = (429, 500, 502, 503, 504)


def http_get(url, headers=None, timeout=60, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    delay = 2
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read()
        except urllib.error.HTTPError as e:
            if e.code in RETRY_STATUS and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return e.code, "", b""
        except Exception as e:  # network errors
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return -1, str(e), b""
    return -1, "retries exhausted", b""


def norm_doi(doi):
    doi = doi.strip()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi, flags=re.I)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.I)
    return doi.rstrip(".,;")


def candidates(doi, email):
    q = urllib.parse.quote(doi, safe="")
    if email:
        st, _, body = http_get(f"https://api.unpaywall.org/v2/{q}?email={urllib.parse.quote(email)}")
        if st == 200:
            d = json.loads(body)
            for loc in [d.get("best_oa_location")] + (d.get("oa_locations") or []):
                if loc and loc.get("url_for_pdf"):
                    yield "unpaywall", loc["url_for_pdf"], loc.get("license")
    st, _, body = http_get(f"https://api.openalex.org/works/doi:{q}" + (f"?mailto={email}" if email else ""))
    if st == 200:
        d = json.loads(body)
        for loc in [d.get("best_oa_location")] + (d.get("locations") or []):
            if loc and loc.get("pdf_url"):
                yield "openalex", loc["pdf_url"], loc.get("license")
    st, _, body = http_get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{q}?fields=openAccessPdf,externalIds")
    if st == 200:
        d = json.loads(body)
        oa = d.get("openAccessPdf") or {}
        if oa.get("url"):
            yield "semanticscholar", oa["url"], oa.get("license")
        arx = (d.get("externalIds") or {}).get("ArXiv")
        if arx:
            yield "arxiv", f"https://arxiv.org/pdf/{arx}", "arXiv"
    if doi.lower().startswith("10.48550/arxiv."):
        yield "arxiv", f"https://arxiv.org/pdf/{doi[len('10.48550/arxiv.'):]}", "arXiv"
    core_key = pathlib.Path.home() / ".config" / "core.key"
    if core_key.exists():
        k = core_key.read_text().strip()
        st, _, body = http_get(f"https://api.core.ac.uk/v3/search/works?q=doi:%22{q}%22&limit=3",
                               headers={"Authorization": f"Bearer {k}"})
        if st == 200:
            for w in (json.loads(body).get("results") or []):
                if w.get("downloadUrl"):
                    yield "core", w["downloadUrl"], (w.get("license") or None)
    key = pathlib.Path.home() / ".config" / "elsevier.key"
    if key.exists() and doi.startswith("10.1016/"):
        k = key.read_text().strip()
        yield "elsevier_tdm", f"https://api.elsevier.com/content/article/doi/{q}?apiKey={k}&httpAccept=application/pdf", "TDM"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dois", nargs="*")
    ap.add_argument("--from-file", default=None, help="text file with one DOI per line (# comments allowed)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--email", default="", help="contact e-mail for Unpaywall / OpenAlex polite pool")
    ap.add_argument("--list", action="store_true", help="only list candidate URLs, download nothing")
    ap.add_argument("--sleep", type=float, default=1.0, help="pause between attempts (s)")
    a = ap.parse_args()
    dois = list(a.dois)
    if a.from_file:
        for line in pathlib.Path(a.from_file).read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                dois.append(line)
    if not dois:
        ap.error("no DOIs given")
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log = out / "fetch_log.jsonl"
    need = out / "NEED_FROM_USER.md"
    lic = out / "LICENSES.tsv"
    if not lic.exists():
        lic.write_text("doi\tfile\tsource\tlicense\n")
    summary = {"ok": 0, "cached": 0, "need": 0}
    for raw in dois:
        doi = norm_doi(raw)
        fname = out / (re.sub(r"[^A-Za-z0-9._-]", "_", doi) + ".pdf")
        if fname.exists():
            summary["cached"] += 1
            print(doi, "CACHED")
            continue
        ok = False
        for src, url, license_ in candidates(doi, a.email):
            if a.list:
                print(doi, src, url.split("apiKey=")[0], license_)
                continue
            st, ctype, body = http_get(url)
            good = st == 200 and body[:4] == b"%PDF"
            with log.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"doi": doi, "source": src, "url": url.split("apiKey=")[0], "status": st,
                                    "content_type": ctype[:60], "pdf": good, "license": license_, "t": time.time()}) + "\n")
            if good:
                fname.write_bytes(body)
                with lic.open("a", encoding="utf-8") as f:
                    f.write(f"{doi}\t{fname.name}\t{src}\t{license_ or ''}\n")
                ok = True
                break
            time.sleep(a.sleep)
        if a.list:
            continue
        if ok:
            summary["ok"] += 1
        else:
            summary["need"] += 1
            with need.open("a", encoding="utf-8") as f:
                f.write(f"- https://doi.org/{doi}  (no legal OA PDF found automatically; supply via institutional access or mark as blocked)\n")
        print(doi, "OK" if ok else "NEED_FROM_USER")
    if not a.list:
        print(json.dumps(summary))


if __name__ == "__main__":
    main()
