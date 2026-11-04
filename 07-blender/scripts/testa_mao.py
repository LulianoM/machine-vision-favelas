#!/usr/bin/env python3
"""
testa_mao.py: folha de conferencia visual do item 8 (arma na mao), molde do test_pessoas.py.
Uma fila de pessoas com as poses de porte, armas e objetos, renderizada de perto (3 m) e de cima a 35 m,
com a flag desligada (como nos corpora de hoje) e ligada. Em CPU, para nao tirar a GPU de um treino.

  blender -b --python testa_mao.py -- --out C:\\arma3-favela\\blender\\_teste_mao [--sinal -1] [--so-perto]
"""
import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people_mpfb as PM  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", default=r"C:\arma3-favela\blender\_teste_mao")
ap.add_argument("--seed", type=int, default=5)
ap.add_argument("--sinal", type=float, default=1.0)
ap.add_argument("--so-perto", action="store_true")
ap.add_argument("--samples", type=int, default=24)
args = ap.parse_args(argv)
os.makedirs(args.out, exist_ok=True)
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene
PM.build_pool(random.Random(args.seed), 3, print)
PM.PORTE_REALISTA = True
PM.CURL_SINAL = args.sinal

bpy.ops.mesh.primitive_plane_add(size=80)
g = bpy.context.active_object
gm = bpy.data.materials.new("chao")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.32, 0.29, 0.26, 1)
g.data.materials.append(gm)
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
sc.cycles.device = 'CPU'
sc.cycles.samples = args.samples
sc.cycles.use_denoising = True
sc.view_settings.view_transform = 'AgX'
sc.render.image_settings.media_type = 'IMAGE'
sc.render.image_settings.file_format = 'PNG'

# (pose, armada, arma/objeto via classe)
ESPECS = [("empunhando", True, 0), ("lado", True, 0), ("andando", True, 0), ("empunhando", True, 0),
          ("empunhando", False, 2), ("lado", False, 2), ("andando", False, 2), ("costas", True, 0)]


def fila(flag):
    PM.clear_people()
    PM.ARMA_NA_MAO = flag
    rng = random.Random(args.seed + 100)
    for i, (pose, armed, classe) in enumerate(ESPECS):
        p = PM.make_person(rng, i, -4.2 + i * 1.2, 0, 0, armed, pose=pose, classe=classe)
        p["rig"].rotation_euler = (0, 0, math.radians(-90 + rng.uniform(-12, 12)))
        print("PESSOA", i, pose, p["tipo_obj"], p["comp_obj"])


def shot(nome, pos, alvo, lente, res):
    co.location = pos
    cam.lens = lente
    co.rotation_euler = (Vector(alvo) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = os.path.join(args.out, nome + ".png")
    bpy.ops.render.render(write_still=True)
    print("SHOT", nome, flush=True)


for flag in (False, True):
    fila(flag)
    tag = "com_mao" if flag else "sem_mao"
    shot(f"{tag}_perto", (0, -7.5, 1.4), (0, 0, 1.0), 24, (2400, 640))
    # zoom nas maos da pessoa 3 (empunhando, x = -0.6) e da pessoa 1 (lado, x = -3.0)
    shot(f"{tag}_maos_empunhando", (-0.6, -2.0, 1.35), (-0.6, 0, 1.15), 60, (1200, 800))
    shot(f"{tag}_maos_lado", (-3.0, -2.0, 1.0), (-3.0, 0, 0.85), 60, (1200, 800))
    if not args.so_perto:
        shot(f"{tag}_35m", (0, -3, 35), (0, 0, 0.9), 29, (1400, 500))
print("fim")
