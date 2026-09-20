# M04 — Operacionalizar "distância ao centro de massa do corpus"

Executada em 2026-08-21. Dois papers baixados e lidos, um verificado por metadados.

---

## Resumo do que esta missão muda

1. **Os proxies óbvios estão empiricamente refutados.** Dunn, Adams e Tayyar Madabushi mediram representação de 974 populações locais e concluíram que o viés **não é explicado por fatores socioeconômicos, geográficos nem sociolinguísticos**. Renda não prevê fidelidade. Tamanho de população não prevê fidelidade. Usar renda como proxy de distância seria assumir exatamente o que a literatura já testou e rejeitou.

2. **⚠️ Um dado corta contra a premissa do T2.** No mesmo paper, **o Brasil aparece entre os países com *menos* variação interna** na qualidade de representação. Se o Brasil for internamente homogêneo aos olhos do modelo, a variação identificadora do T2 encolhe. Há uma refutação boa e honesta desse dado — está na seção 4 — mas ela precisa ser feita explicitamente no paper, não ignorada.

3. **A saída é reformular a pergunta.** O T2 não deve *escolher* uma medida de distância a priori. Deve tratar **"qual noção de distância prevê o decaimento de fidelidade?"** como pergunta empírica. Isso resolve a anomalia da M02 (renda alta é central no texto e periférica no comportamento), transforma uma fraqueza de desenho em achado, e é mais defensável diante de um revisor.

---

## 1. O problema, e por que a M02 o agravou

A hipótese do T2 exige uma variável contínua que ordene estratos por "distância ao centro de massa do corpus de treino". A M02 mostrou que a intuição sociodemográfica falha: o único estrato onde Brand, Israeli e Ngwe acharam **coeficiente de preço positivo** — violação de teoria da demanda — foi renda acima de US$ 150 mil. Consumidor rico, americano e anglófono deveria estar no centro do corpus, não na borda.

Isso obriga distinguir pelo menos três noções de "distância", que não coincidem:

| Noção | O que mede | Onde renda alta cai |
|---|---|---|
| **D1 — Densidade textual** | Quanto texto daquele grupo existe no corpus de pré-treino | **Centro** |
| **D2 — Densidade comportamental** | Quantos dados de *escolha observada* daquele grupo existem (conjoint, painel de consumo, carrinho) | **Periferia** |
| **D3 — Distância cultural** | Quão diferente o grupo é do grupo modal em dimensões de valor e atitude | Intermediário |

A anomalia de renda alta é evidência a favor de D2. Mas D2 é a mais difícil de medir e a mais especulativa. Esta missão precisa decidir o que é operacionalizável em 90 dias.

---

## 2. As medidas candidatas

### Candidata A — Sondagem por perplexidade (Dunn, Adams e Tayyar Madabushi)

**Referência verificada:** DUNN, Jonathan; ADAMS, Benjamin; TAYYAR MADABUSHI, Harish. *Pre-Trained Language Models Represent Some Geographic Populations Better Than Others*. arXiv:2403.11025v1, 16 de março de 2024. University of Illinois Urbana-Champaign; University of Canterbury; University of Bath.

**Método, em detalhe, porque é o mais importável:**

- Tarefa de **sondagem espacial**: mede a **perplexidade de cada sub-corpus local** sob o modelo, para determinar se o modelo considera corpora comparáveis ao redor do mundo igualmente prováveis.
- Escala: mais de **86.000 sub-corpora**, **130 países**, **927 aeroportos** representando áreas metropolitanas num raio de 25 km, **974 populações locais**.
- **Controle de língua:** tudo em inglês, uma única língua franca, para que a variação observada não seja variação de língua.
- **Controle de tópico e registro** — e este é o truque metodológico que o T2 deve copiar: constroem um conjunto de **250 itens lexicais comuns**, escolhidos para não serem nem puramente funcionais (`the`, `is`) nem puramente tópicos (`Biden`). Para cada localidade, montam sub-corpora com **um tweet único por palavra-chave**. Isso força as populações a falarem sobre o mesmo conjunto de assuntos, de modo que a diferença de perplexidade reflita a população e não o tema.
- Padronização por **escore z** entre todas as amostras de cada modelo; zero é a média global.
- Modelos: séries **bloom** (560M, 1,7B, 3B) e **opt** (350M, 1,7B, 3B), para testar se escala aumenta representatividade.

**Resultados relevantes:**

- EUA e Reino Unido bem representados; Sul e Sudeste Asiático mal representados. México entre os de menor perplexidade, apesar de o inglês não ser majoritário.
- As duas famílias de modelos compartilham **o mesmo viés** — não é idiossincrasia de um modelo.
- Escala **não fecha o gap**.
- Fazem análise **dentro de países** (urbano contra rural), que é precisamente o eixo de que o T2 precisa.

**O resultado negativo, que é o achado mais importante para esta missão:**

> *"this skew cannot be fully explained by sociolinguistic factors, economic factors, or geographic factors."*

Testaram PIB per capita, tamanho populacional e volume de viagem aérea internacional como proxy de conectividade. Nenhum explica. Sobre tamanho: *"we see no clear relationship between population size and fit with the model"*, com a leve tendência sendo artefato de China e Índia. Sobre riqueza: *"not the case that wealth alone drives the degree of fit."*

**Conclusão para o T2: qualquer proxy assumido é indefensável. A distância precisa ser medida, não estipulada.**

### Candidata B — Índice de fixação cultural (CFst)

**Referência verificada:** MUTHUKRISHNA, Michael; BELL, Adrian V.; HENRICH, Joseph; CURTIN, Cameron M.; GEDRANOVICH, Alexander; McINERNEY, Jason; THUE, Braden. *Beyond Western, Educated, Industrial, Rich, and Democratic (WEIRD) Psychology: Measuring and Mapping Scales of Cultural and Psychological Distance*. **Psychological Science**, 2020. DOI 10.1177/0956797620916782. PMID 32437234.

Constrói o **CFst** por analogia direta com o índice de fixação F_ST da genética de populações. No F_ST, mede-se quanto as frequências genotípicas de cada subpopulação divergem do esperado sob acasalamento aleatório na população inteira — ou seja, o grau em que as populações podem ser consideradas estruturadas e separadas. Para herança cultural, o análogo é a diferenciação entre grupos causada por seleção, migração e mecanismos de aprendizado social.

**O que o torna atraente para o T2:** os autores afirmam explicitamente que o CFst serve para *"regional, national, or **arbitrary cultural groupings (such as class differences)**"*, e permite medir distância entre dois grupos tanto por agregado de muitas dimensões culturais quanto ao longo de dimensões arbitrárias escolhidas pela teoria.

Código em R publicado; ferramenta on-line em `culturaldistance.com`.

**Limitação:** depende de dados de survey de valores com resolução intra-brasileira suficiente. Verificar cobertura do World Values Survey para o Brasil com desagregação por classe e região. **Pendência para a M05.**

### Candidata C — Participação populacional do estrato

Peso amostral do estrato na PNAD ou POF. Simples, oficial, ponderado.

**Refutada como medida primária** pelo resultado de Dunn et al.: tamanho de população não prevê fidelidade. Serve como covariável de controle, não como a variável de interesse.

### Candidata D — Pegada digital do estrato

Proxy de quanto texto aquele estrato **produz**, não quanto ele **é**. Análogo brasileiro ao proxy de viagem aérea usado por Dunn et al. Fontes candidatas: suplemento de TIC da PNAD Contínua (acesso à internet, posse de celular), participação em comércio eletrônico.

**Atraente teoricamente** — é o proxy mais direto de D1 disponível em dado oficial. **Fraco empiricamente** — Dunn et al. testaram conectividade e ela não explicou o viés.

### Candidata E — Perplexidade da própria descrição da persona

Barato e direto: medir a perplexidade do texto de condicionamento sob o modelo. Zero infraestrutura externa.

**Rejeitada como medida principal.** Mede a fluência da descrição, não a representação do grupo. Uma persona periférica descrita em prosa fluente terá perplexidade baixa. Serve como controle, para descartar a hipótese de que o efeito seja artefato de redação do prompt — e nesse papel é obrigatória.

---

## 3. A decisão

**O T2 não escolhe uma medida. Ele testa qual medida prevê o decaimento.**

A pergunta de pesquisa ganha um segundo andar:

> **RQ1.** A fidelidade do respondente sintético decai de forma sistemática ao longo dos estratos, ou o erro é aleatório como afirmam Boelaert et al.?
> **RQ2.** Se decai, **qual noção de distância** — textual, comportamental ou cultural — prevê o decaimento?

Isso é estritamente melhor que a formulação anterior, por quatro razões:

1. **Sobrevive ao resultado negativo de Dunn et al.** Não assume proxy nenhum; deixa os dados decidirem.
2. **Resolve a anomalia da M02.** Se D2 (densidade comportamental) prevê melhor que D1 (densidade textual), a inversão de sinal em renda alta deixa de ser anomalia e vira confirmação.
3. **Blinda contra a ameaça de Boelaert et al.** Eles afirmaram aleatoriedade; a RQ2 só faz sentido se houver estrutura, e responder RQ2 já é refutá-los.
4. **É um achado mesmo se o resultado for nulo.** "Nenhuma noção de distância prevê o erro" é publicável e útil — significa que o profissional não tem como saber ex ante onde não confiar, o que é uma advertência forte.

### A hierarquia proposta

| Papel | Medida | Justificativa |
|---|---|---|
| **Primária** | Perplexidade por estrato, método Dunn et al. adaptado | Única medida do campo que é medida e não estipulada; controla tópico e registro por construção |
| **Secundária** | CFst intra-Brasil por classe e região | Publicada em *Psychological Science*, com código e ferramenta; explicitamente destinada a recortes de classe |
| **Terciária** | Pegada digital do estrato (PNAD TIC) | Proxy direto de produção textual; barata |
| **Controle** | Participação populacional do estrato | Dunn et al. mostram que não prevê; entra para demonstrar que não prevê aqui também |
| **Controle** | Perplexidade da descrição da persona | Descarta artefato de redação do prompt |
| **Aspiracional** | Densidade comportamental (D2) | Sem fonte óbvia. Ver pendências |

### Adaptação necessária no método de Dunn et al.

O método deles é geográfico e em inglês. O T2 precisa dele **socioeconômico e em português**. Três adaptações:

1. **Unidade de análise** deixa de ser área metropolitana e passa a ser célula sociodemográfica. Isso exige um corpus em português **rotulado por estrato**, que é o gargalo real — ver pendências.
2. **Os 250 itens lexicais de controle** precisam de equivalente em português, construídos com o mesmo critério: nem funcionais, nem tópicos.
3. **A língua deixa de ser controle e vira parte do objeto.** Rodar a mesma sondagem em português e em inglês dá, de graça, a comparação de língua que o T1 queria fazer.

---

## 4. ⚠️ O dado que corta contra a premissa, e a resposta honesta

Dunn et al. reportam desvio padrão da perplexidade média **dentro** de cada país, como medida de heterogeneidade interna de representação. Reino Unido 0,19; Austrália 0,22; Nigéria 0,27; Canadá 0,31; Alemanha 0,34; Tailândia 1,09; Colômbia 1,10.

E o texto diz: *"Canada, **Brazil**, and Australia have **less internal variation** (regardless of how well the model fits the population)."*

**Se o Brasil é internamente homogêneo aos olhos do modelo, a variação identificadora do T2 encolhe.** Um revisor com este paper em mãos levanta isso, e com razão.

### A refutação, que precisa estar no paper

Três argumentos, em ordem de força:

1. **O eixo é outro.** A medida deles é **geográfica** — áreas metropolitanas. A do T2 é **socioeconômica**. Um país pode ser homogêneo entre cidades e profundamente heterogêneo entre classes. No Brasil, especificamente, a desigualdade é muito mais de classe do que de região metropolitana, e as regiões metropolitanas concentram justamente a população conectada.

2. **A amostra brasileira deles é uma fatia estreita do Brasil.** Eles coletam **tweets em inglês**. Brasileiro que tuíta em inglês é urbano, escolarizado e de renda alta — precisamente o estrato central. Baixa variação interna medida sobre uma amostra já selecionada no centro é **artefato de seleção**, não evidência de homogeneidade. Este é o argumento mais forte e é verificável.

3. **A medida é de fit linguístico, não de fidelidade de resposta.** Perplexidade sobre texto produzido mede quão previsível o texto é. Não é a mesma coisa que a acurácia da distribuição de resposta simulada. A correlação entre as duas é uma hipótese, e testá-la é parte do T2.

**Registrar como ameaça formal na M08.** E note que o argumento 2 implica um requisito de desenho: o corpus brasileiro de sondagem tem de ser **em português** e amostrado de forma a cobrir estratos de baixa renda, ou o T2 repete o mesmo erro de seleção.

---

## 5. Achado lateral: existe hierarquia de previsibilidade por construto

**Referência verificada:** KU, Chan-Tung; HSU, Chan; HUANG, Pei-Cing; LIU, Frank Cheng-shan; CHENG, I-Ling; KANG, Yihuang. *Silicon Sampling via Cross-Survey Transfer*. arXiv:2607.03091. National Sun Yat-sen University e National Chung Hsing University, Taiwan.

Propõem **transferência entre surveys**: dar ao modelo as respostas de um indivíduo a um conjunto de questões e pedir que preveja as respostas dele a um conjunto **disjunto** de questões do mesmo survey. Argumentam que a avaliação distribucional dominante *"risks conflating pattern matching with coherent respondent-level prediction"* — e observam que mesmo o Estudo 3 de Argyle, que usa 11 itens para prever um 12º, avalia correspondência distribucional e não acurácia individual.

Dados: **TEDS 2024** (Taiwan Election and Democratization Study), três LLMs de peso aberto (27B a 120B), linhas de base de aprendizado supervisionado.

Achados:
- Zero-shot atinge **52%** de acurácia em itens genuinamente não vistos, a **6 pontos percentuais** de uma floresta aleatória supervisionada treinada na mesma população.
- **Hierarquia estável de previsibilidade por construto: 67% para atitudes partidárias, 23% para soberania.**
- Colapso de variância **também afeta os modelos supervisionados** — ou seja, não é patologia exclusiva de LLM.
- Efeitos de alinhamento variam dramaticamente entre famílias de modelo.

**Três implicações para o T2:**

- A **hierarquia de construtos** é a confirmação empírica da intuição de Brand et al. sobre hierarquia de dificuldade de momentos (ver M02). O eixo "complexidade do construto" existe e é mensurável. Reforça a hipótese de interação registrada na M02.
- A escolha deliberada de contexto **não-WEIRD e não-anglófono**, justificada exatamente como o T2 se justifica, é **precedente favorável** — mostra que o argumento vende. E é **concorrência**, porque alguém já ocupou o nicho "silicon sampling fora do Ocidente".
- O achado de que **colapso de variância afeta também modelos supervisionados** é uma ameaça a interpretações ingênuas: parte do colapso pode ser propriedade de qualquer preditor treinado, não específica de LLM. **O T2 precisa de uma linha de base supervisionada** para separar as duas coisas. Isso não estava no desenho e agora está.

---

## 6. Especificação operacional

```
Para cada estrato s (definido na M05):

  D1(s) = perplexidade média padronizada (escore z) de um sub-corpus
          em português rotulado como pertencente a s, construído com
          controle lexical de ~250 itens no padrão Dunn et al.

  D3(s) = CFst(s, s_modal) calculado sobre dimensões de valor do WVS
          Brasil, com s_modal = estrato de maior densidade populacional

  Dd(s) = índice de pegada digital do estrato (PNAD TIC)

  Ctrl1(s) = participação populacional de s
  Ctrl2(s) = perplexidade do texto de condicionamento da persona de s

Desfecho:
  E(s) = erro de fidelidade do respondente sintético no estrato s,
         medido por Wasserstein-1 normalizada (M01) e TV (M03)

Modelo:
  E(s) = f(D1, D3, Dd | Ctrl1, Ctrl2) + ε
  Forma funcional e teste de não-linearidade: M09
```

---

## Pendências geradas

- [ ] **Gargalo crítico:** de onde vem um corpus em português **rotulado por estrato socioeconômico**? Candidatos a investigar: dados de survey com resposta aberta e demografia anexa; corpora de redes sociais georreferenciados por setor censitário; transcrições de atendimento. **Se não houver fonte, D1 cai e a hierarquia inteira precisa ser refeita.** Esta é a maior ameaça de viabilidade do T2 até agora.
- [ ] **M05:** verificar cobertura do World Values Survey para o Brasil com desagregação por classe e região, para viabilizar o CFst.
- [ ] **M05:** confirmar existência e granularidade do suplemento de TIC da PNAD Contínua.
- [ ] **M06:** construir a lista de ~250 itens lexicais de controle em português.
- [ ] **M08:** registrar formalmente a ameaça da baixa variação interna do Brasil e a refutação por seleção amostral.
- [ ] **Desenho ganha componente novo:** linha de base supervisionada (floresta aleatória ou similar sobre PNAD/POF) para separar colapso de variância genérico de colapso específico de LLM.
- [ ] Investigar se existe fonte de **densidade comportamental** (D2) para o Brasil — dados de conjoint, painel de consumo, scanner. Sem isso, D2 fica como hipótese não testável e a anomalia da M02 fica sem resposta empírica.
- [ ] Verificar se Dunn et al. (2024) saiu em periódico ou anais além do arXiv.
