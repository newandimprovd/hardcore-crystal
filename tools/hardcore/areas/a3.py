"""Area 3: THE UNION, a robot state with a robot mayor where humans are filed, ranked and paired by committee."""
from . import a3_text as T
from . import kits
from .builder import AreaCfg, BossSpec, build_area
from .specbase import SpecBase
from .a2 import TIERS


class Spec(SpecBase):
    pool = "A3"
    l0, l1 = 44, 62
    T = T
    theme = {"ELECTRIC": 3, "STEEL": 3, "PSYCHIC_TYPE": 2, "NORMAL": 2, "POISON": 1.5, "FIGHTING": 1.5, "FIRE": 1,
             "DARK": 1, "GROUND": 1, "FLYING": 1, "ROCK": 0.8, "ICE": 0.7, "BUG": 0.7, "WATER": 0.5, "GHOST": 0.5,
             "DRAGON": 0.4, "GRASS": 0.3, "FAIRY": 0.3}
    classes = [("SCIENTIST", "SPRITE_SCIENTIST", "PAL_NPC_GREEN", 3),
               ("GRUNTM", "SPRITE_ROCKET", "PAL_NPC_BLUE", 3),
               ("GRUNTF", "SPRITE_ROCKET_GIRL", "PAL_NPC_BLUE", 2),
               ("OFFICER", "SPRITE_OFFICER", "PAL_NPC_BLUE", 3),
               ("EXECUTIVEM", "SPRITE_GENTLEMAN", "PAL_NPC_RED", 1),
               ("EXECUTIVEF", "SPRITE_RECEPTIONIST", "PAL_NPC_RED", 1),
               ("SUPER_NERD", "SPRITE_SUPER_NERD", "PAL_NPC_BLUE", 2),
               ("COOLTRAINERM", "SPRITE_COOLTRAINER_M", "PAL_NPC_BLUE", 2),
               ("COOLTRAINERF", "SPRITE_COOLTRAINER_F", "PAL_NPC_BLUE", 2),
               ("TEACHER", "SPRITE_TEACHER", "PAL_NPC_GREEN", 1),
               ("BLACKBELT_T", "SPRITE_BLACK_BELT", "PAL_NPC_BROWN", 2),
               ("GUITARIST", "SPRITE_ROCKER", "PAL_NPC_RED", 1),
               ("BIKER", "SPRITE_BIKER", "PAL_NPC_GREEN", 1)]


def build(w, roster, rng, entry_doors, open_exit=False):
    texts = dict(center=T.CENTER, mart=T.MART, house=T.HOUSE)
    bosses = [
        BossSpec("AxiomRegistry", "DR AXIOM", "SCIENTIST", "SPRITE_SCIENTIST", "PAL_NPC_GREEN", 51, 5, T.LAB_SEEN,
                 T.LAB_BEATEN, T.LAB_AFTER, template="karen", item="FLASHLIGHT"),
        BossSpec("AxiomArmory", "IRONWARDEN", "OFFICER", "SPRITE_OFFICER", "PAL_NPC_RED", 57, 5, T.ARMORY_SEEN,
                 T.ARMORY_BEATEN, T.ARMORY_AFTER, template="will", item="SLEDGEHAMMER"),
        BossSpec("AxiomMayoralty", "THE MAYOR", "EXECUTIVEM", "SPRITE_ROCKET", "PAL_NPC_BLUE", 64, 6, T.MAYORALTY_SEEN,
                 T.MAYORALTY_BEATEN, T.MAYORALTY_AFTER, template="bruno", landmark="LANDMARK_AXIOM_MAYORALTY",
                 music="MUSIC_ROCKET_HIDEOUT", open_exit=open_exit)]
    cfg = AreaCfg("AREA3", "Axiom", Spec(), kits.modern(), "PALETTE_DAY",
                  [("AXIOM_OUTSKIRTS", 46, 54, "AXIOM<BSP>OUTSKIRTS"), ("AXIOM_CENTRAL", 42, 50, "AXIOM<BSP>CENTRAL"),
                   ("AXIOM_MAYORALTY", 38, 46, "THE<BSP>MAYORALTY")],
                  "MUSIC_GOLDENROD_CITY", texts, TIERS, bosses, [None, "dark", "slab"], [3, 2, 3], "AxiomGate",
                  T.GATE[0], trainers=([13, 14, 13, 13, 13], [13, 13, 13, 14, 13], 13), stock_ix=(1, 1, 1, 2, 2, 2, 2))
    return build_area(w, roster, rng, cfg, entry_doors)
