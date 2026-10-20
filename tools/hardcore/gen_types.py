#!/usr/bin/env python3
"""Hardcore Crystal type system generator.

Rebuilds the type constants, names, Pokedex search lists and the matchup table
from the vanilla files at the base commit, so it is safe to run repeatedly.

Author's chart changes plus the Fairy type. Where the author's wording was
ambiguous the reading used is recorded in docs/HARDCORE_ROADMAP.md.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "3bc8daa"


def base(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"], text=True)


NVE, SE, NO = "NOT_VERY_EFFECTIVE", "SUPER_EFFECTIVE", "NO_EFFECT"
P = "PSYCHIC_TYPE"

# (attacker, defender) -> effectiveness, or None to remove the row.
PATCH = {
    # Normal is immune to Dark and hits Bug and Psychic super effectively.
    ("DARK", "NORMAL"): NO,
    ("NORMAL", "BUG"): SE,
    ("NORMAL", P): SE,
    # Bug is immune to Ghost, Dark, Psychic, Grass and Ground.
    ("GHOST", "BUG"): NO,
    ("DARK", "BUG"): NO,
    (P, "BUG"): NO,
    ("GRASS", "BUG"): NO,
    ("GROUND", "BUG"): NO,
    # Electric and Steel are weak to Grass. Steel is weak to Water. Water is weak to Ice.
    ("GRASS", "ELECTRIC"): SE,
    ("GRASS", "STEEL"): SE,
    ("WATER", "STEEL"): SE,
    ("ICE", "WATER"): SE,
    # Grass and Flying are super effective against each other.
    ("GRASS", "FLYING"): SE,
    ("FLYING", "GRASS"): SE,
    # Fairy.
    ("FAIRY", "FIGHTING"): SE,
    ("FAIRY", "DRAGON"): SE,
    ("FAIRY", "DARK"): SE,
    ("FAIRY", "FIRE"): NVE,
    ("FAIRY", "POISON"): NVE,
    ("FAIRY", "STEEL"): NVE,
    ("POISON", "FAIRY"): SE,
    ("STEEL", "FAIRY"): SE,
    ("FIGHTING", "FAIRY"): NVE,
    ("BUG", "FAIRY"): NVE,
    ("DARK", "FAIRY"): NVE,
    ("DRAGON", "FAIRY"): NO,
}

ROW = re.compile(r"^\tdb\s+(\w+),\s+(\w+),\s+(\w+)\s*$")


def gen_matchups():
    text = base("data/types/type_matchups.asm")
    pre, post = text.split("\tdb -2 ; end (with Foresight)")
    rows = []
    for line in pre.splitlines():
        m = ROW.match(line)
        if m:
            rows.append((m[1], m[2], m[3]))
    table = {(a, d): v for a, d, v in rows}
    vanilla = [(a, d) for a, d, _ in rows]
    added = []
    for key, val in PATCH.items():
        if key not in table:
            added.append(key)
        table[key] = val

    def fmt(a, d):
        return f"\tdb {a + ',':<13} {d + ',':<13} {table[(a, d)]}"

    out = ["TypeMatchups:", "\t;  attacker,     defender,     *="]
    out += [fmt(a, d) for a, d in vanilla]
    out += ["", "; Hardcore Crystal additions (see tools/hardcore/gen_types.py)"]
    out += [fmt(a, d) for a, d in added]
    return "\n".join(out) + "\n\n\tdb -2 ; end (with Foresight)" + post, len(vanilla) + len(added)


def gen_misc():
    p = ROOT / "constants/type_constants.asm"
    t = base("constants/type_constants.asm")
    t = t.replace("\tconst DARK\n", "\tconst DARK\n\tconst FAIRY\n")
    p.write_text(t)

    p = ROOT / "data/types/names.asm"
    t = base("data/types/names.asm")
    t = t.replace("\tdw Dark\n", "\tdw Dark\n\tdw Fairy\n")
    t = t.replace('Dark:      db "DARK@"\n', 'Dark:      db "DARK@"\nFairy:     db "FAIRY@"\n')
    p.write_text(t)

    p = ROOT / "data/types/search_types.asm"
    t = base("data/types/search_types.asm")
    t = t.replace("\tdb STEEL\n", "\tdb STEEL\n\tdb FAIRY\n")
    p.write_text(t)

    p = ROOT / "data/types/search_strings.asm"
    t = base("data/types/search_strings.asm")
    t = t.replace('\tdb " STEEL  @"\n', '\tdb " STEEL  @"\n\tdb " FAIRY  @"\n')
    p.write_text(t)


if __name__ == "__main__":
    text, n = gen_matchups()
    (ROOT / "data/types/type_matchups.asm").write_text(text)
    gen_misc()
    print(f"type matchup rows: {n}; Fairy added")
