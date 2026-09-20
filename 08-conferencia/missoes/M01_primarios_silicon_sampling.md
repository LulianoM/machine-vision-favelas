# M01 — Os primários de silicon sampling: desenho, métricas, N e trabalho futuro

Executada em 2026-08-21. Fontes lidas em texto integral, exceto Bisbee (ver nota de acesso).

---

## Resumo do que esta missão muda

Três coisas, em ordem de importância para o T2:

1. **Santurkar et al. deixam o T2 escrito na seção de limitações.** Verbatim: *"our conclusions are only valid for the populations in the US, to which ATP surveys are targeted. Many societies differ from WEIRD (Western, Educated, Industrialized, Rich and Democratic) societies such as the United States (Henrich et al., 2010) and **there is a need for future work on global equivalents to OpinionQA**."* Isto é uma licença explícita de trabalho futuro, assinada por Stanford, em ICML. Vai na introdução do paper.

2. **A métrica que eu havia recomendado por intuição é a métrica canônica do campo.** Santurkar et al. constroem o alinhamento sobre **distância de Wasserstein de ordem 1**, normalizada. Não é escolha exótica minha — é o padrão que o revisor espera. Ganhamos precedente e perdemos o risco de parecer improviso.

3. **O desenho de Argyle tem um ponto cego que o Brasil expõe.** Eles corrigem marginais enviesadas amostrando *backstories* de uma distribuição conhecida (ANES) em vez da distribuição implícita do modelo. Isso conserta a **composição** da amostra, não a **fidelidade condicional** dentro de cada célula. Se a fidelidade decai com a distância ao centro de massa do corpus, a correção de marginais de Argyle *mascara* o problema: a média agregada melhora enquanto os estratos periféricos continuam errados. Essa é a brecha exata do T2.

---

## 1. Argyle, Busby, Fulda, Gubler, Rytting e Wingate (2023)

**Referência verificada:** *Out of One, Many: Using Language Models to Simulate Human Samples*. **Political Analysis**, 31(3), 2023.
**Texto lido:** preprint arXiv:2209.06899v1 (14 set 2022). ⚠️ Números conferidos contra o preprint; a versão de *Political Analysis* pode ter mudado detalhes. Reconferir antes de citar número específico.

### Desenho

Condicionamento do **GPT-3 Davinci** (175B) em *backstories* sociodemográficas em primeira pessoa, construídas por templating a partir de participantes humanos reais. Um "sujeito de silício" por participante humano. Temperatura **0.7**.

Fontes humanas: **ANES 2012, 2016 e 2020**, e o dataset *Pigeonholing Partisans* de Rothschild et al.

### Os quatro critérios de fidelidade algorítmica

Este é o aparato conceitual que o campo herdou, e que o T2 precisa citar e depois estressar:

| Critério | Definição |
|---|---|
| 1 — Social Science Turing Test | Respostas geradas são indistinguíveis de textos humanos paralelos |
| 2 — Backward Continuity | A resposta é consistente com o contexto de condicionamento, a ponto de um humano inferir elementos do input |
| 3 — Forward Continuity | A resposta decorre naturalmente do contexto de condicionamento |
| 4 — Pattern Correspondence | Os padrões de relação entre ideias e atitudes espelham os da população humana |

Note o que **não** está aí: nenhum critério exige que a *variância* da resposta sintética corresponda à humana. A fidelidade é definida sobre indistinguibilidade e sobre padrão de correlação — as duas coisas que sobrevivem ao colapso de moda. **É por isso que Argyle acha fidelidade e Bisbee acha colapso: eles não estão medindo a mesma coisa.** Este parágrafo vale um bloco inteiro na revisão de literatura do T2.

### N por estudo

- **Estudo 1** (texto livre partidário): **2.107** participantes humanos do Pigeonholing Partisans → 2.107 indivíduos de silício. Cada um listava quatro palavras sobre Republicanos e quatro sobre Democratas (2.107 × 2 listas se houvesse conformidade total). Corpus final de **7.675 textos únicos** humanos + GPT-3. Julgamento tipo Turing feito via Lucid, com 120/7.675 (1,5%) perdidos por falha de servidor. **Custo de API do Estudo 1: US$ 29.**
- **Estudo 2** (predição de voto): ondas ANES 2012, 2016, 2020. Correlações tetracóricas de **0,90 (2012), 0,92 (2016), 0,90 (2020)**.
- **Estudo 3** (fechadas e correlações complexas): amostra de silício de participantes virtuais da ANES, **N = 1.782**.

### O achado que interessa ao T2 — e que Argyle publica sem alarde

Na tabela de estatísticas descritivas do Estudo 3 (linha 2242 do preprint):

| Variável | Fonte | N | Média | D.P. |
|---|---|---|---|---|
| Idade | ANES | 1.782 | 50,14 | 17,56 |
| Idade | GPT-3 | 1.782 | **35,49** | **12,59** |

Duas coisas ao mesmo tempo: a média sintética é **14,7 anos mais jovem** e o desvio padrão é **28% menor**. Isto é colapso de variância aparecendo dentro do próprio artigo fundador, num apêndice, sem ser nomeado como tal. Vale citar exatamente assim.

E em temperatura 0,001: *"GPT-3 identified all respondents as white"* — perda total de variância racial, a ponto de impedir o cálculo do V de Cramér. Evidência direta de que **o parâmetro de amostragem controla o colapso**, o que obriga o T2 a tratar temperatura como variável de desenho, não como configuração.

### Limitações declaradas pelos autores

- Não avaliam correspondência em **nível individual**, só distribucional. *"we do not expect the values in the silicon sample to exactly match the human response on the individual level."*
- Estudo restrito a **um domínio** (política e opinião pública nos EUA). Convite explícito: *"the underlying methodology is general purpose and calls for additional work to quantify both the extent and limitations of GPT-3's algorithmic fidelity in a wide array of social science fields. Such an effort goes well beyond what one research team can hope to accomplish; we extend this invitation to the wider scientific community."*

Segunda licença explícita de trabalho futuro. O T2 aceita o convite em outro domínio (consumo) e em outra população (não-WEIRD, com variação interna).

### A correção de marginais — e por que ela não salva o T2

Argyle reconhecem que a distribuição de *backstories* que o GPT-3 produziria por conta própria, P(B_GPT3), não bate com a populacional, P(B_True). A solução deles é amostrar *backstories* de uma distribuição conhecida (ANES) e calcular P(V|B_ANES)·P(B_ANES).

**Isto corrige composição, não fidelidade condicional.** Se P(V|B) é enviesado de forma heterogênea — pior nas células periféricas — a reponderação por marginais conhecidas produz uma média agregada bonita sobre células individualmente erradas. É exatamente a patologia que a função de decaimento do T2 quer expor.

---

## 2. Santurkar, Durmus, Ladhak, Lee, Liang e Hashimoto (2023)

**Referência verificada:** *Whose Opinions Do Language Models Reflect?* **ICML 2023**, PMLR v202. Lido em texto integral.

### Desenho

Constroem o **OpinionQA** a partir dos *American Trends Panels* do Pew: **1.498 questões**, tópicos de ciência a política a relações pessoais. Avaliam **9 LMs** (350M a 178B parâmetros, AI21 Labs e OpenAI) contra a população geral dos EUA e **60 grupos demográficos**.

Extração de opinião por **log-probabilidade do próximo token** sobre as letras das alternativas (‘A’, ‘B’, …), ignorando todas as demais continuações. Recusa tratada separadamente das demais alternativas.

### Os três eixos de avaliação

1. **Representatividade** — quão alinhada é a distribuição de opinião padrão do modelo com a população. Achado: desalinhamento substancial, *"on par with the Democrat-Republican divide on climate change"*.
2. **Direcionabilidade** (*steerability*) — o modelo consegue emular um grupo quando instruído? Achado: melhora, mas **modesta**; *"none of the aforementioned representativeness problems are resolved by steering"*.
3. **Consistência** — os grupos com que o modelo se alinha são estáveis entre tópicos? Achado: **não**. `text-davinci-002/003`, genericamente liberais, expressam visões conservadoras em religião.

### Três formas de condicionamento (nomenclatura a herdar)

| Modo | Como o grupo é informado |
|---|---|
| `QA` | Como resposta a uma pergunta de múltipla escolha anterior, na fraseologia do Pew |
| `BIO` | Como texto livre biográfico — **é o modo de Argyle**, citado como tal |
| `PORTRAY` | Instrução direta para fingir ser membro do grupo |

O T2 deve rodar os três e reportar separadamente. São a variação de instrumento mais barata que existe e o revisor vai perguntar.

### A métrica — precedente para o T2

Distância de **Wasserstein de ordem 1** entre distribuições de opinião, com alternativas ordinais mapeadas para inteiros positivos. Alinhamento definido como:

```
A(D₁, D₂; Q) = (1/|Q|) · Σ_q [ 1 − WD(D₁(q), D₂(q)) / (N − 1) ]
```

onde N é o número de alternativas excluindo recusa, e (N−1) é a WD máxima naquele espaço métrico. Limitada em [0, 1]; 1 é correspondência perfeita.

Detalhes de mapeamento que o T2 herda de graça: alternativa de recusa é omitida do cálculo e comparada à parte; alternativa final de hedge ("Nem um nem outro", "Mais ou menos o mesmo") é mapeada à média das ordinais restantes (ex.: ‘Muito bom’, ‘Muito ruim’, ‘Nem bom nem ruim’ → 1, 2, 1,5).

### Grupos mal representados por **todos** os modelos

**65+, mórmons e viúvos.** Note o padrão: idade alta, minoria religiosa, estado civil menos frequente. Todos são células de **baixa densidade no corpus** — sustenta empiricamente a hipótese de decaimento por distância ao centro de massa, ainda que os autores não formulem assim.

### Limitações declaradas

- **A licença do T2**, verbatim: *"our conclusions are only valid for the populations in the US, to which ATP surveys are targeted. Many societies differ from WEIRD societies such as the United States (Henrich et al., 2010) and there is a need for future work on global equivalents to OpinionQA."*
- Formato de múltipla escolha difere do uso aberto real; questão em aberto se o alinhamento medido assim se transfere.
- O ATP tem problemas conhecidos de **viés de desejabilidade social** (Yan, 2021), o que contamina a própria distribuição humana de referência.
- Advertência de uso: as métricas são *probes*, **não benchmark a ser otimizado indiscriminadamente**.

---

## 3. Bisbee, Clinton, Dorff, Kenkel e Larson (2024)

**Referência verificada:** *Synthetic Replacements for Human Survey Data? The Perils of Large Language Models*. **Political Analysis**, 32(4), 401–416, outubro de 2024. Cambridge University Press.

> ⚠️ **Nota de acesso.** O texto integral está atrás do paywall da Cambridge e os espelhos (ResearchGate, site do autor, OSF) bloquearam download automatizado. Confirmei autoria, venue, volume, número, páginas, mês e ano por fonte bibliográfica (RePEc/IDEAS) e o conteúdo do resumo pela página do periódico. **Os números quantitativos abaixo vêm de fontes secundárias e estão marcados.** Conseguir o PDF pelo acesso institucional da FGV antes de citar qualquer número.

### Desenho (do resumo verificado)

ChatGPT instruído a adotar diferentes **personas** e fornecer notas de **termômetro de sentimento** para grupos sociopolíticos, comparadas a respondentes humanos pareados da **ANES 2016 e 2020**.

### Achados (resumo verificado)

- As **médias** sintéticas correspondem de perto às médias da ANES.
- *"less variation in responses than in the real surveys"* — colapso de variância.
- Coeficientes de regressão *"often differ significantly from equivalent estimates obtained using ANES data"*.
- A distribuição sintética muda com **alterações mínimas na redação do prompt**.
- O **mesmo prompt** produz resultados significativamente diferentes ao longo de um período de meses.
- Conclusão dos autores: *"findings raise serious concerns about the quality, reliability, and reproducibility of synthetic survey data generated by LLMs."*

### Números repetidos de forma consistente por fontes secundárias — [NÃO VERIFICADOS NO ORIGINAL]

- **11** grupos sociopolíticos avaliados.
- **48%** dos coeficientes de regressão estatisticamente diferentes dos equivalentes humanos.
- Janela de instabilidade temporal de **3 meses**.

Não usar nenhum destes três números no paper antes de abrir o PDF.

---

## 4. Síntese operacional para o T2

### O que herdar diretamente

| Elemento | Fonte | Como usar |
|---|---|---|
| Wasserstein-1 normalizada como métrica de alinhamento | Santurkar, eq. (1) | Métrica primária. Reportar exatamente na forma deles para comparabilidade. |
| Os três modos de condicionamento QA / BIO / PORTRAY | Santurkar | Rodar os três; reportar separado. Barato e esperado. |
| Extração por log-prob do próximo token | Santurkar | Onde o modelo permitir. Onde não permitir (APIs fechadas), documentar a alternativa. |
| Backstory em primeira pessoa por templating | Argyle | Base do instrumento do T2 (detalhar na M06). |
| Temperatura como variável de desenho | Argyle, apêndice | Grade de temperatura, não valor fixo. |
| Recusa tratada à parte; hedge mapeado à média ordinal | Santurkar, A.4 | Regra de codificação. |

### As três brechas que o T2 ocupa

1. **A fidelidade nunca foi definida sobre variância.** Os quatro critérios de Argyle cobrem indistinguibilidade e correspondência de padrão; nenhum exige correspondência de dispersão. O T2 propõe o critério ausente e o mede.

2. **A correção de marginais mascara heterogeneidade condicional.** Argyle consertam composição; ninguém testou se P(V|B) decai sistematicamente com a periferia de B. É a função de decaimento.

3. **O convite ao equivalente global foi feito e não foi atendido no eixo certo.** Santurkar pedem "equivalentes globais ao OpinionQA" — o que quase todo mundo leu como "faça outro país". A leitura mais forte é **dentro de um país de alta desigualdade**, onde a variação de distância ao centro de massa é grande com língua e nação fixas. E o T2 troca opinião por consumo, saindo do terreno lotado.

### Fricção nova detectada

O ATP tem viés de desejabilidade social documentado, e Santurkar admitem que isso contamina a referência humana. **A POF tem um problema análogo e conhecido**: subdeclaração de despesa em categorias socialmente sensíveis (álcool, tabaco, jogo). Se o T2 usar essas categorias, o "erro" medido mistura falha do modelo com falha do benchmark. **Decisão a tomar na M05:** ou excluir categorias sensíveis, ou tratar a diferença de desejabilidade como quantidade de interesse — o que seria um segundo achado, não um ruído.

---

## Pendências geradas

- [ ] Obter o PDF de Bisbee et al. (2024) pelo acesso institucional da FGV e reconferir os três números marcados.
- [ ] Reconferir os N e as correlações de Argyle contra a versão publicada em *Political Analysis* 31(3), não contra o preprint.
- [ ] Decidir na M05 o tratamento das categorias da POF com desejabilidade social.
- [ ] Verificar se as APIs a usar expõem log-probabilidade do próximo token; se não, definir o substituto na M06.
