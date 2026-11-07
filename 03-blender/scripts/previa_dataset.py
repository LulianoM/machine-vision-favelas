#!/usr/bin/env python3
"""
previa_dataset.py: monta uma folha de contato de um dataset YOLO, com as caixas desenhadas,
para conferir a olho se a anotação está no lugar certo.

Serve para duas coisas distintas, e é importante não confundi-las:
  1. Ver se a ANOTAÇÃO bate com a imagem (caixa em cima da pessoa, e não deslocada ou girada).
  2. Ver o tamanho REAL do alvo em pixel, que é o que decide se o treino vai funcionar. A 150 m
     com a Zenmuse Z30 uma pessoa de 1,7 m ocupa cerca de 17 px, e o menor stride do YOLO é 8.

Cor: verde para `pessoa_armada`, azul para `pessoa_desarmada`. Um recorte ampliado de cada caixa
vai no fim da folha, porque numa imagem inteira de 1920 px a caixa de 17 px não se enxerga.

Uso:
  python previa_dataset.py --ds C:\\arma3-favela\\blender\\ds_morro --n 6 --out previa.jpg
"""
import argparse
import glob
import os
import random

from PIL import Image, ImageDraw, ImageFont

CORES = {0: (60, 230, 90), 1: (80, 170, 255)}
NOMES = {0: "armada", 1: "desarmada"}

ap = argparse.ArgumentParser()
ap.add_argument("--ds", required=True, help="raiz do dataset (com images/ e labels/)")
ap.add_argument("--n", type=int, default=6, help="quantas imagens na folha")
ap.add_argument("--cols", type=int, default=3)
ap.add_argument("--larg", type=int, default=760, help="largura de cada celula na folha")
ap.add_argument("--crops", type=int, default=24, help="quantos recortes ampliados no fim")
ap.add_argument("--zoom", type=int, default=5)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--out", default="previa.jpg")
ap.add_argument("--en", action="store_true",
                help="rotulos em ingles e sem nome de arquivo (figura do artigo, pedido do autor em 30/09)")
args = ap.parse_args()

# a fonte bitmap padrao do PIL come os espacos em JPEG reduzido; na figura do artigo vai Arial
try:
    FONTE = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15) if args.en else None
    FONTE_P = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13) if args.en else None
except OSError:
    FONTE = FONTE_P = None

rng = random.Random(args.seed)
imgs = sorted(glob.glob(os.path.join(args.ds, "images", "*", "*.png")))
if not imgs:
    raise SystemExit(f"nenhuma imagem em {args.ds}")
esc = rng.sample(imgs, min(args.n, len(imgs)))


def rotulos_de(p):
    lp = p.replace(os.sep + "images" + os.sep, os.sep + "labels" + os.sep)
    lp = os.path.splitext(lp)[0] + ".txt"
    if not os.path.exists(lp):
        return []
    out = []
    for ln in open(lp, encoding="utf-8"):
        v = ln.split()
        if len(v) >= 5:
            out.append((int(v[0]), *(float(x) for x in v[1:5])))
    return out


celulas = []
recortes = []
n_cx = n_arm = 0
for p in esc:
    im = Image.open(p).convert("RGB")
    W, H = im.size
    rots = rotulos_de(p)
    n_cx += len(rots)
    n_arm += sum(1 for r in rots if r[0] == 0)
    # recortes ampliados ANTES de desenhar, para o zoom mostrar o pixel do alvo, nao a caixa
    for c, xc, yc, w, h in rots:
        x1, y1 = int((xc - w / 2) * W), int((yc - h / 2) * H)
        x2, y2 = int((xc + w / 2) * W), int((yc + h / 2) * H)
        m = 12
        cx = im.crop((max(0, x1 - m), max(0, y1 - m), min(W, x2 + m), min(H, y2 + m)))
        if cx.width < 3 or cx.height < 3:
            continue
        cz = cx.resize((cx.width * args.zoom, cx.height * args.zoom), Image.NEAREST)
        d2 = ImageDraw.Draw(cz)
        d2.rectangle([(x1 - max(0, x1 - m)) * args.zoom, (y1 - max(0, y1 - m)) * args.zoom,
                      (x2 - max(0, x1 - m)) * args.zoom, (y2 - max(0, y1 - m)) * args.zoom],
                     outline=CORES[c], width=2)
        recortes.append((cz, x2 - x1, y2 - y1, c))

    d = ImageDraw.Draw(im)
    for c, xc, yc, w, h in rots:
        x1, y1 = (xc - w / 2) * W, (yc - h / 2) * H
        x2, y2 = (xc + w / 2) * W, (yc + h / 2) * H
        # caixa folgada, para nao tapar o alvo de 17 px que se quer justamente enxergar
        d.rectangle([x1 - 4, y1 - 4, x2 + 4, y2 + 4], outline=CORES[c], width=3)
    esc_f = args.larg / W
    celulas.append((im.resize((args.larg, int(H * esc_f)), Image.LANCZOS),
                    (f"{len(rots)} boxes" if args.en else f"{os.path.basename(p)}  {len(rots)} caixas")))

cols = min(args.cols, len(celulas))
linhas = (len(celulas) + cols - 1) // cols
ch = celulas[0][0].height
FAIXA = 22
alt_grade = linhas * (ch + FAIXA)

rng.shuffle(recortes)
recortes = recortes[:args.crops]
alt_rec = max((c[0].height for c in recortes), default=0) + 34
larg_total = cols * args.larg
folha = Image.new("RGB", (larg_total, alt_grade + (alt_rec + 30 if recortes else 0)), (18, 18, 20))
dd = ImageDraw.Draw(folha)

for k, (im, cap) in enumerate(celulas):
    x = (k % cols) * args.larg
    y = (k // cols) * (ch + FAIXA)
    folha.paste(im, (x, y))
    dd.text((x + 6, y + ch + 3), cap, fill=(200, 200, 205), font=FONTE)

if recortes:
    y0 = alt_grade + 8
    dd.text((6, y0), (f"crops enlarged {args.zoom} times: green, armed; blue, unarmed "
                      f"(width by height in pixels of the original frame)") if args.en else
                     (f"recortes ampliados {args.zoom}x: verde = armada, azul = desarmada "
                      f"(largura x altura em pixel na imagem original)"), fill=(210, 210, 215),
            font=FONTE)
    x = 6
    y0 += 20
    for cz, w, h, c in recortes:
        if x + cz.width > larg_total - 6:
            break
        folha.paste(cz, (x, y0))
        dd.text((x, y0 + cz.height + 2), f"{w} by {h}" if args.en else f"{w}x{h}", fill=CORES[c],
                font=FONTE_P)
        x += cz.width + 10

folha.save(args.out, quality=92)
print(f"{len(esc)} imagens, {n_cx} caixas ({n_arm} armadas, {n_cx - n_arm} desarmadas)")
if recortes:
    ws = [r[1] for r in recortes]
    hs = [r[2] for r in recortes]
    print(f"alvo em pixel: largura {min(ws)} a {max(ws)}, altura {min(hs)} a {max(hs)}")
print(f"gravado {args.out}")
