"""Builders for lanes (forced-fight corridors), plazas and interiors."""
import os
import random

from .model import ROOT, MapDef, link
from .text import emit_text

FACE = {"UP": "SPRITEMOVEDATA_STANDING_UP", "DOWN": "SPRITEMOVEDATA_STANDING_DOWN",
        "LEFT": "SPRITEMOVEDATA_STANDING_LEFT", "RIGHT": "SPRITEMOVEDATA_STANDING_RIGHT"}


def autotile(m, kit, rng):
    """Replace the plain wall blocks of a map by the role that fits their neighbors: building fronts where the street is to
    the south, parapets where it is to the north, side walls east and west, roof fill inside.  Only for area tilesets."""
    auto = kit.extra.get("auto")
    if not auto:
        return
    walls = set(kit.wall)

    def open_(x, y):
        if not (0 <= x < m.w and 0 <= y < m.h):
            return False
        return any(c in ("FLOOR", "TALL_GRASS") for c in kit.coll[m.get(x, y)])

    cells = [(x, y) for y in range(m.h) for x in range(m.w) if m.get(x, y) in walls]
    for x, y in cells:
        if open_(x, y + 1):
            role = "facade"
        elif open_(x + 1, y):
            role = "side_e"
        elif open_(x - 1, y):
            role = "side_w"
        elif open_(x, y - 1):
            role = "roof"
        else:
            role = "mass"
        m.set(x, y, rng.choice(auto[role]))


def blk(path):
    return open(os.path.join(ROOT, path), "rb").read()


class Slot:
    """A place where a trainer stands, with the direction it faces and how far it sees."""

    def __init__(self, x, y, face, sight):
        self.x, self.y, self.face, self.sight = x, y, face, sight


def lane(g, name, kit, rng, *, trainers=13, a=3, cw=3, right=3, landmark, music, north="open",
         neck=0, extra_top=0, gate=None, w=None, pal="PALETTE_DAY"):
    """A vertical corridor. The player enters at the bottom (connection) and leaves at the top
    (connection, or a door block when north == 'door'). Trainers stand in pairs or alone on the channel
    edges so every row of the channel is watched."""
    rows = trainers - trainers // 3
    pairs = trainers - rows
    H = rows + 4 + extra_top
    W = a + cw + right
    m = MapDef(g.key, name, W, H, kit.tileset, "ROUTE", landmark, music, border=kit.extra["border"], pal=pal)
    for y in range(H):
        for x in range(W):
            m.set(x, y, rng.choice(kit.wall))
    for y in range(H):
        for x in range(a, a + cw):
            m.set(x, y, rng.choice(kit.floor))
    if neck:
        for y in range(H - neck, H):
            for x in range(a, a + cw):
                if x != a + cw // 2:
                    m.set(x, y, rng.choice(kit.wall))
    cx0, cx1 = 2 * a, 2 * (a + cw) - 1
    door = None
    if north == "door":
        for x in range(a, a + cw):
            m.set(x, 0, rng.choice(kit.wall))
        dx = a + cw // 2
        m.set(dx, 0, kit.extra["rift"])
        dcell = kit.door_cell(dx, 0, kit.extra["rift"])
        door = m.warp(*dcell)
    if gate:
        assert neck >= 2, "a gate needs a neck"
        gate_objects(m, gate, w, 2 * (a + cw // 2), 2 * (H - neck))
    ys = [2 * H - 6 - 2 * i for i in range(rows)]
    ys = [y for y in ys if y >= 4 + 2 * extra_top]
    assert len(ys) == rows, (name, len(ys), rows)
    pair_rows = set(rng.sample(range(rows), pairs))
    slots = []
    side = 0
    for i, y in enumerate(ys):
        if i in pair_rows:
            slots.append(Slot(cx0, y, "RIGHT", cx1 - cx0))
            slots.append(Slot(cx1, y, "LEFT", cx1 - cx0))
        else:
            if side == 0:
                slots.append(Slot(cx0, y, "RIGHT", cx1 - cx0))
            else:
                slots.append(Slot(cx1, y, "LEFT", cx1 - cx0))
            side ^= 1
    autotile(m, kit, rng)
    g.add(m)
    m.a, m.cw = a, cw
    m.door = door
    return m, slots


# Item gates. kind -> (item, sprite, how, sound, text when the item is missing, text when it is used)
GATES = {
    "tree": ("CHAINSAW", "SPRITE_FRUIT_TREE", "remove",
             "A hedge of city-owned trees fills the road. You would need something with a motor.",
             "<PLAYER> fired up the CHAINSAW! The hedge never saw it coming."),
    "boulder": ("CROWBAR", "SPRITE_BOULDER", "push", "", ""),
    "river": ("JET_SKI", "SPRITE_ROCK", "remove",
              "A brown river cuts the trail. It is too wide to swim and too lively to wade. Something with a motor, maybe.",
              "<PLAYER> dragged out the JET SKI. Nobody asked where it came from. The river parted anyway."),
    "hive": ("BASEBALL_BAT", "SPRITE_FRUIT_TREE", "remove",
             "A tree drips with angry hornets. A solid swing could settle it, if you owned one.",
             "<PLAYER> swung the BASEBALL BAT! The tree came down. So did the hornets. Mostly on the tree."),
    "dark": ("FLASHLIGHT", "SPRITE_ROCK", "remove",
             "Pitch black ahead. Something in there is breathing. Slowly. On purpose.",
             "<PLAYER> switched on the FLASHLIGHT. The breathing stopped. Probably fine."),
    "slab": ("SLEDGEHAMMER", "SPRITE_ROCK", "remove",
             "A slab of cracked rock blocks the way. It seems to want a hammer. It seems to want an argument.",
             "<PLAYER> swung the SLEDGEHAMMER. The slab was in pieces. So was someone's property."),
    "hook": ("GRAPPLE_HOOK", "SPRITE_ROCK", "remove",
             "A sheer wall of sandstone, forty feet of it. A hook on a rope would do nicely.",
             "<PLAYER> threw the GRAPPLE HOOK and hauled up. The cops would be proud, or at least nearby."),
    "rubble": ("SHOVEL", "SPRITE_ROCK", "remove",
               "A heap of fresh dirt fills the way. It looks suspiciously like a grave in a hurry.",
               "<PLAYER> dug it out with the SHOVEL. Nothing in there. Mostly nothing."),
}


def gate_objects(m, kind, w, x, y):
    """Two objects across the two cells of a one-block neck, each needing a key item. The 'push' gate (boulders
    and the CROWBAR) uses the engine's strength puzzle; the others vanish when the item is used. They are the
    first objects of the map, so their constants are GATE0/GATE1 (BOULDER0/BOULDER1 for the push gate)."""
    n = m.name
    item, sprite, how, no_text, use_text = GATES[kind]
    if how == "push":
        m.object_consts = ["BOULDER0", "BOULDER1"]
        for i in range(2):
            m.obj(x + i, y, sprite, "SPRITEMOVEDATA_STRENGTH_BOULDER", f"{n}BoulderScript", pal="PAL_NPC_BROWN")
        m.scripts.append(f"{n}BoulderScript:\n\tjumpstd StrengthBoulderScript\n")
        return
    flag = w.flag(f"EVENT_GEN_{m.const}_GATE")
    m.object_consts = ["GATE0", "GATE1"]
    pal = "PAL_NPC_GREEN" if sprite == "SPRITE_FRUIT_TREE" else "PAL_NPC_BROWN"
    for i in range(2):
        m.obj(x + i, y, sprite, "SPRITEMOVEDATA_STILL", f"{n}GateScript", pal=pal, flag=flag)
    m.scripts.append(
        f"{n}GateScript:\n\tcheckitem {item}\n\tiffalse .Missing\n\topentext\n\twritetext {n}GateUseText\n"
        f"\twaitbutton\n\tclosetext\n\tplaysound SFX_STRENGTH\n\tearthquake 12\n\twaitsfx\n"
        f"\tdisappear {m.const}_GATE0\n\tdisappear {m.const}_GATE1\n\tsetevent {flag}\n\tend\n\n"
        f".Missing:\n\tjumptext {n}GateNoText\n")
    m.scripts.append(emit_text(f"{n}GateNoText", no_text))
    m.scripts.append(emit_text(f"{n}GateUseText", use_text))


def chain(lower, upper, offset=0):
    """Connect upper to the north of lower."""
    lower.connect("north", upper, offset)
    upper.connect("south", lower, -offset)


def grass_patches(m, kit):
    """Wild encounters happen in tall grass: an east and a west patch in the lower half of a plaza, clear of the door row, the
    corridor columns and the south exit.  Uses a random source of its own so the rest of the layout does not change.
    Returns the number of grass blocks (0 for tilesets without grass)."""
    grass = kit.extra.get("grass")
    if not grass:
        return 0
    r = random.Random("grass:" + m.name)
    dense, detail = grass[0], grass[1]
    n = 0
    for (x0, x1) in ((7, m.w - 2), (1, 2)):
        for y in range(4, min(9, m.h - 2)):
            for x in range(x0, x1 + 1):
                corner = x in (x0, x1) and y in (4, 8)
                if corner and r.random() < 0.6:
                    continue
                m.set(x, y, detail if r.random() < 0.08 else dense)
                n += 1
    return n


def plaza(g, name, kit, rng, *, landmark, music, a=3, cw=3, width=13, height=11, rift=False, houses=1, extra=0,
          south="open", pal="PALETTE_DAY"):
    """A hub: Pokecenter and Mart on the north wall, an optional rift house, an opening to the north lane
    and an opening to the south lane. Returns the map and a dict of door warps."""
    W, H = width, height
    m = MapDef(g.key, name, W, H, kit.tileset, "TOWN", landmark, music, border=kit.extra["border"], pal=pal)
    for y in range(H):
        for x in range(W):
            m.set(x, y, rng.choice(kit.wall))
    for y in range(2, H - 1):
        for x in range(1, W - 1):
            m.set(x, y, rng.choice(kit.extra["plaza"]) if (x + y) % 2 == 0 else rng.choice(kit.floor))
    for y in range(H):
        for x in range(a, a + cw):
            m.set(x, y, rng.choice(kit.floor))
    if south != "open":
        for y in (H - 1,):
            for x in range(a, a + cw):
                m.set(x, y, rng.choice(kit.wall))
    # Pokecenter at x=1..2, Mart at x=6..7 (rows 0..1)
    pc, mt = kit.extra["center"], kit.extra["mart"]
    for dy in range(2):
        for dx in range(2):
            m.set(1 + dx, dy, pc[dy][dx])
            m.set(a + cw + dx, dy, mt[dy][dx])
    w_pc = m.warp(*kit.door_cell(1, 1, pc[1][0]))
    w_mt = m.warp(*kit.door_cell(a + cw, 1, mt[1][0]))
    doors = {"center": w_pc, "mart": w_mt}
    x = a + cw + 2
    assert x + 2 * (houses + extra + (1 if rift else 0)) + 1 <= W, (name, "plaza too narrow for its doors")
    hs, ex = [], []
    n = 0
    for lst, count in ((hs, houses), (ex, extra)):
        for i in range(count):
            hx = x + 2 * n
            n += 1
            m.set(hx, 1, kit.extra["house"][0])
            m.set(hx + 1, 1, kit.extra["house"][1])
            if "house_roof" in kit.extra:
                m.set(hx, 0, kit.extra["house_roof"][0])
                m.set(hx + 1, 0, kit.extra["house_roof"][1])
            lst.append(m.warp(*kit.door_cell(hx, 1, kit.extra["house"][0])))
    doors["houses"] = hs
    doors["extra"] = ex
    if rift:
        hx = x + 2 * n
        m.set(hx, 1, kit.extra["house"][0])
        m.set(hx + 1, 1, kit.extra["house"][1])
        if "house_roof" in kit.extra:
            m.set(hx, 0, kit.extra["house_roof"][0])
            m.set(hx + 1, 0, kit.extra["house_roof"][1])
        doors["rift"] = m.warp(*kit.door_cell(hx, 1, kit.extra["house"][0]))
    m.grass = grass_patches(m, kit)
    autotile(m, kit, rng)
    g.add(m)
    m.a, m.cw = a, cw
    m.spawn_cell = (kit.door_cell(1, 1, pc[1][0])[0], kit.door_cell(1, 1, pc[1][0])[1] + 1)
    return m, doors


# ------------------------------------------------------------------ interiors

def hub(g, key, i, default_sprite, default_pal="0"):
    """(sprite, palette) of an interior NPC: the area's own cast (g.hub, set by the area) or the vanilla default."""
    h = getattr(g, "hub", {}).get(key)
    if not h:
        return default_sprite, default_pal
    e = h[i] if isinstance(h, list) else h
    return e


def pokecenter_interior(g, name, outer_warp, landmark, texts):
    m = MapDef(g.key, name, 5, 4, "TILESET_POKECENTER", "INDOOR", landmark, "MUSIC_POKEMON_CENTER", pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/Pokecenter1F.blk"))
    w1, w2 = m.warp(3, 7), m.warp(4, 7)
    outer_warp.dest = w1
    w1.dest = outer_warp
    w2.dest = outer_warp
    m.object_consts = ["NURSE"] + [f"NPC{i}" for i in range(len(texts))]
    m.scripts.append(f"{name}NurseScript:\n\tjumpstd PokecenterNurseScript\n")
    ns, npal = hub(g, "nurse", 0, "SPRITE_NURSE")
    m.obj(3, 1, ns, FACE["DOWN"], f"{name}NurseScript", pal=npal)
    spots = [(2, 3, "SPRITE_FISHER", "UP"), (8, 6, "SPRITE_GENTLEMAN", "UP"), (1, 6, "SPRITE_TEACHER", "RIGHT")]
    for i, t in enumerate(texts):
        x, y, sp, f = spots[i]
        sp, pal = hub(g, "pc", i, sp, "PAL_NPC_RED" if i != 1 else "0")
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal=pal)
    g.add(m)
    return m


def mart_interior(g, name, outer_warp, landmark, mart_const, texts):
    m = MapDef(g.key, name, 6, 4, "TILESET_MART", "INDOOR", landmark, "MUSIC_CHERRYGROVE_CITY", pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/Mart.blk"))
    w1, w2 = m.warp(2, 7), m.warp(3, 7)
    outer_warp.dest = w1
    w1.dest = outer_warp
    w2.dest = outer_warp
    m.object_consts = ["CLERK"] + [f"NPC{i}" for i in range(len(texts))]
    m.scripts.append(f"{name}ClerkScript:\n\topentext\n\tpokemart MARTTYPE_STANDARD, MART_{mart_const}\n\tclosetext\n\tend\n")
    cs, cpal = hub(g, "clerk", 0, "SPRITE_CLERK")
    m.obj(1, 3, cs, FACE["RIGHT"], f"{name}ClerkScript", pal=cpal)
    spots = [(7, 6, "SPRITE_COOLTRAINER_M", "LEFT"), (2, 5, "SPRITE_YOUNGSTER", "DOWN")]
    for i, t in enumerate(texts):
        x, y, sp, f = spots[i]
        sp, pal = hub(g, "mart", i, sp, "PAL_NPC_RED" if i else "0")
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal=pal)
    g.add(m)
    return m


def house_interior(g, name, outer_warp, landmark, texts, music="MUSIC_VIOLET_CITY"):
    m = MapDef(g.key, name, 4, 4, "TILESET_HOUSE", "INDOOR", landmark, music, pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/House1.blk"))
    w1, w2 = m.warp(2, 7), m.warp(3, 7)
    outer_warp.dest = w1
    w1.dest = outer_warp
    w2.dest = outer_warp
    spots = [(2, 3, "SPRITE_POKEFAN_M", "DOWN"), (5, 5, "SPRITE_BUG_CATCHER", "LEFT")]
    m.object_consts = [f"NPC{i}" for i in range(len(texts))]
    for i, t in enumerate(texts):
        x, y, sp, f = spots[i]
        sp, pal = hub(g, "house", i, sp, "PAL_NPC_GREEN" if i else "0")
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal=pal)
    g.add(m)
    return m


def gatehouse(g, name, lane_door, plaza_door, landmark, music, texts=()):
    """A north-south gate house (rift). The bottom mats lead back to lane_door (the door at the north end
    of the southern segment), the top mats lead to plaza_door (a door on the northern segment)."""
    m = MapDef(g.key, name, 5, 4, "TILESET_GATE", "GATE", landmark, music, pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/NorthSouthGate.blk"))
    t1, t2 = m.warp(4, 0), m.warp(5, 0)
    b1, b2 = m.warp(4, 7), m.warp(5, 7)
    lane_doors = lane_door if isinstance(lane_door, (list, tuple)) else [lane_door]
    for d in lane_doors:
        d.dest = b1
    b1.dest = lane_doors[0]
    b2.dest = lane_doors[0]
    plaza_door.dest = t1
    t1.dest = plaza_door
    t2.dest = plaza_door
    m.object_consts = [f"NPC{i}" for i in range(len(texts))]
    spots = [(0, 4, "SPRITE_OFFICER", "RIGHT"), (6, 4, "SPRITE_YOUNGSTER", "LEFT")]
    for i, t in enumerate(texts):
        x, y, sp, f = spots[i]
        sp, pal = hub(g, "gate", i, sp, "PAL_NPC_RED")
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal=pal)
    g.add(m)
    return m


HALL_BLOCKS = [
    0x04, 0x04, 0x17, 0x04, 0x04, 0x04, 0x04, 0x04,
    0x0f, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0f,
    0x03, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x03,
    0x10, 0x02, 0x02, 0x12, 0x12, 0x02, 0x02, 0x10,
    0x03, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x03,
    0x08, 0x08, 0x08, 0x0e, 0x08, 0x08, 0x08, 0x08,
]


def mansion_hall(g, name, boss_exits, landmark, music):
    """The rival's mansion hall (mansion tileset, 8x6 blocks): the exit mat leads back into the boss room, the
    door in the top wall to the bedroom. Returns (map, door warp). NPCs are added by the caller."""
    m = MapDef(g.key, name, 8, 6, "TILESET_MANSION", "INDOOR", landmark, music, pal="PALETTE_DAY")
    m.blocks = bytearray(HALL_BLOCKS)
    mat1, mat2 = m.warp(6, 11), m.warp(7, 11)
    door = m.warp(5, 0)
    boss_exits[0].dest = mat1
    boss_exits[1].dest = mat1
    mat1.dest = boss_exits[0]
    mat2.dest = boss_exits[0]
    g.add(m)
    return m, door


def mansion_bedroom(g, name, hall_door, landmark, music):
    """The bedroom (the player's room blocks of vanilla): the stairs go down to the hall."""
    m = MapDef(g.key, name, 4, 3, "TILESET_PLAYERS_ROOM", "INDOOR", landmark, music, pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/PlayersHouse2F.blk"))
    stairs = m.warp(7, 0)
    stairs.dest = hall_door
    hall_door.dest = stairs
    g.add(m)
    return m


# Boss rooms reuse the Elite Four room blocks of vanilla (same tileset), which already have the funnel shape,
# the mat at the bottom and a door at the top. The boss stands at the left edge of the last wide row, so every
# route from the funnel into the room crosses his line of sight.
BOSS_TEMPLATES = {"karen": ("maps/KarensRoom.blk", 10), "will": ("maps/WillsRoom.blk", 9),
                  "bruno": ("maps/BrunosRoom.blk", 9)}


def boss_room(g, w, name, outer_warp, landmark, music, template, boss, item=None, open_exit=False, story=0):
    """boss: dict(cls, sprite, pal, name, party, seen, beaten, after) with Text objects for the three texts.
    item: key item constant placed on a ball in the room (event flag generated).
    Returns (map, exit_warps); exit_warps is [] unless open_exit (then the two top warps, unlinked)."""
    path, row = BOSS_TEMPLATES[template]
    m = MapDef(g.key, name, 5, 9, "TILESET_ELITE_FOUR_ROOM", "INDOOR", landmark, music, pal="PALETTE_DAY")
    m.blocks = bytearray(blk(path))
    w1, w2 = m.warp(4, 17), m.warp(5, 17)
    outer_warp.dest = w1
    w1.dest = outer_warp
    w2.dest = outer_warp
    exits = []
    if open_exit:
        m.set(2, 1, 0x16)
        exits = [m.warp(4, 2), m.warp(5, 2)]
    tid = w.trainer(boss["cls"], boss["name"], boss["party"])
    if story:
        w.story.append((boss["cls"], tid, story))
    flag = w.flag(f"EVENT_GEN_{m.const}_BOSS")
    n = name
    m.scripts.append(
        f"{n}BossScript:\n\ttrainer {boss['cls']}, {tid}, {flag}, {n}BossSeenText, {n}BossBeatenText, 0, {n}BossAfterScript\n\n"
        f"{n}BossAfterScript:\n\tendifjustbattled\n\topentext\n\twritetext {n}BossAfterText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(boss["seen"].emit(f"{n}BossSeenText"))
    m.scripts.append(boss["beaten"].emit(f"{n}BossBeatenText"))
    m.scripts.append(boss["after"].emit(f"{n}BossAfterText"))
    m.obj(2, row, boss["sprite"], FACE["RIGHT"], f"{n}BossScript", pal=boss["pal"], otype="OBJECTTYPE_TRAINER", sight=5)
    if item:
        iflag = w.flag(f"EVENT_GEN_{m.const}_ITEM")
        m.scripts.append(f"{n}ItemBall:\n\titemball {item}\n")
        m.obj(7, 7, "SPRITE_POKE_BALL", "SPRITEMOVEDATA_STILL", f"{n}ItemBall", otype="OBJECTTYPE_ITEMBALL", flag=iflag)
    g.add(m)
    return m, exits
