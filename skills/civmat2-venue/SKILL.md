---
name: civmat2-venue
description: civmatflow v2 V0——给定一组土木材料一/二区期刊，统计近 3 年非实验类 topic 的频次/增长/拥挤度，并抽样录用稿做理论深度标定（公式数、推导类型、留出与 baseline 数）。新方向选题前使用。
---

# V0 期刊画像 + 理论深度标定

## 输入
期刊清单（默认 CCR、CCC、CBM、Composites B、M&S、JBE、JMCE、CSCM、EFM、Mech Mater、MCR、Struct Concr、JACT；`civmat2 venue journals` 打印内置 ISSN 表，使用前核对）。

## 步骤
1. 题录：`civmat2 venue fetch --journals all --years <Y1-Y3> --out {{CIVMAT2_PROJECT}}/venue --mailto <email>`（Crossref；Elsevier 无摘要，仅标题）。需要摘要时 `--source openalex`（免费额度易 429，可等 UTC 0 点或用 key）。原始 JSONL 存 `venue/raw/`。
2. 分类：`civmat2 venue classify --out {{CIVMAT2_PROJECT}}/venue --sample 60` 生成 `classified.csv`、`topic_map.md`、`sample_for_manual_check.csv`；**人工填写 ≥50 条 manual_class**，`civmat2 venue score --sample …` 得判对率，写在 topic_map.md 顶部。只按标题时注明精度（0970 实测 ±30 点）。
3. topic 聚类：`topic_map.md` 已给各 topic 各刊各年篇数、增长倍数（后半段占比 ÷ 前半段占比）、纯 ML 占比、被引中位数、代表作 DOI；需要新 topic 时改 `tools/venue_profile.py` 的 TOPICS 词表并重跑。
4. 理论深度标定：每刊抽 10–15 篇 OA 录用稿（无新试验），`civmat2 fetch` 取全文、`civmat2 cards` 抽文本后 `civmat2 depth {{CIVMAT2_PROJECT}}/venue/depth_corpus/text --out {{CIVMAT2_PROJECT}}/venue/theory_depth_tally` 得公式/图表/页数等计数；再逐篇阅读填 CSV 中的 derivation_type、true_holdout、n_baselines_rerun、n_datasets。产出"目标深度带"。
5. 产出：`venue/topic_map.md`、`venue/theory_depth.md`（人读后的结论，引用 tally 表）。

## 已有结果（0970，2026-10-27）
目标带：正文 15–30 式（中位 18）、1 条机理新关系（4–10 步）、≥3 数据集且 ≥1 真留出、≥2 baseline 同数据重跑、RMSE+均值比/CoV、~20 页、10–15 图；仅 9/40 有真留出、13/40 有 ≥2 baseline。
