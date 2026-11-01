"""Generated creature sprites: renders a recipe (recipes.py) into front.png (base frame plus three animation frames, stacked) and back.png.

build(slug, out_dir) is the module interface used by gen_roster.gen_art.  `python3 gen.py sheet NAME...` writes a contact sheet to
/home/claude/scratch/spr/sheet.png; `python3 gen.py stats` prints the animation tile budget of every recipe.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importer  # noqa: E402
import plans  # noqa: E402
import rig  # noqa: E402
from recipes import RECIPES  # noqa: E402
from sdf import Model  # noqa: E402

BUDGET = 49  # distinct changed tiles allowed over the three animation frames (the pic animation shares unchanged tiles)
POSES = [{"jaw": 1, "glow": 1, "wing": 0.6}, {"head_dy": 0.06, "breath": 1, "tail": 0.25, "wing": -0.6}, {"head_dy": -0.05, "jaw": 1, "arm": 0.5, "tail": -0.25, "wing": 0.3}]


def c5(c):
    return tuple(round(v * 255 / 31) for v in c)


def palette(rec, shiny=False):
    a, b = rec["shiny" if shiny else "pal"]
    return [(255, 255, 255), c5(a), c5(b), (0, 0, 0)]


def make_rig(rec):
    params = rec["params"]

    def builder(pose):
        M = Model()
        plans.PLANS[rec["plan"]](M, pose, params)
        if rec.get("ramps"):
            M.ramps = dict(rec["ramps"])
        return M
    f, b = rec["front"], rec["back"]
    views = {k: dict(v) for k, v in rig.VIEWS.items()}
    for k, ov in (("front", f), ("back", b)):
        views[k].update({kk: vv for kk, vv in ov.items() if kk in ("yaw", "pitch", "dist")})
    return rig.Rig(builder, views=views, fill=rec["fill"])


def tiles_of(img):
    n = img.shape[0] // 8
    return [img[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] for ty in range(n) for tx in range(n)]


def changed_tiles(base, fr):
    tb, tf = tiles_of(base), tiles_of(fr)
    return [i for i in range(len(tb)) if not np.array_equal(tb[i], tf[i])]


def enforce_budget(frames):
    """Revert tiles of the animation frames to the base until the number of distinct changed tiles fits the budget."""
    base = frames[0]
    out = [base]
    pool = {}
    n = base.shape[0] // 8
    for fr in frames[1:]:
        fr = fr.copy()
        for i in changed_tiles(base, fr):
            ty, tx = divmod(i, n)
            t = fr[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            key = t.tobytes()
            if key not in pool and len(pool) >= BUDGET:
                fr[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = base[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            else:
                pool[key] = True
        out.append(fr)
    return out, len(pool)


def render(name):
    rec = RECIPES[name]
    pal = palette(rec)
    pal8 = [pal[1], pal[2]]
    need_rig = not rec.get("import_front") or not (rec.get("import_back") or rec.get("back_mirror"))
    r = make_rig(rec) if need_rig else None
    if rec.get("import_front"):
        # a finished sprite supplied by the author is the front picture
        base, mask = importer.convert(os.path.join(HERE, rec["import_front"]), pal8)
        frames = [base] + importer.bob_frames(base, mask, **rec.get("bob", {}))
    else:
        base = r.render("front")
        frames = [base] + [r.render("front", dict(p)) for p in (rec["poses"] or POSES)]
    frames, used = enforce_budget(frames)
    if rec.get("import_back"):
        back, _ = importer.convert(os.path.join(HERE, rec["import_back"]), pal8, size=48)
    elif rec.get("back_mirror") and rec.get("import_front"):
        back = importer.convert_mirror(os.path.join(HERE, rec["import_front"]), pal8, 48, drop_c2=rec["back_mirror"] == "drop")
    else:
        back = r.render("back")
    return frames, back, used


def write_png(imgs, pal, path):
    n = imgs[0].shape[1]
    h = sum(i.shape[0] for i in imgs)
    im = Image.new("P", (n, h))
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    arr = np.concatenate(imgs, axis=0).astype(np.uint8)
    im.putdata(arr.ravel().tolist())
    im.save(path)


def source_hash(name):
    import hashlib
    h = hashlib.sha1(repr(sorted(RECIPES[name].items(), key=lambda kv: kv[0])).encode())
    for f in ("sdf.py", "toon.py", "rig.py", "parts.py", "plans.py", "gen.py", "importer.py"):
        h.update(open(os.path.join(HERE, f), "rb").read())
    for key in ("import_front", "import_back"):
        if RECIPES[name].get(key):
            h.update(open(os.path.join(HERE, RECIPES[name][key]), "rb").read())
    return h.hexdigest()


def build(slug, out_dir):
    """Render slug's recipe into out_dir (front.png, back.png).  Skipped when the files are current (hash of recipe and engine sources)."""
    name = slug.upper()
    os.makedirs(out_dir, exist_ok=True)
    rec = RECIPES[name]
    hf = os.path.join(out_dir, ".gen_hash")
    hsh = source_hash(name)
    if os.path.exists(hf) and open(hf).read().strip() == hsh and all(os.path.exists(os.path.join(out_dir, f)) for f in ("front.png", "back.png")):
        return -1
    frames, back, used = render(name)
    pal = palette(rec)
    write_png(frames, pal, os.path.join(out_dir, "front.png"))
    write_png([back], pal, os.path.join(out_dir, "back.png"))
    open(hf, "w").write(hsh + "\n")
    return used


def sheet(names, path="/home/claude/scratch/spr/sheet.png", scale=4):
    import preview
    items = []
    for nm in names:
        frames, back, used = render(nm)
        pal = palette(RECIPES[nm])
        items += [(frames[0], pal), (back, pal)]
        print(nm, "tiles", used)
    preview.sheet(items, path, scale=scale)


def _build_job(name):
    root = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    return name, build(name.lower(), os.path.join(root, "gfx", "pokemon", name.lower()))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    names = [a.upper() for a in sys.argv[2:]] or list(RECIPES)
    if cmd == "sheet":
        sheet(names)
    elif cmd == "all":
        # render every recipe that is not current into gfx/pokemon/<slug>, two at a time
        from multiprocessing import Pool
        with Pool(2) as pool:
            for nm, used in pool.imap_unordered(_build_job, names):
                print(nm, "tiles" if used >= 0 else "current", used if used >= 0 else "")
    elif cmd == "stats":
        for nm in names:
            frames, back, used = render(nm)
            print(nm, used)
