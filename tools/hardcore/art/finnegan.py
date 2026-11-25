"""FINNEGAN's battle picture (56x56, four colors: 0 white, 1 skin, 2 cloth, 3 black): the last boss as a distorted humanoid.

A skull too large for the body on a thin neck, tilted, with a crack running down the forehead, one big and one small eye, a grin from ear to ear with too many teeth,
long hair that hangs past the shoulders, a ragged robe that ends in strips, two long arms that reach down and out with long fingers, a second pair of hands folded at the waist,
and bands of rows knocked sideways, as if the figure were a bad copy of a man.  Drawn with PIL (no antialiasing) and a fixed random seed, so the picture never changes
between runs.  usage (preview): python3 finnegan.py out.png"""
import random
import sys

from PIL import Image, ImageDraw

W = H = 56
BG, SKIN, CLOTH, BLACK, CLEAR = 0, 1, 2, 3, 4


def head():
    """The head on its own canvas (36x30), rotated by the caller."""
    im = Image.new("L", (36, 30), CLEAR)
    d = ImageDraw.Draw(im)
    d.ellipse((4, 0, 31, 26), fill=SKIN, outline=BLACK)  # the skull, taller than wide
    # the crack down the forehead, with a white gap
    pts = [(17, 1), (19, 4), (16, 7), (19, 10), (17, 13)]
    d.line(pts, fill=BLACK, width=3)
    d.line(pts, fill=BG, width=1)
    # brows: heavy and not level
    d.line((7, 8, 14, 11), fill=BLACK, width=2)
    d.line((22, 11, 29, 6), fill=BLACK, width=2)
    # the left eye: large, black, with a white fleck; the right eye: small and wrong
    d.ellipse((7, 11, 15, 19), fill=BLACK)
    d.point((10, 13), fill=BG)
    d.point((11, 13), fill=BG)
    d.ellipse((22, 13, 27, 17), fill=BLACK)
    d.point((24, 14), fill=BG)
    # a nose that is only a slit
    d.line((18, 16, 18, 18), fill=BLACK, width=1)

    def up(x):
        return 18 + 4 * (1 - ((x - 18) / 16.0) ** 2)

    def lo(x):
        return 23 + 4 * (1 - ((x - 18) / 16.0) ** 2)

    # the grin: a black lens from ear to ear, white teeth in two rows
    xs = range(2, 35)
    d.polygon([(x, round(up(x))) for x in xs] + [(x, round(lo(x))) for x in reversed(xs)], fill=BLACK)
    for x in range(5, 32, 2):
        d.line((x, round(up(x)) + 1, x, round(up(x)) + 2), fill=BG)
    for x in range(6, 31, 2):
        d.line((x, round(lo(x)) - 2, x, round(lo(x)) - 1), fill=BG)
    return im


def limb(d, pts, w=4):
    """A thin limb with an outline: black stroke, skin stroke on top."""
    d.line(pts, fill=BLACK, width=w)
    d.line(pts, fill=SKIN, width=max(1, w - 2))


def fingers(d, x, y, dirs):
    for dx, dy in dirs:
        d.line((x, y, x + dx, y + dy), fill=BLACK, width=1)


def draw():
    im = Image.new("P", (W, H), BG)
    d = ImageDraw.Draw(im)
    # the robe: shoulders at y 29, ragged hem in strips at the bottom
    robe = [(15, 30), (28, 26), (41, 30), (46, 42), (50, 55), (44, 52), (41, 55), (36, 51), (32, 55), (27, 51), (23, 55), (18, 52), (13, 55), (9, 52), (6, 55), (10, 42)]
    d.polygon(robe, fill=CLOTH, outline=BLACK)
    for x0, x1, y0 in ((20, 17, 34), (25, 24, 35), (31, 32, 35), (36, 39, 34)):
        d.line((x0, y0, x1, 52), fill=BLACK, width=1)
    # the chest shows through a deep V
    d.polygon([(23, 28), (33, 28), (28, 40)], fill=SKIN, outline=BLACK)
    for y in (31, 34, 37):  # ribs
        d.line((25 + (y - 31) // 3, y, 31 - (y - 31) // 3, y), fill=BLACK)
    # the neck, long and thin (the head hides its top)
    d.rectangle((26, 20, 30, 28), fill=SKIN, outline=BLACK)
    # the second pair of hands, folded at the waist (drawn before the long arms)
    limb(d, [(17, 36), (22, 43), (27, 46)], 4)
    limb(d, [(39, 36), (34, 43), (29, 46)], 4)
    d.ellipse((25, 43, 31, 49), fill=SKIN, outline=BLACK)
    for x in (25, 27, 29, 31):
        d.line((x, 48, x + 1, 52), fill=BLACK)
    # the long arms: down and out, hands with long fingers
    limb(d, [(15, 32), (9, 41), (6, 49)], 4)
    fingers(d, 6, 49, [(-3, 4), (-1, 6), (1, 6), (3, 5), (4, 3)])
    limb(d, [(41, 32), (47, 39), (52, 46)], 4)
    fingers(d, 52, 46, [(-1, 6), (1, 6), (3, 5), (4, 3), (4, 0)])
    # hair: strands that hang from the skull past the shoulders
    for x0, x1, y1 in ((15, 11, 44), (18, 15, 49), (39, 43, 42), (36, 41, 50)):
        d.line((x0, 8, x1, y1), fill=BLACK, width=1)
    # the head, rotated a little, on the neck
    hd = head().rotate(8, resample=Image.NEAREST, expand=False, fillcolor=CLEAR)
    px = im.load()
    hp = hd.load()
    for y in range(hd.size[1]):
        for x in range(hd.size[0]):
            if hp[x, y] != CLEAR and 0 <= x + 10 < W and 0 <= y - 1 < H:
                px[x + 10, y - 1] = hp[x, y]
    # bands of rows knocked sideways
    rng = random.Random("finnegan")
    for (y0, y1, dx) in ((10, 11, 3), (22, 23, -3), (36, 38, 2), (45, 45, -4), (50, 52, 3)):
        for y in range(y0, y1 + 1):
            row = [px[x, y] for x in range(W)]
            for x in range(W):
                px[x, y] = row[(x - dx) % W] if 0 <= x - dx < W else BG
    # scanline gaps in the robe
    for y in (40, 44, 48):
        for x in range(8, 49):
            if px[x, y] == CLOTH:
                px[x, y] = BG
    # a little bad data around the edges
    for _ in range(9):
        x, y = rng.randrange(2, 52), rng.randrange(4, 52)
        if px[x, y] == BG and (x < 12 or x > 44):
            px[x, y] = BLACK
            px[x + 1, y] = BLACK
    return im


def portrait(path, colors):
    """colors: [(r,g,b)] for indices 0..3 (white, skin, cloth, black), as portraits.py builds them."""
    im = draw()
    flat = []
    for c in colors:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(path)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "finnegan.png"
    im = draw()
    pal = [(255, 255, 255), (240, 190, 150), (60, 100, 200), (0, 0, 0)]
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.convert("RGB").resize((W * 8, H * 8), Image.NEAREST).save(out)
