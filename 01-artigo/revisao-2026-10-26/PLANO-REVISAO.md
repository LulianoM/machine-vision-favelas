# Plano de revisão de 26/10/2026

Consolidação dos onze pareceres de `PARECERES.md` num único plano de edição para s1 a s7 e para um arquivo novo, `01-artigo/manuscrito/apendice-online.md`. A s8 (referências) será sincronizada depois por script; aqui só se lista o que entra e o que sai. Regras que valem para tudo: nenhum número, citação ou DOI inventado; nenhum número, critério ou limitação se perde (o que sai do texto vai para o apêndice); nenhum caminho de arquivo, script ou nome interno do repositório no manuscrito; nenhum travessão; o revisor 1 (itens E1 a E3, M1 a M5, S1 a S8, C1 a C4, A2, A3 de `feedback-2026-10-14/PLANO-CORRECAO.md`) é respeitado em todos os pontos.

## 1. Decisão de enquadramento

O artigo passa a ser lido como contribuição à Administração Pública sem deixar de ser fiel ao que foi medido. A lacuna deixa de ser "plano contra vertical" e passa a ser: a literatura de discricionariedade algorítmica e responsabilização na polícia estuda como agentes e cidadãos reagem a resultados algorítmicos e toma a capacidade do sistema como dada; para um sistema de percepção, a validade depende da aquisição. A contribuição administrativa é a "declaração de capacidade condicionada à aquisição" (acquisition-conditioned capability statement): o que uma afirmação de detectar pessoa armada do ar precisa declarar para ser verificável antes da compra ou do uso. Ela é dita uma vez na introdução (1.4), situada na literatura em 2.4, argumentada uma vez na discussão (6.4) e fechada na conclusão. Não vira RQ4, porque nada a mediu.

Título adotado (o autor pode voltar ao atual): "Machine Vision from the Global South: Acquisition Conditions and the Accountability of Aerial Armed-Person Detection, Evidence from Synthetic Favelas".

Palavras-chave: algorithmic accountability; street-level discretion; police use of force; aerial object detection; synthetic data; ground sampling distance; dual use; favelas.

Parágrafo de contribuição (texto-base em inglês, adaptado em 1.4):

> The article contributes to public administration and to aerial machine vision. Research on algorithms in policing asks how officers trust, resist or follow algorithmic outputs and takes the capability behind them as given; for a perception system that would inform the judgement on which lethal force turns, capability is a property of the acquisition, not of the algorithm alone. The article proposes the acquisition-conditioned capability statement as the object to which such a system can be held to account before a public body acquires it: a statement of the GSD, camera pitch and illumination at which the capability was or was not shown, the rate at which ordinary objects are called armed there, the imagery on which that rate was measured, and the result that would withdraw the claim. Three measurements on synthetic favelas show why each term is needed: transfer depended on matching the camera geometry of the test imagery and reversed between two benchmarks; a synthetic corpus lowered accuracy once real images existed; and finer resolution did not reduce the rate at which ordinary objects were called armed. At the conditions studied here no claim to detect armed persons from the air is supported.

Perguntas de pesquisa (texto final em inglês):

- RQ1. Trained on synthetic imagery of a dense informal settlement alone, how much of the person-detection accuracy that a reference model trained on as many real images reaches does a detector recover on real aerial benchmarks, and how much do camera geometry, settlement variety and the number of training frames move that fraction, with apparent target size held matched? (Experimento A)
- RQ2. Once a small number of real training images is available (5 or 10 per cent of the benchmark's training split), does the synthetic corpus add accuracy, used as pretraining or mixed into the training set, and does the answer depend on the fine-tuning schedule? (Experimento B)
- RQ3. On synthetic imagery alone, how well does a detector separate a person carrying a firearm from one carrying an ordinary elongated object, and at what rate does it call the latter armed, at GSDs of 4.88, 2.44 and 1.14 cm per pixel? (Experimento C)
- Questão secundária, só sintética: como a detecção varia com a iluminação (Experimento D). Sai do RQ1.

## 2. Conflitos entre pareceres e como foram resolvidos

| Tema | Resolução |
|---|---|
| Taxas de objeto no resumo (24 e 27 por cento de seleção, sem rótulo e de corpora não pareados) | Usar o trio pareado em quadros novos: 25 (1,14), 12,5 (2,44) e 24,5 por cento (4,88). As taxas de seleção ficam só na tabela de três classes, rotuladas |
| Atalho em 4,88 cm/px | A regra pré-registrada fica, mas a premissa passa a ser declarada uma vez em 4.6 com a conta de pixels (fuzil de 0,92 m: cerca de 19 px; pistola de 0,20 m: cerca de 4 px). Fora de 4.6 diz-se "uma pista que não é a forma da arma, não estabelecida"; candidatas: comprimento e, na família de 35 m, a pose de carregar. A pistola a 0,50 em 150 m é dita como evidência de que não é a forma, não como evidência de comprimento |
| Variedade de assentamento | Só o par nadir isola variedade (+0,0054, dentro da dispersão). S-oblique-six contra S-oblique é um pacote de quatro mudanças e é relatado assim em 4.6, 5.2, tabela de hipóteses, 6.1 e 7 |
| "Pitch determina a maior parte" | Vira "a geometria da câmera (pitch com altitude, filtro de colocação e GSD que mudam junto) moveu a fração pelo maior fator"; a explicação por forma passa a "consistente com", não "através de" |
| Sol duro | Regra de D-ii mantida; leitura: "o déficit não foi mostrado ser da luz; o especialista recuperou a maior parte (D-i)". Nada de "pertence à fração de treino" |
| HERIDAL | 62,7 contra 42,1 por cento é razão contra R, que ali é modelo de referência e não teto; dizer que não passa na leitura por sementes e que o cenário é mata, não cidade. "Teto" fica reservado a R no VisDrone |
| Similaridade de recortes | "Separou fracamente, menos que o detector", não "não separou"; intervalos de AUC excluem 0,5 a 2,44 e 4,88; limites corrigidos para -0,030 a +0,032; a célula de d′ do detector a 150 m é marcada como do primeiro modelo de 150 m, que falhou a condição de validade |
| Taxa de objeto como dano | Deixa de ser "estimativa" e "limite inferior" de dano real. 6.4 usa a precisão da classe armada lida contra a prevalência fixada pelo gerador |
| Status das hipóteses | Três rótulos: confirmatória (hipótese e critério fixados antes de qualquer resultado naquele conjunto de teste), seguimento pré-especificado (hipótese formada em resultado anterior no mesmo conjunto, critério fixado antes) e exploratória. Valor p só onde o critério foi fixado nele (McNemar; réplica em quadros novos de 35 contra 75 m), com a nota "sem correção para agrupamento por quadro" |
| S-oblique-six como melhor de quatro no mesmo teste | Declarado em 4.6 e em 6.5; HERIDAL é a verificação independente |
| Tabela panorâmica (visao) | Vai inteira para o apêndice (Tabela C1), com as linhas F corrigidas para médias de três sementes. No texto, a Tabela de Experimento A (obliquo) e a de Experimento B (cronograma) cobrem o que ela mostrava |
| Fontes da PAR | Seis no texto: Busuioc, Meijer et al., Selten et al., Afzal e Panagiotopoulos, Alcadipani et al., West e Bowman. As demais ficam de fora (ver seção 9) |
| 6.3 (aquisição) | Encolhe para cerca de 300 palavras; mantém National Geodetic Survey (2002), RICS (2021), Maes (2025) e Dandois et al. (2015); o resto das fontes de prática sai |
| Conclusão sobre "ausência" de capacidade | "Não demonstrada nas condições estudadas", nunca "ausente" |

## 3. Terminologia única (vale para s1 a s7 e para o apêndice)

- S-nadir-150 é o nome do corpus de 150 m; "corpus of record" aparece uma só vez, entre parênteses, na definição em 4.3.
- "selection split" para todo conjunto que escolhe checkpoint (inclusive o de corpora sintéticos); "held-out frames" para quadros renderizados depois do treino; "VisDrone-DET" na primeira menção e "VisDrone" depois; "HERIDAL"; nunca "the benchmark" quando houver ambiguidade.
- "ceiling" só para R no VisDrone. No HERIDAL, "reference model R". A razão mAP50 do modelo sobre mAP50 de R no mesmo teste chama-se "share of R" (definida uma vez em 4.7); some "efficacy" e "transfer fraction". Na prosa pode-se dizer "per cent of the ceiling" apenas para o VisDrone.
- "reference acquisition": nadir, 4,88 cm/px, isto é, render 3840 x 2160 a 150 m, igual à câmera de referência (Zenmuse Z30) com zoom de 2x. Sem zoom a Z30 dá 9,71 cm/px a 150 m.
- "object rate" (taxa de objeto chamado de arma); "false-alarm rate" sai.
- Classes: armed, unarmed, object. Modelos de três classes: S-nadir-75, S-nadir-35, Twin-75, Twin-150 (definidos em 4.6).
- "pre-specified" no lugar de "fixed in advance" e "fixed before the run".
- GSD nunca é "distance".
- YOLO11 (não YOLOv11).
- Convenção de sinal: diferença = modelo em teste menos referência, dita uma vez em 4.7. Razões com duas casas (6,01; 1,87). mAP50 com quatro casas só nas tabelas; na discussão, conclusão e resumo, três casas ou percentual de R.
- Números de um a nove por extenso quando não são dado medido.
- "against" só para modelo contra modelo; variar conectores (E3).
- Siglas definidas uma vez: GSD, UAV, mAP, mAP50, IoU, AUC, GNSS, PVC, DN, SD.

## 4. Orçamento de palavras (prosa, sem tabelas e legendas)

| Arquivo | Hoje (total com tabelas) | Meta de prosa |
|---|---|---|
| s1 (resumo e introdução) | 1.485 | 1.200 (resumo até 270) |
| s2 | 1.970 | 1.450 (com a 2.4 nova) |
| s3 | 1.407 | 850 |
| s4 | 9.058 | 3.500 |
| s5 | 10.066 | 2.800 |
| s6 | 4.664 | 2.800 (com o parágrafo administrativo) |
| s7 (conclusão e declarações) | 1.045 | 800 (conclusão até 420) |

Total de prosa perto de 13.400 palavras. Legendas com até 40 palavras cada, remetendo a 4.7 em vez de repetir o protocolo.

## 5. Tabelas e figuras

Ficam no texto dez tabelas (chaves mantidas): `gsdzoom`, `corpora` (absorve `modelos`), `rq` (com identificadores H1 a H23 e coluna de modelos) em s4; `forma` (absorve `gsd`), `similaridade` (sem coluna PCA/LDA), `obliquo` (Experimento A; absorve `teto`, `nadir`, `variedade`, `heridal`), `cronograma` (Experimento B; absorve as linhas principais de `ajuste` e F-joint), `armado` (dois painéis, seleção e quadros novos; absorve `gsd150` e as linhas pareadas de `gemeo`), `regimes` (com colunas de contraste) e `hipoteses` (identificador, rótulo curto, status, resultado, leituras) em s5.

Saem do texto e vão para o apêndice: `params` (B1), versão completa de `corpora` e papéis de `modelos` (B2), `visao` corrigida (C1), `pitch` (C2), `contraste` (C3), `piloto` (C4), colunas extras de `teto`, `nadir`, `variedade` (C5), `obliquo` por semente e comparações da semente 0 (C6), `pr` (C7), `curva` (C8), `ajuste` por semente (C9), `gemeo` e `gsd150` completas (C10), `limiar` com as 14 combinações (C11), similaridade completa (C12), taxas por arma e por objeto (C13).

Remissões: no texto, todo `@tab{}` de chave removida vira a chave que a absorveu (`visao` para `obliquo` ou `cronograma`; `heridal`, `teto`, `nadir`, `variedade` para `obliquo`; `gsd` para `forma`; `gsd150` e `gemeo` para `armado`; `contraste` para `regimes`; `modelos` para `corpora` ou `rq`; `ajuste` para `cronograma`) ou vira texto literal "Online Appendix, Table Cn".

Figuras no texto (nove): fig1_nadir, fig2_climas, fig8_nadir_obliquo, fig9_desenho_experimental, fig7_armados, fig13_similaridade, fig10_ajuste_fino, fig11_pr_visdrone, fig12_limiar_armado. Vão para o apêndice: fig3_beco (Figura B1), fig6_assentamentos (B2), fig5_anotacao (B3), fig4_dataset (B4). Redesenhar fig9 com o HERIDAL é tarefa separada do desktop; até lá a legenda continua honesta.

## 6. Identificadores das hipóteses (comuns a `rq` e `hipoteses`)

H1 R válido. H2 fração recuperada e verificação de escala. H3 geometria (S-oblique contra S-nadir-150). H4 inversão no HERIDAL. H5 variedade de assentamento no nadir. H6 pacote oblíquo (S-oblique-six contra S-oblique, quatro mudanças). H7 dispersão por semente de cena. H8 152 contra 30 quadros. H9 fim da curva (152 contra 120). H10 ordem por iluminação. H11 déficit do sol duro intrínseco à luz. H12 pré-treino sintético acrescenta. H13 custo robusto ao cronograma. H14 treino conjunto acrescenta. H15 conjunto contra início sintético. H16 armas não vistas (biblioteca de assets). H17 objeto carregado como arma (McNemar). H18 validade em 4,88. H19 separação em 4,88. H20 4,88 contra 2,44 em quadros novos. H21 1,14 contra 2,44 em quadros novos (taxa de objeto). H22 taxas de armado e desarmado, 35 m contra gêmeo. H23 35 m contra o 75 m original (exploratória).

## 7. Instruções por arquivo (resumo; o texto completo em inglês vai a cada editor)

**s1.** Título e palavras-chave novos. Resumo reescrito (cerca de 260 palavras) com: drones já sobre território policiado e bases de imagem com armas montadas para polícia (CNN, 2026; Faheem et al., 2025; AlJundi et al., 2025); a afirmação como especificação verificável; 4,88 cm/px como "150 m, ou a câmera de referência com zoom de 2x"; 2,2 e 15,3 por cento; HERIDAL 62,7 contra 42,1 por cento "do modelo de referência", com a ressalva da dispersão; o corpus sintético piorou com 5 ou 10 por cento de dado real; trio de quadros novos 25, 12,5 e 24,5 por cento; frase final administrativa. Em 1.1: premissa com fonte, condição de aquisição com três termos, apagar o parágrafo dos "blind spots", parágrafo novo de discricionariedade (Selten et al.; Afzal e Panagiotopoulos; Busuioc), parágrafo do Sul Global reescrito. 1.2 trocada pela lacuna das três literaturas (com a frase da "figura em pé"), apagando a taxonomia de terreno. 1.3 com o objetivo e as RQs da seção 1, Experimento D como questão secundária, frase sobre confirmatório e exploratório, frase "as respostas são medições; a implicação é argumentada em 6.4". Apagar a frase sobre Jacarezinho e a frase sobre morfologia. 1.4 com três contribuições (empírica, metodológica, administrativa) e roteiro curto. No máximo uma remissão por parágrafo.

**s2.** Frase de abertura que mapeia quatro literaturas às RQs. 2.1 retitulada "Aerial policing and machine vision in informal settlements", em cerca de 230 palavras, com "et al." e sem Jiang et al. (2026); corrigir a frase que nega a integração vertical. 2.2: domain randomisation sem os números de Horváth; definição de IoU sai para 4.7; VisDrone apresentado na primeira menção; apagar a frase "objetos que ocupam grande parte do quadro"; conferir a frase marítima de Kiefer et al. contra a nota conferida ou apagá-la; parágrafo de mecanismos em uma frase; origem de 2022 em uma oração com remissão aos Agradecimentos. 2.3 retitulada "Scale, illumination and weapon detection from the air"; passo de 8 pixels sai para 4.4; corta a frase do rastreador e a de especificações de levantamento; busca de bases de armas descrita (setembro de 2026, sem busca de texto completo em IEEE Xplore, Scopus ou Google Scholar), com "none we found"; atalho com Geirhos et al. (2020) se o DOI for confirmado. 2.4 nova: "Algorithmic discretion and accountability in policing" (cerca de 200 palavras, seis fontes da PAR). 2.5 (antiga 2.4): quatro achados corretos (4,9 a 23,2 por cento em Kiefer et al.; Liao et al. com valores de coluna; sinal contestado do pré-treino; material de armas a 2 a 8 m) e quatro aberturas ligadas a RQ1, RQ2, RQ3 e à responsabilização.

**s3.** Parágrafo de status (pano de fundo, fontes públicas, nada coletado) no início da seção. 3.1 retitulada "Lethal force, its oversight and aerial systems in Rio de Janeiro", cinco parágrafos (letalidade; ADPF 635; Operação Contenção; drones dos dois lados; controle territorial e a premissa da linha de visada), só com fatos já presentes; saem a série da cidade, veículos e mandados, reações, 699, críticos, 1979 e Ilha Grande, mapas de rotas. 3.2 retitulada "Jacarezinho as the motivating case", com censo e faixa de estimativas, sem "steep slopes" e sem o parágrafo final. 3.3 com discricionariedade de rua (Alcadipani et al.; Afzal e Panagiotopoulos), assimetria dos erros ("withholds a warning"), confirmação (Selten et al.) e responsabilização (Busuioc); a frase jurídica suavizada ("a central category in decisions to use lethal force"); apagar o parágrafo 2. "Civil Police" padronizado.

**s4.** 4.1 com o enquadramento de auditoria anterior à adoção, parágrafos 2 e 3 fundidos, origem na proposta de 2022 de um perito da Polícia Civil (fato já nos Agradecimentos) e a frase sobre o trabalho fotogramétrico exploratório que não entra no artigo. 4.2 com citação de software; 4.2.1, 4.2.2 e 4.2.3 enxutas, parâmetros para B3 e B6; corrigir em 4.2.2 a afirmação não verificada sobre malhas, definir "recorded length" e corrigir a frase das poses (família de 35 m difere por classe; quatro pistas; o teste de carregar como arma cobre só o 75 m original). 4.2.4 com a tabela `gsdzoom` reestruturada, definição de "reference acquisition", frase do render 4K corrigida, "1.25 times". 4.2.5 com a frase da figura descartada só se confirmada no código. 4.3 com a tabela `corpora` fundida com `modelos`, comparação de instâncias de R (18.858 contra 4.678), HERIDAL "duas a três vezes mais fino". 4.4 retitulada "Characterisation of the target without a trained detector", quatro propriedades, similaridade em um parágrafo curto, ressalva do contraste medido no piloto. 4.5 com abertura nova, seleção de R no teste dita só aqui, "conservative" corrigido (viés líquido de direção desconhecida). 4.6 com identificadores, desenho sem critérios (critérios só na `rq`), Experimento A em A1 a A4 com a declaração do pacote e do melhor de quatro, razão de mistura no B, lista do que mudou entre o 75 m original e o 35 m, premissa geométrica de 4,88, remédios do Twin-150 fixados antes, Experimento D como secundário com leitura honesta de D-ii, três rótulos de status. 4.7 com "share of R", convenção de sinal, correção log-linear explícita, status do valor p. 4.8 sem a promessa de reproduzir o gerador.

**s5.** Abertura nova. 5.1: tabela `forma` absorve `gsd` (com as linhas de 75 e 35 m), uma frase do pitch, contraste resumido com remissão a `regimes`, similaridade reescrita com os limites corretos e a célula de 150 m marcada; fig7 vai para o início da similaridade. 5.2: piloto vira uma frase em 5.1; teto, nadir e variedade viram frases e linhas da `obliquo`; apagar a corrida interrompida; verificação de escala, oblíquo (pacote), HERIDAL e curva reescritos sem veredictos (que ficam na `hipoteses`); comparações da semente 0 para C6. 5.3: `cronograma` absorve `ajuste`; dois parágrafos; PR vai para o fim de 5.3. 5.4 reordenada (2,44; 1,14 contra 2,44; 4,88; limiar), `armado` em dois painéis, frase de precisão e prevalência (se conferida), sinais corrigidos, valores p só em H17 e H21. 5.5 com nuance da iluminação e sem a frase zero-shot do especialista (vai para C3). 5.6 com a robustez de IoU consolidada e `hipoteses` enxuta, com as correções de linha (iluminação, sol duro, H22, rótulos sem jargão, H6 como pacote).

**s6.** Parágrafo de abertura com as três respostas em linguagem simples. 6.1 só interpretação: RQ1 (geometria, variedade isolada só no nadir, forma consistente com a inversão, comparação com Kiefer et al. em ordem de grandeza), RQ2 (com Hinterstoisser, Tremblay e Mensink), RQ3 (não demonstrada; comprimento e pose como pistas; similaridade fraca; parágrafo de resolubilidade apagado). 6.2 retitulada "Geometry as a design variable", sem ranquear contra fotorrealismo. 6.3 em cerca de 300 palavras, remissão corrigida para 4.1. 6.4 retitulada "Dual use and accountability: the object rate as a term of the capability claim", com taxa de objeto que não estima dano, precisão contra prevalência, os dois testes em uma frase cada e o parágrafo administrativo. 6.5 com dez itens curtos (inclui um só detector, multiplicidade, ausência de limiar de d′, prevalência, pose, R com mais instâncias e cronograma não ajustado, S-oblique-six melhor de quatro). 6.6 com as bases nadir só aqui, sem "which is itself a finding", e as perguntas administrativas em aberto.

**s7.** Conclusão reescrita (cerca de 420 palavras) com rótulos RQ1 a RQ3, frase de escopo, frase administrativa (Busuioc) e o fecho atual. Declarações: ética sem contradição com a reconstrução fotogramétrica; dupla utilização remetida a 6.4 e 4.1; apagar a frase redundante do financiamento. Conflito de interesse, IA e motivo da não liberação ficam como estão até o autor decidir (seção 8).

## 8. Pendências do autor (não aplicar sem confirmação)

- A3, motivo da não liberação do gerador, corpora e pesos: a disponibilidade de dados precisa dizer por quê (revisor 1, C4). Sugestão a confirmar: risco de uso dual de um corpus pronto de pessoas armadas.
- A4, declaração de IA: três pareceres apontam que ela descreve menos do que o projeto registra (código do gerador, análises, rascunhos com Claude Code). Texto sugerido no parecer R7; decisão do autor.
- A5, conflito de interesse e coautor: a origem na proposta de um perito da Polícia Civil passa a ser dita em 4.1 (fato já nos Agradecimentos); a frase "nenhum autor tem vínculo com a instituição" e a declaração de conflito dependem do autor. Também o nível de detalhe sobre o voo de referência de 2022.
- Declaração de contribuições (CRediT): papéis a confirmar.
- Ler as seis fontes da PAR antes de submeter: as caracterizações do plano seguem os resumos conferidos no levantamento de 20/10 e no OpenAlex.
- Ano de Busuioc (online 2020, número 81(5) de 2021) e de Alcadipani et al. (online 2023, número 2024): usar o ano que o Crossref der para o fascículo, uma forma só em todo o texto.
- Liao et al. (2026), Tabela 5: o ganho impresso (+27,0) não bate com a diferença das colunas (74,5 menos 50,2 = 24,3). O texto passa a citar os valores de coluna; conferir no PDF.

## 9. Referências para a sincronização da s8

Entram (DOI conferido no levantamento de 20/10, reconfirmar no Crossref): Busuioc, M. (10.1111/puar.13293); Meijer, A., Lorenz, L., & Wessels, M. (2021, 10.1111/puar.13391); Selten, F., Robeer, M., & Grimmelikhuijsen, S. (2023, 10.1111/puar.13602); Afzal, M., & Panagiotopoulos, P. (2025, 10.1111/puar.13957); Alcadipani, R., Lotta, G., & Cohen, N. (10.1111/puar.13670); West, J. P., & Bowman, J. S. (2016, 10.1111/puar.12506).

Entram só se o DOI for confirmado no Crossref (sem confirmação, a frase fica sem citação): Geirhos et al. (2020), "Shortcut learning in deep neural networks", Nature Machine Intelligence; Lin et al. (2014), Microsoft COCO. Software citado sem DOI salvo verificação: Ultralytics YOLO11, Blender, MakeHuman e MPFB, Poly Haven.

Saem se ficarem órfãs: Jiang et al. (2026); Al Jazeera (2021); Barros (2026); Causa Operária (2025); CBS News (2025); Gazeta do Povo (2025); OPEB (2025); Misse (2011); ISP-RJ (n.d.-b), com ISP-RJ (n.d.-a) passando a (n.d.); Caminhos Languages (2025); IBGE (n.d.) se não for mais citado; Pix4D; Leitão et al. (2016); GeoCue (2025); DECEA (2026); Slade et al. (2025); Broyles et al. (2022). O script de sincronização decide pela presença no texto final. JOTA (2025): trocar o endereço do espelho pelo do próprio JOTA, se encontrado.

## 10. Apêndice online

Arquivo novo `01-artigo/manuscrito/apendice-online.md`, em inglês, montado a partir da versão comprometida antes desta revisão (`git show HEAD:...`), para não depender da ordem das edições. Seções A (contexto), B (métodos) e C (resultados suplementares), mais figuras B1 a B4. Rótulos literais ("Table B1", "Figure B2"), sem marcadores `TAB` e `FIG`, porque o montador não lê esse arquivo. Nenhum caminho do repositório, nenhum número novo; a Tabela C1 recebe as linhas F corrigidas a partir de `bootstrap_visdrone_r5.md`.

## 11. Ordem de execução e verificação

1. Sete editores em paralelo (s1 a s7) e um para o apêndice, cada um com as instruções completas.
2. Integrador: conferir remissões `@tab{}`, `@fig{}` e de seção; varrer travessões; contar palavras por arquivo contra a seção 4; rodar o script de números (`nums.py` do rascunho da sessão) para confirmar que todo número do manuscrito de 22/10 está no texto ou no apêndice; montar o PDF no formato JMIS e medir páginas.
3. Sincronizar s8 por script.
4. Atualizar `STATUS.md`, `DIARIO.md` e `PENDENCIAS.md` com as pendências da seção 8; commit e push.

## 12. Achados não adotados

- RQ4 sobre responsabilização: nada a mediu (revisor 1, M1).
- Fontes da AMJ: o próprio levantamento classifica a aderência como muito baixa.
- Anastasopoulos (2026), Gao e Riccucci (2026), Degli Esposti et al. (2021), Jennings e Rubado (2017), Selten et al. (2026), Headley et al. (2025): ponte fraca, resumo não lido ou orçamento; podem voltar numa versão para a PAR.
- Títulos "Checking a Capability Before It Is Believed", "Before a Drone Calls Someone Armed" e similares: perdem a marca do projeto.
- Análises novas (R no último epoch, contraste refeito no S-nadir-150, medir as malhas no Blender, recomputar d′ e o suplemento a 150 m com o modelo válido, redesenhar fig9): não cabem numa revisão de texto; ficam como tarefas opcionais do desktop. Até lá o texto declara a limitação (malhas: a frase sai; contraste: ressalva; 150 m: célula marcada).
- Afirmar "cada fator acrescentou seis pontos e meio do teto": o ganho de S-oblique-six é de um pacote, não de variedade.
- Atribuir o limiar de 30 por cento ao revisor.
- Balanceamento de lotes no treino conjunto: não confirmado; entra só a razão de mistura, derivada das contagens.
- Frase sobre a concentração de moradores afro-brasileiros em 3.3: não acrescenta ao argumento.
- Citar a norma de uso da força (Portaria 4.226/2010): não conferida; a frase é suavizada.
- Usar o projeto de 2022 como prova de que "se propõe" a detecção: substituído por Faheem et al. e AlJundi et al.
- Reescrever agora a declaração de IA, o conflito de interesse e as contribuições: decisões do autor (seção 8).
- Apagar a tabela panorâmica ou o piloto: ambos vão para o apêndice, não somem.
