"""
gen_favela.py  v2 (2026-09-11)
Gera dataset sintetico aereo (drone a ~100 m) de uma favela procedural no Blender,
com pessoas (armadas / desarmadas) e anotacao automatica de bounding box 2D em formato YOLO.

Substitui o pipeline ARMA 3 (capturaDataset.sqf): mesma saida (imagens + labels YOLO +
manifesto por imagem), mas 100% headless e deterministico (seed).

Uso (headless):
  blender -b --python gen_favela.py -- --out dataset_blender --n 30 --res 3840 2160 \
        --samples 48 --engine CYCLES --seed 1 --alt 100 --alt-jitter 8 --pitch 60 90

Classes: 0 = pessoa_armada, 1 = pessoa_desarmada  (igual ao pipeline ARMA 3)
Labels: <out>/labels/<split>/<nome>.txt  (YOLO: cls xc yc w h, normalizado)
Manifesto: <out>/manifest.jsonl  (uma linha JSON por imagem: camera, sol, clima, contagens)
"""
import bpy, bmesh, sys, os, math, random, json, argparse, time, colorsys
from mathutils import Vector, Euler, noise
from bpy_extras.object_utils import world_to_camera_view

# ----------------------------------------------------------------- args
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="dataset_blender")
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--start", type=int, default=1)
ap.add_argument("--res", type=int, nargs=2, default=[3840, 2160])
ap.add_argument("--samples", type=int, default=48)
ap.add_argument("--engine", default="CYCLES", choices=["CYCLES", "BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"])
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--alt", type=float, default=100.0)
ap.add_argument("--alt-jitter", type=float, default=8.0)
ap.add_argument("--pitch", type=float, nargs=2, default=[60.0, 90.0])   # 90 = nadir
ap.add_argument("--lens", type=float, nargs=2, default=[20.0, 30.0])    # mm em sensor 36 mm (~24 mm eq. DJI)
ap.add_argument("--people", type=int, nargs=2, default=[3, 6])
ap.add_argument("--prob-armado", type=float, default=0.5)
ap.add_argument("--min-vis", type=float, default=0.35)
ap.add_argument("--min-lado", type=float, default=0.002)
ap.add_argument("--val", type=float, default=0.15)
ap.add_argument("--rebuild-every", type=int, default=8, help="regenera a favela a cada N imagens")
ap.add_argument("--save-blend", default=None)
args = ap.parse_args(argv)

OUT = os.path.abspath(args.out)
for sp in ("train", "val"):
    os.makedirs(os.path.join(OUT, "images", sp), exist_ok=True)
    os.makedirs(os.path.join(OUT, "labels", sp), exist_ok=True)
rng = random.Random(args.seed)


# ----------------------------------------------------------------- materiais
def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)


def _grime(nt, bsdf, color, strength=0.9, scale=None):
    """noise multiplicando a cor base (sujeira / manchas)"""
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = scale or rng.uniform(2, 12)
    tex.inputs["Detail"].default_value = 4
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.45, 0.42, 0.4, 1)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = strength
    mix.inputs[6].default_value = (color[0], color[1], color[2], 1)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    return mix


def mat_principled(name, color, rough=0.85, metallic=0.0, grime=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    _grime(nt, bsdf, color, grime)
    return m


def mat_brick(name):
    """tijolo aparente (baiano/ceramico), cor terracota"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.95
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = rng.uniform(3, 5)
    c1 = hsv(rng.uniform(0.02, 0.05), rng.uniform(0.6, 0.85), rng.uniform(0.28, 0.5))
    c2 = hsv(rng.uniform(0.02, 0.05), rng.uniform(0.55, 0.8), rng.uniform(0.2, 0.4))
    br.inputs["Color1"].default_value = (c1[0], c1[1], c1[2], 1)
    br.inputs["Color2"].default_value = (c2[0], c2[1], c2[2], 1)
    br.inputs["Mortar"].default_value = (0.32, 0.29, 0.26, 1)
    br.inputs["Mortar Size"].default_value = 0.02
    br.inputs["Bias"].default_value = rng.uniform(-0.3, 0.3)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    # sujeira sobre o tijolo
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = rng.uniform(1.5, 6)
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.4, 0.38, 0.36, 1)
    ramp.color_ramp.elements[1].position = 0.7
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = 0.85
    nt.links.new(tc.outputs["Object"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(br.outputs["Color"], mix.inputs[6])
    nt.links.new(ramp.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    return m


def mat_corrugated(name, base, metallic=0.4, rough=None):
    """telha ondulada: fibrocimento (cinza) ou zinco (metalico, com ferrugem)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough if rough is not None else rng.uniform(0.45, 0.75)
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.inputs["Scale"].default_value = rng.uniform(5, 9)
    wave.wave_type = 'BANDS'
    wave.bands_direction = rng.choice(['X', 'Y'])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (base[0] * 0.55, base[1] * 0.55, base[2] * 0.55, 1)
    ramp.color_ramp.elements[1].color = (base[0], base[1], base[2], 1)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], wave.inputs["Vector"])
    nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"])
    # ferrugem / manchas
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = rng.uniform(1, 4)
    r2 = nt.nodes.new("ShaderNodeValToRGB")
    r2.color_ramp.elements[0].position = rng.uniform(0.35, 0.5)
    r2.color_ramp.elements[0].color = (0.30, 0.14, 0.07, 1)
    r2.color_ramp.elements[1].position = rng.uniform(0.55, 0.7)
    r2.color_ramp.elements[1].color = (1, 1, 1, 1)
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = rng.uniform(0.3, 1.0)
    nt.links.new(tc.outputs["Object"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Fac"], r2.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix.inputs[6])
    nt.links.new(r2.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    return m


def mat_ground(name):
    """chao: mistura de asfalto escuro, concreto e terra"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.95
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n1 = nt.nodes.new("ShaderNodeTexNoise")
    n1.inputs["Scale"].default_value = rng.uniform(0.05, 0.12)
    n1.inputs["Detail"].default_value = 6
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    e = ramp.color_ramp.elements
    e[0].position = 0.4
    a = hsv(rng.uniform(0.07, 0.1), rng.uniform(0.15, 0.45), rng.uniform(0.18, 0.3))   # terra
    b = hsv(0, 0, rng.uniform(0.12, 0.22))                                            # asfalto/concreto sujo
    e[0].color = (a[0], a[1], a[2], 1)
    e[1].position = 0.6
    e[1].color = (b[0], b[1], b[2], 1)
    n2 = nt.nodes.new("ShaderNodeTexNoise")
    n2.inputs["Scale"].default_value = rng.uniform(1.5, 4)
    r2 = nt.nodes.new("ShaderNodeValToRGB")
    r2.color_ramp.elements[0].position = 0.35
    r2.color_ramp.elements[0].color = (0.55, 0.55, 0.55, 1)
    r2.color_ramp.elements[1].position = 0.7
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = 0.9
    nt.links.new(tc.outputs["Object"], n1.inputs["Vector"])
    nt.links.new(tc.outputs["Object"], n2.inputs["Vector"])
    nt.links.new(n1.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(n2.outputs["Fac"], r2.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix.inputs[6])
    nt.links.new(r2.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    return m


# ----------------------------------------------------------------- geometria em lote (sem operadores)
class MeshBuilder:
    """acumula primitivas e gera um unico objeto com varios materiais"""

    def __init__(self, name):
        self.name = name
        self.verts = []
        self.faces = []
        self.fmat = []
        self.smooth = []
        self.mats = []

    def _mi(self, mat):
        if mat not in self.mats:
            self.mats.append(mat)
        return self.mats.index(mat)

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

    def cyl(self, cx, cy, cz, r, h, mat, n=10):
        b = len(self.verts)
        for dz in (-0.5, 0.5):
            for k in range(n):
                a = 2 * math.pi * k / n
                self.verts.append((cx + r * math.cos(a), cy + r * math.sin(a), cz + dz * h))
        mi = self._mi(mat)
        for k in range(n):
            k2 = (k + 1) % n
            self.faces.append((b + k, b + k2, b + n + k2, b + n + k))
            self.fmat.append(mi)
            self.smooth.append(True)
        self.faces.append(tuple(b + k for k in range(n)))
        self.fmat.append(mi)
        self.smooth.append(False)
        self.faces.append(tuple(b + n + k for k in range(n)))
        self.fmat.append(mi)
        self.smooth.append(False)

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
            self.faces.append((b, b + 1 + (j + 1) % seg, b + 1 + j))
            self.fmat.append(mi)
            self.smooth.append(True)
        for i in range(rings - 2):
            r0 = b + 1 + i * seg
            r1 = r0 + seg
            for j in range(seg):
                j2 = (j + 1) % seg
                self.faces.append((r0 + j, r0 + j2, r1 + j2, r1 + j))
                self.fmat.append(mi)
                self.smooth.append(True)
        r0 = b + 1 + (rings - 2) * seg
        for j in range(seg):
            self.faces.append((r0 + j, r0 + (j + 1) % seg, top))
            self.fmat.append(mi)
            self.smooth.append(True)

    def build(self, collection=None):
        me = bpy.data.meshes.new(self.name)
        me.from_pydata(self.verts, [], self.faces)
        for m in self.mats:
            me.materials.append(m)
        me.polygons.foreach_set("material_index", self.fmat)
        me.polygons.foreach_set("use_smooth", self.smooth)
        me.update()
        o = bpy.data.objects.new(self.name, me)
        (collection or bpy.context.collection).objects.link(o)
        return o


# ----------------------------------------------------------------- terreno (encosta)
TERRAIN = {}


def terrain_h(x, y):
    t = TERRAIN
    base = t["slope"] * (x * t["dirx"] + y * t["diry"])
    n = noise.noise(Vector((x * 0.015 + t["off"], y * 0.015, 0))) * t["amp"]
    n += noise.noise(Vector((x * 0.06, y * 0.06 + t["off"], 1))) * t["amp"] * 0.2
    return base + n


def build_terrain(size=900, step=4.0):
    TERRAIN.update(slope=rng.uniform(0.12, 0.4), dirx=rng.uniform(-1, 1), diry=rng.uniform(-1, 1),
                   amp=rng.uniform(2, 6), off=rng.uniform(0, 100))
    l = math.hypot(TERRAIN["dirx"], TERRAIN["diry"]) or 1
    TERRAIN["dirx"] /= l
    TERRAIN["diry"] /= l
    bm = bmesh.new()
    n = int(size / step) + 1
    grid = []
    for i in range(n):
        row = []
        for j in range(n):
            x = -size / 2 + i * step
            y = -size / 2 + j * step
            row.append(bm.verts.new((x, y, terrain_h(x, y))))
        grid.append(row)
    bm.verts.ensure_lookup_table()
    for i in range(n - 1):
        for j in range(n - 1):
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
    me = bpy.data.meshes.new("terreno")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("terreno", me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat_ground("m_terreno"))
    for p in o.data.polygons:
        p.use_smooth = True
    return o


# ----------------------------------------------------------------- layout da favela
BUILDINGS = []   # dicts com footprint rotacionado e topo (para pessoas em laje e colisao)


def split_axis(a, b, bmin, bmax, street):
    """divide [a,b] em quarteiroes separados por ruas"""
    out = []
    x = a
    while x < b - bmin * 0.6:
        w = rng.uniform(bmin, bmax)
        x1 = min(b, x + w)
        out.append((x, x1))
        x = x1 + rng.uniform(*street)
    return out


def layout_lots(extent=100):
    """retorna lotes (cx, cy, w, d, rot) organizados em quarteiroes com becos estreitos"""
    lots = []
    xs = split_axis(-extent, extent, 22, 48, (3.5, 7))
    ys = split_axis(-extent, extent, 22, 48, (3.5, 7))
    for (bx0, bx1) in xs:
        for (by0, by1) in ys:
            if rng.random() < 0.06:
                continue  # quarteirao vazio (campo, escola, area de risco)
            rot = rng.uniform(-0.35, 0.35) if rng.random() < 0.6 else 0.0
            bcx, bcy = (bx0 + bx1) / 2, (by0 + by1) / 2
            c, s = math.cos(rot), math.sin(rot)
            y = by0
            while y < by1 - 3:
                depth = rng.uniform(4.5, 8.5)
                if y + depth > by1:
                    depth = by1 - y
                if depth < 3.2:
                    break
                x = bx0
                while x < bx1 - 2.5:
                    w = rng.uniform(3.5, 8.0)
                    if x + w > bx1:
                        w = bx1 - x
                    if w < 2.8:
                        break
                    if rng.random() < 0.07:   # lote vazio / patio
                        x += w + rng.uniform(0, 1)
                        continue
                    lx, ly = x + w / 2 - bcx, y + depth / 2 - bcy
                    cx = bcx + lx * c - ly * s
                    cy = bcy + lx * s + ly * c
                    lots.append((cx, cy, w, depth, rot))
                    r = rng.random()
                    gap = 0.0 if r < 0.5 else (rng.uniform(0.5, 1.6) if r < 0.88 else rng.uniform(2, 4))
                    x += w + gap
                r = rng.random()
                y += depth + (0.0 if r < 0.3 else (rng.uniform(0.6, 1.8) if r < 0.85 else rng.uniform(2.5, 4)))
    return lots


def build_favela(extent=170):
    BUILDINGS.clear()
    # paleta: tijolo aparente domina; concreto cru; reboco pintado
    mats_brick = [mat_brick(f"m_brick{i}") for i in range(5)]
    mats_conc = [mat_principled(f"m_conc{i}", hsv(rng.uniform(0.08, 0.12), rng.uniform(0.03, 0.12), rng.uniform(0.3, 0.55)), rough=0.95) for i in range(3)]
    paint_h = [0.12, 0.55, 0.08, 0.0, 0.33, 0.16, 0.6, 0.95]
    mats_paint = [mat_principled(f"m_paint{i}", hsv(rng.choice(paint_h) + rng.uniform(-0.03, 0.03), rng.uniform(0.25, 0.75), rng.uniform(0.35, 0.8)), rough=0.8) for i in range(7)]
    mats_roof = []
    for i in range(3):
        g = rng.uniform(0.3, 0.5)
        mats_roof.append(mat_corrugated(f"m_fibro{i}", (g, g * 0.98, g * 0.95), metallic=0.0, rough=0.9))     # fibrocimento
    for i in range(3):
        g = rng.uniform(0.45, 0.75)
        mats_roof.append(mat_corrugated(f"m_zinco{i}", (g, g, g * 0.98), metallic=0.7))                          # zinco
    mats_laje = [mat_principled(f"m_laje{i}", hsv(0.09, rng.uniform(0.03, 0.1), rng.uniform(0.28, 0.5)), rough=0.95) for i in range(4)]
    mats_telha = [mat_principled(f"m_telha{i}", hsv(rng.uniform(0.03, 0.06), rng.uniform(0.5, 0.75), rng.uniform(0.3, 0.5)), rough=0.9) for i in range(2)]
    m_tank_b = mat_principled("m_tank_b", (0.03, 0.18, 0.5), rough=0.4, grime=0.5)
    m_tank_k = mat_principled("m_tank_k", (0.02, 0.02, 0.02), rough=0.5, grime=0.3)
    m_tank_w = mat_principled("m_tank_w", (0.7, 0.7, 0.68), rough=0.5, grime=0.5)
    m_dark = mat_principled("m_dark", (0.03, 0.03, 0.03), rough=0.9, grime=0.3)
    m_trunk = mat_principled("m_trunk", (0.12, 0.08, 0.05), rough=0.95, grime=0.3)
    mats_leaf = [mat_principled(f"m_leaf{i}", hsv(rng.uniform(0.2, 0.32), rng.uniform(0.5, 0.85), rng.uniform(0.15, 0.4)), rough=0.9) for i in range(3)]
    m_clutter = [mat_principled(f"m_clut{i}", hsv(rng.random(), rng.uniform(0.2, 0.7), rng.uniform(0.2, 0.7)), rough=0.8) for i in range(4)]

    lots = layout_lots(extent)
    mb = MeshBuilder("favela")
    for li, (cx, cy, w, d, rot) in enumerate(lots):
        c, s = math.cos(rot), math.sin(rot)
        corners = [(cx + dx * w / 2 * c - dy * d / 2 * s, cy + dx * w / 2 * s + dy * d / 2 * c) for dx in (-1, 1) for dy in (-1, 1)]
        zmin = min(terrain_h(x, y) for x, y in corners)
        zmax = max(terrain_h(x, y) for x, y in corners)
        z0 = zmin - 0.3
        floors = rng.choices([1, 2, 3, 4, 5], weights=[0.22, 0.38, 0.25, 0.11, 0.04])[0]
        r = rng.random()
        wall = rng.choice(mats_brick) if r < 0.55 else (rng.choice(mats_conc) if r < 0.75 else rng.choice(mats_paint))
        ztop = z0
        fw, fd = w, d
        fx, fy = cx, cy
        for f in range(floors):
            fh = rng.uniform(2.6, 3.2) + ((zmax - zmin) if f == 0 else 0)
            if f > 0 and rng.random() < 0.45:
                # adicao em laje: andar menor e deslocado (morfologia vertical)
                nw, nd = fw * rng.uniform(0.55, 0.95), fd * rng.uniform(0.55, 0.95)
                lx = rng.uniform(-(fw - nw) / 2, (fw - nw) / 2)
                ly = rng.uniform(-(fd - nd) / 2, (fd - nd) / 2)
                mb.box(fx, fy, ztop + 0.06, fw, fd, 0.12, rng.choice(mats_laje))   # laje exposta do andar de baixo
                fx, fy = fx + lx * c - ly * s, fy + lx * s + ly * c
                fw, fd = nw, nd
            mwall = wall if rng.random() < 0.7 else rng.choice(mats_brick + mats_conc + mats_paint)
            mb.box(fx, fy, ztop + fh / 2, fw, fd, fh, mwall, rot)
            ztop += fh
        # cobertura
        r = rng.random()
        if r < 0.45:
            roof = rng.choice(mats_laje)
            mb.box(fx, fy, ztop + 0.07, fw * 1.02, fd * 1.02, 0.14, roof, rot)
            ztop += 0.14
            if rng.random() < 0.5:   # parapeito
                ph = rng.uniform(0.7, 1.1)
                for (dx, dy, sw, sd) in ((0, -0.5, fw, 0.15), (0, 0.5, fw, 0.15), (-0.5, 0, 0.15, fd), (0.5, 0, 0.15, fd)):
                    px, py = dx * fw, dy * fd
                    mb.box(fx + px * c - py * s, fy + px * s + py * c, ztop + ph / 2, sw, sd, ph, wall, rot)
        elif r < 0.85:
            roof = rng.choice(mats_roof)
            mb.box(fx, fy, ztop + 0.05, fw * 1.08, fd * 1.08, 0.1, roof, rot)   # telha ondulada com beiral
            ztop += 0.1
            if rng.random() < 0.5:   # tijolos/pedras segurando a telha
                for _ in range(rng.randint(2, 6)):
                    px, py = rng.uniform(-fw / 2, fw / 2), rng.uniform(-fd / 2, fd / 2)
                    mb.box(fx + px * c - py * s, fy + px * s + py * c, ztop + 0.1, 0.25, 0.12, 0.2, rng.choice(mats_brick), rot)
        else:
            roof = rng.choice(mats_telha)
            mb.box(fx, fy, ztop + 0.1, fw * 1.06, fd * 1.06, 0.2, roof, rot)
            ztop += 0.2
        # caixa d'agua
        if rng.random() < 0.45:
            tx, ty = rng.uniform(-fw / 3, fw / 3), rng.uniform(-fd / 3, fd / 3)
            tm = rng.choices([m_tank_b, m_tank_k, m_tank_w], weights=[0.5, 0.35, 0.15])[0]
            if rng.random() < 0.7:
                mb.cyl(fx + tx * c - ty * s, fy + tx * s + ty * c, ztop + 0.5, rng.uniform(0.45, 0.65), 1.0, tm)
            else:
                mb.box(fx + tx * c - ty * s, fy + tx * s + ty * c, ztop + 0.45, 1.1, 1.1, 0.9, tm, rot)
        # tralha na laje
        if rng.random() < 0.3:
            for _ in range(rng.randint(1, 3)):
                px, py = rng.uniform(-fw / 2.5, fw / 2.5), rng.uniform(-fd / 2.5, fd / 2.5)
                mb.box(fx + px * c - py * s, fy + px * s + py * c, ztop + 0.25, rng.uniform(0.4, 1.2), rng.uniform(0.4, 1.0), 0.5, rng.choice(m_clutter), rot + rng.uniform(-0.5, 0.5))
        BUILDINGS.append(dict(cx=fx, cy=fy, w=fw, d=fd, rot=rot, ztop=ztop, floors=floors, base=(cx, cy, w, d)))
    # arvores em vazios
    for _ in range(int(len(lots) * 0.12)):
        x, y = rng.uniform(-extent, extent), rng.uniform(-extent, extent)
        if inside_building(x, y, margin=1.5):
            continue
        h = rng.uniform(4, 9)
        z = terrain_h(x, y)
        mb.cyl(x, y, z + h * 0.35, 0.15, h * 0.7, m_trunk, 6)
        lm = rng.choice(mats_leaf)
        for k in range(rng.randint(2, 4)):
            mb.sphere(x + rng.uniform(-1, 1), y + rng.uniform(-1, 1), z + h * 0.75 + rng.uniform(-0.8, 0.8), rng.uniform(1.6, 3.0), lm, squash=0.8)
    # lixo / entulho no chao
    for _ in range(int(len(lots) * 0.25)):
        x, y = rng.uniform(-extent, extent), rng.uniform(-extent, extent)
        if inside_building(x, y, margin=0.2):
            continue
        z = terrain_h(x, y)
        mb.box(x, y, z + 0.2, rng.uniform(0.4, 1.5), rng.uniform(0.4, 1.2), 0.4, rng.choice(m_clutter + [m_dark]), rng.uniform(0, 3))
    mb.build()
    return len(lots)


def inside_building(x, y, margin=0.4):
    for b in BUILDINGS:
        bx, by, bw, bd = b["base"]
        c, s = math.cos(-b["rot"]), math.sin(-b["rot"])
        lx = (x - bx) * c - (y - by) * s
        ly = (x - bx) * s + (y - by) * c
        if abs(lx) < bw / 2 + margin and abs(ly) < bd / 2 + margin:
            return b
    return None


def on_roof_point(b, x, y, margin=0.5):
    """true se (x,y) cai no topo do ultimo andar (fx,fy,fw,fd)"""
    c, s = math.cos(-b["rot"]), math.sin(-b["rot"])
    lx = (x - b["cx"]) * c - (y - b["cy"]) * s
    ly = (x - b["cx"]) * s + (y - b["cy"]) * c
    return abs(lx) < b["w"] / 2 - margin and abs(ly) < b["d"] / 2 - margin


# ----------------------------------------------------------------- pessoas (low-poly, ~1.7 m)
PEOPLE = []


def make_person(idx, pos, armed):
    skin = mat_principled(f"m_skin{idx}", hsv(rng.uniform(0.04, 0.08), rng.uniform(0.3, 0.6), rng.uniform(0.2, 0.8)), rough=0.7, grime=0.2)
    shirt = mat_principled(f"m_shirt{idx}", hsv(rng.random(), rng.uniform(0.2, 0.9), rng.uniform(0.1, 0.95)), rough=0.85, grime=0.3)
    pants = mat_principled(f"m_pants{idx}", hsv(rng.choice([0.6, 0.08, 0.0]), rng.uniform(0.1, 0.7), rng.uniform(0.08, 0.5)), rough=0.85, grime=0.3)
    h = rng.uniform(1.55, 1.85)
    yaw = rng.uniform(0, 2 * math.pi)
    walking = rng.random() < 0.5
    x, y, z = pos
    mb = MeshBuilder(f"person_{idx}")
    leg_h = h * 0.47
    for s in (-1, 1):
        lx = x + math.cos(yaw + math.pi / 2) * 0.1 * s
        ly = y + math.sin(yaw + math.pi / 2) * 0.1 * s
        step = 0.18 * s if walking else 0
        mb.cyl(lx + math.cos(yaw) * step, ly + math.sin(yaw) * step, z + leg_h / 2, 0.08, leg_h, pants, 8)
    torso_h = h * 0.33
    mb.box(x, y, z + leg_h + torso_h / 2, 0.42, 0.24, torso_h, shirt, yaw)
    arm_m = shirt if rng.random() < 0.5 else skin
    for s in (-1, 1):
        ax = x + math.cos(yaw + math.pi / 2) * 0.26 * s
        ay = y + math.sin(yaw + math.pi / 2) * 0.26 * s
        mb.cyl(ax, ay, z + leg_h + torso_h * 0.55, 0.055, torso_h * 0.9, arm_m, 8)
    mb.sphere(x, y, z + leg_h + torso_h + 0.14, 0.12, skin)
    if rng.random() < 0.5:
        mb.sphere(x, y, z + leg_h + torso_h + 0.17, 0.12, mat_principled(f"m_hair{idx}", rng.choice([(0.02, 0.015, 0.01), (0.9, 0.05, 0.05), (0.05, 0.05, 0.6), (0.9, 0.9, 0.9)]), grime=0.2))
    if armed:
        gm = mat_principled(f"m_gun{idx}", (0.02, 0.02, 0.02), rough=0.5, metallic=0.5, grime=0.2)
        gx = x + math.cos(yaw) * 0.35
        gy = y + math.sin(yaw) * 0.35
        mb.box(gx, gy, z + leg_h + torso_h * 0.65, 0.9, 0.06, 0.12, gm, yaw + rng.uniform(-0.4, 0.4))
    o = mb.build()
    o["cls"] = 0 if armed else 1
    o["height"] = h
    PEOPLE.append(o)
    return o


def place_people(center, n, radius=30):
    for o in PEOPLE:
        me = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.meshes.remove(me)
    PEOPLE.clear()
    placed = 0
    tries = 0
    while placed < n and tries < 400:
        tries += 1
        x = center[0] + rng.uniform(-radius, radius)
        y = center[1] + rng.uniform(-radius, radius)
        b = inside_building(x, y)
        on_roof = False
        if b is not None:
            if rng.random() < 0.4 and on_roof_point(b, x, y):
                z = b["ztop"]
                on_roof = True
            else:
                continue
        else:
            z = terrain_h(x, y)
        if any(math.hypot(p.location.x - x, p.location.y - y) < 0.8 for p in PEOPLE):
            continue
        armed = rng.random() < args.prob_armado
        o = make_person(placed, (x, y, z), armed)
        o["on_roof"] = on_roof
        o["px"], o["py"] = x, y
        placed += 1
    return placed


# ----------------------------------------------------------------- iluminacao / mundo
def setup_world():
    w = bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    sky = nt.nodes.new("ShaderNodeTexSky")
    for st in ('MULTIPLE_SCATTERING', 'NISHITA', 'SINGLE_SCATTERING'):
        try:
            sky.sky_type = st
            break
        except TypeError:
            continue
    bg = nt.nodes["Background"]
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    sun = bpy.data.lights.new("Sun", type='SUN')
    so = bpy.data.objects.new("Sun", sun)
    bpy.context.collection.objects.link(so)
    return sky, bg, so


def randomize_light(sky, bg, so):
    elev = math.radians(rng.uniform(20, 80))
    rot = rng.uniform(0, 2 * math.pi)
    for attr, val in (("sun_elevation", elev), ("sun_rotation", rot), ("altitude", 30),
                      ("air_density", rng.uniform(0.8, 1.8)), ("dust_density", rng.uniform(0.5, 5.0)),
                      ("sun_intensity", 0.0), ("sun_size", math.radians(rng.uniform(0.5, 3.0)))):
        try:
            setattr(sky, attr, val)
        except Exception:
            pass
    overcast = rng.random() < 0.3
    bg.inputs["Strength"].default_value = rng.uniform(0.25, 0.4) if overcast else rng.uniform(0.08, 0.18)
    so.data.energy = rng.uniform(0.6, 1.5) if overcast else rng.uniform(2.0, 4.0)
    so.data.angle = math.radians(rng.uniform(10, 30) if overcast else rng.uniform(0.5, 3))
    so.rotation_euler = Euler((math.pi / 2 - elev, 0, rot + math.pi), 'XYZ')
    bpy.context.scene.view_settings.exposure = rng.uniform(-1.2, -0.5)
    return dict(sun_elev=round(math.degrees(elev), 1), sun_az=round(math.degrees(rot), 1), overcast=overcast)


# ----------------------------------------------------------------- camera drone
def setup_camera():
    cam = bpy.data.cameras.new("DroneCam")
    cam.sensor_width = 36
    cam.sensor_fit = 'HORIZONTAL'
    co = bpy.data.objects.new("DroneCam", cam)
    bpy.context.collection.objects.link(co)
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
    cx = target[0] - math.cos(yaw) * dh
    cy = target[1] - math.sin(yaw) * dh
    co.location = (cx, cy, gz + alt)
    direction = Vector((target[0], target[1], gz)) - co.location
    co.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    co.rotation_euler.rotate_axis('Z', rng.uniform(-0.3, 0.3))
    return dict(alt=round(alt, 1), pitch=round(pitch, 1), yaw=round(math.degrees(yaw), 1), lens=round(lens, 1))


# ----------------------------------------------------------------- anotacao
def bbox_2d(scene, co, obj):
    mw = obj.matrix_world
    xs, ys = [], []
    for v in obj.data.vertices:
        p = world_to_camera_view(scene, co, mw @ v.co)
        if p.z <= 0:
            continue
        xs.append(p.x)
        ys.append(1.0 - p.y)
    if len(xs) < 4:
        return None
    x1, x2 = max(0.0, min(xs)), min(1.0, max(xs))
    y1, y2 = max(0.0, min(ys)), min(1.0, max(ys))
    if x2 - x1 < args.min_lado or y2 - y1 < args.min_lado:
        return None
    if x2 <= 0 or x1 >= 1 or y2 <= 0 or y1 >= 1:
        return None
    return (x1, y1, x2, y2)


def visibility(scene, co, obj, depsgraph, n=12):
    """fracao de pontos do corpo com linha de visao livre ate a camera"""
    mw = obj.matrix_world
    origin = co.matrix_world.translation
    verts = obj.data.vertices
    idxs = [int(i * (len(verts) - 1) / (n - 1)) for i in range(n)]
    ok = 0
    for i in idxs:
        p = mw @ verts[i].co
        d = p - origin
        dist = d.length
        d.normalize()
        hit, loc, nrm, fi, hobj, mtx = scene.ray_cast(depsgraph, origin, d, distance=dist + 0.5)
        if not hit or hobj == obj or (loc - p).length < 0.25:
            ok += 1
    return ok / len(idxs)


# ----------------------------------------------------------------- render setup
def setup_render(scene):
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.engine = 'CYCLES' if args.engine == 'CYCLES' else 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'AgX'
    try:
        scene.view_settings.look = 'AgX - Medium High Contrast'
    except Exception:
        pass
    if scene.render.engine == 'CYCLES':
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
    else:
        scene.eevee.taa_render_samples = max(16, args.samples)
        try:
            scene.eevee.use_shadows = True
            scene.eevee.use_raytracing = True
        except Exception:
            pass


def clear_favela():
    for o in list(bpy.data.objects):
        if o.name in ("favela", "terreno") or o.name.startswith("person_"):
            me = o.data
            bpy.data.objects.remove(o, do_unlink=True)
            bpy.data.meshes.remove(me)
    PEOPLE.clear()
    for m in list(bpy.data.materials):
        if m.users == 0:
            bpy.data.materials.remove(m)


# ----------------------------------------------------------------- main
t0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
setup_render(scene)
sky, bg, sun = setup_world()
cam = setup_camera()
build_terrain()
nb = build_favela()
print(f"[gen] favela inicial: {nb} edificacoes  ({time.time() - t0:.1f}s)")

manifest_path = os.path.join(OUT, "manifest.jsonl")
mf = open(manifest_path, "a", encoding="utf-8")
tot_boxes = 0
for i in range(args.start, args.start + args.n):
    if i > args.start and (i - args.start) % args.rebuild_every == 0:
        tb = time.time()
        clear_favela()
        build_terrain()
        nb = build_favela()
        print(f"[gen] nova favela: {nb} edificacoes ({time.time() - tb:.1f}s)")
    center = (rng.uniform(-50, 50), rng.uniform(-50, 50))
    n_people = rng.randint(args.people[0], args.people[1])
    place_people(center, n_people)
    light = randomize_light(sky, bg, sun)
    caminfo = place_camera(cam, center)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()

    split = "val" if rng.random() < args.val else "train"
    name = f"bl_{i:06d}"
    labels = []
    for p in PEOPLE:
        bb = bbox_2d(scene, cam, p)
        if bb is None:
            continue
        vis = visibility(scene, cam, p, depsgraph)
        if vis < args.min_vis:
            continue
        x1, y1, x2, y2 = bb
        labels.append((p["cls"], (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1, round(vis, 2), bool(p["on_roof"])))
    scene.render.filepath = os.path.join(OUT, "images", split, name + ".png")
    tr = time.time()
    bpy.ops.render.render(write_still=True)
    with open(os.path.join(OUT, "labels", split, name + ".txt"), "w") as f:
        for l in labels:
            f.write(f"{l[0]} {l[1]:.6f} {l[2]:.6f} {l[3]:.6f} {l[4]:.6f}\n")
    rec = dict(img=name + ".png", split=split, w=args.res[0], h=args.res[1])
    rec.update(caminfo)
    rec.update(light)
    rec.update(n_people=len(PEOPLE), n_boxes=len(labels), n_armed=sum(1 for l in labels if l[0] == 0),
               n_roof=sum(1 for l in labels if l[6]), vis=[l[5] for l in labels], buildings=nb, seed=args.seed,
               render_s=round(time.time() - tr, 1))
    mf.write(json.dumps(rec) + "\n")
    mf.flush()
    tot_boxes += len(labels)
    print(f"[gen] {name} {split} caixas={len(labels)}/{len(PEOPLE)} alt={caminfo['alt']} pitch={caminfo['pitch']} render={rec['render_s']}s")
mf.close()

with open(os.path.join(OUT, "data.yaml"), "w") as f:
    f.write(f"path: {OUT.replace(os.sep, '/')}\ntrain: images/train\nval: images/val\nnames:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
if args.save_blend:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.save_blend))
print(f"[gen] fim: {args.n} imagens, {tot_boxes} caixas, {time.time() - t0:.1f}s total")
