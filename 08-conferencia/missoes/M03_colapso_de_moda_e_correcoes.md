# M03 — Colapso de moda: taxonomia, correções e a ameaça ao T2

Executada em 2026-08-21. Seis papers baixados e lidos em texto integral, mais uma referência crítica localizada por busca.

---

## Resumo do que esta missão muda

Três coisas, e duas delas são desconfortáveis:

1. **"Colapso de moda" são três fenômenos distintos, e a literatura os confunde.** A distinção não está formalizada em lugar nenhum que eu tenha lido. Formalizá-la já é contribuição, e o T2 precisa dela para não medir a coisa errada.

2. **⚠️ Ameaça competitiva séria: Boelaert et al. (2025), em *Sociological Methods & Research*.** Testaram **687 subpopulações sociodemográficas** e acharam variância entre subgrupos substancialmente menor que a humana, mesmo com prompt sociodemográfico explícito. Isto é o achado principal que eu havia atribuído ao T2. **A novidade do T2 precisa se deslocar de "existe colapso entre grupos?" para "o colapso é estruturado e previsível?"**

3. **⚠️ Ameaça metodológica grave: o desenho de repetição pode estar medindo artefato.** Jang, Lee e Kim (KAIST, jul/2026) mostram que modelos ajustados por instrução **não amostram de distribuições — colapsam num único output**. Em 100 itens do OpinionQA, 57% dos pares (persona, item) retornam a mesma resposta em **todas** as 50 chamadas. Se isso for verdade nos modelos que o T2 vai usar, contar repetições não estima distribuição nenhuma.

---

## 1. A taxonomia que a literatura não fez

Três falhas distintas circulam sob o mesmo nome. Elas têm mecanismos diferentes, métricas diferentes e correções diferentes.

| | Falha | O que colapsa | Como se detecta |
|---|---|---|---|
| **C1** | Colapso intra-persona | A mesma persona, na mesma questão, devolve a mesma resposta em chamadas repetidas | Taxa de resposta modal em N repetições; gap de logit entre as duas primeiras opções |
| **C2** | Colapso entre grupos | Personas diferentes produzem distribuições parecidas demais; minorias somem | Variância entre subgrupos; representação de opinião minoritária |
| **C3** | Colapso de estrutura correlacional | Correlações entre questões ficam altas demais; consenso artificial | Teste de Mantel entre matrizes de correlação; divergência entre distribuições de coeficientes |

**A implicação é dura e é o achado central desta missão:**

> **Não se pode medir C2 com um instrumento que sofre de C1.** Se a amostragem por chamada é degenerada, a variância entre grupos observada está confundida com a degeneração do primitivo de amostragem. Um T2 que rode N repetições por estrato e compare variâncias estará medindo C1 e chamando de C2.

Isso muda o desenho do T2 de forma não-negociável. Ver seção 5.

---

## 2. Os mecanismos propostos — quatro explicações concorrentes

| Mecanismo | Autores | Tese | Nível |
|---|---|---|---|
| **Viés de tipicidade nos dados de preferência** | Zhang et al. (2026) | Anotadores humanos preferem sistematicamente texto familiar e fluente. Mesmo com modelo de recompensa perfeito e otimização perfeita, o viés nos dados de preferência já produz colapso. | Dados |
| **Primitivo de amostragem degenerado** | Jang, Lee e Kim (2026) | O output por chamada de um modelo instruction-tuned não é amostra da distribuição condicional que o pipeline assume. Visível no logit; induzido pelo alinhamento. | Arquitetura |
| **Hipótese de otimização por acurácia** | Li, Li e Qiu | A homogeneização decorre de o modelo priorizar a resposta modal — maximizar predição às custas de representatividade. | Objetivo |
| **Falha em gerar dado numérico** | Heath e Alexander (2026) | O colapso decorre da incapacidade de gerar número; resposta em texto é mais adequada à tarefa. | Formato de saída |

Não são mutuamente exclusivos. O de Jang et al. é o mais proximal e o mais bem evidenciado, porque é medido no logit e replicado em três famílias de modelo.

---

## 3. Tabela comparativa das correções

| Método | Autores / venue | Como funciona | Métrica | Ganho reportado | Limitação declarada |
|---|---|---|---|---|---|
| **Semantic Similarity Rating (SSR)** | Heath e Alexander, arXiv:2607.28550v1, 30/07/2026, U. Toronto | Solicita resposta **só em texto**, depois mapeia para escala numérica via *embeddings*. Um **parâmetro global de temperatura** aprendido controla a variância | Divergência KL contra ANES 2016; erro absoluto das médias sintéticas por grupo | Distribuições "muito mais próximas" das reais, KL menor, **sem perda significativa** na acurácia das médias. Parâmetro aprendido em ANES 2016 **generaliza para ANES 2020** | **As médias continuam consistentemente enviesadas**, exatamente como em Bisbee et al. Corrige variância, não viés |
| **Verbalized Sampling (VS)** | Zhang, Yu, Chong, Sicilia, Tomz, Manning e Shi, arXiv:2510.01171v4, 15/07/2026 (Stanford, Northeastern) | *Prompting* sem treino: pede ao modelo que **verbalize uma distribuição de probabilidade** sobre um conjunto de respostas ("gere 5 piadas e suas probabilidades"), aliviando a pressão por uma resposta típica | Escore de diversidade semântica e lexical; KL contra corpus de referência | **Diversidade 1,6× a 2,1×** sobre *prompting* direto em escrita criativa. KL de 0,12 contra o corpus de referência. Mantém acurácia factual e segurança | Custo computacional por chamada maior que gerar resposta única; validado sobretudo em criação, diálogo e geração de dado sintético — **não em survey demográfico** |
| **Describe pathway** | Jang, Lee e Kim, arXiv:2607.25292v1, 28/07/2026, KAIST | Uma única chamada pedindo **a distribuição de respostas**, em vez de agregar chamadas por persona | Distância de variação total (TV) contra dados humanos | **Reduz o erro a menos da metade**: TV 0,22 contra 0,46 da agregação por persona. Vantagem se mantém mesmo com personas pareadas demograficamente aos respondentes reais do Pew | Não produz **saída por respondente**; inútil quando a aplicação exige indivíduos simulados |
| **Prompt-Perturbed Argyle (PPA)** | Jang, Lee e Kim, idem | Randomiza **ordem das opções e fraseado da questão** entre chamadas, induzindo variação por chamada | TV | **−21%** de erro, **sem custo adicional** | Ganho modesto comparado ao describe; é paliativo sobre um primitivo degenerado |
| **Fine-tuning com survey prévio** | Brand, Israeli e Ngwe, HBS WP 23-062 (ver M02) | Ajusta pesos com pares prompt-resposta de survey humano anterior | WTP via logit multinomial; taxa de opção externa | Inverte de volta sinais errados dentro da categoria; aproxima taxa de não-compra | **Não ajuda e às vezes piora** em categoria diferente; **nulo entre segmentos de cliente** |
| **Unblinding** | Gui e Toubia, arXiv:2312.15524v3, 22/11/2025, Columbia Business School | **Revela o desenho experimental** ao sujeito simulado, em vez de mantê-lo cego como se faz com humanos | Estimação de demanda contra experimento real com 40 produtos | Melhora consistente **em todos os modelos testados**, com e sem raciocínio. Complementa fine-tuning e torna as predições robustas a dado irrelevante no treino | Controlar covariáveis para resolver confundimento **compromete validade ecológica** — a covariável controlada fica artificialmente saliente na decisão simulada |
| **Audience Segmentation** | arXiv:2604.06663 | Segmentação sistemática de audiência para restaurar heterogeneidade | — | — | ⚠️ **[NÃO LIDO]** — localizado por busca, não baixado. Ler na M11 |
| **Parametric Social Identity Injection** | KDD 2026, DOI 10.1145/3770855.3817926 | Injeção paramétrica de identidade social e diversificação em simulação de opinião pública | — | — | ⚠️ **[NÃO LIDO]** — localizado por busca. Ler na M11 |

---

## 4. A ameaça competitiva: Boelaert et al. (2025)

**Referência verificada:** BOELAERT, Julien; COAVOUX, Samuel; OLLION, Étienne; PETEV, Ivaylo; PRÄG, Patrick. *Machine Bias. How Do Generative Language Models Answer Opinion Polls?* **Sociological Methods & Research**, 2025. DOI 10.1177/00491241251330582.

> ⚠️ Texto integral não baixado nesta missão — venue, ano, autoria e DOI verificados via SAGE e portal do Institut Polytechnique de Paris. Achados abaixo de fonte secundária e da citação em Jang et al. **Marcar como [PARCIALMENTE VERIFICADO] até ler o original.**

O que eles fizeram e acharam:

- Testaram a capacidade de LLMs de replicar respostas de survey em **687 subpopulações definidas sociodemograficamente**.
- Encontraram **"machine bias"**: erro imprevisível, com viés forte e variância baixa em cada tópico, e o viés variando aleatoriamente de tópico para tópico.
- **Mesmo com prompt sociodemográfico explícito**, as distribuições de resposta permanecem altamente concentradas entre subgrupos.
- Jang et al. os citam exatamente como a fonte de que "*between-group variance collapses*".

### O que isso faz com o T2

Mata a formulação ingênua. "Existe colapso de heterogeneidade entre grupos?" está respondido, com N de subpopulações uma ordem de grandeza acima do que o T2 conseguiria, publicado em periódico de metodologia sociológica de primeira linha.

**O que sobra, e sobra bem:**

| Boelaert et al. (2025) | O que o T2 faz de diferente |
|---|---|
| Mostra que a variância entre grupos colapsa | Mostra que o colapso **tem forma** — estima o erro como função contínua da posição do estrato |
| Viés "varia aleatoriamente de tópico para tópico" | Testa se a variação é aleatória mesmo, ou se é **previsível pela densidade do estrato** |
| Opinião pública | **Consumo e disposição a pagar** — desfecho com implicação gerencial direta |
| Subpopulações de país central | Desigualdade **intra-país** extrema, com língua e nação fixas |
| Diagnóstico | **Função de correção** utilizável ex ante, sem benchmark humano por célula |

A frase "o viés varia aleatoriamente de um tópico para outro" é, na verdade, o melhor presente que Boelaert et al. poderiam ter dado ao T2: eles afirmam aleatoriedade. **Se o T2 mostrar estrutura onde eles viram ruído, isso é uma refutação direta, publicável e citável.** É um enquadramento muito mais forte do que "mais um paper achando colapso".

---

## 5. A ameaça metodológica: o split KNOWS/DOES

**Referência verificada:** JANG, Chaemin; LEE, Dongman; KIM, Jihee. *Instruction-Tuned Language Models Cannot Sample from Distributions They Can Describe*. arXiv:2607.25292v1, 28 de julho de 2026. School of Computing e School of Business and Technology Management, KAIST.

### Os números

- Pedido de inteiro aleatório uniforme entre 1 e 100: o modelo devolve **42 em 78% das chamadas**.
- Em sete alvos categóricos (enviesados, bimodais, multi-classe): resposta única em **mais de 94% das chamadas**.
- Em 100 itens do **OpinionQA** (o dataset de Santurkar, ver M01), com 50 chamadas repetidas por par (persona, item): **57% dos pares devolvem a mesma resposta todas as vezes**; **80% devolvem a mesma resposta em mais de 90% das chamadas**.
- Gap de logit entre as duas primeiras opções, a temperatura zero, **excede 14 nats** em alguns alvos — **fora do alcance recuperável por qualquer temperatura de decodificação disponível em API padrão**.
- Falha presente em **todos** os modelos instruction-tuned testados, em três famílias com pipelines de pós-treino materialmente diferentes. **Modelos base falham muito menos.**
- Andaimes de *chain-of-thought* não resolvem, porque o número aleatório que o modelo sorteia dentro do andaime é ele próprio não-uniforme.

### O nome do fenômeno

**KNOWS/DOES split**: o mesmo modelo que **não consegue amostrar** de uma distribuição **consegue descrevê-la corretamente** numa única chamada. Figura 1 do paper: no alvo binário enviesado, amostragem por chamada dá A=1,00 e B=0,00 em 200 chamadas; pedir a descrição da distribuição recupera A=0,70 e B=0,30, que é a forma correta.

### O que isso obriga no T2

O plano original — condicionar por estrato, rodar N repetições, comparar distribuições — **é exatamente o pipeline que este paper demole**. Três saídas, e o T2 deve usar mais de uma:

1. **Log-probabilidades do próximo token** (abordagem de Santurkar, ver M01). Contorna a amostragem inteiramente. Depende de a API expor logprobs — pendência já registrada na M01.
2. **Describe pathway**. Uma chamada por estrato pedindo a distribuição. Barato, e reduz TV pela metade. Perde a saída por indivíduo, o que para o T2 **não é problema**, porque o T2 quer distribuição por estrato, não respondentes simulados.
3. **PPA** como braço de comparação, para quem insiste em agregação por persona.

**E aqui aparece uma oportunidade que vale mais que a mitigação:** rodar os três caminhos lado a lado, por estrato, e testar se **o próprio KNOWS/DOES split varia com a periferia do estrato**. Ou seja: o modelo descreve bem a distribuição de um estrato central e mal a de um estrato periférico? Se sim, o T2 tem um segundo achado independente, e mais fundamental que o primeiro.

Registrar como hipótese H3 na M09.

---

## 6. Os outros dois papers de diagnóstico

### Li, Li e Qiu — *ChatGPT is not A Man but Das Man*

**Referência:** LI, Dai; LI, Linzhuo; QIU, Huilian Sophie. *ChatGPT is not A Man but Das Man: Representativeness and Structural Consistency of Silicon Samples Generated by Large Language Models*. arXiv:2507.02919. Afiliações: China University of Political Science and Law; Zhejiang University; **Kellogg, Northwestern**.

Desenho: GPT-4 e Llama 3.1 (8B, 70B, 405B), questões sobre aborto e imigração não autorizada da **ANES 2020**.

Dois construtos que o T2 deve adotar como vocabulário:

- **Consistência estrutural** — a acurácia proporcional se mantém em **todos os níveis de agregação**, do subgrupo de variável única (gênero, raça) até as células interseccionais mais específicas. Acharam inconsistência estrutural significativa.
- **Homogeneização** — sub-representação de opinião minoritária. Acharam severa.

**Consistência estrutural é quase a hipótese do T2, dita em vocabulário de sociologia.** A diferença: eles testam *se* a acurácia se mantém entre níveis de agregação; o T2 pergunta *como ela decai* em função da posição da célula. Diagnóstico binário contra função contínua. A distinção é real, mas é fina — e um revisor pode não vê-la se o paper não a explicitar na primeira página.

Contribuição teórica deles: a **hipótese de otimização por acurácia**, ligando homogeneização à estrutura algorítmica que prioriza maximização de predição às custas de representatividade real.

### Shi e Haupt — *The Collapse of Heterogeneity in Silicon Philosophers*

**Referência:** SHI, Yuanming; HAUPT, Andreas. *The Collapse of Heterogeneity in Silicon Philosophers*. arXiv:2604.23575v2, 29 de abril de 2026. **Adobe Inc.** e **Stanford University**.

Desenho: **N = 277** filósofos profissionais de perfis do PhilPeople; **sete modelos** proprietários e abertos; validação contra o **PhilPapers 2020 Survey (N = 1.785)**.

Achados:
- Modelos **super-correlacionam** julgamentos filosóficos, produzindo **consenso artificial** entre domínios (isto é C3).
- **Efeitos de especialista** espúrios: o modelo assume implicitamente que especialistas de um domínio têm visões altamente semelhantes entre si.
- **Fine-tuning com DPO melhora a preservação da estrutura correlacional** — mas o paper avalia isso como robustez, não como solução geral.

Aparato métrico que o T2 pode importar para C3, se quiser um terceiro desfecho: **teste de Mantel** (permutacional, compara duas matrizes de correlação), matrizes questão-a-questão com deleção pareada, e divergência entre distribuições de coeficientes discretizadas em 20 faixas.

O paralelo com o T2 é bonito: *especialistas de um domínio* está para *filósofos* assim como *consumidores de um estrato* está para o T2. O modelo achata a diversidade interna de uma categoria que ele reconhece como categoria.

---

## 7. Referências novas geradas, ainda não verificadas

Citadas por Heath e Alexander, por Jang et al. ou por Brand et al., todas relevantes e **nenhuma lida**:

| Referência | Contexto da citação | Prioridade |
|---|---|---|
| Boelaert et al. (2025), *Sociological Methods & Research* | Colapso de variância entre grupos — **ameaça direta** | **Máxima. Ler o integral.** |
| Kaiser et al. (2025) | Citado junto de Bisbee para colapso de variância | Alta |
| Barrie e Cerina (2026) | Idem | Alta |
| Alexander e Collins (2026) | Sensibilidade a mudança de prompt e versão de modelo | Média |
| Schröder et al. (2025) | Idem | Média |
| Tjuatja et al. (2024) | Vieses de resposta divergindo de padrões humanos | Média |
| Hu e Collier (2024) | Sensibilidade a enquadramento de prompt | Média |
| Gligorić et al. (2024) | Idem | Média |
| Goli e Singh (2024) | Citado por Brand et al. entre as limitações | Média |
| Dominguez-Olmedo et al. (2023) | Idem | Média |
| Acerbi e Stubbersfield (2023) | Idem | Baixa |
| Dentella et al. (2023) | Idem | Baixa |
| Padmakumar e He (2024) | Colapso de moda sob RLHF | Baixa |
| Meister et al. (2025); Xiao et al. (2025); Zhang et al. (2025) | Assimetria describe versus agregação | Média |
| Broska, Howes e Loon (2024) | Métodos de comparar predição de LLM com observação real | Média |
| Park et al. (2023, 2024) | Condicionamento por entrevista, acurácia comparável a teste-reteste humano | **Alta** — é o estado da arte de condicionamento |

---

## 8. Síntese operacional para o T2

### Decisões forçadas por esta missão

1. **Abandonar agregação ingênua por repetição como método primário.** Usar log-probabilidades onde a API permitir e *describe pathway* onde não permitir. Manter PPA e agregação por persona apenas como braços de comparação.
2. **Adotar a taxonomia C1/C2/C3 explicitamente**, e declarar na primeira página que o T2 mede C2 controlando C1. É a defesa contra o revisor que disser "isso já foi feito".
3. **Reposicionar contra Boelaert et al.**: não "existe colapso", mas "o colapso que eles chamaram de aleatório é estruturado".
4. **Adotar SSR como braço de correção**, porque é o único que ataca variância mantendo a média, e o parâmetro de temperatura global generaliza entre ondas de survey. É a linha de base mais defensável.
5. **Adotar unblinding de Gui e Toubia**, porque o desfecho do T2 é estimação de demanda — exatamente o contexto em que eles demonstram o problema de confundimento. Não usar unblinding num paper de WTP com LLM é deixar um flanco aberto.
6. **Registrar H3**: o próprio split KNOWS/DOES varia com a periferia do estrato.

### Vocabulário a adotar

`fidelidade algorítmica` (Argyle) · `representatividade`, `direcionabilidade`, `consistência` (Santurkar) · `consistência estrutural`, `homogeneização` (Li, Li e Qiu) · `machine bias` (Boelaert et al.) · `split KNOWS/DOES` (Jang et al.) · `viés de tipicidade` (Zhang et al.)

### Risco de escavação, atualizado

Alto e subindo. Entre abril e julho de 2026 saíram **quatro** papers relevantes (philo em abril, VS em julho, SSR em julho, KNOWS/DOES em julho). O campo está em aceleração. A janela do T2 até 19 de novembro é estreita, e o diferencial precisa ser o que **ninguém mais tem**: o benchmark brasileiro oficial e a variação intra-país. Não é a métrica, não é o método, não é o diagnóstico.

---

## Pendências geradas

- [ ] **Prioridade máxima:** ler Boelaert et al. (2025) integral. Verificar se eles já testaram estrutura no erro ou apenas afirmaram aleatoriedade. **Se já testaram, o T2 precisa ser repensado.**
- [ ] Ler Park et al. (2023, 2024) — condicionamento por entrevista é o estado da arte e não está no radar.
- [ ] Baixar e ler os dois métodos de correção localizados por busca (arXiv:2604.06663 e KDD 2026 DOI 10.1145/3770855.3817926).
- [ ] Verificar data e status de publicação de Li, Li e Qiu (arXiv:2507.02919) — checar se saiu em periódico.
- [ ] **M06 muda de escopo:** o instrumento agora tem de comparar quatro caminhos de extração (logprob, describe, PPA, agregação simples), não um.
- [ ] **M07 ganha a distância de variação total (TV)** ao lado de Wasserstein e KS, porque é a métrica de Jang et al. e permite comparação direta com o número deles (0,22 contra 0,46).
- [ ] **M09 ganha H3.**
