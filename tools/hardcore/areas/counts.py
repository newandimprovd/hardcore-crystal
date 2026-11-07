"""Battle budget of the game: one place for every number of fights.

  * MANDATORY = 500 normal trainers on the roads, in the lanes and the first kill (Timmy), 100 for each of the five areas.  Bosses and cameo
    duels are special encounters and are counted separately; so is everything in Purgatorio.
  * The whole game stays at or under TOTAL_CAP = 650 battles (tools/hardcore/battle_budget.py checks the emitted maps).
  * A lane keeps its length when it holds fewer fighters: trail() spaces the trainers GAP block rows apart, so the room between them goes to the
    scenery, the glades and the neutral people.

The tidal wave (the radio news about New Bark Town) arrives on kill TSUNAMI_KILLS = 400, the author's number.  It is emitted as HC_TSUNAMI_KILLS
(constants/area_event_flags.asm) so the engine never hard-codes it.  The crater comes with the fall of the rival, the last boss of Area 4
(rival_kills())."""

AREAS = 5
MANDATORY = 500
PER_AREA = MANDATORY // AREAS  # 100
TOTAL_CAP = 650
ROAD_TRAINERS = 6  # Tithe Road
TIMMY = 1  # the first kill, in Cherrygrove
BOSSES_PER_AREA = 3
GAP = 2  # block rows between two trainer rows of a lane
LANES = 15  # 3 acts of 5 lanes
TSUNAMI_KILLS = 400  # the radio news of the tidal wave comes with this kill (New Bark Town floods)


def spread(total, n):
    """total split over n lanes as evenly as possible (the larger ones spread out, not bunched)."""
    base, extra = divmod(total, n)
    return [base + (1 if (i + 1) * extra // n > i * extra // n else 0) for i in range(n)]


def lanes_of(area):
    """Trainers per lane for area 1..5 as the three acts of five lanes."""
    total = PER_AREA - (TIMMY + ROAD_TRAINERS if area == 1 else 0)
    flat = spread(total, LANES)
    r = (4 * area) % LANES  # every area starts its pattern somewhere else
    flat = flat[r:] + flat[:r]
    return tuple(flat[5 * k:5 * k + 5] for k in range(3))


def rival_kills():
    """Kills when the rival falls (the crater): every normal trainer of Areas 1 to 4 and the bosses of Areas 1 to 3 and the rival."""
    return 4 * PER_AREA + 4 * BOSSES_PER_AREA


def drop_tiers():
    """Kill counts at which the item drops of trainers improve: 10, 20 and 35 percent of the mandatory kills."""
    return tuple(MANDATORY * p // 100 for p in (10, 20, 35))
