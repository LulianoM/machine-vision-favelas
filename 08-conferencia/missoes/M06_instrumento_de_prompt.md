# M06 — Instrumento de prompt: persona, ordem, âncoras, aquiescência e versionamento

Executada em 2026-08-21. Três papers de viés de resposta baixados e lidos; disponibilidade de logprob verificada por provedor.

---

## Resumo do que esta missão muda

1. **O gargalo de corpus está resolvido, por uma quarta via que não estava nas três opções da M05.** Em vez de medir cobertura por perplexidade sobre corpus externo rotulado — que não existe em português —, medir **erro factual de caracterização do estrato**: pedir ao modelo fatos verificáveis sobre o grupo e pontuar contra POF/PNAD. Não precisa de corpus, é barato, e é **não-circular** porque usa itens diferentes dos do desfecho.

2. **Viés de recência é o achado operacional mais forte da literatura de instrumento.** Rupprecht, Ahnert e Strohmaier (2025), com 167 mil entrevistas simuladas: **todos** os modelos favorecem desproporcionalmente a última opção apresentada, **em até 20 vezes**. Randomização de ordem deixa de ser refinamento e vira requisito de validade.

3. **LLMs não têm aquiescência — têm o oposto, e só em inglês.** Braun (2025): viés a responder **"não"**, independentemente de isso indicar concordância ou discordância. Sem padrão claro em alemão e polonês. **Ninguém testou em português.** O T2 ganha uma contribuição lateral de graça.

4. **⚠️ Restrição dura de API: a Anthropic não expõe logprobs.** OpenAI (`top_logprobs` de 0 a 5) e Gemini via Vertex (1 a 20) expõem; a Anthropic não. Isso quebra a comparabilidade entre modelos no caminho de logprob e força o *describe pathway* como via primária.

---

## 1. Decisão do gargalo de corpus

### O problema herdado

A M04 propôs medir distância por perplexidade sobre sub-corpora rotulados por estrato, no padrão Dunn et al. A M05 mostrou que corpus assim não existe em português: os candidatos são orais, regionais e pequenos, e o maior deles — C-ORAL-BRASIL I — tem 208 mil palavras contra os 86 mil sub-corpora de Dunn et al. As três saídas listadas eram abandonar D1, construir o corpus, ou reformular D1 como medida interna ao modelo.

### A quarta via: erro de caracterização do estrato

> **D1′(s) = erro factual do modelo ao descrever o estrato s, pontuado contra POF/PNAD.**

Pergunta-se ao modelo, sem qualquer item do survey, um conjunto de fatos verificáveis sobre o estrato: rendimento médio, tamanho médio do domicílio, escolaridade modal da pessoa de referência, participação das principais categorias de despesa no orçamento, taxa de posse de bens duráveis. Compara-se com o valor oficial. O erro agregado é a medida de distância.

### Por que isso é melhor que perplexidade sobre corpus

| Critério | Perplexidade sobre corpus | Erro de caracterização |
|---|---|---|
| Precisa de corpus rotulado em português | **Sim — e não existe** | Não |
| Custo | Alto (coleta e rotulagem) | Trivial (uma chamada por estrato) |
| O que mede | Previsibilidade do texto produzido pelo grupo | **Conhecimento do modelo sobre o grupo** |
| Erro de imputação ecológica | Sim, se o estrato for imputado por setor | Não |
| Interpretabilidade para revisor de marketing | Baixa | **Alta** |

O segundo ponto é o argumento decisivo. Perplexidade mede quão previsível é o texto de um grupo, que é um proxy indireto de cobertura. O erro de caracterização mede diretamente **quanto o modelo sabe sobre aquele grupo** — que é a variável de que a hipótese realmente precisa.

### Por que não é circular

A objeção óbvia: usar o modelo para medir a distância que explica o erro do próprio modelo. A defesa tem duas camadas:

1. **Objetos diferentes.** D1′ é computado sobre uma tarefa de **conhecimento factual sobre o grupo**, com resposta verificável contra dado oficial. O desfecho E(s) é computado sobre uma tarefa de **simulação de resposta de survey**, comparada a uma distribuição. Prompts distintos, itens disjuntos, critérios de correção distintos. Entropia da tarefa A prevendo erro na tarefa B é relação preditiva legítima, não tautologia.
2. **D1′ tem verdade externa.** Não é medida de autoconfiança do modelo — é medida de **acerto contra o IBGE**. Um modelo pode estar muito confiante e muito errado, e D1′ captura o errado, não o confiante.

**Blindagem adicional obrigatória:** reportar também a **entropia** da distribuição de saída na tarefa de caracterização, separadamente do erro. Se erro e entropia divergirem — modelo confiante e errado em estratos periféricos — isso é um achado por si só, e é o achado mais interessante possível: o modelo não sinaliza a própria ignorância justamente onde ela é maior.

### Consequência

A pendência da M04 de construir 250 itens lexicais de controle em português **dissolve-se**. Não é mais necessária.

O CFst (D3) permanece como medida secundária, com a ressalva de N≈1.500 do WVS Brasil registrada na M05. A pegada digital (Dd) permanece na forma reformulada — uso produtor de texto contra uso consumidor de conteúdo.

---

## 2. Caminhos de extração — e a restrição da Anthropic

### Disponibilidade de log-probabilidade por provedor

| Provedor | Logprobs | Detalhe |
|---|---|---|
| **OpenAI** | ✅ | `logprobs: true` com `top_logprobs` entre 0 e 5 |
| **Google Gemini / Vertex AI** | ✅ | Parâmetro `logprobs` inteiro entre 1 e 20 |
| **Anthropic** | ❌ | Não expõe. Existem propostas e implementações de terceiros para *estimar* confiança, mas não é funcionalidade da API |
| **Pesos abertos (Llama, Mistral, gemma) via inferência local** | ✅ | Acesso completo à distribuição |

**Implicação de desenho:** o caminho de logprob não cobre todos os modelos. Comparar modelos usando logprob onde disponível e outra coisa onde não está introduz confundimento entre modelo e método de extração.

**Decisão:** o *describe pathway* é a **via primária**, porque funciona em todos os provedores, é o mais barato, e Jang et al. mostraram que reduz o erro à metade (TV 0,22 contra 0,46, ver M03). Logprob entra como **validação convergente** no subconjunto que o suporta.

### Os quatro caminhos, especificados

| Caminho | Chamadas por célula | Cobertura de provedor | Papel |
|---|---|---|---|
| **P1 — Describe** | 1 | Todos | **Primário.** Pede a distribuição de respostas do estrato diretamente |
| **P2 — Logprob** | 1 | OpenAI, Gemini, pesos abertos | Validação convergente. Extrai probabilidade dos tokens das alternativas |
| **P3 — PPA** | k (proposto: 50) | Todos | Comparação. Agregação por persona com ordem de opções e fraseado randomizados a cada chamada |
| **P4 — Agregação simples** | k (proposto: 50) | Todos | **Linha de base negativa.** É o método que a literatura usa e que Jang et al. demolem. Serve para demonstrar o quanto ele erra |

Incluir P4 é deliberado: sem ele, o T2 não consegue mostrar que o pipeline dominante mede artefato. **P4 não é desperdício, é o contrafactual.**

---

## 3. Estrutura da persona

Três modos de condicionamento, herdados de Santurkar et al. (ver M01) e rodados os três:

| Modo | Forma |
|---|---|
| `QA` | Informação do grupo como resposta a uma pergunta de múltipla escolha anterior, na fraseologia da própria PNAD |
| `BIO` | Texto livre biográfico em primeira pessoa — é o modo de Argyle |
| `PORTRAY` | Instrução direta para assumir o papel de membro do grupo |

### Gabarito do modo BIO

Templating a partir das variáveis do estrato definidas na M05, em primeira pessoa, ordem fixa, sem adjetivos avaliativos:

```
Moro na região {REGIÃO}, em área {urbana|rural}.
Tenho {IDADE} anos e me identifico como {COR/RAÇA}.
Estudei até {ESCOLARIDADE}.
A renda total mensal da minha família é de {FAIXA EM R$}.
Somos {N} pessoas no domicílio.
```

Regras de construção, cada uma com uma razão:

- **Sem adjetivo avaliativo.** Nada de "humilde", "batalhador", "de classe média". Adjetivo carrega estereótipo e contamina a resposta com o que o modelo acha que aquele grupo *deveria* responder.
- **Faixa de renda em reais, não em salários mínimos.** O salário mínimo mudou de valor entre 2009 (referência da POF) e o corte de treino dos modelos; reais nominais da POF são ambíguos no tempo. **Registrar como ameaça na M08** — este é um ponto em que o confundidor temporal da M05 entra pelo instrumento.
- **Ordem fixa entre estratos**, para que a variação observada seja de conteúdo e não de estrutura.
- **Sem menção a consumo** na persona, para não ancorar a resposta subsequente.

---

## 4. Controles de viés de resposta

### O que a literatura estabeleceu

**Rupprecht, Ahnert e Strohmaier (2025)** — arXiv:2507.07188v3, 16/10/2025. Universidade de Mannheim, GESIS Leibniz e Complexity Science Hub Viena. **167.000 entrevistas simuladas**, nove LLMs, questões normativas do World Values Survey, **dez perturbações** sobre estrutura das alternativas (erros de digitação, sinônimos) e sobre fraseado da questão (ordem das respostas, estrutura de escala).

- **Viés de recência consistente em todos os modelos testados**, com a última alternativa apresentada favorecida **em até 20 vezes**.
- Modelos maiores são mais robustos (citam Llama-3.3-70B-Instruct e Gemini-1.5-Pro), mas **mesmo os maiores são sensíveis a mudanças no fraseado**.
- Pretendem liberar o dataset de perguntas e respostas com perturbações.

**Braun (2025)** — arXiv:2509.08480v1, 10/09/2025. Universidade de Marburg. Cinco modelos (Llama-3.1-8B-Instruct, Mistral-Small-24B-Instruct-2501, gemma-2-27b-it, Llama-3.3-70B-Instruct, gpt-4o-2024-08-06), nove tarefas, **três línguas: inglês, alemão e polonês**.

- Converter a questão para formato sim/não **influencia significativamente** as respostas, em todas as tarefas, modelos e línguas.
- Em inglês: **ao contrário dos humanos, os modelos são enviesados a responder "não"**, independentemente de isso indicar concordância ou discordância.
- **Sem padrão claro em alemão e polonês.**
- Referência de magnitude humana: Krosnick (1999) estima o efeito de aquiescência humana em torno de **10%**.
- Recomendação clássica de desenho de survey que eles reiteram: **evitar questões sim/não e concorda/discorda**.

**Tjuatja, Chen, Wu, Talwalkar e Neubig (2024)** — *Transactions of the ACL*, 2024.tacl-1.56. Carnegie Mellon. Nove modelos. Estudam aquiescência, ordem de resposta, flutuação de opinião e estrutura de escala.

- Modelos populares, abertos e comerciais, **geralmente falham em refletir comportamento humano**, particularmente os que passaram por RLHF.
- Mesmo quando um modelo muda na mesma direção que humanos, **é sensível a perturbações que não movem humanos**.

### Os controles obrigatórios do T2

| Controle | Implementação | Justificativa |
|---|---|---|
| **Randomização de ordem das alternativas** | Ordem sorteada por chamada, com semente registrada | Recência de até 20× (Rupprecht et al.). Sem isso, o efeito de estrato é confundido com posição |
| **Ordem reversa balanceada** | Metade das chamadas com escala invertida | Separa efeito de posição de efeito de conteúdo |
| **Proibição de formato sim/não e concorda/discorda** | Todos os itens em escala ordinal ou escolha entre alternativas substantivas | Braun (2025) e a recomendação clássica de desenho |
| **Teste de aquiescência em português** | Subconjunto de itens replicado em formato sim/não, comparado ao formato ordinal | **Contribuição lateral.** Braun testou inglês, alemão e polonês; português está em aberto |
| **Ausência de âncora numérica no prompt** | Nenhum valor de referência de preço ou quantidade antes da resposta | Ancoragem é viés replicado por LLM (Jones e Steinhardt, citado por Braun) |
| **Perturbação de paráfrase** | Cada item em duas redações semanticamente equivalentes | Rupprecht et al. mostram sensibilidade a paráfrase mesmo nos maiores modelos |
| **Item de atenção** | Item com resposta objetivamente correta, embutido | Detecta colapso degenerado (C1 da M03) sem precisar de análise de logit |

### A contribuição lateral que vale explicitar

Braun testou três línguas e achou o viés anti-aquiescência **apenas em inglês**. Ele próprio não explica por quê. Se o T2 rodar o teste em português e achar padrão — em qualquer direção — é o quarto ponto de uma curva que hoje tem três, e é barato: um subconjunto de itens replicado em dois formatos.

Isso **não é o paper**, e não deve virar. Entra como seção de robustez com meia página e uma tabela. Mas é o tipo de achado que um discussant cita.

---

## 5. Protocolo de versionamento

Bisbee et al. mostraram que **o mesmo prompt produz resultados significativamente diferentes ao longo de meses** (ver M01). Rupprecht et al. e Braun mostram sensibilidade a paráfrase e formato. Sem protocolo, o T2 não é reproduzível e o revisor sabe disso.

### Registro obrigatório por chamada

```
{
  "modelo_id": "gpt-4o-2024-08-06",        // string exata da versão, nunca alias
  "provedor": "openai",
  "data_hora_utc": "...",
  "temperatura": 0.0,
  "top_p": 1.0,
  "seed": 20261119,                         // onde suportado
  "caminho_extracao": "P1|P2|P3|P4",
  "modo_condicionamento": "QA|BIO|PORTRAY",
  "estrato_id": "L2_renda3_sudeste",
  "item_id": "...",
  "ordem_alternativas": [3,1,4,2],
  "variante_parafrase": "A|B",
  "prompt_sha256": "...",                   // hash do prompt exato enviado
  "resposta_bruta": "...",
  "logprobs": {...}                          // quando disponível
}
```

Três regras:

1. **Nunca usar alias de modelo.** `gpt-4o` aponta para versões diferentes ao longo do tempo; `gpt-4o-2024-08-06` não. Braun cita a versão datada exatamente por isso.
2. **Hash do prompt exato.** Permite provar depois que a redação não mudou entre células.
3. **Janela de coleta declarada e curta.** Coletar todos os modelos na menor janela possível e reportar as datas. Se a coleta atravessar uma atualização de modelo, a série quebra.

### Grade de temperatura

Argyle et al. usaram 0,7; a temperatura 0,001 fez o GPT-3 classificar todos os respondentes como brancos (ver M01). Jang et al. mostram gap de logit de até 14 nats, **fora do alcance recuperável por qualquer temperatura** (ver M03).

**Decisão:** temperatura não é configuração, é fator. Rodar `{0,0 · 0,7 · 1,0}` no caminho P3 e P4. Em P1 e P2 a temperatura é irrelevante por construção — mais um argumento a favor de P1 como primário.

---

## 6. Decisão sobre desejabilidade social

Pendência aberta na M01: a POF tem subdeclaração conhecida em categorias sensíveis, assim como o ATP tem viés de desejabilidade que Santurkar et al. admitem contaminar a referência humana.

**Decisão em duas partes:**

1. **Análise primária exclui categorias sensíveis.** Fora: bebida alcoólica, tabaco, jogos e apostas. Nessas, o "erro" do modelo mistura falha do modelo com falha do benchmark, e não há como separar.
2. **Análise secundária pré-registrada usa exatamente essas categorias, com o sinal invertido.** A hipótese é que o modelo, treinado em texto e não em declaração a entrevistador, **subdeclare menos** que o respondente humano. Se a resposta sintética estiver *acima* da POF justamente nas categorias sensíveis, isso é evidência de que a distância entre os dois não é só erro do modelo.

A parte 2 é o "segundo achado, não ruído" que a M01 antecipou. E ganhou relevância com a M05: **a POF 2024-2025 passa a investigar gastos com apostas eletrônicas**, categoria nova e socialmente carregada.

---

## Pendências geradas

- [ ] Definir o conjunto exato de fatos verificáveis da tarefa D1′ e a regra de pontuação do erro de caracterização.
- [ ] Verificar se Rupprecht et al. já liberaram o dataset de perturbações — se sim, importar em vez de reconstruir.
- [ ] Confirmar suporte a `seed` por provedor; onde não houver, documentar a não-reprodutibilidade exata.
- [ ] **M08:** registrar a ameaça de ambiguidade temporal das faixas de renda em reais nominais da POF dentro do prompt.
- [ ] **M07:** as métricas precisam acomodar P1 (que devolve distribuição declarada) e P3/P4 (que devolvem contagens) na mesma escala.
- [ ] **M10:** com P1 custando uma chamada por célula, o cálculo de poder muda de natureza — a incerteza relevante passa a ser entre paráfrases e entre execuções, não entre respostas.
- [ ] Ler Park et al. (2023, 2024), pendência ainda aberta desde a M03: condicionamento por entrevista pode ser um quarto modo, superior aos três de Santurkar.
