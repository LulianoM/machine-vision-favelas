# M26 — Especificação de implementação do coletor

Executada em 2026-08-21. Fecha o Bloco C. **Especificação, não implementação.**

---

## Quatro regras duras

Tudo o mais decorre delas.

1. **A resposta bruta é imutável e nunca se perde.** Métodos de extração vão mudar; a série só sobrevive se o texto original permitir recomputar tudo. Perder o bruto é perder o estudo.

2. **Nada que o instrumento produz pode ser irreproduzível.** Prompt com hash, versão de modelo datada, semente registrada, geolocalização fixada. Se uma célula não puder ser reexecutada em condições declaradas, ela não entra.

3. **Toda coleta é retomável.** Trinta mil respostas por rodada vão falhar no meio. Uma rodada que precisa recomeçar do zero é uma rodada que não acontece.

4. **Nada de raspagem.** Só APIs licenciadas ou oficiais. A restrição jurídica da M22 é regra de arquitetura, não observação.

---

## 1. Camadas

```
argos-geo/
├── universe/       marcas, categorias, prompts — tudo congelado e versionado
├── engines/        um adaptador por provedor, interface única
├── runner/         orquestra a rodada; retomável, idempotente
├── store/          persistência bruta e derivada
├── extract/        menção, citação, sentimento — versionado
├── metrics/        índices de concentração
└── audit/          verificações de integridade e relatórios de rodada
```

A separação entre `extract` e `store` é a mais importante: **extração é derivada e recomputável; armazenamento bruto é fonte de verdade.**

---

## 2. `universe` — o que é congelado

Conteúdo versionado em repositório, não em banco. Alteração é *commit*, com data e justificativa.

| Artefato | Conteúdo |
|---|---|
| `categories.yaml` | Categorias, mercados, mapeamento para categorias do Top of Mind (M25) |
| `prompts.yaml` | Texto, língua, categoria, camada de intenção, tem-marca, **SHA-256** |
| `brands.yaml` | Marca, categoria, mercado, aliases e grafias, **fonte de entrada no universo** (M25: Top of Mind · levantamento próprio · menção em piloto) |
| `engines.yaml` | Provedor, identificador de modelo **datado**, parâmetros, geolocalização |

**Regra de congelamento:** depois da rodada 1, nada é editado. Acréscimos entram como **novo conjunto com nova versão**, e as análises declaram qual versão usam.

O campo de **aliases** em `brands.yaml` é o que evita o erro mais provável de extração: "Nike", "nike", "NIKE Brasil" e "Tênis Nike" são a mesma marca; sem tabela de grafias, a contagem se fragmenta e o índice de concentração cai artificialmente.

---

## 3. `engines` — interface única, comportamentos diferentes

```
interface Engine:
    id, provider, model_version, supports_citations: bool
    query(prompt_text, seed?, geo) -> RawResponse

RawResponse:
    text, citations[]?, latency_ms, provider_request_id,
    model_version_returned, raw_payload  ← guardar o JSON inteiro
```

Um adaptador por provedor: ChatGPT, Gemini, Claude, Perplexity, Google AI Overviews, e o **SERP orgânico** — que implementa a mesma interface, devolvendo posições em vez de texto corrido.

Tratar o SERP como mais um `Engine` é a decisão de arquitetura que faz o desenho de canais pareados funcionar sem código paralelo.

**Dois cuidados por provedor:**

- `model_version_returned` guarda o que o provedor **de fato** usou, que pode divergir do solicitado. Divergência é evento de auditoria.
- `supports_citations` explicita a assimetria da M21 — de 95% no Perplexity a 10% no Claude — para que a camada de métricas nunca compare citação entre motores sem condicionar.

---

## 4. `runner` — retomável por construção

**Unidade de trabalho:** a tupla `(run_id, prompt_id, engine_id, repetition)`. Uma linha de tarefa por tupla, com estado `pendente · em_curso · concluída · falhada`.

```
run(run_id):
    plano = produto_cartesiano(prompts_ativos, engines, repeticoes)
    persistir_plano(plano)              # antes de qualquer chamada
    para cada tarefa pendente:
        com limite_de_taxa(provedor):
            resposta = engine.query(...)
            persistir_bruto(resposta)   # commit imediato
            marcar_concluida()
```

**Persistir o plano antes de chamar** é o que torna a rodada auditável: sabe-se exatamente o que deveria ter sido coletado, e a diferença entre planejado e concluído é a taxa de falha da rodada — que vira coluna de qualidade na análise.

**Repetições:** 10 por prompt-motor. **Nunca em paralelo dentro do mesmo par**, para não acionar cache do provedor e produzir dez respostas idênticas que pareceriam colapso de variância quando são artefato de infraestrutura. Intercalar entre prompts.

**Limite de taxa e recuo exponencial por provedor**, com teto de tentativas. Tarefa que falha três vezes é marcada `falhada` com o erro, e a rodada segue.

---

## 5. `store` — bruto e derivado, separados

```
raw_response      run_id, prompt_id, engine_id, repetition,
                  texto, payload_json, latencia, coletado_em_utc,
                  model_version_returned                    ← IMUTÁVEL

extraction_run    extraction_id, metodo, versao, executado_em

mention           extraction_id, response_id, brand_id, posicao, sentimento
citation          extraction_id, response_id, dominio, url, posicao, tipo_pagina
serp_position     extraction_id, response_id, brand_id, posicao_organica
```

**`extraction_id` em toda tabela derivada.** Trocar o extrator não sobrescreve nada: cria uma nova execução de extração sobre as mesmas respostas brutas, e as duas coexistem. É o que permite responder à pergunta *"o achado muda se eu trocar o extrator?"* sem recoletar.

**Sem exclusão em nenhuma tabela.** Correção é nova versão.

---

## 6. `extract` — onde mora o risco de medida

Três extratores, cada um versionado:

| Extrator | Tarefa | Risco |
|---|---|---|
| **Menção de marca** | Achar marcas do universo no texto | Grafias, negação ("não recomendo X"), menção genérica |
| **Citação** | Domínios e URLs referenciados | Formato varia muito por provedor |
| **Sentimento** | Enquadramento da menção | ⚠️ Kumar (M21): flutua **6,7× mais** que a própria menção |

**Regras:**

- Menção por **casamento léxico contra a tabela de aliases**, não por modelo. Determinístico, auditável, reproduzível. Modelo só como camada de desambiguação em casos marcados.
- **Validação humana obrigatória em subamostra**, com concordância reportada — mesma exigência que a M03 impôs ao classificador do T2.
- **Sentimento é coletado e não entra na tese.** A instabilidade medida por Kumar o desqualifica como desfecho principal.

---

## 7. `metrics` — puro, sem efeitos colaterais

Funções que recebem uma distribuição sobre o universo fixo e devolvem os índices da M22: HHI, número efetivo, Gini, entropia, C4, C8, C80, sobrevivência de cauda.

**Duas regras:**

- **Marcas do universo não mencionadas entram como zero.** É a decisão central da M22, e o lugar mais provável de erro silencioso — um `groupby` ingênuo simplesmente omite as ausentes e destrói o achado.
- **Bootstrap sobre prompts, nunca sobre respostas.** As 10 repetições do mesmo prompt não são independentes.

---

## 8. `audit` — o que roda depois de cada rodada

Relatório automático, e a rodada não é aceita sem ele:

| Verificação | Alerta |
|---|---|
| Cobertura do plano | Menos de 95% concluído |
| Divergência de versão de modelo | Qualquer ocorrência |
| Taxa de resposta vazia ou erro por motor | Acima de 5% |
| Taxa de citação por motor | Desvio grande da referência da M21 |
| Menções fora do universo | Acima de um limiar — indica universo incompleto |
| Respostas idênticas dentro do mesmo par prompt-motor | Indica cache do provedor |
| Deriva do volume de menções contra a rodada anterior | Indica mudança de modelo do fornecedor |

A penúltima linha é a mais importante em termos práticos: **cache silencioso do provedor é o modo de falha que mais facilmente passaria despercebido** e que produziria exatamente o resultado que a hipótese prevê.

---

## 9. Custo e escala

Por rodada semanal, com 6 categorias:

```
50 prompts × 5 motores × 10 repetições × 2 línguas × 6 categorias = 30.000 chamadas
+ SERP orgânico: 50 × 2 × 6 = 600 consultas (sem repetição — resultado é determinístico o bastante)
```

| Item | Ordem de grandeza |
|---|---|
| APIs de LLM | Dezenas de dólares por rodada |
| **API de SERP licenciada** | **A linha material** — depende do fornecedor |
| Armazenamento | Desprezível; texto comprime bem |

**Guardas obrigatórias:** teto de gasto por rodada, com parada automática; estimativa de custo antes de executar, exibida no plano.

**Modo piloto:** 1 categoria, 2 motores, 3 repetições — para validar ponta a ponta antes de ligar a série. **A rodada 1 completa só depois que o piloto reproduzir as ordens de grandeza da M21** (78% de citações a sites corporativos, listicles em torno de 21%).

---

## 10. O que não construir

| Tentação | Por que não |
|---|---|
| Painel bonito | O produto é a série, não a interface. Consultas ad hoc bastam |
| Extração por LLM como método primário | Não é reproduzível nem auditável; casamento léxico é |
| Detecção de mudança de modelo em tempo real | A auditoria semanal já pega |
| Raspagem própria de SERP ou de AI Overviews | Viola termos de uso. **Regra, não preferência** |
| Cobertura de mais motores no início | Cada motor multiplica custo e superfície de falha. Cinco bastam |

---

## Pendências geradas

- [ ] Escolher e contratar o fornecedor de API de SERP — **destrava o canal orgânico e é a única decisão de custo**.
- [ ] Construir `brands.yaml` com tabela de aliases por marca; é o artefato que mais afeta a qualidade da medida.
- [ ] Definir o limiar de "menções fora do universo" que dispara revisão.
- [ ] Rodar o piloto e comparar com as referências de Kumar antes de ligar a série.
- [ ] Verificar quais provedores expõem `seed` e documentar a irreprodutibilidade exata onde não houver.
- [ ] Confirmar política de cache de cada provedor — determina o intervalo mínimo entre repetições.
