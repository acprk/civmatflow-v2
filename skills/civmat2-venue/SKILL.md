---
name: civmat2-venue
description: civmatflow v2 V0——给定一组土木材料一/二区期刊，统计近 3 年非实验类 topic 的频次/增长/拥挤度，并抽样录用稿做理论深度标定（公式数、推导类型、留出与 baseline 数）。新方向选题前使用。
---

# V0 期刊画像 + 理论深度标定

## 输入
期刊清单（默认 CCR、CCC、CBM、Composites B、M&S、JBE、JMCE、CSCM、EFM、Mech Mater、MCR、Struct Concr、JACT）。

## 步骤
1. 题录：OpenAlex（免费额度易 429，可等 UTC 0 点或用户 key）→ 回退 Crossref（Elsevier 无摘要，仅标题）。原始 JSON 存 `venue/raw/`，脚本存 `venue/scripts/`。
2. 分类：实验 / 计算-理论 / 纯 ML / 综述；人工抽查 ≥50 篇并报告判对率。只按标题时注明精度（0970 实测 ±30 点）。
3. topic 聚类：每类给各刊各年篇数、增长倍数（近两年占比 ÷ 前两年占比）、纯 ML 篇数、被引中位数、代表作 DOI。
4. 理论深度标定：每刊抽 10–15 篇 OA 录用稿（无新试验），量：编号公式数、推导类型、正文/附录推导、数据集数与来源、真留出、baseline 重跑数、指标、页数图表数。产出"目标深度带"。
5. 产出：`venue/topic_map.md`、`venue/theory_depth.md`。

## 已有结果（0970，2026-10-27）
目标带：正文 15–30 式（中位 18）、1 条机理新关系（4–10 步）、≥3 数据集且 ≥1 真留出、≥2 baseline 同数据重跑、RMSE+均值比/CoV、~20 页、10–15 图；仅 9/40 有真留出、13/40 有 ≥2 baseline。
