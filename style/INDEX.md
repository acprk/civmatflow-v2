# 期刊×领域写作风格库索引

由 `civmat-style-distiller` 生成；每行一个 key，对应仓库 `style/<key>/`（STYLE.md、phrasebank.md、style_check.py、stats.json、CORPUS.md；pdfs/ 与 text/ 只存本地）与 `agents/<key>-writer.md` 写作 agent。检查器统一入口：`civmat2 style <key> DRAFT`。
已有的非土木风格 agent：`gao-style-writer`（Gao 计算代数）、`www-writing-agent`（WWW）。

| key | 期刊 | 领域 | A/B 层篇数 | GS 盲测 | 日期 |
|---|---|---|---|---|---|
| efm-sizeeffect | Engineering Fracture Mechanics (B: Materials and Structures, Cem. Concr. Res., IJSS, JEM-ASCE) | quasi-brittle fracture & size effect of concrete (cohesive crack, SEL/USEL, BEM) | A 15 (3 held out) / B 20; 32 distilled | checker gate PASS 3/3 (rewrite 0.833 / 0.778 / 0.806 vs threshold 0.725 = 90 % of LOO median 0.806); blind judgement by civrev-writing pending (`blindtest.md`) | 2026-10-28 |
| ms-cemchem | Materials and Structures (RILEM, Springer) | cement chemistry, thermodynamic and pore-solution modelling of blended cements (GEMS/Cemdata18, alkali uptake in C-S-H, SCM reactivity) | A 37 (34 distilled + 3 holdout) / B 17; 10 paywalled items listed for user supply | style_check gate PASS 3/3 (rewrites 0.725 / 0.800 / 0.825 vs gate 0.720 = 0.9 × LOO median 0.80; originals 0.725 / 0.650 / 0.775); civrev-writing blind judgement FAIL 6/6 (cues = originals' non-native slips + rewrites shorter/more even) → writer texture rule added, GS criterion revised; re-test on high-language-quality holdouts pending | 2026-10-28 |
