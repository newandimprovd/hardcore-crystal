"""Parse the vanilla per-species data from base commit 3bc8daa.

Everything the roster generator needs to know about the 251 vanilla species is read from git
(never from the working tree, so the generators stay idempotent).
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = "3bc8daa"


def git(path):
    return subprocess.check_output(["git", "-C", ROOT, "show", f"{BASE}:{path}"], text=True)


def load():
    consts = []
    for l in git("constants/pokemon_constants.asm").splitlines():
        m = re.match(r"\tconst (\w+)\s+;", l)
        if m:
            consts.append(m.group(1))
        if "NUM_POKEMON" in l:
            break
    consts = consts[:251]
    assert consts[0] == "BULBASAUR" and consts[-1] == "CELEBI", consts[-1]
    n = len(consts)
    sp = {c: {"const": c, "id": i + 1} for i, c in enumerate(consts)}

    # display names
    names = re.findall(r'dname "([^"]*)"', git("data/pokemon/names.asm"))[:n]
    for c, nm in zip(consts, names):
        sp[c]["name"] = nm

    # base stats files, in order
    inc = re.findall(r'INCLUDE "(data/pokemon/base_stats/(\w+)\.asm)"', git("data/pokemon/base_stats.asm"))
    assert len(inc) == n
    for c, (path, slug) in zip(consts, inc):
        sp[c]["slug"] = slug
        t = git(path)
        sp[c]["base_stats_text"] = t
        m = re.search(r"db\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\n", t)
        sp[c]["stats"] = [int(x) for x in m.groups()]  # hp atk def spd sat sdf
        m = re.search(r"db (\w+), (\w+) ; type", t)
        sp[c]["types"] = [m.group(1), m.group(2)]
        sp[c]["growth"] = re.search(r"db (GROWTH_\w+) ; growth rate", t).group(1)
        sp[c]["catch"] = int(re.search(r"db (\d+) ; catch rate", t).group(1))
        sp[c]["exp"] = int(re.search(r"db (\d+) ; base exp", t).group(1))
        sp[c]["tmhm"] = re.search(r"\ttmhm (.*)\n", t).group(1) if re.search(r"\ttmhm (.*)\n", t) else ""
        sp[c]["gfxdir"] = re.search(r'INCBIN "gfx/pokemon/(\w+)/front.dimensions"', t).group(1)

    def table(path, rx, key):
        vals = re.findall(rx, git(path), flags=re.M)
        for c, v in zip(consts, vals[:n]):
            sp[c][key] = v
        return vals

    # cries
    cr = re.findall(r"^\tmon_cry (\w+),\s+(-?\d+),\s+(\d+)", git("data/pokemon/cries.asm"), flags=re.M)
    for c, v in zip(consts, cr[:n]):
        sp[c]["cry"] = (v[0], int(v[1]), int(v[2]))
    table("data/pokemon/menu_icons.asm", r"^\tdb (ICON_\w+)", "icon")
    pics = re.findall(r"^\tdba_pics (\w+), (\w+)", git("data/pokemon/pic_pointers.asm"), flags=re.M)
    for c, v in zip(consts, pics[:n]):
        sp[c]["pics"] = v
    table("data/pokemon/dex_entry_pointers.asm", r"^\tdw (\w+)", "dexlabel")
    table("data/pokemon/evos_attacks_pointers.asm", r"^\tdw (\w+)", "evoslabel")
    table("data/pokemon/egg_move_pointers.asm", r"^\tdw (\w+)", "egglabel")
    table("gfx/pokemon/anim_pointers.asm", r"^\tdw (\w+)", "animlabel")
    table("gfx/pokemon/idle_pointers.asm", r"^\tdw (\w+)", "idlelabel")
    table("gfx/pokemon/frame_pointers.asm", r"^\tdw (\w+)", "frameslabel")
    table("gfx/pokemon/bitmask_pointers.asm", r"^\tdw (\w+)", "bitmasklabel")
    dex = re.findall(r'^(\w+)::?\s+INCLUDE "data/pokemon/dex_entries/(\w+)\.asm"', git("data/pokemon/dex_entries.asm"), flags=re.M)
    lab2file = {a: b for a, b in dex}
    for c in consts:
        sp[c]["dexfile"] = lab2file[sp[c]["dexlabel"]]
    # evolutions + learnsets
    ev = git("data/pokemon/evos_attacks.asm")
    blocks = re.split(r"^(\w+EvosAttacks):\n", ev, flags=re.M)
    lab2block = {blocks[i]: blocks[i + 1] for i in range(1, len(blocks), 2)}
    for c in consts:
        blk = lab2block[sp[c]["evoslabel"]]
        evs, lvl = blk.split("db 0 ; no more evolutions\n")
        sp[c]["evo_text"] = evs
        moves = re.findall(r"^\tdb (\d+), (\w+)", lvl, flags=re.M)
        sp[c]["learnset"] = [(int(a), b) for a, b in moves]
    return consts, sp


if __name__ == "__main__":
    consts, sp = load()
    print(len(consts), sp["PIKACHU"]["types"], sp["PIKACHU"]["cry"], sp["PIKACHU"]["gfxdir"], sp["MR__MIME"]["slug"])
