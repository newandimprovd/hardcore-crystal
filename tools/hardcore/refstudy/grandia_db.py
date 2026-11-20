#!/usr/bin/env python3
"""Static reader for Grandia's (GBC) world database, built from the game's own loader code.

Everything here was read from the loader routines in bank 00 ($1622 room, $12CC palette,
$12F9 tiles) and verified against live emulator state:
  * 162 of 162 tiles of area 47 match VRAM bank 1 byte for byte.
  * The palette buffer at WRAM $C10F matches the bank $82 set of the current area.

Tables (all keyed by area id, which is also the tileset id and the palette set id):
  bank $82 $4000  48 pointers to 40-byte BG palette sets (BG0..BG4, four RGB555 words each)
  bank $83 $4000  48 entries (tileset id, pointer to room list in bank $83)
  bank $F9 $4000  48 entries (tile count N, pointer; top 2 bits of the pointer are a bank offset
                  from $F9) to a list of N two-byte tile pointers. A tile pointer is 14 bits of
                  address (or $4000) plus a 2-bit bank offset from $FB. Each tile is 16 bytes of
                  2bpp and tile id i is entry i of the list.
Room record, 900 bytes: 360 tile ids (20 x 18, row major), 360 attributes, 180 collision bytes.
Attributes: bits 0-2 palette, bit 3 VRAM bank, bit 5 flip X, bit 6 flip Y.
"""
import struct
from PIL import Image

REC = 900
TILE_BASE_BANK = 0xFB


class Grandia:
    def __init__(self, path):
        self.rom = open(path, "rb").read()
        self.areas = self._areas()
        self._tilecache = {}

    # ---- low level
    def u16(self, bank, addr):
        o = bank * 0x4000 + (addr - 0x4000)
        return self.rom[o] | (self.rom[o + 1] << 8)

    def raw(self, bank, addr, n):
        o = bank * 0x4000 + (addr - 0x4000)
        return self.rom[o:o + n]

    # ---- palettes
    def palette_set(self, area):
        ptr = self.u16(0x82, 0x4000 + 2 * area)
        out = []
        for p in range(5):
            out.append([self._rgb(self.u16(0x82, ptr + p * 8 + 2 * k)) for k in range(4)])
        return out

    @staticmethod
    def _rgb(w):
        return (w & 31, (w >> 5) & 31, (w >> 10) & 31)

    # ---- areas and rooms
    def _areas(self):
        res = []
        ents = []
        for i in range(48):
            a = 0x4000 + 3 * i
            ents.append((self.raw(0x83, a, 1)[0], self.u16(0x83, a + 1)))
        for i, (tile, ptr) in enumerate(ents):
            nxt = ents[i + 1][1] if i + 1 < 48 else None
            rooms, a = [], ptr
            while nxt is None or a < nxt:
                b = self.raw(0x83, a, 3)
                bank, addr = b[0], b[1] | (b[2] << 8)
                if not (0x83 <= bank <= 0xA2 and 0x4000 <= addr <= 0x8000 - REC):
                    break
                rooms.append((bank, addr))
                a += 3
            res.append({"area": i, "tileset": tile, "rooms": rooms})
        return res

    def room(self, area, n):
        bank, addr = self.areas[area]["rooms"][n]
        r = self.raw(bank, addr, REC)
        return r[:360], r[360:720], r[720:900]

    # ---- tiles
    def tileset(self, t):
        if t in self._tilecache:
            return self._tilecache[t]
        e = 0x4000 + 3 * t
        n = self.raw(0xF9, e, 1)[0]
        de = self.u16(0xF9, e + 1)
        bank, addr = 0xF9 + (de >> 14), (de & 0x3FFF) | 0x4000
        tiles = []
        for i in range(n):
            c, b = self.raw(bank, addr + 2 * i, 2)
            tb, ta = TILE_BASE_BANK + (b >> 6), ((b & 0x3F) << 8 | c) | 0x4000
            tiles.append(self.raw(tb, ta, 16))
        self._tilecache[t] = tiles
        return tiles

    # ---- rendering
    def render(self, area, n, extra_pals=None):
        tid, att, _ = self.room(area, n)
        tiles = self.tileset(self.areas[area]["tileset"])
        pals = self.palette_set(area)
        if extra_pals:
            pals = pals + extra_pals
        im = Image.new("RGB", (160, 144))
        px = im.load()
        missing = 0
        for ty in range(18):
            for tx in range(20):
                i = ty * 20 + tx
                t, a = tid[i], att[i]
                if t >= len(tiles):
                    missing += 1
                    continue
                data = tiles[t]
                pal = pals[a & 7] if (a & 7) < len(pals) else [(31, 0, 31)] * 4
                for y in range(8):
                    lo, hi = data[2 * y], data[2 * y + 1]
                    for x in range(8):
                        bit = 7 - x
                        v = ((lo >> bit) & 1) | (((hi >> bit) & 1) << 1)
                        xx = 7 - x if a & 0x20 else x
                        yy = 7 - y if a & 0x40 else y
                        c = pal[v]
                        px[tx * 8 + xx, ty * 8 + yy] = tuple((q << 3) | (q >> 2) for q in c)
        return im, missing


if __name__ == "__main__":
    import sys
    g = Grandia(sys.argv[1])
    area, n = int(sys.argv[2]), int(sys.argv[3])
    im, miss = g.render(area, n)
    im.resize((320, 288), Image.NEAREST).save(sys.argv[4])
    print("missing tiles", miss)
