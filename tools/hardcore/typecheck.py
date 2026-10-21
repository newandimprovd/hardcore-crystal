#!/usr/bin/env python3
"""Read the type chart back out of a built ROM and check it against the design rules.
usage: typecheck.py ROM.gbc [ROM.sym]"""
import re, sys

rom_path = sys.argv[1]
sym_path = sys.argv[2] if len(sys.argv) > 2 else rom_path.replace(".gbc", ".sym")
rom = open(rom_path, "rb").read()
sym = {}
for line in open(sym_path):
    m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)", line)
    if m:
        sym[m[3]] = (int(m[1], 16), int(m[2], 16))

def off(bank, addr):
    return addr if bank == 0 else bank * 0x4000 + (addr - 0x4000)

T = {n: i for i, n in enumerate("NORMAL FIGHTING FLYING POISON GROUND ROCK BIRD BUG GHOST STEEL".split())}
T.update({"FIRE": 20, "WATER": 21, "GRASS": 22, "ELECTRIC": 23, "PSYCHIC": 24, "ICE": 25, "DRAGON": 26, "DARK": 27, "FAIRY": 28})
NAME = {v: k for k, v in T.items()}

b, a = sym["TypeMatchups"]
p = off(b, a)
chart, foresight = {}, {}
section = chart
rows = 0
while True:
    x = rom[p]
    if x == 0xFF:
        break
    if x == 0xFE:
        section = foresight
        p += 1
        continue
    section[(x, rom[p + 1])] = rom[p + 2]
    rows += 1
    p += 3
SE, NVE, NO = 20, 5, 0
fails = []

def eff(atk, d1, d2=None):
    m = 10
    for d in {d1, d2} - {None}:
        m = m * chart.get((T[atk], T[d]), 10) // 10
    return m

def expect(atk, d, want):
    got = eff(atk, d)
    if got != want:
        fails.append(f"{atk} -> {d}: expected {want}, got {got}")

# author rules
expect("DARK", "NORMAL", NO)
expect("NORMAL", "BUG", SE); expect("NORMAL", "PSYCHIC", SE)
for atk in ["GHOST", "DARK", "PSYCHIC", "GRASS", "GROUND"]:
    expect(atk, "BUG", NO)
expect("GRASS", "ELECTRIC", SE); expect("GRASS", "STEEL", SE)
expect("WATER", "STEEL", SE); expect("ICE", "WATER", SE)
expect("GRASS", "FLYING", SE); expect("FLYING", "GRASS", SE)
# fairy
for d in ["FIGHTING", "DRAGON", "DARK"]: expect("FAIRY", d, SE)
for d in ["FIRE", "POISON", "STEEL"]: expect("FAIRY", d, NVE)
expect("POISON", "FAIRY", SE); expect("STEEL", "FAIRY", SE)
for atk in ["FIGHTING", "BUG", "DARK"]: expect(atk, "FAIRY", NVE)
expect("DRAGON", "FAIRY", NO)
expect("NORMAL", "FAIRY", 10); expect("FAIRY", "NORMAL", 10); expect("FAIRY", "FAIRY", 10)
# vanilla sanity
expect("FIRE", "GRASS", SE); expect("WATER", "FIRE", SE); expect("ELECTRIC", "GROUND", NO)
expect("GROUND", "FLYING", NO); expect("PSYCHIC", "DARK", NO); expect("POISON", "STEEL", NO)
expect("FIGHTING", "NORMAL", SE); expect("DRAGON", "DRAGON", SE); expect("ELECTRIC", "FLYING", SE)
expect("ICE", "DRAGON", SE); expect("ROCK", "FLYING", SE); expect("GHOST", "PSYCHIC", SE)
if foresight != {(T["NORMAL"], T["GHOST"]): 0, (T["FIGHTING"], T["GHOST"]): 0}:
    fails.append(f"foresight section wrong: {foresight}")
# dual types
if eff("FIRE", "GRASS", "BUG") != 40: fails.append("FIRE vs GRASS/BUG should be 40")
if eff("FAIRY", "DRAGON", "DARK") != 40: fails.append("FAIRY vs DRAGON/DARK should be 40")
if eff("DRAGON", "FAIRY", "STEEL") != 0: fails.append("DRAGON vs FAIRY/STEEL should be 0")
if eff("POISON", "FAIRY", "STEEL") != 0 and eff("POISON", "FAIRY", "STEEL") != 0: pass

# type names
b, a = sym["TypeNames"]
p = off(b, a) + 28 * 2
ptr = rom[p] | rom[p + 1] << 8
s = bytes(rom[off(b, ptr): off(b, ptr) + 6])
if s != bytes([0x85, 0x80, 0x88, 0x91, 0x98, 0x50]):  # F A I R Y @ in Crystal charmap
    fails.append(f"TypeNames[28] bytes {s.hex()}")

print(f"matchup rows: {rows}, foresight rows: {len(foresight)}")
if fails:
    print("FAIL"); [print("  ", f) for f in fails]; sys.exit(1)
print("typecheck PASS")
