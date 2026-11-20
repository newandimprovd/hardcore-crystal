#!/usr/bin/env python3
"""Read Grandia (GBC) background palette sets straight from the ROM and compare them
with pokecrystal's tileset palettes.

Usage: grandia_palettes.py GRANDIA.gbc OUTDIR [--crystal gfx/tilesets/bg_tiles.pal]

Findings this script relies on (all verified by watching the game):
  * The game copies 64 bytes of BG palettes and 64 bytes of OBJ palettes from a WRAM buffer
    at $C10F into the colour registers (routine at bank 02:$699A).
  * Bank $82 starts with a table of 48 little-endian pointers ($4060, $4088, ...), each
    pointing at 40 bytes, which is five BG palettes (BG0..BG4) of four RGB555 colours.
  * BG5 and BG6 (white and skin tones) come from a separate table in bank $7B.
"""
import colorsys, os, re, struct, sys
from PIL import Image, ImageDraw

BANK_PAL = 0x82
N_SETS = 48
PALS_PER_SET = 5


def rgb(w):
    r, g, b = w & 31, (w >> 5) & 31, (w >> 10) & 31
    return r, g, b


def disp(c):
    return tuple((v << 3) | (v >> 2) for v in c)


def hsv(c):
    return colorsys.rgb_to_hsv(*(v / 31 for v in c))


def vivid(c):
    h, s, v = hsv(c)
    return s >= 0.5 and v >= 0.4


def hue_bin(c):
    return int(hsv(c)[0] * 6 + 0.5) % 6  # red, yellow, green, cyan, blue, magenta


def grandia_sets(rom):
    base = BANK_PAL * 0x4000
    sets = []
    for i in range(N_SETS):
        ptr = struct.unpack_from("<H", rom, base + 2 * i)[0]
        off = base + (ptr - 0x4000)
        pals = []
        for p in range(PALS_PER_SET):
            pals.append([rgb(struct.unpack_from("<H", rom, off + p * 8 + 2 * k)[0]) for k in range(4)])
        sets.append(pals)
    return sets


def crystal_day(path):
    """The five time-of-day blocks of pokecrystal's bg_tiles.pal, as {name: [palette,...]}."""
    out, cur = {}, None
    for line in open(path):
        line = line.split(";")[0] if not line.startswith(";") else line
        m = re.match(r";\s*(\w+)", line)
        if line.startswith(";") and m:
            cur = m.group(1)
            out[cur] = []
            continue
        nums = re.findall(r"RGB\s+(.*)", line)
        if nums and cur:
            v = [int(x) for x in re.findall(r"\d+", nums[0])]
            out[cur].append([tuple(v[i:i + 3]) for i in range(0, 12, 3)])
    return out


def stats(pals):
    cols = [c for p in pals for c in p]
    uniq = sorted(set(cols))
    viv = [c for c in uniq if vivid(c)]
    sats = [hsv(c)[1] for c in uniq if hsv(c)[2] > 0.2]
    return {
        "distinct": len(uniq),
        "vivid": len(viv),
        "hues": len({hue_bin(c) for c in viv}),
        "mean_sat": sum(sats) / max(1, len(sats)),
    }


def render(sets, title_fmt, path, sw=14):
    rows = len(sets)
    im = Image.new("RGB", (PALS_PER_SET * (4 * sw + 8) + 40, rows * (sw + 2) + 4), (24, 24, 24))
    d = ImageDraw.Draw(im)
    for i, pals in enumerate(sets):
        y = 2 + i * (sw + 2)
        d.text((2, y + 1), title_fmt.format(i), fill=(200, 200, 200))
        for p, pal in enumerate(pals):
            for k, c in enumerate(pal):
                x = 40 + p * (4 * sw + 8) + k * sw
                d.rectangle([x, y, x + sw - 1, y + sw - 1], fill=disp(c))
    im.save(path)


def main():
    rom = open(sys.argv[1], "rb").read()
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    crystal = None
    if "--crystal" in sys.argv:
        crystal = crystal_day(sys.argv[sys.argv.index("--crystal") + 1])
    sets = grandia_sets(rom)
    render(sets, "{:02d}", os.path.join(out, "grandia_bg_palette_sets.png"))
    print("Grandia BG palette sets (bank $82)")
    print("set distinct vivid hues mean_sat")
    tot = {"distinct": 0, "vivid": 0}
    hist = {}
    for i, pals in enumerate(sets):
        s = stats(pals)
        hist[s["hues"]] = hist.get(s["hues"], 0) + 1
        tot["distinct"] += s["distinct"]
        tot["vivid"] += s["vivid"]
        print(f"{i:3d} {s['distinct']:8d} {s['vivid']:5d} {s['hues']:4d} {s['mean_sat']:.2f}")
    print("sets by number of distinct vivid hue families:", dict(sorted(hist.items())))
    allpals = [p for s in sets for p in s]
    print("all sets together:", stats(allpals))
    print("opening-chapter sets 44..47:", [stats(sets[i]) for i in range(44, 48)])
    if crystal:
        cs = []
        for name, pals in crystal.items():
            s = stats(pals[:7])
            cs.append((name, s))
            print("Crystal", name, s)
        render([crystal["day"][:5]], "day", os.path.join(out, "crystal_day_palettes.png"))


if __name__ == "__main__":
    main()
