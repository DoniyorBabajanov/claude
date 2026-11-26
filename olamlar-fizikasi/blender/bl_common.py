"""Blender (bpy) yordamchilari: sahna, materiallar, geometriya, render va
yozuvlar qatlami bilan SVG yig'ish.

Barcha rasmlar kitob palitrasida, yumshoq yorug'lik va to'q ko'k konturlar
bilan (fotorealizm emas). Yozuvlar Blender'da emas, SVG ning alohida
«yozuvlar» qatlamida — tahrirlanadigan matn bo'lib qoladi.
"""
import base64
import io
import math
import os
import sys

import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "generator"))
import common as C  # noqa: E402  (palitra, shrift, SVG yordamchilari)

OUT_PNG = os.path.join(HERE, "render")
OUT_RENDER = OUT_PNG          # yozuvsiz toza render
OUT_SVG = os.path.join(HERE, "svg")
OUT_BLEND = os.path.join(HERE, "blend")
DPI = 300


# ---------------------------------------------------------------- ranglar
def lin(hexcol, a=1.0):
    """sRGB hex -> Blender chiziqli RGBA."""
    r, g, b = C.hex2rgb(hexcol)

    def s2l(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (s2l(r), s2l(g), s2l(b), a)


# ---------------------------------------------------------------- sahna
def reset(samples=64, transparent=True):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.film_transparent = transparent
    sc.view_settings.view_transform = "Standard"   # palitra ranglari buzilmasin
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    w = bpy.data.worlds.new("dunyo")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = lin("#FFFFFF")
    bg.inputs[1].default_value = 0.85
    return sc


def world(color="#FFFFFF", strength=0.85):
    bg = bpy.context.scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = lin(color)
    bg.inputs[1].default_value = strength


def sun(direction=(-0.5, -0.4, -1.0), strength=2.2, angle=8.0, color="#FFFFFF"):
    ld = bpy.data.lights.new("quyosh_nuri", "SUN")
    ld.energy = strength
    ld.angle = math.radians(angle)
    ld.color = lin(color)[:3]
    ob = bpy.data.objects.new("quyosh_nuri", ld)
    bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = Vector(direction).to_track_quat("-Z", "Y").to_euler()
    return ob


def camera(loc, target, lens=50.0, ortho_scale=None, shift=(0, 0)):
    cd = bpy.data.cameras.new("kamera")
    if ortho_scale:
        cd.type = "ORTHO"
        cd.ortho_scale = ortho_scale
    else:
        cd.lens = lens
    cd.shift_x, cd.shift_y = shift
    cd.clip_end = 1000
    ob = bpy.data.objects.new("kamera", cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = ob
    return ob


def size(w_units, h_units):
    """Kanvas o'lchami 0,1 mm birliklarida -> 300 dpi piksel."""
    sc = bpy.context.scene
    sc.render.resolution_x = math.ceil(w_units / 254 * DPI)
    sc.render.resolution_y = math.ceil(h_units / 254 * DPI)
    sc.render.resolution_percentage = 100
    sc.render.pixel_aspect_x = sc.render.pixel_aspect_y = 1


def project(p):
    """3D nuqta -> kanvas (0,1 mm birlik) koordinatasi."""
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    v = world_to_camera_view(sc, sc.camera, Vector(p))
    W = sc.render.resolution_x / DPI * 254
    H = sc.render.resolution_y / DPI * 254
    return (v.x * W, (1 - v.y) * H)


# ---------------------------------------------------------------- materiallar
_mats = {}


def mat(name, hexcol, rough=0.55, metal=0.0, alpha=1.0, emit=0.0, spec=0.25):
    key = (name, hexcol, rough, metal, alpha, emit)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexcol)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = spec
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
    if emit > 0:
        b.inputs["Emission Color"].default_value = lin(hexcol)
        b.inputs["Emission Strength"].default_value = emit
    _mats[key] = m
    return m


def flat_mat(name, hexcol, strength=1.0):
    """Soyasiz, tekis rang (chiziqlar, strelkalar uchun)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = lin(hexcol)
    em.inputs[1].default_value = strength
    nt.links.new(em.outputs[0], out.inputs[0])
    return m


def collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


def _link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


# ---------------------------------------------------------------- geometriya
def mesh(name, verts, faces, material=None, smooth=True, coll=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(map(float, v)) for v in verts], [], [tuple(map(int, f)) for f in faces])
    me.update()
    if smooth:
        me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    if material:
        me.materials.append(material)
    return _link(ob, coll)


def grid_mesh(name, X, Y, Z, material=None, smooth=True, coll=None):
    nr, nc = X.shape
    verts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    faces = []
    for i in range(nr - 1):
        for j in range(nc - 1):
            a = i * nc + j
            faces.append((a, a + 1, a + nc + 1, a + nc))
    return mesh(name, verts, faces, material, smooth, coll)


def tube(name, points, radius, material, coll=None, cyclic=False, res=6):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for p, q in zip(sp.points, points):
        p.co = (float(q[0]), float(q[1]), float(q[2]), 1.0)
    sp.use_cyclic_u = cyclic
    ob = bpy.data.objects.new(name, cu)
    cu.materials.append(material)
    return _link(ob, coll)


def sphere(name, loc, r, material, coll=None, seg=48):
    me = bpy.data.meshes.new(name)
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    me.materials.append(material)
    return _link(ob, coll)


def cylinder(name, p0, p1, r, material, coll=None, seg=32, caps=True, r2=None, smooth=True):
    import bmesh
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=caps, segments=seg, radius1=r,
                          radius2=r if r2 is None else r2, depth=d.length)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    ob.location = (p0 + p1) / 2
    ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    me.materials.append(material)
    return _link(ob, coll)


# ---------------------------------------------------------------- konturlar
def outlines(coll, thickness_px=3.1, color="#1F3A5F", crease=False):
    """Faqat berilgan kolleksiyadagi ob'ektlar uchun Freestyle kontur
    (0,75 pt @ 300 dpi ≈ 3,1 px)."""
    sc = bpy.context.scene
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = "ABSOLUTE"
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    for ls in list(fs.linesets):
        fs.linesets.remove(ls)
    ls = fs.linesets.new("kontur")
    ls.select_by_collection = True
    ls.collection = coll
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_crease = crease
    ls.linestyle.color = lin(color)[:3]
    ls.linestyle.thickness = thickness_px
    return ls


# ---------------------------------------------------------------- render va SVG
def render(name):
    os.makedirs(OUT_PNG, exist_ok=True)
    os.makedirs(OUT_BLEND, exist_ok=True)
    sc = bpy.context.scene
    raw = os.path.join(OUT_PNG, f"_{name}_alfa.png")
    sc.render.filepath = raw
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_BLEND, f"{name}.blend"))
    return raw


def flatten(raw, out, bg=(255, 255, 255)):
    from PIL import Image
    im = Image.open(raw).convert("RGBA")
    base = Image.new("RGBA", im.size, bg + (255,))
    base.alpha_composite(im)
    base.convert("RGB").save(out, dpi=(DPI, DPI), optimize=True)
    os.remove(raw)
    return out


def compose(name, title, w_units, h_units, png_path, labels, defs="", overlay="",
            bg=None, desc=None):
    """PNG ni «rasm» qatlamiga joylab, yozuvlarni alohida qatlamga qo'yadi."""
    os.makedirs(OUT_SVG, exist_ok=True)
    with open(png_path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    art = (f'<image x="0" y="0" width="{w_units}" height="{h_units}" '
           f'preserveAspectRatio="none" href="data:image/png;base64,{b64}" '
           f'xlink:href="data:image/png;base64,{b64}"/>\n' + overlay)
    doc = C.svg_doc(w_units, h_units, title, art, "\n".join(labels), defs, bg=bg,
                    desc=desc or "«Olamlar fizikasi» uchun Blender’da yaratilgan original rasm. "
                                 "Yozuvlar alohida «yozuvlar» qatlamida.")
    p = os.path.join(OUT_SVG, f"{name}.svg")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("svg", p)
    return p


def solidify(ob, t=0.03):
    m = ob.modifiers.new("qalinlik", "SOLIDIFY")
    m.thickness = t
    m.offset = 0
    return ob


def text3d(name, body, loc, rot_matrix, size_, material, coll=None):
    """Yuzaga yopishgan 3D matn (raqamlar uchun)."""
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size_
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    ob = bpy.data.objects.new(name, cu)
    ob.location = loc
    ob.rotation_euler = rot_matrix.to_euler()
    cu.materials.append(material)
    return _link(ob, coll)
