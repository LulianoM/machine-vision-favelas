# M41 — Seção de dados e contexto institucional

Executada em 2026-08-21. **Duas pendências fechadas na fonte primária.**

---

## Pendências resolvidas nesta missão

### ✅ O N amostral da POF 2017-2018 — divergência explicada

A M05 registrou que as fontes divergiam entre "58 mil" e "75 mil domicílios". **As duas estavam certas, e referem-se a coisas diferentes.**

Da **Tabela 1 das Notas Técnicas** — *Unidades primárias de amostragem selecionadas e domicílios esperados, selecionados e entrevistados*:

| Brasil | |
|---|---|
| Unidades primárias de amostragem selecionadas | **5.504** ¹ |
| Domicílios **esperados** | 69.660 |
| Domicílios **selecionados** | 75.635 |
| **Domicílios entrevistados** | **57.920** |

¹ Das 5.504 UPAs, três tiveram todas as entrevistas não realizadas, e seus fatores de expansão foram redistribuídos entre as demais UPAs do mesmo estrato.

> **O N analítico é 57.920.** É esse que vai no paper.

### ✅ Os percentuais regionais — verificados na tabela oficial

Distribuição acumulada de famílias por classe de rendimento, primeira faixa (**até 2 salários mínimos**):

| Recorte | % |
|---|---|
| **Nordeste** | **39,4** |
| **Norte** | **39,1** |
| Rural | 42,5 |
| Centro-Oeste | 17,6 |
| **Sudeste** | **16,4** |
| **Sul** | **14,8** |

E o texto do relatório confirma: *"cerca de 2/5 das famílias do Norte (39,1%) e Nordeste (39,4%) viviam com dois salários mínimos ou menos."*

**A amplitude Nordeste-contra-Sul é de 24,6 pontos percentuais.** Era o número que a M40 usou como `[39,4]` e `[14,8]` na introdução. **Confirmado.**

---

## A seção — texto de entrega

> **3. Data and Institutional Context**
>
> **3.1 The human benchmark**
>
> Our benchmark is the *Pesquisa de Orçamentos Familiares* (POF), the Brazilian national household budget survey, conducted by the Instituto Brasileiro de Geografia e Estatística (IBGE) in 2017–2018. The POF is the reference instrument for household consumption in Brazil: it supplies the expenditure structure underlying the national consumer price index and the consumption vector of the national accounts.
>
> The survey uses a two-stage cluster design with geographic and statistical stratification of first-stage units. Census tracts serve as primary sampling units and permanent private households as second-stage units. Of 5,504 primary sampling units selected, the survey selected 75,635 households and completed interviews in **57,920**. Each interviewed household carries a sampling weight, or expansion factor, that allows population estimates for the survey universe.
>
> Two properties make the POF an unusually strong benchmark for this exercise, and both are worth stating explicitly because most of the synthetic-respondent literature does not have them. First, it is a **probability sample with published weights**, not a convenience panel: the human distribution against which we compare is itself a defensible population estimate. Second, it measures **observed expenditure**, collected through household budget diaries, rather than stated preference. Where prior work in this literature benchmarks against opt-in survey panels — and, in the case of the closest marketing antecedent, against a panel the authors themselves describe as younger, more educated, more politically skewed, and lower income than the general population — our reference distribution is designed to represent the country.
>
> **3.2 Why Brazil**
>
> The identifying variation this study requires is dispersion in *population heterogeneity* across strata. Brazil supplies it unusually cleanly, because the dispersion occurs **within a single language and a single national market**, which removes the confound between country, language, culture, and training-corpus coverage that a cross-national design would introduce.
>
> The magnitude is large. In the 2017–2018 POF, **39.4%** of families in the Northeast and **39.1%** in the North lived on up to two minimum wages, against **16.4%** in the Southeast and **14.8%** in the South — a spread of nearly twenty-five percentage points inside one currency, one legal framework, and one consumer market. In rural areas the figure reaches 42.5%. A cross-national design would have to attribute variation of this size to national differences; here it is internal.
>
> **3.3 Strata and the fixed brand-agnostic universe**
>
> The POF reports seven official income classes, defined in minimum wages of January 15, 2009, running from "up to 2" through "more than 25." We retain these classes as published for the marginal analysis, which allows direct comparison against IBGE's own published tables without touching microdata.
>
> Our confirmatory analysis operates at a finer level. We cross a four-band collapse of the income classes with five macro-regions and three education levels, producing **60 cells**. The collapse is necessary because the top income class contains roughly 3% of urban families and does not sustain crossed cells. Cells with fewer than 100 unweighted households are collapsed with adjacent cells or dropped, and every drop is reported.
>
> **3.4 The temporal gap, and how we address it**
>
> The POF reference period is 2017–2018; the models we audit were trained on data extending several years beyond it. Divergence between a synthetic response and the benchmark could therefore reflect model error or genuine drift in Brazilian consumption — a period that includes the pandemic, food price inflation, the diffusion of instant payments, and the consolidation of delivery platforms.
>
> We address this in three ways. First, we compute for each consumption category its rate of change between the 2008–2009 and 2017–2018 POF waves, and include that rate as a covariate: if model error tracks a category's historical volatility, the divergence is drift; if the stratum coefficient survives the control, it is not. Second, we replicate the design on variables covered by the *Pesquisa Nacional por Amostra de Domicílios Contínua*, which extends to 2024. Third, we run a temporal placebo against the 2008–2009 wave: a stratum-level error pattern that is stable across two waves separated by a decade is not an artifact of any single reference period.
>
> A new POF wave, fielded from November 2024 across more than 103,000 households, is expected to become available and would collapse this gap. We do not condition the design on its release.

**≈ 700 palavras.** No orçamento da M39.

---

## Comentário sobre as escolhas

| Escolha | Razão |
|---|---|
| **Abrir dizendo que a POF alimenta o IPCA e as contas nacionais** | Estabelece autoridade do benchmark para quem nunca ouviu falar dela. O leitor é americano |
| **Dar os três números da amostra — 75.635 selecionados, 57.920 entrevistados** | Transparência, e antecipa a pergunta. Reportar taxa de resposta implícita é boa prática |
| **A comparação com o painel de conveniência de Brand, Israeli e Ngwe** | ⭐ **É o parágrafo mais forte da seção.** Eles próprios descrevem a amostra como enviesada (M02); usar isso é justo e é devastador. **O T2 tem benchmark melhor, não só contexto diferente** |
| **"observed expenditure, not stated preference"** | Distingue o T2 de toda a literatura de opinião — Argyle, Bisbee, Santurkar, Boelaert — de uma vez |
| **"We do not condition the design on its release"** | A M05 alertou contra planejar em cima da POF 2024-2025. Dizer isso explicitamente antecipa a pergunta do revisor |
| **O confundidor temporal tem subseção própria** | A M08 classificou como ameaça número um, certa e fatal. **Esconder num parágrafo de limitações seria erro** |

### O que ficou de fora, deliberadamente

- **A discussão sobre desejabilidade social nas categorias sensíveis** — vai para a seção de robustez (M44), não aqui.
- **O detalhe das medidas de distância** — é método (seção 5), não dados.
- **Qualquer justificativa biográfica do Brasil.** A M35 foi clara: o Brasil é escolha de desenho.

---

## Pendências geradas

- [x] ~~Confirmar N amostral da POF~~ — **fechada: 57.920 entrevistados de 75.635 selecionados, 5.504 UPAs**
- [x] ~~Confirmar percentuais regionais~~ — **fechada: 39,4 · 39,1 · 17,6 · 16,4 · 14,8, e 42,5 no rural**
- [ ] Confirmar a comparabilidade da classificação de despesa entre as ondas 2008-2009 e 2017-2018 — **o placebo temporal depende disso** (pendência aberta desde a M08)
- [ ] Verificar a data prevista de divulgação da POF 2024-2025 junto ao IBGE.
- [ ] Confirmar se a PNAD Contínua cobre as variáveis necessárias ao braço de contemporaneidade.
- [ ] Definir as 12 a 15 categorias de consumo e calcular a taxa de mudança de cada uma entre as duas ondas.
- [ ] Verificar se o IBGE exige forma específica de citação do microdado.
