"""
build_cidade.py (v2): reconstroi o recorte do Jacarezinho como CIDADE DE SOLIDOS no Blender,
calibrado contra foto aerea real de favela paulista/carioca (bloco ceramico laranja dominante,
estrutura de concreto aparente, lajes cinza com caixa d'agua azul, sacadas, grades, fiacao,
entulho, nevoa e cidade ao fundo).

Entrada: predios.json + recorte_terreno.npz + recorte_orto.jpg (saidas do segmenta_predios.py).

Uso:
  blender -b --python build_cidade.py -- --sector sudoeste --out C:\arma3-favela\odm\quadra.blend --preview
"""
import bpy, bmesh, sys, os, math, json, argparse, random, colorsys
import numpy as np
from mathutils import Vector, Euler

ASSETS = r"C:\arma3-favela\assets"
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--sector", default="sudoeste")
ap.add_argument("--out", default=r"C:\arma3-favela\odm\quadra.blend")
ap.add_argument("--seed", type=int, default=3)
ap.add_argument("--preview", action="store_true")
ap.add_argument("--res", type=int, nargs=2, default=[1920, 1080])
ap.add_argument("--samples", type=int, default=96)
ap.add_argument("--pessoas", type=int, default=0)
ap.add_argument("--sem-entorno", action="store_true", help="nao carrega a malha do setor inteiro em volta do recorte")
ap.add_argument("--sem-nevoa", action="store_true")
ap.add_argument("--so-eval", action="store_true", help="renderiza so a camera de avaliacao")
args = ap.parse_args(argv)
root = os.path.join(r"C:\arma3-favela\odm", args.sector)
rng = random.Random(args.seed)

D = json.load(open(os.path.join(root, "predios.json")))
T = np.load(os.path.join(root, "recorte_terreno.npz"))
GX0, GY0, RES = float(T["x0"]), float(T["y0"]), float(T["res"])
R, C = int(T["R"]), int(T["C"])
SOLO = T["solo"]
LX, LY = C * RES, R * RES
print(f"[cidade] {len(D['predios'])} edificacoes, recorte {LX:.0f} x {LY:.0f} m", flush=True)


def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)


# ================================================================= materiais
PH = json.load(open(os.path.join(ASSETS, "polyhaven", "index.json")))
TEX = {}
for n, e in PH["textures"].items():
    TEX.setdefault(e["cat"], []).append(n)


def img(rel, noncolor=False):
    i = bpy.data.images.load(os.path.join(ASSETS, "polyhaven", rel), check_existing=True)
    if noncolor:
        i.colorspace_settings.name = 'Non-Color'
    return i


def _grime(nt, cor_out, forca, escala=None):
    """manchas de umidade e sujeira; escorridos verticais como em fachada real"""
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = escala or rng.uniform(0.4, 1.3)
    nz.inputs["Detail"].default_value = 6
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position = 0.36
    rp.color_ramp.elements[0].color = (0.42, 0.40, 0.37, 1)
    rp.color_ramp.elements[1].position = 0.66
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = 'RGBA'
    mx.blend_type = 'MULTIPLY'
    mx.inputs["Factor"].default_value = forca
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], rp.inputs["Fac"])
    nt.links.new(cor_out, mx.inputs[6])
    nt.links.new(rp.outputs["Color"], mx.inputs[7])
    # escorrido vertical: ruido esticado em Z
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (6.0, 6.0, 0.35)
    nz2 = nt.nodes.new("ShaderNodeTexNoise")
    nz2.inputs["Scale"].default_value = 1.0
    nz2.inputs["Detail"].default_value = 3
    rp2 = nt.nodes.new("ShaderNodeValToRGB")
    rp2.color_ramp.elements[0].position = 0.55
    rp2.color_ramp.elements[0].color = (0.55, 0.52, 0.5, 1)
    rp2.color_ramp.elements[1].position = 0.7
    mx2 = nt.nodes.new("ShaderNodeMix")
    mx2.data_type = 'RGBA'
    mx2.blend_type = 'MULTIPLY'
    mx2.inputs["Factor"].default_value = forca * 0.7
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz2.inputs["Vector"])
    nt.links.new(nz2.outputs["Fac"], rp2.inputs["Fac"])
    nt.links.new(mx.outputs[2], mx2.inputs[6])
    nt.links.new(rp2.outputs["Color"], mx2.inputs[7])
    return mx2.outputs[2]


def mat_bloco(nome, tom=0.0):
    """bloco ceramico de 6 furos assentado deitado (39 x 19 cm), argamassa cinza, sujeira e relevo.
    Mapeamento por face: u = x|ny| + y|nx|, v = z, para o bloco ficar deitado em qualquer parede."""
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.93
    tc = nt.nodes.new("ShaderNodeTexCoord")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    sn = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sp.inputs[0])
    nt.links.new(geo.outputs["True Normal"], sn.inputs[0])
    ax = nt.nodes.new("ShaderNodeMath"); ax.operation = 'ABSOLUTE'
    ay = nt.nodes.new("ShaderNodeMath"); ay.operation = 'ABSOLUTE'
    nt.links.new(sn.outputs["X"], ax.inputs[0])
    nt.links.new(sn.outputs["Y"], ay.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = 'MULTIPLY'
    m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = 'MULTIPLY'
    nt.links.new(sp.outputs["X"], m1.inputs[0]); nt.links.new(ay.outputs[0], m1.inputs[1])
    nt.links.new(sp.outputs["Y"], m2.inputs[0]); nt.links.new(ax.outputs[0], m2.inputs[1])
    ad = nt.nodes.new("ShaderNodeMath"); ad.operation = 'ADD'
    nt.links.new(m1.outputs[0], ad.inputs[0]); nt.links.new(m2.outputs[0], ad.inputs[1])
    cb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(ad.outputs[0], cb.inputs["X"])
    nt.links.new(sp.outputs["Z"], cb.inputs["Y"])
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.5
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.013
    br.inputs["Mortar Smooth"].default_value = 0.25
    br.inputs["Bias"].default_value = 0.0
    br.inputs["Brick Width"].default_value = 0.39
    br.inputs["Row Height"].default_value = 0.19
    c1 = hsv(0.052 + tom, 0.86, 0.86)
    c2 = hsv(0.044 + tom, 0.80, 0.70)
    br.inputs["Color1"].default_value = (c1[0], c1[1], c1[2], 1)
    br.inputs["Color2"].default_value = (c2[0], c2[1], c2[2], 1)
    br.inputs["Mortar"].default_value = (0.50, 0.47, 0.43, 1)
    nt.links.new(cb.outputs["Vector"], br.inputs["Vector"])
    # variacao de tom bloco a bloco
    nzv = nt.nodes.new("ShaderNodeTexNoise")
    nzv.inputs["Scale"].default_value = 3.0
    nzv.inputs["Detail"].default_value = 1
    rpv = nt.nodes.new("ShaderNodeValToRGB")
    rpv.color_ramp.elements[0].color = (0.82, 0.78, 0.76, 1)
    rpv.color_ramp.elements[1].color = (1.12, 1.08, 1.02, 1)
    mxv = nt.nodes.new("ShaderNodeMix")
    mxv.data_type = 'RGBA'
    mxv.blend_type = 'MULTIPLY'
    mxv.inputs["Factor"].default_value = 1.0
    nt.links.new(cb.outputs["Vector"], nzv.inputs["Vector"])
    nt.links.new(nzv.outputs["Fac"], rpv.inputs["Fac"])
    nt.links.new(br.outputs["Color"], mxv.inputs[6])
    nt.links.new(rpv.outputs["Color"], mxv.inputs[7])
    cor = _grime(nt, mxv.outputs[2], rng.uniform(0.25, 0.55))
    nt.links.new(cor, b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.35
    bp.invert = True
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_pbr(nome, texname, escala, tint=None, forca_tint=0.0, sujeira=0.5, metal=0.0, rough_fixo=None):
    e = PH["textures"][texname]
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Metallic"].default_value = metal
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1 / escala, 1 / escala, 1 / escala)
    mp.inputs["Location"].default_value = (rng.uniform(0, 9), rng.uniform(0, 9), rng.uniform(0, 9))
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    d = nt.nodes.new("ShaderNodeTexImage")
    d.image = img(e["diff"])
    d.projection = 'BOX'
    d.projection_blend = 0.2
    nt.links.new(mp.outputs["Vector"], d.inputs["Vector"])
    cor = d.outputs["Color"]
    if tint is not None and forca_tint > 0:
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = 'RGBA'
        mx.blend_type = 'MULTIPLY'
        mx.inputs["Factor"].default_value = forca_tint
        mx.inputs[7].default_value = (tint[0], tint[1], tint[2], 1)
        nt.links.new(cor, mx.inputs[6])
        cor = mx.outputs[2]
    if sujeira > 0:
        cor = _grime(nt, cor, sujeira)
    nt.links.new(cor, b.inputs["Base Color"])
    if rough_fixo is not None:
        b.inputs["Roughness"].default_value = rough_fixo
    elif "rough" in e:
        rg = nt.nodes.new("ShaderNodeTexImage")
        rg.image = img(e["rough"], True)
        rg.projection = 'BOX'
        nt.links.new(mp.outputs["Vector"], rg.inputs["Vector"])
        nt.links.new(rg.outputs["Color"], b.inputs["Roughness"])
    else:
        b.inputs["Roughness"].default_value = 0.9
    if "nor" in e:
        nr = nt.nodes.new("ShaderNodeTexImage")
        nr.image = img(e["nor"], True)
        nr.projection = 'BOX'
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = 1.0
        nt.links.new(mp.outputs["Vector"], nr.inputs["Vector"])
        nt.links.new(nr.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_simples(nome, cor, rough=0.85, metal=0.0):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (cor[0], cor[1], cor[2], 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def mat_foto(nome, caminho, x0, y0, lx, ly):
    """foto real projetada pelas coordenadas do mundo"""
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.95
    for k in ("Specular IOR Level", "Specular"):
        if k in b.inputs:
            b.inputs[k].default_value = 0.05
            break
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    ux = nt.nodes.new("ShaderNodeMath"); ux.operation = 'SUBTRACT'; ux.inputs[1].default_value = x0
    uy = nt.nodes.new("ShaderNodeMath"); uy.operation = 'SUBTRACT'; uy.inputs[1].default_value = y0
    dx = nt.nodes.new("ShaderNodeMath"); dx.operation = 'DIVIDE'; dx.inputs[1].default_value = lx
    dy = nt.nodes.new("ShaderNodeMath"); dy.operation = 'DIVIDE'; dy.inputs[1].default_value = ly
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(sep.outputs["X"], ux.inputs[0]); nt.links.new(sep.outputs["Y"], uy.inputs[0])
    nt.links.new(ux.outputs[0], dx.inputs[0]); nt.links.new(uy.outputs[0], dy.inputs[0])
    nt.links.new(dx.outputs[0], comb.inputs["X"]); nt.links.new(dy.outputs[0], comb.inputs["Y"])
    im = nt.nodes.new("ShaderNodeTexImage")
    im.image = bpy.data.images.load(caminho, check_existing=True)
    im.extension = 'EXTEND'
    nt.links.new(comb.outputs["Vector"], im.inputs["Vector"])
    nt.links.new(im.outputs["Color"], b.inputs["Base Color"])
    return m


# ================================================================= construtor de malha
class MB:
    def __init__(self, nome):
        self.nome = nome
        self.v, self.f, self.fm, self.sm, self.mats = [], [], [], [], []

    def mi(self, mat):
        if mat not in self.mats:
            self.mats.append(mat)
        return self.mats.index(mat)

    def face(self, idx, mat, smooth=False):
        self.f.append(tuple(idx))
        self.fm.append(self.mi(mat))
        self.sm.append(smooth)

    def prisma(self, poly, z0, z1, mat_par, mat_topo):
        n = len(poly)
        b = len(self.v)
        for (x, y) in poly:
            self.v.append((x, y, z0))
        for (x, y) in poly:
            self.v.append((x, y, z1))
        for i in range(n):
            j = (i + 1) % n
            self.face([b + i, b + j, b + n + j, b + n + i], mat_par)
        self.face([b + n + i for i in range(n)], mat_topo)

    def caixa(self, cx, cy, cz, sx, sy, sz, mat, rot=0.0):
        c, s = math.cos(rot), math.sin(rot)
        b = len(self.v)
        for dz in (-0.5, 0.5):
            for (dx, dy) in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
                x, y = dx * sx, dy * sy
                self.v.append((cx + x * c - y * s, cy + x * s + y * c, cz + dz * sz))
        for fa in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            self.face([b + i for i in fa], mat)

    def cilindro(self, cx, cy, cz, raio, h, mat, n=14):
        b = len(self.v)
        for dz in (-0.5, 0.5):
            for k in range(n):
                a = 2 * math.pi * k / n
                self.v.append((cx + raio * math.cos(a), cy + raio * math.sin(a), cz + dz * h))
        for k in range(n):
            k2 = (k + 1) % n
            self.face([b + k, b + k2, b + n + k2, b + n + k], mat, True)
        self.face([b + n + k for k in range(n)], mat)

    def fio(self, p0, p1, raio, mat, n=4, barriga=0.0):
        p0, p1 = Vector(p0), Vector(p1)
        passos = 6 if barriga else 1
        ant = p0
        for s in range(1, passos + 1):
            t = s / passos
            cur = p0.lerp(p1, t)
            cur.z -= math.sin(t * math.pi) * barriga
            d = cur - ant
            L = d.length
            if L > 1e-4:
                d.normalize()
                up = Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))
                u = d.cross(up).normalized()
                w = d.cross(u).normalized()
                b = len(self.v)
                for p in (ant, cur):
                    for k in range(n):
                        a = 2 * math.pi * k / n
                        q = p + u * (raio * math.cos(a)) + w * (raio * math.sin(a))
                        self.v.append((q.x, q.y, q.z))
                for k in range(n):
                    k2 = (k + 1) % n
                    self.face([b + k, b + k2, b + n + k2, b + n + k], mat, True)
            ant = cur

    def build(self, col=None):
        me = bpy.data.meshes.new(self.nome)
        me.from_pydata(self.v, [], self.f)
        for m in self.mats:
            me.materials.append(m)
        if self.f:
            me.polygons.foreach_set("material_index", self.fm)
            me.polygons.foreach_set("use_smooth", self.sm)
        me.update()
        o = bpy.data.objects.new(self.nome, me)
        (col or bpy.context.scene.collection).objects.link(o)
        return o


# ================================================================= cena
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
scene = bpy.context.scene
COLS = {}
for n in ("EDIFICACOES", "TERRENO", "DETALHES", "ENTORNO", "LUZ_E_CAMERAS"):
    COLS[n] = bpy.data.collections.new(n)
    scene.collection.children.link(COLS[n])

# ----------------------------------------------------------------- paleta calibrada na referencia
# ~62% bloco ceramico laranja (varios tons), ~20% reboco pintado, ~12% concreto/reboco cru, ~6% tijolo escuro
M_BLOCO = [mat_bloco(f"bloco{i}", tom=rng.uniform(-0.012, 0.012)) for i in range(7)]
PAL = [(0.58, 0.55, 0.80), (0.33, 0.45, 0.62), (0.14, 0.70, 0.85), (0.96, 0.35, 0.82), (0.06, 0.55, 0.62),
       (0.10, 0.30, 0.88), (0.45, 0.30, 0.70), (0.0, 0.0, 0.88), (0.0, 0.0, 0.72), (0.55, 0.20, 0.55)]
M_REBOCO = []
for i in range(10):
    h_, s_, v_ = PAL[i % len(PAL)]
    M_REBOCO.append(mat_pbr(f"reboco{i}", rng.choice(TEX["plaster"]), rng.uniform(1.4, 2.4),
                            tint=hsv(h_ + rng.uniform(-0.02, 0.02), s_ * rng.uniform(0.85, 1.15), v_ * rng.uniform(0.9, 1.1)),
                            forca_tint=rng.uniform(0.72, 0.95), sujeira=rng.uniform(0.35, 0.7)))
M_CONC = [mat_pbr(f"concreto{i}", t, rng.uniform(1.6, 2.4), sujeira=rng.uniform(0.4, 0.75))
          for i, t in enumerate(rng.sample(TEX["concrete"], 4))]
M_TIJ = [mat_pbr(f"tijolo{i}", t, rng.uniform(1.1, 1.6), sujeira=rng.uniform(0.4, 0.7))
         for i, t in enumerate(rng.sample(TEX["brick"], 3))]
# bloco ceramico fotografico (clay_block_wall, Poly Haven) com tons variados, junto com o procedural
M_BLOCO_FOTO = []
if "clay_block_wall" in PH["textures"]:
    for i in range(4):
        M_BLOCO_FOTO.append(mat_pbr(f"bloco_foto{i}", "clay_block_wall", rng.uniform(1.6, 2.2),
                                    tint=hsv(0.05 + rng.uniform(-0.01, 0.01), rng.uniform(0.55, 0.8), rng.uniform(0.85, 1.05)),
                                    forca_tint=rng.uniform(0.35, 0.6), sujeira=rng.uniform(0.25, 0.5)))
if "rough_block_wall" in PH["textures"]:
    M_CONC.append(mat_pbr("bloco_concreto", "rough_block_wall", 1.9, sujeira=0.5))
# clay_block_wall do Poly Haven e adobe, nao bloco ceramico: fica fora. O procedural e mais fiel.
M_FACHADA = M_BLOCO * 11 + M_REBOCO * 2 + M_CONC * 3 + M_TIJ * 1
M_ESTRUT = mat_pbr("estrutura_concreto", "concrete_wall_006" if "concrete_wall_006" in PH["textures"] else TEX["concrete"][0],
                   1.8, tint=(0.62, 0.61, 0.58), forca_tint=0.6, sujeira=0.5)
M_LAJE = [mat_pbr(f"laje{i}", t, rng.uniform(2.0, 3.0), sujeira=rng.uniform(0.4, 0.75)) for i, t in enumerate(rng.sample(TEX["laje"], 3))]
# fibrocimento claro (maioria), zinco novo brilhante e telha escura envelhecida (minoria), como na foto
M_FIBRO = [mat_pbr(f"fibro{i}", t, rng.uniform(1.0, 1.4), tint=hsv(0.09, 0.04, rng.uniform(0.62, 0.9)), forca_tint=0.75,
                   sujeira=rng.uniform(0.3, 0.55), metal=0.05) for i, t in enumerate(rng.sample(TEX["roof_metal"], 3))]
M_FIBRO += [mat_pbr("zinco_novo", rng.choice(TEX["roof_metal"]), 1.1, tint=(0.85, 0.86, 0.88), forca_tint=0.7, sujeira=0.25, metal=0.7, rough_fixo=0.35)]
M_FIBRO += [mat_pbr("telha_escura", rng.choice(TEX["roof_metal"]), 1.2, tint=(0.30, 0.27, 0.24), forca_tint=0.8, sujeira=0.6)]
M_FIBRO = M_FIBRO[:3] * 5 + M_FIBRO[3:]

M_FOTO = mat_foto("foto_recorte", os.path.join(root, "recorte_orto.jpg"), GX0, GY0, LX, LY)


def mat_telhado(nome, texname):
    """laje: foto real do ortomosaico misturada com concreto PBR. A foto sozinha, vista de lado,
    vira mancha (sombra e brilho gravados); o concreto devolve grao e uniformidade."""
    m = mat_foto(nome, os.path.join(root, "recorte_orto.jpg"), GX0, GY0, LX, LY)
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    foto = b.inputs["Base Color"].links[0].from_socket
    e = PH["textures"][texname]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.4, 0.4, 0.4)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    d = nt.nodes.new("ShaderNodeTexImage")
    d.image = img(e["diff"])
    d.projection = 'BOX'
    nt.links.new(mp.outputs["Vector"], d.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = 'RGBA'
    mx.blend_type = 'MIX'
    mx.inputs["Factor"].default_value = 0.45
    nt.links.new(foto, mx.inputs[6])
    nt.links.new(d.outputs["Color"], mx.inputs[7])
    nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    if "nor" in e:
        nr = nt.nodes.new("ShaderNodeTexImage")
        nr.image = img(e["nor"], True)
        nr.projection = 'BOX'
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = 0.6
        nt.links.new(mp.outputs["Vector"], nr.inputs["Vector"])
        nt.links.new(nr.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    return m


M_TELHADO = [mat_telhado(f"telhado{i}", t) for i, t in enumerate(rng.sample(TEX["laje"], 3))]
M_VIDRO = mat_simples("vidro", (0.012, 0.015, 0.02), rough=0.15)
M_BURACO = mat_simples("vao_escuro", (0.008, 0.007, 0.006), rough=0.95)
M_CAIXILHO = [mat_simples("caixilho_branco", (0.7, 0.7, 0.68), rough=0.5),
              mat_simples("caixilho_ferro", (0.16, 0.17, 0.19), rough=0.5, metal=0.6),
              mat_simples("caixilho_aluminio", (0.62, 0.63, 0.64), rough=0.35, metal=0.8)]
M_GRADE = mat_simples("grade", (0.09, 0.09, 0.1), rough=0.5, metal=0.7)
M_PORTA = [mat_simples("porta_madeira", (0.13, 0.08, 0.05), rough=0.7),
           mat_simples("portao_metal", (0.22, 0.24, 0.27), rough=0.45, metal=0.6),
           mat_simples("portao_vermelho", (0.45, 0.06, 0.05), rough=0.5, metal=0.4)]
M_CXD = [mat_simples("cx_azul", (0.03, 0.14, 0.45), rough=0.4), mat_simples("cx_azul2", (0.05, 0.22, 0.55), rough=0.4),
         mat_simples("cx_preta", (0.022, 0.022, 0.024), rough=0.45), mat_simples("cx_branca", (0.68, 0.68, 0.65), rough=0.5)]
M_FIO = mat_simples("fio", (0.02, 0.02, 0.02), rough=0.7)
M_POSTE = mat_simples("poste", (0.42, 0.41, 0.39), rough=0.9)
M_FERRO = mat_simples("ferragem", (0.28, 0.14, 0.08), rough=0.9, metal=0.3)
M_ANT = mat_simples("antena", (0.66, 0.66, 0.64), rough=0.5, metal=0.3)
M_LONA = [mat_simples("lona_azul", (0.05, 0.18, 0.62), rough=0.6), mat_simples("lona_preta", (0.03, 0.03, 0.03), rough=0.6)]
M_ZINCO = mat_pbr("zinco_cerca", rng.choice(TEX["roof_metal"]), 1.2, sujeira=0.6, metal=0.4)
M_ROUPA = [mat_simples(f"roupa{i}", hsv(rng.random(), rng.uniform(0.3, 0.9), rng.uniform(0.3, 0.95)), rough=0.9) for i in range(8)]
M_FUNDO = mat_simples("fundo_cidade", (0.52, 0.55, 0.60), rough=0.8)

# ----------------------------------------------------------------- terreno com a foto real
bm = bmesh.new()
passo = 2
nR, nC = R // passo, C // passo
grid = [[bm.verts.new((GX0 + j * passo * RES, GY0 + i * passo * RES, float(SOLO[i * passo, j * passo]))) for j in range(nC)] for i in range(nR)]
for i in range(nR - 1):
    for j in range(nC - 1):
        bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
me = bpy.data.meshes.new("terreno")
bm.to_mesh(me)
bm.free()
chao = bpy.data.objects.new("terreno", me)
COLS["TERRENO"].objects.link(chao)
chao.data.materials.append(M_FOTO)
for p in chao.data.polygons:
    p.use_smooth = True

# ----------------------------------------------------------------- entorno: anel de casario procedural ate 900 m
# A malha de fotogrametria fora do recorte derrete e destoa dos solidos. Em vez dela, um anel de
# casario simples (sem esquadria detalhada) na mesma paleta, seguindo a cota do terreno na borda.
PAV_H = 2.85


def solo_clamp(x, y):
    i = min(R - 1, max(0, int((y - GY0) / RES)))
    j = min(C - 1, max(0, int((x - GX0) / RES)))
    return float(SOLO[i, j])


if not args.sem_entorno:
    anel = MB("anel_casario")
    M_JAN_LONGE = mat_simples("janela_longe", (0.02, 0.02, 0.025), rough=0.9)
    passo = 9.5
    cxm, cym = GX0 + LX / 2, GY0 + LY / 2
    n_anel = 0
    for gi in range(int(-900 / passo), int(900 / passo) + 1):
        for gj in range(int(-900 / passo), int(900 / passo) + 1):
            x = cxm + gi * passo + rng.uniform(-2.5, 2.5)
            y = cym + gj * passo + rng.uniform(-2.5, 2.5)
            if GX0 - 2 < x < GX0 + LX + 2 and GY0 - 2 < y < GY0 + LY + 2:
                continue
            dist = math.hypot(x - cxm, y - cym)
            if dist > 900 or rng.random() < 0.18:
                continue
            w, d = rng.uniform(4.5, 9.0), rng.uniform(4.5, 9.0)
            hz = rng.choices([3.0, 5.6, 8.4, 11.2], weights=[0.25, 0.4, 0.25, 0.1])[0] + rng.uniform(-0.4, 0.4)
            ang = rng.uniform(0, math.pi)
            gz = solo_clamp(x, y) - 0.3
            fach = rng.choice(M_FACHADA)
            c, s = math.cos(ang), math.sin(ang)
            poly = [(x + dx * w / 2 * c - dy * d / 2 * s, y + dx * w / 2 * s + dy * d / 2 * c) for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            anel.prisma(poly, gz, gz + hz, fach, rng.choice(M_LAJE + M_FIBRO[:3]))
            if dist < 650:   # so o anel interno ganha vaos, o resto some na nevoa
                for pv in range(max(1, int(hz / PAV_H))):
                    for lado in range(4):
                        if rng.random() < 0.5:
                            continue
                        x1, y1 = poly[lado]
                        x2, y2 = poly[(lado + 1) % 4]
                        a2 = math.atan2(y2 - y1, x2 - x1)
                        nx, ny = math.sin(a2), -math.cos(a2)
                        anel.caixa((x1 + x2) / 2 + nx * 0.03, (y1 + y2) / 2 + ny * 0.03, gz + 0.4 + pv * PAV_H + 1.5, 1.1, 0.08, 1.0, M_JAN_LONGE, a2)
            if rng.random() < 0.35:
                anel.cilindro(x + rng.uniform(-1, 1), y + rng.uniform(-1, 1), gz + hz + 0.5, 0.6, 1.0, rng.choice(M_CXD), 8)
            n_anel += 1
    anel.build(COLS["ENTORNO"])
    print(f"[cidade] anel de casario: {n_anel} volumes", flush=True)
    # chao ate o horizonte, na cota baixa do terreno, para o skyline nao flutuar sobre o vazio
    zb = float(np.percentile(SOLO, 3)) - 1.5
    bpy.ops.mesh.primitive_plane_add(size=6000, location=(GX0 + LX / 2, GY0 + LY / 2, zb))
    mold = bpy.context.active_object
    mold.name = "moldura_entorno"
    mold.data.materials.append(mat_pbr("chao_longe", rng.choice([t for t in TEX["ground"] if "asphalt" in t or "dirt" in t]), 9.0,
                                       tint=(0.55, 0.53, 0.5), forca_tint=0.8, sujeira=0.6))
    for c in list(mold.users_collection):
        c.objects.unlink(mold)
    COLS["ENTORNO"].objects.link(mold)
    # skyline distante: silhuetas de predios altos na nevoa, como na referencia
    sk = MB("skyline")
    for k in range(70):
        a = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(900, 1900)
        x, y = GX0 + LX / 2 + math.cos(a) * dist, GY0 + LY / 2 + math.sin(a) * dist
        h = rng.choice([15, 18, 24, 30, 36, 45, 55])
        w = rng.uniform(14, 30)
        sk.caixa(x, y, zb + h / 2, w, w * rng.uniform(0.7, 1.4), h, M_FUNDO, rng.uniform(0, 3))
    sk.build(COLS["ENTORNO"])

# ----------------------------------------------------------------- edificacoes
mb = MB("edificacoes")
mbe = MB("estrutura")
mbj = MB("esquadrias")
det = MB("detalhes")
n_jan = n_porta = n_cx = n_sac = n_col = 0
topos = []
PAV_H = 2.85
for p in D["predios"]:
    poly = [(float(a), float(b)) for a, b in p["poly"]]
    area2 = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    if area2 < 0:
        poly.reverse()
    z0, z1 = p["z_base"] - 0.4, p["z_topo"]
    h = z1 - z0
    fach = rng.choice(M_FACHADA)
    inacabado = fach in M_BLOCO or fach in M_CONC   # estrutura de concreto aparente so em obra crua
    pav = max(1, min(6, int(round(h / PAV_H))))
    mb.prisma(poly, z0, z1, fach, rng.choice(M_TELHADO))
    topos.append((p, poly, z1))
    cxp = sum(a for a, _ in poly) / len(poly)
    cyp = sum(b for _, b in poly) / len(poly)

    # ---------------- estrutura de concreto aparente: pilares nas quinas e a cada ~3,5 m, viga por pavimento
    if inacabado and rng.random() < 0.75:
        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % len(poly)]
            L = math.hypot(x2 - x1, y2 - y1)
            if L < 0.5:
                continue
            ang = math.atan2(y2 - y1, x2 - x1)
            nx, ny = math.sin(ang), -math.cos(ang)
            mbe.caixa(x1 + nx * 0.02, y1 + ny * 0.02, (z0 + z1) / 2, 0.22, 0.22, h, M_ESTRUT, ang)
            n_col += 1
            kk = int(L / rng.uniform(3.2, 4.2))
            for w in range(1, kk + 1):
                t = w / (kk + 1)
                mbe.caixa(x1 + (x2 - x1) * t + nx * 0.02, y1 + (y2 - y1) * t + ny * 0.02, (z0 + z1) / 2, 0.20, 0.20, h, M_ESTRUT, ang)
                n_col += 1
            for pv in range(1, pav + 1):
                zv = z0 + pv * (h / pav)
                if zv > z1 + 0.05:
                    continue
                mbe.caixa((x1 + x2) / 2 + nx * 0.02, (y1 + y2) / 2 + ny * 0.02, min(zv, z1) - 0.14, L, 0.10, 0.28, M_ESTRUT, ang)

    # ---------------- esquadrias por pavimento: vao aberto, janela com caixilho, grade, porta ou portao
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 1.8:
            continue
        ang = math.atan2(y2 - y1, x2 - x1)
        nx, ny = math.sin(ang), -math.cos(ang)
        tx, ty = math.cos(ang), math.sin(ang)
        k = max(1, int(L / rng.uniform(2.4, 3.6)))
        for w in range(k):
            t = (w + 0.5) / k + rng.uniform(-0.05, 0.05)
            bx, by = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            for pv in range(pav):
                zb = z0 + 0.4 + pv * (h / pav)
                zc = zb + (h / pav) * 0.55
                if zc > z1 - 0.45:
                    continue
                if pv == 0 and rng.random() < 0.24:
                    mp_ = rng.choice(M_PORTA)
                    mbj.caixa(bx + nx * 0.05, by + ny * 0.05, zb + 1.05, rng.uniform(0.9, 1.6) if mp_ is not M_PORTA[0] else 0.9, 0.12, 2.1, mp_, ang)
                    n_porta += 1
                    continue
                if rng.random() > 0.68:
                    continue
                jw, jh = rng.uniform(0.7, 1.35), rng.uniform(0.8, 1.2)
                tipo = rng.random()
                if tipo < 0.35:      # vao aberto, sem esquadria (obra crua)
                    mbj.caixa(bx - nx * 0.10, by - ny * 0.10, zc, jw, 0.24, jh, M_BURACO, ang)
                elif tipo < 0.8:     # caixilho + vidro
                    cx_ = rng.choice(M_CAIXILHO)
                    mbj.caixa(bx + nx * 0.04, by + ny * 0.04, zc, jw + 0.14, 0.10, jh + 0.14, cx_, ang)
                    mbj.caixa(bx + nx * 0.07, by + ny * 0.07, zc, jw, 0.06, jh, M_VIDRO, ang)
                    # peitoril
                    mbj.caixa(bx + nx * 0.08, by + ny * 0.08, zc - jh / 2 - 0.03, jw + 0.3, 0.16, 0.06, M_ESTRUT, ang)
                else:                # grade de ferro sobre vao escuro
                    mbj.caixa(bx - nx * 0.08, by - ny * 0.08, zc, jw, 0.2, jh, M_BURACO, ang)
                    nb = max(2, int(jw / 0.15))
                    for g in range(nb):
                        u = -jw / 2 + (g + 0.5) * jw / nb
                        mbj.caixa(bx + nx * 0.06 + tx * u, by + ny * 0.06 + ty * u, zc, 0.02, 0.02, jh, M_GRADE, ang)
                n_jan += 1

    # ---------------- sacada com guarda-corpo num pavimento superior
    if pav >= 2 and rng.random() < 0.28:
        i = rng.randrange(len(poly))
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        L = math.hypot(x2 - x1, y2 - y1)
        if L > 2.5:
            ang = math.atan2(y2 - y1, x2 - x1)
            nx, ny = math.sin(ang), -math.cos(ang)
            tx, ty = math.cos(ang), math.sin(ang)
            pv = rng.randrange(1, pav)
            zs = z0 + 0.4 + pv * (h / pav)
            prof = rng.uniform(0.8, 1.2)
            comp = min(L - 0.4, rng.uniform(2.2, 4.5))
            u0 = rng.uniform(-(L - comp) / 2, (L - comp) / 2)
            mx_, my_ = (x1 + x2) / 2 + tx * u0 + nx * prof / 2, (y1 + y2) / 2 + ty * u0 + ny * prof / 2
            mbe.caixa(mx_, my_, zs - 0.08, comp, prof, 0.16, M_ESTRUT, ang)
            if rng.random() < 0.5:   # mureta
                mbe.caixa(mx_ + nx * prof / 2, my_ + ny * prof / 2, zs + 0.5, comp, 0.12, 1.0, fach, ang)
            else:                    # guarda-corpo de ferro
                for g in range(int(comp / 0.14)):
                    u = -comp / 2 + (g + 0.5) * comp / int(comp / 0.14)
                    mbj.caixa(mx_ + nx * prof / 2 + tx * u, my_ + ny * prof / 2 + ty * u, zs + 0.5, 0.02, 0.02, 1.0, M_GRADE, ang)
                mbj.caixa(mx_ + nx * prof / 2, my_ + ny * prof / 2, zs + 1.0, comp, 0.04, 0.04, M_GRADE, ang)
            n_sac += 1

    # ---------------- cobertura: mureta, telha de fibrocimento sobre a laje, lona, ferragem de espera
    r_ = rng.random()
    if r_ < 0.5:      # mureta de laje
        ph = rng.uniform(0.5, 1.05)
        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % len(poly)]
            L = math.hypot(x2 - x1, y2 - y1)
            if L < 0.6:
                continue
            ang = math.atan2(y2 - y1, x2 - x1)
            nx, ny = math.sin(ang), -math.cos(ang)
            det.caixa((x1 + x2) / 2 - nx * 0.07, (y1 + y2) / 2 - ny * 0.07, z1 + ph / 2, L, 0.14, ph, fach, ang)
    elif r_ < 0.72:   # telhado de fibrocimento/zinco sobre a laje, com beiral curto, apoiado em pontaletes
        mf = rng.choice(M_FIBRO)
        beiral = [(cxp + (a - cxp) * 1.07, cyp + (b - cyp) * 1.07) for a, b in poly]
        det.prisma(beiral, z1 + 0.42, z1 + 0.47, mf, mf)
        for (px_, py_) in poly:
            det.caixa(px_ * 0.88 + cxp * 0.12, py_ * 0.88 + cyp * 0.12, z1 + 0.21, 0.08, 0.08, 0.42, M_POSTE, 0)
    if rng.random() < 0.12:
        det.caixa(cxp + rng.uniform(-1, 1), cyp + rng.uniform(-1, 1), z1 + 0.03,
                  rng.uniform(2, 4), rng.uniform(2, 3.5), 0.04, rng.choice(M_LONA), rng.uniform(0, 3))
    if rng.random() < 0.4:   # ferragem de espera nas quinas
        for (px_, py_) in poly[:4]:
            if rng.random() < 0.7:
                det.fio((px_, py_, z1), (px_ + rng.uniform(-0.04, 0.04), py_ + rng.uniform(-0.04, 0.04), z1 + rng.uniform(0.5, 1.4)), 0.02, M_FERRO)

    # ---------------- volumes de laje medidos (caixa d'agua, casa de maquinas, escada)
    for ob in p["objetos"]:
        raio = max(0.35, min(1.1, ob["raio"]))
        hh = max(0.6, min(2.6, ob["h"]))
        if raio < 0.75 and hh < 1.6:
            det.cilindro(ob["x"], ob["y"], z1 + hh / 2, raio, hh, rng.choices(M_CXD, weights=[0.4, 0.25, 0.22, 0.13])[0])
            det.cilindro(ob["x"], ob["y"], z1 + hh + 0.03, raio * 1.06, 0.06, M_CXD[2] if rng.random() < 0.5 else M_CXD[0])
        else:
            det.caixa(ob["x"], ob["y"], z1 + hh / 2, raio * 2, raio * 2, hh, rng.choice(M_LAJE + [fach]))
        n_cx += 1

    # ---------------- parabolica, varal
    if rng.random() < 0.3:
        px_, py_ = cxp + rng.uniform(-1.5, 1.5), cyp + rng.uniform(-1.5, 1.5)
        det.fio((px_, py_, z1), (px_, py_, z1 + 1.1), 0.03, M_ANT)
        det.cilindro(px_, py_, z1 + 1.2, 0.33, 0.07, M_ANT, 12)
    if rng.random() < 0.18 and len(poly) >= 3:
        a_, c_ = poly[0], poly[len(poly) // 2]
        det.fio((a_[0], a_[1], z1 + 1.7), (c_[0], c_[1], z1 + 1.7), 0.008, M_FIO)
        for k in range(rng.randint(2, 5)):
            t = rng.uniform(0.15, 0.85)
            det.caixa(a_[0] + (c_[0] - a_[0]) * t, a_[1] + (c_[1] - a_[1]) * t, z1 + 1.35, 0.45, 0.02, 0.6, rng.choice(M_ROUPA), math.atan2(c_[1] - a_[1], c_[0] - a_[0]))

print(f"[cidade] {len(D['predios'])} predios, {n_col} pilares, {n_jan} vaos, {n_porta} portas, {n_sac} sacadas, {n_cx} volumes de laje", flush=True)

# ----------------------------------------------------------------- postes e fiacao
topos.sort(key=lambda t: -t[0]["area"])
altos = [t for t in topos if t[2] - t[0]["z_base"] > 4.5][:240]
n_fio = 0
for a in altos:
    pa = (sum(x for x, _ in a[1]) / len(a[1]), sum(y for _, y in a[1]) / len(a[1]), a[2])
    viz = sorted(((math.dist(pa[:2], (sum(x for x, _ in b[1]) / len(b[1]), sum(y for _, y in b[1]) / len(b[1]))), b) for b in altos if b is not a), key=lambda t: t[0])[:2]
    for dist, b in viz:
        if not (6 < dist < 32) or rng.random() < 0.4:
            continue
        pb = (sum(x for x, _ in b[1]) / len(b[1]), sum(y for _, y in b[1]) / len(b[1]), b[2])
        for k in range(rng.randint(1, 3)):
            det.fio((pa[0], pa[1], pa[2] + 0.6 - 0.12 * k), (pb[0], pb[1], pb[2] + 0.6 - 0.12 * k), 0.012, M_FIO, barriga=rng.uniform(0.4, 1.1))
            n_fio += 1
# postes de concreto em vazios (rua) com cruzeta e fios
postes = []
for k in range(40):
    x, y = GX0 + rng.uniform(5, LX - 5), GY0 + rng.uniform(5, LY - 5)
    if any(math.hypot(x - sum(a for a, _ in t[1]) / len(t[1]), y - sum(b for _, b in t[1]) / len(t[1])) < 5.0 for t in topos):
        continue
    gz = float(SOLO[min(R - 1, int((y - GY0) / RES)), min(C - 1, int((x - GX0) / RES))])
    det.fio((x, y, gz - 0.3), (x, y, gz + 8.6), 0.12, M_POSTE, 8)
    det.caixa(x, y, gz + 8.3, 1.3, 0.1, 0.12, M_POSTE, rng.uniform(0, 3))
    postes.append((x, y, gz + 8.4))
for i, p in enumerate(postes):
    for q in postes[i + 1:]:
        d_ = math.hypot(q[0] - p[0], q[1] - p[1])
        if 8 < d_ < 45:
            for k in range(rng.randint(2, 4)):
                det.fio((p[0], p[1], p[2] - 0.15 * k), (q[0], q[1], q[2] - 0.15 * k), 0.012, M_FIO, barriga=rng.uniform(0.5, 1.2))
                n_fio += 1
print(f"[cidade] {len(postes)} postes, {n_fio} tracados de fiacao", flush=True)

# ----------------------------------------------------------------- entulho, cercas de zinco, pneus no chao
for k in range(160):
    x, y = GX0 + rng.uniform(3, LX - 3), GY0 + rng.uniform(3, LY - 3)
    if any(math.hypot(x - sum(a for a, _ in t[1]) / len(t[1]), y - sum(b for _, b in t[1]) / len(t[1])) < 4.0 for t in topos):
        continue
    gz = float(SOLO[min(R - 1, int((y - GY0) / RES)), min(C - 1, int((x - GX0) / RES))])
    r_ = rng.random()
    if r_ < 0.4:
        det.caixa(x, y, gz + 0.2, rng.uniform(0.5, 1.6), rng.uniform(0.4, 1.2), rng.uniform(0.2, 0.5), rng.choice(M_CONC + M_LAJE), rng.uniform(0, 3))
    elif r_ < 0.7:
        det.cilindro(x, y, gz + 0.1, 0.32, 0.2, M_GRADE, 12)
    else:
        det.caixa(x, y, gz + 1.0, rng.uniform(2, 5), 0.03, 2.0, M_ZINCO, rng.uniform(0, 3))

obj_pred = mb.build(COLS["EDIFICACOES"])
obj_est = mbe.build(COLS["EDIFICACOES"])
obj_esq = mbj.build(COLS["EDIFICACOES"])
obj_det = det.build(COLS["DETALHES"])
print(f"[cidade] faces: predios {len(obj_pred.data.polygons)}, estrutura {len(obj_est.data.polygons)}, esquadrias {len(obj_esq.data.polygons)}, detalhes {len(obj_det.data.polygons)}", flush=True)

# ----------------------------------------------------------------- arvores (acervo CC0) onde a foto mostra copa
arv = D.get("arvores", [])
LIB = {}
if arv:
    colv = bpy.data.collections.new("_acervo_arvores")
    scene.collection.children.link(colv)
    for n in ("island_tree_01", "island_tree_02", "tree_small_02"):
        p = PH.get("models", {}).get(n)
        if not p:
            continue
        antes = set(bpy.data.objects)
        try:
            bpy.ops.import_scene.gltf(filepath=os.path.join(ASSETS, "polyhaven", p))
        except Exception as e:
            print("[cidade] arvore falhou", n, e)
            continue
        sub = bpy.data.collections.new(f"arv_{n}")
        colv.children.link(sub)
        for o in [o for o in bpy.data.objects if o not in antes]:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            sub.objects.link(o)
        LIB[n] = sub
    bpy.context.view_layer.layer_collection.children["_acervo_arvores"].exclude = True
    # alem das copas detectadas, arvores em vazios entre casas (a foto de referencia tem varias)
    extra = []
    tent = 0
    while len(extra) < int(len(D["predios"]) * 0.03) and tent < 4000:
        tent += 1
        x, y = GX0 + rng.uniform(5, LX - 5), GY0 + rng.uniform(5, LY - 5)
        if any(math.hypot(x - sum(a for a, _ in t[1]) / len(t[1]), y - sum(b for _, b in t[1]) / len(t[1])) < 5.5 for t in topos):
            continue
        extra.append(dict(x=x, y=y, raio=rng.uniform(1.6, 3.2)))
    arv = arv + extra
    for k, a in enumerate(arv):
        if not LIB:
            break
        o = bpy.data.objects.new(f"arvore_{k}", None)
        o.instance_type = 'COLLECTION'
        o.instance_collection = LIB[rng.choice(list(LIB))]
        esc = max(0.45, min(2.4, a["raio"] / 2.4))
        gz = float(SOLO[min(R - 1, max(0, int((a["y"] - GY0) / RES))), min(C - 1, max(0, int((a["x"] - GX0) / RES)))])
        o.location = (a["x"], a["y"], gz - 0.3)
        o.rotation_euler = (0, 0, rng.uniform(0, 6.28))
        o.scale = (esc, esc, esc * rng.uniform(0.9, 1.2))
        COLS["DETALHES"].objects.link(o)
    print(f"[cidade] {len(arv)} arvores", flush=True)

# ----------------------------------------------------------------- pessoas
if args.pessoas > 0:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import people_mpfb as PM
    COL_P = bpy.data.collections.new("PESSOAS")
    scene.collection.children.link(COL_P)
    PM.build_pool(rng, 6, print)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    def solo_fn(x, y):
        hit, loc, nrm, fi, o, mtx = scene.ray_cast(dg, Vector((x, y, 200)), Vector((0, 0, -1)), distance=500)
        if not hit or nrm.z < 0.9 or o.original.name.startswith(("entorno", "skyline", "anel", "moldura", "detalhes", "esquadrias")):
            return None
        return loc.z - 0.02

    # metade em grupos de 2 a 4 (conversando, parados juntos), metade solta
    posto = tent = 0
    while posto < args.pessoas and tent < args.pessoas * 40:
        tent += 1
        x = GX0 + rng.uniform(4, LX - 4)
        y = GY0 + rng.uniform(4, LY - 4)
        z = solo_fn(x, y)
        if z is None:
            continue
        if rng.random() < 0.5:
            feitos = PM.place_group(rng, posto, x, y, rng.randint(2, 4), solo_fn, armed_prob=0.3)
        else:
            feitos = [PM.make_person(rng, posto, x, y, z, rng.random() < 0.3)]
        for pp in feitos:
            for ob in pp["kids"] + [pp["rig"]] + ([pp["gun"]] if pp["gun"] else []):
                for cc in list(ob.users_collection):
                    cc.objects.unlink(ob)
                COL_P.objects.link(ob)
        posto += len(feitos)
    print(f"[cidade] {posto} pessoas", flush=True)
    cp = bpy.data.collections.new("_acervo")
    scene.collection.children.link(cp)
    for hh in PM.POOL:
        for ob in hh["kids"] + [hh["rig"]]:
            for cc in list(ob.users_collection):
                cc.objects.unlink(ob)
            cp.objects.link(ob)
    cp.hide_viewport = cp.hide_render = True

# ----------------------------------------------------------------- luz: dia encoberto e umido como na referencia
w = bpy.data.worlds.new("Ceu")
scene.world = w
w.use_nodes = True
nt = w.node_tree
bg = nt.nodes["Background"]
sky = nt.nodes.new("ShaderNodeTexSky")
for st in ('MULTIPLE_SCATTERING', 'NISHITA'):
    try:
        sky.sky_type = st
        break
    except TypeError:
        continue
ELEV, AZ = 49.4, 1.6
for a_, v_ in (("sun_elevation", math.radians(ELEV)), ("sun_rotation", math.radians(AZ)),
               ("altitude", 30), ("air_density", 1.3), ("dust_density", 6.0), ("sun_intensity", 0.0)):
    try:
        setattr(sky, a_, v_)
    except Exception:
        pass
nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0
amb = nt.nodes.new("ShaderNodeBackground")
amb.inputs["Color"].default_value = (0.94, 0.95, 0.98, 1.0)
amb.inputs["Strength"].default_value = 0.75
lp = nt.nodes.new("ShaderNodeLightPath")
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
nt.links.new(amb.outputs["Background"], mx.inputs[1])
nt.links.new(bg.outputs["Background"], mx.inputs[2])
ow = next(n for n in nt.nodes if n.type == 'OUTPUT_WORLD')
nt.links.new(mx.outputs["Shader"], ow.inputs["Surface"])
# ceu de dia encoberto: o que a camera ve e um branco-acinzentado, nao azul profundo
ceu_claro = nt.nodes.new("ShaderNodeBackground")
ceu_claro.inputs["Color"].default_value = (0.88, 0.90, 0.93, 1.0)
ceu_claro.inputs["Strength"].default_value = 1.0
mx_ceu = nt.nodes.new("ShaderNodeMixShader")
mx_ceu.inputs["Fac"].default_value = 0.78
nt.links.new(bg.outputs["Background"], mx_ceu.inputs[1])
nt.links.new(ceu_claro.outputs["Background"], mx_ceu.inputs[2])
nt.links.new(mx_ceu.outputs["Shader"], mx.inputs[2])
sol_d = bpy.data.lights.new("Sol", type='SUN')
sol_d.energy = 2.2
sol_d.angle = math.radians(5.0)
sol = bpy.data.objects.new("Sol", sol_d)
COLS["LUZ_E_CAMERAS"].objects.link(sol)
sol.rotation_euler = Euler((math.radians(90 - ELEV), 0, math.radians(180 - AZ)), 'XYZ')
scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Base Contrast'
except Exception:
    pass
scene.view_settings.exposure = -0.1

# ----------------------------------------------------------------- cameras
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
CX, CY = GX0 + LX / 2, GY0 + LY / 2


def solo_em(x, y):
    hit, loc, nrm, fi, o, mtx = scene.ray_cast(dg, Vector((x, y, 300)), Vector((0, 0, -1)), distance=800)
    return loc.z if hit else 0.0


GZ = solo_em(CX, CY)


def camera(nome, lente, pos, alvo):
    c = bpy.data.cameras.new(nome)
    c.lens = lente
    c.sensor_width = 36
    c.clip_start = 0.05
    c.clip_end = 4000
    o = bpy.data.objects.new(nome, c)
    COLS["LUZ_E_CAMERAS"].objects.link(o)
    o.location = pos
    d = Vector(alvo) - Vector(pos)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o


# CAM_REFERENCIA imita o enquadramento da foto de referencia: ~70 m, olhando ~38 graus para baixo, grande angular
cams = [
    camera("CAM_REFERENCIA", 22, (CX - 62, CY - 78, GZ + 68), (CX + 10, CY + 30, GZ + 6)),
    camera("CAM_NADIR_150m", 4.3 * 36 / 5.37, (CX, CY, GZ + 150), (CX, CY, GZ)),
    camera("CAM_OBLIQUA_100m", 24, (CX - 80, CY - 80, GZ + 100), (CX, CY, GZ + 4)),
    camera("CAM_RASANTE_25m", 24, (CX - 60, CY - 60, GZ + 25), (CX, CY, GZ + 6)),
    camera("CAM_BECO_8m", 20, (CX - 50, CY - 50, GZ + 9), (CX, CY, GZ + 6)),
]
scene.camera = cams[0]

scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons.get('cycles')
if prefs:
    for bt in ('OPTIX', 'CUDA'):
        try:
            prefs.preferences.compute_device_type = bt
            prefs.preferences.get_devices()
            if any(d.type == bt for d in prefs.preferences.devices):
                for d in prefs.preferences.devices:
                    d.use = (d.type == bt)
                break
        except Exception:
            pass
scene.cycles.device = 'GPU'
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 4
scene.cycles.volume_bounces = 0
scene.cycles.volume_step_rate = 4.0
scene.render.resolution_x, scene.render.resolution_y = args.res
scene.render.image_settings.media_type = 'IMAGE'
scene.render.image_settings.file_format = 'PNG'

# ----------------------------------------------------------------- nevoa por profundidade (compositor)
# perspectiva aerea como na foto: o que esta longe vai clareando e perdendo contraste.
if not args.sem_nevoa:
    try:
        scene.world.mist_settings.start = 90.0
        scene.world.mist_settings.depth = 1700.0
        scene.world.mist_settings.falloff = 'LINEAR'
        scene.view_layers[0].use_pass_mist = True
        ntc = None
        if hasattr(scene, "compositing_node_group"):
            ntc = bpy.data.node_groups.new("comp_nevoa", 'CompositorNodeTree')
            scene.compositing_node_group = ntc
        else:
            scene.use_nodes = True
            ntc = scene.node_tree
            for n in list(ntc.nodes):
                ntc.nodes.remove(n)
        # Blender 5: o compositor usa os nos genericos (ShaderNodeMix / ShaderNodeMath) e um NodeGroupOutput
        rl = ntc.nodes.new("CompositorNodeRLayers")
        mixn = ntc.nodes.new("ShaderNodeMix")
        mixn.data_type = 'RGBA'
        mixn.blend_type = 'MIX'
        mixn.inputs[7].default_value = (0.86, 0.88, 0.91, 1.0)
        mult = ntc.nodes.new("ShaderNodeMath")
        mult.operation = 'MULTIPLY'
        mult.inputs[1].default_value = 0.62
        ntc.links.new(rl.outputs["Mist"], mult.inputs[0])
        ntc.links.new(mult.outputs[0], mixn.inputs["Factor"])
        ntc.links.new(rl.outputs["Image"], mixn.inputs[6])
        if hasattr(scene, "compositing_node_group"):
            ntc.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
            comp = ntc.nodes.new("NodeGroupOutput")
            ntc.links.new(mixn.outputs[2], comp.inputs[0])
        else:
            comp = ntc.nodes.new("CompositorNodeComposite")
            ntc.links.new(mixn.outputs[2], comp.inputs["Image"])
        print("[cidade] nevoa por compositor ativa", flush=True)
    except Exception as e:
        print("[cidade] nevoa por compositor falhou:", e, flush=True)

for sc_ in bpy.data.screens:
    for area in sc_.areas:
        if area.type == 'VIEW_3D':
            sp = area.spaces.active
            sp.clip_start = 0.05
            sp.clip_end = 4000
            sp.shading.type = 'MATERIAL'

bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.out))
print(f"[cidade] salvo {args.out} ({os.path.getsize(args.out)/1e6:.0f} MB)", flush=True)

if args.preview:
    saida = os.path.join(os.path.dirname(os.path.abspath(args.out)), "cidade")
    os.makedirs(saida, exist_ok=True)
    for c in ((cams[0], cams[3]) if args.so_eval else cams):
        scene.camera = c
        scene.render.filepath = os.path.join(saida, c.name + ".png")
        bpy.ops.render.render(write_still=True)
        print("[cidade] render", c.name, flush=True)
print("[cidade] fim", flush=True)
