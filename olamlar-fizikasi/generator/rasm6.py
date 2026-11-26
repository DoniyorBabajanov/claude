"""VI bob — Tegmarkning olamlari: rasmlar 6.1–6.4"""
import math
import sys
import numpy as np
from common import *


def galaxy(x, y, s=1.0, rot=0, col=CREAM, core="#FFF6DE", opacity=1.0):
    """Kichik spiral galaktika belgisi: xira disk, ikki spiral qo'l va yorqin o'zak."""
    return (f'<g transform="translate({f(x)},{f(y)}) rotate({f(rot)}) scale({s:.2f},{s * 0.6:.2f})" '
            f'opacity="{opacity:.2f}">'
            f'<ellipse rx="14" ry="14" fill="{col}" opacity="0.22"/>'
            f'<path d="M-1,-2 C7,-11 17,-3 12,6 M1,2 C-7,11 -17,3 -12,-6" fill="none" stroke="{col}" '
            f'stroke-width="2.6" stroke-linecap="round"/>'
            f'<circle r="3.6" fill="{core}"/></g>')


# =========================================================================
# Rasm 6.1 — To'rt darajali multikoinot
# =========================================================================
def rasm_6_1():
    W = H = 1120
    cx, cy = 560, 560
    rng = np.random.default_rng(61)
    radii = [175, 300, 422, 548]
    fills = [mix(CREAM, WHITE, 0.25), mix(CREAM, BLUE, 0.20), mix(CREAM, BLUE, 0.46),
             mix(CREAM, BLUE, 0.78)]
    inks = [BLUE, BLUE, CREAM, CREAM]
    art, L, defs = [], [], []
    for r, fl in list(zip(radii, fills))[::-1]:
        art.append(circle(cx, cy, r, fill=fl, stroke=BLUE, sw=SW * 1.2))

    def free(x, y, rmin, rmax, pad=0):
        d = math.hypot(x - cx, y - cy)
        if not (rmin + pad < d < rmax - pad):
            return False
        ang = math.degrees(math.atan2(y - cy, x - cx)) % 360
        # yozuv yoyi (yuqori qism, tashqi chetga yaqin)
        if 192 < ang < 348 and d > rmax - 64:
            return False
        return True

    # I — bir xil mayda galaktikalar
    g = []
    for gx in np.arange(cx - 170, cx + 171, 46):
        for gy in np.arange(cy - 170, cy + 171, 46):
            x, y = gx + rng.uniform(-10, 10), gy + rng.uniform(-10, 10)
            if not free(x, y, 30, radii[0], 12):
                continue
            if abs(x - cx) < 160 and 572 < y < 662:
                continue
            g.append(galaxy(x, y, 0.95, rng.uniform(0, 180), col=GOLD, core=GOLD))
    art.append('<g id="I-galaktikalar">' + "\n".join(g) + '</g>')
    # II — turli rangdagi pufakchalar
    cols = [GOLD, ACCENT, CREAM, mix(BLUE, WHITE, 0.55), G4, mix(ACCENT, CREAM, 0.5)]
    placed = []
    g = []
    tries = 0
    while len(placed) < 40 and tries < 6000:
        tries += 1
        r_ = rng.uniform(9, 25)
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(radii[0] + r_ + 6, radii[1] - r_ - 6)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        if not free(x, y, radii[0], radii[1], r_):
            continue
        if any(math.hypot(x - px, y - py) < r_ + pr + 7 for px, py, pr in placed):
            continue
        placed.append((x, y, r_))
        c = cols[len(placed) % len(cols)]
        g.append(circle(x, y, r_, fill=c, stroke=BLUE, sw=SW * 0.7))
        g.append(circle(x - r_ * 0.35, y - r_ * 0.35, r_ * 0.22, fill=WHITE, stroke=None, sw=0,
                        extra=' opacity="0.6"'))
    art.append('<g id="II-pufakchalar">' + "\n".join(g) + '</g>')
    # III — tarmoqlanuvchi ingichka chiziqlar
    g = []
    def branch(x, y, ang, ln, depth):
        if depth == 0:
            return
        x2, y2 = x + ln * math.cos(ang), y + ln * math.sin(ang)
        g.append(line(x, y, x2, y2, stroke=CREAM, sw=SW * (0.45 + 0.25 * depth)))
        for da in (-0.42, 0.42):
            branch(x2, y2, ang + da, ln * 0.7, depth - 1)
    n3 = 20
    for k in range(n3):
        a = 2 * math.pi * k / n3 + 0.1
        ad = math.degrees(a) % 360
        if 196 < ad < 344:
            continue
        r0 = radii[1] + 18
        branch(cx + r0 * math.cos(a), cy + r0 * math.sin(a), a, 34, 4)
    for k in range(9):
        a = math.radians(198 + 148 * (k + 0.5) / 9)
        r0 = radii[1] + 12
        branch(cx + r0 * math.cos(a), cy + r0 * math.sin(a), a, 20, 3)
    art.append('<g id="III-tarmoqlar" opacity="0.85">' + "\n".join(g) + '</g>')
    # IV — geometrik shakllar va matematik belgilar
    g = []
    syms = ["π", "∞", "∑", "∫", "√2", "∂", "φ", "e", "i", "ℵ₀", "∇", "≅", "∈", "∀", "ħ"]
    shapes = ["tri", "hex", "cube", "circ", "sq"]
    n4 = 30
    k_s = 0
    for k in range(n4):
        a = 2 * math.pi * k / n4 + 0.05
        ad = math.degrees(a) % 360
        rr = (radii[2] + radii[3]) / 2 + (18 if k % 2 else -14)
        if 194 < ad < 346:
            rr = radii[2] + 34
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        if k % 2 == 0:
            s = syms[k_s % len(syms)]
            k_s += 1
            g.append(f'<text x="{f(x)}" y="{f(y + 12)}" font-family="{FONT}" font-size="36" '
                     f'text-anchor="middle" fill="{CREAM}" opacity="0.9">{esc(s)}</text>')
        else:
            sh = shapes[(k // 2) % len(shapes)]
            if sh == "tri":
                g.append(polygon([(x, y - 18), (x + 17, y + 12), (x - 17, y + 12)], fill="none", stroke=GOLD, sw=SW))
            elif sh == "hex":
                g.append(polygon([(x + 17 * math.cos(math.radians(60 * j)), y + 17 * math.sin(math.radians(60 * j)))
                                  for j in range(6)], fill="none", stroke=GOLD, sw=SW))
            elif sh == "cube":
                g.append(polygon([(x - 13, y - 5), (x + 7, y - 5), (x + 7, y + 15), (x - 13, y + 15)], fill="none", stroke=GOLD, sw=SW))
                g.append(polyline([(x - 13, y - 5), (x - 5, y - 13), (x + 15, y - 13), (x + 15, y + 7), (x + 7, y + 15)],
                                  stroke=GOLD, sw=SW))
                g.append(line(x + 7, y - 5, x + 15, y - 13, stroke=GOLD, sw=SW))
            elif sh == "circ":
                g.append(path(f"M{f(x - 20)},{f(y)} C{f(x - 13)},{f(y - 22)} {f(x - 7)},{f(y - 22)} {f(x)},{f(y)} "
                              f"S{f(x + 13)},{f(y + 22)} {f(x + 20)},{f(y)}", stroke=GOLD, sw=SW))
            else:
                g.append(polygon([(x - 14, y - 14), (x + 14, y - 14), (x + 14, y + 14), (x - 14, y + 14)],
                                 fill="none", stroke=GOLD, sw=SW,
                                 extra=f' transform="rotate(45 {f(x)} {f(y)})"'))
    art.append('<g id="IV-matematika">' + "\n".join(g) + '</g>')
    # markaz: bizning kuzatiladigan koinot
    art.append(circle(cx, cy, 13, fill=GOLD, stroke=BLUE, sw=SW))
    # yoy bo'ylab yozuvlar
    names = ["I daraja: gorizontdan nari", "II daraja: pufakcha-koinotlar",
             "III daraja: kvant tarmoqlari", "IV daraja: matematik tuzilmalar"]
    for k, (r, nm) in enumerate(zip(radii, names)):
        rr = r - 40
        pid = f"yoy{k + 1}"
        defs.append(f'<path id="{pid}" d="M{f(cx - rr)},{f(cy)} A{f(rr)},{f(rr)} 0 0 1 {f(cx + rr)},{f(cy)}"/>')
        L.append(f'<text font-size="{FS}" fill="{inks[k]}" font-weight="bold">'
                 f'<textPath href="#{pid}" xlink:href="#{pid}" startOffset="50%" text-anchor="middle">{esc(nm)}</textPath></text>')
    L.append(text_lines(cx, cy + 58, ["bizning kuzatiladigan", "koinot"], anchor="middle", size=FS_SMALL))
    L.append(line(cx, cy + 16, cx, cy + 30, stroke=BLUE, sw=SW))
    return svg_doc(W, H, "Rasm 6.1. To‘rt darajali multikoinot", "\n".join(art), "\n".join(L), "\n".join(defs))


# =========================================================================
# Rasm 6.2 — Reliktli nurlanish xaritasi
# =========================================================================
CMB_STOPS = [(0.0, "#1F3A5F"), (0.25, "#3F5689"), (0.5, "#7E5F86"), (0.75, "#C0614A"), (1.0, "#EFAE7C")]


def cmb_color(t):
    for (t0, c0), (t1, c1) in zip(CMB_STOPS, CMB_STOPS[1:]):
        if t <= t1:
            return mix(c0, c1, (t - t0) / (t1 - t0))
    return CMB_STOPS[-1][1]


def rasm_6_2():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.spatial import cKDTree
    W, H = 1120, 550
    cx, cy, a, b = 560, 228, 450, 225
    rng = np.random.default_rng(62)
    # sferada tasodifiy Gauss maydoni (ikki masshtab)
    def rand_sphere(n):
        v = rng.normal(size=(n, 3))
        return v / np.linalg.norm(v, axis=1, keepdims=True)
    nu, nv = 560, 280
    u = np.linspace(-1, 1, nu)
    v = np.linspace(-1, 1, nv)
    U, V = np.meshgrid(u, v)
    th = np.arcsin(np.clip(V, -1, 1))
    lat = np.arcsin(np.clip((2 * th + np.sin(2 * th)) / math.pi, -1, 1))
    lon = math.pi * U / np.maximum(np.cos(th), 1e-3)
    lon = np.clip(lon, -math.pi, math.pi)
    P = np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], -1).reshape(-1, 3)
    field = np.zeros(len(P))
    tree = cKDTree(P)
    for n, sig, amp in [(9000, 0.020, 1.0), (2500, 0.045, 0.8)]:
        C = rand_sphere(n)
        w = rng.normal(size=n) * amp
        for ci, wi in zip(C, w):
            idx = tree.query_ball_point(ci, 3 * sig)
            if idx:
                d2 = np.sum((P[idx] - ci) ** 2, axis=1)
                field[idx] += wi * np.exp(-d2 / (2 * sig * sig))
    field = field.reshape(nv, nu)
    field = (field - field.mean()) / field.std()
    levels = [-10, -1.6, -1.0, -0.5, -0.15, 0.15, 0.5, 1.0, 1.6, 10]
    fig = plt.figure()
    cs = plt.contourf(U, V, field, levels=levels)
    plt.close(fig)
    nb = len(levels) - 1
    art = [f'<clipPath id="ellips"><ellipse cx="{cx}" cy="{cy}" rx="{a}" ry="{b}"/></clipPath>',
           '<g clip-path="url(#ellips)">']
    paths = cs.get_paths()
    for k, pth in enumerate(paths):
        col = cmb_color(k / (nb - 1))
        verts, codes = pth.vertices, pth.codes
        if len(verts) == 0:
            continue
        d = []
        for (x, y), c in zip(verts, codes if codes is not None else [2] * len(verts)):
            X, Y = cx + x * a, cy - y * b
            if c == 1:
                d.append(f"M{X:.0f},{Y:.0f}")
            elif c == 79:
                d.append("Z")
            else:
                d.append(f"L{X:.0f},{Y:.0f}")
        art.append(f'<path d="{"".join(d)}" fill="{col}" fill-rule="evenodd" stroke="none"/>')
    art.append('</g>')
    art.append(ellipse(cx, cy, a, b, fill="none", stroke=BLUE, sw=SW))
    # rang shkalasi
    sx0, sw_, sy, sh = 330, 460, 474, 22
    for k in range(nb):
        art.append(f'<rect x="{f(sx0 + k * sw_ / nb)}" y="{sy}" width="{f(sw_ / nb + 0.5)}" height="{sh}" '
                   f'fill="{cmb_color(k / (nb - 1))}"/>')
    art.append(f'<rect x="{sx0}" y="{sy}" width="{sw_}" height="{sh}" fill="none" stroke="{BLUE}" stroke-width="{SW}"/>')
    L = [text(sx0 - 16, sy + 20, "sovuqroq", anchor="end"),
         text(sx0 + sw_ + 16, sy + 20, "issiqroq"),
         text(cx, 538, "farq: gradusning yuz mingdan bir ulushi", anchor="middle", size=FS_SMALL)]
    return svg_doc(W, H, "Rasm 6.2. Reliktli nurlanish xaritasi", "\n".join(art), "\n".join(L),
                   desc="Original chizma: tasodifiy izotrop maydon, Mollveyde proyeksiyasi. "
                        "ESA Planck xaritasidan nusxa emas.")


# =========================================================================
# Rasm 6.3 — Abadiy inflyatsiya
# =========================================================================
def rasm_6_3():
    W, H = 1120, 600
    rng = np.random.default_rng(63)
    art, L, defs = [], [], []
    art.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#fazo)"/>')
    hues = [GOLD, mix(BLUE, WHITE, 0.55), ACCENT, mix(ACCENT, BLUE, 0.45), mix(GOLD, CREAM, 0.6),
            mix(G4, BLUE, 0.2), mix("#6F9A8A", BLUE, 0.1)]
    for i, h in enumerate(hues):
        defs.append(f'<radialGradient id="pf{i}" cx="0.4" cy="0.38" r="0.7">'
                    f'<stop offset="0" stop-color="{mix(h, WHITE, 0.55)}" stop-opacity="0.95"/>'
                    f'<stop offset="0.7" stop-color="{h}" stop-opacity="0.75"/>'
                    f'<stop offset="1" stop-color="{h}" stop-opacity="0.95"/></radialGradient>')
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
    our = 3   # bizning koinot: (455, 470, 66)
    for i, (x, y, r) in enumerate(bubbles):
        hi = i % len(hues)
        art.append(circle(x, y, r, fill=f"url(#pf{hi})", stroke=mix(hues[hi], WHITE, 0.4), sw=SW))
        if r >= 40:
            ng = int(r / 9)
            for _ in range(ng):
                a = rng.uniform(0, 2 * math.pi)
                d = rng.uniform(0, r * 0.72)
                art.append(galaxy(x + d * math.cos(a), y + d * math.sin(a), rng.uniform(0.6, 1.0) * min(1, r / 70),
                                  rng.uniform(0, 180), col=WHITE, core="#FFFFFF", opacity=0.8))
        elif r <= 12:
            art.append(circle(x, y, r * 0.35, fill=WHITE, stroke=None, sw=0, extra=' opacity="0.9"'))
    # kengayish strelkalari (pufakchalar orasida, siyrak)
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
        art.append(arrow(x, y, x + 24 * math.cos(ang), y + 24 * math.sin(ang), stroke=mix(CREAM, NIGHT, 0.4),
                         sw=SW * 0.8, head=10))
    defs.append(f'<radialGradient id="fazo" cx="0.5" cy="0.5" r="0.75">'
                f'<stop offset="0" stop-color="{mix(NIGHT, BLUE, 0.55)}"/><stop offset="1" stop-color="{NIGHT}"/></radialGradient>')
    ox, oy, orr = bubbles[our]
    c = CREAM
    L.append(text(580, 522, "bizning koinot", fill=c))
    L.append(arrow(574, 508, ox + orr * 0.74 + 4, oy + orr * 0.5 + 4, stroke=c, sw=SW, head=15))
    L.append(text(W - 24, H - 24, "shishayotgan fazo", anchor="end", fill=c))
    return svg_doc(W, H, "Rasm 6.3. Abadiy inflyatsiya", "\n".join(art), "\n".join(L), "\n".join(defs))


# =========================================================================
# Rasm 6.4 — Qora tuynuk sirtidagi axborot
# =========================================================================
def rasm_6_4():
    W = H = 540
    cx, cy, R = 212, 318, 182
    rng = np.random.default_rng(64)
    tilt = math.radians(24)
    spin = math.radians(8)

    def P3(lat, lon):
        x = np.cos(lat) * np.sin(lon + spin)
        y = np.sin(lat)
        z = np.cos(lat) * np.cos(lon + spin)
        # x o'qi atrofida egish (shimol qutbi biz tomonga)
        y2 = y * math.cos(tilt) - z * math.sin(tilt)
        z2 = y * math.sin(tilt) + z * math.cos(tilt)
        return x, y2, z2

    def S(x, y):
        return cx + R * x, cy - R * y

    art, L = [], []
    art.append(circle(cx, cy, R, fill="url(#qoraShar)", stroke=G1, sw=SW))
    dl = math.radians(10)
    lats = np.arange(-90, 91, 10)
    segs = []

    def add_curve(lat_arr, lon_arr):
        x, y, z = P3(lat_arr, lon_arr)
        cur = []
        for xi, yi, zi in zip(x, y, z):
            if zi > 0.0:
                cur.append(S(xi, yi))
            else:
                if len(cur) > 1:
                    segs.append((cur, None))
                cur = []
        if len(cur) > 1:
            segs.append((cur, None))

    cells = []
    for i in range(len(lats) - 1):
        la0, la1 = math.radians(lats[i]), math.radians(lats[i + 1])
        lc = (la0 + la1) / 2
        n = max(3, int(round(36 * math.cos(lc))))
        off = rng.uniform(0, 2 * math.pi / n)
        # kenglik chizig'i
        lon = np.linspace(-math.pi, math.pi, 400)
        add_curve(np.full_like(lon, la0), lon)
        for k in range(n):
            lo = off + 2 * math.pi * k / n
            add_curve(np.linspace(la0, la1, 12), np.full(12, lo))
            cells.append((lc, lo + math.pi / n, la1 - la0, 2 * math.pi / n * math.cos(lc)))
    g = ['<g id="katakchalar" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" opacity="0.9">' % GOLD]
    for pts_, _ in segs:
        g.append(f'<polyline points="{pts(pts_)}"/>')
    g.append('</g>')
    art += g
    # raqamlar
    dg = []
    for (lc, lo, dla, dlo) in cells:
        x, y, z = P3(np.array([lc]), np.array([lo]))
        x, y, z = float(x[0]), float(y[0]), float(z[0])
        if z < 0.35 or rng.random() > 0.55:
            continue
        e = 1e-4
        xa, ya, _ = P3(np.array([lc]), np.array([lo + e / math.cos(lc)]))
        xb, yb, _ = P3(np.array([lc + e]), np.array([lo]))
        ex = np.array([float(xa[0]) - x, -(float(ya[0]) - y)]) / e * R   # sharq (ekranda)
        en = np.array([float(xb[0]) - x, -(float(yb[0]) - y)]) / e * R   # shimol (ekranda)
        sx, sy = S(x, y)
        k = 0.0135
        m = (ex[0] * k, ex[1] * k, -en[0] * k, -en[1] * k)
        dg.append(f'<text transform="matrix({m[0]:.3f},{m[1]:.3f},{m[2]:.3f},{m[3]:.3f},{sx:.1f},{sy:.1f})" '
                  f'font-family="{FONT}" font-size="10" text-anchor="middle" dy="3.6" fill="{CREAM}" '
                  f'opacity="{0.35 + 0.6 * z:.2f}">{rng.integers(0, 2)}</text>')
    art.append('<g id="bitlar">' + "\n".join(dg) + '</g>')
    # kattalashtirish doirasi
    tlc, tlo = math.radians(35), None
    best = None
    for (lc, lo, dla, dlo) in cells:
        x, y, z = P3(np.array([lc]), np.array([lo]))
        if z[0] > 0.6 and lc > math.radians(20):
            sc_ = S(float(x[0]), float(y[0]))
            score = sc_[0] - 0.4 * sc_[1]
            if best is None or score > best[0]:
                best = (score, sc_)
    hx, hy = best[1]
    mx, my, mr = 448, 98, 74
    for sgn in (-1, 1):
        ang = math.atan2(my - hy, mx - hx) + sgn * math.pi / 2
        art.append(line(hx + 13 * math.cos(ang), hy + 13 * math.sin(ang), mx + mr * math.cos(ang),
                        my + mr * math.sin(ang), stroke=BLUE, sw=SW * 0.8))
    art.append(circle(hx, hy, 13, fill="none", stroke=ACCENT, sw=SW * 1.2))
    art.append(circle(mx, my, mr, fill=WHITE, stroke=BLUE, sw=SW * 1.4))
    art.append(f'<rect x="{mx - 40}" y="{my - 40}" width="80" height="80" fill="#0B0B0B" stroke="{GOLD}" stroke-width="{SW * 1.4}"/>')
    art.append(f'<text x="{mx}" y="{my + 22}" font-family="{FONT}" font-size="62" text-anchor="middle" '
               f'fill="{CREAM}">1</text>')
    defs = f"""<radialGradient id="qoraShar" cx="0.38" cy="0.32" r="0.75">
  <stop offset="0" stop-color="#3A3A3A"/><stop offset="0.55" stop-color="#121212"/><stop offset="1" stop-color="#000000"/></radialGradient>"""
    L.append(text(mx - mr - 14, 76, "har katakcha ≈ 1 bit", anchor="end"))
    L.append(text(16, H - 14, "voqealar gorizonti"))
    yy_ = cy + 92
    L.append(leader([(22, H - 42), (22, yy_), (cx - math.sqrt(R * R - (yy_ - cy) ** 2) + 6, yy_)]))
    return svg_doc(W, H, "Rasm 6.4. Qora tuynuk sirtidagi axborot", "\n".join(art), "\n".join(L), defs)


if __name__ == "__main__":
    which = sys.argv[1:] or ["6-1", "6-2", "6-3", "6-4"]
    for w in which:
        save(f"rasm_{w}.svg", globals()["rasm_" + w.replace("-", "_")]())
