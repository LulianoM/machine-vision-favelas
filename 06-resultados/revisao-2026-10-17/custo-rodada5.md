# Custo estimado dos experimentos R5-1 a R5-7 (revisão de 2026-10-17, agente D1)

Estimativas para a máquina do desktop (Ryzen 5 5600X, 32 GB, RTX 2060 de 6 GB), a partir dos tempos medidos nesta rodada de revisão e em `RESULTADOS.md`. Nada roda nesta rodada; a tabela serve à decisão A6 do `PLANO-CORRECAO.md`. Hora de GPU e hora de parede coincidem porque render e treino disputam a mesma GPU e a cadeia roda uma etapa de cada vez (quando render e treino rodaram juntos, em 25 e 26/09, os dois ficaram mais lentos; `RESULTADOS.md`, entrada de 25/09: 277 min de máquina para 180 quadros).

## Tempos unitários medidos (origem)

| Etapa | Medido | Origem |
|---|---|---|
| Render de um quadro 4K nadir ou oblíquo a 96 amostras | mediana 173 a 183 s; 180 quadros = 8,7 a 11,1 h | `corpora.md`, tabela 4 (`render_s` dos manifests de `ds_morro_4k`, `ds_variedade`, `ds_morro_obl`, `ds_oblvar`) |
| Render de um quadro 4K a 64 amostras (35 m, gêmeos) | mediana 116 a 128 s; 200 quadros = 6,8 a 7,2 h; 80 quadros = 2,7 h | idem (`ds_armado_35`, `_75g`, `_150g`, `_extra`) |
| Render de um quadro 4K a 96 amostras com três classes (75 m) | mediana 157 a 169 s; 200 quadros = 9,5 h; 50 quadros = 2,2 h | idem (`ds_armado_75`, `_inedita`, `_porte`) |
| Ladrilhamento de 180 a 200 quadros | minutos, desprezível | `tile_dataset.py` |
| Treino de classe única, 60 épocas com paciência 15, 890 a 1.135 ladrilhos | 2,5 a 4,0 h (parada entre a época 46 e a 60) | `checkpoints.md` (`s_nadir_4k` 4,0; `s_variedade` 3,7; `s_obliquo` 2,8; `s_oblvar` 2,5 a 2,9) |
| Treino de três classes, 60 épocas, 1.166 a 1.316 ladrilhos | 2,6 a 5,4 h | `checkpoints.md` (`armado_*`) |
| Treino R (1.106 imagens inteiras do VisDrone a 1280 px, 60 épocas) | 5,9 h | `checkpoints.md` (`r_pareado`) |
| Ajuste fino, 30 épocas | 0,8 h com 324 imagens; 1,5 h com 647 | `checkpoints.md` (`ft05_*`, `ft10_*`) |
| Treino conjunto, 30 épocas, 1.214 a 1.537 imagens | 2,9 a 3,7 h | `checkpoints.md` (`misto05`, `misto10`) |
| Avaliação zero-shot no VisDrone val (548 imagens, imgsz 1280) | minutos por modelo (não cronometrado em arquivo; tomado como 0,1 h) | `avalia_sim2real.py` |
| Matriz de confusão de imagem inteira (imgsz 3840, 24 a 80 quadros) | minutos por corpus (tomado como 0,1 h) | `confusao_armado.py` |

Regra de escala usada: o tempo de treino cresce proporcionalmente ao número de ladrilhos de treino (épocas fixas); o de render, ao número de quadros.

## Estimativas

| # | Experimento | Derivação | GPU (h) | Parede |
|---|---|---|---|---|
| R5-1 | Sementes de treino 1 e 2 para S-nadir-150 e S-oblique | 2 treinos de `ds_morro_4k_tiles` (1.106 ladrilhos, 4,0 h cada se forem as 60 épocas) + 2 treinos de `ds_morro_obl_tiles` (968 ladrilhos, 2,8 h cada) + 4 avaliações no VisDrone (0,4 h). Sem render. | 8,0 + 5,6 + 0,4 = **14** | 14 h, uma noite e meia; corre em paralelo com escrita |
| R5-2 | Variação da semente de cena para S-oblique-six (gerar e treinar) | Por réplica: 6 sítios × 30 quadros a 96 amostras (10,0 h, medido em `ds_oblvar`) + treino (2,5 a 2,9 h) + avaliação (0,1 h) = 13 h. Duas sementes novas de cena (o mínimo para uma faixa) = 26 h; três = 39 h. | **26 a 39** | 1 a 2 dias de máquina por réplica, sequencial |
| R5-3 | Curva de aprendizado sobre o tamanho do corpus (antiga 10.1) | Opção A, só treinos, subconjuntos de S-oblique-six (30, 60, 90, 120 e 152 quadros de treino): tempo proporcional aos ladrilhos, cerca de 2,7 h × (0,2 + 0,4 + 0,6 + 0,8) = 5,4 h de treinos novos (o ponto 152 já existe), mais 4 avaliações; com três sementes por ponto para ter faixa, 16 h. Opção B, estender o corpus para 360 quadros (180 novos): render 10 h + treino com 1.780 ladrilhos (5,4 h) + avaliação = 16 h por semente, 31 h com duas. | A: **6 a 16**; B: **16 a 31** | A cabe num fim de semana; B exige dois a quatro dias |
| R5-4 | Ablação só com sol duro (antiga 10.3) | Corpus de 180 quadros nadir a 150 m só com `--climas sol_duro` (11,1 h, pelo `ds_morro_4k`) + ladrilhos + treino (4,0 h) + teste por regime em `ds_regime_4k` (0,3 h) + avaliação no VisDrone (0,1 h) = 15,5 h. Controle já existe (`s_nadir_4k`). Para separar regime de volume, acrescentar o espelho "tudo menos sol duro" (mesmo custo) = 31 h. | **16 a 31** | 1 a 2 dias |
| R5-5 | Ajuste fino com extrator congelado e taxa menor | Grade mínima: 2 inícios (S-oblique-six, COCO) × 2 congelamentos (`freeze` 0 e 10) × 2 taxas (`lr0` 0,01 e 0,001 com `optimizer SGD` ou AdamW fixo) = 8 treinos de 30 épocas na fatia de 5 por cento (0,8 h cada, menos com backbone congelado) + 8 avaliações = 7,2 h; repetir na fatia de 10 por cento dobra o número de imagens: + 13 h. | **7 a 20** | Meio dia a um dia; o experimento mais barato por pergunta |
| R5-6 | Zero-shot dos modelos nadir numa base real nadir (candidatas de D4) | Download e conversão para YOLO (horas de pessoa, não de GPU; o tamanho depende da base escolhida) + avaliação de `s_nadir_4k`, `s_variedade`, `s_obliquo`, `s_oblvar` e, com `single_cls`, dos três-classes de 150 m, a 0,1 h cada: cerca de 1 h de GPU. Se a base pedir ladrilhamento ou outra escala de entrada, ainda menos de 2 h. | **1 a 2** | Depende do download; GPU em uma tarde |
| R5-7 | Modelo de três classes a 150 m que passe a condição de validade (corpus maior) | O gêmeo de 150 m (200 quadros, 1.215 ladrilhos) deu recall 0,498 com 2,6 h de treino e parada na época 36. Triplicar o corpus: 400 quadros novos a 64 amostras (400 × 128 s = 14,2 h) + treino com cerca de 3.650 ladrilhos (3 × 2,6 a 4,0 h, se a paciência não parar antes: 8 a 12 h) + matriz de confusão (0,2 h) = 22 a 27 h. Sem garantia de passar o critério: o déficit pode ser de GSD, não de volume (ver `gsd_zoom.md`: a 4,88 cm/px a pessoa em planta tem 9,8 px). Mais barato e mais informativo: antes, treinar os 200 quadros com 120 épocas e paciência 30 (5 h) para ver se o teto sobe com tempo de treino. | **22 a 27** (teste prévio: 5) | 1 a 1,5 dia de render e treino |

Soma de todos, no limite inferior: 14 + 26 + 6 + 16 + 7 + 1 + 22 = 92 h de GPU; no superior: 14 + 39 + 31 + 31 + 20 + 2 + 27 = 164 h. Quatro a sete dias de máquina dedicada. A recomendação A6 do plano (R5-1, R5-5 e R5-6 primeiro) custa 22 a 36 h, cerca de um dia e meio, e é a que fecha as perguntas de validade (dispersão entre treinos, custo do cronograma de ajuste fino, geometria do benchmark).

Ressalvas: (1) os tempos de treino medidos incluem paradas antecipadas; um run que vá às 60 épocas custa o teto da faixa; (2) a cadeia morre se o aplicativo for reiniciado (`docs/AMBIENTE-DESKTOP.md`), então a hora de parede real inclui pausas do autor, como as três retomadas registradas em `checkpoints.md`; (3) nenhum tempo de render a 96 amostras com três classes a 150 m foi medido; usou-se o de 64 amostras do gêmeo (128 s) para R5-7.
