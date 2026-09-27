# Pendências do rascunho v2 (Irigaray, 2026-09-10)

Tudo abaixo foi verificado no texto em 2026-09-17, com busca automática nos arquivos de `manuscrito/`. Marcar `[x]` ao resolver e anotar o commit.

## A. Estrutura

- [x] A1. "Conclusion" não conclui: só contém Limitations, Delimitations e Implications and Directions for Future Research. Falta o parágrafo de fecho (`07-conclusion.md`).
- [x] A2. A introdução não tem título de seção (`01-introduction.md`).
- [x] A3. Remissões a seções numeradas que não existem. O texto não numera as seções, mas cita "Section 2", "3", "4", "5", "6" e "7" em dez pontos, e a numeração implícita não bate com a ordem atual (a revisão de literatura é a segunda seção e é chamada de "Section 4"). Ocorrências: `02-literature-review.md` linha 11; `03-methodology.md` linhas 3 e 13; `06-results-proposed-model.md` linhas 5, 6 e 7; `07-conclusion.md` linhas 5, 17, 21 e 29. Decidir: numerar as seções e corrigir, ou trocar por remissão nominal. **Fechado em 2026-09-22** junto com a reordenação do artigo. As seções passaram a ser numeradas pelo montador e todas as remissões foram remapeadas por arquivo, porque os dois conjuntos de texto usavam esquemas incompatíveis: as seções técnicas usavam a numeração real do arquivo e as do orientador um esquema próprio (4 = revisão de literatura, 5 = metodologia, 6 = contexto de campo, 7 = modelo proposto) que nunca bateu com a ordem. Cinco remissões ambíguas foram resolvidas uma a uma lendo o contexto e estão listadas no script da rodada. **O orientador precisa confirmar as cinco.**
- [x] A4. Trecho repetido quase literalmente: o parágrafo das "two bodies of literature that rarely intersect" aparecia na introdução e de novo em "Positioning this study" na revisão, e a descrição de Gevaert et al. (2016) em Kigali também aparecia duas vezes. **Fechado em 2026-09-22** (commit 7ee8927): a revisão remete à introdução, e a introdução cita Gevaert, Sithole e da Silva em uma linha, remetendo à seção 2.
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
- [ ] B8. A lista mistura dois formatos: seis entradas em lista com marcadores, sem padrão APA completo, seguidas de entradas APA em ordem alfabética, e as entradas acrescentadas em 20/09 ficam num bloco à parte, depois de Vanguard Attaché, fora da ordem alfabética. Unificar.
- [ ] B9. O título da nota do Small Wars Journal de 2025 fala em 132 mortos e o texto usa 121 a 122 (número oficial). Deixar explícito no texto de onde vem cada número.
- [ ] B10. Fontes jornalísticas frágeis para dado estatístico: a taxa de homicídios do ISP-RJ é citada via Vanguard Attaché (site de turismo) e a série histórica via Crime Brasil. Citar o ISP-RJ e o Anuário do Fórum diretamente.

## C. Texto

- [x] C1. Resíduo de XML no início do último parágrafo de Delimitations: "T", tabulação, "he comparative" (`07-conclusion.md` linha 21).
- [x] C2. Título "eferences" sem o R (`08-references.md` linha 1).
- [x] C3. "informal áreas,  including" (palavra em português, vírgula e espaço duplo) em `01-introduction.md`. "23,000 ." com espaço antes do ponto e sem a fonte em `05-case-jacarezinho.md`.
- [x] C4. Travessões: 27 linhas com travessão no manuscrito. Preferência do autor é texto sem travessão.
- [x] C5. O objetivo declarado fala em "propose and conceptually validate". Quando houver número do experimento, o texto de Results e de Limitations ("No model has been trained") precisa mudar de conceitual para empírico preliminar. Atualização de 2026-09-18 [DESKTOP]: a frase "No model has been trained" já é falsa. Há 5 treinos com métricas no sintético em `06-resultados/RESULTADOS.md` (seção 5 da ficha). Ainda não há métrica em imagem real (seção 6), então o máximo que o texto pode afirmar hoje é "validação preliminar em dado sintético". Não mexer no texto antes de o autor decidir os itens 1 a 3 de `docs/DIVERGENCIAS.md`.

## D. Conteúdo a incorporar (vem do trabalho feito depois da v2)

- [x] D1. Citar Liao et al. 2026 (Remote Sensing 18(2):361, DOI 10.3390/rs18020361) como evidência direta de que a origem da geometria pesa mais que a textura. Ver `05-levantamento-3d/`. **Feito:** citado nas seções 2, 7.2, 7.5 e 9.3, com os valores conferidos em E1 e a ressalva de que o objeto deles é veículo.
- [ ] D2. Citar G-MAD (Kim et al., ACM MM 2026, arXiv 2607.19942) como prior art do uso de ARMA 3 para dado aéreo sintético, e Berwaldt, Bettker e Pozzer (SBGames 2020, DOI 10.1109/SBGames51465.2020.00027) para geração procedural de favela. Conferir os três no Crossref ou arXiv antes de incluir.
- [ ] D3. Registrar a ortofoto pública do IPP de 2024 como alternativa aberta e não sensível aos dados da PCERJ, o que reforça o argumento ético da metodologia.
- [x] D4. Inserir os resultados do experimento. **Feito até 2026-09-26:** as seções 8 a 11 trazem os resultados, cada número com arquivo de origem em `06-resultados/` (validado em 10 rodadas, `01-artigo/VALIDACAO-2026-09-26.md`). Dos três números de sim-to-real, dois existem: zero-shot no VisDrone (9.2 e 9.3) e ajuste fino com 5 e 10% do treino do VisDrone (9.4). O terceiro, sintético e real no mesmo treino, não rodou, e a conclusão o declara não testado.
- [ ] D5. O método executado é Blender 5.2 headless, não ARMA 3 (`docs/DIVERGENCIAS.md`, item 1). Depois da decisão do autor, ajustar a descrição do método, manter o crédito a Fábio H. P. Guimarães e ao prof. Claudio Miceli pela proposta de 2022, e reposicionar o G-MAD como linhagem comum com método diferente. Ferramentas a citar por versão e URL: Blender 5.2.1, OpenDroneMap 3.6.2, MPFB 2.0.17, Ultralytics 8.4.148 (YOLO11), Poly Haven (CC0), OpenStreetMap. **Situação em 2026-09-26:** a descrição do método já é a do Blender headless (seção 7) e o manuscrito não menciona o ARMA 3, então o crédito a Fábio H. P. Guimarães e ao prof. Claudio Miceli só volta a ser necessário se o pipeline de 2022 for citado. OpenDroneMap deixou de se aplicar, porque o braço fotogramétrico saiu do artigo em 22/09; OpenStreetMap entra pela 11.6, como origem das plantas do braço anterior do par 0,116 e 0,561 da 7.6. Blender 5.2 e Ultralytics 8.4.148 já estão citados (7.2 e 7.6); faltam a versão do MPFB e o reposicionamento do G-MAD.
- [x] D6. Proposto como achado próprio e citável (a 100 m a pessoa ocupa 11 a 41 px em 4K, e ladrilhar em 1280 px em escala nativa levou o mAP50 de 0,116 para 0,561 nas mesmas 120 imagens). **Superado pelo texto em 2026-09-26:** a 7.6 e a 11.1 reportam o par como consistente com a aritmética e não como efeito isolado da escala, porque os dois treinos diferem também em tamanho do detector, entrada, épocas e inicialização, e a 11.1 pede que nenhum número do artigo seja citado como efeito da escala de treino. O "11 a 41 px" saiu do texto na rodada 5 da validação, por não ter comando de origem.
- [x] D7. Duas frases novas para Limitations sobre o levantamento aéreo de 2022 (só nadir a 150 m, sem textura de fachada) e sobre a sombra gravada na textura fotogramétrica. **Não se aplica mais:** o voo de 2022 e o braço fotogramétrico saíram do artigo em 22/09 (commit 235cb23), e a 11.6 diz que nenhuma medição reportada deriva dos ramos fotogramétricos.
- [ ] D8. Cuidado ético ao reportar a distinção armado e desarmado: funciona no sintético porque a arma é sempre o mesmo modelo, na mesma posição e com o mesmo contraste. Reportar como capacidade validada seria o salto que o artigo critica. Decisão do autor em `docs/DIVERGENCIAS.md`, item 3. **Situação em 2026-09-26:** o texto já aplica o cuidado (9.5 e 11.5): nenhuma acurácia a 150 m (ausência argumentada pela resolução, não medida); a 75 m e a 35 m, cinco modelos de arma contra nove objetos confundíveis, a taxa de objeto chamado de arma como quantidade principal e o teste de arma inédita com critério fixado antes. A premissa original (a arma sempre o mesmo modelo, na mesma posição e com o mesmo contraste) não vale para os corpora de 75 m e 35 m. Falta a decisão formal do autor em `docs/DIVERGENCIAS.md`, item 3.
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
- [x] E4. Acrescentar ao artigo a ressalva de denominador. **Resolvido de outra forma em 2026-09-26:**
  o artigo só compara a sua razão com a de Kiefer et al. (9.2), cujo denominador é o treino
  inteiro do próprio VisDrone, em dez classes, e não um real treinado fora do domínio; a 9.2 diz
  por que as duas razões não são diretamente comparáveis. A razão de Liao et al., com
  denominador fora do domínio, não é usada, e o braço real fora do domínio da seção 3 de
  `07-blender/PLANO-EXPERIMENTAL.md` não rodou.
