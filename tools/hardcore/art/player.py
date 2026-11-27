"""Chris, the player (alpha 3.3): a scruffy, tired criminal with a duffel over one shoulder, drawn from the same figure code as the trainers.

CHRIS is a cast recipe (art/npcs.py), so the overworld sheet (16x96), the front picture (56x56) and the trainer card picture (40x56) come from it and
agree with each other.  The battle back picture (48x48) is drawn here: the same man from behind, the jacket collar up around a messy head of hair, the
duffel strap across the back and one arm out holding a ball.  Palette indices as everywhere: 0 white, 1 skin, 2 cloth, 3 black.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bigfig  # noqa: E402
import npcs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SHADES = {0: 255, 1: 170, 2: 85, 3: 0}
CHRIS = npcs.recipe(hair="bushy", hairc="D", torso="coat", torsoc="C", legsc="D", face="tired", extra=("bag", "belt"))


def save(px, path):
    px = np.asarray(px)
    im = Image.new("L", (px.shape[1], px.shape[0]), 255)
    im.putdata([SHADES[int(v)] for v in px.ravel()])
    im.save(path)


def front():
    return bigfig.draw(CHRIS, hold="ball")


def card():
    """The trainer card shows the front picture without the margins: columns 5..44 of the 56 wide figure."""
    return front()[:, 5:45]


def back():
    """48x48 from behind.  Drawn on the 56x56 canvas of the figure painter with an offset of (4, 8), then cut out."""
    p = bigfig.Painter(1.0)
    ox, oy = 4, 8

    def X(u):
        return u + ox

    def Y(v):
        return v + oy

    def ell(u, v, rx, ry=None, rot=0.0):
        return p.ell(X(u), Y(v), rx, ry, rot)

    def poly(pts):
        return p.poly([(X(u), Y(v)) for u, v in pts])

    def tube(pts, w0, w1=None):
        return p.tube([(X(u), Y(v)) for u, v in pts], w0, w1)

    # duffel behind the hip on the far side
    p.paint(ell(37, 43, 8, 7), 3, hi=0.6)
    # the arm that hangs on the viewer's left
    p.paint(tube([(8, 33), (5, 41), (6, 48)], 7.5, 6.5), 2, hi=0.8)
    # jacket: broad shoulders, tapering to the waist
    p.paint(poly([(2, 48), (4, 36), (11, 30), (33, 30), (40, 36), (44, 48)]) | ell(22, 31, 12, 4), 2, hi=0.8)
    # strap across the back
    p.line(X(12), Y(31), X(36), Y(46), 3)
    p.line(X(13), Y(31), X(37), Y(46), 3)
    p.line(X(12), Y(32), X(35), Y(47), 3)
    # the raised arm, the viewer's right, with the ball in the hand
    p.paint(tube([(32, 34), (37, 37), (39, 31)], 7.0, 6.0), 2, hi=0.8)
    p.paint(ell(39, 28, 3.2, 3.6), 1, hi=0.6, sd=0.0, R=2.0)
    ball = ell(42, 24, 3.6)
    p.paint(ball, 0, outline=True, flat=True)
    top = ball & p.rect(X(37), Y(18), X(47), Y(24.2))
    for y in range(bigfig.N):
        for x in range(bigfig.N):
            if top.a[y, x] and p.px[y, x] == 0:
                p.px[y, x] = 2
    p.line(X(38.4), Y(24.6), X(45.6), Y(24.6), 3)
    p.paint(ell(42, 24.8, 1.2), 0, flat=True)
    # collar and hood bunched up around the neck
    p.paint(ell(22, 30, 9.5, 3.4), 2, hi=0.9)
    # neck and ears
    p.paint(ell(22, 27, 3.8, 3.2), 1, flat=True)
    p.paint(ell(11, 19, 2.4, 3.0) | ell(33, 19, 2.4, 3.0), 1, hi=0.0, sd=0.0, flat=True)
    # the head of messy hair, with a few short tufts
    hair = ell(22, 16, 10.5, 11.5)
    for (bu, bv, tu, tv, w) in ((15, 8, 12, 3, 7), (22, 5, 23, 1, 7), (29, 8, 33, 3, 7)):
        hair = hair | p.spike(X(bu), Y(bv), X(tu), Y(tv), w)
    p.paint(hair, 3, hi=0.9, R=4.0, lit=2)
    # locks in the hair
    p.line(X(21), Y(8), X(23), Y(16), 2)
    p.line(X(15), Y(14), X(16), Y(21), 2)
    p.line(X(29), Y(14), X(28), Y(21), 2)
    return p.px[oy:oy + 48, ox:ox + 48].copy()


def overworld():
    return npcs.sheet_rows(CHRIS)


def write_all():
    save(overworld(), os.path.join(ROOT, "gfx/sprites/chris.png"))
    save(front(), os.path.join(ROOT, "gfx/player/chris.png"))
    save(card(), os.path.join(ROOT, "gfx/trainer_card/chris_card.png"))
    save(back(), os.path.join(ROOT, "gfx/player/chris_back.png"))


def preview(path, pal=((255, 255, 255), (240, 190, 150), (200, 40, 40), (0, 0, 0)), scale=6):
    parts = [front(), card(), back()]
    sheet = np.array(overworld())
    parts.append(np.concatenate([sheet[i * 16:(i + 1) * 16] for i in range(6)], axis=1))
    pal = np.array(pal, np.uint8)
    ims = []
    for a in parts:
        rgb = pal[a].copy()
        rgb[a == 0] = (232, 232, 232)
        ims.append(Image.fromarray(rgb).resize((a.shape[1] * scale, a.shape[0] * scale), Image.NEAREST))
    W = sum(i.width for i in ims[:3]) + 20
    H = max(i.height for i in ims[:3]) + 10 + ims[3].height
    out = Image.new("RGB", (max(W, ims[3].width), H), (120, 120, 120))
    x = 0
    for i in ims[:3]:
        out.paste(i, (x, 0))
        x += i.width + 10
    out.paste(ims[3], (0, ims[0].height + 10))
    out.save(path)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "write":
        write_all()
    else:
        preview("/home/claude/scratch/spr/chris_new.png")
