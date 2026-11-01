"""Rendering rig: model builder + pose + view -> four-colour pixel image, with face decals.

A builder is a function (pose: dict) -> Model whose `anchors` dict (name -> xyz) and `face` dict (eyes, mouth) describe where the decals go.
The framing is fitted once on the base pose and reused for every pose of the same view, so tiles that do not move stay identical
(the pic animation shares unchanged tiles).
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sdf  # noqa: E402
import toon  # noqa: E402
from sdf import Camera  # noqa: E402

VIEWS = {
    "front": dict(yaw=24.0, pitch=-4.0, dist=6.5, n=56),
    "back": dict(yaw=-152.0, pitch=-3.0, dist=6.5, n=48),
}


class Rig:
    def __init__(self, builder, target=(0, 1.1, 0.0), fill=0.97, views=None, ss=4, style=None, yaw=None, anchor_bottom=True, pitch=None, dist=None):
        self.builder = builder
        self.target = target
        self.fill = fill
        self.ss = ss
        self.style = style
        self.views = {k: dict(v) for k, v in (views or VIEWS).items()}
        if yaw:
            for k, v in yaw.items():
                self.views[k]["yaw"] = v
        for k in self.views:
            if pitch is not None:
                self.views[k]["pitch"] = pitch
            if dist is not None:
                self.views[k]["dist"] = dist
        self.cache = {}
        self.anchor_bottom = anchor_bottom

    def camera(self, view):
        v = self.views[view]
        return Camera(target=self.target, yaw=v["yaw"], pitch=v["pitch"], dist=v["dist"], half=2.0)

    def view_for(self, view):
        if view not in self.cache:
            base = self.builder({})
            cam = self.camera(view)
            self.cache[view] = toon.fit_view(base, cam, self.fill, anchor=("bottom" if self.anchor_bottom else "center"))
        return self.cache[view]

    def render(self, view="front", pose=None):
        pose = pose or {}
        v = self.views[view]
        n = v["n"]
        model = self.builder(pose)
        cam = self.camera(view)
        vw = self.view_for(view)
        buf = sdf.render(model, cam, n=n, ss=self.ss, view=vw)
        img = toon.shade(toon.reduce(buf, model), model, style=self.style)
        if view == "front":
            draw_face(img, model, cam, vw, n, pose)
        return img


# ---------------------------------------------------------------------------------------------- face decals
def _put(img, x, y, c):
    if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
        img[y, x] = c


def draw_face(img, model, cam, view, n, pose):
    faces = ([model.face] if getattr(model, "face", None) else []) + list(getattr(model, "faces", []) or [])
    for face in faces:
        _draw_one(img, model, cam, view, n, pose, face)


def _draw_one(img, model, cam, view, n, pose, face):
    A = model.anchors
    fwd = face.get("fwd")
    if fwd is not None:
        to_cam = cam.pos - cam.target
        to_cam = to_cam / np.linalg.norm(to_cam)
        if float(np.dot(fwd, to_cam)) < 0.15:
            return  # this head faces away from the camera
    sz = face.get("size", 1.0)
    glow = pose.get("glow", 0)
    for i, name in enumerate(face.get("eyes", [])):
        (x, y), = sdf.project(cam, [A[name]], n, view)
        xi, yi = int(round(x - 0.5)), int(round(y - 0.5))
        side = -1 if A[name][0] > 0 else 1  # the creature's left eye is at +x; seen from the front it is on the screen's left for yaw ~ 0
        eye(img, xi, yi, face.get("eye", "angry"), sz, side, glow, face.get("eye_col", 0))
    m = face.get("mouth")
    if m:
        (x0, y0), (x1, y1) = sdf.project(cam, [A[m[0]], A[m[1]]], n, view)
        mouth(img, int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)), face.get("teeth", 3), pose.get("jaw", 0), sz)


def eye(img, x, y, kind, sz, side, glow, col=0):
    """Eye centred on pixel (x, y).  side: +1 for an eye on the left of the face (the brow slopes down toward the right), -1 otherwise.
    col is the palette index of the glow (0 white, 2 the second colour)."""
    big = sz >= 1.3
    if kind == "angry":
        w = 4 if big else 3
        rows = 2 if big else 1
        for i in range(w):
            inner = i if side > 0 else w - 1 - i
            by = y - 1 + (1 if inner >= w // 2 else 0)
            cx = x - w // 2 + i
            _put(img, cx, by, 3)
            for k in range(rows):
                _put(img, cx, by + 1 + k, col)
            _put(img, cx, by + 1 + rows, 3)
        pi = (w - 1) if side > 0 else 0
        _put(img, x - w // 2 + pi, y + 1 + (1 if big else 0), 3)
    elif kind == "hollow":
        for dx in (-1, 0, 1):
            for dy in (0, 1):
                _put(img, x + dx, y + dy, 3)
        _put(img, x, y, col if glow else 3)
    elif kind == "round":
        for dx in (0, 1):
            for dy in (0, 1):
                _put(img, x + dx - 1, y + dy, 0)
        _put(img, x + (0 if side > 0 else -1), y + 1, 3)
        for dx in (-2, -1, 0, 1):
            _put(img, x + dx, y - 1, 3)
    elif kind == "dot":
        _put(img, x, y, 3)
        _put(img, x + 1, y, 3)
    elif kind == "slit":
        for i in range(3):
            _put(img, x - 1 + i, y, col)
        _put(img, x, y - 1, 3)
        _put(img, x, y + 1, 3)
        _put(img, x - 1, y, 0 if glow else col)


def mouth(img, x0, y0, x1, y1, teeth, jaw, sz):
    """Black mouth line from (x0, y0) to (x1, y1) with white fangs hanging from it."""
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    pts = []
    for i in range(steps + 1):
        x = round(x0 + (x1 - x0) * i / steps)
        y = round(y0 + (y1 - y0) * i / steps)
        pts.append((x, y))
        _put(img, x, y, 3)
        if jaw:
            _put(img, x, y + 1, 3)
    if teeth and len(pts) > 3:
        for k in range(teeth):
            x, y = pts[int((k + 0.5) * len(pts) / teeth)]
            _put(img, x, y + 1 + (1 if jaw else 0), 0)
            if sz >= 1.3:
                _put(img, x, y + 2 + (1 if jaw else 0), 0)
