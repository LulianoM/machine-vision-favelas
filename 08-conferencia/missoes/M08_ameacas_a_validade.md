# M08 — As oito ameaças mais prováveis à validade do T2

Executada em 2026-08-21. Consolida ameaças registradas em M01 a M07 e as ordena por probabilidade × dano.

---

## Nota de atualização durante a missão

A pendência de prioridade máxima da M07 foi **resolvida**. O pacote `Machine-Bias-replication.zip` (osf.io/yzect, depositado em 26/02/2025, 336 MB) foi baixado e inspecionado. Conteúdo confirmado:

| Diretório | O que tem |
|---|---|
| `code/` | Pipeline completo em R 4.4.1 e Python 3.11.9, numerado em ordem de execução, mais `EMD.cpp` |
| `data/subpops.csv` | **26.981 observações individuais** com o agrupamento em subpopulações |
| `data/WVS/` | `wvs-data.csv`, `wvs-levels.csv`, `wvs-questions.csv` — a referência humana |
| `data/LLM-outputs/` | Saídas por método e modelo: `FA-GPT-3`, `FA-Llama-3-70B`, `FA-Mixtral-8x7B`, `NTP-GPT-4T`, `NTP-Llama-3-70B`, `NTP-Mixtral-8x7B`, mais coleção em `csv/` |
| `data/Linear/` | Predições do **modelo de linha de base linear com validação cruzada LOO** |
| `data/Robustness/` | Varredura de temperatura (0,3 · 0,7 · 1,0 · 1,2 · 1,5) e checagem de quantização |

Cinco fatos que mudam o dossiê:

1. **Eles usam EMD, ou seja, Wasserstein.** `EMD.cpp` chamado por `6-results.R`, e a figura principal é `Figure-2-nEMD-density`. A métrica primária da M07 é a mesma família da deles — comparabilidade direta, sem tradução.
2. **Eles rodam dois caminhos de extração: NTP (probabilidade do próximo token) e FA (resposta completa).** É quase exatamente a distinção P2 versus P4 da M06. O caminho *describe* (P1) **não está lá** — segue sendo território do T2.
3. **Eles já têm linha de base supervisionada** (`data/Linear/`, com `ranger` e `nnet` entre as dependências do R). Isso dá precedente e possivelmente dado reaproveitável para a mitigação da ameaça A7.
4. **A estrutura de subpopulação inclui classe social.** O campo `profile` tem a forma `País§Ano§Idade§Sexo§Classe§Ocupação§EstadoCivil`, com classe assumindo valores como `High` e `Middle`. **A variação intra-país por classe está no dado deles.**
5. **⚠️ Cinco países, e o Brasil não está entre eles:** Rússia (5.883), Alemanha (5.618), Estados Unidos (5.387), Austrália (5.282) e **México (4.811)**.

### O que isso permite fazer imediatamente, de graça

O México é o análogo mais próximo do Brasil disponível: América Latina, renda média, língua não-inglesa. Isso torna possível um **pré-teste de RD2 sem coletar nada**:

> Estimar o gradiente de erro por classe social **dentro** do México e **dentro** dos Estados Unidos, e testar se o gradiente é mais íngreme no México.

Os três desfechos e o que cada um significa para o T2:

| Resultado no dado de Boelaert et al. | Leitura |
|---|---|
| Gradiente de classe existe e é mais íngreme no México | **Prova de conceito.** A hipótese do T2 vale num país semiperiférico. A coleta brasileira vira confirmação com benchmark melhor (POF ponderada contra WVS) e desfecho melhor (consumo contra opinião) |
| Gradiente existe mas é igual nos dois | Hipótese de decaimento sobrevive, hipótese de periferia não. T2 muda de tese |
| Gradiente ausente nos dois | **Boelaert et al. estão certos.** Considerar migração para o T5 |

E a ausência do Brasil deixa de ser lacuna e vira justificativa explícita: cinco países, nenhum deles a maior economia da América do Sul.

## Tabela-resumo

| # | Ameaça | Probabilidade | Dano | Mitigação existe? |
|---|---|---|---|---|
| **A1** | Confundidor temporal do benchmark | **Certa** | **Fatal** | Sim, e custa trabalho |
| **A2** | O colapso não é estruturado (RD2 nulo) | Média-alta | **Fatal para a contribuição** | Parcial — agora testável ex ante |
| **A3** | Escavação antes de 19/11 | Média-alta | Alto | Só velocidade |
| **A4** | Célula pequena confundida com viés | Alta | Médio | Sim, barata |
| **A5** | Confundimento modelo × método de extração | Certa se ignorada | Médio | Sim, já decidida |
| **A6** | A premissa de heterogeneidade é contestável | Média | Médio-alto | Sim, mas exige texto |
| **A7** | O colapso não é específico de LLM | Média | **Alto** | Sim, exige braço novo |
| **A8** | Faixas de renda temporalmente ambíguas no prompt | Alta | Médio | Sim, trivial |

---

## A1 — Confundidor temporal do benchmark

**Mecanismo.** A POF vigente é de 2017-2018. Os modelos auditados foram treinados com dado até 2024-2025. Toda divergência observada mistura duas coisas inseparáveis a priori: viés do modelo em relação ao grupo, e **deriva real do consumo brasileiro** no intervalo — pandemia, inflação de alimentos, difusão do Pix, consolidação de aplicativos de entrega, explosão de apostas on-line.

**Por que é a ameaça número um.** É certa, não provável. E é a primeira coisa que um economista vê. Se o modelo "erra" a participação de delivery no orçamento de uma família de baixa renda, ele pode estar simplesmente certo sobre 2025 e comparado contra 2017.

**Mitigação, em três camadas:**

1. **Covariável de deriva.** Para cada categoria de consumo, calcular a taxa de mudança entre POF 2008-2009 e POF 2017-2018 e incluí-la na regressão. Se o erro do modelo correlaciona com a taxa histórica de mudança da categoria, é deriva; se o coeficiente de distância sobrevive ao controle, é viés. **Esta é a mitigação principal e precisa estar no pré-registro.**
2. **Braço PNAD.** Replicar o desenho nas variáveis cobertas pela PNAD Contínua, que chega a 2024. Perde detalhe de despesa, ganha contemporaneidade. Se o padrão de decaimento aparecer nos dois, a deriva não explica.
3. **Teste de placebo temporal.** Rodar o mesmo modelo contra POF 2008-2009 e contra POF 2017-2018. Se o erro por estrato for estável entre as duas ondas, a estrutura não é artefato de época.

**Risco residual.** A camada 3 é a mais forte e a mais barata, e não estava no dossiê até agora. Com as três, o risco cai de fatal para gerenciável — mas não desaparece, porque nenhuma delas cobre categorias que simplesmente não existiam em 2018.

**O que o revisor diria:** *"Como você separa viés do modelo de mudança real no consumo?"* Se essa pergunta chegar na sessão e não houver resposta em um slide, o paper morre em público.

---

## A2 — O colapso não é estruturado

**Mecanismo.** A regra de decisão RD2 testa se o erro decai sistematicamente com a distância. Se `β₁` for nulo, Boelaert et al. estão certos — o viés varia de forma imprevisível — e o T2 deixa de ser refutação e vira replicação em novo domínio.

**Por que é fatal para a contribuição, não para o paper.** Um nulo bem medido em consumo brasileiro ainda é publicável. Mas é um paper muito mais fraco, e não é o que se leva a Los Angeles.

**Mitigação, agora possível:**

**Confirmada e viável.** O pacote de replicação foi baixado e contém tudo o que RD2 precisa: `subpops.csv` com 26.981 indivíduos e classe social no perfil, `WVS/wvs-data.csv` como referência humana, e as saídas de seis combinações de modelo e método. Ver a nota de atualização no topo para o desenho do pré-teste México contra Estados Unidos.

**Risco residual.** Alto até o pré-teste ser rodado; conhecido depois dele. O pré-teste custa dias, não semanas, porque o dado está limpo e o pipeline dos autores é público.

**Ação:** este teste passa a ser a coisa mais valiosa do cronograma. Deve acontecer **antes** da M12 (pré-registro), não depois.

---

## A3 — Escavação antes de 19 de novembro

**Mecanismo.** O campo acelerou visivelmente: entre abril e julho de 2026 saíram pelo menos quatro trabalhos diretamente relevantes — colapso de heterogeneidade em filósofos (abril), *verbalized sampling* (julho), *semantic similarity rating* (julho) e o split KNOWS/DOES (julho). Mais os métodos de restauração de heterogeneidade por segmentação de audiência e injeção paramétrica de identidade social, ainda não lidos.

**Mitigação.** Nenhuma técnica. Só três coisas práticas:

1. **Depositar preprint** assim que o resultado principal estiver estável, antes da submissão à AIM. Estabelece prioridade.
2. **Defender o que não é escavável:** o benchmark brasileiro oficial e a variação intra-país. Método e métrica são copiáveis; POF ponderada não é.
3. **Varredura ativa** — é a missão M11, que já está no roteiro.

**Risco residual.** Irredutível. É custo de operar num campo quente.

---

## A4 — Célula pequena confundida com viés sistemático

**Mecanismo.** O nível L4 do desenho (renda × região × escolaridade × cor/raça, 180 células) produz células como renda alta no Norte rural com N de um dígito na POF. O "erro do modelo" ali é ruído do benchmark. E o problema é insidioso porque **as células pequenas são justamente as periféricas** — ou seja, o ruído se correlaciona com a variável explicativa, produzindo exatamente o resultado que a hipótese prediz, por motivo errado.

Esta é a leitura (b) da anomalia de renda alta em Brand et al. (ver M02), promovida a ameaça geral.

**Mitigação:**

1. Regra de tamanho mínimo já fixada na M05: **100 domicílios não ponderados por célula**, abaixo disso colapsa ou descarta, e o descarte é reportado.
2. **Ponderar a regressão pelo inverso da variância do benchmark**, para que células mal estimadas pesem menos.
3. **Teste direto:** incluir o N da célula como covariável concorrente. Se o efeito de distância desaparece ao controlar por N, era ruído.

**Risco residual.** Baixo, e a mitigação 3 é decisiva. Mas ela precisa estar no pré-registro, senão parece justificativa post hoc.

---

## A5 — Confundimento entre modelo e método de extração

**Mecanismo.** A Anthropic não expõe log-probabilidades; OpenAI e Gemini expõem. Comparar modelos usando logprob onde há e outro método onde não há torna impossível separar "este modelo é pior" de "este modelo foi medido de outro jeito".

**Mitigação.** Já decidida na M06 e sem custo adicional: o caminho *describe* (P1) é primário porque funciona em todos os provedores; logprob (P2) entra como validação convergente apenas no subconjunto que o suporta. **Toda comparação entre modelos usa exclusivamente P1.**

**Risco residual.** Nulo se a regra for seguida. A ameaça real é de disciplina, não de método — a tentação de usar o dado de logprob onde ele existe porque é mais rico.

---

## A6 — A premissa de heterogeneidade intra-Brasil é contestável

**Mecanismo.** Dunn et al. (arXiv:2403.11025) reportam que o Brasil está entre os países com **menos** variação interna na qualidade de representação pelo modelo. Um revisor com esse paper em mãos ataca a escolha do sítio empírico: se o Brasil é homogêneo aos olhos do modelo, por que estudar variação intra-brasileira?

**Mitigação — três argumentos, já formulados na M04 e agora com número:**

1. **O eixo é outro.** A medida deles é geográfica, entre áreas metropolitanas; a do T2 é socioeconômica. E no Brasil a desigualdade é muito mais de classe que de metrópole.
2. **A amostra brasileira deles é elite.** Eles coletam tweets **em inglês**. Brasileiro que tuíta em inglês é urbano, escolarizado e de renda alta. Baixa variação medida sobre amostra já selecionada no centro é artefato de seleção. **Argumento mais forte e verificável.**
3. **Dado oficial contradiz a leitura.** POF 2017-2018: viviam com até dois salários mínimos **39,1% das famílias do Norte e 39,4% do Nordeste**, contra **14,8% no Sul e 16,4% no Sudeste**. Vinte e cinco pontos percentuais de diferença é heterogeneidade de sobra.

**Risco residual.** Baixo, desde que os três argumentos ocupem um parágrafo explícito. Ignorar o paper de Dunn et al. é pior do que enfrentá-lo.

---

## A7 — O colapso não é específico de LLM

**Mecanismo.** Ku et al. (arXiv:2607.03091) acham que **colapso de variância também afeta modelos supervisionados** treinados na mesma população. Se parte do achatamento é propriedade de qualquer preditor estatístico — regressão à média, essencialmente — então atribuí-lo a "viés do modelo de linguagem" é erro de interpretação.

**Por que o dano é alto.** Não mata o achado, mas muda o que ele significa. E é o tipo de objeção que um econometrista da plateia levanta em quinze segundos.

**Mitigação.** Braço de linha de base supervisionada, registrado na M04 e ainda não incorporado ao desenho: treinar uma floresta aleatória ou modelo equivalente sobre microdado POF/PNAD para prever a mesma distribuição por estrato, e medir seu colapso com as mesmas seis métricas da M07.

Interpretação do contraste:

- Se o LLM colapsa **mais** que o supervisionado → o excesso é atribuível ao modelo de linguagem. Achado limpo.
- Se colapsam **igual** → o fenômeno é de predição estatística em geral, e o T2 muda de tese sem perder valor: passa a ser sobre o limite fundamental de qualquer respondente sintético.
- Se o LLM colapsa **menos** → resultado inesperado e muito interessante.

**Risco residual.** Baixo com o braço; alto sem ele. **Custo:** uma semana de trabalho. **Recomendação: incorporar.**

---

## A8 — Faixas de renda temporalmente ambíguas dentro do prompt

**Mecanismo.** As sete classes da POF estão expressas em reais **de 2009**. Colocar "a renda da minha família é de R$ 2.862 por mês" no prompt de um modelo treinado até 2025 evoca um estrato socioeconômico completamente diferente do que a POF classifica. É o confundidor A1 entrando pela porta do instrumento, e é pior que A1 porque contamina a **condição experimental**, não só a comparação.

**Mitigação:**

1. **Condicionar por posição relativa, não por valor nominal.** Usar percentil de renda ou múltiplo de salário mínimo vigente, em vez de reais nominais de 2009. "Minha família está entre os 30% de menor renda do país" é temporalmente estável; "R$ 1.908" não é.
2. **Braço de robustez com valor nominal atualizado**, deflacionado para o ano de corte do modelo.
3. **Testar as três formulações** — percentil, salário mínimo, real nominal — em subconjunto de células. A sensibilidade a essa escolha é, ela própria, informação.

**Risco residual.** Baixo. A mitigação 1 é trivial e provavelmente superior por outros motivos.

---

## Ameaças registradas fora do top 8

Não desapareceram; apenas têm mitigação já decidida ou dano menor.

| Ameaça | Estado |
|---|---|
| Circularidade da medida D1′ | Mitigada por construção na M06 — itens disjuntos, verdade externa no IBGE, entropia reportada à parte |
| Viés de recência de até 20× | Mitigada — randomização de ordem e ordem reversa balanceada (M06) |
| Desejabilidade social nas categorias sensíveis | Resolvida — exclusão do primário, análise secundária com sinal invertido (M06) |
| WVS Brasil com N≈1.500 | Limita D3 a papel secundário; D1′ é primária, então o dano é contido |
| Deriva de versão de modelo durante a coleta | Mitigada — protocolo de versionamento e janela curta declarada (M06) |
| KL infinito sem suavização | Resolvida — Laplace com α = 0,5 no pré-registro (M07) |
| Testes clássicos inválidos porque *k* é escolha de desenho | Resolvida — toda incerteza por bootstrap entre réplicas (M07) |
| Bisbee et al. sem texto integral | Contida — três números marcados como não verificados, não usados |

---

## O que mudou no desenho por causa desta missão

Duas adições concretas:

1. **Teste de placebo temporal** contra POF 2008-2009, como terceira camada de A1. Barato e forte.
2. **Braço de linha de base supervisionada**, para A7. Uma semana de trabalho, e sem ele o achado é interpretável de duas maneiras.

E uma reordenação de cronograma: **o teste de RD2 sobre os dados de Boelaert et al. precisa vir antes do pré-registro**, não depois. É o único item capaz de matar o projeto cedo o bastante para trocar de tema sem perder o prazo.

---

## Pendências geradas

- [x] ~~Baixar e inspecionar `Machine-Bias-replication.zip`~~ — **feito nesta missão.** Pacote completo, 336 MB, em `scratchpad/boelaert/`.
- [ ] **Rodar o pré-teste México contra Estados Unidos sobre os dados de Boelaert et al., antes da M12.** É o item de maior valor por hora de trabalho em todo o cronograma.
- [ ] Verificar se `data/Linear/` é reaproveitável como linha de base supervisionada para a ameaça A7.
- [ ] Incorporar formalmente o braço supervisionado ao desenho (afeta M09, M10 e M12).
- [ ] Incorporar o placebo temporal contra POF 2008-2009 (afeta M09 e M12).
- [ ] Verificar disponibilidade e comparabilidade do microdado da POF 2008-2009 com o da POF 2017-2018 — mudanças de classificação de despesa entre ondas podem inviabilizar o placebo.
- [ ] Decidir a formulação de condicionamento de renda (percentil, salário mínimo ou nominal) e registrar no pré-registro.
