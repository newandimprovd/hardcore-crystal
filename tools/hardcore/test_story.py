#!/usr/bin/env python3
"""Story tests (stage 7): the kill 200 news, the flooded and cratered New Bark Town, the portal.

usage:
  test_story.py milestone ROM   ROM = testbuild.sh stA TEST_MAP=TITHE_PLAZA1 TEST_X=3 TEST_Y=4 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
  test_story.py newbark ROM     ROM = testbuild.sh stB TEST_MAP=NEW_BARK_TOWN TEST_X=10 TEST_Y=10 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2
  test_story.py ending ROM      ROM = testbuild.sh stF TEST_MAP=JUDECCA_CENTRE TEST_X=4 TEST_Y=17 TEST_MON=DEATHROLL TEST_LEVEL=100 TEST_REVEALED=1 TEST_STORY=2
                                (beats the last boss, talks to Elm on the crater rim, plays the credits and Continues in the bedroom;
                                 EXPECT_MON=CALDERA etc. is for builds where the party holds another species)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("WALK_GOD", "1")
import test_walk as tw  # noqa: E402
from gbtest import T  # noqa: E402

SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/story")
os.makedirs(SHOTS, exist_ok=True)
EV = tw.const_table("constants/event_flags.asm")
NEWBARK = "?24:4"  # the walker only names generated maps


def getflag(t, name):
    i = EV[name]
    return (t.mem("wEventFlags", i // 8) >> (i % 8)) & 1


def setflag(t, name):
    i = EV[name]
    t.poke("wEventFlags", t.mem("wEventFlags", i // 8) | (1 << (i % 8)), i // 8)


def boot(rom):
    t = T(rom)
    for i in range(600):
        t.pb.button("a" if i % 2 else "start", 4)
        t.tick(20)
        if t.mem("wMapGroup") and t.mem("wXCoord"):
            break
    t.tick(200)
    return t


def milestone(rom):
    wk = tw.Walker(rom)
    t = wk.t
    wk.seen_map()
    t.poke("wHCKillCount", 199, 0)
    t.poke("wHCKillCount", 0, 1)
    ok = wk.go("TitheStreet1")
    ok = ok and wk.go("TitheStreet2")
    kills = t.mem("wHCKillCount", 0, 2)
    print("kills", kills[0] + 256 * kills[1], "tidal flag", getflag(t, "EVENT_HC_TIDAL_WAVE"))
    t.shot(f"{SHOTS}/milestone_end.png", 3)
    good = ok and getflag(t, "EVENT_HC_TIDAL_WAVE") == 1 and not wk.log
    print("PASS" if good else "FAIL")
    return good


def settle(t, limit=200):
    """Mash A while a script runs (the teacher at the west edge stops a player who has no Pokemon flagged)."""
    quiet = 0
    for _ in range(limit):
        if t.mem("wScriptRunning"):
            quiet = 0
            t.pb.button("a", 4)
            t.tick(16)
        else:
            quiet += 1
            t.tick(6)
            if quiet > 5:
                return


def rival(rom):
    """ROM built with testbuild.sh stD TEST_MAP=LOTUS_MANSION TEST_X=4 TEST_Y=17 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1.
    Beats the rival in his boss room, checks the stolen POKEMON, the crater flag and walks the hall and the bedroom."""
    wk = tw.Walker(rom)
    t = wk.t
    wk.seen_map()
    t.poke("wHCKillCount", 255, 0)
    t.poke("wHCKillCount", 2, 1)
    party0 = t.mem("wPartyCount")
    for i in range(14):
        t.press("up", hold=16, wait=6)
        if wk.busy():
            wk.settle()
            break
    wk.settle()
    t.tick(60)
    party1 = t.mem("wPartyCount")
    species = t.mem("wPartySpecies", 0, 3)
    print("party", party0, "->", party1, "species", species, "level2", t.mem("wPartyMon2Level"))
    flags = {n: getflag(t, n) for n in ("EVENT_HC_RIVAL_FELL", "EVENT_HC_STOLEN_BACK", "EVENT_HC_CRATER", "EVENT_HC_ELM_AT_RIM")}
    print(flags)
    t.shot(f"{SHOTS}/rival_after.png", 3)
    ok = party1 == party0 + 1 and all(flags.values())
    ok = ok and wk.go("LotusHall")
    t.shot(f"{SHOTS}/hall.png", 3)
    ok = ok and wk.go("LotusBedroom")
    t.shot(f"{SHOTS}/bedroom.png", 3)
    ok = ok and wk.go("LotusHall")
    print("PASS" if ok and not wk.log else "FAIL", wk.log)
    return ok and not wk.log


def step(t, d, n=1):
    for _ in range(n):
        t.press(d, hold=16, wait=6)
        settle(t)
    t.tick(10)


def cross_and_back(t, out, back):
    """Leave New Bark Town through its west edge and return so the map callbacks run again."""
    step(t, out, 4)
    t.tick(60)
    step(t, back, 4)
    t.tick(60)


def newbark(rom):
    """ROM built with TEST_STORY=2 and TEST_MAP=NEW_BARK_TOWN TEST_X=10 TEST_Y=10: the crater, the swirl above the player."""
    t = boot(rom)
    print("start", t.where())
    t.shot(f"{SHOTS}/nb_crater.png", 3)
    g0 = t.mem("wMapGroup")
    t.pb.button("up", 9)
    t.tick(20)
    t.pb.button("a", 4)
    t.tick(60)
    t.shot(f"{SHOTS}/nb_portal_text.png", 3)
    for i in range(60):  # text pages, then the yes/no prompt: A picks YES
        t.pb.button("a", 4)
        t.tick(30)
        if i == 4:
            t.shot(f"{SHOTS}/nb_portal_text.png", 3)
        if t.mem("wMapGroup") != g0:
            break
    t.tick(120)
    print("after portal", t.where())
    t.shot(f"{SHOTS}/nb_after.png", 3)
    ok = t.mem("wMapGroup") != g0
    print("PASS" if ok else "FAIL")
    return ok


def talk_to_elm(t):
    """From the arrival cell below the swirl walk to the cell right of ELM and talk."""
    step(t, "down")
    step(t, "left", 5)
    t.press("left", hold=16, wait=6)  # blocked by ELM: only turns
    t.tick(10)


def ending(rom):
    wk = tw.Walker(rom)
    t = wk.t
    wk.seen_map()
    for i in range(14):
        t.press("up", hold=16, wait=6)
        if wk.busy():
            wk.settle()
            break
    wk.settle()
    t.tick(120)
    st = wk.state()
    print("after the final boss:", st, "FINN_FELL", getflag(t, "EVENT_HC_FINN_FELL"))
    t.shot(f"{SHOTS}/end_rim.png", 3)
    ok = st[0] == NEWBARK and getflag(t, "EVENT_HC_FINN_FELL") == 1
    if not ok:
        print("FAIL")
        return False
    talk_to_elm(t)
    t.shot(f"{SHOTS}/end_elm.png", 3)
    t.pb.button("a", 4)
    t.tick(40)
    last = None
    for i in range(400):  # text pages, then the hall of fame and the credits
        if getflag(t, "EVENT_HC_ENDED") and i % 50 == 0:
            t.shot(f"{SHOTS}/end_progress_{i // 50}.png", 2)
        t.pb.button("a", 4)
        t.tick(40)
        if getflag(t, "EVENT_HC_ENDED") and i > 30 and not t.mem("wScriptRunning"):
            pass
    print("ENDED flag", getflag(t, "EVENT_HC_ENDED"), "where", wk.state())
    t.shot(f"{SHOTS}/end_after_credits.png", 3)
    # back at the title screen: Continue
    for i in range(80):
        t.pb.button("start" if i % 4 == 0 else "a", 4)
        t.tick(40)
        if wk.state()[0] == "LotusBedroom":
            break
    t.tick(120)
    st = wk.state()
    t.shot(f"{SHOTS}/end_continue.png", 3)
    print("after Continue:", st)
    good = getflag(t, "EVENT_HC_ENDED") == 1 and st[0] == "LotusBedroom"
    print("PASS" if good else "FAIL")
    return good


def notyet(rom):
    """ROM built with TEST_MAP=NEW_BARK_TOWN TEST_X=10 TEST_Y=10 TEST_MON=CTHULUDON TEST_STORY=3: ELM must not end the game yet."""
    t = boot(rom)
    print("start", t.where())
    talk_to_elm(t)
    t.shot(f"{SHOTS}/notyet_elm.png", 3)
    t.pb.button("a", 4)  # talk
    t.tick(40)
    for i in range(80):  # stop pressing A the moment the script ends (A again would only talk to ELM again)
        if not t.mem("wScriptRunning"):
            break
        t.pb.button("a", 4)
        t.tick(40)
    t.tick(200)
    t.shot(f"{SHOTS}/notyet_after.png", 3)
    ok = getflag(t, "EVENT_HC_ENDED") == 0 and not t.mem("wScriptRunning")
    print("ENDED flag", getflag(t, "EVENT_HC_ENDED"), "script running", t.mem("wScriptRunning"))
    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    mode, rom = sys.argv[1], sys.argv[2]
    ok = {"milestone": milestone, "newbark": newbark, "rival": rival, "ending": ending, "notyet": notyet}[mode](rom)
    sys.exit(0 if ok else 1)
