"""Species recipes for the generated creature sprites: plan + parameters + the two palette colours (5-bit RGB, body then shade/accent) and the
shiny pair.  The key is the species name; gen.py renders them and roster_data.py reads pal and shiny from here (art = "gen").

Palette slots of every picture: white (glow, highlights, bone), colour 1 (lit body), colour 2 (shade and second colour), black (outline).
View overrides: front / back dicts with yaw, pitch, dist.
"""
RECIPES = {}


def R(name, plan, params, pal, shiny, front=None, back=None, poses=None, fill=0.97, import_front=None, ramps=None, bob=None, import_back=None, back_mirror=None):
    """import_front: path (under sprites/) of a finished sprite supplied by the author, used as the front picture instead of a render.
    ramps: material shading override for the rendered views (see toon.RAMPS)."""
    assert name not in RECIPES, name
    RECIPES[name] = dict(plan=plan, params=params, pal=pal, shiny=shiny, front=front or {}, back=back or {}, poses=poses, fill=fill,
                         import_front=import_front, import_back=import_back, back_mirror=back_mirror, ramps=ramps, bob=bob or {})


# ---------------------------------------------------------------------------------------------- stage 4, checkpoint set
R("TYPHONEUS", "biped",
  dict(bulk=1.3, hunch=18, head="beast", head_s=1.7, head_kw=dict(horns_=("curved", 1.3), fangs=1.0, cheek=1.0), back=("spikes", 6, 0.65),
       tail={"kind": "spike", "length": 1.8, "thick": 0.34}, hand="claw", hand_size=1.4, arms=1, tex=("cracks", 1.6, 0.045, 0)),
  ((15, 19, 14), (24, 5, 5)), ((14, 16, 24), (26, 20, 6)), import_front="imports/typhoneus.png", back_mirror="drop")
R("EMBERWYRM", "biped",
  dict(bulk=1.0, hunch=8, head="dragon", head_s=1.75, head_kw=dict(horns_=("back", 1.3), fangs=1.0, cheek=1.0), hand="claw", hand_size=1.2,
       wings=dict(kind="bat", span=1.8, height=1.3), tail={"kind": "flame", "length": 1.7, "thick": 0.32}, back=("spikes", 4, 0.4)),
  ((30, 17, 5), (21, 4, 5)), ((24, 24, 30), (10, 10, 20)))
R("HELLHOUND", "quad",
  dict(bulk=1.15, head="beast", head_s=1.65, head_kw=dict(fangs=1.0, cheek=1.0, ears="point"), mane=1.2, back=("spikes", 7, 0.55),
       tail={"kind": "flame", "length": 1.5, "thick": 0.28}),
  ((21, 18, 19), (11, 9, 10)), ((14, 18, 24), (6, 8, 14)), front=dict(yaw=48), back=dict(yaw=-140), import_front="imports/hellhound.png", back_mirror="keep")
R("KINGCOBRA", "serpent",
  dict(head="dragon", head_s=1.8, hood=1.1, head_kw=dict(fangs=1.0, horns_=("back", 1.0))),
  ((17, 8, 22), (6, 3, 12)), ((28, 24, 6), (14, 8, 3)), front=dict(yaw=20), back=dict(yaw=-160))
R("BEEHEMOTH", "insect",
  dict(kind="bee", wings_kind="insect", fur=True, abdomen=1.2, head_s=1.45, tex=("stripes", 2, 0.45, 0.5, 2), abd_tex=("stripes", 2, 0.42, 0.5, 2),
       horn=0.5),
  ((30, 26, 5), (12, 6, 4)), ((26, 30, 8), (8, 12, 4)))
R("CARCINIZE", "arthro",
  dict(kind="crab", claws=True, claw_size=1.7, legs=3, shell=1.0, fangs=False, body=1.1, leg_len=0.85, leg_r=0.2, head_s=1.5, h=0.6),
  ((16, 19, 24), (6, 9, 16)), ((26, 20, 8), (14, 8, 3)), front=dict(pitch=10), back=dict(pitch=10))
R("APPARITION", "orb",
  dict(kind="ghost", r=1.25, arms=2, spikes=9, spike_size=0.6, face_s=1.1, mouth_big=True),
  ((15, 8, 20), (6, 3, 11)), ((8, 20, 22), (3, 9, 12)), front=dict(yaw=12), back=dict(yaw=-168))
R("RAVENOUS", "biped",
  dict(arms=0, head="bird", head_s=1.7, wings=dict(kind="feather", span=1.9, height=1.2), foot="talon", foot_size=1.4, bulk=0.9, spikes=False,
       tail={"kind": "plain", "length": 1.3, "thick": 0.22}, hunch=22, belly=False, back=None),
  ((9, 10, 15), (3, 3, 7)), ((26, 8, 8), (12, 3, 3)))
R("WYRMKING", "biped",
  dict(bulk=1.1, hunch=10, head="dragon", head_s=1.8, head_kw=dict(horns_=("crown", 1.4), fangs=1.0, cheek=1.0), hand="claw", arms=2,
       wings=dict(kind="bat", span=2.0, height=1.4), tail={"kind": "spike", "length": 1.8, "thick": 0.34}, back=("spikes", 5, 0.5)),
  ((28, 22, 6), (14, 7, 3)), ((8, 22, 26), (3, 8, 14)))
R("MONOLITH", "biped",
  dict(bulk=1.45, hunch=12, head="ape", head_s=1.4, arms=2, hand="fist", hand_size=1.6, shoulder_w=0.95, back=("plates", 5, 1.2), tail=None,
       tex=("dots", 0.36, 0.17, 2), arm_r=0.27, foot_size=1.5),
  ((22, 18, 11), (10, 7, 5)), ((18, 22, 12), (7, 10, 5)))

# ---------------------------------------------------------------------------------------------- centipedal and chimeric designs
R("TITANFIST", "biped",
  dict(bulk=1.45, hunch=14, head="ape", head_s=1.35, arms=4, hand="fist", hand_size=1.35, shoulder_w=0.95, arm_r=0.24, arm_len=1.0,
       head_kw=dict(horns_=("bull", 1.0), fangs=0.8), back=("plates", 4, 1.0), tail=None, tex=("dots", 0.36, 0.15, 2), foot_size=1.5),
  ((18, 19, 24), (21, 4, 6)), ((26, 22, 6), (14, 8, 3)))
R("SKYSCRAPER", "serpent",
  dict(path=[(1.9, 0.3, -0.9), (1.5, 0.38, -0.05), (0.8, 0.45, 0.45), (0.0, 0.5, 0.25), (-0.8, 0.55, -0.15), (-1.25, 0.7, 0.5),
             (-1.0, 1.2, 1.0), (-0.55, 1.8, 1.05)], girth=0.4, neck_r=0.36, head="dragon", head_s=1.7, head_turn=-65, plates=True, spines=0,
       leg_pairs=8, leg_range=(0.1, 0.72), leg_len=0.85, leg_r=0.1, head_kw=dict(horns_=("crown", 1.3), fangs=1.0)),
  ((16, 18, 23), (6, 8, 15)), ((27, 22, 8), (13, 8, 3)), front=dict(yaw=14, pitch=14), back=dict(yaw=-166, pitch=14))
R("GATEHOUND", "quad",
  dict(bulk=1.2, head="beast", head_s=1.5, head_kw=dict(fangs=1.0, cheek=1.0, ears="point"), mane=0.8, back=("spikes", 7, 0.55),
       extra_heads=[dict(pos=(1.0, -0.3, -0.15), turn=45), dict(pos=(-1.0, -0.3, -0.15), turn=0)],
       tail={"kind": "flame", "length": 1.5, "thick": 0.28}),
  ((20, 20, 23), (6, 11, 26)), ((26, 14, 8), (14, 5, 4)), front=dict(yaw=42), back=dict(yaw=-140))
R("DREADSTEED", "quad",
  dict(bulk=1.1, h=1.15, length=2.0, upper=dict(arms=2, hand="claw", head="skull", head_s=1.35, head_kw=dict(horns_=("crown", 1.2)), torso_h=0.75,
                                                  bulk=0.95, hunch=8, back=("spikes", 3, 0.4), arm_len=1.0),
       back=("plates", 5, 0.9), tail={"kind": "flame", "length": 1.8, "thick": 0.3}, spikes=True),
  ((12, 10, 14), (26, 9, 21)), ((26, 26, 28), (8, 12, 26)), front=dict(yaw=40), back=dict(yaw=-140))


# ---------------------------------------------------------------------------------------------- author-supplied sprites (drop-in)
def _register_imports():
    """imports/<species>.png is a finished front sprite for that species (imports/<species>_back.png its back sprite).  A species without a
    recipe gets one made here: palette suggested from the image, shiny by a channel rotation, a mirrored front as the back until a back arrives."""
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(here, "imports")
    if not os.path.isdir(d):
        return
    sys.path.insert(0, here)
    import importer
    for fn in sorted(os.listdir(d)):
        stem, ext = os.path.splitext(fn)
        if ext != ".png" or stem.endswith("_back"):
            continue
        name = stem.upper()
        if name in RECIPES:
            continue
        pal8 = importer.suggest_palette(os.path.join(d, fn))
        pal = tuple(tuple(v * 31 // 255 for v in c) for c in pal8)
        shiny = tuple((c[2], c[0], c[1]) for c in pal)
        back = f"imports/{stem}_back.png"
        has_back = os.path.exists(os.path.join(d, f"{stem}_back.png"))
        R(name, None, {}, pal, shiny, import_front=f"imports/{fn}", import_back=back if has_back else None, back_mirror=None if has_back else "keep")


_register_imports()
