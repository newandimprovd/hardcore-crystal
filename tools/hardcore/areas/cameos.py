"""The people around the duels: the Kabbalist mafia and the Yakuza (Area 1), Satoshi (Area 2) and the Amphitheater (Area 2), built
after the areas.  The historic characters who fight (Steiner, Crowley, Sabbah, Cioran, the philosophers) are placed by named.py.
Everything here only adds objects, scripts and a map to groups the area builders have finished."""
from . import cast_text as C
from . import named
from .flags import flag_once
from .kits import grove
from .layout import FACE
from .model import MapDef
from .people import lore_npc, plain_npc
from .text import Text

def free_cells(m):
    taken = {(o["x"], o["y"]) for o in m.objects}
    return [c for c in m.npc_cells if c not in taken]


def spot(m, k=0):
    """A free floor cell of the plaza for a named character (the plaza keeps its free cells in a seeded random order, from the end)."""
    return free_cells(m)[-1 - k]


def cluster(m, offsets):
    """A cell c such that c and c + every offset are free floor cells (a little scene: a man and the crowd around him)."""
    free = set(free_cells(m))
    for c in reversed(free_cells(m)):
        if all((c[0] + dx, c[1] + dy) in free for dx, dy in offsets):
            return c
    raise AssertionError(f"{m.name}: no free place for a scene")


def find(g, name):
    for m in g.maps:
        if m.name == name:
            return m
    raise KeyError(name)


def add_sprite(g, *names):
    for n in names:
        if n not in g.sprites:
            g.sprites.append(n)


def area1(w, g):
    """The Kabbalist mafia and the Yakuza sit in two house interiors (a third person in each room): the story of the jewel beetle."""
    flag_once(w, "EVENT_LORE_BEETLE")
    h4 = find(g, "TitheHouse4")
    lore_npc(w, h4, 5, 2, "SPRITE_HC_SUIT", "PAL_NPC_BROWN", "DOWN", "TitheHouse4MafiaScript", C.KAB_MAFIA, flag="EVENT_LORE_BEETLE")
    h6 = find(g, "TitheHouse6")
    plain_npc(h6, 5, 2, "SPRITE_HC_THUG", "PAL_NPC_RED", "DOWN", "TitheHouse6YakuzaScript", C.YAKUZA)


def area2(w, g, rng, roster):
    h4 = find(g, "GroveHouse4")
    lore_npc(w, h4, 5, 2, "SPRITE_HC_KID_M", "PAL_NPC_GREEN", "DOWN", "GroveHouse4SatoshiScript", C.SATOSHI, flag="EVENT_LORE_SATOSHI")
    amphitheater(w, g, rng, roster)


AMPH_WOMEN = [
    "The jars are for later. Do not touch the jars. The jars have been touched enough.",
    "He is very dedicated. It is almost moving. In the way a fire alarm is moving.",
    "We vote on everything here. We voted yes on this. It was unanimous. Mostly.",
    "My husband is in the other circle. He is also very happy. We compare notes at breakfast.",
    "I came for the foraging. I stayed for the ceremony. The foraging is not as good.",
    "Do not worry about the towel. The towel is a technicality. Bring it anyway.",
]


def amphitheater(w, g, rng, roster):
    """Replaces the second house of the first Commune plaza by the Amphitheater: Crowley, six women and the scene."""
    house = find(g, "GroveHouse2b")
    outer = house.warps[0].dest  # the door in the plaza
    g.maps.remove(house)
    kit = grove()
    add_sprite(g, "SPRITE_HC_CROWLEY", "SPRITE_HC_HIPPIE_F", "SPRITE_HC_BATHER_F", "SPRITE_HC_ELDER_F")
    m = MapDef(g.key, "GroveAmphitheater", 9, 9, kit.tileset, "TOWN", "LANDMARK_GROVE_COMMUNE", "MUSIC_ROUTE_36",
               border=kit.extra["border"])
    for y in range(9):
        for x in range(9):
            m.set(x, y, rng.choice(kit.wall))
    for y in range(1, 8):
        for x in range(1, 8):
            if abs(x - 4) + abs(y - 4) <= 5:
                m.set(x, y, rng.choice(kit.floor))
    for y in range(3, 6):
        for x in range(3, 6):
            m.set(x, y, kit.extra["plaza"][-1])
    m.set(4, 7, rng.choice(kit.floor))
    m.set(4, 8, kit.extra["scn"]["mat"])  # a doormat: stepping on a door tile on the last row would walk the player off the map
    door = m.warp(8, 17)
    outer.dest = door
    door.dest = outer
    flag_once(w, "EVENT_AMPH_DONE")
    flag_once(w, "EVENT_LORE_AMPH")
    m.scripts.append(
        "GroveAmphitheaterSceneScript:\n\tcheckevent EVENT_AMPH_DONE\n\tiftrue .Skip\n\topentext\n"
        "\twritetext GroveAmphitheaterSceneText1\n\twaitbutton\n\tclosetext\n\tspecial FadeOutToBlack\n\tpause 80\n"
        "\tspecial FadeInFromBlack\n\topentext\n\twritetext GroveAmphitheaterSceneText2\n\twaitbutton\n\tclosetext\n"
        "\tsetevent EVENT_AMPH_DONE\n.Skip:\n\tend\n")
    m.scripts.append(Text(C.AMPH_1).emit("GroveAmphitheaterSceneText1"))
    m.scripts.append(Text(C.AMPH_2).emit("GroveAmphitheaterSceneText2"))
    m.coords.append((door.x, door.y - 2, -1, "GroveAmphitheaterSceneScript"))
    g.add(m)
    named.add_one(w, g, "AMPH", roster, m)  # Crowley himself: the duel that hands over the jet ski
    women = [(3, 6, "SPRITE_HC_HIPPIE_F", "PAL_NPC_PINK", "RIGHT"), (3, 9, "SPRITE_HC_BATHER_F", "PAL_NPC_BLUE", "RIGHT"),
             (3, 12, "SPRITE_HC_ELDER_F", "PAL_NPC_GREEN", "RIGHT"), (14, 6, "SPRITE_HC_BATHER_F", "PAL_NPC_PINK", "LEFT"),
             (14, 9, "SPRITE_HC_HIPPIE_F", "PAL_NPC_GREEN", "LEFT"), (14, 12, "SPRITE_HC_ELDER_F", "PAL_NPC_RED", "LEFT")]
    for i, (x, y, sp, pal, face) in enumerate(women):
        plain_npc(m, x, y, sp, pal, face, f"GroveAmphitheaterWoman{i}Script", AMPH_WOMEN[i])
    m.a, m.cw = 3, 3
    return m
