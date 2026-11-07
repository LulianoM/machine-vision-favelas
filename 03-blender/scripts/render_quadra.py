"""
render_quadra.py: renderiza um recorte da favela de angulos fixos, para comparar a malha antiga
(fotogrametria bruta, paredes derretidas) com a malha nova (degraus do DSM, paredes verticais,
texturizada com as fotos reais pelo ODM).

Uso:
  blender -b --python render_quadra.py -- --obj <caminho.obj> --sufixo nova --centro 50 0
"""
import bpy, sys, os, math, json, argparse
from mathutils import Vector, Euler

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--obj", required=True)
ap.add_argument("--sufixo", required=True)
ap.add_argument("--centro", type=float, nargs=2, default=[50.0, 0.0])
ap.add_argument("--out", default=r"C:\arma3-favela\odm\quadra")
ap.add_argument("--res", type=int, nargs=2, default=[1600, 900])
ap.add_argument("--samples", type=int, default=48)
args = ap.parse_args(argv)
os.makedirs(args.out, exist_ok=True)

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
scene = bpy.context.scene

bpy.ops.wm.obj_import(filepath=args.obj, forward_axis='Y', up_axis='Z')
malhas = [o for o in bpy.data.objects if o.type == 'MESH']
if len(malhas) > 1:
    bpy.ops.object.select_all(action='DESELECT')
    for o in malhas:
        o.select_set(True)
    bpy.context.view_layer.objects.active = malhas[0]
    bpy.ops.object.join()
m = bpy.context.view_layer.objects.active or malhas[0]
m.name = "quadra"
pols = m.data.polygons
pols.foreach_set("use_smooth", [False] * len(pols))
m.data.update()
for mat in m.data.materials:
    if mat and mat.use_nodes:
        b = mat.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Roughness"].default_value = 0.95
            for k in ("Specular IOR Level", "Specular"):
                if k in b.inputs:
                    b.inputs[k].default_value = 0.05
                    break
print(f"MALHA {len(m.data.vertices)} verts, {len(pols)} faces")

# ----------------------------------------------------------------- luz: ambiente neutro + sol do voo
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
for attr, val in (("sun_elevation", math.radians(ELEV)), ("sun_rotation", math.radians(AZ)),
                  ("altitude", 30), ("air_density", 0.6), ("dust_density", 1.0), ("sun_intensity", 0.0)):
    try:
        setattr(sky, attr, val)
    except Exception:
        pass
nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0
amb = nt.nodes.new("ShaderNodeBackground")
amb.inputs["Color"].default_value = (1.0, 0.96, 0.90, 1.0)
amb.inputs["Strength"].default_value = 0.95
lp = nt.nodes.new("ShaderNodeLightPath")
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
nt.links.new(amb.outputs["Background"], mx.inputs[1])
nt.links.new(bg.outputs["Background"], mx.inputs[2])
out_w = next(n for n in nt.nodes if n.type == 'OUTPUT_WORLD')
nt.links.new(mx.outputs["Shader"], out_w.inputs["Surface"])
sol = bpy.data.lights.new("Sol", type='SUN')
sol.energy = 1.0
sol.angle = math.radians(2.0)
so = bpy.data.objects.new("Sol", sol)
scene.collection.objects.link(so)
so.rotation_euler = Euler((math.radians(90 - ELEV), 0, math.radians(180 - AZ)), 'XYZ')

scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Medium Contrast'
except Exception:
    pass
scene.view_settings.exposure = 0.15

# ----------------------------------------------------------------- render
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
scene.cycles.max_bounces = 3
scene.render.resolution_x, scene.render.resolution_y = args.res
scene.render.image_settings.media_type = 'IMAGE'
scene.render.image_settings.file_format = 'PNG'

bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
CX, CY = args.centro


def solo(x, y):
    hit, loc, nrm, fi, o, mtx = scene.ray_cast(dg, Vector((x, y, 400)), Vector((0, 0, -1)), distance=900)
    return loc.z if hit else 0.0


GZ = solo(CX, CY)
print(f"CENTRO ({CX}, {CY}) solo {GZ:.1f}")


def camera(nome, lente, pos, alvo):
    c = bpy.data.cameras.new(nome)
    c.lens = lente
    c.sensor_width = 36
    c.clip_start = 0.05
    c.clip_end = 2000
    o = bpy.data.objects.new(nome, c)
    scene.collection.objects.link(o)
    o.location = pos
    d = Vector(alvo) - Vector(pos)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o


# angulos escolhidos para mostrar PAREDE, que e onde a malha antiga falha
vistas = [
    ("a_obliqua_60m", 28, (CX - 55, CY - 55, GZ + 60), (CX, CY, GZ + 4)),
    ("b_rasante_25m", 24, (CX - 45, CY - 45, GZ + 25), (CX, CY, GZ + 5)),
    ("c_beco_8m", 20, (CX - 38, CY - 38, GZ + 9), (CX, CY, GZ + 6)),
]
for nome, lente, pos, alvo in vistas:
    cam = camera(nome, lente, pos, alvo)
    scene.camera = cam
    scene.render.filepath = os.path.join(args.out, f"{nome}_{args.sufixo}.png")
    bpy.ops.render.render(write_still=True)
    print("RENDER", nome, args.sufixo)
print("fim")
