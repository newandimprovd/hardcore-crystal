#!/usr/bin/env python3
"""Run GetMoveCategory in the emulator for every move ID and compare with the generator's table."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import importlib.util
from gbtest import T

rom = sys.argv[1] if len(sys.argv) > 1 else "pokecrystal11.gbc"
root = __file__.rsplit("/tools/", 1)[0]
spec = importlib.util.spec_from_file_location("g", root + "/tools/hardcore/gen_moves.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
want = g.category_table()

t = T(rom)
t.tick(60)
fn = t.addr("GetMoveCategory")
code = [0xF3, 0xCD, fn & 0xFF, fn >> 8, 0x18, 0xFE]   # di; call GetMoveCategory; jr $
for i, b in enumerate(code):
    t.pb.memory[0xC000 + i] = b
bad = 0
for mid in range(1, 252):
    rf = t.pb.register_file
    rf.A = mid; rf.B = 0x12; rf.C = 0x34; rf.D = 0x56; rf.E = 0x78; rf.HL = 0x9ABC
    rf.PC = 0xC000; rf.SP = 0xDFF0
    t.pb.tick(3, False)
    rf = t.pb.register_file
    exp = 20 if want[mid] == "Special" else 0
    ok = rf.A == exp and (rf.B, rf.C, rf.D, rf.E, rf.HL) == (0x12, 0x34, 0x56, 0x78, 0x9ABC) and rf.PC in (0xC004, 0xC005)
    if not ok:
        bad += 1
        if bad < 10:
            print("MISMATCH", mid, want[mid], "A", rf.A, "PC", hex(rf.PC))
print("checked 251 moves, mismatches:", bad)
sys.exit(1 if bad else 0)
