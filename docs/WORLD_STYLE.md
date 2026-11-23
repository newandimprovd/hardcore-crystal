# World and town style: Sinnoh and Unova as the guide

Direction from the author (alpha 3.2 playtest, 23 Nov 2026): the buildings of a town stand apart from each other, like in the towns of Sinnoh and Unova, and those two regions are the guide
for the building of towns and of the world. Earlier direction: the world is a mixture of Sinnoh and Hoenn. This file keeps the rules in one place, what is built, and what is not.

## Rules for a town

1. **Every building is a free standing block** on open ground, never part of a row or a wall. Between two buildings there is always at least one block (two steps) of open ground.
2. **Every door has an apron and a path.** The block under the door is paved, and a paved path (cheapest walk, few turns) runs from it to the main street. A building can face the street directly.
3. **A building has a yard.** The ring of ground round it carries flowers and the odd tree, the front stays clear.
4. **The street is the spine.** One street runs from the way in at the bottom to the way out at the top, with a bend (the street band) in between, and every path joins it.
5. **Districts fill the open ground between the buildings**: a fountain square, a park, a market, a garden, a terrace, a lake, an orchard, a cloister, a promenade, a hedge maze. Every town has a patch of tall grass.
6. **The way in is a procession.** The bottom stem of the first town of an area is an avenue lined with trees and flower beds.
7. **The edge of a town is runs of trees and runs of house backs**, so no wall of fused facades shuts the town in. The towns of the wild areas (Grove, Lotus) have trees all round.

Implemented in `tools/hardcore/areas/town.py` (`build_plaza`: placement with a halo of one block round every footprint, `path_between` for the paths, `free_rects` for the districts,
`decorate` for the district kinds). Every town is checked by `plaza2` (every door and the exit are reachable on foot, the grass patch can be reached) and by the walker (`walk_all.sh`).

## Rules for the world (routes)

1. **A route has things to find beside the way**: glades with a pond, an orchard, a garden or a meadow, lakes, clearings and groves (`trail.py`), each on a different side and height.
2. **Routes bend** east and west (turned lanes), they are not a straight run north.
3. **Hidden places** on the side: the Undercroft, the ten hollows (caves with fighters, hermits, balls, a sign and a plaque), reached through a one block gap in a tree line.

## What is not built yet (said plainly)

- **Towns with three or four exits.** The towns have two (south and north). Sinnoh and Unova towns are crossroads. Side exits need a spur route per exit, a second kind of map connection and a walker that visits a
  branch and comes back (the walker only follows one chain now).
- **Roads that run south or loop** back to an earlier town (shortcuts that open later).
- **Bridges and water routes.** No bridge tile exists in the five tilesets, and the tile budget (192 of 192 tiles) has no room for one without removing something.
- **Landmarks with a silhouette** (a tower, a ferris wheel, a cathedral) need new tiles, see the tile budget above.
- **Building facades that face east or west** need an engine change (see `docs/REFERENCE_STUDY.md`, corrected in alpha 3.2).
