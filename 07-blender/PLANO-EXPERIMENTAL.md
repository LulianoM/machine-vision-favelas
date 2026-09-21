# Plano experimental: do sítio único à coleção de sítios

Aberto em 2026-09-21 [DESKTOP], depois de o primeiro braço sintético fechar em 1,6% de eficácia e
de os números de Kiefer et al. (2022) e Liao et al. (2026) serem conferidos na fonte. Substitui o
plano informal que estava só na conversa.

Fichas de conferência: `04-bibliografia/kiefer-2022-numeros-conferidos.md` e
`04-bibliografia/liao-2026-numeros-conferidos.md`. Nenhum número abaixo é citado de memória.

## 1. Onde estamos

| | mAP50 |
|---|---|
| S-nadir no próprio sintético | 0,79 |
| S-nadir zero-shot no VisDrone | 0,0102 |
| R pareado (1.106 imagens reais, hiperparâmetros idênticos) | 0,631 |
| razão de eficácia | **1,6%** |

Comandos e arquivos em `06-resultados/sim2real_s_nadir_4k.json` e
`C:\arma3-favela\blender\resultados\r_pareado.json`.

O braço oblíquo, que separaria geometria de captura de qualidade de síntese, saiu com zero caixas
por um defeito de câmera já corrigido (commit `0ad4984`). Precisa ser refeito antes de qualquer
conclusão sobre a causa do 1,6%.

## 2. O que a literatura de fato sustenta, e o que ela NÃO sustenta

### Sustenta: variação de luz, clima e ângulo é o maior ganho isolado

Liao et al., Tabela 4, mAP50, detecção de veículo: tirar a randomização de clima e ângulo custa
**30,4 pontos no YOLOv11** (74,5 cai para 38,7). A média entre seis detectores é +17,5. Já
fazemos isso, com seis regimes de tempo. **Manter.**

Kiefer et al., Tabela VII, reforça por outro ângulo: alinhar a distribuição de captura ao real
sobe o sintético PURO em +4,1 mAP@50 (horário) e +7,4 (ângulo de câmera), e o sintético com dado
real em +0,2 e +0,0. **Alinhamento de captura só importa quando não há dado real, que é o nosso
caso exato.** No caso do ângulo, eles conseguiram o ganho jogando dado fora, ficando só com o
subconjunto que casa com o real. Menos dado, melhor alinhado, ganhou de mais dado desalinhado.

### Sustenta: variedade de lugar, mas só no regime fora de domínio

Kiefer gera as 40.000 imagens por travessias aleatórias do mapa do GTA, escolhendo um novo destino
a cada 60 segundos, e avalia no VisDrone, que são 14 cidades. Regime de variedade.

### NÃO sustenta: que mais imagens do mesmo lugar resolva

Liao usa 4.659 imagens de **dez trajetórias sobre um único sítio reconstruído**. O ganho dele não
vem do número de imagens, vem de o sítio ser o mesmo que o do teste.

Kiefer, Figura 2, mede explicitamente o efeito do tamanho do conjunto sintético e encontra
**retorno decrescente**: o ganho por imagem cai conforme o conjunto cresce. Ele também encontra
que o benefício do sintético é **desproporcionalmente maior quanto MENOS dado real existe**.

Conclusão para nós: ir de 180 para 4.600 imagens do mesmo morro é o eixo de menor retorno dos
três. A intuição do autor (vários morros diferentes, um com avenida no meio, outro sem mata, etc.)
está certa e é o que Kiefer faz.

### A tensão que o plano não pode esconder

Liao et al., Tabela 5: trocar base fotogramétrica por assets genéricos custa **27,0 pontos no
YOLOv11** (74,5 para 50,2). Na taxonomia deles, o nosso `gen_morro.py` está do lado dos assets
genéricos, não do lado da fotogrametria.

Mas o teste deles é **no mesmo sítio que reconstruíram**. O número diz "gêmeo digital de X ajuda a
detectar em X". Não diz nada sobre detectar em Y. E o nosso teste é em Y (o VisDrone), porque não
existe imagem aérea anotada de favela que possamos usar.

O braço fotogramétrico existe aqui (`gen_odm.py`, malha do OpenDroneMap sobre as 567 fotos da
PCERJ) e é exatamente o que não pode ser publicado nem ilustrado. Isso é uma restrição do projeto,
não um descuido, e entra no artigo como tal.

## 3. Um problema de método no nosso próprio número

Liao, Tabela 3, YOLOv11 no VisDrone sem nunca ter visto VisDrone:

| treinado em | tipo | mAP50 no VisDrone | razão sobre o real |
|---|---|---|---|
| UAV-RealScene (Shenzhen) | real | 36,4 | - |
| UAV-SynthScene | sintético | 34,2 | 94% |
| UEMM-Air (genéricos) | sintético | 29,3 | 80% |

O denominador deles, 36,4, é um modelo treinado em dado real de **outro lugar** e testado no
VisDrone. O nosso denominador, 63,1, é um modelo treinado no **próprio VisDrone**.

São perguntas diferentes:

- nosso 1,6% responde: *quanto o sintético recupera do que o dado real do próprio alvo entrega?*
- o 94% deles responde: *quanto o sintético recupera do que o dado real de outro lugar entrega?*

Os dois são legítimos e o primeiro é mais duro. Reportar só o primeiro, sem o segundo, faz o
método parecer pior do que a literatura sem dizer que a régua mudou. **Vamos reportar os dois.**

## 4. O plano, em quatro frentes

### Frente A: fechar o braço 100% sintético de sítio único (o que já está em curso)

1. Refazer o oblíquo com a câmera corrigida. 2,6 h de render, 7 min de treino.
   Decide se o 1,6% é problema de síntese ou de geometria de captura.
2. Curva de eficácia por pitch: nadir, 30 graus, 50 graus. Três pontos, não um.
3. **Braço real fora de domínio**, para ter o denominador da literatura. Treinar em um conjunto
   aéreo real que não seja o VisDrone e testar no VisDrone. Candidato: usar as próprias imagens
   reais que já estão no disco em outro recorte, ou declarar a limitação se não houver fonte.

Entrega: o artigo passa a ter razão de eficácia com dois denominadores declarados.

### Frente B: coleção de sítios (o que o autor propôs, e que a literatura sustenta)

O gerador já é procedural: terreno, parcelamento, ruas e vegetação saem de semente. Gerar N sítios
é mudar a semente e alguns parâmetros de morfologia, não escrever código novo.

Eixos de variação a expor como opção de linha de comando:

| eixo | hoje | proposto |
|---|---|---|
| relevo | um morro assimétrico fixo | plano, morro único, dois morros, encosta |
| via principal | não existe | avenida com carros cortando o núcleo, ou ausente |
| densidade | um valor | esparsa, média, muito adensada |
| altura média | 1 a 3 pavimentos | variar por sítio |
| mata | anel em volta | anel, manchas internas, ausente |
| água | não existe | valão, canal |

**Orçamento igual, variedade maior.** Em vez de 4.600 imagens de um morro, 40 sítios com 115
imagens cada. Mesmo custo de render, e é o desenho do Kiefer.

Antes de gastar o orçamento inteiro, rodar **um teste de dose**: 4 sítios x 45 imagens contra 1
sítio x 180 imagens, mesmo total. Se a variedade de sítio não mover a eficácia nesse recorte
pequeno, não move em escala, e o orçamento vai para outro eixo. Isso custa um render de 180
imagens, que é o que já sabemos fazer.

### Frente C: modelo misto, sintético mais uma fatia de real

É o passo 2 do plano do autor, e é o que a literatura mostra funcionar. Kiefer: de 10,2 sintético
puro para 45,0 com transferência. Liao: sintético sozinho já chega perto do real no sítio casado.

Desenho: pré-treino no sintético, transferência com 5%, 10% e 20% do VisDrone train. Comparar
contra treinar só com a mesma fatia de real. A pergunta é se o pré-treino sintético vale alguma
coisa, e o Kiefer prevê que o ganho é **maior quanto menor a fatia de real**, o que é testável.

Custo: são treinos, não renders. Cerca de 4 h cada, sem GPU de render competindo.

### Frente D: a pergunta armada

Corre em paralelo, já está na fila (etapa 16, render a 75 m com objetos confundíveis). Independe
das frentes acima e responde a outra pergunta: com que frequência um detector chama de arma uma
vassoura, em função da distância de amostragem no solo.

## 5. Ordem e custo

| ordem | frente | custo de GPU | o que fecha |
|---|---|---|---|
| 1 | A1, oblíquo refeito | 3 h | causa do 1,6% |
| 2 | D, armado a 75 m | em curso, termina hoje | curva de falso positivo |
| 3 | B, teste de dose de variedade | 8 h | se vale gerar N sítios |
| 4 | C, misto com 5, 10 e 20% | 12 h | o segundo modelo do artigo |
| 5 | A2, curva por pitch | 9 h | dose-resposta da geometria |
| 6 | B em escala, se o teste de dose der sinal | 40 h | o corpus grande |

As etapas 1 a 4 cabem em quatro dias de máquina e já dão ao artigo os dois modelos que o autor
pediu, com denominador duplo e com a causa do 1,6% identificada. A etapa 6 só se justifica se a 3
der sinal.

## 6. O que decidir antes de começar

1. Existe alguma fonte de imagem aérea real anotada, que não o VisDrone, para o braço real fora de
   domínio da Frente A3? Sem isso, a limitação entra declarada no texto.
2. O braço fotogramétrico da PCERJ entra como resultado medido (sem imagem publicada) ou fica de
   fora do artigo? A restrição de dado permite o número, não a figura.
3. A Frente B em escala precisa de decisão de orçamento: 40 h de render é uma semana de máquina
   compartilhada com o resto.
