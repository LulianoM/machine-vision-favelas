# M12 — Pré-registro OSF do T2 (rascunho completo)

Executada em 2026-08-21. Consolida M01 a M11. Formato de pré-registro do OSF.

> ⚠️ **Este rascunho contém uma mudança de tese em relação ao dossiê original.** A hipótese primária deixa de ser o gradiente de decaimento por estrato e passa a ser a **não-responsividade de variância**, seguindo a recomendação da M10 e a advertência metodológica da M11. O gradiente é rebaixado a hipótese secundária. A justificativa está na seção 2.

---

## 1. Informações do estudo

**Título.** Non-Responsive Variance: Do Synthetic Consumers Track the Dispersion of Real Populations? Evidence from Brazilian Household Budget Microdata

**Título em português.** Variância não-responsiva: respondentes sintéticos acompanham a dispersão de populações reais? Evidência de microdados de orçamento familiar brasileiros

**Autoria.** A definir (ver M36). Primeiro autor e apresentador: Felipe Figueira, FGV.

**Data de registro.** Anterior a qualquer chamada de API. Alvo: até 30 de setembro de 2026.

### Descrição

Modelos de linguagem são crescentemente usados como respondentes sintéticos em pesquisa de mercado. A literatura estabeleceu que eles acertam médias e erram dispersão (Bisbee et al., 2024; Boelaert et al., 2025), e que o erro é previsível a partir da **estrutura do item** (Özkan, 2026). Não se sabe se o erro é previsível a partir da **posição da população** — isto é, se o modelo erra mais em estratos socioeconômicos distantes daqueles que dominam seu corpus.

Este estudo audita respondentes sintéticos contra microdado oficial brasileiro de consumo, estratificado por rendimento, região e escolaridade, e testa se a variância que o modelo produz acompanha a variância real da população.

### Hipóteses

**H1 — Não-responsividade de variância (confirmatória, primária).**

> A variância das respostas sintéticas é aproximadamente invariante ao estrato, enquanto a variância humana varia substancialmente. Formalmente: a correlação entre a variância humana do estrato e o log da razão de variância é **negativa e substancial**.
>
> `H1: ρ( Var[H_s], ln VR_s ) < −0,5`

Predição de sinal e de magnitude. O limiar de −0,5 é escolhido a priori como "substancial", bem abaixo do −0,89 observado em dado de terceiros (ver seção 2), para não pré-registrar o resultado esperado.

**H2 — Gradiente por distância (confirmatória, secundária).**

> O erro de fidelidade cresce com a distância do estrato ao centro de massa do corpus, medida por erro factual de caracterização.
>
> `H2: β₁ > 0 em E_sq = β₀ + β₁·D1′(s) + controles`

**H3 — Interação complexidade × periferia (exploratória).**

> O erro em estratos periféricos é desproporcionalmente maior em momentos estatísticos mais complexos (incidência < frequência < participação orçamentária < escolha < disposição a pagar).

**H4 — Gradiente do split KNOWS/DOES (exploratória).**

> A vantagem do caminho *describe* sobre a agregação por persona cresce com a distância do estrato.

**H5 — Excesso sobre linha de base estatística (exploratória).**

> O colapso do modelo de linguagem excede o de uma linha de base de cópula gaussiana ajustada ao mesmo microdado.

---

## 2. Justificativa da mudança de tese

Registrada aqui por transparência, porque o dossiê original perseguia H2 como primária.

**Razão 1 — poder.** O gradiente de classe observado em dado de terceiros (Boelaert et al., 2025, pacote de replicação, 45 células de país × classe) tem amplitude de **0,086** log contra desvio padrão residual de **0,24**, o que corresponde a `β ≈ 0,043`. A simulação de poder da M10, calibrada nesses parâmetros, indica poder inferior a 0,43 mesmo com 180 estratos. **H2 como primária seria um teste subdimensionado por construção.**

**Razão 2 — o dado já mostra H1 com força.** No mesmo material, `r(Var[H], ln VR) = −0,887` no conjunto e **−0,974 e −0,977** em dois dos três itens. O coeficiente de variação da variância humana é 5,2 a 7,8 vezes o da variância do modelo.

**Razão 3 — robustez ao viés do instrumento.** Özkan (2026) mostra que o caminho *describe*, eleito primário na M06, **super-dispersa de forma estrutural** (razão de desvio padrão de 0,4–0,56 para 1,26–1,37). Um desfecho de **nível** de `ln VR` é contaminado por esse viés; uma **correlação** é invariante a deslocamento constante. H1 é robusta exatamente onde H2 é frágil.

**Razão 4 — diferenciação.** A onda de economia de 2026 ocupa o segundo momento em **expectativas macroeconômicas de domicílios** — Dalloul e Pfeifer sobre SCE, Michigan e SPF ⚠️ [NÃO VERIFICADO, ver seção 9], Banco da Inglaterra WP 1.190, NBER w34308. Nenhum deles trata **consumo desagregado por estrato socioeconômico com benchmark oficial ponderado**. A contribuição é a estrutura transversal do segundo momento, não o segundo momento em si.

---

## 3. Plano de desenho

**Tipo de estudo.** Observacional com manipulação de instrumento. Não há sujeitos humanos: a referência humana é microdado secundário já coletado pelo IBGE.

**Fatores manipulados**, todos cruzados:

| Fator | Níveis |
|---|---|
| Modelo | 5 — GPT-4o, Gemini, Claude, Llama-3-70B, Mistral (versões datadas exatas) |
| Caminho de extração | 4 — P1 *describe* (primário), P2 logprob (onde disponível), P3 PPA, P4 agregação simples |
| Modo de condicionamento | 3 — QA, BIO, PORTRAY (Santurkar et al., 2023) |
| Réplica | 5 — 2 paráfrases × 2 sementes de ordem × execuções em dias distintos |

**Cegamento.** Não aplicável. Registra-se, porém, que a análise confirmatória será executada por script fixado no pré-registro, com o dado de referência humano **mascarado até a execução final**.

**Randomização.** Ordem das alternativas sorteada por chamada, com semente registrada. Metade das chamadas com escala invertida.

---

## 4. Plano amostral

**Fonte humana.** POF 2017-2018 (IBGE), microdado com peso amostral. Braço de contemporaneidade: PNAD Contínua até 2024.

**Unidade de análise.** Célula estrato × item.

**Nível confirmatório: L3 — 60 células.**

```
Renda (4 faixas colapsadas das 7 oficiais) × Região (5) × Escolaridade (3)
```

Níveis L1 (7 células, renda marginal) e L2 (20) são descritivos e servem à comparabilidade com tabelas publicadas. L4 (180, acrescentando cor ou raça) é exploratório, para consistência estrutural.

**Justificativa do tamanho.** Simulação da M10, cenário realista (`sd_u = 0,15`, `sd_e = 0,19`, calibrados em dado real): 60 estratos dão poder de **0,82–0,83** em `β = 0,10` e **0,99** em `β = 0,15`, confirmado em duas corridas independentes. Estratos valem cerca de dez vezes mais que itens: quadruplicar itens move o poder em três centésimos; triplicar estratos move em trinta e cinco.

**Itens.** 12 a 15 categorias de consumo da POF, escolhidas por **cobertura substantiva**, não por poder. **Exclusão a priori:** bebida alcoólica, tabaco, jogos e apostas, por subdeclaração conhecida no benchmark. Essas categorias entram apenas na análise secundária de desejabilidade social (seção 7).

**Regra mínima de célula.** Célula com menos de **100 domicílios não ponderados** é colapsada com a adjacente ou descartada. Todo descarte é reportado.

**Volume.** Caminho primário: 60 × 15 × 5 réplicas × 5 modelos ≈ **22.500 chamadas**. P3 e P4 restritos a **2 modelos e 5 itens**, suficientes para reproduzir o contraste de Jang et al. (TV 0,22 contra 0,46).

### Regra de parada

**Desenho fixo. Não há parada opcional.** O número de chamadas é escolha de desenho e não restrição amostral (Brand, Israeli e Ngwe, WP 23-062), logo nenhuma regra baseada em precisão é válida.

**Única interrupção permitida**, e não é sobre resultado: se na primeira réplica completa mais de 20% das células retornarem resposta inválida, ou o item de atenção falhar em mais de 10% delas, **interromper, corrigir o instrumento e descartar a coleta parcial**.

---

## 5. Variáveis

### Desfechos

| Símbolo | Definição | Uso |
|---|---|---|
| `ln VR_s` | `ln( Var[M_s] / Var[H_s] )` | Insumo de H1; desfecho de H2 |
| `A_Wass` | Alinhamento por Wasserstein-1 normalizada, fórmula de Santurkar et al. (2023) | Fidelidade, itens ordinais |
| `TV` | Distância de variação total | Fidelidade, itens nominais |
| `KS` | Sup da diferença entre acumuladas | Descritiva |
| `ESS`, `deff` | Tamanho efetivo de amostra e efeito de desenho de Kish | Tradução gerencial |
| `Cobertura(k)` | Fração de células em que o IC de 95% ingênuo contém o valor humano | **Figura principal** |

### Preditores

| Símbolo | Definição |
|---|---|
| `Var[H_s]` | Variância humana do estrato, ponderada pelo peso amostral da POF |
| `D1′(s)` | **Erro factual de caracterização**: erro do modelo ao declarar fatos verificáveis do estrato (rendimento médio, tamanho do domicílio, escolaridade modal, participação das principais despesas, posse de duráveis), pontuado contra POF/PNAD |
| `D3(s)` | CFst cultural (Muthukrishna et al., *Psychological Science*, 2020) — secundária, limitada por N≈1.500 do WVS Brasil |
| `Ent(s)` | Entropia da saída do modelo na tarefa de caracterização, reportada **separadamente** de `D1′` |

### Controles

| Símbolo | Definição | Origem |
|---|---|---|
| `Δ(q)` | Taxa de mudança da categoria entre POF 2008-2009 e 2017-2018 | Ameaça A1 (M08) |
| `Norm(q)` | Indicador de o item ter resposta normativamente correta | Özkan (2026) |
| `N_s` | Tamanho não ponderado da célula | Ameaça A4 (M08) |
| `Perp(s)` | Perplexidade do texto de condicionamento | Descarta artefato de redação |
| `C(q)` | Complexidade do momento, ordenada a priori em 5 níveis | H3 |

**Condicionamento de renda por posição relativa** (percentil ou múltiplo do salário mínimo vigente), **nunca por valor nominal em reais de 2009** — as faixas oficiais estão em reais de 15 de janeiro de 2009 e seriam temporalmente ambíguas dentro do prompt (ameaça A8).

---

## 6. Plano de análise

### Teste confirmatório primário (H1)

```
ρ̂ = corr( Var[H_s] , ln VR_s )    dentro de item, padronizado, agrupado sobre L3
```

Inferência por **bootstrap sobre réplicas** (paráfrase × semente × execução), 9.999 reamostragens. Rejeita-se H₀ se o intervalo de 95% de `ρ̂` estiver inteiramente abaixo de **−0,5**.

**Um teste, um alfa de 5%.** Tudo o mais é secundário ou exploratório e rotulado como tal.

### Teste confirmatório secundário (H2)

```
ln VR_sq = β₀ + β₁·D1′(s) + γ′X(s) + δ·Δ(q) + θ·Norm(q) + α_m + α_p + α_q + ε
```

Erro padrão por **bootstrap selvagem agrupado por estrato**, pesos de Rademacher — obrigatório dado o número pequeno de grupos. Ponderação das células pelo **inverso da variância do benchmark**.

Desfechos limitados em [0,1] (`TV`, `1 − A_Wass`, `KS`, `ESS/k`) estimados por **GLM fracionário quase-binomial com ligação logito**. `ln VR` por MQO.

### Teste de não-linearidade (pré-especificado)

Spline cúbico restrito com **4 nós nos percentis 5, 35, 65 e 95** de `D1′`. Teste de Wald conjunto sobre os termos não-lineares. Posições fixadas a priori.

### Multiplicidade

- Confirmatório: H1 e H2, alfa de 5% cada, declarados a priori.
- Exploratórias H3, H4, H5: **Benjamini–Hochberg com FDR de 10%**.
- RQ2 (qual medida de distância prevê melhor) é **comparação de modelos, não teste**: validação cruzada *leave-one-stratum-out*, reportando ordenação sem valor-p.

### Camada de variância declarada

Este estudo mede **V2** — variância entre personas dentro da célula. Distinta de **V1** (entre chamadas repetidas na mesma persona) e **V3** (entre células). A distinção é declarada porque resultados aparentemente contraditórios na literatura (Özkan mede V1 e acha sub-dispersão; a análise exploratória deste projeto sobre dado de Boelaert et al. mede V2 e acha super-dispersão em 82% das células) são camadas diferentes, não contradição.

### Exclusões

- Célula com N < 100 não ponderado.
- Resposta inválida ou recusa: tratada à parte, nunca imputada.
- Categorias com desejabilidade social: fora do primário.
- Suavização de Laplace com **α = 0,5** onde KL for calculado.

### Análises de robustez pré-especificadas

1. **Placebo temporal.** Repetir contra POF 2008-2009. Erro por estrato estável entre ondas indica que a estrutura não é artefato de época.
2. **Braço PNAD** até 2024, para as variáveis cobertas.
3. **Linha de base de cópula gaussiana** ajustada ao microdado (precedente: Lukauskas e Šarkauskaitė, 2026), para H5.
4. **Grade de temperatura** {0,0 · 0,7 · 1,0} em P3 e P4.
5. **Três formulações de condicionamento de renda** (percentil, salário mínimo, nominal deflacionado) em subconjunto de células.
6. **Teste de aquiescência em português**: subconjunto replicado em formato sim/não contra ordinal. Braun (2025) testou inglês, alemão e polonês; português está em aberto.

---

## 7. Análise secundária de desejabilidade social

Pré-registrada com **predição de sinal invertido**: nas categorias sensíveis excluídas do primário (álcool, tabaco, apostas), espera-se que a resposta sintética esteja **acima** do benchmark POF, porque o modelo é treinado em texto e não em declaração a entrevistador. Se confirmado, é evidência de que a distância medida não é só erro do modelo — parte é viés do benchmark.

---

## 8. O abstract da versão nula

Escrito **antes** da coleta, conforme a M09, e depositado junto ao pré-registro:

> *Auditamos respondentes sintéticos contra microdado oficial de orçamento familiar brasileiro em 60 estratos socioeconômicos e 15 categorias de consumo. **Não encontramos** relação sistemática entre a variância real de um estrato e a variância produzida pelo modelo (ρ = X, IC 95% [·,·]), nem gradiente de erro por distância ao centro de massa do corpus (β₁ = X, IC 95% [·,·]). O erro do respondente sintético em consumo brasileiro é, tanto quanto conseguimos medir, imprevisível ex ante. Isso corrobora Boelaert et al. (2025) num novo domínio e numa nova população, e implica que o profissional de pesquisa **não dispõe de critério anterior** para decidir em que estrato confiar — o que é uma advertência mais forte, não mais fraca, do que a hipótese que testamos.*

---

## 9. Pendências que devem ser fechadas antes do registro

| # | Item | Impacto se não fechado |
|---|---|---|
| 1 | **Pré-teste sobre o pacote de Boelaert et al.**: gradiente de classe por país nos cinco países, regredido contra centralidade | Sem ele, H2 é registrada às cegas |
| 2 | **Verificar Dalloul e Pfeifer (2026)** na SSRN | ⚠️ [NÃO VERIFICADO]. Sei apenas, por fonte secundária, que trata do segundo momento em SCE, Michigan e SPF. Se cobrir estrutura transversal, H1 perde novidade |
| 3 | **Testar a amplitude de `D1′`** | Validade sem amplitude não serve; se discriminar pouco, H2 cai |
| 4 | Confirmar N amostral da POF 2017-2018 (58 mil ou 75 mil domicílios) | Documentação divergente |
| 5 | Comparabilidade de classificação de despesa entre POF 2008-2009 e 2017-2018 | Inviabiliza o placebo temporal |
| 6 | Ler Park et al. (2023, 2024) | Condicionamento por entrevista pode ser um quarto modo superior |
| 7 | Verificar `data/Linear/` de Boelaert como gabarito de linha de base | Economiza implementação |

---

## 10. Cronograma até 19 de novembro de 2026

| Semana | Entrega |
|---|---|
| até 28/08 | E-mail à AIM sobre formato e elegibilidade; abrir o formulário logado; alinhar coautoria |
| 29/08 – 12/09 | **Pré-teste em Boelaert** (pendência 1) e verificação de Dalloul e Pfeifer (pendência 2). **Ponto de decisão: seguir com T2 ou migrar** |
| 13/09 – 30/09 | Instrumento, teste de amplitude de `D1′`, **registro no OSF** |
| 01/10 – 25/10 | Coleta e análise confirmatória |
| 26/10 – 12/11 | Redação em formato de working paper de marketing science |
| até 12/11 | **Depositar preprint** — o campo produziu cinco trabalhos relevantes só em julho de 2026 |
| até 19/11 | Submeter, com uma semana de folga |
