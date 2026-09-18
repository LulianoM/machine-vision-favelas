#!/bin/bash
# espera o lote v3 (render + treino) terminar, depois gera o dataset sobre a malha real (ODM Sudoeste),
# pos-processa e treina o YOLO. Depois faz o mesmo em 1080p com a camera real da PCERJ (z30).
cd "$(dirname "$0")"
BL="/c/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"
PY=/c/arma3-favela/venv/Scripts/python.exe
SCRIPTS=../projeto_contexto/PROJETO-MACHINE-VISION-FAVELAS/03-arma3/scripts
while ! grep -q "=== fim:" run_batch_v3.log; do sleep 60; done
echo "=== v3 terminou, iniciando dataset_odm: $(date) ==="
rm -rf dataset_odm
"$BL" -b --python gen_odm.py -- --out dataset_odm --n 150 --res 3840 2160 --samples 48 --seed 3031 --pitch 55 90 --people 5 10 --repool-every 8 > dataset_odm.log 2>&1
grep -E "^\[odm" dataset_odm.log | tail -2
$PY post_process.py --data dataset_odm --seed 9 --blur 0.8 1.4
echo "=== treino odm: $(date) ==="
$PY $SCRIPTS/train_yolo.py --data dataset_odm/data.yaml --model yolo11n.pt --epochs 40 --imgsz 1920 --batch 4 --name blender_odm 2>&1 | grep -vE "it/s\]?$" | tail -40
echo "=== z30 (camera real PCERJ, 150 m, 1080p): $(date) ==="
rm -rf dataset_odm_z30
"$BL" -b --python gen_odm.py -- --out dataset_odm_z30 --n 120 --samples 48 --seed 4041 --camera z30 --people 6 12 --repool-every 8 > dataset_odm_z30.log 2>&1
grep -E "^\[odm" dataset_odm_z30.log | tail -2
$PY post_process.py --data dataset_odm_z30 --seed 10 --blur 0.6 1.2
echo "=== fim odm: $(date) ==="
