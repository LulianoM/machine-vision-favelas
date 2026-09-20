# M14 — Medição de homogeneização: escolha metodológica para entregas de agência

Executada em 2026-08-21. Quatro papers baixados; duas referências centrais verificadas por venue e página.

---

## Resumo do que esta missão muda

1. **A literatura confunde dois construtos, e o T3 precisa separá-los explicitamente.** DSI mede **criatividade dentro de uma peça**; a métrica de Doshi e Hauser mede **similaridade entre peças**. São perguntas diferentes: "cada entrega ficou mais sem graça?" não é "as entregas ficaram parecidas entre si?". Um paper que mede uma e afirma a outra é atacável.

2. **Encontrei a métrica que resolve o problema de comunicação do T3: o Vendi Score.** É o **número efetivo de peças distintas** num portfólio. Dizer a um dono de estúdio que "vinte entregas do trimestre valem por seis distintas" comunica sem tradução — é o análogo, para diversidade, do tamanho efetivo de amostra que a M07 adotou para variância.

3. **⚠️ Duas armadilhas técnicas que quebram a métrica de Doshi e Hauser fora do contexto original.** Anisotropia de embeddings infla o cosseno de linha de base, e o centroide *leave-one-out* fica instável quando o grupo é pequeno — que é exatamente o caso de um estúdio por trimestre. Ambas têm correção barata.

---

## 1. A distinção que a literatura confunde

| Construto | O que mede | Métrica típica | Pergunta |
|---|---|---|---|
| **Criatividade intra-peça** | Quão divergentes são as ideias **dentro** de um mesmo texto | **DSI** (Johnson et al., 2023); DAT | "Esta peça é criativa?" |
| **Diversidade entre peças** | Quão distintas as peças são **umas das outras** | Cosseno ao centroide; Vendi Score | "O conjunto é variado?" |

**Elas podem se mover em direções opostas.** Um estúdio pode produzir peças individualmente mais elaboradas e, ao mesmo tempo, mais parecidas entre si — que é literalmente a tese de Doshi e Hauser, com criatividade individual subindo e diversidade coletiva caindo.

**Consequência de desenho:** o T3 deve medir **as duas**, e a força do paper está em mostrar a tesoura. Medir só a segunda deixa o revisor perguntar se a qualidade caiu; medir só a primeira não toca a tese.

### DSI, verificado

JOHNSON, Daniel R.; KAUFMAN, James C.; BAKER, Brendan S.; PATTERSON, John D.; BARBOT, Baptiste; GREEN, Adam E.; VAN HELL, Janet; KENNEDY, Evan; SULLIVAN, Grace F.; TAYLOR, Christa L.; WARD, Thomas; BEATY, Roger E. *Divergent semantic integration (DSI): Extracting creativity from narratives with distributional semantic modeling*. **Behavior Research Methods**, v. 55, n. 7, p. 3726–3759, 2023. DOI 10.3758/s13428-022-01986-2.

Nove estudos, 27 comandos narrativos distintos, mais de 3.500 narrativas curtas, seis modelos de DSI comparados. O melhor emprega **BERT**, e os escores explicam **até 72% da variância** das avaliações humanas de criatividade, aproximando-se da confiabilidade entre avaliadores humanos em algumas tarefas. Poder preditivo equivalente para avaliadores especialistas e não especialistas.

**Isso é uma medida validada de criatividade percebida, obtida sem avaliadores humanos.** Para o T3 é valiosíssimo: permite ter um desfecho de qualidade percebida por peça **sem contratar um painel de avaliação**, que seria o custo proibitivo do desenho.

---

## 2. As candidatas

### A — Cosseno ao centroide *leave-one-out* (Doshi e Hauser, 2024)

```
Sim_i = 100 × cos( e_i , média{ e_j : j ∈ g, j ≠ i } )
```

**A favor:** desfecho **por peça**, o que a torna diretamente utilizável como variável dependente em regressão com efeitos fixos. Precedente publicado em *Science Advances*. Trivial de implementar.

**Contra:** o centroide é uma péssima representação de um grupo **multimodal**. Um estúdio que atende dois setores muito distintos tem um centroide que não se parece com nenhuma peça, e a similaridade ao centroide fica artificialmente baixa para todas.

### B — Distância média par a par

```
Div_i = 1 − média{ cos(e_i, e_j) : j ∈ g, j ≠ i }
```

**A favor:** também é por peça; **robusta a multimodalidade**, porque não colapsa o grupo num ponto. Interpretação direta.

**Contra:** custo O(n²), irrelevante nas escalas do T3. Perde o precedente exato de Doshi e Hauser.

### C — Vendi Score (Friedman e Dieng, 2023)

**Referência verificada:** FRIEDMAN, Dan; DIENG, Adji Bousso. *The Vendi Score: A Diversity Evaluation Metric for Machine Learning*. **Transactions on Machine Learning Research**, julho de 2023. arXiv:2210.02410v2. Princeton University e Vertaix.

Definição, reproduzida do artigo:

> Seja `k` uma função de similaridade semidefinida positiva com `k(x,x) = 1`; seja `K` a matriz de kernel com `K_ij = k(x_i, x_j)`; sejam `λ₁ … λₙ` os autovalores de `K/n`. Então
>
> ```
> VS = exp( − Σᵢ λᵢ · log λᵢ )
> ```
> com a convenção `0 log 0 = 0`.

Os autovalores de `K/n` são não negativos e somam 1, porque a diagonal de `K/n` vale `1/n` — logo a entropia de Shannon está bem definida. O Vendi Score é o **posto efetivo** da matriz de kernel, noção introduzida por Roy e Vetterli (2007) em processamento de sinais.

**Interpretação:** o **número efetivo de elementos distintos** no conjunto. Vale **1** quando todas as peças são idênticas e **n** quando são mutuamente ortogonais.

**A favor:** interpretável sem estatística. Não exige conjunto de referência nem distribuição. Aceita **qualquer** função de similaridade, então o T3 pode usar embeddings de texto para copy e de imagem para peças visuais, no mesmo arcabouço.

**Contra:** é **de grupo, não de peça** — não serve diretamente como variável dependente com efeitos fixos de peça. E é limitada superiormente por `n`, então comparar grupos de tamanhos diferentes exige normalizar por `n`.

**Truque computacional que o artigo registra:** os autovalores de `K/n` são os mesmos da matriz de covariância `XXᵀ/n`. Como no T3 o número de peças por estúdio-trimestre é pequeno e a dimensão do embedding é grande, computa-se a matriz `n × n`, que é barata.

### D — Taxa de crescimento de diversidade

Estilo rarefação: quanto conteúdo novo cada peça adicional acrescenta ao conjunto. Conceitualmente é a medida mais fiel à ideia de "novidade coletiva", e a literatura registra o achado de que cada ensaio humano adicional contribui mais ideias novas que cada ensaio de GPT-4.

**Contra:** exige uma definição operacional de "ideia nova" — agrupamento, cobertura de tópicos ou limiar de similaridade. Cada escolha é um grau de liberdade a mais e um flanco a mais. **Fora do escopo de 12 meses.**

### E — Contexto: o colapso também vem do pós-treino

**Referência verificada:** KAROUZOS, Constantinos; TAN, Xingwei; ALETRAS, Nikolaos. *Where does output diversity collapse in post-training?* arXiv:2604.16027v1, 17 de abril de 2026. School of Computer Science, University of Sheffield.

Rastreiam diversidade de saída em três linhagens paralelas de pós-treino do Olmo 3 — Think (destilação de cadeia de raciocínio), Instruct (dado multi-fonte amplo) e RL-Zero — em **15 tarefas e quatro métricas de diversidade textual**, separando o papel da composição do dado de treino do papel do método, e o do formato de geração do dos pesos.

**Uso no T3:** não é métrica, é **fonte de confundimento**. Se o estúdio troca de ferramenta durante o período, parte da mudança de homogeneização vem do modelo por trás e não da adoção. **Registrar a ferramenta e a versão por entrega, ou o efeito medido mistura adoção com deriva de modelo.** É o análogo, no T3, do protocolo de versionamento que a M06 fixou para o T2.

---

## 3. As duas armadilhas técnicas

### Anisotropia de embeddings

Espaços de embedding modernos são **anisotrópicos**: os vetores concentram-se num cone estreito, e o cosseno entre dois textos aleatórios já é alto — frequentemente acima de 0,7. Isso comprime toda a variação num intervalo curto e é parte da razão pela qual a amplitude no grupo de controle de Doshi e Hauser é de apenas **8,10 pontos** (ver M13).

**Correção padrão e barata:** **centrar os embeddings** — subtrair a média global do corpus — antes de calcular cosseno. Recupera amplitude sem alterar a ordenação.

**Decisão para o T3:** reportar as duas versões, crua e centrada. A crua mantém comparabilidade com Doshi e Hauser; a centrada é a que tem poder.

### Instabilidade do centroide em grupo pequeno

Com `n` peças por estúdio-trimestre, o centroide *leave-one-out* é a média de `n−1` vetores. Para `n = 5`, é uma média de quatro — ruidosa, e o ruído **cresce quando o grupo encolhe**. Como o tamanho do grupo pode correlacionar com o período e com a adoção, isso é ruído correlacionado com o tratamento.

**Correções:**
1. Preferir **B (par a par)** como primária, que não passa por centroide.
2. **Reportar o `n` do grupo** e incluí-lo como controle.
3. Fixar **`n` mínimo por grupo** — proposta: 8 peças, abaixo disso o grupo é agregado ou descartado, com descarte reportado. É o análogo da regra de célula mínima da M05.

---

## 4. A escolha, justificada

**Duas métricas, em dois níveis, mais uma de controle.**

| Papel | Métrica | Nível | Por quê |
|---|---|---|---|
| **Primária** | Distância média par a par, sobre embeddings **centrados**, restrita a peças de **outros clientes** no mesmo estúdio-período | Peça | Serve de variável dependente com efeitos fixos; robusta a multimodalidade; a restrição a outros clientes é a pergunta substantiva |
| **Secundária** | **Vendi Score normalizado** (`VS/n`) | Estúdio-período | Comunicação. "Vinte entregas valem por seis distintas" |
| **Controle** | **DSI** | Peça | Separa "ficou sem graça por dentro" de "ficou parecida com as outras" |
| Comparabilidade | Cosseno ao centroide *leave-one-out*, cru, ×100 | Peça | Reproduz Doshi e Hauser exatamente, para calibração |

### A restrição a "outros clientes" é a decisão substantiva

A M13 deixou aberto contra que grupo medir similaridade, e observou que a escolha define a pergunta. A resposta:

> **Peças de clientes diferentes, no mesmo estúdio e no mesmo período.**

Porque a tese do T3 é que a agência passa a entregar coisas parecidas **para marcas concorrentes** — que é exatamente o que destrói o valor que o cliente compra. Medir contra peças do mesmo cliente capturaria consistência de marca, que é desejável, e inverteria o sinal da interpretação.

**Consequência:** o desenho exige pelo menos dois clientes por estúdio-período com entregas comparáveis. Isso restringe a amostra e precisa entrar no critério de inclusão de estúdios da M17.

### Normalização por formato

Embeddings de textos de comprimentos muito diferentes não são comparáveis, e entregas de agência variam muito. Duas camadas:

1. **Estratificar por tipo de entrega** e calcular similaridade **dentro do tipo** — copy com copy, identidade visual com identidade visual.
2. **Controlar por extensão** na regressão, e reportar robustez com fragmentação em blocos de tamanho fixo com média dos embeddings.

---

## 5. O que implementar

```python
# Pseudocódigo. n peças no grupo g, embeddings E (n × d)

E_c = E - media_global_do_corpus          # correção de anisotropia
E_n = normalizar_l2(E_c)

K = E_n @ E_n.T                            # matriz de similaridade n × n

# Primária, por peça — só contra outros clientes
div_i = 1 - media( K[i, j] for j onde cliente_j != cliente_i )

# Secundária, por grupo
lam = autovalores(K / n)
lam = lam[lam > 0]
VS  = exp( -sum(lam * log(lam)) )
VS_norm = VS / n

# Comparabilidade com Doshi e Hauser (embeddings CRUS, sem centrar)
centroide_loo_i = media( E_bruto[j] for j != i )
sim_dh_i = 100 * cos( E_bruto[i], centroide_loo_i )
```

Sem dependência pesada: embeddings mais NumPy. O único custo real é a chamada de API de embedding por entrega, que é desprezível.

---

## Pendências geradas

- [ ] Fixar `n` mínimo por estúdio-período (proposta: 8) e a regra de agregação abaixo disso.
- [ ] Decidir o modelo de embedding e **congelar a versão** — trocar de modelo no meio da série quebra a comparabilidade, do mesmo modo que trocar de LLM quebra a do T2.
- [ ] Definir a taxonomia de tipos de entrega para a estratificação por formato.
- [ ] **M17 herda:** critério de inclusão de estúdio passa a exigir **pelo menos dois clientes por período** com entregas do mesmo tipo.
- [ ] **M18 herda:** registrar ferramenta e versão por entrega, para não confundir adoção com deriva de modelo (Karouzos et al.).
- [ ] Verificar se há implementação de referência do Vendi Score em Python mantida pelos autores, para não reimplementar.
- [ ] Testar DSI em português — o modelo de referência é BERT em inglês, e a validação de Johnson et al. é em inglês. **Se DSI não transferir para português, o desfecho de controle cai** e é preciso substituto.
