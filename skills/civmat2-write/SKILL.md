---
name: civmat2-write
description: civmatflow v2 V8–V9——先定目录与主张清单（CLAIM_EVIDENCE.csv），按目标"期刊×领域"写作 agent 逐节成稿，数字全部由 NUMBERS_USED.json 回填并可追溯，再用 style_check.py 与 civrev-writing 润色；无对应写作 agent 时先跑 civmat-style-distiller。
---

# V8 写作 / V9 润色

## 前置
- 风格库：`~/xzy/.claude/agents/style/INDEX.md`；没有目标期刊×领域条目 → 先派 civmat-style-distiller（只走合法渠道，GS 用修订标准）。
- 结果须已过 V7。

## 写作顺序
1. `paper/OUTLINE.md`：按 STYLE.md 的章节模板与篇幅比例；名词短语小节标题；图表清单（每图对应结果文件）。
2. `paper/CLAIM_EVIDENCE.csv`：每条主张 → 证据文件/图表 → 限定语（必须保留的 hedging）。
3. `paper/NUMBERS_USED.json`：所有正文数字由脚本从结果文件生成；正文用占位符回填，不手抄数字。
4. 逐节交 `<key>-writer` 执笔（只改表达，不改事实/数字/限定程度；缺信息留 [TODO]）。
5. 推导：正文给关键步骤，长推导进附录（工程化表述，见教训 15）。
6. 润色：style_check.py 逐节打分达到语料基线；civrev-writing 给逐段建议；数字核查脚本比对正文与 NUMBERS_USED.json，不一致=0。
7. 作者信息、基金、利益冲突、AI 声明留黄色占位，写进 `作者待办.md`。
