"""Background palettes of the five areas (the vanilla slots are GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF, TEXT).

Every slot is four colors, lightest first: base, light, dark, outline.  Each area has an outdoor set and an indoor set; the engine
(engine/hardcore/area_pals.asm) loads them for every map of the area, whatever the time of day.  Colors are 5-bit RGB."""

K = (3, 3, 8)  # default outline


def S(*cols):
    assert len(cols) == 4
    return tuple(cols)


TEXT = S((31, 31, 16), (31, 31, 16), (14, 9, 0), (0, 0, 0))

AREAS = {
    # TITHE CITY: overcast gothic stone, gold windows, crimson trim
    "AREA1": dict(
        out=[S((11, 13, 19), (21, 23, 29), (6, 7, 12), (1, 1, 5)),        # gray: stone (base = dark slate walls, 1 = street light)
             S((11, 13, 19), (31, 10, 20), (17, 3, 9), (1, 1, 5)),         # red: neon, wine
             S((11, 13, 19), (9, 21, 12), (3, 11, 8), (1, 1, 5)),          # green: moss
             S((11, 13, 19), (11, 21, 31), (3, 7, 21), (1, 1, 5)),         # water: glass, puddles
             S((11, 13, 19), (31, 28, 8), (22, 12, 2), (1, 1, 5)),         # yellow: lit windows, gold
             S((11, 13, 19), (20, 12, 8), (10, 5, 5), (1, 1, 5)),          # brown: wood
             S((11, 13, 19), (15, 17, 28), (8, 9, 18), (1, 1, 5)),         # roof: slate
             TEXT],
        road=[S((22, 24, 29), (15, 17, 24), (9, 10, 17), (3, 3, 8)),        # gray: stone and streets
             S((22, 24, 29), (28, 14, 16), (20, 5, 9), (3, 3, 8)),         # red: trim, carpets
             S((19, 25, 19), (10, 19, 13), (4, 11, 8), (2, 3, 5)),         # green: park
             S((22, 26, 31), (8, 13, 26), (3, 5, 17), (2, 3, 8)),          # water
             S((22, 24, 29), (31, 28, 10), (29, 18, 4), (3, 3, 8)),        # yellow: lit windows
             S((22, 24, 29), (22, 15, 11), (14, 8, 7), (3, 3, 8)),         # brown: wood, rust
             S((22, 24, 29), (11, 13, 22), (6, 7, 15), (3, 3, 8)),         # roof: slate
             TEXT],
        inn=[S((28, 26, 24), (20, 18, 19), (12, 10, 14), (4, 3, 7)),
             S((28, 26, 24), (30, 14, 16), (21, 5, 9), (4, 3, 7)),
             S((22, 26, 18), (12, 20, 12), (5, 12, 7), (3, 3, 5)),
             S((28, 28, 30), (10, 14, 28), (4, 6, 18), (3, 3, 8)),
             S((28, 26, 24), (31, 29, 9), (30, 19, 3), (4, 3, 7)),
             S((27, 23, 19), (23, 15, 9), (15, 8, 5), (4, 3, 7)),
             S((28, 26, 24), (13, 14, 24), (7, 8, 16), (4, 3, 7)),
             TEXT]),
    # THE COMMUNE (Grove): warm earth, living green, thatch
    "AREA2": dict(
        out=[S((22, 17, 10), (28, 23, 15), (15, 10, 6), (3, 2, 1)),       # gray: packed earth, clay, fieldstone
             S((22, 17, 10), (31, 9, 9), (19, 2, 5), (3, 2, 1)),            # red: paint, mushrooms, coals
             S((22, 17, 10), (14, 26, 8), (5, 15, 5), (2, 6, 2)),           # green: grass, ferns on the ground
             S((22, 17, 10), (13, 23, 30), (4, 10, 21), (3, 2, 1)),         # water: puddles, glass
             S((22, 17, 10), (31, 27, 10), (24, 15, 3), (3, 2, 1)),         # yellow: thatch, lantern light
             S((22, 17, 10), (24, 16, 8), (12, 6, 3), (3, 2, 1)),           # brown: timber
             S((8, 19, 6), (17, 27, 8), (3, 11, 4), (1, 4, 2)),             # roof: forest canopy
             TEXT],
        road=[S((27, 28, 22), (20, 20, 15), (12, 12, 9), (4, 3, 2)),
             S((27, 28, 22), (31, 17, 14), (24, 7, 6), (4, 3, 2)),
             S((22, 30, 12), (12, 24, 4), (4, 13, 2), (2, 4, 1)),
             S((24, 30, 31), (9, 20, 29), (3, 10, 23), (2, 4, 10)),
             S((27, 28, 22), (31, 29, 10), (30, 18, 3), (4, 3, 2)),
             S((27, 25, 18), (24, 17, 8), (16, 10, 4), (4, 3, 2)),
             S((27, 25, 18), (27, 21, 8), (19, 13, 4), (4, 3, 2)),
             TEXT],
        inn=[S((29, 27, 21), (22, 19, 13), (14, 11, 8), (5, 3, 2)),
             S((29, 27, 21), (31, 17, 14), (24, 7, 6), (5, 3, 2)),
             S((24, 29, 14), (14, 23, 6), (6, 13, 3), (3, 4, 2)),
             S((26, 30, 29), (10, 19, 28), (4, 10, 22), (3, 4, 10)),
             S((29, 27, 21), (31, 29, 10), (30, 18, 3), (5, 3, 2)),
             S((28, 24, 16), (25, 17, 8), (17, 10, 4), (5, 3, 2)),
             S((28, 24, 16), (27, 21, 8), (19, 13, 4), (5, 3, 2)),
             TEXT]),
    # THE UNION (Axiom): fluorescent steel and teal, alarm red
    "AREA3": dict(
        out=[S((10, 14, 17), (22, 28, 30), (5, 7, 10), (1, 2, 4)),        # gray: steel
             S((10, 14, 17), (31, 8, 9), (18, 1, 4), (1, 2, 4)),            # red: alarm
             S((10, 14, 17), (8, 28, 16), (2, 14, 9), (1, 2, 4)),           # green: terminal
             S((10, 14, 17), (8, 26, 31), (2, 12, 22), (1, 2, 4)),          # water: screens, glass
             S((10, 14, 17), (31, 30, 6), (27, 18, 0), (1, 2, 4)),          # yellow: hazard, lamps
             S((10, 14, 17), (22, 15, 10), (11, 7, 6), (1, 2, 4)),          # brown: rust, pipes
             S((10, 14, 17), (17, 22, 26), (7, 11, 16), (1, 2, 4)),         # roof: hull plates
             TEXT],
        road=[S((24, 30, 30), (16, 23, 25), (8, 13, 17), (1, 3, 5)),
             S((24, 30, 30), (31, 8, 10), (20, 1, 5), (1, 3, 5)),
             S((22, 31, 24), (6, 24, 16), (2, 12, 10), (1, 3, 5)),
             S((22, 30, 31), (4, 18, 28), (1, 8, 20), (1, 3, 8)),
             S((24, 30, 30), (31, 31, 6), (28, 20, 0), (1, 3, 5)),
             S((24, 28, 28), (22, 18, 14), (14, 10, 8), (1, 3, 5)),
             S((24, 30, 30), (10, 18, 22), (4, 10, 14), (1, 3, 5)),
             TEXT],
        inn=[S((27, 31, 31), (18, 25, 27), (9, 14, 19), (2, 4, 7)),
             S((27, 31, 31), (31, 9, 11), (20, 2, 6), (2, 4, 7)),
             S((24, 31, 26), (8, 25, 17), (3, 13, 11), (2, 4, 7)),
             S((24, 31, 31), (6, 19, 29), (2, 9, 21), (2, 4, 9)),
             S((27, 31, 31), (31, 31, 7), (28, 20, 1), (2, 4, 7)),
             S((26, 29, 29), (23, 18, 14), (14, 10, 8), (2, 4, 7)),
             S((27, 31, 31), (12, 20, 24), (5, 11, 15), (2, 4, 7)),
             TEXT]),
    # THE LOTUS COAST: pastel resort, turquoise water, coral roofs
    "AREA4": dict(
        out=[S((30, 28, 24), (23, 20, 19), (16, 13, 15), (5, 3, 7)),      # gray: stucco, sand, grout
             S((30, 28, 24), (31, 15, 18), (24, 5, 10), (5, 3, 7)),         # red: coral, awnings
             S((30, 28, 24), (10, 26, 8), (3, 14, 6), (2, 6, 4)),           # green: palms
             S((30, 28, 24), (6, 26, 31), (2, 13, 27), (2, 5, 14)),         # water: pool, sea
             S((30, 28, 24), (31, 28, 7), (30, 18, 2), (5, 3, 7)),          # yellow: sun, lamps
             S((30, 28, 24), (26, 19, 11), (17, 10, 5), (5, 3, 7)),         # brown: shutters, wood
             S((28, 14, 12), (31, 22, 17), (22, 9, 8), (5, 3, 7)),          # roof: terracotta
             TEXT],
        road=[S((31, 30, 27), (25, 24, 24), (17, 16, 19), (6, 5, 9)),
             S((31, 30, 27), (31, 16, 20), (26, 6, 12), (6, 5, 9)),
             S((24, 31, 14), (10, 26, 8), (3, 15, 5), (2, 6, 3)),
             S((26, 31, 31), (6, 24, 30), (2, 12, 26), (2, 6, 14)),
             S((31, 30, 27), (31, 28, 8), (31, 20, 3), (6, 5, 9)),
             S((31, 30, 25), (29, 22, 12), (21, 13, 6), (6, 5, 9)),
             S((31, 30, 27), (31, 17, 20), (26, 8, 13), (6, 5, 9)),
             TEXT],
        inn=[S((31, 30, 28), (26, 25, 24), (18, 17, 19), (7, 6, 9)),
             S((31, 30, 28), (31, 17, 21), (26, 7, 12), (7, 6, 9)),
             S((25, 31, 16), (11, 26, 9), (4, 15, 6), (3, 6, 3)),
             S((27, 31, 31), (8, 25, 30), (3, 13, 26), (3, 6, 14)),
             S((31, 30, 28), (31, 28, 8), (31, 20, 3), (7, 6, 9)),
             S((31, 29, 24), (29, 21, 12), (21, 13, 6), (7, 6, 9)),
             S((31, 30, 28), (31, 18, 21), (26, 9, 14), (7, 6, 9)),
             TEXT]),
    # DIS: black basalt, ember light, bone, the frozen lake
    "AREA5": dict(
        out=[S((10, 6, 9), (21, 14, 15), (4, 2, 5), (0, 0, 1)),           # gray: basalt, ash
             S((10, 6, 9), (31, 20, 3), (26, 5, 2), (0, 0, 1)),             # red: lava, embers
             S((10, 6, 9), (14, 17, 9), (6, 8, 5), (0, 0, 1)),              # green: dead moss, ash trees
             S((10, 6, 9), (24, 30, 31), (9, 18, 28), (2, 4, 12)),          # water: ice
             S((10, 6, 9), (31, 29, 9), (30, 15, 2), (0, 0, 1)),            # yellow: flame
             S((10, 6, 9), (28, 25, 20), (17, 13, 10), (0, 0, 1)),          # brown: bone
             S((7, 4, 8), (14, 8, 13), (3, 1, 4), (0, 0, 1)),               # roof: obsidian
             TEXT],
        road=[S((15, 10, 12), (10, 6, 9), (6, 3, 6), (1, 0, 2)),
             S((20, 9, 6), (31, 17, 3), (27, 6, 2), (1, 0, 2)),
             S((14, 14, 9), (9, 12, 7), (4, 7, 4), (1, 1, 1)),
             S((27, 31, 31), (14, 23, 30), (6, 13, 26), (2, 3, 12)),
             S((18, 10, 7), (31, 28, 8), (31, 14, 2), (1, 0, 2)),
             S((25, 21, 17), (19, 14, 10), (10, 6, 5), (1, 0, 2)),
             S((15, 10, 12), (11, 4, 7), (6, 2, 5), (1, 0, 2)),
             TEXT],
        inn=[S((19, 13, 14), (12, 7, 10), (7, 3, 7), (1, 0, 2)),
             S((22, 10, 7), (31, 18, 4), (27, 7, 3), (1, 0, 2)),
             S((16, 15, 10), (10, 13, 8), (5, 8, 5), (1, 1, 1)),
             S((27, 31, 31), (14, 23, 30), (6, 13, 26), (2, 3, 12)),
             S((20, 11, 8), (31, 28, 8), (31, 15, 2), (1, 0, 2)),
             S((27, 23, 18), (20, 15, 10), (11, 7, 5), (1, 0, 2)),
             S((19, 13, 14), (12, 5, 8), (7, 2, 5), (1, 0, 2)),
             TEXT]),
}

ORDER = ["AREA1", "AREA2", "AREA3", "AREA4", "AREA5"]


def outset(area):
    return AREAS[area].get("out", AREAS[area]["road"])


def roof_colors(area):
    """Colors 1 and 2 of the roof slot, as the RGB triples the roof palette table wants (day and nite are the same)."""
    c = outset(area)[6]
    t = (*c[1], *c[2])
    return t, t


def rgb(c):
    return f"{c[0]:02d},{c[1]:02d},{c[2]:02d}"


SLOTS = ["gray", "red", "green", "water", "yellow", "brown", "roof", "text"]


def emit(path):
    o = ["; Generated by tools/hardcore/art/areapal.py. Do not edit by hand.",
         "; per area: outdoor set, then indoor set; 8 palettes each (see PAL_BG_* constants)\n"]
    for a in ORDER:
        for kind in ("out", "road", "inn"):
            o.append(f"; {a} {kind}")
            for name, p in zip(SLOTS, outset(a) if kind == "out" else AREAS[a][kind]):
                o.append("\tRGB " + ", ".join(rgb(c) for c in p) + f" ; {name}")
            o.append("")
    open(path, "w").write("\n".join(o))


# ---------------------------------------------------------------------------------------------------- NPC (object) palettes
# The overworld object palettes (PAL_NPC_*): slot 0 (red) is the player's and stays vanilla everywhere, as do emote, tree and rock.
# Slots BLUE, GREEN, BROWN and PINK are the area's own colorways.  Each palette is: unused/transparent, skin, cloth, dark.
# Sprites follow the convention 1 skin, 2 cloth, 3 dark (art/npcs.py), so a colorway sets the cloth and may recolor the skin
# (robots are steel, imps are red).  Always the day set: the area maps ignore the time of day.
VANILLA_NPC = [
    S((27, 31, 27), (31, 19, 10), (31, 7, 1), (0, 0, 0)),      # red (the player)
    S((27, 31, 27), (31, 19, 10), (10, 9, 31), (0, 0, 0)),     # blue
    S((27, 31, 27), (31, 19, 10), (7, 23, 3), (0, 0, 0)),      # green
    S((27, 31, 27), (31, 19, 10), (15, 10, 3), (0, 0, 0)),     # brown
    S((27, 31, 27), (31, 19, 10), (30, 10, 6), (0, 0, 0)),     # pink
    S((31, 31, 31), (31, 31, 31), (13, 13, 13), (0, 0, 0)),    # silver (emotes)
    S((22, 31, 10), (12, 25, 1), (5, 14, 0), (7, 7, 7)),       # tree
    S((27, 31, 27), (24, 18, 7), (20, 15, 3), (7, 7, 7)),      # rock
]
SKIN = (31, 19, 10)
NPC = {
    # TITHE CITY: cop navy, soot-brown coats and cassocks, olive street rags, violet choir robes
    "AREA1": dict(BLUE=S((27, 31, 27), SKIN, (6, 9, 21), (1, 1, 5)),
                  GREEN=S((27, 31, 27), SKIN, (12, 15, 8), (2, 3, 2)),
                  BROWN=S((27, 31, 27), SKIN, (11, 8, 8), (2, 1, 1)),
                  PINK=S((27, 31, 27), SKIN, (21, 9, 20), (3, 1, 4))),
    # THE COMMUNE: river-blue linen, leaf green, hemp, tie-dye magenta
    "AREA2": dict(BLUE=S((27, 31, 27), SKIN, (7, 16, 28), (1, 3, 8)),
                  GREEN=S((27, 31, 27), SKIN, (6, 22, 7), (1, 6, 2)),
                  BROWN=S((27, 31, 27), SKIN, (21, 14, 6), (4, 2, 0)),
                  PINK=S((27, 31, 27), SKIN, (29, 8, 21), (5, 1, 4))),
    # THE UNION: bots have steel skin; serfs wear gray-green; executives rust; doctors white coats
    "AREA3": dict(BLUE=S((27, 31, 27), (19, 23, 28), (7, 13, 24), (0, 1, 6)),
                  GREEN=S((27, 31, 27), SKIN, (14, 18, 14), (2, 3, 2)),
                  BROWN=S((27, 31, 27), (24, 17, 9), (17, 8, 3), (3, 1, 0)),
                  PINK=S((27, 31, 27), SKIN, (29, 29, 31), (6, 6, 12))),
    # LOTUS COAST: aqua swimwear, mint linen, tan canvas, coral aloha
    "AREA4": dict(BLUE=S((27, 31, 27), SKIN, (3, 19, 29), (0, 4, 9)),
                  GREEN=S((27, 31, 27), SKIN, (9, 25, 16), (1, 7, 3)),
                  BROWN=S((27, 31, 27), SKIN, (27, 20, 10), (6, 3, 1)),
                  PINK=S((27, 31, 27), SKIN, (31, 12, 14), (7, 1, 3))),
    # DIS: imps are red-skinned, shades violet, the damned bone-pale, embers orange
    "AREA5": dict(BLUE=S((27, 31, 27), (27, 8, 6), (13, 2, 5), (3, 0, 1)),
                  GREEN=S((27, 31, 27), (14, 8, 23), (7, 3, 12), (1, 0, 3)),
                  BROWN=S((27, 31, 27), (29, 28, 23), (14, 12, 11), (2, 1, 1)),
                  PINK=S((27, 31, 27), SKIN, (30, 14, 3), (6, 2, 0))),
}


def npc_set(area):
    pals = list(VANILLA_NPC)
    for i, name in enumerate(("BLUE", "GREEN", "BROWN", "PINK"), start=1):
        pals[i] = NPC[area][name]
    return pals


def emit_npc(path):
    o = ["; Generated by tools/hardcore/art/areapal.py. Do not edit by hand.",
         "; per area: the 8 object palettes (see PAL_OW_* constants), day colors\n"]
    names = ["red", "blue", "green", "brown", "pink", "silver", "tree", "rock"]
    for a in ORDER:
        o.append(f"; {a}")
        for name, p in zip(names, npc_set(a)):
            o.append("\tRGB " + ", ".join(rgb(c) for c in p) + f" ; {name}")
        o.append("")
    open(path, "w").write("\n".join(o))
