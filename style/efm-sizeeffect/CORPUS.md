# CORPUS.md — efm-sizeeffect (Engineering Fracture Mechanics; quasi-brittle fracture and size effect of concrete)

Built 2026-10-28. **Local use only: do not redistribute the PDFs or texts.**
Only legal channels were used, in this order: OpenAlex locations (best_oa / all locations) → Semantic Scholar openAccessPdf / arXiv id → repository landing pages (HAL, IRIS, DSpace, NVA, OSTI, EPrints) → reuse of PDFs already collected legally in `/home/luck/xzy/0970project/lit/pdfs/D2/` and `/home/luck/xzy/0970project/venue/depth_corpus/pdfs/` (copied). No Elsevier TDM key (`~/.config/elsevier.key` absent), so the TDM step was skipped. No shadow libraries. ScienceDirect PDF endpoints and several Pure portals (Edinburgh, TU/e, UWA) refuse automated access; those items are listed under "pending user supply".
Fetch log with every URL tried: `fetch_log.json`. Metadata (OpenAlex, 2026-10-28): `meta.json`. Scripts: `scripts/`.

Counts: **A layer 15** (12 used for distillation + **3 held out for the blind test**); **B layer 20**. Total 35 PDFs / texts. Distillation uses 32 papers (12 A + 20 B).
Hold-outs (excluded from STYLE.md, phrasebank.md and stats.json): `A_augusthus2021`, `A_zhu2020`, `A_miarka2020`.

## A layer — Engineering Fracture Mechanics (concrete/quasi-brittle size effect, fracture energy, notch effects, FPZ)
| key | first author | year | DOI | cited (OpenAlex) | route (legal) | licence / version |
|---|---|---|---|---|---|---|
| A_augusthus2021 **(HOLD-OUT)** | Augusthus-Nelson | 2021 | 10.1016/j.engfracmech.2021.107987 | 9 | Cambridge Apollo repository (via Salford USIR record) | CC BY / accepted manuscript |
| A_zhu2020 **(HOLD-OUT)** | Zhu | 2020 | 10.1016/j.engfracmech.2020.107101 | 27 | HAL hal-03490759 | HAL deposit / accepted manuscript |
| A_miarka2020 **(HOLD-OUT)** | Miarka | 2020 | 10.1016/j.engfracmech.2020.107209 | 11 | idUS (Univ. Sevilla) repository | CC BY-NC-ND / accepted manuscript |
| A_kosteski2020 | Kosteski | 2020 | 10.1016/j.engfracmech.2020.107041 | 39 | IRIS PoliTo | CC BY-NC-ND / submitted version |
| A_elias2020 | Eliáš | 2020 | 10.1016/j.engfracmech.2020.107160 | 3 | arXiv:2002.01804 (copied from 0970project D2) | arXiv / preprint |
| A_pijaudier2022 | Pijaudier-Cabot | 2022 | 10.1016/j.engfracmech.2022.108630 | 26 | HAL hal-04193943 (univ-pau) | HAL deposit / accepted manuscript |
| A_puccia2022 | Puccia | 2022 | 10.1016/j.engfracmech.2022.108956 | 9 | IRIS UniPa (copied from depth_corpus) | CC BY-NC-ND / accepted manuscript |
| A_khan2023 | Khan | 2023 | 10.1016/j.engfracmech.2023.109439 | 23 | NVA / OsloMet hdl 11250/3099547 | CC BY 4.0 / VoR |
| A_suarez2023 | Suárez | 2023 | 10.1016/j.engfracmech.2023.109356 | 6 | RUJA hdl 10953/4778 (copied from depth_corpus) | CC BY-NC-ND / accepted manuscript |
| A_rahman2024 | Rahman | 2024 | 10.1016/j.engfracmech.2024.109965 | 12 | re.public.polimi.it | CC BY / VoR |
| A_friedrich2026 | Ferreira Friedrich | 2026 | 10.1016/j.engfracmech.2026.112234 | 0 | IRIS PoliTo | CC BY / VoR |
| A_zhang2026 | Zhang J.X. | 2026 | 10.1016/j.engfracmech.2026.112445 | 0 | DI-fusion ULB repository | repository / accepted manuscript |
| A_hoover2013 (pre-2020) | Hoover | 2013 | 10.1016/j.engfracmech.2013.08.007 | 198 | Bažant homepage author copy 524.pdf (copied from D2) | author copy |
| A_carloni2019 (pre-2020) | Carloni | 2019 | 10.1016/j.engfracmech.2019.04.036 | 78 | Bažant homepage author copy 602.pdf (copied from D2) | author copy |
| A_elias2015 (pre-2020) | Eliáš | 2015 | 10.1016/j.engfracmech.2015.01.004 | 132 | Vořechovský homepage author copy (copied from D2) | author copy |

## B layer — high-cited / topical OA papers in M&S, CCR, IJSS, JEM-ASCE (+ IJF, JAM, TAFM, Materials)
| key | first author | year | venue | DOI | cited | route | licence / version |
|---|---|---|---|---|---|---|---|
| B_grassl2009 | Grassl | 2009 | IJSS | 10.1016/j.ijsolstr.2009.12.010 | 258 | arXiv:0901.4636 | arXiv preprint |
| B_grassl2012 | Grassl | 2012 | IJSS | 10.1016/j.ijsolstr.2012.03.023 | 213 | arXiv:1107.2311 (copied from D2) | arXiv preprint |
| B_leguillon2017 | Leguillon | 2017 | IJSS | 10.1016/j.ijsolstr.2017.05.036 | 43 | HAL hal-01529248 | HAL deposit |
| B_caner2018 | Caner | 2018 | IJSS | 10.1016/j.ijsolstr.2018.11.029 | 3 | UPCommons hdl 2117/126898 | accepted manuscript |
| B_alam2019 | Alam | 2019 | IJSS | 10.1016/j.ijsolstr.2019.08.003 | 44 | HAL hal-03488220 | HAL deposit |
| B_grassl2022 | Grassl | 2022 | IJSS | 10.1016/j.ijsolstr.2022.112086 | 15 | Glasgow Enlighten eprint 287302 | CC BY / VoR |
| B_karrer2022 | Karrer | 2022 | Mater. Struct. | 10.1617/s11527-022-02011-w | 2 | Springer OA PDF | CC BY / VoR |
| B_pathirage2025 | Pathirage | 2025 | Mater. Struct. | 10.1617/s11527-024-02565-x | 2 | HAL hal-05044779 | CC BY / accepted manuscript |
| B_gudzulic2025 | Gudžulić | 2025 | Mater. Struct. | 10.1617/s11527-025-02815-6 | 4 | Springer OA PDF (copied from depth_corpus) | CC BY / VoR |
| B_bazant2002 | Bažant | 2002 | CCR | 10.1016/S0008-8846(01)00723-2 | 508 | Bažant homepage author copy 413.pdf (copied from D2) | author copy |
| B_gangnant2016 | Gangnant | 2016 | CCR | 10.1016/j.cemconres.2016.07.010 | 62 | HAL hal-02367593 | HAL deposit |
| B_mishra2025 | Mishra | 2025 | CCR | 10.1016/j.cemconres.2025.108012 | 14 | DORA Empa | CC BY / VoR |
| B_hoover2014usel | Hoover | 2014 | JEM-ASCE | 10.1061/(ASCE)EM.1943-7889.0000627 | 150 | Bažant homepage author copy 533.pdf (copied from D2) | author copy |
| B_hoover2014bem | Hoover | 2014 | JEM-ASCE | 10.1061/(ASCE)EM.1943-7889.0000632 | 61 | Bažant homepage author copy 534.pdf (copied from D2) | author copy |
| B_das2019 | Das | 2019 | JEM-ASCE | 10.1061/(ASCE)EM.1943-7889.0001628 | 19 | OSTI purl 1572459 | CC BY-NC-ND / accepted manuscript |
| B_hoover2014ijf | Hoover | 2014 | Int. J. Fract. | 10.1007/s10704-013-9926-0 | 147 | Bažant homepage author copy 538.pdf (copied from D2) | author copy |
| B_nguyen2020 | Nguyen | 2020 | J. Appl. Mech. | 10.1115/1.4047215 | 84 | Bažant homepage author copy 613.pdf (copied from D2) | author copy |
| B_bazant2022 | Bažant | 2022 | J. Appl. Mech. | 10.1115/1.4054221 | 80 | Bažant homepage author copy 623.pdf (copied from D2) | author copy |
| B_baldassari2023 | Baldassari | 2023 | TAFM | 10.1016/j.tafmec.2023.103787 | 26 | IRIS PoliTo (copied from D2) | CC BY / VoR |
| B_han2025 | Han (Hu group, BEM) | 2025 | Materials | 10.3390/ma18081877 | 5 | MDPI gold OA, PMC12028945 (copied from D2) | CC BY 4.0 / VoR |

## Pending user supply (relevant, but no legal automated copy was obtained)
OA (CC BY) but blocked for automated download. These can be fetched manually in a browser and dropped into `pdfs/`:
- Hu X. et al. 2024, *Prediction of crack initiation for notched concrete beam from FPZ at maximum load*, EFM, 10.1016/j.engfracmech.2024.110074 (CC BY; Hu–Duan BEM voice, high priority)
- Suchorzewski & Nitka 2022, EFM, 10.1016/j.engfracmech.2022.108357 (CC BY)
- Liu W. et al. 2026, *Progressive failure and structural size effect in FRC*, EFM, 10.1016/j.engfracmech.2026.111962 (CC BY)
- Nitka et al. 2024, EFM, 10.1016/j.engfracmech.2024.110153 (CC BY)
- Pirmoradi et al. 2025, EFM, 10.1016/j.engfracmech.2025.111166 (CC BY; TU/e portal 403)
- Zhou R. et al. 2021, *Mesoscale modelling of size effect on the evolution of FPZ*, EFM, 10.1016/j.engfracmech.2021.107559 (Edinburgh Pure, 403)
- İnce 2025, SCB nonlinear fracture characteristics, EFM, 10.1016/j.engfracmech.2025.110951 (repository HTTP 500)
- Rong et al. 2019, Mater. Struct., 10.1617/s11527-019-1326-0 (GCU Pure)
- IJSS open-archive items (ScienceDirect only): Morel 2011 10.1016/j.ijsolstr.2011.01.014; Morel 2006 10.1016/j.ijsolstr.2006.11.014; Vořechovský 2006 10.1016/j.ijsolstr.2006.08.019; Sinaie 2016 10.1016/j.ijsolstr.2016.12.022; Qing 2022 10.1016/j.ijsolstr.2022.111654

Closed access (user-supplied copy needed if wanted): Hu X. et al. 2021 FPZ width/length 10.1016/j.engfracmech.2021.108158; Han X. et al. 2021 10.1016/j.engfracmech.2021.107589; Han X. et al. 2023 10.1016/j.engfracmech.2023.109259; Guan J. et al. 2022 10.1016/j.engfracmech.2022.108596; Zhao Y. et al. 2021 (BEM R-curve) 10.1016/j.engfracmech.2021.107562; Lemery et al. 2020 10.1016/j.engfracmech.2020.107022; Negi et al. 2021 10.1016/j.engfracmech.2020.107511; Zhang J. et al. 2021 (SFRC size effect) 10.1016/j.engfracmech.2021.108193; Bakour & Ben Ftima 2021 10.1016/j.engfracmech.2021.108144; dos Santos & Forti 2022 10.1016/j.engfracmech.2022.108249; Wendner et al. 2014 database 10.1617/s11527-014-0426-0.

## Files
`pdfs/` (35 PDFs, local only) · `text/` (pdftotext reading-order extraction) · `STYLE.md` · `phrasebank.md` · `style_check.py` · `stats.json` · `blindtest.md` (+ `blindtest_key.md`, answer key) · `scripts/` (search, fetch, assemble, diagnostics, quote verifier `s11_verify_quotes.py`, GS runner) · `scratch/` (dumps, GS working files).
