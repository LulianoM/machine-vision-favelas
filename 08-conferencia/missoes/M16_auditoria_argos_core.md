# M16 — Auditoria do Argos Core: o que existe de fato

Executada em 2026-08-21, por consulta direta à API via MCP. **Somente leitura — nada foi modificado.**

---

## Veredito

> **A premissa do T3 não se sustenta sobre o dado atual.** O Argos Core não é um microdado histórico de execução criativa. É um sistema de gestão de projetos com **dois meses de vida**, treze projetos, sem histórico de mudança de status, sem vínculo com os artefatos entregues e sem qualquer período anterior à adoção de IA generativa.
>
> Não há "antes". O sistema nasceu depois.

Isso não mata o T3 — **reclassifica-o**. Detalhado na seção 6.

---

## 1. Cobertura

| | |
|---|---|
| Projetos | **13** |
| Primeiro registro | **2026-06-01** |
| Último registro | **2026-07-28** |
| Cobertura temporal | **≈ 2 meses** |
| Times | 5 — Geral (padrão), Brand, Growth, Tech, UGC |

### Composição dos 13 projetos

| Natureza | Quantos | Quais |
|---|---|---|
| **Cliente externo** | **4** | Sistema Viverde (R$ 24.000), Plataforma SEMPER (R$ 12.000), [Rebranding] Gestionna (R$ 8.300), [UGC] Carlos Pina |
| Marketing interno | 4 | Instagram Argos 1º trimestre, Tráfego Criativos, Ecossistema SEO, Produtos Argos Lançamentos |
| Produto interno | 2 | Argos Core v1.0.0, Prospector IA Botz |
| Interno diverso | 2 | Remodelagem Instagram, Pesquisa de benchmarking e moodboard |
| **Teste** | **1** | MCP SERVICE TESTE 2.0 |

**Apenas 3 dos 13 projetos têm orçamento diferente de zero.** Quatro são de cliente. Um é lixo de teste.

### Granularidade observada

Etapas por projeto: **2 a 9**. Tarefas por etapa nas amostras inspecionadas: **2 a 3**.

Ordem de grandeza estimada do universo: **algo entre 100 e 150 tarefas no total.** Para comparação, Dell'Acqua et al. têm 758 sujeitos × 19 tarefas; Doshi e Hauser têm 293 histórias.

---

## 2. O esquema — o que cada tarefa carrega

Campos observados no retorno da API:

| Campo | Presente | Utilidade para o T3 |
|---|---|---|
| `id`, `external_id` | ✅ | Identificação |
| `name` | ✅ | Classificação de tipo de tarefa |
| `description` | ✅ parcial | **Rica no time Tech, vazia no Brand** |
| `owner_id` | ✅ | Efeito fixo de pessoa |
| `team_id` | ✅ | Proxy de tipo de trabalho (Brand/Growth/Tech/UGC) |
| `stage_id` | ✅ | Posição no fluxo |
| `priority` | ✅ | Controle |
| `status` | ✅ | A Fazer / Em Andamento / Concluído |
| `deadline` | ✅ parcial | ⚠️ ver problemas de qualidade |
| `created_at` | ✅ | Início nominal |
| `updated_at` | ✅ | ⚠️ **sobrescrito a cada edição** |

### O que falta — e é isto que inviabiliza o desenho

| Ausente | Por que é fatal |
|---|---|
| ❌ **Histórico de mudança de status** | Impossível reconstruir quando a tarefa saiu de "A Fazer", entrou em "Em Andamento" e virou "Concluído". Sem isso **não há tempo de ciclo** |
| ❌ **`completed_at`** | Só existe `updated_at`, que é sobrescrito por qualquer edição posterior. Uma tarefa concluída em julho e editada em agosto perde a data de conclusão |
| ❌ **Contador de retrabalho ou reabertura** | A hipótese central do T3 — retrabalho sobe fora da fronteira — **não tem variável dependente** |
| ❌ **Vínculo com o artefato entregue** | As entregas moram no Google Drive, referenciadas em texto livre na descrição do projeto. **Sem artefato, não há embedding, e sem embedding não há medida de homogeneização** — que é a métrica primária definida na M14 |
| ❌ **Ferramenta de IA usada e versão** | Sem isso, não se distingue adoção de deriva de modelo (a ameaça de Karouzos et al., M14) |
| ❌ **Cliente como campo** | O cliente está implícito no nome do projeto. A M14 fixou que a similaridade deve ser medida **entre clientes distintos** — sem campo de cliente, a consulta não existe |
| ❌ **Esforço, horas ou estimativa** | Sem medida de produtividade além de contagem de tarefas |

---

## 3. Problemas de qualidade encontrados

**Prazo anterior à criação.** As três tarefas da etapa de naming do Gestionna têm `deadline` em **2026-04-13** e `created_at` em **2026-06-15** — dois meses depois do prazo. É registro retroativo de um projeto já em curso, não acompanhamento.

**Assinatura de entrada em lote.** No Gestionna, as 9 etapas foram criadas entre 13:18:43 e 13:18:53 e atualizadas entre 16:04:56 e 16:05:07 — intervalos de cerca de um segundo entre registros. As três tarefas de naming, idem: criadas em 13:19:32, 13:19:34 e 13:19:35; atualizadas em 16:05:25, 16:05:26 e 16:05:28.

> Isso é preenchimento por script ou por ação em massa na interface. **Não é rastro de execução.**

**Etapas paradas.** As 9 etapas do Gestionna estão todas em "Em Andamento" desde 15 de junho, sem alteração em mais de dois meses. Ou o projeto parou, ou o sistema não está sendo atualizado conforme o trabalho anda.

**Contraste entre times.** O time Tech tem sinal mais orgânico: as tarefas de correção de bugs do SEMPER foram criadas em 18/06 e atualizadas em 23/06 — cinco dias depois, plausivelmente ao serem concluídas. E as descrições são detalhadas, com fonte declarada ("áudio do cliente em 15/06/2026, 19:59").

**O time Brand, que é o objeto do T3, é justamente o de dado mais pobre:** descrições vazias, entrada em lote, prazos inconsistentes.

---

## 4. O que dá para medir hoje

Honestamente, pouco:

| Possível | Ressalva |
|---|---|
| Contagem de tarefas por time e por pessoa | N ≈ 100–150; sem poder para nada |
| Distribuição de prioridade | Descritivo |
| Tempo entre `created_at` e `updated_at` | **Só é tempo de ciclo se a tarefa não foi editada depois.** Não verificável |
| Composição de projetos por natureza | Descritivo |

**Nenhuma das três hipóteses do T3 é testável:** homogeneização de portfólio exige artefatos; retrabalho exige histórico de status; tempo de ciclo exige `completed_at` confiável.

---

## 5. O que teria de mudar

Especificação mínima para que o T3 se torne possível. **Nada aqui é difícil — é tudo campo e log.**

| Adição | Prioridade | Custo |
|---|---|---|
| **Log de eventos append-only** de mudança de status, com `de`, `para`, `quando`, `quem` | **Crítica** | Baixo. Uma tabela |
| **`completed_at` imutável**, gravado na primeira transição para Concluído | **Crítica** | Trivial |
| **`client_id`** como campo de primeira classe no projeto | **Crítica** | Baixo |
| **Vínculo de artefato**: URL, hash e tipo de cada entrega associada à tarefa | **Crítica** | Médio |
| **`reopened_count`**, derivável do log de eventos | Alta | Grátis, se houver log |
| **`ai_tool` e `ai_tool_version`** por tarefa | Alta | Baixo |
| **Taxonomia de tipo de tarefa**, com marcação de verificabilidade objetiva (dentro/fora da fronteira, conforme M15) | Alta | Baixo, mas exige decisão |
| Estimativa de esforço e realizado | Média | Médio |

O **log de eventos** é o item que sozinho destrava mais: dele saem tempo de ciclo, retrabalho, reabertura e sequência de estados.

---

## 6. A reclassificação do T3

O dossiê descrevia o T3 como "programa de 12 meses" usando o Argos Core como espinha dorsal de dado já existente. **Isso estava errado, e a auditoria corrige.**

| | Antes desta missão | Depois |
|---|---|---|
| Natureza | Análise de dado histórico existente | **Estudo prospectivo com instrumentação** |
| Ponto de partida | Junho de 2026 | **Dia em que o log de eventos entrar em produção** |
| Janela de coleta | Retroativa | 12 a 18 meses **a partir da instrumentação** |
| Alvo realista | AIM 2027 (já descartado) | **AIM 2028, e apertado** |
| Risco principal | Endogeneidade da adoção | **Não instrumentar a tempo** |

### E há um lado bom, que é real

Todo o trabalho de desenho das missões M13 a M15 **não se perde — vira a especificação da instrumentação**:

- A M14 define que a métrica primária exige artefato vinculado e cliente identificado → **campos a criar**.
- A M15 define que a hipótese de retrabalho só vale em tarefas com verificabilidade objetiva → **taxonomia a criar**.
- A M14 registra que a versão da ferramenta confunde adoção com deriva de modelo → **campo a criar**.

Ou seja: as três missões produziram, sem saber, o **requisito de produto** do Argos Core para virar instrumento de pesquisa.

E há um ativo estratégico embutido. O Argos Core é produto — há um projeto "Argos Core v1.0.0" e outro de lançamento. **Se os estúdios parceiros da M17 usarem o produto instrumentado, a coleta multi-firma deixa de ser um pedido de favor e passa a ser subproduto do uso.** Isso resolve, de uma vez, a dependência de terceiros que a M08 apontou como ameaça e que os medidores do dossiê marcam em 5 de 5.

---

## 7. O que isso significa para novembro

**Nada muda no T2**, que é o tema de submissão e não depende do Argos Core.

**O T3 sai definitivamente do horizonte de 2027** — o que já estava indicado, mas agora por um motivo concreto e verificado, não por estimativa de esforço.

**A ação de agosto muda de "conversar com estúdios parceiros" para "instrumentar o produto".** É trabalho de engenharia, que é o que Felipe faz, e o custo é de dias, não de meses. Cada semana sem log de eventos é uma semana de dado que não existirá em 2028.

---

## Pendências geradas

- [ ] **Especificar e implementar o log de eventos de status.** É o item de maior retorno do roteiro inteiro em termos de dado futuro.
- [ ] Adicionar `completed_at` imutável e `client_id`.
- [ ] Decidir o modelo de vínculo de artefato — URL do Drive é frágil; hash de conteúdo é melhor para embedding estável.
- [ ] Definir a taxonomia de tipo de tarefa com marcação de verificabilidade objetiva.
- [ ] **Limpar o projeto de teste** "MCP SERVICE TESTE 2.0" ou marcá-lo com flag de exclusão analítica.
- [ ] Corrigir ou marcar os registros com prazo anterior à criação.
- [ ] **M17 muda de escopo:** o recrutamento de estúdios passa a ser recrutamento para uso do produto instrumentado, não pedido de doação de dados.
- [ ] **M18 e M19 mudam de natureza:** o event study passa a ser desenhado sobre dado que ainda não existe, o que na verdade é melhor — permite pré-registrar antes de qualquer observação.
- [ ] Atualizar o dossiê na fronteira do bloco B (M20) com a reclassificação do T3.
