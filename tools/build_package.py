#!/usr/bin/env python3
"""Assemble a civmatflow v2 submission package (the 0961 ES layout).

Collects files from a direction workspace into <ws>/submit/, lists missing items
(never fabricates them), builds 07_Supplementary_data_and_code.zip, writes
PACKAGE_MANIFEST_sha256.json and the upload-order README, then zips submit/ to
<out>/投稿包_<name>_<YYYYMMDD>.zip with a .sha256 file next to it.

Expected (all optional) inputs
  <ws>/paper/   cover_letter.docx, highlights.docx, manuscript.docx (or main.pdf),
                graphical_abstract.(pdf|tif), figures/, supplementary.pdf,
                CLAIM_EVIDENCE.csv, NUMBERS_USED.json, NUMBER_CHECK.md, CITATION_CHECK.md,
                作者待办.md, 推荐审稿人候选_待作者核实.md, latex/
  <ws>/data/raw/<dataset>/PROVENANCE.md   (only redistributable licences are copied;
                others get provenance + download instructions only)
  <ws>/data/processed, <ws>/results, <ws>/code (with run_all.sh), <ws>/expected_output
  <ws>/PREREG.md (+ PREREG.sha256, FROZEN_MANIFEST.json), <ws>/HOLDOUT/, <ws>/BASELINES.md,
  <ws>/FALSIFY.md, <ws>/review/

Usage: build_package.py --ws DIR --name 中文名 --journal NAME [--out DIR] [--no-zip]
Standard library only.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import shutil
import zipfile

NONREDIST = ("BY-NC", "BY-ND", "ODbL", "all rights reserved", "no licence", "no license",
             "not redistributable", "redistribution: no", "permission required")


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


def zip_dir(root, out, prefix=None):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                rel = p.relative_to(root)
                z.write(p, pathlib.Path(prefix) / rel if prefix else rel)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ws", required=True, help="direction workspace")
    ap.add_argument("--name", required=True, help="direction name used in the zip file name")
    ap.add_argument("--journal", required=True)
    ap.add_argument("--out", default=None, help="where the final zip goes (default: parent of --ws)")
    ap.add_argument("--no-zip", action="store_true", help="only build submit/, do not zip")
    a = ap.parse_args()
    ws = pathlib.Path(a.ws).resolve()
    paper = ws / "paper"
    sub = ws / "submit"
    if sub.exists():
        shutil.rmtree(sub)
    ref = sub / "00_作者参考_勿上传"
    missing = []
    copy(paper / "cover_letter.docx", sub / "01_Cover_Letter_DRAFT.docx", missing, "01 cover letter")
    copy(paper / "highlights.docx", sub / "02_Highlights.docx", missing, "02 highlights")
    man = first(paper / "manuscript.docx", paper / "main.pdf", paper / "manuscript.pdf")
    copy(man, sub / ("03_Manuscript" + man.suffix), missing, "03 manuscript")
    ga = first(paper / "graphical_abstract.pdf", paper / "graphical_abstract.tif", paper / "graphical_abstract.png")
    copy(ga, sub / ("04_Graphical_abstract" + ga.suffix), missing, "04 graphical abstract")
    copy(paper / "figures", sub / "05_Figures", missing, "05 figures")
    copy(paper / "supplementary.pdf", sub / "06_Supplementary_Material.pdf", missing, "06 supplementary")

    # 07 data and code
    stage = ws / "_pkg07"
    if stage.exists():
        shutil.rmtree(stage)
    lic_notes = []
    raw = ws / "data" / "raw"
    if raw.exists() and any(p.is_dir() for p in raw.iterdir()):
        for d in sorted(p for p in raw.iterdir() if p.is_dir()):
            prov = d / "PROVENANCE.md"
            text = prov.read_text(errors="ignore") if prov.exists() else "no licence"
            dst = stage / "data" / "raw" / d.name
            if not prov.exists():
                missing.append(f"data/raw/{d.name}/PROVENANCE.md")
            if any(k.lower() in text.lower() for k in NONREDIST):
                dst.mkdir(parents=True, exist_ok=True)
                if prov.exists():
                    shutil.copy2(prov, dst / "PROVENANCE.md")
                for extra in ("download.sh", "download.py", "sha256sum.txt", "SHA256SUMS"):
                    if (d / extra).exists():
                        shutil.copy2(d / extra, dst / extra)
                lic_notes.append(f"{d.name}: not redistributed (licence) — provenance + download instructions only")
            else:
                shutil.copytree(d, dst, dirs_exist_ok=True)
    else:
        missing.append("data/raw")
    for part in ("data/processed", "results", "code", "expected_output"):
        copy(ws / part, stage / part, missing, part)
    if not (stage / "code" / "run_all.sh").exists() and not (stage / "run_all.sh").exists():
        missing.append("code/run_all.sh")
    for f in ("LICENSE", "README.md"):
        if (ws / "code" / f).exists():
            shutil.copy2(ws / "code" / f, stage / f)
    if not (stage / "LICENSE").exists():
        missing.append("code/LICENSE")
    (stage / "README.md").write_text(
        f"# Supplementary data and code — {a.name}\n\nTarget journal: {a.journal}\n\n"
        "Run `code/run_all.sh` from this directory; outputs are compared with `expected_output/`.\n\n"
        "Licence notes:\n" + ("\n".join(f"- {n}" for n in lic_notes) or "- all raw data redistributable under their stated licences") + "\n",
        encoding="utf-8")
    z7 = sub / "07_Supplementary_data_and_code.zip"
    z7.parent.mkdir(parents=True, exist_ok=True)
    zip_dir(stage, z7)
    shutil.rmtree(stage)

    # author reference (never uploaded)
    for f in ("CLAIM_EVIDENCE.csv", "NUMBERS_USED.json", "NUMBER_CHECK.md", "CITATION_CHECK.md",
              "作者待办.md", "推荐审稿人候选_待作者核实.md"):
        copy(paper / f, ref / f, missing, f)
    for f in ("PREREG.md", "PREREG.sha256", "FROZEN_MANIFEST.json", "BASELINES.md", "FALSIFY.md", "DIRECTION.md"):
        copy(ws / f, ref / f, missing, f)
    for f in ("split.json", "HOLDOUT_CONSUMED", "evaluations.log"):
        if (ws / "HOLDOUT" / f).exists():
            copy(ws / "HOLDOUT" / f, ref / "HOLDOUT" / f, missing, f)
    if not (ws / "HOLDOUT" / "HOLDOUT_CONSUMED").exists():
        missing.append("HOLDOUT/HOLDOUT_CONSUMED (hold-out not evaluated?)")
    copy(ws / "review", ref / "review", missing, "review/")
    copy(paper / "latex", ref / "LaTeX_source", missing, "LaTeX source")
    copy(ws / "code", ref / "Rebuild_scripts", missing, "Rebuild_scripts (code/)")

    manifest = {str(p.relative_to(sub)): sha(p) for p in sorted(sub.rglob("*")) if p.is_file()}
    (sub / "PACKAGE_MANIFEST_sha256.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    (sub / "README_投稿上传顺序与作者待办.md").write_text(
        f"# {a.name} — 投稿包（{a.journal}）\n\n生成时间：{datetime.datetime.now():%Y-%m-%d %H:%M}\n\n"
        "上传顺序：01 → 02 → 03 → 04 → 05 → 06 → 07（`00_作者参考_勿上传/` 不上传）。\n\n"
        "## 缺项（由作者或后续步骤补齐；脚本不编造）\n" + ("\n".join(f"- [ ] {m}" for m in missing) or "- 无") +
        "\n\n## 数据许可\n" + ("\n".join(f"- {n}" for n in lic_notes) or "- 全部原始数据许可允许再分发") +
        "\n\n## 作者须填（黄色占位）\n- [ ] 作者与单位、通讯作者、ORCID\n- [ ] 基金\n- [ ] 利益冲突\n- [ ] AI 使用声明\n"
        "- [ ] 数据可用性声明核对（与 07 包一致）\n- [ ] 推荐审稿人核实\n- [ ] 对外提交由作者本人操作\n",
        encoding="utf-8")
    result = {"submit_dir": str(sub), "files": len(manifest), "missing": missing, "licence_notes": lic_notes}
    if not a.no_zip:
        out_dir = pathlib.Path(a.out).resolve() if a.out else ws.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        day = datetime.date.today().strftime("%Y%m%d")
        out = out_dir / f"投稿包_{a.name}_{day}.zip"
        zip_dir(sub, out, prefix="submit")
        out.with_suffix(".zip.sha256").write_text(f"{sha(out)}  {out.name}\n")
        result["package"] = str(out)
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
