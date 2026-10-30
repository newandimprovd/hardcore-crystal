"""Generated creature sprites: recipes -> front.png (four stacked animation frames) and back.png, plus preview sheets.

usage: gen.py preview OUT.png NAME [NAME...]     contact sheet (front, back, two animation frames) of the named recipes
       gen.py sheet OUT.png                      contact sheet of every recipe
gen_roster.py calls build(slug, out_dir) for every species whose NEW entry has art="gen"."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from PIL import Image, ImageDraw  # noqa: E402
from creature import Scene  # noqa: E402
from pixart import c5, preview, render  # noqa: E402
import recipes  # noqa: E402

POSES = [
    {},
    {"head": (-1, -2), "mouth": 1, "glow": 1, "sway": 1.0},
    {"head": (0, -1), "glow": 1, "sway": 2.0},
    {"head": (0, 1), "sway": -1.0},
]


def pal(rc, shiny=False):
    body, accent = rc["shiny"] if shiny else rc["pal"]
    return [(255, 255, 255), c5(*body), c5(*accent), (0, 0, 0)]


def draw(rc, view, pose=None):
    sc = Scene(view=view, stage=rc["stage"], seed=rc.get("seed", 1), pose=pose)
    rc["plan"](sc, rc["params"], rc.get("hooks"))
    return sc.result()


def frames_of(rc):
    return [draw(rc, "front", p) for p in POSES]


def tile_diff(frames):
    base = frames[0]
    n = base.n // 8
    tiles = set()
    for fr in frames[1:]:
        for ty in range(n):
            for tx in range(n):
                a = tuple(tuple(r[tx * 8:tx * 8 + 8]) for r in base.px[ty * 8:ty * 8 + 8])
                c = tuple(tuple(r[tx * 8:tx * 8 + 8]) for r in fr.px[ty * 8:ty * 8 + 8])
                if a != c:
                    tiles.add(c)
    return len(tiles)


def build(slug, out_dir):
    rc = recipes.get(slug.upper())
    os.makedirs(out_dir, exist_ok=True)
    frames = frames_of(rc)
    extra = tile_diff(frames)
    assert 49 + extra <= 98, (slug, "animation tiles", 49 + extra)
    render(frames, pal(rc)).save(os.path.join(out_dir, "front.png"))
    render([draw(rc, "back")], pal(rc)).save(os.path.join(out_dir, "back.png"))
    return frames


def sheet(names, out, scale=3):
    cells = []
    for nm in names:
        rc = recipes.get(nm)
        cells.append((nm, rc, [draw(rc, "front"), draw(rc, "back"), draw(rc, "front", POSES[1]), draw(rc, "front", POSES[3])]))
    cw = 56 * scale + 8
    cols = 4
    W = cols * cw
    rows = len(cells)
    im = Image.new("RGB", (W, rows * (56 * scale + 22)), (70, 100, 140))
    d = ImageDraw.Draw(im)
    for r, (nm, rc, cvs) in enumerate(cells):
        y0 = r * (56 * scale + 22)
        d.text((6, y0 + 3), f"{nm}  stage {rc['stage']}", fill=(255, 255, 255))
        pl = pal(rc)
        for k, cv in enumerate(cvs):
            n = cv.n
            t = Image.new("RGB", (n, n))
            for y in range(n):
                for x in range(n):
                    t.putpixel((x, y), pl[cv.px[y][x]])
            t = t.resize((n * scale, n * scale), Image.NEAREST)
            im.paste(t, (k * cw + 4, y0 + 18 + (56 - n) * scale))
    im.save(out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        sheet([n.upper() for n in sys.argv[3:]], sys.argv[2])
    elif cmd == "sheet":
        sheet(sorted(recipes.RECIPES), sys.argv[2])
    else:
        raise SystemExit(__doc__)
