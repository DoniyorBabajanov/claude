"""III bob — Bir o'lchamli va yassi olamlar: rasmlar 3.1–3.4"""
import math
import sys
import numpy as np
from scipy.spatial import ConvexHull
from common import *


# =========================================================================
# Rasm 3.1 — Flatlandiya aholisi
# =========================================================================
def reg_poly(cx, cy, r, n, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 360 * k / n)),
             cy + r * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)]


def face(cx, cy, s=1.0, dark=False):
    """Yassi yuz: bitta ko'z va tabassum (qalinliksiz, soyasiz)."""
    ink = CREAM if dark else BLUE
    o = [circle(cx - 4 * s, cy - 8 * s, 9 * s, fill=WHITE, stroke=ink, sw=SW * 0.8),
         circle(cx - 2 * s, cy - 7 * s, 4 * s, fill=G1, stroke=None, sw=0),
         path(f"M{f(cx - 14 * s)},{f(cy + 10 * s)} Q{f(cx)},{f(cy + 22 * s)} "
              f"{f(cx + 14 * s)},{f(cy + 8 * s)}", stroke=ink, sw=SW)]
    return "\n".join(o)


def rasm_3_1():
    W, H = 1120, 700
    art, L = [], []
    # yuqori panel: tekislik tepadan
    art.append(f'<rect x="30" y="62" width="1060" height="400" fill="{CREAM}" '
               f'stroke="{BLUE}" stroke-width="{SW}"/>')
    figs = []
    tri = reg_poly(170, 285, 82, 3, -90)
    figs.append(("uchburchak", tri, GOLD, (170, 297)))
    sq = reg_poly(360, 215, 72, 4, -45)
    figs.append(("kvadrat", sq, mix(BLUE, CREAM, 0.15), (360, 215)))
    pen = reg_poly(815, 330, 78, 5, -90)
    figs.append(("beshburchak", pen, G3, (815, 335)))
    figs.append(("doira", ("circle", 975, 195, 62), ACCENT, (975, 195)))
    # uy: tepadan ochiq ko'pburchak (to'g'ri to'rtburchak, eshik joyi bo'sh)
    hx0, hx1, hy0, hy1 = 498, 690, 140, 345
    house = [(hx0, hy0), (hx1, hy0), (hx1, hy1), (hx0, hy1)]
    hx_min, hx_max = hx0, hx1
    dm, gap = 594, 36
    wall = [(dm + gap, hy1), (hx1, hy1), (hx1, hy0), (hx0, hy0), (hx0, hy1), (dm - gap, hy1)]
    art.append(polygon(house, fill=mix(CREAM, WHITE, 0.55), stroke=None, sw=0))
    art.append(polyline(wall, stroke=G1, sw=SW * 3.2, extra=' stroke-linecap="butt"'))
    art.append(line(hx0, 245, 560, 245, stroke=G1, sw=SW * 2.2, extra=' stroke-linecap="butt"'))
    for name, shp, col, fc in figs:
        if shp[0] == "circle":
            _, cx, cy, r = shp
            art.append(circle(cx, cy, r, fill=col, stroke=BLUE, sw=SW))
        else:
            art.append(polygon(shp, fill=col, stroke=BLUE, sw=SW))
        art.append(face(fc[0], fc[1], 1.25, dark=(col in (ACCENT,) or col.startswith("#2") or col == mix(BLUE, CREAM, 0.15))))
    L.append(text(30, 46, "tepadan ko‘rinish (biz)"))

    # pastki panel: tekislik sathidan
    y_line = 585
    art.append(line(30, y_line, 1090, y_line, stroke=G4, sw=SW))
    segs = []
    for name, shp, col, fc in figs:
        if shp[0] == "circle":
            _, cx, cy, r = shp
            xmin, xmax = cx - r, cx + r
            ylow = cy
        else:
            xs = [p[0] for p in shp]
            xmin, xmax = min(xs), max(xs)
            ylow = None
        segs.append((xmin, xmax, col, shp))
    segs.append((hx_min, hx_max, G1, house))
    for xmin, xmax, col, shp in segs:
        # proyeksiya chiziqlari
        if shp[0] == "circle":
            _, cx, cy, r = shp
            pts_ = [(cx - r, cy), (cx + r, cy)]
        else:
            pa = min(shp, key=lambda p: p[0])
            pb = max(shp, key=lambda p: p[0])
            pts_ = [pa, pb]
        for (px, py) in pts_:
            art.append(line(px, py, px, y_line - 12, stroke=G3, sw=SW * 0.7,
                            extra=' stroke-dasharray="6 8"'))
        art.append(f'<rect x="{f(xmin)}" y="{f(y_line - 7)}" width="{f(xmax - xmin)}" '
                   f'height="14" fill="{col}" stroke="{BLUE}" stroke-width="{SW * 0.8}"/>')
    L.append(text(30, 640, "flatlandiyalik ko‘zi bilan"))
    return svg_doc(W, H, "Rasm 3.1. Flatlandiya aholisi", "\n".join(art), "\n".join(L))


# =========================================================================
# Rasm 3.2 — Shar Flatlandiyani kesib o'tadi
# =========================================================================
def rasm_3_2():
    W, H = 1120, 600
    phi = math.radians(24)
    az = math.radians(28)
    R = 66
    plane_w, plane_d = 80, 58
    fib = 2400
    i = np.arange(fib) + 0.5
    zz = 1 - 2 * i / fib
    rr = np.sqrt(1 - zz ** 2)
    aa = np.pi * (1 + 5 ** 0.5) * i
    sph = np.stack([rr * np.cos(aa), rr * np.sin(aa), zz], 1)

    def proj(P, ox, oy):
        P = np.atleast_2d(P)
        x1 = P[:, 0] * math.cos(az) - P[:, 1] * math.sin(az)
        y1 = P[:, 0] * math.sin(az) + P[:, 1] * math.cos(az)
        X = ox + x1
        Y = oy - P[:, 2] * math.cos(phi) - y1 * math.sin(phi)
        return np.stack([X, Y], 1)

    hcs = [R, 0.78 * R, 0.0, -0.78 * R, -R]
    art, L = [], []
    fw = W / 5
    y_plane = 235
    y_top = 488
    for k, hc in enumerate(hcs):
        ox = fw * (k + 0.5)
        corners = np.array([[-plane_w, -plane_d, 0], [plane_w, -plane_d, 0],
                            [plane_w, plane_d, 0], [-plane_w, plane_d, 0]])
        cp = [tuple(p) for p in proj(corners, ox, y_plane)]
        P = sph * R + np.array([0, 0, hc])
        upper = P[P[:, 2] > 0.0]
        lower = P[P[:, 2] < 0.0]
        rc = math.sqrt(max(R * R - hc * hc, 0))
        th = np.linspace(0, 2 * np.pi, 120, endpoint=False)
        sec = np.stack([rc * np.cos(th), rc * np.sin(th), np.zeros_like(th)], 1)
        g = []
        if len(lower) > 3:
            pl = proj(np.vstack([lower, sec]) if rc > 1 else lower, ox, y_plane)
            hull = ConvexHull(pl)
            poly = [tuple(pl[v]) for v in hull.vertices]
            g.append(polygon(poly, fill=BLUE, stroke=BLUE, sw=SW,
                             extra=' fill-opacity="0.28" stroke-dasharray="7 6"'))
        g.append(polygon(cp, fill=CREAM, stroke=BLUE, sw=SW, extra=' fill-opacity="0.82"'))
        # kesim
        cc = proj(np.array([[0, 0, 0]]), ox, y_plane)[0]
        if rc > 2:
            g.append(ellipse(cc[0], cc[1], rc, rc * math.sin(phi), fill=ACCENT,
                             stroke=mix(ACCENT, "#000000", 0.3), sw=SW))
        else:
            g.append(circle(cc[0], cc[1], 6.5, fill=ACCENT, stroke=mix(ACCENT, "#000000", 0.3), sw=SW))
        if len(upper) > 3:
            pu = proj(np.vstack([upper, sec]) if rc > 1 else upper, ox, y_plane)
            hull = ConvexHull(pu)
            poly = [tuple(pu[v]) for v in hull.vertices]
            g.append(polygon(poly, fill="url(#sharGrad)", stroke=BLUE, sw=SW,
                             extra=' fill-opacity="0.55"'))
        # harakat strelkasi
        sc_ = proj(np.array([[0, 0, hc]]), ox, y_plane)[0]
        g.append(arrow(ox + 86, 112, ox + 86, 160, stroke=G3, sw=SW, head=14))
        art.append(f'<g id="kadr{k + 1}">' + "\n".join(g) + '</g>')
        # tepadan ko'rinish
        if rc > 2:
            art.append(circle(ox, y_top, rc, fill=ACCENT, stroke=mix(ACCENT, "#000000", 0.3), sw=SW))
        else:
            art.append(circle(ox, y_top, 6.5, fill=ACCENT, stroke=mix(ACCENT, "#000000", 0.3), sw=SW))
        L.append(text(ox, 52, str(k + 1), anchor="middle", weight="bold", size=32))
        if k > 0:
            art.append(line(fw * k, 30, fw * k, 575, stroke=G5, sw=SW))
    art.append(line(20, 398, W - 20, 398, stroke=G4, sw=SW, extra=' stroke-dasharray="4 8"'))
    defs = f"""<radialGradient id="sharGrad" cx="0.38" cy="0.32" r="0.8">
  <stop offset="0" stop-color="{mix(BLUE, WHITE, 0.75)}"/><stop offset="1" stop-color="{mix(BLUE, WHITE, 0.15)}"/></radialGradient>"""
    return svg_doc(W, H, "Rasm 3.2. Shar Flatlandiyani kesib o‘tadi", "\n".join(art),
                   "\n".join(L), defs)


# =========================================================================
# Rasm 3.3 — Ikki o'lchamli Boze–Eynshteyn kondensatidagi uyurmalar
# =========================================================================
def rasm_3_3():
    W = H = 540
    cx, cy = 270, 282
    Rc = 205
    art, L = [], []
    art.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{NIGHT}"/>')
    art.append(circle(cx, cy, Rc, fill="url(#bulut)", stroke=None, sw=0))
    a = 80
    # uchburchak markazli uchburchakli panjara: 12 ta o'zak
    pts_ = []
    for i in range(-4, 5):
        for j in range(-4, 5):
            x = a * (i + 0.5 * j)
            y = a * (math.sqrt(3) / 2) * j
            pts_.append((x, y))
    c0 = (a * 0.5, a * math.sqrt(3) / 6)
    pts_ = [(x - c0[0], y - c0[1]) for x, y in pts_]
    pts_ = sorted(pts_, key=lambda p: math.hypot(*p))[:12]
    rot = math.radians(8)
    cores = [(cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot))
             for x, y in pts_]
    for (x, y) in cores:
        art.append(circle(x, y, 22, fill="url(#ozak)", stroke=None, sw=0))
    # aylanish strelkalari (hammasi soat miliga teskari)
    for idx in (0, 4, 9):
        x, y = cores[idx]
        rr = 31
        a0, a1 = math.radians(200), math.radians(200 + 280)
        n = 30
        ptsa = [(x + rr * math.cos(a0 - (a1 - a0) * t / n), y + rr * math.sin(a0 - (a1 - a0) * t / n))
                for t in range(n + 1)]
        art.append(polyline(ptsa[:-2], stroke=CREAM, sw=SW * 0.9))
        e1, e2 = ptsa[-3], ptsa[-1]
        art.append(arrow_head(e2[0], e2[1], math.atan2(e2[1] - e1[1], e2[0] - e1[0]), 13, CREAM))
    defs = f"""<radialGradient id="bulut">
  <stop offset="0" stop-color="#FFF7E6"/>
  <stop offset="0.45" stop-color="{mix(GOLD, CREAM, 0.6)}"/>
  <stop offset="0.78" stop-color="{GOLD}" stop-opacity="0.75"/>
  <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="ozak">
  <stop offset="0" stop-color="{NIGHT}"/><stop offset="0.45" stop-color="{NIGHT}"/>
  <stop offset="1" stop-color="{NIGHT}" stop-opacity="0"/></radialGradient>"""
    c = CREAM
    L.append(text(18, 38, "kondensat", fill=c))
    L.append(leader([(70, 50), (70, 78), (cx - Rc * 0.66, cy - Rc * 0.62)], stroke=c))
    L.append(text(W - 18, H - 20, "uyurma o‘zagi", anchor="end", fill=c))
    tx, ty = max(cores, key=lambda p: p[0] + p[1])
    L.append(leader([(W - 110, H - 52), (W - 110, ty + 40), (tx + 9, ty + 9)], stroke=c))
    return svg_doc(W, H, "Rasm 3.3. Ikki o‘lchamli Boze–Eynshteyn kondensatidagi uyurmalar",
                   "\n".join(art), "\n".join(L), defs)


# =========================================================================
# Rasm 3.4 — Grafen panjarasi
# =========================================================================
def rasm_3_4():
    W, H = 540, 540
    b = 42          # bog' uzunligi
    ra = 10.5       # atom radiusi
    art, L = [], []
    # asalari uyasi panjarasi (A va B pastki panjaralar)
    a1 = np.array([1.5 * b, math.sqrt(3) / 2 * b])
    a2 = np.array([1.5 * b, -math.sqrt(3) / 2 * b])
    atoms = {}
    for i in range(-9, 10):
        for j in range(-9, 10):
            o = i * a1 + j * a2
            atoms[("A", i, j)] = o
            atoms[("B", i, j)] = o + np.array([b, 0])
    bonds = []
    for (s, i, j), p in atoms.items():
        if s == "A":
            for nb in (("B", i, j), ("B", i - 1, j), ("B", i, j - 1)):
                if nb in atoms:
                    bonds.append((p, atoms[nb]))
    # qiya perspektiva (affin + yengil perspektiva)
    cx, cy = 255, 262
    rot = math.radians(12)

    def T(p):
        x, y = p
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        k = 1 / (1 + 0.0009 * (-yr))      # uzoqroq (yuqoriroq) qism kichikroq
        return (cx + xr * k, cy + yr * 0.56 * k)

    def vis(q):
        dx, dy = (q[0] - cx) / 240, (q[1] - cy) / 140
        return dx * dx + dy * dy < 1.25

    bl = []
    for p, q in bonds:
        P, Q = T(p), T(q)
        if vis(P) or vis(Q):
            bl.append(line(P[0], P[1], Q[0], Q[1], stroke=G3, sw=6.5))
    al = []
    pts_ = [T(p) for p in atoms.values()]
    pts_ = [p for p in pts_ if vis(p)]
    for p in sorted(pts_, key=lambda p: p[1]):
        al.append(circle(p[0], p[1], ra, fill="url(#atom)", stroke=G1, sw=SW * 0.6))
    art.append('<g mask="url(#sochilish)">' + "\n".join(bl + al) + '</g>')
    # kattalashtirilgan halqa
    hex_c = atoms[("A", 0, 0)] + np.array([b / 2 + b / 2, 0]) * 0  # markaz tanlash
    # halqa markazi: A(0,0), B(0,0), A(1,0)... olti burchak markazi = A(0,0) + (-b, 0)? hisoblaymiz
    ring = [atoms[k] for k in (("A", 0, 0), ("B", 0, 0), ("A", 1, 0), ("B", 1, -1),
                                ("A", 1, -1), ("B", 0, -1))]
    rc_ = np.mean(ring, axis=0)
    small = T(rc_)
    mx, my, mr = 418, 118, 100
    art.append(ellipse(small[0], small[1], 46, 28, fill="none", stroke=BLUE, sw=SW))
    # urinma chiziqlar
    for sgn in (-1, 1):
        ang = math.atan2(my - small[1], mx - small[0]) + sgn * math.pi / 2
        art.append(line(small[0] + 40 * math.cos(ang), small[1] + 26 * math.sin(ang),
                        mx + mr * math.cos(ang), my + mr * math.sin(ang), stroke=BLUE, sw=SW * 0.8))
    art.append(circle(mx, my, mr, fill=WHITE, stroke=BLUE, sw=SW * 1.4))
    hr = 48
    hexp = [(mx + hr * math.cos(math.radians(60 * k)), my + hr * math.sin(math.radians(60 * k)))
            for k in range(6)]
    for k in range(6):
        p, q = hexp[k], hexp[(k + 1) % 6]
        art.append(line(p[0], p[1], q[0], q[1], stroke=G3, sw=9))
        out = (mx + (hr + 30) * math.cos(math.radians(60 * k)), my + (hr + 30) * math.sin(math.radians(60 * k)))
        art.append(line(p[0], p[1], out[0], out[1], stroke=G4, sw=9, extra=' stroke-linecap="butt"'))
    for p in hexp:
        art.append(circle(p[0], p[1], 15, fill="url(#atom)", stroke=G1, sw=SW * 0.7))
    defs = f"""<radialGradient id="atom" cx="0.35" cy="0.32" r="0.75">
  <stop offset="0" stop-color="{mix(G4, WHITE, 0.6)}"/><stop offset="1" stop-color="{G2}"/></radialGradient>
<radialGradient id="sochGrad" cx="{cx}" cy="{cy}" r="1" gradientUnits="userSpaceOnUse"
  gradientTransform="translate({cx},{cy}) scale(252,150) translate({-cx},{-cy})">
  <stop offset="0" stop-color="#fff"/><stop offset="0.72" stop-color="#fff"/>
  <stop offset="1" stop-color="#000"/></radialGradient>
<mask id="sochilish" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#sochGrad)"/></mask>"""
    # yozuvlar
    p0 = hexp[3]
    L.append(text(18, 40, "uglerod atomi"))
    L.append(leader([(100, 52), (100, p0[1]), (p0[0] - 15, p0[1])]))
    # qalinlik: varaqning yon tomondan ko'rinishi (bir qator atom)
    yr = 468
    xs_ = [40 + 34 * k for k in range(9)]
    art.append(line(xs_[0] - 30, yr, xs_[-1] + 30, yr, stroke=G4, sw=6.5,
                    extra=' stroke-dasharray="2 0"'))
    for x in xs_:
        art.append(circle(x, yr, ra + 1.5, fill="url(#atom)", stroke=G1, sw=SW * 0.6))
    xa = xs_[-1] + 52
    art.append(line(xs_[-1], yr - ra - 1.5, xa + 10, yr - ra - 1.5, stroke=G1, sw=SW * 0.7))
    art.append(line(xs_[-1], yr + ra + 1.5, xa + 10, yr + ra + 1.5, stroke=G1, sw=SW * 0.7))
    L.append(arrow(xa, yr - ra - 30, xa, yr - ra - 1.5, stroke=BLUE, sw=SW, head=11))
    L.append(arrow(xa, yr + ra + 30, xa, yr + ra + 1.5, stroke=BLUE, sw=SW, head=11))
    L.append(text_lines(xa + 22, yr - 6, ["bir atom", "qalinlikda"]))
    return svg_doc(W, H, "Rasm 3.4. Grafen panjarasi", "\n".join(art), "\n".join(L), defs)


if __name__ == "__main__":
    which = sys.argv[1:] or ["3-1", "3-2", "3-3", "3-4"]
    for w in which:
        save(f"rasm_{w}.svg", globals()["rasm_" + w.replace("-", "_")]())
