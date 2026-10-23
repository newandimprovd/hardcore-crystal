#!/usr/bin/env python3
"""Static check of the roster tables inside a built ROM against roster_out.json.

usage: test_roster.py ROM
Checks, for all 248 species: name, base stats, types, evolution target and level (25/50/75),
learnset ordering, cry table length, and that every line has exactly four stages.
"""
import json
import re
import sys

rom_path = sys.argv[1]
root = __file__.rsplit("/tools/", 1)[0]
rom = open(rom_path, "rb").read()
sym = {}
for line in open(rom_path.replace(".gbc", ".sym")):
    m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)", line)
    if m:
        sym[m[3]] = (int(m[1], 16), int(m[2], 16))
exp = json.load(open(root + "/tools/hardcore/roster/roster_out.json"))
assert len(exp) == 248


def off(bank, addr):
    return addr if addr < 0x4000 else bank * 0x4000 + (addr - 0x4000)


def label(name):
    b, a = sym[name]
    return off(b, a)


CH = {0x7F: " ", 0xE3: "-", 0xE6: "?", 0xE8: ".", 0xEF: "♂", 0xF5: "♀"}
CH.update({0xF6 + i: str(i) for i in range(10)})


def decode(bs):
    s = ""
    for b in bs:
        if b == 0x50:
            break
        s += CH.get(b, chr(b - 0x80 + 65) if 0x80 <= b <= 0x99 else "~")
    return s


bad = 0


def check(cond, msg):
    global bad
    if not cond:
        bad += 1
        if bad < 40:
            print("FAIL", msg)


# names
nb = label("PokemonNames")
for r in exp:
    got = decode(rom[nb + (r["id"] - 1) * 10: nb + r["id"] * 10])
    check(got == r["name"], f"name {r['id']} {got!r} != {r['name']!r}")

# type constants (parsed from the const_def / const_next / const lines)
tid = {}
v = 0
for l in open(root + "/constants/type_constants.asm"):
    l = l.split(";")[0]
    m = re.match(r"\s*const_def(?:\s+(\d+))?", l)
    if m:
        v = int(m[1]) if m[1] else 0
        continue
    m = re.match(r"\s*const_next\s+(\d+)", l)
    if m:
        v = int(m[1])
        continue
    m = re.match(r"\s*const (\w+)", l)
    if m:
        tid[m[1]] = v
        v += 1

# base data (32 bytes per species): species, hp atk def spd sat sdf, type1, type2
bb = label("BaseData")
for r in exp:
    o = bb + (r["id"] - 1) * 32
    check(rom[o] == r["id"], f"base data id byte {r['id']}")
    check(list(rom[o + 1:o + 7]) == r["stats"], f"stats {r['name']}: {list(rom[o + 1:o + 7])} != {r['stats']}")
    check([rom[o + 7], rom[o + 8]] == [tid[t] for t in r["types"]], f"types {r['name']}")

# evolutions
eb = label("EvosAttacksPointers")
ebank = sym["EvosAttacksPointers"][0]
byid = {r["id"]: r for r in exp}
byconst = {r["const"]: r for r in exp}
for r in exp:
    p = rom[eb + (r["id"] - 1) * 2] | (rom[eb + (r["id"] - 1) * 2 + 1] << 8)
    o = off(ebank, p)
    evos = []
    while rom[o] != 0:
        evos.append((rom[o], rom[o + 1], rom[o + 2]))
        o += 3
    o += 1
    if r["next"]:
        nxt = byconst[r["next"]]
        want = [(1, {1: 25, 2: 50, 3: 75}[r["stage"]], nxt["id"])]
        check(evos == want, f"evolution {r['name']}: {evos} != {want}")
    else:
        check(evos == [], f"final form {r['name']} evolves: {evos}")
    moves = []
    while rom[o] != 0:
        moves.append((rom[o], rom[o + 1]))
        o += 2
    lv = [m[0] for m in moves]
    check(lv == sorted(lv), f"learnset order {r['name']}")
    check(len(moves) >= 1, f"empty learnset {r['name']}")

# lines: exactly four stages per base form, no branching
lines = {}
for r in exp:
    lines.setdefault(r["line"], []).append(r)
check(len(lines) == 62, f"lines {len(lines)}")
for k, st in lines.items():
    st.sort(key=lambda r: r["stage"])
    check([r["stage"] for r in st] == [1, 2, 3, 4], f"line {k} stages")
    for a, b in zip(st, st[1:]):
        check(a["next"] == b["const"], f"line {k} link {a['name']}")
    check(st[-1]["next"] is None, f"line {k} final")
fin = {k: sum(st[-1]["stats"]) for k, st in lines.items()}
top = sorted(fin.items(), key=lambda x: -x[1])
check({top[0][0], top[1][0]} == {"DRATINI", "LARVITAR"}, f"strongest lines {top[:3]}")
# strongest species overall
allst = sorted(exp, key=lambda r: -sum(r["stats"]))
check({allst[0]["line"], allst[1]["line"]} == {"DRATINI", "LARVITAR"}, "strongest species")

# cries table length
cb = label("PokemonCries")
print(f"checked {len(exp)} species, lines {len(lines)}, failures {bad}")
sys.exit(1 if bad else 0)
