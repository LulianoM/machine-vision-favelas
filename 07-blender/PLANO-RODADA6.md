# Rodada 6: plano, critérios fixados antes e custo

Escrito em 04/11/2026 [DESKTOP], antes de qualquer resultado da rodada. Executa a lista
`08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md` inteira, por decisão do autor no mesmo dia
("o que manda é o PDF"), inclusive os itens que a lista deixava para o periódico (3, 5, 6, 7) ou para
pedido de revisor (9). O item 8 (arma na mão) não está nesta cadeia: exige modelagem no rig do MPFB com
verificação visual e entra como grupo próprio quando estiver pronto (seção 7). As regras abaixo são as que
`06-resultados/rodada6_criterios.py` executa. Este arquivo é versionado antes da partida; mudança de
regra depois disso tem de dizer que veio depois e por quê.

Fontes: tempos de `06-resultados/revisao-2026-10-17/custo-rodada5.md` e dos runs da rodada 5
(`checkpoints.md`); comandos de `07-blender/scripts/rodada4.py` e `rodada5.py`; leituras de
resolubilidade da seção 2.3 do `PLANO-RODADA5.md`, sem mudança; caixas das armas de
`06-resultados/armas_malhas.md` (item 1, feito hoje).

## 1. Resumo: ordem, horas e o que cada grupo fecha

| Ordem | Grupo | Item da lista | O que | Seção do artigo | Horas (estimativa) |
|---|---|---|---|---|---|
| 0 | P1 | | Checagem de partida (disco, venv, caminhos, runs livres) | | 0,1 |
| 1 | R | 4 | Teto R com seleção fora do teste: espera o `r_sel.py` lançado às 11:28 e recalcula as eficácias | 4.6, 5.2, 5.3, 6.1, tabela de hipóteses | 6,5 (já em curso) |
| 2 | P2 | | Um quadro de teste com a flag nova do gerador | | 0,1 |
| 3 | Q | 5 | S-nadir-35 e gêmeo de 75 m com 120 épocas e paciência 30; confusão no val e nos 80 quadros novos | 5.4, 6.1 | 10 a 18 |
| 4 | L | 6 | Objetos confundíveis no comprimento das armas: 200 quadros a 75 e a 150 m, 80 novos de cada, dois treinos, confusões cruzadas | 5.4, 6.2, 6.4 | 36 a 44 |
| 5 | E | 7 | Especialista de sol duro com sementes 1 e 2 e o espelho "tudo menos sol duro" | 5.5, 6.3 | 19 a 23 |
| 6 | G | 3 | Ruído, borrão e JPEG como aumento nos ladrilhos de S-nadir-150 e S-oblique-six | 6.5 | 8 a 10 |
| 7 | T | 5, 3, 7 | Sementes 1 e 2 de Q, G e do espelho | 5.4, 5.5, 6.5 | 48 a 60 |
| 8 | V | 9 | Teto R com o treino completo do VisDrone (menos a fatia de seleção) | 4.6, 5.3 | 30 a 36 |
| 9 | H | 8 | Arma na mão: os três gêmeos (35, 75 e 150 m) re-renderizados com a cinemática das mãos, 80 novos de cada, três treinos e120, confusões cruzadas (acrescentado às 12:10, ver 3.7) | 5.4, 6.2 | 50 a 60 |
| 10 | C | | Transferência de cor de Monge-Kantorovich para a estatística do VisDrone train: dois treinos, sementes condicionais a (b), braço combinado com degradação (acrescentado em 04/11 à tarde, ver 3.10) | 6.1, 6.5 | 18 a 36 |
| 11 | Y | | Todos os critérios | | 0,5 |

**Total estimado: 226 a 294 h de máquina** (9,4 a 12,3 dias sem pausas; 208 a 258 h sem o grupo C, 158 a 198 h sem C e H).
Partindo às 12:00 de 04/11, termina entre 13/11 e 15/11, antes do prazo de 19/11 da AIM, com a ordem feita para que os resultados de
uma semente (Q, L, E, G) existam até 08/11 e só as sementes e o teto completo fiquem para a segunda
semana. Hora de GPU e hora de parede coincidem (uma etapa por vez). Pausas do autor somam-se.

## 2. Convenções comuns

Caminhos, receita de treino, moldes de comando e as três leituras de resolubilidade são os da seção 2 do
`PLANO-RODADA5.md`, sem mudança: YOLO11s, imgsz 1280, lote 6, 4 workers, `deterministic=True`, aumentos
de `train_yolo_win.py`, 60 épocas com paciência 15 nos de classe única, ladrilhos de 1280 px com
sobreposição 0,2, seleção do `best.pt` pelo mAP50-95 na divisão `val` do `data.yaml`. Os três-classes
"e120" usam 120 épocas e paciência 30, a receita do `armado_150g_e120` (rodada 5, M2). Estado, logs,
trava e PAUSA em `RAIZ\fila6`; cadeia `07-blender/scripts/rodada6.py`; supervisor, pausa, retrato e
`retoma_rodada6.cmd` são cópias dos da rodada 5.

Leituras (2.3 da rodada 5): **(a)** faixas de sementes que não se cruzam; **(b)** intervalo de 95% por
reamostragem que exclui zero (1.000 reamostras de imagens, semente 0, pareadas, no VisDrone e na HERIDAL;
1.000 de quadros nos três-classes; 2.000 no teste por regime); **(c)** 30% do menor valor, descritiva.
Resolvível = (a) ou (b).

## 3. Experimentos, na ordem da cadeia

### 3.1 Grupo R: item 4, teto R com seleção fora do teste

**Hipótese.** O checkpoint de R foi escolhido no próprio VisDrone val (`checkpoints.md`, achado 1), um
teto com seleção otimista. Escolhido numa fatia fora do teste, R muda pouco (R fez as 60 épocas sem
parada antecipada e a época 58 difere pouco das vizinhas), e as eficácias do artigo (razões a R) mudam na
mesma proporção.

**Etapas.** `r_sel.py` (lançado às 11:28, fora da cadeia): treino `r_pareado_sel` com a receita exata de
`r_pareado` (`--dry-run --compara` acusa só `data` e `name`), `val` = `ft/sel_r.txt`. Achado ao montar a
fatia: `ft/sel` (324 imagens) tem 59 em comum com `visdrone_sub/train`; `sel_r` são as 265 restantes
(`ft/sel_r.json`). Depois: zero-shot no VisDrone val, predições por imagem, e R2 = `rodada6_criterios.py
--parte R`, que grava `rodada6_eficacias.json/.md`.

**Critério, fixado antes.** R-sel passa a ser o teto R do artigo (seleção fora do teste), e **todas** as
eficácias (média das sementes de cada grupo dividida por R) são recalculadas com ele, com intervalo por
reamostragem pareada. A diferença R menos R-sel é reportada como viés de seleção, com intervalo pareado;
se o intervalo exclui zero, o texto diz "viés real, pequeno"; se inclui, "sem viés detectável". Nenhuma
frase sobre ordem entre modelos muda por este item (o denominador é o mesmo para todos).

**Tempo.** 5,9 h de treino (R) mais 0,3 h: cerca de 6,5 h, de 11:28 a cerca de 18:00.

### 3.2 Grupo Q: item 5, a forma em U e o orçamento de treino

**Hipótese.** A curva em U da QP3 (objeto chamado de armada nos 80 quadros novos: 25,3% a 35 m, 12,5% no
gêmeo de 75 m, 24,5% no gêmeo de 150 m) compara modelos de 60 épocas a 35 e 75 m com um de 120 épocas e
paciência 30 a 150 m. Se a vantagem de 75 m sobrevive com orçamento igual, a U é da GSD; se um vizinho a
alcança, a U era em parte orçamento.

**Etapas.** Q1 `TREINO(armado_35_e120, ds_armado_35_tiles, 120, paciência 30)`; Q2 o mesmo para
`armado_75g_e120`; Q3 `CONF` de cada um no seu val e nos seus 80 quadros novos (`confusao_<run>.json`,
`extra_<run>.json`); Q4 critérios. Sementes 1 e 2 dos dois no grupo T (T1 a T5).

**Critério, fixado antes.** Nos 80 quadros novos. (i) e120 contra e60 na mesma altitude: pareado (os
mesmos quadros), d′ e objeto chamado de armada, (b) e (c); com as sementes, (a). (ii) Curva com orçamento
igual: 75 m contra 35 m e 75 m contra 150 m, todos e120, reamostragem independente. **U confirmada com
orçamento igual** = a 120 épocas o gêmeo de 75 m continua com objeto chamado de armada abaixo de 35 m e de
150 m pela leitura (b) nas duas comparações. **U era (em parte) orçamento** = pelo menos uma das duas
deixa de passar em (b) ou inverte. O texto da 5.4 e da 6.1 passa a citar a curva com orçamento igual, e a
de 60 épocas fica como primeira medida.

**Tempo.** 261 s por época a 150 m; a 35 e 75 m os corpora têm 1.166 a 1.316 ladrilhos (2,6 a 5,4 h nas 60
épocas). Com 120 épocas e paciência 30: 5 a 9 h cada. **10 a 18 h** (seed 0); as sementes, outro tanto
dobrado.

### 3.3 Grupo L: item 6, o comprimento como atalho, testado de fato

**Hipótese.** A 4,88 cm/px a forma transversal da arma não existe no sensor (largura abaixo de 1 px,
`armas_malhas.md`); o que a rede pode usar para separar armada de objeto é o comprimento (0,62 a 1,05 m
contra 0,88 a 2,5 m), o material e o ângulo de porte. Com os objetos escalados para a faixa de
comprimento das armas, se a separação some, ela era comprimento; se fica, a forma (ou o material)
sobrevive.

**Etapas.** Gerador com `--objetos-comprimento-arma` (novo: cada objeto confundível é escalado só no eixo
do comprimento até medir um sorteio uniforme em [0,62, 1,05] m; largura, altura e material não mudam;
como nenhum passa de 1,15 m, também não há o reângulo dos objetos longos). P2 prova a flag num quadro.
L1 `RENDER(ds_armado_75c, 200, GEMEO75 + flag)`; L2 ladrilhos; L3 `TREINO(armado_75c, 60)` (a receita do
`armado_75g`); L4 `RENDER(ds_armado_150c, 200, GEMEO150 + flag)`; L5 ladrilhos; L6
`TREINO(armado_150c_e120, 120, paciência 30)` (a receita do `armado_150g_e120`); L7 80 quadros novos de
cada (índices 200 a 279, `--val 1.0`); L8 confusões: cada modelo novo no seu val e nos seus 80 novos; os
novos nos 80 originais (`extra75g_armado_75c.json`, `extra150g_armado_150c_e120.json`); os modelos
originais nos 80 novos de comprimento igual (`extra75c_armado_75g.json`,
`extra150c_armado_150g_e120.json`); L9 critérios.

**Critério, fixado antes.** Para cada altitude, o modelo treinado com objetos no comprimento das armas,
medido nos seus 80 quadros novos (objetos no comprimento das armas): se o intervalo de d′ (armada contra
objeto, 1.000 reamostras de quadros, semente 0) **inclui zero**, a separação nessa altitude dependia do
comprimento (atalho confirmado); se **exclui**, a forma sobrevive sem o comprimento, e a queda contra o
modelo original é dada por (b) independente e (c). Cruzado, descritivo: o modelo original nos quadros de
comprimento igual mede quanto do seu falso alarme vem do comprimento. Uma semente por modelo: (a) não se
aplica. A regra "a forma se perde a 4,88 cm/px" (hoje uma leitura) e "o comprimento é alternativa não
testada" (6.2, 6.4) passam a medida.

**Tempo.** Render 200 quadros a 75 m a 64 amostras: 7,1 h; a 150 m: 7,1 h; 80 novos de cada: 5,7 h;
treinos 2,6 a 5,4 h e 5 a 9 h; confusões 0,5 h. **36 a 44 h**.

### 3.4 Grupo E: item 7, D-ii sem "nulo por regra"

**Hipótese.** Na rodada 5, D-ii (especialista de sol duro sob sol duro menos generalista sob nublado) deu
intervalo que inclui zero, lido pela regra como "queda de participação no treino". Com três sementes de
cada lado e o espelho "tudo menos sol duro" (o regime nublado com a participação máxima possível do outro
lado), a comparação deixa de depender de um treino único e de um generalista que vê um sexto de cada
regime.

**Etapas.** E1, E2 `TREINO(s_soldur_4k_sd1 e _sd2)` (o corpus existe); E3 `RENDER(ds_semsol_4k, 180,
NADIR4K com --climas sol_baixo,nublado,encoberto,neblina,chuva)` (mesma semente de cena e sítio); E4
ladrilhos; E5 `TREINO(s_semsol_4k)`; E6 `por_regime.py --por-quadro` para os dois especialistas novos, o
espelho e as sementes 1 e 2 do generalista (`s_nadir_4k_sd1`, `_sd2`, que não tinham medida por regime);
E7 zero-shot dos três, exploratório; E8 critérios. Sementes 1 e 2 do espelho em T11 a T13.

**Critério, fixado antes.** Recall a conf 0,25 em imagem inteira nos 120 quadros de teste por regime
(`ds_regime_4k`, 20 por regime), 2.000 reamostras de quadros, semente 0, na média das sementes de cada
lado. **E-iii decide:** especialista de sol duro sob sol duro menos espelho sob nublado (independente).
Intervalo inteiro abaixo de zero: regime intrinsecamente mais difícil, resolvível, e a 6.3 recupera o
condicional "quando voar"; intervalo que inclui zero: não resolvível com 20 quadros por regime, e a 6.3
diz isso em vez de "nulo por regra"; (a) com as sementes dos dois lados, (c) no mAP50. D-ii repetida com
sementes (especialista contra generalista sob nublado) fica como leitura secundária.

**Tempo.** Dois treinos de 4 h; render 180 quadros a 96 amostras 8,7 a 11,1 h; treino 4 h; por regime
0,5 h: **19 a 23 h** (seed 0 do espelho).

### 3.5 Grupo G: item 3, ruído, borrão e JPEG como aumento

**Hipótese.** Os renders não têm ruído de sensor, borrão nem compressão (`gerador-fatos.md`), e a 6.5
declara isso como limitação não medida. Se treinar com essas degradações como aumento sobe o zero-shot
no VisDrone ou na HERIDAL, parte da lacuna sim-to-real é artefato de sensor; se não, não é.

**Etapas.** G1 `degrada_ladrilhos.py` (novo) sobre `ds_morro_4k_tiles` e `ds_oblvar_tiles`: cada
ladrilho de treino sai degradado com probabilidade 0,75 (ruído gaussiano dependente do sinal, sigma
0,004 a 0,018; borrão 0,3 a 1,2 px; JPEG 50 a 90 com 4:2:0), limpo nos outros; validação sem mudança;
semente 0; parâmetros por ladrilho em `_degradacao.json`. G2 `TREINO(s_nadir_4k_deg)`, G3
`TREINO(s_oblvar_deg)`; G4 zero-shot, predições no VisDrone e na HERIDAL (1152 e 1280); G5 critérios.
Sementes 1 e 2 em T6 a T10.

**Critério, fixado antes.** Degradado menos limpo, média das sementes, no VisDrone val (pareado) e na
HERIDAL a imgsz casado (pareado); (a) com três sementes de cada lado (as limpas existem); (c). Resolvível
para cima: a falta de artefatos explica parte da lacuna, e a 6.5 ganha a medida; não resolvível: não
explica; resolvível para baixo: degradar prejudica (reportado). A frase atual da 6.5 só muda se resolvível.

**Tempo.** Degradar: minutos. Dois treinos: 2,5 a 4 h cada; avaliações 1 h. **8 a 10 h**.

### 3.6 Grupo V: item 9, teto com o treino completo

**Hipótese.** R com 1.106 imagens é o teto do protocolo pareado, não do VisDrone. Com o treino inteiro
menos a fatia de seleção (6.471 menos 324 = 6.147 imagens; a seleção fica em `sel`, disjunta do treino e do
val) o teto sobe, e as eficácias ganham uma segunda referência.

**Etapas.** V1 lista `train_sem_sel.txt` e `data_cheio_sel.yaml`; V2 `TREINO(r_cheio_sel, 60, classe
única, seleção em sel)`; V3 zero-shot e predições. Descritivo: razão R-full / R-sel com intervalo pareado;
eficácias / R-full em `rodada6_eficacias`. O texto continua a declarar R como teto do protocolo e cita o
teto completo como referência.

**Tempo.** 5,9 h por 1.106 imagens: 6.147 imagens, cerca de 33 h nas 60 épocas. **30 a 36 h**.

### 3.7 Grupo H: item 8, arma na mão (acrescentado às 12:10 de 04/11, antes de qualquer resultado)

**O que mudou no gerador.** `people_mpfb.ARMA_NA_MAO` e `gen_morro.py --arma-na-mao`: a origem da arma
(a empunhadura) vai ao centro da palma direita (entre o fim do osso `wrist.R` e a articulação
`finger3-1.R`), as três falanges dos cinco dedos da mão direita fecham sobre o cabo (polegar menos), e
nas poses de duas mãos (`empunhando`, menos pistola) o braço esquerdo é levado por IK (`lowerarm02.L`,
cadeia de 4 ossos) até um alvo no guarda-mão, e a mão esquerda fecha também. Vale igual para arma e para
objeto confundível, para não criar um indício novo. O jitter dos dedos usa um gerador próprio
(derivado do nome da arma): a flag não muda nenhum sorteio, e a mesma semente dá os mesmos quadros.
Conferência visual por `testa_mao.py` (CPU, 3 m e zoom nas mãos): sentido de flexão +1 fecha a mão (o
-1 a hiperestende); figura em `06-resultados/figuras/item8_mao_conferencia.jpg`.

**Hipótese.** A 35 m (1,14 cm/px) a mão tem 4 px e a diferença entre arma pousada na ponta do punho e
arma empunhada pode mudar a silhueta armada e a taxa de objeto chamado de armada; a 75 e 150 m a
diferença é sub-pixel e o efeito esperado é nulo, o que é parte do que se mede.

**Etapas.** P3 prova a flag num quadro. Para cada gêmeo (35, 75g, 150g): render de 200 quadros com o
comando original mais `--arma-na-mao` (`ds_armado_<tag>m`), ladrilhos, `TREINO(armado_<tag>m_e120, 120,
paciência 30)` (a receita e120 do grupo Q, para comparar com `armado_<tag>_e120`), 80 quadros novos
(índices 200 a 279). H13: confusões de cada modelo novo no seu val e nos seus 80 novos; os e120
originais nos 80 novos com mão (`extra<tag>m_armado_<tag>_e120.json`); os novos nos 80 originais
(`extra<tag>_armado_<tag>m_e120.json`). H14 critérios. Fora do grupo, declarado: o corpus original de
75 m (`ds_armado_75`, 96 amostras), a arma inédita e o porte não são re-renderizados.

**Critério, fixado antes.** Por altitude, modelo com mão nos seus 80 novos contra o e120 original nos
seus 80 (mesmos índices, reamostragem independente, 1.000, semente 0): d′ e objeto chamado de armada,
(b) e (c); uma semente por lado, (a) não se aplica. Resolvível = a cinemática das mãos muda a medida
nessa altitude e o texto da 5.4 diz qual; não resolvível = sub-pixel, e a 6.5 perde a limitação "a arma
é pousada na ponta do punho" como fonte de viés.

**Tempo.** Render 3 × 200 quadros a 128 s: 21 h; 3 × 80 novos: 8,5 h mais o sorteio sem render; três
treinos e120: 15 a 27 h; confusões 1 h. **50 a 60 h**.

### 3.8 Grupo T: sementes

T1 a T4: `armado_35_e120_sd1`, `armado_75g_e120_sd1`, `_sd2`, `_sd2` (intercaladas); T5 confusões (val e
80 novos); T6 a T9: `s_nadir_4k_deg_sd1`, `s_oblvar_deg_sd1`, `_sd2`, `_sd2`; T10 avaliações; T11, T12:
`s_semsol_4k_sd1`, `_sd2`; T13 por regime; T14 critérios com sementes. **48 a 60 h**.

### 3.10 Grupo C: transferência de cor (acrescentado em 04/11 à tarde, antes de qualquer resultado)

**Hipótese.** Parte da lacuna sim-to-real pode ser aparência de cor (balanço de branco, brilho, saturação e
correlação entre canais), e não geometria. Se levar a estatística de cor de segunda ordem dos ladrilhos à de
imagens reais sobe o zero-shot, a aparência explica parte da lacuna; se não sobe, a lacuna é geometria, que é a
tese do artigo.

**Etapas.** `07-blender/scripts/transfere_cor.py`, fora de linha como `degrada_ladrilhos.py`. C1: média (3) e
covariância (3x3) RGB em 0..1 de cada imagem de `visdrone_yolo/train/images` (6.471; nunca o val, que o script
recusa), numa grade de passo 4 px, sem rótulo, em `C:\arma3-favela\visdrone\cor_visdrone_train.json`. C2: para
cada ladrilho de treino de `ds_morro_4k_tiles` e `ds_oblvar_tiles`, com probabilidade 0,75 e semente 0, sorteia
uma imagem real alvo (mu_t, S_t), calcula (mu_s, S_s) do próprio ladrilho e aplica o mapa linear de
Monge-Kantorovich T = S_s^-1/2 (S_s^1/2 S_t S_s^1/2)^1/2 S_s^-1/2, x' = T (x - mu_s) + mu_t, recorte em 0..1
(raízes por autodecomposição, autovalores no mínimo 1e-6); JPEG 92 4:4:4 como os limpos; os outros 25% saem
limpos byte a byte; validação intacta por link físico; parâmetros por ladrilho em `_transferencia.json`.
Conferido antes da partida numa amostra fora das pastas da rodada: T S_s T' = S_t com erro 2e-14, média
transferida igual à do alvo, limpos e val idênticos byte a byte. C3, C4: `TREINO(s_nadir_4k_ct)` e
`TREINO(s_oblvar_ct)`, receita da 7.6, semente 0. C5: zero-shot no VisDrone val a 1280 e a 1024 (os limpos
também a 1024, `sim2real_<run>_1024.json`), predições por imagem no VisDrone (1280) e na HERIDAL (1152, casado,
e 1280). C6: critério. C7, C8: sementes 1 e 2 do braço transferido, só nos corpora em que (b) passou em algum
benchmark (`rodada6_criterios.json`, campo `C.sementes_indicadas`), com avaliação; dispensadas se nenhum
passou. Desvio declarado do pedido: as sementes ficam no próprio grupo C, e não no T, porque o T roda antes do
C na cadeia e a condição depende do resultado de C6. C9 a C12, braço combinado (opcional): `degrada_ladrilhos.py`
sobre os ladrilhos já transferidos (as duas sorteadas com probabilidade 0,75, independentes), treinos
`s_nadir_4k_ctdeg` e `s_oblvar_ctdeg`, avaliação. C13: critério com sementes e combinado.

**Critério, fixado antes.** Transferido menos limpo, pareado por imagem, 1.000 reamostras, semente 0, no
VisDrone val (1280) e na HERIDAL (imgsz casado); leituras (b) e (c); (a) só quando houver sementes dos dois
lados (as limpas existem nos dois benchmarks). Por corpus: **resolvível para cima no VisDrone e não na
HERIDAL** = a aparência explica parte da lacuna, específica do alvo; **para cima nos dois** = aparência
genérica; **nulo nos dois** = a lacuna é geometria, que é a tese; qualquer outra combinação (para baixo, ou
para cima só na HERIDAL) é reportada como caso não previsto, com os dois números. A 1024 e o braço combinado
são descritivos.

**Tempo.** Estatística 0,5 a 1 h de CPU; transferência 0,5 h; dois treinos 6,5 a 8 h; avaliações 1,5 h;
sementes condicionais 0 a 16 h; combinado 9 h. **18 a 36 h**.

### 3.9 Grupo Y

Y1: `rodada6_criterios.py --parte tudo`.

## 4. Desenho da cadeia

Molde da rodada 5: prova por etapa, render retomável pelo manifest, treino retomável de `last.pt` com
`TREINO_OK`, trava, PAUSA, duas tentativas, grupo que falha não impede os outros. Particularidades:

- R1 espera o processo `r_sel.py` (lançado fora da cadeia) terminar, escrevendo no log a cada 15 min; o
  supervisor não mata a cadeia enquanto houver `r_sel.py` vivo.
- P2 (quadro de teste com a flag) roda depois de R, porque a GPU está com o treino de R até lá; L1 exige a
  prova de P2.
- Grupos G e T usam a HERIDAL se `real_nadir\heridal\yolo\data.yaml` existir (existe desde a rodada 5).
- Scripts novos: `rodada6.py`, `supervisiona_rodada6.py`, `pausa_rodada6.py`, `status_rodada6.py`,
  `retoma_rodada6.cmd`, `degrada_ladrilhos.py`, `06-resultados/rodada6_criterios.py`. Modificados,
  compatíveis para trás: `objetos_alongados.py` (`COMPRIMENTO_ARMA`), `gen_morro.py`
  (`--objetos-comprimento-arma`).
- Lançamento pela sessão com `Start-Process cmd.exe -ArgumentList '/c retoma_rodada6.cmd'` (o único modo
  que carrega o MPFB a partir da sessão, visto em 18/10). Atalho na pasta Inicializar só com o OK do autor.

## 5. Cronograma previsto (partida 04/11 às 12:00, sem pausas)

| Grupo | Início | Fim |
|---|---|---|
| R (em curso desde 11:28) | 04/11 11:28 | 04/11 18:00 |
| P2, Q | 04/11 18:00 | 05/11 12:00 |
| L | 05/11 12:00 | 07/11 06:00 |
| E | 07/11 06:00 | 08/11 03:00 |
| G | 08/11 03:00 | 08/11 13:00 |
| T | 08/11 13:00 | 10/11 19:00 |
| V | 10/11 19:00 | 12/11 05:00 |
| H | 12/11 05:00 | 14/11 15:00 |
| C | 14/11 15:00 | 16/11 03:00 |
| Y | 16/11 03:00 | 16/11 04:00 |

## 6. Regras que continuam valendo

Nenhum número entra no texto sem estar em `06-resultados/RESULTADOS.md` com o comando; o manuscrito não
cita caminho, arquivo, script nem corpus; renders derivados da PCERJ não saem do desktop (toda esta
rodada é procedural, `gen_morro.py`, e pode ser ilustrada).

## 7. Item 8, arma na mão: como entrou

Às 11:48 a cadeia partiu sem o item 8. Entre 11:50 e 12:10 a cinemática das mãos foi implementada e
conferida visualmente (seção 3.7) e o grupo H foi acrescentado no fim da cadeia, depois de V e antes de
Y, sem nenhum resultado da rodada existir (a cadeia estava em R1, esperando o treino do item 4). A
cadeia foi reiniciada para carregar as etapas novas; o supervisor a relança sozinho. Se o grupo H não
couber antes do prazo da AIM, o autor pausa a rodada e o item fica para o periódico, com o gerador já
pronto.

## 8. Mudanças depois da partida

- 04/11, 12:10: grupo H (item 8) acrescentado (seção 7).
- 04/11, 14:38 a 16:11: pausa pedida pelo autor; cronograma deslocado em cerca de 1,5 h.
- 04/11, cerca de 16:40: grupo C (seção 3.10) acrescentado depois do H, a pedido do autor, com critério fixado
  antes de qualquer resultado da rodada (a cadeia estava em R1, no treino do item 4). Cronograma da seção 5
  estendido até 16/11; prazo da AIM em 19/11.
- 05/11, 22:00: **ordem nova da cadeia a partir do grupo L**, pedida pelo autor depois dos resultados de R (item 4)
  e Q (item 5), pela criticidade do dado para o artigo da AIM (prazo 19/11, corte de texto em 15/11). **Nenhum
  critério muda, só a ordem.** Ordem: L (em curso, L3 treinando; L1 a L9 como no plano, cruzados e critério
  incluídos); R3 e R4, acertos do item 4 (R-sel na HERIDAL a 1152 e 1280 com predições por imagem, e o critério R
  de novo com todas as linhas da Tabela 4, F-joint incluído, e as eficácias da HERIDAL contra R-sel com intervalo
  pareado); G (item 3); T1 a T5 (sementes 1 e 2 de `armado_35_e120` e `armado_75g_e120` e confusões) seguidos de Q5,
  o critério do item 5 com as três sementes (leitura (a)); E (item 7); T6 a T14; H, V e C, nesta ordem, **só se a
  previsão do grupo terminar antes de 15/11 às 12:00** (regra executada pela cadeia: no início de cada um desses
  grupos ela soma a previsão das etapas pelos tempos do `status_rodada6.py` e, se passar do prazo, marca o grupo
  como `adiada_periodico` e não o inicia; um grupo já começado continua; a regra é reavaliada a cada passagem,
  inclusive depois de uma pausa; `rodada6.py --sem-prazo` a desliga depois da submissão); Y.
  Feitos à mão na mesma hora, sem GPU: o critério R com todas as linhas da Tabela 4 (`rodada6_eficacias.md` ganhou
  a tabela por treino individual) e a Figura do ajuste fino regerada com R-sel (`figuras_mpl.py`, rótulo
  "0.6224"). Para não lançar um segundo processo por cima de um render ou treino que sobreviva ao reinício, a
  cadeia agora espera o processo anterior terminar (`espera_orfao`). A previsão do status passou a contar 95% das
  120 épocas nos treinos longos (os dois já feitos foram a 120 e 109). Previsão por grupo às 21:56 de 05/11, sem
  pausas: L até 07/11 00:49; R3 e R4 até 01:29; G até 07/11 10:02; T1 a T5 e Q5 até 08/11 18:23; E até 09/11
  16:43; T6 a T14 até 10/11 17:49; H até 13/11 02:23; V até 14/11 11:29; C terminaria em 15/11 22:30, depois do
  prazo, e pela regra fica para o periódico se a previsão não melhorar até lá.
