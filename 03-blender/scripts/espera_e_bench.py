#!/usr/bin/env python3
"""
espera_e_bench.py: espera a fila em execucao acabar e roda o benchmark de otimizacao.

A fila que esta rodando foi lancada com `--so 16,17,18,20,21,22,23,19` e carregou essa lista em
memoria, entao ela nao conhece a etapa 24. Este esperador existe para nao precisar de ninguem
acordado: ele so olha se ainda existe processo da fila e, quando nao existir, dispara a 24.

Nao mata nada e nao interrompe nada. Se a fila cair no meio, o benchmark roda de todo jeito, o que
e o comportamento certo: ele nao depende de nenhuma etapa anterior.
"""
import os
import subprocess
import time
from datetime import datetime

SCR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")


def log(m):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}", flush=True)


def fila_viva():
    try:
        saida = subprocess.check_output(
            ["wmic", "process", "where", "name like '%python%'", "get", "CommandLine",
             "/format:csv"], stderr=subprocess.DEVNULL, text=True, errors="replace")
    except Exception:
        return True          # na duvida, espera: nunca competir pela GPU por acidente
    for linha in saida.splitlines():
        if "fila_noite.py" in linha and "--listar" not in linha:
            return True
    return False


log("esperando a fila em execucao acabar")
while fila_viva():
    time.sleep(300)
log("fila encerrada")

log("rodando a etapa 24, benchmark de otimizacao")
rc = subprocess.call([PY, os.path.join(SCR, "fila_noite.py"), "--so", "24"], cwd=RAIZ)
log(f"benchmark terminou com rc={rc}")
