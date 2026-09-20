# M02 — Brand, Israeli e Ngwe: categorias, método de WTP e onde o sinal inverteu

Executada em 2026-08-21. **Texto integral lido**, versão de 30 de abril de 2026.

---

## Nota de versão

**Referência verificada:** BRAND, James; ISRAELI, Ayelet; NGWE, Donald. *Using LLMs for Market Research*. Harvard Business School Working Paper 23-062. Página de rosto com copyright **2023, 2024, 2025 e 2026**; data do manuscrito **30 de abril de 2026**. Circulou antes com o título *"Using GPT for Market Research"*.

Afiliações: Brand e Ngwe no **Office of the Chief Economist, Microsoft**; Israeli em **Harvard Business School**. Isto importa: dois dos três autores são economistas da Microsoft, o que dá ao paper peso de indústria e explica o uso de Surface como estímulo.

Apresentado em USC, Wharton, MIT, HBS, ACM EC'24, JSM e MSI/ARF, entre outros. **Inclusive na USC** — o que significa que parte da comissão da AIM já viu este trabalho. Assumir familiaridade da plateia.

---

## Resumo do que esta missão muda

Quatro achados, todos favoráveis ao T2:

1. **Eles tentaram recuperar heterogeneidade demográfica, por várias vias, e falharam — e publicam isso.** Verbatim: *"We have not, in our investigation, been able to have GPT meaningfully reflect heterogeneous preferences across demographic groups."* O estado da arte do lado marketing declara nulo exatamente onde o T2 trabalha.

2. **Eles declaram a variância fora do escopo.** Verbatim: *"Characterizing sampling variance for LLM-generated data raises unique challenges that are beyond the scope of this paper."* Não reportam erro padrão nenhum para estimativas de LLM. Porta aberta e sinalizada.

3. **A falha aparece localizada num estrato específico, e é uma violação de teoria da demanda.** Nota de rodapé 17: *"GPT always implies a negative price coefficient, **except for the case of higher income (above $150,000) customers, where the price coefficient is positive**."* Ou seja: no estrato de renda alta o modelo diz que o consumidor prefere preço maior. Isso não é ruído — é o erro concentrado numa célula demográfica. É a hipótese do T2 visível a olho nu no paper que fundou a área.

4. **A amostra humana de referência deles é enviesada, e eles sabem.** *"tends to be younger, more educated, more likely to identify as Democrats, and lower income compared to the general population."* O benchmark humano é ele próprio não representativo — o que reforça o argumento do T2 de ancorar em **microdado oficial** (POF/PNAD) e não em painel de conveniência.

---

## 1. As três perguntas de pesquisa

Formuladas explicitamente:

1. LLMs conseguem simular preferências de consumidor **fora da caixa**?
2. LLMs conseguem recuperar **heterogeneidade de preferência entre grupos demográficos**?
3. Dados prévios de survey humano podem ser usados para **fine-tuning** e melhorar o alinhamento com novos surveys, inclusive para novos atributos?

Respostas dos autores: (1) parcialmente e de forma não diagnosticável; (2) **não**; (3) sim, dentro da mesma categoria e população, e não fora.

**A pergunta 2 é a pergunta do T2, respondida com um nulo.** O T2 não a repete — ele estrutura o nulo, mostrando que o erro não é aleatório e sim função da posição do estrato.

---

## 2. Desenho experimental

### Piloto

Réplica no espírito de **Fong et al. (2023)**, um conjoint de mundo real conduzido no fim de 2020 cujas estimativas os autores confirmaram serem consistentes com resultados de mercado. Rodado em **março de 2023** com **text-davinci-003**, escolhido porque o corte de treino do modelo não poderia incluir os resultados de Fong et al.

Categorias do piloto: **creme dental** (flúor) e **desodorante** (alumínio). Apenas marca, preço e ingrediente.

### Estudos principais

Cinco surveys humanos próprios, com participantes reais:

| Estudo | Categoria | Atributos | Amostra humana |
|---|---|---|---|
| Piloto A | Creme dental | Flúor | 401 participantes, Fong et al. (2023) |
| Estudo 1A | Creme dental | Flúor, sabores convencionais | 300 participantes |
| Estudo 1B | Creme dental | 1A + **sabores incomuns** (pepino, panqueca) | 302 participantes |
| Estudo 2A | Laptop | Armazenamento, RAM, tamanho de tela | 302 participantes |
| Estudo 2B | Laptop | 2A + **projetor embutido** (feature nova) | 300 participantes |
| Estudo 2C | Tablet | Mesmos atributos do laptop, níveis diferentes | — |

Estímulos de marca: Colgate/Crest, Dove/Speed Stick, Microsoft Surface Laptop vs Macbook, Microsoft Surface vs iPad.

**A arquitetura de teste é elegante e vale copiar:** a feature nova (sabor incomum, projetor) é o teste de extrapolação — algo que não existe no mercado e portanto não pode estar no corpus.

### Modelos comparados

Principal: **GPT-3.5 Turbo**, formalmente `gpt-3.5-turbo-0125`. Estudos principais rodados entre **abril e julho de 2024**.

Réplica do Estudo 2A em: **GPT-4o, Claude 3 Haiku, Claude 3.5 Sonnet, LLaMA-3 8B e LLaMA-3 70B**, apresentados em ordem de número de parâmetros.

Achados entre modelos:
- GPT-3.5 Turbo e GPT-4o aproximam-se mais da amostra humana do que Claude e LLaMA-8B.
- **LLaMA-8B subestima preferências significativamente** — os autores atribuem ao tamanho.
- **Claude tem a preferência de tamanho de tela mais distante dos humanos entre todos os modelos.**
- Mesmo entre GPT-4o e GPT-3.5 Turbo há divergências relevantes: no Estudo 2B, a WTP implícita por GPT-4o é de aproximadamente **US$ 333**, muito distante da do 3.5.

Verbatim: *"Across different LLMs, we find substantial variation in estimates, underscoring that results are not robust to model choice."*

### Repetições

- Estudos principais: **150 respostas por conjunto**, reduzidas depois para **50**.
- Réplicas entre modelos: **50 repetições por prompt**, totalizando **288.900** por LLM.
- Exceção: **LLaMA-3 70B com apenas 2 repetições por prompt**, 11.556 prompts no total, por limite computacional.
- Análises de segmento e do modelo com fine-tuning: **30 respostas por grupo**.

### Fine-tuning

Transformam respostas de surveys humanos anteriores em pares de prompt e resposta idênticos aos do estudo-alvo e ajustam os pesos do modelo. **300 participantes × 12 questões = 3.600 respostas** de treino.

Desenho de extrapolação: treinar em 1A (sabores convencionais) e avaliar em 1B (sabores incomuns); treinar em 2A (laptop) e avaliar em 2B (projetor) e 2C (tablet).

---

## 3. Método de estimação de WTP

Modelo de escolha **logit multinomial**. WTP calculada dividindo o **coeficiente do atributo pelo valor absoluto do coeficiente de preço**.

### O parágrafo metodológico mais importante do paper para o T2

> *"We note that LLM responses are simulation-based responses, and are therefore akin to counterfactual simulation responses. However, unlike most settings, we know neither the data used to estimate the LLMs nor the model structure, meaning we have no way to precisely characterize sampling uncertainty arising from the LLM. **We therefore do not report standard errors for LLM-based estimates throughout the paper.** Characterizing sampling variance for LLM-generated data raises unique challenges that are beyond the scope of this paper. More fundamentally, **the number of queries submitted to the LLM is a researcher design choice rather than a sampling constraint.**"*

Três consequências diretas para o T2:

1. **Eles não reportam erro padrão nenhum.** O T2 pode ser o trabalho que resolve isso, e a lacuna está assinada pelos próprios autores.
2. **N não é tamanho de amostra, é escolha de desenho.** Isso quebra a inferência clássica: aumentar consultas estreita o intervalo sem adicionar informação sobre a população. Vai direto para a **M10** (cálculo de poder) — a regra de parada do T2 não pode ser "N até o intervalo fechar".
3. A incerteza relevante não é amostral, é **de especificação**: qual modelo, qual versão, qual prompt, qual temperatura. O T2 deve tratar essas quatro como fatores de um desenho fatorial, não como configuração.

---

## 4. Onde exatamente o sinal inverteu

Lista completa das falhas nomeadas pelos autores, com GPT-3.5 Turbo na linha de base sem fine-tuning:

| Falha | Natureza | Estudo |
|---|---|---|
| **Flúor em creme dental** | Superestima WTP em cerca de **3×** | Magnitude |
| **Sabores novos de creme dental (pepino, panqueca)** | **Sinal errado** | Inversão |
| **Tela maior de laptop** | **WTP negativa**, ao contrário da preferência humana | Inversão |
| **Preferência de marca Macbook e iPad** | Erro substancial de estimativa | Magnitude |
| **Coeficiente de preço, renda acima de US$ 150 mil** | **Coeficiente de preço positivo** — único caso em todo o paper | Inversão, localizada em estrato |

E a frase que fecha o argumento de por que isso é grave:

> *"Critically, in all of these cases, a researcher lacking a human benchmark would have had no basis for identifying which estimates were unreliable."*

**Este é o problema que o T2 resolve.** Se existe uma função de decaimento estimável, o pesquisador *passa a ter* base para saber onde não confiar, sem precisar do benchmark humano em cada célula. É assim que a contribuição deve ser vendida na introdução.

### O que o fine-tuning conserta e o que não conserta

Conserta:
- **Inverte de volta os sinais errados** de WTP para sabores pepino e panqueca.
- Aproxima a WTP do projetor embutido da estimativa humana.
- Aproxima a taxa de escolha da **opção de não comprar** (outside option) da observada nos humanos, inclusive nos estudos 1B e 2B onde o conjunto de escolha difere do de treino — evidência de extrapolação genuína dentro da categoria.

Não conserta:
- **Categoria diferente** — não ajuda e *em alguns casos piora*.
- **Diferenças entre segmentos de clientes** — nulo declarado.

Verbatim do fecho sobre heterogeneidade:

> *"...conclude that even with our augmentation method, the current state-of-the-art models of GPT better reflect **average population WTP** and do not provide meaningful across-group estimates."*

Atributos de segmentação testados: **gênero, idade, raça/etnia, afiliação política, renda domiciliar e escolaridade**.

---

## 5. Intuição dos autores sobre o mecanismo — e o que ela implica

> *"In small samples especially, LLMs may more easily learn simple moments such as market shares rather than estimate WTP, which is a complex and highly model-dependent function of the data."*

Hipótese deles: há uma **hierarquia de dificuldade de momentos**. Momentos simples (participação de mercado, taxa de não compra) são aprendidos primeiro; funções complexas dos dados (WTP, e por extensão heterogeneidade entre grupos) exigem muito mais.

Isto é compatível com — e complementar a — a hipótese do T2. Combinadas, produzem uma predição de duas dimensões que nenhum dos dois papers tem sozinho:

> **O erro do respondente sintético cresce tanto com a complexidade do momento estimado quanto com a distância do estrato ao centro de massa do corpus, e os dois efeitos interagem.**

Ou seja: a WTP de um estrato periférico deve ser muito pior do que a soma das duas penalidades isoladas. **Um termo de interação é o achado mais publicável que o T2 pode ter.** Registrar como hipótese formal na M09 e no pré-registro da M12.

---

## 6. Custos de API declarados

Úteis para o orçamento do T2:

| Modelo | Input (1M tokens) | Output (1M tokens) |
|---|---|---|
| GPT-3.5 Turbo | US$ 0,50 | US$ 1,50 |
| GPT-4o | US$ 5,00 | US$ 15,00 |

Fine-tuning tem custo de token significativamente maior. Piloto do Estudo 1 de Argyle custou US$ 29 (ver M01) — a ordem de grandeza de um estudo deste tipo é de dezenas a poucas centenas de dólares, não milhares. **A restrição do T2 não é orçamento.**

---

## 7. Como Brand et al. situam a literatura

Citam explicitamente como trabalhos que examinam as limitações do respondente sintético: **Acerbi e Stubbersfield (2023); Atari et al. (2024); Bisbee et al. (2024); Dentella et al. (2023); Dominguez-Olmedo et al. (2023); Goli e Singh (2024); Gui e Toubia (2025).**

Três nomes novos que não estavam no radar e precisam ser checados na **M03** ou na **M11**:
- **Goli e Singh (2024)** — marketing, provavelmente sobre preferência temporal ou desconto.
- **Gui e Toubia (2025)** — Toubia é de Columbia, marketing quantitativo; provavelmente sobre inferência causal com LLM.
- **Dominguez-Olmedo et al. (2023)** — provavelmente sobre respostas de LLM a surveys.

Sobre Horton: *"He also compares GPT to a random number generator, which is related to our approach. **We focus on the distribution of responses rather than a single draw.**"* — o foco distribucional é herdado de Brand et al., e o T2 herda dele.

---

## 8. Síntese operacional para o T2

### O que herdar

| Elemento | Como usar |
|---|---|
| WTP por logit multinomial, coef. atributo / \|coef. preço\| | Estimador primário do desfecho de consumo |
| Arquitetura piloto → estudos → feature nova | Estrutura do desenho; a "feature nova" testa extrapolação fora do corpus |
| 50 repetições por prompt como padrão de fato | Ponto de partida da M10, ajustado pela lógica de que N é escolha de desenho |
| Grade de modelos por número de parâmetros | Replicar: o tamanho do modelo é covariável, não ruído |
| Taxa de escolha da opção externa como momento simples de controle | Diagnóstico barato de sanidade antes de olhar WTP |
| Custos de API declarados | Orçamento |

### As quatro brechas que o T2 ocupa

1. **A heterogeneidade entre grupos é nulo declarado.** Estruturar o nulo é a contribuição: mostrar que o erro tem forma, direção e magnitude previsíveis.
2. **Variância amostral declarada fora do escopo, sem erro padrão em nenhuma estimativa.** O T2 entra exatamente aí, com o aparato de Wasserstein-1 herdado de Santurkar (ver M01).
3. **O benchmark humano deles é painel de conveniência enviesado.** O T2 ancora em POF e PNAD — microdado oficial, ponderado, com desenho amostral probabilístico. É uma vantagem de qualidade de benchmark, não só de contexto.
4. **A interação entre complexidade do momento e periferia do estrato não foi testada por ninguém.** É a hipótese mais forte disponível e sai da combinação deste paper com o desenho do T2.

### Fricção nova detectada

O coeficiente de preço positivo em renda acima de US$ 150 mil é, ao mesmo tempo, o melhor achado e um alerta. Melhor achado porque é erro localizado em estrato. Alerta porque **renda alta não é periferia do corpus** — consumidores ricos, americanos e anglófonos deveriam estar no centro de massa, não na borda.

Duas leituras possíveis, e o T2 precisa escolher e defender uma:

- **(a) A distância não é sociodemográfica pura, é de densidade de *dados de escolha* naquele estrato.** Consumidor de renda muito alta é raro em painel de conjoint, mesmo sendo abundante em texto. Isso refina a hipótese: a distância relevante é ao centro de massa dos **dados de comportamento de escolha**, não do corpus textual em geral.
- **(b) É artefato do desenho deles** — poucas respostas na célula de renda alta (30 por grupo), o que produz estimativa instável e não viés sistemático.

**A leitura (a) é mais interessante e mais arriscada; a (b) é mais provável.** Testar as duas é obrigatório, porque um revisor levanta isso. Registrar como ameaça na **M08** e como decisão de operacionalização na **M04** — que trata justamente de como definir "distância ao centro de massa do corpus".

---

## Pendências geradas

- [ ] **M04 fica mais difícil e mais importante:** a definição de distância precisa distinguir densidade textual de densidade de dados de escolha. O achado de renda alta força essa distinção.
- [ ] **M03/M11:** checar Goli e Singh (2024), Gui e Toubia (2025), Dominguez-Olmedo et al. (2023), Acerbi e Stubbersfield (2023), Dentella et al. (2023).
- [ ] **M08:** registrar a ameaça de instabilidade por célula pequena versus viés sistemático.
- [ ] **M09/M12:** formalizar a hipótese de interação entre complexidade do momento e periferia do estrato.
- [ ] **M10:** a regra de parada não pode ser baseada em fechamento de intervalo, já que N é escolha de desenho. Precisa de outro critério.
- [ ] Localizar Fong et al. (2023) — é o benchmark de conjoint de mundo real validado contra resultados de mercado, e o T2 pode precisar de um equivalente brasileiro.
