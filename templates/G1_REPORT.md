# G1 REPORT — <方向>

## 0. 留出冻结
- `civmat2 holdout freeze` 参数（group / frac / seed）：
- `HOLDOUT/split.json`：来源数 / 留出来源数 / 行数：
- 所有 baseline 脚本已用 `load_calibration()`，零重叠断言：通过

## 1. 实现
| baseline | 实现文件 | 依据（原文式号 / 官方算例） | 算例核对结果 |
|---|---|---|---|

## 2. 原文误差复现（±10 % 为 PASS）
| baseline | 子集 | 指标 | 原文 | 复现 | 差异 | 解释 |
|---|---|---|---|---|---|---|

## 3. 残差地图（`civmat2 residuals` → results/residual_map.md）
- 系统性失效区（符号一致 ≥ 0.7、|ρ| ≥ 0.3）：
- 来源间/内方差：ICC(1) = … [CI]；可检测性判定：OK / MARGINAL / SWAMPED

## 4. 结论
- G1：PASS / CONDITIONAL / FAIL；理由：
- 进入 V5 的候选失效区与机理方向：
