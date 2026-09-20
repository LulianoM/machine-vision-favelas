#!/usr/bin/env python3
"""
gen_morro.py: favela procedural num vale cercado de morro com mata, vista de drone a 150 m.

Por que existe: os tres bracos anteriores (v3 sobre OSM, odm sobre malha fotogrametrica e
cid150 sobre o DSM) ou dependem de dado da PCERJ ou tem quarteirao largo demais. Este aqui e
100% procedural sobre CC0 (Poly Haven), entao pode ilustrar o artigo, e persegue tres coisas
que a referencia aerea mostra e os anteriores nao tinham:

  1. BECO ESTREITO. O loteamento sai de uma subdivisao binaria em que a maioria das divisas e
     parede geminada (folga zero) e o resto vira beco de 0,7 a 2,6 m. Travessa de 3 a 4,6 m e
     rara. Vista de cima o beco vira uma fresta escura, que e a assinatura da favela.
  2. PALETA DE COBERTURA. Na foto aerea a cobertura e um mosaico: laje cinza, telha ceramica,
     azul forte de caixa d'agua e de lona, branco caiado, verde e amarelo. Os bracos anteriores
     saiam monocromaticos em laranja de bloco, o que nao se parece com o alvo.
  3. MORRO COM MATA EM VOLTA. O nucleo construido fica num vale e o terreno sobe nas bordas
     coberto de vegetacao, o que fecha o horizonte sem skyline postico e da ao detector um
     negativo util (copa de arvore nao e pessoa).

A malha da rua nao e ortogonal: o loteamento e gerado em grade e depois passa por uma
deformacao suave de dominio (domain warp), entao os becos entortam como no real sem que
nenhum lote fique concavo.

Escala: a camera Z30 a 150 m em nadir enquadra cerca de 187 x 105 m no chao, a 9,8 cm/px.
O nucleo construido tem cerca de 184 x 116 m, ou seja, enche o quadro com mata aparecendo nos
cantos. Uma pessoa de 1,7 m ocupa cerca de 17 px, dentro da faixa em que o ladrilhamento de
1280 px em escala nativa funciona.

Ainda NAO faz: pessoas e anotacao de bounding box. O proximo passo e plugar `people_mpfb.py`
e a projecao de vertice com ray cast de oclusao, que ja existem e nao dependem deste arquivo.

Uso:
  blender -b --python gen_morro.py -- --out C:\\arma3-favela\\blender\\morro --vistas nadir,obliqua,beco
  blender -b --python gen_morro.py -- --seed 12 --vistas nadir --samples 256
  blender -b --python gen_morro.py -- --save-blend C:\\arma3-favela\\blender\\morro\\morro.blend --no-render
"""
import argparse
import colorsys
import math
import os
import random
import sys

import numpy as np

import bpy
from mathutils import Euler, Vector

ASSETS = r"C:\arma3-favela\assets"

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default=r"C:\arma3-favela\blender\morro")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--alt", type=float, default=150.0, help="altura da camera nadir, em metros")
ap.add_argument("--samples", type=int, default=128)
ap.add_argument("--res", type=int, nargs=2, default=[1920, 1080])
ap.add_argument("--elev", type=float, default=66.0, help="elevacao do sol em graus")
ap.add_argument("--azim", type=float, default=35.0, help="azimute do sol em graus")
ap.add_argument("--vistas", default="nadir", help="nadir, obliqua, beco, contexto (separados por virgula)")
ap.add_argument("--arvores", type=int, default=2600)
ap.add_argument("--save-blend", default=None)
ap.add_argument("--no-render", action="store_true")
args = ap.parse_args(argv)

rng = random.Random(args.seed)
os.makedirs(args.out, exist_ok=True)

# geometria do sitio
NUC_A, NUC_B = 92.0, 58.0      # semi-eixos do nucleo construido, em metros
MORRO_H = 62.0                 # altura do morro que cerca o vale
AREA_X, AREA_Y = 250.0, 205.0  # semi-extensao do terreno modelado
PAV_H = 2.72                   # pe-direito medio de um pavimento


def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)


def s2l(h):
    """hex sRGB para linear, que e o espaco que o Blender espera em Base Color"""
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


# ================================================================= ruido e terreno
class Ruido:
    """ruido de valor com interpolacao suave, vetorizado. Substitui o noise do Blender para
    poder consultar o terreno em Python sem depender de ray cast."""

    def __init__(self, seed, n=256):
        self.n = n
        self.g = np.random.default_rng(seed).random((n, n)).astype(np.float64)

    def __call__(self, x, y, freq):
        n = self.n
        u = np.asarray(x, dtype=np.float64) * freq % n
        v = np.asarray(y, dtype=np.float64) * freq % n
        i0 = np.floor(u).astype(np.int64) % n
        j0 = np.floor(v).astype(np.int64) % n
        i1 = (i0 + 1) % n
        j1 = (j0 + 1) % n
        fu = u - np.floor(u)
        fv = v - np.floor(v)
        su = fu * fu * (3 - 2 * fu)
        sv = fv * fv * (3 - 2 * fv)
        a = self.g[j0, i0] * (1 - su) + self.g[j0, i1] * su
        b = self.g[j1, i0] * (1 - su) + self.g[j1, i1] * su
        return a * (1 - sv) + b * sv

    def fbm(self, x, y, freq, oct=4):
        s = 0.0
        amp = 1.0
        tot = 0.0
        f = freq
        for _ in range(oct):
            s = s + amp * self(x, y, f)
            tot += amp
            amp *= 0.5
            f *= 2.0
        return s / tot


NZ = Ruido(args.seed)


def raio(x, y):
    """distancia normalizada ao centro do nucleo, com a borda quebrada por ruido.
    Menor que 1 e area construida; acima de 1 comeca a subida do morro."""
    rx = np.asarray(x, dtype=np.float64) / NUC_A
    ry = np.asarray(y, dtype=np.float64) / NUC_B
    r = np.sqrt(rx * rx + ry * ry)
    return r * (0.88 + 0.26 * NZ.fbm(x, y, 1 / 90.0, 3))


def terreno(x, y):
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    r = raio(x, y)
    t = np.clip((r - 0.95) / 0.85, 0.0, 1.0)
    t = t * t * (3 - 2 * t)
    # Subida ASSIMETRICA. Um anel de mesma altura em volta vira cratera, que foi o erro da
    # primeira versao. Aqui o morro sobe muito mais de um lado, entao o nucleo construido fica
    # na meia encosta, que e onde favela de fato se assenta.
    lado = 0.5 + 0.5 * np.tanh((y + 0.55 * x) / 105.0)
    subida = MORRO_H * t ** 1.3 * (0.32 + 1.30 * lado)
    incl = 0.075 * y + 0.045 * x                                   # encosta suave no nucleo
    rug = 3.0 * (NZ.fbm(x + 500, y - 300, 1 / 55.0, 4) - 0.5) * 2   # ondulacao do vale
    cume = 13.0 * (NZ.fbm(x - 900, y + 700, 1 / 95.0, 4) - 0.5) * 2 * t  # relevo do morro
    return subida + incl + rug + cume


def warp(x, y):
    """deformacao suave de dominio: entorta a malha viaria sem tornar o lote concavo"""
    a = 3.2
    dx = (NZ.fbm(x + 2000, y + 1500, 1 / 85.0, 3) - 0.5) * 2 * a
    dy = (NZ.fbm(x - 1700, y + 900, 1 / 85.0, 3) - 0.5) * 2 * a
    return x + dx, y + dy


# ================================================================= cena vazia
# Tem de vir ANTES dos materiais: read_factory_settings descarta todo o datablock, entao
# qualquer material criado antes daqui viraria referencia morta.
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
COLS = {}
for _nome in ("TERRENO", "FAVELA", "MATA", "LUZ_E_CAMERAS"):
    _c = bpy.data.collections.new(_nome)
    scene.collection.children.link(_c)
    COLS[_nome] = _c

# ================================================================= materiais
import json  # noqa: E402  (depois dos helpers, para manter o topo legivel)

PH = json.load(open(os.path.join(ASSETS, "polyhaven", "index.json")))
TEX = {}
for _n, _e in PH["textures"].items():
    TEX.setdefault(_e["cat"], []).append(_n)


def img(rel, noncolor=False):
    i = bpy.data.images.load(os.path.join(ASSETS, "polyhaven", rel), check_existing=True)
    if noncolor:
        i.colorspace_settings.name = "Non-Color"
    return i


def _grime(nt, cor_out, forca):
    """mancha de umidade e escorrido vertical, que e a assinatura do concreto em clima tropical"""
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = rng.uniform(0.4, 1.3)
    nz.inputs["Detail"].default_value = 6
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position = 0.36
    rp.color_ramp.elements[0].color = (0.42, 0.40, 0.37, 1)
    rp.color_ramp.elements[1].position = 0.66
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = "RGBA"
    mx.blend_type = "MULTIPLY"
    mx.inputs["Factor"].default_value = forca
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], rp.inputs["Fac"])
    nt.links.new(cor_out, mx.inputs[6])
    nt.links.new(rp.outputs["Color"], mx.inputs[7])
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (6.0, 6.0, 0.35)
    nz2 = nt.nodes.new("ShaderNodeTexNoise")
    nz2.inputs["Scale"].default_value = 1.0
    nz2.inputs["Detail"].default_value = 3
    rp2 = nt.nodes.new("ShaderNodeValToRGB")
    rp2.color_ramp.elements[0].position = 0.55
    rp2.color_ramp.elements[0].color = (0.55, 0.52, 0.50, 1)
    rp2.color_ramp.elements[1].position = 0.70
    mx2 = nt.nodes.new("ShaderNodeMix")
    mx2.data_type = "RGBA"
    mx2.blend_type = "MULTIPLY"
    mx2.inputs["Factor"].default_value = forca * 0.7
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz2.inputs["Vector"])
    nt.links.new(nz2.outputs["Fac"], rp2.inputs["Fac"])
    nt.links.new(mx.outputs[2], mx2.inputs[6])
    nt.links.new(rp2.outputs["Color"], mx2.inputs[7])
    return mx2.outputs[2]


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
    d.projection = "BOX"
    d.projection_blend = 0.2
    nt.links.new(mp.outputs["Vector"], d.inputs["Vector"])
    cor = d.outputs["Color"]
    if tint is not None and forca_tint > 0:
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = "RGBA"
        mx.blend_type = "MULTIPLY"
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
        rg.projection = "BOX"
        nt.links.new(mp.outputs["Vector"], rg.inputs["Vector"])
        nt.links.new(rg.outputs["Color"], b.inputs["Roughness"])
    else:
        b.inputs["Roughness"].default_value = 0.9
    if "nor" in e:
        nr = nt.nodes.new("ShaderNodeTexImage")
        nr.image = img(e["nor"], True)
        nr.projection = "BOX"
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(mp.outputs["Vector"], nr.inputs["Vector"])
        nt.links.new(nr.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_bloco(nome, tom=0.0):
    """bloco ceramico de 6 furos assentado deitado (39 x 19 cm). Mapeamento por face:
    u = x|ny| + y|nx|, v = z, para o bloco ficar deitado em qualquer parede."""
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
    ax = nt.nodes.new("ShaderNodeMath"); ax.operation = "ABSOLUTE"
    ay = nt.nodes.new("ShaderNodeMath"); ay.operation = "ABSOLUTE"
    nt.links.new(sn.outputs["X"], ax.inputs[0])
    nt.links.new(sn.outputs["Y"], ay.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
    m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
    nt.links.new(sp.outputs["X"], m1.inputs[0]); nt.links.new(ay.outputs[0], m1.inputs[1])
    nt.links.new(sp.outputs["Y"], m2.inputs[0]); nt.links.new(ax.outputs[0], m2.inputs[1])
    ad = nt.nodes.new("ShaderNodeMath"); ad.operation = "ADD"
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
    nzv = nt.nodes.new("ShaderNodeTexNoise")
    nzv.inputs["Scale"].default_value = 3.0
    nzv.inputs["Detail"].default_value = 1
    rpv = nt.nodes.new("ShaderNodeValToRGB")
    rpv.color_ramp.elements[0].color = (0.82, 0.78, 0.76, 1)
    rpv.color_ramp.elements[1].color = (1.12, 1.08, 1.02, 1)
    mxv = nt.nodes.new("ShaderNodeMix")
    mxv.data_type = "RGBA"
    mxv.blend_type = "MULTIPLY"
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


def mat_simples(nome, cor, rough=0.85, metal=0.0):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (cor[0], cor[1], cor[2], 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def mat_mata(nome):
    """chao do morro: verde de mata com variacao de tom e de sombra, sem textura de folhagem
    (a biblioteca CC0 aqui nao tem uma). As copas por cima e que dao o volume."""
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.95
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.16
    nz.inputs["Detail"].default_value = 8
    nz.inputs["Roughness"].default_value = 0.62
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position = 0.34
    rp.color_ramp.elements[0].color = (*s2l("#1d3320"), 1)
    rp.color_ramp.elements[1].position = 0.70
    rp.color_ramp.elements[1].color = (*s2l("#4a6b33"), 1)
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], rp.inputs["Fac"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.5
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    nt.links.new(rp.outputs["Color"], b.inputs["Base Color"])
    return m


# ----------------------------------------------------------------- paleta calibrada na foto aerea
# Proporcoes lidas da referencia: a cobertura e um mosaico, nao um campo laranja. Laje de concreto
# em varios tons de cinza domina; telha ceramica, azul forte (caixa d'agua, lona, laje pintada),
# branco caiado e um punhado de cores saturadas compoem o resto.
# Os cinzas sao QUENTES: laje de concreto exposta ao sol do Rio puxa para o bege sujo, nao para
# o azul. Cinza frio foi o erro da primeira versao e deixou o conjunto com cara de maquete.
TELHA_PAL = [
    ("#c4b9a1", 11, "laje"), ("#ad9f87", 10, "laje"), ("#938672", 7, "laje"), ("#75695b", 3, "laje"),
    ("#d2cab6", 6, "fibro"), ("#b0aea4", 4, "zinco"),
    ("#c05b2c", 12, "ceramica"), ("#a04720", 8, "ceramica"), ("#d47e4c", 6, "ceramica"),
    ("#1f6dbe", 8, "pint"), ("#3a92d8", 4, "pint"), ("#2356a6", 3, "lona"),
    ("#ebe6d6", 7, "pint"), ("#e8e2d0", 4, "pint"),
    ("#bd3e28", 3, "pint"), ("#e0b95c", 2, "pint"), ("#cf8468", 2, "pint"),
]

MATS = []          # lista de materiais na ordem dos slots do objeto principal


def slot(m):
    MATS.append(m)
    return len(MATS) - 1


# fachada: bloco ceramico aparente domina, reboco pintado e concreto completam
I_FACHADA = []
for i in range(7):
    I_FACHADA += [slot(mat_bloco(f"bloco{i}", tom=rng.uniform(-0.012, 0.012)))] * 3
PAL_PAREDE = [(0.58, 0.45, 0.72), (0.33, 0.40, 0.60), (0.14, 0.60, 0.80), (0.06, 0.50, 0.60),
              (0.0, 0.0, 0.84), (0.0, 0.0, 0.66), (0.10, 0.28, 0.82), (0.45, 0.28, 0.62)]
for i, (h_, s_, v_) in enumerate(PAL_PAREDE):
    I_FACHADA.append(slot(mat_pbr(f"reboco{i}", rng.choice(TEX["plaster"]), rng.uniform(1.4, 2.4),
                                  tint=hsv(h_, s_, v_), forca_tint=rng.uniform(0.72, 0.95),
                                  sujeira=rng.uniform(0.35, 0.7))))
for i, t in enumerate(rng.sample(TEX["concrete"], 4)):
    I_FACHADA += [slot(mat_pbr(f"concreto{i}", t, rng.uniform(1.6, 2.4), sujeira=rng.uniform(0.4, 0.75)))] * 2

# cobertura, pelos pesos da referencia
I_TELHA = []
for i, (hexcor, peso, tipo) in enumerate(TELHA_PAL):
    cor = s2l(hexcor)
    if tipo == "laje":
        m = mat_pbr(f"telha_laje{i}", rng.choice(TEX["laje"]), rng.uniform(2.0, 3.0),
                    tint=cor, forca_tint=0.88, sujeira=rng.uniform(0.3, 0.6))
    elif tipo == "fibro":
        m = mat_pbr(f"telha_fibro{i}", rng.choice(TEX["roof_metal"]), rng.uniform(1.0, 1.4),
                    tint=cor, forca_tint=0.88, sujeira=rng.uniform(0.25, 0.45), metal=0.05)
    elif tipo == "zinco":
        m = mat_pbr(f"telha_zinco{i}", rng.choice(TEX["roof_metal"]), 1.1,
                    tint=cor, forca_tint=0.85, sujeira=0.25, metal=0.6, rough_fixo=0.4)
    elif tipo == "ceramica":
        m = mat_pbr(f"telha_cer{i}", rng.choice(TEX["roof_tile"]), rng.uniform(0.9, 1.3),
                    tint=cor, forca_tint=0.8, sujeira=rng.uniform(0.25, 0.45))
    elif tipo == "lona":
        m = mat_simples(f"telha_lona{i}", cor, rough=0.55)
    else:  # laje pintada
        m = mat_pbr(f"telha_pint{i}", rng.choice(TEX["laje"]), rng.uniform(2.2, 3.2),
                    tint=cor, forca_tint=0.95, sujeira=rng.uniform(0.2, 0.45))
    I_TELHA += [slot(m)] * peso
I_LAJE_CRUA = slot(mat_pbr("laje_crua", rng.choice(TEX["laje"]), 2.4,
                           tint=s2l("#a89a86"), forca_tint=0.8, sujeira=0.6))

I_ESTRUT = slot(mat_pbr("estrutura", "concrete_wall_006", 1.8, tint=(0.62, 0.61, 0.58),
                        forca_tint=0.6, sujeira=0.5))
I_FIBRO_CLARO = slot(mat_simples("fibro_claro", s2l("#cfcabd"), rough=0.7))
I_CXAZUL = slot(mat_simples("caixa_azul", s2l("#1a5fa8"), rough=0.5))
I_CXPRETA = slot(mat_simples("caixa_preta", s2l("#26262a"), rough=0.55))
I_GRADE = slot(mat_simples("grade", (0.05, 0.05, 0.055), rough=0.6, metal=0.5))
I_VIDRO = slot(mat_simples("vao", (0.015, 0.015, 0.02), rough=0.35))
I_PORTA = [slot(mat_simples("porta_mad", s2l("#5a3a22"), rough=0.7)),
           slot(mat_simples("portao_met", s2l("#3d4246"), rough=0.45, metal=0.55)),
           slot(mat_simples("portao_verm", s2l("#8a2f24"), rough=0.5, metal=0.35))]
I_FIO = slot(mat_simples("fio", (0.02, 0.02, 0.02), rough=0.7))
I_ROUPA = [slot(mat_simples(f"roupa{i}", hsv(rng.random(), rng.uniform(0.35, 0.9), rng.uniform(0.35, 0.95)),
                            rough=0.9)) for i in range(6)]
I_CHAO = slot(mat_pbr("chao_beco", "concrete_pavement_02" if "concrete_pavement_02" in PH["textures"]
                      else TEX["ground"][0], 2.4, sujeira=0.7))


def escolha(lista):
    return rng.choice(lista)


# ================================================================= acumulador de geometria
class Acc:
    """junta tudo num unico mesh com indice de material por face. Uma malha so e muito mais
    rapida de avaliar que milhares de objetos, e a 150 m nao perdemos nada com isso."""

    def __init__(self):
        self.v = []
        self.f = []
        self.m = []

    def quad(self, pts, mi):
        n = len(self.v)
        self.v.extend(pts)
        self.f.append((n, n + 1, n + 2, n + 3))
        self.m.append(mi)

    def prisma(self, cantos, z0, z1, mi_par, mi_topo):
        for i in range(4):
            a = cantos[i]
            b = cantos[(i + 1) % 4]
            self.quad([(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)], mi_par)
        self.quad([(c[0], c[1], z1) for c in cantos], mi_topo)

    def caixa(self, cx, cy, cz, sx, sy, sz, mi, rot=0.0):
        co, si = math.cos(rot), math.sin(rot)
        hx, hy, hz = sx / 2, sy / 2, sz / 2
        p = []
        for dx, dy, dz in ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
                           (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)):
            x, y = dx * hx, dy * hy
            p.append((cx + x * co - y * si, cy + x * si + y * co, cz + dz * hz))
        for a, b, c, d in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2),
                           (2, 6, 7, 3), (3, 7, 4, 0)):
            self.quad([p[a], p[b], p[c], p[d]], mi)

    def fio(self, p0, p1, raio_, mi, barriga=0.35, n=5):
        ant = None
        for k in range(n + 1):
            t = k / n
            x = p0[0] + (p1[0] - p0[0]) * t
            y = p0[1] + (p1[1] - p0[1]) * t
            z = p0[2] + (p1[2] - p0[2]) * t - barriga * math.sin(math.pi * t)
            if ant is not None:
                dx, dy = x - ant[0], y - ant[1]
                L = math.hypot(dx, dy) or 1e-6
                nx, ny = -dy / L * raio_, dx / L * raio_
                self.quad([(ant[0] + nx, ant[1] + ny, ant[2]), (x + nx, y + ny, z),
                           (x - nx, y - ny, z), (ant[0] - nx, ant[1] - ny, ant[2])], mi)
            ant = (x, y, z)

    def objeto(self, nome, colecao):
        me = bpy.data.meshes.new(nome)
        me.from_pydata([list(p) for p in self.v], [], [list(f) for f in self.f])
        for m in MATS:
            me.materials.append(m)
        me.polygons.foreach_set("material_index", self.m)
        me.update()
        ob = bpy.data.objects.new(nome, me)
        colecao.objects.link(ob)
        return ob


# ================================================================= terreno
RES_T = 2.0
nx = int(2 * AREA_X / RES_T) + 1
ny = int(2 * AREA_Y / RES_T) + 1
gx = np.linspace(-AREA_X, AREA_X, nx)
gy = np.linspace(-AREA_Y, AREA_Y, ny)
GX, GY = np.meshgrid(gx, gy)
GZ = terreno(GX, GY)
GR = raio(GX, GY)

verts = np.stack([GX.ravel(), GY.ravel(), GZ.ravel()], axis=1)
idx = np.arange(nx * ny).reshape(ny, nx)
faces = np.stack([idx[:-1, :-1].ravel(), idx[:-1, 1:].ravel(),
                  idx[1:, 1:].ravel(), idx[1:, :-1].ravel()], axis=1)
# uma face e mata quando o centro dela esta fora do nucleo construido
rc = 0.25 * (GR[:-1, :-1] + GR[:-1, 1:] + GR[1:, 1:] + GR[1:, :-1]).ravel()

me = bpy.data.meshes.new("Terreno")
me.from_pydata(verts.tolist(), [], faces.tolist())
# O chao do beco e cimento sujo e escuro, nao terra clara. Chao claro vira mancha branca vista
# de cima e destroi a leitura de tecido continuo.
me.materials.append(mat_pbr("chao_beco_terreno", "concrete_pavement_02" if "concrete_pavement_02"
                            in PH["textures"] else TEX["ground"][0], 2.2,
                            tint=s2l("#585349"), forca_tint=0.85, sujeira=0.8))
me.materials.append(mat_mata("mata_chao"))
me.polygons.foreach_set("material_index", (rc > 0.92).astype(np.int32).tolist())
me.update()
ob_ter = bpy.data.objects.new("Terreno", me)
COLS["TERRENO"].objects.link(ob_ter)
print(f"[morro] terreno {nx} x {ny} celulas de {RES_T} m, z {GZ.min():.1f}..{GZ.max():.1f} m", flush=True)


def z_em(x, y):
    """altura do terreno num ponto, por interpolacao bilinear na mesma grade do mesh"""
    u = (x + AREA_X) / RES_T
    v = (y + AREA_Y) / RES_T
    i0 = int(np.clip(math.floor(u), 0, nx - 2))
    j0 = int(np.clip(math.floor(v), 0, ny - 2))
    fu, fv = u - i0, v - j0
    a = GZ[j0, i0] * (1 - fu) + GZ[j0, i0 + 1] * fu
    b = GZ[j0 + 1, i0] * (1 - fu) + GZ[j0 + 1, i0 + 1] * fu
    return float(a * (1 - fv) + b * fv)


# ----------------------------------------------------------------- loteamento com becos
def folga():
    """largura da divisa. A maioria e parede geminada, que e o que fecha o tecido."""
    u = rng.random()
    if u < 0.64:
        return 0.0
    if u < 0.91:
        return rng.uniform(0.6, 1.3)
    if u < 0.985:
        return rng.uniform(1.4, 2.2)
    return rng.uniform(2.5, 3.4)


def bsp(x0, y0, x1, y1, prof, out):
    w, h = x1 - x0, y1 - y0
    # Lote de favela e pequeno: a referencia aerea tem casa de 4 x 7 a 8 x 11 m, nao quarteirao.
    # Parar cedo demais aqui foi o que deixou a primeira versao com cara de conjunto habitacional.
    if prof >= 13 or w * h < rng.uniform(22, 62) or min(w, h) < 3.6:
        if w > 2.2 and h > 2.2:
            out.append((x0, y0, x1, y1))
        return
    vert = w >= h if abs(w - h) > 1.5 else rng.random() < 0.5
    t = rng.uniform(0.34, 0.66)
    g = folga() / 2
    if vert:
        xm = x0 + w * t
        bsp(x0, y0, xm - g, y1, prof + 1, out)
        bsp(xm + g, y0, x1, y1, prof + 1, out)
    else:
        ym = y0 + h * t
        bsp(x0, y0, x1, ym - g, prof + 1, out)
        bsp(x0, ym + g, x1, y1, prof + 1, out)


sys.setrecursionlimit(5000)

# ---- bairros: cada um tem orientacao propria, e a divisa entre eles e um diagrama de Voronoi.
# Uma subdivisao unica, por mais deformada que seja, deixa fileiras retas legiveis de 10 e 20
# casas, que e o sinal mais forte de geracao procedural numa vista de cima. Favela consolidada
# cresce por nucleos que se encontram em angulo, e e isso que esta reproduzido aqui.
N_BAIRRO = 9
SEEDS = []
while len(SEEDS) < N_BAIRRO:
    sx = rng.uniform(-NUC_A, NUC_A)
    sy = rng.uniform(-NUC_B, NUC_B)
    if all((sx - a) ** 2 + (sy - b) ** 2 > 34 ** 2 for a, b, _ in SEEDS):
        SEEDS.append((sx, sy, rng.uniform(0, math.pi)))


def bairro_de(x, y):
    """indice do bairro mais proximo e folga ate o segundo, para evitar lote em cima da divisa"""
    d = sorted(((x - a) ** 2 + (y - b) ** 2, k) for k, (a, b, _) in enumerate(SEEDS))
    return d[0][1], math.sqrt(d[1][0]) - math.sqrt(d[0][0])


LOTES = []
R_CORTE = math.hypot(NUC_A, NUC_B) + 18
for kb, (sxb, syb, angb) in enumerate(SEEDS):
    locais = []
    bsp(-R_CORTE, -R_CORTE, R_CORTE, R_CORTE, 0, locais)
    co, si = math.cos(angb), math.sin(angb)
    for (x0, y0, x1, y1) in locais:
        # canto no referencial do mundo, girado em torno da semente do bairro
        cant = []
        for (px, py) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            cant.append((sxb + px * co - py * si, syb + px * si + py * co))
        cx_ = sum(p[0] for p in cant) / 4
        cy_ = sum(p[1] for p in cant) / 4
        k_, folga_ = bairro_de(cx_, cy_)
        if k_ != kb or folga_ < 0.6:
            continue                      # pertence a outro bairro, ou esta em cima da divisa
        LOTES.append(cant)
print(f"[morro] {len(LOTES)} lotes em {N_BAIRRO} bairros com orientacao propria", flush=True)

acc = Acc()
CASAS = []                     # (cantos, zbase, ztopo), usado depois para achar os becos
n_casa = n_cx = n_varal = 0

for cant0 in LOTES:
    cx = sum(p[0] for p in cant0) / 4
    cy = sum(p[1] for p in cant0) / 4
    if raio(cx, cy) > 0.97:
        continue                                    # fora do nucleo: fica para a mata
    if rng.random() < 0.02:
        continue                                    # vazio, quintal, laje de terreno
    cantos = [warp(px, py) for (px, py) in cant0]
    zs = [z_em(p[0], p[1]) for p in cantos] + [z_em(cx, cy)]
    zbase = min(zs) - 0.6
    # Numero de pavimentos por campo de ruido: favela tem ZONAS altas e zonas baixas, nao
    # altura sorteada casa a casa. O sorteio independente deixa a massa homogenea vista de cima.
    campo = float(NZ.fbm(cx + 3000, cy - 2000, 1 / 62.0, 3))
    pav = int(round(rng.gauss(1.0 + 4.0 * campo, 0.95)))
    pav = max(1, min(6, pav))
    alt = pav * rng.uniform(PAV_H - 0.14, PAV_H + 0.18)
    ztopo = zbase + 0.6 + alt
    mi_par = escolha(I_FACHADA)
    mi_tel = escolha(I_TELHA)

    # PUXADINHO. A casa de favela quase nunca e um prisma unico: o pavimento de cima e menor que
    # o de baixo e fica deslocado, deixando um pedaco de laje descoberto ao lado. Vista de cima
    # isso vira o recorte em L que define a textura da favela. Sem ele, a mancha fica com cara
    # de conjunto de caixas, que era o problema das versoes anteriores.
    fez_puxadinho = False
    if pav >= 2 and rng.random() < 0.55:
        fez_puxadinho = True
        n_baixo = rng.randint(1, max(1, pav - 1))
        alt_baixo = alt * n_baixo / pav
        z_meio = zbase + 0.6 + alt_baixo
        acc.prisma(cantos, zbase, z_meio, mi_par, escolha(I_TELHA))
        # bloco de cima: encolhido em um ou dois lados, encostado numa das divisas
        fx = rng.uniform(0.45, 0.82)
        fy = rng.uniform(0.45, 0.82)
        ox = rng.choice([0.0, 1.0 - fx])
        oy = rng.choice([0.0, 1.0 - fy])
        c0, c1, c3 = cantos[0], cantos[1], cantos[3]
        ux, uy = c1[0] - c0[0], c1[1] - c0[1]
        vx, vy = c3[0] - c0[0], c3[1] - c0[1]
        topo = []
        for (a_, b_) in ((ox, oy), (ox + fx, oy), (ox + fx, oy + fy), (ox, oy + fy)):
            topo.append((c0[0] + ux * a_ + vx * b_, c0[1] + uy * a_ + vy * b_))
        acc.prisma(topo, z_meio - 0.15, ztopo, mi_par, mi_tel)
        cantos_topo = topo
    else:
        acc.prisma(cantos, zbase, ztopo, mi_par, mi_tel)
        cantos_topo = cantos

    # o que vive na cobertura vai sobre a laje DE CIMA, que com puxadinho nao e a do lote
    lx = math.hypot(cantos_topo[1][0] - cantos_topo[0][0], cantos_topo[1][1] - cantos_topo[0][1])
    ly = math.hypot(cantos_topo[3][0] - cantos_topo[0][0], cantos_topo[3][1] - cantos_topo[0][1])
    ang = math.atan2(cantos_topo[1][1] - cantos_topo[0][1], cantos_topo[1][0] - cantos_topo[0][0])
    wcx = sum(p[0] for p in cantos_topo) / 4
    wcy = sum(p[1] for p in cantos_topo) / 4
    CASAS.append((cantos, zbase, ztopo))
    n_casa += 1

    # ---- esquadria: vao escuro com caixilho, na fachada. A 150 m vale pouco, na obliqua vale tudo.
    for lado in range(4):
        a, b = cantos[lado], cantos[(lado + 1) % 4]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 2.2:
            continue
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nxv, nyv = dy, -dx                            # normal para fora
        n_vaos = max(1, int(L / 2.6))
        for k in range(n_vaos):
            if rng.random() < 0.25:
                continue
            u = (k + 0.5) / n_vaos
            bx, by = a[0] + dx * L * u, a[1] + dy * L * u
            for p_ in range(pav):
                zc = zbase + 0.6 + p_ * (alt / pav) + 1.45
                if p_ == 0 and rng.random() < 0.3:
                    acc.caixa(bx + nxv * 0.05, by + nyv * 0.05, zbase + 0.6 + 1.05,
                              rng.uniform(0.9, 1.3), 0.12, 2.1, escolha(I_PORTA), ang + lado * math.pi / 2)
                    continue
                jw = rng.uniform(0.8, 1.4)
                jh = rng.uniform(1.0, 1.35)
                acc.caixa(bx - nxv * 0.09, by - nyv * 0.09, zc, jw, 0.2, jh, I_VIDRO, ang + lado * math.pi / 2)
                acc.caixa(bx + nxv * 0.04, by + nyv * 0.04, zc, jw + 0.12, 0.09, jh + 0.12,
                          I_ESTRUT, ang + lado * math.pi / 2)
                if rng.random() < 0.45:
                    for g_ in range(int(jw / 0.16)):
                        u2 = -jw / 2 + 0.08 + g_ * 0.16
                        acc.caixa(bx + nxv * 0.06 + dx * u2, by + nyv * 0.06 + dy * u2, zc,
                                  0.025, 0.025, jh, I_GRADE, ang + lado * math.pi / 2)

    # ---- cobertura: mureta, caixa d'agua, casinha de escada, ferragem de espera, varal
    r_ = rng.random()
    if r_ < 0.46:                                    # laje com mureta baixa
        ph = rng.uniform(0.35, 0.9)
        for lado in range(4):
            a, b = cantos_topo[lado], cantos_topo[(lado + 1) % 4]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            mx_, my_ = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            ang2 = math.atan2(b[1] - a[1], b[0] - a[0])
            acc.caixa(mx_, my_, ztopo + ph / 2, L, 0.12, ph, I_LAJE_CRUA, ang2)
    elif r_ < 0.70:                                  # duas aguas: a telha inclinada que a foto mostra
        # dois planos inclinados em torno da cumeeira, no eixo mais longo da casa
        h_cum = rng.uniform(0.5, 1.2)
        ao = ang if lx >= ly else ang + math.pi / 2
        la, lb = (lx, ly) if lx >= ly else (ly, lx)
        co, si = math.cos(ao), math.sin(ao)
        po, qo = -si, co                              # eixo transversal
        beir = rng.uniform(0.15, 0.45)
        for s_ in (-1, 1):
            p0 = (wcx - co * (la / 2 + beir) + po * s_ * (lb / 2 + beir),
                  wcy - si * (la / 2 + beir) + qo * s_ * (lb / 2 + beir), ztopo)
            p1 = (wcx + co * (la / 2 + beir) + po * s_ * (lb / 2 + beir),
                  wcy + si * (la / 2 + beir) + qo * s_ * (lb / 2 + beir), ztopo)
            p2 = (wcx + co * (la / 2 + beir), wcy + si * (la / 2 + beir), ztopo + h_cum)
            p3 = (wcx - co * (la / 2 + beir), wcy - si * (la / 2 + beir), ztopo + h_cum)
            acc.quad([p0, p1, p2, p3] if s_ > 0 else [p3, p2, p1, p0], mi_tel)
    elif r_ < 0.86:                                  # telha de fibrocimento plana sobre a laje
        acc.caixa(wcx, wcy, ztopo + 0.22, lx * 1.06, ly * 1.06, 0.1, mi_tel, ang)
        for s_ in (-1, 1):
            acc.caixa(wcx + s_ * lx * 0.4 * math.cos(ang), wcy + s_ * lx * 0.4 * math.sin(ang),
                      ztopo + 0.11, 0.09, 0.09, 0.22, I_ESTRUT, ang)

    if rng.random() < 0.5:                           # caixa d'agua, o marcador mais visivel a 150 m
        for _ in range(rng.choice([1, 1, 1, 1, 2])):
            d = rng.uniform(0.55, 0.9)
            px = wcx + rng.uniform(-0.3, 0.3) * lx
            py = wcy + rng.uniform(-0.3, 0.3) * ly
            acc.caixa(px, py, ztopo + d / 2 + 0.2, d, d, d,
                      I_CXAZUL if rng.random() < 0.6 else I_CXPRETA, rng.uniform(0, 3))
            n_cx += 1
    if rng.random() < 0.3:                           # casinha de escada
        acc.caixa(wcx + rng.uniform(-0.25, 0.25) * lx, wcy + rng.uniform(-0.25, 0.25) * ly,
                  ztopo + 1.1, rng.uniform(1.6, 2.4), rng.uniform(1.6, 2.4), 2.2, mi_par, ang)
    # ---- o resto do que vive numa laje. Laje vazia e o que mais denuncia cena sintetica:
    # na foto aerea quase toda laje tem alguma coisa em cima.
    if rng.random() < 0.34:                          # antena parabolica
        acc.caixa(wcx + rng.uniform(-0.35, 0.35) * lx, wcy + rng.uniform(-0.35, 0.35) * ly,
                  ztopo + 0.45, 0.72, 0.72, 0.12, I_FIBRO_CLARO, rng.uniform(0, 3))
    if rng.random() < 0.42:                          # telha e material empilhado num canto
        px = wcx + rng.uniform(-0.38, 0.38) * lx
        py = wcy + rng.uniform(-0.38, 0.38) * ly
        a_ = rng.uniform(0, 3)
        for k_ in range(rng.randint(2, 5)):
            acc.caixa(px, py, ztopo + 0.06 + k_ * 0.07, rng.uniform(1.0, 1.9),
                      rng.uniform(0.7, 1.2), 0.07, mi_tel, a_ + k_ * 0.07)
    if rng.random() < 0.3:                           # entulho e tralha solta
        for _ in range(rng.randint(2, 6)):
            s_ = rng.uniform(0.25, 0.6)
            acc.caixa(wcx + rng.uniform(-0.42, 0.42) * lx, wcy + rng.uniform(-0.42, 0.42) * ly,
                      ztopo + s_ / 2 + 0.03, s_, s_ * rng.uniform(0.6, 1.5), s_ * rng.uniform(0.4, 1.0),
                      rng.choice([I_ESTRUT, mi_par, I_CXPRETA]), rng.uniform(0, 3))
    if rng.random() < 0.22:                          # tanque de lavar roupa
        acc.caixa(wcx + rng.uniform(-0.3, 0.3) * lx, wcy + rng.uniform(-0.3, 0.3) * ly,
                  ztopo + 0.4, 1.1, 0.75, 0.8, I_FIBRO_CLARO, rng.uniform(0, 3))
    if pav < 5 and rng.random() < 0.55:              # ferragem de espera: a casa continua subindo
        for _ in range(rng.randint(3, 7)):
            acc.caixa(wcx + rng.uniform(-0.45, 0.45) * lx, wcy + rng.uniform(-0.45, 0.45) * ly,
                      ztopo + 0.45, 0.025, 0.025, 0.9, I_ESTRUT, 0)
    if rng.random() < 0.38 and min(lx, ly) > 3.0:    # varal, muito visivel em nadir
        ax_ = wcx - lx * 0.3 * math.cos(ang)
        ay_ = wcy - lx * 0.3 * math.sin(ang)
        bx_ = wcx + lx * 0.3 * math.cos(ang)
        by_ = wcy + lx * 0.3 * math.sin(ang)
        acc.fio((ax_, ay_, ztopo + 1.4), (bx_, by_, ztopo + 1.4), 0.015, I_FIO, barriga=0.12)
        for k in range(rng.randint(3, 7)):
            t = (k + 0.5) / 7
            px = ax_ + (bx_ - ax_) * t
            py = ay_ + (by_ - ay_) * t
            acc.caixa(px, py, ztopo + 1.05, rng.uniform(0.35, 0.6), 0.03, rng.uniform(0.5, 0.8),
                      escolha(I_ROUPA), ang)
        n_varal += 1

# ---- fiacao aerea atravessando os becos, que e outra assinatura forte da favela
for _ in range(220):
    x = rng.uniform(-NUC_A, NUC_A)
    y = rng.uniform(-NUC_B, NUC_B)
    if raio(x, y) > 0.95:
        continue
    ang = rng.uniform(0, math.tau)
    L = rng.uniform(7, 18)
    z = z_em(x, y) + rng.uniform(7.5, 12.5)
    acc.fio((x, y, z), (x + L * math.cos(ang), y + L * math.sin(ang), z + rng.uniform(-1.5, 1.5)),
            0.022, I_FIO, barriga=rng.uniform(0.5, 1.3))

ob_fav = acc.objeto("Favela", COLS["FAVELA"])
print(f"[morro] {n_casa} edificacoes, {n_cx} caixas d'agua, {n_varal} varais, "
      f"{len(acc.f)} faces", flush=True)

# ----------------------------------------------------------------- mata no morro
MODELOS = [n for n in ("jacaranda_tree", "tree_small_02", "island_tree_01", "island_tree_02")
           if n in PH["models"]]
arv = []
for nome in MODELOS:
    antes = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ASSETS, "polyhaven", PH["models"][nome]))
    novos = [o for o in set(bpy.data.objects) - antes if o.type == "MESH"]
    for o in novos:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        o.parent = None
        arv.append(o)
        o.hide_render = True
        o.hide_viewport = True
        COLS["MATA"].objects.link(o)
print(f"[morro] {len(arv)} modelos de arvore carregados de {len(MODELOS)} arquivos", flush=True)

if arv:
    postos = 0
    tent = 0
    while postos < args.arvores and tent < args.arvores * 30:
        tent += 1
        x = rng.uniform(-AREA_X * 0.86, AREA_X * 0.86)
        y = rng.uniform(-AREA_Y * 0.86, AREA_Y * 0.86)
        r = float(raio(x, y))
        if r < 1.0:
            continue                                # nada de mata dentro do nucleo construido
        src = rng.choice(arv)
        o = bpy.data.objects.new(src.name + f"_{postos}", src.data)
        COLS["MATA"].objects.link(o)
        o.location = (x, y, z_em(x, y) - 0.3)
        s = rng.uniform(0.75, 1.9)
        o.scale = (s, s, s * rng.uniform(0.85, 1.2))
        o.rotation_euler = Euler((0, 0, rng.uniform(0, math.tau)), "XYZ")
        postos += 1
    print(f"[morro] {postos} arvores instanciadas", flush=True)

# ----------------------------------------------------------------- luz e ceu
w = bpy.data.worlds.new("Ceu")
scene.world = w
w.use_nodes = True
nt = w.node_tree
bg = nt.nodes["Background"]
sky = nt.nodes.new("ShaderNodeTexSky")
for st in ("MULTIPLE_SCATTERING", "NISHITA"):
    try:
        sky.sky_type = st
        break
    except TypeError:
        continue
for a_, v_ in (("sun_elevation", math.radians(args.elev)), ("sun_rotation", math.radians(args.azim)),
               ("altitude", 20), ("air_density", 1.1), ("dust_density", 2.2), ("sun_intensity", 0.0)):
    try:
        setattr(sky, a_, v_)
    except Exception:
        pass
nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0

# Separar o que a camera VE do que ILUMINA. Um ceu Nishita limpo e azul profundo e, usado como
# unica fonte de ambiente, pinta toda a sombra de azul: foi o que deixou a primeira versao com
# aspecto de maquete fria. A camera continua vendo o ceu; a luz de preenchimento vira um ambiente
# neutro levemente quente, que e o que uma foto aerea do Rio mostra depois do balanco de branco.
amb = nt.nodes.new("ShaderNodeBackground")
amb.inputs["Color"].default_value = (1.0, 0.94, 0.85, 1.0)
amb.inputs["Strength"].default_value = 0.85
lp = nt.nodes.new("ShaderNodeLightPath")
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
nt.links.new(amb.outputs["Background"], mx.inputs[1])
nt.links.new(bg.outputs["Background"], mx.inputs[2])
ow = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
nt.links.new(mx.outputs["Shader"], ow.inputs["Surface"])

sol_d = bpy.data.lights.new("Sol", type="SUN")
sol_d.energy = 5.2
sol_d.color = (1.0, 0.96, 0.90)
sol_d.angle = math.radians(0.6)      # disco solar real: sombra dura, que e o que escurece o beco
sol = bpy.data.objects.new("Sol", sol_d)
COLS["LUZ_E_CAMERAS"].objects.link(sol)
sol.rotation_euler = Euler((math.radians(90 - args.elev), 0, math.radians(180 - args.azim)), "XYZ")

scene.view_settings.view_transform = "AgX"
for look in ("AgX - Punchy", "AgX - Medium High Contrast", "AgX - Base Contrast"):
    try:
        scene.view_settings.look = look
        break
    except Exception:
        continue
scene.view_settings.exposure = 1.6

# ----------------------------------------------------------------- cameras
Z30_LENS = 4.3 * 36 / 5.37            # 4.3 mm num sensor de 5.37 mm, ou seja ~28,8 mm equivalente


def camera(nome, lente, pos, alvo):
    c = bpy.data.cameras.new(nome)
    c.lens = lente
    c.sensor_width = 36
    c.sensor_fit = "HORIZONTAL"
    c.clip_start = 0.05
    c.clip_end = 3000
    o = bpy.data.objects.new(nome, c)
    COLS["LUZ_E_CAMERAS"].objects.link(o)
    o.location = pos
    d = Vector(alvo) - Vector(pos)
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return o


Z0 = z_em(0, 0)


# ---- mapa de ocupacao: onde NAO ha casa e o beco. Chutar a posicao da camera de beco nao
# funciona, ela nasce dentro de parede ou em cima do morro. Aqui o beco e achado de fato.
GB = 0.25
BX0, BY0 = -NUC_A - 16, -NUC_B - 16
BNX = int(2 * (NUC_A + 16) / GB)
BNY = int(2 * (NUC_B + 16) / GB)
occ = np.zeros((BNY, BNX), dtype=bool)
for _cant, _zb, _zt in CASAS:
    xs = [p[0] for p in _cant]
    ys = [p[1] for p in _cant]
    i0 = max(0, int((min(xs) - BX0) / GB) - 1)
    i1 = min(BNX, int((max(xs) - BX0) / GB) + 2)
    j0 = max(0, int((min(ys) - BY0) / GB) - 1)
    j1 = min(BNY, int((max(ys) - BY0) / GB) + 2)
    if i1 <= i0 or j1 <= j0:
        continue
    MX, MY = np.meshgrid(BX0 + (np.arange(i0, i1) + 0.5) * GB,
                         BY0 + (np.arange(j0, j1) + 0.5) * GB)
    pos = np.ones(MX.shape, dtype=bool)
    neg = np.ones(MX.shape, dtype=bool)
    for k in range(4):
        a, b = _cant[k], _cant[(k + 1) % 4]
        cr = (b[0] - a[0]) * (MY - a[1]) - (b[1] - a[1]) * (MX - a[0])
        pos &= cr >= 0
        neg &= cr <= 0
    occ[j0:j1, i0:i1] |= (pos | neg)


def corrida(m, eixo):
    """comprimento, em celulas, da faixa livre contigua que contem cada celula"""
    t = m if eixo == 1 else m.T
    n = t.shape[1]
    esq = np.zeros(t.shape, dtype=np.int32)
    a = np.zeros(t.shape[0], dtype=np.int32)
    for i in range(n):
        a = np.where(t[:, i], a + 1, 0)
        esq[:, i] = a
    dir_ = np.zeros(t.shape, dtype=np.int32)
    a = np.zeros(t.shape[0], dtype=np.int32)
    for i in range(n - 1, -1, -1):
        a = np.where(t[:, i], a + 1, 0)
        dir_[:, i] = a
    r = np.where(t, esq + dir_ - 1, 0)
    return r if eixo == 1 else r.T


livre = ~occ
RH = corrida(livre, 1)
RV = corrida(livre, 0)
# beco: faixa de 1,2 a 2,8 m de largura e pelo menos 9 m de comprimento. Abaixo de 1,2 m entre
# paredes de 12 m a fresta nao recebe luz nenhuma e a vista sai preta, sem servir para nada.
BECO_V = (RH >= 5) & (RH <= 11) & (RV >= 36)    # corre no sentido de y
BECO_H = (RV >= 5) & (RV <= 11) & (RH >= 36)    # corre no sentido de x
cand = np.argwhere(BECO_V | BECO_H)
print(f"[morro] {len(cand)} celulas de beco estreito no mapa de ocupacao "
      f"({100*occ.mean():.0f}% do recorte e construido)", flush=True)

if len(cand):
    # entre os candidatos, o mais proximo do centro, para a vista pegar o miolo
    jj, ii = cand[:, 0], cand[:, 1]
    bx = BX0 + (ii + 0.5) * GB
    by = BY0 + (jj + 0.5) * GB
    k = int(np.argmin(bx * bx + by * by))
    PBX, PBY = float(bx[k]), float(by[k])
    ao_longo_y = bool(BECO_V[jj[k], ii[k]])
    d = (0.0, 1.0) if ao_longo_y else (1.0, 0.0)
    if rng.random() < 0.5:
        d = (-d[0], -d[1])
    ZB = z_em(PBX, PBY)
    beco_pos = (PBX, PBY, ZB + 1.55)
    beco_alvo = (PBX + d[0] * 26, PBY + d[1] * 26, ZB + 2.6)
    print(f"[morro] camera de beco em ({PBX:.1f}, {PBY:.1f}), "
          f"beco corre em {'y' if ao_longo_y else 'x'}", flush=True)
else:
    beco_pos, beco_alvo = (0, 0, Z0 + 2), (20, 0, Z0 + 2)

# A obliqua precisa ficar ACIMA da copa do morro: a primeira versao nasceu dentro da mata.
OBL = (-165.0, -215.0)
ZOBL = max(z_em(*OBL), Z0) + 145.0

CAMS = {
    "nadir": camera("CAM_NADIR_150m_Z30", Z30_LENS, (0, 0, Z0 + args.alt), (0, 0, Z0)),
    "obliqua": camera("CAM_OBLIQUA", 38.0, (OBL[0], OBL[1], ZOBL), (0, -5, Z0 + 8)),
    "beco": camera("CAM_BECO", 24.0, beco_pos, beco_alvo),
    "contexto": camera("CAM_CONTEXTO", 34.0, (-300, -360, Z0 + 235), (0, 0, Z0 + 15)),
}

larg = 2 * args.alt * (18.0 / Z30_LENS)
print(f"[morro] nadir a {args.alt:.0f} m enquadra {larg:.0f} x {larg*args.res[1]/args.res[0]:.0f} m "
      f"({larg/args.res[0]*100:.1f} cm/px); pessoa de 1,7 m ~ {1.7/(larg/args.res[0]):.0f} px", flush=True)

# ----------------------------------------------------------------- render
scene.render.engine = "CYCLES"
scene.render.resolution_x, scene.render.resolution_y = args.res
scene.render.image_settings.file_format = "PNG"
prefs = bpy.context.preferences.addons.get("cycles")
if prefs:
    for bt in ("OPTIX", "CUDA"):
        try:
            prefs.preferences.compute_device_type = bt
            prefs.preferences.get_devices()
            if any(d.type == bt for d in prefs.preferences.devices):
                for d in prefs.preferences.devices:
                    d.use = d.type in (bt, "CPU")
                break
        except Exception:
            continue
scene.cycles.device = "GPU"
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 10          # beco fundo so aparece com luz indireta de varios saltos
scene.cycles.diffuse_bounces = 8
scene.cycles.transmission_bounces = 4
scene.cycles.volume_bounces = 0

# Exposicao por vista: o beco esta cerca de 6 paradas abaixo da laje, e uma camera real
# compensaria isso. Sem o ajuste a vista sai preta mesmo com a luz correta.
EXPO = {"beco": 3.2, "obliqua": 0.3}
EXPO_BASE = scene.view_settings.exposure

if args.save_blend:
    os.makedirs(os.path.dirname(args.save_blend) or ".", exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=args.save_blend)
    print(f"[morro] cena salva em {args.save_blend}", flush=True)

if not args.no_render:
    for nome in [v.strip() for v in args.vistas.split(",") if v.strip()]:
        if nome not in CAMS:
            print(f"[morro] vista desconhecida: {nome}", flush=True)
            continue
        scene.camera = CAMS[nome]
        scene.view_settings.exposure = EXPO_BASE + EXPO.get(nome, 0.0)
        scene.render.filepath = os.path.join(args.out, f"{nome}.png")
        print(f"[morro] renderizando {nome} ...", flush=True)
        bpy.ops.render.render(write_still=True)
        print(f"[morro] gravado {scene.render.filepath}", flush=True)
print("[morro] fim", flush=True)
