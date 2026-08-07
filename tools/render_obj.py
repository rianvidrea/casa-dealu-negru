#!/usr/bin/env python3
"""Randare software a modelului OBJ de masing, fara dependente externe.

Z-buffer, proiectie perspectiva, lumina directionala + ambient ocluziv simplu,
umbre proiectate pe teren, muchii desenate pentru claritate arhitecturala.
Iesire: PNG (zlib din stdlib).
"""

import math
import os
import struct
import zlib

# --------------------------------------------------------------------------
# vector helpers
# --------------------------------------------------------------------------


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(a):
    l = math.sqrt(dot(a, a)) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


# --------------------------------------------------------------------------
# OBJ / MTL
# --------------------------------------------------------------------------


def load_mtl(path):
    mats, cur = {}, None
    with open(path) as fh:
        for line in fh:
            p = line.split()
            if not p:
                continue
            if p[0] == "newmtl":
                cur = p[1]
                mats[cur] = {"kd": (0.8, 0.8, 0.8), "d": 1.0}
            elif cur and p[0] == "Kd":
                mats[cur]["kd"] = (float(p[1]), float(p[2]), float(p[3]))
            elif cur and p[0] == "d":
                mats[cur]["d"] = float(p[1])
    return mats


def load_obj(path):
    verts, objs = [], []
    name, mat = "default", "default"
    with open(path) as fh:
        for line in fh:
            p = line.split()
            if not p:
                continue
            if p[0] == "v":
                verts.append((float(p[1]), float(p[2]), float(p[3])))
            elif p[0] in ("o", "g"):
                name = p[1]
            elif p[0] == "usemtl":
                mat = p[1]
            elif p[0] == "f":
                idx = [int(t.split("/")[0]) - 1 for t in p[1:]]
                objs.append({"name": name, "mat": mat, "idx": idx})
    return verts, objs


# --------------------------------------------------------------------------
# camera
# --------------------------------------------------------------------------


class Camera:
    def __init__(self, eye, target, up, fov_deg, w, h):
        self.eye = eye
        self.f = norm(sub(target, eye))
        self.r = norm(cross(self.f, up))
        self.u = cross(self.r, self.f)
        self.w, self.h = w, h
        self.scale = (w * 0.5) / math.tan(math.radians(fov_deg) * 0.5)
        self.near = 0.06

    def to_cam(self, p):
        d = sub(p, self.eye)
        return (dot(d, self.r), dot(d, self.u), dot(d, self.f))

    def project(self, c):
        iz = 1.0 / c[2]
        return (
            self.w * 0.5 + c[0] * self.scale * iz,
            self.h * 0.5 - c[1] * self.scale * iz,
            iz,
        )


def clip_near(poly, near):
    """Sutherland-Hodgman pe planul z = near (spatiu camera)."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ain, bin_ = a[2] >= near, b[2] >= near
        if ain:
            out.append(a)
        if ain != bin_:
            t = (near - a[2]) / (b[2] - a[2])
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, near))
    return out


# --------------------------------------------------------------------------
# framebuffer
# --------------------------------------------------------------------------


class Frame:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.col = [0.0] * (w * h * 3)
        self.z = [0.0] * (w * h)  # stocam 1/z, 0 = infinit

    def sky(self, top, bot):
        w, h, col = self.w, self.h, self.col
        for y in range(h):
            t = y / (h - 1)
            t = t ** 0.85
            r = top[0] + (bot[0] - top[0]) * t
            g = top[1] + (bot[1] - top[1]) * t
            b = top[2] + (bot[2] - top[2]) * t
            base = y * w * 3
            for x in range(w):
                i = base + x * 3
                col[i] = r
                col[i + 1] = g
                col[i + 2] = b

    def tri(self, p0, p1, p2, rgb, alpha=1.0, zwrite=True, bias=1.0):
        """Rasterizare triunghi cu interpolare liniara a lui 1/z."""
        w, h, col, zb = self.w, self.h, self.col, self.z
        x0, y0, w0 = p0
        x1, y1, w1 = p1
        x2, y2, w2 = p2
        area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(area) < 1e-9:
            return
        inv_area = 1.0 / area
        minx = max(0, int(math.floor(min(x0, x1, x2))))
        maxx = min(w - 1, int(math.ceil(max(x0, x1, x2))))
        miny = max(0, int(math.floor(min(y0, y1, y2))))
        maxy = min(h - 1, int(math.ceil(max(y0, y1, y2))))
        if minx > maxx or miny > maxy:
            return
        cr, cg, cb = rgb
        for py in range(miny, maxy + 1):
            fy = py + 0.5
            row = py * w
            for px in range(minx, maxx + 1):
                fx = px + 0.5
                l1 = ((fx - x0) * (y2 - y0) - (x2 - x0) * (fy - y0)) * inv_area
                if l1 < 0.0 or l1 > 1.0:
                    continue
                l2 = ((x1 - x0) * (fy - y0) - (fx - x0) * (y1 - y0)) * inv_area
                if l2 < 0.0 or l1 + l2 > 1.0:
                    continue
                l0 = 1.0 - l1 - l2
                iz = l0 * w0 + l1 * w1 + l2 * w2
                k = row + px
                if iz * bias <= zb[k]:
                    continue
                i = k * 3
                if alpha >= 0.999:
                    col[i] = cr
                    col[i + 1] = cg
                    col[i + 2] = cb
                else:
                    col[i] += (cr - col[i]) * alpha
                    col[i + 1] += (cg - col[i + 1]) * alpha
                    col[i + 2] += (cb - col[i + 2]) * alpha
                if zwrite:
                    zb[k] = iz

    def poly(self, pts, rgb, alpha=1.0, zwrite=True, bias=1.0):
        for i in range(1, len(pts) - 1):
            self.tri(pts[0], pts[i], pts[i + 1], rgb, alpha, zwrite, bias)

    def line(self, a, b, rgb, width, alpha=1.0):
        """Linie groasa cu test de adancime (bias, fara scriere)."""
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        if n < 1e-6:
            return
        ox, oy = -dy / n * width * 0.5, dx / n * width * 0.5
        q = [
            (a[0] + ox, a[1] + oy, a[2]),
            (b[0] + ox, b[1] + oy, b[2]),
            (b[0] - ox, b[1] - oy, b[2]),
            (a[0] - ox, a[1] - oy, a[2]),
        ]
        self.poly(q, rgb, alpha, zwrite=False, bias=1.004)

    def downsample_png(self, path, ss):
        w, h = self.w // ss, self.h // ss
        inv = 1.0 / (ss * ss)
        rows = bytearray()
        col = self.col
        for y in range(h):
            rows.append(0)
            for x in range(w):
                r = g = b = 0.0
                for sy in range(ss):
                    base = ((y * ss + sy) * self.w + x * ss) * 3
                    for sx in range(ss):
                        i = base + sx * 3
                        r += col[i]
                        g += col[i + 1]
                        b += col[i + 2]
                rows.append(min(255, max(0, int(r * inv * 255 + 0.5))))
                rows.append(min(255, max(0, int(g * inv * 255 + 0.5))))
                rows.append(min(255, max(0, int(b * inv * 255 + 0.5))))
        write_png(path, w, h, bytes(rows))


def write_png(path, w, h, raw):
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    hdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n")
        fh.write(chunk(b"IHDR", hdr))
        fh.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        fh.write(chunk(b"IEND", b""))


# --------------------------------------------------------------------------
# scena
# --------------------------------------------------------------------------

SUN = norm((0.58, -0.74, -0.34))          # directia in care cade lumina
SKY_TOP = (0.36, 0.55, 0.79)
SKY_BOT = (0.87, 0.91, 0.94)
HAZE = (0.78, 0.83, 0.86)
GRASS = (0.50, 0.55, 0.38)
SHADOW = (0.06, 0.09, 0.14)


def ground_quad(cx, cz, half=420.0):
    return [(cx - half, 0.0, cz - half), (cx + half, 0.0, cz - half),
            (cx + half, 0.0, cz + half), (cx - half, 0.0, cz + half)]


def srgb(c):
    return tuple(v ** (1 / 2.2) for v in c)


def shade(kd, n):
    """Lambert + cer hemisferic + bounce cald de la sol."""
    ndl = max(0.0, -dot(n, SUN))
    sky = 0.5 + 0.5 * n[1]
    bounce = max(0.0, -n[1]) * 0.5 + 0.12
    out = []
    for i, k in enumerate(kd):
        lin = k ** 2.2
        v = lin * (0.10 + 0.92 * ndl)
        v += lin * sky * (0.21, 0.25, 0.33)[i]
        v += lin * bounce * (0.13, 0.13, 0.09)[i]
        out.append(min(1.0, v))
    return srgb(tuple(out))


def face_normal(pts):
    n = (0.0, 0.0, 0.0)
    m = len(pts)
    for i in range(m):
        a, b = pts[i], pts[(i + 1) % m]
        n = add(n, (
            (a[1] - b[1]) * (a[2] + b[2]),
            (a[2] - b[2]) * (a[0] + b[0]),
            (a[0] - b[0]) * (a[1] + b[1]),
        ))
    return norm(n)


def hull2d(pts):
    """Infasuratoare convexa (monotone chain) pe (x, z)."""
    p = sorted(set((round(a, 4), round(b, 4)) for a, b in pts))
    if len(p) < 3:
        return p

    def half(seq):
        out = []
        for q in seq:
            while len(out) >= 2:
                o, a = out[-2], out[-1]
                if (a[0] - o[0]) * (q[1] - o[1]) - (a[1] - o[1]) * (q[0] - o[0]) <= 0:
                    out.pop()
                else:
                    break
            out.append(q)
        return out

    return half(p)[:-1] + half(reversed(p))[:-1]


def shadow_polygon(pts, h=0.02):
    """Umbra unui volum: proiectie pe teren + infasuratoare convexa."""
    if SUN[1] >= -1e-6:
        return None
    flat = []
    for p in pts:
        t = (p[1] - h) / -SUN[1]
        flat.append((p[0] + SUN[0] * t, p[2] + SUN[2] * t))
    hull = hull2d(flat)
    return [(x, h, z) for x, z in hull] if len(hull) >= 3 else None


def fit_eye(view, verts, w, h, margin=0.93):
    """Distanta camerei astfel incat tot modelul sa intre in cadru."""
    t, e = view["target"], view["eye"]
    d = sub(e, t)
    lo, hi = 0.25, 8.0
    x0, x1 = w * (1 - margin) / 2, w * (1 + margin) / 2
    y0, y1 = h * (1 - margin) / 2, h * (1 + margin) / 2
    for _ in range(34):
        mid = (lo + hi) / 2
        cam = Camera(add(t, mul(d, mid)), t, (0, 1, 0), view["fov"], w, h)
        ok = True
        for p in verts:
            c = cam.to_cam(p)
            if c[2] < cam.near:
                ok = False
                break
            s = cam.project(c)
            if not (x0 < s[0] < x1 and y0 < s[1] < y1):
                ok = False
                break
        if ok:
            hi = mid
        else:
            lo = mid
    return add(t, mul(d, hi))




# --------------------------------------------------------------------------
# vegetatie procedurala (nu face parte din modelul OBJ, doar context vizual)
# --------------------------------------------------------------------------

ARBORI = [
    (-25.0, 13.0, 0.95), (-15.0, 17.5, 0.85), (-4.5, 19.0, 1.00),
    (6.5, 17.0, 0.90), (17.0, 13.5, 0.95), (25.0, 7.0, 0.85),
    (-29.0, 4.0, 1.00), (-28.0, -6.5, 0.90), (25.0, -4.0, 0.95),
    (-22.0, 21.0, 0.80), (10.0, 23.0, 0.85), (-33.0, 12.0, 0.90),
]

TUFE = [
    (-3.9, -13.6, 0.32), (-2.4, -13.7, 0.28), (3.3, -13.6, 0.30),
    (8.15, -7.0, 0.28), (8.15, -0.2, 0.30), (-6.0, 4.2, 0.30),
    (-7.5, -6.0, 0.28), (13.0, -6.4, 0.28), (13.0, 1.8, 0.30),
    (-13.9, 8.6, 0.28), (-17.7, 8.6, 0.30),
]


def _prisma(verts, objs, name, mat, cx, cz, r, y0, y1, n=6, phase=0.0):
    """Trunchi de piramida / con cu n laturi."""
    base = len(verts)
    for i in range(n):
        a = phase + 2 * math.pi * i / n
        verts.append((cx + r[0] * math.cos(a), y0, cz + r[0] * math.sin(a)))
    for i in range(n):
        a = phase + 2 * math.pi * i / n
        verts.append((cx + r[1] * math.cos(a), y1, cz + r[1] * math.sin(a)))
    for i in range(n):
        j = (i + 1) % n
        objs.append({"name": name, "mat": mat,
                     "idx": [base + i, base + j, base + n + j, base + n + i]})
    objs.append({"name": name, "mat": mat,
                 "idx": [base + n + i for i in range(n)]})


def add_vegetatie(verts, objs, mats):
    mats["mat_trunchi"] = {"kd": (0.34, 0.27, 0.21), "d": 1.0}
    mats["mat_frunzis_1"] = {"kd": (0.33, 0.44, 0.24), "d": 1.0}
    mats["mat_frunzis_2"] = {"kd": (0.38, 0.49, 0.27), "d": 1.0}
    mats["mat_frunzis_3"] = {"kd": (0.29, 0.40, 0.22), "d": 1.0}
    mats["mat_tufa"] = {"kd": (0.36, 0.45, 0.26), "d": 1.0}

    for k, (x, z, s) in enumerate(ARBORI):
        name = "Arbore_%02d" % k
        ph = 0.4 * k
        h = 5.2 * s
        _prisma(verts, objs, name, "mat_trunchi", x, z, (0.16 * s, 0.13 * s),
                0.0, 0.42 * h, n=5, phase=ph)
        cr = 1.75 * s
        mat = "mat_frunzis_%d" % (1 + k % 3)
        _prisma(verts, objs, name, mat, x, z, (0.55 * cr, cr),
                0.34 * h, 0.60 * h, n=7, phase=ph)
        _prisma(verts, objs, name, mat, x, z, (cr, 0.70 * cr),
                0.60 * h, 0.82 * h, n=7, phase=ph + 0.3)
        _prisma(verts, objs, name, mat, x, z, (0.70 * cr, 0.05 * cr),
                0.82 * h, h, n=7, phase=ph + 0.6)

    for k, (x, z, s) in enumerate(TUFE):
        name = "Tufa_%02d" % k
        h = 3.1 * s
        _prisma(verts, objs, name, "mat_tufa", x, z, (0.9 * h, 1.05 * h),
                0.0, 0.55 * h, n=6, phase=0.7 * k)
        _prisma(verts, objs, name, "mat_tufa", x, z, (1.05 * h, 0.15 * h),
                0.55 * h, h, n=6, phase=0.7 * k + 0.4)


def render(view, verts, objs, mats, out_path, w=1500, h=940, ss=2, fit_verts=None):
    W, H = w * ss, h * ss
    eye = (fit_eye(view, fit_verts or verts, W, H)
           if view.get("fit") else view["eye"])
    up = view.get("up", (0, 1, 0))
    cam = Camera(eye, view["target"], up, view["fov"], W, H)
    fb = Frame(W, H)
    fb.sky(SKY_TOP, SKY_BOT)

    def emit(world_pts, color, alpha=1.0, zwrite=True, bias=1.0):
        cpts = clip_near([cam.to_cam(p) for p in world_pts], cam.near)
        if len(cpts) < 3:
            return None
        scr = [cam.project(c) for c in cpts]
        fb.poly(scr, color, alpha, zwrite, bias)
        return scr

    # grupare pe volume
    groups = {}
    for o in objs:
        groups.setdefault(o["name"], []).append(o)

    # 1. teren
    emit(ground_quad(cam.eye[0], cam.eye[2]), srgb(tuple(v ** 2.2 for v in GRASS)))

    # 2. umbre - o singura infasuratoare per volum opac, fara suprapuneri
    for name, faces in groups.items():
        m = mats.get(faces[0]["mat"], {"kd": (0.8,) * 3, "d": 1.0})
        a = 0.30
        if m["d"] < 0.99:
            if "Vitraj" in name:
                continue
            a = 0.13          # context: umbra doar sugerata
        pts = [verts[i] for f in faces for i in f["idx"]]
        if max(p[1] for p in pts) < 0.3:
            continue
        sh = shadow_polygon(pts)
        if sh:
            emit(sh, SHADOW, alpha=a, zwrite=False)

    # 3. volume opace
    outlines, trans = [], []
    for o in objs:
        m = mats.get(o["mat"], {"kd": (0.8,) * 3, "d": 1.0})
        pts = [verts[i] for i in o["idx"]]
        # fetele de la cota 0 sunt coplanare cu terenul - le sarim
        if max(p[1] for p in pts) < 1e-4:
            continue
        cen = mul(tuple(sum(p[k] for p in pts) for k in range(3)), 1.0 / len(pts))
        n = face_normal(pts)
        if dot(n, sub(cam.eye, cen)) < 0:
            n = mul(n, -1.0)
        if m["d"] < 0.99:
            trans.append((-dot(sub(cen, cam.eye), cam.f), pts, n, m))
            continue
        scr = emit(pts, shade(m["kd"], n))
        if scr:
            outlines.append(scr)

    # 4. transparente, din spate spre fata
    trans.sort(key=lambda t: t[0])
    for _, pts, n, m in trans:
        scr = emit(pts, shade(m["kd"], n), alpha=m["d"], zwrite=False)
        if scr:
            outlines.append(scr)

    # 5. muchii
    lw = max(1.0, ss * 1.1)
    for scr in outlines:
        for i in range(len(scr)):
            fb.line(scr[i], scr[(i + 1) % len(scr)], (0.12, 0.12, 0.14), lw, 0.5)

    # 6. ceata atmosferica dupa adancime
    col, zb = fb.col, fb.z
    for k in range(W * H):
        iz = zb[k]
        if iz <= 0.0:
            continue
        f = 1.0 - math.exp(-(1.0 / iz) / 900.0)
        if f < 0.004:
            continue
        i = k * 3
        col[i] += (HAZE[0] - col[i]) * f
        col[i + 1] += (HAZE[1] - col[i + 1]) * f
        col[i + 2] += (HAZE[2] - col[i + 2]) * f

    fb.downsample_png(out_path, ss)
    return out_path


VIEWS = {
    "01_ansamblu_sud_est": dict(
        eye=(34.0, 14.5, -33.0), target=(-2.0, 2.6, -2.0), fov=38.0, fit=True,
        titlu="Ansamblu dinspre sud-est"),
    "02_ansamblu_nord_vest": dict(
        eye=(-30.0, 13.5, -27.0), target=(-3.0, 2.6, -1.0), fov=38.0, fit=True,
        titlu="Ansamblu dinspre nord-vest, cu garajul in prim-plan"),
    "03_terasa": dict(
        eye=(9.0, 1.70, -31.0), target=(-0.5, 3.4, -8.0), fov=46.0,
        titlu="Din gradina, spre terasa si zona de distractie"),
    "04_curte_piscina": dict(
        eye=(-13.0, 1.70, -2.2), target=(8.0, 2.4, -1.6), fov=52.0,
        titlu="De pe aleea pavata, spre piscina si SPA"),
    "05_perspectiva_sud_est": dict(
        eye=(26.0, 1.80, -23.0), target=(1.5, 3.4, -6.0), fov=46.0,
        titlu="Perspectiva de la nivelul ochiului, dinspre sud-est"),
    "06_plan_de_situatie": dict(
        eye=(-2.5, 150.0, -1.9), target=(-2.5, 0.0, -2.0), fov=16.0, fit=True,
        titlu="Plan de situatie"),
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    verts, objs = load_obj(os.path.join(root, "model", "concept_wellness.obj"))
    mats = load_mtl(os.path.join(root, "model", "concept_wellness.mtl"))
    fit_verts = list(verts)
    add_vegetatie(verts, objs, mats)
    outdir = os.path.join(root, "renders")
    os.makedirs(outdir, exist_ok=True)
    for key, view in VIEWS.items():
        path = os.path.join(outdir, key + ".png")
        render(view, verts, objs, mats, path, fit_verts=fit_verts)
        print("scris", path)


if __name__ == "__main__":
    main()
