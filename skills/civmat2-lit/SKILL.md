---
name: civmat2-lit
description: civmatflow v2 V2–V3——合法渠道检索与全文获取（OA 链 → 用户自供），PDF 本地压缩为文献卡（方程、数据集、指标数值+页码），建立 baseline 台账。后续 agent 只读卡片不读 PDF。
---

# V2 检索 + V3 本地压缩

## 获取（`tools/fetch_fulltext.py DOI [DOI…] --out lit/pdfs/<dir>`）
回退顺序：Unpaywall → OpenAlex best_oa_location → Semantic Scholar openAccessPdf → arXiv → Elsevier TDM（仅当 `~/.config/elsevier.key` 存在）→ 写入 `lit/NEED_FROM_USER.md`。记录每次尝试与 HTTP 状态到 `lit/fetch_log.jsonl`。禁止影子图书馆。

## 压缩（`tools/pdf2cards.py lit/pdfs/<dir> --cards lit/cards/<dir>`）
1. pdftotext / PyMuPDF 抽文本到 `lit/text/`。
2. 每篇一张卡 `lit/cards/<dir>/<firstauthor_year>.md`：问题｜模型方程（LaTeX，标原式号）｜数据集（来源/条数/许可）｜指标与数值（页码/表号）｜作者自述局限｜代码链接｜状态（FULLTEXT / ABSTRACT-ONLY=UNVERIFIED）。脚本只生成骨架和候选数值行，方程与数值由 agent 对照原文填写。
3. 抽查：每方向随机 3 个数值回原文核对，记录在卡片底部。

## baseline 台账 `BASELINES.md`
每方向：SOTA 模型、数据、报告误差（指标+值+出处）、可复现性（代码？参数全？）、已知失效区、拥挤度。
