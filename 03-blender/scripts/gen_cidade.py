"""
gen_cidade.py: dataset de drone sobre a CIDADE DE SOLIDOS (quadra.blend, saida do build_cidade.py),
com as pessoas v2 (people_mpfb): fuzil na mao, poses, grupos, sem camisa. Anotacao YOLO com oclusao.

Uso:
  blender -b --python gen_cidade.py -- --blend C:\arma3-favela\odm\quadra.blend --out dataset_cidade --n 120
  blender -b --python gen_cidade.py -- --blend ... --out dataset_cidade_z30 --n 100 --camera z30
"""
import bpy, sys, os, math, random, json, argparse, time
from mathutils import Vector, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people_mpfb as PM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--blend", default=r"C:\arma3-favela\odm\quadra.blend")
ap.add_argument("--out", default="dataset_cidade")
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--start", type=int, default=1)
ap.add_argument("--res", type=int, nargs=2, default=[3840, 2160])
ap.add_argument("--samples", type=int, default=48)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--alt", type=float, default=100.0)
ap.add_argument("--alt-jitter", type=float, default=10.0)
ap.add_argument("--pitch", type=float, nargs=2, default=[55.0, 90.0])
ap.add_argument("--lens", type=float, nargs=2, default=[20.0, 30.0])
ap.add_argument("--people", type=int, nargs=2, default=[6, 14])
ap.add_argument("--prob-armado", type=float, default=0.5)
ap.add_argument("--min-vis", type=float, default=0.35)
ap.add_argument("--min-lado", type=float, default=0.002)
ap.add_argument("--val", type=float, default=0.15)
ap.add_argument("--pool", type=int, default=6)
ap.add_argument("--repool-every", type=int, default=12)
ap.add_argument("--camera", default="generic", choices=["generic", "z30"])
ap.add_argument("--raio", type=float, default=35.0, help="raio (m) em torno do alvo onde as pessoas sao colocadas")
ap.add_argument("--grupo", type=float, default=0.45, help="probabilidade de colocar um grupo em vez de pessoa solta")
ap.add_argument("--grupo-n", type=int, nargs=2, default=[2, 4])
ap.add_argument("--stamp", default="cid")
ap.add_argument("--margem", type=float, default=150.0, help="distancia minima (m) do alvo ate a borda da cidade, para o anel procedural nao entrar no quadro")
ap.add_argument("--prob-laje", type=float, default=0.25, help="probabilidade de aceitar uma posicao sobre laje/telhado em vez de rua")
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
    print(f"[cid {time.time() - T0:6.1f}s]", *a, flush=True)


bpy.ops.wm.open_mainfile(filepath=args.blend)
scene = bpy.context.scene
# limpa pessoas que vieram no .blend (o gerador coloca as suas)
for c in ("PESSOAS", "_acervo"):
    col = bpy.data.collections.get(c)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
PM.PEOPLE.clear()
PM.POOL.clear()
ent = bpy.data.objects.get("edificacoes")
xs = [v.co.x for v in ent.data.vertices]
ys = [v.co.y for v in ent.data.vertices]
X0, X1, Y0, Y1 = min(xs), max(xs), min(ys), max(ys)
log(f"cidade: {X1-X0:.0f} x {Y1-Y0:.0f} m")

# render
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for d in prefs.devices:
        d.use = d.type == 'OPTIX'
    log("GPU:", [d.name for d in prefs.devices if d.use])
except Exception as e:
    log("GPU prefs:", e)
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = args.res
scene.render.resolution_percentage = 100
scene.render.image_settings.media_type = 'IMAGE'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
cam = bpy.data.objects.get("CAM_OBLIQUA_100m")
sol = bpy.data.objects.get("Sol")
scene.camera = cam


def solo_fn(x, y, dg, laje_ok=None):
    hit, loc, nrm, fi, o, mtx = scene.ray_cast(dg, Vector((x, y, 300)), Vector((0, 0, -1)), distance=800)
    if not hit or nrm.z < 0.9 or o.original.name.startswith(("entorno", "skyline", "anel", "moldura", "detalhes", "esquadrias", "person", "gun")):
        return None
    if o.original.name != "terreno":
        if laje_ok is None:
            laje_ok = rng.random() < args.prob_laje
        if not laje_ok:
            return None
    return loc.z - 0.02


def place_camera(target, gz):
    alt = args.alt + rng.uniform(-args.alt_jitter, args.alt_jitter)
    pitch = rng.uniform(*args.pitch)
    yaw = rng.uniform(0, 2 * math.pi)
    lens = rng.uniform(*args.lens)
    cam.data.lens = lens
    dh = alt / math.tan(math.radians(pitch)) if pitch < 89.5 else 0
    cam.location = (target[0] - math.cos(yaw) * dh, target[1] - math.sin(yaw) * dh, gz + alt)
    d = Vector((target[0], target[1], gz)) - cam.location
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    cam.rotation_euler.rotate_axis('Z', rng.uniform(-0.3, 0.3))
    return dict(alt=round(alt, 1), pitch=round(pitch, 1), yaw=round(math.degrees(yaw), 1), lens=round(lens, 1))


def randomize_light():
    elev = rng.uniform(28, 72)
    az = rng.uniform(0, 360)
    if sol:
        sol.data.energy = rng.uniform(1.6, 3.4)
        sol.data.angle = math.radians(rng.uniform(0.6, 6.0))
        sol.rotation_euler = Euler((math.radians(90 - elev), 0, math.radians(180 - az)), 'XYZ')
    scene.view_settings.exposure = rng.uniform(-0.35, 0.15)
    return dict(sun_elev=round(elev, 1), sun_az=round(az, 1))


PM.build_pool(rng, args.pool, log)
mf = open(os.path.join(OUT, "manifest.jsonl"), "a", encoding="utf-8")
tot = 0
for i in range(args.start, args.start + args.n):
    if i > args.start and (i - args.start) % args.repool_every == 0:
        PM.clear_people()
        PM.build_pool(rng, args.pool, log)
    PM.clear_people()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    M = args.margem
    cx = rng.uniform(X0 + M, X1 - M)
    cy = rng.uniform(Y0 + M, Y1 - M)
    gz = None
    for _ in range(30):
        gz = solo_fn(cx, cy, dg, laje_ok=False)
        if gz is not None:
            break
        cx, cy = rng.uniform(X0 + M, X1 - M), rng.uniform(Y0 + M, Y1 - M)
    if gz is None:
        gz = 0.0
    # pessoas: grupos e soltas num raio de 35 m do alvo
    alvo_n = rng.randint(*args.people)
    idx = 0
    tent = 0
    while idx < alvo_n and tent < alvo_n * 30:
        tent += 1
        x, y = cx + rng.uniform(-args.raio, args.raio), cy + rng.uniform(-args.raio, args.raio)
        z_laje = rng.random() < args.prob_laje
        z = solo_fn(x, y, dg, laje_ok=z_laje)
        if z is None:
            continue
        if rng.random() < args.grupo:
            feitos = PM.place_group(rng, idx, x, y, rng.randint(*args.grupo_n), (lambda a, b, lk=(z_laje): solo_fn(a, b, dg, laje_ok=lk)), armed_prob=args.prob_armado)
        else:
            feitos = [PM.make_person(rng, idx, x, y, z, rng.random() < args.prob_armado)]
        idx += len(feitos)
    light = randomize_light()
    caminfo = place_camera((cx, cy), gz)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    split = "val" if rng.random() < args.val else "train"
    name = f"{args.stamp}_{i:06d}"
    labels = []
    for p in PM.PEOPLE:
        pts = PM.person_points(p, dg)
        bb = PM.bbox_2d(scene, cam, pts, args.min_lado)
        if bb is None:
            continue
        vis = PM.visibility(scene, cam, p, pts, dg)
        if vis < args.min_vis:
            continue
        x1, y1, x2, y2 = bb
        labels.append((p["cls"], (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1, round(vis, 2), p.get("pose", "")))
    scene.render.filepath = os.path.join(OUT, "images", split, name + ".png")
    tr = time.time()
    bpy.ops.render.render(write_still=True)
    with open(os.path.join(OUT, "labels", split, name + ".txt"), "w") as f:
        for l in labels:
            f.write(f"{l[0]} {l[1]:.6f} {l[2]:.6f} {l[3]:.6f} {l[4]:.6f}\n")
    rec = dict(img=name + ".png", split=split, w=args.res[0], h=args.res[1], source="cidade_solidos")
    rec.update(caminfo)
    rec.update(light)
    rec.update(n_people=len(PM.PEOPLE), n_boxes=len(labels), n_armed=sum(1 for l in labels if l[0] == 0),
               poses=[l[6] for l in labels], vis=[l[5] for l in labels], seed=args.seed, render_s=round(time.time() - tr, 1))
    mf.write(json.dumps(rec) + "\n")
    mf.flush()
    tot += len(labels)
    log(f"{name} {split} caixas={len(labels)}/{len(PM.PEOPLE)} alt={caminfo['alt']} pitch={caminfo['pitch']} render={rec['render_s']}s")
mf.close()
with open(os.path.join(OUT, "data.yaml"), "w") as f:
    f.write(f"path: {OUT.replace(os.sep, '/')}\ntrain: images/train\nval: images/val\nnames:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
log(f"fim: {args.n} imagens, {tot} caixas")
