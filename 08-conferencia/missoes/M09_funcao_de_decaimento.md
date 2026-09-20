# M09 — Função de decaimento: forma funcional, estimador, teste de não-linearidade

Executada em 2026-08-21. Especificação ancorada na inspeção direta do dado de Boelaert et al., agora em disco.

---

## Resumo do que esta missão muda

1. **Descobri por que Boelaert et al. viram aleatoriedade, e o motivo é de resolução, não de natureza.** O dado deles tem **três níveis de classe** (Low, Middle, High) e **quatro itens substantivos**. A afirmação de que "o viés varia aleatoriamente de um tópico para o outro" é uma observação sobre **n = 4 tópicos**. Com três níveis na variável explicativa e quatro tópicos, nenhuma função de decaimento é detectável, ainda que exista.

2. **O T2 tem entre duas e três vezes mais resolução na variável que importa.** Sete classes de rendimento da POF contra três de classe subjetiva; dezenas de categorias de consumo contra quatro atitudes. Isso deixa de ser vantagem retórica e vira argumento de poder estatístico, que é o que a AIM entende.

3. **⚠️ O pré-teste precisa mudar de desenho.** A célula de classe baixa nos Estados Unidos tem **105 observações**, contra **1.055 no México**. Uma comparação México contra Estados Unidos está desbalanceada em 10 para 1 exatamente na célula que carrega a hipótese. Substituir por comparação contínua entre os cinco países.

---

## 1. O que a inspeção do dado revelou

### Distribuição de classe por país, em `subpops.csv`

| País | Low | Middle | High | NA | Total |
|---|---:|---:|---:|---:|---:|
| **México** | **1.055** | 2.406 | 1.326 | 24 | 4.811 |
| Alemanha | 524 | 3.274 | 1.770 | 50 | 5.618 |
| Rússia | 324 | 2.578 | 2.949 | 32 | 5.883 |
| Austrália | 197 | 2.423 | 2.532 | 130 | 5.282 |
| **Estados Unidos** | **105** | 2.789 | 2.454 | 39 | 5.387 |
| **Total** | 2.205 | 13.470 | 11.031 | 275 | 26.981 |

687 subpopulações distintas, formadas pelo cruzamento de país × ano × faixa etária × sexo × classe × ocupação × estado civil.

### Os itens

Doze variáveis, das quais **oito são de identidade** (`i_surveyyear`, `i_country`, `i_birth`, `i_age`, `i_sex`, `i_education`, `i_employment`, `i_marstat`) e apenas **quatro são substantivas**:

| Item | Conteúdo |
|---|---|
| `d_happy` | Felicidade autodeclarada |
| `d_trust` | Confiança generalizada nas pessoas |
| `d_religiousp` | Participação religiosa em ritos |
| `d_polpos` | Autoposicionamento na escala esquerda-direita |

### As três consequências

**Primeira.** A afirmação central de Boelaert et al. — o viés *"randomly varies from one topic to the next"* — descreve a variação entre **quatro** tópicos. Isso não é um defeito do trabalho deles, cujo objetivo era outro, mas **limita fortemente o que se pode concluir sobre estrutura**. Quatro pontos não sustentam nem a afirmação de aleatoriedade nem a de estrutura.

**Segunda.** Com três níveis de classe, o modelo mais flexível estimável é uma saturação com duas dummies. **Não há grau de liberdade para testar forma funcional.** Um decaimento côncavo, convexo ou com limiar é indistinguível de linear nesse dado. A pergunta da M04 — *qual noção de distância prevê o decaimento* — é inrespondível ali por construção.

**Terceira.** A classe deles é **subjetiva e autodeclarada** (Low/Middle/High), não uma faixa de renda medida. No Brasil, autoclassificação de classe é notoriamente comprimida em direção a "média". A POF dá faixa de rendimento **medida e ponderada**, em sete níveis. É uma variável melhor, não apenas mais granular.

### O que isso faz com o posicionamento do T2

O argumento deixa de ser "eles olharam opinião, eu olho consumo" e passa a ser:

> **A estrutura pode existir e ter passado despercebida por falta de resolução.** Três níveis de classe autodeclarada e quatro itens não permitem detectar decaimento. Sete faixas de rendimento medidas e dezenas de categorias de consumo permitem.

Isso é mais forte, mais específico e verificável por qualquer revisor que abra o pacote de replicação — que é público.

### Correção no pré-teste da M08

A comparação México contra Estados Unidos está comprometida: 1.055 contra 105 na célula de classe baixa. **Desenho substituto:**

> Estimar o gradiente de classe **por país** nos cinco países e regredir a inclinação estimada contra um índice de centralidade do país (por exemplo, participação da língua no corpus, ou a própria medida de Dunn et al. para aquele país). Cinco pontos ainda é pouco, mas é uma tendência, não uma comparação binária desbalanceada.

Como robustez, comparar México contra **Alemanha** (Low = 524), que é a célula de classe baixa mais próxima entre os países centrais.

---

## 2. Notação e estrutura de dados

```
E(s, q, m, p)   desfecho de erro
   s = estrato          (7 classes de renda marginais; 20/60/180 células cruzadas)
   q = item             (categoria de consumo)
   m = modelo           (grade da M06)
   p = caminho          (P1 describe · P2 logprob · P3 PPA · P4 agregação)

D(s)            distância, nas três medidas da M04:
   D1′(s)  erro factual de caracterização do estrato   [primária, M06]
   D3(s)   CFst cultural                                [secundária]
   Dd(s)   pegada digital reformulada                   [terciária]

X(s)            controles: N da célula, participação populacional,
                perplexidade da descrição da persona, região, urbano/rural

C(q)            complexidade do construto (RD4)
Δ(q)            taxa histórica de mudança da categoria (controle de deriva, M08/A1)
```

Estrutura **classificada cruzada**: estratos e itens não são aninhados um no outro. Isso obriga erro padrão agrupado nas duas dimensões.

---

## 3. Forma funcional

Nenhuma teoria disponível fixa a forma. A M02 sugere hierarquia de dificuldade de momentos; a M04 sugere decaimento com cobertura; nenhuma das duas prediz curvatura. **Portanto: uma especificação primária simples e pré-registrada, mais um teste de não-linearidade também pré-registrado.**

### F1 — Especificação primária, confirmatória

```
g(E_sqmp) = β₀ + β₁·D1′(s) + γ′X(s) + δ·Δ(q) + α_m + α_p + α_q + ε_sqmp
```

- `α_m`, `α_p`, `α_q` são efeitos fixos de modelo, caminho e item.
- `δ·Δ(q)` é o controle de deriva temporal exigido pela ameaça A1.
- **`β₁` é o parâmetro da RD2.** Sinal predito: positivo (mais distância, mais erro).

### A transformação `g(·)`

Depende da métrica, e precisa ser declarada por desfecho:

| Desfecho (M07) | Domínio | `g(·)` | Estimador |
|---|---|---|---|
| `ln VR` (razão de variância) | ℝ | identidade | MQO |
| `TV`, `1 − A_Wass` | [0, 1] | **logito fracionário** | GLM quase-binomial com ligação logito |
| `KS` | [0, 1] | logito fracionário | idem |
| `ESS/k` | (0, 1] | logito fracionário | idem |
| `Cobertura` | {0,1} por célula | — | logístico |

Usar MQO sobre desfecho limitado em [0,1] produz predição fora do suporte e heterocedasticidade previsível. **O GLM fracionário quase-binomial é o padrão para proporção como desfecho contínuo e não exige que os dados sejam contagens.**

**Desfecho primário declarado: `ln VR`.** É o que isola o fenômeno, é irrestrito, e admite MQO — o que mantém a especificação principal simples e legível na apresentação de 12 minutos.

### F2 — Teste de não-linearidade, pré-registrado

```
g(E) = β₀ + s(D1′) + γ′X + δ·Δ(q) + α_m + α_p + α_q + ε
```

com `s(·)` **spline cúbico restrito com 4 nós**, posicionados nos percentis **5, 35, 65 e 95** da distribuição de `D1′` — locação padrão de Harrell, fixada a priori para não haver escolha pós-hoc.

> **Teste:** Wald conjunto sobre os termos não-lineares do spline. Se rejeitar, reporta-se a forma estimada e a especificação primária passa a ser a spline. Se não rejeitar, mantém-se F1 e reporta-se o teste como evidência de linearidade.

Três formas concorrentes a inspecionar visualmente no gráfico da spline, com interpretação distinta:

| Forma | Leitura substantiva |
|---|---|
| **Linear** | A cobertura degrada proporcionalmente à distância |
| **Côncava (satura)** | Existe um piso de fidelidade; abaixo de certa cobertura o modelo já está tão errado quanto pode ficar |
| **Convexa com limiar** | Há uma região central segura e um colapso abrupto fora dela. **Seria o achado gerencialmente mais útil**, porque define uma fronteira de uso |

O limiar é a forma mais interessante e a menos provável de ser detectada com pouca resolução — mais um motivo pelo qual as sete classes da POF importam.

### F3 — Interação complexidade × periferia (RD4, hipótese da M02)

```
ln VR = … + β₄·[ D1′(s) × C(q) ] + …
```

`C(q)` ordenado a priori, do momento mais simples ao mais complexo, seguindo Brand et al. e a hierarquia de construtos de Ku et al. (M04):

```
1. incidência de consumo da categoria  (você compra?)
2. frequência                            (com que frequência?)
3. participação no orçamento            (quanto do total?)
4. escolha entre alternativas            (qual marca?)
5. disposição a pagar                    (quanto vale?)
```

Predição: `β₄ > 0` — o erro em estrato periférico é desproporcionalmente maior nos momentos complexos. **Este é o coeficiente mais publicável do desenho**, porque nenhum dos dois papers de origem o tem.

### F4 — Gradiente do split KNOWS/DOES (RD5, hipótese H3 da M03)

```
[ TV(P4) − TV(P1) ]_sqm = β₀ + β₅·D1′(s) + α_m + α_q + ε
```

O desfecho é a **vantagem do caminho *describe* sobre a agregação**, por célula. `β₅ > 0` significa que descrever ajuda mais onde o modelo sabe menos.

### F5 — Contraste com linha de base supervisionada (ameaça A7)

```
[ ln VR_LLM − ln VR_sup ]_sq = β₀ + β₆·D1′(s) + … + ε
```

Isola o **excesso de colapso atribuível ao modelo de linguagem**, acima do colapso que qualquer preditor estatístico exibe. Se `β₆ > 0`, o decaimento é específico de LLM. Se `β₆ ≈ 0` com `β₁ > 0`, o decaimento existe mas é propriedade de predição estatística em geral — e o T2 muda de tese sem perder valor.

O pacote de Boelaert et al. traz `data/Linear/` com predições de um modelo linear sob validação cruzada *leave-one-out*, e `ranger` entre as dependências em R. **Verificar se serve de gabarito antes de implementar do zero.**

---

## 4. Estimação

### Ponderação

Peso da célula `s` = **inverso da variância do benchmark**, `1 / Var[Ĥ_s]`, calculado com o peso amostral da POF. Atende diretamente à ameaça A4: célula mal estimada pesa menos, e o efeito de distância não é comprado com ruído de benchmark.

### Erro padrão

Duas fontes de dependência simultâneas: itens repetidos entre estratos, estratos repetidos entre itens.

1. **Agrupamento bidirecional** por estrato e por item (Cameron–Gelbach–Miller).
2. ⚠️ **Com poucos grupos, o agrupamento bidirecional é anticonservador.** No nível L1 há apenas 7 estratos. **Usar bootstrap selvagem agrupado (*wild cluster bootstrap*) com 9.999 réplicas** para todo teste no nível L1 e L2.
3. **A incerteza de primeira ordem continua sendo entre réplicas** (M07): paráfrase, semente de ordem, execução. O bootstrap é sobre réplicas, e o agrupamento entra dentro dele.

### Multiplicidade

Seis regras de decisão, três medidas de distância, quatro caminhos, vários modelos. Sem controle, alguma coisa aparece por acaso.

- **Confirmatório:** apenas `β₁` em F1 com desfecho `ln VR` e distância `D1′`. **Um teste, um alfa.** Tudo o mais é exploratório e rotulado como tal.
- **Secundárias pré-registradas** (F3, F4, F5): correção de **Benjamini–Hochberg** com FDR de 10%, declarada no pré-registro.
- **RQ2** (qual distância prevê melhor) é **comparação de modelos, não teste** — reporta-se ordenação por validação cruzada *leave-one-stratum-out*, sem valor-p.

### Validação cruzada

`leave-one-stratum-out`: retira-se um estrato inteiro, estima-se, prediz-se o erro daquele estrato. Mede exatamente o que o T2 promete entregar — **saber ex ante em que estrato não confiar** —, e não apenas ajuste dentro da amostra.

Métrica de comparação: erro quadrático médio de predição fora da amostra, com intervalo por bootstrap.

---

## 5. Como reportar

### Tabela principal

Colunas empilhando as especificações, no formato canônico de economia aplicada:

| | (1) bruta | (2) + controles | (3) + deriva Δ(q) | (4) + EF modelo/caminho | (5) spline |
|---|---|---|---|---|---|
| `D1′` | β₁ | β₁ | β₁ | β₁ | — |
| termos não-lineares | — | — | — | — | Wald |
| N células | | | | | |
| R² dentro | | | | | |

A leitura é a estabilidade de `β₁` da coluna 1 à 4. Se ele sobrevive ao controle de deriva na coluna 3, a ameaça A1 está respondida **na tabela**, não em nota de rodapé.

### Figura principal

Não é a tabela. É a **curva de cobertura descendente em `k`** (M07, M6), com anotação do ponto em que a cobertura cruza 50%.

### Figura secundária

Predito contra observado por estrato, com o eixo x ordenado pela distância, e barras de erro de bootstrap. Mostra o decaimento diretamente e deixa visível onde o modelo de decaimento falha.

### Reporte obrigatório de nulos

Se `β₁` for nulo, a tabela é a mesma e a conclusão inverte. **Escrever a versão nula do abstract antes da coleta** e guardá-la junto ao pré-registro. É a defesa mais barata contra racionalização posterior, e a M12 deve incluí-la.

---

## Pendências geradas

- [ ] **Refazer o desenho do pré-teste** conforme a seção 1: gradiente por país nos cinco, regredido contra centralidade, em vez de México contra Estados Unidos.
- [ ] Verificar se `data/Linear/` de Boelaert et al. serve de gabarito para a linha de base supervisionada de F5.
- [ ] Definir a operacionalização exata dos cinco níveis de `C(q)` sobre as categorias da POF.
- [ ] Calcular `Δ(q)` — taxa de mudança POF 2008-2009 → 2017-2018 por categoria — e checar comparabilidade de classificação entre as ondas (pendência aberta desde a M08).
- [ ] **M10 herda:** o poder é sobre número de réplicas e de estratos; com 7 estratos em L1, o bootstrap selvagem é obrigatório e o poder para detectar não-linearidade é provavelmente baixo. **Verificar se L2 (20 células) precisa virar o nível confirmatório em vez de L1.**
- [ ] **M12 herda:** pré-registrar posição dos nós da spline, ordenação de `C(q)`, correção BH, e o abstract da versão nula.
