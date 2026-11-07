#!/usr/bin/env python3
"""
Converte o log do ARMA 3 (.rpt com linhas DSIMG/DSLBL geradas por capturaDataset.sqf)
mais as screenshots em um dataset no formato YOLO (Ultralytics).

Uso:
  python rpt_to_yolo.py --out dataset_arma3
  python rpt_to_yolo.py --rpt "C:/Users/x/AppData/Local/Arma 3/arma3_2026-09-12_10-00-00.rpt" \
                        --screens "C:/Users/x/Documents/Arma 3/Screenshots" --out dataset_arma3 --val 0.15

Sem --rpt, usa o .rpt mais recente em %LOCALAPPDATA%/Arma 3.
Sem --screens, procura Documents/Arma 3/Screenshots e Documents/Arma 3 - Other Profiles/*/Screenshots.
"""
import argparse, glob, os, random, shutil, sys
from pathlib import Path

from PIL import Image

NOMES_CLASSES = ["pessoa_armada", "pessoa_desarmada"]


def rpt_mais_recente():
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Arma 3"
    rpts = sorted(base.glob("*.rpt"), key=lambda p: p.stat().st_mtime)
    return rpts[-1] if rpts else None


def pasta_screens():
    docs = Path.home() / "Documents"
    cands = [docs / "Arma 3" / "Screenshots"] + list((docs / "Arma 3 - Other Profiles").glob("*/Screenshots"))
    cands = [c for c in cands if c.exists()]
    if not cands:
        return None
    return max(cands, key=lambda p: p.stat().st_mtime)


def parse_rpt(caminho):
    imgs, labels = {}, {}
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        for linha in f:
            if "DSIMG|" in linha:
                campos = linha.split("DSIMG|", 1)[1].strip().split("|")
                nome = campos[0]
                imgs[nome] = campos
                labels.setdefault(nome, [])
            elif "DSLBL|" in linha:
                campos = linha.split("DSLBL|", 1)[1].strip().split("|")
                nome, cls = campos[0], int(campos[1])
                x1, y1, x2, y2 = map(float, campos[2:6])
                labels.setdefault(nome, []).append((cls, x1, y1, x2, y2))
    return imgs, labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rpt", default=None)
    ap.add_argument("--screens", default=None)
    ap.add_argument("--out", default="dataset_arma3")
    ap.add_argument("--val", type=float, default=0.15)
    ap.add_argument("--min-lado", type=float, default=0.004, help="descarta caixas menores (fração da tela)")
    ap.add_argument("--manter-vazias", action="store_true", help="inclui imagens sem anotação (negativos)")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rpt = Path(args.rpt) if args.rpt else rpt_mais_recente()
    screens = Path(args.screens) if args.screens else pasta_screens()
    if not rpt or not rpt.exists():
        sys.exit("RPT não encontrado. Passe --rpt.")
    if not screens or not screens.exists():
        sys.exit("Pasta de screenshots não encontrada. Passe --screens.")
    print(f"RPT: {rpt}\nScreenshots: {screens}")

    imgs, labels = parse_rpt(rpt)
    print(f"{len(imgs)} imagens no log, {sum(len(v) for v in labels.values())} caixas")

    pares = []
    faltando = 0
    for nome in imgs:
        src = screens / nome
        if not src.exists():
            faltando += 1
            continue
        caixas = [c for c in labels.get(nome, []) if (c[3] - c[1]) >= args.min_lado and (c[4] - c[2]) >= args.min_lado]
        if not caixas and not args.manter_vazias:
            continue
        pares.append((src, caixas))
    if faltando:
        print(f"aviso: {faltando} imagens do log não existem na pasta de screenshots")
    if not pares:
        sys.exit("Nenhum par imagem+anotação. Confira o RPT e a pasta.")

    random.Random(args.seed).shuffle(pares)
    n_val = max(1, int(len(pares) * args.val))
    splits = {"val": pares[:n_val], "train": pares[n_val:]}

    out = Path(args.out)
    for split, itens in splits.items():
        (out / "images" / split).mkdir(parents=True, exist_ok=True)
        (out / "labels" / split).mkdir(parents=True, exist_ok=True)
        for src, caixas in itens:
            dst = out / "images" / split / src.name
            shutil.copy2(src, dst)
            with Image.open(dst) as im:
                im.verify()
            with open(out / "labels" / split / (src.stem + ".txt"), "w") as f:
                for cls, x1, y1, x2, y2 in caixas:
                    xc, yc, w, h = (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1
                    f.write(f"{cls} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
        print(f"{split}: {len(itens)} imagens")

    with open(out / "data.yaml", "w") as f:
        f.write(f"path: {out.resolve().as_posix()}\ntrain: images/train\nval: images/val\n")
        f.write("names:\n" + "".join(f"  {i}: {n}\n" for i, n in enumerate(NOMES_CLASSES)))
    print(f"data.yaml escrito em {out / 'data.yaml'}")


if __name__ == "__main__":
    main()
