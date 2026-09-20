# M20 — Recrutamento de estúdios: quantos, perfil, contrapartida, mensagem

Executada em 2026-08-21. Fecha o Bloco B.

---

## Resumo

1. **O número é 10 estúdios com pelo menos 40 projetos cada ao longo da coleta** — não 8 a 15 como o dossiê estimava por intuição. Poder de **0,79** para um efeito ITT padronizado de 0,25.

2. **Contraste com a M10 que vale registrar:** lá, acrescentar itens não ajudava; aqui, acrescentar projetos ajuda muito. O motivo é estrutural — **quando o sorteio é dentro do cluster, as unidades dentro do cluster carregam variação identificadora.** Na M10 a distância variava só entre estratos.

3. **A contrapartida é o que sustenta a adesão, e ela já existe como funcionalidade.** O estúdio não é convidado a doar dado: é convidado a usar um produto e receber um relatório comparativo que não consegue obter sozinho.

---

## 1. Quantos — cálculo de poder

Simulação com sorteio no nível do projeto dentro de estúdio, erro agrupado por estúdio, bootstrap selvagem, alfa de 5%.

**Referência de tamanho de efeito.** Doshi e Hauser (M13) acharam +0,871 pontos de similaridade contra amplitude de 8,10 na condição de controle — o que sugere desvio padrão da ordem de 2 pontos e efeito padronizado próximo de **0,44**, em condição de laboratório com atribuição direta. **No campo, com encorajamento em vez de atribuição e com a contaminação da M19, o efeito ITT será substancialmente menor.** Planejar para **0,25**.

### Resultados

**Correlação intraestúdio de 0,10:**

| Estúdios | Projetos por estúdio | d=0,15 | d=0,25 | d=0,35 | d=0,50 |
|---:|---:|---:|---:|---:|---:|
| 6 | 20 | 0,25 | 0,41 | 0,64 | 0,86 |
| 10 | 20 | 0,28 | 0,50 | 0,74 | 0,97 |
| **10** | **40** | **0,43** | **0,79** | **0,95** | **1,00** |
| 15 | 20 | 0,35 | 0,68 | 0,87 | — |
| 15 | 40 | 0,57 | 0,90 | 0,99 | — |

**Correlação intraestúdio de 0,25:**

| Estúdios | Projetos por estúdio | d=0,15 | d=0,25 | d=0,35 |
|---:|---:|---:|---:|---:|
| 10 | 20 | 0,29 | 0,61 | 0,82 |
| **10** | **40** | **0,47** | **0,82** | **0,98** |
| 15 | 40 | 0,56 | 0,94 | 0,99 |

### O achado que reforça o desenho

**Dobrar a correlação intraestúdio não reduz o poder.** Em 10 estúdios com 40 projetos e d=0,25: **0,79** com ICC de 0,10 e **0,82** com ICC de 0,25 — diferença dentro do ruído de simulação.

Isso não é acidente, é propriedade do desenho. Como **o sorteio é dentro do estúdio**, o efeito aleatório de estúdio é diferenciado pela própria comparação intraestúdio: ele infla a variância bruta, mas não toca a variação identificadora.

> **É o oposto exato da aleatorização por cluster**, onde correlação intraestúdio alta destrói o poder. Vale escrever no paper: o desenho de encorajamento intra-firma é **robusto à homogeneidade interna dos estúdios** — que é justamente o que se espera de um estúdio pequeno com processo padronizado.

A recomendação de 10 × 40 vale, portanto, **independentemente de quão parecidos os projetos de um mesmo estúdio sejam entre si**. Isso remove a incerteza mais desconfortável do cálculo.

### As três leituras

**Projetos por estúdio importam mais que estúdios.** De 20 para 40 projetos com 10 estúdios: 0,50 → 0,79 em d=0,25. De 6 para 10 estúdios com 20 projetos: 0,41 → 0,50. **Dobrar projetos vale mais que quase dobrar estúdios.**

Isso inverte a lição da M10, e por bom motivo: lá o tratamento variava **entre** estratos, então só estratos identificavam; aqui o sorteio é **dentro** do estúdio, então cada projeto acrescenta variação. Vale escrever isso no paper — é o argumento de por que o desenho de encorajamento resolve o problema de poucos clusters que a M18 apontou.

**Seis estúdios não bastam.** Poder de 0,41 em d=0,25. Seria um estudo desenhado para não achar nada.

**O alvo:** **10 estúdios, mínimo de 40 projetos cada** ao longo de 12 a 18 meses. Para um estúdio pequeno, 40 projetos em 18 meses é cerca de 2 por mês — plausível, e verificável no ato do recrutamento.

**Se 15 estúdios forem alcançáveis, vale o esforço:** 15 × 40 leva o poder de 0,79–0,82 para **0,90–0,94** em d=0,25. Mas 10 × 40 já é um desenho defensável, e 15 × 20 (0,61–0,68) é pior que 10 × 40. **Profundidade antes de largura.**

---

## 2. Perfil e critérios de inclusão

| Critério | Exigência | Origem |
|---|---|---|
| **Dois ou mais clientes ativos por período**, com entregas do mesmo tipo | **Eliminatório** | M14 — sem isso a métrica primária não é calculável |
| Volume de ~40 projetos previstos em 18 meses | **Eliminatório** | Poder |
| Mínimo de 8 peças por estúdio-trimestre | **Eliminatório** | M14 — estabilidade da métrica |
| Entregas em formato digital arquivável | **Eliminatório** | Sem artefato não há embedding |
| Equipe de 3 a 25 pessoas | Preferencial | Escopo declarado do estudo |
| Mix de serviços com componente criativo | Preferencial | Objeto |
| Uso já existente de alguma ferramenta de IA | **Preferencial, não eliminatório** | Encorajamento precisa de margem para mover |

**Exclusão declarada:** a própria Argos Estúdio **não entra na análise em nível individual**, pela subordinação hierárquica mapeada na M17. Pode entrar como estúdio-piloto de instrumentação, com dado descartado da amostra analítica.

### O que não exigir

Não exigir maturidade de gestão nem uso prévio do Argos Core. Ambos estreitariam a amostra na direção já enviesada que a M19 registrou como B6 — e a amostra já é seletiva por construção.

---

## 3. Contrapartida

O que o estúdio recebe, em ordem de valor percebido:

| Entrega | Quando | Custo de produzir |
|---|---|---|
| **Relatório trimestral comparativo anonimizado** — posição do estúdio contra a distribuição dos participantes, sem identificar os demais | A cada trimestre | Baixo — é consulta ao mesmo dado |
| Painel de métricas de execução próprio: tempo de ciclo, retrabalho, distribuição de carga | Contínuo | Já é o produto |
| Licença do Argos Core sem custo durante a pesquisa | Contínuo | Custo de infra |
| Menção como estúdio participante na publicação, se desejar | Ao publicar | Zero |
| Acesso antecipado aos resultados | Antes da publicação | Zero |

**O primeiro item é o que fecha a adesão.** Um estúdio pequeno não tem como saber se seu tempo de ciclo é bom ou ruim — não existe referência de mercado. O relatório comparativo é informação genuinamente inacessível de outra forma, e produzi-la custa quase nada.

---

## 4. Rascunho da mensagem

> **Assunto:** Estudo FGV sobre execução em estúdios criativos — convite
>
> Olá, [nome].
>
> Sou [nome], da Argos Estúdio, e estou conduzindo uma pesquisa de mestrado na FGV sobre como estúdios criativos organizam a execução de projetos. O estudo é conduzido sob a FGV, e o convênio de dados é entre a sua empresa e a universidade.
>
> **O que é.** Ao longo de 12 a 18 meses, acompanhamos dados de execução de projetos — quais tarefas, quanto tempo, quantas revisões — em um grupo de cerca de dez estúdios. Os dados são pseudonimizados na origem: nomes de pessoas e de clientes nunca saem da sua empresa.
>
> **O que você usa.** Um sistema de gestão de projetos, sem custo durante a pesquisa. Ele registra o que você já registraria de qualquer forma. Uma parte do fluxo é sorteada para receber sugestões de uso de ferramentas de IA — nada é bloqueado nem obrigatório, e sua equipe segue decidindo como trabalha.
>
> **O que você recebe.** Um relatório trimestral comparando seus indicadores com a distribuição dos estúdios participantes, sem identificar ninguém. Tempo de ciclo, retrabalho, distribuição de carga. É uma referência que hoje não existe no mercado brasileiro.
>
> **O que você não faz.** Não preenche formulário de pesquisa, não responde questionário, não muda processo. O único campo novo é uma seleção de um toque ao concluir uma tarefa, e ela é opcional.
>
> Se fizer sentido, mando os detalhes e o termo de participação. E se preferir só entender melhor antes, marco vinte minutos.
>
> [assinatura]

### As cinco escolhas de redação, e por quê

1. **"conduzido sob a FGV"** logo no início — a base legal da LGPD é do órgão de pesquisa, não do pesquisador pessoa física (M17).
2. **"pseudonimizados na origem"** com o que não sai, em vez de jargão de conformidade.
3. **O sorteio é declarado**, porque omiti-lo seria antiético e o CEP não aprovaria. **A hipótese não é declarada**, o que preserva o desenho contra efeito de demanda (M19/B3).
4. **"nada é bloqueado nem obrigatório"** desarma a objeção principal — ninguém aceita que digam à sua equipe como trabalhar.
5. **"O que você não faz"** é a seção mais importante. A objeção real de um estúdio pequeno não é privacidade, é **tempo**.

---

## 5. Funil e cronograma

| Etapa | Meta | Prazo |
|---|---|---|
| Lista de candidatos | 40 estúdios | Set 2026 |
| Contato inicial | 40 | Out–Nov 2026 |
| Conversa de 20 min | 20 | Nov–Dez 2026 |
| Adesão assinada | **12** | Jan 2027 |
| Instrumentação ativa | 10 | Fev 2027 |
| Início da coleta | 10 | **Mar 2027** |
| Fim da coleta | ≥ 8 | Set 2028 |

**Recruta-se 12 para terminar com 10**, pela ameaça de atrito (M19/B7).

⚠️ **O caminho crítico não é o recrutamento, é o CEP.** A M17 estabeleceu que o protocolo precisa entrar em 2026 e que, com o desenho de intervenção da M18, ele é mais exigente. **Nenhum contato de recrutamento deve prometer data de início antes de o parecer sair.**

---

## Pendências geradas

- [ ] Concluir a simulação de poder (15 e 20 estúdios; correlação intraestúdio de 0,25) e atualizar a seção 1.
- [ ] Montar a lista dos 40 estúdios candidatos.
- [ ] Redigir o termo de participação organizacional e a notificação ao trabalhador (M17).
- [ ] Submeter o protocolo ao CEP da FGV — **caminho crítico**.
- [ ] Verificar se a FGV exige convênio formal com cada empresa ou se um termo padrão basta.
- [ ] Especificar o relatório comparativo trimestral — é a contrapartida, e precisa existir antes do primeiro trimestre de coleta.
- [ ] Confirmar com o CEP a redação que declara o sorteio sem revelar a hipótese.
