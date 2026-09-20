# M48 — Apresentação de 12 minutos

Executada em 2026-08-21. **Última missão do roteiro.**

---

## As restrições, verificadas no programa oficial (M34)

| | |
|---|---|
| Tempo | **12 minutos de fala + 3 de perguntas.** Sessão de 60 min com 4 trabalhos — **sem folga** |
| Discussant | **Não existe.** Ninguém leu o paper. O retorno vem da plateia, nos 3 minutos |
| Trilha provável | **D**, presidida por **Daniel E. O'Leary** nas sete sessões — métodos, avaliação de LLM, confiabilidade |
| Concorrência | **Quatro trilhas paralelas.** Quem está na sala escolheu estar |
| Vizinho | Sessão 6D de 2026 trazia *Synthetic Personalities* (Kinzinger e Hartmann) — o paper adjacente |

> **12 minutos são cerca de 1.600 palavras faladas.** Tudo abaixo cabe nisso e foi cronometrado por contagem, não por estimativa.

---

## A decisão de estrutura: uma mensagem, um gráfico, uma implicação

### ⭐ A mensagem única

> **A variância que um modelo devolve para um segmento não diz nada sobre a variância daquele segmento na população.**

**Mudou na M47 e a mudança importa.** Até a M45 a mensagem era *"uma variância serve para todos"*. O teste do caminho NTP mostrou que sob outra via de extração o modelo devolve variâncias **bem diferentes** entre estratos — só que na direção errada. A forma do erro depende do caminho; **a ausência de informação, não.** A mensagem nova é mais geral e sobrevive aos dois caminhos.

### O gráfico único — e por que mudou

A M43 recomendou abrir com a **Figura 2**, a cobertura do intervalo caindo conforme *k* cresce. **Estou revertendo essa decisão**, por duas razões:

1. **A mensagem mudou na M47, e o gráfico segue a mensagem.** A Figura 2 ilustra a *consequência*; a Figura 1 **é a afirmação**.
2. **A Figura 1 existe hoje**; a Figura 2 depende de coleta que ainda não aconteceu. Num prazo com risco, o gráfico único tem de ser o que não pode faltar.

**O gráfico:** variância do modelo (eixo y) contra variância da população (eixo x), um painel por item, com a **diagonal tracejada `y = x`** — onde um modelo fiel cairia — e a **nuvem achatada** dos pontos reais. A distância entre a diagonal e a nuvem é o achado, e é visível sem estatística.

A cobertura vira o **slide de implicação**, não o de abertura.

### A implicação única

> **Coletar mais respostas sintéticas não reduz a chance de estar errado. Reduz a chance de perceber.**

---

## O roteiro falado — texto de entrega

> Marcações de tempo são cumulativas. **Ensaiar com cronômetro; o corte está previsto ao fim.**

---

**[0:00 — Slide 1: título]**

> Good morning. I'm Felipe Figueira, from Fundação Getulio Vargas in Brazil.
>
> Here is a question a marketing team asked me last year. They wanted to test a product concept across six customer segments. A synthetic panel would cost about two hundred dollars and take an afternoon. A human panel would cost about forty thousand and take six weeks.
>
> They asked whether the cheap one would give them the same answer.
>
> **I want to give you the honest version of that answer, because it is not the one either camp gives you.**

**[0:50 — Slide 2: o que já se sabe]**

> The literature has converged on something. Language models reproduce population **means** remarkably well, and reproduce population **variance** badly. Under-dispersion, mode collapse, variance collapse — several names, same finding.
>
> So the practical advice has been: use synthetic panels for averages, not for spread.
>
> **That advice is incomplete in a way that matters.** Almost every marketing question that justifies the expense of a survey is a question about spread. Which segment differs. Where the tails are. How much a market disagrees with itself. If you only trust the mean, you have bought a very cheap answer to a question you did not ask.
>
> **So the real question is not whether the variance is wrong. It is whether the wrongness is predictable.**

**[1:55 — Slide 3: a métrica é um artefato]** ⭐

> Before the result, one methodological point, because it changed our own analysis.
>
> This literature commonly summarizes dispersion error as the **log variance ratio** — log of model variance over population variance — and reports its correlation with population variance. Those correlations are large and negative. Ours was minus point nine eight.
>
> **That number is close to meaningless.** The population variance sits in the denominator of the ratio, so the correlation is negative by construction.
>
> We tested it. We replaced the model's variance with **gaussian noise** — no relationship to the population at all, matched mean and standard deviation. The correlation came out at **minus point nine seven nine**. Our observed value sits inside that null.
>
> **A random number generator reproduces the published finding.** So we do not use that metric, and I would gently suggest that results resting on it deserve a second look.

**[3:05 — Slide 4: o estimando]**

> What we use instead is a slope.
>
> Regress the model's variance for a stratum on the population's variance for that stratum. **A model that reproduced dispersion has a slope of one. A model whose dispersion tells you nothing about the stratum has a slope of zero.**
>
> And note the null. We test against **one**, not against zero. Testing against zero asks whether the model has *any* relation to the population. The question managers have is whether it has **enough**.

**[3:55 — Slide 5: O GRÁFICO]** ⭐ *(pausar dois segundos antes de falar)*

> This is public data — a replication package we did not produce, four models, World Values Survey items, five countries, strata defined by educational attainment.
>
> **The dashed line is where a faithful model would fall.** Each point is a country-by-education cell. The x-axis is how much that population actually disagrees. The y-axis is how much the model thinks it does.
>
> *[pausa]*
>
> **The population spreads out. The model does not follow.**
>
> Across twelve model-by-item combinations, **eleven have a confidence interval for the slope that excludes one**. Most sit between zero and point two. One of them — the newest model, on political position — comes in at **minus point zero one nine**. Not weak. **Absent.**
>
> And I want to flag the twelfth, because it is the interesting one. The largest model, on the item with the fewest response options, has a slope of **one point zero three**. It tracks perfectly. **The failure is not universal, and where it disappears is informative.**

**[5:45 — Slide 6: a advertência]**

> Two things this slide is not.
>
> These are **opinion items**, not consumption. These are strata defined by **education**, not income. **This analysis motivates the study. It does not test its hypothesis.**
>
> I show it because it is data we did not generate, and because the pattern is already visible in it.

**[6:20 — Slide 7: o estudo]**

> The study itself audits frontier models against the Brazilian household budget survey — a probability sample, published weights, fifty-seven thousand nine hundred and twenty interviewed households, and **observed expenditure rather than stated preference**.
>
> Brazil supplies the variation this design needs. Thirty-nine percent of families in the Northeast live on up to two minimum wages, against fifteen percent in the South. **A twenty-five point spread inside one language, one currency, one market** — which is what removes the confound a cross-national design would carry.
>
> Four extraction paths, three conditioning modes, randomized option order, two paraphrases per item, and dated model identifiers with prompt hashes. All of it pre-registered, including the conditions under which we would report that we were wrong.
>
> **And one factorial arm that came out of our own adversarial review:** the same construct measured on three-, five-, seven- and eleven-point scales. Because in the public data, the spread across **items** is larger than the spread across **models** — and if response granularity explains the whole effect, this is a paper about scale design and not about representation. **We would rather find that out than be told it.**

**[8:20 — Slide 8: a implicação]**

> What does this cost someone who buys the cheap panel?
>
> Two translations. The first is **effective sample size**: what your synthetic responses are worth in units of independent human observations.
>
> The second is the one I would ask you to remember. **Interval coverage — and it moves the wrong way.** A ninety-five percent confidence interval built from synthetic responses in the ordinary way contains the true value less often **the more synthetic responses you collect**.
>
> That is not a paradox. The number of queries you send a model is a **choice**, not a sampling constraint. More queries shrink the interval around your estimate without moving the estimate toward the population. **The interval converges. It converges on the wrong value, and it converges tightly.**
>
> **Collecting more synthetic data does not reduce your chance of being wrong. It reduces your chance of noticing.**

**[9:35 — Slide 9: o negativo honesto]** ⭐

> I want to close with something we looked for and **did not find**.
>
> It would be valuable to have a rule that flags unreliable synthetic estimates **without** a human benchmark — because the benchmark is exactly what the synthetic panel was supposed to replace.
>
> The obvious candidate is to flag panels that return nearly identical dispersion for every segment. **We tested it against our own data and it fails.** Under one extraction path the model returns near-constant dispersion. Under another, the same model returns dispersion that varies **more** than the population's — in an unrelated direction. **A diagnostic tuned to the first pattern passes the second, which is the worse of the two.**
>
> Absence of information does not have a single observable signature. **So I am not going to sell you a screening rule.** What I can offer is narrower and I think it is true: **the number of segments a synthetic panel can actually distinguish is an empirical quantity, it is not the number of segments you queried, and in our audit it was close to zero.**

**[11:00 — Slide 10: o que derrubaria]**

> Three things would overturn this, and they are in the pre-registration.
>
> If the effect vanishes under item fixed effects, it is about the item, not the population. If our statistical baselines — a copula, a random forest — show the same flat slope, it is not about language models at all. And if frontier models reach a slope whose interval contains one, **the deficiency has been solved, and our contribution is to date its resolution.**
>
> **Any of those is a result. None of them is a failure.**
>
> Thank you.

**[11:50 — fim]**

---

**Contagem medida: 1.282 palavras faladas** (só o texto entre aspas, sem rubricas). A 130 palavras por minuto — ritmo de apresentação, não de leitura — são **9 min 52 s**. Somando as pausas marcadas, as trocas de slide e a respiração natural, fica em torno de **11 minutos**.

> ⚠️ **A margem é deliberada e não é folga.** Um roteiro cronometrado em 11:50 estoura na sala. Os ~2 minutos de sobra absorvem a pausa do slide 5, o tropeço inevitável e a chance de o moderador começar atrasado. **Se o ensaio der menos de 10 minutos, acrescente conteúdo ao slide 7 — não ao 5.**

---

## Os dez slides

| # | Slide | Conteúdo visual | Regra |
|---|---|---|---|
| 1 | Título | Título, nome, FGV. Nada mais | Sem logotipo grande, sem agenda |
| 2 | O que se sabe | Duas linhas: **médias ✓ · variância ✗** | Zero bullets além disso |
| 3 | **O artefato** | Duas barras: observado **−0,977** · ruído puro **−0,979** | ⭐ Um número ao lado do outro. **É todo o argumento** |
| 4 | O estimando | A equação e as duas âncoras: **β=1 fiel · β=0 sem informação** | Uma equação, no máximo |
| 5 | **O GRÁFICO** | Três painéis, diagonal tracejada, nuvem achatada, `n` e IC | **O único slide que pode levar 90 s** |
| 6 | A advertência | Duas linhas, fundo neutro | Deliberadamente feio. É honestidade, não venda |
| 7 | O estudo | Mapa do Brasil com o gradiente 39% / 15% + 4 linhas de método | Um mapa, não uma tabela |
| 8 | **A implicação** | Curva de cobertura descendo, linha tracejada em 0,95 | A Figura 2 mora aqui |
| 9 | O negativo | Os dois padrões de CV lado a lado — 6,2 e 0,27 | ⭐ Mostrar que o diagnóstico falha |
| 10 | Derrubada | Três condições, uma linha cada | Termina em texto, não em obrigado |

> **Regra de execução:** nenhum slide com mais de 20 palavras, exceto o 10. **Se um slide precisa ser lido, ele está competindo com você.**

---

## Preparação dos 3 minutos de perguntas

Sem discussant, as perguntas vêm da plateia e são previsíveis. **Resposta de 30 segundos, ensaiada, e depois parar de falar.**

| Pergunta provável | Resposta |
|---|---|
| *"Isso não é só regressão à média de qualquer preditor estatístico?"* | "Pode ser, e é por isso que temos cópula gaussiana e floresta aleatória como linhas de base no mesmo conjunto de métricas. Se elas achatarem igual, o achado é sobre respondentes sintéticos em geral e não sobre modelos de linguagem — **e a gente diz isso**." |
| *"Modelos novos não estão resolvendo isso?"* | "A inclinação mediana sobe com a data de lançamento: 0,056, 0,116, 0,173. Três pontos não são tendência, mas a direção é real e está no paper. **0,173 continua sendo um sexto de 1.** E incluímos um modelo antigo como âncora para medir isso em vez de afirmar." |
| *"Por que a variância seria fixa? Qual o mecanismo?"* | "**Não sei, e o paper não afirma saber.** É descritivo. Especular sobre RLHF sem testar seria pior que dizer que está em aberto." |
| *"Seu caminho primário tem viés conhecido de superdispersão."* | "Tem — Özkan documenta razões indo de 0,4 para 1,3. **É exatamente por isso que o estimando é uma inclinação e não um nível**, e a decisão está no pré-registro, não é defesa posterior. E testamos se a superdispersão é homogênea entre estratos, porque a defesa depende disso." |
| *"n = 15 células."* | "Todo ponto vem com intervalo de bootstrap, e o resultado é 11 de 12 combinações independentes, não uma." |
| *"Por que o Brasil?"* | "Porque preciso de dispersão dentro de uma língua. Um desenho entre países confunde país, língua e cobertura de corpus. **É escolha de identificação.**" |
| *"Isso replica com dado americano?"* | "O dado motivador **é** internacional e inclui os Estados Unidos. A coleta confirmatória é brasileira porque o benchmark é melhor: amostra probabilística e despesa observada, não painel de conveniência." |
| *"Vocês recomendam parar de usar painéis sintéticos?"* | "Não. Médias são recuperadas bem. **Recomendamos parar de usá-los para decisão de segmento**, que é justamente o que a maior parte do mercado está usando." |

---

## O plano de corte

**A regra do limite duro:** se aos 8:20 você não estiver no slide 8, corte.

| Ordem de corte | O que sai | Custo |
|---|---|---|
| 1º | O parágrafo dos quatro caminhos e três modos, no slide 7 | Baixo. Está no paper |
| 2º | A célula que rastreia perfeitamente (β = 1,03), no slide 5 | **Médio.** É honestidade, mas cabe na pergunta |
| 3º | Duas das três condições de derrubada, slide 10 | Baixo |
| **Nunca** | **Slides 3, 5 e 9** | ⭐ São o método, o achado e a honestidade. **Sem eles a fala não existe** |

---

## Por que o slide 9 fica, mesmo sendo o negativo

Um resultado nulo declarado voluntariamente, numa fala de 12 minutos onde ninguém obrigaria, faz três coisas de uma vez:

1. **Elimina a pergunta hostil mais provável** — a regra é circular — porque ela já foi respondida.
2. **Estabelece que os outros números não estão inflados.** Quem admite o que não achou compra credibilidade no que achou.
3. É **a coisa mais rara numa sessão de 60 minutos com quatro trabalhos.** Três vão vender. Um vai dizer o que não funcionou. **É esse que a plateia lembra no jantar.**

---

## Pendências finais do roteiro

- [ ] **Plotar as Figuras 1 e 2.** Ambiente sem `matplotlib`; os 45 pontos estão na M43 e os do NTP na M47.
- [ ] **Emendar o pré-registro da M12** — cinco mudanças materiais listadas na M47. **Antes de qualquer coleta.**
- [ ] Rodar a validação *leave-one-stratum-out* — pendente desde a M45.
- [ ] Ler Morocho et al. (ACM Web Conference 2026) a fundo — concorrente mais próximo com venue.
- [ ] Reverificar em novembro se Özkan e Rupprecht ganharam venue.
- [ ] Confirmar formato de submissão com `mike.nguyen@marshall.usc.edu` (canal da M34, não aparece no CFP).
- [ ] **Ensaiar com cronômetro.** O roteiro tem 13 segundos de margem e nenhuma tolerância a improviso.

---

> **Fim do roteiro. 48 missões.**
