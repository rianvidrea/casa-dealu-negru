#!/usr/bin/env python3
"""Planul zonei wellness cu cele 7 compartimente, desenat la scara.

Reface schita de mana in cote reale, cu acelasi cod de culoare:
negru = perete plin, bleu = vitraj retractabil, albastru inchis = vitraj fix,
rosu = usa. Iesire SVG; daca exista Chromium in sistem se scoate si un PNG
pentru folosit ca referinta de geometrie la randare.

    python3 tools/plan_compartimente.py
"""

import os
import subprocess
import sys

# --------------------------------------------------------------------------
# geometrie, in metri; originea = coltul nord-vest al barei lungi
# x creste spre est, y creste spre sud
# --------------------------------------------------------------------------

BARA_L = 18.0          # 6 (zona 1) + 8 (zona 2) + 4 (zona 3), cotat de mana
BARA_A = 6.0           # adancimea barei, cotata de mana
X1, X2, X3 = 6.0, 14.0, 18.0      # rosturile dintre 1|2, 2|3, 3|hol

HOL_X0, HOL_X1 = 18.0, 20.0       # holul, latime 2.0 (dedus din schita)
ARIPA_X1 = 25.0                   # fata est a camerelor 5 si 6
Y56 = 7.0                         # rostul dintre 5 si 6
ARIPA_Y1 = 12.0                   # fata sud a aripii
TERASA_Y0 = -3.5                  # terasa jacuzzi, la nord

COMPARTIMENTE = [
    ("1", "BBQ + bucatarie", 0.0, 0.0, X1, BARA_A),
    ("2", "piscina", X1, 0.0, X2, BARA_A),
    ("3", "fitness", X2, 0.0, X3, BARA_A),
    ("4", "hol", HOL_X0, 0.0, HOL_X1, ARIPA_Y1),
    ("5", "relaxare", HOL_X1, 0.0, ARIPA_X1, Y56),
    ("6", "sauna", HOL_X1, Y56, ARIPA_X1, ARIPA_Y1),
    ("7", "jacuzzi", HOL_X0, TERASA_Y0, ARIPA_X1, 0.0),
]

# pereti: (tip, x0, y0, x1, y1)
PLIN, RETRACTABIL, FIX = "plin", "retractabil", "fix"

PERETI = [
    # bara lunga
    (PLIN, 0.0, 0.0, 0.0, BARA_A),                 # peretele negru cu BBQ-ul
    (RETRACTABIL, 0.0, 0.0, X2, 0.0),              # fatada nord, zonele 1+2
    (RETRACTABIL, 0.0, BARA_A, X2, BARA_A),        # fatada sud, zonele 1+2
    (FIX, X2, 0.0, X2, BARA_A),                    # peretele piscina | fitness
    (FIX, X2, 0.0, X3, 0.0),                       # fatada nord, fitness
    (PLIN, X2, BARA_A, X3, BARA_A),                # fatada sud, fitness
    # hol
    (PLIN, HOL_X0, 0.0, HOL_X0, ARIPA_Y1),         # latura vest a holului
    (PLIN, HOL_X1, 0.0, HOL_X1, ARIPA_Y1),         # latura est a holului
    (PLIN, HOL_X0, ARIPA_Y1, ARIPA_X1, ARIPA_Y1),  # fatada sud a aripii
    # camerele 5 si 6
    (FIX, HOL_X1, 0.0, ARIPA_X1, 0.0),             # fatada nord, relaxare
    (FIX, ARIPA_X1, 0.0, ARIPA_X1, Y56),           # fatada est, relaxare
    (PLIN, HOL_X1, Y56, ARIPA_X1, Y56),            # relaxare | sauna
    (PLIN, ARIPA_X1, Y56, ARIPA_X1, ARIPA_Y1),     # fatada est, sauna
]

# usi: (x0, y0, x1, y1, eticheta)
USI = [
    (2.9, BARA_A, 3.9, BARA_A, "spre gradina"),
    (9.2, BARA_A, 10.2, BARA_A, "spre gradina"),
    (18.6, 0.0, 19.6, 0.0, "hol -> terasa jacuzzi"),
    (HOL_X0, 4.4, HOL_X0, 5.4, "hol -> fitness"),
    (HOL_X0, 7.2, HOL_X0, 8.2, "intrare din exterior"),
    (HOL_X1, 4.9, HOL_X1, 5.9, "hol -> relaxare"),
    (HOL_X1, 7.6, HOL_X1, 8.6, "hol -> sauna"),
]

# cote: (x0, y0, x1, y1, text, sigur)
COTE = [
    (0.0, BARA_A, X1, BARA_A, "6 m", True),
    (X1, BARA_A, X2, BARA_A, "8 m", True),
    (X2, BARA_A, X3, BARA_A, "4 m", True),
    (0.0, 0.0, 0.0, BARA_A, "6 m", True),
    (HOL_X0, ARIPA_Y1, HOL_X1, ARIPA_Y1, "2 m", False),
    (HOL_X1, ARIPA_Y1, ARIPA_X1, ARIPA_Y1, "5 m", False),
    (ARIPA_X1, 0.0, ARIPA_X1, Y56, "7 m", False),
    (ARIPA_X1, Y56, ARIPA_X1, ARIPA_Y1, "5 m", False),
    (HOL_X0, TERASA_Y0, ARIPA_X1, TERASA_Y0, "7 m", False),
]

CULORI = {
    PLIN: "#141414",
    RETRACTABIL: "#22b3f0",
    FIX: "#2b3fc4",
    "usa": "#c1121f",
}

# --------------------------------------------------------------------------
# transformare lume -> pagina
# --------------------------------------------------------------------------

SCARA = 60.0                       # px / m
MARGINE = 130.0
LEGENDA_H = 420.0
X_MIN, X_MAX = -2.2, 27.2
Y_MIN, Y_MAX = -5.4, 14.2

W = (X_MAX - X_MIN) * SCARA + 2 * MARGINE
H = (Y_MAX - Y_MIN) * SCARA + 2 * MARGINE + LEGENDA_H


def px(x, y):
    return (MARGINE + (x - X_MIN) * SCARA, MARGINE + (y - Y_MIN) * SCARA)


def m(v):
    return v * SCARA


# --------------------------------------------------------------------------
# primitive svg
# --------------------------------------------------------------------------


def rect(x0, y0, x1, y1, **kw):
    a, b = px(x0, y0)
    c, d = px(x1, y1)
    attrs = " ".join('%s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items())
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" %s/>' % (
        a, b, c - a, d - b, attrs)


def line(x0, y0, x1, y1, **kw):
    a, b = px(x0, y0)
    c, d = px(x1, y1)
    attrs = " ".join('%s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items())
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" %s/>' % (a, b, c, d, attrs)


def circle(cx, cy, r, **kw):
    a, b = px(cx, cy)
    attrs = " ".join('%s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items())
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" %s/>' % (a, b, m(r), attrs)


def text(x, y, s, size=20, fill="#141414", anchor="middle", weight="400",
         dy=0.0, style=""):
    a, b = px(x, y)
    return ('<text x="%.1f" y="%.1f" font-family="Helvetica,Arial,sans-serif" '
            'font-size="%s" font-weight="%s" fill="%s" text-anchor="%s" '
            'style="%s">%s</text>') % (a, b + dy, size, weight, fill, anchor,
                                       style, s)


def text_px(a, b, s, size=20, fill="#141414", anchor="start", weight="400"):
    return ('<text x="%.1f" y="%.1f" font-family="Helvetica,Arial,sans-serif" '
            'font-size="%s" font-weight="%s" fill="%s" text-anchor="%s">%s'
            '</text>') % (a, b, size, weight, fill, anchor, s)


# --------------------------------------------------------------------------
# mobilier schematic, doar cat sa se citeasca programul
# --------------------------------------------------------------------------


def mobilier():
    g = ['<g fill="none" stroke="#8a8f98" stroke-width="2.4">']
    s = dict(stroke="#8a8f98", stroke_width="2.4", fill="#eef0f3")

    # 1 - blat de bucatarie pe toata lungimea peretelui plin, gratar la mijloc
    g.append(rect(0.15, 0.5, 0.85, 5.5, **s))
    g.append(rect(0.15, 2.4, 0.85, 3.6, stroke="#8a8f98", stroke_width="2.4",
                  fill="#d8dce2"))
    # masa cu scaune
    g.append(rect(3.0, 2.2, 5.4, 3.8, **s))
    for k in range(4):
        yy = 2.35 + k * 0.45
        g.append(rect(2.55, yy, 2.95, yy + 0.35, **s))
        g.append(rect(5.45, yy, 5.85, yy + 0.35, **s))

    # 2 - piscina 6 x 3, cu trepte la capatul de vest
    g.append(rect(7.0, 1.5, 13.0, 4.5, stroke="#2b3fc4", stroke_width="2.6",
                  fill="#d9edf7"))
    for k in range(3):
        g.append(line(7.0 + 0.35 * k, 1.5, 7.0 + 0.35 * k, 4.5,
                      stroke="#7fb6d4", stroke_width="1.8"))

    # 3 - banda, bench, rastel, doua aparate
    g.append(rect(14.4, 0.5, 15.3, 2.6, **s))          # banda de alergat
    g.append(rect(15.7, 0.5, 17.6, 1.1, **s))          # rastel de greutati
    g.append(rect(15.9, 2.0, 17.4, 2.6, **s))          # bench
    g.append(rect(14.4, 3.4, 15.9, 4.4, **s))          # aparat 1
    g.append(rect(16.2, 3.4, 17.7, 4.4, **s))          # aparat 2

    # 5 - patru paturi de relaxare
    for k in range(2):
        for j in range(2):
            g.append(rect(20.6 + k * 2.3, 1.2 + j * 3.0,
                          21.9 + k * 2.3, 3.0 + j * 3.0, **s))

    # 6 - cabina de sauna cu banci in L, dus rece langa usa
    g.append(rect(21.2, 7.6, 24.5, 11.4, stroke="#8a8f98", stroke_width="2.6",
                  fill="#f3ece2"))
    g.append(rect(21.5, 7.9, 24.2, 8.6, **s))
    g.append(rect(21.5, 8.6, 22.3, 11.1, **s))
    g.append(circle(20.7, 9.6, 0.35, stroke="#8a8f98", stroke_width="2.2",
                    fill="#eef0f3"))

    # 7 - jacuzzi rotund pe terasa
    g.append(circle(21.5, -1.85, 1.15, stroke="#2b3fc4", stroke_width="3.0",
                    fill="#d9edf7"))
    g.append(circle(21.5, -1.85, 0.82, stroke="#7fb6d4", stroke_width="1.8",
                    fill="none"))
    g.append("</g>")
    return g


# --------------------------------------------------------------------------
# desenul
# --------------------------------------------------------------------------


def cota(x0, y0, x1, y1, eticheta, sigur):
    """Linie de cota deportata in afara conturului."""
    col = "#7a3fb8"
    dash = "" if sigur else ' stroke-dasharray="9 6"'
    out = []
    orizontala = abs(y1 - y0) < 1e-6
    d = 1.15
    if orizontala:
        yy = y0 + d if y0 >= 6.0 else y0 - d
        out.append(line(x0, y0, x0, yy, stroke=col, stroke_width="1.4",
                        opacity="0.55"))
        out.append(line(x1, y1, x1, yy, stroke=col, stroke_width="1.4",
                        opacity="0.55"))
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="2.2" marker-start="url(#sg)" '
                   'marker-end="url(#sg)"%s/>'
                   % (px(x0, yy)[0], px(x0, yy)[1], px(x1, yy)[0],
                      px(x1, yy)[1], col, dash))
        out.append(text((x0 + x1) / 2, yy, eticheta, size=25, fill=col,
                        weight="600", dy=-11))
    else:
        xx = x1 + d if x1 >= 18.0 else x0 - d
        out.append(line(x0, y0, xx, y0, stroke=col, stroke_width="1.4",
                        opacity="0.55"))
        out.append(line(x1, y1, xx, y1, stroke=col, stroke_width="1.4",
                        opacity="0.55"))
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="2.2" marker-start="url(#sg)" '
                   'marker-end="url(#sg)"%s/>'
                   % (px(xx, y0)[0], px(xx, y0)[1], px(xx, y1)[0],
                      px(xx, y1)[1], col, dash))
        out.append(text(xx, (y0 + y1) / 2, eticheta, size=25, fill=col,
                        weight="600", dy=8,
                        style="writing-mode:tb;glyph-orientation-vertical:0"))
    return out


def legenda(y0):
    """Legenda si tabelul de suprafete, sub desen."""
    out = []
    x = MARGINE
    out.append(text_px(x, y0, "Cod de culoare", size=27, weight="700"))
    randuri = [
        (CULORI[PLIN], "perete plin"),
        (CULORI[RETRACTABIL], "vitraj retractabil"),
        (CULORI[FIX], "vitraj fix"),
        (CULORI["usa"], "usa"),
    ]
    for k, (col, et) in enumerate(randuri):
        yy = y0 + 42 + k * 38
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="11" stroke-linecap="butt"/>'
                   % (x, yy - 8, x + 66, yy - 8, col))
        out.append(text_px(x + 84, yy, et, size=23, fill="#33383f"))

    x2 = MARGINE + 400
    out.append(text_px(x2, y0, "Suprafete", size=27, weight="700"))
    tabel = [
        ("1  BBQ + bucatarie + masa", "6,0 x 6,0", "36,0 m2"),
        ("2  piscina", "8,0 x 6,0", "48,0 m2"),
        ("3  fitness", "4,0 x 6,0", "24,0 m2"),
        ("4  hol", "2,0 x 12,0", "24,0 m2"),
        ("5  relaxare", "5,0 x 7,0", "35,0 m2"),
        ("6  sauna", "5,0 x 5,0", "25,0 m2"),
        ("7  terasa jacuzzi (exterior)", "7,0 x 3,5", "24,5 m2"),
    ]
    for k, (a, b, c) in enumerate(tabel):
        yy = y0 + 42 + k * 32
        out.append(text_px(x2, yy, a, size=22, fill="#33383f"))
        out.append(text_px(x2 + 400, yy, b, size=22, fill="#6b7076",
                           anchor="end"))
        out.append(text_px(x2 + 560, yy, c, size=22, fill="#33383f",
                           anchor="end"))
    yy = y0 + 42 + 7 * 32 + 14
    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#c9ced4" '
               'stroke-width="1.6"/>' % (x2, yy - 22, x2 + 560, yy - 22))
    out.append(text_px(x2, yy, "construit sub acoperis", size=22,
                       weight="700"))
    out.append(text_px(x2 + 560, yy, "192,0 m2", size=22, weight="700",
                       anchor="end"))

    x3 = MARGINE + 1130
    out.append(text_px(x3, y0, "Note", size=27, weight="700"))
    note = [
        "Cotele cu mov continuu (6 / 8 / 4 / 6 m) sunt cele din schita.",
        "Cotele punctate sunt citite la scara din desen si raman de confirmat.",
        "1 si 2 sunt un singur spatiu, fara perete intre ele.",
        "3 nu are usa spre 2: legatura piscina - hol trece prin exterior.",
        "Nordul este in sus; fatadele lungi ale barei privesc nord si sud.",
    ]
    for k, n in enumerate(note):
        out.append(text_px(x3, y0 + 42 + k * 32, n, size=21, fill="#33383f"))
    return out


def construieste_svg():
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
         'viewBox="0 0 %.0f %.0f">' % (W, H, W, H)]
    o.append('<defs><marker id="sg" viewBox="0 0 10 10" refX="5" refY="5" '
             'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M 0 0 L 10 5 L 0 10 z" fill="#7a3fb8"/></marker></defs>')
    o.append('<rect width="%.0f" height="%.0f" fill="#ffffff"/>' % (W, H))

    # caroiaj de un metru
    o.append('<g stroke="#eceef1" stroke-width="1">')
    x = int(X_MIN)
    while x <= X_MAX:
        o.append(line(x, Y_MIN, x, Y_MAX))
        x += 1
    y = int(Y_MIN)
    while y <= Y_MAX:
        o.append(line(X_MIN, y, X_MAX, y))
        y += 1
    o.append("</g>")

    # pardoseli
    for nr, _, x0, y0, x1, y1 in COMPARTIMENTE:
        fill = "#f2ede4" if nr == "7" else "#fbfbfc"
        o.append(rect(x0, y0, x1, y1, fill=fill, stroke="none"))
    # terasa exterioara: contur punctat, nu e volum inchis
    o.append(rect(HOL_X0, TERASA_Y0, ARIPA_X1, 0.0, fill="none",
                  stroke="#a9a293", stroke_width="2.4", stroke_dasharray="10 7"))

    o.extend(mobilier())

    # pereti
    o.append('<g stroke-linecap="butt">')
    for tip, x0, y0, x1, y1 in PERETI:
        o.append(line(x0, y0, x1, y1, stroke=CULORI[tip], stroke_width="10"))
    o.append("</g>")

    # usi peste pereti
    o.append('<g stroke-linecap="butt">')
    for x0, y0, x1, y1, _ in USI:
        o.append(line(x0, y0, x1, y1, stroke="#ffffff", stroke_width="14"))
        o.append(line(x0, y0, x1, y1, stroke=CULORI["usa"], stroke_width="10"))
    o.append("</g>")

    # numere si nume
    etichete = {
        "1": (3.0, 4.9), "2": (10.0, 5.3), "3": (16.0, 5.3),
        "4": (19.0, 2.2), "5": (22.5, 5.0), "6": (22.9, 9.3),
        "7": (23.9, -2.7),
    }
    for nr, nume, x0, y0, x1, y1 in COMPARTIMENTE:
        cx, cy = etichete[nr]
        o.append(text(cx, cy, nr, size=78, weight="700", fill="#1d2126",
                      style="opacity:0.16"))
        o.append(text(cx, cy + 0.42, nume, size=24, weight="600",
                      fill="#3b4149"))

    # cote
    for c in COTE:
        o.extend(cota(*c))

    # sageata de nord
    nx, ny = px(-1.2, -4.4)
    o.append('<g transform="translate(%.1f,%.1f)">'
             '<path d="M 0 -34 L 12 20 L 0 10 L -12 20 z" fill="#3b4149"/>'
             '<text x="0" y="46" font-family="Helvetica,Arial,sans-serif" '
             'font-size="24" font-weight="700" fill="#3b4149" '
             'text-anchor="middle">N</text></g>' % (nx, ny))

    o.append(text_px(MARGINE, 62, "Casa Dealu Negru - zona wellness, plan",
                     size=38, weight="700"))
    o.append(text_px(MARGINE, 98,
                     "7 compartimente, scara 1:100 la 60 px/m",
                     size=24, fill="#6b7076"))

    o.extend(legenda(H - LEGENDA_H + 40))
    o.append("</svg>")
    return "\n".join(o)


def rasterizeaza(svg_path, png_path):
    """PNG prin Chromium headless, daca exista. Altfel doar SVG-ul."""
    candidati = [
        "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
        "/opt/pw-browsers/chromium/chrome-linux/chrome",
        "chromium", "chromium-browser", "google-chrome",
    ]
    for c in candidati:
        exe = c if os.path.isabs(c) else _which(c)
        if not exe or not os.path.exists(exe):
            continue
        cmd = [exe, "--headless", "--disable-gpu", "--no-sandbox",
               "--hide-scrollbars", "--default-background-color=ffffff",
               "--force-device-scale-factor=1",
               "--window-size=%d,%d" % (int(W), int(H)),
               "--screenshot=" + png_path, "file://" + os.path.abspath(svg_path)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=180)
            return png_path
        except Exception:
            continue
    return None


def _which(name):
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = os.path.join(d, name)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    outdir = os.path.join(root, "renders")
    os.makedirs(outdir, exist_ok=True)
    svg_path = os.path.join(outdir, "plan_compartimente.svg")
    with open(svg_path, "w") as fh:
        fh.write(construieste_svg())
    print("scris", svg_path)
    png = rasterizeaza(svg_path, os.path.join(outdir, "plan_compartimente.png"))
    if png:
        print("scris", png)
    else:
        print("Chromium nu a fost gasit - a iesit doar SVG-ul.", file=sys.stderr)


if __name__ == "__main__":
    main()
