"""
eval_cidade.py: avalia um modelo YOLO em imagens 4K inteiras com inferencia fatiada (ladrilhos 1280,
sobreposicao 0.2, NMS global). Mede deteccao (P/R/F1 a IoU 0.5, sem classe) e a separacao armado vs
desarmado (acuracia e matriz de confusao entre as caixas casadas), alem de mAP50 via ultralytics em
uma versao ladrilhada do conjunto. Gera previas com caixas previstas.

Uso: python eval_cidade.py --pesos runs/detect/cid150_s/weights/best.pt --data teste_angulos --out aval_angulos
"""
import argparse, json, glob, os, random
import numpy as np
from PIL import Image, ImageDraw
import torch
from ultralytics import YOLO
from torchvision.ops import nms

ap = argparse.ArgumentParser()
ap.add_argument("--pesos", required=True)
ap.add_argument("--data", required=True)
ap.add_argument("--split", default="val")
ap.add_argument("--out", required=True)
ap.add_argument("--tile", type=int, default=1280)
ap.add_argument("--overlap", type=float, default=0.2)
ap.add_argument("--conf", type=float, default=0.25)
ap.add_argument("--iou-match", type=float, default=0.5)
ap.add_argument("--device", default="0")
ap.add_argument("--previas", type=int, default=6)
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)
model = YOLO(args.pesos)
step = int(args.tile * (1 - args.overlap))


def iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0


def predict_full(im):
    W, H = im.size
    xs = list(range(0, max(1, W - args.tile + 1), step))
    ys = list(range(0, max(1, H - args.tile + 1), step))
    if xs[-1] + args.tile < W:
        xs.append(W - args.tile)
    if ys[-1] + args.tile < H:
        ys.append(H - args.tile)
    tiles, offs = [], []
    for ty in ys:
        for tx in xs:
            tiles.append(im.crop((tx, ty, tx + args.tile, ty + args.tile)))
            offs.append((tx, ty))
    boxes, scores, classes = [], [], []
    for k in range(0, len(tiles), 4):
        res = model.predict(tiles[k:k + 4], imgsz=args.tile, conf=args.conf, iou=0.5, device=args.device, verbose=False)
        for r, (tx, ty) in zip(res, offs[k:k + 4]):
            for b, s, c in zip(r.boxes.xyxy.cpu().numpy(), r.boxes.conf.cpu().numpy(), r.boxes.cls.cpu().numpy()):
                boxes.append([b[0] + tx, b[1] + ty, b[2] + tx, b[3] + ty]); scores.append(float(s)); classes.append(int(c))
    if not boxes:
        return []
    bt, st = torch.tensor(boxes), torch.tensor(scores)
    keep = nms(bt, st, 0.5).numpy()
    return [(boxes[i], scores[i], classes[i]) for i in keep]


imgs = sorted(glob.glob(os.path.join(args.data, "images", args.split, "*.jpg")) + glob.glob(os.path.join(args.data, "images", args.split, "*.png")))
TP = FP = FN = 0
conf_mat = np.zeros((2, 2), int)   # [gt][pred]
por_img = []
prev = []
rng = random.Random(3)
for p in imgs:
    im = Image.open(p).convert("RGB"); W, H = im.size
    lbl = os.path.join(args.data, "labels", args.split, os.path.splitext(os.path.basename(p))[0] + ".txt")
    gts = []
    if os.path.exists(lbl):
        for l in open(lbl):
            if l.strip():
                c, xc, yc, w, h = map(float, l.split())
                gts.append((int(c), [(xc - w / 2) * W, (yc - h / 2) * H, (xc + w / 2) * W, (yc + h / 2) * H]))
    preds = sorted(predict_full(im), key=lambda t: -t[1])
    usado = [False] * len(gts)
    tp = 0
    casados = []
    for b, s, c in preds:
        best, bi = 0, -1
        for j, (gc, gb) in enumerate(gts):
            if usado[j]:
                continue
            v = iou(b, gb)
            if v > best:
                best, bi = v, j
        if best >= args.iou_match:
            usado[bi] = True; tp += 1
            conf_mat[gts[bi][0]][c] += 1
            casados.append((gts[bi][0], c))
        else:
            FP += 1
    TP += tp; FN += len(gts) - tp
    por_img.append(dict(img=os.path.basename(p), gt=len(gts), pred=len(preds), tp=tp))
    if len(prev) < args.previas * 3:
        prev.append((p, gts, preds))

P = TP / max(1, TP + FP); R = TP / max(1, TP + FN); F1 = 2 * P * R / max(1e-9, P + R)
acc_cls = conf_mat.trace() / max(1, conf_mat.sum())
rec_armado = conf_mat[0][0] / max(1, conf_mat[0].sum())
rec_desarm = conf_mat[1][1] / max(1, conf_mat[1].sum())
res = dict(pesos=args.pesos, data=args.data, imagens=len(imgs), gt_total=TP + FN, TP=TP, FP=FP, FN=FN,
           precisao=round(P, 4), recall=round(R, 4), f1=round(F1, 4),
           acuracia_classe_entre_casadas=round(float(acc_cls), 4),
           recall_armado=round(float(rec_armado), 4), recall_desarmado=round(float(rec_desarm), 4),
           matriz_confusao_gt_x_pred=conf_mat.tolist(), conf=args.conf,
           gt_por_imagem=round((TP + FN) / max(1, len(imgs)), 1))
print(json.dumps(res, indent=2, ensure_ascii=False))
json.dump(dict(resumo=res, por_imagem=por_img), open(os.path.join(args.out, "resultado.json"), "w"), indent=2)

# previas: recorte 900x600 em torno das caixas, verde=desarmado previsto, vermelho=armado previsto, GT em tracejado branco
rng.shuffle(prev)
folha = []
for p, gts, preds in prev[:args.previas]:
    im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im)
    for gc, gb in gts:
        d.rectangle([gb[0] - 3, gb[1] - 3, gb[2] + 3, gb[3] + 3], outline=(255, 255, 255), width=1)
    for b, s, c in preds:
        col = (255, 40, 40) if c == 0 else (40, 220, 40)
        d.rectangle(b, outline=col, width=2)
        d.text((b[0], b[1] - 11), f"{'A' if c == 0 else 'D'} {s:.2f}", fill=col)
    if gts:
        xs = [g[1][0] for g in gts] + [g[1][2] for g in gts]; ys = [g[1][1] for g in gts] + [g[1][3] for g in gts]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    else:
        cx, cy = im.size[0] / 2, im.size[1] / 2
    cx = min(max(cx, 500), im.size[0] - 500); cy = min(max(cy, 350), im.size[1] - 350)
    folha.append(im.crop((int(cx - 500), int(cy - 350), int(cx + 500), int(cy + 350))))
if folha:
    cols = 2; rows = (len(folha) + 1) // 2
    S = Image.new("RGB", (1000 * cols, 700 * rows), (20, 20, 20))
    for i, f in enumerate(folha):
        S.paste(f, ((i % cols) * 1000, (i // cols) * 700))
    S.save(os.path.join(args.out, "previas.jpg"), quality=88)
    print("previas:", os.path.join(args.out, "previas.jpg"))
