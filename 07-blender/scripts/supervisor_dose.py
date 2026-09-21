#!/usr/bin/env python3
"""
supervisor_dose.py: assume a fila depois do render armado, conserta o data.yaml e reordena.

Duas coisas precisam acontecer entre a etapa 16 e a 17, e a fila em execucao nao sabe de nenhuma
das duas porque carregou a lista de etapas em memoria antes de elas existirem.

1. O `data.yaml` do lote armado vai sair com DUAS classes. O gerador que esta rodando e o de
   antes do commit que corrigiu isso: ele declara `pessoa_armada` e `pessoa_desarmada` mesmo
   quando os rotulos trazem a terceira, `pessoa_objeto`. Conferido no manifesto: o lote tem 274
   caixas armadas, 255 desarmadas e 263 com objeto alongado. Se o yaml for para o ladrilhamento
   como esta, a classe 2 vira indice fora de faixa e o treino quebra horas depois.

2. Depois da 18 a fila emendaria na 19, o treino no VisDrone inteiro, que leva cerca de 20 h. O
   teste de dose de variedade vale mais: a razao de eficacia ja sai do braco real pareado, e a 19
   so melhora um denominador que ja temos.

O corte acontece quando a etapa 16 estiver gravada como concluida. Nesse instante a 17 comecou ha
segundos e e so ladrilhamento, que custa um minuto e refaz do zero sem prejuizo.

A fila roda como tres processos em arvore (lancador do venv, interpretador de verdade, e o Blender
ou o treino). Matar so o do meio deixa o filho orfao segurando a GPU, entao o alvo e a raiz, com
taskkill /T.

Uso:
  python supervisor_dose.py            # espera a etapa 16 e assume
  python supervisor_dose.py --agora    # assume ja
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
DS_ARM = os.path.join(RAIZ, "ds_armado_75")


def log(m):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}", flush=True)


def pid_da_fila():
    """raiz da arvore de processos da fila, achada pela linha de comando"""
    try:
        saida = subprocess.check_output(
            ["wmic", "process", "where", "name like '%python%'", "get",
             "ProcessId,ParentProcessId,CommandLine", "/format:csv"],
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
    for ppid, pid in cands:
        if ppid not in pids:
            return pid
    return cands[0][1]


def etapa_feita(n):
    try:
        return str(n) in json.load(open(ESTADO, encoding="utf-8"))
    except Exception:
        return False


def classes_nos_rotulos(raiz):
    """quais indices de classe FORAM de fato escritos. Contar em vez de supor pela --mistura,
    porque um lote pequeno pode nao produzir nenhuma instancia da terceira."""
    vistos = set()
    for split in ("train", "val"):
        d = os.path.join(raiz, "labels", split)
        if not os.path.isdir(d):
            continue
        for nome in os.listdir(d):
            for linha in open(os.path.join(d, nome), encoding="utf-8"):
                p = linha.split()
                if p:
                    vistos.add(int(p[0]))
    return vistos


def conserta_yaml(raiz):
    y = os.path.join(raiz, "data.yaml")
    if not os.path.exists(y):
        log(f"{y} nao existe, nada a consertar")
        return
    vistos = classes_nos_rotulos(raiz)
    n = (max(vistos) + 1) if vistos else 2
    NOMES = ["pessoa_armada", "pessoa_desarmada", "pessoa_objeto"]
    atual = open(y, encoding="utf-8").read()
    declaradas = atual.count("\n  ")
    log(f"{raiz}: classes nos rotulos {sorted(vistos)}, declaradas no yaml {declaradas}")
    if declaradas >= n:
        log("yaml ja esta coerente, nao mexo")
        return
    with open(y, "w", encoding="utf-8") as f:
        f.write("path: " + os.path.abspath(raiz).replace(os.sep, "/") + "\n"
                "train: images/train\nval: images/val\nnames:\n")
        for i in range(n):
            f.write(f"  {i}: {NOMES[i]}\n")
    log(f"yaml reescrito com {n} classes")


ap = argparse.ArgumentParser()
ap.add_argument("--agora", action="store_true")
ap.add_argument("--espera", type=int, default=16)
a = ap.parse_args()

if not a.agora:
    log(f"esperando a etapa {a.espera} concluir")
    while not etapa_feita(a.espera):
        time.sleep(60)
    log(f"etapa {a.espera} concluida")

pid = pid_da_fila()
if pid:
    log(f"assumindo a fila: matando a arvore da raiz {pid}")
    subprocess.call(["taskkill", "/PID", str(pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(20)
else:
    log("nenhuma fila em execucao encontrada, seguindo")

conserta_yaml(DS_ARM)

for etapas, nome in (("17,18", "ladrilhamento e treino do braco armado"),
                     ("20,21,22,23", "teste de dose de variedade"),
                     ("19", "VisDrone inteiro, que foi adiado de proposito")):
    log(f"rodando {nome} (etapas {etapas})")
    rc = subprocess.call([PY, FILA, "--so", etapas], cwd=RAIZ)
    log(f"{nome} terminou com rc={rc}")

log("supervisor encerrado")
sys.exit(0)
