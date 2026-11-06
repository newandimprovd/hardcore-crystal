"""Bodies for the orb plan that are more than a ball: pill, puffball, coil, crystal cluster, clam, nautilus, starfish, sludge heap.

Each builder(M, d, cy, tex) adds the body in model space (y up, camera looks from +z) and returns the z of the surface in front of the face
(so the face decal sits on the body).  `feature(M, d, cy, tex)` adds the optional extras any kind can have: warts, bands, drips,
pseudopods, bubbles, junk, a halo, legs, a hat, an IV pole, tendrils."""
import math
import random

from parts import V
from sdf import ACCENT, BODY, BONE, DARK


def ring(M, c, rad, thick, mat, a0=0.0, a1=2 * math.pi, n=16, plane="xz", k=0.04, tex=None):
    """A thin tube along a circle (or an arc) around c in the xz (flat), xy (facing the viewer) or yz plane."""
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        u, v = math.cos(a) * rad, math.sin(a) * rad
        pts.append((c[0] + u, c[1], c[2] + v) if plane == "xz" else (c[0] + u, c[1] + v, c[2]) if plane == "xy" else (c[0], c[1] + u, c[2] + v))
    M.tube(pts, thick, thick, mat, k, tex=tex)


def fib(n, skip=None):
    """n points on the unit sphere (golden spiral), those for which skip(x, y, z) is true left out."""
    out = []
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        rr = math.sqrt(max(0.0, 1 - y * y))
        a = i * 2.399963
        p = (math.cos(a) * rr, y, math.sin(a) * rr)
        if not (skip and skip(*p)):
            out.append(p)
    return out


def pill(M, d, cy, tex):
    r = d["r"]
    ang = math.radians(d.get("tilt", 22))
    ux, uy = math.cos(ang), math.sin(ang)
    L = r * 1.05
    a, b, mid = V(-ux * L, cy - uy * L, 0), V(ux * L, cy + uy * L, 0), V(0, cy, 0)
    M.cone(a, mid, r * 0.88, r * 0.9, BODY, 0.1, tex=tex)
    M.part()
    M.cone(mid, b, r * 0.9, r * 0.88, ACCENT, 0.1)
    M.part()
    for i in range(4):  # a shine on the upper half
        M.ell(V(-ux * L * 0.55, cy - uy * L * 0.55 + r * (0.45 - 0.1 * i), r * 0.62), (0.05, 0.12, 0.05), BONE, 0.02)
    return r * 0.88


def puff(M, d, cy, tex):
    r = d["r"]
    M.ell((0, cy, 0), (r * 0.9, r * 0.9, r * 0.85), BODY, 0.2, tex=tex)
    M.part()
    for (x, y, z) in fib(d.get("puff_n", 34), skip=lambda x, y, z: z > 0.45 and abs(x) < 0.65 and -0.7 < y < 0.5):
        base = V(x * r * 0.85, cy + y * r * 0.85, z * r * 0.8)
        tip = base + V(x, y, z) * r * 0.75
        M.spike(base, tip, 0.05, BONE, 0.02)
        M.ell(tip + V(x, y, z) * 0.05, (0.15, 0.15, 0.15), ACCENT if (x + y) > 0 else BONE, 0.04)
    return r * 0.8


def coil(M, d, cy, tex):
    r = d["r"]
    M.cone(V(0, cy - r * 0.95, 0), V(0, cy + r * 0.95, 0), r * 0.6, r * 0.6, BODY, 0.1, tex=tex)
    M.part()
    n = d.get("turns", 6)
    for i in range(n):
        y = cy - r * 0.8 + 1.6 * r * i / (n - 1)
        ring(M, (0, y, 0), r * 0.82, 0.075, ACCENT, n=14, k=0.03)
    M.part()
    for sy in (-1, 1):
        M.ell((0, cy + sy * r * 1.0, 0), (r * 0.7, r * 0.2, r * 0.7), BONE, 0.08)
        for dx in (-0.4, 0.0, 0.4):
            M.spike(V(dx * r, cy + sy * r * 1.1, 0), V(dx * r * 1.4, cy + sy * r * 1.65, 0), 0.07, ACCENT, 0.02)
    for sx in (-1, 1):  # bolts of lightning between the electrodes, drawn as thin plates
        p = [V(sx * r * 0.5, cy + r * 1.7, 0.1), V(sx * r * 0.85, cy + r * 1.35, 0.15), V(sx * r * 0.6, cy + r * 1.35, 0.15), V(sx * r * 1.0, cy + r * 0.9, 0.2)]
        M.tri(p[0], p[1], p[2], 0.03, BONE)
        M.tri(p[1], p[2], p[3], 0.03, BONE)
    return r * 0.62


def cubes(M, d, cy, tex):
    r = d["r"]
    M.box((0, cy, 0), (r * 0.72,) * 3, 0.1, BODY, 0.06, rot=(0.35, 0.65, 0.2), tex=tex)
    M.part()
    mats = [ACCENT, BONE, BODY]
    for i in range(d.get("sat_n", 6)):
        a = i * 6.283 / max(d.get("sat_n", 6), 1) + 0.4
        M.box((math.cos(a) * r * 1.45, cy + math.sin(a * 1.3) * r * 0.9, math.sin(a) * r * 0.5), (d["sat_r"] * 0.7,) * 3, 0.05, mats[i % 3], 0.04,
              rot=(a, 0.5 * a, 0.3))
    M.part()
    for i in range(5):  # a trail of falling pixels
        s = 0.2 - 0.03 * i
        M.box((-r * 0.9 - 0.05 * i, cy - r * 0.9 - 0.3 * i, -r * 0.4), (s,) * 3, 0.02, mats[i % 3], 0.02, rot=(0.3 * i, 0.4, 0.1))
    return r * 0.8


def magnets(M, d, cy, tex):
    """A glossy core with three horseshoe magnets round it on struts, red and white poles."""
    r = d["r"]
    M.ell((0, cy, 0), (r * 0.8, r * 0.8, r * 0.75), BODY, 0.2, tex=tex)
    for i in range(3):
        a = math.radians(90 + 120 * i)
        cx, cyy = math.cos(a) * r * 1.65, cy + math.sin(a) * r * 1.2
        M.part()
        M.tube([V(math.cos(a) * r * 0.6, cy + math.sin(a) * r * 0.6, 0), V(cx * 0.8, cyy * 0.9 + cy * 0.1, 0.05)], 0.1, 0.1, ACCENT, 0.04)
        sr = d["sat_r"]
        ring(M, (cx, cyy, 0.05), sr * 1.1, sr * 0.42, BODY, a0=a + 0.9, a1=a + 2 * math.pi - 0.9, n=14, plane="xy", k=0.03)
        for sgn, mat in ((-1, ACCENT), (1, BONE)):  # the two poles at the ends of the horseshoe
            ang = a + (0.9 if sgn < 0 else 2 * math.pi - 0.9)
            px, py = cx + math.cos(ang) * sr * 1.1, cyy + math.sin(ang) * sr * 1.1
            M.box((px, py, 0.05), (sr * 0.5, sr * 0.5, sr * 0.45), 0.03, mat, 0.02, rot=(0, 0, ang))
    return r * 0.72


def clam(M, d, cy, tex):
    r = d["r"]
    M.ell((0, cy - r * 0.05, r * 0.1), (r * 0.8, r * 0.5, r * 0.7), ACCENT, 0.15)  # the soft body inside
    M.part()
    M.ell((0, cy + r * 0.7, -r * 0.15), (r * 1.4, r * 0.62, r * 1.15), BODY, 0.12, rot=(-0.45, 0, 0), tex=tex)
    M.ell((0, cy - r * 0.78, -r * 0.1), (r * 1.4, r * 0.5, r * 1.1), BODY, 0.12, rot=(0.3, 0, 0), tex=tex)
    M.part()
    for i in range(-3, 4):  # ribs of the upper shell
        a = i * 0.3
        M.cone(V(math.sin(a) * r * 0.2, cy + r * 0.6, -r * 0.55), V(math.sin(a) * r * 1.3, cy + r * 0.95, r * 0.45), 0.09, 0.05, ACCENT, 0.03)
    for i in range(-2, 3):  # icicle teeth along the lips
        x = i * r * 0.5
        M.spike(V(x, cy + r * 0.28, r * 0.78), V(x, cy - r * 0.15, r * 0.88), 0.1, BONE, 0.02)
        M.spike(V(x + r * 0.25, cy - r * 0.38, r * 0.78), V(x + r * 0.25, cy + r * 0.05, r * 0.88), 0.09, BONE, 0.02)
    M.ell((r * 0.55, cy - r * 0.1, r * 0.55), (0.2, 0.2, 0.2), BONE, 0.04)  # the pearl
    return r * 0.62


def nautilus(M, d, cy, tex):
    """A coiled shell (a log spiral of growing tube, each whorl its own part so the shader inks the whorls apart) with the soft body in its
    mouth, tentacles and a row of spines on the outer whorl."""
    r = d["r"]
    cx, cyy, cz = -0.5 * r, cy + 0.2 * r, -0.3 * r
    T = 4 * math.pi
    b = math.log(8.0) / T
    end_rho, end_tube = 1.0 * r, 0.55 * r
    n = 28
    pts = [(cx + end_rho * math.exp(b * (T * k / n - T)) * math.cos(T * k / n), cyy + end_rho * math.exp(b * (T * k / n - T)) * math.sin(T * k / n), cz)
           for k in range(n + 1)]
    rads = [end_tube * math.exp(b * (T * k / n - T)) for k in range(n + 1)]
    for s0 in range(0, n, 7):
        seg = pts[max(0, s0 - 1):s0 + 8]
        rr = rads[max(0, s0 - 1):s0 + 8]
        M.part()
        M.tube(seg, rr[0], rr[-1], BODY, 0.05, tex=tex, steps=len(seg) * 2, rfn=lambda u, rr=rr: rr[min(len(rr) - 1, int(u * (len(rr) - 1)))])
    M.part()
    mouth = V(pts[-1][0], pts[-1][1], pts[-1][2])
    M.ell(mouth + V(0.1 * r, -0.05 * r, 0.35 * r), (r * 0.62, r * 0.55, r * 0.5), ACCENT, 0.15)  # the soft body in the mouth of the shell
    M.part()
    for i in range(d.get("shell_spikes", 8)):
        t = T * (0.62 + 0.38 * i / max(d.get("shell_spikes", 8) - 1, 1))
        rho = end_rho * math.exp(b * (t - T)) + end_tube * math.exp(b * (t - T)) * 0.9
        bx, by = cx + rho * math.cos(t), cyy + rho * math.sin(t)
        M.spike(V(bx, by, cz + 0.1), V(bx + math.cos(t) * r * 0.45, by + math.sin(t) * r * 0.45, cz + 0.15), 0.1, BONE, 0.02)
    for i in range(5):  # tentacles from the mouth
        a = -0.5 + i * 0.3
        pts2 = [mouth + V(0.4 * r, -0.2 * r, 0.5 * r), mouth + V(0.8 * r, -0.35 * r + a * 0.3, 0.8 * r), mouth + V(1.0 * r, -0.8 * r + 0.2 * i, 1.0 * r)]
        M.tube(pts2, 0.12, 0.03, ACCENT, 0.05)
    return mouth[2] + r * 0.75


def starfish(M, d, cy, tex):
    r = d["r"]
    n = d.get("star_arms", 5)
    curl = d.get("curl", 0.5)
    M.ell((0, cy, 0), (r * 0.78, r * 0.78, r * 0.5), BODY, 0.2, tex=tex)
    M.part()
    for i in range(n):
        a = math.radians(90 + 360 * i / n)
        pts = []
        for s in (0, 0.3, 0.6, 1.0):
            L = r * (0.3 + 1.7 * s)
            aa = a + curl * s * s
            pts.append(V(math.cos(aa) * L, cy + math.sin(aa) * L, -0.12 * s * r))
        M.tube(pts, r * 0.44, r * 0.07, BODY, 0.1, tex=tex)
        M.part()
        for s in (0.25, 0.45, 0.65, 0.82):  # a ridge of nodules down the arm and the tube feet at its edge
            L = r * (0.3 + 1.7 * s)
            aa = a + curl * s * s
            c = V(math.cos(aa) * L, cy + math.sin(aa) * L, 0.12 * r)
            M.ell(c, (r * 0.11 * (1.2 - s),) * 3, ACCENT if s < 0.7 else BONE, 0.03)
            side = V(-math.sin(aa), math.cos(aa), 0) * r * 0.3 * (1.1 - s)
            M.ell(c + side, (0.05,) * 3, BONE, 0.02)
            M.ell(c - side, (0.05,) * 3, BONE, 0.02)
        M.part()
    if d.get("halo"):
        ring(M, (0, cy, -r * 0.2), r * 1.95, 0.04, BONE, n=24, plane="xy")
    return r * 0.5


def heap(M, d, cy, tex):
    """A sludge mound: a wide low body with a second mass on top and a drooping lip, so the face sits in a melting layer."""
    r = d["r"]
    M.ell((0, cy - r * 0.3, 0), (r * 1.25, r * 0.78, r * 1.05), BODY, 0.2, tex=tex)
    M.ell((r * 0.1, cy + r * 0.45, -r * 0.1), (r * 0.8, r * 0.6, r * 0.7), BODY, 0.2, tex=tex)
    M.ell((0, cy - r * 0.9, r * 0.2), (r * 1.4, r * 0.3, r * 1.2), BODY, 0.2, tex=tex)
    return r * 0.85


KINDS = {"magnets": magnets, "pill": pill, "puff": puff, "coil": coil, "cubes": cubes, "clam": clam, "nautilus": nautilus, "starfish": starfish, "heap": heap}


def feature(M, d, cy, tex, rnd):
    """Extras any orb can have."""
    r = d["r"]
    hover = d["hover"]
    if d.get("bumps"):  # warts / barnacles / pustules over the front and sides
        M.part()
        for (x, y, z) in fib(d["bumps"] * 2, skip=lambda x, y, z: z < -0.2 or (z > 0.45 and abs(x) < 0.6 and -0.5 < y < 0.55)):
            p = V(x, y, z) * r * 0.98
            M.ell(V(0, cy, 0) + p, (0.1 * r + 0.03,) * 3, d.get("bump_mat", BONE) if (x * 7 + y * 3) % 2 > 1 else ACCENT, 0.04)
    for i in range(d.get("bands", 0)):  # bands round the middle
        ring(M, (0, cy + (i - (d["bands"] - 1) / 2) * r * 0.45, 0), r * 1.03, 0.06, ACCENT, n=18, plane="xz")
    if d.get("drips"):
        M.part()
        for i in range(d["drips"]):
            x = (i - (d["drips"] - 1) / 2) * r * 0.55
            M.tube([V(x, cy - r * 0.6, r * 0.55), V(x * 1.05, hover + r * 0.3, r * 0.65), V(x * 1.05, hover + 0.1, r * 0.7)], 0.1, 0.07, BODY, 0.08, tex=tex)
            M.ell(V(x * 1.05, hover + 0.08, r * 0.7), (0.15, 0.1, 0.15), BODY, 0.05, tex=tex)
    if d.get("pods"):
        M.part()
        for i in range(d["pods"]):
            a = math.radians(-70 + 140 * i / max(d["pods"] - 1, 1) + 90 * (1 if i % 2 else 0))
            p0 = V(math.cos(a) * r * 0.8, hover + r * 0.25, math.sin(a) * r * 0.8)
            p1 = V(math.cos(a) * r * 1.45, hover + 0.12, math.sin(a) * r * 1.45)
            M.tube([p0, (p0 + p1) * 0.5 + V(0, 0.1, 0), p1], 0.2, 0.1, BODY, 0.1, tex=tex)
            M.ell(p1, (0.17, 0.12, 0.17), BODY, 0.05, tex=tex)
    if d.get("bubbles"):
        M.part()
        for (x, y, z) in fib(d["bubbles"] * 3, skip=lambda x, y, z: z < 0.0 or (z > 0.45 and abs(x) < 0.6 and -0.5 < y < 0.55)):
            M.ell(V(0, cy, 0) + V(x, y, z) * r * 1.0, (0.13, 0.13, 0.13), BONE, 0.03)
    if d.get("junk"):
        M.part()
        for i in range(d["junk"]):
            a = math.radians(210 + 150 * i / max(d["junk"] - 1, 1))
            p = V(math.cos(a) * r * 1.15, cy + math.sin(a) * r * 0.7 - r * 0.2, rnd.uniform(-0.3, 0.4) * r)
            if i % 2:
                M.box(p, (0.17, 0.2, 0.17), 0.03, ACCENT, 0.03, rot=(0.3 * i, 0.5 * i, 0.2))
            else:
                M.cone(p, p + V(0.25 * math.cos(a), 0.25 * math.sin(a), 0.1), 0.15, 0.15, DARK, 0.02)
    if d.get("halo"):
        ring(M, (0, cy + r * 1.35, 0), r * 0.6, 0.06, BONE, n=18, plane="xz")
    if d.get("hat"):
        M.part()
        M.cone(V(0, cy + r * 1.0, 0), V(0, cy + r * 1.6, 0), r * 0.5, r * 0.05, ACCENT, 0.06)
        M.ell(V(0, cy + r * 1.02, 0), (r * 0.95, 0.07, r * 0.95), ACCENT, 0.04)
    if d.get("legs"):
        M.part()
        for sx in (-1, 1):
            M.cone(V(sx * r * 0.45, hover + r * 0.25, 0.1), V(sx * r * 0.5, hover + 0.1, 0.25), 0.13, 0.13, BODY, 0.05)
            M.ell(V(sx * r * 0.5, hover + 0.06, 0.4), (0.26, 0.08, 0.4), DARK, 0.03)
    if d.get("valve"):
        M.cone(V(r * 0.6, cy + r * 0.8, -r * 0.3), V(r * 0.75, cy + r * 1.0, -r * 0.35), 0.1, 0.07, ACCENT, 0.03)
    if d.get("iv"):  # an IV pole held at the side: pole, hook, bag, line
        M.part()
        px = r * 1.35
        M.cone(V(px, hover - 0.1, 0.3), V(px, cy + r * 1.5, 0.3), 0.04, 0.04, BONE, 0.02)
        M.ell(V(px - 0.2, cy + r * 1.25, 0.3), (0.16, 0.26, 0.1), BODY, 0.03)
        M.tube([V(px - 0.2, cy + r * 1.0, 0.3), V(px - 0.4, cy + r * 0.4, 0.45), V(px - 0.5, cy + r * 0.1, 0.55)], 0.025, 0.025, DARK, 0.02)
        M.ell(V(px, hover - 0.08, 0.3), (0.35, 0.06, 0.35), DARK, 0.02)
    if d.get("tendrils"):
        M.part()
        for i in range(d["tendrils"]):
            a = 0.5 + i * 6.283 / d["tendrils"]
            p0 = V(math.cos(a) * r * 0.7, cy - r * 0.4, math.sin(a) * r * 0.5)
            M.tube([p0, p0 + V(math.cos(a) * 0.4, -r * 0.6, -0.2), p0 + V(math.cos(a + 1) * 0.6, -r * 1.2, -0.4)], 0.2, 0.03, BODY, 0.1, tex=tex)
    if d.get("virus"):
        M.part()
        for (x, y, z) in fib(d["virus"], skip=lambda x, y, z: z > 0.4 and abs(x) < 0.6 and -0.5 < y < 0.55):
            b = V(0, cy, 0) + V(x, y, z) * r * 0.9
            t = b + V(x, y, z) * r * 0.5
            M.cone(b, t, 0.06, 0.05, ACCENT, 0.02)
            M.ell(t + V(x, y, z) * 0.08, (0.14, 0.14, 0.14), ACCENT, 0.03)
