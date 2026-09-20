# Desenho do experimento de sim-to-real

Aberto em 2026-09-20 [DESKTOP]. Define os modelos, os conjuntos e o que cada número responde.
Nenhum número entra no artigo sem estar aqui com o comando que o gerou.

## O problema com um número só

O projeto tinha, até hoje, apenas métricas de sintético avaliado em sintético (melhor:
`cid150_s`, mAP50 0,676). Isso é o modelo se avaliando no mundo em que nasceu, e não diz nada
sobre transferência. Mas o inverso também é verdade: um zero-shot de mAP50 0,0055 no VisDrone,
sozinho, também não diz nada, porque não há régua. Sem saber quanto um modelo treinado em dado
REAL alcança no mesmo conjunto de teste, não dá para dizer se 0,0055 é fracasso ou se o conjunto
é simplesmente difícil.

## Os três modelos

Todos YOLO11s, mesmo teste, mesma métrica.

| Modelo | Treino | O que responde |
|---|---|---|
| **R** (real) | VisDrone-DET train, 6.471 imagens, 106.396 caixas de pessoa | Teto alcançável no conjunto de teste. É a régua |
| **S-nadir** | Sintético do `gen_morro.py`, nadir a 150 m, 4K, seis climas | A nossa metodologia, com a geometria de captura do voo real de 2022 |
| **S-obliqua** | Mesmo gerador, câmera oblíqua e baixa, calibrada na geometria do VisDrone | Se o sintético falha por ser sintético, ou por a captura não bater |

Teste comum: VisDrone-DET val, 548 imagens, 13.969 caixas, classe única `pessoa`.

## As métricas que saem daí

- **Eficácia do sintético** = mAP50(S) dividido por mAP50(R). É o número honesto: quanto do teto
  o sintético alcança sem nenhuma imagem real.
- **Custo da geometria de captura** = mAP50(S-obliqua) menos mAP50(S-nadir). Se for grande, a
  lição é que o ângulo de captura pesa mais que o realismo da cena, o que conversa direto com o
  achado de Liao et al. sobre origem da geometria.
- **Sim-to-real com dado real parcial**: ajuste fino de S com 5 e 10% do VisDrone train, contra R
  treinado com a mesma fração. Diz quanto dado real o pré-treino sintético economiza.

## Por que a câmera oblíqua entrou

Medido em 2026-09-20 sobre as 13.969 caixas reais do VisDrone val e as 4.856 do `cid150`:

| Conjunto | Largura mediana | Altura mediana | h/w mediana | h/w p90 |
|---|---|---|---|---|
| VisDrone val (real) | 12,0 px | 25,0 px | **2,20** | 3,17 |
| `cid150` (nadir a 150 m) | 18,5 px | 22,9 px | **1,24** | 2,07 |

A ÁREA do alvo é parecida nos dois. A FORMA não é. Uma razão altura sobre largura de 2,20
significa pessoa em pé vista de câmera oblíqua; 1,24 significa planta de cabeça e ombro vista de
cima. O detector aprende a silhueta, não a área, então esse é o domain shift que importa, e ele
não aparece em nenhuma métrica de tamanho.

O preset `--obliqua` do gerador foi calibrado nesse número, não em estimativa.

## Correção registrada

Uma versão anterior deste raciocínio afirmava que o VisDrone tem alvo 2,49 vezes maior que o
nosso sintético, e tratava isso como domain shift de altitude. Era artefato de uma escolha de
resolução de render (1920x1080 em vez de 4K), não propriedade do projeto. Em 4K o alvo mediano
do `cid150` é 24,6 px contra 25,0 px do VisDrone, praticamente iguais.

## Ressalva que precisa entrar no artigo

A Zenmuse Z30 do voo real de 2022 grava em 1080p. A 150 m isso dá 9,76 cm por pixel e uma pessoa
de cerca de 10 px, com 25% das caixas abaixo do menor stride do YOLO. Renderizar em 4K dá 4,88
cm/px e alvo de cerca de 24 px, ou seja, o sintético em 4K é mais fácil que um quadro isolado da
câmera real. O ortomosaico do OpenDroneMap, por ser costurado de quadros sobrepostos, sai a 6,4
e 7,4 cm/px, portanto melhor que o quadro isolado e pior que o render em 4K. Isso precisa ser
declarado como limitação, e o número do artigo deve dizer a que GSD se refere.
