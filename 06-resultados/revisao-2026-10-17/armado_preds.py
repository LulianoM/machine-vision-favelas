#!/usr/bin/env python3
"""
armado_preds.py: inferencia dos modelos de tres classes (armada, desarmada, objeto) em imagem 4K inteira,
na escala nativa (imgsz 3840), guardando TODAS as predicoes com confianca >= 0,05 (caixa, confianca,
classe) e as caixas verdadeiras de cada quadro, para a varredura de limiar de limiar_armado.py.

Por que guardar a 0,05 e filtrar depois: a NMS do Ultralytics (por classe, IoU 0,7) so suprime uma
caixa por outra de confianca MAIOR da mesma classe; as caixas abaixo do limiar nunca suprimem as de
cima. Logo, o conjunto de caixas com conf >= t que sobrevive a NMS rodada a 0,05 e o mesmo que
sobreviveria a NMS rodada a t (max_det 300 nunca e atingido nestes quadros). limiar_armado.py confere
isso reproduzindo, a conf 0,25, as taxas de confusao_armado_*.json ja publicadas.

Protocolo de confusao_armado.py: imagem inteira, imgsz 3840, casamento um para um por IoU >= 0,50
sem olhar a classe; cada pessoa recebe a classe da predicao com que casou. O casamento e feito em
limiar_armado.py, a partir do que este script guarda.

Revisao de 17/10/2026 (agente D2). So inferencia. Nao toca corpora odm, cid150 ou derivados da PCERJ.

  C:/arma3-favela/venv/Scripts/python.exe armado_preds.py --todos --fp16
"""
import argparse
import glob
import json
import os
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
DETECT = os.path.join(RAIZ, "runs", "detect")
CLASSES = {0: "armada", 1: "desarmada", 2: "objeto"}

# (nome no artigo, run, conjunto, corpus, split, arquivo de referencia em 06-resultados a conf 0,25)
# "val" = divisao de validacao do proprio corpus; "novos" = quadros que o modelo nunca viu.
CONJUNTOS = [
    ("S-nadir-75", "armado_75", "val", "ds_armado_75", "val", "confusao_armado_75.json"),
    ("S-nadir-75", "armado_75", "novos", "ds_armado_75_inedita", "todos", "holdout_armas_armado_75.json"),
    ("S-nadir-35 s0", "armado_35", "val", "ds_armado_35", "val", "confusao_armado_35.json"),
    ("S-nadir-35 s0", "armado_35", "novos", "ds_armado_35_extra", "val", "extra_armado_35.json"),
    ("S-nadir-35 s1", "armado_35_sd1", "val", "ds_armado_35", "val", "confusao_armado_35_sd1.json"),
    ("S-nadir-35 s1", "armado_35_sd1", "novos", "ds_armado_35_extra", "val", "extra_armado_35_sd1.json"),
    ("S-nadir-35 s2", "armado_35_sd2", "val", "ds_armado_35", "val", "confusao_armado_35_sd2.json"),
    ("S-nadir-35 s2", "armado_35_sd2", "novos", "ds_armado_35_extra", "val", "extra_armado_35_sd2.json"),
    ("Twin-75 s0", "armado_75g", "val", "ds_armado_75g", "val", "confusao_armado_75g.json"),
    ("Twin-75 s0", "armado_75g", "novos", "ds_armado_75g_extra", "val", "extra_armado_75g.json"),
    ("Twin-75 s1", "armado_75g_sd1", "val", "ds_armado_75g", "val", "confusao_armado_75g_sd1.json"),
    ("Twin-75 s1", "armado_75g_sd1", "novos", "ds_armado_75g_extra", "val", "extra_armado_75g_sd1.json"),
    ("Twin-75 s2", "armado_75g_sd2", "val", "ds_armado_75g", "val", "confusao_armado_75g_sd2.json"),
    ("Twin-75 s2", "armado_75g_sd2", "novos", "ds_armado_75g_extra", "val", "extra_armado_75g_sd2.json"),
]


def quadros(ds, split):
    splits = ["train", "val"] if split == "todos" else [split]
    out = []
    for s in splits:
        for p in sorted(glob.glob(os.path.join(RAIZ, ds, "images", s, "*.png"))):
            base = os.path.splitext(os.path.basename(p))[0]
            lab = os.path.join(RAIZ, ds, "labels", s, base + ".txt")
            if os.path.exists(lab):
                out.append((base, s, p, lab))
    return out


def tipos_do_manifest(ds):
    meta = {}
    mf = os.path.join(RAIZ, ds, "manifest.jsonl")
    if os.path.exists(mf):
        for l in open(mf, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                meta[os.path.splitext(r["img"])[0]] = r.get("caixas")
    return meta


def roda(nome, run, conjunto, ds, split, ref, conf_min, imgsz, fp16, refaz, out_dir=AQUI, device=None):
    saida = os.path.join(out_dir, f"preds_armado_{run}_{conjunto}.json")
    if os.path.exists(saida) and not refaz:
        print(f"{run} {conjunto}: ja guardado")
        return
    pesos = os.path.join(DETECT, run, "weights", "best.pt")
    if not os.path.exists(pesos):
        print(f"{run}: SEM PESOS em {pesos}")
        json.dump({"run": run, "conjunto": conjunto, "faltando": True, "pesos": pesos},
                  open(saida, "w", encoding="utf-8"), indent=1)
        return
    qs = quadros(ds, split)
    if not qs:
        print(f"{run} {conjunto}: SEM QUADROS em {ds}/{split}")
        json.dump({"run": run, "conjunto": conjunto, "faltando": True, "ds": ds}, open(saida, "w", encoding="utf-8"), indent=1)
        return
    from ultralytics import YOLO
    m = YOLO(pesos)
    meta = tipos_do_manifest(ds)
    kw = dict(imgsz=imgsz, conf=conf_min, iou=0.7, max_det=300, verbose=False, device=device)
    if fp16:
        kw["quantize"] = 16
    registros = []
    for base, s, img, lab in qs:
        r = m.predict(img, **kw)[0]
        W, H = r.orig_shape[1], r.orig_shape[0]
        gts = []
        for ln in open(lab):
            c, cx, cy, w, h = map(float, ln.split())
            # sem arredondar: um casamento na fronteira de IoU 0,50 muda com 0,01 px (achado de 17/10)
            gts.append([int(c), (cx - w / 2) * W, (cy - h / 2) * H, (cx + w / 2) * W, (cy + h / 2) * H])
        tipos = meta.get(base)
        if tipos is not None and len(tipos) != len(gts):
            tipos = None
        preds = [[float(x) for x in b] + [float(cf), int(c)]
                 for b, cf, c in zip(r.boxes.xyxy.tolist(), r.boxes.conf.tolist(), r.boxes.cls.tolist())]
        registros.append({"quadro": base, "split": s, "w": W, "h": H, "gt": gts,
                          "tipos": [t[1] for t in tipos] if tipos is not None else None,
                          "preds": preds})
    out = {"nome": nome, "run": run, "conjunto": conjunto, "pesos": pesos, "ds": os.path.join(RAIZ, ds), "split": split,
           "referencia_conf025": ref, "imgsz": imgsz, "conf_min": conf_min, "nms_iou": 0.7, "max_det": 300,
           "fp16": fp16, "quadros": len(registros), "caixas_verdadeiras": sum(len(q["gt"]) for q in registros),
           "predicoes": sum(len(q["preds"]) for q in registros), "max_predicoes_num_quadro": max(len(q["preds"]) for q in registros),
           "classes": CLASSES, "formato_pred": "x1, y1, x2, y2 (px da imagem), conf, classe",
           "formato_gt": "classe, x1, y1, x2, y2", "quando": datetime.now().isoformat(timespec="seconds"),
           "registros": registros}
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print(f"{run} {conjunto}: {len(registros)} quadros, {out['caixas_verdadeiras']} caixas, {out['predicoes']} predicoes "
          f"(max {out['max_predicoes_num_quadro']} num quadro)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--runs", nargs="*", default=[])
    ap.add_argument("--conf-min", type=float, default=0.05)
    ap.add_argument("--imgsz", type=int, default=3840)
    ap.add_argument("--fp16", action="store_true")
    ap.add_argument("--refaz", action="store_true")
    ap.add_argument("--out-dir", default=AQUI, help="outra pasta de saida (checagem de reproducao)")
    ap.add_argument("--device", default=None, help="cpu para conferir a arimetica do GPU")
    ap.add_argument("--conjuntos", nargs="*", default=None, help="val, novos")
    a = ap.parse_args()
    for nome, run, conjunto, ds, split, ref in CONJUNTOS:
        if a.todos or run in a.runs:
            if a.conjuntos and conjunto not in a.conjuntos:
                continue
            roda(nome, run, conjunto, ds, split, ref, a.conf_min, a.imgsz, a.fp16, a.refaz, a.out_dir, a.device)


if __name__ == "__main__":
    main()
