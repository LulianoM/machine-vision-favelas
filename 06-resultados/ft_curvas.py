#!/usr/bin/env python3
"""
ft_curvas.py: curvas de aprendizado dos quatro ajustes finos da rodada 3 (secao 9.4 do artigo), na
fatia de selecao do VisDrone (324 imagens do treino, disjuntas das fatias de treino e do teste).

Le runs/detect/{ft05_sint, ft05_coco, ft10_sint, ft10_coco}/results.csv no desktop e grava
ft_curvas_selecao.json com mAP50 e mAP50-95 por epoca, a epoca do melhor mAP50 e a primeira epoca
em que o inicio COCO passa o inicio sintetico em cada volume. O numero de teste de cada modelo esta
em ft_visdrone.json (etapa D6 de rodada3.py); isto aqui e so selecao.

  python ft_curvas.py
"""
import csv
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join("C:" + os.sep, "arma3-favela", "blender", "runs", "detect")
NOMES = ["ft05_sint", "ft05_coco", "ft10_sint", "ft10_coco"]


def curva(nome):
    with open(os.path.join(RUNS, nome, "results.csv"), encoding="utf-8") as f:
        rows = [{k.strip(): v.strip() for k, v in r.items()} for r in csv.DictReader(f)]
    return [dict(epoca=int(r["epoch"]), mAP50=round(float(r["metrics/mAP50(B)"]), 4),
                 mAP50_95=round(float(r["metrics/mAP50-95(B)"]), 4)) for r in rows]


def main():
    out = {"conjunto": "fatia sel do VisDrone (324 imagens), escolha do peso; nao e teste"}
    for n in NOMES:
        c = curva(n)
        melhor = max(c, key=lambda x: x["mAP50"])
        out[n] = dict(epocas=len(c), melhor=melhor, curva=c)
    for v in ("05", "10"):
        s, k = out[f"ft{v}_sint"]["curva"], out[f"ft{v}_coco"]["curva"]
        passa = next((b["epoca"] for a, b in zip(s, k) if b["mAP50"] > a["mAP50"]), None)
        out[f"coco_passa_sint_{v}"] = passa
    with open(os.path.join(AQUI, "ft_curvas_selecao.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    for n in NOMES:
        m = out[n]["melhor"]
        print(f"{n:<10} epoca 1 {out[n]['curva'][0]['mAP50']:.3f}  melhor {m['mAP50']:.3f} na {m['epoca']}")
    print("COCO passa o sintetico na epoca:", out["coco_passa_sint_05"], "(5%)", out["coco_passa_sint_10"], "(10%)")


if __name__ == "__main__":
    main()
