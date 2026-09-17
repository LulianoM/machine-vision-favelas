#!/usr/bin/env python3
"""
Desenha as caixas YOLO sobre N imagens para validar o alinhamento antes de treinar.
Uso: python preview_boxes.py --data dataset_arma3 --n 10 --out preview
Se as caixas saírem deslocadas de forma sistemática (todas para um lado ou esticadas),
o problema é a conversão de safeZone no capturaDataset.sqf (DS_USA_SAFEZONE).
"""
import argparse, random
from pathlib import Path
from PIL import Image, ImageDraw

CORES = {0: (255, 40, 40), 1: (40, 200, 255)}

ap = argparse.ArgumentParser()
ap.add_argument("--data", default="dataset_arma3")
ap.add_argument("--split", default="train")
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--out", default="preview")
args = ap.parse_args()

imgs = sorted((Path(args.data) / "images" / args.split).glob("*.png"))
random.seed(0)
amostra = random.sample(imgs, min(args.n, len(imgs)))
Path(args.out).mkdir(exist_ok=True)
for p in amostra:
    im = Image.open(p).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    lbl = Path(args.data) / "labels" / args.split / (p.stem + ".txt")
    if lbl.exists():
        for linha in lbl.read_text().splitlines():
            c, xc, yc, w, h = linha.split()
            c = int(c); xc, yc, w, h = map(float, (xc, yc, w, h))
            x1, y1, x2, y2 = (xc - w / 2) * W, (yc - h / 2) * H, (xc + w / 2) * W, (yc + h / 2) * H
            d.rectangle([x1, y1, x2, y2], outline=CORES.get(c, (0, 255, 0)), width=3)
            d.text((x1, max(0, y1 - 12)), str(c), fill=CORES.get(c, (0, 255, 0)))
    im.save(Path(args.out) / p.name)
print(f"{len(amostra)} imagens em {args.out}/")
