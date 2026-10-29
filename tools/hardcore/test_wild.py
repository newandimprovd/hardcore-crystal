#!/usr/bin/env python3
"""In-game wild encounter test: walks back and forth in the tall grass of one plaza until N wild battles have started, checks every
species and level against the generated table for the time of day, runs from most of them, fights and catches some, and checks
that a wild kill does not count as a trainer kill.

usage: test_wild.py ROM MAP_NAME [N]
ROM built with: testbuild.sh wild1 TEST_MAP=TITHE_PLAZA1 TEST_X=12 TEST_Y=12 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
(the player starts on plaza floor to the west of the east grass patch)"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gbtest import T  # noqa: E402
from areamodel import World  # noqa: E402
from test_walk import const_table, find_ids, pick_move  # noqa: E402

SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/wild")
os.makedirs(SHOTS, exist_ok=True)


def shuffle_key(t, steps):
    """Stay inside the east patch (cells 14..23): walk right until deep in the grass, then back and forth."""
    x = t.where()[2]
    if x <= 15:
        return "right"
    if x >= 22:
        return "left"
    return "right" if (steps // 3) % 2 == 0 else "left"


def main():
    rom, mapname = sys.argv[1], sys.argv[2]
    want = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    spec = json.load(open(os.path.join(HERE, "wild_out.json")))
    entry = next(e for e in spec["entries"] if e["map"] == mapname)
    species = const_table("constants/pokemon_constants.asm")
    names = {}
    for k, v in species.items():
        names.setdefault(v, k)
    ids = find_ids(World())
    by_name = {n: gn for gn, n in ids.items()}
    t = T(rom)
    for i in range(600):
        t.pb.button("a" if i % 2 else "start", 4)
        t.tick(20)
        if t.mem("wMapGroup") and t.mem("wXCoord"):
            break
    t.tick(200)
    problems = []
    g, n, x, y = t.where()
    print("start", (g, n, x, y), "expected map", by_name[mapname])
    if (g, n) != by_name[mapname]:
        print("!! not in the expected map")
        return 1
    seen = []
    state = {"flag": False}

    def menu(ctx):
        if not state["flag"]:
            state["flag"] = True
            state["rec"] = dict(sp=names.get(t.mem("wEnemyMonSpecies")), lv=t.mem("wEnemyMonLevel"), tod=t.mem("wTimeOfDay"),
                                battle=t.mem("wBattleMode"), kills=t.mem("wHCKillCount") + 256 * t.mem("wHCKillCount", 1))
    t.hook("BattleMenu", menu)
    kills0 = t.mem("wHCKillCount") + 256 * t.mem("wHCKillCount", 1)
    steps = 0
    shot_done = False
    while len(seen) < want and steps < 4000:
        if t.mem("wBattleMode") and not state["flag"]:
            # the encounter has started: confirm the "appeared!" text until the battle menu comes up (the hook sets the flag)
            for _ in range(80):
                t.press("a", hold=3, wait=10)
                if state["flag"]:
                    break
        else:
            # step into the grass and shuffle around inside it
            key = shuffle_key(t, steps)
            t.pb.button(key, 8)
            t.tick(20)
            steps += 1
        if state["flag"]:
            rec = state["rec"]
            state["flag"] = False
            seen.append(rec)
            if not shot_done:
                t.shot(os.path.join(SHOTS, f"{mapname}_battle.png"), 2)
                shot_done = True
            # run away: RUN is down, right on the battle menu
            t.tick(60)  # the hook fires before the menu is drawn
            for k in ("down", "right", "a"):
                t.press(k, hold=4, wait=20)
            for _ in range(40):
                t.press("b", hold=3, wait=10)
                if t.mem("wBattleMode") == 0:
                    break
            t.tick(30)
            if t.mem("wBattleMode") != 0:
                problems.append("could not leave the wild battle")
                break
            # the escape leaves the player where he stood: walk out of any text and carry on
            for _ in range(6):
                t.press("b", hold=3, wait=8)
    # one wild battle fought to the end, and one ball thrown: the player's own mon is far stronger, so attack until it is over
    caught0 = t.mem("wPartyCount")
    for attempt in ("fight", "ball"):
        for _ in range(400):
            if t.mem("wBattleMode"):
                break
            t.pb.button(shuffle_key(t, steps), 8)
            t.tick(20)
            steps += 1
        for _ in range(80):
            t.press("a", hold=3, wait=10)
            if state["flag"]:
                break
        state["flag"] = False
        t.tick(60)
        # a damaging move that the enemy does not resist, and a sure catch rate (the test is about the flow, not about luck)
        t.poke("wBattleMonMoves", pick_move(t.mem("wEnemyMonType1"), t.mem("wEnemyMonType2")), 0)
        t.poke("wBattleMonPP", 30, 0)
        t.poke("wCurMoveNum", 0)
        t.poke("wEnemyMonCatchRate", 255)
        t.poke("wPlayerAccLevel", 13)  # +6: no misses, a miss only makes the test slower and flaky
        t.poke("wEnemyEvaLevel", 1)
        if attempt == "fight":
            t.poke("wEnemyMonHP", 0, 0)
            t.poke("wEnemyMonHP", 1, 1)
            for _ in range(60):
                t.press("a", hold=3, wait=12)
                if not t.mem("wBattleMode"):
                    break
            if t.mem("wBattleMode"):
                problems.append("the wild battle did not end after the enemy fainted")
        else:
            # PACK is below FIGHT; the Balls pocket is one to the right of the Items pocket; the enemy is at 1 HP and asleep-free,
            # so a handful of balls always catches it
            for throw in range(8):
                t.poke("wEnemyMonHP", 0, 0)
                t.poke("wEnemyMonHP", 1, 1)
                for k in ("down", "a", "right", "a", "a"):
                    t.press(k, hold=4, wait=50)  # the Pack screen ignores input while it opens
                state["flag"] = False
                for _ in range(120):
                    t.press("b", hold=3, wait=12)  # B: advances text and answers the nickname question with NO
                    if state["flag"] or not t.mem("wBattleMode"):
                        break
                if not t.mem("wBattleMode"):
                    break
                state["flag"] = False
                t.tick(60)
            if t.mem("wBattleMode"):
                problems.append("the ball battle did not end")
            elif t.mem("wPartyCount") != caught0 + 1:
                problems.append(f"ball thrown, party {caught0} -> {t.mem('wPartyCount')}")
            else:
                print("caught:", names.get(t.mem("wPartySpecies", t.mem("wPartyCount") - 1)), "after", throw + 1, "ball(s)")
        for _ in range(12):
            t.press("b", hold=3, wait=8)
    kills1 = t.mem("wHCKillCount") + 256 * t.mem("wHCKillCount", 1)
    if kills1 != kills0:
        problems.append(f"kill counter changed {kills0} -> {kills1} during wild battles")
    tod_names = ["morn", "day", "nite"]
    count = Counter()
    for rec in seen:
        tod = rec["tod"] if rec["tod"] < 3 else 1
        table = entry[tod_names[tod]]
        ok = [(lv, sp) for lv, sp in table if sp == rec["sp"] and lv == rec["lv"]]
        if not ok:
            problems.append(f"{mapname} {tod_names[tod]}: got {rec['sp']} L{rec['lv']}, not in {table}")
        count[rec["sp"]] += 1
        if rec["battle"] != 1:
            problems.append(f"battle mode {rec['battle']} for a wild encounter ({rec['sp']})")
    print(f"{len(seen)} encounters in {steps} steps, {len(count)} species: {dict(count.most_common())}")
    print(f"steps per encounter {steps / max(1, len(seen)):.1f}")
    if len(seen) < want:
        t.shot(os.path.join(SHOTS, f"{mapname}_stuck.png"), 2)
        problems.append(f"only {len(seen)} of {want} encounters in {steps} steps (at {t.where()}, battle mode {t.mem('wBattleMode')})")
    if problems:
        print("problems:", len(problems))
        for p in problems[:20]:
            print("  !!", p)
        print("FAIL")
        return 1
    print("problems: 0")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
