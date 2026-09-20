# M45 — Discussão e implicações gerenciais

Executada em 2026-08-21.

---

## A ideia que organiza a seção

O achado do T2 não é "respondente sintético falha". Isso já está publicado.

**É que a falha é computável antes de gastar dinheiro.**

Boelaert et al. descrevem o erro como aleatório entre tópicos. Se for aleatório, o profissional não tem saída: cada aplicação exigiria o benchmark humano que o painel sintético deveria substituir. **Se for estruturado, e a estrutura for uma função de uma quantidade observável, então existe uma regra de triagem.**

> **A implicação gerencial do T2 é uma regra de decisão, não uma advertência.** É a diferença entre "cuidado" e "aqui está o que fazer" — e é o que separa este paper dos anteriores para um público que inclui um professor de prática com quinze anos de CRM (M33).

---

## Seção 8 — texto de entrega

> **8. What This Costs, and What Can Be Done About It**
>
> **8.1 The cost, in the units practitioners use**
>
> The practical question is not whether synthetic respondents are imperfect. It is whether a firm that uses them is worse off than one that does not, and by how much.
>
> Two of our measures translate directly. The first is **effective sample size**. Under the standard survey formulation, a set of synthetic responses is worth the number of independent human observations that would produce the same precision. In our strata, [X] synthetic responses carry the information of approximately [X] human respondents — a design effect of [X]. A firm that budgets a synthetic panel as though it were a human panel of the same nominal size is overstating its evidence by that factor.
>
> The second is **interval coverage**, and it behaves in a way that inverts standard intuition. A 95% confidence interval computed from synthetic responses in the ordinary way contains the benchmark value in [X]% of strata. More importantly, **that share falls as more synthetic responses are collected**. This is not a paradox. The number of queries submitted to a model is a researcher's design choice, not a sampling constraint: increasing it shrinks the interval around the estimate without moving the estimate toward the population. The interval converges on the wrong value, and it converges tightly.
>
> The operational statement is therefore uncomfortable and simple. **Collecting more synthetic data does not reduce the probability of being wrong. It reduces the probability of noticing.**
>
> **8.2 A screening rule**
>
> If the error were unpredictable, the only defensible response would be to abandon the method or to validate every application against human data — which would eliminate the cost advantage that motivates it. Our result points to a third option.
>
> Because model variance is approximately fixed while population variance is not, the strata in which synthetic data fails worst are the strata in which the true population is most and least dispersed relative to that fixed value. And population dispersion is **observable in advance**, from any weighted benchmark, without querying a model at all.
>
> This yields a screening rule that costs nothing to apply:
>
> 1. For the target population, compute the variance of the outcome within each segment of interest, using existing weighted survey data.
> 2. Compare each segment's dispersion against the model's fixed dispersion, estimable once from any calibrated sample.
> 3. **Segments whose true dispersion is far from that fixed value are the segments where synthetic estimates should not be used for decisions** — regardless of how plausible the synthetic responses appear.
>
> The rule does not rescue synthetic panels for segment-level work. It identifies, ex ante, where they are least defensible — which is precisely what the prior literature concluded was impossible. Brand, Israeli, and Ngwe observe that in each of their failure cases a researcher lacking a human benchmark would have had no basis for identifying which estimates were unreliable. **Our result supplies that basis, and it requires the benchmark only once, not once per application.**
>
> **8.3 Where synthetic respondents remain defensible**
>
> Our findings do not argue for abandoning the method. Means are recovered well, and simple aggregate moments are recovered well. Synthetic panels remain reasonable for questions about population averages, for pilot exploration before fielding a human study, and for generating hypotheses. They are not reasonable for questions whose answer depends on dispersion — segment targeting, tail identification, willingness-to-pay ranges, or any decision that rests on how much a population disagrees with itself.

**≈ 620 palavras.**

---

## Seção 9 — texto de entrega

> **9. Limitations**
>
> **The benchmark predates the models.** Our reference survey was fielded in 2017–2018 and the audited models were trained on later data. We address this with a drift covariate, a replication on data extending to 2024, and a temporal placebo against an earlier survey wave, and we report all three. None of these eliminates the gap for consumption categories that did not exist in 2018, and results for such categories should be read with that in mind.
>
> **One country, one language.** Brazil was chosen because it supplies within-country dispersion without confounding language and nation. That choice buys identification and costs external validity: we cannot say whether the fixed-variance property holds at the same magnitude in markets with different corpus representation. The direction of the relationship should generalize more readily than its slope.
>
> **One layer of variance.** We measure dispersion across personas within a stratum. Studies measuring dispersion across repeated calls on a single persona, or across strata, are measuring different quantities, and our estimates should not be read against theirs without adjustment. We report the alternative layer separately for that reason.
>
> **Results are dated by construction.** Model behavior drifts, and the same prompt has been shown to yield materially different distributions months apart. We record exact dated model versions, freeze prompts by hash, and retain raw responses so that the audit can be re-run. We expect the magnitudes to change. **We do not expect the structure to, and that is the claim we make.**
>
> **We measure fidelity, not usefulness.** A synthetic panel that misrepresents dispersion may still improve a decision relative to no data at all. Establishing that would require a different design, comparing decision quality rather than distributional distance.

**≈ 400 palavras.**

---

## As decisões de redação

| Decisão | Razão |
|---|---|
| **A seção 8 vem antes das limitações** | A M33 pediu implicação de decisão. Enterrar isso depois das limitações desperdiça a peça mais forte |
| **A regra de triagem em três passos numerados** | Um professor de prática lê passos. Prosa sobre "implicações" não é acionável |
| **A citação de Brand, Israeli e Ngwe reaparece aqui** | Ela abre a lacuna na introdução e **fecha na discussão** — é o arco do paper: eles disseram que não havia base, e o T2 fornece a base |
| **A 8.3 diz onde o método ainda serve** | ⭐ Um paper que só destrói parece motivado. Delimitar o uso legítimo é honesto **e** mais persuasivo |
| **"Results are dated by construction"** | Antecipa a objeção de que o achado envelhece. E a resposta — magnitude muda, estrutura não — **é a afirmação forte, declarada como tal** |
| **A última limitação é a mais generosa** | Admitir que fidelidade ≠ utilidade abre a porta para o próximo paper em vez de fingir completude |

---

## O arco do paper, agora fechado

| Seção | Movimento |
|---|---|
| 1. Introdução | *"a researcher lacking a human benchmark would have had no basis"* — o problema |
| 4. Evidência sem modelo | A variância do modelo não se move |
| 6. Resultados | E não se mover é sistemático |
| **8.2 Regra de triagem** | **Logo, existe a base que faltava** |
| 9. Limitações | E aqui está o que ela não cobre |

**A mesma frase abre e fecha o argumento.** É o recurso estrutural mais simples que existe e o mais eficaz em texto curto.

---

## O que NÃO entrou

| Fora | Por quê |
|---|---|
| Contribuição teórica ampla sobre representação em modelos | Espaço caro; a AIM premia achado, não teoria (M01) |
| Recomendação de política pública | É o T1, não o T2 |
| Qualquer menção a Foucault ou à dissertação | M31 — dois textos, dois públicos |
| Agenda de pesquisa futura longa | Uma frase na última limitação basta |
| Desculpa pelo contexto brasileiro | M35 |

---

## Pendências geradas

- [ ] Fechar os `[X]` de tamanho efetivo, efeito de desenho e cobertura após a análise.
- [ ] Verificar se a regra de triagem da 8.2 sobrevive à validação cruzada *leave-one-stratum-out* — **se não sobreviver, a seção inteira cai** e vira advertência em vez de regra.
- [ ] Testar a regra numericamente antes de afirmá-la: quantificar quanto erro ela evitaria numa aplicação simulada.
- [ ] Confirmar a formulação exata da citação de Brand, Israeli e Ngwe usada na introdução e aqui.
- [ ] **M46 herda:** a regra de triagem é a afirmação mais forte do paper e o alvo mais provável do revisor hostil.
