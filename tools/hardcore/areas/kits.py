"""Block kits: which block ids of a tileset are floor, wall, doors and buildings.

Kits are checked against the tileset collision tables so a wrong id fails the generator,
not the game."""
import os
import re

from .model import ROOT

STEM = {
    "TILESET_JOHTO": "johto", "TILESET_JOHTO_MODERN": "johto_modern", "TILESET_KANTO": "kanto",
    "TILESET_FACILITY": "facility", "TILESET_CAVE": "cave", "TILESET_FOREST": "forest",
    "TILESET_MANSION": "mansion", "TILESET_PARK": "park", "TILESET_ICE_PATH": "ice_path",
    "TILESET_DARK_CAVE": "dark_cave", "TILESET_UNDERGROUND": "underground", "TILESET_HOUSE": "house",
    "TILESET_POKECENTER": "pokecenter", "TILESET_MART": "mart", "TILESET_PORT": "port",
    "TILESET_LAB": "lab", "TILESET_TOWER": "tower", "TILESET_RUINS_OF_ALPH": "ruins_of_alph",
    "TILESET_BATTLE_TOWER_OUTSIDE": "battle_tower_outside", "TILESET_RADIO_TOWER": "radio_tower",
    "TILESET_TITHE": "tithe", "TILESET_GROVE": "grove", "TILESET_AXIOM": "axiom", "TILESET_LOTUS": "lotus", "TILESET_DIS": "dis",
}

WALKABLE = {"FLOOR", "TALL_GRASS"}
DOORISH = {"DOOR", "STAIRCASE", "CAVE", "WARP_PANEL", "LADDER"}


def load_collision(stem):
    out = []
    for l in open(os.path.join(ROOT, f"data/tilesets/{stem}_collision.asm")):
        m = re.match(r"\s*tilecoll\s+(.*?)\s*;", l)
        if m:
            out.append(tuple(x.strip() for x in m[1].split(",")))
    return out


class Kit:
    def __init__(self, tileset, floor, wall, **extra):
        self.tileset = tileset
        self.coll = load_collision(STEM[tileset])
        self.floor = list(floor)
        self.wall = list(wall)
        self.extra = extra
        for b in self.floor:
            assert all(c in WALKABLE for c in self.coll[b]), f"{tileset} floor {b:02x} {self.coll[b]}"
        for b in self.wall:
            assert all(c == "WALL" for c in self.coll[b]), f"{tileset} wall {b:02x} {self.coll[b]}"

    def door_quadrant(self, b):
        """(qx, qy) of the quadrant holding a door-type collision, or None. Quadrants: 0 TL,1 TR,2 BL,3 BR."""
        for i, c in enumerate(self.coll[b]):
            if c in DOORISH:
                return (i % 2, i // 2)
        return None

    def door_cell(self, bx, by, b):
        q = self.door_quadrant(b)
        assert q is not None, f"{self.tileset} block {b:02x} has no door"
        return (2 * bx + q[0], 2 * by + q[1])

    def check_door(self, b):
        self.door_quadrant(b)
        return b


def modern():
    return Kit("TILESET_JOHTO_MODERN",
               floor=[0x01, 0x07],
               wall=[0x20, 0x23, 0x27, 0x28, 0x2b, 0x2c, 0x21, 0x22, 0x25, 0x26, 0x29, 0x2a],
               plaza=[0x06], grass=[0x02], flowers=[0x04],
               center=[[0x18, 0x19], [0x1a, 0x1b]], mart=[[0x18, 0x19], [0x1a, 0x33]],
               house=[0x14, 0x15], rift=0x2d, border=0x23)


def johto():
    return Kit("TILESET_JOHTO",
               floor=[0x01, 0x02],
               wall=[0x05],
               plaza=[0x01], grass=[0x02], flowers=[0x04],
               center=[[0x18, 0x19], [0x1a, 0x1b]], mart=[[0x18, 0x19], [0x1a, 0x17]],
               house=[0x14, 0x15], rift=0x14, border=0x05)


def kanto():
    """Brick Kanto city blocks: roofs 0x20/0x21 over the door blocks 0x7c (door) and 0x7e or 0x73 (Mart sign)."""
    return Kit("TILESET_KANTO",
               floor=[0x31, 0x01],
               wall=[0x20, 0x21, 0x13, 0x54, 0x37, 0x68, 0x69],
               plaza=[0x55], grass=[0x0a], flowers=[0x0a],
               center=[[0x20, 0x21], [0x7c, 0x7e]], mart=[[0x20, 0x21], [0x7c, 0x73]],
               house=[0x7c, 0x7e], house_roof=[0x20, 0x21], rift=0x7c, border=0x0f)


def _art_kit(tileset, mod, weights):
    """Kit for a generated area tileset: ids come from art/<area>.py (roles), see gen_tilesets.py."""
    t = mod.build()
    r, ids = t.roles, t.ids
    floor = []
    for role, wt in weights["floor"]:
        for b in r[role]:
            floor += [b] * wt
    auto = {k: [b for role, wt in v for b in r[role] for _ in range(wt)] for k, v in mod.AUTO.items()}
    # weighted facades: repeat the entries listed in mod.FACADE_WEIGHTS (index into the facade role)
    if hasattr(mod, "FACADE_WEIGHTS"):
        fac = r["facade"]
        auto["facade"] = [fac[i] for i, wt in enumerate(mod.FACADE_WEIGHTS) for _ in range(wt)]
    plaza = [b for b in r["plaza"][:1] for _ in range(1)] + [b for b in r["plaza"][1:] for _ in range(3)]
    return Kit(tileset, floor=floor, wall=auto["mass"] + auto["facade"],
               plaza=plaza, center=[[ids["cr_l"], ids["cr_r"]], [ids["c_door"], ids["c_sign"]]],
               mart=[[ids["cr_l"], ids["cr_r"]], [ids["m_door"], ids["m_sign"]]],
               house=[ids["h_door"], ids["h_side"]], house_roof=[ids["hr_l"], ids["hr_r"]], rift=ids["rift"],
               border=ids["border"], auto=auto, grass=r["grass"])


def tithe():
    from art import tithe as mod
    return _art_kit("TILESET_TITHE", mod, dict(floor=[("floor", 4), ("floor_rare", 1)]))


def grove():
    from art import grove as mod
    return _art_kit("TILESET_GROVE", mod, dict(floor=[("floor", 8), ("floor_rare", 1)]))


def axiom():
    from art import axiom as mod
    return _art_kit("TILESET_AXIOM", mod, dict(floor=[("floor", 8), ("floor_rare", 1)]))


def lotus():
    from art import lotus as mod
    return _art_kit("TILESET_LOTUS", mod, dict(floor=[("floor", 8), ("floor_rare", 1)]))


def dis():
    from art import disart as mod
    return _art_kit("TILESET_DIS", mod, dict(floor=[("floor", 8), ("floor_rare", 1)]))
