"""
gen_jacarezinho.py  v3 (2026-09-11)
Dataset sintetico aereo (drone a ~100 m) sobre favela reconstruida a partir de dados reais:
  - footprints e vias do OpenStreetMap (Jacarezinho ou Rocinha), terreno SRTM 30 m
  - texturas PBR e ceus HDRI CC0 do Poly Haven (C:\arma3-favela\assets\polyhaven)
  - props CC0 do Poly Haven (arvores, caixotes, lixo, pneus, botijoes...)
  - pessoas realistas do MPFB (MakeHuman), riggadas e posadas, roupa procedural
  - anotacao automatica de bounding box 2D (YOLO) com teste de oclusao

Uso:
  blender -b --python gen_jacarezinho.py -- --area jacarezinho --out dataset_v3 --n 200 --res 3840 2160

Classes: 0 = pessoa_armada, 1 = pessoa_desarmada
"""
import bpy, bmesh, sys, os, math, random, json, argparse, time, colorsys
from mathutils import Vector, Euler, Matrix, noise
from bpy_extras.object_utils import world_to_camera_view
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people_mpfb as PM
PEOPLE = PM.PEOPLE


ASSETS = r"C:\arma3-favela\assets"

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--area", default="jacarezinho", choices=["jacarezinho", "rocinha"])
ap.add_argument("--out", default="dataset_v3")
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--start", type=int, default=1)
ap.add_argument("--res", type=int, nargs=2, default=[3840, 2160])
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--alt", type=float, default=100.0)
ap.add_argument("--alt-jitter", type=float, default=8.0)
ap.add_argument("--pitch", type=float, nargs=2, default=[55.0, 90.0])
ap.add_argument("--lens", type=float, nargs=2, default=[20.0, 30.0])
ap.add_argument("--people", type=int, nargs=2, default=[4, 9])
ap.add_argument("--prob-armado", type=float, default=0.5)
ap.add_argument("--min-vis", type=float, default=0.35)
ap.add_argument("--min-lado", type=float, default=0.002)
ap.add_argument("--val", type=float, default=0.15)
ap.add_argument("--radius", type=float, default=170.0, help="raio (m) de cidade construida em torno do centro da cena")
ap.add_argument("--rebuild-every", type=int, default=6)
ap.add_argument("--pool", type=int, default=6, help="humanos MPFB distintos por favela")
ap.add_argument("--no-people", action="store_true")
ap.add_argument("--save-blend", default=None)
ap.add_argument("--camera", default="generic", choices=["generic", "z30"],
                help="z30 = camera real da PCERJ (Zenmuse Z30 1080p, nadir, 150 m) como nas fotos de 2022")
args = ap.parse_args(argv)
if args.camera == "z30":
    args.res = [1920, 1080]
    args.alt = 150.0
    args.alt_jitter = 3.0
    args.pitch = [86.0, 90.0]
    args.lens = [4.3 * 36 / 5.37, 4.3 * 36 / 5.37]   # 4.3 mm em sensor de 5.37 mm  ->  ~28.8 mm equivalente

OUT = os.path.abspath(args.out)
for sp in ("train", "val"):
    os.makedirs(os.path.join(OUT, "images", sp), exist_ok=True)
    os.makedirs(os.path.join(OUT, "labels", sp), exist_ok=True)
rng = random.Random(args.seed)
T0 = time.time()


def log(*a):
    print(f"[gen {time.time() - T0:6.1f}s]", *a, flush=True)


# ================================================================= dados reais (OSM + SRTM)
def load_area(name):
    d = json.load(open(os.path.join(ASSETS, "osm", f"{name}.json"), encoding="utf-8"))
    srtm = json.load(open(os.path.join(ASSETS, "osm", f"{name}_srtm.json"), encoding="utf-8"))
    nodes = {e["id"]: (e["lon"], e["lat"]) for e in d["elements"] if e["type"] == "node"}
    lats = [v[1] for v in nodes.values()]
    lons = [v[0] for v in nodes.values()]
    lat0, lon0 = (min(lats) + max(lats)) / 2, (min(lons) + max(lons)) / 2
    kx = 111320 * math.cos(math.radians(lat0))
    ky = 111320

    def loc(lon, lat):
        return ((lon - lon0) * kx, (lat - lat0) * ky)

    buildings, roads = [], []
    for e in d["elements"]:
        if e["type"] != "way":
            continue
        tags = e.get("tags", {})
        pts = [loc(*nodes[i]) for i in e["nodes"] if i in nodes]
        if "building" in tags:
            if len(pts) > 1 and pts[0] == pts[-1]:
                pts = pts[:-1]
            # simplifica pontos muito proximos
            simp = [pts[0]]
            for p in pts[1:]:
                if math.hypot(p[0] - simp[-1][0], p[1] - simp[-1][1]) > 0.35:
                    simp.append(p)
            if len(simp) < 3:
                continue
            area = 0.5 * abs(sum(simp[i][0] * simp[(i + 1) % len(simp)][1] - simp[(i + 1) % len(simp)][0] * simp[i][1] for i in range(len(simp))))
            if area < 6:
                continue
            sa = 0.5 * sum(simp[i][0] * simp[(i + 1) % len(simp)][1] - simp[(i + 1) % len(simp)][0] * simp[i][1] for i in range(len(simp)))
            if sa < 0:
                simp.reverse()  # anti-horario
            lv = tags.get("building:levels")
            try:
                lv = int(float(lv)) if lv else None
            except ValueError:
                lv = None
            cx = sum(p[0] for p in simp) / len(simp)
            cy = sum(p[1] for p in simp) / len(simp)
            rmax = max(math.hypot(x - cx, y - cy) for x, y in simp)
            buildings.append(dict(poly=simp, area=area, levels=lv, cx=cx, cy=cy, r=rmax, kind=tags.get("building", "yes")))
        elif "highway" in tags and len(pts) > 1:
            roads.append(dict(pts=pts, kind=tags["highway"]))
    # grade SRTM
    glat, glon = srtm["grid_lat"], srtm["grid_lon"]
    elev = {}
    for la, lo, z in srtm["points"]:
        elev[(round(la, 5), round(lo, 5))] = z if z is not None else 0.0
    grid = [[elev.get((round(la, 5), round(lo, 5)), 0.0) for lo in glon] for la in glat]
    zmed = sorted(v for row in grid for v in row)[len(glat) * len(glon) // 2]
    return dict(buildings=buildings, roads=roads, lat0=lat0, lon0=lon0, kx=kx, ky=ky, glat=glat, glon=glon, grid=grid, zmed=zmed)


AREA = load_area(args.area)
log(f"area {args.area}: {len(AREA['buildings'])} edificacoes, {len(AREA['roads'])} vias")


def terrain_h(x, y):
    a = AREA
    lat = a["lat0"] + y / a["ky"]
    lon = a["lon0"] + x / a["kx"]
    glat, glon, g = a["glat"], a["glon"], a["grid"]
    fi = (lat - glat[0]) / (glat[1] - glat[0])
    fj = (lon - glon[0]) / (glon[1] - glon[0])
    i = min(max(int(fi), 0), len(glat) - 2)
    j = min(max(int(fj), 0), len(glon) - 2)
    ti = min(max(fi - i, 0), 1)
    tj = min(max(fj - j, 0), 1)
    z = (g[i][j] * (1 - ti) * (1 - tj) + g[i + 1][j] * ti * (1 - tj) + g[i][j + 1] * (1 - ti) * tj + g[i + 1][j + 1] * ti * tj)
    return z - a["zmed"] + noise.noise(Vector((x * 0.05, y * 0.05, 0))) * 0.25


# ================================================================= materiais PBR (Poly Haven)
PH = json.load(open(os.path.join(ASSETS, "polyhaven", "index.json")))
TEX_BY_CAT = {}
for n, e in PH["textures"].items():
    TEX_BY_CAT.setdefault(e["cat"], []).append(n)
SIZE_BY_CAT = {"brick": (1.0, 1.6), "concrete": (1.5, 2.5), "plaster": (1.5, 2.5), "roof_metal": (0.9, 1.4), "roof_tile": (1.4, 2.2), "laje": (2.0, 3.0), "ground": (4.0, 7.0)}
MAT_CACHE = {}


def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)


def load_img(rel, noncolor=False):
    p = os.path.join(ASSETS, "polyhaven", rel)
    img = bpy.data.images.load(p, check_existing=True)
    if noncolor:
        img.colorspace_settings.name = 'Non-Color'
    return img


def mat_pbr(texname, tint=None, tint_strength=0.0, grime=0.5, rough_add=0.0, metallic=0.0, size=None, paint=None, paint_strength=0.0):
    """material Principled com diff/rough/normal do Poly Haven, projecao BOX em coordenadas de mundo.
    tint multiplica (escurece/colore); paint mistura uma cor de tinta por cima (clareia, ex. laje caiada)"""
    key = (texname, tint, round(tint_strength, 2), round(grime, 2), paint, round(paint_strength, 2))
    if key in MAT_CACHE:
        return MAT_CACHE[key]
    e = PH["textures"][texname]
    m = bpy.data.materials.new(f"pbr_{texname}_{len(MAT_CACHE)}")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Metallic"].default_value = metallic
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    sz = size or rng.uniform(*SIZE_BY_CAT.get(e["cat"], (2, 3)))
    mp.inputs["Scale"].default_value = (1 / sz, 1 / sz, 1 / sz)
    mp.inputs["Location"].default_value = (rng.uniform(0, 10), rng.uniform(0, 10), rng.uniform(0, 10))
    mp.inputs["Rotation"].default_value = (0, 0, rng.choice([0, math.pi / 2]))
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    diff = nt.nodes.new("ShaderNodeTexImage")
    diff.image = load_img(e["diff"])
    diff.projection = 'BOX'
    diff.projection_blend = 0.25
    nt.links.new(mp.outputs["Vector"], diff.inputs["Vector"])
    color_out = diff.outputs["Color"]
    if tint is not None and tint_strength > 0:
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.inputs["Factor"].default_value = tint_strength
        mix.inputs[7].default_value = (tint[0], tint[1], tint[2], 1)
        nt.links.new(color_out, mix.inputs[6])
        color_out = mix.outputs[2]
    if paint is not None and paint_strength > 0:
        pm = nt.nodes.new("ShaderNodeMix")
        pm.data_type = 'RGBA'
        pm.blend_type = 'MIX'
        pm.inputs["Factor"].default_value = paint_strength
        pm.inputs[7].default_value = (paint[0], paint[1], paint[2], 1)
        nt.links.new(color_out, pm.inputs[6])
        color_out = pm.outputs[2]
    if grime > 0:
        gn = nt.nodes.new("ShaderNodeTexNoise")
        gn.inputs["Scale"].default_value = rng.uniform(0.15, 0.6)
        gn.inputs["Detail"].default_value = 6
        gr = nt.nodes.new("ShaderNodeValToRGB")
        gr.color_ramp.elements[0].position = 0.35
        gr.color_ramp.elements[0].color = (0.45, 0.42, 0.4, 1)
        gr.color_ramp.elements[1].position = 0.65
        gm = nt.nodes.new("ShaderNodeMix")
        gm.data_type = 'RGBA'
        gm.blend_type = 'MULTIPLY'
        gm.inputs["Factor"].default_value = grime
        nt.links.new(tc.outputs["Object"], gn.inputs["Vector"])
        nt.links.new(gn.outputs["Fac"], gr.inputs["Fac"])
        nt.links.new(color_out, gm.inputs[6])
        nt.links.new(gr.outputs["Color"], gm.inputs[7])
        color_out = gm.outputs[2]
    nt.links.new(color_out, bsdf.inputs["Base Color"])
    if "rough" in e:
        rg = nt.nodes.new("ShaderNodeTexImage")
        rg.image = load_img(e["rough"], True)
        rg.projection = 'BOX'
        rg.projection_blend = 0.25
        nt.links.new(mp.outputs["Vector"], rg.inputs["Vector"])
        if rough_add:
            ad = nt.nodes.new("ShaderNodeMath")
            ad.operation = 'ADD'
            ad.inputs[1].default_value = rough_add
            ad.use_clamp = True
            nt.links.new(rg.outputs["Color"], ad.inputs[0])
            nt.links.new(ad.outputs[0], bsdf.inputs["Roughness"])
        else:
            nt.links.new(rg.outputs["Color"], bsdf.inputs["Roughness"])
    else:
        bsdf.inputs["Roughness"].default_value = 0.85
    if "nor" in e:
        nr = nt.nodes.new("ShaderNodeTexImage")
        nr.image = load_img(e["nor"], True)
        nr.projection = 'BOX'
        nr.projection_blend = 0.25
        nt.links.new(mp.outputs["Vector"], nr.inputs["Vector"])
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = 0.8
        nt.links.new(nr.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    MAT_CACHE[key] = m
    return m


def mat_flat(name, color, rough=0.8, metallic=0.0, grime=0.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if grime > 0:
        tc = nt.nodes.new("ShaderNodeTexCoord")
        gn = nt.nodes.new("ShaderNodeTexNoise")
        gn.inputs["Scale"].default_value = rng.uniform(2, 8)
        gr = nt.nodes.new("ShaderNodeValToRGB")
        gr.color_ramp.elements[0].position = 0.3
        gr.color_ramp.elements[0].color = (0.5, 0.48, 0.45, 1)
        gr.color_ramp.elements[1].position = 0.7
        gm = nt.nodes.new("ShaderNodeMix")
        gm.data_type = 'RGBA'
        gm.blend_type = 'MULTIPLY'
        gm.inputs["Factor"].default_value = grime
        gm.inputs[6].default_value = (color[0], color[1], color[2], 1)
        nt.links.new(tc.outputs["Object"], gn.inputs["Vector"])
        nt.links.new(gn.outputs["Fac"], gr.inputs["Fac"])
        nt.links.new(gr.outputs["Color"], gm.inputs[7])
        nt.links.new(gm.outputs[2], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1)
    return m


def mat_ground():
    """chao: dois PBR (terra e asfalto/concreto) misturados por ruido grande"""
    m = bpy.data.materials.new("m_ground")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    outs = []
    for tn in (rng.choice([t for t in TEX_BY_CAT["ground"] if "dirt" in t or "mud" in t or "ground" in t]),
               rng.choice([t for t in TEX_BY_CAT["ground"] if "asphalt" in t or "road" in t or "pavement" in t or "rubble" in t])):
        e = PH["textures"][tn]
        mp = nt.nodes.new("ShaderNodeMapping")
        sz = rng.uniform(6, 10)
        mp.inputs["Scale"].default_value = (1 / sz, 1 / sz, 1 / sz)
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        d = nt.nodes.new("ShaderNodeTexImage")
        d.image = load_img(e["diff"])
        d.projection = 'BOX'
        nt.links.new(mp.outputs["Vector"], d.inputs["Vector"])
        r = nt.nodes.new("ShaderNodeTexImage")
        r.image = load_img(e["rough"], True) if "rough" in e else None
        r.projection = 'BOX'
        nt.links.new(mp.outputs["Vector"], r.inputs["Vector"])
        outs.append((d, r))
    # terceira camada: mato / grama rala (cor procedural)
    n1 = nt.nodes.new("ShaderNodeTexNoise")
    n1.inputs["Scale"].default_value = rng.uniform(0.02, 0.05)
    n1.inputs["Detail"].default_value = 6
    n1.inputs["Roughness"].default_value = 0.7
    nt.links.new(tc.outputs["Object"], n1.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.44
    ramp.color_ramp.elements[1].position = 0.56
    nt.links.new(n1.outputs["Fac"], ramp.inputs["Fac"])
    mc = nt.nodes.new("ShaderNodeMix")
    mc.data_type = 'RGBA'
    nt.links.new(ramp.outputs["Color"], mc.inputs["Factor"])
    nt.links.new(outs[0][0].outputs["Color"], mc.inputs[6])
    nt.links.new(outs[1][0].outputs["Color"], mc.inputs[7])
    n2 = nt.nodes.new("ShaderNodeTexNoise")
    n2.inputs["Scale"].default_value = rng.uniform(0.03, 0.08)
    n2.inputs["Detail"].default_value = 8
    n2.inputs["Roughness"].default_value = 0.75
    nt.links.new(tc.outputs["Object"], n2.inputs["Vector"])
    r2 = nt.nodes.new("ShaderNodeValToRGB")
    r2.color_ramp.elements[0].position = rng.uniform(0.55, 0.62)
    r2.color_ramp.elements[1].position = 0.7
    nt.links.new(n2.outputs["Fac"], r2.inputs["Fac"])
    grass = nt.nodes.new("ShaderNodeTexNoise")
    grass.inputs["Scale"].default_value = 3.0
    grass.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Object"], grass.inputs["Vector"])
    gr = nt.nodes.new("ShaderNodeValToRGB")
    g1 = hsv(rng.uniform(0.2, 0.28), rng.uniform(0.35, 0.6), rng.uniform(0.12, 0.25))
    g2 = hsv(rng.uniform(0.12, 0.2), rng.uniform(0.3, 0.55), rng.uniform(0.25, 0.4))
    gr.color_ramp.elements[0].color = (g1[0], g1[1], g1[2], 1)
    gr.color_ramp.elements[1].color = (g2[0], g2[1], g2[2], 1)
    nt.links.new(grass.outputs["Fac"], gr.inputs["Fac"])
    mg = nt.nodes.new("ShaderNodeMix")
    mg.data_type = 'RGBA'
    nt.links.new(r2.outputs["Color"], mg.inputs["Factor"])
    nt.links.new(mc.outputs[2], mg.inputs[6])
    nt.links.new(gr.outputs["Color"], mg.inputs[7])
    # escurece um pouco (sujeira geral)
    dk = nt.nodes.new("ShaderNodeMix")
    dk.data_type = 'RGBA'
    dk.blend_type = 'MULTIPLY'
    dk.inputs["Factor"].default_value = 1.0
    dk.inputs[7].default_value = (0.62, 0.6, 0.56, 1)
    nt.links.new(mg.outputs[2], dk.inputs[6])
    nt.links.new(dk.outputs[2], bsdf.inputs["Base Color"])
    mr = nt.nodes.new("ShaderNodeMix")
    mr.data_type = 'RGBA'
    nt.links.new(ramp.outputs["Color"], mr.inputs["Factor"])
    nt.links.new(outs[0][1].outputs["Color"], mr.inputs[6])
    nt.links.new(outs[1][1].outputs["Color"], mr.inputs[7])
    nt.links.new(mr.outputs[2], bsdf.inputs["Roughness"])
    return m


# ================================================================= construtor de malha em lote
class MeshBuilder:
    def __init__(self, name):
        self.name = name
        self.verts, self.faces, self.fmat, self.smooth, self.mats = [], [], [], [], []

    def _mi(self, mat):
        if mat not in self.mats:
            self.mats.append(mat)
        return self.mats.index(mat)

    def _add(self, faces, mi, smooth=False):
        for f in faces:
            self.faces.append(f)
            self.fmat.append(mi)
            self.smooth.append(smooth)

    def box(self, cx, cy, cz, sx, sy, sz, mat, rot=0.0, mat_top=None):
        c, s = math.cos(rot), math.sin(rot)
        b = len(self.verts)
        for dz in (-0.5, 0.5):
            for (dx, dy) in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
                x, y = dx * sx, dy * sy
                self.verts.append((cx + x * c - y * s, cy + x * s + y * c, cz + dz * sz))
        mi = self._mi(mat)
        mt = self._mi(mat_top) if mat_top else mi
        for f, m in (((0, 3, 2, 1), mi), ((4, 5, 6, 7), mt), ((0, 1, 5, 4), mi), ((1, 2, 6, 5), mi), ((2, 3, 7, 6), mi), ((3, 0, 4, 7), mi)):
            self.faces.append(tuple(b + i for i in f))
            self.fmat.append(m)
            self.smooth.append(False)

    def prism(self, poly, z0, z1, mat_side, mat_top, cap_bottom=False):
        n = len(poly)
        b = len(self.verts)
        for (x, y) in poly:
            self.verts.append((x, y, z0))
        for (x, y) in poly:
            self.verts.append((x, y, z1))
        ms, mt = self._mi(mat_side), self._mi(mat_top)
        for i in range(n):
            j = (i + 1) % n
            self._add([(b + i, b + j, b + n + j, b + n + i)], ms)
        self._add([tuple(b + n + i for i in range(n))], mt)
        if cap_bottom:
            self._add([tuple(b + i for i in reversed(range(n)))], ms)

    def seg(self, p0, p1, r, mat, n=6):
        """cilindro entre dois pontos 3D"""
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0
        L = d.length
        if L < 1e-4:
            return
        d.normalize()
        up = Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))
        u = d.cross(up).normalized()
        v = d.cross(u).normalized()
        b = len(self.verts)
        for p in (p0, p1):
            for k in range(n):
                a = 2 * math.pi * k / n
                q = p + u * (r * math.cos(a)) + v * (r * math.sin(a))
                self.verts.append((q.x, q.y, q.z))
        mi = self._mi(mat)
        for k in range(n):
            k2 = (k + 1) % n
            self._add([(b + k, b + k2, b + n + k2, b + n + k)], mi, True)
        self._add([tuple(b + k for k in range(n)), tuple(b + n + k for k in reversed(range(n)))], mi)

    def cyl(self, cx, cy, cz, r, h, mat, n=12):
        self.seg((cx, cy, cz - h / 2), (cx, cy, cz + h / 2), r, mat, n)

    def sphere(self, cx, cy, cz, r, mat, seg=10, rings=6, squash=1.0):
        b = len(self.verts)
        self.verts.append((cx, cy, cz - r * squash))
        for i in range(1, rings):
            phi = math.pi * i / rings
            for j in range(seg):
                th = 2 * math.pi * j / seg
                self.verts.append((cx + r * math.sin(phi) * math.cos(th), cy + r * math.sin(phi) * math.sin(th), cz - r * squash * math.cos(phi)))
        top = len(self.verts)
        self.verts.append((cx, cy, cz + r * squash))
        mi = self._mi(mat)
        for j in range(seg):
            self._add([(b, b + 1 + (j + 1) % seg, b + 1 + j)], mi, True)
        for i in range(rings - 2):
            r0 = b + 1 + i * seg
            r1 = r0 + seg
            for j in range(seg):
                self._add([(r0 + j, r0 + (j + 1) % seg, r1 + (j + 1) % seg, r1 + j)], mi, True)
        r0 = b + 1 + (rings - 2) * seg
        for j in range(seg):
            self._add([(r0 + j, r0 + (j + 1) % seg, top)], mi, True)

    def build(self):
        me = bpy.data.meshes.new(self.name)
        me.from_pydata(self.verts, [], self.faces)
        for m in self.mats:
            me.materials.append(m)
        if self.faces:
            me.polygons.foreach_set("material_index", self.fmat)
            me.polygons.foreach_set("use_smooth", self.smooth)
        me.update()
        o = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(o)
        return o


# ================================================================= biblioteca de props (glTF CC0)
LIB = {}


def load_props():
    col = bpy.data.collections.new("LIB")
    bpy.context.scene.collection.children.link(col)
    wanted = ["island_tree_01", "island_tree_02", "tree_small_02", "jacaranda_tree", "old_tyre", "plastic_crate_01", "plastic_monobloc_chair_01",
              "metal_trash_can", "trashbag", "cement_bag", "propane_tank", "small_lpg_tank", "wooden_crate_01", "barrel_03", "cardboard_box_01",
              "planter_pot_clay", "potted_plant_01", "wooden_ladder", "rusted_wheel_rim_01", "compost_bags", "weed_plant_02", "fern_02", "wild_rooibos_bush", "covered_car"]
    for n in wanted:
        p = PH["models"].get(n)
        if not p:
            continue
        before = set(bpy.data.objects)
        try:
            bpy.ops.import_scene.gltf(filepath=os.path.join(ASSETS, "polyhaven", p))
        except Exception as e:
            log("prop falhou", n, e)
            continue
        new = [o for o in bpy.data.objects if o not in before]
        sub = bpy.data.collections.new(f"LIB_{n}")
        col.children.link(sub)
        for o in new:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            sub.objects.link(o)
        LIB[n] = sub
    # exclui a biblioteca da view layer (as instancias continuam renderizando)
    bpy.context.view_layer.layer_collection.children["LIB"].exclude = True
    log(f"props: {len(LIB)} modelos")


PROPS = []


def prop(name, x, y, z, yaw=None, scale=1.0):
    if name not in LIB:
        return None
    o = bpy.data.objects.new(f"prop_{name}", None)
    o.instance_type = 'COLLECTION'
    o.instance_collection = LIB[name]
    o.location = (x, y, z)
    o.rotation_euler = (0, 0, rng.uniform(0, 2 * math.pi) if yaw is None else yaw)
    o.scale = (scale, scale, scale)
    bpy.context.scene.collection.objects.link(o)
    PROPS.append(o)
    return o


# ================================================================= cidade
BUILT = []   # edificacoes construidas: poly, ztop, floors, roof_poly (ultimo andar)
SCENE_CENTER = (0.0, 0.0)


def shrink_poly(poly, f, ox=0.0, oy=0.0):
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    return [(cx + (p[0] - cx) * f + ox, cy + (p[1] - cy) * f + oy) for p in poly]


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                inside = not inside
    return inside


def inside_building(x, y, margin=0.4):
    for b in BUILT:
        if abs(x - b["cx"]) > b["r"] + margin or abs(y - b["cy"]) > b["r"] + margin:
            continue
        if point_in_poly(x, y, b["poly"]):
            return b
        if margin > 0:
            for (px, py) in b["poly"]:
                if math.hypot(px - x, py - y) < margin:
                    return b
    return None


ROAD_W = {"primary": 10, "secondary": 9, "tertiary": 8, "trunk": 11, "residential": 6.5, "unclassified": 6, "service": 4.5,
          "living_street": 4.5, "pedestrian": 3, "footway": 2.2, "path": 1.8, "steps": 2.2, "cycleway": 2.5}


def seg_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L2))
    return math.hypot(px - (x1 + dx * t), py - (y1 + dy * t))


def densify(cx0, cy0, R):
    """preenche vazios do OSM com lotes procedurais alinhados ao vizinho real mais proximo"""
    osm = [b for b in AREA["buildings"] if math.hypot(b["cx"] - cx0, b["cy"] - cy0) < R + 20]
    segs = []
    for rd in AREA["roads"]:
        w = ROAD_W.get(rd["kind"], 4)
        pts = rd["pts"]
        for i in range(len(pts) - 1):
            if math.hypot(pts[i][0] - cx0, pts[i][1] - cy0) < R + 40:
                segs.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], w))
    extra = []
    step = 6.2
    gx0 = int((cx0 - R) / step)
    gy0 = int((cy0 - R) / step)
    for gi in range(gx0, gx0 + int(2 * R / step) + 1):
        for gj in range(gy0, gy0 + int(2 * R / step) + 1):
            x = gi * step + rng.uniform(-1.5, 1.5)
            y = gj * step + rng.uniform(-1.5, 1.5)
            if math.hypot(x - cx0, y - cy0) > R or rng.random() < 0.08:
                continue
            if any(math.hypot(x - b["cx"], y - b["cy"]) < b["r"] + 2.0 for b in osm):
                continue
            if any(seg_dist(x, y, *sg[:4]) < sg[4] / 2 + 2.0 for sg in segs):
                continue
            w, d = rng.uniform(5.0, 8.5), rng.uniform(5.0, 8.5)
            nb = min(osm, key=lambda b: math.hypot(x - b["cx"], y - b["cy"]), default=None)
            if nb is not None and math.hypot(x - nb["cx"], y - nb["cy"]) < 40:
                p0, p1 = nb["poly"][0], nb["poly"][1]
                ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + rng.uniform(-0.08, 0.08)
            else:
                ang = rng.uniform(0, math.pi)
            c, sn = math.cos(ang), math.sin(ang)
            corners = [(x + dx * w / 2 * c - dy * d / 2 * sn, y + dx * w / 2 * sn + dy * d / 2 * c) for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            if any(math.hypot(px - b["cx"], py - b["cy"]) < b["r"] + 0.3 for px, py in corners for b in osm):
                continue
            if any(math.hypot(x - e["cx"], y - e["cy"]) < (min(w, d) + min(e["w"], e["d"])) / 2 - 0.3 for e in extra):
                continue
            extra.append(dict(poly=corners, area=w * d, levels=None, cx=x, cy=y, r=math.hypot(w, d) / 2, kind="yes", w=w, d=d, synth=True))
    log(f"densificacao: +{len(extra)} lotes procedurais")
    return extra


def build_city():
    global BUILT, PROPS
    BUILT = []
    R = args.radius
    cx0, cy0 = SCENE_CENTER
    mats = {}
    mats["brick"] = [mat_pbr(t, grime=rng.uniform(0.3, 0.7)) for t in rng.sample(TEX_BY_CAT["brick"], 6)]
    mats["concrete"] = [mat_pbr(t, grime=rng.uniform(0.3, 0.7)) for t in rng.sample(TEX_BY_CAT["concrete"], 4)]
    paint_h = [0.12, 0.55, 0.08, 0.0, 0.33, 0.16, 0.6, 0.95, 0.1]
    mats["plaster"] = [mat_pbr(t, tint=hsv(rng.choice(paint_h) + rng.uniform(-0.03, 0.03), rng.uniform(0.3, 0.8), rng.uniform(0.5, 0.95)), tint_strength=rng.uniform(0.5, 0.9), grime=rng.uniform(0.3, 0.7)) for t in rng.sample(TEX_BY_CAT["plaster"], 6)]
    mats["metal"] = [mat_pbr(t, grime=rng.uniform(0.2, 0.5), metallic=0.3) for t in rng.sample(TEX_BY_CAT["roof_metal"], 4)]
    # fibrocimento claro / telha metalica pintada de branco ou cinza claro
    mats["metal"] += [mat_pbr(t, paint=hsv(0.0, 0.0, rng.uniform(0.45, 0.7)), paint_strength=rng.uniform(0.35, 0.65), grime=rng.uniform(0.4, 0.7), metallic=0.1) for t in rng.sample(TEX_BY_CAT["roof_metal"], 3)]
    mats["tile"] = [mat_pbr(t, tint=hsv(rng.uniform(0.02, 0.05), rng.uniform(0.6, 0.85), rng.uniform(0.35, 0.55)), tint_strength=rng.uniform(0.6, 0.9), grime=rng.uniform(0.3, 0.6)) for t in rng.sample(TEX_BY_CAT["roof_tile"], 3)]
    # lajes: concreto cru, ou pintadas de branco/cinza claro (muito comum nas fotos reais do Jacarezinho)
    mats["laje"] = [mat_pbr(t, grime=rng.uniform(0.4, 0.8)) for t in rng.sample(TEX_BY_CAT["laje"], 4)]
    mats["laje"] += [mat_pbr(t, paint=hsv(rng.uniform(0.08, 0.15), rng.uniform(0.0, 0.08), rng.uniform(0.5, 0.75)), paint_strength=rng.uniform(0.35, 0.65), grime=rng.uniform(0.4, 0.7)) for t in rng.sample(TEX_BY_CAT["laje"], 3)]
    mats["laje"] += [mat_pbr(t, paint=hsv(0.0, 0.0, rng.uniform(0.4, 0.55)), paint_strength=rng.uniform(0.3, 0.6), grime=rng.uniform(0.4, 0.7)) for t in rng.sample(TEX_BY_CAT["laje"], 2)]
    asph = [mat_pbr(t, grime=0.5, size=rng.uniform(4, 7)) for t in TEX_BY_CAT["ground"] if "asphalt" in t or "road" in t][:3]
    pav = [mat_pbr(t, grime=0.5, size=rng.uniform(3, 5)) for t in TEX_BY_CAT["ground"] if "pavement" in t or "rubble" in t or "gravel" in t][:3]
    m_tank_b = mat_flat("m_tank_b", (0.03, 0.14, 0.42), rough=0.4, grime=0.6)
    m_tank_k = mat_flat("m_tank_k", (0.02, 0.02, 0.02), rough=0.4, grime=0.3)
    m_tank_w = mat_flat("m_tank_w", (0.75, 0.75, 0.72), rough=0.5, grime=0.5)
    m_glass = mat_flat("m_glass", (0.02, 0.03, 0.05), rough=0.15, grime=0.0)
    m_frame = mat_flat("m_frame", (0.55, 0.55, 0.52), rough=0.6, grime=0.4)
    m_door = mat_flat("m_door", (0.15, 0.09, 0.05), rough=0.7, grime=0.3)
    m_rebar = mat_flat("m_rebar", (0.25, 0.12, 0.06), rough=0.9, metallic=0.3, grime=0.3)
    m_tarp = mat_flat("m_tarp", (0.05, 0.2, 0.7), rough=0.6, grime=0.3)
    m_dish = mat_flat("m_dish", (0.7, 0.7, 0.7), rough=0.5, metallic=0.4, grime=0.2)
    m_pole = mat_flat("m_pole", (0.45, 0.44, 0.42), rough=0.9, grime=0.4)
    m_wire = mat_flat("m_wire", (0.02, 0.02, 0.02), rough=0.7, grime=0.0)
    m_ac = mat_flat("m_ac", (0.85, 0.85, 0.83), rough=0.5, grime=0.3)
    m_line = mat_flat("m_line", (0.3, 0.3, 0.3), rough=0.8, grime=0.0)
    cloth_m = [mat_flat(f"m_cloth{i}", hsv(rng.random(), rng.uniform(0.3, 0.9), rng.uniform(0.3, 0.95)), rough=0.9, grime=0.1) for i in range(8)]
    car_m = [mat_flat(f"m_car{i}", rng.choice([(0.9, 0.9, 0.9), (0.05, 0.05, 0.05), (0.5, 0.5, 0.5), (0.6, 0.05, 0.05), (0.05, 0.1, 0.4), (0.7, 0.7, 0.72)]), rough=0.3, metallic=0.5, grime=0.3) for i in range(6)]
    m_tire = mat_flat("m_tire", (0.03, 0.03, 0.03), rough=0.9, grime=0.0)

    mb = MeshBuilder("cidade")
    mbw = MeshBuilder("janelas")
    extra = densify(cx0, cy0, R)
    # ---------------- edificacoes
    for b in AREA["buildings"] + extra:
        if math.hypot(b["cx"] - cx0, b["cy"] - cy0) > R:
            continue
        poly = b["poly"]
        zs = [terrain_h(x, y) for x, y in poly]
        z0 = min(zs) - 0.3
        big = b["area"] > 500 or b["kind"] in ("industrial", "warehouse", "retail")
        if b["levels"]:
            floors = max(1, min(b["levels"], 8))
        elif big:
            floors = rng.choice([1, 1, 2])
        else:
            floors = rng.choices([1, 2, 3, 4, 5], weights=[0.2, 0.37, 0.27, 0.12, 0.04])[0]
        r = rng.random()
        wall = rng.choice(mats["brick"]) if r < 0.55 else (rng.choice(mats["concrete"]) if r < 0.75 else rng.choice(mats["plaster"]))
        fh_base = rng.uniform(2.7, 3.1) if not big else rng.uniform(4.0, 6.0)
        ztop = z0
        cur = poly
        ox = oy = 0.0
        for f in range(floors):
            fh = fh_base + ((max(zs) - min(zs)) if f == 0 else 0)
            if f > 0 and rng.random() < 0.4 and len(cur) <= 12:
                fac = rng.uniform(0.55, 0.9)
                cur2 = shrink_poly(cur, fac, rng.uniform(-0.8, 0.8), rng.uniform(-0.8, 0.8))
                mb.prism(cur, ztop, ztop + 0.12, rng.choice(mats["laje"]), rng.choice(mats["laje"]))  # laje exposta
                ztop += 0.12
                cur = cur2
            mwall = wall if rng.random() < 0.7 else rng.choice(mats["brick"] + mats["concrete"] + mats["plaster"])
            mb.prism(cur, ztop, ztop + fh, mwall, rng.choice(mats["laje"]))
            # janelas / portas / ar-condicionado nas fachadas
            n = len(cur)
            for i in range(n):
                x1, y1 = cur[i]
                x2, y2 = cur[(i + 1) % n]
                L = math.hypot(x2 - x1, y2 - y1)
                if L < 2.2:
                    continue
                ang = math.atan2(y2 - y1, x2 - x1)
                nx, ny = math.sin(ang), -math.cos(ang)  # normal externa (poligono anti-horario)
                k = max(1, int(L / rng.uniform(2.8, 4.0)))
                for w in range(k):
                    t = (w + 0.5) / k + rng.uniform(-0.08, 0.08)
                    px, py = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
                    if f == 0 and rng.random() < 0.3:
                        mbw.box(px + nx * 0.03, py + ny * 0.03, ztop + 1.05, 0.9, 0.06, 2.1, m_door, ang)
                    elif rng.random() < 0.8:
                        ww, wh = rng.uniform(0.8, 1.4), rng.uniform(0.9, 1.2)
                        mbw.box(px + nx * 0.02, py + ny * 0.02, ztop + 1.5, ww + 0.12, 0.05, wh + 0.12, m_frame, ang)
                        mbw.box(px + nx * 0.04, py + ny * 0.04, ztop + 1.5, ww, 0.05, wh, m_glass, ang)
                        if rng.random() < 0.12:
                            mbw.box(px + nx * 0.2 + math.cos(ang) * 0.9, py + ny * 0.2 + math.sin(ang) * 0.9, ztop + 2.0, 0.6, 0.35, 0.5, m_ac, ang)
            ztop += fh
        # ---------------- cobertura
        r = rng.random()
        roof_poly = cur
        if big or r < 0.42:
            if big:
                mb.prism(shrink_poly(roof_poly, 1.04), ztop, ztop + 0.12, rng.choice(mats["metal"]), rng.choice(mats["metal"]))
                ztop += 0.12
            else:
                mb.prism(shrink_poly(roof_poly, 1.04), ztop, ztop + 0.10, rng.choice(mats["metal"]), rng.choice(mats["metal"]))
                ztop += 0.10
                if rng.random() < 0.5:  # tijolos/pedras sobre a telha
                    for _ in range(rng.randint(2, 7)):
                        p = rng.choice(shrink_poly(roof_poly, rng.uniform(0.3, 0.9)))
                        mb.box(p[0], p[1], ztop + 0.08, 0.25, 0.12, 0.16, rng.choice(mats["brick"]), rng.uniform(0, 3))
        elif r < 0.85:
            laje = rng.choice(mats["laje"])
            mb.prism(roof_poly, ztop, ztop + 0.14, laje, laje)
            ztop += 0.14
            if rng.random() < 0.45:  # parapeito
                ph = rng.uniform(0.7, 1.1)
                n = len(roof_poly)
                for i in range(n):
                    x1, y1 = roof_poly[i]
                    x2, y2 = roof_poly[(i + 1) % n]
                    L = math.hypot(x2 - x1, y2 - y1)
                    ang = math.atan2(y2 - y1, x2 - x1)
                    nx, ny = math.sin(ang), -math.cos(ang)
                    mb.box((x1 + x2) / 2 - nx * 0.08, (y1 + y2) / 2 - ny * 0.08, ztop + ph / 2, L, 0.16, ph, wall, ang)
            if rng.random() < 0.35:  # colunas de espera (ferragem)
                for (px, py) in shrink_poly(roof_poly, 0.9):
                    if rng.random() < 0.7:
                        mb.seg((px, py, ztop), (px + rng.uniform(-0.05, 0.05), py + rng.uniform(-0.05, 0.05), ztop + rng.uniform(0.8, 1.6)), 0.05, m_rebar, 5)
            if rng.random() < 0.25:  # varal
                pts = shrink_poly(roof_poly, 0.6)
                if len(pts) >= 2:
                    a, c = pts[0], pts[len(pts) // 2]
                    mb.seg((a[0], a[1], ztop), (a[0], a[1], ztop + 1.8), 0.03, m_line, 5)
                    mb.seg((c[0], c[1], ztop), (c[0], c[1], ztop + 1.8), 0.03, m_line, 5)
                    mb.seg((a[0], a[1], ztop + 1.75), (c[0], c[1], ztop + 1.75), 0.008, m_line, 4)
                    for k in range(rng.randint(2, 6)):
                        t = rng.uniform(0.1, 0.9)
                        mb.box(a[0] + (c[0] - a[0]) * t, a[1] + (c[1] - a[1]) * t, ztop + 1.4, 0.45, 0.02, 0.6, rng.choice(cloth_m), math.atan2(c[1] - a[1], c[0] - a[0]))
            if rng.random() < 0.1:  # lona
                tp = shrink_poly(roof_poly, rng.uniform(0.4, 0.7), rng.uniform(-1, 1), rng.uniform(-1, 1))
                mb.prism(tp, ztop, ztop + 0.04, m_tarp, m_tarp)
        else:
            tl = rng.choice(mats["tile"])
            mb.prism(shrink_poly(roof_poly, 1.05), ztop, ztop + 0.25, tl, tl)
            ztop += 0.25
        # caixa d'agua
        if rng.random() < 0.45 and not big:
            p = rng.choice(shrink_poly(roof_poly, 0.5))
            tm = rng.choices([m_tank_b, m_tank_k, m_tank_w], weights=[0.45, 0.35, 0.2])[0]
            if rng.random() < 0.75:
                rr = rng.uniform(0.5, 0.75)
                mb.cyl(p[0], p[1], ztop + 0.5, rr, 1.0, tm, 14)
                mb.cyl(p[0], p[1], ztop + 1.03, rr * 1.06, 0.06, tm, 14)
            else:
                mb.box(p[0], p[1], ztop + 0.45, 1.2, 1.2, 0.9, tm, rng.uniform(0, 1))
        # antena parabolica
        if rng.random() < 0.3 and not big:
            p = rng.choice(shrink_poly(roof_poly, 0.7))
            mb.seg((p[0], p[1], ztop), (p[0], p[1], ztop + 1.2), 0.03, m_dish, 5)
            a = rng.uniform(0, 2 * math.pi)
            mb.seg((p[0], p[1], ztop + 1.2), (p[0] + math.cos(a) * 0.03, p[1] + math.sin(a) * 0.03, ztop + 1.25), 0.35, m_dish, 12)
        # tralha na laje (props)
        if rng.random() < 0.4 and not big:
            for _ in range(rng.randint(1, 4)):
                p = rng.choice(shrink_poly(roof_poly, rng.uniform(0.3, 0.8)))
                prop(rng.choice(["plastic_crate_01", "plastic_monobloc_chair_01", "old_tyre", "propane_tank", "small_lpg_tank", "cardboard_box_01", "wooden_crate_01",
                                 "barrel_03", "trashbag", "cement_bag", "planter_pot_clay", "potted_plant_01", "wooden_ladder", "rusted_wheel_rim_01", "compost_bags", "metal_trash_can"]), p[0], p[1], ztop)
        rmax = max(math.hypot(x - b["cx"], y - b["cy"]) for x, y in poly)
        BUILT.append(dict(poly=poly, roof=roof_poly, cx=b["cx"], cy=b["cy"], r=rmax, ztop=ztop, floors=floors, big=big))

    # ---------------- vias, postes, fiacao, carros
    mbr = MeshBuilder("vias")
    poles = []
    for rd in AREA["roads"]:
        pts = [p for p in rd["pts"] if math.hypot(p[0] - cx0, p[1] - cy0) < R + 40]
        if len(pts) < 2:
            continue
        w = ROAD_W.get(rd["kind"], 4)
        m = rng.choice(asph) if w >= 4.5 else rng.choice(pav)
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            L = math.hypot(x2 - x1, y2 - y1)
            if L < 0.5:
                continue
            nx, ny = -(y2 - y1) / L * w / 2, (x2 - x1) / L * w / 2
            q = [(x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x2 - nx, y2 - ny), (x2 + nx, y2 + ny)]
            b0 = len(mbr.verts)
            for (x, y) in q:
                mbr.verts.append((x, y, terrain_h(x, y) + 0.06))
            mbr._add([(b0, b0 + 1, b0 + 2, b0 + 3)], mbr._mi(m))
            # postes a cada ~28 m nas vias de carro
            if w >= 2.2:
                nseg = int(L / (28 if w >= 4.5 else 22))
                for k in range(nseg + (1 if rng.random() < L / 28 % 1 else 0)):
                    t = (k + rng.uniform(0.2, 0.8)) / max(1, nseg + 1)
                    side = 1 if (i + k) % 2 == 0 else -1
                    px, py = x1 + (x2 - x1) * t + nx * 1.15 * side, y1 + (y2 - y1) * t + ny * 1.15 * side
                    if inside_building(px, py, 0.3):
                        continue
                    pz = terrain_h(px, py)
                    mb.seg((px, py, pz), (px, py, pz + 8.5), 0.13, m_pole, 8)
                    mb.box(px, py, pz + 8.2, 1.4, 0.1, 0.12, m_pole, math.atan2(y2 - y1, x2 - x1) + math.pi / 2)
                    poles.append((px, py, pz + 8.3))
            # carros estacionados
            if w >= 4.5 and rng.random() < 0.5 and L > 8:
                for k in range(int(L / 30) + 1):
                    if rng.random() > 0.5:
                        continue
                    t = rng.uniform(0.1, 0.9)
                    side = rng.choice([1, -1])
                    cxp, cyp = x1 + (x2 - x1) * t + nx * (1 - 2.0 / w) * side, y1 + (y2 - y1) * t + ny * (1 - 2.0 / w) * side
                    if inside_building(cxp, cyp, 0.5):
                        continue
                    if rng.random() < 0.15:
                        prop("covered_car", cxp, cyp, terrain_h(cxp, cyp), math.atan2(y2 - y1, x2 - x1) + math.pi / 2)
                        continue
                    ang = math.atan2(y2 - y1, x2 - x1) + rng.uniform(-0.05, 0.05)
                    cz = terrain_h(cxp, cyp)
                    cm = rng.choice(car_m)
                    mb.box(cxp, cyp, cz + 0.62, 4.2, 1.75, 0.55, cm, ang)
                    mb.box(cxp + math.cos(ang) * -0.2, cyp + math.sin(ang) * -0.2, cz + 1.15, 2.1, 1.6, 0.55, m_glass if rng.random() < 0.5 else cm, ang, mat_top=cm)
                    for dx, dy in ((1.3, 0.85), (1.3, -0.85), (-1.3, 0.85), (-1.3, -0.85)):
                        wx = cxp + math.cos(ang) * dx - math.sin(ang) * dy
                        wy = cyp + math.sin(ang) * dx + math.cos(ang) * dy
                        mb.seg((wx - math.sin(ang) * 0.1, wy + math.cos(ang) * 0.1, cz + 0.32), (wx + math.sin(ang) * 0.1, wy - math.cos(ang) * 0.1, cz + 0.32), 0.32, m_tire, 10)
    # fiacao entre postes proximos e "gatos" dos postes para as lajes vizinhas
    def wire(p, q, r=0.012, sagm=1.0):
        prev = p
        for k in range(1, 5):
            t = k / 4
            sag = -math.sin(t * math.pi) * sagm
            cur = (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, p[2] + (q[2] - p[2]) * t + sag)
            mb.seg(prev, cur, r, m_wire, 4)
            prev = cur
    for i, p in enumerate(poles):
        cands = sorted(((math.hypot(q[0] - p[0], q[1] - p[1]), q) for q in poles[i + 1:] if 8 < math.hypot(q[0] - p[0], q[1] - p[1]) < 45), key=lambda t: t[0])[:2]
        for _, q in cands:
            for c in range(rng.randint(2, 4)):
                wire((p[0], p[1], p[2] - 0.15 * c), (q[0], q[1], q[2] - 0.15 * c), 0.012, rng.uniform(0.6, 1.2))
        near = sorted(((math.hypot(b["cx"] - p[0], b["cy"] - p[1]), b) for b in BUILT if math.hypot(b["cx"] - p[0], b["cy"] - p[1]) < 28), key=lambda t: t[0])[:rng.randint(2, 5)]
        for _, b in near:
            e = rng.choice(b["roof"])
            wire((p[0], p[1], p[2] - rng.uniform(0.3, 1.5)), (e[0], e[1], b["ztop"] + 0.3), 0.008, rng.uniform(0.3, 0.9))
    mbr.build()
    city = mb.build()
    mbw.build()
    # ---------------- arvores, lixo, mato
    for _ in range(int(len(BUILT) * 0.22) + 12):
        x, y = cx0 + rng.uniform(-R, R), cy0 + rng.uniform(-R, R)
        if inside_building(x, y, 1.2):
            continue
        prop(rng.choices(["island_tree_01", "island_tree_02", "tree_small_02", "jacaranda_tree"], weights=[0.4, 0.35, 0.22, 0.03])[0], x, y, terrain_h(x, y) - 0.1, scale=rng.uniform(0.9, 1.7))
    for _ in range(int(len(BUILT) * 0.9)):
        x, y = cx0 + rng.uniform(-R, R), cy0 + rng.uniform(-R, R)
        if inside_building(x, y, 0.3):
            continue
        prop(rng.choice(["trashbag", "old_tyre", "barrel_03", "plastic_crate_01", "cardboard_box_01", "weed_plant_02", "fern_02", "wild_rooibos_bush", "wooden_crate_01", "rusted_wheel_rim_01", "compost_bags", "metal_trash_can", "cement_bag"]), x, y, terrain_h(x, y))
    # sanidade: props com caixa envolvente grande demais (exceto arvores)
    for o in PROPS:
        if "tree" in o.name:
            continue
        pts = [ob.matrix_world @ Vector(c) for ob in o.instance_collection.objects if ob.type == 'MESH' for c in ob.bound_box]
        if pts:
            ext = max(max(p.x for p in pts) - min(p.x for p in pts), max(p.y for p in pts) - min(p.y for p in pts), max(p.z for p in pts) - min(p.z for p in pts)) * o.scale.x
            if ext > 5:
                log(f"AVISO prop grande: {o.name} {ext:.1f} m")
    log(f"cidade: {len(BUILT)} edificacoes, {len(poles)} postes, {len(PROPS)} props")
    return city


def build_terrain(size=900, step=4.0):
    cx0, cy0 = SCENE_CENTER
    bm = bmesh.new()
    n = int(size / step) + 1
    grid = []
    for i in range(n):
        row = []
        for j in range(n):
            x = cx0 - size / 2 + i * step
            y = cy0 - size / 2 + j * step
            row.append(bm.verts.new((x, y, terrain_h(x, y))))
        grid.append(row)
    for i in range(n - 1):
        for j in range(n - 1):
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
    me = bpy.data.meshes.new("terreno")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("terreno", me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat_ground())
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def clear_city():
    global PROPS
    for o in list(bpy.data.objects):
        if o.name in ("cidade", "vias", "janelas", "terreno") or o.name.startswith("prop_") or o.name.startswith("person_") or o.name.startswith("rig_") or o.name.startswith("gun_"):
            me = o.data
            bpy.data.objects.remove(o, do_unlink=True)
            if me is not None and isinstance(me, bpy.types.Mesh) and me.users == 0:
                bpy.data.meshes.remove(me)
    PROPS = []
    PEOPLE.clear()
    for m in list(bpy.data.materials):
        if m.users == 0 and m.name.startswith(("pbr_", "m_")):
            bpy.data.materials.remove(m)
    MAT_CACHE.clear()


# ================================================================= pessoas (MPFB, modulo people_mpfb)
def place_people(center, n, radius=32):
    PM.clear_people()
    placed = tries = 0
    while placed < n and tries < 500:
        tries += 1
        x = center[0] + rng.uniform(-radius, radius)
        y = center[1] + rng.uniform(-radius, radius)
        b = inside_building(x, y, 0.5)
        on_roof = False
        if b is not None:
            if b["big"] or rng.random() > 0.4 or not point_in_poly(x, y, shrink_poly(b["roof"], 0.8)):
                continue
            z = b["ztop"]
            on_roof = True
        else:
            z = terrain_h(x, y)
        if any(math.hypot(p["x"] - x, p["y"] - y) < 0.9 for p in PEOPLE):
            continue
        PM.make_person(rng, placed, x, y, z, rng.random() < args.prob_armado, on_roof)
        placed += 1
    return placed


# ================================================================= luz e camera
HDRIS = list(PH["hdris"].items())


def setup_world():
    w = bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    sky = nt.nodes.new("ShaderNodeTexSky")
    for st in ('MULTIPLE_SCATTERING', 'NISHITA', 'SINGLE_SCATTERING'):
        try:
            sky.sky_type = st
            break
        except TypeError:
            continue
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    mp = nt.nodes.new("ShaderNodeMapping")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    nt.links.new(sky.outputs["Color"], mix.inputs[6])
    nt.links.new(env.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], bg.inputs["Color"])
    sun = bpy.data.lights.new("Sun", type='SUN')
    so = bpy.data.objects.new("Sun", sun)
    bpy.context.scene.collection.objects.link(so)
    return dict(sky=sky, env=env, map=mp, mix=mix, bg=bg, sun=so)


def randomize_light(W):
    use_hdri = rng.random() < 0.35
    elev = math.radians(rng.uniform(22, 78))
    rot = rng.uniform(0, 2 * math.pi)
    info = dict(sun_elev=round(math.degrees(elev), 1), sun_az=round(math.degrees(rot), 1))
    if use_hdri:
        name, rel = rng.choice(HDRIS)
        W["env"].image = load_img(rel)
        W["map"].inputs["Rotation"].default_value = (0, 0, rng.uniform(0, 2 * math.pi))
        W["mix"].inputs["Factor"].default_value = 1.0
        overcast = "overcast" in name or "misty" in name or "cloudy" in name
        W["bg"].inputs["Strength"].default_value = rng.uniform(0.8, 1.3)
        W["sun"].data.energy = rng.uniform(0.3, 1.2) if overcast else rng.uniform(1.5, 3.0)
        W["sun"].data.angle = math.radians(rng.uniform(10, 25) if overcast else rng.uniform(1, 4))
        info.update(light="hdri", hdri=name, overcast=overcast)
    else:
        W["mix"].inputs["Factor"].default_value = 0.0
        for attr, val in (("sun_elevation", elev), ("sun_rotation", rot), ("altitude", 20), ("air_density", rng.uniform(0.9, 2.0)),
                          ("dust_density", rng.uniform(1.0, 6.0)), ("sun_intensity", 0.0), ("sun_size", math.radians(1.0))):
            try:
                setattr(W["sky"], attr, val)
            except Exception:
                pass
        W["bg"].inputs["Strength"].default_value = rng.uniform(0.1, 0.2)
        W["sun"].data.energy = rng.uniform(2.5, 4.5)
        W["sun"].data.angle = math.radians(rng.uniform(0.5, 2.5))
        info.update(light="sky", overcast=False)
    W["sun"].rotation_euler = Euler((math.pi / 2 - elev, 0, rot + math.pi), 'XYZ')
    bpy.context.scene.view_settings.exposure = rng.uniform(-0.8, -0.2)
    return info


def setup_camera():
    cam = bpy.data.cameras.new("DroneCam")
    cam.sensor_width = 36
    cam.sensor_fit = 'HORIZONTAL'
    co = bpy.data.objects.new("DroneCam", cam)
    bpy.context.scene.collection.objects.link(co)
    bpy.context.scene.camera = co
    return co


def place_camera(co, target):
    alt = args.alt + rng.uniform(-args.alt_jitter, args.alt_jitter)
    pitch = rng.uniform(args.pitch[0], args.pitch[1])
    yaw = rng.uniform(0, 2 * math.pi)
    lens = rng.uniform(args.lens[0], args.lens[1])
    co.data.lens = lens
    gz = terrain_h(target[0], target[1])
    dh = alt / math.tan(math.radians(pitch)) if pitch < 89.5 else 0
    co.location = (target[0] - math.cos(yaw) * dh, target[1] - math.sin(yaw) * dh, gz + alt)
    direction = Vector((target[0], target[1], gz)) - co.location
    co.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    co.rotation_euler.rotate_axis('Z', rng.uniform(-0.3, 0.3))
    return dict(alt=round(alt, 1), pitch=round(pitch, 1), yaw=round(math.degrees(yaw), 1), lens=round(lens, 1))


# ================================================================= anotacao
def person_points(p, depsgraph):
    return PM.person_points(p, depsgraph)


def bbox_2d(scene, co, pts):
    return PM.bbox_2d(scene, co, pts, args.min_lado)


def visibility(scene, co, p, pts, depsgraph, n=14):
    return PM.visibility(scene, co, p, pts, depsgraph, n)



# ================================================================= render
def setup_render(scene):
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.engine = 'CYCLES'
    scene.view_settings.view_transform = 'AgX'
    try:
        scene.view_settings.look = 'AgX - Medium High Contrast'
    except Exception:
        pass
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for bt in ('OPTIX', 'CUDA'):
        try:
            prefs.compute_device_type = bt
            prefs.get_devices()
            if any(d.type == bt for d in prefs.devices):
                for d in prefs.devices:
                    d.use = (d.type == bt)
                break
        except Exception:
            pass
    scene.cycles.device = 'GPU'
    scene.cycles.samples = args.samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = 'OPTIX'
    except Exception:
        pass
    scene.cycles.max_bounces = 4
    scene.cycles.diffuse_bounces = 2
    scene.cycles.glossy_bounces = 2
    scene.cycles.transparent_max_bounces = 8


# ================================================================= main
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
scene = bpy.context.scene
setup_render(scene)
W = setup_world()
cam = setup_camera()
load_props()
if not args.no_people:
    PM.build_pool(rng, args.pool, log)


def pick_center():
    """centro de cena dentro da regiao densa da area (perto de uma edificacao aleatoria)"""
    b = rng.choice(AREA["buildings"])
    return (b["cx"] + rng.uniform(-30, 30), b["cy"] + rng.uniform(-30, 30))


SCENE_CENTER = pick_center()
build_terrain()
build_city()

mf = open(os.path.join(OUT, "manifest.jsonl"), "a", encoding="utf-8")
tot = 0
for i in range(args.start, args.start + args.n):
    if i > args.start and (i - args.start) % args.rebuild_every == 0:
        clear_city()
        SCENE_CENTER = pick_center()
        build_terrain()
        build_city()
        if not args.no_people:
            PM.build_pool(rng, args.pool, log)
    center = (SCENE_CENTER[0] + rng.uniform(-40, 40), SCENE_CENTER[1] + rng.uniform(-40, 40))
    if not args.no_people:
        place_people(center, rng.randint(args.people[0], args.people[1]))
    light = randomize_light(W)
    caminfo = place_camera(cam, center)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    split = "val" if rng.random() < args.val else "train"
    name = f"jc_{i:06d}"
    labels = []
    for p in PEOPLE:
        pts = person_points(p, depsgraph)
        bb = bbox_2d(scene, cam, pts)
        if bb is None:
            continue
        vis = visibility(scene, cam, p, pts, depsgraph)
        if vis < args.min_vis:
            continue
        x1, y1, x2, y2 = bb
        labels.append((p["cls"], (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1, round(vis, 2), p["on_roof"]))
    scene.render.filepath = os.path.join(OUT, "images", split, name + ".png")
    tr = time.time()
    bpy.ops.render.render(write_still=True)
    with open(os.path.join(OUT, "labels", split, name + ".txt"), "w") as f:
        for l in labels:
            f.write(f"{l[0]} {l[1]:.6f} {l[2]:.6f} {l[3]:.6f} {l[4]:.6f}\n")
    rec = dict(img=name + ".png", split=split, w=args.res[0], h=args.res[1], area=args.area)
    rec.update(caminfo)
    rec.update(light)
    rec.update(n_people=len(PEOPLE), n_boxes=len(labels), n_armed=sum(1 for l in labels if l[0] == 0), n_roof=sum(1 for l in labels if l[6]),
               vis=[l[5] for l in labels], buildings=len(BUILT), seed=args.seed, render_s=round(time.time() - tr, 1))
    mf.write(json.dumps(rec) + "\n")
    mf.flush()
    tot += len(labels)
    log(f"{name} {split} caixas={len(labels)}/{len(PEOPLE)} alt={caminfo['alt']} pitch={caminfo['pitch']} luz={light['light']} render={rec['render_s']}s")
mf.close()
with open(os.path.join(OUT, "data.yaml"), "w") as f:
    f.write(f"path: {OUT.replace(os.sep, '/')}\ntrain: images/train\nval: images/val\nnames:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
if args.save_blend:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.save_blend))
log(f"fim: {args.n} imagens, {tot} caixas")
