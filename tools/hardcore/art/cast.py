"""The cast of original overworld characters: slug -> recipe (see npcs.py).  Slugs become SPRITE_HC_<SLUG> in the game.

Colors are indices (1 skin, 2 cloth, 3 dark); the real colors come from the NPC palette slot the object uses (areapal.py).
Palette slot per character is chosen in areas/aN.py when the character is used."""
from collections import OrderedDict

from npcs import recipe as R

CAST = OrderedDict()


def add(slug, **kw):
    CAST[slug] = R(**kw)


# ---------------------------------------------------------------------------------------------------- Area 1: Tithe City
add("cop", hat="cap", torso="shirt", legsc="D", extra=("badge", "belt"))
add("cop_chief", hat="cap", torso="shirt", legsc="D", width=1, face="tired", extra=("badge", "belt"))
add("priest", hair="short", hat="zuc", torso="robe", legs="robe", extra=("collar", "buttons", "hem"))
add("bishop", hair="bald", hat="mitre", torso="robe", legs="robe", extra=("staff", "cross", "hem"))
add("monsignor", hair="bald", hat="mitre", torso="robe", legs="robe", width=1, extra=("chain", "cross", "hem"))
add("suit", hat="bowler", torso="coat", legsc="D", extra=("tie", "monocle"))
add("suit_f", hair="bun", torso="dress", legs="robe", extra=("glasses",))
add("hoodie", hat="hood", torso="shirt", face="tired", extra=("bag",))
add("nun", hat="wimple", hatc="D", torso="habit", legs="robe", extra=("cross", "hem"))
add("punk", hair="mohawk", hairc="C", torso="shirt", torsoc="D", armc="D", legs="pants", legsc="C", face="angry", extra=("spikes",))
add("beggar", hat="hood", hatc="D", torso="shirt", face="tired", extra=("bag",), bagc="C")
add("choir", hair="short", torso="robe", legs="robe", extra=("sash",), sashc="S")
add("thug", hat="bandana", torso="shirt", torsoc="D", armc="D", legs="pants", legsc="C", face="angry", extra=("chain",))

# ---------------------------------------------------------------------------------------------------- Area 2: the Grove
add("hippie_m", hair="long", hat="crown", torso="bare", legs="shorts", legsc="C", face="grin", extra=("beard",))
add("hippie_f", hair="long", hat="crown", torso="dress", legs="robe")
add("elder_m", hair="bald", torso="robe", legs="robe", extra=("whisker_hair", "staff"), beardc="C")
add("elder_f", hair="bun", hairc="C", torso="dress", legs="robe", extra=("glasses",))
add("shaman", hair="long", hat="antlers", hatc="D", torso="bare", legs="shorts", legsc="C", face="angry", extra=("staff", "sash"))
add("forager", hair="bushy", torso="bare", legs="shorts", legsc="C", extra=("bag",))
add("fisher", hat="sunhat", torso="shirt", legsc="D", extra=("rod",))
add("hiker", hat="cap", torso="shirt", legsc="D", extra=("bag",), bagc="C")
add("kid_f", hair="pigtails", torso="dress", legs="robe")
add("kid_m", hat="bandana", torso="shirt", legsc="C", legs="shorts", face="grin")
add("birder", hat="visor", torso="shirt", legsc="D", extra=("glasses", "bag"))
add("matriarch", hair="long", hat="crownk", hatc="S", torso="dress", legs="robe", extra=("staff",))
add("bather_m", hair="short", torso="bare", legs="shorts", legsc="C")
add("bather_f", hair="long", torso="swim", legs="shorts", legsc="C")

# ---------------------------------------------------------------------------------------------------- Area 3: the Union
add("bot", hair="bald", hat="helmet", torso="armor", legs="treads", face="none", extra=("visor", "antenna"), skinc=1)
add("bot_cop", hair="bald", hat="cap", torso="armor", legs="treads", face="none", extra=("visor", "badge"), skinc=1)
add("bot_exec", hair="bald", hat="tophat", torso="coat", legs="treads", face="none", extra=("visor", "tie"), skinc=1)
add("bot_drone", hair="bald", hat="antenna", torso="shirt", legs="hover", face="none", extra=("visor",), skinc=1)
add("bot_mayor", hair="bald", hat="tophat", torso="coat", legs="treads", width=1, face="none", extra=("visor", "tie", "chain"), skinc=1)
add("bot_warden", hair="bald", hat="helmet+horns", torso="armor", legs="treads", width=1, face="none", extra=("visor", "spikes"), skinc=1)
add("serf", hair="bald", torso="shirt", legsc="D", face="tired", extra=("number",))
add("serf_f", hair="bun", torso="dress", legs="robe", face="tired", extra=("number",))
add("doc", hair="short", torso="coat", legsc="D", extra=("glasses",))
add("doc_mad", hair="bushy", torso="coat", legsc="D", extra=("goggles",))
add("guard", hat="helmet", torso="armor", legsc="D", face="angry", extra=("belt",))
add("matchmaker", hair="bun", torso="dress", legs="robe", extra=("glasses", "chain"))

# ---------------------------------------------------------------------------------------------------- Area 4: the Lotus Coast
add("tourist_m", hat="visor", torso="shirt", legs="shorts", legsc="C", extra=("sunglasses", "aloha"))
add("tourist_f", hair="long", hat="sunhat", torso="dress", legs="robe", extra=("sunglasses",))
add("swimmer_m", hat="swimcap", torso="swim", legs="shorts", legsc="C", extra=("goggles",))
add("swimmer_f", hat="swimcap", torso="swim", legs="shorts", legsc="C")
add("lifeguard", hat="visor", torso="swim", legs="shorts", legsc="C", extra=("sash",), sashc="C")
add("sailor", hat="cap", torso="shirt", legsc="D", extra=("pocket_stripes", "beard"), stripec="S")
add("waiter", hair="short", torso="shirt", legsc="D", extra=("tray", "tie"))
add("clinician", hair="bun", torso="coat", legsc="D", extra=("mask", "glasses"))
add("forgotten", hair="short", torso="robe", legs="robe", face="blank")
add("resort_boss", hat="tophat", torso="coat", legsc="D", extra=("sunglasses", "tie", "aloha"), patc="S")
add("beach_bum", hair="afro", torso="bare", legs="shorts", legsc="C", face="grin", extra=("sunglasses",))
add("sunbather", hair="long", torso="swim", legs="shorts", legsc="C", extra=("sunglasses",))

# ---------------------------------------------------------------------------------------------------- Area 5: Dis
add("imp", hair="bald", hat="horns", hatc="D", torso="bare", legs="pants", legsc="D", face="grin", extra=("tail", "wings", "fangs"))
add("brute", hair="bald", hat="horns", hatc="D", torso="bare", legs="shorts", legsc="C", width=1, face="angry", extra=("spikes", "tail"))
add("shade", hair="bald", hat="hood", hatc="D", skinc=3, torso="robe", legs="hover", face="glow", eyec="S", extra=("hem",))
add("damned", hair="bald", torso="bare", legs="shorts", legsc="C", face="hollow", extra=("ribs", "chain"))
add("warden", hat="helmet+horns", hatc="C", torso="armor", legsc="D", face="angry", extra=("belt",))
add("jester", hat="jester", torso="shirt", legsc="C", face="grin", extra=("pocket_stripes",), stripec="D")
add("judge", hair="bushy", hairc="S", torso="robe", legs="robe", extra=("collar", "staff"))
add("witch", hair="long", hat="witch", torso="dress", legs="robe", face="tired", extra=("glasses",))
add("firebreather", hair="mohawk", hairc="C", torso="bare", legs="shorts", legsc="C", face="grin", extra=("fangs",))
add("demon_lord", hair="bald", hat="horns", hatc="D", torso="robe", legs="robe", width=1, face="angry", extra=("fangs", "chain", "tail"))
add("finnegan", hair="bald", torso="robe", legs="robe", face="tired", extra=("whisker_hair",), beardc="C", torsoc="C")
