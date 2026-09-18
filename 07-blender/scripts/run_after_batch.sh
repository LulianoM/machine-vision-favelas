#!/bin/bash
# espera o lote terminar e treina o YOLO no dataset gerado pelo Blender
cd "$(dirname "$0")"
while ! grep -q "^\[gen\] fim" dataset_v1.log; do
  if ! tasklist //FI "IMAGENAME eq blender.exe" 2>/dev/null | grep -qi blender.exe; then echo "blender saiu sem [gen] fim"; break; fi
  sleep 60
done
echo "=== lote terminou: $(date) ==="; tail -2 dataset_v1.log
PY=/c/arma3-favela/venv/Scripts/python.exe
SCRIPTS=../projeto/PROJETO-MACHINE-VISION-FAVELAS/03-arma3/scripts
$PY $SCRIPTS/preview_boxes.py --data dataset_v1 --split val --n 12 --out dataset_v1/preview
$PY crops.py dataset_v1 60
echo "=== treino: $(date) ==="
$PY $SCRIPTS/train_yolo.py --data dataset_v1/data.yaml --model yolo11n.pt --epochs 40 --imgsz 1920 --batch 4 --name blender_v1 2>&1 | grep -vE "^\s+[0-9]+/[0-9]+ .*it/s\]?$" | tail -60
echo "=== fim treino: $(date) ==="
