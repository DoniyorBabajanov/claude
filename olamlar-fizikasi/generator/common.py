"""«Olamlar fizikasi» rasmlari uchun umumiy yordamchi funksiyalar.

Koordinatalar: 1 birlik = 0,1 mm. To'liq kenglik 1120 birlik (11,2 sm),
yarim kenglik 540 birlik (5,4 sm).
"""
import math
import os

# --- Kitob palitrasi -------------------------------------------------------
BLUE = "#1F3A5F"      # to'q ko'k
GOLD = "#A67C2E"      # oltinrang
CREAM = "#F3EEE3"     # och qaymoq
ACCENT = "#B8553A"    # yagona urg'u rangi (terrakota) — barcha rasmlarda bir xil
G1 = "#3C3C3C"        # kulrang tuslar
G2 = "#6E6E6E"
G3 = "#9A9A9A"
G4 = "#C9C9C9"
G5 = "#E6E3DD"
WHITE = "#FFFFFF"
NIGHT = "#0D1826"     # qorong'i fon (to'q ko'kdan olingan)

# --- Chiziq va shrift ------------------------------------------------------
SW = 2.65             # 0,75 pt  — asosiy chiziq
SW_THIN = 1.4         # 0,4 pt   — to'r/tekstura chiziqlari
FONT = "Arial, Helvetica, 'Liberation Sans', sans-serif"
FS = 30               # 8,5 pt
FS_SMALL = 28.5       # 8,1 pt

OUT_SVG = os.path.join(os.path.dirname(__file__), "..", "svg")


def f(v):
    """Raqamni ixcham yozish."""
    s = f"{v:.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    if s == "-0":
        s = "0"
    return s


def pts(points):
    return " ".join(f"{f(x)},{f(y)}" for x, y in points)


def path_d(points, closed=False):
    if not points:
        return ""
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in points)
    if closed:
        d += " Z"
    return d


def lerp(a, b, t):
    return a + (b - a) * t


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(c):
    return "#" + "".join(f"{max(0, min(255, int(round(v)))):02X}" for v in c)


def mix(c1, c2, t):
    a, b = hex2rgb(c1), hex2rgb(c2)
    return rgb2hex(tuple(lerp(a[i], b[i], t) for i in range(3)))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=FS, anchor="start", fill=BLUE, weight="normal",
         extra=""):
    w = "" if weight == "normal" else f' font-weight="{weight}"'
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}" '
            f'text-anchor="{anchor}" fill="{fill}"{w}{extra}>{esc(s)}</text>')


def text_lines(x, y, lines, size=FS, anchor="start", fill=BLUE, lh=1.18,
               weight="normal"):
    out = []
    for i, s in enumerate(lines):
        out.append(text(x, y + i * size * lh, s, size, anchor, fill, weight))
    return "\n".join(out)


def line(x1, y1, x2, y2, stroke=BLUE, sw=SW, extra=""):
    return (f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
            f'stroke="{stroke}" stroke-width="{f(sw)}" '
            f'stroke-linecap="round"{extra}/>')


def polyline(points, stroke=BLUE, sw=SW, fill="none", extra=""):
    return (f'<polyline points="{pts(points)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{f(sw)}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}/>')


def polygon(points, fill=CREAM, stroke=BLUE, sw=SW, extra=""):
    st = "none" if stroke is None else stroke
    return (f'<polygon points="{pts(points)}" fill="{fill}" stroke="{st}" '
            f'stroke-width="{f(sw)}" stroke-linejoin="round"{extra}/>')


def circle(cx, cy, r, fill=CREAM, stroke=BLUE, sw=SW, extra=""):
    st = "none" if stroke is None else stroke
    return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" '
            f'stroke="{st}" stroke-width="{f(sw)}"{extra}/>')


def ellipse(cx, cy, rx, ry, fill=CREAM, stroke=BLUE, sw=SW, extra=""):
    st = "none" if stroke is None else stroke
    return (f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" '
            f'fill="{fill}" stroke="{st}" stroke-width="{f(sw)}"{extra}/>')


def path(d, fill="none", stroke=BLUE, sw=SW, extra=""):
    st = "none" if stroke is None else stroke
    return (f'<path d="{d}" fill="{fill}" stroke="{st}" stroke-width="{f(sw)}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}/>')


def arrow_head(x, y, ang, size=16, fill=BLUE):
    """Uchi (x, y) nuqtada, ang yo'nalishiga qaragan to'ldirilgan uchburchak."""
    a = ang
    p1 = (x, y)
    p2 = (x - size * math.cos(a) + size * 0.42 * math.sin(a),
          y - size * math.sin(a) - size * 0.42 * math.cos(a))
    p3 = (x - size * math.cos(a) - size * 0.42 * math.sin(a),
          y - size * math.sin(a) + size * 0.42 * math.cos(a))
    return polygon([p1, p2, p3], fill=fill, stroke=None, sw=0)


def arrow(x1, y1, x2, y2, stroke=BLUE, sw=SW, head=16, both=False):
    ang = math.atan2(y2 - y1, x2 - x1)
    # chiziq uchini biroz qisqartiramiz, uchburchak toza ko'rinsin
    sx2 = x2 - head * 0.8 * math.cos(ang)
    sy2 = y2 - head * 0.8 * math.sin(ang)
    sx1, sy1 = x1, y1
    out = []
    if both:
        sx1 = x1 + head * 0.8 * math.cos(ang)
        sy1 = y1 + head * 0.8 * math.sin(ang)
        out.append(arrow_head(x1, y1, ang + math.pi, head, stroke))
    out.insert(0, line(sx1, sy1, sx2, sy2, stroke, sw))
    out.append(arrow_head(x2, y2, ang, head, stroke))
    return "\n".join(out)


def leader(points, stroke=G1, sw=SW * 0.75, dot=True, dot_fill=None):
    """Yozuv ko'rsatkichi: siniq chiziq, oxirida kichik nuqta."""
    out = [polyline(points, stroke=stroke, sw=sw)]
    if dot:
        x, y = points[-1]
        out.append(circle(x, y, 4.2, fill=dot_fill or stroke, stroke=None, sw=0))
    return "\n".join(out)


def svg_doc(w, h, title, art, labels="", defs="", bg=None, desc=""):
    """Qatlamli SVG hujjat. w, h — 0,1 mm birliklarida."""
    bg_layer = ""
    if bg:
        bg_layer = (f'<g id="fon" inkscape:groupmode="layer" inkscape:label="fon">'
                    f'<rect x="0" y="0" width="{f(w)}" height="{f(h)}" fill="{bg}"/></g>\n')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="{f(w / 10)}mm" height="{f(h / 10)}mm" viewBox="0 0 {f(w)} {f(h)}">
<title>{esc(title)}</title>
<desc>{esc(desc or "«Olamlar fizikasi» kitobi uchun original rasm. Yozuvlar alohida «yozuvlar» qatlamida.")}</desc>
<defs>
{defs}
</defs>
{bg_layer}<g id="rasm" inkscape:groupmode="layer" inkscape:label="rasm">
{art}
</g>
<g id="yozuvlar" inkscape:groupmode="layer" inkscape:label="yozuvlar" font-family="{FONT}">
{labels}
</g>
</svg>
'''


def save(name, content):
    os.makedirs(OUT_SVG, exist_ok=True)
    p = os.path.join(OUT_SVG, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("saved", name, f"{len(content) / 1024:.0f} KB")
    return p
