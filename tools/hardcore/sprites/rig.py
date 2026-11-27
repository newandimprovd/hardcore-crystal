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
        eye(img, xi, yi, face.get("eye", "angry"), face.get("eye_size", sz), side, glow, face.get("eye_col", 0))
        if i == 0 and face.get("scar"):
            scar(img, xi, yi, side)
    m = face.get("mouth")
    if m:
        (x0, y0), (x1, y1) = sdf.project(cam, [A[m[0]], A[m[1]]], n, view)
        mouth(img, int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)), face.get("teeth", 3), pose.get("jaw", 0), sz)


def eye(img, x, y, kind, sz, side, glow, col=0):
    """Eye centred on pixel (x, y).  side: +1 for an eye on the left of the face (the brow slopes down toward the right), -1 otherwise.
    col is the palette index of the glow (0 white, 2 the second colour).  Every moody eye is an outlined white eye with a black pupil, four pixels
    wide (five when sz is 1.3 or more), so the face reads at the size of the picture."""
    big = sz >= 1.3
    w = 5 if big else 4
    x0 = x - w // 2
    near = (lambda i: i) if side > 0 else (lambda i: w - 1 - i)  # w - 1 is the end of the eye nearest the nose, 0 the outer end
    at_near = lambda k: (w - 1 - k) if side > 0 else k  # noqa: E731  column of the k-th pixel counted back from the nose end

    def px(i, r, c):
        _put(img, x0 + i, y - 1 + r, c)

    if kind == "angry":
        h = 4 if big else 3
        for i in range(w):
            drop = 1 if near(i) >= w // 2 else 0  # the brow runs down toward the nose
            if drop:
                px(i, 0, 3)
            px(i, drop, 3)
            for r in range(drop + 1, h - 1):
                px(i, r, col)
            px(i, h - 1, 3)
        px(at_near(0), h - 2, 3)  # the pupil in the end by the nose: the glare
        px(at_near(1), h - 2, 3)
    elif kind == "sly":
        for i in range(w):
            lid = 0 if near(i) < w // 2 else 1  # the lid climbs toward the outer end: the smug squint
            px(i, lid, 3)
            px(i, lid + 1, col)
            px(i, 2, 3)
        px(at_near(1), 1, 3)
    elif kind == "tired":
        for i in range(w):
            px(i, 0, 3)
            px(i, 1, col)
            px(i, 2, 3 if i % 2 == 0 else col)  # the bag under the eye
        px(w // 2, 1, 3)
        px(w // 2 - 1, 1, 3)
    elif kind == "round":
        h = w
        for i in range(1, w - 1):
            px(i, 0, 3)
            px(i, h - 1, 3)
        for r in range(1, h - 1):
            px(0, r, 3)
            px(w - 1, r, 3)
            for i in range(1, w - 1):
                px(i, r, col)
        px(w // 2, h // 2, 3)  # the pin prick pupil
    elif kind == "addled":
        for i in range(w):
            px(i, 0, 3)
            px(i, 1, col)
            px(i, 2, col)
            px(i, 3, 3)
        px(at_near(0), 2, 3)  # both pupils pushed in toward the nose
        px(at_near(0), 1, 3)
        px(at_near(1), 2, 3)
    elif kind == "blank":
        for i in range(w):
            px(i, 0, 3)
            px(i, 1, col)
            px(i, 2, col)
            px(i, 3, 3)
        for i in range(w):
            px(i, 1, 3 if glow else col)
    elif kind == "hollow":
        for dx in (-1, 0, 1):
            for dy in (0, 1):
                _put(img, x + dx, y + dy, 3)
        _put(img, x, y, col if glow else 3)
    elif kind == "dot":
        for i in range(2):
            px(i + 1, 1, 3)
            px(i + 1, 2, 3)
    elif kind == "slit":
        for i in range(w):
            px(i, 1, col)
        for i in range(1, w - 1):
            px(i, 0, 3)
            px(i, 2, 3)
        px(w // 2, 1, 3)


def scar(img, x, y, side):
    """A white scar slanting across the brow above and below the eye (only on body coloured pixels, so it never eats the eye)."""
    d = 1 if side > 0 else -1
    for k, (dx, dy) in enumerate(((-1, -3), (0, -2), (1, -1), (1, 0), (2, 1), (2, 2))):
        px_, py_ = x + d * dx, y + dy
        if 0 <= py_ < img.shape[0] and 0 <= px_ < img.shape[1] and img[py_, px_] in (1, 2) and k not in (3,):
            img[py_, px_] = 0


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
