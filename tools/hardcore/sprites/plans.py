"""Body plans for the SDF creatures.  A plan is a function plan(M, pose, p) that builds a creature into Model M from the parameter dict p
and the pose dict (animation: jaw, glow, head_dy, arm, tail, breath).  Plans return nothing; they set M.face and register anchors.

Common parameters (all plans):  tex  texture tuple for the body, mat/accent  palette roles are fixed (BODY, ACCENT), hook  a function
hook(M, pose, A) called at the end with the anchor dict, for the extras that make one species itself.
"""
import math

import numpy as np

import parts
from parts import V
from sdf import ACCENT, BODY, BONE, DARK, EYE, Model


def _pose(pose, key, default=0.0):
    return pose.get(key, default)


# ============================================================================================ biped
def biped(M, pose, p):
    d = dict(leg=0.95, thigh_r=0.26, shin_r=0.19, hip_w=0.32, bulk=1.0, torso_h=0.62, hunch=10.0, shoulder_w=0.66, arm_r=0.19,
             arm_len=1.0, arms=1, hand="fist", hand_size=1.0, foot="plant", foot_size=1.0, head="beast", head_s=1.15, head_kw={}, neck=0.2,
             tail={"kind": "plain", "length": 1.3, "thick": 0.26}, back=None, belly=True, tex=None, pelvis=1.0, hook=None, legs_kind="plain",
             arm_spread=0.0, shoulder_ball=True)
    d.update(p)
    tex = d["tex"]
    L = d["leg"]
    bulk = d["bulk"]
    th = d["torso_h"]
    sw = d["shoulder_w"]
    breath = _pose(pose, "breath")
    A = {}
    # ---- legs
    hw = d["hip_w"]
    if d["legs_kind"] != "none":
        M.cone((hw, L, 0), (hw * 1.15, L * 0.52, 0.12), d["thigh_r"], d["thigh_r"] * 0.76, BODY, 0.12, True, tex=tex)
        M.cone((hw * 1.15, L * 0.52, 0.12), (hw * 1.1, 0.14, 0.02), d["thigh_r"] * 0.76, d["shin_r"] * 0.85, BODY, 0.1, True, tex=tex)
        parts.foot(M, (hw * 1.1, 0.1, 0.0), d["foot"], d["foot_size"], True)
    M.ell((0, L + 0.04, 0), (hw * 1.25 * d["pelvis"], 0.28, 0.32), BODY, 0.2, tex=tex)
    # ---- torso, arms, head in the hunched frame
    with M.frame((0, L + 0.1, 0), (d["hunch"], 0, 0)):
        M.ell((0, 0.52 * th + breath * 0.03, 0.04), (0.58 * bulk * sw / 0.66, 0.62 * th + 0.02 * breath, 0.44 * bulk), BODY, 0.25, tex=tex)
        if d["belly"]:
            M.ell((0, 0.45 * th, 0.31 * bulk), (0.32 * bulk, 0.4 * th, 0.15 * bulk), ACCENT, 0.05)
        sx, sy = sw * bulk, 0.98 * th
        if d["shoulder_ball"]:
            M.ell((sx, sy, 0.0), (0.3 * bulk, 0.27 * bulk, 0.28 * bulk), BODY, 0.15, True, tex=tex)
        raise_ = _pose(pose, "arm")
        for pair in range(d["arms"]):
            oy = -pair * 0.42 * th
            ox = pair * 0.06 * bulk
            ar = d["arm_r"] * (1.0 - 0.1 * pair)
            ln = d["arm_len"] * (1.0 - 0.15 * pair)
            sh = V(sx + ox, sy + oy, 0.0)
            el = sh + V(0.16 + d["arm_spread"], -0.52 * ln + raise_ * 0.15, 0.08 + raise_ * 0.3)
            wr = el + V(0.02 + d["arm_spread"] * 0.4, -0.42 * ln + raise_ * 0.2, 0.32 + raise_ * 0.42)
            M.cone(sh, el, ar * 1.1, ar * 0.9, BODY, 0.1, True, tex=tex)
            M.cone(el, wr, ar * 0.95, ar * 1.12, BODY, 0.1, True, tex=tex)
            parts.hand(M, wr, d["hand"], d["hand_size"] * (1.0 - 0.12 * pair), True)
            if pair == 0:
                A["hand"] = wr
        # neck and head
        hc = V(0, th + 0.42 + d["neck"] + _pose(pose, "head_dy") * 0.5, 0.26 + _pose(pose, "head_dz") * 0.4)
        M.cone((0, th * 0.85, 0.05), hc - V(0, 0.1, 0.0), 0.28 * bulk, 0.24 * d["head_s"], BODY, 0.15, tex=tex)
        face = parts.head(M, d["head"], hc, d["head_s"], jaw=_pose(pose, "jaw"), tex=tex, **d["head_kw"])
        A["head"] = hc
        # back decorations
        back = d["back"]
        if back:
            kind = back[0]
            if kind == "spikes":
                n, size = back[1], back[2]
                pts = [(0, th * (1.0 - 0.55 * i / max(n - 1, 1)), -0.36 * bulk - 0.05 * i) for i in range(n)]
                parts.row_spikes(M, pts, size, 0.11 * bulk, (0, 1.0, -0.8), BONE, 0.3)
            elif kind == "plates":
                n, size = back[1], back[2]
                for i in range(n):
                    y = th * (1.0 - 0.6 * i / max(n - 1, 1))
                    M.ell((0, y, -0.38 * bulk), (0.1 * size, 0.2 * size, 0.4 * size), BONE, 0.04)
            elif kind == "shell":
                M.ell((0, 0.5 * th, -0.32 * bulk), (0.62 * bulk, 0.64 * th, 0.36 * bulk), ACCENT, 0.15, tex=back[1] if len(back) > 1 else None)
    # ---- tail
    t = d["tail"]
    if t:
        tt = dict(t)
        kind = tt.pop("kind", "plain")
        tt["sway"] = tt.get("sway", 0.0) + _pose(pose, "tail")
        parts.tail(M, (0, L + 0.05, -0.2), kind, tex=tex, **tt)
    M.face = face
    if d["hook"]:
        d["hook"](M, pose, A)
    M.A = A


PLANS = {"biped": biped}
