"""V bob — Kvantlar olami: rasmlar 5.1–5.3"""
import math
import sys
import numpy as np
from common import *


# =========================================================================
# Rasm 5.1 — Ikki tirqishli tajriba
# =========================================================================
LAM, DSL, SLIT_W = 15.0, 64.0, 10.0


def wave_I(y, xs, xsc, yc):
    """Ekrandagi yorqinlik: ikki tirqish interferensiyasi x bitta tirqish
    difraksiyasi (sinc^2) — aniq yo'l farqi bilan."""
    y1, y2 = yc - DSL / 2, yc + DSL / 2
    r1 = np.hypot(xsc - xs, y - y1)
    r2 = np.hypot(xsc - xs, y - y2)
    sin_t = (y - yc) / np.hypot(xsc - xs, y - yc)
    beta = math.pi * SLIT_W * sin_t / LAM
    env = np.where(np.abs(beta) < 1e-9, 1.0, (np.sin(beta) / np.where(beta == 0, 1, beta)) ** 2)
    return np.cos(math.pi * (r1 - r2) / LAM) ** 2 * env * (np.cos(np.arctan2(y - yc, xsc - xs))) ** 3


def screen_strip(x, y0, y1, I, w=20):
    """Ekran: yorqinlik bo'yicha bo'yalgan gorizontal bo'laklar."""
    o = []
    n = len(I)
    hh = (y1 - y0) / n
    for k in range(n):
        c = mix(BLUE, "#FFF4DA", float(I[k]) ** 0.8)
        o.append(f'<rect x="{f(x)}" y="{f(y0 + k * hh)}" width="{w}" height="{f(hh + 0.6)}" fill="{c}"/>')
    o.append(f'<rect x="{f(x)}" y="{f(y0)}" width="{w}" height="{f(y1 - y0)}" fill="none" '
             f'stroke="{BLUE}" stroke-width="{SW}"/>')
    return "\n".join(o)


def rasm_5_1():
    W, H = 1120, 700
    art, L = [], []
    yc = 292
    ytop, ybot = 82, 502
    xs_src, xs_w, xs_scr, xs_gr = 42, 190, 420, 452
    ys = np.linspace(ytop, ybot, 210)

    def wall(ox):
        y1, y2 = yc - DSL / 2, yc + DSL / 2
        h = SLIT_W / 2
        o = []
        for a, b in [(ytop, y1 - h), (y1 + h, y2 - h), (y2 + h, ybot)]:
            o.append(f'<rect x="{f(ox + xs_w - 6)}" y="{f(a)}" width="12" height="{f(b - a)}" '
                     f'fill="{G2}" stroke="{BLUE}" stroke-width="{SW * 0.8}"/>')
        return "\n".join(o)

    def graph(ox, I):
        o = [line(ox + xs_gr, ytop, ox + xs_gr, ybot, stroke=G3, sw=SW)]
        o.append(polyline([(ox + xs_gr + 72 * v, y) for v, y in zip(I, ys)], stroke=BLUE, sw=SW))
        return "\n".join(o)

    # ---------------- chap ustun: zarrachalar ----------------
    ox = 22
    g = []
    # trayektoriyalar
    for sl in (-1, 1):
        ysl = yc + sl * DSL / 2
        for dy in (-3.5, 0, 3.5):
            yy = ysl + dy
            k = (yy - yc) / (xs_w - xs_src)
            yend = yc + k * (xs_scr - xs_src)
            g.append(line(ox + xs_src, yc, ox + xs_scr, yend, stroke=G4, sw=SW * 0.8))
            for t in (0.25, 0.55, 0.8):
                x = xs_src + t * (xs_scr - xs_src)
                g.append(circle(ox + x, yc + k * (x - xs_src), 5.5, fill=BLUE, stroke=None, sw=0))
    for yy in (yc - 110, yc + 85, yc - 12):     # devorga urilganlar
        k = (yy - yc) / (xs_w - xs_src)
        g.append(line(ox + xs_src, yc, ox + xs_w - 7, yy, stroke=G4, sw=SW * 0.8))
        g.append(circle(ox + xs_w - 14, yy - k * 7, 5.5, fill=BLUE, stroke=None, sw=0,
                        extra=' opacity="0.55"'))
    yb = yc + (DSL / 2) * (xs_scr - xs_src) / (xs_w - xs_src)
    Ip = np.exp(-((ys - (2 * yc - yb)) / 17) ** 2) + np.exp(-((ys - yb) / 17) ** 2)
    Ip /= Ip.max()
    g.append(wall(ox))
    g.append(screen_strip(ox + xs_scr - 10, ytop, ybot, Ip))
    g.append(graph(ox, Ip))
    # manba (to'p otuvchi)
    g.append(f'<rect x="{ox + xs_src - 34}" y="{yc - 20}" width="44" height="40" rx="6" '
             f'fill="{G1}" stroke="{BLUE}" stroke-width="{SW}"/>')
    g.append(f'<rect x="{ox + xs_src + 8}" y="{yc - 8}" width="16" height="16" fill="{G1}" '
             f'stroke="{BLUE}" stroke-width="{SW}"/>')
    art.append('<g id="zarrachalar">' + "\n".join(g) + '</g>')

    # ---------------- o'ng ustun: to'lqinlar ----------------
    ox = 590
    g = []
    clip_in = f'<clipPath id="kirish"><rect x="{ox + xs_src}" y="{ytop}" width="{xs_w - xs_src - 6}" height="{ybot - ytop}"/></clipPath>'
    clip_out = f'<clipPath id="chiqish"><rect x="{ox + xs_w + 6}" y="{ytop}" width="{xs_scr - xs_w - 16}" height="{ybot - ytop}"/></clipPath>'
    g.append(clip_in + clip_out)
    gi = []
    for k in range(1, 11):
        r = k * LAM
        gi.append(circle(ox + xs_src, yc, r, fill="none", stroke=BLUE, sw=1.5))
    g.append('<g clip-path="url(#kirish)" opacity="0.75">' + "\n".join(gi) + '</g>')
    go = []
    for sl in (-1, 1):
        ysl = yc + sl * DSL / 2
        for k in range(1, 17):
            go.append(circle(ox + xs_w, ysl, k * LAM, fill="none", stroke=BLUE, sw=1.4))
    g.append('<g clip-path="url(#chiqish)" opacity="0.55">' + "\n".join(go) + '</g>')
    # yorug' yo'nalishlar: r1 - r2 = m*lambda (giperbolalar)
    for m in range(-3, 4):
        ptsm = []
        for x in np.linspace(xs_w + 8, xs_scr - 10, 50):
            lo, hi = yc - 260, yc + 260
            fn = lambda y: (math.hypot(x - xs_w, y - (yc - DSL / 2)) -
                            math.hypot(x - xs_w, y - (yc + DSL / 2))) - m * LAM
            if fn(lo) * fn(hi) > 0:
                continue
            for _ in range(50):
                md = (lo + hi) / 2
                if fn(lo) * fn(md) <= 0:
                    hi = md
                else:
                    lo = md
            y = (lo + hi) / 2
            if ytop <= y <= ybot:
                ptsm.append((ox + x, y))
        if len(ptsm) > 1:
            g.append(polyline(ptsm, stroke=GOLD, sw=SW, extra=' stroke-dasharray="8 6"'))
    Iw = wave_I(ys, xs_w, xs_scr, yc)
    Iw /= Iw.max()
    g.append(wall(ox))
    g.append(screen_strip(ox + xs_scr - 10, ytop, ybot, Iw))
    g.append(graph(ox, Iw))
    g.append(circle(ox + xs_src, yc, 9, fill=GOLD, stroke=BLUE, sw=SW))
    art.append('<g id="tolqinlar">' + "\n".join(g) + '</g>')

    # ---------------- pastki lenta: elektronlar birma-bir ----------------
    rng = np.random.default_rng(51)
    yy = np.linspace(yc - 205, yc + 205, 4000)
    pdf = wave_I(yy, xs_w, xs_scr, yc)
    cdf = np.cumsum(pdf)
    cdf /= cdf[-1]
    pw, ph, py = 330, 74, 572
    for i, (n, x0) in enumerate([(10, 40), (100, 395), (10000, 750)]):
        art.append(f'<rect x="{x0}" y="{py}" width="{pw}" height="{ph}" fill="{BLUE}"/>')
        u = rng.random(n)
        sx = np.interp(u, cdf, yy)
        px = x0 + (sx - (yc - 205)) / 410 * pw
        pyy = py + 4 + rng.random(n) * (ph - 8)
        dot = 3.4 if n < 1000 else 1.6
        d = "".join(f"M{f(a)},{f(b)}h0" for a, b in zip(px, pyy))
        art.append(f'<path d="{d}" stroke="#FFF4DA" stroke-width="{dot}" stroke-linecap="round" fill="none"/>')
        L.append(text(x0 + pw / 2, py + ph + 36, f"{n:,}".replace(",", " ") , anchor="middle"))

    # yozuvlar
    L.append(text(22 + xs_src + 230, 48, "zarrachalar: 2 yo‘l", anchor="middle", weight="bold"))
    L.append(text(590 + xs_src + 230, 48, "to‘lqinlar: interferensiya", anchor="middle", weight="bold"))
    for ox in (22, 590):
        L.append(text(ox + xs_src - 10, 540, "manba", anchor="middle", size=FS_SMALL))
        L.append(text(ox + xs_w, 540, "ikki tirqish", anchor="middle", size=FS_SMALL))
        L.append(text(ox + xs_scr + 4, 540, "ekran", anchor="middle", size=FS_SMALL))
    return svg_doc(W, H, "Rasm 5.1. Ikki tirqishli tajriba", "\n".join(art), "\n".join(L))


# =========================================================================
# Rasm 5.2 — Shryodinger mushugi
# =========================================================================
def trefoil(cx, cy, r, fg=BLUE, bg=GOLD):
    o = [circle(cx, cy, r, fill=bg, stroke=fg, sw=SW * 0.8)]
    for k in range(3):
        a = math.radians(-90 + 120 * k)
        a0, a1 = a - math.radians(30), a + math.radians(30)
        r0, r1 = r * 0.24, r * 0.86
        d = (f"M{f(cx + r0 * math.cos(a0))},{f(cy + r0 * math.sin(a0))} "
             f"L{f(cx + r1 * math.cos(a0))},{f(cy + r1 * math.sin(a0))} "
             f"A{f(r1)},{f(r1)} 0 0 1 {f(cx + r1 * math.cos(a1))},{f(cy + r1 * math.sin(a1))} "
             f"L{f(cx + r0 * math.cos(a1))},{f(cy + r0 * math.sin(a1))} Z")
        o.append(path(d, fill=fg, stroke=None, sw=0))
    o.append(circle(cx, cy, r * 0.15, fill=fg, stroke=None, sw=0))
    return "\n".join(o)


def cat(cx, base, s=1.0, color=G3):
    """O'tirgan mushuk (old tomondan), qiziquvchan, sodda."""
    o = []
    body_c = (cx, base - 62 * s)
    # dum
    o.append(path(f"M{f(cx + 48 * s)},{f(base - 18 * s)} C{f(cx + 105 * s)},{f(base - 10 * s)} "
                  f"{f(cx + 100 * s)},{f(base - 92 * s)} {f(cx + 80 * s)},{f(base - 120 * s)}",
                  stroke=color, sw=15 * s))
    o.append(ellipse(body_c[0], body_c[1], 58 * s, 66 * s, fill=color, stroke=None, sw=0))
    o.append(ellipse(cx, base - 58 * s, 27 * s, 44 * s, fill=CREAM, stroke=None, sw=0))
    for dx in (-21, 21):
        o.append(ellipse(cx + dx * s, base - 6 * s, 17 * s, 10 * s, fill=CREAM, stroke=G2, sw=SW * 0.6))
    hc = (cx, base - 150 * s)
    for sg in (-1, 1):
        ear = [(hc[0] + sg * 18 * s, hc[1] - 34 * s), (hc[0] + sg * 40 * s, hc[1] - 70 * s),
               (hc[0] + sg * 44 * s, hc[1] - 18 * s)]
        o.append(polygon(ear, fill=color, stroke=None, sw=0))
        ear_in = [(hc[0] + sg * 24 * s, hc[1] - 32 * s), (hc[0] + sg * 38 * s, hc[1] - 58 * s),
                  (hc[0] + sg * 40 * s, hc[1] - 26 * s)]
        o.append(polygon(ear_in, fill=mix(CREAM, ACCENT, 0.25), stroke=None, sw=0))
    o.append(ellipse(hc[0], hc[1], 47 * s, 42 * s, fill=color, stroke=None, sw=0))
    # peshonadagi chiziqlar
    for dx in (-9, 0, 9):
        o.append(line(hc[0] + dx * s, hc[1] - 40 * s, hc[0] + dx * 0.8 * s, hc[1] - 28 * s, stroke=G2, sw=SW * 1.2))
    o.append(ellipse(hc[0], hc[1] + 16 * s, 22 * s, 15 * s, fill=CREAM, stroke=None, sw=0))
    for sg in (-1, 1):
        o.append(ellipse(hc[0] + sg * 17 * s, hc[1] - 6 * s, 10 * s, 12 * s, fill=WHITE, stroke=G1, sw=SW * 0.6))
        o.append(circle(hc[0] + sg * 16 * s, hc[1] - 11 * s, 5.5 * s, fill="#111111", stroke=None, sw=0))
        o.append(circle(hc[0] + sg * 14.5 * s, hc[1] - 13 * s, 1.8 * s, fill=WHITE, stroke=None, sw=0))
        for k in (-1, 0, 1):
            o.append(line(hc[0] + sg * 20 * s, hc[1] + 16 * s + k * 5 * s, hc[0] + sg * 58 * s,
                          hc[1] + 12 * s + k * 11 * s, stroke=G1, sw=SW * 0.5))
    o.append(polygon([(hc[0] - 6 * s, hc[1] + 7 * s), (hc[0] + 6 * s, hc[1] + 7 * s), (hc[0], hc[1] + 14 * s)],
                     fill=ACCENT, stroke=None, sw=0))
    o.append(path(f"M{f(hc[0] - 9 * s)},{f(hc[1] + 21 * s)} q{f(4.5 * s)},{f(5 * s)} {f(9 * s)},0 "
                  f"q{f(4.5 * s)},{f(5 * s)} {f(9 * s)},0", stroke=G1, sw=SW * 0.8))
    return "\n".join(o)


def rasm_5_2():
    W, H = 540, 640
    art, L = [], []
    D = (78, -62)
    x0, x1, yb_, yt_ = 18, 410, 532, 312   # old yuz
    fbl, fbr, ftr, ftl = (x0, yb_), (x1, yb_), (x1, yt_), (x0, yt_)
    add = lambda p: (p[0] + D[0], p[1] + D[1])
    bbl, bbr, btr, btl = add(fbl), add(fbr), add(ftr), add(ftl)
    wood = mix(CREAM, GOLD, 0.35)
    # qopqoq (orqa yuqori chetda ochilgan)
    lid_h = (25, -190)
    art.append(polygon([btl, btr, (btr[0] + lid_h[0], btr[1] + lid_h[1]), (btl[0] + lid_h[0], btl[1] + lid_h[1])],
                       fill=mix(wood, WHITE, 0.25), stroke=BLUE, sw=SW))
    # ichki yuzalar
    art.append(polygon([bbl, bbr, btr, btl], fill=mix(wood, G2, 0.25), stroke=BLUE, sw=SW))   # orqa devor
    art.append(polygon([fbl, bbl, btl, ftl], fill=mix(wood, G2, 0.45), stroke=BLUE, sw=SW))   # chap devor ichi
    art.append(polygon([fbl, fbr, bbr, bbl], fill=mix(wood, G2, 0.12), stroke=BLUE, sw=SW))   # pol
    # savol belgisi
    art.append(f'<text x="128" y="292" font-family="{FONT}" font-size="150" font-weight="bold" '
               f'text-anchor="middle" fill="{BLUE}" opacity="0.22">?</text>')
    # mushuk
    art.append(cat(118, 508, 0.98))
    # qurilma: tokcha
    sx0, sx1, sy = 236, 400, 430
    # radioaktiv manba
    art.append(ellipse(268, 488, 26, 9, fill=G2, stroke=BLUE, sw=SW))
    art.append(f'<rect x="242" y="470" width="52" height="18" fill="{G2}" stroke="none"/>')
    art.append(line(242, 470, 242, 488, stroke=BLUE, sw=SW))
    art.append(line(294, 470, 294, 488, stroke=BLUE, sw=SW))
    art.append(ellipse(268, 470, 26, 9, fill=G4, stroke=BLUE, sw=SW))
    art.append(trefoil(268, 448, 15))
    # Geyger hisoblagichi
    art.append(f'<rect x="300" y="372" width="86" height="58" rx="6" fill="{BLUE}" stroke="{BLUE}" stroke-width="{SW}"/>')
    art.append(circle(326, 400, 16, fill=CREAM, stroke=G1, sw=SW * 0.8))
    art.append(line(326, 400, 335, 389, stroke=ACCENT, sw=SW))
    art.append(f'<rect x="350" y="388" width="26" height="8" rx="2" fill="{GOLD}"/>')
    art.append(f'<rect x="350" y="402" width="26" height="8" rx="2" fill="{G4}"/>')
    art.append(f'<rect x="279" y="404" width="22" height="12" fill="{G4}" stroke="{BLUE}" stroke-width="{SW * 0.8}"/>')
    art.append(line(282, 416, 276, 430, stroke=G1, sw=SW))   # trubka
    # bolg'acha mexanizmi
    art.append(line(386, 380, 402, 380, stroke=G1, sw=SW * 1.5))
    art.append(circle(404, 380, 5, fill=G1, stroke=None, sw=0))
    art.append(line(404, 380, 386, 448, stroke=G1, sw=SW * 1.8))
    art.append(f'<rect x="368" y="444" width="30" height="16" rx="3" fill="{G2}" stroke="{BLUE}" stroke-width="{SW * 0.8}" '
               f'transform="rotate(-14 383 452)"/>')
    # zahar idishchasi
    vx, vy = 384, 470
    art.append(path(f"M{vx - 9},{vy} L{vx - 9},{vy + 18} Q{vx - 26},{vy + 34} {vx - 22},{vy + 52} "
                    f"L{vx + 22},{vy + 52} Q{vx + 26},{vy + 34} {vx + 9},{vy + 18} L{vx + 9},{vy} Z",
                    fill=mix(WHITE, G4, 0.3), stroke=BLUE, sw=SW))
    art.append(path(f"M{vx - 20},{vy + 36} Q{vx},{vy + 31} {vx + 20},{vy + 36} L{vx + 22},{vy + 52} L{vx - 22},{vy + 52} Z",
                    fill=ACCENT, stroke=None, sw=0))
    art.append(f'<rect x="{vx - 11}" y="{vy - 6}" width="22" height="8" rx="2" fill="{G1}"/>')
    # sim
    art.append(path("M386,420 C420,430 420,380 404,380", stroke=GOLD, sw=SW))
    # old devor (shaffof, faqat chegara) va yuqori chetlar
    art.append(polygon([fbl, fbr, ftr, ftl], fill=mix(wood, WHITE, 0.2), stroke=BLUE, sw=SW,
                       extra=' fill-opacity="0.22"'))
    art.append(polygon([fbr, bbr, btr, ftr], fill=mix(wood, G2, 0.05), stroke=BLUE, sw=SW))   # o'ng devor
    art.append(line(ftl[0], ftl[1], btl[0], btl[1], stroke=BLUE, sw=SW))
    # yozuvlar
    L.append(text(18, 592, "radioaktiv atom"))
    L.append(leader([(110, 572), (110, 556), (250, 556), (258, 500)]))
    L.append(text(W - 18, 592, "zahar", anchor="end"))
    L.append(leader([(W - 50, 572), (W - 50, 556), (vx + 4, vy + 44)]))
    L.append(text(W - 18, 630, "hisoblagich", anchor="end"))
    L.append(leader([(W - 170, 620), (W - 190, 620), (W - 190, 556), (338, 426)]))
    return svg_doc(W, H, "Rasm 5.2. Shryodinger mushugi", "\n".join(art), "\n".join(L))


# =========================================================================
# Rasm 5.3 — Tarmoqlanuvchi olamlar
# =========================================================================
def small_box(cx, cy, s=1.0, open_=False, content=None):
    D = (12 * s, -9 * s)
    w, h = 30 * s, 22 * s
    fl, fr = (cx - w / 2, cy + h / 2), (cx + w / 2, cy + h / 2)
    tl, tr = (cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2)
    add = lambda p: (p[0] + D[0], p[1] + D[1])
    wood = mix(CREAM, GOLD, 0.45)
    o = []
    if open_:
        o.append(polygon([add(tl), add(tr), (add(tr)[0] + 3 * s, add(tr)[1] - 18 * s),
                          (add(tl)[0] + 3 * s, add(tl)[1] - 18 * s)], fill=mix(wood, WHITE, 0.3), stroke=BLUE, sw=SW * 0.8))
        o.append(polygon([tl, tr, add(tr), add(tl)], fill=mix(wood, G1, 0.45), stroke=BLUE, sw=SW * 0.8))
        if content:
            o.append(content)
    else:
        o.append(polygon([tl, tr, add(tr), add(tl)], fill=mix(wood, WHITE, 0.3), stroke=BLUE, sw=SW * 0.8))
    o.append(polygon([fr, add(fr), add(tr), tr], fill=mix(wood, G2, 0.25), stroke=BLUE, sw=SW * 0.8))
    o.append(polygon([fl, fr, tr, tl], fill=wood, stroke=BLUE, sw=SW * 0.8))
    return "\n".join(o)


def cat_head(cx, cy, s=1.0):
    o = []
    for sg in (-1, 1):
        o.append(polygon([(cx + sg * 5 * s, cy - 8 * s), (cx + sg * 11 * s, cy - 19 * s), (cx + sg * 12 * s, cy - 3 * s)],
                         fill=G3, stroke=None, sw=0))
    o.append(ellipse(cx, cy, 13 * s, 11 * s, fill=G3, stroke=None, sw=0))
    for sg in (-1, 1):
        o.append(circle(cx + sg * 5 * s, cy - 2 * s, 2.6 * s, fill=WHITE, stroke=None, sw=0))
        o.append(circle(cx + sg * 5 * s, cy - 2.6 * s, 1.4 * s, fill="#111111", stroke=None, sw=0))
    o.append(polygon([(cx - 1.8 * s, cy + 3 * s), (cx + 1.8 * s, cy + 3 * s), (cx, cy + 5 * s)], fill=ACCENT, stroke=None, sw=0))
    return "\n".join(o)


def rasm_5_3():
    W, H = 1120, 700
    rng = np.random.default_rng(53)
    art, L = [], []
    # daraxt tuzilishi
    xs = [70, 255, 420, 618, 840, 1080]

    class N:
        def __init__(self, d):
            self.d, self.kids, self.y = d, [], None

    root = N(0)
    m1 = N(1)
    root.kids = [m1]
    up, down = N(2), N(2)
    m1.kids = [up, down]

    def grow(node, depth):
        if depth >= len(xs) - 1:
            return
        k = 2 if depth >= 4 else int(rng.choice([2, 3], p=[0.4, 0.6]))
        node.kids = [N(depth + 1) for _ in range(k)]
        for c in node.kids:
            grow(c, depth + 1)

    grow(up, 2)
    grow(down, 2)

    leaves = []
    def collect(n):
        if not n.kids:
            leaves.append(n)
        for c in n.kids:
            collect(c)
    collect(root)
    y0, y1 = 40, 625
    for i, lf in enumerate(leaves):
        lf.y = y0 + (y1 - y0) * i / (len(leaves) - 1)

    def place(n):
        if n.kids:
            for c in n.kids:
                place(c)
            n.y = sum(c.y for c in n.kids) / len(n.kids)
    place(root)
    root.y = m1.y
    widths = [10, 10, 7.5, 5.2, 3.6, 2.5]
    br = []

    def draw(n):
        for c in n.kids:
            x0_, x1_ = xs[n.d], xs[c.d]
            col = mix(BLUE, WHITE, 0.08 * c.d)
            br.append(path(f"M{f(x0_)},{f(n.y)} C{f(x0_ + (x1_ - x0_) * 0.55)},{f(n.y)} "
                           f"{f(x0_ + (x1_ - x0_) * 0.45)},{f(c.y)} {f(x1_)},{f(c.y)}",
                           stroke=col, sw=widths[c.d]))
            draw(c)
    draw(root)
    art.append('<g id="shoxlar">' + "\n".join(br) + '</g>')
    nodes = []

    def dots(n):
        if 2 <= n.d <= 3 and n.kids:
            nodes.append(circle(xs[n.d], n.y, widths[n.d] * 0.9 + 2, fill=GOLD, stroke=None, sw=0))
        if not n.kids:
            nodes.append(circle(xs[n.d], n.y, 4.5, fill=BLUE, stroke=None, sw=0))
        for c in n.kids:
            dots(c)
    dots(root)
    art.append("\n".join(nodes))
    # ildiz: olam (doira ichida sayyora)
    art.append(circle(xs[0], root.y, 38, fill=CREAM, stroke=BLUE, sw=SW))
    art.append(circle(xs[0], root.y, 16, fill="url(#sayyora)", stroke=BLUE, sw=SW * 0.8))
    art.append(ellipse(xs[0], root.y, 27, 7, fill="none", stroke=GOLD, sw=SW * 1.2,
                       extra=f' transform="rotate(-18 {xs[0]} {f(root.y)})"'))
    # birinchi o'lchov: yopiq quti
    art.append(circle(xs[1], m1.y, 34, fill=WHITE, stroke=GOLD, sw=SW * 1.2))
    art.append(small_box(xs[1] - 4, m1.y + 6, 1.25))
    # ikki natija
    bx = (xs[1] + xs[2]) / 2 + 10
    def ybez(n0, n1, t=0.5):
        return (1 - t) ** 3 * n0 + 3 * (1 - t) ** 2 * t * n0 + 3 * (1 - t) * t * t * n1 + t ** 3 * n1
    yu = ybez(m1.y, up.y)
    yd = ybez(m1.y, down.y)
    art.append(circle(bx, yu, 30, fill=WHITE, stroke=BLUE, sw=SW))
    art.append(small_box(bx - 3, yu + 9, 1.05, open_=True, content=cat_head(bx + 2, yu - 6, 0.9)))
    art.append(circle(bx, yd, 30, fill=WHITE, stroke=BLUE, sw=SW))
    art.append(small_box(bx - 3, yd + 9, 1.05, open_=True))
    defs = f"""<radialGradient id="sayyora" cx="0.35" cy="0.35" r="0.8">
  <stop offset="0" stop-color="{mix(BLUE, WHITE, 0.55)}"/><stop offset="1" stop-color="{BLUE}"/></radialGradient>"""
    L.append(text(xs[1] - 52, m1.y + 72, "kvant o‘lchov", anchor="middle"))
    L.append(text(W - 20, H - 20, "vaqt →", anchor="end"))
    return svg_doc(W, H, "Rasm 5.3. Tarmoqlanuvchi olamlar", "\n".join(art), "\n".join(L), defs)


if __name__ == "__main__":
    which = sys.argv[1:] or ["5-1", "5-2", "5-3"]
    for w in which:
        save(f"rasm_{w}.svg", globals()["rasm_" + w.replace("-", "_")]())
