"""Party generation for generated trainers, using the four-stage roster."""
import json
import os

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


class Roster:
    def __init__(self):
        d = json.load(open(os.path.join(ROOT, "tools/hardcore/roster/roster_out.json")))
        self.mons = d
        self.by_stage = {s: [m for m in d if m["stage"] == s] for s in (1, 2, 3, 4)}

    @staticmethod
    def stage_for(level):
        return 1 + (level >= 25) + (level >= 50) + (level >= 75)

    def pick(self, rng, level, theme, lower_chance=0.25):
        """theme: dict type -> weight. Chooses a species whose stage fits the level."""
        stage = self.stage_for(level)
        if stage > 1 and rng.random() < lower_chance:
            stage -= 1
        pool = self.by_stage[stage]
        weights = []
        for m in pool:
            w = max(theme.get(t, 0) for t in m["types"])
            weights.append(w if w > 0 else 0.05)
        return rng.choices(pool, weights)[0]


def party_size(rng, progress, max_size=6):
    base = 1 + progress * 4.2
    n = int(round(base + rng.uniform(-0.9, 0.9)))
    return max(1, min(max_size, n))


def make_party(roster, rng, level, size, theme):
    """Returns [(level, SPECIES)] with the strongest mon last (the money reward uses the last mon)."""
    mons = []
    for i in range(size):
        lv = max(2, level + rng.randint(-2, 1) + (2 if i == size - 1 else 0))
        mons.append((lv, roster.pick(rng, lv, theme)["const"]))
    mons.sort(key=lambda t: t[0])
    return mons
