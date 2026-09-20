# M19 — Ameaças à identificação do T3

Executada em 2026-08-21. Registro reconstruído para o desenho de **encorajamento aleatorizado** fixado na M18.

---

## Nota de escopo

A missão foi escrita para um desenho observacional — endogeneidade da adoção, seleção de clientes, mudança de composição. A M18 trocou o desenho por encorajamento aleatorizado. **Duas das três ameaças originais morrem com a aleatorização; a terceira sobrevive; e cinco novas nascem.**

| Ameaça original | Estado |
|---|---|
| Endogeneidade da adoção | **Morta** pela aleatorização — mas ressuscita como heterogeneidade de conformidade (B2) |
| Seleção de clientes | **Viva e agravada** (B6) |
| Mudança de composição | **Viva** (B5) |

---

## Tabela-resumo

| # | Ameaça | Severidade | Mitigação existe? |
|---|---|---|---|
| **B1** | **Contaminação entre braços dentro do estúdio** | 🔴 **Crítica — mata o desenho** | Sim, e custa desenho |
| **B2** | Primeira etapa fraca e conformidade desigual | 🔴 Alta | Parcial |
| **B3** | Efeitos Hawthorne e de demanda | 🟠 Média-alta | Sim |
| **B4** | Deriva de modelo contaminando o desfecho | 🟠 Média-alta | Sim, barata |
| **B5** | Mudança de composição de projetos | 🟠 Média | Sim |
| **B6** | Seleção dos estúdios participantes | 🟡 Média — validade externa | Parcial |
| **B7** | Atrito diferencial | 🟡 Média | Sim |
| **B8** | Instabilidade do desfecho de homogeneização por tamanho de grupo | 🟡 Média | Sim (M14) |

---

## B1 — Contaminação entre braços dentro do estúdio 🔴

**Mecanismo.** Se o sorteio for por tarefa, a **mesma pessoa** recebe encorajamento em algumas tarefas e não em outras. Ela não desaprende. Usa IA nos dois braços, e o braço de controle deixa de ser controle. É violação direta de SUTVA — o desfecho de uma unidade depende da atribuição de outras.

Num estúdio de 5 a 15 pessoas, isso é agravado por proximidade: prompts circulam, atalhos são compartilhados, alguém mostra ao colega.

**Esta é a ameaça que decide o desenho.** Sorteio por tarefa é atraente por dar muitas unidades e é, por isso mesmo, o erro mais provável.

### As opções, e o trade-off

| Unidade de sorteio | Unidades | Contaminação | Serve ao desfecho de homogeneização? |
|---|---|---|---|
| Tarefa | Muitas | 🔴 Quase total — mesma pessoa nos dois braços | Não — o grupo fica misturado |
| **Projeto** | Média | 🟠 Parcial — pessoa pode cruzar projetos | **Sim** — preserva o agrupamento por cliente |
| Trabalhador | Poucas | 🟠 Parcial — colegas conversam | Parcial |
| Estúdio | 8 a 15 | 🟢 Baixa | Sim, mas **poder catastrófico** |
| Estúdio-período (switchback) | Média | 🟢 Baixa | Sim, mas confunde com tempo |

**Recomendação: sorteio no nível do projeto**, estratificado por estúdio, tipo de entrega e período.

Razões: preserva a estrutura de agrupamento que a métrica de homogeneização exige (peças de clientes distintos no mesmo estúdio-período, M14); dá mais unidades que o nível de estúdio; e reduz a contaminação intra-pessoa, porque o contexto do projeto muda.

### Mitigações adicionais, não opcionais

1. **Medir a contaminação em vez de assumir ausência.** Incluir como covariável a **fração dos projetos concomitantes do mesmo trabalhador que estão no braço encorajado**. É um desenho de interferência parcial: se o coeficiente for diferente de zero, há vazamento e ele é quantificado.
2. **Reportar o uso efetivo de IA nos dois braços.** O campo `ai_usage` da M17 torna a contaminação **observável**. Se o braço de controle registrar uso alto, o desenho é reportado como encorajamento marginal, não como comparação com ausência.
3. **Análise por período inicial.** A contaminação tende a crescer no tempo. Estimar separadamente os primeiros períodos, quando o vazamento é menor.

**Risco residual: alto.** Contaminação não se elimina em organização pequena. **Ela se mede e se declara.**

---

## B2 — Primeira etapa fraca e conformidade desigual 🔴

**Mecanismo.** Encorajamento só identifica se move o comportamento. Duas falhas possíveis: quase todos já usam IA e o encorajamento não muda nada (teto), ou o encorajamento é ignorado.

E há a falha mais sutil: **a conformidade é sistematicamente desigual.**

**Referência verificada:** HUMLUM, Anders; VESTERGAARD, Emilie. *The unequal adoption of ChatGPT exacerbates existing inequalities among workers*. **PNAS**, 2025. DOI 10.1073/pnas.2414972121. Levantamento em larga escala ligado a registros administrativos na Dinamarca, **18.000 trabalhadores** em **11 ocupações expostas**.

Achados que importam:

- **Mulheres têm 16 pontos percentuais menos probabilidade** de ter usado a ferramenta no trabalho.
- Trabalhadores mais jovens e menos experientes adotaram mais rápido.
- **Usuários já ganhavam mais antes da chegada do ChatGPT**, mesmo com menor tempo de casa — a ferramenta não nivelou, acompanhou a hierarquia existente.
- Barreiras principais: **restrição do empregador** e **percepção de necessidade de treinamento**.

**Consequência direta:** os *compliers* de um desenho de encorajamento serão desproporcionalmente jovens, homens e de maior remuneração. O efeito local estimado é **o efeito sobre esse grupo**, não sobre o trabalhador médio.

**Mitigações:**

1. **Reportar o perfil dos compliers**, não só o efeito. É honesto e é o que a literatura agora espera.
2. **Pré-registrar o limiar de força da primeira etapa** e a decisão de abandonar a estimativa de dois estágios abaixo dele.
3. **Reportar sempre a forma reduzida** — efeito do encorajamento sobre o desfecho —, que é válida mesmo com primeira etapa fraca.
4. **Estratificar o sorteio por características do trabalhador**, para garantir variação de encorajamento dentro de cada estrato.

**Risco residual: médio.** É gerenciável, mas muda o que o paper pode afirmar.

---

## B3 — Efeitos Hawthorne e de demanda 🟠

**Mecanismo.** São dois, e a distinção importa: **Hawthorne** decorre de o participante **sentir-se observado**, independentemente de entender o objetivo; **demanda** decorre de o participante **inferir o propósito** do experimento e agir conforme o que acredita ser esperado.

No T3, o segundo é o perigoso: se o trabalhador percebe que o estúdio participa de uma pesquisa sobre IA, e que o dono do estúdio é o pesquisador (ver o conflito de interesse da M17), o incentivo a "dar o resultado certo" é real.

**Mitigações:**

1. **Encorajamento como funcionalidade de produto**, não como intervenção de pesquisa. A sugestão de uso de IA é indistinguível de uma melhoria de interface.
2. **Não revelar a hipótese.** A notificação de pesquisa da M17 informa que dados de execução são usados, sem dizer o que se testa.
3. **Hawthorne atinge os dois braços igualmente** e, portanto, não enviesa a comparação — só o nível. Dizer isso explicitamente.
4. **Desfecho de homogeneização é difícil de manipular deliberadamente.** Um trabalhador que quer agradar não sabe como tornar sua peça mais ou menos similar às dos outros clientes. **O desfecho principal é naturalmente resistente à demanda** — vantagem real sobre desfechos autorrelatados.

**Risco residual: baixo para o desfecho principal, médio para tempo de ciclo e retrabalho.**

---

## B4 — Deriva de modelo contaminando o desfecho 🟠

**Mecanismo.** Dois vetores, ambos registrados antes:

- **Do lado do tratamento:** o modelo por trás da ferramenta muda sozinho. Parte da mudança de homogeneização vem do fornecedor, não da adoção (Karouzos et al., M14).
- **Do lado da medida:** se o modelo de embedding usado para calcular similaridade mudar durante a série, a métrica muda de escala e a comparação temporal quebra.

**Mitigações:**

1. **Registrar `ai_tool` e `ai_tool_version` por tarefa** — campo já especificado na M17.
2. **Congelar o modelo de embedding** e sua versão, e recomputar tudo se precisar trocar.
3. **Efeito fixo de período** absorve choques comuns de fornecedor.
4. **Usar depreciações de modelo como evento** no desenho secundário (M18) — transforma a ameaça em fonte de identificação.

**Risco residual: baixo**, e a mitigação é barata. Mas exige disciplina desde o dia um: um embedding recomputado com outro modelo no meio do caminho é irrecuperável.

---

## B5 — Mudança de composição de projetos 🟠

**Mecanismo.** Se o encorajamento alterar **quais** projetos o estúdio aceita, ou **como** os aloca, o conjunto de artefatos muda de composição e a homogeneização medida reflete carteira, não processo.

**Mitigações:**

1. **Sortear depois da entrada do projeto**, nunca antes. O projeto entra, é registrado, e só então recebe braço. Isso torna a composição pré-tratamento independente do sorteio por construção.
2. **Teste de equilíbrio** em características do projeto: orçamento, prazo, setor do cliente, tipo de entrega, tamanho da equipe. Reportar a tabela.
3. **Efeito fixo de tipo de entrega**, e estratificação do sorteio pelo mesmo eixo.
4. **Monitorar a taxa de entrada** de projetos por braço — se divergir, há vazamento para a decisão comercial.

**Risco residual: baixo**, desde que a regra "sortear depois da entrada" seja inviolável.

---

## B6 — Seleção dos estúdios participantes 🟡

**Mecanismo.** Estúdios que adotam um produto de gestão instrumentado e aceitam participar de pesquisa não são estúdios típicos. São mais organizados, mais digitalizados, provavelmente mais jovens. **Ameaça de validade externa, não interna.**

Agravante: o recrutamento passa pela rede da Argos, o que estreita ainda mais.

**Mitigações:**

1. **Caracterizar a amostra** contra alguma referência do setor — número de funcionários, faturamento, tempo de mercado, mix de serviços. Sem referência disponível, declarar a ausência.
2. **Declarar o escopo da inferência**: estúdios pequenos, digitalizados, brasileiros. Não generalizar para agências grandes nem para outros países.
3. **Reportar a taxa de recusa** e, se possível, o que distingue quem recusou.

**Risco residual: irredutível.** É custo de fazer pesquisa de campo com N pequeno. Trata-se declarando, não corrigindo.

---

## B7 — Atrito diferencial 🟡

**Mecanismo.** Estúdios abandonam o produto, ou param de vincular artefatos, ou param de preencher `ai_usage`. Se o abandono correlacionar com o braço ou com o resultado, a amostra final é enviesada.

**Mitigações:**

1. **Monitorar taxa de preenchimento por braço e por período** — é o indicador precoce.
2. **Reportar o fluxo da amostra** no padrão CONSORT: quantos entraram, quantos sortearam, quantos completaram, por braço.
3. **Limites de Lee** ou análise de sensibilidade a atrito, se a diferença entre braços for material.
4. **Análise por intenção de tratar** como principal — quem foi sorteado permanece na análise.

**Risco residual: baixo se monitorado, alto se descoberto tarde.**

---

## B8 — Instabilidade do desfecho por tamanho de grupo 🟡

Herdada da M14. A similaridade ao conjunto depende de quantas peças há no grupo, e o ruído cresce quando o grupo encolhe. Se o tamanho do grupo correlacionar com o braço ou com o período, o ruído fica correlacionado com o tratamento.

**Mitigações**, já fixadas na M14: métrica par a par em vez de centroide; mínimo de 8 peças por estúdio-período; tamanho do grupo como covariável; Vendi Score normalizado por `n` no nível de grupo.

---

## O que muda no desenho por causa desta missão

Três decisões concretas:

1. **A unidade de sorteio é o projeto**, não a tarefa. Decisão tomada aqui, e é a mais importante do bloco B.
2. **A fração de projetos concomitantes encorajados entra como covariável**, transformando a contaminação de premissa em quantidade medida.
3. **A regra "sortear somente após a entrada do projeto"** é restrição de implementação, não escolha analítica — vai para a especificação do produto.

E uma constatação favorável que vale registrar: **o desfecho principal do T3 é naturalmente resistente a efeito de demanda**, porque um trabalhador que quisesse agradar não saberia como tornar sua peça mais ou menos parecida com as de outros clientes. Poucos desfechos organizacionais têm essa propriedade.

---

## Pendências geradas

- [ ] Especificar o sorteio em nível de projeto: estratos, semente registrada, momento exato no fluxo.
- [ ] Definir e pré-registrar o limiar de força da primeira etapa.
- [ ] Definir a tabela de equilíbrio: quais características de projeto entram.
- [ ] Definir os indicadores de atrito e a periodicidade de monitoramento.
- [ ] Levantar alguma referência setorial de estúdios de design no Brasil para caracterizar a amostra — se não existir, declarar.
- [ ] Confirmar venue e ano de Bandiera, Barankay e Rasul sobre experimentos de campo com firmas ⚠️ [NÃO VERIFICADO nesta missão].
- [ ] **M20 herda:** o recrutamento deve informar que há sorteio, sem revelar a hipótese — redação delicada, precisa passar pelo CEP.
