#!/usr/bin/env python3
"""Story tests (stage 7): the kill 200 news, the flooded and cratered New Bark Town, the portal.

usage:
  test_story.py milestone ROM   ROM = testbuild.sh stA TEST_MAP=TITHE_PLAZA1 TEST_X=3 TEST_Y=4 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
  test_story.py newbark ROM     ROM = testbuild.sh stB TEST_MAP=NEW_BARK_TOWN TEST_X=2 TEST_Y=8 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("WALK_GOD", "1")
import test_walk as tw  # noqa: E402
from gbtest import T  # noqa: E402

SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/story")
os.makedirs(SHOTS, exist_ok=True)
EV = tw.const_table("constants/event_flags.asm")


def getflag(t, name):
    i = EV[name]
    return (t.mem("wEventFlags", i // 8) >> (i % 8)) & 1


def setflag(t, name):
    i = EV[name]
    t.poke("wEventFlags", t.mem("wEventFlags", i // 8) | (1 << (i % 8)), i // 8)


def boot(rom):
    t = T(rom)
    for i in range(600):
        t.pb.button("a" if i % 2 else "start", 4)
        t.tick(20)
        if t.mem("wMapGroup") and t.mem("wXCoord"):
            break
    t.tick(200)
    return t


def milestone(rom):
    wk = tw.Walker(rom)
    t = wk.t
    wk.seen_map()
    t.poke("wHCKillCount", 199, 0)
    t.poke("wHCKillCount", 0, 1)
    ok = wk.go("TitheStreet1")
    ok = ok and wk.go("TitheStreet2")
    kills = t.mem("wHCKillCount", 0, 2)
    print("kills", kills[0] + 256 * kills[1], "tidal flag", getflag(t, "EVENT_HC_TIDAL_WAVE"))
    t.shot(f"{SHOTS}/milestone_end.png", 3)
    good = ok and getflag(t, "EVENT_HC_TIDAL_WAVE") == 1 and not wk.log
    print("PASS" if good else "FAIL")
    return good


def settle(t, limit=200):
    """Mash A while a script runs (the teacher at the west edge stops a player who has no Pokemon flagged)."""
    quiet = 0
    for _ in range(limit):
        if t.mem("wScriptRunning"):
            quiet = 0
            t.pb.button("a", 4)
            t.tick(16)
        else:
            quiet += 1
            t.tick(6)
            if quiet > 5:
                return


def step(t, d, n=1):
    for _ in range(n):
        t.press(d, hold=16, wait=6)
        settle(t)
    t.tick(10)


def cross_and_back(t, out, back):
    """Leave New Bark Town through its west edge and return so the map callbacks run again."""
    step(t, out, 4)
    t.tick(60)
    step(t, back, 4)
    t.tick(60)


def newbark(rom):
    """ROM built with TEST_STORY=2 and TEST_MAP=NEW_BARK_TOWN TEST_X=10 TEST_Y=10: the crater, the swirl above the player."""
    t = boot(rom)
    print("start", t.where())
    t.shot(f"{SHOTS}/nb_crater.png", 3)
    g0 = t.mem("wMapGroup")
    t.pb.button("up", 9)
    t.tick(20)
    t.pb.button("a", 4)
    t.tick(60)
    t.shot(f"{SHOTS}/nb_portal_text.png", 3)
    for i in range(60):  # text pages, then the yes/no prompt: A picks YES
        t.pb.button("a", 4)
        t.tick(30)
        if i == 4:
            t.shot(f"{SHOTS}/nb_portal_text.png", 3)
        if t.mem("wMapGroup") != g0:
            break
    t.tick(120)
    print("after portal", t.where())
    t.shot(f"{SHOTS}/nb_after.png", 3)
    ok = t.mem("wMapGroup") != g0
    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    mode, rom = sys.argv[1], sys.argv[2]
    ok = {"milestone": milestone, "newbark": newbark}[mode](rom)
    sys.exit(0 if ok else 1)
