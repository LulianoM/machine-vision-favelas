#!/usr/bin/env python3
"""
Converte VisDrone-DET (VisDrone2019-DET-train / -val) para YOLO com classe única 'pessoa'
(pedestrian=1 e people=2 do VisDrone). Serve de conjunto real para medir sim-to-real.

Download (Ultralytics hospeda espelhos): https://docs.ultralytics.com/datasets/detect/visdrone/
Uso:
  python visdrone_to_yolo.py --src VisDrone2019-DET-val --out visdrone_yolo/val
  python visdrone_to_yolo.py --src VisDrone2019-DET-train --out visdrone_yolo/train --fracao 0.05
Depois escreva visdrone_yolo/data.yaml:
  path: <abs>/visdrone_yolo
  train: train/images
  val: val/images
  names: {0: pessoa}
"""
import argparse, random, shutil
from pathlib import Path
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--fracao", type=float, default=1.0)
ap.add_argument("--seed", type=int, default=42)
args = ap.parse_args()

src = Path(args.src); out = Path(args.out)
(out / "images").mkdir(parents=True, exist_ok=True)
(out / "labels").mkdir(parents=True, exist_ok=True)
imgs = sorted((src / "images").glob("*.jpg"))
random.Random(args.seed).shuffle(imgs)
imgs = imgs[: max(1, int(len(imgs) * args.fracao))]
n_box = 0
for p in imgs:
    ann = src / "annotations" / (p.stem + ".txt")
    with Image.open(p) as im:
        W, H = im.size
    linhas = []
    if ann.exists():
        for l in ann.read_text().splitlines():
            c = l.strip().split(",")
            if len(c) < 6:
                continue
            x, y, w, h, score, cat = map(int, c[:6])
            if cat not in (1, 2) or score == 0:   # score 0 = região ignorada
                continue
            linhas.append(f"0 {(x + w / 2) / W:.6f} {(y + h / 2) / H:.6f} {w / W:.6f} {h / H:.6f}")
    shutil.copy2(p, out / "images" / p.name)
    (out / "labels" / (p.stem + ".txt")).write_text("\n".join(linhas) + ("\n" if linhas else ""))
    n_box += len(linhas)
print(f"{len(imgs)} imagens, {n_box} caixas em {out}")
