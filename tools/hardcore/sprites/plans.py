"""Body plans for the SDF creatures.  A plan is a function plan(M, pose, p) that builds a creature into Model M from the parameter dict p
and the pose dict (animation: jaw, glow, head_dy, arm, tail, breath).  Plans return nothing; they set M.face and register anchors.

Common parameters (all plans):  tex  texture tuple for the body, mat/accent  palette roles are fixed (BODY, ACCENT), hook  a function
hook(M, pose, A) called at the end with the anchor dict, for the extras that make one species itself.
"""
import math
import random

import numpy as np

import orbs
import parts
from parts import V
from sdf import ACCENT, BODY, BONE, DARK, EYE, MEMB, Model


def _pose(pose, key, default=0.0):
    return pose.get(key, default)


# ============================================================================================ biped
UPPER = dict(bulk=1.0, torso_h=0.70, shoulder_w=0.80, arm_r=0.22, arm_len=1.0, arms=1, hand="fist", hand_size=1.2, head="beast", head_s=1.55,
             head_kw={}, neck=0.0, back=None, belly=True, tex=None, spikes=True, wings=None, reach=0.0, arm_spread=0.0, shoulder_ball=True,
             extra_heads=(), hunch=14.0, arm_hands=None)


def upper_body(M, pose, d, A):
    """Torso, arms (any number of pairs), neck, head(s), back decoration and wings, in the current frame (origin at the hips, y up).  Used by
    the biped and by the centaur.  Returns the face dict of the main head."""
    tex = d["tex"]
    bulk = d["bulk"]
    th = d["torso_h"]
    sw = d["shoulder_w"]
    breath = _pose(pose, "breath")
    M.part()
    M.ell((0, 0.2 * th, 0.02), (0.44 * bulk, 0.36 * th, 0.36 * bulk), BODY, 0.2, tex=tex)  # abdomen
    M.ell((0, 0.74 * th + breath * 0.03, 0.06), (0.74 * bulk * sw / 0.8, 0.5 * th + 0.02 * breath, 0.48 * bulk), BODY, 0.12, tex=tex)  # chest
    if d["belly"]:
        M.ell((0, 0.55 * th, 0.38 * bulk), (0.34 * bulk, 0.5 * th, 0.14 * bulk), ACCENT, 0.03)
    sx, sy = sw * bulk * 0.92, 1.06 * th
    raise_ = _pose(pose, "arm")
    n_arms = d["arms"]
    gap = min(0.5, 1.25 / max(n_arms, 1)) * th
    for pair in range(n_arms):
        oy = -pair * gap
        ox = (pair % 2) * 0.1 * bulk - 0.03 * pair * bulk
        zo = 0.0 if n_arms <= 2 else (0.12 if pair % 2 else -0.05)
        ar = d["arm_r"] * (1.0 - (0.08 if n_arms <= 2 else 0.12) * pair) * bulk
        ln = d["arm_len"] * (1.0 - (0.12 if n_arms <= 2 else 0.1) * pair)
        sh = V(sx + ox, sy + oy, zo)
        M.part()
        if d["shoulder_ball"] and pair < 2:
            M.ell(sh + V(0.04, 0.02, 0), (0.3 * bulk, 0.27 * bulk, 0.3 * bulk), BODY, 0.05, True, tex=tex)
            if d["spikes"] and pair == 0:
                M.spike(sh + V(0.1, 0.18, -0.05), sh + V(0.34, 0.62, -0.3), 0.1, BONE, 0.02, True)
        spread = d["arm_spread"] + 0.1 * pair
        if n_arms <= 2:
            el = sh + V(0.26 + spread, -0.5 * ln + raise_ * 0.15, 0.1 + zo + raise_ * 0.3 + d["reach"] * 0.3)
            wr = el + V(0.0 + spread * 0.4, -0.42 * ln + raise_ * 0.2, 0.42 + raise_ * 0.42 + d["reach"] * 0.4 + 0.1 * pair)
        else:
            # a fan of arms: the top pair raised and flexing, the others sweeping down and out
            tt = pair / (n_arms - 1)
            a1 = math.radians(60 - 95 * tt)
            a2 = math.radians(25 - 105 * tt)
            el = sh + V(math.cos(a1), math.sin(a1), 0.0) * (0.62 * ln) + V(0.0, 0.0, 0.12 + 0.1 * tt)
            wr = el + V(math.cos(a2), math.sin(a2), 0.0) * (0.62 * ln) + V(0.0, 0.0, 0.3 + 0.2 * tt)
        M.cone(sh, el, ar * 1.15, ar * 0.95, BODY, 0.05, True, tex=tex)
        M.part()
        M.cone(el, wr, ar * 1.05, ar * 1.2, BODY, 0.04, True, tex=tex)
        if d["spikes"] and pair < 2:
            M.spike(el + V(0.1, 0.0, -0.05), el + V(0.34, 0.1, -0.3), 0.08, BONE, 0.02, True)
        M.part()
        hk = d["hand"] if not d["arm_hands"] else d["arm_hands"][min(pair, len(d["arm_hands"]) - 1)]
        parts.hand(M, wr, hk, d["hand_size"] * (1.0 - 0.1 * pair) * bulk ** 0.5, True)
        if pair == 0:
            A["hand"] = M.tp(wr)
    # neck and head, thrust forward and low between the shoulders
    hc = V(0, th + 0.36 + d["neck"] + _pose(pose, "head_dy") * 0.5, 0.42 + _pose(pose, "head_dz") * 0.4)
    M.part()
    M.cone((0, th * 0.9, 0.05), hc - V(0, 0.1, 0.0), 0.34 * bulk, 0.28 * d["head_s"], BODY, 0.1, tex=tex)
    M.part()
    face = parts.head(M, d["head"], hc, d["head_s"], jaw=_pose(pose, "jaw"), tex=tex, **d["head_kw"])
    A["head"] = M.tp(hc)
    A["back"] = M.tp(V(0, th * 0.9, -0.5 * bulk))
    A["chest"] = M.tp(V(0, th * 0.7, 0.5 * bulk))
    for i, eh in enumerate(d["extra_heads"]):
        eh = dict(eh)
        off = V(*eh.pop("pos", (0.7, 0.2, -0.1)))
        kind = eh.pop("kind", d["head"])
        s_ = eh.pop("s", d["head_s"] * 0.75)
        turn = eh.pop("turn", 0.0)
        c2 = hc + off
        M.part()
        M.tube([(0, th * 0.9, 0.05), (off[0] * 0.6, th * 0.9 + 0.4, 0.2 + off[2] * 0.3), c2 - V(0, 0.1, 0)], 0.3 * bulk, 0.2 * s_, BODY, 0.12, tex=tex)
        M.part()
        with M.frame(c2, (0, turn, 0)):
            M.faces.append(parts.head(M, kind, (0, 0, 0), s_, jaw=_pose(pose, "jaw"), tex=tex, tag=f"x{i}_", **eh))
    back = d["back"]
    if back:
        M.part()
        kind = back[0]
        if kind == "spikes":
            n, size = back[1], back[2]
            pts = [(0, th * (1.25 - 0.8 * i / max(n - 1, 1)), -0.40 * bulk - 0.05 * i) for i in range(n)]
            parts.row_spikes(M, pts, size, 0.12 * bulk, (0, 1.0, -0.8), BONE, 0.3)
        elif kind == "plates":
            n, size = back[1], back[2]
            for i in range(n):
                y = th * (1.2 - 0.8 * i / max(n - 1, 1))
                M.ell((0, y, -0.44 * bulk), (0.1 * size, 0.24 * size, 0.46 * size), BONE, 0.04)
        elif kind == "shell":
            M.ell((0, 0.6 * th, -0.34 * bulk), (0.7 * bulk, 0.74 * th, 0.4 * bulk), ACCENT, 0.15, tex=back[1] if len(back) > 1 else None)
    if d["wings"]:
        M.part()
        w = dict(d["wings"])
        kind = w.pop("kind", "bat")
        at = V(0.2 * bulk, 0.92 * th, -0.28)
        if kind == "bat":
            parts.wing_bat(M, at, flap=_pose(pose, "wing"), **w)
        elif kind == "feather":
            parts.wing_feather(M, at, flap=_pose(pose, "wing"), **w)
    return face


def biped(M, pose, p):
    d = dict(UPPER)
    d.update(leg=0.95, thigh_r=0.30, shin_r=0.22, hip_w=0.36, pelvis=1.0, foot="plant", foot_size=1.2,
             tail={"kind": "plain", "length": 1.4, "thick": 0.3}, hook=None, legs_kind="plain", crouch=0.0)
    d.update(p)
    tex = d["tex"]
    L = d["leg"] - d["crouch"] * 0.25
    bulk = d["bulk"]
    A = {}
    hw = d["hip_w"]
    if d["legs_kind"] != "none":
        M.part()
        knee = V(hw * 1.2, L * 0.5, 0.2 + d["crouch"] * 0.15)
        M.cone((hw, L, 0), knee, d["thigh_r"], d["thigh_r"] * 0.8, BODY, 0.06, True, tex=tex)
        M.part()
        M.cone(knee, (hw * 1.1, 0.16, -0.04), d["thigh_r"] * 0.78, d["shin_r"] * 0.8, BODY, 0.04, True, tex=tex)
        if d["spikes"]:
            M.spike(knee + V(0.0, 0.05, 0.12), knee + V(0.1, 0.12, 0.4), 0.09, BONE, 0.02, True)
        M.part()
        parts.foot(M, (hw * 1.1, 0.12, -0.04), d["foot"], d["foot_size"], True)
    M.part()
    M.ell((0, L + 0.04, 0), (hw * 1.3 * d["pelvis"], 0.3, 0.34), BODY, 0.15, tex=tex)
    with M.frame((0, L + 0.1, 0), (d["hunch"], 0, 0)):
        face = upper_body(M, pose, d, A)
    t = d["tail"]
    if t:
        M.part()
        tt = dict(t)
        kind = tt.pop("kind", "plain")
        tt["sway"] = tt.get("sway", 0.0) + _pose(pose, "tail")
        parts.tail(M, (0, L + 0.05, -0.2), kind, tex=tex, **tt)
    M.face = face
    M.A = A
    if d["hook"]:
        d["hook"](M, pose, A)


# ============================================================================================ quad
def quad(M, pose, p):
    """Four-legged beast.  The body runs along z (chest forward), the head turns toward the camera by head_turn degrees."""
    d = dict(length=1.7, chest=0.62, hip=0.55, h=1.05, leg_r=0.24, neck=0.55, rise=0.5, head="beast", head_s=1.5, head_kw={}, head_turn=25.0,
             tail={"kind": "plain", "length": 1.5, "thick": 0.26}, back=("spikes", 6, 0.45), mane=0.0, tex=None, foot="paw", foot_size=1.2,
             hook=None, spikes=True, wings=None, belly=True, bulk=1.0, hunch=0.0, chest_up=0.0, front_wide=1.0, hind_wide=1.0, mane_kind="spikes",
             upper=None, extra_heads=())
    d.update(p)
    tex = d["tex"]
    h = d["h"]
    ln = d["length"]
    bulk = d["bulk"]
    zc, zh = ln * 0.5, -ln * 0.5
    ch, hp = d["chest"] * bulk, d["hip"] * bulk
    breath = _pose(pose, "breath")
    A = {}
    M.part()
    M.ell((0, h + 0.1 + d["chest_up"], zc), (ch, ch * (0.95 + 0.02 * breath), ch * 0.95), BODY, 0.2, tex=tex)
    M.ell((0, h, zh), (hp, hp * 0.9, hp * 0.95), BODY, 0.2, tex=tex)
    M.cone((0, h + 0.05, zh), (0, h + 0.1 + d["chest_up"], zc), hp * 0.92, ch * 0.92, BODY, 0.25, tex=tex)
    if d["belly"]:
        M.ell((0, h - 0.18, 0.0), (ch * 0.7, ch * 0.45, ln * 0.45), ACCENT, 0.05)
    # legs: front pair straight under the shoulders, hind pair digitigrade
    fx = ch * 0.75 * d["front_wide"]
    M.part()
    sh = V(fx, h + 0.2, zc - 0.05)
    el = V(fx * 1.08, h * 0.5, zc - 0.15)
    pw = V(fx * 1.1, 0.12, zc + 0.02)
    M.cone(sh, el, d["leg_r"] * 1.25, d["leg_r"], BODY, 0.06, True, tex=tex)
    M.cone(el, pw, d["leg_r"], d["leg_r"] * 0.85, BODY, 0.04, True, tex=tex)
    M.part()
    parts.foot(M, pw + V(0, 0, -0.05), d["foot"], d["foot_size"], True)
    hx = hp * 0.8 * d["hind_wide"]
    M.part()
    hip = V(hx, h + 0.1, zh + 0.05)
    knee = V(hx * 1.12, h * 0.55, zh + 0.32)
    hock = V(hx * 1.12, h * 0.26, zh - 0.12)
    pw2 = V(hx * 1.12, 0.12, zh + 0.12)
    M.cone(hip, knee, d["leg_r"] * 1.35, d["leg_r"] * 1.0, BODY, 0.06, True, tex=tex)
    M.cone(knee, hock, d["leg_r"], d["leg_r"] * 0.8, BODY, 0.04, True, tex=tex)
    M.cone(hock, pw2, d["leg_r"] * 0.8, d["leg_r"] * 0.8, BODY, 0.04, True, tex=tex)
    M.part()
    parts.foot(M, pw2 + V(0, 0, -0.02), d["foot"], d["foot_size"], True)
    # neck and head, or the upper body of a centaur
    top = V(0, h + 0.1 + d["chest_up"] + ch * 0.5, zc + 0.1)
    hc = V(0, h + 0.15 + d["chest_up"] + d["rise"] - 0.1 * d["hunch"], zc + d["neck"] + 0.2)
    if d["upper"]:
        u = dict(UPPER)
        u.update(d["upper"])
        M.part()
        with M.frame(V(0, h + 0.1 + d["chest_up"] + ch * 0.3, zc + 0.05), (u["hunch"], 0, 0)):
            face = upper_body(M, pose, u, A)
    else:
        M.part()
        M.tube([top, (top + hc) / 2 + V(0, 0.05, -0.1), hc - V(0, 0.05, 0.1)], ch * 0.62, d["head_s"] * 0.3, BODY, 0.15, tex=tex)
        if d["mane"]:
            mm = d["mane"]
            if d["mane_kind"] == "spikes":
                M.part()
                for i in range(7):
                    u_ = i / 6.0
                    base = top * (1 - u_) + hc * u_ + V(0, 0.12, -0.12 - 0.2 * (1 - u_))
                    parts.row_spikes(M, [base], 0.5 * mm, 0.11, (0.0, 1.0, -0.8 - 0.4 * (1 - u_)), BODY, 0.0, False)
                    M.spike(base + V(0.12, 0.0, 0.0), base + V(0.5 * mm, 0.45 * mm, -0.25 * mm), 0.09, BODY, 0.02, True)
        M.part()
        with M.frame(hc, (0, d["head_turn"], 0)):
            face = parts.head(M, d["head"], (0, 0, 0), d["head_s"], jaw=_pose(pose, "jaw"), tex=tex, **d["head_kw"])
        for i, eh in enumerate(d["extra_heads"]):
            eh = dict(eh)
            off = V(*eh.pop("pos", (0.7, 0.1, -0.1)))
            kind = eh.pop("kind", d["head"])
            s_ = eh.pop("s", d["head_s"] * 0.8)
            turn = eh.pop("turn", d["head_turn"])
            c2 = hc + off
            M.part()
            M.tube([top + V(off[0] * 0.2, 0, 0), (top + c2) / 2 + V(off[0] * 0.4, 0.05, -0.1), c2 - V(0, 0.05, 0.1)], ch * 0.5, s_ * 0.3, BODY, 0.15, tex=tex)
            M.part()
            with M.frame(c2, (0, turn, 0)):
                M.faces.append(parts.head(M, kind, (0, 0, 0), s_, jaw=_pose(pose, "jaw"), tex=tex, tag=f"x{i}_", **eh))
    A["head"] = hc
    A["back"] = V(0, h + 0.15 + ch * 0.9, 0.0)
    A["chest"] = V(0, h + 0.1, zc)
    A["hip"] = V(0, h, zh)
    # back
    back = d["back"]
    if back:
        M.part()
        kind, n, size = back[0], back[1], back[2]
        for i in range(n):
            u = i / max(n - 1, 1)
            z = zc * (1 - u) + zh * u
            y = h + 0.1 + d["chest_up"] * (1 - u) + (ch * 0.9) * (1 - u) + hp * 0.85 * u
            f = 1.0 - 0.3 * abs(u * 2 - 1)
            if kind == "spikes":
                M.spike((0, y - 0.05, z), (0, y + size * f * 1.2, z - size * f * 0.7), 0.13 * f + 0.03, BONE, 0.03)
            elif kind == "plates":
                M.ell((0, y + 0.05, z), (0.08 * size * 2, 0.28 * size * f, 0.2), BONE, 0.04)
    if d["wings"]:
        M.part()
        w = dict(d["wings"])
        kind = w.pop("kind", "bat")
        at = V(0.15, h + ch + d["chest_up"], zc - 0.35)
        (parts.wing_bat if kind == "bat" else parts.wing_feather)(M, at, flap=_pose(pose, "wing"), **w)
    t = d["tail"]
    if t:
        M.part()
        tt = dict(t)
        kind = tt.pop("kind", "plain")
        tt["sway"] = tt.get("sway", 0.0) + _pose(pose, "tail")
        parts.tail(M, (0, h + 0.05, zh - hp * 0.7), kind, tex=tex, **tt)
    M.face = face
    M.A = A
    if d["hook"]:
        d["hook"](M, pose, A)


# ============================================================================================ serpent
def serpent(M, pose, p):
    """A long body along a spline path (tail tip first, head last) with a head, hood, spines, fins and optional arms."""
    d = dict(path=[(1.5, 0.28, -1.0), (1.35, 0.4, 0.0), (0.55, 0.5, 0.55), (-0.5, 0.55, 0.35), (-0.55, 0.6, -0.35), (0.0, 0.85, -0.5), (0.0, 1.5, -0.4),
                   (0.0, 2.1, -0.1), (0.0, 2.3, 0.5), (0.0, 2.15, 1.0)], girth=0.42, taper_tail=0.06, neck_r=0.34, head="dragon", head_s=1.6, head_kw={}, hood=0.0, spines=6,
             spine_size=0.45, fins=None, arms=0, tex=None, belly=True, hook=None, steps=26, head_turn=0.0, head_pitch=0.0, ring_tex=None, wings=None, head_up=0.0, leg_pairs=0, leg_range=(0.12, 0.62), leg_len=0.8, leg_r=0.1, plates=False)
    d.update(p)
    tex = d["tex"]
    pts = [np.array(q, float) for q in d["path"]]
    n = d["steps"]
    A = {}
    g = d["girth"]

    def rad(s):
        # thin tail tip, full middle, a slightly narrower neck, then the head
        base = d["taper_tail"] + (g - d["taper_tail"]) * min(1.0, s * 1.6) ** 0.8
        neck = d["neck_r"] + (g - d["neck_r"]) * (1 - max(0.0, (s - 0.62) / 0.38)) if s > 0.62 else g
        return min(base, neck if s > 0.62 else base) if s > 0.62 else base

    M.part()
    path = [sdf_spline(pts, i / n) for i in range(n + 1)]
    for i in range(n):
        if i % 4 == 0:
            M.part()
        M.cone(path[i], path[i + 1], rad(i / n), rad((i + 1) / n), BODY, 0.1, False, tex=tex if (i % 2 == 0 or d["ring_tex"] is None) else tex)
        if d["belly"] and i / n > 0.12:
            # a pale stripe of belly plates on the side facing the viewer
            prv = path[i]
            M.ell(prv + V(0, -0.0, 0.0) + V(0, 0, 0.0), (0.001, 0.001, 0.001), ACCENT, 0.0)
    head_at = path[-1]
    tan = path[-1] - path[-4]
    tan = tan / np.linalg.norm(tan)
    yaw_h = math.degrees(math.atan2(tan[0], tan[2])) + d["head_turn"]
    pitch_h = math.degrees(math.asin(max(-1.0, min(1.0, -tan[1])))) + d["head_pitch"]
    M.part()
    hc = head_at + V(0, 0.1 + d["head_up"], 0.0) + tan * 0.1
    with M.frame(hc, (pitch_h, yaw_h, 0)):
        face = parts.head(M, d["head"], (0, 0, 0.1), d["head_s"], jaw=_pose(pose, "jaw"), tex=tex, **d["head_kw"])
    A["head"] = hc
    # hood (cobra) as two big plates behind the head
    if d["hood"]:
        M.part()
        hd = d["hood"]
        nk = path[-4]
        M.ell(nk + V(0, 0.05, -0.05), (0.62 * hd, 0.5 * hd, 0.08), ACCENT, 0.08)
        M.ell(nk + V(0, 0.05, -0.1), (0.7 * hd, 0.58 * hd, 0.08), BODY, 0.08)
    # spines along the back
    if d["spines"]:
        M.part()
        for i in range(d["spines"]):
            u = 0.25 + 0.7 * i / max(d["spines"] - 1, 1)
            q = sdf_spline(pts, u)
            r = rad(u)
            f = 0.6 + 0.4 * math.sin(math.pi * (i + 0.5) / d["spines"])
            M.spike(q + V(0, r * 0.7, -r * 0.4), q + V(0, r * 0.7 + d["spine_size"] * f, -r * 0.4 - d["spine_size"] * f * 0.8), 0.1 * f + 0.03, BONE, 0.03)
    if d["leg_pairs"]:
        M.part()
        lo, hi = d["leg_range"]
        for i in range(d["leg_pairs"]):
            u = lo + (hi - lo) * i / max(d["leg_pairs"] - 1, 1)
            q = sdf_spline(pts, u)
            q2 = sdf_spline(pts, min(u + 0.03, 1.0))
            tv = q2 - q
            tv[1] = 0.0
            nrm = np.linalg.norm(tv)
            tv = tv / nrm if nrm > 1e-6 else np.array([0.0, 0.0, 1.0])
            side = np.array([tv[2], 0.0, -tv[0]])
            r = rad(u)
            for sgn in (-1, 1):
                sd = side * sgn
                hip = q + sd * r * 0.7 + V(0, -r * 0.2, 0)
                knee = hip + sd * d["leg_len"] * 0.55 + V(0, d["leg_len"] * 0.25, 0)
                foot = V(knee[0] + sd[0] * d["leg_len"] * 0.45, 0.06, knee[2] + sd[2] * d["leg_len"] * 0.45 + 0.05)
                M.cone(hip, knee, d["leg_r"] * 1.2, d["leg_r"], BODY, 0.03)
                M.cone(knee, foot, d["leg_r"], d["leg_r"] * 0.45, BODY, 0.02)
                M.spike(foot, foot + sd * 0.1 + V(0, 0, 0.18), d["leg_r"] * 0.6, BONE, 0.01)
    if d["plates"]:
        M.part()
        for i in range(2, n - 2, 2):
            u = i / n
            q = sdf_spline(pts, u)
            r = rad(u)
            M.ell(q + V(0, r * 0.8, 0), (r * 0.8, r * 0.34, r * 0.9), BONE, 0.04)
    if d["fins"]:
        M.part()
        for u in d["fins"]:
            q = sdf_spline(pts, u)
            r = rad(u)
            M.tri(q + V(r * 0.5, 0.0, 0.0), q + V(r * 1.8, 0.45, -0.3), q + V(r * 1.4, -0.45, -0.2), 0.04, MEMB, 0.0, True)
    if d["wings"]:
        M.part()
        w = dict(d["wings"])
        kind = w.pop("kind", "bat")
        q = sdf_spline(pts, 0.78)
        (parts.wing_bat if kind == "bat" else parts.wing_feather)(M, q + V(0.1, 0.2, -0.2), flap=_pose(pose, "wing"), **w)
    if d["arms"]:
        M.part()
        q = sdf_spline(pts, 0.82)
        sh = q + V(0.18, 0.1, 0.12)
        el = sh + V(0.3, -0.25, 0.2)
        wr = el + V(0.15, -0.3, 0.25)
        M.cone(sh, el, 0.15, 0.12, BODY, 0.05, True)
        M.cone(el, wr, 0.12, 0.13, BODY, 0.05, True)
        parts.hand(M, wr, "claw", 1.1, True)
    M.face = face
    M.A = A
    if d["hook"]:
        d["hook"](M, pose, A)


def sdf_spline(pts, s):
    import sdf
    return sdf.spline3(pts, s)


# ============================================================================================ insect
def insect(M, pose, p):
    """Winged insect: head, thorax, abdomen (with stinger), six legs and wings.  kind: bee, moth, beetle, mantis."""
    d = dict(kind="bee", abdomen=1.0, thorax=0.55, wings_kind="insect", wing_span=1.7, wing_h=1.2, legs=3, mandibles=True, head_s=1.2, antenna=1.0,
             tex=None, stinger=True, scythe=False, fur=False, hook=None, tilt=18.0, h=0.9, eyes_size=1.0, abd_tex=None, horn=0.0, armor=False)
    d.update(p)
    tex = d["tex"]
    h = d["h"]
    A = {}
    th = d["thorax"]
    flap = _pose(pose, "wing")
    with M.frame((0, h + 0.7, 0), (d["tilt"], 0, 0)):
        M.part()
        M.ell((0, 0, 0), (th * 0.95, th, th * 1.0), BODY, 0.15, tex=tex)
        if d["fur"]:
            for i in range(10):
                a = i * 0.7
                M.spike((math.cos(a) * th * 0.5, math.sin(a) * th * 0.5 + 0.1, th * 0.6), (math.cos(a) * th * 1.05, math.sin(a) * th * 1.05 + 0.1, th * 0.95), 0.12, BODY, 0.04)
        # abdomen hanging behind and below
        M.part()
        ab = d["abdomen"]
        M.ell((0, -0.5 * ab, -0.75 * ab), (0.5 * ab, 0.55 * ab, 0.8 * ab), BODY, 0.12, tex=d["abd_tex"] or tex)
        M.ell((0, -0.78 * ab, -1.3 * ab), (0.3 * ab, 0.32 * ab, 0.5 * ab), BODY, 0.1, tex=d["abd_tex"] or tex)
        if d["stinger"]:
            M.spike((0, -0.85 * ab, -1.7 * ab), (0, -1.15 * ab, -2.2 * ab), 0.14 * ab, BONE, 0.03)
        # head
        M.part()
        hs = d["head_s"]
        hc = V(0, 0.45, 0.62)
        M.ell(hc, (0.42 * hs, 0.38 * hs, 0.36 * hs), BODY, 0.12, tex=tex)
        M.ell(hc + V(0.3 * hs, 0.08 * hs, 0.14 * hs), (0.2 * hs * d["eyes_size"], 0.22 * hs * d["eyes_size"], 0.18 * hs), DARK, 0.03, True)
        if d["mandibles"]:
            M.cone(hc + V(0.1, -0.28 * hs, 0.28 * hs), hc + V(0.02, -0.5 * hs, 0.62 * hs), 0.09 * hs, 0.02, BONE, 0.02, True)
        for sgn in (-1, 1):
            M.tube([hc + V(0.14 * sgn, 0.3 * hs, 0.2), hc + V(0.3 * sgn * d["antenna"], 0.7 * d["antenna"], 0.5), hc + V(0.5 * sgn * d["antenna"], 0.9 * d["antenna"], 0.4)], 0.04, 0.015, BODY, 0.02)
        if d["horn"]:
            M.spike(hc + V(0, 0.28 * hs, 0.2), hc + V(0, 0.28 * hs + d["horn"], 0.7), 0.14, BONE, 0.03)
        M.anchor("eye_l", hc + V(0.32 * hs, 0.08 * hs, 0.28 * hs))
        M.anchor("eye_r", hc + V(-0.32 * hs, 0.08 * hs, 0.28 * hs))
        M.anchor("mouth_a", hc + V(-0.12, -0.2 * hs, 0.34 * hs))
        M.anchor("mouth_b", hc + V(0.12, -0.2 * hs, 0.34 * hs))
        face = dict(eye="slit", eyes=["eye_l", "eye_r"], mouth=None, size=1.0 + 0.3 * (hs > 1.2), eye_col=0)
        # arms: scythes or small claws
        if d["scythe"]:
            M.part()
            sh = V(th * 0.7, 0.1, 0.35)
            el = sh + V(0.35, 0.15, 0.55)
            M.cone(sh, el, 0.14, 0.11, BODY, 0.05, True)
            M.tri(el, el + V(0.1, -0.9, 0.15), el + V(0.1, -0.3, 0.55), 0.05, BONE, 0.0, True)
            M.tri(el, el + V(0.1, -0.9, 0.15), el + V(0.1, -0.3, -0.25), 0.05, BONE, 0.0, True)
        # wings
        M.part()
        sp, wh = d["wing_span"], d["wing_h"]
        if d["wings_kind"] == "insect":
            for (sy, ln, ang) in ((0.3, 1.0, 28), (-0.1, 0.72, 5)):
                a = V(th * 0.45, sy, -0.25)
                L_ = sp * ln
                c = a + V(L_ * 0.5 * math.cos(math.radians(ang + 8 * flap)), L_ * 0.5 * math.sin(math.radians(ang + 8 * flap)), -0.3)
                M.ell(c, (L_ * 0.55, 0.04, wh * 0.26 * ln), MEMB, 0.0, True, rot=(0, 0, ang + 8 * flap))
                M.cone(a, a + (c - a) * 2.0, 0.06, 0.02, BODY, 0.02, True)
        elif d["wings_kind"] == "moth":
            for (sy, ln, dn) in ((0.3, 1.0, 0.6), (-0.1, 0.8, -0.2)):
                a = V(th * 0.4, sy, -0.15)
                M.tri(a, a + V(sp * ln, wh * 0.8 * ln + flap * 0.3, -0.3), a + V(sp * ln * 0.9, wh * 0.05, -0.3), 0.04, MEMB, 0.0, True, tex=tex)
                M.tri(a, a + V(sp * ln * 0.9, wh * 0.05, -0.3), a + V(sp * ln * 0.55, -wh * 0.7 * ln, -0.25), 0.04, MEMB, 0.0, True, tex=tex)
        elif d["wings_kind"] == "elytra":
            M.ell(V(0.0, 0.2, -0.55), (th * 1.05, th * 0.7, 1.0), ACCENT if d["armor"] else BODY, 0.06, tex=tex)
            a = V(th * 0.5, 0.15, -0.3)
            M.tri(a, a + V(sp, wh * 0.4 + flap * 0.3, -0.5), a + V(sp * 0.7, wh * 0.8, -0.5), 0.03, MEMB, 0.0, True)
    # legs
    M.part()
    for i in range(d["legs"]):
        z = 0.35 - i * 0.45
        hip = V(0.3, h + 0.5, z)
        knee = V(0.85 + 0.1 * i, h + 0.95, z + 0.1)
        foot = V(1.0 + 0.2 * i, 0.08, z + 0.35 - 0.15 * i)
        M.cone(hip, knee, 0.1, 0.08, BODY, 0.03, True)
        M.cone(knee, foot, 0.08, 0.04, BODY, 0.02, True)
    M.face = face
    M.A = A
    if d["hook"]:
        d["hook"](M, pose, A)


# ============================================================================================ arthro (spider, crab, scorpion)
def arthro(M, pose, p):
    d = dict(kind="spider", body=0.8, abd=1.0, legs=4, leg_len=1.5, leg_r=0.09, claws=False, claw_size=1.0, head_s=1.0, fangs=True, eyes=6, tex=None,
             shell=0.0, tail=False, hook=None, h=0.8, spikes=True, abd_tex=None, eyestalks=False, abd_up=0.0, web=False)
    d.update(p)
    tex = d["tex"]
    h = d["h"]
    bd = d["body"]
    A = {}
    M.part()
    M.ell((0, h + 0.2, 0.1), (bd * 0.8, bd * 0.5, bd * 0.7), BODY, 0.12, tex=tex)
    if d["kind"] == "spider":
        M.ell((0, h + 0.5 + d["abd_up"], -0.7 * d["abd"]), (0.8 * d["abd"], 0.75 * d["abd"], 0.95 * d["abd"]), BODY, 0.12, tex=d["abd_tex"] or tex)
    elif d["kind"] == "crab":
        M.ell((0, h + 0.3, -0.05), (bd * 1.05, bd * 0.5, bd * 0.8), BODY, 0.1, tex=tex)
        if d["shell"]:
            M.ell((0, h + 0.5, -0.1), (bd * 1.1, bd * 0.45, bd * 0.85), ACCENT, 0.08, tex=tex)
    elif d["kind"] == "scorpion":
        M.ell((0, h + 0.2, -0.6), (bd * 0.7, bd * 0.4, bd * 0.8), BODY, 0.1, tex=tex)
    # head front with eyes and fangs
    M.part()
    hs = d["head_s"]
    hc = V(0, h + 0.3, bd * 0.75)
    M.ell(hc, (0.4 * hs, 0.33 * hs, 0.3 * hs), BODY, 0.1, tex=tex)
    if d["fangs"]:
        M.cone(hc + V(0.16 * hs, -0.18 * hs, 0.2 * hs), hc + V(0.1 * hs, -0.6 * hs, 0.42 * hs), 0.1 * hs, 0.02, BONE, 0.02, True)
    ex = 0.2 * hs
    M.anchor("eye_l", hc + V(ex, 0.1 * hs, 0.28 * hs))
    M.anchor("eye_r", hc + V(-ex, 0.1 * hs, 0.28 * hs))
    M.anchor("mouth_a", hc + V(-0.1 * hs, -0.12 * hs, 0.3 * hs))
    M.anchor("mouth_b", hc + V(0.1 * hs, -0.12 * hs, 0.3 * hs))
    face = dict(eye="angry", eyes=["eye_l", "eye_r"], mouth=None, size=1.0 + 0.3 * (hs > 1.2), eye_col=0)
    # legs
    M.part()
    for i in range(d["legs"]):
        z = bd * 0.55 - i * (bd * 1.0 / max(d["legs"] - 1, 1))
        spread = 0.5 + 0.12 * i
        hip = V(bd * 0.6, h + 0.2, z)
        knee = V(bd * 0.6 + d["leg_len"] * 0.5 * spread, h + 0.2 + d["leg_len"] * 0.55, z + 0.1 * (1.5 - i))
        foot = V(bd * 0.6 + d["leg_len"] * 0.95 * spread, 0.06, z + 0.25 - 0.18 * i)
        M.cone(hip, knee, d["leg_r"] * 1.3, d["leg_r"], BODY, 0.03, True)
        M.cone(knee, foot, d["leg_r"], d["leg_r"] * 0.45, BODY, 0.02, True)
        if d["spikes"]:
            M.spike(knee, knee + V(0.1, 0.25, -0.05), 0.07, BONE, 0.02, True)
    if d["claws"]:
        M.part()
        cs = d["claw_size"]
        up = _pose(pose, "arm")
        sh = V(bd * 0.8, h + 0.3, bd * 0.5)
        el = sh + V(0.5 * cs, 0.35 * cs + up * 0.2, 0.25 * cs)
        wr = el + V(0.2 * cs, 0.4 * cs + up * 0.25, 0.3 * cs)
        M.cone(sh, el, 0.17 * cs, 0.15 * cs, BODY, 0.05, True)
        M.cone(el, wr, 0.15 * cs, 0.2 * cs, BODY, 0.05, True)
        M.ell(wr + V(0.05, 0.05, 0.15 * cs), (0.3 * cs, 0.2 * cs, 0.36 * cs), BODY, 0.06, True, tex=tex)
        M.cone(wr + V(0.0, 0.12 * cs, 0.35 * cs), wr + V(0.15 * cs, 0.4 * cs, 0.8 * cs), 0.15 * cs, 0.02, BONE, 0.02, True)
        M.cone(wr + V(0.0, -0.1 * cs, 0.35 * cs), wr + V(0.15 * cs, -0.1 * cs, 0.78 * cs), 0.13 * cs, 0.02, BONE, 0.02, True)
    if d["tail"]:
        M.part()
        pts = [V(0, h + 0.2, -0.9), V(0, h + 0.3, -1.5), V(0, h + 1.0, -1.7), V(0, h + 1.7, -1.1), V(0, h + 1.9, -0.45)]
        M.tube(pts, 0.28, 0.14, BODY, 0.06, tex=tex)
        M.spike(pts[-1], pts[-1] + V(0, -0.35, 0.55), 0.16, BONE, 0.02)
    M.face = face
    M.A = A
    if d["hook"]:
        d["hook"](M, pose, A)


# ============================================================================================ orb (blobs, ghosts, gas clouds, starfish, machines)
def orb(M, pose, p):
    """A big central mass with a face, surrounded by arms, spikes and satellites.  kind: ghost, blob, cloud, star, core."""
    d = dict(kind="ghost", r=1.0, head="blob", head_s=1.5, tex=None, arms=2, arm_len=1.2, arm_r=0.2, hand="claw", tail_len=1.3, spikes=8, spike_size=0.5,
             satellites=0, sat_r=0.4, hook=None, face_y=0.2, hover=0.5, mouth_big=True, cloud_n=5, eye="angry", face_s=1.0, eye_col=0, drip=0)
    d.update(p)
    tex = d["tex"]
    r = d["r"]
    A = {}
    cy = d["hover"] + r * 1.1
    breath = _pose(pose, "breath")
    M.part()
    face_z = None
    if d["kind"] in orbs.KINDS:
        face_z = orbs.KINDS[d["kind"]](M, d, cy, tex)
    elif d["kind"] in ("ghost", "blob", "core"):
        M.ell((0, cy, 0), (r * 1.1, r * (1.0 + 0.03 * breath), r * 0.95), BODY, 0.2, tex=tex)
        if d["kind"] == "ghost":
            # a tapering ghostly tail below the body
            pts = [(0, cy - r * 0.6, 0), (0.1, cy - r * 1.2, -0.2), (0.4, cy - r * 1.7, -0.5), (0.9, cy - r * 1.9, -0.8)]
            M.tube(pts, r * 0.8, 0.06, BODY, 0.15, tex=tex)
        elif d["kind"] == "blob":
            M.ell((0, d["hover"] + r * 0.35, 0), (r * 1.3, r * 0.45, r * 1.1), BODY, 0.2, tex=tex)
    elif d["kind"] == "cloud":
        for i in range(d["cloud_n"]):
            a = i * 2.4
            M.ell((math.cos(a) * r * 0.9, cy + math.sin(a * 1.7) * r * 0.5, math.sin(a) * r * 0.3), (r * 0.6, r * 0.55, r * 0.55), BODY, 0.2, tex=tex)
        M.ell((0, cy, 0.1), (r, r * 0.9, r * 0.85), BODY, 0.2, tex=tex)
    elif d["kind"] == "star":
        M.ell((0, cy, 0), (r * 0.85, r * 0.85, r * 0.55), BODY, 0.2, tex=tex)
        for i in range(5):
            a = math.radians(90 + 72 * i)
            M.cone((0, cy, 0), (math.cos(a) * r * 1.9, cy + math.sin(a) * r * 1.9, 0.0), r * 0.5, r * 0.08, BODY, 0.15, tex=tex)
    # face on the front
    fc = V(0, cy + d["face_y"] * r, face_z if face_z is not None else r * 0.8)
    if d["mouth_big"]:
        M.part()
    hs = d["face_s"]
    M.anchor("eye_l", fc + V(0.32 * r * hs, 0.12 * r, 0.12 * r))
    M.anchor("eye_r", fc + V(-0.32 * r * hs, 0.12 * r, 0.12 * r))
    M.anchor("mouth_a", fc + V(-0.4 * r * hs, -0.3 * r, 0.1 * r))
    M.anchor("mouth_b", fc + V(0.4 * r * hs, -0.3 * r, 0.1 * r))
    eyes = ["eye_l", "eye_r"]
    for i in range(d.get("extra_eyes", 0)):  # more eyes: a row above the pair
        M.anchor(f"eye_x{i}", fc + V((i - (d["extra_eyes"] - 1) / 2) * 0.3 * r * hs, 0.5 * r, 0.05 * r))
        eyes.append(f"eye_x{i}")
    face = dict(eye=d["eye"], eyes=eyes, mouth=["mouth_a", "mouth_b"] if d["mouth_big"] else None, teeth=5, size=1.4, eye_col=d["eye_col"])
    # arms
    if d["arms"]:
        M.part()
        for pair in range(d["arms"]):
            sh = V(r * 0.95, cy - 0.1 * r - 0.35 * pair, 0.1)
            el = sh + V(0.5, -0.2 + 0.1 * pair, 0.4)
            wr = el + V(0.3, -0.3, 0.55) * d["arm_len"]
            M.cone(sh, el, d["arm_r"], d["arm_r"] * 0.9, BODY, 0.08, True, tex=tex)
            M.cone(el, wr, d["arm_r"] * 0.95, d["arm_r"] * 1.1, BODY, 0.08, True, tex=tex)
            parts.hand(M, wr, d["hand"], 1.3, True)
    if d["spikes"]:
        M.part()
        for i in range(d["spikes"]):
            a = math.radians(40 + 100 * i / max(d["spikes"] - 1, 1))
            b = V(math.cos(a) * r * 0.95, cy + math.sin(a) * r * 0.95, -0.1 * r)
            M.spike(b, b + V(math.cos(a) * d["spike_size"], math.sin(a) * d["spike_size"], -0.2 * d["spike_size"]), 0.13, BONE, 0.03, True)
    for i in range(d["satellites"]):
        a = i * 6.28 / max(d["satellites"], 1) + 0.6
        M.part()
        M.ell((math.cos(a) * r * 1.6, cy + math.sin(a) * r * 0.9, 0.3), (d["sat_r"],) * 3, BODY, 0.1, tex=tex)
    orbs.feature(M, d, cy, tex, random.Random(d.get("seed", 1)))
    M.face = face
    M.A = A
    if d["hook"]:
        d["hook"](M, pose, A)


PLANS = {"biped": biped, "quad": quad, "serpent": serpent, "insect": insect, "arthro": arthro, "orb": orb}
