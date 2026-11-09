#!/usr/bin/env python3
"""Removal script: takes the dead weight of vanilla Crystal out of the source, completely, and reports what it freed.

  maps       every vanilla map the player can never reach (tools/hardcore/map_reach.py), with its script, block data, attributes, scene
             variable and the map group tables.  Of the 388 vanilla maps only the opening (New Bark Town, the houses, Route 29) and Cherrygrove stay.
  tables     the data tables that only list dead maps (vanilla wild tables, tree and roaming Pokemon maps, spawn points, flypoints ...)

The script works on the current tree and can be run again: it recomputes the dead set every time, so a second run changes nothing.
Usage: python3 tools/hardcore/remove_baggage.py maps [--dry]"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_reach  # noqa: E402

ROOT = map_reach.ROOT
DRY = "--dry" in sys.argv


def path(p):
    return os.path.join(ROOT, p)


def read(p):
    with open(path(p)) as f:
        return f.read()


def write(p, s):
    if not DRY:
        with open(path(p), "w") as f:
            f.write(s)


def delete(p):
    if os.path.exists(path(p)) and not DRY:
        os.remove(path(p))


def camel(const):
    """NEW_BARK -> NewBark"""
    return "".join(w.capitalize() for w in const.split("_"))


# ------------------------------------------------------------------------------------------------------------ the map groups
def parse_groups():
    """The vanilla part of constants/map_constants.asm: [(group const name, index, [(map const, w, h)])] in order."""
    src = read("constants/map_constants.asm")
    body = src.split("\tconst_def\n", 1)[1].split('INCLUDE "constants/area_map_constants.asm"')[0]
    groups, cur = [], None
    for line in body.splitlines():
        m = re.match(r"\tnewgroup ([A-Z0-9_]+)", line)
        if m:
            cur = (m.group(1), len(groups) + 1, [])
            groups.append(cur)
            continue
        m = re.match(r"\tmap_const ([A-Z0-9_]+),\s*(\d+),\s*(\d+)", line)
        if m and cur:
            cur[2].append((m.group(1), int(m.group(2)), int(m.group(3))))
    return groups


def remove_maps():
    consts, attrs, graph = map_reach.edges()
    # the attributes table gives every map its label; the reachable set comes from the same graph the checker uses
    gen = set(re.findall(r"^\s*map_const ([A-Z0-9_]+),", read("constants/area_map_constants.asm"), re.M))
    seen, todo = set(), list({"PLAYERS_HOUSE_2F"} | gen)
    while todo:
        c = todo.pop()
        if c not in seen:
            seen.add(c)
            todo.extend(graph.get(c, ()))
    label_of = {c: l for l, c in attrs.items()}
    dead = [c for c in consts if c not in seen]
    if not dead:
        print("maps: nothing to remove")
        return 0
    dead_set = set(dead)
    dead_labels = {label_of[c] for c in dead if c in label_of}
    groups = parse_groups()
    kept_groups = [(n, i, [m for m in ms if m[0] not in dead_set]) for n, i, ms in groups]
    kept_groups = [g for g in kept_groups if g[2]]
    dead_group_names = {n for n, _, ms in groups} - {n for n, _, _ in kept_groups}
    print(f"maps: removing {len(dead)} maps and {len(dead_group_names)} map groups, keeping groups {[n for n, _, _ in kept_groups]}")

    # 1. constants/map_constants.asm: the vanilla groups again, renumbered
    src = read("constants/map_constants.asm")
    head, rest = src.split("\tconst_def\n", 1)
    _, tail = rest.split('INCLUDE "constants/area_map_constants.asm"', 1)
    out = [head, "\tconst_def\n\n"]
    for gi, (n, _, ms) in enumerate(kept_groups, 1):
        out.append(f"\tnewgroup {n:<53}; {gi}\n")
        for mi, (c, w, h) in enumerate(ms, 1):
            out.append(f"\tmap_const {c + ',':<46}{w:>2}, {h:>2} ; {mi:>2}\n")
        out.append("\tendgroup\n\n")
    out.append('INCLUDE "constants/area_map_constants.asm"' + tail)
    s = "".join(out)
    s = re.sub(r"DEF NUM_MAP_GROUPS EQU const_value ; \d+", f"DEF NUM_MAP_GROUPS EQU const_value ; {len(kept_groups)} vanilla groups plus the generated ones", s)
    write("constants/map_constants.asm", s)

    # 2. data/maps/maps.asm: the group pointers, the groups, the map lines
    lines = read("data/maps/maps.asm").splitlines(keepends=True)
    out, i, in_ptr, cur_block = [], 0, False, None
    kept_labels = {f"MapGroup_{camel(n)}" for n, _, _ in kept_groups}
    ptr_done = False
    for line in lines:
        if line.startswith("MapGroupPointers::"):
            in_ptr = True
            out.append(line)
            continue
        if in_ptr:
            m = re.match(r"\tdw (MapGroup_\w+)\s*;", line)
            if m:
                if m.group(1) in kept_labels:
                    out.append(f"\tdw {m.group(1):<20}; {sum(1 for l in out if re.match(chr(9) + 'dw MapGroup_', l)) + 1}\n")
                continue
            if "table_width" in line or line.startswith(";"):
                out.append(line)
                continue
            in_ptr = False  # the INCLUDE of the generated groups and the assert end the table
        m = re.match(r"(MapGroup_\w+):", line)
        if m:
            cur_block = m.group(1)
        if cur_block and cur_block not in kept_labels and re.match(r"MapGroup_\w+:", line) and not re.match(r"MapGroup_(Area|Open|Purg)", cur_block) \
                and cur_block in {f"MapGroup_{camel(n)}" for n in dead_group_names}:
            out.append("\x00" + line)  # marker: the whole block goes
            continue
        m = re.match(r"\tmap (\w+),", line)
        if m and m.group(1) in dead_labels:
            continue
        out.append(line)
    # drop the marked blocks (from the marker to the assert_table_length line, and the blank line after it)
    res, skipping = [], False
    for line in out:
        if line.startswith("\x00"):
            skipping = True
            continue
        if skipping:
            if line.startswith("\tassert_table_length"):
                skipping = False
                continue
            if line.startswith("\t"):
                continue
            # the blank line after an assert, or the next block label
            skipping = False
        res.append(line)
    text = "".join(res)
    text = re.sub(r"\n{3,}", "\n\n", text)
    write("data/maps/maps.asm", text)

    # 3. data/maps/attributes.asm: the block of a map starts at its map_attributes line and ends at the next one
    lines = read("data/maps/attributes.asm").splitlines(keepends=True)
    out, skip = [], False
    for line in lines:
        m = re.match(r"\tmap_attributes (\w+),", line)
        if m:
            skip = m.group(1) in dead_labels
        if not skip:
            out.append(line)
    write("data/maps/attributes.asm", re.sub(r"\n{3,}", "\n\n", "".join(out)))

    # 4. data/maps/blocks.asm and scripts.asm, scenes.asm
    s = read("data/maps/blocks.asm")
    for lab in dead_labels:
        s = re.sub(rf"{lab}_Blocks:\n\tINCBIN \"maps/{lab}\.blk\"\n\n?", "", s)
    write("data/maps/blocks.asm", s)
    s = read("data/maps/scripts.asm")
    for lab in dead_labels:
        s = s.replace(f'INCLUDE "maps/{lab}.asm"\n', "")
    write("data/maps/scripts.asm", s)
    s = read("data/maps/scenes.asm")
    s = "".join(l for l in s.splitlines(keepends=True) if not (l.strip().startswith("scene_var ") and l.split()[1].rstrip(",") in dead_set))
    write("data/maps/scenes.asm", s)

    # 5. the tables with one entry per map group
    keep_idx = [i for _, i, _ in kept_groups]  # original 1-based indexes of the groups that stay
    s = read("data/maps/roofs.asm")
    head, tab = s.split("MapGroupRoofs:", 1)
    rows = re.findall(r"\tdb (\S+)\s*;\s*(\d+)", tab)
    byidx = {int(i): v for v, i in rows}
    t = ["MapGroupRoofs:\n; entries correspond to MAPGROUP_* constants\n; values are indexes for Roofs (see below)\n\ttable_width 1\n\tdb -1             ;  0\n"]
    for gi, (n, oi, _) in enumerate(kept_groups, 1):
        t.append(f"\tdb {byidx[oi]:<14}; {gi:>2} ({camel(n)})\n")
    rest_after = tab[tab.index("INCLUDE"):] if "INCLUDE" in tab else ""
    write("data/maps/roofs.asm", head + "".join(t) + rest_after)

    s = read("data/maps/sgb_roof_pal_inds.asm")
    head, tab = s.split("MapGroupRoofSGBPalInds:", 1)
    vals = re.findall(r"^\tdb (PREDEFPAL_\w+)\s*$", tab, re.M)  # index 0 is the placeholder, then the 26 groups
    t = ["MapGroupRoofSGBPalInds:\n; entries correspond to map groups\n\ttable_width 1\n", f"\tdb {vals[0]}\n"]
    for _, oi, _ in kept_groups:
        t.append(f"\tdb {vals[oi]}\n")
    rest_after = tab[tab.index("\tINCLUDE"):]
    write("data/maps/sgb_roof_pal_inds.asm", head + "".join(t) + rest_after)

    s = read("data/maps/outdoor_sprites.asm")
    for n in dead_group_names:
        s = s.replace(f"\tdw {camel(n)}GroupSprites\n", "")
        s = re.sub(rf"{camel(n)}GroupSprites:\n(?:\tdb .*\n)+\n?", "", s)
    write("data/maps/outdoor_sprites.asm", s)

    # 6. the files of the maps
    for lab in dead_labels:
        delete(f"maps/{lab}.asm")
        delete(f"maps/{lab}.blk")
    print(f"maps: deleted {len(dead_labels)} map sources and block files")
    return len(dead)


# ------------------------------------------------------------------------------------------------------------ tables that name maps
def live_labels():
    return set(re.findall(r"^\tmap_attributes (\w+),", read("data/maps/attributes.asm"), re.M))


def clean_blocks():
    """data/maps/blocks.asm: a chunk is a run of Label_Blocks: lines and the INCBIN under them.  Labels of removed maps go, a chunk without labels goes,
    and so does every .blk file under maps/ that no chunk includes any more."""
    live = live_labels()
    lines = read("data/maps/blocks.asm").splitlines(keepends=True)
    out, labels = [], []
    used = set()
    for line in lines:
        m = re.match(r"(\w+)_Blocks:", line)
        if m and not line.startswith("\t"):
            if m.group(1) in live or m.group(1).startswith("Beta") and False:
                labels.append(line)
            else:
                labels.append(None)
            continue
        m = re.match(r'\tINCBIN "(maps/[^"]+\.blk)"', line)
        if m and labels:
            keep = [l for l in labels if l]
            if keep:
                out.extend(keep)
                out.append(line)
                used.add(m.group(1))
                out.append("\n")
            labels = []
            continue
        if labels:
            labels = []
        if line.strip() or (out and out[-1].strip()):
            out.append(line)
    write("data/maps/blocks.asm", re.sub(r"\n{3,}", "\n\n", "".join(out)))
    gone = 0
    for d, _, fs in os.walk(path("maps")):
        rel = os.path.relpath(d, ROOT)
        if rel.startswith("maps/gen"):
            continue
        for f in fs:
            if f.endswith(".blk") and f"{rel}/{f}" not in used:
                delete(f"{rel}/{f}")
                gone += 1
    print(f"blocks: {len(used)} block files stay, {gone} unused .blk files deleted")


def clean_roof_pals():
    """gfx/tilesets/roofs.pal: one two-line entry per map group; the groups of the vanilla world that are gone lose theirs."""
    names = {re.sub(r"[^a-z]", "", n.lower()) for n, _, _ in parse_groups()}
    src = read("gfx/tilesets/roofs.pal")
    parts = re.split(r"(?m)^(?=; group \d+)", src)
    head, entries = parts[0], parts[1:]
    tail = ""
    if entries and "INCLUDE" in entries[-1]:
        last, tail = entries[-1].split("INCLUDE", 1)
        entries[-1] = last
        tail = "INCLUDE" + tail
    keep = [e for e in entries if re.match(r"; group (\d+) \(([^)]*)\)", e).group(1) == "0"
            or re.sub(r"[^a-z]", "", re.match(r"; group (\d+) \(([^)]*)\)", e).group(2).lower()) in names]
    out = []
    for i, e in enumerate(keep):
        out.append(re.sub(r"^; group \d+", f"; group {i}", e, count=1).rstrip("\n") + "\n\n")
    write("gfx/tilesets/roofs.pal", head + "".join(out) + tail)
    print(f"roof palettes: {len(keep)} groups stay")


def live_consts():
    return {c for _, _, ms in parse_groups() for c, _, _ in ms} | set(
        re.findall(r"^\s*map_const ([A-Z0-9_]+),", read("constants/area_map_constants.asm"), re.M))


def clean_wild():
    """The vanilla wild tables keep only the blocks of maps that are still in the game."""
    live = live_consts()
    for f in ("johto_grass", "johto_water", "kanto_grass", "kanto_water"):
        p = f"data/wild/{f}.asm"
        src = read(p)
        parts = re.split(r"(?m)^(?=\tdef_(?:grass|water)_wildmons )", src)
        head, blocks = parts[0], parts[1:]
        tail = ""
        if blocks and "\tdb -1 ; end" in blocks[-1]:
            last, t = blocks[-1].split("\tdb -1 ; end", 1)
            blocks[-1], tail = last, "\tdb -1 ; end" + t
        keep = [b for b in blocks if re.match(r"\tdef_\w+_wildmons (\w+)", b).group(1) in live]
        write(p, head + "".join(keep) + tail)
        print(f"wild {f}: {len(keep)} of {len(blocks)} blocks stay")
    # swarms: a swarm block is a comment line, map_id and the table until the blank line
    for f in ("swarm_grass",):
        p = f"data/wild/{f}.asm"
        src = read(p)
        parts = re.split(r"(?m)^(?=; \w+ swarm\n\tmap_id )", src)
        head, blocks = parts[0], parts[1:]
        tail = ""
        if blocks and "\tdb -1 ; end" in blocks[-1]:
            last, t = blocks[-1].split("\tdb -1 ; end", 1)
            blocks[-1], tail = last, "\tdb -1 ; end" + t
        keep = [b for b in blocks if re.search(r"\tmap_id (\w+)", b).group(1) in live]
        write(p, head + "".join(keep) + tail)
        print(f"wild {f}: {len(keep)} of {len(blocks)} blocks stay")
    # treemon maps: one line per map
    p = "data/wild/treemon_maps.asm"
    src = read(p)
    lines = [l for l in src.splitlines(keepends=True) if not (l.startswith("\ttreemon_map ") and l.split()[1].rstrip(",") not in live)]
    write(p, "".join(lines))


# ------------------------------------------------------------------------------------------------------------ whole features
FEATURES = {
    # name: (files and directories that go, what it was)
    "battle_tower": (["engine/events/battle_tower", "constants/battle_tower_constants.asm", "data/battle_tower"], "Battle Tower (maps are gone already)"),
    "printer": (["engine/printer", "engine/events/print_photo.asm", "engine/events/print_unown.asm", "engine/events/print_unown_2.asm",
                 "constants/printer_constants.asm"], "Game Boy Printer"),
    "games": (["engine/games"], "slot machine, card flip, Unown puzzle, memory game (the Game Corner)"),
    "events": (["engine/events/bug_contest", "engine/events/magnet_train.asm", "engine/events/celebi.asm", "engine/events/dratini.asm",
                "engine/events/shuckle.asm", "engine/events/odd_egg.asm", "engine/events/kurt.asm",
                "engine/events/kurt_selectquantity_interpretjoypad.asm", "engine/events/buena.asm", "engine/events/buena_menu.asm",
                "engine/events/lucky_number.asm", "engine/events/name_rater.asm", "engine/events/haircut.asm", "engine/events/poke_seer.asm",
                "engine/events/elevator.asm", "engine/events/basement_key.asm", "engine/events/card_key.asm", "engine/events/npc_trade.asm",
                "engine/events/daycare.asm", "engine/events/move_deleter.asm", "data/events/npc_trades.asm", "data/events/elevator_floors.asm", "data/events/bug_contest_flags.asm",
                "data/events/bug_contest_winners.asm", "data/events/odd_eggs.asm", "data/items/buena_prizes.asm", "data/items/apricorn_balls.asm",
                "data/wild/bug_contest_mons.asm", "data/items/bargain_shop.asm", "data/items/rooftop_sale.asm"],
               "vanilla event machinery that only the dead maps used: bug contest, magnet train, Celebi, Dratini, Shuckle, odd egg, Kurt, Buena, "
               "lucky number, name rater, haircut, Poke Seer, elevator, keys, NPC trades, day care, move deleter"),
    "phone": (["engine/phone", "data/phone", "engine/events/mom_phone.asm", "constants/phone_constants.asm"], "phone calls and the phone card"),
    "radio": (["engine/pokegear/radio.asm", "data/radio", "constants/radio_constants.asm"], "Pokegear radio (stations, Pokemon Talk, Lucky Channel) and the radio card"),
    "mobile": (["mobile", "lib/mobile", "constants/mobile_constants.asm", "gfx/mobile", "audio/music/mobileadapter.asm",
                "audio/music/mobileadaptermenu.asm", "audio/music/mobilecenter.asm"], "Mobile Adapter (menus, battle room, news, EZ Chat) and its SDK library"),
    "link": (["engine/link", "engine/battle/link_result.asm", "engine/movie/trade_animation.asm", "constants/serial_constants.asm",
              "constants/npc_trade_constants.asm", "data/decorations/mystery_gift_decos.asm", "data/items/mystery_gift_items.asm"],
             "link cable: colosseum, trade centre, Mystery Gift, Time Capsule, link battle results, trade animation"),
}


def drop_includes(gone):
    """Remove every INCLUDE line that names a deleted file, in all sources."""
    gone = set(gone)
    n = 0
    for top in ("main.asm", "home.asm", "audio.asm", "ram.asm", "includes.asm", "engine", "home", "data", "gfx", "audio", "maps", "macros", "constants", "ram", "mobile", "lib"):
        base = path(top)
        files = [base] if os.path.isfile(base) else [os.path.join(d, f) for d, _, fs in os.walk(base) for f in fs]
        for fp in files:
            if not fp.endswith(".asm"):
                continue
            try:
                s = open(fp).read()
            except (UnicodeDecodeError, OSError):
                continue
            if "INCLUDE" not in s:
                continue
            out = []
            for l in s.splitlines(keepends=True):
                m = re.match(r'\s*INCLUDE\s+"([^"]+)"', l)
                if m and m.group(1) in gone:
                    n += 1
                    continue
                out.append(l)
            t = "".join(out)
            if t != s and not DRY:
                open(fp, "w").write(t)
    return n


def drop(names):
    removed = []
    for name in names:
        paths, what = FEATURES[name]
        for p in paths:
            full = path(p)
            if os.path.isdir(full):
                for d, _, fs in os.walk(full):
                    for f in fs:
                        removed.append(os.path.relpath(os.path.join(d, f), ROOT))
                if not DRY:
                    import shutil
                    shutil.rmtree(full)
            elif os.path.exists(full):
                removed.append(p)
                delete(p)
        print(f"{name}: {what}")
    bytes_ = 0
    n = drop_includes(removed)
    print(f"deleted {len(removed)} files, removed {n} INCLUDE lines")


def main():
    cmds = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cmds:
        print(__doc__)
        return
    if cmds[0] == "features":
        drop(cmds[1:] or list(FEATURES))
        return
    for c in cmds:
        {"maps": remove_maps, "blocks": clean_blocks, "roofpals": clean_roof_pals, "wild": clean_wild}[c]()


if __name__ == "__main__":
    main()
