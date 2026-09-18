#!/bin/bash
# Depois que o mapa final terminar, gera o dataset sobre a MALHA REAL do Jacarezinho
# (textura fotografica das fotos da PCERJ) com pessoas sinteticas anotadas, ladrilha e treina.
# So roda com a maquina livre: com Blender e ODM disputando RAM, cada render passava de 10 minutos.
cd "$(dirname "$0")"
BL="/c/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"
PY=/c/arma3-favela/venv/Scripts/python.exe

echo "=== esperando o mapa final: $(date) ==="
while ! grep -q "^=== fim" mapa_hq.log 2>/dev/null; do sleep 60; done
echo "mapa pronto: $(date)"
sleep 20

echo "=== dataset sobre a malha real: $(date) ==="
rm -rf dataset_odm
"$BL" -b --python gen_odm.py -- --out dataset_odm --n 120 --res 3840 2160 --samples 40 \
  --seed 5051 --pitch 55 90 --people 5 10 --repool-every 10 > dataset_odm.log 2>&1
grep -E "^\[odm" dataset_odm.log | tail -3

echo "=== pos-processamento: $(date) ==="
$PY post_process.py --data dataset_odm --seed 11 --blur 0.8 1.4

echo "=== ladrilhamento: $(date) ==="
$PY tile_dataset.py --data dataset_odm --out dataset_odm_tiles --tile 1280 --overlap 0.2 | tail -2

echo "=== treino sobre a malha real: $(date) ==="
echo "=== treino odm $(date) ===" > treino_odm.log
$PY -u train_yolo_win.py --data dataset_odm_tiles/data.yaml --model yolo11s.pt \
  --epochs 60 --imgsz 1280 --batch 4 --workers 2 --name blender_odm_tiles >> treino_odm.log 2>&1
tail -14 treino_odm.log | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-140
echo "=== fim: $(date) ==="
