#!/usr/bin/env python3
"""Construieste modelul 3D al zonei wellness rev. 3 din cotele planului.

Citeste geometria direct din `plan_compartimente`, ca planul si modelul sa nu
poata pleca unul de la celalalt. Scrie `model/zona_wellness_rev3.obj` + `.mtl`,
1 unitate = 1 metru, gata de deschis in Blender / SketchUp / Twinmation.

Convertie plan -> 3D: x din plan ramane x, y din plan (spre sud) devine z,
inaltimea este y.

    python3 tools/model_rev3.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import plan_compartimente as P

# --------------------------------------------------------------------------
# inaltimi
# --------------------------------------------------------------------------

H_PERETE = 3.20            # streasina / intradosul acoperisului
H_PARTITIE = 2.60          # compartimentari interioare
GROS_EXT = 0.30            # grosime perete exterior
GROS_INT = 0.12            # grosime compartimentare
H_ACOP = 0.34              # grosimea placii de acoperis
STREASINA = 0.85           # iesirea acoperisului in consola
H_PARDOSEALA = 0.14        # cota pardoselii peste teren
AD_BAZIN = 1.45            # adancimea piscinei
H_JACUZZI = 0.85           # inaltimea cazii peste terasa

MATERIALE = {
    "mat_calcar":      ((0.79, 0.75, 0.67), 1.0),
    "mat_antracit":    ((0.15, 0.15, 0.16), 1.0),
    "mat_sticla":      ((0.52, 0.66, 0.74), 0.34),
    "mat_acoperis":    ((0.26, 0.27, 0.29), 1.0),
    "mat_pardoseala":  ((0.68, 0.66, 0.63), 1.0),
    "mat_partitie":    ((0.87, 0.86, 0.83), 1.0),
    "mat_apa":         ((0.18, 0.52, 0.64), 1.0),
    "mat_lemn":        ((0.52, 0.39, 0.27), 1.0),
    "mat_mobilier":    ((0.74, 0.72, 0.69), 1.0),
    "mat_gratar":      ((0.22, 0.22, 0.24), 1.0),
}


class Model:
    def __init__(self):
        self.v = []
        self.f = []

    def _idx(self, p):
        self.v.append(p)
        return len(self.v)

    def quad(self, name, mat, pts):
        idx = [self._idx(p) for p in pts]
        self.f.append((name, mat, idx))

    def box(self, name, mat, x0, z0, x1, z1, y0, y1, capac=True, fund=False):
        """Paralelipiped aliniat la axe, dat prin amprenta si doua cote."""
        x0, x1 = min(x0, x1), max(x0, x1)
        z0, z1 = min(z0, z1), max(z0, z1)
        a = [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)]
        b = [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]
        self.quad(name, mat, [a[0], a[1], b[1], b[0]])
        self.quad(name, mat, [a[1], a[2], b[2], b[1]])
        self.quad(name, mat, [a[2], a[3], b[3], b[2]])
        self.quad(name, mat, [a[3], a[0], b[0], b[3]])
        if capac:
            self.quad(name, mat, b)
        if fund:
            self.quad(name, mat, a)

    def perete(self, name, mat, x0, z0, x1, z1, y0, y1, gros):
        """Perete dat prin axa lui; se ingroasa simetric fata de axa."""
        if abs(z1 - z0) < 1e-9:
            self.box(name, mat, x0, z0 - gros / 2, x1, z0 + gros / 2, y0, y1)
        else:
            self.box(name, mat, x0 - gros / 2, z0, x0 + gros / 2, z1, y0, y1)

    def inel(self, name, mat, cx, cz, r0, r1, y, n=28):
        """Coroana circulara, desenata din n patrulatere."""
        for i in range(n):
            a0 = 2 * math.pi * i / n
            a1 = 2 * math.pi * (i + 1) / n
            pts = [(cx + r0 * math.cos(a0), y, cz + r0 * math.sin(a0)),
                   (cx + r1 * math.cos(a0), y, cz + r1 * math.sin(a0)),
                   (cx + r1 * math.cos(a1), y, cz + r1 * math.sin(a1)),
                   (cx + r0 * math.cos(a1), y, cz + r0 * math.sin(a1))]
            self.quad(name, mat, pts)

    def cilindru(self, name, mat, cx, cz, r, y0, y1, n=28, capac=True):
        baza = [self._idx((cx + r * math.cos(2 * math.pi * i / n), y0,
                           cz + r * math.sin(2 * math.pi * i / n)))
                for i in range(n)]
        sus = [self._idx((cx + r * math.cos(2 * math.pi * i / n), y1,
                          cz + r * math.sin(2 * math.pi * i / n)))
               for i in range(n)]
        for i in range(n):
            j = (i + 1) % n
            self.f.append((name, mat, [baza[i], baza[j], sus[j], sus[i]]))
        if capac:
            self.f.append((name, mat, sus))

    def disc(self, name, mat, cx, cz, r, y, n=28):
        idx = [self._idx((cx + r * math.cos(2 * math.pi * i / n), y,
                          cz + r * math.sin(2 * math.pi * i / n)))
               for i in range(n)]
        self.f.append((name, mat, idx))

    def scrie(self, obj_path, mtl_path):
        with open(mtl_path, "w") as fh:
            fh.write("# Zona wellness rev. 3\n")
            for nume, (kd, d) in MATERIALE.items():
                fh.write("\nnewmtl %s\n" % nume)
                fh.write("Kd %.4f %.4f %.4f\n" % kd)
                fh.write("Ka 0.0 0.0 0.0\nKs 0.05 0.05 0.05\nNs 24\n")
                fh.write("d %.3f\n" % d)
        with open(obj_path, "w") as fh:
            fh.write("# Casa Dealu Negru - zona wellness, revizia 3\n")
            fh.write("# Generat de tools/model_rev3.py; 1 unitate = 1 metru\n")
            fh.write("mtllib %s\n\n" % os.path.basename(mtl_path))
            for p in self.v:
                fh.write("v %.4f %.4f %.4f\n" % p)
            nume, mat = None, None
            for n, m, idx in self.f:
                if n != nume:
                    fh.write("\no %s\n" % n)
                    nume, mat = n, None
                if m != mat:
                    fh.write("usemtl %s\n" % m)
                    mat = m
                fh.write("f %s\n" % " ".join(str(i) for i in idx))


# --------------------------------------------------------------------------
# construirea modelului
# --------------------------------------------------------------------------

def construieste():
    m = Model()
    h0, h1 = H_PARDOSEALA, H_PARDOSEALA + H_PERETE
    BL, BA = P.BARA_L, P.BARA_A
    AX0, AX1, AY1 = P.ARIPA_X0, P.ARIPA_X1, P.ARIPA_Y1
    HX1, YJ = P.HOL_X1, P.Y_JOS

    # --- placile de pardoseala -------------------------------------------
    px0, pz0, px1, pz1 = 11.5, 1.5, 17.5, 4.5      # oglinda bazinului
    m.box("Pardoseala_bara", "mat_pardoseala", -0.15, -0.15, px0, BA + 0.15,
          0.0, h0)
    m.box("Pardoseala_bara", "mat_pardoseala", px1, -0.15, AX0, BA + 0.15,
          0.0, h0)
    m.box("Pardoseala_bara", "mat_pardoseala", px0, -0.15, px1, pz0, 0.0, h0)
    m.box("Pardoseala_bara", "mat_pardoseala", px0, pz1, px1, BA + 0.15,
          0.0, h0)
    m.box("Pardoseala_aripa", "mat_pardoseala", AX0, -0.15, AX1 + 0.15,
          AY1 + 0.15, 0.0, h0)

    # --- peretii exteriori plini -----------------------------------------
    m.perete("Perete_BBQ", "mat_antracit", 0.0, 0.0, 0.0, BA, h0, h1, GROS_EXT)
    m.perete("Perete_aripa_vest", "mat_calcar", AX0, 0.0, AX0, AY1, h0, h1,
             GROS_EXT)
    m.perete("Perete_aripa_sud", "mat_calcar", AX0, AY1, AX1, AY1, h0, h1,
             GROS_EXT)
    m.perete("Perete_hol_nord", "mat_calcar", AX0, 0.0, HX1, 0.0, h0, h1,
             GROS_EXT)

    # --- vitraje ----------------------------------------------------------
    # bara: fatadele lungi, retractabile
    m.perete("Vitraj_bara_nord", "mat_sticla", 0.0, 0.0, BL, 0.0, h0, h1, 0.10)
    m.perete("Vitraj_bara_sud", "mat_sticla", 0.0, BA, BL, BA, h0, h1, 0.10)
    # aripa: fatadele fixe
    m.perete("Vitraj_relaxare_nord", "mat_sticla", HX1, 0.0, AX1, 0.0,
             h0, h1, 0.10)
    m.perete("Vitraj_est", "mat_sticla", AX1, 0.0, AX1, AY1, h0, h1, 0.10)

    # --- compartimentari interioare ---------------------------------------
    hp = h0 + H_PARTITIE
    m.perete("Partitie_hol", "mat_partitie", HX1, 0.0, HX1, AY1, h0, hp,
             GROS_INT)
    m.perete("Partitie_relaxare_sala", "mat_partitie", HX1, YJ, AX1, YJ,
             h0, hp, GROS_INT)
    m.perete("Partitie_baie_nord", "mat_partitie", HX1, P.BAIE_Y0, P.BAIE_X1,
             P.BAIE_Y0, h0, hp, GROS_INT)
    m.perete("Partitie_baie_sud", "mat_partitie", HX1, P.BAIE_Y1, P.BAIE_X1,
             P.BAIE_Y1, h0, hp, GROS_INT)
    m.perete("Partitie_baie_est", "mat_partitie", P.BAIE_X1, P.BAIE_Y0,
             P.BAIE_X1, P.BAIE_Y1, h0, hp, GROS_INT)
    # cabina de sauna, in lemn
    hs = h0 + 2.20
    m.perete("Sauna_nord", "mat_lemn", HX1, P.CAB_Y0, P.CAB_X1, P.CAB_Y0,
             h0, hs, GROS_INT)
    m.perete("Sauna_est", "mat_lemn", P.CAB_X1, P.CAB_Y0, P.CAB_X1, AY1,
             h0, hs, GROS_INT)

    # --- acoperisul, placa unica peste ambele volume ----------------------
    ya, yb = h1, h1 + H_ACOP
    s = STREASINA
    m.box("Acoperis_bara", "mat_acoperis", -s, -s, AX0, BA + s, ya, yb)
    m.box("Acoperis_aripa", "mat_acoperis", AX0, -s, AX1 + s, AY1 + s, ya, yb)

    # --- piscina ----------------------------------------------------------
    yf = h0 - AD_BAZIN
    for a, b in (((px0, pz0), (px1, pz0)), ((px1, pz0), (px1, pz1)),
                 ((px1, pz1), (px0, pz1)), ((px0, pz1), (px0, pz0))):
        m.quad("Bazin", "mat_pardoseala",
               [(a[0], yf, a[1]), (b[0], yf, b[1]),
                (b[0], h0, b[1]), (a[0], h0, a[1])])
    m.quad("Bazin", "mat_pardoseala",
           [(px0, yf, pz0), (px1, yf, pz0), (px1, yf, pz1), (px0, yf, pz1)])
    ya_apa = 0.05          # peste planul terenului, ca sa se vada oglinda
    m.quad("Apa_piscina", "mat_apa",
           [(px0, ya_apa, pz0), (px1, ya_apa, pz0),
            (px1, ya_apa, pz1), (px0, ya_apa, pz1)])

    # --- terasa cu jacuzzi ------------------------------------------------
    tx0, tx1 = P.TERASA_X0, P.TERASA_X1
    m.box("Terasa_jacuzzi", "mat_lemn", tx0, P.TERASA_Y_NEC, tx1, 0.0,
          0.0, h0)
    cx, cz = (tx0 + tx1) / 2.0, P.TERASA_Y_NEC / 2.0
    r = P.JACUZZI_D / 2.0
    m.cilindru("Jacuzzi", "mat_lemn", cx, cz, r, h0, h0 + H_JACUZZI,
               capac=False)
    m.inel("Jacuzzi", "mat_lemn", cx, cz, r - 0.30, r, h0 + H_JACUZZI)
    m.cilindru("Jacuzzi", "mat_lemn", cx, cz, r - 0.30, h0 + 0.20,
               h0 + H_JACUZZI, capac=False)
    m.disc("Apa_jacuzzi", "mat_apa", cx, cz, r - 0.30, h0 + H_JACUZZI - 0.16)

    # --- mobilier, cat sa se citeasca programul din vederea de sus --------
    mob = "mat_mobilier"
    # 1: blat pe peretele plin, gratar, masa cu scaune
    m.box("Bucatarie_blat", mob, 0.15, 0.5, 0.85, 5.5, h0, h0 + 0.92)
    m.box("Gratar", "mat_gratar", 0.15, 2.4, 0.85, 3.6, h0 + 0.92, h0 + 1.10)
    m.box("Hota", "mat_gratar", 0.15, 2.3, 1.05, 3.7, h0 + 1.95, h0 + 2.35)
    m.box("Masa", mob, 4.3, 2.1, 7.3, 3.9, h0 + 0.62, h0 + 0.76)
    for k in range(5):
        z = 2.25 + k * 0.36
        m.box("Scaune", mob, 3.85, z, 4.25, z + 0.30, h0, h0 + 0.46)
        m.box("Scaune", mob, 7.35, z, 7.75, z + 0.30, h0, h0 + 0.46)
    # 5: paturi de relaxare
    for k in range(2):
        m.box("Pat_relaxare", mob, 20.4 + k * 2.3, 0.35, 21.7 + k * 2.3,
              2.15, h0, h0 + 0.42)
        m.box("Pat_relaxare", mob, 22.6, 2.7 + k * 2.0, 24.7, 4.0 + k * 2.0,
              h0, h0 + 0.42)
    # 8: cabinele si chiuvetele
    y = P.BAIE_Y0
    for _, lat in P.CABINE:
        m.box("Cabine_baie", "mat_partitie", P.BAIE_X0 + 1.0, y, P.BAIE_X1,
              y + lat, h0, h0 + 2.05)
        y += lat
    for k in range(2):
        m.box("Chiuvete", mob, P.BAIE_X0 + 0.04, 3.6 + k * 2.2,
              P.BAIE_X0 + 0.45, 4.2 + k * 2.2, h0 + 0.60, h0 + 0.86)
    # 6: bancile saunei
    m.box("Banca_sauna", "mat_lemn", HX1 + 0.25, P.CAB_Y0 + 0.25, P.CAB_X1 - 0.25,
          P.CAB_Y0 + 0.80, h0 + 0.42, h0 + 0.52)
    m.box("Banca_sauna", "mat_lemn", P.CAB_X1 - 0.85, P.CAB_Y0 + 0.80,
          P.CAB_X1 - 0.25, AY1 - 0.30, h0 + 0.80, h0 + 0.90)
    # 3: aparatele din sala
    m.box("Banda_alergat", mob, 20.3, 7.3, 21.2, 9.4, h0, h0 + 1.30)
    m.box("Rastel", mob, 21.7, 7.3, 24.7, 7.9, h0, h0 + 1.90)
    m.box("Bench", mob, 23.0, 8.5, 24.5, 9.1, h0, h0 + 0.48)
    m.box("Aparat_1", mob, 22.9, 9.9, 24.7, 10.9, h0, h0 + 1.55)
    m.box("Aparat_2", mob, 22.9, 11.0, 24.7, 11.8, h0, h0 + 1.20)
    return m


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    outdir = os.path.join(root, "model")
    os.makedirs(outdir, exist_ok=True)
    obj = os.path.join(outdir, "zona_wellness_rev3.obj")
    mtl = os.path.join(outdir, "zona_wellness_rev3.mtl")
    m = construieste()
    m.scrie(obj, mtl)
    print("scris %s (%d varfuri, %d fete)" % (obj, len(m.v), len(m.f)))
    print("scris", mtl)


if __name__ == "__main__":
    main()
