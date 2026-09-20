# M30 — O modelo mediado duplo e o estimador

Executada em 2026-08-21. Fecha a parte analítica do Bloco D.

---

## Resumo do que esta missão muda

1. **⚠️ Ameaça grave e específica: mediação em corte transversal é enviesada.** Maxwell e Cole mostram que a análise transversal **pode indicar efeito indireto substancial mesmo quando o verdadeiro efeito indireto longitudinal é zero**. A Parte 1 do T4, como estava, não pode reivindicar mediação.

2. **A mediação migra para o experimento**, onde a exposição é aleatorizada e a precedência temporal é garantida por construção.

3. **⚠️ Mas nem no experimento a mediação está identificada**, porque só X é sorteado — o mediador não é. A saída é **análise de mediação causal com análise de sensibilidade**, que reporta **quanto de confundimento não medido seria necessário para anular o efeito indireto**.

4. **É a mesma jogada epistêmica da M18.** Lá, o HonestDiD substituiu "testar tendências paralelas" por "limitar a violação". Aqui, a sensibilidade substitui "assumir ignorabilidade sequencial" por "reportar o quanto ela precisaria estar errada". **O dossiê passa a ter uma postura metodológica coerente: não assumir o inverificável, e sim limitá-lo.**

5. **A predição contraintuitiva que dá o retorno teórico da dissertação:** **mais autonomia de agendamento pode aumentar a autocobrança**, porque a fronteira passa a ser sua para estabelecer.

---

## 1. A ameaça: mediação transversal

**Referência verificada:** MAXWELL, Scott E.; COLE, David A. *Bias in cross-sectional analyses of longitudinal mediation*. **Psychological Methods**, v. 12, p. 23–44, 2007. Extensão para mediação parcial em *Bias in Cross-Sectional Analyses of Longitudinal Mediation: Partial and Complete Mediation Under an Autoregressive Model*, **Multivariate Behavioral Research**, 2011 ⚠️ [volume e páginas não verificados].

O argumento: mediação é **processo causal que se desenrola no tempo**, e a maior parte dos testes empíricos usa dado transversal. O resultado de 2007 mostrava viés substancial no caso de mediação completa; a extensão de 2011 mostra que:

> **A análise transversal pode implicar a existência de um efeito indireto substancial mesmo quando o verdadeiro efeito indireto longitudinal é zero.** Uma variável que aparece como forte mediadora em análise transversal pode não ser mediadora nenhuma numa análise longitudinal.

### Consequência direta para o T4

| Parte | O que pode reivindicar |
|---|---|
| **Parte 1** — survey transversal | **Associação. Não mediação.** Reportar correlações e o modelo de medida; descrever o padrão como consistente ou inconsistente com a hipótese, sem linguagem causal |
| **Parte 2** — experimento de vinheta | **Efeito causal de X** sobre mediadores e desfecho. Mediação **sob sensibilidade declarada** |

Isso não empobrece o T4 — **corrige uma reivindicação que não se sustentaria em arguição.** É exatamente o tipo de coisa que um metodologista na banca ou um revisor da AIM levanta.

---

## 2. O modelo, no experimento

### Estrutura

```
        ┌─────────────── caminho da AUTONOMIA ───────────────┐
        │                                                     │
   X ───┼──►  M1  autonomia de MÉTODO        (↓)  ──────────►│
(prescri│                                                     ├──► Y
 ção de │──►  M2  autonomia de AGENDAMENTO   (↑)  ──────────►│  autocobrança
 método)│                                                     │  (excesso de
        │                                                     │  comprometimento)
        └─────────────── caminho do PARADOXO ────────────────┤
                                                              │
   X ──────►  M3  AUTOEFICÁCIA        (augmentação, ↑) ──────►│
   X ──────►  M4  INSEGURANÇA         (automação,   ↑) ──────►│
```

Moderadores medidos: vínculo de trabalho, complexidade da tarefa, dependência de renda, tempo de uso de IA. Fator entre sujeitos: opacidade.

### As hipóteses de caminho

| # | Caminho | Sinal predito |
|---|---|---|
| P1 | X → M1 (método) | **negativo** |
| P2 | X → M2 (agendamento) | **positivo** — a troca (M28) |
| P3 | M1 → Y | negativo (menos autonomia de método, mais autocobrança) |
| **P4** | **M2 → Y** | **positivo** ⭐ |
| P5 | X → M3 (autoeficácia) | positivo |
| P6 | X → M4 (insegurança) | positivo |
| P7 | M4 → Y | positivo |
| P8 | M3 → Y | ambíguo — sem predição declarada |

### ⭐ P4 é a hipótese que vale o trabalho

Predição contraintuitiva: **ganhar autonomia de agendamento aumenta a autocobrança**.

O raciocínio, e é o núcleo teórico da dissertação: quando o sistema define o prazo, a fronteira entre trabalho e não-trabalho é **externa e contestável**. Quando o trabalhador define, a fronteira passa a ser dele — e a cobrança por atravessá-la também. É a "autonomia controlada, geradora de dependência psíquica" de Gaulejac, e o sujeito de desempenho de Han, escritos como coeficiente.

**Se P2 e P4 forem ambos positivos, o T4 mostra que a flexibilidade concedida é o mecanismo da autocobrança, não o seu alívio.** Isso é resultado, não confirmação de senso comum — e é o que separa este paper de mais um estudo dizendo que IA reduz autonomia.

⚠️ **Nota de atribuição, pendência da M28:** este modelo é **construção própria do T4**, informada pelo enquadramento de Raisch e Krakowski. Não é o modelo deles, que é ensaio de revisão no nível organizacional sem proposições formais. Escrever assim, explicitamente.

---

## 3. A identificação — e o que ela não cobre

Num experimento, o sorteio de X identifica:

| Caminho | Identificado por aleatorização? |
|---|---|
| X → M | ✅ Sim |
| X → Y (efeito total) | ✅ Sim |
| **M → Y** | ❌ **Não.** O mediador não é sorteado |
| Efeito indireto | ❌ Requer **ignorabilidade sequencial**, que é **inverificável** |

### O tratamento

**Referência verificada:** IMAI, Kosuke; KEELE, Luke; TINGLEY, Dustin (e YAMAMOTO, Teppei em trabalhos correlatos). Análise de mediação causal, com o pacote **`mediation`** em R. A abordagem estabelece que a análise padrão de mediação se justifica sob **ignorabilidade sequencial**, condição sob a qual o **efeito causal médio de mediação (ACME)** é identificado não-parametricamente.

E, porque a ignorabilidade sequencial **não é testável**:

> A análise de sensibilidade **mede a robustez do ACME a confundimento não medido entre mediador e desfecho.**

**O que reportar:** o valor do parâmetro de sensibilidade — tipicamente a correlação entre os erros das equações do mediador e do desfecho — **no qual o efeito indireto cruza zero**. Vira uma afirmação honesta: *"o efeito de mediação sobrevive a confundimento mediador-desfecho de até ρ = X."*

### A coerência metodológica do dossiê

Vale registrar, porque é argumento de qualidade:

| Missão | Problema | Solução adotada |
|---|---|---|
| M18 | Tendências paralelas são inverificáveis | **HonestDiD**: limitar a violação, reportar o ponto de quebra |
| M07 | Incerteza amostral não existe em LLM | Bootstrap **entre réplicas**, não entre chamadas |
| **M30** | Ignorabilidade sequencial é inverificável | **Sensibilidade**: reportar quanto de confundimento anularia o efeito |

**Três problemas diferentes, a mesma postura: não assumir o inverificável — limitá-lo e mostrar a fronteira.** Isso deve estar dito em uma frase na seção de método, porque um revisor atento reconhece a consistência.

---

## 4. Estimadores

### Modelo de medida — a AFC das escalas

Itens Likert de 5 pontos são **ordinais**, não contínuos.

| Situação | Estimador |
|---|---|
| AFC das cinco escalas (M27) | **WLSMV** — apropriado a indicadores ordinais |
| Modelo estrutural | **MLR** (máxima verossimilhança robusta), tolerante a não-normalidade |
| Robustez | Reportar **ambos** e mostrar que as conclusões não dependem da escolha |

Também obrigatório: **invariância de medida** entre subgrupos usados como moderadores — sem invariância, comparar coeficientes entre vínculos de trabalho é comparar réguas diferentes.

### Experimento — medidas repetidas

Como na M29: multinível com intercepto aleatório por respondente, erro padrão agrupado por respondente. A mediação causal roda **dentro** dessa estrutura, com bootstrap para os intervalos.

### Efeitos indiretos

**Bootstrap percentílico com viés corrigido, 10.000 reamostragens**, reamostrando **respondentes**, não observações — o aninhamento manda.

---

## 5. O tamanho da amostra

O N é governado por **três exigências simultâneas**, e vale o maior.

| Exigência | Requisito |
|---|---|
| **AFC de cinco escalas** | Wolf, Harrington, Clark e Miller (2013) mostram por simulação de Monte Carlo que o mais relevante não é a razão N:q, e sim o N absoluto (**acima de 200 a 400**) e a magnitude das cargas. E que **mais indicadores por fator reduz o N necessário**, não aumenta |
| **Modelo estrutural com efeitos indiretos** | Efeitos indiretos são produtos de coeficientes; exigem mais N que efeitos diretos. Faixa de **400 a 500** |
| **Experimento multinível** | Poder vem do número de **respondentes**, com 8 observações cada |

> **Recomendação: N = 500 respondentes completos.**

Atende às três com margem, permite subgrupos de moderação com células viáveis, e absorve exclusões por falha em checagem de atenção.

**Meta de campo: 650 iniciados**, prevendo abandono num questionário longo.

⚠️ **E há a razão de custo:** os itens de checagem de manipulação, as duas partes e as cinco escalas produzem um questionário que a M29 já sinalizou como longo demais. **Com N = 500 e questionário de 20 minutos, painel pago é a via realista**, e isso é linha de orçamento — como a API de SERP é para o T1.

### A alternativa, se o orçamento não permitir

**Separar as amostras.** Parte 1 com uma amostra, Parte 2 com outra. Perde-se a ligação intra-sujeito entre trabalho real e resposta a cenário — que é informativa, mas **não é necessária a nenhuma das hipóteses confirmatórias**. Corta o questionário pela metade e reduz o abandono.

**Recomendação: manter amostra única se o orçamento permitir; separar sem culpa se não permitir.**

---

## Pendências geradas

- [ ] Verificar volume e páginas da extensão de 2011 de Maxwell e Cole em *Multivariate Behavioral Research*.
- [ ] Verificar a referência canônica de Imai, Keele, Tingley e Yamamoto — provavelmente *American Political Science Review* e *Psychological Methods* ⚠️ [não verificadas].
- [ ] Confirmar venue de Wolf, Harrington, Clark e Miller (2013) — provavelmente *Educational and Psychological Measurement* ⚠️ [não verificado].
- [ ] Rodar **simulação de Monte Carlo** do modelo estrutural específico do T4 para substituir a regra de bolso por número próprio.
- [ ] Orçar painel pago com 500 completos no perfil de profissionais de marketing no Brasil.
- [ ] Decidir amostra única contra amostras separadas, à luz do orçamento.
- [ ] **M31 herda:** a Parte 1 não reivindica mediação, o que muda o que o capítulo quantitativo da dissertação pode afirmar.
- [ ] **M32 herda:** o pré-registro precisa declarar P4 como predição contraintuitiva a priori, e P8 como sem predição.
