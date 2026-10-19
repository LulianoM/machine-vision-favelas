# Pendências do rascunho v2 (Irigaray, 2026-09-10)

Tudo abaixo foi verificado no texto em 2026-09-17, com busca automática nos arquivos de `manuscrito/`. Marcar `[x]` ao resolver e anotar o commit.

## A. Estrutura

- [x] A1. "Conclusion" não conclui: só contém Limitations, Delimitations e Implications and Directions for Future Research. Falta o parágrafo de fecho (`07-conclusion.md`).
- [x] A2. A introdução não tem título de seção (`01-introduction.md`).
- [x] A3. Remissões a seções numeradas que não existem. O texto não numera as seções, mas cita "Section 2", "3", "4", "5", "6" e "7" em dez pontos, e a numeração implícita não bate com a ordem atual (a revisão de literatura é a segunda seção e é chamada de "Section 4"). Ocorrências: `02-literature-review.md` linha 11; `03-methodology.md` linhas 3 e 13; `06-results-proposed-model.md` linhas 5, 6 e 7; `07-conclusion.md` linhas 5, 17, 21 e 29. Decidir: numerar as seções e corrigir, ou trocar por remissão nominal. **Fechado em 2026-09-22** junto com a reordenação do artigo. As seções passaram a ser numeradas pelo montador e todas as remissões foram remapeadas por arquivo, porque os dois conjuntos de texto usavam esquemas incompatíveis: as seções técnicas usavam a numeração real do arquivo e as do orientador um esquema próprio (4 = revisão de literatura, 5 = metodologia, 6 = contexto de campo, 7 = modelo proposto) que nunca bateu com a ordem. Cinco remissões ambíguas foram resolvidas uma a uma lendo o contexto e estão listadas no script da rodada. **O orientador precisa confirmar as cinco.**
- [x] A4. Trecho repetido quase literalmente: o parágrafo das "two bodies of literature that rarely intersect" aparecia na introdução e de novo em "Positioning this study" na revisão, e a descrição de Gevaert et al. (2016) em Kigali também aparecia duas vezes. **Fechado em 2026-09-22** (commit 7ee8927): a revisão remete à introdução, e a introdução cita Gevaert, Sithole e da Silva em uma linha, remetendo à seção 2.
- [x] A5. Não há abstract nem palavras-chave.

- [x] A7. (17 e 18/10) Reestruturação pelo feedback de 14/10: sete seções, método fora dos resultados, interpretação só na discussão, limitações em 6.5, Declarations, RQ1 a RQ3. Plano e decisões abertas em `01-artigo/feedback-2026-10-14/PLANO-CORRECAO.md`.
- [x] A6. (30/09) Refino geral a pedido do autor: abstract de 510 para 330 palavras; 11.1 e 10.7 removidas; histórico de rascunho fora do texto; tabelas numeradas com legenda e figuras citadas; duas figuras e três tabelas novas; quadros de autoria fora do PDF. Diagnóstico e o que fica para os autores em `01-artigo/ANALISE-2026-09-30.md`.

## B. Referências

> **Busca bibliográfica de 2026-09-30 [DESKTOP], aplicada com o OK do autor.** B1, B3, B6, B7, B9 e
> B10 resolvidos; B8 em parte. Relatório, fontes e textos propostos em
> `04-bibliografia/busca-2026-09-30-pontos-abertos.md`. Cada DOI novo foi conferido de novo no
> Crossref antes de entrar (o do Zenodo, no DataCite).

> **Rodada de 2026-09-20 [DESKTOP].** B1 fechado PELA METADE, e a metade que ficou aberta é
> deliberada. A busca no Crossref por sobrenome e ano devolveu correspondência para as 13, mas
> comparando o TÍTULO devolvido com a frase que cita a obra, só 8 correspondem de fato. Um
> exemplo do que a conferência evitou: "Xu (2025)" é citado no texto comparando RRT, ACO e A*
> para planejamento de rota, e a busca por sobrenome e ano devolveu um artigo de sensoriamento
> remoto. Inserir aquele DOI teria fabricado uma citação. As 7 restantes (Chen et al. 2025, Xu
> 2025, Jiang et al. 2026, Wang e Qian 2026, Yan, Hsieh e Lai 2025, Horváth et al. 2023, Watson
> e Elliott 2025) dependem de quem escreveu a frase dizer qual obra é. Ferramenta em
> `01-artigo/ferramentas/busca_crossref.py`.

- [x] B1. (30/09: as 13 com entrada conferida no Crossref; cinco metadados corrigidos e quatro frases ajustadas ao que as obras dizem.) Treze obras citadas no texto sem entrada na lista: Chen, Liu, Hu, Zhang e Pan (2025); Rasoulie e Pashazadeh (2026); Xu (2025); Agrawal, Ratnoo e Ghose (2017); Jiang et al. (2026); Wang e Qian (2026); Yan, Hsieh e Lai (2025); Gevaert, Persello, Sliuzas e Vosselman (2016); Du, Xing, Wang, Wei e Zhang (2024); Barisic, Petric e Bogdan (2022); Horváth et al. (2023); Watson e Elliott (2025); da Silva, Kormann da Silva e Westerholt (2024). Localizar cada uma e conferir o DOI no Crossref antes de incluir. Nunca inventar DOI.
- [x] B2. Entrada "[Slovo Park study] (2025)" está sem autores. No texto a obra é citada como Sithole e Mhangara (2025). Completar.
- [x] B3. (30/09: trocada por CNN Brasil, Justiça Global, Lessing 2008, Misse 2011 e InSight Crime.) Wikipedia citada três vezes como fonte ("Wikipedia, 2026" duas vezes e "Wikipedia, 2025a", em `04-situating-the-study.md`) e sem entrada na lista. Substituir por fonte primária.
- [x] B4. Amnesty International é mencionada no texto sem referência. A entrada da Inter-American Commission on Human Rights (2021) está na lista e não é citada no texto. **Resolvido em 18/10/2026** na reestruturação: o texto novo não cita a Amnesty International e a entrada da Inter-American Commission saiu da lista (só ficam entradas citadas).
- [x] B5. Há duas entradas de Human Rights Watch de 2021 e o texto cita só "Human Rights Watch, 2021". Diferenciar como 2021a e 2021b. **Resolvido em 18/10/2026:** a lista ficou com uma só entrada da Human Rights Watch de 2021, a citada.
- [x] B6. (30/09: é matéria da Defesa em Foco, de Marcelo Barros; os números vão ao 20º Anuário, tabelas 6 e 8, e sai "the sharpest increase recorded nationally", que é falso em termos relativos.) A entrada "CNN Brasil (2026a)" aponta para uma URL do site Defesa em Foco, a mesma da entrada "Defesa em Foco (2026)". Conferir qual é a fonte real.
- [x] B7. (30/09: autor Scott Mistler-Ferguson, 27/01/2022; as frases sobre ambiente construído passaram a Grillo 2014 e às notas do Small Wars Journal, e a falta de mapas das rotas virou premissa do estudo.) "Ad Infinitum (2023)" provavelmente não é autor. O slug da URL (`brazil-tries-reclaim-rio-favelas-ad-infinitum`) indica que "Ad Infinitum" é o fim da manchete do InSight Crime. Abrir a página, identificar o autor e corrigir a entrada e as quatro citações no texto.
- [x] B8. (30/09, em parte: os dois blocos APA viraram uma ordem alfabética só; falta o bloco de marcadores herdado da v2.) A lista mistura dois formatos: seis entradas em lista com marcadores, sem padrão APA completo, seguidas de entradas APA em ordem alfabética, e as entradas acrescentadas em 20/09 ficam num bloco à parte, depois de Vanguard Attaché, fora da ordem alfabética. Unificar. **Resolvido em 18/10/2026:** a lista nova é uma ordem alfabética APA só, sem bloco de marcadores (102 entradas, todas citadas).
- [x] B9. (30/09: o texto dá 121 oficial, 122 com o quinto policial e 132 da Defensoria, cada um com a fonte.) O título da nota do Small Wars Journal de 2025 fala em 132 mortos e o texto usa 121 a 122 (número oficial). Deixar explícito no texto de onde vem cada número.
- [x] B10. (30/09: ISP-RJ e 19º e 20º Anuários citados direto; o pico da série estadual é 1994, não o início dos anos 2000.) Fontes jornalísticas frágeis para dado estatístico: a taxa de homicídios do ISP-RJ é citada via Vanguard Attaché (site de turismo) e a série histórica via Crime Brasil. Citar o ISP-RJ e o Anuário do Fórum diretamente.

## C. Texto

- [x] C1. Resíduo de XML no início do último parágrafo de Delimitations: "T", tabulação, "he comparative" (`07-conclusion.md` linha 21).
- [x] C2. Título "eferences" sem o R (`08-references.md` linha 1).
- [x] C3. "informal áreas,  including" (palavra em português, vírgula e espaço duplo) em `01-introduction.md`. "23,000 ." com espaço antes do ponto e sem a fonte em `05-case-jacarezinho.md`.
- [x] C4. Travessões: 27 linhas com travessão no manuscrito. Preferência do autor é texto sem travessão.
- [x] C5. O objetivo declarado fala em "propose and conceptually validate". Quando houver número do experimento, o texto de Results e de Limitations ("No model has been trained") precisa mudar de conceitual para empírico preliminar. Atualização de 2026-09-18 [DESKTOP]: a frase "No model has been trained" já é falsa. Há 5 treinos com métricas no sintético em `06-resultados/RESULTADOS.md` (seção 5 da ficha). Ainda não há métrica em imagem real (seção 6), então o máximo que o texto pode afirmar hoje é "validação preliminar em dado sintético". Não mexer no texto antes de o autor decidir os itens 1 a 3 de `docs/DIVERGENCIAS.md`.

## D. Conteúdo a incorporar (vem do trabalho feito depois da v2)

- [x] D1. Citar Liao et al. 2026 (Remote Sensing 18(2):361, DOI 10.3390/rs18020361) como evidência direta de que a origem da geometria pesa mais que a textura. Ver `05-levantamento-3d/`. **Feito:** citado nas seções 2, 7.2, 7.5 e 9.3, com os valores conferidos em E1 e a ressalva de que o objeto deles é veículo.
- [x] D2. Citar G-MAD (Kim et al., ACM MM 2026, arXiv 2607.19942) como prior art do uso de ARMA 3 para dado aéreo sintético, e Berwaldt, Bettker e Pozzer (SBGames 2020, DOI 10.1109/SBGames51465.2020.00027) para geração procedural de favela. Conferir os três no Crossref ou arXiv antes de incluir. **Resolvido em 18/10/2026:** G-MAD (Kim et al., 2026, arXiv, DOI da ACM ainda não registrado) e Berwaldt, Bettker e Pozzer (2020, DOI conferido no Crossref) citados na 2.2.
- [x] D3. Registrar a ortofoto pública do IPP de 2024 como alternativa aberta e não sensível aos dados da PCERJ, o que reforça o argumento ético da metodologia. **Fechado em 18/10/2026:** o autor descartou o braço do IPP em 20/09 (ver STATUS); o artigo não depende dele.
- [x] D4. Inserir os resultados do experimento. **Feito até 2026-09-26:** as seções 8 a 11 trazem os resultados, cada número com arquivo de origem em `06-resultados/` (validado em 10 rodadas, `01-artigo/VALIDACAO-2026-09-26.md`). Dos três números de sim-to-real, dois existem: zero-shot no VisDrone (9.2 e 9.3) e ajuste fino com 5 e 10% do treino do VisDrone (9.4). O terceiro, sintético e real no mesmo treino, rodou na rodada 4 (30/09) e está na 9.4: fica abaixo do só real nas duas frações. A rodada 4 também acrescentou sementes, a checagem de IoU e a regra oficial do VisDrone, a escala casada da 10.2, o teste por regime da 10.3, o objeto no porte de arma, os quadros novos a 35 e 75 m e o gêmeo de 150 m (critérios em `07-blender/PLANO-RODADA4.md`).
- [x] D5. O método executado é Blender 5.2 headless, não ARMA 3 (`docs/DIVERGENCIAS.md`, item 1). Depois da decisão do autor, ajustar a descrição do método, manter o crédito a Fábio H. P. Guimarães e ao prof. Claudio Miceli pela proposta de 2022, e reposicionar o G-MAD como linhagem comum com método diferente. Ferramentas a citar por versão e URL: Blender 5.2.1, OpenDroneMap 3.6.2, MPFB 2.0.17, Ultralytics 8.4.148 (YOLO11), Poly Haven (CC0), OpenStreetMap. **Situação em 2026-09-26:** a descrição do método já é a do Blender headless (seção 7) e o manuscrito não menciona o ARMA 3, então o crédito a Fábio H. P. Guimarães e ao prof. Claudio Miceli só volta a ser necessário se o pipeline de 2022 for citado. OpenDroneMap deixou de se aplicar, porque o braço fotogramétrico saiu do artigo em 22/09; OpenStreetMap entra pela 11.6, como origem das plantas do braço anterior do par 0,116 e 0,561 da 7.6. Blender 5.2 e Ultralytics 8.4.148 já estão citados (7.2 e 7.6); faltam a versão do MPFB e o reposicionamento do G-MAD. **Resolvido em 18/10/2026:** o método descrito é o Blender headless (4.2); a 2.2 diz que o trabalho nasce da proposta de 2022 com ARMA 3 e por que o motor de jogo foi trocado; os Acknowledgements creditam Fábio H. P. Guimarães e o prof. Claudio Miceli de Farias.
- [x] D6. Proposto como achado próprio e citável (a 100 m a pessoa ocupa 11 a 41 px em 4K, e ladrilhar em 1280 px em escala nativa levou o mAP50 de 0,116 para 0,561 nas mesmas 120 imagens). **Superado pelo texto em 2026-09-26:** a 7.6 e a 11.1 reportam o par como consistente com a aritmética e não como efeito isolado da escala, porque os dois treinos diferem também em tamanho do detector, entrada, épocas e inicialização, e a 11.1 pede que nenhum número do artigo seja citado como efeito da escala de treino. O "11 a 41 px" saiu do texto na rodada 5 da validação, por não ter comando de origem.
- [x] D7. Duas frases novas para Limitations sobre o levantamento aéreo de 2022 (só nadir a 150 m, sem textura de fachada) e sobre a sombra gravada na textura fotogramétrica. **Não se aplica mais:** o voo de 2022 e o braço fotogramétrico saíram do artigo em 22/09 (commit 235cb23), e a 11.6 diz que nenhuma medição reportada deriva dos ramos fotogramétricos.
- [x] D8. Cuidado ético ao reportar a distinção armado e desarmado: funciona no sintético porque a arma é sempre o mesmo modelo, na mesma posição e com o mesmo contraste. Reportar como capacidade validada seria o salto que o artigo critica. Decisão do autor em `docs/DIVERGENCIAS.md`, item 3. **Situação em 2026-09-26:** o texto já aplica o cuidado (9.5 e 11.5): nenhuma acurácia a 150 m (ausência argumentada pela resolução, não medida); a 75 m e a 35 m, cinco modelos de arma contra nove objetos confundíveis, a taxa de objeto chamado de arma como quantidade principal e o teste de arma inédita com critério fixado antes. A premissa original (a arma sempre o mesmo modelo, na mesma posição e com o mesmo contraste) não vale para os corpora de 75 m e 35 m. Falta a decisão formal do autor em `docs/DIVERGENCIAS.md`, item 3. **Resolvido em 18/10/2026:** a distinção é reportada só no sintético, com a confusão contra objetos, a varredura de limiar e a ressalva das pistas de comprimento (5.4, 6.1, 6.5 item 10).
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
- [x] E3. Corrigir `docs/CONTEXTO.md`, que ainda traz o intervalo "1,2 a 2,4" sem a linha do YOLO
  e o "22,5" de Liao sem a ressalva de inconsistencia. **Resolvido em 18/10/2026:** o CONTEXTO
  traz agora os três valores de Kiefer et al. com os reais correspondentes (1,2, 2,4 e 10,2 contra
  24,6, 48,6 e 43,9, como na seção 2 do manuscrito) e a linha do YOLO; e as duas ablações de Liao
  et al. pelos números de E1 (30,4 e 27,0 no YOLOv11; 17,5 e cerca de 22 a 23 na média, com a
  inconsistência 23,3 contra 22,5 e o aviso de que o objeto é veículo).
- [x] E4. Acrescentar ao artigo a ressalva de denominador. **Resolvido de outra forma em 2026-09-26:**
  o artigo só compara a sua razão com a de Kiefer et al. (9.2), cujo denominador é o treino
  inteiro do próprio VisDrone, em dez classes, e não um real treinado fora do domínio; a 9.2 diz
  por que as duas razões não são diretamente comparáveis. A razão de Liao et al., com
  denominador fora do domínio, não é usada, e o braço real fora do domínio da seção 3 de
  `07-blender/PLANO-EXPERIMENTAL.md` não rodou.
