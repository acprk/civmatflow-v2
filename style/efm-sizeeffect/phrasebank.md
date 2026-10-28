# phrasebank.md — efm-sizeeffect (EFM, quasi-brittle fracture / size effect of concrete)

Every entry is a verbatim sentence or clause from `text/<key>.txt` (the DOI follows the key; see CORPUS.md). PDF artefacts are kept as they appear in the source (ligatures such as ‘eﬀect’, a missing hyphen such as ‘sizeeffect’, glyph errors in ASCE PDFs). Reuse the **frame** of a sentence, not its content.
Verify all entries with: `python scripts/s11_verify_quotes.py` (it checks every quoted string against text/).

DOIs used: A_hoover2013 10.1016/j.engfracmech.2013.08.007 · A_carloni2019 10.1016/j.engfracmech.2019.04.036 · A_elias2015 10.1016/j.engfracmech.2015.01.004 · A_elias2020 10.1016/j.engfracmech.2020.107160 · A_friedrich2026 10.1016/j.engfracmech.2026.112234 · A_pijaudier2022 10.1016/j.engfracmech.2022.108630 · A_rahman2024 10.1016/j.engfracmech.2024.109965 · A_khan2023 10.1016/j.engfracmech.2023.109439 · A_suarez2023 10.1016/j.engfracmech.2023.109356 · A_zhang2026 10.1016/j.engfracmech.2026.112445 · A_puccia2022 10.1016/j.engfracmech.2022.108956 · B_hoover2014usel 10.1061/(ASCE)EM.1943-7889.0000627 · B_hoover2014bem 10.1061/(ASCE)EM.1943-7889.0000632 · B_hoover2014ijf 10.1007/s10704-013-9926-0 · B_grassl2012 10.1016/j.ijsolstr.2012.03.023 · B_grassl2009 10.1016/j.ijsolstr.2009.12.010 · B_grassl2022 10.1016/j.ijsolstr.2022.112086 · B_pathirage2025 10.1617/s11527-024-02565-x · B_caner2018 10.1016/j.ijsolstr.2018.11.029 · B_bazant2002 10.1016/S0008-8846(01)00723-2 · B_bazant2022 10.1115/1.4054221 · B_nguyen2020 10.1115/1.4047215 · B_han2025 10.3390/ma18081877 · B_baldassari2023 10.1016/j.tafmec.2023.103787 · B_gangnant2016 10.1016/j.cemconres.2016.07.010 · B_mishra2025 10.1016/j.cemconres.2025.108012 · B_karrer2022 10.1617/s11527-022-02011-w · B_gudzulic2025 10.1617/s11527-025-02815-6 · B_das2019 10.1061/(ASCE)EM.1943-7889.0001628 · B_alam2019 10.1016/j.ijsolstr.2019.08.003

## 1. Establishing why scaling matters
- "A persistent challenge in structural engineering lies in accurately translating the mechanical behavior observed in small-scale laboratory tests into reliable predictions for full-scale structures." — A_friedrich2026
- "Large-scale experimental campaigns, while ideal, are often impractical due to their high cost and complexity [4]." — A_friedrich2026
- "Size-effect is one of the most important consequence of fracture mechanics theory." — B_pathirage2025
- "For plain concrete structures subjected to bending, the nominal strength depends strongly on the size of the structure." — B_grassl2012
- "The model parameters are usually obtained from small size laboratory specimens, but applying these parameters to large structures poses difficulties." — A_elias2015
- "As a matter of fact, evaluating the size effect in quasi-brittle materials is now considered a fundamental benchmark for quantitatively validating computational fracture models [13]." — A_friedrich2026

## 2. Defining terms and the two types of size effect
- "Here, size effect is the dependence of the dimensionless nominal strength of a beam on its depth, when geometrically similar structures are compared." — B_grassl2012
- "The Type 1 size effect occurs in structures that have no notches nor preexisting large cracks and fail right after the initiation of a macro-crack from a smooth surface." — A_hoover2013
- "The Type 2 size effect occurs when either a deep notch or a long stress-free crack has grown in a stable manner before reaching the maximum load (as is typical of reinforced concrete)." — A_hoover2013
- "In Type 2 asymptotic behavior, the notch or pre-existing macro-crack is much larger than the fracture process zone (FPZ), while in Type 1 the macro-crack at maximum load is approximately of the size of the FPZ." — A_hoover2013
- "The size effect is understood as any dependence of sN on D, which is a feature typical of fracture or damage mechanics." — B_hoover2014usel
- "Here, fracture process zone is defined as the zone in which energy is dissipated at a certain stage of analysis." — B_grassl2012
- "The deterministic size effect is also called energetic, because it can be derived from the limit case of energy release when the crack length approaches zero." — B_hoover2014usel

## 3. Reviewing models neutrally
- "Modelling approaches for fracture in concrete are divided in three groups." — B_grassl2012
- "These approaches can be broadly classified into two main groups: models based on continuum mechanics and models that explicitly account for the random nature of the material microstructure." — A_friedrich2026
- "In such models, energy dissipation is usually regularized by a mesh-adjusted constitutive relationship – the crack band model [6]." — A_elias2020
- "However, an asymptotic scaling law was discovered by Bažant in the 1980s [4]." — B_pathirage2025
- "It involves two key material parameters: the fracture energy Gf characterizing a stable crack propagation and the effective length of the fracture process zone cf which represents the length of the equivalent linear elastic crack that gives the same unloading compliance as the actual crack in a sufficiently large specimen at peak load." — B_pathirage2025
- "It was first proposed by Hu and Wittmann (2000) and subsequently elaborated on in a series of papers by Hu and Duan (Duan and Hu 2004; Duan et al. 2006; Hu 2002; Hu and Duan 2007, 2008, 2010)." — B_hoover2014bem
- "Since then, the Size Effect Law (SEL) has become a widely recognized framework for modeling quasi-brittle fracture of concrete." — B_han2025

## 4. Pointing to controversy or competing models
- "Currently, three main theories for describing the size effect are promoted in the literature, namely statistical theories of random strength, stress-redistribution and energy release, and theory of crack fractality (Bažant, 2002)." — B_grassl2012
- "There is no full consensus on the range of applicability of these theories for concrete structures of different geometries and subjected to different loading, since the results of several of these theories are similar for the size range of experimental results available (Bažant and Yavaris, 2005)." — B_grassl2012
- "It is thus not surprising that rather different theoretical models have happily coexisted for a long time, and polemics about their differences have not resulted in a universal consensus." — B_hoover2014bem
- "This has been a challenge that has led to extensive polemics and, unfortunately, persistent controversies." — A_carloni2019
- "However, some authors [4,8,9] have reported that, in situations where the specimen boundaries limit the expansion of the fracture process zone (FPZ), the conventional SEL may not preserve high local accuracy." — A_friedrich2026
- "Furthermore, when the tests at different notch depths do not include the case of zero notch depth and very different sizes, the same data can be fitted by very different models, e.g., the size effect law, the Hu-Duan model [13–18] or Carpinteri’s ‘multifractal scaling law’ [7,23]." — A_hoover2013
- "But the data fit becomes unique when the zero notch depth is included [36,37]." — A_hoover2013

## 5. Identifying the gap
- "An especially important gap of knowledge, which has, for example, hampered a critical appraisal of the Hu-Duan boundary effect model [13–18], exists in the transition between the Type 1 and Type 2 size effects." — A_hoover2013
- "These two size effects are fundamentally different and transition between them has been one important gap in experimental information." — B_hoover2014usel
- "The problem is difficult because, in the transition, the crack or notch is not much larger than the fracture process zone (FPZ), which precludes linear approximations." — B_hoover2014usel
- "Development of such a formula has been attempted before (Bazant and Yu 2004, 2009; Bazant 1995, 1997) based on the technique of asymptotic matching, but experimental verification was incomplete." — B_hoover2014usel
- "Although PD has been increasingly applied to model fracture in quasi-brittle materials, few studies have specifically addressed the structural size effect using this approach." — A_friedrich2026
- "However, a limited number of studies were conducted to understand the fracture behavior of GFRP-RC beams [3,5,16,19,20]." — A_rahman2024
- "Most experimental studies are only able to demonstrate the effect on the strength for a small size range, since large scale experiments are too difficult to carry out." — B_grassl2012
- "Aggregated evaluations of the available data have been attempted, yet with little success since the fracture characteristics have been drowned in great uncertainties and scatter due to the effects of the aforementioned influencing parameters and test conditions, without which a clear interpretation of the available data is impossible." — A_hoover2013
- "A few other transformations resulting in linear and nonlinear regressions accounting or not for weights have been used and compared in the past [6, 7, 36, 43], but none of these studies rely on rigorous nonlinear regression statistics, rather on an inadequate adaptation of linear regression metrics." — B_pathirage2025
- "However, the interpretation of test data yielding the fracture 3 energy according to the size effect law is still pending." — A_pijaudier2022 (line number "3" is a manuscript artefact)

## 6. Stating the objective and contribution
- "The objective of this paper is to develop and experimentally verify a new formula for the combined effects of structure size and crack or notch depth, called the universal size-shape effect law (because the variation of crack depth represents an effect of structure shape, or geometry)." — B_hoover2014usel
- "One particular objective is to bridge the previously clarified size effects in specimens with no cracks or notches and in specimens with deep notches or cracks called the Type 1 and Type 2 size effects, respectively." — B_hoover2014usel
- "A key objective of this study is to determine the transition between types 1 and 2." — A_hoover2013
- "The objective of this work is to contribute to the understanding of fracture processes by investigating numerically the size effect on fracture process zones in concrete structures." — B_grassl2012
- "The contribution of the present study is to apply this strategy to the meso-scale modelling of the size effect on the fracture process zone, which should provide a better insight into fracture processes and, therewith, a better description of size effect." — B_grassl2012
- "This paper deals exclusively with statistics and shows the importance of using the correct statistical regression method for the identification of fracture parameters using the size-effect formula." — B_pathirage2025
- "The present work fills a glaring gap in the experimental basis of concrete fracture modeling—the lack of comprehensive experimental data, and especially the lack of information on the transition between the Type 1 and 2 size effects." — A_hoover2013 (strong wording; use only with matching evidence)

## 7. Describing the data basis (single batch, broad range)
- "All the specimens were made from the same batch of concrete, were of virtually the same age, and all went through the same curing regimen and the same environmental conditions during the test." — A_hoover2013
- "The current study is based on recently obtained comprehensive fracture test data for three-point bend beams cast from one batch of the same concrete and cured and tested under identical conditions." — B_hoover2014usel
- "In total, 18 different beam geometries (families of beams) were cast." — B_hoover2014usel
- "They were geometrically similar three-point bend beams of four different depths, D 5 500, 215, 93 and 40 mm, and five different relative crack lengths, a0 =D 5 0, 0:025, 0:075, 0:15 and 0:30 for each size, except that the notch a0 =D 5 0:025 was skipped for the two smallest sizes (because it would have been much shorter than the coarse aggregate diameter da and thus essentially equivalent to the case a 5 a=D 5 0)." — B_hoover2014bem ("5" = "=" glyph error in the ASCE PDF)
- "The model assumptions are clearly stated and verified based on a large database of sizeeffect data collected from the available literature for 16 different types of quasi-brittle materials comprising a total of 71 sets of size-effect tests, for a total of 905 individual fracture tests." — B_pathirage2025
- "These data are comprehensive enough to check the basic hypothesis of Hu and Duan’s model for the" — B_hoover2014bem (fragment; continues after a page footer)

## 8. Separating calibration from prediction (hold-out logic)
- "Only the responses of the beams with the deepest notch are used to identify the deterministic model parameters, while the rest of the test data is subsequently compared to the deterministic model predictions." — A_elias2015
- "In particular, the fracture parameters Gf and cf should not be influenced by the data for beams with no notches (Type 1 data) or shallow notches, and fr‘ , Db , lp , and r should not be influenced by the data for deep notches." — B_hoover2014usel
- "It would not have been meaningful to fit all the unknown parameters concurrently because every one of them would then be influenced by all the data." — B_hoover2014usel
- "The BEM and SEL fits are optimized in Figs. 2 and 3 with the restriction that all the material parameters of each model be the same for all tests." — B_hoover2014bem
- "This shows that the BEM cannot predict the strength of beams with notches if it is fitted to specimens with no notch." — B_hoover2014bem
- "An identification procedure of model parameters obtained using a subset of experimental data confirmed the robustness of the model by showing reasonable agreement between simulated and experimental responses for all the data." — A_elias2015
- "The Model M7 must be calibrated independently of the peak loads obtained in the size effect tests using only the free parameters of the model." — B_caner2018

## 9. Stating assumptions and scope
- "The present work is based on several assumptions." — B_grassl2012
- "This paper will solely focus on the size-effect produced due to crack formation and energy release." — B_pathirage2025
- "Even though there are several possible sources of random fluctuations, it is considered here that all of them can be approximately described by a single homogeneous random field." — A_elias2020
- "Only the nonstatistical USEL in Eq. (11) was considered because parameters m and ls for the Weibull statistical size effect cannot be identified from the present data." — B_hoover2014usel
- "It should be noted that the present study does not aim to reproduce statistical size effect on strength, for which most likely a larger auto-correlation length is required as reported in Vořechovskỳ (2007) and Grassl and Bažant (2009)." — B_grassl2022
- "It is worth noting that the fractal framework adopted here is not used as a constitutive assumption nor as a calibration tool." — A_friedrich2026

## 10. Reporting fit quality and error
- "The new universal law is shown to fit the comprehensive data quite well, with a coefficient of variation of only 2.3%." — B_hoover2014usel
- "The COV of fit of the entire surface (defined as the RMS error divided by the mean of all data) is only 2.30%." — B_hoover2014usel
- "The largest COV, equal to 3.8%, comes from the size effect plot for a 5 0:025, which is in the transition." — B_hoover2014usel
- "The coefficients of variation of the regressions (i.e., the root-mean-square of the deviations from the regression line divided by the data mean) were only 0.117, 0.135, and 0.151." — B_nguyen2020
- "Both fittings exhibited a CoV of 50.24 % and 45.69 %, respectively, despite the limited data range." — A_carloni2019
- "The results demonstrate 20 that the predicted elastic modulus and tensile strength agree well with the tested values, with errors 21 within 7%." — A_zhang2026 (line numbers are manuscript artefacts)
- "Error bars of the numerical results show the mean plus and minus one standard deviation of 100 analyses." — B_grassl2012
- "For the experiments, standard deviations are not presented, since only a small number of beams for each size and geometry was tested, rendering any estimate of standard deviation inaccurate (Grégoire et al., 2011)." — B_grassl2012
- "The difference with the correct point estimates is statistically significant with an alpha level of 0.05." — B_pathirage2025

## 11. Comparing with a baseline model
- "On the other hand, the Type 1 and 2 size effect laws (SELs) and their amalgamation in the universal size effect law are found to give a far better fit of the test results." — B_hoover2014bem
- "The optimum fit of the data by Hu and Duan’s model shows major deviations from these new test results." — B_hoover2014bem
- "As seen in Figs. 2 and 3, for deep notches (a 5 0:30 and 0:15), the size effect fits by BEM are worse than those by SEL, and for short or zero notches, they are much worse." — B_hoover2014bem
- "In all cases, the SEL fits are distinctly more accurate." — B_hoover2014bem
- "In fitting these data, the BEM is distinctly inferior to the SELs, both Types 1 and 2, and their transition described by the universal SEL." — B_hoover2014bem
- "In contrast, the predictions of SEL are always in excellent agreement, with a CoV in the order of 4 %." — A_carloni2019
- "This is expected because Eq. (4) has the same form as the Type 2 SEL." — B_hoover2014bem
- "The comprehensive fracture tests now make possible such a check, and show that the previous attempts to bridge the Type 1 and 2 size effects were not accurate enough." — B_hoover2014usel
- "According to these values the comparison is shown in Fig. 10: the agreement is more than satisfactory, FFM predictions somewhat overestimating the size effect for cracked configurations." — B_baldassari2023
- "A good agreement was observed between the numerical and experimental results for load versus crack mouth displacement (CMD)." — A_khan2023
- "This study confirmed again that the linear BEM is easy to use and provides fairly accurate predictions across concrete specimens and structures of various sizes." — B_han2025 (BEM-school voice)

## 12. Explaining mechanisms and asymptotics
- "The reason is that the energy release rate of an initiating crack vanishes, which forces the use of higher-order derivatives of gðaÞ." — B_hoover2014usel
- "However, differentiation of a functional approximation is known to always greatly increase the approximation error." — B_hoover2014usel
- "The reason is that the stress concentration is so severe that the crack is forced to propagate from one specific location (the notch tip) and the ability of the spatial material variability to change its location is largely suppressed." — A_elias2020
- "The minimum of the mean strength occurs when the autocorrelation length is close to the material’s characteristic length." — A_elias2020
- "The only purpose of the transition parameter l is to provide a smooth transition between the Type 1 and 2 behaviors." — B_hoover2014usel
- "The flaw size distribution is strictly a material property and thus cannot be a function of the structure size (nor shape)." — B_hoover2014bem
- "This depth is roughly the same as the size of the FPZ of deep cracks and is about seven times da ." — B_hoover2014usel
- "As will be shown in Section 5.1, in contrast to SEL, the deviation of BEM from cohesive fracture mechanics occurs well before the structure size D gets close to the aggregate size." — A_carloni2019

## 13. Anticipating objections (question–answer, Bažant school)
- "Using an elastic solution to determine factor c might seem debatable." — B_hoover2014usel
- "Wouldn’t a solution with the cohesive crack model or a damage model be more appropriate?" — B_hoover2014usel
- "Not in the present context, because the purpose of ɛ ,n is to introduce a correction of elasticity to approximate the solution with the cohesive crack or damage model, for which no correction for strain gradient is needed." — B_hoover2014usel
- "Nevertheless, let us check what is implied." — B_hoover2014bem

## 14. Translating results into engineering consequences
- "This is a serious issue because the BEM will grossly overestimate the mean strength of large-size structures, which would lead to an unsafe design." — A_carloni2019
- "While it is clear that estimation of fracture parameters from nonfracture tests can never replace fracture testing of notched specimens, an improved formula with a known standard deviation can nevertheless serve a useful purpose for preliminary design and for approximate analysis of structures with not too high fracture sensitivity." — B_bazant2002
- "It also means that Eq. (7) cannot be used to determine Gf , which means the only way to determine Gf is to perform size effect tests on a large size range of beams with deep relative notches." — B_hoover2014usel
- "In summary, the fracture parameters should only be obtained in the space (P vs. D)." — B_pathirage2025
- "The linear regression plot suggested by RILEM [38] should be avoided for the statistical inverse problem of the size-effect method." — B_pathirage2025
- "Arguments favoring one model or another have undermined confidence in fracture mechanics among practicing engineers and in the committees responsible for updating the design code." — B_hoover2014ijf
- "Such selective comparisons are insufficient to justify applicability in engineering practice." — B_bazant2022

## 15. Acknowledging limitations
- "However, this remains to be proven experimentally." — B_hoover2014usel
- "The transition function l is not completely local, and therefore its applicability to other geometries is less certain." — B_hoover2014usel
- "Extending these function to a very different material would surely necessitate recalibration." — B_hoover2014usel
- "Although it seems that these parameter values can be kept the same even for other specimen geometries, recalibration may be needed for good accuracy." — B_hoover2014usel
- "The modelling techniques used in the present study are based on many simplifications stated in the introduction of this work." — B_grassl2012
- "The stochastic parameters unfortunately could not be identified, and were merely generated." — A_elias2015
- "But it alone cannot capture the Weibull type statistical size effect in large unnotched specimens; for larger specimens or different type of loading (e.g. four point bending or direct tension) the deterministic model would inevitably fail to reproduce the experimental data [17]." — A_elias2015
- "This is a well-known theoretical limitation of the bond-based formulation, and therefore cannot be modified within PD-DYNA." — A_friedrich2026
- "Therefore, it is not expected to reproduce quantitatively the experimental results of the gap-test." — B_grassl2022

## 16. Future work
- "Therefore, additional experiments, which provide local information on fracture processes, should be carried out to verify the local results presented here." — B_grassl2012
- "Future work should address the computational demands of fully 3D simulations, explore alternative PD kernels, and broaden validation to other quasi-brittle materials and loading scenarios." — A_friedrich2026
- "The applicability of D and l to other geometries could also be verified computationally, using the cohesive or crack-band model." — B_hoover2014usel
- "In future work, the meso-scale results will be used to calibrate nonlocal macroscopic damage models reported in the literature, which describe boundaries differently." — B_grassl2009
- "Nevertheless, further research is needed to decide this question unambiguously." — B_bazant2002

## 17. Opening and structuring the conclusions
- "Random meso-scale analyses of three point bending tests were performed to investigate the influence of the size effect on fracture process zones, which were determined from an average of increments of energy just after peak load." — B_grassl2012
- "This study examined the size-dependent fracture behavior of quasi-brittle materials using a PD framework implemented in LSDYNA and interpreted via a fractal-based scaling law." — A_friedrich2026
- "In this paper, the effect of such model transformations was investigated." — B_pathirage2025
- "The following conclusions can be drawn." — B_pathirage2025
- "The study resulted in the following conclusions: The width of the fracture process zone does not depend on the size of notched specimen." — B_grassl2012
- "Consequently, the following conclusions may be drawn in this study: The specimens tested have failed in Mode I." — B_caner2018
- "The new USEL fits the measured nominal strength quite well, with an overall COV of only 2.3%." — B_hoover2014usel
- "Overall, the results demonstrate that PD-DYNA, combined with a fractal interpretation of size effects, is a reliable and versatile tool for modeling quasi-brittle fracture." — A_friedrich2026

## 18. Roadmap and pointers
- "This paper is organized as follows." — B_mishra2025
- "For this reason, the second section of this work provides a brief description of the embedded crack formulation and the third section presents the smeared crack formulation proposed here." — A_suarez2023
- "In Figs. 4 and 5, these plots are created and compared with the data from Hoover et al. (2013)." — B_hoover2014usel
- "The analysis is relegated to a follow-up paper." — A_hoover2013

## 19. Abstract openers and closers
- "The boundary effect model (BEM) for concrete fracture and the effects of specimens size and crack length has previously been criticized on theoretical grounds, but the experimental evidence found in the literature, when taken alone, has been too limited to judge the validity of BEM conclusively." — B_hoover2014bem
- "Presented is an experimental investigation of unprecedented comprehensiveness and low scatter, using specimens made from one batch of concrete." — A_hoover2013
- "The size effect on the fracture process zone in notched and unnotched three point bending tests of concrete beams is analysed by a meso-scale approach." — B_grassl2012
- "This paper investigates the regression statistics of the size-effect method to obtain fracture parameters of quasi-brittle materials." — B_pathirage2025
- "Thus, regardless of the previously expounded theoretical objections, the comparison with experimental evidence alone suffices to conclude that Hu and Duan’s model is not realistic." — B_hoover2014bem
