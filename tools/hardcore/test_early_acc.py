#!/usr/bin/env python3
"""The first fights of the road with a level 5 starter, played with the lead mon's first move only (usually TACKLE): per battle the hit rate of our attacks,
the lowest accuracy stage we sank to, and which moves the foe used.  Finds out whether the early game is made hard by foe moves that lower accuracy.
usage: test_early_acc.py TESTROM   (testbuild.sh acc5 TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=8 TEST_MON=CYNDAQUIL TEST_LEVEL=5)"""
import collections
import faulthandler
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(1500, exit=True)
import gbtest  # noqa: E402
gbtest.T.hook = lambda self, label, fn: None
import test_walk  # noqa: E402

MAXB = int(os.environ.get("BATTLES", "6"))
wk = test_walk.Walker(sys.argv[1])
t = wk.t
pb = t.pb
cur = {}
battles = []
hooked = []
MOVES = {}
try:
    for l in open("/home/claude/pokecrystal/constants/move_constants.asm"):
        pass
except OSError:
    pass


def get(name, off=0):
    return t.mem(name, off)


def cb_acc(ctx):
    who = get("hBattleTurn")
    cur["pending"] = (who, pb.register_file.B, get("wPlayerAccLevel"),
                      get("wPlayerMoveStruct") if who == 0 else get("wEnemyMoveStruct"))


def cb_res(hit):
    def f(ctx):
        p = cur.get("pending")
        if p:
            cur.setdefault("log", []).append(p + (hit,))
    return f


def hook_all():
    if hooked:
        return
    for name, cb in (("BattleCommand_CheckHit.skip_brightpowder", cb_acc), ("BattleCommand_CheckHit.Hit", cb_res(True)), ("BattleCommand_CheckHit.Miss", cb_res(False))):
        bank, addr = t.sym[name]
        pb.hook_register(bank, addr, cb, None)
        hooked.append(name)


def probe():
    hook_all()
    cur.clear()
    mode = t.mem("wBattleMode")
    foe = get("wEnemyMonSpecies")
    foelv = get("wEnemyMonLevel")
    mine_lv = get("wBattleMonLevel")
    for i in range(4000):
        if not t.mem("wBattleMode"):
            break
        base = t.sym["wTilemap"][1]
        pb.tick(6, False)
        # we never faint (this is about the hit rate, not about winning), the foe has its real HP
        t.poke("wBattleMonHP", 3, 0)
        t.poke("wBattleMonHP", 0xE7, 1)
        pb.button("a", 4)
        t.tick(10)
    log = cur.get("log", [])
    mine = [l for l in log if l[0] == 0]
    theirs = [l for l in log if l[0] != 0]
    hits = sum(1 for l in mine if l[4])
    battles.append(dict(foe=foe, foelv=foelv, mode=mode, checks=len(mine), hits=hits, minacc=min([l[2] for l in mine] or [7]),
                        bytes=collections.Counter(l[1] for l in mine).most_common(3), foe_bytes=collections.Counter(l[1] for l in theirs).most_common(3)))
    b = battles[-1]
    print(f"battle {len(battles)}: foe #{b['foe']} L{b['foelv']} mode {b['mode']}: our attacks {b['checks']}, hits {b['hits']}; lowest accuracy stage {b['minacc']}; "
          f"our bytes {b['bytes']}; foe bytes {b['foe_bytes']}", flush=True)
    if len(battles) >= MAXB:
        tot = sum(b['checks'] for b in battles)
        hit = sum(b['hits'] for b in battles)
        print(f"total: {hit} of {tot} hit ({hit / max(1, tot):.0%})")
        sys.exit(0)


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
try:
    wk.go("TithePokecenter1")
except SystemExit:
    raise
print("walk ended")
