#!/usr/bin/env python3
"""Dessine les visuels Kurovani en SVG (hoodie, cargo, affiche) dans studio.html.
Usage : python3 tools/draw.py > tools/studio.html, puis node tools/render.js pour les PNG."""
import math, random

RED, DEEP, OFF, GREY = "#d1001c", "#7a0010", "#eaeaea", "#3a3a3a"

DEFS = f"""
<svg width="0" height="0" style="position:absolute"><defs>
  <linearGradient id="fab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26262a"/><stop offset=".55" stop-color="#141416"/><stop offset="1" stop-color="#0a0a0b"/></linearGradient>
  <linearGradient id="fabS" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#232327"/><stop offset="1" stop-color="#09090a"/></linearGradient>
  <linearGradient id="rib" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1c1f"/><stop offset="1" stop-color="#0b0b0c"/></linearGradient>
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".34" stop-color="#c9c9d0"/><stop offset=".5" stop-color="#63636c"/><stop offset=".6" stop-color="#f3f3f6"/><stop offset="1" stop-color="#8b8b95"/></linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#77777f"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="#5c5c64"/></linearGradient>
  <radialGradient id="sun" cx=".4" cy=".36" r=".75"><stop offset="0" stop-color="#ff3550"/><stop offset=".45" stop-color="{RED}"/><stop offset="1" stop-color="{DEEP}"/></radialGradient>
  <radialGradient id="skin" cx=".4" cy=".3" r=".8"><stop offset="0" stop-color="#e9c4a6"/><stop offset="1" stop-color="#a97e62"/></radialGradient>
  <pattern id="ribs" width="6" height="10" patternUnits="userSpaceOnUse"><rect width="6" height="10" fill="url(#rib)"/><rect x="0" width="1.4" height="10" fill="#000" opacity=".55"/><rect x="3" width=".8" height="10" fill="#fff" opacity=".05"/></pattern>
  <filter id="tex" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="1.15" numOctaves="2" seed="3" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 -.2" result="g"/><feComposite in="g" in2="SourceAlpha" operator="in" result="gg"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="gg"/></feMerge></filter>
  <filter id="grunge" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency=".09 .16" numOctaves="4" seed="11" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -14 5.3" result="m"/><feComposite in="SourceGraphic" in2="m" operator="out"/></filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="14"/></filter>
  <g id="mark"><!-- emblème : deux X chromés et l'étoile à 4 branches -->
    <g fill="url(#chrome)" stroke="{RED}" stroke-width="1.6" stroke-linejoin="miter">
      <path d="M0,45 L62,37 L62,53 Z"/><path d="M200,45 L138,37 L138,53 Z"/>
      <path d="M14,6 L44,6 L70,36 L88,10 L99,10 L78,45 L99,80 L88,80 L70,54 L44,84 L14,84 L52,45 Z"/>
      <path d="M186,6 L156,6 L130,36 L112,10 L101,10 L122,45 L101,80 L112,80 L130,54 L156,84 L186,84 L148,45 Z"/>
    </g>
    <path d="M100,8 L105,39 L128,45 L105,51 L100,82 L95,51 L72,45 L95,39 Z" fill="{RED}" stroke="#fff" stroke-width=".8"/>
  </g>
  <path id="star" d="M0,-14 L3,-3 L14,0 L3,3 L0,14 L-3,3 L-14,0 L-3,-3 Z"/>
</defs></svg>"""


def zig(p0, p1, n, amp, seed):
    r = random.Random(seed)
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    pts = [(x0, y0)]
    for i in range(1, n):
        t = i / n + r.uniform(-.25, .25) / n
        o = r.uniform(.45, 1) * amp * (1 if i % 2 else -1)
        pts.append((x0 + dx * t + nx * o, y0 + dy * t + ny * o))
    pts.append((x1, y1))
    return pts


def blade(pts, w):
    """Polygone effilé le long d'une ligne brisée : épais au départ, pointu à l'arrivée."""
    left, right = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        ax, ay = pts[max(0, i - 1)]
        bx, by = pts[min(n - 1, i + 1)]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        h = w / 2 * (1 - i / (n - 1)) ** .8
        left.append((x - dy / L * h, y + dx / L * h))
        right.append((x + dy / L * h, y - dx / L * h))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in left + right[::-1])


def bolt(p0, p1, n=7, amp=14, seed=1, w=5, color=RED, core=True, branches=2):
    w = w * 2.6
    pts = zig(p0, p1, n, amp, seed)
    out = f'<polygon points="{blade(pts, w)}" fill="{color}"/>'
    r = random.Random(seed * 7)
    for b in range(branches):
        i = r.randrange(1, len(pts) - 2)
        x, y = pts[i]
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + r.choice([-1, 1]) * r.uniform(.45, .9)
        ln = r.uniform(.25, .42) * math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        q = (x + math.cos(ang) * ln, y + math.sin(ang) * ln)
        out += f'<polygon points="{blade(zig((x, y), q, 4, amp * .5, seed + b + 3), w * .6)}" fill="{color}"/>'
    if core:
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-1])
        out += f'<polyline points="{d}" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.2" stroke-linejoin="miter"/>'
    return out


def vtext(x, y, s, size, fill=OFF, gap=1.08, extra=""):
    return "".join(f'<text x="{x}" y="{y + i * size * gap:.1f}" font-family="Shippori Mincho B1, serif" font-weight="800" font-size="{size}" text-anchor="middle" fill="{fill}" {extra}>{c}</text>' for i, c in enumerate(s))


def pagoda(cx, top, tiers=4, w0=34, step=18, h=27):
    out = f'<path d="M{cx},{top - 26} L{cx},{top + 4}" stroke="#0a0a0b" stroke-width="3"/><circle cx="{cx}" cy="{top - 16}" r="3.5" fill="#0a0a0b"/>'
    for k in range(tiers):
        y = top + k * h
        w = w0 + k * step
        out += (f'<path d="M{cx - w / 2 - 18},{y + 13} Q{cx - w / 2 - 6},{y + 10} {cx - w / 2 + 6},{y + 2} L{cx + w / 2 - 6},{y + 2} Q{cx + w / 2 + 6},{y + 10} {cx + w / 2 + 18},{y + 13} L{cx + w / 2 + 8},{y + 17} L{cx - w / 2 - 8},{y + 17} Z" fill="#0a0a0b"/>'
                f'<rect x="{cx - w / 2 + 7}" y="{y + 17}" width="{w - 14}" height="{h - 14}" fill="#0a0a0b"/>')
    return out


def torii(cx, y, s=1.0, fill="#e2122e", stroke="#16000a"):
    return (f'<g transform="translate({cx},{y}) scale({s})" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-linejoin="round">'
            '<path d="M-58,0 Q0,9 58,0 L52,12 Q0,19 -52,12 Z"/><rect x="-44" y="26" width="88" height="8"/>'
            '<path d="M-36,14 L-28,14 L-25,84 L-39,84 Z"/><path d="M36,14 L28,14 L25,84 L39,84 Z"/><rect x="-4" y="14" width="8" height="12"/></g>')


def smoke(cx, cy, s=1.0, seed=2, col="#c9c9d0"):
    r = random.Random(seed)
    out = ""
    for i in range(5):
        x, y = cx + r.uniform(-90, 90) * s, cy + r.uniform(-30, 40) * s
        a, b = r.uniform(30, 70) * s, r.uniform(10, 26) * s
        out += f'<path d="M{x - a:.0f},{y:.0f} C{x - a / 2:.0f},{y - b:.0f} {x:.0f},{y + b:.0f} {x + a:.0f},{y - b / 2:.0f} C{x + a * .6:.0f},{y + b * .3:.0f} {x + a * .2:.0f},{y + b * 1.2:.0f} {x - a * .2:.0f},{y + b * .5:.0f}" fill="none" stroke="{col}" stroke-width="{r.uniform(2, 5) * s:.1f}" stroke-linecap="round" opacity="{r.uniform(.35, .8):.2f}"/>'
    return out


def wordmark(x, y, size, anchor="middle", sp=2):
    return f'<text x="{x}" y="{y}" font-family="Michroma, sans-serif" font-size="{size}" letter-spacing="{sp}" text-anchor="{anchor}" fill="url(#chrome)" stroke="{RED}" stroke-width=".5" paint-order="stroke">KUROVANI</text>'


# ------------------------------------------------------------------ HOODIE
SLEEVE = "M152,182 C112,204 84,262 66,360 L40,548 L112,562 L150,420 Z"
CUFF = "M38,546 L114,560 L108,606 L33,592 Z"
BODY_F = "M228,150 C200,162 172,170 150,182 L146,604 L454,604 L450,182 C428,170 400,162 372,150 C350,178 250,178 228,150 Z"
BODY_B = "M228,150 C200,162 172,170 150,182 L146,604 L454,604 L450,182 C428,170 400,162 372,150 Z"


def back_print():
    """Le graphisme dos : soleil, pagode, torii, brumes, emblème."""
    return (f'<g filter="url(#grunge)"><circle cx="300" cy="352" r="92" fill="url(#sun)"/>'
            + smoke(300, 420, 1.0, 5) + bolt((228, 300), (196, 470), 6, 12, 21, 5) + bolt((372, 470), (404, 300), 6, 12, 33, 4, "#c9c9d0", False, 1)
            + pagoda(300, 292) + torii(300, 404, .78)
            + f'<path d="M214,468 C250,440 286,476 300,452 C316,476 352,440 386,468" fill="none" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>'
            + '</g>'
            + vtext(410, 300, "黒バニ", 30)
            + f'<g fill="{OFF}" opacity=".7">' + "".join(f'<rect x="188" y="{330 + i * 7}" width="{3 + (i * 7) % 9}" height="3"/>' for i in range(14)) + '</g>'
            + '<use href="#mark" transform="translate(212,486) scale(.88)"/>' + wordmark(300, 590, 21))


def hoodie(side, hood="up"):
    front = side == "front"
    g = '<g filter="url(#tex)">'
    for mirror in ("", ' transform="translate(600,0) scale(-1,1)"'):
        g += f'<g{mirror}><path d="{SLEEVE}" fill="url(#fabS)" stroke="#303034" stroke-width="1.5"/><path d="{CUFF}" fill="url(#ribs)" stroke="#303034" stroke-width="1.5"/>'
        g += '<path d="M150,250 C128,300 118,360 122,430" fill="none" stroke="#000" stroke-opacity=".55" stroke-width="5"/><path d="M92,330 C84,400 76,460 70,520" fill="none" stroke="#fff" stroke-opacity=".05" stroke-width="6"/></g>'
    if not front:
        g += f'<path d="{BODY_B}" fill="url(#fab)" stroke="#303034" stroke-width="1.5"/>'
        if hood == "up":
            g += '<path d="M222,162 C190,62 250,20 300,20 C350,20 410,62 378,162 C378,216 340,242 300,246 C260,242 222,216 222,162 Z" fill="url(#fabS)" stroke="#34343a" stroke-width="1.5"/>'
            g += '<path d="M300,22 L300,244" stroke="#000" stroke-opacity=".6" stroke-width="2"/><path d="M240,190 C262,224 338,224 360,190" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="5"/>'
        else:
            g += '<path d="M226,156 C250,140 350,140 374,156 C392,214 344,250 300,254 C256,250 208,214 226,156 Z" fill="url(#fabS)" stroke="#34343a" stroke-width="1.5"/>'
            g += '<path d="M300,150 L300,252" stroke="#000" stroke-opacity=".6" stroke-width="2"/><path d="M244,176 C266,200 334,200 356,176" fill="none" stroke="#000" stroke-opacity=".55" stroke-width="6"/>'
    else:
        g += '<path d="M226,154 C194,60 250,22 300,22 C350,22 406,60 374,154 C350,182 250,182 226,154 Z" fill="url(#fabS)" stroke="#34343a" stroke-width="1.5"/>'
        g += '<path d="M250,152 C234,94 268,60 300,60 C332,60 366,94 350,152 C334,172 266,172 250,152 Z" fill="#050506" stroke="#2a2a2e" stroke-width="1.5"/>'
        g += f'<path d="M258,150 C250,108 276,82 300,82 C324,82 350,108 342,150" fill="none" stroke="{DEEP}" stroke-opacity=".7" stroke-width="3"/>'
        g += f'<path d="{BODY_F}" fill="url(#fab)" stroke="#303034" stroke-width="1.5"/>'
        g += '<path d="M228,150 C250,180 284,198 300,204 C316,198 350,180 372,150" fill="none" stroke="#3a3a40" stroke-width="2"/>'
    g += '<rect x="146" y="598" width="308" height="46" rx="7" fill="url(#ribs)" stroke="#303034" stroke-width="1.5"/>'
    g += '<path d="M176,200 C168,330 170,470 166,596" fill="none" stroke="#fff" stroke-opacity=".045" stroke-width="10"/><path d="M430,210 C436,340 432,470 436,596" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="12"/>'
    if front:
        g += '<path d="M206,474 L394,474 L426,586 L174,586 Z" fill="#17171a" stroke="#34343a" stroke-width="1.5"/><path d="M206,474 C196,500 186,530 180,560 M394,474 C404,500 414,530 420,560" fill="none" stroke="#000" stroke-opacity=".7" stroke-width="4"/>'
    g += '</g>'
    # impressions
    g += f'<clipPath id="clip-h-{side}"><path d="{SLEEVE}"/><path d="{SLEEVE}" transform="translate(600,0) scale(-1,1)"/><path d="{BODY_B}"/></clipPath><g clip-path="url(#clip-h-{side})">'
    g += f'<g>{bolt((132, 250), (70, 520), 9, 13, 4, 5)}{bolt((120, 300), (96, 470), 6, 8, 9, 2.5, "#c9c9d0", False, 1)}</g>'
    g += f'<g>{bolt((468, 250), (530, 520), 9, 15, 6, 6, "#c9c9d0", False, 3)}{bolt((478, 280), (512, 500), 8, 10, 14, 4)}</g>'
    g += f'<g transform="rotate(11 100 380)">{vtext(104, 330, "黒バニ", 21)}</g></g>'
    if front:
        g += f'<path d="M279,198 C274,250 277,300 272,338" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="7 2"/><path d="M321,198 C326,250 323,300 328,338" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="7 2"/>'
        g += '<rect x="268" y="336" width="8" height="30" rx="2" fill="url(#steel)"/><rect x="324" y="336" width="8" height="30" rx="2" fill="url(#steel)"/><circle cx="279" cy="197" r="4.5" fill="url(#steel)"/><circle cx="321" cy="197" r="4.5" fill="url(#steel)"/>'
        g += '<use href="#mark" transform="translate(196,236) scale(1.04)"/>' + wordmark(300, 366, 27, sp=3)
        g += f'<text x="300" y="392" font-family="Shippori Mincho B1, serif" font-weight="800" font-size="16" text-anchor="middle" fill="{OFF}" letter-spacing="4">— 黒バニ —</text><use href="#star" transform="translate(300,424)" fill="{RED}"/>'
        g += f'<rect x="226" y="540" width="52" height="24" fill="#0a0a0b" stroke="{OFF}" stroke-width="1.2"/><text x="252" y="555" font-family="Michroma, sans-serif" font-size="5.6" text-anchor="middle" fill="{OFF}">KUROVANI</text>'
        g += f'<text x="376" y="578" font-family="Shippori Mincho B1, serif" font-weight="800" font-size="13" text-anchor="middle" fill="{OFF}">黒バニ</text><use href="#star" transform="translate(406,574) scale(.5)" fill="{RED}"/>'
    else:
        g += f'<use href="#star" transform="translate(300,{120 if hood == "up" else 222}) scale({1.5 if hood == "up" else 1})" fill="{RED}"/>' + back_print()
    return f'<svg class="art" id="hoodie-{side}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 664" width="600" height="664">{g}</svg>'


# ------------------------------------------------------------------ CARGO
LEG = "M132,84 C104,190 74,400 84,652 C120,672 210,672 246,654 C248,520 254,360 260,252 L260,84 Z"


def pants_print(side):
    g = ""
    if side == "front":
        g += bolt((120, 420), (150, 640), 8, 16, 41, 6) + bolt((150, 380), (214, 600), 7, 12, 43, 3, "#c9c9d0", False, 1)
        g += bolt((402, 300), (350, 640), 10, 18, 47, 6) + bolt((420, 420), (396, 630), 6, 10, 51, 3, "#c9c9d0", False, 1)
        g += vtext(330, 300, "黒波", 34)
    else:
        g += f'<g filter="url(#grunge)"><circle cx="330" cy="220" r="62" fill="url(#sun)"/>{smoke(330, 262, .6, 9)}</g>'
        g += bolt((300, 250), (370, 640), 10, 20, 61, 7) + bolt((340, 300), (420, 600), 8, 14, 63, 4, "#c9c9d0", False, 2)
        g += bolt((176, 300), (130, 640), 9, 16, 67, 5) + vtext(396, 330, "黒波", 34)
    return g


def pants(side):
    front = side == "front"
    g = '<g filter="url(#tex)">'
    for mirror in ("", ' transform="translate(520,0) scale(-1,1)"'):
        g += f'<g{mirror}><path d="{LEG}" fill="url(#fab)" stroke="#303034" stroke-width="1.5"/>'
        g += '<path d="M150,120 C128,260 112,420 118,640" fill="none" stroke="#fff" stroke-opacity=".05" stroke-width="12"/><path d="M236,270 C232,400 226,520 228,650" fill="none" stroke="#000" stroke-opacity=".6" stroke-width="14"/>'
        g += '<path d="M86,628 C122,650 208,650 245,632" fill="none" stroke="#000" stroke-opacity=".7" stroke-width="5"/><path d="M96,640 l6,-14 M130,652 l4,-15 M170,656 l1,-15 M210,650 l-3,-14" stroke="#34343a" stroke-width="2"/>'
        # poche cargo à rabat
        g += '<path d="M90,338 L176,326 L180,444 L96,456 Z" fill="#161619" stroke="#34343a" stroke-width="1.5"/><path d="M86,300 L174,290 L177,328 L89,340 Z" fill="#1c1c20" stroke="#3a3a40" stroke-width="1.5"/><path d="M92,446 L176,434" stroke="#000" stroke-opacity=".6" stroke-width="4"/></g>'
    g += '<path d="M260,86 L260,252" stroke="#000" stroke-opacity=".7" stroke-width="3"/>'
    g += '<rect x="130" y="36" width="260" height="52" rx="10" fill="url(#ribs)" stroke="#303034" stroke-width="1.5"/>'
    if front:
        g += '<path d="M260,150 C250,190 252,226 260,252" fill="none" stroke="#34343a" stroke-width="2"/>'
    else:
        g += '<path d="M150,150 L236,140 L238,156 L152,166 Z M370,150 L284,140 L282,156 L368,166 Z" fill="#1c1c20" stroke="#3a3a40" stroke-width="1.5"/>'
    g += '</g>' + f'<clipPath id="clip-p-{side}"><path d="{LEG}"/><path d="{LEG}" transform="translate(520,0) scale(-1,1)"/></clipPath><g clip-path="url(#clip-p-{side})">' + pants_print(side) + '</g>'
    if front:
        g += f'<path d="M250,60 C246,110 250,150 244,186" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="7 2"/><path d="M270,60 C274,110 270,150 276,186" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="7 2"/>'
        g += '<rect x="240" y="184" width="8" height="28" rx="2" fill="url(#steel)"/><rect x="272" y="184" width="8" height="28" rx="2" fill="url(#steel)"/><circle cx="250" cy="60" r="4.5" fill="url(#steel)"/><circle cx="270" cy="60" r="4.5" fill="url(#steel)"/>'
        g += f'<g transform="rotate(-7 132 372)"><rect x="104" y="360" width="58" height="22" fill="{RED}"/><text x="133" y="375" font-family="Michroma, sans-serif" font-size="6.6" text-anchor="middle" fill="#fff">KUROVANI</text></g>'
    else:
        g += f'<rect x="226" y="46" width="68" height="32" fill="#0a0a0b" stroke="{OFF}" stroke-width="1.2"/><use href="#mark" transform="translate(236,49) scale(.24)"/><text x="260" y="74" font-family="Michroma, sans-serif" font-size="5" text-anchor="middle" fill="{OFF}">KUROVANI</text>'
        g += f'<use href="#star" transform="translate(194,200) scale(1.1)" fill="{RED}"/>'
    return f'<svg class="art" id="pants-{side}" xmlns="http://www.w3.org/2000/svg" viewBox="40 20 440 668" width="440" height="668">{g}</svg>'


# ------------------------------------------------------------------ AFFICHE
def poster():
    W, H = 900, 1200
    r = random.Random(77)
    g = f'<rect width="{W}" height="{H}" fill="#050506"/>'
    g += f'<circle cx="450" cy="440" r="380" fill="{RED}" opacity=".35" filter="url(#soft)"/>'
    g += '<clipPath id="sunclip"><circle cx="450" cy="440" r="330"/></clipPath>'
    g += '<g filter="url(#grunge)"><circle cx="450" cy="440" r="330" fill="url(#sun)"/></g>'
    # lignes de vitesse dans le soleil
    g += '<g clip-path="url(#sunclip)" stroke="#000" opacity=".22">' + "".join(
        f'<line x1="450" y1="440" x2="{450 + math.cos(a) * 420:.0f}" y2="{440 + math.sin(a) * 420:.0f}" stroke-width="{r.uniform(1, 5):.1f}" stroke-dasharray="{r.randint(40, 160)} {r.randint(30, 220)}" stroke-dashoffset="{r.randint(0, 200)}"/>'
        for a in [i * math.pi / 36 + r.uniform(-.03, .03) for i in range(72)]) + '</g>'
    # brumes sur le bas du soleil
    g += '<g clip-path="url(#sunclip)">' + "".join(f'<rect x="100" y="{560 + i * 30}" width="700" height="{6 + i * 2}" fill="#050506" opacity="{.25 + i * .09:.2f}"/>' for i in range(8)) + '</g>'
    # ville, pagode lointaine
    city = ""
    for x0, x1 in ((0, 250), (650, 900)):
        x = x0
        while x < x1:
            w, h = r.randint(26, 64), r.randint(110, 380)
            city += f'<rect x="{x}" y="{800 - h}" width="{w}" height="{h}" fill="#08080a"/>'
            for _ in range(r.randint(2, 7)):
                city += f'<rect x="{x + r.randint(3, max(4, w - 8))}" y="{800 - h + r.randint(8, max(9, h - 20))}" width="4" height="7" fill="{RED}" opacity="{r.uniform(.35, .9):.2f}"/>'
            x += w + r.randint(0, 6)
    g += city + f'<g transform="translate(-40,150) scale(1.7)">{pagoda(140, 232, 4, 30, 16, 26)}</g>'
    # grand torii
    g += torii(450, 196, 5.2, "#0a0a0b", "#2a0008")
    # sol mouillé
    g += '<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a0206"/><stop offset=".25" stop-color="#0b0b0d"/><stop offset="1" stop-color="#020203"/></linearGradient>'
    g += '<rect y="790" width="900" height="410" fill="url(#ground)"/>'
    g += "".join(f'<line x1="450" y1="790" x2="{x}" y2="1200" stroke="{RED}" stroke-opacity=".12" stroke-width="2"/>' for x in range(-600, 1600, 150))
    g += "".join(f'<rect x="{r.randint(0, 800)}" y="{r.randint(810, 1180)}" width="{r.randint(40, 220)}" height="2" fill="{RED}" opacity="{r.uniform(.08, .35):.2f}"/>' for _ in range(46))
    g += '<ellipse cx="450" cy="1168" rx="250" ry="26" fill="#000" opacity=".8" filter="url(#soft)"/>'
    # éclairs d'ambiance
    g += f'<g filter="url(#glow)">{bolt((96, 380), (250, 800), 12, 30, 91, 7)}{bolt((820, 330), (660, 800), 12, 30, 93, 7)}</g>'
    # ---- personnage, de dos
    fig = ""
    # jambes : cargo baggy
    for mirror in ("", ' transform="translate(900,0) scale(-1,1)"'):
        fig += f'<g{mirror}><path d="M338,800 C306,920 296,1040 312,1150 L438,1154 C442,1040 446,930 450,850 L450,800 Z" fill="url(#fab)" stroke="#303034" stroke-width="1.5"/>'
        fig += '<path d="M318,930 L378,922 L380,1010 L322,1020 Z" fill="#161619" stroke="#34343a" stroke-width="1.5"/><path d="M314,902 L376,896 L378,924 L316,932 Z" fill="#1c1c20" stroke="#3a3a40" stroke-width="1.5"/>'
        fig += '<path d="M314,1132 C350,1148 410,1148 438,1136" fill="none" stroke="#000" stroke-opacity=".7" stroke-width="5"/><path d="M430,860 C426,960 424,1060 426,1150" fill="none" stroke="#000" stroke-opacity=".6" stroke-width="10"/>'
        # baskets
        fig += '<path d="M318,1150 L436,1152 L438,1180 L306,1180 C304,1166 310,1154 318,1150 Z" fill="#0c0c0e" stroke="#303034" stroke-width="1.5"/>'
        fig += f'<rect x="304" y="1178" width="136" height="10" rx="4" fill="{OFF}"/><rect x="330" y="1160" width="54" height="5" fill="{RED}"/></g>'
    fig += f'<g filter="url(#grunge)"><circle cx="520" cy="900" r="44" fill="url(#sun)"/></g>' + bolt((500, 930), (552, 1140), 8, 14, 101, 5) + bolt((372, 940), (342, 1140), 8, 12, 103, 4)
    fig += vtext(566, 960, "黒波", 26)
    # hoodie de dos (même dessin que la pièce)
    hb = hoodie("back", "down").replace("clip-h-back", "clip-h-poster")
    inner = hb[hb.index(">") + 1:hb.rindex("</svg>")]
    # mains
    hands = '<ellipse cx="72" cy="612" rx="26" ry="20" fill="url(#skin)" stroke="#5e4334" stroke-width="1.5" transform="rotate(10 72 612)"/><ellipse cx="528" cy="612" rx="26" ry="20" fill="url(#skin)" stroke="#5e4334" stroke-width="1.5" transform="rotate(-10 528 612)"/>'
    fig += f'<g transform="translate(234,350) scale(.72)">{hands}{inner}'
    # tête vue de dos : nuque, oreilles, cheveux en pointes
    fig += '<g transform="translate(300,176) scale(1.38) translate(-300,-176)">'
    fig += '<path d="M278,96 L278,172 C290,184 310,184 322,172 L322,96 Z" fill="url(#skin)" stroke="#5e4334" stroke-width="1.5"/>'
    fig += '<path d="M258,166 C278,186 322,186 342,166" fill="none" stroke="#1d1d21" stroke-width="12" stroke-linecap="round"/>'
    fig += '<ellipse cx="247" cy="74" rx="8" ry="13" fill="url(#skin)" stroke="#5e4334" stroke-width="1.5"/><ellipse cx="353" cy="74" rx="8" ry="13" fill="url(#skin)" stroke="#5e4334" stroke-width="1.5"/>'
    hair = "M250,84 L230,62 L252,50 L232,22 L260,26 L254,-10 L282,10 L296,-28 L314,10 L344,-12 L340,26 L370,20 L350,50 L372,60 L350,84 L356,118 L338,102 L332,134 L315,110 L300,142 L285,110 L268,134 L262,102 L244,118 Z"
    fig += f'<path d="{hair}" fill="#0b0b0d" stroke="#3a3a40" stroke-width="2" stroke-linejoin="miter"/>'
    fig += f'<path d="M262,30 L276,84 M296,-18 L300,74 M340,28 L326,86 M236,60 L264,96 M366,60 L338,98" stroke="#c9c9d0" stroke-opacity=".5" stroke-width="2.5" fill="none"/><path d="M282,14 L288,96 M316,14 L312,100" stroke="{RED}" stroke-width="3" fill="none"/>'
    fig += '</g></g>'
    g += fig
    # braises
    g += "".join(f'<circle cx="{r.randint(40, 860)}" cy="{r.randint(120, 1100)}" r="{r.uniform(1, 3.6):.1f}" fill="{RED}" opacity="{r.uniform(.4, 1):.2f}"/>' for _ in range(70))
    # typographie d'affiche
    g += vtext(826, 250, "黒バニ", 96, OFF, 1.1, 'stroke="#000" stroke-width="3" paint-order="stroke"')
    g += '<use href="#mark" transform="translate(48,52) scale(.9)"/>' + wordmark(48, 172, 30, "start", 4)
    g += f'<text x="50" y="204" font-family="Barlow Condensed, sans-serif" font-weight="700" font-size="24" letter-spacing="10" fill="{RED}">ORIGINALS</text>'
    for i, (t, f) in enumerate((("MORE THAN", OFF), ("FASHION.", OFF), ("A STATE", "url(#chrome)"), ("OF MIND.", "url(#chrome)"))):
        g += f'<text x="50" y="{1060 + i * 30}" font-family="Michroma, sans-serif" font-size="22" fill="{f}">{t}</text>'
    g += f'<text x="850" y="1152" font-family="Shippori Mincho B1, serif" font-weight="800" font-size="17" text-anchor="end" fill="{OFF}">黒の中に、俺たちの道がある</text>'
    g += f'<text x="850" y="62" font-family="Barlow Condensed, sans-serif" font-weight="600" font-size="16" letter-spacing="5" text-anchor="end" fill="#9a9a9a">STREETWEAR / ANIME INSPIRED / PARIS – TOKYO</text>'
    g += "".join(f'<rect x="{50 + i * 11}" y="1000" width="6" height="20" fill="{RED}" transform="skewX(-24)" transform-origin="{50 + i * 11} 1020"/>' for i in range(3))
    g += f'<rect x="20" y="20" width="860" height="1160" fill="none" stroke="{OFF}" stroke-opacity=".35" stroke-width="1.5"/>'
    return f'<svg class="art" id="poster-dos" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{g}</svg>'


if __name__ == "__main__":
    print('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Michroma&family=Shippori+Mincho+B1:wght@800&display=swap"><style>body{margin:0;background:transparent}.art{display:block;margin:20px}</style></head><body>')
    print(DEFS)
    for s in ("front", "back"):
        print(hoodie(s)); print(pants(s))
    print(poster())
    print("</body></html>")
