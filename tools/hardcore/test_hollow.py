#!/usr/bin/env python3
"""Hollows (alpha 3.2): from the first plaza of Tithe to the hidden portal of the Alms Cellar, through its fighters, hermits, balls and signs, and
back out to the lane.  Fights inside a hollow are plain fights: the kill counter must not move there.

usage: test_hollow.py ROM
ROM built like walk_all.sh does it (spawn of TithePlaza1, god mode):
  testbuild.sh hl TEST_MAP=TITHE_PLAZA1 TEST_X=.. TEST_Y=.. TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=0
Prints PASS or FAIL."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SHOTS", "/home/claude/scratch/hollow")
os.environ.setdefault("WALK_GOD", "1")
import test_purg as P  # noqa: E402
from test_walk import Walker  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
HOLLOW = os.environ.get("HOLLOW", "TitheAlmsCellar")


def const_of(name):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()


def lane_of(w, hollow):
    c = const_of(hollow)
    for name, mp in w.maps.items():
        if any(dest == c for (_, _, dest, _) in mp.warps):
            return name
    raise KeyError(hollow)


def bg_events(name):
    out = []
    for ln in open(os.path.join(ROOT, f"maps/gen/{name}.asm")):
        m = re.match(r"\s*bg_event\s+(\d+),\s*(\d+),\s*BGEVENT_READ,\s*(\w+)", ln)
        if m:
            out.append((int(m[1]), int(m[2]), m[3]))
    return out


def read_sign(wk, x, y):
    """Walk next to the sign tile, face it, press A and wait until the text is gone."""
    w = wk.w
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        cell = (wk.state()[0], x + dx, y + dy)
        if w.route(wk.state(), lambda s, c=cell: s == c) is not None and wk.go_state(lambda s, c=cell: s == c, f"next to sign {x},{y}"):
            wk.t.pb.button({(0, 1): "up", (0, -1): "down", (1, 0): "left", (-1, 0): "right"}[(dx, dy)], 9)
            wk.t.tick(24)
            wk.t.pb.button("a", 4)
            for _ in range(12):
                wk.t.tick(20)
                if wk.busy():
                    break
            ran = wk.busy()
            for _ in range(8):
                wk.t.pb.button("a", 4)
                wk.t.tick(30)
            wk.settle()
            return ran
    return False


def main():
    rom = sys.argv[1]
    wk = Walker(rom)
    t = wk.t
    wk.seen_map()
    lane = lane_of(wk.w, HOLLOW)
    P.check("spawn on a plaza", wk.state()[0].startswith("Tithe"), str(wk.state()))
    P.check(f"the portal lane {lane} is reached", wk.go(lane), str(wk.state()))
    P.check(f"the hidden portal leads into {HOLLOW}", wk.go(HOLLOW), str(wk.state()))
    wk.seen_map()
    k0 = P.kills(t)
    nb = P.pick_all(wk, HOLLOW)
    P.check(f"{HOLLOW}: {nb} balls picked up", nb == 2, str(nb))
    nt = P.talk_all(wk, HOLLOW)
    P.check(f"{HOLLOW}: {nt} hermits talked to", nt == 2, str(nt))
    c = const_of(HOLLOW)
    for i in range(2):
        P.check(f"hermit {i} gave its present", P.flag_get(t, f"EVENT_GEN_{c}_HGIFT{i}"))
    fought = 0
    for i, o in P.objects_of(wk, HOLLOW, lambda o: o["otype"] == "OBJECTTYPE_TRAINER"):
        if P.interact(wk, HOLLOW, i):
            fought += 1
    P.check(f"{HOLLOW}: {fought} fighters met", fought == 5, str(fought))
    for (x, y, label) in bg_events(HOLLOW):
        P.check(f"sign {label} reads", read_sign(wk, x, y))
    P.check("no kills counted inside the hollow", P.kills(t) == k0, f"{k0} -> {P.kills(t)}")
    P.check(f"the ladder leads back to {lane}", wk.go(lane), str(wk.state()))
    print("problems:", len(wk.log))
    for line in wk.log:
        print("  ", line)
    P.check("walker log clean", not wk.log)
    bad = [k for k, v in P.results.items() if not v]
    print("PASS" if not bad else "FAIL: " + ", ".join(bad))
    t.stop()
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
