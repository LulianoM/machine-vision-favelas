#!/usr/bin/env python3
"""
export_dsm.py (venv, rasterio): prepara o terreno real 2.5D a partir das saidas do ODM.
  - DSM (7 cm) reamostrado para ~0.6 m, buracos preenchidos, convertido para o mesmo sistema
    de coordenadas do odm_textured_model_geo.obj (UTM menos offset de odm_georeferencing/coords.txt)
  - ortomosaico exportado como JPG de ate 8192 px para textura
  - confere o alinhamento vertical entre a malha ODM e o DSM
Saida: <setor>/dsm_grid.npz  e  <setor>/ortho_tex.jpg
Uso: python export_dsm.py --sector sudoeste [--step 8]
"""
import argparse, os, re, json
import numpy as np
import rasterio
from rasterio.enums import Resampling
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--sector", default="sudoeste")
ap.add_argument("--step", type=int, default=8, help="fator de reamostragem do DSM (8 x 7,4 cm = 0,59 m)")
ap.add_argument("--tex", type=int, default=8192)
args = ap.parse_args()
root = os.path.join(r"C:\arma3-favela\odm", args.sector)

# offset do ODM (obj = utm - offset)
txt = open(os.path.join(root, "odm_georeferencing", "coords.txt")).read().split("\n")
ox, oy = [float(v) for v in txt[1].split()[:2]]
print("offset", ox, oy)

with rasterio.open(os.path.join(root, "odm_dem", "dsm.tif")) as ds:
    H = ds.height // args.step
    W = ds.width // args.step
    z = ds.read(1, out_shape=(H, W), resampling=Resampling.average).astype(np.float32)
    nod = ds.nodata
    b = ds.bounds
    resx = (b.right - b.left) / W
    resy = (b.top - b.bottom) / H
mask = ~np.isfinite(z) if nod is None else (z == nod) | ~np.isfinite(z)
if mask.any():
    # preenche buracos com o valor valido mais proximo (transformada de distancia), depois suaviza so nos buracos
    from scipy.ndimage import distance_transform_edt, uniform_filter
    _, (iy, ix) = distance_transform_edt(mask, return_indices=True)
    zz = z[iy, ix]
    sm = uniform_filter(zz, size=9, mode='nearest')
    zz[mask] = sm[mask]
    z = zz
    print("buracos preenchidos:", int(mask.sum()), "de", mask.size)
# coordenadas no frame do obj: x cresce para leste, y para norte; linha 0 do raster e o norte
x0 = b.left - ox
y_top = b.top - oy
z = z[::-1, :]  # inverte para que a linha 0 seja o sul (y crescente)
mask = mask[::-1, :]
y0 = b.bottom - oy
print("grid", W, H, "res", round(resx, 3), round(resy, 3), "x0,y0", round(x0, 1), round(y0, 1), "z", float(np.nanmin(z)), float(np.nanmedian(z)), float(np.nanmax(z)))

# alinhamento vertical com a malha ODM: amostra vertices do obj e compara com o DSM
obj = os.path.join(root, "odm_texturing", "odm_textured_model_geo.obj")
vs = []
with open(obj, "r", errors="ignore") as f:
    for i, line in enumerate(f):
        if line.startswith("v "):
            p = line.split()
            vs.append((float(p[1]), float(p[2]), float(p[3])))
            if len(vs) >= 200000:
                break
vs = np.array(vs)
ix = ((vs[:, 0] - x0) / resx).astype(int)
iy = ((vs[:, 1] - y0) / resy).astype(int)
ok = (ix >= 0) & (ix < W) & (iy >= 0) & (iy < H)
d = vs[ok, 2] - z[iy[ok], ix[ok]]
dz = float(np.median(d))
print(f"obj z: {vs[:,2].min():.1f}..{vs[:,2].max():.1f}  diferenca obj-dsm mediana {dz:.2f} m (p10 {np.percentile(d,10):.2f}, p90 {np.percentile(d,90):.2f})")
np.savez_compressed(os.path.join(root, "dsm_grid.npz"), z=z + dz, x0=x0, y0=y0, resx=resx, resy=resy, W=W, H=H, ox=ox, oy=oy,
                    semdado=mask.astype(np.uint8))

with rasterio.open(os.path.join(root, "odm_orthophoto", "odm_orthophoto.tif")) as ds:
    f = max(1, int(np.ceil(max(ds.width, ds.height) / args.tex)))
    arr = ds.read([1, 2, 3], out_shape=(3, ds.height // f, ds.width // f), resampling=Resampling.average)
    im = Image.fromarray(np.moveaxis(arr, 0, -1))
    im.save(os.path.join(root, "ortho_tex.jpg"), quality=93, subsampling=0)
    ob = ds.bounds
    json.dump(dict(left=ob.left - ox, right=ob.right - ox, bottom=ob.bottom - oy, top=ob.top - oy, w=im.width, h=im.height),
              open(os.path.join(root, "ortho_tex.json"), "w"))
    print("ortho_tex", im.size)
print("ok")
