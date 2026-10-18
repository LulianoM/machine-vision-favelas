#!/usr/bin/env python3
"""
checa_precisao_lote.py: qual parte da diferenca entre o mAP50 desta rodada e o reportado vem da precisao
(FP16 contra FP32) e qual vem do tamanho do lote (4 contra 16; o agrupamento retangular do validador
depende do lote). Mede um ou mais modelos nas quatro combinacoes, sem guardar predicoes.

  C:/arma3-favela/venv/Scripts/python.exe checa_precisao_lote.py --modelos ft10_coco r_pareado
Saida: checa_precisao_lote.json
"""
import argparse
import json
import os
import sys
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from visdrone_preds import DETECT, VIS_YAML, reportado  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", nargs="+", required=True)
    ap.add_argument("--combos", nargs="*", default=["4:16", "4:32", "16:32", "16:16"], help="lote:bits")
    a = ap.parse_args()
    from ultralytics import YOLO
    chk = os.path.join(AQUI, "checa_precisao_lote.json")
    out = json.load(open(chk, encoding="utf-8")) if os.path.exists(chk) else {}
    for run in a.modelos:
        pesos = os.path.join(DETECT, run, "weights", "best.pt")
        rep = reportado(run)
        linha = out.setdefault(run, {"reportado": rep})
        for combo in a.combos:
            lote, bits = (int(x) for x in combo.split(":"))
            kw = dict(data=VIS_YAML, imgsz=1280, conf=0.001, iou=0.7, max_det=300, single_cls=True, split="val",
                      batch=lote, plots=False, verbose=False)
            if bits == 16:
                kw["quantize"] = 16
            r = YOLO(pesos).val(**kw)
            m = round(float(r.box.map50), 5)
            linha[f"lote{lote}_fp{bits}"] = {"mAP50": m, "dif_reportado": None if rep is None else round(m - rep, 5),
                                            "quando": datetime.now().isoformat(timespec="seconds")}
            print(f"{run} lote {lote} fp{bits}: mAP50 {m:.5f}  reportado {rep}  dif {linha[f'lote{lote}_fp{bits}']['dif_reportado']}",
                  flush=True)
            json.dump(out, open(chk, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
