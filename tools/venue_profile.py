#!/usr/bin/env python3
"""Journal topic profile (V0): what do the target journals publish, and what is growing?

fetch     Pull bibliographic records for a list of journals and years from Crossref
          (works endpoint, cursor pagination, polite pool via --mailto) into
          <out>/raw/<slug>_<year>.jsonl. OpenAlex can be used instead with --source openalex
          (richer abstracts, stricter rate limits).
classify  Read the raw files, classify every record as experimental / computational-theory /
          pure-ML / review by title (+ abstract when present) keyword rules, assign topics,
          and write <out>/classified.csv, <out>/topic_map.md and a random sample
          <out>/sample_for_manual_check.csv (fill the manual_class column by hand).
score     Compare a filled sample file with the automatic classes and report the agreement
          rate — report this number next to every count that comes from title-only data
          (0970 experience: about ±30 points when abstracts are missing).

Usage:
  venue_profile.py fetch --journals CCR,CBM --years 2023-2025 --out venue --mailto you@x.org [--max 500]
  venue_profile.py classify --out venue [--sample 60 --seed 1]
  venue_profile.py score --sample venue/sample_for_manual_check.csv
  venue_profile.py journals            # print the built-in journal -> ISSN table (verify before use)
Standard library only.
"""
import argparse
import csv
import json
import pathlib
import random
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request

UA = "civmatflow2-venue/1.0 (research)"

# Built-in journal table. ISSNs are from the journals' own pages; verify before relying on them.
JOURNALS = {
    "CCR": ("Cement and Concrete Research", "0008-8846"),
    "CCC": ("Cement and Concrete Composites", "0958-9465"),
    "CBM": ("Construction and Building Materials", "0950-0618"),
    "CompB": ("Composites Part B: Engineering", "1359-8368"),
    "MS": ("Materials and Structures", "1359-5997"),
    "JBE": ("Journal of Building Engineering", "2352-7102"),
    "JMCE": ("Journal of Materials in Civil Engineering", "0899-1561"),
    "CSCM": ("Case Studies in Construction Materials", "2214-5095"),
    "EFM": ("Engineering Fracture Mechanics", "0013-7944"),
    "MechMater": ("Mechanics of Materials", "0167-6636"),
    "MCR": ("Magazine of Concrete Research", "0024-9831"),
    "StructConcr": ("Structural Concrete", "1464-4177"),
    "JACT": ("Journal of Advanced Concrete Technology", "1346-8014"),
}

REVIEW = r"\b(review|state[- ]of[- ]the[- ]art|overview|perspective|roadmap|survey|bibliometric)\b"
ML = r"\b(machine[- ]learning|deep[- ]learning|neural network|ann|cnn|lstm|transformer|random forest|xgboost|gradient boosting|catboost|lightgbm|support vector|svm|gaussian process|data[- ]driven|artificial intelligence|genetic programming|symbolic regression|ensemble learning|shap|bayesian optimi[sz]ation|surrogate model)\b"
COMP = r"\b(model(?:l)?ing|model|simulation|numerical|analytical|theoretical|theory|finite[- ]element|fem|phase[- ]field|lattice|discrete element|dem|peridynamic|homogeni[sz]ation|micromechanic\w*|mesoscale|meso[- ]scale|multiscale|thermodynamic\w*|constitutive|closed[- ]form|size[- ]effect law|prediction model|predictive model|kinetic\w* model|reactive transport|molecular dynamics|monte carlo|probabilistic|reliability|formulation|derivation)\b"
EXP = r"\b(experimental|experiment\w*|test\w*|specimen\w*|laboratory|measured|measurement\w*|characteri[sz]ation|xrd|sem|tga|nmr|mip|microstructur\w*|mix design|mixture\w*|cast\w*|cured|curing|performance of|properties of|effect of|influence of|behavio(?:u)?r of|utili[sz]ation of|recycl\w*|waste|fresh and hardened)\b"

TOPICS = {
    "fracture_size_effect": r"\b(fracture|size effect|crack\w*|cohesive|fracture energy|toughness|notch\w*|quasi[- ]?brittle|softening|fpz)\b",
    "durability_transport": r"\b(chloride|carbonation|sulfate|sulphate|freeze[- ]thaw|diffusion|permeab\w*|transport|durability|corrosion|service life|ingress|moisture transport|drying|sorption)\b",
    "itz_interface": r"\b(interfacial transition zone|itz|interface\w*|bond\w*|pull[- ]out|debonding)\b",
    "damage_plasticity_constitutive": r"\b(constitutive|damage|plasticity|plastic|stress[- ]strain|hardening|viscoplastic|fatigue|dynamic|impact|strain rate)\b",
    "thermodynamics_hydration": r"\b(thermodynamic\w*|hydration|gems|phase assemblage|pore solution|c-s-h|c-a-s-h|kinetic\w*|dissolution|calorimetr\w*|degree of hydration|reactivity)\b",
    "creep_shrinkage": r"\b(creep|shrinkage|relaxation|viscoelastic\w*|autogenous|long[- ]term deformation|time[- ]dependent)\b",
    "frp_confinement_bond": r"\b(frp|fibre[- ]reinforced polymer|fiber[- ]reinforced polymer|confin\w*|wrapped|cfrp|gfrp|bfrp|strengthen\w*)\b",
    "homogenization_porous": r"\b(homogeni[sz]ation|effective propert\w*|micromechanic\w*|porous|foam\w*|cellular|lightweight|aerated|rve|representative volume)\b",
    "fibre_composites": r"\b(fibre|fiber|uhpc|ecc|shcc|strain[- ]hardening|textile|steel fiber|steel fibre|pullout)\b",
    "alkali_activated_geopolymer": r"\b(alkali[- ]activated|geopolymer|slag|fly ash|calcined clay|lc3|metakaolin|scm\w*|supplementary cementitious)\b",
    "3d_printing": r"\b(3d[- ]print\w*|additive manufactur\w*|printab\w*|extrusion)\b",
    "thermal_fire": r"\b(fire|elevated temperature\w*|high temperature\w*|thermal conductiv\w*|spalling)\b",
    "asr_expansion": r"\b(alkali[- ]silica|asr|delayed ettringite|def|expansion)\b",
}


def http_json(url, retries=4):
    delay = 2
    for i in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return e.code, None
        except Exception:
            if i < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return -1, None
    return -1, None


def parse_years(s):
    if "-" in s:
        a, b = s.split("-", 1)
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in s.split(",")]


def cmd_fetch(a):
    out = pathlib.Path(a.out) / "raw"
    out.mkdir(parents=True, exist_ok=True)
    keys = [k.strip() for k in a.journals.split(",")] if a.journals != "all" else list(JOURNALS)
    for k in keys:
        if k not in JOURNALS and not re.fullmatch(r"\d{4}-\d{3}[\dX]", k):
            sys.exit(f"unknown journal key {k}; use `venue_profile.py journals` or pass an ISSN")
    for k in keys:
        name, issn = JOURNALS.get(k, (k, k))
        slug = re.sub(r"[^A-Za-z0-9]", "", k)
        for y in parse_years(a.years):
            f = out / f"{slug}_{y}.jsonl"
            if f.exists() and not a.force:
                print("exists", f)
                continue
            n, cursor, recs = 0, "*", []
            while True:
                if a.source == "crossref":
                    url = (f"https://api.crossref.org/journals/{issn}/works?filter=from-pub-date:{y}-01-01,until-pub-date:{y}-12-31,type:journal-article"
                           f"&rows={a.rows}&cursor={urllib.parse.quote(cursor)}&select=DOI,title,abstract,issued,is-referenced-by-count,container-title,type"
                           + (f"&mailto={a.mailto}" if a.mailto else ""))
                    st, d = http_json(url)
                    if st != 200 or not d:
                        print(f"{k} {y}: HTTP {st}; stopping this year after {n} records (resume with --force later)")
                        break
                    items = d["message"]["items"]
                    for it in items:
                        recs.append({"doi": it.get("DOI"), "title": (it.get("title") or [""])[0],
                                     "abstract": re.sub(r"<[^>]+>", " ", it.get("abstract") or ""),
                                     "year": y, "journal": name, "key": k, "cited": it.get("is-referenced-by-count", 0),
                                     "source": "crossref"})
                    n += len(items)
                    cursor = d["message"].get("next-cursor")
                    if not items or not cursor or (a.max and n >= a.max):
                        break
                else:  # openalex
                    url = (f"https://api.openalex.org/works?filter=primary_location.source.issn:{issn},publication_year:{y},type:article"
                           f"&per-page={min(a.rows, 200)}&cursor={urllib.parse.quote(cursor)}&select=doi,title,abstract_inverted_index,publication_year,cited_by_count"
                           + (f"&mailto={a.mailto}" if a.mailto else ""))
                    st, d = http_json(url)
                    if st != 200 or not d:
                        print(f"{k} {y}: HTTP {st} (OpenAlex rate limit? retry after UTC midnight or with a key); stopping after {n}")
                        break
                    items = d.get("results", [])
                    for it in items:
                        inv = it.get("abstract_inverted_index") or {}
                        words = sorted((pos, w) for w, poss in inv.items() for pos in poss)
                        recs.append({"doi": (it.get("doi") or "").replace("https://doi.org/", ""), "title": it.get("title") or "",
                                     "abstract": " ".join(w for _, w in words), "year": y, "journal": name, "key": k,
                                     "cited": it.get("cited_by_count", 0), "source": "openalex"})
                    n += len(items)
                    cursor = (d.get("meta") or {}).get("next_cursor")
                    if not items or not cursor or (a.max and n >= a.max):
                        break
                time.sleep(a.sleep)
            with f.open("w", encoding="utf-8") as fh:
                for r in recs:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"{k} {y}: {len(recs)} records -> {f}")


def classify_record(r):
    text = (r.get("title") or "") + " " + (r.get("abstract") or "")
    low = text.lower()
    title = (r.get("title") or "").lower()
    if re.search(REVIEW, title):
        cls = "review"
    elif re.search(ML, low):
        cls = "pure_ml" if not re.search(r"\b(physics[- ]informed|mechanistic|hybrid|constitutive|thermodynamic)\b", low) else "computational_theory"
    elif re.search(COMP, title) and not re.search(r"\b(experimental (study|investigation)|tests? on|specimens?)\b", title):
        cls = "computational_theory"
    elif re.search(EXP, title):
        cls = "experimental"
    elif re.search(COMP, low):
        cls = "computational_theory"
    else:
        cls = "experimental"
    topics = [t for t, pat in TOPICS.items() if re.search(pat, low)]
    return cls, topics


def cmd_classify(a):
    base = pathlib.Path(a.out)
    raw = base / "raw"
    files = sorted(raw.glob("*.jsonl"))
    if not files:
        sys.exit(f"no raw files in {raw}; run fetch first")
    recs = []
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                recs.append(json.loads(line))
    n_abs = sum(1 for r in recs if r.get("abstract"))
    rows = []
    for r in recs:
        cls, topics = classify_record(r)
        rows.append({**r, "class": cls, "topics": ";".join(topics)})
    with (base / "classified.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["key", "journal", "year", "doi", "cited", "class", "topics", "title"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    years = sorted({r["year"] for r in rows})
    keys = sorted({r["key"] for r in rows})

    def growth(sel):
        if len(years) < 2:
            return None
        half = max(1, len(years) // 2)
        early, late = years[:half], years[-half:]
        tot_e = sum(1 for r in rows if r["year"] in early) or 1
        tot_l = sum(1 for r in rows if r["year"] in late) or 1
        se = sum(1 for r in sel if r["year"] in early) / tot_e
        sl = sum(1 for r in sel if r["year"] in late) / tot_l
        return (sl / se) if se else None
    lines = ["# Topic map", "", f"records: {len(rows)} from {len(files)} raw files; with abstract: {n_abs} "
             f"({100 * n_abs / max(1, len(rows)):.0f} %). **Title-only classification is approximate** — report the agreement "
             "rate from `venue_profile.py score` next to these counts.", "",
             "## Class share per journal (all years)", "", "| journal | n | experimental | computational/theory | pure ML | review |", "|---|---|---|---|---|---|"]
    for k in keys:
        sub = [r for r in rows if r["key"] == k]
        n = len(sub) or 1
        c = {c_: sum(1 for r in sub if r["class"] == c_) for c_ in ("experimental", "computational_theory", "pure_ml", "review")}
        lines.append(f"| {k} | {len(sub)} | {100 * c['experimental'] / n:.0f} % | {100 * c['computational_theory'] / n:.0f} % | {100 * c['pure_ml'] / n:.0f} % | {100 * c['review'] / n:.0f} % |")
    lines += ["", "## Topics (non-experimental records only: computational/theory + pure ML)", "",
              "| topic | n | " + " | ".join(str(y) for y in years) + " | growth (late/early share) | pure-ML share | median citations | " + " | ".join(keys) + " | top-cited DOIs |",
              "|---|---|" + "---|" * len(years) + "---|---|---|" + "---|" * len(keys) + "---|"]
    nonexp = [r for r in rows if r["class"] in ("computational_theory", "pure_ml")]
    topic_rows = []
    for t in TOPICS:
        sel = [r for r in nonexp if t in r["topics"].split(";")]
        if not sel:
            continue
        g = growth(sel)
        ml = sum(1 for r in sel if r["class"] == "pure_ml") / len(sel)
        med = statistics.median(int(r.get("cited") or 0) for r in sel)
        top = sorted(sel, key=lambda r: -int(r.get("cited") or 0))[:3]
        topic_rows.append((t, len(sel), [sum(1 for r in sel if r["year"] == y) for y in years], g, ml, med,
                           [sum(1 for r in sel if r["key"] == k) for k in keys], [r["doi"] for r in top]))
    for t, n, per_y, g, ml, med, per_k, dois in sorted(topic_rows, key=lambda x: -x[1]):
        lines.append(f"| {t} | {n} | " + " | ".join(str(x) for x in per_y) + f" | {'' if g is None else f'{g:.2f}'} | {100 * ml:.0f} % | {med:.0f} | "
                     + " | ".join(str(x) for x in per_k) + " | " + ", ".join(d for d in dois if d) + " |")
    lines += ["", "Reading guide: a direction needs a topic with a stable or growing share, a low pure-ML share "
              "(crowding) and public data (checked separately at G0). Growth = share in the later half of the years "
              "divided by the share in the earlier half."]
    (base / "topic_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if a.sample:
        rng = random.Random(a.seed)
        samp = rng.sample(rows, min(a.sample, len(rows)))
        with (base / "sample_for_manual_check.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["doi", "title", "auto_class", "manual_class"])
            w.writeheader()
            for r in samp:
                w.writerow({"doi": r["doi"], "title": r["title"], "auto_class": r["class"], "manual_class": ""})
    print(json.dumps({"records": len(rows), "with_abstract": n_abs, "classified_csv": str(base / "classified.csv"),
                      "topic_map": str(base / "topic_map.md")}))


def cmd_score(a):
    with open(a.sample, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("manual_class", "").strip()]
    if not rows:
        sys.exit("no rows with manual_class filled")
    agree = sum(1 for r in rows if r["manual_class"].strip() == r["auto_class"].strip())
    conf = {}
    for r in rows:
        conf.setdefault((r["manual_class"].strip(), r["auto_class"].strip()), 0)
        conf[(r["manual_class"].strip(), r["auto_class"].strip())] += 1
    print(json.dumps({"n_checked": len(rows), "agreement": round(agree / len(rows), 3),
                      "confusion(manual,auto)": {f"{m}->{au}": c for (m, au), c in sorted(conf.items())}}, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--journals", default="all", help="comma-separated keys (see `journals`) or ISSNs, or 'all'")
    f.add_argument("--years", required=True, help="e.g. 2023-2025 or 2022,2024")
    f.add_argument("--out", required=True)
    f.add_argument("--mailto", default="")
    f.add_argument("--source", choices=("crossref", "openalex"), default="crossref")
    f.add_argument("--rows", type=int, default=1000)
    f.add_argument("--max", type=int, default=0, help="cap records per journal-year (testing)")
    f.add_argument("--sleep", type=float, default=1.0)
    f.add_argument("--force", action="store_true")
    c = sub.add_parser("classify")
    c.add_argument("--out", required=True)
    c.add_argument("--sample", type=int, default=60)
    c.add_argument("--seed", type=int, default=1)
    s = sub.add_parser("score")
    s.add_argument("--sample", required=True)
    sub.add_parser("journals")
    a = ap.parse_args()
    if a.cmd == "journals":
        for k, (n, i) in JOURNALS.items():
            print(f"{k:12s} {i}  {n}")
        return
    {"fetch": cmd_fetch, "classify": cmd_classify, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
