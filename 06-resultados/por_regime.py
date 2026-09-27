#!/usr/bin/env python3
"""
por_regime.py: desempenho do detector por regime de luz, a checagem 10.3 do artigo (rodada 4).

Corpus: ds_regime_4k, 120 quadros novos (indices 180 a 299) do mesmo comando e da mesma semente do
ds_morro_4k, todos em validacao; o gerador percorre os seis regimes em ordem, entao sao 20 quadros por
regime. Modelo: s_nadir_4k (S-nadir-150), treinado nos quadros 0 a 179.

Duas medidas por regime, fixadas antes de rodar:
  1. mAP50 (principal) nos ladrilhos de 1280 px do regime, pelo validador do Ultralytics, classe
     unica, conf 0,001: o mesmo protocolo do teto sintetico da secao 9.2;
  2. recall a conf 0,25 em imagem inteira (imgsz 3840, casamento 1:1 IoU >= 0,5), com IC 95% por
     bootstrap de quadros (2.000 reamostragens, semente 0), que da a incerteza que o mAP nao da.

Criterio da secao 10.3, aplicado a medida 1: a implicacao da secao 11.3 fica se o mAP50 sob
"overcast" (nublado) for maior que sob "hard sun" (sol_duro) e sob "rain" (chuva), e se sol_duro
estiver entre os dois regimes mais fracos; senao e retirada.

  python por_regime.py --pesos .../s_nadir_4k/weights/best.pt --ds .../ds_regime_4k --tiles .../ds_regime_4k_tiles
"""
import argparse
import glob
import json
import os
import random
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
NOMES_ARTIGO = {"sol_duro": "hard sun", "sol_baixo": "low sun", "nublado": "overcast",
                "neblina": "haze", "encoberto": "heavy overcast", "chuva": "rain"}


def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy
    return i / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i + 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pesos", required=True)
    ap.add_argument("--ds", required=True)
    ap.add_argument("--tiles", required=True)
    ap.add_argument("--out", default=os.path.join(AQUI, "por_regime_s_nadir_4k.json"))
    a = ap.parse_args()

    from ultralytics import YOLO

    clima = {}
    for ln in open(os.path.join(a.ds, "manifest.jsonl"), encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            clima[os.path.splitext(r["img"])[0]] = r["clima"]
    regimes = sorted(set(clima.values()), key=list(NOMES_ARTIGO).index)

    # 1. mAP50 nos ladrilhos de cada regime
    tiles = sorted(glob.glob(os.path.join(a.tiles, "images", "val", "*.jpg")))
    por = defaultdict(list)
    for t in tiles:
        quadro = "_".join(os.path.basename(t).split("_")[:2])          # mr_000183_01024_00880 -> mr_000183
        if quadro in clima:
            por[clima[quadro]].append(t.replace(os.sep, "/"))
    lst_dir = os.path.join(a.tiles, "listas")
    os.makedirs(lst_dir, exist_ok=True)
    res = {}
    for reg in regimes:
        lista = os.path.join(lst_dir, f"{reg}.txt")
        open(lista, "w").write("\n".join(por[reg]) + "\n")
        yml = os.path.join(lst_dir, f"{reg}.yaml")
        open(yml, "w").write(f"path: {a.tiles.replace(os.sep, '/')}\ntrain: {lista.replace(os.sep, '/')}\n"
                             f"val: {lista.replace(os.sep, '/')}\nnames:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
        r = YOLO(a.pesos).val(data=yml, imgsz=1280, conf=0.001, single_cls=True, plots=False, verbose=False)
        res[reg] = {"regime_no_artigo": NOMES_ARTIGO[reg], "ladrilhos": len(por[reg]),
                    "quadros": sum(1 for q, c in clima.items() if c == reg),
                    "mAP50": round(float(r.box.map50), 4), "mAP50-95": round(float(r.box.map), 4),
                    "P": round(float(r.box.mp), 4), "R": round(float(r.box.mr), 4)}
        print(reg, res[reg], flush=True)

    # 2. recall a conf 0,25 em imagem inteira, com bootstrap de quadros
    m = YOLO(a.pesos)
    acertos = defaultdict(list)            # regime -> [(acertos, n) por quadro]
    for img in sorted(glob.glob(os.path.join(a.ds, "images", "val", "*.png"))):
        base = os.path.splitext(os.path.basename(img))[0]
        lab = os.path.join(a.ds, "labels", "val", base + ".txt")
        if base not in clima or not os.path.exists(lab):
            continue
        r = m.predict(img, imgsz=3840, conf=0.25, verbose=False)[0]
        W, H = r.orig_shape[1], r.orig_shape[0]
        gts = []
        for ln in open(lab):
            _, cx, cy, w, h = map(float, ln.split())
            gts.append(((cx - w / 2) * W, (cy - h / 2) * H, (cx + w / 2) * W, (cy + h / 2) * H))
        preds = r.boxes.xyxy.tolist()
        pares = sorted(((iou(g, p), gi, pi) for gi, g in enumerate(gts) for pi, p in enumerate(preds)), reverse=True)
        ug, up, k = set(), set(), 0
        for v, gi, pi in pares:
            if v < 0.5:
                break
            if gi in ug or pi in up:
                continue
            ug.add(gi)
            up.add(pi)
            k += 1
        acertos[clima[base]].append((k, len(gts)))
    rnd = random.Random(0)
    for reg in regimes:
        q = acertos[reg]
        k, n = sum(x for x, _ in q), sum(y for _, y in q)
        bs = []
        for _ in range(2000):
            s = [q[rnd.randrange(len(q))] for _ in q]
            bs.append(sum(x for x, _ in s) / max(1, sum(y for _, y in s)))
        bs.sort()
        res[reg]["recall_conf025"] = {"acertos": k, "n": n, "recall": round(k / max(1, n), 4),
                                      "ic95_bootstrap_quadros": [round(bs[49], 4), round(bs[1949], 4)]}

    ordem = sorted(regimes, key=lambda g: res[g]["mAP50"])
    criterio = {
        "overcast_acima_de_hard_sun": res["nublado"]["mAP50"] > res["sol_duro"]["mAP50"],
        "overcast_acima_de_rain": res["nublado"]["mAP50"] > res["chuva"]["mAP50"],
        "hard_sun_entre_os_dois_mais_fracos": "sol_duro" in ordem[:2],
    }
    criterio["implicacao_11_3_fica"] = all(criterio.values())
    out = {"pesos": a.pesos, "ds": a.ds, "tiles": a.tiles, "por_regime": res,
           "ordem_mAP50_crescente": [NOMES_ARTIGO[g] for g in ordem], "criterio_10_3": criterio,
           "protocolo": "mAP50: ladrilhos 1280, classe unica, conf 0,001; recall: imagem inteira imgsz 3840, "
                        "conf 0,25, casamento 1:1 IoU >= 0,5, IC por bootstrap de quadros"}
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(criterio), flush=True)


if __name__ == "__main__":
    main()
