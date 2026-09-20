# M47 — Responder às objeções da M46 dentro do texto

Executada em 2026-08-21.

> A M46 encontrou seis objeções e deixou três lacunas. Esta missão **fechou as três** — e a maior delas produziu uma **auto-refutação**: o teste que a M46 mandou fazer derruba a solução que a própria M46 propôs.

---

## Resumo — o que mudou nesta missão

| | Estado ao fim da M46 | Estado agora |
|---|---|---|
| `NTP-GPT-4T` não rodado | 🔴 lacuna mais visível | ✅ **rodado — e refuta o diagnóstico do R4** |
| 4 citações `[NÃO VERIFICADO]` | 🔴 nenhuma com venue | ✅ **4 de 4 verificadas**, 2 com venue formal |
| Afirmação central | "uma variância serve para todos" | ⭐ **"a variância do modelo não informa a variância da população"** — mais geral e sobrevive em 11 de 12 |
| Regra gerencial | diagnóstico sem benchmark (R4 da M46) | 🔴 **refutado. Vira hipótese pré-registrada, não contribuição entregue** |

---

## 1. O teste que faltava — `NTP-GPT-4T`

A M46 registrou: *"Não testei o caminho NTP, que está em disco e é o modelo mais recente do pacote. É o teste mais óbvio que sobrou e o revisor vai fazê-lo."*

Rodei. O caminho NTP devolve a distribuição de probabilidade sobre as opções por perfil; a distribuição prevista da célula é a mistura dos perfis, e a variância da mistura é o análogo da variância entre personas do caminho FA. Massa mínima de 0,5, células `NA` excluídas, 15 células, bootstrap de 4000 réplicas.

| Item | n | Inclinação | IC 95% | r(V_h,V_m) | CV_H | CV_M | CV_H/CV_M |
|---|--:|--:|:--:|--:|--:|--:|--:|
| Felicidade | 15 | **+0,128** | [+0,014, +0,355] | +0,377 | 0,202 | 0,656 | **0,31** |
| Participação religiosa | 15 | **+0,321** | [−0,197, +0,746] | +0,317 | 0,225 | 0,839 | **0,27** |
| Posição política | 15 | **−0,019** | [−0,043, +0,061] | −0,272 | 0,347 | 0,459 | **0,76** |

**Os três intervalos excluem 1,0.** O achado sobrevive no modelo mais recente do pacote e no segundo caminho de extração.

### ⚠️ Mas o mecanismo é outro, e isso derruba o R4

No caminho FA a razão `CV_H/CV_M` ia de 2,6 a 6,2 — a variância do modelo era **quase fixa** entre estratos. É de onde saiu "uma variância serve para todos".

**No caminho NTP a razão inverte: 0,27 a 0,76.** A variância que o GPT-4T devolve **varia mais entre estratos do que a variância humana varia**. Ele não está devolvendo o mesmo espalhamento para todo mundo. Está devolvendo espalhamentos bem diferentes — **na direção errada**. Em posição política, a inclinação é −0,019: literalmente nenhuma informação.

> 🔴 **O diagnóstico que a M46 propôs no R4 falha exatamente aqui.** Aquela regra dizia: *"se a dispersão entre segmentos que o modelo devolve for muito menor que a esperada na população, rejeite."* O GPT-4T pela via NTP **passaria** nesse teste — sua dispersão entre segmentos é maior que a humana — e é o pior caso da tabela inteira.

**A M46 propôs um diagnóstico sem benchmark. Não existe.** Registro isso como resultado da missão, não como falha dela: a M46 acertou ao matar a versão circular da M45; errou ao supor que o substituto funcionava. Só rodando o segundo caminho dava para saber.

---

## 2. A afirmação que sobrevive a tudo

Consolidando **4 modelos × 2 caminhos × 3 itens = 12 combinações**:

| Caminho | Modelo | Felicidade | Posição política | Part. religiosa |
|---|---|--:|--:|--:|
| FA | GPT-3 | +0,515 ✓ | +0,037 ✓ | +0,038 ✓ |
| FA | Mixtral-8x7B | +0,366 ✓ | +0,124 ✓ | −0,070 ✓ |
| FA | Llama-3-70B | **+1,031 ✗** | +0,168 ✓ | +0,031 ✓ |
| NTP | GPT-4T | +0,128 ✓ | −0,019 ✓ | +0,321 ✓ |

*(✓ = IC 95% exclui 1,0)*

> ⭐ **Em 11 de 12 combinações a inclinação é significativamente menor que 1.** A única exceção é Llama-3-70B em felicidade — item de 4 pontos, o menor espaço de resposta do conjunto.

**A afirmação passa a ser esta, e é mais geral que a anterior:**

> **A variância que um modelo devolve para um estrato não é informativa sobre a variância daquele estrato na população.** Em alguns modelos isso aparece como variância quase constante; em outros, como variância que varia bastante mas em direção não relacionada. **A forma do erro difere; a ausência de informação não.**

Isso é melhor que "uma variância serve para todos" por três razões: é verdadeiro nos dois caminhos, é medido por um estimando não mecânico, e **não sobrevive a qualquer dado** — a célula Llama-3-70B × felicidade mostra que o teste pode falhar e falhou.

---

## 3. As citações — quatro fechadas, com venue

A M46 deixou quatro afirmações da M42 sem verificação. **Todas verificadas.**

| # | Afirmação | Fonte verificada | Venue | Estado |
|---|---|---|---|:--:|
| 1 | Superdispersão do caminho *describe*, razões 0,4–0,56 → 1,26–1,37 | **Gürkan Özkan** (Istanbul Technical University), *Distribution-First Population Simulation: Collapse, Calibration, and Recall in Non-WEIRD LLM Persona Modeling*, arXiv:2607.18310v1 [physics.soc-ph], 17 jul. 2026 | preprint, **sem venue** | ✅ |
| 2 | Viés de recência | **Rupprecht, Ahnert & Strohmaier**, *Prompt Perturbations Reveal Human-Like Biases in Large Language Model Survey Responses*, arXiv:2507.07188, v1 jul. 2025, v3 out. 2025 | preprint, **sem venue** | ✅ |
| 3 | Tendência sistemática ao "não" | **Daniel Braun** (Marburg), *Acquiescence Bias in Large Language Models* | **Findings of EMNLP 2025** | ✅ ⭐ |
| 4 | Deriva de distribuição entre meses | **Chen, Zaharia & Zou**, *How Is ChatGPT's Behavior Changing over Time?*, arXiv:2307.09009 | **Harvard Data Science Review** | ✅ ⭐ |

### Correções obrigatórias que a verificação produziu

**3.1 — Özkan: adotar a terminologia dele.** O método não se chama "describe path". Chama-se **Verbalized Sampling (VS)**. Os números conferem exatamente:

| Modelo | Linha de base *silicon* | Verbalized Sampling |
|---|--:|--:|
| GLM-5.2 | 0,46 | 1,26 |
| Qwen3.6-35B | 0,56 | 1,36 |
| Gemma-4-26B | 0,40 | 1,37 |

Citação exata: *"The same move throws every model from under-dispersion (0.40–0.56) to over-dispersion (1.26–1.37): VS corrects variance collapse by pushing variance past the target, a structural property rather than one model's quirk."*

> ⚠️ Özkan é preprint de julho de 2026 **sem venue**, de autor único. É o pilar da 5.3 da M42. **Citar como preprint, com data, e não apoiar nele nenhuma afirmação que o T2 não teste por conta própria.**

**3.2 — Braun: são tarefas de classificação, não itens de survey.** ⚠️ Cinco modelos, **9 tarefas de classificação binária** em três línguas — inglês (7 tarefas do LegalBench), alemão (1, AGB-DE), polonês (1, LEPISZCZE). A M42 descreveu como viés de resposta em survey. **Não é.** A extrapolação para itens sim/não de questionário é inferência minha, e o texto tem de dizer isso. **A afirmação de que não foi caracterizado em português continua válida** e continua sendo o achado lateral do T2.

**3.3 — Rupprecht: o número exato não está no resumo.** O resumo confirma a direção — *"all tested models exhibit a consistent recency bias, disproportionately favoring the last-presented answer option"* — sobre 9 LLMs e mais de 167 mil entrevistas simuladas com itens do WVS. O ganho de mais de 2000% para Llama-3.1-8B ao mover a opção para o fim está no texto completo, não no resumo. **Citar como "mais de 2000% num modelo", não como "até vinte vezes em geral".** A formulação da M42 — *"All tested models favor the last-presented option, by up to a factor of twenty"* — confunde **preferência posicional média** com **efeito de mover a opção**. São coisas diferentes e a segunda é a que o paper mede.

### Bônus — um concorrente novo, com venue

**Morocho, Cima, Fagni, Avvenuti & Cresci**, *Assessing the Reliability of Persona-Conditioned LLMs as Synthetic Survey Respondents*, arXiv:2602.18462, fev. 2026 — publicado em **Companion Proceedings of the ACM Web Conference 2026**, DOI 10.1145/3774905.3795477. Mais de 70 mil instâncias respondente-item.

> ⚠️ Achado deles: *"most items exhibit minimal change, while a small subset of questions and underrepresented subgroups experience disproportionate distortions."* **Isso antecipa parcialmente o R3 e parcialmente a hipótese de estrato do T2.** Tem de entrar na revisão de literatura e o T2 tem de dizer o que acrescenta: eles reportam que a distorção se concentra; o T2 **mede a inclinação e testa se ela é prevista pela largura da escala**.

---

## 4. As reescritas — texto de entrega

### 4.1 H1, reescrita (responde R1)

> **H1.** Let `Var[H_s]` denote the variance of the outcome within stratum *s* in the population, and `Var[M_s]` the variance of the corresponding synthetic distribution. We estimate the slope β in `Var[M_s] = α + β·Var[H_s] + ε_s`. **A model that reproduced population dispersion would have β = 1; a model whose dispersion is uninformative about the stratum would have β = 0. We predict β significantly below 1, and test it against that null rather than against zero.**
>
> We test against β = 1 deliberately. **The conventional null of β = 0 is uninformative here**: it asks whether the model has any relation to the population, when the question of interest is whether it has enough.

### 4.2 Nota metodológica obrigatória (responde R1)

Vai na 5.5, e é meia contribuição metodológica por si:

> **A note on a metric we do not use.** Much of this literature summarizes dispersion error as the log variance ratio, `ln(Var[M_s]/Var[H_s])`, and reports its correlation with population variance. **That correlation is mechanically negative and carries almost no information.** Because the ratio contains `Var[H_s]` in its denominator, a synthetic variance generated at random, with no relation whatever to the population, reproduces the observed correlation: in our data the observed value is −0.977 and a null in which model variance is independent gaussian noise with matched mean and standard deviation yields −0.979 (90% interval −0.989 to −0.966). **We report the log variance ratio descriptively and base no inference on it.**

### 4.3 Seção 4, renomeada e requalificada (responde R6.1 e R2)

> **4. Motivating Evidence**
>
> Before describing our own collection we report an analysis of an existing public replication package, to establish that the phenomenon we set out to measure is present in data we did not generate.
>
> [Autor et al.] released synthetic responses for four models against World Values Survey items for five countries. We recompute, at the level of **country × educational attainment**, the slope of synthetic variance on population variance for three items and two extraction paths.
>
> **Two qualifications are essential and we state them before the result.** These are opinion items in five high-income and middle-income countries, not consumption in Brazil; and the strata are defined by **education**, not by income. This analysis motivates the study. It does not test its hypothesis.
>
> Across twelve model-by-item combinations, **eleven have a bootstrap confidence interval for the slope that excludes 1**. [Table]. The single exception is the largest model on the item with the fewest response options.

> ⭐ A frase *"This analysis motivates the study. It does not test its hypothesis"* é barata e desarma o R6.1 inteiro. **Escrevê-la antes do resultado, e não depois, é o que a torna crível.**

### 4.4 A emenda à 5.3 (responde R6.5)

A defesa da M42 supunha, sem testar, que a superdispersão do VS é homogênea entre estratos.

> **[acrescentar ao fim da 5.3]** This argument requires that the over-dispersion introduced by verbalized sampling be approximately constant across strata; if the method over-disperses more in some strata than others, it is not a location shift and the correlation is not protected. **We test this directly**, regressing the log dispersion ratio of the verbalized-sampling path against stratum indicators, and report the result whether or not it supports the assumption. **Where the assumption fails, we report the affected strata and restrict the primary estimate to those where it holds.**

### 4.5 Duas subseções novas de robustez (responde R3 e R5)

> **7.9 Response-scale width**
>
> *Threat.* The slope may be a property of the item's response space rather than of the population. In our motivating data the spread across items — median slope 0.52 on a four-point item against 0.04 on a seven-point item — **exceeds the spread across models**.
>
> *Test.* A factorial arm. Each of four consumption constructs is measured on 3-, 5-, 7- and 11-point scales, with strata held fixed, so that scale width is manipulated rather than observed. We test whether the slope declines in scale width and whether the stratum coefficient survives item fixed effects.
>
> *Overturning condition.* **If the slope is fully accounted for by scale width, the finding is about response granularity and not about population representation, and we will say so.** We regard that outcome as a publishable result under a different title, not as a failure.
>
> **7.10 Model generation**
>
> *Threat.* The deficiency may be shrinking with each model generation, making a 2027 finding obsolete on arrival. In our motivating data the median slope rises with release date: 0.056, 0.116, 0.173.
>
> *Test.* The audited set spans four years of releases, including a deliberately dated anchor model, so that generation is measured rather than asserted. We report the slope by release date.
>
> *Overturning condition.* **If the frontier models reach a slope whose interval contains 1, the deficiency has been solved and our contribution is to date its resolution.** We consider that a result and would report it as one.

### 4.6 A 8.2, terceira versão — o que resta depois do R4 cair

A versão da M45 era circular. A versão da M46 é refutada pelo dado NTP. **O que sobra é menor e é honesto.**

> **8.2 What a manager can and cannot compute**
>
> It would be valuable to offer a rule that identifies unreliable synthetic estimates without a human benchmark. **We looked for one and we report that we did not find one.**
>
> The natural candidate — flagging panels that return near-identical dispersion for every segment — fails on our own data. Under one extraction path the model returns nearly constant dispersion across strata; under another, the same phenomenon appears as dispersion that varies *more* than the population's, in an unrelated direction. **A diagnostic tuned to the first pattern passes the second, which is the worse of the two.** Absence of information about the population does not have a single observable signature.
>
> What can be computed is a **calibration, performed once**. Estimating the slope requires benchmark variances for a set of strata on a set of items — obtainable from any weighted public survey, and in most markets already public. The open question, which we pre-register rather than claim, is **how far a slope estimated on one set of outcomes transports to others**. Our motivating data is discouraging on this point: slopes vary more across items than across models, which suggests calibration must be item-specific. **If that holds, the cost advantage of synthetic panels for segment-level work is smaller than currently assumed, because each new outcome requires its own calibration.**
>
> The defensible statement for practice is therefore narrow: **the number of segments a synthetic panel can actually distinguish is an empirical quantity, it is not the number of segments queried, and in our audit it was close to zero.**

> **Isso é uma reivindicação bem menor que a da M45.** E é a única que quatro modelos e dois caminhos sustentam. **Prometer a regra e não entregá-la seria a única forma de perder o paper na sessão.**

---

## 5. Mapa objeção → onde ela é respondida

| Objeção da M46 | Onde é respondida | Como |
|---|---|---|
| **R1** correlação mecânica | H1 (4.1) + nota na 5.5 (4.2) | Estimando trocado; a nota **antecipa a objeção com a simulação** |
| **R2** "classe" é escolaridade | Seção 4 (4.3) | Declarado antes do resultado; renda e escolaridade cruzadas nos 60 estratos da M41 |
| **R3** dependência do item | 7.9 (4.5) | Vira **braço fatorial**, com condição de derrubada |
| **R4** regra circular | 8.2 (4.6) | ⭐ **Abandonada explicitamente.** "We looked for one and we report that we did not find one" |
| **R5** melhora por geração | 7.10 (4.5) | Reportada como tendência e transformada em hipótese datada |
| **R6.1** domínio diferente | Seção 4 (4.3) | *"This analysis motivates the study. It does not test its hypothesis"* |
| **R6.2** sem mecanismo | Seção 9 | ⚠️ **Não respondida.** Declarada como questão aberta. **Especular sobre RLHF sem testar é pior que silêncio** |
| **R6.3** n = 15 | Todas as tabelas | IC bootstrap em todo ponto estimado |
| **R6.4** célula EUA n = 105 | Nota da Figura 1 | Marcada visualmente |
| **R6.5** superdispersão heterogênea | 5.3 emendada (4.4) | Pressuposto declarado **e testado** |
| **R6.6** célula `NA` | — | Corrigida na M46; todos os números refeitos |

**Dez de onze respondidas no corpo.** A décima primeira — mecanismo — é declarada como limite, que é a resposta correta.

---

## 6. O que continua aberto

- ⚠️ **A validação *leave-one-stratum-out*** que a M45 pediu **continua sem ser feita.** Com a 8.2 reduzida a calibração, ela deixou de ser condição de sobrevivência de uma seção, mas continua sendo o teste natural da transportabilidade da inclinação. **Roda com o dado em disco.**
- ⚠️ **Não verifiquei se algum dos oito premiados de 2026 já reporta inclinação em vez de correlação** — pendência aberta desde a M46. Se reportarem, a nota da 4.2 vale menos.
- ⚠️ **Özkan e Rupprecht são preprints sem venue.** Ambos sustentam decisões de método. Reverificar em novembro; se ainda não tiverem venue, **o texto tem de dizer "preprint" explicitamente**.
- ⚠️ **Morocho et al. (ACM Web Conference 2026) precisa ser lido a fundo**, não só pelo resumo. É o concorrente mais próximo com venue e pode cobrir mais do T2 do que parece.
- 🔴 **O pré-registro da M12 tem de ser emendado antes de qualquer coleta.** Mudaram: o estimando (inclinação, nulo 1,0), o fator de largura de escala (7.9), a âncora de geração (7.10), o teste de homogeneidade da superdispersão (5.3) e a retirada da regra de triagem. **São cinco mudanças materiais.**
- **M48 herda:** a apresentação de 12 minutos. ⭐ **A mensagem única mudou.** Não é mais "uma variância serve para todos" — é **"a variância que o modelo devolve não diz nada sobre a variância da população, e isso vale em 11 de 12 testes"**. A Figura 2 continua sendo a abertura.
