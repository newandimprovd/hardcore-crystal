# Hardcore Crystal, alpha 1 (test build, not a release)

ROM: `HardcoreCrystal_alpha1.gbc` (2 MB, Game Boy Color, MBC3 with battery, built from the `hardcore-crystal` branch on pret/pokecrystal 3bc8daa).
Runs in any GBC emulator (mGBA, SameBoy, BGB) or on a flash cart. Use a real save slot: the game saves like Crystal does.
**Adults only.** The new-game screen says so. This file contains spoilers on purpose, it is for the author.

## What the alpha is for
Finding what breaks or feels wrong in a full run. It is not balanced and not finished. Nothing in it is final, and the final ROM will only be cut
after the author approves a change list.

## Controls and defaults that differ from vanilla
- Hold **B** while walking to run (a game with about 1000 mandatory fights needs it).
- Text speed fast, battle scene off, battle style set (all changeable in OPTION).
- New game shows an adults-only screen (plain wording, it does not hint at the story).

## How far it plays
1. Vanilla-looking start: bedroom, Mom, New Bark Town, Elm's lab, starter, Route 29, Cherrygrove. Checked by `tools/hardcore/test_intro.py` on the real ROM.
2. First kill (TIMMY in Cherrygrove) reveals the player. Kill counter, corpses, trainer death in every later fight.
3. Five generated areas, about 996 mandatory trainers: Tithe City, the Commune and the Grove, the Union and Axiom, the Lotus Coast, Dis / Cocytus / Judecca.
   Every area passes the full automatic walk.
4. Kill 200: the tidal wave news and the flooded south of New Bark Town. Kill 800: the rival (a crimelord) falls, New Bark Town becomes a crater with a portal into Area 5.
5. Normal ending: final boss FINNEGAN falls, crater rim, Elm checks the fully evolved starter, Hall of Fame, credits, Continue in the bedroom.
6. Wild encounters: tall grass in all 35 plazas, the base form of every one of the 62 lines can be caught.
7. 62 four-stage lines (evolve at 25, 50, 75), 248 species (97 new), Fairy type, Showdown move set and the physical/special split per move.

## Things worth trying first
- Start a new game and play to the first kill without cheats. Does anything before Cherrygrove look or sound wrong? (nothing there may hint at the twist)
- Walk a whole area at your own pace: are the lanes readable, do Pokecenters and marts appear often enough, is the grass easy to find?
- Catch a base form in the grass of each area and level it. Do the evolve levels (25/50/75) feel right against the trainer levels?
- Reach kill 200 and 800 and read the story texts.
- Lose a fight on purpose (whiteout) in each area and see where you wake up.

## Known issues and gaps (all expected in this alpha)
- Art: the 95 new species except CTHUSPAWN and CTHULUDON still use tinted vanilla sprites. Cries are vanilla. Trainer battle portraits are scaled-up overworld sprites.
  Interiors (houses, Pokecenters, marts, gatehouses) still use vanilla tiles. Music is vanilla.
- Credits do not name Claude yet.
- The Outboard key item has no place yet. Purgatorio, the Abyss, Nick's Landing, Steiner, Sabbah, Cioran, the Crowley quest, the Corkboard and the true ending are not built.
- Elm keeps the evolved starter at the ending instead of handing it back (keeps the party safe from a removal bug).
- No wild water encounters on the Lotus Coast.
- Balance is untested: wild levels vs trainer levels, one-shots from late-area enemies, Destiny Bond on the APPARITION and MIASMA lines, how fast a level-1 base form can catch up.
- The Pokedex number shows the species ID, not the line order.
- Final boss text is a placeholder.

## Tests that passed on this build
Five full area walks, milestone 200 and 800, New Bark crater, rival, ending, whiteout, reveal, roster table check, wild table check, wild encounters in all five areas,
and the real-start test (title, intro, Mom, Elm, starter, Route 29, Cherrygrove, TIMMY, reveal).
