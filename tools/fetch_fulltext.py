#!/usr/bin/env python3
"""Legal full-text fetcher for civmatflow v2.

Order: Unpaywall -> OpenAlex best_oa_location -> Semantic Scholar openAccessPdf
-> arXiv (if DOI maps to arXiv) -> Elsevier TDM (only if ~/.config/elsevier.key exists)
-> NEED_FROM_USER. Never uses shadow libraries. Logs every attempt.

Usage: fetch_fulltext.py DOI [DOI ...] --out DIR [--email ADDR]
"""
import argparse
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request

UA = "civmatflow2-fetch/1.0 (research; legal OA only)"


def http_get(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, "", b""
    except Exception as e:  # network errors
        return -1, str(e), b""


def candidates(doi, email):
    q = urllib.parse.quote(doi)
    if email:
        st, _, body = http_get(f"https://api.unpaywall.org/v2/{q}?email={urllib.parse.quote(email)}")
        if st == 200:
            d = json.loads(body)
            for loc in [d.get("best_oa_location")] + (d.get("oa_locations") or []):
                if loc and loc.get("url_for_pdf"):
                    yield "unpaywall", loc["url_for_pdf"], loc.get("license")
    st, _, body = http_get(f"https://api.openalex.org/works/doi:{q}")
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
    key = pathlib.Path.home() / ".config" / "elsevier.key"
    if key.exists() and doi.startswith("10.1016/"):
        k = key.read_text().strip()
        yield "elsevier_tdm", f"https://api.elsevier.com/content/article/doi/{q}?apiKey={k}&httpAccept=application/pdf", "TDM"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dois", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--email", default="")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log = out / "fetch_log.jsonl"
    need = out / "NEED_FROM_USER.md"
    for doi in a.dois:
        doi = doi.strip().removeprefix("https://doi.org/")
        fname = out / (re.sub(r"[^A-Za-z0-9._-]", "_", doi) + ".pdf")
        if fname.exists():
            continue
        ok = False
        for src, url, lic in candidates(doi, a.email):
            st, ctype, body = http_get(url)
            good = st == 200 and body[:4] == b"%PDF"
            with log.open("a") as f:
                f.write(json.dumps({"doi": doi, "source": src, "url": url.split("apiKey=")[0],
                                    "status": st, "pdf": good, "license": lic, "t": time.time()}) + "\n")
            if good:
                fname.write_bytes(body)
                ok = True
                break
            time.sleep(1)
        if not ok:
            with need.open("a") as f:
                f.write(f"- https://doi.org/{doi}  (no legal OA PDF found automatically)\n")
        print(doi, "OK" if ok else "NEED_FROM_USER")


if __name__ == "__main__":
    main()
