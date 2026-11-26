"""IV bob — Yuqori o'lchamlar: rasmlar 4.1–4.4"""
import math
import sys
import numpy as np
from common import *


# =========================================================================
# Rasm 4.1 — Nuqtadan tesseraktgacha
# =========================================================================
def rasm_4_1():
    W, H = 1120, 500
    art, L = [], []
    yc = 215
    SWB, SWG = SW * 1.15, SW * 1.9
    figs = []

    def draw(edges_old, edges_new, verts):
        o = []
        for (p, q) in edges_old:
            o.append(line(p[0], p[1], q[0], q[1], stroke=BLUE, sw=SWB))
        for (p, q) in edges_new:
            o.append(line(p[0], p[1], q[0], q[1], stroke=GOLD, sw=SWG))
        for v in verts:
            o.append(circle(v[0], v[1], 6.5, fill=BLUE, stroke=WHITE, sw=1.5))
        return "\n".join(o)

    centers = [62, 245, 470, 718, 968]
    s = 58
    # 0D
    art.append(draw([], [], [(centers[0], yc)]))
    # 1D
    a, b = (centers[1] - s, yc), (centers[1] + s, yc)
    art.append(draw([], [(a, b)], [a, b]))
    # 2D
    cx = centers[2]
    sq = [(cx - s, yc + s), (cx + s, yc + s), (cx + s, yc - s), (cx - s, yc - s)]
    art.append(draw([(sq[0], sq[1]), (sq[3], sq[2])], [(sq[0], sq[3]), (sq[1], sq[2])], sq))
    # 3D (qiya proyeksiya)
    cx = centers[3] - 22
    d = (48, -40)
    f_ = [(cx - s, yc + s + 18), (cx + s, yc + s + 18), (cx + s, yc - s + 18), (cx - s, yc - s + 18)]
    b_ = [(p[0] + d[0], p[1] + d[1]) for p in f_]
    sq_e = lambda P: [(P[i], P[(i + 1) % 4]) for i in range(4)]
    art.append(draw(sq_e(f_) + sq_e(b_), [(f_[i], b_[i]) for i in range(4)], f_ + b_))
    # 4D: kub ichidagi kub
    cx = centers[4] - 28
    S2 = 72
    d2 = (60, -50)
    def cube(c, sz, dd):
        fr = [(c[0] - sz, c[1] + sz), (c[0] + sz, c[1] + sz), (c[0] + sz, c[1] - sz), (c[0] - sz, c[1] - sz)]
        bk = [(p[0] + dd[0], p[1] + dd[1]) for p in fr]
        V = fr + bk
        E = sq_e(fr) + sq_e(bk) + [(fr[i], bk[i]) for i in range(4)]
        return V, E
    oc = (cx, yc + 22)
    Vo, Eo = cube(oc, S2, d2)
    mid = (oc[0] + d2[0] / 2, oc[1] + d2[1] / 2)
    k = 0.42
    Vi = [(mid[0] + (p[0] - mid[0]) * k, mid[1] + (p[1] - mid[1]) * k) for p in Vo]
    Ei = [((mid[0] + (p[0] - mid[0]) * k, mid[1] + (p[1] - mid[1]) * k),
           (mid[0] + (q[0] - mid[0]) * k, mid[1] + (q[1] - mid[1]) * k)) for p, q in Eo]
    En = [(Vi[i], Vo[i]) for i in range(8)]
    assert len(Vo + Vi) == 16 and len(Eo + Ei + En) == 32
    art.append(draw(Eo + Ei, En, Vo + Vi))
    # strelkalar
    gaps = [(centers[0] + 26, centers[1] - s - 24), (centers[1] + s + 24, centers[2] - s - 24),
            (centers[2] + s + 24, centers[3] - 22 - s - 22), (centers[3] - 22 + s + d[0] + 18, centers[4] - 28 - S2 - 20)]
    for x1, x2 in gaps:
        art.append(arrow(x1, yc, x2, yc, stroke=G3, sw=SW, head=16))
    names = ["0D", "1D", "2D", "3D", "4D"]
    counts = [1, 2, 4, 8, 16]
    lab_x = [centers[0], centers[1], centers[2], centers[3] - 22 + d[0] / 2, centers[4] - 28 + d2[0] / 2]
    for x, n_, c in zip(lab_x, names, counts):
        L.append(text(x, 408, n_, anchor="middle", weight="bold", size=32))
        L.append(text(x, 450, f"{c} ta uch", anchor="middle"))
    return svg_doc(W, H, "Rasm 4.1. Nuqtadan tesseraktgacha", "\n".join(art), "\n".join(L))


# =========================================================================
# Rasm 4.2 — Chumoli va arqon
# =========================================================================
def tree(x, ground, h=215):
    trunk = mix(G2, GOLD, 0.25)
    leaf1 = mix(GOLD, CREAM, 0.15)
    leaf2 = mix(GOLD, "#000000", 0.12)
    o = [f'<rect x="{f(x - 13)}" y="{f(ground - h * 0.62)}" width="26" height="{f(h * 0.62)}" '
         f'rx="5" fill="{trunk}"/>']
    blobs = [(0, -0.72, 0.30), (-0.22, -0.60, 0.22), (0.22, -0.60, 0.22), (0, -0.90, 0.22),
             (-0.13, -0.80, 0.2), (0.15, -0.82, 0.2)]
    for i, (dx, dy, r) in enumerate(blobs):
        o.append(circle(x + dx * h, ground + dy * h, r * h, fill=leaf2 if i < 3 else leaf1,
                        stroke=None, sw=0))
    return "\n".join(o)


def ant(x, y, s=1.0):
    """Sodda, do'stona chumoli (o'ngga qaragan)."""
    body = G1
    o = []
    # oyoqlar
    for k, (bx, sx) in enumerate([(-10, -30), (0, 2), (10, 34)]):
        o.append(path(f"M{f(x + (bx + 8) * s)},{f(y + 4 * s)} q{f((sx - bx) * 0.4 * s)},{f(-16 * s)} "
                      f"{f((sx - bx) * s)},{f(22 * s)}", stroke=body, sw=SW * 1.2))
    o.append(ellipse(x - 26 * s, y - 2 * s, 24 * s, 17 * s, fill=body, stroke=None, sw=0))
    o.append(ellipse(x + 6 * s, y - 4 * s, 13 * s, 10 * s, fill=body, stroke=None, sw=0))
    o.append(circle(x + 31 * s, y - 13 * s, 15 * s, fill=body, stroke=None, sw=0))
    # mo'ylovlar
    o.append(path(f"M{f(x + 33 * s)},{f(y - 26 * s)} q{f(2 * s)},{f(-20 * s)} {f(18 * s)},{f(-24 * s)}",
                  stroke=body, sw=SW * 1.1))
    o.append(path(f"M{f(x + 26 * s)},{f(y - 26 * s)} q{f(-4 * s)},{f(-18 * s)} {f(6 * s)},{f(-28 * s)}",
                  stroke=body, sw=SW * 1.1))
    o.append(circle(x + 51 * s, y - 50 * s, 3.5 * s, fill=body, stroke=None, sw=0))
    o.append(circle(x + 32 * s, y - 54 * s, 3.5 * s, fill=body, stroke=None, sw=0))
    # ko'z va tabassum
    o.append(circle(x + 36 * s, y - 17 * s, 6.5 * s, fill=WHITE, stroke=None, sw=0))
    o.append(circle(x + 38 * s, y - 16.5 * s, 3.2 * s, fill="#111111", stroke=None, sw=0))
    o.append(path(f"M{f(x + 34 * s)},{f(y - 5 * s)} q{f(6 * s)},{f(5 * s)} {f(11 * s)},{f(-2 * s)}",
                  stroke=WHITE, sw=SW * 0.9))
    return "\n".join(o)


def rasm_4_2():
    W, H = 1120, 600
    art, L = [], []
    ground = 262
    ry = 192
    art.append(line(20, ground, W - 20, ground, stroke=G4, sw=SW))
    art.append(tree(92, ground))
    art.append(tree(1028, ground))
    art.append(path(f"M105,{ry} Q560,{ry + 16} 1015,{ry}", stroke=G1, sw=SW))
    L.append(text(370, ry - 22, "uzoqdan: 1 o‘lcham", anchor="middle"))
    # lupa
    zx, zy = 560, ry + 8
    mx, my, mr = 560, 432, 150
    for sgn in (-1, 1):
        ang = math.atan2(my - zy, mx - zx) + sgn * math.pi / 2
        art.append(line(zx + 15 * math.cos(ang), zy + 15 * math.sin(ang),
                        mx + mr * math.cos(ang), my + mr * math.sin(ang), stroke=BLUE, sw=SW * 0.8))
    art.append(circle(zx, zy, 15, fill="none", stroke=BLUE, sw=SW))
    rc = 58
    inner = [f'<clipPath id="lupaKlip"><circle cx="{mx}" cy="{my}" r="{mr}"/></clipPath>',
             f'<g clip-path="url(#lupaKlip)">',
             circle(mx, my, mr, fill=WHITE, stroke=None, sw=0),
             f'<rect x="{mx - mr - 5}" y="{my - rc}" width="{2 * mr + 10}" height="{2 * rc}" fill="url(#arqon)"/>',
             line(mx - mr, my - rc, mx + mr, my - rc, stroke=G1, sw=SW),
             line(mx - mr, my + rc, mx + mr, my + rc, stroke=G1, sw=SW)]
    # arqon eshilishi (yengil chiziqlar)
    for k in range(-8, 9):
        x0 = mx + k * 30
        inner.append(path(f"M{f(x0 - 22)},{f(my + rc)} Q{f(x0)},{f(my)} {f(x0 + 22)},{f(my - rc)}",
                          stroke=mix(GOLD, "#000000", 0.1), sw=SW * 0.6, extra=' opacity="0.35"'))
    # o'ralgan o'lcham: kesim aylanasi
    ex = mx + 92
    inner.append(path(f"M{ex},{my - rc} A16,{rc} 0 0 0 {ex},{my + rc}", stroke=ACCENT, sw=SW * 1.2,
                      extra=' stroke-dasharray="7 6"'))
    inner.append('</g>')
    art += inner
    # oldingi yarim (ko'rinadigan) aylana va strelka
    art.append(path(f"M{ex},{my + rc} A16,{rc} 0 0 0 {ex},{my - rc}", stroke=ACCENT, sw=SW * 1.5))
    art.append(arrow_head(ex - 3, my - rc + 4, math.radians(-100), 18, ACCENT))
    art.append(circle(mx, my, mr, fill="none", stroke=BLUE, sw=SW * 1.5))
    # chumoli
    art.append(ant(mx - 50, my - 14, 1.15))
    # arqon bo'ylab strelka
    art.append(arrow(mx - 140, my + 30, mx + 52, my + 30, stroke=BLUE, sw=SW * 1.4, head=18))
    L.append(text(mx - mr - 26, my - 120, "yaqindan:", anchor="end"))
    L.append(text(mx - mr - 26, my - 84, "2 o‘lcham", anchor="end"))
    L.append(text(mx + mr + 40, my + 108, "o‘ralgan o‘lcham"))
    L.append(leader([(mx + mr + 32, my + 98), (mx + mr - 10, my + 98), (ex + 17, my + 22)]))
    defs = f"""<linearGradient id="arqon" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{mix(GOLD, CREAM, 0.35)}"/><stop offset="0.35" stop-color="{mix(GOLD, CREAM, 0.7)}"/>
  <stop offset="1" stop-color="{mix(GOLD, G1, 0.25)}"/></linearGradient>"""
    return svg_doc(W, H, "Rasm 4.2. Chumoli va arqon", "\n".join(art), "\n".join(L), defs)


# =========================================================================
# Rasm 4.3 — Kalabi–Yau fazosi (kvintik kesimi, o'zimiz hisoblagan)
# =========================================================================
def rasm_4_3():
    W = H = 540
    n = 5
    alpha = math.pi / 4
    m = 12
    xs = np.linspace(-1, 1, m)
    ys = np.linspace(0, math.pi / 2, m)
    X, Y = np.meshgrid(xs, ys)
    Z = X + 1j * Y
    quads = []
    rot_y, rot_x = math.radians(38), math.radians(-28)
    Ry = np.array([[math.cos(rot_y), 0, math.sin(rot_y)], [0, 1, 0], [-math.sin(rot_y), 0, math.cos(rot_y)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(rot_x), -math.sin(rot_x)], [0, math.sin(rot_x), math.cos(rot_x)]])
    R = Rx @ Ry
    for k1 in range(n):
        for k2 in range(n):
            z1 = np.exp(2j * math.pi * k1 / n) * np.cosh(Z) ** (2 / n)
            z2 = np.exp(2j * math.pi * k2 / n) * np.sinh(Z) ** (2 / n)
            P = np.stack([z1.real, z2.real, math.cos(alpha) * z1.imag + math.sin(alpha) * z2.imag], -1)
            P = P @ R.T
            for i in range(m - 1):
                for j in range(m - 1):
                    q = np.array([P[i, j], P[i, j + 1], P[i + 1, j + 1], P[i + 1, j]])
                    quads.append((q, k1, k2))
    allp = np.concatenate([q for q, _, _ in quads])
    mn, mx_ = allp[:, :2].min(0), allp[:, :2].max(0)
    sc = (W - 50) / max(mx_ - mn)
    off = np.array([W, H]) / 2 - (mn + mx_) / 2 * sc
    light = np.array([-0.4, -0.6, 0.7])
    light /= np.linalg.norm(light)
    quads.sort(key=lambda t: t[0][:, 2].mean())
    art = []
    art.append('<g stroke-linejoin="round">')
    for q, k1, k2 in quads:
        nrm = np.cross(q[1] - q[0], q[3] - q[0])
        nn = np.linalg.norm(nrm)
        if nn < 1e-9:
            continue
        nrm /= nn
        sh = abs(nrm @ light)
        base = mix(BLUE, GOLD, 0.25 + 0.5 * ((k1 + k2) % 5) / 4)
        col = mix(base, CREAM, 0.15 + 0.7 * sh)
        p2 = q[:, :2] * sc + off
        p2[:, 1] = H - p2[:, 1]
        art.append(f'<polygon points="{pts(p2)}" fill="{col}" fill-opacity="0.62" '
                   f'stroke="{BLUE}" stroke-opacity="0.55" stroke-width="1.1"/>')
    art.append('</g>')
    return svg_doc(W, H, "Rasm 4.3. Kalabi–Yau fazosi", "\n".join(art), "",
                   desc="Kvintik Kalabi–Yau ko‘pxilligining 2 o‘lchamli kesimi; "
                        "tenglamalar asosida hisoblab, qayta chizilgan.")


# =========================================================================
# Rasm 4.4 — Bran-olamlar
# =========================================================================
def rasm_4_4():
    W, H = 1120, 700
    rng = np.random.default_rng(44)
    art, L = [], []
    art.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{NIGHT}"/>')
    # fon yulduzlari (balk)
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        art.append(circle(x, y, rng.uniform(0.8, 2.0), fill=CREAM, stroke=None, sw=0,
                          extra=f' opacity="{rng.uniform(0.15, 0.45):.2f}"'))

    def surf(u, v, base, ph):
        # u: -1..1 (eni), v: 0..1 (chuqurlik)
        z = 22 * np.sin(2.4 * u + 3.2 * v + ph) + 12 * np.sin(4.1 * v - 1.7 * u + ph * 1.3)
        X = 560 + u * (480 - 70 * v) + 90 * v
        Y = base - v * 150 - z
        return X, Y

    def brane(base, ph, fill_id, lid):
        g = []
        uu = np.linspace(-1, 1, 60)
        vv = np.linspace(0, 1, 30)
        edge = []
        for u in uu:
            edge.append(surf(u, 0, base, ph))
        for v in vv:
            edge.append(surf(1, v, base, ph))
        for u in uu[::-1]:
            edge.append(surf(u, 1, base, ph))
        for v in vv[::-1]:
            edge.append(surf(-1, v, base, ph))
        g.append(polygon(edge, fill=f"url(#{fill_id})", stroke=mix(CREAM, BLUE, 0.3), sw=SW,
                         extra=' fill-opacity="0.85"'))
        for u in np.linspace(-1, 1, 13)[1:-1]:
            g.append(polyline([surf(u, v, base, ph) for v in vv], stroke=CREAM, sw=1.2,
                              extra=' opacity="0.28"'))
        for v in np.linspace(0, 1, 8)[1:-1]:
            g.append(polyline([surf(u, v, base, ph) for u in uu], stroke=CREAM, sw=1.2,
                              extra=' opacity="0.28"'))
        return f'<g id="{lid}">' + "\n".join(g) + '</g>'

    def open_string(u, v, base, ph, du=0.07, h=34, down=False):
        p1 = surf(u - du, v, base, ph)
        p2 = surf(u + du, v, base, ph)
        mxp, myp = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + (h if down else -h)
        hh = h if down else -h
        o = [path(f"M{f(p1[0])},{f(p1[1])} C{f(p1[0] - 6)},{f(p1[1] + hh * 1.3)} "
                  f"{f(p2[0] + 6)},{f(p2[1] + hh * 1.3)} {f(p2[0])},{f(p2[1])}", stroke=ACCENT, sw=SW * 1.3),
             circle(p1[0], p1[1], 5, fill=ACCENT, stroke=None, sw=0),
             circle(p2[0], p2[1], 5, fill=ACCENT, stroke=None, sw=0)]
        return "\n".join(o), (mxp, myp)

    up_b, lo_b = 300, 650
    art.append(brane(up_b, 1.3, "branUst", "qoshni-bran"))
    # bizning bran: galaktikalar, yulduzlar
    art.append(brane(lo_b, 0.2, "branPast", "bizning-bran"))
    gal = []
    for _ in range(14):
        u, v = rng.uniform(-0.9, 0.9), rng.uniform(0.08, 0.92)
        x, y = surf(u, v, lo_b, 0.2)
        s_ = rng.uniform(0.7, 1.3) * (1 - 0.35 * v)
        a_ = rng.uniform(-30, 30)
        gal.append(f'<g transform="translate({f(x)},{f(y)}) rotate({f(a_)}) scale({s_:.2f},{s_ * 0.5:.2f})">'
                   f'<ellipse rx="22" ry="22" fill="url(#galaktika)"/>'
                   f'<path d="M-16,4 Q-4,-16 14,-6 M16,-4 Q4,16 -14,6" fill="none" stroke="{CREAM}" '
                   f'stroke-width="2.4" opacity="0.8"/></g>')
    for _ in range(90):
        u, v = rng.uniform(-0.97, 0.97), rng.uniform(0.02, 0.98)
        x, y = surf(u, v, lo_b, 0.2)
        gal.append(circle(x, y, rng.uniform(1, 2.4), fill=CREAM, stroke=None, sw=0,
                          extra=f' opacity="{rng.uniform(0.5, 1):.2f}"'))
    art.append('<g id="galaktikalar">' + "\n".join(gal) + '</g>')
    # ochiq torlar
    strings = []
    for (u, v) in [(-0.55, 0.25), (0.05, 0.62), (0.62, 0.30), (0.35, 0.82), (-0.2, 0.9)]:
        s_, top = open_string(u, v, lo_b, 0.2)
        strings.append(s_)
    target_open = surf(0.62, 0.30, lo_b, 0.2)
    for (u, v) in [(-0.45, 0.55), (0.48, 0.65)]:
        s_, _ = open_string(u, v, up_b, 1.3, h=30)
        strings.append(s_)
    art.append('<g id="ochiq-torlar">' + "\n".join(strings) + '</g>')
    # yopiq tor (graviton) — branlar orasida
    gx, gy = 760, 330
    th = np.linspace(0, 2 * np.pi, 200)
    rr = 26 + 4 * np.sin(6 * th)
    loop = [(gx + r * math.cos(t), gy + 0.8 * r * math.sin(t)) for r, t in zip(rr, th)]
    art.append(polygon(loop, fill="none", stroke=ACCENT, sw=SW * 1.3))
    art.append(arrow(gx + 10, gy - 40, gx + 34, gy - 96, stroke=ACCENT, sw=SW, head=13))

    defs = f"""<linearGradient id="branUst" x1="0" y1="1" x2="0.3" y2="0">
  <stop offset="0" stop-color="{mix(BLUE, CREAM, 0.30)}"/><stop offset="1" stop-color="{mix(BLUE, NIGHT, 0.4)}"/></linearGradient>
<linearGradient id="branPast" x1="0" y1="1" x2="0.3" y2="0">
  <stop offset="0" stop-color="{mix(BLUE, CREAM, 0.22)}"/><stop offset="1" stop-color="{mix(BLUE, NIGHT, 0.35)}"/></linearGradient>
<radialGradient id="galaktika"><stop offset="0" stop-color="#FFF6DE"/>
  <stop offset="0.35" stop-color="{mix(GOLD, CREAM, 0.4)}" stop-opacity="0.9"/>
  <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>"""
    c = CREAM
    L.append(text(20, 52, "qo‘shni bran", fill=c))
    p = surf(-0.85, 0.75, up_b, 1.3)
    L.append(leader([(232, 42), (p[0], 42), p], stroke=c))
    L.append(text(20, 372, "balk (ko‘p o‘lchamli fazo)", fill=c))
    L.append(text(20, H - 22, "bizning bran-olamimiz", fill=c))
    uu_ = np.linspace(-1, 1, 400)
    xs_, ys_ = surf(uu_, 0.12, lo_b, 0.2)
    j_ = int(np.argmin(np.abs(xs_ - 365)))
    L.append(leader([(335, H - 32), (365, H - 32), (365, ys_[j_])], stroke=c))
    L.append(text(W - 20, 420, "yopiq tor (graviton)", anchor="end", fill=c))
    L.append(leader([(W - 290, 410), (gx + 50, 410), (gx + 22, gy + 16)], stroke=c))
    L.append(text(W - 20, H - 22, "ochiq tor (modda, yorug‘lik)", anchor="end", fill=c))
    L.append(leader([(W - 170, H - 52), (W - 170, target_open[1] - 20), (target_open[0] + 30, target_open[1] - 28)], stroke=c))
    return svg_doc(W, H, "Rasm 4.4. Bran-olamlar", "\n".join(art), "\n".join(L), defs)


if __name__ == "__main__":
    which = sys.argv[1:] or ["4-1", "4-2", "4-3", "4-4"]
    for w in which:
        save(f"rasm_{w}.svg", globals()["rasm_" + w.replace("-", "_")]())
