"""Tileset builder: draw 32x32 blocks in code, pack them into a Crystal tileset.

A block is a 32x32 canvas of color indices 0-3 plus a palette slot per 8x8 cell (a tile has one slot, so a cell may only use
that slot's four colors).  pack() removes duplicate tiles (same pixels, same slot), assigns tile ids (0x00-0x5f in VRAM bank 0,
0x80-0xdf in bank 1) and writes the tileset png, the metatile table, the collision table and the palette map.

Palette convention of the custom outdoor sets (art/areapal.py): index 0 is the BASE color shared by every slot, so a cell of any
slot can hold plain wall or ground; indices 1-3 are the slot's accents and index 3 is the shared outline."""
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF, TEXT = range(8)
SLOT_NAMES = ["GRAY", "RED", "GREEN", "WATER", "YELLOW", "BROWN", "ROOF", "TEXT"]

TILE_IDS = list(range(0x00, 0x60)) + list(range(0x80, 0xE0))


class Canvas:
    def __init__(self, w=32, h=32, slot=GRAY):
        self.w, self.h = w, h
        self.p = [0] * (w * h)
        self.s = [[slot] * (w // 8) for _ in range(h // 8)]
        self.touched = set()  # (cell x, cell y) -> slots it was drawn with, checked in pack()
        self.drawn = {}

    # -- slots
    def slot(self, x, y, w, h, s):
        """Give the cells overlapped by the pixel rectangle the slot s."""
        for cy in range(y // 8, (y + h - 1) // 8 + 1):
            for cx in range(x // 8, (x + w - 1) // 8 + 1):
                self.s[cy][cx] = s

    def cell(self, cx, cy, s, cw=1, ch=1):
        for yy in range(cy, cy + ch):
            for xx in range(cx, cx + cw):
                self.s[yy][xx] = s

    def all_slot(self, s):
        for row in self.s:
            for i in range(len(row)):
                row[i] = s

    # -- drawing
    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c is not None:
            self.p[y * self.w + x] = c

    def get(self, x, y):
        return self.p[y * self.w + x]

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def box(self, x, y, w, h, c):
        self.hline(x, y, w, c)
        self.hline(x, y + h - 1, w, c)
        self.vline(x, y, h, c)
        self.vline(x + w - 1, y, h, c)

    def hline(self, x, y, w, c):
        for xx in range(x, x + w):
            self.set(xx, y, c)

    def vline(self, x, y, h, c):
        for yy in range(y, y + h):
            self.set(x, yy, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r + r // 2:
                    self.set(xx, yy, c)

    def ring(self, cx, cy, r, c):
        for yy in range(cy - r - 1, cy + r + 2):
            for xx in range(cx - r - 1, cx + r + 2):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if r * r - r <= d <= r * r + r:
                    self.set(xx, yy, c)

    def dither(self, x, y, w, h, a, b, phase=0):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, a if (xx + yy + phase) % 2 == 0 else b)

    def stamp(self, x, y, art, legend=None, clear=False):
        """ASCII art: digits are color indices, '.' is transparent (or index 0 when clear)."""
        for dy, row in enumerate(art):
            for dx, ch in enumerate(row):
                if ch == ".":
                    if clear:
                        self.set(x + dx, y + dy, 0)
                    continue
                v = legend[ch] if legend and ch in legend else int(ch)
                self.set(x + dx, y + dy, v)

    def paste(self, other, x, y):
        for yy in range(other.h):
            for xx in range(other.w):
                self.set(x + xx, y + yy, other.p[yy * other.w + xx])

    def text(self, x, y, s, c, gap=1):
        for ch in s:
            g = FONT.get(ch.upper())
            if g is None:
                x += 3
                continue
            for dy, row in enumerate(g):
                for dx, v in enumerate(row):
                    if v == "#":
                        self.set(x + dx, y + dy, c)
            x += len(g[0]) + gap
        return x

    def text_width(self, s, gap=1):
        return sum((len(FONT[ch.upper()][0]) if ch.upper() in FONT else 3) + gap for ch in s) - gap


FONT = {
    "A": ["###", "# #", "###", "# #", "# #"], "B": ["## ", "# #", "## ", "# #", "## "],
    "C": ["###", "#  ", "#  ", "#  ", "###"], "D": ["## ", "# #", "# #", "# #", "## "],
    "E": ["###", "#  ", "## ", "#  ", "###"], "F": ["###", "#  ", "## ", "#  ", "#  "],
    "G": ["###", "#  ", "# #", "# #", "###"], "H": ["# #", "# #", "###", "# #", "# #"],
    "I": ["###", " # ", " # ", " # ", "###"], "J": ["  #", "  #", "  #", "# #", "###"],
    "K": ["# #", "# #", "## ", "# #", "# #"], "L": ["#  ", "#  ", "#  ", "#  ", "###"],
    "M": ["# #", "###", "###", "# #", "# #"], "N": ["###", "# #", "# #", "# #", "# #"],
    "O": ["###", "# #", "# #", "# #", "###"], "P": ["###", "# #", "###", "#  ", "#  "],
    "Q": ["###", "# #", "# #", "###", "  #"], "R": ["###", "# #", "## ", "# #", "# #"],
    "S": ["###", "#  ", "###", "  #", "###"], "T": ["###", " # ", " # ", " # ", " # "],
    "U": ["# #", "# #", "# #", "# #", "###"], "V": ["# #", "# #", "# #", "# #", " # "],
    "W": ["# #", "# #", "###", "###", "# #"], "X": ["# #", "# #", " # ", "# #", "# #"],
    "Y": ["# #", "# #", " # ", " # ", " # "], "Z": ["###", "  #", " # ", "#  ", "###"],
    "0": ["###", "# #", "# #", "# #", "###"], "1": [" # ", "## ", " # ", " # ", "###"],
    "2": ["###", "  #", "###", "#  ", "###"], "3": ["###", "  #", "###", "  #", "###"],
    "4": ["# #", "# #", "###", "  #", "  #"], "5": ["###", "#  ", "###", "  #", "###"],
    "6": ["###", "#  ", "###", "# #", "###"], "7": ["###", "  #", "  #", " # ", " # "],
    "8": ["###", "# #", "###", "# #", "###"], "9": ["###", "# #", "###", "  #", "###"],
    "%": ["# #", "  #", " # ", "#  ", "# #"], "$": ["###", "## ", " ##", "###", " # "],
    ".": [" ", " ", " ", " ", "#"], "!": ["#", "#", "#", " ", "#"], "?": ["###", "  #", " ##", "   ", " # "],
    "-": ["   ", "   ", "###", "   ", "   "], "+": ["   ", " # ", "###", " # ", "   "],
    ":": [" ", "#", " ", "#", " "], "'": ["#", "#", " ", " ", " "],
}

COLL_NAMES = None


class Tileset:
    def __init__(self, name, const, stem):
        self.name, self.const, self.stem = name, const, stem  # "Tithe", "TILESET_TITHE", "tithe"
        self.blocks = []  # (Canvas, (c0, c1, c2, c3))
        self.pinned = {}  # tile id -> (slot, 8x8 pixels)
        self.roles = {}

    def add(self, canvas, coll="FLOOR", role=None):
        """coll: one name for all four quadrants, or a 4-tuple (TL, TR, BL, BR)."""
        if isinstance(coll, str):
            coll = (coll,) * 4
        self.blocks.append((canvas, coll))
        bid = len(self.blocks) - 1
        if role:
            self.roles.setdefault(role, []).append(bid)
        return bid

    def pin(self, tid, slot, pixels):
        self.pinned[tid] = (slot, tuple(pixels))

    def pack(self):
        # engine quirk (home/map.asm LoadMetatiles): block id 0 in a map is drawn as the border block, so block 0 of a
        # custom tileset has to be the border itself and the maps use border block 0
        assert self.roles.get("border", [None])[0] == 0, f"{self.name}: block 0 must be the border block"
        tiles = {}  # (slot, pixels) -> id
        order = []
        for tid, key in self.pinned.items():
            tiles[key] = tid
        free = [t for t in TILE_IDS if t not in self.pinned]
        meta = []
        for bi, (cv, coll) in enumerate(self.blocks):
            ids = []
            for cy in range(4):
                for cx in range(4):
                    px = tuple(cv.p[(cy * 8 + y) * cv.w + cx * 8 + x] for y in range(8) for x in range(8))
                    key = (cv.s[cy][cx], px)
                    if key not in tiles:
                        assert free, f"{self.name}: out of tiles at block {bi:02x}"
                        tiles[key] = free.pop(0)
                    ids.append(tiles[key])
            meta.append(ids)
        self.tiles = tiles
        self.meta = meta
        self.used = len(tiles)
        return self

    # -- files
    def write(self, root=ROOT):
        stem = self.stem
        im = Image.new("L", (128, 96), 255)  # 16 tiles per row, 12 rows = 192 tiles
        pm = {t: None for t in TILE_IDS}
        for (slot, px), tid in self.tiles.items():
            idx = tid if tid < 0x60 else 96 + tid - 0x80
            tx, ty = idx % 16, idx // 16
            for y in range(8):
                for x in range(8):
                    im.putpixel((tx * 8 + x, ty * 8 + y), 255 - px[y * 8 + x] * 85)
            pm[tid] = slot
        im.save(os.path.join(root, f"gfx/tilesets/{stem}.png"))
        open(os.path.join(root, f"data/tilesets/{stem}_metatiles.bin"), "wb").write(
            bytes(b for ids in self.meta for b in ids))
        o = []
        for bi, (cv, coll) in enumerate(self.blocks):
            o.append(f"\ttilecoll {', '.join(coll)} ; {bi:02x}")
        open(os.path.join(root, f"data/tilesets/{stem}_collision.asm"), "w").write("\n".join(o) + "\n")
        lines = []
        for bank, base in ((0, 0x00), (1, 0x80)):
            for r in range(12):
                names = []
                for c in range(8):
                    s = pm[base + r * 8 + c]
                    names.append(SLOT_NAMES[0 if s is None else s])
                lines.append(f"\ttilepal {bank}, " + ", ".join(names))
            if bank == 0:
                lines.append("\nrept 16\n\tdb $ff\nendr\n")
        open(os.path.join(root, f"gfx/tilesets/{stem}_palette_map.asm"), "w").write("\n".join(lines) + "\n")


def _col(c):
    return (c[0] * 255 // 31, c[1] * 255 // 31, c[2] * 255 // 31)


def preview(ts, pals, out, scale=3, cols=8):
    """Render the packed blocks (from tile data, not from the canvases) with ids, to check packing and palettes."""
    from PIL import ImageDraw
    rev = {tid: key for key, tid in ts.tiles.items()}
    n = len(ts.meta)
    rows = (n + cols - 1) // cols
    im = Image.new("RGB", (cols * 34, rows * 42), (40, 40, 40))
    dr = ImageDraw.Draw(im)
    for b, ids in enumerate(ts.meta):
        cx, cy = (b % cols) * 34, (b // cols) * 42
        for i, tid in enumerate(ids):
            slot, px = rev[tid]
            for y in range(8):
                for x in range(8):
                    im.putpixel((cx + 1 + (i % 4) * 8 + x, cy + 9 + (i // 4) * 8 + y), _col(pals[slot][px[y * 8 + x]]))
        dr.text((cx + 2, cy), f"{b:02x}", fill=(255, 255, 0))
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(out)
