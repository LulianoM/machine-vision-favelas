#!/usr/bin/env python3
"""
pausa_rodada4.py: pausa ou retoma a rodada 4 para o autor usar o PC.

  python pausa_rodada4.py pausa    cria fila4/PAUSA, encerra o supervisor, a cadeia e o Blender/treino
                                    em curso (perde-se so o quadro ou a epoca em andamento), libera a GPU
  python pausa_rodada4.py retoma   apaga fila4/PAUSA e abre o supervisor (retoma_rodada4.cmd)

Com PAUSA presente, o supervisor aberto pelo atalho de inicializacao sai sem lancar nada.
"""
import os
import subprocess
import sys
from datetime import datetime

import psutil

RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
FILA = os.path.join(RAIZ, "fila4")
PAUSA = os.path.join(FILA, "PAUSA")
LOGV = os.path.join(RAIZ, "vigia4.log")


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
        if any(k in c for k in ("supervisiona_rodada4.py", "rodada4.py", "gen_morro.py",
                                "train_yolo_win.py", "resume=True", "avalia_sim2real.py",
                                "confusao_armado.py", "tile_dataset.py", "prepara_ft.py",
                                "avalia_visdrone_oficial.py", "escala_casada.py", "por_regime.py",
                                "rodada4_criterios.py")) \
                and "status_rodada4" not in c and "pausa_rodada4" not in c:
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
        os.remove(os.path.join(FILA, "rodada4.trava"))
    except OSError:
        pass
    return len(alvo)


def main():
    acao = sys.argv[1] if len(sys.argv) > 1 else ""
    if acao == "pausa":
        with open(PAUSA, "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat(timespec="seconds"))
        n = encerra()
        log(f"pausada pelo autor: {n} processos encerrados")
    elif acao == "retoma":
        try:
            os.remove(PAUSA)
        except OSError:
            pass
        subprocess.call(["cmd", "/c", os.path.join(RAIZ, "retoma_rodada4.cmd")])
        log("retomada pelo autor")
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
