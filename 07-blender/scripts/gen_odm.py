"""
gen_odm.py  (2026-09-12)
Dataset sintetico aereo sobre a MALHA REAL do Jacarezinho (fotogrametria ODM das fotos da PCERJ, 2022):
  - importa odm_textured_model_geo.obj (textura fotografica real)
  - coloca pessoas MPFB (riggadas, posadas, roupa procedural, armadas ou nao) sobre a malha via ray cast
    (cai naturalmente em rua, beco ou laje)
  - camera drone a 100 m (ou preset z30 = camera real da PCERJ a 150 m)
  - anotacao YOLO com teste de oclusao, mesmo formato dos outros geradores

Uso:
  blender -b --python gen_odm.py -- --mesh C:\arma3-favela\odm\sudoeste\odm_texturing\odm_textured_model_geo.obj --out dataset_odm --n 100

Dados da PCERJ: uso interno, nao redistribuir as imagens geradas com a textura real sem autorizacao.
"""
import bpy, sys, os, math, random, json, argparse, time, colorsys
from mathutils import Vector, Euler, Matrix
from bpy_extras.object_utils import world_to_camera_view
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people_mpfb as PM
PEOPLE = PM.PEOPLE


ASSETS = r"C:\arma3-favela\assets"
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--mesh", default=r"C:\arma3-favela\odm\sudoeste\odm_texturing\odm_textured_model_geo.obj")
ap.add_argument("--out", default="dataset_odm")
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--start", type=int, default=1)
ap.add_argument("--res", type=int, nargs=2, default=[3840, 2160])
ap.add_argument("--samples", type=int, default=48)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--alt", type=float, default=100.0)
ap.add_argument("--alt-jitter", type=float, default=8.0)
ap.add_argument("--pitch", type=float, nargs=2, default=[60.0, 90.0])
ap.add_argument("--lens", type=float, nargs=2, default=[20.0, 30.0])
ap.add_argument("--people", type=int, nargs=2, default=[4, 9])
ap.add_argument("--prob-armado", type=float, default=0.5)
ap.add_argument("--min-vis", type=float, default=0.35)
ap.add_argument("--min-lado", type=float, default=0.002)
ap.add_argument("--val", type=float, default=0.15)
ap.add_argument("--pool", type=int, default=6)
ap.add_argument("--repool-every", type=int, default=10)
ap.add_argument("--margin", type=float, default=60.0, help="margem (m) da borda da malha que nao recebe centro de cena")
ap.add_argument("--camera", default="generic", choices=["generic", "z30"])
ap.add_argument("--save-blend", default=None)
args = ap.parse_args(argv)
if args.camera == "z30":
    args.res = [1920, 1080]
    args.alt = 150.0
    args.alt_jitter = 3.0
    args.pitch = [86.0, 90.0]
    args.lens = [4.3 * 36 / 5.37, 4.3 * 36 / 5.37]

OUT = os.path.abspath(args.out)
for sp in ("train", "val"):
    os.makedirs(os.path.join(OUT, "images", sp), exist_ok=True)
    os.makedirs(os.path.join(OUT, "labels", sp), exist_ok=True)
rng = random.Random(args.seed)
T0 = time.time()


def log(*a):
    print(f"[odm {time.time() - T0:6.1f}s]", *a, flush=True)


def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)


# ================================================================= malha ODM
def load_mesh(path):
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=path, forward_axis='Y', up_axis='Z')
    new = [o for o in bpy.data.objects if o not in before and o.type == 'MESH']
    if not new:
        raise RuntimeError("OBJ sem malhas")
    if len(new) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for o in new:
            o.select_set(True)
        bpy.context.view_layer.objects.active = new[0]
        bpy.ops.object.join()
        new = [bpy.context.active_object]
    m = new[0]
    m.name = "odm_mesh"
    # centraliza em XY (as coordenadas geo do ODM sao UTM com offset; tira coordenadas absolutas do dataset)
    xs = [v.co.x for v in m.data.vertices]
    ys = [v.co.y for v in m.data.vertices]
    zs = [v.co.z for v in m.data.vertices]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    zmed = sorted(zs)[len(zs) // 2]
    m.location = (-cx, -cy, -zmed)
    bpy.context.view_layer.update()
    # materiais: garante roughness alta e sem especular (textura fotografica ja tem luz embutida)
    for mat in m.data.materials:
        if mat and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Roughness"].default_value = 0.95
                try:
                    bsdf.inputs["Specular IOR Level"].default_value = 0.1
                except Exception:
                    pass
    for p in m.data.polygons:
        p.use_smooth = False
    ext = dict(x0=min(xs) - cx, x1=max(xs) - cx, y0=min(ys) - cy, y1=max(ys) - cy, z0=min(zs) - zmed, z1=max(zs) - zmed)
    log(f"malha: {len(m.data.vertices)} verts, {len(m.data.polygons)} faces, extensao {ext['x1']-ext['x0']:.0f} x {ext['y1']-ext['y0']:.0f} m, z {ext['z0']:.1f}..{ext['z1']:.1f}")
    return m, ext


def surface_z(x, y, depsgraph, allow_dsm=True):
    """altura da superficie (rua, beco ou laje) na malha real via ray cast para baixo"""
    hit, loc, nrm, fi, obj, mtx = bpy.context.scene.ray_cast(depsgraph, Vector((x, y, 400.0)), Vector((0, 0, -1)), distance=800.0)
    if not hit or obj is None:
        return None, None
    n = obj.original.name
    if n != "odm_mesh" and not (allow_dsm and n == "dsm_mesh"):
        return None, None
    return loc.z, nrm


def load_dsm_mesh(odm_mesh):
    """malha 2.5D (DSM + ortomosaico) por baixo da malha ODM: tapa buracos e bordas com a foto real"""
    blend = os.path.join(os.path.dirname(os.path.dirname(args.mesh)), "dsm_mesh.blend")
    if not os.path.exists(blend):
        log("sem dsm_mesh.blend (rode export_dsm.py + build_dsm_mesh.py); seguindo so com a malha ODM")
        return None
    with bpy.data.libraries.load(blend, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n == "dsm_mesh"]
    o = dst.objects[0]
    bpy.context.scene.collection.objects.link(o)
    o.location = (odm_mesh.location.x, odm_mesh.location.y, odm_mesh.location.z - 0.25)
    for mat in o.data.materials:
        pass
    log(f"dsm_mesh: {len(o.data.vertices)} verts")
    return o


def coverage(cx, cy, depsgraph, half=70.0, n=6):
    """fracao de pontos numa caixa em torno do centro que caem sobre a malha ODM (evita bordas e buracos)"""
    ok = 0
    for i in range(n):
        for j in range(n):
            x = cx - half + (2 * half) * (i + 0.5) / n
            y = cy - half + (2 * half) * (j + 0.5) / n
            z, _ = surface_z(x, y, depsgraph, allow_dsm=False)
            ok += z is not None
    return ok / (n * n)


# ================================================================= pessoas (MPFB, modulo people_mpfb)
def place_people(center, n, depsgraph, radius=32):
    PM.clear_people()
    placed = tries = 0
    while placed < n and tries < 400:
        tries += 1
        x = center[0] + rng.uniform(-radius, radius)
        y = center[1] + rng.uniform(-radius, radius)
        z, nrm = surface_z(x, y, depsgraph)
        if z is None or nrm is None or nrm.z < 0.8:
            continue
        if any(math.hypot(p["x"] - x, p["y"] - y) < 0.9 for p in PEOPLE):
            continue
        PM.make_person(rng, placed, x, y, z - 0.02, rng.random() < args.prob_armado)
        placed += 1
    return placed


# ================================================================= luz e camera
PH = json.load(open(os.path.join(ASSETS, "polyhaven", "index.json")))
HDRIS = list(PH["hdris"].items())


def setup_world():
    w = bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    mp = nt.nodes.new("ShaderNodeMapping")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    sun = bpy.data.lights.new("Sun", type='SUN')
    so = bpy.data.objects.new("Sun", sun)
    bpy.context.scene.collection.objects.link(so)
    return dict(env=env, map=mp, bg=bg, sun=so)


def randomize_light(W):
    # a textura ja traz a luz do meio-dia de agosto embutida: iluminacao suave, sol moderado quase a pino
    name, rel = rng.choice(HDRIS)
    W["env"].image = bpy.data.images.load(os.path.join(ASSETS, "polyhaven", rel), check_existing=True)
    W["map"].inputs["Rotation"].default_value = (0, 0, rng.uniform(0, 2 * math.pi))
    W["bg"].inputs["Strength"].default_value = rng.uniform(0.6, 1.0)
    # sol coerente com as sombras ja gravadas na textura: fotos de 01 e 02/08/2022 entre 11h50 e 12h07,
    # sol quase no meio-dia solar no Rio: elevacao ~49 graus, azimute ~norte (sombras para o sul)
    elev = math.radians(rng.uniform(45, 54))
    rot = math.radians(rng.uniform(-12, 12))
    W["sun"].data.energy = rng.uniform(1.5, 2.8)
    W["sun"].data.angle = math.radians(rng.uniform(1, 4))
    W["sun"].rotation_euler = Euler((math.pi / 2 - elev, 0, rot + math.pi), 'XYZ')
    bpy.context.scene.view_settings.exposure = rng.uniform(-0.6, 0.1)
    return dict(light="hdri+sun", hdri=name, sun_elev=round(math.degrees(elev), 1), sun_az=round(math.degrees(rot), 1))


def setup_camera():
    cam = bpy.data.cameras.new("DroneCam")
    cam.sensor_width = 36
    cam.sensor_fit = 'HORIZONTAL'
    co = bpy.data.objects.new("DroneCam", cam)
    bpy.context.scene.collection.objects.link(co)
    bpy.context.scene.camera = co
    return co


def place_camera(co, target, gz):
    alt = args.alt + rng.uniform(-args.alt_jitter, args.alt_jitter)
    pitch = rng.uniform(args.pitch[0], args.pitch[1])
    yaw = rng.uniform(0, 2 * math.pi)
    lens = rng.uniform(args.lens[0], args.lens[1])
    co.data.lens = lens
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




def setup_render(scene):
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.engine = 'CYCLES'
    scene.view_settings.view_transform = 'AgX'
    try:
        scene.view_settings.look = 'AgX - Medium Contrast'
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
    scene.cycles.max_bounces = 3


# ================================================================= main
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
scene = bpy.context.scene
setup_render(scene)
W = setup_world()
cam = setup_camera()
mesh, EXT = load_mesh(args.mesh)
dsm = load_dsm_mesh(mesh)
PM.build_pool(rng, args.pool, log)
mf = open(os.path.join(OUT, "manifest.jsonl"), "a", encoding="utf-8")
tot = 0
for i in range(args.start, args.start + args.n):
    if i > args.start and (i - args.start) % args.repool_every == 0:
        PM.build_pool(rng, args.pool, log)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    # centro de cena dentro da malha, longe da borda e de buracos (cobertura da malha ODM >= 92%)
    best, bestc = -1, None
    for _ in range(60):
        cx = rng.uniform(EXT["x0"] + args.margin, EXT["x1"] - args.margin)
        cy = rng.uniform(EXT["y0"] + args.margin, EXT["y1"] - args.margin)
        c = coverage(cx, cy, depsgraph)
        if c > best:
            best, bestc = c, (cx, cy)
        if c >= 0.92:
            break
    cx, cy = bestc
    gz, _n = surface_z(cx, cy, depsgraph)
    if gz is None:
        gz = 0.0
    place_people((cx, cy), rng.randint(args.people[0], args.people[1]), depsgraph)
    light = randomize_light(W)
    caminfo = place_camera(cam, (cx, cy), gz)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    split = "val" if rng.random() < args.val else "train"
    name = f"odm_{i:06d}"
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
        labels.append((p["cls"], (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1, round(vis, 2)))
    scene.render.filepath = os.path.join(OUT, "images", split, name + ".png")
    tr = time.time()
    bpy.ops.render.render(write_still=True)
    with open(os.path.join(OUT, "labels", split, name + ".txt"), "w") as f:
        for l in labels:
            f.write(f"{l[0]} {l[1]:.6f} {l[2]:.6f} {l[3]:.6f} {l[4]:.6f}\n")
    rec = dict(img=name + ".png", split=split, w=args.res[0], h=args.res[1], source="odm_mesh")
    rec.update(caminfo)
    rec.update(light)
    rec.update(n_people=len(PEOPLE), n_boxes=len(labels), n_armed=sum(1 for l in labels if l[0] == 0), vis=[l[5] for l in labels], seed=args.seed, render_s=round(time.time() - tr, 1))
    mf.write(json.dumps(rec) + "\n")
    mf.flush()
    tot += len(labels)
    log(f"{name} {split} caixas={len(labels)}/{len(PEOPLE)} alt={caminfo['alt']} pitch={caminfo['pitch']} render={rec['render_s']}s")
mf.close()
with open(os.path.join(OUT, "data.yaml"), "w") as f:
    f.write(f"path: {OUT.replace(os.sep, '/')}\ntrain: images/train\nval: images/val\nnames:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
if args.save_blend:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.save_blend))
log(f"fim: {args.n} imagens, {tot} caixas")
