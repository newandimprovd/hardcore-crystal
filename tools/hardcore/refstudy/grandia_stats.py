"""ROM-wide statistics over Grandia's 556 room records (no emulator needed).
Record layout: 360 tile ids, 360 attribute bytes, 90 little-endian collision words, 900 bytes, 18 records per bank, banks $84 to $A2."""
import os, sys, collections, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grandia_rooms import rec

N = 556
ids = []; flip = tot = 0; pal = collections.Counter(); bank1 = 0
words = collections.Counter(); hi = collections.Counter(); side = collections.Counter()
for i in range(N):
    t, at, w = rec(i)
    ids.append(len(set(t)))
    for a in at:
        tot += 1; flip += bool(a & 0x60); pal[a & 7] += 1; bank1 += bool(a & 8)
    for row in w:
        for x in row:
            words[x] += 1; hi[x >> 8] += 1
            if 0 < (x & 0xF) < 0xF: side[x & 0xF] += 1
print("distinct tile ids per room: min", min(ids), "median", statistics.median(ids), "max", max(ids))
print("flipped cells %.1f%%" % (100 * flip / tot), "palettes", dict(sorted(pal.items())), "VRAM bank 1 cells %.1f%%" % (100 * bank1 / tot))
print("collision high byte histogram", {hex(k): v for k, v in sorted(hi.items())})
print("most common words", {hex(k): v for k, v in words.most_common(12)})

def op(w, r, c): return (w[r][c] & 0xFF) == 0
W = [rec(i)[2] for i in range(N)]
def edge(i, side_):
    w = W[i]
    return tuple({"R": lambda r: op(w, r, 9), "L": lambda r: op(w, r, 0)}[side_](r) for r in range(9)) if side_ in "RL" else \
           tuple(op(w, 8 if side_ == "B" else 0, c) for c in range(10))
v = sum(1 for i in range(N - 1) if any(edge(i, "B")) and edge(i, "B") == edge(i + 1, "T"))
print("rooms whose open south edge matches the open north edge of the next record:", v, "of", sum(1 for i in range(N) if any(edge(i, "B"))))
