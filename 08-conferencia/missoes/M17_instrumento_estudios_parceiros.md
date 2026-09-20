# M17 — Instrumento comum: campos mínimos, coleta sem atrito, consentimento e anonimização

Executada em 2026-08-21. Escopo revisado pela M16.

---

## Mudança de escopo, herdada da M16

A missão foi escrita como "instrumento para estúdios parceiros doarem dados". A auditoria da M16 mostrou que **não existe dado histórico a doar** — nem no Argos Core nem, por extensão, em sistemas equivalentes de estúdios pequenos, que raramente registram histórico de status ou vinculam artefatos.

**A missão vira, portanto, a especificação de instrumentação de um produto** que os estúdios já usariam de qualquer forma. Isso é melhor: elimina a dependência de terceiros que a M08 marcou como ameaça máxima.

---

## Resumo do que esta missão entrega

1. **Esquema mínimo de pesquisa** — 4 tabelas, ~20 campos novos, dos quais **apenas um exige input humano**.
2. **Base legal verificada:** LGPD art. 7º, IV. Mas com uma ressalva importante — a orientação da ANPD sobre o tema é **texto para discussão, não norma vinculante**.
3. **⚠️ CEP é provavelmente obrigatório**, e não dispensável: a dispensa da Resolução CNS 510/2016 vale para dado **já agregado** (DataSUS, IBGE). Tarefa por trabalhador não é agregada.
4. **⚠️ Conflito de interesse estrutural, que o CEP vai apontar.** Felipe é pesquisador, dono do estúdio e vendedor do produto. Os trabalhadores da Argos são subordinados a ele. Tratamento na seção 6.

---

## 1. O esquema mínimo

### Tabela nova: `task_status_event` (append-only)

O item de maior retorno de todo o roteiro. Dele derivam tempo de ciclo, retrabalho, reabertura e sequência de estados.

| Campo | Tipo | Nota |
|---|---|---|
| `event_id` | uuid | |
| `task_id` | uuid | |
| `from_status` | enum | nulo na criação |
| `to_status` | enum | |
| `occurred_at` | timestamptz | **UTC, nunca sobrescrito** |
| `actor_id` | uuid | quem moveu |
| `source` | enum | `ui` · `api` · `automation` |

**Append-only, sem update e sem delete.** É o que distingue rastro de execução de registro de plano.

### Acréscimos a `task`

| Campo | Origem | Input humano? |
|---|---|---|
| `completed_at` | Primeira transição para Concluído; **imutável** | Não, derivado |
| `reopened_count` | Derivado do log | Não |
| `task_type_id` | Taxonomia (ver M15) | Não, herdado do template |
| `objectively_verifiable` | Booleano da taxonomia — dentro ou fora da fronteira | Não, herdado |
| `ai_usage` | `nenhum` · `ideação` · `rascunho` · `edição` · `execução integral` · `não informado` | **Sim — o único** |
| `ai_tool` e `ai_tool_version` | Texto, preenchido quando `ai_usage ≠ nenhum` | Sim, mas opcional |
| `effort_estimate_min`, `effort_actual_min` | Opcional | Sim, opcional |

### Acréscimos a `project`

| Campo | Por quê |
|---|---|
| `client_id` | **A M14 fixou que a similaridade se mede entre clientes distintos.** Sem campo, a consulta não existe |
| `client_sector` | Permite testar a hipótese forte: convergência entre **marcas concorrentes** |

### Tabela nova: `artifact`

Sem isto, a métrica primária da M14 é impossível.

| Campo | Nota |
|---|---|
| `artifact_id`, `task_id` | |
| `kind` | `copy` · `imagem` · `documento` · `vídeo` · `layout` |
| `uri` | Onde mora (Drive, storage) |
| `content_hash` | SHA-256 — **identidade estável, resistente a renomeação e movimentação** |
| `size_metric` | Contagem de caracteres, dimensões ou duração — necessário para a normalização por formato (M14) |
| `created_at` | |
| `embedding`, `embedding_model`, `embedding_version` | Calculado e **congelado** — trocar de modelo no meio da série quebra a comparabilidade |

### Acréscimos a `organization`

`studio_id`, `size_band`, `founded_year`, `research_consent_status`, `consent_date`.

---

## 2. Coleta sem atrito

O princípio: **tudo que puder ser derivado, deriva-se.** Restam duas fricções.

**A única obrigatória: o campo `ai_usage`.** Desenho para custo próximo de zero:

- Aparece **uma vez**, na transição para Concluído.
- Seis opções, seleção única, um toque.
- **Padrão é `não informado`, e nunca bloqueia a conclusão da tarefa.** Um campo que impede o trabalho é um campo que gera dado falso.
- Ausência é informação: taxa de preenchimento por estúdio e por período vira variável de qualidade e entra como controle.

**A segunda, opcional: vincular o artefato.** Mitigação — integração que puxa automaticamente o link do Drive quando a tarefa é concluída, com confirmação de um clique. Onde a integração não existir, colar URL.

### O que não fazer

- ❌ Formulário de pesquisa separado. Ninguém preenche.
- ❌ Campo obrigatório novo em qualquer fluxo existente.
- ❌ Pedir estimativa de esforço no início. Notoriamente mal preenchida e enviesada.

---

## 3. Base legal — LGPD

**Referência verificada:** ANPD, *A LGPD e o tratamento de dados pessoais para fins acadêmicos e para a realização de estudos por órgão de pesquisa*. **Texto para discussão nº 1/2022**, processo SEI 00261.000810/2022-17.

> ⚠️ **É documento de discussão, não norma vinculante.** O próprio texto se descreve como *"documento de referência inicial, divulgado no formato de texto para discussão, com o intuito de promover o debate público e colher contribuições da sociedade"*. Citar como orientação, nunca como autorização.

Dispositivos aplicáveis:

| Dispositivo | Conteúdo |
|---|---|
| **Art. 7º, IV** | Tratamento permitido *"para a realização de estudos por órgão de pesquisa, **garantida, sempre que possível, a anonimização** dos dados pessoais"* |
| Art. 11, II, c | Equivalente para dado sensível |
| Art. 5º, XVIII | Define **órgão de pesquisa** |
| Art. 4º, II, b | Define tratamento *"para fins exclusivamente acadêmicos"* |
| Art. 16, II | Conservação para estudo por órgão de pesquisa |

**Consequência prática:** a base legal é do **órgão de pesquisa**, não do pesquisador pessoa física. O estudo tem de correr **sob a FGV**, com vínculo comprovado. O documento da ANPD registra que órgãos públicos vêm **indeferindo pedidos de pessoa natural** para tratamento de dados com fim de pesquisa acadêmica.

> **Isto tem consequência de desenho:** o convênio de dados deve ser entre **estúdio parceiro e FGV**, com Felipe como pesquisador vinculado — não entre estúdio e Argos Estúdio, nem entre estúdio e Felipe.

---

## 4. Ética em pesquisa — CEP

A Resolução CNS nº 510/2016 rege pesquisa em Ciências Humanas e Sociais que envolva dados obtidos diretamente com participantes **ou informações identificáveis**.

**A dispensa de submissão ao sistema CEP/CONEP é restrita a dado já fornecido de forma agregada** — os exemplos citados são DataSUS e IBGE.

| Tema | Precisa de CEP? |
|---|---|
| **T2** (POF/PNAD públicos agregados + saídas de LLM; sem sujeito humano) | **Provavelmente dispensável** — enquadra-se na hipótese de dado agregado |
| **T3** (tarefa por trabalhador identificável, em firmas) | **Provavelmente obrigatório** |

**Recomendação:** submeter o T3 ao CEP da FGV com **pedido de dispensa de TCLE individual**, justificado por anonimização na origem, risco mínimo e impraticabilidade de consentir cada trabalhador de cada estúdio ao longo de 18 meses. **Preparar-se para que a dispensa seja negada** e para ter de fazer, no mínimo, notificação individual.

Prazo: submissão ao CEP leva semanas a meses. **Se o T3 mira 2028, o protocolo tem de entrar em 2026.**

---

## 5. Esquema de anonimização

Aplicado **na origem**, antes de qualquer dado sair do ambiente do estúdio.

| Entidade | Tratamento |
|---|---|
| **Pessoa** | `actor_id` substituído por `HMAC-SHA256(chave_do_estudo, user_uuid)`. Chave sob custódia da FGV, nunca no repositório. Nome e e-mail **nunca saem** |
| **Estúdio** | Pseudônimo (`Estúdio A`, `B`…). Preservam-se apenas faixa de tamanho e ano de fundação |
| **Cliente** | Pseudônimo mais **código de setor**. Nome do cliente nunca sai — e o setor é o que a hipótese exige |
| **Texto livre** | `description` e `name` de tarefa **excluídos do conjunto compartilhado**. Contêm nome de cliente, de pessoa e detalhe comercial |
| **Artefato** | Conteúdo bruto **nunca compartilhado**. Só `content_hash`, `size_metric` e o **embedding** |

### ⚠️ A ressalva que precisa estar escrita

**Embedding não é anonimização.** Há literatura estabelecida sobre inversão de embeddings — recuperação aproximada do texto original a partir do vetor. Tratar embedding como dado anonimizado é erro técnico e jurídico.

**Consequência:** o conjunto com embeddings é de **acesso restrito sob acordo**, não de publicação aberta. O que se publica para replicação são as **estatísticas derivadas** — matrizes de similaridade agregadas, coeficientes — e nunca os vetores.

---

## 6. ⚠️ O conflito de interesse

Felipe é, simultaneamente: **pesquisador**, **dono do estúdio** sob estudo, e **vendedor do produto** que faz a coleta. Os trabalhadores da Argos são **subordinados hierárquicos** dele.

Isso é problema real, não formalidade. Um CEP competente vai apontar três coisas:

1. **Consentimento sob subordinação não é livre.** Um funcionário não recusa participar de pesquisa do dono da empresa.
2. **O pesquisador tem interesse comercial no resultado.** Um achado que valorize o produto beneficia o pesquisador financeiramente.
3. **Ele tem acesso irrestrito ao dado bruto** por ser administrador do sistema.

### Mitigações, e nenhuma é opcional

| Problema | Mitigação |
|---|---|
| Subordinação | **Excluir os trabalhadores da própria Argos da análise em nível individual.** A Argos entra como estúdio, com dado agregado, ou fica de fora |
| Interesse comercial | **Declaração de conflito de interesse** no paper, no pré-registro e no protocolo do CEP. Explícita, não em nota de rodapé |
| Acesso ao bruto | Pseudonimização executada por **rotina automática sob custódia da FGV**, com o pesquisador acessando apenas o conjunto já tratado. Chave HMAC fora do alcance dele |
| Viés de resultado | **Pré-registro** com o abstract da versão nula escrito antes da coleta, como já se fez para o T2 na M12 |

**A primeira mitigação custa dado e é a mais importante.** Melhor perder o próprio estúdio da amostra individual do que ter o desenho inteiro questionado.

---

## 7. Fluxo de recrutamento

Deixa de ser pedido de doação e passa a ser proposta de valor.

| Etapa | Conteúdo |
|---|---|
| 1. Oferta | Uso do Argos Core, com o painel de métricas de execução como benefício direto ao estúdio |
| 2. Adesão à pesquisa | **Opt-in explícito e separado**, no nível da organização, com recusa sem perda de funcionalidade |
| 3. Convênio | **Estúdio ↔ FGV**, não estúdio ↔ Argos |
| 4. Notificação aos trabalhadores | Aviso claro de que dados de execução pseudonimizados são usados em pesquisa, com canal de objeção |
| 5. Contrapartida | Relatório comparativo anonimizado — cada estúdio vê sua posição contra a distribuição, sem identificar os demais |

A contrapartida do item 5 é o que sustenta a adesão. **É informação que o estúdio não consegue obter sozinho**, e custa quase nada produzir.

### Critério de inclusão, herdado da M14

> Pelo menos **dois clientes por período** com entregas do mesmo tipo.

Sem isso, a métrica primária — similaridade entre clientes distintos — não é calculável para aquele estúdio-período.

---

## Pendências geradas

- [ ] **Implementar `task_status_event`.** Reafirmado da M16 como o item de maior retorno do roteiro.
- [ ] Consultar o **CEP da FGV** sobre enquadramento do T3 e sobre a viabilidade de dispensa de TCLE. Prazo longo — iniciar em 2026.
- [ ] Verificar se a FGV tem modelo de **convênio de compartilhamento de dados** com empresa privada para pesquisa.
- [ ] Confirmar o texto do art. 5º, XVIII da LGPD e se a FGV se enquadra como órgão de pesquisa — o estudo da ANPD levanta a questão sem fechá-la.
- [ ] Verificar se saiu norma da ANPD posterior a 2022 sobre o tema; o documento lido é texto para discussão e pode ter sido superado.
- [ ] Decidir se a Argos entra na amostra individual. **Recomendação: não.**
- [ ] Levantar a literatura de inversão de embeddings para fundamentar a restrição de compartilhamento com número, não com afirmação genérica.
- [ ] Redigir o termo de notificação ao trabalhador e o texto de opt-in organizacional.
