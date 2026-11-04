<!-- Nota de trabalho que ocupava a página 1 dos PDFs da versão curta. Retirada dos HTMLs em 2026-11-04 à noite a pedido do autor, depois de tomadas as decisões; fica aqui como registro. -->

# NOTA DE TRABALHO (não faz parte do manuscrito; apagar antes de submeter)

**O que é isto.** Versão curta (2026-11-04) do artigo para a 7th AI in Management Conference (AIM 2027, USC Marshall, 19 e 20 de março de 2027), feita a partir do manuscrito inglês v9. Alvo combinado com Felipe em 2026-11-03: corpo entre 8 e 9 mil palavras (a professora indicou cerca de 10 mil; os quatro papers premiados em 2026 têm mediana de 10,5 mil palavras e 37 páginas). Prazo de submissão: **19/11/2026**, pelo formulário do dossiê (`08-conferencia/README.md`). Formato principal: o do periódico (A4, duas colunas, Times 9,5 pt), arquivo `versao-curta-elsevier.html`, montado por `gera_elsevier.py` a partir de `versao-curta-aim2027.html`, que é onde o texto se edita. A mesma versão no formato dos premiados da AIM (Carta, Times 12, espaço duplo) e o extended abstract de 3 mil palavras continuam na pasta; `pagina.py` fecha os buracos de paginação e `gera_pdf.sh` renderiza os três.

**Contagem.** Corpo (seções 1 a 7, sem resumo, tabelas, legendas, declarações e referências): 8.728 palavras; com legendas e tabelas, 12.056; resumo, 363; declarações, 444; 80 referências, todas citadas; 12 tabelas e 5 figuras. PDF no formato Elsevier: 17 páginas mais esta nota; no formato dos premiados da AIM (Carta, espaço duplo): 41 páginas de manuscrito; extended abstract: 19 páginas.

**O que foi cortado do v9 (24 mil palavras no corpo em inglês).** O corpo ficou em cerca de 36% do v9, com os números essenciais, 12 tabelas e 5 figuras; nenhum número foi alterado, e tudo o que está aqui está no v9, exceto as medidas de 04/11 citadas abaixo. Mudanças de estrutura, para quem for comparar: a seção 2.4 saiu; a antiga 3.4 (base ética da síntese) virou uma frase em 4.1 e a antiga 3.5 passou a ser a 3.4; a 5.6 (robustez) virou uma frase na abertura da seção 5; a 6.1 perdeu o parágrafo de síntese das três questões. As referências cruzadas foram atualizadas. Cortes de conteúdo: as tabelas de hipóteses e de robustez viraram prosa; a análise de similaridade de recortes saiu; curva de aprendizado, semente de assentamento, piloto e verificação de escala ficaram em uma frase cada; saíram as tabelas de ângulo de inclinação, contraste, precisão e revocação e pontos de operação; os parâmetros de treino viraram nota da Tabela 3; 6.2, 6.3, limitações e trabalhos futuros ficaram em um parágrafo cada. Três números não estão no v9 e foram medidos no desktop em 04/11 (itens 1 e 2 da lista do servidor; origem e comando em `06-resultados/RESULTADOS.md`, entrada de 04/11): as duas células da Tabela 5 com a fração sub-stride dos corpora oblíquos (0,9% e 3,9%) e o parágrafo da 5.1 sobre a largura das armas em pixels (fuzil 22 por 1 px a 150 m). Quando o texto condensado perdeu uma nuance que importa, o lugar de recuperá-la é o v9.

**Simulações em curso no desktop (04/11).** A rodada 6 foi lançada em 04/11 às 11:48 com os itens 3 a 9 da lista do servidor (teto R com seleção fora do teste, orçamento igual nos três modelos da QP3, atalho de comprimento, sol duro com sementes, ruído e borrão, arma na mão e teto completo); previsão de término entre 13 e 15/11, uma semente de cada item até 08/11. O que terminar antes de 19/11 entra no texto com o número conferido em `06-resultados/RESULTADOS.md`; o que não terminar fica para o periódico. A lista completa, com custos, está em `O-QUE-FALTA-NO-SERVIDOR.md`.

**Decisões tomadas em 04/11 (Felipe).**

  1. **Título:** fica o (A), usado aqui: "Machine Vision from the Global South: Synthetic Training, Acquisition Limits and What an Aerial Claim of an Armed Person Must Declare".

  1. **Figuras:** as cinco ficam (Fig. 1 = fig. 8 do v9, nadir contra oblíquo; Fig. 2 = fig. 9, desenho experimental; Fig. 3 = fig. 7, três GSDs; Fig. 4 = fig. 10, ajuste fino; Fig. 5 = fig. 12, varredura de limiar). Não cortar figura para ganhar página.

  1. **Trilha do CFP:** "Applications of Natural Language Processing or Machine Vision".

**Ordem até 19/11.** (1) Felipe lê e marca este PDF. (2) Entram os resultados da rodada 6 que terminarem, com o número conferido em `06-resultados/RESULTADOS.md`. (3) Orientador revisa. (4) Leitura final: nenhum travessão, nenhum caminho de arquivo, todos os números batendo com o v9 ou com `RESULTADOS.md`. (5) Apaga esta página, gera o PDF e submete na trilha de Machine Vision.


---

<!-- Nota de trabalho que abria o extended abstract de 3 mil palavras (esqueleto-aim2027.html), retirada na mesma data. -->

# NOTA DE TRABALHO (não faz parte do manuscrito; apagar antes de submeter)

**O que é isto.** Esqueleto da versão curta em inglês para a 7th AI in Management Conference (AIM 2027, USC Marshall, 19 e 20 de março de 2027). Prazo de submissão: **19/11/2026**, pelo formulário do dossiê (`08-conferencia/README.md`). Formato copiado do extended abstract premiado em 2026: Carta, margens de 1 pol., Times New Roman 12, espaço duplo, rótulo "Extended Abstract". Tabelas, legendas e referências em espaço simples para caber. Gerado em 2026-11-03 a partir do manuscrito inglês v9 (seções s1 a s7 do repositório). Fonte editável: `esqueleto-aim2027.html` na mesma pasta; PDF regenerado por `gera_pdf.sh`.

**Como ler as marcas.**

  1. **Texto normal**: prosa condensada do v9, nas palavras dos autores. Todo número foi copiado do v9 e conferido com ele; nada foi medido de novo. Os reenquadramentos novos (ganhos absolutos em vez da razão 4,08; a U da QP3 lida com o orçamento; D-ii como "não demonstrado"; a condição em quatro itens) usam só números que já estão no v9.

  1. [[NEW: ...]] em amarelo: conteúdo que não existe no v9 e precisa ser escrito, medido ou verificado antes de entrar. São 6 itens (ver tabela).

  1. [[DECIDE: ...]] em azul: decisão dos autores, sem trabalho novo.

  | # | Item novo | Onde | Custo |

  | 1 | Afiliação completa, e-mails, ORCID | cabeçalho | minutos |

  | 2 | Pegada da arma em pixels: o comprimento está derivado (comprimento registrado dividido pelo GSD); a largura das malhas não está no v9 e precisa ser lida no gerador (desktop) antes de qualquer número ser impresso | Seção 4 | 1 h, sem GPU |

  | 3 | Fração sub-stride (lado menor < 8 px) dos dois corpora oblíquos, que o v9 não mede (Tabela 7 do v9 só tem linhas nadir e VisDrone). Só rótulos, sem GPU | Tabela 1 | 1 h, sem GPU |

  | 4 | Casos documentados de objeto cotidiano tomado por arma em operação no Rio (guarda-chuva, furadeira etc.), com fonte verificável; sem fonte, cortar a frase | Seção 6 | 2 h de busca |

  | 5 | Opcional: ablação de ruído, blur e JPEG no teste zero-shot (uma frase em Limitações). Sem ela, o texto fica como está | Seção 7 | 1 dia de GPU |

  | 6 | Contagem final de palavras e páginas depois da revisão dos autores | tudo | minutos |

**Decisões pendentes.**

  1. **Título.** Usado aqui (A): "Machine Vision from the Global South: Synthetic Training, Acquisition Limits and What an Aerial Claim of an Armed Person Must Declare". Mantém a marca, tira "dense favelas" do título porque nada foi medido numa favela. Alternativas: (B) "Before the Alert Is Believed: Acquisition Limits of Synthetic-Trained Armed-Person Detection for Aerial Policing"; (C) "Conditions Under Which a Capability Has Not Been Shown: Synthetic Data, Acquisition Geometry and the Aerial Armed-Person Claim".

  1. **Figuras.** Duas incluídas: Fig. 1 = fig. 7 do v9 (o que o detector recebe nos três GSDs) e Fig. 2 = fig. 10 (ajuste fino). A fig. 8 do v9 (nadir contra oblíquo) ilustra o achado de geometria e cabe como Fig. 1b se sobrar página.

  1. **Parágrafo de iluminação** (fim da Seção 5): é o resultado mais fraco e custa um terço de página. Manter, reduzir a uma frase ou cortar.

  1. **Rodar GPU antes de 19/11**: só o item 5 acima exige. Recomendação: fazer os itens 2 e 3 (sem GPU) e deixar o 5 para o periódico.

  1. **Trilha do CFP**: "AI Ethics, Bias, and Discrimination" ou "Applications of Natural Language Processing or Machine Vision". O texto como está pende para a primeira.

**Contagens deste PDF** (medidas na geração): ver o relatório da sessão; a meta é 8 a 12 páginas de manuscrito sem contar esta nota. Se precisar cortar: Seção 2 pela metade, parágrafo de iluminação, segundo parágrafo da Seção 7.

**Ordem sugerida até 19/11.** (1) Felipe lê e marca este PDF. (2) Decide título, figuras, trilha. (3) Itens 2 e 3 da tabela no desktop. (4) Escreve os [[NEW]]. (5) Orientador revisa. (6) Leitura final: nenhum travessão, nenhum caminho de arquivo, todos os números batendo com o v9. (7) Apaga esta página, gera o PDF e submete.
