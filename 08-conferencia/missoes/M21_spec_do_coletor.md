# M21 — Especificação do coletor do T1

Executada em 2026-08-21. Abre o Bloco C.

---

## ⚠️ Achado competitivo antes da spec

**Referência verificada:** KUMAR, Pratyush. *Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines*. arXiv:2606.20065v1 [cs.IR], 18 de junho de 2026. Autor vinculado à **Ranqo**, ferramenta comercial de GEO.

**100 mil respostas de prompt, 100+ marcas, entre março e maio de 2026.** E o achado central é a tese de concentração do T1, já medida:

> **Escada de três degraus por estatura de marca.** Nomes globais como Stripe e Nike aparecem em **73%** das respostas de IA relevantes na primeira rodada de rastreamento; marcas médias e regionais estabelecidas como Olipop e Klaviyo, em **44%**; marcas de nicho e pequenas, em **11%**. Cada degrau cerca de 30 pontos percentuais abaixo do anterior.

Estatística de apoio: Kruskal-Wallis rejeitando igualdade entre degraus (H = 38,32, gl = 2, p = 4,78 × 10⁻⁹); Mann-Whitney pareado sobrevivendo a Bonferroni nas três direções, com **d de Cohen de 1,57** (degrau 1 contra 2) e **2,34** (degrau 1 contra 3).

### O que sobra para o T1

A concentração está medida. Mas o trabalho tem quatro fragilidades que definem a faixa remanescente:

| Fragilidade de Kumar (2026) | O que o T1 pode fazer |
|---|---|
| **Amostra são marcas rastreadas na Ranqo** — ou seja, marcas que pagam por ferramenta de GEO. Seleção massiva | Amostra de marcas de categorias reais de consumo, independente de quem contrata GEO |
| **Sem contrafactual.** Mede concentração na IA, mas não contra a distribuição de cliques orgânicos da mesma categoria | O contrafactual orgânico é a contribuição — sem ele não se sabe se a IA concentra *mais* que a busca |
| **Sem índice formal de desigualdade.** Reporta taxas por degrau, não HHI, Gini ou curva de Lorenz | Medida contínua em vez de degraus definidos a priori |
| **Presumivelmente só em inglês** | Eixo de língua |
| Preprint de fornecedor, não revisado por pares | — |

**A segunda linha é a mais importante.** "Marcas grandes aparecem mais na IA" é banal sem comparação: marcas grandes também aparecem mais na busca orgânica. **A pergunta é se a IA concentra mais que o canal que ela substitui**, e ninguém respondeu.

> **Reposicionamento do T1, terceira vez:** não é "há concentração" (Kumar), nem "como otimizar" (Aggarwal et al., KDD 2024), mas **"a migração de canal aumenta a desigualdade de visibilidade, e quanto?"**

---

## 1. Motores e a assimetria que quebra a comparação

Kumar reporta taxa de citação de fonte por motor:

| Motor | Cita fonte em |
|---|---|
| Perplexity | **95%** |
| Gemini | 35% |
| Grok | 20% |
| ChatGPT | 15% |
| Claude | **10%** |

> ⚠️ **Consequência metodológica dura: "citação" não é comparável entre motores.** Um índice de concentração de domínios citados no Claude descreve os 10% de respostas que citam algo. Comparar isso com o Perplexity é comparar coisas diferentes.

**Decisão para o coletor: separar dois desfechos, sempre.**

| Desfecho | Definição | Comparável entre motores? |
|---|---|---|
| **Menção de marca** | A marca aparece no texto da resposta | ✅ Sim — é o desfecho primário |
| **Citação de fonte** | Um domínio é referenciado | ❌ Não diretamente — analisar por motor, ou condicionado a haver citação |

Cobertura do coletor: **ChatGPT, Gemini, Claude, Perplexity e Google AI Overviews**, mais Grok se o acesso permitir.

---

## 2. Prompts

### A distinção que não pode ser ignorada

Kumar registra que prompts **com marca** inflam a visibilidade — o degrau 2 ganha **+8,6 pontos percentuais**, enquanto o degrau 1 ganha só +0,6, porque já é reconhecido de qualquer jeito.

**Decisão: o conjunto primário é de prompts SEM marca.** Prompts com marca entram como conjunto secundário, e a diferença entre os dois é quantidade de interesse — mede o quanto a marca depende de ser lembrada versus ser descoberta.

### Taxonomia de intenção

Herdada da estrutura que Kumar descreve, adaptada:

| Camada | Exemplo | Papel |
|---|---|---|
| **Descoberta** (sem marca) | "melhor tênis para maratona" | **Primária** — é onde a descoberta acontece |
| Comparação | "Nike Pegasus ou Brooks Ghost" | Secundária — já nomeia marcas |
| **Especialista** | Pergunta técnica de comprador informado | Testa se a concentração cai com profundidade |
| Transacional | "onde comprar X" | Testa o fim do funil |

### Tamanho do conjunto

Kumar afirma que **"uma fatia de 50 prompts já basta para ver concentração de categoria"**, e a referência de categoria dele é: **50 prompts sem marca × 5 motores × 10 repetições = 2.500 respostas**, sobre 10 marcas.

**Adotar essa escala como unidade de categoria**, e replicar por categoria e por língua:

```
50 prompts × 5 motores × 10 repetições × 2 línguas = 5.000 respostas por categoria por rodada
```

Com 6 categorias de consumo: **30.000 respostas por rodada semanal.**

### O pareamento de língua — o diferencial do T1

Cada prompt existe em duas versões, **semanticamente equivalentes e verificadas por tradução reversa**: pt-BR e en-US, com a mesma intenção e a mesma categoria de produto adaptada ao mercado.

⚠️ **Armadilha:** "melhor tênis de corrida" no Brasil e "best running shoes" nos EUA não têm o mesmo conjunto de marcas disponíveis. **Parear por posição no mercado, não por marca.** A comparação é entre *distribuições de concentração*, não entre marcas específicas.

---

## 3. Congelamento e versionamento

O que a M06 fixou para o T2 vale igual aqui, e é mais crítico porque a série é longa:

| Elemento | Regra |
|---|---|
| Texto do prompt | **Congelado.** Hash SHA-256 registrado por prompt |
| Conjunto de prompts | Congelado na rodada 1. Adições entram como conjunto novo, nunca substituem |
| Versão de motor | Registrada por chamada; nunca usar alias |
| Ordem das repetições | Semente registrada |
| Geolocalização | Fixada e declarada — resultado de IA varia por região |
| Modelo de extração de marca | Congelado; se trocar, recomputar toda a série |

**A série só vale se o instrumento não se mexer.** Um prompt reescrito no meio do caminho invalida a comparação temporal, que é o único ativo que o T1 acumula com o tempo.

---

## 4. Frequência

| Parâmetro | Valor | Razão |
|---|---|---|
| Cadência | **Semanal** | Captura atualização de modelo sem custo excessivo |
| Dia e hora | Fixos | Reduz variação intrassemanal |
| Repetições por prompt-motor | **10** | Referência de Kumar; suficiente para estimar taxa de menção |
| Início | **Imediato** | Cada semana perdida é dado que não existirá |

Horizonte: de agosto de 2026 a novembro de 2027 são **cerca de 65 rodadas** — série suficiente para submissão à AIM 2028 com folga.

---

## 5. Esquema de armazenamento

```sql
prompt(
  prompt_id, texto, texto_sha256, lingua, categoria,
  camada_intencao, tem_marca BOOLEAN, congelado_em
)

run(
  run_id, iniciado_em_utc, motor, modelo_versao,
  geolocalizacao, semente, notas
)

response(
  response_id, run_id, prompt_id, repeticao,
  texto_bruto, latencia_ms, erro,
  coletado_em_utc
)

mention(                      -- desfecho primário
  response_id, marca_id, posicao_no_texto,
  sentimento, extraido_por_modelo, extraido_versao
)

citation(                     -- desfecho secundário
  response_id, dominio, url, posicao,
  tipo_pagina                 -- listicle, site corporativo, fórum, vídeo, editorial
)

brand(
  marca_id, nome, categoria, mercado, degrau_estatura, fonte_do_degrau
)

organic_benchmark(            -- o contrafactual
  categoria, mercado, periodo, dominio_ou_marca,
  participacao_cliques, fonte
)
```

**Guardar sempre o `texto_bruto`.** Métodos de extração mudam; o texto original permite recomputar. Sem ele, cada mudança de extrator descarta a série inteira.

---

## 6. Achados de Kumar que o coletor deve poder reproduzir

Servem de validação: se o coletor não reproduzir a ordem de grandeza, há erro de implementação antes de qualquer conclusão.

| Achado | Valor |
|---|---|
| Citações que vão para sites corporativos | **~78%** |
| Fonte não-corporativa mais citada | **YouTube**, à frente de Reddit, mídia editorial e Wikipédia |
| Formato de página mais citado | **Listicle do tipo "melhores X"**, ~21% de todas as citações |
| Instabilidade de sentimento | O enquadramento positivo ou negativo muda **6,7×** mais que a própria menção |

O último é relevante e limita o escopo: **sentimento é ruidoso demais para ser desfecho principal**. Coletar, mas não construir a tese em cima dele.

---

## 7. Referências novas geradas

Citadas por Kumar, **nenhuma verificada diretamente** — todas ⚠️ [NÃO VERIFICADO]:

| Referência | Relevância |
|---|---|
| **Puerto et al. (2025), C-SEO Bench** | Primeiro benchmark sistemático de táticas de SEO conversacional. Achado: *"most of those tactics do not help, and several hurt, while plain source relevance keeps working"*. **Alta prioridade** — se táticas de GEO não funcionam, o eixo de otimização está ainda mais morto do que a M11 concluiu |
| **Kirsten et al. (2025)** | Motores generativos puxam de conjunto de fontes mais amplo e muito diferente do da busca clássica. **Diretamente relevante ao contrafactual do T1** |
| Ranqo (2026b) | Estudo de categoria em CRM, 50 prompts × 5 motores × 10 repetições |

---

## Pendências geradas

- [ ] **Verificar Puerto et al. (2025), C-SEO Bench.** Se táticas de GEO comprovadamente não funcionam, isso muda o enquadramento gerencial do T1 inteiro.
- [ ] Verificar Kirsten et al. (2025) — é a fonte mais próxima do contrafactual.
- [ ] **Resolver o contrafactual orgânico:** de onde vem a distribuição de cliques por categoria e mercado? Search Console próprio cobre um domínio só. Investigar dados públicos de participação de mercado, ou parceria com agências para dados agregados.
- [ ] Definir as 6 categorias de consumo, pareadas Brasil/EUA.
- [ ] Verificar acesso programático a Google AI Overviews e a viabilidade de coleta automatizada sem violar termos de uso — **questão jurídica, não técnica**.
- [ ] Decidir o modelo de extração de marca e menção, e congelá-lo.
- [ ] **M22 herda:** os índices de concentração precisam funcionar sobre menção (comparável) e citação (não comparável entre motores).
- [ ] Corrigir a M11: a varredura competitiva não capturou Kumar (2026), que estava nos resultados da primeira rodada de busca do dossiê e não foi seguido.
