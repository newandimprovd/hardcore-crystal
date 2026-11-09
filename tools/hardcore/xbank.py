#!/usr/bin/env python3
"""List plain call/jp/jr instructions whose target label lives in another ROM bank than the caller.
rgbasm cannot see this (the sections are placed by layout.link), and it silently executes the wrong code.
Sources: main.asm/home.asm INCLUDE tree + layout.link give each file its bank, the .sym file each label's bank.
Usage: xbank.py [pokecrystal11.sym]"""
import re, sys, os
sym = sys.argv[1] if len(sys.argv) > 1 else "pokecrystal11.sym"

lab = {}
for l in open(sym):
    m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) ([A-Za-z_]\w*)$", l.strip())
    if m: lab.setdefault(m[3], set()).add(int(m[1], 16))

# section name -> bank from layout.link
secbank, cur = {}, None
for l in open("layout.link"):
    m = re.match(r"(ROM0|ROMX \$([0-9a-f]+))", l)
    if m: cur = 0 if m[1] == "ROM0" else int(m[2], 16); continue
    if re.match(r"(WRAM|SRAM|VRAM|HRAM|OAM)", l): cur = None; continue
    m = re.match(r'\s*"([^"]+)"', l)
    if m and cur is not None: secbank[m[1]] = cur

filebank = {}
def walk(path, bank):
    sec = bank
    for l in open(path, errors="replace"):
        m = re.match(r'\s*SECTION\s+(?:UNION\s+|FRAGMENT\s+)?"([^"]+)"', l)
        if m:
            sec = secbank.get(m[1], None)
            continue
        m = re.match(r'\s*INCLUDE\s+"([^"]+)"', l)
        if m and os.path.exists(m[1]):
            if m[1] not in filebank and sec is not None:
                filebank[m[1]] = sec
                walk(m[1], sec)
for top in ("main.asm", "home.asm"):
    if os.path.exists(top): walk(top, None)

pat = re.compile(r"^\s*(call|jp|jr)\s+(?:[a-z]+\s*,\s*)?([A-Z][A-Za-z0-9_]*)\b")
n = 0
for f, b in sorted(filebank.items()):
    if b == 0: continue
    for i, l in enumerate(open(f, errors="replace"), 1):
        m = pat.match(l)
        if not m: continue
        t = m[2]
        banks = lab.get(t)
        if not banks or 0 in banks or b in banks: continue
        print(f"{f}:{i}: {l.strip()}   (caller bank {b:02x}, target bank {sorted(banks)[0]:02x})")
        n += 1
print(n, "cross-bank plain calls")
