#!/usr/bin/env python3
"""The opening of alpha 3.1: the rival on the road, Mr. POKeMON's house (not optional), the CORKBOARD and POKeDEX handover, Joyce walking up
to the player outside (not optional) and his lore talk afterwards.

usage: test_opening.py ROM
ROM built with: testbuild.sh op TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
Screenshots of the cutscenes land in $SHOTS (default /home/claude/scratch/op).  Prints PASS or FAIL."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SHOTS", "/home/claude/scratch/op")
os.environ.setdefault("WALK_GOD", "1")
import test_walk  # noqa: E402
import test_purg  # noqa: E402
from test_walk import Walker, has_item, item_value  # noqa: E402
from test_purg import flag_get  # noqa: E402

SHOTS = os.environ["SHOTS"]
os.makedirs(SHOTS, exist_ok=True)
results = {}
STARTERS = {152, 155, 158}  # CHIKORITA CYNDAQUIL TOTODILE


def check(name, ok, detail=""):
    results[name] = bool(ok)
    print(("ok   " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))


def pokedex_flag(t):
    return t.mem("wStatusFlags") & 1


def play_until(wk, pred, limit=500, shots=None, tag="s", idle=True):
    """Press A while a script runs (a cutscene), looking at the screen now and then, until pred(state) holds and the script is over."""
    t = wk.t
    n = 0
    quiet = 0
    for i in range(limit):
        st = wk.raw_state()
        # a scene queued for the next map starts a tick after the arrival: the state has to stay quiet for a while
        quiet = quiet + 1 if (not t.mem("wScriptRunning") and not t.mem("wBattleMode")) else 0
        if pred(st) and (not idle or quiet >= 4):
            return True
        if t.mem("wScriptRunning") or t.mem("wBattleMode"):
            if shots is not None and i % 6 == 0 and n < shots:
                t.shot(f"{SHOTS}/{tag}{n:02d}.png", 2)
                n += 1
            t.pb.button("a", 4)
        t.tick(16)
    return False


def opening(wk, check=check):
    """The whole opening from the spawn on the stem: the checks go to `check` (test_purg plays it before its own steps)."""
    t = wk.t
    check("spawn at the junction (stem)", wk.state() == ("TitheJunction", 19, 20), str(wk.state()))

    # ---- the rival: the whole width of the road is a trigger, he is beaten before anything else
    n0 = len(wk.fights)
    for _ in range(3):
        wk.press_dir("up")
    check("rival fight starts on the stem", len(wk.fights) == n0 + 1 and wk.fights[-1]["n"] == 2, str(wk.fights[n0:]))
    if len(wk.fights) > n0:
        party = wk.fights[-1]["party"]
        check("  rival carries a starter", party[-1] in STARTERS, str(party))
    check("  rival flag set", flag_get(t, "EVENT_NAMED_RIVAL0_DONE"))

    # ---- the forced walk to Mr. POKeMON's door: the first step onto the road, nobody can pass
    while wk.state()[2] > 12:
        wk.press_dir("up")
    check("still on the stem before the road", wk.state()[0] == "TitheJunction" and wk.state()[2] == 12, str(wk.state()))
    check("  not yet met Mr. POKeMON", not flag_get(t, "EVENT_FINNEGAN_GONE"))
    t.pb.button("up", 9)
    t.tick(23)
    ok = play_until(wk, lambda s: s[0] == "FinneganHouse", limit=200, shots=4, tag="call", idle=False)
    check("the road pulls the player into the house", ok, str(wk.raw_state()))
    # the scene runs by itself on arrival (re-entry script)
    ok = play_until(wk, lambda s: s[0] == "TitheJunction", limit=900, shots=10, tag="mrp")
    check("Mr. POKeMON's scene runs and the player is walked out", ok, str(wk.raw_state()))
    check("  CORKBOARD in the bag", has_item(wk, item_value("CORKBOARD")))
    check("  POKeDEX flag set", pokedex_flag(t) == 1)
    check("  gone and lore flags", flag_get(t, "EVENT_FINNEGAN_GONE") and flag_get(t, "EVENT_LORE_MRP"))

    # ---- Joyce: he walks up to the player, nobody has to talk to him
    check("Joyce scene played out on the road", flag_get(t, "EVENT_JOYCE_MET"), str(wk.raw_state()))
    check("  Joyce has not told his lore yet", not flag_get(t, "EVENT_JOYCE_TOLD") and not flag_get(t, "EVENT_LORE_JOYCE"))
    wk.settle()
    t.shot(f"{SHOTS}/after_joyce_scene.png", 2)
    st = wk.state()
    check("  player may move after the scene", st[0] == "TitheJunction", str(st))

    # ---- the later talk with Joyce: the lore, once
    ok = test_purg.talk(wk, "TitheJunction", "JoyceScript")
    check("Joyce talk runs", ok)
    check("  lore told", flag_get(t, "EVENT_JOYCE_TOLD") and flag_get(t, "EVENT_LORE_JOYCE"))

    # ---- the house is only a chair now
    ok = wk.go("FinneganHouse")
    check("the house can be entered again without a scene", ok and not t.mem("wScriptRunning"), str(wk.state()))
    wk.settle()


def main():
    wk = Walker(sys.argv[1])
    wk.seen_map()
    opening(wk)
    bad = [k for k, v in results.items() if not v]
    print("PASS" if not bad else "FAIL " + ", ".join(bad))
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
