#!/usr/bin/env python3
"""
build_quadra.py: gera geometria LIMPA de um recorte da favela a partir do modelo digital de
superficie (DSM) do OpenDroneMap, com paredes verdadeiramente VERTICAIS.

Por que isso existe: a malha de fotogrametria derrete as superficies quase verticais, porque o
MVS nao consegue reconstruir parede a partir de fotos em nadir. Mas o DSM tem a altura real de
cada ponto a 7,4 cm. Reconstruindo a superficie como degraus (cada celula vira um quadrilatero
horizontal na sua propria altura, e entre celulas vizinhas entra um quadrilatero vertical), a
parede sai reta e no lugar certo.

Depois disso a malha volta para o ODM no lugar de `odm_meshing/odm_mesh.ply`, e a etapa
`mvs_texturing` projeta as FOTOS REAIS sobre ela. Como agora a geometria da parede esta correta,
a projecao fica nitida em vez de esticada.

Saida: PLY binario no mesmo referencial do ODM (UTM menos o offset de odm_georeferencing/coords.txt).

Uso:
  python build_quadra.py --sector sudoeste --size 150 --res 0.25 --out quadra.ply
  python build_quadra.py --sector sudoeste --centro 40 -60 --size 150
"""
import argparse, os, json
import numpy as np
import rasterio
from rasterio.enums import Resampling
from scipy.ndimage import minimum_filter, uniform_filter

ap = argparse.ArgumentParser()
ap.add_argument("--sector", default="sudoeste")
ap.add_argument("--size", type=float, default=150.0, help="lado do recorte em metros")
ap.add_argument("--res", type=float, default=0.25, help="tamanho da celula em metros")
ap.add_argument("--centro", type=float, nargs=2, default=None, help="centro no referencial do ODM; sem isso escolhe a area mais densa")
ap.add_argument("--out", default=None)
ap.add_argument("--altura-min", type=float, default=2.0, help="altura acima do solo para contar como edificacao")
args = ap.parse_args()

root = os.path.join(r"C:\arma3-favela\odm", args.sector)
ox, oy = [float(v) for v in open(os.path.join(root, "odm_georeferencing", "coords.txt")).read().split("\n")[1].split()[:2]]
out = args.out or os.path.join(root, "quadra.ply")

# ----------------------------------------------------------------- DSM na resolucao pedida
with rasterio.open(os.path.join(root, "odm_dem", "dsm.tif")) as ds:
    b = ds.bounds
    W = int((b.right - b.left) / args.res)
    H = int((b.top - b.bottom) / args.res)
    z = ds.read(1, out_shape=(H, W), resampling=Resampling.average).astype(np.float32)
    nod = ds.nodata
mask = (z == nod) | ~np.isfinite(z) if nod is not None else ~np.isfinite(z)
if mask.any():
    from scipy.ndimage import distance_transform_edt
    _, (iy, ix) = distance_transform_edt(mask, return_indices=True)
    z = z[iy, ix]
z = z[::-1, :]          # linha 0 passa a ser o sul
mask = mask[::-1, :]
x0 = b.left - ox
y0 = b.bottom - oy
print(f"DSM: {W} x {H} celulas de {args.res} m, z {z.min():.1f}..{z.max():.1f}")

# ----------------------------------------------------------------- solo aproximado e altura das edificacoes
jan = max(3, int(40.0 / args.res))            # janela de 40 m: maior que qualquer quadra
solo = minimum_filter(z, size=jan, mode='nearest')
solo = uniform_filter(solo, size=jan // 2, mode='nearest')
altura = z - solo
print(f"altura acima do solo: mediana {np.median(altura):.1f} m, p99 {np.percentile(altura, 99):.1f} m")

# ----------------------------------------------------------------- escolhe o recorte mais denso
n = int(args.size / args.res)
if args.centro is None:
    ed = (altura > args.altura_min) & (~mask)
    dens = uniform_filter(ed.astype(np.float32), size=n, mode='constant')
    m = n // 2 + 1
    dens[:m, :] = dens[-m:, :] = dens[:, :m] = dens[:, -m:] = 0
    j, i = np.unravel_index(np.argmax(dens), dens.shape)[1], np.unravel_index(np.argmax(dens), dens.shape)[0]
    cx = x0 + j * args.res
    cy = y0 + i * args.res
    print(f"recorte escolhido automaticamente em ({cx:.0f}, {cy:.0f}), densidade {dens[i, j]*100:.0f}% de edificacao")
else:
    cx, cy = args.centro
    j = int((cx - x0) / args.res)
    i = int((cy - y0) / args.res)
i0, j0 = max(0, i - n // 2), max(0, j - n // 2)
i1, j1 = min(z.shape[0], i0 + n), min(z.shape[1], j0 + n)
zc = z[i0:i1, j0:j1]
hc = altura[i0:i1, j0:j1]
mc = mask[i0:i1, j0:j1]
gx0 = x0 + j0 * args.res
gy0 = y0 + i0 * args.res
R, C = zc.shape
print(f"recorte: {R} x {C} celulas, {R*args.res:.0f} x {C*args.res:.0f} m, canto ({gx0:.1f}, {gy0:.1f})")

# ----------------------------------------------------------------- malha em degraus
# cada celula vira um quadrilatero horizontal proprio (4 vertices nao compartilhados).
# entre celulas vizinhas com alturas diferentes entra um quadrilatero VERTICAL: a parede.
r = args.res
ii, jj = np.mgrid[0:R, 0:C]
xs = gx0 + jj * r
ys = gy0 + ii * r
zz = zc
# 4 cantos de cada celula, na ordem anti-horaria vista de cima
vx = np.stack([xs, xs + r, xs + r, xs], axis=-1).reshape(-1)
vy = np.stack([ys, ys, ys + r, ys + r], axis=-1).reshape(-1)
vz = np.repeat(zz.reshape(-1), 4)
base = np.arange(R * C) * 4
teto = np.stack([base, base + 1, base + 2, base + 3], axis=1)

paredes = []
# vizinho em +C (leste): cantos 1,2 da celula da esquerda encostam nos cantos 0,3 da direita
a = base.reshape(R, C)[:, :-1].reshape(-1)
bb = base.reshape(R, C)[:, 1:].reshape(-1)
dz = (zz[:, :-1] - zz[:, 1:]).reshape(-1)
sel = np.abs(dz) > 0.02
paredes.append(np.stack([a[sel] + 1, a[sel] + 2, bb[sel] + 3, bb[sel] + 0], axis=1))
# vizinho em +R (norte): cantos 3,2 da celula de baixo encostam nos cantos 0,1 da de cima
a = base.reshape(R, C)[:-1, :].reshape(-1)
bb = base.reshape(R, C)[1:, :].reshape(-1)
dz = (zz[:-1, :] - zz[1:, :]).reshape(-1)
sel = np.abs(dz) > 0.02
paredes.append(np.stack([a[sel] + 3, a[sel] + 2, bb[sel] + 1, bb[sel] + 0], axis=1))
faces = np.concatenate([teto] + paredes, axis=0)
verts = np.stack([vx, vy, vz], axis=1).astype(np.float32)
print(f"malha: {len(verts)} vertices, {len(faces)} faces ({len(teto)} de teto e chao, {len(faces)-len(teto)} de parede)")

# ----------------------------------------------------------------- grava PLY binario
with open(out, "wb") as f:
    f.write(b"ply\nformat binary_little_endian 1.0\n")
    f.write(f"element vertex {len(verts)}\n".encode())
    f.write(b"property float x\nproperty float y\nproperty float z\n")
    f.write(f"element face {len(faces)}\n".encode())
    f.write(b"property list uchar int vertex_indices\nend_header\n")
    f.write(verts.tobytes())
    fl = np.empty((len(faces), 1), dtype=np.uint8)
    fl[:] = 4
    rec = np.empty(len(faces), dtype=[("n", "u1"), ("v", "<i4", 4)])
    rec["n"] = 4
    rec["v"] = faces.astype(np.int32)
    f.write(rec.tobytes())
print(f"gravado {out} ({os.path.getsize(out)/1e6:.0f} MB)")
json.dump(dict(centro=[float(cx), float(cy)], canto=[float(gx0), float(gy0)], lado=float(args.size),
               res=float(args.res), R=int(R), C=int(C), offset=[ox, oy]),
          open(os.path.splitext(out)[0] + ".json", "w"), indent=1)
