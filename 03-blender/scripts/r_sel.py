#!/usr/bin/env python3
"""
r_sel.py: item 4 de 08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md (teto R com selecao fora do teste).

Treina R de novo com a MESMA receita de r_pareado (fila_noite.py, etapa 10: yolo11s.pt, as 1.106 imagens de
visdrone_sub/train, 60 epocas, batch 6, imgsz 1280, paciencia 15, semente 0, classe unica; conferido com
train_yolo_win.py --dry-run --compara: so `data` e `name` mudam), trocando apenas a divisao em que o
checkpoint e escolhido: `sel_r` (C:/arma3-favela/visdrone/ft/sel_r.txt, 265 imagens do VisDrone train que
nao estao na amostra de treino de R nem no VisDrone val; sao as 324 da fatia `sel` menos 59 em comum com
visdrone_sub/train, ver ft/sel_r.json) em vez do proprio VisDrone val, que e o conjunto de teste.

Etapas, cada uma so roda se a saida nao existir (idempotente; o treino retoma de last.pt):
  1. treino  -> runs/detect/r_pareado_sel/weights/best.pt + TREINO_OK
  2. aval    -> 06-resultados/sim2real_r_pareado_sel.json (zero-shot no VisDrone val, imgsz 1280)
  3. preds   -> 06-resultados/revisao-2026-10-17/preds_visdrone_r_pareado_sel.npz (para bootstrap e regra oficial)

Uso (cwd C:\\arma3-favela\\blender; o lanca_r_sel.cmd faz isso e grava r_sel.log):
  C:\\arma3-favela\\venv\\Scripts\\python.exe -u -X utf8 r_sel.py
"""
import os
import subprocess
import sys
from datetime import datetime

RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
REPO = os.path.join("C:" + os.sep, "projetos", "machine-vision-favelas")
SCR = os.path.join(REPO, "03-blender", "scripts")
RES = os.path.join(REPO, "06-resultados")
REV = os.path.join(RES, "revisao-2026-10-17")
DATA = "C:/arma3-favela/visdrone/visdrone_sub/data_sel.yaml"
VIS_YAML = os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "visdrone_yolo", "data.yaml")
NOME = "r_pareado_sel"
RUN = os.path.join(RAIZ, "runs", "detect", NOME)
BEST = os.path.join(RUN, "weights", "best.pt")
LAST = os.path.join(RUN, "weights", "last.pt")
OK = os.path.join(RUN, "TREINO_OK")


def log(m):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}", flush=True)


def roda(cmd):
    log("$ " + " ".join(str(c) for c in cmd))
    return subprocess.call([str(c) for c in cmd], cwd=RAIZ)


def treino():
    if os.path.exists(OK) and os.path.exists(BEST):
        log("treino ja feito")
        return 0
    if os.path.exists(LAST):
        log("retomando de last.pt")
        from ultralytics import YOLO
        YOLO(LAST).train(resume=True)
        rc = 0 if os.path.exists(BEST) else 1
    else:
        rc = roda([PY, os.path.join(SCR, "train_yolo_win.py"), "--data", DATA, "--model", "yolo11s.pt",
                   "--imgsz", 1280, "--epochs", 60, "--batch", 6, "--workers", 4, "--name", NOME, "--single-cls"])
    if rc == 0 and os.path.exists(BEST):
        open(OK, "w").write(f"{datetime.now():%Y-%m-%d %H:%M:%S}\n")
    return rc


def aval():
    saida = os.path.join(RES, f"sim2real_{NOME}.json")
    if os.path.exists(saida):
        log("aval ja feita")
        return 0
    return roda([PY, os.path.join(SCR, "avalia_sim2real.py"), "--weights", BEST, "--real", VIS_YAML,
                 "--imgsz", 1280, "--out", saida])


def preds():
    saida = os.path.join(REV, f"preds_visdrone_{NOME}.npz")
    if os.path.exists(saida):
        log("preds ja feitas")
        return 0
    return roda([PY, os.path.join(REV, "visdrone_preds.py"), "--modelos", NOME, "--batch", 4])


def main():
    log("r_sel: inicio")
    for nome, fn in (("treino", treino), ("aval", aval), ("preds", preds)):
        rc = fn()
        log(f"{nome}: rc={rc}")
        if rc != 0:
            log("r_sel: parou com erro")
            sys.exit(rc)
    log("r_sel: FIM")


if __name__ == "__main__":
    main()
