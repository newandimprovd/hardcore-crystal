"""Core data model and emitters for the Hardcore Crystal area generator.

A World holds map groups, maps, generated trainers, event flags and text pools. emit() writes
plain assembly and .blk files that the normal build includes, so the tree always builds from source.
"""
import os
import re
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def camel_to_const(name):
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)
    return s.upper()


def read(path):
    return open(os.path.join(ROOT, path)).read()


def write(path, text, binary=False):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb" if binary else "w") as f:
        f.write(text)


# ---------------------------------------------------------------- constants parsed from the tree

def trainer_classes():
    """Class name -> 1-based class id, from constants/trainer_constants.asm."""
    out = OrderedDict()
    n = 0
    for l in read("constants/trainer_constants.asm").splitlines():
        m = re.match(r"\s*trainerclass (\w+)", l)
        if m:
            if m[1] != "TRAINER_NONE":
                n += 1
                out[m[1]] = n
    return out


def free_event_flags():
    """Event flag indices that no EVENT_* constant uses: 2048..2847 first, then the holes below 2048."""
    v = 0
    used = set()
    for l in read("constants/event_flags.asm").splitlines():
        l = l.split(";")[0]
        if re.match(r"\s*const_def", l):
            v = 0
        elif re.match(r"\s*const_next\s+(\d+)", l):
            v = int(re.match(r"\s*const_next\s+(\d+)", l)[1])
        elif re.match(r"\s*const_skip", l):
            v += 1
        elif re.match(r"\s*const EVENT_", l):
            used.add(v)
            v += 1
    holes = [i for i in range(2048) if i not in used]
    return list(range(2048, 2848)) + holes


# ---------------------------------------------------------------- maps

class Warp:
    def __init__(self, m, x, y, kind="door"):
        self.m, self.x, self.y, self.kind = m, x, y, kind
        self.dest = None

    @property
    def index(self):
        return self.m.warps.index(self) + 1


class ForeignWarp:
    """A warp that lives in a vanilla map (hand-edited): only its map constant and warp number are needed."""

    def __init__(self, const, index):
        class _M:
            pass
        self.m = _M()
        self.m.const = const
        self.m.name = const
        self._index = index
        self.dest = None

    @property
    def index(self):
        return self._index


def link(a, b):
    """Make warps a and b lead to each other."""
    a.dest, b.dest = b, a


class MapDef:
    def __init__(self, group, name, w, h, tileset, env, landmark, music, pal="PALETTE_DAY",
                 fish="FISHGROUP_NONE", border=0, const=None):
        self.group, self.name, self.w, self.h = group, name, w, h
        self.const = const or camel_to_const(name)
        self.tileset, self.env, self.landmark, self.music = tileset, env, landmark, music
        self.pal, self.fish, self.border = pal, fish, border
        self.blocks = bytearray(w * h)
        self.warps, self.objects, self.bgs, self.coords = [], [], [], []
        self.connections = {}  # direction -> (MapDef, offset)
        self.scripts = []  # extra asm chunks
        self.object_consts = []
        self.callbacks = []  # (type, label)

    def set(self, bx, by, b):
        assert 0 <= bx < self.w and 0 <= by < self.h, (self.name, bx, by)
        self.blocks[by * self.w + bx] = b

    def get(self, bx, by):
        return self.blocks[by * self.w + bx]

    def fill(self, b, x0=0, y0=0, x1=None, y1=None):
        x1 = self.w if x1 is None else x1
        y1 = self.h if y1 is None else y1
        for y in range(y0, y1):
            for x in range(x0, x1):
                self.set(x, y, b)

    def warp(self, x, y, kind="door"):
        w = Warp(self, x, y, kind)
        self.warps.append(w)
        return w

    def obj(self, x, y, sprite, move, script, pal="0", otype="OBJECTTYPE_SCRIPT", sight=0, flag="-1", rad=(0, 0)):
        self.objects.append(dict(x=x, y=y, sprite=sprite, move=move, pal=pal, otype=otype, sight=sight,
                                 script=script, flag=flag, rad=rad))
        assert len(self.objects) <= 15, f"{self.name}: more than 15 objects"
        return len(self.objects)

    def bg(self, x, y, func, script):
        self.bgs.append((x, y, func, script))

    def connect(self, direction, other, offset):
        self.connections[direction] = (other, offset)

    @property
    def label(self):
        return self.name

    def events_asm(self):
        o = [f"{self.name}_MapEvents:", "\tdb 0, 0 ; filler", "", "\tdef_warp_events"]
        for w in self.warps:
            d = w.dest
            assert d is not None, f"unlinked warp in {self.name} at {w.x},{w.y}"
            o.append(f"\twarp_event {w.x:2d}, {w.y:2d}, {d.m.const}, {d.index}")
        o += ["", "\tdef_coord_events"]
        for (x, y, scene, script) in self.coords:
            o.append(f"\tcoord_event {x:2d}, {y:2d}, {scene}, {script}")
        o += ["", "\tdef_bg_events"]
        for (x, y, func, script) in self.bgs:
            o.append(f"\tbg_event {x:2d}, {y:2d}, {func}, {script}")
        o += ["", "\tdef_object_events"]
        for ob in self.objects:
            o.append("\tobject_event %2d, %2d, %s, %s, %d, %d, -1, -1, %s, %s, %d, %s, %s" % (
                ob["x"], ob["y"], ob["sprite"], ob["move"], ob["rad"][0], ob["rad"][1], ob["pal"],
                ob["otype"], ob["sight"], ob["script"], ob["flag"]))
        return "\n".join(o) + "\n"

    def asm(self):
        o = []
        o.append("\tobject_const_def")
        for i, c in enumerate(self.object_consts):
            o.append(f"\tconst {self.const}_{c}")
        o.append("")
        o.append(f"{self.name}_MapScripts:")
        o.append("\tdef_scene_scripts")
        o.append("")
        o.append("\tdef_callbacks")
        for (t, lab) in self.callbacks:
            o.append(f"\tcallback {t}, {lab}")
        o.append("")
        o += self.scripts
        o.append(self.events_asm())
        return "\n".join(o) + "\n"


class Group:
    def __init__(self, key, sprites, roof=-1, sgb="PREDEFPAL_ROUTES",
                 roofpal=((21, 21, 21, 11, 11, 11), (21, 21, 21, 17, 8, 7))):
        self.key = key  # e.g. "AREA1"
        self.camel = key.title().replace("_", "")
        self.maps = []
        self.sprites = sprites
        self.roof = roof
        self.roofpal = roofpal
        self.sgb = sgb

    def add(self, m):
        self.maps.append(m)
        return m


class World:
    def __init__(self):
        self.groups = OrderedDict()
        self.classes = trainer_classes()
        self.flag_pool = free_event_flags()
        self.flag_next = 0
        self.flag_names = []  # (name, index)
        self.trainers = defaultdict(list)  # class const -> [(name, party)]
        self.spawns = []  # (const, map, x, y)
        self.landmarks = []  # (const, x, y, name)
        self.marts = []  # (const, label, items)
        self.pools = OrderedDict()  # pool label -> list of text strings
        self.extra_asm = []
        self.story = []  # (trainer class, id, kind) of bosses that run a story script after their death

    def group(self, key, sprites, **kw):
        g = Group(key, sprites, **kw)
        self.groups[key] = g
        return g

    def flag(self, name):
        idx = self.flag_pool[self.flag_next]
        self.flag_next += 1
        self.flag_names.append((name, idx))
        return name

    def trainer(self, cls, name, party):
        """Register a generated trainer, returns its id (>= 128)."""
        assert cls in self.classes, cls
        assert len(name) <= 10, name
        lst = self.trainers[cls]
        lst.append((name, party))
        tid = 127 + len(lst)
        assert tid <= 255, f"too many generated {cls} trainers"
        return tid

    def all_maps(self):
        for g in self.groups.values():
            for m in g.maps:
                yield g, m
