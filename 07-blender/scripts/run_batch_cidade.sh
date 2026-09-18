#!/bin/bash
# Batelada "cidade de solidos" a 150 m: 560 imagens treino/val + teste angulos/luz (60) + teste multidao (40),
# pos-processamento de camera, tiling 1280 e treino YOLO11s. Log em batch_cidade.log
set -u
cd /c/arma3-favela/blender
BL="/c/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"
PY=/c/arma3-favela/venv/Scripts/python.exe
BLEND=C:/arma3-favela/odm/quadra.blend
COMUM="--blend $BLEND --samples 32 --alt 150 --alt-jitter 12 --margem 150"
echo "=== inicio $(date)"
[ -f dataset_cid150/data.yaml ] || "$BL" -b --python gen_cidade.py -- $COMUM --out dataset_cid150 --n 560 --seed 11 --pitch 50 90 --lens 30 50 --people 6 14 --val 0.15 > dataset_cid150.log 2>&1
echo "=== treino gerado $(date)"
[ -f teste_angulos/data.yaml ] || "$BL" -b --python gen_cidade.py -- $COMUM --out teste_angulos --n 60 --seed 77 --stamp ang --pitch 40 90 --lens 28 55 --people 6 14 --val 1.0 > teste_angulos.log 2>&1
echo "=== teste angulos gerado $(date)"
[ -f teste_denso/data.yaml ] || "$BL" -b --python gen_cidade.py -- $COMUM --out teste_denso --n 40 --seed 99 --stamp den --pitch 50 90 --lens 30 50 --people 30 60 --raio 22 --grupo 0.7 --grupo-n 3 8 --val 1.0 > teste_denso.log 2>&1
echo "=== teste denso gerado $(date)"
for D in dataset_cid150 teste_angulos teste_denso; do
  [ -d $D/images_png ] || $PY post_process.py --data $D --seed 5 --keep-png > ${D}_pp.log 2>&1
done
echo "=== pos-processado $(date)"
[ -f dataset_cid150_tiles/data.yaml ] || $PY tile_dataset.py --data dataset_cid150 --out dataset_cid150_tiles --tile 1280 --overlap 0.2 --keep-empty 0.05 > tiles.log 2>&1
echo "=== tiles $(date)"
$PY train_yolo_win.py --data dataset_cid150_tiles/data.yaml --model yolo11s.pt --epochs 60 --imgsz 1280 --batch 6 --workers 4 --name cid150_s > treino_cid150.log 2>&1
echo "=== treino fim $(date)"
