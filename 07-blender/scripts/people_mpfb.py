"""
people_mpfb.py (v2): pessoas realistas para os geradores (MPFB + assets CC0 do MakeHuman).

O que mudou na v2, calibrado para imagem aerea de favela:
  - fuzil com silhueta reconhecivel (receiver, cano, carregador curvo, coronha, empunhadura),
    preso ao rig e posicionado pela pose: empunhado na frente do peito, apoiado ao lado do corpo
    ou pendurado nas costas; pistola na mao como variante
  - poses: parado, andando, empunhando arma, sentado, agachado, bracos cruzados
  - variante sem camisa e de bermuda (pintada no corpo), comum no contexto real
  - grupos: pessoas proximas umas das outras, viradas umas para as outras
  - remove SUBSURF das pecas (a 100 m e custo puro)

API:
  build_pool(rng, k)                      cria k humanos vestidos e guarda fora da cena
  make_person(rng, idx, x, y, z, armed, on_roof=False, pose=None, arma=None)
  place_group(rng, idx0, cx, cy, n, solo_fn, armed_prob)   grupo em torno de um ponto
  person_points / bbox_2d / visibility   anotacao e oclusao
"""
import bpy, os, glob, math, colorsys
from mathutils import Vector, Euler, Matrix
from bpy_extras.object_utils import world_to_camera_view

try:
    import objetos_alongados as OA
except Exception:            # o modulo vive ao lado; se faltar, o gerador segue sem a 3a classe
    OA = None

# gen_morro.py liga isto com --porte-realista. Ver comentario em make_person.
PORTE_REALISTA = False

POOL = []
PEOPLE = []
POOL_Z = -500.0
_SUITS = None
_MATS = {}


def _suits():
    global _SUITS
    if _SUITS is None:
        d = os.path.join(bpy.utils.user_resource('EXTENSIONS'), '.user', 'user_default', 'mpfb', 'data', 'clothes')
        _SUITS = sorted(glob.glob(os.path.join(d, '*suit*', '*.mhclo')))
    return _SUITS


def _is_body(o):
    mods = [m.type for m in o.modifiers]
    return o.type == 'MESH' and 'ARMATURE' in mods and 'MASK' in mods


def _mat(nome, cor, rough=0.8, metal=0.0):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (cor[0], cor[1], cor[2], 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def build_pool(rng, k, log=print):
    global POOL
    clear_pool()
    # O MPFB sorteia o corpo com o `random` GLOBAL quando a propriedade de semente da cena esta
    # vazia (createrandomhuman.py: `seed = random.randint(...)`). Medido em 22/09: dois lotes com
    # a mesma semente e o mesmo sitio davam cena identica (439 edificacoes, 208.396 faces) e
    # quadros diferentes (elev 64 contra 61, 13 contra 11 caixas), porque a altura e a largura de
    # cada corpo entram na oclusao e na contagem, e dai tudo diverge. Semear o global aqui com um
    # valor derivado do rng do lote fecha isso sem consumir um sorteio a mais do rng.
    import random as _random
    _random.seed(0x5EED ^ (k * 2654435761 % (2 ** 31)) ^ (rng.getstate()[1][0] & 0xFFFF))
    suits = _suits()
    for i in range(k):
        before = set(bpy.data.objects)
        try:
            bpy.ops.mpfb.create_random_human()
        except Exception as e:
            log("mpfb falhou", e)
            break
        new = [o for o in bpy.data.objects if o not in before]
        rigs = [o for o in new if o.type == 'ARMATURE']
        bodies = [o for o in new if _is_body(o)]
        if not rigs or not bodies:
            for o in new:
                bpy.data.objects.remove(o, do_unlink=True)
            continue
        rig, body = rigs[0], bodies[0]
        if suits and not any('suit' in o.name for o in new):
            bpy.ops.object.select_all(action='DESELECT')
            body.select_set(True)
            bpy.context.view_layer.objects.active = body
            try:
                bpy.ops.mpfb.load_library_clothes(filepath=rng.choice(suits), object_type="Clothes", material_type="MAKESKIN")
            except Exception as e:
                log("roupa falhou", e)
            new = [o for o in bpy.data.objects if o not in before]
        masc = any('male_' in o.name and 'female' not in o.name for o in new)
        for o in list(new):
            if any(kw in o.name for kw in ('teeth', 'tongue', 'eyebrow', 'eyelashes', 'low-poly')):
                bpy.data.objects.remove(o, do_unlink=True)
                new.remove(o)
        kids = [o for o in new if o.type == 'MESH' and o.parent == rig]
        for o in kids:
            for md in [m for m in o.modifiers if m.type == 'SUBSURF']:
                o.modifiers.remove(md)
        rig.name = f"pool_rig_{i}"
        for j, o in enumerate(kids):
            tipo = 'body' if _is_body(o) else ('suit' if 'suit' in o.name else ('shoes' if 'shoe' in o.name else 'part'))
            o.name = f"pool_{i}_{j}_{tipo}"
            o.hide_render = True
        rig.hide_render = True
        rig.location = (i * 5.0, 0, POOL_Z)
        POOL.append(dict(rig=rig, kids=kids, masc=masc))
    log(f"pool MPFB: {len(POOL)} humanos vestidos ({sum(1 for h in POOL if h['masc'])} masc)")
    return len(POOL)


def clear_pool():
    global POOL
    for h in POOL:
        for o in h["kids"]:
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.objects.remove(h["rig"], do_unlink=True)
    POOL = []


def clear_people():
    for p in PEOPLE:
        for o in p["kids"] + [p["rig"]] + ([p["gun"]] if p["gun"] else []):
            try:
                bpy.data.objects.remove(o, do_unlink=True)
            except Exception:
                pass
    PEOPLE.clear()


# ----------------------------------------------------------------- materiais de roupa
def _vary_material(rng, obj):
    obj.data = obj.data.copy()
    for si, mat in enumerate(obj.data.materials):
        if mat is None or not mat.use_nodes:
            continue
        m2 = mat.copy()
        obj.data.materials[si] = m2
        nt = m2.node_tree
        bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if bsdf is None:
            continue
        link = next((l for l in nt.links if l.to_node == bsdf and l.to_socket.name == "Base Color"), None)
        hs = nt.nodes.new("ShaderNodeHueSaturation")
        hs.inputs["Hue"].default_value = rng.random()
        hs.inputs["Saturation"].default_value = rng.uniform(0.4, 1.4)
        hs.inputs["Value"].default_value = rng.uniform(0.5, 1.15)
        if link:
            src = link.from_socket
            nt.links.remove(link)
            nt.links.new(src, hs.inputs["Color"])
        else:
            hs.inputs["Color"].default_value = bsdf.inputs["Base Color"].default_value
        nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.85


def _shirtless_material(rng, body):
    """sem camisa, de bermuda: pinta a bermuda no corpo por faixa de altura, mantem a pele do MPFB"""
    body.data = body.data.copy()
    for si, mat in enumerate(body.data.materials):
        if mat is None or not mat.use_nodes:
            continue
        m2 = mat.copy()
        body.data.materials[si] = m2
        nt = m2.node_tree
        bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if bsdf is None:
            continue
        link = next((l for l in nt.links if l.to_node == bsdf and l.to_socket.name == "Base Color"), None)
        pele = link.from_socket if link else None
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs[0])
        # bermuda entre 0,42 e 0,58 da altura (objeto MPFB tem ~1,75 m de altura no espaco local)
        lo = nt.nodes.new("ShaderNodeMath"); lo.operation = 'GREATER_THAN'; lo.inputs[1].default_value = 0.42 * 1.75
        hi = nt.nodes.new("ShaderNodeMath"); hi.operation = 'LESS_THAN'; hi.inputs[1].default_value = 0.58 * 1.75
        an = nt.nodes.new("ShaderNodeMath"); an.operation = 'MULTIPLY'
        nt.links.new(sep.outputs["Z"], lo.inputs[0]); nt.links.new(sep.outputs["Z"], hi.inputs[0])
        nt.links.new(lo.outputs[0], an.inputs[0]); nt.links.new(hi.outputs[0], an.inputs[1])
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = 'RGBA'
        cor = rng.choice([(0.05, 0.08, 0.35), (0.04, 0.04, 0.04), (0.5, 0.5, 0.5), (0.25, 0.12, 0.05), (0.6, 0.08, 0.06), (0.8, 0.8, 0.78)])
        mx.inputs[7].default_value = (cor[0], cor[1], cor[2], 1)
        nt.links.new(an.outputs[0], mx.inputs["Factor"])
        if pele is not None:
            nt.links.remove(link)
            nt.links.new(pele, mx.inputs[6])
        else:
            mx.inputs[6].default_value = bsdf.inputs["Base Color"].default_value
        nt.links.new(mx.outputs[2], bsdf.inputs["Base Color"])


# ----------------------------------------------------------------- armas
class _MB:
    def __init__(self, nome):
        self.nome, self.v, self.f, self.fm, self.mats = nome, [], [], [], []

    def mi(self, mat):
        if mat not in self.mats:
            self.mats.append(mat)
        return self.mats.index(mat)

    def box(self, cx, cy, cz, sx, sy, sz, mat, rot_y=0.0):
        c, s = math.cos(rot_y), math.sin(rot_y)
        b = len(self.v)
        for dz in (-0.5, 0.5):
            for (dx, dy) in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
                x, z = dx * sx, dz * sz
                self.v.append((cx + x * c + z * s, cy + dy * sy, cz - x * s + z * c))
        mi = self.mi(mat)
        for fa in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            self.f.append(tuple(b + i for i in fa))
            self.fm.append(mi)

    def cyl_x(self, x0, x1, cy, cz, r, mat, n=8):
        b = len(self.v)
        for x in (x0, x1):
            for k in range(n):
                a = 2 * math.pi * k / n
                self.v.append((x, cy + r * math.cos(a), cz + r * math.sin(a)))
        mi = self.mi(mat)
        for k in range(n):
            k2 = (k + 1) % n
            self.f.append((b + k, b + k2, b + n + k2, b + n + k))
            self.fm.append(mi)
        self.f.append(tuple(b + n + k for k in range(n)))
        self.fm.append(mi)

    def build(self):
        me = bpy.data.meshes.new(self.nome)
        me.from_pydata(self.v, [], self.f)
        for m in self.mats:
            me.materials.append(m)
        me.polygons.foreach_set("material_index", self.fm)
        me.update()
        o = bpy.data.objects.new(self.nome, me)
        bpy.context.scene.collection.objects.link(o)
        return o


def _gun_mats():
    if "metal" not in _MATS or _MATS["metal"].name not in bpy.data.materials:
        _MATS["metal"] = _mat("arma_metal", (0.03, 0.03, 0.035), rough=0.4, metal=0.7)
        _MATS["madeira"] = _mat("arma_madeira", (0.32, 0.16, 0.07), rough=0.55)
        _MATS["polimero"] = _mat("arma_polimero", (0.06, 0.06, 0.06), rough=0.7)
    return _MATS


def make_rifle(nome, rng):
    """fuzil generico no eixo +X (cano para +X), origem na empunhadura. ~0,88 m."""
    M = _gun_mats()
    mb = _MB(nome)
    tipo = rng.random()
    if tipo < 0.55:   # padrao AK: coronha e guarda-mao de madeira, carregador curvo
        mb.box(0.04, 0, 0.0, 0.34, 0.045, 0.075, M["metal"])              # receiver
        mb.cyl_x(0.21, 0.62, 0, 0.012, 0.011, M["metal"])                 # cano
        mb.box(0.30, 0, -0.005, 0.20, 0.05, 0.06, M["madeira"])           # guarda-mao
        mb.box(-0.30, 0, -0.01, 0.30, 0.04, 0.06, M["madeira"], rot_y=0.05)  # coronha
        mb.box(-0.04, 0, -0.085, 0.045, 0.035, 0.11, M["madeira"], rot_y=-0.35)  # empunhadura
        mb.box(0.11, 0, -0.10, 0.06, 0.03, 0.17, M["metal"], rot_y=-0.5)  # carregador curvo
        mb.box(0.62, 0, 0.012, 0.06, 0.02, 0.02, M["metal"])
    elif tipo < 0.85:  # padrao AR: preto, coronha retratil, carregador reto
        mb.box(0.02, 0, 0.0, 0.32, 0.045, 0.07, M["polimero"])
        mb.cyl_x(0.18, 0.66, 0, 0.010, 0.010, M["metal"])
        mb.box(0.32, 0, 0.0, 0.26, 0.05, 0.055, M["polimero"])
        mb.box(-0.28, 0, 0.0, 0.26, 0.04, 0.05, M["polimero"])
        mb.box(-0.03, 0, -0.085, 0.04, 0.035, 0.11, M["polimero"], rot_y=-0.3)
        mb.box(0.10, 0, -0.10, 0.05, 0.03, 0.18, M["metal"], rot_y=-0.15)
        mb.box(0.02, 0, 0.055, 0.14, 0.03, 0.03, M["metal"])              # mira/trilho
    else:              # carabina curta / submetralhadora
        mb.box(0.03, 0, 0.0, 0.28, 0.045, 0.07, M["polimero"])
        mb.cyl_x(0.17, 0.40, 0, 0.010, 0.010, M["metal"])
        mb.box(-0.22, 0, 0.0, 0.18, 0.03, 0.04, M["metal"])
        mb.box(-0.02, 0, -0.08, 0.04, 0.035, 0.10, M["polimero"], rot_y=-0.3)
        mb.box(0.06, 0, -0.10, 0.04, 0.03, 0.16, M["metal"])
    return mb.build()


def make_pistol(nome, rng):
    M = _gun_mats()
    mb = _MB(nome)
    mb.box(0.06, 0, 0.0, 0.17, 0.03, 0.035, M["metal"])
    mb.box(-0.02, 0, -0.05, 0.035, 0.028, 0.09, M["polimero"], rot_y=-0.3)
    return mb.build()


# ----------------------------------------------------------------- pose
def _rot(rig, name, x=0, y=0, z=0):
    pb = rig.pose.bones.get(name)
    if pb:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = Euler((math.radians(x), math.radians(y), math.radians(z)), 'XYZ')


def pose_rig(rng, rig, pose):
    """poses: parado | andando | empunhando | lado | costas | sentado | agachado | bracos_cruzados"""
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    try:
        bpy.ops.object.mode_set(mode='POSE')
    except Exception:
        return
    for pb in rig.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
    j = lambda a, b: rng.uniform(a, b)
    if pose == "empunhando":
        # bracos para a frente segurando o fuzil no peito; direito na empunhadura, esquerdo no guarda-mao
        _rot(rig, 'upperarm01.R', j(55, 70), 0, j(-35, -20))
        _rot(rig, 'lowerarm01.R', j(70, 95), j(-20, 0), 0)
        _rot(rig, 'upperarm01.L', j(45, 60), 0, j(15, 30))
        _rot(rig, 'lowerarm01.L', j(55, 80), j(0, 20), 0)
        _rot(rig, 'spine02', j(4, 10), 0, j(-10, 10))
        _rot(rig, 'head', j(-5, 12), 0, j(-25, 25))
        if rng.random() < 0.5:
            k = j(12, 24)
            _rot(rig, 'upperleg01.L', k, 0, 0)
            _rot(rig, 'upperleg01.R', -k * 0.6, 0, 0)
            _rot(rig, 'lowerleg01.R', k * 0.5, 0, 0)
    elif pose == "lado":
        # fuzil apoiado ao lado do corpo, mao direita na empunhadura, braco esquerdo solto
        _rot(rig, 'upperarm01.R', j(10, 20), 0, j(-70, -55))
        _rot(rig, 'lowerarm01.R', j(35, 55), 0, 0)
        _rot(rig, 'upperarm01.L', j(-6, 6), 0, j(58, 75))
        _rot(rig, 'lowerarm01.L', j(0, 20), 0, 0)
    elif pose == "costas":
        _rot(rig, 'upperarm01.R', j(-6, 6), 0, j(-75, -60))
        _rot(rig, 'upperarm01.L', j(-6, 6), 0, j(60, 75))
        _rot(rig, 'lowerarm01.R', j(0, 25), 0, 0)
        _rot(rig, 'lowerarm01.L', j(0, 25), 0, 0)
    elif pose == "sentado":
        _rot(rig, 'upperleg01.L', j(80, 95), 0, j(-8, 8))
        _rot(rig, 'upperleg01.R', j(80, 95), 0, j(-8, 8))
        _rot(rig, 'lowerleg01.L', j(-100, -80), 0, 0)
        _rot(rig, 'lowerleg01.R', j(-100, -80), 0, 0)
        _rot(rig, 'upperarm01.R', j(10, 30), 0, j(-70, -55))
        _rot(rig, 'upperarm01.L', j(10, 30), 0, j(55, 70))
        _rot(rig, 'lowerarm01.R', j(50, 80), 0, 0)
        _rot(rig, 'lowerarm01.L', j(50, 80), 0, 0)
        _rot(rig, 'spine02', j(6, 14), 0, 0)
    elif pose == "agachado":
        _rot(rig, 'upperleg01.L', j(95, 115), 0, j(-15, -5))
        _rot(rig, 'upperleg01.R', j(95, 115), 0, j(5, 15))
        _rot(rig, 'lowerleg01.L', j(-130, -110), 0, 0)
        _rot(rig, 'lowerleg01.R', j(-130, -110), 0, 0)
        _rot(rig, 'upperarm01.R', j(30, 50), 0, j(-60, -45))
        _rot(rig, 'upperarm01.L', j(30, 50), 0, j(45, 60))
        _rot(rig, 'lowerarm01.R', j(60, 90), 0, 0)
        _rot(rig, 'lowerarm01.L', j(60, 90), 0, 0)
        _rot(rig, 'spine02', j(15, 25), 0, 0)
    elif pose == "bracos_cruzados":
        _rot(rig, 'upperarm01.R', j(35, 45), 0, j(-55, -45))
        _rot(rig, 'lowerarm01.R', j(95, 115), j(20, 35), 0)
        _rot(rig, 'upperarm01.L', j(35, 45), 0, j(45, 55))
        _rot(rig, 'lowerarm01.L', j(95, 115), j(-35, -20), 0)
    else:
        walking = pose == "andando"
        for s, sg in (('L', 1), ('R', -1)):
            _rot(rig, f'upperarm01.{s}', j(-8, 8) + (j(-18, 18) if walking else 0), 0, sg * -j(58, 78))
            _rot(rig, f'lowerarm01.{s}', j(0, 25), j(0, 10), 0)
            if walking:
                k = j(15, 30) * (1 if s == 'L' else -1)
                _rot(rig, f'upperleg01.{s}', k, 0, 0)
                _rot(rig, f'lowerleg01.{s}', -abs(k) * 0.6 if k < 0 else 0, 0, 0)
            else:
                _rot(rig, f'upperleg01.{s}', j(-4, 4), 0, j(-3, 3))
        _rot(rig, 'spine02', j(-5, 8), 0, j(-8, 8))
        _rot(rig, 'head', j(-10, 15), 0, j(-30, 30))
    bpy.ops.object.mode_set(mode='OBJECT')
    rig.select_set(False)


# posicao e orientacao da arma no espaco LOCAL do rig (x direita, y frente, z cima), por pose
_GUN_LOCAL = {
    "empunhando": dict(loc=(0.10, 0.27, 1.22), rot=(0.0, 0.0, 1.05), pitch=-0.25),   # atravessado no peito, cano para frente-esquerda e um pouco para baixo
    "lado":       dict(loc=(0.24, 0.05, 0.95), rot=(0.0, 0.0, 1.35), pitch=-0.55),   # ao lado da coxa direita, cano para baixo-frente
    "costas":     dict(loc=(-0.05, -0.16, 1.25), rot=(0.0, 0.0, 2.2), pitch=0.9),    # pendurado nas costas, diagonal
    "sentado":    dict(loc=(0.12, 0.22, 0.72), rot=(0.0, 0.0, 1.2), pitch=-0.1),
    "agachado":   dict(loc=(0.10, 0.28, 0.85), rot=(0.0, 0.0, 1.05), pitch=-0.2),
}


def make_person(rng, idx, x, y, z, armed, on_roof=False, pose=None, arma=None, classe=None):
    """classe: 0 armada, 1 desarmada, 2 desarmada COM OBJETO ALONGADO.

    A classe 2 e o negativo dificil, e e a razao de ser deste experimento. A 150 m em 4K um fuzil
    ocupa 18 px de comprimento por 1 px de largura, entao o que chega ao sensor e uma estrutura
    linear que quebra a silhueta, nao a forma da arma. Sem alguem carregando uma vassoura no
    corpus, a rede aprende que linha escura igual a armada, e a taxa de falso positivo real fica
    sem medida. Ver 07-blender/PLANO-ARMADO.md."""
    if classe is None:
        classe = 0 if armed else 1
    armed = (classe == 0)
    com_objeto = (classe == 2 and OA is not None)
    h = rng.choice(POOL)
    bpy.ops.object.select_all(action='DESELECT')
    h["rig"].select_set(True)
    for k in h["kids"]:
        k.select_set(True)
    bpy.context.view_layer.objects.active = h["rig"]
    bpy.ops.object.duplicate(linked=True)
    sel = list(bpy.context.selected_objects)
    rig = [o for o in sel if o.type == 'ARMATURE'][0]
    kids = [o for o in sel if o.type == 'MESH']
    rig.name = f"rig_{idx}"
    sem_camisa = h.get("masc", False) and rng.random() < 0.35   # so homens sem camisa, como no contexto real
    body = None
    for j, o in enumerate(kids):
        o.name = f"person_{idx}_{j}"
        o.hide_render = False
        src = next((k for k in h["kids"] if k.data == o.data), None)
        if src is not None and 'suit' in src.name:
            if sem_camisa:
                o.hide_render = True
                o.hide_viewport = True
            else:
                _vary_material(rng, o)
        if src is not None and 'body' in src.name:
            body = o
    if sem_camisa and body is not None:
        # o MPFB adiciona ao corpo uma mascara "Delete.<roupa>" que apaga a pele sob a roupa.
        # Sem a roupa, essa mascara deixaria so cabeca, maos e pes. Remove so a da roupa; a dos
        # sapatos e a "Hide helpers" ficam.
        for md in [m for m in body.modifiers if m.type == 'MASK' and 'suit' in m.name.lower()]:
            body.modifiers.remove(md)
        _shirtless_material(rng, body)
    rig.hide_render = False
    yaw = rng.uniform(0, 2 * math.pi)
    sc = rng.uniform(0.92, 1.08)
    if pose is None:
        if armed or com_objeto:
            # MESMA distribuicao de pose para arma e para objeto. Se quem carrega vassoura
            # estivesse sempre numa pose diferente de quem carrega fuzil, a rede separaria pela
            # pose e o experimento nao mediria a confusao entre os objetos, que e o ponto.
            # EXCECAO de 2026-09-22 (PORTE_REALISTA): 23% das vassouras do corpus a 75 m sairam
            # chamadas de arma, e a folha de recortes mostrou o motivo: cano de PVC "empunhado"
            # com as duas maos atravessado no peito, que e uma pose que ninguem faz com cano.
            # Com a flag, o objeto vai sobretudo ao lado, no ombro ou na mao caminhando, e a pose
            # de tiro fica rara. A sobreposicao continua existindo (8%), so que na frequencia
            # em que existe na rua, e nao em 42%.
            if com_objeto and PORTE_REALISTA:
                pose = rng.choices(["empunhando", "lado", "costas", "andando"],
                                   weights=[0.08, 0.34, 0.28, 0.30])[0]
            else:
                pose = rng.choices(["empunhando", "lado", "costas", "andando"],
                                   weights=[0.42, 0.26, 0.16, 0.16])[0]
        else:
            pose = rng.choices(["parado", "andando", "sentado", "bracos_cruzados"], weights=[0.36, 0.38, 0.14, 0.12])[0]
    zz = z
    if pose == "sentado":
        zz = z - 0.42 * sc
    rig.location = (x, y, zz)
    rig.rotation_euler = (0, 0, yaw)
    rig.scale = (sc, sc, sc)
    pose_rig(rng, rig, pose)
    gun = None
    tipo_obj, comp_obj = None, 0.0
    if armed or com_objeto:
        if com_objeto:
            gun, tipo_obj, comp_obj = OA.faz_objeto(f"obj_{idx}", rng)
        elif OA is not None:
            gun, tipo_obj, comp_obj = OA.faz_arma(f"gun_{idx}", rng)
            arma = "pistola" if tipo_obj == "pistola" else "fuzil"
        else:
            if arma is None:
                arma = "pistola" if rng.random() < 0.15 else "fuzil"
            gun = make_pistol(f"gun_{idx}", rng) if arma == "pistola" else make_rifle(f"gun_{idx}", rng)
            tipo_obj, comp_obj = arma, 0.9
        gun.parent = rig
        gun.matrix_parent_inverse = Matrix.Identity(4)
        # o rig do MPFB olha para -Y; direita do corpo = -X. A arma tem o cano em +X local.
        # A POSICAO vem do osso do punho direito (depois da pose); a ORIENTACAO e fixada por pose
        # no espaco do corpo, porque a orientacao do punho varia demais com o jitter da pose.
        bpy.context.view_layer.update()
        pb = rig.pose.bones.get('wrist.R')
        if pose == "costas":
            sp = rig.pose.bones.get('spine03')
            base = (sp.tail if sp else Vector((0, 0, 1.3))) + Vector((0.0, 0.16, 0.0))
            rz, ry = math.radians(-115 + rng.uniform(-8, 8)), math.radians(-45 + rng.uniform(-8, 8))
        else:
            base = (pb.tail if pb else Vector((-0.25, -0.1, 1.0)))
            if pose == "empunhando":
                rz, ry = math.radians(-62 + rng.uniform(-10, 10)), math.radians(14 + rng.uniform(-6, 6))    # atravessado, cano frente-esquerda, leve para baixo
            elif pose == "andando":
                rz, ry = math.radians(-58 + rng.uniform(-10, 10)), math.radians(40 + rng.uniform(-8, 8))    # cano para baixo-frente
            else:  # lado
                rz, ry = math.radians(-75 + rng.uniform(-10, 10)), math.radians(68 + rng.uniform(-8, 8))    # quase vertical, cano para baixo
            if arma == "pistola":
                ry = math.radians(8 + rng.uniform(-6, 6)) if pose == "empunhando" else math.radians(60)
        if comp_obj > 1.15:
            # objeto de mais de 1,15 m nao se carrega na horizontal: vai apoiado no ombro com a
            # ponta para cima, ou inclinado com a ponta perto do chao. Sem isso a vassoura sairia
            # boiando, e a rede separaria por isso e nao pela forma.
            ry = math.radians(rng.choice([-52, -38, 46, 62]) + rng.uniform(-9, 9))
        # a origem da arma e a empunhadura: recua um pouco para a mao envolver o cabo
        gun.location = base + Vector((0.0, 0.0, -0.03))
        gun.rotation_euler = Euler((0.0, ry, rz), 'XYZ')
        gun.scale = (1 / sc, 1 / sc, 1 / sc)
    p = dict(rig=rig, kids=[k for k in kids if not k.hide_render], gun=gun, cls=classe,
             x=x, y=y, z=z, on_roof=on_roof, pose=pose,
             tipo_obj=tipo_obj, comp_obj=round(comp_obj, 2))
    PEOPLE.append(p)
    return p


def place_group(rng, idx0, cx, cy, n, solo_fn, armed_prob=0.3, raio=1.6):
    """grupo de n pessoas em torno de (cx, cy), viradas para o centro; solo_fn(x, y) -> z ou None"""
    feitos = []
    tent = 0
    while len(feitos) < n and tent < n * 15:
        tent += 1
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.5, raio)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        z = solo_fn(x, y)
        if z is None or any(math.hypot(q["x"] - x, q["y"] - y) < 0.55 for q in feitos):
            continue
        p = make_person(rng, idx0 + len(feitos), x, y, z, rng.random() < armed_prob)
        p["rig"].rotation_euler = (0, 0, math.atan2(cy - y, cx - x) + rng.uniform(-0.6, 0.6))
        feitos.append(p)
    return feitos


# ----------------------------------------------------------------- anotacao
def person_points(p, depsgraph, max_pts=500):
    pts = []
    for o in p["kids"]:
        ev = o.evaluated_get(depsgraph)
        mw = ev.matrix_world
        vs = ev.data.vertices
        step = max(1, len(vs) // (max_pts // max(1, len(p["kids"]))))
        for i in range(0, len(vs), step):
            pts.append(mw @ vs[i].co)
    if p["gun"] is not None:
        mg = p["gun"].matrix_world
        for v in p["gun"].data.vertices:
            pts.append(mg @ v.co)
    return pts


def bbox_2d(scene, co, pts, min_lado):
    xs, ys = [], []
    for w in pts:
        q = world_to_camera_view(scene, co, w)
        if q.z <= 0:
            continue
        xs.append(q.x)
        ys.append(1.0 - q.y)
    if len(xs) < 4:
        return None
    x1, x2 = max(0.0, min(xs)), min(1.0, max(xs))
    y1, y2 = max(0.0, min(ys)), min(1.0, max(ys))
    if x2 - x1 < min_lado or y2 - y1 < min_lado or x2 <= 0 or x1 >= 1 or y2 <= 0 or y1 >= 1:
        return None
    return (x1, y1, x2, y2)


def visibility(scene, co, p, pts, depsgraph, n=14):
    origin = co.matrix_world.translation
    own = set(p["kids"]) | {p["rig"]}
    if p["gun"]:
        own.add(p["gun"])
    idxs = [int(i * (len(pts) - 1) / (n - 1)) for i in range(n)]
    ok = 0
    for i in idxs:
        q = pts[i]
        d = q - origin
        dist = d.length
        d.normalize()
        hit, loc, nrm, fi, hobj, mtx = scene.ray_cast(depsgraph, origin, d, distance=dist + 0.5)
        if not hit or hobj in own or (hobj and hobj.original in own) or (loc - q).length < 0.3:
            ok += 1
    return ok / len(idxs)
