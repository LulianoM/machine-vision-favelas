"""
build_map.py (2026-09-12)
Monta o MAPA NAVEGAVEL do Jacarezinho no Blender a partir das saidas do OpenDroneMap:
  - malha texturizada de cada setor (fotogrametria das fotos da PCERJ de 2022)
  - malha 2.5D do DSM com o ortomosaico por baixo, tapando buracos e bordas
  - setores alinhados no mesmo mundo pelo georreferenciamento UTM (origem = canto sudoeste comum)
  - sol calculado para a data e hora reais do voo (sombras batem com as ja gravadas na textura)
  - cameras prontas: nadir 150 m (camera real Z30), obliqua 100 m, nivel da rua, e um voo animado
  - viewport configurado para navegar (clip ate 5 km, sombreamento material, EEVEE)

Uso:
  blender -b --python build_map.py -- --sectors sudoeste nordeste --out C:\arma3-favela\odm\jacarezinho.blend
Opcoes uteis:
  --decimate 0.4     versao leve para navegar em maquina fraca
  --no-dsm           so a malha de fotogrametria
  --preview          renderiza 4 imagens de checagem
  --video 240        renderiza um voo de N quadros (mp4)
"""
import bpy, bmesh, sys, os, math, json, argparse, time, random
from mathutils import Vector, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ODM_ROOT = r"C:\arma3-favela\odm"
ASSETS = r"C:\arma3-favela\assets"

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--sectors", nargs="+", default=["sudoeste", "nordeste"])
ap.add_argument("--out", default=os.path.join(ODM_ROOT, "jacarezinho.blend"))
ap.add_argument("--decimate", type=float, default=0.0, help="0 = malha cheia; 0.4 = 40%% das faces")
ap.add_argument("--no-dsm", action="store_true")
ap.add_argument("--preview", action="store_true")
ap.add_argument("--video", type=int, default=0, help="quadros do voo animado (0 = nao renderiza)")
ap.add_argument("--video-res", type=int, nargs=2, default=[1280, 720])
ap.add_argument("--alt-voo", type=float, default=70.0)
ap.add_argument("--pessoas", type=int, default=0, help="povoa o mapa com N pessoas MPFB (ruas e lajes)")
ap.add_argument("--pool", type=int, default=8, help="humanos distintos no acervo")
ap.add_argument("--prob-armado", type=float, default=0.35)
ap.add_argument("--seed", type=int, default=7)
args = ap.parse_args(argv)
T0 = time.time()


def log(*a):
    print(f"[mapa {time.time() - T0:6.1f}s]", *a, flush=True)


# ----------------------------------------------------------------- posicao do sol (NOAA)
def sun_position(y, mo, d, h_utc, lat, lon):
    """devolve (elevacao_graus, azimute_graus_da_bussola)"""
    a = (14 - mo) // 12
    ye = y + 4800 - a
    m = mo + 12 * a - 3
    jdn = d + (153 * m + 2) // 5 + 365 * ye + ye // 4 - ye // 100 + ye // 400 - 32045
    jd = jdn + (h_utc - 12) / 24.0
    n = jd - 2451545.0
    g = math.radians((357.529 + 0.98560028 * n) % 360)
    q = (280.459 + 0.98564736 * n) % 360
    L = math.radians((q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360)
    e = math.radians(23.439 - 0.00000036 * n)
    ra = math.atan2(math.cos(e) * math.sin(L), math.cos(L))
    dec = math.asin(math.sin(e) * math.sin(L))
    gmst = (18.697374558 + 24.06570982441908 * n) % 24
    lst = (gmst + lon / 15.0) % 24
    ha = math.radians((lst * 15 - math.degrees(ra) + 540) % 360 - 180)
    la = math.radians(lat)
    elev = math.asin(math.sin(la) * math.sin(dec) + math.cos(la) * math.cos(dec) * math.cos(ha))
    az = math.atan2(-math.sin(ha), math.tan(dec) * math.cos(la) - math.sin(la) * math.cos(ha))
    return math.degrees(elev), math.degrees(az) % 360


# ----------------------------------------------------------------- setores
def sector_offset(sector):
    p = os.path.join(ODM_ROOT, sector, "odm_georeferencing", "coords.txt")
    ox, oy = [float(v) for v in open(p).read().split("\n")[1].split()[:2]]
    return ox, oy


def latlon_center(sector):
    """centro aproximado do setor em lat/lon, a partir do ortomosaico"""
    j = os.path.join(ODM_ROOT, sector, "ortho_tex.json")
    ox, oy = sector_offset(sector)
    if os.path.exists(j):
        d = json.load(open(j))
        e = ox + (d["left"] + d["right"]) / 2
        nn = oy + (d["bottom"] + d["top"]) / 2
    else:
        e, nn = ox, oy
    # UTM 23S -> lat/lon (aproximacao suficiente para o sol)
    k0, a, f = 0.9996, 6378137.0, 1 / 298.257223563
    e2 = f * (2 - f)
    x = (e - 500000) / k0
    y = (nn - 10000000) / k0
    mu = y / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu) + (21 * e1 ** 2 / 16) * math.sin(4 * mu))
    lat = math.degrees(phi)
    lon = -45 + math.degrees(x / (a * math.cos(phi))) if abs(math.cos(phi)) > 1e-9 else -45
    return lat, lon


AVAIL = []
for s in args.sectors:
    obj = os.path.join(ODM_ROOT, s, "odm_texturing", "odm_textured_model_geo.obj")
    if os.path.exists(obj):
        AVAIL.append(s)
    else:
        log(f"setor {s} sem malha ainda, pulando")
if not AVAIL:
    raise SystemExit("nenhum setor pronto")
offs = {s: sector_offset(s) for s in AVAIL}
ORIGIN = (min(o[0] for o in offs.values()), min(o[1] for o in offs.values()))
log(f"setores: {AVAIL}  origem UTM: {ORIGIN}")

# ----------------------------------------------------------------- cena limpa
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
scene = bpy.context.scene
root = scene.collection


def new_col(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or root).children.link(c)
    return c


COL_MAPA = new_col("MAPA_FOTOGRAMETRIA")
COL_DSM = new_col("TERRENO_ORTOMOSAICO")
COL_LC = new_col("LUZ_E_CAMERAS")


def move_to(o, col):
    for c in list(o.users_collection):
        c.objects.unlink(o)
    col.objects.link(o)


# ----------------------------------------------------------------- carrega malhas
BOUNDS = dict(x0=1e9, x1=-1e9, y0=1e9, y1=-1e9, z0=1e9, z1=-1e9)


def grow_bounds(o):
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        BOUNDS["x0"] = min(BOUNDS["x0"], w.x)
        BOUNDS["x1"] = max(BOUNDS["x1"], w.x)
        BOUNDS["y0"] = min(BOUNDS["y0"], w.y)
        BOUNDS["y1"] = max(BOUNDS["y1"], w.y)
        BOUNDS["z0"] = min(BOUNDS["z0"], w.z)
        BOUNDS["z1"] = max(BOUNDS["z1"], w.z)


def fix_materials(o):
    for mat in o.data.materials:
        if not mat or not mat.use_nodes:
            continue
        b = mat.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Roughness"].default_value = 0.95
            for k in ("Specular IOR Level", "Specular"):
                if k in b.inputs:
                    b.inputs[k].default_value = 0.08
                    break


ZSHIFT = 0.0
for s in AVAIL:
    t = time.time()
    obj_path = os.path.join(ODM_ROOT, s, "odm_texturing", "odm_textured_model_geo.obj")
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=obj_path, forward_axis='Y', up_axis='Z')
    new = [o for o in bpy.data.objects if o not in before and o.type == 'MESH']
    if len(new) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for o in new:
            o.select_set(True)
        bpy.context.view_layer.objects.active = new[0]
        bpy.ops.object.join()
        new = [bpy.context.active_object]
    m = new[0]
    m.name = f"odm_{s}"
    dx = offs[s][0] - ORIGIN[0]
    dy = offs[s][1] - ORIGIN[1]
    m.location = (dx, dy, 0)
    bpy.context.view_layer.update()   # sem isso matrix_world fica velha e o bound_box sai no lugar errado
    pols = m.data.polygons
    pols.foreach_set("use_smooth", [True] * len(pols))
    m.data.update()
    fix_materials(m)
    if args.decimate > 0:
        md = m.modifiers.new("dec", 'DECIMATE')
        md.ratio = args.decimate
    move_to(m, COL_MAPA)
    grow_bounds(m)
    log(f"{m.name}: {len(m.data.vertices)} verts, {len(pols)} faces, offset ({dx:.0f}, {dy:.0f}) em {time.time()-t:.0f}s")

    if not args.no_dsm:
        blend = os.path.join(ODM_ROOT, s, "dsm_mesh.blend")
        if os.path.exists(blend):
            with bpy.data.libraries.load(blend, link=False) as (src, dst):
                dst.objects = [n for n in src.objects if n == "dsm_mesh"]
            d = dst.objects[0]
            d.name = f"dsm_{s}"
            root.objects.link(d)
            d.location = (dx, dy, -0.25)
            bpy.context.view_layer.update()
            move_to(d, COL_DSM)
            grow_bounds(d)
            log(f"{d.name}: {len(d.data.vertices)} verts")
        else:
            log(f"{s}: sem dsm_mesh.blend (rode export_dsm.py + build_dsm_mesh.py)")

CX = (BOUNDS["x0"] + BOUNDS["x1"]) / 2
CY = (BOUNDS["y0"] + BOUNDS["y1"]) / 2
EXT_X = BOUNDS["x1"] - BOUNDS["x0"]
EXT_Y = BOUNDS["y1"] - BOUNDS["y0"]
log(f"mapa: {EXT_X:.0f} x {EXT_Y:.0f} m, z {BOUNDS['z0']:.1f}..{BOUNDS['z1']:.1f}")

bpy.context.view_layer.update()
depsgraph = bpy.context.evaluated_depsgraph_get()


def ground_z(x, y, default=None):
    hit, loc, nrm, fi, o, mtx = scene.ray_cast(depsgraph, Vector((x, y, BOUNDS["z1"] + 200)), Vector((0, 0, -1)), distance=1000)
    return loc.z if hit else (default if default is not None else BOUNDS["z0"])


def amostra_alturas(n=40):
    """varre o mapa com raios verticais e devolve as alturas atingidas, em ordem"""
    zs = []
    for i in range(n):
        for j in range(n):
            x = BOUNDS["x0"] + (BOUNDS["x1"] - BOUNDS["x0"]) * (i + 0.5) / n
            y = BOUNDS["y0"] + (BOUNDS["y1"] - BOUNDS["y0"]) * (j + 0.5) / n
            hit, loc, nrm, fi, o, mtx = scene.ray_cast(depsgraph, Vector((x, y, BOUNDS["z1"] + 200)), Vector((0, 0, -1)), distance=1000)
            if hit:
                zs.append(loc.z)
    zs.sort()
    return zs


_zs = amostra_alturas()
GZ = _zs[len(_zs) // 2] if _zs else BOUNDS["z0"]
Z_BAIXO = _zs[max(0, int(len(_zs) * 0.03))] if _zs else BOUNDS["z0"]
log(f"centro ({CX:.0f}, {CY:.0f}): {len(_zs)} amostras, cota mediana {GZ:.1f}, cota baixa {Z_BAIXO:.1f}")

# ----------------------------------------------------------------- moldura do entorno
# O levantamento cobre so o poligono voado. Sem isso o mapa fica uma ilha flutuante no vazio.
# Um plano grande na altura mediana do terreno fecha o horizonte sem inventar edificacao.
def add_moldura():
    ph_path = os.path.join(ASSETS, "polyhaven", "index.json")
    size = max(EXT_X, EXT_Y) * 6
    bpy.ops.mesh.primitive_plane_add(size=size, location=(CX, CY, Z_BAIXO - 1.0))
    p = bpy.context.active_object
    p.name = "moldura_entorno"
    m = bpy.data.materials.new("m_moldura")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.95
    b.inputs["Base Color"].default_value = (0.19, 0.18, 0.17, 1)
    if os.path.exists(ph_path):
        ph = json.load(open(ph_path))
        cand = [n for n, e in ph["textures"].items() if e.get("cat") == "ground" and "diff" in e]
        if cand:
            e = ph["textures"][sorted(cand)[0]]
            nt_ = m.node_tree
            tc = nt_.nodes.new("ShaderNodeTexCoord")
            mp = nt_.nodes.new("ShaderNodeMapping")
            mp.inputs["Scale"].default_value = (0.12, 0.12, 0.12)
            img = nt_.nodes.new("ShaderNodeTexImage")
            img.image = bpy.data.images.load(os.path.join(ASSETS, "polyhaven", e["diff"]), check_existing=True)
            img.projection = 'BOX'
            dk = nt_.nodes.new("ShaderNodeMix")
            dk.data_type = 'RGBA'
            dk.blend_type = 'MULTIPLY'
            dk.inputs["Factor"].default_value = 1.0
            dk.inputs[7].default_value = (0.55, 0.54, 0.52, 1)
            nt_.links.new(tc.outputs["Object"], mp.inputs["Vector"])
            nt_.links.new(mp.outputs["Vector"], img.inputs["Vector"])
            nt_.links.new(img.outputs["Color"], dk.inputs[6])
            nt_.links.new(dk.outputs[2], b.inputs["Base Color"])
    p.data.materials.append(m)
    move_to(p, COL_DSM)
    return p


add_moldura()

# ----------------------------------------------------------------- sol real do voo
# Sudoeste 02/08/2022 11:55 local; Nordeste 01/08/2022 11:58 local (UTC-3)
lat, lon = latlon_center(AVAIL[0])
elev, az = sun_position(2022, 8, 2, 14 + 55 / 60, lat, lon)
log(f"voo em {lat:.4f}, {lon:.4f}: sol elevacao {elev:.1f} graus, azimute {az:.1f} graus")

w = bpy.data.worlds.new("Ceu")
scene.world = w
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
# A textura da fotogrametria ja traz o sol e as sombras do voo gravados no pixel.
# Somar um sol forte escureceria tudo duas vezes, entao a luz aqui e quase toda ambiente:
# ceu claro e pouco azulado como preenchimento, sol fraco so para dar relevo e sombrear
# o que for acrescentado na cena (pessoas, objetos).
for attr, val in (("sun_elevation", math.radians(elev)), ("sun_rotation", math.radians(az)),
                  ("altitude", 30), ("air_density", 0.6), ("dust_density", 1.0),
                  ("sun_intensity", 0.0), ("sun_size", math.radians(0.545))):
    try:
        setattr(sky, attr, val)
    except Exception:
        pass
nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0
# A camera ve o ceu azul; a ILUMINACAO vem de um ambiente neutro levemente quente.
# Sem isso o ceu fisico tinge a favela inteira de azul, o que nao existe na foto original.
bg_amb = nt.nodes.new("ShaderNodeBackground")
bg_amb.inputs["Color"].default_value = (1.0, 0.96, 0.90, 1.0)
bg_amb.inputs["Strength"].default_value = 0.95
lp = nt.nodes.new("ShaderNodeLightPath")
mix = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
nt.links.new(bg_amb.outputs["Background"], mix.inputs[1])
nt.links.new(bg.outputs["Background"], mix.inputs[2])
out = next(n for n in nt.nodes if n.type == 'OUTPUT_WORLD')
nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])

sun_d = bpy.data.lights.new("Sol", type='SUN')
sun_d.energy = 1.0
sun_d.angle = math.radians(2.0)
sun_o = bpy.data.objects.new("Sol", sun_d)
root.objects.link(sun_o)
sun_o.rotation_euler = Euler((math.radians(90 - elev), 0, math.radians(180 - az)), 'XYZ')
sun_o.location = (CX, CY, BOUNDS["z1"] + 100)
move_to(sun_o, COL_LC)

scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Medium Contrast'
except Exception:
    pass
scene.view_settings.exposure = 0.15

# ----------------------------------------------------------------- cameras
def add_cam(name, lens, loc, look_at, clip_end=4000):
    c = bpy.data.cameras.new(name)
    c.lens = lens
    c.sensor_width = 36
    c.clip_start = 0.1
    c.clip_end = clip_end
    o = bpy.data.objects.new(name, c)
    root.objects.link(o)
    o.location = loc
    d = Vector(look_at) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    move_to(o, COL_LC)
    return o


cam_nadir = add_cam("CAM_NADIR_150m_Z30", 4.3 * 36 / 5.37, (CX, CY, GZ + 150), (CX, CY, GZ))
cam_obl = add_cam("CAM_OBLIQUA_100m", 24, (CX - 60, CY - 60, GZ + 100), (CX, CY, GZ))
# 45 m olhando bem para baixo e a menor altura em que a fotogrametria ainda segura.
# Ao nivel da rua nao ha dado: o voo foi todo em nadir a 150 m, entao nao existe fachada.
bx, by = CX + EXT_X * 0.12, CY - EXT_Y * 0.12
cam_baixa = add_cam("CAM_BAIXA_45m", 24, (bx, by, ground_z(bx, by) + 45), (bx + 28, by + 28, ground_z(bx + 28, by + 28)))
cam_topo = add_cam("CAM_TOPO_MAPA", 24, (CX, CY, GZ + max(EXT_X, EXT_Y) * 1.15), (CX, CY, GZ))
scene.camera = cam_obl

# ----------------------------------------------------------------- voo animado
N = args.video if args.video > 0 else 240
cu = bpy.data.curves.new("rota_voo", 'CURVE')
cu.dimensions = '3D'
sp = cu.splines.new('NURBS')
K = 12
R = min(EXT_X, EXT_Y) * 0.30
sp.points.add(K - 1)
import random as _r
rr = _r.Random(7)
def sobre_fotogrametria(x, y):
    """true se o raio vertical atinge a malha de fotogrametria (nao o preenchimento nem a moldura)"""
    hit, loc, nrm, fi, o, mtx = scene.ray_cast(depsgraph, Vector((x, y, BOUNDS["z1"] + 200)), Vector((0, 0, -1)), distance=1000)
    return (hit and o is not None and o.original.name.startswith("odm_"), loc.z if hit else None)


for i in range(K):
    a = 2 * math.pi * i / K
    rad = R * rr.uniform(0.75, 1.15)
    # os dois setores ficam na diagonal, entao a caixa envolvente tem cantos vazios.
    # puxa o ponto para o centro ate cair sobre area levantada, senao o voo passa pelo vazio.
    x = y = None
    for _ in range(8):
        px = CX + math.cos(a) * rad
        py = CY + math.sin(a) * rad * 0.9
        ok, zz = sobre_fotogrametria(px, py)
        if ok:
            x, y = px, py
            break
        rad *= 0.82
    if x is None:
        x, y = CX + math.cos(a) * R * 0.25, CY + math.sin(a) * R * 0.25
    z = ground_z(x, y, GZ) + args.alt_voo + rr.uniform(-8, 8)
    sp.points[i].co = (x, y, z, 1)
sp.use_cyclic_u = True
sp.order_u = 4
cu.use_path = True
cu.path_duration = N
path = bpy.data.objects.new("ROTA_VOO", cu)
root.objects.link(path)
move_to(path, COL_LC)

cam_voo_d = bpy.data.cameras.new("CAM_VOO")
cam_voo_d.lens = 24
cam_voo_d.sensor_width = 36
cam_voo_d.clip_start = 0.1
cam_voo_d.clip_end = 4000
cam_voo = bpy.data.objects.new("CAM_VOO", cam_voo_d)
root.objects.link(cam_voo)
move_to(cam_voo, COL_LC)
alvo_path = bpy.data.objects.new("ALVO_VOO", None)
alvo_path.empty_display_size = 5
root.objects.link(alvo_path)
move_to(alvo_path, COL_LC)
alvo = bpy.data.objects.new("ALVO_OLHAR", None)
alvo.empty_display_size = 3
root.objects.link(alvo)
move_to(alvo, COL_LC)
alvo.parent = alvo_path
alvo.location = (0, 0, -args.alt_voo * 0.85)

for o, off in ((cam_voo, 0.0), (alvo_path, -N * 0.10)):
    c = o.constraints.new('FOLLOW_PATH')
    c.target = path
    c.use_curve_follow = False
    c.offset = off
t = cam_voo.constraints.new('TRACK_TO')
t.target = alvo
t.track_axis = 'TRACK_NEGATIVE_Z'
t.up_axis = 'UP_Y'

cu.eval_time = 0
cu.keyframe_insert("eval_time", frame=1)
cu.eval_time = N
cu.keyframe_insert("eval_time", frame=N)
def action_fcurves(act):
    """Blender 4.4+ moveu as fcurves para layers/strips/channelbags"""
    if act is None:
        return []
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])):
        return list(act.fcurves)
    out = []
    for layer in getattr(act, "layers", []):
        for strip in getattr(layer, "strips", []):
            for cb in getattr(strip, "channelbags", []):
                out += list(getattr(cb, "fcurves", []))
    return out


if cu.animation_data:
    for fc in action_fcurves(cu.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'
scene.frame_start = 1
scene.frame_end = N
scene.render.fps = 24

# ----------------------------------------------------------------- render / viewport
scene.render.engine = 'BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples = 32
    scene.eevee.use_shadows = True
    scene.eevee.use_raytracing = True
except Exception:
    pass
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
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
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 3

# ----------------------------------------------------------------- pessoas (opcional)
if args.pessoas > 0:
    import people_mpfb as PM
    COL_PESSOAS = new_col("PESSOAS")
    rng = random.Random(args.seed)
    PM.build_pool(rng, args.pool, log)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    posto = tentativas = 0
    while posto < args.pessoas and tentativas < args.pessoas * 40:
        tentativas += 1
        x = rng.uniform(BOUNDS["x0"] + 40, BOUNDS["x1"] - 40)
        y = rng.uniform(BOUNDS["y0"] + 40, BOUNDS["y1"] - 40)
        hit, loc, nrm, fi, o, mtx = scene.ray_cast(dg, Vector((x, y, BOUNDS["z1"] + 200)), Vector((0, 0, -1)), distance=1000)
        if not hit or nrm.z < 0.85:          # so superficie quase horizontal: rua, patio, laje
            continue
        nome = o.original.name
        if nome.startswith("dsm_") or nome == "moldura_entorno":
            continue   # so sobre a malha de fotogrametria, nunca no preenchimento nem na moldura
        p = PM.make_person(rng, posto, x, y, loc.z - 0.02, rng.random() < args.prob_armado)
        for ob in p["kids"] + [p["rig"]] + ([p["gun"]] if p["gun"] else []):
            move_to(ob, COL_PESSOAS)
        posto += 1
    log(f"pessoas: {posto} colocadas em {tentativas} tentativas")
    # o acervo de humanos fica guardado fora do caminho e escondido
    COL_POOL = new_col("_acervo_humanos")
    for h in PM.POOL:
        for ob in h["kids"] + [h["rig"]]:
            move_to(ob, COL_POOL)
    COL_POOL.hide_viewport = True
    COL_POOL.hide_render = True

# viewport pronto para navegar (persiste no .blend)
for sc_ in bpy.data.screens:
    for area in sc_.areas:
        if area.type == 'VIEW_3D':
            sp3 = area.spaces.active
            sp3.clip_start = 0.1
            sp3.clip_end = 5000
            sp3.lens = 28
            sp3.shading.type = 'MATERIAL'
            sp3.overlay.show_overlays = True
            try:
                sp3.region_3d.view_location = Vector((CX, CY, GZ))
                sp3.region_3d.view_distance = max(EXT_X, EXT_Y) * 0.8
            except Exception:
                pass

bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.out))
log(f"salvo {args.out}  ({os.path.getsize(args.out)/1e6:.0f} MB)")

# ----------------------------------------------------------------- previews
if args.preview:
    outdir = os.path.join(os.path.dirname(os.path.abspath(args.out)), "preview_mapa")
    os.makedirs(outdir, exist_ok=True)
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    for cam in (cam_topo, cam_nadir, cam_obl, cam_baixa):
        scene.camera = cam
        scene.render.filepath = os.path.join(outdir, cam.name + ".png")
        bpy.ops.render.render(write_still=True)
        log("preview", cam.name)
    scene.camera = cam_voo
    for fr in (1, N // 3, 2 * N // 3):
        scene.frame_set(fr)
        scene.render.filepath = os.path.join(outdir, f"CAM_VOO_f{fr:03d}.png")
        bpy.ops.render.render(write_still=True)
        log("preview voo", fr)
    scene.camera = cam_obl

if args.video > 0:
    scene.camera = cam_voo
    scene.render.resolution_x, scene.render.resolution_y = args.video_res
    # No Blender 5 o formato de video so aparece depois de marcar media_type como VIDEO
    try:
        scene.render.image_settings.media_type = 'VIDEO'
    except Exception:
        pass
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
    scene.render.filepath = os.path.join(os.path.dirname(os.path.abspath(args.out)), "voo_jacarezinho.mp4")
    scene.frame_start, scene.frame_end = 1, args.video
    bpy.ops.render.render(animation=True)
    log("video", scene.render.filepath)
log("fim")
