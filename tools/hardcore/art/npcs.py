"""Original overworld NPC sprites, drawn in code.

Every character is a recipe (a dict) turned into six 16x16 frames: stand down, up, left and walk down, up, left (the engine mirrors
left for right and alternates the walk frames by flipping them).  The sprite sheet is 16x96, 4 colors: 0 transparent, 1 skin,
2 cloth, 3 dark (hair, shoes, outline).  The real colors come from the NPC object palette that the map uses (see areapal.py,
per-area NPC palettes), so one sheet looks different in every area.

Drawing order: legs, torso, arms, head, hair, hat, extras; the outline (index 3) is added at the end around everything.
Fills are kept inside x 2..13, y 1..14 so the outline fits the 16x16 frame."""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
S, C, D = 1, 2, 3
COL = {"S": S, "C": C, "D": D}


class Fig:
    def __init__(self):
        self.g = [[0] * 16 for _ in range(16)]
        self.oy = 0  # vertical offset of the upper body (walk frames bob down one pixel)

    def px(self, x, y, c):
        y += self.oy
        if 0 <= x < 16 and 0 <= y < 16 and c is not None:
            self.g[y][x] = c

    def r(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def pts(self, pts, c):
        for (x, y) in pts:
            self.px(x, y, c)

    def get(self, x, y):
        y += self.oy
        return self.g[y][x] if 0 <= x < 16 and 0 <= y < 16 else 0

    def outline(self):
        src = [row[:] for row in self.g]
        for y in range(16):
            for x in range(16):
                if src[y][x] == 0:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < 16 and 0 <= yy < 16 and src[yy][xx] != 0:
                            self.g[y][x] = D
                            break


def col(name):
    return COL[name]


# ------------------------------------------------------------------------------------------------------ recipes

DEFAULT = dict(
    hair="short", hairc="D", hat=None, hatc="C", torso="shirt", torsoc="C", legs="pants", legsc="D", extra=(),
    face="eyes", armc=None, shoes="D", skin_legs=False, width=0,
)


def recipe(**kw):
    r = dict(DEFAULT)
    r.update(kw)
    return r


# ------------------------------------------------------------------------------------------------------ legs

def legs(f, view, rec, walk):
    k = rec["legs"]
    lc = col(rec["legsc"])
    if k in ("robe", "hover", "treads"):
        return  # drawn with the torso
    y0 = 13
    if view in "FB":
        if not walk:
            f.r(5, y0, 6, 14, lc)
            f.r(9, y0, 10, 14, lc)
            f.r(5, 14, 6, 14, col(rec["shoes"]))
            f.r(9, 14, 10, 14, col(rec["shoes"]))
            if k == "shorts":
                f.r(5, 14, 6, 14, S)
                f.r(9, 14, 10, 14, S)
                f.r(5, 13, 6, 13, lc)
                f.r(9, 13, 10, 13, lc)
        else:
            f.r(5, 14, 6, 14, col(rec["shoes"]) if k != "shorts" else S)
            f.r(9, 14, 10, 14, lc if k == "shorts" else lc)
            f.r(9, 13, 10, 13, lc)
    else:
        if not walk:
            f.r(5, 13, 8, 14, lc)
            f.r(4, 14, 8, 14, col(rec["shoes"]))
            if k == "shorts":
                f.r(5, 14, 8, 14, S)
                f.r(4, 14, 4, 14, col(rec["shoes"]))
        else:
            # scissor: one foot ahead, one behind
            f.r(5, 14, 6, 14, lc)
            f.r(3, 14, 4, 14, col(rec["shoes"]))
            f.r(8, 14, 9, 14, col(rec["shoes"]))


# ------------------------------------------------------------------------------------------------------ torso

def torso(f, view, rec, walk):
    k = rec["torso"]
    tc = col(rec["torsoc"])
    wd = rec["width"]
    if view in "FB":
        x0, x1 = 4 - wd, 11 + wd
        if k in ("robe", "habit"):
            f.r(x0 + 1, 9, x1 - 1, 9, tc)
            f.r(x0, 10, x1, 12, tc)
            f.r(x0 - 1 if wd else x0, 13, x1 + 1 if wd else x1, 14, tc)
            if walk:
                f.px(x0, 14 - 0, 0)
        elif k == "coat":
            f.r(x0 + 1, 9, x1 - 1, 9, tc)
            f.r(x0, 10, x1, 12, tc)
            f.r(x0, 13, x1, 13, tc)
        elif k == "dress":
            f.r(x0 + 1, 9, x1 - 1, 9, tc)
            f.r(x0, 10, x1, 11, tc)
            f.r(x0 - 1, 12, x1 + 1, 12, tc)
        elif k == "bare":
            f.r(x0 + 1, 9, x1 - 1, 9, S)
            f.r(x0, 10, x1, 12, S)
        elif k == "swim":
            f.r(x0 + 1, 9, x1 - 1, 9, S)
            f.r(x0, 10, x1, 12, S)
            f.r(x0 + 1, 12, x1 - 1, 12, tc)
        elif k == "armor":
            f.r(x0 - 1, 9, x1 + 1, 9, tc)
            f.r(x0, 10, x1, 12, tc)
        else:  # shirt, labcoat, vest, aloha, striped ...
            f.r(x0 + 1, 9, x1 - 1, 9, tc)
            f.r(x0, 10, x1, 12, tc)
    else:
        if k in ("robe", "habit", "dress"):
            f.r(5, 9, 9, 9, tc)
            f.r(4, 10, 10, 12, tc)
            f.r(3 if k == "dress" else 4, 13, 10 if k != "dress" else 11, 13, tc) if False else None
        elif k == "coat":
            f.r(5, 9, 9, 13, tc)
            f.r(4, 10, 10, 12, tc)
        elif k in ("bare", "swim"):
            f.r(5, 9, 9, 12, S)
            if k == "swim":
                f.r(5, 12, 9, 12, tc)
        else:
            f.r(5, 9, 9, 12, tc)


def robe_hem(f, view, rec, walk):
    if rec["legs"] != "robe":
        return
    if walk:
        # little wobble of the hem
        if view in "FB":
            f.px(4, 14, 0)
            f.px(11, 14, 0)
        else:
            f.px(4, 14, 0)


# ------------------------------------------------------------------------------------------------------ arms

def arms(f, view, rec, walk):
    k = rec["torso"]
    ac = col(rec["armc"] or rec["torsoc"])
    bare = k in ("bare", "swim", "dress") or rec.get("barearms")
    sc = S if bare else ac
    wd = rec["width"]
    if view in "FB":
        for x0, x1 in ((2 - wd, 3 - wd), (12 + wd, 13 + wd)):
            f.r(x0, 10, x1, 11, sc)
            f.r(x0, 12, x1, 12, S)
        if walk:
            pass
    else:
        f.r(6, 10, 8, 11, sc)
        f.r(6, 12, 7, 12, S)
        # a dark seam so the arm reads against the torso
        f.px(9, 11, D)
        f.px(5, 11, D)


# ------------------------------------------------------------------------------------------------------ head

HEAD_ROWS_F = {2: (5, 10), 3: (4, 11), 4: (4, 11), 5: (4, 11), 6: (4, 11), 7: (4, 11), 8: (5, 10)}
HEAD_ROWS_L = {2: (5, 9), 3: (4, 10), 4: (4, 10), 5: (4, 10), 6: (4, 10), 7: (4, 10), 8: (5, 9)}


def head(f, view, rec, walk):
    rows = HEAD_ROWS_F if view in "FB" else HEAD_ROWS_L
    skin = rec.get("skinc", S)
    for y, (a, b) in rows.items():
        f.r(a, y, b, y, skin)
    face = rec["face"]
    ec = col(rec.get("eyec", "D"))
    mc = col(rec.get("mouthc", "D"))
    if view == "F":
        if face == "eyes":
            f.px(6, 6, ec)
            f.px(9, 6, ec)
        elif face == "tired":
            f.r(5, 6, 6, 6, ec)
            f.r(9, 6, 10, 6, ec)
            f.px(7, 8, mc)
            f.px(8, 8, mc)
        elif face == "blank":
            f.px(6, 6, ec)
            f.px(9, 6, ec)
            f.r(6, 8, 9, 8, mc)
        elif face == "grin":
            f.px(6, 6, ec)
            f.px(9, 6, ec)
            f.r(5, 8, 10, 8, mc)
        elif face == "angry":
            f.px(6, 6, ec)
            f.px(9, 6, ec)
            f.px(5, 5, ec)
            f.px(10, 5, ec)
            f.r(7, 8, 8, 8, mc)
        elif face == "glow":  # two lit eyes in a dark face
            f.r(5, 6, 6, 6, ec)
            f.r(9, 6, 10, 6, ec)
        elif face == "hollow":  # skull: big eye sockets and a toothy mouth
            f.r(5, 5, 6, 6, D)
            f.r(9, 5, 10, 6, D)
            f.px(8, 7, D)
            f.r(6, 8, 9, 8, D)
            f.pts([(7, 8), (9, 8)], skin)
        elif face == "none":
            pass
    elif view == "L":
        if face == "glow":
            f.px(5, 5, ec)
            f.px(5, 6, ec)
        elif face == "hollow":
            f.r(5, 5, 6, 6, D)
            f.r(4, 8, 6, 8, D)
        elif face != "none":
            f.px(3, 6, skin)  # nose
            f.px(5, 5, ec)
            if face in ("tired", "angry", "blank"):
                f.px(5, 4, ec)


def hair(f, view, rec, walk):
    k = rec["hair"]
    hc = col(rec["hairc"])
    if k in ("bald", None):
        if view == "B" or view == "L":
            pass
        return
    if view in "FB":
        if k == "short":
            f.r(5, 2, 10, 2, hc)
            f.r(4, 3, 11, 3, hc)
            if view == "F":
                f.px(4, 4, hc)
                f.px(11, 4, hc)
                f.r(5, 4, 5, 4, hc)
                f.r(10, 4, 10, 4, hc)
            else:
                f.r(4, 4, 11, 7, hc)
                f.r(5, 8, 10, 8, hc) if False else None
        elif k == "long":
            f.r(5, 2, 10, 2, hc)
            f.r(4, 3, 11, 3, hc)
            f.r(3, 3, 3, 10, hc)
            f.r(12, 3, 12, 10, hc)
            f.r(4, 4, 4, 9, hc)
            f.r(11, 4, 11, 9, hc)
            if view == "F":
                f.r(5, 4, 6, 4, hc)
                f.r(9, 4, 10, 4, hc)
            else:
                f.r(4, 4, 11, 10, hc)
        elif k == "mohawk":
            f.r(7, 1, 8, 3, hc)
            f.r(7, 0, 8, 0, hc)
            if view == "B":
                f.r(7, 4, 8, 6, hc)
        elif k == "bun":
            f.r(5, 2, 10, 2, hc)
            f.r(4, 3, 11, 3, hc)
            f.r(7, 0, 8, 1, hc)
            if view == "F":
                f.px(4, 4, hc)
                f.px(11, 4, hc)
            else:
                f.r(4, 4, 11, 7, hc)
        elif k == "bushy":
            f.r(4, 1, 11, 2, hc)
            f.r(3, 2, 12, 5, hc)
            if view == "F":
                f.r(5, 4, 10, 4, S)
                f.r(4, 3, 4, 3, hc)
            else:
                f.r(3, 2, 12, 8, hc)
        elif k == "afro":
            f.r(4, 0, 11, 1, hc)
            f.r(3, 1, 12, 6, hc)
            if view == "F":
                f.r(5, 4, 10, 5, S)
            else:
                f.r(3, 1, 12, 8, hc)
        elif k == "pigtails":
            f.r(5, 2, 10, 2, hc)
            f.r(4, 3, 11, 3, hc)
            f.r(2, 5, 3, 8, hc)
            f.r(12, 5, 13, 8, hc)
            if view == "F":
                f.px(4, 4, hc)
                f.px(11, 4, hc)
            else:
                f.r(4, 4, 11, 7, hc)
    else:  # left
        if k == "short":
            f.r(5, 2, 9, 2, hc)
            f.r(4, 3, 10, 3, hc)
            f.r(7, 4, 10, 7, hc)
        elif k == "long":
            f.r(5, 2, 9, 2, hc)
            f.r(4, 3, 10, 3, hc)
            f.r(7, 4, 10, 10, hc)
        elif k == "mohawk":
            f.r(6, 0, 8, 3, hc)
        elif k == "bun":
            f.r(5, 2, 9, 2, hc)
            f.r(4, 3, 10, 3, hc)
            f.r(7, 4, 10, 7, hc)
            f.r(8, 0, 10, 2, hc)
        elif k == "bushy":
            f.r(4, 1, 10, 2, hc)
            f.r(4, 2, 11, 3, hc)
            f.r(6, 4, 11, 8, hc)
        elif k == "afro":
            f.r(4, 0, 11, 1, hc)
            f.r(4, 1, 11, 8, hc)
        elif k == "pigtails":
            f.r(5, 2, 9, 2, hc)
            f.r(4, 3, 10, 3, hc)
            f.r(7, 4, 10, 7, hc)
            f.r(9, 5, 11, 9, hc)


# ------------------------------------------------------------------------------------------------------ hats

def hat(f, view, rec, walk):
    if not rec["hat"]:
        return
    for k in rec["hat"].split("+"):
        one_hat(f, view, rec, k)


def one_hat(f, view, rec, k):
    hc = col(rec["hatc"])
    F = view in "FB"
    if k == "cap":
        f.r(5, 1, 10, 1, hc)
        f.r(4, 2, 11, 3, hc)
        if view == "F":
            f.r(4, 4, 11, 4, D)
        elif view == "L":
            f.r(2, 3, 10, 4, hc)
            f.r(2, 4, 4, 4, D)
        else:
            f.r(4, 4, 11, 4, hc)
    elif k == "bowler":
        f.r(5, 0, 10, 0, hc)
        f.r(4, 1, 11, 3, hc)
        f.r(2 if F else 2, 4, 13 if F else 11, 4, hc)
        f.r(4, 3, 11, 3, D)
    elif k == "tophat":
        f.r(5, -1 + 1, 10, 0, hc)
        f.r(4, 1, 11, 2, hc)
        f.r(2, 3, 13, 3, hc)
        f.r(4, 2, 11, 2, D)
    elif k == "mitre":
        f.r(7, 0, 8, 0, hc)
        f.r(6, 1, 9, 1, hc)
        f.r(5, 2, 10, 3, hc)
        f.r(4, 3, 11, 3, hc)
        f.r(7, 2, 8, 3, S) if view == "F" else None
        if view == "F":
            f.px(7, 1, S)
            f.px(8, 1, S)
    elif k == "hood":
        f.r(5, 1, 10, 1, hc)
        f.r(4, 2, 11, 4, hc)
        f.r(3, 4, 12, 9, hc)
        if F or True:
            if view == "F":
                f.r(5, 4, 10, 8, S)
                f.px(5, 4, hc)
                f.px(10, 4, hc)
            elif view == "L":
                f.r(4, 5, 5, 8, S)
    elif k == "wimple":
        f.r(5, 1, 10, 1, hc)
        f.r(4, 2, 11, 3, hc)
        f.r(3, 4, 12, 10, hc)
        if view == "F":
            f.r(5, 4, 10, 8, S)
        elif view == "L":
            f.r(4, 5, 5, 8, S)
    elif k == "visor":
        f.r(4, 2, 11, 2, hc)
        if view == "F":
            f.r(3, 3, 12, 3, hc)
        elif view == "L":
            f.r(2, 3, 10, 3, hc)
        else:
            f.r(3, 3, 12, 3, hc)
    elif k == "sunhat":
        f.r(5, 1, 10, 1, hc)
        f.r(4, 2, 11, 2, hc)
        f.r(2, 3, 13, 3, hc)
        f.r(3, 4, 12, 4, hc)
        f.r(4, 2, 11, 2, D) if False else None
    elif k == "crown":  # flower crown: dots around the top of the head
        f.pts([(5, 2), (7, 1), (9, 2), (10, 3), (4, 3), (8, 1)] if view != "L" else [(5, 2), (7, 1), (9, 2), (10, 3)], hc)
    elif k == "horns":
        if view == "L":
            f.r(6, 0, 6, 2, hc)
            f.px(5, 0, hc)
            f.r(9, 0, 9, 2, hc)
        else:
            f.r(4, 0, 4, 2, hc)
            f.r(11, 0, 11, 2, hc)
            f.px(3, 0, hc)
            f.px(12, 0, hc)
    elif k == "antlers":
        if view == "L":
            f.pts([(6, 1), (6, 0), (5, -0), (8, 1), (9, 0), (8, 0), (10, 1)], hc)
        else:
            f.pts([(5, 1), (4, 0), (3, 0), (4, 1), (10, 1), (11, 0), (12, 0), (11, 1), (5, 2), (10, 2)], hc)
    elif k == "helmet":
        f.r(5, 1, 10, 1, hc)
        f.r(4, 2, 11, 4, hc)
        if view == "F":
            f.r(5, 5, 10, 5, hc)
            f.r(5, 4, 10, 4, D)
        elif view == "B":
            f.r(4, 5, 11, 7, hc)
        else:
            f.r(4, 5, 10, 6, hc)
    elif k == "bandana":
        f.r(4, 3, 11, 3, hc)
        if view == "B":
            f.r(10, 3, 13, 4, hc)
        elif view == "L":
            f.r(9, 3, 12, 5, hc)
    elif k == "swimcap":
        f.r(5, 1, 10, 1, hc)
        f.r(4, 2, 11, 3, hc)
        if view == "F":
            f.px(4, 4, hc)
            f.px(11, 4, hc)
        elif view == "B":
            f.r(4, 4, 11, 6, hc)
        else:
            f.r(7, 4, 10, 6, hc)
    elif k == "jester":
        f.r(4, 2, 11, 3, hc)
        f.pts([(3, 1), (2, 0), (12, 1), (13, 0), (7, 1), (8, 1), (7, 0), (8, 0)], D)
        f.pts([(3, 2), (12, 2)], hc)
    elif k == "halo":
        f.r(5, 0, 10, 0, hc)
    elif k == "zuc":  # skull cap
        f.r(6, 1, 9, 1, hc)
        f.r(5, 2, 10, 2, hc)
    elif k == "beret":
        f.r(5, 1, 11, 1, hc)
        f.r(4, 2, 11, 3, hc)
    elif k == "antenna":
        f.pts([(7, 0), (7, -1)] if False else [(7, 0)], hc)
        f.r(8, 0, 8, 1, hc)
        f.px(8, -1, hc)
    elif k == "witch":
        f.r(7, 0, 8, 0, hc)
        f.r(6, 1, 9, 1, hc)
        f.r(5, 2, 10, 2, hc)
        f.r(2, 3, 13, 3, hc)
        f.r(4, 3, 11, 3, D) if False else None
    elif k == "crownk":  # king's crown
        f.pts([(4, 1), (6, 0), (8, 1), (10, 0), (11, 1)], hc)
        f.r(4, 2, 11, 2, hc)


# ------------------------------------------------------------------------------------------------------ extras

def extras(f, view, rec, walk):
    for e in rec["extra"]:
        EX[e](f, view, rec, walk)


def ex_beard(f, view, rec, walk):
    bc = col(rec.get("beardc", "D"))
    if view == "F":
        f.r(4, 7, 11, 7, bc)
        f.r(5, 8, 10, 9, bc)
        f.r(7, 8, 8, 8, S) if False else None
    elif view == "L":
        f.r(4, 7, 8, 7, bc)
        f.r(4, 8, 8, 9, bc)
    # back: nothing


def ex_glasses(f, view, rec, walk):
    if view == "F":
        f.r(5, 6, 6, 6, D)
        f.r(9, 6, 10, 6, D)
        f.px(7, 6, D) if False else None
    elif view == "L":
        f.r(3, 5, 5, 5, D)


def ex_sunglasses(f, view, rec, walk):
    if view == "F":
        f.r(5, 5, 10, 6, D)
        f.r(7, 5, 8, 5, S)
    elif view == "L":
        f.r(3, 5, 6, 6, D)


def ex_monocle(f, view, rec, walk):
    if view == "F":
        f.px(9, 6, D)
        f.pts([(10, 5), (10, 7), (11, 6)], D)


def ex_tie(f, view, rec, walk):
    if view == "F":
        f.r(7, 9, 8, 9, S)
        f.r(7, 10, 8, 12, D)


def ex_collar(f, view, rec, walk):  # white clerical collar tab
    if view == "F":
        f.r(7, 9, 8, 9, S)


def ex_badge(f, view, rec, walk):
    if view == "F":
        f.pts([(5, 10), (5, 11)], S)
    elif view == "L":
        f.px(6, 10, S)


def ex_belt(f, view, rec, walk):
    if view in "FB":
        f.r(4, 12, 11, 12, D)
    else:
        f.r(5, 12, 9, 12, D)


def ex_cross(f, view, rec, walk):
    if view == "F":
        f.pts([(7, 10), (8, 10), (7, 11), (7, 12), (8, 11) if False else (7, 11)], S)
        f.pts([(6, 11), (8, 11)], S)


def ex_chain(f, view, rec, walk):
    if view == "F":
        f.pts([(5, 9), (6, 10), (7, 11), (8, 11), (9, 10), (10, 9)], S)
        f.px(7, 12, S)
        f.px(8, 12, S)


def ex_tail(f, view, rec, walk):
    if view == "B":
        f.pts([(12, 14), (13, 13), (13, 12)], col(rec.get("tailc", "D")))
    elif view == "L":
        f.pts([(10, 13), (11, 13), (12, 12), (12, 11)], col(rec.get("tailc", "D")))
    else:
        f.pts([(12, 14), (13, 13)], col(rec.get("tailc", "D")))


def ex_wings(f, view, rec, walk):
    wc = col(rec.get("wingc", "D"))
    if view == "B":
        f.r(1, 8, 3, 12, wc)
        f.r(12, 8, 14, 12, wc)
    elif view == "F":
        f.pts([(2, 8), (1, 7), (13, 8), (14, 7)], wc)
    else:
        f.r(9, 8, 12, 11, wc)


def ex_pocket_stripes(f, view, rec, walk):
    """Horizontal stripes on the shirt (sailor, prisoner)."""
    if view in "FB":
        for y in (10, 12):
            f.r(4, y, 11, y, col(rec.get("stripec", "S")))
    else:
        for y in (10, 12):
            f.r(5, y, 9, y, col(rec.get("stripec", "S")))


def ex_aloha(f, view, rec, walk):
    """Loud shirt: dots of the light color."""
    pts = [(5, 10), (8, 10), (10, 11), (6, 12), (9, 12), (4, 11)]
    if view in "FB":
        f.pts(pts, col(rec.get("patc", "S")))
    else:
        f.pts([(6, 10), (8, 11), (6, 12), (9, 12)], col(rec.get("patc", "S")))


def ex_number(f, view, rec, walk):
    """Prisoner / serf number patch on the chest."""
    if view == "F":
        f.r(6, 10, 9, 11, S)
        f.pts([(7, 10), (8, 11)], D)
    elif view == "B":
        f.r(6, 10, 9, 11, S)
        f.pts([(7, 11), (8, 10)], D)


def ex_visor(f, view, rec, walk):
    """Robot eye visor: a dark band with one lit dot."""
    if view == "F":
        f.r(5, 5, 10, 6, D)
        f.px(8, 5, S)
        f.px(7, 5, S) if False else None
    elif view == "L":
        f.r(3, 5, 6, 6, D)
        f.px(4, 5, S)


def ex_antenna(f, view, rec, walk):
    f.px(8, 0, D)
    f.px(8, 1, D)
    f.px(9, -1, D) if False else None
    f.px(8, -0, D)


def ex_staff(f, view, rec, walk):
    sc = col(rec.get("staffc", "D"))
    if view == "F":
        f.r(14, 5, 14, 14, sc)
        f.px(14, 4, S)
        f.pts([(13, 5), (15, 5)], sc) if False else None
    elif view == "B":
        f.r(1, 5, 1, 14, sc)
    else:
        f.r(2, 6, 2, 14, sc)
        f.px(2, 5, S)


def ex_bag(f, view, rec, walk):
    bc = col(rec.get("bagc", "D"))
    if view == "B":
        f.r(5, 9, 10, 13, bc)
    elif view == "L":
        f.r(9, 9, 11, 12, bc)
    elif view == "F":
        f.px(4, 9, bc)
        f.px(11, 9, bc)
        f.px(4, 10, bc)
        f.px(11, 10, bc)


def ex_rod(f, view, rec, walk):
    if view == "F":
        f.r(14, 3, 14, 12, D)
        f.pts([(13, 3), (12, 4)], D)
    elif view == "L":
        f.r(2, 4, 2, 12, D)
        f.pts([(1, 3), (0, 3)], D)


def ex_tray(f, view, rec, walk):
    if view == "F":
        f.r(13, 8, 15 - 1, 8, S)
        f.px(13, 7, D)


def ex_blush_dots(f, view, rec, walk):
    if view == "F":
        f.px(5, 7, D)
        f.px(10, 7, D)


def ex_mask(f, view, rec, walk):
    """Surgical mask."""
    if view == "F":
        f.r(5, 7, 10, 8, S)
        f.r(5, 7, 10, 7, col("C"))
        f.r(5, 8, 10, 8, col("C"))
    elif view == "L":
        f.r(3, 7, 5, 8, col("C"))


def ex_cheeks(f, view, rec, walk):
    if view == "F":
        f.pts([(5, 7), (10, 7)], col("C"))


def ex_buttons(f, view, rec, walk):
    if view == "F":
        f.pts([(7, 10), (7, 12)], D)
        f.px(7, 14, D) if rec["legs"] == "robe" else None


def ex_ribs(f, view, rec, walk):
    if view == "F":
        f.r(5, 10, 10, 10, D)
        f.r(5, 12, 10, 12, D)
        f.r(7, 9, 8, 9, D) if False else None
    elif view == "B":
        f.r(7, 9, 8, 12, D)
    else:
        f.r(6, 10, 8, 10, D)
        f.r(6, 12, 8, 12, D)


def ex_hem(f, view, rec, walk):  # dark hem line on a robe
    if view in "FB":
        f.r(3, 14, 12, 14, D)
    else:
        f.r(4, 14, 11, 14, D)


def ex_sash(f, view, rec, walk):  # diagonal sash across the chest
    if view == "F":
        f.pts([(5, 9), (6, 10), (7, 11), (8, 12)], col(rec.get("sashc", "D")))
    elif view == "B":
        f.pts([(10, 9), (9, 10), (8, 11), (7, 12)], col(rec.get("sashc", "D")))


def ex_goggles(f, view, rec, walk):
    if view == "F":
        f.r(4, 4, 11, 4, D)
        f.pts([(5, 5), (6, 5), (9, 5), (10, 5)], S)
    elif view == "L":
        f.r(4, 4, 6, 4, D)
        f.px(5, 5, S)


def ex_spikes(f, view, rec, walk):  # shoulder spikes
    if view in "FB":
        f.pts([(2, 9), (13, 9), (2, 8), (13, 8)], D)


def ex_whisker_hair(f, view, rec, walk):  # long beard that reaches the chest
    if view == "F":
        f.r(5, 8, 10, 10, col(rec.get("beardc", "S")))
        f.r(6, 11, 9, 11, col(rec.get("beardc", "S")))
    elif view == "L":
        f.r(4, 8, 7, 10, col(rec.get("beardc", "S")))


def ex_fangs(f, view, rec, walk):
    if view == "F":
        f.pts([(6, 8), (9, 8)], S)


def ex_hump(f, view, rec, walk):
    pass


EX = {k[3:]: v for k, v in dict(globals()).items() if k.startswith("ex_")}


# ------------------------------------------------------------------------------------------------------ special bodies

def body_special(f, view, rec, walk):
    """Bodies that replace the torso/legs: treads (robots), hover (ghosts), robe skirts (extended torso)."""
    k = rec["legs"]
    tc = col(rec["torsoc"])
    if k == "treads":
        if view in "FB":
            f.r(4, 13, 11, 13, D)
            f.r(3, 14, 12, 14, tc)
            f.pts([(4, 14), (6, 14), (9, 14), (11, 14)], D)
        else:
            f.r(4, 13, 10, 13, D)
            f.r(3, 14, 11, 14, tc)
            f.pts([(4, 14), (6, 14), (8, 14), (10, 14)], D)
    elif k == "hover":
        if view in "FB":
            f.r(5, 13, 10, 13, tc)
            f.r(6, 14, 9, 14, tc if walk else D)
        else:
            f.r(5, 13, 9, 13, tc)
            f.r(6, 14, 8, 14, tc if walk else D)
    elif k == "robe":
        if view in "FB":
            f.r(3, 13, 12, 14, tc)
        else:
            f.r(4, 13, 11, 14, tc)


def frame(rec, view, walk):
    f = Fig()
    if walk:
        f.oy = 1
    # legs are drawn without the upper body offset (they stay on the ground)
    oy, f.oy = f.oy, 0
    if rec["legs"] in ("treads", "hover", "robe"):
        f.oy = oy
        body_special(f, view, rec, walk)
        f.oy = oy
    else:
        legs(f, view, rec, walk)
        f.oy = oy
    torso(f, view, rec, walk)
    arms(f, view, rec, walk)
    head(f, view, rec, walk)
    hair(f, view, rec, walk)
    hat(f, view, rec, walk)
    extras(f, view, rec, walk)
    f.oy = 0
    f.outline()
    return f.g


def sheet_rows(rec):
    """Six frames stacked: down, up, left, walk down, walk up, walk left."""
    rows = []
    for walk in (False, True):
        for view in "FBL":
            rows += frame(rec, view, walk)
    return rows


# ------------------------------------------------------------------------------------------------------ output

PNG_SHADES = {0: 255, 1: 170, 2: 85, 3: 0}


def write_png(rec, path):
    rows = sheet_rows(rec)
    im = Image.new("L", (16, 96), 255)
    for y, row in enumerate(rows):
        for x, v in enumerate(row):
            im.putpixel((x, y), PNG_SHADES[v])
    im.save(path)


def preview(recs, path, pals=None, scale=6, per_row=3):
    """Contact sheet: one column per recipe, the six frames side by side, drawn with the palette (idx 1,2,3 RGB)."""
    pals = pals or {}
    n = len(recs)
    cols = 6
    fw = 18
    cellw = cols * fw
    rowsn = (n + per_row - 1) // per_row
    im = Image.new("RGB", (per_row * cellw * scale, rowsn * 20 * scale), (200, 200, 200))
    for i, (name, rec) in enumerate(recs):
        rows = sheet_rows(rec)
        pal = pals.get(name, [(200, 200, 200), (248, 168, 88), (200, 40, 40), (16, 16, 16)])
        ox = (i % per_row) * cellw * scale
        oy = (i // per_row) * 20 * scale
        for fi in range(6):
            for y in range(16):
                for x in range(16):
                    v = rows[fi * 16 + y][x]
                    c = (232, 232, 232) if v == 0 else pal[v]
                    for dy in range(scale):
                        for dx in range(scale):
                            im.putpixel((ox + (fi * fw + 1 + x) * scale + dx, oy + (1 + y) * scale + dy), c)
    im.save(path)
