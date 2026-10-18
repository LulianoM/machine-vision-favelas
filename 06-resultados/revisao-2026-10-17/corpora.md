# Corpora do artigo: contagens lidas do disco (revisão de 2026-10-17, agente D1)

Gerado por `contagens.py` com o comando `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/revisao-2026-10-17/contagens.py`. Cada número vem dos rótulos YOLO, dos manifests do gerador e das pastas de ladrilhos em `C:\arma3-favela\blender\` e `C:\arma3-favela\visdrone\`. Nenhum corpus derivado do ortomosaico da PCERJ foi lido. Detalhe por corpus em `corpora.json`.

Câmera de todos os corpora sintéticos: sensor de 36 mm (ajuste horizontal) e lente de 28,82 mm (`Z30_LENS = 4.3 * 36 / 5.37` em `gen_morro.py`). A GSD da tabela é (altitude média × 36 / 28,82) / largura em px; para os corpora oblíquos é a GSD nominal de nadir na altitude média da câmera, não a GSD real no solo, que varia ao longo do quadro.

## 1. Corpora sintéticos

| Nome interno | Nome no artigo | Render | Altitude realizada (m) | Pitch realizado (graus a partir do nadir) | GSD (cm/px) | Quadros train / val | Ladrilhos train / val | Semente | Sítios (quadros) |
|---|---|---|---|---|---|---|---|---|---|
| `ds_morro_clima` | Pilot corpus (1080p) | 1920x1080 | 144.2 a 155.7 (média 149.4) | nao gravado (corpus anterior ao campo pitch; faixa nominal --pitch 0 3.5) | 9.72 | 40 / 8 | 274 / 61 | 11 | sítio -1 (histórico): 48 |
| `ds_morro_4k` | S-nadir-150 (corpus of record) | 3840x2160 | 144.0 a 156.0 (média 150.1) | nao gravado (corpus anterior ao campo pitch; faixa nominal --pitch 0 3.5) | 4.88 | 149 / 31 | 1106 / 225 | 21 | sítio -1 (histórico): 180 |
| `ds_variedade` | S-nadir-150-six | 3840x2160 | 144.2 a 155.7 (média 149.9) | 0.0 a 3.4 (média 1.7) | 4.88 | 156 / 24 | 1135 / 174 | 21 | s0: 30, s1: 30, s2: 30, s3: 30, s4: 30, sm1: 30 |
| `ds_morro_obl` | S-oblique | 3840x2160 | 84.7 a 155.9 (média 120.4) | 26.4 a 51.9 (média 38.4) | 3.92 | 155 / 25 | 968 / 136 | 21 | sítio -1 (histórico): 180 |
| `ds_oblvar` | S-oblique-six | 3840x2160 | 86.1 a 155.6 (média 121.3) | 45.0 a 56.0 (média 50.2) | 3.94 | 152 / 28 | 890 / 144 | 21 | -1: 30, 0: 30, 1: 30, 2: 30, 3: 30, 4: 30 |
| `ds_armado_75` | S-nadir-75 (original) | 3840x2160 | 69.1 a 81.0 (média 75.2) | 0.1 a 3.5 (média 1.7) | 2.45 | 173 / 27 | 1316 / 202 | 41 | sítio -1 (histórico): 200 |
| `ds_armado_35` | S-nadir-35 | 3840x2160 | 32.0 a 38.0 (média 35.1) | 0.0 a 3.5 (média 1.7) | 1.14 | 165 / 35 | 1166 / 242 | 43 | sítio -1 (histórico): 200 |
| `ds_armado_75g` | Twin of S-nadir-35 at 75 m | 3840x2160 | 69.1 a 81.0 (média 75.3) | 0.0 a 3.5 (média 1.7) | 2.45 | 176 / 24 | 1287 / 176 | 43 | sítio -1 (histórico): 200 |
| `ds_armado_150g` | Twin of S-nadir-35 at 150 m | 3840x2160 | 137.1 a 162.8 (média 150.3) | 0.0 a 3.5 (média 1.7) | 4.89 | 173 / 27 | 1215 / 180 | 43 | sítio -1 (histórico): 200 |
| `ds_armado_35_extra` | New frames, 35 m (80) | 3840x2160 | 32.1 a 38.0 (média 34.9) | 0.1 a 3.4 (média 1.6) | 1.14 | 0 / 80 | não ladrilhado | 43 | sítio -1 (histórico): 80 |
| `ds_armado_75g_extra` | New frames, twin at 75 m (80) | 3840x2160 | 69.1 a 80.7 (média 74.5) | 0.0 a 3.5 (média 1.6) | 2.42 | 0 / 80 | não ladrilhado | 43 | sítio -1 (histórico): 80 |
| `ds_armado_75_inedita` | Unseen-weapon test frames (50) | 3840x2160 | 69.2 a 80.8 (média 75.2) | 0.1 a 3.5 (média 1.7) | 2.45 | 47 / 3 | não ladrilhado | 47 | sítio -1 (histórico): 50 |
| `ds_armado_75_porte` | Carried-as-weapon re-render (50) | 3840x2160 | 69.2 a 80.8 (média 75.2) | 0.1 a 3.5 (média 1.7) | 2.45 | 47 / 3 | não ladrilhado | 47 | sítio -1 (histórico): 50 |
| `ds_regime_4k` | Per-regime test frames (120) | 3840x2160 | 144.1 a 156.0 (média 150.1) | 0.0 a 3.5 (média 1.8) | 4.88 | 0 / 120 | 0 / 885 | 21 | sítio -1 (histórico): 120 |

## 2. Instâncias anotadas por classe (rótulos dos quadros inteiros)

| Nome interno | Classes | Train: armada / desarmada / objeto / total | Val: armada / desarmada / objeto / total | Pessoas colocadas | Caixas retidas | Fração retida | Caixas por quadro |
|---|---|---|---|---|---|---|---|
| `ds_morro_clima` | 2 | 292 / 273 / 0 / 565 | 55 / 64 / 0 / 119 | 1088 | 684 | 0.629 | 14.2 |
| `ds_morro_4k` | 2 | 1331 / 1328 / 0 / 2659 | 278 / 288 / 0 / 566 | 4582 | 3225 | 0.704 | 17.9 |
| `ds_variedade` | 2 | 1424 / 1368 / 0 / 2792 | 203 / 233 / 0 / 436 | 4622 | 3228 | 0.698 | 17.9 |
| `ds_morro_obl` | 2 | 839 / 841 / 0 / 1680 | 113 / 119 / 0 / 232 | 4648 | 1912 | 0.411 | 10.6 |
| `ds_oblvar` | 2 | 0 / 1325 / 0 / 1325 | 0 / 196 / 0 / 196 | 4472 | 1521 | 0.34 | 8.4 |
| `ds_armado_75` | 3 | 816 / 820 / 846 / 2482 | 117 / 153 / 135 / 405 | 4361 | 2887 | 0.662 | 14.4 |
| `ds_armado_35` | 3 | 640 / 587 / 619 / 1846 | 137 / 119 / 121 / 377 | 3477 | 2223 | 0.639 | 11.1 |
| `ds_armado_75g` | 3 | 650 / 638 / 701 / 1989 | 85 / 92 / 91 / 268 | 3635 | 2257 | 0.621 | 11.3 |
| `ds_armado_150g` | 3 | 692 / 619 / 640 / 1951 | 92 / 104 / 101 / 297 | 3618 | 2248 | 0.621 | 11.2 |
| `ds_armado_35_extra` | 3 | 0 / 0 / 0 / 0 | 346 / 315 / 292 / 953 | 1448 | 953 | 0.658 | 11.9 |
| `ds_armado_75g_extra` | 3 | 0 / 0 / 0 / 0 | 257 / 292 / 288 / 837 | 1392 | 837 | 0.601 | 10.5 |
| `ds_armado_75_inedita` | 3 | 243 / 212 / 216 / 671 | 13 / 10 / 14 / 37 | 1092 | 708 | 0.648 | 14.2 |
| `ds_armado_75_porte` | 3 | 243 / 212 / 217 / 672 | 13 / 10 / 14 / 37 | 1092 | 709 | 0.649 | 14.2 |
| `ds_regime_4k` | 2 | 0 / 0 / 0 / 0 | 1085 / 1119 / 0 / 2204 | 3044 | 2204 | 0.724 | 18.4 |

## 3. Instâncias por classe nos ladrilhos de treino (o que o detector vê)

| Nome interno | Ladrilhos train / val | Train: armada / desarmada / objeto / total | Val: armada / desarmada / objeto / total | Ladrilhos vazios mantidos train / val |
|---|---|---|---|---|
| `ds_morro_clima` | 274 / 61 | 494 / 486 / 0 / 980 | 95 / 123 / 0 / 218 | 6 / 0 |
| `ds_morro_4k` | 1106 / 225 | 2359 / 2319 / 0 / 4678 | 471 / 528 / 0 / 999 | 10 / 1 |
| `ds_variedade` | 1135 / 174 | 2498 / 2391 / 0 / 4889 | 363 / 413 / 0 / 776 | 13 / 1 |
| `ds_morro_obl` | 968 / 136 | 1430 / 1422 / 0 / 2852 | 194 / 218 / 0 / 412 | 24 / 2 |
| `ds_oblvar` | 890 / 144 | 0 / 2405 / 0 / 2405 | 0 / 341 / 0 / 341 | 26 / 4 |
| `ds_armado_75` | 1316 / 202 | 1276 / 1303 / 1382 / 3961 | 193 / 260 / 215 / 668 | 9 / 1 |
| `ds_armado_35` | 1166 / 242 | 1039 / 957 / 977 / 2973 | 219 / 193 / 186 / 598 | 16 / 3 |
| `ds_armado_75g` | 1287 / 176 | 1058 / 993 / 1131 / 3182 | 135 / 152 / 158 / 445 | 13 / 3 |
| `ds_armado_150g` | 1215 / 180 | 1194 / 1031 / 1068 / 3293 | 169 / 157 / 170 / 496 | 18 / 1 |
| `ds_regime_4k` | 0 / 885 | 0 / 0 / 0 / 0 | 1890 / 1959 / 0 / 3849 | 0 / 9 |

## 4. Regimes de luz, elevação do sol e tempo de render

| Nome interno | Quadros por regime | Elevação do sol realizada (graus) | Render mediano por quadro (s) | Render total (h) |
|---|---|---|---|---|
| `ds_morro_clima` | sol_duro 8, sol_baixo 8, nublado 8, encoberto 8, neblina 8, chuva 8 | 9.1 a 73.7 | 47.8 | 0.64 |
| `ds_morro_4k` | sol_duro 30, sol_baixo 30, nublado 30, encoberto 30, neblina 30, chuva 30 | 9.1 a 74.0 | 182.9 | 11.09 |
| `ds_variedade` | sol_duro 30, sol_baixo 30, nublado 30, encoberto 30, neblina 30, chuva 30 | 9.6 a 69.6 | 172.6 | 8.71 |
| `ds_morro_obl` | sol_duro 30, sol_baixo 30, nublado 30, encoberto 30, neblina 30, chuva 30 | 9.1 a 73.5 | 176.0 | 9.12 |
| `ds_oblvar` | sol_duro 30, sol_baixo 30, nublado 30, encoberto 30, neblina 30, chuva 30 | 9.4 a 73.4 | 181.1 | 10.01 |
| `ds_armado_75` | sol_duro 34, sol_baixo 34, nublado 33, encoberto 33, neblina 33, chuva 33 | 9.8 a 72.7 | 169.3 | 9.5 |
| `ds_armado_35` | sol_duro 34, sol_baixo 34, nublado 33, encoberto 33, neblina 33, chuva 33 | 10.3 a 74.0 | 118.2 | 6.75 |
| `ds_armado_75g` | sol_duro 34, sol_baixo 34, nublado 33, encoberto 33, neblina 33, chuva 33 | 9.6 a 73.2 | 121.1 | 6.87 |
| `ds_armado_150g` | sol_duro 34, sol_baixo 34, nublado 33, encoberto 33, neblina 33, chuva 33 | 9.3 a 73.9 | 128.4 | 7.16 |
| `ds_armado_35_extra` | nublado 14, encoberto 14, neblina 13, chuva 13, sol_duro 13, sol_baixo 13 | 10.4 a 73.6 | 116.2 | 2.65 |
| `ds_armado_75g_extra` | nublado 14, encoberto 14, neblina 13, chuva 13, sol_duro 13, sol_baixo 13 | 9.8 a 74.0 | 122.2 | 2.78 |
| `ds_armado_75_inedita` | sol_duro 9, sol_baixo 9, nublado 8, encoberto 8, neblina 8, chuva 8 | 12.6 a 72.1 | 160.9 | 2.27 |
| `ds_armado_75_porte` | sol_duro 9, sol_baixo 9, nublado 8, encoberto 8, neblina 8, chuva 8 | 12.6 a 72.1 | 157.2 | 2.24 |
| `ds_regime_4k` | sol_duro 20, sol_baixo 20, nublado 20, encoberto 20, neblina 20, chuva 20 | 10.8 a 71.5 | 175.4 | 5.89 |

## 5. VisDrone: imagens e instâncias de pessoa (pedestrian + people fundidas na classe única `pessoa`)

| Conjunto | Nome no artigo | Imagens | Instâncias de pessoa | Imagens sem caixa |
|---|---|---|---|---|
| `visdrone_yolo/train` | VisDrone-DET train (full, 6,471) | 6471 | 106396 | 787 |
| `visdrone_yolo/val` | VisDrone-DET val (test set, 548) | 548 | 13969 | 17 |
| `visdrone_sub/train` | R (1,106 images, seed 21) | 1106 | 18858 | 125 |
| `ft/ft05` | 5 per cent slice (324) | 324 | 5883 | 38 |
| `ft/ft10` | 10 per cent slice (647) | 647 | 11091 | 71 |
| `ft/sel` | 5 per cent selection slice (324) | 324 | 5886 | 29 |

Conferência no formato original do VisDrone-DET val (`VisDrone2019-DET-val/annotations`): 548 imagens, 8844 pedestrian + 5125 people = 13969 instâncias de pessoa; 1378 regiões ignoradas (categoria 0) em 340 imagens, mais 32 linhas de outras categorias com score 0, também descartadas. Regra do conversor: categoria 1 ou 2 e score != 0 (visdrone_to_yolo.py descarta score 0 = regiao ignorada).

Fatias (`visdrone/ft/fatias.json`, `prepara_ft.py`): sel 324, ft05 324, ft10 647 de 6471 imagens de treino; semente 2609; ft05 contido em ft10: True; sel disjunta de ft10: True. A fatia `sel` é a validação (seleção de checkpoint) dos modelos de ajuste fino e dos conjuntos; o teste é o val inteiro.

## 6. Notas de leitura

- Nomes do artigo contra nomes internos: Pilot corpus = `ds_morro_clima` (treino `morro_clima_s`); S-nadir-150 = `ds_morro_4k` (`s_nadir_4k`); S-nadir-150-six = `ds_variedade` (`s_variedade`); S-oblique = `ds_morro_obl` (`s_obliquo`); S-oblique-six = `ds_oblvar` (`s_oblvar`, `_sd1`, `_sd2`); S-nadir-75 = `ds_armado_75` (`armado_75`); S-nadir-35 = `ds_armado_35` (`armado_35`, `_sd1`, `_sd2`); gêmeo a 75 m = `ds_armado_75g` (`armado_75g`, `_sd1`, `_sd2`); gêmeo a 150 m = `ds_armado_150g` (`armado_150g`); quadros novos = `ds_armado_35_extra` e `ds_armado_75g_extra`; arma inédita = `ds_armado_75_inedita`; porte de arma = `ds_armado_75_porte`; teste por regime = `ds_regime_4k`; R = `visdrone_sub/train` (`r_pareado`); F = `ft/ft05`, `ft/ft10` com seleção em `ft/sel`; F-joint = `ds_misto05`, `ds_misto10` (890 ladrilhos de `ds_oblvar_tiles/train` mais a fatia real).
- A GSD da tabela 1 é a realizada (altitude média do manifest); a nominal na altitude de comando está em `gsd_zoom.md` (150 m: 9,76 em 1080p e 4,88 em 4K; 75 m: 2,44; 35 m: 1,14).
- `pitch` não foi gravado no manifest dos dois corpora mais antigos (`ds_morro_clima`, `ds_morro_4k`); a faixa de comando era o padrão `--pitch 0 3.5` (graus a partir do nadir), a mesma realizada nos corpora posteriores de nadir (0,0 a 3,5).
- Amostras do Cycles por quadro (não ficam no manifest; lidas dos comandos em `07-blender/scripts/fila_noite.py`, `rodada3.py` e `rodada4.py`): 96 em `ds_morro_4k`, `ds_variedade`, `ds_morro_obl`, `ds_oblvar`, `ds_armado_75`, `ds_armado_75_inedita`, `ds_armado_75_porte` e `ds_regime_4k`; 64 em `ds_armado_35`, `ds_armado_75g`, `ds_armado_150g` e nos dois `_extra`. Para `ds_morro_clima` o comando não ficou registrado: não apurado.
- Pessoas colocadas contra caixas retidas: a diferença soma três causas que o manifest não separa (visibilidade abaixo de 0,35 em 14 raios, caixa fora do quadro, lado abaixo de 0,2 por cento do quadro). Nos corpora oblíquos a fração retida cai a 0,34 a 0,41 porque a câmera inclinada enquadra uma faixa menor do terreno sorteado.
- As divisões train/val são por quadro (sorteio com probabilidade `--val 0.15` por quadro); os ladrilhos herdam a divisão do quadro. `ds_armado_75_inedita` e `ds_armado_75_porte` têm 47 quadros em train e 3 em val só por herança do sorteio: nenhum dos dois foi usado em treino; os testes usaram `--split todos` (50 quadros).
- As instâncias dos ladrilhos (tabela 3) não somam às dos quadros (tabela 2): a sobreposição de 20 por cento duplica caixas na emenda e caixas com menos de 40 por cento da área dentro do ladrilho são descartadas.
- VisDrone: os rótulos YOLO em disco (`visdrone_yolo`, conversor `03-arma3/scripts/visdrone_to_yolo.py`) fundem pedestrian (8.844 no val) e people (5.125) na classe única `pessoa` e descartam linhas com score 0; as 1.378 regiões ignoradas (categoria 0, 340 imagens) não viram caixa, e é por isso que o validador padrão conta detecção dentro delas como falso positivo (ver `avalia_visdrone_oficial.py`).
