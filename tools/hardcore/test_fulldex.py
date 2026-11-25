#!/usr/bin/env python3
"""The ending ROM (alpha 3.3): every species caught and stored in the PC, the whole Pokedex complete, the player named CHRIS.
usage: test_fulldex.py ROM    ROM = testbuild.sh NAME TEST_MAP=JUDECCA_CENTRE TEST_X=4 TEST_Y=17 TEST_MON=DEATHROLL TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2 TEST_FULLDEX=1 TEST_NAME=CHRIS
Checks: the name, the seen and caught bits of every species, and that boxes 1 to 13 hold each species exactly once at level 100 with the player as OT."""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(600, exit=True)
from gbtest import T  # noqa: E402

NUM = int(os.environ.get("NUM_POKEMON", "248"))
rom = sys.argv[1]
t = T(rom)
pb = t.pb
for i in range(600):
    pb.button("a" if i % 2 else "start", 4)
    t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"):
        break
t.tick(200)
bad = []


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


CH = {0x50: ""}
CH.update({0x80 + i: chr(65 + i) for i in range(26)})
CH.update({0xA0 + i: chr(97 + i) for i in range(26)})
name = "".join(CH.get(b, "?") for b in t.mem("wPlayerName", 0, 8)).split("")[0] if False else ""
raw = t.mem("wPlayerName", 0, 8)
for b in raw:
    if b == 0x50:
        break
    name += CH.get(b, "?")
check("the player is named CHRIS", name == "CHRIS", repr(name))


def bits(sym):
    data = t.mem(sym, 0, 32)
    return {i + 1 for i in range(256) if data[i // 8] >> (i % 8) & 1}


caught, seen = bits("wPokedexCaught"), bits("wPokedexSeen")
want = set(range(1, NUM + 1))
check("every species is caught in the Pokedex", want <= caught, f"{len(caught & want)} of {NUM}")
check("every species is seen in the Pokedex", want <= seen, f"{len(seen & want)} of {NUM}")

found = []
levels = set()
ots = set()
for box in range(1, 15):
    b, a = t.sym[f"sBox{box}"]
    cnt = pb.memory[b, a]
    if cnt == 0xFF or cnt > 20:
        check(f"box {box} has a sane count", False, str(cnt))
        continue
    sp = [pb.memory[b, a + 1 + k] for k in range(cnt)]
    found += sp
    mons = a + 1 + 21
    for k in range(cnt):
        levels.add(pb.memory[b, mons + k * 32 + 31])
    ot = a + 1 + 21 + 32 * 20
    for k in range(cnt):
        s = ""
        for c in range(11):
            v = pb.memory[b, ot + k * 11 + c]
            if v == 0x50:
                break
            s += CH.get(v, "?")
        ots.add(s)
    print(f"   box {box}: {cnt} mons")
check("each species is in the PC exactly once", sorted(found) == sorted(want), f"{len(found)} mons, {len(set(found))} different")
check("all of them are level 100", levels == {100}, str(sorted(levels)))
check("the original trainer of all of them is CHRIS", ots == {"CHRIS"}, str(sorted(ots)))
print("PASS" if not bad else f"FAIL {bad}")
sys.exit(0 if not bad else 1)
