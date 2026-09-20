# M43 — Plano de figuras e tabelas

Executada em 2026-08-21. Convenção medida nos vencedores; **dados da Figura 1 extraídos e prontos para plotar**.

---

## Resumo

1. **"Model-Free Evidence" é convenção literal, não paráfrase minha.** Dois dos premiados de 2026 usam a expressão na própria legenda: *"Figure 2: Model-Free Evidence on Platform Performance"* e *"Figure 3 presents model-free evidence of…"*. **A Figura 1 do T2 deve usar o mesmo rótulo.**

2. **A Figura 1 pode ser construída hoje**, com dado de terceiros já em disco. Extraí os 45 pontos e as correlações. Estão na seção 2.

3. **O desenho da Figura 1 mudou depois de olhar os números.** Um gráfico único seria dominado por diferença de escala entre itens. **Três painéis, e a variância do modelo vira uma faixa horizontal visível — que é literalmente o achado "uma variância serve para todos".**

⚠️ **Não há `matplotlib` neste ambiente.** Entrego especificação e dados, não imagem.

---

## 1. As cinco peças

| # | Peça | Papel | Existe hoje? |
|---|---|---|---|
| **Fig. 1** | Variância humana × log da razão de variância, três painéis | **Evidência sem modelo** | ✅ Dados prontos |
| **Fig. 2** | Cobertura do intervalo, decrescente em *k* | **A figura do paper** | ❌ Depende da coleta |
| **Tab. 1** | Estratos, N por célula, descartes | Transparência amostral | Parcial (M41) |
| **Tab. 2** | Coeficiente principal em 4 especificações | **A estabilidade é o argumento** | ❌ |
| **Tab. 3** | Métricas por estrato | Panorama | ❌ |

Cinco é o teto para 12 páginas. A mediana dos vencedores é 8 tabelas e 6 figuras — **mas eles têm 37 páginas**.

---

## 2. Figura 1 — a evidência sem modelo

**Legenda proposta:** *Figure 1: Model-Free Evidence — Model Variance Does Not Track Population Variance*

### O desenho, e por que mudou

A primeira ideia era um gráfico de dispersão único. **Os dados desaconselham:** as variâncias humanas vivem em escalas incompatíveis — felicidade entre 0,35 e 0,66; participação religiosa entre 2,5 e 4,9; posição política entre 3,0 e 8,8. Um painel só seria dominado pela escala, e a correlação conjunta de −0,887 só existe sobre valores padronizados **dentro** de item.

**Desenho revisado: três painéis lado a lado, um por item, escala própria em cada.**

Cada painel traz:
- **Eixo x:** variância da população humana
- **Eixo y:** variância do modelo — **não** o log da razão
- **Linha diagonal tracejada** `y = x`: onde o modelo acertaria a dispersão
- **Linha horizontal sólida** na média da variância do modelo naquele item
- **Pontos** marcados por classe (Low, Middle, High), com o país no rótulo
- **`r` no canto** de cada painel

> ⭐ **A razão de plotar variância do modelo em vez do log da razão:** a linha horizontal é o achado. O leitor vê os pontos humanos se espalharem no eixo x enquanto os pontos do modelo permanecem colados numa faixa. **"Uma variância serve para todos" deixa de ser afirmação e vira coisa visível.**
>
> O log da razão vai para o eixo y da regressão, na Tabela 2 — não aqui.

### As correlações, para as legendas dos painéis

| Item | Escala | `r` (variância humana × ln VR) | n |
|---|---|---:|---:|
| Felicidade | 4 pontos | **−0,712** | 15 |
| Participação religiosa | 7 pontos | **−0,974** | 15 |
| Posição política | 10 pontos | **−0,977** | 15 |
| **Conjunto** (z dentro de item) | — | **−0,887** | 45 |

### Os 45 pontos

Calculados sobre o pacote de replicação público de Boelaert et al., comparando `FA-GPT-3` contra o WVS. Filtro de 50 observações mínimas por célula.

```
pais,classe,item,var_humana,var_modelo,ln_VR,n_humano
Australia,High,d_happy,0.3535,0.5664,0.4715,2522
Australia,High,d_religiousp,4.1165,5.1215,0.2184,2519
Australia,High,d_polpos,3.7407,5.5536,0.3952,2389
Australia,Low,d_happy,0.5022,0.6980,0.3293,196
Australia,Low,d_religiousp,4.7359,5.0067,0.0556,196
Australia,Low,d_polpos,5.0251,6.0447,0.1847,177
Australia,Middle,d_happy,0.4016,0.5421,0.3001,2416
Australia,Middle,d_religiousp,3.8214,4.9659,0.2620,2419
Australia,Middle,d_polpos,3.6264,5.5133,0.4189,2181
Germany,High,d_happy,0.3675,0.5505,0.4040,1742
Germany,High,d_religiousp,3.1858,5.1467,0.4796,1578
Germany,High,d_polpos,3.1040,5.5820,0.5869,1682
Germany,Low,d_happy,0.5444,0.6355,0.1547,509
Germany,Low,d_religiousp,3.3771,5.0615,0.4046,409
Germany,Low,d_polpos,3.2023,5.5566,0.5511,435
Germany,Middle,d_happy,0.4656,0.4980,0.0672,3228
Germany,Middle,d_religiousp,3.1907,5.0470,0.4586,2745
Germany,Middle,d_polpos,3.0200,5.5807,0.6140,2977
Mexico,High,d_happy,0.5176,0.5124,-0.0100,1317
Mexico,High,d_religiousp,3.9172,5.1681,0.2771,1323
Mexico,High,d_polpos,6.6020,5.6669,-0.1527,1195
Mexico,Low,d_happy,0.6570,0.6907,0.0499,1047
Mexico,Low,d_religiousp,3.0997,4.9162,0.4612,1049
Mexico,Low,d_polpos,8.7977,6.0554,-0.3735,849
Mexico,Middle,d_happy,0.5647,0.5581,-0.0117,2394
Mexico,Middle,d_religiousp,3.6534,5.0315,0.3201,2404
Mexico,Middle,d_polpos,7.4747,5.2281,-0.3575,2081
Russia,High,d_happy,0.4460,0.6217,0.3321,2867
Russia,High,d_religiousp,2.5382,5.2602,0.7287,2845
Russia,High,d_polpos,3.7916,5.6621,0.4010,1323
Russia,Low,d_happy,0.6742,0.6663,-0.0117,312
Russia,Low,d_religiousp,2.9469,5.2053,0.5689,313
Russia,Low,d_polpos,5.0778,5.9824,0.1640,140
Russia,Middle,d_happy,0.5092,0.5956,0.1567,2497
Russia,Middle,d_religiousp,2.5361,5.1865,0.7154,2514
Russia,Middle,d_polpos,4.1988,5.5571,0.2803,829
United_States,High,d_happy,0.3676,0.5031,0.3139,2447
United_States,High,d_religiousp,4.9074,5.2161,0.0610,2430
United_States,High,d_polpos,5.5384,5.3893,-0.0273,2373
United_States,Low,d_happy,0.5491,0.7806,0.3517,105
United_States,Low,d_religiousp,4.6283,5.8625,0.2364,104
United_States,Low,d_polpos,5.5175,5.8307,0.0552,89
United_States,Middle,d_happy,0.4313,0.4945,0.1368,2785
United_States,Middle,d_religiousp,5.0711,4.9992,-0.0143,2748
United_States,Middle,d_polpos,4.4320,5.2978,0.1784,2619
```

⚠️ **Nota importante sobre o estatuto desta figura.** Ela usa **dado de terceiros e desfecho de opinião**, não a coleta brasileira sobre consumo. **É evidência motivadora, e a legenda tem de dizer isso.** Se ela aparecer no paper, é como Figura 1 de motivação, com a coleta própria vindo depois.

⚠️ E a célula de classe baixa dos Estados Unidos tem **n = 89 a 105** — a menor do conjunto. Marcar visualmente ou reportar em nota.

---

## 3. Figura 2 — a figura do paper

**Legenda proposta:** *Figure 2: Naive Interval Coverage Declines as Synthetic Sample Size Increases*

| Elemento | Especificação |
|---|---|
| Eixo x | *k*, número de consultas por célula, em escala logarítmica: 10, 50, 100, 500, 1000 |
| Eixo y | Fração de células em que o intervalo ingênuo de 95% contém o valor da POF |
| **Linha de referência** | **Horizontal tracejada em 0,95** — o nominal |
| Curva | A cobertura observada, **descendo** |
| Anotação | O ponto em que a curva cruza 0,50 |
| Faixa | Intervalo de bootstrap entre réplicas |

> **A distância entre a linha de 0,95 e a curva é o achado.** E a inclinação negativa é o argumento: **coletar mais dado sintético não melhora nada — só estreita o intervalo em torno do lugar errado.**

Esta é a figura que a M33 recomendou como abertura da apresentação, porque comunica sem estatística.

---

## 4. As tabelas

### Tabela 1 — Estratos e cobertura amostral

Colunas: estrato (renda × região × escolaridade) · N de domicílios não ponderados · N ponderado · situação (mantido, colapsado, descartado).

**A coluna de situação é o ponto.** A M05 fixou mínimo de 100 domicílios não ponderados e a M12 exige que todo descarte seja reportado. **Uma tabela que só mostra o que ficou esconde a decisão.**

### Tabela 2 — A estabilidade do coeficiente ⭐

| | (1) bruto | (2) + controles | (3) + deriva Δ(q) | (4) + EF modelo e caminho |
|---|---|---|---|---|
| Correlação (H1) | | | | |
| Coeficiente de distância (H2) | | | | |
| Células | | | | |
| Erro padrão | bootstrap selvagem entre estratos | | | |

> **A leitura é horizontal.** Se o coeficiente sobrevive à coluna 3, o confundidor temporal está respondido **na tabela**, e não numa nota de rodapé. A M08 classificou esse confundidor como a ameaça número um; **esta linha é a resposta.**

### Tabela 3 — Panorama métrico por estrato

Uma linha por estrato do nível confirmatório. Colunas: `ln VR` · alinhamento por Wasserstein · distância de variação total · efeito de desenho · tamanho efetivo de amostra · cobertura.

**A coluna de tamanho efetivo é a que o profissional lê.** É onde "quinhentas respostas sintéticas valem doze respondentes humanos" aparece como número.

---

## 5. Regras de execução

Convenções de figura em paper acadêmico, que diferem de gráfico de apresentação:

| Regra | Razão |
|---|---|
| **Legível em escala de cinza** | Papers circulam impressos e em PDF monocromático. Codificar por **forma e posição**, nunca só por cor |
| **A legenda é autossuficiente** | O leitor de conferência folheia. Cada figura precisa ser compreensível sem o texto ao redor |
| **Sem grade pesada, sem sombra, sem efeito** | Não é peça de comunicação |
| **Eixos rotulados com unidade** | "Variância da população" e não "var" |
| **N em toda tabela** | Sempre |
| **Mesma casa decimal na coluna** | E dígitos tabulares |
| Fonte da figura igual à do texto | Coerência tipográfica |

**O que não fazer:** três painéis com escalas silenciosamente diferentes sem dizer — a diferença de escala **é** parte do achado e precisa estar rotulada; e nunca usar eixo y truncado numa figura cujo argumento é magnitude.

---

## Pendências geradas

- [ ] Plotar a Figura 1 a partir dos 45 pontos acima. Ambiente sem `matplotlib` — fazer localmente.
- [ ] Decidir se a Figura 1 entra no paper como motivação com dado de terceiros, ou se é substituída pela versão brasileira depois da coleta.
- [ ] Marcar visualmente as células de N pequeno na Figura 1.
- [ ] Definir o conjunto de valores de *k* da Figura 2 e confirmar que a coleta os suporta.
- [ ] **M44 herda:** cada linha de robustez precisa de destino — tabela do corpo ou menção no texto.
- [ ] **M48 herda:** a Figura 2 é a abertura da apresentação de 12 minutos.
