#!/bin/bash
# Depois que o mapa terminar de renderizar, retoma o treino em ladrilhos.
# O treino anterior caiu por falta de RAM do sistema porque o Blender, o OpenDroneMap e os
# workers do DataLoader disputaram memoria ao mesmo tempo. Aqui ele roda com menos workers
# e so quando o mapa ja liberou a maquina.
cd "$(dirname "$0")"
PY=/c/arma3-favela/venv/Scripts/python.exe

echo "=== esperando o mapa terminar: $(date) ==="
while ! grep -q "^\[mapa.*fim" build_map_final.log 2>/dev/null; do sleep 30; done
echo "mapa pronto: $(date)"
sleep 10

echo "=== treino em ladrilhos, retomando do melhor peso: $(date) ==="
echo "=== treino ladrilhos 2 $(date) ===" > treino_v3_tiles2.log
$PY -u train_yolo_win.py --data dataset_v3_tiles/data.yaml \
  --weights runs/detect/blender_v3_tiles/weights/best.pt \
  --epochs 60 --imgsz 1280 --batch 4 --workers 2 --name blender_v3_tiles2 >> treino_v3_tiles2.log 2>&1
echo "EXIT=$?" >> treino_v3_tiles2.log
tail -12 treino_v3_tiles2.log | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-140
echo "=== fim: $(date) ==="
