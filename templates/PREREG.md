# PREREG — <方向名> / <idea slug>

> 预注册文件。写完后 `civmat2 holdout seal --prereg PREREG.md --split HOLDOUT --code code/`，
> 之后任何改动都会让 `civmat2 holdout evaluate` 拒绝运行。正负结果都必须报告。

## 0. 身份
- 方向 / 工作区：
- 想法文件：`ideas/<slug>.md`（版本/日期）
- 作者（agent）与日期：
- 冻结留出：`HOLDOUT/split.json`（sha256 of holdout_ids.csv = `…`）；是否曾被评估：否（必须）

## 1. 模型清单
| 编号 | 模型 | 参数数 | 来源 / 式号 | 角色 |
|---|---|---|---|---|
| B0 | <baseline> | | | 正对照（原文参数） |
| B0r | <baseline, 在校准集重标定> | | | 重标定对照（不是机理） |
| M1 | <候选机理模型> | ≤ B0 + 2 | ideas/<slug>.md Eq. (…) | 待检验 |
| M2 | <竞争机理模型> | | | 待检验 |

## 2. 数据
- 校准集：`data/processed/<tidy>.csv` 经 `load_calibration()` 过滤；条数 / 来源数：
- 留出集：按来源整组；条数 / 来源数：
- 排除规则（写死，评估前不得增删）：
- 缺测处理：
- 数据 sha256：

## 3. 指标
- 主指标：来源等权 log10-RMSE（或：`…`）；定义式：
- 次指标：pooled RMSE、MAE、均值比、CoV、按来源的中位绝对偏差
- 分层判据（关键失效区）：在 `<变量 ∈ 区间>` 子集上 `<指标>` 须 `<条件>`

## 4. 胜出判据（全部满足才算 M 型胜出）
1. Δ主指标(M1 − B0r) ≤ `<阈值>`，且来源 bootstrap（B = `<n>`，seed = `<s>`）95 % CI 上界 < 0；
2. ≥ 半数留出来源上 M1 优于 B0r；
3. 去掉任一留出来源后 1–2 仍成立；
4. 分层判据成立；
5. M1 在校准集上的参数与 ideas/<slug>.md 预言的符号/量级一致（不得改符号）。
持平规则：若 1 不成立但 CI 包含 0 → 报告为"持平"，只能作 E 型或"参数更少/物理一致"叙述。

## 5. 杀伤规则（任一触发 → 想法失败，照实报告）
- K1：消融去掉新增项后 Δ主指标 变化 < `<阈值>`（新增项无贡献）
- K2：B0r（纯重标定）达到与 M1 不可区分的精度
- K3：参数落在物理不允许的区间 / 可辨识性剖面似然平坦
- K4：留出上失效区偏差符号翻转
- K5：`<方向专属规则>`

## 6. 执行
- 评估脚本：`code/evaluate_holdout.py`（只在 `civmat2 holdout evaluate` 下运行，内部用 `load_holdout()`）
- 随机种子：；bootstrap 次数：；计算资源上限：≤3 线程、nice 10
- 预期产出：`results/holdout_metrics.csv`、`results/holdout_bootstrap.json`、`results/holdout_strata.csv`
- 中断恢复：只允许"不重预测、不改目标与指标"的恢复并完整披露

## 7. 偏离声明（评估后填写，不得改上文）
- 实际执行与预注册的差异：无 / <列出>
