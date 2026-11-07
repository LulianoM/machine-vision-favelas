#!/usr/bin/env python3
"""
retoma_cadeia.py: continua a cadeia da noite de onde parou. Idempotente: pode ser chamado quantas
vezes for preciso; cada chamada olha o que ja existe no disco e faz so o que falta.

Por que existe. Em 23/09 as 17:16 o app Claude atualizou e reiniciou, e a cadeia (encadeia.py),
lancada de dentro da sessao, morreu junto: no Windows o filho fica no mesmo job object do pai.
Tentei o Agendador de Tarefas e o WMI para desacoplar: nos dois o Blender sobe sem carregar as
extensoes do usuario (MPFB e blender_mcp somem do sys.path, mesmo com APPDATA igual), e o pool de
humanos sai vazio. Entao a cadeia continua sendo lancada da sessao, e o que garante a conclusao e
um watcher que chama este script de novo se o processo sumir.

Ordem:
  1. zoom (etapa 25): se o manifest de ds_armado_35 tem menos de 200 linhas, roda o gen_morro com
     --start N (deterministico desde 38bb01f: os quadros restantes saem iguais aos que sairiam).
  2. fila 26,27 (ladrilhar e treinar armado_35): a fila pula o que ja tem arquivo de prova.
  3. fila 12,13,14,15 (obliquo 4K): idem. O render do obliquo NAO tem retomada por quadro na fila;
     se cair no meio, este script passa --start pelo manifest tambem.
"""
import os
import subprocess
import sys
from datetime import datetime

SCR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
BLENDER = os.path.join("C:" + os.sep, "Program Files (x86)", "Steam", "steamapps", "common",
                       "Blender", "blender.exe")
LOG = os.path.join(RAIZ, "encadeia.log")


def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} [retoma] {m}\n")
    print(m, flush=True)


def linhas(p):
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def render_retomavel(nome_log, out, total, args_gen):
    """roda o gen_morro a partir do que ja existe no manifest; devolve rc"""
    feitos = linhas(os.path.join(out, "manifest.jsonl"))
    if os.path.exists(os.path.join(out, "data.yaml")) and feitos >= total:
        log(f"{nome_log}: ja completo ({feitos}/{total})")
        return 0
    cmd = [BLENDER, "-b", "--python-exit-code", "1", "--python",
           os.path.join(SCR, "gen_morro.py"), "--", "--out", out, "--dataset", str(total),
           *[str(a) for a in args_gen], "--start", str(feitos)]
    log(f"{nome_log}: retomando de {feitos}/{total}")
    with open(os.path.join(RAIZ, "fila", nome_log), "a", encoding="utf-8", buffering=1) as f:
        f.write(f"\n# {datetime.now():%Y-%m-%d %H:%M:%S} retomada --start {feitos}\n")
        rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=RAIZ)
    log(f"{nome_log}: rc={rc}")
    return rc


def fila(ids):
    log(f"fila --so {ids}")
    rc = subprocess.call([PY, "-u", os.path.join(SCR, "fila_noite.py"), "--so", ids], cwd=RAIZ)
    log(f"fila --so {ids}: rc={rc}")
    return rc


ZOOM = ["--samples", 64, "--res", 3840, 2160, "--people", 12, 24, "--pool", 6, "--seed", 43,
        "--climas", "todos", "--alt", 35, "--alt-jitter", 3, "--mistura", 0.34, 0.33, 0.33,
        "--porte-realista", "--fio-gsd", "--laje", 0.75, "--amostra-no-quadro"]
OBL = ["--samples", 96, "--res", 3840, 2160, "--people", 16, 34, "--pool", 6, "--seed", 21,
       "--climas", "todos", "--obliqua", "--mistura", 0.5, 0.5, 0.0]

if render_retomavel("25_render_zoom35.log", os.path.join(RAIZ, "ds_armado_35"), 200, ZOOM) != 0:
    sys.exit(1)
if fila("26,27") != 0:
    sys.exit(1)
if render_retomavel("12_render_obliquo.log", os.path.join(RAIZ, "ds_morro_obl"), 180, OBL) != 0:
    sys.exit(1)
if fila("13,14,15") != 0:
    sys.exit(1)
log("cadeia encerrada")
