#!/usr/bin/env python3
"""EXP for the benched party members (alpha 3.2, playtest point 4): the battle text announces what each mon of the party gained, and the "grew to level"
line names the mon that grew, not the foe that was defeated.
Gives the lone test mon a benched partner called BENCH that is one EXP short of level 13, then wins the first trainer fight (the foe's HP is set to 1 at
every battle menu, the keys do the rest) and reads the text screens.
usage: test_exp.py TESTROM  (testbuild.sh ui TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=8 TEST_MON=TOTODILE TEST_LEVEL=12 TEST_REVEALED=1)"""
import faulthandler
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(900, exit=True)
SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/exp")
os.makedirs(SHOTS, exist_ok=True)
import gbtest  # noqa: E402
gbtest.T.hook = lambda self, label, fn: None  # keys only
import test_walk  # noqa: E402

wk = test_walk.Walker(sys.argv[1])
t = wk.t
pb = t.pb
bad = []

CH = {0x7F: " ", 0xE3: "-", 0xE8: ".", 0xE7: "!", 0xE6: "?", 0xF4: ",", 0xE0: "'", 0x9C: ":", 0xF3: "/"}
CH.update({0x80 + i: chr(65 + i) for i in range(26)})
CH.update({0xA0 + i: chr(97 + i) for i in range(26)})
CH.update({0xF6 + i: str(i) for i in range(10)})
PARTY_MON = 48
NICK = 11


def text():
    base = t.sym["wTilemap"][1]
    rows = []
    for r in range(18):
        s = "".join(CH.get(pb.memory[base + r * 20 + c], "?") for c in range(20)).strip()
        if s:
            rows.append(s)
    return " | ".join(rows)


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


def addr(name, off=0):
    bank, a = t.sym[name]
    return a + off


def put(name, off, val):
    pb.memory[addr(name, off)] = val


def make_bench():
    """A second party member: a copy of the first with another nickname and EXP one short of level 13 (medium slow growth: 1261 at 13)."""
    for i in range(PARTY_MON):
        put("wPartyMon2", i, pb.memory[addr("wPartyMon1", i)])
    put("wPartyMon2", 0x08, 0x00)  # MON_EXP, three bytes, big endian
    put("wPartyMon2", 0x09, 0x04)
    put("wPartyMon2", 0x0A, 0xEC)  # 1260
    put("wPartySpecies", 1, pb.memory[addr("wPartySpecies", 0)])
    put("wPartySpecies", 2, 0xFF)
    put("wPartyCount", 0, 2)
    for i, c in enumerate("BENCH"):
        put("wPartyMonNicknames", NICK + i, 0x80 + ord(c) - 65)
    put("wPartyMonNicknames", NICK + 5, 0x50)


def fight():
    make_bench()
    level_before = pb.memory[addr("wPartyMon2", 0x1F)]
    screens = []
    for i in range(2500):
        if not t.mem("wBattleMode"):
            break
        tx = text()
        if tx and (not screens or screens[-1] != tx):
            screens.append(tx)
        if "FIGHT" in tx and "RUN" in tx:
            put("wEnemyMonHP", 0, 0)
            put("wEnemyMonHP", 1, 1)
            put("wBattleMonMoves", 0, 33)  # TACKLE
            put("wBattleMonPP", 0, 30)
            pb.button("a", 4)
            t.tick(40)
            pb.button("a", 4)
            t.tick(30)
            continue
        pb.button("a", 4)
        t.tick(10)
    t.tick(60)
    low = " || ".join(screens)
    exp_lines = [s for s in screens if "gained" in s.lower() or "grew" in s.lower() or "EXP" in s]
    print("exp screens:")
    for s in exp_lines[:14]:
        print("   ", s)
    check("a fight was fought", len(screens) > 3)
    check("the fighter's EXP line is shown", any("TOTODILE gained" in s or "gained" in s and "TOTODILE" in s for s in exp_lines) or any("gained" in s.lower() for s in exp_lines))
    check("the benched mon's EXP line is shown by its own name", any("BENCH gained" in s for s in exp_lines), "")
    check("the benched mon's level up names it", any("BENCH grew to" in s and "level 13" in s for s in exp_lines),
          f"level {level_before} -> {pb.memory[addr('wPartyMon2', 0x1F)]}")
    foe_names = ("CATERPIE", "WEEDLE", "RATTATA", "PIDGEY", "STARLY", "NIDORAN")
    check("no level up line names a foe", not any("grew" in s and any(f in s.upper() for f in foe_names) for s in exp_lines))
    print("PASS" if not bad else f"FAIL: {bad}")
    sys.exit(0 if not bad else 1)


def settle(self, limit=3000):
    for i in range(limit):
        if t.mem("wBattleMode"):
            fight()
        if self.busy():
            t.pb.button("a", 4)
            t.tick(16)
        else:
            t.tick(6)
            if i > 8:
                break
    return i


test_walk.Walker.settle = settle
wk.pay_bearers()
wk.go("TithePokecenter1")
print("FAIL: no battle")
sys.exit(1)
