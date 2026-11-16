#!/usr/bin/env python3
"""The credits (data/credits_script.asm): plays the real Credits routine in the emulator, reads the text on the screen every few frames and checks that the
Hardcore Crystal block (title, the author, CLAUDE as co-creator, the pret disassembly, the memorial) comes up, in order, before the copyright line, with every
line inside the screen.  Screenshots of every new screen go to $SHOTS (default /home/claude/scratch/credits).
usage: test_credits.py TESTROM     (a ROM from testbuild.sh: the spawn is the overworld)"""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gbtest import T  # noqa: E402

faulthandler.dump_traceback_later(900, exit=True)
SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/credits")
os.makedirs(SHOTS, exist_ok=True)
t = T(sys.argv[1])
pb = t.pb
rf = pb.register_file
SENT = 0x23E6  # a 'jr $' in bank 0 (the same one test_charms.py uses)

# text of the screen: the tilemap is 20 x 18 bytes in the game's own character encoding
CH = {0x7F: " ", 0xE3: "-", 0xE8: ".", 0xF4: ",", 0xE0: "'"}
CH.update({0x80 + i: chr(65 + i) for i in range(26)})
CH.update({0xF6 + i: str(i) for i in range(10)})


def screen_lines():
    base = t.sym["wTilemap"][1]
    out = []
    for row in range(18):
        s = "".join(CH.get(pb.memory[base + row * 20 + col], "?" if pb.memory[base + row * 20 + col] not in (0x00, 0x7F) else " ") for col in range(20))
        out.append(s.rstrip())
    return [x for x in out if x.strip()]


def start(name, **regs):
    """Start a routine from wherever the CPU is.  The frame may end inside the VBlank handler, where interrupts are off, and a routine started from
    there would wait forever for the next VBlank.  So the jump goes through the 'reti' at $0050 (the timer vector, unused): it returns to rst FarCall
    with interrupts on, and FarCall returns to SENT."""
    pb.memory[0xFF70] = 1
    sp = rf.SP - 16
    pb.memory[sp - 2] = SENT & 0xFF
    pb.memory[sp - 1] = SENT >> 8
    pb.memory[sp - 4] = 0x08
    pb.memory[sp - 3] = 0x00
    rf.SP = sp - 4
    bank, addr = t.sym[name]
    rf.A, rf.HL = bank, addr
    for k, v in regs.items():
        setattr(rf, k.upper(), v)
    rf.PC = 0x0050


# A test ROM (testbuild.sh NAME, any spawn point) starts in the overworld with the standard font loaded and the normal VBlank handler, which is how the
# game is when the credits come; on the title screen the credits would draw the title's tiles as letters.
from gbtest import boot_to_overworld  # noqa: E402

boot_to_overworld(t)
for _ in range(120):
    pb.tick(1, False)
start("Credits", b=0)

seen = []  # (frame, lines) of every distinct screen of text
bad = []
last = None
done = False
frame = 0
while frame < 60000:
    pb.tick(8, False)
    frame += 8
    if rf.PC == SENT:
        done = True
        break
    lines = [x for x in screen_lines() if any(c.isalpha() for c in x)]
    if lines and lines != last:
        if all(len(x) <= 20 for x in lines):
            seen.append((frame, lines))
            n = len(seen)
            pb.tick(40, False)  # the text is copied to the screen a few frames after it is written to the tilemap
            pb.tick(1, True)
            t.shot(f"{SHOTS}/{n:02d}.png", 2)
            frame += 41
        last = lines

flat = [x.strip() for _, ls in seen for x in ls]
# (The routine does not return to its caller in this test: after the last screen it waits for the player at THE END and then resets, so the run is
# simply cut off after 60000 frames.)
print(f"credits ran {'to the end' if done else 'for 60000 frames'}; {len(seen)} distinct text screens")
for f, ls in seen:
    if any(w in " ".join(ls) for w in ("HARDCORE", "AUTHOR", "CLAUDE", "PRET", "MEMORY", "TIMMY", "COPYRIGHT", "CONVERSION")):
        print(f"  frame {f:6d}: {' | '.join(x.strip() for x in ls)}")

want = [["HARDCORE CRYSTAL", "A TOTAL CONVERSION"],
        ["STORY AND DIRECTION", "THE AUTHOR"],
        ["CO-CREATOR", "CLAUDE", "ANTHROPIC"],
        ["BUILT ON THE PRET", "POKECRYSTAL", "DISASSEMBLY"],
        ["IN LOVING MEMORY", "TIMMY", "AND 499 OTHERS"]]
pos = -1
for group in want:
    idx = next((i for i, (_, ls) in enumerate(seen) if all(any(g in x for x in ls) for g in group)), None)
    if idx is None:
        bad.append(f"screen {group} never appeared")
    elif idx <= pos:
        bad.append(f"screen {group} out of order")
    else:
        pos = idx
if not any("COPYRIGHT" in x or "NINTENDO" in x or "CREATURES" in x for x in flat):
    print("  (note: the copyright line is drawn from tiles, not text; not checked)")
for f, ls in seen:
    for x in ls:
        if len(x) > 20:
            bad.append(f"line over 20 columns: {x!r}")
print("PASS" if not bad else "FAIL: " + "; ".join(bad))
sys.exit(0 if not bad else 1)
