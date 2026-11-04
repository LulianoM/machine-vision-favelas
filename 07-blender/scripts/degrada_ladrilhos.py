#!/usr/bin/env python3
"""
degrada_ladrilhos.py: copia um corpus de ladrilhos aplicando ruido de sensor, borrao e compressao JPEG
aos ladrilhos de TREINO, como aumento de dados fora de linha. Rodada 6, item 3 (ablacao de ruido,
borrao e JPEG, 6.5 do artigo), sem renderizar de novo.

Por que fora de linha. O Ultralytics 8.4 nao tem ruido, borrao nem JPEG como aumento configuravel (o
albumentations opcional aplica borrao com p = 0,01 e nao e parametrizavel sem codigo). Degradar os
ladrilhos uma vez, com semente fixa, deixa o treino identico ao dos corpora limpos em tudo o mais
(mesmos ladrilhos, mesma contagem, mesma validacao) e torna o corpus reprodutivel e inspecionavel.

Regra: cada ladrilho de treino sai degradado com probabilidade --prob (padrao 0,75) e limpo nos outros
casos (copia byte a byte), para a rede ver os dois. A degradacao sorteia, por ladrilho:
  ruido gaussiano dependente do sinal, sigma 0,004 a 0,018 (a faixa de post_process.py), mais forte nas sombras
  borrao gaussiano de 0,3 a 1,2 px
  JPEG de qualidade 50 a 90 com subamostragem de croma 4:2:0 (os ladrilhos limpos sao JPEG 92, 4:4:4)
A validacao e copiada sem mudanca (link fisico), os rotulos sao copiados, o data.yaml aponta para a
nova pasta. Os parametros sorteados de cada ladrilho ficam em _degradacao.json na pasta de saida.

  python degrada_ladrilhos.py --src C:/arma3-favela/blender/ds_morro_4k_tiles --out C:/arma3-favela/blender/ds_morro_4k_deg_tiles
"""
import argparse
import json
import os
import random
import shutil

import numpy as np
from PIL import Image, ImageFilter


def degrada(im, r):
    a = np.asarray(im).astype(np.float32) / 255.0
    sig = r.uniform(0.004, 0.018)
    ruido = np.random.default_rng(r.randint(0, 10 ** 9)).normal(0, 1, a.shape)
    a += ruido * (sig * (1.2 - a.mean(axis=2, keepdims=True)))
    a = np.clip(a, 0, 1)
    out = Image.fromarray((a * 255).astype(np.uint8))
    borrao = r.uniform(0.3, 1.2)
    out = out.filter(ImageFilter.GaussianBlur(borrao))
    q = r.randint(50, 90)
    return out, dict(sigma=round(sig, 4), borrao_px=round(borrao, 2), jpeg=q)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--prob", type=float, default=0.75)
    a = ap.parse_args()
    r = random.Random(a.seed)
    src, out = a.src, a.out
    if os.path.exists(os.path.join(out, "data.yaml")):
        print("ja existe:", out)
        return
    shutil.rmtree(out, ignore_errors=True)
    reg = {"src": src, "seed": a.seed, "prob": a.prob, "train": {}, "val": "copia sem mudanca (link fisico)"}
    for sp in ("train", "val"):
        os.makedirs(os.path.join(out, "images", sp))
        os.makedirs(os.path.join(out, "labels", sp))
        for f in sorted(os.listdir(os.path.join(src, "images", sp))):
            si = os.path.join(src, "images", sp, f)
            di = os.path.join(out, "images", sp, f)
            base = os.path.splitext(f)[0]
            lab = os.path.join(src, "labels", sp, base + ".txt")
            if os.path.exists(lab):
                shutil.copy2(lab, os.path.join(out, "labels", sp, base + ".txt"))
            if sp == "train" and r.random() < a.prob:
                im, par = degrada(Image.open(si).convert("RGB"), r)
                im.save(di, quality=par["jpeg"], subsampling=2)
                reg["train"][f] = par
            else:
                try:
                    os.link(si, di)
                except OSError:
                    shutil.copy2(si, di)
                if sp == "train":
                    reg["train"][f] = None
    with open(os.path.join(src, "data.yaml"), encoding="utf-8") as f:
        nomes = f.read().split("names:", 1)[1]
    with open(os.path.join(out, "data.yaml"), "w", encoding="utf-8") as f:
        f.write(f"path: {out.replace(os.sep, '/')}\ntrain: images/train\nval: images/val\nnames:{nomes}")
    n = len(reg["train"])
    nd = sum(1 for v in reg["train"].values() if v)
    reg["ladrilhos_treino"], reg["degradados"] = n, nd
    with open(os.path.join(out, "_degradacao.json"), "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=1)
    print(f"{out}: {nd} de {n} ladrilhos de treino degradados")


if __name__ == "__main__":
    main()
