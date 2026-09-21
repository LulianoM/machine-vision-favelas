# Liao et al. (2026), números conferidos na fonte

Conferido em 2026-09-21 [DESKTOP] lendo o artigo aberto no site do periódico. O DOI já constava
conferido no Crossref; o que faltava, e que `01-artigo/PENDENCIAS.md` registrava como pendente,
eram os valores das ablações, que estavam nas nossas notas sem terem sido lidos no texto.

**Título:** Bridging the Sim2Real Gap in UAV Remote Sensing: A High-Fidelity Synthetic Data
Framework for Vehicle Detection
**Autores:** Fuping Liao, Yan Liu, Wei Xu, Xingqi Wang, Gang Liu, Kun Yang, Jiahao Li
**Veículo:** Remote Sensing 18(2), 361, publicado em 21/01/2026. DOI 10.3390/rs18020361
**Métrica em todas as tabelas abaixo:** mAP50, protocolo COCO.

## Aviso de escopo, que precisa aparecer sempre que citarmos

O objeto detectado é **veículo**, não pessoa. Carro em imagem aérea é alvo grande, rígido, de alto
contraste contra asfalto. Pessoa a 150 m tem 17 px e contraste baixo. Nenhum número abaixo
transfere direto para o nosso caso, e citá-los como se transferisse seria o tipo de salto que o
próprio artigo que estamos escrevendo critica.

## Os conjuntos

| conjunto | o que é | imagens |
|---|---|---|
| UAV-RealScene | real, DJI Mavic 3T, Shenzhen, área de ~1.000 x 2.000 m | 8.736 (8.000 treino) |
| UAV-SynthScene | sintético deles, fotogrametria oblíqua da MESMA área | 4.659, 1920x1536 |
| UEMM-Air | sintético de terceiros, Unreal com **assets genéricos** | grande |
| SkyScenes | sintético de terceiros, simulador de alta fidelidade | grande |
| VisDrone | real, 14 cidades chinesas, usado como referência NÃO vista | 6.471 treino |

O UAV-SynthScene sai de **dez trajetórias de voo** sobre **um único sítio reconstruído**, com
altitude sorteada entre 50 e 300 m e pitch entre -45 e -90 graus. Ou seja: a variedade deles é de
ponto de vista e de clima, não de lugar.

## Tabela 4: tirar a variação de luz, clima e ângulo

> Ablation study on the impact of diversified rendering.

| detector | estático (geral) | estático (truncado) | diversificado (geral) | diversificado (truncado) | ganho médio |
|---|---|---|---|---|---|
| **YOLOv11** | **38,7** | 27,7 | **74,5** | 52,6 | **+30,4** |
| DINO | 78,7 | 44,2 | 87,9 | 73,0 | +19,0 |
| RT-DETR | 68,1 | 44,6 | 84,4 | 68,1 | +19,9 |
| Média | 71,1 | 43,5 | 84,5 | 65,0 | +17,5 |

A nota antiga do projeto dizia "cerca de 10 pontos, cerca de 20 em objetos truncados". Confere com
o texto corrido do artigo. Pela tabela, a média vai de 71,1 para 84,5 no geral (+13,4) e de 43,5
para 65,0 no truncado (+21,5). **No YOLO, que é o nosso detector, o efeito é muito maior: +30,4.**

## Tabela 5: trocar a base fotogramétrica por assets genéricos

> Impact of high-fidelity scene reconstruction on detector performance.

| detector | assets genéricos | cena fotogramétrica | ganho |
|---|---|---|---|
| **YOLOv11** | **50,2** | **74,5** | **+27,0** |
| DINO | 66,5 | 87,9 | +21,8 |
| RT-DETR | 61,8 | 84,4 | +27,5 |
| Média | 62,3 | 84,5 | +23,3 |

A nota antiga dizia 22,5 pontos. **O artigo é inconsistente consigo mesmo aqui:** a seção de
resultados escreve "+22.5 mAP50 points" e a discussão e a própria Tabela 5 dizem +23,3. A
diferença é entre a média da coluna "All" (62,3 para 84,5, +22,2) e a média dos ganhos por
detector (+23,3). Citar como "cerca de 22 a 23 pontos" e não como um valor exato.

## Tabela 3: transferência para o VisDrone sem ver o VisDrone

É a tabela mais próxima do nosso desenho, e a que mais muda o que devemos fazer.

| detector | treinado em | tipo | mAP50 no VisDrone |
|---|---|---|---|
| **YOLOv11** | UAV-RealScene | real | **36,4** |
| **YOLOv11** | UAV-SynthScene | sintético | **34,2** |
| YOLOv11 | SkyScenes | sintético | 33,4 |
| YOLOv11 | UEMM-Air (genéricos) | sintético | 29,3 |
| DINO | UAV-RealScene | real | 66,3 |
| DINO | UAV-SynthScene | sintético | 58,9 |

**O denominador aqui é outro.** O "real" da tabela é um modelo treinado em Shenzhen e testado no
VisDrone, ou seja **também fora do domínio**. O nosso braço real foi treinado no PRÓPRIO VisDrone
e testado no VisDrone, que é dentro do domínio, e marcou 63,1.

Consequência direta para a nossa razão de eficácia: estamos dividindo por um denominador muito
mais duro que o da literatura. Eles comparam sintético contra real-fora-de-domínio (34,2 sobre
36,4, ou 94%); nós comparamos sintético contra real-dentro-do-domínio (1,02 sobre 63,1, ou 1,6%).
Os dois números medem coisas diferentes e não podem ser postos lado a lado sem essa ressalva.

## O que isto decide no nosso desenho

1. **Manter a randomização de clima.** É o maior ganho isolado no YOLO (+30,4) e já a temos.
2. **A base procedural é o nosso ponto fraco declarado.** O gerador `gen_morro.py` está, na
   taxonomia deles, do lado dos "assets genéricos", não do lado da fotogrametria. O braço
   fotogramétrico existe (`gen_odm.py`, malha do OpenDroneMap sobre as fotos da PCERJ) e é
   justamente o que não pode ser ilustrado nem publicado. Essa tensão é do projeto e precisa ser
   dita no artigo, não contornada.
3. **A tese deles é geoespecífica.** O +23 pontos é medido testando no MESMO sítio reconstruído.
   Diz que gêmeo digital de X ajuda a detectar em X. Não diz que gêmeo digital de X ajuda a
   detectar em Y, e é Y (o VisDrone) que nós medimos.
4. **Acrescentar um braço real fora do domínio** ao nosso desenho, para termos o denominador que a
   literatura usa além do que já temos.
