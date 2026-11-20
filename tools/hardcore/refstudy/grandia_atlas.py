#!/usr/bin/env python3
"""Render one representative room per Grandia area with its true palettes, plus statistics.

Usage: grandia_atlas.py GRANDIA.gbc OUTDIR [--tilesets DIR_OF_CRYSTAL_TILESET_PNGS]
"""
import colorsys, os, sys, glob
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grandia_db import Grandia


def vivid(c):
    h, s, v = colorsys.rgb_to_hsv(*(q / 31 for q in c))
    return s >= 0.5 and v >= 0.4, int(h * 6 + 0.5) % 6


def main():
    g = Grandia(sys.argv[1])
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    cols = 6
    rows = 8
    atlas = Image.new("RGB", (cols * 164, rows * 164), (20, 20, 20))
    d = ImageDraw.Draw(atlas)
    print("area rooms tiles used_ids rep_room colours vivid hues")
    tot_rooms = 0
    sizes = []
    for a in range(48):
        nrooms = len(g.areas[a]["rooms"])
        tot_rooms += nrooms
        tiles = g.tileset(g.areas[a]["tileset"])
        sizes.append(len(tiles))
        used = set()
        best, bestn = 0, -1
        for n in range(nrooms):
            tid, _, _ = g.room(a, n)
            u = set(tid)
            used |= u
            if len(u) > bestn:
                best, bestn = n, len(u)
        im, miss = g.render(a, best)
        cs = set(im.getdata())
        cs5 = {tuple(q >> 3 for q in c) for c in cs}
        vv = [vivid(c) for c in cs5]
        nviv = sum(1 for v, _ in vv if v)
        hues = len({h for v, h in vv if v})
        print(f"{a:3d} {nrooms:5d} {len(tiles):5d} {len(used):8d} {best:8d} {len(cs):7d} {nviv:5d} {hues:4d}")
        x, y = (a % cols) * 164 + 2, (a // cols) * 164 + 2
        atlas.paste(im, (x, y))
        d.text((x + 3, y + 3), str(a), fill=(255, 255, 255))
    atlas.save(os.path.join(out, "grandia_areas_atlas.png"))
    print("total room records", tot_rooms)
    print("tileset sizes min/mean/max", min(sizes), sum(sizes) / len(sizes), max(sizes))
    if "--tilesets" in sys.argv:
        dd = sys.argv[sys.argv.index("--tilesets") + 1]
        cs = []
        for p in sorted(glob.glob(os.path.join(dd, "*.png"))):
            w, h = Image.open(p).size
            cs.append((os.path.basename(p), w * h // 64))
        print("Crystal tileset tile counts:", cs)


if __name__ == "__main__":
    main()
