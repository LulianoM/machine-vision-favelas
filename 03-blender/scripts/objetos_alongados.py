#!/usr/bin/env python3
"""
objetos_alongados.py: armas e objetos CONFUNDIVEIS, construidos no mesmo eixo e na mesma escala.

Por que este modulo existe, e por que ele e o centro do experimento de uso dual.

Medido em 2026-09-20 pela otica do gerador: a 150 m em 4K (4,88 cm/px) um fuzil de 0,90 m ocupa
18,4 px de comprimento por 1,0 px de largura, e a pessoa em planta ocupa 9,8 px. Ou seja, o que
chega ao sensor nao e a forma da arma: e uma ESTRUTURA LINEAR FINA que quebra a silhueta.

A consequencia e que a tarefa nao e reconhecer uma arma. E decidir se uma linha escura de 18 px
saindo de um blob de 10 px e uma arma ou uma vassoura. E ate aqui o corpus nao tinha NADA alem de
armas que produzisse uma linha escura, o que torna a distincao trivialmente aprendivel pela razao
errada e deixa a taxa de falso positivo real inteiramente sem medida.

Numa favela as pessoas carregam vassoura, rodo, cano de PVC, vergalhao, tabua, guarda-chuva
fechado, enxada, mangueira enrolada, tapete. Um detector que nunca viu nenhum desses aprende
"linha escura igual a armada". Esse e exatamente o dano de uso dual de que o artigo trata, e
medi-lo e mais valioso que reportar acuracia.

Convencao geometrica, identica para arma e para objeto, para que nada alem da forma diferencie:
  eixo +X e o comprimento (cano para +X, cabo de vassoura para +X)
  origem no ponto de empunhadura
  +Z e para cima quando o objeto esta na horizontal

Todo comprimento esta em metros e foi escolhido na faixa real do objeto, nao por conveniencia.
"""
import math

import bpy

_MATS = {}


def _mat(nome, cor, rough=0.8, metal=0.0):
    if nome in _MATS and _MATS[nome].name in bpy.data.materials:
        return _MATS[nome]
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (cor[0], cor[1], cor[2], 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    _MATS[nome] = m
    return m


def mats():
    """Paleta compartilhada. Arma e objeto usam a MESMA faixa de cor e de rugosidade de proposito:
    se a arma fosse a unica coisa preta e metalica na cena, a rede separaria por cor e o
    experimento nao mediria nada."""
    return dict(
        metal=_mat("mat_metal", (0.030, 0.030, 0.035), 0.40, 0.70),
        metal_gasto=_mat("mat_metal_gasto", (0.075, 0.072, 0.068), 0.62, 0.55),
        madeira=_mat("mat_madeira", (0.320, 0.160, 0.070), 0.55),
        madeira_clara=_mat("mat_madeira_clara", (0.430, 0.300, 0.160), 0.62),
        polimero=_mat("mat_polimero", (0.060, 0.060, 0.060), 0.70),
        pvc=_mat("mat_pvc", (0.560, 0.560, 0.540), 0.55),
        pvc_cinza=_mat("mat_pvc_cinza", (0.230, 0.235, 0.245), 0.60),
        ferrugem=_mat("mat_ferrugem", (0.190, 0.085, 0.040), 0.85),
        pano_escuro=_mat("mat_pano_escuro", (0.050, 0.055, 0.075), 0.90),
        cerda=_mat("mat_cerda", (0.420, 0.330, 0.150), 0.90),
        plastico_cor=_mat("mat_plastico_cor", (0.140, 0.260, 0.420), 0.60),
    )


class Construtor:
    """acumulador minimo de caixas e cilindros, no eixo +X"""

    def __init__(self, nome):
        self.nome, self.v, self.f, self.fm, self.mats = nome, [], [], [], []

    def _mi(self, m):
        if m not in self.mats:
            self.mats.append(m)
        return self.mats.index(m)

    def box(self, cx, cy, cz, sx, sy, sz, mat, rot_y=0.0):
        c, s = math.cos(rot_y), math.sin(rot_y)
        b = len(self.v)
        for dz in (-0.5, 0.5):
            for (dx, dy) in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
                x, z = dx * sx, dz * sz
                self.v.append((cx + x * c + z * s, cy + dy * sy, cz - x * s + z * c))
        mi = self._mi(mat)
        for fa in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            self.f.append(tuple(b + i for i in fa))
            self.fm.append(mi)

    def cyl_x(self, x0, x1, cy, cz, r, mat, n=8):
        b = len(self.v)
        for x in (x0, x1):
            for k in range(n):
                a = k * 2 * math.pi / n
                self.v.append((x, cy + r * math.cos(a), cz + r * math.sin(a)))
        mi = self._mi(mat)
        for k in range(n):
            k2 = (k + 1) % n
            self.f.append((b + k, b + k2, b + n + k2, b + n + k))
            self.fm.append(mi)

    def build(self):
        me = bpy.data.meshes.new(self.nome)
        me.from_pydata(self.v, [], [list(f) for f in self.f])
        for m in self.mats:
            me.materials.append(m)
        me.polygons.foreach_set("material_index", self.fm)
        me.update()
        o = bpy.data.objects.new(self.nome, me)
        bpy.context.scene.collection.objects.link(o)
        return o


# ===================================================================== ARMAS
# Cinco modelos cobrindo a faixa real de comprimento. Antes existia essencialmente um, sempre na
# mesma pose e com o mesmo contraste, e era por isso que a distincao era aprendivel sem significar
# nada: a rede decorava o asset, nao o objeto.

def arma_fuzil_ak(nome, rng, M):
    """fuzil padrao AK, coronha e guarda-mao de madeira, carregador curvo. 0,88 m."""
    c = Construtor(nome)
    mad = M["madeira"] if rng.random() < 0.7 else M["madeira_clara"]
    met = M["metal"] if rng.random() < 0.6 else M["metal_gasto"]
    c.box(0.04, 0, 0.0, 0.34, 0.045, 0.075, met)
    c.cyl_x(0.21, 0.62, 0, 0.012, 0.011, met)
    c.box(0.30, 0, -0.005, 0.20, 0.05, 0.06, mad)
    c.box(-0.30, 0, -0.01, 0.30, 0.04, 0.06, mad, rot_y=0.05)
    c.box(-0.04, 0, -0.085, 0.045, 0.035, 0.11, mad, rot_y=-0.35)
    c.box(0.11, 0, -0.10, 0.06, 0.03, 0.17, met, rot_y=-0.5)
    return c.build(), 0.92


def arma_fuzil_ar(nome, rng, M):
    """padrao AR, preto, coronha retratil, carregador reto. 0,94 m."""
    c = Construtor(nome)
    pol = M["polimero"]
    met = M["metal"]
    c.box(0.02, 0, 0.0, 0.32, 0.045, 0.07, pol)
    c.cyl_x(0.18, 0.66, 0, 0.010, 0.010, met)
    c.box(0.32, 0, 0.0, 0.26, 0.05, 0.055, pol)
    c.box(-0.28, 0, 0.0, 0.26, 0.04, 0.05, pol)
    c.box(-0.03, 0, -0.085, 0.04, 0.035, 0.11, pol, rot_y=-0.3)
    c.box(0.10, 0, -0.10, 0.05, 0.03, 0.18, met, rot_y=-0.15)
    c.box(0.02, 0, 0.055, 0.14, 0.03, 0.03, met)
    return c.build(), 0.94


def arma_carabina(nome, rng, M):
    """carabina de coronha retratil recolhida. 0,62 m: a faixa em que a assinatura linear
    comeca a se confundir com a do proprio braco."""
    c = Construtor(nome)
    pol, met = M["polimero"], M["metal"]
    c.box(0.03, 0, 0.0, 0.26, 0.045, 0.07, pol)
    c.cyl_x(0.16, 0.36, 0, 0.010, 0.010, met)
    c.box(-0.18, 0, 0.0, 0.14, 0.035, 0.045, met)
    c.box(-0.02, 0, -0.08, 0.04, 0.035, 0.10, pol, rot_y=-0.3)
    c.box(0.06, 0, -0.10, 0.04, 0.03, 0.16, met)
    return c.build(), 0.62


def arma_espingarda(nome, rng, M):
    """espingarda de cano longo, coronha de madeira. 1,05 m, o extremo superior da faixa."""
    c = Construtor(nome)
    mad = M["madeira"] if rng.random() < 0.8 else M["madeira_clara"]
    met = M["metal_gasto"] if rng.random() < 0.5 else M["metal"]
    c.box(0.02, 0, 0.0, 0.22, 0.042, 0.065, met)
    c.cyl_x(0.12, 0.74, 0, 0.012, 0.0125, met)
    c.box(0.34, 0, -0.018, 0.22, 0.042, 0.04, mad)
    c.box(-0.26, 0, -0.015, 0.34, 0.042, 0.075, mad, rot_y=0.07)
    return c.build(), 1.05


def arma_pistola(nome, rng, M):
    """pistola. 0,20 m: abaixo do limiar em que a assinatura linear existe a 150 m, e esta aqui
    justamente para medir onde a capacidade deixa de existir."""
    c = Construtor(nome)
    met = M["metal"] if rng.random() < 0.6 else M["polimero"]
    c.box(0.06, 0, 0.0, 0.17, 0.030, 0.035, met)
    c.box(-0.02, 0, -0.05, 0.035, 0.028, 0.09, M["polimero"], rot_y=-0.3)
    return c.build(), 0.20


ARMAS = [
    ("fuzil_ak", arma_fuzil_ak, 26),
    ("fuzil_ar", arma_fuzil_ar, 24),
    ("carabina", arma_carabina, 20),
    ("espingarda", arma_espingarda, 18),
    ("pistola", arma_pistola, 12),
]


# ===================================================================== OBJETOS CONFUNDIVEIS
# Cada um produz, a 150 m em nadir, uma assinatura linear de comprimento comparavel ao de uma
# arma. Sao os NEGATIVOS DIFICEIS, e sao a parte do experimento que de fato mede risco.

def obj_vassoura(nome, rng, M):
    """cabo de 1,20 m com a cerda no extremo. Em nadir e uma linha com um bloco na ponta,
    que e exatamente a assinatura de um fuzil com carregador."""
    c = Construtor(nome)
    cabo = M["madeira_clara"] if rng.random() < 0.5 else M["pvc_cinza"]
    c.cyl_x(-0.10, 1.10, 0, 0.0, 0.011, cabo)
    c.box(1.14, 0, -0.02, 0.09, 0.26, 0.05, M["madeira"])
    c.box(1.14, 0, -0.07, 0.085, 0.25, 0.07, M["cerda"])
    return c.build(), 1.28


def obj_rodo(nome, rng, M):
    c = Construtor(nome)
    c.cyl_x(-0.10, 1.05, 0, 0.0, 0.011, M["madeira_clara"])
    c.box(1.10, 0, -0.02, 0.055, 0.34, 0.055, M["plastico_cor"])
    return c.build(), 1.22


def obj_cano_pvc(nome, rng, M):
    """cano de 1,5 a 2,5 m. Mais longo que qualquer arma, e e por isso que importa: se a rede
    usar so comprimento, erra aqui."""
    L = rng.uniform(1.5, 2.5)
    c = Construtor(nome)
    c.cyl_x(-0.12, L - 0.12, 0, 0.0, rng.uniform(0.015, 0.030), M["pvc"])
    return c.build(), L


def obj_vergalhao(nome, rng, M):
    """barra de aco de 1,0 a 2,0 m, escura e fina. E o negativo mais dificil de todos: a secao
    e menor que a de um cano de fuzil e o material e o mesmo."""
    L = rng.uniform(1.0, 2.0)
    c = Construtor(nome)
    c.cyl_x(-0.10, L - 0.10, 0, 0.0, rng.uniform(0.005, 0.010),
            M["ferrugem"] if rng.random() < 0.5 else M["metal_gasto"])
    return c.build(), L


def obj_tabua(nome, rng, M):
    L = rng.uniform(0.9, 2.0)
    c = Construtor(nome)
    c.box(L / 2 - 0.10, 0, 0.0, L, rng.uniform(0.09, 0.22), rng.uniform(0.02, 0.035),
          M["madeira_clara"] if rng.random() < 0.6 else M["madeira"])
    return c.build(), L


def obj_guarda_chuva(nome, rng, M):
    """fechado. 0,85 m, praticamente o comprimento de um fuzil, e escuro."""
    c = Construtor(nome)
    c.cyl_x(-0.10, 0.10, 0, 0.0, 0.013, M["madeira"])
    c.cyl_x(0.10, 0.72, 0, 0.0, 0.026, M["pano_escuro"])
    c.cyl_x(0.72, 0.78, 0, 0.0, 0.008, M["metal"])
    return c.build(), 0.88


def obj_enxada(nome, rng, M):
    c = Construtor(nome)
    c.cyl_x(-0.10, 1.05, 0, 0.0, 0.013, M["madeira"])
    c.box(1.12, 0, -0.06, 0.16, 0.17, 0.02, M["metal_gasto"], rot_y=0.5)
    return c.build(), 1.24


def obj_tapete(nome, rng, M):
    """tapete ou colchao enrolado. Linear, grosso, e uma classe de erro diferente: o detector
    pode acertar que ha algo alongado e errar completamente o que e."""
    L = rng.uniform(1.1, 1.8)
    c = Construtor(nome)
    c.cyl_x(-0.10, L - 0.10, 0, 0.0, rng.uniform(0.07, 0.13),
            M["plastico_cor"] if rng.random() < 0.4 else M["pano_escuro"])
    return c.build(), L


def obj_mangueira(nome, rng, M):
    c = Construtor(nome)
    c.cyl_x(-0.08, rng.uniform(0.7, 1.3), 0, 0.0, 0.012, M["plastico_cor"])
    return c.build(), 1.0


OBJETOS = [
    ("vassoura", obj_vassoura, 20),
    ("rodo", obj_rodo, 12),
    ("cano_pvc", obj_cano_pvc, 14),
    ("vergalhao", obj_vergalhao, 16),
    ("tabua", obj_tabua, 12),
    ("guarda_chuva", obj_guarda_chuva, 12),
    ("enxada", obj_enxada, 8),
    ("tapete", obj_tapete, 8),
    ("mangueira", obj_mangueira, 6),
]


# ===================================================================== ARMAS INEDITAS
# Nunca entram em corpus de treino. Existem so para o teste da secao 11.5 do artigo: um detector
# que separa armada de desarmada so por ter decorado os cinco modelos acima perde o recall nestes
# dois. Sao escolhidos para cair dentro da faixa de comprimento dos cinco (um longo e um curto),
# de modo que o teste mede o asset, nao o tamanho.

def arma_fuzil_fal(nome, rng, M):
    """fuzil padrao FAL, coronha fixa, alca de transporte, carregador reto. 1,10 m."""
    c = Construtor(nome)
    met = M["metal"] if rng.random() < 0.6 else M["metal_gasto"]
    cor = M["polimero"] if rng.random() < 0.6 else M["madeira"]
    c.box(0.02, 0, 0.0, 0.30, 0.05, 0.08, met)
    c.cyl_x(0.17, 0.62, 0, 0.012, 0.013, met)
    c.cyl_x(0.62, 0.70, 0, 0.012, 0.017, met)
    c.box(0.29, 0, -0.005, 0.22, 0.055, 0.06, cor)
    c.box(-0.27, 0, -0.012, 0.26, 0.04, 0.07, cor, rot_y=0.04)
    c.box(-0.05, 0, -0.085, 0.04, 0.034, 0.11, cor, rot_y=-0.3)
    c.box(0.08, 0, -0.105, 0.07, 0.03, 0.16, met, rot_y=-0.08)
    c.box(0.06, 0, 0.055, 0.12, 0.012, 0.02, met)
    return c.build(), 1.10


def arma_submetralhadora(nome, rng, M):
    """submetralhadora compacta, coronha de arame recolhida, carregador curvo. 0,55 m."""
    c = Construtor(nome)
    met = M["metal"]
    pol = M["polimero"]
    c.box(0.02, 0, 0.0, 0.28, 0.045, 0.07, pol if rng.random() < 0.5 else met)
    c.cyl_x(0.16, 0.26, 0, 0.010, 0.011, met)
    c.box(0.15, 0, -0.045, 0.10, 0.05, 0.04, pol)
    c.box(-0.21, 0, 0.0, 0.18, 0.03, 0.025, met)
    c.box(-0.03, 0, -0.08, 0.04, 0.032, 0.10, pol, rot_y=-0.25)
    c.box(0.07, 0, -0.12, 0.04, 0.028, 0.18, met, rot_y=-0.22)
    return c.build(), 0.55


ARMAS_INEDITAS = [
    ("fuzil_fal", arma_fuzil_fal, 50),
    ("submetralhadora", arma_submetralhadora, 50),
]

# "padrao": so os cinco modelos de treino. "mista_inedita": metade das armas sai dos cinco,
# metade dos dois ineditos, para comparar o recall dentro do MESMO corpus de teste (mesmas cenas,
# mesma luz), com o tipo de cada caixa gravado no manifest. gen_morro.py liga com --armas.
MODO_ARMAS = "padrao"

# Rodada 6, item 6 (2026-11-04): com COMPRIMENTO_ARMA = (lo, hi) cada objeto confundivel e, depois de
# construido, escalado SO no eixo X (o do comprimento, em torno da origem, que e a ponta segurada) ate
# medir um comprimento sorteado em [lo, hi], a faixa das cinco armas de treino (0,62 a 1,05 m, medida em
# 06-resultados/armas_malhas.md). Largura, altura e material nao mudam. Assim o detector nao pode usar o
# comprimento para separar objeto de arma; e como nenhum objeto passa de 1,15 m, tambem nao ha o
# reangulo dos objetos longos (people_mpfb.make_person), que era outro indicio. gen_morro.py liga com
# --objetos-comprimento-arma. O manifest grava o comprimento final em `comps`.
COMPRIMENTO_ARMA = None


def _escala_comprimento(o, alvo):
    xs = [v.co.x for v in o.data.vertices]
    atual = max(xs) - min(xs)
    if atual <= 0:
        return
    f = alvo / atual
    for v in o.data.vertices:
        v.co.x *= f
    o.data.update()


def _sorteia(rng, tabela):
    tot = sum(p for _, _, p in tabela)
    u = rng.uniform(0, tot)
    a = 0
    for nome, fn, p in tabela:
        a += p
        if u <= a:
            return nome, fn
    return tabela[-1][0], tabela[-1][1]


def faz_arma(nome_obj, rng):
    """devolve (objeto, tipo, comprimento_m)"""
    M = mats()
    tabela = ARMAS
    if MODO_ARMAS == "mista_inedita" and rng.random() < 0.5:
        tabela = ARMAS_INEDITAS
    tipo, fn = _sorteia(rng, tabela)
    o, L = fn(nome_obj, rng, M)
    return o, tipo, L


def faz_objeto(nome_obj, rng):
    """objeto confundivel: devolve (objeto, tipo, comprimento_m)"""
    M = mats()
    tipo, fn = _sorteia(rng, OBJETOS)
    o, L = fn(nome_obj, rng, M)
    if COMPRIMENTO_ARMA is not None:
        L = rng.uniform(*COMPRIMENTO_ARMA)
        _escala_comprimento(o, L)
    return o, tipo, L


# ===================================================================== PORTE
# Como o objeto se posiciona em relacao ao corpo. A assinatura em nadir muda por completo entre
# estes, e alguns nao produzem assinatura nenhuma, o que tambem e um resultado.
PORTES = {
    "peito":      dict(loc=(0.10, 0.27, 1.22), yaw=1.05, pitch=-0.25, peso_arma=26, peso_obj=6),
    "ombro_cima": dict(loc=(0.16, 0.08, 1.34), yaw=1.25, pitch=1.15, peso_arma=14, peso_obj=22),
    "ombro_baixo": dict(loc=(0.18, 0.06, 1.30), yaw=1.30, pitch=-1.05, peso_arma=10, peso_obj=14),
    "tiracolo":   dict(loc=(-0.05, -0.16, 1.25), yaw=2.20, pitch=0.90, peso_arma=18, peso_obj=4),
    "lado":       dict(loc=(0.24, 0.05, 0.95), yaw=1.35, pitch=-0.55, peso_arma=16, peso_obj=20),
    "uma_mao":    dict(loc=(0.26, 0.03, 0.88), yaw=1.10, pitch=-0.15, peso_arma=10, peso_obj=24),
    "arrastando": dict(loc=(0.28, 0.02, 0.42), yaw=1.20, pitch=-0.10, peso_arma=2, peso_obj=10),
    "pousado":    dict(loc=(0.42, 0.10, 0.06), yaw=0.60, pitch=0.00, peso_arma=4, peso_obj=0),
}


def sorteia_porte(rng, e_arma):
    k = "peso_arma" if e_arma else "peso_obj"
    itens = [(n, d) for n, d in PORTES.items() if d[k] > 0]
    tot = sum(d[k] for _, d in itens)
    u = rng.uniform(0, tot)
    a = 0
    for n, d in itens:
        a += d[k]
        if u <= a:
            return n, d
    return itens[-1]
