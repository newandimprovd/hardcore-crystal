#!/usr/bin/env python3
"""Prints 'MAP_CONST X Y' for the first street with a hut: the cell in front of the hut's door (for test_hut.py)."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for f in sorted(glob.glob(os.path.join(ROOT, "maps/gen/*Street*.asm"))):
    s = open(f).read()
    m = re.search(r"warp_event\s+(\d+),\s*(\d+),\s*(\w+_HUT\w*),", s)
    if m:
        const = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", os.path.basename(f)[:-4]).upper()
        print(const, m[1], int(m[2]) + 1)
        sys.exit(0)
sys.exit(1)
