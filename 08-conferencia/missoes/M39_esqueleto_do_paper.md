# M39 — Esqueleto do paper do T2, medido nos vencedores

Executada em 2026-08-21. Abre o Bloco F. **Medi os oito papers premiados de 2026 em vez de inventar o formato.**

---

## Resumo

1. **⭐ A pendência de formato aberta desde a M01 está empiricamente resolvida.** Um vencedor do prêmio Tellis de 2026 tem **7 páginas e 1.802 palavras**, e é explicitamente rotulado **"Extended Abstract"**. Um vencedor do Rao tem **122 páginas**. **A AIM aceita as duas coisas, e as duas ganham.**

2. **Isso reordena o plano de 90 dias.** O entregável de 19 de novembro passa a ser um **resumo estendido de 8 a 12 páginas** — que é literalmente o primeiro terço do paper completo. Nada de trabalho se perde, e o prazo deixa de ser o risco principal.

3. **A estrutura modal é clara e replicável**, e tem duas convenções que valem ouro: **evidência sem modelo antes da regressão**, e **robustez como seção numerada com várias subseções, não apêndice**.

---

## 1. A medição

Oito papers premiados de 2026, todos baixados da página oficial da conferência.

| Paper | Prêmio | Páginas | Palavras | Tabelas | Figuras |
|---|---|---:|---:|---:|---:|
| **Contigiani et al.** — *Experimentation in the Age of Generative AI* | Tellis | **7** | **1.802** | 0 | 0 |
| Dai, Li e Telang — *Algorithmic Illusion?* | Rao | 23 | 7.201 | 15 | 7 |
| Zhuoyan Ma et al. — *Collaborate to Elevate* | Hanssens | 33 | 10.115 | 9 | 8 |
| Pan Li — *All Explanations are Wrong* | Tellis | 37 | 10.894 | 11 | 3 |
| Salas — *AI-Mediated Marketing* | Hanssens | 37 | 10.081 | 7 | 8 |
| Grumbach et al. — *Innovation-Diversity Tradeoff* | Hanssens | 45 | 13.750 | 5 | 1 |
| Binglu Wang — *Human–AI Collaboration in Science* | Rao | 57 | 11.579 | 0 | 4 |
| Hoong e Dreyfuss — *Calibrated Coarsening* | Rao | **122** | **35.093** | 49 | 48 |

**Mediana: 37 páginas, 10.500 palavras, 8 tabelas, 6 figuras.**
**Amplitude: de 7 a 122 páginas.** Fator de dezessete.

### O que isso significa

> **A AIM não impõe padrão de extensão.** E o extremo curto **não é penalizado** — o paper de 7 páginas ganhou um dos quatro prêmios, competindo com um de 122.

O de Contigiani não tem seção numerada, tabela nem figura. É prosa corrida com referências, rotulada como resumo estendido. **Ganhou o prêmio Cheryl & Gerard Tellis.**

⚠️ **Ressalva honesta:** isso é evidência sobre o que é **aceito e premiado**, não sobre o que o formulário **exige**. O formulário segue inacessível (M01, M36). **Mas a evidência é forte o bastante para planejar em cima dela.**

---

## 2. A decisão de formato

| | Resumo estendido, 8–12 pp | Paper completo, ~35 pp |
|---|---|---|
| Precedente de prêmio | ✅ Contigiani, 2026 | ✅ Cinco dos oito |
| Viável em 90 dias com as pendências abertas | ✅ **Sim** | ⚠️ Apertado |
| Trabalho perdido se sobrar tempo | Nenhum — vira a introdução do completo | — |
| Risco de o prazo escorregar | Baixo | **Alto** |

> **Recomendação: escrever o resumo estendido como entregável de 19 de novembro.** Ele é o primeiro terço do paper completo, que segue sendo escrito para a ISMS de janeiro e para o periódico (M38).

Isso **desarma o maior risco do cronograma** identificado na M12 — a coleta e a análise consumirem outubro e sobrar pouco para escrever.

---

## 3. A estrutura modal, medida

Extraí a numeração de seções dos dois papers de formato mediano e premiados:

**Zhuoyan Ma (Hanssens, 33 pp):** 1 Introdução · 2 Literatura (3 subseções) · 3 Métodos (contexto, dados) · 4 Arcabouço empírico (estratégia de pareamento, especificação) · 5 Resultados (efeito principal + 2 de heterogeneidade) · **6 Robustez** · 7 Discussão

**Dai, Li e Telang (Rao, 23 pp):** 1 Introdução · **2 Dados e evidência sem modelo** · 3 Análise de regressão (uma subseção por desfecho) · 4 Análise multimodal · 5 Efeitos heterogêneos (5 subseções, incluindo **grupos de controle alternativos**) · **6 Robustez e explicações alternativas (5 subseções)**

### As três convenções que valem copiar

**⭐ Evidência sem modelo antes da regressão.** Dai dedica a seção 2.2 a mostrar o padrão bruto antes de qualquer estimação. **É persuasivo e é honesto** — o leitor vê o fenômeno antes de ver a especificação. O T2 tem isso pronto: a correlação de −0,89 entre variância humana e razão de variância (M10) é evidência sem modelo.

**⭐ Robustez é seção numerada, com subseções.** Não é apêndice. Dai tem cinco subseções de robustez e explicações alternativas; Ma dedica a seção 6 à validação de tendências pré-tratamento. **Num fórum sem discussants (M34), a robustez tem de estar no corpo.**

**⭐ Heterogeneidade tem seção própria.** Não é parágrafo. Nos dois casos ocupa a seção mais longa depois dos resultados principais.

---

## 4. O esqueleto do T2

Versão **resumo estendido**, com orçamento de palavras. O paper completo expande cada seção sem mudar a ordem.

| # | Seção | Palavras | O que entra |
|---|---|---:|---|
| — | **Título e abstract** | 200 | Nome, afiliação, e o abstract que a M40 vai escrever. **Teste da M35: funciona com a afiliação coberta?** |
| **1** | **Introdução** | 900 | O problema em três parágrafos: pesquisa de mercado sintética está sendo vendida e usada; a literatura sabe que a média acerta e a variância erra; **ninguém sabe se o erro tem estrutura**. Fecha com o achado principal em números. |
| **2** | **O que se sabe** | 700 | Curto e cirúrgico. Argyle e a fidelidade algorítmica; Bisbee e o colapso; Brand, Israeli e Ngwe com WTP de sinal trocado; **Boelaert et al. e a afirmação de aleatoriedade que o T2 contesta**. Uma frase para cada. |
| **3** | **Contexto e dados** | 700 | POF/PNAD, os estratos, o desenho L3 com 60 células, a fixação do universo. **Aqui o Brasil aparece como escolha de desenho** — os 39% contra 15% (M05). |
| **4** | **Evidência sem modelo** ⭐ | 600 | A correlação de −0,89. O gráfico de variância humana contra `ln VR`. **Antes de qualquer especificação.** |
| **5** | **Método** | 800 | Caminhos de extração, versionamento, as métricas da M07. **É a seção que O'Leary lê** (M33/M34). Densa e precisa. |
| **6** | **Resultados** | 800 | H1 primeiro. Depois o gradiente. Tabela principal com a estabilidade do coeficiente entre especificações. |
| **7** | **Robustez** ⭐ | 700 | Placebo temporal, braço PNAD, linha de base supervisionada, grade de temperatura, três formulações de renda. **Seção numerada, não apêndice.** |
| **8** | **O que isso custa** | 500 | **A curva de cobertura decrescente em *k*.** É a figura principal e o parágrafo de implicação de decisão que a M33 exige. |
| **9** | **Limitações e discussão** | 400 | Confundidor temporal e como foi tratado; escopo declarado; o que não se pode afirmar. |
| — | **Referências** | — | |
| | **Total** | **≈ 6.300** | **10 a 12 páginas** |

### Figuras e tabelas — o mínimo que carrega o argumento

| # | Peça | Papel |
|---|---|---|
| **Figura 1** | Variância humana × `ln VR`, com a reta e o r = −0,89 | **A evidência sem modelo** |
| **Figura 2** | **Curva de cobertura decrescente em *k*** | **A figura do paper** (M07) |
| Tabela 1 | Estratos, N por célula, descartes reportados | Transparência amostral |
| Tabela 2 | Coeficiente principal entre 4 especificações, incluindo controle de deriva | **A estabilidade é o argumento** (M09) |
| Tabela 3 | Métricas por estrato: razão de variância, Wasserstein, TV, ESS | Panorama |

Cinco peças. A mediana dos vencedores é 8 tabelas e 6 figuras — mas eles têm 37 páginas. **Para 12 páginas, cinco é o teto.**

---

## 5. O que NÃO entra

| Fora | Por quê |
|---|---|
| Revisão de literatura longa | A gramática é de working paper de marketing science, não de dissertação (M01) |
| **Qualquer aparato foucaultiano** | Dois textos, dois públicos (M31) |
| Sentimento como desfecho | Flutua 6,7× mais que a própria menção (M21) — é do T1, e nem lá sustenta tese |
| Discussão de implicações teóricas amplas | Espaço é caro; a implicação **de decisão** vale mais (M33) |
| Apêndice extenso | Num resumo estendido, não há |
| Pedido de desculpas pelo contexto brasileiro | O Brasil é ativo (M35) |

---

## 6. A ordem de escrita

Não é a ordem de leitura. Proposta, para as semanas 9 a 11 do cronograma:

1. **Seção 4** (evidência sem modelo) — já existe, é a correlação medida.
2. **Seção 5** (método) — já está inteira nos pré-registros da M12.
3. **Seção 3** (dados) — já está na M05.
4. **Seção 6 e 7** (resultados e robustez) — dependem da coleta.
5. **Seção 8** (o que custa) — depende de 6.
6. **Seção 1 e 2** (introdução e literatura) — **por último**, quando se sabe o que o paper de fato mostra.
7. **Abstract** — por último de todos. É a M40.

> **Três das nove seções já estão escritas em substância**, espalhadas pelos arquivos de missão. **O paper não começa do zero.**

---

## Pendências geradas

- [ ] Confirmar por e-mail se o formulário aceita resumo estendido — a evidência é forte, a confirmação é barata (M36).
- [ ] Verificar se há limite de páginas declarado em algum lugar do formulário.
- [ ] Ler o resumo estendido de Contigiani inteiro como modelo de gênero — **7 páginas que ganharam US$ 5.000 merecem leitura atenta**.
- [ ] Ler o *AI-Mediated Marketing* de Salas — formato mediano, mesma família de tema, e é âncora do T1.
- [ ] Decidir se o paper completo é escrito em paralelo ou depois da submissão.
- [ ] **M40 herda:** o abstract precisa caber em 200 palavras e passar no teste da afiliação coberta.
- [ ] **M43 herda:** o plano de figuras está esboçado aqui com cinco peças; a M43 detalha cada uma.
