#!/usr/bin/env python3
"""Render every block of a tileset (day palettes) with its collision summary.

usage: blocksheet.py TILESET OUT.png [FIRST LAST]
TILESET is the file stem under data/tilesets (johto, johto_modern, kanto, ...).
Each cell shows the block id (hex) and the four collision types of its quadrants in the order
top-left top-right bottom-left bottom-right (F floor, W wall, G tall grass, w water, C cut tree,
S smashable rock, B boulder, D door, A warp, L ladder, P pc, K counter, other letters see ABBR).
Colours come from the palette map and the day palettes, so they match the game closely.
"""
import os
import re
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ABBR = {
    "FLOOR": "F", "WALL": "W", "TALL_GRASS": "G", "WATER": "w", "CUT_TREE": "C", "ROCK_SMASH?": "S",
    "DOOR": "D", "LADDER": "L", "PC": "P", "COUNTER": "K", "CAVE": "V", "WHIRLPOOL": "o", "BUOY": "b",
    "WATERFALL": "f", "ICE": "i", "WARP_CARPET_DOWN": "a", "WARP_CARPET_LEFT": "a", "WARP_CARPET_RIGHT": "a",
    "WARP_CARPET_UP": "a", "DIVE_WATER": "d", "SHORE_WATER": "w", "LAND_WATER?": "w", "BOOKSHELF": "h",
    "TV": "t", "TOWN_MAP": "m", "WINDOW": "n", "SIGNPOST": "s", "MAGAZINE_SHELF": "h", "INCENSE_BURNER": "u",
    "MART_SHELF": "r", "RADIO": "r", "BLACKOUT_STAIRS": "e", "TRASH_CAN": "x", "CUT_TREE_RIGHT": "C",
}

PAL = ["GRAY", "RED", "GREEN", "WATER", "YELLOW", "BROWN", "ROOF", "TEXT"]


def load_day_palettes():
    rows = []
    sec = None
    for l in open(os.path.join(ROOT, "gfx/tilesets/bg_tiles.pal")):
        if l.startswith("; "):
            sec = l[2:].strip()
        m = re.match(r"\s*RGB\s+(.*?)\s*;", l)
        if m and sec == "day":
            v = [int(x) for x in re.findall(r"\d+", m[1])]
            rows.append([tuple(round(c * 255 / 31) for c in v[i:i + 3]) for i in range(0, 12, 3)])
    return dict(zip(PAL, rows))


def load_tiles(stem):
    data = open(os.path.join(ROOT, f"gfx/tilesets/{stem}.2bpp"), "rb").read()
    tiles = []
    for t in range(len(data) // 16):
        px = []
        for y in range(8):
            lo, hi = data[t * 16 + y * 2], data[t * 16 + y * 2 + 1]
            px.append([((lo >> (7 - x)) & 1) | (((hi >> (7 - x)) & 1) << 1) for x in range(8)])
        tiles.append(px)
    return tiles


def load_palmap(stem):
    rows = []
    path = os.path.join(ROOT, f"gfx/tilesets/{stem}_palette_map.asm")
    if not os.path.exists(path):
        return None
    for l in open(path):
        m = re.match(r"\s*tilepal\s+(\d+),\s*(.*)", l)
        if m:
            rows.append((int(m[1]), [x.strip() for x in m[2].split(";")[0].split(",")]))
    return rows


def load_coll(stem):
    out = []
    for l in open(os.path.join(ROOT, f"data/tilesets/{stem}_collision.asm")):
        m = re.match(r"\s*tilecoll\s+(.*?)\s*;", l)
        if m:
            out.append([x.strip() for x in m[1].split(",")])
    return out


def tile_pixels(tiles, palmap, pals, t):
    # tile ids 0x00-0x5f come from the first half, 0x80-0xdf from the second half of the file
    if t < 0x60:
        idx, row = t, t // 8
    elif t >= 0x80:
        idx, row = 0x60 + (t - 0x80), 12 + (t - 0x80) // 8
    else:
        return None, None
    if idx >= len(tiles):
        return None, None
    name = "GRAY"
    if palmap and row < len(palmap):
        name = palmap[row][1][t % 8]
    return tiles[idx], pals.get(name, pals["GRAY"])


def render_block(meta, b, tiles, palmap, pals):
    im = Image.new("RGB", (32, 32), (255, 0, 255))
    for ty in range(4):
        for tx in range(4):
            t = meta[b * 16 + ty * 4 + tx]
            px, pal = tile_pixels(tiles, palmap, pals, t)
            if px is None:
                continue
            for y in range(8):
                for x in range(8):
                    im.putpixel((tx * 8 + x, ty * 8 + y), pal[px[y][x]])
    return im


def sheet(stem, out, first=0, last=None):
    meta = open(os.path.join(ROOT, f"data/tilesets/{stem}_metatiles.bin"), "rb").read()
    n = len(meta) // 16
    last = n - 1 if last is None else min(last, n - 1)
    tiles = load_tiles(stem)
    palmap = load_palmap(stem)
    pals = load_day_palettes()
    coll = load_coll(stem)
    ids = list(range(first, last + 1))
    cols = 8
    cw, ch = 72, 92
    rows = (len(ids) + cols - 1) // cols
    img = Image.new("RGB", (cols * cw, rows * ch), (40, 40, 40))
    d = ImageDraw.Draw(img)
    for i, b in enumerate(ids):
        x, y = (i % cols) * cw, (i // cols) * ch
        blk = render_block(meta, b, tiles, palmap, pals).resize((64, 64), Image.NEAREST)
        img.paste(blk, (x + 4, y + 2))
        c = coll[b] if b < len(coll) else ["?"] * 4
        ab = "".join(ABBR.get(v, "#") if not re.match(r"^[0-9a-fA-F]+$", v) else "?" for v in c)
        d.text((x + 4, y + 68), f"{b:02x} {ab[:2]}", fill=(255, 255, 0))
        d.text((x + 4, y + 79), f"   {ab[2:]}", fill=(255, 255, 0))
    img.save(out)
    # also print a text table
    return coll


if __name__ == "__main__":
    stem, out = sys.argv[1], sys.argv[2]
    f = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0
    l = int(sys.argv[4], 16) if len(sys.argv) > 4 else None
    sheet(stem, out, f, l)
    print("wrote", out)
