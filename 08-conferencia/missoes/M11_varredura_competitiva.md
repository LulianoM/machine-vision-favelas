# M11 — Varredura competitiva: quem está trabalhando nisso agora

Executada em 2026-08-21. Quatro papers baixados e lidos; onda de economia mapeada por busca.

---

## Resumo do que esta missão muda

1. **⚠️ Concorrente muito próximo, publicado em julho de 2026: Özkan (Istanbul Technical University).** Não-WEIRD, dados do WVS, e a frase de posicionamento é literalmente a do T2: *"The failure is predictable rather than random, which is what makes it useful."* **Mas a previsibilidade dele é do lado do item, não do estrato** — e ele declara explicitamente que suas afirmações sobre subgrupos são contaminadas. A faixa do T2 continua aberta, e agora precisa ser nomeada com precisão cirúrgica.

2. **⚠️ Advertência metodológica grave, do mesmo paper: o caminho *describe* super-dispersa.** A razão de desvio padrão vai de 0,4–0,56 para **1,26–1,37** ao adotar *verbalized sampling*, e ele descreve isso como **propriedade estrutural do método, não idiossincrasia de modelo**. A M06 elegeu P1 como caminho primário. Medir razão de variância por P1 sem correção mede o viés do instrumento.

3. **A onda de economia chegou e é séria.** Banco da Inglaterra, NBER, *Journal of Monetary Economics* e um preprint na SSRN cujo subtítulo é *"From Representative Agents to Population Distributions"* — que é exatamente a tese de não-responsividade de variância da M10, em vocabulário macroeconômico.

4. **Uma clarificação necessária ao achado da M10:** "variância" não é uma quantidade só, e Özkan e eu medimos coisas diferentes. Detalhado na seção 5.

---

## 1. Mapa de ameaça

| Trabalho | Venue e data | Proximidade | Ameaça |
|---|---|---|---|
| **Özkan** — *Distribution-First Population Simulation* | arXiv:2607.18310v1, 17/07/2026, Istanbul Tech | Altíssima | 🔴 |
| **Lukauskas e Šarkauskaitė** — *Plausible but Not Valid* | arXiv:2608.14606v1 ⚠️, Kaunas / AI Insight Lab | Alta | 🔴 |
| **Dalloul e Pfeifer** — *Can LLMs Mimic Household Surveys?* | Preprint SSRN, 2026 | Alta no segundo momento | 🟠 |
| Banco da Inglaterra — *Inflation attitudes of large language models* | Staff WP nº 1.190, jun/2026 | Média-alta | 🟠 |
| NBER — *LLM Survey Framework* | NBER WP w34308 | Média | 🟠 |
| **Boelaert et al.** | *Sociological Methods & Research* 54(3), 2025 | Alta | 🟠 (já mapeada, M03/M07) |
| **Kinzinger** — *Synthetic Personalities* | arXiv:2606.04592, finalista AIM 2026 | Média | 🟡 |
| *Assessing the Reliability of Persona-Conditioned LLMs* | arXiv:2602.18462 | Média | 🟡 |
| *Specializing LLMs to Simulate Survey Response Distributions for Global Populations* | arXiv:2502.07068 | Média | 🟡 |
| Zarifhonarvar (2026) — expectativas de inflação | — | Baixa-média | 🟡 |

⚠️ **Inconsistência de metadado registrada:** o paper de Lukauskas tem identificador arXiv 2608 (agosto de 2026) mas carimbo de data de 6 de julho de 2026 no corpo. Reconferir antes de citar.

---

## 2. Özkan (2026) — o concorrente mais próximo

**Referência:** ÖZKAN, Gürkan. *Distribution-First Population Simulation: Collapse, Calibration, and Recall in Non-WEIRD LLM Persona Modeling*. arXiv:2607.18310v1 [physics.soc-ph], 17 de julho de 2026. Istanbul Technical University.

### O que ele faz

Contrasta duas rotas para obter uma distribuição populacional:

| | Rota B — agentes independentes | Rota A — *Verbalized Sampling* |
|---|---|---|
| Custo | N chamadas, O(N) | **1 chamada, O(1)** |
| Mecânica | Cada personagem ancorado roda como agente independente; agrupam-se as escolhas | Pergunta-se uma vez pela distribuição da população |
| Resultado | **Amontoamento modal (colapso)** | Dispersão realista |

Dados: **2.414 respondentes reais do World Values Survey**, contexto **não-WEIRD com a Turquia primeiro**. Verificador determinístico e validado por construto.

### Os quatro achados

1. **A Rota B falha.** Em quatro cenários e cinco sementes: concentração sobe de 0,36 para 0,69, entropia cai de 1,46 para 0,77, **85% das unidades colapsam**, TVD = 0,44.
2. **O colapso é previsível pela estrutura do cenário**, com `r = 0,55` contra a existência de uma única resposta normativamente correta.
3. **VS corrige a sub-dispersão crônica sem treino**, em três famílias de modelo (fidelidade +7 a +10; significativo em Qwen, pareado entre sementes, p = 0,002, d = 6,2). **Mas universalmente ultrapassa para super-dispersão** — razão de desvio padrão de 0,4–0,56 para **1,26–1,37** — e ele qualifica isso como *"a structural property of VS rather than one model's quirk"*.
4. **Fidelidade de survey transfere mal para comportamento agêntico.** Numa tarefa de reserva, uma persona calibrada por survey é dominada por um padrão de menor preço em cerca de 80% dos casos, com a renda modulando mas não sobrepondo (escolha de conforto sobe 0% → 7% → 32% entre faixas de renda baixa, média e alta).

E um ataque de memorização com placebo mais um *backtest* de eleição nacional anonimizada mostram que **VS mantém a força agregada enquanto afirmações sobre subgrupo e sobre indivíduo são contaminadas por recall e subdeterminação**.

### Por que ameaça o T2

A frase de abertura do argumento dele é a do T2: *"The failure is predictable rather than random, which is what makes it useful."* Somada a contexto não-WEIRD e dados de WVS, a sobreposição de superfície é grande.

### Por que a faixa do T2 continua aberta — e mais estreita

Três diferenças, e a primeira é decisiva:

| | Özkan (2026) | T2 |
|---|---|---|
| **Eixo da previsibilidade** | **Estrutura do cenário** — se o item tem uma resposta normativamente correta (r = 0,55) | **Posição do estrato** na população |
| Afirmações sobre subgrupo | **Declaradamente contaminadas** e não sustentadas | São o objeto |
| Referência | WVS, 2.414 respondentes, 4 cenários | POF ponderada, ~58 mil domicílios, 12 a 15 categorias |
| Desfecho | Atitude e comportamento agêntico | Consumo e disposição a pagar |
| Escala do estrato | Turquia, sem estratificação socioeconômica fina | 7 faixas de rendimento medidas, 60 células em L3 |

**O posicionamento do T2 precisa mudar de "o colapso é previsível" para "o colapso é previsível também pelo lado da população, e não só pelo lado do item".** E o achado dele vira um **controle obrigatório**: incluir a estrutura do item — se há resposta normativamente correta — como covariável, e mostrar que a distância do estrato acrescenta poder explicativo além dela. Isso é mais forte que ignorá-lo e transforma um concorrente em fundação.

---

## 3. Lukauskas e Šarkauskaitė (2026) — auditoria psicométrica

**Referência:** LUKAUSKAS, Mantas; ŠARKAUSKAITĖ, Viktorija. *Plausible but Not Valid: A Psychometric Audit of LLMs as Synthetic Survey Respondents*. arXiv:2608.14606v1 [cs.CY]. Hostinger, Kaunas University of Technology e AI Insight Lab.

Dataset lituano aberto de psicologia organizacional, n = 263 empregados, três instrumentos validados, 68 itens, 12 subescalas. **37 LLMs** de OpenAI, Anthropic, Google e doze famílias de peso aberto. Escada de revelação de persona em cinco níveis, ablações de apresentação, esforço de raciocínio e língua, trocas contrafactuais em três eixos demográficos, e sonda de memorização verbatim.

Quatro achados que importam ao T2:

1. **Uma linha de base de cópula gaussiana compete com todos os LLMs** nos componentes dirigidos por amostra — distribuição, correlação, confiabilidade. PSS da cópula 0,69 contra 0,71 do melhor LLM, ambos muito abaixo do teto humano-contra-humano de 0,825. **É a linha de base estatística que a ameaça A7 exige (M08), com precedente publicado.**
2. **A "multidão" de LLMs é mais homogênea entre si (PSS médio inter-LLM 0,73) do que semelhante a humanos.** Achado forte e citável: agregar modelos diferentes não resolve, porque eles erram juntos.
3. **Memorização não explica o desempenho** — recall verbatim de pior caso 4,7%, correlação de posto com PSS igual a 0,00.
4. **Efeitos contrafactuais dirigidos por escolaridade dominam:** `|d|` médio de 0,56, máximo 1,50, contra 0,18 de papel e 0,12 de gênero.

O item 4 é diretamente acionável: **escolaridade é o eixo demográfico com maior efeito**, o que sustenta mantê-la no nível L3 do desenho (M05) e sugere que ela — não renda — pode ser a variável de maior amplitude para a M10.

---

## 4. A onda de economia

Apareceu entre o desenho do dossiê e hoje, e é a mais perigosa para o T2 porque fala a língua da AIM.

| Trabalho | Status de verificação |
|---|---|
| **Dalloul e Pfeifer (2026)**, *Can LLMs Mimic Household Surveys?: From Representative Agents to Population Distributions*, preprint SSRN | ⚠️ **[NÃO VERIFICADO]** — localizado apenas por fonte secundária. Descrito como examinando *"o segundo momento — a parte da distribuição que diz se o modelo representa uma opinião ou mil"* |
| **Banco da Inglaterra**, *Inflation attitudes of large language models*, Staff Working Paper nº 1.190, junho de 2026 | URL institucional confirmada; autoria não verificada |
| **NBER**, *LLM Survey Framework*, Working Paper w34308 | URL institucional confirmada; autoria não verificada |
| *Generating inflation expectations with large language models*, ScienceDirect S0304393225001308 | Provável *Journal of Monetary Economics*; ⚠️ **confirmar venue** |
| **Zarifhonarvar (2026)** | Modelos proprietários exibem **menos discordância** que os de peso aberto — efeito de família de modelo sobre dispersão |

**O subtítulo de Dalloul e Pfeifer é o problema.** "De agentes representativos a distribuições populacionais" é, palavra por palavra, a tese de não-responsividade de variância que a M10 derivou do dado de Boelaert. Se o paper já estabelece que o modelo se comporta como agente representativo em vez de população, a novidade dessa formulação cai.

**O que ainda sobra, mesmo no pior caso:** eles estão em expectativas macroeconômicas de domicílios; o T2 está em consumo por estrato socioeconômico, com benchmark oficial ponderado e desagregação em 60 células. Diferença de objeto e de resolução, não de tese. **Mas a tese deixaria de ser nova.**

---

## 5. Correção necessária ao achado da M10

Özkan mede Rota B **sub-dispersando** (razão de desvio padrão 0,4–0,56). Eu medi, na M10, o caminho FA de Boelaert **super-dispersando** em 82% das células. São resultados opostos, e a resolução importa.

**"Variância" são pelo menos três quantidades distintas:**

| | O que é | Quem mede |
|---|---|---|
| **V1** | Variância entre chamadas repetidas, **mesma persona** | Jang et al. (C1 da M03); Özkan na Rota B |
| **V2** | Variância entre personas **dentro da mesma célula** — perfis diferentes agrupados | **A M10**, sobre `FA-GPT-3` de Boelaert |
| **V3** | Variância **entre células** | O gradiente de decaimento do T2 |

A M10 mediu V2, que pool a heterogeneidade genuína de idade, sexo, ocupação e estado civil dentro de cada célula de país × classe. Özkan mede algo mais próximo de V1 agregado por cenário. **Não são contraditórios — são camadas diferentes da decomposição.**

Isso não invalida o achado central da M10. A correlação de −0,89 entre variância humana e `ln VR`, e a quase-constância da variância do modelo (CV 5 a 8 vezes menor que a humana), são propriedades de V2 e permanecem. **Mas o paper precisa declarar explicitamente qual camada mede**, sob pena de o revisor apontar contradição com Özkan que não existe.

**Ação:** acrescentar a decomposição V1/V2/V3 à taxonomia C1/C2/C3 da M03. São eixos ortogonais — C descreve o *fenômeno*, V descreve a *camada de agregação*.

---

## 6. Advertência sobre o caminho primário

A M06 elegeu P1, o caminho *describe*, como primário, apoiada em Jang et al. (redução de TV de 0,46 para 0,22).

Özkan acrescenta o outro lado: **VS ultrapassa para super-dispersão de forma estrutural**, com razão de desvio padrão indo a 1,26–1,37. Ou seja, P1 conserta o viés de sub-dispersão e introduz um viés de super-dispersão.

**Consequência dura:** medir `ln VR` por P1 sem correção mede parcialmente o instrumento. Três respostas, e o T2 precisa das três:

1. **Calibrar P1 contra a razão de desvio padrão conhecida**, usando os valores de Özkan como referência de magnitude.
2. **Reportar `ln VR` nos quatro caminhos**, e tratar a divergência entre eles como quantidade de interesse, não como ruído.
3. **Deslocar o desfecho primário de nível para forma.** A correlação entre variância humana e `ln VR` é **invariante a um deslocamento constante** de `ln VR`: se P1 adiciona um viés aproximadamente constante, a correlação sobrevive intacta enquanto o nível médio não.

**O ponto 3 é a saída elegante, e reforça a recomendação da M10** de promover a correlação de −0,89 a tese central. Ela é robusta exatamente ao viés que ameaça a alternativa.

---

## 7. Risco de escavação — avaliação revisada

**Subiu de "médio-alto" para alto.** Cronologia dos trabalhos diretamente relevantes:

```
2025 ago  Boelaert et al. (SMR)
2026 abr  Colapso de heterogeneidade em filósofos
2026 jun  Banco da Inglaterra WP 1.190
2026 jul  Verbalized Sampling · SSR · KNOWS/DOES · Özkan · Silicon Sampling via Cross-Survey Transfer
2026 ago  Lukauskas e Šarkauskaitė (auditoria psicométrica)
```

**Cinco trabalhos relevantes em julho de 2026 sozinho.** A taxa é de aproximadamente um por semana e está acelerando.

### O que é escavável e o que não é

| Ativo do T2 | Escavável? |
|---|---|
| A tese de não-responsividade de variância | **Sim, e talvez já tenha sido** (Dalloul e Pfeifer) |
| O gradiente por estrato socioeconômico | Sim, mas ninguém o fez ainda — Özkan declina explicitamente |
| Benchmark oficial ponderado da POF, com 58 mil domicílios | **Não.** Exige acesso e trabalho com microdado brasileiro |
| Desfecho de consumo e disposição a pagar por estrato | Difícil — exige o benchmark acima |
| 7 faixas de rendimento medidas contra 3 de classe autodeclarada | **Não**, pelo mesmo motivo |

**Conclusão:** o fosso do T2 é o **benchmark**, não a tese nem o método. Isso já estava dito na M03, e a M11 confirma com evidência mais dura.

### Três ações imediatas

1. **Depositar preprint assim que o resultado principal estiver estável**, antes da submissão de 19 de novembro. Estabelece prioridade num campo que se move semanalmente.
2. **Verificar Dalloul e Pfeifer com urgência.** Se eles já publicaram a tese de agente representativo, o T2 precisa reposicionar do primeiro momento para o gradiente por estrato — que é o que Özkan declina fazer.
3. **Reescrever a introdução** para nomear Özkan e Boelaert et al. como fundação, não como concorrência, e situar a contribuição no eixo população em vez do eixo item.

---

## Pendências geradas

- [ ] **Urgente:** localizar e ler Dalloul e Pfeifer (2026) na SSRN. É a maior incógnita do dossiê agora.
- [ ] Verificar autoria e conteúdo do Staff WP nº 1.190 do Banco da Inglaterra e do NBER w34308.
- [ ] Confirmar o venue de `S0304393225001308` no ScienceDirect.
- [ ] Resolver a inconsistência de metadado de Lukauskas (arXiv 2608 contra data de julho).
- [ ] **Acrescentar ao desenho:** estrutura do item (existência de resposta normativamente correta) como covariável de controle, conforme Özkan.
- [ ] **Acrescentar ao desenho:** linha de base de cópula gaussiana, conforme Lukauskas — atende A7 com precedente publicado e é mais barata que floresta aleatória.
- [ ] **M12 herda:** declarar explicitamente qual camada de variância (V1, V2 ou V3) o T2 mede, e pré-registrar a correlação como desfecho primário em vez do nível.
- [ ] Ainda não lidos, de baixa prioridade agora: Park et al. (2023, 2024), Goli e Singh (2024), Dominguez-Olmedo et al. (2023), Kaiser et al. (2025), Barrie e Cerina (2026), Alexander e Collins (2026), Schröder et al. (2025), Broska et al. (2024).
