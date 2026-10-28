# STYLE.md — Engineering Fracture Mechanics: quasi-brittle fracture and size effect of concrete (key `efm-sizeeffect`)

Local use only; do not redistribute. Corpus: `CORPUS.md` (A layer = EFM, 15 papers, 3 of them held out; B layer = M&S / CCR / IJSS / JEM-ASCE plus IJF / JAM / TAFM / Materials, 20 papers).
Statistics: 32 distillation papers (hold-outs `A_augusthus2021`, `A_zhu2020`, `A_miarka2020` excluded), computed by `style_check.py --build` → `stats.json`.
Every quoted sentence below is verbatim from `text/<key>.txt` (PDF extraction; ligatures and hyphenation artefacts kept). The DOI comes after the key.
Target paper: C3, a size-effect transition law validated on public single-lab data (Hoover–Bažant 2013 and a second single-lab set) with a pre-registered geometry hold-out.

---

## 1. Macro structure

### 1.1 Section templates found in the corpus
| Paper type | Top-level sections (corpus examples) |
|---|---|
| Experimental database / test campaign | Introduction → Test specimen details → Description of tests → Testing of standard material characteristics → Size effect tests with different notch depths → Size effect tests of beams → Summary and conclusions (`A_hoover2013`); Introduction → Description of the experiments → Tests results → Determination of the fracture energy → Conclusions (`A_pijaudier2022`) |
| Model + validation against data | Introduction → model description → identification of material parameters → simulations vs. experiments → discussion → Conclusions (`A_elias2015`, `A_elias2020`, `A_friedrich2026`, `A_khan2023`) |
| Law / formula + verification on one data set | Introduction (with an embedded review of SEL Type 1/Type 2) → derivation → calibration ("To calibrate the deterministic USEL ...") → Conclusions (`B_hoover2014usel`, JEM technical paper, about 6 000 words) |
| Comparative critique of competing laws | Introduction → review of energetic SEL Types 1 and 2 → summary of data → comparison of optimum fits → comparison in terms of crack-length effect → Conclusion (`B_hoover2014bem`); Introduction → Progress-retarding controversies → Conclusions (`A_carloni2019`) |
| Statistical identification method | Introduction → Regression model and assumptions → Residual diagnostics → Transformation and change in error structure → Asymptotic results → Conclusion (`B_pathirage2025`) |

**Suggested template for C3** (based on the ‘law + verification’ and ‘comparative critique’ rows): 1 Introduction; 2 Size effect laws and the Type 1–Type 2 transition (SEL, USEL, BEM, cohesive asymptotics); 3 Derivation of the transition law; 4 Data and identification protocol (single-batch data, pre-registered hold-out, error measure); 5 Results (calibration, hold-out prediction, independent data set, comparison with USEL/BEM); 6 Discussion (physical meaning of the parameters, limits of validity, cohesive-FE check); 7 Conclusions; Appendix (derivation details, fitting algorithm, data processing).

### 1.2 Proportions (corpus P10 / median / P90; n = 27 papers whose section boundaries were recovered)
| Quantity | P10 | Median | P90 |
|---|---|---|---|
| top-level sections (Intro … Conclusions) | 4 | 5 | 7 |
| words from Introduction to end of Conclusions | 4 730 | 6 580 | 10 330 |
| Introduction share of body | 6 % | 14 % | 23 % |
| Conclusions share of body | 2 % | 6 % | 13 % |
| figures (highest Fig. number) | 7.6 | 13 | 25 |
| tables | 0 | 2 | 6.4 |
| numbered equations | 5.6 | 15 | 52 |
| equations per 1000 body words | 0.85 | 2.4 | 6.3 |
| conclusions written as a numbered/bulleted list | — | yes in ≥ 50 % | — |
| abstract length (words in well-formed sentences, n = 20 recovered abstracts) | ≈ 125 | ≈ 195 | ≈ 260 |

### 1.3 Figures, tables, appendices
* Figures appear in the order ‘geometry/specimen sketch → load–CMOD curves → size effect plot log σN vs log D → notch-depth (α) plot → error/parameter comparison’. The core evidence of a size-effect paper is the **double-logarithmic size effect plot** with asymptotes. `A_carloni2019` and `B_hoover2014bem` add a **crack-length (α) plot** at fixed D.
* Tables list mix and specimen data (dimensions, number of specimens per family, CoV), fitted parameters per model, and CoV of fit per curve (`B_hoover2014bem` Tables 1–3).
* Appendices are short. They hold derivations or special cases (`B_baldassari2023` Appendix A: "Here we provide the flexural strength size effect for plain specimens choosing the original FFM approach [5], i.e. Eq. (3)."). Data and code are pointed to a website or repository (`A_hoover2013`: "numerous additional details ... are posted on a website").
* EFM front matter includes a **highlights** list and **4–6 keywords**, e.g., ‘Quasibrittle materials / Concrete structures / Fracture mechanics / Energetic size eﬀect’ (`A_carloni2019`) or ‘Concrete fracture / Scaling of strength / Fracture testing / Statistical scatter’ (`A_hoover2013`) (one keyword per line in the source).

---

## 2. Rhetorical moves

### 2.1 Abstract (single paragraph, ≈ 125–260 words, no citations: corpus P90 of cited sentences = 0)
| Move | Typical form | Corpus example |
|---|---|---|
| A1 Problem/limitation of the existing evidence | "Although …, their evaluation is ambiguous because …" | "Although hundreds of concrete fracture tests exist, their evaluation is ambiguous because they have limited ranges of specimen size, initial notch depth and postpeak response, and refer to different concretes, different batches of concrete, different ages, different environmental conditions, different loading rates and test procedures, and different specimen types." — `A_hoover2013` 10.1016/j.engfracmech.2013.08.007 |
| A2 What is done (often an inverted or passive opening) | ‘Presented is …’, ‘… is analysed by …’ | "Presented is an experimental investigation of unprecedented comprehensiveness and low scatter, using specimens made from one batch of concrete." — `A_hoover2013` |
| A3 Data basis | "The current study is based on …" | "The current study is based on recently obtained comprehensive fracture test data for three-point bend beams cast from one batch of the same concrete and cured and tested under identical conditions." — `B_hoover2014usel` 10.1061/(ASCE)EM.1943-7889.0000627 |
| A4 Key finding, stated against the old model | "The test data reveal that …" | "The test data reveal that the Type 1-Type 2 transition in the previous universal law has insufficient accuracy and cannot be captured by Taylor series expansion of the energy release rate function of linear elastic fracture mechanics." — `B_hoover2014usel` |
| A5 Quantified fit | "… is shown to fit … with a coefficient of variation of only …" | "The new universal law is shown to fit the comprehensive data quite well, with a coefficient of variation of only 2.3%." — `B_hoover2014usel` |
| A6 Verdict / recommendation | ‘Thus, … suffices to conclude that …’ (`B_hoover2014bem`); ‘… should be avoided …’ | "The linear regression plot suggested by RILEM should be avoided for the statistical inverse problem of the size-effect method." — `B_pathirage2025` 10.1617/s11527-024-02565-x |

### 2.2 Introduction (median 14 % of body; median 32 % of sentences carry a citation; 1.8 citation groups per 100 words)
Sequence (Hoover 2013, Hoover–Bažant 2014, Grassl 2012, Friedrich 2026, Pathirage 2025):
1. **I1 Practical stake of scaling**: extrapolating from the laboratory to the structure. "A persistent challenge in structural engineering lies in accurately translating the mechanical behavior observed in small-scale laboratory tests into reliable predictions for full-scale structures." — `A_friedrich2026` 10.1016/j.engfracmech.2026.112234; "Size-effect is one of the most important consequence of fracture mechanics theory." — `B_pathirage2025`
2. **I2 Definitions and theory review** (SEL, Type 1 vs Type 2, FPZ, asymptotes; the size effect is *defined* explicitly): "Here, size effect is the dependence of the dimensionless nominal strength of a beam on its depth, when geometrically similar structures are compared." — `B_grassl2012` 10.1016/j.ijsolstr.2012.03.023; "The Type 1 size effect occurs in structures that have no notches nor preexisting large cracks and fail right after the initiation of a macro-crack from a smooth surface." — `A_hoover2013`
3. **I3 Competing models / controversy**: "Currently, three main theories for describing the size effect are promoted in the literature, namely statistical theories of random strength, stress-redistribution and energy release, and theory of crack fractality (Bažant, 2002)." — `B_grassl2012`; "It is thus not surprising that rather different theoretical models have happily coexisted for a long time, and polemics about their differences have not resulted in a universal consensus." — `B_hoover2014bem` 10.1061/(ASCE)EM.1943-7889.0000632
4. **I4 Gap (experimental or theoretical)**: "An especially important gap of knowledge, which has, for example, hampered a critical appraisal of the Hu-Duan boundary effect model [13–18], exists in the transition between the Type 1 and Type 2 size effects." — `A_hoover2013`; "These two size effects are fundamentally different and transition between them has been one important gap in experimental information." — `B_hoover2014usel`
5. **I5 Objective(s)**, often split into a principal and a secondary one: "The objective of this paper is to develop and experimentally verify a new formula for the combined effects of structure size and crack or notch depth, called the universal size-shape effect law (because the variation of crack depth represents an effect of structure shape, or geometry)." — `B_hoover2014usel`; "Thus, as the secondary objective of this study, the errors in the predictions of size effect fracture parameters are investigated …" — `B_caner2018` 10.1016/j.ijsolstr.2018.11.029
6. **I6 Approach and data, including which subset calibrates and which predicts**: "Only the responses of the beams with the deepest notch are used to identify the deterministic model parameters, while the rest of the test data is subsequently compared to the deterministic model predictions." — `A_elias2015` 10.1016/j.engfracmech.2015.01.004 (the closest corpus precedent for a pre-registered hold-out)
7. **I7 Assumptions and scope**: "The present work is based on several assumptions." — `B_grassl2012`
8. **I8 Roadmap** (optional; about 1 paper in 3): "This paper is organized as follows." — `B_mishra2025`

### 2.3 Discussion (inside the results section or as a separate "Discussion")
* Fit comparisons use **the same parameters for all data**. Deviations are quantified in % or as CoV of fit: "The BEM and SEL fits are optimized in Figs. 2 and 3 with the restriction that all the material parameters of each model be the same for all tests." — `B_hoover2014bem`
* Calibration and prediction subsets are separated explicitly: "In particular, the fracture parameters Gf and cf should not be influenced by the data for beams with no notches (Type 1 data) or shallow notches, and fr‘ , Db , lp , and r should not be influenced by the data for deep notches." — `B_hoover2014usel`
* Objections are anticipated in question–answer form (Bažant school): "Wouldn’t a solution with the cohesive crack model or a damage model be more appropriate?" followed by "Not in the present context, because …" — `B_hoover2014usel`
* Limits are stated plainly: "However, this remains to be proven experimentally." — `B_hoover2014usel`; "It should be noted that the present study does not aim to reproduce statistical size effect on strength, for which most likely a larger auto-correlation length is required as reported in Vořechovskỳ (2007) and Grassl and Bažant (2009)." — `B_grassl2022` 10.1016/j.ijsolstr.2022.112086

### 2.4 Conclusions (median 6 % of body; citations almost absent, P90 = 0.56 per 100 words; no ‘we’ in the median paper)
1. **C1 One- or two-sentence recap of what was done** (passive or ‘This study examined …’, `A_friedrich2026`): "Random meso-scale analyses of three point bending tests were performed to investigate the influence of the size effect on fracture process zones, which were determined from an average of increments of energy just after peak load." — `B_grassl2012`
2. **C2 Lead-in to a list**: "The following conclusions can be drawn." — `B_pathirage2025`; "The study resulted in the following conclusions: …" — `B_grassl2012`
3. **C3 Numbered findings**, each a self-contained claim, mostly in the present tense, with numbers: "The new USEL fits the measured nominal strength quite well, with an overall COV of only 2.3%." — `B_hoover2014usel`; "In particular, it is shown that when BEM is used as a predictive theory, the CoV of errors of fit can be significant, in the order of 50%." — `A_carloni2019` 10.1016/j.engfracmech.2019.04.036
4. **C4 Practical or standardisation consequence**: "In summary, the fracture parameters should only be obtained in the space (P vs. D)." — `B_pathirage2025`
5. **C5 Limitation and the next experiment**: "Therefore, additional experiments, which provide local information on fracture processes, should be carried out to verify the local results presented here." — `B_grassl2012`

---

## 3. Language statistics (corpus P10 / median / P90; values computed by `style_check.py`)

| Metric | Abstract | Introduction | Conclusions | Body |
|---|---|---|---|---|
| mean sentence length (words) | 18.8 / 25.0 / 33.4 | 22.1 / 23.8 / 32.6 | 20.0 / 25.3 / 33.0 | 20.9 / 24.0 / 27.8 |
| share of sentences > 35 words | 0 / .13 / .50 | .06 / .16 / .39 | 0 / .16 / .33 | .08 / .15 / .27 |
| passive share (sentences with a passive verb group) | .42 / .69 / 1.0 | .29 / .49 / .66 | .20 / .47 / .70 | .43 / .50 / .65 |
| we/our/us per 1000 words | 0 / 0 / 0 | 0 / 0 / 2.9 | 0 / 0 / .5 | 0 / .5 / 4.0 |
| hedges per 1000 words | 0 / 0 / 8.5 | 0 / 4.3 / 7.6 | 0 / 2.2 / 11.1 | 2.7 / 4.8 / 7.8 |
| boosters per 1000 words | 0 / 0 / 0 | 0 / .9 / 2.8 | 0 / 0 / 4.4 | .4 / 1.2 / 2.1 |
| connectors per 1000 words | 0 / 4.1 / 10.0 | 3.8 / 8.0 / 12.6 | 0 / 5.1 / 10.9 | 4.1 / 7.1 / 9.9 |
| past auxiliaries share (was/were/had vs is/are/has/have) | 0 / 0 / .29 | 0 / .10 / .33 | 0 / .07 / .43 | .04 / .19 / .34 |
| citation groups per 100 words | 0 / 0 / 0 | .72 / 1.77 / 2.39 | 0 / 0 / .56 | .58 / .83 / 1.26 |
| numerals per 100 words | 0 / .8 / 9.0 | 1.6 / 3.5 / 8.2 | 0 / 1.5 / 7.3 | 3.5 / 4.7 / 8.5 |
| semicolons per 1000 words | 0 / 0 / 4.2 | 0 / 0 / 7.1 | 0 / 0 / 2.8 | .2 / 1.1 / 5.5 |
| em-dashes per 1000 words | 0 / 0 / 0 | 0 / 0 / 2.4 | 0 / 0 / .3 | 0 / 0 / 1.0 |
| sentences opening with This/These/It/There | 0 / .08 / .33 | .05 / .12 / .22 | 0 / .10 / .18 | .06 / .11 / .17 |
| sentences opening with a connector | 0 / 0 / .14 | .02 / .08 / .19 | 0 / .09 / .15 | .05 / .07 / .15 |
| AI-flavoured lexicon per 1000 words | 0 / 0 / 3.6 | 0 / 0 / 2.2 | 0 / 0 / 0 | 0 / .2 / 1.2 |

A-layer (EFM) vs B-layer medians differ little. EFM introductions carry more citations (1.94 vs 1.54 per 100 words) and more hedges (4.8 vs 2.7 per 1000), but fewer connectors (6.1 vs 9.1 per 1000) and fewer long sentences (12 % vs 17 %).

Further observations (body text, 184 000 words):
* **Sentence length distribution**: P10 = 11, P25 = 15, median = 22, P75 = 30, P90 = 39 words. Long, clause-rich sentences (35–60 words) are normal in Bažant-school introductions. Do not chop them into 12-word fragments.
* **Tense**: present tense for laws, definitions and the paper's own claims ("The BEM does not properly distinguish between Type 1 and 2 size eﬀects." — `A_carloni2019`). Past tense for what was done or tested ("Fifteen notched beams were tested in a three-point bending test setup." — `A_rahman2024` 10.1016/j.engfracmech.2024.109965). Present perfect for the state of the field ("This effect has been extensively investigated in the literature and was recently adopted in specific design standards [1]." — `B_pathirage2025`).
* **Person**: impersonal by default (‘the present study’, 19/32 papers; ‘the authors’, 17/32). ‘We’ appears in 18/32 papers, mostly in method sections ("We compare experimental and numerical results in terms of both local and global quantities." — `B_mishra2025`), never in the median Conclusions.
* **Connectors per 10 000 words**: however 13.0, i.e. 8.4, therefore 8.0, thus 7.4, e.g. 3.7, although 3.6, moreover 2.7, on the other hand 2.4, whereas 2.3, finally 2.3, nevertheless 2.3, furthermore 2.1, consequently 2.1, in addition 2.0, hence 1.7. Prefer *however/therefore/thus/although*. Avoid stacks of *moreover/furthermore/additionally*.
* **Hedges per 10 000**: may 6.7, could 6.3, possible 3.8, approximately 2.5, indicates 2.4, might 2.3, typically 2.2, almost 2.1, generally 2.1, tends 2.0. **Boosters**: significantly 3.2, strongly 1.8, clearly 1.7, always 1.7. Bažant-school papers use strong evaluative wording ("grossly deviates", "distinctly inferior", "glaring gap"), but it is always attached to a number or a figure.
* **Reporting verbs per 10 000**: shown 18.8 (‘It is shown that …’, ‘As shown in Fig. …’), present(ed) 19, proposed 8.9, predicted 3.8, indicate(s) 4.7. Rare: *demonstrate(d)* ≈ 2.8, *confirmed* 0.8, *reveal* (used for data: "Comparisons with the test data on size eﬀect reveal extensive disagreements." — `A_carloni2019`).
* **Frequent sentence openers**: "In the …", "It is …", "This is …", "In this …", "For the …", "Note that …", "However, the …", "Since the …", "The results …", "Therefore, the …", "It should be noted that …", "According to …", "As shown in …".
* **Semicolons** appear in enumerations inside parentheses (‘(1) …; (2) …’, as in `A_hoover2013`'s abstract) and in lists of conditions, not as stylistic clause joiners. **Em-dashes** are rare (median 0) and are a recognisable Bažant mannerism ("The scaling is a fundamental property of every physical theory—if it is not understood, the theory itself is not understood." — `A_carloni2019`). Do not imitate them in a non-Bažant voice.

---

## 4. Terminology, symbols, units, references

| Item | Convention (papers using it out of 32) |
|---|---|
| quasi-brittle / quasibrittle | both common (27 / 22). Bažant group: *quasibrittle*; EFM others: *quasi-brittle*. Pick one and keep it. |
| Type 1 / Type 2 size effect | Arabic numerals (7 papers, 123 uses) ≫ Roman "Type II" (3 papers). Define both at first use. |
| size effect law (SEL), universal size(-shape) effect law (USEL), boundary effect model (BEM), fracture process zone (FPZ), crack mouth opening displacement (CMOD), linear elastic fracture mechanics (LEFM) | abbreviation defined at first use in the abstract **and** again in the text |
| three-point bending / three-point bend (TPB, 3PB) | hyphenated "three-point bending" (21) is preferred over "three point bending" (8) |
| nominal strength σN = cN Pu/(bD); D = beam depth (characteristic size); α0 = a0/D relative notch depth | as in `B_hoover2014usel` Eq. (1) |
| Gf (initial fracture energy, area under the initial tangent of the softening law) vs GF (total fracture energy, work-of-fracture) | always distinguish: "Whereas the SEL corresponds to the area under the initial tangent of the softening bilinear stress-separation curve of the cohesive crack model, which represents the initial fracture energy Gf (and can be used to determine Gf from size effect tests), Hu and Duan’s BEM uses the total area under the softening curve, which represents the total fracture energy GF (Hu and Wittmann 2000; Duan et al. 2006)." — `B_hoover2014bem` |
| cf effective FPZ length; ft′ tensile strength; fr∞ large-size modulus of rupture; Db boundary-layer depth; lch = EGF/ft² Irwin/Hillerborg length | define each symbol in the sentence where it first appears ("where … = …") |
| error measure | ‘coefficient of variation (CoV) of the errors of fit’, defined: "(COV; defined as the RMS error divided by the mean of all data)" — `B_hoover2014bem`. ‘CoV’ and ‘COV’ both occur. Choose one. |
| units | SI: mm, MPa, N/m or J/m² for fracture energy (13 papers), kN for loads. US units only in parentheses (`A_hoover2013` gives in. and mm). |
| spelling | AmE (behavior 26, modeling 23) slightly more common than BrE (behaviour 18, modelling 18). EFM accepts either, but be consistent. |
| references | EFM: numbered in square brackets in order of appearance ([1], [2,3], [13–18]) in 23 of 32 papers; author–year is used in JEM/IJSS sources. Elsevier reference style; cite the journal version, not the preprint. Standards: RILEM TC-50 FMC (work-of-fracture), RILEM TC-89 FMT (size effect method), fib Model Code 2010. |

---

## 5. How theory is presented

* **Equation density**: median 15 numbered equations (2.4 per 1000 words). Laws are written in full in the main text: SEL Type 2, Type 1 and the universal law, each with an equation number, parameter definitions and asymptotes. Lengthy derivations (asymptotic matching, special-case limits) go to an appendix or to a cited companion paper (`A_hoover2013`: "The analysis is relegated to a follow-up paper.").
* **The asymptotic properties are the main argument**: the law is checked against small-size and large-size limits before it is fitted. "The universal size-shape effect law is a law that describes the dependence of nominal strength of specimen or structure on both its size and the crack (or notch) length, over the entire range of interest, and exhibits the correct small-size and large-size asymptotic properties as required by the cohesive crack model (or crack band model)." — `B_hoover2014usel`
* **Each parameter gets a physical meaning or is labelled empirical**: "The only purpose of the transition parameter l is to provide a smooth transition between the Type 1 and 2 behaviors." — `B_hoover2014usel`; "Here B and the transitional structure size D0 are empirical parameters to be identified by data fitting …" — `B_hoover2014usel`
* **Mathematical results become engineering consequences** (design safety, testing standards, extrapolation): "This is a serious issue because the BEM will grossly overestimate the mean strength of large-size structures, which would lead to an unsafe design." — `A_carloni2019`; "While it is clear that estimation of fracture parameters from nonfracture tests can never replace fracture testing of notched specimens, an improved formula with a known standard deviation can nevertheless serve a useful purpose for preliminary design and for approximate analysis of structures with not too high fracture sensitivity." — `B_bazant2002` 10.1016/S0008-8846(01)00723-2
* **Identification protocol stated step by step** (which parameters come from which subset, the optimiser, the weights): "The trust-region-reflective optimization algorithm (Coleman and Li 1994, 1996) was used."; "Therefore, these parameters were determined first by separate fitting of specimens with deep notches (a 5 0:30, 0:15) and specimens with shallow or no notches (a 5 0), and only the remaining ones, i.e., k, p, and q were identified by simultaneous optimal fitting of all the data." — `B_hoover2014usel` (PDF glyph errors as in source)
* **Statistical honesty**: error bars (mean ± 1 SD), the number of replicates, and an explanation when SDs are not reported: "For the experiments, standard deviations are not presented, since only a small number of beams for each size and geometry was tested, rendering any estimate of standard deviation inaccurate (Grégoire et al., 2011)." — `B_grassl2012`

---

## 6. Figure captions and citation density

* **Caption format (EFM)**: ‘Fig. N.’ followed by a noun phrase and a full stop. Panels are labelled ‘(a) … (b) …’ inside the caption. Captions are descriptive and do not draw conclusions. Examples: "Fig. 3. Optimum ﬁtting of size eﬀect data by using Eq. (5)." / "Fig. 4. Type 1 size eﬀect: (a) schematic of energetic and energetic-statistical Type 1 size eﬀect curves, and (b) comparison with experimental data." (`A_carloni2019`); "Fig. 2. Comparison of experimental load–CMOD curves and simulated responses obtained by automatic optimization." (`A_elias2015`). Abbreviations and CoV conventions may be explained in the caption: "Average concrete compressive (fc′ ) and splitting tensile strength (ft′ ) versus the age of the concrete (CoV within parentheses)." (`A_rahman2024`).
* **In-text references to figures**: ‘As shown in Fig. X’, ‘(Fig. 1)’, "In Figs. 4 and 5, these plots are created and compared with the data from Hoover et al. (2013)."
* **Citation density**: Introduction median 1.8 citation groups per 100 words (P10–P90: 0.7–2.4), with 16–45 % of sentences cited. Body 0.83 per 100 words. Conclusions about 0. Abstract 0. Citations are grouped and ranged ("[13–18]"). A model family is typically introduced with 2–4 references in one bracket.

---

## 7. Checker and caveats
* `style_check.py` recovers section boundaries from PDF text heuristically. Some corpus papers lose the abstract or conclusions (two-column order), so n varies per section (abstract 21, introduction 27, conclusions 28, body 32).
* The bands are corpus descriptions, not targets to maximise. A draft lying inside [P10, P90] on about 80 % of the metrics reads like a corpus paper; the leave-one-out median of corpus papers is 0.806 (intro + conclusions).
* The A layer is thin for Hu–Duan (BEM) voices: the only CC-BY EFM paper (Hu 2024, 10.1016/j.engfracmech.2024.110074) could not be fetched legally (repository blocked). `B_han2025` (Materials, Hu group) is used instead. See CORPUS.md, section ‘pending user supply’.
