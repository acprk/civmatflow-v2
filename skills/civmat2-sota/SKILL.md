---
name: civmat2-sota
description: civmatflow v2 V4/G1——先冻结留出、再按原文方程复现 SOTA baseline 并对齐原文误差（±10% 或精确解释差异），输出按物理变量分层的残差图与来源间/内方差分解。任何建模之前使用。
---

# V4 SOTA 复现（G1）

## 顺序（不可颠倒）
1. **冻结留出**：`civmat2 holdout freeze --data <ws>/data/processed/tidy.csv --group <source_col> --id record_id --frac 0.3 --seed <seed> --out <ws>/HOLDOUT`（按来源/机构整组；写 sha256；文件只读；已存在则拒绝覆盖）。
2. **守卫**：所有 baseline/正对照脚本开头
   ```python
   import sys; sys.path.insert(0, "{{CIVMAT2_HOME}}/tools")
   from holdout_guard import load_calibration
   rows = load_calibration("data/processed/tidy.csv", "HOLDOUT")   # 断言零重叠
   ```
   任何导出的校准文件再用 `civmat2 holdout check --data <file> --split <ws>/HOLDOUT` 复核。`load_holdout()` 在 evaluate 之外会抛 PermissionError。
3. **实现**：按原文方程（标式号）独立实现；有官方算例/库则先对算例（注意算例自身矛盾要记录，不是你的错）。
4. **复现原文误差**：同子集、同指标；±10 % 内为 PASS，否则逐项解释（选集规则不全、单位、版本）。原文选集无法重建时，改用自己冻结的显式选集，原文数字只作背景。
5. **残差地图**：`civmat2 residuals <calibration.csv> --obs <y> --pred <B0,B1> --source <source_col> --by <age_d,w_b,size,rh,…> --out <ws>/results [--log]` → `stratified_errors.csv`（符号一致性、Spearman 趋势）、`variance_decomposition.json`（ICC(1) + 来源 bootstrap CI + 可检测性判定 OK/MARGINAL/SWAMPED）、`residual_map.md`。
6. 产出 `notes/G1_REPORT.md`（模板 `civmat2 template G1_REPORT`）、`results/residuals_*.csv`、`results/stratified_errors.csv`。
7. 独立审计：派 civrev-experiment 新上下文核对（留出冻结、零重叠、复现容差、残差只用校准集）；或一键 `Workflow({scriptPath: "{{CIVMAT2_HOME}}/workflows/civmat2-sota.js", args: {home, ws, direction, dois, data_csv, group_col, seed, obs_col, pred_cols, by_cols}})`。

## 常见坑
随机点切分高估精度（D4：R² 0.81→0.44）；同一汇编多份重叠要去重；文献算例与代码库互相印证不算独立核对；在含留出行的总体上复现"原文精度"等于消费留出（C2）。
