> Nota de 2026-09-18 [DESKTOP]: este pipeline foi tentado no desktop em 2026-09-11 e abandonado na mesma noite, sem nenhuma imagem capturada. O experimento que de fato rodou está em `07-blender/`. O que restou da tentativa (missão, mods, automação por OCR) está em `missao/` e `scripts/windows/`. Ver `docs/DIVERGENCIAS.md`, itens 1 e 14.

# Pipeline: ARMA 3 -> bounding box -> YOLO -> teste em imagem real

Objetivo: reproduzir e fechar o pipeline iniciado em 2022 (Fábio Guimarães e Luciano Figueira, UFRJ) e produzir os números que a Seção 7 do artigo precisa: mAP em dado sintético, mAP zero-shot em dado real e mAP após fine-tuning com pouco dado real.

## 0. Estado herdado de 2022

- Ideia (Fábio, proposta de 19/04/2022): usar o ARMA 3 como gerador de imagens aéreas foto-realistas e o comando `boundingBoxReal` da engine para anotar automaticamente.
- Script original (`scripts/myScriptArmas3-original-2022.sqf`): 3 linhas. Pegava o `boundingBoxReal` de uma unidade e salvava screenshot com o box no nome.
- Dataset de 2022 (Drive, ver `manifest-drive.md`): 28 capturas do editor, 7 com nome de box 3D ou posição 2D, 42 com posição 2D do centro da unidade via `worldToScreen`. Ou seja: chegou até a posição 2D do centro, não à caixa 2D completa.
- O que falta e este pacote resolve: projetar os 8 cantos da caixa 3D para a tela, randomizar cena, câmera e clima, gravar labels em formato legível e treinar.

## 1. Instalação (Windows)

1. ARMA 3 na Steam. Vanilla basta. Apex (Tanoa) ajuda: tem os objetos `Land_Slum_01_F`, `Land_Slum_02_F`, `Land_Slum_03_F` e a cidade de Georgetown, os mais próximos de construção informal que existe no jogo base. Conferir no editor: Assets > Structures > Slum.
2. Python 3.10+; `python -m venv .venv && .venv\Scripts\activate && pip install -r scripts/requirements.txt`.
3. GPU: `nvidia-smi`. PyTorch com CUDA: seguir https://pytorch.org/get-started/locally/ se o pip padrão instalar a versão CPU.

## 2. Preparar a missão no editor Eden

1. Abrir ARMA 3 > Editor > escolher mapa (Tanoa, Altis ou Livonia; ver seção 6 para alternativas mais densas).
2. Colocar um jogador (qualquer unidade, F1 > pode ser um civil) num canto afastado.
3. Colocar marcadores (F6) chamados `ds_centro_1`, `ds_centro_2`, ... nos pontos onde as cenas devem acontecer: ruas estreitas, pátios entre casas, telhados, escadas. Quanto mais variados, melhor.
4. Salvar a missão (nome livre, ex.: `dsFavela`). O ARMA cria `Documents\Arma 3\missions\dsFavela.Tanoa\` (ou em `Arma 3 - Other Profiles\<perfil>\missions\`).
5. Copiar `scripts/capturaDataset.sqf` para essa pasta e criar `init.sqf` com:

```sqf
[] execVM "capturaDataset.sqf";
```

6. Ajustar no topo do `capturaDataset.sqf`: `DS_N_IMAGENS` (comece com 30 para validar; depois 2.000 a 5.000), altitudes, quantidade de unidades.
7. Configurar o jogo: resolução 1920x1080 ou maior (a screenshot sai na resolução de render), Video > Interface size em "Small" ou "Normal", desativar "Blur"/"Bloom" se quiser imagens mais limpas.
8. Play (Play Scenario). Deixar rodando. O hint mostra o progresso.

Saídas:
- PNGs em `Documents\Arma 3\Screenshots\` (ou na pasta do perfil).
- Labels no arquivo `%LOCALAPPDATA%\Arma 3\arma3_<data>.rpt`, linhas:
  - `DSRUN|inicio|N|WxH|safeZone=...|mapa=...`
  - `DSIMG|ds_000001.png|1920|1080|alt|pitch|hora|overcast|fog|n_caixas`
  - `DSLBL|ds_000001.png|classe|x1|y1|x2|y2|typeOf` (frações da tela, origem no canto superior esquerdo)

Classes: 0 = pessoa_armada, 1 = pessoa_desarmada.

## 3. Converter para YOLO e validar

```bat
python scripts\rpt_to_yolo.py --out dataset_arma3
python scripts\preview_boxes.py --data dataset_arma3 --n 10 --out preview
```

Abra `preview\` e confira. Se as caixas estiverem deslocadas de forma sistemática (todas esticadas ou empurradas para um lado), o culpado é a conversão de safeZone: mude `DS_USA_SAFEZONE` para `false` no SQF, gere 30 imagens de novo e reconfira. Só treine quando as caixas fecharem com as pessoas.

Motivos conhecidos de caixa errada:
- Interface size do jogo alterada entre a captura e a conversão (muda safeZone).
- Screenshot em resolução diferente da reportada (`getResolution`); o conversor usa frações, então só importa se o aspecto mudar.
- Unidade parcialmente atrás de parede: `checkVisibility` filtra abaixo de `DS_MIN_VIS`; suba o limiar se aparecerem caixas em pessoas invisíveis.

## 4. Treinar

```bat
python scripts\train_yolo.py --data dataset_arma3\data.yaml --model yolo11n.pt --epochs 50 --imgsz 1280 --name arma3_2cls
python scripts\train_yolo.py --data dataset_arma3\data.yaml --model yolo11n.pt --epochs 50 --imgsz 1280 --single-cls --name arma3_single
```

Sem GPU local: subir `dataset_arma3/` para o Google Drive e treinar no Colab (`pip install ultralytics`, mesmo comando). O modelo `yolo11n` treina 2.000 imagens 1280 em cerca de 1 h numa T4.

## 5. Medir sim-to-real

Benchmark real público mais próximo: VisDrone-DET (imagens de drone em cidades chinesas, classes pedestrian e people). Não existe benchmark público aéreo de "pessoa armada", então a comparação com dado real é em classe única "pessoa".

```bat
python scripts\visdrone_to_yolo.py --src VisDrone2019-DET-val --out visdrone_yolo\val
python scripts\visdrone_to_yolo.py --src VisDrone2019-DET-train --out visdrone_yolo\train --fracao 0.05
```

Crie `visdrone_yolo\data.yaml` (path absoluto, train: train/images, val: val/images, names: {0: pessoa}). Depois:

```bat
:: zero-shot (treinou só no sintético)
python scripts\train_yolo.py --eval-only --weights runs\detect\arma3_single\weights\best.pt --real visdrone_yolo\data.yaml --single-cls --name zero_shot
:: few-shot (fine-tuning com 5% do real)
python scripts\train_yolo.py --weights runs\detect\arma3_single\weights\best.pt --data visdrone_yolo\data.yaml --single-cls --epochs 20 --name finetune_5pct --real visdrone_yolo\data.yaml
:: baseline: só real 5%, sem sintético
python scripts\train_yolo.py --data visdrone_yolo\data.yaml --model yolo11n.pt --single-cls --epochs 20 --name real_only_5pct --real visdrone_yolo\data.yaml
```

Tabela que vai para o artigo:

| Treino | mAP50 real | mAP50-95 real |
|---|---|---|
| sintético (zero-shot) | | |
| real 5% | | |
| sintético + real 5% (fine-tuning) | | |

Se a terceira linha superar a segunda, o sintético ajuda, que é a tese de Barisic 2022 e Horváth 2023 citada no artigo. Os resultados ficam em `resultados/*.json` e em `runs/detect/`.

Se os ortomosaicos do Jacarezinho (PCERJ) forem usados como teste, é só internamente: recortar tiles, anotar à mão umas 50 pessoas com LabelImg ou CVAT, e rodar o `--eval-only`. Não incluir esses tiles em nenhum pacote.

## 6. Como estender para as classes do artigo (morfologia vertical)

O artigo (Seção 7) quer classificar altura de edificação, adições em laje e transição de material, não pessoas. Mesmo pipeline, muda o que se spawna e se anota:

1. No Eden, montar composições de casas empilhadas com os objetos `Land_Slum_*`, `Land_Shed_*`, `Land_House_Small_*`, contêineres e muros, em encosta (Tanoa tem morros perto de Georgetown). Salvar como composições e replicá-las.
2. No SQF, em vez de `createUnit`, usar `createSimpleObject` / `createVehicle` para as estruturas em posições e rotações randomizadas, e empilhar (setPosATL com z = altura da de baixo).
3. Anotar com o mesmo `DS_fnc_bbox2D`, mas classe = número de pavimentos (1, 2, 3+) ou presença de laje ocupada. A altura pode ser lida de `boundingBoxReal` (z2 - z1).
4. Para teste real com dado consentido e público, usar os datasets citados no artigo: Kigali (Gevaert et al. 2016) e Slovo Park (Sithole e Mhangara 2025), ou o Open Cities AI Challenge (edificações em cidades africanas, licença aberta).

Limite honesto: nenhum mapa do ARMA 3 reproduz a morfologia de favela. O que o jogo dá é variação fotométrica e geométrica barata com anotação exata. Para geometria fiel, o passo seguinte é Unreal/Unity ou Blender com geração procedural, o que o artigo já chama de "procedurally generated 3D scenes".

## 7. Referências rápidas de scripting

- boundingBoxReal: https://community.bistudio.com/wiki/boundingBoxReal
- worldToScreen: https://community.bistudio.com/wiki/worldToScreen
- modelToWorldVisual: https://community.bistudio.com/wiki/modelToWorldVisual
- screenshot: https://community.bistudio.com/wiki/screenshot
- checkVisibility: https://community.bistudio.com/wiki/checkVisibility
- safeZone: https://community.bistudio.com/wiki/SafeZone
- camCreate / camSetPos / camSetTarget: https://community.bistudio.com/wiki/camCreate
- Eden Editor: https://community.bistudio.com/wiki/Eden_Editor
- Ultralytics YOLO: https://docs.ultralytics.com/
- VisDrone: https://docs.ultralytics.com/datasets/detect/visdrone/
