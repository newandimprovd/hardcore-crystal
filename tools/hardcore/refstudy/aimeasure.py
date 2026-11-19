"""Measure what the vanilla-style AI costs in cycles inside real battles of our ROM.
Cycle clock = completed frames * 70224 + LY * 456 (LY is the scanline counter, so the resolution is about 456 cycles).
usage: aimeasure.py ROM"""
import os, sys, statistics
HERE = "/home/claude/pokecrystal/tools/hardcore"
sys.path.insert(0, HERE)
os.environ["WALK_GOD"] = "0"
from test_walk import Walker
ROOT = "/home/claude/pokecrystal"
rom = sys.argv[1]
wk = Walker(rom); t = wk.t; pb = t.pb
def now(): return pb.frame_count * 70224 + pb.memory[0xff44] * 456
def vb(): return pb.memory[0xff91]
syms = {}
for ln in open(rom[:-4] + ".sym"):
    m = __import__("re").match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)$", ln.strip())
    if m: syms[m[3]] = (int(m[1], 16), int(m[2], 16))
rom_bytes = open(rom, "rb").read()
bank_dc, addr_dc = syms["AIDamageCalc"]
sites = []
base = bank_dc * 0x4000 - 0x4000
for off in range(bank_dc * 0x4000, bank_dc * 0x4000 + 0x4000 - 2):
    if rom_bytes[off] == 0xCD and rom_bytes[off+1] == addr_dc & 0xff and rom_bytes[off+2] == addr_dc >> 8:
        sites.append(off - base)
print("AIDamageCalc call sites in its bank:", [hex(s) for s in sites])
st = dict(choose_t0=None, calc_t0=None, choose=[], calc=[], calc_in_choose=0, per_choose_calls=[])
st["choose_vb"] = []; st["calc_vb"] = []
def choose_enter(ctx): st["choose_t0"] = now(); st["choose_v0"] = vb(); st["calc_in_choose"] = 0
def choose_exit(ctx):
    if st["choose_t0"] is not None:
        st["choose_vb"].append((vb() - st["choose_v0"]) & 0xff); st["choose"].append(now() - st["choose_t0"]); st["per_choose_calls"].append(st["calc_in_choose"]); st["choose_t0"] = None
def calc_enter(ctx): st["calc_t0"] = now(); st["calc_v0"] = vb(); st["calc_in_choose"] += 1
def calc_exit(ctx):
    if st["calc_t0"] is not None: st["calc_vb"].append((vb() - st["calc_v0"]) & 0xff); st["calc"].append(now() - st["calc_t0"]); st["calc_t0"] = None
t.hook("AIChooseMove", choose_enter)
t.hook("IsMobileBattle", choose_exit)
t.hook("AIDamageCalc", calc_enter)
for s in sites: pb.hook_register(bank_dc, s + 3, calc_exit, None)
# play the rival fight on the stem
for _ in range(4): wk.press_dir("up")
for _ in range(60):
    if not t.mem("wBattleMode") and st["choose"]: break
    t.pb.button("a", 4); t.tick(30)
def stats(name, v):
    v = [x for x in v if 0 <= x < 5_000_000]
    if not v: print(name, "no samples"); return
    print(f"{name}: n={len(v)} min={min(v)} median={int(statistics.median(v))} max={max(v)} cycles  ({max(v)/70224:.2f} frames max)")
stats("AIChooseMove (whole 4 move scoring, all layers)", st["choose"])
stats("AIDamageCalc (one move, real damage routine)", st["calc"])
print("AIDamageCalc calls per AIChooseMove:", st["per_choose_calls"])

print("VBlank interrupts during AIChooseMove:", st["choose_vb"], " during each AIDamageCalc:", st["calc_vb"])
