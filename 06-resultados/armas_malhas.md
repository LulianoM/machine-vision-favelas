# Caixa envolvente das malhas de arma e pegada em pixels

Gerado por `mede_armas.py` (dentro do Blender headless; ver docstring). Metros no referencial local da arma: comprimento no eixo do cano, largura de lado a lado, altura do carregador ao topo. Pixels = metros dividido pelo GSD (4,88, 2,44 e 1,14 cm/px a 150, 75 e 35 m em 4K). A caixa e deterministica: 12 sementes por malha deram a mesma caixa (o sorteio so escolhe material). "Registrado" e o comprimento nominal que a funcao devolve e que o manuscrito cita; a malha pode ser mais comprida (coronha e carregador fora do nominal). Os objetos confundiveis sorteiam o comprimento: para eles a tabela traz a mediana das sementes e, entre colchetes, a faixa.

## Armas de treino (as cinco)

| Malha | Peso | Registrado (m) | Comprimento (m) | Largura (m) | Altura (m) | 150 m: C x L (px) | 75 m: C x L (px) | 35 m: C x L (px) | Altura a 150 / 75 / 35 (px) |
|---|---|---|---|---|---|---|---|---|---|
| fuzil_ak | 26 | 0.92 | 1.071 | 0.050 | 0.227 | 22.0 x 1.0 | 43.9 x 2.0 | 94.0 x 4.4 | 4.6 / 9.3 / 19.9 |
| fuzil_ar | 24 | 0.94 | 1.070 | 0.050 | 0.263 | 21.9 x 1.0 | 43.9 x 2.0 | 93.9 x 4.4 | 5.4 / 10.8 / 23.0 |
| carabina | 20 | 0.62 | 0.610 | 0.045 | 0.215 | 12.5 x 0.9 | 25.0 x 1.8 | 53.5 x 3.9 | 4.4 / 8.8 / 18.9 |
| espingarda | 18 | 1.05 | 1.172 | 0.042 | 0.099 | 24.0 x 0.9 | 48.0 x 1.7 | 102.8 x 3.7 | 2.0 / 4.0 / 8.6 |
| pistola | 12 | 0.20 | 0.195 | 0.030 | 0.116 | 4.0 x 0.6 | 8.0 x 1.2 | 17.1 x 2.6 | 2.4 / 4.7 / 10.1 |

## Armas ineditas (so teste)

| Malha | Peso | Registrado (m) | Comprimento (m) | Largura (m) | Altura (m) | 150 m: C x L (px) | 75 m: C x L (px) | 35 m: C x L (px) | Altura a 150 / 75 / 35 (px) |
|---|---|---|---|---|---|---|---|---|---|
| fuzil_fal | 50 | 1.10 | 1.101 | 0.055 | 0.253 | 22.6 x 1.1 | 45.1 x 2.3 | 96.6 x 4.8 | 5.2 / 10.4 / 22.2 |
| submetralhadora | 50 | 0.55 | 0.560 | 0.050 | 0.247 | 11.5 x 1.0 | 23.0 x 2.0 | 49.1 x 4.4 | 5.1 / 10.1 / 21.7 |

## Objetos confundiveis (contraste)

| Malha | Peso | Registrado (m) | Comprimento (m) | Largura (m) | Altura (m) | 150 m: C x L (px) | 75 m: C x L (px) | 35 m: C x L (px) | Altura a 150 / 75 / 35 (px) |
|---|---|---|---|---|---|---|---|---|---|
| vassoura | 20 | 1.28 | 1.285 | 0.260 | 0.116 | 26.3 x 5.3 | 52.7 x 10.7 | 112.7 x 22.8 | 2.4 / 4.8 / 10.2 |
| rodo | 12 | 1.22 | 1.228 | 0.340 | 0.059 | 25.2 x 7.0 | 50.3 x 13.9 | 107.7 x 29.8 | 1.2 / 2.4 / 5.1 |
| cano_pvc | 14 | 2.01 | 2.009 [1.68 a 2.36] | 0.047 | 0.047 | 41.2 x 1.0 | 82.3 x 1.9 | 176.2 x 4.2 | 1.0 / 1.9 / 4.2 |
| vergalhao | 16 | 1.51 | 1.509 [1.18 a 1.86] | 0.016 | 0.016 | 30.9 x 0.3 | 61.8 x 0.6 | 132.3 x 1.4 | 0.3 / 0.6 / 1.4 |
| tabua | 12 | 1.46 | 1.459 [1.10 a 1.84] | 0.165 | 0.024 | 29.9 x 3.4 | 59.8 x 6.8 | 128.0 x 14.5 | 0.5 / 1.0 / 2.1 |
| guarda_chuva | 12 | 0.88 | 0.880 | 0.052 | 0.052 | 18.0 x 1.1 | 36.1 x 2.1 | 77.2 x 4.6 | 1.1 / 2.1 / 4.6 |
| enxada | 8 | 1.24 | 1.295 | 0.170 | 0.120 | 26.5 x 3.5 | 53.1 x 7.0 | 113.6 x 14.9 | 2.5 / 4.9 / 10.5 |
| tapete | 8 | 1.46 | 1.456 [1.23 a 1.70] | 0.209 | 0.209 | 29.8 x 4.3 | 59.7 x 8.6 | 127.7 x 18.4 | 4.3 / 8.6 / 18.4 |
| mangueira | 6 | 1.00 | 1.085 [0.89 a 1.29] | 0.024 | 0.024 | 22.2 x 0.5 | 44.5 x 1.0 | 95.2 x 2.1 | 0.5 / 1.0 / 2.1 |

## Resumo das cinco armas de treino

| GSD | Comprimento (px), min a max | Largura (px), min a max | Comprimento medio ponderado pelo sorteio (px) | Largura media ponderada (px) |
|---|---|---|---|---|
| 150 m, 4.88 cm/px | 4.0 a 24.0 | 0.6 a 1.0 | 18.3 | 0.91 |
| 75 m, 2.44 cm/px | 8.0 a 48.0 | 1.2 a 2.0 | 36.5 | 1.81 |
| 35 m, 1.14 cm/px | 17.1 a 102.8 | 2.6 a 4.4 | 78.2 | 3.96 |
