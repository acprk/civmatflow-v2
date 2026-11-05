---
name: civmat2-prereg
description: civmatflow v2 V6/G3——写预注册 PREREG.md（主/次指标、胜出判据含来源 bootstrap CI、杀伤规则、分母与排除规则），sha256 封存，代码级 fail-closed 门禁，一次性留出评估并写 consumed 标记；正负结果都报告。
---

# V6 预注册与一次性留出

## PREREG.md 必含（模板 `civmat2 template PREREG`）
模型列表（含 baseline 与重标定对照）｜数据与冻结 split 的 sha256｜主指标（推荐来源等权 log-RMSE）与次指标｜胜出判据（Δ ≤ 阈值、CI 上界 < 0、≥半数来源改善、去任一来源仍成立）｜分层判据（关键失效区）｜杀伤规则｜排除与缺测规则｜随机种子与 bootstrap 次数｜评估脚本路径。

## 封存与执行
1. 封存：`civmat2 holdout seal --prereg <ws>/PREREG.md --split <ws>/HOLDOUT --code <ws>/code` → `PREREG.sha256` + `FROZEN_MANIFEST.json`（代码与 split 的 sha256），PREREG.md 置只读。
2. 评估脚本 `code/evaluate_holdout.py` 内部用 `from holdout_guard import load_holdout`（只有在 evaluate 下 `CIVMAT2_HOLDOUT_EVAL=1` 时允许）。
3. 一次性评估：`civmat2 holdout evaluate --split <ws>/HOLDOUT --prereg <ws>/PREREG.md --sha <ws>/PREREG.sha256 --manifest <ws>/FROZEN_MANIFEST.json --cmd "{{CIVMAT2_PYTHON}} code/evaluate_holdout.py"`：校验哈希与代码指纹 → 先写 `HOLDOUT_CONSUMED`（running）→ 运行 → 更新为 finished 并追加 `evaluations.log`。已存在 consumed 标记、哈希不符或代码改动都会拒绝（fail-closed）。
4. 结果中断（如评分 schema 报错）只允许"不重预测、不改目标与指标"的恢复，并在 PREREG §7 完整披露；`civmat2 holdout status --split <ws>/HOLDOUT` 查看记录。
5. 正负结果全部写入报告；之后不得用该留出验证新想法（新想法 = 新的、从未评估的留出，如嵌套按来源 CV 或独立原始试验集）。
