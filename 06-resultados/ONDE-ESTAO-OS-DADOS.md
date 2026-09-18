# Onde estão os dados (desktop)

Levantado em 2026-09-17 e 18 [DESKTOP]. Nada desta lista está no git. Tudo mora em `C:\arma3-favela\` (44 GB), que fica intacta como arquivo morto. A coluna PCERJ marca o que deriva das fotos operacionais da PCERJ e por isso não sai do desktop por nenhum canal.

## Pesos

SHA256 calculado com `Get-FileHash -Algorithm SHA256`. Caminho base: `C:\arma3-favela\blender\`.

| Arquivo | MB | Data | PCERJ | SHA256 |
|---|---|---|---|---|
| `runs\detect\blender_v3\weights\best.pt` | 5,3 | 2026-09-12 02:04 | não | 42434FA00C61F0CDA7790C100296EAD5457A6D511CB040E8D5E9F348C8AD2F67 |
| `runs\detect\blender_v3\weights\last.pt` | 5,3 | 2026-09-12 02:04 | não | 0D12423532DD4822ECF5D820BD4037EA816F6E30A8522397D2C9678F523C08FB |
| `runs\detect\blender_v3_tiles\weights\best.pt` | 72,6 | 2026-09-12 03:05 | não | 502D3F7F4397F99A52A0971A34E7A5DD598E3D40D9007B9A1ADA9701B350AAE2 |
| `runs\detect\blender_v3_tiles\weights\last.pt` | 72,6 | 2026-09-12 03:24 | não | ECEB81A5968BBD7323D7E5BBFEC5B0E5709E2209BC552E7739312BE38682B793 |
| `runs\detect\blender_v3_tiles2\weights\best.pt` | 18,4 | 2026-09-12 04:44 | não | F8D00AFBE3DCF4E0C280247410D652496782C8EBC80622C8B4A7716F93EE8579 |
| `runs\detect\blender_v3_tiles2\weights\last.pt` | 18,4 | 2026-09-12 04:44 | não | 2D0EB454983712243E401DEF4CA85DC4C1CF45B3CE3781CF1C8013A9275F6F4E |
| `runs\detect\blender_odm_tiles\weights\best.pt` | 18,4 | 2026-09-12 07:02 | treinado em dado PCERJ | 6DDF75294A40D48E85393E76DBB1ACA94D3210F44C2758B8D3C9AAF984CA887F |
| `runs\detect\blender_odm_tiles\weights\last.pt` | 18,4 | 2026-09-12 07:02 | treinado em dado PCERJ | 51F27FF64A1EEFA14AA63B91E0BED48AD6C2C3DEF177386F9D9B00006E641B82 |
| `runs\detect\cid150_s\weights\best.pt` | 18,4 | 2026-09-13 05:23 | treinado em dado PCERJ | CEA30547EEB62589D1537F4E1B83C3FAA0A573AA9F965344E99DA88BDE9CDFD2 |
| `runs\detect\cid150_s\weights\last.pt` | 18,4 | 2026-09-13 05:23 | treinado em dado PCERJ | 33135A28E0EAC5EDD476404B3BF220CAC2FB5BE31FC86A7B859335747F203D94 |
| `yolo11n.pt` (COCO, Ultralytics) | 5,4 | 2026-09-12 01:31 | não | 0EBBC80D4A7680D14987A577CD21342B65ECFD94632BD9A8DA63AE6417644EE1 |
| `yolo11s.pt` (COCO, Ultralytics) | 18,4 | 2026-09-12 02:07 | não | 85A76FE86DD8AFE384648546B56A7A78580C7CB7B404FC595F97969322D502D5 |
| `weights\yolo26n.pt` (baixado, não usado em nenhum run) | 5,3 | 2026-09-12 01:31 | não | 9B09CC8BF347F0FC8A5F7657480587F25DB09B34BF33B0652110FB03A8AD4FEF |

Os `best.pt` do `blender_v3_tiles` têm 72,6 MB, o quádruplo dos outros yolo11s. Explicação provável (não verificada abrindo o arquivo): o treino foi interrompido antes de o Ultralytics remover o estado do otimizador, o que ele só faz ao fim do treino.

## Datasets

Caminho base: `C:\arma3-favela\blender\`. Estrutura YOLO (`images/{train,val}`, `labels/{train,val}`, `data.yaml`, `manifest.jsonl`). Os `data.yaml` têm o caminho absoluto antigo no campo `path`.

| Pasta | MB | Imagens train / val | Rótulos .txt | Caixas | Data | PCERJ |
|---|---|---|---|---|---|---|
| `dataset_v3` | 224 | 103 / 17 | 120 | 671 | 2026-09-11 e 12 | não |
| `dataset_v3_tiles` | 251 | 520 / 80 | 600 | 1.173 | 2026-09-12 | não |
| `dataset_odm` | 172 | 105 / 15 | 120 | 857 | 2026-09-12 | sim |
| `dataset_odm_tiles` | 217 | 595 / 87 | 682 | 1.551 | 2026-09-12 | sim |
| `dataset_cid150` (inclui `images_png` sem pós-processamento) | 7.621 | 473 / 87 | 560 | 5.745 | 2026-09-12 | sim |
| `dataset_cid150_tiles` | 1.169 | 2.377 / 437 | 2.814 | 10.239 | 2026-09-12 | sim |
| `teste_angulos` | 828 | 0 / 60 | 60 | 596 | 2026-09-12 | sim |
| `teste_denso` | 543 | 0 / 40 | 40 | 1.749 | 2026-09-12 | sim |

Pastas de ensaio (renders avulsos de calibração, sem valor de dataset): `amostra-4k`, `test_cid`, `test_now`, `test_odm`, `test_odm2`, `test_paint`, `test_pm`, `test_v3`, `test_v3b`, `test_v3c`, `test_z30`. Somam cerca de 2,4 GB.

## Runs completos

`C:\arma3-favela\blender\runs\detect\` (308 MB): `blender_v3`, `blender_v3_tiles`, `blender_v3_tiles2`, `blender_odm_tiles`, `cid150_s`, cada um com a pasta irmã `<run>_val`. O que é leve e não sensível está copiado em `06-resultados/<run>/`. Ficaram só no desktop: pesos, e os mosaicos `train_batch*.jpg` e `val_batch*.jpg` dos runs `blender_odm_tiles` e `cid150_s` (mostram textura PCERJ).

Avaliações: `C:\arma3-favela\blender\aval_angulos\` e `aval_denso\` (`resultado.json` copiado, `previas.jpg` não).

Logs: 35 arquivos `.log` em `C:\arma3-favela\blender\` e 5 em `C:\arma3-favela\odm\`. Não copiados: têm caminhos locais e, em `build_map_final.log`, latitude e longitude do centro do voo.

## Fotogrametria e cenas 3D (tudo PCERJ, nada sai do desktop)

| Item | Caminho | Tamanho |
|---|---|---|
| Fotos brutas do drone, 217 + 350 (ago/2022, Zenmuse Z30) | `C:\arma3-favela\assets\ortomosaico\{sudoeste,nordeste}\` | 752 MB |
| Zip original baixado do Drive | `C:\Users\marti\Downloads\Ortomosaico-20260912T023827Z-1-001.zip` | 375 MB |
| Projeto ODM Sudoeste (ortomosaico, DSM, nuvem, malha) | `C:\arma3-favela\odm\sudoeste\` | 9,3 GB |
| Projeto ODM Nordeste | `C:\arma3-favela\odm\nordeste\` | 13,8 GB |
| Mapa navegável dos dois setores | `C:\arma3-favela\odm\jacarezinho.blend` (mais `.blend1`) | 314 MB |
| Quadra com paredes verticais e cidade de sólidos | `C:\arma3-favela\odm\quadra.blend` (mais `.blend1`), `odm\quadra\`, `odm\cidade\` | 386 MB |
| Vídeo do voo | `C:\arma3-favela\odm\voo_jacarezinho.mp4` | 8,6 MB |
| Figuras de comparação | `C:\arma3-favela\odm\*.png`, `odm\preview_mapa\`, `odm\mapa_hoje\`, `odm\pessoas\` | cerca de 55 MB |

## Insumos abertos (não sensíveis, fora do git por peso ou licença)

| Item | Caminho | Tamanho |
|---|---|---|
| Poly Haven CC0: 72 texturas PBR 1k, 15 HDRI 2k, 29 modelos glTF | `C:\arma3-favela\assets\polyhaven\` | 735 MB |
| OSM (footprints e vias de Jacarezinho e Rocinha) e SRTM | `C:\arma3-favela\assets\osm\` | 4,3 MB |
| MakeHuman e MPFB (pacotes de instalação) | `C:\arma3-favela\assets\makehuman\`, `assets\mpfb\` | 311 MB |
| Human Base Meshes v1.1.0 (Blender Studio, CC0) | `C:\arma3-favela\assets\human-base-meshes-bundle-v1.1.0\` | 48 MB |
| Instalador do ODM 3.6.2 | `C:\arma3-favela\tools\ODM_Setup_3.6.2.exe` | 239 MB |
| Pacote de contexto de 11/09 descompactado (com os 18 PDFs) | `C:\arma3-favela\projeto_contexto\` | 102 MB |

## ARMA 3

| Item | Caminho |
|---|---|
| Jogo | `C:\Program Files (x86)\Steam\steamapps\common\Arma 3\` |
| Missão em uso | `C:\Users\marti\Documents\Arma 3\missions\dsFavela.Tanoa\` (copiada para `03-arma3/missao/`) |
| Logs `.rpt` | `C:\Users\marti\AppData\Local\Arma 3\`, 6 arquivos de 2026-09-11, nenhum com linha `DSIMG` ou `DSLBL` |
| Screenshots | A pasta `Documents\Arma 3\Screenshots\` não existe: nenhuma captura foi feita |
