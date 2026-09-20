#!/usr/bin/env python3
"""
teste_fidelidade.py: mede, com número, a diferença entre as iterações do gerador e o alvo da
`RUBRICA-FIDELIDADE.md`. Roda fora do Blender, no venv de treino.

Por que existe: nas três vezes em que o loop andou para trás, a causa foi um bug de código que
a inspeção visual do render não pega (ColorRamp sem cor, ramo inalcançável, filtro que descarta
93% das tentativas). Olhar para a imagem e achar que melhorou não é evidência. Este script é o
que separa "melhorou" de "parece ter melhorado".

Cada métrica tem faixa alvo declarada, derivada da rubrica ou de fotografia aérea de favela
carioca ao meio-dia. A saída é uma tabela por iteração mais um veredito por métrica.

Uso:
  python teste_fidelidade.py                      # compara todas as versões em 06-resultados
  python teste_fidelidade.py --img caminho.png    # mede uma imagem só
  python teste_fidelidade.py --csv saida.csv
"""
import argparse
import csv
import glob
import re
import os

import numpy as np
from PIL import Image

# (nome, minimo, maximo, o que significa fora da faixa)
ALVOS = [
    ("luminancia_media", 90.0, 140.0, "cena sub ou superexposta para dia claro"),
    ("contraste_linear", 3.5, 4.5, "histograma de dois modos (sol e sombra) sem meio-tom"),
    ("meio_tom_pct", 35.0, 62.0, "faltam os tons medios que uma exposicao unica de sensor da"),
    ("escuro_pct", 0.0, 16.0, "sombra virou buraco sem informacao"),
    ("sombra_B_sobre_R", 0.70, 1.30, "sombra sem componente de ceu, cor de tijolo"),
    ("saturacao_media", 0.14, 0.24, "fora da faixa da fotografia aerea real de favela"),
    ("laranja_pct", 12.0, 30.0, "telha ceramica de menos ou monocromia laranja"),
    ("azul_forte_pct", 0.0, 1.2, "confete azul: caixa d'agua saturada demais e em excesso"),
    ("verde_telhado_pct", 0.0, 1.0, "telhado verde, que a referencia carioca nao tem"),
    ("anisotropia_0_90", 0.0, 1.60, "grade ortogonal legivel, assinatura de geracao procedural"),
]


def mede(caminho):
    a = np.asarray(Image.open(caminho).convert("RGB")).astype(np.float32) / 255.0
    L = a.mean(2)
    # CONTRASTE EM CENA LINEAR. Medir log2(p90/p10) direto em DN de tela da um numero
    # sistematicamente menor e nao comparavel ao alvo da rubrica: na mesma imagem, 3,09 em DN
    # corresponde a 4,87 em cena linear. Errar isso faz um item que reprova parecer que passa.
    lin = np.where(L <= 0.04045, L / 12.92, ((L + 0.055) / 1.055) ** 2.4)
    p10, p90 = np.percentile(lin, [10, 90])
    escuro = L[L < np.percentile(L, 12)]
    sh = a[L < np.percentile(L, 12)].mean(0) if len(escuro) else np.zeros(3)

    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    # matiz por maximo de canal, barato e suficiente para separar laranja de verde
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    delta = np.maximum(mx - mn, 1e-6)
    hue = np.where(mx == r, ((g - b) / delta) % 6,
                   np.where(mx == g, (b - r) / delta + 2, (r - g) / delta + 4)) * 60.0
    ilum = L > 0.30
    laranja = ilum & (hue > 10) & (hue < 45) & (sat > 0.25)
    azul_forte = ilum & (hue > 185) & (hue < 250) & (sat > 0.35)
    verde = ilum & (hue > 65) & (hue < 175) & (sat > 0.25) & (L > 0.42)   # verde CLARO: telhado,
    # a mata e escura e fica de fora pelo corte de luminancia

    # anisotropia: energia de aresta em 0 e 90 graus contra o esperado isotropico
    gy, gx = np.gradient(L)
    mag = np.hypot(gx, gy)
    forte = mag > np.percentile(mag, 88)
    ang = (np.degrees(np.arctan2(gy[forte], gx[forte])) % 180.0)
    if len(ang):
        card = float(((ang < 7.5) | (ang > 172.5) | (np.abs(ang - 90) < 7.5)).mean())
        aniso = card / (15.0 / 180.0)     # 15 graus de 180 e a fracao isotropica
    else:
        aniso = float("nan")

    return {
        "luminancia_media": float(L.mean() * 255),
        "contraste_linear": float(np.log2(max(p90, 1e-9) / max(p10, 1e-9))),
        "meio_tom_pct": float(((L * 255 >= 60) & (L * 255 <= 150)).mean() * 100),
        "escuro_pct": float((L * 255 < 25).mean() * 100),
        "sombra_B_sobre_R": float(sh[2] / max(sh[0], 1e-6)),
        "saturacao_media": float(sat.mean()),
        "laranja_pct": float(laranja.mean() * 100),
        "azul_forte_pct": float(azul_forte.mean() * 100),
        "verde_telhado_pct": float(verde.mean() * 100),
        "anisotropia_0_90": float(aniso),
    }


def veredito(nome, v):
    for m, lo, hi, _ in ALVOS:
        if m == nome:
            if np.isnan(v):
                return "?"
            return "ok" if lo <= v <= hi else ("baixo" if v < lo else "alto")
    return ""


ap = argparse.ArgumentParser()
ap.add_argument("--img", default=None, help="mede uma imagem so")
ap.add_argument("--dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "..", "..", "06-resultados"))
ap.add_argument("--csv", default=None)
args = ap.parse_args()

if args.img:
    alvos = [(os.path.basename(args.img), args.img)]
else:
    achados = glob.glob(os.path.join(args.dir, "morro_v*_nadir.jpg"))
    # ordem NUMERICA, nao alfabetica: alfabetica poe v10 antes de v3 e o "mais recente"
    # do relatorio sai errado, que e exatamente o tipo de erro silencioso que este script existe
    # para evitar.
    def _n(p):
        m = re.search(r"morro_v(\d+)_", os.path.basename(p))
        return int(m.group(1)) if m else 0
    alvos = [(os.path.basename(p).replace("morro_", "").replace("_nadir.jpg", ""), p)
             for p in sorted(achados, key=_n)]

if not alvos:
    raise SystemExit("nada para medir")

linhas = []
for nome, p in alvos:
    r = mede(p)
    r["versao"] = nome
    linhas.append(r)

cols = [m for m, _, _, _ in ALVOS]
larg = max(len(c) for c in cols) + 2
print(f"\n{'metrica':<{larg}} {'alvo':>14} " + " ".join(f"{l['versao']:>10}" for l in linhas))
print("-" * (larg + 16 + 11 * len(linhas)))
for m, lo, hi, _ in ALVOS:
    faixa = f"{lo:g} a {hi:g}"
    cel = []
    for l in linhas:
        v = l[m]
        marca = {"ok": " ", "baixo": "v", "alto": "^", "?": "?"}[veredito(m, v)]
        cel.append(f"{v:>9.2f}{marca}")
    print(f"{m:<{larg}} {faixa:>14} " + " ".join(cel))

print("\nfora da faixa na versao mais recente:")
ultima = linhas[-1]
algum = False
for m, lo, hi, porque in ALVOS:
    if veredito(m, ultima[m]) not in ("ok", "?"):
        print(f"  {m} = {ultima[m]:.2f} (alvo {lo:g} a {hi:g}): {porque}")
        algum = True
if not algum:
    print("  nenhuma. Todas as metricas medidas estao dentro da faixa.")

if args.csv:
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["versao"] + cols)
        w.writeheader()
        for l in linhas:
            w.writerow({k: l[k] for k in ["versao"] + cols})
    print(f"\ngravado {args.csv}")
