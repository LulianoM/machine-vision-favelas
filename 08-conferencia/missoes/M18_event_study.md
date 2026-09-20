# M18 — Event study: unidade, tratamento, efeitos fixos, janela e tendências paralelas

Executada em 2026-08-21.

---

## Resumo do que esta missão muda

1. **⚠️ O event study provavelmente não é o desenho certo, e o motivo é aritmético.** Um estudo de evento exige período **anterior** ao tratamento. A M16 estabeleceu que o dado só passa a existir na instrumentação. Em 2026, **todos os estúdios candidatos já adotaram IA generativa** — logo não há período pré-tratamento, não há coorte nunca tratada, e não há adoção escalonada a explorar.

2. **A saída é melhor que o problema: desenho de encorajamento aleatorizado embutido no produto.** Se o Argos Core é seu, a aleatorização é uma decisão de engenharia, não um favor pedido a terceiros. Isso troca identificação frágil por identificação forte, e alinha o T3 com o padrão de Dell'Acqua et al. — que é o que a AIM premia.

3. **E se o event study for mesmo usado, TWFE está morto.** Baker, Larcker e Wang mostram que corrigir o viés de adoção escalonada muda os resultados com frequência, e que *"in many cases, the reported effects in prior research become indistinguishable from zero"*. Um paper com TWFE de dois períodos e adoção escalonada é rejeitado na AIM sem discussão.

---

## 1. O problema de identificação, em ordem

### O que um event study exigiria

| Requisito | Situação do T3 |
|---|---|
| Período pré-tratamento observado | ❌ Dado começa na instrumentação |
| Variação na data de adoção entre unidades | ❌ Todos adotaram antes |
| Coorte nunca tratada, ou ao menos não-ainda-tratada | ❌ Improvável em 2027–2028 |
| Unidades suficientes para agrupar erro | ⚠️ 8 a 15 estúdios é pouco |

**Três dos quatro requisitos falham.** Insistir no event study de adoção de IA seria estimar um efeito que o dado não contém.

### O que ainda pode ser tratado como evento

A adoção de IA generativa já aconteceu, mas **eventos menores continuam acontecendo**, e alguns são plausivelmente exógenos ao estúdio:

| Evento candidato | Exogeneidade | Frequência |
|---|---|---|
| Estúdio adota **uma ferramenta nova** (troca de modelo, nova suíte) | Média — decisão do estúdio, mas por motivo externo (preço, disponibilidade) | Alta |
| **Atualização ou depreciação de modelo** pelo fornecedor | **Alta** — ninguém no estúdio decide | Alta em 2026–2028 |
| **Mudança de preço** ou de limite de uso do fornecedor | **Alta** | Média |
| **Cliente proíbe** uso de IA em contrato | **Alta**, e trata só parte do portfólio | Baixa, mas cresce |
| Contratação ou saída de pessoa | Baixa | Média |

**Os três primeiros são os interessantes**, porque a decisão é do fornecedor e não do estúdio. Uma depreciação de modelo é um choque de tratamento genuinamente externo, atinge todos os estúdios que usavam aquele modelo, e a data é pública.

> **Reformulação viável do event study:** em vez de "adoção de IA", o evento é **troca ou depreciação de modelo**, que produz variação intra-estúdio e entre-estúdios sem depender de decisão endógena.

---

## 2. A recomendação: encorajamento aleatorizado no produto

O ativo que o T3 tem e Dell'Acqua et al. não tinham: **controle sobre o instrumento**.

### Desenho

Dentro dos estúdios participantes, para tarefas de tipos elegíveis:

```
Ao criar a tarefa, o sistema sorteia (estratificado por estúdio, tipo e período):

  Braço A — sem encorajamento     (a ferramenta de IA fica disponível, mas não é sugerida)
  Braço B — com encorajamento     (sugestão ativa de usar IA, com atalho no fluxo)
```

**Não se proíbe nada.** É encorajamento, não atribuição de tratamento — o que é eticamente muito mais defensável, dispensa o problema de negar ferramenta a trabalhador, e produz uma **variável instrumental** limpa.

### Por que é superior

| | Event study de adoção | Encorajamento aleatorizado |
|---|---|---|
| Identificação | Frágil, sem pré-período | **Forte, por aleatorização** |
| Precisa de coorte não tratada | Sim | Não |
| Precisa de histórico | Sim | **Não — começa a valer no dia 1** |
| Ética | Observacional | Requer CEP, mas é minimamente invasivo |
| Padrão da AIM | Aceitável | **É o que a sala premia** |
| Custo | Zero de engenharia | Baixo — um sorteio e uma sugestão de interface |

E resolve o problema que a M16 criou: **não é preciso esperar 18 meses de série histórica.** O relógio começa quando o sorteio entra em produção.

### O estimador

Encorajamento é instrumento; uso efetivo é o tratamento. Estimativa por **dois estágios**, com o efeito local sobre os *compliers*:

```
1º estágio:   ai_usage_it  = π·Z_it + α_i + δ_t + ν_it
2º estágio:   Y_it         = β·ai_usage_it_hat + α_i + δ_t + ε_it
```

com `Z` o sorteio de encorajamento. Reportar também a forma reduzida — efeito do encorajamento direto sobre o desfecho —, que é válida mesmo se a primeira etapa for fraca.

**Diagnóstico obrigatório:** força da primeira etapa. Se o encorajamento move pouco o uso efetivo, a estimativa de dois estágios é inútil e só a forma reduzida sobrevive. **Pré-registrar o limiar.**

---

## 3. Se o event study for usado: especificação completa

Para o caso de troca ou depreciação de modelo, ou como análise secundária.

### Unidades e desfechos — são dois estudos, não um

| Desfecho | Unidade | Agrupamento |
|---|---|---|
| **Homogeneização** (M14) | Artefato | Estúdio × período |
| **Retrabalho** (M15) | Tarefa | Estúdio × período |
| Tempo de ciclo | Tarefa | Estúdio × período |

A homogeneização é intrinsecamente **de grupo**: uma peça só é "similar" em relação a um conjunto. O retrabalho é **de tarefa**. Misturá-los numa especificação só é erro.

### Estimador

**Não usar TWFE com adoção escalonada.** Usar, em ordem de preferência:

| Estimador | Por quê |
|---|---|
| **Callaway e Sant'Anna (2021)** | ATT(g,t) por coorte e período, usando só comparações limpas — controle não tratado nos dois períodos. Admite **não-ainda-tratados** como controle, que é a única saída quando não há nunca-tratados |
| Sun e Abraham (2021) | Extensão dinâmica; estimador de interação ponderada |
| Borusyak, Jaravel e Spiess | Estimador de imputação |
| de Chaisemartin e D'Haultfœuille | Alternativa robusta |
| **Goodman-Bacon (2021)** | Não é estimador — é o **diagnóstico** que decompõe o TWFE e mostra os pesos negativos. Rodar e reportar |

> ⚠️ Anos confirmados por levantamento; **venues não verificados diretamente** nesta missão. Confirmar antes de citar.

**A capacidade de usar não-ainda-tratados como controle é o que salva o desenho**, dado que uma coorte nunca tratada é implausível.

### Efeitos fixos

```
α_estúdio        nível do estúdio
α_período        choques comuns (calendário, sazonalidade de agência)
α_tipo_tarefa    heterogeneidade de formato (M14)
α_trabalhador    onde o N permitir — é a linha de base individual análoga à de Dell'Acqua (M15)
```

**Não incluir efeito fixo de cliente junto do desfecho de homogeneização.** O desfecho é definido *entre* clientes; absorver cliente absorve parte do objeto.

### Janela

| Parâmetro | Proposta |
|---|---|
| Pré-evento | 3 períodos (trimestres), mínimo 2 |
| Pós-evento | 4 períodos |
| Período de referência | **−1**, declarado |
| Empilhamento | Balancear a janela; reportar quantas unidades sobrevivem a cada horizonte |

**Reportar a composição da amostra por horizonte de evento.** Efeito que aparece só em horizonte +4, onde restam três estúdios, é composição, não efeito.

### Erro padrão

Com 8 a 15 estúdios, o agrupamento assintótico é anticonservador. **Bootstrap selvagem agrupado por estúdio**, 9.999 réplicas — mesma decisão da M09 para o T2.

---

## 4. Tendências paralelas: não testar, limitar

A prática de "rodar o pré-teste, não rejeitar, seguir em frente" está desacreditada — pré-testes têm baixo poder, e não rejeitar não é evidência de tendências paralelas.

**Abordagem moderna:** RAMBACHAN, Ashesh; ROTH, Jonathan. *A More Credible Approach to Parallel Trends*. **Review of Economic Studies**. Pacote `HonestDiD` em R, no CRAN e no GitHub.

A ideia: **não exigir que tendências paralelas valham exatamente.** Permite-se que o contrafactual não tratado derive após o tratamento, com desvio limitado pelo maior desvio pré-tratamento observado. O parâmetro `M` governa a restrição de magnitude relativa: `M = 0` impõe tendências paralelas exatas; `M = 1` admite violação tão grande quanto o maior desvio pré observado.

**O que reportar:** o **intervalo de confiança em função de `M`**, e o valor de `M` em que o efeito deixa de ser distinguível de zero — a *quebra*. Isso substitui o pré-teste por uma afirmação honesta: *"o achado sobrevive a violações de tendências paralelas de até X vezes o maior desvio pré-tratamento observado."*

É mais defensável, mais informativo, e é o que um econometrista na plateia da AIM espera ver em 2027.

---

## 5. A advertência de Baker, Larcker e Wang

**Referência:** BAKER, Andrew C.; LARCKER, David F.; WANG, Charles C. Y. *How Much Should We Trust Staggered Difference-In-Differences Estimates?* Harvard Business School Working Paper 21-112, 2021. Stanford GSB e HBS. ⚠️ Há versão publicada em periódico; **não verificada** nesta missão.

Do resumo: aplicam os métodos recentes a resultados previamente publicados e encontram que a correção do viés de adoção escalonada frequentemente muda a estimativa — *"In many cases, the reported effects in prior research become indistinguishable from zero."*

**Uso no T3:** citar na seção de método como justificativa de não usar TWFE. É a referência que a plateia de contabilidade e finanças da AIM reconhece imediatamente.

---

## 6. O que isso muda no cronograma do T3

| | Antes desta missão | Depois |
|---|---|---|
| Desenho principal | Event study com adoção escalonada | **Encorajamento aleatorizado embutido no produto** |
| Event study | Principal | **Secundário**, sobre troca ou depreciação de modelo |
| Espera necessária | 18 meses de série | **Começa quando o sorteio entra em produção** |
| Dependência de terceiros | Alta | Média — precisa de estúdios usando, não doando |
| Bloqueio ético | Menor | **CEP obrigatório e mais rigoroso** — há intervenção |

O item 3 é o ganho relevante: o desenho aleatorizado **não precisa de histórico**, o que neutraliza o achado da M16.

E o item 5 é o custo: um desenho com intervenção exige protocolo de CEP mais cuidadoso que um observacional. **Reforça a urgência da submissão ao CEP registrada na M17.**

---

## Pendências geradas

- [ ] **Decidir entre encorajamento aleatorizado e event study.** Recomendação forte pelo primeiro. Afeta M19, M20 e todo o bloco B.
- [ ] Verificar venues e anos de Callaway e Sant'Anna, Sun e Abraham, Goodman-Bacon, Borusyak et al. e de Chaisemartin e D'Haultfœuille antes de citar.
- [ ] Confirmar a publicação em periódico de Baker, Larcker e Wang.
- [ ] Confirmar volume, número e ano de Rambachan e Roth na *Review of Economic Studies*.
- [ ] Especificar o sorteio: unidade de aleatorização (tarefa, projeto ou semana-trabalhador), estratificação e semente registrada.
- [ ] Definir o limiar de força da primeira etapa e pré-registrá-lo.
- [ ] Levantar o calendário público de depreciações de modelo dos principais fornecedores — é a fonte de eventos exógenos do desenho secundário.
- [ ] **M17 herda:** o protocolo de CEP passa a ser de pesquisa com intervenção, não observacional.
- [ ] **M19 herda:** as ameaças mudam — sai endogeneidade da adoção, entra não-conformidade e efeito de contaminação entre braços dentro do mesmo estúdio.
