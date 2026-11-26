#!/usr/bin/env python3
"""Validates the line files of the alpha 3.3 variety pass (areas/lines3_<area>.py).
usage: check_lines3.py areas/lines3_tithe.py [...]
Checks the shape of every variable (see SPEC), the character set the game font can show, the length, and that no line repeats a line that already exists
anywhere in areas/*.py (word for word after normalising) or another line of the same file.  Exit 1 on any problem."""
import ast
import glob
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OK_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,'!?:;-()/&%+")
# name: (kind, count, max chars of one line).  kind "line": a list of strings; "gift": a list of (NAME, etymology sentence, offer sentence)
SPEC = {
    "BEATEN_NEW": ("line", 45, 110),
    "INTERIOR_CENTER": ("line", 4, 140),
    "INTERIOR_MART": ("line", 4, 140),
    "INTERIOR_HOUSE": ("line", 16, 140),
    "GIVER": ("gift", 7, 150),
    "GIVER_AFTER": ("line", 7, 110),
}
SPEC_PURG = {"PURG_HERMIT_SEEN": ("line", 44, 150), "PURG_HERMIT_BEATEN": ("line", 44, 120), "PURG_HERMIT_GIFT": ("line", 44, 150), "PURG_HERMIT_AFTER": ("line", 44, 150)}


def norm(t):
    return " ".join(re.sub(r"[^a-z0-9 ]", "", t.lower()).split())


def existing():
    seen = set()
    for f in glob.glob(os.path.join(HERE, "areas", "*.py")):
        if os.path.basename(f).startswith("lines3_"):
            continue
        try:
            tree = ast.parse(open(f).read())
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) >= 25:
                seen.add(norm(n.value))
    return seen


def main():
    bad = 0
    old = existing()
    for path in sys.argv[1:]:
        spec = importlib.util.spec_from_file_location("l3", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        table = SPEC_PURG if os.path.basename(path).startswith("lines3_purg") else SPEC
        mine = set()
        for var, (kind, n, mx) in table.items():
            data = getattr(mod, var, None)
            if data is None:
                print(f"{path}: {var} is missing")
                bad += 1
                continue
            if len(data) < n:
                print(f"{path}: {var} has {len(data)} entries, needs {n}")
                bad += 1
            for item in data:
                parts = list(item) if kind == "gift" else [item]
                if kind == "gift" and (len(parts) != 3 or not parts[0].isupper()):
                    print(f"{path}: {var} entry must be (NAME in capitals, etymology, offer): {item!r}")
                    bad += 1
                    continue
                for s in parts:
                    badc = sorted(set(s) - OK_CHARS)
                    if badc:
                        print(f"{path}: {var}: characters {badc} in {s!r}")
                        bad += 1
                    key = norm(s)
                    if len(key) >= 25 and (key in old or key in mine):
                        print(f"{path}: {var}: repeats an existing line: {s!r}")
                        bad += 1
                    mine.add(key)
                if sum(len(s) for s in parts) > mx + (40 if kind == "gift" else 0):
                    print(f"{path}: {var}: too long ({sum(len(s) for s in parts)} > {mx}): {parts[-1]!r}")
                    bad += 1
        print(f"{path}: {'ok' if not bad else 'problems'}")
    sys.exit(1 if bad else 0)


main()
