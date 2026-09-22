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
import time

import numpy as np

import bpy
from bpy_extras.object_utils import world_to_camera_view
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
ap.add_argument("--dataset", type=int, default=0, help="quantas imagens de dataset YOLO gerar")
ap.add_argument("--climas", default="todos", help="regimes de tempo, separados por virgula")
ap.add_argument("--comparar-climas", action="store_true", help="um nadir por regime, mesmo enquadramento")
ap.add_argument("--people", type=int, nargs=2, default=[10, 26])
ap.add_argument("--pool", type=int, default=6, help="humanos MPFB distintos")
ap.add_argument("--val", type=float, default=0.15)
ap.add_argument("--min-vis", type=float, default=0.35)
ap.add_argument("--min-lado", type=float, default=0.002)
ap.add_argument("--mistura", type=float, nargs=3, default=[0.34, 0.33, 0.33],
                help="pesos das classes armada, desarmada e desarmada com objeto alongado")
ap.add_argument("--alt-jitter", type=float, default=6.0)
ap.add_argument("--porte-realista", action="store_true",
                help="objeto confundivel raramente em pose de tiro (8%% em vez de 42%%); "
                     "ver people_mpfb.make_person")
ap.add_argument("--pitch", type=float, nargs=2, default=[0.0, 3.5],
                help="inclinacao da camera em graus a partir do NADIR (0 = nadir puro)")
ap.add_argument("--obliqua", action="store_true",
                help="preset calibrado na geometria do VisDrone: camera obliqua e baixa, "
                     "para a caixa sair alta e estreita (h/w perto de 2,2) em vez de quadrada")
# Otimizacoes atras de flag, e nao editadas no lugar, para o A/B ficar reprodutivel: a mesma
# semente roda com e sem, e o teste_fidelidade.py compara as dez metricas nos dois. As tres
# suspeitas estao em 07-blender/PLANO-OTIMIZACAO.md e nenhuma foi medida em separado ainda.
ap.add_argument("--otimizado", action="store_true",
                help="liga as tres otimizacoes de uma vez: dado persistente, caixa de ar "
                     "encolhida e poda de arvore fora do quadro")
ap.add_argument("--persistente", action="store_true",
                help="use_persistent_data: a cena e construida uma vez e so as pessoas mudam "
                     "entre quadros; sem isso o Cycles ressincroniza tudo a cada imagem")
ap.add_argument("--nevoa-folga", type=float, default=190.0,
                help="quantos metros a caixa de ar sobe acima do ponto mais alto do terreno. "
                     "A camera fica a 150 m acima do terreno do centro, entao 190 e folga grande")
ap.add_argument("--podar-arvores", action="store_true",
                help="esconde do render a arvore fora do raio util da camera. Sao 2.600 num "
                     "sitio de 250x205 m e o quadro nadir cobre 187x105 m")
ap.add_argument("--start", type=int, default=0,
                help="retoma o dataset a partir deste indice, pulando o que ja existe. Hoje uma "
                     "queda em 113 de 180 perde as 113")
ap.add_argument("--sitio", type=int, default=-1,
                help="indice do sitio na colecao de sitios.py. -1 e o sitio historico, identico "
                     "ao que gerou ds_morro_4k, e serve de controle")
ap.add_argument("--save-blend", default=None)
ap.add_argument("--no-render", action="store_true")
args = ap.parse_args(argv)

# --otimizado e so um atalho para as tres. Deixar cada uma tambem isolada permite descobrir QUAL
# delas paga, que e o que PLANO-OTIMIZACAO.md diz nao estar medido.
if args.otimizado:
    args.persistente = True
    args.podar_arvores = True
    if args.nevoa_folga == 190.0:
        args.nevoa_folga = 40.0

# Preset OBLIQUO, calibrado na medicao do VisDrone TREINO. Medido em 106.396 caixas reais:
# largura mediana 13 px, altura 24 px, ou seja h/w de 1,95 (p90 em 3,00). Isso e pessoa EM PE
# vista de camera obliqua. O nosso nadir a 150 m da h/w de 0,98, que e planta de cabeca e ombro.
# A AREA em pixel e praticamente a mesma nos dois (301 contra 300 px2), mas a FORMA do alvo e
# outra, por um fator de 2,0, e e essa a diferenca que importa para o detector. Este preset
# existe para separar duas perguntas: o sintetico nao transfere, ou a geometria de captura e que
# nao bate?
#
# CORRECAO de 2026-09-22. Ate aqui o preset estava calibrado no split de VALIDACAO (13.969
# caixas, h/w 2,20), que e o conjunto de TESTE. Calibrar o gerador no conjunto de teste e
# circular: o resultado mede o quanto o alvo foi ajustado ao gabarito, nao o quanto a geometria
# de captura explica a transferencia. Pior, o texto do artigo ja afirmava que a calibracao era
# no treino, entao codigo e artigo discordavam. Agora e o treino, e os dois numeros ficam
# registrados para quem comparar: treino h/w 1,95, validacao 2,20.
if args.obliqua:
    args.alt = 60.0
    args.alt_jitter = 18.0
    args.pitch = [26.0, 52.0]      # alvo h/w 1,95, nao 2,20

rng = random.Random(args.seed)
os.makedirs(args.out, exist_ok=True)

# geometria do sitio
# geometria do sitio, vinda da colecao em sitios.py. O sitio -1 reproduz o gerador de antes de
# 2026-09-21, e serve de controle: mesma semente, mesmo lote.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitios  # noqa: E402

SITIO = sitios.sitio(args.sitio)
NUC_A, NUC_B = SITIO["nuc_a"], SITIO["nuc_b"]   # semi-eixos do nucleo construido, em metros
MORRO_H = SITIO["morro_h"]                      # altura do morro que cerca o vale
RELEVO = SITIO["relevo"]
AVENIDA = SITIO["avenida"]
AREA_X, AREA_Y = 250.0, 205.0  # semi-extensao do terreno modelado
PAV_H = 2.72                   # pe-direito medio de um pavimento
print(f"[morro] sitio {args.sitio}: {SITIO['nome']}, nucleo {NUC_A:.0f}x{NUC_B:.0f} m, "
      f"relevo {RELEVO}, mata {SITIO['mata']}, "
      f"avenida {'nao' if not AVENIDA else str(round(AVENIDA['larg'])) + ' m'}", flush=True)


def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)


def s2l(h, alb=1.0):
    """hex sRGB para linear, que e o espaco que o Blender espera em Base Color.

    `alb` existe por causa de um erro que custou duas iteracoes: a cor lida de uma FOTO ja e o
    resultado iluminado, nao o albedo da superficie. Usar #c4b9a1 (linear 0,50) como albedo de
    laje faz o telhado estourar de branco sob sol direto, porque concreto real reflete algo
    entre 0,20 e 0,35. Toda cor vinda da foto de referencia entra com alb em torno de 0,45."""
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return tuple(x * alb for x in lin)


ALB = 0.50          # fator global de albedo para cor lida de foto


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
    return r * (0.84 + 0.34 * NZ.fbm(x, y, 1 / 45.0, 4))


def _dist_avenida(x, y):
    """distancia perpendicular ao eixo da avenida. Vetorizado, aceita escalar ou array."""
    a = AVENIDA["ang"]
    # normal ao eixo; o eixo passa por um ponto deslocado do centro do nucleo
    nx, ny = -math.sin(a), math.cos(a)
    c = AVENIDA["desloc"] * NUC_B
    return np.abs(np.asarray(x, dtype=np.float64) * nx
                  + np.asarray(y, dtype=np.float64) * ny - c)


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

    if RELEVO == "plano":
        # Jacarezinho, que e o caso do artigo, e praticamente plano. A encosta do sitio historico
        # nao e universal e nao deve virar assinatura do que o detector chama de favela.
        subida = MORRO_H * t ** 1.3
        incl = 0.012 * y + 0.008 * x
        cume = 4.0 * (NZ.fbm(x - 900, y + 700, 1 / 95.0, 4) - 0.5) * 2 * t
    elif RELEVO == "encosta":
        # subida monotonica: o nucleo inteiro fica na rampa, como na Rocinha. Muda a silhueta do
        # alvo visto de cima, porque a pessoa esta num chao inclinado.
        subida = MORRO_H * (0.30 + 0.70 * t) * (0.25 + 1.05 * lado)
        incl = 0.190 * y + 0.115 * x
        cume = 9.0 * (NZ.fbm(x - 900, y + 700, 1 / 95.0, 4) - 0.5) * 2 * t
    elif RELEVO == "dois_morros":
        # dois cumes com um vale entre eles cortando o nucleo
        l2 = 0.5 + 0.5 * np.tanh((-y + 0.40 * x) / 95.0)
        subida = MORRO_H * t ** 1.3 * (0.28 + 0.80 * lado + 0.70 * l2)
        incl = 0.045 * y + 0.030 * x
        cume = 15.0 * (NZ.fbm(x - 900, y + 700, 1 / 78.0, 4) - 0.5) * 2 * t
    else:                                                          # morro, o sitio historico
        subida = MORRO_H * t ** 1.3 * (0.32 + 1.30 * lado)
        incl = 0.075 * y + 0.045 * x                               # encosta suave no nucleo
        cume = 13.0 * (NZ.fbm(x - 900, y + 700, 1 / 95.0, 4) - 0.5) * 2 * t  # relevo do morro

    rug = 3.0 * (NZ.fbm(x + 500, y - 300, 1 / 55.0, 4) - 0.5) * 2   # ondulacao do vale
    z = subida + incl + rug + cume

    # A avenida corta o nucleo, e uma via nao acompanha ondulacao de 3 m em 55 m: ela e aplainada
    # em corte e aterro. Sem isto o asfalto fica boiando ou enterrado, que e pior que nao ter via.
    if AVENIDA is not None:
        d = _dist_avenida(x, y)
        k = np.clip(1.0 - d / (AVENIDA["larg"] * 0.5 + AVENIDA["calcada"] + 4.0), 0.0, 1.0)
        k = k * k * (3 - 2 * k)
        z = z * (1 - k) + (subida + incl) * k

    return z


def warp(x, y):
    """deformacao de dominio: entorta a malha viaria sem tornar o lote concavo.
    Amplitude 3,2 m em comprimento de onda 85 m girava as divisas em 4 a 8 graus, o que nao
    chegava perto de dissolver a grade (48% da energia de aresta ficava em 0 e 90 graus).
    Com 9 m em 38 m o beco deixa de correr reto por 30 m."""
    a = 9.0
    dx = (NZ.fbm(x + 2000, y + 1500, 1 / 38.0, 4) - 0.5) * 2 * a
    dy = (NZ.fbm(x - 1700, y + 900, 1 / 38.0, 4) - 0.5) * 2 * a
    return x + dx, y + dy


# ================================================================= cena vazia
# Tem de vir ANTES dos materiais: read_factory_settings descarta todo o datablock, entao
# qualquer material criado antes daqui viraria referencia morta.
# NAO usar read_factory_settings: ele reseta as PREFERENCIAS e com isso desabilita a extensao
# MPFB, entao bpy.ops.mpfb.create_random_human deixa de existir e o dataset sai sem pessoa
# nenhuma. Limpeza manual da cena de partida faz o mesmo efeito sem tocar nas preferencias.
for _ob in list(bpy.data.objects):
    bpy.data.objects.remove(_ob, do_unlink=True)
for _co in list(bpy.data.collections):
    bpy.data.collections.remove(_co)
for _me in list(bpy.data.meshes):
    bpy.data.meshes.remove(_me)
for _ma in list(bpy.data.materials):
    bpy.data.materials.remove(_ma)
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
    rp.color_ramp.elements[1].color = (0.30, 0.28, 0.25, 1)
    # MIX em direcao a cor de sujeira, nao MULTIPLY. Dois MULTIPLY em cascata sobre um albedo
    # ja tingido derrubavam a cena inteira umas 2 paradas e meia.
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = "RGBA"
    mx.blend_type = "MIX"
    mx.inputs["Factor"].default_value = min(forca, 0.13)
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
    rp2.color_ramp.elements[1].color = (0.38, 0.36, 0.34, 1)
    mx2 = nt.nodes.new("ShaderNodeMix")
    mx2.data_type = "RGBA"
    mx2.blend_type = "MIX"
    mx2.inputs["Factor"].default_value = min(forca * 0.7, 0.13)
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
        # NAO multiplicar a cor alvo pela difusa: sao dois albedos, e o produto derruba o
        # branco caiado de 0,70 para 0,15, o que pintava a cena inteira de marrom. Aqui a
        # textura entra so como MODULACAO de luminancia (0,78 a 1,18) sobre a cor pretendida,
        # entao o albedo final cai de fato na cor que a paleta pediu.
        bw = nt.nodes.new("ShaderNodeRGBToBW")
        nt.links.new(d.outputs["Color"], bw.inputs[0])
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["From Min"].default_value = 0.08
        mr.inputs["From Max"].default_value = 0.85
        mr.inputs["To Min"].default_value = 0.78
        mr.inputs["To Max"].default_value = 1.18
        mr.clamp = True
        nt.links.new(bw.outputs[0], mr.inputs["Value"])
        alvo = nt.nodes.new("ShaderNodeMix")
        alvo.data_type = "RGBA"
        alvo.blend_type = "MULTIPLY"
        alvo.inputs["Factor"].default_value = 1.0
        alvo.inputs[6].default_value = (tint[0], tint[1], tint[2], 1)
        nt.links.new(mr.outputs["Result"], alvo.inputs[7])
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = "RGBA"
        mx.blend_type = "MIX"
        mx.inputs["Factor"].default_value = forca_tint
        nt.links.new(cor, mx.inputs[6])
        nt.links.new(alvo.outputs[2], mx.inputs[7])
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
    c1 = hsv(0.045 + tom, 0.70, 0.74)
    c2 = hsv(0.038 + tom, 0.64, 0.60)
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
    ("#c4b9a1", 9, "laje"), ("#ad9f87", 8, "laje"), ("#938672", 6, "laje"), ("#75695b", 3, "laje"),
    ("#d2cab6", 6, "fibro"), ("#b0aea4", 4, "zinco"),
    ("#cf5f24", 15, "ceramica"), ("#b04a18", 10, "ceramica"), ("#e08246", 8, "ceramica"),
    ("#6e6a63", 5, "fibro"), ("#8a4f30", 6, "zinco"), ("#8c8a84", 3, "fibro"),
    ("#1f6dbe", 10, "pint"), ("#3a92d8", 5, "pint"), ("#2356a6", 4, "lona"),
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
    I_FACHADA += [slot(mat_bloco(f"bloco{i}", tom=rng.uniform(-0.012, 0.012)))] * 1
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
    cor = s2l(hexcor, ALB)
    if tipo == "laje":
        m = mat_pbr(f"telha_laje{i}", rng.choice(TEX["laje"]), rng.uniform(2.0, 3.0),
                    tint=cor, forca_tint=0.92, sujeira=rng.uniform(0.3, 0.6))
    elif tipo == "fibro":
        m = mat_pbr(f"telha_fibro{i}", rng.choice(TEX["roof_metal"]), rng.uniform(1.0, 1.4),
                    tint=cor, forca_tint=0.88, sujeira=rng.uniform(0.25, 0.45), metal=0.05)
    elif tipo == "zinco":
        m = mat_pbr(f"telha_zinco{i}", rng.choice(TEX["roof_metal"]), 1.1,
                    tint=cor, forca_tint=0.85, sujeira=0.25, metal=0.6, rough_fixo=0.4)
    elif tipo == "ceramica":
        m = mat_pbr(f"telha_cer{i}", rng.choice(TEX["roof_tile"]), rng.uniform(0.9, 1.3),
                    tint=tuple(c * 1.12 for c in cor), forca_tint=0.95, sujeira=rng.uniform(0.18, 0.34))
    elif tipo == "lona":
        m = mat_simples(f"telha_lona{i}", cor, rough=0.55)
    else:  # laje pintada
        m = mat_pbr(f"telha_pint{i}", rng.choice(TEX["laje"]), rng.uniform(2.2, 3.2),
                    tint=cor, forca_tint=0.95, sujeira=rng.uniform(0.2, 0.45))
    I_TELHA += [slot(m)] * peso
I_LAJE_CRUA = slot(mat_pbr("laje_crua", rng.choice(TEX["laje"]), 2.4,
                           tint=s2l("#a89a86", ALB), forca_tint=0.8, sujeira=0.6))

I_ESTRUT = slot(mat_pbr("estrutura", "concrete_wall_006", 1.8, tint=(0.62, 0.61, 0.58),
                        forca_tint=0.6, sujeira=0.5))
I_FIBRO_CLARO = slot(mat_simples("fibro_claro", s2l("#cfcabd", ALB), rough=0.7))
# Confete azul era um dos dois sinais mais fortes de cena sintetica: 159 discos de matiz 215
# graus com desvio de apenas 4 graus e saturacao 0,473, cobrindo 3,57% do quadro em azul forte
# contra 0,80% da fotogrametria real, ou seja 4,5 vezes demais. Na foto real a caixa aparece
# pequena, fosca, e boa parte delas e cinza ou preta.
I_CAIXA = (
    [slot(mat_simples("caixa_azul", s2l("#4a7ba6", 0.52), rough=0.62))] * 6
    + [slot(mat_simples("caixa_azul_velha", s2l("#5d7f96", 0.48), rough=0.78))] * 3
    + [slot(mat_simples("caixa_preta", s2l("#33333a", 0.80), rough=0.60))] * 6
    + [slot(mat_simples("caixa_fibro", s2l("#b8b4a8", 0.55), rough=0.80))] * 5
)
I_CXPRETA = slot(mat_simples("caixa_preta_tampa", s2l("#26262a", 0.8), rough=0.55))
I_GRADE = slot(mat_simples("grade", (0.05, 0.05, 0.055), rough=0.6, metal=0.5))
I_VIDRO = slot(mat_simples("vao", (0.015, 0.015, 0.02), rough=0.35))
I_PORTA = [slot(mat_simples("porta_mad", s2l("#5a3a22", 0.8), rough=0.7)),
           slot(mat_simples("portao_met", s2l("#3d4246", 0.8), rough=0.45, metal=0.55)),
           slot(mat_simples("portao_verm", s2l("#8a2f24", 0.8), rough=0.5, metal=0.35))]
I_FIO = slot(mat_simples("fio", (0.055, 0.052, 0.050), rough=0.65))
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

    def cilindro(self, cx, cy, z0, raio_, h, mi, n=12, tampa_mi=None):
        """caixa d'agua e tambor sao CILINDROS. Cubo alinhado ao eixo, repetido em laje apos
        laje, foi apontado como um dos tres sinais mais fortes de cena sintetica."""
        fase = rng.uniform(0, math.tau)
        pts = [(cx + raio_ * math.cos(fase + k * math.tau / n),
                cy + raio_ * math.sin(fase + k * math.tau / n)) for k in range(n)]
        for k in range(n):
            a, b = pts[k], pts[(k + 1) % n]
            self.quad([(a[0], a[1], z0), (b[0], b[1], z0),
                       (b[0], b[1], z0 + h), (a[0], a[1], z0 + h)], mi)
        # tampa em leque, um pouco menor e levemente acima, como a tampa real
        tm = tampa_mi if tampa_mi is not None else mi
        for k in range(0, n, 2):
            a, b, c = pts[k], pts[(k + 1) % n], pts[(k + 2) % n]
            self.quad([(cx, cy, z0 + h + 0.04), (a[0], a[1], z0 + h),
                       (b[0], b[1], z0 + h), (c[0], c[1], z0 + h)], tm)

    def disco(self, cx, cy, cz, raio_, mi, incl=0.5, az=0.0, n=10):
        """antena parabolica: disco inclinado, que em nadir vira uma elipse clara"""
        ca, sa = math.cos(az), math.sin(az)
        ci, si_ = math.cos(incl), math.sin(incl)
        pts = []
        for k in range(n):
            t = k * math.tau / n
            lx_, ly_ = raio_ * math.cos(t), raio_ * math.sin(t)
            hx, hy, hz = lx_, ly_ * ci, ly_ * si_          # inclina em torno do eixo local x
            pts.append((cx + hx * ca - hy * sa, cy + hx * sa + hy * ca, cz + hz))
        for k in range(0, n, 2):
            self.quad([(cx, cy, cz), pts[k], pts[(k + 1) % n], pts[(k + 2) % n]], mi)

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
                            tint=s2l("#585349", 0.75), forca_tint=0.85, sujeira=0.8))
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
    if u < 0.82:
        return 0.0
    if u < 0.94:
        return rng.uniform(0.5, 1.2)
    if u < 0.992:
        return rng.uniform(1.3, 2.0)
    return rng.uniform(2.3, 3.1)


def bsp(x0, y0, x1, y1, prof, out):
    w, h = x1 - x0, y1 - y0
    # Lote de favela e pequeno: a referencia aerea tem casa de 4 x 7 a 8 x 11 m, nao quarteirao.
    # Parar cedo demais aqui foi o que deixou a primeira versao com cara de conjunto habitacional.
    if prof >= 13 or w * h < rng.uniform(26, 62) or min(w, h) < 3.4:
        if w > 3.0 and h > 3.0:
            out.append((x0, y0, x1, y1))
        return
    # cortar sempre o lado maior enquanto ele for mais que 2,2 vezes o menor: favela tem lote
    # ESTREITO E PROFUNDO (razao 1,8 a 2,5), nao quadrado. Alternar cegamente dava razao 1,57.
    if max(w, h) / max(min(w, h), 1e-6) > 2.2:
        vert = w > h
    else:
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
N_BAIRRO = SITIO['n_bairro']
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
n_fio = 0
CASAS = []                     # (cantos, zbase, ztopo), usado depois para achar os becos
n_casa = n_cx = n_varal = 0

for cant0 in LOTES:
    cx = sum(p[0] for p in cant0) / 4
    cy = sum(p[1] for p in cant0) / 4
    if raio(cx, cy) > 0.97:
        continue                                    # fora do nucleo: fica para a mata
    if AVENIDA is not None and _dist_avenida(cx, cy) < AVENIDA["larg"] * 0.5 + AVENIDA["calcada"]:
        continue                                    # caixa da via mais calcada: nao se constroi
    if rng.random() < SITIO['vazio']:
        continue                                   # vazio, quintal, laje de terreno
    # giro proprio de cada lote em torno do centroide, com encolhimento para os vizinhos
    # girados nao se interpenetrarem. Junto com o warp forte, e o que tira a assinatura
    # ortogonal que o validador mediu em 4,35 vezes o esperado de uma distribuicao isotropica.
    gir = rng.uniform(-0.17, 0.17)
    cg, sg = math.cos(gir), math.sin(gir)
    cant1 = []
    for (px, py) in cant0:
        dx_, dy_ = px - cx, py - cy
        L_ = math.hypot(dx_, dy_) or 1e-6
        enc = max(0.0, L_ - 0.15) / L_          # encolhe 15 cm em direcao ao centro
        rx_, ry_ = dx_ * enc, dy_ * enc
        cant1.append((cx + rx_ * cg - ry_ * sg, cy + rx_ * sg + ry_ * cg))
    cantos = [warp(px, py) for (px, py) in cant1]
    zs = [z_em(p[0], p[1]) for p in cantos] + [z_em(cx, cy)]
    zbase = min(zs) - 0.6
    # Numero de pavimentos por campo de ruido: favela tem ZONAS altas e zonas baixas, nao
    # altura sorteada casa a casa. O sorteio independente deixa a massa homogenea vista de cima.
    campo = float(NZ.fbm(cx + 3000, cy - 2000, 1 / 62.0, 3))
    pav = int(round(rng.gauss(SITIO['pav_base'] + SITIO['pav_amp'] * campo, 0.95)))
    pav = max(1, min(SITIO['pav_max'], pav))
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

    # ---- QUEBRA DE NIVEL NA LAJE. Face de telhado lisa acima de 25 m2 foi o item pior avaliado
    # (34% do quadro). Laje de favela quase nunca esta num plano so: uma metade e mais nova, ou
    # cobre um comodo acrescentado depois, e fica de 12 a 30 cm acima da outra.
    if rng.random() < 0.62 and lx > 3.5 and ly > 3.5:
        c0, c1, c2, c3 = cantos_topo
        t1, t2 = rng.uniform(0.3, 0.7), rng.uniform(0.3, 0.7)
        P1 = (c0[0] + (c1[0] - c0[0]) * t1, c0[1] + (c1[1] - c0[1]) * t1)
        P2 = (c2[0] + (c3[0] - c2[0]) * t2, c2[1] + (c3[1] - c2[1]) * t2)
        meia = [P1, c1, c2, P2] if rng.random() < 0.5 else [c0, P1, P2, c3]
        dz = rng.uniform(0.12, 0.30)
        acc.prisma(meia, ztopo - 0.05, ztopo + dz, I_LAJE_CRUA, escolha(I_TELHA))
        ztopo += dz
        cantos_topo = meia
        lx = math.hypot(meia[1][0] - meia[0][0], meia[1][1] - meia[0][1])
        ly = math.hypot(meia[3][0] - meia[0][0], meia[3][1] - meia[0][1])
        ang = math.atan2(meia[1][1] - meia[0][1], meia[1][0] - meia[0][0])
        wcx = sum(p[0] for p in meia) / 4
        wcy = sum(p[1] for p in meia) / 4

    # ---- cobertura: mureta, caixa d'agua, casinha de escada, ferragem de espera, varal
    r_ = rng.random()
    if r_ < 0.44:                                    # laje com platibanda
        ph = rng.uniform(0.35, 0.9)
        for lado in range(4):
            a, b = cantos_topo[lado], cantos_topo[(lado + 1) % 4]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            mx_, my_ = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            ang2 = math.atan2(b[1] - a[1], b[0] - a[0])
            acc.caixa(mx_, my_, ztopo + ph / 2, L, 0.20, ph, I_LAJE_CRUA, ang2)
    elif r_ < 0.70:                                  # duas aguas: a telha inclinada que a foto mostra
        # dois planos inclinados em torno da cumeeira, no eixo mais longo da casa
        h_cum = rng.uniform(0.5, 1.2)
        ao = ang if lx >= ly else ang + math.pi / 2
        la, lb = (lx, ly) if lx >= ly else (ly, lx)
        co, si = math.cos(ao), math.sin(ao)
        po, qo = -si, co                              # eixo transversal
        beir = rng.uniform(0.15, 0.45)
        # A agua NAO e um plano liso. Telha ceramica e fibrocimento tem canal e capa: a 9,74
        # cm/px a canaleta de 16 cm da quase 2 px de periodo, e sem ela a agua vira mancha
        # homogenea grande, que era 739 m2 de laranja liso e o pior item da rubrica.
        n_f = rng.randint(8, 13)
        for s_ in (-1, 1):
            for k_ in range(n_f):
                t0, t1 = k_ / n_f, (k_ + 1) / n_f
                dz = 0.03 if k_ % 2 else 0.0           # capa e canal alternados
                ptos = []
                for tt, alt_ in ((t0, 0.0), (t1, 0.0), (t1, 1.0), (t0, 1.0)):
                    # tt corre no sentido da cumeeira, alt_ do beiral para o cume
                    ex = -(la / 2 + beir) + (la + 2 * beir) * tt
                    ey = s_ * (lb / 2 + beir) * (1.0 - alt_)
                    ptos.append((wcx + co * ex + po * ey, wcy + si * ex + qo * ey,
                                 ztopo + h_cum * alt_ + dz))
                acc.quad(ptos if s_ > 0 else ptos[::-1], mi_tel)
        # cumeeira
        acc.caixa(wcx, wcy, ztopo + h_cum + 0.06, la + 2 * beir, 0.20, 0.12, mi_tel, ao)
    elif r_ < 0.86:                                  # telha de fibrocimento plana sobre a laje
        acc.caixa(wcx, wcy, ztopo + 0.22, lx * 1.06, ly * 1.06, 0.1, mi_tel, ang)
        for s_ in (-1, 1):
            acc.caixa(wcx + s_ * lx * 0.4 * math.cos(ang), wcy + s_ * lx * 0.4 * math.sin(ang),
                      ztopo + 0.11, 0.09, 0.09, 0.22, I_ESTRUT, ang)

    if rng.random() < 0.62:                          # caixa d'agua, o marcador mais visivel a 150 m
        for _ in range(rng.choice([1, 1, 1, 1, 2])):
            rr = rng.choice([rng.uniform(0.35, 0.45), rng.uniform(0.50, 0.62),
                             rng.uniform(0.68, 0.85)])      # 310 L, 500 L, 1000 L
            hh = rng.uniform(0.85, 1.25)
            px = wcx + rng.uniform(-0.32, 0.32) * lx
            py = wcy + rng.uniform(-0.32, 0.32) * ly
            mi_cx = escolha(I_CAIXA)
            # base de alvenaria: caixa d'agua quase nunca fica direto na laje
            if rng.random() < 0.55:
                acc.caixa(px, py, ztopo + 0.22, rr * 2.2, rr * 2.2, 0.44, mi_par, rng.uniform(0, 3))
                acc.cilindro(px, py, ztopo + 0.44, rr, hh, mi_cx, tampa_mi=mi_cx)
            else:
                acc.cilindro(px, py, ztopo + 0.05, rr, hh, mi_cx, tampa_mi=mi_cx)
            n_cx += 1
    if rng.random() < 0.3:                           # casinha de escada
        acc.caixa(wcx + rng.uniform(-0.25, 0.25) * lx, wcy + rng.uniform(-0.25, 0.25) * ly,
                  ztopo + 1.1, rng.uniform(1.6, 2.4), rng.uniform(1.6, 2.4), 2.2, mi_par, ang)
    # ---- o resto do que vive numa laje. Laje vazia e o que mais denuncia cena sintetica:
    # na foto aerea quase toda laje tem alguma coisa em cima.
    if rng.random() < 0.38:                          # antena parabolica, disco inclinado
        acc.disco(wcx + rng.uniform(-0.38, 0.38) * lx, wcy + rng.uniform(-0.38, 0.38) * ly,
                  ztopo + rng.uniform(0.35, 0.75), rng.uniform(0.32, 0.48), I_FIBRO_CLARO,
                  incl=rng.uniform(0.5, 0.95), az=rng.uniform(0, math.tau))
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
        acc.fio((ax_, ay_, ztopo + 1.4), (bx_, by_, ztopo + 1.4), 0.05, I_FIO, barriga=0.12)
        # numero, posicao e tamanho de peca aleatorios: o motivo de 7 retangulos igualmente
        # espacados, repetido identico dezenas de vezes, foi apontado como sinal de "kit de pecas"
        n_pc = rng.randint(2, 9)
        for k in range(n_pc):
            t = rng.uniform(0.06, 0.94)
            px = ax_ + (bx_ - ax_) * t
            py = ay_ + (by_ - ay_) * t
            acc.caixa(px, py, ztopo + 1.4 - rng.uniform(0.28, 0.5), rng.uniform(0.22, 0.62),
                      0.03, rng.uniform(0.35, 0.95), escolha(I_ROUPA), ang + rng.uniform(-0.2, 0.2))
        n_varal += 1

# ---- fiacao aerea atravessando os becos, que e outra assinatura forte da favela
# Ancorado no TELHADO, nao numa altura sorteada sobre o terreno: 41% dos fios nasciam abaixo da
# laje vizinha e ficavam presos dentro do predio. E com secao de feixe real (16 cm): 2,2 cm a
# 9,74 cm/px dava 0,45 px, sub-pixel, e a fiacao simplesmente nao aparecia na imagem.
def _ponta(ca):
    """ponto de amarracao na BORDA da laje, nao no centroide. Ancorar no centro fazia dezenas de
    lajes mostrarem estrelas de 3 a 5 hastes saindo exatamente do mesmo ponto no meio da
    cobertura, o que nenhuma rede eletrica real faz: o ramal encosta na quina ou na fachada."""
    k = rng.randrange(4)
    a, b = ca[k], ca[(k + 1) % 4]
    t = rng.choice([0.0, 0.5, 1.0, rng.uniform(0.15, 0.85)])
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


_pontas = {}
if CASAS:
    for _ in range(3000):
        ia = rng.randrange(len(CASAS))
        ib = rng.randrange(len(CASAS))
        if _pontas.get(ia, 0) >= 3 or _pontas.get(ib, 0) >= 3:
            continue                      # no maximo 3 fios por laje, senao vira aranha
        ca, _zb, zt = CASAS[ia]
        cb, _zb2, zt2 = CASAS[ib]
        x, y = _ponta(ca)
        x2, y2 = _ponta(cb)
        d = math.hypot(x2 - x, y2 - y)
        if not (5.0 < d < 22.0):
            continue
        z1 = zt + rng.uniform(0.6, 2.2)
        z2 = zt2 + rng.uniform(0.6, 2.2)
        acc.fio((x, y, z1), (x2, y2, z2), 0.08, I_FIO, barriga=rng.uniform(0.5, 1.4))
        n_fio += 1
        _pontas[ia] = _pontas.get(ia, 0) + 1
        _pontas[ib] = _pontas.get(ib, 0) + 1

# ----------------------------------------------------------------- avenida, quando o sitio tem
# Por que uma via principal entra na colecao de sitios: o VisDrone e um benchmark de TRAFEGO, e o
# nosso sitio historico nao tem asfalto nem carro nenhum. Sem esse elemento, a diferenca entre os
# dois dominios inclui "existe rua larga" alem de tudo o mais, e nao da para separar.
#
# Os carros sao construidos com primitivas, nao importados. A 150 m em 4K um carro tem cerca de
# 10 x 4 px, e nessa escala o que existe e a silhueta e a cor do teto, nao a modelagem. Um modelo
# detalhado custaria VRAM e tempo de render sem mudar um pixel. Isto e simplificacao declarada,
# nao descuido, e vale enquanto a camera ficar a 150 m; para voo baixo precisaria de modelo real.
n_carro = 0
if AVENIDA is not None:
    _ang = AVENIDA["ang"]
    _ex, _ey = math.cos(_ang), math.sin(_ang)          # direcao do eixo
    _nx, _ny = -math.sin(_ang), math.cos(_ang)         # normal
    _c = AVENIDA["desloc"] * NUC_B
    _meia = AVENIDA["larg"] * 0.5
    _L = math.hypot(AREA_X, AREA_Y) * 0.92

    mat_asf = mat_simples("asfalto", (0.021, 0.021, 0.023), rough=0.72)
    mat_cal = mat_simples("calcada", (0.095, 0.092, 0.086), rough=0.88)
    ia_asf = slot(mat_asf)
    ia_cal = slot(mat_cal)
    ia_faixa = slot(mat_simples("faixa_via", (0.52, 0.49, 0.38), rough=0.80))

    # a via segue o terreno em segmentos, senao atravessa o relevo
    _passo = 4.0
    _n = int(2 * _L / _passo)
    for _k in range(_n):
        t0 = -_L + _k * _passo
        t1 = t0 + _passo
        for (w0, w1, mi, dz) in ((-_meia, _meia, ia_asf, 0.06),
                                 (-_meia - AVENIDA["calcada"], -_meia, ia_cal, 0.20),
                                 (_meia, _meia + AVENIDA["calcada"], ia_cal, 0.20)):
            q = []
            for (tt, ww) in ((t0, w0), (t1, w0), (t1, w1), (t0, w1)):
                px = _ex * tt + _nx * (ww + _c)
                py = _ey * tt + _ny * (ww + _c)
                q.append((px, py, z_em(px, py) + dz))
            acc.quad(q, mi)
        # faixa central tracejada, so para o asfalto nao virar um retangulo chapado
        if _k % 3 == 0:
            q = []
            for (tt, ww) in ((t0 + 0.6, -0.16), (t1 - 0.6, -0.16), (t1 - 0.6, 0.16), (t0 + 0.6, 0.16)):
                px = _ex * tt + _nx * (ww + _c)
                py = _ey * tt + _ny * (ww + _c)
                q.append((px, py, z_em(px, py) + 0.08))
            acc.quad(q, ia_faixa)

    # CORES de carro. Deliberadamente na mesma familia de cinzas e tons foscos das lajes: se o
    # carro fosse vermelho vivo, o detector separaria carro de pessoa por cor, o que nao sobrevive
    # a imagem real. Mesma razao pela qual objetos_alongados.py usa a paleta das armas.
    CORES_CARRO = [(0.32, 0.33, 0.34), (0.55, 0.55, 0.56), (0.08, 0.08, 0.09),
                   (0.18, 0.20, 0.26), (0.42, 0.40, 0.37), (0.13, 0.22, 0.17),
                   (0.46, 0.44, 0.40), (0.23, 0.24, 0.25)]
    # Sortear tt numa faixa fixa e descartar o que cai fora do nucleo rejeitava dois tercos dos
    # carros, porque o eixo da via pode estar orientado no lado curto do nucleo. Com tentativas,
    # o numero pedido e o numero entregue.
    _tent_c = 0
    while n_carro < AVENIDA["carros"] and _tent_c < AVENIDA["carros"] * 40:
        _tent_c += 1
        tt = rng.uniform(-NUC_A * 1.15, NUC_A * 1.15)
        faixa = rng.choice([-1, 1])
        ww = faixa * rng.uniform(_meia * 0.22, _meia * 0.74)
        px = _ex * tt + _nx * (ww + _c)
        py = _ey * tt + _ny * (ww + _c)
        if float(raio(px, py)) > 1.15:
            continue
        _i = n_carro
        zc = z_em(px, py) + 0.08
        comp = rng.uniform(3.9, 4.9)
        larg = rng.uniform(1.65, 1.86)
        h1 = rng.uniform(0.62, 0.78)          # altura do corpo
        h2 = rng.uniform(0.46, 0.58)          # altura da cabine sobre o corpo
        mi_c = slot(mat_simples(f"carro_{_i}", rng.choice(CORES_CARRO),
                                rough=rng.uniform(0.18, 0.42)))
        a_ = _ang + (0 if faixa > 0 else math.pi) + rng.uniform(-0.03, 0.03)
        ca_, sa_ = math.cos(a_), math.sin(a_)

        acc.caixa(px, py, zc + h1 / 2, comp, larg, h1, mi_c, rot=a_)
        # cabine encurtada e deslocada, que e o que da a silhueta de carro vista de cima
        dl = rng.uniform(-0.35, 0.25)
        acc.caixa(px + dl * ca_, py + dl * sa_, zc + h1 + h2 / 2,
                  comp * rng.uniform(0.46, 0.56), larg * 0.86, h2, mi_c, rot=a_)
        n_carro += 1

ob_fav = acc.objeto("Favela", COLS["FAVELA"])
print(f"[morro] {n_casa} edificacoes, {n_cx} caixas d'agua, {n_varal} varais, "
      f"{n_fio} fios, {n_carro} carros, {len(acc.f)} faces", flush=True)

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

# Area de sorteio da arvore. Sem poda, o sitio inteiro; com poda, a UNIAO dos quadros que a
# camera pode enquadrar, que e o centro sorteado (ate 45% do semi-eixo do nucleo) mais a meia
# largura do quadro nadir. Arvore fora dessa uniao nao aparece em nenhuma imagem do dataset e so
# custa: sao 2.600 num sitio de 250x205 m e o quadro cobre 187x105 m, ou seja 3,6 vezes mais area
# do que a util. A poda vale para NADIR; vista de beco ou obliqua alcanca mais longe.
# Z30_LENS so e definido na secao da camera, mais abaixo; usar a constante aqui derrubou TODO
# render em 22/09 com NameError, com ou sem --podar-arvores. O valor e o mesmo: 4,3 mm num
# sensor de 5,37 mm, equivalente a 28,8 mm em 36 mm.
_meia_q = 150.0 * (18.0 / (4.3 * 36 / 5.37))
if args.podar_arvores:
    _arv_x = min(AREA_X * 0.86, NUC_A * 0.45 + _meia_q + 20.0)
    _arv_y = min(AREA_Y * 0.86, NUC_B * 0.45 + _meia_q * 0.5625 + 20.0)
    print(f"[morro] poda de arvore LIGADA: sorteio em {2 * _arv_x:.0f} x {2 * _arv_y:.0f} m "
          f"em vez de {2 * AREA_X * 0.86:.0f} x {2 * AREA_Y * 0.86:.0f} m", flush=True)
else:
    _arv_x, _arv_y = AREA_X * 0.86, AREA_Y * 0.86

if arv:
    postos = 0
    tent = 0
    while postos < args.arvores and tent < args.arvores * 30:
        tent += 1
        x = rng.uniform(-_arv_x, _arv_x)
        y = rng.uniform(-_arv_y, _arv_y)
        r = float(raio(x, y))
        # Tres regimes de mata. O anel em volta era o unico ate 2026-09-21 e virou assinatura:
        # o detector podia estar aprendendo "verde em volta de telhado" em vez de telhado.
        if SITIO["mata"] == "ausente":
            if r < 1.18:
                continue                      # so uma franja distante, o morro fica pelado
        elif SITIO["mata"] == "manchas":
            # manchas internas: capao de mato dentro do nucleo, alem do anel externo
            if r < 1.0:
                mancha = float(NZ.fbm(x + 7000, y - 4000, 1 / 40.0, 3))
                if mancha < 0.62 or rng.random() > 0.35:
                    continue
        elif r < 1.0 and rng.random() > 0.028:
            continue          # mangueira e bananeira entre lajes existem, clareira a machado nao
        if AVENIDA is not None and float(_dist_avenida(x, y)) < AVENIDA["larg"] * 0.5 + 1.0:
            continue                          # arvore no meio do asfalto, nao
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
amb.inputs["Color"].default_value = (0.82, 0.87, 1.00, 1.0)
amb.inputs["Strength"].default_value = 0.92
lp = nt.nodes.new("ShaderNodeLightPath")
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
nt.links.new(amb.outputs["Background"], mx.inputs[1])
nt.links.new(bg.outputs["Background"], mx.inputs[2])
ow = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
nt.links.new(mx.outputs["Shader"], ow.inputs["Surface"])

# AIRLIGHT. Nao havia NADA nos 150 m de ar entre camera e solo, e era isso que matava a sombra:
# 6,8 paradas entre sol e sombra, com 17% do quadro sem informacao nenhuma dentro. Ar umido do
# Rio poe de 2 a 4% de luz espalhada dentro de toda sombra a essa distancia. Isso corrige o
# contraste no lugar certo (a fisica da cena), nao no tone mapper.
#
# O volume vai numa CAIXA, nao no World: volume de World e ilimitado, entao o raio do sol
# atravessa distancia infinita de meio, a transmitancia vai a zero e a cena apaga por completo.
_vz0 = float(GZ.min()) - 12.0
_vz1 = float(GZ.max()) + args.nevoa_folga
# Todo raio de camera atravessa este meio com volume_bounces = 1, e volumetrico e o
# multiplicador classico de custo no Cycles. A folga de 190 m acima do ponto MAIS ALTO do
# morro e generosa: a camera esta a 150 m acima do terreno do CENTRO. Encolher reduz o
# caminho optico sem mexer no airlight que a camera de fato atravessa, mas mexe em tres das
# dez metricas de fidelidade (contraste, meio-tom e B/R da sombra), entao exige remedicao.
_me_v = bpy.data.meshes.new("Ar")
_vx, _vy = AREA_X * 1.02, AREA_Y * 1.02
_me_v.from_pydata(
    [(-_vx, -_vy, _vz0), (_vx, -_vy, _vz0), (_vx, _vy, _vz0), (-_vx, _vy, _vz0),
     (-_vx, -_vy, _vz1), (_vx, -_vy, _vz1), (_vx, _vy, _vz1), (-_vx, _vy, _vz1)], [],
    [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
_me_v.update()
_mat_ar = bpy.data.materials.new("Ar")
_mat_ar.use_nodes = True
_nta = _mat_ar.node_tree
for _n in list(_nta.nodes):
    if _n.type != "OUTPUT_MATERIAL":
        _nta.nodes.remove(_n)
_out_a = _nta.nodes[0]
_vs = _nta.nodes.new("ShaderNodeVolumeScatter")
_vs.inputs["Density"].default_value = 0.9e-4
_vs.inputs["Color"].default_value = (0.78, 0.85, 1.0, 1.0)
_vs.inputs["Anisotropy"].default_value = 0.35
_nta.links.new(_vs.outputs["Volume"], _out_a.inputs["Volume"])
_me_v.materials.append(_mat_ar)
_ob_ar = bpy.data.objects.new("Ar", _me_v)
COLS["LUZ_E_CAMERAS"].objects.link(_ob_ar)
_ob_ar.visible_shadow = False

sol_d = bpy.data.lights.new("Sol", type="SUN")
sol_d.energy = 5.0
sol_d.color = (1.0, 0.96, 0.90)
sol_d.angle = math.radians(0.6)      # disco solar real: sombra dura, que e o que escurece o beco
sol = bpy.data.objects.new("Sol", sol_d)
COLS["LUZ_E_CAMERAS"].objects.link(sol)
sol.rotation_euler = Euler((math.radians(90 - args.elev), 0, math.radians(180 - args.azim)), "XYZ")

scene.view_settings.view_transform = "AgX"
for look in ("AgX - Medium High Contrast", "AgX - Base Contrast", "AgX - Punchy"):
    try:
        scene.view_settings.look = look
        break
    except Exception:
        continue
scene.view_settings.exposure = 0.20

# ================================================================= regimes de tempo
# Domain randomization de iluminacao. Nao e enfeite: Liao et al. 2026 (Remote Sensing 18(2):361)
# mede que TIRAR a variacao de sol, tempo e angulo custa cerca de 10 pontos de mAP50, e cerca de
# 20 em objeto truncado. Este e o eixo mais barato de randomizar e o de maior retorno medido.
#
# Cada regime e um orcamento de luz coerente, nao um ajuste solto de brilho. O que muda junto:
#   sol      energia do disco solar
#   disco    tamanho angular do sol em graus. 0,6 e o sol real (sombra dura). Acima de 20 a
#            sombra some, que e exatamente o que um ceu encoberto faz.
#   amb      preenchimento do ceu. Num dia encoberto o ceu INTEIRO vira a fonte, entao sobe muito.
#   nevoa    densidade do airlight. Nublado e neblina tem muito mais agua em suspensao.
#   dust     densidade de aerossol no ceu Nishita, que e o que tira o azul e branqueia o ceu.
CLIMAS = {
    "sol_duro":  dict(sol=5.0,  cor_sol=(1.00, 0.96, 0.90), disco=0.6,  amb=0.92,
                      cor_amb=(0.82, 0.87, 1.00), nevoa=0.9e-4, expo=0.20, elev=(46, 74),
                      ar=1.1, dust=2.2),
    "sol_baixo": dict(sol=3.6,  cor_sol=(1.00, 0.80, 0.56), disco=0.9,  amb=0.85,
                      cor_amb=(0.86, 0.86, 1.00), nevoa=2.8e-4, expo=0.40, elev=(9, 25),
                      ar=1.6, dust=8.0),
    "nublado":   dict(sol=0.55, cor_sol=(1.00, 0.99, 0.98), disco=24.0, amb=2.45,
                      cor_amb=(0.90, 0.93, 1.00), nevoa=2.6e-4, expo=-0.10, elev=(30, 70),
                      ar=1.9, dust=6.0),
    "encoberto": dict(sol=0.12, cor_sol=(1.00, 1.00, 1.00), disco=38.0, amb=1.70,
                      cor_amb=(0.86, 0.90, 1.00), nevoa=3.8e-4, expo=-0.55, elev=(28, 66),
                      ar=2.2, dust=9.5),
    "neblina":   dict(sol=2.0,  cor_sol=(1.00, 0.97, 0.93), disco=7.0,  amb=1.60,
                      cor_amb=(0.90, 0.94, 1.00), nevoa=9.0e-4, expo=0.05, elev=(22, 52),
                      ar=2.4, dust=10.0),
    "chuva":     dict(sol=0.22, cor_sol=(1.00, 1.00, 1.00), disco=32.0, amb=1.10,
                      cor_amb=(0.80, 0.87, 1.00), nevoa=5.2e-4, expo=-0.90, elev=(24, 60),
                      ar=2.3, dust=10.0),
}
EXPO_BASE_CLIMA = scene.view_settings.exposure


def aplica_clima(nome, rng_, elev=None, azim=None):
    """poe a cena inteira num regime de tempo. Devolve o que foi aplicado, para o manifesto."""
    c = CLIMAS[nome]
    el = elev if elev is not None else rng_.uniform(*c["elev"])
    az = azim if azim is not None else rng_.uniform(0, 360)
    sol_d.energy = c["sol"] * rng_.uniform(0.85, 1.15)
    sol_d.color = c["cor_sol"]
    sol_d.angle = math.radians(c["disco"])
    sol.rotation_euler = Euler((math.radians(90 - el), 0, math.radians(180 - az)), "XYZ")
    amb.inputs["Strength"].default_value = c["amb"] * rng_.uniform(0.9, 1.1)
    amb.inputs["Color"].default_value = (*c["cor_amb"], 1.0)
    _vs.inputs["Density"].default_value = c["nevoa"] * rng_.uniform(0.8, 1.25)
    scene.view_settings.exposure = c["expo"] + rng_.uniform(-0.12, 0.12)
    for a_, v_ in (("sun_elevation", math.radians(el)), ("sun_rotation", math.radians(az)),
                   ("air_density", c["ar"]), ("dust_density", c["dust"])):
        try:
            setattr(sky, a_, v_)
        except Exception:
            pass
    return dict(clima=nome, elev=round(el, 1), azim=round(az, 1),
                sol=round(sol_d.energy, 2), amb=round(amb.inputs["Strength"].default_value, 2),
                nevoa=round(_vs.inputs["Density"].default_value * 1e4, 2),
                expo=round(scene.view_settings.exposure, 2))

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
_gsd = larg / args.res[0]
# CUIDADO com o numero que se reporta aqui. "Pessoa de 1,7 m ocupa 17 px" e verdade para camera
# OBLIQUA e falso para nadir: em nadir a altura e justamente a dimensao que NAO se projeta. O
# que a camera ve de cima e a PLANTA da pessoa, cerca de 0,48 m de ombro a ombro. Reportar a
# altura aqui fazia o alvo parecer duas a tres vezes maior do que e.
print(f"[morro] nadir a {args.alt:.0f} m enquadra {larg:.0f} x {larg*args.res[1]/args.res[0]:.0f} m "
      f"({_gsd*100:.1f} cm/px)", flush=True)
print(f"[morro] alvo em NADIR: ombro a ombro 0,48 m = {0.48/_gsd:.1f} px; planta cabeca e ombro "
      f"0,62 m = {0.62/_gsd:.1f} px. (De pe, 1,70 m daria {1.70/_gsd:.0f} px, mas essa dimensao "
      f"so aparece em camera obliqua.)", flush=True)
print(f"[morro] o menor stride do YOLO e 8 px: alvo desse tamanho esta no limite da rede.",
      flush=True)

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
scene.cycles.volume_bounces = 1
if args.persistente:
    scene.render.use_persistent_data = True
    print("[morro] dado persistente LIGADO: a cena nao e ressincronizada por quadro",
          flush=True)

# Exposicao por vista: o beco esta cerca de 6 paradas abaixo da laje, e uma camera real
# compensaria isso. Sem o ajuste a vista sai preta mesmo com a luz correta.
EXPO = {"beco": 3.2, "obliqua": 0.3}
EXPO_BASE = scene.view_settings.exposure

if args.save_blend:
    os.makedirs(os.path.dirname(args.save_blend) or ".", exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=args.save_blend)
    print(f"[morro] cena salva em {args.save_blend}", flush=True)

# ================================================================= dataset YOLO
# Reaproveita o mapa de ocupacao ja calculado para a camera de beco: celula livre e beco ou
# laje de terreno (onde pessoa anda), e CASAS da a cota de cada laje (onde pessoa tambem anda,
# e onde a vista de drone mais a enxerga). Isso e melhor que o ray cast cego de gen_jacarezinho,
# porque aqui sabemos de antemao o que e chao e o que e cobertura.
CLIMAS_USO = ([k.strip() for k in args.climas.split(",") if k.strip() in CLIMAS]
              if args.climas != "todos" else list(CLIMAS))
if not CLIMAS_USO:
    CLIMAS_USO = ["sol_duro"]

# ---- modo comparacao: a MESMA cena e o MESMO enquadramento em cada regime de tempo, que e a
# unica forma de ver o efeito da luz isolado da geometria.
if args.comparar_climas:
    scene.camera = CAMS["nadir"]
    for _k in CLIMAS_USO:
        _i = aplica_clima(_k, rng, elev=58.0, azim=35.0)
        scene.render.filepath = os.path.join(args.out, f"clima_{_k}.png")
        print(f"[morro] clima {_k}: sol={_i['sol']} amb={_i['amb']} "
              f"nevoa={_i['nevoa']}e-4 expo={_i['expo']}", flush=True)
        bpy.ops.render.render(write_still=True)
    print("[morro] comparacao de climas gravada", flush=True)

if args.dataset > 0:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import people_mpfb as PM
    PM.PORTE_REALISTA = args.porte_realista

    for _sp in ("train", "val"):
        os.makedirs(os.path.join(args.out, "images", _sp), exist_ok=True)
        os.makedirs(os.path.join(args.out, "labels", _sp), exist_ok=True)

    LIVRES = np.argwhere(livre)
    print(f"[morro] {len(LIVRES)} celulas livres para pessoa no chao", flush=True)
    PM.build_pool(rng, args.pool, print)

    cam_ds = CAMS["nadir"]
    scene.camera = cam_ds
    scene.view_settings.exposure = EXPO_BASE
    mf = open(os.path.join(args.out, "manifest.jsonl"), "a", encoding="utf-8")
    tot_cx = 0
    tot_obj = 0

    for i in range(args.dataset):
        PM.clear_people()
        # Domain randomization: regime de tempo completo, nao so posicao do sol. Varrer os
        # regimes em ordem (e nao sortear) garante que um dataset pequeno fique balanceado,
        # o que importa porque o eixo de luz e o que mais pesa no sim-to-real.
        clima = CLIMAS_USO[i % len(CLIMAS_USO)]
        info_luz = aplica_clima(clima, rng)
        el, az = info_luz["elev"], info_luz["azim"]
        alt = args.alt + rng.uniform(-args.alt_jitter, args.alt_jitter)
        ccx = rng.uniform(-NUC_A * 0.45, NUC_A * 0.45)
        ccy = rng.uniform(-NUC_B * 0.45, NUC_B * 0.45)
        _pit = rng.uniform(args.pitch[0], args.pitch[1])
        _yaw = rng.uniform(0, math.tau)
        # A camera e posicionada e depois APONTADA para o alvo, em vez de receber uma rotacao
        # calculada a mao. A versao anterior montava o Euler e corrigia a posicao com um recuo
        # de sinal deduzido no papel; o sinal estava trocado, a camera andava para o mesmo lado
        # para onde passou a olhar, e o lote obliquo de 2026-09-21 saiu com 992 pessoas na cena e
        # ZERO caixas, depois de 2,6 h de render. `to_track_quat` nao depende de eu acertar a
        # convencao de eixo do Blender: dada a direcao, ela devolve a rotacao que olha para la.
        _alvo = Vector((ccx, ccy, z_em(ccx, ccy)))
        _d = alt * math.tan(math.radians(_pit))
        cam_ds.location = (ccx + _d * math.sin(_yaw), ccy - _d * math.cos(_yaw),
                           z_em(ccx, ccy) + alt)
        _dir = _alvo - Vector(cam_ds.location)
        cam_ds.rotation_euler = _dir.to_track_quat("-Z", "Y").to_euler()
        bpy.context.view_layer.update()

        n_p = rng.randint(args.people[0], args.people[1])
        idx = 0

        def _no_quadro(x, y, z, folga=0.04):
            """a pessoa entra no quadro? Perguntado por PROJECAO, nao por raio no plano.

            O filtro antigo era `abs(px - ccx) > meia`, com `meia` derivado da largura do quadro
            NADIR. Isso tem dois defeitos que so aparecem com a camera inclinada: a pegada no
            chao deixa de ser um quadrado centrado na camera e vira um trapezio deslocado, e
            `meia` encolhe junto com a altura, que no preset obliquo cai de 150 m para 60 m. O
            resultado combinado foi rejeitar quase toda candidata e ainda assim enquadrar errado
            as poucas aceitas. Projetar o ponto do chao custa o mesmo e vale para qualquer pitch."""
            q = world_to_camera_view(scene, cam_ds, Vector((x, y, z)))
            return q.z > 0 and -folga <= q.x <= 1 + folga and -folga <= q.y <= 1 + folga

        for _ in range(n_p * 12):
            if idx >= n_p:
                break
            # Tres classes balanceadas. A terceira (desarmada COM objeto alongado) e o negativo
            # dificil: e ela que permite medir com que frequencia um detector chama de arma uma
            # vassoura, que e o dano de uso dual que o artigo discute. Ver PLANO-ARMADO.md.
            cls_ = rng.choices([0, 1, 2], weights=args.mistura)[0]
            armed = (cls_ == 0)
            if rng.random() < 0.45 and CASAS:      # em cima da laje
                ca, _zb, zt = rng.choice(CASAS)
                mx_ = sum(p[0] for p in ca) / 4
                my_ = sum(p[1] for p in ca) / 4
                if not _no_quadro(mx_, my_, zt):
                    continue
                px = mx_ + rng.uniform(-0.3, 0.3)
                py = my_ + rng.uniform(-0.3, 0.3)
                PM.make_person(rng, idx, px, py, zt + 0.02, armed, on_roof=True, classe=cls_)
            else:                                  # no beco
                j_, i_ = LIVRES[rng.randrange(len(LIVRES))]
                px = BX0 + (i_ + 0.5) * GB
                py = BY0 + (j_ + 0.5) * GB
                if not _no_quadro(px, py, z_em(px, py)):
                    continue
                PM.make_person(rng, idx, px, py, z_em(px, py) + 0.02, armed, on_roof=False, classe=cls_)
            idx += 1

        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        split = "val" if rng.random() < args.val else "train"
        nome = f"mr_{i:06d}"
        rotulos = []
        for p in PM.PEOPLE:
            pts = PM.person_points(p, dg)
            bb = PM.bbox_2d(scene, cam_ds, pts, args.min_lado)
            if bb is None:
                continue
            vis = PM.visibility(scene, cam_ds, p, pts, dg)
            if vis < args.min_vis:
                continue
            x1, y1, x2, y2 = bb
            rotulos.append((p["cls"], (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1,
                            round(vis, 2), p["on_roof"], p.get("tipo_obj"), p.get("comp_obj", 0.0)))

        # RETOMADA. O quadro ja sorteado e descartado aqui, e nao antes: todo o consumo de
        # numero aleatorio do quadro ja aconteceu, entao a sequencia continua identica a de uma
        # execucao do zero. Pular o sorteio junto deslocaria o gerador e os quadros seguintes
        # sairiam diferentes dos que o lote interrompido teria produzido.
        if i < args.start:
            if i % 20 == 0:
                print(f"[morro] retomada: pulando {nome}", flush=True)
            continue

        scene.render.filepath = os.path.join(args.out, "images", split, nome + ".png")
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        with open(os.path.join(args.out, "labels", split, nome + ".txt"), "w") as f:
            for l in rotulos:
                f.write(f"{l[0]} {l[1]:.6f} {l[2]:.6f} {l[3]:.6f} {l[4]:.6f}\n")
        rec = dict(img=nome + ".png", split=split, w=args.res[0], h=args.res[1],
                   alt=round(alt, 1), pitch=round(_pit, 1),
                   n_pessoas=len(PM.PEOPLE), n_caixas=len(rotulos),
                   n_armadas=sum(1 for l in rotulos if l[0] == 0),
                   n_desarmadas=sum(1 for l in rotulos if l[0] == 1),
                   n_objeto=sum(1 for l in rotulos if l[0] == 2),
                   tipos=[l[7] for l in rotulos if l[7]],
                   comps=[l[8] for l in rotulos if l[8]],
                   n_laje=sum(1 for l in rotulos if l[6]),
                   vis=[l[5] for l in rotulos], seed=args.seed,
                   render_s=round(time.time() - t0, 1))
        rec.update(info_luz)
        mf.write(json.dumps(rec) + "\n")
        mf.flush()
        tot_cx += len(rotulos)
        tot_obj += sum(1 for l in rotulos if l[0] == 2)

        # Freio. Um lote sem caixa nenhuma e um lote inutil, e o custo de descobrir isso no fim
        # e alto: o braco obliquo de 2026-09-21 rendeu 180 imagens em 2,6 h com 992 pessoas na
        # cena e zero anotacoes, e so apareceu no treino, horas depois. Cinco quadros bastam
        # para saber se a camera esta olhando para onde as pessoas estao.
        if i == 4 and tot_cx == 0:
            raise SystemExit(
                "[morro] ABORTADO: 5 quadros renderizados e nenhuma caixa anotada. A camera "
                "provavelmente nao esta enquadrando as pessoas. Conferir pitch, posicao da "
                "camera e o filtro _no_quadro antes de gastar o lote inteiro.")
        print(f"[morro] {nome} {split} caixas={len(rotulos)}/{len(PM.PEOPLE)} "
              f"{clima} elev={el:.0f} alt={alt:.0f} {rec['render_s']}s", flush=True)
    mf.close()
    # As classes declaradas precisam bater com as que SAIRAM nos rotulos. Declarar duas quando o
    # lote tem tres faz o Ultralytics tratar a classe 2 como fora de faixa, e o erro so aparece
    # no treino, horas depois. Conta-se o que foi ESCRITO em vez de supor pela --mistura, porque
    # um peso zero ou um lote pequeno podem nao produzir nenhuma instancia da terceira classe.
    NOMES = ["pessoa_armada", "pessoa_desarmada", "pessoa_objeto"]
    n_cls = 3 if tot_obj > 0 else 2
    with open(os.path.join(args.out, "data.yaml"), "w") as f:
        cab = "path: " + os.path.abspath(args.out).replace(os.sep, "/") + "\n"
        cab += "train: images/train\nval: images/val\nnames:\n"
        for i in range(n_cls):
            cab += "  %d: %s\n" % (i, NOMES[i])
        f.write(cab)
    print(f"[morro] data.yaml com {n_cls} classes, {tot_obj} caixas de objeto alongado", flush=True)
    print(f"[morro] dataset: {args.dataset} imagens, {tot_cx} caixas", flush=True)

if args.dataset == 0 and not args.comparar_climas and not args.no_render:
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
