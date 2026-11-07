#!/usr/bin/env python3
"""
pausa_rodada5.py: pausa ou retoma a rodada 5 para o autor usar o PC (molde do pausa_rodada3.py).

  python pausa_rodada5.py pausa    cria fila5/PAUSA, encerra primeiro o supervisor e depois a cadeia, o
                                    Blender e o treino ou a avaliacao em curso (perde-se so o quadro ou a
                                    epoca em andamento), libera a GPU
  python pausa_rodada5.py retoma   apaga fila5/PAUSA e abre o supervisor (retoma_rodada5.cmd)

Com PAUSA presente, o supervisor aberto pelo atalho de inicializacao sai sem lancar nada, e a cadeia,
se ainda estiver viva, para antes da proxima etapa.
"""
import os
import subprocess
import sys
from datetime import datetime

import psutil

SCR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
FILA = os.path.join(RAIZ, "fila5")
PAUSA = os.path.join(FILA, "PAUSA")
LOGV = os.path.join(RAIZ, "vigia5.log")
CMD = os.path.join(SCR, "retoma_rodada5.cmd")
ALVOS = ("supervisiona_rodada5.py", "rodada5.py", "gen_morro.py", "train_yolo_win.py", "resume=True",
         "avalia_sim2real.py", "confusao_armado.py", "tile_dataset.py", "por_regime.py", "visdrone_preds.py",
         "preds_nadir.py", "bootstrap_nadir.py", "escala_nadir.py", "avalia_visdrone_oficial.py",
         "bootstrap_visdrone.py", "resolvivel.py", "rodada5_criterios.py")


def log(m):
    with open(LOGV, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} [pausa] {m}\n")
    print(m, flush=True)


def cmd(p):
    try:
        return " ".join(p.cmdline())
    except (psutil.Error, OSError):
        return ""


def encerra():
    eu = {os.getpid()} | {p.pid for p in psutil.Process().parents()}
    alvo = []
    for p in psutil.process_iter():
        if p.pid in eu:
            continue
        c = cmd(p)
        if any(k in c for k in ALVOS) and "status_rodada5" not in c and "pausa_rodada5" not in c:
            try:
                alvo += p.children(recursive=True) + [p]
            except psutil.Error:
                alvo.append(p)
    # supervisor primeiro, para ele nao relancar a cadeia no meio
    alvo.sort(key=lambda p: 0 if "supervisiona" in cmd(p) else 1)
    for p in alvo:
        try:
            p.kill()
        except psutil.Error:
            pass
    psutil.wait_procs(alvo, timeout=30)
    try:
        os.remove(os.path.join(FILA, "rodada5.trava"))
    except OSError:
        pass
    return len(alvo)


def main():
    acao = sys.argv[1] if len(sys.argv) > 1 else ""
    if acao == "pausa":
        os.makedirs(FILA, exist_ok=True)
        with open(PAUSA, "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat(timespec="seconds"))
        n = encerra()
        log(f"pausada pelo autor: {n} processos encerrados")
    elif acao == "retoma":
        try:
            os.remove(PAUSA)
        except OSError:
            pass
        subprocess.call(["cmd", "/c", CMD])
        log("retomada pelo autor")
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
