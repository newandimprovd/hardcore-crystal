"""Party generation for generated trainers, using the four-stage roster."""
import json
import os
import random
from collections import Counter, deque

from .model import ROOT

NAMES = """ABEL ADRIAN AL ALDO AMOS ANDRE ARLO ARNIE ASHER AUGUST BARRY BART BEN BERT BILLY BLAKE BOYD BRAD
BRAM BRUNO BUCK BYRON CAL CARL CASEY CECIL CHAD CHUCK CLEM CLYDE COLE CORY CURT DALE DAN DANTE DARREN
DAVE DEAN DENNIS DEREK DIRK DOUG DREW DUANE DUKE DWAYNE EARL ED ELI ELMER ERIC ERNIE EVAN FELIX FRANK
FRED GARY GENE GIL GLEN GREG GUS HANK HARV HOMER HUGH IAN IRA ISAAC JACK JAKE JAY JED JESS JIM JOEL
JON KARL KEN KIRK KURT LANCE LARRY LEE LEN LEO LEW LOU LUKE LYLE MACK MARV MAX MEL MIKE MILO MORT
NATE NED NEIL NICK NOAH NORM OLAF OMAR ORVAL OSCAR OTIS OWEN PAT PAUL PETE PHIL QUINN RAY REX RICK ROB
ROD ROY RUSS RYAN SAM SEAN SETH SID STAN STU TED TIM TOBY TODD TOM TONY TY VAL VERN VIC WADE WALT WES
WILL ZACK ABBY ADA ALMA AMY ANITA ANN AVA BECKY BELLA BESS BETH BLANCHE BONNIE BRENDA CARA CARLA CARMEN
CHLOE CLARA CORA DAISY DANA DAWN DEB DEE DELIA DIANA DORA EDNA ELLA ELSA EMMA ERIN ESTHER EVE FAY FERN
FIONA FLO GAIL GINA GLORIA GRACE HANNAH HAZEL HEIDI HOPE IDA INEZ IRIS IVY JADE JAN JEAN JILL JOAN JUNE
KAREN KATE KAY KIM LANA LAURA LEAH LENA LILA LISA LOLA LORI LUCY LYNN MABEL MAE MAGGIE MARA MEG MIA MINA
MONA NELL NINA NORA OLGA OPAL PAM PEARL PEGGY PENNY PHYLLIS RITA ROSA ROSE RUBY RUTH SADIE SALLY SARA
SHEILA SUE TARA TESS TINA TRUDY UMA VERA VIOLA WANDA WENDY YVONNE ZOE""".split()


# One booster per type (the held items of generation 2).  There is no Fairy booster in the item list, so a Fairy mon takes one of the
# general items instead.
BOOSTER = {
    "NORMAL": "PINK_BOW", "FIGHTING": "BLACKBELT_I", "FLYING": "SHARP_BEAK", "POISON": "POISON_BARB", "GROUND": "SOFT_SAND",
    "ROCK": "HARD_STONE", "BUG": "SILVERPOWDER", "GHOST": "SPELL_TAG", "STEEL": "METAL_COAT", "FIRE": "CHARCOAL", "WATER": "MYSTIC_WATER",
    "GRASS": "MIRACLE_SEED", "ELECTRIC": "MAGNET", "PSYCHIC_TYPE": "TWISTEDSPOON", "ICE": "NEVERMELTICE", "DRAGON": "DRAGON_SCALE",
    "DARK": "BLACKGLASSES",
}
# The general items by tier: (item, weight at level < 25, at 25 to 49, at 50 and up).  Early teams carry berries, late teams carry the
# items that decide a fight (a survival chance, a priority chance, extra critical hits, a flinch chance, a heal every turn).
GENERAL = [
    ("BERRY", 5, 2, 0),
    ("GOLD_BERRY", 0, 3, 3),
    ("BERRY_JUICE", 0, 1, 1),
    ("PSNCUREBERRY", 1, 0.5, 0), ("PRZCUREBERRY", 1, 0.5, 0), ("BURNT_BERRY", 1, 0.5, 0), ("ICE_BERRY", 1, 0.5, 0),
    ("MINT_BERRY", 1, 0.5, 0), ("BITTER_BERRY", 1, 0.5, 0),
    ("MIRACLEBERRY", 0, 1, 2),
    ("FOCUS_BAND", 0.5, 1.5, 2.5),
    ("QUICK_CLAW", 0.5, 1.5, 2),
    ("SCOPE_LENS", 0.5, 1.5, 2),
    ("KINGS_ROCK", 0.5, 1.5, 2),
    ("LEFTOVERS", 0, 1.5, 3.5),
    ("BRIGHTPOWDER", 0.5, 1, 1),
    ("CLEANSE_TAG", 0, 0.5, 1),
]


class Roster:
    def __init__(self):
        d = json.load(open(os.path.join(ROOT, "tools/hardcore/roster/roster_out.json")))
        self.mons = d
        self.by_stage = {s: [m for m in d if m["stage"] == s] for s in (1, 2, 3, 4)}
        self.by_const = {m["const"]: m for m in d}
        # How often each species was handed out in this run, and the last ones handed out.  A trainer team is drawn against both, so one
        # theme no longer turns every team of an area into the same five species.
        self.used = Counter()
        self.picks = Counter()
        self.recent = deque(maxlen=30)

    @staticmethod
    def stage_for(level):
        return 1 + (level >= 25) + (level >= 50) + (level >= 75)

    def pick(self, rng, level, theme, taken=(), floor=0.35, hard=False):
        """theme: dict type -> weight.  Chooses a species of the stage that fits the level: a trainer never has an unevolved form of a
        stage the level has already passed (the unevolved high level mons are the wild ones).  taken: the species already in the team, whose
        evolution lines and doubled types are drawn against.  hard: the named fights; the weak forms of the stage (below nine tenths of the
        stage's average total) are out and the strong ones are drawn far more often."""
        stage = self.stage_for(level)
        pool = self.by_stage[stage]
        avg = sum(sum(m["stats"]) for m in pool) / len(pool)
        lines = {self.by_const[c]["line"] for c in taken}
        tcount = Counter(t for c in taken for t in set(self.by_const[c]["types"]))
        expected = self.picks[stage] / len(pool) + 1
        weights = []
        for m in pool:
            if m["line"] in lines:
                weights.append(0)
                continue
            w = max(theme.get(t, 0) for t in m["types"])
            w = w if w > 0 else floor
            w /= 1 + (self.used[m["const"]] / expected) ** 2
            if hard:
                r = sum(m["stats"]) / avg
                w = 0 if r < 0.9 else w * r ** 4
            if m["const"] in self.recent:
                w *= 0.25
            if any(tcount[t] >= 2 for t in set(m["types"])):
                w *= 0.1
            weights.append(w)
        m = rng.choices(pool, weights)[0]
        self.used[m["const"]] += 1
        self.picks[stage] += 1
        self.recent.append(m["const"])
        return m

    def item_for(self, rng, mon, level, taken_items=()):
        """A held item for one mon: a booster of one of its types, or a general item of the tier.  A team never repeats an item."""
        tier = 0 if level < 25 else 1 if level < 50 else 2
        opts = []
        for t in set(mon["types"]):
            if t in BOOSTER:
                opts.append((BOOSTER[t], (4, 7, 7)[tier]))
        for name, *ws in GENERAL:
            if ws[tier] > 0:
                opts.append((name, ws[tier]))
        opts = [(n, w) for n, w in opts if n not in taken_items]
        return rng.choices([n for n, _ in opts], [w for _, w in opts])[0]


def party_size(rng, progress, max_size=6):
    base = 1 + progress * 4.2
    n = int(round(base + rng.uniform(-0.9, 0.9)))
    return max(1, min(max_size, n))


def item_chance(level, last):
    """The chance that a mon carries an item: the last (strongest) mon of a team always does from level 10, the rest more and more often."""
    if last:
        return 1.0 if level >= 10 else 0.5
    return min(0.85, 0.15 + level / 90)


def make_party(roster, rng, level, size, theme, hard=False):
    """Returns [(level, SPECIES, ITEM)] with the strongest mon last (the money reward uses the last mon).  ITEM is NO_ITEM for a mon without one.
    A team takes exactly one draw from the caller's source and rolls with a source of its own, so tuning the teams never re-rolls the maps.
    hard (the fights of the named characters): every mon is at the level or above it, the strong forms of the stage are preferred and every
    mon carries an item."""
    rng = random.Random(rng.getrandbits(32))
    lvs = []
    for i in range(size):
        if hard:
            lvs.append(min(100, level + rng.randint(0, 2) + (2 if i == size - 1 else 0)))
        else:
            lvs.append(min(100, max(2, level + rng.randint(-2, 1) + (2 if i == size - 1 else 0))))
    if level >= 99:  # Area 5 and everything at its end: every mon is level 100
        lvs = [100] * size
    lvs.sort()
    taken = []
    for lv in lvs:
        taken.append(roster.pick(rng, lv, theme, taken, hard=hard)["const"])
    mons, items = [], []
    for i, (lv, sp) in enumerate(zip(lvs, taken)):
        it = "NO_ITEM"
        if hard or rng.random() < item_chance(lv, i == size - 1):
            it = roster.item_for(rng, roster.by_const[sp], lv, items)
            items.append(it)
        mons.append((lv, sp, it))
    return mons
