"""The opening junction outside Cherrygrove: a T intersection with Mr. POKeMON's house (the POKeDEX and the vanishing), James Joyce
(the lore, the CORKBOARD) and the door into PURGATORIO.  The road out of Cherrygrove comes in from the south, turns west and then north
to Tithe Road, and the east arm ends under the hill at the cave door."""
import random

from . import cast_text as C
from . import named
from . import named_text as N
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
    g = w.group("OPEN", ["SPRITE_HC_JOYCE", "SPRITE_POKE_BALL", "SPRITE_RIVAL"])
    johto = kits.johto()
    W, H = 19, 12
    m = MapDef(g.key, "TitheJunction", W, H, johto.tileset, "ROUTE", LM, "MUSIC_HC_ROAD", border=johto.extra["border"])
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
    roof, front = johto.extra["house_roof"], johto.extra["house_front"]  # a whole house: roof row over the front row, not a single strip
    m.set(hx, 1, roof[0])
    m.set(hx + 1, 1, roof[1])
    m.set(hx, 2, front[0])
    m.set(hx + 1, 2, front[1])
    house_door = m.warp(*johto.door_cell(hx, 2, front[0]))
    # the cave: a whole mountain face like the Dark Cave of Route 31, not one block among trees.  It fills the north east corner of the map
    # (west rim, five blocks of rock, east rim; two rows of plateau over one row of cliff face, the mouth in the face) so the rock runs to
    # the edge of the screen from wherever the player stands on the east arm.
    MX0, MX1 = 11, W - 1
    for x in range(MX0, MX1 + 1):
        if x == MX0:
            col = (0x68, 0x68, 0x6c)
        elif x == MX1:
            col = (0x69, 0x69, 0x6d)
        else:
            col = (0x71, 0x71, 0x73 if x == 15 else 0x72)
        for y, b in enumerate(col):
            m.set(x, y, b)
    cave = m.warp(2 * 15, 2 * 2 + 1, "mouth")
    # a signpost on the grass just west of the mountain
    m.set(9, 2, 0x47)
    sign(m, 2 * 9 + 1, 2 * 2 + 1, "TitheJunctionSign", "EAST: PURGATORIO. Nobody dies in there. Complaints go to the dead. WEST: Tithe Lowtown.")
    # Joyce is not on the map until Mr. POKeMON's scene is over.  Then the player steps out of the house, Joyce walks in from the west
    # along the top of the road and speaks first (confused, he knows nothing yet).  Talking to him later gives the lore, once.
    flag_once(w, "EVENT_LORE_JOYCE")
    joyce_met = flag_once(w, "EVENT_JOYCE_MET")
    joyce_told = flag_once(w, "EVENT_JOYCE_TOLD")
    joyce_away = flag_once(w, "EVENT_JOYCE_ABSENT")
    jidx = len(m.objects) + 1
    JC = named.name_object(m, jidx, "JOYCE")
    player_x_after_house = 15  # the player stands below the door of Mr. POKeMON's house when the scene starts
    JOYCE_END = (14, 6)  # next to the cell where the player stands after leaving the house door
    m.obj(JOYCE_END[0], JOYCE_END[1], "SPRITE_HC_JOYCE", FACE["RIGHT"], "TitheJunctionJoyceScript", pal="PAL_NPC_BROWN", flag=joyce_away)
    m.scripts.append(
        "TitheJunctionJoyceScript:\n\tfaceplayer\n\topentext\n\tcheckevent EVENT_JOYCE_TOLD\n\tiftrue .Again\n"
        "\twritetext TitheJunctionJoyceLoreText\n\twaitbutton\n\tsetevent EVENT_JOYCE_TOLD\n\tsetevent EVENT_LORE_JOYCE\n\tclosetext\n\tend\n\n"
        ".Again:\n\twritetext TitheJunctionJoyceAgainText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(C.JOYCE_2).emit("TitheJunctionJoyceLoreText"))
    m.scripts.append(Text(C.JOYCE_AGAIN).emit("TitheJunctionJoyceAgainText"))
    m.scripts.append(f"TitheJunctionJoyceAppear:\n\tcheckevent EVENT_JOYCE_MET\n\tiftrue .Show\n\tdisappear {JC}\n.Show:\n\tendcallback\n")
    m.callbacks.append(("MAPCALLBACK_OBJECTS", "TitheJunctionJoyceAppear"))
    # he starts just beyond the left edge of the screen (an object further out has no object struct and the walk would never end)
    start = player_x_after_house - 5
    walk = JOYCE_END[0] - start
    m.scripts.append(
        "TitheJunctionJoyceScene:\n\tcheckevent EVENT_FINNEGAN_GONE\n\tiffalse .Done\n\tcheckevent EVENT_JOYCE_MET\n\tiftrue .Done\n"
        f"\tmoveobject {JC}, {start}, {JOYCE_END[1]}\n\tappear {JC}\n\tapplymovement {JC}, TitheJunctionJoyceWalk\n"
        f"\tturnobject PLAYER, LEFT\n\tshowemote EMOTE_QUESTION, {JC}, 15\n\topentext\n\twritetext TitheJunctionJoyceText\n\twaitbutton\n"
        "\tclosetext\n\tsetevent EVENT_JOYCE_MET\n.Done:\n\tend\n\n"
        "TitheJunctionJoyceWalk:\n" + "\tstep RIGHT\n" * walk + "\tstep_end\n")
    m.scripts.append(Text(C.JOYCE_1).emit("TitheJunctionJoyceText"))
    # the engine does not look at coord events on the cell a warp lands on (events stay off until the first step), so the scene is queued
    # as a re-entry script: the house script calls TitheJunctionQueueJoyce right before the player is walked out, and the engine runs the
    # queue on the first tick on the road
    m.scripts.append(
        "TitheJunctionQueueJoyce::\n\tld hl, wMapReentryScriptQueueFlag\n\tld [hl], 1\n\tinc hl\n\tld [hl], BANK(TitheJunctionJoyceScene)\n"
        "\tinc hl\n\tld [hl], LOW(TitheJunctionJoyceScene)\n\tinc hl\n\tld [hl], HIGH(TitheJunctionJoyceScene)\n\tret\n")
    # Mr. POKeMON's house is not optional: the first step onto the road from the stem walks the player to the door and in.
    # The movement is one per trigger cell (the cells differ in how far they are from the door at (15, 5)).
    m.scripts.append(Text(C.MRP_CALL).emit("TitheJunctionHouseCallText"))
    door_x, door_y = 15, 5
    for x in range(2 * STEM_A, 2 * STEM_A + 6):
        k = x - door_x
        mv = "\tstep UP\n" * (11 - (door_y + 1)) + (("\tstep LEFT\n" * k) if k > 0 else ("\tstep RIGHT\n" * -k)) + "\tstep UP\n"
        m.scripts.append(
            f"TitheJunctionHouseCall{x}:\n\tcheckevent EVENT_FINNEGAN_GONE\n\tiftrue .Done\n\topentext\n\twritetext TitheJunctionHouseCallText\n"
            f"\twaitbutton\n\tclosetext\n\tapplymovement PLAYER, TitheJunctionHouseCall{x}Move\n"
            "\tplaysound SFX_ENTER_DOOR\n\twaitsfx\n\tcallasm FinneganHouseQueueMeet\n\twarp FINNEGAN_HOUSE, 3, 6\n\tend\n.Done:\n\tend\n\n"
            f"TitheJunctionHouseCall{x}Move:\n{mv}\tstep_end\n")
        m.coords.append((x, 11, -1, f"TitheJunctionHouseCall{x}"))
    # the first fight with the rival: he stands in the stem and the whole width of the road is a trigger, so nobody gets to Joyce, the
    # house or the cave without it (level 5, two creatures: the thief has the starter that was meant to be the player's)
    named.rival_duel(w, m, "RIVAL0", "RIVAL1", 5, 2, random.Random("named-RIVAL0"), roster, N.RIVAL0, (19, 15),
                     [(x, 18) for x in range(2 * STEM_A, 2 * STEM_A + 6)])
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
    # the scene is a re-entry script queued by the junction right before the warp (coord events do not fire on the arrival cell): the player is
    # walked to Mr. POKeMON's chair, he speaks a few lines about himself, hands over the CORKBOARD and the POKeDEX and leaves by the door,
    # and the player is walked out after him (Joyce's scene is queued for the road)
    hm.scripts.append(
        "FinneganHouseQueueMeet::\n\tld hl, wMapReentryScriptQueueFlag\n\tld [hl], 1\n\tinc hl\n\tld [hl], BANK(FinneganHouseMeetScript)\n"
        "\tinc hl\n\tld [hl], LOW(FinneganHouseMeetScript)\n\tinc hl\n\tld [hl], HIGH(FinneganHouseMeetScript)\n\tret\n\n"
        "FinneganHouseMeetScript:\n\tcheckevent EVENT_FINNEGAN_GONE\n\tiftrue .Done\n"
        "\tapplymovement PLAYER, FinneganHouseWalkToMrp\n\tturnobject PLAYER, RIGHT\n\tturnobject FINNEGAN_HOUSE_MRP, LEFT\n"
        "\topentext\n\twritetext FinneganHouseMrpTextA\n\twaitbutton\n\tverbosegiveitem CORKBOARD\n"
        "\tsetflag ENGINE_POKEDEX\n\tplaysound SFX_ITEM\n\twritetext FinneganHouseGotDexText\n\twaitbutton\n"
        "\twritetext FinneganHouseMrpTextB\n\twaitbutton\n\tsetevent EVENT_LORE_MRP\n\tclosetext\n"
        "\tapplymovement FINNEGAN_HOUSE_MRP, FinneganHouseRunMovement\n"
        "\tplaysound SFX_EXIT_BUILDING\n\tdisappear FINNEGAN_HOUSE_MRP\n\tsetevent EVENT_FINNEGAN_GONE\n"
        "\tapplymovement PLAYER, FinneganHouseWalkOut\n\tplaysound SFX_EXIT_BUILDING\n\tcallasm TitheJunctionQueueJoyce\n"
        "\twarp TITHE_JUNCTION, 15, 6\n.Done:\n\tend\n\n"
        "FinneganHouseMrpScript:\n\tfaceplayer\n\topentext\n\twritetext FinneganHouseMrpTextB\n\twaitbutton\n\tclosetext\n\tend\n\n"
        "FinneganHouseWalkToMrp:\n\tstep RIGHT\n\tstep RIGHT\n\tstep UP\n\tstep UP\n\tstep UP\n\tstep_end\n\n"
        "FinneganHouseWalkOut:\n\tstep DOWN\n\tstep DOWN\n\tstep DOWN\n\tstep LEFT\n\tstep LEFT\n\tstep_end\n\n"
        "FinneganHouseRunMovement:\n\tbig_step DOWN\n\tbig_step DOWN\n\tbig_step DOWN\n\tbig_step LEFT\n\tbig_step LEFT\n"
        "\tbig_step LEFT\n\tbig_step DOWN\n\tstep_end\n")
    hm.scripts.append(Text(C.MRP_1).emit("FinneganHouseMrpTextA"))
    hm.scripts.append(Text(C.MRP_2).emit("FinneganHouseMrpTextB"))
    hm.scripts.append("FinneganHouseGotDexText:\n\ttext \"<PLAYER> got\"\n\tline \"POKéDEX!\"\n\tdone\n")
    # the Gentleman of the base game: Mr. POKeMON's own sprite
    hm.obj(6, 3, "SPRITE_GENTLEMAN", FACE["DOWN"], "FinneganHouseMrpScript", pal="0", flag=gone)
    # the empty chair
    hm.scripts.append("FinneganHouseChairScript:\n\tjumptext FinneganHouseChairText\n")
    hm.scripts.append(Text(C.MRP_GONE_NOTE).emit("FinneganHouseChairText"))
    hm.bg(6, 3, "BGEVENT_READ", "FinneganHouseChairScript")
    g.add(hm)
    return g, cave, m
