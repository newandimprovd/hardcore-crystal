#!/usr/bin/env python3
"""Free space of the ROM from the rgblink map file: python3 tools/hardcore/romfree.py [pokecrystal11.map]
The trailing 0xFF count of the ROM is misleading (padding inside banks), the map file lists the EMPTY ranges per bank."""
import re
import sys

p = sys.argv[1] if len(sys.argv) > 1 else "pokecrystal11.map"
cur, free, used, banks = None, {}, {}, {}
for line in open(p, errors="replace"):
    m = re.match(r"(ROM0|ROMX) bank #(\d+):", line)
    if m:
        cur = 0 if m.group(1) == "ROM0" else int(m.group(2))
        free.setdefault(cur, 0)
        continue
    m = re.search(r"EMPTY: \$[0-9a-f]+-\$[0-9a-f]+ \(\$([0-9a-f]+) bytes\)", line)
    if m and cur is not None:
        free[cur] += int(m.group(1), 16)
    m = re.search(r"SECTION: \$[0-9a-f]+-\$[0-9a-f]+ \(\$([0-9a-f]+) bytes\)", line)
    if m and cur is not None:
        used[cur] = used.get(cur, 0) + int(m.group(1), 16)
tf = sum(free.values())
print(f"ROM banks {len(free)}, free {tf} bytes ({tf // 1024} KB), used {sum(used.values())} bytes")
if "-v" in sys.argv:
    for b in sorted(free):
        print(f"  bank {b:3d}: used {used.get(b, 0):5d}  free {free[b]:5d}")
