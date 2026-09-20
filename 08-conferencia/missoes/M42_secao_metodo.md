# M42 — Seção de método e identificação

Executada em 2026-08-21.

> **É a seção que decide.** A M33 e a M34 estabeleceram que a trilha de métodos da AIM é presidida em todas as sete sessões por um Senior Member da AAAI, e que **não há discussants** — ninguém lê o paper a fundo antes. A robustez tem de estar no corpo, e o método tem de estar impecável.

---

## A seção — texto de entrega

> **5. Method**
>
> **5.1 What "variance" means here**
>
> The literature on synthetic respondents uses "variance collapse" to describe at least three distinct quantities, and results that appear to contradict each other often do not. We distinguish them explicitly:
>
> - **V1**, variance across repeated calls holding the persona fixed;
> - **V2**, variance across personas *within* a stratum, pooling within-cell demographic heterogeneity;
> - **V3**, variance *between* strata.
>
> **This study measures V2.** Reported disagreements — for instance, evidence of under-dispersion in independent-agent designs alongside evidence of over-dispersion in profile-conditioned designs — are differences in aggregation layer, not contradictions. We state the layer in every result.
>
> **5.2 Extraction paths**
>
> Recent work establishes that instruction-tuned models do not sample from a conditional distribution: repeated calls on the same persona and item return the identical answer in a majority of cases, the concentration is visible in the logits, and it is not recoverable through any decoding temperature exposed by standard APIs. **The standard pipeline of aggregating repeated calls therefore risks measuring a degenerate sampling primitive rather than a distribution.**
>
> We collect four paths and report all four:
>
> | Path | Description | Calls per cell |
> |---|---|---|
> | **P1 — Describe** | The model is asked, in a single call, for the response *distribution* of the stratum | 1 |
> | P2 — Log-probability | Next-token log-probabilities over answer options | 1 |
> | P3 — Perturbed aggregation | Repeated persona calls with option order and question wording randomized per call | *k* |
> | P4 — Naive aggregation | Repeated persona calls, unperturbed | *k* |
>
> **P1 is primary**, for two reasons. First, it is the only path available across all providers: one major provider does not expose token log-probabilities, and comparing models across different extraction methods would confound model with method. Second, the describe path has been shown to reduce error against human benchmarks by more than half relative to persona aggregation.
>
> P4 is retained deliberately as a **negative baseline**. It is the method the applied literature uses, and reporting how far it departs from the benchmark is part of the contribution.
>
> **5.3 A known bias in the primary path, and why the estimand is robust to it**
>
> The describe path is not neutral. Evidence indicates that it corrects chronic under-dispersion and **overshoots into over-dispersion**, with standard-deviation ratios moving from roughly 0.4–0.56 to 1.26–1.37, and that this is a structural property of the method rather than a quirk of one model.
>
> This is why our primary estimand is a **correlation** rather than a level. If the describe path introduces an approximately constant additive shift in log variance ratio, the level is contaminated and the correlation between human variance and log variance ratio is not: correlation is invariant to a location shift in either variable. We report levels for all four paths and treat divergence between them as a quantity of interest.
>
> **5.4 Conditioning and instrument controls**
>
> Each stratum is conditioned in three modes — group information supplied as a prior multiple-choice answer, as a first-person biographical statement, and as a direct instruction to adopt the group — and all three are reported.
>
> Persona templates are built by fixed-order templating from the stratum variables, without evaluative adjectives, and **income is expressed as relative position** (percentile, or multiple of the prevailing minimum wage) rather than as nominal currency, because the official income classes are denominated in 2009 currency and would evoke a different stratum in a model trained a decade later.
>
> Three instrument controls follow from documented response biases in language models:
>
> 1. **Answer order is randomized per call, with the seed recorded, and half of all calls use the reversed scale.** All tested models favor the last-presented option, in one large study by up to a factor of twenty.
> 2. **No yes/no or agree/disagree items.** Models exhibit a systematic tendency toward "no" — the opposite of human acquiescence — documented in English but not in every language tested. We replicate a subset of items in both formats and report the comparison; to our knowledge this bias has not previously been characterized in Portuguese.
> 3. **Each item appears in two semantically equivalent paraphrases.** Even the largest models are sensitive to paraphrase.
>
> **5.5 Metrics**
>
> All metrics are computed over a **fixed stratum-level answer space**, with unobserved options entering as zeros. This is not a technical detail: computing indices only over observed options would eliminate by construction the phenomenon we measure.
>
> - **Alignment**, following the normalized 1-Wasserstein formulation standard in this literature, with ordinal options mapped to integers, refusal excluded and compared separately, and hedging options mapped to the mean of remaining ordinals.
> - **Total variation distance**, for nominal items and for comparability with published values.
> - **Log variance ratio**, `ln(Var[M_s] / Var[H_s])` — the primary outcome, because it isolates dispersion from location.
> - **Kolmogorov–Smirnov**, reported as a descriptive statistic only, for reasons given in 5.6.
> - **Design effect and effective sample size**, in the standard survey formulation, to express the result in the units practitioners use.
> - **Interval coverage**: the share of cells in which a naive 95% interval built from synthetic responses contains the benchmark value.
>
> **5.6 Inference, and why standard tests do not apply**
>
> The number of queries submitted to a model is a **researcher design choice, not a sampling constraint**. Three consequences follow, and we adopt them as rules rather than caveats:
>
> 1. Test statistics whose null distribution assumes a fixed random sample — the Kolmogorov–Smirnov test among them — have arbitrary p-values here, because *k* is arbitrary. We report KS as a descriptive distance only.
> 2. Standard errors computed as `sqrt(p(1−p)/k)` treat calls as independent. Under the sampling degeneracy described in 5.2, they are not.
> 3. **All reported uncertainty derives from variation between replicates** — paraphrase variant, ordering seed, execution run, model version — via bootstrap over replicates, never from variation between calls within a replicate.
>
> Estimation of the stratum gradient weights cells by the inverse variance of the benchmark estimate, so that imprecisely estimated cells contribute less; standard errors use a wild cluster bootstrap over strata, appropriate given the small number of clusters.
>
> **5.7 Versioning**
>
> Model responses drift: the same prompt has been shown to produce significantly different distributions months apart. Every call records the exact dated model identifier — never an alias — together with provider, temperature, seed where supported, extraction path, conditioning mode, stratum, item, answer ordering, paraphrase variant, and a SHA-256 hash of the exact prompt submitted. Raw response text is retained for every call, so that any change in extraction method can be recomputed against the original corpus rather than requiring recollection. Collection occurs within a declared and narrow window, and the window is reported.

**≈ 950 palavras.** O orçamento da M39 era 800 — cabe cortar 5.4 no resumo estendido e restaurá-lo no paper completo.

---

## As sete decisões que essa seção defende

| Subseção | O que ela antecipa |
|---|---|
| **5.1** | *"Seu resultado contradiz o paper X."* — Não contradiz: mede outra camada. **Declarar a taxonomia antes de qualquer resultado desarma a objeção mais provável** |
| **5.2** | *"Por que não agregou repetições, como todo mundo?"* — Porque todo mundo pode estar medindo artefato |
| **5.3** | *"Seu caminho primário tem viés conhecido."* — **Sim, e por isso o estimando é uma correlação.** ⭐ Antecipar a crítica e mostrar que o desenho já a incorpora é a melhor defesa que existe |
| **5.4** | *"Isso não é efeito de ordem?"* — Randomizada, com escala invertida em metade |
| **5.5** | *"Você calculou o índice só sobre o que apareceu?"* — Não, e explico por que isso destruiria o achado |
| **5.6** | *"Cadê o valor-p?"* — Não existe valor-p válido aqui, e explico |
| **5.7** | *"Isso replica?"* — Hash de prompt, versão datada, texto bruto retido |

---

## Comentário

**A subseção 5.3 é a peça mais importante do paper inteiro.** Ela pega o argumento mais forte contra o T2 — o caminho primário é enviesado — e mostra que **o desenho foi escolhido justamente por ser invariante a esse viés**. Não é defesa depois do fato; é decisão anterior, e o pré-registro prova.

**A 5.6 vale por si.** A maioria dos papers desta literatura reporta valores-p que, pelo argumento de Brand, Israeli e Ngwe, não significam nada. Dizer isso de forma explícita e adotar a alternativa é **contribuição metodológica menor mas real**, e é o tipo de coisa que o presidente da trilha de métodos nota.

**A 5.4 contém o único achado lateral do paper:** o viés de aquiescência invertida foi documentado em inglês, alemão e polonês, e **não em português**. Meia página de robustez, e é o quarto ponto de uma curva que hoje tem três.

### Sobre as citações

Escrevi a seção **sem nomes**, com as afirmações em forma indireta — *"recent work establishes"*, *"one large study"*. **Isso é rascunho, não estilo.** No texto final cada afirmação leva a citação nominal. Deixei assim para que a M46, a revisão adversarial, verifique cada uma contra a fonte antes de fixar.

---

## Pendências geradas

- [ ] **Inserir as citações nominais em todas as afirmações** — Argyle, Bisbee, Santurkar, Jang, Özkan, Rupprecht, Braun, Brand. A M46 confere uma a uma.
- [ ] Decidir se 5.4 fica no resumo estendido ou só no paper completo — é a candidata natural a corte.
- [ ] Confirmar se o provedor sem log-probabilidade deve ser nomeado ou descrito genericamente.
- [ ] Verificar quais provedores expõem semente e documentar a irreprodutibilidade exata onde não houver.
- [ ] Fixar o número de réplicas e o valor de *k* antes do pré-registro final.
- [ ] **M43 herda:** as métricas da 5.5 definem quais tabelas existem.
- [ ] **M44 herda:** a robustez pré-especificada precisa cobrir cada rua aberta aqui — caminhos, modos, temperatura, paráfrase.
