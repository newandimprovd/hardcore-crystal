"""Trainer classes of the generated areas: every (area, cast sprite, colorway) is a class of its own with its own name and battle portrait.

Entry: (constant, name shown in battle (12 chars max), cast slug (art/cast.py), NPC palette name (art/areapal.py), count in the area's
random mix, vanilla class that attributes/DVs/encounter music are copied from, gender for the Battle Tower table).
The `boss` entries are classes that only a boss uses (count 0)."""
from collections import OrderedDict

M, F = "MALE", "FEMALE"

AREA_CLASSES = OrderedDict()

AREA_CLASSES["AREA1"] = [
    ("T_COP", "COP", "cop", "BLUE", 6, "OFFICER", M),
    ("T_SUIT", "SUIT", "suit", "BROWN", 3, "GENTLEMAN", M),
    ("T_HOODIE", "HOODIE", "hoodie", "GREEN", 2, "COOLTRAINERM", M),
    ("T_BANKER", "BANKER", "suit_f", "PINK", 2, "COOLTRAINERF", F),
    ("T_CHOIR", "CHOIR", "choir", "PINK", 2, "BEAUTY", F),
    ("T_THUG", "THUG", "thug", "GREEN", 2, "BIKER", M),
    ("T_PRIEST", "PRIEST", "priest", "BROWN", 3, "GRUNTM", M),
    ("T_NUN", "NUN", "nun", "BROWN", 2, "GRUNTF", F),
    ("T_BEGGAR", "BEGGAR", "beggar", "GREEN", 2, "SUPER_NERD", M),
    ("T_ALTARBOY", "ALTAR BOY", "choir", "BLUE", 2, "SCHOOLBOY", M),
    ("T_PUNK", "PUNK", "punk", "RED", 2, "LASS", F),
    ("T_SISTER", "SISTER", "nun", "PINK", 1, "TEACHER", F),
    ("T_DRIFTER", "DRIFTER", "beggar", "BROWN", 1, "POKEFANM", M),
    ("T_ENFORCER", "ENFORCER", "thug", "RED", 1, "BLACKBELT_T", M),
    ("T_BUSKER", "BUSKER", "punk", "BLUE", 1, "GUITARIST", M),
    ("T_ACCOUNTANT", "ACCOUNTANT", "suit", "BLUE", 1, "SCIENTIST", M),
    # bosses
    ("T_DEACON", "DEACON", "priest", "RED", 0, "SAGE", M),
    ("T_COPCHIEF", "COP CHIEF", "cop_chief", "BLUE", 0, "OFFICER", M),
    ("T_MONSIGNOR", "MONSIGNOR", "monsignor", "RED", 0, "MYSTICALMAN", M),
]
AREA_CLASSES["AREA2"] = [
    ("G_HIKER", "HIKER", "hiker", "BROWN", 4, "HIKER", M),
    ("G_SCOUT", "SCOUT", "kid_m", "GREEN", 3, "CAMPER", M),
    ("G_SPROUT", "SPROUT", "kid_f", "PINK", 3, "PICNICKER", F),
    ("G_URCHIN", "URCHIN", "kid_m", "BROWN", 2, "BUG_CATCHER", M),
    ("G_ANGLER", "ANGLER", "fisher", "BLUE", 2, "FISHER", M),
    ("G_FLOWERKID", "FLOWER CHILD", "hippie_f", "PINK", 2, "BEAUTY", F),
    ("G_ELDER", "ELDER", "elder_m", "BROWN", 2, "POKEFANM", M),
    ("G_GRANNY", "GRANNY", "elder_f", "RED", 2, "POKEFANF", F),
    ("G_SHAMAN", "SHAMAN", "shaman", "BROWN", 2, "SAGE", M),
    ("G_DRUIDESS", "DRUIDESS", "hippie_f", "GREEN", 2, "KIMONO_GIRL", F),
    ("G_NATURISTM", "NATURIST", "bather_m", "BLUE", 2, "SWIMMERM", M),
    ("G_NATURISTF", "NATURIST", "bather_f", "PINK", 2, "SWIMMERF", F),
    ("G_DRUMMER", "DRUMMER", "hippie_m", "BROWN", 1, "BLACKBELT_T", M),
    ("G_BARD", "BARD", "hippie_m", "GREEN", 2, "GUITARIST", M),
    ("G_FORAGER", "FORAGER", "forager", "BLUE", 1, "SUPER_NERD", M),
    ("G_BIRDER", "BIRDER", "birder", "GREEN", 2, "BIRD_KEEPER", M),
    # bosses
    ("G_REEVE", "REEVE", "fisher", "BLUE", 0, "FISHER", M),
    ("G_ELDRESS", "ELDRESS", "elder_f", "GREEN", 0, "SAGE", F),
    ("G_MATRIARCH", "MATRIARCH", "matriarch", "RED", 0, "MEDIUM", F),
]
AREA_CLASSES["AREA3"] = [
    ("U_DOCTOR", "DOCTOR", "doc", "PINK", 3, "SCIENTIST", M),
    ("U_BOT", "SERVO BOT", "bot", "BLUE", 3, "GRUNTM", M),
    ("U_DRONE", "DRONE", "bot_drone", "BLUE", 2, "GRUNTF", F),
    ("U_BOTCOP", "BOT COP", "bot_cop", "BLUE", 3, "OFFICER", M),
    ("U_EXEC", "EXECUTIVE", "bot_exec", "BROWN", 1, "EXECUTIVEM", M),
    ("U_MATCHMAKER", "MATCHMAKER", "matchmaker", "PINK", 1, "EXECUTIVEF", F),
    ("U_SERF", "SERF", "serf", "GREEN", 2, "SUPER_NERD", M),
    ("U_GUARD", "GUARD", "guard", "BROWN", 2, "COOLTRAINERM", M),
    ("U_SERFF", "SERF", "serf_f", "GREEN", 2, "COOLTRAINERF", F),
    ("U_CASEWORKER", "CASEWORKER", "matchmaker", "GREEN", 1, "TEACHER", F),
    ("U_WARDBOT", "WARDEN BOT", "bot_warden", "BROWN", 2, "BLACKBELT_T", M),
    ("U_MADDOC", "MAD DOCTOR", "doc_mad", "PINK", 1, "GUITARIST", M),
    ("U_COURIER", "COURIER", "bot_drone", "BROWN", 1, "BIKER", M),
    # bosses
    ("U_MAYOR", "MAYOR BOT", "bot_mayor", "BROWN", 0, "EXECUTIVEM", M),
]
AREA_CLASSES["AREA4"] = [
    ("L_SUNBATHER", "SUNBATHER", "sunbather", "PINK", 4, "BEAUTY", F),
    ("L_SWIMMERM", "SWIMMER", "swimmer_m", "BLUE", 4, "SWIMMERM", M),
    ("L_SWIMMERF", "SWIMMER", "swimmer_f", "PINK", 4, "SWIMMERF", F),
    ("L_SAILOR", "SAILOR", "sailor", "BLUE", 2, "SAILOR", M),
    ("L_MANAGER", "MANAGER", "resort_boss", "BROWN", 2, "GENTLEMAN", M),
    ("L_TOURISTF", "TOURIST", "tourist_f", "PINK", 2, "LASS", F),
    ("L_BEACHBUM", "BEACH BUM", "beach_bum", "RED", 2, "GUITARIST", M),
    ("L_LIFEGUARD", "LIFEGUARD", "lifeguard", "BLUE", 2, "FISHER", M),
    ("L_FORGOTTEN", "FORGOTTEN", "forgotten", "BROWN", 2, "SAGE", M),
    ("L_CLINICIAN", "CLINICIAN", "clinician", "GREEN", 2, "SCIENTIST", F),
    ("L_WAITER", "WAITER", "waiter", "GREEN", 1, "TEACHER", M),
    ("L_TOURISTG", "TOURIST", "tourist_f", "GREEN", 2, "COOLTRAINERF", F),
    ("L_TOURISTM", "TOURIST", "tourist_m", "RED", 2, "COOLTRAINERM", M),
    ("L_BELLHOP", "BELLHOP", "waiter", "BROWN", 2, "BURGLAR", M),
    ("L_LOUNGER", "LOUNGER", "beach_bum", "BROWN", 2, "GRUNTM", M),
]
AREA_CLASSES["AREA5"] = [
    ("D_BRUTE", "BRUTE", "brute", "BLUE", 2, "BLACKBELT_T", M),
    ("D_SHADE", "SHADE", "shade", "GREEN", 3, "PSYCHIC_T", M),
    ("D_HAG", "HAG", "witch", "PINK", 2, "MEDIUM", F),
    ("D_JUDGE", "JUDGE", "judge", "BROWN", 2, "SAGE", M),
    ("D_IMP", "IMP", "imp", "BLUE", 2, "BURGLAR", M),
    ("D_FIREEATER", "FIRE EATER", "firebreather", "PINK", 2, "FIREBREATHER", M),
    ("D_JESTER", "JESTER", "jester", "RED", 2, "JUGGLER", M),
    ("D_WARDEN", "WARDEN", "warden", "BROWN", 2, "GRUNTM", M),
    ("D_IMPF", "IMP", "imp", "PINK", 2, "GRUNTF", F),
    ("D_DAMNED", "DAMNED", "damned", "BROWN", 1, "SCIENTIST", M),
    ("D_MAGISTRATE", "MAGISTRATE", "judge", "GREEN", 1, "GENTLEMAN", M),
    ("D_CRONE", "CRONE", "witch", "GREEN", 1, "BEAUTY", F),
    ("D_SINNER", "SINNER", "damned", "GREEN", 2, "POKEFANM", M),
    ("D_BRAWLER", "BRAWLER", "brute", "BROWN", 2, "BIKER", M),
    ("D_IMPB", "IMP", "imp", "BROWN", 1, "COOLTRAINERM", M),
    ("D_SPECTRE", "SPECTRE", "shade", "BROWN", 1, "COOLTRAINERF", F),
    # bosses
    ("D_DEMON", "DEMON LORD", "demon_lord", "BLUE", 0, "BURGLAR", M),
    ("D_FINNEGAN", "FINNEGAN", "finnegan", "BLUE", 0, "MYSTICALMAN", M),
]

ALL = [(a, c) for a, lst in AREA_CLASSES.items() for c in lst]


def sprite(slug):
    return "SPRITE_HC_" + slug.upper()


def area_mix(area):
    """The (class, sprite, palette, count) tuples of the random trainer mix of one area (bosses excluded)."""
    return [(c[0], sprite(c[2]), "PAL_NPC_" + c[3], c[4]) for c in AREA_CLASSES[area] if c[4]]


def by_const(const):
    for a, c in ALL:
        if c[0] == const:
            return a, c
    raise KeyError(const)
