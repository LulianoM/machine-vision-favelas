# O que o desktop acrescenta ao levantamento de 12/09

Escrito em 2026-09-18 [DESKTOP], na reconciliação.

## Primeiro, o que NÃO existe

Não há pesquisa feita no desktop a partir do e-mail de 12/09. Procurei em `C:\arma3-favela\`, no cofre do Obsidian, em Documentos, Downloads e na transcrição completa da sessão de 12 e 13/09: nenhuma leitura de Liao et al., nenhuma leitura do G-MAD, nenhum recorte da ortofoto do IPP, nenhum dado LiDAR, nenhuma decisão de engine escrita. Esta pasta existe para dizer isso às claras e para registrar como o que o desktop FEZ conversa com o que o levantamento RECOMENDA. Os próximos passos do e-mail (escrever ao IPP, ler os dois artigos, baixar a ortofoto, prova de conceito de 500 imagens) continuam todos em aberto.

## O que é novo em relação ao levantamento

O desktop chegou, por outro caminho e antes do e-mail, à mesma "resposta curta" do levantamento: geometria real por fotogrametria, e sobre ela variação de sol, ângulo e câmera. A diferença é a fonte: fotos de drone da PCERJ de 2022 processadas no OpenDroneMap, e não a ortofoto do IPP. Detalhes em `06-resultados/RESULTADOS.md`.

| Tema do levantamento | O que o desktop mostrou na prática |
|---|---|
| "A origem da geometria decide" (Liao et al.) | Coerente, sem ser prova: o braço sobre malha real teve recall e mAP50-95 maiores que o procedural (0,639 e 0,340 contra 0,497 e 0,238), mas em conjuntos de validação diferentes. Não é ablação controlada |
| Delighting como problema a planejar | Confirmado como o obstáculo central. A textura do ODM tem a sombra das 11h55 gravada. Contorno 1: luz ambiente neutra, sol preso à direção real (perde a variação de sol). Contorno 2, igual à "mitigação barata" da seção 7 do levantamento: prédios segmentados do DSM, paredes com PBR, cor de telhado amostrada do ortomosaico. É o `dataset_cid150`, e nele o sol varia livremente |
| Engine: levantamento recomenda Blender 4.2 + BlenderProc com GPU alugada, ou ARMA 3 + G-MAD, ou Unreal | Usado: Blender 5.2.1 puro (sem BlenderProc), Cycles com OptiX numa RTX 2060 local. 18 a 46 s por imagem 4K. 560 imagens em 6 h 38 min. Não foi preciso alugar GPU para esse volume. ARMA 3 tentado e abandonado |
| Hardware mínimo | RTX 2060 de 6 GB deu conta de render e de treino YOLO11s em 1280 px. O gargalo foi RAM (32 GB): Blender, ODM e DataLoader juntos derrubaram um treino |
| Fotogrametria só com nadir | Achado novo: as 567 fotos são todas em nadir a 150 m. Sem oblíqua não há fachada. O mapa serve de cima até cerca de 45 m. Para morfologia vertical, o levantamento de 2022 é o dado errado |
| Escala do alvo | Achado novo, e o mais forte: pessoa a 100 m tem 11 a 41 px em 4K. Treinar com a imagem reduzida a 1536 px dá mAP50 de 0,116; treinar em ladrilhos de 1280 px em escala nativa dá 0,561, nas mesmas 120 imagens |
| blender-mcp | O levantamento alerta para CVEs. O desktop usa a versão 1.9.1 fora de container (ver `docs/DIVERGENCIAS.md`, item 4) |
| Google 3D Tiles | Scripts chegaram a ser escritos no desktop e o caminho foi vetado pelo autor. Bate com a proibição contratual do levantamento |

## O que muda no desenho do experimento

1. Já existe uma "cidade de sólidos" construída sobre DSM real. Trocar a fonte (DSM e ortomosaico da PCERJ) pela ortofoto de 15 cm do IPP, e pelo MDS ou LiDAR se o IPP liberar, dá um braço de geometria real que é aberto e publicável. O código (`segmenta_predios.py`, `build_cidade.py`, `gen_cidade.py`) já lê GeoTIFF; a adaptação é de caminho e de resolução.
2. O ladrilhamento passa a ser parte fixa do método, tanto no treino quanto na inferência (`tile_dataset.py`, `eval_cidade.py`).
3. A ablação de Liao et al. pode ser reproduzida quase de graça: o mesmo gerador com sol preso (como no `dataset_odm`) contra sol livre (como no `cid150`), mesma cidade, mesmo teste.
4. O sim-to-real continua por fazer e é o que falta para o artigo: VisDrone em classe única de pessoa, e cerca de 50 pessoas anotadas à mão nas fotos reais como teste interno (esse teste interno usa dado PCERJ e não sai do desktop).

## O que muda no texto do artigo

Nada foi alterado no manuscrito. Para decisão do autor, em `01-artigo/PENDENCIAS.md` (itens D5 a D8) e `docs/DIVERGENCIAS.md` (itens 1 a 3):

- O método executado é Blender, não motor de jogo.
- Limitations ganha duas frases honestas: só nadir, e sombra gravada na textura.
- O achado de escala (ladrilhamento) é resultado próprio e citável, com origem em arquivo.
- A distinção armado e desarmado pede cuidado ético na forma de reportar.

## Citações

| Citação | Identificador | Situação |
|---|---|---|
| Liao, Liu, Xu, Wang, Liu, Yang e Li (2026). "Bridging the Sim2Real Gap in UAV Remote Sensing: A High-Fidelity Synthetic Data Framework for Vehicle Detection". Remote Sensing, 18(2), 361 | DOI 10.3390/rs18020361 | CONFERIDA no Crossref em 2026-09-18 (título, autores, volume, número e artigo batem). Atenção: o objeto detectado é veículo, não pessoa. Os números das ablações (10, 20 e 22,5 pontos) NÃO foram conferidos no texto do artigo por este lado |
| Kim, Park, Yoon, Jung e Jeon (2026). "G-MAD: A Game-Based Data Generation Framework for Multi-View RGB-T Aerial Object Detection". ACM Multimedia 2026 | arXiv 2607.19942 | CONFERIDA no arXiv em 2026-09-18 (título, autores, submissão em 22/07/2026, comentário "ACM Multimedia 2026"). DOI da versão da ACM: não conferido, não informar |
| Berwaldt, Bettker e Pozzer (2020). "Procedural Generation of Favela Layouts on Arbitrary Terrains". SBGames 2020 | DOI 10.1109/SBGames51465.2020.00027 | CONFERIDA no Crossref em 2026-09-18 |
| Kiefer, Ott e Zell (ICPR 2022); SynDrone (ICCVW 2023) | sem identificador neste repositório | NÃO CONFERIDAS. Vêm do levantamento do Mac |
| Ferramentas usadas no desktop: OpenDroneMap 3.6.2, Blender 5.2.1, MPFB 2.0.17, Ultralytics 8.4.148 (YOLO11), Poly Haven (CC0), OpenStreetMap | sem DOI | Citar por URL e versão. Nenhum DOI foi procurado |
