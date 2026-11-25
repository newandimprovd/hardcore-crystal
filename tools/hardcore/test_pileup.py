#!/usr/bin/env python3
"""Stat pile-ups in a wild battle (alpha 3.3, playtest: tackle missed over 60 percent in the early game).
Walks in the grass of a plaza until a wild battle starts, gives the foe SAND-ATTACK and TACKLE only (and a lot of HP), then uses TACKLE for TURNS turns.
Reports the lowest accuracy stage the player sank to and the hit rate of the player's attacks.  PASS when the stage never falls below -1 (6) and at
least 80 percent of the attacks hit.  Run it on an old ROM too: the same test ends on a stage near the floor there.
Known limit (not finished): a foe from the flee list (data/wild/flee_mons.asm, in this roster also PORYGON) can run away and end the test before 20 attacks;
poke wTempEnemyMonSpecies or take another map.  What it showed so far: the 3.2 engine sank to -2 within 6 attacks, the fixed one stayed at -1 (13 of 15 hit).
usage: test_pileup.py ROM MAP_NAME   (ROM built with testbuild.sh and TEST_MAP at the grass cell of MAP_NAME, see spawn.py MAP grass)"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gbtest import T  # noqa: E402
import faulthandler  # noqa: E402
faulthandler.dump_traceback_later(900, exit=True)

TURNS = int(os.environ.get("TURNS", "40"))
rom, mapname = sys.argv[1], sys.argv[2]
sp = json.load(open(os.path.join(HERE, "spawns.json")))[mapname]
cx, hw = sp["grass"][0], sp["grass"][2]
t = T(rom)
pb = t.pb
for i in range(600):
    pb.button("a" if i % 2 else "start", 4)
    t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"):
        break
t.tick(200)
SAND, TACKLE = 0x1C, 33
log = []
cur = {}


def acc(ctx):
    cur["who"] = t.mem("hBattleTurn")
    cur["b"] = pb.register_file.B
    cur["lvl"] = t.mem("wPlayerAccLevel")


def res(hit):
    def f(ctx):
        log.append((cur.get("who"), cur.get("b"), cur.get("lvl"), hit))
    return f


for name, cb in (("BattleCommand_CheckHit.skip_brightpowder", acc), ("BattleCommand_CheckHit.Hit", res(True)), ("BattleCommand_CheckHit.Miss", res(False))):
    bank, addr = t.sym[name]
    pb.hook_register(bank, addr, cb, None)

CH = {0x7F: " "}
CH.update({0x80 + i: chr(65 + i) for i in range(26)})


def menu_up():
    base = t.sym["wTilemap"][1]
    txt = "".join(CH.get(pb.memory[base + r * 20 + c], "?") for r in range(18) for c in range(20))
    return "FIGHT" in txt and "RUN" in txt


steps = 0
while not t.mem("wBattleMode") and steps < 3000:
    x = t.where()[2]
    key = "right" if x <= cx - hw else "left" if x >= cx + hw else ("right" if (steps // 2) % 2 == 0 else "left")
    pb.button(key, 8)
    t.tick(20)
    steps += 1
if not t.mem("wBattleMode"):
    print("FAIL: no wild battle after", steps, "steps")
    sys.exit(1)
print("wild battle after", steps, "steps; mode", t.mem("wBattleMode"))
minlvl = 7
uses_sand = 0
seen = []
CH.update({0xA0 + i: chr(97 + i) for i in range(26)})
CH.update({0xE7: '!', 0xE8: '.', 0xF3: '/', 0xE3: '-', 0xE6: '?', 0xF4: ',', 0xE0: "'", 0x9C: ':'})
CH.update({0xF6 + i: str(i) for i in range(10)})
SCREENS = []
for i in range(5000):
    if not t.mem("wBattleMode"):
        break
    # the foe: SAND-ATTACK and TACKLE only; both sides stay alive
    for k, v in enumerate((SAND, TACKLE, 0, 0)):
        t.poke("wEnemyMonMoves", v, k)
    t.poke("wEnemyMonPP", 15, 0)
    t.poke("wEnemyMonPP", 35, 1)
    t.poke("wBattleMonMoves", TACKLE, 0)
    t.poke("wBattleMonPP", 35, 0)
    for hp in ("wEnemyMonHP", "wEnemyMonMaxHP", "wBattleMonHP", "wBattleMonMaxHP"):
        t.poke(hp, 3, 0)
        t.poke(hp, 0xE7, 1)
    mine = [l for l in log if l[0] == 0]
    if len(mine) >= TURNS:
        break
    if os.environ.get("DEBUG") and i % 8 == 0:
        print(f"   round {i}: foe {t.mem('wEnemyMonSpecies')} HP {t.mem('wEnemyMonHP') * 256 + t.mem('wEnemyMonHP', 1)} ours {t.mem('wBattleMonHP') * 256 + t.mem('wBattleMonHP', 1)} "
              f"menu {menu_up()} attacks so far {len(mine)}", flush=True)
    tx = " | ".join(x for x in ("".join(CH.get(pb.memory[t.sym["wTilemap"][1] + r * 20 + c], "?") for c in range(20)).strip() for r in range(18)) if x)
    if tx and (not SCREENS or SCREENS[-1] != tx):
        SCREENS.append(tx)
    if menu_up():
        pb.button("a", 4)  # FIGHT
        t.tick(40)
        pb.button("a", 4)  # the first move
        t.tick(30)
    else:
        pb.button("a", 4)
        t.tick(10)
if os.environ.get("DEBUG"):
    print("last screens:"); [print("   ", x) for x in SCREENS[-14:]]
print("battle mode at the end:", t.mem("wBattleMode"), "after", i, "rounds")
mine = [l for l in log if l[0] == 0]
minlvl = min([l[2] for l in mine] or [7])
print("accuracy stage at each of our attacks:", " ".join(f"{l[2] - 7:+d}{'h' if l[3] else 'm'}" for l in mine))
hits = sum(1 for l in mine if l[3])
rate = hits / max(1, len(mine))
print(f"player attacks {len(mine)}, hits {hits} ({rate:.0%}); lowest accuracy stage {minlvl - 7:+d}")
ok = len(mine) >= 20 and minlvl >= 6 and rate >= 0.8
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
