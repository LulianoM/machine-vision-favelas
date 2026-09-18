> Nota de 2026-09-18 [DESKTOP]: este README veio de `C:\arma3-favela\blender\README-BLENDER.md` sem alteração. Os caminhos `C:\arma3-favela\...` são os do desktop, onde os dados continuam morando (ver `06-resultados/ONDE-ESTAO-OS-DADOS.md`). Os scripts estão em `scripts/`. Resultados em `06-resultados/RESULTADOS.md`.

# Pipeline Blender: favela real (OSM + fotos PCERJ) -> drone a 100 m -> bounding box -> YOLO

Atualizado em 2026-09-12. Substitui o pipeline ARMA 3 (`capturaDataset.sqf`). Saida no mesmo formato YOLO, entao `train_yolo.py`, `preview_boxes.py` e `visdrone_to_yolo.py` do pacote original continuam valendo.

## Tres geradores, do mais simples ao mais realista

| Script | Base geometrica | Materiais | Pessoas | Uso |
|---|---|---|---|---|
| `gen_favela.py` (v2) | favela procedural (quarteiroes, becos) | procedurais | low-poly | prototipo, muito rapido |
| `gen_jacarezinho.py` (v3) | footprints reais do OSM (Jacarezinho ou Rocinha) + terreno SRTM + densificacao procedural nos vazios | PBR Poly Haven (tijolo, concreto, reboco, zinco, fibrocimento, telha, asfalto, terra) + HDRI | MPFB (MakeHuman) riggadas e posadas, roupa procedural | dataset principal |
| (proximo) malha ODM | fotogrametria das 567 fotos reais de 2022 (ortomosaico + DSM + malha texturizada) | textura fotografica real | MPFB | teste sim-to-real com geometria e textura reais |

## Dados reais disponiveis (uso interno, PCERJ, nao redistribuir)

- `C:\arma3-favela\assets\ortomosaico\{sudoeste,nordeste}\`: 217 + 350 fotos DJI (Zenmuse Z30, 1920x1080, nadir, 150 m de altura relativa, passo de 21,6 m entre fotos, com GPS). Voadas em 01 e 02/08/2022. Cobrem 528 x 554 m (Sudoeste) e 822 x 814 m (Nordeste). Os zips do Drive contem so as fotos brutas; as pastas "output" estavam vazias, ou seja, o processamento de 2022 se perdeu e foi refeito aqui com o OpenDroneMap.
- `C:\arma3-favela\odm\`: projetos ODM (`sudoeste`, `nordeste`). Saidas em `<setor>\odm_orthophoto\odm_orthophoto.tif`, `<setor>\odm_dem\dsm.tif`, `<setor>\odm_texturing\odm_textured_model_geo.obj`.
- `C:\arma3-favela\assets\osm\`: footprints e vias do OSM (2.756 edificacoes no Jacarezinho, 2.720 na Rocinha) e grades SRTM 30 m.

## O que foi instalado

| Item | Onde |
|---|---|
| Blender 5.2.1 LTS (Steam) | `C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe` |
| Addon MCP for Blender v1.6 | `%APPDATA%\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py` (habilitado) |
| Servidor blender-mcp | `C:\arma3-favela\mcp-venv\Scripts\blender-mcp.exe`, registrado com `claude mcp add blender -s user` |
| MPFB 2.0.17 (MakeHuman para Blender, extensao oficial) | `%APPDATA%\Blender Foundation\Blender\5.2\extensions\user_default\mpfb` |
| Poly Haven CC0: 72 texturas PBR 1k, 15 HDRI 2k, 29 modelos glTF | `C:\arma3-favela\assets\polyhaven\` (indice em `index.json`, baixador `fetch_ph.py`) |
| Human Base Meshes v1.1.0 (Blender Studio, CC0) | `C:\arma3-favela\assets\human-base-meshes-bundle-v1.1.0\` |
| OpenDroneMap 3.6.2 nativo Windows | `C:\ODM\run.bat` |
| venv de treino (torch 2.14 cu126, ultralytics 8.4, gdown) | `C:\arma3-favela\venv` |

Para usar o MCP: abrir o Blender, painel lateral (N) > aba "BlenderMCP" > "Connect to MCP server" (porta 9876), ou abrir ja conectado:

```bat
"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe" cena_exemplo.blend --python-expr "import bpy; bpy.app.timers.register(lambda: (bpy.ops.blendermcp.start_server(), None)[1], first_interval=3.0)"
```

## Mapa navegavel (build_map.py)

Monta um `.blend` unico com o Jacarezinho reconstruido, pronto para voar dentro dele:

```bat
cd C:\arma3-favela\blender
"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe" -b --python build_map.py -- ^
  --sectors sudoeste nordeste --out C:\arma3-favela\odm\jacarezinho.blend --preview --video 240 --pessoas 120
```

O que ele monta:

- **MAPA_FOTOGRAMETRIA**: a malha texturizada de cada setor, posicionada pelo georreferenciamento UTM real, entao Sudoeste e Nordeste encaixam no mesmo mundo sem ajuste manual.
- **TERRENO_ORTOMOSAICO**: malha 2.5D do DSM com o ortomosaico aplicado, 25 cm por baixo da malha principal, tapando buracos e bordas.
- **LUZ_E_CAMERAS**: sol calculado para a data e hora reais do voo (02/08/2022, 11h55, elevacao 49,4 graus, azimute 1,6 graus, ou seja, quase a pino e ao norte), mais as cameras.
- **PESSOAS**: pessoas MPFB vestidas, colocadas por ray cast so onde a superficie e quase horizontal (rua, patio, laje).

Cameras prontas: `CAM_TOPO_MAPA` (setor inteiro), `CAM_NADIR_150m_Z30` (igual a camera real da PCERJ), `CAM_OBLIQUA_100m`, `CAM_BAIXA_45m` e `CAM_VOO` (voo animado de 240 quadros por uma rota fechada a 70 m, com alvo adiantado para olhar para a frente e para baixo).

**Como navegar**: abra o `.blend`, passe o mouse sobre a viewport e use Shift + acento grave para entrar no modo voo (W, A, S, D para mover, mouse para olhar, roda para acelerar). O clipping ja vai ate 5 km e o sombreamento ja abre em Material. Para ver pela camera, numpad 0.

**Sobre a iluminacao**: a textura da fotogrametria ja tem o sol e as sombras do voo gravados no pixel. Por isso a cena usa luz quase toda ambiente (ceu neutro levemente quente) e um sol fraco, so para dar relevo e sombrear o que for acrescentado. Se aumentar o sol, a favela escurece duas vezes e fica azulada.

**Limite honesto do dado**: todas as 567 fotos foram tiradas em nadir a 150 m. Nao existe nenhuma foto obliqua, entao as paredes verticais nao tem textura propria: elas sao esticadas a partir dos pixels do telhado e da rua. Por isso o mapa se sustenta bem de cima ate uns 45 m e derrete quando a camera desce ao nivel da rua. Para ter fachada seria preciso um voo novo com camera obliqua.

## Gerar o dataset (v3)

```bat
cd C:\arma3-favela\blender
"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe" -b --python gen_jacarezinho.py -- --area jacarezinho --out dataset_v3 --n 120 --res 3840 2160 --samples 48 --seed 2026 --pitch 55 90 --rebuild-every 6
C:\arma3-favela\venv\Scripts\python.exe post_process.py --data dataset_v3
```

Parametros principais (`--help` lista todos):

- `--area jacarezinho|rocinha`: qual malha real do OSM usar. Cada rebuild sorteia um centro de cena dentro da area e constroi um raio de `--radius` 170 m.
- `--alt 100 --alt-jitter 8 --pitch 55 90 --lens 20 30`: camera drone (focal em mm num sensor de 36 mm).
- `--camera z30`: reproduz a camera real das fotos da PCERJ (1920x1080, nadir, 150 m, 28,8 mm eq.). Util para medir sim-to-real contra as fotos reais.
- `--people 4 9 --prob-armado 0.5`: pessoas por cena e fracao com fuzil.
- `--min-vis 0.35`: fracao minima do corpo com linha de visao livre (ray cast) para anotar.
- `--pool 6`: humanos MPFB distintos por favela; cada pessoa da cena e uma copia com roupa e pose proprias.
- `--rebuild-every 6`: nova cena (centro, materiais, props) a cada N imagens.

Saida: `images/{train,val}/jc_000001.jpg` (apos `post_process.py`: ruido de sensor, desfoque, aberracao cromatica, vinheta, neblina, JPEG), `labels/{train,val}/*.txt` (YOLO, 0 = pessoa_armada, 1 = pessoa_desarmada), `data.yaml`, `manifest.jsonl` (camera, luz, HDRI, contagens, visibilidade por caixa, tempo de render).

Custo: cena constroi em 1 s; render 4K Cycles/OptiX na RTX 2060 em 26 a 29 s; 1080p em 9 s. O carregamento inicial (props glTF + 6 humanos MPFB) leva 30 s por processo.

## O que a cena v3 contem

- Edificacoes do OSM extrudadas: 1 a 5 pavimentos (pesos 20/37/27/12/4%, ou `building:levels` quando existe), 40% de chance por andar de "adicao em laje" (andar menor, deslocado, laje exposta), galpoes industriais com telha metalica.
- Densificacao: onde o OSM nao tem nada, lotes de 5 a 8,5 m alinhados ao vizinho real mais proximo, encostados uns nos outros, fora das vias.
- Fachadas: janelas com moldura e vidro escuro, portas no terreo, ar-condicionado. Coberturas: laje (45%: cru, caiada ou cinza), com parapeito (45%), colunas de espera (35%), varal com roupas (25%), lona (10%); telha metalica/fibrocimento (40%) com tijolos segurando; telha ceramica (15%). Caixa d'agua azul, preta ou branca (45%), antena parabolica (30%), tralha na laje com props reais (40%).
- Vias do OSM com asfalto ou concreto PBR por tipo; postes de concreto com cruzeta a cada 22 a 28 m; fiacao com catenaria entre postes e "gatos" para as lajes vizinhas; carros estacionados (geometria propria com 6 cores, e carro coberto do Poly Haven).
- Arvores (island_tree_01/02, tree_small_02, jacaranda), mato, lixo, pneus, tambores, caixotes, botijoes, sacos de lixo espalhados.
- Terreno SRTM com chao de terra, asfalto e mato misturados por ruido.
- Luz: 65% ceu fisico (multiple scattering) + sol nitido, 35% HDRI real (Poly Haven) + sol fraco. Exposicao entre -0.8 e -0.2.
- Pessoas: MPFB aleatorias (idade, sexo, biotipo), rig padrao, pose parada ou andando com variacao, roupa procedural por altura (sapato, calca ou bermuda, camisa ou regata, pele), escala 0,92 a 1,08. Armadas carregam fuzil (corpo, cano, carregador, coronha) a frente do peito.
- Anotacao: caixa 2D dos vertices deformados do corpo + arma projetados na camera; oclusao por ray cast de 14 pontos.

## Validar antes de treinar

```bat
C:\arma3-favela\venv\Scripts\python.exe ..\projeto_contexto\PROJETO-MACHINE-VISION-FAVELAS\03-arma3\scripts\preview_boxes.py --data dataset_v3 --split val --n 12 --out dataset_v3\preview
```

## Fotogrametria das fotos reais (ODM)

```bat
C:\ODM\run.bat --project-path C:\arma3-favela\odm sudoeste --dsm --orthophoto-resolution 5 --mesh-size 300000 --feature-quality high --pc-quality medium --max-concurrency 10
```

Depois: importar `odm_textured_model_geo.obj` no Blender (`bpy.ops.wm.obj_import`), colocar as pessoas MPFB sobre a malha (ray cast para baixo para achar o chao ou a laje) e renderizar com a mesma camera. Isso da imagens com textura fotografica real do Jacarezinho e pessoas sinteticas anotadas.

## Treino do detector

O `train_yolo.py` do pacote original **trava no Windows**: ele executa o treino no nivel do modulo, e o
DataLoader com `workers > 0` usa multiprocessing por spawn, reimporta o arquivo e dispara o treino de
novo dentro de cada worker. Use `train_yolo_win.py`, que e o mesmo script com `if __name__ == "__main__"`.

```bat
C:\arma3-favela\venv\Scripts\python.exe train_yolo_win.py --data dataset_v3_tiles/data.yaml ^
  --model yolo11s.pt --epochs 60 --imgsz 1280 --batch 4 --name blender_v3_tiles
```

### Ladrilhamento: por que ele e obrigatorio aqui

Uma pessoa a 100 m ocupa de 11 a 41 px numa imagem 4K. Treinando com `imgsz=1536`, a imagem inteira
encolhe 2,5 vezes e a pessoa vira de 4 a 16 px. O menor stride do YOLO e 8, entao um alvo de 4 px
praticamente nao chega a rede. O `tile_dataset.py` recorta o 4K em ladrilhos, preservando o tamanho
original do alvo:

```bat
C:\arma3-favela\venv\Scripts\python.exe tile_dataset.py --data dataset_v3 --out dataset_v3_tiles --tile 1280 --overlap 0.2
```

Medido no conjunto de validacao sintetico (120 imagens, 671 caixas, yolo11n/yolo11s):

| Treino | mAP50 |
|---|---|
| imagem 4K reduzida para 1536 | 0,116 |
| ladrilhos de 1280 em escala nativa | 0,151 na epoca 4 de 60 |

### Ver o que o detector faz

```bat
C:\arma3-favela\venv\Scripts\python.exe preview_deteccao.py ^
  --pesos runs\detect\blender_v3_tiles\weights\best.pt --data dataset_v3_tiles --out exemplo_treino.png --n 6 --conf 0.15
```

Monta uma folha com verde na anotacao gerada pelo Blender e vermelho ou azul na previsao, com a
confianca. Serve para enxergar o que a metrica esconde: hoje a rede acerta a posicao da pessoa, mas
confunde armada com desarmada (a 100 m um fuzil tem 3 ou 4 px) e produz muito alarme falso.

## Resultados

Ver `RESULTADOS-BLENDER.md`.

## Proximos passos

1. Terminar ODM do Nordeste (350 fotos) e montar o gerador sobre a malha ODM.
2. Anotar a mao umas 50 pessoas nas fotos reais (CVAT ou LabelImg) para ter teste real interno; VisDrone continua como teste publico.
3. Segundo experimento do artigo (morfologia vertical): o gerador ja guarda `floors`, footprint e `ztop` por edificacao; basta trocar a anotacao de pessoa por edificacao.
4. Sketchfab: modelos de favela e pessoas escaneadas CC-BY existem, mas o download exige conta. Se quiser, crie uma conta e cole o token no painel do addon MCP (aba Sketchfab) ou em `C:\arma3-favela\assets\sketchfab_token.txt`.
