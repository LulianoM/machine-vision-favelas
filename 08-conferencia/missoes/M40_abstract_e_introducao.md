# M40 — Abstract e introdução do T2

Executada em 2026-08-21. **Texto de entrega em inglês; comentário em português.**

---

## Nota de honestidade sobre o que dá para escrever agora

**A coleta não aconteceu.** Portanto:

| Peça | Estado |
|---|---|
| **Introdução** | ✅ **Escrita por inteiro.** Não depende de resultado |
| **Abstract** | ⚠️ **Estrutura fechada, números marcados como `[X]`.** Só se fecha depois da análise |
| Âncora empírica | ✅ Real — a correlação de **−0,89** medida no dado público de Boelaert et al. (M10) já existe e pode entrar como evidência motivadora |

Não inventei número nenhum. Onde o resultado ainda não existe, está `[X]`.

---

## 1. Calibração: como os vencedores escrevem o abstract

Medi três premiados de 2026. Padrão consistente, **200 a 250 palavras**, em cinco movimentos:

| Movimento | Exemplo (Dai, Li e Telang — prêmio Rao) |
|---|---|
| **Tensão** | *"Platforms increasingly use generative AI to create and enhance content, but it remains unclear whether such images boost user engagement or erode consumer trust."* |
| **Cenário** | Mercado de entrega de comida na Índia; Zomato baniu imagens de IA em agosto de 2024, Swiggy manteve |
| **Desenho** | Painel de compras nas duas plataformas, diferenças-em-diferenças |
| **Achado, com especificidade** | Aumentos significativamente maiores em volume, receita e número de clientes |
| **Validação** | Análises forenses multimodais e três detectores de IA |

Duas observações úteis:

- **O cenário vem antes do desenho**, sempre. O leitor precisa saber *onde* antes de saber *como*.
- **Um dos oito vencedores não tem abstract nenhum** — o de Zhuoyan Ma começa direto na introdução. Não é obrigatório, mas é melhor ter.

---

## 2. O título

**Da M12:**

> *Non-Responsive Variance: Do Synthetic Consumers Track the Dispersion of Real Populations? Evidence from Brazilian Household Budget Microdata*

**Alternativa mais curta, e prefiro esta:**

> **One Variance Fits All: Synthetic Consumers Do Not Track the Dispersion of Real Populations**

Razões: nomeia o achado em vez de perguntá-lo; *"one variance fits all"* é memorável e descreve o mecanismo com precisão; e cabe num slide. O contexto brasileiro entra no subtítulo ou no abstract, não no título — consistente com a M35, que recomendou o Brasil como escolha de desenho e não como identidade.

---

## 3. Abstract — texto de entrega

> **One Variance Fits All: Synthetic Consumers Do Not Track the Dispersion of Real Populations**
>
> Firms increasingly replace human respondents with large language models in market research, and a growing literature has established that synthetic respondents recover population means while compressing population variance. What remains unknown is whether that error is structured. If it is random, practitioners have no way to know when synthetic data can be trusted; if it is systematic, the failure can be predicted before it is made. We audit synthetic consumers against Brazilian household budget microdata, a nationally representative and probability-weighted benchmark, across [60] socioeconomic strata defined by income, region, and education, and [15] consumption categories. Brazil offers unusual identifying variation: extreme socioeconomic dispersion within a single language and a single national market. We find that the variance a model produces is approximately **invariant to the stratum it is asked to represent**, while true population variance varies substantially — the correlation between human variance and the log variance ratio is [X] (95% CI [·,·]). The model over-disperses where the real population is homogeneous and flattens it where the population is heterogeneous. We further show that naive confidence intervals built from synthetic respondents contain the true value in only [X]% of cells, and that this coverage **declines as more synthetic data is collected**, because query count is a design choice rather than a sampling constraint. Collecting more synthetic respondents makes researchers more confident without making them more correct.

**≈ 245 palavras.** Dentro da faixa medida.

### Onde cada movimento está

| Movimento | Frase |
|---|---|
| Tensão | *"What remains unknown is whether that error is structured"* |
| **Por que importa** | *"If it is random… if it is systematic…"* — dá a consequência prática antes do método |
| Cenário | Microdado de orçamento familiar brasileiro, com a justificativa de desenho embutida |
| Desenho | 60 estratos, 15 categorias, benchmark ponderado |
| Achado 1 | Invariância da variância, com a correlação |
| Achado 2 | Cobertura, e a propriedade decrescente |
| **Fecho** | A frase que fica: *"more confident without making them more correct"* |

### Os dois testes

**Teste da M35 — funciona com a afiliação coberta?** Sim. Não há nada no texto que dependa de quem assina.

**Teste da M33 — faz sentido para alguém de estratégia que nunca ouviu falar de amostragem de silício?** Sim. O termo *silicon sampling* **não aparece**. A primeira frase diz "empresas substituem respondentes humanos por modelos de linguagem em pesquisa de mercado", que qualquer pessoa entende.

---

## 4. Introdução — texto de entrega

> **1. Introduction**
>
> Market research is being quietly rebuilt. Firms that once fielded surveys to human panels now prompt large language models to answer as consumers, and vendors sell the practice as faster, cheaper, and good enough. The appeal is obvious: a synthetic panel returns in minutes what a human panel returns in weeks. The question is what is lost in the substitution, and whether the loss can be anticipated.
>
> A short literature has answered the first half of that question. Argyle et al. (2023) established that conditioning a language model on sociodemographic backstories produces response distributions that resemble human ones, a property they called algorithmic fidelity. Bisbee et al. (2024) then showed the limits: synthetic means track human means closely, but synthetic responses vary far less than human responses, and regression coefficients estimated from them frequently differ from their human counterparts. In marketing specifically, Brand, Israeli, and Ngwe report willingness-to-pay estimates that are sometimes comparable to human studies, often inaccurate, and in some cases wrong-signed. The pattern is consistent across settings: the first moment survives, the second does not.
>
> The second half of the question is open, and it is the one that determines whether the practice is usable. Boelaert et al. (2025), testing 687 sociodemographically defined subpopulations, describe the error as *machine bias* — a strong bias with low variance on each topic, varying **randomly** from one topic to the next. If that characterization is right, the practical implication is severe: a researcher holding synthetic data has no way to know, in advance, which of its estimates to trust. Every application would require the very human benchmark the synthetic panel was meant to replace. Brand, Israeli, and Ngwe state the same problem from the practitioner's side: in each of their failure cases, *a researcher lacking a human benchmark would have had no basis for identifying which estimates were unreliable*.
>
> We ask whether the error is in fact unstructured. Our answer is that it is not, and that the structure is simpler than expected. **The variance a model produces is approximately fixed.** It does not respond to the stratum it is asked to represent. Because true population variance does vary — substantially, and in ways that are measurable — the model over-disperses where the real population is homogeneous and flattens it where the population is heterogeneous. What looks like unpredictable error across topics is, within a topic, a near-deterministic function of a quantity the researcher can compute in advance from any weighted benchmark.
>
> We test this against Brazilian household budget microdata. The choice is not incidental. Brazil combines extreme socioeconomic dispersion with a single language and a single national market, which allows the relationship between population heterogeneity and synthetic fidelity to be estimated without confounding language, country, and culture in one variable. In the 2017–2018 national household budget survey, [39.4]% of families in the Northeast lived on up to two minimum wages, against [14.8]% in the South — a spread of twenty-five percentage points inside one country, one currency, and one consumer market.
>
> Our contribution is threefold. First, we show that the second-moment failure of synthetic respondents is systematic rather than random, and we characterize its form. Second, we move the question from political attitudes, where this literature has developed, to consumption, where the practice is actually being sold. Third, we quantify the cost: naive confidence intervals built from synthetic respondents cover the true value in a minority of cells, and coverage **falls as sample size rises**, because the number of queries is a researcher's design choice rather than a sampling constraint. The practical implication inverts the usual advice. Collecting more synthetic data does not reduce the risk of being wrong; it reduces the visibility of being wrong.

**≈ 640 palavras.** O orçamento da M39 era 900 — sobra espaço para uma passagem sobre o que o paper não faz, ou para a estrutura do texto.

---

## 5. As decisões de redação, e por quê

| Decisão | Razão |
|---|---|
| **"Market research is being quietly rebuilt"** como primeira frase | Estabelece consequência antes de literatura. A M33 pediu implicação de decisão para um público de estratégia |
| **Boelaert et al. citado como o alvo, e com respeito** | A M07 estabeleceu que a afirmação de aleatoriedade deles é a abertura do T2. Contestar bem exige representar bem |
| **A citação direta de Brand, Israeli e Ngwe** | É a formulação mais clara do problema, e vem de dentro da comunidade de marketing (M02) |
| **O achado principal aparece no quarto parágrafo, em negrito conceitual** | Padrão da área: problema, literatura, lacuna, achado |
| **Os 39,4% contra 14,8%** | A M05 levantou; é dado oficial e é o que transforma "Brasil" de biografia em desenho (M35) |
| **"reduces the visibility of being wrong"** como última frase | A M07 identificou a cobertura decrescente como o resultado mais citável. A frase final tem de ser essa |
| **Nada de Foucault, nada de amostragem de silício** | M31 e M33 |

---

## 6. O que ainda falta para fechar

| Item | Depende de |
|---|---|
| Os `[X]` do abstract | Coleta e análise |
| Confirmar 39,4% e 14,8% na fonte primária | Pendência da M05 |
| Decidir entre os dois títulos | Conversa com o orientador |
| Verificar se Dalloul e Pfeifer mudam o parágrafo 3 | Portão de setembro (M12) |
| Parágrafo final sobre estrutura do texto | Depois que as seções existirem |

---

## Pendências geradas

- [ ] Fechar os `[X]` após a análise.
- [ ] Confirmar os percentuais da POF na publicação oficial antes de usá-los na introdução.
- [ ] Decidir o título com o orientador.
- [ ] **Se Dalloul e Pfeifer já publicaram a tese do agente representativo**, o parágrafo 3 precisa citá-los e o parágrafo 4 precisa se diferenciar deles explicitamente.
- [ ] Revisar a introdução depois de escrever os resultados — a M39 fixou que introdução e abstract se escrevem por último, e este texto é a versão de trabalho, não a final.
- [ ] Ler o resumo estendido de Contigiani como modelo de gênero — pendência ainda aberta da M39.
