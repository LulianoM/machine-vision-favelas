# Base real nadir (heridal_1280): reamostragem de imagens (19/10/2026)

1000 reamostras das 1647 imagens, semente 0, pareadas. R = 0.3353 (interpretavel).

| Grupo | runs | mAP50 (media) | IC 95% | eficacia |
|---|---|---|---|---|
| R | r_pareado | 0.3353 | 0.3027 a 0.3700 | 100.0% |
| S-nadir-150 | s_nadir_4k, s_nadir_4k_sd1, s_nadir_4k_sd2 | 0.1682 | 0.1431 a 0.1947 | 50.2% |
| S-nadir-150-six | s_variedade | 0.2208 | 0.1842 a 0.2584 | 65.8% |
| S-oblique | s_obliquo, s_obliquo_sd1, s_obliquo_sd2 | 0.1422 | 0.1214 a 0.1651 | 42.4% |
| S-oblique-six | s_oblvar, s_oblvar_sd1, s_oblvar_sd2 | 0.1418 | 0.1218 a 0.1655 | 42.3% |
| Armado-150 (exploratorio) | armado_150g | 0.1272 | 0.1029 a 0.1566 | 37.9% |

| Comparacao | a | b | dif. | IC 95% | (a) | (b) | (c) | razao a/b (IC 95%) |
|---|---|---|---|---|---|---|---|---|
| principal: oblique vs nadir | 0.1422 | 0.1682 | -0.0260 | -0.0414 a -0.0097 | nao resolvivel: faixas se cruzam | sim | nao | 0.845 ([0.77, 0.936]) |
| secundaria: six settlements, oblique vs nadir | 0.1418 | 0.2208 | -0.0789 | -0.1020 a -0.0568 | treino unico em b; o valor de b fica fora da faixa de a | sim | sim | 0.642 ([0.591, 0.709]) |

Razao oblique/nadir no VisDrone: 6.011 ([4.571, 7.011]), de bootstrap_visdrone.json.
