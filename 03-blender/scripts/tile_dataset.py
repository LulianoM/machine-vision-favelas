#!/usr/bin/env python3
"""
tile_dataset.py: recorta um dataset YOLO de imagens grandes em ladrilhos, preservando o tamanho
em pixels dos objetos.

Por que isso importa aqui: as imagens saem em 4K (3840x2160) e uma pessoa a 100 m ocupa de 11 a 41 px.
Treinando com imgsz=1536 a imagem inteira encolhe 2,5 vezes e a pessoa vira de 4 a 16 px. O menor
stride do YOLO e 8, entao um alvo de 4 px praticamente nao existe para a rede. Recortando em
ladrilhos de 1280 px o alvo chega ao treino no tamanho original.

Uso:
  python tile_dataset.py --data dataset_v3 --out dataset_v3_tiles --tile 1280 --overlap 0.2
Opcoes:
  --keep-empty 0.05   fracao de ladrilhos sem nenhuma caixa que fica no conjunto (negativos)
  --min-vis 0.4       fracao minima da caixa original que precisa sobrar dentro do ladrilho
"""
import argparse, random, shutil
from pathlib import Path
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--tile", type=int, default=1280)
ap.add_argument("--overlap", type=float, default=0.2)
ap.add_argument("--keep-empty", type=float, default=0.05)
ap.add_argument("--min-vis", type=float, default=0.4)
ap.add_argument("--seed", type=int, default=1)
args = ap.parse_args()
rng = random.Random(args.seed)
src = Path(args.data)
dst = Path(args.out)
step = int(args.tile * (1 - args.overlap))

total_t = total_b = vazios = 0
for split in ("train", "val"):
    di = dst / "images" / split
    dl = dst / "labels" / split
    di.mkdir(parents=True, exist_ok=True)
    dl.mkdir(parents=True, exist_ok=True)
    imgs = sorted(list((src / "images" / split).glob("*.jpg")) + list((src / "images" / split).glob("*.png")))
    for p in imgs:
        im = Image.open(p).convert("RGB")
        W, H = im.size
        lbl = src / "labels" / split / (p.stem + ".txt")
        caixas = []
        if lbl.exists():
            for line in lbl.read_text().splitlines():
                if not line.strip():
                    continue
                c, xc, yc, w, h = line.split()
                xc, yc, w, h = float(xc) * W, float(yc) * H, float(w) * W, float(h) * H
                caixas.append((int(c), xc - w / 2, yc - h / 2, xc + w / 2, yc + h / 2))
        xs = list(range(0, max(1, W - args.tile + 1), step))
        ys = list(range(0, max(1, H - args.tile + 1), step))
        if xs[-1] + args.tile < W:
            xs.append(W - args.tile)
        if ys[-1] + args.tile < H:
            ys.append(H - args.tile)
        for tx in xs:
            for ty in ys:
                linhas = []
                for c, x1, y1, x2, y2 in caixas:
                    ix1, iy1 = max(x1, tx), max(y1, ty)
                    ix2, iy2 = min(x2, tx + args.tile), min(y2, ty + args.tile)
                    if ix2 <= ix1 or iy2 <= iy1:
                        continue
                    area_o = (x2 - x1) * (y2 - y1)
                    if area_o <= 0 or ((ix2 - ix1) * (iy2 - iy1)) / area_o < args.min_vis:
                        continue
                    cx = ((ix1 + ix2) / 2 - tx) / args.tile
                    cy = ((iy1 + iy2) / 2 - ty) / args.tile
                    bw = (ix2 - ix1) / args.tile
                    bh = (iy2 - iy1) / args.tile
                    linhas.append(f"{c} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
                if not linhas:
                    if rng.random() > args.keep_empty:
                        continue
                    vazios += 1
                nome = f"{p.stem}_{tx:05d}_{ty:05d}"
                im.crop((tx, ty, tx + args.tile, ty + args.tile)).save(di / (nome + ".jpg"), quality=92, subsampling=0)
                (dl / (nome + ".txt")).write_text("\n".join(linhas))
                total_t += 1
                total_b += len(linhas)
    print(f"{split}: {len(imgs)} imagens de origem")

yaml_src = src / "data.yaml"
nomes = "names:\n  0: pessoa_armada\n  1: pessoa_desarmada\n"
if yaml_src.exists():
    txt = yaml_src.read_text()
    if "names:" in txt:
        nomes = txt[txt.index("names:"):]
(dst / "data.yaml").write_text(f"path: {dst.resolve().as_posix()}\ntrain: images/train\nval: images/val\n{nomes}")
print(f"{total_t} ladrilhos de {args.tile} px, {total_b} caixas, {vazios} ladrilhos vazios mantidos")
print(f"data.yaml em {dst / 'data.yaml'}")
