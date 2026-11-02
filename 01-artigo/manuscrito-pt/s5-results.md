## Resultados

A Seção 5.1 relata a caracterização independente de modelo do alvo, as Seções 5.2 a 5.5 relatam os Experimentos A a D na ordem das questões de pesquisa, e a Seção 5.6 aplica os critérios das Seções 4.6 e 4.7 a cada verificação pré-especificada. A Tabela @tab{visao} reúne cada modelo com seu conjunto de teste e seu número principal; o que as observações significam para QP1 a QP3 fica para a Seção 6.

Um resultado por questão. Para QP1, treinado apenas com imagens sintéticas, o detector recuperou 2,2; 8,8 e 15,3% do teto no benchmark urbano, como médias de três execuções de treino, na geometria nadir, na geometria oblíqua do mesmo assentamento e na melhor configuração oblíqua; no benchmark nadir a ordem se inverteu, 62,7% do teto para o modelo nadir contra 42,1 e 46,4 para os dois modelos oblíquos, com faixas sobre execuções de treino que se sobrepõem (Seção 5.2). Para QP2, o início sintético não trouxe ganho uma vez disponíveis 5 ou 10% das imagens reais de treino: 0,4424 contra 0,5220 para o início genérico a 5% e 0,5095 contra 0,5709 a 10, no cronograma original (Seção 5.3). Para QP3, os detectores de três classes chamaram de armado um objeto confundível em 25,3; 12,5 e 24,5% dos casos a 1,14; 2,44 e 4,88 cm por pixel nos quadros independentes, a partir da primeira execução de treino de cada modelo, de modo que a taxa foi mais baixa na GSD intermediária (Seção 5.4).

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:visao|Resultados em síntese: mAP50 em VisDrone-DET val com intervalos de 95% por reamostragem das 548 imagens de teste, e eficácia em relação a R nas mesmas reamostragens; onde um modelo foi treinado três vezes, a média das três execuções com seu intervalo, e a melhor execução. As últimas linhas de classe única dão o benchmark nadir, HERIDAL, no tamanho de entrada pareado. Os modelos de três classes trazem seu mAP50 de três classes e a taxa de objeto na confiança 0,25 em sua divisão de seleção e em quadros independentes (held-out) renderizados após o treino.-->

| Modelo | Dados de treino (imagens reais) | Conjunto de teste | mAP50 (intervalo de 95%) | Eficácia (intervalo de 95%) |
|---|---|---|---|---|
| R | 1.106 imagens de VisDrone-DET train (1.106) | VisDrone-DET val | 0,6311 (0,6149 a 0,6471) | teto |
| S-nadir-150, média de 3 sementes (melhor execução) | 180 quadros, 1 assentamento, nadir, 4,88 cm/px (0) | VisDrone-DET val | 0,0136 (0,0120 a 0,0160); melhor 0,0198 | 2,2% (1,9 a 2,5); melhor 3,1% |
| S-nadir-150-six | 180 quadros, 6 assentamentos, nadir, 4,88 cm/px (0) | VisDrone-DET val | 0,0190 (0,0142 a 0,0211) | 3,0% (2,3 a 3,3) |
| S-oblique, média de 3 sementes (melhor execução) | 180 quadros, 1 assentamento, oblíquo, 3,90 cm/px nominal (0) | VisDrone-DET val | 0,0555 (0,0502 a 0,0614); melhor 0,0614 | 8,8% (8,1 a 9,6); melhor 9,7% |
| S-oblique-six, média de 3 sementes (melhor execução) | 180 quadros, 6 assentamentos, inclinação da câmera de 45 a 56 graus (0) | VisDrone-DET val | 0,0966 (0,0896 a 0,1048); melhor 0,1055 | 15,3% (14,4 a 16,5); melhor 16,7% |
| F-synthetic, 5 e 10%, primeira semente de treino (as três sementes a 5% estão na Tabela @tab{ajuste}) | a partir de S-oblique-six (324 e 647) | VisDrone-DET val | 0,4424 (0,4260 a 0,4587); 0,5095 (0,4935 a 0,5264) | 70,1% (68,4 a 71,8); 80,7% (79,3 a 82,1) |
| F-generic, 5 e 10%, primeira semente de treino (as três sementes a 5% estão na Tabela @tab{ajuste}) | a partir dos pesos COCO (324 e 647) | VisDrone-DET val | 0,5220 (0,5045 a 0,5403); 0,5709 (0,5535 a 0,5883) | 82,7% (81,4 a 84,1); 90,5% (89,2 a 91,6) |
| F-generic, taxa de aprendizado menor (escolhida na fatia de seleção), 5 e 10% | a partir dos pesos COCO (324 e 647) | VisDrone-DET val | 0,5897 (0,5748 a 0,6073), média de 3 sementes; 0,6224 (0,6072 a 0,6396) | 93,4% (92,3 a 94,8); 98,6% (97,4 a 100,1) |
| F-joint, 5 e 10% | pesos COCO, 890 ladrilhos sintéticos e as imagens reais (324 e 647) | VisDrone-DET val | 0,4607 (0,4444 a 0,4789); 0,5428 (0,5259 a 0,5610) | 73,0% (71,6 a 74,6); 86,0% (84,8 a 87,4) |
| R no benchmark nadir | como acima (1.106) | HERIDAL, 1.647 imagens | 0,3185 (0,2843 a 0,3543) | teto |
| S-nadir-150 no benchmark nadir, média de 3 sementes | como acima (0) | HERIDAL | 0,1997 (0,1713 a 0,2306) | 62,7% |
| S-oblique no benchmark nadir, média de 3 sementes | como acima (0) | HERIDAL | 0,1341 (0,1149 a 0,1555) | 42,1% |
| S-nadir-75 | 200 quadros, 3 classes, 2,44 cm/px (0) | divisão de seleção, 27 quadros; independentes, 50 | 0,579; taxa de objeto 0,237; independentes 0,152 | não se aplica |
| S-nadir-35 | 200 quadros, 3 classes, 1,14 cm/px (0) | divisão de seleção, 35; independentes, 80 | 0,514; taxa de objeto 0,273; independentes 0,253 | não se aplica |
| Gêmeo de S-nadir-35 a 75 m | o corpus de 35 m a 2,44 cm/px (0) | divisão de seleção, 24; independentes, 80 | 0,508; taxa de objeto 0,165; independentes 0,125 | não se aplica |
| Gêmeo de S-nadir-35 a 150 m, treinado por mais tempo | o corpus de 35 m a 4,88 cm/px (0) | divisão de seleção, 27; independentes, 80 | 0,388; taxa de objeto 0,178; independentes 0,245 | não se aplica |

</div>

### 5.1 Caracterização do alvo: tamanho, forma e contraste

Medidos apenas nas anotações e nos pixels renderizados, a GSD definiu o tamanho do alvo, a inclinação da câmera definiu sua forma, o regime de iluminação deslocou seu contraste em relação à desordem visual (clutter) local, e os recortes das três classes separaram-se apenas fracamente sob um extrator genérico congelado em cada uma das três GSDs, menos do que sob o detector.

**Tamanho.** A Tabela @tab{gsd} dá o tamanho da caixa anotada por GSD.

<!--TAB:gsd|Tamanho do alvo por GSD: mediana do lado maior da caixa anotada e fração das instâncias cujo lado menor fica abaixo de um stride do detector (8 pixels), em resolução nativa, na divisão de treino do corpus piloto, nas duas divisões do corpus de referência e na divisão de validação do benchmark.-->

| Corpus | Altitude, GSD (cm/px) | Renderização | Mediana do lado maior | Lado menor abaixo de 8 px |
|---|---|---|---|---|
| Corpus piloto | nadir 150 m, 9,76 | 1920 por 1080 | 10,1 px | 66,9% |
| Corpus de referência | nadir 150 m, 4,88 | 3840 por 2160 | 20,6 px | 0,8% |
| VisDrone-DET val | não registrada | mista, 408 de 548 a 1360 por 765 | 25,0 px | 30,5% |

Reduzir a GSD à metade, de 9,76 para 4,88 cm por pixel, levou a mediana do lado maior de 10,1 para 20,6 pixels e a fração de instâncias abaixo de um stride no lado menor de 66,9 para 0,8%, contra 30,5% no benchmark. Em área, a instância sintética mediana a 4,88 cm por pixel cobria 301 pixels quadrados e a instância mediana do benchmark, divisões de treino e validação agrupadas, 300, uma razão de 1,00; no lado maior as duas diferiam, 20,6 contra 24,0 pixels nas divisões agrupadas e 25,0 na divisão de validação. A 2,44 cm por pixel (75 m) a instância mediana media 47,6 por 41,7 pixels, 6,4 vezes a área a 4,88 em todas as classes e 5,2 vezes para figuras armadas; a 1,14 (35 m) media 121,8 por 103,1 pixels. Esses tamanhos são em resolução nativa, antes do redimensionamento da Seção 4.5.

**Forma.** A Tabela @tab{forma} dá a razão altura-largura dos mesmos conjuntos de anotação, e a Tabela @tab{pitch} divide o corpus S-oblique pela inclinação da câmera registrada por imagem.

<!--TAB:forma|Forma aparente do alvo: dimensões medianas da caixa e razão altura-largura por corpus e geometria de câmera, a partir dos rótulos de quadro inteiro. As linhas nadir trazem a configuração do gerador (dentro de 3,5 graus da vertical); as linhas oblíquas registram a inclinação da câmera por imagem; o benchmark não registra a geometria de aquisição.-->

| Corpus e geometria | Altitude, GSD (cm/px) | Largura mediana | Altura mediana | Mediana a/l | Instâncias |
|---|---|---|---|---|---|
| Corpus piloto, nadir | 150 m, 9,76 | 8,3 px | 8,2 px | **0,98** | 565 |
| Corpus de referência, nadir | 150 m, 4,88 | 17,6 px | 17,5 px | **0,98** | 3.225 |
| S-oblique, inclinação da câmera de 26 a 52 graus, um assentamento | 120 m, 3,90 nominal | 17,9 px | 26,4 px | **1,46** | 1.912 |
| S-oblique-six, inclinação da câmera de 45 a 56 graus, seis assentamentos, figuras que não carregam nada | 120 m, 3,90 nominal | 13,3 px | 25,2 px | **1,85** | 1.521 |
| VisDrone-DET train, aquisição real | não registrada | 13,0 px | 24,0 px | **1,95** | 106.396 |
| VisDrone-DET val, aquisição real | não registrada | 12,0 px | 25,0 px | **2,20** | 13.969 |

<!--TAB:pitch|Razão altura-largura da caixa anotada por inclinação da câmera no corpus S-oblique (120 m, 3,90 cm por pixel nominal), a partir dos rótulos de quadro inteiro.-->

| Inclinação da câmera registrada por imagem | Instâncias | Mediana a/l, todas as figuras | Mediana a/l, figuras que não carregam nada |
|---|---|---|---|
| 26 a 30 graus | 482 | 1,28 | 1,35 |
| 30 a 35 graus | 512 | 1,41 | 1,50 |
| 35 a 40 graus | 231 | 1,49 | 1,58 |
| 40 a 45 graus | 359 | 1,64 | 1,82 |
| 45 a 50 graus | 222 | 1,64 | 1,78 |
| 50 a 52 graus | 106 | 1,70 | 1,97 |

Os dois corpora nadir, que diferem por um fator de 2 em resolução de renderização e de 6 em contagem de instâncias, concordaram na razão até a segunda casa decimal, contra 1,95 e 2,20 nas duas divisões do benchmark. No corpus oblíquo a razão subiu com a inclinação da câmera de 1,28 para 1,70, não estritamente entre 40 e 50 graus, e para figuras que não carregam nada alcançou o 1,95 da divisão de treino do benchmark apenas entre 50 e 52 graus, onde mediu 1,97 em 49 figuras. S-oblique, tal como renderizado, realizou 1,46 em vez do 1,95 para o qual foi calibrado, com suas figuras armadas medindo 1,38 contra 1,58 para figuras que não carregam nada; S-oblique-six realizou 1,85 a 13,3 por 25,2 pixels.

**Contraste.** A Tabela @tab{contraste} dá o contraste figura-fundo por regime de iluminação.

<!--TAB:contraste|Contraste figura-fundo por regime de iluminação no corpus piloto (nadir, 150 m, 9,76 cm por pixel): luminância média do quadro, diferença bruta de luminância em números digitais (DN), contraste em relação ao clutter local agregado por quadro, e sua dispersão entre quadros (desvio padrão, DP); 684 instâncias em 48 quadros, 8 por regime.-->

| Regime | Luminância média do quadro | Diferença bruta (DN) | Contraste sobre o clutter, mediana por quadro | DP entre quadros | Instâncias |
|---|---|---|---|---|---|
| Sol duro | 87,0 | 15,2 | **0,64** | 0,14 | 113 |
| Sol baixo | 56,0 | 9,0 | 0,70 | 0,20 | 117 |
| Nublado | 84,6 | **16,4** | **0,88** | 0,26 | 122 |
| Névoa | 94,4 | 9,6 | 0,79 | 0,25 | 113 |
| Encoberto | 55,6 | 11,2 | 0,72 | 0,38 | 91 |
| Chuva | 35,1 | 6,6 | **0,63** | 0,12 | 128 |

O nublado deu tanto a maior diferença bruta quanto o maior contraste sobre o clutter; sol duro e chuva foram os dois mais baixos neste último, e o sol duro chegou a isso enquanto ficava em segundo lugar no contraste bruto. Com 8 quadros por regime e uma dispersão entre quadros de 0,12 a 0,38, apenas a distância entre os extremos, chuva e sol duro a 0,63 e 0,64 contra nublado a 0,88, aproximou-se de um desvio padrão; a ordenação dos quatro regimes intermediários não era resolvível neste tamanho de amostra. A Figura @fig{fig7_armados} mostra o que o detector recebe nas três GSDs do Experimento C.

<!--FIG:06-resultados/figuras/fig7_armados.jpg|Figuras carregando um fuzil, uma pistola, nada, uma vassoura, um pedaço de cano ou um guarda-chuva fechado a 1,14; 2,44 e 4,88 cm por pixel (35, 75 e 150 m). Cada uma é recortada de um quadro renderizado do corpus de 35 m, de seus gêmeos ou de seus quadros independentes e redimensionada ao mesmo tamanho sem suavização, de modo que cada recorte mostra os pixels que o detector recebe. As figuras que carregam algo foram escolhidas a olho, sob luz clara, como aquelas cujo item fica na mão próximo da horizontal; em muitos quadros o item aponta acentuadamente para baixo ou não fica na empunhadura (Seção 4.2.2).-->

**Similaridade de recortes.** Sob o protocolo da Seção 4.4, as matrizes de cossimilaridade das três classes foram planas em todas as GSDs (Figura @fig{fig13_similaridade}, Tabela @tab{similaridade}). Após a centralização, toda entrada ficou entre -0,030 e +0,032 (entre 0,71 e 0,79 antes da centralização); a maior entrada foi 0,025; 0,026; 0,032 e 0,020 a 35 m, no gêmeo a 75 m, no gêmeo a 150 m e no corpus original de 75 m, e a silhueta das três classes foi 0,002; 0,007; 0,002 e 0,006. A única estrutura presente opunha a classe desarmada às duas classes que carregam algo. As maiores entradas negativas ficaram no par desarmado-contra-objeto em todas as GSDs (-0,017 a -0,030), e os cossenos dos centroides foram -0,75; -0,85; -0,86 e -0,69 para esse par contra +0,15; -0,03; -0,55 e +0,13 para armado contra objeto. A silhueta da classe armada foi negativa em todas as quatro GSDs.

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:similaridade|Separação das três classes no espaço de características genérico congelado por GSD (Seção 4.4). Colunas: caixa anotada mediana no conjunto de avaliação; classificação por centroide mais próximo sob validação cruzada de 5 dobras, com o d′ do detector na divisão de seleção do corpus entre parênteses (a 4,88 cm por pixel, o do primeiro modelo a 150 m, que falhou em sua condição de validade; Seção 5.4) e intervalos de 95% por reamostragem de quadros; todo d′ desta tabela é sem a correção log-linear da Seção 4.7, como a Seção 4.4 especifica, e com ela os valores do detector a 1,14 e 2,44 cm por pixel são 0,77 e 0,89 em vez de 0,78 e 0,90 (Tabela @tab{armado}); AUC de armado contra objeto; acurácia após PCA para 2 e 10 dimensões e após LDA para 2 dimensões. Acaso: 0,33 para acurácia, 0,50 para AUC.-->

| Corpus (GSD, cm/px) | Recortes: armado / desarmado / objeto | Caixa mediana (px) | Acurácia, 3 classes | Objeto chamado de armado (intervalo de 95%) | Revocação de armado | d′ (detector), sem correção | AUC armado vs objeto (intervalo de 95%) | Acurácia, PCA 2 / PCA 10 / LDA 2 |
|---|---|---|---|---|---|---|---|---|
| S-nadir-35 (1,14) | 483 / 434 / 413 | 124 por 105 | 0,507 | 0,332 (0,285 a 0,375) | 0,420 | 0,23 (0,78; 0,77 corrigido) | 0,525 (0,483 a 0,561) | 0,384 / 0,495 / 0,547 |
| Gêmeo a 75 m (2,44) | 342 / 384 / 379 | 48 por 41 | 0,531 | 0,253 (0,207 a 0,297) | 0,377 | 0,35 (0,90; 0,89 corrigido) | 0,576 (0,531 a 0,622) | 0,399 / 0,525 / 0,586 |
| Gêmeo a 150 m (4,88) | 92 / 104 / 101 | 21 por 20 | 0,492 | 0,208 (0,131 a 0,287) | 0,359 | 0,45 (0,67) | 0,654 (0,574 a 0,730) | 0,428 / 0,471 / 0,502 |
| S-nadir-75, original (2,44) | 117 / 153 / 135 | 45 por 41 | 0,558 | 0,267 (0,187 a 0,360) | 0,436 | 0,46 (0,83) | 0,534 (0,459 a 0,615) | 0,348 / 0,526 / 0,514 |

</div>

A AUC de armado contra objeto foi mais alta nas GSDs mais grosseiras nas estimativas pontuais, com intervalos que se sobrepõem entre GSDs vizinhas, e com o valor mais alto, a 4,88 cm por pixel, apoiado em 92 contra 101 recortes com o intervalo mais largo. Uma regra de centroide mais próximo chamou de armado 0,208 a 0,332 dos objetos e reconheceu 0,359 a 0,436 das figuras armadas, um d′ de 0,23 a 0,46 contra 0,67 a 0,90 para o detector nas divisões de seleção (sendo o 0,67 a 4,88 cm por pixel o do primeiro modelo a 150 m, que falhou em sua condição de validade), ambos calculados sem a correção log-linear, como na Seção 4.4; com a correção os valores do detector a 1,14 e 2,44 cm por pixel são 0,77 e 0,89 em vez de 0,78 e 0,90 (Tabela @tab{armado}). A regra dos 5 vizinhos mais próximos, os dois mapas de características mais rasos (AUC de 0,485 a 0,572 sob a regra de centroide mais próximo) e dobras sorteadas por quadro deram o mesmo retrato. Ajustada na divisão de treino e aplicada aos próprios conjuntos do detector, a regra chamou de armado 0,331 (0,254 a 0,408) dos objetos na divisão de seleção de 35 m contra 0,273 do detector, e 0,288 (0,237 a 0,343) nos quadros independentes de 35 m contra 0,253. No gêmeo chamou 0,231 (0,151 a 0,316) na divisão de seleção contra 0,165 e 0,292 (0,234 a 0,351) nos quadros independentes contra 0,125, com revocação de armado de 0,39 a 0,50 nos quatro conjuntos contra 0,43 a 0,57 do detector. Dois componentes principais retiveram 0,18 a 0,20 da variância e reduziram a acurácia para 0,348 a 0,428; 10 componentes retiveram 0,50 a 0,55 e igualaram o espaço completo; a projeção de Fisher deu a maior acurácia sem detector, 0,502 a 0,586, com um d′ de 0,18 a 0,53. O suplemento com o backbone de cada detector treinado, que não é independente de modelo, deu AUC de 0,547; 0,502; 0,574 e 0,494.

<!--FIG:06-resultados/figuras/fig13_similaridade.png|Similaridade de recortes sem detector a 1,14; 2,44 e 4,88 cm por pixel (35 m, o gêmeo a 75 m, o gêmeo a 150 m). Acima: o conjunto de avaliação de cada corpus em seus dois primeiros componentes principais (18 a 20% da variância), centroides de classe como marcadores grandes, silhueta das três classes impressa. Abaixo: similaridade de cosseno média par a par das características centralizadas entre e dentro das classes, escala comum de -0,04 a +0,04.-->

### 5.2 Experimento A: transferência zero-shot para imagens reais

Treinado apenas com imagens sintéticas, o detector recuperou no benchmark urbano, como médias de três execuções de treino, 2,2% do teto na geometria nadir da aquisição de referência, 8,8% quando o mesmo assentamento foi renderizado obliquamente e 15,3% para a melhor configuração oblíqua; no benchmark nadir a ordem das duas geometrias se inverteu.

**Piloto.** O piloto do protocolo, uma execução exploratória com 40 quadros de treino a 9,76 cm por pixel com a receita anterior da Seção 4.5, falhou em seu próprio domínio (Tabela @tab{piloto}): 0,077 em sua própria divisão de validação, uma média de duas classes que não está na escala de classe única das linhas seguintes, contra 0,7915 para o corpus de referência.

<!--TAB:piloto|O piloto do protocolo: um modelo de duas classes treinado em 40 quadros renderizados a 1920 por 1080 (9,76 cm por pixel), pontuado em sua própria divisão de validação e zero-shot (sem treino no domínio real) no benchmark.-->

| Execução piloto | Conjunto de avaliação | Precisão | Revocação | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| Modelo piloto (nadir, 150 m), 40 quadros de treino a 1080p | divisão de validação sintética | 0,109 | 0,148 | 0,077 | 0,019 |
| mesmo modelo | VisDrone-DET val, zero-shot | 0,038 | 0,031 | 0,0055 | 0,0020 |

**Teto.** R alcançou mAP50 de 0,6311 no conjunto de teste (Tabela @tab{teto}); seu checkpoint foi selecionado nessa mesma divisão (Seção 4.5), na época 58 de 60, sem parada antecipada. Uma execução na divisão de treino completa foi iniciada e interrompida antes de concluir.

<!--TAB:teto|O teto: R, treinado em 1.106 imagens reais de VisDrone-DET train, em VisDrone-DET val, com o intervalo de 95% por reamostragem de imagens. Precisão e revocação na confiança que maximiza o F1.-->

| Modelo | Precisão | Revocação | mAP50 (intervalo de 95%) | mAP50-95 |
|---|---|---|---|---|
| R (1.106 imagens reais de treino; checkpoint selecionado na divisão de teste) | 0,7312 | 0,5729 | 0,6311 (0,6149 a 0,6471) | 0,2538 |

**Nadir.** S-nadir-150 pontuou 0,7915 em sua própria divisão de validação (sua divisão de seleção, Seção 4.5) e 0,0102 no benchmark com sua primeira semente de treino (Tabela @tab{nadir}), uma eficácia de 1,6% (1,4 a 2,1). Suas duas sementes adicionais pontuaram 0,0198 e 0,0108 (0,794 e 0,810 na divisão de validação), uma média em três execuções de 0,0136 (0,0120 a 0,0160) e uma eficácia de 2,2% (1,9 a 2,5), 3,1% para a melhor execução.

<!--TAB:nadir|S-nadir-150 (nadir, 150 m, 4,88 cm por pixel), primeira semente de treino, em sua própria divisão de validação e zero-shot no conjunto de teste real, com o intervalo de 95% por reamostragem de imagens.-->

| Conjunto de avaliação | Precisão | Revocação | mAP50 (intervalo de 95%) | mAP50-95 |
|---|---|---|---|---|
| Divisão de validação sintética (teto do corpus) | 0,8707 | 0,7413 | 0,7915 | 0,3656 |
| VisDrone-DET val, zero-shot | 0,0856 | 0,0421 | 0,0102 (0,0087 a 0,0133) | 0,0025 |

Na verificação com escala pareada (Seção 4.6), a mediana do lado maior das caixas de pessoa do benchmark chegou à rede com 25,33 pixels no tamanho de entrada do protocolo, de 1.280, e com 20,27 pixels a 1.024, o mais próximo que um múltiplo de 32 chega dos 20,55 do corpus de referência, enquanto a área mediana caiu de 283 para 181 pixels quadrados. A 1.024 pixels a primeira execução de S-nadir-150 pontuou 0,0128 e R 0,5849, uma eficácia de 2,2 em vez de 1,6%; a diferença, 0,0026 sobre 0,0102, é um quarto do número do protocolo, contra a metade fixada de antemão.

**Variedade de assentamentos.** Distribuir os mesmos 180 quadros por seis assentamentos elevou a pontuação no benchmark de 0,0102 para 0,0190 e reduziu a pontuação na própria divisão de validação do modelo (Tabela @tab{variedade}). Em relação à primeira execução nadir, a diferença pareada foi de +0,0088 (+0,0038 a +0,0102), uma razão de 1,866 (1,308 a 2,071) e uma diferença relativa de 86,6% do menor valor. Em relação à média das três execuções nadir foi de +0,0054 (+0,0009 a +0,0066), uma razão de 1,40 (1,07 a 1,50) e 39,9%, e o valor de seis assentamentos, de uma execução, ficou dentro da faixa das três execuções nadir (0,0102 a 0,0198).

<!--TAB:variedade|Um assentamento contra seis com 180 quadros fixos, nadir a 150 m (4,88 cm por pixel), na divisão de validação sintética e no conjunto de teste real.-->

| Modelo | mAP50 na validação sintética | mAP50 em VisDrone-DET val (intervalo de 95%) | mAP50-95 | Eficácia (intervalo de 95%) |
|---|---|---|---|---|
| S-nadir-150, um assentamento | 0,7915 | 0,0102 (0,0087 a 0,0133) | 0,0025 | 1,6% (1,4 a 2,1) |
| S-nadir-150-six, seis assentamentos | 0,6786 | 0,0190 (0,0142 a 0,0211) | 0,0071 | 3,0% (2,3 a 3,3) |

**Oblíquo.** Com todas as configurações da verificação de geometria da Seção 4.6 mantidas e a câmera levada a uma inclinação de 26 a 52 graus, a pontuação no benchmark subiu de 0,0102 para 0,0614 na primeira semente de treino de cada modelo (Tabela @tab{obliquo}), uma diferença pareada de +0,0511 (+0,0447 a +0,0567) e uma razão de 6,011 (4,571 a 7,011). As duas sementes adicionais de S-oblique pontuaram 0,0552 e 0,0501 (0,764 e 0,736 em sua divisão de validação), uma média de 0,0555 (0,0502 a 0,0614) e uma eficácia de 8,8% (8,1 a 9,6). Nas médias de três execuções por lado a diferença pareada foi de +0,0419 (+0,0368 a +0,0470), uma razão de 4,08 (3,44 a 4,64) e uma diferença relativa de 307,9%, e as faixas dos dois modelos, 0,0501 a 0,0614 e 0,0102 a 0,0198, não se sobrepuseram; para as sementes 1 e 2 isoladamente a razão foi de 2,79 e 4,64. Na mesma comparação a razão altura-largura mediana passou de 0,98 para 1,46 e a área mediana de 301 para 456 pixels quadrados, com a GSD oblíqua no centro do quadro entre cerca de 4,3 e 6,3 cm por pixel ao longo da faixa de inclinação da câmera. S-oblique-six, que mudou em conjunto os assentamentos, a faixa de inclinação da câmera, as figuras e o posicionamento da câmera, pontuou 0,1055 em sua primeira execução (precisão 0,2631, revocação 0,1716, mAP50-95 0,0329; 0,7047 em sua própria divisão de validação), 0,0958 e 0,0887 em duas sementes de treino adicionais, uma média de 0,0966 e uma eficácia de 15,3% nas três execuções. Em relação a S-oblique a diferença pareada foi de +0,0441 (+0,0383 a +0,0514) entre primeiras execuções e, nas médias de três execuções por lado, +0,0411 (+0,0367 a +0,0462), uma razão de 1,74 (1,64 a 1,85) e 74,0%, com faixas que não se sobrepuseram. Sob a regra do toolkit oficial para regiões ignoradas (Seção 4.7) todo mAP50 deste experimento subiu ligeiramente, R para 0,6548 e a primeira execução de S-oblique-six para 0,1074, toda eficácia caiu ligeiramente, a de S-oblique-six de 16,7 para 16,4%, e nenhuma comparação entre esses modelos, incluídas as sementes adicionais, mudou de ordem a IoU 0,50; 0,60 ou 0,75.

**Semente de assentamento.** Renderizado com as sementes de assentamento 22 e 23 em vez de 21 e treinado com a semente 0, S-oblique-six pontuou 0,0935 e 0,0821 contra 0,1055 (Tabela @tab{obliquo}), uma média de 0,0937 (0,0868 a 0,1019) e uma eficácia de 14,8%. A faixa sobre sementes de assentamento, de 0,0234 de largura, foi 1,4 vez a faixa sobre sementes de treino (0,0887 a 0,1055, 0,0168 de largura), abaixo do fator de 2 fixado de antemão (Seção 4.6) como sinal de que a cena domina a dispersão. Nas três sementes de assentamento seis assentamentos permaneceram acima de um assentamento em suas três sementes de treino por +0,0381 (+0,0334 a +0,0437), 68,7%, com faixas que não se sobrepuseram.

<!--TAB:obliquo|Aquisição nadir contra oblíqua no conjunto de teste real, cada modelo para cada uma de suas três sementes de treino e como média das três, S-oblique-six também para duas sementes de assentamento adicionais (semente de treino 0), com intervalos de 95% por reamostragem de imagens.-->

| Modelo | mAP50 em VisDrone-DET val (intervalo de 95%) | Eficácia (intervalo de 95%) |
|---|---|---|
| S-nadir-150 (4,88 cm/px), semente 0 | 0,0102 (0,0087 a 0,0133) | 1,6% (1,4 a 2,1) |
| S-nadir-150, semente 1 | 0,0198 (0,0172 a 0,0232) | 3,1% (2,7 a 3,7) |
| S-nadir-150, semente 2 | 0,0108 (0,0090 a 0,0128) | 1,7% (1,4 a 2,0) |
| S-nadir-150, média de 3 sementes | 0,0136 (0,0120 a 0,0160) | 2,2% (1,9 a 2,5) |
| S-oblique (3,90 cm/px nominal), semente 0 | 0,0614 (0,0554 a 0,0673) | 9,7% (8,9 a 10,6) |
| S-oblique, semente 1 | 0,0552 (0,0493 a 0,0607) | 8,7% (7,9 a 9,6) |
| S-oblique, semente 2 | 0,0501 (0,0448 a 0,0569) | 7,9% (7,1 a 8,9) |
| S-oblique, média de 3 sementes | 0,0555 (0,0502 a 0,0614) | 8,8% (8,1 a 9,6) |
| S-oblique-six, semente 0 (semente de assentamento 21) | 0,1055 (0,0980 a 0,1148) | 16,7% (15,7 a 18,1) |
| S-oblique-six, semente 1 | 0,0958 (0,0884 a 0,1048) | 15,2% (14,1 a 16,5) |
| S-oblique-six, semente 2 | 0,0887 (0,0813 a 0,0968) | 14,1% (13,1 a 15,2) |
| S-oblique-six, média de 3 sementes | 0,0966 (0,0896 a 0,1048) | 15,3% (14,4 a 16,5) |
| S-oblique-six, semente de assentamento 22 | 0,0935 (0,0866 a 0,1023) | 14,8% (13,8 a 16,1) |
| S-oblique-six, semente de assentamento 23 | 0,0821 (0,0746 a 0,0901) | 13,0% (11,9 a 14,1) |
| S-oblique-six, média de 3 sementes de assentamento | 0,0937 (0,0868 a 0,1019) | 14,8% (13,9 a 16,0) |

**Precisão e revocação.** A Figura @fig{fig11_pr_visdrone} traça as curvas de precisão-revocação de R, da primeira execução de S-oblique-six e dos dois modelos de ajuste fino a 10% (Seção 5.3), e a Tabela @tab{pr} dá seus pontos de operação. As três curvas com dados de treino reais mantiveram a mesma ordem em toda a faixa de revocação; a curva zero-shot caiu abaixo de uma precisão de 0,6 a 1% de revocação e terminou em uma revocação de 0,39.

<!--FIG:06-resultados/figuras/fig11_pr_visdrone.png|Curvas de precisão-revocação a IoU 0,50 em VisDrone-DET val (548 imagens, classes pedestrian e people fundidas) para R, S-oblique-six (semente 0, zero-shot), F-generic e F-synthetic a 10%, a partir do envelope de precisão do validador em 1.000 pontos de revocação. O marcador em cada curva é a confiança que maximiza o F1.-->

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:pr|Pontos de operação em VisDrone-DET val para os quatro modelos da figura de precisão-revocação: confiança, precisão, revocação e F1 no máximo de F1 (suavizado como faz o validador), e precisão e revocação na confiança de predição padrão de 0,25.-->

| Modelo | Confiança no F1 máximo | Precisão | Revocação | F1 | Precisão a 0,25 | Revocação a 0,25 |
|---|---|---|---|---|---|---|
| R | 0,2963 | 0,7312 | 0,5729 | 0,6424 | 0,6731 | 0,6036 |
| F-generic 10% | 0,3193 | 0,6823 | 0,5160 | 0,5876 | 0,5698 | 0,5757 |
| F-synthetic 10% | 0,2983 | 0,6372 | 0,4579 | 0,5328 | 0,5535 | 0,4986 |
| S-oblique-six, semente 0 | 0,2152 | 0,2631 | 0,1716 | 0,2077 | 0,2804 | 0,1625 |

</div>

**Número de quadros.** Treinado em subconjuntos aninhados de seus quadros de treino (152 quadros de treino de seus 180), S-oblique-six subiu no benchmark de 0,0618 com 30 quadros para 0,0966 com 152 (Tabela @tab{curva}). A diferença de +0,0349 (+0,0310 a +0,0392), 56,5%, passou nas três leituras, sem sobreposição das faixas em três sementes. Entre 120 e 152 quadros foi de +0,0062 (+0,0033 a +0,0088), 6,9%, o que passou apenas na leitura por intervalo, com as faixas se sobrepondo. Um ajuste de mAP50 sobre o logaritmo do número de quadros nas cinco médias deu um ganho de 0,0140 por duplicação.

<!--TAB:curva|Curva de aprendizado de S-oblique-six sobre o número de quadros de treino: subconjuntos aninhados estratificados por assentamento, os mesmos ladrilhos de validação, 60 épocas, mAP50 zero-shot em VisDrone-DET val por semente de treino, com a média sobre sementes, seu intervalo de 95% por reamostragem de imagens e a eficácia da média. Médias e diferenças são calculadas antes do arredondamento.-->

| Quadros de treino (ladrilhos) | mAP50 por semente de treino | Média (intervalo de 95%) | Faixa | Eficácia da média |
|---|---|---|---|---|
| 30 (182) | 0,0499; 0,0674; 0,0679 | 0,0618 (0,0566 a 0,0679) | 0,0499 a 0,0679 | 9,8% |
| 60 (341) | 0,0806 | 0,0806 (0,0739 a 0,0885) | uma execução | 12,8% |
| 90 (503) | 0,0810 | 0,0810 (0,0745 a 0,0886) | uma execução | 12,8% |
| 120 (696) | 0,0915; 0,0878; 0,0918 | 0,0904 (0,0838 a 0,0986) | 0,0878 a 0,0918 | 14,3% |
| 152 (890), o corpus completo | 0,1055; 0,0958; 0,0887 | 0,0966 (0,0896 a 0,1048) | 0,0887 a 0,1055 | 15,3% |

**Benchmark nadir.** No HERIDAL, no tamanho de entrada pareado de 1.152 pixels (Seção 4.6), R pontuou 0,3185 (0,2843 a 0,3543), acima do 0,05 fixado como limite de interpretabilidade. A ordem das duas geometrias se inverteu em relação ao benchmark urbano (Tabela @tab{heridal}). S-nadir-150 alcançou 0,1997 na média de suas três execuções, 62,7% de R, e S-oblique 0,1341, 42,1%. A diferença, -0,0656 (-0,0840 a -0,0471), uma razão de 0,671 (0,61 a 0,74) contra 4,08 no benchmark urbano, passou nas leituras por intervalo e relativa e não na leitura por semente: as execuções nadir se espalharam de 0,0926 a 0,2672 e se sobrepuseram às execuções oblíquas, 0,1092 a 0,1476. Com seis assentamentos o modelo nadir, de uma execução, alcançou 0,2488, 78,1% de R, contra 0,1477 para S-oblique-six em três execuções, uma diferença de -0,1012 (-0,1216 a -0,0786) que passou nas leituras por intervalo e relativa. No tamanho do protocolo de 1.280 pixels a ordem foi a mesma, -0,0260 (-0,0414 a -0,0097) entre os braços de assentamento único, o que passou apenas na leitura por intervalo.

<!--TAB:heridal|Detecção zero-shot de pessoas no benchmark nadir, HERIDAL (1.647 imagens, 3.229 pessoas, nadir de 40 a 65 m), no tamanho de entrada pareado de 1.152 pixels e no tamanho do protocolo de 1.280: mAP50 com o intervalo de 95% por reamostragem de imagens, na média das execuções de treino onde um modelo foi treinado três vezes, a faixa sobre essas execuções e a fração de R, que foi treinado no benchmark urbano.-->

| Modelo | Execuções | mAP50 a 1.152 (intervalo de 95%) | Faixa sobre execuções | Fração de R | mAP50 a 1.280 |
|---|---|---|---|---|---|
| R (1.106 imagens reais de VisDrone-DET train) | 1 | 0,3185 (0,2843 a 0,3543) | uma execução | 100% | 0,3353 |
| S-nadir-150 | 3 | 0,1997 (0,1713 a 0,2306) | 0,0926 a 0,2672 | 62,7% | 0,1682 |
| S-nadir-150-six | 1 | 0,2488 (0,2116 a 0,2865) | uma execução | 78,1% | 0,2208 |
| S-oblique | 3 | 0,1341 (0,1149 a 0,1555) | 0,1092 a 0,1476 | 42,1% | 0,1422 |
| S-oblique-six | 3 | 0,1477 (0,1265 a 0,1715) | 0,1079 a 0,1847 | 46,4% | 0,1418 |

### 5.3 Experimento B: pré-treino sintético e treino conjunto contra um início genérico

Dada a fatia de 5 ou 10% de imagens reais, o modelo que partiu dos pesos sintéticos terminou abaixo do início genérico em ambos os volumes, sob o cronograma original e sob cada um de três outros, e o mesmo ocorreu com o modelo treinado com imagens sintéticas e reais em conjunto (Tabela @tab{ajuste}, Figura @fig{fig10_ajuste_fino}).

<!--TAB:ajuste|Ajuste fino em 5 e 10% da divisão de treino do benchmark a partir do modelo sintético e a partir de pesos genéricos, e treino conjunto a partir de pesos genéricos nas mesmas imagens reais com os 890 ladrilhos sintéticos: mAP50 em VisDrone-DET val com intervalos de 95% por reamostragem de imagens, por semente de treino onde repetido.-->

| Dados de treino reais, semente | F-synthetic (a partir de S-oblique-six) | F-generic (a partir de COCO) | F-joint |
|---|---|---|---|
| 5% (324 imagens), semente 0 | 0,4424 (0,4260 a 0,4587) | 0,5220 (0,5045 a 0,5403) | 0,4607 (0,4444 a 0,4789) |
| 5%, semente 1 | 0,4608 (0,4441 a 0,4784) | 0,5228 (0,5056 a 0,5410) | treinado uma vez |
| 5%, semente 2 | 0,4554 (0,4400 a 0,4721) | 0,5285 (0,5114 a 0,5474) | treinado uma vez |
| 10% (647 imagens), semente 0 | 0,5095 (0,4935 a 0,5264) | 0,5709 (0,5535 a 0,5883) | 0,5428 (0,5259 a 0,5610) |

<!--FIG:06-resultados/figuras/fig10_ajuste_fino.png|mAP50 em VisDrone-DET val contra o número de imagens reais de treino para as três maneiras de usar o corpus sintético uma vez que existam imagens reais: como pesos iniciais (início sintético), misturado ao conjunto de treino (conjunto) ou de modo algum (início genérico). Marcadores cheios: a primeira execução de treino; marcadores vazados: as duas execuções adicionais onde existem. Linha tracejada: R, treinado em 1.106 imagens reais por duas vezes mais épocas.-->

A 5% o início genérico terminou acima do início sintético por +0,0796 (+0,0721 a +0,0873); +0,0620 (+0,0548 a +0,0706) e +0,0731 (+0,0654 a +0,0810) nas três sementes, +0,0716 (+0,0658 a +0,0780) nas médias, uma razão de 1,158 (1,144 a 1,173) e uma diferença relativa de 15,8%. A execução genérica mais baixa ficou acima da sintética mais alta. A 10% a diferença foi de +0,0614 (+0,0553 a +0,0679), uma razão de 1,121 (1,108 a 1,134) e 12,1%. O sinal foi o mesmo em mAP50-95, a métrica de seleção (Seção 4.7): -0,0368 para o início sintético a 5% e -0,0232 a 10. Os melhores pesos de todo modelo ajustado e conjunto sob o cronograma original caíram nas épocas 27 a 30 de suas 30. O início sintético com 647 imagens reais (0,5095) não alcançou o início genérico com 324 (0,5220), e a expectativa fixada antes da execução (Seção 4.6), de que a diferença seria maior no volume menor, falhou no sinal: a diferença foi mais negativa ali e estreitou-se à medida que os dados reais cresceram. O ajuste fino de fato moveu o próprio modelo sintético, de 0,1055 para 0,4424 com 324 imagens reais.

Os modelos conjuntos terminaram 0,0637 (0,0562 a 0,0700) abaixo do início genérico na média de suas três sementes a 5% (razão 1,138; 1,121 a 1,154; 13,8%) e 0,0281 (0,0214 a 0,0346) abaixo a 10% (razão 1,052; 1,039 a 1,064; 5,2%). Ambas as margens excederam o dobro do desvio padrão das três execuções genéricas a 5% (um desvio padrão de 0,0035), a margem fixada de antemão e emprestada a 10%. Em relação ao início sintético o modelo conjunto pontuou +0,0078 (+0,0025 a +0,0147) mais alto na média das sementes sintéticas a 5% (1,7%), com o intervalo cruzando zero em relação a duas das três sementes sintéticas e o valor conjunto caindo dentro de sua faixa. A 10% pontuou +0,0333 (+0,0276 a +0,0399) mais alto (6,5%), acima do início sintético a IoU 0,50 e 0,60 e abaixo dele a 0,75 (0,0983 contra 0,1025). Na fatia de seleção o início sintético liderou nas três primeiras épocas a 5% e foi ultrapassado na quarta; a 10% o início genérico liderou desde a primeira época; depois disso o início sintético liderou apenas de forma intermitente, e a vantagem do início genérico não se estreitou entre a época 20 e a época 30.

**Cronograma de ajuste fino.** Com o otimizador definido explicitamente, a execução de controle reproduziu exatamente o modelo genérico a 5%, 0,5220 contra 0,5220 (tolerância 0,0035, Seção 4.6), de modo que as novas células são comparáveis aos modelos existentes. A Tabela @tab{cronograma} dá as doze células. Congelar o backbone, reduzir a taxa de aprendizado ou ambos reduziu o início sintético em todas as células, para entre 0,2028 e 0,3875, enquanto a taxa de aprendizado menor elevou o início genérico em ambos os volumes. Na fatia de seleção o início sintético preferiu o cronograma original em ambos os volumes e o início genérico a taxa de aprendizado de 0,0002; suas duas sementes adicionais a 5% pontuaram 0,5963 e 0,5982. Com cada início no cronograma que preferiu, o início genérico terminou acima do sintético por +0,1369 (+0,1290 a +0,1465) a 5%, 0,5897 contra 0,4529 nas médias de três sementes, uma razão de 1,302 (1,279 a 1,331) e 30,2%, com faixas que não se sobrepuseram; a 10% por +0,1129 (+0,1044 a +0,1230), 0,6224 contra 0,5095, uma razão de 1,222 (1,202 a 1,245) e 22,2%, de uma execução por lado. Sob cada um dos quatro cronogramas, em ambos os volumes, o início genérico ficou acima do sintético com um intervalo que exclui zero, e nenhuma das ordenações mudou a IoU 0,60 ou 0,75. Os modelos conjuntos não foram treinados sob os novos cronogramas (Seção 4.6).

<!--TAB:cronograma|Ajuste fino sob quatro cronogramas, por fatia de dados reais e início: mAP50 do modelo ajustado em VisDrone-DET val, o conjunto de teste (primeira semente de treino), e, entre parênteses, o mAP50-95 de seu melhor checkpoint na fatia de seleção, na qual o cronograma de cada início foi escolhido; a célula escolhida está em negrito. Os cronogramas são os da grade da Seção 4.6: o original treina a rede inteira a uma taxa de aprendizado de 0,002, os outros congelam o backbone, reduzem a taxa para 0,0002, ou ambos, com o mesmo orçamento de 30 épocas.-->

| Fatia, início | Original | Backbone congelado | Taxa de aprendizado 0,0002 | Ambos |
|---|---|---|---|---|
| 5%, sintético | **0,4424 (0,1480)** | 0,2808 (0,0901) | 0,3103 (0,1019) | 0,2028 (0,0585) |
| 5%, genérico | 0,5220 (0,1802) | 0,5467 (0,1886) | **0,5746 (0,2230)** | 0,5410 (0,1915) |
| 10%, sintético | **0,5095 (0,1743)** | 0,3209 (0,1053) | 0,3875 (0,1258) | 0,2241 (0,0681) |
| 10%, genérico | 0,5709 (0,1951) | 0,5772 (0,2030) | **0,6224 (0,2451)** | 0,5644 (0,2001) |

### 5.4 Experimento C: a distinção entre armado e desarmado por GSD

A 2,44 e 1,14 cm por pixel os detectores de três classes chamaram de armado entre 0,165 e 0,273 dos objetos confundíveis em suas divisões de seleção, e reduzir a GSD à metade, de 2,44 para 1,14 cm por pixel, não reduziu essa taxa em corpora pareados (0,253 contra 0,125 em quadros independentes); a 4,88 cm por pixel permaneceu uma separação acima do acaso, mais fraca do que a 2,44 nos mesmos quadros independentes, onde a taxa de objeto foi 0,245, de modo que a taxa foi mais baixa na GSD intermediária.

**4,88 cm por pixel.** O gêmeo a 150 m, onde a caixa anotada mediana de sua divisão de seleção mede 21 por 20 pixels, primeiro encontrou 148 de 297 figuras anotadas (0,498) em sua divisão de seleção, abaixo da metade fixada antes de sua execução. Treinado de novo por mais tempo (Seção 4.6; parou na época 80), encontrou 0,606 das 297 figuras em qualquer classe em sua divisão de seleção e 0,663 de 916 em seus 80 quadros independentes, e passou na condição. Na divisão de seleção chamou de armado 0,435 das figuras armadas e 0,178 (0,107 a 0,247) dos objetos confundíveis, um d′ de 0,75 (0,33 a 1,26), com um mAP50 de três classes de 0,388. Nos quadros independentes (Tabela @tab{gsd150}) chamou de armado 0,457 das figuras armadas, 0,245 (0,204 a 0,289) dos objetos confundíveis e 0,205 das pessoas desarmadas, um d′ contra objetos de 0,58 (0,38 a 0,78), cujo intervalo exclui zero. Nos mesmos índices de quadro o d′ foi 0,97 para o gêmeo a 75 m e 0,77 para o modelo de 35 m. Em relação ao gêmeo a 75 m, o d′ a 150 m foi mais baixo por 0,394 (-0,681 a -0,098) e a taxa de objeto mais alta por 0,120 (+0,058 a +0,181), ambos passando nas leituras por intervalo e relativa. Figuras carregando a pistola de 0,20 m foram chamadas de armadas a 0,50 (17 de 34), dentro da faixa das armas longas (0,41 a 0,50).

<!--TAB:gsd150|Os modelos de três classes a 1,14; 2,44 e 4,88 cm por pixel nos 80 quadros independentes de cada corpus, que compartilham seus índices de quadro: fração de figuras anotadas encontradas em qualquer classe, as taxas em que cada classe é chamada de armada na confiança 0,25, e d′ contra objetos confundíveis (correção log-linear), a partir da primeira execução de treino de cada modelo, sendo o modelo a 150 m o treinado por mais tempo. O intervalo a 150 m é por 1.000 reamostragens de quadros; os intervalos das duas GSDs mais finas estão na Tabela @tab{gemeo}.-->

| Modelo (GSD, cm/px) | Figuras encontradas | Armado chamado de armado | Objeto chamado de armado | Desarmado chamado de armado | d′ vs objeto |
|---|---|---|---|---|---|
| S-nadir-35 (1,14) | 0,684 | 0,543 | 0,253 | 0,156 | 0,77 |
| Gêmeo a 75 m (2,44) | 0,766 | 0,432 | 0,125 | 0,140 | 0,97 |
| Gêmeo a 150 m (4,88) | 0,663 | 0,457 | 0,245 (0,204 a 0,289) | 0,205 | 0,58 (0,38 a 0,78) |

**2,44 e 1,14 cm por pixel, divisão de seleção.** A Tabela @tab{armado} dá os três modelos em suas divisões de seleção (contagens de instâncias na Tabela @tab{corpora}).

<!--TAB:armado|A distinção entre armado e desarmado na divisão de seleção de cada corpus de três classes (27, 35 e 24 quadros), sob o protocolo da Seção 4.7, na confiança 0,25, com intervalos de 95% por reamostragem de quadros. d′ com a correção log-linear; sem ela os valores contra objetos são 0,83; 0,78 e 0,90 e contra pessoas desarmadas 1,24; 1,14 e 1,16. O mAP50 de três classes é em quadros inteiros.-->

| Grandeza | S-nadir-75 (75 m, 2,44 cm/px) | S-nadir-35 (35 m, 1,14 cm/px) | Gêmeo de S-nadir-35 a 75 m (2,44 cm/px) |
|---|---|---|---|
| mAP50, três classes | 0,579 | 0,514 | 0,508 |
| Revocação, armado | 0,547 (0,476 a 0,627) | 0,569 (0,492 a 0,646) | 0,471 (0,397 a 0,558) |
| Precisão, armado | 0,386 | 0,415 | 0,440 |
| Objeto confundível chamado de armado | 0,237 (0,183 a 0,289) | 0,273 (0,202 a 0,353) | 0,165 (0,100 a 0,230) |
| Pessoa desarmada que não carrega nada chamada de armada | 0,131 (0,073 a 0,188) | 0,168 (0,101 a 0,235) | 0,109 (0,044 a 0,174) |
| d′ contra objetos confundíveis | 0,83 (0,54 a 1,13) | 0,77 (0,46 a 1,10) | 0,89 (0,58 a 1,32) |
| d′ contra pessoas desarmadas | 1,23 | 1,12 | 1,14 |

**Quadros independentes a 2,44 cm por pixel.** Nos 50 quadros independentes do teste de arma não vista (Seção 4.3), S-nadir-75 chamou de armado 0,434 (0,381 a 0,496) das figuras armadas, 0,152 (0,113 a 0,196) dos objetos confundíveis e 0,068 (0,035 a 0,102) das pessoas desarmadas. Sua precisão para armado foi 0,430 e seu d′ contra objetos 0,85 (0,64 a 1,09). Todas as taxas foram mais baixas do que na divisão de seleção. A revocação foi 0,400 nas cinco armas de fogo de treino (50 de 125) e 0,466 nas duas não vistas (61 de 131), uma razão de 1,16 (intervalo aproximado de 95% de 0,88 a 1,54) contra o limiar de 0,80 (Seção 4.6). O grupo visto inclui a pistola, 20 de suas 125 instâncias, e com a pistola posta de lado a razão permaneceu acima do limiar. Por modelo, de 15 a 69 instâncias cada e sem intervalos, o fuzil não visto de 1,10 m foi chamado de armado a 0,50, dentro da faixa das armas longas vistas (0,34 a 0,52), a submetralhadora não vista de 0,55 m a 0,43 e a pistola a 0,20. Entre os objetos, o guarda-chuva fechado, de 0,88 m de comprimento, foi chamado de armado a 0,38 (29 instâncias), as vassouras a 0,10 (41) e os pedaços de cano a 0,11 (28). Na nova renderização com objetos portados como armas, pareada caixa a caixa em 49 de 50 quadros, S-nadir-75 chamou de armado 0,154 dos 227 objetos pareados quando portados normalmente e 0,137 quando portados nas poses das armas e em seus ângulos (teste exato de McNemar, p = 0,56), e o guarda-chuva, cujo porte não mudou, permaneceu em 0,38.

**35 m contra seu gêmeo a 75 m.** A Tabela @tab{gemeo} dá os dois modelos pareados em suas divisões de seleção e nos 80 quadros independentes de cada corpus, em três sementes de treino e em três limiares de IoU.

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:gemeo|S-nadir-35 contra seu gêmeo a 75 m, com todas as demais configurações mantidas. Taxas em que cada classe é chamada de armada na confiança 0,25 nas divisões de seleção (35 e 24 quadros) e nos 80 quadros independentes de cada corpus, com diferenças, intervalos de 95% por reamostragem de quadros independentemente em cada lado e p de um teste de duas proporções. As linhas seguintes dão faixas e médias em três sementes de treino, a taxa de objeto em limiares de IoU mais estritos e d′ (correção log-linear) com intervalos por reamostragem de quadros.-->

| Grandeza | S-nadir-35 (1,14 cm/px) | Gêmeo a 75 m (2,44 cm/px) | Diferença (intervalo de 95%) |
|---|---|---|---|
| Objeto confundível chamado de armado, divisão de seleção | 0,273 | 0,165 | +0,108 (+0,015 a +0,211), p = 0,06 |
| Objeto confundível chamado de armado, 80 quadros independentes | 0,253 (74 de 292) | 0,125 (36 de 288) | +0,128 (+0,071 a +0,194), p = 0,0001 |
| Pessoa armada chamada de armada, divisão de seleção | 0,569 | 0,471 | +0,099 (-0,022 a +0,217), p = 0,15 |
| Pessoa armada chamada de armada, 80 quadros independentes | 0,543 | 0,432 | +0,112 (+0,031 a +0,192) |
| Pessoa desarmada chamada de armada, divisão de seleção | 0,168 | 0,109 | +0,059 (-0,038 a +0,154), p = 0,22 |
| Pessoa desarmada chamada de armada, 80 quadros independentes | 0,156 | 0,140 | +0,015 (-0,040 a +0,073) |
| d′ contra objetos confundíveis, divisão de seleção | 0,77 (0,46 a 1,10) | 0,89 (0,58 a 1,32) | |
| d′ contra objetos confundíveis, 80 quadros independentes | 0,77 (0,57 a 0,99) | 0,97 (0,77 a 1,20) | |
| Taxa de objeto em três sementes de treino, divisão de seleção (faixa; média) | 0,231 a 0,273; 0,248 | 0,132 a 0,242; 0,179 | faixas se sobrepõem; +0,068 (+0,002 a +0,142), 38,1% |
| Taxa de objeto em três sementes de treino, 80 quadros independentes (faixa; média) | 0,202 a 0,253; 0,222 | 0,097 a 0,181; 0,134 | faixas separadas; +0,087 (+0,044 a +0,136), 64,9% |
| Taxa de objeto, divisão de seleção, a IoU 0,60 e 0,75 | 0,223 e 0,132 | 0,165 e 0,132 | niveladas a 0,75 |

</div>

Semente a semente, a diferença na taxa de objeto excluiu zero nas sementes 0 e 1 e não na semente 2 em ambos os conjuntos; a revocação de armado do modelo de 35 m excedeu a do gêmeo nos quadros independentes nas sementes 0 e 1 e ficou abaixo dela na semente 2, e a taxa de desarmado não diferiu em nenhuma semente. Nas médias das três sementes a diferença para armado foi de +0,072 (-0,023 a +0,163) nas divisões de seleção e +0,050 (-0,017 a +0,111) nos quadros independentes, e a diferença para desarmado +0,004 (-0,053 a +0,062) e -0,018 (-0,063 a +0,031), com todos os intervalos cruzando zero. Em relação ao modelo original de 75 m, a taxa de objeto do modelo de 35 m na divisão de seleção diferiu por +0,036 (-0,059 a +0,124) a IoU 0,50 e ficou abaixo dela a 0,60 e 0,75, onde o modelo original chamou de armado 0,230 e 0,141 dos objetos; a taxa de desarmado fez o mesmo a 0,75 (0,076 contra 0,085). Entre o corpus original de 75 m e o gêmeo, que mudou as poses de porte e as demais configurações da Seção 4.6 na mesma GSD, a taxa de objeto passou de 0,237 para 0,165 (p = 0,19).

**Varredura de limiar.** A Figura @fig{fig12_limiar_armado} varre o limiar de confiança dos sete modelos de três classes em ambos os conjuntos, e a Tabela @tab{limiar} dá os três pontos de operação da Seção 4.7 para a primeira execução de cada modelo.

<!--FIG:06-resultados/figuras/fig12_limiar_armado.png|Revocação de armado contra a taxa de objeto à medida que o limiar de confiança vai de 0,95 (canto inferior esquerdo) a 0,05 (canto superior direito), para S-nadir-75, S-nadir-35 e o gêmeo a 75 m. Esquerda: divisão de seleção de cada corpus. Direita: quadros independentes (80 a 35 m e a 75 m; os 50 quadros de arma não vista para S-nadir-75). Marcadores cheios: confiança 0,25, semente 0; marcadores vazados: confiança 0,25, sementes 1 e 2 (curvas tracejadas e pontilhadas).-->

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:limiar|Os três pontos de operação da Seção 4.7 (confiança padrão 0,25, F1 máximo de armado, taxa de objeto igual ou inferior a 0,10) para cada modelo de três classes (semente 0) em sua divisão de seleção e em seus quadros independentes; d′ contra objetos confundíveis, correção log-linear.-->

| Modelo | Conjunto (quadros) | Ponto de operação | Limiar | Revocação de armado | Objeto chamado de armado | Precisão de armado | d′ vs objeto |
|---|---|---|---|---|---|---|---|
| S-nadir-75 | seleção (27) | padrão | 0,25 | 0,547 | 0,237 | 0,386 | 0,83 |
| S-nadir-75 | seleção (27) | F1 máximo de armado | 0,40 | 0,564 | 0,200 | 0,516 | 0,99 |
| S-nadir-75 | seleção (27) | taxa de objeto 0,10 | 0,70 | 0,333 | 0,096 | 0,661 | 0,86 |
| S-nadir-75 | independentes (50) | padrão | 0,25 | 0,434 | 0,152 | 0,430 | 0,85 |
| S-nadir-75 | independentes (50) | F1 máximo de armado | 0,45 | 0,391 | 0,126 | 0,578 | 0,86 |
| S-nadir-75 | independentes (50) | taxa de objeto 0,10 | 0,55 | 0,340 | 0,100 | 0,669 | 0,86 |
| S-nadir-35 | seleção (35) | padrão | 0,25 | 0,569 | 0,273 | 0,415 | 0,77 |
| S-nadir-35 | seleção (35) | F1 máximo de armado | 0,30 | 0,555 | 0,256 | 0,469 | 0,79 |
| S-nadir-35 | seleção (35) | taxa de objeto 0,10 | 0,60 | 0,285 | 0,099 | 0,722 | 0,70 |
| S-nadir-35 | independentes (80) | padrão | 0,25 | 0,543 | 0,253 | 0,408 | 0,77 |
| S-nadir-35 | independentes (80) | F1 máximo de armado | 0,35 | 0,497 | 0,226 | 0,484 | 0,74 |
| S-nadir-35 | independentes (80) | taxa de objeto 0,10 | 0,65 | 0,211 | 0,099 | 0,603 | 0,48 |
| Gêmeo a 75 m | seleção (24) | padrão | 0,25 | 0,471 | 0,165 | 0,440 | 0,89 |
| Gêmeo a 75 m | seleção (24) | F1 máximo de armado | 0,40 | 0,423 | 0,154 | 0,522 | 0,81 |
| Gêmeo a 75 m | seleção (24) | taxa de objeto 0,10 | 0,55 | 0,341 | 0,099 | 0,630 | 0,86 |
| Gêmeo a 75 m | independentes (80) | padrão | 0,25 | 0,432 | 0,125 | 0,370 | 0,97 |
| Gêmeo a 75 m | independentes (80) | F1 máximo de armado | 0,40 | 0,381 | 0,090 | 0,480 | 1,03 |
| Gêmeo a 75 m | independentes (80) | taxa de objeto 0,10 | 0,40 | 0,381 | 0,090 | 0,480 | 1,03 |

</div>

Nas 14 combinações de modelo, semente e conjunto, o limiar que maximizou o F1 da classe armada ficou entre 0,30 e 0,50 (0,40 em 7 delas) e elevou a precisão de armado de 0,37 a 0,46 no padrão para 0,47 a 0,66, ao custo de 1 a 8 pontos de revocação de armado em 13 delas e com um ganho de 2 em S-nadir-75 em sua divisão de seleção. Levar a taxa de objeto a 0,10 exigiu um limiar de 0,55 a 0,70 para S-nadir-35 e S-nadir-75, onde a revocação de armado ficou então entre 0,21 e 0,36; o gêmeo alcançou 0,10 em limiares entre 0,25 e 0,65. Em nenhum limiar algum modelo excedeu uma revocação de armado de 0,65, e a uma taxa de objeto de 0,10 ou menos a maior revocação de armado foi 0,42, para o gêmeo a 75 m em sua terceira semente de treino nos quadros independentes (precisão de armado 0,61), e 0,38 ou menos em todas as outras combinações. Nos quadros independentes a curva do modelo de 35 m correu à direita da do gêmeo, a uma taxa de objeto mais alta para a mesma revocação de armado.

### 5.5 Experimento D: desempenho por regime de iluminação

Medido em quadros sintéticos, o sol duro foi o mais fraco dos seis regimes para S-nadir-150 em ambas as medidas, e o nublado o mais forte em mAP50, nivelado com o sol baixo (Tabela @tab{regimes}, Figura @fig{fig4_dataset}); um modelo treinado apenas sob sol duro não ficou resolvivelmente abaixo do modelo de todos os regimes sob nublado em revocação.

<!--TAB:regimes|Desempenho por regime nos 120 quadros independentes do corpus de referência (nadir, 150 m, 4,88 cm por pixel), 20 por regime: mAP50 nos ladrilhos de cada regime e revocação na confiança 0,25 em quadros inteiros, para S-nadir-150, treinado em todos os seis regimes, com intervalos de 95% por reamostragem de quadros, e para o modelo treinado apenas sob sol duro.-->

| Regime | mAP50, todos os regimes | Revocação a 0,25, todos os regimes | Intervalo de 95% | mAP50, só sol duro | Revocação a 0,25, só sol duro |
|---|---|---|---|---|---|
| Sol duro | 0,675 | 0,657 | 0,591 a 0,720 | 0,742 | 0,739 |
| Encoberto | 0,755 | 0,768 | 0,714 a 0,816 | 0,754 | 0,749 |
| Chuva | 0,759 | 0,789 | 0,748 a 0,827 | 0,728 | 0,747 |
| Névoa | 0,780 | 0,726 | 0,697 a 0,757 | 0,652 | 0,569 |
| Sol baixo | 0,790 | 0,814 | 0,768 a 0,854 | 0,794 | 0,776 |
| Nublado | 0,791 | 0,796 | 0,760 a 0,827 | 0,796 | 0,759 |

<!--FIG:06-resultados/figuras/fig4_dataset.jpg|Um quadro anotado do corpus piloto (nadir, 150 m, 1920 por 1080, 9,76 cm por pixel) de cada um dos seis regimes de iluminação, com as caixas geradas desenhadas: verde para a classe armada, azul para a classe desarmada. A rotulagem não depende do regime (Seção 4.2.5).-->

Nas estimativas pontuais, sem intervalos, o sol duro pontuou 8 pontos de mAP50 abaixo do regime seguinte; em revocação, que traz um intervalo, seu intervalo ficou inteiramente abaixo dos de nublado, chuva e sol baixo, enquanto se sobrepunha aos de névoa e encoberto. O nublado pontuou acima tanto do sol duro quanto da chuva em ambas as medidas, e a margem do nublado sobre a chuva ficou dentro dos intervalos de revocação. O sol baixo, que também projeta sombras nítidas, pontuou nivelado com o nublado em mAP50 (0,790 contra 0,791) e mais alto em revocação. A ordenação por detecção, medida no corpus de referência a 4,88 cm por pixel, coincidiu com a ordenação por contraste sobre o clutter da Seção 5.1, medida no corpus piloto a 9,76 cm por pixel, nos dois extremos, nublado e sol duro, e não entre os regimes intermediários.

**Ablação só com sol duro.** Treinado em 180 quadros apenas sob sol duro, o modelo especialista pontuou 0,7422 de mAP50 e 0,739 de revocação sob sol duro. Nos mesmos 20 quadros de sol duro sua revocação excedeu a do modelo de todos os regimes por +0,0818 (+0,0377 a +0,1243). Em relação ao modelo de todos os regimes sob nublado, a comparação fixada como decisiva, sua revocação sob sol duro diferiu por -0,0572 (-0,1252 a +0,0067), um intervalo que inclui zero; seu mAP50 sob sol duro permaneceu abaixo do 0,7906 daquele modelo sob nublado, por 6,5%. Sob os outros cinco regimes o especialista ficou abaixo do modelo de todos os regimes em revocação, mais sob névoa (0,569 contra 0,726), enquanto seu mAP50 ficou nivelado sob encoberto e mais alto sob sol baixo e nublado. Zero-shot no benchmark urbano, como leitura exploratória, pontuou 0,0072 contra 0,0102 para a primeira execução de S-nadir-150.

### 5.6 Verificações de robustez e resumo das hipóteses

Toda verificação fixada de antemão foi executada, incluídas as da última etapa da Seção 4.6; a Tabela @tab{hipoteses} registra cada desfecho contra seu critério, com as três leituras de resolvibilidade da Seção 4.7 para cada comparação principal. Tanto sob o validador quanto sob a regra do toolkit oficial, nenhum par entre os fixados para a verificação de IoU mudou de ordem entre 0,50; 0,60 e 0,75 no benchmark, incluídos os pares da última etapa (a comparação de geometria em três sementes por lado, 152 contra 30 quadros, as sementes de assentamento contra S-oblique e os inícios de ajuste fino em seus cronogramas escolhidos); as duas comparações que de fato se inverteram são relatadas nos três limiares nas Seções 5.3 e 5.4.

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:hipoteses|Cada hipótese e verificação pré-especificada contra seu critério, com seu status (Seção 4.6) e as leituras da Seção 4.7 em que sua diferença principal passa: (a) faixas de sementes, (b) intervalo pareado, (c) 30%; n.a. onde um lado foi treinado uma vez ou nenhuma diferença está em questão.-->

| Hipótese ou verificação | Critério pré-especificado | Status | Dados | Desfecho | Resolvível (a / b / c) |
|---|---|---|---|---|---|
| Teto R válido | R não próximo do acaso | confirmatória | reais; R selecionado na divisão de teste | sustentada: 0,6311 | n.a. |
| O treino só com sintético recupera uma fração do teto | razão em relação a R; a escala é um fator de confusão se o número com escala pareada diferir por mais da metade | confirmatória | reais | sustentada: 2,2% em 3 sementes (1,6% na semente 0); a verificação de escala diferiu por um quarto | n.a. |
| Geometria determinante: S-oblique acima de S-nadir-150 | braço oblíquo supera braço nadir; última etapa: leituras da Seção 4.7 em 3 sementes por lado | confirmatória | reais | sustentada: +0,0419 em 3 sementes por lado, razão 4,08 (só semente 0: +0,0511, razão 6,011) | sim / sim / sim, 307,9% |
| Vantagem oblíqua diminui ou se inverte em um benchmark nadir | R não abaixo de 0,05; S-oblique contra S-nadir-150 no tamanho de entrada pareado, leituras da Seção 4.7; dependente de escala se a ordem diferir a 1.280 | confirmatória | reais, nadir | sustentada, invertida: -0,0656, razão 0,671; R 0,3185; mesma ordem a 1.280 | não, faixas se sobrepõem / sim / sim, 48,9% |
| Seis assentamentos contra um, nadir | nenhum; última etapa: leituras da Seção 4.7 | exploratória, critério fixado | reais | observado: +0,0054 em 3 sementes nadir (+0,0088 na semente 0) | valor de seis assentamentos dentro da faixa de 3 sementes / sim / sim, 39,9% |
| Seis assentamentos contra um, oblíquo | nenhum; última etapa: leituras da Seção 4.7 em 3 sementes por lado | exploratória, critério fixado | reais | observado: +0,0411 em 3 sementes por lado | sim / sim / sim, 74,0% |
| Seis assentamentos acima de um entre sementes de assentamento | leituras da Seção 4.7; a cena domina se sua faixa exceder o dobro da faixa de treino | confirmatória | reais | sustentada: +0,0381; faixa da cena 1,4 vez a faixa de treino | sim / sim / sim, 68,7% |
| Número de quadros operante: 152 contra 30 | 152 acima de 30 em (a) e (b) | confirmatória | reais | sustentada: +0,0349 | sim / sim / sim, 56,5% |
| Fim da curva: 152 contra 120 | crescente se (a) e (b); plana se nenhuma; crescente dentro da dispersão de treino se apenas (b) | confirmatória | reais | crescente dentro da dispersão de treino: +0,0062; 0,0140 por duplicação | não, faixas se sobrepõem / sim / não, 6,9% |
| Iluminação: nublado acima de sol duro e chuva; sol duro entre os 2 mais fracos | como enunciado | confirmatória | sintéticos independentes | sustentada nas estimativas pontuais; a margem do nublado sobre a chuva fica dentro dos intervalos de revocação | n.a. |
| O déficit sob sol duro pertence ao regime | especialista sob sol duro abaixo do modelo de todos os regimes sob nublado, intervalo D-ii inteiramente abaixo de zero | confirmatória | sintéticos independentes | intervalo D-ii inclui zero: -0,0572 (-0,1252 a +0,0067); condição não atendida | n.a. / não / não, 6,5% em mAP50 |
| O pré-treino sintético acrescenta acurácia, mais a 5% | expectativa fixada antes da execução | exploratória, critério fixado | reais | não sustentada: -0,0716 a 5%, -0,0614 a 10% | 5%: sim / sim / não, 15,8%; 10%: n.a. / sim / não, 12,1% |
| Custo do início sintético robusto ao cronograma | F-generic resolvivelmente acima de F-synthetic em ambos os volumes, cada um no cronograma escolhido na fatia de seleção; controle reproduzido dentro de 0,0035 | confirmatória | reais | sustentada: +0,1369 a 5%, +0,1129 a 10%; controle 0,5220 contra 0,5220 | 5%: sim / sim / sim, 30,2%; 10%: n.a. / sim / não, 22,2% |
| O treino conjunto acrescenta acurácia | margem do dobro do DP das 3 execuções genéricas (DP 0,0035) | exploratória, critério fixado | reais | não sustentada: -0,0637 e -0,0281, além da margem | 5%: conjunto fora da faixa genérica / sim / não, 13,8%; 10%: n.a. / sim / não, 5,2% |
| Treino conjunto contra o início sintético | nenhum | exploratória | reais | observado: +0,0078 a 5%, +0,0333 a 10% | 5%: conjunto dentro da faixa sintética / sim na média, não em 2 de 3 sementes / não, 1,7%; 10%: n.a. / sim / não, 6,5% |
| Revocação de arma de fogo não vista a 75 m contra revocação de arma de fogo vista | número de 75 m retirado se a razão cair abaixo de 0,80 | confirmatória | sintéticos independentes | condição de retirada não atendida: razão 1,16 | n.a. |
| Objetos portados como armas são chamados de armados com mais frequência | taxa pareada sobe (teste exato de McNemar); ressalva sobre o porte retirada se não subir | confirmatória | sintéticos independentes | taxa pareada não subiu: 0,154 contra 0,137, p = 0,56; condição de retirada da ressalva atendida | n.a. |
| Validade do modelo de três classes a 4,88 cm por pixel | pelo menos metade das figuras anotadas encontradas, na divisão de seleção e em 80 quadros independentes | confirmatória | divisão de seleção sintética e quadros independentes | primeiro modelo não interpretável: 0,498; treinado por mais tempo, sustentada: 0,606 e 0,663 | n.a. |
| Separação a 4,88 cm por pixel | intervalo de d′ inclui zero: ausência medida; exclui zero: separação acima do acaso, lida como atalho | confirmatória | sintéticos independentes | intervalo exclui zero: d′ 0,58 (0,38 a 0,78); lido como atalho pela regra da Seção 4.6 | n.a. / sim, exclui zero / n.a. |
| 4,88 contra 2,44 cm por pixel, quadros independentes pareados | leituras (b) e (c) | confirmatória | sintéticos independentes | d′ mais baixo por 0,394, taxa de objeto mais alta por 0,120 | n.a. / sim / sim, 68,0% e 96,2% |
| A taxa de objeto difere entre 1,14 e 2,44 cm por pixel, tudo o mais mantido | taxa de 35 m acima da do gêmeo em quadros independentes com p abaixo de 0,05; retirada se invertida | exploratória, critério fixado | sintéticos independentes; divisão de seleção | sustentada: +0,128, p = 0,0001; +0,087 nas médias de sementes (divisão de seleção: +0,108; +0,068 nas médias de sementes) | independentes: sim / sim / sim, 64,9%; seleção: não, faixas se sobrepõem / sim / sim, 38,1% |
| As taxas de armado e desarmado diferem entre o modelo de 35 m e seu gêmeo | nenhum | exploratória | sintéticos, ambas as divisões | não resolvível: intervalos das médias de sementes cruzam zero em ambos os conjuntos; a diferença para armado nos quadros independentes se inverte na semente 2 | não / não / n.a. |
| Modelo de 35 m contra o modelo original de 75 m | ordenação se mantém a IoU 0,50; 0,60 e 0,75 | exploratória | divisão de seleção sintética | não resolvível: +0,036 (-0,059 a +0,124); ordem se inverte a 0,60 | n.a. / não / não, 15,1% |

</div>
