# M05 — Estratos POF/PNAD: variáveis, células e disponibilidade de dado

Executada em 2026-08-21. Documento metodológico da POF 2017-2018 baixado e lido; demais fontes verificadas por busca.

---

## Resumo do que esta missão muda

1. **As sete classes de rendimento da POF são oficiais, estão publicadas e resolvem a estratificação primária.** Verificadas no Quadro 2 das Notas Técnicas. Usar exatamente essas faixas dá comparabilidade direta com tabelas publicadas do IBGE — o que significa que parte do benchmark do T2 não precisa nem de microdado.

2. **⚠️ Confundidor temporal grave, e é o achado mais importante desta missão.** A POF vigente é de **2017-2018**. Os modelos que o T2 vai auditar foram treinados com dado até 2024-2025. Se a resposta sintética divergir do benchmark, pode ser porque **o consumo brasileiro mudou** — pandemia, inflação, Pix, aplicativos de entrega, bets — e não porque o modelo é enviesado. Sem tratamento explícito, este confundidor derruba o paper.

3. **⚠️ O proxy de pegada digital está saturado e morreu.** PNAD Contínua TIC 2024: **93,6% dos domicílios com internet**, e a diferença rural-urbana caiu de mais de 40 pontos em 2016 para 9,9 pontos em 2024. Acesso à internet não discrimina mais estrato no Brasil. A candidata D da M04 precisa ser substituída por medida de **tipo de uso**, não de acesso.

4. **O gargalo de corpus da M04 continua aberto e piorou.** Os corpora do português brasileiro com metadado de falante existem, mas são orais, regionais e pequenos — o maior que encontrei tem 208 mil palavras. Não sustentam sondagem por perplexidade no padrão Dunn et al.

---

## 1. As sete classes de rendimento da POF

**Fonte verificada:** IBGE, *Pesquisa de Orçamentos Familiares 2017-2018: Primeiros Resultados*, Notas Técnicas, Quadro 2 — *Classes de rendimento total e variação patrimonial mensal familiar*.

Definição: rendimento total é a soma dos rendimentos monetário e não monetário mensal familiar mais a parcela monetária referente à variação patrimonial. Valores em salários mínimos de **15 de janeiro de 2009**.

| # | Reais mensais | Salários mínimos |
|---|---|---|
| 1 | Até R$ 1.908 ¹ | Até 2 |
| 2 | Mais de R$ 1.908 a R$ 2.862 | Mais de 2 a 3 |
| 3 | Mais de R$ 2.862 a R$ 5.724 | Mais de 3 a 6 |
| 4 | Mais de R$ 5.724 a R$ 9.540 | Mais de 6 a 10 |
| 5 | Mais de R$ 9.540 a R$ 14.310 | Mais de 10 a 15 |
| 6 | Mais de R$ 14.310 a R$ 23.850 | Mais de 15 a 25 |
| 7 | Mais de R$ 23.850 | Mais de 25 |

¹ Inclusive sem rendimento.

### Distribuição — e por que ela favorece o desenho do T2

Números extraídos do mesmo documento:

- **23,9%** das famílias brasileiras viviam com até R$ 1.908 (dois salários mínimos).
- Cerca de **60 milhões de famílias** recebiam até 10 salários mínimos.
- Apenas **3,0%** das famílias urbanas recebiam mais de 25 salários mínimos.
- **Interação renda × região é forte:** viviam com dois salários mínimos ou menos **39,1% no Norte** e **39,4% no Nordeste**, contra **14,8% no Sul** e **16,4% no Sudeste**.

Essa última linha é o argumento empírico de que a variação intra-Brasil é grande — a resposta direta ao dado de Dunn et al. que dizia que o Brasil tem pouca variação interna (ver M04, seção 4). **Uma diferença de 25 pontos percentuais entre Norte e Sul na incidência de pobreza é heterogeneidade de sobra.** Citar este número no paper.

E note o outro lado: a classe 7 tem apenas 3,0% das famílias urbanas. **A cauda de renda alta é rala no Brasil**, o que reforça a leitura (a) da M02 — renda muito alta é periférica em *dados de comportamento de escolha* brasileiros, ainda que central em corpus textual global.

---

## 2. Qual edição usar — e o confundidor temporal

### O estado das edições

| Edição | Situação | Domicílios | Divulgação |
|---|---|---|---|
| POF 2017-2018 | Publicada, microdado disponível | ~58 mil ² | 2019-2020 |
| **POF 2024-2025** | **Em campo desde 5/11/2024**, 12 meses | **mais de 103 mil** | **Prevista para 2026** |

² ⚠️ **Fontes divergem.** Encontrei "aproximadamente 58 mil domicílios" e também "75 mil domicílios em 1.900 municípios". O documento oficial descreve plano amostral por conglomerados em dois estágios, com estratificação geográfica e estatística das unidades de primeiro estágio — setores como UPAs, domicílios particulares permanentes como segundo estágio — mas não consegui isolar o N final na leitura desta missão. **Confirmar antes de citar.**

A POF 2024-2025 traz módulos novos diretamente úteis: gastos com **apostas eletrônicas (bets)**, satisfação com aspectos pessoais e financeiros, discriminação (gênero, raça, orientação sexual, capacitismo), uso do tempo e detalhamento de acesso a serviços financeiros.

### O confundidor

> Se o T2 mede a distância entre a resposta de um modelo treinado até 2024-2025 e um benchmark de consumo de 2017-2018, **o erro observado mistura viés do modelo com deriva real do consumo brasileiro** no período que inclui pandemia, inflação de alimentos, difusão do Pix, consolidação de aplicativos de entrega e explosão de apostas on-line.

Esse confundidor é fatal se não tratado, e um revisor de economia o vê na primeira leitura. Quatro tratamentos, do melhor ao pior:

1. **Usar a POF 2024-2025 se sair a tempo.** Alinha benchmark e corte de treino. Risco: divulgação prevista "para 2026" sem data, e o IBGE declarou publicamente restrição orçamentária para finalizar a pesquisa. **Não planejar contando com isso.**
2. **Ancorar em PNAD Contínua**, que é anual e chega a 2024, para todas as variáveis que ela cobre. Perde o detalhe de despesa por produto, ganha atualidade.
3. **Controle de deriva explícito.** Para cada categoria de consumo, medir o quanto ela mudou entre POF 2008-2009 e POF 2017-2018 e usar essa taxa como covariável. Se o erro do modelo correlaciona com a taxa histórica de mudança da categoria, é deriva; se não, é viés. **É o tratamento mais elegante e o mais defensável dentro do prazo.**
4. **Restringir a categorias de consumo estáveis.** Reduz o confundidor por seleção, ao custo de reduzir também a validade externa.

**Recomendação: adotar (3) como desenho central e (2) como robustez.** Registrar (1) como upside.

---

## 3. Especificação dos estratos

Desenho aninhado, seguindo a lógica de consistência estrutural de Li, Li e Qiu (ver M03), que constroem subgrupos em níveis crescentes de interseccionalidade e testam se a acurácia se mantém.

### Variáveis

| Variável | Níveis | Fonte | Observação |
|---|---|---|---|
| **Renda** | 7 (marginal) / 4 (cruzamentos) | POF, Quadro 2 | Colapsar em 4 para cruzar: até 2 SM; 2–6; 6–15; mais de 15. Justificativa: a classe 7 tem 3% das famílias urbanas e não sustenta célula cruzada |
| **Região** | 5 | POF / PNAD | Norte, Nordeste, Sudeste, Sul, Centro-Oeste |
| **Escolaridade** | 3 | PNAD | Sem instrução ou fundamental incompleto; médio; superior |
| **Cor ou raça** | 3 | PNAD | Branca; preta ou parda; demais |
| **Situação do domicílio** | 2 | POF / PNAD | Urbana; rural |

### Os quatro níveis de agregação

| Nível | Cruzamento | Células | Papel |
|---|---|---|---|
| **L1** | Renda (7 classes oficiais) | **7** | Benchmark direto contra tabelas publicadas do IBGE. **Não exige microdado.** |
| **L2** | Renda(4) × Região(5) | **20** | Núcleo do teste de decaimento. Captura a interação renda-região de 25 pontos |
| **L3** | L2 × Escolaridade(3) | **60** | Primeiro teste de consistência estrutural |
| **L4** | L3 × Cor/raça(3) | **180** | Teste interseccional; onde o colapso deve ser mais severo |

### Regra de tamanho mínimo de célula

Célula com menos de **100 domicílios não ponderados** na POF é colapsada com a adjacente ou descartada, e o descarte é **reportado**. Sem essa regra, L4 produz células de renda alta no Norte rural com N de um dígito, e o "erro do modelo" ali vira ruído do benchmark. Isto responde diretamente à leitura (b) da M02 — instabilidade por célula pequena contra viés sistemático.

### Faseamento

O desenho completo explode: 180 células × 3 modos de condicionamento (QA/BIO/PORTRAY, ver M01) × 4 caminhos de extração (logprob, describe, PPA, agregação, ver M03) × k modelos × j categorias de consumo. Faseamento obrigatório:

- **Fase 1 — núcleo.** L1 e L2 (27 células), fatorial completo em modos, caminhos e modelos. É o que responde RQ1 e RQ2.
- **Fase 2 — consistência estrutural.** L3 e L4, fatorial reduzido: melhor caminho de extração e melhor modo apenas, todos os modelos.

---

## 4. Disponibilidade de dado — o que verifiquei

| Fonte | Existe? | Tabelas prontas? | Microdado? | Veredito |
|---|---|---|---|---|
| **POF 2017-2018** | ✅ | ✅ Tabelas de resultado e de coeficiente de variação no portal | ✅ Microdado publicado, com instrumentos de coleta | **Usável.** L1 sai de tabela pronta; L2-L4 exigem microdado |
| **POF 2024-2025** | Em campo | — | — | Upside, não planejar em cima |
| **PNAD Contínua TIC 2024** | ✅ | ✅ | ✅ | Usável, mas ver saturação abaixo |
| **Base dos Dados** | ✅ hospeda POF 2017-2018 | — | — | ⚠️ Páginas carregam por JavaScript e não consegui ler o esquema. **Verificar manualmente** — se hospedam a POF tratada em BigQuery, economiza semanas de limpeza |
| **INSE / INEP** | ✅ Indicador de Nível Socioeconômico, nota técnica do SAEB 2023 | — | — | ⚠️ Download falhou por erro de certificado SSL. **Reverificar** — é um indicador socioeconômico oficial validado que poderia substituir a construção manual de estratos |
| **World Values Survey Brasil, onda 7** | ✅ Campo em maio-junho de 2018 | — | ✅ | ⚠️ **Amostra efetiva de ~1.500.** Fino demais para CFst com desagregação por classe. A candidata B da M04 fica comprometida |

### A saturação que mata o proxy de pegada digital

PNAD Contínua TIC 2024, números verificados:

- **93,6%** dos domicílios com internet (74,9 milhões), alta de 1,1 ponto sobre 2023.
- **89,1%** das pessoas de 10 anos ou mais usaram internet nos últimos três meses (168,0 milhões de 188,5 milhões).
- Diferença rural-urbana caiu de **mais de 40 pontos em 2016** (35,0% contra 76,6%) para **9,9 pontos em 2024** (84,8% contra 94,7%).
- Pela primeira vez, mais da metade da população acessa internet pela TV.

**Com 93,6% de penetração, acesso à internet não tem variância suficiente para ordenar estratos.** A candidata D da M04 morre nessa forma.

**Substituto proposto:** medir *tipo e intensidade* de uso, não acesso. Os 5,1 milhões de domicílios sem uso declaram três motivos principais — ninguém sabia usar (32,6%), serviço caro (27,6%), falta de necessidade (26,7%) — e a distribuição desses motivos por estrato ainda discrimina. Melhor ainda: **acesso pela TV como marcador de perfil de uso passivo**, que é justamente o tipo de uso que **não gera texto**. Como o que interessa a D1 é produção textual, um índice de "uso produtor de texto contra uso consumidor de conteúdo" é teoricamente melhor que penetração e ainda tem variância.

---

## 5. O gargalo de corpus continua aberto

A M04 deixou como ameaça de viabilidade: existe corpus em português rotulado por estrato socioeconômico? Levantei os candidatos:

| Corpus | Tamanho | Metadado de falante | Problema |
|---|---|---|---|
| **C-ORAL-BRASIL I** | 139 sessões, 21,13 horas, **208.130 palavras**, 362 informantes | Sim, com metadados publicados | Oral e informal; regional (Belo Horizonte e Minas Gerais); **pequeno demais** para sondagem por perplexidade. Licença CC BY-NC-SA 4.0, download aberto no site do projeto |
| **ALIP / banco Iboruna** | — | Sim | Regional (interior paulista); oral |
| **NURC** | Grande para a época | Sim | Por definição **apenas norma culta urbana**, cinco capitais — cobre só o centro, exatamente o oposto do que o T2 precisa |
| **CORAA** | Grande, validado manualmente | Parcial | Voltado a reconhecimento de fala; metadado socioeconômico incerto |

**Diagnóstico:** nenhum sustenta a medida D1 no padrão Dunn et al., que usa 86 mil sub-corpora. O NURC é particularmente irônico: é um corpus *desenhado* para capturar apenas o estrato central.

**Três saídas, para decidir na M06:**

1. **Abandonar D1 e promover D3 (cultural) a primária** — mas a M05 acabou de mostrar que o WVS Brasil tem N≈1.500, o que também é fino.
2. **Construir o corpus.** Amostrar texto público por marcador geográfico fino (setor censitário ou CEP) e imputar estrato pelo perfil do setor. Viável tecnicamente, caro em tempo, e introduz erro de imputação ecológica.
3. **Reformular D1 como medida interna ao modelo.** Em vez de perplexidade sobre corpus externo rotulado, medir a **perplexidade que o modelo atribui às próprias respostas condicionadas por estrato**, ou a entropia da distribuição de saída por estrato. Não precisa de corpus nenhum, é barato, e mede algo próximo do que interessa: quanta massa de probabilidade o modelo tem disponível naquela região do espaço.

**A saída 3 é a mais promissora e não estava no radar.** Tem risco de circularidade — usar o próprio modelo para medir a distância que explica o erro do modelo — e precisa de defesa cuidadosa. Registrar como decisão aberta prioritária para a M06.

---

## Pendências geradas

- [ ] **Confirmar o N amostral da POF 2017-2018** (58 mil ou 75 mil domicílios) na documentação metodológica completa, não nos Primeiros Resultados.
- [ ] **Verificar manualmente o Base dos Dados** — se a POF está tratada em BigQuery, muda o cronograma da M06 e da coleta.
- [ ] **Rebaixar o INSE de pendência para verificação** — refazer o download da nota técnica do SAEB 2023 contornando o erro de certificado.
- [ ] **Decidir a saída do gargalo de corpus** (abandonar D1 / construir corpus / reformular D1 como medida interna). **Prioridade máxima na M06.**
- [ ] Definir a lista de categorias de consumo do T2, com a taxa histórica de mudança POF 2008-2009 → 2017-2018 calculada para cada uma, para o controle de deriva.
- [ ] Verificar a data prevista de divulgação da POF 2024-2025 diretamente com o IBGE — se for antes de novembro, muda tudo.
- [ ] Confirmar se o WVS Brasil onda 7 permite desagregação por classe com células mínimas viáveis, ou se o CFst fica inviável.
