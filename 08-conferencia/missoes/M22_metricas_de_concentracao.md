# M22 — Índices de concentração e o contrafactual orgânico

Executada em 2026-08-21.

---

## Resumo do que esta missão resolve

1. **O contrafactual estava travado e destravou por reformulação, não por acesso a dado.** Não é preciso comprar dados de clique nem depender de Search Console de terceiros. **Basta rodar o mesmo conjunto de prompts nos dois canais** — motores de IA e busca clássica — e comparar a concentração da distribuição de marcas. O contrafactual é a própria página de resultados.

2. **A decisão metodológica que torna tudo comparável: fixar o universo de marcas a priori**, por categoria e mercado, e computar os índices sobre esse conjunto fixo, com marcas não mencionadas entrando como zero. Sem isso, nenhum índice é comparável entre canais, categorias ou línguas.

3. **O índice principal não é HHI nem Gini — é o número efetivo de marcas.** "A resposta de IA apresenta efetivamente 3,2 marcas onde a busca orgânica apresenta 8,7" é a frase que a plateia da AIM entende sem tradução. É o mesmo movimento do tamanho efetivo de amostra na M07 e do Vendi Score na M14.

---

## 1. Da menção à participação

Antes de qualquer índice, é preciso uma distribuição que some 1. Menção bruta não soma: uma resposta cita várias marcas.

| Definição | Fórmula | Problema |
|---|---|---|
| Taxa de menção | respostas em que `b` aparece / total de respostas | Não é distribuição — soma passa de 1 |
| **Participação de menção** | menções de `b` / total de menções na categoria | ✅ **Primária** |
| Participação ponderada por posição | menções de `b` ponderadas pela ordem de aparição | Secundária — testa se aparecer primeiro importa |

**Decisão:** participação de menção como primária; ponderada por posição como robustez.

---

## 2. A decisão que torna os índices comparáveis

⚠️ **Todo índice de concentração depende do número de unidades no universo.** Um HHI calculado sobre as 5 marcas que apareceram não é comparável a um calculado sobre as 30 que poderiam ter aparecido. E é justamente aí que mora o efeito: **a IA concentra porque menciona menos marcas distintas.**

> **Regra: o universo de marcas é fixado a priori, por categoria e mercado, a partir de lista externa** — participação de mercado publicada, associação setorial, ou levantamento próprio pré-registrado. Marcas do universo que não foram mencionadas entram com participação **zero**.

Sem essa regra, o efeito principal — desaparecimento da cauda — some por construção, porque marcas ausentes simplesmente não entram na conta.

**Consequência prática:** a construção do universo de marcas precisa ser feita **antes** da primeira rodada e congelada, como os prompts (M21).

---

## 3. Os índices

Para cada célula `(categoria, mercado, canal, motor, período)`, com participações `s₁ … s_N` sobre o universo fixo de `N` marcas:

### Primário — número efetivo de marcas

```
HHI      = Σᵢ sᵢ²
N_efet   = 1 / HHI
```

Inverso do índice de Simpson. Vale **1** quando toda a atenção vai a uma marca e **N** quando ela se divide igualmente. Interpretação direta: *quantas marcas o canal efetivamente apresenta*.

### Secundários

| Índice | Fórmula | O que detecta |
|---|---|---|
| **HHI** | `Σ sᵢ²` | Concentração no topo. **É a linguagem nativa da economia industrial** — a plateia da AIM reconhece |
| **Gini** | Área entre a curva de Lorenz e a diagonal, ×2 | Desigualdade ao longo de **toda** a distribuição, não só no topo |
| **Entropia de Shannon** | `−Σ sᵢ log sᵢ` | Complementar ao HHI; base do número efetivo por outra via |
| **C4 e C8** | Participação acumulada das 4 e das 8 maiores | Simples, e é o que reguladores usam |
| **Sobrevivência da cauda** | Participação das marcas fora do top-k | **O desfecho substantivo** — mede quem some |
| **C80** | Quantas marcas são necessárias para acumular 80% da atenção | Interpretável e robusto |

### A curva de Lorenz é a figura

Duas curvas no mesmo gráfico — canal orgânico e canal de IA, mesma categoria, mesmo conjunto de prompts. **A área entre elas é o achado.** É a figura do T1, do mesmo modo que a curva de cobertura decrescente é a do T2 (M07).

### Cuidados

- **Bootstrap sobre prompts**, não sobre respostas. A unidade de reamostragem é o prompt, porque as 10 repetições do mesmo prompt não são independentes.
- **Reportar `N` do universo** em toda tabela.
- **Índices são não-lineares**: a média de HHIs entre motores não é o HHI da média. Agregar com cuidado e declarar como.

---

## 4. O contrafactual orgânico

### A reformulação que destrava

O plano anterior era conseguir distribuição de cliques por categoria — o que exigiria dados pagos ou Search Console de parceiros, e foi a pendência que travou o T1 desde a M21.

**Não é necessário.** O contrafactual correto é mais simples e é totalmente auto-coletável:

> **O mesmo prompt, nos dois canais.** Para cada prompt do conjunto congelado, coletar (a) a resposta dos motores de IA e (b) a página de resultados orgânicos da busca clássica. Extrair a distribuição de marcas em ambos, sobre o mesmo universo fixo. Comparar os índices.

Isso responde exatamente à pergunta que sobrou depois de Kumar (M21): **a migração de canal aumenta a desigualdade de visibilidade, e quanto?**

### Dois níveis de comparação

| Nível | O que compara | Força |
|---|---|---|
| **Presença** | Marcas no top-10 orgânico contra marcas na resposta de IA | Simples, mas trata posição 1 e 10 como iguais |
| **Atenção** | Posições orgânicas ponderadas por curva de CTR, contra menções na IA | **É a comparação que responde à pergunta** |

O nível de presença subestima a concentração orgânica: um resultado em décimo lugar existe, mas quase ninguém clica. **Sem a ponderação, o orgânico parece mais plural do que é, e o efeito da IA é superestimado.** Reportar os dois.

### As curvas de CTR disponíveis

> ⚠️ **Todas são estudos de fornecedor, não revisados por pares.** São a melhor evidência pública disponível e devem ser tratadas como aproximação, com sensibilidade reportada.

Valores da SISTRIX, citados de forma consistente em levantamentos de 2026:

| Posição | CTR |
|---|---|
| 1 | **28,5%** |
| 2 | 15,7% |
| 3 | 11,0% |
| 10 | 2,5% |

E a variação por composição da página, que é o achado mais importante para o T1:

- CTR de posição 1 varia de **13,7% a 46,9%** conforme o layout do resultado.
- Em página puramente orgânica no celular: **34,2%**. Com painel de conhecimento: **16,8%**. Com resultados de compras dominando: **13,7%**.
- Análise da SISTRIX sobre **mais de 100 milhões de palavras-chave alemãs**: o CTR da posição 1 **cai 59% quando um AI Overview aparece**.

**A última linha é diretamente relevante e deve ser citada com a ressalva de fornecedor.** Ela quantifica o mecanismo que o T1 mede, e vem de uma base de escala.

**Decisão:** usar a curva SISTRIX como principal e reportar sensibilidade a pelo menos duas curvas alternativas. Se a ordenação dos índices entre canais não mudar entre curvas, o achado é robusto à escolha.

### ⚠️ A restrição jurídica, que é a verdadeira barreira

Coletar página de resultados de busca de forma automatizada viola os termos de uso do Google. **Isto é problema jurídico, não técnico**, e é o mesmo obstáculo já registrado na M21 para AI Overviews.

Três caminhos, e nenhum é gratuito:

| Caminho | Viabilidade |
|---|---|
| **Fornecedor de API de SERP** licenciado | Custo mensal, mas legítimo e citável em método. **Recomendado** |
| Coleta própria automatizada | Viola termos de uso. **Descartar** — não vale o risco num trabalho acadêmico assinado |
| Search Console próprio | Cobre um domínio; insuficiente para distribuição de categoria |

**Orçar o fornecedor de API de SERP como custo de pesquisa.** É a única linha de custo material do T1, e sem ela o contrafactual não existe.

---

## 5. A especificação da comparação

```
Para cada (categoria c, mercado m, período t):

  Universo fixo de marcas B(c,m), congelado antes da rodada 1

  Canal IA:      s^IA_b   = menções de b / total de menções   (por motor e agregado)
  Canal orgânico: s^ORG_b = Σ_posições CTR(pos) · 1[b na posição] / normalizador

  Δ N_efet(c,m,t) = N_efet^ORG − N_efet^IA      ← o desfecho principal
  Δ Gini,  Δ HHI,  Δ cauda                       ← secundários

Hipótese H1:  Δ N_efet > 0        (a IA apresenta menos marcas efetivas)
Hipótese H2:  Δ N_efet é maior em pt-BR que em en-US
```

**H2 é o diferencial do T1** e o que Kumar não pode responder.

---

## Pendências geradas

- [ ] **Orçar fornecedor de API de SERP** com cobertura de Brasil e Estados Unidos. É a linha de custo que viabiliza o contrafactual.
- [ ] Construir e congelar o universo de marcas por categoria e mercado, com fonte declarada.
- [ ] Localizar as fontes primárias das curvas de CTR (SISTRIX e ao menos duas outras) e verificar metodologia e ano — os números aqui vêm de levantamentos secundários.
- [ ] Verificar se a queda de 59% no CTR com AI Overview tem publicação metodológica própria — se tiver, é citação forte.
- [ ] Definir a regra de agregação entre motores, dado que os índices são não-lineares.
- [ ] **M23 herda:** verificar se Agarwal e Sen (2026) construíram algum contrafactual desse tipo — se sim, o desenho precisa se diferenciar.
- [ ] Testar a sensibilidade dos índices ao tamanho do universo `N` em simulação, antes de fixar as categorias.
