#!/usr/bin/env python3
"""Battle budget check (areas/counts.py): counts every fight of the emitted maps and fails when the plan is broken.

  normal     trainers of the roads and lanes (and the plazas), plus Timmy in Cherrygrove: the mandatory kills, MANDATORY = 500 in all
  specials   bosses (one trainer rooms of the areas) and the scripted duels (Bruno), the named duels (areas/named.py: eight key bearers, five philosophers, five rival fights)
  purg       the trainers of Purgatorio: not part of the 500
The whole game must stay at or under TOTAL_CAP = 650, and the tidal wave (TSUNAMI_KILLS) must come before the crater (the rival's fall).
Usage: python3 tools/hardcore/battle_budget.py [--quiet]"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from areas import counts  # noqa: E402

AREAS = ("Tithe", "Grove", "Axiom", "Lotus", "Dis")


def tally():
    normal = dict.fromkeys(AREAS, 0)
    specials, purg, scripted, other = {}, 0, 0, {}
    for f in sorted(glob.glob(os.path.join(ROOT, "maps", "gen", "*.asm"))):
        name = os.path.basename(f)[:-4]
        src = open(f).read()
        n = len(re.findall(r"OBJECTTYPE_TRAINER", src))
        if not name.startswith("Purg"):
            scripted += len(re.findall(r"^\tstartbattle", src, re.M))  # the named duelists of the plazas (areas/specials.py)
        if name.startswith("Purg"):
            purg += n
            if name in ("PurgLanding", "PurgThreshold"):  # Bruno; Steiner, Abd al-Jabbar and the rival in the hub
                scripted += len(re.findall(r"^\tstartbattle", src, re.M))
            continue
        if not n:
            continue
        area = next((a for a in AREAS if name.startswith(a)), None)
        if area and re.search(r"(Street\d+|Road|Plaza\d+)$", name):
            normal[area] += n
        elif area:
            specials[name] = n
        else:
            other[name] = n  # the two last rooms of Area 5 (Judecca, Cocytus)
    return normal, specials, other, purg, scripted


def main():
    quiet = "--quiet" in sys.argv
    normal, specials, other, purg, scripted = tally()
    timmy = counts.TIMMY
    mandatory = sum(normal.values()) + timmy
    spec = sum(specials.values()) + sum(other.values()) + scripted
    total = mandatory + spec + purg
    problems = []
    if mandatory != counts.MANDATORY:
        problems.append(f"mandatory trainers {mandatory}, plan {counts.MANDATORY}")
    for a in AREAS:
        want = counts.PER_AREA - (timmy if a == "Tithe" else 0)
        if normal[a] != want:
            problems.append(f"{a}: {normal[a]} normal trainers, plan {want}")
    if not 0 < counts.TSUNAMI_KILLS < counts.rival_kills():
        problems.append(f"tidal wave at kill {counts.TSUNAMI_KILLS} must come before the rival's fall at kill {counts.rival_kills()}")
    if total > counts.TOTAL_CAP:
        problems.append(f"{total} battles in all, cap {counts.TOTAL_CAP}")
    if not quiet:
        print("normal per area:", normal, "+ Timmy", timmy, "=", mandatory)
        print("specials (bosses and last rooms):", spec - scripted, "scripted duels:", scripted)
        print("purgatorio:", purg)
        print(f"total {total} of {counts.TOTAL_CAP}, room for {counts.TOTAL_CAP - total} more special encounters")
        print(f"tidal wave news at kill {counts.TSUNAMI_KILLS}, crater with the rival at kill {counts.rival_kills()}, drop tiers at {counts.drop_tiers()}")
    for p in problems:
        print("PROBLEM:", p)
    print("PASS" if not problems else "FAIL")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
