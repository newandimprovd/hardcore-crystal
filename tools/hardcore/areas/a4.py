"""Area 4: THE LOTUS COAST, a resort nation built on forgetting, ending at the rival's mansion."""
from . import a4_text as T
from . import kits
from .builder import AreaCfg, BossSpec, build_area
from .layout import mansion_bedroom, mansion_hall
from .text import Text
from .specbase import SpecBase
from .layout import FACE
from .a2 import TIERS


class Spec(SpecBase):
    pool = "A4"
    l0, l1 = 62, 78
    T = T
    theme = {"WATER": 3, "FAIRY": 2.5, "PSYCHIC_TYPE": 2, "NORMAL": 2, "FLYING": 2, "GRASS": 1.5, "FIRE": 1.5,
             "ICE": 1, "GROUND": 1, "ELECTRIC": 1, "POISON": 1, "GHOST": 1, "DARK": 1, "BUG": 0.7, "FIGHTING": 0.7,
             "STEEL": 0.5, "ROCK": 0.5, "DRAGON": 0.6}
    classes = [("BEAUTY", "SPRITE_BEAUTY", "PAL_NPC_PINK", 4),
               ("SWIMMERM", "SPRITE_SWIMMER_GUY", "PAL_NPC_BLUE", 4),
               ("SWIMMERF", "SPRITE_SWIMMER_GIRL", "PAL_NPC_PINK", 4),
               ("SAILOR", "SPRITE_SAILOR", "PAL_NPC_BLUE", 2),
               ("GENTLEMAN", "SPRITE_GENTLEMAN", "PAL_NPC_BROWN", 2),
               ("LASS", "SPRITE_LASS", "PAL_NPC_PINK", 2),
               ("GUITARIST", "SPRITE_ROCKER", "PAL_NPC_RED", 2),
               ("FISHER", "SPRITE_FISHER", "PAL_NPC_BLUE", 2),
               ("SAGE", "SPRITE_SAGE", "PAL_NPC_BROWN", 2),
               ("SCIENTIST", "SPRITE_PHARMACIST", "PAL_NPC_GREEN", 2),
               ("TEACHER", "SPRITE_TEACHER", "PAL_NPC_GREEN", 1),
               ("COOLTRAINERF", "SPRITE_COOLTRAINER_F", "PAL_NPC_PINK", 2),
               ("COOLTRAINERM", "SPRITE_COOLTRAINER_M", "PAL_NPC_RED", 2),
               ("BURGLAR", "SPRITE_ROCKET", "PAL_NPC_BROWN", 2),
               ("GRUNTM", "SPRITE_BIKER", "PAL_NPC_BROWN", 2)]


def build(w, roster, rng, entry_doors, open_exit=False):
    texts = dict(center=T.CENTER, mart=T.MART, house=T.HOUSE)
    bosses = [
        BossSpec("LotusClinic", "DR LETHE", "SCIENTIST", "SPRITE_PHARMACIST", "PAL_NPC_GREEN", 69, 5, T.CLINIC_SEEN,
                 T.CLINIC_BEATEN, T.CLINIC_AFTER, template="karen", item="GRAPPLE_HOOK"),
        BossSpec("LotusCabana", "MGR KAI", "GENTLEMAN", "SPRITE_GENTLEMAN", "PAL_NPC_BROWN", 74, 5,
                 T.CABANA_SEEN, T.CABANA_BEATEN, T.CABANA_AFTER, template="will", item="SHOVEL"),
        BossSpec("LotusMansion", "RIVAL", "RIVAL2", "SPRITE_RIVAL", "PAL_NPC_RED", 80, 6, T.MANSION_SEEN,
                 T.MANSION_BEATEN, T.MANSION_AFTER, template="bruno", landmark="LANDMARK_LOTUS_MANSION",
                 music="MUSIC_ROCKET_HIDEOUT", open_exit=open_exit, story=2)]
    cfg = AreaCfg("AREA4", "Lotus", Spec(), kits.kanto(), "PALETTE_DAY",
                  [("LOTUS_COAST", 36, 62, "LOTUS<BSP>COAST"), ("LOTUS_BOARDWALK", 32, 58, "THE<BSP>BOARDWALK"),
                   ("LOTUS_MANSION", 28, 54, "THE<BSP>HILLTOP")],
                  "MUSIC_VERMILION_CITY", texts, TIERS, bosses, [None, "hook", "rubble"], [3, 2, 3], "LotusGate",
                  T.GATE[0], trainers=([13, 14, 13, 13, 13], [13, 13, 13, 14, 13], 13), stock_ix=(2, 2, 2, 2, 2, 2, 2))
    g, exits = build_area(w, roster, rng, cfg, entry_doors)
    mansion(g, exits)
    return g, exits


def mansion(g, exits):
    """The rival's house, the player's from the rival's death on: a hall full of staff, a limousine to New Bark
    Town and the bedroom where the game ends."""
    lm = "LANDMARK_LOTUS_MANSION"
    music = "MUSIC_CELADON_CITY"
    hall, door = mansion_hall(g, "LotusHall", exits, lm, music)
    bed = mansion_bedroom(g, "LotusBedroom", door, lm, "MUSIC_NEW_BARK_TOWN")
    spots = [(3, 3, "SPRITE_BEAUTY", "DOWN", "PAL_NPC_PINK"), (12, 3, "SPRITE_LASS", "DOWN", "PAL_NPC_RED"),
             (2, 9, "SPRITE_BEAUTY", "RIGHT", "PAL_NPC_BLUE"), (13, 9, "SPRITE_LASS", "LEFT", "PAL_NPC_PINK"),
             (4, 5, "SPRITE_BEAUTY", "DOWN", "PAL_NPC_GREEN"), (11, 5, "SPRITE_LASS", "DOWN", "PAL_NPC_BROWN")]
    hall.object_consts = [f"NPC{i}" for i in range(len(spots) + 2)]
    for i, (x, y, sp, f, pal) in enumerate(spots):
        hall.scripts.append(f"LotusHallMaid{i}Script:\n\tjumptextfaceplayer LotusHallMaid{i}Text\n")
        hall.scripts.append(Text(T.HALL_MAIDS[i]).emit(f"LotusHallMaid{i}Text"))
        hall.obj(x, y, sp, FACE[f], f"LotusHallMaid{i}Script", pal=pal)
    n = len(spots)
    hall.scripts.append("LotusHallButlerScript:\n\tjumptextfaceplayer LotusHallButlerText\n")
    hall.scripts.append(Text(T.HALL_BUTLER).emit("LotusHallButlerText"))
    hall.obj(9, 4, "SPRITE_GENTLEMAN", FACE["DOWN"], "LotusHallButlerScript", pal="PAL_NPC_BROWN")
    hall.scripts.append(
        "LotusHallChauffeurScript:\n\tfaceplayer\n\topentext\n\twritetext LotusHallChauffeurText\n\tyesorno\n"
        "\tiffalse .No\n\twritetext LotusHallChauffeurGoText\n\twaitbutton\n\tcloseText\n"
        "\tspecial FadeOutToBlack\n\twarp NEW_BARK_TOWN, 2, 8\n\tend\n\n.No:\n\twritetext LotusHallChauffeurNoText\n"
        "\twaitbutton\n\tclosetext\n\tend\n".replace("closeText", "closetext"))
    hall.scripts.append(Text(T.HALL_CHAUFFEUR).emit("LotusHallChauffeurText"))
    hall.scripts.append(Text(T.HALL_CHAUFFEUR_GO).emit("LotusHallChauffeurGoText"))
    hall.scripts.append(Text(T.HALL_CHAUFFEUR_NO).emit("LotusHallChauffeurNoText"))
    hall.obj(8, 9, "SPRITE_OFFICER", FACE["UP"], "LotusHallChauffeurScript", pal="PAL_NPC_RED")
    return hall, bed
