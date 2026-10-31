"""Reusable creature parts for the SDF renderer.  Every function draws into a Model in the model's current frame (see Model.frame) and
returns nothing unless noted.  Anchors are registered through Model.anchor, so they follow frames.

Conventions of a local frame: y up, the creature faces +z, +x is the creature's left (the viewer's right in the front view).
"""
import math

import numpy as np

import sdf
from sdf import ACCENT, BODY, BONE, DARK, EYE, Model


def V(*a):
    return np.array(a, float)


# ============================================================================================ horns, spikes, crests
def horn(M, base, tip, r, bend=(0, 0, 0), mat=BONE, mirror=True, k=0.04, tex=None, segs=4):
    """A horn from base to tip, bent sideways by `bend` (added at the middle, quadratic)."""
    b, t = V(*base), V(*tip)
    pts = []
    for i in range(segs + 1):
        s = i / segs
        p = b + (t - b) * s + V(*bend) * (4 * s * (1 - s))
        pts.append(p)
    for i in range(segs):
        ra = r * (1 - i / segs) + 0.004
        rb = r * (1 - (i + 1) / segs) + 0.004
        M.cone(pts[i], pts[i + 1], ra, rb, mat, k, mirror, tex=tex)


def antlers(M, base, size, mat=BONE, mirror=True):
    b = V(*base)
    M.tube([b, b + V(0.15, 0.35, -0.1) * size, b + V(0.3, 0.7, -0.15) * size], 0.06 * size, 0.025 * size, mat, 0.03, mirror)
    for f in (0.45, 0.8):
        s0 = b + V(0.3 * f, 0.7 * f, -0.15 * f) * size
        M.spike(s0, s0 + V(-0.05, 0.3, 0.2) * size, 0.04 * size, mat, 0.02, mirror)
        M.spike(s0, s0 + V(0.25, 0.25, -0.1) * size, 0.04 * size, mat, 0.02, mirror)


def row_spikes(M, pts, size, r, direction=(0, 1, -0.5), mat=BONE, taper=0.3, mirror=False, k=0.03, tex=None):
    """A row of spikes standing on the points pts, pointing along `direction` (not normalised); sizes ramp up then down."""
    n = len(pts)
    d = V(*direction)
    d = d / np.linalg.norm(d)
    for i, p in enumerate(pts):
        f = 1.0 - taper * abs((i + 0.5) / n * 2 - 1)
        M.spike(V(*p), V(*p) + d * size * f, r * (0.6 + 0.4 * f), mat, k, mirror, tex=tex)


def plates(M, pts, size, mat=ACCENT, mirror=False, k=0.05, tex=None):
    """Armour plates: flattened ellipsoids on the points, facing +z."""
    for p in pts:
        M.ell(p, (size, size * 0.8, size * 0.35), mat, k, mirror, tex=tex)


# ============================================================================================ hands and feet
def hand(M, wrist, kind="fist", size=1.0, mirror=True, claws=3, mat=BODY, claw_mat=BONE, dirn=(0.1, -1.0, 0.5)):
    """Hand at the wrist point.  kinds: fist (big knuckled fist), claw (open hand with long claws), blade (a blade grows from the arm), paw."""
    w = V(*wrist)
    d = V(*dirn)
    d = d / np.linalg.norm(d)
    side = V(1, 0, 0)
    if kind == "fist":
        M.ell(w + d * 0.14 * size, (0.20 * size, 0.18 * size, 0.2 * size), mat, 0.08, mirror)
        for i in range(claws):
            o = (i - (claws - 1) / 2) * 0.1 * size
            M.spike(w + d * 0.2 * size + side * o + V(0, 0, 0.12 * size), w + d * 0.34 * size + side * o * 1.4 + V(0, 0, 0.2 * size), 0.05 * size, claw_mat, 0.02, mirror)
    elif kind == "claw":
        M.ell(w + d * 0.1 * size, (0.16 * size, 0.1 * size, 0.18 * size), mat, 0.06, mirror)
        for i in range(claws):
            o = (i - (claws - 1) / 2) * 0.11 * size
            M.spike(w + d * 0.12 * size + side * o, w + d * 0.5 * size + side * o * 1.5 + V(0, 0, 0.1 * size), 0.045 * size, claw_mat, 0.02, mirror)
    elif kind == "blade":
        M.tri(w, w + d * 0.9 * size + V(0, 0, 0.1), w + side * 0.0 + d * 0.3 * size + V(0.0, 0.0, 0.32 * size), 0.04, BONE, 0.0, mirror)
        M.tri(w, w + d * 0.9 * size + V(0, 0, 0.1), w + d * 0.3 * size + V(0.0, 0.0, -0.1 * size) + side * 0.18 * size, 0.04, BONE, 0.0, mirror)
        M.ell(w, (0.14 * size, 0.14 * size, 0.14 * size), mat, 0.05, mirror)
    elif kind == "paw":
        M.ell(w + d * 0.1 * size, (0.15 * size, 0.1 * size, 0.17 * size), mat, 0.06, mirror)
        for i in range(claws):
            o = (i - (claws - 1) / 2) * 0.08 * size
            M.spike(w + d * 0.12 * size + side * o + V(0, 0, 0.1 * size), w + d * 0.2 * size + side * o * 1.1 + V(0, 0, 0.22 * size), 0.03 * size, claw_mat, 0.015, mirror)


def foot(M, ankle, kind="plant", size=1.0, mirror=True, mat=BODY, claw_mat=BONE, toes=3):
    a = V(*ankle)
    if kind == "plant":
        M.ell(a + V(0, -0.03, 0.18) * size, (0.2 * size, 0.1 * size, 0.3 * size), mat, 0.07, mirror)
    elif kind == "hoof":
        M.cone(a + V(0, 0.0, 0.0), a + V(0, -0.12 * size, 0.04), 0.1 * size, 0.12 * size, DARK if False else BONE, 0.03, mirror)
        return
    elif kind == "paw":
        M.ell(a + V(0, -0.03, 0.12) * size, (0.15 * size, 0.09 * size, 0.2 * size), mat, 0.06, mirror)
    elif kind == "talon":
        M.ell(a + V(0, -0.03, 0.08) * size, (0.13 * size, 0.08 * size, 0.14 * size), mat, 0.05, mirror)
        for i in range(toes):
            o = (i - (toes - 1) / 2) * 0.14 * size
            M.cone(a + V(o * 0.4, -0.04, 0.05), a + V(o, -0.06, 0.4 * size), 0.05 * size, 0.025 * size, mat, 0.03, mirror)
            M.spike(a + V(o, -0.06, 0.38 * size), a + V(o * 1.2, -0.1, 0.55 * size), 0.035 * size, claw_mat, 0.015, mirror)
        return
    for i in range(toes):
        o = (i - (toes - 1) / 2) * 0.11 * size
        M.spike(a + V(o, -0.04, 0.38 * size), a + V(o * 1.2, -0.08, 0.58 * size), 0.045 * size, claw_mat, 0.02, mirror)


# ============================================================================================ tails
def tail(M, base, kind="plain", length=1.2, thick=0.22, curl=0.3, up=0.0, sway=0.0, mat=BODY, tip_mat=ACCENT, tex=None):
    """A tail from `base` going back (-z), drooping then curling up by `curl`; sway moves the tip sideways."""
    b = V(*base)
    pts = [b, b + V(0, -0.1, -length * 0.35), b + V(sway * 0.4, -0.05 + up * 0.5, -length * 0.7), b + V(sway, curl + up, -length)]
    end_r = {"plain": 0.05, "club": 0.2, "blade": 0.06, "spike": 0.04}.get(kind, 0.05)
    M.tube(pts, thick, end_r, mat, 0.1, False, 8, tex=tex)
    tip = pts[-1]
    if kind == "club":
        M.ell(tip + V(0, 0.02, -0.05), (0.3, 0.26, 0.3), mat, 0.08, tex=tex)
        for a in (0, 1, 2, 3, 4, 5):
            ang = a * math.pi / 3
            M.spike(tip + V(math.cos(ang) * 0.26, math.sin(ang) * 0.24, -0.05), tip + V(math.cos(ang) * 0.5, math.sin(ang) * 0.46, -0.05), 0.07, BONE)
    elif kind == "blade":
        M.tri(tip + V(0, 0.0, 0.1), tip + V(0, 0.0, -0.7), tip + V(0, 0.35, -0.2), 0.04, BONE, 0.0)
        M.tri(tip + V(0, 0.0, 0.1), tip + V(0, 0.0, -0.7), tip + V(0, -0.35, -0.2), 0.04, BONE, 0.0)
    elif kind == "spike":
        M.spike(tip, tip + V(0, 0.1, -0.45), 0.09, BONE)
        for s in (0.45, 0.65, 0.85):
            p = spline_pt(pts, s)
            M.spike(p + V(0, 0.05, 0), p + V(0, 0.35, -0.15), 0.07, BONE)
    elif kind == "flame":
        flame(M, tip, 0.45, mat=tip_mat)


def spline_pt(pts, s):
    return sdf.spline3(pts, s)


def flame(M, base, size, mat=ACCENT, up=(0, 1, -0.3), k=0.12):
    """A little flame: a teardrop of three cones."""
    b = V(*base)
    d = V(*up)
    d = d / np.linalg.norm(d)
    M.cone(b, b + d * size * 1.4, size * 0.4, 0.01, mat, k)
    M.cone(b + V(0.05, 0, 0), b + d * size * 1.0 + V(0.28 * size, 0, 0), size * 0.28, 0.01, mat, k)
    M.cone(b - V(0.05, 0, 0), b + d * size * 0.9 - V(0.28 * size, 0, 0), size * 0.26, 0.01, mat, k)


# ============================================================================================ wings
def wing_bat(M, shoulder, span=1.6, height=1.0, back=0.5, mat=ACCENT, bone_mat=BODY, mirror=True, fold=0.0, tex=None):
    """Bat or dragon wing: arm bone, three finger bones fanning out, membrane triangles between them."""
    s = V(*shoulder)
    elbow = s + V(span * 0.38, height * 0.35, -back * 0.2)
    tip0 = s + V(span * 0.9 * (1 - 0.5 * fold), height * 1.05, -back * 0.6)
    fingers = [tip0,
               s + V(span * 1.0 * (1 - 0.5 * fold), height * 0.45, -back * 1.0),
               s + V(span * 0.82 * (1 - 0.5 * fold), -height * 0.1, -back * 1.2),
               s + V(span * 0.5, -height * 0.35, -back * 0.9)]
    wrist = elbow + (tip0 - elbow) * 0.25
    M.cone(s, elbow, 0.1, 0.07, bone_mat, 0.05, mirror)
    M.cone(elbow, wrist, 0.07, 0.05, bone_mat, 0.04, mirror)
    prev = None
    for f in fingers:
        M.cone(wrist, f, 0.045, 0.012, bone_mat, 0.02, mirror)
        if prev is not None:
            M.tri(wrist, prev, f, 0.03, mat, 0.0, mirror, tex=tex)
        prev = f
    M.tri(s + V(0, -0.05, -0.1), wrist, fingers[-1], 0.03, mat, 0.0, mirror, tex=tex)
    M.spike(wrist, wrist + V(0.05, 0.22, 0.1), 0.045, BONE, 0.02, mirror)


# ============================================================================================ heads
def head(M, kind, c, s=1.0, jaw=0.0, brow=1.0, ears=None, horns_=None, eye="angry", teeth=3, mat=BODY, accent=ACCENT, tex=None, snout=1.0):
    """A head centred at c (cranium centre), scale s.  Registers the anchors eye_l, eye_r, mouth_a, mouth_b and returns the face dict."""
    c = V(*c)

    def at(x, y, z):
        return c + V(x, y, z) * s
    face = dict(eye=eye, teeth=teeth, size=1.0 + 0.3 * (s > 1.2))
    if kind == "beast":
        M.ell(c, (0.38 * s, 0.34 * s, 0.38 * s), mat, 0.15, tex=tex)
        M.ell(at(0, -0.10, 0.34), (0.23 * s, 0.15 * s, 0.26 * s * snout), mat, 0.1, tex=tex)
        M.ell(at(0, -0.26 - 0.15 * jaw, 0.28), (0.21 * s, 0.07 * s, 0.25 * s * snout), mat, 0.05, tex=tex)
        M.cone(at(0.06, 0.13, 0.30), at(0.34, 0.21, 0.08), 0.08 * s * brow, 0.07 * s * brow, mat, 0.08, True, tex=tex)
        eyes = ((0.19, 0.06, 0.36),)
        mouth = ((0.24, -0.20, 0.52 * snout),)
    elif kind == "ape":
        M.ell(c, (0.36 * s, 0.32 * s, 0.34 * s), mat, 0.15, tex=tex)
        M.ell(at(0, -0.08, 0.26), (0.28 * s, 0.2 * s, 0.2 * s), mat, 0.1, tex=tex)
        M.ell(at(0, -0.25 - 0.14 * jaw, 0.24), (0.25 * s, 0.09 * s, 0.2 * s), mat, 0.05, tex=tex)
        M.cone(at(0.0, 0.12, 0.28), at(0.3, 0.2, 0.2), 0.1 * s * brow, 0.09 * s * brow, mat, 0.08, True, tex=tex)
        eyes = ((0.16, 0.05, 0.40),)
        mouth = ((0.25, -0.2, 0.40),)
    elif kind == "croc":
        M.ell(c, (0.32 * s, 0.26 * s, 0.34 * s), mat, 0.12, tex=tex)
        M.ell(at(0, -0.05, 0.62), (0.2 * s, 0.1 * s, 0.5 * s * snout), mat, 0.08, tex=tex)
        M.ell(at(0, -0.17 - 0.2 * jaw, 0.58), (0.2 * s, 0.06 * s, 0.5 * s * snout), mat, 0.04, tex=tex)
        M.ell(at(0.2, 0.2, 0.16), (0.1 * s, 0.1 * s, 0.1 * s), mat, 0.05, True, tex=tex)
        eyes = ((0.2, 0.2, 0.2),)
        mouth = ((0.2, -0.12, 1.0 * snout),)
    elif kind == "owl":
        M.ell(c, (0.42 * s, 0.38 * s, 0.38 * s), mat, 0.15, tex=tex)
        M.ell(at(0.18, 0.04, 0.3), (0.19 * s, 0.19 * s, 0.1 * s), BONE, 0.03, True)
        M.cone(at(0, -0.04, 0.38), at(0, -0.2 - 0.06 * jaw, 0.62), 0.1 * s, 0.025 * s, BONE, 0.02)
        M.cone(at(0, -0.12, 0.36), at(0, -0.16 - 0.1 * jaw, 0.52), 0.06 * s, 0.02 * s, BONE, 0.02)
        eyes = ((0.18, 0.04, 0.4),)
        face["eye"] = "round" if eye == "angry" else eye
        mouth = None
    elif kind == "skull":
        M.ell(c, (0.36 * s, 0.34 * s, 0.34 * s), BONE, 0.1)
        M.ell(at(0, -0.2 - 0.12 * jaw, 0.22), (0.2 * s, 0.1 * s, 0.2 * s), BONE, 0.05)
        M.ell(at(0.15, 0.04, 0.3), (0.1 * s, 0.1 * s, 0.1 * s), DARK, 0.0, True)
        eyes = ((0.15, 0.04, 0.4),)
        face["eye"] = "hollow"
        mouth = ((0.14, -0.14, 0.4),)
    elif kind == "bird":
        M.ell(c, (0.3 * s, 0.28 * s, 0.34 * s), mat, 0.12, tex=tex)
        M.cone(at(0, -0.02, 0.3), at(0, -0.12, 0.8 * snout), 0.15 * s, 0.04 * s, BONE, 0.03)
        M.cone(at(0, -0.1, 0.3), at(0, -0.22 - 0.2 * jaw, 0.74 * snout), 0.09 * s, 0.03 * s, BONE, 0.03)
        eyes = ((0.2, 0.08, 0.26),)
        mouth = None
        face["eye"] = "angry" if eye == "angry" else eye
    elif kind == "dragon":
        M.ell(c, (0.34 * s, 0.3 * s, 0.38 * s), mat, 0.12, tex=tex)
        M.ell(at(0, -0.06, 0.48), (0.2 * s, 0.13 * s, 0.34 * s * snout), mat, 0.08, tex=tex)
        M.ell(at(0, -0.24 - 0.16 * jaw, 0.42), (0.18 * s, 0.06 * s, 0.34 * s * snout), mat, 0.04, tex=tex)
        M.cone(at(0.05, 0.12, 0.32), at(0.26, 0.2, 0.16), 0.08 * s * brow, 0.06 * s * brow, mat, 0.06, True, tex=tex)
        eyes = ((0.19, 0.07, 0.32),)
        mouth = ((0.2, -0.17, 0.76 * snout),)
    elif kind == "cat":
        M.ell(c, (0.4 * s, 0.32 * s, 0.34 * s), mat, 0.15, tex=tex)
        M.ell(at(0, -0.1, 0.3), (0.2 * s, 0.13 * s, 0.14 * s), mat, 0.08, tex=tex)
        M.ell(at(0, -0.24 - 0.12 * jaw, 0.25), (0.15 * s, 0.06 * s, 0.14 * s), mat, 0.05, tex=tex)
        eyes = ((0.2, 0.05, 0.3),)
        mouth = ((0.16, -0.18, 0.4),)
    elif kind == "rodent":
        M.ell(c, (0.34 * s, 0.3 * s, 0.36 * s), mat, 0.15, tex=tex)
        M.cone(at(0, -0.02, 0.28), at(0, -0.08, 0.66 * snout), 0.17 * s, 0.07 * s, mat, 0.08, tex=tex)
        M.ell(at(0, -0.2 - 0.12 * jaw, 0.34), (0.14 * s, 0.06 * s, 0.2 * s), mat, 0.04, tex=tex)
        M.box(at(0.0, -0.17 - 0.06 * jaw, 0.58 * snout), (0.045 * s, 0.1 * s, 0.025 * s), 0.01, BONE, 0.0)
        eyes = ((0.18, 0.07, 0.3),)
        mouth = ((0.12, -0.15, 0.55 * snout),)
    elif kind == "horse":
        M.ell(c, (0.28 * s, 0.3 * s, 0.34 * s), mat, 0.12, tex=tex)
        M.ell(at(0, -0.12, 0.55), (0.17 * s, 0.17 * s, 0.4 * s * snout), mat, 0.1, tex=tex)
        M.ell(at(0, -0.3 - 0.1 * jaw, 0.52), (0.13 * s, 0.06 * s, 0.34 * s * snout), mat, 0.04, tex=tex)
        eyes = ((0.2, 0.08, 0.2),)
        mouth = ((0.12, -0.24, 0.86 * snout),)
    elif kind == "duck":
        M.ell(c, (0.4 * s, 0.38 * s, 0.38 * s), mat, 0.15, tex=tex)
        M.ell(at(0, -0.1, 0.5), (0.26 * s, 0.07 * s, 0.26 * s * snout), accent, 0.04)
        M.ell(at(0, -0.2 - 0.1 * jaw, 0.46), (0.22 * s, 0.05 * s, 0.22 * s * snout), accent, 0.03)
        eyes = ((0.2, 0.1, 0.32),)
        mouth = None
    elif kind == "robot":
        M.box(c, (0.36 * s, 0.3 * s, 0.34 * s), 0.07 * s, mat, 0.05, tex=tex)
        M.box(at(0, -0.04, 0.34), (0.3 * s, 0.1 * s, 0.05 * s), 0.02, DARK, 0.0)
        eyes = ((0.14, -0.04, 0.42),)
        face["eye"] = "slit"
        mouth = None
    elif kind == "humanoid":
        M.ell(c, (0.3 * s, 0.34 * s, 0.3 * s), mat, 0.12, tex=tex)
        M.ell(at(0, -0.22, 0.12), (0.18 * s, 0.16 * s, 0.16 * s), mat, 0.08, tex=tex)
        eyes = ((0.13, 0.04, 0.28),)
        mouth = ((0.08, -0.2, 0.26),)
    elif kind == "blob":
        M.ell(c, (0.46 * s, 0.4 * s, 0.4 * s), mat, 0.15, tex=tex)
        eyes = ((0.2, 0.08, 0.36),)
        mouth = ((0.2, -0.16, 0.36),)
    else:
        raise ValueError(kind)
    if eyes:
        ex, ey, ez = eyes[0]
        M.anchor("eye_l", at(ex, ey, ez))
        M.anchor("eye_r", at(-ex, ey, ez))
        face["eyes"] = ["eye_l", "eye_r"]
    if mouth:
        mx, my, mz = mouth[0]
        M.anchor("mouth_a", at(-mx, my, mz))
        M.anchor("mouth_b", at(mx, my, mz))
        face["mouth"] = ["mouth_a", "mouth_b"]
    # ears
    if ears == "point":
        M.cone(at(0.2, 0.22, 0.0), at(0.34, 0.62, -0.12), 0.1 * s, 0.015 * s, mat, 0.05, True, tex=tex)
    elif ears == "long":
        M.cone(at(0.14, 0.24, -0.05), at(0.3, 0.85, -0.3), 0.09 * s, 0.05 * s, mat, 0.05, True, tex=tex)
    elif ears == "round":
        M.ell(at(0.3, 0.26, -0.05), (0.14 * s, 0.14 * s, 0.05 * s), mat, 0.05, True, tex=tex)
    elif ears == "bat":
        M.tri(at(0.15, 0.2, 0.0), at(0.5, 0.75, -0.2), at(0.4, 0.1, -0.1), 0.03, accent, 0.0, True)
    elif ears == "fin":
        M.tri(at(0.28, 0.0, -0.05), at(0.62, 0.3, -0.3), at(0.4, -0.25, -0.1), 0.03, accent, 0.0, True)
    if horns_:
        kind_h, size = horns_
        if kind_h == "curved":
            horn(M, at(0.2, 0.26, 0.05), at(0.34, 0.78 * size, -0.28 * size), 0.1 * s, (0.1, 0.0, 0.0), BONE)
        elif kind_h == "straight":
            horn(M, at(0.14, 0.3, 0.08), at(0.2, 0.8 * size, 0.05), 0.1 * s, (0, 0, 0), BONE)
        elif kind_h == "bull":
            horn(M, at(0.3, 0.2, 0.0), at(0.62 * size, 0.7 * size, 0.2 * size), 0.1 * s, (0.3, -0.1, 0.0), BONE)
        elif kind_h == "back":
            horn(M, at(0.18, 0.26, -0.1), at(0.3, 0.45 * size, -0.8 * size), 0.1 * s, (0.0, 0.25, 0.0), BONE)
        elif kind_h == "crown":
            for i in range(5):
                a = (i - 2) * 0.4
                M.spike(at(math.sin(a) * 0.3, 0.3, -0.05 + math.cos(a) * 0.12), at(math.sin(a) * 0.4, 0.3 + 0.38 * size, -0.05), 0.07 * s, BONE, 0.02)
        elif kind_h == "antlers":
            antlers(M, at(0.14, 0.28, -0.05), size * s)
    return face
