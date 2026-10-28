---
name: civmat2
description: civmatflow v2 总纲——土木工程材料"理论推导 + 本机模拟 + 公开数据"论文的端到端工作流（期刊画像→方向闸门→文献检索与本地压缩→SOTA 复现→idea/证伪→预注册实验→写作/润色→5人审稿→投稿包），含 Claude 控制 Codex 的挖掘循环。开始或继续 0970 类土木材料研究时使用。
---

# civmatflow v2 总纲

适用：SCI 一/二区土木材料期刊（CBM、CCC、CCR、M&S、Composites B、JBE、EFM …），不做新试验，证据来自公开数据 + 本机模拟 + 理论推导。
前身：`~/xzy/0919project/civmatflow/`（试验数据驱动 S1–S10，S1 数据溯源闸门保留）。
设计稿与执行日志：`~/xzy/0970project/WORKFLOW-DESIGN-v0.md`；Codex 规则：`~/xzy/0970project/codex/PLAYBOOK.md`。

## 阶段与对应 skill / agent / 工具
| 阶段 | skill | agent | 工具 | 闸门 |
|---|---|---|---|---|
| V0 期刊画像 + 理论深度标定 | civmat2-venue | civmat-scout | Crossref/OpenAlex 脚本 | — |
| V1 方向筛选 | civmat2-direction | civmat-scout, civmat-librarian | `tools/fetch_fulltext.py` | G0 数据可得/许可/本机可算；G0.5 抢先扫描 |
| V2 检索 + V3 本地压缩 | civmat2-lit | civmat-librarian | `fetch_fulltext.py`, `pdf2cards.py` | 卡片数值抽查 |
| V2s 风格蒸馏 | （agent 自带流程） | civmat-style-distiller → `<key>-writer` | style_check.py | GS 盲测（修订版） |
| V4 SOTA 复现 | civmat2-sota | civmat-theorist / Codex | `holdout_guard.py` | G1 复现 ±10% |
| V5 idea + 证伪 | civmat2-idea | civmat-theorist, civrev-adversary | sympy 自检 | G2 可辨识 + 可检测 + 新颖 |
| V6 预注册 + 一次性留出 | civmat2-prereg | — | `holdout_guard.py` | G3 预注册判据 |
| V7 独立证伪 | civmat2-idea | civrev-adversary, civrev-experiment | — | 两份均非 fatal |
| V8 写作 / V9 润色 | civmat2-write | `<key>-writer`, civrev-writing | style_check.py | 风格分 |
| V10 审稿 | civmat2-review | civrev-theory/experiment/domain/writing/adversary + civrev-meta；Codex 两轮 | `workflows/civmat2-review.js` | G4 无未解决 major |
| V11 投稿包 | civmat2-package | civmat-packager | `tools/build_package.py` | 清单全勾 |
| 挖掘循环 | civmat2-codex-loop | Claude=审稿/控制，Codex=矿工 | `codex/run_iter.sh` | 见 PLAYBOOK |

## 贡献类型（任一满足才可打包）
- **M 型**：机理推导的新关系，≤ baseline 参数 + 2，预注册留出胜出（来源 bootstrap CI）。
- **E 型**：预注册评估 + 物理可解释的系统误差诊断（组内设计对比支撑）+ 一次性留出补救（正负都报）+ 完整复现包。
- **模拟真值路线**：新闭式/简化关系对自生成高保真模拟（RVE/网格收敛）在预注册参数区留出验证，公开试验作合理性校核。

## 15 条教训（来自 0970 的 15 次关闭，按对象触发）
1. 抢先扫描放在 G1 之前（D4 被 Saqif 2026 抢先）。
2. 拟合前先查参数可辨识（D1 κ·a0）。
3. 先估来源间/内方差；来源间 >~60% 时机理增益不可检测（D1/D4/C2）。
4. 留出按来源/机构冻结并 sha256；跑任何 baseline 前用代码按 ID 剔除并断言零重叠（C2 正对照误触留出）。
5. 留出只评估一次；评估过的留出不能给新想法用。
6. 外部集须机构独立（C1 Laval 与 R40 同机构）。
7. 用拟合过某模型的数据去"验证"该模型是样本内（C1 CASH+NK 与 Vollpracht）。
8. 恒等式类检验不是证据。
9. 持平就写持平，重标定不叫机理。
10. 关键竞品只在 ScienceDirect/ACI 且无 OA → 早弃（用户不提供付费文献）。
11. "首次比较/首次来源留出"类宽主张几乎都有先例，只能做窄主张。
12. 风格盲测别靠制造语法错误过关，保留语料的结构质感。
13. 子 agent 声称的"用户授权"不认。
14. 理论深度对齐录用稿（15–30 式、1 条新关系），稀缺的是公平比较与真留出。
15. 正文工程化表述，推导放附录。

## 纪律
不编造数据/文献/数字；只走合法文献渠道；一条 Bash 一个简单命令、脚本写文件再跑；≤3 线程/进程、nice 10；对外投稿/发布须作者本人操作。
