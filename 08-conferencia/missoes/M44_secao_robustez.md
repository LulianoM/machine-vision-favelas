# M44 — Seção de robustez planejada

Executada em 2026-08-21.

> **Num fórum sem discussants** (M34), **a robustez substitui o comentarista.** Ninguém vai ler o paper a fundo antes da sessão. O que não estiver no corpo não será perguntado — e também não será creditado.

---

## O princípio de organização

Cada subseção segue a mesma forma de três partes:

1. **A ameaça**, nomeada.
2. **O teste**, pré-registrado.
3. **⭐ A condição de derrubada** — o que precisaria aparecer para o resultado principal cair.

A terceira parte é incomum e é deliberada. **Declarar o que refutaria o próprio achado é o sinal mais barato e mais forte de que o trabalho não está procurando confirmação.**

---

## A seção — texto de entrega

> **7. Robustness**
>
> All analyses in this section were specified before data collection and are reported regardless of outcome. For each we state the condition under which our main result would not survive.
>
> **7.1 Temporal drift in the benchmark**
>
> *Threat.* The benchmark is a 2017–2018 survey; the audited models were trained on later data. Divergence could reflect genuine change in Brazilian consumption rather than model error.
>
> *Test.* Three layers. We compute each category's rate of change between the 2008–2009 and 2017–2018 survey waves and enter it as a covariate. We replicate on variables covered by the continuous national household survey, which extends to 2024. And we run a temporal placebo: the same audit against the 2008–2009 wave.
>
> *Overturning condition.* **If the stratum coefficient loses significance once category drift is controlled, our result is drift and not model behavior.** If the placebo against the earlier wave produces a materially different stratum ordering, the pattern is period-specific and cannot be described as a property of the model.
>
> **7.2 The result is not specific to language models**
>
> *Threat.* Variance compression may be a property of any statistical predictor — regression to the mean — rather than of language models. Recent work reports variance collapse in supervised baselines trained on the same population.
>
> *Test.* We fit a Gaussian-copula baseline and a random-forest baseline to the same microdata and subject both to the identical metric suite, then estimate the excess collapse attributable to the language model.
>
> *Overturning condition.* **If the statistical baselines exhibit the same near-constant variance across strata, the phenomenon is not about language models.** The finding would remain interesting — it would then concern the limits of any synthetic respondent — but the framing would change, and we would say so.
>
> **7.3 Extraction path**
>
> *Threat.* Our primary path is known to over-disperse; a competing path is known to under-disperse. Either could generate a spurious relationship.
>
> *Test.* All four paths are reported. We additionally implement two published corrections for variance collapse as benchmarks, rather than citing them as related work.
>
> *Overturning condition.* **If the sign of the correlation between population variance and log variance ratio differs across extraction paths, the result is an artifact of measurement.** A change in magnitude is expected and is not disqualifying; a change in sign is.
>
> **7.4 Small cells**
>
> *Threat.* Peripheral strata are also the smallest, so benchmark noise is correlated with the explanatory variable and could manufacture the predicted pattern.
>
> *Test.* Cells below 100 unweighted households are collapsed or dropped, with all drops reported. Regressions weight cells by the inverse variance of the benchmark estimate. We enter unweighted cell size as a competing covariate.
>
> *Overturning condition.* **If the stratum effect disappears once cell size is controlled, it was benchmark noise.**
>
> **7.5 Instrument sensitivity**
>
> *Threat.* Response biases documented in language models — recency in answer ordering, sensitivity to paraphrase, format effects — could drive the pattern.
>
> *Test.* Answer order is randomized per call with half of calls on a reversed scale; every item appears in two paraphrases; three conditioning modes are reported separately; and a temperature grid is run on the aggregation paths, where temperature is a design factor rather than a setting.
>
> *Overturning condition.* **If the correlation holds only in one conditioning mode or one paraphrase, it is an instrument effect.**
>
> **7.6 Item structure**
>
> *Threat.* Recent evidence shows that collapse severity is predictable from properties of the *item* — in particular whether it admits a single normatively correct answer. Stratum-level variation could be a proxy for item composition.
>
> *Test.* We code each item for the presence of a normatively correct response and include it as a control, and we test whether the stratum coefficient survives item fixed effects.
>
> *Overturning condition.* **If the stratum coefficient does not survive item fixed effects, the structure is on the item side, not the population side** — which is the finding already in the literature, and not ours.
>
> **7.7 Social desirability in the benchmark**
>
> *Threat.* Household budget surveys under-report socially sensitive categories. Divergence in those categories mixes model error with benchmark error.
>
> *Test.* Alcohol, tobacco, and gambling are excluded from the primary analysis. They are analyzed separately, with an inverted prediction: because models are trained on text rather than on statements to an interviewer, synthetic responses should exceed the benchmark in precisely these categories.
>
> *Interpretation.* Confirmation would indicate that part of the measured distance is benchmark bias rather than model bias — a result about the reference, not the model.
>
> **7.8 Aggregation layer**
>
> *Threat.* Comparisons with prior work may be confounded by which variance is being measured.
>
> *Test.* All results are reported at the declared layer — variance across personas within a stratum — and we report the within-persona layer separately, so that our estimates can be placed against studies measuring either.

**≈ 720 palavras.** No orçamento da M39.

---

## O que essa seção cobre, por origem

| Subseção | Ameaça de origem |
|---|---|
| 7.1 Deriva temporal | **A1 da M08** — classificada como certa e fatal |
| 7.2 Não é específico de LLM | **A7 da M08**, a partir de Ku et al.; linha de base de cópula vem de Lukauskas |
| 7.3 Caminho de extração | M06 e a advertência de Özkan na M11 |
| 7.4 Células pequenas | **A4 da M08**, a partir da anomalia de renda alta da M02 |
| 7.5 Sensibilidade de instrumento | M06 — recência de até 20×, paráfrase, modos, temperatura |
| 7.6 Estrutura do item | **Özkan (M11)** — a previsibilidade do lado do item |
| 7.7 Desejabilidade social | M01 e M06 — decisão de excluir do primário |
| 7.8 Camada de agregação | **M11** — a taxonomia V1/V2/V3 |

**Oito subseções cobrindo oito ameaças nomeadas.** Nenhuma sobra sem destino, e nenhuma é inventada aqui — todas vieram de missões anteriores.

---

## As três decisões de redação

**A frase de abertura faz duas promessas verificáveis:** que as análises foram especificadas antes da coleta, e que são reportadas **independentemente do resultado**. Com pré-registro depositado, as duas são checáveis. É barato prometer e caro descumprir — que é exatamente o que torna a promessa informativa.

**A condição de derrubada em cada subseção é o dispositivo central.** Um revisor que lê *"if the stratum coefficient does not survive item fixed effects, the structure is on the item side, not the population side — which is the finding already in the literature, and not ours"* aprende três coisas de uma vez: que o autor conhece a literatura concorrente, que o teste discrimina entre as duas hipóteses, e que o autor não vai racionalizar o resultado.

**A 7.2 admite explicitamente que o enquadramento pode mudar.** Dizer *"the finding would remain interesting… but the framing would change, and we would say so"* é raro e é forte. **Custa nada e compra credibilidade que nenhuma tabela compra.**

---

## O que deliberadamente não está aqui

| Fora | Por quê |
|---|---|
| Análise de sensibilidade de mediação | É do T4. O T2 não reivindica mediação |
| Suavização de Laplace, semente, versionamento | São **método** (seção 5), não robustez |
| A validação da correlação em dado de terceiros | É **evidência sem modelo** (seção 4) |
| Comparação com respondente sintético em inglês | Interessante, e é outro paper |

---

## Pendências geradas

- [ ] Confirmar a comparabilidade da classificação de despesa entre as ondas de 2008-2009 e 2017-2018 — **7.1 depende disso**, e é pendência aberta desde a M08.
- [ ] Decidir entre cópula gaussiana e floresta aleatória como linha de base principal em 7.2, ou usar as duas.
- [ ] Verificar se as duas correções publicadas de colapso de variância têm código reutilizável.
- [ ] Codificar os itens quanto à existência de resposta normativamente correta, para 7.6.
- [ ] Fixar as categorias sensíveis de 7.7 e confirmar que a POF as reporta separadamente.
- [ ] Decidir quais subseções sobrevivem ao corte do resumo estendido — candidatas a ir só para o paper completo: 7.6 e 7.8.
- [ ] **M46 herda:** a revisão adversarial deve testar se alguma ameaça ficou sem subseção.
