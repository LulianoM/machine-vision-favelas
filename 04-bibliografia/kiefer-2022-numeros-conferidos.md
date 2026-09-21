# Kiefer, Ott e Zell (2022), números conferidos na fonte

Conferido em 2026-09-21 [DESKTOP] no PDF do arXiv 2112.12252, que é a versão do mesmo trabalho
publicado na ICPR 2022 (DOI 10.1109/ICPR56361.2022.9956710).

**Título:** Leveraging Synthetic Data in Object Detection on Unmanned Aerial Vehicles
**Autores:** Benjamin Kiefer, David Ott, Andreas Zell

## Por que esta ficha existe

`docs/CONTEXTO.md` registrava "Kiefer, Ott e Zell, ICPR 2022: 1,2 a 2,4 mAP no VisDrone" sem dizer
qual métrica, e eu usei esse intervalo em 2026-09-21 para dizer que o nosso resultado estava "na
mesma ordem de grandeza". Conferido na fonte, **a métrica está certa e o intervalo está
incompleto, de um jeito que inverte a conclusão**.

## Tabela III da fonte, verbatim

> TABLE III. PERFORMANCE OF OBJECT DETECTORS FOR DIFFERENT TRAINING STRATEGIES GIVEN BY MAP@50.

Linhas do VisDrone, nas três estratégias:

| detector | Synthetic | Real | SyntheticToReal | razão sintético sobre real |
|---|---|---|---|---|
| EfficientDet-D0 | 1,2 | 24,6 | 27,2 | 4,9% |
| Faster R-CNN | 2,4 | 48,6 | 51,2 | 4,9% |
| **YOLO** | **10,2** | **43,9** | **45,0** | **23,2%** |

A métrica é **mAP@50**, declarada no título da tabela. Sobre isso a nota antiga estava certa.

O "1,2 a 2,4" são as duas primeiras linhas. **A linha do YOLO, que é o detector que nós usamos,
está em 10,2, e ficou de fora da nota.** Citar o intervalo sem ela seleciona justamente os dois
piores casos, e foi o que me fez dizer que 1,6% era comparável. Não é.

## Tabela V, verbatim

> TABLE V. EFFECT OF COCO PRE-TRAINED WEIGHTS ON PERFORMANCE GIVEN BY MAP@50 EVALUATED ON VISDRONE.

| | pesos aleatórios | pré-treinado em COCO |
|---|---|---|
| Real | 43,1 | 43,9 |
| Synthetic | 7,5 | 10,2 |
| SyntheticToReal | 44,7 | 45,0 |

Confirma que o 10,2 do YOLO é com inicialização COCO, que é a mesma que usamos (`yolo11s.pt`).

## Tabela IV: tamanho dos conjuntos

| conjunto | treino | val | teste |
|---|---|---|---|
| VisDrone (real) | 6.471 | 548 | 1.610 |
| DGTA-VisDrone (sintético deles) | **40.000** | 10.000 | - |

O corpus sintético deles tem **40.000 imagens de treino**. O nosso tem 1.106 ladrilhos vindos de
180 cenas de um único sítio. São 36 vezes menos imagens, e a diferença de variedade de lugar é
maior ainda: as 180 cenas são o mesmo morro com as mesmas casas, variando câmera, clima e pessoas.

## Onde ficamos

| | sintético | real | razão |
|---|---|---|---|
| Kiefer, YOLO, 10 classes | 10,2 | 43,9 | 23,2% |
| **nosso, YOLO11s, pessoa** | **1,02** | **63,1** | **1,6%** |

Comparar os valores absolutos não vale: eles medem 10 classes e nós uma só, fundida. A **razão** é
o que dá para comparar, e por ela estamos catorze vezes abaixo da referência.

Três causas candidatas, em ordem de tamanho provável, e nenhuma medida ainda em separado:

1. **Volume e variedade.** 1.106 ladrilhos de um sítio contra 40.000 imagens de cidade inteira.
2. **Conteúdo de cena.** O sintético deles é GTA V, cidade com tráfego, que é o mesmo domínio do
   VisDrone. O nosso é um morro. O VisDrone não contém nada parecido com favela.
3. **Geometria de captura.** Nosso nadir a 150 m dá alvo quadrado (h/w 0,98), o VisDrone dá alvo
   alto e estreito (h/w 2,00). Medido em `06-resultados/alvo_4k_vs_visdrone.csv`.

Note que a causa 2 é estrutural e não tem conserto: o artigo é sobre favela e o benchmark público
não tem favela. Isso já está dito na seção 11.2 do manuscrito e agora tem número por trás.

## Achado adicional, útil para o desenho do experimento

Kiefer também reporta o ganho de alinhar parâmetros de captura (Tabela VII): alinhar o horário do
dia sobe o sintético puro em +4,1 mAP@50 e o pré-treino sintético em apenas +0,2. Ou seja, o
alinhamento de captura pesa muito mais quando NÃO há dado real, que é exatamente o nosso caso.
Isso sustenta a prioridade do braço oblíquo.
