"""Tall-grass blocks for the five area tilesets: one original grass look per area (a block is 32x32 px, 4x4 tiles of 8x8).

Wild encounters happen on blocks with TALL_GRASS collision.  The engine puts the player sprite behind every BG pixel that is not
color 0 while it stands in grass, so the ground (index 0) shows through the gaps between blades and the blades hide the legs.
Every block uses the GREEN palette slot (index 1 tips, 2 blades, 3 shade) and a few cells of the second block borrow another slot
for a small detail (a can, a flower, a sensor, a hibiscus, an ember).

grass_pair(style) -> [dense block, block with detail]; both are role "grass" with TALL_GRASS collision."""
import random

from tilebuild import Canvas, GREEN, RED, WATER, YELLOW, GRAY


def _tile(cv, cx, cy, blades, flecks=()):
    """blades: (x, height, lean) with x in 0..7 and height in 1..8; they stand on the tile's bottom row.  lean shifts the top two
    pixels by -1 or +1 so tufts do not all point straight up."""
    ox, oy = cx * 8, cy * 8
    for x, h, lean in blades:
        for k in range(h):
            y = 7 - k
            px = x + (lean if k >= h - 2 and h > 3 else 0)
            col = 3 if k < 2 else (1 if k == h - 1 else 2)
            cv.set(ox + px % 8, oy + y, col)
    for x, y in flecks:
        cv.set(ox + x, oy + y, 3)


def _tiles(rng, n, count, hmin, hmax, lean, step=2):
    """n distinct tile recipes: `count` blades each, at spread columns."""
    out = []
    for _ in range(n):
        cols = sorted(rng.sample(range(8), count))
        blades = []
        last = -9
        for x in cols:
            if x - last < 1:
                continue
            blades.append((x, rng.randint(hmin, hmax), rng.choice(lean)))
            last = x
        out.append(blades)
    return out


# layout of the four tile recipes over the 4x4 cells of a block (indices into the recipe list)
LAYOUT = [[0, 1, 2, 3],
          [2, 3, 0, 1],
          [1, 0, 3, 2],
          [3, 2, 1, 0]]

STYLES = {
    # Tithe: a vacant lot, thin weeds and litter
    "tithe": dict(seed=11, count=6, hmin=4, hmax=7, lean=(-1, 0, 1), flecks=[(1, 3), (6, 5), (3, 2), (5, 1)]),
    # Grove: tall wild grass with seed heads
    "grove": dict(seed=23, count=5, hmin=5, hmax=8, lean=(-1, 0, 0, 1), flecks=[]),
    # Axiom: engineered turf, evenly spaced and all the same height
    "axiom": dict(seed=0, uniform=True),
    # Lotus: soft resort lawn, fronds in pairs
    "lotus": dict(seed=37, count=6, hmin=4, hmax=7, lean=(-1, 1), flecks=[], fronds=True),
    # Dis: dead spiky ash weed
    "dis": dict(seed=41, count=6, hmin=3, hmax=7, lean=(-1, 1, 1), flecks=[(2, 4), (6, 3)], jag=True),
}


def _recipes(style):
    st = STYLES[style]
    rng = random.Random(st["seed"])
    if st.get("uniform"):
        a = [(x, 6 if x % 2 else 5, 0) for x in range(8)]
        b = [(x, 5 if x % 2 else 6, 0) for x in range(8)]
        c = [(x, 7 if x % 4 == 1 else 5, 0) for x in range(8)]
        d = [(x, 7 if x % 4 == 3 else 5, 0) for x in range(8)]
        return [a, b, c, d], [[] for _ in range(4)]
    recs = _tiles(rng, 4, st["count"], st["hmin"], st["hmax"], st["lean"])
    if st.get("fronds"):
        # fronds: every second blade gets a lean away from its neighbor so the pair makes a V
        for r in recs:
            for i, (x, h, l) in enumerate(r):
                r[i] = (x, h, -1 if i % 2 == 0 else 1)
    if st.get("jag"):
        for r in recs:
            r[:] = [(x, h if i % 2 else max(2, h - 3), l) for i, (x, h, l) in enumerate(r)]
    return recs, [st["flecks"] if i % 2 == 0 else [] for i in range(4)]


def _dense(style):
    recs, flecks = _recipes(style)
    cv = Canvas(slot=GREEN)
    for cy in range(4):
        for cx in range(4):
            i = LAYOUT[cy][cx]
            _tile(cv, cx, cy, recs[i], flecks[i])
    return cv


def _detail(cv, style):
    """The cell at (2, 2) of the second block carries the area's small detail."""
    cx, cy = 2, 2
    ox, oy = cx * 8, cy * 8
    for y in range(8):
        for x in range(8):
            cv.set(ox + x, oy + y, 0)
    if style == "tithe":  # a crushed can in the weeds
        cv.cell(cx, cy, RED)
        cv.rect(ox + 2, oy + 5, 4, 2, 1)
        cv.hline(ox + 2, oy + 4, 4, 3)
        cv.set(ox + 3, oy + 5, 0)
        for x, h in ((0, 5), (7, 4), (1, 3)):
            cv.vline(ox + x, oy + 8 - h, h, 2)
            cv.set(ox + x, oy + 8 - h, 1)
    elif style == "grove":  # wildflowers
        cv.cell(cx, cy, YELLOW)
        for x in (1, 4, 6):
            cv.vline(ox + x, oy + 4, 4, 3)
        for x, y in ((1, 3), (4, 2), (6, 3)):
            cv.set(ox + x, oy + y, 1)
            cv.set(ox + x - 1, oy + y, 2)
            cv.set(ox + x + 1, oy + y, 2)
            cv.set(ox + x, oy + y - 1, 2)
    elif style == "axiom":  # a sensor blinking in the turf
        cv.cell(cx, cy, WATER)
        cv.rect(ox + 2, oy + 3, 4, 4, 3)
        cv.rect(ox + 3, oy + 4, 2, 2, 1)
        cv.set(ox + 3, oy + 4, 2)
        for x in (0, 7):
            cv.vline(ox + x, oy + 4, 4, 3)
    elif style == "lotus":  # a hibiscus
        cv.cell(cx, cy, RED)
        cv.disc(ox + 4, oy + 3, 2, 1)
        cv.set(ox + 4, oy + 3, 3)
        cv.set(ox + 4, oy + 2, 2)
        cv.vline(ox + 4, oy + 5, 3, 3)
        cv.hline(ox + 1, oy + 7, 6, 3)
    elif style == "dis":  # a bed of embers
        cv.cell(cx, cy, RED)
        for x, y in ((1, 6), (3, 5), (5, 6), (6, 4), (2, 3)):
            cv.set(ox + x, oy + y, 1)
        for x, y in ((1, 7), (3, 7), (5, 7), (4, 6), (6, 5), (2, 4)):
            cv.set(ox + x, oy + y, 2)
        for x in (0, 7):
            cv.vline(ox + x, oy + 3, 5, 3)
    return cv


def grass_pair(style):
    a = _dense(style)
    b = _detail(_dense(style), style)
    return [a, b]
