---
name: civmat2-review
description: civmatflow v2 V10/G4——5 名专职审稿 agent（civrev-theory/experiment/domain/writing/adversary）新上下文并行盲审 + civrev-meta 元审稿，再加 Codex 两轮外审；按必改清单修改，直到无未解决 major。可用 workflows/civmat2-review.js 一键编排。
---

# V10 审稿团

## 输入
投稿 PDF（或 tex/docx）、补充材料、代码与数据包路径、目标期刊、风格 key。审稿人不看内部笔记与其他审稿报告。

## 流程
1. 并行派 civrev-theory、civrev-experiment、civrev-domain、civrev-writing、civrev-adversary，各写 `review/R1_theory.md … R5_adversary.md`。
   - 编排脚本：`Workflow({scriptPath: "/home/luck/xzy/0970project/civmatflow2/workflows/civmat2-review.js", args: {paper, supp, code, journal, style_key, review_dir}})`（Workflow 需用户已同意多 agent 编排）；否则用 Agent 工具手动并行派 5 个。
2. civrev-meta 汇总：去重、逐条回稿件核实、给 decision 与必改清单 `review/meta.md`。
3. Codex 外审两轮：`codex exec`（gpt-6.1-sol，xhigh，只读稿件与包），提示词含期刊口径与"找拒稿理由"；输出 `review/codex_R1.md`、`codex_R2.md`。
4. 修改：按 strategic-revision 记录"意见→修改→证据"到 `review/response_table.md`；涉及新实验/新推导的回到 V5–V6（不得复用已消费留出）。
5. G4：meta 结论 ≥ minor 且无未解决 major，Codex 第二轮无 fatal。
