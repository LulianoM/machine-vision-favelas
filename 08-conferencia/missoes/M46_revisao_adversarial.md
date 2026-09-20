# M46 — Revisão adversarial: o revisor mais hostil possível

Executada em 2026-08-21.

> **Esta missão não é uma lista de objeções hipotéticas.** Rodei os testes que o revisor rodaria. **Três deles derrubam afirmações que estão hoje no dossiê e no rascunho do paper.** As correções estão aqui, e são executáveis.

---

## Resumo executivo — o que quebrou

| # | Achado | Gravidade | Consequência |
|---|---|---|---|
| **R1** | **A correlação de −0,89 é artefato aritmético.** Var_M como ruído puro independente produz r = −0,979 | 🔴 **Fatal** | O estimando principal muda. H1 tem de ser reescrita |
| **R2** | **A variável chamada "classe" nas M02–M43 é escolaridade** (`i_education`: Low/Middle/High) | 🔴 **Fatal para o rótulo** | Toda menção a "classe social" na validação de terceiros está errada |
| **R3** | **O achado é dependente do item.** Llama-3-70B rastreia a variância humana perfeitamente em felicidade (incl. **+1,03**) | 🟠 **Grave** | Aciona a condição de derrubada da 7.6 da M44 |
| **R4** | A regra de triagem da 8.2 (M45) é **circular** na formulação atual | 🟠 **Grave** | A contribuição gerencial cai ou muda |
| **R5** | A falha **diminui monotonamente com a geração do modelo**: 0,056 → 0,116 → 0,173 | 🟡 Séria | Convida a objeção "isso se resolve sozinho até 2027" |
| **R6** | Célula `NA` de escolaridade entrava silenciosamente como 16º estrato | 🟡 Higiene | Números da M43 mudam na terceira casa |

**Nada disso mata o projeto.** Dois dos seis (R1 e R3) tornam o paper *melhor*, porque substituem uma afirmação frágil por uma verificável. Mas todos exigem reescrita antes de 19 de novembro.

---

## R1 — A objeção que mata o paper na sessão de perguntas

### A objeção, como ela seria feita

> *"Seu resultado principal é a correlação entre a variância da população e o log da razão de variâncias. Mas ln VR = ln(Var_M) − ln(Var_H). Se Var_M é aproximadamente constante, então ln VR ≈ constante − ln(Var_H), e a correlação com Var_H é **negativa por construção**. Você não mediu nada. Você mediu que x é correlacionado com −x."*

### O teste

Rodei em `d_polpos`, o item de maior amplitude, com as 15 células reais:

| Cenário para Var_M | r(Var_H, ln VR) |
|---|---:|
| **Observado (Var_M real)** | **−0,977** |
| Var_M fixado na constante 5,633 | −0,987 |
| **Var_M como ruído gaussiano independente** (2000 simulações, mesma média e mesmo dp) | **−0,979** (IC 5–95%: −0,989 a −0,966) |
| Var_M = 1,4 × Var_H (o modelo acompanha perfeitamente) | −0,326 |

> 🔴 **O valor observado está dentro do intervalo do ruído puro.** A correlação de −0,977 é **indistinguível** do que se obteria se a variância do modelo fosse gerada por um gerador de números aleatórios sem qualquer relação com a população.

A correlação não é falsa — é **vazia**. Ela só informa que `CV(Var_M) << CV(Var_H)`, e informa isso de forma comprimida e não interpretável.

### A correção — o estimando que sobrevive

**A inclinação da regressão de Var_M sobre Var_H, testada contra o nulo informativo de 1,0.**

Se o modelo reproduzisse a dispersão da população, a inclinação seria 1. Se ignorasse o estrato completamente, seria 0. O número é interpretável, tem unidade, e **não é mecanicamente determinado**.

### O resultado corrigido — 3 modelos × 3 itens, IC bootstrap de 4000 réplicas

Células `NA` de escolaridade excluídas. 15 células por item. Mínimo de 50 observações.

| Modelo | Item | n | Inclinação | IC 95% | Exclui 0? | **Exclui 1?** |
|---|---|--:|--:|:--:|:--:|:--:|
| FA-GPT-3 | felicidade | 15 | +0,515 | [+0,261, +0,854] | sim | **sim** |
| FA-GPT-3 | posição política | 15 | +0,037 | [−0,064, +0,109] | não | **sim** |
| FA-GPT-3 | participação religiosa | 15 | +0,038 | [−0,085, +0,236] | não | **sim** |
| FA-Mixtral-8x7B | felicidade | 15 | +0,366 | [+0,154, +0,481] | sim | **sim** |
| FA-Mixtral-8x7B | posição política | 15 | +0,124 | [−0,028, +0,408] | não | **sim** |
| FA-Mixtral-8x7B | participação religiosa | 15 | −0,070 | [−0,236, +0,107] | não | **sim** |
| FA-Llama-3-70B | felicidade | 15 | **+1,031** | [+0,753, +1,195] | sim | **NÃO** |
| FA-Llama-3-70B | posição política | 15 | +0,168 | [+0,019, +0,497] | sim | **sim** |
| FA-Llama-3-70B | participação religiosa | 15 | +0,031 | [−0,073, +0,117] | não | **sim** |

> ⭐ **A afirmação que sobrevive, e é forte:** em **8 de 9** combinações modelo × item, o intervalo de confiança da inclinação **exclui 1,0**. A variância sintética não acompanha a variância da população — e agora isso está dito de uma forma que um estatístico pode verificar e refutar.

### O que muda no texto

| Onde | De | Para |
|---|---|---|
| **H1** | "correlação negativa entre variância da população e razão de variâncias" | **"a inclinação de Var_M sobre Var_H é menor que 1"** |
| **Figura 1 (M43)** | já estava certa — eixo y é Var_M, não ln VR | mantida; **acrescentar a reta ajustada e sua inclinação em cada painel** |
| **Tabela 2 (M43)** | "Correlação (H1)" | **"Inclinação (H1), nulo = 1,0"** |
| **5.5 (M42)** | `ln VR` como desfecho primário | `ln VR` vira **descritivo**; a inclinação vira primário |
| **Abstract (M40)** | qualquer número de correlação | substituir pela inclinação e pelo IC |

> **A Figura 1 da M43 já estava certa pelo motivo errado.** A M43 escolheu plotar Var_M em vez de ln VR porque a faixa horizontal era visualmente mais forte. **Acontece que era também a única escolha estatisticamente defensável.** Sorte, e vale registrar como sorte.

---

## R2 — A variável está com o nome errado desde a M02

### O que o arquivo diz

O campo do perfil no pacote de Boelaert é `País§Ano§Idade§Sexo§_§Ocupação§EstadoCivil`. As missões anteriores leram o quinto campo como **classe social**. O arquivo `data/WVS/wvs-levels.csv` do próprio pacote define:

```
i_education, 1, Low
i_education, 2, Middle
i_education, 3, High
```

E as colunas do arquivo humano são `i_country, i_sex, i_marstat, i_education, i_employment, i_age`. **Não existe variável de classe ou renda no conjunto.**

> 🔴 **O quinto campo é escolaridade.** Low/Middle/High são níveis educacionais, não classes sociais.

### A gravidade real

Menor do que parece, e maior do que é confortável.

**Menor** porque escolaridade é um estratificador legítimo e, para o argumento do T2, **provavelmente melhor que renda**: a hipótese de fundo é sobre representação no corpus de treinamento, e o corpus é texto escrito — escolaridade é um preditor mais direto de quem escreve na internet do que renda.

**Maior** porque:
1. O dossiê publicado diz "classe" e está errado.
2. A M10 reportou um "gradiente de classe de 0,086 unidades logarítmicas" — é **gradiente de escolaridade**.
3. A ponte narrativa com a POF brasileira, que estratifica por **renda**, deixa de ser direta. **A evidência de terceiros e a coleta própria passam a estratificar por variáveis diferentes.**

### A correção

- Substituir "classe" por **"escolaridade"** em toda referência ao dado de Boelaert — dossiê, M02, M09, M10, M43.
- No paper, a Seção 4 (evidência sem modelo) declara: *"strata defined by educational attainment"*.
- **Na Seção 3, acrescentar uma frase** reconhecendo que a evidência motivadora estratifica por escolaridade e a coleta confirmatória por renda e região, e por que isso é aceitável: a hipótese é sobre representação no corpus, e ambas as variáveis são proxies dela.
- ⚠️ **Ou** acrescentar escolaridade como terceiro eixo dos estratos da POF — a M41 já cruza renda × região × escolaridade em 60 células. **A ponte já existe no desenho; só não estava explicitada.**

---

## R3 — O achado é do item, não da população (a condição de derrubada da 7.6 disparou)

### A objeção

> *"Özkan mostra que a severidade do colapso é previsível a partir de propriedades do item. Você está atribuindo à população uma estrutura que é do item. Seu próprio dado mostra isso."*

### Ele tem razão, e o dado é meu

Reagrupando a tabela do R1 por item:

| Item | Escala | Inclinação mediana (3 modelos) | Leitura |
|---|--:|--:|---|
| **Felicidade** | 4 pontos | **+0,515** | O modelo **rastreia parcialmente**; Llama-3 rastreia **totalmente** |
| Posição política | 10 pontos | +0,124 | Quase não rastreia |
| Participação religiosa | 7 pontos | +0,038 | **Não rastreia** |

> 🟠 A amplitude entre itens (**+0,52 contra +0,04**, treze vezes) é **maior** que a amplitude entre modelos (+0,056 contra +0,173, três vezes).

A M44 escreveu a condição de derrubada da 7.6 assim: *"If the stratum coefficient does not survive item fixed effects, the structure is on the item side, not the population side — which is the finding already in the literature, and not ours."*

**Escrevi essa condição em antecipação e ela disparou no meu próprio dado motivador.**

### Três saídas, e a que recomendo

| Saída | Avaliação |
|---|---|
| Ignorar e reportar só a média entre itens | ❌ Desonesto, e o revisor tem os dados públicos |
| Reportar e admitir que o achado é do item | ⚠️ Honesto, mas então o paper repete Özkan |
| ⭐ **Reformular: a interação é o achado** | ✅ **Recomendada** |

**A reformulação.** A pergunta deixa de ser *"o modelo rastreia a dispersão da população?"* e passa a ser:

> **Em quais itens o rastreamento falha, e a falha é prevista pela largura da escala do item?**

Três pontos sugerem — e só sugerem, com n=3 — que **a inclinação decresce com o número de opções de resposta**: 4 opções → +0,52; 7 opções → +0,04; 10 opções → +0,12. Não é monótono e não é testável com três itens.

**Consequência de desenho, e é grande:** a coleta brasileira precisa de **variação deliberada na largura da escala**, com itens de consumo em escalas de 3, 5, 7 e 11 pontos medindo a mesma quantidade subjacente. Isso é um braço fatorial novo, e **não estava no pré-registro da M12**.

> ⭐ Se a interação escala × estrato se confirmar, o paper fica **mais forte** que a versão original: passa de "o modelo erra a dispersão" para **"o erro de dispersão é uma função da granularidade que você pede ao modelo"** — que é acionável e não está publicado.

---

## R4 — A regra de triagem é circular

### A objeção

> *"Seu passo 1 é 'compute a variância do desfecho dentro de cada segmento usando dado de pesquisa ponderado existente'. Se eu tenho isso, já tenho a resposta. Por que eu compraria o painel sintético?"*

**Procede.** A regra da 8.2 da M45, como está escrita, exige exatamente o dado que o painel sintético deveria substituir.

### As duas defesas possíveis, e por que só uma funciona

**Defesa A — variância é propriedade do segmento, não do item.** *"Você mede a variância de alguns desfechos conhecidos por segmento e usa isso para prever a fidelidade em desfechos novos nos mesmos segmentos."*

🔴 **Refutada pelo próprio dado.** O R3 mostra que a variância depende fortemente do item: os mesmos 15 segmentos produzem inclinações de +0,52 a +0,04 conforme o item. **A fidelidade não é transportável entre desfechos dentro do mesmo segmento.**

**Defesa B — a triagem é sobre o modelo, não sobre o segmento.** ✅

O que é estável e barato de medir **uma vez** é a dispersão que o modelo produz — o CV da variância do modelo entre estratos foi de 0,045 no GPT-3, contra 0,347 na população. A regra útil não é "compare este segmento contra a variância fixa", é:

> **Peça ao modelo a distribuição para todos os seus segmentos. Calcule a dispersão *entre segmentos* das variâncias que ele devolveu. Se ela for muito menor que a dispersão entre segmentos que você espera na população, o modelo está devolvendo o mesmo espalhamento para todo mundo — e nenhuma comparação entre segmentos que você fizer com esse dado é confiável.**

**Isso não exige benchmark humano por desfecho.** Exige apenas uma expectativa de ordem de grandeza sobre quanto os segmentos diferem — que é o que o profissional já tem antes de encomendar a pesquisa. E é **inteiramente computável a partir da saída sintética**, o que é o requisito.

### A reescrita da 8.2

> **8.2 A diagnostic that requires no human benchmark**
>
> Query the model for all segments of interest. Compute the dispersion, across segments, of the variances the model returns. Compare it against the dispersion across segments you would expect in the population — an order-of-magnitude judgment, not an estimate.
>
> In our audit that ratio was [X]. **A model returning near-identical dispersion for every segment is not distinguishing between them, whatever the means suggest.** Segment-level conclusions drawn from such output are conclusions about the model, not about the market.
>
> The diagnostic is computed entirely from synthetic output. It does not tell the analyst whether any particular estimate is right. **It tells the analyst when the panel has stopped varying — which is the failure mode that produces confident, wrong segment recommendations.**

**É uma reivindicação menor que a da M45 e é a que se sustenta.** A M45 prometia dizer *quais* segmentos são não confiáveis; esta diz *quando o painel inteiro parou de discriminar*. Menos ambiciosa, verificável, e ainda responde a Brand, Israeli e Ngwe — só que com "não use para segmentos" em vez de "use nestes segmentos".

---

## R5 — "Isso se resolve sozinho até 2027"

### A objeção

Ordenando por data de lançamento:

| Modelo | Lançamento | Inclinação mediana |
|---|---|--:|
| GPT-3 | 2020 | **+0,056** |
| Mixtral-8x7B | dez. 2023 | **+0,116** |
| Llama-3-70B | abr. 2024 | **+0,173** |

> *"Sua inclinação triplicou em quatro anos e o modelo mais novo rastreia perfeitamente num dos três itens. Você está documentando uma limitação que está desaparecendo, e a conferência é em 2027."*

### A resposta honesta

**Três pontos não são uma tendência**, e a ordenação por data de lançamento confunde geração com arquitetura, tamanho e receita de alinhamento. Mas a direção é real e **não pode ser omitida** — o pacote é público e o revisor pode rodar isso em vinte minutos, como eu rodei.

**A resposta que funciona tem três partes:**

1. **Reportar a tendência explicitamente.** Omitir é o único erro fatal aqui.
2. **+0,173 continua sendo um sexto de 1,0.** Uma melhora de três vezes a partir de uma base catastrófica ainda é inadequada. O painel sintético que devolve 17% da variação entre segmentos não serve para decisão de segmento.
3. ⭐ **Transformar em desenho.** O T2 audita modelos de fronteira de 2026–2027, não de 2020. **A pergunta "a propriedade persiste na fronteira atual?" vira uma hipótese pré-registrada com data**, e a resposta é uma contribuição em qualquer direção. Se persistir, é um resultado forte. Se tiver desaparecido, é o **primeiro paper a documentar quando desapareceu** — o que também vale a conferência.

**Isso exige incluir na coleta um modelo antigo como âncora**, para que a comparação temporal seja medida e não citada.

---

## R6 — Os outros seis ataques, com veredito

| # | A objeção | Veredito |
|---|---|---|
| **R6.1** | *"Sua evidência é opinião política em cinco países com GPT-3; sua afirmação é consumo no Brasil com modelos de 2027. Domínios diferentes."* | ✅ **Procede parcialmente.** A M43 já manda a legenda dizer que é motivadora. **Reforçar: a Figura 1 é a razão de fazer o estudo, não o resultado dele.** A Seção 4 tem de se chamar *"Motivating Evidence"*, não *"Model-Free Evidence"* |
| **R6.2** | *"Você não oferece mecanismo. Por que a variância seria fixa?"* | ⚠️ **Procede e não tem resposta.** A honesta é declarar que o paper é descritivo e que o mecanismo é questão aberta. **Especular sobre RLHF sem testar é pior que silêncio** |
| **R6.3** | *"n = 15 células por item."* | ⚠️ Procede. Mitigado pelo bootstrap, que já está na tabela do R1. **Reportar sempre com IC, nunca só com ponto** |
| **R6.4** | *"A célula de escolaridade baixa dos EUA tem n = 105."* | ✅ Já registrado na M43. **Manter e marcar na figura** |
| **R6.5** | *"Sua defesa da invariância a deslocamento (5.3) supõe que a superdispersão do caminho *describe* é constante entre estratos. Se ela variar por estrato, não é deslocamento."* | 🟠 **Procede, e é uma falha real na 5.3.** A defesa da M42 é válida só sob homogeneidade não testada. **Correção: acrescentar teste explícito de que a razão de dispersão do caminho não varia com o estrato, e declará-lo como pressuposto verificável** |
| **R6.6** | *"Célula `NA` de escolaridade entrou como 16º estrato nas contas anteriores."* | ✅ **Procedia. Corrigido nesta missão** — todos os números do R1 são com `NA` excluído |

---

## A ameaça que ficou sem subseção de robustez (herança da M44)

A M44 pediu que esta missão verificasse se alguma ameaça ficou sem destino. **Duas ficaram:**

1. **A dependência do item quanto à largura da escala** (R3). A 7.6 controla a existência de resposta normativamente correta — **não controla número de opções**. É acréscimo obrigatório.
2. **A heterogeneidade da superdispersão entre estratos** (R6.5). Não há subseção; a 7.3 testa entre caminhos, não dentro de estratos.

---

## Verificação de citações (herança da M42)

A M42 escreveu a seção sem nomes, deixando a conferência para esta missão. **Estado:**

| Afirmação na M42 | Fonte | Estado |
|---|---|---|
| Degeneração amostral, resposta idêntica em repetição | Boelaert et al. | ✅ Pacote de replicação verificado em disco |
| Superdispersão do caminho *describe*, razões 0,4–0,56 → 1,26–1,37 | Özkan | ⚠️ **[NÃO VERIFICADO]** — não reconferido nesta missão |
| Viés de recência de até 20× | — | ⚠️ **[NÃO VERIFICADO]** |
| Tendência sistemática ao "não" em inglês, alemão e polonês | — | ⚠️ **[NÃO VERIFICADO]** |
| Deriva de distribuição entre meses | — | ⚠️ **[NÃO VERIFICADO]** |
| Painel de conveniência descrito pelos próprios autores como enviesado | Brand, Israeli e Ngwe | ✅ Verificado na M02 |

> ⚠️ **Quatro afirmações permanecem sem verificação de venue e ano.** Esta missão gastou seu orçamento nos testes estatísticos, que eram mais letais. **A M47 tem de fechar essas quatro antes que qualquer uma entre no texto.**

---

## O que esta revisão não conseguiu atacar

Registro de honestidade, porque uma revisão adversarial que só encontra o que sabe procurar não é adversarial:

- **Não testei a regra de triagem numericamente** — a reformulação do R4 é argumento lógico, não simulação. A M45 pediu validação *leave-one-stratum-out* e ela **não foi feita**.
- **Não verifiquei se algum dos oito premiados de 2026 já reporta inclinação em vez de correlação** — se reportarem, a "correção metodológica" do R1 é menos original do que parece.
- **Não testei o caminho NTP** (`NTP-GPT-4T`), que está em disco e é o modelo mais recente do pacote. **É o teste mais óbvio que sobrou** e o revisor vai fazê-lo.

---

## Pendências geradas

- [ ] **Rodar `NTP-GPT-4T` com o estimando de inclinação.** É a lacuna mais visível desta missão e o dado está em disco.
- [ ] Corrigir "classe" → "escolaridade" no dossiê, na M02, M09, M10 e M43.
- [ ] Reescrever H1 no M40 e a Tabela 2 do M43 em termos de inclinação com nulo 1,0.
- [ ] Reescrever a 8.2 do M45 conforme o R4.
- [ ] Acrescentar largura de escala como fator do desenho e como controle na 7.6.
- [ ] Acrescentar subseção de robustez para a heterogeneidade da superdispersão (R6.5).
- [ ] Incluir um modelo antigo como âncora temporal na coleta (R5).
- [ ] Renomear a Seção 4 para *"Motivating Evidence"*.
- [ ] **Fechar as quatro citações [NÃO VERIFICADO]** da tabela acima.
- [ ] **Emendar o pré-registro da M12** — o fator de largura de escala e o estimando de inclinação são mudanças materiais.
- [ ] **M47 herda:** responder R1 a R6 dentro do texto. **R1, R2 e R4 não são "responder" — são reescrever.**
