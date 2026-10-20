# Base real nadir (heridal): reamostragem de imagens (19/10/2026)

1000 reamostras das 1647 imagens, semente 0, pareadas. R = 0.3185 (interpretavel).

| Grupo | runs | mAP50 (media) | IC 95% | eficacia |
|---|---|---|---|---|
| R | r_pareado | 0.3185 | 0.2843 a 0.3543 | 100.0% |
| S-nadir-150 | s_nadir_4k, s_nadir_4k_sd1, s_nadir_4k_sd2 | 0.1997 | 0.1713 a 0.2306 | 62.7% |
| S-nadir-150-six | s_variedade | 0.2488 | 0.2116 a 0.2865 | 78.1% |
| S-oblique | s_obliquo, s_obliquo_sd1, s_obliquo_sd2 | 0.1341 | 0.1149 a 0.1555 | 42.1% |
| S-oblique-six | s_oblvar, s_oblvar_sd1, s_oblvar_sd2 | 0.1477 | 0.1265 a 0.1715 | 46.4% |
| Armado-150 (exploratorio) | armado_150g | 0.1417 | 0.1145 a 0.1711 | 44.5% |

| Comparacao | a | b | dif. | IC 95% | (a) | (b) | (c) | razao a/b (IC 95%) |
|---|---|---|---|---|---|---|---|---|
| principal: oblique vs nadir | 0.1341 | 0.1997 | -0.0656 | -0.0840 a -0.0471 | nao resolvivel: faixas se cruzam | sim | sim | 0.671 ([0.61, 0.744]) |
| secundaria: six settlements, oblique vs nadir | 0.1477 | 0.2488 | -0.1012 | -0.1216 a -0.0786 | treino unico em b; o valor de b fica fora da faixa de a | sim | sim | 0.593 ([0.55, 0.65]) |

Razao oblique/nadir no VisDrone: 6.011 ([4.571, 7.011]), de bootstrap_visdrone.json.
