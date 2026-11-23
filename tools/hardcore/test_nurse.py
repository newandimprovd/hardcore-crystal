#!/usr/bin/env python3
"""The POKéCENTER nurse, played through by key presses in the emulator.
Free in the Cherrygrove center only (it must say exactly what the base game nurse says), paid everywhere else, Tithe Lowtown included. A free nurse must never say a word about money, and the
text that turns a poor player away must never follow a successful heal.
usage: test_nurse.py TESTROM free|paid
The test ROM must start the player inside a center, one step below the counter (x=3, y=3)."""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(600, exit=True)
import gbtest  # noqa: E402

rom, mode = sys.argv[1], sys.argv[2]
t = gbtest.T(rom)
pb = t.pb
bad = []
CH = {0x7F: " ", 0xE8: ".", 0xE7: "!", 0xE6: "?", 0xF4: ",", 0xE0: "'", 0xF0: "¥"}
CH.update({0x80 + i: chr(65 + i) for i in range(26)})
CH.update({0xA0 + i: chr(97 + i) for i in range(26)})
CH.update({0xF6 + i: str(i) for i in range(10)})


def text():
    base = t.sym["wTilemap"][1]
    rows = []
    for r in range(18):
        rows.append("".join(CH.get(pb.memory[base + r * 20 + c], "~") for c in range(20)).replace("~", " ").strip())
    return " / ".join(x for x in rows[12:] if x)


def money():
    b, a = t.sym["wMoney"]
    v = [pb.memory[max(b, 1), a + i] for i in range(3)]
    return v[0] << 16 | v[1] << 8 | v[2]


def set_money(n):
    b, a = t.sym["wMoney"]
    for i in range(3):
        pb.memory[max(b, 1), a + i] = (n >> (16 - 8 * i)) & 255


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


gbtest.boot_to_overworld(t)
t.tick(120)
print("map", t.where(), "x,y", t.mem("wXCoord"), t.mem("wYCoord"))
set_money(5000)
# hurt the first mon so the heal is visible
hp_b, hp_a = t.sym["wPartyMon1HP"]
pb.memory[max(hp_b, 1), hp_a] = 0
pb.memory[max(hp_b, 1), hp_a + 1] = 1
before = money()
pb.button("up", 8)
t.tick(20)
pb.button("a", 4)
t.tick(30)
seen = []
idle = 0
for i in range(900):
    t.tick(6)
    tx = text()
    if tx and (not seen or seen[-1] != tx):
        seen.append(tx)
    if tx and i % 4 == 3:
        pb.button("a", 4)  # only while there is text: a press with none would start the talk again
    if not tx:
        idle += 1
        if idle > 60 and seen:
            break
    else:
        idle = 0
print("screens:")
for s in seen:
    print("   ", s)
low = " ".join(seen).lower()
after = money()
hp = pb.memory[max(hp_b, 1), hp_a] << 8 | pb.memory[max(hp_b, 1), hp_a + 1]
check("the party was healed", hp > 1, f"hp {hp}")
check("no 'cash up front' after a heal", "cash up front" not in low and "come back when" not in low)
if mode == "free":
    check("it cost nothing", after == before, f"{before} -> {after}")
    check("the nurse never mentions a price", "costs" not in low and "pay" not in low and "¥" not in low and "$" not in low)
else:
    check("it cost 40 per level of the best mon plus 200 (680 for a level 12)", before - after == 680, f"{before} -> {after}")
    check("the nurse names the price before healing", "costs" in low)
print("PASS" if not bad else f"FAIL: {bad}")
sys.exit(0 if not bad else 1)
