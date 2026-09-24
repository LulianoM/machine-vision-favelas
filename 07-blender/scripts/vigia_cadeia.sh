#!/bin/bash
# vigia_cadeia.sh: uma passada de verificacao da cadeia. Imprime UMA linha so quando ha algo a
# fazer (processo morto, traceback novo, log parado); silencio = tudo bem. Relanca sozinho.
cd /c/arma3-favela/blender || exit 1
ESTADO=/c/arma3-favela/blender/vigia.estado
touch "$ESTADO"
ultimo_tb=$(cat "$ESTADO")

# 0. etapa nova concluida? (o Claude manda e-mail ao autor a cada uma; pedido de 23/09)
REL=/c/arma3-favela/blender/vigia.relatadas
touch "$REL"
for id in 25 26 27 12 13 14 15; do
  est=$(python -c "import json;e=json.load(open('fila/estado.json'));print(e.get('$id',{}).get('estado',''))" 2>/dev/null)
  if [ "$est" = "ok" ] && ! grep -qx "$id" "$REL"; then
    echo "$id" >> "$REL"
    echo "ETAPA OK: $id $(python -c "import json;e=json.load(open('fila/estado.json'));print(e['$id'].get('nome',''), e['$id'].get('segundos',''), 's')" 2>/dev/null)"
  fi
done
# zoom render (25) roda pelo retoma_cadeia, nao pela fila: conclui quando o data.yaml existe
if [ -f ds_armado_35/data.yaml ] && ! grep -qx "25" "$REL"; then echo "25" >> "$REL"; echo "ETAPA OK: 25 render_zoom35 $(wc -l < ds_armado_35/manifest.jsonl) quadros"; fi
if [ -f ds_morro_obl/data.yaml ] && ! grep -qx "12" "$REL"; then echo "12" >> "$REL"; echo "ETAPA OK: 12 render_obliquo $(wc -l < ds_morro_obl/manifest.jsonl) quadros"; fi

# 1. cadeia encerrada?
if tail -3 encadeia.log | grep -q "cadeia encerrada"; then
  echo "FIM: cadeia encerrada. $(grep -h '^real ' fila/15_aval_S_obliquo.log 2>/dev/null | tail -1)"
  exit 0
fi

# 2. processo vivo? (retoma_cadeia.py ou fila_noite.py)
vivo=$(wmic process where "name='python.exe'" get commandline 2>/dev/null | grep -c "retoma_cadeia\|fila_noite")
if [ "$vivo" = "0" ]; then
  # traceback novo desde a ultima passada?
  tb=$(grep -h "Traceback\|Error:\|CUDA error\|out of memory" fila/25_render_zoom35.log fila/27_treino_armado_35.log fila/12_render_obliquo.log fila/14_treino_S_obliquo.log 2>/dev/null | tail -1)
  echo "MORTO: relancando. ultimo erro: ${tb:-nenhum} | $(tail -1 encadeia.log)"
  powershell -c "Start-Process -FilePath 'C:\arma3-favela\venv\Scripts\python.exe' -ArgumentList '-u','C:\projetos\machine-vision-favelas\07-blender\scripts\retoma_cadeia.py' -WorkingDirectory 'C:\arma3-favela\blender' -RedirectStandardOutput 'C:\arma3-favela\blender\retoma.out' -RedirectStandardError 'C:\arma3-favela\blender\retoma.err' -WindowStyle Hidden" >/dev/null
  exit 0
fi

# 3. log parado ha mais de 40 min com processo vivo = travou
mais_novo=$(ls -t fila/*.log | head -1)
idade=$(( $(date +%s) - $(stat -c %Y "$mais_novo") ))
if [ "$idade" -gt 2400 ]; then
  echo "TRAVADO: $mais_novo sem escrita ha $((idade/60)) min; matando e relancando"
  wmic process where "name='blender.exe' or (name='python.exe' and commandline like '%retoma_cadeia%') or (name='python.exe' and commandline like '%fila_noite%') or (name='python.exe' and commandline like '%train_yolo%')" call terminate >/dev/null 2>&1
  sleep 5
  powershell -c "Start-Process -FilePath 'C:\arma3-favela\venv\Scripts\python.exe' -ArgumentList '-u','C:\projetos\machine-vision-favelas\07-blender\scripts\retoma_cadeia.py' -WorkingDirectory 'C:\arma3-favela\blender' -RedirectStandardOutput 'C:\arma3-favela\blender\retoma.out' -RedirectStandardError 'C:\arma3-favela\blender\retoma.err' -WindowStyle Hidden" >/dev/null
  exit 0
fi

# 4. traceback novo com processo vivo (a fila pode ter pulado para a etapa seguinte)
tb=$(grep -h "Traceback" fila/25_render_zoom35.log fila/27_treino_armado_35.log fila/12_render_obliquo.log fila/14_treino_S_obliquo.log 2>/dev/null | wc -l)
if [ "$tb" != "$ultimo_tb" ]; then
  echo "$tb" > "$ESTADO"
  if [ -n "$ultimo_tb" ] && [ "$tb" -gt "${ultimo_tb:-0}" ]; then
    echo "ERRO NOVO no log (tracebacks: $ultimo_tb -> $tb): $(grep -h -A3 Traceback fila/2[57]*.log fila/1[24]*.log 2>/dev/null | tail -4 | tr '\n' ' ' | cut -c1-300)"
  fi
fi
exit 0
