# Diferencas de manchete: resolviveis sob tres leituras (17/10/2026, agente D2)

Leituras: (a) faixas min-max das sementes de treino nao se cruzam; (b) intervalo de 95% por reamostragem da diferenca pareada exclui zero (VisDrone: reamostragem de imagens, pareada; armados: reamostragem de quadros, independente em cada lado); (c) diferenca relativa de pelo menos 30% do menor valor. Onde ha sementes dos dois lados, a diferenca e a das medias das sementes; a leitura (a) exige sementes dos dois lados, e com um lado de treino unico fica registrado onde o valor unico cai em relacao a faixa do outro.

| Comparacao | medida | a | b | dif. absoluta | dif. relativa (% do menor) | razao a/b (IC 95%) | sementes a | sementes b | (a) faixas | (b) IC 95% da dif. | (b) | (c) >= 30% | veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nadir vs oblique (S-oblique vs S-nadir-150) | mAP50 no VisDrone-DET val | 0.0614 | 0.0102 | +0.0511 | +501.1% | 6.011 (4.571 a 7.011) | treino unico | treino unico | treino unico dos dois lados: nao avaliavel | +0.0447 a +0.0567 | sim | sim | resolvivel nas 2 de 2 leituras |
| Six settlements vs one, nadir (S-nadir-150-six vs S-nadir-150) | mAP50 no VisDrone-DET val | 0.0190 | 0.0102 | +0.0088 | +86.6% | 1.866 (1.308 a 2.071) | treino unico | treino unico | treino unico dos dois lados: nao avaliavel | +0.0038 a +0.0102 | sim | sim | resolvivel nas 2 de 2 leituras |
| Six settlements vs one, oblique (S-oblique-six vs S-oblique) | mAP50 no VisDrone-DET val | 0.0966 | 0.0614 | +0.0353 | +57.5% | 1.575 (1.477 a 1.692) | 0.0887 a 0.1055 | treino unico | treino unico em b; o valor de b fica fora da faixa de a | +0.0305 a +0.0411 | sim | sim | resolvivel nas 2 de 2 leituras |
| Generic vs synthetic start, 5% | mAP50 no VisDrone-DET val | 0.5245 | 0.4529 | +0.0716 | +15.8% | 1.158 (1.144 a 1.173) | 0.522 a 0.528 | 0.442 a 0.461 | resolvivel: faixas nao se cruzam | +0.0658 a +0.0780 | sim | nao | resolvivel nas 2 de 3 leituras |
| Generic vs synthetic start, 10% | mAP50 no VisDrone-DET val | 0.5709 | 0.5095 | +0.0614 | +12.1% | 1.121 (1.108 a 1.134) | treino unico | treino unico | treino unico dos dois lados: nao avaliavel | +0.0553 a +0.0679 | sim | nao | resolvivel nas 1 de 2 leituras |
| Generic vs joint, 5% | mAP50 no VisDrone-DET val | 0.5245 | 0.4607 | +0.0637 | +13.8% | 1.138 (1.121 a 1.154) | 0.522 a 0.528 | treino unico | treino unico em b; o valor de b fica fora da faixa de a | +0.0562 a +0.0700 | sim | nao | resolvivel nas 1 de 2 leituras |
| Generic vs joint, 10% | mAP50 no VisDrone-DET val | 0.5709 | 0.5428 | +0.0281 | +5.2% | 1.052 (1.039 a 1.064) | treino unico | treino unico | treino unico dos dois lados: nao avaliavel | +0.0214 a +0.0346 | sim | nao | resolvivel nas 1 de 2 leituras |
| Joint vs synthetic start, 5% | mAP50 no VisDrone-DET val | 0.4607 | 0.4529 | +0.0078 | +1.7% | 1.017 (1.006 a 1.032) | treino unico | 0.442 a 0.461 | treino unico em a; o valor de a fica dentro da faixa de b | +0.0025 a +0.0147 | sim | nao | resolvivel nas 1 de 2 leituras |
| Joint vs synthetic start, 10% | mAP50 no VisDrone-DET val | 0.5428 | 0.5095 | +0.0333 | +6.5% | 1.065 (1.054 a 1.079) | treino unico | treino unico | treino unico dos dois lados: nao avaliavel | +0.0276 a +0.0399 | sim | nao | resolvivel nas 1 de 2 leituras |
| 35 m vs twin at 75 m, object called armed, validation split | objeto chamado de armada a conf 0,25 | 0.2479 | 0.1795 | +0.0684 | +38.1% | 1.381 | 0.231 a 0.273 | 0.1319 a 0.2418 | nao resolvivel: faixas se cruzam | +0.0021 a +0.1424 | sim | sim | resolvivel nas 2 de 3 leituras |
| 35 m vs twin at 75 m, object called armed, new frames, 80 each | objeto chamado de armada a conf 0,25 | 0.2215 | 0.1343 | +0.0872 | +64.9% | 1.649 | 0.202 a 0.253 | 0.0972 a 0.1806 | resolvivel: faixas nao se cruzam | +0.0445 a +0.1359 | sim | sim | resolvivel nas tres leituras |
| 35 m vs original 75 m, object called armed, validation split | objeto chamado de armada a conf 0,25 | 0.2727 | 0.2370 | +0.0357 | +15.1% | 1.151 | treino unico | treino unico | treino unico dos dois lados: nao avaliavel | -0.0587 a +0.1244 | nao | nao | nao resolvivel em nenhuma leitura |

Diferencas semente a semente (onde ha sementes):

- Nadir vs oblique (S-oblique vs S-nadir-150): S-oblique - S-nadir-150: +0.0511, IC 95% +0.0447 a +0.0567, exclui zero: sim
- Six settlements vs one, nadir (S-nadir-150-six vs S-nadir-150): S-nadir-150-six - S-nadir-150: +0.0088, IC 95% +0.0038 a +0.0102, exclui zero: sim
- Six settlements vs one, oblique (S-oblique-six vs S-oblique): S-oblique-six s0 - S-oblique: +0.0441, IC 95% +0.0383 a +0.0514, exclui zero: sim
- Six settlements vs one, oblique (S-oblique-six vs S-oblique): S-oblique-six s1 - S-oblique: +0.0344, IC 95% +0.0288 a +0.0412, exclui zero: sim
- Six settlements vs one, oblique (S-oblique-six vs S-oblique): S-oblique-six s2 - S-oblique: +0.0273, IC 95% +0.0221 a +0.0330, exclui zero: sim
- Generic vs synthetic start, 5%: F-generic 5% s0 - F-synthetic 5% s0: +0.0796, IC 95% +0.0721 a +0.0873, exclui zero: sim
- Generic vs synthetic start, 5%: F-generic 5% s1 - F-synthetic 5% s1: +0.0620, IC 95% +0.0548 a +0.0706, exclui zero: sim
- Generic vs synthetic start, 5%: F-generic 5% s2 - F-synthetic 5% s2: +0.0731, IC 95% +0.0654 a +0.0810, exclui zero: sim
- Generic vs synthetic start, 10%: F-generic 10% - F-synthetic 10%: +0.0614, IC 95% +0.0553 a +0.0679, exclui zero: sim
- Generic vs joint, 5%: F-generic 5% s0 - F-joint 5%: +0.0613, IC 95% +0.0537 a +0.0681, exclui zero: sim
- Generic vs joint, 5%: F-generic 5% s1 - F-joint 5%: +0.0621, IC 95% +0.0534 a +0.0697, exclui zero: sim
- Generic vs joint, 5%: F-generic 5% s2 - F-joint 5%: +0.0678, IC 95% +0.0596 a +0.0752, exclui zero: sim
- Generic vs joint, 10%: F-generic 10% - F-joint 10%: +0.0281, IC 95% +0.0214 a +0.0346, exclui zero: sim
- Joint vs synthetic start, 5%: F-joint 5% - F-synthetic 5% s0: +0.0183, IC 95% +0.0116 a +0.0273, exclui zero: sim
- Joint vs synthetic start, 5%: F-joint 5% - F-synthetic 5% s1: -0.0001, IC 95% -0.0062 a +0.0078, exclui zero: nao
- Joint vs synthetic start, 5%: F-joint 5% - F-synthetic 5% s2: +0.0053, IC 95% -0.0011 a +0.0120, exclui zero: nao
- Joint vs synthetic start, 10%: F-joint 10% - F-synthetic 10%: +0.0333, IC 95% +0.0276 a +0.0399, exclui zero: sim
- 35 m vs twin at 75 m, object called armed, validation split: S-nadir-35 s0 - Twin-75 s0: +0.1079, IC 95% +0.0151 a +0.2107, exclui zero: sim
- 35 m vs twin at 75 m, object called armed, validation split: S-nadir-35 s1 - Twin-75 s1: +0.0995, IC 95% +0.0044 a +0.2021, exclui zero: sim
- 35 m vs twin at 75 m, object called armed, validation split: S-nadir-35 s2 - Twin-75 s2: -0.0021, IC 95% -0.0951 a +0.0927, exclui zero: nao
- 35 m vs twin at 75 m, object called armed, validation split: S-nadir-35 s0 - S-nadir-75 (original): +0.0357, IC 95% -0.0587 a +0.1244, exclui zero: nao
- 35 m vs twin at 75 m, object called armed, new frames, 80 each: S-nadir-35 s0 - Twin-75 s0: +0.1284, IC 95% +0.0709 a +0.1936, exclui zero: sim
- 35 m vs twin at 75 m, object called armed, new frames, 80 each: S-nadir-35 s1 - Twin-75 s1: +0.1049, IC 95% +0.0463 a +0.1656, exclui zero: sim
- 35 m vs twin at 75 m, object called armed, new frames, 80 each: S-nadir-35 s2 - Twin-75 s2: +0.0283, IC 95% -0.0317 a +0.0859, exclui zero: nao
