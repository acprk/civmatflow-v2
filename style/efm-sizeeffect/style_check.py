#!/usr/bin/env python3
"""style_check.py -- EFM quasi-brittle fracture / size-effect style checker (key: efm-sizeeffect).

Usage
  python style_check.py DRAFT.(tex|md|docx|txt)        # check a draft against the corpus (stats.json)
  python style_check.py DRAFT --json                    # machine-readable output
  python style_check.py --build                         # rebuild stats.json from text/*.txt (hold-outs excluded)
  python style_check.py --selftest                      # leave-one-out scores of corpus papers

Per section (abstract / introduction / conclusions / body) it prints every statistic, its empirical
percentile in the corpus distribution, the corpus [P10, P90] band and whether the value is inside it.
Total score = fraction of (section, metric) pairs whose value lies inside [P10, P90].
Macro (whole-paper) metrics are scored only if the draft has >= 4 top-level sections (or --full).
Only the Python standard library is required; python-docx is used for .docx if available.
"""
import json
import math
import os
import re
import statistics
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
STATS = os.path.join(HERE, "stats.json")
TEXT_DIR = os.path.join(HERE, "text")
HOLDOUT = {"A_augusthus2021", "A_zhu2020", "A_miarka2020"}  # never used for distillation / stats

# ----------------------------------------------------------------------------- lexicons
HEDGES = r"may|might|could|possibly|possible|likely|unlikely|perhaps|appears?|appeared|seems?|seemed|" \
         r"suggests?|suggested|indicates?|indicated|approximately|roughly|relatively|generally|typically|" \
         r"usually|tends?|tended|somewhat|presumably|probably|partly|partially|essentially|nearly|almost"
BOOSTERS = r"clearly|obviously|significantly|substantially|strongly|remarkably|undoubtedly|definitely|" \
           r"considerably|markedly|greatly|highly|always|never|certainly|indeed"
CONNECTORS = ["however", "moreover", "furthermore", "therefore", "thus", "hence", "in addition", "consequently",
              "whereas", "although", "nevertheless", "on the other hand", "in contrast", "accordingly",
              "similarly", "finally", "in particular", "for instance", "for example", "namely", "i.e.", "e.g."]
AI_WORDS = r"delve|delves|crucial|pivotal|intricate|underscores?|showcases?|leverag\w*|robust|comprehensive|" \
           r"notably|landscape|realm|seamless\w*|holistic|paramount|multifaceted|meticulous\w*|groundbreaking|" \
           r"cutting-edge|game-changer|elucidat\w*|harness\w*|unveil\w*|shed light|paving the way|tapestry"
IRREG = "shown|known|given|taken|made|seen|found|done|written|chosen|drawn|built|held|kept|set|put|cut|split|" \
        "broken|grown|thrown|understood|run|laid|led|left|meant|met|paid|read|sent|spent|brought|bought|" \
        "caught|taught|thought|told|sold|won|begun|frozen|hidden|proven|driven|beaten|worn|torn|borne|cast|" \
        "spread|bent|fed|dealt|sought|struck|bound|ground|undertaken|overcome|withdrawn|forgotten"
PASSIVE = re.compile(r"\b(am|is|are|was|were|be|been|being)\s+(?:(?:not|also|then|thus|further|first|"
                     r"generally|usually|often|widely|commonly|\w+ly)\s+)?(\w+ed|" + IRREG + r")\b", re.I)
ABBREV = ["et al.", "e.g.", "i.e.", "Fig.", "Figs.", "Eq.", "Eqs.", "Ref.", "Refs.", "vs.", "approx.", "No.",
          "Sect.", "Sec.", "Ch.", "Tab.", "cf.", "resp.", "Dr.", "Prof.", "St.", "Jr.", "ca.", "viz.", "etc.)",
          "Mr.", "Ms.", "Inc.", "Ltd.", "Co.", "Vol.", "pp.", "Eng.", "Mech.", "Struct.", "Mater.", "Int.",
          "J.", "Res.", "Proc.", "Appl.", "Phys.", "min.", "max.", "Exp.", "Comput.", "Constr.", "Build."]

STOP_HEAD = re.compile(r"^(references|bibliography|acknowledg|declaration of competing|declaration of interest|"
                       r"credit authorship|data availability|funding|appendix|nomenclature|conflict of interest|"
                       r"author contributions|supplementary)", re.I)
CONCL_HEAD = re.compile(r"^(summary and conclusions?|conclusions? and (outlook|perspectives?|future work|remarks|"
                        r"discussion)|concluding remarks|conclusions?|summary|final remarks|closing remarks|"
                        r"closing comments)\b", re.I)
INTRO_HEAD = re.compile(r"^introduction\b", re.I)
ABS_HEAD = re.compile(r"^(abstract|a\s?b\s?s\s?t\s?r\s?a\s?c\s?t)\s*[:.]?\s*", re.I)

SECTIONS = ["abstract", "introduction", "conclusions", "body"]
TEXT_METRICS = [
    ("sent_len_mean", "mean sentence length (words)"),
    ("sent_len_sd", "sentence length SD (words)"),
    ("long_sent_share", "share of sentences > 35 words"),
    ("passive_share", "share of sentences with a passive verb group"),
    ("we_per_kw", "first-person plural (we/our/us) per 1000 words"),
    ("hedge_per_kw", "hedges per 1000 words"),
    ("booster_per_kw", "boosters per 1000 words"),
    ("connector_per_kw", "logical connectors per 1000 words"),
    ("past_aux_share", "past auxiliaries / (past+present) [was,were,had vs is,are,has,have]"),
    ("cite_per_100w", "citation groups per 100 words"),
    ("cited_sent_share", "share of sentences carrying a citation"),
    ("num_per_100w", "numerals per 100 words"),
    ("semicolon_per_kw", "semicolons per 1000 words"),
    ("dash_per_kw", "em-dashes per 1000 words"),
    ("this_start_share", "share of sentences starting This/These/It/There"),
    ("conn_start_share", "share of sentences starting with a connector"),
    ("word_len_mean", "mean word length (characters)"),
    ("mattr", "moving-average type-token ratio (window 100)"),
    ("ai_lex_per_kw", "AI-flavoured lexicon per 1000 words"),
]
MACRO_METRICS = [
    ("n_top_sections", "number of top-level sections (Intro..Conclusions)"),
    ("words_total", "words from Introduction to end of Conclusions"),
    ("intro_frac", "Introduction share of body words"),
    ("concl_frac", "Conclusions share of body words"),
    ("abstract_words", "abstract length (words)"),
    ("n_figs", "number of figures (max Fig. N)"),
    ("n_tables", "number of tables (max Table N)"),
    ("n_eqs", "number of numbered equations (est.)"),
    ("eq_per_kw", "numbered equations per 1000 body words"),
    ("concl_enumerated", "conclusions written as numbered/bulleted list (0/1)"),
]
# metrics only meaningful when the section has citations at all
SECTION_SKIP = {"conclusions": {"cite_per_100w", "cited_sent_share"}, "abstract": {"cite_per_100w", "cited_sent_share"}}

# ----------------------------------------------------------------------------- text loading


def read_any(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return "docx", docx_to_struct(path)
    raw = open(path, encoding="utf-8", errors="ignore").read()
    if ext == ".tex":
        return "tex", tex_to_struct(raw)
    if ext in (".md", ".markdown"):
        return "md", md_to_struct(raw)
    return "pdftxt", pdftxt_to_struct(raw)


def new_struct():
    return {"headings": [], "sections": {}, "order": [], "n_eqs": 0, "n_figs": 0, "n_tables": 0,
            "concl_enumerated": 0}


def classify_heading(h):
    h0 = re.sub(r"^[\dIVX]+(\.\d+)*\.?\s+", "", h.strip()).strip(" :.")
    if ABS_HEAD.match(h0) and len(h0) < 20:
        return "abstract", h0
    if INTRO_HEAD.match(h0):
        return "introduction", h0
    if CONCL_HEAD.match(h0):
        return "conclusions", h0
    if STOP_HEAD.match(h0):
        return "stop", h0
    return "other", h0


def assemble(blocks, st):
    """blocks: list of (kind, text) where kind in {'h1','h2','p','li'}; fills st sections."""
    cur = None
    body_on = False
    tops = []
    li_in_concl = 0
    for kind, txt in blocks:
        if kind == "h1":
            c, name = classify_heading(txt)
            if c == "abstract":
                cur = "abstract"
                continue
            if c == "introduction":
                if "conclusions" in st["order"]:
                    break  # duplicated document text (e.g. repository cover + manuscript)
                if tops and all(t.lower().startswith("introduction") for t in tops):
                    st["sections"].pop("introduction", None)  # repeated Introduction heading: restart
                    tops.clear()
                    st["order"].clear()
                body_on = True
            if c == "stop":
                cur = None
                if body_on:
                    body_on = False
                continue
            if c == "conclusions" and tops:
                body_on = True  # two-column PDFs may emit the reference list before the conclusions
            if body_on:
                tops.append(name)
                cur = c if c in ("introduction", "conclusions") else "other:" + name
                st["order"].append(cur)
            continue
        if kind == "h2":
            continue
        if cur is None:
            continue
        st["sections"].setdefault(cur, []).append(txt)
        if cur == "conclusions" and kind == "li":
            li_in_concl += 1
    st["headings"] = tops
    st["concl_enumerated"] = 1 if li_in_concl >= 2 else 0
    st["sections"] = {k: " ".join(v) for k, v in st["sections"].items()}
    ab = st["sections"].get("abstract")
    if ab is not None:
        ab = re.split(r"\b(?:Keywords?|Key words|K E Y W O R D S|Article history|A R T I C L E I N F O|Highlights)\b|©|\(c\) 20\d\d", ab)[0]
        if len(ab.split()) > 450 or len(ab.split()) < 40:
            st["sections"].pop("abstract")
        else:
            st["sections"]["abstract"] = ab
    return st


def md_to_struct(raw):
    st = new_struct()
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    st["n_eqs"] = len(re.findall(r"\$\$.+?\$\$", raw, flags=re.S))
    raw = re.sub(r"\$\$.+?\$\$", " ", raw, flags=re.S)
    blocks, para = [], []

    def flush():
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()
    for line in raw.splitlines():
        s = line.strip()
        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if m:
            flush()
            lvl = len(m.group(1))
            blocks.append(("h1" if lvl <= 2 else "h2", m.group(2)))
            continue
        if not s:
            flush()
            continue
        if re.match(r"^(\d+[.)]|\(\d+\)|\([ivx]+\)|[-*•])\s+", s):
            flush()
            blocks.append(("li", re.sub(r"^(\d+[.)]|\(\d+\)|\([ivx]+\)|[-*•])\s+", "", s)))
            continue
        para.append(s)
    flush()
    cleaned = []
    for k, t in blocks:
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
        t = re.sub(r"[*_`]", "", t)
        t = re.sub(r"\$[^$]+\$", "x", t)
        cleaned.append((k, t))
    st = assemble(cleaned, st)
    joined = " ".join(t for _, t in cleaned)
    st["n_figs"] = max_num(r"\bFig(?:ure|s?\.)\s*(\d+)", joined)
    st["n_tables"] = max_num(r"\bTable\s+(\d+)", joined)
    return st


def tex_to_struct(raw):
    st = new_struct()
    raw = re.sub(r"(?<!\\)%.*", "", raw)
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", raw, flags=re.S)
    if m:
        raw = m.group(1)
    st["n_eqs"] = len(re.findall(r"\\begin\{(equation|align|eqnarray|multline|gather)\}", raw))
    st["n_figs"] = len(re.findall(r"\\begin\{figure\*?\}", raw))
    st["n_tables"] = len(re.findall(r"\\begin\{table\*?\}", raw))
    raw = re.sub(r"\\begin\{(equation|align|eqnarray|multline|gather)\*?\}.*?\\end\{\1\*?\}", " ", raw, flags=re.S)
    raw = re.sub(r"\\begin\{(figure|table)\*?\}.*?\\end\{\1\*?\}", " ", raw, flags=re.S)
    raw = re.sub(r"\\\[.*?\\\]", " ", raw, flags=re.S)
    raw = raw.replace("\\begin{abstract}", "\n@@H1@@Abstract\n").replace("\\end{abstract}", "\n")
    raw = re.sub(r"\\(cite|citep|citet|parencite|textcite)\w*\*?(\[[^\]]*\])*\{[^}]*\}", "[1]", raw)
    raw = re.sub(r"\\(eq)?ref\{[^}]*\}", "1", raw)
    raw = re.sub(r"\$[^$]+\$", "x", raw)
    raw = re.sub(r"\\(section|chapter)\*?\{([^}]*)\}", lambda mm: "\n@@H1@@" + mm.group(2) + "\n", raw)
    raw = re.sub(r"\\(subsection|subsubsection|paragraph)\*?\{([^}]*)\}", lambda mm: "\n@@H2@@" + mm.group(2) + "\n", raw)
    raw = re.sub(r"\\item\s*(\[[^\]]*\])?", "\n@@LI@@", raw)
    raw = re.sub(r"\\begin\{(itemize|enumerate)\}|\\end\{(itemize|enumerate)\}", "\n", raw)
    for _ in range(3):
        raw = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", raw)
    raw = re.sub(r"\\[a-zA-Z]+\*?", " ", raw)
    raw = raw.replace("~", " ").replace("{", "").replace("}", "").replace("``", '"').replace("''", '"')
    raw = raw.replace("---", "—").replace("--", "–")
    blocks, para = [], []

    def flush():
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("@@H1@@"):
            flush(); blocks.append(("h1", s[6:])); continue
        if s.startswith("@@H2@@"):
            flush(); blocks.append(("h2", s[6:])); continue
        if s.startswith("@@LI@@"):
            flush(); blocks.append(("li", s[6:])); continue
        if not s:
            flush(); continue
        para.append(s)
    flush()
    return assemble(blocks, st)


def docx_to_struct(path):
    st = new_struct()
    paras = []
    try:
        import docx  # python-docx
        d = docx.Document(path)
        for p in d.paragraphs:
            sty = (p.style.name or "").lower() if p.style is not None else ""
            paras.append((sty, p.text))
    except Exception:
        x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8", "ignore")
        for p in re.findall(r"<w:p[ >].*?</w:p>", x, flags=re.S):
            sty = re.search(r'<w:pStyle w:val="([^"]+)"', p)
            t = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))
            paras.append(((sty.group(1) if sty else "").lower(), t))
    blocks = []
    for sty, t in paras:
        t = t.strip()
        if not t:
            continue
        if sty.startswith("heading 1") or sty in ("heading1", "title") or (len(t) < 40 and classify_heading(t)[0] in ("abstract", "introduction", "conclusions", "stop")):
            blocks.append(("h1", t))
        elif sty.startswith("heading"):
            blocks.append(("h2", t))
        elif "list" in sty or re.match(r"^(\d+[.)]|\(\d+\)|\([ivx]+\)|[-•])\s+", t):
            blocks.append(("li", t))
        else:
            blocks.append(("p", t))
    st = assemble(blocks, st)
    joined = " ".join(t for _, t in blocks)
    st["n_figs"] = max_num(r"\bFig(?:ure|s?\.)\s*(\d+)", joined)
    st["n_tables"] = max_num(r"\bTable\s+(\d+)", joined)
    return st


def max_num(pat, text):
    v = [int(x) for x in re.findall(pat, text) if int(x) < 100]
    return max(v) if v else 0


HEAD_NUM = re.compile(r"^\s*(\d{1,2})\.?\s+([A-Z][A-Za-z][A-Za-z0-9 ,:;&()'’/–\-]{1,80})$")
HEAD_PLAIN = re.compile(r"^\s*(Abstract|ABSTRACT|a\s?b\s?s\s?t\s?r\s?a\s?c\s?t|A B S T R A C T|Introduction|INTRODUCTION|"
                        r"Conclusions?|CONCLUSIONS?|Concluding [Rr]emarks|Summary and [Cc]onclusions?|"
                        r"Summary|References|REFERENCES|Acknowledg\w*|ACKNOWLEDG\w*|Appendix.*|APPENDIX.*|"
                        r"Declaration of [Cc]ompeting [Ii]nterest|CRediT authorship.*|Data availability)\s*\.?\s*$")


def pdftxt_to_struct(raw):
    """Heuristic structure recovery from pdftotext (reading-order) output."""
    st = new_struct()
    raw = raw.replace("\u00ad", "").replace("\ufb01", "fi").replace("\ufb02", "fl").replace("\x0c", "\n")
    lines = [ln.rstrip() for ln in raw.splitlines()]
    nonempty = [ln for ln in lines if ln.strip()]
    numbered = sum(1 for ln in nonempty if re.match(r"^\s*\d{1,2}\s+[A-Za-z(]", ln))
    if nonempty and numbered > 0.25 * len(nonempty):  # line-numbered review manuscript
        lines = [re.sub(r"^\s*\d{1,2}\s+(?=[A-Za-z(])", "", ln) for ln in lines]
    freq = {}
    for ln in lines:
        k = ln.strip()
        if len(k) > 3:
            freq[k] = freq.get(k, 0) + 1
    # drop running headers/footers (identical non-heading lines repeated on many pages)
    lines = ["" if (freq.get(ln.strip(), 0) >= 3 and not HEAD_PLAIN.match(ln.strip())) else ln for ln in lines]
    blocks = []
    para = []
    expected_next = 1
    seen_intro = False

    def flush():
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()

    def title_like(t):
        w = t.split()
        if not w or len(w) > 12 or not t[:1].isupper():
            return False
        if re.search(r"[.,;=<>]$|\d{3}", t):
            return False
        if w[-1].lower() in ("the", "of", "for", "and", "to", "a", "an", "in", "with", "by", "on", "at", "is", "are"):
            return False
        if re.match(r"^(Table|Fig|Figure|Step|Type|Case|Series|Specimen|Depth|Force|Load|Journal|Transactions|"
                    r"Professor|McCormick|Corresponding|E-mail|Email|Downloaded|Copyright)\b", t):
            return False
        if re.search(r"\((mm|kN|N|MPa|GPa|m|s|%|J/m2|N/m)\)|[=-]|Professor|University", t):
            return False
        if len([x for x in w if re.match(r"^[A-Za-z][a-z\-]{2,}", x)]) < 2 and not INTRO_HEAD.match(t) and not CONCL_HEAD.match(t):
            return False
        return sum(1 for x in w if re.match(r"[A-Za-z]", x)) >= max(1, len(w) - 2)

    in_concl = False
    skip = set()
    for i, ln in enumerate(lines):
        if i in skip:
            continue
        s = ln.strip()
        if not s:
            flush()
            continue
        m = HEAD_PLAIN.match(s.rstrip(":"))
        if m and len(s) < 60:
            flush()
            blocks.append(("h1", s.rstrip(":")))
            if INTRO_HEAD.match(s):
                seen_intro = True
                expected_next = 2
            in_concl = bool(CONCL_HEAD.match(s))
            continue
        ma = re.match(r"^\s*(Abstract|ABSTRACT)\s*[:.—–-]\s*(.+)", s)
        if ma:
            flush()
            blocks.append(("h1", "Abstract"))
            para.append(ma.group(2))
            continue
        # "N" alone on a line, title on the next non-empty line (arXiv / Springer layouts)
        mn = re.match(r"^\s*(\d{1,2})\.?\s*$", s)
        if mn and (not in_concl):
            n = int(mn.group(1))
            j = i + 1
            while j < len(lines) and j <= i + 3 and not lines[j].strip():
                j += 1
            if j < len(lines):
                nxt = lines[j].strip()
                ok_seq = (n == expected_next) if seen_intro else (n == 1)
                if ok_seq and title_like(nxt) and (n > 1 or INTRO_HEAD.match(nxt) or not seen_intro):
                    flush()
                    blocks.append(("h1", f"{n} {nxt}" if n > 1 or INTRO_HEAD.match(nxt) else "Introduction"))
                    skip.add(j)
                    if n == 1:
                        seen_intro = True
                    expected_next = n + 1
                    in_concl = bool(CONCL_HEAD.match(nxt))
                    continue
        m = HEAD_NUM.match(s)
        if m and title_like(m.group(2)) and not in_concl:
            n = int(m.group(1))
            title = m.group(2).rstrip(":")
            if INTRO_HEAD.match(title) or (n == 1 and not seen_intro):
                flush(); blocks.append(("h1", "Introduction")); seen_intro = True; expected_next = 2; continue
            if seen_intro and n in (expected_next, expected_next + 1):
                flush(); blocks.append(("h1", s)); expected_next = n + 1
                in_concl = bool(CONCL_HEAD.match(title)); continue
            if seen_intro and CONCL_HEAD.match(title):
                flush(); blocks.append(("h1", s)); expected_next = n + 1; in_concl = True; continue
        if re.match(r"^\s*\d{1,2}\.\d{1,2}\.?\s+[A-Z]", s) and len(s.split()) <= 14 and not s.endswith("."):
            flush(); blocks.append(("h2", s)); continue
        if re.match(r"^\s*(\(\d{1,2}\)|\d{1,2}[.)]|\([ivx]{1,4}\)|[•●▪–-])\s+[A-Za-z]", s) and len(s.split()) > 3:
            flush()
            blocks.append(("li", re.sub(r"^\s*(\(\d{1,2}\)|\d{1,2}[.)]|\([ivx]{1,4}\)|[•●▪–-])\s+", "", s)))
            continue
        if blocks and blocks[-1][0] == "li" and not para and s[:1].islower():
            k, t = blocks.pop()
            blocks.append((k, t + " " + s))
            continue
        if para and para[-1].endswith("-") and s[:1].islower():
            para[-1] = para[-1][:-1] + s
        else:
            para.append(s)
    flush()
    joined = raw
    st["n_figs"] = max_num(r"\bFig(?:ure|s?\.)\s*(\d+)", joined)
    st["n_tables"] = max_num(r"\bTable\s+(\d+)\b", joined)
    eqn = [int(x) for x in re.findall(r"^\s*\((\d{1,3})[a-z]?\)\s*$", raw, flags=re.M)]
    eqn += [int(x) for x in re.findall(r"\bEqs?\.\s*\(?(\d{1,3})\)?", raw)]
    eqn = [e for e in eqn if e < 150]
    st["n_eqs"] = max(eqn) if eqn else 0
    return assemble(blocks, st)


# ----------------------------------------------------------------------------- sentence-level metrics
_ABBR_TOKENS = {a: a.replace(".", "§") for a in ABBREV}


def clean_text(t):
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def split_sentences(t):
    t = clean_text(t)
    for a, b in _ABBR_TOKENS.items():
        t = t.replace(a, b)
    t = re.sub(r"\b([A-Z])\.\s(?=[A-Z])", r"\1§ ", t)  # initials
    t = re.sub(r"(\d)\.(\d)", r"\1§\2", t)
    parts = re.split(r"(?<=[.!?])[\"”’)]*\s+(?=[\"“(\[]?[A-Z0-9])", t)
    out = []
    for p in parts:
        p = p.replace("§", ".").strip()
        w = p.split()
        if len(w) < 5 or len(w) > 90:
            continue
        alpha = sum(1 for x in w if re.search(r"[A-Za-z]{2,}", x))
        if alpha / len(w) < 0.7:
            continue
        if re.match(r"^(Fig(ure)?s?\.?|Table)\s*\d", p):
            continue
        if not re.search(r"[.!?][\"”’)]*$", p):
            continue
        out.append(p)
    return out


WORD = re.compile(r"[A-Za-z][A-Za-z'’\-]*")
CITE_NUM = re.compile(r"\[\s*\d{1,3}(?:\s*[,–\-]\s*\d{1,3})*\s*\]")
CITE_AY = re.compile(r"\((?:[^()]*?(?:et al\.|and|&)?[^()]*?,?\s(?:19|20)\d\d[a-z]?)(?:;[^()]*?(?:19|20)\d\d[a-z]?)*\)")
CITE_NARR = re.compile(r"[A-Z][A-Za-z\-’']+(?: et al\.| and [A-Z][A-Za-z\-’']+)?\s\((?:19|20)\d\d[a-z]?\)")


def mattr(words, win=100):
    if len(words) < win:
        return len(set(words)) / max(1, len(words))
    vals = []
    step = 10
    for i in range(0, len(words) - win + 1, step):
        vals.append(len(set(words[i:i + win])) / win)
    return sum(vals) / len(vals)


def text_metrics(text):
    sents = split_sentences(text)
    if len(sents) < 3:
        return None
    joined = " ".join(sents)
    words = WORD.findall(joined)
    nw = max(1, len(words))
    lw = [w.lower() for w in words]
    lens = [len(WORD.findall(s)) for s in sents]
    kw = 1000.0 / nw
    low = joined.lower()
    conn = 0
    for c in CONNECTORS:
        conn += len(re.findall(r"(?<![a-z])" + re.escape(c) + r"(?![a-z])", low))
    past = len(re.findall(r"\b(was|were|had)\b", low))
    pres = len(re.findall(r"\b(is|are|has|have)\b", low))
    cites = len(CITE_NUM.findall(joined)) + len(CITE_AY.findall(joined)) + len(CITE_NARR.findall(joined))
    cited_s = sum(1 for s in sents if CITE_NUM.search(s) or CITE_AY.search(s) or CITE_NARR.search(s))
    nums = len(re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?(?![A-Za-z]*\])", joined))
    conn_start = sum(1 for s in sents if re.match(r"^(However|Moreover|Furthermore|Therefore|Thus|Hence|In addition|"
                                                  r"Consequently|Nevertheless|Accordingly|Similarly|Finally|In contrast|"
                                                  r"On the other hand|Additionally|Besides|Meanwhile|Overall)\b", s))
    m = {
        "sent_len_mean": statistics.mean(lens),
        "sent_len_sd": statistics.pstdev(lens),
        "long_sent_share": sum(1 for x in lens if x > 35) / len(lens),
        "passive_share": sum(1 for s in sents if PASSIVE.search(s)) / len(sents),
        "we_per_kw": len(re.findall(r"\b(we|our|us|ours|ourselves)\b", low)) * kw,
        "hedge_per_kw": len(re.findall(r"\b(" + HEDGES + r")\b", low)) * kw,
        "booster_per_kw": len(re.findall(r"\b(" + BOOSTERS + r")\b", low)) * kw,
        "connector_per_kw": conn * kw,
        "past_aux_share": past / (past + pres) if past + pres else 0.0,
        "cite_per_100w": cites * 100.0 / nw,
        "cited_sent_share": cited_s / len(sents),
        "num_per_100w": nums * 100.0 / nw,
        "semicolon_per_kw": joined.count(";") * kw,
        "dash_per_kw": joined.count("—") * kw,
        "this_start_share": sum(1 for s in sents if re.match(r"^(This|These|It|There)\b", s)) / len(sents),
        "conn_start_share": conn_start / len(sents),
        "word_len_mean": sum(len(w) for w in words) / nw,
        "mattr": mattr(lw),
        "ai_lex_per_kw": len(re.findall(r"\b(" + AI_WORDS + r")\b", low)) * kw,
        "_n_sent": len(sents),
        "_n_words": nw,
    }
    return m


def analyse(path_or_struct):
    if isinstance(path_or_struct, dict):
        st = path_or_struct
    else:
        _, st = read_any(path_or_struct)
    secs = st["sections"]
    body_keys = [k for k in st["order"] if k in secs]
    body_txt = " ".join(secs[k] for k in dict.fromkeys(body_keys))
    out = {"sections": {}, "macro": {}, "headings": st["headings"]}
    caps = {"abstract": 450, "introduction": 2600, "conclusions": 1200}  # longer = section boundary not recovered
    for name in ("abstract", "introduction", "conclusions"):
        if name in secs and len(WORD.findall(secs[name])) <= caps[name]:
            out["sections"][name] = text_metrics(secs[name])
    out["sections"]["body"] = text_metrics(body_txt) if body_txt else None
    wc = {k: len(WORD.findall(secs[k])) for k in dict.fromkeys(body_keys)}
    tot = sum(wc.values())
    if tot:
        out["macro"] = {
            "n_top_sections": len(st["headings"]),
            "words_total": tot,
            "intro_frac": wc.get("introduction", 0) / tot,
            "concl_frac": wc.get("conclusions", 0) / tot,
            "abstract_words": len(WORD.findall(secs.get("abstract", ""))),
            "n_figs": st["n_figs"],
            "n_tables": st["n_tables"],
            "n_eqs": st["n_eqs"],
            "eq_per_kw": st["n_eqs"] * 1000.0 / tot,
            "concl_enumerated": st["concl_enumerated"],
        }
    return out


# ----------------------------------------------------------------------------- corpus statistics

def pct(sorted_vals, q):
    if not sorted_vals:
        return float("nan")
    k = (len(sorted_vals) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def percentile_of(sorted_vals, x):
    if not sorted_vals:
        return float("nan")
    below = sum(1 for v in sorted_vals if v < x)
    equal = sum(1 for v in sorted_vals if v == x)
    return 100.0 * (below + 0.5 * equal) / len(sorted_vals)


def corpus_files():
    fs = sorted(f[:-4] for f in os.listdir(TEXT_DIR) if f.endswith(".txt"))
    return [k for k in fs if k not in HOLDOUT]


def band(vals):
    s = sorted(vals)
    return {"n": len(s), "p10": pct(s, 0.10), "p25": pct(s, 0.25), "p50": pct(s, 0.50), "p75": pct(s, 0.75),
            "p90": pct(s, 0.90), "mean": statistics.mean(s) if s else float("nan"), "values": s}


def score(res, stats, use_macro, sections=None):
    rows = []
    for sec in (sections or SECTIONS):
        m = res["sections"].get(sec)
        if not m:
            continue
        for key, _ in TEXT_METRICS:
            if key in SECTION_SKIP.get(sec, set()):
                continue
            b = stats["sections"].get(sec, {}).get(key)
            if not b or b["n"] < 5:
                continue
            x = m[key]
            rows.append((sec, key, x, percentile_of(b["values"], x), b["p10"], b["p90"], b["p10"] <= x <= b["p90"]))
    if use_macro and res["macro"]:
        for key, _ in MACRO_METRICS:
            b = stats["macro"].get(key)
            if not b or b["n"] < 5:
                continue
            x = res["macro"][key]
            rows.append(("macro", key, x, percentile_of(b["values"], x), b["p10"], b["p90"], b["p10"] <= x <= b["p90"]))
    sc = sum(1 for r in rows if r[6]) / len(rows) if rows else float("nan")
    return sc, rows


def build():
    per = {}
    for k in corpus_files():
        st = pdftxt_to_struct(open(os.path.join(TEXT_DIR, k + ".txt"), encoding="utf-8", errors="ignore").read())
        per[k] = {"res": analyse(st)}
    stats = {"corpus": sorted(per), "holdout": sorted(HOLDOUT), "sections": {}, "macro": {}, "per_paper": {}}
    for sec in SECTIONS:
        stats["sections"][sec] = {}
        for key, _ in TEXT_METRICS:
            vals = [p["res"]["sections"][sec][key] for p in per.values() if p["res"]["sections"].get(sec)]
            stats["sections"][sec][key] = band(vals)
    for key, _ in MACRO_METRICS:
        vals = [p["res"]["macro"][key] for p in per.values() if p["res"]["macro"] and p["res"]["macro"]["n_top_sections"] >= 3]
        stats["macro"][key] = band(vals)
    for k, p in per.items():
        r = p["res"]
        stats["per_paper"][k] = {"headings": r["headings"],
                                 "sections_found": [s for s in SECTIONS if r["sections"].get(s)],
                                 "macro": r["macro"],
                                 "metrics": {s: ({kk: round(v, 4) for kk, v in r["sections"][s].items()} if r["sections"].get(s) else None) for s in SECTIONS}}
    # leave-one-out self scores on introduction + conclusions (the GS reference)
    loo = {}
    for k, p in per.items():
        st2 = loo_stats(stats, k, per)
        sc, rows = score(p["res"], st2, False, ["introduction", "conclusions"])
        if rows:
            loo[k] = sc
    vals = sorted(loo.values())
    stats["loo_intro_concl_scores"] = loo
    stats["loo_median_score"] = pct(vals, 0.5) if vals else float("nan")
    json.dump(stats, open(STATS, "w"), indent=1)
    print(f"built stats.json from {len(per)} corpus papers (hold-outs excluded: {sorted(HOLDOUT)})")
    for sec in SECTIONS:
        n = stats["sections"][sec]["sent_len_mean"]["n"]
        print(f"  {sec:13s} n={n}")
    print(f"  LOO median score (intro+concl) = {stats['loo_median_score']:.3f}; GS threshold (90%) = {0.9 * stats['loo_median_score']:.3f}")


def loo_stats(stats, drop, per):
    st2 = {"sections": {}, "macro": {}}
    for sec in SECTIONS:
        st2["sections"][sec] = {}
        for key, _ in TEXT_METRICS:
            vals = [p["res"]["sections"][sec][key] for kk, p in per.items() if kk != drop and p["res"]["sections"].get(sec)]
            st2["sections"][sec][key] = band(vals)
    return st2


# ----------------------------------------------------------------------------- CLI

def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    if a[0] == "--build":
        build()
        return
    stats = json.load(open(STATS))
    if a[0] == "--selftest":
        for k, v in sorted(stats["loo_intro_concl_scores"].items(), key=lambda kv: kv[1]):
            print(f"{k:24s} {v:.3f}")
        print("median", round(stats["loo_median_score"], 3))
        return
    path = a[0]
    res = analyse(path)
    st_full = len(res["headings"]) >= 4 or "--full" in a
    # excerpts (fewer than 4 top-level sections): body == intro+concl, so score the named sections only
    secs = None if st_full else ["abstract", "introduction", "conclusions"]
    if "--sections" in a:
        secs = a[a.index("--sections") + 1].split(",")
    sc, rows = score(res, stats, st_full, secs)
    ref = stats["loo_median_score"]
    if "--json" in a:
        print(json.dumps({"score": sc, "corpus_median": ref, "gs_threshold": 0.9 * ref,
                          "rows": rows, "headings": res["headings"]}, indent=1))
        return
    print(f"# style_check  efm-sizeeffect  file={os.path.basename(path)}")
    print(f"headings: {res['headings']}")
    names = dict(TEXT_METRICS + MACRO_METRICS)
    cur = None
    for sec, key, x, p, lo, hi, ok in rows:
        if sec != cur:
            cur = sec
            n = (res["sections"].get(sec) or {}).get("_n_words", "")
            print(f"\n[{sec}] words={n}")
        flag = "ok " if ok else "OUT"
        print(f"  {flag} {key:18s} {x:9.3f}  pct={p:5.1f}  band=[{lo:.3f}, {hi:.3f}]  -- {names[key]}")
    print(f"\nSCORE = {sc:.3f}  ({sum(1 for r in rows if r[6])}/{len(rows)} metrics inside corpus P10-P90)")
    print(f"corpus LOO median (intro+concl) = {ref:.3f}; GS threshold = {0.9 * ref:.3f}; "
          f"{'PASS' if sc >= 0.9 * ref else 'below threshold'}")


if __name__ == "__main__":
    main()
