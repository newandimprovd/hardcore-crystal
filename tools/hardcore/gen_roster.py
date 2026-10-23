#!/usr/bin/env python3
"""Hardcore Crystal roster generator (stage 4).

Turns tools/hardcore/roster/roster_data.py (62 four-stage lines, 97 new species) into assembly:
  * constants/pokemon_constants.asm (248 species, aliases for removed names)
  * every per-species table: base stats, names, cries, palettes, icons, pics, Pokedex entries and
    orders, evolutions and learnsets, egg move pointers, animation/frame/bitmask/idle pointers,
    footprints
  * engine patches: per-species animation frames bank, Pokedex flag array size

Everything is rebuilt from files at the base commit (and from the stage 2 move tables in the
working tree), so running it twice gives identical output.  Run gen_moves.py first.
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "roster"))
import vanilla  # noqa: E402
import roster_data as R  # noqa: E402
import gen_moves as GM  # noqa: E402
from textgen import wrap_lines  # noqa: E402

NUM_POKEMON = 248
EGG_ID = 253
STAGE_LEVELS = [25, 50, 75]


def git(path):
    return vanilla.git(path)


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def camel(const):
    return "".join(p.capitalize() for p in const.split("_"))


# ---------------------------------------------------------------------------------------------
# Species table
# ---------------------------------------------------------------------------------------------
CURVE = [300, 395, 485, 565]
APEX_CURVE = [300, 420, 600, 665]
FINAL_HP_BONUS = 35
ARCH = {
    "bal": [1, 1, 1, 1, 1, 1],
    "phys": [1.0, 1.25, 1.0, 1.0, 0.8, 1.0],
    "spec": [1.0, 0.8, 1.0, 1.0, 1.25, 1.0],
    "tank": [1.2, 1.0, 1.2, 0.7, 1.0, 1.15],
    "fast": [0.9, 1.0, 0.85, 1.35, 1.0, 1.0],
    "wall": [1.0, 0.8, 1.3, 0.6, 1.0, 1.3],
}


def split_types(spec):
    ts = spec.split("/")
    if len(ts) == 1:
        ts = ts * 2
    return [("PSYCHIC_TYPE" if t == "PSYCHIC" else t) for t in ts]


def distribute(props, total):
    """Integer stats that follow `props` and add up to `total`, each within 5..255."""
    s = sum(props)
    raw = [p / s * total for p in props]
    out = [max(5, min(255, int(r))) for r in raw]
    order = sorted(range(6), key=lambda i: raw[i] - int(raw[i]), reverse=True)
    i = 0
    while sum(out) < total:
        k = order[i % 6]
        if out[k] < 255:
            out[k] += 1
        i += 1
    while sum(out) > total:
        k = max(range(6), key=lambda j: out[j])
        out[k] -= 1
    return out


def build():
    consts, vsp = vanilla.load()
    keep = [s for _, st in R.LINES for s in st if not s.startswith("*")]
    removed = [c for c in consts if c not in keep]
    freed = sorted(vsp[c]["id"] for c in removed if vsp[c]["id"] <= NUM_POKEMON)
    new_order = [s[1:] for _, st in R.LINES for s in st if s.startswith("*")]
    assert len(freed) == len(new_order) == 97
    new_id = dict(zip(new_order, freed))

    S = {}
    line_of = {}
    for lkey, stages in R.LINES:
        prev = None
        for k, s in enumerate(stages):
            c = s[1:] if s.startswith("*") else s
            line_of[c] = lkey
            rec = {"const": c, "stage": k + 1, "line": lkey, "prev": prev, "next": None, "new": s.startswith("*")}
            if prev:
                S[prev]["next"] = c
            if rec["new"]:
                nd = R.NEW[c]
                rec.update(id=new_id[c], name=c, slug=c.lower(), label=c.capitalize(), nd=nd)
                rec["types"] = split_types(nd["types"])
            else:
                v = vsp[c]
                rec.update(id=v["id"], name=v["name"], slug=v["slug"], v=v, label=None)
                tspec = R.TYPE_OVERRIDE.get(c)
                rec["types"] = split_types(tspec) if tspec else list(v["types"])
            S[c] = rec
            prev = c
    # gfx source (a vanilla species) and template (previous stage)
    for lkey, stages in R.LINES:
        for s in stages:
            c = s[1:] if s.startswith("*") else s
            rec = S[c]
            if not rec["new"]:
                rec["gfx"] = c
            else:
                src = rec["nd"]["src"] or rec["prev"]
                rec["gfx"] = S[src]["gfx"] if src in S else src
                assert not S[rec["gfx"]]["new"]
    # stats
    for lkey, stages in R.LINES:
        apex = lkey in R.APEX_LINES
        opt = R.LINE_OPT.get(lkey, {})
        prev_props = None
        for k, s in enumerate(stages):
            c = s[1:] if s.startswith("*") else s
            rec = S[c]
            curve = APEX_CURVE if apex else CURVE
            total = curve[k] * (1.0 if apex else opt.get("s", 1.0))
            if k == 0 and "s1" in opt:
                total = opt["s1"]
            total = int(round(total))
            if rec["new"]:
                props = [a * b for a, b in zip(prev_props, ARCH[rec["nd"]["arch"]])]
            else:
                props = list(rec["v"]["stats"])
            prev_props = [p / sum(props) for p in props]
            stats = distribute(props, total)
            if k == 3:
                stats[0] = min(255, stats[0] + FINAL_HP_BONUS)
            rec["stats"] = stats
    return consts, vsp, S, removed


def species_by_id(S):
    by = {r["id"]: r for r in S.values()}
    assert sorted(by) == list(range(1, NUM_POKEMON + 1)), "ID gaps"
    return [by[i] for i in range(1, NUM_POKEMON + 1)]


# ---------------------------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------------------------
def gen_constants(L, removed):
    t = git("constants/pokemon_constants.asm")
    head, rest = t.split("\tconst BULBASAUR", 1)
    m = re.search(r"\tconst CELEBI\s+; fb\n", rest)
    tail = rest[m.end():]
    assert tail.startswith("DEF NUM_POKEMON")
    lines = []
    for r in L:
        if r["id"] == 152:
            lines.append("DEF JOHTO_POKEMON EQU const_value")
        lines.append(f"\tconst {r['const']:<10} ; {r['id']:02x}")
    tail_new = [
        "DEF NUM_POKEMON EQU const_value - 1",
        "",
        "; Vanilla species that no longer exist keep their names so that vanilla data still assembles.",
        "; Names the engine special-cases are parked on an ID no species can have, so the special",
        "; code can never match a real species.  Everything else aliases a surviving species.",
    ]
    for c in R.PARKED:
        tail_new.append(f"DEF {c} EQU $fe")
    for c in removed:
        if c in R.ALIAS:
            tail_new.append(f"DEF {c} EQU {R.ALIAS[c]}")
    tail_new += ["", f"\tconst_skip {EGG_ID - 1 - NUM_POKEMON} ; unused IDs", "\tconst EGG        ; fd"]
    after = tail.split("\tconst EGG        ; fd\n", 1)[1]
    write("constants/pokemon_constants.asm", head + "\n".join(lines) + "\n" + "\n".join(tail_new) + "\n" + after)


# ---------------------------------------------------------------------------------------------
# base stats
# ---------------------------------------------------------------------------------------------
def exp_yield(rec):
    bst = sum(rec["stats"])
    return max(36, min(255, int(round(bst * 0.38))))


def catch_rate(rec):
    if not rec["new"]:
        return rec["v"]["catch"]
    return 45 if rec["stage"] == 3 else 25


def gen_base_stats(L):
    base = git("data/pokemon/base_stats.asm")
    head = base.split('INCLUDE "data/pokemon/base_stats/')[0]
    inc = [f'INCLUDE "data/pokemon/base_stats/{r["slug"]}.asm"' for r in L]
    write("data/pokemon/base_stats.asm", head + "\n".join(inc) + "\n\tassert_table_length NUM_POKEMON\n")
    by_const = {r["const"]: r for r in L}
    texts = {}

    def text_for(r):
        if r["const"] in texts:
            return texts[r["const"]]
        if r["new"]:
            tpl = text_for(by_const[r["prev"]])
            gfxdir = R_gfxdir[r["gfx"]]
        else:
            tpl = r["v"]["base_stats_text"]
            gfxdir = r["v"]["gfxdir"]
        t = tpl
        t = re.sub(r"^\tdb \w+ ; \d+", f"\tdb {r['const']} ; {r['id']:03d}", t, count=1, flags=re.M)
        s = r["stats"]
        t = re.sub(r"^\tdb\s+\d+,\s+\d+,\s+\d+,\s+\d+,\s+\d+,\s+\d+$",
                   "\tdb " + ", ".join(f"{x:3d}" for x in s), t, count=1, flags=re.M)
        t = re.sub(r"^\tdb \w+, \w+ ; type", f"\tdb {r['types'][0]}, {r['types'][1]} ; type", t, count=1, flags=re.M)
        t = re.sub(r"^\tdb \d+ ; catch rate", f"\tdb {catch_rate(r)} ; catch rate", t, count=1, flags=re.M)
        t = re.sub(r"^\tdb \d+ ; base exp", f"\tdb {exp_yield(r)} ; base exp", t, count=1, flags=re.M)
        t = re.sub(r'INCBIN "gfx/pokemon/\w+/front.dimensions"', f'INCBIN "gfx/pokemon/{gfxdir}/front.dimensions"', t)
        t = GM.word_sub(t, GM.REMAP)
        texts[r["const"]] = t
        return t

    for r in L:
        write(f"data/pokemon/base_stats/{r['slug']}.asm", text_for(r))


# ---------------------------------------------------------------------------------------------
# names, cries, icons, pics, pointers
# ---------------------------------------------------------------------------------------------
def gen_names(L):
    t = git("data/pokemon/names.asm")
    head = t.split("\tdname", 1)[0]
    out = head.rstrip("\n").split("\n")
    for r in L:
        out.append(f'\tdname "{r["name"]}"')
    out.append("\tassert_table_length NUM_POKEMON")
    for _ in range(EGG_ID - 1 - NUM_POKEMON):
        out.append('\tdname "?????"')
    out += ['\tdname "EGG"', "\tassert_table_length EGG", '\tdname "?????"', '\tdname "?????"', '\tdname "?????"',
            "\tassert_table_length $100"]
    write("data/pokemon/names.asm", "\n".join(out) + "\n")


def new_cry(r, vsp):
    base_species = r["gfx"]
    cry, pitch, length = vsp[base_species]["cry"]
    st = r["stage"]
    if st == 3:
        return cry, pitch - 48, length + 40
    return cry, pitch - 96, length + 80


def gen_cries(L, vsp):
    t = git("data/pokemon/cries.asm")
    head = t.split("\tmon_cry ", 1)[0]
    out = head.rstrip("\n").split("\n")
    for r in L:
        if r["new"]:
            cry, pitch, length = new_cry(r, vsp)
        else:
            cry, pitch, length = r["v"]["cry"]
        out.append(f"\tmon_cry {cry}, {pitch:4d}, {length:4d} ; {r['const']}")
    out.append("\tassert_table_length NUM_POKEMON")
    for i in range(NUM_POKEMON + 1, 256):
        out.append(f"\tmon_cry CRY_NIDORAN_M,     0,    0 ; {i}")
    out.append("\tassert_table_length $ff")
    write("data/pokemon/cries.asm", "\n".join(out) + "\n")


def gen_icons(L, vsp):
    t = git("data/pokemon/menu_icons.asm")
    head = t.split("\tdb ICON_", 1)[0].rstrip("\n").split("\n")
    out = head[:]
    for r in L:
        icon = vsp[r["gfx"]]["icon"] if r["new"] else r["v"]["icon"]
        if r["new"] and r["nd"]["icon"]:
            icon = r["nd"]["icon"]
        out.append(f"\tdb {icon:<18}; {r['const']}")
    out.append("\tassert_table_length NUM_POKEMON")
    write("data/pokemon/menu_icons.asm", "\n".join(out) + "\n")


def gen_pointer_tables(L, vsp):
    def sv(r):  # vanilla record that supplies graphics data
        return vsp[r["gfx"]]

    # pics
    t = git("data/pokemon/pic_pointers.asm")
    head = t.split("\tdba_pics ", 1)[0].rstrip("\n").split("\n")
    out = head[:]
    for r in L:
        a, b = sv(r)["pics"]
        out.append(f"\tdba_pics {a}, {b}")
    out.append("\tassert_table_length NUM_POKEMON")
    for _ in range(EGG_ID - 1 - NUM_POKEMON):
        out.append("\tdba_pics ; unused")
    out += ["\tdba_pics EggPic ; Egg has no back sprite", "\tassert_table_length EGG"]
    write("data/pokemon/pic_pointers.asm", "\n".join(out) + "\n")

    def simple(path, key, fmt="\tdw {}"):
        t = git(path)
        head = t.split("\tdw ", 1)[0].rstrip("\n").split("\n")
        o = head[:]
        for r in L:
            o.append(fmt.format(sv(r)[key]))
        o.append("\tassert_table_length NUM_POKEMON")
        return o

    write("gfx/pokemon/anim_pointers.asm", "\n".join(simple("gfx/pokemon/anim_pointers.asm", "animlabel")) + "\n")
    write("gfx/pokemon/idle_pointers.asm", "\n".join(simple("gfx/pokemon/idle_pointers.asm", "idlelabel")) + "\n")
    write("gfx/pokemon/bitmask_pointers.asm", "\n".join(simple("gfx/pokemon/bitmask_pointers.asm", "bitmasklabel")) + "\n")
    fr = simple("gfx/pokemon/frame_pointers.asm", "frameslabel")
    fr += ["", "; Hardcore Crystal: the bank of each species' frame set (see GetMonFramesPointer), so any",
           "; species can reuse the frames of any other species.", "FramesBanks:", "\ttable_width 1"]
    for r in L:
        fr.append(f"\tdb BANK({sv(r)['frameslabel']})")
    fr.append("\tassert_table_length NUM_POKEMON")
    write("gfx/pokemon/frame_pointers.asm", "\n".join(fr) + "\n")


def gen_palettes(L, vsp):
    pal = json.load(open(HERE / "roster/vanilla_pal.json"))
    t = git("data/pokemon/palettes.asm")
    head, rest = t.split('INCBIN "gfx/pokemon/bulbasaur/normal.gbcpal", middle_colors', 1)
    tail = t.split("\tassert_table_length NUM_POKEMON + 1\n", 1)[1]
    pad_block, tail_rest = tail.split("INCBIN \"gfx/pokemon/egg/front.gbcpal\"", 1)
    out = [head.rstrip("\n")]
    out.append("")
    for r in L:
        if not r["new"]:
            d = r["v"]["gfxdir"]
            out.append(f'INCBIN "gfx/pokemon/{d}/normal.gbcpal", middle_colors')
            out.append(f'INCLUDE "gfx/pokemon/{d}/shiny.pal"')
        else:
            n, s = new_palette(r, pal, vsp)
            out.append(f"; {r['const']}")
            for c in n:
                out.append(f"\tRGB {c[0]:2d}, {c[1]:2d}, {c[2]:2d}")
            out.append(f"; {r['const']} shiny")
            for c in s:
                out.append(f"\tRGB {c[0]:2d}, {c[1]:2d}, {c[2]:2d}")
    out.append("")
    out.append("\tassert_table_length NUM_POKEMON + 1")
    text = "\n".join(out) + "\n"
    for i in range(NUM_POKEMON + 1, EGG_ID):
        text += pad_block.replace("; 252 shiny", f"; {i} shiny").replace("; 252\n", f"; {i}\n")
    text += 'INCBIN "gfx/pokemon/egg/front.gbcpal"' + tail_rest
    write("data/pokemon/palettes.asm", text)


TINT = {
    "NORMAL": ((24, 22, 18), (14, 12, 9)), "FIGHTING": ((26, 14, 10), (16, 6, 4)),
    "FLYING": ((22, 24, 31), (12, 14, 24)), "POISON": ((24, 10, 26), (14, 4, 17)),
    "GROUND": ((26, 22, 12), (16, 12, 5)), "ROCK": ((22, 20, 14), (13, 11, 7)),
    "BUG": ((20, 27, 8), (10, 17, 3)), "GHOST": ((18, 12, 26), (9, 5, 16)),
    "STEEL": ((22, 24, 26), (12, 14, 17)), "FIRE": ((31, 18, 8), (26, 6, 2)),
    "WATER": ((12, 20, 31), (5, 10, 24)), "GRASS": ((14, 28, 10), (5, 17, 4)),
    "ELECTRIC": ((31, 28, 6), (24, 18, 0)), "PSYCHIC_TYPE": ((31, 16, 22), (22, 6, 14)),
    "ICE": ((20, 28, 31), (10, 18, 27)), "DRAGON": ((20, 12, 30), (10, 4, 22)),
    "DARK": ((14, 12, 14), (6, 4, 8)), "FAIRY": ((31, 20, 26), (26, 10, 18)),
}


def lerp(a, b, f):
    return [a[i] + (b[i] - a[i]) * f for i in range(3)]


def clamp5(c):
    return [max(0, min(31, int(round(x)))) for x in c]


def new_palette(r, pal, vsp):
    d = vsp[r["gfx"]]["gfxdir"]
    if r["nd"]["pal"]:
        n = [list(c) for c in r["nd"]["pal"]]
    else:
        src = pal[d]
        t1, t2 = r["types"][0], r["types"][1]
        n = []
        for i in range(2):
            c = lerp(src[i], TINT[t1][i], 0.5)
            if t2 != t1:
                c = lerp(c, TINT[t2][i], 0.2)
            f = 1.0 if r["stage"] == 3 else 0.9
            if "DARK" in r["types"] or "GHOST" in r["types"]:
                f *= 0.8
            n.append(clamp5([x * f for x in c]))
    s = [[c[1], c[2], c[0]] for c in n]  # shiny: channel rotation
    return n, s


# ---------------------------------------------------------------------------------------------
# Pokedex
# ---------------------------------------------------------------------------------------------
def dex_text(rec):
    nd = rec["nd"]
    lines = wrap_lines(nd["text"], 18)
    if len(lines) > 6:
        raise ValueError(f"{rec['const']}: dex text has {len(lines)} lines: {nd['text']}")
    ft, inch = nd["ht"].split("'")
    height = int(ft) * 100 + int(inch)
    weight = int(round(nd["wt"] * 10))
    p1, p2 = lines[:3], lines[3:]
    out = [f'\tdb "{nd["cat"]}@" ; species name', f"\tdw {height}, {weight} ; height, weight", ""]
    for i, ln in enumerate(p1):
        end = "@" if (not p2 and i == len(p1) - 1) else ""
        out.append(f'\tdb   "{ln}{end}"' if i == 0 else f'\tnext "{ln}{end}"')
    if p2:
        out.append("")
        for i, ln in enumerate(p2):
            end = "@" if i == len(p2) - 1 else ""
            out.append(f'\t{"page" if i == 0 else "next"} "{ln}{end}"')
    return "\n".join(out) + "\n"


def gen_dex(L):
    for r in L:
        if r["new"]:
            write(f"data/pokemon/dex_entries/{r['slug']}.asm", dex_text(r))
    # pointers
    t = git("data/pokemon/dex_entry_pointers.asm")
    head = t.split("\tdw ", 1)[0].rstrip("\n").split("\n")
    out = head[:]
    for r in L:
        out.append(f"\tdw {r['label'] or camel(r['const'])}PokedexEntry" if r["new"] else f"\tdw {r['v']['dexlabel']}")
    out.append("\tassert_table_length NUM_POKEMON")
    write("data/pokemon/dex_entry_pointers.asm", "\n".join(out) + "\n")
    # entries, 64 per section
    out = []
    for i in range(0, NUM_POKEMON, 64):
        chunk = L[i:i + 64]
        # the last section keeps its vanilla name because layout.link refers to it
        out.append(f'SECTION "Pokedex Entries {i + 1:03d}-{min(i + 64, 251):03d}", ROMX')
        out.append("")
        for r in chunk:
            lab = (r["label"] + "PokedexEntry") if r["new"] else r["v"]["dexlabel"]
            f = r["slug"] if r["new"] else r["v"]["dexfile"]
            out.append(f'{lab + "::":<24} INCLUDE "data/pokemon/dex_entries/{f}.asm"')
        out.append("")
        out.append("")
    write("data/pokemon/dex_entries.asm", "\n".join(out).rstrip("\n") + "\n")
    # orders
    t = git("data/pokemon/dex_order_new.asm")
    head = t.split("\tdb ", 1)[0].rstrip("\n").split("\n")
    order = [s[1:] if s.startswith("*") else s for _, st in R.LINES for s in st]
    write("data/pokemon/dex_order_new.asm",
          "\n".join(head + [f"\tdb {c}" for c in order] + ["\tassert_table_length NUM_POKEMON"]) + "\n")
    t = git("data/pokemon/dex_order_alpha.asm")
    head = t.split("\tdb ", 1)[0].rstrip("\n").split("\n")
    byname = sorted(L, key=lambda r: r["name"].replace("♀", "\x01").replace("♂", "\x02"))
    write("data/pokemon/dex_order_alpha.asm",
          "\n".join(head + [f"\tdb {r['const']}" for r in byname] + ["\tassert_table_length NUM_POKEMON"]) + "\n")


# ---------------------------------------------------------------------------------------------
# Evolutions and learnsets
# ---------------------------------------------------------------------------------------------
TYPE_MOVES = {
    "NORMAL": ["BODY_SLAM", "SLASH", "TRI_ATTACK", "HYPER_BEAM"],
    "FIGHTING": ["BRICK_BREAK", "SUBMISSION", "CROSS_CHOP", "DRAIN_PUNCH", "FOCUS_BLAST"],
    "FLYING": ["WING_ATTACK", "DRILL_PECK", "BRAVE_BIRD", "HURRICANE"],
    "POISON": ["SLUDGE_BOMB", "POISON_JAB", "GUNK_SHOT", "TOXIC"],
    "GROUND": ["DIG", "EARTHQUAKE", "EARTH_POWER", "MAGNITUDE"],
    "ROCK": ["ROCK_SLIDE", "ANCIENTPOWER", "POWER_GEM", "STONE_EDGE"],
    "BUG": ["TWINEEDLE", "X_SCISSOR", "BUG_BUZZ", "MEGAHORN"],
    "GHOST": ["SHADOW_SNEAK", "SHADOW_CLAW", "SHADOW_BALL", "NIGHT_SHADE"],
    "STEEL": ["METAL_CLAW", "BULLET_PUNCH", "IRON_HEAD", "FLASH_CANNON"],
    "FIRE": ["FIRE_FANG", "FLAMETHROWER", "FLARE_BLITZ", "FIRE_BLAST"],
    "WATER": ["AQUA_JET", "WATERFALL", "AQUA_TAIL", "HYDRO_PUMP"],
    "GRASS": ["RAZOR_LEAF", "GIGA_DRAIN", "ENERGY_BALL", "WOOD_HAMMER"],
    "ELECTRIC": ["THUNDER_FANG", "THUNDERBOLT", "WILD_CHARGE", "THUNDER"],
    "PSYCHIC_TYPE": ["CONFUSION", "ZEN_HEADBUTT", "PSYCHO_CUT", "PSYCHIC_M"],
    "ICE": ["ICE_FANG", "ICE_SHARD", "ICE_BEAM", "BLIZZARD"],
    "DRAGON": ["DRAGONBREATH", "DRAGON_CLAW", "DRAGON_PULSE", "OUTRAGE"],
    "DARK": ["FAINT_ATTACK", "CRUNCH", "NIGHT_SLASH", "DARK_PULSE"],
    "FAIRY": ["FAIRY_WIND", "DRAIN_KISS", "PLAY_ROUGH", "DAZZLE_GLEAM", "MOONBLAST"],
}


def move_table():
    """move constant -> (power, type) from the stage 2 move table in the working tree."""
    t = (ROOT / "data/moves/moves.asm").read_text()
    out = {}
    for m in re.finditer(r"^\tmove (\w+),\s+\w+,\s+(\d+),\s+(\w+)\s*,", t, flags=re.M):
        out[m.group(1)] = (int(m.group(2)), m.group(3))
    return out


def learnset_for(r, L_by_const, MT):
    if r["new"]:
        prev = L_by_const[r["prev"]]
        # early moves of the previous form never matter at level 50+, so they are not copied
        # (the evolutions-and-attacks data has to fit in one bank)
        ls = [(lv, m) for lv, m in prev["learnset"] if lv >= 20]
    else:
        ls = [(lv, GM.REMAP.get(m, m)) for lv, m in r["v"]["learnset"]]
    known = {m for _, m in ls}
    st = r["stage"]
    arrive = {1: 5, 2: 25, 3: 50, 4: 75}[st]
    add = []

    def put(level, move):
        if move not in known:
            known.add(move)
            add.append((level, move))

    # fairy lines learn Fairy Wind and Drain Kiss early
    if "FAIRY" in r["types"]:
        prev_types = L_by_const[r["prev"]]["types"] if r["prev"] else []
        if st == 1 or "FAIRY" not in prev_types:
            if st == 1:
                put(4, "FAIRY_WIND")
                put(9, "DRAIN_KISS")
            else:
                put(arrive, "FAIRY_WIND")
                put(arrive, "DRAIN_KISS")
    # every type a species has needs at least one damaging move of that type
    for t in dict.fromkeys(r["types"]):
        have = any(MT.get(m, (0, ""))[1] == t and MT.get(m, (0, ""))[0] > 0 for m in known)
        if not have:
            for m in TYPE_MOVES[t]:
                if m not in known:
                    put(arrive if st > 1 else 12, m)
                    break
    # new forms learn two fresh moves per type slot at 5-level steps
    if r["new"]:
        levels = [arrive + 0, arrive + 5, arrive + 10, arrive + 15]
        order = []
        for t in dict.fromkeys(r["types"]):
            order.append([m for m in TYPE_MOVES[t] if m not in known])
        picks = []
        i = 0
        while len(picks) < 4 and any(order):
            col = order[i % len(order)]
            if col:
                picks.append(col.pop(0 if st == 3 else min(len(col) - 1, 1)))
            i += 1
        for lv, m in zip(levels, picks):
            put(lv, m)
    ls = ls + add
    seen = set()
    out = []
    for lv, m in sorted(ls, key=lambda x: x[0]):
        if m in seen:
            continue
        seen.add(m)
        out.append((lv, m))
    return out


def gen_evos(L):
    MT = move_table()
    by = {r["const"]: r for r in L}
    # learnsets must be resolved in line order (new forms copy the previous stage)
    for lkey, stages in R.LINES:
        for s in stages:
            c = s[1:] if s.startswith("*") else s
            by[c]["learnset"] = learnset_for(by[c], by, MT)
            for lv, m in by[c]["learnset"]:
                assert m in MT, (c, m)
    t = git("data/pokemon/evos_attacks.asm")
    head = t.split("BulbasaurEvosAttacks:")[0]
    ptr = git("data/pokemon/evos_attacks_pointers.asm")
    pt_head = ptr.split("\tdw ", 1)[0].rstrip("\n").split("\n")
    out_ptr = pt_head[:]
    body = [head.rstrip("\n"), ""]
    for r in L:
        lab = (r["label"] + "EvosAttacks") if r["new"] else r["v"]["evoslabel"]
        out_ptr.append(f"\tdw {lab}")
        body.append(f"{lab}:")
        if r["next"]:
            body.append(f"\tdb EVOLVE_LEVEL, {STAGE_LEVELS[r['stage'] - 1]}, {r['next']}")
        body.append("\tdb 0 ; no more evolutions")
        for lv, m in r["learnset"]:
            body.append(f"\tdb {lv}, {m}")
        body.append("\tdb 0 ; no more level-up moves")
        body.append("")
    out_ptr.append("\tassert_table_length NUM_POKEMON")
    write("data/pokemon/evos_attacks_pointers.asm", "\n".join(out_ptr) + "\n")
    write("data/pokemon/evos_attacks.asm", "\n".join(body))
    # egg moves: pointers only (bodies come from gen_moves)
    t = git("data/pokemon/egg_move_pointers.asm")
    head = t.split("\tdw ", 1)[0].rstrip("\n").split("\n")
    out = head[:]
    for r in L:
        out.append(f"\tdw {r['v']['egglabel']}" if not r["new"] else "\tdw NoEggMoves")
    out.append("\tassert_table_length NUM_POKEMON")
    write("data/pokemon/egg_move_pointers.asm", "\n".join(out) + "\n")


# ---------------------------------------------------------------------------------------------
# footprints
# ---------------------------------------------------------------------------------------------
def gen_footprints(L, vsp):
    t = git("gfx/footprints.asm")
    head = t.split("; 001-008 top halves")[0]
    names = [vsp[r["gfx"]]["slug"] if r["new"] else r["slug"] for r in L]
    # IDs after the last species are blank footprints, 253..256 keep their own files
    names += ["252"] * (252 - NUM_POKEMON) + ["253", "254", "255", "256"]
    assert len(names) == 256, len(names)
    out = [head.rstrip("\n"), ""]
    for g in range(0, 256, 8):
        grp = names[g:g + 8]
        out.append(f"; {g + 1:03d}-{g + 8:03d} top halves")
        for n in grp:
            out.append(f'INCBIN "gfx/footprints/{n}.1bpp", footprint_top')
        out.append(f"; {g + 1:03d}-{g + 8:03d} bottom halves")
        for n in grp:
            out.append(f'INCBIN "gfx/footprints/{n}.1bpp", footprint_bottom')
    out += ["", "\tassert_table_length $100"]
    write("gfx/footprints.asm", "\n".join(out) + "\n")


def gen_gen1_order():
    """Time Capsule index table: keep the 190 Gen 1 slots, trim the Johto tail to the new length."""
    lines = git("data/pokemon/gen1_order.asm").split("\n")
    k = next(i for i, l in enumerate(lines) if "assert_table_length 190" in l)
    tail = [l for l in lines[k + 1:] if l.startswith("\tdb ")]
    out = lines[:k + 1] + tail[:NUM_POKEMON + 1 - 190] + ["\tassert_table_length NUM_POKEMON + 1", ""]
    write("data/pokemon/gen1_order.asm", "\n".join(out))


# ---------------------------------------------------------------------------------------------
# engine patches
# ---------------------------------------------------------------------------------------------
def patch(path, old, new, marker):
    p = ROOT / path
    t = p.read_text()
    if marker in t:
        return
    assert old in t, (path, old[:40])
    p.write_text(t.replace(old, new, 1))


def engine_patches():
    patch("engine/gfx/pic_animation.asm",
          """	ld a, [wPokeAnimSpecies]
	cp JOHTO_POKEMON
	ld b, BANK(FramesPointers)
	ld c, BANK(KantoFrames)
	ld hl, FramesPointers
	jr c, .got_frames
	ld c, BANK(JohtoFrames)
.got_frames""",
          """	; Hardcore Crystal: the bank of each frame set comes from FramesBanks, so a species can
	; reuse the animation frames of any other species.
	ld a, [wPokeAnimSpecies]
	dec a
	ld e, a
	ld d, 0
	ld hl, FramesBanks
	add hl, de
	ld a, BANK(FramesBanks)
	call GetFarByte
	ld c, a
	ld b, BANK(FramesPointers)
	ld hl, FramesPointers
.got_frames""", "FramesBanks")
    for old, new in (("wPokedexCaught:: flag_array NUM_POKEMON", "wPokedexCaught:: flag_array 251 ; Hardcore: layout kept"),
                     ("wPokedexSeen:: flag_array NUM_POKEMON", "wPokedexSeen:: flag_array 251 ; Hardcore: layout kept")):
        patch("ram/wram.asm", old, new, "layout kept")
    patch("engine/menus/intro_menu.asm", "ld b, (NUM_POKEMON + 7) / 8", "ld b, (251 + 7) / 8 ; Hardcore: flag array size kept",
          "flag array size kept")


# ---------------------------------------------------------------------------------------------
def main():
    consts, vsp, S, removed = build()
    global R_gfxdir
    R_gfxdir = {c: vsp[c]["gfxdir"] for c in vsp}
    L = species_by_id(S)
    # new species names must not collide with any other constant
    defined = set()
    for q in list((ROOT / "constants").glob("*.asm")) + list((ROOT / "macros").rglob("*.asm")):
        if q.name == "pokemon_constants.asm":
            continue
        defined |= set(re.findall(r"^\s*(?:const|DEF|shift_const|enum_start)\s+(\w+)", q.read_text(), flags=re.M))
    bad = [r["const"] for r in L if r["new"] and r["const"] in defined]
    if bad:
        raise SystemExit(f"species names collide with existing constants: {bad}")
    gen_constants(L, removed)
    gen_base_stats(L)
    gen_names(L)
    gen_cries(L, vsp)
    gen_icons(L, vsp)
    gen_pointer_tables(L, vsp)
    gen_palettes(L, vsp)
    gen_dex(L)
    gen_evos(L)
    gen_footprints(L, vsp)
    gen_gen1_order()
    engine_patches()
    # remove data files of removed species that nothing includes any more
    for c in removed:
        for p in (f"data/pokemon/base_stats/{vsp[c]['slug']}.asm", f"data/pokemon/dex_entries/{vsp[c]['dexfile']}.asm"):
            q = ROOT / p
            if q.exists() and not any(r["slug"] == vsp[c]["slug"] for r in L):
                q.unlink()
    out = []
    for r in L:
        out.append({"id": r["id"], "const": r["const"], "name": r["name"], "line": r["line"], "stage": r["stage"],
                    "types": r["types"], "stats": r["stats"], "new": r["new"], "gfx": r["gfx"],
                    "learnset": r["learnset"], "next": r["next"]})
    (HERE / "roster/roster_out.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    from collections import Counter
    cnt = Counter()
    for r in L:
        for t in set(r["types"]):
            cnt[t] += 1
    print(f"species {len(L)}, new {sum(1 for r in L if r['new'])}")
    print("types:", dict(sorted(cnt.items(), key=lambda x: -x[1])))
    fin = [sum(r["stats"]) for r in L if r["stage"] == 4]
    print("final BST range", min(fin), max(fin))


if __name__ == "__main__":
    main()
