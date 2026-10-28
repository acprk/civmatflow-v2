# STYLE.md — Materials and Structures (RILEM, Springer) × cement chemistry, thermodynamic and pore-solution modelling of blended cements

key `ms-cemchem` · distilled 2026-10-28 · local only, not for redistribution.

Corpus (details in `CORPUS.md`). **A layer**: 37 Materials and Structures (M&S) papers from 2021–2026, all CC-BY Springer PDFs. Topics: thermodynamic modelling, pore solution, alkali binding/release, C-(A)-S-H, M-S-H, SCM reactivity (R3), and chloride binding. The set includes RILEM TC 267-TRM, 282-CCL, 283-CAM, 298-EBD and 301-ASR reports. 3 A papers are held out for the blind test (Bagheri 2022, Barzgar 2022, Rehman 2025), so the statistics below come from **34 A papers**. **B layer**: 17 high-cited OA papers (Cem Concr Res / Cem Concr Compos repository copies, plus M&S/RILEM Tech Lett before 2021: Lothenbach 2019 ×2, Kulik 2022, Miron 2022a, Myers 2014, Yan 2022 ×2, Vollpracht 2016, De Weerdt 2019, Barzgar 2021, Ke 2020, …). B is used as a style reference only. Numbers come from `scripts/s4_measure.py`, `s8_aggregate.py` and `s9_notation.py` (P10 / P50 / P90 over papers). Every quoted sentence is verbatim from `text/<key>.txt` and is followed by [key | DOI]. `scripts/s10_verify_quotes.py` re-checks all quotes.

---

## 1 Macro structure

### 1.1 Section template (A layer, top-level headings detected in 34 papers)
- **Standard research article (27/34)**: `1 Introduction` → `2 Materials and methods` (variants: `Experimental`, `Materials and experimental methods`, `Experimental program` + `Methodology`) → `3 Results and discussion` (15 papers) **or** `3 Results` + `4 Discussion` (9 papers) → `4/5 Conclusions` (also `Conclusion`, `Concluding remarks`, `Summary and conclusions`, `Conclusions and recommendations`).
- **Modelling-heavy papers** use the same template and put the model inside Materials and methods as a numbered subsection, e.g. `2.5 Thermodynamic modelling` (Gluth 2024), `2.2.1 Software and database` (Jin 2025), `2.2.2 Thermodynamic modeling of the soluble alkali` (Sharbaf 2026), `2.6 Thermodynamic modelling` (Danner 2026). Miron 2022 uses `2 Calculation setup` → `3 Results` → `4 Discussion` → `5 Summary and conclusion`. Jin 2025 adds a separate `5 Limitations and perspectives` before the Conclusions. This is a good model for a benchmark + new-model paper.
- **RILEM TC reports and reviews** use topical headings (`2 Bulk methods`, `3 Chloride quantification by phase`; `2 Pore solution database`; `3 Knowledge gaps`, `4 Outlook`; `6 Final remarks and perspectives`). The front matter states the TC: “This article was prepared by members of WP2 within RILEM TC 301-ASR …”, “The article was reviewed and approved by all members of the TC.” A TC membership list follows.
- Numbering: Springer style without trailing dots (`2.1 Materials`, `3.3 FA-composite cements`), two or at most three levels. Subsection headings are noun phrases.
- Back matter, in order: Acknowledgements → Author contributions (CRediT verbs: “Conceptualization, Methodology, Validation, Formal analysis …”) → Funding (“Open Access funding enabled and organized by Projekt DEAL.” / “Open access funding provided by …”) → Data availability → Declarations / Conflict of interest. An ESM statement appears in **71 %** of A papers (“Supplementary Information The online version contains supplementary material available at https://doi.org/…”). Appendices appear in about a quarter. Mostly they hold synthesis or input tables (“as detailed in Appendix F”). The norm is ESM, not an appendix.

### 1.2 Length and proportions (A, words in detected sections, P10 / P50 / P90)
| part | words | share of text |
|---|---|---|
| Abstract | 183 / 263 / 440 (one paragraph; the TC reports run long) | 3 / 4 / 7 % |
| Introduction | 596 / 833 / 1324 | 8 / 13 / 21 % |
| Methods + Results + Discussion | 3110 / 5313 / 7310 | 66 / 76 / 80 % |
| Conclusions | 201 / 479 / 883 | 4 / 7 / 11 % |
| Total (sections) | 4707 / 6695 / 9245 | |

### 1.3 Figures, tables, equations, references (A)
- Figures **7 / 10 / 13**; tables **1 / 3 / 6**; numbered display equations **0 / 0 / 2** (M&S papers rarely number equations; the B-layer CCR model papers have many). References **30 / 52 / 73** (TC reports and reviews 110–160).
- Figure placement: Fig. 1 usually sits in Materials and methods (materials, PSD, a schematic or a DoR-vs-replacement plot). About 70 % of figures are in Results. The Conclusions never cite figures (Fig./Table refs per 1000 words in Conclusions: P90 = 0).

---

## 2 Rhetorical moves

### 2.1 Abstract (single paragraph, no citations, no figure refs)
Move sequence: **A1 problem/context (1 sentence)** → **A2 what this study does** (“This study …”, “In this paper …”, “This is a theoretical study on …”) → **A3 materials/techniques** → **A4 main quantitative results** (numbers, ranges, thresholds) → **A5 mechanism or recommendation sentence**.
- A1: "Chloride binding by the hydrate phases of cementitious materials influences the rate of chloride ingress into these materials and, thus, the time at which chloride reaches the steel reinforcement in concrete structures." [A_2024_Gluth_LDH | 10.1617/s11527-024-02311-3]
- A2: "This is a theoretical study on the applicability of a thermodynamic model (GEMS) and the empirical Taylor model to predict the required replacement level of portland cement (PC) by SCMs to achieve an alkali metal concentration below 300 mmol/L." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- A4: "To get an improved agreement with the pore solution data, the stability of two CASH? model endmembers, TCKh and TCNh, has been fine-tuned with standard Gibbs energy corrections of ? 7.0 and ? 5.0 kJmol-1, respectively (at 1 bar, 25 °C)." [A_2022_Miron_CASHNK | 10.1617/s11527-022-02045-0] (“?” = “+”/“−” lost in the PDF text layer)
- A5: "The main difference between the two models is how they account for the uptake of alkali metals by the C–S–H." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- A5 (recommendation): "It is recommended that (Na + K) is used as the most reliable and relatively easily accessible parameter to indicate the potential for ASR in concretes or mortars up to 40 °C." [A_2025_Lothenbach_TC301 | 10.1617/s11527-025-02726-6]

### 2.2 Introduction (≈ 830 words, 4–7 paragraphs, about one citation per sentence)
**I1 relevance** (CO2 and clinker factor, or a durability mechanism such as ASR or chloride ingress) → **I2 chemistry background** (phases, reactions, where the alkalis sit, cement notation, sometimes a reaction equation) → **I3 named prior work** (“Shehata and Thomas [6] proposed …, Duchesne and Bérubé [7] reported …”) → **I4 gap**: a missing dataset, an untested model or a contradiction, introduced by *However*/*Despite*/*Although* → **I5 aim** (“The aim of the present paper is to …”) → **I6 approach in one or two sentences** (techniques listed; for modelling, which code and database) → optional **I7 scope note** (“Note that …”, “… lies beyond the scope of this paper”). Roadmap paragraphs appear only in reviews and TC reports.
- I1: "The presence of alkali metals in cementitious materials is of great importance as the alkali concentration plays a key role for the chemical and mechanical properties of cementitious materials." [A_2022_Miron_CASHNK | 10.1617/s11527-022-02045-0]
- I2: "Thus, the alkali binding by C–S–H controls the distribution of alkali metals between solids and aqueous solution, and hence the pH values in the pore solution in Portland cements and blended cements" [A_2022_Miron_CASHNK | 10.1617/s11527-022-02045-0]
- I3: "Shehata and Thomas [6] proposed 600 mmol/L for Na + K as a lower limit for ASR expansion, Duchesne and Bérubé [7] reported 650 mmol/L, while Bagheri et al. [8] reported no expansion at a Na + K concentration below 300 mmol/L or at pH values < 13.2." [A_2025_Lothenbach_TC301 | 10.1617/s11527-025-02726-6]
- I4 (untested model): "However, this parameterization was never systematically tested against the pore solution data from hydrated cements with porosity normally around 10–15 vol%, where a rather small amount of pore water per unit mass of cement is available." [A_2022_Miron_CASHNK | 10.1617/s11527-022-02045-0]
- I4 (missing data): "Even though it is a proven approach to reduce the concentration of soluble alkalis, no systematic analysis on a threshold value to prevent ASR based on pore solution data has yet been conducted." [A_2025_Lothenbach_TC301 | 10.1617/s11527-025-02726-6]
- I5: "The aim of the present paper is to assess the CASH? model performance when modeling the alkali concentration in cement pore solutions." [A_2022_Miron_CASHNK | 10.1617/s11527-022-02045-0]
- I6: "In this study, we therefore look into the applicability of two models to predict the pore solution composition in hydrated cement pastes containing SCMs: Thermodynamic modelling [12] and the empirical model of Taylor [13]." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- I7: "Note that the presented thresholds and models do not eliminate the need for performance testing but are intended as an aid for efficient and informed design of performance test matrices." [A_2025_Lothenbach_TC301 | 10.1617/s11527-025-02726-6]

### 2.3 Methods (modelling subsection)
Write the modelling subsection as a fixed sequence of short declarative sentences: code → databases → C-S-H / solid-solution model → activity model with parameters → input (bulk composition, degree of reaction) → blocked or suppressed phases → assumptions such as equilibrium, temperature and homogeneity.
- "For the thermodynamic modelling, we used the geochemical software GEMS (https:// gems. web. psi. ch) [18], combining the PSI-Nagra thermodynamic database [19] with the cement-specific Cemdata18 database [12] and the CASH + NK model [20–22] to describe alkali uptake by C-S–H, which depends on the alkali concentration in solution, on the amount of C–S–H formed as well as on its Ca/Si." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- "Activity coefficients of aqueous species were calculated using the extended Debye-Hückel equation [22] and the common parameter values for KOH background electrolyte, ion size parameter å = 3.67 and bc = 0.123." [A_2022_Miron_CASHNK | 10.1617/s11527-022-02045-0]
- "Therefore, the DoR of the SCMs as input in the GEMS model was adjusted so that the portlandite content predicted by GEMS would approx. match the portlandite content measured experimentally by TGA." [B_2022_Babaahmadi_Clbinding | 10.1016/j.cemconres.2022.106924]
- Code sentence (generic): "GEMS is a broad-purpose geochemical modelling code which computes" … "equilibrium phase assemblage and speciation in a complex chemical system from its total bulk elemental composition." [A_2022_Bernard_MSH | 10.1617/s11527-022-02018-3]

### 2.4 Results and discussion (modelling papers)
Pattern: state what the figure shows (“Figure 4 shows …”) → describe the trend with numbers → compare model with experiment (agreement or bias, with direction) → attribute the deviation to a named cause (equilibrium assumption, DoR input, kinetics, homogeneous-system assumption, analytical artefact, reported raw-material oxides) → limit the claim (“Note that …”).
- "This is likely due to the inhomogeneity of the real concrete on the microstructural level, which is captured by the empirical Taylor model but not by the GEMS model as the latter simulates a fully homogenous system." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- "When using the CASH? model (original or fine-tuned), the measured OH- concentration (3 mM) is underestimated at the later hydration stages by around one order of magnitude (0.16 mM)." [A_2022_Miron_CASHNK | 10.1617/s11527-022-02045-0]
- "Apparently, Na concentrations are underestimated which is most likely due to systematically low reported Na2O levels in the raw materials and not to a deficiency in the model." [B_2016_Vollpracht_MSreview | 10.1617/s11527-015-0724-1]
- "The reason for underestimation may be related to the experimental system not reaching equilibrium (i.e. an immature binder tested at early age) and the conservative degree of reaction of GGBFS used here (60%, compared to the 70–80% reacted in experiments [42])." [A_2025_Jin_ASR_AAM | 10.1617/s11527-025-02781-z]

### 2.5 Conclusions (≈ 480 words; no citations, no figure refs)
**C1 one-sentence recap of what was done** (past tense: “This study investigated …”, “The paper investigates …”) → **C2 findings**, either as numbered/bulleted items (about half the A papers, introduced by “The key findings are:” / “The following conclusions can be drawn …”) or as 2–4 paragraphs, each with its key number → **C3 practical meaning or recommendation** → **C4 limitations and needed work** (“Further studies are needed to …”).
- C1: "The paper investigates the applicability of two theoretical models to predict how much of the Portland cement (PC) should be replaced with a specific SCM to keep the alkali concentration in the pore solution (Na + K) below a given threshold below which deleterious alkali-silica reaction (ASR) is assumed to be mitigated." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- C2: "The thermodynamic model predicted little impact of the alkali content of the PC and w/b-ratio on the required replacement level of the investigated SCMs." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- C3: "The models do therefore not replace concrete performance testing, but function as an aid in putting up focused testing programs." [A_2025_DeWeerdt_TC301 | 10.1617/s11527-025-02583-3]
- C4: "Further studies are needed to validate the proposed test method across a broader range of SCMs, with increased replication over the test duration to better define its precision limits." [A_2026_Sharbaf_solublealkali | 10.1617/s11527-026-03086-5]

---

## 3 Language statistics (A, P10 / P50 / P90 per paper; `stats.json` holds the full distributions)

| metric | Introduction | Body (methods + results + discussion) | Conclusions |
|---|---|---|---|
| mean sentence length (words) | 24.2 / 27.6 / 34.1 | 24.8 / 27.5 / 33.8 | 22.2 / 27.9 / 35.9 |
| 90th-pct sentence length | 36 / 42 / 54 | 41 / 46 / 60 | 32 / 44 / 60 |
| share of sentences > 35 words | 0.11 / 0.21 / 0.38 | 0.15 / 0.21 / 0.30 | 0.09 / 0.21 / 0.40 |
| share of sentences with a passive | 0.25 / 0.42 / 0.58 | 0.36 / 0.47 / 0.57 | 0.20 / 0.39 / 0.58 |
| we/our per 1000 words | 0 / 0 / 6.4 | 0 / 0.2 / 2.7 | 0 / 0 / 2.8 |
| “this study/paper/work” per 1000 | 0 / 1.5 / 4.0 | 0.0 / 0.8 / 1.7 | 0 / 1.9 / 6.3 |
| hedges per 1000 (may, could, suggest, likely, approx., …) | 2.5 / 8.2 / 13.6 | 6.1 / 10.8 / 15.1 | 0 / 8.1 / 15.9 |
| boosters per 1000 (clearly, significantly, crucial, novel, …) | 0 / 1.4 / 3.4 | 0.4 / 1.0 / 2.2 | 0 / 1.6 / 5.1 |
| was/were/had share of finite aux (tense) | 0.01 / 0.15 / 0.38 | 0.20 / 0.43 / 0.70 | 0.07 / 0.38 / 0.78 |
| connectives per 1000 | 6.1 / 10.7 / 16.8 | 6.5 / 9.1 / 11.2 | 2.6 / 8.5 / 15.3 |
| “however” per 1000 | 0 / 1.5 / 4.5 | 0.1 / 1.2 / 2.0 | 0 / 0 / 2.4 |
| semicolons per 1000 | 0 / 0 / 3.7 | 0.3 / 1.2 / 2.9 | 0 / 0 / 3.8 |
| citations per sentence | 0.55 / 0.98 / 1.57 | 0.11 / 0.29 / 0.77 | 0 / 0 / 0.10 |
| share of sentences citing | 0.29 / 0.47 / 0.67 | 0.07 / 0.19 / 0.37 | 0 / 0 / 0.07 |
| Fig./Table refs per 1000 | 0 / 0 / 1.4 | 2.0 / 4.8 / 7.3 | 0 / 0 / 0 |
| numerals per 100 words | 3.2 / 5.8 / 7.4 | 5.2 / 7.0 / 9.6 | 0.7 / 2.5 / 4.4 |

How to read the table:
- **Voice and person**: the default is impersonal. About 40–47 % of sentences contain a passive, and the subjects are “this study”, “the model”, “the thermodynamic model”. “We” is allowed (De Weerdt, Jin, Danner, Sharbaf use it), but the corpus median in Introduction and Conclusions is zero. Use it at most for decisions: “we used …”, “we therefore look into …”.
- **Tense**: the Introduction states background in the present tense (past share 0.15). Methods and results use the past tense for what was done or measured and the present for what a figure shows or a model assumes. The Conclusions mix the past (recap) and the present (general statements).
- **Hedging**: about 8–11 hedges per 1000 words, mostly *may, could, likely, suggest, indicate, approx.* Boosters are rare (about 1 per 1000). Avoid *novel, first time, crucial*. Sentences open with *This indicates that …* / *This suggests that …*, not *This clearly demonstrates*.
- **Connectives** (pooled per 1000 words): *due to / as a result* 1.8, *while* 1.5, *however* 1.3, *i.e./e.g.* 1.0, *although* 0.6, *therefore* 0.6, *thus* 0.5, *in addition* 0.4, *in contrast / on the other hand* 0.4. *Moreover* (0.24) and *furthermore* (0.21) are uncommon; do not stack them.
- **Sentence openers** (pooled counts): The 2047, This 513, In 489, For 238, However 231, A 153, It 150, These 144, As 133, To 89, At 86, After 67, Therefore 60, While 53, Moreover 51, Thus 51, Although 46 …
- **Semicolons** are rare, about one per 1000 words in the body and none in the median Introduction or Conclusions. Parentheses are frequent (body 11–31 per 1000) and carry abbreviations, values and conditions: “(w/b 0.5, 20 °C)”.

---

## 4 Terminology, symbols, units, citation format

Counts give the number of A papers (out of 34) that use each variant. Pick one variant and keep it consistent; M&S accepts both British and American spelling.

| item | corpus usage | recommended for ms-cemchem |
|---|---|---|
| C-S-H | “C–S–H” en dash 13 papers / “C-S-H” 20; C-A-S-H 14; C-(A)-S-H 6 | C-S-H, C-A-S-H, C-(A)-S-H, C-(N-)A-S-H, M-S-H; define once |
| pore solution | “pore solution” 20 papers (478 hits); “pore water” 7; “porewater” 2 | *pore solution* (Miron 2022 uses *porewater* in its title only) |
| cement | PC 20 papers; OPC 16; CEM I 9 | “Portland cement (PC)”, with CEM I for the EN type |
| SCM | SCM(s) 27 papers | SCM(s); silica fume (SF), metakaolin (MK), fly ash (FA), slag (or GGBFS); define every abbreviation at first use |
| water/binder | w/b 10 papers, w/c 9, written out 15 | “water-to-binder ratio (w/b)” and then w/b |
| concentration | mmol/L 6 papers (84 hits); M 11; mol/L 6; mM 3 | mmol/L for pore solution; M or mol/L for host solutions; never “mmol L−1” (0 hits) |
| mass fraction | wt% 21 papers; wt.% 18 | wt% (or wt.%; be consistent) |
| alkali content | Na2Oeq 8 papers | Na2Oeq (wt%) |
| temperature | °C in 30 papers; K 0 in A | °C; kelvin only in thermodynamic data tables (B layer) |
| energy | kJ/mol 3 papers; J/g 10 (R3 heat) | kJ/mol for ΔG corrections; J/g SCM for heat |
| degree of reaction | “degree of reaction” 10 papers, DoR 4, “reaction degree” 3 | degree of reaction (DoR) |
| software | GEMS 14 papers, GEM-Selektor 12, Cemdata18 15 (as CEMDATA18 in some), PHREEQC 5 | GEMS (GEM-Selektor v3.x) + PSI-Nagra 12/07 + Cemdata18 |
| spelling | modelling 13 / modeling 6; sulfate 24 / sulphate 13; aluminium 14 / aluminum 17 | British: modelling, aluminium; sulfate (IUPAC) |
| figure/eq./section refs | Fig. 34 papers (1023 hits); Figure at sentence start; Sect. 19; Eq. 16; “Section” 0 | “Fig. 3”, “Figs. 3–4”; “Figure 6 shows …” at sentence start; “Sect. 2.3”; “Eq. 1” |
| cement notation | stated as a key line: “Cement chemistry notation: C: CaO; A: Al2O3; F: Fe2O3; S: SiO2; S̅: SO3; c: CO2; H: H2O.” (Martins 2024) | only if reactions are written |

**Citation format (Springer basic numbered)**: square brackets in order of appearance, placed before the full stop. Examples: “[1]”, “[3–5]”, “[2, 7]”; an author name with *et al.* goes before the bracket, as in “Bagheri et al. [8] reported …” (25/34 papers write “et al. [n]”). In the reference list, authors are given as surname + initials without periods, followed by the year in parentheses, the title, the abbreviated journal, volume:pages. Example from the corpus: "Lothenbach B, Kulik DA, Matschei T, Balonis M, Baquerizo L, Dilnesa B et al (2019) Cemdata18: a chemical thermodynamic database for hydrated Portland cements and alkali-activated materials." [A_2026_Sharbaf_solublealkali | 10.1617/s11527-026-03086-5]. Journal abbreviations follow ISO style without periods (“Cem Concr Res”).

---

## 5 How theory is presented

- **Equation density is low.** Median 0 numbered equations in A. M&S modelling papers do not derive the solid-solution or activity models; they cite them (Kulik 2022, Miron 2022a, Lothenbach 2019) and give only (i) the model name, (ii) its parameters, often in a table, and (iii) any changed parameter with its value. Example: the ΔG° corrections of −7.0/−5.0 kJ/mol in Miron 2022. Empirical models, such as Taylor’s linear alkali-binding isotherm in De Weerdt 2025, are written out with their binding factors in a table and uploaded as an Excel file in the ESM. Long derivations, fits and full datasets go to the ESM, not to an appendix in the main text.
- **Reactions** are written in cement notation and numbered “Eq. 1–6” where hydration stoichiometry matters (Mrak 2021).
- **Assumptions are stated as assumptions** (homogeneous system, equilibrium, DoR from the literature), and the consequence of each is spelled out in the Discussion: “The thermodynamic model assumes homogenous hydrate distribution and thus predicts that portlandite has to be depleted before C–S–H starts to bind more alkalis, …” (De Weerdt 2025, Conclusions).
- **Translating model output into engineering statements.** The corpus turns modelled concentrations into (a) **thresholds** (Na + K ≤ 300 mmol/L), (b) **required replacement levels** (“20% SF, 20% MK, 40–50% FA and 60–70% slag”), (c) **rankings of SCMs**, and (d) **what the model can and cannot replace** (performance testing). Each engineering statement carries its boundary conditions: temperature, w/b, Na2Oeq of the PC, and the aggregate reactivity the threshold refers to.
- **Model–experiment comparison** is mostly graphical: concentration vs replacement level with experimental symbols and model lines, or measured vs calculated. It is summarised in words such as “good agreement”, “reasonable agreement”, “within an order of magnitude”, “underestimated by around one order of magnitude”. The A layer rarely gives formal error metrics. Exceptions: mean relative errors (8.9 %) in Boiger 2025, and R² values for empirical correlations. B-layer model papers report mean absolute errors (Miron 2022a: “The mean absolute errors are 7.4% and 24.4% …”). For a benchmark paper, report the numeric metric (e.g. RMSE in log10 units) **and** the verbal judgement, and state the direction of the bias.

---

## 6 Figures, tables, captions, citation density

- Caption style: “Fig. 4 Na + K concentration in the pore solution for cement paste containing increasing replacement levels of a FA, b SF, c MK and d slag. The symbols present experimental data, the dashed lines the predictions by thermodynamic modelling and the solid lines the values predicted by the empirical Taylor model. …” (De Weerdt 2025). Panel letters are unbracketed and set italic in print (“a …, b …”). The caption says what the symbols and lines mean, lists the fixed conditions (w/b, Na2Oeq, temperature), gives the number of data points and the data source (“The data was extracted from reference data [1, 2, 4]”, “Adapted from [32]”), and may end without a full stop.
- Tables hold the XRF oxide composition (wt%), mineralogy (XRD-Rietveld, wt%), model inputs (DoR rules, binding factors, phases allowed/suppressed) and thermodynamic data (ΔfG°, ΔfH°, S°, Cp°, V°) for added phases. Table titles are noun phrases (“Table 2 Parameters used for the Taylor model for PC and the various SCMs”).
- Typical figures in a thermodynamic or pore-solution paper: a DoR-vs-replacement input plot (Fig. 1); phase assemblage vs SCM replacement or time (stacked, g/100 g binder or cm³/100 g); pore-solution concentrations vs replacement or age (model line + literature symbols, log axis for Al, Si, S); distribution of Na and K between pore solution, C-S-H and unreacted material; measured vs calculated, or a sensitivity plot.
- Citation density: the Introduction cites in about half of its sentences, about one reference per sentence. The body cites in about 19 % of sentences, mostly in methods and when comparing with the literature. The Conclusions practically never cite.

---

## 7 Applying this to the D3 paper (GEMS/Cemdata18 benchmark + ion-specific alkali uptake model for C-S-H)

These are notes on form only. Every technical statement must come from `/home/luck/xzy/0970project/D3_poresolution` (G1_REPORT.md, results/); nothing here is a finding.
- Suggested skeleton, consistent with the corpus: `1 Introduction` → `2 Materials and methods` (`2.1 Pore solution database` [cf. Lothenbach 2025 §2], `2.2 Thermodynamic modelling` [code, databases, C-S-H model, activity model, DoR rules, suppressed phases, solver], `2.3 Ion-specific alkali uptake model`, `2.4 Benchmark metrics and hold-out`) → `3 Results` → `4 Discussion` (bias attribution: model, inputs, data) → `5 Limitations and perspectives` (as in Jin 2025) → `6 Conclusions`. Target about 7000 words, 8–10 figures, 3–5 tables, input tables and per-source residuals in the ESM.
- Use the corpus’s comparison vocabulary (agreement / underestimate by … / within an order of magnitude), but always alongside the numeric metric, its uncertainty, the number of records and source groups, and the direction of the bias.
- Engineering translation: state what the benchmark means for predicting the Na + K threshold or SCM replacement level, with boundary conditions, and add a sentence on what the model does not replace (performance testing).
