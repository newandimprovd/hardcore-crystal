#!/usr/bin/env python3
"""Drop the ENGINE_* flags nothing uses: the const in constants/engine_flags.asm and the engine_flag row in
data/events/engine_flags.asm (both lists are in the same order).  Usage: prune_engine_flags.py [--delete]"""
import glob, re, sys
C = "constants/engine_flags.asm"; D = "data/events/engine_flags.asm"
cl = open(C).read().splitlines(keepends=True); dl = open(D).read().splitlines(keepends=True)
ci = [i for i, l in enumerate(cl) if re.match(r"\tconst ENGINE_\w+", l)]
di = [i for i, l in enumerate(dl) if re.match(r"\tengine_flag ", l)]
print(len(ci), "consts,", len(di), "rows")
assert len(ci) == len(di)
names = [re.match(r"\tconst (ENGINE_\w+)", cl[i]).group(1) for i in ci]
texts = ""
for f in glob.glob("**/*.asm", recursive=True) + glob.glob("tools/hardcore/**/*.py", recursive=True):
    if f not in (C, D): texts += open(f, errors="replace").read() + "\n"
used = set(re.findall(r"ENGINE_\w+", texts))
dead = [k for k, n in enumerate(names) if n not in used]
print(len(dead), "unused:", " ".join(names[k] for k in dead))
if "--delete" in sys.argv:
    kill_c = {ci[k] for k in dead}; kill_d = {di[k] for k in dead}
    open(C, "w").write("".join(l for i, l in enumerate(cl) if i not in kill_c))
    open(D, "w").write("".join(l for i, l in enumerate(dl) if i not in kill_d))
    print("deleted")
