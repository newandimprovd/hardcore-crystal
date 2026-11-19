import sys; sys.path.insert(0,"/home/claude/pokecrystal/tools/hardcore/refstudy")
from drive import *
import numpy as np
def _tile_pixels(vram, bank, addr):
    base = addr - 0x8000
    d = vram[bank][base:base+16]
    px = np.zeros((8,8), dtype=np.uint8)
    for r in range(8):
        lo, hi = d[2*r], d[2*r+1]
        for c in range(8):
            px[r, c] = ((lo >> (7-c)) & 1) | (((hi >> (7-c)) & 1) << 1)
    return px
def _canon(px):
    cands = [px, px[:, ::-1], px[::-1, :], px[::-1, ::-1]]
    return min(c.tobytes() for c in cands)
def analyze(pb):
    m = pb.memory
    lcdc = m[0xff40]; scx = m[0xff43]; scy = m[0xff42]
    bgmap = 0x9c00 if lcdc & 8 else 0x9800
    signed = not (lcdc & 0x10)
    vram = [bytes(m[b, 0x8000+i] for i in range(0x1800)) for b in (0,1)]
    mp = [[m[0, bgmap+32*y+x] for x in range(32)] for y in range(32)]
    at = [[m[1, bgmap+32*y+x] for x in range(32)] for y in range(32)]
    cells = []
    for ty in range(18):
        for tx in range(20):
            y = ((scy // 8) + ty) % 32; x = ((scx // 8) + tx) % 32
            cells.append((x, y, mp[y][x], at[y][x]))
    def taddr(tid): return 0x9000 + (tid - 256 if tid > 127 else tid) * 16 if signed else 0x8000 + tid * 16
    ids = set(); pix = set(); pals = set(); prio = flips = 0; pixcnt = {}
    for x, y, tid, a in cells:
        bank = (a >> 3) & 1
        ids.add((bank, tid)); pals.add(a & 7)
        prio += (a >> 7) & 1; flips += ((a >> 5) & 1) + ((a >> 6) & 1)
        px = _tile_pixels(vram, bank, taddr(tid)); k = _canon(px); pix.add(k)
        pixcnt[k] = pixcnt.get(k, 0) + 1
    blank = sum(v for k, v in pixcnt.items() if len(set(k)) == 1)
    # distinct 2x2 groups (aligned at even or odd cells)
    best = None
    for ox in (0, 1):
        for oy in (0, 1):
            g = set()
            for ty in range(oy, 17, 2):
                for tx in range(ox, 19, 2):
                    cs = []
                    for dy in (0, 1):
                        for dx in (0, 1):
                            x = ((scx//8)+tx+dx) % 32; y = ((scy//8)+ty+dy) % 32
                            cs.append((mp[y][x], at[y][x]))
                    g.add(tuple(cs))
            best = len(g) if best is None else min(best, len(g))
    oam = [(m[0xfe00+4*i], m[0xfe00+4*i+1]) for i in range(40)]
    spr = sum(1 for y, x in oam if 0 < y < 160 and 0 < x < 168)
    pb.tick(1, True)
    im = np.array(pb.screen.image.convert("RGB")).reshape(-1, 3)
    cols = len({tuple(c) for c in im})
    return dict(lcdc=hex(lcdc), scroll=(scx, scy), window=bool(lcdc & 0x20), tall_sprites=bool(lcdc & 4),
                cells=len(cells), unique_ids=len(ids), unique_pixel_tiles=len(pix), blank_cells=blank,
                palettes_used=sorted(pals), priority_cells=prio, flipped_flags=flips,
                unique_2x2_groups=best, sprites_on_screen=spr, colors_on_screen=cols)
