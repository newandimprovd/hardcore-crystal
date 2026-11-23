# Hardcore Crystal, alpha 3.2 (the fix pass on your 27 point playtest list)

This file has spoilers on purpose, it is for the author. For every point it says what was built, how it was checked, and what was **not** done. Where a point asked for
art I could not draw, it says so instead of calling it done.

ROMs: `HardcoreCrystal_alpha3_2.gbc` (the game), `HardcoreCrystal_alpha3_2_sampler.gbc` (starts on Tithe Plaza 1, level 100 CTHULUDON, kills revealed, key items in the bag)
and `HardcoreCrystal_alpha3_2_ending.gbc` (starts in Judecca with the story flags of the end). The test ROMs are for looking, not for judging balance.

## Your 27 points, one by one

1. **Run animation cuts the head in half.** The side views of the run poses sheared the sprite tiles at the neck. They are rewritten (`FacingRun*` in `data/sprites/facings.asm`) so the head and
   the body move as one piece, and the second stride lifts the whole figure a pixel. `test_run.py` passes (16 frames per tile walking, 8 running, strides every 4 frames) and I looked at a
   contact sheet of all four directions: no split. It is still the existing sprite tiles posed, not new run art.
2. **Overworld sprites of trainer classes must match their battle pictures.** The cause I found was colour: the caves (Purgatorio group) loaded the vanilla NPC palettes while the battle
   portrait used the area's colours. Every cave map now names its area (`data/hardcore/purg_obj_areas.asm`, read by `HC_LoadAreaObjPalette`), so the fighters of a hollow or of the
   Undercroft wear the colours of their area. Checked by reading the object palette RAM on the road and inside a hollow: identical. **Not done:** the overworld sprite *shapes* are still the shared set
   of walking sprites, a unique overworld sprite per trainer class would be a drawing job (about 50 classes).
3. **Fountain art against collision.** The old fountain drew a 16 pixel basin in the middle of a block that was solid all over, so the player ran into air. The fountain is now a pool of two by two
   blocks (`fountain_nw` to `fountain_se` in `art/scenery.py`): the shore pieces of the ponds go round the edge and the water and the stone lip fill every pixel that the collision blocks, with the
   pedestal and the jet at the centre. The plaque is still read from the south.
4. **Battle text: the rest of the team's EXP, and the wrong name on a passive level up.** Alpha 3.1 paid the benched party members silently, which also left the defeated foe's name in the string buffer,
   so the "grew to level" line named the wrong mon. Benched members are announced like the fighters now and the line takes the nickname of the mon that grew (`GiveExperiencePoints`,
   `engine/battle/core.asm`). Not yet re-checked in a full fight with the new ROM (see the verification section).
5. **Pokecenter upstairs replaced by normal tiles.** The staircase block in `maps/Pokecenter1F.blk` (the interior every generated Pokecenter copies) is plain floor now.
6. **Unlimited TMs.** A TM is not used up (`engine/items/tmhm.asm`).
7. **Crowley.** The Amphitheater event was reworked, he speaks less, and there is a new class of special characters. **Partly done:** the quote scenes are pastiche written for this game, not the real
   texts (see the note on quotes at the end), and the children's playground flight is a short scene, not a new map.
8. **Repeating NPC conversations, personalities, sprite variety.** Every plaza now has named townsfolk with their own personality and four lines that show up in turns (`areas/persona.py`, 40 people),
   and the hermits and townsfolk of one area draw from larger pools without repeats (`fresh_line`). Sprite diversity: the NPCs pick from the area's full sprite set with a different offset, but
   there are no new NPC sprites.
9. **The Corkboard has its own page.** Opened from the bag it is a framed list of the 21 notes with a page of its own for each, like the trainer details page. `test_cork.py` passes.
10. **Structures need tiles for six directions.** **Not done.** I measured why. A metatile is a list of tile ids and the colour attributes come from the tileset's palette map, one byte per tile
    id, with no flip bit (corrected in `docs/REFERENCE_STUDY.md`). So mirrored facades need an engine change, and all five area tilesets already sit at 192 of 192 tiles. Buildings still face south.
11. **Weak early mons are stronger.** Base stats and early movesets of the first stage mons were raised (`tools/hardcore/buff_early.py`), the stat tables changed in `data/pokemon/base_stats/`.
12. **Better NPC story scripts quoting named writers.** The scripts are longer and the writers are named, but the quotations are **my own pastiche**, not verbatim passages (I do not reproduce
    passages from books or poems). `areas/quotes_override.py` is where the author can put the real lines, if you want exact quotations you have to paste them in there.
13. **Purgatorio entrances hidden.** Both the Undercroft and the ten new hollows are entered through a one block gap in a tree line in a glade that no sign points at.
14. **Trainers with the same few Pokémon.** Teams are drawn against how often each species has already been handed out, against the last 30 picks, and never repeat a line or double a type.
15. **Purgatorio exit to the Crossroads showed two tiles but one worked.** The exit corridor of the hub is two steps wide and only the right step was a warp carpet. The last row is now block 0x40 with a carpet under both steps and both warps lead out (`hub()` in `areas/purg.py`).
16. **Characters speak too much too early.** The named characters tell their story in several short visits (a `.Later` block per character); the first meeting is a line or two.
17. **Corridors are boring, more tile diversity.** **Partly done.** New plaza districts (an orchard, a cloister, a promenade, a hedge maze) and an avenue of honour at every area's entrance.
    No new tiles (the tile budget is spent), so the variety comes from new arrangements of the blocks we have.
18. **The Parish feels like one building, the Commune entrance needs glory.** **Partly done.** The entrance of every area (the Commune included) is now a processional, the stem from the gate to the
    first bend is lined with trees and beds. The Parish is still built from the same house and facade blocks as every other town, a real cathedral needs new art that the tile budget does not allow.
19. **Checkpoints share one layout, the map always goes north, crisscross like Hoenn and Sinnoh.** **Partly done.** Lanes now bend east and west (turned lanes) in all five areas, and the walker follows
    them. The road never runs south, and the checkpoint houses still share a layout.
20. **Held items and diverse teams.** One booster per type plus tiered general items (berries early, Leftovers, Focus Band, Quick Claw and the like later). The last mon of a team always carries one.
21. **The EXP charm and the level ranges.** The EXP CHARM is in a ball on the last floor of the Undercroft of Area 3, behind a hidden portal. The lane fighters of the five areas are generated between levels 5 and 22,
    25 and 47, 50 and 72, 75 and 97, and 99 and 100 (`l0, l1` in `areas/a1.py` to `a5.py`), with the bosses and named fights standing at the top of each band (up to 25, 50, 75 and 100)
    and the hollows two levels above the lane they hide beside.
22. **Modern maps, a hybrid map.** The ten hollows, the lane bends and the new districts take the Hoenn and Sinnoh idea of side branches and hidden places. A full second map system (the modern
    tileset everywhere) was **not** done.
23. **Rival encounters.** Praised, left alone.
24. **No unevolved trainer mon past its evolution level.** The roster has four stages and a trainer only draws from the stage that fits the level. Wild unevolved high level mons are untouched.
25. **Extra mandatory Crowley encounter, Amphitheater cinematic, six mon Crowley battle.** **Partly done**, see point 7. Crowley's class is Poet. A full cinematic with camera movement is not built.
26. **Pokecenter healing costs ten times more.** `engine/hardcore/nurse.asm`; `test_nurse.py` plays both centers by key presses.
27. **The Alleycat sprite, the leg raising animation.** The Alleycat and the Kingpin were re-rendered as slimmer cats with a raised tail and a round head, but this is still the generated 3D to pixel
    pipeline, I did not hand draw it. I could not find a raised leg in the idle frames of the generator (the quadruped has no leg pose), so what you saw may come from a battle animation,
    tell me when it shows. I am not happy with the sprites in general either, and real hand drawn art for the 97 new species is still the biggest open job.

## What is new and was not on your list

- **Ten hollows.** Two small hidden caves in every area (the Alms Cellar, the Ossuary, the Hollow Oak, the Moss Chapel, the Spare Room, the Break Room, the Dry Pool, the Last Cabana, the Filing
  Pit, the Furnace Room). Each has five fighters (plain fights, nobody dies, no kill count), two hermits who give a present after their fight, two item balls, a sign by the ladder and a plaque
  at the far end that tells the place's story. This is the answer to "a lot to fight and nothing to explore". `test_hollow.py` walks the first one end to end (PASS).
- **Per-map object palettes in the caves**, see point 2.

## What is tested, and how

See the verification section at the end of this file, written after the last run.

## Known gaps, in one place

Overworld sprite shapes per trainer class, run art, hand drawn creature art, six direction facades (needs an engine change), a real Parish cathedral, south running roads, a full cinematic for Crowley,
real quotations (only pastiche), and everything for the battle engine rework (next version).
