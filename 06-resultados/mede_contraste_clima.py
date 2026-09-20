#!/usr/bin/env python3
"""
mede_contraste_clima.py: produz a tabela de contraste por regime de tempo da Seção 8.3 do artigo.

Existe porque a auditoria de números de 2026-09-20 não conseguiu reproduzir os dígitos da tabela:
ela vivia só numa nota de histórico, sem script e sem comando gravado, e a rubrica exige que todo
número do artigo tenha origem sob `06-resultados/` com o comando que o gerou.

O que mede, para cada caixa anotada:
  - luminância média dentro da caixa
  - luminância média de um anel de `--anel` pixels em volta, excluindo a própria caixa
  - desvio padrão desse anel

Duas quantidades saem daí. A diferença absoluta é o contraste bruto. A diferença dividida pelo
desvio do anel é o contraste contra a desordem local, que é o que o detector de fato enfrenta.

Agregação: caixa dentro de uma mesma imagem NÃO é independente (mesma cena, mesma luz, mesmo
ruído de render), então a estatística é a mediana por imagem e a dispersão reportada é ENTRE
imagens. Reportar dispersão entre caixas inflaria o n efetivo de 8 para ~114 por regime e faria
diferenças não resolvíveis parecerem resolvidas.

A luminância média de quadro sai do próprio corpus, e não dos renders de comparação de clima:
são cenas e enquadramentos diferentes, e misturar as duas fontes numa tabela só foi um erro
apontado pela mesma auditoria.

Uso:
  python mede_contraste_clima.py --ds C:\\arma3-favela\\blender\\ds_morro_clima --out contraste_clima.csv
"""
import argparse
import csv
import json
import os
from collections import defaultdict

import numpy as np
from PIL import Image

ORDEM = ["sol_duro", "sol_baixo", "nublado", "neblina", "encoberto", "chuva"]
NOME_EN = {"sol_duro": "Hard sun", "sol_baixo": "Low sun", "nublado": "Overcast",
           "neblina": "Haze", "encoberto": "Heavy overcast", "chuva": "Rain"}

ap = argparse.ArgumentParser()
ap.add_argument("--ds", required=True, help="raiz do dataset, com manifest.jsonl")
ap.add_argument("--anel", type=int, default=6, help="largura do anel de fundo, em pixels")
ap.add_argument("--out", default=None)
args = ap.parse_args()

reg = [json.loads(l) for l in open(os.path.join(args.ds, "manifest.jsonl"), encoding="utf-8")]
por_clima = defaultdict(lambda: {"bruto": [], "razao": [], "lum": [], "n_cx": 0})

for rec in reg:
    ip = os.path.join(args.ds, "images", rec["split"], rec["img"])
    lp = os.path.join(args.ds, "labels", rec["split"], os.path.splitext(rec["img"])[0] + ".txt")
    if not (os.path.exists(ip) and os.path.exists(lp)):
        continue
    a = np.asarray(Image.open(ip).convert("L")).astype(np.float32)
    H, W = a.shape
    brutos, razoes = [], []
    for ln in open(lp):
        v = ln.split()
        if len(v) < 5:
            continue
        xc, yc, w, h = (float(t) for t in v[1:5])
        x1, y1 = int((xc - w / 2) * W), int((yc - h / 2) * H)
        x2, y2 = int((xc + w / 2) * W), int((yc + h / 2) * H)
        if x2 <= x1 or y2 <= y1:
            continue
        m = args.anel
        X1, Y1 = max(0, x1 - m), max(0, y1 - m)
        X2, Y2 = min(W, x2 + m), min(H, y2 + m)
        alvo = a[y1:y2, x1:x2]
        anel = a[Y1:Y2, X1:X2].copy()
        anel[y1 - Y1:y2 - Y1, x1 - X1:x2 - X1] = np.nan
        if alvo.size < 4 or np.all(np.isnan(anel)):
            continue
        d = abs(float(np.nanmean(anel)) - float(alvo.mean()))
        brutos.append(d)
        razoes.append(d / max(float(np.nanstd(anel)), 1e-3))
    if not brutos:
        continue
    g = por_clima[rec["clima"]]
    g["bruto"].append(float(np.median(brutos)))
    g["razao"].append(float(np.median(razoes)))
    g["lum"].append(float(a.mean()))
    g["n_cx"] += len(brutos)

linhas = []
for k in ORDEM:
    g = por_clima.get(k)
    if not g or not g["razao"]:
        continue
    linhas.append(dict(
        regime=NOME_EN[k], clima=k, n_img=len(g["razao"]), n_caixas=g["n_cx"],
        lum_media=round(float(np.mean(g["lum"])), 1),
        bruto_dn=round(float(np.median(g["bruto"])), 1),
        razao_mediana=round(float(np.median(g["razao"])), 2),
        razao_dp_entre_img=round(float(np.std(g["razao"], ddof=1)), 2)))

print(f"anel de {args.anel} px, mediana por imagem, dispersao ENTRE imagens\n")
print(f"{'Regime':<16}{'lum':>7}{'bruto DN':>10}{'razao':>8}{'DP':>7}{'img':>6}{'caixas':>8}")
for l in linhas:
    print(f"{l['regime']:<16}{l['lum_media']:>7.1f}{l['bruto_dn']:>10.1f}"
          f"{l['razao_mediana']:>8.2f}{l['razao_dp_entre_img']:>7.2f}{l['n_img']:>6}{l['n_caixas']:>8}")

tot_i = sum(l["n_img"] for l in linhas)
tot_c = sum(l["n_caixas"] for l in linhas)
print(f"\ntotal: {tot_c} caixas em {tot_i} imagens")
print("Com este n por regime, diferenca menor que um DP nao e resolvivel.")

if args.out:
    p = args.out if os.path.isabs(args.out) else os.path.join(os.path.dirname(
        os.path.abspath(__file__)), args.out)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(f"gravado {p}")
