#!/usr/bin/env python3
"""
preds_nadir.py: o visdrone_preds.py para uma base real nadir (rodada 5, R5-6; PLANO-RODADA5.md, secao 3.3).

Roda o validador do Ultralytics na divisao `val` do --data, uma vez por modelo, com o protocolo do
artigo (classe unica, conf 0,001, NMS IoU 0,7, max_det 300, FP32, lote 4) no --imgsz pedido, e guarda
por imagem o que o validador usa para o mAP (acerto nos 10 limiares de IoU, confianca, caixas
verdadeiras), para a reamostragem de bootstrap_nadir.py. O validador que guarda e o mesmo de
visdrone_preds.py (importado de la), cuja reproducao bateu o reportado a 0,00005.

Saidas, nesta pasta: preds_<tag>_<run>.npz por modelo e <tag>_reproducao.json com o mAP50 do validador
e o recalculado dos dados guardados. Um .npz que ja existe e pulado (--refaz para medir de novo). Como
o nome do arquivo nao leva o imgsz, cada imgsz tem a sua tag: a cadeia usa `heridal` no imgsz casado
(escala_heridal.json) e `heridal_1280` no protocolo de 1280.

Se a GPU ficar sem memoria (imagens de 12 MP em imgsz alto), o lote cai para 2 e depois 1, e o lote
usado fica no JSON.

  C:/arma3-favela/venv/Scripts/python.exe preds_nadir.py --data C:/arma3-favela/real_nadir/heridal/yolo/data.yaml \
      --tag heridal --imgsz 2016 --modelos s_nadir_4k s_obliquo r_pareado
"""
import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from visdrone_preds import DETECT, recalcula_map50, validador_que_guarda  # noqa: E402


def roda(run, data, tag, batch, imgsz, refaz):
    from ultralytics import YOLO
    import torch
    saida_npz = os.path.join(AQUI, f"preds_{tag}_{run}.npz")
    if os.path.exists(saida_npz) and not refaz:
        print(f"{run}: ja guardado em {os.path.basename(saida_npz)}")
        return None
    pesos = os.path.join(DETECT, run, "weights", "best.pt")
    if not os.path.exists(pesos):
        print(f"{run}: SEM PESOS em {pesos}")
        return {"run": run, "pesos": pesos, "faltando": True}
    r = None
    for lote in [b for b in (batch, 2, 1) if b <= batch]:
        try:
            kw = dict(data=data, imgsz=imgsz, conf=0.001, iou=0.7, max_det=300, single_cls=True, split="val",
                      batch=lote, plots=False, verbose=False, validator=validador_que_guarda())
            r = YOLO(pesos).val(**kw)
            batch = lote
            break
        except torch.cuda.OutOfMemoryError:
            print(f"{run}: sem memoria com lote {lote}", flush=True)
            torch.cuda.empty_cache()
    if r is None:
        raise SystemExit(f"{run}: sem memoria mesmo com lote 1")
    map50_val = float(r.box.map50)
    g = r.guarda
    nomes = np.array([x[0] for x in g])
    n_gt = np.array([len(x[4]) for x in g], dtype=np.int32)
    n_pred = np.array([len(x[2]) for x in g], dtype=np.int32)
    img_idx = np.repeat(np.arange(len(g), dtype=np.int32), n_pred)
    tp = np.concatenate([x[1].reshape(-1, 10) for x in g], 0).astype(bool)
    conf = np.concatenate([x[2] for x in g], 0).astype(np.float32)
    pred_cls = np.concatenate([x[3] for x in g], 0).astype(np.int16)
    target_cls = np.concatenate([x[4] for x in g], 0).astype(np.int16)
    assert int(n_gt.sum()) == len(target_cls)
    assert not target_cls.any() and not pred_cls.any(), "classe unica: tudo deveria ser classe 0"
    m50, m5095 = recalcula_map50(tp, conf, pred_cls.astype(float), target_cls.astype(float))
    np.savez_compressed(saida_npz, names=nomes, n_gt=n_gt, img_idx=img_idx, conf=conf, tp=tp, pred_cls=pred_cls)
    out = {"run": run, "pesos": pesos, "data": data, "imagens": len(g), "caixas_verdadeiras": int(n_gt.sum()),
           "predicoes": int(n_pred.sum()), "batch": batch, "fp16": False, "imgsz": imgsz,
           "mAP50_validador": round(map50_val, 5), "mAP50_recalculado": round(m50, 5),
           "mAP50_95_validador": round(float(r.box.map), 5), "mAP50_95_recalculado": round(m5095, 5),
           "dif_recalculado_validador": round(m50 - map50_val, 6),
           "P_validador": round(float(r.box.mp), 4), "R_validador": round(float(r.box.mr), 4),
           "quando": datetime.now().isoformat(timespec="seconds")}
    print(f"{run}: validador {map50_val:.5f}  recalculado {m50:.5f}  lote {batch}", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--imgsz", type=int, required=True)
    ap.add_argument("--modelos", nargs="+", required=True, help="runs em runs/detect")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--refaz", action="store_true")
    a = ap.parse_args()
    chk = os.path.join(AQUI, f"{a.tag}_reproducao.json")
    saida = json.load(open(chk, encoding="utf-8")) if os.path.exists(chk) else {}
    saida["protocolo"] = (f"{a.data}, divisao val, classe unica, imgsz {a.imgsz} (lado maior), conf 0,001, NMS IoU 0,7, "
                          "max_det 300, FP32, validador do Ultralytics 8.4.148")
    saida.setdefault("modelos", {})
    falhou = False
    for run in a.modelos:
        r = roda(run, a.data, a.tag, a.batch, a.imgsz, a.refaz)
        if r is not None:
            falhou |= bool(r.get("faltando"))
            saida["modelos"][run] = r
            with open(chk, "w", encoding="utf-8") as f:
                json.dump(saida, f, indent=1, ensure_ascii=False)
    with open(chk, "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=1, ensure_ascii=False)
    if falhou:
        print("AVISO: modelos sem pesos ficaram como 'faltando' no JSON (o bootstrap os deixa de fora)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
