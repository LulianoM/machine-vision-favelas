---
tags: [projeto, ml, blender, fotogrametria, odm, favela, bounding-box, visao-computacional, dataset-sintetico]
criado: 2026-09-11
atualizado: 2026-09-12
projeto: Machine-Vision-Favelas
status: em-andamento
---

# Machine Vision Favelas: mapa 3D do Jacarezinho e dataset sintético

> **O Arma 3 saiu do pipeline em 12/09/2026.** O gerador agora é o **Blender**, em cima da
> **fotogrametria das fotos reais da PCERJ**. O histórico do Arma 3 está no fim desta nota.

## Objetivo

Artigo FGV EBAPE **"Machine Vision from the Global South: Developing an AI Model for Vertical Favelas"**.
Autor: Luciano ("Felipe") Martins Figueira; orientador: prof. Hélio Arthur Reis Irigaray.
Validar o pipeline da Seção 7: cena sintética com anotação automática, treino de detector, teste em dado real.

## Por que o Arma 3 saiu

O jogo não expõe controles nativos, então a automação dependia de OCR e cliques na tela. O Blender roda
100% headless, com seed determinística, e a anotação sai exata por projeção de vértices mais ray cast de
oclusão. O próprio README-PIPELINE de 2022 já dizia que nenhum mapa do Arma 3 reproduz a morfologia de
favela e apontava Blender procedural como o passo seguinte.

## O que existe hoje

| Entrega | Caminho |
|---|---|
| Mapa 3D navegável do Jacarezinho | `C:\arma3-favela\odm\jacarezinho.blend` (321 MB) |
| Vídeo do voo | `C:\arma3-favela\odm\voo_jacarezinho.mp4` |
| Dataset procedural + detector | `dataset_v3_tiles`, `runs/detect/blender_v3_tiles2` |
| Dataset sobre malha real + detector | `dataset_odm_tiles`, `runs/detect/blender_odm_tiles` |
| Registro completo para o artigo | `C:\arma3-favela\blender\RESULTADOS-BLENDER.md` |
| Manual dos comandos | `C:\arma3-favela\blender\README-BLENDER.md` |

Mapa: 1.368 x 1.115 m, 5,1 M faces de fotogrametria + 2,5 M de terreno, 100 pessoas, 5 câmeras e voo animado.
Para navegar: abrir o `.blend`, Shift + acento grave na viewport, depois W A S D.

## Fotogrametria (OpenDroneMap 3.6.2)

As 567 fotos de ago/2022 (Zenmuse Z30, 1080p, nadir, 150 m de altura relativa, passo de 21,6 m).
**As pastas "output" do Drive estavam vazias: o processamento de 2022 se perdeu e foi refeito do zero.**

| Setor | Fotos | Ortomosaico | Área |
|---|---|---|---|
| Sudoeste | 217 | 7,4 cm/px | 707 x 680 m |
| Nordeste | 350 | 6,4 cm/px | 983 x 947 m |

Os dois setores encaixam sozinhos pelo georreferenciamento UTM, sem ajuste manual.

## Resultados do detector

| Treino | Precisão | Recolocação | mAP50 | mAP50-95 |
|---|---|---|---|---|
| 4K reduzido para 1536 | 0,272 | 0,186 | 0,116 | 0,031 |
| ladrilhos 1280 em escala nativa | 0,737 | 0,497 | 0,561 | 0,238 |
| ladrilhos sobre a malha real | 0,616 | 0,639 | 0,646 | 0,340 |

**Achado principal:** o ladrilhamento sozinho multiplicou o mAP50 por 4,8, sem mudar o dataset.
Uma pessoa a 100 m tem de 11 a 41 px no 4K; reduzindo para 1536 ela vira de 4 a 16 px, abaixo do
stride mínimo do YOLO. Em imagem aérea de favela, a escala de treino pesa mais que o volume de dados.

## Duas ressalvas obrigatórias no artigo

1. A distinção armado/desarmado funciona no sintético (mAP50 0,591 contra 0,532), mas lá a arma é
   sempre o mesmo modelo, na mesma posição e com o mesmo contraste. **Sim-to-real não foi medido.**
2. As 567 fotos são todas em nadir a 150 m. Não há textura de fachada, então o mapa se sustenta de
   cima até ~45 m e derrete ao nível da rua. Fachada exigiria voo novo com câmera oblíqua.

## Armadilhas técnicas resolvidas

- MPFB entrega tudo com SUBSURF: render caiu de 23 min para 20 s ao remover. Era também o motivo de
  o dataset sobre a malha real levar 10 min por imagem (virou 18 s).
- Textura de fotogrametria já tem sol embutido: iluminar com ambiente neutro e céu só por raio de câmera.
- `train_yolo.py` do pacote original trava no Windows (multiprocessing); usar `train_yolo_win.py`.
- Blender 5 mudou a API de vídeo, de fcurves e de céu; `matrix_world` exige `view_layer.update()`.
- ODM só remalha com a máquina livre; disputando RAM ele para de consumir CPU e nunca termina.
- `sky.sun_rotation` é azimute de bússola (0 = norte, 90 = leste), verificado empiricamente.

## Próximos passos

- [x] Fotogrametria dos dois setores e mapa 3D navegável
- [x] Dataset procedural e dataset sobre a malha real, com detectores treinados
- [ ] Sim-to-real no VisDrone: zero-shot e com ajuste fino de 5%
- [ ] Anotar à mão ~50 pessoas nas fotos reais para teste interno
- [ ] Segundo experimento: trocar anotação de pessoa por edificação (pavimentos, adição em laje)

## Ética

Sem imagem identificando moradores. Sem coordenadas em nível de endereço. As fotos e tudo derivado
delas são dados operacionais da PCERJ: uso interno, sem redistribuição.

## Histórico: tentativa com Arma 3 (11/09/2026)

Chegou a funcionar até a geração da missão. O `capturaDataset.sqf` projetava os 8 cantos do
`boundingBoxReal` via `modelToWorldVisual` + `worldToScreen` e logava `DSIMG`/`DSLBL` no `.rpt`.
A automação de GUI dependia de OCR do Windows (`C:\arma3-favela\ocr.ps1`) porque o jogo não expõe
controles, e só cliques em foreground (SendInput) chegavam ao jogo. Base escolhida: Tanoa, com os
objetos `Land_Slum_01/02/03_F` perto de Georgetown `[5396, 10335]`. Scripts originais preservados em
`C:\arma3-favela\projeto_contexto\PROJETO-MACHINE-VISION-FAVELAS\02-projeto-ufrj-2022/arma3-2022\`.

## Referências

- Pipeline Blender: `C:\arma3-favela\blender\`
- Pacote de contexto original: `C:\arma3-favela\projeto_contexto\PROJETO-MACHINE-VISION-FAVELAS\`
- Histórico 2022 (UFRJ, Fábio Guimarães + Claudio Miceli): `...\02-projeto-ufrj-2022\`
