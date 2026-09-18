#!/usr/bin/env python3
"""
preview_deteccao.py: monta uma folha comparando a anotacao verdadeira com o que o detector previu,
em ladrilhos do conjunto de validacao. Verde = anotacao gerada no Blender. Vermelho = previsao de
pessoa armada. Azul = previsao de pessoa desarmada.

Uso:
  python preview_deteccao.py --pesos runs/detect/blender_v3_tiles/weights/best.pt \
      --data dataset_v3_tiles --out exemplo_treino.png --n 6 --conf 0.15
"""
import argparse, random
from pathlib import Path
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("--pesos", required=True)
ap.add_argument("--data", required=True)
ap.add_argument("--split", default="val")
ap.add_argument("--out", default="exemplo_treino.png")
ap.add_argument("--n", type=int, default=6)
ap.add_argument("--conf", type=float, default=0.15)
ap.add_argument("--zoom", type=int, default=640, help="lado do recorte centrado nas caixas")
ap.add_argument("--device", default="cpu")
ap.add_argument("--seed", type=int, default=3)
args = ap.parse_args()

from ultralytics import YOLO

root = Path(args.data)
imgs = sorted((root / "images" / args.split).glob("*.jpg")) + sorted((root / "images" / args.split).glob("*.png"))
com_caixa = []
for p in imgs:
    lbl = root / "labels" / args.split / (p.stem + ".txt")
    if lbl.exists() and lbl.read_text().strip():
        com_caixa.append((p, lbl))
random.Random(args.seed).shuffle(com_caixa)
sel = com_caixa[:args.n]
print(f"{len(com_caixa)} ladrilhos com anotacao, usando {len(sel)}")

modelo = YOLO(args.pesos)
CORES = {0: (255, 60, 60), 1: (60, 170, 255)}
NOMES = {0: "armada", 1: "desarmada"}
tiles = []
acertos = total_gt = total_pred = 0
for p, lbl in sel:
    im = Image.open(p).convert("RGB")
    W, H = im.size
    r = modelo.predict(source=str(p), conf=args.conf, imgsz=1280, device=args.device, verbose=False)[0]
    d = ImageDraw.Draw(im)
    gt = []
    for line in lbl.read_text().splitlines():
        if not line.strip():
            continue
        c, xc, yc, w, h = line.split()
        xc, yc, w, h = float(xc) * W, float(yc) * H, float(w) * W, float(h) * H
        box = (xc - w / 2, yc - h / 2, xc + w / 2, yc + h / 2)
        gt.append(box)
        d.rectangle(box, outline=(60, 230, 60), width=3)
    total_gt += len(gt)
    preds = []
    for b, cls, cf in zip(r.boxes.xyxy.tolist(), r.boxes.cls.tolist(), r.boxes.conf.tolist()):
        preds.append((b, int(cls), cf))
        d.rectangle(b, outline=CORES[int(cls)], width=2)
        d.text((b[0], max(0, b[1] - 11)), f"{NOMES[int(cls)]} {cf:.2f}", fill=CORES[int(cls)])
    total_pred += len(preds)
    for g in gt:
        for b, _, _ in preds:
            ix1, iy1 = max(g[0], b[0]), max(g[1], b[1])
            ix2, iy2 = min(g[2], b[2]), min(g[3], b[3])
            if ix2 > ix1 and iy2 > iy1:
                inter = (ix2 - ix1) * (iy2 - iy1)
                uni = (g[2] - g[0]) * (g[3] - g[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
                if uni > 0 and inter / uni > 0.3:
                    acertos += 1
                    break
    # recorte centrado na regiao com caixas, para a pessoa aparecer no tamanho util
    if gt:
        # centra na MAIOR caixa, nao na media: com caixas espalhadas a media cai no vazio entre elas
        g = max(gt, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
        cx, cy = (g[0] + g[2]) / 2, (g[1] + g[3]) / 2
    else:
        cx, cy = W / 2, H / 2
    z = args.zoom // 2
    x0 = int(min(max(cx - z, 0), W - 2 * z))
    y0 = int(min(max(cy - z, 0), H - 2 * z))
    tiles.append(im.crop((x0, y0, x0 + 2 * z, y0 + 2 * z)))

cols = 3
rows = (len(tiles) + cols - 1) // cols
S = 520
LEG = 46
sheet = Image.new("RGB", (cols * S, rows * S + LEG), (18, 18, 20))
for i, t in enumerate(tiles):
    sheet.paste(t.resize((S, S), Image.LANCZOS), ((i % cols) * S, LEG + (i // cols) * S))
d = ImageDraw.Draw(sheet)
d.rectangle((12, 14, 34, 30), outline=(60, 230, 60), width=3)
d.text((42, 17), "anotacao gerada no Blender", fill=(230, 230, 230))
d.rectangle((300, 14, 322, 30), outline=(255, 60, 60), width=3)
d.text((330, 17), "previsao: pessoa armada", fill=(230, 230, 230))
d.rectangle((600, 14, 622, 30), outline=(60, 170, 255), width=3)
d.text((630, 17), "previsao: pessoa desarmada", fill=(230, 230, 230))
d.text((900, 17), f"conf>={args.conf}  |  {acertos}/{total_gt} pessoas encontradas  |  {total_pred} previsoes", fill=(200, 200, 200))
sheet.save(args.out)
print(f"{args.out}: {acertos}/{total_gt} encontradas, {total_pred} previsoes")
