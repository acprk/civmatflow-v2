---
name: civmat2-package
description: civmatflow v2 V11——把通过 G4 的方向封装成可投稿包（沿用 0961 ES 投稿包结构）：01–07 上传件 + 07_Supplementary_data_and_code.zip（原始数据或下载脚本+sha256、处理后数据、全部结果、代码与 run_all）+ 00_作者参考_勿上传 + 清单与哈希，打成 zip+sha256。
---

# V11 投稿包

运行：`python /home/luck/xzy/0970project/civmatflow2/tools/build_package.py --ws <方向工作区> --name <方向中文名> --journal <期刊>`
它会按下面的结构收集文件、检查缺项、生成 PACKAGE_MANIFEST_sha256.json 与 zip+sha256；缺项不报错而列进 README 的待办。

```
submit/
  01_Cover_Letter_DRAFT.docx  02_Highlights.docx  03_Manuscript.docx
  04_Graphical_abstract.pdf|tif  05_Figures/  06_Supplementary_Material.pdf
  07_Supplementary_data_and_code.zip
      data/raw/<dataset>/ (许可允许再分发才放原件，否则 download.sh + sha256 + 引用)
      data/processed/  results/  code/  run_all.sh  expected_output/  README.md  LICENSE
  PACKAGE_MANIFEST_sha256.json   README_投稿上传顺序与作者待办.md
  00_作者参考_勿上传/
      CLAIM_EVIDENCE.csv NUMBERS_USED.json NUMBER_CHECK.md CITATION_CHECK.md
      PREREG.md(+sha256) BASELINES.md FALSIFY.md review/ response_table.md
      作者待办.md 推荐审稿人候选_待作者核实.md LaTeX_source/ Rebuild_scripts/
```

## 投稿前清单
G1–G4 全过｜数字核查不一致=0｜文献 DOI 全部可解析（refcheck）｜期刊格式（篇幅/图数/参考文献）｜摘要/亮点只含已验证结论｜数据许可核对（CC BY-NC 数据不得随包再分发）｜作者信息/基金/利益冲突/AI 声明由作者填写｜同一数据未一稿多投｜对外提交须作者本人操作。
