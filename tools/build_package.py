#!/usr/bin/env python3
"""Assemble a civmatflow v2 submission package (0961 ES layout).

Collects files from a direction workspace into <ws>/submit/, lists missing items
(never fabricates them), builds 07_Supplementary_data_and_code.zip, writes
PACKAGE_MANIFEST_sha256.json and README, then zips submit/ to
/home/luck/xzy/0970project/投稿包_<name>_<YYYYMMDD>.zip with a .sha256.

Expected (optional) inputs in <ws>/paper/: cover_letter.docx, highlights.docx,
manuscript.docx (or main.pdf), graphical_abstract.(pdf|tif), figures/, supplementary.pdf,
CLAIM_EVIDENCE.csv, NUMBERS_USED.json, NUMBER_CHECK.md, CITATION_CHECK.md, 作者待办.md, latex/.
Data/code: <ws>/data/raw (only redistributable licences), <ws>/data/processed, <ws>/results,
<ws>/code (with run_all.sh), <ws>/expected_output. Prereg/review: <ws>/PREREG.md(+.sha256),
<ws>/BASELINES.md, <ws>/FALSIFY.md, <ws>/review/.

Usage: build_package.py --ws DIR --name 中文名 --journal NAME
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import shutil
import zipfile

NONREDIST = ("BY-NC", "BY-ND", "ODbL", "all rights reserved", "no licence", "no license")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def copy(src, dst, missing, label):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
        return True
    missing.append(label)
    return False


def first(*paths):
    for p in paths:
        if p.exists():
            return p
    return paths[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--journal", required=True)
    a = ap.parse_args()
    ws = pathlib.Path(a.ws)
    paper = ws / "paper"
    sub = ws / "submit"
    if sub.exists():
        shutil.rmtree(sub)
    ref = sub / "00_作者参考_勿上传"
    missing = []
    copy(paper / "cover_letter.docx", sub / "01_Cover_Letter_DRAFT.docx", missing, "01 cover letter")
    copy(paper / "highlights.docx", sub / "02_Highlights.docx", missing, "02 highlights")
    man = first(paper / "manuscript.docx", paper / "main.pdf")
    copy(man, sub / ("03_Manuscript" + man.suffix), missing, "03 manuscript")
    ga = first(paper / "graphical_abstract.pdf", paper / "graphical_abstract.tif")
    copy(ga, sub / ("04_Graphical_abstract" + ga.suffix), missing, "04 graphical abstract")
    copy(paper / "figures", sub / "05_Figures", missing, "05 figures")
    copy(paper / "supplementary.pdf", sub / "06_Supplementary_Material.pdf", missing, "06 supplementary")

    # 07 data and code
    stage = ws / "_pkg07"
    if stage.exists():
        shutil.rmtree(stage)
    lic_notes = []
    raw = ws / "data" / "raw"
    if raw.exists():
        for d in sorted(p for p in raw.iterdir() if p.is_dir()):
            prov = d / "PROVENANCE.md"
            text = prov.read_text(errors="ignore") if prov.exists() else "no licence"
            if any(k.lower() in text.lower() for k in NONREDIST):
                (stage / "data" / "raw" / d.name).mkdir(parents=True, exist_ok=True)
                if prov.exists():
                    shutil.copy2(prov, stage / "data" / "raw" / d.name / "PROVENANCE.md")
                lic_notes.append(f"{d.name}: not redistributed (licence) — provenance + download instructions only")
            else:
                shutil.copytree(d, stage / "data" / "raw" / d.name, dirs_exist_ok=True)
    else:
        missing.append("data/raw")
    for part in ("data/processed", "results", "code", "expected_output"):
        copy(ws / part, stage / part, missing, part)
    if not (stage / "code" / "run_all.sh").exists() and not (stage / "run_all.sh").exists():
        missing.append("run_all.sh")
    (stage / "README.md").write_text(f"# Supplementary data and code — {a.name}\n\nLicence notes:\n" +
                                     "\n".join(f"- {n}" for n in lic_notes) + "\n")
    z7 = sub / "07_Supplementary_data_and_code.zip"
    z7.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(z7, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(stage.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(stage))
    shutil.rmtree(stage)

    # author reference
    for f in ("CLAIM_EVIDENCE.csv", "NUMBERS_USED.json", "NUMBER_CHECK.md", "CITATION_CHECK.md", "作者待办.md"):
        copy(paper / f, ref / f, missing, f)
    for f in ("PREREG.md", "PREREG.sha256", "BASELINES.md", "FALSIFY.md"):
        copy(ws / f, ref / f, missing, f)
    copy(ws / "review", ref / "review", missing, "review/")
    copy(paper / "latex", ref / "LaTeX_source", missing, "LaTeX source")

    manifest = {str(p.relative_to(sub)): sha(p) for p in sorted(sub.rglob("*")) if p.is_file()}
    (sub / "PACKAGE_MANIFEST_sha256.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    (sub / "README_投稿上传顺序与作者待办.md").write_text(
        f"# {a.name} — 投稿包（{a.journal}）\n\n上传顺序：01→07（00_作者参考_勿上传 不上传）。\n\n"
        "## 缺项（由作者或后续步骤补齐，未编造）\n" + "\n".join(f"- [ ] {m}" for m in missing) +
        "\n\n## 数据许可\n" + ("\n".join(f"- {n}" for n in lic_notes) or "- 全部原始数据许可允许再分发") +
        "\n\n## 作者须填\n- [ ] 作者与单位、通讯作者\n- [ ] 基金\n- [ ] 利益冲突\n- [ ] AI 使用声明\n- [ ] 数据可用性声明核对\n- [ ] 对外提交由作者本人操作\n")
    day = datetime.date.today().strftime("%Y%m%d")
    out = pathlib.Path("/home/luck/xzy/0970project") / f"投稿包_{a.name}_{day}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(sub.rglob("*")):
            if p.is_file():
                z.write(p, pathlib.Path("submit") / p.relative_to(sub))
    out.with_suffix(".zip.sha256").write_text(f"{sha(out)}  {out.name}\n")
    print(json.dumps({"package": str(out), "files": len(manifest), "missing": missing}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
