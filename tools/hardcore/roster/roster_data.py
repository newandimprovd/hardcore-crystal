"""Hardcore Crystal roster: 62 four-stage lines, 248 species, 97 of them new.

Rules (see docs/Hardcore_Crystal_complete_idea.md, "Roster and evolution rules"):
  * every line has exactly four stages, evolving at levels 25, 50 and 75, no branching
  * all 27 vanilla three-stage lines get one new fourth form, 35 of the 58 vanilla two-stage lines
    are kept and get two new forms (27 + 70 = 97 new species), everything else is removed
  * the last form of every line gets +35 base HP, Dragonite and Tyranitar lines stay on top
  * target type counts: Poison 31 species, Fairy 24 species, more Dark/Ice/Dragon/Bug/Steel than
    vanilla, with Bug/Fire and Bug/Steel both present

This file is data only.  gen_roster.py turns it into assembly.
"""

# ---------------------------------------------------------------------------------------------
# Lines.  Entries are vanilla species constants, or "*NAME" for a new species defined in NEW.
# The three Johto starters come first, which is also the Pokedex order.
# ---------------------------------------------------------------------------------------------
LINES = [
    ("CHIKORITA", ["CHIKORITA", "BAYLEEF", "MEGANIUM", "*ELDERWOOD"]),
    ("CYNDAQUIL", ["CYNDAQUIL", "QUILAVA", "TYPHLOSION", "*CALDERA"]),
    ("TOTODILE", ["TOTODILE", "CROCONAW", "FERALIGATR", "*DEATHROLL"]),
    ("BULBASAUR", ["BULBASAUR", "IVYSAUR", "VENUSAUR", "*OVERGROWN"]),
    ("CHARMANDER", ["CHARMANDER", "CHARMELEON", "CHARIZARD", "*EMBERWYRM"]),
    ("SQUIRTLE", ["SQUIRTLE", "WARTORTLE", "BLASTOISE", "*IRONCLAD"]),
    ("SENTRET", ["SENTRET", "FURRET", "*SENTINEL", "*PANOPTICON"]),
    ("HOOTHOOT", ["HOOTHOOT", "NOCTOWL", "*PROFESSOWL", "*EMERITUS"]),
    ("RATTATA", ["RATTATA", "RATICATE", "*PLAGUERAT", "*RATKING"]),
    ("PIDGEY", ["PIDGEY", "PIDGEOTTO", "PIDGEOT", "*RAVENOUS"]),
    ("CATERPIE", ["CATERPIE", "METAPOD", "BUTTERFREE", "*CINDERWING"]),
    ("WEEDLE", ["WEEDLE", "KAKUNA", "BEEDRILL", "*BEEHEMOTH"]),
    ("HOPPIP", ["HOPPIP", "SKIPLOOM", "JUMPLUFF", "*DANDELION"]),
    ("SPEAROW", ["SPEAROW", "FEAROW", "*DREADBEAK", "*DOOMTALON"]),
    ("EKANS", ["EKANS", "ARBOK", "*KINGCOBRA", "*BASILISK"]),
    ("PICHU", ["PICHU", "PIKACHU", "RAICHU", "*MEGAWATT"]),
    ("CLEFFA", ["CLEFFA", "CLEFAIRY", "CLEFABLE", "*MOONQUEEN"]),
    ("IGGLYBUFF", ["IGGLYBUFF", "JIGGLYPUFF", "WIGGLYTUFF", "*SOPORIFIC"]),
    ("NIDORAN_F", ["NIDORAN_F", "NIDORINA", "NIDOQUEEN", "*MATRIARCH"]),
    ("NIDORAN_M", ["NIDORAN_M", "NIDORINO", "NIDOKING", "*TYRANT"]),
    ("ZUBAT", ["ZUBAT", "GOLBAT", "CROBAT", "*NOSFERATU"]),
    ("ODDISH", ["ODDISH", "GLOOM", "BELLOSSOM", "*BELLADONNA"]),
    ("BELLSPROUT", ["BELLSPROUT", "WEEPINBELL", "VICTREEBEL", "*MAWBLOOM"]),
    ("PARAS", ["PARAS", "PARASECT", "*CORDYCEPS", "*SPOREKING"]),
    ("VENONAT", ["VENONAT", "VENOMOTH", "*CANDLEMOTH", "*PYREMOTH"]),
    ("SPINARAK", ["SPINARAK", "ARIADOS", "*SILKFANG", "*WEBWEAVER"]),
    ("MEOWTH", ["MEOWTH", "PERSIAN", "*ALLEYCAT", "*KINGPIN"]),
    ("PSYDUCK", ["PSYDUCK", "GOLDUCK", "*MIGRAINE", "*ANEURYSM"]),
    ("MANKEY", ["MANKEY", "PRIMEAPE", "*BERSERKER", "*ANGERILLA"]),
    ("MACHOP", ["MACHOP", "MACHOKE", "MACHAMP", "*TITANFIST"]),
    ("ABRA", ["ABRA", "KADABRA", "ALAKAZAM", "*OMNISCIENT"]),
    ("GEODUDE", ["GEODUDE", "GRAVELER", "GOLEM", "*MONOLITH"]),
    ("ONIX", ["ONIX", "STEELIX", "*ADAMANTIX", "*SKYSCRAPER"]),
    ("GROWLITHE", ["GROWLITHE", "ARCANINE", "*HELLHOUND", "*GATEHOUND"]),
    ("VULPIX", ["VULPIX", "NINETALES", "*KITSUNE", "*FOXFIRE"]),
    ("PONYTA", ["PONYTA", "RAPIDASH", "*UNICORN", "*DREADSTEED"]),
    ("HOUNDOUR", ["HOUNDOUR", "HOUNDOOM", "*HELLBOUND", "*PERDITION"]),
    ("MAREEP", ["MAREEP", "FLAAFFY", "AMPHAROS", "*BLACKSHEEP"]),
    ("MAGNEMITE", ["MAGNEMITE", "MAGNETON", "*MAGNETRON", "*SOLENOID"]),
    ("PORYGON", ["PORYGON", "PORYGON2", "*MAINFRAME", "*ALGORITHM"]),
    ("GASTLY", ["GASTLY", "HAUNTER", "GENGAR", "*APPARITION"]),
    ("CUBONE", ["CUBONE", "MAROWAK", "*BONEKEEPER", "*OSSUARY"]),
    ("GRIMER", ["GRIMER", "MUK", "*SLUDGELORD", "*SUPERFUND"]),
    ("KOFFING", ["KOFFING", "WEEZING", "*MIASMA", "*PANDEMIC"]),
    ("RHYHORN", ["RHYHORN", "RHYDON", "*WARHORN", "*BEHEMOTH"]),
    ("SCYTHER", ["SCYTHER", "SCIZOR", "*CLEAVER", "*HEADSMAN"]),
    ("TENTACOOL", ["TENTACOOL", "TENTACRUEL", "*CTHUSPAWN", "*CTHULUDON"]),
    ("POLIWAG", ["POLIWAG", "POLIWHIRL", "POLIWRATH", "*POLIWRAITH"]),
    ("SLOWPOKE", ["SLOWPOKE", "SLOWBRO", "*AMNESIAC", "*OBLIVION"]),
    ("SEEL", ["SEEL", "DEWGONG", "*TUSKDRIFT", "*FROSTSIREN"]),
    ("SHELLDER", ["SHELLDER", "CLOYSTER", "*CRYOCLAM", "*ABYSSHELL"]),
    ("KRABBY", ["KRABBY", "KINGLER", "*CARAPACE", "*CARCINIZE"]),
    ("STARYU", ["STARYU", "STARMIE", "*NEBULON", "*SUPERNOVA"]),
    ("HORSEA", ["HORSEA", "SEADRA", "KINGDRA", "*MAELDRA"]),
    ("MAGIKARP", ["MAGIKARP", "GYARADOS", "*RAGECARP", "*WORLDEATER"]),
    ("MARILL", ["MARILL", "AZUMARILL", "*TIDEBELLY", "*BEACHBALL"]),
    ("DROWZEE", ["DROWZEE", "HYPNO", "*NARCOLEPT", "*SANDMAN"]),
    ("CHANSEY", ["CHANSEY", "BLISSEY", "*PLACEBO", "*HOSPICE"]),
    ("SWINUB", ["SWINUB", "PILOSWINE", "*MAMMOTH", "*ICEAGE"]),
    ("SMOOCHUM", ["SMOOCHUM", "JYNX", "*FROSTBITE", "*RIMEQUEEN"]),
    ("DRATINI", ["DRATINI", "DRAGONAIR", "DRAGONITE", "*WYRMKING"]),
    ("LARVITAR", ["LARVITAR", "PUPITAR", "TYRANITAR", "*CATACLYSM"]),
]

# Dragonite and Tyranitar lines stay the strongest by stats.
APEX_LINES = ("DRATINI", "LARVITAR")

# per-line stat options: s = overall scale (normal lines stay at or below 1.0 so finals never pass
# 600 including the +35 HP), s1 = stage 1 BST override for deliberately weak starts
LINE_OPT = {
    "MAGIKARP": {"s1": 200},
    "CATERPIE": {"s1": 230, "s": 0.96},
    "WEEDLE": {"s1": 230, "s": 0.96},
    "PIDGEY": {"s1": 270},
    "RATTATA": {"s1": 260},
    "SENTRET": {"s1": 250},
    "HOOTHOOT": {"s1": 260},
    "SPEAROW": {"s1": 265},
    "ZUBAT": {"s1": 260},
    "PICHU": {"s1": 250},
    "CLEFFA": {"s1": 250},
    "IGGLYBUFF": {"s1": 250},
    "HOPPIP": {"s1": 260},
    "SWINUB": {"s1": 270},
    "MARILL": {"s1": 265},
    "SPINARAK": {"s1": 270},
    "PORYGON": {"s": 0.96},
    "CHANSEY": {"s": 0.97},
    "SCYTHER": {"s": 0.98},
    "ONIX": {"s": 0.97},
}

# ---------------------------------------------------------------------------------------------
# Type changes for vanilla species that stay (everything else keeps its vanilla types).
# Poison is cut to 31 species, Fairy takes 24.
# ---------------------------------------------------------------------------------------------
TYPE_OVERRIDE = {
    # Poison removed from plants and ghosts
    "BULBASAUR": "GRASS", "IVYSAUR": "GRASS", "VENUSAUR": "GRASS",
    "ODDISH": "GRASS", "GLOOM": "GRASS",
    "BELLSPROUT": "GRASS", "WEEPINBELL": "GRASS", "VICTREEBEL": "GRASS",
    "GASTLY": "GHOST", "HAUNTER": "GHOST", "GENGAR": "GHOST",
    "VENONAT": "BUG", "VENOMOTH": "BUG",
    "CROBAT": "DARK/FLYING",
    # Fairy
    "CLEFFA": "FAIRY", "CLEFAIRY": "FAIRY", "CLEFABLE": "FAIRY",
    "IGGLYBUFF": "NORMAL/FAIRY", "JIGGLYPUFF": "NORMAL/FAIRY", "WIGGLYTUFF": "NORMAL/FAIRY",
    "CHANSEY": "FAIRY", "BLISSEY": "FAIRY",
    "MARILL": "WATER/FAIRY", "AZUMARILL": "WATER/FAIRY",
    # a little more Dark, Ice, Dragon, Steel
    "RATICATE": "NORMAL/DARK",
    "PERSIAN": "NORMAL/DARK",
    "FEAROW": "FLYING/DARK",
    "MAGIKARP": "WATER",
    "SCYTHER": "BUG/FLYING",
}

# ---------------------------------------------------------------------------------------------
# New species.  Fields:
#   types  "A/B" or "A"          cat  dex category (<= 10 chars)
#   ht     feet'inches           wt   pounds
#   text   dex text, wrapped to 18 columns, at most 6 lines
#   src    vanilla species whose sprite/animation/footprint/icon/cry are reused (default: the
#          previous stage of the line)
#   arch   stat archetype        pal  optional ((r,g,b),(r,g,b)) override of the two palette colors
# ---------------------------------------------------------------------------------------------
NEW = {}


def N(name, types, cat, ht, wt, text, src=None, arch="bal", pal=None, icon=None, art=None, shiny=None):
    """art: name of a tools/hardcore/sprites module that draws this species (own front/back sprite).
    pal and shiny are two 5-bit RGB colours each (body, accent); shiny defaults to a channel rotation."""
    assert name not in NEW, name
    NEW[name] = dict(name=name, types=types, cat=cat, ht=ht, wt=wt, text=text, src=src, arch=arch, pal=pal, icon=icon,
                     art=art, shiny=shiny)


# --- three-stage lines, one new final form each -------------------------------------------------
N("ELDERWOOD", "GRASS/GHOST", "ANCIENT", "11'10", 2200,
  "A forest wearing a MEGANIUM. Every ring in its trunk is a missing person.", arch="tank")
N("CALDERA", "FIRE/DARK", "CRATER", "8'06", 520,
  "Its back is a volcano with a gift shop. The gift shop is also on fire.", arch="spec")
N("DEATHROLL", "WATER/DARK", "ROLLER", "11'02", 1100,
  "It rolls prey until they confess. The confession is usually bubbles.", arch="phys")
N("OVERGROWN", "GRASS/DARK", "LANDLORD", "8'10", 380,
  "Its flower holds three mortgages. It evicts anything that stands in the sun.", arch="tank")
N("EMBERWYRM", "FIRE/DRAGON", "WYRM", "9'06", 420,
  "CHARIZARD was never enough. This one burns the sky and then bills it.", arch="phys")
N("IRONCLAD", "WATER/STEEL", "BATTLESHIP", "7'10", 1100,
  "It fires cannons at anything wet. Its shell was fined for noise.", arch="tank")
N("SENTINEL", "NORMAL", "LOOKOUT", "4'03", 85,
  "It stands on its tail and reports everything. Most of its reports are lies.", arch="fast")
N("PANOPTICON", "NORMAL/DARK", "WATCHER", "6'03", 140,
  "It watches every corner and never blinks. You will behave. You always do.", arch="wall")
N("PROFESSOWL", "FLYING/PSYCHIC", "TENURED", "4'11", 110,
  "It hoots in lectures that cost forty thousand a year.", arch="spec")
N("EMERITUS", "FLYING/PSYCHIC", "SAGE", "6'07", 135,
  "Retired decades ago. Still lectures. Still unpaid. Still right.", arch="spec")
N("PLAGUERAT", "NORMAL/DARK", "SEWER", "2'11", 40,
  "It carries every disease in the city and shares generously.", arch="fast")
N("RATKING", "DARK", "COLONY", "4'07", 190,
  "Many tails are tied in one knot. They vote. The vote is always bite.", arch="phys")
N("RAVENOUS", "FLYING/DARK", "CARRION", "5'09", 70,
  "It follows trainers for miles. It is not curious. It is early.", arch="fast")
N("CINDERWING", "BUG/FIRE", "EMBER", "5'11", 66,
  "Its wings drop burning dust. Cities call it the Great Moth Fire.", arch="spec")
N("BEEHEMOTH", "BUG/POISON", "HORNET", "6'03", 310,
  "A hive that learned to walk. One sting and the whole county sues.", arch="phys")
N("DANDELION", "GRASS/FAIRY", "SEEDWISH", "2'11", 4,
  "Blow once and make a wish. It grants one, with fine print.", arch="fast")
N("DREADBEAK", "FLYING/DARK", "BEAK", "4'11", 51,
  "Its beak has opinions about your face. They are not kind.", arch="fast")
N("DOOMTALON", "FLYING/DARK", "TALON", "6'03", 90,
  "It circles quietly above the road and files paperwork on your last steps.", arch="phys")
N("KINGCOBRA", "POISON/DARK", "HOODED", "12'02", 150,
  "Its hood flares with pride. It has no idea what the hood is for.", arch="phys")
N("BASILISK", "POISON/DRAGON", "GAZE", "22'11", 700,
  "One look petrifies. It wears sunglasses at work out of courtesy.", arch="spec")
N("MEGAWATT", "ELECTRIC", "GRIDLOCK", "4'03", 90,
  "It is the reason your city has rolling blackouts. It likes the blackouts.", arch="fast")
N("MOONQUEEN", "FAIRY/PSYCHIC", "MOON", "5'10", 90,
  "It dances in moonlight and cancels meetings. Nations obey its calendar.", arch="spec")
N("SOPORIFIC", "FAIRY/NORMAL", "LULLABY", "4'07", 60,
  "Its lullaby ends wars, meetings and consciousness. Nobody remembers which came first.", arch="tank")
N("MATRIARCH", "GROUND/FAIRY", "BROOD", "7'07", 700,
  "She rules forty nests and two court cases. Her spikes are for emphasis.", arch="tank")
N("TYRANT", "GROUND/DARK", "DESPOT", "7'11", 640,
  "He has never lost an argument. The ones he lost were relabeled treason.", arch="phys")
N("NOSFERATU", "DARK/FLYING", "NIGHT", "6'07", 130,
  "Sleeps upside down in cathedrals. Drinks blood, leaves a nice review.", arch="fast")
N("BELLADONNA", "GRASS/POISON", "NIGHTSHADE", "4'11", 55,
  "Beautiful, deadly, and still on the florist's best seller list.", arch="spec")
N("MAWBLOOM", "GRASS/DARK", "DEVOURER", "7'02", 110,
  "Its mouth is a garden gate. Visitors are encouraged to stay forever.", arch="phys")
N("CORDYCEPS", "BUG/GHOST", "ZOMBIE", "3'05", 35,
  "The mushrooms steer it now. It has come to like the steering.", arch="bal")
N("SPOREKING", "BUG/GHOST", "SPORE", "4'11", 120,
  "A mushroom court with a crab for a horse. Everyone in it agrees. Everyone.", arch="tank")
N("CANDLEMOTH", "BUG/FIRE", "WAX", "4'03", 20,
  "Its wings melt like wax and drip on arsonists' shoes.", arch="spec")
N("PYREMOTH", "BUG/FIRE", "PYRE", "5'11", 75,
  "It dives into bonfires and leaves wearing the party hat.", arch="spec")
N("SILKFANG", "BUG/DARK", "SPINNER", "5'11", 70,
  "Its web has a login page. Flies keep signing up.", arch="phys")
N("WEBWEAVER", "BUG/DARK", "NETWORK", "8'02", 160,
  "The web it spins is the actual internet. Please stop asking why it's down.", arch="bal")
N("ALLEYCAT", "DARK", "STRAY", "3'11", 70,
  "It owns every alley. The rent is your wallet and your dignity.", arch="fast")
N("KINGPIN", "NORMAL/DARK", "BOSS", "5'03", 90,
  "The coin on its head is a bribe it forgot to spend. Its tail is legally a gang.", arch="fast")
N("MIGRAINE", "WATER/PSYCHIC", "HEADACHE", "5'11", 120,
  "The pain gives it power. The power gives everyone else pain.", arch="spec")
N("ANEURYSM", "PSYCHIC", "BURST", "6'07", 190,
  "It thinks too hard. Nearby clocks burst first. Then nearby thoughts.", arch="spec")
N("BERSERKER", "FIGHTING", "FURY", "6'03", 200,
  "It stopped calming down in 1999. It has not missed the calm.", arch="phys")
N("ANGERILLA", "FIGHTING/DARK", "RAGE", "7'11", 510,
  "Its rage has an angry agent and a rage lawyer. It beat both.", arch="phys")
N("TITANFIST", "FIGHTING/STEEL", "IRONARM", "9'02", 890,
  "Four arms of punishing steel. Its high five sounds like a car crash.", arch="phys")
N("OMNISCIENT", "PSYCHIC", "KNOW-ALL", "5'03", 120,
  "It knows everything and is exhausted. Do not ask about your future.", arch="spec")
N("MONOLITH", "ROCK/GROUND", "MONUMENT", "11'06", 6500,
  "It stands in fields until a cult arrives. Cults always arrive.", arch="wall")
N("ADAMANTIX", "STEEL/GROUND", "IRONSNAKE", "29'06", 2600,
  "A mining accident that kept growing.", arch="wall")
N("SKYSCRAPER", "STEEL/DRAGON", "TOWER", "48'03", 4400,
  "It stands taller than most banks. Birds avoid it, as do regulators.", arch="tank")
N("HELLHOUND", "FIRE/DARK", "HOUND", "6'03", 350,
  "A good dog. Sad that the good dog got set on fire.", arch="phys")
N("GATEHOUND", "FIRE/DARK", "GUARD", "9'10", 800,
  "Three heads, one leash. All three bark at the mailman and one bites.", arch="phys")
N("KITSUNE", "FIRE/FAIRY", "MANY-TAIL", "4'07", 90,
  "Its seven tails are for tricks. The eighth is for the bill.", arch="spec")
N("FOXFIRE", "FIRE/FAIRY", "SPIRIT", "5'07", 120,
  "Nine tails, nine lives, nine offshore accounts. It never pays tax.", arch="spec")
N("UNICORN", "FIRE/FAIRY", "RAINBOW", "5'11", 330,
  "Its horn is a glitter cannon. It insists you call it a unicorn.", arch="fast")
N("DREADSTEED", "FIRE/FAIRY", "NIGHT-STEED", "6'10", 380,
  "A pink horse on fire in the dark. It arrives when you close your eyes.", arch="phys")
N("HELLBOUND", "DARK/FIRE", "DAMNED", "4'11", 70,
  "It howls the future of others. The future is mostly smoke.", arch="spec")
N("PERDITION", "DARK/FIRE", "RUIN", "6'11", 260,
  "A loud pack of one. Where it walks, ash obeys.", arch="spec")
N("BLACKSHEEP", "ELECTRIC/DARK", "OUTCAST", "5'09", 180,
  "The flock shuns it. It shocks the flock anyway.", arch="spec")
N("MAGNETRON", "ELECTRIC/STEEL", "MAGNET", "4'07", 330,
  "Three magnets orbit one mood. The mood is attraction, plus fines.", arch="spec")
N("SOLENOID", "ELECTRIC/STEEL", "COIL", "6'03", 480,
  "Its field erases hard drives, credit cards and unfortunate haircuts.", arch="spec")
N("MAINFRAME", "NORMAL/STEEL", "DATA", "5'03", 230,
  "It runs on punch cards and old grudges.", arch="bal")
N("ALGORITHM", "PSYCHIC/STEEL", "FEED", "6'11", 300,
  "It decides what you see. It recommends more of itself.", arch="spec")
N("APPARITION", "GHOST/DARK", "HAUNT", "6'05", 9,
  "It sits on chests at 3 AM. It bills you for the heartbeat.", arch="spec")
N("BONEKEEPER", "GROUND/GHOST", "GRIEF", "5'03", 90,
  "It wears two skulls now. Both were fond of it.", arch="phys")
N("OSSUARY", "GROUND/GHOST", "CRYPT", "6'07", 140,
  "A bone pile that learned to fight. Its mother's skull still gives terrible advice.", arch="phys")
N("SLUDGELORD", "POISON/DARK", "WASTE", "5'11", 700,
  "It rules landfills like a duke. Taxes are plastic and unspeakable.", arch="tank")
N("SUPERFUND", "POISON", "TOXIC SITE", "9'10", 1500,
  "A cleanup site that cleans up nothing. The lawsuits are still evolving.", arch="tank")
N("MIASMA", "POISON/GHOST", "STENCH", "4'11", 25,
  "It hangs in the air and lowers property values.", arch="spec")
N("PANDEMIC", "POISON/DARK", "OUTBREAK", "6'03", 55,
  "It spreads fast and quietly. Officials call it unprecedented.", arch="spec")
N("WARHORN", "GROUND/ROCK", "BULLDOZER", "7'07", 1100,
  "Charges the way a bad idea does. Straight, fast and into the wall.", arch="phys")
N("BEHEMOTH", "GROUND/STEEL", "JUGGERNAUT", "11'10", 2800,
  "A tank that grew a personality. The personality is mostly horn.", arch="tank")
N("CLEAVER", "BUG/STEEL", "BLADE", "6'11", 260,
  "Both arms are cleavers. Both arms are also in a union.", arch="phys")
N("HEADSMAN", "BUG/STEEL", "EXECUTOR", "8'02", 310,
  "It does not take sides. It takes heads, with a polite bow.", arch="phys")
N("CTHUSPAWN", "DARK/POISON", "ABYSS", "8'02", 360,
  "Dived too deep. The dark and the pressure gave it a familiar face.", arch="spec",
  art="cthu", pal=((11, 21, 16), (28, 3, 6)), shiny=((17, 12, 21), (30, 25, 5)))
N("CTHULUDON", "DARK/POISON", "SLEEPER", "14'09", 1850,
  "It dreams of dying cities. Two red gems glow where its thoughts leak out.", arch="spec",
  art="cthu", pal=((9, 18, 17), (25, 3, 10)), shiny=((12, 8, 18), (31, 24, 4)))
N("POLIWRAITH", "WATER/GHOST", "WHIRL", "6'03", 480,
  "The swirl on its belly is a drain. It leads somewhere cold.", arch="phys")
N("AMNESIAC", "WATER/PSYCHIC", "FORGETFUL", "7'11", 460,
  "It forgot its name, its evolution and the reason for its tail.", arch="tank")
N("OBLIVION", "PSYCHIC/DARK", "VOID", "9'02", 600,
  "It forgot everything and was much happier. Doctors are furious.", arch="spec")
N("TUSKDRIFT", "WATER/ICE", "FLOE", "7'10", 540,
  "It naps on ice floes and floats away. It calls that a vacation.", arch="tank")
N("FROSTSIREN", "ICE/FAIRY", "SIREN", "8'11", 600,
  "It sings of warm beaches to icebergs. The ships believe it.", arch="spec")
N("CRYOCLAM", "WATER/ICE", "FREEZER", "4'11", 400,
  "It stores things inside for later. The things are bigger than the shell.", arch="wall")
N("ABYSSHELL", "ICE/DARK", "TRENCH", "6'07", 900,
  "At the bottom of the sea its pearl reflects a face. The face is wrong.", arch="wall")
N("CARAPACE", "WATER/ROCK", "SHELL", "4'11", 190,
  "It added rocks to its shell. Rocks do not mind.", arch="wall")
N("CARCINIZE", "WATER/STEEL", "INEVITABLE", "5'11", 330,
  "Everything becomes a crab eventually. This one just got there first.", arch="phys")
N("NEBULON", "WATER/PSYCHIC", "STARDUST", "3'11", 180,
  "Its core blinks at night. It is asking for help or ordering takeout.", arch="spec")
N("SUPERNOVA", "PSYCHIC/FIRE", "BLAST", "5'03", 330,
  "It outshines its own funeral and will outlive it.", arch="spec")
N("MAELDRA", "WATER/DRAGON", "WHIRLPOOL", "12'02", 520,
  "A dragon the size of a harbor. It prefers to be called weather.", arch="spec")
N("RAGECARP", "WATER/DRAGON", "FURY", "15'01", 1100,
  "It is still a fish and it is furious about it.", arch="phys")
N("WORLDEATER", "WATER/DRAGON", "TSUNAMI", "59'01", 6000,
  "It ate the ocean and then complained about the portion size.", arch="phys")
N("TIDEBELLY", "WATER/FAIRY", "WAVE", "3'11", 120,
  "It rides every tide at the beach. Lifeguards stopped being surprised.", arch="bal")
N("BEACHBALL", "WATER/FAIRY", "BOUNCE", "5'03", 250,
  "It bounces over the pier at sunset. Everyone cheers. No one asks why.", arch="tank")
N("NARCOLEPT", "PSYCHIC", "NAPPER", "5'11", 160,
  "It falls asleep mid-sentence and wakes up with your dreams.", arch="spec")
N("SANDMAN", "PSYCHIC/DARK", "DREAM", "6'11", 200,
  "Its pendulum sells dreams in bulk. The refund policy is nightmares.", arch="spec")
N("PLACEBO", "FAIRY", "SUGAR PILL", "5'11", 70,
  "Eat its egg and feel better. Do not check the lab results.", arch="wall")
N("HOSPICE", "FAIRY/GHOST", "COMFORT", "6'07", 130,
  "It tucks the dying in and says they look great. They always believe it.", arch="wall")
N("MAMMOTH", "ICE/GROUND", "TUSKER", "8'02", 800,
  "Frozen for ten thousand years and still unemployed.", arch="phys")
N("ICEAGE", "ICE/GROUND", "GLACIAL", "11'06", 1900,
  "Its steps start glaciers. Climate scientists keep it on speed dial.", arch="tank")
N("FROSTBITE", "ICE/PSYCHIC", "KISS", "4'11", 110,
  "Its kisses numb lips and ex-lovers. The ex-lovers recover slower.", arch="spec")
N("RIMEQUEEN", "ICE/FAIRY", "WINTER", "6'03", 160,
  "Rules a kingdom of frost with perfect posture. Her subjects are statues now.", arch="spec")
N("WYRMKING", "DRAGON/FLYING", "SOVEREIGN", "13'01", 850,
  "DRAGONITE once delivered mail. This one delivers verdicts. The weather agrees.", arch="bal")
N("CATACLYSM", "ROCK/DARK", "COLLAPSE", "11'02", 2800,
  "An earthquake with a pulse. Maps are redrawn after it naps.", arch="phys")

assert len(NEW) == 97, len(NEW)

# every new species must be listed in exactly one line
_used = [s[1:] for _, st in LINES for s in st if s.startswith("*")]
assert sorted(_used) == sorted(NEW), set(NEW) ^ set(_used)
assert len(LINES) == 62

# ---------------------------------------------------------------------------------------------
# Removed vanilla names.  Data that still mentions them (vanilla maps, trainers, scripts) must
# keep assembling, so each name becomes an alias.  Names the engine special-cases are parked on an
# impossible species ID so the special code can never match a real species.
# ---------------------------------------------------------------------------------------------
PARKED = ["UNOWN", "DITTO", "FARFETCH_D", "MEW", "MEWTWO", "LUGIA", "HO_OH", "CELEBI", "TOGEPI", "SHUCKLE"]
ALIAS = {
    "SANDSHREW": "RATTATA", "SANDSLASH": "RATICATE", "VILEPLUME": "BELLOSSOM", "DIGLETT": "CUBONE",
    "DUGTRIO": "MAROWAK", "DODUO": "SPEAROW", "DODRIO": "FEAROW", "VOLTORB": "MAGNEMITE",
    "ELECTRODE": "MAGNETON", "EXEGGCUTE": "ODDISH", "EXEGGUTOR": "BELLOSSOM", "HITMONLEE": "MACHOKE",
    "HITMONCHAN": "MACHOKE", "LICKITUNG": "PORYGON", "TANGELA": "BELLSPROUT", "KANGASKHAN": "RHYDON",
    "GOLDEEN": "MAGIKARP", "SEAKING": "GYARADOS", "MR__MIME": "ABRA", "ELECTABUZZ": "RAICHU",
    "MAGMAR": "HOUNDOOM", "PINSIR": "SCYTHER", "TAUROS": "RHYDON", "LAPRAS": "DEWGONG",
    "EEVEE": "MEOWTH", "VAPOREON": "PERSIAN", "JOLTEON": "PERSIAN", "FLAREON": "PERSIAN",
    "OMANYTE": "SHELLDER", "OMASTAR": "CLOYSTER", "KABUTO": "KRABBY", "KABUTOPS": "KINGLER",
    "AERODACTYL": "PIDGEOT", "SNORLAX": "CHANSEY", "ARTICUNO": "PIDGEOT", "ZAPDOS": "PIDGEOT",
    "MOLTRES": "PIDGEOT", "LEDYBA": "CATERPIE", "LEDIAN": "BUTTERFREE", "CHINCHOU": "TENTACOOL",
    "LANTURN": "TENTACRUEL", "TOGETIC": "CLEFAIRY", "NATU": "HOOTHOOT", "XATU": "NOCTOWL",
    "SUDOWOODO": "GEODUDE", "POLITOED": "POLIWHIRL", "AIPOM": "MANKEY", "SUNKERN": "HOPPIP",
    "SUNFLORA": "JUMPLUFF", "YANMA": "BUTTERFREE", "WOOPER": "MARILL", "QUAGSIRE": "AZUMARILL",
    "ESPEON": "PERSIAN", "UMBREON": "PERSIAN", "MURKROW": "HOOTHOOT", "SLOWKING": "SLOWBRO",
    "MISDREAVUS": "GASTLY", "WOBBUFFET": "SLOWPOKE", "GIRAFARIG": "PONYTA", "PINECO": "CATERPIE",
    "FORRETRESS": "SCIZOR", "DUNSPARCE": "SENTRET", "GLIGAR": "ZUBAT", "SNUBBULL": "JIGGLYPUFF",
    "GRANBULL": "WIGGLYTUFF", "QWILFISH": "MAGIKARP", "HERACROSS": "SCYTHER", "SNEASEL": "MEOWTH",
    "TEDDIURSA": "MANKEY", "URSARING": "PRIMEAPE", "SLUGMA": "VULPIX", "MAGCARGO": "NINETALES",
    "CORSOLA": "STARYU", "REMORAID": "KRABBY", "OCTILLERY": "KINGLER", "DELIBIRD": "HOOTHOOT",
    "MANTINE": "GYARADOS", "SKARMORY": "PIDGEOT", "PHANPY": "CUBONE", "DONPHAN": "MAROWAK",
    "STANTLER": "PONYTA", "SMEARGLE": "RATTATA", "TYROGUE": "MACHOP", "HITMONTOP": "MACHOKE",
    "ELEKID": "PICHU", "MAGBY": "CHARMANDER", "MILTANK": "RHYDON", "RAIKOU": "PIKACHU",
    "ENTEI": "ARCANINE", "SUICUNE": "DEWGONG",
}
