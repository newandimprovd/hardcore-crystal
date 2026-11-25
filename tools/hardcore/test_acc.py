#!/usr/bin/env python3
"""Hit rate of TACKLE in a real trainer battle (alpha 3.2 playtest: "tackle misses over 60 percent of the time").
Starts the first trainer battle of a test ROM like test_battle_ui.py, gives the lead mon TACKLE only, keeps both sides alive and uses it TURNS times.
Hooks BattleCommand_CheckHit: logs the accuracy byte that is compared with the random number (register B at skip_brightpowder), the stat levels and
whether the attack hit or missed.  PASS when the hit rate is at least 85 percent (the move says 95).
usage: test_acc.py TESTROM"""
import collections
import faulthandler
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(900, exit=True)
import gbtest  # noqa: E402
gbtest.T.hook = lambda self, label, fn: None
import test_walk  # noqa: E402

TURNS = int(os.environ.get("TURNS", "60"))
wk = test_walk.Walker(sys.argv[1])
t = wk.t
pb = t.pb
log = []  # (turn flag, acc byte, own acc level, foe eva level, result)
state = {"b": None, "who": None}


def sym(name):
    return t.sym[name]


def put(name, off, val):
    t.poke(name, val, off)


def get(name, off=0):
    return t.mem(name, off)


def cb_acc(ctx):
    state["b"] = pb.register_file.B
    state["who"] = get("hBattleTurn")
    state["lv"] = (get("wPlayerAccLevel"), get("wPlayerEvaLevel"), get("wEnemyAccLevel"), get("wEnemyEvaLevel"))


def cb_hit(ctx):
    log.append((state["who"], state["b"], state["lv"], "hit"))


def cb_miss(ctx):
    log.append((state["who"], state["b"], state["lv"], "miss"))


def probe():
    for name, cb in (("BattleCommand_CheckHit.skip_brightpowder", cb_acc), ("BattleCommand_CheckHit.Hit", cb_hit), ("BattleCommand_CheckHit.Miss", cb_miss)):
        bank, addr = sym(name)
        pb.hook_register(bank, addr, cb, None)
    turns = 0
    for i in range(6000):
        if not t.mem("wBattleMode"):
            break
        base = t.sym["wTilemap"][1]
        tx = "".join(chr(pb.memory[base + r * 20 + c]) if 0x20 <= pb.memory[base + r * 20 + c] < 0x7F else "?" for r in range(18) for c in range(20))
        pb.tick(6, False)
        # the lead mon: TACKLE in slot 1, lots of PP, and both sides stay alive
        put("wBattleMonMoves", 0, 33)
        put("wBattleMonPP", 0, 35)
        put("wPartyMon1Moves", 0, 33)
        put("wPartyMon1PP", 0, 35)
        for hp in ("wBattleMonHP", "wPartyMon1HP"):
            put(hp, 0, 3)
            put(hp, 1, 0xE7)
        put("wEnemyMonHP", 0, 3)
        put("wEnemyMonHP", 1, 0xE7)
        if len([1 for l in log if l[0] == 0]) >= TURNS:
            break
        pb.button("a", 4)
        t.tick(10)
    mine = [l for l in log if l[0] == 0]
    theirs = [l for l in log if l[0] != 0]
    hits = sum(1 for l in mine if l[3] == "hit")
    print(f"our checks {len(mine)}: hits {hits}, misses {len(mine) - hits}")
    print("accuracy bytes seen:", collections.Counter(l[1] for l in mine).most_common(5))
    print("stat levels (our acc, our eva, foe acc, foe eva) seen:", collections.Counter(l[2] for l in mine).most_common(4))
    if theirs:
        h2 = sum(1 for l in theirs if l[3] == "hit")
        print(f"foe checks {len(theirs)}: hits {h2}; bytes {collections.Counter(l[1] for l in theirs).most_common(4)}")
    rate = hits / max(1, len(mine))
    ok = len(mine) >= 20 and rate >= 0.85
    print(f"hit rate {rate:.0%}", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def settle(self, limit=3000):
    for i in range(limit):
        if t.mem("wBattleMode"):
            probe()
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
