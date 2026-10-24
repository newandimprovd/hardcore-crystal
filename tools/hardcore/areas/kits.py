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
