"""A tiny signed-distance-field renderer for the Hardcore Crystal creature sprites.

A Model is a list of primitives (ellipsoid, round cone, rounded box, thin triangle) with a material id each, blended with a smooth minimum so
bodies, limbs and horns grow into each other like clay.  Pairs of limbs, horns and so on are written once and mirrored in x.
Model space: y up, the creature faces +z (toward the viewer at yaw 0), its right hand is at -x.  Units are roughly "metres": a person is 1.8 high.

render() ray-marches the model from a camera and returns per-pixel buffers (hit, depth, normal, material) at a supersampled resolution; toon.py
turns those into four-colour pixel art.  Everything is numpy-vectorised.
"""
import math

import numpy as np

# material ids
BODY, ACCENT, DARK, EYE, BONE = 0, 1, 2, 3, 4


def _len(v):
    return np.sqrt((v * v).sum(-1))


def _dot2(v):
    return (v * v).sum(-1)


def rotation(rx=0.0, ry=0.0, rz=0.0):
    """Rotation matrix from euler angles in degrees (applied x, then y, then z)."""
    ax, ay, az = (math.radians(a) for a in (rx, ry, rz))
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    mx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    my = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    mz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return mz @ my @ mx


def smin(a, b, k):
    if k <= 1e-6:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1 - h) + a * h - k * h * (1 - h)


class Prim:
    __slots__ = ("kind", "a", "b", "r", "mat", "k", "rot", "extra", "name", "tex")

    def __init__(self, kind, a, b, r, mat, k, rot=None, extra=None, name="", tex=-1):
        self.kind, self.mat, self.k, self.rot, self.extra, self.name, self.tex = kind, mat, k, rot, extra, name, tex
        self.a = np.asarray(a, float)
        self.b = None if b is None else np.asarray(b, float)
        self.r = r


_MX = np.diag([-1.0, 1.0, 1.0])


class Model:
    """A list of primitives.  Inside `with M.frame(origin, rot):` all coordinates are local to that frame (rot = euler degrees or a 3x3 matrix).
    mirror=True adds the mirror image through the local plane x = 0."""

    def __init__(self):
        self.prims = []
        self.R = np.eye(3)
        self.o = np.zeros(3)
        self.stack = []
        self.texs = []
        self.anchors = {}
        self.face = None

    # ---- frames
    def frame(self, origin=(0, 0, 0), rot=None):
        return _Frame(self, origin, rot)

    def tp(self, p):
        return self.o + self.R @ np.asarray(p, float)

    def anchor(self, name, p):
        """Remember a point (local coordinates) under a name; used by the face decals and by plans that attach things."""
        self.anchors[name] = self.tp(p)

    def texture(self, *spec):
        if spec not in self.texs:
            self.texs.append(spec)
        return self.texs.index(spec)

    # ---- primitive constructors
    def _add(self, kind, a, b, r, mat, k, mirror, rot=None, extra=None, name="", tex=None):
        tid = -1 if tex is None else self.texture(*tex)
        for m in ((False, True) if mirror else (False,)):
            def P(p, m=m):
                p = np.asarray(p, float)
                if m:
                    p = _MX @ p
                return self.tp(p)
            rr = None
            if kind in ("ell", "box"):
                local = np.eye(3) if rot is None else (rot if isinstance(rot, np.ndarray) else rotation(*rot))
                if m:
                    local = _MX @ local @ _MX
                rr = self.R @ local
                if rot is None and not m and np.allclose(rr, np.eye(3)):
                    rr = None
            self.prims.append(Prim(kind, P(a), None if b is None else P(b), r, mat, k, rr, None if extra is None else P(extra), name, tid))
        return self

    def ell(self, c, r, mat=BODY, k=0.12, mirror=False, rot=None, name="", tex=None):
        """Ellipsoid centred at c with radii r (scalar or 3)."""
        r = np.broadcast_to(np.asarray(r, float), (3,)).copy()
        return self._add("ell", c, None, r, mat, k, mirror, rot, name=name, tex=tex)

    def cone(self, a, b, ra, rb, mat=BODY, k=0.1, mirror=False, name="", tex=None):
        """Round cone (capsule with two radii) from a to b."""
        return self._add("cone", a, b, (float(ra), float(rb)), mat, k, mirror, name=name, tex=tex)

    def box(self, c, half, rnd=0.02, mat=BODY, k=0.05, mirror=False, rot=None, name="", tex=None):
        half = np.broadcast_to(np.asarray(half, float), (3,)).copy()
        return self._add("box", c, None, (half, rnd), mat, k, mirror, rot, name=name, tex=tex)

    def tri(self, a, b, c, thick=0.03, mat=ACCENT, k=0.0, mirror=False, name="", tex=None):
        """Thin triangular plate (wing membrane, fin, blade)."""
        return self._add("tri", a, b, thick, mat, k, mirror, extra=c, name=name, tex=tex)

    def tube(self, pts, r0, r1, mat=BODY, k=0.1, mirror=False, steps=None, name="", tex=None, rfn=None):
        """Tapered tube along the Catmull-Rom spline through pts; radius r0 at the start to r1 at the end (or rfn(s) -> radius)."""
        n = steps or max(3, 2 * (len(pts) - 1))
        pp = [spline3(pts, i / n) for i in range(n + 1)]
        rad = rfn or (lambda s: r0 + (r1 - r0) * s)
        for i in range(n):
            self.cone(pp[i], pp[i + 1], rad(i / n), rad((i + 1) / n), mat, k, mirror, name=name, tex=tex)
        return self

    def spike(self, base, tip, r, mat=BONE, k=0.03, mirror=False, name="", tex=None):
        return self.cone(base, tip, r, max(r * 0.08, 0.004), mat, k, mirror, name=name, tex=tex)

    # ---- evaluation
    def bounds(self):
        lo = np.array([1e9] * 3)
        hi = np.array([-1e9] * 3)
        for p in self.prims:
            pts = [p.a]
            if p.b is not None:
                pts.append(p.b)
            if p.extra is not None:
                pts.append(p.extra)
            if p.kind == "ell":
                m = float(p.r.max())
            elif p.kind == "cone":
                m = max(p.r)
            elif p.kind == "box":
                m = float(np.linalg.norm(p.r[0])) + p.r[1]
            else:
                m = p.r
            for q in pts:
                lo = np.minimum(lo, q - m)
                hi = np.maximum(hi, q + m)
        return lo, hi

    def dist(self, P, want_id=True):
        """Scene distance and (optionally) the index of the nearest primitive at points P (N, 3)."""
        d = None
        raw = None
        pid = None
        for i, p in enumerate(self.prims):
            di = prim_dist(p, P)
            if d is None:
                d = di
                raw = di.copy()
                pid = np.zeros(len(P), np.int16) if want_id else None
            else:
                if want_id:
                    pid = np.where(di < raw, np.int16(i), pid)
                raw = np.minimum(raw, di)
                d = smin(d, di, p.k)
        return d, pid


class _Frame:
    def __init__(self, m, origin, rot):
        self.m, self.origin = m, np.asarray(origin, float)
        self.rot = np.eye(3) if rot is None else (rot if isinstance(rot, np.ndarray) else rotation(*rot))

    def __enter__(self):
        m = self.m
        m.stack.append((m.R, m.o))
        m.o = m.o + m.R @ self.origin
        m.R = m.R @ self.rot
        return m

    def __exit__(self, *a):
        self.m.R, self.m.o = self.m.stack.pop()


def spline3(pts, s):
    """Catmull-Rom through 3D points, s in 0..1."""
    pts = [np.asarray(p, float) for p in pts]
    n = len(pts) - 1
    t = min(max(s, 0.0), 0.99999) * n
    i = int(t)
    u = t - i
    p0 = pts[max(i - 1, 0)]
    p1 = pts[i]
    p2 = pts[min(i + 1, n)]
    p3 = pts[min(i + 2, n)]
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)


def prim_dist(p, P):
    if p.kind == "ell":
        q = P - p.a
        if p.rot is not None:
            q = q @ p.rot  # rotate points into the primitive's frame
        k0 = _len(q / p.r)
        k1 = _len(q / (p.r * p.r))
        return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)
    if p.kind == "cone":
        return round_cone(P, p.a, p.b, p.r[0], p.r[1])
    if p.kind == "box":
        q = P - p.a
        if p.rot is not None:
            q = q @ p.rot
        half, rnd = p.r
        qq = np.abs(q) - half
        return _len(np.maximum(qq, 0.0)) + np.minimum(np.maximum(qq[:, 0], np.maximum(qq[:, 1], qq[:, 2])), 0.0) - rnd
    if p.kind == "tri":
        return np.sqrt(ud_triangle2(P, p.a, p.b, p.extra)) - p.r
    raise ValueError(p.kind)


def round_cone(P, a, b, r1, r2):
    ba = b - a
    l2 = float(ba @ ba)
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pa = P - a
    y = pa @ ba
    z = y - l2
    x2 = _dot2(pa * l2 - np.outer(y, ba))
    y2 = y * y * l2
    z2 = z * z * l2
    k = math.copysign(1.0, rr) * rr * rr * x2
    c1 = np.sign(z) * a2 * z2 > k
    c2 = np.sign(y) * a2 * y2 < k
    d1 = np.sqrt(x2 + z2) * il2 - r2
    d2 = np.sqrt(x2 + y2) * il2 - r1
    d3 = (np.sqrt(x2 * a2 * il2) + y * rr) * il2 - r1
    return np.where(c1, d1, np.where(c2, d2, d3))


def ud_triangle2(P, a, b, c):
    """Squared unsigned distance to the triangle abc."""
    ba, cb, ac = b - a, c - b, a - c
    pa, pb, pc = P - a, P - b, P - c
    nor = np.cross(ba, ac)
    s = (np.sign(np.cross(ba, nor) @ pa.T) + np.sign(np.cross(cb, nor) @ pb.T) + np.sign(np.cross(ac, nor) @ pc.T))
    e1 = _dot2(ba * np.clip((pa @ ba) / (ba @ ba), 0, 1)[:, None] - pa)
    e2 = _dot2(cb * np.clip((pb @ cb) / (cb @ cb), 0, 1)[:, None] - pb)
    e3 = _dot2(ac * np.clip((pc @ ac) / (ac @ ac), 0, 1)[:, None] - pc)
    edge = np.minimum(np.minimum(e1, e2), e3)
    face = (pa @ nor) ** 2 / (nor @ nor)
    return np.where(s < 2.0, edge, face)


# ------------------------------------------------------------------------------------------------ camera and marching
class Camera:
    """yaw/pitch in degrees around the target; fov in degrees (0 = orthographic); half = half height of the view at the target."""

    def __init__(self, target=(0, 0.9, 0), yaw=25.0, pitch=8.0, dist=9.0, fov=14.0, half=1.4, shift=(0.0, 0.0)):
        self.target = np.asarray(target, float)
        self.yaw, self.pitch, self.dist, self.fov, self.half = yaw, pitch, dist, fov, half
        self.shift = shift
        ya, pa = math.radians(yaw), math.radians(pitch)
        self.pos = self.target + dist * np.array([math.sin(ya) * math.cos(pa), math.sin(pa), math.cos(ya) * math.cos(pa)])
        f = self.target - self.pos
        self.fwd = f / np.linalg.norm(f)
        r = np.cross(self.fwd, np.array([0.0, 1.0, 0.0]))
        self.right = r / np.linalg.norm(r)
        self.up = np.cross(self.right, self.fwd)

    def rays(self, n, ss, view=None):
        """Rays through an n x n pixel grid with ss x ss samples per pixel.  view = (cx, cy, half) in screen units overrides the framing."""
        cx, cy, half = view if view else (self.shift[0], self.shift[1], self.half)
        m = n * ss
        t = (np.arange(m) + 0.5) / m * 2 - 1  # -1..1, left to right / top to bottom
        u, v = np.meshgrid(t * half + cx, -(t * half) + cy)  # v up
        u, v = u.ravel(), v.ravel()
        if self.fov <= 0:
            origin = self.pos[None, :] + u[:, None] * self.right[None, :] + v[:, None] * self.up[None, :]
            dirs = np.broadcast_to(self.fwd, origin.shape).copy()
        else:
            # perspective: the screen plane at the target distance is [-half, half]; the focal length follows from half and fov
            f = half / math.tan(math.radians(self.fov) / 2) if False else self.dist
            origin = np.broadcast_to(self.pos, (len(u), 3)).copy()
            dirs = self.fwd[None, :] * f + u[:, None] * self.right[None, :] + v[:, None] * self.up[None, :]
            dirs /= np.linalg.norm(dirs, axis=1)[:, None]
        return origin, dirs, m


def render(model, cam, n=56, ss=3, view=None, max_steps=70):
    """Ray-march. Returns dict of arrays of shape (m, m[, 3]) with m = n * ss: hit (bool), depth, normal (camera space xyz), mat (int8)."""
    origin, dirs, m = cam.rays(n, ss, view)
    lo, hi = model.bounds()
    cen = (lo + hi) / 2
    rad = float(np.linalg.norm(hi - lo) / 2) + 0.05
    # ray / bounding sphere
    oc = origin - cen
    b = (oc * dirs).sum(1)
    c = (oc * oc).sum(1) - rad * rad
    disc = b * b - c
    cand = disc > 0
    t0 = np.where(cand, -b - np.sqrt(np.maximum(disc, 0)), 0)
    t1 = np.where(cand, -b + np.sqrt(np.maximum(disc, 0)), 0)
    t = np.maximum(t0, 0.0)
    N = len(origin)
    hit = np.zeros(N, bool)
    tt = np.zeros(N)
    active = np.where(cand)[0]
    t = t[active]
    tmax = t1[active]
    for _ in range(max_steps):
        if len(active) == 0:
            break
        P = origin[active] + dirs[active] * t[:, None]
        d, _m = model.dist(P, want_id=False)
        done_hit = d < 0.004
        done_miss = t > tmax
        if done_hit.any():
            idx = active[done_hit]
            hit[idx] = True
            tt[idx] = t[done_hit]
        keep = ~(done_hit | done_miss)
        active = active[keep]
        t = t[keep] + np.maximum(d[keep] * 0.9, 0.002)
        tmax = tmax[keep]
    depth = np.where(hit, tt, np.inf)
    hid = np.where(hit)[0]
    normal = np.zeros((N, 3))
    pid = np.full(N, -1, np.int16)
    pos = np.zeros((N, 3))
    if len(hid):
        P = origin[hid] + dirs[hid] * tt[hid][:, None]
        e = 0.01
        grads = []
        for ax in range(3):
            off = np.zeros(3)
            off[ax] = e
            dp, _ = model.dist(P + off, want_id=False)
            dm, _ = model.dist(P - off, want_id=False)
            grads.append(dp - dm)
        nrm = np.stack(grads, 1)
        nrm /= np.maximum(np.linalg.norm(nrm, axis=1), 1e-9)[:, None]
        # camera space: x right, y up, z toward the viewer
        cs = np.stack([nrm @ cam.right, nrm @ cam.up, -(nrm @ cam.fwd)], 1)
        normal[hid] = cs
        _d, mm = model.dist(P, want_id=True)
        pid[hid] = mm
        pos[hid] = P
    return dict(hit=hit.reshape(m, m), depth=depth.reshape(m, m), normal=normal.reshape(m, m, 3), pid=pid.reshape(m, m), pos=pos.reshape(m, m, 3), m=m, ss=ss, n=n)


def project(cam, pts, n=56, view=None):
    """Model-space points -> (x, y) in final pixel coordinates (float) for the same framing as render()."""
    cx, cy, half = view if view else (cam.shift[0], cam.shift[1], cam.half)
    out = []
    for p in pts:
        v = np.asarray(p, float) - cam.pos
        zc = v @ cam.fwd
        if cam.fov <= 0:
            u, w = v @ cam.right, v @ cam.up
        else:
            u, w = (v @ cam.right) * cam.dist / zc, (v @ cam.up) * cam.dist / zc
        x = ((u - cx) / half + 1) / 2 * n
        y = (1 - (w - cy) / half) / 2 * n
        out.append((float(x), float(y)))
    return out
