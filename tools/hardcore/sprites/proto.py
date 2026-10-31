"""Prototype: one brute through the SDF renderer and toon shader (front and back), to judge the look."""
import os
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sdf  # noqa: E402
import toon  # noqa: E402
from sdf import ACCENT, BODY, BONE, EYE, Camera, Model  # noqa: E402


def brute(pose=None, m=1.0):
    pose = pose or {}
    M = Model()
    jaw = pose.get("jaw", 0.0)
    hy = pose.get("head_dy", 0.0)
    M.ell((0, 0.95, 0), (0.40, 0.30, 0.32), k=0.2)
    M.ell((0, 1.50, 0.04), (0.60, 0.58, 0.42), k=0.25)
    M.ell((0, 1.35, 0.30), (0.34, 0.42, 0.16), mat=ACCENT, k=0.05)
    M.cone((0, 1.80, 0.05), (0, 1.98 + hy, 0.28), 0.26, 0.24, k=0.15)
    hc = (0, 2.08 + hy, 0.38)
    M.ell(hc, (0.40, 0.34, 0.38), k=0.15)
    M.ell((0, hc[1] - 0.10, 0.70), (0.25, 0.15, 0.26), k=0.1)
    M.ell((0, hc[1] - 0.24 - jaw * 0.14, 0.64), (0.22, 0.08, 0.24), k=0.05)
    M.cone((0.06, hc[1] + 0.13, 0.64), (0.34, hc[1] + 0.20, 0.44), 0.08, 0.08, mirror=True, k=0.08)
    M.cone((0.2, hc[1] + 0.2, 0.34), (0.46, hc[1] + 0.78, 0.10), 0.11, 0.015, mat=BONE, mirror=True, k=0.04)
    M.ell((0.70, 1.80, 0.0), (0.32, 0.28, 0.30), mirror=True, k=0.15)
    M.cone((0.70, 1.72, 0.0), (0.88, 1.22, 0.10), 0.21, 0.17, mirror=True, k=0.1)
    M.cone((0.88, 1.22, 0.10), (0.90, 0.80, 0.42), 0.17, 0.23, mirror=True, k=0.1)
    M.ell((0.90, 0.72, 0.48), (0.24, 0.22, 0.24), mirror=True, k=0.1)
    for dx in (-0.09, 0.09, 0.18):
        M.spike((0.90 + dx, 0.62, 0.58), (0.90 + dx * 1.3, 0.36, 0.76), 0.055, mirror=True)
    M.cone((0.30, 0.95, 0.0), (0.36, 0.50, 0.12), 0.26, 0.20, mirror=True, k=0.12)
    M.cone((0.36, 0.50, 0.12), (0.34, 0.14, 0.02), 0.20, 0.17, mirror=True, k=0.1)
    M.ell((0.34, 0.08, 0.20), (0.21, 0.10, 0.32), mirror=True, k=0.08)
    for dx in (-0.1, 0.1):
        M.spike((0.34 + dx, 0.07, 0.44), (0.34 + dx, 0.02, 0.66), 0.055, mirror=True)
    M.tube([(0, 0.95, -0.2), (0, 0.65, -0.8), (0.1, 0.35, -1.3), (0.3, 0.55, -1.65)], 0.26, 0.05, k=0.1)
    for i, (y, z) in enumerate(((1.95, -0.32), (1.70, -0.45), (1.42, -0.46), (1.12, -0.36))):
        M.spike((0, y, z), (0, y + 0.46, z - 0.36), 0.12 - 0.01 * i, mat=BONE)
    M.anchors = {"eye_l": (0.19, hc[1] + 0.05, 0.70), "eye_r": (-0.19, hc[1] + 0.05, 0.70),
                 "mouth_a": (-0.22, hc[1] - 0.20, 0.82), "mouth_b": (0.22, hc[1] - 0.20, 0.82)}
    M.face = {"eyes": ["eye_l", "eye_r"], "eye": "angry", "mouth": ["mouth_a", "mouth_b"], "teeth": 3, "size": 1.0}
    return M


def make(model, yaw, pitch=6, n=56, ss=3, target=(0, 1.1, 0.1), half=1.7, dist=9.0):
    cam = Camera(target=target, yaw=yaw, pitch=pitch, dist=dist, half=half)
    t = time.time()
    buf = sdf.render(model, cam, n=n, ss=ss)
    red = toon.reduce(buf)
    img = toon.shade(red)
    return img, time.time() - t


def save(imgs, pal, path, scale=6):
    n = max(i.shape[0] for i in imgs)
    sheet = Image.new("RGB", (len(imgs) * (n * scale + 8), n * scale + 8), (70, 100, 140))
    for k, img in enumerate(imgs):
        h = img.shape[0]
        rgb = np.array(pal, np.uint8)[img]
        im = Image.fromarray(rgb).resize((h * scale, h * scale), Image.NEAREST)
        sheet.paste(im, (k * (n * scale + 8) + 4, 4))
    sheet.save(path)


if __name__ == "__main__":
    import rig
    pal = [(255, 255, 255), (132, 231, 0), (123, 82, 222), (0, 0, 0)]
    r = rig.Rig(brute)
    imgs = [r.render("front"), r.render("back"), r.render("front", {"jaw": 1, "glow": 1, "head_dy": 0.05}), r.render("front", {"head_dy": -0.04})]
    save(imgs, pal, "/home/claude/scratch/spr/proto3.png")
