---
name: civmat2-lit
description: civmatflow v2 V2–V3——合法渠道检索与全文获取（OA 链 → 用户自供），PDF 本地压缩为文献卡（方程、数据集、指标数值+页码），建立 baseline 台账。后续 agent 只读卡片不读 PDF。
---

# V2 检索 + V3 本地压缩

## 获取（`civmat2 fetch DOI [DOI…] --out <ws>/lit/pdfs --email <addr>`，或 `--from-file dois.txt`）
回退顺序：Unpaywall（需 email）→ OpenAlex best_oa_location → Semantic Scholar openAccessPdf → arXiv → CORE（仅当 `~/.config/core.key`）→ Elsevier TDM（仅当 `~/.config/elsevier.key` 且 10.1016/）→ 写入 `lit/pdfs/NEED_FROM_USER.md`。每次尝试与 HTTP 状态记在 `fetch_log.jsonl`，成功件的许可记在 `LICENSES.tsv`。`--list` 只列候选不下载。禁止影子图书馆。

## 压缩（`civmat2 cards <ws>/lit/pdfs --cards <ws>/lit/cards`）
1. pdftotext / PyMuPDF 抽文本到 `lit/text/`。
2. 每篇一张卡 `lit/cards/<firstauthor_year>.md`（模板 `civmat2 template LIT_CARD`）：问题｜模型方程（LaTeX，标原式号）｜数据集（来源/条数/许可）｜指标与数值（页码/表号）｜作者自述局限｜代码链接｜与本方向关系｜状态（FULLTEXT / ABSTRACT-ONLY=UNVERIFIED）。脚本只生成骨架、DOI 猜测和候选数值行，方程与数值由 agent 对照原文填写。
3. 抽查：每方向随机 3 个数值回原文核对，记录在卡片底部。

## baseline 台账 `BASELINES.md`（模板 `civmat2 template BASELINES`）
每方向：SOTA 模型、数据、报告误差（指标+值+出处）、可复现性（代码？参数全？）、已知失效区、拥挤度。

## 查新（G0.5 与投稿前）
最近 24 个月 + 被引 + 作者后续 + 期刊正式版 + Zenodo/figshare/MDPI；给出最接近 3 篇的逐项对比；负面检索结论要写明覆盖范围与限制（如 OpenAlex 429）。关键竞品不可合法读取 → 在报告中标为"阻断项"。
