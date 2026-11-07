#!/bin/bash
# lote v3 (OSM + PBR + MPFB) em 4K, pos-processamento e treino YOLO
cd "$(dirname "$0")"
BL="/c/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"
PY=/c/arma3-favela/venv/Scripts/python.exe
SCRIPTS=../projeto_contexto/PROJETO-MACHINE-VISION-FAVELAS/02-projeto-ufrj-2022/arma3-2022/scripts
OUT=dataset_v3
rm -rf $OUT
echo "=== render inicio: $(date) ==="
"$BL" -b --python gen_jacarezinho.py -- --area jacarezinho --out $OUT --n 120 --res 3840 2160 --samples 48 --seed 2026 --pitch 55 90 --rebuild-every 6 > ${OUT}.log 2>&1
grep -E "^\[gen" ${OUT}.log | tail -3
echo "=== pos-processamento: $(date) ==="
$PY post_process.py --data $OUT --seed 7
echo "=== treino: $(date) ==="
$PY $SCRIPTS/train_yolo.py --data $OUT/data.yaml --model yolo11n.pt --epochs 40 --imgsz 1920 --batch 4 --name blender_v3 2>&1 | grep -vE "it/s\]?$" | tail -50
echo "=== fim: $(date) ==="
