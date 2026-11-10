#!/bin/bash
# build and list the distinct files and lines that fail, with the first message of each (for the removal work)
cd "$(dirname "$0")/../.."
export PATH=/home/claude/bin:$PATH
make -j2 crystal11 > /home/claude/scratch/builderrs.log 2>&1
python3 - <<'PY'
import re
log = open("/home/claude/scratch/builderrs.log", errors="replace").read().splitlines()
seen = {}
i = 0
while i < len(log):
    if log[i].startswith(("error:", "ERROR", "Linking failed")) or "error:" in log[i][:12]:
        msg = log[i]
        chain = []
        j = i + 1
        while j < len(log) and log[j].startswith(("    at ", "    <- ")):
            chain.append(log[j].strip()); j += 1
        key = (chain[-1] if chain else "?")
        seen.setdefault(key, []).append((msg, chain[:2]))
        i = j
    else:
        i += 1
for k, v in sorted(seen.items()):
    print(f"{len(v):3d}  {k}   e.g. {v[0][0][:110]}  {' '.join(v[0][1][:1])}")
print("distinct sources:", len(seen), "total errors:", sum(len(v) for v in seen.values()))
PY
# make-level failures (missing rule, link failure) have no "error:" line the parser above recognises
grep -E "^make: \*\*\*|Linking failed|^error|ERROR" /home/claude/scratch/builderrs.log | head -5
if [ ! -s pokecrystal11.gbc ] || [ -n "$(find pokecrystal11.gbc -mmin +2 2>/dev/null)" ]; then echo "WARNING: pokecrystal11.gbc was not rebuilt just now"; fi
