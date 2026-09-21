# Pendências do rascunho v2 (Irigaray, 2026-09-10)

Tudo abaixo foi verificado no texto em 2026-09-17, com busca automática nos arquivos de `manuscrito/`. Marcar `[x]` ao resolver e anotar o commit.

## A. Estrutura

- [x] A1. "Conclusion" não conclui: só contém Limitations, Delimitations e Implications and Directions for Future Research. Falta o parágrafo de fecho (`07-conclusion.md`).
- [x] A2. A introdução não tem título de seção (`01-introduction.md`).
- [ ] A3. Remissões a seções numeradas que não existem. O texto não numera as seções, mas cita "Section 2", "3", "4", "5", "6" e "7" em dez pontos, e a numeração implícita não bate com a ordem atual (a revisão de literatura é a segunda seção e é chamada de "Section 4"). Ocorrências: `02-literature-review.md` linha 11; `03-methodology.md` linhas 3 e 13; `06-results-proposed-model.md` linhas 5, 6 e 7; `07-conclusion.md` linhas 5, 17, 21 e 29. Decidir: numerar as seções e corrigir, ou trocar por remissão nominal.
- [ ] A4. Trecho repetido quase literalmente: o parágrafo das "two bodies of literature that rarely intersect" aparece na introdução e de novo em "Positioning this study" na revisão. A descrição de Gevaert et al. (2016) em Kigali também aparece duas vezes. Manter um e remeter ao outro.
- [x] A5. Não há abstract nem palavras-chave.

## B. Referências

> **Rodada de 2026-09-20 [DESKTOP].** B1 fechado PELA METADE, e a metade que ficou aberta é
> deliberada. A busca no Crossref por sobrenome e ano devolveu correspondência para as 13, mas
> comparando o TÍTULO devolvido com a frase que cita a obra, só 8 correspondem de fato. Um
> exemplo do que a conferência evitou: "Xu (2025)" é citado no texto comparando RRT, ACO e A*
> para planejamento de rota, e a busca por sobrenome e ano devolveu um artigo de sensoriamento
> remoto. Inserir aquele DOI teria fabricado uma citação. As 7 restantes (Chen et al. 2025, Xu
> 2025, Jiang et al. 2026, Wang e Qian 2026, Yan, Hsieh e Lai 2025, Horváth et al. 2023, Watson
> e Elliott 2025) dependem de quem escreveu a frase dizer qual obra é. Ferramenta em
> `01-artigo/ferramentas/busca_crossref.py`.

- [ ] B1. Treze obras citadas no texto sem entrada na lista: Chen, Liu, Hu, Zhang e Pan (2025); Rasoulie e Pashazadeh (2026); Xu (2025); Agrawal, Ratnoo e Ghose (2017); Jiang et al. (2026); Wang e Qian (2026); Yan, Hsieh e Lai (2025); Gevaert, Persello, Sliuzas e Vosselman (2016); Du, Xing, Wang, Wei e Zhang (2024); Barisic, Petric e Bogdan (2022); Horváth et al. (2023); Watson e Elliott (2025); da Silva, Kormann da Silva e Westerholt (2024). Localizar cada uma e conferir o DOI no Crossref antes de incluir. Nunca inventar DOI.
- [x] B2. Entrada "[Slovo Park study] (2025)" está sem autores. No texto a obra é citada como Sithole e Mhangara (2025). Completar.
- [ ] B3. Wikipedia citada três vezes como fonte ("Wikipedia, 2026" duas vezes e "Wikipedia, 2025a", em `04-situating-the-study.md`) e sem entrada na lista. Substituir por fonte primária.
- [ ] B4. Amnesty International é mencionada no texto sem referência. A entrada da Inter-American Commission on Human Rights (2021) está na lista e não é citada no texto.
- [ ] B5. Há duas entradas de Human Rights Watch de 2021 e o texto cita só "Human Rights Watch, 2021". Diferenciar como 2021a e 2021b.
- [ ] B6. A entrada "CNN Brasil (2026a)" aponta para uma URL do site Defesa em Foco, a mesma da entrada "Defesa em Foco (2026)". Conferir qual é a fonte real.
- [ ] B7. "Ad Infinitum (2023)" provavelmente não é autor. O slug da URL (`brazil-tries-reclaim-rio-favelas-ad-infinitum`) indica que "Ad Infinitum" é o fim da manchete do InSight Crime. Abrir a página, identificar o autor e corrigir a entrada e as quatro citações no texto.
- [ ] B8. A lista mistura dois formatos: sete entradas em lista numerada, sem padrão APA completo, seguidas de entradas APA em ordem alfabética. Unificar.
- [ ] B9. O título da nota do Small Wars Journal de 2025 fala em 132 mortos e o texto usa 121 a 122 (número oficial). Deixar explícito no texto de onde vem cada número.
- [ ] B10. Fontes jornalísticas frágeis para dado estatístico: a taxa de homicídios do ISP-RJ é citada via Vanguard Attaché (site de turismo) e a série histórica via Crime Brasil. Citar o ISP-RJ e o Anuário do Fórum diretamente.

## C. Texto

- [x] C1. Resíduo de XML no início do último parágrafo de Delimitations: "T", tabulação, "he comparative" (`07-conclusion.md` linha 21).
- [x] C2. Título "eferences" sem o R (`08-references.md` linha 1).
- [x] C3. "informal áreas,  including" (palavra em português, vírgula e espaço duplo) em `01-introduction.md`. "23,000 ." com espaço antes do ponto e sem a fonte em `05-case-jacarezinho.md`.
- [x] C4. Travessões: 27 linhas com travessão no manuscrito. Preferência do autor é texto sem travessão.
- [x] C5. O objetivo declarado fala em "propose and conceptually validate". Quando houver número do experimento, o texto de Results e de Limitations ("No model has been trained") precisa mudar de conceitual para empírico preliminar. Atualização de 2026-09-18 [DESKTOP]: a frase "No model has been trained" já é falsa. Há 5 treinos com métricas no sintético em `06-resultados/RESULTADOS.md` (seção 5 da ficha). Ainda não há métrica em imagem real (seção 6), então o máximo que o texto pode afirmar hoje é "validação preliminar em dado sintético". Não mexer no texto antes de o autor decidir os itens 1 a 3 de `docs/DIVERGENCIAS.md`.

## D. Conteúdo a incorporar (vem do trabalho feito depois da v2)

- [ ] D1. Citar Liao et al. 2026 (Remote Sensing 18(2):361, DOI 10.3390/rs18020361) como evidência direta de que a origem da geometria pesa mais que a textura. Ver `05-levantamento-3d/`.
- [ ] D2. Citar G-MAD (Kim et al., ACM MM 2026, arXiv 2607.19942) como prior art do uso de ARMA 3 para dado aéreo sintético, e Berwaldt, Bettker e Pozzer (SBGames 2020, DOI 10.1109/SBGames51465.2020.00027) para geração procedural de favela. Conferir os três no Crossref ou arXiv antes de incluir.
- [ ] D3. Registrar a ortofoto pública do IPP de 2024 como alternativa aberta e não sensível aos dados da PCERJ, o que reforça o argumento ético da metodologia.
- [ ] D4. Inserir os resultados do experimento. Atualização de 2026-09-18 [DESKTOP]: `06-resultados/RESULTADOS.md` existe. Usar só números da "Ficha do experimento para o artigo", que têm arquivo e comando de origem. Os três números de sim-to-real ainda NÃO existem (ficha, seção 6); sem eles a seção de resultados fica restrita ao sintético.
- [ ] D5. O método executado é Blender 5.2 headless, não ARMA 3 (`docs/DIVERGENCIAS.md`, item 1). Depois da decisão do autor, ajustar a descrição do método, manter o crédito a Fábio H. P. Guimarães e ao prof. Claudio Miceli pela proposta de 2022, e reposicionar o G-MAD como linhagem comum com método diferente. Ferramentas a citar por versão e URL: Blender 5.2.1, OpenDroneMap 3.6.2, MPFB 2.0.17, Ultralytics 8.4.148 (YOLO11), Poly Haven (CC0), OpenStreetMap.
- [ ] D6. Achado próprio e citável: em imagem aérea a 100 m a pessoa ocupa 11 a 41 px em 4K, e treinar em ladrilhos de 1280 px em escala nativa levou o mAP50 de 0,116 para 0,561 nas mesmas 120 imagens (`06-resultados/RESULTADOS.md`, ficha, seção 5). Sustenta o argumento de que escolhas de engenharia pesam mais do que volume de dado.
- [ ] D7. Duas frases novas para Limitations: o levantamento aéreo de 2022 é todo em nadir a 150 m, portanto sem textura de fachada, o que limita justamente a leitura da morfologia vertical; e a textura fotogramétrica traz a sombra do horário do voo gravada, o que restringe a variação de iluminação nesse braço.
- [ ] D8. Cuidado ético ao reportar a distinção armado e desarmado: funciona no sintético porque a arma é sempre o mesmo modelo, na mesma posição e com o mesmo contraste. Reportar como capacidade validada seria o salto que o artigo critica. Decisão do autor em `docs/DIVERGENCIAS.md`, item 3.
- Nota sobre D1 e D2 (2026-09-18 [DESKTOP]): os três identificadores foram conferidos. Liao et al., DOI 10.3390/rs18020361, confere no Crossref; o título é "Bridging the Sim2Real Gap in UAV Remote Sensing: A High-Fidelity Synthetic Data Framework for Vehicle Detection" (o objeto é veículo, não pessoa, e isso precisa ficar claro ao citar). G-MAD, arXiv 2607.19942, confere no arXiv (Kim, Park, Yoon, Jung e Jeon; ACM Multimedia 2026). Berwaldt, Bettker e Pozzer, DOI 10.1109/SBGames51465.2020.00027, confere no Crossref. Os valores das ablações de Liao et al. não foram conferidos no texto do artigo.

## E. Conferencias feitas em 2026-09-21 [DESKTOP]

- [x] E1. Ablacoes de Liao et al. conferidas no texto do artigo, o que estava aberto na nota de
  D1 e D2. Ficha em `04-bibliografia/liao-2026-numeros-conferidos.md`. Achados que mudam o texto:
  o ganho de trocar assets genericos por base fotogrametrica e de 23,3 pontos pela Tabela 5 e de
  22,5 pela secao de resultados do proprio artigo, que e inconsistente consigo mesmo; citar como
  "cerca de 22 a 23 pontos". No YOLOv11, que e o nosso detector, o valor e +27,0. O objeto deles
  e VEICULO, nao pessoa, e isso precisa aparecer sempre que citarmos.
- [x] E2. Kiefer et al. conferido. Ficha em `04-bibliografia/kiefer-2022-numeros-conferidos.md`.
  A metrica e mAP@50, como a nota dizia. O intervalo "1,2 a 2,4" das nossas notas omitia a linha
  do YOLO, que marca 10,2 sintetico contra 43,9 real. Toda comparacao nossa com esse trabalho
  precisa usar a linha do YOLO, nao o intervalo.
- [ ] E3. Corrigir `docs/CONTEXTO.md`, que ainda traz o intervalo "1,2 a 2,4" sem a linha do YOLO
  e o "22,5" de Liao sem a ressalva de inconsistencia.
- [ ] E4. Acrescentar ao artigo a ressalva de denominador: a nossa razao de eficacia divide por um
  real treinado no PROPRIO conjunto de teste, e a da literatura divide por um real treinado fora
  do dominio. Ver secao 3 de `07-blender/PLANO-EXPERIMENTAL.md`.
