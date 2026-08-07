#!/usr/bin/env python3
"""Planul combinat: demisolul desenat plin, parterul suprapus in contur subtire.

Cotele demisolului nu sunt scrise pe schita de mana; se scot masurand schita
fata de conturul negru al partii de sus, care are cote cunoscute (bara 19 x 6,
aripa 6 x 12). De aceea toate cotele demisolului sunt marcate punctat.

Geometria partii de sus vine din `plan_compartimente`, ca cele doua planuri sa
nu poata pleca unul de la celalalt.

    python3 tools/plan_combinat.py
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import plan_compartimente as P

# --------------------------------------------------------------------------
# geometria demisolului, in metri, in acelasi sistem ca parterul
# --------------------------------------------------------------------------

CAMD = (0.0, 6.0, 19.0, 12.0)        # camera de depozitare, sub terasa
CAMJ = (19.0, 0.0, 25.0, 12.0)       # camera de joaca, sub aripa
RAMPA = (15.1, 0.0, 18.6, 6.0)       # intrarea masinii, pe sub bara
SCARA = (16.5, 10.1, 20.0, 11.2)     # scara spre capatul holului de sus
USA_TEHNICA = (15.0, 12.0, 16.0, 12.0)
CASA = (0.0, 12.0, 19.0, 18.9)       # cladirea existenta, necotata

# --------------------------------------------------------------------------
# pagina; se suprascriu variabilele de modul din plan_compartimente, ca sa
# putem refolosi primitivele lui de desen (px, rect, line, text, cota)
# --------------------------------------------------------------------------

P.SCARA = 44.0
P.MARGINE = 115.0
P.LEGENDA_H = 470.0
P.X_MIN, P.X_MAX = -1.6, 26.6
P.Y_MIN, P.Y_MAX = -6.2, 20.2
P.W = max((P.X_MAX - P.X_MIN) * P.SCARA + 2 * P.MARGINE, 1990.0)
P.H = (P.Y_MAX - P.Y_MIN) * P.SCARA + 2 * P.MARGINE + P.LEGENDA_H

px, rect, line, circle = P.px, P.rect, P.line, P.circle
text, text_px, cota = P.text, P.text_px, P.cota

C_SUS = "#a8adb5"
C_ZID = "#141414"
C_RAMPA = "#e8779f"
Cs = "#3fa9d4"
C_CASA = "#a9714f"
C_USA = "#c1121f"
C_NOTA = "#d1600f"


def hasura(x0, y0, x1, y1, pas=1.1, col="#c08a68", w="2.0"):
    """Hasura la 45 de grade, decupata la dreptunghi."""
    out = []
    t = x0 - (y1 - y0)
    while t < x1:
        ax, ay = t, y0
        bx, by = t + (y1 - y0), y1
        if bx > x1:
            by = y0 + (x1 - t)
            bx = x1
        if ax < x0:
            ay = y0 + (x0 - t)
            ax = x0
        if bx > ax:
            out.append(line(ax, ay, bx, by, stroke=col, stroke_width=w,
                            opacity="0.75"))
        t += pas
    return out


def strat_parter():
    """Conturul si compartimentarea partii de sus, in linie subtire."""
    o = ['<g fill="none">']
    # terasa jacuzzi
    o.append(rect(P.TERASA_X0, P.TERASA_Y0, P.TERASA_X1, 0.0, fill="none",
                  stroke=C_SUS, stroke_width="1.6", stroke_dasharray="7 6"))
    o.append(circle((P.TERASA_X0 + P.TERASA_X1) / 2.0, P.TERASA_Y_NEC / 2.0,
                    P.JACUZZI_D / 2.0, fill="none", stroke=C_SUS,
                    stroke_width="1.6", stroke_dasharray="7 6"))
    o.append(rect(11.5, 1.5, 17.5, 4.5, fill="#eaf4fa", stroke="#8fb6cc",
                  stroke_width="2.6", stroke_dasharray="8 6"))
    o.append(text(13.0, 3.1, "bazin", size=19, weight="600", fill="#6f959f"))
    for tip, x0, y0, x1, y1 in P.PERETI:
        gros = "4.4" if tip == P.PLIN else "3.0"
        o.append(line(x0, y0, x1, y1, stroke=C_SUS, stroke_width=gros,
                      opacity="0.85"))
    o.append("</g>")
    # numerele compartimentelor de sus, in cerculet
    poz = {"1": (5.0, 3.0), "2": (10.8, 5.3), "3": (23.6, 8.2),
           "4": (19.5, 4.5), "5": (23.6, 1.6), "6": (21.2, 11.2),
           "8": (21.0, 5.0), "7": (22.0, -4.0)}
    for nr, (cx, cy) in poz.items():
        o.append(circle(cx, cy, 0.46, fill="#ffffff", stroke=C_SUS,
                        stroke_width="1.8"))
        o.append(text(cx, cy, nr, size=20, weight="700", fill="#6f757d", dy=7))
    return o


def strat_demisol():
    o = []
    # pardoseli
    o.append(rect(*CAMD, fill="#fbf7ef", stroke="none"))
    o.append(rect(*CAMJ, fill="#fbf7ef", stroke="none"))
    o.append(rect(*RAMPA, fill="#fdeef3", stroke="none"))
    # cladirea existenta
    o.append(rect(*CASA, fill="#f6ece5", stroke="none"))
    o.extend(hasura(*CASA))
    o.append(rect(*CASA, fill="none", stroke=C_CASA, stroke_width="6"))

    # zidurile demisolului
    z = dict(stroke=C_ZID, stroke_width="8", stroke_linecap="butt")
    o.append(line(CAMD[0], CAMD[1], RAMPA[0], CAMD[1], **z))
    o.append(line(RAMPA[2], CAMD[1], CAMD[2], CAMD[1], **z))
    o.append(line(CAMD[0], CAMD[1], CAMD[0], CAMD[3], **z))
    o.append(line(CAMD[0], CAMD[3], CAMD[2], CAMD[3], **z))
    o.append(line(CAMD[2], CAMD[1], CAMD[2], SCARA[1], **z))
    o.append(line(CAMD[2], SCARA[3], CAMD[2], CAMD[3], **z))
    o.append(line(CAMJ[0], CAMJ[1], CAMJ[2], CAMJ[1], **z))
    o.append(line(CAMJ[2], CAMJ[1], CAMJ[2], CAMJ[3], **z))
    o.append(line(CAMJ[0], CAMJ[3], CAMJ[2], CAMJ[3], **z))
    o.append(line(CAMJ[0], CAMJ[1], CAMJ[0], CAMD[1], **z))

    # rampa auto
    o.append(rect(*RAMPA, fill="none", stroke=C_RAMPA, stroke_width="6"))
    xm = (RAMPA[0] + RAMPA[2]) / 2.0
    o.append(line(xm, RAMPA[1] + 0.5, xm, RAMPA[3] - 0.5, stroke=C_RAMPA,
                  stroke_width="2.4", stroke_dasharray="12 8"))
    a, b = px(xm, RAMPA[3] - 0.5)
    o.append('<path d="M %.1f %.1f l -9 -16 l 9 6 l 9 -6 z" fill="%s"/>'
             % (a, b, C_RAMPA))
    for k in range(6):
        y = RAMPA[1] + 0.55 + k * 0.95
        o.append(line(RAMPA[0] + 0.35, y, RAMPA[2] - 0.35, y, stroke=C_RAMPA,
                      stroke_width="1.6", opacity="0.6"))

    # scara
    o.append(rect(*SCARA, fill="#e8f6fc", stroke=Cs, stroke_width="5"))
    n = 15
    for k in range(1, n):
        x = SCARA[0] + k * (SCARA[2] - SCARA[0]) / n
        o.append(line(x, SCARA[1], x, SCARA[3], stroke=Cs, stroke_width="1.8"))
    a, b = px(SCARA[2] - 0.35, (SCARA[1] + SCARA[3]) / 2.0)
    o.append('<path d="M %.1f %.1f l -15 -9 l 6 9 l -6 9 z" fill="%s"/>'
             % (a, b, Cs))

    # usa camerei tehnice
    o.append(line(*USA_TEHNICA, stroke="#ffffff", stroke_width="12"))
    o.append(line(*USA_TEHNICA, stroke=C_USA, stroke_width="8"))

    # traseul de iarna: usa tehnica -> CAM. D -> scara
    t = dict(stroke="#1f7a4d", stroke_width="3.0", stroke_dasharray="11 8",
             fill="none")
    o.append(line(15.5, 12.0, 15.5, 10.65, **t))
    o.append(line(15.5, 10.65, SCARA[0], 10.65, **t))
    o.append(text(13.6, 10.35, "traseu de iarna", size=18, weight="600",
                  fill="#1f7a4d"))
    return o


def note_clash():
    """Cerculetele portocalii care marcheaza cele doua ciocniri."""
    o = []
    for nr, (cx, cy) in {"A": (16.8, 3.0), "B": (18.2, 10.65)}.items():
        o.append(circle(cx, cy, 0.5, fill=C_NOTA, stroke="#ffffff",
                        stroke_width="2"))
        o.append(text(cx, cy, nr, size=22, weight="700", fill="#ffffff", dy=8))
    return o


TABEL = [
    ("CAM. D  depozitare + garaj", "19,0 x 6,0", "114,0"),
    ("CAM. J  joaca: TV, biliard, ping-pong", "6,0 x 12,0", "72,0"),
    ("rampa auto, pe sub bara", "3,5 x 6,0", "21,0"),
    ("scara spre holul de sus", "3,5 x 1,1", "3,9"),
    ("cladirea existenta (necotata)", "19,0 x 6,9", "131,1"),
]

NOTE = [
    ("Demisolul nu are nicio cota scrisa. Tot ce e mai jos s-a masurat", "#33383f"),
    ("fata de conturul partii de sus, care are cote cunoscute.", "#33383f"),
    ("A  Rampa trece pe sub bazin. Bazinul coboara 1,45 m sub parter,", C_NOTA),
    ("   deci sub el raman 1,4 m liberi. O masina cere 2,2 m.", C_NOTA),
    ("B  Scara are 3,5 m de rampa pentru 3,1 m diferenta de nivel:", C_NOTA),
    ("   trepte de 22 cm. Pentru 25 cm ii trebuie 4,3 m.", C_NOTA),
    ("Traseul de iarna: casa -> camera tehnica -> CAM. D -> scara ->", "#33383f"),
    ("   capatul de sud al holului de sus. Tot pe interior.", "#33383f"),
    ("Deasupra lui CAM. J stau baile, sauna si sala: hidroizolatie", "#33383f"),
    ("   si scurgeri de prevazut in placa.", "#33383f"),
]


def legenda(y0):
    out = []
    x = P.MARGINE
    out.append(text_px(x, y0, "Legenda", size=26, weight="700"))
    randuri = [
        (C_ZID, "zid demisol"),
        (C_SUS, "conturul partii de sus"),
        (C_RAMPA, "rampa auto"),
        (Cs, "scara"),
        (C_USA, "usa camerei tehnice"),
        (C_CASA, "cladirea existenta"),
        ("#1f7a4d", "traseul de iarna"),
    ]
    for k, (col, et) in enumerate(randuri):
        yy = y0 + 40 + k * 35
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="10"/>' % (x, yy - 7, x + 58, yy - 7, col))
        out.append(text_px(x + 74, yy, et, size=21, fill="#33383f"))

    x2 = P.MARGINE + 380
    out.append(text_px(x2, y0, "Suprafete demisol", size=26, weight="700"))
    for k, (a, b, c) in enumerate(TABEL):
        yy = y0 + 40 + k * 31
        out.append(text_px(x2, yy, a, size=21, fill="#33383f"))
        out.append(text_px(x2 + 450, yy, b, size=21, fill="#6b7076",
                           anchor="end"))
        out.append(text_px(x2 + 590, yy, c + " m2", size=21, fill="#33383f",
                           anchor="end"))
    yy = y0 + 40 + len(TABEL) * 31 + 12
    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#c9ced4" '
               'stroke-width="1.6"/>' % (x2, yy - 21, x2 + 590, yy - 21))
    out.append(text_px(x2, yy, "demisol, fara rampa", size=21, weight="700"))
    out.append(text_px(x2 + 590, yy, "186,0 m2", size=21, weight="700",
                       anchor="end"))
    out.append(text_px(x2, yy + 30, "parter, sub acoperis", size=21,
                       weight="700"))
    out.append(text_px(x2 + 590, yy + 30, "186,0 m2", size=21, weight="700",
                       anchor="end"))

    x3 = P.MARGINE + 1130
    out.append(text_px(x3, y0, "Note", size=26, weight="700"))
    for k, (n, col) in enumerate(NOTE):
        out.append(text_px(x3, y0 + 40 + k * 30, n, size=20, fill=col))
    return out


COTE = [
    (CAMD[0], CAMD[3], CAMD[2], CAMD[3], "19 m", False, 1.3),
    (CAMD[0], CAMD[1], CAMD[0], CAMD[3], "6 m", False, -1.3),
    (CAMJ[0], CAMJ[3], CAMJ[2], CAMJ[3], "6 m", False, 1.3),
    (CAMJ[2], CAMJ[1], CAMJ[2], CAMJ[3], "12 m", False, 1.4),
    (RAMPA[0], 0.0, RAMPA[2], 0.0, "3,5 m", False, -1.3),
    (SCARA[0], SCARA[1], SCARA[2], SCARA[1], "3,5 m", False, -1.2),
    (CASA[0], CASA[1], CASA[0], CASA[3], "6,9 m", False, -1.3),
]


def construieste_svg():
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
         'viewBox="0 0 %.0f %.0f">' % (P.W, P.H, P.W, P.H)]
    o.append('<defs><marker id="sg" viewBox="0 0 10 10" refX="5" refY="5" '
             'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path d="M 0 0 L 10 5 L 0 10 z" fill="#7a3fb8"/></marker></defs>')
    o.append('<rect width="%.0f" height="%.0f" fill="#ffffff"/>' % (P.W, P.H))

    o.append('<g stroke="#eceef1" stroke-width="1">')
    x = int(P.X_MIN)
    while x <= P.X_MAX:
        o.append(line(x, P.Y_MIN, x, P.Y_MAX))
        x += 1
    y = int(P.Y_MIN)
    while y <= P.Y_MAX:
        o.append(line(P.X_MIN, y, P.X_MAX, y))
        y += 1
    o.append("</g>")

    o.extend(strat_demisol())
    o.extend(strat_parter())
    o.extend(note_clash())

    o.append(text(9.5, 8.6, "CAM. D", size=44, weight="700", fill="#1d2126",
                  style="opacity:0.20"))
    o.append(text(9.5, 9.35, "depozitare + garaj", size=22, weight="600",
                  fill="#3b4149"))
    o.append(text(22.6, 3.2, "CAM. J", size=40, weight="700", fill="#1d2126",
                  style="opacity:0.22"))
    o.append(text(22.6, 3.9, "joaca", size=21, weight="600", fill="#3b4149"))
    o.append(text(9.5, 15.6, "CLADIREA EXISTENTA", size=26, weight="700",
                  fill="#8a5638"))
    o.append(text(16.85, 1.6, "rampa", size=19, weight="600", fill=C_RAMPA))
    o.append(text(11.4, 12.75, "usa camerei tehnice", size=19, weight="600",
                  fill=C_USA))
    o.append(line(13.9, 12.62, 15.4, 12.1, stroke=C_USA, stroke_width="1.6"))

    for c in COTE:
        o.extend(cota(*c))

    nx, ny = px(-0.8, -5.4)
    o.append('<g transform="translate(%.1f,%.1f)">'
             '<path d="M 0 -30 L 11 18 L 0 9 L -11 18 z" fill="#3b4149"/>'
             '<text x="0" y="41" font-family="Helvetica,Arial,sans-serif" '
             'font-size="22" font-weight="700" fill="#3b4149" '
             'text-anchor="middle">N</text></g>' % (nx, ny))

    o.append(text_px(P.MARGINE, 58,
                     "Casa Dealu Negru — plan combinat, demisol + parter",
                     size=36, weight="700"))
    o.append(text_px(P.MARGINE, 92,
                     "demisolul plin, partea de sus suprapusa in contur "
                     "subtire; scara 1:100 la 44 px/m",
                     size=22, fill="#6b7076"))

    o.extend(legenda(P.H - P.LEGENDA_H + 36))
    o.append("</svg>")
    return "\n".join(o)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    outdir = os.path.join(root, "renders")
    os.makedirs(outdir, exist_ok=True)
    svg_path = os.path.join(outdir, "plan_combinat.svg")
    with open(svg_path, "w") as fh:
        fh.write(construieste_svg())
    print("scris", svg_path)
    png = P.rasterizeaza(svg_path, os.path.join(outdir, "plan_combinat.png"))
    print("scris", png) if png else print("Chromium lipseste; doar SVG.",
                                          file=sys.stderr)


if __name__ == "__main__":
    main()
