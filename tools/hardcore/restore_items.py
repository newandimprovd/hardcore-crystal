#!/usr/bin/env python3
"""Bring back items that prune_items.py dropped, into every index-aligned item table at once (the opposite of that tool).
The new items go in just before ITEM_B3, the first filler item, in every table:
  constants/item_constants.asm   const lines          data/items/names.asm        li rows
  data/items/descriptions.asm    dw rows + text       data/items/attributes.asm   "; NAME" + item_attribute pairs
  engine/items/item_effects.asm  dw NoEffect rows
The old rows and the description text come from the git commit before the first prune (OLD).  Idempotent.
usage: restore_items.py NAME ...        (default: the six held items of the boutiques)"""
import re
import subprocess
import sys

OLD = "a17569514^"
DEFAULT = ["LEFTOVERS", "QUICK_CLAW", "SCOPE_LENS", "AMULET_COIN", "BRIGHTPOWDER", "SMOKE_BALL"]
CONST, NAMES, DESC = "constants/item_constants.asm", "data/items/names.asm", "data/items/descriptions.asm"
ATTR, EFF = "data/items/attributes.asm", "engine/items/item_effects.asm"


def old(path):
    return subprocess.check_output(["git", "show", f"{OLD}:{path}"]).decode().split("\n")


def rd(p):
    return open(p).read().split("\n")


def wr(p, lines):
    open(p, "w").write("\n".join(lines))


def old_index(names_old, name):
    """0-based position of NAME in the old constants list (row k of a table is item k+1)."""
    return names_old.index(name)


def main():
    want = sys.argv[1:] or DEFAULT
    cl = rd(CONST)
    have = {m.group(1) for l in cl if (m := re.match(r"\s*const (\w+)", l))}
    want = [n for n in want if n not in have]
    if not want:
        print("nothing to restore")
        return
    oc = old(CONST)
    oc_names = [m.group(1) for l in oc if (m := re.match(r"\s*const (\w+)", l))]
    # one row per item in every table, old names/descriptions by position in the old tables
    on, od, oa, oe = old(NAMES), old(DESC), old(ATTR), old(EFF)
    names_rows = [l for l in on[on.index("\tlist_start ITEM_NAME_LENGTH - 1") + 1:] if l.startswith("\tli ")] if "\tlist_start ITEM_NAME_LENGTH - 1" in on else [l for l in on if l.startswith("\tli ")]
    desc_rows = []
    for l in od[od.index("\ttable_width 2") + 1:]:
        if l.startswith("\tassert_table_length"):
            break
        desc_rows.append(l)
    # new rows
    add = []
    for n in want:
        k = old_index(oc_names, n)  # NO_ITEM is 0, so the row is k - 1
        add.append((n, names_rows[k - 1], desc_rows[k - 1].strip().split()[1]))
    # constants: before ITEM_B3
    i = next(i for i, l in enumerate(cl) if re.match(r"\s*const ITEM_B3\b", l))
    cl[i:i] = [f"\tconst {n}" for n, _, _ in add]
    wr(CONST, cl)
    pos = len([1 for l in cl[:i] if re.match(r"\s*const \w+", l)]) - 1  # row index of ITEM_B3 (item id - 1: NO_ITEM has no row); cl[:i] holds none of the new lines
    # names
    nl = rd(NAMES)
    rows = [j for j, l in enumerate(nl) if l.startswith("\tli ")]
    j = rows[pos]
    nl[j:j] = [row for _, row, _ in add]
    wr(NAMES, nl)
    # descriptions: dw rows and the text blocks at the end
    dl = rd(DESC)
    start = dl.index("\ttable_width 2") + 1
    dws = [j for j in range(start, len(dl)) if dl[j].startswith("\tdw ")]
    j = dws[pos]
    dl[j:j] = [f"\tdw {lab}" for _, _, lab in add]
    text = []
    for _, _, lab in add:
        s = od.index(f"{lab}:")
        e = s
        while od[e].strip() != "":
            e += 1
        text += [""] + od[s:e]
    while dl and dl[-1] == "":
        dl.pop()
    wr(DESC, dl + text + [""])
    # attributes
    al = rd(ATTR)
    j = al.index("; ITEM_B3")
    block = []
    for n, _, _ in add:
        s = oa.index(f"; {n}")
        block += oa[s:s + 2]
    al[j:j] = block
    wr(ATTR, al)
    # effects
    el = rd(EFF)
    j = next(j for j, l in enumerate(el) if re.search(r";\s*ITEM_B3\s*$", l))
    el[j:j] = [f"\tdw NoEffect            ; {n}" for n, _, _ in add]
    wr(EFF, el)
    print("restored", " ".join(n for n, _, _ in add))


main()
