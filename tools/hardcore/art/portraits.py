"""Battle portraits (7x7 tiles, 56x56 px, 4 colors) of the area trainer classes: the cast recipe (art/cast.py) drawn as a full figure by
art/bigfig.py with the colorway of its area (art/areapal.py), so the overworld figure and the battle portrait are the same person.
Indexed png, palette order white, skin, cloth, black (the Makefile reads the .gbcpal from the png)."""
import os

from PIL import Image

import areapal
import bigfig

PAL_INDEX = {"RED": 0, "BLUE": 1, "GREEN": 2, "BROWN": 3, "PINK": 4}


def rgb8(c5):
    return tuple(v * 8 + v // 4 for v in c5)


def portrait(slug_rec, area, palname, path):
    pal = areapal.npc_set(area)[PAL_INDEX[palname]]
    px = bigfig.draw(slug_rec)
    im = Image.new("P", (56, 56), 0)
    colors = [(255, 255, 255), rgb8(pal[1]), rgb8(pal[2]), (0, 0, 0)]
    flat = []
    for c in colors:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    for y in range(56):
        for x in range(56):
            im.putpixel((x, y), int(px[y, x]))
    assert len({colors[1], colors[2]}) == 2 and colors[1] != colors[0] and colors[2] != colors[0]
    im.save(path)
