#!/bin/bash
# Fecha o ciclo: espera o Nordeste sair do ODM e o mapa do Sudoeste ficar pronto,
# remalha o Nordeste em alta densidade, gera o terreno dele e monta o mapa final
# com os dois setores no mesmo mundo.
cd "$(dirname "$0")"
BL="/c/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"
PY=/c/arma3-favela/venv/Scripts/python.exe
ODM=/c/arma3-favela/odm

echo "=== esperando o Nordeste sair do ODM: $(date) ==="
while ! grep -q "ODM app finished" $ODM/odm_nordeste.log 2>/dev/null; do sleep 60; done
echo "nordeste pronto: $(date)"

echo "=== esperando o mapa do Sudoeste terminar: $(date) ==="
while ! grep -q "=== fim:" rebuild_map.log 2>/dev/null; do sleep 60; done
echo "sudoeste pronto: $(date)"

echo "=== remalhando o Nordeste em alta densidade: $(date) ==="
echo "=== remesh nordeste $(date) ===" > $ODM/odm_nordeste_hq.log
cmd //c "C:\arma3-favela\odm\run_odm.cmd --project-path C:\arma3-favela\odm nordeste --rerun-from odm_meshing --mesh-size 3000000 --mesh-octree-depth 12 --orthophoto-resolution 4 --max-concurrency 8 --dsm --skip-report" >> $ODM/odm_nordeste_hq.log 2>&1
grep -E "app finished|ERROR" $ODM/odm_nordeste_hq.log | tail -2

echo "=== terreno do Nordeste: $(date) ==="
$PY export_dsm.py --sector nordeste 2>&1 | grep -vE "^[0-9.-]+ [0-9.-]+ [0-9.-]+$" | tail -5
"$BL" -b --python build_dsm_mesh.py -- --sector nordeste 2>&1 | grep -E "dsm_mesh|faces sem dado|salvo"

echo "=== mapa final com os dois setores: $(date) ==="
"$BL" -b --python build_map.py -- --sectors sudoeste nordeste \
  --out $ODM/jacarezinho.blend --preview --video 300 --video-res 1600 900 --pessoas 200 \
  > build_map_final.log 2>&1
grep -E "^\[mapa|Traceback|[A-Za-z]*Error" build_map_final.log | grep -v HIPEW | tail -25
ls -la $ODM/jacarezinho.blend $ODM/voo_jacarezinho.mp4 2>/dev/null
echo "=== fim final: $(date) ==="
