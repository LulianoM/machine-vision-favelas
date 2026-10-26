# Comparação v3, v4 e v5 do artigo

Passagem de integração de 27/10/2026. A v5 é a v3 (commit 29523f5, 22/10, com os resultados da rodada 5) restaurada e só corrigida. A v4 (commit f3bb2cd, 26/10) foi rejeitada pelo autor em 27/10 por ter mudado o escopo; seu texto fica guardado em `v4-texto/` e seu apêndice em `apendice-online-v4.md`, só para comparação. Nada foi commitado nesta passagem.

Regras seguidas na v5: nenhum número mudou de valor a não ser para bater com a fonte (`06-resultados/RESULTADOS.md`, `06-resultados/revisao-2026-10-17/limiar_armado.md` e `bootstrap_visdrone_r5.md`); nenhuma figura, tabela ou subseção foi removida ou movida; nenhuma citação nova; perguntas de pesquisa, título, lista de contribuições e enquadramento intactos; grafia britânica, "per cent" na prosa, sem travessão.

## (a) O que a v5 corrigiu em relação à v3

### Resumo e Introdução (s1)

1. Resumo: a frase de QP3 "At 75 and 35 m detectors called 24 and 27 per cent of ordinary objects armed, finer resolution not reducing it" contradizia o resultado confirmatório (taxas de objeto em quadros reservados 0,245, 0,125 e 0,253 a 4,88, 2,44 e 1,14 cm/px). Agora: "On held-out frames, detectors called 24.5, 12.5 and 25.3 per cent of ordinary objects armed at 150, 75 and 35 m, lowest at the middle resolution". As altitudes saíram da frase anterior do resumo para ficar dentro das 250 palavras (249).
2. 1.1: "lethal force turns on a single judgement" alinhado com a 3.3, que agora declara isso como premissa: "a single judgement, whether the person engaged was armed, is taken here as central to decisions to use lethal force (Section 3.3)".
3. 1.3, objetivo: os cinco termos da condição de aquisição com os mesmos nomes da 1.1 (altitude, sensor e lente, GSD, pitch, iluminação); antes eram quatro com nomes diferentes.
4. 1.3, QP3: "which the reference camera reaches at 150, 75 and 35 m" era erro de fato (a câmera de referência dá 9,71 cm/px a 150 m sem zoom); agora remete aos GSDs que os rótulos de altitude denotam (4.2.4).
5. 1.4, contribuição 4: GSDs ditos como GSD (2,44 e 1,14 cm/px) e não como altitude; registra que a taxa foi menor a 2,44; "new frames" virou "held-out frames".
6. Montador (`monta_artigo.py`): o abstract do JMIS voltou ao da v3 com só a frase de QP3 corrigida (149 palavras).

### Trabalhos relacionados (s2)

7. GNSS expandido na primeira ocorrência (única no artigo).
8. mAP definido uma vez em 2.2; s4 usava "mAP" sem definição.
9. 2.1: "neither literature has integrated the vertical dimension" contradizia Gevaert et al. e Watson e Elliott, citados logo antes; reescrito para dizer o que cada literatura faz com a dimensão vertical e o que continua aberto (as classes da 6.6).
10. 2.2: "the evidence above concerns objects that fill a substantial share of the frame" era falso para os resultados de pessoa no VisDrone do parágrafo anterior; restringido aos resultados de domain randomisation.
11. 2.2: VisDrone-DET nomeado (s4 remetia à 2.2 por esse nome, que não aparecia).
12. 2.2 e 2.4: "Kiefer, Ott and Zell" com vírgula serial como as outras citações de três autores (também corrigido em 6.1).
13. 2.2: "largest gain with the smallest real set" restrito ao VisDrone, conforme a nota de conferência de 30/09.
14. 2.2 e 6.1: YOLOv11 virou YOLO11, o nome usado em s4.
15. 2.3: "none is aerial at the altitudes of this study" virou "none we found".
16. 2.4: Liao et al. não ablacionaram aparência de superfície; "geometry origin matters more than surface appearance" virou "geometry origin and rendering variation both matter".
17. 2.4: as três perguntas não mapeiam uma a uma nas três aberturas; a frase final diz que a terceira abertura é a razão de a QP3 ser só sintética.

### Contexto (s3)

18. 3.1: "Lethal police intervention has not followed" contradizia a queda de 1.814 para 699 (2019 a 2024) dita depois; agora "did not follow in 2025".
19. 3.1: "civil police" e "Civil Police" unificados.
20. 3.1: contagens de um a nove por extenso quando não são dado medido (um policial, dois helicópteros, quatro policiais), como o resto da seção.
21. 3.1: "nearly 6 years" para a ADPF 635 (2019 a abril de 2025) virou "more than five years".
22. 3.1: a divergência 699 contra 703 dita com precisão: "for reasons neither source documents".
23. 3.3: "the legal and operational category on which the use of lethal force turns" não tinha fonte legal; agora é declarado como premissa ("we take as a premise, not as a finding of the sources cited here, that ... is a central category").
24. 3.3: "Missing an armed person fails the operation" (consequência sem apoio) virou "withholds a warning from the officers".

### Materiais e métodos (s4)

25. 4.1: "no imagery of the territory is collected or used" contradizia a 4.8 e a declaração de disponibilidade de dados; agora diz que nada entra em resultado relatado e que o trabalho exploratório anterior com imagens do levantamento fica excluído (4.8).
26. 4.2.2: "Experiment C neutralises the third [cue]" restrito ao teste carregado-como-arma, no corpus original de 75 m, e dito que nenhum teste neutraliza as duas primeiras; registrado que no corpus de 35 m e seus gêmeos a pose de carregar é uma quarta pista não neutralizada.
27. 4.3: GSD do HERIDAL "within a factor of 2 of the reference acquisition" era 2,0 a 3,3 vezes mais fino; corrigido.
28. 4.4: três propriedades medidas "sem detector" eram quatro, e a quarta usa o tronco pré-treinado no COCO; contagem e afirmação corrigidas.
29. 4.5: "every efficacy ratio against it [is] conservative" era afirmação forte demais: R também treina no cronograma não ajustado, então a direção do viés líquido não é conhecida.
30. 4.7: dito uma vez que R é teto para o protocolo, não para o VisDrone (treina em 1.106 das 6.471 imagens no cronograma compartilhado).
31. 4.7: declarado que nenhum limiar, em d′ ou nas taxas, para dizer a capacidade presente foi fixado antes dos resultados; os pontos de operação são relatados descritivamente e a Seção 6 os lê. Nenhum padrão post hoc entrou (os cortes 0,10 / metade / 0,09 / 0,42 da v4 ficaram fora).
32. Terminologia: "new frames" virou "held-out frames" nas seis ocorrências de s4 que nomeiam o conjunto (4.2.2, 4.4, 4.6 e Tabela rq); a definição em 4.3 ("rendered after the models they test had been trained") ficou.

### Resultados (s5)

33. Tabela visao: as linhas F-synthetic e F-generic traziam só a semente 0 enquanto a legenda prometia média de três; rotuladas como primeira semente, com remissão à Tabela ajuste. Valores inalterados.
34. 5.1: "the crops of the three classes did not separate" era afirmação forte demais (intervalos de AUC excluem 0,50 a 2,44 e 4,88 cm/px); agora "separated only weakly ... less than under the detector". Idem em 6.1 e 6.6.
35. 5.1: "between -0.03 and +0.03" contradizia a maior entrada 0,032 na mesma frase; agora "-0.030 and +0.032".
36. Tabela similaridade e prosa de 5.1: o d′ 0,67 do detector a 4,88 cm/px é o do primeiro modelo de 150 m, que falhou a condição de validade; marcado.
37. 5.4, abertura (manchete de QP3): "halving the GSD did not reduce that rate" agora diz de 2,44 para 1,14 cm/px, com 0,253 contra 0,125, e que a 4,88 a taxa foi 0,245, a menor no GSD do meio.
38. Tabela gemeo: d′ marcado como com correção log-linear, como as outras tabelas de d′.
39. 5.4, "Seed by seed": as diferenças de média das sementes com intervalos, que a Tabela hipoteses já citava e o texto não trazia (+0,072, -0,023 a +0,163; +0,004, -0,053 a +0,062; +0,050, -0,017 a +0,111; -0,018, -0,063 a +0,031).
40. 5.4, varredura de limiar: "none brought the object rate below 0.09 while keeping armed recall above 0.42" (cortes fora dos pontos observados) virou o fato descritivo: a taxa de objeto 0,10 ou menos deixa recall de armada de no máximo 0,42 (gêmeo a 75 m, terceira semente, quadros reservados, precisão 0,61) e 0,38 ou menos nas outras combinações.
41. 5.5: a perda do especialista sob os outros regimes vale para recall (sob neblina 0,569 contra 0,726); em mAP50 ficou igual sob nublado pesado e acima sob sol baixo e nublado. Dito assim em 5.5, 6.3 e 7.
42. Tabela hipoteses: linha de iluminação "held" virou "held on point estimates; the margin of overcast over rain lies within the recall intervals"; linha do déficit de sol duro deixou de atribuir à fração de treino um intervalo que inclui zero (-0,0572, -0,1252 a +0,0067).

### Discussão (s6)

43. 6.1, QP1: "camera pitch moved the figure most" virou "camera geometry moved the figure by the largest factor"; geometria (+0,0419) e pacote de seis sítios (+0,0411) são quase iguais em valor absoluto, só a razão (4,08 contra 1,74) favorece a geometria. Dito que S-oblique-six é um pacote de quatro mudanças (4.6) e que só o par nadir isola a variedade (+0,0054).
44. 6.1 e 7, QP3: 25 virou 25,3 per cent (fonte 0,253); "one in four" virou "a little over one in four (0.165 to 0.273)"; "finer resolution did not reduce the confusion" virou "lowest at the middle resolution, 2.44 cm per pixel, and did not fall further at the finest".
45. 6.1, pistas: a pistola de 0,20 m chamada de armada a 0,50 não apoia a pista de comprimento; reescrito como duas observações a favor do comprimento e uma contra a forma; pose de carregar registrada como candidata na família de 35 m (4.2.2). Idem em 6.5, item 10.
46. 6.1, similaridade: AUC com intervalos que excluem 0,5 nos dois GSDs mais grossos; o 0,67 marcado como do primeiro modelo de 150 m.
47. 6.1, resolubilidade: "não demonstrada" dito como leitura dos pontos de operação, com os fatos (precisão de armada 0,37 a 0,46 no limiar padrão; recall de armada nunca acima de 0,65; taxa de objeto 0,10 ou menos deixa recall de no máximo 0,42), já que nenhum limiar foi fixado antes.
48. 6.2: "73 times less area" ganhou o comparador ("than at the wide setting").
49. 6.3: regra de D-ii lida como atribuição à fração de treino, não como demonstração; "the deficit was not demonstrated to belong to the light".
50. 6.3: "No real aerial benchmark isolates the contrast" (amplo demais; DroneCrowd relata contagem por luz) virou "No real aerial benchmark found reports person detection by illumination".
51. 6.4: "lower bound" dito como do protocolo de pareamento (4.7); o teste carregado-como-arma restrito ao modelo original de 75 m; "the capability carries a false-alarm rate" virou "the partial separation carries ..."; "on a cue other than the firearm" dito como leitura pela regra de 4.6.
52. 6.5: "its ceiling is R" no HERIDAL virou "its reference is R ... not a ceiling"; "intermediate points of the learning curve" virou "the 60- and 90-frame points"; item 6 diz que a seleção do checkpoint de R no conjunto de teste e o cronograma não ajustado puxam em direções opostas, com remissão à 4.7 (a frase "ceiling for the protocol" aparece uma vez só, em 4.7).
53. Terminologia: "new frames" e "between images" viraram "held-out frames" e "between frames".

### Conclusão e declarações (s7)

54. QP1: "camera pitch determines most of that fraction, through the apparent shape" virou "camera geometry ... moves that fraction by the largest factor, consistent with the apparent shape"; fator 4,08 com intervalo (3,44 a 4,64); HERIDAL dito como razão contra o modelo de referência, com a ressalva da leitura por sementes; variedade de assentamento com os fatores 1,74 (oblíquo, pacote) e 1,40 (nadir) e a dispersão 1,4 abaixo do fator dois pré-especificado.
55. QP1, sol duro: "no longer resolvably below the overcast figure" vale para recall; mAP50 fica 6,5 per cent abaixo (0,7422 contra 0,7906); déficit "not shown to belong to the light".
56. QP3: "distances" virou "GSDs"; 25 virou 25,3; "about a quarter" virou 24,5 per cent com a leitura "lowest at the middle one"; d′ marcados como com correção log-linear; frase acrescentada dizendo que nenhum limiar foi fixado antes e dando os pontos de operação; "no similarity device ... separates" virou "separated the classes more weakly than [the detector] did".
57. Parágrafo final: "Showing where a capability is absent, and why" virou "Stating the conditions under which a capability has not been demonstrated", como a contribuição 5 da 1.4.
58. Declarações, Ethics contra Data availability: Ethics dizia que nenhuma imagem do território foi usada e Data availability mencionava a reconstrução fotogramétrica do levantamento de 2022. Agora Ethics diz que nenhuma foi coletada para este estudo, nenhuma entra no gerador, nos corpora ou em medida relatada, e que a reconstrução usada em trabalho exploratório anterior (4.8) está excluída; Data availability diz que a 4.8 declara que a reconstrução não pode ser liberada (a 4.8 declara o fato, não a razão).

### Verificações de integração (27/10)

- Citações: as 104 entradas de s8 são citadas em s1 a s7 e toda citação resolve para uma entrada (conferido com o resolvedor do montador); s8 ficou idêntica à v3. Dois empates do resolvedor numérico do formato JMIS, que já existiam na v3 e não afetam o formato Elsevier: "Chen, Liu, Hu, Zhang, and Pan (2025)" resolve para Hu et al. (2025) e "Pyrrö, Naseri, & Jung, 2021" para Pyrrö (2021). Fica como pendência do montador.
- 13 marcadores FIG e 27 TAB, cada um uma vez, todos os `@fig{}` e `@tab{}` resolvem, todas as remissões "Section x.y" existem, nenhum travessão em s1 a s7 (há um em s8, dentro do título citado da Movisafe, mantido como no original), nenhum [X].
- Números decimais novos em s1, s5, s6 e s7 em relação à v3: todos conferidos em `RESULTADOS.md`, `limiar_armado.md` ou `bootstrap_visdrone_r5.md` (24,5, 12,5 e 25,3 são 0,245, 0,125 e 0,253 em percentual).
- Instrução recebida de "+0,0511 e fator 4,08 em toda parte": não aplicada, porque a fonte pareia +0,0511 com a razão 6,011 (semente 0) e +0,0419 com 4,08 (3,44 a 4,64; média de três sementes), e é assim que s5, s6 e s7 já os trazem.
- Liao et al. (2026), 27,0 pontos: mantido em 2.2 e 6.2; a nota de conferência registra que a Tabela 5 do artigo imprime +27,0 embora as colunas difiram em 24,3. Checar o PDF é pendência do autor.
- PDF Elsevier gerado em `C:\Users\marti\Desktop\MVF_v5_2026-10-27_elsevier.pdf`: 40 páginas, 27 tabelas, 13 figuras, zero "Table ?" ou "Figure ?".

## (b) O que a v4 tinha mudado e NÃO entrou na v5 (decisão do autor de 27/10)

- Enquadramento: leitura do artigo como contribuição à administração pública (literatura de discricionariedade algorítmica e responsabilização: Busuioc, Meijer et al., Selten et al., Afzal e Panagiotopoulos, Alcadipani et al., West e Bowman), model cards, AI Act (Regulation (EU) 2024/1689), o instrumento "acquisition-conditioned capability statement" (6.4 da v4), proposições testáveis, parágrafo administrativo na discussão e na conclusão. Decisão do autor de 27/10.
- Título ("... Acquisition Conditions and the Accountability of Aerial Armed-Person Detection over Synthetic Favelas"), palavras-chave novas, lista de três contribuições, QP1 reescrita ("with apparent target size held matched"), questão secundária de iluminação retirada da QP1, parágrafo de "blind spots" e taxonomia de terreno da 1.2 apagados, 2.4 nova e retitulação de 2.1, 2.3, 3.1, 3.2, 5.6, 6.2 e 6.4. Decisão do autor de 27/10.
- Apêndice online (`apendice-online-v4.md`, 28 páginas): 17 tabelas saíram do texto para lá (params, modelos, visao, pitch, contraste, piloto, teto, nadir, variedade, pr, curva, ajuste, gemeo, gsd150, limiar, heridal e as colunas extras), 10 figuras foram removidas do texto (a v4 ficou com 3 marcadores de figura e 5 de tabela em s1 a s7; o apêndice recebeu 2 figuras e 3 marcadores de tabela, 29 tabelas em markdown). Decisão do autor de 27/10, que pediu ilustração farta do processo.
- Corte de 29,7 mil para 13,5 mil palavras em s1 a s7 (prosa de 20,7 mil para 11,4 mil): 3.1 reordenada e enxugada, 4.x e 5.x reescritas sem vereditos, 6.3 reduzida a cerca de 300 palavras, conclusão de cerca de 420 palavras, legendas de até 40 palavras, lista de referências de 104 para 64 entradas. Decisão do autor de 27/10.
- Padrão post hoc de demonstração em 4.7 (taxa de objeto 0,10 ou menos com recall e precisão acima de metade) e leitura "against the standard set afterwards". Na v5 a 4.7 diz que nenhum limiar foi fixado antes e os pontos de operação são relatados descritivamente. Decisão do autor de 27/10.
- Terminologia única da v4 (S-nadir-150 no lugar de "corpus of record", "share of R" no lugar de "efficacy", "pre-specified" no lugar de "fixed in advance", identificadores H1 a H23, mAP com três casas na discussão, "et al." nas citações de três ou mais autores): mantida a terminologia da v3, definida em 4.5 e 4.7. Decisão do autor de 27/10.
- Itens que dependem do autor e ficaram como na v3: conflito de interesses (relação com a Polícia Civil, acesso às imagens do levantamento), declaração de IA, razão da não liberação do material, coautor delegado, citação da Portaria 4.226/2010, frase sobre concentração de moradores afro-brasileiros.

## (c) Contagens

Palavras contadas por espaço em s1 a s7 (inclui tabelas, legendas e marcadores); prosa exclui linhas de tabela, marcadores e títulos. O resumo da v5 tem 249 palavras.

| Versão | Commit | Palavras s1 a s7 | Prosa | Figuras no texto | Tabelas no texto | Referências | PDF Elsevier |
|---|---|---|---|---|---|---|---|
| v3 (22/10) | 29523f5 | 29.729 | 20.678 | 13 | 27 | 104 | 39 páginas |
| v4 (26/10) | f3bb2cd | 13.458 | 11.366 | 3 (mais 2 no apêndice) | 5 (mais 17 no apêndice) | 64 | 19 páginas (mais 28 do apêndice) |
| v5 (27/10) | não commitado | 30.873 | 21.762 | 13 | 27 | 104 | 40 páginas |

Por arquivo (v3 / v4 / v5): s1 1.485 / 1.269 / 1.512; s2 1.970 / 1.409 / 2.064; s3 1.407 / 731 / 1.428; s4 9.092 / 3.976 / 9.247; s5 10.066 / 2.733 / 10.269; s6 4.664 / 2.524 / 5.051; s7 1.045 / 816 / 1.302. A v5 cresceu 3,8 per cent sobre a v3 porque as correções acrescentam qualificação (intervalos, rótulos de conjunto, leituras no lugar de vereditos) e nada foi cortado.
