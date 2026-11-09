#!/usr/bin/env python3
"""List the undefined symbols of the last build (scratch/builderrs.log) with the first place each is used: python3 tools/hardcore/undef.py"""
import re
log = open("/home/claude/scratch/builderrs.log", errors="replace").read().splitlines()
seen = {}
for i, l in enumerate(log):
    m = re.match(r"error: (?:Undefined symbol|Requested `BANK\(\)` of undefined symbol|Requested `BANK\(\)` of undefined symbol) `([^`]+)`", l)
    if not m:
        m = re.match(r"error: .*undefined symbol `([^`]+)`", l)
    if not m:
        continue
    sym = m.group(1)
    loc = ""
    j = i + 1
    frames = []
    while j < len(log) and log[j].startswith(("    at ", "    <- ")):
        frames.append(log[j].strip()[3:].strip() if log[j].strip().startswith("<-") else log[j].strip()[3:]); j += 1
    # the innermost user line: the first frame that is not a macro file
    loc = next((f for f in frames if not f.startswith("macros/")), frames[0] if frames else "?")
    # for links, the frame list names the file where the symbol is used
    seen.setdefault(sym, [loc, 0])[1] += 1
for sym, (loc, n) in sorted(seen.items(), key=lambda kv: kv[1][0]):
    print(f"{loc:60s} {sym}  x{n}")
print(len(seen), "symbols")
