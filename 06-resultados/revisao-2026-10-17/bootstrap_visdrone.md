# Intervalos por reamostragem de imagens no VisDrone-DET val (17/10/2026, agente D2)

Protocolo do artigo (classe unica, imgsz 1280, conf 0,001); 1000 reamostras das 548 imagens com reposicao, semente 0, as mesmas para todos os modelos. Intervalo = percentis 2,5 e 97,5. Eficacia = mAP50 do modelo / mAP50 de R na mesma reamostra. Equivalencia do calculo com ap_per_class do Ultralytics conferida (maior diferenca absoluta 0.0e+00).

## mAP50 por modelo

| Modelo | Run | mAP50 reportado | mAP50 (esta rodada) | media boot | IC 95% | Eficacia | IC 95% da eficacia |
|---|---|---|---|---|---|---|---|
| R | `r_pareado` | 0.6311 | 0.6311 | 0.6315 | 0.6149 a 0.6471 | 100.0% | 100.0 a 100.0% |
| S-nadir-150 | `s_nadir_4k` | 0.0102 | 0.0102 | 0.0108 | 0.0087 a 0.0133 | 1.6% | 1.4 a 2.1% |
| S-nadir-150-six | `s_variedade` | 0.019 | 0.0190 | 0.0181 | 0.0142 a 0.0211 | 3.0% | 2.3 a 3.3% |
| S-oblique | `s_obliquo` | 0.0614 | 0.0614 | 0.0613 | 0.0554 a 0.0673 | 9.7% | 8.9 a 10.6% |
| S-oblique-six s0 | `s_oblvar` | 0.1055 | 0.1055 | 0.1061 | 0.0980 a 0.1148 | 16.7% | 15.7 a 18.1% |
| S-oblique-six s1 | `s_oblvar_sd1` | 0.0958 | 0.0958 | 0.0960 | 0.0884 a 0.1048 | 15.2% | 14.1 a 16.5% |
| S-oblique-six s2 | `s_oblvar_sd2` | 0.0887 | 0.0887 | 0.0888 | 0.0813 a 0.0968 | 14.1% | 13.1 a 15.2% |
| F-synthetic 5% s0 | `ft05_sint` | 0.4424 | 0.4424 | 0.4426 | 0.4260 a 0.4587 | 70.1% | 68.4 a 71.8% |
| F-synthetic 5% s1 | `ft05_sint_sd1` | 0.4608 | 0.4608 | 0.4608 | 0.4441 a 0.4784 | 73.0% | 71.4 a 74.6% |
| F-synthetic 5% s2 | `ft05_sint_sd2` | 0.4554 | 0.4554 | 0.4562 | 0.4400 a 0.4721 | 72.2% | 70.8 a 73.7% |
| F-synthetic 10% | `ft10_sint` | 0.5095 | 0.5095 | 0.5097 | 0.4935 a 0.5264 | 80.7% | 79.3 a 82.1% |
| F-generic 5% s0 | `ft05_coco` | 0.522 | 0.5220 | 0.5224 | 0.5045 a 0.5403 | 82.7% | 81.4 a 84.1% |
| F-generic 5% s1 | `ft05_coco_sd1` | 0.5228 | 0.5228 | 0.5234 | 0.5056 a 0.5410 | 82.8% | 81.5 a 84.2% |
| F-generic 5% s2 | `ft05_coco_sd2` | 0.5285 | 0.5285 | 0.5293 | 0.5114 a 0.5474 | 83.7% | 82.4 a 85.2% |
| F-generic 10% | `ft10_coco` | 0.5709 | 0.5709 | 0.5712 | 0.5535 a 0.5883 | 90.5% | 89.2 a 91.6% |
| F-joint 5% | `misto05` | 0.4607 | 0.4607 | 0.4617 | 0.4444 a 0.4789 | 73.0% | 71.6 a 74.6% |
| F-joint 10% | `misto10` | 0.5428 | 0.5428 | 0.5434 | 0.5259 a 0.5610 | 86.0% | 84.8 a 87.4% |

## Diferencas pareadas (a menos b, mesmas reamostras)

| Comparacao | a | b | dif. absoluta | IC 95% | reamostras com dif. > 0 | dif. relativa (% do menor) | razao a/b | IC 95% da razao |
|---|---|---|---|---|---|---|---|---|
| nadir vs oblique: S-oblique - S-nadir-150 | 0.0614 | 0.0102 | +0.0511 | +0.0447 a +0.0567 | 100.0% | +501.1% | 6.011 | 4.571 a 7.011 |
| six settlements vs one, oblique: S-oblique-six s0 - S-oblique | 0.1055 | 0.0614 | +0.0441 | +0.0383 a +0.0514 | 100.0% | +71.9% | 1.719 | 1.601 a 1.868 |
| six settlements vs one, oblique: S-oblique-six s1 - S-oblique | 0.0958 | 0.0614 | +0.0344 | +0.0288 a +0.0412 | 100.0% | +56.1% | 1.561 | 1.449 a 1.686 |
| six settlements vs one, oblique: S-oblique-six s2 - S-oblique | 0.0887 | 0.0614 | +0.0273 | +0.0221 a +0.0330 | 100.0% | +44.5% | 1.445 | 1.347 a 1.559 |
| six settlements vs one, oblique: S-oblique-six (media das sementes) - S-oblique | 0.0966 | 0.0614 | +0.0353 | +0.0305 a +0.0411 | 100.0% | +57.5% | 1.575 | 1.477 a 1.692 |
| six settlements vs one, nadir: S-nadir-150-six - S-nadir-150 | 0.0190 | 0.0102 | +0.0088 | +0.0038 a +0.0102 | 100.0% | +86.6% | 1.866 | 1.308 a 2.071 |
| generic vs synthetic start, 5%: F-generic 5% s0 - F-synthetic 5% s0 | 0.5220 | 0.4424 | +0.0796 | +0.0721 a +0.0873 | 100.0% | +18.0% | 1.18 | 1.161 a 1.2 |
| generic vs synthetic start, 5%: F-generic 5% s1 - F-synthetic 5% s1 | 0.5228 | 0.4608 | +0.0620 | +0.0548 a +0.0706 | 100.0% | +13.5% | 1.135 | 1.118 a 1.156 |
| generic vs synthetic start, 5%: F-generic 5% s2 - F-synthetic 5% s2 | 0.5285 | 0.4554 | +0.0731 | +0.0654 a +0.0810 | 100.0% | +16.0% | 1.16 | 1.142 a 1.178 |
| generic vs synthetic start, 5%: F-generic 5% (media das sementes) - F-synthetic 5% (media das sementes) | 0.5245 | 0.4529 | +0.0716 | +0.0658 a +0.0780 | 100.0% | +15.8% | 1.158 | 1.144 a 1.173 |
| generic vs synthetic start, 10%: F-generic 10% - F-synthetic 10% | 0.5709 | 0.5095 | +0.0614 | +0.0553 a +0.0679 | 100.0% | +12.1% | 1.121 | 1.108 a 1.134 |
| generic vs joint, 5%: F-generic 5% s0 - F-joint 5% | 0.5220 | 0.4607 | +0.0613 | +0.0537 a +0.0681 | 100.0% | +13.3% | 1.133 | 1.115 a 1.149 |
| generic vs joint, 5%: F-generic 5% s1 - F-joint 5% | 0.5228 | 0.4607 | +0.0621 | +0.0534 a +0.0697 | 100.0% | +13.5% | 1.135 | 1.115 a 1.154 |
| generic vs joint, 5%: F-generic 5% s2 - F-joint 5% | 0.5285 | 0.4607 | +0.0678 | +0.0596 a +0.0752 | 100.0% | +14.7% | 1.147 | 1.128 a 1.165 |
| generic vs joint, 5%: F-generic 5% (media das sementes) - F-joint 5% | 0.5245 | 0.4607 | +0.0637 | +0.0562 a +0.0700 | 100.0% | +13.8% | 1.138 | 1.121 a 1.154 |
| generic vs joint, 10%: F-generic 10% - F-joint 10% | 0.5709 | 0.5428 | +0.0281 | +0.0214 a +0.0346 | 100.0% | +5.2% | 1.052 | 1.039 a 1.064 |
| joint vs synthetic start, 5%: F-joint 5% - F-synthetic 5% s0 | 0.4607 | 0.4424 | +0.0183 | +0.0116 a +0.0273 | 100.0% | +4.1% | 1.041 | 1.026 a 1.062 |
| joint vs synthetic start, 5%: F-joint 5% - F-synthetic 5% s1 | 0.4607 | 0.4608 | -0.0001 | -0.0062 a +0.0078 | 60.1% | -0.0% | 1.0 | 0.987 a 1.017 |
| joint vs synthetic start, 5%: F-joint 5% - F-synthetic 5% s2 | 0.4607 | 0.4554 | +0.0053 | -0.0011 a +0.0120 | 94.7% | +1.2% | 1.012 | 0.998 a 1.026 |
| joint vs synthetic start, 5%: F-joint 5% (media das sementes) - F-synthetic 5% (media das sementes) | 0.4607 | 0.4529 | +0.0078 | +0.0025 a +0.0147 | 99.5% | +1.7% | 1.017 | 1.006 a 1.032 |
| joint vs synthetic start, 10%: F-joint 10% - F-synthetic 10% | 0.5428 | 0.5095 | +0.0333 | +0.0276 a +0.0399 | 100.0% | +6.5% | 1.065 | 1.054 a 1.079 |
