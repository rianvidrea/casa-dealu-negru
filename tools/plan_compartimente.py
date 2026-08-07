#!/usr/bin/env python3
"""Planul zonei wellness, revizia 2 — 8 compartimente.

Reface schita de mana in cote reale. Cod de culoare pastrat din prima schita:
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

X12 = 7.0                          # rostul dintre 1 si 2
BARA_L, BARA_A = 15.0, 6.0         # bara lunga: 7 + 8, adancime 6

ARIPA_X0, ARIPA_X1 = 15.0, 25.0    # aripa, 10 m latime (25 total - 15 bara)
ARIPA_Y1 = 12.0                    # aripa, 12 m adancime
HOL_X1 = 16.0                      # holul: 1 m latime
Y_JOS = 7.0                        # rostul dintre 5 si zona de jos
X_SAUNA_FIT = 20.0                 # rostul dintre zona saunei si fitness

BAIE_X0, BAIE_X1 = 16.0, 18.0      # baia: 1 m circulatie + 1 m cabine
BAIE_Y0, BAIE_Y1 = 3.3, 6.7        # 0,9 + 0,8 + 0,8 + 0,9 = 3,4 m

CAB_X1 = 18.5                      # cabina de sauna, 2,5 m
CAB_Y0 = 10.0                      # cabina de sauna, 2 m adancime

TERASA_X0, TERASA_X1 = 16.0, 22.0  # terasa jacuzzi, 6 m
TERASA_Y0 = -3.0                   # terasa jacuzzi, 3 m spre nord

COMPARTIMENTE = [
    ("1", "BBQ + bucatarie", 0.0, 0.0, X12, BARA_A),
    ("2", "piscina", X12, 0.0, BARA_L, BARA_A),
    ("4", "hol", ARIPA_X0, 0.0, HOL_X1, ARIPA_Y1),
    ("5", "relaxare", HOL_X1, 0.0, ARIPA_X1, Y_JOS),
    ("8", "bai", BAIE_X0, BAIE_Y0, BAIE_X1, BAIE_Y1),
    ("6", "sauna", HOL_X1, Y_JOS, X_SAUNA_FIT, ARIPA_Y1),
    ("3", "fitness", X_SAUNA_FIT, Y_JOS, ARIPA_X1, ARIPA_Y1),
    ("7", "jacuzzi", TERASA_X0, TERASA_Y0, TERASA_X1, 0.0),
]

PLIN, RETRACTABIL, FIX = "plin", "retractabil", "fix"

PERETI = [
    # bara lunga
    (PLIN, 0.0, 0.0, 0.0, BARA_A),                       # peretele negru, BBQ
    (RETRACTABIL, 0.0, 0.0, BARA_L, 0.0),                # fatada nord
    (RETRACTABIL, 0.0, BARA_A, BARA_L, BARA_A),          # fatada sud
    # aripa, contur
    (PLIN, ARIPA_X0, 0.0, ARIPA_X0, ARIPA_Y1),           # latura vest
    (PLIN, ARIPA_X0, ARIPA_Y1, ARIPA_X1, ARIPA_Y1),      # fatada sud
    (PLIN, ARIPA_X0, 0.0, HOL_X1, 0.0),                  # capul de nord al holului
    (FIX, HOL_X1, 0.0, ARIPA_X1, 0.0),                   # fatada nord, relaxare
    (FIX, ARIPA_X1, 0.0, ARIPA_X1, Y_JOS),               # fatada est, relaxare
    (FIX, ARIPA_X1, Y_JOS, ARIPA_X1, ARIPA_Y1),          # fatada est, fitness
    # compartimentari
    (PLIN, HOL_X1, 0.0, HOL_X1, ARIPA_Y1),               # latura est a holului
    (PLIN, HOL_X1, Y_JOS, ARIPA_X1, Y_JOS),              # 5 | zona de jos
    (PLIN, X_SAUNA_FIT, Y_JOS, X_SAUNA_FIT, ARIPA_Y1),   # sauna | fitness
    # baia
    (PLIN, BAIE_X0, BAIE_Y0, BAIE_X1, BAIE_Y0),
    (PLIN, BAIE_X0, BAIE_Y1, BAIE_X1, BAIE_Y1),
    (PLIN, BAIE_X1, BAIE_Y0, BAIE_X1, BAIE_Y1),
]

# usi: (x0, y0, x1, y1, eticheta)
USI = [
    (2.9, BARA_A, 3.9, BARA_A, "1 -> gradina"),
    (9.6, BARA_A, 10.6, BARA_A, "2 -> gradina"),
    (ARIPA_X0, 0.0, HOL_X1, 0.0, "hol -> terasa jacuzzi"),
    (ARIPA_X0, 4.8, ARIPA_X0, 5.8, "piscina -> hol"),
    (HOL_X1, 2.6, HOL_X1, 3.6, "hol -> relaxare"),
    (HOL_X1, 5.2, HOL_X1, 6.2, "hol -> bai"),
    (HOL_X1, 7.4, HOL_X1, 8.4, "hol -> sauna"),
    (HOL_X1, 10.2, HOL_X1, 11.2, "hol -> cabina de sauna"),
]

# cote: (x0, y0, x1, y1, text, sigur, decalaj)
COTE = [
    (0.0, 0.0, ARIPA_X1, 0.0, "25 m", True, -5.2),
    (0.0, 0.0, X12, 0.0, "7 m", True, -1.4),
    (X12, 0.0, BARA_L, 0.0, "8 m", True, -1.4),
    (TERASA_X1, 0.0, ARIPA_X1, 0.0, "3 m", True, -1.4),
    (TERASA_X0, TERASA_Y0, TERASA_X1, TERASA_Y0, "6 m", True, -1.2),
    (0.0, 0.0, 0.0, BARA_A, "6 m", True, -1.5),
    (ARIPA_X1, 0.0, ARIPA_X1, ARIPA_Y1, "12 m", True, 3.0),
    (ARIPA_X1, Y_JOS, ARIPA_X1, ARIPA_Y1, "5 m", True, 1.4),
    (ARIPA_X1, 0.0, ARIPA_X1, Y_JOS, "7 m", False, 1.4),
    (ARIPA_X0, ARIPA_Y1, HOL_X1, ARIPA_Y1, "1 m", True, 1.3),
    (HOL_X1, ARIPA_Y1, CAB_X1, ARIPA_Y1, "2,5 m", True, 1.3),
    (CAB_X1, ARIPA_Y1, X_SAUNA_FIT, ARIPA_Y1, "1,5 m", True, 1.3),
    (X_SAUNA_FIT, ARIPA_Y1, ARIPA_X1, ARIPA_Y1, "5 m", True, 1.3),
]

# cabinele din baie: (eticheta, latime in m)
CABINE = [("DUS", 0.9), ("WC", 0.8), ("WC", 0.8), ("DUS", 0.9)]

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
LEGENDA_H = 480.0
X_MIN, X_MAX = -3.0, 29.5
Y_MIN, Y_MAX = -6.6, 14.6

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

    # 1 - blat pe toata lungimea peretelui plin, gratar la mijloc, masa
    g.append(rect(0.15, 0.5, 0.85, 5.5, **s))
    g.append(rect(0.15, 2.4, 0.85, 3.6, stroke="#8a8f98", stroke_width="2.4",
                  fill="#d8dce2"))
    g.append(rect(3.4, 2.2, 5.8, 3.8, **s))
    for k in range(4):
        yy = 2.35 + k * 0.45
        g.append(rect(2.95, yy, 3.35, yy + 0.35, **s))
        g.append(rect(5.85, yy, 6.25, yy + 0.35, **s))

    # 2 - piscina 6 x 3, cu trepte la capatul de vest
    g.append(rect(8.0, 1.5, 14.0, 4.5, stroke="#2b3fc4", stroke_width="2.6",
                  fill="#d9edf7"))
    for k in range(3):
        g.append(line(8.0 + 0.35 * k, 1.5, 8.0 + 0.35 * k, 4.5,
                      stroke="#7fb6d4", stroke_width="1.8"))

    # 5 - sase paturi de relaxare si un grup de sezut spre coltul vitrat
    for k in range(3):
        for j in range(2):
            g.append(rect(19.0 + k * 2.0, 0.5 + j * 2.2,
                          20.3 + k * 2.0, 2.3 + j * 2.2, **s))
    g.append(rect(16.6, 0.6, 17.8, 2.6, **s))
    g.append(rect(16.6, 3.0, 17.8, 3.1, **s))

    # 8 - patru cabine de 1 m adancime plus doua chiuvete pe fasia de 1 m
    y = BAIE_Y0
    for eticheta, lat in CABINE:
        g.append(rect(BAIE_X0 + 1.0, y, BAIE_X1, y + lat, **s))
        g.append(text(BAIE_X0 + 1.5, y + lat / 2.0, eticheta, size=15,
                      fill="#5c6169", weight="600", dy=5))
        y += lat
    for k in range(2):
        g.append(rect(BAIE_X0 + 0.02, 3.6 + k * 2.2, BAIE_X0 + 0.45,
                      4.2 + k * 2.2, **s))

    # 6 - cabina de sauna cu banci in L, dus rece pe fasia de 1,5 m
    g.append(rect(HOL_X1 + 0.05, CAB_Y0, CAB_X1, ARIPA_Y1 - 0.05,
                  stroke="#8a8f98", stroke_width="2.6", fill="#f3ece2"))
    g.append(rect(HOL_X1 + 0.3, CAB_Y0 + 0.25, CAB_X1 - 0.25, CAB_Y0 + 0.85, **s))
    g.append(rect(CAB_X1 - 0.85, CAB_Y0 + 0.85, CAB_X1 - 0.25,
                  ARIPA_Y1 - 0.35, **s))
    g.append(circle(19.25, 11.3, 0.35, stroke="#8a8f98", stroke_width="2.2",
                    fill="#eef0f3"))
    g.append(rect(16.4, 7.6, 18.6, 8.3, **s))          # banca de racorire

    # 3 - banda, bench, rastel, doua aparate
    g.append(rect(20.4, 7.4, 21.3, 9.5, **s))
    g.append(rect(21.8, 7.4, 24.6, 8.0, **s))
    g.append(rect(22.2, 8.8, 23.7, 9.4, **s))
    g.append(rect(20.4, 10.3, 21.9, 11.4, **s))
    g.append(rect(22.4, 10.3, 23.9, 11.4, **s))

    # 7 - jacuzzi rotund pe terasa
    g.append(circle(19.0, -1.5, 1.15, stroke="#2b3fc4", stroke_width="3.0",
                    fill="#d9edf7"))
    g.append(circle(19.0, -1.5, 0.82, stroke="#7fb6d4", stroke_width="1.8",
                    fill="none"))
    g.append("</g>")
    return g


# --------------------------------------------------------------------------
# desenul
# --------------------------------------------------------------------------


def cota(x0, y0, x1, y1, eticheta, sigur, d):
    col = "#7a3fb8"
    dash = "" if sigur else ' stroke-dasharray="9 6"'
    out = []
    orizontala = abs(y1 - y0) < 1e-6
    if orizontala:
        yy = y0 + d
        out.append(line(x0, y0, x0, yy, stroke=col, stroke_width="1.4",
                        opacity="0.5"))
        out.append(line(x1, y1, x1, yy, stroke=col, stroke_width="1.4",
                        opacity="0.5"))
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="2.2" marker-start="url(#sg)" '
                   'marker-end="url(#sg)"%s/>'
                   % (px(x0, yy)[0], px(x0, yy)[1], px(x1, yy)[0],
                      px(x1, yy)[1], col, dash))
        out.append(text((x0 + x1) / 2, yy, eticheta, size=25, fill=col,
                        weight="600", dy=-11))
    else:
        xx = x0 + d
        out.append(line(x0, y0, xx, y0, stroke=col, stroke_width="1.4",
                        opacity="0.5"))
        out.append(line(x1, y1, xx, y1, stroke=col, stroke_width="1.4",
                        opacity="0.5"))
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="2.2" marker-start="url(#sg)" '
                   'marker-end="url(#sg)"%s/>'
                   % (px(xx, y0)[0], px(xx, y0)[1], px(xx, y1)[0],
                      px(xx, y1)[1], col, dash))
        out.append(text(xx, (y0 + y1) / 2, eticheta, size=25, fill=col,
                        weight="600", dy=8,
                        style="writing-mode:tb;glyph-orientation-vertical:0"))
    return out


TABEL = [
    ("1  BBQ + bucatarie + masa", "7,0 x 6,0", "42,0"),
    ("2  piscina", "8,0 x 6,0", "48,0"),
    ("3  fitness", "5,0 x 5,0", "25,0"),
    ("4  hol", "1,0 x 12,0", "12,0"),
    ("5  relaxare", "9,0 x 7,0 - baia", "56,2"),
    ("6  sauna, cu cabina de 2,5 x 2,0", "4,0 x 5,0", "20,0"),
    ("8  bai: 2 dusuri, 2 WC, 2 chiuvete", "2,0 x 3,4", "6,8"),
    ("7  terasa jacuzzi (exterior)", "6,0 x 3,0", "18,0"),
]

NOTE = [
    "Cotele cu mov continuu sunt cele scrise pe schita.",
    "Cotele punctate ies din scadere si raman de confirmat.",
    "1 si 2 sunt un singur spatiu, fara perete intre ele.",
    "Baia: fasie de 1,0 m cu chiuvetele, plus 4 cabine de 1,0 m adancime",
    "   (dus 90, WC 80, WC 80, dus 90 cm), in total 2,0 x 3,4 m.",
    "Vitrajele sunt preluate din prima schita; a doua nu le mai coloreaza.",
    "3 nu are usa desenata: singurul acces ramane prin 6.",
    "Nordul este in sus; fatadele lungi ale barei privesc nord si sud.",
]


def legenda(y0):
    out = []
    x = MARGINE
    out.append(text_px(x, y0, "Cod de culoare", size=27, weight="700"))
    for k, (col, et) in enumerate([
            (CULORI[PLIN], "perete plin"),
            (CULORI[RETRACTABIL], "vitraj retractabil"),
            (CULORI[FIX], "vitraj fix"),
            (CULORI["usa"], "usa")]):
        yy = y0 + 42 + k * 38
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="11"/>' % (x, yy - 8, x + 66, yy - 8, col))
        out.append(text_px(x + 84, yy, et, size=23, fill="#33383f"))

    x2 = MARGINE + 400
    out.append(text_px(x2, y0, "Suprafete", size=27, weight="700"))
    for k, (a, b, c) in enumerate(TABEL):
        yy = y0 + 42 + k * 32
        out.append(text_px(x2, yy, a, size=22, fill="#33383f"))
        out.append(text_px(x2 + 460, yy, b, size=22, fill="#6b7076",
                           anchor="end"))
        out.append(text_px(x2 + 610, yy, c + " m2", size=22, fill="#33383f",
                           anchor="end"))
    yy = y0 + 42 + len(TABEL) * 32 + 14
    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#c9ced4" '
               'stroke-width="1.6"/>' % (x2, yy - 22, x2 + 610, yy - 22))
    out.append(text_px(x2, yy, "construit sub acoperis", size=22, weight="700"))
    out.append(text_px(x2 + 610, yy, "210,0 m2", size=22, weight="700",
                       anchor="end"))

    x3 = MARGINE + 1230
    out.append(text_px(x3, y0, "Note", size=27, weight="700"))
    for k, n in enumerate(NOTE):
        out.append(text_px(x3, y0 + 42 + k * 32, n, size=21, fill="#33383f"))
    return out


def construieste_svg():
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
         'viewBox="0 0 %.0f %.0f">' % (W, H, W, H)]
    o.append('<defs><marker id="sg" viewBox="0 0 10 10" refX="5" refY="5" '
             'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M 0 0 L 10 5 L 0 10 z" fill="#7a3fb8"/></marker></defs>')
    o.append('<rect width="%.0f" height="%.0f" fill="#ffffff"/>' % (W, H))

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

    for nr, _, x0, y0, x1, y1 in COMPARTIMENTE:
        fill = "#f2ede4" if nr == "7" else "#fbfbfc"
        o.append(rect(x0, y0, x1, y1, fill=fill, stroke="none"))
    # podestul de 1 m din fata usii holului, in aceeasi pardoseala ca terasa
    o.append(rect(ARIPA_X0, TERASA_Y0 + 2.0, TERASA_X0, 0.0, fill="#f2ede4",
                  stroke="none"))
    o.append(rect(TERASA_X0, TERASA_Y0, TERASA_X1, 0.0, fill="none",
                  stroke="#a9a293", stroke_width="2.4", stroke_dasharray="10 7"))
    o.append(rect(ARIPA_X0, TERASA_Y0 + 2.0, TERASA_X0, 0.0, fill="none",
                  stroke="#a9a293", stroke_width="2.4", stroke_dasharray="10 7"))

    o.extend(mobilier())

    o.append('<g stroke-linecap="butt">')
    for tip, x0, y0, x1, y1 in PERETI:
        o.append(line(x0, y0, x1, y1, stroke=CULORI[tip], stroke_width="10"))
    o.append("</g>")

    o.append('<g stroke-linecap="butt">')
    for x0, y0, x1, y1, _ in USI:
        o.append(line(x0, y0, x1, y1, stroke="#ffffff", stroke_width="14"))
        o.append(line(x0, y0, x1, y1, stroke=CULORI["usa"], stroke_width="10"))
    o.append("</g>")

    etichete = {
        "1": (3.5, 5.0), "2": (11.0, 5.3), "3": (22.5, 9.9),
        "4": (15.5, 2.0), "5": (21.0, 5.6), "6": (17.9, 8.9),
        "7": (20.9, -1.5), "8": (17.0, 5.0),
    }
    dimensiuni = {"8": 44, "4": 52}
    for nr, nume, x0, y0, x1, y1 in COMPARTIMENTE:
        cx, cy = etichete[nr]
        o.append(text(cx, cy, nr, size=dimensiuni.get(nr, 78), weight="700",
                      fill="#1d2126", style="opacity:0.17"))
        o.append(text(cx, cy + (0.30 if nr in dimensiuni else 0.42), nume,
                      size=21 if nr in dimensiuni else 24, weight="600",
                      fill="#3b4149"))

    for c in COTE:
        o.extend(cota(*c))

    nx, ny = px(-1.8, -5.4)
    o.append('<g transform="translate(%.1f,%.1f)">'
             '<path d="M 0 -34 L 12 20 L 0 10 L -12 20 z" fill="#3b4149"/>'
             '<text x="0" y="46" font-family="Helvetica,Arial,sans-serif" '
             'font-size="24" font-weight="700" fill="#3b4149" '
             'text-anchor="middle">N</text></g>' % (nx, ny))

    o.append(text_px(MARGINE, 62, "Casa Dealu Negru — zona wellness, plan rev. 2",
                     size=38, weight="700"))
    o.append(text_px(MARGINE, 98,
                     "8 compartimente, 25 x 6 m bara + 10 x 12 m aripa, "
                     "scara 1:100 la 60 px/m", size=24, fill="#6b7076"))

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
