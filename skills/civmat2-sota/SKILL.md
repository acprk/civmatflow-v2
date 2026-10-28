---
name: civmat2-sota
description: civmatflow v2 V4/G1——先冻结留出、再按原文方程复现 SOTA baseline 并对齐原文误差（±10% 或精确解释差异），输出按物理变量分层的残差图与来源间/内方差分解。任何建模之前使用。
---

# V4 SOTA 复现（G1）

## 顺序（不可颠倒）
1. **冻结留出**：`python tools/holdout_guard.py freeze --data <tidy.csv> --group <source_col> --frac 0.3 --seed <seed> --out <dir>/HOLDOUT`（按来源/机构整组；写 sha256）。
2. **守卫**：所有 baseline/正对照脚本开头 `from holdout_guard import load_calibration`，按冻结 ID 剔除留出并断言零重叠。
3. **实现**：按原文方程（标式号）独立实现；有官方算例/库则先对算例（注意算例自身矛盾要记录，不是你的错）。
4. **复现原文误差**：同子集、同指标；±10% 内为 PASS，否则逐项解释（选集规则不全、单位、版本）。原文选集无法重建时，改用自己冻结的显式选集，原文数字只作背景。
5. **残差地图**：按物理变量分层（龄期、尺寸、配比、温湿度、SCM、来源），给符号与趋势；来源间/内方差分解（ICC + bootstrap CI）。
6. 产出 `notes/G1_REPORT.md`、`results/residuals_*.csv`、`results/stratified_errors.csv`。

## 常见坑
随机点切分高估精度（D4：R² 0.81→0.44）；同一汇编多份重叠要去重；文献算例与代码库互相印证不算独立核对。
