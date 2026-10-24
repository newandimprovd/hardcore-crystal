"""Builders for lanes (forced-fight corridors), plazas and interiors."""
import os
import random

from .model import ROOT, MapDef, link

FACE = {"UP": "SPRITEMOVEDATA_STANDING_UP", "DOWN": "SPRITEMOVEDATA_STANDING_DOWN",
        "LEFT": "SPRITEMOVEDATA_STANDING_LEFT", "RIGHT": "SPRITEMOVEDATA_STANDING_RIGHT"}


def blk(path):
    return open(os.path.join(ROOT, path), "rb").read()


class Slot:
    """A place where a trainer stands, with the direction it faces and how far it sees."""

    def __init__(self, x, y, face, sight):
        self.x, self.y, self.face, self.sight = x, y, face, sight


def lane(g, name, kit, rng, *, trainers=13, a=3, cw=3, right=3, landmark, music, north="open",
         neck=0, extra_top=0):
    """A vertical corridor. The player enters at the bottom (connection) and leaves at the top
    (connection, or a door block when north == 'door'). Trainers stand in pairs or alone on the channel
    edges so every row of the channel is watched."""
    rows = trainers - trainers // 3
    pairs = trainers - rows
    H = rows + 4 + extra_top
    W = a + cw + right
    m = MapDef(g.key, name, W, H, kit.tileset, "ROUTE", landmark, music, border=kit.extra["border"])
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
    g.add(m)
    m.a, m.cw = a, cw
    m.door = door
    return m, slots


def chain(lower, upper, offset=0):
    """Connect upper to the north of lower."""
    lower.connect("north", upper, offset)
    upper.connect("south", lower, -offset)


def plaza(g, name, kit, rng, *, landmark, music, a=3, cw=3, width=13, height=11, rift=False, houses=1, south="open"):
    """A hub: Pokecenter and Mart on the north wall, an optional rift house, an opening to the north lane
    and an opening to the south lane. Returns the map and a dict of door warps."""
    W, H = width, height
    m = MapDef(g.key, name, W, H, kit.tileset, "TOWN", landmark, music, border=kit.extra["border"])
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
    hs = []
    for i in range(houses):
        hx = x + 2 * i
        m.set(hx, 1, kit.extra["house"][0])
        m.set(hx + 1, 1, kit.extra["house"][1])
        hs.append(m.warp(*kit.door_cell(hx, 1, kit.extra["house"][0])))
    doors["houses"] = hs
    if rift:
        hx = x + 2 * houses
        m.set(hx, 1, kit.extra["house"][0])
        m.set(hx + 1, 1, kit.extra["house"][1])
        doors["rift"] = m.warp(*kit.door_cell(hx, 1, kit.extra["house"][0]))
    g.add(m)
    m.a, m.cw = a, cw
    m.spawn_cell = (kit.door_cell(1, 1, pc[1][0])[0], kit.door_cell(1, 1, pc[1][0])[1] + 1)
    return m, doors


# ------------------------------------------------------------------ interiors

def pokecenter_interior(g, name, outer_warp, landmark, texts):
    m = MapDef(g.key, name, 5, 4, "TILESET_POKECENTER", "INDOOR", landmark, "MUSIC_POKEMON_CENTER", pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/Pokecenter1F.blk"))
    w1, w2 = m.warp(3, 7), m.warp(4, 7)
    outer_warp.dest = w1
    w1.dest = outer_warp
    w2.dest = outer_warp
    m.object_consts = ["NURSE"] + [f"NPC{i}" for i in range(len(texts))]
    m.scripts.append(f"{name}NurseScript:\n\tjumpstd PokecenterNurseScript\n")
    m.obj(3, 1, "SPRITE_NURSE", FACE["DOWN"], f"{name}NurseScript")
    spots = [(2, 3, "SPRITE_FISHER", "UP"), (8, 6, "SPRITE_GENTLEMAN", "UP"), (1, 6, "SPRITE_TEACHER", "RIGHT")]
    for i, t in enumerate(texts):
        x, y, sp, f = spots[i]
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal="PAL_NPC_RED" if i != 1 else "0")
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
    m.obj(1, 3, "SPRITE_CLERK", FACE["RIGHT"], f"{name}ClerkScript")
    spots = [(7, 6, "SPRITE_COOLTRAINER_M", "LEFT"), (2, 5, "SPRITE_YOUNGSTER", "DOWN")]
    for i, t in enumerate(texts):
        x, y, sp, f = spots[i]
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal="PAL_NPC_RED" if i else "0")
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
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal="PAL_NPC_GREEN" if i else "0")
    g.add(m)
    return m


def gatehouse(g, name, lane_door, plaza_door, landmark, music, texts=()):
    """A north-south gate house (rift). The bottom mats lead back to lane_door (the door at the north end
    of the southern segment), the top mats lead to plaza_door (a door on the northern segment)."""
    m = MapDef(g.key, name, 5, 4, "TILESET_GATE", "GATE", landmark, music, pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/NorthSouthGate.blk"))
    t1, t2 = m.warp(4, 0), m.warp(5, 0)
    b1, b2 = m.warp(4, 7), m.warp(5, 7)
    lane_door.dest = b1
    b1.dest = lane_door
    b2.dest = lane_door
    plaza_door.dest = t1
    t1.dest = plaza_door
    t2.dest = plaza_door
    m.object_consts = [f"NPC{i}" for i in range(len(texts))]
    spots = [(0, 4, "SPRITE_OFFICER", "RIGHT"), (6, 4, "SPRITE_YOUNGSTER", "LEFT")]
    for i, t in enumerate(texts):
        x, y, sp, f = spots[i]
        m.scripts.append(f"{name}Npc{i}Script:\n\tjumptextfaceplayer {name}Npc{i}Text\n")
        m.scripts.append(t.emit(f"{name}Npc{i}Text"))
        m.obj(x, y, sp, FACE[f], f"{name}Npc{i}Script", pal="PAL_NPC_RED")
    g.add(m)
    return m
