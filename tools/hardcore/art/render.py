#!/usr/bin/env python3
"""Static renderer for tilesets and maps (no emulator): block sheets with ids, whole maps, with the area palettes.

usage:
  render.py blocks TILESET_JOHTO_MODERN AREA1 out.png     all blocks of a tileset with their ids
  render.py map TithePlaza1 out.png                       whole map (area palettes for area maps)
  render.py tiles TILESET_JOHTO_MODERN AREA1 out.png      raw tiles with ids
"""
import os
import re
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
import areapal  # noqa: E402

CUSTOM_TILESETS = {"TILESET_TITHE", "TILESET_GROVE", "TILESET_AXIOM", "TILESET_LOTUS", "TILESET_DIS"}
SLOT = {n: i for i, n in enumerate(["GRAY", "RED", "GREEN", "WATER", "YELLOW", "BROWN", "ROOF", "TEXT"])}


def rd(p):
    return open(os.path.join(ROOT, p)).read()


def camel(const):
    return "".join(w.title() for w in const.replace("TILESET_", "").split("_"))


def parse_includes(path, kind):
    """label -> first INCBIN/INCLUDE path after it."""
    out = {}
    pending = []
    for l in rd(path).splitlines():
        m = re.match(r"^(\w+)::?\s*$", l)
        if m:
            pending.append(m[1])
            continue
        m = re.match(r'^\s*(?:INCBIN|INCLUDE)\s+"([^"]+)"', l)
        if m:
            for p in pending:
                out[p] = m[1]
            pending = []
    return out


_GFX = parse_includes("gfx/tilesets.asm", "gfx")
_GFX.update(parse_includes("gfx/area_tilesets.asm", "gfx"))
_PALMAP = parse_includes("gfx/tileset_palette_maps.asm", "pal")


def tileset_files(const):
    c = camel(const)
    gfx = _GFX[f"Tileset{c}GFX"].replace(".2bpp.lz", ".png").replace(".2bpp", ".png")
    meta = _GFX[f"Tileset{c}Meta"]
    pm = _PALMAP[f"Tileset{c}PalMap"]
    return gfx, meta, pm


def load_tiles(png):
    im = Image.open(os.path.join(ROOT, png)).convert("L")
    w, h = im.size
    tiles = []
    for ty in range(h // 8):
        for tx in range(w // 8):
            t = []
            for y in range(8):
                for x in range(8):
                    v = im.getpixel((tx * 8 + x, ty * 8 + y))
                    t.append(3 - min(3, v // 64))
            tiles.append(t)
    return tiles


def load_palmap(path):
    """list of 256 slots (None for unused): ids 0x00-0x5f then 0x80-0xdf."""
    out = [None] * 256
    base = {0: 0x00, 1: 0x80}
    ids = {0: 0, 1: 0}
    for l in rd(path).splitlines():
        m = re.match(r"\s*tilepal\s+(\d),\s*(.*)", l)
        if not m:
            continue
        bank = int(m[1])
        for name in [x.strip() for x in m[2].split(",")]:
            out[base[bank] + ids[bank]] = SLOT[name]
            ids[bank] += 1
    return out


def tile_index(tid):
    """png tile index for a tile id used in a block."""
    if tid < 0x60:
        return tid
    if 0x80 <= tid < 0xE0:
        return 96 + tid - 0x80
    return None


def parse_pal_file(path):
    pals = []
    for l in rd(path).splitlines():
        m = re.match(r"\s*RGB\s+(.*?)\s*(;.*)?$", l)
        if m:
            v = [int(x) for x in m[1].replace(" ", "").split(",")]
            pals.append([tuple(v[i:i + 3]) for i in range(0, 12, 3)])
    return pals


def vanilla_set(indoor=False):
    pals = parse_pal_file("gfx/tilesets/bg_tiles.pal")
    start = 0x20 if indoor else 0x08
    return [pals[start + i] for i in range(8)]


def pal_for(area, indoor, kind=None):
    """kind: 'out' (custom outdoor tileset), 'road' (vanilla outdoor tiles) or 'inn'; default by indoor."""
    if area in areapal.AREAS:
        kind = kind or ("inn" if indoor else "out")
        src = areapal.outset(area) if kind == "out" else areapal.AREAS[area][kind]
        return [list(p) for p in src]
    return vanilla_set(indoor)


def col(c):
    return (c[0] * 255 // 31, c[1] * 255 // 31, c[2] * 255 // 31)


class Tileset:
    def __init__(self, const):
        self.const = const
        gfx, meta, pm = tileset_files(const)
        self.tiles = load_tiles(gfx)
        self.meta = open(os.path.join(ROOT, meta), "rb").read()
        self.palmap = load_palmap(pm)
        self.gfx = gfx

    def blocks(self):
        return len(self.meta) // 16

    def draw_tile(self, im, x, y, tid, pals):
        i = tile_index(tid)
        if i is None or i >= len(self.tiles):
            return
        slot = self.palmap[tid] if self.palmap[tid] is not None else 0
        pal = pals[slot]
        t = self.tiles[i]
        px = im.load()
        for yy in range(8):
            for xx in range(8):
                px[x + xx, y + yy] = col(pal[t[yy * 8 + xx]])

    def draw_block(self, im, x, y, b, pals):
        d = self.meta[b * 16:(b + 1) * 16]
        for i, tid in enumerate(d):
            self.draw_tile(im, x + (i % 4) * 8, y + (i // 4) * 8, tid, pals)


def render_blocks(const, area, out, indoor=False, scale=2):
    ts = Tileset(const)
    pals = pal_for(area, indoor)
    n = ts.blocks()
    cols = 16
    rows = (n + cols - 1) // cols
    im = Image.new("RGB", (cols * 34, rows * 42), (40, 40, 40))
    dr = ImageDraw.Draw(im)
    for b in range(n):
        cx, cy = (b % cols) * 34, (b // cols) * 42
        tmp = Image.new("RGB", (32, 32))
        ts.draw_block(tmp, 0, 0, b, pals)
        im.paste(tmp, (cx + 1, cy + 9))
        dr.text((cx + 2, cy), f"{b:02x}", fill=(255, 255, 0))
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(out)


def render_tiles(const, area, out, indoor=False, scale=3):
    ts = Tileset(const)
    pals = pal_for(area, indoor)
    im = Image.new("RGB", (16 * 10, 12 * 2 * 10 + 20), (40, 40, 40))
    dr = ImageDraw.Draw(im)
    ids = list(range(0x60)) + list(range(0x80, 0xE0))
    for k, tid in enumerate(ids):
        cx, cy = (k % 16) * 10, (k // 16) * 10 + (0 if k < 96 else 4)
        tmp = Image.new("RGB", (8, 8))
        ts.draw_tile(tmp, 0, 0, tid, pals)
        im.paste(tmp, (cx + 1, cy + 1))
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(out)


def area_of(group):
    return group if group in areapal.AREAS else None


def map_info(name):
    """(tileset const, env, width, blk bytes, area key or None)."""
    from areamodel import load
    maps = load()
    mp = maps[name] if isinstance(maps, dict) else next(m for m in maps if m.name == name)
    env = "TOWN"
    area = None
    for l in rd("data/maps/area_map_lists.asm").splitlines():
        m = re.match(rf"\s*map {name}, (\w+), (\w+),", l)
        if m:
            env = m[2]
    for key in areapal.AREAS:
        pass
    return mp, env


def render_map(name, out, scale=2, area=None, indoor=None):
    sys.path.insert(0, os.path.dirname(HERE))
    mp, env = map_info(name)
    if indoor is None:
        indoor = env not in ("TOWN", "ROUTE")
    if area is None:
        m = re.search(r"^(Tithe|Grove|Axiom|Lotus|Dis)", name)
        area = {"Tithe": "AREA1", "Grove": "AREA2", "Axiom": "AREA3", "Lotus": "AREA4", "Dis": "AREA5"}.get(m[1]) if m else None
    ts = Tileset(mp.tileset)
    custom = mp.tileset in CUSTOM_TILESETS
    pals = pal_for(area, indoor, "out" if custom else ("road" if not indoor else "inn"))
    w = mp.w
    h = mp.h
    im = Image.new("RGB", (w * 32, h * 32))
    for i, b in enumerate(mp.blocks):
        ts.draw_block(im, (i % w) * 32, (i // w) * 32, b, pals)
    im = im.resize((im.width * scale // 2 if scale >= 2 else im.width, im.height * scale // 2 if scale >= 2 else im.height), Image.NEAREST) if scale != 2 else im
    im.save(out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "blocks":
        render_blocks(sys.argv[2], sys.argv[3] if sys.argv[3] != "-" else None, sys.argv[4])
    elif cmd == "tiles":
        render_tiles(sys.argv[2], sys.argv[3] if sys.argv[3] != "-" else None, sys.argv[4])
    elif cmd == "map":
        render_map(sys.argv[2], sys.argv[3])
