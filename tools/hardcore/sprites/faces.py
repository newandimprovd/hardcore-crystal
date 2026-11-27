"""Moods and growth of the generated creatures.

MOOD gives every species the look in its eyes (see rig.eye): angry (brow slanted toward the nose), sly (narrow, smug), tired (heavy lids and a bag
under the eye), round (wide, startled, a pin prick pupil), addled (cross eyed, no lid), blank (white and lifeless), hollow (black sockets).
SCAR marks the veterans, who get a white scar across the brow.  GROWTH scales the picture of a species by its place in its line.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

MOOD = dict(
    TYPHONEUS="angry", EMBERWYRM="angry", HELLHOUND="angry", KINGCOBRA="sly", BEEHEMOTH="round", CARCINIZE="sly", APPARITION="blank",
    RAVENOUS="angry", WYRMKING="tired", MONOLITH="blank", TITANFIST="angry", SKYSCRAPER="blank", GATEHOUND="angry", DREADSTEED="round",
    ELDERWOOD="tired", CALDERA="angry", DEATHROLL="sly", OVERGROWN="tired", IRONCLAD="angry", SENTINEL="round", PANOPTICON="round",
    PROFESSOWL="tired", EMERITUS="tired", PLAGUERAT="round", RATKING="angry", CINDERWING="round", CANDLEMOTH="addled", PYREMOTH="blank",
    DANDELION="addled", DREADBEAK="angry", DOOMTALON="angry", BASILISK="sly", MEGAWATT="round", MOONQUEEN="sly", SOPORIFIC="tired",
    PLACEBO="addled", HOSPICE="tired", MATRIARCH="angry", TYRANT="angry", NOSFERATU="sly", BELLADONNA="sly", MAWBLOOM="round",
    CORDYCEPS="blank", SPOREKING="blank", SILKFANG="sly", WEBWEAVER="sly", ALLEYCAT="sly", KINGPIN="tired", MIGRAINE="addled",
    ANEURYSM="round", BERSERKER="angry", ANGERILLA="angry", OMNISCIENT="blank", ADAMANTIX="angry", KITSUNE="sly", FOXFIRE="sly",
    UNICORN="round", HELLBOUND="angry", PERDITION="sly", BLACKSHEEP="tired", MAGNETRON="round", SOLENOID="round", MAINFRAME="blank",
    ALGORITHM="blank", BONEKEEPER="hollow", OSSUARY="hollow", SLUDGELORD="addled", SUPERFUND="addled", MIASMA="addled", PANDEMIC="round",
    WARHORN="angry", BEHEMOTH="angry", CLEAVER="angry", HEADSMAN="tired", POLIWRAITH="addled", AMNESIAC="addled", OBLIVION="blank",
    TUSKDRIFT="tired", FROSTSIREN="sly", CRYOCLAM="round", ABYSSHELL="blank", CARAPACE="angry", NEBULON="blank", SUPERNOVA="round",
    MAELDRA="sly", RAGECARP="angry", WORLDEATER="angry", TIDEBELLY="addled", BEACHBALL="addled", NARCOLEPT="tired", SANDMAN="tired",
    MAMMOTH="tired", ICEAGE="angry", FROSTBITE="sly", RIMEQUEEN="sly",
)
SCAR = {"KINGPIN", "BERSERKER", "HEADSMAN", "TYRANT", "RATKING", "BASILISK", "CALDERA", "DEATHROLL", "WARHORN", "ANGERILLA", "MATRIARCH"}
# eye size per species when the head would otherwise give a small eye
BIG_EYES = {"PLAGUERAT", "CINDERWING", "MEGAWATT", "ANEURYSM", "UNICORN", "DREADSTEED", "PANDEMIC", "CRYOCLAM", "SUPERNOVA", "MIGRAINE", "ALLEYCAT",
            "DANDELION", "PLACEBO", "AMNESIAC", "TIDEBELLY", "BEACHBALL", "SENTINEL"}

# the share of the canvas the silhouette fills, by stage: the stage 3 form of a line is a size down from its stage 4 form, and a stage 4 form is the
# biggest thing in its line, so a growing creature visibly grows (the vanilla forms before them are smaller still)
FILL_BY_STAGE = {3: 0.76, 4: 0.97}

_stage = None


def stage_of(name):
    global _stage
    if _stage is None:
        path = os.path.join(HERE, "..", "roster", "roster_out.json")
        try:
            _stage = {s["name"]: s["stage"] for s in json.load(open(path)) if s["new"]}
        except OSError:
            _stage = {}
    return _stage.get(name, 4)


def fill_for(fill, name):
    """The canvas share of `name`: the recipe's own fill scaled by the stage of the species."""
    if not name:
        return fill
    return fill * FILL_BY_STAGE.get(stage_of(name), 0.97) / 0.97


def apply(M, name):
    """Gives the faces of the built model M the mood, eye size and scar of species `name`."""
    if not name:
        return
    mood = MOOD.get(name)
    for f in ([M.face] if getattr(M, "face", None) else []) + list(getattr(M, "faces", []) or []):
        if mood and f.get("eye") != "hollow" or mood == "hollow":
            f["eye"] = mood
        if name in BIG_EYES:
            f["eye_size"] = 1.3
        if name in SCAR:
            f["scar"] = True


# Camera angle of the front picture for the creatures that share a body plan (the two legged ones above all), so their silhouettes differ: yaw turns
# the creature toward its left (positive) or right (negative), pitch looks down on it (positive) or up at it (negative).
VIEW = dict(
    MATRIARCH=(42, 6), TYRANT=(-36, -2), OBLIVION=(14, 10), NARCOLEPT=(-46, 8), SANDMAN=(52, 4), TIDEBELLY=(-22, 12), POLIWRAITH=(4, 2),
    AMNESIAC=(-52, 6), MONOLITH=(32, -4), SOPORIFIC=(-30, 8), MEGAWATT=(46, 4), MOONQUEEN=(-40, 2), OMNISCIENT=(0, -4), RIMEQUEEN=(36, 4),
    ANGERILLA=(-30, 4), BERSERKER=(40, 8), BLACKSHEEP=(-26, 6), CALDERA=(24, 2), WARHORN=(-34, 6), BEHEMOTH=(30, 10), CLEAVER=(-28, 4),
    HOSPICE=(-18, 8), PLACEBO=(34, 12), FROSTBITE=(-40, 6), ICEAGE=(26, 8), UNICORN=(-32, 4), HEADSMAN=(20, 2), ELDERWOOD=(-28, 4),
    OVERGROWN=(30, 6), DEATHROLL=(-34, 6), PERDITION=(36, 4), KITSUNE=(-34, 4), FOXFIRE=(30, 4), ALLEYCAT=(-34, 6), KINGPIN=(30, 6),
    GATEHOUND=(-30, 4), HELLBOUND=(34, 4), RATKING=(-28, 6), PLAGUERAT=(28, 6), MAMMOTH=(-30, 6), TUSKDRIFT=(32, 6),
)

# How the mood changes the stance: added to the forward lean of two legged creatures (degrees), to the neck rise of four legged ones.
LEAN = dict(tired=10, angry=6, sly=4, round=-6, addled=8, blank=-2, hollow=0)
RISE = dict(tired=-0.16, angry=-0.06, sly=-0.02, round=0.12, addled=-0.1, blank=0.0, hollow=0.0)


def posture(plan, params, name):
    """The params of species `name` with the stance of its mood applied."""
    mood = MOOD.get(name)
    if not mood or name == "TYPHONEUS":
        return params
    p = dict(params)
    if plan == "biped":
        p["hunch"] = p.get("hunch", 0) + LEAN.get(mood, 0)
    elif plan == "quad":
        p["rise"] = p.get("rise", 0.5) + RISE.get(mood, 0.0)
    return p
