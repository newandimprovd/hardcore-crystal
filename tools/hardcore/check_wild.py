#!/usr/bin/env python3
"""Static checker for the wild encounters (stage 9): proves from the built ROM that the player can catch the base form of every line.

usage: check_wild.py [ROM]   (default pokecrystal11.gbc next to the sources; needs the .sym file beside it)

Checks
  1. The wild table in the ROM (KantoGrassWildMons) is exactly what areas/wild.py generated (tools/hardcore/wild_out.json): same
     maps, rates, slots, levels and species, for all three times of day.
  2. Every plaza with an entry has tall-grass cells (collision TALL_GRASS) that the area model can walk to from the plaza floor.
  3. Every one of the 62 base forms has a slot of at least 10 percent in one map or more and shows up in two maps or more.
  4. Levels stay in the level range of the area.
Exit status 1 and a list of problems if anything fails."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from areamodel import GRASS, World  # noqa: E402
from test_walk import const_table, find_ids  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
MIN_PERCENT = 10  # a slot this likely counts as a place to catch the form
MIN_LIKELY_MAPS = 1
MIN_ANY_MAPS = 2  # and the form shows up in this many maps in all


def sym_address(sym_path, name):
    for line in open(sym_path):
        parts = line.split()
        if len(parts) == 2 and parts[1] == name:
            bank, addr = parts[0].split(":")
            return int(bank, 16), int(addr, 16)
    raise KeyError(name)


def read_table(rom, bank, addr):
    off = bank * 0x4000 + (addr - 0x4000 if addr >= 0x4000 else addr)
    entries = []
    while rom[off] != 0xFF:
        grp, num = rom[off], rom[off + 1]
        rates = list(rom[off + 2:off + 5])
        off += 5
        tod = []
        for _ in range(3):
            slots = []
            for _ in range(7):
                slots.append((rom[off], rom[off + 1]))
                off += 2
            tod.append(slots)
        entries.append(dict(group=grp, num=num, rates=rates, tod=tod))
    return entries


def main():
    rom_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "pokecrystal11.gbc")
    sym_path = rom_path.replace(".gbc", ".sym")
    rom = open(rom_path, "rb").read()
    spec = json.load(open(os.path.join(HERE, "wild_out.json")))
    slots = spec["slots"]
    entries = spec["entries"]
    problems = []

    species = const_table("constants/pokemon_constants.asm")
    names = {}
    for k, v in species.items():  # the Unown letters repeat values 1..26 further down: the first name wins
        names.setdefault(v, k)
    world = World()
    ids = find_ids(world)
    by_name = {n: gn for gn, n in ids.items()}

    # 1. the ROM table
    bank, addr = sym_address(sym_path, "KantoGrassWildMons")
    table = read_table(rom, bank, addr)
    if len(table) != len(entries):
        problems.append(f"ROM table has {len(table)} entries, generator wrote {len(entries)}")
    for e, r in zip(entries, table):
        gn = by_name.get(e["map"])
        if gn is None or (r["group"], r["num"]) != gn:
            problems.append(f"{e['map']}: ROM entry is for map {(r['group'], r['num'])}, expected {gn}")
        if r["rates"] != [e["rate"] * 255 // 100] * 3:
            problems.append(f"{e['map']}: encounter rates {r['rates']}")
        for t, key in enumerate(("morn", "day", "nite")):
            got = [(lv, names.get(sp, f"?{sp}")) for lv, sp in r["tod"][t]]
            want = [(lv, sp) for lv, sp in e[key]]
            if got != want:
                problems.append(f"{e['map']} {key}: ROM {got} != generated {want}")

    # 2. grass is there and reachable
    for e in entries:
        mp = world.maps.get(e["map"])
        if mp is None:
            problems.append(f"{e['map']}: not in the area model")
            continue
        cells = [(x, y) for y in range(2 * mp.h) for x in range(2 * mp.w) if mp.cell(x, y) in GRASS]
        if len(cells) < 20:
            problems.append(f"{e['map']}: only {len(cells)} tall-grass cells")
            continue
        start = (e["map"], 8, 6)
        goal = set(cells)
        route = world.route(start, lambda s: s[0] == e["map"] and (s[1], s[2]) in goal)
        if route is None:
            problems.append(f"{e['map']}: no walkable way from the plaza floor to the grass")

    # 3. every base form is catchable
    base = [m["const"] for m in json.load(open(os.path.join(HERE, "roster/roster_out.json"))) if m["stage"] == 1]
    seen = {b: {} for b in base}
    for e in entries:
        for key in ("morn", "day", "nite"):
            for j, (lv, sp) in enumerate(e[key]):
                if sp in seen:
                    seen[sp][e["map"]] = max(seen[sp].get(e["map"], 0), slots[j])
    for b in base:
        good = [m for m, p in seen[b].items() if p >= MIN_PERCENT]
        if len(good) < MIN_LIKELY_MAPS or len(seen[b]) < MIN_ANY_MAPS:
            problems.append(f"{b}: {len(good)} map(s) with a slot of {MIN_PERCENT}+ percent, {len(seen[b])} in all ({seen[b]})")

    # 4. levels in the area's range
    from areas.wild import themes
    _, levels = themes()
    for e in entries:
        l0, l1 = levels[e["area"] - 1]
        for key in ("morn", "day", "nite"):
            for lv, sp in e[key]:
                if not (l0 - 2 <= lv <= l1 + 4):
                    problems.append(f"{e['map']}: level {lv} outside {l0}..{l1}")
    counts = sorted(len([1 for p in seen[b].values() if p >= MIN_PERCENT]) for b in base)
    best = sorted(max(seen[b].values()) if seen[b] else 0 for b in base)
    print(f"{len(entries)} plaza tables, {len(base)} base forms, likely slot (10+%) in {counts[0]}..{counts[-1]} maps each, best chance {best[0]}..{best[-1]} percent")
    if problems:
        print(f"problems: {len(problems)}")
        for p in problems[:40]:
            print("  !!", p)
        print("FAIL")
        return 1
    print("problems: 0")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
