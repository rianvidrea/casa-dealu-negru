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

CAMD = (12.0, 6.0, 19.0, 12.0)       # 3 m la stanga usii rosii (x = 15)
CAMJ = (19.0, 0.0, 25.0, 12.0)       # camera de joaca, sub aripa
CAMJ_EXT = (15.1, 0.0, 19.0, 6.0)    # bratul lui CAM. J, pana la usa de garaj
USA_GARAJ = (15.1, 0.0, 18.6, 0.0)   # usa de garaj, pe fatada de nord
SCARA = (15.5, 10.8, 19.5, 11.9)     # scara: 4 m masurati de la usa tehnica
DIF_NIVEL = 2.15                     # diferenta de nivel masurata, "2 m si un pic"
GROS_PLACA = 0.30                    # placa parterului peste demisol
USA_TEHNICA = (15.0, 12.0, 16.0, 12.0)
CASA = (6.0, 12.0, 19.0, 18.9)       # cladirea existenta: latura de 13 m

# --------------------------------------------------------------------------
# pagina; se suprascriu variabilele de modul din plan_compartimente, ca sa
# putem refolosi primitivele lui de desen (px, rect, line, text, cota)
# --------------------------------------------------------------------------

P.SCARA = 44.0
P.MARGINE = 115.0
P.LEGENDA_H = 620.0
P.X_MIN, P.X_MAX = -1.6, 26.6
P.Y_MIN, P.Y_MAX = -6.2, 21.0
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
    o.append(rect(*CAMJ_EXT, fill="#fbf7ef", stroke="none"))
    # cladirea existenta
    o.append(rect(*CASA, fill="#f6ece5", stroke="none"))
    o.extend(hasura(*CASA))
    o.append(rect(*CASA, fill="none", stroke=C_CASA, stroke_width="6"))

    # zidurile demisolului
    z = dict(stroke=C_ZID, stroke_width="8", stroke_linecap="butt")
    # CAM. D
    o.append(line(CAMD[0], CAMD[1], CAMD[2], CAMD[1], **z))
    o.append(line(CAMD[0], CAMD[1], CAMD[0], CAMD[3], **z))
    o.append(line(CAMD[0], CAMD[3], CAMD[2], CAMD[3], **z))
    o.append(line(CAMD[2], CAMD[1], CAMD[2], SCARA[1], **z))
    o.append(line(CAMD[2], SCARA[3], CAMD[2], CAMD[3], **z))
    # CAM. J, conturul in L
    o.append(line(CAMJ_EXT[0], 0.0, CAMJ[2], 0.0, **z))
    o.append(line(CAMJ_EXT[0], 0.0, CAMJ_EXT[0], CAMJ_EXT[3], **z))
    o.append(line(CAMJ_EXT[0], CAMJ_EXT[3], CAMJ[0], CAMJ_EXT[3], **z))
    o.append(line(CAMJ[2], 0.0, CAMJ[2], CAMJ[3], **z))
    o.append(line(CAMJ[0], CAMJ[3], CAMJ[2], CAMJ[3], **z))

    # usa de garaj, pe fatada de nord a bratului lui CAM. J
    o.append(line(*USA_GARAJ, stroke="#ffffff", stroke_width="13"))
    o.append(line(*USA_GARAJ, stroke=C_RAMPA, stroke_width="9"))
    for k in range(7):
        x = USA_GARAJ[0] + 0.22 + k * 0.51
        o.append(line(x, -0.16, x, 0.16, stroke="#ffffff", stroke_width="2.2"))
    o.append(text((USA_GARAJ[0] + USA_GARAJ[2]) / 2.0, -0.42,
                  "usa de garaj", size=19, weight="600", fill=C_RAMPA))

    # scara
    o.append(rect(*SCARA, fill="#e8f6fc", stroke=Cs, stroke_width="5"))
    n = 12
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
    o.append(line(15.5, 12.0, 15.5, 11.35, **t))
    o.append(text(14.0, 11.55, "traseu de iarna", size=17, weight="600",
                  fill="#1f7a4d"))
    return o


def note_clash():
    """Cerculetele portocalii care marcheaza cele doua ciocniri."""
    o = []
    for nr, (cx, cy) in {"A": (20.8, 14.1), "B": (16.4, 2.2)}.items():
        o.append(circle(cx, cy, 0.5, fill=C_NOTA, stroke="#ffffff",
                        stroke_width="2"))
        o.append(text(cx, cy, nr, size=22, weight="700", fill="#ffffff", dy=8))
    return o


# --------------------------------------------------------------------------
# sectiunea mica prin demisol, desenata in coltul liber din dreapta jos
# --------------------------------------------------------------------------

SX0, SX1 = 20.6, 25.9              # latimea desenului, in unitati de plan
SY0 = 15.0                         # cota pardoselii parterului, pe hartie
KV = 1.12                          # unitati de plan pentru un metru real


def _sy(h):
    """Inaltime reala sub parter -> ordonata pe hartie."""
    return SY0 + h * KV


def _cota_v(x, h0, h1, eticheta, col="#7a3fb8", dash=""):
    y0, y1 = _sy(h0), _sy(h1)
    d = ' stroke-dasharray="8 5"' if dash else ""
    o = ['<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
         'stroke-width="2.0" marker-start="url(#sg)" marker-end="url(#sg)"%s/>'
         % (px(x, y0)[0], px(x, y0)[1], px(x, y1)[0], px(x, y1)[1], col, d)]
    o.append(text(x, (y0 + y1) / 2.0, eticheta, size=19, fill=col, weight="600",
                  dy=6, style="writing-mode:tb;glyph-orientation-vertical:0"))
    return o


def sectiune_gabarit():
    o = [text(21.3, 14.18, "Sectiune prin demisol", size=22, weight="700",
              fill="#1d2126", anchor="start")]
    # placa parterului
    o.append(rect(SX0, _sy(0.0), SX1, _sy(GROS_PLACA), fill="#dfe2e6",
                  stroke="#8a8f98", stroke_width="2.0"))
    o.extend(hasura(SX0, _sy(0.0), SX1, _sy(GROS_PLACA), pas=0.42,
                    col="#9aa0a8", w="1.2"))
    o.append(text(SX0 + 0.1, _sy(0.0) - 0.16, "parter ±0,00", size=17,
                  fill="#6b7076", anchor="start"))
    # pardoseala demisolului, masurata
    o.append(rect(SX0, _sy(DIF_NIVEL), SX1, _sy(DIF_NIVEL + 0.25),
                  fill="#dfe2e6", stroke="#8a8f98", stroke_width="2.0"))
    # pardoseala propusa, coborata
    o.append(rect(SX0, _sy(2.75), SX1, _sy(3.0), fill="#f7efe3",
                  stroke=C_NOTA, stroke_width="2.0", stroke_dasharray="9 6"))
    o.append(text(SX1 - 0.1, _sy(3.0) + 0.42, "propus, sapat cu inca 60 cm",
                  size=17, fill=C_NOTA, anchor="end"))
    # peretii
    for x in (SX0, SX1):
        o.append(line(x, _sy(GROS_PLACA), x, _sy(DIF_NIVEL), stroke="#8a8f98",
                      stroke_width="2.0"))
    o.extend(_cota_v(SX0 - 0.45, 0.0, DIF_NIVEL, "2,15 m"))
    o.extend(_cota_v(SX0 + 1.5, GROS_PLACA, DIF_NIVEL, "1,85 m", col=C_NOTA))
    o.extend(_cota_v(SX1 - 1.3, GROS_PLACA, 2.75, "2,40 m", col=C_NOTA,
                     dash=True))
    return o


TABEL = [
    ("CAM. D  depozitare", "7,0 x 6,0", "42,0"),
    ("CAM. J  joaca, in L", "72,0 + 23,4", "95,4"),
        ("scara, 4 m masurati", "4,0 x 1,1", "4,4"),
    ("cladirea existenta", "13,0 x 6,9", "89,7"),
]

NOTE = [
    ("Masurate de tine: latura de 13 m, cei 4 m ai scarii si diferenta", "#33383f"),
    ("de nivel. Restul cotelor sunt scoase din desen — punctate.", "#33383f"),
    ("CAM. D merge 3 m la stanga usii rosii, deci are 7 m. CAM. J", "#33383f"),
    ("   se intinde in L pana la usa de garaj. Casa ramane la 13 m.", "#33383f"),
    ("A  Gabaritul demisolului. 2,15 m diferenta de nivel minus 30 cm", C_NOTA),
    ("   de placa lasa 1,85 m liberi. O camera de joaca cere 2,40 m.", C_NOTA),
    ("   Solutia: se sapa cu inca 60 cm; scara ajunge la 16 trepte,", C_NOTA),
    ("   adica 3,98 m de rampa — incap in cei 4 m masurati.", C_NOTA),
    ("B  Bratul lui CAM. J trece 2,4 m pe sub bazin, unde raman", C_NOTA),
    ("   40 cm. Bazinul se muta spre vest, la 10,3-16,3, si bratul", C_NOTA),
    ("   ramane liber pe toata latimea.", C_NOTA),
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
        (C_RAMPA, "acces + usa de garaj"),
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
    out.append(text_px(x2, yy, "demisol", size=21, weight="700"))
    out.append(text_px(x2 + 590, yy, "137,4 m2", size=21, weight="700",
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
    (CAMD[0], CAMD[3], CAMD[2], CAMD[3], "7 m", True, 1.3),
    (CAMD[0], CAMD[3], USA_TEHNICA[0], CAMD[3], "3 m", True, -0.95),
    (CAMD[0], CAMD[1], CAMD[0], CAMD[3], "6 m", False, -1.4),
    (CAMJ[0], CAMJ[3], CAMJ[2], CAMJ[3], "6 m", False, 1.3),
    (CAMJ[2], CAMJ[1], CAMJ[2], CAMJ[3], "12 m", False, 1.4),
    (USA_GARAJ[0], 0.0, USA_GARAJ[2], 0.0, "3,5 m", False, -1.9),
    (SCARA[0], SCARA[1], SCARA[2], SCARA[1], "4 m", True, -1.2),
    (CASA[0], CASA[3], CASA[2], CASA[3], "13 m", True, 1.3),
    (CASA[0], CASA[1], CASA[0], CASA[3], "6,9 m", False, -1.4),
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
    o.extend(sectiune_gabarit())
    o.extend(note_clash())

    o.append(text(14.6, 8.1, "CAM. D", size=38, weight="700", fill="#1d2126",
                  style="opacity:0.20"))
    o.append(text(14.6, 8.8, "depozitare", size=21, weight="600",
                  fill="#3b4149"))
    o.append(text(17.05, 4.5, "CAM. J", size=36, weight="700", fill="#1d2126",
                  style="opacity:0.22"))
    o.append(text(17.05, 5.15, "joaca", size=20, weight="600", fill="#3b4149"))
    o.append(text(12.5, 15.6, "CLADIREA EXISTENTA", size=26, weight="700",
                  fill="#8a5638"))
    o.append(text(8.6, 14.5, "usa camerei tehnice", size=19, weight="600",
                  fill=C_USA))
    o.append(line(11.1, 14.35, 15.2, 12.15, stroke=C_USA, stroke_width="1.6"))

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
