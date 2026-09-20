# Eixo alternativo — GenAI e opções de consumo

Levantado em 2026-08-22, a pedido. **Não é missão do roteiro.** É a base de literatura para decidir se vale trocar de tema.

---

## O achado que organiza tudo

A literatura recente se partiu em **duas metades que ninguém juntou**:

| Metade | Pergunta | Quem faz |
|---|---|---|
| **Oferta** | O que uma marca faz para aparecer na resposta do modelo? | GEO (KDD), Kumar, **Salas — vencedor da AIM** |
| **Procura** | O que o consumidor faz com o que apareceu? | Iannelli e Ai, Chu e Hou, Allouah et al. |

E falta a terceira peça em **ambas**: o **contrafactual**. O que a pessoa teria escolhido sem o modelo? Agarwal e Sen fazem isso para *cliques*, ninguém faz para **escolha de marca**.

> ⭐ **É nessa junção que existe paper.** Não em refazer nenhuma das duas metades.

---

## 1. Os oito trabalhos que formam a base

### Camada fundadora — oferta

**1. Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan e Deshpande — "GEO: Generative Engine Optimization"**
**ACM SIGKDD (KDD) 2024** · DOI 10.1145/3637528.3671900 · arXiv:2311.09735 · ✅ **venue verificado**

O documento fundador. GEO-bench com cerca de **10 mil consultas em nove conjuntos**. Demonstrou em experimento controlado que otimização deliberada de conteúdo aumenta visibilidade em resposta gerada em **22% a 41%** — o 41% é máximo, não média.

> **Por que importa para você:** é o *paper de método* que qualquer coisa nessa linha tem de citar, e é peer-reviewed em venue forte. É a âncora.

**2. Pratyush Kumar (Ranqo) — "Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines"**
arXiv:2606.20065 · 18 jun. 2026 · ⚠️ **preprint, sem venue**

Mais de **100 mil respostas de prompt, mais de 100 marcas**, entre março e maio de 2026, em ChatGPT, Claude, Perplexity e Gemini. Achou uma **hierarquia de três camadas**:

| Camada | Exemplo | Visibilidade |
|---|---|--:|
| Marca global | Stripe, Nike | **73%** |
| Média / regional | Olipop, Klaviyo | **44%** |
| Nicho / pequena | — | **11%** |

Cerca de **78% das citações vão para sites corporativos**; o formato mais citado é a listicle "best-of", com ~21%. E o dado mais interessante: **o sentimento muda de lado cerca de 6,7 vezes mais do que muda o fato de ser mencionado.**

> ⚠️ **Este é o trabalho que a M21 flagrou como concorrente perdido.** Autor único, ligado a uma empresa de ferramenta (Ranqo), sem venue. **Rigor menor, dado maior.** É citável e é batível.

**3. Ruben R. Salas (Wharton) — "AI-Mediated Marketing: Constrained Content Optimization for LLM Visibility"**
**Prêmio Hanssens, AIM 2026** · ✅ do índice de premiados do dossiê

> ⭐ **O precedente decisivo.** Salas ganhou o Hanssens **duas vezes** — 2025 com humor de IA, 2026 com visibilidade em LLM. O arquétipo "Canal LLM" é o que mais vence nessa conferência. **Você não estaria adivinhando o gosto do júri; estaria seguindo o histórico dele.**

### Camada de demanda — o que o consumidor faz

**4. Michael Iannelli e Alan Ai — "From Prompt to Purchase: How AI Brand Recommendations Move Consumers on the Open Web"**
arXiv:2606.10907 · 9 jun. 2026 · ⚠️ **preprint, sem venue**

**É literalmente a sua pergunta, já respondida.** Juntaram *clickstream* de opt-in com as **conversas dos usuários** no ChatGPT, Claude e Gemini. Desenho: estudo de evento com pré-tendência, classificador de postura para separar recomendação intencional de menção incidental, condicionamento em não-clientes, e grupo de controle da mesma categoria **dentro da mesma resposta**.

Quando o assistente **recomenda** uma marca a quem não tinha vínculo prévio:

| Desfecho | Efeito |
|---|---|
| Busca no Google pelo nome da marca | **+4,3 pp** [3,1 · 5,5] |
| Visita ao site da marca | **+2,4 pp** [1,4 · 3,5] |
| Visita à página do varejista | **+1,0 pp** [0,3 · 1,7] |

E menção **incidental** move muito menos: +1,8 / +1,1 / +0,3.

> 🔴 **Leia isto como ameaça, não como base.** Se o seu paper for "recomendação de LLM move compra", **você chega em segundo**, com dado pior — eles têm clickstream ligado a conversa real, que você não tem.

**5. Xi Chu e Yupeng Hou — "Incumbent Advantage: Brand Bias and Cognitive Manipulation Dynamics in LLM Recommendation Systems"**
arXiv:2606.17443 · 16 jun. 2026 · ⚠️ **preprint, sem venue**

GPT-4o-mini, Claude Sonnet e Gemini 3 Flash, em cosmético de pele — categoria escolhida porque o consumidor **não consegue avaliar qualidade antes** e depende de reputação.

- Com especificações **idênticas**, a marca conhecida é recomendada **100% das vezes** — índice de vantagem do incumbente = 10,0.
- O domínio **colapsa** com vantagem de concorrente de menos de **+0,1 estrela**.
- "Manipulação cognitiva" = linguagem de autoridade, **incluindo alegação clínica fabricada**, com valor excedente de viés de **+0,17 ponto de nota**.
- ⭐ **E o achado que vale o paper:** quando **várias marcas** usam a mesma estratégia, o ganho individual cai de **+0,802 para +0,007**. **É um dilema do prisioneiro.** Quem não participa recebe **zero** recomendação.

> ⭐ **Esse último resultado é o mais interessante do conjunto todo — e está em simulação.** Ninguém mediu no mundo real.

**6. Allouah, Besbes, Figueroa, Kanoria e Kumar — "What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, & Emerging Implications for Agentic E-Commerce"**
**Proceedings of the ACM Web Conference 2026** · DOI 10.1145/3774904.3792943 · arXiv:2508.02630 (v1 ago. 2025, v3 dez. 2025) · ✅ **venue verificado**

O framework **ACES**, agnóstico de provedor, para auditar decisão de agente comprador. Achados:

- **Viés de posição forte**, que varia entre provedores e entre versões do mesmo modelo, e **persiste em interface só de texto** — ou seja, não é efeito visual.
- **Homogeneidade de escolha:** os agentes concentram demanda em poucos produtos "modais" e ignoram o resto.
- **Atualização de modelo remaneja participação de mercado.**
- Agentes **penalizam conteúdo patrocinado** e favorecem selo da plataforma.

> ⭐ **O anchor acadêmico mais forte da lista.** Besbes e Kanoria são de operações/marketing quantitativo de primeira linha, e tem venue. **É a referência que dá seriedade à sua seção de método.**

### Camada conceitual

**7. Manon Reusens, Sofie Goethals e David Martens — "LLM Consumer Behavior Theory: Foundations of a Novel Research Field"**
arXiv:2606.18005 · 16 jun. 2026 · ⚠️ **preprint, sem venue** · **conceitual, sem validação empírica**

Propõe formalizar como preferência humana é representada e acionada por agente, e **como decisão de agente agrega em demanda de mercado**. Nomeia três frentes abertas: alinhamento, representação de preferência, e dinâmica de mercado quando o decisor não é humano.

> **Uso:** é a sua seção de enquadramento teórico pronta. **Um paper conceitual recente que declara as lacunas é presente de introdução** — você cita e diz qual delas está fechando.

**8. Saharsh Agarwal (Indian School of Business) e Ananya Sen (Carnegie Mellon) — "Google AI Overviews and Publisher Traffic: Evidence from a Field Experiment"**
SSRN, abr. 2026, revisado jun. 2026 · ⚠️ **working paper, sem peer review**

Extensão de Chrome randomizando **1.065 participantes americanos** em três braços — controle, AIO oculto, e redirecionamento para o AI Mode — por duas semanas cada, entre janeiro e fevereiro de 2026. **Quando o AI Overview aparece, o clique orgânico de saída cai 39,8% e a busca sem clique sobe 34,5%**, com clique patrocinado estável. E nenhuma melhora mensurável na qualidade percebida da busca.

> **É o contrafactual bem feito — mas para cliques, não para escolha de marca.** É o desenho que você imitaria.

---

## 2. Onde está o buraco

Cruzando as oito referências, três coisas **ninguém fez**:

| # | Lacuna | Por que ninguém fez |
|---|---|---|
| **A** | **Tudo é em inglês, mercado americano.** A hierarquia 73/44/11 de Kumar é marca dos EUA; Chu e Hou é cosmético em inglês | Falta de acesso a mercado não-anglófono com dado real |
| **B** | ⭐ **Ninguém *interveio*.** Todos auditam de fora. Ninguém pegou marcas reais, mudou o conteúdo delas e mediu o efeito na resposta do modelo **e** na receita | Exige controlar o site de marcas reais. **Pesquisador de universidade não tem isso** |
| **C** | ⭐⭐ **O dilema do prisioneiro de Chu e Hou nunca foi testado fora da simulação.** Quando todo mundo otimiza, o ganho vira zero — em simulação | Exige observar um mercado **antes** da saturação de GEO |

> 🔴 **E a lacuna C é perecível.** No mercado americano a janela do "antes de todo mundo otimizar" **está fechando agora**. No Brasil ela ainda está aberta. **Em 2027 esse estudo não vai mais ser possível nos EUA — e talvez nem aqui.**

---

## 3. O que você tem que os autores acima não têm

| Ativo | Consequência |
|---|---|
| **Argos controla o conteúdo de marcas reais** | Você pode **randomizar a intervenção**, não só observar. É a diferença entre auditoria e experimento |
| **Acesso ao Google Search Console dos clientes** | Você tem o desfecho de busca **ligado à marca**, que é metade do desenho de Agarwal e Sen |
| **Mercado brasileiro, em português** | Nenhum dos oito trabalhos toca. E não é "contexto exótico" — é **o contrafactual pré-saturação** |
| **Clientes de portes diferentes** | A hierarquia de Kumar (global / média / nicho) vira **variável manipulável**, não descritiva |

---

## 4. Os três desenhos possíveis, ordenados

### ⭐ D1 — O experimento de intervenção *(recomendado)*

**Pergunta:** a elevação de visibilidade que o GEO promete sobrevive quando ela chega na receita — e sobrevive quando o concorrente também otimiza?

**Desenho:** carteira de marcas da Argos dividida em tratamento e controle. Tratamento recebe otimização de conteúdo nos moldes do KDD 2024. Mede-se em três camadas: **(a)** menção e citação na resposta do modelo, com prompts fixados e versionados; **(b)** busca de marca e clique, via Search Console; **(c)** conversão, onde o cliente permitir.

**Por que ganha:** fecha as lacunas **A**, **B** e **C** de uma vez. E responde a Chu e Hou com dado de campo onde eles têm simulação.

**Risco:** exige consentimento de cliente, e o n é pequeno. **O poder vem de medidas repetidas no tempo, não de número de marcas** — e isso precisa ser simulado antes, como foi feito no T2.

### D2 — A auditoria brasileira

Replicar Kumar em português, com marcas brasileiras, medindo a hierarquia de visibilidade e — o ponto dele mais frágil — **a volatilidade de sentimento**, que muda 6,7 vezes mais que a menção.

**Mais barato e mais seguro.** Mas é replicação, e a AIM premia achado. **Vale como seção do D1, não como paper.**

### D3 — O agente comprador em português

Estender o ACES para catálogo brasileiro: os vieses de posição e a concentração modal se mantêm fora do inglês?

**Tem venue forte para citar e método pronto.** Mas é o mais distante do que você controla, e **compete com Columbia**.

---

## 5. O custo honesto de trocar

| | |
|---|---|
| **Prazo** | Deadline **19 de novembro de 2026**. Hoje é 22 de agosto. **89 dias.** |
| **O que se abandona** | 48 missões, pré-registro escrito, achado corrigido e defensável (inclinação, 11 de 12), roteiro de fala pronto |
| **O que se ganha** | Arquétipo com **duas vitórias** no histórico da AIM, dado que só você tem, e uma janela temporal que fecha |
| **O híbrido** | ⚠️ **Não existe.** São dois papers, dois métodos, duas literaturas. Tentar os dois em 89 dias entrega dois ruins |

> **O T2 está pronto para submeter e é sólido. O eixo GenAI-consumo é mais premiável e mais arriscado.** A escolha não é técnica — é de apetite a risco, e é sua.

---

## 6. O que verificar antes de decidir

- [ ] **Ler Iannelli e Ai a fundo.** Se eles já cobriram o que você faria, o D1 precisa se deslocar para a intervenção — que eles não têm.
- [ ] Confirmar quantos clientes da Argos topariam participar, e com que desfecho (só visibilidade, ou receita também).
- [ ] Simular o poder do D1 com o número real de marcas e semanas disponíveis — **antes** de prometer o desenho.
- [ ] Verificar se Kumar, Chu e Hou, Iannelli e Ai, e Reusens et al. ganharam venue até novembro. Quatro preprints de junho de 2026 é literatura instável.
- [ ] Checar se o paper de Salas (AIM 2026) está disponível em texto completo — **é o molde do que ganhou.**
- [ ] Perguntar ao orientador se trocar de eixo a 89 dias do prazo é aceitável no programa.

---

## DOI de cada referência

Todos verificados em **Crossref** ou **DataCite** em 2026-08-22. Nenhum inferido.

| # | Trabalho | DOI | Registro |
|---|---|---|---|
| 1 | GEO: Generative Engine Optimization | `10.1145/3637528.3671900` | ✅ Crossref — KDD 2024, ACM |
| 6 | What Is Your AI Agent Buying? | `10.1145/3774904.3792943` | ✅ Crossref — ACM Web Conference 2026, publicado 12 abr. 2026 |
| 8 | Google AI Overviews and Publisher Traffic | `10.2139/ssrn.6513059` | ✅ Crossref — SSRN / Elsevier BV, 2026 |
| 4 | From Prompt to Purchase | `10.48550/arXiv.2606.10907` | ✅ DataCite — arXiv, 2026 |
| 5 | Incumbent Advantage | `10.48550/arXiv.2606.17443` | ✅ DataCite — arXiv, 2026 |
| 7 | LLM Consumer Behavior Theory | `10.48550/arXiv.2606.18005` | ✅ DataCite — arXiv, 2026 |
| 2 | Generative Engine Optimization at Scale | `10.48550/arXiv.2606.20065` | ✅ DataCite — arXiv, 2026 |
| 3 | Salas — AI-Mediated Marketing (AIM 2026) | **não tem** | ⚠️ Apresentação de conferência sem anais publicados |

### Duas divergências de título que importam na hora de citar

- **Agarwal e Sen:** o Crossref registra *"Google AI Overviews and Publisher Traffic: Evidence from a Field Experiment"*, enquanto a página do SSRN mostra *"The Impact of Google AI Overviews on Publisher Traffic and User Experience..."*. **O título mudou entre revisões — cite pelo Crossref.**
- **Allouah et al.:** o arXiv diz *"Implications **for** Agentic E-Commerce"*; a versão publicada na ACM diz *"Implications **of** Agentic E-Commerce"*. **Cite a versão ACM.**

> ⚠️ **Os quatro DOIs `10.48550` são do arXiv, não de publicação.** São DOIs reais e citáveis, registrados no DataCite, mas sinalizam preprint. Quatro dos oito trabalhos são preprints de junho de 2026 sem venue — **reverifique em novembro se algum saiu em anais ou periódico**, porque a citação muda.
