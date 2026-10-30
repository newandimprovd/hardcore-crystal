"""Recipes of the generated creatures.  Every recipe is a dict: stage (3 or 4), plan (a function of plans.py), params, hooks, pal (body, accent as 5-bit
RGB) and shiny.  Palettes come from THEMES unless a recipe gives its own."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plans as P  # noqa: E402

# (body, accent) in 5-bit RGB (0..31).  Index 1 and 2 of every sprite.
THEMES = {
    "swamp": ((10, 20, 12), (26, 8, 6)),
    "ember": ((26, 14, 5), (30, 26, 6)),
    "blood": ((22, 6, 8), (30, 24, 8)),
    "bone": ((26, 24, 18), (22, 6, 6)),
    "moss": ((12, 22, 9), (28, 28, 8)),
    "abyss": ((8, 16, 20), (28, 4, 10)),
    "steel": ((17, 19, 23), (28, 24, 6)),
    "violet": ((17, 10, 24), (30, 22, 8)),
    "ice": ((16, 24, 30), (30, 10, 20)),
    "toxic": ((16, 10, 22), (22, 30, 6)),
    "rust": ((22, 12, 8), (28, 22, 10)),
    "ash": ((17, 17, 19), (28, 10, 6)),
    "sun": ((30, 24, 8), (24, 8, 6)),
    "rose": ((30, 16, 22), (22, 24, 30)),
}


def shiny_of(pal):
    (r, g, b), (r2, g2, b2) = pal
    return ((g, b, r), (min(31, b2 + 4), min(31, r2 + 2), g2))


RECIPES = {}


def R(name, stage, plan, params=None, hooks=None, theme=None, pal=None, shiny=None, seed=1):
    pal = pal or THEMES[theme]
    RECIPES[name] = dict(name=name, stage=stage, plan=plan, params=params or {}, hooks=hooks, pal=pal, shiny=shiny or shiny_of(pal), seed=seed)


def get(name):
    return RECIPES[name]


# ---- test recipes (quadruped plan)
R("DEATHROLL", 4, P.quad, dict(body=(19, 8), leg=8, legw=7, head_off=(-20, -3), head=(9, 6), snout=(9, 4), snout_dx=0.6, jaw=1,
                              tail="spike", tail_len=18, tail_w=9, neck_w=10), theme="moss")
R("HELLHOUND", 3, P.quad, dict(body=(15, 9), leg=14, head_off=(-15, -9), head=(7.5, 7), snout=(6, 3.2), jaw=1, ears="pointed", tail="flame",
                              tail_len=12), theme="ember")
R("BEHEMOTH", 4, P.quad, dict(body=(21, 13), leg=10, legw=9, head_off=(-19, -4), head=(9, 8), snout=(7, 5), horns=2, horn_len=10, tail_len=8),
  theme="steel")
R("MAMMOTH", 3, P.quad, dict(body=(18, 12), leg=12, legw=8, head_off=(-17, -6), head=(9, 9), snout=(5, 5), ears="long", tail_len=7), theme="ice")
