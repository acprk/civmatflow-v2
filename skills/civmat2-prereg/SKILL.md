---
name: civmat2-prereg
description: civmatflow v2 V6/G3——写预注册 PREREG.md（主/次指标、胜出判据含来源 bootstrap CI、杀伤规则、分母与排除规则），sha256 封存，代码级 fail-closed 门禁，一次性留出评估并写 consumed 标记；正负结果都报告。
---

# V6 预注册与一次性留出

## PREREG.md 必含
模型列表（含 baseline 与重标定对照）｜数据与冻结 split 的 sha256｜主指标（推荐来源等权 log-RMSE）与次指标｜胜出判据（Δ ≤ 阈值、CI 上界 < 0、≥半数来源改善、去任一来源仍成立）｜分层判据（关键失效区）｜杀伤规则｜排除与缺测规则｜随机种子与 bootstrap 次数。

## 封存与执行
1. `sha256sum PREREG.md > PREREG.sha256`；代码清单另存 FROZEN_MANIFEST.json。
2. `python tools/holdout_guard.py evaluate --prereg PREREG.md --sha PREREG.sha256 --cmd "<eval script>"`：校验哈希→运行→写 `HOLDOUT_CONSUMED`；已存在 consumed 标记则拒绝再跑。
3. 结果中断（如评分 schema 报错）只允许"不重预测、不改目标与指标"的恢复，并完整披露。
4. 正负结果全部写入报告；之后不得用该留出验证新想法。
