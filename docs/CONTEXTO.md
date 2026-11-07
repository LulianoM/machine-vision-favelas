# Contexto acumulado do projeto

Conhecimento que estava só na memória do Claude do Mac e que o desktop também precisa. Atualizar aqui quando surgir algo que valha para as duas máquinas.

## Linha do tempo

| Quando | O que |
|---|---|
| mar a ago/2022 | Projeto de pesquisa e extensão BCMT-UFRJ com prof. Claudio Miceli (NCE-UFRJ) e Fábio H. P. Guimarães (perito PCERJ): detecção de pessoas armadas em imagens RGB-T de drone, CNN treinada com dados sintéticos do ARMA 3. Ver `02-projeto-ufrj-2022/`. |
| 2026-09-09 | Levantamento de 15 artigos sobre CV, drones e segurança pública. Ver `04-bibliografia/`. Orientador escreve a v1 do artigo (3.205 palavras). |
| 2026-09-10 | v2 do orientador: 6.304 palavras pela contagem do script de divisão (5.644 sem a lista de referências). É a versão vigente. |
| 2026-09-11 | Pacote `.rar` levado ao desktop com briefing, scripts do pipeline e prompt inicial (cópias em `docs/`). |
| 2026-09-11, noite [DESKTOP] | Tentativa com ARMA 3: mods instalados, missão `dsFavela.Tanoa` criada (21h38), automação por OCR. Nenhuma imagem capturada. Abandonado na mesma noite. Às 22h40 o Blender e o blender-mcp já estavam instalados; às 23h02 existia o primeiro gerador procedural (`gen_favela.py`). |
| 2026-09-12, madrugada [DESKTOP] | Gerador sobre OSM (`gen_jacarezinho.py`), `dataset_v3` (120 imagens 4K), treino `blender_v3` (mAP50 0,116), descoberta do ladrilhamento, `blender_v3_tiles2` (mAP50 0,561, fim às 04h44). Em paralelo, OpenDroneMap nas 567 fotos da PCERJ (Sudoeste e Nordeste), mapa navegável `jacarezinho.blend` (05h01), `dataset_odm` e treino `blender_odm_tiles` (mAP50 0,646, fim às 07h02). |
| 2026-09-12, manhã [DESKTOP] | Prova de conceito da quadra com paredes verticais a partir do DSM (`build_quadra.py`, 09h59) e "cidade de sólidos" (`segmenta_predios.py`, `build_cidade.py`, 11h09). |
| 2026-09-12, 12h45 [MAC] | Levantamento técnico sobre como recriar a favela em 3D, e e-mail de resumo. Ver `05-levantamento-3d/`. O desktop não recebeu nem usou esse material. |
| 2026-09-12 11h30 a 2026-09-13 05h24 [DESKTOP] | Batelada a 150 m: 560 imagens de treino, 60 de teste de ângulo e luz, 40 de multidão, ladrilhamento, treino `cid150_s` (8 h 54 min, mAP50 0,676) e avaliação em imagem inteira (F1 0,849 e 0,787). Última atividade do desktop antes da reconciliação. |
| 2026-09-17 | O orientador não enviou versão nova: o arquivo baixado nesse dia é idêntico byte a byte à v2 de 10/09. Pasta reorganizada no Mac, artigo dividido por seção, estrutura de repositório único preparada. |
| 2026-09-17 e 18 [DESKTOP] | Reconciliação: clone em `C:\projetos\machine-vision-favelas`, inventário, `docs/DIVERGENCIAS.md`, código em `03-blender/`, resultados em `06-resultados/`. |

## O experimento e o que ele prova

O pipeline valida o método da seção de resultados do artigo: cena sintética, anotação automática de bounding box, domain randomization, treino de detector, teste em imagem aérea real (VisDrone). Corrigido em 2026-09-18 [DESKTOP]: o pipeline executado é o de `03-blender/` (Blender headless), não o de `02-projeto-ufrj-2022/arma3-2022/`, que foi tentado e abandonado sem gerar imagem (ver `docs/DIVERGENCIAS.md`, item 1). Números que vão para o artigo: mAP zero-shot, mAP com 5 a 10% de dado real, e sintético mais real. Nenhum dos três existe ainda. As classes atuais são duas, `pessoa_armada` e `pessoa_desarmada`, vistas de drone a 100 e a 150 m (a frase anterior dizia só "pessoas vistas de cima"). Classes do artigo (altura de edificação, adição em laje, transição de material) exigem um segundo experimento com cenas de edificações empilhadas; o pipeline é o mesmo.

## Achados do levantamento 3D que decidem o desenho

- O que decide o sim-to-real é a ORIGEM DA GEOMETRIA, não textura nem engine. Liao et al. 2026 (Remote Sensing 18(2):361, DOI 10.3390/rs18020361, dataset UAV-SynthScene, Colosseum + UE 5.1 + UltraDynamicSky, 4.659 imagens, uma RTX 4090) é o template do método. Duas ablações, com veículo como objeto (não pessoa): tirar a variação de sol, clima e ângulo custa 30,4 pontos de mAP50 no YOLOv11 e 17,5 na média dos detectores testados; trocar a base fotogramétrica por assets genéricos custa 27,0 no YOLOv11 e cerca de 22 a 23 na média (a Tabela 5 dá 23,3 e o texto do próprio artigo dá 22,5, inconsistência registrada em `04-bibliografia/liao-2026-numeros-conferidos.md`).
- Consequência: comprar kit de favela é o braço perdedor. Assets servem para props sobre base real, nunca como base.
- O Instituto Pereira Passos serve publicamente uma ortofoto verdadeira do Rio de 2024, pixel de 15 cm, de um voo que incluiu LiDAR: `pgeo3.rio.rj.gov.br/arcgis/rest/services/Imagens/Mosaico_2024/ImageServer`, EPSG:31983, cobre o Jacarezinho. É dado municipal aberto, não sensível. A nuvem LiDAR não está publicada: pedir em cartografia.ipp@prefeitura.rio (disponibilidade, custo e termos não verificados).
- Google Photorealistic 3D Tiles é proibido contratualmente para detecção de objetos. Não usar como fonte de geometria nem como cena de captura.
- Prior art obrigatório: G-MAD (Kim et al., ACM MM 2026, arXiv 2607.19942), que usa ARMA 3 para dados aéreos RGB-T com bbox automático do engine. Também Berwaldt, Bettker e Pozzer, "Procedural Generation of Favela Layouts on Arbitrary Terrains", SBGames 2020, DOI 10.1109/SBGames51465.2020.00027.
- Expectativa calibrada: sintético puro em cena urbana densa pode colapsar (Kiefer, Ott e Zell, ICPR 2022: três detectores treinados só com sintético marcaram 1,2, 2,4 e 10,2 de mAP50 no VisDrone, contra 24,6, 48,6 e 43,9 das mesmas arquiteturas treinadas no treino real inteiro, média de 10 classes; a comparação com o nosso detector usa a linha do YOLO, 10,2 contra 43,9). Altitude é eixo de domain shift severo (SynDrone, ICCVW 2023). Com pré-treino sintético bom, 5 a 20% do dado real recupera 85 a 95% do desempenho. Não prometer substituição total.
- Convenção de anotação: definir e documentar modal (só a parte visível) versus amodal (objeto inteiro, como no VisDrone) antes de gerar o primeiro lote. [DESKTOP, 2026-09-18: já está fixada de fato como amodal recortada no quadro, com visibilidade mínima de 0,35. Ver `06-resultados/RESULTADOS.md`.]
- Problema técnico a planejar se a fotogrametria de 2022 for usada: remover a iluminação assada da textura (delighting). [DESKTOP, 2026-09-18: a fotogrametria de 2022 foi usada e o delighting não foi feito, foi contornado. Ver `docs/DIVERGENCIAS.md`, item 5.]

## Vindo do desktop

Acrescentado em 2026-09-18 [DESKTOP]. É o que estava só na memória local do Claude do desktop e nas notas de `C:\arma3-favela\`. Detalhe e números em `06-resultados/RESULTADOS.md`; máquina e armadilhas em `docs/AMBIENTE-DESKTOP.md`; conflitos com o que este arquivo dizia em `docs/DIVERGENCIAS.md`.

- O ARMA 3 saiu do pipeline em 11 e 12/09. Motivo: o jogo não expõe controles, a automação dependia de OCR e de clique em primeiro plano. O Blender roda 100% headless, com semente determinística, e a anotação sai exata por projeção de vértices mais ray cast de oclusão. O README de 2022 já dizia que nenhum mapa do ARMA 3 reproduz favela e apontava Blender procedural como passo seguinte. Base que tinha sido escolhida no ARMA: Tanoa, objetos `Land_Slum_01/02/03_F`.
- Pedidos explícitos do autor nas sessões do desktop: realismo máximo, fidelidade ao ortomosaico real, mapa navegável em 3D, altura média de 150 m "para seguir o modelo que temos", distinguir armados de desarmados com meta de 75% de acurácia, e NÃO usar fachadas do Google Maps 3D Tiles.
- As pastas "output" do Drive de 2022 estavam vazias: o processamento fotogramétrico da época se perdeu e foi refeito do zero no OpenDroneMap 3.6.2. Sudoeste: 217 fotos, 7,4 cm/px. Nordeste: 350 fotos, 6,4 cm/px. Os dois setores encaixam sozinhos pelo georreferenciamento UTM.
- Câmera real do voo de 2022: Zenmuse Z30, 1920x1080, nadir, 150 m de altura relativa, passo de 21,6 m, voos em 01 e 02/08/2022. O gerador tem o modo `--camera z30` que a reproduz.
- Limite do dado: só nadir. Sem foto oblíqua não há textura de fachada. O mapa se sustenta de cima até cerca de 45 m e derrete ao nível da rua. Fachada exigiria voo novo com câmera oblíqua.
- Achado metodológico mais forte até aqui: a escala de treino pesa mais que o volume de dados. Pessoa a 100 m ocupa 11 a 41 px em 4K; reduzir a imagem para 1536 px a leva para 4 a 16 px, abaixo do menor stride do YOLO (8). Ladrilhar em 1280 px em escala nativa levou o mAP50 de 0,116 para 0,561 nas mesmas 120 imagens.
- A distinção armado e desarmado funciona no sintético, mas a arma é sempre o mesmo modelo, na mesma posição e com o mesmo contraste. Não há prova de que sobreviva ao dado real.
- Os três braços de cena que existem: procedural sobre footprints do OSM (`gen_jacarezinho.py`, sem dado sensível), malha fotogramétrica real (`gen_odm.py`, dado PCERJ), e "cidade de sólidos" segmentada do DSM com paredes verticais e PBR (`gen_cidade.py`, geometria PCERJ). O gerador já guarda `floors`, footprint e `ztop` por edificação, então o segundo experimento do artigo (morfologia vertical) é trocar a anotação de pessoa por edificação.
- Sim-to-real não foi medido. O VisDrone não está no disco do desktop.
- Segundo cérebro do autor: cofre do Obsidian em `C:\Users\marti\Documents\SecondBrain - Glados` (cópia da nota do projeto em `docs/2026-09-12_nota-obsidian-desktop.md`).

## Restrições de máquina

- O MacBook Air M1 de 8 GB está abaixo do mínimo para Unreal Engine 5 e não roda ARMA 3. Todo render e treino acontece no desktop.
- BlenderProc não usa GPU no macOS. Unity Perception foi descontinuado.

## Pessoas

| Pessoa | Papel |
|---|---|
| Luciano Martins Figueira (Felipe) | Autor, mestrando MEX FGV EBAPE 2026.2, engenheiro de software |
| Prof. Hélio Arthur Reis Irigaray | Orientador, autor dos rascunhos v1 e v2 |
| Prof. Claudio Miceli de Farias | Orientador do projeto de 2022 (NCE-UFRJ) |
| Fábio H. P. Guimarães | Perito PCERJ, autor da proposta de 2022 e da ideia de usar ARMA 3 |

## Onde estão os binários que não entram no git

- Pacote completo de 11/09 com os 18 PDFs: no Mac em `~/Documents/Mestrado/Projetos/PROJETO-MACHINE-VISION-FAVELAS-2026-09-11.rar`; no desktop, na pasta descompactada original.
- Dataset de 2022, ortomosaicos e decks: Google Drive, pasta "PROJETO DRONE". IDs em `02-projeto-ufrj-2022/arma3-2022/manifest-drive.md`.
- Tudo que o desktop produziu (datasets, pesos, ODM, cenas `.blend`): `C:\arma3-favela\`, inventariado em `06-resultados/ONDE-ESTAO-OS-DADOS.md`. O pacote de 11/09 está descompactado em `C:\arma3-favela\projeto_contexto\`.
