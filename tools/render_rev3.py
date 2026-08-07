#!/usr/bin/env python3
"""Randeaza modelul 3D al zonei wellness rev. 3.

Foloseste acelasi renderer software ca restul proiectului (`render_obj`),
fara dependente in afara bibliotecii standard. Scoate sase cadre in
`renders/3d/`, dintre care unul cu acoperisul scos, ca sa se vada
compartimentarea.

    python3 tools/render_rev3.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render_obj as R

# Vegetatie asezata in jurul amprentei noi (bara 0..19, aripa 19..25,
# terasa pana la z = -5), nu in interiorul ei.
ARBORI = [
    (-7.5, -6.0, 0.72), (-9.5, 4.0, 0.64), (-8.0, 13.5, 0.76),
    (-3.0, 21.0, 0.66), (7.0, 24.0, 0.80), (19.0, 25.0, 0.62),
    (25.0, 21.0, 0.72), (33.0, 15.0, 0.76), (35.0, 4.0, 0.64),
    (33.0, -6.0, 0.70), (24.0, -14.0, 0.80), (13.0, -12.0, 0.62),
    (3.0, -11.0, 0.72), (-5.0, -12.5, 0.66), (-13.0, -3.0, 0.60),
    (-12.0, 9.0, 0.68),
]

TUFE = [
    (-2.4, -1.8, 0.26), (-2.6, 7.8, 0.24), (-2.6, 13.0, 0.22),
    (27.6, 2.0, 0.26),
    (27.6, 8.5, 0.24), (27.4, 14.4, 0.22), (17.0, -6.4, 0.24),
    (26.6, -6.0, 0.26), (12.0, 14.6, 0.26), (5.0, 14.6, 0.22),
]

VIEWS = {
    "01_aerian_sud_vest": dict(
        eye=(-21.0, 12.0, 39.0), target=(11.0, 1.6, 3.5), fov=40.0,
        titlu="Aerian trei sferturi dinspre sud-vest"),
    "02_aerian_nord_est": dict(
        eye=(47.0, 11.0, -25.0), target=(14.0, 1.6, 4.0), fov=40.0,
        titlu="Aerian trei sferturi dinspre nord-est"),
    "03_de_sus": dict(
        eye=(12.4, 110.0, 4.0), target=(12.4, 0.0, 3.9), fov=17.0, fit=True,
        titlu="Vedere de sus, cu acoperisul"),
    "04_dollhouse": dict(
        eye=(12.4, 110.0, 4.0), target=(12.4, 0.0, 3.9), fov=17.0, fit=True,
        fara_acoperis=True,
        titlu="Sectiune dollhouse, fara acoperis"),
    "05_din_gradina": dict(
        eye=(0.5, 1.75, 30.0), target=(14.0, 2.9, 6.0), fov=46.0,
        titlu="Din gradina, dinspre sud"),
    "06_terasa_jacuzzi": dict(
        eye=(15.5, 2.20, -12.5), target=(22.5, 1.2, -2.4), fov=48.0,
        titlu="Terasa cu jacuzzi, dinspre nord-vest"),
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    verts, objs = R.load_obj(os.path.join(root, "model",
                                          "zona_wellness_rev3.obj"))
    mats = R.load_mtl(os.path.join(root, "model", "zona_wellness_rev3.mtl"))

    R.ARBORI, R.TUFE = ARBORI, TUFE
    fit_verts = list(verts)
    R.add_vegetatie(verts, objs, mats)

    outdir = os.path.join(root, "renders", "3d")
    os.makedirs(outdir, exist_ok=True)
    doar = set(sys.argv[1:])
    for key, view in VIEWS.items():
        if doar and key not in doar:
            continue
        sel = objs
        fit = fit_verts
        if view.get("fara_acoperis"):
            sel = [o for o in objs if not o["name"].startswith("Acoperis")]
            fit = [verts[i] for o in sel for i in o["idx"]
                   if not o["name"].startswith(("Arbore", "Tufa"))]
        path = os.path.join(outdir, key + ".png")
        R.render(view, verts, sel, mats, path, fit_verts=fit)
        print("scris", path)


if __name__ == "__main__":
    main()
