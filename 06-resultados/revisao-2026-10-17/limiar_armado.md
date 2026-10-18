# Varredura de limiar dos modelos de tres classes (17/10/2026, agente D2)

Protocolo: imagem 4K inteira na escala nativa, casamento um para um por IoU >= 0,50 sem olhar a classe; cada pessoa recebe a classe da predicao com que casou. Precisao de armada = armadas chamadas de armada / todas as predicoes de classe armada. d' com correcao log-linear. Conjuntos: val = divisao de validacao do proprio corpus; novos = quadros nunca vistos (80 quadros da semente 43 para o 35 m e o gemeo; os 50 quadros do teste de arma inedita para o 75 m original).

## Reproducao a conf 0,25 contra os arquivos ja publicados

| Modelo | Conjunto | Arquivo | armada (rep. / obtido) | desarmada | objeto | maior dif. | ok (<= 0,002) |
|---|---|---|---|---|---|---|---|
| S-nadir-75 | val | `confusao_armado_75.json` | 0.5470 / 0.5470 | 0.1307 / 0.1307 | 0.2370 / 0.2370 | 0.0000 | sim |
| S-nadir-75 | novos | `holdout_armas_armado_75.json` | 0.4336 / 0.4336 | 0.0676 / 0.0676 | 0.1522 / 0.1522 | 0.0000 | sim |
| S-nadir-35 s0 | val | `confusao_armado_35.json` | 0.5693 / 0.5693 | 0.1681 / 0.1681 | 0.2727 / 0.2727 | 0.0000 | sim |
| S-nadir-35 s0 | novos | `extra_armado_35.json` | 0.5434 / 0.5434 | 0.1556 / 0.1556 | 0.2534 / 0.2534 | 0.0000 | sim |
| S-nadir-35 s1 | val | `confusao_armado_35_sd1.json` | 0.5474 / 0.5474 | 0.1008 / 0.1008 | 0.2314 / 0.2314 | 0.0000 | sim |
| S-nadir-35 s1 | novos | `extra_armado_35_sd1.json` | 0.4711 / 0.4711 | 0.1238 / 0.1238 | 0.2021 / 0.2021 | 0.0000 | sim |
| S-nadir-35 s2 | val | `confusao_armado_35_sd2.json` | 0.5109 / 0.5109 | 0.0924 / 0.0924 | 0.2397 / 0.2397 | 0.0000 | sim |
| S-nadir-35 s2 | novos | `extra_armado_35_sd2.json` | 0.4769 / 0.4769 | 0.1302 / 0.1302 | 0.2089 / 0.2089 | 0.0000 | sim |
| Twin-75 s0 | val | `confusao_armado_75g.json` | 0.4706 / 0.4706 | 0.1087 / 0.1087 | 0.1648 / 0.1648 | 0.0000 | sim |
| Twin-75 s0 | novos | `extra_armado_75g.json` | 0.4319 / 0.4319 | 0.1404 / 0.1404 | 0.1250 / 0.1250 | 0.0000 | sim |
| Twin-75 s1 | val | `confusao_armado_75g_sd1.json` | 0.3529 / 0.3529 | 0.0978 / 0.0978 | 0.1319 / 0.1319 | 0.0000 | sim |
| Twin-75 s1 | novos | `extra_armado_75g_sd1.json` | 0.3541 / 0.3541 | 0.1267 / 0.1267 | 0.0972 / 0.0972 | 0.0000 | sim |
| Twin-75 s2 | val | `confusao_armado_75g_sd2.json` | 0.5882 / 0.5882 | 0.1413 / 0.1413 | 0.2418 / 0.2418 | 0.0000 | sim |
| Twin-75 s2 | novos | `extra_armado_75g_sd2.json` | 0.5564 / 0.5564 | 0.1952 / 0.1952 | 0.1806 / 0.1806 | 0.0000 | sim |

## Tres pontos de operacao por modelo e conjunto

| Modelo | Conjunto | Quadros | Ponto | limiar | recall armada | objeto chamado armada | desarmada chamada armada | precisao armada | F1 armada | d' arm. vs obj. | d' arm. vs desarm. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S-nadir-75 | val | 27 | conf 0,25 (padrao) | 0.25 | 0.547 | 0.237 | 0.131 | 0.386 | 0.452 | 0.83 | 1.23 |
| S-nadir-75 | val | 27 | max F1 de armada | 0.40 | 0.564 | 0.200 | 0.118 | 0.516 | 0.539 | 0.99 | 1.33 |
| S-nadir-75 | val | 27 | objeto <= 0,10 | 0.70 | 0.333 | 0.096 | 0.033 | 0.661 | 0.443 | 0.86 | 1.38 |
| S-nadir-75 | novos | 50 | conf 0,25 (padrao) | 0.25 | 0.434 | 0.152 | 0.068 | 0.430 | 0.432 | 0.85 | 1.31 |
| S-nadir-75 | novos | 50 | max F1 de armada | 0.45 | 0.391 | 0.126 | 0.059 | 0.578 | 0.466 | 0.86 | 1.27 |
| S-nadir-75 | novos | 50 | objeto <= 0,10 | 0.55 | 0.340 | 0.100 | 0.027 | 0.669 | 0.451 | 0.86 | 1.48 |
| S-nadir-35 s0 | val | 35 | conf 0,25 (padrao) | 0.25 | 0.569 | 0.273 | 0.168 | 0.415 | 0.480 | 0.77 | 1.12 |
| S-nadir-35 s0 | val | 35 | max F1 de armada | 0.30 | 0.555 | 0.256 | 0.126 | 0.469 | 0.508 | 0.79 | 1.27 |
| S-nadir-35 s0 | val | 35 | objeto <= 0,10 | 0.60 | 0.285 | 0.099 | 0.017 | 0.722 | 0.408 | 0.70 | 1.47 |
| S-nadir-35 s0 | novos | 80 | conf 0,25 (padrao) | 0.25 | 0.543 | 0.253 | 0.156 | 0.408 | 0.466 | 0.77 | 1.12 |
| S-nadir-35 s0 | novos | 80 | max F1 de armada | 0.35 | 0.497 | 0.226 | 0.121 | 0.484 | 0.491 | 0.74 | 1.16 |
| S-nadir-35 s0 | novos | 80 | objeto <= 0,10 | 0.65 | 0.211 | 0.099 | 0.035 | 0.603 | 0.313 | 0.48 | 0.99 |
| S-nadir-35 s1 | val | 35 | conf 0,25 (padrao) | 0.25 | 0.547 | 0.231 | 0.101 | 0.455 | 0.497 | 0.84 | 1.38 |
| S-nadir-35 s1 | val | 35 | max F1 de armada | 0.35 | 0.504 | 0.223 | 0.067 | 0.507 | 0.505 | 0.76 | 1.48 |
| S-nadir-35 s1 | val | 35 | objeto <= 0,10 | 0.65 | 0.314 | 0.083 | 0.017 | 0.741 | 0.441 | 0.88 | 1.56 |
| S-nadir-35 s1 | novos | 80 | conf 0,25 (padrao) | 0.25 | 0.471 | 0.202 | 0.124 | 0.424 | 0.447 | 0.76 | 1.08 |
| S-nadir-35 s1 | novos | 80 | max F1 de armada | 0.40 | 0.451 | 0.178 | 0.102 | 0.534 | 0.489 | 0.80 | 1.14 |
| S-nadir-35 s1 | novos | 80 | objeto <= 0,10 | 0.65 | 0.275 | 0.096 | 0.044 | 0.651 | 0.386 | 0.70 | 1.09 |
| S-nadir-35 s2 | val | 35 | conf 0,25 (padrao) | 0.25 | 0.511 | 0.240 | 0.092 | 0.407 | 0.453 | 0.73 | 1.33 |
| S-nadir-35 s2 | val | 35 | max F1 de armada | 0.45 | 0.460 | 0.132 | 0.042 | 0.656 | 0.541 | 1.00 | 1.59 |
| S-nadir-35 s2 | val | 35 | objeto <= 0,10 | 0.55 | 0.358 | 0.099 | 0.017 | 0.721 | 0.478 | 0.91 | 1.68 |
| S-nadir-35 s2 | novos | 80 | conf 0,25 (padrao) | 0.25 | 0.477 | 0.209 | 0.130 | 0.439 | 0.457 | 0.75 | 1.06 |
| S-nadir-35 s2 | novos | 80 | max F1 de armada | 0.45 | 0.396 | 0.164 | 0.083 | 0.598 | 0.476 | 0.71 | 1.12 |
| S-nadir-35 s2 | novos | 80 | objeto <= 0,10 | 0.55 | 0.292 | 0.099 | 0.057 | 0.656 | 0.404 | 0.73 | 1.02 |
| Twin-75 s0 | val | 24 | conf 0,25 (padrao) | 0.25 | 0.471 | 0.165 | 0.109 | 0.440 | 0.455 | 0.89 | 1.14 |
| Twin-75 s0 | val | 24 | max F1 de armada | 0.40 | 0.423 | 0.154 | 0.054 | 0.522 | 0.468 | 0.81 | 1.37 |
| Twin-75 s0 | val | 24 | objeto <= 0,10 | 0.55 | 0.341 | 0.099 | 0.043 | 0.630 | 0.443 | 0.86 | 1.26 |
| Twin-75 s0 | novos | 80 | conf 0,25 (padrao) | 0.25 | 0.432 | 0.125 | 0.140 | 0.370 | 0.399 | 0.97 | 0.90 |
| Twin-75 s0 | novos | 80 | max F1 de armada | 0.40 | 0.381 | 0.090 | 0.120 | 0.480 | 0.425 | 1.03 | 0.87 |
| Twin-75 s0 | novos | 80 | objeto <= 0,10 | 0.40 | 0.381 | 0.090 | 0.120 | 0.480 | 0.425 | 1.03 | 0.87 |
| Twin-75 s1 | val | 24 | conf 0,25 (padrao) | 0.25 | 0.353 | 0.132 | 0.098 | 0.417 | 0.382 | 0.73 | 0.90 |
| Twin-75 s1 | val | 24 | max F1 de armada | 0.40 | 0.341 | 0.110 | 0.076 | 0.580 | 0.430 | 0.80 | 1.00 |
| Twin-75 s1 | val | 24 | objeto <= 0,10 | 0.45 | 0.282 | 0.099 | 0.043 | 0.600 | 0.384 | 0.69 | 1.09 |
| Twin-75 s1 | novos | 80 | conf 0,25 (padrao) | 0.25 | 0.354 | 0.097 | 0.127 | 0.396 | 0.374 | 0.92 | 0.76 |
| Twin-75 s1 | novos | 80 | max F1 de armada | 0.40 | 0.284 | 0.062 | 0.089 | 0.549 | 0.374 | 0.95 | 0.77 |
| Twin-75 s1 | novos | 80 | objeto <= 0,10 | 0.25 | 0.354 | 0.097 | 0.127 | 0.396 | 0.374 | 0.92 | 0.76 |
| Twin-75 s2 | val | 24 | conf 0,25 (padrao) | 0.25 | 0.588 | 0.242 | 0.141 | 0.391 | 0.469 | 0.91 | 1.28 |
| Twin-75 s2 | val | 24 | max F1 de armada | 0.40 | 0.541 | 0.209 | 0.076 | 0.511 | 0.526 | 0.90 | 1.50 |
| Twin-75 s2 | val | 24 | objeto <= 0,10 | 0.65 | 0.271 | 0.099 | 0.022 | 0.622 | 0.377 | 0.66 | 1.33 |
| Twin-75 s2 | novos | 80 | conf 0,25 (padrao) | 0.25 | 0.556 | 0.181 | 0.195 | 0.390 | 0.458 | 1.05 | 1.00 |
| Twin-75 s2 | novos | 80 | max F1 de armada | 0.50 | 0.479 | 0.118 | 0.127 | 0.583 | 0.526 | 1.12 | 1.08 |
| Twin-75 s2 | novos | 80 | objeto <= 0,10 | 0.55 | 0.420 | 0.097 | 0.106 | 0.614 | 0.499 | 1.09 | 1.04 |

## Intervalos por reamostragem de quadros a conf 0,25 (1.000 reamostras, semente 0)

| Modelo | Conjunto | Quadros | objeto chamado armada | IC 95% | desarmada chamada armada | IC 95% | recall armada | IC 95% | d' arm. vs obj. | IC 95% |
|---|---|---|---|---|---|---|---|---|---|---|
| S-nadir-75 | val | 27 | 0.237 | 0.183 a 0.289 | 0.131 | 0.073 a 0.188 | 0.547 | 0.476 a 0.627 | 0.83 | 0.54 a 1.13 |
| S-nadir-75 | novos | 50 | 0.152 | 0.113 a 0.196 | 0.068 | 0.035 a 0.102 | 0.434 | 0.381 a 0.496 | 0.85 | 0.64 a 1.09 |
| S-nadir-35 s0 | val | 35 | 0.273 | 0.202 a 0.353 | 0.168 | 0.101 a 0.235 | 0.569 | 0.492 a 0.646 | 0.77 | 0.46 a 1.10 |
| S-nadir-35 s0 | novos | 80 | 0.253 | 0.204 a 0.303 | 0.156 | 0.117 a 0.194 | 0.543 | 0.491 a 0.594 | 0.77 | 0.57 a 0.99 |
| S-nadir-35 s1 | val | 35 | 0.231 | 0.161 a 0.311 | 0.101 | 0.043 a 0.161 | 0.547 | 0.480 a 0.619 | 0.84 | 0.56 a 1.14 |
| S-nadir-35 s1 | novos | 80 | 0.202 | 0.157 a 0.250 | 0.124 | 0.083 a 0.166 | 0.471 | 0.417 a 0.524 | 0.76 | 0.53 a 1.00 |
| S-nadir-35 s2 | val | 35 | 0.240 | 0.173 a 0.308 | 0.092 | 0.049 a 0.140 | 0.511 | 0.424 a 0.600 | 0.73 | 0.44 a 1.06 |
| S-nadir-35 s2 | novos | 80 | 0.209 | 0.159 a 0.255 | 0.130 | 0.090 a 0.174 | 0.477 | 0.422 a 0.527 | 0.75 | 0.55 a 0.98 |
| Twin-75 s0 | val | 24 | 0.165 | 0.100 a 0.230 | 0.109 | 0.044 a 0.174 | 0.471 | 0.397 a 0.558 | 0.89 | 0.58 a 1.32 |
| Twin-75 s0 | novos | 80 | 0.125 | 0.089 a 0.157 | 0.140 | 0.105 a 0.179 | 0.432 | 0.378 a 0.492 | 0.97 | 0.77 a 1.20 |
| Twin-75 s1 | val | 24 | 0.132 | 0.062 a 0.198 | 0.098 | 0.048 a 0.147 | 0.353 | 0.269 a 0.446 | 0.73 | 0.30 a 1.24 |
| Twin-75 s1 | novos | 80 | 0.097 | 0.065 a 0.129 | 0.127 | 0.093 a 0.163 | 0.354 | 0.301 a 0.405 | 0.92 | 0.70 a 1.15 |
| Twin-75 s2 | val | 24 | 0.242 | 0.170 a 0.304 | 0.141 | 0.071 a 0.209 | 0.588 | 0.500 a 0.680 | 0.91 | 0.65 a 1.20 |
| Twin-75 s2 | novos | 80 | 0.181 | 0.138 a 0.225 | 0.195 | 0.143 a 0.246 | 0.556 | 0.494 a 0.617 | 1.05 | 0.83 a 1.28 |

## Diferencas 35 m menos 75 m a conf 0,25 (reamostragem independente de quadros em cada lado)

| Comparacao | Conjunto | Medida | a | b | dif. | IC 95% | exclui zero | reamostras com dif. > 0 | dif. relativa (% do menor) |
|---|---|---|---|---|---|---|---|---|---|
| S-nadir-35 s0 - Twin-75 s0 | val | objeto_chamado_armada | 0.273 | 0.165 | +0.108 | +0.015 a +0.211 | sim | 98.9% | +65.5% |
| S-nadir-35 s0 - Twin-75 s0 | val | desarmada_chamada_armada | 0.168 | 0.109 | +0.059 | -0.038 a +0.154 | nao | 88.0% | +54.6% |
| S-nadir-35 s0 - Twin-75 s0 | val | recall_armada | 0.569 | 0.471 | +0.099 | -0.022 a +0.217 | nao | 94.8% | +21.0% |
| S-nadir-35 s1 - Twin-75 s1 | val | objeto_chamado_armada | 0.231 | 0.132 | +0.100 | +0.004 a +0.202 | sim | 97.9% | +75.4% |
| S-nadir-35 s1 - Twin-75 s1 | val | desarmada_chamada_armada | 0.101 | 0.098 | +0.003 | -0.073 a +0.081 | nao | 51.8% | +3.1% |
| S-nadir-35 s1 - Twin-75 s1 | val | recall_armada | 0.547 | 0.353 | +0.195 | +0.083 a +0.302 | sim | 99.8% | +55.1% |
| S-nadir-35 s2 - Twin-75 s2 | val | objeto_chamado_armada | 0.240 | 0.242 | -0.002 | -0.095 a +0.093 | nao | 49.3% | -0.9% |
| S-nadir-35 s2 - Twin-75 s2 | val | desarmada_chamada_armada | 0.092 | 0.141 | -0.049 | -0.130 a +0.038 | nao | 14.6% | -52.9% |
| S-nadir-35 s2 - Twin-75 s2 | val | recall_armada | 0.511 | 0.588 | -0.077 | -0.198 a +0.048 | nao | 12.8% | -15.1% |
| S-nadir-35 (media das sementes) - Twin-75 (media das sementes) | val | objeto_chamado_armada | 0.248 | 0.179 | +0.068 | +0.002 a +0.142 | sim | 97.9% | +38.1% |
| S-nadir-35 (media das sementes) - Twin-75 (media das sementes) | val | desarmada_chamada_armada | 0.120 | 0.116 | +0.004 | -0.053 a +0.062 | nao | 58.5% | +3.9% |
| S-nadir-35 (media das sementes) - Twin-75 (media das sementes) | val | recall_armada | 0.542 | 0.471 | +0.072 | -0.023 a +0.163 | nao | 92.8% | +15.3% |
| S-nadir-35 s0 - Twin-75 s0 | novos | objeto_chamado_armada | 0.253 | 0.125 | +0.128 | +0.071 a +0.194 | sim | 100.0% | +102.7% |
| S-nadir-35 s0 - Twin-75 s0 | novos | desarmada_chamada_armada | 0.156 | 0.140 | +0.015 | -0.040 a +0.073 | nao | 67.5% | +10.8% |
| S-nadir-35 s0 - Twin-75 s0 | novos | recall_armada | 0.543 | 0.432 | +0.112 | +0.031 a +0.192 | sim | 99.7% | +25.8% |
| S-nadir-35 s1 - Twin-75 s1 | novos | objeto_chamado_armada | 0.202 | 0.097 | +0.105 | +0.046 a +0.166 | sim | 100.0% | +107.9% |
| S-nadir-35 s1 - Twin-75 s1 | novos | desarmada_chamada_armada | 0.124 | 0.127 | -0.003 | -0.060 a +0.055 | nao | 45.1% | -2.3% |
| S-nadir-35 s1 - Twin-75 s1 | novos | recall_armada | 0.471 | 0.354 | +0.117 | +0.036 a +0.197 | sim | 99.8% | +33.0% |
| S-nadir-35 s2 - Twin-75 s2 | novos | objeto_chamado_armada | 0.209 | 0.181 | +0.028 | -0.032 a +0.086 | nao | 82.4% | +15.7% |
| S-nadir-35 s2 - Twin-75 s2 | novos | desarmada_chamada_armada | 0.130 | 0.195 | -0.065 | -0.129 a +0.005 | nao | 3.7% | -49.9% |
| S-nadir-35 s2 - Twin-75 s2 | novos | recall_armada | 0.477 | 0.556 | -0.080 | -0.163 a -0.007 | sim | 1.5% | -16.7% |
| S-nadir-35 (media das sementes) - Twin-75 (media das sementes) | novos | objeto_chamado_armada | 0.222 | 0.134 | +0.087 | +0.044 a +0.136 | sim | 100.0% | +64.9% |
| S-nadir-35 (media das sementes) - Twin-75 (media das sementes) | novos | desarmada_chamada_armada | 0.137 | 0.154 | -0.018 | -0.063 a +0.031 | nao | 23.0% | -12.9% |
| S-nadir-35 (media das sementes) - Twin-75 (media das sementes) | novos | recall_armada | 0.497 | 0.448 | +0.050 | -0.017 a +0.111 | nao | 93.1% | +11.1% |
| S-nadir-35 s0 - S-nadir-75 (original) | val | objeto_chamado_armada | 0.273 | 0.237 | +0.036 | -0.059 a +0.124 | nao | 74.7% | +15.1% |
| S-nadir-35 s0 - S-nadir-75 (original) | val | desarmada_chamada_armada | 0.168 | 0.131 | +0.037 | -0.055 a +0.126 | nao | 79.0% | +28.6% |
| S-nadir-35 s0 - S-nadir-75 (original) | val | recall_armada | 0.569 | 0.547 | +0.022 | -0.090 a +0.124 | nao | 64.7% | +4.1% |
