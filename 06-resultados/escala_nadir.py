#!/usr/bin/env python3
"""
escala_nadir.py: o imgsz casado para uma base real nadir (rodada 5, R5-6; PLANO-RODADA5.md, secao 3.3).

A regra e a da checagem 10.2 da rodada 4 (escala_casada.py), fixada antes de qualquer avaliacao: o
validador do Ultralytics redimensiona toda imagem para que o lado maior valha imgsz, entao a escala que
a rede ve se escolhe pelo imgsz. Este script usa SO os rotulos e o tamanho de cada imagem da divisao
`val` do --data (nenhuma saida de modelo): para cada imgsz multiplo de 32 calcula a mediana do lado
maior das caixas na entrada da rede e escolhe o que fica mais perto do --alvo (20,55 px, o lado maior
mediano do corpus de registro ds_morro_4k em resolucao nativa, alvo_por_split.json). O protocolo de
1280 fica registrado ao lado, como medida secundaria.

  C:/arma3-favela/venv/Scripts/python.exe -I escala_nadir.py --data C:/arma3-favela/real_nadir/heridal/yolo/data.yaml \
      --alvo 20.55 --out escala_heridal.json
"""
import argparse
import glob
import json
import os
import statistics as st


def le_yaml_simples(p):
    """data.yaml de duas ou tres chaves, sem depender de pyyaml (o script roda com -I)"""
    d = {}
    for ln in open(p, encoding="utf-8"):
        if ":" in ln and not ln.startswith(" "):
            k, v = ln.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def pasta_val(data):
    d = le_yaml_simples(data)
    base = d.get("path") or os.path.dirname(os.path.abspath(data))
    val = d["val"]
    return val if os.path.isabs(val) else os.path.join(base, val)


def medidas(img_dir):
    from PIL import Image
    lab_dir = img_dir.replace(os.sep + "images", os.sep + "labels").replace("/images", "/labels")
    L, sem_rotulo, n_img = [], 0, 0
    vistos = {}                 # no Windows *.jpg e *.JPG casam os mesmos arquivos: um por nome
    for p in glob.glob(os.path.join(img_dir, "*")):
        if p.lower().endswith((".jpg", ".jpeg", ".png")):
            vistos.setdefault(os.path.normcase(p), p)
    for p in sorted(vistos.values()):
        lab = os.path.join(lab_dir, os.path.splitext(os.path.basename(p))[0] + ".txt")
        if not os.path.exists(lab):
            sem_rotulo += 1
            continue
        with Image.open(p) as im:
            W, H = im.size
        n_img += 1
        for ln in open(lab, encoding="utf-8"):
            if ln.strip():
                _, _, _, w, h = map(float, ln.split())
                L.append((max(w * W, h * H), max(W, H)))
    return L, n_img, sem_rotulo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--alvo", type=float, default=20.55)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min", type=int, default=320)
    a = ap.parse_args()
    L, n_img, sem = medidas(pasta_val(a.data))
    if not L:
        raise SystemExit("nenhuma caixa na divisao val")
    maior = max(m for _, m in L)
    tab = {s: round(st.median(l * s / m for l, m in L), 2) for s in range(a.min, max(1280, ((maior + 31) // 32) * 32) + 1, 32)}
    escolhido = min(tab, key=lambda s: abs(tab[s] - a.alvo))
    out = {"data": a.data, "alvo_lado_maior_treino_px": a.alvo, "imagens": n_img, "imagens_sem_rotulo": sem,
           "caixas": len(L), "lado_maior_nativo_med_px": round(st.median(l for l, _ in L), 2),
           "imgsz_protocolo": 1280, "no_protocolo_lado_maior_med": tab.get(1280),
           "imgsz_casado": escolhido, "no_casado_lado_maior_med": tab[escolhido],
           "tabela_lado_maior_med": tab,
           "regra": "imgsz multiplo de 32 cuja mediana do lado maior das caixas na entrada da rede fica mais perto do alvo; "
                    "so rotulos e tamanhos de imagem, antes de qualquer avaliacao"}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(L)} caixas em {n_img} imagens; nativo {out['lado_maior_nativo_med_px']} px; "
          f"1280 -> {tab.get(1280)} px; casado imgsz {escolhido} -> {tab[escolhido]} px", flush=True)


if __name__ == "__main__":
    main()
