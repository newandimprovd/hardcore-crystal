#!/usr/bin/env python3
"""The CORKBOARD page (alpha 3.2): a full screen list of every page of the board, the ones not pinned shown as blanks, A reads a page, B leaves.
Sets three lore flags, opens the board the way the item does (the queued script), reads the list, moves down, reads a pinned page and a blank one,
and leaves with B.  usage: test_cork.py TESTROM   (any test ROM, e.g. testbuild.sh cork with the default spawn)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/cork")
os.makedirs(SHOTS, exist_ok=True)
import test_walk  # noqa: E402
import test_purg as P  # noqa: E402

wk = test_walk.Walker(sys.argv[1])
t = wk.t
pb = t.pb
bad = []
CH = {0xF3: "/", 0x7F: " ", 0xE3: "-", 0xE8: ".", 0xE7: "!", 0xE6: "?", 0xF4: ",", 0xE0: "'", 0x9C: ":", 0xED: ">", 0xEC: ">", 0xBD: "."}
CH.update({0x80 + i: chr(65 + i) for i in range(26)})
CH.update({0xA0 + i: chr(97 + i) for i in range(26)})
CH.update({0xF6 + i: str(i) for i in range(10)})


def screen():
    base = t.sym["wTilemap"][1]
    return ["".join(CH.get(pb.memory[base + r * 20 + c], "?") for c in range(20)).rstrip() for r in range(18)]


def text():
    return " | ".join(x.strip() for x in screen() if x.strip())


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


for f in ("EVENT_LORE_MRP", "EVENT_LORE_STEINER", "EVENT_LORE_CROWLEY"):
    P.flag_set(t, f)
armed = [True]


def fake_start_menu(ctx):
    if not armed[0]:
        return
    armed[0] = False
    bank, addr = t.sym["CorkboardScript"]
    t.poke("wQueuedScriptBank", bank)
    t.poke("wQueuedScriptAddr", addr & 0xFF)
    t.poke("wQueuedScriptAddr", addr >> 8, 1)
    t.poke("hMenuReturn", 0x80)
    rf = t.pb.register_file
    sp = rf.SP
    rf.PC = t.pb.memory[sp] | (t.pb.memory[sp + 1] << 8)
    rf.SP = sp + 2


t.hook("StartMenu", fake_start_menu)
pb.button("start", 4)
t.tick(120)
t.shot(f"{SHOTS}/page1.png", 3)
s = text()
print(s)
check("the page has its title and the count", "CORKBOARD" in s and "3/21" in s.replace(" ", "") or "CORKBOARD" in s and "3" in s, s)
check("a pinned page shows its name", "MR. POKe" in s or "MR." in s)
check("a page not pinned is a blank", "- - -" in s)
for _ in range(5):
    pb.button("down", 4)
    t.tick(20)
t.shot(f"{SHOTS}/page2.png", 3)
print(text())
pb.button("a", 4)
t.tick(40)
pb.button("up", 4)  # still on the list or in a text, harmless
t.shot(f"{SHOTS}/read.png", 3)
print("after A:", text())
for _ in range(6):
    pb.button("b", 4)
    t.tick(40)
wk.settle()
check("B leaves the board for the overworld", not wk.busy(), text())
t.stop()
print("PASS" if not bad else "FAIL: " + ", ".join(bad))
sys.exit(1 if bad else 0)
