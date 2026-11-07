#!/usr/bin/env python3
"""
segmenta_predios.py: extrai EDIFICACOES INDIVIDUAIS do modelo digital de superficie do OpenDroneMap
e grava um JSON com planta, altura de base, altura de topo, cor do telhado e objetos de laje.

Ideia: em vez de tentar consertar a malha de fotogrametria (que derrete parede porque as fotos sao
todas em nadir), reconstruir a cidade como SOLIDOS. A planta e a altura saem do dado medido, entao
sao reais; a parede vira plano vertical de verdade; o telhado recebe a foto do ortomosaico.

Etapas:
 1. terreno (DTM) por abertura morfologica do DSM: remove tudo que e menor que uma quadra
 2. altura acima do solo = DSM - DTM
 3. mascara de edificacao, limpeza morfologica
 4. separacao de predios colados por patamar de altura (favela e escadinha: vizinhos com lajes
    em cotas diferentes), depois componentes conexos por patamar
 5. vetorizacao da planta com cv2.findContours + approxPolyDP
 6. cor media do telhado amostrada do ortomosaico
 7. objetos de laje (caixa d'agua, casa de maquinas) por saliencia acima do plano do telhado

Uso:
  python segmenta_predios.py --sector sudoeste --size 220 --res 0.30 --out predios.json
"""
import argparse, json, os
import numpy as np
import cv2
import rasterio
from rasterio.enums import Resampling
from scipy.ndimage import minimum_filter, maximum_filter, uniform_filter, median_filter, label, find_objects

ap = argparse.ArgumentParser()
ap.add_argument("--sector", default="sudoeste")
ap.add_argument("--size", type=float, default=220.0)
ap.add_argument("--res", type=float, default=0.30)
ap.add_argument("--centro", type=float, nargs=2, default=None)
ap.add_argument("--out", default=None)
ap.add_argument("--h-min", type=float, default=2.2, help="altura minima acima do solo para ser edificacao")
ap.add_argument("--area-min", type=float, default=9.0, help="area minima da planta em m2")
ap.add_argument("--patamar", type=float, default=1.6, help="diferenca de cota que separa dois predios colados")
args = ap.parse_args()

root = os.path.join(r"C:\arma3-favela\odm", args.sector)
ox, oy = [float(v) for v in open(os.path.join(root, "odm_georeferencing", "coords.txt")).read().split("\n")[1].split()[:2]]
out = args.out or os.path.join(root, "predios.json")
r = args.res


def px(m):
    return max(1, int(round(m / r)))


# ----------------------------------------------------------------- DSM e ortomosaico no recorte
with rasterio.open(os.path.join(root, "odm_dem", "dsm.tif")) as ds:
    b = ds.bounds
    W = int((b.right - b.left) / r)
    H = int((b.top - b.bottom) / r)
    z = ds.read(1, out_shape=(H, W), resampling=Resampling.bilinear).astype(np.float32)
    nod = ds.nodata
vazio = (z == nod) | ~np.isfinite(z) if nod is not None else ~np.isfinite(z)
if vazio.any():
    from scipy.ndimage import distance_transform_edt
    _, (iy, ix) = distance_transform_edt(vazio, return_indices=True)
    z = z[iy, ix]
z = z[::-1, :]
vazio = vazio[::-1, :]
x0 = b.left - ox
y0 = b.bottom - oy
z = median_filter(z, size=3, mode='nearest')     # tira pontos isolados, preserva quina
print(f"DSM {W} x {H} a {r} m, z {z.min():.1f}..{z.max():.1f}")

# ----------------------------------------------------------------- terreno e altura
k = px(45.0)
solo = minimum_filter(z, size=k, mode='nearest')
solo = maximum_filter(solo, size=k, mode='nearest')       # abertura: remove predio, mantem relevo
solo = uniform_filter(solo, size=k // 2, mode='nearest')
alt = z - solo
print(f"altura acima do solo: mediana {np.median(alt):.1f} m, p95 {np.percentile(alt,95):.1f} m")

# ----------------------------------------------------------------- recorte
n = px(args.size)
if args.centro is None:
    dens = uniform_filter((alt > args.h_min).astype(np.float32), size=n, mode='constant')
    m = n // 2 + 1
    dens[:m, :] = dens[-m:, :] = dens[:, :m] = dens[:, -m:] = 0
    i, j = np.unravel_index(np.argmax(dens), dens.shape)
    print(f"recorte automatico: densidade {dens[i,j]*100:.0f}% de edificacao")
else:
    j = int((args.centro[0] - x0) / r)
    i = int((args.centro[1] - y0) / r)
i0, j0 = max(0, i - n // 2), max(0, j - n // 2)
zc, ac, vc = z[i0:i0 + n, j0:j0 + n], alt[i0:i0 + n, j0:j0 + n], vazio[i0:i0 + n, j0:j0 + n]
sc = solo[i0:i0 + n, j0:j0 + n]
gx0, gy0 = x0 + j0 * r, y0 + i0 * r
R, C = zc.shape
print(f"recorte {R}x{C} celulas = {R*r:.0f} x {C*r:.0f} m, canto ({gx0:.1f}, {gy0:.1f})")

# ----------------------------------------------------------------- ortomosaico do mesmo recorte
with rasterio.open(os.path.join(root, "odm_orthophoto", "odm_orthophoto.tif")) as od:
    ob = od.bounds
    ow = int((ob.right - ob.left) / r)
    oh = int((ob.top - ob.bottom) / r)
    rgb = od.read([1, 2, 3], out_shape=(3, oh, ow), resampling=Resampling.bilinear)
    rgb = np.moveaxis(rgb, 0, -1)[::-1, :, :]
    oj0 = int((gx0 - (ob.left - ox)) / r)
    oi0 = int((gy0 - (ob.bottom - oy)) / r)
    orto = rgb[max(0, oi0):max(0, oi0) + R, max(0, oj0):max(0, oj0) + C]
    if orto.shape[:2] != (R, C):
        pad = np.zeros((R, C, 3), np.uint8)
        pad[:orto.shape[0], :orto.shape[1]] = orto
        orto = pad
print(f"ortomosaico do recorte: {orto.shape}")

# ----------------------------------------------------------------- mascara de edificacao
ed = (ac > args.h_min) & (~vc)
ed = cv2.morphologyEx(ed.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
ed = cv2.morphologyEx(ed, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)).astype(bool)
print(f"cobertura de edificacao: {100*ed.mean():.0f}%")

# ----------------------------------------------------------------- separa predios colados por patamar
# Favela e escadinha: casas grudadas com lajes em cotas diferentes. Quantizando a altura em
# patamares e rotulando por patamar, cada laje vira um predio proprio.
q = np.where(ed, np.round(zc / args.patamar).astype(np.int32), -9999)
rot = np.zeros((R, C), np.int32)
prox = 1
for nivel in np.unique(q):
    if nivel == -9999:
        continue
    m = (q == nivel).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    nlab, lab = cv2.connectedComponents(m, connectivity=4)
    for c in range(1, nlab):
        sel = lab == c
        if sel.sum() * r * r < args.area_min:
            continue
        rot[sel] = prox
        prox += 1
print(f"{prox-1} edificacoes candidatas")

# ----------------------------------------------------------------- vetoriza cada predio
predios = []
descartados = 0
for pid in range(1, prox):
    sel = (rot == pid)
    area = sel.sum() * r * r
    if area < args.area_min:
        descartados += 1
        continue
    m = sel.astype(np.uint8)
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        continue
    cnt = max(cnts, key=cv2.contourArea)
    # simplifica: tolerancia de 1 celula, o suficiente para virar poligono de parede reta
    aprox = cv2.approxPolyDP(cnt, 1.2 * 1.0, True).reshape(-1, 2)
    if len(aprox) < 3:
        descartados += 1
        continue
    if len(aprox) > 14:      # planta muito recortada: usa o retangulo de area minima
        rect = cv2.minAreaRect(cnt)
        aprox = cv2.boxPoints(rect).astype(np.int32)
    poly = [[float(gx0 + (p[0] + 0.5) * r), float(gy0 + (p[1] + 0.5) * r)] for p in aprox]
    ztopo = float(np.percentile(zc[sel], 65))         # cota da laje, robusta a caixa d'agua
    zbase = float(np.percentile(sc[sel], 50))
    hh = ztopo - zbase
    if hh < args.h_min or hh > 40:
        descartados += 1
        continue
    cor = orto[sel].reshape(-1, 3).mean(axis=0) / 255.0 if orto[sel].size else np.array([0.5, 0.5, 0.5])
    # objetos de laje: saliencia entre 0,5 e 3 m acima da cota da laje, area pequena
    salto = sel & (zc > ztopo + 0.5) & (zc < ztopo + 3.0)
    obj = []
    if salto.sum() > 3:
        nl, lb = cv2.connectedComponents(salto.astype(np.uint8), connectivity=8)
        for c in range(1, nl):
            s2 = lb == c
            a2 = s2.sum() * r * r
            if not (0.4 < a2 < 9.0):
                continue
            yy, xx = np.nonzero(s2)
            obj.append(dict(x=float(gx0 + (xx.mean() + 0.5) * r), y=float(gy0 + (yy.mean() + 0.5) * r),
                            raio=float(np.sqrt(a2 / np.pi)), h=float(np.percentile(zc[s2], 80) - ztopo)))
    predios.append(dict(id=pid, poly=poly, z_topo=ztopo, z_base=zbase, altura=hh, area=float(area),
                        cor=[float(v) for v in cor], objetos=obj[:4]))

# ----------------------------------------------------------------- vegetacao
# verde no ortomosaico + altura acima do solo + fora da mascara de edificacao.
# Indice de excesso de verde: 2G - R - B, classico para separar copa de telhado.
o = orto.astype(np.float32)
verde = 2 * o[:, :, 1] - o[:, :, 0] - o[:, :, 2]
veg = (verde > 9) & (ac > 1.5) & (~ed) & (~vc)
veg = cv2.morphologyEx(veg.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
nlv, lbv = cv2.connectedComponents(veg, connectivity=8)
arvores = []
for c in range(1, nlv):
    s = lbv == c
    a2 = s.sum() * r * r
    if a2 < 2.0:
        continue
    yy, xx = np.nonzero(s)
    arvores.append(dict(x=float(gx0 + (xx.mean() + 0.5) * r), y=float(gy0 + (yy.mean() + 0.5) * r),
                        raio=float(np.sqrt(a2 / np.pi)), h=float(np.percentile(ac[s], 85))))
arvores.sort(key=lambda t: -t["raio"])
arvores = arvores[:400]
print(f"vegetacao: {len(arvores)} copas, raio mediano {np.median([a['raio'] for a in arvores]):.1f} m" if arvores else "vegetacao: nenhuma")

alturas = np.array([p["altura"] for p in predios])
print(f"{len(predios)} edificacoes ({descartados} descartadas)")
print(f"altura: mediana {np.median(alturas):.1f} m, p10 {np.percentile(alturas,10):.1f}, p90 {np.percentile(alturas,90):.1f}, max {alturas.max():.1f}")
print(f"objetos de laje detectados: {sum(len(p['objetos']) for p in predios)}")

# ----------------------------------------------------------------- grava terreno e ortomosaico do recorte
np.savez_compressed(os.path.join(root, "recorte_terreno.npz"), solo=sc.astype(np.float32), dsm=zc.astype(np.float32),
                    x0=gx0, y0=gy0, res=r, R=R, C=C)
cv2.imwrite(os.path.join(root, "recorte_orto.jpg"), cv2.cvtColor(orto[::-1, :, :], cv2.COLOR_RGB2BGR),
            [cv2.IMWRITE_JPEG_QUALITY, 95])
json.dump(dict(sector=args.sector, canto=[gx0, gy0], lado=args.size, res=r, R=R, C=C, offset=[ox, oy],
               predios=predios, arvores=arvores), open(out, "w"))
print(f"gravado {out} ({os.path.getsize(out)/1e6:.1f} MB), terreno em recorte_terreno.npz, foto em recorte_orto.jpg")
