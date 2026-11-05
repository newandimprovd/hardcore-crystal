"""The opening junction outside Cherrygrove: a T intersection with Mr. POKeMON's house (the POKeDEX and the vanishing), James Joyce
(the lore, the CORKBOARD) and the door into PURGATORIO.  The road out of Cherrygrove comes in from the south, turns west and then north
to Tithe Road, and the east arm ends under the hill at the cave door."""
from . import cast_text as C
from . import kits
from .flags import flag_once
from .layout import FACE, blk
from .model import MapDef, link
from .people import lore_npc, sign
from .text import Text

STEM_A = 8  # the stem's first block column (three blocks wide)
CHERRY_COL = 7  # the first block column of Cherrygrove's north exit corridor


def build(w, roster, rng):
    """Returns (group, cave warp of the junction (to be linked with the Purgatorio hub), junction map, offset for Cherrygrove)."""
    w.landmarks.append(("TITHE_JUNCTION", 80, 90, "THE<BSP>CROSSROADS"))
    LM = "LANDMARK_TITHE_JUNCTION"
    g = w.group("OPEN", ["SPRITE_HC_JOYCE", "SPRITE_POKE_BALL", "SPRITE_HC_MR_POKEMON"])
    johto = kits.johto()
    W, H = 19, 12
    m = MapDef(g.key, "TitheJunction", W, H, johto.tileset, "ROUTE", LM, "MUSIC_ROUTE_30", border=johto.extra["border"])
    m.fill(0x05)
    road = johto.floor[0]
    # the stem, the band (a T), the west arm up to the north edge
    for y in range(5, H):
        for x in range(STEM_A, STEM_A + 3):
            m.set(x, y, road)
    for y in range(3, 6):
        for x in range(2, 17):
            m.set(x, y, road)
    for y in range(0, 3):
        for x in range(2, 5):
            m.set(x, y, road)
    # Mr. Pokemon's house on the north side of the band, the cave mouth at the east end
    hx = 7
    m.set(hx, 2, johto.extra["house"][0])
    m.set(hx + 1, 2, johto.extra["house"][1])
    house_door = m.warp(*johto.door_cell(hx, 2, johto.extra["house"][0]))
    m.set(15, 2, 0x73)  # the cave mouth in the rock
    cave = m.warp(2 * 15, 2 * 2 + 1, "mouth")
    # a signpost near the cave
    m.set(13, 2, 0x47)
    sign(m, 2 * 13 + 1, 2 * 2 + 1, "TitheJunctionSign", "EAST: PURGATORIO. Nobody dies in there. Complaints go to the dead. WEST: Tithe Lowtown.")
    # Joyce stands on the band west of the stem
    flag_once(w, "EVENT_LORE_JOYCE")
    joyce_flag = flag_once(w, "EVENT_JOYCE_MET")
    m.scripts.append(
        "TitheJunctionJoyceScript:\n\tfaceplayer\n\topentext\n\tcheckevent EVENT_JOYCE_MET\n\tiftrue .Again\n"
        "\twritetext TitheJunctionJoyceText\n\twaitbutton\n\tverbosegiveitem CORKBOARD\n\tsetevent EVENT_JOYCE_MET\n"
        "\tsetevent EVENT_LORE_JOYCE\n\tclosetext\n\tend\n\n"
        ".Again:\n\twritetext TitheJunctionJoyceAgainText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(C.JOYCE_1).emit("TitheJunctionJoyceText"))
    m.scripts.append(Text(C.JOYCE_AGAIN).emit("TitheJunctionJoyceAgainText"))
    m.obj(11, 8, "SPRITE_HC_JOYCE", FACE["RIGHT"], "TitheJunctionJoyceScript", pal="PAL_NPC_BROWN")
    g.add(m)
    m.a, m.cw = 2, 3  # the west arm: the corridor tithe road continues from
    m.stem = STEM_A
    # Mr. Pokemon's house
    hm = MapDef(g.key, "FinneganHouse", 4, 4, "TILESET_HOUSE", "INDOOR", LM, "MUSIC_CHERRYGROVE_CITY", pal="PALETTE_DAY")
    hm.blocks = bytearray(blk("maps/House1.blk"))
    w1, w2 = hm.warp(2, 7), hm.warp(3, 7)
    house_door.dest = w1
    w1.dest = house_door
    w2.dest = house_door
    gone = w.flag("EVENT_FINNEGAN_GONE")
    flag_once(w, "EVENT_LORE_MRP")
    hm.object_consts = ["MRP"]
    first, rest = C.MRP_1.split("\n\n", 3)[:3], C.MRP_1.split("\n\n", 3)[3]
    part_a = "\n\n".join(first)
    hm.scripts.append(
        "FinneganHouseMrpScript:\n\tfaceplayer\n\topentext\n\twritetext FinneganHouseMrpTextA\n\twaitbutton\n"
        "\tsetflag ENGINE_POKEDEX\n\tplaysound SFX_ITEM\n\twritetext FinneganHouseGotDexText\n\twaitbutton\n"
        "\twritetext FinneganHouseMrpTextB\n\twaitbutton\n\tsetevent EVENT_LORE_MRP\n\tclosetext\n"
        "\treadvar VAR_FACING\n\tifequal UP, .Around\n"
        "\tapplymovement FINNEGAN_HOUSE_MRP, FinneganHouseRunMovement\n\tsjump .Gone\n"
        ".Around:\n\tapplymovement FINNEGAN_HOUSE_MRP, FinneganHouseRunAroundMovement\n"
        ".Gone:\n\tplaysound SFX_EXIT_BUILDING\n\tdisappear FINNEGAN_HOUSE_MRP\n\tsetevent EVENT_FINNEGAN_GONE\n\tend\n\n"
        "FinneganHouseRunMovement:\n\tbig_step DOWN\n\tbig_step DOWN\n\tbig_step DOWN\n\tbig_step LEFT\n\tbig_step LEFT\n"
        "\tbig_step LEFT\n\tbig_step DOWN\n\tstep_end\n\n"
        "FinneganHouseRunAroundMovement:\n\tbig_step LEFT\n\tbig_step DOWN\n\tbig_step DOWN\n\tbig_step DOWN\n\tbig_step LEFT\n"
        "\tbig_step LEFT\n\tbig_step DOWN\n\tstep_end\n")
    hm.scripts.append(Text(part_a).emit("FinneganHouseMrpTextA"))
    hm.scripts.append(Text(rest).emit("FinneganHouseMrpTextB"))
    hm.scripts.append("FinneganHouseGotDexText:\n\ttext \"<PLAYER> got\"\n\tline \"POKéDEX!\"\n\tdone\n")
    hm.obj(6, 3, "SPRITE_HC_MR_POKEMON", FACE["DOWN"], "FinneganHouseMrpScript", pal="PAL_NPC_BROWN", flag=gone)
    # the empty chair
    hm.scripts.append("FinneganHouseChairScript:\n\tjumptext FinneganHouseChairText\n")
    hm.scripts.append(Text(C.MRP_GONE_NOTE).emit("FinneganHouseChairText"))
    hm.bg(6, 3, "BGEVENT_READ", "FinneganHouseChairScript")
    g.add(hm)
    return g, cave, m
