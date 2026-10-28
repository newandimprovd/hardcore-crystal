"""Area 3: THE UNION, a robot state with a robot mayor where humans are filed, ranked and paired by committee."""
from art.classes import area_mix
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
    hub = dict(nurse=("SPRITE_HC_DOC", "PAL_NPC_PINK"),
               clerk=("SPRITE_HC_BOT_DRONE", "PAL_NPC_BLUE"),
               pc=[("SPRITE_HC_SERF", "PAL_NPC_GREEN"), ("SPRITE_HC_BOT_EXEC", "PAL_NPC_BROWN"), ("SPRITE_HC_SERF_F", "PAL_NPC_GREEN")],
               mart=[("SPRITE_HC_GUARD", "PAL_NPC_BROWN"), ("SPRITE_HC_SERF", "PAL_NPC_GREEN")],
               house=[("SPRITE_HC_SERF", "PAL_NPC_GREEN"), ("SPRITE_HC_MATCHMAKER", "PAL_NPC_PINK")],
               gate=[("SPRITE_HC_BOT_COP", "PAL_NPC_BLUE"), ("SPRITE_HC_SERF_F", "PAL_NPC_GREEN")])
    classes = area_mix("AREA3")


def build(w, roster, rng, entry_doors, open_exit=False):
    texts = dict(center=T.CENTER, mart=T.MART, house=T.HOUSE)
    bosses = [
        BossSpec("AxiomRegistry", "DR AXIOM", "U_MADDOC", "SPRITE_HC_DOC_MAD", "PAL_NPC_PINK", 51, 5, T.LAB_SEEN,
                 T.LAB_BEATEN, T.LAB_AFTER, template="karen", item="FLASHLIGHT"),
        BossSpec("AxiomArmory", "IRONWARDEN", "U_WARDBOT", "SPRITE_HC_BOT_WARDEN", "PAL_NPC_BROWN", 57, 5, T.ARMORY_SEEN,
                 T.ARMORY_BEATEN, T.ARMORY_AFTER, template="will", item="SLEDGEHAMMER"),
        BossSpec("AxiomMayoralty", "THE MAYOR", "U_MAYOR", "SPRITE_HC_BOT_MAYOR", "PAL_NPC_BROWN", 64, 6, T.MAYORALTY_SEEN,
                 T.MAYORALTY_BEATEN, T.MAYORALTY_AFTER, template="bruno", landmark="LANDMARK_AXIOM_MAYORALTY",
                 music="MUSIC_ROCKET_HIDEOUT", open_exit=open_exit)]
    cfg = AreaCfg("AREA3", "Axiom", Spec(), kits.axiom(), "PALETTE_DAY",
                  [("AXIOM_OUTSKIRTS", 46, 54, "AXIOM<BSP>OUTSKIRTS"), ("AXIOM_CENTRAL", 42, 50, "AXIOM<BSP>CENTRAL"),
                   ("AXIOM_MAYORALTY", 38, 46, "THE<BSP>MAYORALTY")],
                  "MUSIC_GOLDENROD_CITY", texts, TIERS, bosses, [None, "dark", "slab"], [3, 2, 3], "AxiomGate",
                  T.GATE[0], trainers=([13, 14, 13, 13, 13], [13, 13, 13, 14, 13], 13), stock_ix=(1, 1, 1, 2, 2, 2, 2))
    return build_area(w, roster, rng, cfg, entry_doors)
