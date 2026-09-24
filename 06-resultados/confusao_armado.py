#!/usr/bin/env python3
"""
confusao_armado.py: matriz de confusao por casamento de IoU, em imagem inteira, para os modelos de
tres classes (armada, desarmada, objeto), e recall por modelo de arma quando o manifest traz o tipo
de cada caixa.

Por que existe. Os numeros de confusao de 24/09 foram calculados num trecho de codigo digitado na
sessao, sobre ladrilhos, com casamento nao exclusivo. A regra do projeto e que numero so entra no
artigo com o comando que o gerou em 06-resultados. Este script e esse comando, e o protocolo passa
a ser o mesmo para todos os modelos armados:

  - inferencia na imagem 4K inteira com imgsz 3840, ou seja na escala nativa em que os ladrilhos
    de treino foram cortados, sem reamostrar;
  - limiar de confianca 0,25 e IoU de casamento 0,50;
  - casamento um para um: pares (verdade, predicao) ordenados por IoU e atribuidos gulosamente,
    cada predicao usada uma vez so;
  - cada caixa verdadeira cai em uma de quatro colunas: chamada de armada, de desarmada, de objeto,
    ou perdida (nenhuma predicao com IoU >= 0,50).

Uso:
  python confusao_armado.py --pesos C:/arma3-favela/blender/runs/detect/armado_75/weights/best.pt \
      --ds C:/arma3-favela/blender/ds_armado_75 --split val --out confusao_armado_75.json
  --split todos usa treino e validacao juntos (so para corpus de teste que o modelo nunca viu).
"""
import argparse
import glob
import json
import os
from collections import Counter, defaultdict

NOMES = {0: "armada", 1: "desarmada", 2: "objeto", 3: "perdida"}


def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy
    return i / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i + 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pesos", required=True)
    ap.add_argument("--ds", required=True)
    ap.add_argument("--split", default="val", choices=["val", "train", "todos"])
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--iou", type=float, default=0.50)
    ap.add_argument("--imgsz", type=int, default=3840)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default=None, help="cpu para medir sem tirar a GPU de um render")
    a = ap.parse_args()

    from ultralytics import YOLO
    m = YOLO(a.pesos)

    meta = {}
    mf = os.path.join(a.ds, "manifest.jsonl")
    if os.path.exists(mf):
        for l in open(mf, encoding="utf-8"):
            r = json.loads(l)
            meta[os.path.splitext(r["img"])[0]] = r.get("caixas")

    splits = ["train", "val"] if a.split == "todos" else [a.split]
    imgs = sorted(p for s in splits for p in glob.glob(os.path.join(a.ds, "images", s, "*.png")))
    if not imgs:
        raise SystemExit("nenhuma imagem em " + a.ds)

    cm = Counter()
    tot = Counter()
    por_tipo = defaultdict(Counter)       # tipo -> Counter(coluna)
    fp_sem_par = Counter()                # predicoes que nao casaram com nenhuma verdade
    n_imgs = 0
    for p in imgs:
        base = os.path.splitext(os.path.basename(p))[0]
        split = os.path.basename(os.path.dirname(p))
        lab = os.path.join(a.ds, "labels", split, base + ".txt")
        if not os.path.exists(lab):
            continue
        r = m.predict(p, imgsz=a.imgsz, conf=a.conf, verbose=False, device=a.device)[0]
        W, H = r.orig_shape[1], r.orig_shape[0]
        gts = []
        for ln in open(lab):
            c, cx, cy, w, h = map(float, ln.split())
            gts.append((int(c), ((cx - w / 2) * W, (cy - h / 2) * H, (cx + w / 2) * W, (cy + h / 2) * H)))
        tipos = meta.get(base)
        if tipos is not None and len(tipos) != len(gts):
            tipos = None
        preds = list(zip(r.boxes.xyxy.tolist(), [int(c) for c in r.boxes.cls.tolist()]))
        pares = sorted(((iou(g[1], pb), gi, pi) for gi, g in enumerate(gts)
                        for pi, (pb, _) in enumerate(preds)), reverse=True)
        g_usado, p_usado, atrib = set(), set(), {}
        for v, gi, pi in pares:
            if v < a.iou:
                break
            if gi in g_usado or pi in p_usado:
                continue
            g_usado.add(gi)
            p_usado.add(pi)
            atrib[gi] = preds[pi][1]
        for gi, (c, _) in enumerate(gts):
            col = atrib.get(gi, 3)
            cm[(c, col)] += 1
            tot[c] += 1
            if tipos is not None and tipos[gi][1]:
                por_tipo[tipos[gi][1]][col] += 1
        for pi, (_, pc) in enumerate(preds):
            if pi not in p_usado:
                fp_sem_par[pc] += 1
        n_imgs += 1

    taxa = {NOMES[g]: {NOMES[c]: round(cm[(g, c)] / tot[g], 4) for c in range(4)} | {"n": tot[g]}
            for g in range(3) if tot[g]}
    tipo_out = {t: {NOMES[c]: cnt[c] for c in range(4)} | {"n": sum(cnt.values()),
                "chamada_de_armada": round(cnt[0] / max(1, sum(cnt.values())), 4)}
                for t, cnt in sorted(por_tipo.items())}
    # mAP e precisao/recall por classe no MESMO protocolo (imagem inteira, imgsz nativo), pelo
    # validador do Ultralytics. So para os splits que o data.yaml do corpus declara.
    val = None
    if a.split in ("val", "train") and os.path.exists(os.path.join(a.ds, "data.yaml")):
        rv = m.val(data=os.path.join(a.ds, "data.yaml"), split=a.split, imgsz=a.imgsz, batch=1,
                   conf=0.001, plots=False, verbose=False, device=a.device)
        nomes = rv.names
        val = {"mAP50": round(float(rv.box.map50), 4), "mAP50-95": round(float(rv.box.map), 4),
               "por_classe": {nomes[int(c)]: {"P": round(float(rv.box.p[i]), 4),
                                               "R": round(float(rv.box.r[i]), 4),
                                               "mAP50": round(float(rv.box.ap50[i]), 4)}
                              for i, c in enumerate(rv.box.ap_class_index)}}
    saida = dict(pesos=a.pesos, ds=a.ds, split=a.split, imagens=n_imgs, conf=a.conf, val_imagem_inteira=val,
                 iou_casamento=a.iou, imgsz=a.imgsz, protocolo="imagem inteira, casamento 1:1",
                 taxa_por_classe_real=taxa, por_tipo=tipo_out,
                 predicoes_sem_par={NOMES[c]: fp_sem_par[c] for c in range(3)})
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=1, ensure_ascii=False)
    for g, d in taxa.items():
        print(f"real {g:<10} n={d['n']:<4} " + " ".join(f"{k}={v:.2f}" for k, v in d.items() if k != "n"))
    for t, d in tipo_out.items():
        print(f"  tipo {t:<16} n={d['n']:<4} chamada de armada {d['chamada_de_armada']:.2f}")


if __name__ == "__main__":
    main()
