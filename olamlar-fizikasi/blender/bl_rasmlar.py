"""Blender'da yaratiladigan rasmlar. Foydalanish: python3 bl_rasmlar.py 2-2 [3-4 ...]"""
import math
import sys

import numpy as np

import bl_common as B  # bpy ni yuklaydi (mathutils undan keyin)
from bl_common import C
from mathutils import Vector

BLUE, GOLD, CREAM, ACCENT = C.BLUE, C.GOLD, C.CREAM, C.ACCENT


def fit_camera(cam, pts3d, span=(0.95, 0.86), top=0.10):
    """Kamerani (lens/ortho va shift) nuqtalar kadrga sig'adigan qilib sozlaydi."""
    import bpy
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    W, H = sc.render.resolution_x, sc.render.resolution_y
    bpy.context.view_layer.update()
    for _ in range(4):
        vs = [world_to_camera_view(sc, cam, Vector(p)) for p in pts3d]
        xs = [v.x for v in vs]
        ys = [1 - v.y for v in vs]
        sx, sy = max(xs) - min(xs), max(ys) - min(ys)
        k = min(span[0] / sx, span[1] / sy)
        if cam.data.type == "ORTHO":
            cam.data.ortho_scale /= k
        else:
            cam.data.lens *= k
        bpy.context.view_layer.update()
        vs = [world_to_camera_view(sc, cam, Vector(p)) for p in pts3d]
        xs = [v.x for v in vs]
        ys = [1 - v.y for v in vs]
        cx = (max(xs) + min(xs)) / 2
        cy = (max(ys) + min(ys)) / 2
        want_cy = top + (max(ys) - min(ys)) / 2
        big = max(W, H)
        cam.data.shift_x += (cx - 0.5) * W / big
        cam.data.shift_y -= (cy - want_cy) * H / big
        bpy.context.view_layer.update()


# =========================================================================
# 2.2 — Egrilangan fazo-vaqt: rezina choyshab
# =========================================================================
def rasm_2_2():
    W, H = 1120, 700
    B.reset(samples=64)
    B.size(W, H)
    L, R0, s, A = 10.0, 8.6, 1.05, 6.2
    LY0, LY1 = -L, L + 4

    def zf(x, y):
        r = np.sqrt(x * x + y * y)
        g = 1 / np.sqrt(1 + (r / s) ** 2)
        w = np.clip(1 - (r / R0) ** 2, 0, None) ** 2
        return -A * g * w

    kontur = B.collection("kontur")
    X, Y = np.meshgrid(np.linspace(-L, L, 241), np.linspace(LY0, LY1, 289))
    B.grid_mesh("choyshab", X, Y, zf(X, Y), B.mat("qaymoq", C.mix(CREAM, GOLD, 0.10), rough=0.85, spec=0.1), coll=kontur)
    line_m = B.flat_mat("setka", BLUE)
    for v in np.arange(LY0, LY1 + 0.01, 1.0):
        xs = np.linspace(-L, L, 400)
        B.tube("setka_x", np.stack([xs, np.full_like(xs, v), zf(xs, v) + 0.02], 1), 0.028, line_m)
    for v in np.arange(-L, L + 0.01, 1.0):
        ys = np.linspace(LY0, LY1, 480)
        B.tube("setka_y", np.stack([np.full_like(ys, v), ys, zf(v, ys) + 0.02], 1), 0.028, line_m)
    Rs = 1.75
    rr = np.linspace(0, Rs * 0.999, 400)
    sun_c = (0, 0, float(np.max(zf(rr, 0 * rr) + np.sqrt(Rs ** 2 - rr ** 2)) - 0.05))
    B.sphere("Quyosh", sun_c, Rs, B.mat("oltin", C.mix(GOLD, CREAM, 0.15), rough=0.45, spec=0.4), coll=kontur)
    re, th_e, Re = 4.0, math.radians(150), 0.55
    ex, ey = re * math.cos(th_e), re * math.sin(th_e)
    earth_c = (ex, ey, float(zf(ex, ey)) + Re * 0.92)
    B.sphere("Yer", earth_c, Re, B.mat("kok", C.mix(BLUE, "#FFFFFF", 0.12), rough=0.5), coll=kontur)
    # orbita: punktir
    om = B.flat_mat("orbita", ACCENT)
    n = 44
    for k in range(n):
        if k % 2:
            continue
        t = np.linspace(2 * math.pi * k / n, 2 * math.pi * (k + 1) / n, 8)
        P = np.stack([re * np.cos(t), re * np.sin(t), zf(re * np.cos(t), re * np.sin(t)) + 0.14], 1)
        B.tube("orbita", P, 0.055, om)
    B.sun(direction=(0.55, 0.65, -1.0), strength=2.6, angle=12)
    B.world("#FFFFFF", 0.65)
    B.outlines(kontur)
    cam = B.camera((0, -19.5, 14.8), (0, 1.6, -2.2), lens=35)
    corners = [(-L, LY0, 0), (L, LY0, 0), (L, LY1, 0), (-L, LY1, 0),
               (0, 0, sun_c[2] + Rs)]
    fit_camera(cam, corners, span=(0.965, 0.83), top=0.12)
    raw = B.render("rasm_2-2")
    png = B.flatten(raw, B.OUT_RENDER + "/rasm_2-2.png")
    # yozuvlar
    P = B.project
    tr = P((L, LY1, 0))
    sc_ = P(sun_c)
    top_ = P((sun_c[0], sun_c[1], sun_c[2] + Rs * 0.55))
    ec = P(earth_c)
    tl = P((-L, LY1, 0))
    q = P((6.2, -3.4, float(zf(6.2, -3.4))))
    lab = []
    qx = sc_[0] + 20
    lab.append(C.text(qx + 14, tr[1] - 14, "Quyosh"))
    lab.append(C.leader([(qx, tr[1] - 22), (qx, top_[1])]))
    lab.append(C.text(W - 12, tr[1] - 14, "egrilangan fazo", anchor="end"))
    lab.append(C.leader([(W - 160, tr[1] - 2), (W - 160, tr[1] + 30), q]))
    lab.append(C.text(tl[0] - 60, tl[1] + 100, "Yer", anchor="end"))
    lab.append(C.leader([(tl[0] - 52, tl[1] + 90), (ec[0] - 14, ec[1] - 12)]))
    B.compose("rasm_2-2", "Rasm 2.2. Egrilangan fazo-vaqt: rezina choyshab modeli", W, H, png, lab)


def pencil(B, x, y, z_tip, z_top, coll):
    """Olti qirrali qalam (uchi pastda)."""
    r = 0.13
    wood = B.mat("yogoch", C.mix(CREAM, GOLD, 0.35), rough=0.8)
    body = B.mat("qalam", GOLD, rough=0.5)
    B.cylinder("grafit", (x, y, z_tip), (x, y, z_tip + 0.12), 0.0, B.mat("grafit", C.G1, rough=0.6),
               coll, seg=6, r2=r * 0.32, smooth=False)
    B.cylinder("yogoch_uch", (x, y, z_tip + 0.12), (x, y, z_tip + 0.42), r * 0.32, wood, coll, seg=6,
               r2=r, smooth=False)
    B.cylinder("qalam_tana", (x, y, z_tip + 0.42), (x, y, z_top - 0.3), r, body, coll, seg=6, smooth=False)
    B.cylinder("halqa", (x, y, z_top - 0.3), (x, y, z_top - 0.14), r * 1.02, B.mat("metall", C.G4, rough=0.3, metal=0.6),
               coll, seg=24)
    B.cylinder("o'chirg'ich", (x, y, z_top - 0.14), (x, y, z_top), r * 0.98, B.mat("ochirgich", ACCENT, rough=0.7),
               coll, seg=24)


# =========================================================================
# 2.4 — Fazo-vaqt tuneli: buklangan qog'oz
# =========================================================================
def rasm_2_4():
    W, H = 540, 700
    B.reset(samples=64)
    B.size(W, H)
    kont = B.collection("kontur")
    paper = B.mat("qogoz", C.mix(CREAM, GOLD, 0.06), rough=0.9, spec=0.1)
    dark = B.flat_mat("nuqta", BLUE)
    Lp, Wd, r = 5.6, 2.3, 0.5
    zt = 4.4
    # 1) tekis varaq
    X, Y = np.meshgrid(np.linspace(-Lp / 2, Lp / 2, 2), np.linspace(-Wd / 2, Wd / 2, 2))
    ob = B.grid_mesh("tekis_varaq", X, Y, np.full_like(X, zt), paper, smooth=False, coll=kont)
    B.solidify(ob, 0.03)
    A1, B1 = (-Lp / 2 + 0.38, 0, zt + 0.02), (Lp / 2 - 0.38, 0, zt + 0.02)
    for p in (A1, B1):
        B.cylinder("nuqta", p, (p[0], p[1], p[2] + 0.01), 0.1, dark, seg=32)
    om = B.flat_mat("punktir", ACCENT)
    xs = np.linspace(A1[0] + 0.16, B1[0] - 0.16, 17)
    for i in range(0, 16, 2):
        B.tube("punktir", [(xs[i], 0, zt + 0.025), (xs[i + 1], 0, zt + 0.025)], 0.028, om)
    # 2) U shaklida buklangan varaq
    lay = (Lp - math.pi * r) / 2
    xf = -lay / 2 - 0.2                      # bukilish o'qi
    path = [(xf + lay - t, r) for t in np.linspace(0, lay, 12)]
    path += [(xf + r * math.cos(a), r * math.sin(a)) for a in np.linspace(math.pi / 2, 3 * math.pi / 2, 40)[1:]]
    path += [(xf + t, -r) for t in np.linspace(0, lay, 12)[1:]]
    verts, faces = [], []
    for i, (x, z) in enumerate(path):
        verts += [(x, -Wd / 2, z), (x, Wd / 2, z)]
        if i:
            a = 2 * (i - 1)
            faces.append((a, a + 2, a + 3, a + 1))
    ob = B.mesh("buklangan_varaq", verts, faces, paper, smooth=True, coll=kont)
    B.solidify(ob, 0.03)
    xa = xf + lay - 0.38
    pencil(B, xa, 0, -r - 1.55, r + 1.35, kont)
    B.sun(direction=(0.6, 0.5, -1.0), strength=2.4, angle=10)
    B.world("#FFFFFF", 0.8)
    cam = B.camera((-6, -10, 8.5), (0, 0, 1.6), ortho_scale=8)
    B.outlines(kont)
    pts = [(sx * Lp / 2, sy * Wd / 2, zt) for sx in (-1, 1) for sy in (-1, 1)]
    pts += [(xf - r, sy * Wd / 2, sz * r) for sy in (-1, 1) for sz in (-1, 1)]
    pts += [(xf + lay, sy * Wd / 2, sz * r) for sy in (-1, 1) for sz in (-1, 1)]
    pts += [(xa, 0, -r - 1.55), (xa, 0, r + 1.35)]
    fit_camera(cam, pts, span=(0.92, 0.82), top=0.04)
    png = B.flatten(B.render("rasm_2-4"), B.OUT_RENDER + "/rasm_2-4.png")
    P = B.project
    a1, b1 = P(A1), P(B1)
    a2, b2 = P((xa, 0, r)), P((xa, 0, -r))
    lab = [C.text(a1[0], a1[1] - 20, "A", anchor="middle", weight="bold"),
           C.text(b1[0], b1[1] - 20, "B", anchor="middle", weight="bold"),
           C.text((a1[0] + b1[0]) / 2, (a1[1] + b1[1]) / 2 - 30, "uzun yo‘l", anchor="middle"),
           C.text(a2[0] - 34, a2[1] + 10, "A", anchor="end", weight="bold"),
           C.text(b2[0] - 34, b2[1] + 10, "B", anchor="end", weight="bold"),
           C.text(18, H - 18, "qisqa yo‘l (tunel)")]
    ym = (a2[1] + b2[1]) / 2 + 10
    lab.append(C.leader([(250, H - 28), (a2[0] + 62, H - 28), (a2[0] + 62, ym), (a2[0] + 16, ym)]))
    top_low = max(P(p)[1] for p in pts[:4])
    fold_top = min(P(p)[1] for p in pts[4:] + [(xa, 0, r + 1.35)])
    ov = C.arrow(W * 0.3, top_low + 26, W * 0.3, top_low + 84, stroke=C.G3, sw=C.SW * 1.4, head=20)
    B.compose("rasm_2-4", "Rasm 2.4. Fazo-vaqt tuneli: buklangan qog‘oz", W, H, png, lab, overlay=ov)


# =========================================================================
# 3.2 — Shar Flatlandiyani kesib o'tadi
# =========================================================================
def rasm_3_2():
    W, H = 1120, 600
    B.reset(samples=96)
    B.size(W, H)
    kont = B.collection("kontur")
    R = 0.62
    gap = 2.4
    plane_m = B.mat("tekislik", C.mix(CREAM, GOLD, 0.18), rough=0.9, alpha=0.8, spec=0.05)
    sph_m = B.mat("shar", C.mix(BLUE, "#FFFFFF", 0.35), rough=0.25, alpha=0.38, spec=0.6)
    sec_m = B.mat("kesim", ACCENT, rough=0.6)
    hcs = [R, 0.78 * R, 0.0, -0.78 * R, -R]
    centers = []
    for k, hc in enumerate(hcs):
        x0 = (k - 2) * gap
        X, Y = np.meshgrid(np.linspace(x0 - 0.92, x0 + 0.92, 2), np.linspace(-0.72, 0.72, 2))
        B.grid_mesh("tekislik", X, Y, np.zeros_like(X), plane_m, smooth=False, coll=kont)
        B.sphere("shar", (x0, 0, hc), R, sph_m, coll=kont, seg=64)
        rc = math.sqrt(max(R * R - hc * hc, 0))
        if rc > 0.02:
            B.cylinder("kesim", (x0, 0, -0.004), (x0, 0, 0.004), rc, sec_m, seg=96)
        else:
            B.sphere("nuqta", (x0, 0, 0), 0.045, sec_m, seg=24)
        centers.append((x0, hc, rc))
    B.sun(direction=(0.4, 0.6, -1.0), strength=2.2, angle=15)
    B.world("#FFFFFF", 0.9)
    el = math.radians(24)
    cam = B.camera((-1.5, -20 * math.cos(el), 20 * math.sin(el)), (-0.2, 0, 0), ortho_scale=12)
    B.outlines(kont)
    pts = [(c[0] + sx * 0.92, sy * 0.72, 0) for c in centers for sx in (-1, 1) for sy in (-1, 1)]
    pts += [(c[0], 0, c[1] + R) for c in centers] + [(c[0], 0, c[1] - R) for c in centers]
    fit_camera(cam, pts, span=(0.97, 0.5), top=0.13)
    png = B.flatten(B.render("rasm_3-2"), B.OUT_RENDER + "/rasm_3-2.png")
    P = B.project
    ov, lab = [], []
    fw = W / 5
    p0 = P((0, 0, 0))
    p1 = P((R, 0, 0))
    px_per = abs(p1[0] - p0[0]) / R
    y_top = 495
    for k, (x0, hc, rc) in enumerate(centers):
        cx = P((x0, 0, 0))[0]
        if rc > 0.02:
            ov.append(C.circle(cx, y_top, rc * px_per, fill=ACCENT, stroke=C.mix(ACCENT, "#000000", 0.3), sw=C.SW))
        else:
            ov.append(C.circle(cx, y_top, 6.5, fill=ACCENT, stroke=C.mix(ACCENT, "#000000", 0.3), sw=C.SW))
        top = P((x0, 0, hc + R))
        ov.append(C.arrow(cx + 88, 112, cx + 88, 160, stroke=C.G3, sw=C.SW, head=14))
        lab.append(C.text(cx, 52, str(k + 1), anchor="middle", weight="bold", size=32))
        if k > 0:
            ov.append(C.line(fw * k, 30, fw * k, 575, stroke=C.G5, sw=C.SW))
    ov.append(C.line(20, 405, W - 20, 405, stroke=C.G4, sw=C.SW, extra=' stroke-dasharray="4 8"'))
    B.compose("rasm_3-2", "Rasm 3.2. Shar Flatlandiyani kesib o‘tadi", W, H, png, lab, overlay="\n".join(ov))


# =========================================================================
# 3.4 — Grafen panjarasi
# =========================================================================
def rasm_3_4():
    W, H = 540, 540
    B.reset(samples=64)
    B.size(W, H)
    b = 1.0
    ra = 0.24
    a1 = np.array([1.5 * b, math.sqrt(3) / 2 * b])
    a2 = np.array([1.5 * b, -math.sqrt(3) / 2 * b])
    atoms = {}
    for i in range(-10, 11):
        for j in range(-10, 11):
            o = i * a1 + j * a2
            atoms[("A", i, j)] = o
            atoms[("B", i, j)] = o + np.array([b, 0])
    Rv = 6.6

    def fade(p):
        d = np.hypot(p[0] * 0.9, p[1] * 1.15)
        return float(np.clip((Rv - d) / 1.6, 0, 1))
    levels = [0.15, 0.35, 0.55, 0.75, 1.0]
    atom_m = [B.mat(f"uglerod{k}", C.G3, rough=0.35, alpha=a, spec=0.5) for k, a in enumerate(levels)]
    bond_m = [B.mat(f"bog{k}", C.G4, rough=0.6, alpha=a) for k, a in enumerate(levels)]

    def lev(v):
        for k, a in enumerate(levels):
            if v <= a + 1e-9:
                return k
        return len(levels) - 1
    for (s_, i, j), p in atoms.items():
        fv = fade(p)
        if fv <= 0:
            continue
        B.sphere("atom", (p[0], p[1], 0), ra, atom_m[lev(fv)], seg=24)
        if s_ == "A":
            for nb in (("B", i, j), ("B", i - 1, j), ("B", i, j - 1)):
                if nb in atoms:
                    q = atoms[nb]
                    fq = min(fv, fade(q))
                    if max(fv, fade(q)) > 0:
                        B.cylinder("bog", (p[0], p[1], 0), (q[0], q[1], 0), 0.075,
                                   bond_m[lev(max(fq, 0.15))], seg=12)
    B.sun(direction=(0.3, 0.5, -1.0), strength=2.4, angle=12)
    B.world("#FFFFFF", 0.9)
    cam = B.camera((-2.5, -9.5, 6.0), (0.3, 0.6, 0), lens=40)
    pts = [(x, y, 0) for x in (-6.4, 6.4) for y in (-5.0, 5.0)]
    fit_camera(cam, pts, span=(1.12, 0.74), top=0.12)
    png = B.flatten(B.render("rasm_3-4"), B.OUT_RENDER + "/rasm_3-4.png")
    P = B.project
    ring = [atoms[k] for k in (("A", 0, 0), ("B", 0, 0), ("A", 1, 0), ("B", 1, -1), ("A", 1, -1), ("B", 0, -1))]
    rc_ = np.mean(ring, axis=0)
    small = P((rc_[0], rc_[1], 0))
    ov, lab = [], []
    mx, my, mr = 418, 112, 96
    ov.append(C.ellipse(small[0], small[1], 46, 30, fill="none", stroke=BLUE, sw=C.SW))
    for sgn in (-1, 1):
        ang = math.atan2(my - small[1], mx - small[0]) + sgn * math.pi / 2
        ov.append(C.line(small[0] + 42 * math.cos(ang), small[1] + 28 * math.sin(ang),
                         mx + mr * math.cos(ang), my + mr * math.sin(ang), stroke=BLUE, sw=C.SW * 0.8))
    ov.append(C.circle(mx, my, mr, fill="#FFFFFF", stroke=BLUE, sw=C.SW * 1.4))
    hr = 46
    hexp = [(mx + hr * math.cos(math.radians(60 * k)), my + hr * math.sin(math.radians(60 * k))) for k in range(6)]
    for k in range(6):
        p, q = hexp[k], hexp[(k + 1) % 6]
        ov.append(C.line(p[0], p[1], q[0], q[1], stroke=C.G3, sw=9))
        out = (mx + (hr + 28) * math.cos(math.radians(60 * k)), my + (hr + 28) * math.sin(math.radians(60 * k)))
        ov.append(C.line(p[0], p[1], out[0], out[1], stroke=C.G4, sw=9, extra=' stroke-linecap="butt"'))
    for p in hexp:
        ov.append(C.circle(p[0], p[1], 15, fill="url(#atomG)", stroke=C.G1, sw=C.SW * 0.7))
    yr = 478
    xs_ = [40 + 34 * k for k in range(9)]
    ov.append(C.line(xs_[0] - 30, yr, xs_[-1] + 30, yr, stroke=C.G4, sw=6.5))
    for x in xs_:
        ov.append(C.circle(x, yr, 12, fill="url(#atomG)", stroke=C.G1, sw=C.SW * 0.6))
    xa = xs_[-1] + 52
    ov.append(C.line(xs_[-1], yr - 12, xa + 10, yr - 12, stroke=C.G1, sw=C.SW * 0.7))
    ov.append(C.line(xs_[-1], yr + 12, xa + 10, yr + 12, stroke=C.G1, sw=C.SW * 0.7))
    lab.append(C.arrow(xa, yr - 42, xa, yr - 12, stroke=BLUE, sw=C.SW, head=11))
    lab.append(C.arrow(xa, yr + 42, xa, yr + 12, stroke=BLUE, sw=C.SW, head=11))
    lab.append(C.text_lines(xa + 22, yr - 6, ["bir atom", "qalinlikda"]))
    p0 = hexp[3]
    lab.append(C.text(18, 40, "uglerod atomi"))
    lab.append(C.leader([(100, 52), (100, p0[1]), (p0[0] - 15, p0[1])]))
    defs = f"""<radialGradient id="atomG" cx="0.35" cy="0.32" r="0.75">
  <stop offset="0" stop-color="{C.mix(C.G4, '#FFFFFF', 0.6)}"/><stop offset="1" stop-color="{C.G2}"/></radialGradient>"""
    B.compose("rasm_3-4", "Rasm 3.4. Grafen panjarasi", W, H, png, lab, defs=defs, overlay="\n".join(ov))


# =========================================================================
# 4.1 — Nuqtadan tesseraktgacha
# =========================================================================
def rasm_4_1():
    W, H = 1120, 500
    B.reset(samples=64)
    B.size(W, H)
    kont = B.collection("kontur")
    blue_m = B.mat("kok_qirra", BLUE, rough=0.5)
    gold_m = B.mat("oltin_qirra", GOLD, rough=0.4)
    vert_m = B.mat("uch", C.mix(BLUE, "#000000", 0.15), rough=0.4)
    rb, rg, rv = 0.035, 0.055, 0.085
    s = 0.62
    xs = [-6.2, -3.6, -0.7, 2.3, 5.6]

    def edge(p, q, gold=False):
        B.cylinder("qirra", p, q, rg if gold else rb, gold_m if gold else blue_m, seg=16)

    def verts(V):
        for v in V:
            B.sphere("uch", v, rv, vert_m, seg=24)
    allp = []
    # 0D
    verts([(xs[0], 0, 0)])
    allp.append((xs[0], 0, 0))
    # 1D
    a, b_ = (xs[1] - s, 0, 0), (xs[1] + s, 0, 0)
    edge(a, b_, True); verts([a, b_]); allp += [a, b_]
    # 2D (x–z tekisligida)
    c = xs[2]
    sq = [(c - s, 0, -s), (c + s, 0, -s), (c + s, 0, s), (c - s, 0, s)]
    edge(sq[0], sq[1]); edge(sq[3], sq[2]); edge(sq[0], sq[3], True); edge(sq[1], sq[2], True)
    verts(sq); allp += sq
    # 3D
    c = xs[3]
    fr = [(c - s, -s, -s), (c + s, -s, -s), (c + s, -s, s), (c - s, -s, s)]
    bk = [(p[0], s, p[2]) for p in fr]
    for P_ in (fr, bk):
        for i in range(4):
            edge(P_[i], P_[(i + 1) % 4])
    for i in range(4):
        edge(fr[i], bk[i], True)
    verts(fr + bk); allp += fr + bk
    # 4D: kub ichidagi kub
    c = xs[4]
    S2 = 0.78
    Vo = [(c + sx * S2, sy * S2, sz * S2) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    k = 0.42
    Vi = [(c + (v[0] - c) * k, v[1] * k, v[2] * k) for v in Vo]
    E = [(i, j) for i in range(8) for j in range(i + 1, 8)
         if sum(1 for a_, b2 in zip(Vo[i], Vo[j]) if abs(a_ - b2) > 1e-9) == 1]
    assert len(E) == 12
    for V in (Vo, Vi):
        for i, j in E:
            edge(V[i], V[j])
    for i in range(8):
        edge(Vi[i], Vo[i], True)
    assert len(Vo + Vi) == 16 and 2 * len(E) + 8 == 32
    verts(Vo + Vi); allp += Vo
    B.sun(direction=(0.5, 0.7, -0.8), strength=2.2, angle=15)
    B.world("#FFFFFF", 0.9)
    cam = B.camera((-3.0, -14, 5.2), (0, 0, 0), ortho_scale=14)
    fit_camera(cam, allp, span=(0.86, 0.5), top=0.18)
    png = B.flatten(B.render("rasm_4-1"), B.OUT_RENDER + "/rasm_4-1.png")
    P = B.project
    lab, ov = [], []
    names = ["0D", "1D", "2D", "3D", "4D"]
    counts = [1, 2, 4, 8, 16]
    cxs = [P((x, 0, 0))[0] for x in xs]
    yc = P((0, 0, 0))[1]
    ext = [0, s, s, s * 1.25, S2 * 1.3]
    for i in range(4):
        x1 = P((xs[i] + ext[i], 0, 0))[0] + 24
        x2 = P((xs[i + 1] - ext[i + 1], 0, 0))[0] - 24
        ov.append(C.arrow(x1, yc, x2, yc, stroke=C.G3, sw=C.SW, head=16))
    for x, n_, cnt in zip(cxs, names, counts):
        lab.append(C.text(x, 410, n_, anchor="middle", weight="bold", size=32))
        lab.append(C.text(x, 452, f"{cnt} ta uch", anchor="middle"))
    B.compose("rasm_4-1", "Rasm 4.1. Nuqtadan tesseraktgacha", W, H, png, lab, overlay="\n".join(ov))


# =========================================================================
# 4.3 — Kalabi–Yau fazosi
# =========================================================================
def rasm_4_3():
    import bpy
    W = H = 540
    B.reset(samples=96)
    B.size(W, H)
    n = 5
    alpha = math.pi / 4

    def patches(m):
        xs = np.linspace(-1, 1, m)
        ys = np.linspace(0, math.pi / 2, m)
        X, Y = np.meshgrid(xs, ys)
        Z = X + 1j * Y
        out = []
        for k1 in range(n):
            for k2 in range(n):
                z1 = np.exp(2j * math.pi * k1 / n) * np.cosh(Z) ** (2 / n)
                z2 = np.exp(2j * math.pi * k2 / n) * np.sinh(Z) ** (2 / n)
                out.append((k1, k2, z1.real, z2.real,
                            math.cos(alpha) * z1.imag + math.sin(alpha) * z2.imag))
        return out
    surf_m = [B.mat(f"kalabi{k}", C.mix(BLUE, GOLD, 0.2 + 0.6 * k / 4), rough=0.35, alpha=0.72, spec=0.5)
              for k in range(5)]
    wire_m = B.flat_mat("tor", BLUE)
    for k1, k2, X, Y, Z in patches(28):
        B.grid_mesh("yuza", X, Y, Z, surf_m[(k1 + k2) % 5], smooth=True)
    for k1, k2, X, Y, Z in patches(11):
        ob = B.grid_mesh("tor", X, Y, Z, wire_m, smooth=False)
        md = ob.modifiers.new("simlar", "WIREFRAME")
        md.thickness = 0.006
        md.use_replace = True
    B.sun(direction=(-0.4, 0.6, -1.0), strength=2.0, angle=20)
    B.world("#FFFFFF", 1.0)
    from mathutils import Matrix
    zc = Vector((-0.544, -0.469, 0.696)).normalized()
    yc = Vector((-0.289, 0.883, 0.370))
    yc = (yc - zc * yc.dot(zc)).normalized()
    xc = yc.cross(zc)
    cam = B.camera(tuple(zc * 20), (0, 0, 0), ortho_scale=3.2)
    M = Matrix(((xc.x, yc.x, zc.x), (xc.y, yc.y, zc.y), (xc.z, yc.z, zc.z))).to_4x4()
    M.translation = zc * 20
    cam.matrix_world = M
    bpy.context.view_layer.update()
    ms = [o for o in bpy.data.objects if o.type == "MESH"]
    pts = [o.matrix_world @ v.co for o in ms[:25] for v in list(o.data.vertices)[::7]]
    fit_camera(cam, pts, span=(0.96, 0.96), top=0.02)
    png = B.flatten(B.render("rasm_4-3"), B.OUT_RENDER + "/rasm_4-3.png")
    B.compose("rasm_4-3", "Rasm 4.3. Kalabi–Yau fazosi", W, H, png, [],
              desc="Kvintik Kalabi–Yau kesimi tenglamalardan hisoblab, Blender’da yaratildi.")


# =========================================================================
# 4.4 — Bran-olamlar
# =========================================================================
def rasm_4_4():
    W, H = 1120, 700
    B.reset(samples=96, transparent=False)
    B.size(W, H)
    rng = np.random.default_rng(44)
    B.world(C.NIGHT, 1.0)

    def zf(x, y, base, ph):
        return base + 0.28 * np.sin(0.55 * x + 0.8 * y + ph) + 0.15 * np.sin(1.1 * y - 0.4 * x + 1.3 * ph)
    X, Y = np.meshgrid(np.linspace(-7, 7, 160), np.linspace(-3, 3, 70))
    up_m = B.mat("qoshni_bran", C.mix(BLUE, CREAM, 0.30), rough=0.5, alpha=0.72, emit=0.25)
    lo_m = B.mat("bizning_bran", C.mix(BLUE, CREAM, 0.22), rough=0.5, alpha=0.8, emit=0.25)
    grid_m = B.flat_mat("bran_tor", C.mix(CREAM, BLUE, 0.35), 0.8)
    base_u, base_l, ph_u, ph_l = 3.4, -1.7, 1.3, 0.2
    B.grid_mesh("qoshni_bran", X, Y, zf(X, Y, base_u, ph_u), up_m)
    B.grid_mesh("bizning_bran", X, Y, zf(X, Y, base_l, ph_l), lo_m)
    for base, ph in ((base_u, ph_u), (base_l, ph_l)):
        for v in np.linspace(-3, 3, 7):
            xs = np.linspace(-7, 7, 200)
            B.tube("bran_chiziq", np.stack([xs, np.full_like(xs, v), zf(xs, v, base, ph) + 0.01], 1), 0.012, grid_m)
        for v in np.linspace(-7, 7, 15):
            ys = np.linspace(-3, 3, 80)
            B.tube("bran_chiziq", np.stack([np.full_like(ys, v), ys, zf(v, ys, base, ph) + 0.01], 1), 0.012, grid_m)
    # galaktikalar va yulduzlar (bizning bran)
    gal_m = B.mat("galaktika", C.mix(GOLD, CREAM, 0.6), emit=2.2)
    star_m = B.mat("yulduz", CREAM, emit=4.0)
    for _ in range(16):
        x, y = rng.uniform(-6.3, 6.3), rng.uniform(-2.6, 2.6)
        ob = B.sphere("galaktika", (x, y, float(zf(x, y, base_l, ph_l)) + 0.03), 0.13, gal_m, seg=24)
        ob.scale = (1, rng.uniform(0.45, 0.8), 0.15)
        ob.rotation_euler = (0, 0, rng.uniform(0, math.pi))
    for _ in range(140):
        x, y = rng.uniform(-6.8, 6.8), rng.uniform(-2.9, 2.9)
        B.sphere("yulduz", (x, y, float(zf(x, y, base_l, ph_l)) + 0.02), rng.uniform(0.018, 0.035), star_m, seg=8)
    # balkdagi xira yulduzlar
    far_m = B.mat("uzoq", CREAM, emit=1.2)
    for _ in range(80):
        B.sphere("fon", (rng.uniform(-12, 12), rng.uniform(4, 9), rng.uniform(-5, 7)), 0.03, far_m, seg=8)
    # ochiq torlar
    str_m = B.mat("tor", ACCENT, rough=0.5, emit=0.8)
    opens = []

    def open_string(x, y, base, ph, du=0.35, h=0.45, down=False):
        t = np.linspace(0, 1, 30)
        xx = x - du + 2 * du * t
        yy = y + 0.06 * np.sin(math.pi * t)
        zz = zf(xx, yy, base, ph) + (-1 if down else 1) * h * np.sin(math.pi * t) + 0.02
        B.tube("ochiq_tor", np.stack([xx, yy, zz], 1), 0.035, str_m)
        for xe, ye in ((xx[0], yy[0]), (xx[-1], yy[-1])):
            B.sphere("tor_uchi", (xe, ye, float(zf(xe, ye, base, ph)) + 0.02), 0.06, str_m, seg=16)
        return (x, y, float(zf(x, y, base, ph)) + (-1 if down else 1) * h)
    for (x, y) in [(-4.2, -1.0), (0.2, 1.4), (3.6, -0.6), (2.0, 2.0), (-1.6, -1.8), (4.8, -2.2)]:
        opens.append(open_string(x, y, base_l, ph_l))
    for (x, y) in [(-3.5, 0.6), (3.0, 1.0)]:
        open_string(x, y, base_u, ph_u, down=True)
    # yopiq tor (graviton) — branlar orasida
    gc = np.array([2.4, -1.2, 0.85])
    th = np.linspace(0, 2 * math.pi, 240)
    rr = 0.36 + 0.05 * np.sin(7 * th)
    loop = np.stack([gc[0] + rr * np.cos(th), gc[1] + 0.3 * rr * np.sin(th), gc[2] + rr * np.sin(th)], 1)
    B.tube("yopiq_tor", loop, 0.035, str_m, cyclic=True)
    cam = B.camera((-1.0, -16, 8.6), (0, 0, 0.8), lens=40)
    pts = [(x, y, float(zf(x, y, b_, p_))) for x in (-7, 7) for y in (-3, 3) for b_, p_ in ((base_u, ph_u), (base_l, ph_l))]
    fit_camera(cam, pts, span=(0.93, 0.84), top=0.08)
    png = B.flatten(B.render("rasm_4-4"), B.OUT_RENDER + "/rasm_4-4.png")
    P = B.project
    c = CREAM
    lab = []
    pu = P((-5.6, 1.5, float(zf(-5.6, 1.5, base_u, ph_u))))
    lab.append(C.text(20, 46, "qo‘shni bran", fill=c))
    lab.append(C.leader([(232, 38), (pu[0], 38), pu], stroke=c))
    yu_low = max(P((x, -3, float(zf(x, -3, base_u, ph_u))))[1] for x in np.linspace(-7, -2, 20))
    yl_high = min(P((x, 3, float(zf(x, 3, base_l, ph_l))))[1] for x in np.linspace(-7, -2, 20))
    lab.append(C.text(20, (yu_low + yl_high) / 2 + 10, "balk (ko‘p o‘lchamli fazo)", fill=c))
    pl = P((-5.2, -2.4, float(zf(-5.2, -2.4, base_l, ph_l))))
    lab.append(C.text(20, H - 20, "bizning bran-olamimiz", fill=c))
    lab.append(C.leader([(345, H - 30), (max(pl[0] + 40, 360), H - 30), (max(pl[0] + 40, 360), pl[1])], stroke=c))
    g = P(tuple(gc + np.array([0.36, 0, 0])))
    lab.append(C.text(W - 20, g[1] + 10, "yopiq tor (graviton)", anchor="end", fill=c))
    lab.append(C.leader([(W - 292, g[1]), (g[0] + 4, g[1])], stroke=c))
    o = P(max([op for op in opens if op[0] > 0], key=lambda op: P(op)[1]))
    lab.append(C.text(W - 20, H - 20, "ochiq tor (modda, yorug‘lik)", anchor="end", fill=c))
    lab.append(C.leader([(W - 170, H - 50), (W - 170, o[1] + 8), (o[0] + 6, o[1] + 4)], stroke=c))
    B.compose("rasm_4-4", "Rasm 4.4. Bran-olamlar", W, H, png, lab)


# =========================================================================
# 6.3 — Abadiy inflyatsiya
# =========================================================================
def rasm_6_3():
    W, H = 1120, 600
    B.reset(samples=96, transparent=False)
    B.size(W, H)
    rng = np.random.default_rng(63)
    B.world(C.mix(C.NIGHT, BLUE, 0.25), 1.0)
    hues = [GOLD, C.mix(BLUE, "#FFFFFF", 0.55), ACCENT, C.mix(ACCENT, BLUE, 0.45), C.mix(GOLD, CREAM, 0.6),
            C.mix(C.G4, BLUE, 0.2), C.mix("#6F9A8A", BLUE, 0.1)]
    bubbles = [(250, 300, 128), (640, 215, 104), (900, 380, 112), (455, 450, 66), (1030, 135, 56),
               (95, 110, 50), (820, 78, 34), (360, 100, 46), (120, 500, 44)]
    reserved = [(560, 470, 800, 545), (W - 290, H - 70, W, H)]
    tries = 0
    while len(bubbles) < 34 and tries < 20000:
        tries += 1
        r = float(rng.choice([7, 9, 12, 15, 20, 26]))
        x, y = rng.uniform(r + 8, W - r - 8), rng.uniform(r + 8, H - r - 8)
        if any(math.hypot(x - bx, y - by) < r + br + 22 for bx, by, br in bubbles):
            continue
        if any(x0 - r < x < x1 + r and y0 - r < y < y1 + r for x0, y0, x1, y1 in reserved):
            continue
        bubbles.append((x, y, r))
    # dunyo: 1 birlik = 100 kanvas birligi; z = 0 tekisligida, ortografik kamera tepadan
    sc_ = 0.01
    mats = [B.mat(f"pufak{i}", h, rough=0.15, alpha=0.55, spec=0.8, emit=0.35) for i, h in enumerate(hues)]
    gal_m = B.mat("galaktika", "#FFF6E2", emit=4.0)
    for i, (x, y, r) in enumerate(bubbles):
        cx, cy, R = x * sc_, -y * sc_, r * sc_
        B.sphere("pufak", (cx, cy, 0), R, mats[i % len(hues)], seg=48)
        if r >= 40:
            for _ in range(int(r / 9)):
                a = rng.uniform(0, 2 * math.pi)
                d = rng.uniform(0, R * 0.7)
                ob = B.sphere("galaktika", (cx + d * math.cos(a), cy + d * math.sin(a), rng.uniform(-R * 0.3, R * 0.3)),
                              0.07 * min(1, r / 70), gal_m, seg=16)
                ob.scale = (1, 0.45, 0.2)
                ob.rotation_euler = (rng.uniform(0, 1), 0, rng.uniform(0, math.pi))
        elif r <= 12:
            B.sphere("yadro", (cx, cy, 0), R * 0.35, gal_m, seg=12)
    B.sun(direction=(0.4, -0.5, -1.0), strength=1.8, angle=20)
    cam = B.camera((W * sc_ / 2, -H * sc_ / 2, 30), (W * sc_ / 2, -H * sc_ / 2, 0), ortho_scale=W * sc_)
    png = B.flatten(B.render("rasm_6-3"), B.OUT_RENDER + "/rasm_6-3.png")
    ov = []
    placed_ar = []
    for _ in range(3000):
        x, y = rng.uniform(40, W - 40), rng.uniform(40, H - 40)
        if any(math.hypot(x - bx, y - by) < br + 34 for bx, by, br in bubbles):
            continue
        if any(math.hypot(x - ax, y - ay) < 78 for ax, ay in placed_ar):
            continue
        if any(x0 - 10 < x < x1 + 10 and y0 - 10 < y < y1 + 10 for x0, y0, x1, y1 in reserved):
            continue
        placed_ar.append((x, y))
        ang = math.atan2(y - H / 2, x - W / 2) + rng.uniform(-0.25, 0.25)
        ov.append(C.arrow(x, y, x + 24 * math.cos(ang), y + 24 * math.sin(ang),
                          stroke=C.mix(CREAM, C.NIGHT, 0.4), sw=C.SW * 0.8, head=10))
    ox, oy, orr = bubbles[3]
    c = CREAM
    lab = [C.text(580, 522, "bizning koinot", fill=c),
           C.arrow(574, 508, ox + orr * 0.74 + 4, oy + orr * 0.5 + 4, stroke=c, sw=C.SW, head=15),
           C.text(W - 24, H - 24, "shishayotgan fazo", anchor="end", fill=c)]
    B.compose("rasm_6-3", "Rasm 6.3. Abadiy inflyatsiya", W, H, png, lab, overlay="\n".join(ov))


# =========================================================================
# 6.4 — Qora tuynuk sirtidagi axborot
# =========================================================================
def rasm_6_4():
    from mathutils import Matrix
    W = H = 540
    B.reset(samples=96)
    B.size(W, H)
    rng = np.random.default_rng(64)
    R = 2.0
    B.sphere("qora_tuynuk", (0, 0, 0), R, B.mat("qora", "#050505", rough=0.25, spec=0.6), seg=96)
    line_m = B.mat("katak", GOLD, rough=0.4, emit=0.6)
    digit_m = B.mat("bit", CREAM, emit=1.5)
    import bpy as _b
    font = _b.data.fonts.load("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")
    lats = np.arange(-90, 91, 10)
    rl = R * 1.002

    def P3(lat, lon):
        return np.stack([rl * np.cos(lat) * np.cos(lon), rl * np.cos(lat) * np.sin(lon), rl * np.sin(lat)], -1)
    cells = []
    for i in range(len(lats) - 1):
        la0, la1 = math.radians(lats[i]), math.radians(lats[i + 1])
        lc = (la0 + la1) / 2
        nseg = max(3, int(round(36 * math.cos(lc))))
        off = rng.uniform(0, 2 * math.pi / nseg)
        if i > 0:
            lon = np.linspace(0, 2 * math.pi, 361)
            B.tube("kenglik", P3(np.full_like(lon, la0), lon), 0.0075, line_m, cyclic=True)
        for k in range(nseg):
            lo = off + 2 * math.pi * k / nseg
            B.tube("meridian", P3(np.linspace(la0, la1, 10), np.full(10, lo)), 0.0075, line_m)
            cells.append((lc, lo + math.pi / nseg))
    # kamera yo'nalishi
    cam_dir = np.array([0.35, -0.85, 0.42])
    cam_dir /= np.linalg.norm(cam_dir)
    best = None
    for lc, lo in cells:
        p = P3(np.array(lc), np.array(lo))
        nrm = p / np.linalg.norm(p)
        if nrm @ cam_dir < 0.3 or rng.random() > 0.55:
            continue
        east = np.array([-math.sin(lo), math.cos(lo), 0.0])
        north = np.cross(nrm, east)
        M = Matrix(((east[0], north[0], nrm[0]), (east[1], north[1], nrm[1]), (east[2], north[2], nrm[2])))
        tob = B.text3d("bit", str(int(rng.integers(0, 2))), tuple(p * 1.003), M, 0.17, digit_m)
        tob.data.font = font
    for lc, lo in cells:
        p = P3(np.array(lc), np.array(lo))
        nrm = p / np.linalg.norm(p)
        if nrm @ cam_dir > 0.62 and lc > math.radians(15):
            if best is None or (nrm[0] > best[1][0]):
                best = (lc, nrm * R)
    B.sun(direction=(0.6, 0.4, -0.7), strength=3.0, angle=6)
    B.world("#FFFFFF", 0.9)
    cam = B.camera(tuple(cam_dir * 20), (0, 0, 0), ortho_scale=5)
    import bpy
    bpy.context.view_layer.update()
    pts = [(R * math.cos(t), R * math.sin(t), 0) for t in np.linspace(0, 2 * math.pi, 24)]
    pts += [(0, 0, R), (0, 0, -R)]
    fit_camera(cam, pts, span=(0.68, 0.68), top=0.27)
    cam.data.shift_x += 0.1
    bpy.context.view_layer.update()
    png = B.flatten(B.render("rasm_6-4"), B.OUT_RENDER + "/rasm_6-4.png")
    P = B.project
    hx, hy = P(tuple(best[1]))
    ov, lab = [], []
    mx, my, mr = 448, 98, 74
    for sgn in (-1, 1):
        ang = math.atan2(my - hy, mx - hx) + sgn * math.pi / 2
        ov.append(C.line(hx + 13 * math.cos(ang), hy + 13 * math.sin(ang), mx + mr * math.cos(ang),
                         my + mr * math.sin(ang), stroke=BLUE, sw=C.SW * 0.8))
    ov.append(C.circle(hx, hy, 13, fill="none", stroke=ACCENT, sw=C.SW * 1.2))
    ov.append(C.circle(mx, my, mr, fill="#FFFFFF", stroke=BLUE, sw=C.SW * 1.4))
    ov.append(f'<rect x="{mx - 40}" y="{my - 40}" width="80" height="80" fill="#0B0B0B" stroke="{GOLD}" stroke-width="{C.SW * 1.4}"/>')
    ov.append(f'<text x="{mx}" y="{my + 22}" font-family="{C.FONT}" font-size="62" text-anchor="middle" fill="{CREAM}">1</text>')
    lab.append(C.text(mx - mr - 14, 76, "har katakcha ≈ 1 bit", anchor="end"))
    c0 = P((0, 0, 0))
    edge = P((0, 0, 0))
    lab.append(C.text(16, H - 14, "voqealar gorizonti"))
    # shar chap chetidagi nuqta
    rad = abs(P(tuple(np.cross(cam_dir, [0, 0, 1]) / np.linalg.norm(np.cross(cam_dir, [0, 0, 1])) * R))[0] - c0[0])
    yy = c0[1] + rad * 0.45
    xx = c0[0] - math.sqrt(max(rad * rad - (yy - c0[1]) ** 2, 0)) + 6
    lab.append(C.leader([(22, H - 42), (22, yy), (xx, yy)]))
    B.compose("rasm_6-4", "Rasm 6.4. Qora tuynuk sirtidagi axborot", W, H, png, lab, overlay="\n".join(ov))


if __name__ == "__main__":
    for w in sys.argv[1:]:
        globals()["rasm_" + w.replace("-", "_")]()
