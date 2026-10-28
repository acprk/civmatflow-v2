---
name: civmat2-codex-loop
description: civmatflow v2 挖掘循环——Claude 控制 Codex（gpt-6.1-sol xhigh）按 PLAYBOOK 逐方向迭代挖掘；每次迭代完成后 Claude 读 last.txt/RESULT/STATE_UPDATE、必要时派独立证伪、写 feedback.txt/STATE.txt、续跑或关闭并从收割卡补位。用户要求"不间断挖"时使用。
---

# Codex 挖掘循环

## 文件
`codex/PLAYBOOK.md`（矿工规则：bar、E 型、模拟真值路线、留出卫生 5a、文献可读性约束）｜`codex/run_iter.sh C# N [LANE]`｜`codex/STATUS.md`（总表）｜`codex/C#/{brief.txt, feedback.txt, STATE.txt, lanes/, iterN/}`。

## 每次迭代完成（后台通知）时
1. 读 `iterN/last.txt`（首行 STATUS）与 `STATE_UPDATE.txt`；有 RESULT.txt 则读全文。
2. 按 STATUS 分支：
   - PARTIAL：写 `feedback.txt`（接受什么、否定什么、下一轮唯一重点、何时判 DEAD-END），`cp iterN/STATE_UPDATE.txt STATE.txt`，`run_iter.sh C# N+1`。连续 2 轮 PARTIAL 无候选关系 → 下一轮设为决断轮。
   - RESULT：派 civrev-adversary + civrev-experiment 独立证伪（civmat2-idea V7）。都非 fatal/major → 进入 civmat2-write → civmat2-review → civmat2-package；major → 写 feedback 返工；fatal → 关闭。
   - DEAD-END / EXHAUSTED：记录到 STATUS.md 与设计稿 §10，关闭；从 C4 收割卡补位（写新 `C#/brief.txt`，引用已下载数据路径）。
3. 保持 4–5 个进程并行（≤3 线程/进程）；收割连续多轮无果时换收割轴（障碍挖掘、多实验室数据、模拟真值）。
4. 冻结数据与留出文件 `chmod a-w`；Codex 只写自己的 iter 目录。
5. 聊天汇报只在：RESULT、方向关闭、投稿包完成、需要用户提供文件时。
