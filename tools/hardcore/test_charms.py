#!/usr/bin/env python3
"""The six charm key items (docs/CHARMS.md), tested by calling the engine routines in the emulator: set registers and memory, push a sentinel
return address, jump to the routine through FarCall, run to the sentinel and read the result.  Each charm is tried without and with the item in the bag.
usage: test_charms.py ROM          (the real ROM is fine, no test build is needed)"""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gbtest import T  # noqa: E402
from test_walk import item_value, const_table  # noqa: E402

faulthandler.dump_traceback_later(600, exit=True)
rom = sys.argv[1]
t = T(rom)
pb = t.pb
bad = []
SENT = 0x23E6  # a 'jr $' in bank 0: the CPU parks there, registers and flags stay as the routine left them
MON_HP, MON_MAXHP, MON_LEN = 34, 36, 48  # constants/pokemon_data_constants.asm (checked with rgbasm when the test was written)


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


for _ in range(300):
    pb.tick()


SP0 = None


def call(name, read=None, **regs):
    """Run the routine `name` to its return and give back the registers it left (and read(), taken the moment it returned).
    Registers via keyword (a, b, c, d, e, hl).  The return address is the 'jr $' at SENT: the CPU parks there for the rest of the frame
    (a hook on that address would make PyBoy spin on it forever)."""
    global SP0
    bank, addr = t.sym[name]
    rf = pb.register_file
    if SP0 is None:
        SP0 = rf.SP - 16
    pb.memory[0xFF70] = 1  # SVBK: the data below is poked into WRAM bank 1, the CPU must see that one too
    sp = SP0 - 2
    pb.memory[sp] = SENT & 0xFF
    pb.memory[sp + 1] = SENT >> 8
    rf.SP = sp
    if bank == 0 or addr < 0x4000 or "a" in regs or "hl" in regs:
        for k, v in regs.items():
            setattr(rf, k.upper(), v)
    if bank == 0 or addr < 0x4000:
        rf.PC = addr
    elif "a" in regs or "hl" in regs:
        # FarCall itself consumes a and hl, so a routine that takes them gets its bank switched in by hand (the MBC register and hROMBank,
        # which CheckItem and friends restore on the way out)
        pb.memory[0x2000] = bank
        t.poke("hROMBank", bank)
        rf.PC = addr
    else:
        rf.A = bank
        rf.HL = addr
        rf.PC = 0x0008  # rst FarCall: a = bank, hl = address, returns where it was called from
        for k, v in regs.items():
            setattr(rf, k.upper(), v)
    for _ in range(4):  # the frame may end in the middle of the routine
        pb.tick(1, False)
        if rf.PC == SENT:
            break
    if rf.PC != SENT:
        raise SystemExit(f"{name} did not return, PC={rf.PC:04x}")
    snap = dict(A=rf.A, B=rf.B, C=rf.C, D=rf.D, E=rf.E, F=rf.F, HL=rf.HL, PC=rf.PC)
    if read:
        snap["read"] = read()
    return snap


def carry(r):
    return bool(r["F"] & 0x10)


def set_bag(*names):
    vals = [item_value(n) for n in names]
    t.poke("wNumKeyItems", len(vals))
    for i, v in enumerate(vals):
        t.poke("wKeyItems", v, i)
    t.poke("wKeyItems", 0xFF, len(vals))


HQ = t.sym["hQuotient"][1]


# ------------------------------------------------------------------ HC_HasCharm: the finder every other charm uses
t.poke("wCurItem", 0x2B)
set_bag("EXP_CHARM")
r = call("HC_HasCharm", read=lambda: t.mem("wCurItem"), a=item_value("EXP_CHARM"), b=0x11, c=0x22, d=0x33, e=0x44, hl=0x5566)
check("has: carry set when the charm is in the bag", carry(r))
check("has: wCurItem is kept", r["read"] == 0x2B, f"{r['read']:02x}")
check("has: bc, de and hl are kept", (r["B"], r["C"], r["D"], r["E"], r["HL"]) == (0x11, 0x22, 0x33, 0x44, 0x5566),
      f"{r['B']:02x}{r['C']:02x} {r['D']:02x}{r['E']:02x} {r['HL']:04x}")
r = call("HC_HasCharm", read=lambda: t.mem("wCurItem"), a=item_value("LOOT_CHARM"), b=0x11, c=0x22, d=0x33, e=0x44, hl=0x5566)
check("has: carry clear for a charm that is not in the bag", not carry(r))
check("has: wCurItem is kept without the charm", r["read"] == 0x2B)
set_bag("EXP_CHARM", "PURSE_CHARM", "CATCH_CHARM", "LOOT_CHARM", "HEAL_CHARM", "LULL_CHARM")
for n in ("EXP_CHARM", "PURSE_CHARM", "CATCH_CHARM", "LOOT_CHARM", "HEAL_CHARM", "LULL_CHARM"):
    r = call("HC_HasCharm", a=item_value(n))
    check(f"has: {n} found among six", carry(r))
set_bag()
for n in ("EXP_CHARM", "PURSE_CHARM", "CATCH_CHARM", "LOOT_CHARM", "HEAL_CHARM", "LULL_CHARM"):
    r = call("HC_HasCharm", a=item_value(n))
    check(f"has: {n} not found in an empty bag", not carry(r))


# ------------------------------------------------------------------ EXP: x 6/5 on the quotient of the experience calculation
def exp_run(val, charm):
    set_bag("EXP_CHARM") if charm else set_bag()
    for i, v in enumerate((0, 0, val >> 8, val & 0xFF)):
        pb.memory[HQ + i] = v
    r = call("HC_ExpCharm", read=lambda: pb.memory[HQ + 2] * 256 + pb.memory[HQ + 3], b=0x12, c=0x34)
    return r


for val in (100, 250, 1000, 3):
    r = exp_run(val, False)
    check(f"exp {val}: unchanged without the charm", r["read"] == val, str(r["read"]))
    r = exp_run(val, True)
    check(f"exp {val}: x 6/5 with the charm", r["read"] == val * 6 // 5, f"{r['read']} (want {val * 6 // 5})")
    check(f"exp {val}: bc is kept", (r["B"], r["C"]) == (0x12, 0x34))


# ------------------------------------------------------------------ CATCH: a quarter better, 255 at most
def catch_run(rate, charm):
    set_bag("CATCH_CHARM") if charm else set_bag()
    return call("HC_CatchCharm", a=rate, b=0x12, c=0x34)


for rate, want in ((100, 125), (200, 250), (240, 255), (255, 255), (3, 3), (45, 56)):
    r = catch_run(rate, False)
    check(f"catch {rate}: unchanged without the charm", r["A"] == rate, str(r["A"]))
    r = catch_run(rate, True)
    check(f"catch {rate}: {want} with the charm", r["A"] == want, str(r["A"]))
    check(f"catch {rate}: bc is kept", (r["B"], r["C"]) == (0x12, 0x34))


# ------------------------------------------------------------------ LULL: a quarter fewer wild encounters
def lull_run(rate, charm):
    set_bag("LULL_CHARM") if charm else set_bag()
    return call("HC_ApplyLullCharm", b=rate)


for rate, want in ((100, 75), (40, 30), (3, 3), (255, 192)):
    r = lull_run(rate, False)
    check(f"lull {rate}: unchanged without the charm", r["B"] == rate, str(r["B"]))
    r = lull_run(rate, True)
    check(f"lull {rate}: {want} with the charm", r["B"] == want, str(r["B"]))

# the key item switches the charm on and off: EVENT_HC_LULL_OFF set = off (the item script itself is in test_purg.py)
LULL_OFF = const_table(os.path.join(os.path.dirname(os.path.dirname(HERE)), "constants/event_flags.asm"))["EVENT_HC_LULL_OFF"]


def lull_flag(on):
    byte = t.mem("wEventFlags", LULL_OFF // 8)
    t.poke("wEventFlags", (byte & ~(1 << (LULL_OFF % 8))) | ((0 if on else 1) << (LULL_OFF % 8)), LULL_OFF // 8)


lull_flag(False)
for rate in (100, 255):
    r = lull_run(rate, True)
    check(f"lull {rate}: unchanged while the charm is switched off", r["B"] == rate, str(r["B"]))
    r = lull_run(rate, False)
    check(f"lull {rate}: unchanged without the item and switched off", r["B"] == rate, str(r["B"]))
lull_flag(True)
r = lull_run(100, True)
check("lull 100: 75 again once it is switched on", r["B"] == 75, str(r["B"]))


# ------------------------------------------------------------------ HEAL: 1 HP + max/128 for every living, hurt party member
def party(mons):
    t.poke("wPartyCount", len(mons))
    for i, (hp, mx) in enumerate(mons):
        o = i * MON_LEN
        t.poke("wPartyMon1", hp >> 8, o + MON_HP)
        t.poke("wPartyMon1", hp & 0xFF, o + MON_HP + 1)
        t.poke("wPartyMon1", mx >> 8, o + MON_MAXHP)
        t.poke("wPartyMon1", mx & 0xFF, o + MON_MAXHP + 1)


def hps(n):
    out = []
    for i in range(n):
        o = i * MON_LEN
        out.append(t.mem("wPartyMon1", o + MON_HP) * 256 + t.mem("wPartyMon1", o + MON_HP + 1))
    return out


MONS = [(50, 200), (0, 100), (199, 200), (500, 700), (10, 10), (1, 999)]
party(MONS)
set_bag()
call("HC_HealStep")
check("heal: nothing changes without the charm", hps(6) == [h for h, _ in MONS], str(hps(6)))
party(MONS)
set_bag("HEAL_CHARM")
call("HC_HealStep")
want = [52, 0, 200, 506, 10, 9]  # 1 + max/128: 200 -> 2, 700 -> 6, 999 -> 8 (so 1 -> 9); the fainted one stays fainted; nobody passes the maximum
check("heal: 1 HP + max/128 each, the fainted stay down, the maximum is respected", hps(6) == want, f"{hps(6)} (want {want})")
for _ in range(130):
    call("HC_HealStep")
check("heal: 130 rounds fill everybody but the fainted", hps(6) == [200, 0, 200, 700, 10, 999], str(hps(6)))


# ------------------------------------------------------------------ PURSE and LOOT: the rolls
def money():
    v = t.mem("wMoney", 0, 3)
    return v[0] * 65536 + v[1] * 256 + v[2]


def loot_run(charm, n):
    set_bag("PURSE_CHARM") if charm else set_bag()
    amounts = []
    for _ in range(n):
        for i in range(3):
            t.poke("wMoney", 0, i)
        call("HC_RollLoot")
        amounts.append(money())
    return amounts


plain = loot_run(False, 60)
rich = loot_run(True, 60)
check("purse: 100..610 without the charm", all(100 <= a <= 610 for a in plain), f"{min(plain)}..{max(plain)}")
check("purse: 150..915 with the charm and above 610 sometimes", all(150 <= a <= 915 for a in rich) and max(rich) > 610, f"{min(rich)}..{max(rich)}")
check("purse: the charm raises the average by about half", 1.25 < (sum(rich) / sum(plain)) < 1.75, f"x{sum(rich) / sum(plain):.2f}")


def drop_run(charm, n):
    set_bag("LOOT_CHARM") if charm else set_bag()
    hits = 0
    for _ in range(n):
        r = call("HC_RollItemDrop", read=lambda: t.mem("wScriptVar"))
        hits += r["read"] != 0
    return hits / n


p0 = drop_run(False, 600)
p1 = drop_run(True, 600)
check("loot: about one body in four drops something without the charm", 0.17 < p0 < 0.33, f"{p0:.0%}")
check("loot: about three in eight with the charm", 0.30 < p1 < 0.46, f"{p1:.0%}")
check("loot: the charm drops more often", p1 > p0 + 0.05, f"{p0:.0%} -> {p1:.0%}")

print("PASS" if not bad else f"FAIL: {len(bad)} checks: {bad}")
sys.exit(0 if not bad else 1)
