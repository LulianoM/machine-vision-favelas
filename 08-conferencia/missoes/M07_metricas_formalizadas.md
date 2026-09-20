# M07 — Métricas: fórmulas, o que cada uma detecta, regra de decisão

Executada em 2026-08-21.

---

## Resumo do que esta missão muda

1. **Faltava uma métrica, e ela é a melhor de todas para a plateia da AIM: cobertura de intervalo.** Fração das células em que o intervalo de confiança de 95% construído ingenuamente a partir de dados sintéticos contém o valor humano verdadeiro. É o número que um profissional de pesquisa de mercado entende sem tradução.

2. **E ela tem uma propriedade devastadora.** Como o número de consultas é escolha de desenho e não restrição amostral (Brand et al., ver M02), o erro padrão ingênuo tende a zero conforme *k* cresce, enquanto o viés permanece. Logo: **quanto mais dado sintético você coleta, mais confiantemente errado você fica.** Isso é uma figura, não uma nota de rodapé.

3. **Tamanho efetivo de amostra traduz o colapso para o vocabulário nativo da metodologia de survey.** Efeito de desenho de Kish já é o instrumento padrão para quantificar perda de informação quando respondentes não são independentes. Respondentes sintéticos são esse problema no limite.

4. **Boelaert et al. está totalmente verificado agora**, e a leitura do abstract confirma a abertura para o T2 (seção 6).

---

## 1. Notação

Para o estrato `s` e o item `q`:

| Símbolo | Significado |
|---|---|
| `H_s(q)` | Distribuição de referência humana (POF/PNAD, ponderada pelo peso amostral) |
| `M_s(q)` | Distribuição produzida pelo modelo |
| `N` | Número de alternativas, excluída a recusa |
| `n = 1…N` | Índice da alternativa, mapeado a inteiros quando ordinal |
| `F(·)` | Função de distribuição acumulada |
| `k` | Número de chamadas por célula nos caminhos P3 e P4 |
| `r` | Réplica — uma execução completa (variante de paráfrase × semente de ordem × rodada) |

**Regra de forma de dado.** O caminho P1 (*describe*) devolve um vetor de probabilidades declarado; P3 e P4 devolvem contagens. Normalizam-se as contagens para proporções e todas as métricas operam sobre vetores de probabilidade. **A unidade de incerteza é a réplica `r`, para todos os caminhos** — o que resolve a pendência da M06: P1 não tem variabilidade intra-célula, então o intervalo vem de variação entre paráfrases e entre execuções, nunca de variação entre respostas.

---

## 2. As seis métricas

### M1 — Alinhamento por Wasserstein-1 normalizada

Herda a definição de Santurkar et al. (ICML 2023, ver M01), com a fórmula deles preservada para comparabilidade direta:

```
A(M, H; Q) = (1/|Q|) · Σ_q [ 1 − WD₁(M_s(q), H_s(q)) / (N − 1) ]
```

onde `WD₁` é o custo mínimo de transformar uma distribuição na outra, com alternativas ordinais mapeadas a inteiros positivos.

- **Detecta:** deslocamento de posição **e** de dispersão, ponderados pela distância ordinal. Errar por uma categoria custa menos que errar por quatro.
- **Exige:** estrutura ordinal.
- **Domínio:** [0, 1], sendo 1 correspondência perfeita.
- **Regras de codificação herdadas:** recusa omitida do cálculo e comparada à parte; alternativa final de hedge mapeada à média das ordinais restantes.
- **Papel:** métrica primária de fidelidade. Comparável com a literatura.

### M2 — Distância de variação total

```
TV(M, H) = ½ · Σ_n | M_s(q)(n) − H_s(q)(n) |
```

- **Detecta:** qualquer descasamento de massa de probabilidade, **ignorando** distância ordinal.
- **Não exige** estrutura ordinal — é a métrica para desfechos **nominais**, como escolha de marca, onde Wasserstein não faz sentido.
- **Domínio:** [0, 1].
- **Papel:** métrica primária para itens nominais; e comparabilidade direta com Jang et al., que reportam TV de **0,22** no caminho *describe* contra **0,46** na agregação por persona (ver M03). Se o T2 reproduzir essa ordem de grandeza, valida o pipeline; se não reproduzir, há problema de implementação antes de qualquer conclusão substantiva.

### M3 — Razão de variância

Esta é a métrica que **isola o fenômeno**, separado de erro de posição.

Para item ordinal com mapeamento inteiro:

```
Var[P] = Σ_n n²·P(n) − ( Σ_n n·P(n) )²

VR(s,q) = Var[M_s(q)] / Var[H_s(q)]

Reportar em log:   L(s,q) = ln VR(s,q)
```

- **Detecta:** colapso de dispersão, **independentemente de a média estar certa**. É exatamente a patologia que Bisbee et al. descrevem — médias próximas, variância comprimida — e que os quatro critérios de fidelidade de Argyle não capturam (ver M01).
- `VR < 1` é colapso; `VR ≈ 1` é dispersão calibrada; `VR > 1` seria dispersão inflada.
- **Reportar em log** porque a razão é assimétrica: 0,5 e 2,0 são desvios de mesma magnitude e log os torna simétricos em torno de zero.
- **Papel:** o desfecho da hipótese central. Se o T2 tem uma variável dependente, é esta.

### M4 — Kolmogorov–Smirnov

```
KS(s,q) = max_n | F_M(n) − F_H(n) |
```

- **Detecta:** o ponto de pior divergência na acumulada. Complementa Wasserstein, que agrega ao longo de toda a distribuição — KS localiza *onde* a distribuição erra.
- **Exige:** ordinal ou contínuo.
- ⚠️ **Usar como estatística descritiva, não como teste.** O valor-p do teste KS pressupõe amostra aleatória de tamanho fixo, e o *k* sintético é escolha de desenho. Ver seção 4.

### M5 — Tamanho efetivo de amostra e efeito de desenho

O efeito de desenho de Kish é o instrumento padrão da metodologia de survey para quantificar quanta informação se perde quando respondentes não são independentes. Definição usual:

```
deff = n_real / n_efetivo
```

Respondentes sintéticos são esse problema no limite: sob colapso intra-persona (C1 da M03), as `k` chamadas não são `k` observações independentes.

```
deff(s,q) = k · Var_entre_replicas[ p̂ ] / [ p̂(1 − p̂) ]

ESS(s,q) = k / deff(s,q)
```

- **Detecta:** quantas observações humanas independentes o conjunto sintético realmente vale.
- **Papel:** tradução gerencial. Dizer que "500 respostas sintéticas valem 12 respondentes humanos" comunica mais que qualquer divergência.
- **Ponte com a literatura:** Bisbee et al. relatam que populações geradas por LLM apresentam tamanho efetivo de amostra menor que as populações humanas que aproximam. M5 mede exatamente isso, por estrato.

### M6 — Cobertura de intervalo ⭐

A métrica que faltava, e a mais forte para a AIM.

```
IC_naive(s,q) = p̂_M ± 1,96 · sqrt( p̂_M (1 − p̂_M) / k )

Cobertura(k) = (1/|S×Q|) · Σ_{s,q} 1[ p_H(s,q) ∈ IC_naive(s,q) ]
```

Ou seja: constrói-se o intervalo exatamente como faria um pesquisador que trata as respostas sintéticas como respondentes independentes, e conta-se com que frequência o valor humano verdadeiro cai dentro.

- **Detecta:** o **dano prático** do colapso, não a sua magnitude abstrata.
- **Nominal esperado:** 95%. **Predição:** muito abaixo.
- **A propriedade devastadora:** como `k` é escolha do pesquisador e não restrição amostral, o denominador cresce sem limite enquanto o viés `|p̂_M − p_H|` permanece fixo. Logo `IC_naive` estreita e a cobertura **decresce monotonicamente em `k`**.

> **Coletar mais dado sintético aumenta a confiança e não aumenta a informação.** Reportar `Cobertura(k)` para `k ∈ {10, 50, 100, 500, 1000}` e mostrar a curva descendente. É a figura mais citável do paper.

### Decomposição que sustenta M6

```
EQM(s,q) = [ p̂_M − p_H ]²  +  Var_entre_replicas[ p̂_M ]
              └── viés² ──┘      └──── variância ────┘
```

O intervalo ingênuo cobre apenas a parcela de variância. A parcela de viés é **invisível ao pesquisador sem benchmark humano** — que é exatamente a frase de Brand et al. citada na M02: *"a researcher lacking a human benchmark would have had no basis for identifying which estimates were unreliable."* M6 quantifica essa frase.

---

## 3. Cobertura por tipo de desfecho

| Tipo de item | Exemplo | M1 Wass. | M2 TV | M3 VR | M4 KS | M5 ESS | M6 Cob. |
|---|---|---|---|---|---|---|---|
| **Ordinal** | Frequência de compra, escala de importância | ✅ primária | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Nominal** | Escolha de marca, local de compra | ❌ | ✅ primária | ❌ ¹ | ❌ | ✅ | ✅ |
| **Composicional** | Participação das despesas no orçamento | ⚠️ ² | ✅ | ✅ ³ | ❌ | ✅ | ✅ |
| **Contínuo** | Disposição a pagar, valor gasto | ✅ | ⚠️ ⁴ | ✅ | ✅ | ✅ | ✅ |

¹ Para nominal, substituir razão de variância por **razão de entropia**: `ln[ H(M) / H(H) ]`, com `H(·)` a entropia de Shannon. Detecta o mesmo achatamento sem exigir ordem.
² O vetor de participações é literalmente uma distribuição de probabilidade, então TV e KL aplicam-se diretamente. Wasserstein exigiria ordenar as categorias de despesa, o que não tem sentido substantivo. **Não usar Wasserstein em composicional.**
³ Aplicar por categoria, não ao vetor inteiro.
⁴ Para contínuo, TV exige discretização prévia em faixas; declarar as faixas no pré-registro.

**Nota sobre KL:** a divergência de Kullback-Leibler é usada por Heath e Alexander no paper de SSR (ver M03), e entra como métrica de comparabilidade com eles. Exige suavização, porque `H(n) = 0` em alguma célula produz divergência infinita. **Suavização de Laplace com α = 0,5, declarada no pré-registro.**

---

## 4. O problema do *k* — e por que quase nenhum teste clássico vale

Brand et al. formularam o problema com precisão: *"the number of queries submitted to the LLM is a researcher design choice rather than a sampling constraint."*

Consequências, todas restritivas:

| Prática usual | Por que não vale aqui |
|---|---|
| Valor-p do teste KS | Pressupõe amostra aleatória de tamanho fixo; `k` é arbitrário, então o p-valor é arbitrário |
| Erro padrão de `p̂_M` como `sqrt(p(1−p)/k)` | Trata chamadas como independentes; sob colapso C1 elas não são |
| Cálculo de poder sobre `k` | Aumentar `k` não aumenta informação sobre a população |
| Intervalo de confiança sobre a estimativa sintética | É justamente o objeto que M6 mostra estar quebrado |

**A regra do T2:** toda incerteza reportada vem de **variação entre réplicas** — paráfrase, semente de ordem, execução, versão de modelo — via **bootstrap sobre réplicas**, nunca de variação entre chamadas dentro de uma réplica. Isto vale para todos os quatro caminhos de extração e precisa estar escrito no pré-registro em uma frase.

Isso também redefine a M10: o cálculo de poder passa a ser sobre **número de réplicas e número de estratos**, não sobre número de respostas.

---

## 5. Regras de decisão pré-especificadas

Todas a serem fixadas na M12 antes de qualquer coleta.

### RD1 — O colapso existe neste contexto?

> Declara-se colapso se a mediana de `ln VR` entre células for **menor que zero**, com intervalo de bootstrap de 95% sobre réplicas excluindo zero.

Falsificável: se `ln VR ≈ 0`, não há colapso em consumo brasileiro e o T2 vira um resultado nulo informativo — a literatura de opinião política não se transfere para consumo.

### RD2 — O colapso é estruturado? (a refutação a Boelaert et al.)

Regressão do erro sobre as medidas de distância da M04, com controles da M05:

```
E(s) = β₀ + β₁·D1′(s) + β₂·D3(s) + β₃·Dd(s) + γ·Controles(s) + ε
```

> Declara-se estrutura se **β₁ for significativo** sob erro padrão robusto agrupado por estrato **e** o sinal for o predito (erro cresce com a distância) **e** a relação se mantiver ao trocar `E` entre M1, M2 e M3.

O terceiro requisito é deliberadamente duro: um efeito que aparece só em uma das três métricas é ruído de especificação.

Falsificável: `β₁` nulo confirma Boelaert et al. e o T2 vira uma replicação em novo domínio — publicável, mas muito mais fraca. **Este é o risco central do projeto e precisa estar declarado.**

### RD3 — Qual noção de distância prevê melhor? (RQ2 da M04)

> Comparação por `R²` ajustado e por validação cruzada *leave-one-stratum-out* entre modelos com D1′, D3 e Dd isoladamente. Reporta-se a ordenação, não apenas a vencedora.

### RD4 — Há interação complexidade × periferia? (hipótese da M02)

```
E(s,q) = … + β₄·[ D1′(s) × Complexidade(q) ] + …
```

com `Complexidade(q)` operacionalizada pela hierarquia de construtos de Ku et al. (ver M04) ou por uma ordenação simples: participação de mercado < frequência < escolha < disposição a pagar.

> Declara-se interação se **β₄ for significativo e positivo**.

### RD5 — O split KNOWS/DOES varia com a periferia? (H3 da M03)

> Declara-se se a diferença `TV(P4) − TV(P1)` — o ganho do caminho *describe* sobre a agregação — **crescer com a distância**, com `β` significativo.

Interpretação, se confirmada: o modelo descreve melhor do que amostra em todo lugar, e a vantagem é maior justamente onde ele sabe menos. Interpretação, se invertida: o modelo nem sabe descrever o estrato periférico, o que é um achado mais grave e mais interessante.

### RD6 — Qual o dano prático?

> Reportar `Cobertura(k)` para `k ∈ {10, 50, 100, 500, 1000}` e `ESS` mediano por nível de agregação (L1 a L4 da M05). Sem teste; são as quantidades gerenciais.

---

## 6. O que a verificação de Boelaert et al. permite afirmar

**Referência agora totalmente verificada:** BOELAERT, Julien; COAVOUX, Samuel; OLLION, Étienne; PETEV, Ivaylo; PRÄG, Patrick. *Machine Bias. How Do Generative Language Models Answer Opinion Polls?* **Sociological Methods & Research**, v. 54, n. 3, p. 1156–1196, agosto de 2025. DOI 10.1177/00491241251330582. Materiais de replicação em **osf.io/yzect**.

Do abstract verificado: modelos *"cannot replace research subjects for opinion or attitudinal research"*; exibem *"a strong bias and a low variance on each topic"*; e o termo **machine bias** designa o padrão em que esse viés *"randomly varies from one topic to the next"*.

**A abertura para o T2, agora precisa.** A afirmação de aleatoriedade deles é sobre **variação entre tópicos**. O T2 pergunta sobre **estrutura entre estratos**, com o tópico fixo. São eixos ortogonais: é perfeitamente coerente que o viés varie de forma imprevisível de tópico para tópico **e** que, dentro de um tópico, ele decaia de forma previsível ao longo dos estratos. Boelaert et al. mediram o primeiro eixo e não o segundo.

Isso precisa estar escrito em duas frases na introdução do T2, porque é a diferença entre "replicação" e "contribuição". E o RD2 é o teste que a decide.

**Os materiais de replicação no OSF são a maior alavanca disponível.** Se contiverem as distribuições por subpopulação, o T2 pode testar RD2 **nos dados deles** antes de coletar qualquer coisa — o que seria uma validação de conceito de custo praticamente zero e transformaria o risco central do projeto em risco conhecido.

---

## Pendências geradas

- [ ] **Prioridade máxima:** acessar manualmente **osf.io/yzect** e verificar se os dados por subpopulação estão publicados. Tentativa por API falhou nesta missão. Se estiverem, rodar RD2 sobre os dados de Boelaert et al. antes de qualquer coleta própria.
- [ ] Obter o PDF de Boelaert et al. pelo acesso institucional da FGV — o abstract sustenta o argumento, mas o desenho exato ainda não foi lido.
- [ ] Definir a ordenação operacional de `Complexidade(q)` para RD4.
- [ ] Fixar as faixas de discretização para desfechos contínuos, exigidas por M2.
- [ ] **M09** herda a especificação da forma funcional de `f(distância)` e o teste de não-linearidade.
- [ ] **M10** muda de natureza: poder sobre número de réplicas e de estratos, não sobre número de respostas.
- [ ] Verificar se Heath e Alexander disponibilizaram código de cálculo de KL e do parâmetro global de temperatura no Zenodo (DOI 10.5281/zenodo.21706514, registrado na M03) — reaproveitar em vez de reimplementar.
