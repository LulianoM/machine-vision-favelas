#!/usr/bin/env python3
"""
mede_alvo_split.py: tamanho e forma da caixa de pessoa por corpus E por split, com o lado maior.

Existe porque mede_alvo.py junta os splits e nao mede o lado maior, e o artigo precisa dos dois:
a tabela da secao 8.1 compara o lado maior mediano e a fracao de caixas cujo lado menor fica
abaixo do menor stride do detector (8 px), a secao 8 descreve o VisDrone-DET val (o conjunto de
teste) separado do treino, e a secao 9.1 conta as pessoas nas imagens do modelo R. Antes da
rodada 5 da validacao de 26/09 esses numeros estavam no texto sem arquivo de origem.

Mesmo metodo de mede_alvo.py: o rotulo YOLO normalizado vezes o tamanho da imagem, mediana sobre
todas as caixas do conjunto. Grava alvo_por_split.json ao lado deste script.

  python mede_alvo_split.py
"""
import glob
import json
import os
import statistics as st
from collections import Counter

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CORPORA = {
    "ds_morro_clima": os.path.join("C:" + os.sep, "arma3-favela", "blender", "ds_morro_clima"),
    "ds_morro_4k": os.path.join("C:" + os.sep, "arma3-favela", "blender", "ds_morro_4k"),
    # os dois corpora obliquos entraram em 2026-11-04 (item 2 de O-QUE-FALTA-NO-SERVIDOR.md): a Tabela 5
    # do artigo tinha a fracao sub-stride so das linhas nadir e do VisDrone
    "ds_morro_obl": os.path.join("C:" + os.sep, "arma3-favela", "blender", "ds_morro_obl"),
    "ds_oblvar": os.path.join("C:" + os.sep, "arma3-favela", "blender", "ds_oblvar"),
    "visdrone_yolo": os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "visdrone_yolo"),
    "visdrone_sub": os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "visdrone_sub"),
}
SPLITS = ("train", "val")


def pares(raiz, split):
    """aceita os dois arranjos de pasta do projeto: labels/<split> e <split>/labels"""
    for lab, img in ((os.path.join(raiz, "labels", split), os.path.join(raiz, "images", split)),
                     (os.path.join(raiz, split, "labels"), os.path.join(raiz, split, "images"))):
        if os.path.isdir(lab):
            for f in sorted(glob.glob(os.path.join(lab, "*.txt"))):
                base = os.path.splitext(os.path.basename(f))[0]
                cand = [os.path.join(img, base + e) for e in (".png", ".jpg", ".jpeg")]
                yield f, next((c for c in cand if os.path.exists(c)), None)
            return


def resume(ws, hs, n_img, tamanhos):
    if not ws:
        return None
    return dict(imagens=n_img, caixas=len(ws),
                larg_med=round(st.median(ws), 2), alt_med=round(st.median(hs), 2),
                lado_maior_med=round(st.median([max(w, h) for w, h in zip(ws, hs)]), 2),
                hw_med=round(st.median([h / w for w, h in zip(ws, hs) if w > 0]), 3),
                area_med=round(st.median([w * h for w, h in zip(ws, hs)]), 1),
                pct_lado_menor_abaixo_8px=round(100.0 * sum(1 for w, h in zip(ws, hs) if min(w, h) < 8) / len(ws), 2),
                tamanho_de_imagem_mais_comum=dict(zip(("tamanho", "imagens"), tamanhos.most_common(1)[0])))


def main():
    out = {"metodo": "rotulo YOLO normalizado vezes o tamanho da imagem; medianas sobre todas as caixas; "
                     "lado menor abaixo de 8 px = menor que o menor stride do YOLO11"}
    for nome, raiz in CORPORA.items():
        por, W_all, H_all, n_all, t_all = {}, [], [], 0, Counter()
        for sp in SPLITS:
            ws, hs, n, tam = [], [], 0, Counter()
            for f, img in pares(raiz, sp):
                if img is None:
                    continue
                W, H = Image.open(img).size
                n += 1
                tam[f"{W}x{H}"] += 1
                for linha in open(f, encoding="utf-8"):
                    p = linha.split()
                    if len(p) == 5:
                        ws.append(float(p[3]) * W)
                        hs.append(float(p[4]) * H)
            r = resume(ws, hs, n, tam)
            if r:
                por[sp] = r
                W_all += ws
                H_all += hs
                n_all += n
                t_all += tam
        if por:
            por["todos"] = resume(W_all, H_all, n_all, t_all)
            out[nome] = por
            for sp, r in por.items():
                print(f"{nome:<15} {sp:<6} {r['imagens']:>5} img {r['caixas']:>7} caixas  "
                      f"{r['larg_med']:>5} x {r['alt_med']:<5} lado maior {r['lado_maior_med']:>5}  "
                      f"h/w {r['hw_med']:<5}  area {r['area_med']:>6}  <8px {r['pct_lado_menor_abaixo_8px']:>5}%  "
                      f"{r['tamanho_de_imagem_mais_comum']}")
    with open(os.path.join(AQUI, "alvo_por_split.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
