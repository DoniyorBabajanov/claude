"""II bob — Fazo va vaqt: rasmlar 2.1–2.4"""
import math
import numpy as np
from common import *

SKIN = mix(CREAM, GOLD, 0.30)
SHOE = G1


# =========================================================================
# Rasm 2.1 — Odamning "to'rt o'lchamli tasviri"
# =========================================================================
def _limb(points, color, width):
    return polyline(points, stroke=color, sw=width,
                    extra=' stroke-linejoin="round"')


def _ang(deg):
    # vertikaldan (pastga) burchak; musbat — oldinga (+x)
    a = math.radians(deg)
    return math.sin(a), math.cos(a)


def _hair(cx, cy, r, a_from, a_to, color, grow=1.07):
    """Soch: bosh aylanasining a_from..a_to yoyi (gradus; 0 = tepa, musbat =
    oldinga) va boshning orqa qismiga egilgan ichki chegara."""
    n = 30
    outer = []
    for i in range(n + 1):
        a = math.radians(a_from + (a_to - a_from) * i / n)
        outer.append((cx + r * grow * math.sin(a), cy - r * grow * math.cos(a)))
    (ex, ey), (sx, sy) = outer[-1], outer[0]
    qx, qy = cx - 0.10 * r, cy + 0.02 * r
    inner = []
    for i in range(1, n):
        t = i / n
        inner.append(((1 - t) ** 2 * ex + 2 * (1 - t) * t * qx + t * t * sx,
                      (1 - t) ** 2 * ey + 2 * (1 - t) * t * qy + t * t * sy))
    return polygon(outer + inner, fill=color, stroke=None, sw=0)


def _pal(mono=None, hair=G1):
    if mono:
        return dict(torso=mono, arm_near=mono, arm_far=mono, leg_near=mono,
                    leg_far=mono, skin=mono, hair=mono, scarf=mono, shoe=mono,
                    eye=mono, cane=mono)
    return dict(torso=BLUE, arm_near=mix(BLUE, CREAM, 0.16),
                arm_far=mix(BLUE, "#000000", 0.30), leg_near=mix(G3, G1, 0.12),
                leg_far=mix(G3, G1, 0.42), skin=SKIN, hair=hair, scarf=GOLD,
                shoe=SHOE, eye=G1, cane=G1)


def walker(x0, y0, H, head=0.135, leg=0.47, arm=0.40, lean=2, head_lean=4,
           stride=24, hair=G1, hair_span=(35, -150), belly=0.0, cane=False,
           scale_w=1.0, mono=None):
    """Yon tomondan ko'rinishdagi yurayotgan odam (o'ngga qaragan).
    (x0, y0) — oyoqlar orasidagi yer nuqtasi."""
    P = _pal(mono, hair)
    r = head * H / 2
    legw = 0.095 * H * scale_w
    armw = 0.072 * H * scale_w
    torw = 0.20 * H * scale_w
    hip_h = leg * H
    T = hip_h * 0.52
    S = hip_h * 0.48
    near_thigh, near_shin = stride, stride * 0.55
    far_thigh, far_shin = -stride * 0.75, -stride * 1.35
    if cane:
        near_thigh, near_shin = stride * 0.8, stride * 0.2
        far_thigh, far_shin = -stride * 0.5, -stride * 0.9

    def leg_pts(th, shn):
        sx, cy_ = _ang(th)
        kx, ky = sx * T, cy_ * T
        sx2, cy2 = _ang(shn)
        return (0, 0), (kx, ky), (kx + sx2 * S, ky + cy2 * S)

    ln = leg_pts(near_thigh, near_shin)
    lf = leg_pts(far_thigh, far_shin)
    foot_drop = max(ln[2][1], lf[2][1])
    hip = (x0, y0 - foot_drop - legw * 0.35)

    def tr(p):
        return (hip[0] + p[0], hip[1] + p[1])

    torso_len = H - 2 * r - hip_h - 0.03 * H
    lx, ly = math.sin(math.radians(lean)), -math.cos(math.radians(lean))
    sh = (hip[0] + lx * torso_len, hip[1] + ly * torso_len)
    neck_len = 0.035 * H
    hx, hy = math.sin(math.radians(head_lean)), -math.cos(math.radians(head_lean))
    neck = (sh[0] + hx * neck_len, sh[1] + hy * neck_len)
    hc = (neck[0] + hx * r * 0.92, neck[1] + hy * r * 0.92)
    px, py = -ly, lx            # oldinga perpendikulyar

    out = []

    def leg_draw(lp, col):
        a, k, an = [tr(p) for p in lp]
        return "\n".join([
            _limb([a, k, an], col, legw),
            _limb([an, (an[0] + 0.075 * H, an[1] + legw * 0.12)], P["shoe"],
                  legw * 0.62)])

    def arm_draw(up, fo, col):
        sx, sy = _ang(up)
        e = (sh[0] + sx * arm * H * 0.5, sh[1] + sy * arm * H * 0.5)
        fx, fy = _ang(fo)
        w = (e[0] + fx * arm * H * 0.46, e[1] + fy * arm * H * 0.46)
        o = [_limb([sh, e, w], col, armw),
             circle(w[0] + fx * armw * 0.25, w[1] + fy * armw * 0.25,
                    armw * 0.56, fill=P["skin"], stroke=None, sw=0)]
        return "\n".join(o), w

    if cane:
        far_arm, _ = arm_draw(-10, 5, P["arm_far"])
    else:
        far_arm, _ = arm_draw(stride * 0.95, stride * 0.95 + 35, P["arm_far"])
    out.append(far_arm)
    out.append(leg_draw(lf, P["leg_far"]))
    out.append(_limb([(hip[0], hip[1] - torw * 0.25),
                      (sh[0] - lx * torw * 0.32, sh[1] - ly * torw * 0.32)],
                     P["torso"], torw))
    if belly > 0:
        bx = hip[0] + lx * torso_len * 0.38 + torw * 0.30
        by = hip[1] + ly * torso_len * 0.38
        out.append(ellipse(bx, by, torw * 0.30 * belly, torw * 0.40, fill=P["torso"],
                           stroke=None, sw=0))
    out.append(leg_draw(ln, P["leg_near"]))
    out.append(_limb([sh, neck], P["skin"], armw * 1.0))
    out.append(circle(hc[0], hc[1], r, fill=P["skin"], stroke=None, sw=0))
    # sharf — har bir yoshda bir xil belgi
    nb = (sh[0] + lx * torw * 0.05, sh[1] + ly * torw * 0.05)
    out.append(_limb([(nb[0] - px * torw * 0.30, nb[1] - py * torw * 0.30),
                      (nb[0] + px * torw * 0.26, nb[1] + py * torw * 0.26)],
                     P["scarf"], armw * 0.62))
    out.append(_limb([(nb[0] - px * torw * 0.26, nb[1] - py * torw * 0.26),
                      (nb[0] - px * torw * 0.52 - lx * torw * 0.42,
                       nb[1] - py * torw * 0.52 - ly * torw * 0.42)],
                     P["scarf"], armw * 0.5))
    out.append(_hair(hc[0], hc[1], r, hair_span[0], hair_span[1], P["hair"]))
    out.append(circle(hc[0] + r * 0.52, hc[1] - r * 0.06, max(2.6, r * 0.09),
                      fill=P["eye"], stroke=None, sw=0))
    out.append(path(f"M{f(hc[0] + r * 0.96)},{f(hc[1] - r * 0.05)} "
                    f"L{f(hc[0] + r * 1.12)},{f(hc[1] + r * 0.17)} "
                    f"L{f(hc[0] + r * 0.93)},{f(hc[1] + r * 0.22)}",
                    fill=P["skin"], stroke=None, sw=0))
    if cane:
        near_arm, w = arm_draw(28, 62, P["arm_near"])
        cane_top = (w[0] + armw * 0.2, w[1] - armw * 0.3)
        cane_bot = (w[0] + 0.07 * H, y0)
        out.insert(0, _limb([cane_top, cane_bot], P["cane"], armw * 0.42))
        out.append(near_arm)
        out.append(path(f"M{f(cane_top[0] - armw * 0.9)},{f(cane_top[1] + armw * 0.15)} "
                        f"Q{f(cane_top[0] - armw * 0.2)},{f(cane_top[1] - armw * 1.1)} "
                        f"{f(cane_top[0] + armw * 0.15)},{f(cane_top[1])}",
                        stroke=P["cane"], sw=armw * 0.42))
    else:
        near_arm, _ = arm_draw(-stride * 0.9, -stride * 0.9 + 28, P["arm_near"])
        out.append(near_arm)
    top = hc[1] - r * 1.1
    return "\n".join(out), top


def crawler(x0, y0, s=1.0):
    """Emaklayotgan chaqaloq (yon ko'rinish), o'ngga qaragan."""
    P = _pal()
    r = 34 * s
    torw = 52 * s
    legw = 26 * s
    armw = 19 * s
    hip = (x0 - 40 * s, y0 - 62 * s)
    sh = (x0 + 30 * s, y0 - 68 * s)
    out = []
    out.append(_limb([(sh[0] - 6 * s, sh[1]), (sh[0] - 14 * s, y0 - armw * 0.5)],
                     P["arm_far"], armw))
    out.append(_limb([(hip[0] + 6 * s, hip[1]), (hip[0] + 12 * s, y0 - legw * 0.5),
                      (hip[0] - 34 * s, y0 - legw * 0.5)], P["leg_far"], legw))
    out.append(_limb([hip, sh], P["torso"], torw))
    out.append(_limb([(hip[0] - 4 * s, hip[1] + 4 * s), (hip[0] + 2 * s, y0 - legw * 0.5),
                      (hip[0] - 44 * s, y0 - legw * 0.45)], P["leg_near"], legw))
    hc = (sh[0] + 34 * s, sh[1] - 34 * s)
    out.append(_limb([sh, (hc[0] - 10 * s, hc[1] + 12 * s)], P["skin"], armw))
    out.append(circle(hc[0], hc[1], r, fill=P["skin"], stroke=None, sw=0))
    out.append(_limb([(sh[0] - 4 * s, sh[1] - 22 * s), (sh[0] + 14 * s, sh[1] - 30 * s)],
                     P["scarf"], armw * 0.62))
    out.append(_limb([(sh[0] - 2 * s, sh[1] - 22 * s), (sh[0] - 18 * s, sh[1] - 6 * s)],
                     P["scarf"], armw * 0.5))
    out.append(_hair(hc[0], hc[1], r, 20, -120, P["hair"], grow=1.04))
    out.append(circle(hc[0] + r * 0.48, hc[1] - r * 0.02, 3.2 * s, fill=P["eye"],
                      stroke=None, sw=0))
    out.append(path(f"M{f(hc[0] + r * 0.98)},{f(hc[1] + r * 0.05)} "
                    f"q{f(r * 0.12)},{f(r * 0.12)} {f(-r * 0.02)},{f(r * 0.22)}",
                    fill=P["skin"], stroke=None, sw=0))
    out.append(_limb([(sh[0] + 4 * s, sh[1]), (sh[0] + 10 * s, y0 - armw * 0.5)],
                     P["arm_near"], armw))
    out.append(circle(sh[0] + 14 * s, y0 - armw * 0.5, armw * 0.58, fill=P["skin"],
                      stroke=None, sw=0))
    return "\n".join(out), hc[1] - r * 1.1


def rasm_2_1():
    W, H = 1120, 500
    ground = 405
    xs = [100, 275, 450, 625, 797, 962]
    cfg = [
        dict(H=215, head=0.20, leg=0.42, arm=0.38, lean=3, head_lean=6, stride=22,
             hair=G1, hair_span=(40, -150)),
        dict(H=300, head=0.15, leg=0.47, arm=0.40, lean=2, head_lean=4, stride=25,
             hair=G1, hair_span=(45, -160)),
        dict(H=345, head=0.135, leg=0.47, arm=0.40, lean=2, head_lean=3, stride=25,
             hair=G1, hair_span=(38, -150)),
        dict(H=340, head=0.135, leg=0.46, arm=0.40, lean=3, head_lean=3, stride=21,
             hair=G2, hair_span=(18, -150), belly=1.0, scale_w=1.06),
        dict(H=318, head=0.14, leg=0.45, arm=0.40, lean=16, head_lean=24, stride=14,
             hair=G4, hair_span=(-25, -150), cane=True),
    ]
    toddler = dict(H=150, head=0.25, leg=0.37, arm=0.36, lean=4, head_lean=6,
                   stride=16)
    num = ["H", "head", "leg", "arm", "lean", "head_lean", "stride"]

    # oraliq "arvoh" siluetlar — vaqt bo'ylab uzluksizlik
    ghosts = []
    chain = [toddler] + cfg
    gx = [xs[0] + 40] + xs[1:]
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i + 1]
        for t in (1 / 3, 2 / 3):
            c = {k: lerp(a[k], b[k], t) for k in num}
            x = lerp(gx[i], gx[i + 1], t)
            g, _ = walker(x, ground, mono=BLUE, **c)
            ghosts.append(g)

    stages = [crawler(xs[0], ground, 1.0)]
    for x, c in zip(xs[1:], cfg):
        stages.append(walker(x, ground, **c))

    tops = [t for _, t in stages]
    kx = [20] + xs + [1100]
    ky = [ground - 60] + [t - 14 for t in tops] + [tops[-1] + 10]
    xx = np.linspace(20, 1100, 140)

    def cr(x):
        i = max(0, min(len(kx) - 2, int(np.searchsorted(kx, x) - 1)))
        t = (x - kx[i]) / (kx[i + 1] - kx[i])
        p0 = ky[max(i - 1, 0)]; p1 = ky[i]; p2 = ky[i + 1]; p3 = ky[min(i + 2, len(ky) - 1)]
        return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t +
                      (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
    topline = [(x, cr(x)) for x in xx]
    band = topline + [(1100, ground + 8), (20, ground + 8)]
    defs = f'''<linearGradient id="lentaFill" x1="20" y1="0" x2="1100" y2="0" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="{CREAM}" stop-opacity="0"/>
  <stop offset="0.07" stop-color="{CREAM}" stop-opacity="1"/>
  <stop offset="0.93" stop-color="{CREAM}" stop-opacity="1"/>
  <stop offset="1" stop-color="{CREAM}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="lentaEdge" x1="20" y1="0" x2="1100" y2="0" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>
  <stop offset="0.08" stop-color="{GOLD}" stop-opacity="1"/>
  <stop offset="0.92" stop-color="{GOLD}" stop-opacity="1"/>
  <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</linearGradient>'''
    art = ['<g id="lenta">',
           polygon(band, fill="url(#lentaFill)", stroke=None, sw=0),
           polyline(topline, stroke="url(#lentaEdge)", sw=SW,
                    extra=' stroke-dasharray="10 9"'),
           '</g>',
           line(30, ground + 8, 1090, ground + 8, stroke=G4, sw=SW)]
    art.append('<g id="oraliq-siluetlar" opacity="0.13">')
    art += ghosts
    art.append('</g>')
    art.append('<g id="siluetlar">')
    for a, _ in stages:
        art.append(f'<g opacity="0.86">{a}</g>')
    art.append('</g>')
    art.append(arrow(60, 448, 1062, 448, stroke=BLUE, sw=SW, head=20))
    labels = text(560, 488, "vaqt (t)", anchor="middle")
    return svg_doc(W, H, "Rasm 2.1. Odamning “to‘rt o‘lchamli tasviri”",
                   "\n".join(art), labels, defs)


if __name__ == "__main__":
    save("rasm_2-1.svg", rasm_2_1())
