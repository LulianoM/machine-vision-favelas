# M29 — Experimento de vinheta: manipulação, níveis, checagem e amostra

Executada em 2026-08-21.

---

## Resumo do que esta missão entrega

1. **Arquitetura em duas partes, e isso não é detalhe.** As cinco escalas da M27 são longas demais para serem aplicadas oito vezes. **Parte 1** é o survey correlacional sobre o trabalho real do respondente, com as escalas completas. **Parte 2** é o experimento de vinheta, com medidas curtas por cenário. Uma dá o modelo estrutural; a outra dá a causalidade.

2. **O desenho testa uma troca, não um efeito.** Seguindo a correção da M28: prescrição de método e flexibilidade de agendamento entram como **fatores separados**, para que se possa observar autonomia caindo numa faceta e subindo na outra **na mesma pessoa, no mesmo cenário**.

3. **Oito vinhetas intra-sujeito mais uma manipulação entre-sujeitos.** Oito é a mediana da literatura; a quarta manipulação vira entre-sujeitos para não estourar o baralho.

---

## 1. Arquitetura em duas partes

| | Parte 1 — Survey | Parte 2 — Vinhetas |
|---|---|---|
| Objeto | O trabalho **real** do respondente | Cenários **hipotéticos** |
| Instrumentos | WDQ autonomia (9 itens), IDS, NGSE, JIS, ERI excesso de comprometimento — **completos** (M27) | Medidas curtas, 1 a 2 itens por construto |
| Inferência | Associação; modelo estrutural | **Causal**, por aleatorização |
| Papel | Validade externa e ancoragem | Identificação |

**Ordem: survey primeiro, vinhetas depois.** Se as vinhetas vierem antes, elas ancoram a percepção do trabalho real e contaminam a Parte 1. O inverso é inofensivo.

---

## 2. Os fatores

### Manipulados dentro do sujeito — 2 × 2 × 2 = 8 vinhetas

| Fator | Nível baixo | Nível alto |
|---|---|---|
| **A. Prescrição de método** | A ferramenta **sugere** alternativas e você escolhe como fazer | A ferramenta **define** o formato e a sequência; você preenche |
| **B. Flexibilidade de agendamento** | Prazos e ordem das tarefas **definidos pelo sistema** | Você decide **quando** e em que ordem executar |
| **C. Enquadramento do monitoramento** | As métricas são usadas para **apoiar seu desenvolvimento** | As métricas são usadas na sua **avaliação de desempenho** |

**A é a manipulação central.** B existe para permitir a observação da troca: o cenário com método prescrito e agendamento livre é o quadrante que a M28 identificou como o padrão real da gestão algorítmica. C vem do moderador que a revisão de Lu nomeia e que é o único manipulável.

### Manipulado entre sujeitos

| Fator | Níveis |
|---|---|
| **D. Opacidade** | **Transparente**: você consegue ver por que a ferramenta sugeriu aquilo · **Opaca**: você não tem como saber |

Entre sujeitos porque, uma vez revelado o funcionamento num cenário, o respondente carrega esse conhecimento para os demais. É contaminação irreversível dentro do sujeito.

Cobre também a lacuna que Lu registra sobre transparência **acionável** contra **simbólica**.

### Medidos, não manipulados — os moderadores

Da M28: vínculo de trabalho (autônomo, PJ, celetista), complexidade típica da tarefa, dependência de renda de um único contratante, tempo de uso de IA generativa.

---

## 3. Esqueleto da vinheta

Texto curto, mesma estrutura em todos os cenários, com os três blocos manipulados em posição fixa:

> *Imagine que, no seu trabalho, você passa a usar uma ferramenta de inteligência artificial para produzir parte das suas entregas.*
>
> **[A]** *Ao começar uma tarefa, a ferramenta {sugere alguns caminhos possíveis e você escolhe como fazer | define o formato e a sequência do que deve ser produzido, e cabe a você preencher}.*
>
> **[B]** *{O sistema estabelece os prazos e a ordem em que as tarefas devem ser feitas | Você decide quando fazer cada tarefa e em que ordem}.*
>
> **[C]** *A ferramenta registra automaticamente quanto tempo cada etapa levou e quantas revisões foram necessárias. Esses dados {são usados para apoiar seu desenvolvimento | entram na sua avaliação de desempenho}.*

**Regras de redação:**

- **Mesmo comprimento** em todos os níveis, para que a diferença não seja de saliência.
- **Sem adjetivo avaliativo.** Nada de "rígido", "engessado", "autônomo". A avaliação é do respondente, não do instrumento.
- **A tarefa nunca é nomeada.** Nomear ativa esquemas específicos e reduz comparabilidade entre respondentes de subáreas distintas.
- **Ordem dos blocos fixa; ordem das vinhetas aleatória.** A literatura registra efeitos de ordem, aprendizagem e fadiga, e a randomização da ordem é a mitigação padrão.

---

## 4. Medidas por vinheta

Curtas por obrigação aritmética: 8 vinhetas × qualquer escala completa é inviável.

| Construto | Itens | Origem |
|---|---|---|
| Autonomia de **método** | 1 | Adaptado do WDQ, método |
| Autonomia de **agendamento** | 1 | Adaptado do WDQ, agendamento |
| Autonomia de **decisão** | 1 | Adaptado do WDQ, decisão — entra como controle |
| **Autocobrança antecipada** | 2 | Adaptado do excesso de comprometimento do ERI |
| Insegurança antecipada | 1 | Adaptado do JIS |
| **Checagens de manipulação** | 3 | Uma por fator intra-sujeito |

**Total: 9 itens por vinheta, 72 no experimento.** Somados à Parte 1, o questionário fica longo — e a M30 terá de decidir se corta a Parte 1 ou reduz o baralho.

### As checagens de manipulação

Uma por fator, formuladas como percepção e não como memória:

- *Nesse cenário, a ferramenta determinava como o trabalho deveria ser feito.* (A)
- *Nesse cenário, eu controlava quando cada tarefa seria feita.* (B)
- *Nesse cenário, os dados registrados seriam usados para me avaliar.* (C)

**Critério declarado a priori:** cada checagem deve discriminar entre os níveis com diferença significativa e efeito de tamanho ao menos médio. **Fator cuja checagem falhar é reportado como falhado e removido da análise confirmatória** — não reinterpretado.

---

## 5. As hipóteses do experimento

```
H1  Prescrição de método alta  →  autonomia de método MENOR
H2  Flexibilidade de agendamento alta  →  autonomia de agendamento MAIOR
H3  A TROCA: no cenário (método prescrito + agendamento livre),
    autonomia de método cai e a de agendamento sobe, na mesma pessoa
H4  Prescrição de método alta  →  autocobrança antecipada MAIOR
H5  Monitoramento punitivo  →  autocobrança antecipada MAIOR
H6  Opacidade  →  autocobrança antecipada MAIOR  (entre sujeitos)
H7  Autonomia de DECISÃO não é afetada por A nem por B  (predição nula, declarada)
```

**H3 é a hipótese que justifica o desenho** e a que nenhum dos trabalhos revisados testou. **H7 é predição nula declarada a priori**, o que é honesto e a torna informativa: se a autonomia de decisão também cair, a tese de "troca" morre e vira "perda em bloco".

---

## 6. Modelo de análise

Estrutura de medidas repetidas: 8 vinhetas aninhadas em respondente.

```
Y_ij = β₀ + β₁A_ij + β₂B_ij + β₃C_ij + β₄D_i
     + (interações pré-especificadas)
     + u_i + ε_ij            u_i = intercepto aleatório de respondente
```

- **Modelo multinível com intercepto aleatório por respondente.** Ignorar o aninhamento infla a significância.
- **Erro padrão agrupado por respondente.**
- Moderação testada por interação entre fator manipulado e característica medida.
- **Correção de multiplicidade:** confirmatórias são H1 a H3; H4 a H7 sob Benjamini–Hochberg, mesma regra da M12.

---

## 7. Amostra e baralho

**Oito vinhetas por respondente.** Referência: em levantamento de 106 experimentos de survey fatorial em periódicos de sociologia, a **mediana foi de oito vinhetas por respondente**, com máximo de 110; **21% usaram uma única vinheta**, prática descrita como ineficiente e de baixo poder estatístico.

**Fatorial completo intra-sujeito**, 2×2×2 — cada respondente vê **todas as oito combinações**, em ordem aleatória. Isso maximiza o poder e dispensa desenho fracionário D-eficiente, que seria necessário se houvesse mais fatores.

> **Referência metodológica:** AUSPURG, Katrin; HINZ, Thomas. *Factorial Survey Experiments*. Sage. A D-eficiência garante que efeitos principais das vinhetas e interações com características do respondente sejam mutuamente não correlacionados. **Aqui não é necessária**, porque o fatorial é completo — mas a referência entra no método para justificar a escolha.

⚠️ **Alerta de fadiga.** A literatura registra que respondentes de menor escolaridade mostram **maior inconsistência** quando o número de vinhetas é alto. Como a população do T4 é de profissionais de marketing, o risco é moderado — mas **medir consistência** e reportar é obrigatório.

**Tamanho da amostra:** definido na M30, e agora com uma restrição a mais — o N é governado por três coisas ao mesmo tempo: a análise fatorial confirmatória das cinco escalas (M27), o modelo estrutural, e o poder do experimento multinível. **O maior dos três manda.**

---

## 8. ⚠️ A limitação que precisa estar escrita

Vinheta mede **intenção declarada**, não comportamento. A evidência sobre validade externa é mista: intenções podem sub ou superestimar comportamento real, e o efeito depende do método e do comportamento em questão.

**Do lado favorável:** há evidência de correspondência forte em pelo menos um caso bem documentado — experimentos de vinheta sobre atributos de imigrantes hipotéticos comparados a resultados de referendos suíços correspondentes, com efeitos estimados batendo *"remarkably well"* com o comportamento observado. ⚠️ [Referência exata não verificada nesta missão — provavelmente PNAS, 2015.]

**Do lado desfavorável, e é o argumento mais forte contra o T4:** a vinheta apresenta um **momento discreto**, enquanto o trabalhador real experimenta normas por **interações acumuladas ao longo do tempo**, dentro de histórias de relacionamento, dinâmicas de poder e influência de pares.

> **Isto não é ressalva de rodapé — é o núcleo da crítica que a dissertação faz.** A pressão produtiva de que Felipe trata **é acumulativa por definição**. Uma vinheta não a captura.

**A resposta honesta, e ela fortalece o conjunto:** a vinheta não substitui o braço qualitativo, **complementa**. A vinheta estabelece que a prescrição de método *causa* aumento de autocobrança antecipada; as entrevistas mostram *como* isso se acumula e se internaliza ao longo do tempo. **Um sem o outro é incompleto — e essa é a melhor justificativa de método misto que a dissertação pode ter.**

---

## Pendências geradas

- [ ] Redigir os oito textos de vinheta e submeter a pré-teste cognitivo com 8 a 12 profissionais.
- [ ] Verificar a referência de validação de vinheta contra comportamento real (referendos suíços).
- [ ] Verificar a referência canônica de melhores práticas em vinheta na pesquisa organizacional — provavelmente *Organizational Research Methods*, 2014 ⚠️ [não verificada].
- [ ] Confirmar a fonte do levantamento de 106 experimentos e da mediana de oito vinhetas.
- [ ] **M30 herda:** decidir se o questionário completo (Parte 1 mais Parte 2) é longo demais e o que cortar. Candidato natural a corte: o IDS na Parte 1.
- [ ] Definir os itens exatos das medidas curtas, derivados das escalas completas com autorização conceitual.
- [ ] Decidir se a Parte 2 usa amostra distinta da Parte 1 — o que resolveria o comprimento ao custo de perder a ligação intra-sujeito.
