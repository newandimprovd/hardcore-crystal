"""Species-specific extras for the plans: each function returns a hook(M, pose, A) that adds something to the finished model.  A holds world
space anchors: head, back, chest, hand (biped / centaur) and back, chest, hip, head (quadruped)."""
import math

import numpy as np

import parts
from parts import V
from sdf import ACCENT, BODY, BONE, DARK, MEMB


def volcano(size=1.0, flame=0.7):
    def hook(M, pose, A):
        M.part()
        b = A["back"] + V(0, 0.0, -0.05)
        M.cone(b, b + V(0, 0.95 * size, -0.1), 0.72 * size, 0.3 * size, BODY, 0.08)
        M.cone(b + V(0, 0.9 * size, -0.1), b + V(0, 1.0 * size, -0.1), 0.34 * size, 0.26 * size, ACCENT, 0.02)
        parts.flame(M, b + V(0, 1.0 * size, -0.1), flame * size, mat=ACCENT, up=(0, 1, -0.1))
    return hook


def flower(size=1.0, petals=8):
    def hook(M, pose, A):
        M.part()
        c = A["back"] + V(0, 0.55 * size, -0.1)
        M.cone(A["back"], c, 0.12, 0.1, BODY, 0.05)
        M.ell(c, (0.3 * size, 0.3 * size, 0.22 * size), ACCENT, 0.05)
        for i in range(petals):
            a = 2 * math.pi * i / petals
            tip = c + V(math.cos(a) * 1.0 * size, math.sin(a) * 1.0 * size, -0.35 * size)
            M.cone(c, tip, 0.3 * size, 0.09 * size, BONE if i % 2 else ACCENT, 0.06)
    return hook


def mushrooms(n=3, size=1.0):
    def hook(M, pose, A):
        M.part()
        b = A["back"]
        for i in range(n):
            u = (i - (n - 1) / 2)
            base = b + V(u * 0.55 * size, 0.1 + 0.08 * abs(u), -0.1 * abs(u))
            top = base + V(u * 0.12, (0.55 + 0.25 * (1 - abs(u) / (n))) * size, 0.0)
            M.cone(base, top, 0.1 * size, 0.08 * size, BONE, 0.03)
            M.ell(top + V(0, 0.06, 0), (0.42 * size, 0.2 * size, 0.42 * size), BODY, 0.05, tex=("spots", 3.5, 0.55, 0))
    return hook


def cannons(size=1.0):
    def hook(M, pose, A):
        M.part()
        for sgn in (-1, 1):
            b = A["back"] + V(sgn * 0.75, 0.05, 0.2)
            M.cone(b, b + V(sgn * 0.1, 0.5 * size, 0.7 * size), 0.2 * size, 0.2 * size, BODY, 0.03)
            M.cone(b + V(sgn * 0.1, 0.5 * size, 0.7 * size), b + V(sgn * 0.12, 0.6 * size, 0.9 * size), 0.24 * size, 0.24 * size, ACCENT, 0.02)
    return hook


def gem(size=1.0):
    def hook(M, pose, A):
        M.ell(A["head"] + V(0, 0.55 * size, 0.45 * size), (0.14 * size, 0.2 * size, 0.1 * size), ACCENT, 0.02)
    return hook


def halo(size=1.0):
    def hook(M, pose, A):
        M.part()
        c = A["head"] + V(0, 0.35, -0.65)
        for i in range(14):
            a = 2 * math.pi * i / 14
            M.ell(c + V(math.cos(a) * 0.8 * size, math.sin(a) * 0.8 * size, 0), (0.1, 0.1, 0.06), BONE, 0.02)
    return hook


def tails(n=5, length=1.6, spread=1.0):
    def hook(M, pose, A):
        M.part()
        b = A["hip"] + V(0, 0.1, -0.5)
        for i in range(n):
            u = (i - (n - 1) / 2)
            tip = b + V(u * 0.55 * spread, 0.5 + 0.35 * (1 - abs(u) / n), -length * (0.7 + 0.1 * (1 - abs(u) / n)))
            mid = b + V(u * 0.3 * spread, 0.1 + 0.25 * (1 - abs(u) / n), -length * 0.45)
            M.tube([b, mid, tip], 0.2, 0.05, BODY, 0.08)
            parts.flame(M, tip, 0.3, mat=ACCENT, up=(u * 0.2, 1, -0.2))
    return hook


def pendulum():
    def hook(M, pose, A):
        h = A["hand"]
        M.cone(h, h + V(0, -0.1, 0.5), 0.03, 0.03, BONE, 0.0)
        M.ell(h + V(0, -0.4, 0.55), (0.2, 0.2, 0.2), ACCENT, 0.02)
    return hook


def rings(n=2, r=1.5):
    def hook(M, pose, A):
        M.part()
        c = A["head"]
        for k in range(n):
            for i in range(16):
                a = 2 * math.pi * i / 16
                M.ell(c + V(math.cos(a) * r, math.sin(a) * r * 0.35 + (k - 0.5) * 0.4 * (n - 1), math.sin(a) * r * 0.6), (0.12, 0.1, 0.12), BONE, 0.03)
    return hook


def shell_halves(size=1.0):
    """A clam: two big shell halves with teeth around a pearl."""
    def hook(M, pose, A):
        M.part()
        c = A["head"]
        M.ell(c + V(0, 0.9 * size, -0.1), (1.5 * size, 0.55 * size, 1.2 * size), BODY, 0.06)
        M.ell(c + V(0, -0.5 * size, -0.1), (1.4 * size, 0.5 * size, 1.1 * size), BODY, 0.06)
        for i in range(7):
            x = (i - 3) * 0.38 * size
            M.spike(c + V(x, 0.45 * size, 0.85 * size), c + V(x, 0.1 * size, 0.95 * size), 0.09, BONE, 0.01)
            M.spike(c + V(x, -0.2 * size, 0.8 * size), c + V(x, 0.15 * size, 0.9 * size), 0.09, BONE, 0.01)
        M.ell(c + V(0, 0.15 * size, 0.2 * size), (0.45 * size, 0.45 * size, 0.45 * size), ACCENT, 0.03)
    return hook


def chain(*hooks):
    def hook(M, pose, A):
        for h in hooks:
            h(M, pose, A)
    return hook
