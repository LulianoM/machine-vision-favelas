# M13 — Doshi e Hauser: a métrica de diversidade, o que há no Dryad e o que é replicável

Executada em 2026-08-21. **Texto integral lido** via PubMed Central. Abre o Bloco B (T3).

---

## Referência verificada

DOSHI, Anil R.; HAUSER, Oliver P. *Generative AI enhances individual creativity but reduces the collective diversity of novel content*. **Science Advances**, v. 10, n. 28, eadn5290, 12 de julho de 2024. DOI 10.1126/sciadv.adn5290. PMC11244532. PMID 38996021.

Afiliações: Doshi no **Department of Strategy and Entrepreneurship, UCL School of Management**; Hauser no **Department of Economics** e no **Institute for Data Science and Artificial Intelligence, University of Exeter**.

Recebido em 14/12/2023, aceito em 07/06/2024, publicado em 12/07/2024. **Estudo pré-registrado.** Acesso aberto.

---

## Resumo do que esta missão muda

1. **A métrica de diversidade coletiva é mais simples do que eu supunha, e isso é bom.** Não é índice de diversidade semântica nem Sentence-BERT: é **cosseno entre o embedding da peça focal e o embedding médio de todas as outras peças do mesmo grupo**, multiplicado por 100. Uma linha de código. O T3 pode implementar hoje.

2. **⚠️ O efeito de homogeneização é pequeno em termos absolutos e os autores são explícitos sobre isso.** O aumento de similaridade é de **0,871 e 0,718 pontos** numa escala de 0 a 100, contra uma amplitude de apenas **8,10 pontos** na condição sem IA. Eles contextualizam como 10,7% e 8,9% da amplitude total. **O T3 precisa reportar amplitude, não só coeficiente**, ou o achado parece trivial.

3. **⚠️ O efeito é não-monótono, e isso não está no título.** Uma ideia de IA homogeneíza **mais** (0,871) do que cinco (0,718). Vale pensar por quê antes de assumir dose-resposta em qualquer desenho do T3.

4. **O Dryad tem apenas scripts, e o download exige autenticação.** `GenAI_creativity_scripts.zip` (2.472.080 bytes) e `README.md` (3.657 bytes), versão 6. A API devolve *"Unauthorized, must have current bearer token"* — precisa de download manual pelo navegador.

---

## 1. Desenho experimental

Estudo pré-registrado, on-line, em duas fases.

### Fase 1 — escritores

**N = 293.** Tarefa: escrever uma história curta de **oito frases**, "apropriada para público adolescente e jovem adulto", com a instrução explícita "você pode escrever sobre o que quiser".

Inspiração declarada: o gênero "micro" — microficção, micro-vídeos —, com referência à história de seis palavras atribuída a Hemingway.

**Três condições, por atribuição aleatória:**

| Condição | O que o escritor recebe |
|---|---|
| Human-only | Nada |
| Human + 1 ideia GenAI | Pode solicitar **uma** ideia de história gerada por LLM |
| Human + 5 ideias GenAI | Pode solicitar **até cinco** ideias |

Após escrever, autoavaliação da própria história em novidade, utilidade e características emocionais.

### A medida prévia de criatividade individual — o DAT

Antes de escrever, todos fazem a **Divergent Association Task**: fornecer **dez palavras tão diferentes entre si quanto possível**.

> **O escore DAT é a distância de cosseno entre os embeddings das palavras, escalada para 100.**

Requer que 7 das 10 palavras submetidas sejam válidas — palavra única, existente em dicionário. Dois escritores falharam, então o DAT foi computado para **291 dos 293**. Na amostra: **média 77,24, desvio padrão 6,48**.

Note a elegância: **a mesma família de operação — distância de cosseno sobre embeddings — mede tanto a criatividade individual prévia quanto a homogeneização coletiva posterior.** É um desenho metricamente coerente, e vale copiar essa coerência.

### Fase 2 — avaliadores

**N = 600**, grupo separado. Cada avaliador lê **seis histórias sorteadas**, sem ser informado de que houve atribuição aleatória a condições com ou sem IA. Cada história é avaliada por múltiplos avaliadores em novidade, utilidade e características emocionais.

Depois dos desfechos principais, e apenas para fins exploratórios, revelava-se o uso de IA e pedia-se opinião sobre divisão de propriedade e lucros hipotéticos entre escritor e IA.

---

## 2. A métrica de diversidade coletiva — o que o T3 precisa

Reprodução do trecho de método:

> *"Using embeddings obtained from OpenAI's embeddings application programming interface (API), we were able to compute the cosine similarity of the stories to all other stories within condition as well as the generative AI ideas. We multiply the cosine similarity score by 100 to arrive at a measure that ranges from 0 to 100."*

E a operacionalização específica, que é o detalhe que importa:

> *"We look at the similarity of any one story to the 'mass' of all stories within the same condition by computing the cosine similarity of the embedding of the focal story with the **average embedding of all other stories in the same condition**."*

### Formalizado

```
Para cada peça i no grupo g:

  ē_{g,−i} = média dos embeddings de todas as peças de g, exceto i

  Sim_i = 100 × cos( e_i , ē_{g,−i} )
```

O *leave-one-out* no cálculo da média é essencial — sem ele, a peça focal contamina o próprio referencial e a medida fica enviesada para cima em grupos pequenos. **É onde uma implementação apressada erra.**

### Duas coisas que eles medem e que o T3 deve medir também

1. Similaridade da peça **às outras peças do mesmo grupo** — a homogeneização propriamente dita.
2. Similaridade da peça **às ideias geradas pela IA** — que é o mecanismo. Sem essa segunda medida, sabe-se que houve convergência mas não para onde.

Para o T3, a segunda medida tem um análogo direto e barato: similaridade da entrega **ao output bruto da ferramenta** usada no processo, quando ele estiver registrado no Argos Core.

---

## 3. Resultados, com os números

### Criatividade individual sobe

| Desfecho | 1 ideia GenAI | 5 ideias GenAI |
|---|---|---|
| **Novidade** | +5,4% (b = 0,207, P = 0,021) | **+8,1%** (b = 0,311, P < 0,001) |
| **Utilidade** | +3,7% (b = 0,185, P = 0,039) | **+9,0%** (b = 0,453, P < 0,001) |

E cinco ideias superam uma em utilidade por **+5,1%** (P = 0,0012, contra média de 5,21 na condição de uma ideia).

### Diversidade coletiva cai

| | Aumento de similaridade | Significância |
|---|---|---|
| Human + 1 ideia | **b = 0,871** | P < 0,001 |
| Human + 5 ideias | **b = 0,718** | P = 0,003 |

**O contexto que os autores fornecem, e que o T3 deve imitar:** na condição Human-only, os escores de similaridade abrangem uma amplitude de **8,10 pontos**. Logo os aumentos representam **10,7%** e **8,9%** da amplitude total.

> ⚠️ **Sem essa normalização, o achado parece desprezível.** Um coeficiente de 0,871 numa escala de 0 a 100 lido isoladamente é ruído aparente. Contra a amplitude efetiva de 8,10 pontos, é um décimo da variação existente. **O T3 tem de reportar a amplitude do grupo de controle na mesma frase que o coeficiente.**

### ⚠️ A não-monotonicidade

Uma ideia homogeneíza **mais** (0,871) do que cinco (0,718). O título e o abstract não mencionam isso. Duas leituras possíveis, nenhuma testada por eles:

- **Ancoragem única.** Com uma só ideia, o escritor ancora nela integralmente. Com cinco, há escolha e recombinação, o que reintroduz variação.
- **Seleção de uso.** Na condição de cinco, todas as cinco ideias foram solicitadas apenas **24,5% das vezes** — a maioria dos escritores não esgotou o menu, então a dose efetiva é menor que a nominal.

**Consequência para o T3:** não assumir dose-resposta monótona entre intensidade de uso de IA e homogeneização. Se o T3 medir intensidade de adoção como variável contínua, precisa permitir forma não-linear — o que conecta com o teste de spline especificado na M09.

### Heterogeneidade por criatividade prévia

Não há diferença entre escritores mais e menos criativos na **frequência** de acesso às ideias de IA. Mas o efeito sobre o resultado é maior entre os **menos criativos** — o que sustenta a leitura de nivelamento por baixo do teto e por cima do piso.

---

## 4. O que há no Dryad e o que dá para replicar

**Conjunto:** DOI 10.5061/dryad.qfttdz0pm, versão 6, 2.475.737 bytes.

| Arquivo | Tamanho |
|---|---|
| `GenAI_creativity_scripts.zip` | 2.472.080 bytes |
| `README.md` | 3.657 bytes |

⚠️ **A API do Dryad recusa download automatizado:** `{"error":"Unauthorized, must have current bearer token"}`. **Baixar manualmente pelo navegador** na página do conjunto.

### O que provavelmente dá e o que provavelmente não dá

O nome do arquivo é `scripts`, não `data`. Duas hipóteses, e a diferença importa muito:

- **Se contiver apenas código:** replica-se o pipeline, mas **não** as 293 histórias. Sem o corpus, não há como recomputar embeddings nem verificar a medida de similaridade. Ainda assim, o código dá a implementação exata, incluindo o *leave-one-out* e o tratamento do DAT.
- **Se contiver o corpus de histórias:** replicação completa possível, e o T3 ganha um **conjunto de calibração** — pode-se validar a implementação própria contra os coeficientes publicados antes de aplicá-la às entregas da agência.

**A segunda hipótese vale a verificação manual imediata.** Calibrar o pipeline do T3 contra um resultado publicado, antes de rodá-lo em dado próprio, é a diferença entre um número defensável e um número que o revisor não tem como conferir.

---

## 5. O que transfere para o T3 e o que não transfere

### Transfere

| Elemento | Uso no T3 |
|---|---|
| Cosseno contra embedding médio *leave-one-out* | **Métrica central**, aplicada a entregas de clientes distintos |
| Multiplicação por 100 e reporte da amplitude do controle | Torna o coeficiente legível |
| Medir também similaridade ao output bruto da ferramenta | Identifica **para onde** o portfólio converge, não só que converge |
| Medida prévia de criatividade do executor | Análogo: senioridade, tempo de casa ou avaliação prévia do designer, para heterogeneidade |
| Coerência métrica entre a medida prévia e o desfecho | Usar a mesma família de operação nas duas pontas |
| Não-monotonicidade como possibilidade real | Permitir forma funcional flexível (spline, M09) |

### Não transfere — e são três problemas sérios

1. **Eles têm atribuição aleatória; o T3 tem adoção escalonada.** A identificação é muito mais fraca. O grupo de comparação deles é definido pelo desenho; no T3, o grupo é definido por tempo e estúdio, ambos endógenos.

2. **O "grupo" deles é a condição experimental; o do T3 é ambíguo.** Contra o que se mede a similaridade de uma peça? Outras peças do mesmo estúdio no mesmo trimestre? De clientes diferentes? Do mesmo setor? **Cada escolha define um contrafactual diferente e responde a uma pergunta diferente.** Precisa ser fixada e justificada antes da coleta — não é detalhe técnico, é a pergunta de pesquisa.

3. **Oito frases contra entregas heterogêneas.** As histórias têm comprimento e gênero controlados por construção. Entregas de agência variam em formato, extensão e mídia. Embeddings de textos de comprimentos muito diferentes não são diretamente comparáveis, e parte da variação de similaridade será variação de formato. **Exige normalização ou estratificação por tipo de entrega.**

---

## Pendências geradas

- [ ] **Baixar manualmente** `GenAI_creativity_scripts.zip` do Dryad e verificar se contém o corpus de histórias. Se sim, usar como conjunto de calibração do pipeline do T3.
- [ ] **Decidir o grupo de comparação do T3** — a escolha define a pergunta. Prioridade alta, precede qualquer coleta.
- [ ] Definir normalização por tipo e extensão de entrega, para que similaridade não capture formato.
- [ ] Verificar qual modelo de embedding da OpenAI eles usaram, e se ainda está disponível — se foi descontinuado, a replicação exata é impossível e é preciso declarar o substituto.
- [ ] Localizar o pré-registro do estudo (provavelmente AsPredicted ou OSF) para ver o que foi confirmatório e o que foi exploratório.
- [ ] **M14 herda:** comparar esta métrica com as alternativas da literatura de homogeneização (índices de diversidade semântica, Sentence-BERT) e justificar a escolha para o contexto de entregas de agência.
