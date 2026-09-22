#!/usr/bin/env python3
"""
encadeia.py: roda etapas da fila NA ORDEM DADA, e retoma um treino interrompido no meio.

Por que existe. `fila_noite.py --so 16,17,18,20,21,22,23,19` NAO roda nessa ordem: a fila itera a
lista de etapas na ordem de definicao e so filtra pelos ids. Em 22/09 isso fez a 19 (VisDrone
inteiro, 44 h) passar na frente do teste de dose (20 a 23), que era a prioridade acordada. Este
script roda cada grupo numa chamada separada, entao a ordem e a que esta escrita aqui.

A retomada usa o `last.pt` que o Ultralytics grava a cada epoca: `resume=True` reconstroi o
otimizador, o scheduler e a epoca de onde parou. As 8 epocas ja feitas da r_cheio nao se perdem.

Uso:
  python encadeia.py
"""
import os
import subprocess
import sys
from datetime import datetime

SCR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
FILA = os.path.join(SCR, "fila_noite.py")


def log(m):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}", flush=True)


def fila(ids, nome):
    log(f"{nome} (etapas {ids})")
    rc = subprocess.call([PY, FILA, "--so", ids], cwd=RAIZ)
    log(f"{nome}: rc={rc}")
    return rc


def retoma(run):
    last = os.path.join(RAIZ, "runs", "detect", run, "weights", "last.pt")
    if not os.path.exists(last):
        log(f"sem last.pt para {run}, nada a retomar")
        return 1
    log(f"retomando {run} de {last}")
    code = ("from ultralytics import YOLO\n"
            f"YOLO(r'{last}').train(resume=True)\n")
    rc = subprocess.call([PY, "-c", code], cwd=RAIZ)
    log(f"retomada de {run}: rc={rc}")
    return rc


fila("20,21,22,23", "teste de dose de variedade")
retoma("r_cheio")
fila("24", "benchmark de otimizacao")
log("cadeia encerrada")
sys.exit(0)
