# Map design notes (Alpha 3)

Why: the alpha-1 feedback said the maps were boxes. Corridors ran straight north, every town was the same plaza, the ground was flat and bare. This file lists the old-school
techniques the rework uses, where each one lives in the generator, and what is still open. Everything is generated (tools/hardcore/areas/*), nothing is hand placed.

## Techniques taken from the classic games

| Technique (where the classics did it) | What it does here | Code |
|---|---|---|
| **S-bends and a wide/narrow rhythm** (Routes 29/30/31, Mt. Moon, Viridian Forest) | Every road lane is a walk of 2..3 corridor segments that shifts sideways by 2..4 blocks and swells into a clearing every few rows. The corridor stays 3 blocks wide where trainers stand, so sight lines still cover it. | `areas/trail.py walk()` |
| **Tree line along the road, scenery behind it** (Route 30/31 borders, Ilex Forest) | The edge of the lane is a wall of tree blocks, the space behind it is landscaped: ponds with shores, fenced meadows, flower beds, groves. The player sees the landscape and is not allowed into it, which is what makes the road feel like it passes through something. | `trail.landscape()`, `art/scenery.py` |
| **Side-path rewards behind a one-block mouth** (item balls in Route 32/33 grass, Cherrygrove's hidden corners) | Glades hang off the road through a one-block mouth. Each holds the item ball of the lane, a hermit who talks (about 80 percent of lanes) and a hidden item (a bg event, no object slot). Pockets are dead ends on purpose: a detour can never skip a fight. | `trail.glade()`, `builder.pickup()`, `builder.furnish_lane()` |
| **A town is a hub with districts** (Goldenrod, Cianwood, Olivine) | `plaza2` builds an S-shaped main street, then districts, each with a landmark (fountain, park, market, garden, terrace, lake). Pokecenter, Mart and houses stand in a shuffled skyline along the street, trees close the town edges. Every town differs from the next in layout and decor. | `areas/town.py` |
| **Ledges as one-way terraces** (Route 29/30/31/32) | One hop-down block exists in every tileset. Used as terraces at the town edge. | `scenery.ledge`, `town.decorate` |
| **Fences and ponds that shape the path** (Route 34, Azalea, Cherrygrove) | Rails, pond blocks with nine shore pieces and a round pool block. No Surf in this hack, so water is pure scenery and a wall. | `scenery.py` |
| **Route, then gate hall, then town** (Route 29 gate, Route 35 gate) | Tithe Road ends in the checkpoint gate hall; plain connections between different tilesets crashed the game, so only same tileset maps are connected. | `areas/a1.py` |
| **Every checkpoint special** | Each area has its own palette, tileset art (five tilesets) and decor mix. A town is guaranteed reachable: the generator retries until every door front, the exit and a grass cell are connected (`layout.reach`). | `town.plaza2` |
| **Doormat exits for open air rooms** | The Amphitheater is a 9x9 outdoor room. A DOOR tile on the last row steps the player off the map on arrival (the engine walks you down out of a door), which reset the game. Open air rooms now exit over a warp carpet block, as vanilla interiors do. | `scenery.mat`, `cameos.amphitheater` |

## Numbers
- Tilesets: 168..188 of 192 tiles used, 62 blocks each (19 scenery blocks plus the mat, about 33 tiles per tileset).
- Maps: 252 generated maps, 1080 trainers. Kill totals unchanged (Grove, Axiom, Lotus 200; Tithe, Dis 199), milestones 200 and 800 still hold.
- Block rule: (w+6)(h+6) <= 1300 for every map; at most 15 objects per map; at most 23 distinct outdoor sprites per group.

## Tests
- `tools/hardcore/spawn.py` and `spawns.json` give the tests the real spawn cell, street cell and grass cell of every plaza, so tests follow the generated geometry.
- `walk_all.sh N` walks area N with a god-mode test ROM (areamodel.py plans over the emitted maps, PyBoy drives it). Soft blocks are detours around item balls and fallen
  trainers. A walk that never reaches a door can be a **game reset**, not a slow fight: check `wMapGroup` after the last step (0 or 255 means reset).

## Open
- TitheRoad (Johto tileset) still has the old straight lane, the Johto kits have no scenery blocks.
- The Tithe junction and the Purgatorio hub are not reworked.
- Townsfolk crowds (`builder.crowd`) exist but are not placed yet; hermits are 18 of 30 lanes.
