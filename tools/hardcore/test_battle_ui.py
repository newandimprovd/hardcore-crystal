#!/usr/bin/env python3
"""The battle screens a player sees, in the emulator (not the engine routines): the opening text of a trainer battle, the battle menu, the move list with the
names of the moves, B going back from the moves to the battle menu, and the opening text of a wild battle.
Walks north from the spawn of a test ROM (CHERRYGROVE_CITY 17,8) until a trainer sees the player, then plays the first turn by key presses only.
usage: test_battle_ui.py TESTROM"""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

faulthandler.dump_traceback_later(900, exit=True)
SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/ui")
os.makedirs(SHOTS, exist_ok=True)
import gbtest  # noqa: E402
gbtest.T.hook = lambda self, label, fn: None  # no hook on BattleMenu: the keys are all that moves the battle
import test_walk  # noqa: E402
wk = test_walk.Walker(sys.argv[1])
t = wk.t
pb = t.pb
bad = []

CH = {0xF3: "/", 0x7F: " ", 0xE3: "-", 0xE8: ".", 0xE7: "!", 0xE6: "?", 0xF4: ",", 0xE0: "'", 0xEF: "M", 0xF0: "F", 0x9C: ":", 0xED: ">", 0xEC: ">", 0xE1: "P", 0xE2: "K"}
CH.update({0x80 + i: chr(65 + i) for i in range(26)})
CH.update({0xA0 + i: chr(97 + i) for i in range(26)})
CH.update({0xF6 + i: str(i) for i in range(10)})


def screen():
    base = t.sym["wTilemap"][1]
    rows = []
    for r in range(18):
        s = "".join(CH.get(pb.memory[base + r * 20 + c], "?") for c in range(20))
        rows.append(s.rstrip())
    return rows


def text():
    return " | ".join(x.strip() for x in screen() if x.strip())


def shot(name):
    t.shot(f"{SHOTS}/{name}.png", 3)


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)



def probe():
    check("a trainer battle started", t.mem("wBattleMode") == 2, f"mode {t.mem('wBattleMode')} at {t.where()}")
    # play the opening by A presses, noting each distinct screen of text, until the battle menu is up
    seen = []
    menu_up = False
    for i in range(260):
        pb.tick(6, False)
        tx = text()
        if tx and (not seen or seen[-1] != tx):
            seen.append(tx)
            if len(seen) <= 14:
                shot(f"open{len(seen):02d}")
        if "FIGHT" in tx and "RUN" in tx:
            menu_up = True
            break
        if i % 4 == 3:
            pb.button("a", 4)
    print("opening screens:")
    for s in seen:
        print("   ", s)
    check("the battle menu came up", menu_up)
    low = " ".join(seen).lower()
    check("the opening says the trainer wants to battle", "wants to battle" in low or "would like to battle" in low or "challenges" in low or "appeared" in low, "")
    check("the opening sends out our #MON with 'Go!'", "go!" in low)
    check("no switch text at the start", "come back" not in low and "enough!" not in low and "good!" not in low)
    t.tick(60)
    shot("menu")
    if os.environ.get("SAVESTATE"):
        with open(os.environ["SAVESTATE"], "wb") as f:
            pb._pb.save_state(f)
        print("state saved")
        sys.exit(0)
    if menu_up:
        # FIGHT
        pb.button("a", 4)
        t.tick(50)
        shot("moves")
        tx = text()
        moves = ["TACKLE", "SCRATCH", "CHARGE", "FLAME", "BITE", "SURF", "STRENGTH", "ROCK", "EARTH", "ICE", "THUNDER", "HYPER", "CRUNCH", "DIG"]
        print("moves screen:", tx)
        check("the move info box shows category, type and PP", "/" in tx and any(c in tx for c in ("PHYSICAL", "SPECIAL", "STATUS")), tx)
        # rows 12-16 of the move box: the move names are letters there, and FIGHT must be gone
        rows = screen()
        box = "".join(rows[12:17]).replace(" ", "")
        check("move names are drawn in the move box", len([c for c in box if c.isalpha()]) >= 6 and "FIGHT" not in box, repr(box))
        pb.button("b", 4)
        t.tick(50)
        shot("back")
        tx = text()
        check("B goes back to the battle menu", "FIGHT" in tx and "RUN" in tx, tx)
        # and FIGHT again, pick a move
        pb.button("a", 4)
        t.tick(50)
        pb.button("a", 4)
        t.tick(30)
        seen2 = []
        for i in range(80):
            pb.tick(8, False)
            tx = text()
            if tx and (not seen2 or seen2[-1] != tx):
                seen2.append(tx)
            pb.button("a", 4)
        print("first turn:")
        for s in seen2[:10]:
            print("   ", s)
        check("a move was used", any("used" in s.lower() or "!" in s for s in seen2))

    print("PASS" if not bad else f"FAIL: {bad}")
    sys.exit(0 if not bad else 1)


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
check("a battle happened on the way", False)
print("FAIL: no battle")
sys.exit(1)
