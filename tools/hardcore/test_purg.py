#!/usr/bin/env python3
"""Alpha 3 world: the junction outside Cherrygrove, Mr. POKeMON, Joyce and the CORKBOARD, then every floor of PURGATORIO with its item gates,
balls and talkers, Bruno at the Landing and the ending flags.  Fights down there must not count as kills.

usage: test_purg.py ROM
ROM built with: testbuild.sh pg TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=1
Screenshots of every entered map land in $SHOTS (default /home/claude/scratch/purg).  Prints PASS or FAIL."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SHOTS", "/home/claude/scratch/purg")
import test_walk  # noqa: E402
from test_walk import Walker, has_item, item_value  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
FACE_KEY = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
SKIP_SCRIPT = re.compile(r"(Gate\d*Script|BoulderScript|SealedScript)$")
results = {}


def flag_number(name):
    for ln in open(os.path.join(ROOT, "constants/area_event_flags.asm")):
        m = re.match(r"DEF (\w+) EQU (\d+)", ln)
        if m and m[1] == name:
            return int(m[2])
    raise KeyError(name)


def flag_get(t, name):
    n = flag_number(name)
    return (t.mem("wEventFlags", n // 8) >> (n % 8)) & 1


def flag_set(t, name):
    n = flag_number(name)
    t.poke("wEventFlags", t.mem("wEventFlags", n // 8) | (1 << (n % 8)), n // 8)


def kills(t):
    k = t.mem("wHCKillCount", 0, 2)
    return k[0] + 256 * k[1]


def face_and_press(wk, ox, oy):
    st = wk.state()
    d = FACE_KEY[(ox - st[1], oy - st[2])]
    wk.t.pb.button(d, 9)
    wk.t.tick(24)
    wk.t.pb.button("a", 4)
    wk.t.tick(20)
    wk.settle()
    wk.t.tick(30)


def adjacent_goal(name, ox, oy):
    return lambda s: s[0] == name and abs(s[1] - ox) + abs(s[2] - oy) == 1


def interact(wk, name, i):
    """Walk next to object i of map `name`, face it and press A until the script is over."""
    w = wk.w
    o = w.maps[name].objects[i]
    ox, oy = w.moved.get((name, i), (o["x"], o["y"]))
    if not wk.go_state(adjacent_goal(name, ox, oy), f"{name} next to {o['script']}"):
        return False
    face_and_press(wk, ox, oy)
    return True


def objects_of(wk, name, pred):
    w = wk.w
    return [(i, o) for i, o in enumerate(w.maps[name].objects) if (name, i) not in w.removed and pred(o)]


def talk(wk, name, suffix):
    found = objects_of(wk, name, lambda o: o["script"].endswith(suffix))
    if not found:
        wk.note(f"{name}: no object with script *{suffix}")
        return False
    return interact(wk, name, found[0][0])


def talk_all(wk, name):
    """Every plain talker of the map (not trainers, balls, gates, sealed rocks): a smoke test of each script and text."""
    n = 0
    for i, o in objects_of(wk, name, lambda o: o["otype"] == "OBJECTTYPE_SCRIPT" and not SKIP_SCRIPT.search(o["script"])
                           and o["sprite"] != "SPRITE_POKE_BALL"):
        if o["flag"] != "-1":
            continue  # hidden until some event
        if interact(wk, name, i):
            n += 1
        else:
            wk.note(f"{name}: could not reach talker {o['script']}")
    return n


def pick_all(wk, name):
    w = wk.w
    n = 0
    for i, o in objects_of(wk, name, lambda o: o["otype"] == "OBJECTTYPE_ITEMBALL"):
        if interact(wk, name, i):
            w.removed.add((name, i))
            n += 1
    return n


def cave_gates(wk, name):
    """Open every gate of a cave floor, in the order they can be reached.  Remove gates need the item (pair of rocks vanish);
    the boulder is pushed twice away from the player (CROWBAR)."""
    w = wk.w
    mp = w.maps[name]
    gate = re.compile(r"(Gate\d+Script|BoulderScript)$")
    for _ in range(10):
        todo = [(i, o) for i, o in objects_of(wk, name, lambda o: gate.search(o["script"])) if (name, i) not in w.moved]
        if not todo:
            return True
        opened = False
        for i, o in todo:
            gx, gy = o["x"], o["y"]
            for side, d in ((1, "up"), (-1, "down")):
                cur = wk.state()
                tgt = (name, gx, gy + side)
                if w.route(cur, lambda s: s == tgt) is None:
                    continue
                if not wk.go_state(lambda s: s == tgt, f"{name} at gate {o['script']}"):
                    continue
                wk.t.pb.button(d, 9)
                wk.t.tick(24)
                wk.t.pb.button("a", 4)
                wk.t.tick(20)
                wk.settle()
                if o["script"].endswith("BoulderScript"):
                    for _ in range(2):
                        wk.press_dir(d)
                    st = wk.state()
                    if st != (name, gx, gy + (-side)):
                        wk.note(f"{name}: boulder push left the player at {st}, expected {(name, gx, gy - side)}")
                        return False
                    w.moved[(name, i)] = (gx, gy - 2 * side)
                else:
                    for j, o2 in enumerate(mp.objects):
                        if o2["script"] == o["script"]:
                            w.removed.add((name, j))
                    wk.t.tick(30)
                opened = True
                break
            if opened:
                break
        if not opened:
            wk.note(f"{name}: no gate can be reached ({[o['script'] for _, o in todo]})")
            return False
    return False


def check(name, ok, detail=""):
    results[name] = bool(ok)
    print(("ok   " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))


def main():
    rom = sys.argv[1]
    wk = Walker(rom)
    t = wk.t
    wk.seen_map()
    check("spawn at the junction", wk.state()[0] == "TitheJunction", str(wk.state()))

    # ---- the west arm joins Tithe Road (connection offsets), and back
    ok = wk.go("TitheRoad") and wk.go("TitheJunction")
    check("junction <-> Tithe Road connection", ok, str(wk.state()))

    # ---- Mr. POKeMON: the scene, the POKeDEX, the vanishing
    ok = wk.go("FinneganHouse") and talk(wk, "FinneganHouse", "MrpScript")
    check("Mr. Pokemon scene runs", ok)
    check("  lore page and gone flags", flag_get(t, "EVENT_LORE_MRP") and flag_get(t, "EVENT_FINNEGAN_GONE"))
    t.tick(120)
    # ---- Joyce: the CORKBOARD
    ok = wk.go("TitheJunction") and talk(wk, "TitheJunction", "JoyceScript")
    check("Joyce gives the CORKBOARD", ok and has_item(wk, item_value("CORKBOARD")))
    check("  Joyce lore flag", flag_get(t, "EVENT_LORE_JOYCE"))

    # ---- the CORKBOARD script itself (queued the way the item effect does it)
    seen = []
    t.hook("CorkboardScript", lambda ctx: seen.append(1))
    bank, addr = t.sym["CorkboardScript"]
    t.poke("wQueuedScriptBank", bank)
    t.poke("wQueuedScriptAddr", addr & 0xFF)
    t.poke("wQueuedScriptAddr", addr >> 8, 1)
    t.pb.button("b", 4)
    t.tick(60)
    wk.settle()
    check("CorkboardScript runs and ends", bool(seen) and not wk.busy())

    # ---- open the ladder up (the Commune mouth counts as used) and walk Purgatorio
    flag_set(t, "EVENT_PURG_OPEN_A2")
    for i, o in enumerate(wk.w.maps["PurgThreshold"].objects):
        if o["script"].endswith("SealedScript") and o["x"] == 42:
            wk.w.removed.add(("PurgThreshold", i))
    plan = ["PurgThreshold", "PurgDown1", "PurgDown2", "PurgDown3", "PurgDown4", "PurgAbyss", "PurgThreshold",
            "PurgUp1", "PurgUp2", "PurgUp3", "PurgUp4", "PurgLanding"]
    fights0 = len(wk.fights)
    k0 = kills(t)
    for idx, name in enumerate(plan):
        if not wk.go(name):
            check(f"reach {name}", False)
            break
        wk.seen_map()
        if name == "PurgThreshold":
            if idx == 0:
                n = talk_all(wk, name)
                print(f"  {name}: {n} talkers")
            continue
        ok = cave_gates(wk, name)
        nb = pick_all(wk, name)
        nt = talk_all(wk, name)
        check(f"{name}: gates, {nb} balls, {nt} talkers", ok, str(wk.state()))
        if not ok:
            break

    # ---- Abyss lore flags (visited above): grave
    check("Abyss grave read", flag_get(t, "EVENT_ABYSS_GRAVE_READ"))
    check("Trumpet is in the bag", has_item(wk, item_value("TRUMPET")))

    # ---- Bruno
    if wk.state()[0] == "PurgLanding":
        ok = talk(wk, "PurgLanding", "BrunoScript")
        t.tick(200)
        wk.settle(6000)
        check("Bruno beaten, Nick reborn", flag_get(t, "EVENT_PURG_NICK"), str(wk.state()))
        check("Nick's lift back to the Threshold", wk.state()[0] == "PurgThreshold", str(wk.state()))
    else:
        check("Bruno reached", False, str(wk.state()))

    check("no kills counted in Purgatorio", kills(t) == k0, f"{k0} -> {kills(t)}")
    print("fights logged:", len(wk.fights) - fights0, "problems:", len(wk.log))
    for line in wk.log:
        print("  ", line)
    check("walker log clean", not wk.log)
    t.shot(f"{os.environ['SHOTS']}/end.png", 3)
    bad = [k for k, v in results.items() if not v]
    print("PASS" if not bad else "FAIL: " + ", ".join(bad))
    t.stop()
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
