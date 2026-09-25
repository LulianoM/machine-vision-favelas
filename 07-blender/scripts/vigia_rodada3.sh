#!/bin/bash
# APOSENTADO em 25/09: substituido por supervisiona_rodada3.py. Uma copia orfa deste script (o TaskStop
# matou so o invólucro) relancou a cadeia seis minutos depois da pausa pedida pelo autor.
exit 0
# vigia_rodada3.sh: roda em segundo plano durante a rodada 3 e nao fala nada (so escreve em
# vigia3.log). A cada 10 min: se a cadeia morreu, relanca; se esta viva mas nenhum log de fila3 foi
# escrito em 45 min, mata o que for dela e relanca. A cadeia e idempotente e tem trava, entao
# relancar nunca duplica trabalho. Sai sozinho quando a rodada grava "fim" no estado.
# A analise de 1 em 1 h e do Claude (status_rodada3.py); isto aqui so garante que nada fica parado
# esperando a proxima analise.
# 25/09: depois de uma queda de energia a sessao subiu sem coreutils nem System32 no PATH
export PATH="/usr/bin:/bin:/mingw64/bin:/c/Windows/System32:/c/Windows:/c/Windows/System32/Wbem:/c/Windows/System32/WindowsPowerShell/v1.0:$PATH"
PYV=/c/arma3-favela/venv/Scripts/python.exe
RAIZ=/c/arma3-favela/blender
LOGV=$RAIZ/vigia3.log
relanca() {
  powershell -NoProfile -c "Start-Process -FilePath 'C:\arma3-favela\venv\Scripts\python.exe' -ArgumentList '-u','C:\projetos\machine-vision-favelas\07-blender\scripts\rodada3.py' -WorkingDirectory 'C:\arma3-favela\blender' -RedirectStandardOutput 'C:\arma3-favela\blender\rodada3.out' -RedirectStandardError 'C:\arma3-favela\blender\rodada3.err' -WindowStyle Hidden" >/dev/null 2>&1
}
echo "$(date '+%F %T') vigia iniciado" >> $LOGV
while true; do
  if $PYV -c "import json,sys; e=json.load(open(r'C:\arma3-favela\blender\fila3\estado.json')); sys.exit(0 if e.get('fim') else 1)" 2>/dev/null; then
    echo "$(date '+%F %T') rodada encerrada, vigia sai" >> $LOGV; exit 0
  fi
  vivo=$(wmic process where "name='python.exe'" get commandline 2>/dev/null | grep -v "status_rodada3" | grep -c "rodada3.py")
  if [ "$vivo" = "0" ]; then
    echo "$(date '+%F %T') cadeia morta: relancando" >> $LOGV
    rm -f $RAIZ/fila3/rodada3.trava
    relanca
  else
    novo=$(ls -t $RAIZ/fila3/*.log 2>/dev/null | head -1)
    if [ -n "$novo" ]; then
      idade=$(( $(date +%s) - $(stat -c %Y "$novo") ))
      if [ "$idade" -gt 2700 ]; then
        echo "$(date '+%F %T') travada ($(basename $novo) parado ha $((idade/60)) min): matando e relancando" >> $LOGV
        wmic process where "name='blender.exe' and commandline like '%gen_morro%'" call terminate >/dev/null 2>&1
        wmic process where "name='python.exe' and (commandline like '%rodada3.py%' or commandline like '%train_yolo_win%' or commandline like '%avalia_sim2real%' or commandline like '%confusao_armado%' or commandline like '%tile_dataset%' or commandline like '%resume=True%')" call terminate >/dev/null 2>&1
        sleep 20
        rm -f $RAIZ/fila3/rodada3.trava
        relanca
      fi
    fi
  fi
  sleep 600
done
