#!/usr/bin/env python3
"""
mede_alvo.py: mede o tamanho e a forma da caixa de pessoa em qualquer dataset YOLO.

Existe porque o numero que caracteriza o alvo foi reportado errado duas vezes, e das duas o erro
mudou o argumento:

  1. Em 2026-09-19 o dataset saiu em 1080p em vez de 4K, o alvo ficou com 10 px, um quarto das
     caixas ficou abaixo do menor stride do YOLO e o treino falhou. O erro estava numa opcao de
     linha de comando, nao na cena.
  2. Em 2026-09-20 eu escrevi que o alvo do lote 4K tinha "24,6 px, contra 25,0 do VisDrone,
     portanto ja casados". 24,6 px e o PERCENTIL 90 da largura, nao a mediana. A mediana e 17,5
     px. Comparar o p90 de um com a mediana do outro nao compara nada.

Dai a regra que este script aplica: sempre imprimir mediana, p10 e p90 lado a lado, dos dois
conjuntos, e nunca so um numero solto.

O que a medicao mostra, e que importa para o artigo: a AREA em pixel dos dois conjuntos bate
dentro de 3%, e a FORMA nao bate, por um fator de 2,2 na razao altura sobre largura. Isso separa
duas hipoteses que ficariam confundidas: o alvo nao e menor, o alvo e outro. Nadir a 150 m ve
planta de cabeca e ombro (quadrada); o VisDrone ve pessoa em pe de camera obliqua (alta e
estreita). Nenhum reescalonamento uniforme conserta diferenca de forma, e e por isso que o braco
obliquo do gerador existe.

Uso:
  python mede_alvo.py C:/arma3-favela/blender/ds_morro_4k C:/arma3-favela/visdrone/visdrone_yolo
  python mede_alvo.py --csv alvo.csv <raiz> [<raiz> ...]
"""
import argparse
import csv
import glob
import os
import statistics as st
import sys

from PIL import Image


def pct(v, q):
    v = sorted(v)
    return v[min(len(v) - 1, int(q * len(v)))]


def mede(raiz):
    """aceita os dois arranjos de pasta que o projeto usa: images/<split> e <split>/images"""
    ws, hs = [], []
    padroes = [os.path.join(raiz, "labels", "*", "*.txt"),
               os.path.join(raiz, "*", "labels", "*.txt")]
    arquivos = []
    for p in padroes:
        arquivos += glob.glob(p)
    for f in sorted(set(arquivos)):
        base = os.path.basename(f)[:-4]
        img = None
        for cand in (f.replace(os.sep + "labels" + os.sep, os.sep + "images" + os.sep)[:-4] + ext
                     for ext in (".png", ".jpg", ".jpeg")):
            if os.path.exists(cand):
                img = cand
                break
        if img is None:
            continue
        W, H = Image.open(img).size
        for linha in open(img and f, encoding="utf-8"):
            p = linha.split()
            if len(p) == 5:
                ws.append(float(p[3]) * W)
                hs.append(float(p[4]) * H)
    if not ws:
        return None
    return dict(raiz=raiz, caixas=len(ws),
                larg_med=st.median(ws), larg_p10=pct(ws, 0.10), larg_p90=pct(ws, 0.90),
                alt_med=st.median(hs), alt_p10=pct(hs, 0.10), alt_p90=pct(hs, 0.90),
                area_med=st.median([w * h for w, h in zip(ws, hs)]),
                hw_med=st.median([h / w for w, h in zip(ws, hs) if w > 0]),
                abaixo_stride=100.0 * sum(1 for w, h in zip(ws, hs) if min(w, h) < 8) / len(ws))


ap = argparse.ArgumentParser()
ap.add_argument("raizes", nargs="+")
ap.add_argument("--csv", default=None)
a = ap.parse_args()

linhas = [x for x in (mede(r) for r in a.raizes) if x]
if not linhas:
    sys.exit("nenhuma caixa encontrada")

print(f"\n{'conjunto':<26}{'caixas':>8}{'larg med':>10}{'alt med':>9}{'area':>8}"
      f"{'h/w':>7}{'< stride 8':>12}")
print("-" * 80)
for d in linhas:
    print(f"{os.path.basename(d['raiz']):<26}{d['caixas']:>8}"
          f"{d['larg_med']:>10.1f}{d['alt_med']:>9.1f}{d['area_med']:>8.0f}"
          f"{d['hw_med']:>7.2f}{d['abaixo_stride']:>11.1f}%")
print("\ndispersao (p10 a p90)")
for d in linhas:
    print(f"  {os.path.basename(d['raiz']):<24} largura {d['larg_p10']:.0f} a {d['larg_p90']:.0f} px"
          f"   altura {d['alt_p10']:.0f} a {d['alt_p90']:.0f} px")

if len(linhas) == 2:
    a_, b_ = linhas
    print(f"\nrazao entre os dois, {os.path.basename(a_['raiz'])} sobre "
          f"{os.path.basename(b_['raiz'])}:")
    print(f"  area   {a_['area_med'] / b_['area_med']:.2f}x   "
          f"(reescalonamento uniforme corrige isto)")
    print(f"  forma  {a_['hw_med'] / b_['hw_med']:.2f}x   "
          f"(reescalonamento uniforme NAO corrige isto)")

if a.csv:
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        for d in linhas:
            w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in d.items()})
    print(f"\ngravado {a.csv}")
