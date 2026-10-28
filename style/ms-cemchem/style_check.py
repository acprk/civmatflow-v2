#!/usr/bin/env python3
"""style_check.py -- Materials and Structures (RILEM) x cement chemistry / pore-solution thermodynamics.

Usage:
  python style_check.py draft.tex|draft.md|draft.docx|draft.txt [--json] [--sections intro,concl]
  python style_check.py --corpus-text text/KEY.txt          (corpus PDF text; used by scripts/s4_measure.py)

For every section (abstract, introduction, body, conclusions, all) it prints each statistic, the corpus
P10/P50/P90 from stats.json and the percentile of the draft value in the corpus distribution.
Total score = share of (section, metric) pairs whose value lies inside [P10, P90] of the corpus.
Only the Python standard library is required; python-docx is used for .docx when installed.
"""
import json, os, re, sys, statistics, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
STATS = os.path.join(HERE, "stats.json")

# ----------------------------------------------------------------------------- lexicons
HEDGES = r"may|might|could|can be|appear(?:s|ed)?|seem(?:s|ed)?|suggest(?:s|ed|ing)?|indicat(?:e|es|ed|ing)|likely|unlikely|possibl[ey]|probabl[ey]|presumabl[ey]|approximately|about|around|roughly|tend(?:s|ed)? to|potential(?:ly)?|partly|partially|somewhat|relatively|assum(?:e|ed|ing)|expected|plausibl[ey]|in principle"
BOOSTERS = r"clearly|obviously|significantly|strongly|substantially|markedly|considerably|undoubtedly|certainly|definitely|remarkabl[ey]|crucial(?:ly)?|essential(?:ly)?|novel|first time|unprecedented"
CONNECTIVES = {
    "however": r"however", "therefore": r"therefore", "thus": r"thus", "hence": r"hence",
    "moreover": r"moreover", "furthermore": r"furthermore", "in_addition": r"in addition",
    "whereas": r"whereas", "while": r"while", "consequently": r"consequently", "in_contrast": r"in contrast|on the other hand",
    "although": r"although|though", "similarly": r"similarly|likewise", "i_e_e_g": r"i\.e\.|e\.g\.",
    "as_a_result": r"as a result|due to", "overall": r"overall|in summary|in general",
}
PARTICIPLES_IRREG = "known|shown|given|taken|made|found|seen|done|written|chosen|built|drawn|held|kept|left|set|put|run|thought|brought|grown|understood|lost|formed|bound|split|fed|led|met|paid|sent|spent|told|won|caught|read|hidden|undertaken|overestimated|underestimated"
PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+|not\s+)?(?:\w+ed|" + PARTICIPLES_IRREG + r")\b", re.I)
ABBR = ["Fig", "Figs", "Eq", "Eqs", "Ref", "Refs", "et al", "e.g", "i.e", "ca", "approx", "No", "Tab", "vs", "cf", "resp", "wt", "vol", "Sect", "Ch", "Vol", "pp", "Dr", "etc", "Mr", "St"]


# ----------------------------------------------------------------------------- reading inputs
def read_docx(path):
    try:
        import docx  # python-docx
        d = docx.Document(path)
        out = []
        for p in d.paragraphs:
            st = (p.style.name or "").lower() if p.style is not None else ""
            if st.startswith("heading") or st == "title":
                out.append("# " + p.text)
            else:
                out.append(p.text)
        return "\n".join(out), "md"
    except ImportError:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf8", "replace")
        paras = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
        out = []
        for p in paras:
            t = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.S))
            if re.search(r'<w:pStyle w:val="(?:Heading|heading)\d', p):
                t = "# " + t
            out.append(t)
        return "\n".join(out), "md"


def tex_to_md(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", s, flags=re.S)
    abstract = m.group(1) if m else ""
    body = s[s.find("\\begin{document}"):] if "\\begin{document}" in s else s
    body = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", "", body, flags=re.S)
    body = re.sub(r"\\begin\{(equation|align|eqnarray|gather|multline)\*?\}.*?\\end\{\1\*?\}", " [EQ] ", body, flags=re.S)
    body = re.sub(r"\\begin\{(figure|table)\*?\}.*?\\end\{\1\*?\}", " ", body, flags=re.S)
    body = re.sub(r"\\(?:sub)*section\*?\{([^}]*)\}", lambda m: "\n# " + m.group(1) + "\n", body)
    body = re.sub(r"\\cite[pt]?\{([^}]*)\}", lambda m: "[" + ",".join("1" for _ in m.group(1).split(",")) + "]", body)
    body = re.sub(r"\\(?:ref|eqref|autoref|cref|Cref)\{[^}]*\}", "1", body)
    body = re.sub(r"\$[^$]*\$", " X ", body)
    body = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^}]*)\}", r"\2", body)
    body = re.sub(r"\\[a-zA-Z]+\*?", " ", body)
    body = body.replace("~", " ").replace("{", "").replace("}", "")
    if abstract:
        body = "# Abstract\n" + abstract + "\n" + body
    return body


def read_input(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        txt, kind = read_docx(path)
    else:
        txt = open(path, encoding="utf8", errors="replace").read()
        kind = "tex" if ext == ".tex" else "md"
    if kind == "tex":
        txt = tex_to_md(txt)
    return txt


# ----------------------------------------------------------------------------- sectioning
def canon(title):
    t = title.lower()
    if re.search(r"abstract", t):
        return "abstract"
    if re.search(r"introduc|background|state of the art", t):
        return "introduction"
    if re.search(r"conclu|concluding|summary and outlook|^summary|final remarks|^outlook", t):
        return "conclusions"
    if re.search(r"^references|bibliograph|acknowledg|funding|declaration|author contribution|data availab|appendix|supplementary|conflict|compliance", t):
        return "back"
    return "body"


def split_md(txt):
    secs = {"abstract": [], "introduction": [], "body": [], "conclusions": []}
    cur = "abstract" if not re.search(r"^#+\s", txt, flags=re.M) else None
    first = True
    for line in txt.splitlines():
        m = re.match(r"^#+\s*(?:\d+(?:\.\d+)*\.?\s*)?(.*)$", line)
        if m:
            c = canon(m.group(1))
            depth = len(line) - len(line.lstrip("#"))
            if c == "back":
                cur = None
            elif depth <= 2 or c in ("introduction", "conclusions", "abstract") or cur is None:
                if not (depth > 2 and cur in ("introduction", "body", "conclusions") and c == "body"):
                    cur = c
            first = False
            continue
        if cur:
            secs[cur].append(line)
    return {k: "\n".join(v) for k, v in secs.items()}


HEAD_RE = re.compile(r"^(\d{1,2})\.?\s+([A-Z][^\n]{2,90})$")


def clean_corpus_text(raw):
    raw = raw.replace("\f", "\n").replace("­", "")
    raw = re.sub(r"[\x00-\x08\x0b\x0e-\x1f]", "", raw)
    raw = re.sub(r"[ -​ ]", " ", raw)
    lines = raw.splitlines()
    out = []
    for ln in lines:
        s = ln.strip()
        if re.match(r"^(Materials and Structures|Mater Struct|Cement and Concrete (Research|Composites))\b.*\d", s):
            continue
        if re.match(r"^(Vol\.?:\(|\d{1,3}$|Page \d+ of \d+|https?://doi\.org|123$)", s):
            continue
        out.append(s)
    return out


def split_corpus(raw):
    """Split pdftotext (raw reading order) output into canonical sections."""
    lines = clean_corpus_text(raw)
    secs = {"abstract": [], "introduction": [], "body": [], "conclusions": []}
    cur, seen_intro, n_heads = None, False, 0
    i = 0
    while i < len(lines):
        s = lines[i]
        low = s.lower()
        if not seen_intro and re.match(r"^(abstract)\b", low):
            cur = "abstract"
            rest = s[8:].strip()
            if rest:
                secs[cur].append(rest)
            i += 1
            continue
        if cur == "abstract" and re.match(r"^(keywords?|key words)\b", low):
            cur = None
            i += 1
            continue
        m = HEAD_RE.match(s)
        if m and len(s.split()) <= 12 and (not s.endswith(".") or len(s.split()) <= 5) and not re.search(r"\d{3,}|[=<>%]|\bet al\b", s[3:]):
            c = canon(m.group(2).rstrip("."))
            num = int(m.group(1))
            if c == "introduction" and num <= 2:
                seen_intro = True
                cur = "introduction"
                n_heads = num
                i += 1
                continue
            title = m.group(2).strip().rstrip(".")
            wordy = re.fullmatch(r"[A-Za-z][A-Za-z ,\-–:&'()/]+", title) is not None and re.search(r"[a-z]{3,}", title)
            if seen_intro and ((c in ("conclusions", "back") and n_heads < num <= n_heads + 6 and wordy)
                               or (num == n_heads + 1 and wordy)):
                n_heads = num
                cur = "back" if c == "back" else c
                i += 1
                continue
        if seen_intro and re.match(r"^(references|acknowledg(e)?ments?|funding|declarations?|author contributions?|data availability|appendix|conflict of interest|compliance with ethical)\b", low) and len(s.split()) <= 6:
            cur = "back"
        if seen_intro and re.match(r"^(conclusions?|concluding remarks|summary and conclusions?)$", low):
            cur = "conclusions"
            i += 1
            continue
        if cur in secs:
            secs[cur].append(s)
        i += 1
    return {k: "\n".join(v) for k, v in secs.items()}


# ----------------------------------------------------------------------------- tokenising
def join_lines(t):
    t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)
    t = re.sub(r"\n(?!\n)", " ", t)
    return re.sub(r"[ \t]+", " ", t)


def drop_captions_tables(t):
    # remove figure/table captions and short numeric table rows from corpus text
    out = []
    for ln in t.split("\n"):
        s = ln.strip()
        if re.match(r"^(Fig\.?|Figure|Table|Tab\.)\s*\d+", s):
            continue
        if s and (sum(ch.isdigit() for ch in s) / max(1, len(s)) > 0.3 or len(s.split()) <= 2):
            continue
        out.append(ln)
    return "\n".join(out)


def sentences(t):
    t = join_lines(t)
    for a in ABBR:
        t = re.sub(r"\b" + re.escape(a) + r"\.", a.replace(".", "<D>") + "<D>", t)
    t = re.sub(r"(\d)\.(\d)", r"\1<D>\2", t)
    t = re.sub(r"\b([A-Z])\.", r"\1<D>", t)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\[(])", t)
    out = []
    for p in parts:
        p = p.replace("<D>", ".").strip()
        if len(re.findall(r"[A-Za-z]{2,}", p)) >= 4:
            out.append(p)
    return out


WORD = re.compile(r"[A-Za-z][A-Za-z\-']*")


def pct(v, arr):
    if not arr:
        return None
    below = sum(1 for a in arr if a < v)
    eq = sum(1 for a in arr if a == v)
    return round(100.0 * (below + 0.5 * eq) / len(arr), 1)


def quant(arr, q):
    a = sorted(arr)
    if not a:
        return None
    k = (len(a) - 1) * q
    f = int(k)
    c = min(f + 1, len(a) - 1)
    return a[f] + (a[c] - a[f]) * (k - f)


def metrics(text, corpus=False):
    if corpus:
        text = drop_captions_tables(text)
    sents = sentences(text)
    flat = " ".join(sents)
    words = WORD.findall(flat)
    nw = len(words)
    if nw < 40 or len(sents) < 3:
        return None
    lens = [len(WORD.findall(s)) for s in sents]
    per1k = lambda n: 1000.0 * n / nw
    low = flat.lower()
    m = {}
    m["n_words"] = nw
    m["sent_len_mean"] = statistics.mean(lens)
    m["sent_len_sd"] = statistics.pstdev(lens)
    m["sent_len_p90"] = quant(lens, 0.9)
    m["share_long_sent_gt35"] = sum(1 for x in lens if x > 35) / len(lens)
    m["passive_sent_share"] = sum(1 for s in sents if PASSIVE.search(s)) / len(sents)
    m["we_our_per1k"] = per1k(len(re.findall(r"\b(we|our|us|ours)\b", low)))
    m["this_study_per1k"] = per1k(len(re.findall(r"\b(this|the present|the current) (study|work|paper|investigation|contribution|report)\b", low)))
    m["hedge_per1k"] = per1k(len(re.findall(r"\b(?:" + HEDGES + r")\b", low)))
    m["booster_per1k"] = per1k(len(re.findall(r"\b(?:" + BOOSTERS + r")\b", low)))
    past = len(re.findall(r"\b(was|were|had)\b", low))
    pres = len(re.findall(r"\b(is|are|has|have)\b", low))
    m["past_aux_share"] = past / max(1, past + pres)
    m["connective_per1k"] = per1k(sum(len(re.findall(r"\b(?:" + v + r")", low)) for v in CONNECTIVES.values()))
    m["however_per1k"] = per1k(len(re.findall(r"\bhowever\b", low)))
    m["semicolon_per1k"] = per1k(flat.count(";"))
    m["parenthesis_per1k"] = per1k(flat.count("("))
    cites = re.findall(r"\[(\d+(?:\s*[,–\-]\s*\d+)*)\]", flat)
    ncite = 0
    for c in cites:
        for part in re.split(r"\s*,\s*", c):
            r = re.split(r"\s*[–\-]\s*", part)
            if len(r) == 2 and r[0].isdigit() and r[1].isdigit() and int(r[1]) > int(r[0]):
                ncite += min(int(r[1]) - int(r[0]) + 1, 20)
            else:
                ncite += 1
    ncite += len(re.findall(r"\(\s*[A-Z][A-Za-z\-]+(?: et al\.?| and [A-Z][A-Za-z\-]+)?,? (?:19|20)\d\d[a-z]?", flat))
    m["cite_per_sent"] = ncite / len(sents)
    m["cite_sent_share"] = sum(1 for s in sents if re.search(r"\[\d+|\((?:[A-Z][a-z]+ et al\.?|[A-Z][a-z]+),? (?:19|20)\d\d", s)) / len(sents)
    m["figtab_ref_per1k"] = per1k(len(re.findall(r"\b(Fig\.|Figs\.|Figure|Table|Tables)\s*\d", flat)))
    m["numbers_per100w"] = 100.0 * len(re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", flat)) / nw
    m["word_len_mean"] = statistics.mean(len(w) for w in words)
    m["nominalisation_per1k"] = per1k(len(re.findall(r"\b\w{4,}(?:tion|tions|ment|ments|ance|ence|ity|ities)\b", low)))
    return m


METRIC_NOTE = {
    "sent_len_mean": "mean words/sentence", "sent_len_sd": "SD of sentence length", "sent_len_p90": "90th pct sentence length",
    "share_long_sent_gt35": "share of sentences >35 words", "passive_sent_share": "share of sentences with a passive",
    "we_our_per1k": "we/our/us per 1000 words", "this_study_per1k": "'this study/work' per 1000 words",
    "hedge_per1k": "hedges per 1000 words", "booster_per1k": "boosters per 1000 words",
    "past_aux_share": "was/were/had share of finite aux", "connective_per1k": "connectives per 1000 words",
    "however_per1k": "'however' per 1000 words", "semicolon_per1k": "semicolons per 1000 words",
    "parenthesis_per1k": "parentheses per 1000 words", "cite_per_sent": "citations per sentence",
    "cite_sent_share": "share of sentences with a citation", "figtab_ref_per1k": "Fig./Table refs per 1000 words",
    "numbers_per100w": "numerals per 100 words", "word_len_mean": "mean word length (chars)",
    "nominalisation_per1k": "-tion/-ment/-ity nouns per 1000 words",
}
SCORED = [k for k in METRIC_NOTE]
SECTIONS = ["abstract", "introduction", "body", "conclusions", "all"]


def analyse_sections(secs, corpus=False):
    res = {}
    allt = "\n".join(secs.get(k, "") for k in ("abstract", "introduction", "body", "conclusions"))
    for k in SECTIONS:
        t = allt if k == "all" else secs.get(k, "")
        res[k] = metrics(t, corpus=corpus) if t.strip() else None
    tot = sum((res[k] or {}).get("n_words", 0) for k in ("abstract", "introduction", "body", "conclusions"))
    for k in ("abstract", "introduction", "body", "conclusions"):
        if res[k] and tot:
            res[k]["word_share"] = res[k]["n_words"] / tot
    return res


def check(path, as_json=False, only=None):
    txt = read_input(path)
    secs = split_md(txt)
    res = analyse_sections(secs)
    st = json.load(open(STATS)) if os.path.exists(STATS) else None
    report, inside, total = {}, 0, 0
    lines = []
    for sec in SECTIONS:
        if only and sec not in only:
            continue
        r = res.get(sec)
        if not r:
            lines.append(f"\n[{sec}] (absent or <40 words)")
            continue
        lines.append(f"\n[{sec}]  words={r['n_words']}")
        lines.append(f"  {'metric':28s} {'value':>8s} {'P10':>7s} {'P50':>7s} {'P90':>7s} {'pctl':>6s}  ok")
        report[sec] = {}
        for k in SCORED + (["word_share"] if sec != "all" else []):
            v = r.get(k)
            if v is None:
                continue
            dist = (st or {}).get("dist", {}).get(sec, {}).get(k) if st else None
            if dist:
                p10, p50, p90 = quant(dist, .1), quant(dist, .5), quant(dist, .9)
                pc = pct(v, dist)
                ok = p10 <= v <= p90
                if k in SCORED:
                    total += 1
                    inside += ok
                lines.append(f"  {k:28s} {v:8.3f} {p10:7.3f} {p50:7.3f} {p90:7.3f} {pc:6.1f}  {'Y' if ok else '-'}")
                report[sec][k] = {"value": v, "p10": p10, "p50": p50, "p90": p90, "pctl": pc, "ok": ok}
            else:
                lines.append(f"  {k:28s} {v:8.3f}")
                report[sec][k] = {"value": v}
    score = inside / total if total else None
    if as_json:
        print(json.dumps({"score": score, "sections": report}, indent=1))
    else:
        print(f"style_check (ms-cemchem) -- {path}")
        print("\n".join(lines))
        if score is not None:
            med = (st or {}).get("score_median")
            if only:
                sub = (st or {}).get("subset_scores", {}).get(",".join(only))
                med = sub["median"] if sub else med
            print(f"\nTOTAL SCORE = {score:.3f}  ({inside}/{total} metrics inside corpus [P10,P90])"
                  + (f"; corpus median self-score = {med:.3f}; gate (90% of median) = {0.9*med:.3f}" if med else ""))
    return score, report


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(0)
    if a[0] == "--corpus-text":
        secs = split_corpus(open(a[1], encoding="utf8", errors="replace").read())
        print(json.dumps({k: (len(v.split())) for k, v in secs.items()}))
        sys.exit(0)
    only = None
    if "--sections" in a:
        only = a[a.index("--sections") + 1].split(",")
    check(a[0], as_json="--json" in a, only=only)
