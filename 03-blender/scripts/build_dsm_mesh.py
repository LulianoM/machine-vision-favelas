"""
build_dsm_mesh.py (Blender): constroi a malha 2.5D do terreno real (DSM do ODM) texturizada com o ortomosaico
e salva em <setor>/dsm_mesh.blend (objeto "dsm_mesh"). Usada por gen_odm.py por baixo da malha ODM
para preencher buracos e bordas com a foto real.
Uso: blender -b --python build_dsm_mesh.py -- --sector sudoeste
"""
import bpy, bmesh, sys, os, json, argparse
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--sector", default="sudoeste")
args = ap.parse_args(argv)
root = os.path.join(r"C:\arma3-favela\odm", args.sector)
g = np.load(os.path.join(root, "dsm_grid.npz"))
z, x0, y0, rx, ry, W, H = g["z"], float(g["x0"]), float(g["y0"]), float(g["resx"]), float(g["resy"]), int(g["W"]), int(g["H"])
ot = json.load(open(os.path.join(root, "ortho_tex.json")))

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
me = bpy.data.meshes.new("dsm_mesh")
xs = x0 + np.arange(W) * rx
ys = y0 + np.arange(H) * ry
X, Y = np.meshgrid(xs, ys)
verts = np.stack([X.ravel(), Y.ravel(), z.ravel()], axis=1).astype(np.float32)
idx = np.arange(W * H).reshape(H, W)
a = idx[:-1, :-1].ravel()
b = idx[:-1, 1:].ravel()
c = idx[1:, 1:].ravel()
d = idx[1:, :-1].ravel()
faces = np.stack([a, b, c, d], axis=1)
# descarta as faces totalmente sem dado (a borda preta do ortomosaico, que aparecia como
# uma saia escura no horizonte). Buracos internos pequenos ficam, porque servem de tampa
# por baixo da malha de fotogrametria.
if "semdado" in g:
    sd = g["semdado"].astype(bool)
    quatro = sd[:-1, :-1].ravel() & sd[:-1, 1:].ravel() & sd[1:, 1:].ravel() & sd[1:, :-1].ravel()
    faces = faces[~quatro]
    print(f"faces sem dado removidas: {int(quatro.sum())} de {len(quatro)}")
me.vertices.add(len(verts))
me.vertices.foreach_set("co", verts.ravel())
me.loops.add(len(faces) * 4)
me.polygons.add(len(faces))
me.loops.foreach_set("vertex_index", faces.ravel())
me.polygons.foreach_set("loop_start", np.arange(len(faces)) * 4)
me.polygons.foreach_set("loop_total", np.full(len(faces), 4))
me.update(calc_edges=True)
# UV planar a partir das coordenadas (ortho: linha 0 = norte = v 1)
uv = me.uv_layers.new(name="ortho")
u = (X.ravel() - ot["left"]) / (ot["right"] - ot["left"])
v = (Y.ravel() - ot["bottom"]) / (ot["top"] - ot["bottom"])
uvs = np.stack([u[faces.ravel()], v[faces.ravel()]], axis=1).astype(np.float32)
uv.data.foreach_set("uv", uvs.ravel())
for p in me.polygons:
    p.use_smooth = True
mat = bpy.data.materials.new("m_ortho")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Roughness"].default_value = 0.95
try:
    bsdf.inputs["Specular IOR Level"].default_value = 0.1
except Exception:
    pass
img = nt.nodes.new("ShaderNodeTexImage")
img.image = bpy.data.images.load(os.path.join(root, "ortho_tex.jpg"))
nt.links.new(img.outputs["Color"], bsdf.inputs["Base Color"])
me.materials.append(mat)
o = bpy.data.objects.new("dsm_mesh", me)
bpy.context.scene.collection.objects.link(o)
print("dsm_mesh", len(me.vertices), "verts", len(me.polygons), "faces")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root, "dsm_mesh.blend"))
print("salvo", os.path.join(root, "dsm_mesh.blend"))
