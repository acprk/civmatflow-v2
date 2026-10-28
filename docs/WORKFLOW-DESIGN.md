# civmatflow v2 · 土木工程材料（理论+本地模拟+公开数据）分支 — 设计草案 v0

日期：2026-10-27　状态：讨论稿，未执行　前身：`~/xzy/0919project/civmatflow/`（试验数据驱动的 S1–S10）

## 0. 需求对齐（一句话）
在 SCI 一区或二区土木材料期刊上（10/27 用户确认二区也可），选一个**期刊常收**、**无需现场/实验室实测**、**可用公开数据集 + 本机模拟验证**、**有理论推导空间**的方向；
先复现该方向当前最优 baseline，再提出自己的数学模型并在公开数据上配对胜出，最后成稿投稿。

## 1. 硬约束（来自既往项目的规则，全部继承）
| 约束 | 来源 |
|---|---|
| 数据来源先审：公开数据须有 DOI/许可/原始出处，不用"汇总后再整理"的二手表 | 1058 教训、civmatflow S1 |
| 先 SOTA 复现（正对照）再超越；基线同机同数据重跑 | feedback_sota_first_then_beat / full_scale_experiments |
| 自研模型，不做纯移植/纯 ML 堆叠 | feedback_invent_own_methods |
| 先写可证伪文件，子 agent 优先推翻 | feedback_multiagent_falsify_first |
| 判据先写后算、冻结哈希；8 条论文规则（G0 闸门…两次外审） | feedback_paper_project_rules |
| 正文工程化表述，推导可放附录 | feedback_es_engineering_not_math |
| **理论深度以目标期刊已录用论文为准，不追求更高**（10/27 用户确认）：由 V0 的"理论深度标定"给出目标区间，超出部分移附录或删去 | 用户 10/27 |
| 文献获取只走合法渠道（OA、出版社 TDM API、机构订阅、作者稿、用户自供 PDF），不部署影子图书馆类下载器 | 版权合规 |
| 计算限 32 核配额、不独占，计时报 CPU 秒 | reference_host_cpu_quota |

## 2. 思维链条（每一步回答一个问题，答不出就停）
1. **期刊收什么？** 近 3 年一区期刊的 topic 频次与增长（OpenAlex/Crossref 元数据，本地统计）。
2. **哪些 topic 不需要实测？** 有公开数据库 + 可本机模拟（FE/相场/热力学/MD/微观力学）。
3. **这条线的最优 baseline 是谁、在哪个数据上、误差多少？** 建 baseline 台账。
4. **baseline 在哪里系统性失效？** 残差按物理变量分层（龄期、尺寸、配比、温湿度…）找结构性偏差。
5. **失效的机理是什么？** 从偏差反推缺失的物理项 → 写成方程（本构/输运/断裂/热力学）。
6. **新模型可证伪的预言是什么？** 预注册：留出数据集、指标、胜出阈值、配对检验。
7. **它真的赢了吗？** 独立重实现 + 消融 + 跨数据集外推。
8. **新在哪里？** 查新（含被引与作者后续工作）。
9. **审稿人会怎么拒？** 模拟 3 审 + Codex 外审两轮。

## 3. 阶段与闸门
| 阶段 | 内容 | 产出 | 闸门 |
|---|---|---|---|
| V0 期刊画像 | 一/二区期刊清单 → 近 3 年题录 → topic 聚类/频次/增长；**理论深度标定**：每刊抽 10–15 篇同领域录用稿，统计公式数、推导类型（经验拟合/半解析/解析本构/数值反演）、正文 vs 附录推导比例 | `venue/topic_map.md`、`venue/theory_depth.md` | — |
| V1 方向筛选 | 候选方向打分（见 §5）| `DIRECTION.md`（选 1 主 1 备）| **G0**：数据可下载、许可可用、本机可算 |
| V2 文献检索 | OpenAlex/Semantic Scholar/Crossref + 引文雪球；CNKI 由用户导出 | `lit/bib.bib`、`lit/pdfs/` | — |
| V3 本地压缩 | PDF→markdown→**文献卡**（问题/模型方程/数据集/指标/数值+页码）+ **baseline 台账** | `lit/cards/*.md`、`BASELINES.md` | 卡片数值抽样回查原文 |
| V4 SOTA 复现 | 在公开数据上复现最优 baseline（正对照）| `repro/` + 误差对照表 | **G1**：复现误差落在原文报告值容差内 |
| V5 Idea | 残差分层→机理→方程；先写 `FALSIFY.md`，多 agent 尝试推翻 | `ideas/*.md`、存活卡片 | **G2**：至少一条存活且有可检验预言 |
| V6 预注册+实验 | 留出集/跨数据集外推/消融/配对检验；本机模拟 | `PREREG.md`（冻结）、`results/` | **G3**：配对胜出且不靠调参 |
| V7 证伪审计 | 新上下文独立重实现、换工具复算 | `audit/verdict.md` | 通过才可写 |
| V2s 风格语料 | 与 V2 并行：按"期刊×领域"收集范文，蒸馏成本地写作 agent（见 §8）| `style/<journal>-<field>/` | **GS**：风格 agent 通过盲测（§8.4）|
| V8 写作 | 先定目录→主张清单→逐节写，由该期刊×领域的写作 agent 执笔；数字全部可追溯 | `paper/` | — |
| V9 润色 | 风格检查器逐节打分 + AI 味检查 + 术语/单位/规范引用一致性 | 风格报告 | 风格分达到范文基线 |
| V10 审稿 | 5 名专职审稿 agent 盲审（§7）+ Codex 外审两轮 | `review/` | **G4**：无未解决 major，元审稿结论 ≥ minor |
| V11 投稿/修回/交接 | 沿用 civmatflow S8–S10 | 投稿包 | — |

## 4. agent / skill 编排（复用 + 新增）
- 复用：civmat-analyst / modeler / validator / writer / checker / reviewer / auditor；通用 skills：research-lit、paper-write、polish-writing、paper-reviewer、peer-review、strategic-revision；mathflow 的 falsify-math、novelty-and-deps、constant-ledger（用于模型参数台账）。
- 新增：
  - `civmat-scout`（V0–V1 期刊画像与方向打分）
  - `civmat-librarian`（V2–V3 检索、文献卡、baseline 台账、查新）
  - `civmat-theorist`（V5 机理→方程、推导、量纲/极限情形自检）
  - `civmat-falsifier`（V5/V7 新上下文推翻）
  - `civmat-style-distiller`（V2s 范文收集与风格蒸馏，产出写作 agent + 检查器）
  - `<journal>-<field>-writer`（蒸馏产物，每个"期刊×领域"一个，如 `ccr-creep-writer`）
  - 5 名审稿 agent + 1 名元审稿 agent（§7）
- workflow：`civmat-direction.js`（V0–V1 并行侦察）、`civmat-sota.js`（V2–V4）、`civmat-idea.js`（V5–V7）、沿用 `civmat-paper.js`（V8–V10）。

## 5. 方向打分维度
期刊收稿频次与趋势 / 公开数据质量与规模 / 本机可算性 / 理论推导空间 / baseline 清晰度 / 拥挤度（纯 ML 拟合 UCI 类已饱和，扣分）/ 与用户既往（发泡砂浆、纤维复合）衔接度。

## 6. 候选方向初稿（待 V0/G0 核实，数据可得性未逐一验证）
| # | 方向 | 公开数据（待核实）| 本机模拟 | 当前代表 baseline | 理论空间 |
|---|---|---|---|---|---|
| D1 | 混凝土徐变/收缩长期预测 | NU 徐变收缩数据库（Bažant & Li 2008）| 老化粘弹性速率型积分、贝叶斯更新 | B4/B4s、fib MC2010、ACI 209 | 高：微预应力-固化理论、长期外推 |
| D2 | 准脆性断裂尺寸效应 | Hoover–Bažant 综合断裂试验（2013）| 细观随机骨料+相场/内聚力 FE | SEL、Type 1/2 尺寸效应律 | 高：尺寸-几何联合标度 |
| D3 | 水泥基体系热力学建模（掺合料/碳化/氯离子结合）| Cemdata18 + 文献实测相组成 | GEMS 等开源热力学 | Lothenbach 系列 | 中高 |
| D4 | 氯离子侵蚀与服役寿命 | 已发表暴露数据汇编 | 非线性扩散-结合 PDE、不确定性量化 | fib 34、DuraCrete、时变扩散系数模型 | 中高 |
| D5 | 约束混凝土/FRP 约束应力-应变模型 | 已汇编的大规模试验库 | 设计导向/分析导向模型 | Lam–Teng、Ozbakkaloglu 等 | 中 |
| D6 | 纤维/多孔（发泡）水泥基材料细观力学均匀化 | 文献汇编 + 自生成微结构 | Mori–Tanaka/FFT 均匀化 | 经典均匀化+经验修正 | 中高，衔接 0919 背景 |
| ✗ | 纯 ML 预测 UCI 抗压强度 | UCI Concrete | — | 大量 XGBoost/NN | 低，拥挤，不推荐 |

## 7. 审稿团（V10）：5 名专职审稿 agent + 元审稿
每名审稿人在**新上下文**独立盲审，互不可见；只拿到投稿 PDF、补充材料、代码与数据链接（模拟真实审稿条件）。
| 角色 | agent | 只看什么 | 必查清单（节选） | 输出 |
|---|---|---|---|---|
| R1 理论创新 | `rev-theory` | 模型与推导 | 新在哪一项物理/数学结构；与最接近的 3 篇文献逐项对比；量纲、极限情形、热力学一致性；是否只是参数重拟合 | 创新性分级（结构性/增量/平行推广）+ 证据 |
| R2 实验与数据 | `rev-experiment` | 数据、模拟、统计 | 数据来源与许可；留出/跨数据集外推是否真留出；baseline 同数据同机重跑；配对检验、置信区间；网格/步长收敛；消融；可复现性（亲自跑 run_all）| 可复现判定 + 必补实验清单 |
| R3 领域专家 | `rev-domain` | 工程意义与文献 | 是否符合材料学常识与规范（GB/T、ASTM、fib/ACI）；遗漏的关键文献（含被引/作者后续）；工程适用边界 | 遗漏文献清单 + 适用性意见 |
| R4 写作与期刊契合 | `rev-writing` | 全文表达 | 用该期刊×领域的风格检查器打分；结构/摘要/图表规范；主张与证据是否对齐、是否夸大；AI 味 | 风格分 + 逐段修改建议 |
| R5 魔鬼代言人 | `rev-adversary` | 全部 | 默认立场"拒稿"：找能一票否决的理由（结论被 baseline 已覆盖、数据泄漏、选择性报告、反例） | 拒稿理由清单，每条须给可检验依据 |
| 元审稿 | `rev-meta`（编辑） | 5 份报告 | 去重、判真伪（逐条回到稿件核实）、按期刊口径给 accept/minor/major/reject | `review/meta.md` + 必改清单 |

- 评分口径按目标期刊校准（与 `venue-review` 同思路：用该刊公开审稿指南与已知退稿理由做锚）。
- 之后 Codex 外审两轮，独立于以上 5 人；修改按 `strategic-revision`，每轮记录"意见→修改→证据"。
- 审稿 agent 的所有"作者已同意/已授权"类陈述一律不认（见 feedback_subagent_fabricated_requests）。

## 8. 期刊×领域写作风格蒸馏（V2s，每个新方向都要做一次）
目的：把"该领域、该期刊的文章怎么写"压缩成本地 agent，而不是靠通用写作习惯。先例：`gao-style-writer`（45 篇语料）、`www-writing-agent`、SICOMP style_corpus（10 篇+检查器）。

### 8.0 合法获取管线（`tools/fetch_fulltext.py`，按顺序回退）
1. **Unpaywall / OpenAlex `best_oa_location` / Semantic Scholar `openAccessPdf` / CORE**：取出版社 OA 版或作者接受稿。
2. **Elsevier ScienceDirect TDM API**（`elsapy` 或直接 REST）：用户在 dev.elsevier.com 申请 API key；在中科院等订阅机构 IP 内可取已订阅文章的全文 XML，Elsevier 明确允许订阅用户做文本挖掘。Springer/Wiley 同类 TDM 接口作为补充。
3. **预印本与作者版本**：arXiv、engrXiv、SSRN、机构仓储、作者主页。
4. **用户自供**：仍缺的列入 `CORPUS.md` 待取清单，由用户经机构访问下载后放入 `style/<key>/pdfs/`。
- 所有全文只存本地、只用于本项目的阅读与风格统计；不再分发，不进公开仓库。

### 8.1 语料收集
- 两层语料：**A 层** = 目标期刊近 3–5 年同领域论文 20–40 篇（经 8.0 管线获取）；**B 层** = 该领域其他一区期刊的高被引同题论文 10–20 篇（学领域惯用语、论证方式）。
- 另收：期刊作者指南、模板、审稿指南、编辑社论；若有，公开的审稿意见。
- 语料清单 `style/<key>/CORPUS.md`：DOI、年份、被引、OA 状态、是否已读入；只存本地，不外传。

### 8.2 蒸馏内容（`STYLE.md`）
1. 宏观结构：章节目录模板、各节篇幅比例、图表数量与位置、附录使用习惯。
2. 修辞步（move analysis）：摘要/引言/讨论/结论各自的步骤序列与典型句式（例：引言"工程背景→已有模型→缺口→本文"）。
3. 语言统计：句长分布、被动/主动比例、人称、限定语（may/might）密度、时态、连接词。
4. 术语与单位：领域标准术语表、符号约定、单位写法、规范引用格式。
5. 理论呈现方式：推导放正文还是附录、公式密度、如何把数学结果翻译成工程结论。
6. 图表与图注习惯；引文密度与引文位置。
7. 短语库：按功能分类（提出缺口、对比 baseline、承认局限……）。

### 8.3 产物
- `style/<key>/STYLE.md` + `phrasebank.md` + `style_check.py`（统计指标对照范文分布，逐节打分）。
- agent 文件统一放 `~/xzy/.claude/agents/<journal>-<field>-writer.md`（10/27 用户确认，全局共享，作为长期写作语料库）：只改表达，不改技术事实与数字。
- 对应语料与 STYLE.md 统一放 `~/xzy/.claude/agents/style/<journal>-<field>/`，agent 文件内用绝对路径引用；新增一份索引 `~/xzy/.claude/agents/style/INDEX.md`（期刊、领域、语料篇数、盲测结果、日期）。

### 8.4 盲测闸门 GS
- 留出 3 篇范文不进语料；把其中段落去风格化（改写成通用表达）后让写作 agent 重写，检查器打分须落入范文分布；
- 另由 `rev-writing` 盲判"重写段 vs 原文段"，区分正确率接近 50% 视为通过。

## 9. 每个出好结果的方向：投稿包规格（沿用 0961 ES 投稿包形式）
目录 `0970project/D<k>_<slug>/submit/`，打包为 `0970project/投稿包_<方向中文名>_<日期>.zip` + `.sha256`：
```
submit/
  01_Cover_Letter_DRAFT.docx
  02_Highlights.docx
  03_Manuscript.docx              （+ LaTeX 源在 00_作者参考 下）
  04_Graphical_abstract.pdf/.tif
  05_Figures/Figure_*.pdf|png
  06_Supplementary_Material.pdf
  07_Supplementary_data_and_code.zip   ← 实验数据集 + 实验结果数据 + 代码
      data/raw/<dataset>/  （公开数据原件或下载脚本+sha256，按许可决定是否可再分发）
      data/processed/      （清洗后数据 + 清洗脚本）
      results/             （全部实验输出 CSV/JSON，正文每个数字可追溯）
      code/ run_all.sh  expected_output/  README.md  LICENSE
  PACKAGE_MANIFEST_sha256.json
  README_投稿上传顺序与作者待办.md
  00_作者参考_勿上传/
      CLAIM_EVIDENCE.csv  NUMBERS_USED.json  NUMBER_CHECK.md  CITATION_CHECK.md
      PREREG.md(冻结哈希)  BASELINES.md  FALSIFY.md
      review/R1–R5 + meta.md + Codex 两轮  response_table.md
      STYLE 引用（style key）  作者待办.md  推荐审稿人候选_待作者核实.md
      LaTeX_source/  Rebuild_scripts/
```
- 公开数据若许可不允许再分发，只放下载脚本 + 校验哈希 + 引用。
- 作者信息、基金、利益冲突、AI 声明留黄色占位，列入作者待办；对外投稿须作者本人操作。

## 10. 执行日志
- 10/27 V0–V1 侦察启动：topic 画像、理论深度标定、公开数据 G0 核实、SOTA baseline 台账（4 个并行 agent）。
- 10/27 已建 agent：civrev-theory/experiment/domain/writing/adversary/meta、civmat-style-distiller、civmat-theorist（~/xzy/.claude/agents/）。

- 10/27 V0 topic 画像完成（venue/topic_map.md）：OpenAlex 当日 429，改用 Crossref 56,303 篇，但 Elsevier 无摘要→仅标题分类，精度约 ±30 点。非实验类前列：断裂/尺寸效应+细观模拟 570、耐久输运 644(ML 155)、界面/ITZ 343(增长1.33)、损伤塑性本构 409(ML仅11)、热力学/水化动力学 175(增长1.48,CCR/CCC)、徐变收缩 226。D5 FRP 约束份额下降(0.66)→降级。

- 10/27 SOTA 台账完成（BASELINES.md，81 卡/61 篇 OA 全文）。最有希望：D1 自收缩/SCM 收缩（NU 库 Zenodo CC-BY 4663 组，B4 ω≈0.82，所有模型 0.8–1.0）；D4 时变 α 放进 erf 解在数学上不自洽（Fjendbo 2021 CC-BY 现场剖面≤31 年）——须查新，此批评可能已有人提出；D2 USEL 已很准(2.3%)，靶点=无切口/浅切口；D3 无 RMSE 型指标、碱度骤降 vs 渐变；D5 拥挤+无 CSV→放弃；D6 公开数据薄。

- 10/27 G0 完成（data/DATASETS.md，33 个数据集 749MB 已下载+sha256）：D1 PASS（NU 2023 CC BY，1469 徐变/3570 收缩试验）；D3 PASS（Cemdata18.1+GEMS+~800 孔溶液）；D4 碳化 PASS（Chan 2026 8194 深度+TC281）、氯离子 PARTIAL；D2/D5 PARTIAL；D6 FAIL。新发现 FRP–混凝土粘结库 3162 条（CC BY）。
- 10/27 决策：主方向 D1（自收缩/SCM 收缩）+ D4 改为自然碳化；两者 G1 baseline 复现已启动。D3 留作第三方向；D6 因数据 FAIL 放弃。

- 10/27 D1 G1 部分通过：B4/B4s 过 RILEM 算例(47/52，5 条是原文算例自相矛盾)，MC2010 与 structuralcodes 一致；Šmilauer 选集仅 2/5 类 ±10% 内复现（其 §2.1 过滤给出的组数多于其报告）。决策：改用我们自己冻结的显式选集评估 baseline，Šmilauer 数字只作背景。失效图：自收缩全模型低估且随龄期加重(B4 中位 −37%，MC2010 −76%；w/b≤0.30 更甚)；掺合料收缩随时间漂移(单源主导)；浸水/长期徐变 B4 高估。D1 V5 理论阶段已启动（候选：自干燥孔压×B4 基本徐变柔度的粘弹性响应，须查新+至少 2 个竞争模型）。

- 10/27 **D1-autogenous PVE 想法 NO-GO**（D1_shrinkage/notes/V5_THEORY.md）：冻结 151 试验/32 来源，按来源分 87/64；留出集 PVE ω 0.971 vs B4 0.849，5 条杀伤规则全触发；κ·a0 不可辨识；机理已被 Grasley&Leung 2011、Aili 2018 占先。该留出集已用过一次——D1 后续任何想法须用新留出（嵌套按来源 CV 或独立原始试验集，Havlásek 2021 需用户提供 Table 1）。D1 暂停，候选再启：掺合料收缩漂移（先做来源核查）。
- 10/27 D3 G1 启动：GEMS/Cemdata18 对 ~800 组公开孔溶液的系统基准（领域尚无 RMSE 型基准）+ 碱度骤降 vs 渐变失效区。

- 10/27 D4 碳化 G1 PASS（TC281 Eq.9 MAE 1.339/R² 0.812 vs 1.33/0.82；RF/XGB、Chan CatBoost 近似复现；fib Bulletin 34 无合法全文→不得声称胜过 fib）。按来源分组后 ML R² 跌到 0.44–0.77；TC281 w/CaO 线外推到 Chan 库 R² 0.54。失效：>10 年全部高估（室内无雨也减速——查新未见覆盖）、RH 符号翻转、高掺合料/石灰石/高 w/b 低估（疑为活性 CaO 近似失效）。D4 V5 已启动：外部检验=Chan 库（剔除 4 个共享来源），先冻结留出再建模。

- 10/27 **D4 饱和堵塞核 V5 NO-GO**（D4_carbonation/notes/V5_THEORY.md）：Chan 外部检验 MAE 2.31 vs √t 2.39（不显著），对 RH-law 消融 ΔMAE −0.024 [−0.10,0.035]→K1 触发；>10 年偏差减半但仅 5+2 来源；高掺合料更差。两份留出集均已用过一次。
- 10/27 教训（两次 NO-GO 共性）：跨来源文献数据的来源间散布主导误差，机理模型的增益被淹没。策略调整：D4 考虑重构为"按来源分组验证基准 + 可辨识性定理"类论文（恒定气候尖锐前沿必为 √t；幂律堵塞与老化不可区分；ML 随机切分高估精度；TC281 线可迁移），须先过对抗审查与查新。

- 10/27 D3 G1 条件通过：micromamba+gems3k 4.6.1/xgems 2.1.2 免 root；Cemdata18+CSHQ（CASH+NK 无法跑全水泥体系）；944 条/50 来源组，留出 18 组 280 条已冻结且未评估；复现 3 项已发表 GEMS 对比。校准集 log10 RMSE：Na 0.50(偏差−0.31)、K 0.38(0.00)、OH 0.32、S/Al/Si >1。失效：Na 全面低估而 K 无偏；Ca/Si<1 碱过高估 9×（仅 2–3 源）；后期碱度漂移。D3 V5 已启动：离子专属碱吸附模型（Ca 竞争交换等），基准本身也预注册为交付物。

- 10/27 **D4 重构方案也 NO-GO**（notes/REFRAME_ADVERSARY.md）：Saqif 2026（CCR 稿 + Zenodo 21830461）已发布 TC281+Chan 统一数据集、按来源分组基准与跨库迁移；C-B 同行集比较后被推翻（CatBoost 0.595 vs 线 0.541）；√t 定理即 Boltzmann 结果，Aiki&Muntean 2013 已严格证明，且有无材料时间尺度的减速反例；"室内也减速"站不住。**D4 关闭。**
- 10/27 流程修订：**查新/抢先扫描（近 18 个月预印本+Zenodo+MDPI）提前到 G1 之前**，作为 G0.5 闸门。

- 10/27 理论深度标定完成（venue/theory_depth.md，40 篇无新试验 OA 稿，M&S 占 18）：目标带=正文 15–30 个编号公式（中位 18）、一条机理推导的新关系（4–10 步）、≥3 个公开/文献数据集且 ≥1 个留出、≥2 个 baseline 同数据重跑、RMSE+均值比/CoV、~20 页、10–15 图。**稀缺的不是数学，而是公平的 baseline 比较与真留出**（仅 9/40 有真留出、13/40 有 ≥2 baseline）。推论：我们的预注册留出胜出标准高于多数录用稿；"留出持平但参数更少/物理一致 + 诚实基准"也可作为可发表结果，但须如实表述，不得包装为胜出。

- 10/28 **工作流落地**：`0970project/civmatflow2/`——11 个 skill（已软链到 ~/xzy/.claude/skills）、新增 agent civmat-scout/librarian/packager（与已有 theorist、style-distiller、civrev×6、两个风格写作 agent 合计 13 个）、4 个工具（fetch_fulltext、pdf2cards、holdout_guard、build_package；holdout_guard 与 build_package 冒烟测试通过）、2 个 Workflow 脚本（direction、review）、README/install.sh。

## 11. 待讨论决策点
见对话。
