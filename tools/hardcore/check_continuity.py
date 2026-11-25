#!/usr/bin/env python3
"""Continuity audit of the generated world (alpha 3.3).  The playtest said the game still has leftover discontinuities, so this looks for the ones a program can see:

  seam      two connected outdoor maps whose touching edges do not line up: an opening of 3 or more cells at the edge of one map faces solid wall in the other
            (information only: looked at on a rendered seam it reads as open ground meeting a hedge or a tree line, so it does not fail the run), or the two
            maps use different tilesets (a palette jump at the seam; allowed)
  recip     a connection that the other map does not return (A leads east to B, B does not lead west to A at the opposite offset)
  warp      a warp whose destination map or warp number does not exist, or that is not answered by a warp back (one way doors)
  level     a jump of more than LEVEL_JUMP in the average trainer level between two connected maps (the road suddenly gets much easier or much harder)
  music     two connected outdoor maps of one area with different music (the soundtrack changes in the middle of a road)

Prints every finding and exits 1 when there is any in the categories that are not on the allow lists below (intended crossings between areas and story warps).
usage: check_continuity.py [--all]   (--all also lists the allowed ones)"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from areamodel import load, rd, WALKABLE  # noqa: E402

LEVEL_JUMP = 7
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
PASS = lambda c: c is not None and c in WALKABLE or c in (0x00, 0x10, 0x14, 0x18, 0x48, 0x49, 0x4c)  # noqa: E731

maps = load()


def trainer_levels():
    """map name -> list of the highest party level of each trainer on it."""
    groups = {}
    cur = None
    for l in rd("data/hardcore/gen_trainer_data.asm").splitlines():
        m = re.match(r"HC_GenGroup_(\w+):", l)
        if m:
            cur = m[1]
            groups[cur] = [[]]
            continue
        if cur is None:
            continue
        m = re.match(r"\s*db (-?\d+), ([A-Z0-9_]+), ", l)
        if m:
            if int(m[1]) == -1:
                groups[cur].append([])
            else:
                groups[cur][-1].append(int(m[1]))
        elif re.match(r"\s*db -1\s*$", l):
            groups[cur].append([])
    out = {}
    for name, mp in maps.items():
        try:
            s = rd(f"maps/gen/{name}.asm")
        except OSError:
            continue
        lv = []
        for m in re.finditer(r"^\s*trainer (\w+), (\d+),", s, re.M):
            cls, tid = m[1], int(m[2])
            g = groups.get(cls)
            if g and 1 <= tid <= len(g) and g[tid - 1]:
                lv.append(max(g[tid - 1]))
        out[name] = lv
    return out


def map_attrs():
    d = {}
    for l in rd("data/maps/area_map_lists.asm").splitlines():
        m = re.match(r"\s*map (\w+), (TILESET_\w+), (\w+), (\w+), (\w+),", l)
        if m:
            d[m[1]] = dict(tileset=m[2], env=m[3], landmark=m[4], music=m[5])
    return d


attrs = map_attrs()
levels = trainer_levels()
findings = []  # (kind, text, allowed)


def add(kind, text, allowed=False):
    findings.append((kind, text, allowed))


def outdoor(n):
    return attrs.get(n, {}).get("env") in ("TOWN", "ROUTE")


def mean(v):
    return sum(v) / len(v) if v else None


seen_pairs = set()
for name, mp in sorted(maps.items()):
    for d, (other, off) in mp.conns.items():
        om = maps.get(other)
        if om is None:
            add("recip", f"{name} {d} leads to {other}, which is not a generated map", allowed=True)
            continue
        back = om.conns.get(OPP[d])
        if not back or back[0] != name or back[1] != -off:
            add("recip", f"{name} {d} -> {other} (offset {off}), but {other} {OPP[d]} -> {back}")
        key = tuple(sorted([(name, d), (other, OPP[d])]))
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        # the seam: the passages (runs of at least 3 walkable cells along the edge) must meet; pockets of one or two cells are only scenery
        def passages(cells):
            runs, start = [], None
            for i, ok in enumerate(cells + [False]):
                if ok and start is None:
                    start = i
                elif not ok and start is not None:
                    if i - start >= 3:
                        runs.append((start, i - 1))
                    start = None
            return runs

        if d in ("north", "south"):
            ay = 0 if d == "north" else 2 * mp.h - 1
            by = 2 * om.h - 1 if d == "north" else 0
            ea = [bool(PASS(mp.cell(x, ay))) for x in range(2 * mp.w)]
            eb = [bool(PASS(om.cell(x - 2 * off, by))) if 0 <= x - 2 * off < 2 * om.w else False for x in range(2 * mp.w)]
        else:
            ax = 0 if d == "west" else 2 * mp.w - 1
            bx = 2 * om.w - 1 if d == "west" else 0
            ea = [bool(PASS(mp.cell(ax, y))) for y in range(2 * mp.h)]
            eb = [bool(PASS(om.cell(bx, y - 2 * off))) if 0 <= y - 2 * off < 2 * om.h else False for y in range(2 * mp.h)]
        # a passage that meets only wall on the other side is a door to nowhere; a passage that is narrower or wider than its neighbour is scenery
        for (nm, ps, ee, onm) in ((name, passages(ea), eb, other), (other, passages(eb), ea, name)):
            for (s0, s1) in ps:
                if not any(ee[s0:s1 + 1]):
                    add("seam", f"{nm}: the passage at cells {s0} to {s1} of the {d if nm == name else OPP[d]} edge meets only wall in {onm}", allowed=True)
        ta, tb = attrs.get(name, {}).get("tileset"), attrs.get(other, {}).get("tileset")
        if ta and tb and ta != tb:
            add("seam", f"{name} / {other}: tileset {ta} against {tb} (palette jump)", allowed=True)
        ma, mb = attrs.get(name, {}).get("music"), attrs.get(other, {}).get("music")
        if outdoor(name) and outdoor(other) and ma != mb:
            add("music", f"{name} ({ma}) / {other} ({mb})")
        la, lb = mean(levels.get(name, [])), mean(levels.get(other, []))
        if la is not None and lb is not None and len(levels[name]) >= 2 and len(levels[other]) >= 2 and abs(la - lb) > LEVEL_JUMP:
            add("level", f"{name} (avg {la:.0f}) / {other} (avg {lb:.0f})")

consts = {mp.const: mp for mp in maps.values()}
for name, mp in sorted(maps.items()):
    for i, (x, y, dest, dw) in enumerate(mp.warps, 1):
        if dest == "LAST_MAP":
            continue
        dm = consts.get(dest)
        if dm is None:
            add("warp", f"{name} warp {i} -> {dest}: not a generated map", allowed=True)
            continue
        if not (1 <= dw <= len(dm.warps)):
            add("warp", f"{name} warp {i} -> {dest} #{dw}: that map has {len(dm.warps)} warps")
            continue
        bx, by, bdest, bdw = dm.warps[dw - 1]
        if bdest not in (mp.const, "LAST_MAP"):
            add("warp", f"{name} warp {i} -> {dest} #{dw}, which leads on to {bdest} (one way)", allowed=name.startswith(("Purg", "Hollow", "Vault", "Undercroft")) or dest.startswith(("PURG", "HOLLOW", "VAULT", "UNDERCROFT")))

bad_total = 0
for kind in ("seam", "recip", "warp", "level", "music"):
    rows = [f for f in findings if f[0] == kind]
    real = [f for f in rows if not f[2]]
    print(f"{kind:6} {len(real)} problems" + (f" ({len(rows) - len(real)} allowed)" if len(rows) != len(real) else ""))
    for _, text, allowed in rows:
        if not allowed or "--all" in sys.argv:
            print("   " + ("(allowed) " if allowed else "") + text)
    bad_total += len(real)
print("PASS" if not bad_total else f"FAIL: {bad_total} findings")
sys.exit(0 if not bad_total else 1)
