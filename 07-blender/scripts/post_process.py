#!/usr/bin/env python3
"""
post_process.py: aplica caracteristicas de camera real aos renders (PNG) e grava JPG.
  - leve desfoque de lente, ruido de sensor (mais forte nas sombras), aberracao cromatica,
    vinheta, neblina atmosferica sutil, compressao JPEG (qualidade 82 a 95)
Labels YOLO nao mudam (mesma geometria). Mantem os PNG em images_png/ se --keep-png.

Uso: python post_process.py --data dataset_v3 [--seed 1] [--keep-png]
"""
import argparse, random, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--keep-png", action="store_true")
ap.add_argument("--blur", type=float, nargs=2, default=[0.25, 0.8], help="faixa do desfoque gaussiano em px (use 0.8 1.4 para renders sobre a malha ODM, cuja textura vem de fotos 1080p)")
args = ap.parse_args()
rng = random.Random(args.seed)
root = Path(args.data)


def process(im, r):
    a = np.asarray(im).astype(np.float32) / 255.0
    H, W, _ = a.shape
    # neblina: mistura com cinza claro
    haze = r.uniform(0.02, 0.09)
    a = a * (1 - haze) + np.array([0.75, 0.78, 0.82]) * haze
    # aberracao cromatica: desloca R e B radialmente por 0 a 1.5 px
    k = r.uniform(0.0, 1.5)
    if k > 0.2:
        yy, xx = np.mgrid[0:H, 0:W]
        cx, cy = W / 2, H / 2
        dx, dy = (xx - cx) / W, (yy - cy) / H
        for ch, s in ((0, k), (2, -k)):
            sx = np.clip(xx + dx * s * 2, 0, W - 1).astype(np.int32)
            sy = np.clip(yy + dy * s * 2, 0, H - 1).astype(np.int32)
            a[..., ch] = a[..., ch][sy, sx]
    # vinheta
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    a *= (1 - r.uniform(0.05, 0.2) * rr ** 2)[..., None]
    # ruido de sensor (dependente do sinal)
    sig = r.uniform(0.004, 0.018)
    a += np.random.default_rng(r.randint(0, 10**9)).normal(0, 1, a.shape) * (sig * (1.2 - a.mean(axis=2, keepdims=True)))
    a = np.clip(a, 0, 1)
    out = Image.fromarray((a * 255).astype(np.uint8))
    out = out.filter(ImageFilter.GaussianBlur(r.uniform(args.blur[0], args.blur[1])))
    return out


n = 0
for split in ("train", "val"):
    d = root / "images" / split
    for png in sorted(d.glob("*.png")):
        im = Image.open(png).convert("RGB")
        out = process(im, rng)
        out.save(png.with_suffix(".jpg"), quality=rng.randint(82, 95), subsampling=0)
        if args.keep_png:
            k = root / "images_png" / split
            k.mkdir(parents=True, exist_ok=True)
            shutil.move(str(png), k / png.name)
        else:
            png.unlink()
        n += 1
print(f"{n} imagens processadas em {root}")
