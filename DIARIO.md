# DIÁRIO DE BORDO

## 2026-11-07 [MAC] Segunda rodada de verificação: revisão de prova no inglês e cópia pt-BR alinhada

- Dois agentes sobre o Elsevier já validado: um revisor de prova (inglês) e um comparador pt-BR contra o inglês. Nenhum número errado; só redação e termos.
- Inglês (10 trocas, nenhum número novo): 4.7 explica as três taxas que são cota inferior e a quarta grandeza (precisão da classe armada); "armed recall and the rate for each other class give d′"; "a steeper pitch band"; 5.4 cita 0.67 a 0.90 "for the detectors of the same four corpora on their selection splits"; subconjuntos aninhados "as means of three seeds"; precisão 0.37 a 0.46 "at the default threshold (Section 5.4)"; d′ 0.58 "compared with 0.97 for the twin at 75 m"; resumo "with overlapping run ranges" na inversão da HERIDAL; espaço na legenda da Tabela 2; "matched box for box" removido onde já estava dito.
- Português: as mesmas 10 trocas espelhadas, mais 5 frases reescritas (5.1 com ponto e vírgula; 5.4 pose de porte; 6.4 "ficou aquém"; 7 "em coerência com a forma aparente"; célula da Tabela 3 "distinção entre armado e desarmado por GSD") e termos unificados em todo o texto: a GSD sempre feminina, "classificado como armado" (era "chamado de armado", 12 ocorrências), "a confiança 0.25", "aninhados", "avaliados" (era "pontuados"), "benchmark nadir" e "em nadir", "revocação de armados" na Figura 5.
- Rebuild completo (reune_cont antes de gera_elsevier): Elsevier 18 páginas, Carta 44, pt-BR 20; artifact v16.

## 2026-11-07 [MAC] Validação: 760 números conferidos, nenhum errado; ajustes de texto, Tabelas 9 a 11 renumeradas

- Quatro agentes verificadores (1 a 4; 5.1 a 5.3; 5.4 e 5.5; consistência interna) contra `06-resultados/`: nenhum valor divergente; achados só de apresentação e qualificadores, aplicados no inglês e espelhados no pt-BR (lista no STATUS). Único número novo: 8,6 (9,76/1,14) no lugar de 8,5 na 6.2.
- Tabelas renumeradas pela ordem de citação (antigas 10, 11, 9 viram 9, 10, 11) e blocos postos em ordem física crescente; `pagina.py` com `ordem_ok` (rejeita movimento que inverte tabelas ou figuras) e cortes de parágrafo com pelo menos seis palavras de cada lado (a Carta tinha um parágrafo "withdrawn." de uma palavra).
- Lição: `gera_elsevier.py` deve ler o fonte depois de `reune_cont.py`; um build saiu com 19 páginas por usar o fonte com os cortes da Carta. Com as referências em entrelinha 1,15 o Elsevier fecha em 18 páginas (última a 100 pt do pé).
- Artifact v15 com Elsevier, Carta e pt-BR.

## 2026-11-07 [MAC] Seis inconsistências dos pareceres corrigidas; extended abstract deixa de ser mantido

- Corrigido no inglês e na cópia pt-BR (script `corrige_0711h.py` no scratchpad, sem número novo): 6.2 passa a 9,76 cm por pixel (9,71 era o valor pelo FOV do manual da DJI, `gsd_zoom.md`); 4.2.2 explica que 1,15 m vale pelo comprimento registrado e a malha da espingarda chega a 1,17; "about one in five" vira "one in five to one in four" (0,192 a 0,245); 5.4 ganha a frase sobre a pistola a 0,50 como pista que não é a arma (pose fixa por arma); 4.7 enumera os dez modelos com três sementes (S-nadir-150, S-oblique, S-oblique-six e subconjuntos de 30 e 120 quadros, F-synthetic e F-generic a 5 por cento, F-generic com taxa menor, S-nadir-35 e gêmeo a 75 m); `<title>` sem "skeleton".
- Autor: o extended abstract não é mais atualizado (as duas trocas que já tinham entrado nele hoje ficam).
- Elsevier 18 páginas (Figura 2 no topo da 8), Carta 44, pt-BR 20. Artifact v14. Quatro agentes verificadores lançados (números das seções 1 a 4, 5.1 a 5.3, 5.4 a 5.5, consistência interna da 6 e 7).

## 2026-11-07 [MAC] Coautor Toledo, Figura 2 abrindo página, cópia em português e três pareceres frios

- Felipe I. M. Toledo (COPPE/UFRJ) entrou como coautor nos dois fontes, com afiliação própria (¹ FGV EBAPE, ² COPPE/UFRJ); `gera_elsevier.py` passou a aceitar mais de uma linha de afiliação. O `[[DECIDE]]` que restava no extended abstract saiu.
- A Figura 2 confundia o leitor no meio da página 8 (duas filas de colunas). Agora é bloco `full topo` com `break-before: page`; `pagina.py` ganhou `encaixa_topo`, que testa posições até cinco parágrafos à frente da citação, com e sem corte do parágrafo seguinte, e fica com a de menos branco em volta (a primeira tentativa, só avançar e cortar, deixou a página 7 só com a figura porque a Tabela 3 flutuante não coube depois dela). Elsevier 18 páginas, cheias.
- Cópia de leitura em português: cinco agentes traduziram blocos do fonte com tags e números conferidos automaticamente contra o inglês; `versao-curta-elsevier.ptbr.html` tem 20 páginas. Referências em inglês. Vale o inglês em caso de dúvida.
- Três agentes avaliaram o artigo (revisor da trilha, metodologista, gestão pública): aceite estimado 45 a 65 por cento; falhas comuns: contribuição para gestão num parágrafo (6.4), RQ3 apoiada em modelos treinados uma vez, teto R fraco, resumo de 398 palavras; inconsistências conferidas (9,71 contra 9,76; 1,15 m contra 1,17; "one in five" para 0,245). Lista completa no STATUS.
- Artifact privado v13 com os quatro PDFs. Scripts de apoio no scratchpad do Mac (`prep_0711e.py`, `monta_ptbr.py`, `reune_cont.py`).

## 2026-11-07 [DESKTOP] Rodada 6 caiu com o reinício do app e foi pausada

- A cadeia, o supervisor e o treino T1 (`armado_35_e120_sd1`, época 7 de 120) pararam às 12:16 sem erro no log: o app do Claude fechou e reabriu (processos do app com início às 13:48; o PC não reiniciou, boot em 21/10). Processo lançado pela sessão morre com o app (memória `cadeia-morre-com-o-app`), e o atalho na pasta Inicializar só cobre reinício do PC. A vigia horária, que era desta sessão, morreu junto; por isso ninguém relançou entre 12:16 e 13:49.
- O autor notou GPU e RAM ociosas às 13:49 e pediu pausa: `fila6/PAUSA` criada (nada a encerrar). O `last.pt` do T1 é da época 6 (12:14); perde-se só a época 7 em curso.
- Para a retomada sobreviver a reinícios do app, o supervisor deve ser aberto pelo autor (duplo clique em `07-blender/scripts/retoma_rodada6.cmd`, que roda no shell do usuário e carrega o MPFB), não pela sessão do Claude.

## 2026-11-07 [DESKTOP] Rodada 6: item 3 fechado (uma semente) e pausa

- Item 3: `s_nadir_4k_deg` e `s_oblvar_deg` (ladrilhos com ruído, borrão e JPEG). Degradado menos limpo: S-oblique-six no VisDrone +0,0070 (+7,3%, b), S-nadir-150 na HERIDAL +0,0192 (+9,6%, b), as outras duas nulas. Os dois ganhos caem dentro da faixa das sementes limpas; a leitura (a) espera T6 a T10.
- Pausa do autor às 11:25, logo depois de o grupo G fechar; a cadeia já tinha começado T1 (`armado_35_e120_sd1`, época 3), que retoma do `last.pt`.

## 2026-11-07 [DESKTOP] Rodada 6: item 6 fechado e R-sel na HERIDAL

- Pausa do autor em 06/11 de 15:38 a 17:54; o treino a 150 m do item 6 retomou do `last.pt` na época 62.
- Item 6 (uma semente): sem o comprimento como pista, a 150 m a separação entre arma e objeto some (d′ 0,117, IC inclui zero): atalho confirmado. A 75 m cai à metade (d′ 0,973 para 0,444, resolvível) e continua acima do acaso. Cruzado: o modelo original chama de armada 37% dos objetos com comprimento de arma a 150 m (24,5% nos seus quadros) e 21% a 75 m (12,5%). Para o texto: "a forma se perde a 4,88 cm/px" passa de leitura a medida.
- Acertos do item 4: R-sel na HERIDAL 0,2927 (R 0,3185; viés +0,0258, IC 0,0113 a 0,0421, 8,8% relativos, contra 1,4% no VisDrone). Eficácias na HERIDAL contra R-sel: S-nadir-150 68,2%, S-nadir-150-six 85,0%, S-oblique 45,8%, S-oblique-six 50,5%; ordem igual.
- A cadeia seguiu às 05:31 para o grupo G (item 3), primeiro treino `s_nadir_4k_deg`.

## 2026-11-05 [DESKTOP] Rodada 6: ordem nova pela criticidade para a AIM

- Pedido do autor, às 21:45: reordenar o que vem depois do L pela criticidade do dado para o artigo da AIM (corte de texto em 15/11), sem interromper o que roda. Ordem nova registrada na seção 8 do plano (commit 6375941): L, R3/R4, G, T1 a T5 e Q5, E, T6 a T14, H, V e C só se couberem antes de 15/11 12:00, Y. Nenhum critério mudou.
- Feito à mão, sem GPU: o critério R com F-joint e cada treino individual contra R-sel (F-joint 74,0%, IC 72,6 a 75,5, e 87,2%, IC 86,0 a 88,3); a figura do ajuste fino com R-sel (rótulo 0.6224; o "0.571" foi deslocado para não encostar na linha do teto). Divergência para o Mac: a melhor semente de S-oblique-six dá 16,9% sem arredondamento (a Tabela 4 diz 17,0%, provavelmente 0,1055 / 0,6224 com os valores já arredondados).
- Cadeia: regra do prazo executada por ela (grupos H, V e C ficam `adiada_periodico` se a previsão passar de 15/11 12:00; `--sem-prazo` a desliga); espera de processo órfão antes de relançar render ou treino; previsão do status com 95% das 120 épocas. A cadeia foi reiniciada às 21:57; o treino de L3 (`armado_75c`, iniciado às 21:49) seguiu vivo e a cadeia nova espera por ele.
- Previsão às 21:56: C terminaria em 15/11 22:30, depois do prazo; H e V cabem.

## 2026-11-05 [DESKTOP] Rodada 6: item 5 fechado (uma semente)

- Pausa do autor de 08:47 a 11:42; o treino do gêmeo de 75 m retomou do `last.pt` na época 77.
- `armado_35_e120` (120 épocas, best na 116) e `armado_75g_e120` (parou na 109, best na 74). Nos 80 quadros novos, objeto chamado de armada: 35 m 0,192, 75 m 0,222, 150 m 0,245 (todos com 120 épocas); nenhuma diferença entre altitudes passa em (b). Com 60 épocas eram 0,222 e 0,134 (média de três sementes). Veredito pela regra: a U era em parte orçamento. O que mais muda é o 75 m: com o dobro de épocas ele chama mais objetos de armada (+0,088, resolvível). A 150 m o d′ continua o mais baixo (0,58), mas só passa em (c) contra 75 m.
- Consequência para o texto (não aplicada, decisão do autor): a 5.4 e a 6.1 não podem mais apresentar a U como efeito da GSD; o que se sustenta é um falso alarme de 19 a 25% nas três altitudes com orçamento igual. As sementes do grupo T podem mudar a leitura.
- A cadeia seguiu às 14:10 para o grupo L (render de `ds_armado_75c`).

## 2026-11-07 [MAC] Versão curta enxugada de 10,3 mil para 9,3 mil palavras; Elsevier volta a 18 páginas

- Pedido do autor: voltar a 9 mil palavras e depois conferir se o PDF Elsevier tem branco para remanejar. Quatro rodadas de corte (`enxuga_0711.py` a `enxuga_0711d.py` no scratchpad do Mac), cada troca de parágrafo com duas garantias automáticas: nenhum número que não existisse no texto anterior e nenhum travessão. Corpo (seções 1 a 7, sem tabelas, figuras, resumo e declarações): 10.329 → 9.723 → 9.550 → 9.381 → 9.326.
- O que saiu: o resumo "um resultado por questão" da abertura da seção 5 (repetia resumo, 6.1 e conclusão); números da 5.2, 5.3 e 5.4 repetidos na 6.1 (a 6.1 agora remete às seções); na 4.6, a lista de critérios pré-fixados foi para junto do resultado que cada um decide (5.4), ficando na 4.6 o que foi fixado antes, a regra trocada, a hipótese do comprimento, a reseleção de R e o que ainda roda; 6.6 virou item (8) da 6.5, renomeada "Limitations and future work" (nenhuma referência órfã: SeaDronesSee e Stanford Drone continuam citados); frases repetidas em 4.1/4.5/4.7/6.5 sobre o teto R; 4.2 diz agora que o controle de comprimento neutraliza a primeira pista (antes: "no test neutralises the first two", que ficou falso com o item 6). Nada de afirmação, intervalo ou referência saiu; `checa.py` continua com 80 referências e os mesmos três avisos de sempre (CNN, DJI, RioOnWatch, citadas como instituição).
- Antes de editar, os 10 parágrafos que o `pagina.py` tinha partido em volta de tabelas (`class="cont"`, inclusive um "RQ1." órfão) foram reunidos por tokens; o `pagina.py` reparte o que precisar a cada geração. Ordem do build passou a ser `gera_elsevier.py` (a partir do fonte sem cortes) e só depois `pagina.py` no fonte Carta.
- Resultado: Elsevier 18 páginas (era 19), Carta 44 (era 46), extended abstract 18 (não mudou). Branco medido por coluna no PDF Elsevier (`branco_elsevier.py`, mesma geometria do `pagina.py`, faixas de 24 pt ou mais): 294 pt somados nas 17 primeiras páginas (p. 8 col. 1 48 pt, p. 14 col. 2 78 pt, o resto abaixo de 40), mais os 74 pt do artefato do título na p. 1; a última página termina a 134 pt do pé. Como o branco total (428 pt) é menor que uma coluna (726 pt), não há como ganhar página remanejando; o PDF está cheio dentro da tolerância do balanceamento de colunas.
- Os 330 que faltam para 9 mil exigem tirar um resultado. O corte limpo é o braço de iluminação (Experimento D na 4.6, 5.5, 6.3 e Tabela 12, uns 370 + a tabela), que é a mesma marca `[[DECIDE]]` pendente no extended abstract; fica para o autor.

## 2026-11-07 [MAC] Versão curta: item 3 (ruído, borrão e JPEG) aplicado

- `git pull`: desktop fechou o item 3 (dc357c2, 11:20) e pausou às 11:25 com T1 em curso.
- Aplicado em `versao-curta-aim2027.html`: 4.6, Experimento A ganha o quarto check (degradação em 3/4 dos ladrilhos de treino, regra de leitura); 4.6, pré-registro: G sai do "still running" e entra no que rodou; 5.2, parágrafo novo com as quatro células (+0,0070, IC +0,0022 a +0,0119, 7,3%; +0,0192, IC +0,0077 a +0,0309, 9,6%; −0,0004 e −0,0000 nulos) e a ressalva de que os ganhos caem dentro da faixa das três sementes limpas; 6.5 (2) passa a "medido: 7 a 10% relativos em duas de quatro células, dentro da dispersão de treino". Extended abstract: frase das limitações. Números de `06-resultados/RESULTADOS.md`, entrada de 07/11 do grupo G.
- Corpo 10.044 → 10.329 palavras.

## 2026-11-07 [MAC] Versão curta: itens 5 e 6 e R-sel na HERIDAL aplicados (veredito da QP3)

- `git pull`: desktop fechou o item 6 e os acertos do item 4 (8acc7ba, 07/11 05:31); cadeia no grupo G.
- Aplicado em `versao-curta-aim2027.html` e `esqueleto-aim2027.html` por `edita_0711.py` (scratchpad), só com números de `06-resultados/RESULTADOS.md` (entradas de 05 e 07/11), `rodada6_eficacias.md` e `rodada6_criterios.json`; células de recall, armada e desarmada das linhas novas lidas dos `extra_*.json` e `confusao_*.json` citados no RESULTADOS.
- Item 6: a hipótese declarada na 4.6 em 04/11 foi testada; a 150 m o d′ sem o comprimento é 0,12 (IC −0,09 a 0,32, inclui zero): atalho de comprimento confirmado; a 75 m 0,44 (0,24 a 0,65), queda −0,53 resolvível; cruzado 0,368 e 0,208. Entrou em resumo, abertura dos Resultados, 4.6 (Experimento C e pré-registro), 5.4 (parágrafo novo), Tabela 9 (seis linhas novas), Tabela 4 (três linhas), 6.1 QP3, 6.4, 6.5 (6) e conclusão.
- Item 5: aplicado junto, porque a 5.4 e a 6.1 do item 6 não se escrevem com a U como efeito da GSD; texto diz "in part an artefact of training budget", 19,2/22,2/24,5, uma semente por controle (sementes T1 a T5 previstas para 08/11 refazem a leitura).
- HERIDAL: teto R-sel 0,2927, viés +0,0258 (8,8% contra 1,4% no VisDrone); 68,2 (59,0 a 78,9), 85,0, 45,8 (40,6 a 52,6), 50,5 (44,6 a 57,3). Resumo, 5.2, Tabelas 4 e 6, 6.1 QP1. Usei 50,5% (RESULTADOS); `rodada6_eficacias.md` imprime 50,4% para 0,5045: arredondamento, apontado ao desktop.
- Corpo 9.298 → 10.044 palavras. Extended abstract ainda tem uma marca `[[DECIDE]]` (Illumination), decisão do autor.

## 2026-11-05 [MAC] Versão curta: restos do item 4 aplicados; item 5 conferido e pendente de decisão

- `git pull`: desktop fechou o item 5 (af6936e) e, a pedido do autor por e-mail, reordenou a cadeia pela criticidade para a AIM (6375941, d8b7945): L, R3/R4, G, T1 a T5 e Q5, E, T6 a T14, H, V e C só se couberem antes de 15/11 12:00. Previsão do desktop: L 07/11 00:49, G 07/11 10:02, Q5 08/11 18:23, E 09/11 16:43, H 13/11, V 14/11; C fica para o periódico.
- Aplicado em `versao-curta-aim2027.html` e `esqueleto-aim2027.html`, só com números de `06-resultados/rodada6_eficacias.md`: Tabela 4, F-joint com intervalos pareados a R-sel (74,0%, 72,6 a 75,5; 87,2%, 86,0 a 88,3); melhor corrida do S-oblique-six 16,9% (o 17,0% vinha de 0,1055/0,6224 com arredondados). Figura 4 (`fig10_ajuste_fino.png`) já regerada pelo desktop com R-sel, referenciada por caminho: entra nos PDFs ao renderizar. HERIDAL continua com R até a etapa R3.
- Item 5 lido: a U (0,253, 0,125, 0,245) era em parte orçamento; com 120 épocas 0,19, 0,22, 0,25, sem diferença resolvível em (b), uma semente. Não aplicado ao texto: afeta resumo, 5.4, 6.1, Tabela 11; aguarda decisão do autor (sementes T1 a T5 previstas para 08/11 podem mudar a leitura).

## 2026-11-04 [MAC] Versão curta: teto R-sel (item 4) aplicado ao texto

- O desktop publicou o item 4 (commit 4d0bbce): R-sel 0,6224 (0,6069 a 0,6397) contra 0,6311, viés +0,0087 (+0,0035 a +0,0136). Aplicado em `versao-curta-aim2027.html` só com números de `06-resultados/rodada6_eficacias.md`: 4.3 (seleção em 265 imagens fora do teste), 4.5 (viés medido no lugar de "direção do viés desconhecida"), 4.6 (R-sel sai do "still running" e entra como acrescentado), 5.2 (0,6224 e viés), 6.5 (5), Tabela 4 (linha de R, eficácias 2,2/3,1/8,9/15,5, melhores 3,2/9,9/17,0; F-synthetic e F-generic a 5% passam a média de 3 sementes, 72,8 e 84,3; 10% primeira semente 81,8 e 91,7; cronograma escolhido 94,8 e 100,0), resumo, intro dos resultados, 6.1 e conclusão (8,9 e 15,5). HERIDAL continua com R, porque R-sel não foi avaliado lá. F-joint na Tabela 4 ficou só com o ponto (74,0 e 87,2, regra ×1,014 do RESULTADOS) porque o desktop não publicou intervalo para `misto05`/`misto10`. Extended abstract com as mesmas trocas.
- Falta pedir ao desktop: intervalos pareados a R-sel para `misto05`, `misto10`; R-sel na HERIDAL; `figuras_mpl.py` regerando `fig10_ajuste_fino.png` com `r_pareado_sel` (a linha tracejada ainda mostra 0,631).
- Páginas: Elsevier 18, Carta 43, extended abstract 17; corpo 9.298 palavras; 0 marcas.

## 2026-11-04 [DESKTOP] Rodada 6: item 4 fechado

- `r_pareado_sel` fez as 60 épocas (best.pt na 55) e o zero-shot deu 0,6224 contra 0,6311 de R. Viés de seleção +0,0087, IC pareado 0,0035 a 0,0136: real e pequeno. Pela regra do plano, R-sel vira o teto do artigo e as eficácias sobem cerca de 1,4% relativos; nenhuma ordem muda. Números e comandos no RESULTADOS; tabela em `06-resultados/rodada6_eficacias.md`. E-mail na thread da rodada.
- P2 e P3 passaram (flags do comprimento e da mão num quadro cada). A cadeia seguiu para o grupo Q às 19:34.
- O manuscrito não foi tocado: a troca de R por R-sel nas eficácias do texto é decisão do autor.

## 2026-11-04 [DESKTOP] Rodada 6: pausa, retomada e grupo C (transferência de cor)

- Pausa pedida pelo autor de 14:38 a 16:11 (`pausa_rodada6.py`); o treino do item 4 retomou do `last.pt` na época 31, sem perda.
- Pedido do autor: grupo C, transferência de cor de Monge-Kantorovich para a estatística do VisDrone train, no molde do G, critério fixado antes, depois do H. Feito: `07-blender/scripts/transfere_cor.py` (fase `estat`, média e covariância RGB de cada imagem do train com grade de passo 4 px, recusa o val; fase `aplica`, mapa T = S_s^-1/2 (S_s^1/2 S_t S_s^1/2)^1/2 S_s^-1/2 em 75% dos ladrilhos de treino, semente 0, JPEG 92 4:4:4, limpos e val intactos, `_transferencia.json`). Conferido numa amostra no scratchpad: T S_s T' = S_t com erro 2e-14, média transferida igual à do alvo, limpos e val idênticos byte a byte, inspeção visual coerente.
- Cadeia: etapas C1 a C13 em `rodada6.py` (estatística, transferência, `s_nadir_4k_ct` e `s_oblvar_ct`, zero-shot a 1280 e 1024, predições VisDrone e HERIDAL, critério, sementes condicionais a (b), braço combinado com `degrada_ladrilhos.py`, critério final); `rodada6_criterios.py --parte C`; `status_rodada6.py`. Seção 3.10 e cronograma no plano (commit 56e4aad), antes de a cadeia carregar o grupo. Desvio declarado: as sementes condicionais ficam no próprio C, porque o T roda antes e a condição depende do resultado de C6.
- A cadeia (em R1, esperando o item 4) foi reiniciada para carregar as etapas; o processo do treino do item 4 sobreviveu. Previsão com C: 226 a 294 h, fim perto de 16/11; prazo da AIM em 19/11.

## 2026-11-04 [MAC] Versão curta: resumo reescrito, regra da QP3 trocada por hipótese testável, pré-registro declarado, gerador sob solicitação direta

- Pedido do autor, no fim da tarde, depois do parecer frio sobre o estado do artigo: reescrever o resumo abrindo com sintético e com menos números; trocar a regra pré-fixada da QP3 ("d′ fora de zero a 150 m = atalho") por uma hipótese que possa falhar; declarar explicitamente o que foi fixado antes e o que foi acrescentado depois de ver resultados; o gerador procedural não é liberado, mas fica "disponível sob solicitação direta aos autores"; verificar se os itens 4, 6 e 8 já estavam no repositório.
- Repositório: `git fetch` sem commit novo do desktop desde 32735e3 (12:51). O item 4 (`r_pareado_sel`) continua "rodando desde 11:28" em STATUS e RESULTADOS; os itens 6 (grupo L) e 8 (grupo H) estão na fila da rodada 6, sem resultado. Nenhuma eficácia foi recalculada e nada do que entrou no texto depende deles.
- Resumo (`versao-curta-aim2027.html`): a primeira frase abre com "Synthetic imagery is the route this study takes..."; os corpora são "procedurally generated ... with no imagery of any real territory"; de 17 números para 7 medidas (150 m, 4,88 cm/px, 17,6 × 17,5 px, 2,2%, 15,3%, 62,7 contra 42,1%), taxas de objeto em palavras ("between one in eight and one in four") e a frase nova de que a separação a 150 m "is not yet resolved between the form of a firearm and its length". 376 palavras.
- 4.6: o Experimento C ganha o desenho do controle de comprimento (gêmeos de 75 e 150 m com os objetos escalados só no comprimento para 0,62 a 1,05 m, 80 quadros novos cada), marcado "still running when this version was written". O parágrafo "Confirmatory against exploratory" foi reescrito: o que foi fixado antes da primeira rodada (R, S-nadir-150, S-oblique, S-nadir-75 e a razão de eficácia), o que entrou depois com critério fixado antes (a lista da v9 mais os dois testes de 75 m), a única regra trocada depois do resultado (a do atalho a 150 m, aplicada em outubro e substituída em novembro antes de o controle rodar, "because no outcome could have failed it"), a hipótese agora testada (d′ do modelo de comprimento casado inclui zero = era comprimento; exclui = forma ou material sobrevive) e o que ainda rodava (controle de comprimento, R fora do teste, sementes, teto completo, orçamento de treino, especialista de sol duro com espelho, degradação de sensor, arma na mão). 6.1 (QP3) e conclusão: "shortcut" sai, a separação a 150 m fica "unresolved, not as capability"; a limitação (6) da 6.5 aponta para o controle.
- 4.8 e declarações: volta a frase da v9 sobre os três corpora cuja figura não se regenera exatamente (piloto, corpus de registro e S-nadir-75); "The procedural scene generator and its code are available from the authors on direct request; the corpora and the trained weights are not released" (4.8, Data availability e Dual use). A legenda da Tabela 2 apontava para uma frase cortada da 4.3 ("three derived training corpora of Section 4.3"); agora aponta para a Tabela 3 e nomeia os três.
- Extended abstract (`esqueleto-aim2027.html`): ainda tinha 6 marcas `[[NEW]]`. Saíram: linha de e-mail/ORCID apagada, parágrafo das armas em pixels copiado da 5.1 do artigo, duas células do sub-stride preenchidas com 0,9% e 3,9%, placeholders de casos documentados e de ablação de sensor apagados; a frase do atalho ficou coerente com o artigo.
- Diagramação: Elsevier de 17 para 18 páginas (corpo de 8.728 para 9.217 palavras pela contagem do `checa.py`; a última página tem cerca de um terço ocupado; nenhum buraco acima de 50 pt fora o artefato do título na p. 1); Carta/duplo de 41 para 43, 0 buracos; extended abstract 17. PDFs do Desktop regerados e página de download republicada.

## 2026-11-04 [MAC] Versão curta: marcas `[[NEW]]` removidas, números do desktop no texto, formato Elsevier como principal em 17 páginas

- Pedido do autor, à tarde: atualizar o artigo com o que já saiu sem GPU, tirar tudo que é `[[NEW]]`, fazer do formato Elsevier o principal e ocupar 100% de cada página, diminuindo páginas sem sair do padrão.
- Texto: as cinco marcas saíram. Os itens 1 e 2 fechados pelo desktop entraram sem marca: parágrafo novo na 5.1 com a pegada das armas em pixels (fuzil 1,07 m de ponta a ponta, 22 × 1 px a 150 m, 44 × 2 a 75, 94 × 4 a 35; pistola 4 × 0,6) e as duas células da Tabela 5 (0,9% e 3,9%), mais a cláusula "and 0.9 and 3.9 in the two oblique corpora" na frase do sub-stride; origem em `06-resultados/armas_malhas.md` e `alvo_por_split.json`. As frases-placeholder da 6.4 e da 6.5 foram apagadas. Corpo 8.728 palavras (era 8.736), 0 marcas, 0 travessões, nenhum caminho de arquivo no texto visível.
- Diagramação Elsevier (`gera_elsevier.py`): figuras e tabelas estreitas viram blocos flutuantes na coluna (`.flt`: float left, largura da coluna; se não cabem no pé da coluna sobem para o topo da seguinte e o texto preenche a coluna, comportamento confirmado em teste no Chrome 156: 10 pt de sobra contra 126 pt sem float); só as quatro figuras largas (92, 84, 100 e 84% da mancha) e as tabelas com 7 ou mais colunas ou 15 ou mais linhas (2, 4 e 5) atravessam as duas colunas; referências a 8 pt; a nota de trabalho entra na página 1 (`div.nota full`).
- `pagina.py` generalizado: `--colunas 2` mede por raster (pdftoppm a 36 dpi, fundo cinza em figuras e tabelas só na medição; soma das faixas brancas de 24 pt ou mais em cada coluna, inclusive ao lado de uma figura); terceiro movimento, o corte do parágrafo seguinte por busca binária na palavra que deixa a página cheia e o bloco largo no topo da página seguinte (segunda parte com `class="cont"`, sem recuo); um buraco passa a ser atribuído também aos blocos largos da própria página; títulos consecutivos contam como um grupo; a chave de aceitação (páginas, primeiro buraco acionável o mais ao fim possível, branco total) empurra a folga para a última página em vez de travar no primeiro movimento que não baixa o total. Resultado: de 19 páginas (18 + nota, 1.278 pt de branco no pé) para 18 (17 + nota, 465 pt, nenhum buraco acima de 50 pt; a última página termina 166 pt antes do pé). Carta/espaço duplo: 43 páginas (41 + 2 de nota), 0 buracos.
- `gera_pdf.sh`: Elsevier primeiro e nomes novos (`AIM2027_versao-curta_elsevier_DATA.pdf`, `AIM2027_versao-curta_carta-espaco-duplo_DATA.pdf`, extended abstract igual); os PDFs da manhã foram para `antigas-2026-11-04-manha/` no Desktop. `O-QUE-FALTA-NO-SERVIDOR.md` ganhou o estado de 04/11 à tarde (1 e 2 feitos, 4 rodando, o resto na rodada 6) e o PDF do Desktop foi regerado.
- Sincronização: os cinco commits da rodada 6 do desktop foram puxados antes da edição; a alteração dele nas duas células da Tabela 5 foi reaplicada sem a marca, e a nota `[[NEW]]` da 5.1 que ele expandiu virou o parágrafo em inglês.
- Decisões do autor, no fim da tarde: título (A) mantido; as cinco figuras ficam ("quanto mais melhor"); trilha do CFP "Applications of Natural Language Processing or Machine Vision". Registradas na nota de trabalho dos dois PDFs (regerados, mesmas 18 e 43 páginas) e no STATUS.
- À noite, a pedido do autor, a nota de trabalho saiu dos três HTMLs (versão curta nos dois formatos e extended abstract); o texto ficou em `NOTA-DE-TRABALHO.md`. PDFs regerados: Elsevier 17 páginas, Carta 41, extended abstract 17. `pagina.py` passa a medir da página 1 (`--primeira 1` por padrão) e `gera_elsevier.py` só reserva a página 1 se houver `div.nota` no fonte.

## 2026-11-04 [DESKTOP] Rodada 6 lançada: a lista do servidor inteira, por decisão do autor

- Pedido do autor, à tarde: "faça tudo que o PDF está propondo, se tiver que usar a GPU para rodar, rode, o que manda é o PDF agora". A lista deixava 3, 5, 6, 7 para o periódico e 8, 9 para pedido de revisor; agora tudo menos o 8 entra numa cadeia só.
- `07-blender/PLANO-RODADA6.md` escrito e versionado antes da partida (commit 7a459ea), com hipótese, etapas, custo e critério de cada grupo; `06-resultados/rodada6_criterios.py` executa os critérios (R, Q, L, E, G, V) e grava `rodada6_criterios.json` e `rodada6_eficacias.json/.md` (eficácias com o R de seleção fora do teste).
- Novidades de código: `objetos_alongados.COMPRIMENTO_ARMA` e `gen_morro.py --objetos-comprimento-arma` (objeto confundível escalado só no eixo do comprimento até 0,62 a 1,05 m; testado em headless, 40 objetos, todos na faixa, sem flag nada muda); `degrada_ladrilhos.py` (ruído, borrão e JPEG com probabilidade 0,75 nos ladrilhos de treino, val intacto, semente 0); `rodada6.py`, `supervisiona_rodada6.py` (não mata a cadeia enquanto o `r_sel.py` estiver vivo), `pausa_rodada6.py`, `status_rodada6.py`, `retoma_rodada6.cmd`.
- Desenho que vale registrar: o grupo R espera o treino do item 4 lançado fora da cadeia (R1 escreve no log a cada 15 min); o quadro de teste da flag (P2) roda depois de R porque a GPU está ocupada; o teto completo (item 9) treina em 6.147 imagens (train menos a fatia `sel`, que vira a seleção) para a seleção ficar fora do teste como no item 4; os três-classes "e120" (item 5 e 150 m do item 6) usam a receita do `armado_150g_e120`, o de 75 m do item 6 usa a do `armado_75g`.
- Lançamento às 11:48 por `Start-Process cmd.exe /c retoma_rodada6.cmd`; P1 passou (disco 407 GB, venv 8.4.148 / torch 2.14 / CUDA, HERIDAL convertida). Previsão 158 a 198 h, fim entre 11/11 e 13/11. Atalho `retoma_rodada6.lnk` na pasta Inicializar criado às 12:12 com o OK do autor ("Sim, crie o atalho"); aponta para `retoma_rodada6.cmd`, janela minimizada, e o supervisor o apaga no fim da rodada. E-mail de abertura na thread "Rodada 6: iniciada em 04/11 às 11:48".
- Item 8 (arma na mão), 11:50 a 12:10: implementado em `people_mpfb.py` (`ARMA_NA_MAO`, `_arma_na_mao`, `_fecha_mao`) e `gen_morro.py --arma-na-mao`: empunhadura no centro da palma direita, dedos fechados (sentido de flexão +1 conferido; o -1 hiperestende), braço esquerdo por IK até o guarda-mão nas poses de duas mãos; igual para objeto; jitter dos dedos com gerador próprio para a flag não mudar os sorteios (a primeira versão consumia o rng do lote e trocava as pessoas, corrigido). Conferência visual por `testa_mao.py` em CPU (32 s por fila), figura `06-resultados/figuras/item8_mao_conferencia.jpg`. Entrou como grupo H no fim da cadeia (P3 prova a flag; três gêmeos com 200 quadros, 80 novos, treinos e120, confusões cruzadas; seção 3.7 do plano, critério fixado antes), acrescentado às 12:10 sem nenhum resultado da rodada existir; a cadeia, que esperava em R1, foi reiniciada e o supervisor a relançou. Previsão com H: 208 a 258 h, fim entre 13/11 e 15/11. Fora do H, declarado: corpus original de 75 m, arma inédita e porte.

## 2026-11-04 [DESKTOP] Itens 1 e 2 do servidor fechados, item 4 lançado

- Entrada: o PDF `O-que-falta-no-servidor_AIM2027_2026-11-04.pdf` (cópia de `08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md`). Seguida a ordem sugerida: itens 1 e 2 sem GPU, item 4 porque a máquina estava livre.
- Item 1: `06-resultados/mede_armas.py` roda dentro do Blender headless e mede a caixa envolvente das malhas de `objetos_alongados.py` (12 sementes, caixa idêntica: o sorteio só escolhe material). Os dois fuzis medem 1,07 m de ponta a ponta (nominal 0,92 e 0,94), a espingarda 1,17 (nominal 1,05), a carabina 0,61, a pistola 0,195. Largura 0,030 a 0,050 m: abaixo de um pixel a 150 m para toda arma; cerca de 2 px a 75 m e 4 px a 35 m. Os "19, 38 e 81 px" derivados no `[[NEW]]` da 5.1 são limite inferior: o AK ocupa 22, 44 e 94 px. Inéditas e objetos confundíveis medidos de quebra (`armas_malhas.md`).
- Item 2: `mede_alvo_split.py` ganhou `ds_morro_obl` e `ds_oblvar`; as chaves antigas de `alvo_por_split.json` saíram idênticas. Sub-stride (lado menor < 8 px): 0,94% em S-oblique, 3,88% em S-oblique-six (medianas batendo com `forma_corpora.json`). Escrito nas duas células `[[NEW: measure]]` da Tabela 5 de `versao-curta-aim2027.html` como 0,9% e 3,9%, e a nota `[[NEW]]` da 5.1 ganhou as medidas; o PDF não foi regerado aqui (o fluxo `pagina.py` + `gera_pdf.sh` é do Mac).
- Item 4: ao montar a divisão de seleção descobri que `ft/sel` (324 imagens do VisDrone train) tem 59 imagens em comum com a amostra de treino de R (`visdrone_sub/train`, 1.106 imagens): os dois são sorteios independentes do mesmo train. Seleção em `ft/sel_r.txt`, as 265 restantes (`ft/sel_r.json` guarda as removidas). Treino `r_pareado_sel` com a receita de R conferida por `--dry-run --compara` (só `data` e `name` mudam); cadeia `07-blender/scripts/r_sel.py` (treino, zero-shot no VisDrone val, predições por imagem), idempotente e retomável de `last.pt`, lançada por `lanca_r_sel.cmd` com `Start-Process cmd.exe` às 11:28. Vigia de hora em hora na sessão; e-mail de abertura na thread "Item 4: teto R com seleção fora do teste". ETA 17:45.
- Não feito: 5.1 em inglês continua como `[[NEW]]` (o autor escreve os `[[NEW]]`); itens 3 e 5 a 9.

## 2026-11-04 [MAC] Versão curta para a AIM 2027: corpo de 8,7 mil palavras

- Pedido do autor: a professora indicou cerca de 10 mil palavras como ideal para a AIM; o autor fixou o alvo em 8 a 9 mil no corpo. A primeira tentativa (3/11) saiu com 18,7 mil e foi cortada em cinco rodadas, medidas por script a cada rodada, até 8.736 palavras (seções 1 a 7, sem resumo, tabelas, legendas, declarações e referências); com tabelas e legendas, 12.066; resumo com 363; declarações com 444; 80 referências, todas citadas; 12 tabelas e 5 figuras do v9, copiadas em bloco, sem redigitar número.
- Fonte: `08-conferencia/versao-curta/versao-curta-aim2027.html` (HTML à mão, CSS @page em Carta, margens de 1 pol., Times New Roman 12, espaço duplo); PDF por `gera_pdf.sh` com o Chrome headless: 45 páginas, a primeira é uma nota de trabalho em português, a apagar antes de submeter. O extended abstract de 3 mil palavras (`esqueleto-aim2027.html`, 19 páginas) continua na pasta como alternativa. Cópias autocontidas em `~/Desktop/AIM 2027 - Versao Curta/`; as de 3/11 ficaram em `antigas-2026-11-03/`. PDFs fora do git.
- Estrutura em relação ao v9: a 2.4 saiu; a antiga 3.4 (base ética da síntese) virou uma frase em 4.1 e a 3.5 passou a ser a 3.4; a 5.6 (robustez) virou uma frase na abertura da seção 5; a 6.1 perdeu o parágrafo de síntese. Remissões atualizadas; nenhum número alterado.
- Marcas no texto: 6 `[[NEW]]` (e-mails e ORCID no cabeçalho; pegada da arma em pixels na 5.1, que exige ler a largura das malhas no gerador do desktop; fração sub-stride dos corpora oblíquos na Tabela 5; casos documentados de objeto tomado por arma em operação no Rio na 6.4, com fonte ou a frase sai; ablação opcional de ruído, borrão e JPEG na 6.5; contagem final). Decisões do autor: título (A, B ou C), quais figuras ficam, trilha do CFP, se roda GPU antes de 19/11.
- Bug de renderização corrigido nos dois HTMLs: `white-space: nowrap` nas células numéricas deixava as Tabelas 4 e 9 a 12 mais largas que a mancha, e o Chrome encolhia o documento inteiro para cerca de 73% (os PDFs de 3/11 saíram com corpo de 9,7 pt). Verificação agora por `pdftotext -bbox-layout`: passo de linha de 24,0 pt e altura de palavra de 13,3 pt nas páginas de prosa.
- Depois da leitura do autor: a marca do cabeçalho (e-mails, ORCID, apresentador) saiu a pedido dele, sem e-mail na primeira página; dos premiados de 2026, dois trazem e-mail e dois não, nenhum traz ORCID, e o formulário de submissão nunca foi aberto (401). Ficam 5 `[[NEW]]`.
- Buracos no pé das páginas (13, 17, 18, 26, 27, 28: figuras e tabelas com `page-break-inside: avoid` pulando de página) fechados por `pagina.py`, novo na pasta: mede o branco de cada página com `pdftotext -bbox-layout` e move o bloco que pulou para depois do parágrafo seguinte, sem tocar no texto; a Tabela 11 passou a poder quebrar entre páginas com cabeçalho repetido. Resultado: 44 páginas, nenhuma com mais de 100 pt em branco. Rodar `pagina.py` depois de qualquer edição de texto e antes de `gera_pdf.sh`.
- O buraco apontado pelo autor estava na prévia Elsevier, não na versão AIM. A prévia virou parte do fluxo: `gera_elsevier.py` monta `versao-curta-elsevier.html` (A4, duas colunas, CSS do montador do v9, sem a nota) a partir da versão AIM e roda `pagina.py` nela; `gera_pdf.sh` renderiza os três HTMLs. `pagina.py` ganhou busca gulosa com até quatro passos de antevisão (um movimento só é aceito se baixar páginas ou branco), o caso do título que pula junto com a figura seguinte e o recuo para antes do parágrafo anterior quando não dá para avançar. Prévia Elsevier: 18 páginas, um só intervalo de 116 pt (página 7, antes da Figura 2) que nenhum movimento fecha. Versão AIM continua em 44 páginas sem buracos.
- Lista do que falta modelar e gerar no desktop, com custos tirados de `custo-rodada5.md`: `08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md`, com PDF na Área de Trabalho do Mac (`O que falta no servidor - AIM 2027 - 2026-11-04.pdf`). Ordem sugerida: itens 1 e 2 (sem GPU) até 19/11, 4 se houver máquina; 5 e 6 para o periódico.
- Lição de processo: estimativa de contagem feita de cabeça erra 30 a 60% para baixo e ajuste de frase quase não move o total; só a remoção de frases ou subseções inteiras move, e a contagem tem de ser medida a cada rodada.

## 2026-11-02 [DESKTOP] v9: correções da revisão simulada da AIM, inglês e português

- Regra do autor, registrada em memória e no parecer: o enquadramento é SEGURANÇA PÚBLICA; nunca compras públicas, licitação ou prestação de contas administrativa. O parecer foi limpo dessas sugestões antes de aplicar.
- Aplicado no inglês (oficial) sem perda de conteúdo: nenhuma tabela, figura, parágrafo ou número removido. Oito agentes em paralelo (seções 2, 3, 4, 5 e referências; eu mesmo em resumo, introdução, discussão, conclusão), depois quatro tradutores espelhando o diff no português.
- Mudanças principais: resumo compara a mesma condição nos dois benchmarks (8,8 e 15,3 no urbano; 62,7 contra 42,1 e 46,4 no nadir, faixas que se cruzam); objetivo restrito ao medido; 1.4, 2.4, 3.3, 6.4 e conclusão fecham a premissa "o instrumento vê o que dizem que vê" com o que comando policial, STF sob a ADPF 635, Ministério Público e moradores podem exigir de uma alegação aérea; declaração de uso dual; parágrafo demonstrado, hipótese e a validar no fim da 6.1; seção 2 apresenta o HERIDAL e a geometria oblíqua do VisDrone; seção 3 sem "steep slopes", 798 como agregado estadual, ADPF com as datas da 3.1, STF e UAV como siglas; Métodos sem número de resultado (épocas 58 de 60 e 27 a 30 foram para a 5.2 e 5.3); d′ com e sem correção explicitados; tabela de hipóteses com desfecho de critério em vez de rótulo; frases de luz condicionadas ao sintético.
- Referências: 113 para 119 entradas (Jocher & Qiu 2024; Lin et al. 2014 e Hautus 1995 com DOI conferido no Crossref; Blender Foundation 2026; MakeHuman Community 2026; Poly Haven n.d.), 23 títulos em português com tradução, JOTA e CBS com URL canônica, Kiefer 2022 e Sithole completados, "IEEE." uniformizado, travessão do Movisafe retirado. Kim 2026 fica como arXiv até o DOI existir. Citações contra entradas: zero faltas.
- Citações acrescentadas por escopo, sem releitura do PDF, a conferir pelo autor: Lessing 2008 e Misse 2011 (tráfico), InSight Crime 2026 e Misse 2011 (milícias) na 3.1.
- Não feito, por decisão de não perder conteúdo: cortes de extensão (corpo com cerca de 23 mil palavras; o AIM dá 112 páginas em espaço duplo), harmonização do "et al." em todo o texto, JMIS (abstract fixo no montador, desatualizado).
- Leitura final de ponta a ponta do PDF Elsevier em inglês (o de submissão, por decisão do autor; o formato "aim" foi descartado e não volta). Achados corrigidos: iniciais nos homônimos Wang (1.2 e 1.4) e "nesses dois benchmarks" na conclusão; no montador, a legenda de tabela passou a `<caption>` dentro da tabela e as tabelas largas podem quebrar entre páginas com linha inteira e cabeçalho repetido. Resultado: a página quase vazia antes da Tabela 27 (existia desde a v8) sumiu e dez páginas com 20 a 45 por cento de coluna em branco ficaram cheias; o PDF caiu de 44 para 41 páginas (PT: 44). Memória gravada: submissão sempre no Elsevier.
- Segunda rodada de vereditos sobre o PDF final (sete agentes, só leitura). Chegaram quatro antes de a cota da sessão acabar: resumo e introdução OK; discussão OK (três precisões aplicadas: sem "prosecutors", treino conjunto só no cronograma original, ordem no HERIDAL qualificada pelas leituras); seções 2 e 3 com um bloqueio corrigido (a ADPF 635 foi proposta só pelo PSB, com as organizações como amici curiae). Faltam os vereditos de Métodos, Resultados, Conclusão com referências e o transversal. Figura 2 (cena ao nível da rua) removida a pedido do autor; figura de similaridade movida para depois da sua tabela; tabelas com mais de três linhas podem quebrar entre colunas. PDF Elsevier em 41 páginas com cerca de 3 por cento de coluna em branco.
- Vereditos completos da segunda rodada (sete agentes sobre o PDF final): resumo e introdução OK; seções 2 e 3 OK após corrigir que a ADPF 635 foi proposta só pelo PSB, com as organizações como amici curiae; métodos OK (quatro precisões: partida sintética excluída da regra do COCO, divisão de treino completa mais cinco subconjuntos, legenda da Tabela 2, comprimentos de malha); resultados OK, cerca de 110 números conferidos na fonte sem divergência; discussão OK (três precisões); conclusão e referências OK após dois bloqueios corrigidos (os benchmarks também treinam o teto e as fatias do Experimento B; 152 quadros é a divisão de treino completa do S-oblique-six, não o maior corpus); transversal OK após prender o cabeçalho às primeiras linhas da tabela e pôr a sigla GSD no resumo. 119 citações, 119 entradas, zero faltas. PDF Elsevier em inglês: 41 páginas, 12 figuras, 27 tabelas, 3,5 por cento de coluna em branco. Veredito consolidado: pronto para submeter.
- v9 na Área de Trabalho (`v9_2026-11-02_revisao-aim/`): elsevier sem aviso de prévia (41 p., o PDF de submissão), elsevier-PT (44 p.). Cópias soltas "(versao atual)" trocadas de v8 para v9.

## 2026-11-02 [DESKTOP] Revisão simulada da v8 como revisor da AIM 2027

- Pedido do autor: puxar o parecer do Revisor 1 (Felipe I. Toledo, 14/10), ver o que ainda sobra dele e analisar cada capítulo como revisor da AIM lendo um artigo de administração pública, só com feedback construtivo e sem corrigir nada. O autor quer submeter hoje.
- Oito revisores em paralelo (um por capítulo e um transversal), só leitura. Parecer completo em `01-artigo/revisao-2026-11-02/PARECER-AIM.md`. Manuscrito intocado.
- Resolvido do Revisor 1: estrutura, RQs, design science, travessão, vazamento, marcadores, conectores, siglas (três deslizes), seleção contra teste, GSD, intervalos, PR, citações (214 pares, zero faltas).
- Não resolvido: extensão e repetição. Corpo com 22,8 mil palavras contra a meta de 16 mil; 106 páginas no formato AIM; seção 3 cresceu para 2,4 mil contra 1,2 mil.
- Achados que valem para a submissão de hoje: no resumo, o par oblíquo muda de condição entre os dois benchmarks (15,3% é S-oblique-six no VisDrone, 42,1% é S-oblique no HERIDAL); "dual use" ausente na 4.1 e nas Declarations; nenhuma seção fecha a pergunta de administração pública aberta na 1.2 e na 3.3. Sugestões de compras públicas devem respeitar a decisão de 27/10 de tirar esse enquadramento do resumo.

## 2026-10-27 [DESKTOP] v8: evolução da segurança pública, ética do treino sintético e citações na seção 1

- Pedidos do autor, lendo a v7 em português: (1) o resumo falava em compras e prestação de contas, que não se alinham ao artigo; reescrito com foco em segurança pública (letalidade das operações, terreno que a polícia conhece mal, drones já em uso, força letal dependendo do julgamento "armado ou não", dificuldade de treinar detectores nesse tipo de zona urbana); (2) a frase retórica sobre o título na 1.1 saiu; (3) a 1.1 não tinha citação: entraram as fontes já listadas; depois, citações em toda a seção 1 (de 10 para 40 em cada língua), só com fontes já na lista; (4) faltava falar da evolução da segurança pública e das questões éticas que sustentam o treino sintético: subseções novas 3.3 (câmeras corporais, policiamento preditivo, IA e drones na literatura de administração pública; o caso do Rio) e 3.4 (por que não se pode coletar imagem de morador, alternativas rejeitadas, o que o sintético resolve e o que não resolve); a antiga 3.3 virou 3.5 e as remissões foram atualizadas.
- Nove referências novas da Public Administration Review (Alcadipani et al. 2024; Frazier 2016; Gao e Riccucci 2026; Headley et al. 2025; Meijer et al. 2021; Selten et al. 2023; Selten et al. 2026; West e Bowman 2016; Wright et al. 2024), todas conferidas no Crossref; duas com ano de fascículo diferente do levantamento de 20/10 (2024, não 2023). Lista com 113 entradas, todas citadas.
- Tudo feito nas duas línguas. v8 na pasta versionada (Elsevier 41 e 44 páginas, JMIS 124). Resumo com 381 palavras em inglês: cortar ao limite da revista escolhida.

## 2026-10-27 [DESKTOP] v7: resumo com a visão da administração e da segurança públicas

- Pedido do autor: o artigo é administração, segurança pública e visão computacional, e o resumo não mostrava isso. Entrou um primeiro parágrafo (cerca de 130 palavras) com o problema visto pela administração pública e pela segurança pública: sistemas aéreos já voam sobre favelas policiadas, a força letal depende do julgamento "armado ou não", e treinar detectores para território denso, verticalizado e sem mapas é difícil por falta de consentimento para imagens, de benchmark e pelas condições de aquisição. O segundo parágrafo mantém os números. Palavras-chave ganharam public security e public administration. Resumo em inglês com 350 palavras (acima dos 250 usuais de periódico; cortar se a revista exigir), em português 381; abstract do JMIS com 150 ou menos.
- v7 nas duas línguas e no JMIS, na pasta versionada da Área de Trabalho (commit 40b2e1c).

## 2026-10-27 [DESKTOP] v6: decisões do autor sobre as declarações

- Decididos um a um com o autor: (1) ética: nenhum comitê precisava ser consultado, por não haver participantes humanos nem dados pessoais; a declaração diz isso; (2) conflito de interesse: nenhum autor tem ou teve vínculo com a Polícia Civil, outra polícia ou fornecedores de drones ou software; o projeto nasceu na graduação do autor e foi construído por ele; as imagens do levantamento de 2022 vieram pelo projeto de pesquisa da UFRJ, mas o autor preferiu remover a origem nesse projeto do artigo, já que nenhum resultado depende dela: saem o parágrafo de 2.2, os Acknowledgements e as menções à reconstrução fotogramétrica (4.1, 4.8, Ética, Disponibilidade de dados); (3) coautor delegado fica de fora; (4) declaração de IA fica como está; (5) gerador não liberado, sem justificativa no texto; (6) sem declaração CRediT.
- A câmera de referência (Zenmuse Z30) passa a ser descrita como carga flown a 150 m em nadir sobre territórios desse tipo, sem citar o voo de 2022.
- v6 em inglês (Elsevier 40 p., JMIS 119 p.) e tradução refeita para o português. PDFs na pasta versionada. O crédito de 2022 continua em `docs/CONTEXTO.md` e no repositório; só saiu do artigo.

## 2026-10-27 [DESKTOP] v4 rejeitada; v5 = v3 só corrigida

- O autor rejeitou a v4 (26/10): mudou o escopo (enquadramento em administração pública, apêndice, metade das figuras e tabelas fora do corpo). Pedido: voltar à versão anterior e aplicar apenas correções, sem grandes modificações, mantendo o apoio gráfico.
- Manuscrito restaurado do commit 29523f5 (v3). Passada só de correções: 7 revisores por seção, integrador e parecerista novo (escopo intacto, 0 graves, 11 menores aplicados). Nada de figura, tabela, subseção ou enquadramento mudou; nenhuma citação nova; nenhum padrão post hoc de capacidade. Lista completa do que mudou e do que a v4 tinha e não voltou: `01-artigo/revisao-2026-10-26/COMPARACAO-v3-v4-v5.md`. Texto da v4 e seu apêndice guardados em `01-artigo/revisao-2026-10-26/v4-texto/` e `apendice-online-v4.md`.
- Correções principais: manchete da QP3 (a confusão é menor a 2,44 cm/px, não "a resolução não reduz"); fator nadir/oblíquo 4,08 (3,44 a 4,64) pareado com as médias e 6,0 só com a semente 0; "camera pitch determines most" suavizado; R dito como teto do protocolo; nenhum limiar de capacidade fixado antes, dito como leitura; contradição ética/dados sobre as imagens de 2022 resolvida; termos e precisão unificados.
- PDFs v5 (Elsevier 40 p., JMIS 119 p.) na pasta versionada da Área de Trabalho. A tradução em português continua a da v3.

## 2026-10-26 [DESKTOP] Revisão de alto impacto (administração) em três rodadas

- Pedido do autor: revisar cada seção como revisor de revista de alto impacto em administração, cortar, simplificar, corrigir, agrupar e seguir o Revisor 1, com subagentes. Plano, pareceres e vereditos em `01-artigo/revisao-2026-10-26/` (PLANO-REVISAO.md, PARECERES.md, parecer-final-r2.json, parecer-final-r3.json).
- Rodada 1: 11 pareceristas (7 por seção, 4 transversais: contribuição para administração, Revisor 1, extensão, afirmações contra evidência), editor responsável consolidou o plano, 7 editores e o apêndice online em paralelo, integração e parecer novo. Rodadas 2 e 3: correções dos graves (QP3 contradizia o próprio resultado; comparação com model cards e AI Act; proposições testáveis na 6.4; extensão; padrão de capacidade declarado como fixado depois dos resultados).
- Resultado: corpo de cerca de 11,3 mil palavras (era 21 mil); JMIS 50 páginas (era 116), Elsevier 19, apêndice online 28 (`01-artigo/manuscrito/apendice-online.md`, PDF por `01-artigo/ferramentas/monta_apendice.py`). Enquadramento novo em administração pública (discricionariedade algorítmica, accountability, compras públicas), com fontes da PAR do levantamento de 20/10 e referências novas conferidas no registro.
- Pendente do autor (bloqueia submissão): parecer ou dispensa de ética da FGV EBAPE; fatos de conflito de interesse e de acesso às imagens de 2022; coautor delegado. As declarações têm marcadores entre colchetes. A tradução em `01-artigo/manuscrito-pt/` ficou desatualizada.

## 2026-10-22 [DESKTOP] Rodada 5 levada ao artigo

- Fonte: `07-blender/PLANO-RODADA5.md` (blocos "O que muda no artigo"), `06-resultados/RESULTADOS.md` (19 a 22/10), `rodada5_criterios.json`, `rodada5_criterios_M.json`, `revisao-2026-10-17/*_r5.md`, `bootstrap_heridal*.md`, `rodada5_grupo_d.py` (rodado de novo, mesma saída).
- Resumo (250 palavras): médias de três sementes (2,2% nadir, 15,3% S-oblique-six), inversão na HERIDAL (62,7% contra 42,1%), quatro cronogramas de ajuste fino, separação fraca a 150 m lida como atalho.
- 1.1, 1.3, 1.4: duas bases reais; contribuições com a inversão nadir, os quatro cronogramas e o atalho a 150 m.
- 4.1, 4.3, 4.5, 4.6, 4.7, 4.8: HERIDAL e o protocolo (imgsz casado 1152, 1280 secundário, todas as imagens anotadas); corpora derivados (sol duro, sementes de cena, subconjuntos); grade de cronogramas; gêmeo a 150 m com 120 épocas; etapa final como confirmatória com critério fixado antes; tabelas `params`, `modelos`, `corpora` e `rq` atualizadas; dez modelos com três sementes.
- 5.2: fator 4,08 (3,44 a 4,64) nas médias, eficácias 2,2% e 8,8% com a melhor semente; semente de cena (1,4 vez a de treino, +68,7%); curva de aprendizado (tabela nova `curva`); base nadir (tabela nova `heridal`); tabela `obliquo` com todas as sementes. 5.3: grade de doze células (tabela nova `cronograma`), +30,2% a 5% e +22,2% a 10%. 5.4: 150 m válido, d′ 0,58 (tabela nova `gsd150`). 5.5: ablação de sol duro (colunas novas em `regimes`). 5.6 e tabela `hipoteses`: todas as checagens rodadas, linhas novas.
- 6.1 a 6.6: RQ1 com fator 4,08, inversão na HERIDAL medida, curva e semente de cena; RQ2 robusto ao cronograma; RQ3 com atalho a 150 m; 6.3 passa de quando voar para com que luz treinar; 6.4, 6.5 (itens 1, 4, 5, 6, 7, 10) e 6.6 sem o que a rodada fechou. 7 e Declarations (duas bases). s8: entrada do Zenodo 5662351 (DOI conferido na DataCite) e grafia Pyrrö.
- Montador: abstract do JMIS atualizado (149 palavras) e f-string que não compilava no Python 3.11 do venv trocada por concatenação (o formato JMIS do Mac voltou a rodar aqui; teste sem citação perdida).
- PDF: `C:/Users/marti/Desktop/machine-vision-favelas-elsevier-2026-10-22.pdf`, 39 páginas, 27 tabelas, 13 figuras, 0 `[X]`, 0 "Table ?", 0 "Figure ?". Checagem: todo decimal de s1, s5, s6 e s7 achado no artigo anterior, nos arquivos D1 a D3 ou nos da rodada 5.
- Conflitos de fonte registrados: IC do grupo D no `rodada5_criterios.json` (Random(0)) difere do `rodada5_grupo_d.py` (default_rng(0)); o texto usa o segundo, que é o do RESULTADOS. Médias de S-oblique (0,0555 contra 0,0556) e S-oblique-six (0,0966 contra 0,0967) diferem na quarta casa entre o bootstrap e as tabelas do RESULTADOS; o texto usa as do bootstrap, coerentes com diferenças e razões. Contagens dos corpora derivados não estão em arquivo e ficaram fora da tabela `corpora`.

## 2026-10-20 [MAC] Aderência a PAR e AMJ

- Levantamento no Crossref (21 consultas por ISSN) e resumos no OpenAlex: 15 artigos de PAR e 5 de AMJ ligados a segurança pública, em `04-bibliografia/aderencia-PAR-AMJ-2026-10-20.md`. Nenhum sobre visão computacional, detecção aérea, dados sintéticos ou favelas.
- Leitura: PAR tem linha ativa sobre IA, discricionariedade e polícia (exige reenquadrar o artigo como argumento de administração pública e cortar muito); AMJ com aderência muito baixa. Decisão do autor pendente.

Entradas novas no topo. Formato: `## 2026-10-20 [MAC] Artigo no formato do JMIS

- `monta_artigo.py --formato jmis`: manuscrito anônimo para o Journal of Management Information Systems (regras em jmis-web.org/info-for-contributors). Times 12, espaço duplo, alinhado à esquerda, Letter, página numerada; abstract cortado para 148 palavras (os mesmos números do de 18/10, constante `ABSTRACT_JMIS`); citações autor-ano convertidas em número entre colchetes, referências numeradas em ordem alfabética; 23 tabelas e 13 figuras no fim com "[Insert ... about here]" no texto; Funding e Acknowledgements saem do manuscrito e vão para um PDF de folha de rosto à parte. Roda no Mac (Chrome headless) e no Windows (Edge).
- Resultado: 103 páginas (corpo até a p. 50, referências 51 a 64, tabelas e figuras 65 a 103). O JMIS limita o manuscrito completo a 50 páginas: precisa cortar cerca de metade, decisão do autor.
- Folha de rosto com marcadores para endereço, telefone e bio de cada autor. PDFs na Área de Trabalho do Mac.

## AAAA-MM-DD [MÁQUINA] título`, depois o que foi feito, o que foi decidido e o que ficou para o outro lado. Nunca apagar entrada antiga.

## 2026-10-22 [DESKTOP] Rodada 5 encerrada

- Cadeia terminou em 22/10 às 11:05, todos os grupos concluídos (S, F, N, Y1, A, D, M, C, Y2 a Y4); pausa do autor de 21/10 23:38 a 22/10 01:41, retomada sem perda. O supervisor apagou o atalho da pasta Inicializar.
- Resultados que mudam o artigo: fator nadir/oblíquo cerca de 4 (não 6) com três sementes; na HERIDAL a ordem se inverte e o nadir chega a 63% de R (78% com seis sítios); o custo do pré-treino sintético não é do cronograma; a curva sobe pouco no fim; o sol duro deixa de ser pior quando o treino o vê bastante; a 150 m o modelo de três classes é válido e separa fraco, por atalho; a semente de cena varia 1,4 vez a de treino. Detalhe em `06-resultados/RESULTADOS.md`, entradas de 19 a 22/10.
- E-mails por grupo na thread "Rodada 5: iniciada em 18/10 às 23:43". Próximo passo: levar tudo ao manuscrito.

## 2026-10-18 [DESKTOP] Rodada 5 lançada

- Autor liberou a GPU e autorizou a HERIDAL. Fonte oficial (FESB) fora do ar; usada a cópia no Zenodo (registro 5662351, Pyrrö, CC BY 3.0, 8,31 GB, md5 conferido no fim do download), a mesma versão do AIR, já citado no artigo. Divisão pré-registrada: todas as imagens anotadas.
- Cadeia da rodada 5 escrita e testada (grupo P real em 18/10 23:28), commit 3a2e121. Primeiro lançamento pelo Explorer falhou no P2 (Blender sem MPFB); relançada pela sessão com `cmd /c`, P2 ok às 23:43 (6 humanos) e S1 começou.
- Acompanhamento: e-mail inicial com ordem e previsão (thread "Rodada 5: iniciada em 18/10 às 23:43"), checagem de hora em hora (aos 17 min) que relança a cadeia se morrer, converte a HERIDAL quando o download terminar e manda e-mail a cada grupo concluído.

## 2026-10-18 [DESKTOP] Coautor retirado, financiamento, citações e manutenção

- Autor: não houve financiamento nem bolsa (declarado no bloco Funding); o coautor delegado sai por ora. Sem ele, a 4.1, a 3.2, a limitação 8 da 6.5 e o conflito de interesse foram reescritos: nenhuma frase diz mais que um autor é policial, o contexto passa a vir só de fontes públicas, e os autores declaram não ter conflito. A versão anterior está no commit 682a96e, para quando o coautor voltar.
- Citados G-MAD (Kim et al., 2026; DOI da ACM ainda não registrado, citado pelo arXiv) e Berwaldt, Bettker e Pozzer (2020, DOI conferido). A 2.2 diz que o trabalho nasce do projeto UFRJ de 2022 e por que o ARMA 3 foi trocado; Acknowledgements para Fábio H. P. Guimarães e o prof. Claudio Miceli de Farias.
- Censo: o 35.458 é do subdistrito (SIDRA, tabela 9923); a publicação de favelas do IBGE dá 29.766 para a favela (tabela 5). O texto traz os dois, com fonte.
- Sobre a AIM: o edital (`08-conferencia/modelos_2026/AIM2027_CFP.pdf`) dá o prazo de 19/11/2026, mas não o formato; o "8 a 12 páginas" do dossiê é inferido dos premiados de 2026 e foi apresentado ao autor como exigência por engano.
- Resumo para leigo refeito (`01-artigo/resumo-leigo-2026-10-18.md`, 2 páginas; montador mais robusto ao Edge headless). Inventário dos dados com 16 corpora e 26 runs e SHA256 (`06-resultados/inventario.py`). CONTEXTO corrigido (E3). PENDENCIAS sem item aberto. Painel republicado.

## 2026-10-18 [DESKTOP] Decisões do autor sobre o artigo reestruturado

- O autor decidiu não liberar o gerador de código (A3). A 4.8 e o Data availability dizem que o gerador, o código, os corpora e os pesos não são liberados.
- Declaração de uso de IA incluída nas Declarations (A4): Claude (Anthropic) usado para revisar o texto, conferir e corrigir informações e grafia, e auxiliar no monitoramento dos treinos.
- OK do autor às mudanças sugeridas: A1 (sem design science), A2 (morfologia em trabalho futuro) e A7 (sete seções) ficam como aplicados. Aplicados também os pontos que o validador deixou: convenção do d′ da similaridade e intervalo aproximado da arma inédita passados para a seção 4; frase interpretativa do piloto movida para a limitação 7; intervalos repetidos da 6.1 retirados (ficam na seção 5, menos o do fator 6,0); sinais de diferença corrigidos na 6.1.
- PDF refeito (32 páginas, 13 figuras, 23 tabelas, 0 `[X]`) e página privada atualizada. Seguem abertos: coautor delegado (A5), financiamento e rodada 5 (A6).

## 2026-10-18 [DESKTOP] Artigo reestruturado pelo feedback de 14/10

- Material recebido em 17/10 na pasta `FEEDBACKS ARTIGOS` do autor: `feedback.txt` (estrutura-alvo de sete seções, parecer em três blocos, esqueleto de seis seções, mensagens de WhatsApp), quatro áudios de 14/10 (transcritos localmente com faster-whisper large-v3-turbo em CPU), o PDF de 30/09 e o livro de Zobel. Tudo copiado e resumido em `01-artigo/feedback-2026-10-14/` (`FEEDBACK-RECEBIDO.md`; regras de Zobel em `zobel-checklist.md`).
- Plano em `PLANO-CORRECAO.md`: cada ponto do revisor com ação, seção e agente; decisões tomadas (estrutura de sete seções, sem "design science", proposta de morfologia em trabalho futuro, contexto policial condensado, sem treino novo) e decisões abertas A1 a A7.
- Fase 1, só inferência e levantamento (nenhum treino, nenhum render): D1 fatos dos corpora, GSD e zoom da Z30 (manual da DJI), seleção de checkpoint, fatos do gerador, custo da rodada 5; D2 intervalos por reamostragem (as 17 reproduções batem com o publicado a 0,00005; FP16 descartado por desviar até 0,0045), curvas PR, varredura de limiar, resolubilidade; D3 similaridade de recortes com o tronco congelado do YOLO11s COCO; D4 bases reais nadir (HERIDAL, SeaDronesSee, Stanford Drone).
- Fase 2: seis escritores, uma seção cada, a partir de `ARTIGO-COMPLETO-2026-09-30.md`. Fase 3: integrador (consistência de GSD, d′ e siglas, inserções das análises, cortes para 18,9 mil palavras de corpo, referências com 99 entradas cruzadas, PDF) e validador independente.
- Achados que mudam a leitura: o teto R selecionou o checkpoint no próprio conjunto de teste; o fator 6,0 sobrevive à reamostragem (4,6 a 7,0) mas segue com uma corrida por lado; as diferenças do ajuste fino são estáveis e pequenas em termos relativos (nenhuma chega a 30%); 35 m contra gêmeo só é resolvível nos quadros novos; a similaridade não separa arma de objeto (resposta à sugestão do áudio); o 75 m original também teve corpos não semeados (corrigido no arquivo do D1).
- Abstract corrigido à mão: "25 contra 12,5% em 80 quadros novos" é da semente 0, e o que vale para as três corridas é a direção.
- Os 13 arquivos antigos saíram de `01-artigo/manuscrito/` (cópias idênticas em `01-artigo/manuscrito-2026-09-30/`); o montador lê `s1` a `s8`.
- Fica para o autor: ler o PDF, reenviar ao revisor, decidir A1 a A7 e a rodada 5.

## 2026-09-30 [DESKTOP] Refino geral do artigo, análise, resumo para leigo

- Pedido do autor: análise do artigo com o contexto todo, checar se os pontos se ligam, cortar ou resumir, criticar, acrescentar imagens e tabelas, tirar os quadros de autoria deixando um aviso de versão prévia, entregar a versão refinada por e-mail e um resumo "for dummies" de 1 a 2 páginas para o orientador.
- Diagnóstico e lista do que foi aplicado em `01-artigo/ANALISE-2026-09-30.md`. Resumo: a espinha do argumento se sustenta; o problema era repetição (cada resultado em 9, 10, 11 e conclusão; quatro frases-guardiãs de 4 a 9 vezes cada) e histórico de rascunho dentro do artigo.
- Aplicado no manuscrito: abstract de 510 para 330 palavras; 7.2, 7.3, 7.7, 8.1, 9 (piloto), 9.2, 9.3, 9.5, 10.1, 10.2, 10.3, 11.1, 11.2, 11.4 e Limitations encurtadas; 11.1 (escala) absorvida pela 7.6 e 10.7 removida; seção 11 renumerada (11.1 a 11.5, 24 remissões trocadas); seção 6 deixa de antecipar o resultado da 9.4. Corpo de 28,0 mil para 26,5 mil palavras.
- Acréscimos: Figura 5 (diagrama do desenho experimental) e Figura 8 (mAP50 contra imagens reais, três usos do sintético, três sementes, teto R), ambas por `06-resultados/figuras_mpl.py`; Tabela 8 (resultados de relance), Tabela 16 (35 m contra gêmeo, dois conjuntos, três sementes, três IoU) e Tabela 17 (por regime). As 17 tabelas ganharam número e legenda e as 10 figuras são citadas no texto: o montador numera na ordem de leitura e resolve `@fig{}` e `@tab{}`.
- Montador: quadros de autoria fora por padrão (`--com-autoria` devolve), aviso único "Preliminary version, not final" no início (`--sem-previa` tira); figura larga atravessa as colunas a partir de 1,8 de razão de aspecto.
- Origem de cada número das peças novas em `06-resultados/RESULTADOS.md` (entrada de 30/09, refino); as duas eficácias do treino conjunto (73,0 e 86,0%) são razões calculadas de números já reportados.
- Dez críticas que ficam para os autores (ANALISE, seção 4): extensão e periódico-alvo; título da seção 6; proposta contra o resultado da 9.4; o fator 6,0 sem sementes; d′ fraco em toda altitude; coautor sem nome; liberação do gerador; Closing repete o abstract; harmonização de estilo; peso das seções 3 e 4.
- Resumo para leigo em português: `01-artigo/resumo-leigo-2026-09-30.md`, 2 páginas, PDF por `monta_resumo_leigo.py` (Edge headless com perfil próprio, porque a primeira tentativa colidiu com a instância do montador do artigo).
- PDF Elsevier: 17 páginas, 28.621 palavras com referências, 10 figuras, 17 tabelas, 0 `[X]`, na Área de Trabalho. Como o anexo de 5 MB não cabe na ferramenta de e-mail, o artigo e o resumo foram publicados numa página privada da conta claude.ai do autor (https://claude.ai/artifact/WPd1bZtKCVSo6XN56qMeuf, com botões de download) e o e-mail levou o link, o resumo do refino e o resumo para leigo no corpo.

## 2026-09-30 [DESKTOP] Figura 7 refeita: objeto na mão e visível

- Pedido do autor: na figura 7 a pistola e o guarda-chuva não batiam com o objeto, e em alguns recortes a arma estava solta do corpo.
- Primeiro conferi se era erro de rótulo, e não é. Nos corpora com `caixas`, a ordem de classe bate com o arquivo de rótulo em todos os quadros e os tipos batem com as caixas armada e objeto. No `ds_armado_35`, que só tem `tipos`, o número de tipos bate com o de caixas nos 200 quadros. As taxas por objeto da 9.5 não mudam.
- A causa está no gerador (`people_mpfb.py`): o objeto é preso no punho direito (ou nas costas) com orientação fixada por pose no espaço do corpo, sem ser resolvida contra as mãos. Na pose "ao lado" ele aponta quase na vertical, e de cima o guarda-chuva de 0,88 m encolhe a um toco escuro com cara de pistola. A pistola, de 0,20 m, quase não aparece; no recorte antigo de 35 m, o objeto comprido que se via era um varal da cena.
- A figura foi refeita com escolha a olho sobre folhas de candidatos: os de maior caixa por tipo e altitude, com visibilidade de pelo menos 0,85, sozinhos no recorte e sob luz clara. O critério foi objeto na mão e perto da horizontal. As escolhas e o critério ficaram fixados em `06-resultados/figuras_artigo.py` (fig7).
- A legenda da figura 7 diz o critério e a origem dos recortes. A 7.4 ganhou uma frase sobre como o gerador prende o objeto.
- PDF refeito na Área de Trabalho: 28 páginas, 31.267 palavras.

## 2026-09-30 [DESKTOP] Busca bibliográfica aplicada ao manuscrito

- OK do autor às cinco frentes do relatório de 30/09.
- Texto: 33 trocas em 10 arquivos.
  - Arma portada: "we found no public aerial benchmark that annotates a carried firearm at these altitudes" no abstract, na abertura da 7, na 7.7 e na conclusão. A 7.7 ganhou o parágrafo sobre os benchmarks de vigilância e o material aéreo a 2 a 8 m. A 7.4 cita os precedentes do objeto confundível (Sohas; Dual-UAV, do CEFET-RJ) e a 7.6 o do ladrilhamento (ACF). A 8.2 diz que o VisDrone não tem categoria de arma.
  - Céu limpo: a 8.4 e o fecho atribuem a convenção ao aerolevantamento. A 11.3 separa as três práticas (especificação de aerolevantamento, mapeamento com drone, regras de voo) e ganhou duas ressalvas (chuva vedada no Brasil; busca e salvamento não escolhe a luz). A 8.3 ganhou Dare, Du et al. e Reilly et al. e a 10.3 o parágrafo de que nenhum benchmark real isola o contraste. A 7.5 passa a declarar as faixas de elevação do sol (46 a 74 graus no hard sun, 9 a 25 no low sun; origem em RESULTADOS).
  - Sintético que atrapalha: parágrafo novo no fim da 9.4 (Kiefer et al., fig. 2; SynPlay; Archangel; PTL; Martinez-Esteso et al.). A seção 2 ganhou a ressalva de que o ganho é condicional, com as citações, e a citação do VisDrone (Zhu et al., 2022), que faltava.
  - B1: Barisic, Horváth, Gevaert e Watson e Elliott ajustados ao que as obras dizem, sem as oito a nove palavras copiadas dos resumos.
  - Seções 3 e 4: saem Wikipédia, Vanguard Attaché, Crime Brasil e "Ad Infinitum". Entram ISP-RJ, os 19º e 20º Anuários, Justiça Global, CNN Brasil com autoria, Lessing, Misse, InSight Crime, Grillo e as notas do Small Wars Journal com autores. Pico da série em 1994; 121, 122 e 132 mortos, cada um com a fonte. Sai "the sharpest increase recorded nationally". A diferença 699 contra 703 deixa de ser atribuída a séries diferentes.
- Referências: 65 novas; os 45 DOIs foram reconferidos no Crossref nesta sessão, e o do Zenodo no DataCite. Dez entradas saíram ou foram substituídas e cinco foram corrigidas. Os dois blocos APA viraram uma ordem alfabética só. Checagem cruzada: toda entrada é citada e toda citação tem entrada.
- Escolhas feitas no lugar do autor, para revisão:
  - 51 e 100 mandados ficaram ambos, cada um com a origem.
  - A construção que bloqueia a visada e a falta de mapas atualizados das rotas ficaram como premissa declarada do estudo, porque nenhuma fonte lida as sustenta.
  - O sobrenome "Américo da Silva" do registro do editor não foi adotado; só o volume e a inicial foram corrigidos.
  - O traço da manchete do InSight Crime virou dois-pontos na entrada.
- PENDENCIAS: B1, B3, B6, B7, B9 e B10 fechados; B8 em parte. Quadros de autoria do PDF atualizados.
- PDF Elsevier refeito na Área de Trabalho: 28 páginas, 31.171 palavras, 8 figuras, 0 `[X]`. Continua sem ir por e-mail, porque publicar num artifact espera autorização explícita.

## 2026-09-30 [DESKTOP] Busca bibliográfica dos pontos abertos: relatório para o OK do autor

- Pedido do autor: busca bibliográfica com multiagentes, sem rodar o teste de 1%. Oito agentes em cinco frentes, com verificação cética das fontes. Relatório em `04-bibliografia/busca-2026-09-30-pontos-abertos.md` (resultado bruto no `.json` ao lado). Nada no manuscrito foi alterado.
- Pedem mudança no texto, se o autor aprovar:
  - "no public benchmark annotates a carried firearm" é amplo demais: há benchmarks de vigilância com arma portada e material aéreo público a 2 a 8 m (entre eles o Dual-UAV, do CEFET-RJ, com réplica de fuzil contra guarda-chuva). Proposta: "we found no public aerial benchmark that annotates a carried firearm at these altitudes", nas quatro ocorrências.
  - "clear weather" como convenção de voo junta três práticas; só o aerolevantamento tem convenção escrita de céu limpo, e o hard sun do gerador cabe nela. Proposta de reescrita da 8.4, da 11.3 e do fecho.
  - A 9.4 tem precedentes: pré-treino com corpus sintético pequeno também perde no Kiefer et al. (fig. 2) e no SynPlay. Proposta de parágrafo novo na 9.4 e de citações na seção 2.
  - Referências B1: as 13 conferidas; cinco entradas já inseridas têm erro de metadado e duas frases copiam oito a nove palavras do resumo sem aspas.
  - Fontes jornalísticas: "CNN Brasil (2026a)" é da Defesa em Foco; "maior alta do país" é falso em termos relativos; o pico da série do ISP é 1994; o ISP também dá 703 em 2024.
- Resolvido: "more than 1,200 military police officers" está na fonte B7 (InSight Crime, 27/01/2022).
- Nota de processo: dois agentes mandaram o e-mail do autor no campo de contato das primeiras consultas ao Crossref; as seguintes saíram sem ele.
- Correção à entrada anterior: o PDF não seguiu anexado. A ferramenta do Gmail só aceita anexo passado inline e o arquivo tem 5 MB; a publicação do PDF num artifact privado, para mandar o link, foi barrada pelo classificador de permissões e espera autorização do autor. O PDF está na Área de Trabalho do desktop.

## 2026-09-30 [DESKTOP] Revisão geral do manuscrito, figuras em inglês, PDF enviado

- Pedido do autor: trocar os rótulos em português das figuras 2, 4 e 5, revisar o texto inteiro atrás de inconsistências, corrigir e mandar o PDF Elsevier por e-mail.
- Figuras 2, 4 e 5 com rótulos em inglês; a 5 refeita com Arial (a fonte bitmap do PIL comia os espaços). Comandos em `06-resultados/figuras_artigo.py` e em `RESULTADOS.md`.
- Revisão em três lentes (números, lógica, forma), com cada achado conferido na fonte antes de entrar: 128 trocas nas 12 seções. As que mudam o sentido:
  - 10.3: "Both parts of the condition hold" invertia o resultado; agora "Neither part of the condition is met".
  - "dense favela" no abstract, na pergunta de pesquisa e na conclusão (restos de "self-built settlement").
  - Intervenção no Jacarezinho em janeiro de 2022, não 2023 (Cidade Integrada, 19/01/2022), e "less than seven months" depois da decisão da ADPF.
  - Pela regra oficial do VisDrone a eficácia do S-oblique-six cai (16,7 para 16,4), não sobe.
  - Sintético e real juntos a 10% contra pré-treino sintético a 10% inverte a IoU 0,75: ressalva no texto.
  - Ausência a 150 m descrita como argumentada, não medida, em todas as ocorrências; 35 m é a altitude mais alta em que um teste passou a condição de validade.
  - Nota do d': a replicação usa correção log-linear (0,77 e 0,89 no val contra objetos confundíveis).
  - Revisão de literatura: a afirmação de que sintético mais real fecha a lacuna vem agora com o resultado contrário da 9.4.
  - Quadros do piloto passaram da 9.3 para a 10.3, com legenda que identifica o corpus; título da seção 9 passa a "Results: Transfer to Real Imagery and the Armed and Unarmed Distinction".
- Os dois `[X]` viraram "specified and has not been run"; o PDF sai sem marcador. O montador imprimia o título duas vezes na capa (o H1 herdado do docx); corrigido.
- Origem de cada número conferido na revisão registrada em `06-resultados/RESULTADOS.md` (vão entre lotes, variação de altitude oblíqua, h/w 1,58, 2.659 e 3.225 caixas, receita de R com semente 21, receita do piloto).
- PDF Elsevier: 31 páginas, 27.606 palavras, 8 figuras, 0 `[X]`; enviado ao autor por e-mail.
- Não aplicado, fica para o autor: harmonizar -ize/-ise, % e datas no texto do orientador e do coautor; numeração e remissão de figuras e tabelas; o que a 9.4 implica para a proposta da seção 6; "more than 1,200 military police officers" contra as fontes (cerca de 1.200 policiais civis e militares, pendente da fonte B7); abstract acima de 510 palavras; menções a "drafts" e a correção do 2,49 que aparece duas vezes; travessão no título de uma referência (08-references.md, linha 52); topografia do Jacarezinho (neutralizada na conclusão).
- Busca bibliográfica com 8 agentes concluída; relatório a seguir em `04-bibliografia/`, sem mexer no artigo antes do OK do autor.

## 2026-09-30 [DESKTOP] Título: "Self-Built Settlements" vira "Favelas"

- Pedido do autor. Novo título: "Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Favelas" (manuscrito e montador do PDF). O corpo ainda diz "dense self-built settlement" no abstract, na pergunta de pesquisa e na conclusão.
- PDFs Elsevier regerados na Área de Trabalho.

## 2026-09-30 [DESKTOP] Manuscrito atualizado com a rodada 4

- Consequências de cada veredito aplicadas (commit 35b09ca): abstract, 7.6, 7.7, 8.3, 9.3 a 9.5, 10.2, 10.3, 10.6, 10.7, 11.2, 11.3, 11.5, 11.6 e conclusão. Correção da 10.2 sobre o piloto incluída. Caixas de estado do PDF e PENDENCIAS (D4) atualizadas.
- PDFs Elsevier regerados na Área de Trabalho: 26.626 palavras, 5 figuras, 2 `[X]`.
- Para o autor: o abstract foi a ~510 palavras; a seção 6 (proposta) não foi mexida, mas a 9.4 agora mostra que o sintético não ajuda nem como pré-treino nem misturado.

## 2026-09-30 [DESKTOP] Rodada 4 encerrada: vereditos dos critérios fixados antes

- Encerrada às 10:25, sem grupo com falha, depois de quatro pausas do autor. Números e comandos em `06-resultados/RESULTADOS.md` (entrada de 30/09); vereditos em `rodada4_criterios.json`.
- Confirmado: a vantagem do COCO no ajuste fino a 5% sobrevive a três sementes; misturar sintético e real também fica abaixo do só real (5% e 10%); nenhuma comparação do VisDrone troca de ordem entre IoU 0,5, 0,6 e 0,75; a regra oficial das regiões ignoradas não muda nada; o sol duro é o pior regime (a 11.3 fica); a diferença de 35 m contra o gêmeo de 75 m se replica em 80 quadros novos (p 0,0001) e entre as três sementes nesses quadros.
- Muda o texto: o 16,7% do S-oblique-six foi o melhor de três treinos (média 15,3%, faixa 14,1 a 16,7%); o objeto no porte de arma não é chamado de arma com mais frequência (sai a ressalva do ângulo); a ordem dos armados muda com o limiar de IoU e a diferença 35 m contra gêmeo some a 0,75 no val original; no val original as sementes não separam 35 m do gêmeo.
- Não interpretável pela regra: o gêmeo a 150 m detectou 148 de 297 pessoas (0,498, limite 0,5). A ausência a 150 m continua argumentada.
- Correção: a checagem de escala do piloto na 10.2 não casava escala (o validador leva toda imagem ao mesmo lado maior). Casada pelo imgsz (1024), o nadir vai de 0,0102 a 0,0128, abaixo do limite de 50% fixado antes.
- A seguir: consequências no manuscrito e PDFs, em commit separado.

## 2026-09-27 [DESKTOP] Rodada 4 disparada para amarrar o artigo

- Pedido do autor: montar e rodar o pacote recomendado (150 m com objetos confundíveis, sintético e real no mesmo treino, sementes, objeto no porte de arma, validação maior a 35 e 75 m, regime de luz, VisDrone oficial e IoU, escala casada). Plano e critérios em `07-blender/PLANO-RODADA4.md`, versionados antes do primeiro resultado (6ebbaa9). Disparada às 11:31; previsão de cerca de 60 h.
- Código novo:
  - `06-resultados/avalia_visdrone_oficial.py`: validador do Ultralytics com a regra de `dropObjectsInIgr.m` do kit oficial, conferida na fonte. Sem regiões, reproduz o número padrão (0,1055 do S-oblique-six); com a regra, o mesmo modelo dá 0,1074 no teste prévio.
  - `escala_casada.py`, `por_regime.py` e `rodada4_criterios.py`.
  - Flag `--objeto-porte-arma` no gerador: mesmos sorteios, então os quadros saem gêmeos caixa a caixa (conferido em 3 quadros).
  - `--seed` no `train_yolo_win.py` e `--instancias` no `confusao_armado.py`.
- Achado: o validador do Ultralytics redimensiona toda imagem para o lado maior valer imgsz (`data/base.py`). A checagem de escala do piloto na 10.2 comparou a mesma escala de entrada; a frase será corrigida com o resultado novo. No protocolo de 1280, a mediana do lado maior do VisDrone val na entrada da rede é 25,33 px (perto dos 25,0 nativos); o casamento com os 20,55 px do corpus nadir se faz a imgsz 1024.
- Pendência para o autor: meu primeiro teste do gerador, com caminho relativo, deixou as pastas `C:\_teste_porte_a` e `C:\_teste_porte_b` (três quadros pequenos cada, procedurais). A proteção do Claude Code bloqueou a remoção na raiz do C:; podem ser apagadas à mão.

## 2026-09-27 [DESKTOP] Artigo validado em 10 rodadas depois da rodada 3

- Pedido do autor: resumo leigo por e-mail (enviado), atualizar os resultados no artigo e validar num loop de 10 rodadas. Cada rodada foi um revisor independente, só leitura, com uma lente: números contra fontes; consistência e remissões; critérios declarados antes; força das afirmações; proveniência; texto desatualizado; método contra código; revisor cético; forma; passe final. Todo achado foi conferido antes de entrar. Registro completo em `01-artigo/VALIDACAO-2026-09-26.md`.
- 287 achados aplicados. Os que mudam o argumento:
  - A expectativa da 9.4 falhou, e o texto dizia "as expected".
  - O denominador de Kiefer é o VisDrone inteiro, não real de outro domínio.
  - A ausência a 150 m é argumentada pela resolução, não medida, e a frase "learnable a 150 m" era resto do braço fotogramétrico.
  - Cada modelo treinou uma vez só, e isso agora está declarado no corpo do texto.
  - O protocolo cresceu em etapas.
  - A taxa de aprendizado real era AdamW 0,002, não 0,01.
  - Objetos longos são carregados em ângulo que nenhuma arma usa.
  - O S-oblique usou uma biblioteca de armas posterior à do nadir.
  - A taxa de objeto chamado de arma é um limite inferior.
  - O VisDrone foi reduzido a uma classe, e as regiões ignoradas contam como falso positivo.
- Fontes novas em `06-resultados/`: `mede_alvo_split.py` (`alvo_por_split.json`) e `ft_curvas.py` (`ft_curvas_selecao.json`). PDFs Elsevier regerados na Área de Trabalho a pedido do autor.
- Engano meu na rodada 5: um comando de PowerShell gravou STATUS.md vazio no commit 0ddf0d8, e ele foi restaurado da versão anterior no commit seguinte.
- Para o autor: abstract com ~450 palavras (meta ~150); liberar ou não o corpus; periódico; fonte para voar com céu limpo; aval nas passagens reescritas; rótulos em português nas figuras 2, 4 e 5; pendências de referências.

## 2026-09-26 [DESKTOP] Rodada 3 encerrada: gêmeo a 75 m e ajuste fino no VisDrone

- Gêmeo a 75 m (C1 a C4): o comando do corpus de 35 m mudando só a altitude (2.257 caixas, pessoa armada 48 × 43 px). Objeto chamado de arma 16,5% contra 27,3% a 35 m (p 0,06), desarmada 10,9% contra 16,8%, mesmo mAP50 (0,508 contra 0,514). O negativo de 35 m não vem da pose: o modelo de 35 m chama mais gente de armada em todas as classes. Análise em `06-resultados/compara_gemeo.py`.
- Ajuste fino (D1 a D6), teste no val inteiro do VisDrone: com 5% (324 imagens), 0,4424 partindo do sintético contra 0,5220 do COCO; com 10% (647), 0,5095 contra 0,5709. O pré-treino sintético custa 6 a 8 pontos, e o sintético com 647 imagens reais não alcança o COCO com 324. A expectativa declarada (benefício maior no volume menor) não se confirmou: o que encolhe com mais dado é um custo.
- Artigo: `[X]` da rodada 3 preenchidos (9.3, 9.4, 9.5, 11.5), linha do `ds_oblvar` na tabela da 8.2, uma frase no abstract e uma na conclusão; PDFs regerados. Ficam `[X]` só na robustez 10.1 e 10.3.
- Pausa do autor às 10:04, no meio do treino do gêmeo; retomada de `last.pt` às 10:49 sem perda. A coluna `time` do results.csv zera na retomada, e o status passou a estimar o ritmo pela mediana das diferenças entre épocas.
- Para o autor decidir: se o resultado da 9.4 muda a proposta da seção 6, e qual a próxima rodada (sintético e real misturados; ajuste fino mais longo ou com camadas congeladas; robustez).

## 2026-09-25 [DESKTOP] Rodada 3: teste de arma inédita passa; pausas a pedido do autor

- B1 e B2 (teste de arma inédita da 11.5): `armado_75` sem retreino, 50 quadros novos a 75 m com metade das armas de dois modelos nunca vistos (FAL, submetralhadora). Recall de armada 0,466 (61/131) nos inéditos contra 0,400 (50/125) nos cinco de treino, nas mesmas imagens; razão 1,16, acima do limiar pré-declarado de 0,8: a afirmação fica. O reconhecimento segue comprimento e silhueta, não o modelo (FAL 0,50 junto das armas longas vistas; pistola 0,20; guarda-chuva 0,38). Critério em `06-resultados/holdout_criterio.py`.
- Pausas a pedido do autor para usar o PC: 10:46 a 13:20, 18:30 a 19:44 e desde 22:26 (`pausa_rodada3.py`). Na primeira, uma cópia órfã do vigia em bash relançou a cadeia seis minutos depois; o vigia foi aposentado e a pausa encerra tudo, supervisor primeiro. Às 22:26 a cadeia estava no C1 (gêmeo a 75 m), 16/200 quadros, todos íntegros; faltam ~19 h de máquina.
- Consertos: caminhos com `\a`, `\b` e `\f` tinham virado caracteres de controle no STATUS e no RESULTADOS; o formato no topo deste diário tinha sido partido por inserções anteriores.

## 2026-09-25 [DESKTOP] Queda do PC e supervisor fora do app

- O PC desligou de forma abrupta por volta das 23:25 de 24/09 (Kernel-Power 41, sem tela azul, sem erro de hardware ou de driver antes; padrão de queda de energia ou fonte desarmando) e religou às 23:26. A fila morreu e só voltou às 08:49 de 25/09, quando uma sessão foi aberta: 9,5 h perdidas, nenhum quadro perdido (80/180 íntegros, retomada do 81).
- O status dizia 'cadeia VIVA' com ela morta: 'rodada3.py' casa com 'status_rodada3.py'. Corrigido no status, na trava e no vigia.
- A pedido do autor: atalho na pasta Inicializar do Windows que abre `supervisiona_rodada3.py` numa janela própria. Teste de 25/09: processo nascido da sessão (descendente do explorer do usuário) carrega o MPFB; nascido de um explorer lançado por DCOM (pai svchost), como no Agendador e no WMI, não carrega. O atalho roda pelo shell do usuário no login, como a sessão. O supervisor substitui o vigia em bash, que morria com a sessão, e apaga o atalho ao terminar a rodada.
- Armadilha: o python.exe do venv é um lançador que abre o interpretador real como filho com a mesma linha de comando; qualquer detecção de 'outra instância' precisa excluir os ancestrais.

## 2026-09-24 [DESKTOP] Rodada 2 encerrada e rodada 3 disparada

- Rodada 2 (22/09 22:28 a 24/09 16:54, com queda às 17:16 de 23/09 quando o app atualizou): teste de dose 0,0102 → 0,0190 no VisDrone; oblíquo 4K 0,0614 (6x o nadir, eficácia 9,7%); armado a 35 m negativo.
- Confusão refeita em imagem inteira com casamento um para um (`06-resultados/confusao_armado.py`): 75 m objeto→armada 23,7%, 35 m 27,3%. Os 25% e 31% do e-mail de 24/09 05:05 vinham de ladrilhos, que contam a mesma pessoa mais de uma vez; corrigido ao autor por e-mail.
- Calibração do braço combinado medida no próprio corpus oblíquo (`mede_forma.py`): h/w sobe com o pitch, 1,35 a 26-30° e 1,97 a 50-52° nas pessoas sem arma; a caixa da pessoa armada inclui a arma e é mais larga (1,38 contra 1,58). Acima de 50°, 2 de 6 quadros saíam só com copa de árvore: gerador ganhou `--camera-livre`, `--pitch-obl`, `--armas mista_inedita` e o tipo de cada caixa no manifest.
- Teste de arma inédita (11.5) redesenhado antes de rodar: em vez de treinar em 4 modelos e testar no 5º (um corpus e um treino novos), dois modelos que nunca entram em treino (FAL 1,10 m, submetralhadora 0,55 m) misturados meio a meio com os cinco de treino num corpus de teste de 50 quadros; recall comparado nas mesmas imagens. Critério fixado antes: retirar o número de 75 m se o recall nas inéditas cair abaixo de 4/5 do recall nas vistas.
- Bug latente corrigido na nova cadeia: a fila antiga usava best.pt como prova de treino feito, e o Ultralytics grava best.pt já na primeira época.
- Artigo: números oficiais em 7.7, 8.2 (curva h/w por pitch), 9.1 a 9.5, 10.1, 10.2, 10.4, 10.5, 11.2 e 11.5; 9.4 deixa de ser adiada e vira ajuste fino no VisDrone, com resultado `[X]`.

## 2026-09-22 [DESKTOP] Revisao da fila e disparo da cadeia da noite

- Recortes do modelo armado a 75 m: 23% de objeto chamado de arma porque a arma e uma linha de 1 a 2 px e o objeto ia em pose de tiro em 42% dos casos. Flags novas no gerador: `--porte-realista`, `--fio-gsd`, `--laje`, `--amostra-no-quadro`, `--enquadro quadrado`. Amostra a 35 m mostra coronha e carregador.
- Sitios: mata varre por sitio, 5 paletas, rua estreita e rio; MPFB semeado (quadros agora reproduziveis; os corpora anteriores nao eram, e o artigo 10.6 e 11.6 foi corrigido).
- Benchmark de render: `--otimizado` da 3%, descartado. Perfil: 42 s fixos + 1,6 s por sample no 4K.
- Revisao por agentes, verificada: Blender devolvia rc=0 em excecao (`--python-exit-code 1`); fila_noite saia sempre 0 (agora 1 se falhou); controle tem 2 classes e alvos so no centro (dose usa `--mistura 0.5 0.5 0 --enquadro quadrado`); obliquo em 1080p dava 3,7x menos ladrilhos (agora 4K a 120 m); zoom a 35 m so tinha 1 a 3 caixas por quadro (amostragem em quadro: 9 a 11); residuos do obliquo de zero caixas afastados; teto sintetico do avaliador com single_cls do modelo (numero nao mudou: 0,7915 / 0,0102).
- Cadeia disparada as 22:28: dose, zoom, obliquo. ~30 h.

## 2026-09-21 [DESKTOP] Os primeiros números de sim-to-real, e três defeitos que eles revelaram

Primeira vez que o projeto tem a razão de eficácia que o artigo precisa. Também a primeira vez que
três defeitos de geração aparecem no mesmo dia, todos da mesma família: código que roda sem erro e
produz dado errado.

### Os números

| | mAP50 | arquivo |
|---|---|---|
| S-nadir no próprio sintético | 0,7915 | `resultados/s_nadir_4k.json` |
| S-nadir zero-shot no VisDrone | 0,0102 | `06-resultados/sim2real_s_nadir_4k.json` |
| R pareado, 1.106 imagens reais, hiperparâmetros idênticos | 0,6311 | `resultados/r_pareado.json` |
| razão de eficácia | **1,6%** | |

O braço real usa os MESMOS hiperparâmetros e o MESMO N do sintético (yolo11s, 1280 px, 60 épocas,
batch 6, init COCO). Na rodada anterior os dois diferiam em modelo, imgsz, épocas e inicialização
ao mesmo tempo, e por isso a comparação não isolava nada.

### Três defeitos

1. **Braço oblíquo: 180 imagens, 992 pessoas, zero caixas.** O recuo da câmera tinha o sinal
   trocado, e o filtro de enquadramento usava um raio derivado da largura do quadro NADIR, que não
   vale com a câmera inclinada. Corrigido apontando a câmera com `to_track_quat` e trocando o
   filtro por projeção. 2,6 h de render perdidas.
2. **Lote armado com 7,4 pessoas por imagem em vez de 14 a 30.** Mesma causa: o raio de aceitação
   encolhe junto com a altura, e a 75 m caía de 49 m para 24 m. Refeito depois da correção.
3. **`data.yaml` com duas classes tendo três nos rótulos.** O gerador passou a emitir
   `pessoa_objeto` mas o writer do yaml continuou declarando duas. Quebraria o treino horas depois
   do render. Agora conta as classes que foram de fato escritas.

Freio novo no gerador: se cinco quadros renderizarem sem nenhuma caixa, aborta. Foi o que faltou
no item 1, e é o tipo de coisa que só se descobre pagando.

### Correções de número que mudam argumento

- **O alvo mediano é 17,5 px, não 24,6.** 24,6 é o percentil 90 da largura. A área do nosso alvo
  bate com a do VisDrone em 1,00x (301 contra 300 px²) e o que difere é FORMA, por 2,04x (h/w 0,98
  contra 2,00). Ferramenta em `06-resultados/mede_alvo.py`.
- **Kiefer et al. conferido na fonte.** A métrica é mAP@50, como as notas diziam. O intervalo
  "1,2 a 2,4" omitia a linha do YOLO, que é o nosso detector e marca 10,2 sintético contra 43,9
  real, ou 23,2% de razão. Estamos catorze vezes abaixo da referência que se aplica, não "na mesma
  ordem de grandeza" como eu havia dito.
- **Liao et al. conferido na fonte.** Tirar variação de luz, clima e ângulo custa 30,4 pontos no
  YOLOv11. Trocar base fotogramétrica por assets genéricos custa 27,0. O artigo é inconsistente
  consigo mesmo entre 22,5 e 23,3 na média. O objeto deles é VEÍCULO, não pessoa.
- **O denominador da literatura é outro.** Liao compara contra um real treinado FORA do domínio de
  teste (36,4 no VisDrone); nós comparamos contra um real treinado no PRÓPRIO VisDrone (63,1). Por
  isso eles dão 94% e nós 1,6%. O artigo precisa reportar os dois.

Fichas em `04-bibliografia/kiefer-2022-numeros-conferidos.md` e `liao-2026-numeros-conferidos.md`.

### O que entrou no código

- `07-blender/scripts/sitios.py`: coleção de 40 sítios variando relevo (plano, morro, dois morros,
  encosta), avenida com asfalto e carros, densidade, altura média e regime de mata. O índice -1 é o
  sítio histórico, e foi conferido que reproduz byte a byte o `ds_morro_4k` (4.068 lotes, 439
  edificações, 208.396 faces com semente 21).
- `07-blender/scripts/fila_noite.py`: fila de 22 etapas, uma GPU de cada vez, com log por etapa e
  retomada pelo arquivo de saída.
- `07-blender/PLANO-EXPERIMENTAL.md`: quatro frentes com custo de GPU declarado.

### Decidido pelo autor

- Nenhuma imagem real de pessoa armada entra. O braço armado é 100% sintético.
- O teste de dose de variedade (6 sítios x 30 imagens contra 1 sítio x 180, mesmo total) roda antes
  do treino no VisDrone inteiro, que passa a ser o último da fila.
- A escala futura vai por número de SÍTIOS, não por número de imagens do mesmo sítio.

### Para o outro lado

Os três números de sim-to-real do artigo ainda não existem todos: há o zero-shot, falta o com 5 a
10% de dado real e o sintético mais real. São as frentes C do plano. E o braço oblíquo precisa ser
refeito: é ele que decide se o 1,6% é problema de síntese ou de geometria de captura.

## 2026-09-20 [MAC] Dossiê da AIM 2027 entra no repositório

A pesquisa sobre a conferência e sobre os artigos do congresso só existia no Mac, na pasta irmã `~/Documents/Mestrado/AIM2027/dossie-conferencia/`. Movida em bloco para `08-conferencia/`, sem alteração de conteúdo, para que o desktop consiga puxar: `ESTRATEGIA_AIM2027.md` (revisão 2), `ROTEIRO.md` (48 missões, todas feitas), `missoes/` (48 arquivos, blocos A a F), `eixos/EIXO_GENAI_CONSUMO.md` e `modelos_2026/` (CFP mais os quatro papers premiados de 2026). Um `README.md` novo explica o conjunto, as datas da conferência e o formato da submissão.

Numeração: a pasta nasceu como `07-conferencia` no Mac e virou `08-conferencia` no rebase, porque o desktop já havia publicado `07-blender/`.

Decidido:
- Os cinco PDFs de `modelos_2026/` (11 MB) são a única exceção à regra de não versionar PDF de paper: são o CFP e o modelo de formato da submissão, e precisam existir nas duas máquinas. Registrado em `CLAUDE.md` e no `.gitignore`.
- Os temas T1 a T5 do dossiê são linha de pesquisa distinta (GenAI e consumo), levantada quando ainda se avaliava o que submeter. O que serve ao artigo de visão computacional é o calendário, o formato exigido, os modelos de 2026 e o Bloco F (ofício do paper).

Para o desktop: depois do `git pull`, o dossiê está em `08-conferencia/`. A pasta `dossie-conferencia/` do Mac não existe mais.

## 2026-09-20 [DESKTOP] Decisão: o método é o Blender

O autor decidiu adotar o Blender como método do trabalho e do artigo, por facilitar a escrita e a criação dos scripts em Python e por ser o caminho mais eficaz pelo que o levantamento mostrou. Isso fecha o item 1 de `docs/DIVERGENCIAS.md`. O ARMA 3 passa a constar como origem da ideia em 2022 e como prior art via G-MAD, não como método executado.

Também foi feito o levantamento de qual é a melhor modelagem disponível hoje. É a "cidade de sólidos" do braço `cid150`: sólidos por edificação segmentados do DSM da PCERJ, paredes e lajes com PBR autoral do Poly Haven, sol livre. Renders de referência em `C:\arma3-favela\odm\cidade\` (5 câmeras, 1920x1080) e cena em `C:\arma3-favela\odm\quadra.blend`. É também o braço com o melhor mAP50 no sintético (0,676). Nada disso entra no git nem no painel, porque a geometria vem do dado da PCERJ (item 2 das divergências, ainda aberto).

Fica para o autor: aplicar a decisão no texto do manuscrito, e decidir os itens 2, 3 e 4 das divergências.

## 2026-09-18 [DESKTOP] Reconciliação com o repositório

Feito (17 e 18/09):
- `gh` instalado e autenticado, repositório clonado em `C:\projetos\machine-vision-favelas`, identidade git configurada só no clone.
- Inventário completo, só leitura, da pasta real de trabalho, que é `C:\arma3-favela\` (44 GB, não era repositório git, então não havia histórico a preservar). Nenhum processo de treino ou render estava rodando.
- Código do desktop copiado: pasta nova `07-blender/` (19 scripts Python, 8 de batelada, README), missão e automação do ARMA 3 em `03-arma3/missao/` e `03-arma3/scripts/windows/`, `capturaDataset.sqf` e `train_yolo.py` sobrescritos pelas versões do desktop.
- `06-resultados/`: `RESULTADOS.md` com a ficha do experimento no topo (cada número com arquivo e comando de origem), 5 runs com `args.yaml`, `results.csv`, curvas, matrizes, `val_final.json` e `val_por_classe.txt`, manifests de randomização dos 5 datasets, `ONDE-ESTAO-OS-DADOS.md` com SHA256 de 13 arquivos de pesos. Previews com caixas só do braço OSM.
- `docs/DIVERGENCIAS.md` (14 itens), `docs/AMBIENTE-DESKTOP.md`, seção "Vindo do desktop" e linha do tempo corrigida em `docs/CONTEXTO.md`, cópia da nota do Obsidian, `05-levantamento-3d/desktop/LEIA-ME.md`.
- Três citações conferidas em 18/09: Liao et al. 2026 e Berwaldt et al. 2020 no Crossref, G-MAD no arXiv.
- `STATUS.md`, `PENDENCIAS.md` (C5, D4 e novos D5 a D8), `CLAUDE.md` (mapa e tabela de máquinas) e painel atualizados.

Descoberto:
- O experimento não rodou no ARMA 3. Foi tentado em 11/09 e abandonado na mesma noite sem nenhuma captura. Tudo foi feito no Blender 5.2.1 headless.
- Três dos quatro braços usam fotogrametria das fotos da PCERJ, refeita no OpenDroneMap porque o processamento de 2022 se perdeu. Nada saiu do desktop.
- As classes são `pessoa_armada` e `pessoa_desarmada`.
- Nenhum número de sim-to-real existe. O VisDrone nunca foi baixado.
- A pesquisa "a partir do e-mail de 12/09" não foi feita no desktop. A prova de conceito da quadra é anterior ao e-mail e independente dele.

Decidido (pelo desktop, dentro das regras de precedência, com OK geral do autor em 18/09):
- Código Blender em pasta própria `07-blender/`, não dentro de `03-arma3/`.
- Nenhuma imagem com textura ou geometria PCERJ entra no git: dos runs `blender_odm_tiles` e `cid150_s` só entraram números e gráficos. Nenhum `.log` entrou (um deles tem latitude e longitude do voo).
- Scripts do Google 3D Tiles ficaram de fora.
- Caminhos absolutos nos scripts não foram consertados agora; proposta registrada.

Fica para o autor: as quatro divergências abertas (itens 1 a 4 de `docs/DIVERGENCIAS.md`) e o OK para a mudança de base de trabalho.

Fica para o Mac: ler `docs/DIVERGENCIAS.md` e `05-levantamento-3d/desktop/LEIA-ME.md` antes de tocar em `06-results-proposed-model.md` e em Limitations; o que o Mac sabia sobre "pipeline ARMA 3" está superado. Os itens D1 a D3 de `PENDENCIAS.md` continuam valendo e agora têm as citações conferidas.

## 2026-09-17 [MAC] Prompt de reconciliação para o desktop

O autor informou que o desktop avançou muito (modelo já treinado) e que há uma pesquisa feita lá a partir do e-mail de 12/09 ("Levantamento técnico: recriar quarteirão de favela em 3D com alta fidelidade", enviado de si para si). Esse e-mail é o resumo do levantamento cujo PDF completo só existia no Mac e agora está em `05-levantamento-3d/`. `docs/PROMPT-MIGRACAO-DESKTOP.md` foi reescrito (versão 2) para esse cenário: fases com parada para aprovação, regras de precedência (desktop prevalece em experimento e código, repositório prevalece em estrutura e manuscrito, pesquisa é união), divergências registradas em `docs/DIVERGENCIAS.md`. O prompt também está no painel, com botão de copiar.

Para o desktop: tudo que este lado afirma sobre o experimento está desatualizado. Corrigir sem cerimônia, com arquivo de origem para cada número.

## 2026-09-17 [MAC] Reorganização da pasta e repositório único

Feito:
- Pasta `~/Documents/Mestrado/AIM2027/` separada em duas áreas: `dossie-conferencia/` (estratégia AIM 2027, roteiro, 48 missões, eixos, modelos de formato; movidos em bloco, links relativos preservados) e `machine-vision-favelas/` (este projeto).
- As três pastas soltas (PROJETO MACHINE VISION FAVELAS, PROJETO DRONE PCERJ, PESQUISA CV DRONES) foram fundidas aqui, na mesma estrutura numerada do pacote de 11/09 que o desktop recebeu.
- Rascunhos do orientador copiados de `~/Downloads` para `01-artigo/rascunhos-professor/`. Achado: `Machine Vision from the Global South(2).docx`, baixado em 17/09, tem o mesmo MD5 do `(1)` de 10/09. Não existe v3.
- v2 dividida em 8 arquivos Markdown por seção com `01-artigo/ferramentas/docx_para_secoes.py` (só biblioteca padrão, roda igual no Windows). Texto verbatim.
- Auditoria do rascunho refeita e ampliada em `01-artigo/PENDENCIAS.md`.
- Criados `CLAUDE.md`, `STATUS.md`, este diário, `docs/CONTEXTO.md` (conhecimento que estava só na memória do Claude do Mac) e os guias de setup do desktop.

- Repositório privado criado e publicado: https://github.com/LulianoM/machine-vision-favelas. O primeiro commit tem a tag `v2-irigaray-verbatim` (texto do orientador sem nenhuma alteração). Painel web publicado: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH

Decidido:
- Um repositório git é a fonte única de verdade. O desktop é a máquina central. A memória automática do Claude não é canal de comunicação entre máquinas.
- Scripts em `03-arma3/scripts/` aqui são os ORIGINAIS de 11/09. As versões do desktop, se evoluíram, prevalecem: o desktop sobrescreve e o git mostra a diferença.

Para o desktop:
- Seguir `docs/PROMPT-MIGRACAO-DESKTOP.md`. O mais urgente é `06-resultados/RESULTADOS.md` e a atualização do `STATUS.md` com o estado real do treino.
