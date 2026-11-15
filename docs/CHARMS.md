# Charms and hidden people

Thirty people hide in the world, each with a boost. Twelve of them live in the glades of the five areas' lanes and give their present for nothing.
Eighteen are the hermits of Purgatorio (areas/purg.py), who give theirs after a fight. A present is either a **charm** or a stat item.

## The six charms

Charms are key items: they cannot be tossed, they take no room in the item pocket and they work as long as they are in the bag. They replace six unused
APRICORN slots, so the item count did not change. Every effect is a small routine that asks `HC_HasCharm` (home/item.asm) whether the charm is carried.

| Charm | Effect | Where the code is |
|---|---|---|
| EXP CHARM | experience from every fight times 6/5 | `HC_ExpCharm`, engine/battle/core.asm, called after the Lucky Egg boost |
| PURSE CHARM | money from a body times 3/2 | `HC_RollLoot`, engine/hardcore/trainer_death.asm |
| CATCH CHARM | catch rate a quarter better (255 at most) | `HC_CatchCharm`, engine/items/item_effects.asm, in `PokeBallEffect` |
| LOOT CHARM | a body drops an item in 96 of 256 cases instead of 64 | `HC_RollItemDrop`, engine/hardcore/trainer_death.asm |
| HEAL CHARM | every four steps each living party member regains 1 HP plus 1/128 of its maximum | `HC_HealStep`, engine/events/poisonstep.asm |
| LULL CHARM | wild encounter rate a quarter lower | `HC_ApplyLullCharm`, engine/overworld/wildmons.asm |

`tools/hardcore/test_charms.py ROM` runs each routine in the emulator with and without the charm in the bag (64 checks).

## The twelve glade hermits

Defined in areas/wayfolk.py (`GIFT_HERMITS`, with their words), placed by areas/builder.py (`furnish_lane`): the first lane of the area from the
given lane on that has a glade and a free object slot gets him in place of its ordinary hermit. Generation fails if one finds no glade.

| Where | Gives |
|---|---|
| TitheRoad | LULL CHARM |
| TitheStreet8 | HP UP |
| GroveStreet3 | EXP CHARM |
| GroveStreet9 | PROTEIN |
| GroveStreet14 | CARBOS |
| AxiomStreet4 | PURSE CHARM |
| AxiomStreet11 | IRON |
| LotusStreet3 | CATCH CHARM |
| LotusStreet8 | CALCIUM |
| LotusStreet13 | PP UP |
| DisStreet5 | LOOT CHARM |
| DisStreet11 | HEAL CHARM |

Six charms and six stat items (HP UP, PROTEIN, CARBOS, IRON, CALCIUM, PP UP). Each charm exists once in the forest, so a charm is found by walking, not by farming.

## The eighteen hermits of Purgatorio

Two per floor, nine floors (PurgDown1 to PurgAbyss, PurgUp1 to PurgUp4). They are fought first and give stat items afterwards: PROTEIN, IRON, CALCIUM, CARBOS,
HP UP, LUCKY EGG, PP UP, RARE CANDY, MAX ELIXER and MAX REVIVE (the table `FLOORS` in areas/purg.py).
