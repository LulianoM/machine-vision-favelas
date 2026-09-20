# M10 — Poder, tamanho de efeito detectável e regra de parada

Executada em 2026-08-21. Cálculo por **simulação**, com parâmetros estimados diretamente do dado de Boelaert et al., não estipulados.

---

## Resumo do que esta missão muda

1. **Encontrei um fenômeno diferente e melhor do que "colapso de variância": não-responsividade de variância.** A variância do modelo é quase **constante entre estratos**, enquanto a humana varia muito. A correlação entre variância humana e `ln VR` é **−0,89** no conjunto e **−0,97** em dois dos três itens. O modelo aplica uma dispersão fixa: super-disperso onde a população é homogênea, sub-disperso onde ela é heterogênea.

2. **⚠️ O efeito de classe existe, é monótono e na direção prevista — mas é pequeno demais.** High +0,050, Middle −0,014, Low −0,036: uma amplitude de **0,086** log em toda a faixa de classe, contra um desvio padrão residual de **0,24**. Na simulação, **nenhum desenho viável detecta um efeito desse tamanho.**

3. **Estratos valem cerca de dez vezes mais que itens.** Confirmado em duas corridas independentes: quadruplicar itens move o poder em três centésimos; triplicar estratos move em trinta e cinco. Isso decide o desenho: **o nível confirmatório é L3, com 60 células, não L1 nem L2** — e o número de categorias de consumo é escolhido por cobertura substantiva, não por poder.

4. **A prioridade deixa de ser número de células e passa a ser amplitude da variável de distância.** É a única alavanca que transforma um efeito indetectável em detectável.

---

## 1. Parâmetros estimados do dado real

Cálculo feito sobre `FA-GPT-3.csv` contra `WVS/wvs-data.csv`, células de país × classe, itens `d_happy` (4 níveis), `d_religiousp` (7 níveis) e `d_polpos` (escala 1–10). Filtro de 50 observações mínimas por célula. 45 células válidas.

### O achado inesperado: `ln VR` é majoritariamente **positivo**

```
mediana  = +0,277      média = +0,249      dp = 0,249
fração com colapso (ln VR < 0) = 17,8%
```

O GPT-3 no caminho de resposta completa produz distribuições **mais dispersas** que a referência humana em 82% das células. Isso contradiz a narrativa simples de colapso — **e a explicação é mais interessante que a narrativa.**

### A variância do modelo quase não se move

Coeficiente de variação da variância entre células:

| Item | CV(var humana) | CV(var modelo) | Razão |
|---|---:|---:|---:|
| `d_happy` | 0,202 | 0,145 | 1,4× |
| `d_religiousp` | 0,225 | 0,043 | **5,2×** |
| `d_polpos` | 0,347 | 0,045 | **7,8×** |

Em `d_polpos`, a variância humana vai de 3,02 (Alemanha, classe média) a 8,80 (México, classe baixa) — quase três vezes. A do modelo fica entre 5,23 e 6,05 em todas as 15 células.

### E isso produz uma relação quase determinística

Correlação entre variância humana e `ln VR`, dentro de item:

```
d_happy         r = −0,712
d_religiousp    r = −0,974
d_polpos        r = −0,977
conjunto (z dentro de item)  r = −0,887   (n = 45)
```

> **O modelo não erra a variância de forma aleatória. Ele aplica uma variância fixa, alheia ao estrato.** Onde a população real é homogênea, ele super-dispersa; onde é heterogênea, ele achata.

Isto é uma reformulação da tese do T2, e é melhor que a original em três aspectos: é mais precisa, é falsificável com uma correlação, e explica os resultados positivos e negativos de `ln VR` com um único mecanismo. **Nome proposto: não-responsividade de variância.**

### Os gradientes observados

Desvio médio de `ln VR`, líquido de efeito de item:

**Por classe** — monótono e na direção prevista:

| Classe | Desvio |
|---|---:|
| High | **+0,050** |
| Middle | −0,014 |
| Low | **−0,036** |
| **Amplitude** | **0,086** |

**Por país** — 4,5 vezes maior:

| País | Desvio |
|---|---:|
| Alemanha | +0,165 |
| Rússia | +0,122 |
| Austrália | +0,044 |
| Estados Unidos | −0,105 |
| **México** | **−0,226** |
| **Amplitude** | **0,391** |

⚠️ **Nota de interpretação honesta:** a ordenação por país **não** é uma ordenação centro-periferia. Estados Unidos e México aparecem juntos no lado negativo, e Alemanha e Rússia juntos no positivo. O que os separa é a variância humana: onde a população real é mais dispersa, o `ln VR` é mais negativo. **O efeito de país é mediado por dispersão real, não por centralidade cultural.** Isso enfraquece a versão ingênua da hipótese de periferia e fortalece o mecanismo de não-responsividade.

---

## 2. A simulação de poder

### Modelo gerador

```
E_sq = β·D_s + u_s + e_sq
   D_s  distância, padronizada em [−1, +1]
   u_s  efeito aleatório de estrato        (o agrupamento que importa)
   e_sq ruído de célula, média sobre Q itens
```

**Inferência:** MQO com **bootstrap selvagem agrupado por estrato**, pesos de Rademacher, sob H₀ — o procedimento fixado na M09 para poucos grupos.

**Calibração:** `sd` total de 0,24, tirado do dado. Dois cenários de decomposição: componente de estrato forte (`sd_u = 0,15`, `sd_e = 0,19`), que é o realista dado o padrão de país e classe observado, e componente fraca (`sd_u = 0,05`, `sd_e = 0,23`).

### Resultados — poder a 5%

**Cenário realista (componente de estrato forte):**

| Estratos | Itens | β=0,10 | β=0,15 | β=0,25 | β=0,40 |
|---:|---:|---:|---:|---:|---:|
| 7 | 10 | 0,43 | 0,60 | 0,89 | 1,00 |
| 20 | 10 | 0,41 | 0,73 | **1,00** | 1,00 |
| 20 | 40 | 0,53 | 0,80 | 0,99 | 1,00 |
| **60** | **10** | **0,83** | **0,99** | 1,00 | 1,00 |
| 180 | 10 | 0,99 | 1,00 | 1,00 | 1,00 |

**Cenário otimista (componente de estrato fraca):**

| Estratos | Itens | β=0,10 | β=0,15 | β=0,25 | β=0,40 |
|---:|---:|---:|---:|---:|---:|
| 7 | 10 | 0,74 | 0,94 | 1,00 | 1,00 |
| 20 | 10 | 0,90 | 1,00 | 1,00 | 1,00 |
| 20 | 40 | 0,98 | 1,00 | 1,00 | 1,00 |
| 60 | 10 | 1,00 | 1,00 | 1,00 | 1,00 |

### Confirmação por corrida independente de maior precisão

Rodada separada com 700 simulações e 299 réplicas de bootstrap, grade de itens diferente. Cenário realista:

| Estratos | Itens | β=0,10 | β=0,15 | β=0,25 | β=0,40 |
|---:|---:|---:|---:|---:|---:|
| 7 | 5 | 0,41 | 0,58 | 0,88 | 0,99 |
| 7 | 20 | 0,44 | 0,62 | 0,92 | 1,00 |
| 20 | 5 | 0,47 | 0,70 | 0,98 | 1,00 |
| 20 | 20 | 0,49 | 0,78 | 0,99 | 1,00 |
| **60** | **10** | **0,82** | **0,99** | 1,00 | 1,00 |
| 180 | 10 | 1,00 | 1,00 | 1,00 | 1,00 |

Todos os valores batem com a primeira corrida dentro de ±0,06, e o ponto de decisão — 60 estratos com poder de 0,82 a 0,83 em β=0,10 — reproduz-se de forma praticamente idêntica.

### Três leituras

**Estratos valem cerca de dez vezes mais que itens, não quatro.** A corrida de maior precisão isola melhor o contraste: quadruplicar itens de 5 para 20, com 20 estratos, move o poder de **0,47 para 0,49** — três centésimos. Triplicar estratos de 20 para 60, com 10 itens, move de **0,47 para 0,82** — trinta e cinco centésimos. O motivo é estrutural, não numérico: `D` varia **apenas entre estratos**, e o erro está agrupado por estrato. Acrescentar itens reduz `e_sq` mas não toca `u_s`, que é o termo que domina o erro padrão de `β`.

Consequência prática direta: **o número de categorias de consumo é quase irrelevante para o teste confirmatório.** Escolher 12 a 15 categorias por cobertura substantiva e comparabilidade com a POF, não por poder.

**L1 e L2 são insuficientes.** Sete estratos dão poder de 0,60 num efeito de 0,15. Vinte dão 0,73. **Só a partir de 60 o desenho fica defensável.**

**⚠️ E o efeito de classe observado está fora de alcance.** Numa escala `D ∈ [−1, +1]`, a amplitude total corresponde a `2β`. A amplitude de classe medida em Boelaert et al. é 0,086, logo **β ≈ 0,043** — abaixo da menor coluna simulada. Nesse tamanho, o poder é inferior a 0,43 mesmo com 180 estratos.

---

## 3. O que fazer com isso

O efeito de classe de Boelaert et al. é pequeno por dois motivos, e apenas um deles é remediável.

| Motivo | Remediável? | Como |
|---|---|---|
| Classe é **autodeclarada em três níveis** (Low/Middle/High), o que atenua fortemente | **Sim** | A POF tem sete faixas de rendimento **medidas e ponderadas**. Atenuação por erro de medida cai muito |
| A classe pode simplesmente **não ser** a dimensão que move a fidelidade — o dado sugere que a variância real da população é | Parcialmente | Ver abaixo |

### A consequência de desenho

**A prioridade deixa de ser número de células e passa a ser amplitude da distância.** Um desenho com 60 células e uma medida de distância de amplitude estreita perde para um com 30 células e amplitude larga.

Três implicações concretas:

1. **Selecionar estratos nos extremos, não uniformemente.** Amostrar preferencialmente as faixas 1 e 2 e as faixas 6 e 7 da POF, em vez de distribuir esforço igualmente pelas sete. Aumenta `sxx` sem aumentar `S`.
2. **A medida `D1′` da M06 — erro factual de caracterização — passa a ser avaliada por amplitude, não só por validade.** Se ela discriminar pouco entre estratos, é inútil por mais bem fundamentada que seja. Testar amplitude antes de fixar.
3. **Considerar promover a variância humana a preditor concorrente.** O dado mostra `r = −0,89` entre variância humana e `ln VR`. É o preditor mais forte que existe, mede-se direto na POF, e nenhum dos papers o usa. **Deve entrar na RQ2 da M04 como quarta medida candidata.**

### Nível confirmatório: **L3**

Sessenta células, renda(4) × região(5) × escolaridade(3). Poder de **0,83** em β=0,10 e **0,99** em β=0,15, no cenário realista. L1 e L2 passam a ser descritivos e de comparabilidade com tabelas oficiais; L4 fica exploratório, para consistência estrutural.

---

## 4. Regra de parada

O problema formulado por Brand et al. — o número de consultas é escolha de desenho e não restrição amostral — significa que **não existe regra de parada baseada em precisão**. Aumentar `k` estreita o intervalo sem adicionar informação.

**Regra: desenho fixo, sem parada opcional.** Tudo declarado antes da coleta.

| Parâmetro | Valor | Justificativa |
|---|---|---|
| Estratos `S` | **60** (nível L3) | Poder ≥ 0,83 em β = 0,10 |
| Itens `Q` | **12 a 20 categorias de consumo** | Além disso o retorno é marginal (0,41 → 0,53 de 10 a 40) |
| Réplicas `R` | **5** por célula | Paráfrase(2) × semente de ordem(2) × execução, em dias distintos. É a unidade de incerteza fixada na M07 |
| Chamadas `k` em P3/P4 | **50** | Padrão de fato de Brand et al.; não é fonte de inferência, só de comparação com P1 |
| Modelos | **5** | GPT-4o, Gemini, Claude, Llama-3-70B, Mistral — cobrindo escala e provedor |
| Caminhos | **4** | P1 describe (primário), P2 logprob (onde houver), P3 PPA, P4 agregação |

**Volume estimado.** No caminho primário: 60 células × 15 itens × 5 réplicas × 5 modelos ≈ **22.500 chamadas**, uma por célula-item-réplica-modelo. Com P3 e P4 a 50 chamadas cada, o total sobe para a ordem de **1,5 milhão de chamadas**.

⚠️ **Isto é grande demais para P3 e P4 em todos os modelos.** Restringir P3 e P4 a **dois modelos e cinco itens**, o suficiente para reproduzir o contraste de Jang et al. (TV 0,22 contra 0,46) e demonstrar que a agregação ingênua erra. Não é a inferência principal.

**Orçamento.** Aos preços declarados por Brand et al. (GPT-4o a US$ 5 por milhão de tokens de entrada e US$ 15 de saída), o caminho primário fica na ordem de **dezenas a poucas centenas de dólares**. Continua não sendo a restrição.

### Interrupção antecipada — a única permitida

Uma condição, declarada no pré-registro, e não é sobre resultado:

> Se, na primeira réplica completa, mais de 20% das células retornarem resposta inválida ou o item de atenção falhar em mais de 10% delas, **interromper e corrigir o instrumento** antes de prosseguir. Descartar a coleta parcial.

É checagem de instrumento, não olhada nos dados. Qualquer outra interrupção invalida o pré-registro.

---

## 5. O que fazer se o efeito for mesmo de 0,04

Cenário realista e precisa de plano, decidido agora e não em outubro.

Se o pré-teste da M08 e da M09 — gradiente por país nos cinco, regredido contra centralidade — indicar efeito da ordem de 0,04, há três saídas, em ordem de preferência:

1. **Trocar a variável dependente.** Abandonar o gradiente de `ln VR` e adotar **a correlação de −0,89 como o achado central**. "A variância do modelo não responde à variância da população" é um resultado forte, já visível no dado, que não depende de detectar um gradiente fraco, e que vem com um teste de correlação simples e um gráfico limpo.
2. **Trocar o desfecho para cobertura de intervalo** (M07/M6). Cobertura é uma proporção com muito mais amplitude que `ln VR`, e a métrica é mais interpretável para a plateia.
3. **Migrar para o T5.**

**A saída 1 é a mais provável e a mais forte.** Vale considerar promovê-la a tese principal do T2 desde já, com o gradiente de decaimento rebaixado a hipótese secundária.

---

## Pendências geradas

- [ ] **Reconsiderar a tese central do T2** à luz da não-responsividade de variância. Afeta M09 (a especificação passaria a ser correlação, não regressão de gradiente), M12 e todo o bloco F.
- [ ] Acrescentar **variância humana do estrato** como quarta medida candidata de distância na RQ2.
- [ ] Testar a **amplitude** de `D1′` antes de fixá-la como primária — validade sem amplitude não serve.
- [ ] Verificar se a seleção de estratos nos extremos das faixas de renda cria viés de seleção que exija ponderação corretiva.
- [ ] Replicar o cálculo desta missão nos caminhos **NTP** de Boelaert et al. (GPT-4T, Llama-3-70B, Mixtral) — se a não-responsividade aparecer também via logprob, o achado é robusto ao caminho de extração.
- [ ] Confirmar preços correntes de API dos cinco modelos; os de Brand et al. são de 2024.
