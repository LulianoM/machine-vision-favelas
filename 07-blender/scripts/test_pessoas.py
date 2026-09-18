"""
test_pessoas.py: folha de teste do modulo people_mpfb v2. Uma fila de pessoas com todas as poses e
armas, renderizada de perto (4 m), de cima a 30 m e a 100 m, para conferir empunhadura e silhueta.
Uso: blender -b --python test_pessoas.py -- --out C:\arma3-favela\odm\pessoas
"""
import bpy, sys, os, math, random, argparse
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people_mpfb as PM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default=r"C:\arma3-favela\odm\pessoas")
ap.add_argument("--seed", type=int, default=5)
args = ap.parse_args(argv)
os.makedirs(args.out, exist_ok=True)
rng = random.Random(args.seed)
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene
PM.build_pool(rng, 6, print)

bpy.ops.mesh.primitive_plane_add(size=80)
g = bpy.context.active_object
gm = bpy.data.materials.new("chao")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.32, 0.29, 0.26, 1)
g.data.materials.append(gm)

especs = [("parado", False, None), ("andando", False, None), ("sentado", False, None), ("bracos_cruzados", False, None), 
          ("empunhando", True, "fuzil"), ("empunhando", True, "fuzil"), ("lado", True, "fuzil"), ("costas", True, "fuzil"),
          ("andando", True, "fuzil"), ("empunhando", True, "pistola"), ("lado", True, "pistola")]
for i, (pose, armed, arma) in enumerate(especs):
    p = PM.make_person(rng, i, -7.2 + i * 1.2, 0, 0, armed, pose=pose, arma=arma)
    p["rig"].rotation_euler = (0, 0, math.radians(-90 + rng.uniform(-15, 15)))   # de frente para -Y (camera)

sun = bpy.data.lights.new("Sol", 'SUN')
sun.energy = 3.0
sun.angle = math.radians(3)
so = bpy.data.objects.new("Sol", sun)
sc.collection.objects.link(so)
so.rotation_euler = (math.radians(40), 0, math.radians(35))
w = bpy.data.worlds.new("W")
sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.75, 0.8, 0.9, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.7
cam = bpy.data.cameras.new("c")
co = bpy.data.objects.new("c", cam)
sc.collection.objects.link(co)
sc.camera = co
sc.render.engine = 'CYCLES'
sc.cycles.device = 'GPU'
sc.cycles.samples = 48
sc.cycles.use_denoising = True
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == 'OPTIX'
sc.view_settings.view_transform = 'AgX'
sc.render.image_settings.media_type = 'IMAGE'
sc.render.image_settings.file_format = 'PNG'


def shot(nome, pos, alvo, lente, res):
    co.location = pos
    cam.lens = lente
    co.rotation_euler = (Vector(alvo) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = os.path.join(args.out, nome + ".png")
    bpy.ops.render.render(write_still=True)
    print("SHOT", nome)


shot("a_frente_4m", (0, -9.5, 1.5), (0, 0, 0.95), 40, (2400, 700))
shot("b_alto_30m", (0, -14, 28), (0, 0, 0.9), 45, (2400, 900))
shot("c_drone_100m", (0, -40, 95), (0, 0, 0.9), 24, (3840, 2160))
print("fim")
