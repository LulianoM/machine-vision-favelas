#!/usr/bin/env python3
"""
avalia_visdrone_oficial.py: os modelos avaliados no VisDrone val sob duas regras e tres limiares de IoU
(rodada 4, secoes 10.6 e 9 do artigo).

Por que existe. O validador do Ultralytics conta como falso positivo uma deteccao dentro de uma regiao
ignorada do VisDrone (categoria 0 da anotacao original: 1.378 regioes em 340 das 548 imagens de
validacao). O kit oficial nao conta: `dropObjectsInIgr.m` (VisDrone2018-DET-toolkit, utils) tira da
avaliacao toda caixa, verdadeira ou detectada, que tenha metade ou mais da area dentro de regiao
ignorada. Este script mede os dois jeitos com o MESMO validador do Ultralytics: a regra oficial entra
por uma subclasse que so filtra caixas antes do casamento, entao sem regioes ela reproduz o numero
padrao exatamente, e isso e conferido a cada execucao (campo `confere_padrao`).

Para cada modelo e cada regra: mAP50, AP a IoU 0,60 e 0,75 (checagem de convencao de anotacao da
secao 10.6: se a ordem dos modelos muda com o limiar, a comparacao e artefato de anotacao) e
mAP50-95. Todos com imgsz 1280, conf 0,001, classe unica: o protocolo de todos os numeros do artigo.

  python avalia_visdrone_oficial.py --modelos r_pareado s_nadir_4k s_oblvar --out visdrone_oficial_iou.json

Idempotente por modelo: um modelo que ja esta no arquivo de saida e pulado (--refaz para medir de novo).
"""
import argparse
import glob
import json
import os
from datetime import datetime

import numpy as np

RAIZ = os.path.join("C:" + os.sep, "arma3-favela")
DETECT = os.path.join(RAIZ, "blender", "runs", "detect")
VIS_YAML = os.path.join(RAIZ, "visdrone", "visdrone_yolo", "data.yaml")
ANOT = os.path.join(RAIZ, "visdrone", "VisDrone2019-DET-val", "annotations")
IMGS = os.path.join(RAIZ, "visdrone", "visdrone_yolo", "val", "images")


def mascaras():
    """nome da imagem -> mapa booleano das regioes ignoradas (so imagens que tem alguma)"""
    from PIL import Image
    out, n_reg = {}, 0
    for f in sorted(glob.glob(os.path.join(ANOT, "*.txt"))):
        nome = os.path.splitext(os.path.basename(f))[0]
        regs = []
        for ln in open(f, encoding="utf-8"):
            v = [x for x in ln.strip().split(",") if x != ""]
            if len(v) >= 6 and int(v[5]) == 0:
                regs.append(tuple(int(float(x)) for x in v[:4]))
        if not regs:
            continue
        im = os.path.join(IMGS, nome + ".jpg")
        if not os.path.exists(im):
            continue
        W, H = Image.open(im).size
        m = np.zeros((H, W), dtype=bool)
        for x, y, w, h in regs:
            m[max(0, y):min(H, y + h + 1), max(0, x):min(W, x + w + 1)] = True
        out[nome] = m
        n_reg += len(regs)
    return out, n_reg


def cobertura(m, caixas):
    """fracao da area de cada caixa (xyxy, pixels da imagem original) dentro das regioes ignoradas,
    com a area da caixa inteira no denominador, como no kit oficial"""
    H, W = m.shape
    ii = np.pad(m.astype(np.int64).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    fr = []
    for x1, y1, x2, y2 in caixas:
        w, h = max(1, round(x2 - x1)), max(1, round(y2 - y1))
        x, y = min(max(0, round(x1)), W - 1), min(max(0, round(y1)), H - 1)
        xb, yb = min(W, x + w), min(H, y + h)
        s = ii[yb, xb] - ii[y, xb] - ii[yb, x] + ii[y, x]
        fr.append(s / (w * h))
    return np.array(fr)


def validador(igr):
    from pathlib import Path

    from ultralytics.models.yolo.detect import DetectionValidator
    from ultralytics.utils import ops

    class ValidadorIgnoradas(DetectionValidator):
        """o validador padrao, mais o filtro do kit oficial antes do casamento"""

        def update_metrics(self, preds, batch):
            for si, pred in enumerate(preds):
                self.seen += 1
                pbatch = self._prepare_batch(si, batch)
                predn = self._prepare_pred(pred)
                m = igr.get(Path(pbatch["im_file"]).stem)
                if m is not None:
                    if pbatch["cls"].shape[0]:
                        nat = ops.scale_boxes(pbatch["imgsz"], pbatch["bboxes"].clone(), pbatch["ori_shape"],
                                              pbatch["ratio_pad"]).cpu().numpy()
                        fica = cobertura(m, nat) < 0.5
                        pbatch["cls"] = pbatch["cls"][fica]
                        pbatch["bboxes"] = pbatch["bboxes"][fica]
                    if predn["cls"].shape[0]:
                        nat = ops.scale_boxes(pbatch["imgsz"], predn["bboxes"].clone(), pbatch["ori_shape"],
                                              pbatch["ratio_pad"]).cpu().numpy()
                        fica = cobertura(m, nat) < 0.5
                        n = predn["cls"].shape[0]
                        predn = {k: (v[fica] if hasattr(v, "shape") and v.shape[:1] == (n,) else v)
                                 for k, v in predn.items()}
                cls = pbatch["cls"].cpu().numpy()
                sem = predn["cls"].shape[0] == 0
                self.metrics.update_stats({
                    **self._process_batch(predn, pbatch),
                    "target_cls": cls,
                    "target_img": np.unique(cls),
                    "conf": np.zeros(0) if sem else predn["conf"].cpu().numpy(),
                    "pred_cls": np.zeros(0) if sem else predn["cls"].cpu().numpy(),
                    "im_name": Path(pbatch["im_file"]).name,
                })

    return ValidadorIgnoradas


def mede(modelo, val_cls, imgsz):
    # lote padrao (16), o mesmo de avalia_sim2real.py: o agrupamento retangular depende do lote
    r = modelo.val(data=VIS_YAML, imgsz=imgsz, conf=0.001, single_cls=True, split="val",
                   plots=False, verbose=False, validator=val_cls)
    ap = np.asarray(r.box.all_ap)            # (classes, 10 limiares 0,50:0,05:0,95)
    return {"mAP50": round(float(r.box.map50), 4), "AP60": round(float(ap[:, 2].mean()), 4),
            "AP75": round(float(ap[:, 5].mean()), 4), "mAP50-95": round(float(r.box.map), 4),
            "P": round(float(r.box.mp), 4), "R": round(float(r.box.mr), 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", nargs="+", required=True, help="nomes em runs/detect")
    ap.add_argument("--out", required=True)
    ap.add_argument("--imgsz", type=int, default=1280)
    ap.add_argument("--refaz", action="store_true")
    a = ap.parse_args()

    from ultralytics import YOLO

    saida = {}
    if os.path.exists(a.out):
        saida = json.load(open(a.out, encoding="utf-8"))
    saida.setdefault("protocolo", "VisDrone val (548 imagens), classe unica, imgsz %d, conf 0,001; regra "
                     "oficial = dropObjectsInIgr.m do VisDrone2018-DET-toolkit (caixa verdadeira ou detectada "
                     "com metade ou mais da area em regiao ignorada sai da avaliacao)" % a.imgsz)
    saida.setdefault("modelos", {})
    igr, n_reg = mascaras()
    saida["regioes_ignoradas"] = {"regioes": n_reg, "imagens_com_regiao": len(igr)}
    vazio = validador({})
    oficial = validador(igr)
    for nome in a.modelos:
        if nome in saida["modelos"] and not a.refaz:
            print(f"{nome}: ja medido")
            continue
        p = os.path.join(DETECT, nome, "weights", "best.pt")
        if not os.path.exists(p):
            print(f"{nome}: sem pesos em {p}")
            continue
        m = YOLO(p)
        padrao = mede(m, None, a.imgsz)
        sub = mede(YOLO(p), vazio, a.imgsz)
        ofi = mede(YOLO(p), oficial, a.imgsz)
        saida["modelos"][nome] = {"pesos": p, "padrao_ultralytics": padrao, "regra_oficial": ofi,
                                  "confere_padrao": abs(sub["mAP50"] - padrao["mAP50"]) < 1e-4,
                                  "quando": datetime.now().isoformat(timespec="seconds")}
        print(f"{nome}: padrao {padrao}  oficial {ofi}  confere {saida['modelos'][nome]['confere_padrao']}",
              flush=True)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(saida, f, indent=1, ensure_ascii=False)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
