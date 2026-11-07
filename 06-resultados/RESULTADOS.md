# RESULTADOS

Trazido do desktop em 2026-09-18 [DESKTOP]. A primeira parte (ficha) foi montada na reconciliação, conferindo cada número no arquivo de origem. A segunda parte é o `RESULTADOS-BLENDER.md` escrito no desktop em 12 e 13/09, sem alteração de conteúdo.

Aviso de leitura: o experimento NÃO rodou no ARMA 3. O ARMA 3 foi tentado em 11/09 e abandonado no mesmo dia sem gerar nenhuma imagem (ver `docs/DIVERGENCIAS.md`, item 1). Tudo abaixo é Blender 5.2 em modo headless. O código está em `03-blender/scripts/`.

## Ficha do experimento para o artigo

Convenções desta ficha: caminhos relativos são relativos a `06-resultados/`. Caminhos `C:\...` existem só no desktop (ver `ONDE-ESTAO-OS-DADOS.md`). Todos os comandos rodaram a partir de `C:\arma3-favela\blender\` com `BL` = `C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe` e `PY` = `C:\arma3-favela\venv\Scripts\python.exe`.

### 1. Datasets

Classes em todos: `0 pessoa_armada`, `1 pessoa_desarmada` (origem: `data.yaml` de cada dataset). Contagens feitas em 2026-09-17 lendo os `.txt` de `labels/`.

| Dataset | Base da cena | Usa dado PCERJ | Imagens train / val | Caixas train / val | Armada / desarmada | Resolução |
|---|---|---|---|---|---|---|
| `dataset_v3` | Footprints OSM do Jacarezinho + SRTM + materiais Poly Haven + densificação procedural | Não | 103 / 17 | 594 / 77 | 355 / 316 | 3840x2160 |
| `dataset_v3_tiles` | Ladrilhos de 1280 px do anterior, sobreposição 20% | Não | 520 / 80 | 1.028 / 145 | 598 / 575 | 1280x1280 |
| `dataset_odm` | Malha texturizada de fotogrametria (ODM) do setor Sudoeste | Sim (textura e geometria) | 105 / 15 | 750 / 107 | 450 / 407 | 3840x2160 |
| `dataset_odm_tiles` | Ladrilhos do anterior | Sim | 595 / 87 | 1.348 / 203 | 822 / 729 | 1280x1280 |
| `dataset_cid150` | "Cidade de sólidos": prédios segmentados do DSM do ODM, paredes verticais com PBR, laje com foto do ortomosaico misturada a concreto | Sim (geometria, e textura nas lajes) | 473 / 87 | 4.856 / 889 | 2.977 / 2.768 | 3840x2160 |
| `dataset_cid150_tiles` | Ladrilhos do anterior, 5% de ladrilhos vazios mantidos | Sim | 2.377 / 437 | 8.646 / 1.593 | 5.253 / 4.986 | 1280x1280 |
| `teste_angulos` | Mesma cidade, semente nova, ângulo e lente mais abertos | Sim | 0 / 60 | 0 / 596 | 310 / 286 | 3840x2160 |
| `teste_denso` | Mesma cidade, multidão | Sim | 0 / 40 | 0 / 1.749 | 890 / 859 | 3840x2160 |

Convenção de anotação: AMODAL, recortada na borda do quadro. A caixa é o envelope 2D de todos os vértices deformados do corpo e da arma projetados na câmera, inclusive os encobertos por prédio (`03-blender/scripts/people_mpfb.py`, função `bbox_2d`). A pessoa só é anotada se pelo menos 35% de 14 pontos amostrados do corpo têm linha de visão livre até a câmera (função `visibility`, parâmetro `--min-vis 0.35`). Lado mínimo da caixa: 0,2% do quadro (`--min-lado 0.002`). É a mesma lógica do VisDrone (objeto inteiro), com corte de visibilidade mínima.

Comandos que geraram os datasets:

```
# dataset_v3 (origem: run_batch_v3.sh)
BL -b --python gen_jacarezinho.py -- --area jacarezinho --out dataset_v3 --n 120 --res 3840 2160 --samples 48 --seed 2026 --pitch 55 90 --rebuild-every 6
PY post_process.py --data dataset_v3 --seed 7
PY tile_dataset.py --data dataset_v3 --out dataset_v3_tiles --tile 1280 --overlap 0.2

# dataset_odm (origem: dataset_real.sh)
BL -b --python gen_odm.py -- --out dataset_odm --n 120 --res 3840 2160 --samples 40 --seed 5051 --pitch 55 90 --people 5 10 --repool-every 10
PY post_process.py --data dataset_odm --seed 11 --blur 0.8 1.4
PY tile_dataset.py --data dataset_odm --out dataset_odm_tiles --tile 1280 --overlap 0.2

# dataset_cid150, teste_angulos, teste_denso (origem: run_batch_cidade.sh)
COMUM="--blend C:/arma3-favela/odm/quadra.blend --samples 32 --alt 150 --alt-jitter 12 --margem 150"
BL -b --python gen_cidade.py -- $COMUM --out dataset_cid150 --n 560 --seed 11 --pitch 50 90 --lens 30 50 --people 6 14 --val 0.15
BL -b --python gen_cidade.py -- $COMUM --out teste_angulos --n 60 --seed 77 --stamp ang --pitch 40 90 --lens 28 55 --people 6 14 --val 1.0
BL -b --python gen_cidade.py -- $COMUM --out teste_denso --n 40 --seed 99 --stamp den --pitch 50 90 --lens 30 50 --people 30 60 --raio 22 --grupo 0.7 --grupo-n 3 8 --val 1.0
PY post_process.py --data <cada um> --seed 5 --keep-png
PY tile_dataset.py --data dataset_cid150 --out dataset_cid150_tiles --tile 1280 --overlap 0.2 --keep-empty 0.05
```

### 2. Randomização da cena (medida, não nominal)

Faixas efetivamente sorteadas, lidas de `manifests/<dataset>.jsonl` (uma linha por imagem, gravada pelo gerador).

| Dataset | Altitude (m) | Pitch (graus, 90 = nadir) | Lente (mm, sensor 36) | Elevação do sol | Azimute do sol | Pessoas por cena | Luz |
|---|---|---|---|---|---|---|---|
| `dataset_v3` | 92,3 a 107,7 | 55,1 a 90,0 | 20,0 a 30,0 | 22,2 a 77,4 | 1,1 a 354,4 | 4 a 9 | céu físico 78, HDRI 42 |
| `dataset_odm` | 92,4 a 107,9 | 55,1 a 89,5 | 20,2 a 29,8 | 45,1 a 53,9 | -11,8 a 11,7 | 5 a 10 | HDRI + sol fraco, 120 |
| `dataset_cid150` | 138,1 a 162,0 | 50,0 a 89,9 | 30,1 a 50,0 | 28,0 a 71,9 | 0,0 a 359,5 | 6 a 17 | sol livre |
| `teste_angulos` | 139,1 a 162,0 | 43,7 a 89,8 | 28,2 a 54,1 | 28,4 a 71,4 | 4,7 a 345,5 | 6 a 17 | sol livre |
| `teste_denso` | 138,9 a 160,8 | 50,6 a 87,3 | 30,1 a 49,6 | 29,0 a 69,8 | 11,3 a 351,4 | 31 a 61 | sol livre |

Leitura importante: no `dataset_odm` o sol quase não varia (elevação 45 a 54, azimute dentro de 12 graus do norte). Não é descuido: a textura da fotogrametria já tem a sombra das 11h55 de 02/08/2022 gravada no pixel, então o gerador prende o sol perto da direção real. É exatamente o eixo que Liao et al. 2026 mostram custar cerca de 10 pontos de mAP50 quando não é variado. Ver `docs/DIVERGENCIAS.md`, item 5.

Outros eixos randomizados (origem: `03-blender/README.md`, seção "O que a cena v3 contém", e o código): yaw livre de 0 a 360, fração de armados 0,5 (`--prob-armado`), pool de 6 humanos MPFB por lote com idade, sexo, biotipo, roupa e pose sorteados, poses nomeadas no `cid150` (parado, andando, sentado, lado, costas, empunhando, braços cruzados), pavimentos de 1 a 5, adição em laje, cobertura, caixa d'água, props. Pós-processamento de câmera (`post_process.py`): ruído de sensor, desfoque, aberração cromática, vinheta, neblina, compressão JPEG.

### 3. Modelo e hiperparâmetros

Script: `03-blender/scripts/train_yolo_win.py`. Aumentos fixos no script: `hsv_h=0.015, hsv_s=0.6, hsv_v=0.4, degrees=10, scale=0.4, fliplr=0.5, mosaic=1.0, patience=15`. Demais valores: padrão do Ultralytics 8.4.148 (`optimizer=auto, lr0=0.01, amp=true, seed=0`). Origem de cada linha: `<run>/args.yaml`.

| Run | Pesos iniciais | Dataset | Épocas pedidas / feitas | imgsz | batch | workers |
|---|---|---|---|---|---|---|
| `blender_v3` | yolo11n.pt (COCO) | `dataset_v3` | 40 / 40 | 1536 | 4 | 4 |
| `blender_v3_tiles` | yolo11s.pt (COCO) | `dataset_v3_tiles` | 60 / 7 (processo morto por falta de RAM) | 1280 | 4 | 4 |
| `blender_v3_tiles2` | `best.pt` do run anterior | `dataset_v3_tiles` | 60 / 60 | 1280 | 4 | 2 |
| `blender_odm_tiles` | yolo11s.pt (COCO) | `dataset_odm_tiles` | 60 / 60 | 1280 | 4 | 2 |
| `cid150_s` | yolo11s.pt (COCO) | `dataset_cid150_tiles` | 60 / 60 | 1280 | 6 | 4 |

Comando tipo (os outros mudam `--data`, `--model`, `--batch`, `--workers`, `--name`):

```
PY train_yolo_win.py --data dataset_cid150_tiles/data.yaml --model yolo11s.pt --epochs 60 --imgsz 1280 --batch 6 --workers 4 --name cid150_s
```

Ressalva para o artigo: o `blender_v3_tiles2` soma 7 + 60 épocas sobre o mesmo dataset, porque partiu do `best.pt` do run interrompido. Não é comparável época a época com os outros.

### 4. Hardware e tempo

Máquina: Ryzen 5 5600X, 32 GB de RAM, NVIDIA GeForce RTX 2060 de 6 GB, Windows 10 Pro, PyTorch 2.14.0+cu126 (detalhes em `docs/AMBIENTE-DESKTOP.md`).

| Etapa | Tempo | Origem |
|---|---|---|
| Render `dataset_v3` (120 imagens 4K, Cycles 48 amostras) | 91 min somados, 25 a 29 s por imagem típica (uma imagem isolada levou 452 s com a máquina disputada) | `manifests/dataset_v3.jsonl`, campo `render_s` |
| Render `dataset_odm` (120 imagens 4K, 40 amostras) | 36 min, 16 a 20 s por imagem | `manifests/dataset_odm.jsonl` |
| Render `dataset_cid150` (560 imagens 4K, 32 amostras) | 398 min (6 h 38 min), 41 a 49 s por imagem | `manifests/dataset_cid150.jsonl` |
| Treino `blender_v3` | 1.223 s (20 min) | `blender_v3/results.csv`, coluna `time`, última linha |
| Treino `blender_v3_tiles` (7 épocas) | 4.585 s (76 min, máquina disputada com Blender e ODM) | `blender_v3_tiles/results.csv` |
| Treino `blender_v3_tiles2` | 2.155 s (36 min) | `blender_v3_tiles2/results.csv` |
| Treino `blender_odm_tiles` | 2.325 s (39 min) | `blender_odm_tiles/results.csv` |
| Treino `cid150_s` | 32.025 s (8 h 54 min) | `cid150_s/results.csv` |

### 5. Métricas no sintético

Validação do `best.pt` no split `val` do próprio dataset, feita automaticamente ao fim de `train_yolo_win.py` (`modelo.val(data=..., imgsz=...)`). Origem do agregado: `<run>/val_final.json`. Origem das linhas por classe: `<run>/val_por_classe.txt` (extrato do log de treino).

| Run | Classe | Precisão | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| `blender_v3` (4K reduzido a 1536) | todas | 0,272 | 0,186 | 0,116 | 0,031 |
| `blender_v3_tiles2` (ladrilhos 1280) | todas | 0,737 | 0,497 | 0,561 | 0,238 |
| | pessoa_armada | 0,775 | 0,500 | 0,591 | 0,244 |
| | pessoa_desarmada | 0,698 | 0,493 | 0,532 | 0,232 |
| `blender_odm_tiles` | todas | 0,616 | 0,639 | 0,646 | 0,340 |
| | pessoa_armada | 0,634 | 0,550 | 0,611 | 0,287 |
| | pessoa_desarmada | 0,598 | 0,727 | 0,681 | 0,392 |
| `cid150_s` | todas | 0,664 | 0,665 | 0,676 | 0,327 |
| | pessoa_armada | 0,712 | 0,665 | 0,732 | 0,358 |
| | pessoa_desarmada | 0,617 | 0,666 | 0,620 | 0,297 |

Os conjuntos de validação são diferentes entre si: a tabela não ordena pipelines, só mostra que cada fonte produz dado aprendível. A única comparação controlada é `blender_v3` contra `blender_v3_tiles2` (mesmas 120 imagens, muda a escala de treino): mAP50 de 0,116 para 0,561.

Teste do `cid150_s` em imagem 4K inteira com inferência fatiada (conf 0,25, IoU 0,5), em conjuntos sintéticos de semente nova:

```
PY eval_cidade.py --pesos runs/detect/cid150_s/weights/best.pt --data teste_angulos --out aval_angulos
PY eval_cidade.py --pesos runs/detect/cid150_s/weights/best.pt --data teste_denso --out aval_denso
```

A linha de comando exata não ficou gravada em arquivo: foi reconstruída a partir dos campos `pesos`, `data` e `conf` dos JSON de saída e dos valores padrão do script (`--tile 1280 --overlap 0.2 --conf 0.25 --iou-match 0.5`). Rodar de novo reproduz os números, porque o script não tem componente aleatório.

| Conjunto | Imagens | Caixas | TP / FP / FN | Precisão | Recall | F1 | Acurácia armado x desarmado entre caixas casadas | Origem |
|---|---|---|---|---|---|---|---|---|
| `teste_angulos` | 60 | 596 | 493 / 72 / 103 | 0,873 | 0,827 | 0,849 | 0,781 | `cid150_s/teste_angulos.json` |
| `teste_denso` | 40 | 1.749 | 1.305 / 261 / 444 | 0,833 | 0,746 | 0,787 | 0,759 | `cid150_s/teste_denso.json` |

Estes dois testes são sintético contra sintético, na mesma cidade, com a mesma biblioteca de pessoas e a mesma arma. Não são sim-to-real.

### 6. Métricas em imagem real (os três números do artigo)

| Número | Valor | Situação |
|---|---|---|
| mAP no VisDrone, zero-shot | NÃO EXISTE | Nenhuma avaliação em imagem real foi feita. O VisDrone não está no disco do desktop |
| mAP com 5 a 10% de dado real | NÃO EXISTE | Idem |
| mAP sintético mais real | NÃO EXISTE | Idem |

O script já tem o caminho pronto (`train_yolo_win.py --eval-only --weights <best.pt> --real visdrone_yolo/data.yaml --single-cls`), e `02-projeto-ufrj-2022/arma3-2022/scripts/visdrone_to_yolo.py` converte o VisDrone. Falta baixar o VisDrone-DET, converter mantendo só `pedestrian` e `people` numa classe única, e rodar. Observação de desenho: o VisDrone voa mais baixo do que 100 a 150 m e não tem a classe "armada", então o zero-shot mede detecção de pessoa (classe única), não a distinção armado e desarmado.

### 7. Números sem arquivo de origem

Nenhum dos números desta ficha ficou sem origem. Os números da narrativa abaixo que não constam de arquivo copiado para cá estão marcados:

- "9 das 13 pessoas encontradas, 12 previsões" e "10 de 14 pessoas, 14 previsões" (folhas de `preview_deteccao.py`): [SEM ARQUIVO DE ORIGEM] no repositório. As folhas existem no desktop como PNG (`C:\arma3-favela\odm\exemplo_treino_final.png` e `exemplo_malha_real.png`), a segunda com textura PCERJ. Contagem feita a olho na sessão de 12/09. Não usar no artigo.
- "38 previsões para 13 pessoas" com o modelo anterior: [SEM ARQUIVO DE ORIGEM]. Não usar.
- Tempos "23 min contra 20 s" do render com e sem subdivisão: origem em log do desktop (`C:\arma3-favela\blender\build_map_final.log` e `hq_preview.log`), não copiados porque trazem coordenadas. Podem ser citados como ordem de grandeza.

---

## Narrativa original do desktop (RESULTADOS-BLENDER.md, 12 e 13/09/2026)


Atualizado em 2026-09-12. Este arquivo registra o que foi feito, o que funcionou, o que não funcionou e os números medidos. Escrito para virar insumo da Seção 7 do artigo.

### 1. Reconstrução do Jacarezinho a partir das fotos da PCERJ

As 567 fotos de agosto de 2022 (Zenmuse Z30, 1920x1080, nadir, 150 m de altura relativa, passo de 21,6 m) foram processadas no OpenDroneMap 3.6.2 nativo em Windows.

| Setor | Fotos | Ortomosaico | Área coberta | Nuvem densa |
|---|---|---|---|---|
| Sudoeste | 217 | 7,4 cm/px | 707 x 680 m | 632 MB (cerca de 20 M pontos) |
| Nordeste | 350 | 6,4 cm/px | 983 x 947 m | processada |

Saídas por setor: ortomosaico GeoTIFF, modelo digital de superfície, nuvem densa e malha texturizada.

Unindo os dois pelo georreferenciamento UTM real, sem ajuste manual, o mapa fica com **1.368 x 1.115 m**, cerca de 1,5 km².

Observação importante para o artigo: as pastas "output" do Drive de 2022 estavam vazias. O processamento fotogramétrico da época se perdeu e foi inteiramente refeito aqui.

### 2. Limite do dado, declarado

Todas as 567 fotos são em nadir. Não existe nenhuma foto oblíqua. Consequência direta: as paredes verticais não têm textura própria e são esticadas a partir dos pixels do telhado e da rua. O mapa se sustenta de cima até cerca de 45 m de altura de câmera e derrete ao nível da rua.

Isso importa para a tese do artigo. A morfologia vertical de favela (altura de edificação, adição em laje, transição de material) é justamente o que um voo em nadir captura pior. Um levantamento voltado a esse problema precisa de câmera oblíqua.

### 3. Mapa navegável no Blender

`build_map.py` monta um `.blend` único com:

- malha de fotogrametria de cada setor, posicionada pelo UTM;
- malha 2.5D do modelo de superfície com o ortomosaico aplicado, 25 cm por baixo, tapando buracos e bordas (1,16 milhão de faces sem dado removidas nos dois setores);
- moldura de terreno fechando o horizonte, na cota do percentil 3 do terreno medida por 1.600 raios verticais;
- sol calculado para a data e hora reais do voo: 02/08/2022, 11h55, elevação 49,4 graus, azimute 1,6 graus;
- pessoas MPFB vestidas, colocadas por ray cast só onde a superfície é quase horizontal;
- cinco câmeras e uma rota de voo animada.

### Decisões de iluminação

A textura da fotogrametria já traz o sol e as sombras gravados no pixel. Somar um sol forte escurece a cena duas vezes e a deixa azulada. A solução foi separar o que a câmera vê do que ilumina: o céu físico entra só por raio de câmera (nó Light Path), e a iluminação vem de um ambiente neutro levemente quente.

### Desempenho: a lição mais cara

O MPFB entrega cada peça de corpo e roupa com modificador de subdivisão. Numa vista de drone a 100 m a pessoa ocupa de 11 a 41 px, então subdividir não muda nada na imagem e multiplica o custo de avaliação da cena.

| Render de um quadro, mapa com 200 pessoas | Com subdivisão | Sem subdivisão |
|---|---|---|
| Vista de topo | 23 min | 20 s |
| Câmera de voo | não terminou | 8 s |

O mesmo problema estava tornando a geração do dataset sobre a malha real inviável, a 10 minutos por imagem.

### 4. Detector: o efeito do ladrilhamento

Dataset v3 (favela procedural sobre footprints do OpenStreetMap): 120 imagens 4K, 671 caixas, classes pessoa_armada e pessoa_desarmada.

O problema é de escala. Uma pessoa a 100 m ocupa de 11 a 41 px no 4K. Treinando com `imgsz=1536` a imagem encolhe 2,5 vezes e a pessoa vira de 4 a 16 px. O menor stride do YOLO é 8, então um alvo de 4 px praticamente não chega à rede.

`tile_dataset.py` recorta o 4K em ladrilhos de 1280 px com 20% de sobreposição, preservando o tamanho original do alvo: 600 ladrilhos, 1.173 caixas.

| Treino | Precisão | Recolocação | mAP50 | mAP50-95 |
|---|---|---|---|---|
| 4K reduzido para 1536, yolo11n, 40 épocas | 0,272 | 0,186 | 0,116 | 0,031 |
| ladrilhos 1280 em escala nativa, yolo11s, época 5 | 0,354 | 0,461 | 0,296 | 0,113 |
| ladrilhos 1280, yolo11s, treino completo | **0,737** | **0,497** | **0,561** | **0,238** |

Por classe, no treino completo:

| Classe | Precisão | Recolocação | mAP50 |
|---|---|---|---|
| pessoa_armada | 0,775 | 0,500 | 0,591 |
| pessoa_desarmada | 0,698 | 0,493 | 0,532 |

O ladrilhamento sozinho multiplicou o mAP50 por 4,8, de 0,116 para 0,561, sem mudar nada no dataset.
Esse é o achado metodológico mais forte do experimento até aqui: em imagem aérea de favela a 100 m,
a escolha de escala de treino pesa mais do que o volume de dados.

### O que a folha de detecção mostra

`preview_deteccao.py` monta uma folha com a anotação em verde e a previsão em vermelho ou azul.
Em 6 ladrilhos de validação, com confiança mínima de 0,35: 9 das 13 pessoas encontradas e apenas
12 previsões no total, com confiança tipicamente entre 0,7 e 0,8. Com o modelo anterior, o mesmo
recorte dava 38 previsões para 13 pessoas.

Sobre a distinção armado e desarmado: ela **funciona no dado sintético**, com mAP50 de 0,591 contra
0,532. Isso contraria a expectativa inicial de que um fuzil de 3 ou 4 px seria indistinguível.
A ressalva necessária para o artigo é que no sintético a arma é sempre o mesmo modelo, sempre na
mesma posição em relação ao corpo e sempre com o mesmo contraste. Não há prova nenhuma de que essa
separação sobreviva ao dado real, e a medida de sim-to-real ainda não foi feita. Reportar essa
distinção como capacidade validada seria exatamente o tipo de salto que o artigo critica na
literatura de policiamento aéreo.

### 4b. Dataset sobre a malha real do Jacarezinho

`gen_odm.py` coloca as pessoas MPFB sobre a malha de fotogrametria, por ray cast, só onde a
superfície é quase horizontal, e renderiza com a câmera de drone. A imagem resultante tem
**geometria e textura reais do Jacarezinho** com **anotação exata e sem custo humano**.

120 imagens 4K, 857 caixas, 41 minutos de render (18 s por imagem). Ladrilhado em 1280 px:
682 ladrilhos, 1.551 caixas.

| Dataset (validação própria de cada um) | Precisão | Recolocação | mAP50 | mAP50-95 |
|---|---|---|---|---|
| v3 procedural (OSM + PBR + props) | 0,737 | 0,497 | 0,561 | 0,238 |
| malha real do ODM | 0,616 | 0,639 | 0,646 | 0,340 |

Ressalva metodológica: são dois conjuntos de validação diferentes, então os números não provam
que um pipeline é melhor que o outro. O que eles mostram é que as duas fontes produzem dado
aprendível, e que a malha real entrega recolocação e mAP50-95 sensivelmente maiores.

Na folha de detecção sobre a malha real, com confiança 0,35: 10 de 14 pessoas encontradas,
14 previsões. As falhas se concentram em pessoa sobre vegetação e em pessoa na borda do ladrilho.

Limitação visível nessa imagem: a textura da malha vem de fotos 1080p a 150 m, ou seja, cerca de
9 cm por pixel no solo. A pessoa aparece como uma mancha escura de poucos pixels, com muito menos
contraste do que no dataset procedural, onde ela é renderizada em resolução plena. Isso é fiel ao
que a câmera da PCERJ realmente capta, e por isso é o cenário mais honesto dos dois.

### 5. Falhas encontradas e registradas

- `train_yolo.py` do pacote original trava no Windows: executa o treino no nível do módulo, e o DataLoader com `workers > 0` reimporta o arquivo e dispara o treino dentro de cada worker. Corrigido em `train_yolo_win.py`.
- A remalhagem do Sudoeste para 3 M e depois 1,5 M de faces parou de consumir CPU nas duas tentativas enquanto disputava memória com outros processos. Retomada isolada.
- Um treino caiu por falta de RAM do sistema quando Blender, OpenDroneMap e os workers do DataLoader rodavam juntos numa máquina de 32 GB.
- No Blender 5, `matrix_world` fica desatualizada depois de mover um objeto até chamar `view_layer.update()`. Isso fez o segundo setor entrar com limites errados e centrou as câmeras no lugar errado.
- No Blender 5, o formato de vídeo só aparece depois de marcar `image_settings.media_type = 'VIDEO'`.

### 6. Próximos passos

1. Terminar o treino em ladrilhos e medir sim-to-real no VisDrone, zero-shot e com ajuste fino.
2. Gerar o dataset sobre a malha real (`gen_odm.py`), agora viável com a correção de desempenho.
3. Anotar à mão cerca de 50 pessoas nas fotos reais para ter um teste real interno.
4. Segundo experimento do artigo: trocar a anotação de pessoa por edificação, usando os dados de pavimentos e footprint que o gerador já guarda.

### Cidade de solidos a 150 m (13/09/2026): treino com 560 imagens e testes de acuracia

Pipeline: `gen_cidade.py` sobre `odm/quadra.blend` (segmentacao DSM + build_cidade.py), pessoas v2 (people_mpfb),
altitude 150 m +- 12 m, 4K, Cycles 32 amostras (~43 s por imagem), `post_process.py`, `tile_dataset.py` 1280 px,
`train_yolo_win.py` YOLO11s 60 epocas imgsz 1280. Script da batelada: `run_batch_cidade.sh`. Avaliacao em imagem
inteira com inferencia fatiada: `eval_cidade.py` (conf 0,25, IoU 0,5).

| Conjunto | Imagens | Caixas | Precisao | Recall | F1 | Acuracia armado x desarmado (caixas casadas) |
|---|---|---|---|---|---|---|
| Treino/val (ladrilhos, val) | 473 / 87 (2814 ladrilhos) | 5745 | 0,664 | 0,665 | mAP50 0,676 (armada 0,732 / desarmada 0,620) | |
| Teste angulos e luz (pitch 40 a 90, lente 28 a 55, sol livre, semente nova) | 60 | 596 | 0,873 | 0,827 | 0,849 | 0,781 (recall armado 0,773, desarmado 0,790) |
| Teste multidao (30 a 60 pessoas, grupos de 3 a 8) | 40 | 1749 | 0,833 | 0,746 | 0,787 | 0,759 (recall armado 0,727, desarmado 0,796) |

Leitura: a deteccao de pessoas a 150 m fica acima de 80% de F1 nos dois testes; a separacao armado x desarmado
fica em torno de 76 a 78%, ou seja, no limite da meta de 75%. Na multidao o recall cai (0,75) por oclusao mutua e
por caixas coladas; a confusao entre classes cresce quando o fuzil fica encoberto por outra pessoa.
Pesos: `runs/detect/cid150_s/weights/best.pt`. Resultados: `aval_angulos/resultado.json`, `aval_denso/resultado.json`.

## 2026-11-07 [DESKTOP] Rodada 6, grupo G (item 3): ruído, borrão e JPEG como aumento

Plano e critério fixados antes em `03-blender/PLANO-RODADA6.md`, seção 3.5. Ladrilhos degradados por `03-blender/scripts/degrada_ladrilhos.py --src C:/arma3-favela/blender/ds_morro_4k_tiles --out C:/arma3-favela/blender/ds_morro_4k_deg_tiles` (e o mesmo para `ds_oblvar_tiles`): 75% dos ladrilhos de treino com ruído gaussiano dependente do sinal (sigma 0,004 a 0,018), borrão de 0,3 a 1,2 px e JPEG 50 a 90 com 4:2:0, semente 0, validação intacta, parâmetros em `_degradacao.json`. Treinos `s_nadir_4k_deg` (parou na 42) e `s_oblvar_deg` (fez as 60), receita da 7.6, semente 0. Zero-shot por `avalia_sim2real.py` (VisDrone val, imgsz 1280; `sim2real_s_nadir_4k_deg.json`, `sim2real_s_oblvar_deg.json`), predições por `visdrone_preds.py` e `preds_nadir.py` (HERIDAL, tags `heridal` a 1152 e `heridal_1280`). Critério por `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/rodada6_criterios.py --parte G` (1.000 reamostras pareadas por imagem, semente 0). Lado degradado: uma semente; lado limpo: média das três sementes existentes.

| Corpus e benchmark | Limpo, 3 sementes (faixa) | Degradado, 1 semente | Diferença (IC 95% pareado) | Relativa | Leituras |
|---|---|---|---|---|---|
| S-nadir-150, VisDrone val | 0,0136 (0,0102 a 0,0198) | 0,0132 | −0,0004 (−0,0019 a +0,0010) | −3,3% | nenhuma |
| S-oblique-six, VisDrone val | 0,0966 (0,0887 a 0,1055) | 0,1037 | +0,0070 (+0,0022 a +0,0119) | +7,3% | (b) |
| S-nadir-150, HERIDAL (1152) | 0,1997 (0,0926 a 0,2672) | 0,2190 | +0,0192 (+0,0077 a +0,0309) | +9,6% | (b) |
| S-oblique-six, HERIDAL (1152) | 0,1477 (0,1079 a 0,1847) | 0,1476 | −0,0000 (−0,0105 a +0,0096) | 0,0% | nenhuma |

Veredito pela regra fixada antes: **resolvível para cima em duas das quatro células (S-oblique-six no VisDrone, S-nadir-150 na HERIDAL), pela leitura (b); nulo nas outras duas; nenhuma passa em (c)**. Ressalva que pesa na leitura: nas duas células resolvíveis o valor degradado cai dentro da faixa das três sementes limpas (0,1037 dentro de 0,0887 a 0,1055; 0,2190 dentro de 0,0926 a 0,2672). O intervalo (b) mede a variação por imagem com os treinos fixos, não a dispersão entre treinos; a leitura (a), que mede essa dispersão, só existe depois das sementes 1 e 2 do lado degradado (grupo T, etapas T6 a T10).

Consequência para o texto (não aplicada; aplicação no Mac): por ora, os artefatos de sensor explicam no máximo uma fração pequena da lacuna (ganhos de 7 a 10% relativos, menores que a dispersão entre sementes) e nenhuma nos outros dois casos; a frase da 6.5 pode passar de "não medido" a "medido: efeito pequeno e inconsistente entre benchmarks, dentro da dispersão de treino", à espera das sementes para dizer se é resolvível em (a).

## 2026-11-07 [DESKTOP] Rodada 6, grupo L (item 6): o comprimento como atalho, testado

Plano e critério fixados antes em `03-blender/PLANO-RODADA6.md`, seção 3.3. Gerador com `--objetos-comprimento-arma` (objeto confundível escalado só no eixo do comprimento até 0,62 a 1,05 m, a faixa das cinco armas; `03-blender/scripts/objetos_alongados.py`, `COMPRIMENTO_ARMA`). Cadeia `03-blender/scripts/rodada6.py`, etapas L1 a L9: `ds_armado_75c` (200 quadros, comando do gêmeo de 75 m mais a flag) e treino `armado_75c` (receita do `armado_75g`, 60 épocas, fez as 60); `ds_armado_150c` (200 quadros, comando do gêmeo de 150 m mais a flag) e treino `armado_150c_e120` (receita do `armado_150g_e120`, parou por paciência na 106, `best.pt` na 37; pausa do autor de 15:38 a 17:54 de 06/11); 80 quadros novos de cada (índices 200 a 279, `ds_armado_75c_extra`, `ds_armado_150c_extra`). Confusões por `06-resultados/confusao_armado.py --pesos <run>/weights/best.pt --ds <ds> --split val --instancias` (imgsz 3840, conf 0,25, IoU 0,50): `extra_armado_75c.json`, `extra_armado_150c_e120.json` e os cruzados `extra75c_armado_75g.json`, `extra150c_armado_150g_e120.json`, `extra75g_armado_75c.json`, `extra150g_armado_150c_e120.json`. Critério por `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/rodada6_criterios.py --parte L` (`rodada6_criterios.json`, item L; 1.000 reamostras de quadros, semente 0, independentes entre corpora). Uma semente por modelo.

Nos 80 quadros novos:

| Modelo e quadros | d′ armada contra objeto (IC 95%) | Objeto chamado de armada (IC 95%) | Armada chamada de armada | Recall em qualquer classe |
|---|---|---|---|---|
| 75 m original (`armado_75g`), quadros originais | 0,973 (0,772 a 1,192) | 0,125 (0,090 a 0,162) | 0,432 | 0,766 |
| 75 m sem o comprimento (`armado_75c`), quadros de comprimento igual | 0,444 (0,237 a 0,655) | 0,201 (0,150 a 0,255) | 0,347 | 0,806 |
| 75 m original nos quadros de comprimento igual | 0,830 (0,627 a 1,052) | 0,208 (0,162 a 0,255) | 0,508 | 0,797 |
| 150 m original (`armado_150g_e120`), quadros originais | 0,579 (0,376 a 0,780) | 0,245 (0,204 a 0,289) | 0,457 | 0,663 |
| 150 m sem o comprimento (`armado_150c_e120`), quadros de comprimento igual | 0,117 (−0,091 a 0,318) | 0,158 (0,121 a 0,201) | 0,188 | 0,623 |
| 150 m original nos quadros de comprimento igual | 0,247 (0,034 a 0,442) | 0,368 (0,320 a 0,418) | 0,464 | 0,710 |

Comparações (sem o comprimento menos original, cada um nos seus quadros novos; reamostragem independente):
- 75 m: d′ −0,529 (IC −0,821 a −0,246), passa em (b) e (c); objeto chamado de armada +0,076 (IC +0,016 a +0,135), passa em (b) e (c).
- 150 m: d′ −0,462 (IC −0,738 a −0,191), passa em (b) e (c); objeto chamado de armada −0,087 (IC −0,145 a −0,031), passa em (b) e (c), mas porque o modelo quase deixa de chamar qualquer coisa de armada (armada chamada de armada 0,188).
- Cruzado, original nos quadros de comprimento igual menos nos seus: a 75 m, objeto chamado de armada +0,083 (IC +0,026 a +0,141), d′ −0,143 não resolvível; a 150 m, objeto chamado de armada +0,123 (IC +0,053 a +0,190), d′ −0,332 (IC −0,606 a −0,077), ambos em (b) e (c).

Veredito pela regra fixada antes: **a 150 m, sem o comprimento o IC de d′ inclui zero: a separação dependia do comprimento (atalho confirmado). A 75 m a forma sobrevive sem o comprimento (d′ 0,444, IC exclui zero), mas a separação cai à metade (−0,529, resolvível)**. Leitura descritiva do cruzado: o modelo original, sem retreino, passa a chamar de armada 21% (75 m) e 37% (150 m) dos objetos quando eles têm o comprimento de uma arma, contra 12,5% e 24,5% nos seus quadros.

Consequência para o texto (não aplicada; aplicação no Mac): a regra "a forma se perde a 4,88 cm/px", hoje uma leitura, passa a medida a 150 m: sem o comprimento não há separação acima do acaso. O comprimento, hoje "alternativa não testada" (6.2, 6.4), passa a causa demonstrada de toda a separação a 150 m e de cerca de metade a 75 m. O cruzado dá um número de risco direto: um objeto cotidiano do comprimento de uma arma é chamado de arma em cerca de um terço dos casos a 150 m pelo modelo treinado no corpus original. Ressalva: uma semente por modelo.

## 2026-11-07 [DESKTOP] Rodada 6, grupo R (item 4, acertos): R-sel na HERIDAL e todas as linhas da Tabela 4

Seção 8 do plano (ordem nova de 05/11). R3: `revisao-2026-10-17/preds_nadir.py --data C:/arma3-favela/real_nadir/heridal/yolo/data.yaml --tag heridal --imgsz 1152 --modelos r_pareado_sel --batch 4` e o mesmo com `--tag heridal_1280 --imgsz 1280`; zero-shot por `03-blender/scripts/avalia_sim2real.py --weights runs/detect/r_pareado_sel/weights/best.pt --real <HERIDAL> --imgsz 1152 --out 06-resultados/sim2real_r_pareado_sel_heridal.json` (e 1280, `_heridal_1280.json`). R4: `rodada6_criterios.py --parte R` (1.000 reamostras pareadas das 1.647 imagens, semente 0). Saídas em `rodada6_eficacias.json/.md` (seções "Cada treino individual" e "HERIDAL"). As linhas do VisDrone com F-joint e cada treino individual foram feitas à mão em 05/11 às 21:50 (mesmo comando).

HERIDAL, imgsz casado (1152):

| Modelo | mAP50 (IC 95%) | Eficácia / R (antes) | Eficácia / R-sel (IC 95%) |
|---|---|---|---|
| R (seleção no VisDrone val) | 0,3185 (0,2843 a 0,3543) | 100% | 108,8% (103,8 a 114,5) |
| R-sel (seleção fora do teste) | 0,2927 (0,2618 a 0,3247) | 91,9% | 100% |
| S-nadir-150, 3 sementes | 0,1997 (0,1713 a 0,2306) | 62,7% | 68,2% (59,0 a 78,9) |
| S-nadir-150-six | 0,2488 (0,2116 a 0,2865) | 78,1% | 85,0% (73,2 a 98,2) |
| S-oblique, 3 sementes | 0,1341 (0,1149 a 0,1555) | 42,1% | 45,8% (40,6 a 52,6) |
| S-oblique-six, 3 sementes | 0,1477 (0,1265 a 0,1715) | 46,4% | 50,5% (44,6 a 57,3) |
| Armado-150 (exploratório) | 0,1417 (0,1145 a 0,1711) | 44,5% | 48,4% (40,3 a 57,8) |

A imgsz 1280: R 0,3353, R-sel 0,3026; eficácias / R-sel 55,6% (S-nadir-150), 73,0% (S-nadir-150-six), 47,0% (S-oblique), 46,9% (S-oblique-six), 42,0% (Armado-150).

Leitura: na HERIDAL a seleção no VisDrone val pesa mais que no próprio VisDrone. R menos R-sel é +0,0258 (IC pareado +0,0113 a +0,0421), 8,8% relativos, contra 1,4% no VisDrone; o checkpoint escolhido no teste urbano generaliza melhor para o nadir por acaso de época. Com R-sel no denominador, todas as eficácias na HERIDAL sobem cerca de 9% relativos, e nenhuma ordem muda (nadir acima do oblíquo, as faixas como antes). Consequência para o texto (não aplicada): as linhas da HERIDAL da Tabela 4 e do resumo passam a 68,2% (nadir) contra 45,8% e 50,5% (oblíquos), com R-sel 0,2927 como teto.

## 2026-11-05 [DESKTOP] Rodada 6, grupo Q (item 5): a forma em U da QP3 com orçamento igual

Plano e critério fixados antes em `03-blender/PLANO-RODADA6.md`, seção 3.2. Treinos de três classes com a receita do `armado_150g_e120` (120 épocas, paciência 30), cadeia `03-blender/scripts/rodada6.py`, etapas Q1 e Q2: `armado_35_e120` (`ds_armado_35_tiles`, fez as 120, `best.pt` na época 116) e `armado_75g_e120` (`ds_armado_75g_tiles`, parou por paciência na 109, `best.pt` na 74; pausa do autor de 08:47 a 11:42, retomada de `last.pt`). Confusão por `06-resultados/confusao_armado.py --pesos <run>/weights/best.pt --ds <ds> --split val --instancias` no val e nos 80 quadros novos (`confusao_armado_35_e120.json`, `extra_armado_35_e120.json`, `confusao_armado_75g_e120.json`, `extra_armado_75g_e120.json`; imgsz 3840, conf 0,25, IoU 0,50). Critério por `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/rodada6_criterios.py --parte Q` (`rodada6_criterios.json`, item Q; 1.000 reamostras de quadros, semente 0). O lado de 60 épocas é a média das três sementes já existentes (`extra_armado_35*.json`, `extra_armado_75g*.json`); o de 120 épocas é uma semente (as sementes 1 e 2 estão no grupo T).

Nos 80 quadros novos (índices 200 a 279, os mesmos nas três altitudes):

| Altitude, orçamento | Objeto chamado de armada (IC 95%) | d′ armada contra objeto (IC 95%) | Recall em qualquer classe |
|---|---|---|---|
| 35 m, 60 épocas (média de 3 sementes) | 0,2215 | 0,759 | 0,694 |
| 75 m gêmeo, 60 épocas (média de 3 sementes) | 0,1343 | 0,980 | 0,740 |
| 35 m, 120 épocas | 0,1918 (0,1515 a 0,2357) | 0,875 (0,654 a 1,087) | 0,739 |
| 75 m gêmeo, 120 épocas | 0,2222 (0,1742 a 0,2711) | 0,854 (0,646 a 1,071) | 0,761 |
| 150 m gêmeo, 120 épocas (rodada 5) | 0,2452 (0,2042 a 0,2890) | 0,579 (0,376 a 0,780) | 0,663 |

Comparações:
- 75 m, 120 contra 60 épocas (pareado): objeto chamado de armada +0,0879 (IC +0,0441 a +0,1311), passa em (b) e (c); d′ −0,126 (IC −0,349 a +0,088), não resolvível. Com o orçamento maior, o gêmeo de 75 m passa a chamar mais objetos de armada.
- 35 m, 120 contra 60 épocas: objeto chamado de armada −0,0297 (IC −0,0634 a +0,0037); d′ +0,116 (IC −0,045 a +0,262); nenhum resolvível.
- Curva com orçamento igual, 75 contra 35 m: objeto chamado de armada +0,0304 (IC −0,0322 a +0,0914), d′ −0,021; nenhum resolvível.
- 75 contra 150 m: objeto chamado de armada −0,0230 (IC −0,0887 a +0,0428), não resolvível; d′ +0,275 (IC −0,006 a +0,552), passa só em (c).

Veredito pela regra fixada antes: **a forma em U era (em parte) orçamento**. Com 120 épocas nas três altitudes, o falso alarme sobre objetos fica entre 0,19 e 0,25 e nenhuma diferença entre altitudes passa em (b); a vantagem de 75 m sobre 35 e 150 m, medida com 60 épocas a 35 e 75 m, não sobrevive ao orçamento igual. O que sobra, descritivo: a 150 m o d′ é o mais baixo (0,58 contra 0,85 a 0,88), mas a diferença para 75 m não passa em (b). Ressalva: o lado de 120 épocas tem uma semente; as sementes 1 e 2 (grupo T, etapas T1 a T5) refazem o critério com (a).

## 2026-11-04 [DESKTOP] Rodada 6, grupo R (item 4): teto R com o checkpoint escolhido fora do teste

Plano e critério fixados antes em `03-blender/PLANO-RODADA6.md`, seção 3.1. Treino `r_pareado_sel` pela cadeia `03-blender/scripts/r_sel.py` (receita exata de `r_pareado`: yolo11s.pt, as 1.106 imagens de `visdrone_sub/train`, 60 épocas, lote 6, imgsz 1280, paciência 15, semente 0, classe única; `train_yolo_win.py --dry-run --compara runs/detect/r_pareado/args.yaml` acusa só `data` e `name`), com `val` em `C:/arma3-favela/visdrone/ft/sel_r.txt`: 265 imagens do VisDrone train fora da amostra de R e fora do VisDrone val (a fatia `sel` de 324 menos 59 em comum com `visdrone_sub/train`, `ft/sel_r.json`). Fez as 60 épocas (pausa do autor de 14:38 a 16:11, retomada de `last.pt` na época 31); `best.pt` na época 55 (mAP50-95 em `sel_r` 0,2285). Zero-shot por `03-blender/scripts/avalia_sim2real.py --weights runs/detect/r_pareado_sel/weights/best.pt --real C:/arma3-favela/visdrone/visdrone_yolo/data.yaml --imgsz 1280 --out 06-resultados/sim2real_r_pareado_sel.json`; predições por imagem por `revisao-2026-10-17/visdrone_preds.py --modelos r_pareado_sel --batch 4`; critério e eficácias por `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/rodada6_criterios.py --parte R` (saídas `rodada6_criterios.json`, `rodada6_eficacias.json` e `rodada6_eficacias.md`; 1.000 reamostras pareadas das 548 imagens, semente 0).

| | mAP50 no VisDrone val | IC 95% |
|---|---|---|
| R (checkpoint escolhido no próprio val, época 58) | 0,6311 | 0,6149 a 0,6471 |
| R-sel (checkpoint escolhido em `sel_r`, época 55) | 0,6224 | 0,6069 a 0,6397 |
| Viés de seleção, R menos R-sel (pareado) | +0,0087 (1,4% relativos) | +0,0035 a +0,0136 |

Veredito pela regra: o intervalo exclui zero, viés real e pequeno. R-sel passa a ser o teto R do artigo e todas as eficácias sobem cerca de 1,4% relativos (a razão a R-sel é a razão a R vezes 1,014); nenhuma ordem entre modelos muda, porque o denominador é o mesmo para todos. Eficácias com R-sel (média das sementes), com a de R entre parênteses: S-nadir-150 2,2% (2,2%), S-oblique 8,9% (8,8%), S-oblique-six 15,5%, IC 14,6 a 16,7% (15,3%), S-nadir-150-six 3,1% (3,0%); ajuste fino a 5% nos cronogramas escolhidos, início sintético 72,8% (71,8%) e COCO 94,8% (93,4%); a 10%, 81,8% (80,7%) e 100,0% (98,6%). Tabela completa em `rodada6_eficacias.md`. Coincidência a registrar: o ajuste fino COCO a 10% com taxa 0,0002 (`ft10_coco_lr`) também dá 0,6224, igual a R-sel na quarta casa; são modelos diferentes.

Checagens de partida da mesma cadeia: P2, um quadro a 75 m com `--objetos-comprimento-arma`, 20 pessoas, 5 objetos com 0,83 a 1,03 m (todos na faixa das armas), pool MPFB de 6; P3, um quadro a 35 m com `--arma-na-mao`, 20 pessoas, 13 caixas, pool de 6.

## 2026-11-04 [DESKTOP] Itens 1, 2 e 4 de `O-QUE-FALTA-NO-SERVIDOR.md`: malhas de arma, sub-stride oblíquo, R com seleção fora do teste

Lista em `08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md` (feita no Mac em 04/11 a partir dos `[[NEW]]` da versão curta para a AIM 2027). Os itens 1 e 2 são só leitura; o 4 é um treino de R.

**Item 1, caixa envolvente das cinco malhas de arma** (`06-resultados/mede_armas.py`, roda dentro do Blender headless: `"C:\Program Files (x86)\Steam\steamapps\common\Blenderlender.exe" -b --python 06-resultados/mede_armas.py`; saídas `06-resultados/armas_malhas.json` e `armas_malhas.md`). Vértices da malha construída por `03-blender/scripts/objetos_alongados.py`, no referencial local da arma (+X cano, Y largura, Z altura); 12 sementes por malha deram a mesma caixa (o sorteio só escolhe material). Pixels = metros / GSD (4,88, 2,44 e 1,14 cm/px a 150, 75 e 35 m em 4K, `revisao-2026-10-17/gsd_zoom.md`). "Nominal" é o comprimento que a função devolve e que o manuscrito cita (4.2.2).

| Malha | Peso no sorteio | Nominal (m) | Comprimento (m) | Largura (m) | Altura (m) | 150 m, C × L (px) | 75 m (px) | 35 m (px) | Altura a 150 / 75 / 35 (px) |
|---|---|---|---|---|---|---|---|---|---|
| fuzil AK | 26 | 0,92 | 1,071 | 0,050 | 0,227 | 22,0 × 1,0 | 43,9 × 2,0 | 94,0 × 4,4 | 4,6 / 9,3 / 19,9 |
| fuzil AR | 24 | 0,94 | 1,070 | 0,050 | 0,263 | 21,9 × 1,0 | 43,9 × 2,0 | 93,9 × 4,4 | 5,4 / 10,8 / 23,0 |
| carabina | 20 | 0,62 | 0,610 | 0,045 | 0,215 | 12,5 × 0,9 | 25,0 × 1,8 | 53,5 × 3,9 | 4,4 / 8,8 / 18,9 |
| espingarda | 18 | 1,05 | 1,172 | 0,042 | 0,099 | 24,0 × 0,9 | 48,0 × 1,7 | 102,8 × 3,7 | 2,0 / 4,0 / 8,6 |
| pistola | 12 | 0,20 | 0,195 | 0,030 | 0,116 | 4,0 × 0,6 | 8,0 × 1,2 | 17,1 × 2,6 | 2,4 / 4,7 / 10,1 |

Média ponderada pelo peso de sorteio das cinco: comprimento 18,3 / 36,5 / 78,2 px e largura 0,91 / 1,81 / 3,96 px a 150 / 75 / 35 m. Leitura: (1) os dois fuzis medem 1,07 m de ponta a ponta, não 0,92 e 0,94 (coronha e carregador ficam fora do nominal), e a espingarda 1,17 m; os "19, 38 e 81 px para 0,92 m" derivados no `[[NEW]]` da 5.1 são limite inferior, o fuzil AK ocupa 22, 44 e 94 px; (2) a largura de toda arma de treino fica abaixo de um pixel a 150 m (0,6 a 1,0 px) e em torno de dois a 75 m: o que sobrevive à GSD é o comprimento, a forma transversal não existe no sensor, o que é a base numérica da frase "a forma se perde a 4,88 cm/px"; (3) a pistola, a 150 m, cabe em 4 × 0,6 px. São extensões da malha, não a projeção no quadro: a pegada no nadir depende do ângulo de porte (pousada, tiracolo, ombro). As duas armas inéditas (FAL 1,101 × 0,055 × 0,253 m; submetralhadora 0,560 × 0,050 × 0,247 m) e os nove objetos confundíveis estão nos mesmos arquivos; os objetos sorteiam o comprimento (cano de PVC 1,68 a 2,36 m, vergalhão 1,18 a 1,86 m), e a tabela traz mediana e faixa.

**Item 2, fração sub-stride dos corpora oblíquos** (`06-resultados/mede_alvo_split.py`, agora com `ds_morro_obl` e `ds_oblvar`; comando `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/mede_alvo_split.py`; saída `alvo_por_split.json`, chaves antigas inalteradas). Rótulos da imagem inteira em 4K, lado menor abaixo de 8 px (menor stride do YOLO11):

| Corpus | Caixas | Largura × altura medianas (px) | h/w | Lado menor < 8 px |
|---|---|---|---|---|
| S-oblique (`ds_morro_obl`), todos os 180 quadros | 1.912 | 17,93 × 26,39 | 1,464 | 0,94% (train 0,95; val 0,86) |
| S-oblique-six (`ds_oblvar`), todos os 180 quadros | 1.521 | 13,32 × 25,20 | 1,855 | 3,88% (train 4,00; val 3,06) |

As medianas e contagens batem com `forma_corpora.json` (as linhas oblíquas da Tabela 5 do artigo). Para a Tabela 5: 0,9% e 3,9%, contra 0,8% no corpus de registro e 30,5% no VisDrone val. S-oblique-six tem quatro vezes mais caixas sub-stride que S-oblique porque o pitch mais alto (45 a 56 graus) e os seis sítios estreitam a pessoa em planta (largura mediana 13,3 contra 17,9 px).

**Item 4, teto R com o checkpoint escolhido fora do teste** (em curso). `03-blender/scripts/r_sel.py`, lançado por `lanca_r_sel.cmd` em 04/11 às 11:28 (log `C:rma3-favelalender
_sel.log`). Mesma receita de `r_pareado` (`train_yolo_win.py --data C:/arma3-favela/visdrone/visdrone_sub/data_sel.yaml --model yolo11s.pt --imgsz 1280 --epochs 60 --batch 6 --workers 4 --name r_pareado_sel --single-cls`; `--dry-run --compara runs/detect/r_pareado/args.yaml` acusa só `data` e `name`), com `val` apontando para `C:/arma3-favela/visdrone/ft/sel_r.txt`. Achado ao montar a fatia: `ft/sel` (324 imagens do VisDrone train) tem 59 imagens em comum com `visdrone_sub/train` (as 1.106 de R, semente 21), porque os dois são sorteios independentes do mesmo train; `sel_r` são as 265 restantes (`ft/sel_r.json` lista as 59 removidas), fora do treino de R e fora do VisDrone val. Isso vale também como ressalva para os ajustes finos da rodada 3 e 5: a seleção deles em `sel` é disjunta do val (teste) e das fatias `ft05`/`ft10`, como sempre se disse, mas não da amostra de R (que esses runs não usam no treino, então não há vazamento, só a observação). Depois do treino a cadeia roda `avalia_sim2real.py` (VisDrone val, imgsz 1280, `sim2real_r_pareado_sel.json`) e `visdrone_preds.py --modelos r_pareado_sel` para o bootstrap. Resultado e eficácias recalculadas entram numa entrada própria quando terminar.

## 2026-10-22 [DESKTOP] Rodada 5 encerrada: fechamento (Y2 a Y4) e vereditos

Nota de 2026-10-27, acrescentada após a revisão de prova do manuscrito v5. O revisor encontrou três discrepâncias entre arquivos-fonte desta pasta, nenhuma delas no manuscrito: (1) o limiar que maximiza o F1 de armada é 0,40 em 7 dos 14 casos segundo `revisao-2026-10-17/limiar_armado.md`, e não em 8, como diz a frase "0,40 em 8 deles" na entrada da varredura de limiar mais abaixo nesta página; (2) o limite superior do intervalo do d′ do gêmeo a 75 m nos 80 quadros novos é 1,20 em `limiar_armado.md` e na Tabela gemeo do manuscrito, e aparece como 1,19 na linha da curva por GSD de outra entrada desta página; (3) a média de S-oblique-six sobre as três sementes de treino aparece como 0,0967 nas tabelas desta página (média dos valores já arredondados) e como 0,0966 no manuscrito (média calculada antes do arredondamento, como a legenda da tabela da curva de aprendizado declara). Em cada caso o manuscrito segue o arquivo primário: `limiar_armado.md` em (1) e (2), e o cálculo antes do arredondamento em (3). As entradas antigas abaixo ficam como estavam, por serem histórico.

A cadeia terminou em 22/10 às 11:05, sem grupo com falha além do P2 da primeira partida (Blender lançado pelo Explorer, sem MPFB; relançado pela sessão em 18/10 às 23:43). Pausa do autor de 21/10 23:38 a 22/10 01:41. Vereditos em `06-resultados/rodada5_criterios.json` (`06-resultados/rodada5_criterios.py --parte tudo`); leituras de resolubilidade em `06-resultados/revisao-2026-10-17/resolvivel_r5.md`; regra oficial do VisDrone e IoU em `06-resultados/visdrone_oficial_iou.json`.

- R5-1 (S): oblíquo acima de nadir nas três leituras, razão 4,08 (3,44 a 4,64); seis sítios contra um no oblíquo, três leituras; em nadir, (b) e (c).
- R5-5 (F): custo do pré-treino sintético robusto ao cronograma; nos cronogramas escolhidos, +30,2% a 5% (três leituras) e +22,2% a 10% (b).
- R5-6 (N): na HERIDAL, nadir acima do oblíquo, leituras (b) e (c); a ordem se inverte em relação ao VisDrone.
- R5-3 (A): número de quadros operante (152 contra 30, três leituras); fim da curva subindo dentro da dispersão de treino (152 contra 120, só (b), +6,9%).
- R5-4 (D): queda de participação no treino; a desvantagem do sol duro deixa de ser resolvível com sol duro bastante no treino.
- R5-7 (M): três classes a 150 m válidas; separação acima do acaso no sintético, mais fraca que a 75 m, tratada como atalho.
- R5-2 (C): seis sítios nas três cenas acima de S-oblique nas três sementes, três leituras (+68,7%).
- IoU 0,50, 0,60 e 0,75: ordem dos modelos novos estável nos três limiares.

## 2026-10-22 [DESKTOP] Rodada 5, grupo C (R5-2): semente de cena para S-oblique-six

Cadeia `03-blender/scripts/rodada5.py`, etapas C1 a C8 (plano 3.8). Duas réplicas do corpus oblíquo de seis sítios com sementes de cena 22 e 23 (a 21 é a do corpus original), 180 quadros cada, mesma receita e semente de treino 0; zero-shot em `06-resultados/sim2real_s_oblvar_e22.json` e `sim2real_s_oblvar_e23.json`. A réplica 23 foi pausada pelo autor em 21/10 às 23:38 e retomada em 22/10 às 01:41, do quadro 13 de 30 do sítio interrompido.

| Semente de cena (treino 0) | mAP50 no VisDrone |
|---|---|
| 21 (S-oblique-six original) | 0,1055 |
| 22 | 0,0935 |
| 23 | 0,0821 |

- Faixa sobre as três sementes de cena: 0,0821 a 0,1055 (amplitude 0,0234, média 0,0937); faixa sobre as três sementes de treino na cena 21: 0,0887 a 0,1055 (amplitude 0,0168). A dispersão de cena é 1,4 vez a de treino, abaixo do dobro fixado como "o cenário domina".
- C-ii, seis sítios nas três cenas contra S-oblique nas três sementes de treino (0,0501 a 0,0614): faixas não se cruzam, passa em (a); a leitura (b) sai no fechamento (Y3).
- A eficácia de S-oblique-six continua a da cena 21 (média de três treinos, 15,3%); com as três cenas, a média seria 14,8% (0,0937 / 0,6311), dada ao lado.

## 2026-10-21 [DESKTOP] Rodada 5, grupo M (R5-7): três classes a 150 m, agora válido

Cadeia `03-blender/scripts/rodada5.py`, etapas M1 a M4 (plano 3.7); M5 a M8 (corpus de 600 quadros) dispensadas pela regra, porque o modelo passou a validade. Gêmeo a 150 m do corpus de 35 m, 80 quadros novos (índices 200 a 279) renderizados com o mesmo gerador; treino `armado_150g_e120` (120 épocas, paciência 30; parou na 80). Confusão por `06-resultados/confusao_armado.py` no val (`confusao_armado_150g_e120.json`) e nos 80 quadros novos (`extra_armado_150g_e120.json`); critério por `rodada5_criterios.py` (item M, salvo em `06-resultados/rodada5_criterios_M.json`): conf 0,25, d′ com correção log-linear, 1.000 reamostras de quadros, semente 0.

- Validade (pelo menos metade das pessoas encontradas em qualquer classe, no val e nos novos): 0,606 (297 pessoas) e 0,663 (916). Válido; a rodada 4 tinha 0,498.
- 150 m, val (27 quadros): armada chamada de armada 0,435; objeto chamado de armada 0,178 (IC 0,107 a 0,247); d′ 0,75 (IC 0,33 a 1,26).
- 150 m, 80 quadros novos: armada 0,457; objeto chamado de armada 0,245 (IC 0,204 a 0,289); d′ 0,58 (IC 0,38 a 0,78).
- Curva nos 80 quadros novos (mesmos índices): 35 m d′ 0,77 (0,57 a 0,99), objeto 0,253; gêmeo a 75 m d′ 0,97 (0,77 a 1,19), objeto 0,125; gêmeo a 150 m d′ 0,58 (0,38 a 0,78), objeto 0,245.
- 150 contra 75 m: d′ -0,394 (IC -0,681 a -0,098), objeto chamado de armada +0,120 (IC 0,058 a 0,181); as duas passam em (b) e (c).
- Veredito pela regra fixada: o intervalo de d′ exclui zero, então há separação acima do acaso no sintético a 150 m; como a arma é argumentada irresolvível a essa distância (pessoa em planta de cerca de 10 px), a separação é tratada como atalho (comprimento, silhueta), não como capacidade. A 150 m a separação é a mais fraca das três distâncias e o falso alarme sobre objetos volta ao nível de 35 m.

## 2026-10-20 [DESKTOP] Rodada 5, grupo D (R5-4): ablação só com sol duro

Cadeia `03-blender/scripts/rodada5.py`, etapas D1 a D5 (plano 3.6). Corpus de 180 quadros nadir a 150 m só com sol duro (mesma semente de cena e sítio do corpus de registro), treino `s_soldur_4k` com a receita da 7.6. Avaliação por regime nos 120 quadros de teste (20 por regime) por `06-resultados/por_regime.py --por-quadro`, para o especialista (`06-resultados/por_regime_s_soldur_4k.json`) e para o generalista S-nadir-150 reavaliado (`06-resultados/por_regime_s_nadir_4k_r5.json`). Comparações do critério por `06-resultados/rodada5_grupo_d.py` (recall a conf 0,25 em imagem inteira, 2.000 reamostras de quadros, semente 0).

| Regime | mAP50 especialista (só sol duro) | mAP50 generalista (seis regimes) | recall especialista | recall generalista |
|---|---|---|---|---|
| sol duro | 0,7422 | 0,6750 | 0,739 | 0,657 |
| sol baixo | 0,7944 | 0,7903 | 0,776 | 0,814 |
| nublado | 0,7958 | 0,7906 | 0,759 | 0,796 |
| neblina | 0,6519 | 0,7796 | 0,569 | 0,726 |
| encoberto | 0,7536 | 0,7545 | 0,749 | 0,768 |
| chuva | 0,7276 | 0,7589 | 0,747 | 0,789 |

- D-i (pareada, os mesmos 20 quadros de sol duro): especialista menos generalista, recall +0,0818 (IC 0,0377 a 0,1243). Ver seis vezes mais sol duro no treino melhora a detecção sob sol duro.
- Nota de 22/10: `rodada5_criterios.json` traz intervalos um pouco diferentes para D-i (0,0383 a 0,1236) e D-ii (-0,1237 a +0,0085), de outra implementação da mesma reamostragem; o veredito é o mesmo, e o artigo usa os de `rodada5_grupo_d.py`.
- D-ii (a que decide): especialista sob sol duro menos generalista sob nublado, recall -0,0572 (IC -0,1252 a +0,0067). O intervalo inclui zero; o mAP50 do especialista sob sol duro (0,7422) fica abaixo do generalista sob nublado (0,7906), 6,5% relativos. Pela regra fixada, a leitura é "queda de participação no treino": a desvantagem do sol duro não se mostra intrínseca quando o treino vê o regime o bastante. A implicação da 6.3 passa de quando voar para com que luz treinar.
- Exploratório: zero-shot do especialista no VisDrone 0,0072 (o generalista faz 0,0102).

## 2026-10-20 [DESKTOP] Rodada 5, grupo A (R5-3): curva de aprendizado sobre o número de quadros

Cadeia `03-blender/scripts/rodada5.py`, etapas A1 a A10 (plano 3.5). Subconjuntos encaixados dos 152 quadros de treino de S-oblique-six, estratificados por sítio (`06-resultados/curva_subconjuntos.json`: 182, 341, 503 e 696 ladrilhos); mesma validação; 60 épocas; zero-shot em `06-resultados/sim2real_s_oblvar_c*.json`.

| Quadros de treino | mAP50 no VisDrone (sementes) | Média | Faixa |
|---|---|---|---|
| 30 | 0,0499, 0,0674, 0,0679 | 0,0617 | 0,0499 a 0,0679 |
| 60 | 0,0806 | 0,0806 | um treino |
| 90 | 0,0810 | 0,0810 | um treino |
| 120 | 0,0915, 0,0878, 0,0918 | 0,0904 | 0,0878 a 0,0918 |
| 152 (S-oblique-six) | 0,1055, 0,0958, 0,0887 | 0,0967 | 0,0887 a 0,1055 |

Leituras disponíveis agora (a de intervalo pareado sai no fechamento, Y3):
- Regra da antiga 10.1, 152 contra 30 quadros: faixas não se cruzam, passa em (a); +0,0349, 57% relativos. O número de quadros é operante, pendente de (b).
- Fim da curva, 152 contra 120: faixas se cruzam, não passa em (a); +0,0063, 7%. Pelo critério, "plano" ou "subindo dentro da dispersão de treino", conforme (b).
- Descritivo: mAP50 = 0,0202 ln(N) - 0,0060 nas médias; ganho previsto por duplicação 0,0140.
- Observação: s_oblvar_c120_sd1 parou por paciência na época 45, e a última época caiu a mAP50 de validação 0,163 (precisão 0,690, recall 0,163 no results.csv). O best.pt, que é o avaliado, vem de uma época anterior; o zero-shot dele (0,0878) fica um pouco abaixo das outras duas sementes (0,0915 e 0,0918), não dentro da faixa delas (correção de 22/10). O retrato do status mostra a última época, não a escolhida.

## 2026-10-19 [DESKTOP] Rodada 5, grupos F (R5-5), N (R5-6) e Y1: ajuste fino por cronograma, HERIDAL e critérios

Cadeia `03-blender/scripts/rodada5.py`, etapas F0 a F16, N1 a N3 e Y1 (plano `03-blender/PLANO-RODADA5.md`, 3.2 a 3.4). Vereditos em `06-resultados/rodada5_criterios.json` (`06-resultados/rodada5_criterios.py --parte prioridade`); escolha de cronograma em `06-resultados/rodada5_ft_selecao.json`; zero-shot em `06-resultados/sim2real_<run>.json`; reamostragem em `06-resultados/revisao-2026-10-17/bootstrap_visdrone_r5.md`, `resolvivel_r5.md`, `bootstrap_heridal.md` e `bootstrap_heridal_1280.md`.

**Grupo S, leituras de intervalo (Y1).** S-oblique menos S-nadir-150 na média de três sementes: +0,0419 (IC 0,0368 a 0,0470), razão 4,08 (3,44 a 4,64); passa em (a), (b) e (c). S-oblique-six contra S-oblique, três contra três: razão 1,74 (1,64 a 1,85), passa nas três. S-nadir-150-six contra S-nadir-150: razão 1,40 (1,07 a 1,50), passa em (b) e (c), não em (a). Eficácia na média: S-nadir-150 2,2% (1,9 a 2,5), S-oblique 8,8% (8,1 a 9,6).

**Grupo F (ajuste fino).** Reprodução de controle com otimizador explícito: ft05_coco_rep 0,5220 contra 0,5220 (tolerância 0,0035): reproduz. mAP50 no VisDrone val das doze células (original, extrator congelado, taxa 0,0002, os dois):

| Fatia, início | orig | fz | lr | fzlr |
|---|---|---|---|---|
| 5%, sintético | 0,4424 | 0,2808 | 0,3103 | 0,2028 |
| 5%, COCO | 0,5220 | 0,5467 | 0,5746 | 0,5410 |
| 10%, sintético | 0,5095 | 0,3209 | 0,3875 | 0,2241 |
| 10%, COCO | 0,5709 | 0,5772 | 0,6224 | 0,5644 |

Seleção no `sel` (mAP50-95), nunca no teste: o início sintético prefere o cronograma original nas duas fatias; o COCO prefere a taxa 0,0002 nas duas. Sementes 1 e 2 do ft05_coco_lr: 0,5963 e 0,5982. Comparação de interesse, cada início no cronograma que preferiu: a 5%, COCO 0,5897 (três sementes) contra sintético 0,4529 (três), +0,1369 (IC 0,1290 a 0,1465), 30,2% relativos, passa em (a), (b) e (c); a 10%, 0,6224 contra 0,5095, +0,1129 (IC 0,1044 a 0,1230), 22,2%, passa em (b). Veredito do critério: custo robusto ao cronograma. Congelar o extrator ou baixar a taxa piorou o início sintético em todas as células; no COCO, a taxa menor melhorou.

**Grupo N (HERIDAL, base real nadir, 40 a 65 m).** Zenodo 5662351 (CC BY 3.0), 1.647 imagens e 3.229 pessoas, todas as anotadas (`03-blender/scripts/prepara_heridal.py --divisao todas`, contagens em `06-resultados/heridal_contagens.json`); imgsz casado 1152 pela regra dos rótulos (`06-resultados/escala_nadir.py`, `06-resultados/escala_heridal.json`), 1280 como medida secundária. R (treinado no VisDrone) faz 0,3185: protocolo interpretável (limiar 0,05).

| Grupo | mAP50, imgsz 1152 (IC 95%) | parcela de R | mAP50, imgsz 1280 |
|---|---|---|---|
| R | 0,3185 (0,2843 a 0,3543) | 100% | 0,3353 |
| S-nadir-150, três sementes | 0,1997 (0,1713 a 0,2306) | 62,7% | 0,1682 |
| S-nadir-150-six | 0,2488 (0,2116 a 0,2865) | 78,1% | 0,2208 |
| S-oblique, três sementes | 0,1341 (0,1149 a 0,1555) | 42,1% | 0,1422 |
| S-oblique-six, três sementes | 0,1477 (0,1265 a 0,1715) | 46,4% | 0,1418 |
| Armado-150 (exploratório) | 0,1417 | 44,5% | 0,1272 |

Principal (oblíquo menos nadir, três contra três): -0,0656 (IC -0,0840 a -0,0471), razão 0,671 (0,61 a 0,74), passa em (b) e (c), não em (a) (faixas se cruzam). A 1280: -0,0260 (IC -0,0414 a -0,0097), passa em (b). Secundária (seis sítios, oblíquo menos nadir): -0,1012 (IC -0,1216 a -0,0786), passa em (b) e (c). A ordem é a mesma nos dois tamanhos: num benchmark real nadir, o corpus nadir transfere melhor que o oblíquo, o inverso do VisDrone (razão oblíquo/nadir 0,67 contra 4,08). Ressalva fixada no plano: a HERIDAL é mato e não cidade, e a GSD dela foi estimada.

## 2026-10-19 [DESKTOP] Rodada 5, grupo S (R5-1): sementes 1 e 2 de S-nadir-150 e S-oblique

Cadeia `03-blender/scripts/rodada5.py`, etapas S1 a S7 (plano `03-blender/PLANO-RODADA5.md`, 3.1, critério fixado antes). Treinos com a receita da 7.6, corpus fixo, só a semente de treino muda: `train_yolo_win.py` com `--seed 1` e `--seed 2`. Zero-shot no VisDrone val por `03-blender/scripts/avalia_sim2real.py --weights <run>/weights/best.pt --real <visdrone val> --imgsz 1280 --out 06-resultados/sim2real_<run>.json`; regra oficial em `06-resultados/visdrone_oficial_iou.json`; predições por imagem em `06-resultados/revisao-2026-10-17/preds_visdrone_<run>.npz` (não versionadas).

| Modelo | Semente 0 (já reportada) | Semente 1 | Semente 2 | Média | Faixa | Eficácia da média (R = 0,6311) |
|---|---|---|---|---|---|---|
| S-nadir-150 | 0,0102 | 0,0198 | 0,0108 | 0,0136 | 0,0102 a 0,0198 | 2,2% |
| S-oblique | 0,0614 | 0,0552 | 0,0501 | 0,0556 | 0,0501 a 0,0614 | 8,8% |

Regra oficial do VisDrone: 0,0203 e 0,0111 (nadir sd1, sd2), 0,0560 e 0,0508 (oblíquo sd1, sd2).

Leituras do critério (as de intervalo pareado saem no grupo Y1):
- S-oblique contra S-nadir-150: faixas não se cruzam, passa em (a); diferença das médias +0,0420, 309% relativos, passa em (c). Razão das médias 4,09; por semente 6,02, 2,79 e 4,64. O fator 6,0 do artigo é o da semente 0; com três sementes de cada lado o fator é cerca de 4.
- S-oblique-six (0,0887 a 0,1055) contra S-oblique (0,0501 a 0,0614): faixas não se cruzam, passa em (a).
- S-nadir-150-six (0,0190, um treino) contra S-nadir-150: o valor único cai dentro da faixa das três sementes (0,0102 a 0,0198), então a vantagem de seis sítios em nadir deixa de passar em (a).
- Validação sintética: nadir 0,794 e 0,810; oblíquo 0,764 e 0,736 (épocas 56, 60, 60 e 45).

## 2026-10-17 [DESKTOP] Revisão: intervalos por reamostragem, curvas PR e varredura de limiar (agente D2)

Fase 1 do `01-artigo/feedback-2026-10-14/PLANO-CORRECAO.md`, pontos S1 (intervalos de confiança), S6 (curvas precisão-recall e limiares justificados) e A3 (diferenças pequenas tratadas como resultado). Só inferência, nenhum treino nem render; nada de corpora `odm`, `cid150` ou derivados da PCERJ. Tudo em `06-resultados/revisao-2026-10-17/` (scripts, JSON, tabelas `.md`); figuras em `06-resultados/figuras/`. Todos os comandos rodaram de dentro dessa pasta com `PY` = `C:/arma3-favela/venv/Scripts/python.exe` (Ultralytics 8.4.148, PyTorch 2.14, RTX 2060).

### Arquivos e comandos

| Arquivo | Conteúdo | Comando |
|---|---|---|
| `visdrone_preds.py`, `preds_visdrone_<run>.npz` (17), `visdrone_reproducao.json` | validador do Ultralytics no VisDrone-DET val (548 imagens; classe única, imgsz 1280, conf 0,001, NMS IoU 0,7, max_det 300) guardando por imagem a bandeira de acerto de cada predição nos 10 limiares de IoU, a confiança e o número de caixas verdadeiras, para recalcular o mAP50 de qualquer subconjunto com `ap_per_class` | `PY visdrone_preds.py --todos --batch 4` |
| `checa_precisao_lote.py`, `checa_precisao_lote.json`, `visdrone_reproducao_fp16_lote4.json` | o que a precisão (FP16 contra FP32) e o lote (4 contra 16) mudam no mAP50 | `PY checa_precisao_lote.py --modelos ft10_coco` |
| `bootstrap_visdrone.py`, `bootstrap_visdrone.json`, `bootstrap_visdrone.md` | 1.000 reamostras das 548 imagens com reposição (numpy `default_rng(0)`), as mesmas para todos os modelos; mAP50, eficácia (mAP50 / mAP50 de R na mesma reamostra) e diferenças pareadas, com percentis 2,5 e 97,5, fração de reamostras positiva, diferença relativa (% do menor) e razão com intervalo | `PY bootstrap_visdrone.py` |
| `pr_visdrone.py`, `pr_visdrone.json`, `figuras/fig11_pr_visdrone.png` | curvas precisão-recall a IoU 0,50 (envelope do validador, 1.000 pontos de recall) para R, S-oblique-six (semente 0), F-generic 10% e F-synthetic 10%; P e R na confiança que maximiza o F1 (como o validador: F1 em 1.000 pontos de confiança, suavizado com filtro de caixa de 10%) e a conf 0,25 | `PY pr_visdrone.py` |
| `armado_preds.py`, `preds_armado_<run>_<val|novos>.json` (14) | inferência dos sete modelos de três classes em imagem 4K inteira (imgsz 3840) guardando todas as predições com conf >= 0,05 e as caixas verdadeiras de cada quadro, sem arredondar coordenadas | `PY armado_preds.py --todos` |
| `limiar_armado.py`, `limiar_armado.json`, `limiar_armado.md`, `figuras/fig12_limiar_armado.png` | varredura de limiar de 0,05 a 0,95 (passo 0,05) com o protocolo de `confusao_armado.py` (casamento 1:1 por IoU >= 0,50 sem classe): recall de armada, objeto e desarmada chamados de armada, precisão de armada, F1 de armada, d' com correção log-linear; três pontos por modelo e conjunto (conf 0,25, máximo F1 de armada, menor limiar com objeto <= 0,10); bootstrap de quadros (1.000, semente 0) das taxas a 0,25 e das diferenças 35 m menos gêmeo | `PY limiar_armado.py` |
| `resolvivel.py`, `resolvivel.json`, `resolvivel.md` | cada comparação de manchete sob três leituras: (a) faixas das sementes de treino não se cruzam, (b) intervalo de 95% da diferença pareada exclui zero, (c) diferença relativa >= 30% do menor | `PY resolvivel.py` |

Por que guardar a conf 0,05 e filtrar: a NMS (torchvision, gulosa e exata, por classe) só suprime uma caixa por outra de confiança maior da mesma classe, então o conjunto de caixas com conf >= t que sobrevive à NMS rodada a 0,05 é o mesmo que sobreviveria rodada a t; conferido quadro a quadro em `armado_35_sd1` (0 quadros diferentes em 35) e pela reprodução abaixo. O máximo de predições num quadro foi 67, longe do `max_det` 300.

### Checagem de reprodução

VisDrone, em FP32 e lote 4: os 17 modelos reproduzem o mAP50 reportado em `sim2real_<run>.json` com diferença máxima de 0,00005 (R 0,63111 contra 0,6311; S-oblique-six 0,10545 contra 0,1055; S-nadir-150 0,01021 contra 0,0102; `visdrone_reproducao.json`). O mAP50 recalculado dos dados guardados é idêntico ao do validador em todos. A primeira passagem, em FP16, desviou até 0,0045 nos modelos ajustados (`ft10_coco` 0,5664 contra 0,5709) e ficou registrada em `visdrone_reproducao_fp16_lote4.json`; `checa_precisao_lote.json` mostra que o lote não muda nada (0,57086 a 4 e a 16 em FP32) e que a diferença é só da precisão, por isso a rodada ficou em FP32 com lote 4. A equivalência entre o cálculo rápido por multiplicidade de imagem e o `ap_per_class` com as predições repetidas de fato deu diferença 0,0 em 12 casos conferidos.

Modelos de três classes: os 14 conjuntos (val próprio e quadros novos dos sete modelos) reproduzem a conf 0,25 as três taxas de `confusao_armado_*.json`, `extra_armado_*.json` e `holdout_armas_armado_75.json` com diferença 0,0000 e as mesmas contagens (`limiar_armado.md`, primeira tabela). Armadilha encontrada e corrigida: a primeira versão do armazenamento arredondava as coordenadas a 0,01 px e isso mudou um casamento na fronteira de IoU 0,50 em 3 dos 14 conjuntos (uma caixa em 119, 256 e 288); sem arredondar, a reprodução é exata. GPU e CPU dão as mesmas contagens.

### Resultados

VisDrone, mAP50 com intervalo de 95% (`bootstrap_visdrone.md`): R 0,6311 (0,6149 a 0,6471); S-nadir-150 0,0102 (0,0087 a 0,0133); S-nadir-150-six 0,0190 (0,0142 a 0,0211); S-oblique 0,0614 (0,0554 a 0,0673); S-oblique-six 0,1055 (0,0980 a 0,1148), sementes 1 e 2 0,0958 (0,0884 a 0,1048) e 0,0887 (0,0813 a 0,0968); F-synthetic 5% 0,4424 (0,4260 a 0,4587); F-generic 5% 0,5220 (0,5045 a 0,5403); F-synthetic 10% 0,5095 (0,4935 a 0,5264); F-generic 10% 0,5709 (0,5535 a 0,5883); F-joint 0,4607 (0,4444 a 0,4789) e 0,5428 (0,5259 a 0,5610). Eficácias: S-oblique-six 16,7% (15,7 a 18,1); S-oblique 9,7% (8,9 a 10,6); nadir 1,6% (1,4 a 2,1).

Diferenças pareadas (mesmas reamostras): S-oblique menos S-nadir-150 +0,0511 (+0,0447 a +0,0567), razão 6,0 com intervalo 4,6 a 7,0, positiva em 100% das reamostras; S-oblique-six menos S-oblique +0,0441 (+0,0383 a +0,0514) na semente 0, +0,0353 (+0,0305 a +0,0411) na média das três sementes (razão 1,58, 1,48 a 1,69; o 1,7 do texto é o da melhor semente); S-nadir-150-six menos S-nadir-150 +0,0088 (+0,0038 a +0,0102); F-generic menos F-synthetic +0,0716 (+0,0658 a +0,0780) na média das sementes a 5% (semente a semente +0,0796, +0,0620, +0,0731, todas com intervalo acima de zero) e +0,0614 (+0,0553 a +0,0679) a 10%; F-generic menos F-joint +0,0637 (+0,0562 a +0,0700) a 5% e +0,0281 (+0,0214 a +0,0346) a 10%; F-joint menos F-synthetic +0,0078 (+0,0025 a +0,0147) a 5% na média das sementes, mas por semente só a 0 exclui zero (+0,0183; sementes 1 e 2: -0,0001 e +0,0053 com intervalos que cruzam zero), e +0,0333 (+0,0276 a +0,0399) a 10%.

Curvas PR (`pr_visdrone.json`, figura 11): no ponto de máximo F1, R tem P 0,731 e R 0,573 a conf 0,30; F-generic 10% P 0,682 e R 0,516 a 0,32; F-synthetic 10% P 0,637 e R 0,458 a 0,30; S-oblique-six P 0,263 e R 0,172 a 0,22. As três curvas com dado real são paralelas em todo o recall; a curva zero-shot cai abaixo de 0,6 de precisão já a 1% de recall e termina em recall 0,39.

Varredura de limiar (`limiar_armado.md`, figura 12): a conf 0,25, objeto chamado de armada 0,237 (S-nadir-75, val), 0,273 (S-nadir-35, val) e 0,165 (gêmeo a 75 m, val); nos quadros novos 0,152, 0,253 e 0,125; recall de armada 0,547, 0,569 e 0,471 (val). O limiar que maximiza o F1 de armada fica entre 0,30 e 0,50 em todos os 14 casos (0,40 em 8 deles) e sobe a precisão de armada de 0,37 a 0,46 para 0,47 a 0,66 perdendo 1 a 8 pontos de recall. Trazer o objeto chamado de armada a 0,10 exige limiar de 0,55 a 0,70 no 35 m e no 75 m original, com recall de armada de 0,21 a 0,36; o gêmeo chega a 0,10 com limiar de 0,25 a 0,65. Em nenhum limiar de nenhum modelo o recall de armada passa de 0,65 nem o objeto chamado de armada fica abaixo de 0,09 com recall acima de 0,42: a curva é a mesma troca em todas as altitudes, o 35 m apenas corre por ela com mais alarme para o mesmo recall nos quadros novos. Intervalos de 95% por reamostragem de quadros a 0,25 (objeto chamado de armada): 35 m 0,204 a 0,303 e gêmeo 0,081 a 0,167 nos 80 quadros novos (semente 0); d' de armada contra objeto 0,77 (0,57 a 0,99) e 0,97 (0,77 a 1,20).

Resolvível (`resolvivel.md`): nadir contra oblíquo passa nas duas leituras avaliáveis (intervalo exclui zero; +501% relativo), mas não tem sementes dos dois lados (um treino cada), que é o ponto R5-1. Seis sítios contra um passa nas duas leituras avaliáveis no nadir (+87%) e no oblíquo (+58%; o valor do S-oblique fica fora da faixa das três sementes do six). Início genérico contra sintético a 5% passa em (a) e (b) e falha em (c): +15,8% relativo, abaixo de 30%; a 10% passa em (b) e falha em (c) (+12,1%). Genérico contra conjunto: +13,8% a 5% e +5,2% a 10%, só (b). Conjunto contra sintético: +1,7% a 5% (o conjunto cai dentro da faixa das sementes do sintético) e +6,5% a 10%, só (b). 35 m contra gêmeo a 75 m, objeto chamado de armada: nos 80 quadros novos passa nas três leituras (média das sementes 0,222 contra 0,134, +0,087, intervalo +0,045 a +0,136, +65%, faixas 0,202 a 0,253 contra 0,097 a 0,181); no val passa em (b) e (c) mas as faixas se cruzam (semente 2 do gêmeo 0,242). 35 m contra 75 m original: não resolvível em nenhuma leitura (+0,036, intervalo -0,059 a +0,124, +15%).

Leitura para o texto: as comparações de geometria (nadir contra oblíquo, um sítio contra seis) são grandes em termos relativos e sobrevivem à reamostragem de imagens, faltando só a repetição de treino; as comparações de ajuste fino são estáveis entre sementes e entre reamostras mas pequenas (5 a 16% relativo), então devem ser escritas como diferenças consistentes e modestas, não como fatores; e o efeito da altitude sobre o alarme com objeto se sustenta nos quadros novos, não na divisão de validação.

## 2026-10-17 [DESKTOP] Revisão: fatos dos corpora, GSD e seleção de checkpoint (agente D1)

Fase 1 do `01-artigo/feedback-2026-10-14/PLANO-CORRECAO.md` (pontos M2, M3, M4, S3, S7, S8 e seção 5). Nenhum render, nenhum treino: só leitura de rótulos, manifests, `args.yaml`, `results.csv`, `best.pt` e código. Nenhuma pasta `odm`, `cid150` ou derivada do ortomosaico da PCERJ foi lida. Saída em `06-resultados/revisao-2026-10-17/`:

| Arquivo | Conteúdo | Comando |
|---|---|---|
| `contagens.py`, `corpora.json`, `corpora.md` | 14 corpora procedurais (piloto, S-nadir-150, S-nadir-150-six, S-oblique, S-oblique-six, S-nadir-75, S-nadir-35, gêmeos a 75 e a 150 m, 80 quadros novos de cada, arma inédita, porte de arma, teste por regime): render, altitude e pitch realizados, GSD, quadros e ladrilhos por divisão, instâncias por classe nos quadros e nos ladrilhos, pessoas colocadas contra caixas retidas, quadros por regime e por sítio, render por quadro; VisDrone (train 6.471 imagens e 106.396 pessoas; val 548 e 13.969; R 1.106 e 18.858; ft05 324 e 5.883; ft10 647 e 11.091; sel 324 e 5.886), conferido no formato original (8.844 pedestrian + 5.125 people; 1.378 regiões ignoradas em 340 imagens) | `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/revisao-2026-10-17/contagens.py` |
| `gsd_zoom.md`, `gsd_zoom.json` | câmera do gerador (sensor 36 mm, 28,83 mm equivalente, FOV 63,96 graus; concorda com a 7.3 do manuscrito), tabela altitude × render → GSD e pegada (150 m: 187,3 × 105,4 m, 9,76 cm/px em 1080p e 4,88 em 4K; 75 m: 2,44; 35 m: 1,14), Zenmuse Z30 pelo manual da DJI (CMOS 1/2,8", 2,13 MP, 4,3 a 129 mm, 29 a 872 mm equivalente, FOV 63,7 a 2,3 graus, 1920 × 1080; https://dl.djicdn.com/downloads/Z30/20190906/Z30_User_Manual_EN.pdf): a 150 m a Z30 dá 9,71 cm/px em grande-angular e 0,31 a 30×; casar 2,44 cm/px pede 4,0× (pegada 47 × 26 m) e 1,14 cm/px pede 8,5× (22 × 12 m); o render 4K equivale a 2× | aritmética em Python, reproduzida no arquivo |
| `checkpoints.py`, `checkpoints.json`, `checkpoints.md` | 26 runs: pesos iniciais, dado, divisão de seleção, épocas pedidas e feitas, parada antecipada, época do `best.pt` (casada com `train_metrics` do próprio `best.pt`), métrica de seleção (mAP50-95, `DetMetrics.fitness` do Ultralytics 8.4.148, `w = [0, 0, 0, 1]`), tempo de treino. Achados: R (`r_pareado`) seleciona o checkpoint no próprio VisDrone val (época 58 de 60); `ft10_sint` e `ft10_coco` têm `best.pt` na época 29 (o registro de 26/09 citava as épocas 27 e 30 pelo mAP50, que não é o critério); 13 dos 26 runs pararam pela paciência; três runs foram retomados de `last.pt` após pausa (`armado_75g` após a 28; `armado_35_sd1` após 12, 21 e 51; `misto10` após a 18) | `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/revisao-2026-10-17/checkpoints.py` |
| `gerador-fatos.md` | Cycles com denoising, PNG sem perda nos quadros, um JPEG de qualidade 92 (4:4:4) só nos ladrilhos; nenhum ruído de sensor, borrão de movimento, profundidade de campo, obturador rolante ou aberração cromática simulados; `post_process.py` existe mas não foi aplicado a nenhum corpus do artigo; seis corpos MPFB por corpus (sexo, idade, biotipo, pele e cabelo sorteados pelo MPFB), 12 trajes, roupa recolorida por instância, 35 por cento dos homens sem camisa, escala 0,92 a 1,08, poses e pesos; `ds_morro_clima` e `ds_morro_4k` usaram a biblioteca de armas antiga de `people_mpfb.py` (três silhuetas de fuzil e pistola), os demais a de `objetos_alongados.py` (cinco armas de 0,20 a 1,05 m, duas inéditas, nove objetos de 0,88 a 2,5 m, paleta compartilhada, fixação no punho); os seis regimes com elevação, disco solar, exposição e névoa; o experimento de luz (contraste do piloto em `contraste_clima.csv`; teste por regime de um só modelo, `s_nadir_4k`, em 120 quadros novos do mesmo sítio) e o que ele não é | leitura de código, com linha |
| `custo-rodada5.md` | R5-1 14 h; R5-2 26 a 39 h; R5-3 6 a 16 h (subconjuntos) ou 16 a 31 h (corpus estendido); R5-4 16 a 31 h; R5-5 7 a 20 h; R5-6 1 a 2 h de GPU mais download; R5-7 22 a 27 h, com teste prévio de 5 h; total 92 a 164 h; a recomendação A6 (R5-1, R5-5, R5-6) custa 22 a 36 h | derivado dos tempos de `corpora.md` e `checkpoints.md` |

Números que mudam ou qualificam o texto: (1) R foi selecionado no conjunto de teste; (2) os modelos de três classes têm matriz de confusão no mesmo val da seleção, e só os 80 quadros novos, os 50 de arma inédita e o porte são teste independente; (3) os renders não têm ruído, borrão nem compressão com perda nos quadros; (4) a GSD de 35 m corresponde a 8,5× de zoom da Z30 a 150 m, com pegada 73 vezes menor; (5) o teste por regime mede um modelo treinado nos seis regimes, em sintético, não uma ablação; (6) nos dois corpora mais antigos a arma vinha de outra biblioteca. Não apurado: amostras do Cycles do piloto (comando não registrado); extensão real das malhas das armas contra o comprimento registrado; se o pool do MPFB produz corpos infantis.

## 2026-10-17 [DESKTOP] Revisão: similaridade de recortes por altitude (agente D3)

Resposta ao áudio do revisor de 14/10 (itens A2 e S4 de `01-artigo/feedback-2026-10-14/PLANO-CORRECAO.md`: "matriz de co-similaridade ou redução de ordem" antes do detector de três classes). Análise sem detector e sem treino sobre os recortes anotados dos corpora de três classes: caixa com margem de 25% por lado, cortada no quadro, encaixada em 224 px (bilinear, cinza 114), passada pelo tronco congelado do YOLO11s do COCO (`C:/arma3-favela/blender/yolo11s.pt`, camadas 0 a 10; vetor = média espacial da camada 10, 512-d; camadas 4 e 6 como checagem). Pool de avaliação = val mais quadros novos: 35 m (`ds_armado_35` + `_extra`) 1.330 recortes; gêmeo 75 m (`ds_armado_75g` + `_extra`) 1.105; gêmeo 150 m (`ds_armado_150g`) 297; 75 m original (`ds_armado_75`) 405; a divisão de treino só como referência (protocolo `ref_para_eval`). Tipo do objeto por caixa lido do campo `caixas` do manifesto ou reconstruído de `tipos` pela regra do gerador (conferida em 560 quadros, bate em todos). Texto: `revisao-2026-10-17/similaridade.md`; números: `revisao-2026-10-17/similaridade.json`; script: `revisao-2026-10-17/similaridade.py`; figura: `figuras/fig13_similaridade.png` (PCA 2-D e matrizes de co-similaridade, 35 m, gêmeo 75 m, gêmeo 150 m); vetores fora do git em `C:/arma3-favela/blender/similaridade/`. Classificadores, PCA, LDA, silhueta e AUC em numpy (sem scikit-learn no venv; nada instalado nem baixado).

```
cd 06-resultados/revisao-2026-10-17
PY similaridade.py --etapa extrair --device cpu --threads 6
PY similaridade.py --etapa analisar
PY similaridade.py --etapa treinado --device cpu --threads 6
PY similaridade.py --etapa figura
```

Camada P5, validação cruzada de 5 dobras estratificada por classe no pool de avaliação (`cv_eval`), centroide mais próximo; IC 95% por reamostragem de quadros:

| medida | 35 m | gêmeo 75 m | gêmeo 150 m | 75 m original |
|---|---|---|---|---|
| silhueta das 3 classes (cosseno, centralizado) | 0,002 | 0,007 | 0,002 | 0,006 |
| maior entrada da co-similaridade centralizada (sem centralizar, tudo entre 0,71 e 0,79) | 0,025 | 0,026 | 0,032 | 0,020 |
| acurácia em 3 classes (acaso 0,33) | 0,507 | 0,531 | 0,492 | 0,558 |
| objeto chamado de armada | 0,332 (0,285 a 0,375) | 0,253 (0,207 a 0,297) | 0,208 (0,131 a 0,287) | 0,267 (0,187 a 0,360) |
| recall de armada | 0,420 | 0,377 | 0,359 | 0,436 |
| AUC armada contra objeto (similaridade ao centroide de armada) | 0,525 (0,483 a 0,561) | 0,576 (0,531 a 0,622) | 0,654 (0,574 a 0,730) | 0,534 (0,459 a 0,615) |
| d' armada contra objeto; detector no val entre parênteses | 0,23 (0,78) | 0,35 (0,90) | 0,45 (0,67) | 0,46 (0,83) |
| acurácia com PCA 2 / PCA 10 / LDA 2 | 0,384 / 0,495 / 0,547 | 0,399 / 0,525 / 0,586 | 0,428 / 0,471 / 0,502 | 0,348 / 0,526 / 0,514 |

Comparação com o detector (objeto chamado de armada; similaridade = centroide ajustado na divisão de treino, `ref_para_eval`): 35 m val 0,331 contra 0,273 do detector; 35 m quadros novos 0,288 contra 0,253; gêmeo val 0,231 contra 0,165; gêmeo quadros novos 0,292 contra 0,125; com recall de armada 0,39 a 0,50 contra 0,43 a 0,57 do detector. Concordância por figura com objeto entre o critério por similaridade e o detector: phi 0,40 (35 m val), 0,22 (35 m novos), 0,11 e 0,13 (gêmeo). Suplemento com o tronco do detector treinado em cada corpus (`runs/detect/armado_*/weights/best.pt`, mesmo vetor médio): AUC 0,547, 0,502, 0,574 e 0,494; não separa melhor, e o espaço médio é quase degenerado (2 componentes explicam 73 a 89% da variância).

Leitura: a co-similaridade das características genéricas é plana (o único eixo opõe desarmada a quem carrega algo; armada e objeto não se separam em nenhuma altitude), o classificador por similaridade tem metade do d' do detector, a redução de ordem não cria separação (PCA 2 piora, PCA 10 iguala o espaço inteiro, LDA 2 é o melhor sem detector), e descer a 35 m não ajuda (AUC 0,53 a 35 m contra 0,58 a 75 m), no mesmo sentido do resultado negativo do detector a 35 m. Entra em 5.1 (um parágrafo e a figura 13) e em 6.1/6.5 como resposta ao ponto A2; o caminho "detectar, depois classificar por similaridade" (6.6) fica condicionado a características locais, não testadas.

## 2026-09-23 [DESKTOP] Teste de dose de variedade (Frente B, dois pontos)

Mesmo N (180 imagens 4K), mesma receita de treino (yolo11s, 1280, 60 epocas, batch 6, single_cls), mesmo gerador com `--mistura 0.5 0.5 0 --enquadro quadrado` para so diferir do controle no sitio. Braco: 6 sitios x 30 imagens (`ds_variedade`, sitios -1, 0, 1, 2, 3, 4 de `sitios.py`). Avaliacao zero-shot no VisDrone val (`avalia_sim2real.py`, conf 0,001, imgsz 1280).

| | 1 sitio (`s_nadir_4k`) | 6 sitios (`s_variedade`) |
|---|---|---|
| mAP50 VisDrone | 0,0102 | 0,0190 |
| mAP50-95 VisDrone | 0,0025 | 0,0071 |
| P / R VisDrone | 0,086 / 0,042 | 0,092 / 0,058 |
| mAP50 sintetico (teto, val proprio) | 0,7915 | 0,6786 |
| razao de eficacia vs R pareado (0,6311) | 1,6% | 3,0% |

Arquivos: `sim2real_s_nadir_4k.json`, `sim2real_s_variedade.json`; logs em `C:\arma3-favela\blender\fila_*.log` a `23_*.log`. Leitura: variedade de sitio move o numero na direcao prevista (Liao 2026, Kiefer 2022), quase dobrando o mAP50 e quase triplicando o mAP50-95, e o teto sintetico cai de 0,79 para 0,68 (o modelo deixa de decorar uma cena). O patamar continua uma ordem de grandeza abaixo de Kiefer (10 a 23%): sitio nao e o unico gargalo. Proximo: braco obliquo em 4K (geometria) e, se justificar, Frente B em escala.

## 2026-09-24 [DESKTOP] Armado a 35 m (segundo ponto de GSD), resultado NEGATIVO

Corpus `ds_armado_35`: 200 imagens 4K a 35 m (1,1 cm/px), 2.223 caixas (777 armada, 706 desarmada, 740 objeto), `--porte-realista --fio-gsd --laje 0.75 --amostra-no-quadro`, 64 samples. Treino `armado_35`: mesma receita do `armado_75` (yolo11s, 1280, 60 epocas, batch 6, 3 classes). Matriz de confusao por casamento IoU >= 0,5 no val proprio, conf 0,25 (script no log da sessao de 24/09; `runs/detect/armado_35`):

| real | chamado de armada | de desarmada | de objeto | perdida | n |
|---|---|---|---|---|---|
| armada, 75 m | 0,53 | 0,10 | 0,16 | 0,20 | 193 |
| armada, 35 m | 0,69 | 0,05 | 0,07 | 0,18 | 219 |
| desarmada, 75 m | 0,15 | 0,48 | 0,07 | 0,29 | 260 |
| desarmada, 35 m | 0,18 | 0,45 | 0,02 | 0,35 | 193 |
| objeto, 75 m | 0,25 | 0,07 | 0,46 | 0,23 | 215 |
| objeto, 35 m | **0,31** | 0,04 | 0,37 | 0,28 | 186 |

mAP50 no val proprio: 0,546 (75 m) contra 0,489 (35 m). A hipotese "a 1 cm/px a arma vira arma e a confusao cai" NAO se confirmou neste corpus: o recall de armada subiu (0,53 -> 0,69), mas objeto chamado de arma subiu junto (0,25 -> 0,31) e desarmada chamada de arma tambem (0,15 -> 0,18). O modelo a 35 m esta enviesado para "armada".

Leituras possiveis, a testar antes de escrever qualquer conclusao: (a) o corpus a 35 m muda GSD e pose ao mesmo tempo (`--porte-realista` tirou do objeto a pose de tiro, que a 75 m era um atalho para separar as classes; sem o atalho, a tarefa ficou mais dificil, nao mais facil); (b) 64 samples contra 96; (c) 1.166 ladrilhos de treino contra 1.331, com menos instancias por ladrilho; (d) a 35 m com nadir a perspectiva nas bordas do quadro inclina a pessoa. Para isolar (a), falta o 75 m com `--porte-realista` (1,5 h de render); para (b), o 35 m a 96 samples. Nenhum dos dois esta na fila.

## 2026-09-24 [DESKTOP] Braco obliquo em 4K (geometria de captura): 6x no VisDrone

Corpus `ds_morro_obl`: 180 imagens 4K a 120 m com camera inclinada 26 a 52 graus (preset `--obliqua`, GSD 3,9 cm/px), mesma cena e semente do nadir (21), 2 classes, `--mistura 0.5 0.5 0`. 1.912 caixas; forma do alvo h/w mediana 1,46 (nadir 0,98; VisDrone treino 1,95: o preset moveu a forma, mas nao ate o alvo). 968 ladrilhos de treino. Treino `s_obliquo` com a mesma receita do nadir (yolo11s, 1280, 60 epocas, single_cls); avaliacao `sim2real_s_obliquo.json`.

| modelo | mAP50 VisDrone | mAP50-95 | P / R | teto sintetico | eficacia vs R pareado (0,6311) |
|---|---|---|---|---|---|
| S-nadir-150 (1 sitio) | 0,0102 | 0,0025 | 0,086 / 0,042 | 0,79 | 1,6% |
| S-variedade (6 sitios, nadir) | 0,0190 | 0,0071 | 0,092 / 0,058 | 0,68 | 3,0% |
| **S-obliquo (1 sitio, inclinada)** | **0,0614** | **0,0192** | 0,203 / 0,106 | 0,75 | **9,7%** |

Leitura: a geometria de captura e o fator dominante do gap medido no VisDrone, seis vezes o nadir com a mesma cena, contra duas vezes com seis sitios. A eficacia de 9,7% entra na faixa de Kiefer, Ott e Zell 2022 (1,2 a 10,2 mAP50 em sintetico puro). Ressalvas: (1) o VisDrone e obliquo, entao este resultado mede aderencia ao benchmark, nao ao alvo operacional (nadir a 150 m), e a 11.2 do artigo precisa dizer isso; (2) h/w 1,46 ainda esta abaixo de 1,95, o que sugere que ha margem com pitch maior; (3) sitio e geometria ainda nao foram combinados (6 sitios obliquos e a proxima rodada obvia, ~10 h de render).

## 2026-09-25 [DESKTOP] Rodada 3, grupo A: corpus obliquo combinado pronto (A1, A2)

`ds_oblvar`: 180 imagens 4K em 6 sitios (-1 a 4, 30 cada), camera inclinada 45 a 56 graus com `--camera-livre`, so pessoas sem arma (`--mistura 0 1 0`), 96 samples, semente 21. Render em 277 min de maquina (com a queda do PC e a pausa no meio). 1.521 caixas, 8,5 por imagem. Forma do alvo (`06-resultados/forma_corpora.json`, `mede_forma.py`): **h/w mediana 1,85** (alvo de calibracao 1,95, treino do VisDrone), largura 13,3 px e altura 25,2 px contra 13,0 e 24,0 do VisDrone treino, area 324 contra 300 px2. Por pitch: 1,81 (45-50), 1,92 (50-55), 1,99 (55-56). O corpus obliquo anterior tinha 1,46 e 456 px2. Ladrilhos: 890 de treino, 144 de validacao (28 imagens). Treino `s_oblvar` em curso.


## 2026-09-25 [DESKTOP] Rodada 3, grupo A: S-oblique-six no VisDrone (A3, A4)

Treino `s_oblvar` (yolo11s, 1280, batch 6, single_cls, receita de todos os bracos): parada antecipada na epoca 46, melhor peso na 31, 153 min. Avaliacao `06-resultados/sim2real_s_oblvar.json` (`avalia_sim2real.py`, conf 0,001, imgsz 1280):

| | P | R | mAP50 | mAP50-95 |
|---|---|---|---|---|
| sintetico (validacao propria) | 0,7648 | 0,6540 | 0,7047 | 0,3453 |
| **VisDrone val, zero-shot** | 0,2631 | 0,1716 | **0,1055** | 0,0329 |

Eficacia contra o R pareado (0,6311): **16,7%**. Serie completa no VisDrone: nadir um sitio 0,0102 (1,6%); nadir seis sitios 0,0190 (3,0%); obliquo um sitio 0,0614 (9,7%); obliquo seis sitios calibrado 0,1055 (16,7%). O combinado rende 10,3 vezes o nadir e 1,7 vez o obliquo de um sitio. Em mAP50 absoluto (10,5 pontos: o valor bruto fica entre 0,10545 e 0,1055, pelo log da etapa A4) fica logo acima da faixa sintetica de Kiefer, Ott e Zell 2022 (1,2 a 10,2), que mede 10 classes contra a nossa uma. [Corrigido em 26/09 na rodada 1 da validacao; antes dizia 10,6 e topo da faixa.] Nao e ablacao: mudam juntos sitios, pitch, figuras sem arma e camera livre de mata.

## 2026-09-25 [DESKTOP] Rodada 3, grupo B: teste de arma inedita (B1, B2)

Corpus `ds_armado_75_inedita`: 50 quadros 4K a 75 m com o comando que gerou `ds_armado_75` (96 samples, 14 a 30 pessoas, `--mistura 0.34 0.33 0.33`, `--climas todos`), semente nova (47) e `--armas mista_inedita`: metade das armas sai dos cinco modelos de treino (fuzil AK, fuzil AR, carabina, espingarda, pistola) e metade de dois modelos que nunca entraram em treino (FAL 1,10 m, submetralhadora 0,55 m), com o tipo de cada caixa no manifest. Modelo `armado_75` sem retreino, protocolo de imagem inteira: `confusao_armado.py --pesos runs/detect/armado_75/weights/best.pt --ds ds_armado_75_inedita --split todos --out holdout_armas_armado_75.json` (imgsz 3840, conf 0,25, casamento 1:1 com IoU >= 0,5). Criterio aplicado por `python holdout_criterio.py` (saida `holdout_armas_criterio.json`).

| grupo | chamadas de armada / caixas | recall | IC 95% (Wilson) |
|---|---|---|---|
| cinco modelos de treino | 50 / 125 | 0,400 | 0,318 a 0,488 |
| dois modelos ineditos | 61 / 131 | 0,466 | 0,382 a 0,551 |

Razao ineditos/vistos **1,16** (IC 95% de Katz 0,88 a 1,54, que ignora o agrupamento das caixas por quadro). Criterio pre-declarado: retirar a afirmacao se a razao ficar abaixo de 0,8. **Afirmacao mantida**: o detector nao depende de ter visto o modelo especifico de arma.

Chamada de armada por modelo: fuzil AK 0,52; FAL (inedito) 0,50; espingarda 0,47; carabina 0,46; submetralhadora (inedita) 0,43; fuzil AR 0,34; pistola 0,20. Objetos: guarda-chuva 0,38; vergalhao 0,17; mangueira 0,17; enxada 0,16; tapete 0,13; cano PVC 0,11; rodo 0,10; vassoura 0,10; tabua 0,07.

Leitura: o reconhecimento acompanha comprimento e silhueta, nao o modelo. O FAL inedito fica junto das armas longas vistas (0,34 a 0,52); as armas curtas ficam abaixo e sao chamadas de desarmada com frequencia (pistola 45%, submetralhadora 32%); o guarda-chuva e chamado de arma quase tanto quanto o fuzil AR. A mesma generalizacao que faz o teste passar explica a confusao com objetos alongados. Ressalva: neste teste todas as taxas de chamada de armada ficam abaixo das do val do `armado_75` (`confusao_armado_75.json`, 27 imagens): armada 0,434 contra 0,547, desarmada 0,068 contra 0,131, objeto 0,152 contra 0,237. A causa nao foi isolada (semente e quadros novos, mesmo comando); a comparacao entre vistas e ineditas e feita nas mesmas imagens e nao e afetada.

## 2026-09-26 [DESKTOP] Rodada 3, grupo C: corpus gemeo a 75 m pronto (C1, C2)

Corpus `ds_armado_75g`: 200 quadros 4K com o comando que gerou `ds_armado_35` (64 samples, 12 a 24 pessoas, `--mistura 0.34 0.33 0.33`, `--porte-realista --fio-gsd --laje 0.75 --amostra-no-quadro`, `--climas todos`), mudando so a altura: `--alt 75 --alt-jitter 6` (argumentos `GEMEO75` de `03-blender/scripts/rodada3.py`). Render medio 124 s por quadro. 2.257 caixas (735 armada, 730 desarmada, 792 objeto), contra 2.223 do `ds_armado_35` (777, 706, 740).

Forma (`python mede_forma.py`, `forma_corpora.json`): pessoa armada com mediana 48,1 x 42,7 px, igual a `ds_armado_75` (48,1 x 42,5) e cerca de 2,5 vezes menor em cada lado que `ds_armado_35` (122,3 x 107,7); h/w de todas as caixas 0,87 (75 m original 0,88; 35 m 0,84). Ladrilhos (`tile_dataset.py --tile 1280 --overlap 0.2`): 1.287 de treino e 176 de validacao (24 quadros), contra 1.166 e 242 do 35 m.

Para que serve: na rodada 2 os corpora de 75 m e 35 m mudavam altitude e pose juntas (o de 75 m e anterior ao `--porte-realista`, com o objeto em pose de tiro em 42% dos casos; o de 35 m tem 8%). O gemeo muda so a altitude. Treino `armado_75g` (C3) em curso; a matriz de confusao (C4) decide se a diferenca entre 35 m e 75 m vem da resolucao ou da pose.

## 2026-09-26 [DESKTOP] Rodada 3, grupo C: gemeo a 75 m (C3, C4) e fatias do VisDrone (D1)

Treino `armado_75g` (yolo11s, 1280, batch 6, 3 classes, receita do `armado_75` e do `armado_35`), com pausa do autor na epoca 28 e retomada de `last.pt`: parada antecipada na epoca 59 (paciencia 15), melhor peso na 44, mAP50 0,473 no val de ladrilhos. Matriz de confusao de imagem inteira no val do gemeo, 24 imagens (`confusao_armado.py --pesos runs/detect/armado_75g/weights/best.pt --ds ds_armado_75g --split val --out confusao_armado_75g.json`), comparada com os outros dois modelos por `python compara_gemeo.py` (saida `gemeo_75_35.json`):

| fracao chamada de armada | 75 m original | 35 m | gemeo 75 m |
|---|---|---|---|
| pessoa armada (recall) | 0,547 (n 117) | 0,569 (137) | 0,471 (85) |
| pessoa desarmada | 0,131 (153) | 0,168 (119) | 0,109 (92) |
| pessoa com objeto | 0,237 (135) | 0,273 (121) | 0,165 (91) |
| d' armada contra objeto | 0,83 | 0,78 | 0,90 |
| d' armada contra desarmada | 1,24 | 1,14 | 1,16 |
| mAP50 imagem inteira | 0,579 | 0,514 | 0,508 |

Contraste de altitude (gemeo -> 35 m, so a altura muda): objeto +10,8 pontos (z 1,86, p 0,063), desarmada +5,9 (p 0,22), armada +9,9 (p 0,15). Contraste do gerador a 75 m (original -> gemeo: `--porte-realista --fio-gsd --laje 0.75 --amostra-no-quadro`, 64 samples, 12 a 24 pessoas): objeto -7,2 pontos (p 0,19), desarmada -2,2 (p 0,61), armada -7,6 (p 0,28). Testes de duas proporcoes sem correcao para o agrupamento por quadro.

Leitura: com tudo igual menos a altitude, descer a 35 m nao reduz a confusao entre arma e objeto; o modelo de 35 m chama mais gente de armada em todas as classes (mais acerto e mais alarme falso), com mAP50 igual e d' igual ou menor. A leitura (a) da entrada de 24/09 (o 35 m piorou porque perdeu o atalho da pose) nao se sustenta: a 75 m, as mudancas do gerador baixaram a confusao em vez de subir. O negativo de 35 m e da altitude, com a ressalva de que nenhum contraste passa de p 0,05 com vals de 24 a 35 imagens. Por tipo, o guarda-chuva segue como o objeto mais chamado de arma (0,40 no gemeo; 0,38 no teste de arma inedita).

D1 (`prepara_ft.py`, `C:\arma3-favela\visdrone\ft\fatias.json`): do treino do VisDrone (6.471 imagens), 324 para a fatia de 5% e 647 para a de 10% (a de 5% contida na de 10%), mais 324 de selecao disjuntas, semente 2609; o teste e o val inteiro do VisDrone.

## 2026-09-26 [DESKTOP] Rodada 3, grupo D: ajuste fino 5% a partir do sintetico (D2)

`ft05_sint` (etapa D2 de `03-blender/scripts/rodada3.py`): pesos `s_oblvar` (S-oblique-six) ajustados na fatia de 5% do VisDrone (324 imagens de treino), 30 epocas, yolo11s, 1280, batch 6, single_cls, selecao na fatia `sel` (324 imagens disjuntas). mAP50 na selecao (`runs/detect/ft05_sint/results.csv`): 0,159 na epoca 1, 0,251 na 5, 0,320 na 10, 0,378 na 20 e **0,396 na 30** (melhor, ainda subindo); mAP50-95 0,148. E numero de selecao, nao de teste: o teste no val inteiro do VisDrone e a etapa D6 (`ft_visdrone.json`). A comparacao com o braco COCO (D3) entra junto com ele.

## 2026-09-26 [DESKTOP] Rodada 3, grupo D: ajuste fino 5% a partir do COCO (D3)

`ft05_coco` (etapa D3 de `03-blender/scripts/rodada3.py`): `yolo11s.pt` (COCO) ajustado na mesma fatia de 5% do VisDrone (324 imagens), com a receita do D2 (30 epocas, 1280, batch 6, single_cls, selecao em `sel`). mAP50 na selecao (`runs/detect/ft05_sint/results.csv` e `runs/detect/ft05_coco/results.csv`):

| inicio | epoca 1 | 3 | 4 | 10 | 20 | melhor (epoca) | mAP50-95 no melhor |
|---|---|---|---|---|---|---|---|
| sintetico (`s_oblvar`, D2) | 0,159 | 0,226 | 0,244 | 0,320 | 0,378 | 0,396 (30) | 0,148 |
| COCO (D3) | 0,034 | 0,168 | 0,306 | 0,336 | 0,430 | 0,465 (29) | 0,180 |

Leitura provisoria (selecao, nao teste): com 5% do VisDrone o inicio sintetico so fica na frente nas tres primeiras epocas; o COCO passa na quarta e termina 6,8 pontos de mAP50 acima (3,2 de mAP50-95). O numero do artigo e o do teste no val inteiro do VisDrone (D6, `ft_visdrone.json`).

## 2026-09-26 [DESKTOP] Rodada 3, grupo D: ajuste fino 10% a partir do sintetico (D4)

`ft10_sint` (etapa D4 de `03-blender/scripts/rodada3.py`): pesos `s_oblvar` ajustados na fatia de 10% do VisDrone (647 imagens, contem a de 5%), receita do D2. mAP50 na selecao (`runs/detect/ft10_sint/results.csv`): 0,180 na epoca 1, 0,383 na 10, 0,426 na 20 e **0,449 na 27** (melhor); mAP50-95 0,171. Leitura provisoria (selecao, nao teste): dobrar o dado real sobe o inicio sintetico de 0,396 para 0,449, ainda abaixo do inicio COCO com metade do dado (0,465 com 5%).

## 2026-09-26 [DESKTOP] Rodada 3, grupo D: ajuste fino no VisDrone, teste (D5, D6); rodada encerrada

`ft10_coco` (D5): `yolo11s.pt` ajustado na fatia de 10% (647 imagens) com a receita do D2; melhor mAP50 na selecao 0,507 (epoca 30). D6 (`ft_resumo` de `03-blender/scripts/rodada3.py`): os quatro melhores pesos avaliados no val inteiro do VisDrone com o protocolo do R pareado (`avalia_sim2real.py`, conf 0,001, imgsz 1280). Resumo em `ft_visdrone.json`, metricas completas em `sim2real_ft05_sint.json`, `sim2real_ft05_coco.json`, `sim2real_ft10_sint.json`, `sim2real_ft10_coco.json`; curvas de selecao em `ft_curvas_selecao.json` (`python ft_curvas.py`).

| dado real | inicio | P | R | mAP50 | mAP50-95 | eficacia vs R pareado (0,6311) |
|---|---|---|---|---|---|---|
| 5% (324) | sintetico (`s_oblvar`) | 0,5869 | 0,4068 | 0,4424 | 0,1657 | 70,1% |
| 5% (324) | COCO | 0,6410 | 0,4718 | 0,5220 | 0,2025 | 82,7% |
| 10% (647) | sintetico (`s_oblvar`) | 0,6372 | 0,4579 | 0,5095 | 0,1984 | 80,7% |
| 10% (647) | COCO | 0,6823 | 0,5160 | 0,5709 | 0,2216 | 90,5% |

Diferenca sintetico menos COCO: -0,0796 com 5% e -0,0614 com 10% de mAP50 (-0,0368 e -0,0232 de mAP50-95). Leitura: o pre-treino sintetico custa em vez de ajudar, nas duas fracoes, e o sintetico com 647 imagens reais nao alcanca o COCO com 324. A expectativa declarada antes da rodada (o valor do pre-treino sintetico e maior no volume menor) falhou: a diferenca e mais negativa no volume menor, e o que encolhe com mais dado real e um custo. [Corrigido em 26/09 na rodada 3 da validacao; antes dizia 'como declarado antes da rodada'.] O ajuste fino transforma o proprio modelo sintetico (0,1055 para 0,4424 com 324 imagens), que e o efeito da literatura; o que ele nao faz aqui e superar um inicio generico com o mesmo dado. Hipotese nao testada: 46 epocas em 890 ladrilhos sinteticos sobrescrevem parte do que o COCO codifica sobre pessoas reais. Na selecao, o inicio COCO passa o sintetico na epoca 4 com 5% e ja na 1 com 10%.

Rodada 3 encerrada em 26/09 17:54, sem grupo com falha. Todos os `[X]` da rodada preenchidos no manuscrito (9.3, 9.4, 9.5, 11.5, mais a linha do `ds_oblvar` na tabela da 8.2); ficam `[X]` so as checagens de robustez 10.1 (curva completa) e 10.3 (por regime), que nao estavam na rodada.

## 2026-09-30 [DESKTOP] Rodada 4 (27 a 30/09): resultados e criterios

Cadeia `03-blender/scripts/rodada4.py`, plano e criterios fixados antes do primeiro resultado em `03-blender/PLANO-RODADA4.md` (commit 6ebbaa9). Disparada em 27/09 11:31, encerrada em 30/09 10:25 sem grupo com falha, com quatro pausas do autor. Os criterios foram aplicados por `python rodada4_criterios.py` (saida `rodada4_criterios.json`), que so le arquivos desta pasta.

### K. VisDrone pela regra oficial e a IoU 0,50/0,60/0,75 (10.6), armados a IoU 0,60 e 0,75, escala casada (10.2)

`python avalia_visdrone_oficial.py --modelos <nomes> --out visdrone_oficial_iou.json` (etapas K1 e Y1). Validador do Ultralytics com o filtro de `dropObjectsInIgr.m` (VisDrone2018-DET-toolkit): caixa verdadeira ou detectada com metade ou mais da area em regiao ignorada sai da avaliacao; 1.378 regioes em 340 das 548 imagens. Sem regioes, o avaliador reproduz o numero padrao em todos os modelos (`confere_padrao`). Classe unica, imgsz 1280, conf 0,001.

| modelo | mAP50 | AP60 | AP75 | mAP50 oficial | AP60 oficial | AP75 oficial |
|---|---|---|---|---|---|---|
| `r_pareado` | 0,6311 | 0,4871 | 0,1363 | 0,6548 | 0,5035 | 0,1400 |
| `s_nadir_4k` | 0,0102 | 0,0042 | 0,0002 | 0,0104 | 0,0043 | 0,0002 |
| `s_variedade` | 0,0190 | 0,0097 | 0,0052 | 0,0194 | 0,0098 | 0,0052 |
| `s_obliquo` | 0,0614 | 0,0313 | 0,0082 | 0,0624 | 0,0318 | 0,0082 |
| `s_oblvar` | 0,1055 | 0,0562 | 0,0136 | 0,1074 | 0,0572 | 0,0138 |
| `ft05_sint` | 0,4424 | 0,3225 | 0,0779 | 0,4555 | 0,3313 | 0,0797 |
| `ft05_coco` | 0,5220 | 0,3912 | 0,1033 | 0,5404 | 0,4039 | 0,1060 |
| `ft10_sint` | 0,5095 | 0,3845 | 0,1025 | 0,5271 | 0,3976 | 0,1050 |
| `ft10_coco` | 0,5709 | 0,4311 | 0,1136 | 0,5939 | 0,4469 | 0,1169 |
| `misto05` | 0,4607 | 0,3350 | 0,0878 | 0,4758 | 0,3452 | 0,0898 |
| `misto10` | 0,5428 | 0,4057 | 0,0983 | 0,5634 | 0,4197 | 0,1011 |
| `s_oblvar_sd1` | 0,0958 | 0,0497 | 0,0098 | 0,0978 | 0,0507 | 0,0101 |
| `s_oblvar_sd2` | 0,0887 | 0,0448 | 0,0117 | 0,0907 | 0,0456 | 0,0118 |
| `ft05_sint_sd1` | 0,4608 | 0,3319 | 0,0824 | 0,4735 | 0,3406 | 0,0840 |
| `ft05_sint_sd2` | 0,4554 | 0,3240 | 0,0796 | 0,4721 | 0,3356 | 0,0819 |
| `ft05_coco_sd1` | 0,5228 | 0,3952 | 0,1122 | 0,5428 | 0,4092 | 0,1153 |
| `ft05_coco_sd2` | 0,5285 | 0,3863 | 0,0995 | 0,5499 | 0,4010 | 0,1025 |

Eficacia pela regra oficial (R 0,6548): nadir 1,59%, variedade 2,96%, obliquo 9,53%, S-oblique-six 16,40%. Nenhum par comparado no artigo troca de ordem entre 0,50, 0,60 e 0,75, em nenhuma das duas regras (`rodada4_criterios.json`, item 10.6).

Armados a IoU 0,60 e 0,75 (`confusao_armado.py --iou 0.6` e `--iou 0.75`, saidas `confusao_armado_{75,35,75g}_iou60.json` e `_iou75.json`), fracao chamada de armada a 0,50 / 0,60 / 0,75:

| modelo | pessoa armada | pessoa desarmada | pessoa com objeto |
|---|---|---|---|
| `armado_75` | 0,547 / 0,504 / 0,376 | 0,131 / 0,124 / 0,085 | 0,237 / 0,230 / 0,141 |
| `armado_35` | 0,569 / 0,526 / 0,416 | 0,168 / 0,135 / 0,076 | 0,273 / 0,223 / 0,132 |
| `armado_75g` | 0,471 / 0,459 / 0,365 | 0,109 / 0,087 / 0,054 | 0,165 / 0,165 / 0,132 |

Pelo criterio, a ordem da taxa de objeto chamado de arma muda com o limiar (35 m acima de 75 m a 0,50, abaixo a 0,60 e a 0,75), entao essas taxas vao ao texto nos tres limiares. A 0,75 o 35 m e o gemeo empatam (0,132).

Escala casada (`python escala_casada.py`, saidas `escala_casada.json`, `sim2real_s_nadir_4k_casada.json`, `sim2real_r_pareado_casada.json`). O validador redimensiona cada imagem para o lado maior valer imgsz (`ultralytics/data/base.py`), entao a escala se casa pelo imgsz: a 1280 (protocolo) a mediana do lado maior das caixas do VisDrone val na entrada da rede e 25,33 px; a 1024 e 20,27 px, a mais perto dos 20,55 px do `ds_morro_4k`. `s_nadir_4k` a 1024: mAP50 0,0128 (contra 0,0102 a 1280, +25%); `r_pareado` a 1024: 0,5849. Criterio: diverge substancialmente se passar de 50%; **nao diverge**. Consequencia para o texto: a checagem do piloto (0,0055 contra 0,0061, `sim2real_morro_v1.json`) avaliou o conjunto reescalado e o nativo ambos a imgsz 640, isto e, na mesma escala de entrada; nao foi uma comparacao de escala.

### H. Objeto carregado como arma (9.5)

Corpus `ds_armado_75_porte`: o comando do teste de arma inedita (semente 47) com `--objeto-porte-arma` (objeto na distribuicao de pose da arma, sem o reangulo dos de mais de 1,15 m, mesmos sorteios). Gemeo caixa a caixa em 49 de 50 quadros (`porte_arma_gemeo.json`). `confusao_armado.py --split todos --instancias` no corpus normal e no de porte (`holdout_armas_armado_75_inst.json`, `porte_arma_armado_75.json`; idem com `75g`). Pareado objeto a objeto (227 objetos, `armado_75`): chamado de armada 0,154 no porte normal e 0,137 no porte de arma, 11 discordantes num sentido e 15 no outro, McNemar exato p 0,56. `armado_75g`: 0,181 e 0,141, p 0,12. Por tipo (`armado_75`): guarda-chuva 0,379 e 0,379; cano PVC 0,107 e 0,000; vassoura 0,098 e 0,049; enxada 0,167 e 0,222; vergalhao 0,167 e 0,194. Recall de armada igual nos dois corpora (0,434). Criterio: **a taxa nao sobe; sai a ressalva do angulo de porte**.

### F. Sintetico e real no mesmo treino (9.4)

`ds_misto05` e `ds_misto10`: os 890 ladrilhos de treino do `ds_oblvar_tiles` mais as 324 ou 647 imagens das fatias `ft05` e `ft10`, por link fisico (`monta_misto` em `rodada4.py`). Treino a partir do `yolo11s.pt`, 30 epocas, 1280, batch 6, single_cls, selecao em `sel`; teste `avalia_sim2real.py` no val inteiro (`sim2real_misto05.json`, `sim2real_misto10.json`):

| dado real | so real (COCO) | misto | sintetico e depois real |
|---|---|---|---|
| 5% | 0,5220 | 0,4607 (P 0,6073, R 0,4235, mAP50-95 0,1748) | 0,4424 |
| 10% | 0,5709 | 0,5428 (P 0,6540, R 0,4966, mAP50-95 0,2081) | 0,5095 |

Criterio: desvio entre as tres sementes do `ft05_coco` 0,0035; o misto fica 0,0613 (5%) e 0,0281 (10%) abaixo do so real, alem de 2 desvios: **misto pior nas duas fracoes** (a 10% com o desvio de 5%, declarado como aproximacao). O misto da mais passos de gradiente que o so real; cada imagem real e vista 30 vezes nos dois.

### E. Gemeo a 150 m (11.5)

`ds_armado_150g`: o comando do `ds_armado_35` com `--alt 150 --alt-jitter 13` (`GEMEO150`), 200 quadros, 2.248 caixas (784 armada, 723 desarmada, 741 objeto), 27 de validacao. Treino `armado_150g` (receita dos armados, 3 classes): parada antecipada na epoca 36. `confusao_armado.py --split val --instancias` (`confusao_armado_150g.json`): chamada de armada 0,337 (armada, n 92), 0,173 (desarmada, 104), 0,139 (objeto, 101); perdidas 41%, 64% e 44%; mAP50 de imagem inteira 0,368. Criterio de validade: detectar pelo menos metade das pessoas anotadas; o modelo detectou 148 de 297 (**0,498**): **nao interpretavel**, a ausencia a 150 m continua argumentada. Descritivo (`rodada4_criterios.json`): d' armada contra objeto 0,66 (IC 95% por bootstrap de quadros 0,20 a 1,13), contra 0,77 a 35 m e 0,89 no gemeo de 75 m.

### I. Validacao maior a 35 m e 75 m (9.5, 11.5)

`ds_armado_35_extra` e `ds_armado_75g_extra`: indices 200 a 279 da semente 43, todos em validacao, pelos comandos do 35 m e do gemeo. `confusao_armado.py --split val --instancias` (`extra_armado_35.json`, `extra_armado_75g.json`). Objeto chamado de arma: 35 m 0,253 (74 de 292), gemeo 0,125 (36 de 288), z 3,94, p bilateral 0,0001; somado ao val original 107 de 413 contra 51 de 379 (p < 0,001). Armada: 0,543 e 0,432; desarmada 0,156 e 0,140. d' armada contra objeto 0,77 (0,57 a 0,99) e 0,97 (0,77 a 1,20). Criterio: **estabelecida** (quadros novos, IoU 0,5).

### J. Regime de luz (10.3)

`ds_regime_4k`: indices 180 a 299 da semente 21 com o comando do `ds_morro_4k`, todos em validacao, 20 quadros por regime. `python por_regime.py --pesos runs/detect/s_nadir_4k/weights/best.pt --ds ds_regime_4k --tiles ds_regime_4k_tiles` (saida `por_regime_s_nadir_4k.json`):

| regime | mAP50 (ladrilhos) | recall a conf 0,25 (IC 95% bootstrap de quadros) |
|---|---|---|
| hard sun (sol_duro) | 0,675 | 0,657 (0,591 a 0,720) |
| heavy overcast (encoberto) | 0,755 | 0,768 (0,714 a 0,816) |
| rain (chuva) | 0,759 | 0,789 (0,748 a 0,827) |
| haze (neblina) | 0,780 | 0,726 (0,697 a 0,757) |
| low sun (sol_baixo) | 0,790 | 0,814 (0,768 a 0,854) |
| overcast (nublado) | 0,791 | 0,796 (0,760 a 0,827) |

Criterio da 10.3: overcast acima de hard sun e de rain, hard sun entre os dois mais fracos: **cumprido, a implicacao da 11.3 fica**. A vantagem de overcast sobre rain e pequena e os intervalos de recall se sobrepoem.

### G. Sementes de treino 1 e 2 (10.6)

Mesma receita com `--seed 1` e `--seed 2` (`train_yolo_win.py`); corpus fixo. O ajuste fino sintetico parte do S-oblique-six da mesma semente. VisDrone: `sim2real_s_oblvar_sd1.json` e analogos para `ft05_sint` e `ft05_coco`, sementes 1 e 2; armados: `confusao_armado_35_sd1.json` e analogos (val) e `extra_armado_35_sd1.json` e analogos (quadros novos).

| medida | semente 0 | 1 | 2 | criterio (faixas min-max) |
|---|---|---|---|---|
| S-oblique-six, mAP50 VisDrone | 0,1055 | 0,0958 | 0,0887 | media 0,0967, eficacia 15,3% (14,1 a 16,7%) |
| ajuste fino 5%, sintetico | 0,4424 | 0,4608 | 0,4554 | contra COCO: resolvivel |
| ajuste fino 5%, COCO | 0,5220 | 0,5228 | 0,5285 | dp 0,0035 |
| objeto chamado de arma, 35 m, val | 0,273 | 0,231 | 0,240 | contra gemeo: nao resolvivel |
| idem, gemeo 75 m, val | 0,165 | 0,132 | 0,242 | |
| objeto chamado de arma, 35 m, quadros novos | 0,253 | 0,202 | 0,209 | contra gemeo: resolvivel |
| idem, gemeo 75 m, quadros novos | 0,125 | 0,097 | 0,181 | |

Leitura: a vantagem do COCO no ajuste fino sobrevive a variacao entre treinos. O 16,7% do S-oblique-six foi o melhor de tres treinos; a media, 9,7 pontos de mAP50, fica logo dentro da faixa sintetica de Kiefer et al. (1,2 a 10,2) e vale 9,5 vezes o nadir (0,0967 / 0,0102). A diferenca de altitude nos armados se separa entre treinos nos 80 quadros novos (292 e 288 objetos), mas nao no val original (121 e 91), onde o gemeo de semente 2 chega a 0,242.

Rodada 4 encerrada em 30/09 10:25. Ficam `[X]` a curva de aprendizado da 10.1 e a ablacao so com sol duro da 10.3, que nao estavam na rodada.

## 2026-09-30 [DESKTOP] Revisao geral do manuscrito: origem dos numeros conferidos

A revisao geral de 30/09 (tres revisores: numeros, logica, forma) conferiu contra a fonte cada numero abaixo, que o texto usa sem citar arquivo (regra de 30/09: o artigo sai so como texto). Fica aqui a origem.

| No texto | Valor | Origem |
|---|---|---|
| 7.2, vao entre lotes | 0 com p 0,82; 0,5 a 1,2 m com p 0,12; 1,3 a 2,0 m com p 0,052; 2,3 a 3,1 m com p 0,008 | `03-blender/scripts/gen_morro.py`, funcao `folga()` (limiares 0,82, 0,94 e 0,992 sobre `rng.random()`) |
| 10.4, camera obliqua | 120 m com variacao de ate 36 m para cada lado | `gen_morro.py`, bloco `if args.obliqua`: `alt = 60 x res/1920` e `alt_jitter = 18 x res/1920`; em 4K (3840) da 120 e 36 |
| 8.2 e figura do nadir contra obliquo | h/w mediana 1,58 dos sem arma no corpus obliquo (1,46 em todas), tabela por pitch, 0,98 no nadir | `forma_corpora.json` (`ds_morro_obl/por_classe`, `ds_morro_obl/por_pitch`), `python mede_forma.py` |
| 9.1, pessoas nas imagens | 2.659 caixas nos 149 quadros de treino do corpus de referencia (3.225 nos 180); 18.858 pessoas nas 1.106 imagens de R | `alvo_por_split.json` (`ds_morro_4k/train`, `ds_morro_4k/todos`, `visdrone_sub/train`), `python mede_alvo_split.py` |
| 9.1 e tabela de protocolo, modelo R | 1.106 imagens sorteadas com semente 21; 60 epocas, batch 6, imgsz 1280, patience 15, semente de treino 0, as 60 epocas completas | sorteio: `monta_subamostra()` em `03-blender/scripts/fila_noite.py` (`random.Random(21).sample`, N = ladrilhos de treino do corpus de referencia); treino: `runs/detect/r_pareado/args.yaml` e `results.csv` (60 linhas) |
| 9.0, receita do piloto | ladrilho e entrada de 640 px, orcamento de 120 epocas, patience 15, batch 8, duas classes; parada antecipada na epoca 24 | `runs/detect/morro_clima_s/args.yaml` (`imgsz: 640`, `epochs: 120`, `patience: 15`, `batch: 8`, `data: ds_morro_clima_tiles`) e `results.csv` (24 linhas) |
| 7.5 e 11.3, elevacao do sol | 46 a 74 graus no hard sun, 9 a 25 no low sun | `gen_morro.py`, dicionario de regimes (`elev=(46, 74)` e `elev=(9, 25)`, desde o commit 6c604f6 de 20/09); realizado no corpus de referencia 47,2 a 74,0 e 9,1 a 24,9, e nos quadros do teste por regime 47,1 a 71,5 e 10,8 a 25,0 (campo `elev` dos manifests de `ds_morro_4k` e `ds_regime_4k`) |
| 7.6, validacao | 24 a 35 quadros por corpus | entrada de 26/09 acima (vals de 24 a 35 imagens) e `alvo_por_split.json` (31 no corpus de referencia) |
| 9.5, pessoas por quadro | 14 a 30 | entrada do teste de arma inedita acima (comando do `ds_armado_75`) |

Figura 5 refeita com rotulos em Arial (a fonte bitmap padrao do PIL comia os espacos): `python ../03-blender/scripts/previa_dataset.py --ds C:/arma3-favela/blender/ds_morro_clima --n 4 --cols 2 --larg 900 --zoom 5 --seed 1 --en --out figuras/fig5_anotacao.jpg`.

## 2026-09-30 [DESKTOP] Refino do artigo: origem das tabelas e figuras novas

Pedido do autor (analise geral, cortes, tabelas e figuras; diagnostico em `01-artigo/ANALISE-2026-09-30.md`). Nenhum numero novo foi medido; o que segue e a origem de cada numero que passou a aparecer em forma de tabela ou figura.

| Peca | Conteudo | Origem |
|---|---|---|
| Figura 5 (`figuras/fig9_desenho_experimental.png`) | diagrama do desenho experimental | so contagens de quadros ja no texto (180 e 200 por corpus, 80 quadros novos, 548 imagens do val, 1.106 de R); `C:/arma3-favela/venv/Scripts/python.exe figuras_mpl.py` |
| Figura 8 (`figuras/fig10_ajuste_fino.png`) | mAP50 no VisDrone val contra imagens reais de treino, tres usos do corpus sintetico, tres sementes e o teto R | lido dos JSON `sim2real_ft05_sint`, `_sd1`, `_sd2`, `sim2real_ft05_coco`, `_sd1`, `_sd2`, `sim2real_ft10_sint`, `sim2real_ft10_coco`, `sim2real_misto05`, `sim2real_misto10`, `sim2real_s_oblvar`, `_sd1`, `_sd2`, `sim2real_r_pareado` (mesmo comando) |
| Tabela 8 (resultados de relance) | doze modelos com dado de treino, teste, mAP50 e eficacia | numeros das secoes 9.1 a 9.5; as duas eficacias do treino conjunto sao razoes calculadas aqui: 0,4607 / 0,6311 = 0,7300 (73,0%) e 0,5428 / 0,6311 = 0,8601 (86,0%) |
| Tabela 16 (35 m contra gemeo a 75 m) | taxas nos vals e nos 80 quadros novos, faixas das tres sementes, IoU 0,60 e 0,75 | `gemeo_75_35.json`, `extra_armado_35.json`, `extra_armado_75g.json`, `confusao_armado_35_sd1/sd2.json`, `confusao_armado_75g_sd1/sd2.json`, `extra_armado_*_sd1/sd2.json`, `confusao_armado_35_iou60/75.json`, `confusao_armado_75g_iou60/75.json`, `rodada4_criterios.json` (numeros ja na entrada de 30/09 da rodada 4) |
| Tabela 17 (por regime) | mAP50, recall a 0,25 e intervalo de 95% dos seis regimes | `por_regime_s_nadir_4k.json` (`python por_regime.py`, entrada J da rodada 4); os tres recalls que nao estavam no texto: sol baixo 0,814 (0,768 a 0,854), neblina 0,726 (0,697 a 0,757), encoberto 0,768 (0,714 a 0,816) |

Saiu do artigo, e fica registrado aqui: a linha do piloto com o VisDrone reescalado por 1/2,49 (0,0061 contra 0,0055, `sim2real_morro_v1.json`), porque a 10.2 ja concluira que as duas avaliacoes viam a mesma escala de entrada; as correcoes historicas (1,62 para 0,94 na estatistica de orientacao; o 2,49 de escala; as redacoes anteriores das condicoes da 10.1 a 10.3) continuam nas entradas anteriores deste arquivo.

Paleta da figura 8 validada em 30/09 com o validador do skill dataviz (tres slots, todos os pares, modo claro): ΔE CVD minimo 9,2, visao normal 24,0; o verde-agua fica abaixo de 3:1 de contraste, por isso os valores vao escritos ao lado dos pontos.
