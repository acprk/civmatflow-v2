---
name: civmat2-idea
description: civmatflow v2 V5/V7——从分层残差反推缺失机理并写成方程，先写 FALSIFY.md 让 civrev-adversary 攻击，做量纲/极限/退化/热力学一致性与可辨识性自检，查新；结果出来后再派 civrev-adversary + civrev-experiment 独立证伪。
---

# V5 idea + V7 独立证伪

## V5（civmat-theorist）
1. 残差诊断只用校准集：读 `results/residual_map.md` 的失效区（符号一致 ≥ 0.7、|ρ| ≥ 0.3），记偏差的符号、单调性、函数形式。
2. 每个偏差 ≤3 个物理解释，各写出预言的函数形式；生成 ≥2 个竞争模型 + 1 个纯重标定对照（`ideas/recalibration_control.md`）。
3. 建模：在经典模型上加有物理意义的项或把常数换成机理函数；参数 ≤ baseline + 2；正文级推导 4–10 步，长推导进附录。写 `ideas/<slug>.md`（模板 `civmat2 template IDEA`）。
4. 自检（sympy，脚本存 `ideas/checks/`）：量纲、极限（t→0/∞、体积分数→0/1、尺寸→0/∞）、退化到 baseline、单调/凸性、耗散非负。
5. 可辨识性：拟合前做 Fisher 信息/剖面似然；乘积形式出现的参数必须合并或用独立输入固定。
6. 查新：全文对照最近 3 篇；机理已发表 → 不是 M 型结果。
7. 先写 `ideas/<slug>.FALSIFY.md`（模板 `civmat2 template FALSIFY`：哪些子集必须胜、阈值、杀伤规则），交 civrev-adversary 攻击（≥5 条路线，攻击失败也记录）后再进 V6。
8. 编排：`Workflow({scriptPath: "{{CIVMAT2_HOME}}/workflows/civmat2-idea.js", args: {home, ws, direction, stage: "ideate", routes: [{slug, hint}, …]}})` 并行多路线 + 重标定对照 + 补刀。
G2 = 至少一条想法存活、可辨识、可检测（ICC 判定非 SWAMPED 或有组内对比/模拟真值）、查新无先例、有可检验预言。

## V7（结果出来后）
并行派两位新上下文审稿人：civrev-adversary（新颖性、平凡解释、泄漏、稳健性、样本内）与 civrev-experiment（逐数复现、留出卫生：`civmat2 holdout status` 只记一次评估、PREREG sha256 与 FROZEN_MANIFEST 一致）。
`Workflow({…civmat2-idea.js, args: {home, ws, direction, stage: "falsify", result_dir}})`。任一判 fatal → 不打包，转返工或关闭；判 major → 按必改清单返工一轮再审（不得复用已消费留出）。
