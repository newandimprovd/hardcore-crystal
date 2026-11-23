#!/usr/bin/env python3
"""The world map of the Pokegear (and of every Town Map): one stylised picture for the whole game.

Bruno (Nick) hands the player this map, so there is exactly one world: a ring road around the mountain of
PURGATORIO, walked from the south-east corner (NEW BARK) west along the south coast through TITHE, up the west
coast through the GROVE, east along the north coast through AXIOM and LOTUS, and down the east coast to DIS.

This script owns three things and writes them all deterministically:
  gfx/pokegear/johto.bin, kanto.bin   the 20x18 tilemap (both Pokegear pages show the same world)
  gfx/pokegear/town_map.png           tiles 44..47 become the label "WORLD"
  the pixel coordinates of every landmark (ORDER below; gen_areas.py asks for them through `coords()`)
and optionally a preview PNG that uses the real palettes:  python3 tools/hardcore/world_map.py --preview out.png
"""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# (tile column, tile row, marker): marker "sq" = city square, "dot" = point of interest.  Order = cursor order
# (pressing Up walks forward through this list, Down backward).
ORDER = [
    ("TITHE_JUNCTION", 10, 14, "dot"),
    ("TITHE_ROAD", 8, 14, "dot"),
    ("TITHE_CITY", 6, 14, "sq"),
    ("TITHE_MIDTOWN", 4, 14, "sq"),
    ("TITHE_PARISH", 3, 12, "sq"),
    ("GROVE_COMMUNE", 3, 10, "sq"),
    ("GROVE_ORCHARD", 3, 8, "dot"),
    ("GROVE_HEARTH", 3, 6, "sq"),
    ("AXIOM_OUTSKIRTS", 5, 3, "dot"),
    ("AXIOM_CENTRAL", 8, 3, "sq"),
    ("AXIOM_MAYORALTY", 11, 3, "sq"),
    ("LOTUS_COAST", 14, 3, "sq"),
    ("LOTUS_BOARDWALK", 16, 5, "dot"),
    ("LOTUS_MANSION", 16, 7, "sq"),
    ("DIS_CITY", 16, 9, "sq"),
    ("DIS_COCYTUS", 16, 11, "dot"),
    ("DIS_JUDECCA", 14, 12, "sq"),
    ("THE_ABYSS", 10, 11, "dot"),
    ("PURGATORIO", 10, 8, "dot"),
    ("NICKS_LANDING", 10, 5, "sq"),
    ("UNDERCROFT", 8, 5, "dot"),
]
# the three starting places of the vanilla Johto page (their rows in data/maps/landmarks.asm are patched)
START = [("NewBarkTownName", 16, 14, "sq"), ("Route29Name", 14, 14, "dot"), ("CherrygroveCityName", 12, 14, "sq")]

# the ring road (list of waypoints, drawn with straight Manhattan legs) and the spurs
RING = [(16, 14), (3, 14), (3, 3), (16, 3), (16, 14)]
SPURS = [[(10, 14), (10, 5)], [(16, 11), (14, 11), (14, 12)]]
LAKE = [(14, 9), (15, 9), (14, 10), (15, 10)]

# tiles
SEA, SEA2 = 24, 25
LAND = 17
COAST = {"N": 1, "S": 33, "W": 16, "E": 18, "NW": 0, "NE": 2, "SW": 32, "SE": 34}
MTN = 20
MTN_EDGE = {"N": 4, "S": 36, "W": 19, "E": 21, "NW": 3, "NE": 5, "SW": 35, "SE": 37}
ROAD = 26
SQ, DOT_ROAD, DOT_MTN, DOT_SEA, DOT_LAND = 10, 12, 13, 14, 15
LABEL = (44, 45, 46, 47)

W, H = 20, 18


def landmask():
    """Interior cells (cols 1..18, rows 1..16) -> 'sea' | 'land' | 'mtn'.  The continent is the rectangle that holds the
    ring road with one cell of shore around it, a few bulges for character, and the mountain of Purgatorio inside."""
    t = {(c, r): "sea" for c in range(1, 19) for r in range(1, 17)}
    for r in range(2, 16):
        for c in range(2, 18):
            t[(c, r)] = "land"
    for cell in [(2, 2), (17, 2), (2, 15), (17, 15)]:  # round the corners
        t[cell] = "sea"
    for cell in [(1, 7), (1, 8), (1, 9), (18, 5), (18, 6), (7, 16), (8, 16), (9, 16), (10, 16), (12, 1), (13, 1)]:  # bulges
        t[cell] = "land"
    for r in range(5, 13):  # the mountain: a chamfered block
        for c in range(6, 14):
            if r in (5, 12) and c in (6, 13):
                continue
            t[(c, r)] = "mtn"
    for cell in LAKE:
        t[cell] = "sea"
    return t


def legs(points):
    cells = []
    for (c0, r0), (c1, r1) in zip(points, points[1:]):
        if c0 == c1:
            step = 1 if r1 >= r0 else -1
            cells += [(c0, r) for r in range(r0, r1 + step, step)]
        else:
            assert r0 == r1, (points,)
            step = 1 if c1 >= c0 else -1
            cells += [(c, r0) for c in range(c0, c1 + step, step)]
    return cells


def build():
    """-> (list of 360 tile numbers, mask dict)."""
    t = landmask()
    road = set(legs(RING))
    for sp in SPURS:
        road |= set(legs(sp))
    marks = {(c, r): m for _, c, r, m in ORDER}
    marks.update({(c, r): m for _, c, r, m in START})
    for cell in road | set(marks):
        assert t[cell] in ("land", "mtn"), f"road/marker on water at {cell}"
    tiles = [LAND] * (W * H)

    def put(c, r, v):
        tiles[r * W + c] = v

    # the frame, exactly as in the original
    for c in range(W):
        put(c, 0, 7)
        put(c, 17, 7)
    for r in range(18):
        put(0, r, 22)
        put(19, r, 22)
    put(0, 0, 6)
    put(19, 0, 23)
    put(0, 17, 38)
    put(19, 17, 39)

    def is_land(c, r):
        return t.get((c, r), "sea") != "sea"

    def is_mtn(c, r):
        return t.get((c, r), "sea") == "mtn"

    for (c, r), kind in t.items():
        if kind == "sea":
            put(c, r, SEA2 if (c * 7 + r * 3) % 11 == 0 else SEA)
            continue
        if kind == "mtn":
            n, s, w, e = (not is_mtn(c, r - 1), not is_mtn(c, r + 1), not is_mtn(c - 1, r), not is_mtn(c + 1, r))
        else:
            n, s, w, e = (not is_land(c, r - 1), not is_land(c, r + 1), not is_land(c - 1, r), not is_land(c + 1, r))
        table = MTN_EDGE if kind == "mtn" else COAST
        plain = MTN if kind == "mtn" else LAND
        tile = plain
        if n and w:
            tile = table["NW"]
        elif n and e:
            tile = table["NE"]
        elif s and w:
            tile = table["SW"]
        elif s and e:
            tile = table["SE"]
        elif n:
            tile = table["N"]
        elif s:
            tile = table["S"]
        elif w:
            tile = table["W"]
        elif e:
            tile = table["E"]
        put(c, r, tile)
    for (c, r) in road:
        put(c, r, ROAD)
    for (c, r), m in marks.items():
        if m == "sq":
            put(c, r, SQ)
        else:
            put(c, r, DOT_ROAD if (c, r) in road else (DOT_MTN if t[(c, r)] == "mtn" else DOT_LAND))
    for i, v in enumerate(LABEL):
        put(1 + i, 16, v)
    return tiles, t


def coords():
    """{CONST: (x, y)} in the pixel units of data/maps/landmarks.asm (the centre of the tile)."""
    return {k: (c * 8 + 4, r * 8 + 4) for k, c, r, _ in ORDER}


def write_bins(tiles):
    data = bytes(tiles) + b"\xff"
    for name in ("johto.bin", "kanto.bin"):
        with open(os.path.join(ROOT, "gfx", "pokegear", name), "wb") as f:
            f.write(data)


FONT = {
    "W": ["X...X", "X...X", "X.X.X", "X.X.X", "XX.XX", "X...X"],
    "O": [".XXX.", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "R": ["XXXX.", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
    "L": ["X....", "X....", "X....", "X....", "X....", "XXXXX"],
    "D": ["XXXX.", "X...X", "X...X", "X...X", "X...X", "XXXX."],
}


def write_label(word="WORLD"):
    from PIL import Image
    path = os.path.join(ROOT, "gfx", "pokegear", "town_map.png")
    im = Image.open(path).convert("L")
    x0 = 44 % 16 * 8  # tiles 44..47 sit in row 2 of the sheet
    y0 = 44 // 16 * 8
    for y in range(8):
        for x in range(32):
            im.putpixel((x0 + x, y0 + y), 255)
    x = 1
    for ch in word:
        for dy, row in enumerate(FONT[ch]):
            for dx, v in enumerate(row):
                if v == "X":
                    im.putpixel((x0 + x + dx, y0 + 1 + dy), 0)
        x += 6
    im.save(path)


def patch_start_landmarks():
    path = os.path.join(ROOT, "data", "maps", "landmarks.asm")
    s = open(path).read()
    for label, c, r, _ in START:
        s, n = re.subn(r"(\tlandmark\s+)\d+,\s*\d+(,\s*" + label + r"\b)", lambda m: f"{m.group(1)}{c * 8 + 4:3d}, {r * 8 + 4:3d}{m.group(2)}", s)
        assert n == 1, label
    open(path, "w").write(s)


def preview(tiles, out, scale=3):
    from PIL import Image
    sheet = Image.open(os.path.join(ROOT, "gfx", "pokegear", "town_map.png")).convert("L")
    pals = {0: [(28, 31, 20), (21, 21, 21), (13, 13, 13), (0, 0, 0)],
            1: [(28, 31, 20), (0, 31, 0), (0, 0, 31), (0, 0, 0)],
            2: [(28, 31, 20), (0, 31, 0), (15, 7, 0), (0, 0, 0)],
            3: [(28, 31, 20), (31, 15, 0), (15, 7, 0), (0, 0, 0)],
            4: [(28, 31, 20), (0, 31, 0), (0, 0, 31), (31, 0, 0)],
            5: [(28, 31, 20), (0, 31, 0), (15, 7, 0), (31, 0, 0)]}
    # tile -> palette, as in gfx/pokegear/town_map_palette_map.asm (E=1 M=2 C=3 P=4 PM=5 B=0)
    names = ("E E E M M M B B E E C E P PM P PM E E E M M M B B E E B E E B B B "
             "E E E M M M B B B B B B B B B B B B B B B B B B").split()
    key = {"B": 0, "E": 1, "M": 2, "C": 3, "P": 4, "PM": 5}
    pal_of = [key[n] for n in names][:48]
    order = sorted(set(sheet.getdata()), reverse=True)
    lvl = {v: i for i, v in enumerate(order)}
    out_im = Image.new("RGB", (W * 8, H * 8))
    for i, t in enumerate(tiles):
        tx, ty = t % 16, t // 16
        pal = pals[pal_of[t]] if t < len(pal_of) else pals[0]
        for y in range(8):
            for x in range(8):
                p = lvl[sheet.getpixel((tx * 8 + x, ty * 8 + y))]
                col = tuple(v * 255 // 31 for v in pal[p])
                out_im.putpixel(((i % W) * 8 + x, (i // W) * 8 + y), col)
    # the cursor positions
    for k, (x, y) in coords().items():
        for d in range(-1, 2):
            for e in range(-1, 2):
                if abs(d) + abs(e) == 1 or (d == 0 and e == 0):
                    pass
    out_im = out_im.resize((W * 8 * scale, H * 8 * scale), Image.NEAREST)
    out_im.save(out)


def main():
    tiles, _ = build()
    if "--preview" in sys.argv:
        write_label()
        preview(tiles, sys.argv[sys.argv.index("--preview") + 1])
        return
    write_bins(tiles)
    write_label()
    patch_start_landmarks()


if __name__ == "__main__":
    main()
