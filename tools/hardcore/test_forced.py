#!/usr/bin/env python3
"""Model check of the forced bearers (areas/named.py forced=True): in every plaza that has a forced bearer the top street, the only way
out, can not be reached from the south end of the plaza without stepping on one of the trigger cells, and it can be reached once the
trigger cells are walkable (so the check itself is not vacuous).

usage: test_forced.py            (reads the generated maps, needs no ROM)  Prints PASS or FAIL."""
import os
import re
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from areamodel import World, WARPTILE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))


def triggers(name):
    """Cells of the coord events that start a forced bearer's talk (script label ends in 'Trigger')."""
    out = set()
    path = os.path.join(ROOT, "maps/gen", f"{name}.asm")
    if not os.path.exists(path):
        return out  # a vanilla map
    for ln in open(path):
        m = re.match(r"\s*coord_event\s+(\d+),\s*(\d+),\s*-?\d+,\s*(\w+)Trigger\b", ln)
        if m:
            out.add((int(m[1]), int(m[2])))
    return out


def reach(w, mp, starts, avoid):
    seen = set(starts)
    q = deque(starts)
    while q:
        x, y = q.popleft()
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            n = (x + dx, y + dy)
            if n in seen or n in avoid:
                continue
            if not w.walkable(mp, n[0], n[1]) or mp.cell(n[0], n[1]) in WARPTILE:
                continue  # a door tile warps at once, it is no way through
            seen.add(n)
            q.append(n)
    return seen


def main():
    w = World()
    bad = []
    found = 0
    for name, mp in w.maps.items():
        trig = triggers(name)
        if not trig:
            continue
        found += 1
        bottom = [(x, 2 * mp.h - 1) for x in range(2 * mp.w) if w.walkable(mp, x, 2 * mp.h - 1)]
        top = lambda cells: [c for c in cells if c[1] == 0]  # noqa: E731
        blocked = reach(w, mp, bottom, trig)
        free = reach(w, mp, bottom, set())
        ok = not top(blocked) and bool(top(free))
        print(("ok   " if ok else "FAIL ") + f"{name}: triggers {sorted(trig)[:3]}.. top reachable around them: {bool(top(blocked))}, with them: {bool(top(free))}")
        if not ok:
            bad.append(name)
    if not found:
        print("FAIL no forced bearer found")
        bad.append("none")
    print("PASS" if not bad else "FAIL " + ", ".join(bad))
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
