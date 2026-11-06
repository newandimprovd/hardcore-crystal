"""Recipes of the stage 3 and stage 4 species of the evolution lines (the ones that used to borrow a vanilla picture).  Imported at the end of
recipes.py.  Every family shares one body plan and palette family so the stages read as one line; stage 4 is larger, harder or stranger.
Palette entries are 5-bit RGB: (lit body colour, shade/second colour); the shiny is the second pair."""
from recipes import R


def sh(p, k=0):
    """Shiny pair by rotating the channels of the normal pair (k picks the rotation)."""
    if k == 0:
        return tuple((c[2], c[0], c[1]) for c in p)
    if k == 1:
        return tuple((c[1], c[2], c[0]) for c in p)
    return tuple((c[0], c[2], c[1]) for c in p)


def P(a, b, k=0):
    pal = (a, b)
    return pal, sh(pal, k)


# ============================================================================================ starters (stage 4)
R("ELDERWOOD", "quad",
  dict(bulk=1.35, length=2.1, head="dragon", head_s=1.5, head_kw=dict(horns_=("antlers", 1.2), eye="round"), back=("spikes", 8, 0.7),
       tail={"kind": "plain", "length": 1.5, "thick": 0.3}, tex=("stripes", 1, 0.32, 0.4, 2), neck=0.7, rise=0.7),
  *P((13, 20, 9), (7, 11, 5), 1), front=dict(yaw=40), back=dict(yaw=-140))
R("CALDERA", "biped",
  dict(bulk=1.3, hunch=12, head="beast", head_s=1.5, head_kw=dict(horns_=("curved", 1.2), fangs=0.8), back=("spikes", 7, 0.95), arms=1,
       hand="claw", tail={"kind": "flame", "length": 1.5, "thick": 0.3}, tex=("cracks", 1.5, 0.05, 0)),
  *P((17, 14, 13), (28, 9, 3), 1))
R("DEATHROLL", "quad",
  dict(bulk=1.3, length=2.4, h=0.75, head="croc", head_s=1.7, head_kw=dict(fangs=1.2), back=("plates", 8, 0.8), neck=0.4, rise=0.15,
       tail={"kind": "plain", "length": 2.0, "thick": 0.4}, tex=("dots", 0.3, 0.14, 2), foot="paw"),
  *P((8, 17, 17), (3, 8, 11), 0), front=dict(yaw=42), back=dict(yaw=-138))
R("OVERGROWN", "quad",
  dict(bulk=1.4, length=1.9, h=0.9, head="beast", head_s=1.4, head_kw=dict(fangs=0.8, cheek=1.0), back=("plates", 7, 1.3), neck=0.35,
       tail={"kind": "spike", "length": 1.2, "thick": 0.3}, tex=("dots", 0.34, 0.15, 2)),
  *P((9, 17, 8), (14, 6, 18), 1), front=dict(yaw=42), back=dict(yaw=-140))
R("IRONCLAD", "biped",
  dict(bulk=1.4, hunch=8, head="robot", head_s=1.45, arms=1, hand="fist", hand_size=1.4, back=("shell", ("dots", 0.3, 0.13, 2)), tail=None,
       tex=("dots", 0.34, 0.12, 2), foot_size=1.5, shoulder_w=0.95),
  *P((16, 20, 27), (7, 10, 17), 2))

# ============================================================================================ Furret line
R("SENTINEL", "serpent",
  dict(head="rodent", head_s=1.55, head_kw=dict(eye="round"), spines=0, girth=0.44, tex=("stripes", 1, 0.5, 0.25, 2)),
  *P((26, 20, 14), (14, 9, 6), 0), front=dict(yaw=20), back=dict(yaw=-160))
R("PANOPTICON", "serpent",
  dict(head="owl", head_s=1.9, hood=1.0, spines=0, girth=0.5, tex=("rings", 1, 0.3, 0.2, 2),
       path=[(1.7, 0.3, -0.7), (1.3, 0.42, 0.2), (0.4, 0.52, 0.7), (-0.5, 0.58, 0.3), (-0.4, 0.8, -0.4), (0.1, 1.5, -0.4), (0.0, 2.3, -0.2),
             (0.0, 2.9, 0.1), (0.0, 3.1, 0.6)]),
  *P((9, 9, 14), (3, 3, 8), 1), front=dict(yaw=18), back=dict(yaw=-162))

# ============================================================================================ Noctowl line
R("PROFESSOWL", "biped",
  dict(arms=0, head="owl", head_s=1.6, head_kw=dict(ears="point"), wings=dict(kind="feather", span=1.7, height=1.1), foot="talon", foot_size=1.3,
       bulk=0.95, spikes=False, tail={"kind": "plain", "length": 1.0, "thick": 0.24}, hunch=18, back=None),
  *P((22, 17, 12), (11, 8, 6), 1))
R("EMERITUS", "biped",
  dict(arms=0, head="owl", head_s=1.8, head_kw=dict(ears="long", crest=1.0), wings=dict(kind="feather", span=2.1, height=1.3), foot="talon",
       foot_size=1.4, bulk=1.1, spikes=False, tail={"kind": "plain", "length": 1.3, "thick": 0.26}, hunch=20, back=None),
  *P((24, 24, 27), (14, 12, 22), 2))

# ============================================================================================ Raticate line
R("PLAGUERAT", "quad",
  dict(bulk=0.95, length=1.6, h=0.8, head="rodent", head_s=1.5, head_kw=dict(ears="round", fangs=0.6), back=None, neck=0.3,
       tail={"kind": "plain", "length": 2.0, "thick": 0.14}, tex=("spots", 3.0, 0.62, 2)),
  *P((17, 15, 11), (9, 8, 4), 1), front=dict(yaw=40), back=dict(yaw=-140))
R("RATKING", "quad",
  dict(bulk=1.25, length=1.9, h=0.85, head="rodent", head_s=1.5, head_kw=dict(ears="round", fangs=0.8), back=("spikes", 5, 0.4), neck=0.35,
       extra_heads=[dict(pos=(0.9, -0.1, 0.0), turn=50), dict(pos=(-0.9, -0.1, 0.0), turn=0)],
       tail={"kind": "plain", "length": 2.2, "thick": 0.36, "curl": 0.7}, tex=("spots", 3.0, 0.62, 2)),
  *P((13, 12, 12), (6, 5, 7), 0), front=dict(yaw=40), back=dict(yaw=-140))

# ============================================================================================ Butterfree, Venomoth lines
R("CINDERWING", "insect",
  dict(kind="moth", wings_kind="moth", fur=True, abdomen=0.9, head_s=1.3, wing_span=2.2, wing_h=1.5, tex=("spots", 3.0, 0.66, 2), mandibles=False,
       stinger=False, antenna=1.3),
  *P((29, 14, 5), (12, 5, 5), 1))
R("CANDLEMOTH", "insect",
  dict(kind="moth", wings_kind="moth", fur=True, abdomen=0.8, head_s=1.2, wing_span=1.7, wing_h=1.2, mandibles=False, stinger=False, antenna=1.1,
       tex=("stripes", 1, 0.4, 0.3, 2)),
  *P((29, 24, 14), (20, 10, 6), 1))
R("PYREMOTH", "insect",
  dict(kind="moth", wings_kind="moth", fur=True, abdomen=1.0, head_s=1.35, wing_span=2.0, wing_h=1.5, mandibles=False, stinger=False, antenna=1.4,
       horn=0.3, tex=("stripes", 1, 0.4, 0.3, 2)),
  *P((28, 10, 4), (14, 4, 6), 1))

# ============================================================================================ Jumpluff
R("DANDELION", "orb",
  dict(kind="puff", r=1.0, puff_n=44, arms=2, arm_len=0.9, arm_r=0.17, hand="claw", spikes=0, legs=True, eye="round", mouth_big=True, face_s=0.9, hover=0.35),
  *P((29, 28, 17), (22, 20, 8), 1))

# ============================================================================================ Fearow line
R("DREADBEAK", "biped",
  dict(arms=0, head="bird", head_s=1.55, head_kw=dict(snout=1.3), wings=dict(kind="feather", span=1.8, height=1.1), foot="talon", foot_size=1.3,
       bulk=0.9, spikes=False, tail={"kind": "plain", "length": 1.2, "thick": 0.2}, hunch=22, back=None, tex=("stripes", 1, 0.35, 0.3, 2)),
  *P((14, 10, 16), (6, 4, 8), 1))
R("DOOMTALON", "biped",
  dict(arms=0, head="bird", head_s=1.8, head_kw=dict(snout=1.4, crest=1.2), wings=dict(kind="feather", span=2.3, height=1.4), foot="talon",
       foot_size=1.5, bulk=1.1, spikes=False, tail={"kind": "plain", "length": 1.5, "thick": 0.24}, hunch=24, back=None,
       tex=("stripes", 1, 0.35, 0.3, 2)),
  *P((10, 8, 12), (22, 5, 6), 0))

# ============================================================================================ Arbok
R("BASILISK", "serpent",
  dict(head="dragon", head_s=2.0, hood=0.9, girth=0.55, spines=7, spine_size=0.5, head_kw=dict(horns_=("crown", 1.2), fangs=1.0),
       tex=("dots", 0.3, 0.14, 2),
       path=[(1.9, 0.3, -0.9), (1.5, 0.4, 0.0), (0.7, 0.5, 0.6), (-0.4, 0.6, 0.4), (-0.6, 0.65, -0.3), (0.0, 1.0, -0.5), (0.0, 1.7, -0.3),
             (0.0, 2.3, 0.0), (0.0, 2.5, 0.6)]),
  *P((12, 21, 10), (5, 11, 4), 0), front=dict(yaw=18), back=dict(yaw=-162))

# ============================================================================================ Raichu
R("MEGAWATT", "biped",
  dict(bulk=1.0, hunch=10, head="rodent", head_s=1.55, head_kw=dict(ears="long", eye="dot"), arms=1, hand="paw",
       tail={"kind": "blade", "length": 1.8, "thick": 0.2}, back=None, spikes=False, tex=None),
  *P((31, 27, 6), (23, 13, 3), 1))

# ============================================================================================ Clefable, Wigglytuff, Blissey lines
R("MOONQUEEN", "biped",
  dict(bulk=0.9, hunch=6, head="humanoid", head_s=1.5, head_kw=dict(ears="long", eye="round"), arms=1, hand="paw",
       wings=dict(kind="feather", span=1.4, height=1.0), tail={"kind": "plain", "length": 1.0, "thick": 0.2, "curl": 0.6}, back=None, spikes=False),
  *P((27, 22, 29), (16, 10, 24), 1))
R("SOPORIFIC", "biped",
  dict(bulk=1.4, hunch=4, head="cat", head_s=1.6, head_kw=dict(ears="long", eye="round"), arms=1, hand="paw", torso_h=0.8,
       tail={"kind": "plain", "length": 1.0, "thick": 0.3, "curl": 0.8}, back=None, spikes=False),
  *P((30, 22, 26), (22, 11, 17), 2))
R("PLACEBO", "orb",
  dict(kind="pill", r=1.0, tilt=18, arms=2, arm_len=0.8, arm_r=0.16, spikes=0, legs=True, eye="round", mouth_big=True, face_s=0.8, hover=0.3, extra_eyes=0),
  *P((31, 26, 27), (25, 15, 18), 2), front=dict(yaw=10), back=dict(yaw=-170))
R("HOSPICE", "orb",
  dict(kind="ghost", r=1.2, arms=2, arm_len=1.0, spikes=0, halo=True, iv=True, bands=2, eye="round", mouth_big=True, face_s=0.9, hover=0.6),
  *P((27, 26, 31), (17, 15, 25), 0), front=dict(yaw=12), back=dict(yaw=-168))

# ============================================================================================ Nidoqueen, Nidoking
R("MATRIARCH", "biped",
  dict(bulk=1.4, hunch=8, head="beast", head_s=1.45, head_kw=dict(ears="round", cheek=0.8), arms=1, hand="claw", back=("spikes", 5, 0.6),
       tail={"kind": "club", "length": 1.5, "thick": 0.3}, tex=("dots", 0.36, 0.13, 2)),
  *P((22, 14, 25), (12, 6, 16), 1))
R("TYRANT", "biped",
  dict(bulk=1.55, hunch=12, head="beast", head_s=1.45, head_kw=dict(horns_=("straight", 1.5), fangs=1.0), arms=1, hand="fist", hand_size=1.5,
       back=("plates", 5, 1.0), tail={"kind": "spike", "length": 1.8, "thick": 0.34}, tex=("dots", 0.36, 0.13, 2)),
  *P((13, 11, 17), (5, 4, 10), 1))

# ============================================================================================ Crobat
R("NOSFERATU", "biped",
  dict(bulk=0.9, hunch=20, head="beast", head_s=1.5, head_kw=dict(ears="bat", fangs=1.3, snout=0.8), arms=1, hand="claw",
       wings=dict(kind="bat", span=2.3, height=1.5), tail={"kind": "plain", "length": 1.0, "thick": 0.18}, back=None, spikes=False),
  *P((15, 10, 21), (7, 4, 13), 2))

# ============================================================================================ Bellossom, Victreebel lines
R("BELLADONNA", "biped",
  dict(bulk=0.9, hunch=8, head="humanoid", head_s=1.4, head_kw=dict(horns_=("crown", 1.3), eye="round"), arms=1, hand="claw",
       back=("plates", 4, 1.0), tail=None, spikes=False),
  *P((19, 9, 25), (10, 4, 16), 1))
R("MAWBLOOM", "serpent",
  dict(head="beast", head_s=2.5, head_kw=dict(fangs=1.2, snout=1.2), girth=0.5, spines=0, fins=[0.35, 0.5, 0.65], tex=("stripes", 1, 0.6, 0.25, 2),
       path=[(1.2, 0.3, -0.8), (1.0, 0.45, 0.2), (0.2, 0.6, 0.5), (-0.4, 0.7, -0.1), (0.0, 1.2, -0.5), (0.0, 1.9, -0.3), (0.0, 2.5, 0.0),
             (0.0, 2.7, 0.5)]),
  *P((10, 21, 8), (24, 5, 9), 0), front=dict(yaw=18), back=dict(yaw=-162))

# ============================================================================================ Parasect line
R("CORDYCEPS", "arthro",
  dict(kind="crab", claws=True, claw_size=1.2, legs=3, shell=1.0, fangs=False, body=0.95, leg_len=0.8, leg_r=0.17, head_s=1.2, h=0.55,
       tex=("spots", 3.0, 0.62, 2)),
  *P((24, 14, 10), (13, 6, 10), 1), front=dict(pitch=10), back=dict(pitch=10))
R("SPOREKING", "arthro",
  dict(kind="crab", claws=True, claw_size=1.5, legs=3, shell=1.0, fangs=True, body=1.2, leg_len=0.9, leg_r=0.2, head_s=1.4, h=0.6,
       tex=("spots", 3.0, 0.6, 2)),
  *P((27, 25, 27), (15, 10, 21), 0), front=dict(pitch=10), back=dict(pitch=10))

# ============================================================================================ Ariados line
R("SILKFANG", "arthro",
  dict(kind="spider", legs=4, leg_len=1.5, claws=False, fangs=True, body=0.8, abd=1.0, head_s=1.0, tex=None, abd_tex=("stripes", 2, 0.5, 0.3, 2)),
  *P((13, 8, 15), (25, 4, 8), 0), front=dict(pitch=8), back=dict(pitch=8))
R("WEBWEAVER", "arthro",
  dict(kind="spider", legs=4, leg_len=1.7, claws=False, fangs=True, body=0.95, abd=1.3, head_s=1.2, abd_tex=("stripes", 2, 0.5, 0.3, 2), web=True),
  *P((9, 12, 22), (24, 22, 4), 1), front=dict(pitch=8), back=dict(pitch=8))

# ============================================================================================ Persian line
R("ALLEYCAT", "quad",
  dict(bulk=0.95, length=1.7, h=0.85, head="cat", head_s=1.55, head_kw=dict(ears="point", eye="slit"), back=None, neck=0.35,
       tail={"kind": "plain", "length": 1.8, "thick": 0.2, "curl": 0.5}, tex=("stripes", 2, 0.4, 0.22, 2), foot="paw"),
  *P((13, 13, 18), (24, 6, 17), 1), front=dict(yaw=42), back=dict(yaw=-140))
R("KINGPIN", "quad",
  dict(bulk=1.15, length=1.9, h=0.95, head="cat", head_s=1.65, head_kw=dict(ears="point", eye="slit", crest=0.8), back=None, neck=0.4, mane=0.5,
       tail={"kind": "plain", "length": 2.0, "thick": 0.24, "curl": 0.6}, foot="paw"),
  *P((28, 25, 19), (15, 10, 8), 2), front=dict(yaw=42), back=dict(yaw=-140))

# ============================================================================================ Golduck line
R("MIGRAINE", "biped",
  dict(bulk=1.0, hunch=14, head="duck", head_s=1.55, head_kw=dict(eye="angry", ears="fin"), arms=1, hand="paw",
       tail={"kind": "plain", "length": 1.0, "thick": 0.2}, back=None, spikes=False, foot="plant", foot_size=1.4),
  *P((9, 19, 28), (4, 8, 19), 2))
R("ANEURYSM", "biped",
  dict(bulk=1.05, hunch=12, head="duck", head_s=2.0, head_kw=dict(eye="round", ears="fin", crest=1.2), arms=1, hand="paw",
       tail={"kind": "plain", "length": 1.0, "thick": 0.2}, back=None, spikes=False, foot="plant", foot_size=1.5),
  *P((25, 11, 22), (13, 4, 14), 1))

# ============================================================================================ Primeape line
R("BERSERKER", "biped",
  dict(bulk=1.25, hunch=18, head="ape", head_s=1.5, arms=1, hand="fist", hand_size=1.5, tail=None, back=None, shoulder_w=0.95,
       head_kw=dict(brow=1.3), tex=("dots", 0.38, 0.12, 2)),
  *P((27, 19, 13), (15, 8, 6), 0))
R("ANGERILLA", "biped",
  dict(bulk=1.55, hunch=16, head="ape", head_s=1.55, head_kw=dict(horns_=("bull", 1.0), brow=1.4), arms=2, hand="fist", hand_size=1.5, tail=None,
       back=("plates", 4, 1.0), shoulder_w=1.0, arm_r=0.25, tex=("dots", 0.38, 0.12, 2)),
  *P((14, 13, 16), (26, 6, 6), 1))

# ============================================================================================ Alakazam
R("OMNISCIENT", "biped",
  dict(bulk=0.85, hunch=16, head="beast", head_s=1.75, head_kw=dict(ears="long", snout=1.2, crest=1.0, eye="slit"), arms=1, hand="claw",
       tail=None, back=None, spikes=False, torso_h=0.65, tex=("stripes", 1, 0.3, 0.2, 2)),
  *P((22, 20, 28), (10, 8, 19), 0))

# ============================================================================================ Steelix line
R("ADAMANTIX", "serpent",
  dict(head="dragon", head_s=1.8, head_kw=dict(horns_=("bull", 1.0), fangs=0.6), girth=0.6, plates=True, spines=8, spine_size=0.55,
       tex=("rings", 1, 0.3, 0.14, 2),
       path=[(2.3, 0.35, -0.9), (1.7, 0.5, 0.0), (0.9, 0.65, 0.5), (0.0, 0.7, 0.3), (-0.8, 0.75, -0.1), (-1.0, 1.1, 0.5), (-0.6, 1.8, 0.6),
             (-0.2, 2.5, 0.4), (0.1, 2.9, 0.8)]),
  *P((17, 18, 22), (8, 9, 13), 1), front=dict(yaw=22), back=dict(yaw=-158))

# ============================================================================================ Ninetales line
R("KITSUNE", "quad",
  dict(bulk=0.95, length=1.8, h=0.95, head="beast", head_s=1.5, head_kw=dict(ears="point", snout=1.1, eye="slit"), back=None, neck=0.45,
       tail={"kind": "flame", "length": 2.0, "thick": 0.4, "curl": 0.5}, foot="paw"),
  *P((30, 19, 12), (23, 9, 9), 1), front=dict(yaw=42), back=dict(yaw=-140))
R("FOXFIRE", "quad",
  dict(bulk=1.05, length=1.9, h=1.0, head="beast", head_s=1.55, head_kw=dict(ears="long", snout=1.1, eye="slit", crest=0.8), back=None, neck=0.5,
       mane=0.9, tail={"kind": "flame", "length": 2.3, "thick": 0.5, "curl": 0.6}, foot="paw"),
  *P((31, 29, 24), (27, 17, 7), 1), front=dict(yaw=42), back=dict(yaw=-140))

# ============================================================================================ Rapidash
R("UNICORN", "quad",
  dict(bulk=1.0, length=1.9, h=1.2, head="horse", head_s=1.5, head_kw=dict(horns_=("straight", 1.5), eye="round"), back=None, neck=0.6, rise=0.6,
       mane=1.0, tail={"kind": "flame", "length": 1.8, "thick": 0.3}, foot="hoof"),
  *P((30, 27, 29), (25, 12, 24), 0), front=dict(yaw=42), back=dict(yaw=-140))

# ============================================================================================ Houndoom line
R("HELLBOUND", "quad",
  dict(bulk=0.95, length=1.75, h=0.95, head="beast", head_s=1.5, head_kw=dict(horns_=("curved", 1.0), ears="point", fangs=1.0), back=None,
       neck=0.4, tail={"kind": "spike", "length": 1.4, "thick": 0.2}, foot="paw"),
  *P((10, 9, 12), (28, 11, 4), 1), front=dict(yaw=42), back=dict(yaw=-140))
R("PERDITION", "quad",
  dict(bulk=1.3, length=2.0, h=1.0, head="beast", head_s=1.65, head_kw=dict(horns_=("back", 1.5), ears="point", fangs=1.2, cheek=1.0),
       back=("spikes", 6, 0.6), neck=0.45, mane=1.2, tail={"kind": "flame", "length": 1.8, "thick": 0.32}, foot="paw"),
  *P((13, 10, 13), (29, 7, 3), 1), front=dict(yaw=42), back=dict(yaw=-140))

# ============================================================================================ Ampharos
R("BLACKSHEEP", "biped",
  dict(bulk=1.25, hunch=8, head="beast", head_s=1.5, head_kw=dict(horns_=("bull", 1.2), eye="angry", snout=0.8), arms=1, hand="fist",
       tail={"kind": "flame", "length": 1.2, "thick": 0.3}, back=None, tex=("dots", 0.3, 0.17, 2)),
  *P((10, 9, 12), (30, 26, 6), 1))

# ============================================================================================ Magneton, Porygon2 lines
R("MAGNETRON", "orb",
  dict(kind="magnets", r=0.95, arms=0, spikes=0, sat_r=0.42, eye="round", mouth_big=True, hover=0.55, face_s=0.9),
  *P((17, 20, 27), (8, 10, 19), 1))
R("SOLENOID", "orb",
  dict(kind="coil", r=1.1, turns=7, arms=2, arm_len=1.1, arm_r=0.16, hand="claw", spikes=0, eye="slit", mouth_big=True, hover=0.35, face_s=0.8),
  *P((27, 19, 8), (14, 8, 4), 0))
R("MAINFRAME", "biped",
  dict(bulk=1.2, hunch=6, head="robot", head_s=1.5, arms=1, hand="fist", tail=None, back=("plates", 3, 0.8), tex=("dots", 0.3, 0.12, 2), spikes=False,
       foot_size=1.4),
  *P((22, 22, 19), (9, 10, 13), 1))
R("ALGORITHM", "orb",
  dict(kind="cubes", r=1.0, sat_n=7, sat_r=0.32, arms=0, spikes=0, eye="slit", mouth_big=True, hover=0.55, face_s=0.9),
  *P((8, 23, 24), (3, 10, 14), 1))

# ============================================================================================ Marowak line
R("BONEKEEPER", "biped",
  dict(bulk=0.95, hunch=14, head="skull", head_s=1.5, arms=1, hand="blade", tail={"kind": "plain", "length": 1.1, "thick": 0.2}, back=None,
       spikes=False),
  *P((21, 18, 14), (10, 8, 7), 1))
R("OSSUARY", "biped",
  dict(bulk=1.3, hunch=14, head="skull", head_s=1.55, head_kw=dict(horns_=("curved", 1.0)), arms=2, hand="claw", tail={"kind": "plain", "length": 1.3,
       "thick": 0.24}, back=("plates", 6, 1.0), extra_heads=[dict(pos=(0.55, 0.15, -0.1), turn=40, s=0.9)], spikes=True),
  *P((23, 22, 17), (9, 13, 10), 0))

# ============================================================================================ Muk, Weezing lines
R("SLUDGELORD", "orb",
  dict(kind="heap", r=1.25, arms=2, arm_len=1.1, spikes=0, bumps=7, drips=4, pods=3, junk=4, bubbles=5, eye="angry", mouth_big=True, hover=0.1, tex=("spots", 3.0, 0.64, 2), seed=3),
  *P((16, 9, 20), (7, 3, 11), 1), front=dict(yaw=10), back=dict(yaw=-170))
R("SUPERFUND", "orb",
  dict(kind="heap", r=1.55, arms=3, arm_len=1.2, spikes=0, bumps=6, drips=5, pods=4, junk=7, bubbles=8, extra_eyes=1, eye="round", mouth_big=True, hover=0.05, tex=("spots", 2.5, 0.6, 2), seed=5),
  *P((14, 24, 8), (5, 12, 3), 1), front=dict(yaw=10), back=dict(yaw=-170))
R("MIASMA", "orb",
  dict(kind="cloud", r=0.95, cloud_n=7, arms=0, spikes=0, tendrils=5, bumps=0, extra_eyes=1, eye="slit", mouth_big=True, hover=0.75),
  *P((20, 16, 24), (10, 7, 16), 0))
R("PANDEMIC", "orb",
  dict(kind="cloud", r=1.1, cloud_n=7, arms=0, spikes=0, virus=24, tendrils=3, extra_eyes=2, eye="angry", mouth_big=True, hover=0.65),
  *P((10, 17, 10), (4, 7, 5), 1))

# ============================================================================================ Rhydon line
R("WARHORN", "biped",
  dict(bulk=1.4, hunch=14, head="beast", head_s=1.5, head_kw=dict(horns_=("straight", 1.7), fangs=0.6), arms=1, hand="fist", hand_size=1.4,
       back=("plates", 4, 0.9), tail={"kind": "club", "length": 1.5, "thick": 0.3}, tex=("dots", 0.36, 0.14, 2)),
  *P((20, 18, 18), (10, 9, 10), 1))
R("BEHEMOTH", "quad",
  dict(bulk=1.65, length=2.0, h=1.1, head="beast", head_s=1.5, head_kw=dict(horns_=("straight", 1.8), fangs=0.5), back=("plates", 6, 1.2),
       neck=0.3, rise=0.2, tail={"kind": "club", "length": 1.4, "thick": 0.4}, tex=("dots", 0.36, 0.14, 2), foot="plant"),
  *P((16, 17, 19), (7, 8, 11), 2), front=dict(yaw=42), back=dict(yaw=-140))

# ============================================================================================ Scizor line
R("CLEAVER", "insect",
  dict(kind="beetle", wings_kind="elytra", armor=True, scythe=True, abdomen=0.9, head_s=1.2, mandibles=True, stinger=False, tex=("dots", 0.3, 0.12, 2)),
  *P((23, 10, 10), (12, 3, 6), 1))
R("HEADSMAN", "insect",
  dict(kind="mantis", wings_kind="elytra", armor=True, scythe=True, abdomen=1.1, head_s=1.4, mandibles=True, stinger=False, horn=0.4,
       tex=("dots", 0.3, 0.12, 2)),
  *P((14, 15, 21), (6, 6, 12), 0))

# ============================================================================================ Poliwrath, Slowbro lines
R("POLIWRAITH", "biped",
  dict(bulk=1.35, hunch=6, head="blob", head_s=1.3, head_kw=dict(eye="hollow"), arms=1, hand="fist", hand_size=1.5, tail=None, back=None,
       spikes=False, tex=("rings", 2, 0.35, 0.12, 2)),
  *P((16, 20, 28), (7, 9, 19), 1))
R("AMNESIAC", "biped",
  dict(bulk=1.25, hunch=8, head="beast", head_s=1.5, head_kw=dict(snout=1.1, eye="dot", ears="round"), arms=1, hand="paw", torso_h=0.8,
       tail={"kind": "club", "length": 1.3, "thick": 0.3}, back=None, spikes=False),
  *P((28, 17, 19), (18, 8, 11), 2))
R("OBLIVION", "biped",
  dict(bulk=1.5, hunch=8, head="beast", head_s=1.7, head_kw=dict(snout=1.1, eye="dot", ears="round"), arms=1, hand="paw", torso_h=0.85,
       tail={"kind": "club", "length": 1.4, "thick": 0.34}, back=("shell", None), spikes=False),
  *P((21, 12, 22), (10, 5, 13), 1))

# ============================================================================================ Dewgong line
R("TUSKDRIFT", "quad",
  dict(bulk=1.3, length=2.4, h=0.55, head="beast", head_s=1.5, head_kw=dict(fangs=1.6, snout=0.9, eye="round"), back=None, neck=0.3, rise=0.1,
       tail={"kind": "blade", "length": 1.6, "thick": 0.3}, foot="paw", leg_r=0.18),
  *P((26, 28, 31), (14, 18, 28), 1), front=dict(yaw=42), back=dict(yaw=-140))
R("FROSTSIREN", "serpent",
  dict(head="humanoid", head_s=1.5, head_kw=dict(eye="round"), arms=1, girth=0.38, spines=0, fins=[0.1, 0.25],
       path=[(1.7, 0.3, -0.7), (1.3, 0.4, 0.2), (0.5, 0.5, 0.6), (-0.4, 0.55, 0.2), (-0.1, 0.9, -0.4), (0.0, 1.5, -0.3), (0.0, 2.1, 0.0),
             (0.0, 2.35, 0.4)]),
  *P((18, 26, 30), (8, 14, 24), 2), front=dict(yaw=18), back=dict(yaw=-162))

# ============================================================================================ Cloyster line
R("CRYOCLAM", "orb",
  dict(kind="clam", r=1.05, arms=0, spikes=0, eye="angry", mouth_big=True, hover=0.1, face_s=0.9),
  *P((19, 25, 30), (9, 13, 22), 1), front=dict(yaw=10), back=dict(yaw=-170))
R("ABYSSHELL", "orb",
  dict(kind="nautilus", r=1.2, shell_spikes=9, arms=0, spikes=0, eye="hollow", mouth_big=True, hover=0.15, face_s=0.9),
  *P((8, 10, 21), (3, 4, 11), 0), front=dict(yaw=10), back=dict(yaw=-170))

# ============================================================================================ Kingler
R("CARAPACE", "arthro",
  dict(kind="crab", claws=True, claw_size=1.5, legs=3, shell=1.0, fangs=False, body=1.0, leg_len=0.85, leg_r=0.19, head_s=1.3, h=0.55,
       tex=("dots", 0.3, 0.14, 2)),
  *P((22, 18, 14), (11, 8, 8), 1), front=dict(pitch=10), back=dict(pitch=10))

# ============================================================================================ Starmie line
R("NEBULON", "orb",
  dict(kind="starfish", r=1.15, star_arms=5, curl=0.6, halo=True, arms=0, spikes=0, satellites=2, sat_r=0.2, eye="round", mouth_big=True, hover=0.45, face_s=0.8),
  *P((18, 12, 26), (8, 5, 16), 1))
R("SUPERNOVA", "orb",
  dict(kind="starfish", r=1.3, star_arms=8, curl=0.15, halo=False, arms=0, spikes=0, eye="angry", mouth_big=True, hover=0.35, face_s=0.8, extra_eyes=2),
  *P((30, 22, 6), (24, 8, 3), 1))

# ============================================================================================ Kingdra, Gyarados lines
R("MAELDRA", "serpent",
  dict(head="dragon", head_s=2.1, head_kw=dict(horns_=("crown", 1.3), fangs=0.8), girth=0.5, spines=8, spine_size=0.55, fins=[0.3, 0.5, 0.7],
       plates=True, tex=("dots", 0.3, 0.13, 2)),
  *P((14, 20, 28), (5, 8, 18), 1), front=dict(yaw=20), back=dict(yaw=-160))
R("RAGECARP", "serpent",
  dict(head="dragon", head_s=1.9, head_kw=dict(fangs=1.2, cheek=1.0), hood=0.7, girth=0.5, spines=7, spine_size=0.5, fins=[0.4],
       tex=("stripes", 1, 0.35, 0.25, 2)),
  *P((28, 11, 6), (14, 4, 3), 1), front=dict(yaw=20), back=dict(yaw=-160))
R("WORLDEATER", "serpent",
  dict(head="dragon", head_s=2.4, head_kw=dict(horns_=("back", 1.5), fangs=1.4, cheek=1.0), girth=0.65, neck_r=0.55, plates=True, spines=9,
       spine_size=0.6, fins=[0.3, 0.45, 0.6, 0.75], tex=("dots", 0.3, 0.14, 2),
       path=[(2.2, 0.4, -1.0), (1.8, 0.55, 0.0), (1.0, 0.7, 0.6), (0.0, 0.8, 0.4), (-0.9, 0.85, 0.0), (-1.2, 1.0, -0.6), (-0.6, 1.4, -0.8),
             (0.2, 2.0, -0.5), (0.4, 2.8, 0.0), (0.4, 3.2, 0.7)]),
  *P((8, 15, 21), (3, 5, 11), 0), front=dict(yaw=18, pitch=8), back=dict(yaw=-162, pitch=8))

# ============================================================================================ Azumarill, Hypno, Piloswine, Jynx lines
R("TIDEBELLY", "biped",
  dict(bulk=1.3, hunch=4, head="rodent", head_s=1.55, head_kw=dict(ears="round", eye="round"), arms=1, hand="paw", torso_h=0.75,
       tail={"kind": "plain", "length": 0.9, "thick": 0.3, "curl": 0.9}, back=None, spikes=False),
  *P((12, 19, 28), (5, 9, 19), 2))
R("BEACHBALL", "orb",
  dict(kind="blob", r=1.45, arms=2, arm_len=0.7, arm_r=0.18, spikes=0, legs=True, hat=True, valve=True, eye="round", mouth_big=True, hover=0.2, face_s=0.8, tex=("stripes", 1, 0.9, 0.5, 2)),
  *P((29, 29, 31), (9, 14, 28), 1), front=dict(yaw=10), back=dict(yaw=-170))
R("NARCOLEPT", "biped",
  dict(bulk=1.1, hunch=26, head="beast", head_s=1.5, head_kw=dict(snout=1.6, eye="dot", ears="round"), arms=1, hand="paw", torso_h=0.8,
       tail=None, back=None, spikes=False),
  *P((28, 24, 12), (15, 10, 5), 1))
R("SANDMAN", "biped",
  dict(bulk=1.2, hunch=24, head="beast", head_s=1.7, head_kw=dict(snout=1.6, eye="slit", ears="round", crest=0.8), arms=1, hand="claw",
       torso_h=0.85, tail=None, back=None, spikes=False),
  *P((10, 10, 21), (25, 22, 6), 0))
R("MAMMOTH", "quad",
  dict(bulk=1.3, length=2.0, h=0.8, head="beast", head_s=1.5, head_kw=dict(horns_=("bull", 1.4), snout=1.2), back=None, neck=0.3, rise=0.2,
       mane=0.9, tail={"kind": "plain", "length": 0.9, "thick": 0.2}, tex=("stripes", 1, 0.3, 0.2, 2), foot="plant"),
  *P((24, 20, 16), (12, 9, 8), 1), front=dict(yaw=42), back=dict(yaw=-140))
R("ICEAGE", "quad",
  dict(bulk=1.65, length=2.2, h=1.0, head="beast", head_s=1.55, head_kw=dict(horns_=("bull", 2.0), snout=1.2), back=("spikes", 9, 1.0), neck=0.3,
       rise=0.2, mane=1.0, tail={"kind": "plain", "length": 1.0, "thick": 0.25}, foot="plant"),
  *P((24, 27, 31), (12, 15, 25), 1), front=dict(yaw=42), back=dict(yaw=-140))
R("FROSTBITE", "biped",
  dict(bulk=1.0, hunch=6, head="humanoid", head_s=1.55, head_kw=dict(eye="round", ears="round"), arms=1, hand="paw", torso_h=0.8, tail=None,
       back=None, spikes=False),
  *P((24, 15, 27), (12, 6, 19), 1))
R("RIMEQUEEN", "biped",
  dict(bulk=1.0, hunch=3, head="humanoid", head_s=1.55, head_kw=dict(horns_=("crown", 1.5), eye="slit"), arms=1, hand="claw", torso_h=0.9,
       tail=None, back=("plates", 4, 0.9), spikes=False),
  *P((20, 28, 31), (8, 16, 26), 0))
