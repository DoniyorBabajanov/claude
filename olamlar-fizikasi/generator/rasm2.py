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



# =========================================================================
# Rasm 2.2 — Egrilangan fazo-vaqt: rezina choyshab modeli
# =========================================================================
class Cam:
    def __init__(self, pos, target, focal=1.0):
        self.C = np.array(pos, float)
        fw = np.array(target, float) - self.C
        self.f = fw / np.linalg.norm(fw)
        r = np.cross(self.f, [0, 0, 1.0])
        self.r = r / np.linalg.norm(r)
        self.u = np.cross(self.r, self.f)
        self.focal = focal

    def proj(self, P):
        P = np.asarray(P, float)
        v = P - self.C
        z = v @ self.f
        return np.stack([(v @ self.r) / z, -(v @ self.u) / z], axis=-1) * self.focal

    def ray(self, sx, sy):
        d = self.f + (sx / self.focal) * self.r - (sy / self.focal) * self.u
        return d / np.linalg.norm(d, axis=-1, keepdims=True)


def rasm_2_2():
    W, H = 1120, 700
    L, R0, s, A = 10.0, 8.6, 1.05, 6.2

    def zf(x, y):
        r = np.sqrt(x * x + y * y)
        g = 1 / np.sqrt(1 + (r / s) ** 2)
        w = np.clip(1 - (r / R0) ** 2, 0, None) ** 2
        return -A * g * w

    cam = Cam((0, -19.5, 14.8), (0, 1.6, -2.2))
    Rs = 2.15
    rr_ = np.linspace(0, Rs * 0.999, 400)
    sun_c = np.array([0, 0, np.max(zf(rr_, 0 * rr_) + np.sqrt(Rs ** 2 - rr_ ** 2)) - 0.05])
    re, th_e = 4.0, math.radians(150)
    Re = 0.62
    earth_c = np.array([re * math.cos(th_e), re * math.sin(th_e),
                        zf(re * math.cos(th_e), re * math.sin(th_e)) + Re * 0.9])

    def occluded(P, extra_spheres=True):
        """P: (N,3). Kameradan P gacha nur sirt yoki Quyosh bilan to'silganmi."""
        C = cam.C
        n = P.shape[0]
        ts = np.linspace(0.02, 0.985, 160)
        Q = C[None, None, :] + ts[None, :, None] * (P[:, None, :] - C[None, None, :])
        surf = zf(Q[..., 0], Q[..., 1])
        hid = np.any(Q[..., 2] < surf - 0.02, axis=1)
        if extra_spheres:
            for c, rr in ((sun_c, Rs),):
                d = P - C
                dn = np.linalg.norm(d, axis=1)
                dh = d / dn[:, None]
                oc = C - c
                b = dh @ oc
                cc = oc @ oc - rr * rr
                disc = b * b - cc
                t1 = -b - np.sqrt(np.clip(disc, 0, None))
                hid |= (disc > 0) & (t1 > 0) & (t1 < dn - 0.05)
        return hid

    # proyeksiya -> kanvas masshtabi
    LY0, LY1 = -L, L + 4
    corners = np.array([[-L, LY0, 0], [L, LY0, 0], [L, LY1, 0], [-L, LY1, 0]])
    gx_, gy_ = np.meshgrid(np.linspace(-L, L, 60), np.linspace(LY0, LY1, 60))
    allp = np.stack([gx_.ravel(), gy_.ravel(), zf(gx_.ravel(), gy_.ravel())], 1)
    pc = cam.proj(np.vstack([allp, sun_c[None, :] + [0, 0, Rs]]))
    minx, maxx = pc[:, 0].min(), pc[:, 0].max()
    miny, maxy = pc[:, 1].min(), pc[:, 1].max()
    sc = min((W - 30) / (maxx - minx), (H - 70) / (maxy - miny))
    ox = W / 2 - (minx + maxx) / 2 * sc
    oy = 75 + (H - 95 - (maxy - miny) * sc) / 2 - miny * sc

    def S(P):
        p = cam.proj(P)
        return np.stack([ox + p[..., 0] * sc, oy + p[..., 1] * sc], axis=-1)

    art = []
    # choyshab foni
    cs = S(corners)
    art.append(polygon([tuple(p) for p in cs], fill="url(#choyshab)", stroke=BLUE, sw=SW))
    # chuqurcha soyasi
    sh_c = S(np.array([[0, 0, zf(0, 0) * 0.35]]))[0]
    art.append(ellipse(sh_c[0], sh_c[1] + 10, 330, 120, fill="url(#botiq)", stroke=None, sw=0))

    # Quyosh (oldingi chet bilan qirqilgan)
    scc = S(sun_c[None, :])[0]
    # proyeksiyadagi radius
    edge = sun_c + Rs * cam.r
    srad = np.linalg.norm(S(edge[None, :])[0] - scc)
    xs_ = np.linspace(scc[0] - srad - 2, scc[0] + srad + 2, 90)
    bottom = []
    for X in xs_:
        ys_ = np.linspace(scc[1] - srad - 2, scc[1] + srad + 2, 160)
        sx = (X - ox) / sc
        vis_low = None
        for Y in ys_:
            sy = (Y - oy) / sc
            d = cam.ray(np.array([sx]), np.array([sy]))[0] if False else None
            dd = cam.f + sx * cam.r - sy * cam.u
            dd /= np.linalg.norm(dd)
            oc = cam.C - sun_c
            b = dd @ oc
            disc = b * b - (oc @ oc - Rs * Rs)
            if disc <= 0:
                continue
            t1 = -b - math.sqrt(disc)
            ts = np.linspace(0.05, t1 - 0.02, 120)
            Q = cam.C[None, :] + ts[:, None] * dd[None, :]
            if np.any(Q[:, 2] < zf(Q[:, 0], Q[:, 1]) - 0.01):
                continue
            vis_low = Y
        bottom.append((X, vis_low if vis_low is not None else scc[1] - srad - 3))
    clip = [(scc[0] - srad - 5, scc[1] - srad - 10)] + bottom + \
           [(scc[0] + srad + 5, scc[1] - srad - 10)]
    art.append(f'<clipPath id="quyoshKlip"><polygon points="{pts(clip)}"/></clipPath>')
    art.append(f'<g clip-path="url(#quyoshKlip)">' +
               circle(scc[0], scc[1], srad, fill="url(#quyosh)", stroke=GOLD, sw=SW) +
               '</g>')

    # to'r chiziqlari
    grid = []
    for orient in (0, 1):
        vals = np.arange(LY0, LY1 + 0.01, 1.0) if orient == 0 else np.arange(-L, L + 0.01, 1.0)
        samp = np.linspace(-L, L, 420) if orient == 0 else np.linspace(LY0, LY1, 480)
        for v in vals:
            if orient == 0:
                P = np.stack([samp, np.full_like(samp, v), np.zeros_like(samp)], 1)
            else:
                P = np.stack([np.full_like(samp, v), samp, np.zeros_like(samp)], 1)
            P[:, 2] = zf(P[:, 0], P[:, 1])
            hid = occluded(P)
            sp = S(P)
            seg = []
            for j in range(len(samp)):
                if not hid[j]:
                    seg.append(tuple(sp[j]))
                else:
                    if len(seg) > 1:
                        grid.append(seg)
                    seg = []
            if len(seg) > 1:
                grid.append(seg)
    art.append('<g id="setka" fill="none" stroke="%s" stroke-width="1.9" '
               'stroke-linecap="round" stroke-linejoin="round">' % BLUE)
    for seg in grid:
        art.append(f'<polyline points="{pts(seg)}"/>')
    art.append('</g>')

    # orbita (punktir)
    th = np.linspace(0, 2 * np.pi, 400)
    P = np.stack([re * np.cos(th), re * np.sin(th), np.zeros_like(th)], 1)
    P[:, 2] = zf(P[:, 0], P[:, 1]) + 0.25
    hid = occluded(P)
    sp = S(P)
    orb = []
    seg = []
    for j in range(len(th)):
        if not hid[j]:
            seg.append(tuple(sp[j]))
        else:
            if len(seg) > 1:
                orb.append(seg)
            seg = []
    if len(seg) > 1:
        orb.append(seg)
    for seg in orb:
        art.append(polyline(seg, stroke=ACCENT, sw=SW, extra=' stroke-dasharray="11 9"'))
    # Yer
    ec = S(earth_c[None, :])[0]
    erad = np.linalg.norm(S((earth_c + Re * cam.r)[None, :])[0] - ec)
    art.append(circle(ec[0], ec[1], erad, fill="url(#yer)", stroke=BLUE, sw=SW))
    # harakat yo'nalishi (kichik strelka orbita ustida)
    j0 = int(np.argmin(np.abs(th - (th_e - 0.55))))
    a1, a2 = sp[j0], sp[j0 - 6]
    art.append(arrow_head(a2[0], a2[1], math.atan2(a2[1] - a1[1], a2[0] - a1[0]), 17, ACCENT))

    defs = f"""<linearGradient id="choyshab" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{mix(CREAM, WHITE, 0.6)}"/>
</linearGradient>
<radialGradient id="botiq"><stop offset="0" stop-color="{mix(CREAM, GOLD, 0.35)}"/>
  <stop offset="0.6" stop-color="{mix(CREAM, GOLD, 0.12)}"/><stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></radialGradient>
<radialGradient id="quyosh" cx="0.38" cy="0.35" r="0.75"><stop offset="0" stop-color="{mix(GOLD, CREAM, 0.75)}"/>
  <stop offset="0.55" stop-color="{mix(GOLD, CREAM, 0.25)}"/><stop offset="1" stop-color="{GOLD}"/></radialGradient>
<radialGradient id="yer" cx="0.35" cy="0.35" r="0.8"><stop offset="0" stop-color="{mix(BLUE, WHITE, 0.55)}"/>
  <stop offset="1" stop-color="{BLUE}"/></radialGradient>"""

    labels = []
    tr_ = cs[2]          # yuqori o'ng burchak (uzoq chet)
    br_ = cs[1]
    def edge_x(y):       # o'ng chetning y dagi x koordinatasi
        t = (y - tr_[1]) / (br_[1] - tr_[1])
        return tr_[0] + t * (br_[0] - tr_[0])
    y1 = tr_[1] + 70
    y1 = tr_[1] + 110
    labels.append(text(edge_x(y1 - 10) + 28, y1, "Quyosh"))
    labels.append(leader([(edge_x(y1 - 10) + 18, y1 - 10), (scc[0] + srad * 0.9, y1 - 10),
                          (scc[0] + srad * 0.42, scc[1] - srad * 0.5)]))
    q = S(np.array([[6.2, -3.4, zf(6.2, -3.4)]]))[0]
    y2 = tr_[1] - 2
    labels.append(text(W - 12, y2 - 6, "egrilangan fazo", anchor="end"))
    labels.append(leader([(W - 160, y2 + 6), (W - 160, y2 + 40), q]))

    tl_ = cs[3]
    labels.append(text(tl_[0] - 30, tl_[1] + 100, "Yer", anchor="end"))
    labels.append(leader([(tl_[0] - 22, tl_[1] + 90), (ec[0] - erad * 0.72, ec[1] - erad * 0.72)]))
    return svg_doc(W, H, "Rasm 2.2. Egrilangan fazo-vaqt: rezina choyshab modeli",
                   "\n".join(art), "\n".join(labels), defs)



# =========================================================================
# Rasm 2.3 — Qora tuynuk va uning "soyasi"
# =========================================================================
def glow_color(b):
    """Yorqinlik 0..1 -> rang (qorong'i -> oltin -> qaymoq)."""
    stops = [(0.0, NIGHT), (0.30, mix(GOLD, NIGHT, 0.55)), (0.62, GOLD),
             (0.85, mix(GOLD, CREAM, 0.6)), (1.0, "#FFF9EC")]
    b = max(0.0, min(1.0, b))
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if b <= t1:
            return mix(c0, c1, (b - t0) / (t1 - t0))
    return stops[-1][1]


def rasm_2_3():
    W = H = 540
    cx, cy = 270, 268
    rng = np.random.default_rng(23)
    N = 180
    th = np.linspace(0, 2 * np.pi, N, endpoint=False)
    # notekislik: bir nechta garmonika
    ph = rng.uniform(0, 2 * np.pi, 6)
    def harm(t, amp):
        return sum(amp / (k + 1) * np.sin((k + 2) * t + ph[k]) for k in range(5))
    bright = 0.55 + 0.45 * np.clip(np.sin(th) * 0.9 + 0.25, 0, None) ** 1.3 / 1.15 ** 1.3
    bright = bright * (1 + 0.22 * harm(th, 1.0)) 
    bright = np.clip(bright, 0.15, 1.0)
    rin = 110 + 3 * harm(th + 1, 1.0)
    width = 40 + 16 * np.clip(np.sin(th), 0, None) + 6 * harm(th + 2, 1.0)
    art = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{NIGHT}"/>']
    dth = 2 * np.pi / N * 0.62
    layers = [(0.0, 0.45, 1.0), (0.42, 1.0, 0.75), (1.0, 1.7, 0.36)]
    art.append('<g filter="url(#yumshoq)">')
    for a0, a1, k in layers[::-1]:
        for j in range(N):
            t = th[j]
            r0 = rin[j] + width[j] * a0
            r1 = rin[j] + width[j] * a1
            p = [(cx + r0 * math.cos(t - dth), cy + r0 * math.sin(t - dth)),
                 (cx + r1 * math.cos(t - dth), cy + r1 * math.sin(t - dth)),
                 (cx + r1 * math.cos(t + 2 * dth), cy + r1 * math.sin(t + 2 * dth)),
                 (cx + r0 * math.cos(t + 2 * dth), cy + r0 * math.sin(t + 2 * dth))]
            art.append(polygon(p, fill=glow_color(bright[j] * k), stroke=None, sw=0))
    art.append('</g>')
    # soya
    art.append(circle(cx, cy, 104, fill="url(#soya)", stroke=None, sw=0))
    defs = f"""<filter id="yumshoq" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="9"/></filter>
<radialGradient id="soya"><stop offset="0" stop-color="#000000"/><stop offset="0.86" stop-color="#020407"/>
  <stop offset="1" stop-color="#05080D" stop-opacity="0"/></radialGradient>"""
    L = []
    c = CREAM
    L.append(text_lines(18, 40, ["yorug‘ halqa", "(qizigan gaz)"], fill=c))
    L.append(leader([(110, 82), (110, 108), (cx - 150 * 0.72, cy - 150 * 0.62)], stroke=c))
    L.append(text_lines(W - 18, 40, ["qora tuynuk", "soyasi"], anchor="end", fill=c))
    L.append(leader([(W - 70, 82), (W - 70, 108), (cx + 22, cy - 18)], stroke=c))
    return svg_doc(W, H, "Rasm 2.3. Qora tuynuk va uning “soyasi”", "\n".join(art),
                   "\n".join(L), defs,
                   desc="Rassomning o‘z chizmasi; EHT suratidan nusxa ko‘chirilmagan.")


# =========================================================================
# Rasm 2.4 — Fazo-vaqt tuneli: buklangan qog'oz
# =========================================================================
def pencil(x, y_top, y_tip, w=30):
    """Vertikal qalam (uchi pastda). Bo'laklarga ajratib chizish uchun
    (kesish oralig'i bilan) elementlar ro'yxatini qaytaradi."""
    cone = 62
    body_bot = y_tip - cone
    o = []
    o.append(f'<rect x="{f(x - w / 2)}" y="{f(y_top)}" width="{f(w)}" height="{f(24)}" '
             f'rx="6" fill="{ACCENT}" stroke="{BLUE}" stroke-width="{SW}"/>')
    o.append(f'<rect x="{f(x - w / 2)}" y="{f(y_top + 20)}" width="{f(w)}" height="{f(20)}" '
             f'fill="{G4}" stroke="{BLUE}" stroke-width="{SW}"/>')
    o.append(f'<rect x="{f(x - w / 2)}" y="{f(y_top + 40)}" width="{f(w)}" '
             f'height="{f(body_bot - y_top - 40)}" fill="{GOLD}" stroke="{BLUE}" stroke-width="{SW}"/>')
    o.append(line(x - w / 6, y_top + 42, x - w / 6, body_bot - 2, stroke=mix(GOLD, CREAM, 0.45),
                  sw=SW))
    o.append(line(x + w / 6, y_top + 42, x + w / 6, body_bot - 2, stroke=mix(GOLD, "#000000", 0.25),
                  sw=SW))
    o.append(polygon([(x - w / 2, body_bot), (x + w / 2, body_bot), (x, y_tip)],
                     fill=mix(CREAM, GOLD, 0.25), stroke=BLUE, sw=SW))
    o.append(polygon([(x - w * 0.17, y_tip - cone * 0.34), (x + w * 0.17, y_tip - cone * 0.34),
                      (x, y_tip)], fill=G1, stroke=BLUE, sw=SW))
    return "\n".join(o)


def rasm_2_4():
    W, H = 540, 760
    D = (70, -120)
    art = []
    L = []
    # --- 1-qism: tekis varaq ---
    fl, fr = (40, 250), (430, 250)
    sheet = [fl, fr, (fr[0] + D[0], fr[1] + D[1]), (fl[0] + D[0], fl[1] + D[1])]
    art.append(polygon(sheet, fill=CREAM, stroke=BLUE, sw=SW))
    A = (fl[0] + D[0] / 2 + 30, fl[1] + D[1] / 2)
    B = (fr[0] + D[0] / 2 - 30, fr[1] + D[1] / 2)
    art.append(line(A[0], A[1], B[0], B[1], stroke=ACCENT, sw=SW, extra=' stroke-dasharray="12 9"'))
    for p in (A, B):
        art.append(circle(p[0], p[1], 8, fill=BLUE, stroke=None, sw=0))
    L.append(text(A[0], A[1] - 18, "A", anchor="middle", weight="bold"))
    L.append(text(B[0], B[1] - 18, "B", anchor="middle", weight="bold"))
    L.append(text((A[0] + B[0]) / 2, A[1] + 40, "uzun yo‘l", anchor="middle"))
    # o'tish strelkasi
    art.append(arrow(270, 272, 270, 318, stroke=G3, sw=SW * 1.4, head=20))

    # --- 2-qism: U shaklida buklangan varaq ---
    yb, yt = 650, 515        # pastki va yuqori qatlam old cheti
    xl, xr = 140, 440
    r = (yb - yt) / 2
    fc = (xl, (yb + yt) / 2)
    bc = (fc[0] + D[0], fc[1] + D[1])
    def arc(cxy, a0, a1, n=48):
        return [(cxy[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                 cxy[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    at = math.degrees(math.atan2(D[0], -D[1])) + 180   # siluet urinma burchagi (~210°)
    bot = [(xl, yb), (xr, yb), (xr + D[0], yb + D[1]), (xl + D[0], yb + D[1])]
    top = [(xl, yt), (xr, yt), (xr + D[0], yt + D[1]), (xl + D[0], yt + D[1])]
    A2 = (xr - 40 + D[0] / 2, yt + D[1] / 2)
    B2 = (A2[0], yb + D[1] / 2)
    x_p = A2[0]
    full_pencil = pencil(x_p, A2[1] - 140, yb + 58)
    def clipped(y0, y1, cid):
        return (f'<clipPath id="{cid}"><rect x="{f(x_p - 40)}" y="{f(y0)}" width="80" '
                f'height="{f(y1 - y0)}"/></clipPath><g clip-path="url(#{cid})">{full_pencil}</g>')
    # ichki yuza (old ochiq tomondan ko'rinadi)
    inner = arc(fc, 90, 270) + [(xl + D[0], yt + D[1]), (xl + D[0], yb + D[1])]
    art.append(polygon(inner, fill=mix(CREAM, G2, 0.45), stroke=None, sw=0))
    art.append(clipped(B2[1], yb + 70, "qalamPast"))
    art.append(polygon(bot, fill=mix(CREAM, G4, 0.45), stroke=BLUE, sw=SW))
    art.append(ellipse(B2[0], B2[1], 19, 8, fill=G1, stroke=BLUE, sw=SW))
    # tashqi (ko'rinadigan) bukilish yuzasi — yuqori-chap qism
    band = arc(bc, at, 270) + arc(fc, 270, at)
    art.append(polygon(band, fill="url(#bukilish)", stroke=None, sw=0))
    pa, pb = arc(fc, at, at, 1)[0], arc(bc, at, at, 1)[0]
    art.append(line(pa[0], pa[1], pb[0], pb[1], stroke=BLUE, sw=SW))
    art.append(polyline(arc(bc, at, 270), stroke=BLUE, sw=SW))
    art.append(polyline(arc(fc, 90, 270), stroke=BLUE, sw=SW))
    art.append(clipped(A2[1], B2[1], "qalamOrta"))
    art.append(polygon(top, fill=CREAM, stroke=BLUE, sw=SW))
    art.append(ellipse(A2[0], A2[1], 19, 8, fill=G1, stroke=BLUE, sw=SW))
    art.append(clipped(A2[1] - 200, A2[1], "qalamTepa"))
    L.append(text(A2[0] - 34, A2[1] + 10, "A", anchor="end", weight="bold"))
    L.append(text(B2[0] - 34, B2[1] + 10, "B", anchor="end", weight="bold"))
    L.append(text(28, 742, "qisqa yo‘l (tunel)"))
    ym = yt + 34
    L.append(leader([(255, 732), (B2[0] - 95, 732), (B2[0] - 95, ym), (x_p - 17, ym)]))
    defs = f"""<linearGradient id="bukilish" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{mix(CREAM, G3, 0.55)}"/><stop offset="1" stop-color="{mix(CREAM, G4, 0.2)}"/></linearGradient>"""
    return svg_doc(W, H, "Rasm 2.4. Fazo-vaqt tuneli: buklangan qog‘oz", "\n".join(art),
                   "\n".join(L), defs)


if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["2-1", "2-2", "2-3", "2-4"]
    for w in which:
        fn = globals().get("rasm_" + w.replace("-", "_"))
        if fn:
            save(f"rasm_{w}.svg", fn())
