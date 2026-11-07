#!/bin/bash
# Espera a remalhagem de alta densidade do ODM terminar, regenera o terreno do DSM
# e monta o mapa navegavel final, com previews e um voo em video.
cd "$(dirname "$0")"
BL="/c/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"
PY=/c/arma3-favela/venv/Scripts/python.exe
ODM=/c/arma3-favela/odm

echo "=== esperando remalhagem do sudoeste: $(date) ==="
while ! grep -q "ODM app finished" $ODM/odm_sudoeste_hq.log 2>/dev/null; do
  if ! tasklist //FI "IMAGENAME eq python.exe" 2>/dev/null | grep -qi python.exe; then
    echo "AVISO: nenhum python do ODM rodando"; break
  fi
  sleep 60
done
grep -E "app finished|ERROR" $ODM/odm_sudoeste_hq.log | tail -2
ls -la $ODM/sudoeste/odm_texturing/odm_textured_model_geo.obj

echo "=== terreno do DSM + ortomosaico novo: $(date) ==="
$PY export_dsm.py --sector sudoeste 2>&1 | grep -vE "^[0-9.-]+ [0-9.-]+ [0-9.-]+$" | tail -5
"$BL" -b --python build_dsm_mesh.py -- --sector sudoeste 2>&1 | grep -E "dsm_mesh|salvo"

echo "=== montando o mapa navegavel: $(date) ==="
"$BL" -b --python build_map.py -- --sectors sudoeste \
  --out $ODM/jacarezinho.blend --preview --video 240 --video-res 1600 900 --pessoas 120 \
  > build_map.log 2>&1
grep -E "^\[mapa|Traceback|[A-Za-z]*Error" build_map.log | grep -v HIPEW | tail -25
ls -la $ODM/jacarezinho.blend $ODM/voo_jacarezinho.mp4 2>/dev/null
echo "=== fim: $(date) ==="
