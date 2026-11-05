# civmatflow v2 分阶段 runbook

每一阶段：**输入 → 命令/agent → 产出 → 闸门**。路径约定：`$HOME`=本仓库（`civmat2 home`），`$PROJECT`=研究工作区，`<ws>`=方向工作区（`civmat2 init <ws>` 生成）。所有阶段都遵守总纲 `skills/civmat2/SKILL.md` 的 15 条教训与纪律。

## V0 期刊画像 + 理论深度标定（skill `civmat2-venue`，agent `civmat-scout`）
1. `civmat2 venue fetch --journals all --years 2023-2025 --out $PROJECT/venue --mailto <email>`
2. `civmat2 venue classify --out $PROJECT/venue --sample 60` → 人工填 `sample_for_manual_check.csv` → `civmat2 venue score` 得判对率，写入 `topic_map.md` 顶部。
3. 每刊抽 10–15 篇无新试验的 OA 录用稿：`civmat2 fetch`、`civmat2 cards`、`civmat2 depth $PROJECT/venue/depth_corpus/text --out $PROJECT/venue/theory_depth_tally`，逐篇阅读补 derivation_type / true_holdout / n_baselines_rerun。
4. 产出 `venue/topic_map.md`、`venue/theory_depth.md`（目标深度带）。无闸门。

## V1 方向筛选（skill `civmat2-direction`，agents `civmat-scout` + `civrev-adversary`，workflow `civmat2-direction.js`）
1. 收割候选卡（`civmat2 template DIRECTION_CARD`）：读障碍不读主题。
2. **G0**：真下载到 `$PROJECT/data/raw/<slug>/`，写 PROVENANCE.md（`civmat2 template PROVENANCE`）+ sha256；登录墙不绕过。
3. **G0.5 抢先扫描**（先于 G1）：近 24 个月论文/预印本/Zenodo/MDPI/被引/作者后续，关键竞品读全文；已有等价工作 → 关闭。
4. **可检测性**：有 baseline 预测时 `civmat2 residuals … --out results/` 看 ICC(1)；SWAMPED 且无组内对比 → 改走模拟真值路线或关闭。
5. 补刀：civrev-adversary 攻击每张存活卡。
6. 产出 `<ws>/DIRECTION.md`（主/备）与 `$PROJECT/codex/STATUS.md` 的关闭记录。

## V2–V3 文献检索与本地压缩（skill `civmat2-lit`，agent `civmat-librarian`）
1. `civmat2 fetch <DOIs> --out <ws>/lit/pdfs --email <email>`；失败项自动进 `NEED_FROM_USER.md`（用户不提供付费文献 → 标"阻断项"）。
2. `civmat2 cards <ws>/lit/pdfs --cards <ws>/lit/cards`；agent 对照原文填方程（式号）与数值（页/表），每方向抽 3 个数值回查。
3. `<ws>/BASELINES.md`（`civmat2 template BASELINES`）。闸门：卡片数值抽查通过。

## V2s 风格蒸馏（agent `civmat-style-distiller` → `<key>-writer`）
与 V2 并行。A 层 20–40 篇 + B 层 10–20 篇（合法渠道），3 篇留出；产出 `style/<key>/{CORPUS,STYLE,phrasebank}.md`、`style_check.py`、`stats.json`，写作 agent `agents/<key>-writer.md`，`style/INDEX.md` 加一行。**GS**：留出段重写后 `civmat2 style <key>` 分数 ≥ LOO 中位数 90 %，civrev-writing 盲判按修订标准。已有：`efm-sizeeffect`、`ms-cemchem`。

## V4 SOTA 复现（skill `civmat2-sota`，agent `civmat-theorist`，审计 `civrev-experiment`，workflow `civmat2-sota.js`）
1. **先冻结**：`civmat2 holdout freeze --data <ws>/data/processed/tidy.csv --group source --seed <s> --out <ws>/HOLDOUT`。
2. 所有脚本 `from holdout_guard import load_calibration`；导出文件 `civmat2 holdout check`。
3. 按原文式号实现，先对官方算例；同子集同指标复现原文误差 ±10 %（否则逐项解释；原文选集不可重建时用自己的显式选集）。
4. `civmat2 residuals <calibration.csv> --obs y --pred B0,B1 --source source --by <物理变量> --out <ws>/results --log`。
5. `<ws>/notes/G1_REPORT.md`（`civmat2 template G1_REPORT`）；civrev-experiment 新上下文审计。**G1**：复现 ±10 %、留出冻结且零重叠、残差只用校准集、可检测性已判定。

## V5 idea + 证伪（skill `civmat2-idea`，agent `civmat-theorist` + `civrev-adversary`，workflow `civmat2-idea.js` stage ideate）
1. 从 `results/residual_map.md` 的失效区出发：≤3 个物理解释 → ≥2 个竞争模型 + 1 个纯重标定对照。
2. 方程：≤ baseline + 2 参数；正文级推导 4–10 步；sympy 自检存 `ideas/checks/`；拟合前查可辨识性；查新 3 篇。
3. 先写 `ideas/<slug>.FALSIFY.md`，civrev-adversary ≥5 条路线攻击，攻击记录写回。**G2**：至少一条存活、可辨识、可检测、新颖、有可检验预言。

## V6 预注册 + 一次性留出（skill `civmat2-prereg`）
1. `PREREG.md`（`civmat2 template PREREG`）：模型清单、数据与 split 哈希、主/次指标、胜出判据（来源 bootstrap CI）、分层判据、杀伤规则、排除规则、种子。
2. `civmat2 holdout seal --prereg <ws>/PREREG.md --split <ws>/HOLDOUT --code <ws>/code`。
3. `civmat2 holdout evaluate --split <ws>/HOLDOUT --prereg <ws>/PREREG.md --sha <ws>/PREREG.sha256 --manifest <ws>/FROZEN_MANIFEST.json --cmd "python3 <ws>/code/evaluate_holdout.py"`（评估脚本内用 `load_holdout`）。
4. 正负结果都写报告；偏离写 PREREG §7。**G3**：预注册判据原样执行；该留出此后不得复用。

## V7 独立证伪（skill `civmat2-idea`，workflow `civmat2-idea.js` stage falsify）
并行新上下文：civrev-adversary（新颖性、平凡解释、泄漏、稳健性、持平包装）+ civrev-experiment（隔离目录跑 run_all、逐数核对、`civmat2 holdout status` 只记一次）。任一 fatal → 不打包；major → 返工一轮（不复用留出）。

## V8–V9 写作与润色（skill `civmat2-write`，agents `<key>-writer` + `civrev-writing`，workflow `civmat2-write.js`）
1. `paper/OUTLINE.md`、`paper/CLAIM_EVIDENCE.csv`、`code/make_numbers.py` → `paper/NUMBERS_USED.json`。
2. 草稿只写 `{{key}}` 占位；逐节交 `<key>-writer`（只改表达）；`civmat2 numcheck fill`。
3. `civmat2 style <key> paper/manuscript_draft.md` ≥ 门槛；`civmat2 numcheck check … --allow-years --report paper/NUMBER_CHECK.md` 不一致 = 0；`civmat2 refcheck paper/refs.bib --report paper/CITATION_CHECK.md` 无 NOT_FOUND；civrev-writing 逐段建议。
4. 作者信息/基金/利益冲突/AI 声明留黄色占位 → `paper/作者待办.md`。

## V10 审稿（skill `civmat2-review`，agents `civrev-*` ×5 + `civrev-meta`，workflow `civmat2-review.js`）
1. 五审稿人新上下文并行，只看稿件/补充材料/代码包 → `review/R1…R5`。
2. civrev-meta 去重、逐条核实、给 decision 与必改清单 → `review/meta.md`。
3. Codex 外审两轮 → `review/codex_R1.md`、`codex_R2.md`。
4. 修改记录 `review/response_table.md`（`civmat2 template response_table`）；新实验/新推导回 V5–V6。**G4**：meta ≥ minor 且无未解决 major，Codex 第二轮无 fatal。

## V11 投稿包（skill `civmat2-package`，agent `civmat-packager`）
`civmat2 package --ws <ws> --name <中文名> --journal <期刊>` → `<ws>/submit/` + `投稿包_<名>_<日期>.zip` + `.sha256`；缺项列入 README 待办；作者本人提交。

## 挖掘循环（skill `civmat2-codex-loop`）
`civmat2 codex C# N [LANE]` 跑一轮；完成后按 `iterN/last.txt` 首行 STATUS 分支：PARTIAL → 写 feedback/STATE 续跑；RESULT → V7 独立证伪 → V8–V11；DEAD-END/EXHAUSTED → 记 STATUS.md 与设计稿 §10，从收割卡补位。4–5 进程并行，≤3 线程/进程。

## 闸门速查
| 闸门 | 通过条件 | 由谁判 |
|---|---|---|
| G0 | 数据已下载、许可可用、本机可算 | civmat-scout |
| G0.5 | 近 24 个月无等价工作 | civmat-scout + civrev-adversary |
| 可检测性 | ICC 非 SWAMPED 或有组内对比/模拟真值 | `civmat2 residuals` |
| G1 | 留出冻结零重叠；复现 ±10 % | civrev-experiment |
| G2 | 想法存活、可辨识、可检测、新颖 | civrev-adversary |
| G3 | 预注册封存后一次性评估 | `civmat2 holdout evaluate` |
| V7 | 两位独立审稿均非 fatal/major | civrev-adversary + civrev-experiment |
| GS | 风格分 ≥ LOO 中位数 90 % + 盲判 | `civmat2 style` + civrev-writing |
| G4 | meta ≥ minor 且无未解决 major | civrev-meta + Codex 两轮 |
