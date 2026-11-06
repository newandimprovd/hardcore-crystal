"""The historic characters placed into the four areas after they are built: Steiner (A1, A2, A4), the Crowley chase and the Kabbalist
mafia (A1), the Yakuza (A1), the Amphitheater and Satoshi (A2), Sabbah (A3), Cioran (A4).  Everything here only adds objects, scripts and
a map to groups the area builders have finished."""
from . import cast_text as C
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


def steiner(w, g, plaza, text, label):
    add_sprite(g, "SPRITE_HC_STEINER")
    m = find(g, plaza)
    x, y = spot(m)
    lore_npc(w, m, x, y, "SPRITE_HC_STEINER", "PAL_NPC_BROWN", "LEFT", label, text, flag="EVENT_LORE_STEINER")


def area1(w, g):
    add_sprite(g, "SPRITE_HC_CROWLEY", "SPRITE_HC_STEINER")
    steiner(w, g, "TithePlaza1", C.STEINER_1, "TithePlaza1SteinerScript")
    # the chase: Crowley caught at the east side of the first mid-city plaza, three residents screaming at him
    m = find(g, "TithePlaza2")
    crowd_at = [(-3, -1, "SPRITE_HC_SUIT", "PAL_NPC_BROWN", C.CROWD_1), (-3, 1, "SPRITE_HC_HOODIE", "PAL_NPC_GREEN", C.CROWD_2),
                (-2, 0, "SPRITE_HC_COP", "PAL_NPC_BLUE", C.CROWD_3)]
    cx, cy = cluster(m, [(dx, dy) for dx, dy, *_ in crowd_at])
    lore_npc(w, m, cx, cy, "SPRITE_HC_CROWLEY", "PAL_NPC_BROWN", "LEFT", "TithePlaza2CrowleyScript", C.CROWLEY_1,
             again=C.CROWLEY_1_AGAIN, flag="EVENT_LORE_CROWLEY")
    for i, (dx, dy, sp, pal, t) in enumerate(crowd_at):
        plain_npc(m, cx + dx, cy + dy, sp, pal, "RIGHT", f"TithePlaza2Crowd{i}Script", t)
    # the Kabbalist mafia and the Yakuza sit in two house interiors (a third person in each room)
    flag_once(w, "EVENT_LORE_BEES")
    h4 = find(g, "TitheHouse4")
    lore_npc(w, h4, 5, 2, "SPRITE_HC_SUIT", "PAL_NPC_BROWN", "DOWN", "TitheHouse4MafiaScript", C.KAB_MAFIA, flag="EVENT_LORE_BEES")
    h6 = find(g, "TitheHouse6")
    plain_npc(h6, 5, 2, "SPRITE_HC_THUG", "PAL_NPC_RED", "DOWN", "TitheHouse6YakuzaScript", C.YAKUZA)


def area2(w, g, rng):
    add_sprite(g, "SPRITE_HC_CROWLEY", "SPRITE_HC_STEINER")
    steiner(w, g, "GrovePlaza4", C.STEINER_2, "GrovePlaza4SteinerScript")
    h4 = find(g, "GroveHouse4")
    plain_npc(h4, 5, 2, "SPRITE_HC_KID_M", "PAL_NPC_GREEN", "DOWN", "GroveHouse4SatoshiScript", C.SATOSHI)
    amphitheater(w, g, rng)


AMPH_WOMEN = [
    "The jars are for later. Do not touch the jars. The jars have been touched enough.",
    "He is very dedicated. It is almost moving. In the way a fire alarm is moving.",
    "We vote on everything here. We voted yes on this. It was unanimous. Mostly.",
    "My husband is in the other circle. He is also very happy. We compare notes at breakfast.",
    "I came for the foraging. I stayed for the ceremony. The foraging is not as good.",
    "Do not worry about the towel. The towel is a technicality. Bring it anyway.",
]


def amphitheater(w, g, rng):
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
    m.set(4, 8, kit.extra["rift"])
    door = m.warp(*kit.door_cell(4, 8, kit.extra["rift"]))
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
    m.scripts.append(
        "GroveAmphitheaterCrowleyScript:\n\tfaceplayer\n\topentext\n\tcheckevent EVENT_AMPH_DONE\n\tiffalse .Wait\n"
        "\tcheckevent EVENT_LORE_AMPH\n\tiftrue .Again\n\twritetext GroveAmphitheaterCrowleyText\n\twaitbutton\n"
        "\tsetevent EVENT_LORE_AMPH\n\tclosetext\n\tend\n.Again:\n\twritetext GroveAmphitheaterCrowleyAgainText\n"
        "\twaitbutton\n\tclosetext\n\tend\n.Wait:\n\twritetext GroveAmphitheaterCrowleyWaitText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(C.CROWLEY_2).emit("GroveAmphitheaterCrowleyText"))
    m.scripts.append(Text(C.CROWLEY_3).emit("GroveAmphitheaterCrowleyAgainText"))
    m.scripts.append(Text("Sit. Do not take notes. The circle is not yet full.").emit("GroveAmphitheaterCrowleyWaitText"))
    m.obj(8, 8, "SPRITE_HC_CROWLEY", FACE["DOWN"], "GroveAmphitheaterCrowleyScript", pal="PAL_NPC_BROWN")
    women = [(3, 6, "SPRITE_HC_HIPPIE_F", "PAL_NPC_PINK", "RIGHT"), (3, 9, "SPRITE_HC_BATHER_F", "PAL_NPC_BLUE", "RIGHT"),
             (3, 12, "SPRITE_HC_ELDER_F", "PAL_NPC_GREEN", "RIGHT"), (14, 6, "SPRITE_HC_BATHER_F", "PAL_NPC_PINK", "LEFT"),
             (14, 9, "SPRITE_HC_HIPPIE_F", "PAL_NPC_GREEN", "LEFT"), (14, 12, "SPRITE_HC_ELDER_F", "PAL_NPC_RED", "LEFT")]
    for i, (x, y, sp, pal, face) in enumerate(women):
        plain_npc(m, x, y, sp, pal, face, f"GroveAmphitheaterWoman{i}Script", AMPH_WOMEN[i])
    g.add(m)
    m.a, m.cw = 3, 3
    return m


def area3(w, g):
    add_sprite(g, "SPRITE_HC_SABBAH")
    for plaza, text, label in (("AxiomPlaza1", C.SABBAH_1, "AxiomPlaza1SabbahScript"), ("AxiomPlaza6", C.SABBAH_2, "AxiomPlaza6SabbahScript")):
        lore_npc(w, find(g, plaza), *spot(find(g, plaza)), "SPRITE_HC_SABBAH", "PAL_NPC_BROWN", "LEFT", label, text, flag="EVENT_LORE_SABBAH")


def area4(w, g):
    add_sprite(g, "SPRITE_HC_CIORAN", "SPRITE_HC_STEINER")
    lore_npc(w, find(g, "LotusPlaza1"), *spot(find(g, "LotusPlaza1")), "SPRITE_HC_CIORAN", "PAL_NPC_BROWN", "LEFT", "LotusPlaza1CioranScript",
             C.CIORAN_1, flag="EVENT_LORE_CIORAN")
    lore_npc(w, find(g, "LotusPlaza4"), *spot(find(g, "LotusPlaza4")), "SPRITE_HC_CIORAN", "PAL_NPC_BROWN", "LEFT", "LotusPlaza4CioranScript",
             C.CIORAN_2, flag="EVENT_LORE_CIORAN")
    steiner(w, g, "LotusPlaza6", C.STEINER_4, "LotusPlaza6SteinerScript")
