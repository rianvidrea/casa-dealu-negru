#!/usr/bin/env python3
"""Planul zonei wellness, revizia 3 — 8 compartimente.

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

X12 = 10.0                         # rostul dintre 1 si 2
BARA_L, BARA_A = 19.0, 6.0         # bara lunga: 10 + 9, adancime 6

ARIPA_X0, ARIPA_X1 = 19.0, 25.0    # aripa, 6 m latime (25 total - 19 bara)
ARIPA_Y1 = 12.0                    # aripa, 12 m adancime
HOL_X1 = 20.0                      # holul: 1 m latime
Y_JOS = 7.0                        # rostul dintre 5 si zona de jos

BAIE_X0, BAIE_X1 = 20.0, 22.0      # baia: 1 m circulatie + 1 m cabine
BAIE_Y0, BAIE_Y1 = 3.3, 6.7        # 0,9 + 0,8 + 0,8 + 0,9 = 3,4 m

CAB_X1 = 22.5                      # cabina de sauna, 2,5 m
CAB_Y0 = 10.0                      # cabina de sauna, 2 m adancime

TERASA_X0, TERASA_X1 = 19.0, 25.0  # terasa jacuzzi, 6 m, toata latimea aripii
TERASA_Y0 = -3.0                   # terasa jacuzzi, 3 m spre nord, cotat
TERASA_Y_NEC = -5.0                # cat i-ar trebui ca sa incapa cada de 4,5
JACUZZI_D = 4.5                    # diametrul scris cu galben pe schita

COMPARTIMENTE = [
    ("1", "BBQ + bucatarie", 0.0, 0.0, X12, BARA_A),
    ("2", "piscina", X12, 0.0, BARA_L, BARA_A),
    ("4", "hol", ARIPA_X0, 0.0, HOL_X1, ARIPA_Y1),
    ("5", "relaxare", HOL_X1, 0.0, ARIPA_X1, Y_JOS),
    ("8", "bai", BAIE_X0, BAIE_Y0, BAIE_X1, BAIE_Y1),
    ("3", "fitness", HOL_X1, Y_JOS, ARIPA_X1, ARIPA_Y1),
    ("6", "sauna", HOL_X1, CAB_Y0, CAB_X1, ARIPA_Y1),
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
    (PLIN, HOL_X1, CAB_Y0, CAB_X1, CAB_Y0),              # cabina de sauna, nord
    (PLIN, CAB_X1, CAB_Y0, CAB_X1, ARIPA_Y1),            # cabina de sauna, est
    # baia
    (PLIN, BAIE_X0, BAIE_Y0, BAIE_X1, BAIE_Y0),
    (PLIN, BAIE_X0, BAIE_Y1, BAIE_X1, BAIE_Y1),
    (PLIN, BAIE_X1, BAIE_Y0, BAIE_X1, BAIE_Y1),
]

# usi: (x0, y0, x1, y1, eticheta)
USI = [
    (3.9, BARA_A, 4.9, BARA_A, "1 -> gradina"),
    (12.6, BARA_A, 13.6, BARA_A, "2 -> gradina"),
    (ARIPA_X0, 0.0, HOL_X1, 0.0, "hol -> terasa jacuzzi"),
    (ARIPA_X0, 4.8, ARIPA_X0, 5.8, "piscina -> hol"),
    (HOL_X1, 2.6, HOL_X1, 3.6, "hol -> relaxare"),
    (HOL_X1, 5.2, HOL_X1, 6.2, "hol -> bai"),
    (HOL_X1, 7.6, HOL_X1, 8.6, "hol -> fitness"),
    (HOL_X1, 10.4, HOL_X1, 11.4, "hol -> sauna"),
]

# cote: (x0, y0, x1, y1, text, sigur, decalaj)
COTE = [
    (0.0, 0.0, ARIPA_X1, 0.0, "25 m", True, -6.6),
    (0.0, 0.0, X12, 0.0, "10 m", True, -1.4),
    (X12, 0.0, BARA_L, 0.0, "9 m", True, -1.4),
    (TERASA_X0, TERASA_Y_NEC, TERASA_X1, TERASA_Y_NEC, "6 m", True, -1.2),
    (TERASA_X0, TERASA_Y0, TERASA_X0, 0.0, "3 m", True, -1.4),
    (0.0, 0.0, 0.0, BARA_A, "6 m", True, -1.5),
    (ARIPA_X1, 0.0, ARIPA_X1, ARIPA_Y1, "12 m", True, 3.0),
    (ARIPA_X1, Y_JOS, ARIPA_X1, ARIPA_Y1, "5 m", True, 1.4),
    (ARIPA_X1, 0.0, ARIPA_X1, Y_JOS, "7 m", False, 1.4),
    (BAIE_X0, BAIE_Y0, BAIE_X1, BAIE_Y0, "2 m", True, -0.9),
    (ARIPA_X0, ARIPA_Y1, HOL_X1, ARIPA_Y1, "1 m", True, 1.3),
    (HOL_X1, ARIPA_Y1, CAB_X1, ARIPA_Y1, "2,5 m", True, 1.3),
    (CAB_X1, ARIPA_Y1, ARIPA_X1, ARIPA_Y1, "2,5 m", True, 1.3),
    (ARIPA_X0, ARIPA_Y1, ARIPA_X1, ARIPA_Y1, "6 m", True, 3.0),
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
Y_MIN, Y_MAX = -8.2, 15.0

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
    g.append(rect(4.3, 2.1, 7.3, 3.9, **s))
    for k in range(5):
        yy = 2.25 + k * 0.36
        g.append(rect(3.85, yy, 4.25, yy + 0.3, **s))
        g.append(rect(7.35, yy, 7.75, yy + 0.3, **s))

    # 2 - piscina 6 x 3, cu trepte la capatul de vest
    g.append(rect(11.5, 1.5, 17.5, 4.5, stroke="#2b3fc4", stroke_width="2.6",
                  fill="#d9edf7"))
    for k in range(3):
        g.append(line(11.5 + 0.35 * k, 1.5, 11.5 + 0.35 * k, 4.5,
                      stroke="#7fb6d4", stroke_width="1.8"))

    # 5 - patru paturi de relaxare, doua sub fatada de nord, doua la est
    for k in range(2):
        g.append(rect(20.4 + k * 2.3, 0.35, 21.7 + k * 2.3, 2.15, **s))
    for k in range(2):
        g.append(rect(22.6, 2.7 + k * 2.0, 24.7, 4.0 + k * 2.0, **s))

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

    # 6 - cabina de sauna 2,5 x 2 cu banci in L
    g.append(rect(HOL_X1 + 0.05, CAB_Y0 + 0.05, CAB_X1 - 0.05, ARIPA_Y1 - 0.05,
                  stroke="#8a8f98", stroke_width="2.6", fill="#f3ece2"))
    g.append(rect(HOL_X1 + 0.25, CAB_Y0 + 0.25, CAB_X1 - 0.25, CAB_Y0 + 0.8, **s))
    g.append(rect(CAB_X1 - 0.85, CAB_Y0 + 0.8, CAB_X1 - 0.25,
                  ARIPA_Y1 - 0.3, **s))

    # 3 - sala, in L in jurul cabinei de sauna; dus rece langa usa saunei
    g.append(rect(20.3, 7.3, 21.2, 9.4, **s))          # banda de alergat
    g.append(rect(21.7, 7.3, 24.7, 7.9, **s))          # rastel de greutati
    g.append(rect(23.0, 8.5, 24.5, 9.1, **s))          # bench
    g.append(rect(22.9, 9.9, 24.7, 10.9, **s))         # aparat 1
    g.append(rect(22.9, 11.0, 24.7, 11.8, **s))        # aparat 2
    g.append(circle(24.4, 9.5, 0.3, stroke="#8a8f98", stroke_width="2.2",
                    fill="#eef0f3"))                   # dus rece

    # 7 - jacuzzi rotund, diametrul scris pe schita
    cx, cy = (TERASA_X0 + TERASA_X1) / 2.0, TERASA_Y_NEC / 2.0
    g.append(circle(cx, cy, JACUZZI_D / 2.0, stroke="#2b3fc4",
                    stroke_width="3.0", fill="#d9edf7"))
    g.append(circle(cx, cy, JACUZZI_D / 2.0 - 0.35, stroke="#7fb6d4",
                    stroke_width="1.8", fill="none"))
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
    ("1  BBQ + bucatarie + masa", "10,0 x 6,0", "60,0"),
    ("2  piscina", "9,0 x 6,0", "54,0"),
    ("3  sala, in L in jurul saunei", "5,0 x 5,0 - sauna", "20,0"),
    ("4  hol", "1,0 x 12,0", "12,0"),
    ("5  relaxare", "5,0 x 7,0 - baia", "28,2"),
    ("6  sauna", "2,5 x 2,0", "5,0"),
    ("8  bai: 2 dusuri, 2 WC, 2 chiuvete", "2,0 x 3,4", "6,8"),
    ("7  terasa jacuzzi (exterior)", "6,0 x 3,0", "18,0"),
]

NOTE = [
    "Cotele cu mov continuu sunt cele scrise pe schita.",
    "Cotele punctate ies din scadere si raman de confirmat.",
    "1 si 2 sunt un singur spatiu, fara perete intre ele.",
    "Baia: fasie de 1,0 m cu chiuvetele, plus 4 cabine de 1,0 m adancime",
    "   (dus 90, WC 80, WC 80, dus 90 cm), in total 2,0 x 3,4 m.",
    "Cada de 4,5 m nu incape pe terasa de 3 m: ii trebuie 5 m adancime.",
    "   Punctat subtire, conturul terasei de care ar fi nevoie.",
    "Vitrajele sunt preluate din prima schita; a doua nu le mai coloreaza.",
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
    out.append(text_px(x2 + 610, yy, "186,0 m2", size=22, weight="700",
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
    # terasa de care ar fi nevoie ca sa incapa cada de 4,5 m
    o.append(rect(TERASA_X0, TERASA_Y_NEC, TERASA_X1, TERASA_Y0,
                  fill="#f7f3ec", stroke="none"))
    o.append(rect(TERASA_X0, TERASA_Y_NEC, TERASA_X1, 0.0, fill="none",
                  stroke="#c9b98f", stroke_width="1.8", stroke_dasharray="5 6"))
    # terasa asa cum e cotata
    o.append(rect(TERASA_X0, TERASA_Y0, TERASA_X1, 0.0, fill="none",
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
        "1": (5.8, 5.2), "2": (14.5, 5.4), "3": (22.1, 9.1),
        "4": (19.5, 2.2), "5": (23.4, 6.1), "6": (21.25, 11.0),
        "7": (19.9, -4.2), "8": (21.0, 5.0),
    }
    dimensiuni = {"8": 44, "4": 52, "6": 44}
    for nr, nume, x0, y0, x1, y1 in COMPARTIMENTE:
        cx, cy = etichete[nr]
        o.append(text(cx, cy, nr, size=dimensiuni.get(nr, 78), weight="700",
                      fill="#1d2126", style="opacity:0.17"))
        o.append(text(cx, cy + (0.30 if nr in dimensiuni else 0.42), nume,
                      size=21 if nr in dimensiuni else 24, weight="600",
                      fill="#3b4149"))

    for c in COTE:
        o.extend(cota(*c))

    nx, ny = px(-1.8, -6.8)
    o.append('<g transform="translate(%.1f,%.1f)">'
             '<path d="M 0 -34 L 12 20 L 0 10 L -12 20 z" fill="#3b4149"/>'
             '<text x="0" y="46" font-family="Helvetica,Arial,sans-serif" '
             'font-size="24" font-weight="700" fill="#3b4149" '
             'text-anchor="middle">N</text></g>' % (nx, ny))

    o.append(text_px(MARGINE, 62, "Casa Dealu Negru — zona wellness, plan rev. 3",
                     size=38, weight="700"))
    o.append(text_px(MARGINE, 98,
                     "8 compartimente, bara de 19 x 6 m + aripa de 6 x 12 m, "
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
