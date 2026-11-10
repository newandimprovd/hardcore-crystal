#!/usr/bin/env python3
"""Remove the palette/SGB layouts (SCGB_*) nothing selects: the constant, the row in CGBLayoutJumptable and in SGBLayoutJumptable.
The layout bodies become unreferenced labels; dead_labels.py --delete removes them.  Usage: prune_scgb.py [--delete]"""
import glob, re, sys
C = "constants/scgb_constants.asm"
CG = "engine/gfx/cgb_layouts.asm"
SG = "engine/gfx/sgb_layouts.asm"
cs = open(C).read().split("\n")
a = next(i for i, l in enumerate(cs) if l.strip() == "const_def")
b = next(i for i, l in enumerate(cs) if l.startswith("DEF NUM_SCGB_LAYOUTS"))
cl = [(re.match(r"\s*const (\w+)", cs[i]).group(1), i) for i in range(a + 1, b)]
text = ""
for f in glob.glob("**/*.asm", recursive=True) + glob.glob("tools/hardcore/**/*.py", recursive=True):
    if f != C: text += open(f, errors="replace").read()
dead = [(n, i) for n, i in cl if not re.search(r"\b" + n + r"\b", text)]
print(len(cl), "layouts;", len(dead), "unused:", " ".join(n for n, _ in dead))
if "--delete" not in sys.argv: sys.exit(0)
idx = [k for k, (n, _) in enumerate(cl) if n in {d for d, _ in dead}]
for path in (CG, SG):
    L = open(path).read().split("\n")
    s = next(i for i, l in enumerate(L) if l.strip() == "table_width 2")
    e = next(i for i, l in enumerate(L) if l.strip() == "assert_table_length NUM_SCGB_LAYOUTS")
    rows = list(range(s + 1, e))
    assert len(rows) == len(cl), (path, len(rows), len(cl))
    for k in reversed(idx): del L[rows[k]]
    open(path, "w").write("\n".join(L))
for _, i in sorted(dead, key=lambda x: -x[1]): del cs[i]
open(C, "w").write("\n".join(cs))
print("done")
