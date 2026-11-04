#!/usr/bin/env python3
"""
transfere_cor.py: copia um corpus de ladrilhos aplicando aos ladrilhos de TREINO a transferencia de cor
linear de Monge-Kantorovich em direcao a estatistica de cor de imagens reais do VisDrone-DET train.
Rodada 6, grupo C (PLANO-RODADA6.md, 3.10), fora de linha como degrada_ladrilhos.py.

Duas fases:

  estat  para cada imagem de visdrone_yolo/train/images (NUNCA o val, que e o teste), media (3) e covariancia
         (3x3) RGB em 0..1, sobre os pixels de uma grade de passo 4 em cada eixo (a estatistica de segunda ordem
         de 1/16 dos pixels de uma imagem de 1360x765 ou mais e indistinguivel da de todos). Nao usa rotulo.
         Grava um JSON (uma entrada por imagem). Idempotente.
  aplica para cada ladrilho de treino, com probabilidade --prob (0,75) e semente --seed (0): sorteia uma imagem
         real alvo (mu_t, S_t), calcula media e covariancia do proprio ladrilho (mu_s, S_s) e aplica
             T  = S_s^-1/2 (S_s^1/2 S_t S_s^1/2)^1/2 S_s^-1/2
             x' = T (x - mu_s) + mu_t,  clip 0..1
         (raizes de matriz simetrica por autodecomposicao; autovalores abaixo de 1e-6 levados a 1e-6). Os outros
         ladrilhos saem limpos, copia byte a byte (link fisico). Salva como JPEG 92 4:4:4, igual aos limpos.
         Validacao intacta (link fisico), rotulos copiados, data.yaml apontando para a nova pasta, parametros por
         ladrilho (imagem alvo, mu_s, mu_t, T) em _transferencia.json.

  python transfere_cor.py estat --visdrone C:/arma3-favela/visdrone/visdrone_yolo/train/images --out C:/arma3-favela/visdrone/cor_visdrone_train.json
  python transfere_cor.py aplica --src C:/arma3-favela/blender/ds_morro_4k_tiles --out C:/arma3-favela/blender/ds_morro_4k_ct_tiles --estat C:/arma3-favela/visdrone/cor_visdrone_train.json
"""
import argparse
import json
import os
import random
import shutil
import sys

import numpy as np
from PIL import Image

PASSO = 4
EPS = 1e-6


def estat_img(caminho):
    a = np.asarray(Image.open(caminho).convert("RGB"), dtype=np.float64)[::PASSO, ::PASSO] / 255.0
    x = a.reshape(-1, 3)
    return x.mean(0), np.cov(x, rowvar=False)


def raiz(S, inversa=False):
    w, V = np.linalg.eigh((S + S.T) / 2)
    w = np.maximum(w, EPS)
    d = w ** (-0.5 if inversa else 0.5)
    return (V * d) @ V.T


def mapa_mk(S_s, S_t):
    r = raiz(S_s)
    ri = raiz(S_s, inversa=True)
    return ri @ raiz(r @ S_t @ r) @ ri


def fase_estat(a):
    if os.path.exists(a.out):
        print("ja existe:", a.out)
        return
    if os.sep + "val" in os.path.normpath(a.visdrone) or "/val" in a.visdrone.replace("\\", "/"):
        sys.exit("recusado: a estatistica vem so do treino do VisDrone, nunca do val")
    fs = sorted(f for f in os.listdir(a.visdrone) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    out = {"origem": a.visdrone, "passo_px": PASSO, "n": len(fs), "imagens": {}}
    for i, f in enumerate(fs):
        mu, S = estat_img(os.path.join(a.visdrone, f))
        out["imagens"][f] = {"mu": [round(float(v), 6) for v in mu], "S": [[round(float(v), 8) for v in r] for r in S]}
        if i % 500 == 0:
            print(f"{i}/{len(fs)}", flush=True)
    tmp = a.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(out, fh)
    os.replace(tmp, a.out)
    print(f"{a.out}: {len(fs)} imagens")


def fase_aplica(a):
    if os.path.exists(os.path.join(a.out, "data.yaml")):
        print("ja existe:", a.out)
        return
    est = json.load(open(a.estat, encoding="utf-8"))
    alvos = sorted(est["imagens"])
    r = random.Random(a.seed)
    shutil.rmtree(a.out, ignore_errors=True)
    reg = {"src": a.src, "estat": a.estat, "seed": a.seed, "prob": a.prob, "jpeg": "92, 4:4:4", "train": {},
           "val": "copia sem mudanca (link fisico)"}
    for sp in ("train", "val"):
        os.makedirs(os.path.join(a.out, "images", sp))
        os.makedirs(os.path.join(a.out, "labels", sp))
        for f in sorted(os.listdir(os.path.join(a.src, "images", sp))):
            si = os.path.join(a.src, "images", sp, f)
            di = os.path.join(a.out, "images", sp, f)
            base = os.path.splitext(f)[0]
            lab = os.path.join(a.src, "labels", sp, base + ".txt")
            if os.path.exists(lab):
                shutil.copy2(lab, os.path.join(a.out, "labels", sp, base + ".txt"))
            if sp == "train" and r.random() < a.prob:
                alvo = r.choice(alvos)
                mu_t = np.array(est["imagens"][alvo]["mu"])
                S_t = np.array(est["imagens"][alvo]["S"])
                x = np.asarray(Image.open(si).convert("RGB"), dtype=np.float64) / 255.0
                p = x.reshape(-1, 3)
                mu_s, S_s = p.mean(0), np.cov(p, rowvar=False)
                T = mapa_mk(S_s, S_t)
                y = np.clip((p - mu_s) @ T.T + mu_t, 0, 1).reshape(x.shape)
                Image.fromarray((y * 255 + 0.5).astype(np.uint8)).save(di, quality=92, subsampling=0)
                reg["train"][f] = {"alvo": alvo, "mu_s": [round(float(v), 4) for v in mu_s],
                                   "mu_t": [round(float(v), 4) for v in mu_t],
                                   "T": [[round(float(v), 4) for v in row] for row in T]}
            else:
                try:
                    os.link(si, di)
                except OSError:
                    shutil.copy2(si, di)
                if sp == "train":
                    reg["train"][f] = None
    with open(os.path.join(a.src, "data.yaml"), encoding="utf-8") as fh:
        nomes = fh.read().split("names:", 1)[1]
    with open(os.path.join(a.out, "data.yaml"), "w", encoding="utf-8") as fh:
        fh.write(f"path: {a.out.replace(os.sep, '/')}\ntrain: images/train\nval: images/val\nnames:{nomes}")
    n = len(reg["train"])
    nt = sum(1 for v in reg["train"].values() if v)
    reg["ladrilhos_treino"], reg["transferidos"] = n, nt
    with open(os.path.join(a.out, "_transferencia.json"), "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=1)
    print(f"{a.out}: {nt} de {n} ladrilhos de treino transferidos")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="fase", required=True)
    e = sub.add_parser("estat")
    e.add_argument("--visdrone", required=True)
    e.add_argument("--out", required=True)
    p = sub.add_parser("aplica")
    p.add_argument("--src", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--estat", required=True)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--prob", type=float, default=0.75)
    a = ap.parse_args()
    fase_estat(a) if a.fase == "estat" else fase_aplica(a)


if __name__ == "__main__":
    main()
