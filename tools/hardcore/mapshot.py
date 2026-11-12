#!/usr/bin/env python3
"""Render a map's blocks to a PNG (day palettes), to look at a generated map without running the game.

usage: mapshot.py MapName OUT.png [tileset-stem]
Reads maps/MapName.blk, the size from constants/map_constants.asm and the tileset from data/maps/attributes.asm, so it shows what the generator wrote."""
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocksheet import ROOT, load_coll, load_day_palettes, load_palmap, load_tiles, render_block  # noqa: E402

TS = {"TILESET_JOHTO": "johto", "TILESET_JOHTO_MODERN": "johto_modern", "TILESET_KANTO": "kanto"}


def stem_of(tileset):
    if tileset in TS:
        return TS[tileset]
    return tileset[len("TILESET_"):].lower()


def main():
    name, out = sys.argv[1], sys.argv[2]
    const = re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()
    src = open(os.path.join(ROOT, "constants/map_constants.asm")).read() + open(os.path.join(ROOT, "constants/area_map_constants.asm")).read()
    m = re.search(r"map_const\s+%s,\s*(\d+),\s*(\d+)" % const, src)
    assert m, f"no map_const for {const}"
    w, h = int(m[1]), int(m[2])
    path = os.path.join(ROOT, f"maps/gen/{name}.blk")
    if not os.path.exists(path):
        path = os.path.join(ROOT, f"maps/{name}.blk")
    if len(sys.argv) > 3:
        stem = sys.argv[3]
    else:
        stem = None
        for f in ("data/maps/maps.asm", "data/maps/area_map_lists.asm"):
            for l in open(os.path.join(ROOT, f)):
                r = re.match(r"\s*map\s+%s,\s*(TILESET_\w+)" % name, l)
                if r:
                    stem = stem_of(r[1])
        assert stem, "tileset not found; pass the stem"
    blk = open(path, "rb").read()
    assert len(blk) == w * h, (len(blk), w, h)
    meta = open(os.path.join(ROOT, f"data/tilesets/{stem}_metatiles.bin"), "rb").read()
    tiles, palmap, pals = load_tiles(stem), load_palmap(stem), load_day_palettes()
    img = Image.new("RGB", (w * 32, h * 32))
    cache = {}
    for y in range(h):
        for x in range(w):
            b = blk[y * w + x]
            if b not in cache:
                cache[b] = render_block(meta, b, tiles, palmap, pals)
            img.paste(cache[b], (x * 32, y * 32))
    img.save(out)
    print("wrote", out, w, "x", h, "blocks,", stem)


main()
