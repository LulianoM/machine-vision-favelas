#!/usr/bin/env python3
"""
supervisor_dose.py: espera a etapa 18 terminar, corta a 19 e roda o teste de dose antes dela.

Por que existe. A fila que esta rodando carregou a lista de etapas em memoria antes de as etapas
20 a 23 existirem, entao ela nao as conhece: depois da 18 ela emenda direto na 19, que e o treino
no VisDrone inteiro e leva cerca de 20 h. O teste de dose de variedade vale mais que a 19, porque
a razao de eficacia ja sai do braco real pareado e a 19 so melhora um denominador que ja temos.

O que ele NAO faz: nao interrompe nada que esteja produzindo resultado. Ele so age depois que a
etapa 18 estiver gravada como concluida no estado.json, e nesse instante a 19 comecou ha segundos.
Se a 18 falhar, ele age do mesmo jeito, porque o que interessa e nao deixar a 19 tomar a placa.

Ordem depois do corte: 20 a 23 (teste de dose) e so entao a 19, que passa a ser a ultima da fila,
que e onde ela deveria estar desde o inicio.

Uso:
  python supervisor_dose.py            # espera a 18 e age
  python supervisor_dose.py --agora    # corta ja, sem esperar
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

SCR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
ESTADO = os.path.join(RAIZ, "fila", "estado.json")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
FILA = os.path.join(SCR, "fila_noite.py")


def log(m):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}", flush=True)


def pid_da_fila():
    """acha o processo raiz da fila em execucao pela linha de comando.

    A fila roda como tres processos em arvore: o lancador do venv, o interpretador de verdade e o
    Blender ou o treino. Matar so o do meio deixa o filho orfao segurando a GPU, entao o alvo e a
    raiz, com /T para levar a arvore junto."""
    try:
        saida = subprocess.check_output(
            ["wmic", "process", "where", "name like '%python%'", "get", "ProcessId,ParentProcessId,CommandLine", "/format:csv"],
            stderr=subprocess.DEVNULL, text=True, errors="replace")
    except Exception as e:
        log(f"wmic falhou: {e!r}")
        return None
    cands = []
    for linha in saida.splitlines():
        if "fila_noite.py" in linha and "--listar" not in linha and "supervisor" not in linha:
            partes = linha.rsplit(",", 2)
            if len(partes) == 3:
                try:
                    cands.append((int(partes[1]), int(partes[2])))   # (ppid, pid)
                except ValueError:
                    pass
    if not cands:
        return None
    pids = {p for _, p in cands}
    # a raiz e aquela cujo pai NAO esta no conjunto
    for ppid, pid in cands:
        if ppid not in pids:
            return pid
    return cands[0][1]


def etapa_feita(n):
    try:
        return str(n) in json.load(open(ESTADO, encoding="utf-8"))
    except Exception:
        return False


ap = argparse.ArgumentParser()
ap.add_argument("--agora", action="store_true")
ap.add_argument("--espera", type=int, default=18, help="etapa cuja conclusao dispara o corte")
a = ap.parse_args()

if not a.agora:
    log(f"esperando a etapa {a.espera} concluir")
    while not etapa_feita(a.espera):
        time.sleep(60)
    log(f"etapa {a.espera} concluida")

pid = pid_da_fila()
if pid:
    log(f"cortando a fila em execucao, pid raiz {pid}, com a arvore junto")
    subprocess.call(["taskkill", "/PID", str(pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(20)
else:
    log("nenhuma fila em execucao encontrada, seguindo")

for etapas, nome in (("20,21,22,23", "teste de dose de variedade"),
                     ("19", "VisDrone inteiro, o que foi adiado")):
    log(f"rodando {nome} (etapas {etapas})")
    rc = subprocess.call([PY, FILA, "--so", etapas], cwd=RAIZ)
    log(f"{nome} terminou com rc={rc}")

log("supervisor encerrado")
sys.exit(0)
