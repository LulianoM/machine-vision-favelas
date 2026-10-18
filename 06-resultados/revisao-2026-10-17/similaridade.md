# Similaridade de recortes por altitude, sem detector (revisão de 17/10/2026, agente D3)

Resposta ao áudio do revisor (10h15 e 10h34 de 14/10; itens A2 e S4 de `01-artigo/feedback-2026-10-14/PLANO-CORRECAO.md`): antes, ou em vez, de um detector de três classes, os autores deveriam propor "algum método de redução de ordem, uma matriz de co-similaridade ou algum dispositivo matemático" que refine o critério de classificação, porque as classes armada, desarmada e objeto são sensíveis demais; e o revisor observou que os erros dos modelos comparados são quase todos os mesmos.

O que se fez: uma análise de similaridade dos recortes anotados, sem detector e sem treino, com um extrator de características congelado que já estava no disco, nos corpora de três classes às três altitudes (35 m, gêmeo a 75 m, gêmeo a 150 m: mesma cena, mesmas figuras, só a altura muda), mais o corpus original de 75 m e os 80 quadros novos de 35 m e do gêmeo de 75 m. Nada aqui entrou no manuscrito; a seção 10 diz o que pode entrar e onde. Todos os números estão em `similaridade.json`; o script é `similaridade.py`, nesta pasta.

## Resumo em cinco linhas

1. A matriz de co-similaridade das características genéricas é plana: todas as entradas ficam entre -0,03 e +0,03 depois de centralizar (e entre 0,71 e 0,79 sem centralizar), e a silhueta das três classes é 0,00 a 0,01 nas quatro altitudes. A única estrutura que aparece é "desarmada contra quem carrega algo"; armada e objeto não se separam em nenhuma altitude.
2. Um classificador por similaridade (centroide mais próximo ou cinco vizinhos) chama de armada 25 a 33 por cento dos objetos e reconhece 36 a 50 por cento das armadas: d' de 0,2 a 0,5 contra 0,8 a 1,0 do detector nos mesmos quadros. A 35 m e no gêmeo de 75 m ele erra mais que o detector tanto no alarme falso quanto no acerto.
3. Descer a 35 m não ajuda: a AUC armada contra objeto é 0,53 a 35 m, 0,58 a 75 m e 0,65 a 150 m (esta com intervalo largo, n de 92 contra 101). É o mesmo sinal do resultado negativo do detector a 35 m.
4. Redução de ordem não cria separação que as características não têm: PCA a 2 dimensões piora (acurácia de 0,35 a 0,43 em três classes), PCA a 10 iguala o espaço inteiro, e a redução supervisionada (LDA a 2) dá o melhor resultado sem detector, ainda com metade do d' do detector.
5. Os erros do critério por similaridade coincidem só em parte com os do detector (phi de 0,1 a 0,4 por figura com objeto): a confusão não é propriedade de figuras específicas vista por qualquer critério, e sim do que o critério consegue ler. O vetor médio do tronco do próprio detector treinado também não separa (AUC 0,49 a 0,57, seção 8): a informação que o detector usa é local e de escala, e não sobrevive a um vetor médio de recorte.

## 1. Método

### 1.1 Recortes

Cada figura anotada (caixa YOLO) vira um recorte com margem de 25 por cento da largura e da altura de cada lado, cortado na borda do quadro 4K. Tamanhos no pool de avaliação (mediana; percentis 10 e 90 entre parênteses), em pixels:

| Altitude (GSD) | Caixa, largura x altura | Recorte, largura | Recorte, altura |
|---|---|---|---|
| 35 m (1,1 cm/px) | 124 x 105 | 185 (103 a 285) | 155 (86 a 247) |
| gêmeo 75 m (2,4 cm/px) | 48 x 41 | 73 (43 a 108) | 62 (39 a 97) |
| gêmeo 150 m (4,9 cm/px) | 21 x 20 | 33 (19 a 50) | 31 (20 a 46) |
| 75 m original (2,4 cm/px) | 45 x 41 | 69 (44 a 106) | 62 (40 a 93) |

Nenhuma caixa degenerada foi descartada. O tipo do objeto carregado (modelo de arma ou objeto) vem do campo `caixas` do manifesto, uma entrada por linha de rótulo, nos corpora que o têm (gêmeos de 75 m e 150 m, quadros novos); nos dois corpora anteriores a esse campo (35 m e 75 m original) ele é reconstruído do campo `tipos` pela regra do gerador (os tipos das linhas das classes 0 e 2, na ordem das linhas). A regra foi conferida nos 560 quadros que têm os dois campos: bate em todos.

### 1.2 Extrator

Tronco do YOLO11s pré-treinado no COCO (`C:/arma3-favela/blender/yolo11s.pt`, o peso inicial de todos os treinos do projeto; Ultralytics 8.4.148, PyTorch 2.14), camadas 0 a 10 do modelo de detecção, congelado, sem nenhum ajuste. O recorte é encaixado em 224 x 224 (lado maior em 224, reamostragem bilinear do PIL, preenchimento cinza 114, como o Ultralytics faz), RGB dividido por 255. O vetor de um recorte é a média espacial da saída da camada 10 (fim do tronco, 512 dimensões), chamada P5; como checagem, o mesmo foi feito com as camadas 4 (P3, 256) e 6 (P4, 256). Extração em CPU, 6 threads, cerca de 5 minutos para 10.405 recortes; vetores guardados fora do git em `C:/arma3-favela/blender/similaridade/emb_<corpus>.npz`. Nada foi baixado.

### 1.3 Pools

O pool de avaliação de cada altitude é a divisão de validação do corpus mais os quadros novos (índices 200 a 279, todos em validação) quando existem. A divisão de treino só entra como pool de referência no protocolo que imita o detector.

| Altitude | Corpus (treino / val) | Quadros novos | Recortes de avaliação (armada / desarmada / objeto) | Recortes de referência (treino) |
|---|---|---|---|---|
| 35 m | `ds_armado_35` (165 / 35) | `ds_armado_35_extra` (80) | 1.330 (483 / 434 / 413) | 1.846 |
| gêmeo 75 m | `ds_armado_75g` (176 / 24) | `ds_armado_75g_extra` (80) | 1.105 (342 / 384 / 379) | 1.989 |
| gêmeo 150 m | `ds_armado_150g` (173 / 27) | nenhum | 297 (92 / 104 / 101) | 1.951 |
| 75 m original | `ds_armado_75` (173 / 27) | nenhum | 405 (117 / 153 / 135) | 2.482 |

### 1.4 Pré-processamento, protocolos e medidas

Cada vetor é centralizado pela média do pool de ajuste e normalizado a norma 1; a similaridade é o cosseno. Sem centralizar, todos os cossenos ficam entre 0,71 e 0,79 por causa da componente comum a todo recorte, e a matriz não mostra nada; a versão centralizada é a que vai nas tabelas e na figura (as duas estão no JSON).

Protocolos:

- `cv_eval` (principal): validação cruzada de 5 dobras, estratificada por classe, sorteio por recorte, no pool de avaliação. Centroides, vizinhos, PCA e LDA são ajustados nas dobras de treino e aplicados à dobra de teste.
- `cv_eval_quadro`: o mesmo com dobras sorteadas por quadro (recortes do mesmo quadro ficam juntos), para medir o vazamento entre recortes do mesmo quadro.
- `ref_para_eval`: ajuste na divisão de treino do corpus e aplicação ao pool de avaliação, com val e quadros novos reportados em separado. É o protocolo do detector e é o que entra na comparação com ele.
- `cv_todos`: validação cruzada por quadro em todos os recortes do corpus (treino, val e novos), só como leitura suplementar com mais dados.

Medidas: matriz 3 x 3 do cosseno médio entre pares de recortes (classe a contra classe b; na diagonal, pares distintos da mesma classe), matriz do cosseno entre centroides, silhueta com distância de cosseno; centroide mais próximo e 5 vizinhos mais próximos com matriz de confusão, recall por classe, fração de objetos chamados de armada, fração de desarmadas chamadas de armada, d' (z do recall de armada menos z da fração de objetos chamados de armada, a fórmula usada no artigo para o detector) e AUC armada contra objeto do score "similaridade ao centroide de armada"; PCA a 2 e 10 dimensões com variância explicada e centroide mais próximo (euclidiano) no espaço reduzido; LDA de Fisher a 2 dimensões com encolhimento 0,1 (extra: a redução supervisionada); taxa por tipo de objeto e por modelo de arma; intervalos de 95 por cento por reamostragem de quadros (2.000 reamostras; 500 para a AUC). Classificadores, PCA, LDA, silhueta e AUC implementados em numpy no próprio script (o ambiente não tem scikit-learn e nada foi instalado).

## 2. Matriz de co-similaridade e silhueta (camada P5, pool de avaliação)

Cosseno médio entre pares, centralizado. Ordem: armada, desarmada, objeto.

| | 35 m | gêmeo 75 m | gêmeo 150 m | 75 m original |
|---|---|---|---|---|
| armada x (armada, desarmada, objeto) | +0,003, -0,005, +0,001 | +0,005, -0,003, -0,000 | +0,000, +0,004, -0,012 | +0,004, -0,011, +0,002 |
| desarmada x (...) | -0,005, +0,025, -0,017 | -0,003, +0,026, -0,021 | +0,004, +0,019, -0,030 | -0,011, +0,020, -0,016 |
| objeto x (...) | +0,001, -0,017, +0,016 | -0,000, -0,021, +0,019 | -0,012, -0,030, +0,032 | +0,002, -0,016, +0,012 |
| silhueta (todas; armada, desarmada, objeto) | 0,002 (-0,017; 0,022; 0,004) | 0,007 (-0,015; 0,024; 0,010) | 0,002 (-0,033; -0,000; 0,036) | 0,006 (-0,009; 0,022; 0,002) |

Cosseno entre centroides (centralizado), que amplia a mesma geometria: a 35 m, armada contra desarmada -0,48, armada contra objeto +0,15, desarmada contra objeto -0,75; no gêmeo de 75 m, -0,21, -0,03 e -0,85; no gêmeo de 150 m, +0,22, -0,55 e -0,86; no 75 m original, -0,57, +0,13 e -0,69.

Leitura. Dentro de cada classe os pares são tão parecidos quanto entre classes: a maior entrada da matriz é 0,03. O único eixo que existe opõe desarmada a objeto (as duas entradas negativas maiores, -0,017 a -0,030, estão sempre nesse par), e armada fica no meio: a 35 m e a 75 m um pouco mais perto de objeto, a 150 m mais perto de desarmada, onde a arma (0,2 a 1,05 m, isto é, 4 a 21 pixels) deixa de ser visível e o objeto longo (até 2,5 m, até 50 pixels) passa a dominar um recorte de 33 pixels. O extrator genérico vê "carrega algo comprido"; não vê "o que carrega". A silhueta de armada é negativa nas quatro altitudes: em média uma figura armada está mais perto de alguma outra classe do que da própria.

## 3. Classificadores por similaridade (camada P5, `cv_eval`)

Centroide mais próximo (CM) e 5 vizinhos (5V). Intervalos de 95 por cento por reamostragem de quadros entre colchetes.

| Altitude | Método | Acurácia (3 classes) | Recall armada / desarmada / objeto | Objeto chamado de armada | Desarmada chamada de armada | d' armada contra objeto | AUC armada contra objeto |
|---|---|---|---|---|---|---|---|
| 35 m | CM | 0,507 | 0,420 / 0,631 / 0,477 | 0,332 [0,285 a 0,375] | 0,214 | 0,23 | 0,525 [0,483 a 0,561] |
| 35 m | 5V | 0,492 | 0,447 / 0,569 / 0,463 | 0,392 | 0,290 | 0,14 | |
| gêmeo 75 m | CM | 0,531 | 0,377 / 0,656 / 0,543 | 0,253 [0,207 a 0,297] | 0,237 | 0,35 | 0,576 [0,531 a 0,622] |
| gêmeo 75 m | 5V | 0,489 | 0,325 / 0,589 / 0,536 | 0,248 | 0,221 | 0,23 | |
| gêmeo 150 m | CM | 0,492 | 0,359 / 0,423 / 0,683 | 0,208 [0,131 a 0,287] | 0,327 | 0,45 | 0,654 [0,574 a 0,730] |
| gêmeo 150 m | 5V | 0,451 | 0,250 / 0,587 / 0,495 | 0,287 | 0,240 | -0,11 | |
| 75 m original | CM | 0,558 | 0,436 / 0,699 / 0,504 | 0,267 [0,187 a 0,360] | 0,176 | 0,46 | 0,534 [0,459 a 0,615] |
| 75 m original | 5V | 0,479 | 0,367 / 0,667 / 0,363 | 0,296 | 0,196 | 0,20 | |

Acaso em três classes equilibradas: acurácia 0,33; AUC 0,50. A AUC do score "similaridade a armada menos similaridade a objeto" (a regra de decisão das duas classes) é 0,62, 0,68, 0,70 e 0,59, nas mesmas quatro altitudes: também fraca.

Os outros protocolos dão o mesmo quadro (centroide mais próximo; acurácia, objeto chamado de armada, recall de armada, AUC):

| Altitude | `cv_eval` | `cv_eval_quadro` | `ref_para_eval` | `cv_todos` |
|---|---|---|---|---|
| 35 m | 0,507; 0,332; 0,420; 0,525 | 0,520; 0,317; 0,439; 0,522 | 0,529; 0,300 [0,259 a 0,342]; 0,470; 0,531 | 0,519; 0,317; 0,428; 0,523 |
| gêmeo 75 m | 0,531; 0,253; 0,377; 0,576 | 0,552; 0,248; 0,392; 0,574 | 0,540; 0,277 [0,231 a 0,329]; 0,412; 0,575 | 0,533; 0,260; 0,400; 0,578 |
| gêmeo 150 m | 0,492; 0,208; 0,359; 0,654 | 0,468; 0,178; 0,315; 0,646 | 0,485; 0,168 [0,101 a 0,245]; 0,293; 0,604 | 0,495; 0,159; 0,258; 0,617 |
| 75 m original | 0,558; 0,267; 0,436; 0,534 | 0,588; 0,252; 0,487; 0,577 | 0,580; 0,244 [0,190 a 0,301]; 0,444; 0,591 | 0,535; 0,273; 0,418; 0,548 |

Não há vazamento relevante entre recortes do mesmo quadro (as dobras por quadro dão números iguais aos das dobras por recorte), e ajustar na divisão de treino inteira (1.846 a 2.482 recortes) não melhora nada: o limite é a informação nas características, não o tamanho do pool.

Camadas mais rasas (P3, camada 4; P4, camada 6), centroide mais próximo em `cv_eval`, AUC armada contra objeto: P3 0,551, 0,572, 0,524 e 0,532; P4 0,514, 0,567, 0,550 e 0,485 (35 m, gêmeo 75 m, gêmeo 150 m, 75 m original). Nenhuma camada separa armada de objeto.

## 4. Redução de ordem (camada P5, `cv_eval`, centroide mais próximo no espaço reduzido)

| Altitude | Variância explicada: 2 dim / 10 dim | PCA 2: acurácia; objeto chamado de armada; recall armada; d' | PCA 10: idem | LDA 2 (supervisionada): idem |
|---|---|---|---|---|
| 35 m | 0,19 / 0,50 | 0,384; 0,491; 0,542; 0,13 | 0,495; 0,300; 0,400; 0,27 | 0,547; 0,329; 0,443; 0,30 |
| gêmeo 75 m | 0,18 / 0,50 | 0,399; 0,298; 0,406; 0,29 | 0,525; 0,240; 0,365; 0,36 | 0,586; 0,259; 0,453; 0,53 |
| gêmeo 150 m | 0,20 / 0,55 | 0,428; 0,257; 0,326; 0,20 | 0,471; 0,267; 0,337; 0,20 | 0,502; 0,198; 0,326; 0,40 |
| 75 m original | 0,18 / 0,52 | 0,348; 0,289; 0,385; 0,26 | 0,526; 0,311; 0,479; 0,44 | 0,514; 0,341; 0,410; 0,18 |

Leitura. Dez componentes guardam metade da variância e toda a (pouca) separação que o espaço de 512 dimensões tem; duas componentes guardam um quinto da variância e perdem até isso (a 35 m, metade dos objetos vira armada). A projeção supervisionada de Fisher, que é o "dispositivo matemático" mais favorável à proposta do revisor porque usa os rótulos para escolher as duas direções, chega a 0,55 a 0,59 de acurácia em três classes e a d' de 0,3 a 0,5 armada contra objeto; na camada P4 ela chega a d' 0,59 (35 m) e 0,72 (gêmeo 75 m), com 0,30 e 0,25 dos objetos chamados de armada e recall de armada 0,52. É o melhor que se consegue sem detector e ainda fica abaixo do detector (seção 6).

## 5. Por tipo de objeto (camada P5, `cv_eval`, centroide mais próximo; fração chamada de armada e n)

| Tipo | 35 m | gêmeo 75 m | gêmeo 150 m | 75 m original |
|---|---|---|---|---|
| guarda-chuva | 0,38 (58) | 0,39 (41) | 0,18 (11) | 0,20 (10) |
| vassoura | 0,23 (65) | 0,25 (53) | 0,12 (16) | 0,22 (27) |
| cano PVC | 0,25 (61) | 0,12 (50) | 0,13 (15) | 0,41 (17) |
| vergalhão | 0,33 (51) | 0,28 (60) | 0,12 (16) | 0,31 (26) |
| tábua | 0,40 (52) | 0,35 (40) | 0,36 (11) | 0,30 (10) |
| rodo | 0,29 (49) | 0,23 (57) | 0,15 (13) | 0,24 (17) |
| enxada | 0,32 (19) | 0,24 (37) | 0,25 (8) | 0,00 (8) |
| tapete enrolado | 0,43 (37) | 0,21 (24) | 0,40 (5) | 0,23 (13) |
| mangueira | 0,52 (21) | 0,18 (17) | 0,50 (6) | 0,43 (7) |

No gêmeo de 75 m o guarda-chuva é o objeto mais chamado de armada também pelo critério de similaridade (0,39), como no detector (0,40 no gêmeo, 0,38 no teste de arma inédita); a 35 m passam à frente a mangueira, o tapete e a tábua, objetos compactos ou largos que a 1,1 cm/px ocupam parte grande do recorte. Com n de 5 a 65 por célula, só as diferenças grandes contam. O recall por modelo de arma está no JSON (`armada_por_modelo`).

## 6. Comparação com o detector (objeto chamado de armada e recall de armada)

Detector: taxas de `confusao_armado.py` já no artigo (IoU 0,5, conf 0,25), sobre todas as figuras anotadas, com figura perdida contando como não chamada de armada; entre parênteses, a taxa só entre as figuras que o detector encontrou, que é a comparável com um classificador que recebe todas as figuras. Similaridade: centroide mais próximo na camada P5, ajustado na divisão de treino e aplicado ao mesmo pool (`ref_para_eval`), com intervalo de 95 por cento por reamostragem de quadros; e o mesmo em validação cruzada no pool (`cv_eval`).

| Pool | n objetos | Detector: objeto chamado de armada (entre detectados) | Detector: recall armada (entre detectados) | Detector: d' | Similaridade `ref_para_eval`: objeto chamado de armada [IC 95%] | Similaridade: recall armada | Similaridade: d' | Similaridade `cv_eval`: objeto chamado de armada |
|---|---|---|---|---|---|---|---|---|
| 35 m, val | 121 | 0,273 (0,379) | 0,569 (0,813) | 0,78 | 0,331 [0,254 a 0,408] | 0,504 | 0,45 | 0,355 |
| 35 m, quadros novos | 292 | 0,253 (0,372) | 0,543 (0,740) | 0,77 | 0,288 [0,237 a 0,343] | 0,457 | 0,45 | 0,322 |
| gêmeo 75 m, val | 91 | 0,165 (0,234) | 0,471 (0,556) | 0,90 | 0,231 [0,151 a 0,316] | 0,388 | 0,45 | 0,231 |
| gêmeo 75 m, quadros novos | 288 | 0,125 (0,158) | 0,432 (0,539) | 0,98 | 0,292 [0,234 a 0,351] | 0,420 | 0,35 | 0,260 |
| gêmeo 150 m, val | 101 | 0,139 (0,246) | 0,337 (0,574) | 0,67 | 0,168 [0,094 a 0,247] | 0,294 | 0,42 | 0,208 |
| 75 m original, val | 135 | 0,237 (0,299) | 0,547 (0,667) | 0,83 | 0,244 [0,188 a 0,303] | 0,444 | 0,55 | 0,267 |

Leitura. Nos quatro pools de 35 m e do gêmeo de 75 m o critério por similaridade chama de armada uma fração de objetos igual ou maior que a do detector (0,29 a 0,33 contra 0,25 a 0,27 a 35 m; 0,23 a 0,29 contra 0,13 a 0,17 no gêmeo) e reconhece menos armadas (0,39 a 0,50 contra 0,43 a 0,57 no total, 0,54 a 0,81 entre as detectadas). O d' do detector é o dobro. A diferença entre 35 m e 75 m que o artigo relata para o detector (objeto chamado de armada 0,273 contra 0,165 no val, 0,253 contra 0,125 nos quadros novos) aparece no mesmo sentido no critério por similaridade em `cv_eval` (0,332 contra 0,253 no pool inteiro) e no val (0,331 contra 0,231), mas não nos quadros novos em `ref_para_eval` (0,288 contra 0,292): com características genéricas a altitude muda pouco a confusão, e o que muda vai no sentido de mais confusão a 35 m, não menos.

## 7. Concordância por figura com o detector

Para cada figura com objeto do pool, o detector a chamou de armada? O critério por similaridade (`ref_para_eval`, centroide) também? Figura perdida pelo detector conta como não chamada de armada.

| Pool | n objetos | Ambos | Só detector | Só similaridade | Nenhum | phi | P(sim. armada dado det. armada) | P(sim. armada dado det. não armada) |
|---|---|---|---|---|---|---|---|---|
| 35 m, val | 121 | 21 | 12 | 19 | 69 | 0,40 | 0,64 | 0,22 |
| 35 m, quadros novos | 292 | 34 | 40 | 50 | 168 | 0,22 | 0,46 | 0,23 |
| gêmeo 75 m, val | 91 | 5 | 10 | 16 | 60 | 0,11 | 0,33 | 0,21 |
| gêmeo 75 m, quadros novos | 288 | 16 | 20 | 68 | 184 | 0,13 | 0,44 | 0,27 |

Com os 5 vizinhos o phi cai a 0,05 a 0,09. Leitura: a 35 m, o objeto que o detector confunde com arma tem duas a três vezes mais chance de ser confundido também pelo critério genérico (0,64 contra 0,22 no val), então parte da confusão é da figura (pose, tamanho, cor do objeto); mas a maior parte dos erros não coincide (phi 0,1 a 0,4), e no gêmeo de 75 m quase nada coincide. A observação do revisor de que os erros dos modelos comparados são os mesmos vale entre detectores treinados na mesma receita; não vale entre o detector e um critério sem modelo.

## 8. Suplemento: o mesmo pipeline com o tronco treinado na tarefa

Para medir o teto do caminho "detectar, depois classificar por similaridade", a extração e a análise foram repetidas com o tronco (camadas 0 a 10) do detector de três classes treinado em cada corpus (`runs/detect/{armado_35, armado_75g, armado_150g, armado_75}/weights/best.pt`), congelado, mesmo recorte, mesma entrada de 224 pixels, mesma média espacial da camada 10. Não é livre de modelo: o tronco viu a divisão de treino e a de validação selecionou o checkpoint; só os quadros novos são inéditos. Camada P5, centroide mais próximo.

| Altitude | Silhueta | Maior entrada da co-similaridade | `cv_eval`: acurácia; objeto chamado de armada [IC]; recall armada; d'; AUC [IC] | `ref_para_eval`, quadros novos (val quando não há): objeto chamado de armada [IC]; recall armada; d' | Variância em 2 / 10 componentes |
|---|---|---|---|---|---|
| 35 m | -0,008 | 0,066 | 0,482; 0,286 [0,243 a 0,333]; 0,323; 0,11; 0,547 [0,511 a 0,584] | 0,219 [0,180 a 0,259]; 0,202; -0,06 | 0,73 / 0,98 |
| gêmeo 75 m | -0,016 | 0,064 | 0,445; 0,340 [0,292 a 0,392]; 0,412; 0,19; 0,502 [0,459 a 0,547] | 0,441 [0,372 a 0,510]; 0,346; -0,25 | 0,77 / 0,98 |
| gêmeo 150 m | -0,042 | 0,026 | 0,377; 0,079 [0,040 a 0,117]; 0,065; -0,10; 0,574 [0,493 a 0,660] | (val) 0,030 [0,000 a 0,065]; 0,044; 0,17 | 0,89 / 1,00 |
| 75 m original | -0,018 | 0,080 | 0,454; 0,207 [0,153 a 0,259]; 0,299; 0,29; 0,494 [0,421 a 0,565] | (val) 0,096 [0,054 a 0,139]; 0,154; 0,28 | 0,79 / 0,98 |

Leitura. O vetor médio do tronco treinado não separa armada de objeto melhor que o genérico (AUC 0,49 a 0,57), e com a concordância por figura entre esse critério e o próprio detector em phi de -0,07 a 0,19. Isso não diz que o detector não tem a informação: diz que ela não está num vetor médio. A decisão do detector é tomada pela cabeça sobre o mapa espacial, na posição da figura e na escala de treino (figura de 20 a 120 pixels num ladrilho de 1.280); a média espacial de um recorte ampliado para 224 pixels descarta a localização e muda a escala, e o espaço resultante é quase degenerado (duas componentes explicam 73 a 89 por cento da variância, contra 18 a 20 por cento no extrator genérico). Consequência para a seção 6.6 do artigo: um classificador por similaridade na saída de um detector exigiria características locais (por exemplo, o vetor do mapa na célula da figura, na escala nativa), não um vetor médio de recorte; isso não foi testado e fica como caminho, não como resultado.

## 9. O que isto responde ao revisor

1. Matriz de co-similaridade: pedida, feita, e é plana. Com um extrator genérico congelado, armada e objeto são a mesma coisa em todas as altitudes; a única separação que existe é entre quem carrega algo e quem não carrega. Isso confirma o diagnóstico do revisor de que as classes são sensíveis: nenhum critério simples sobre aparência genérica as separa.
2. Redução de ordem: pedida, feita, e não substitui o detector. PCA a 10 dimensões preserva o pouco que há; a 2 destrói; a projeção supervisionada melhora um pouco e fica na metade do d' do detector. O "dispositivo matemático" não cria separabilidade; ele só pode organizar a que o extrator entregar.
3. O detector faz algo que a similaridade genérica não faz (d' 0,8 a 1,0 contra 0,2 a 0,5), e mesmo assim pouco. A hierarquia proposta pelo revisor (primeiro um critério de similaridade, depois a classificação) só teria sentido com características aprendidas na tarefa e locais; o vetor médio do tronco treinado não serve (seção 8), e um critério local sobre o mapa do detector é o detector de novo, com outro nome.
4. Altitude: a similaridade genérica também não melhora a 35 m. Isso dá ao artigo um segundo apoio, independente do detector, para o resultado negativo de 35 m (5.4 e 6.2 da estrutura nova): não é só o treino que não aproveita a resolução; a aparência genérica dos recortes a 1,1 cm/px também não separa arma de objeto.
5. Onde entra no texto: em 5.1 (caracterização do alvo, um parágrafo com a matriz, a silhueta e a AUC por altitude, e a figura 13); em 6.1 ou 6.5 como resposta direta ao ponto A2; em 6.6, o caminho "detectar, depois classificar por similaridade" fica condicionado ao suplemento da seção 8. Se o integrador preferir um só número por altitude: AUC armada contra objeto 0,53, 0,58 e 0,65 (35 m, 75 m, 150 m), silhueta 0,00 a 0,01, d' 0,2 a 0,5 contra 0,8 a 1,0 do detector.

## 10. Limitações

- O resultado vale para este extrator (tronco do YOLO11s do COCO, três profundidades). Um extrator auto-supervisionado (DINOv2) poderia ler mais; não estava no disco e a regra desta rodada era não baixar nada quando há peso disponível. Fica como checagem barata para a rodada 5 (só download e inferência).
- O recorte com margem de 25 por cento inclui contexto (laje, beco) que pode dominar o vetor a 150 m, onde o recorte tem 33 pixels. Uma margem menor foi considerada e não testada; a reamostragem bilinear para 224 pixels amplia o recorte de 150 m sete vezes.
- A comparação com o detector não é exata: o detector decide sobre a imagem inteira e perde 21 a 44 por cento das figuras; o critério por similaridade recebe todas as figuras recortadas pela anotação verdadeira. As taxas entre detectados aproximam a condição do classificador, mas não a igualam.
- A divisão de validação de cada corpus selecionou o checkpoint do detector (M2 do plano); por isso os quadros novos são a linha mais limpa da tabela da seção 6.
- Intervalos por reamostragem de quadros medem a variação de amostragem, não a de ajuste; com 24 a 35 quadros de validação os intervalos são largos.

## 11. Arquivos e comandos

- `similaridade.py` (esta pasta): etapas `extrair`, `analisar`, `treinado` e `figura`.
- `similaridade.json`: todos os números (pools, tamanhos, validação da regra de tipos, três camadas, quatro protocolos, por tipo, intervalos, comparação e concordância com o detector, suplemento).
- `06-resultados/figuras/fig13_similaridade.png`: PCA 2-D por altitude (linha de cima) e matrizes de co-similaridade (linha de baixo), em inglês, paleta de `figuras_mpl.py`.
- Vetores (fora do git): `C:/arma3-favela/blender/similaridade/emb_<corpus>.npz` e `emb_<corpus>__<modelo>.npz`.
- Entradas: `C:/arma3-favela/blender/{ds_armado_35, ds_armado_35_extra, ds_armado_75g, ds_armado_75g_extra, ds_armado_150g, ds_armado_75}` (imagens, rótulos e `manifest.jsonl`), `yolo11s.pt`, `runs/detect/{armado_35, armado_75g, armado_150g, armado_75}/weights/best.pt`, e os JSON do detector em `06-resultados/` (`confusao_armado_35_inst.json`, `confusao_armado_75g_inst.json`, `confusao_armado_150g.json`, `confusao_armado_75_inst.json`, `extra_armado_35.json`, `extra_armado_75g.json`).

```
cd 06-resultados/revisao-2026-10-17
C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa extrair --device cpu --threads 6
C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa analisar
C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa treinado --device cpu --threads 6
C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa figura
```
