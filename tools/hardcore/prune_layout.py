#!/usr/bin/env python3
"""Remove the lines of layout.link that name a section no source defines any more (run after the removal script deleted a feature)."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
names = set()
for top in ("."):
    for d, _, fs in os.walk(ROOT):
        if "/.git" in d or "/tools" in d:
            continue
        for f in fs:
            if f.endswith(".asm"):
                try:
                    s = open(os.path.join(d, f), errors="ignore").read()
                except OSError:
                    continue
                for m in re.finditer(r'^\s*SECTION\s+(?:UNION\s+|FRAGMENT\s+)?"([^"]+)"', s, re.M):
                    names.add(m.group(1))
p = os.path.join(ROOT, "layout.link")
out, gone = [], []
for l in open(p).read().splitlines(keepends=True):
    m = re.match(r'\s*"([^"]+)"', l)
    if m and m.group(1) not in names:
        gone.append(m.group(1))
        continue
    out.append(l)
open(p, "w").write("".join(out))
print(f"layout.link: {len(gone)} lines for sections that are gone removed")
