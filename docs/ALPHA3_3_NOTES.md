# Hardcore Crystal, alpha 3.3 (buildings, streets, sprites and the sideways layout)

This file has spoilers on purpose and is written for the author. It says what was built, how it was checked, and what was not done or only half done, because the project rule is to be plain about that.

The ROMs are `HardcoreCrystal_alpha3_3.gbc` (the game), `HardcoreCrystal_alpha3_3_sampler.gbc` (starts on Tithe Plaza 1 with a level 100 Cthuludon, the kills revealed and the key items in the bag) and `HardcoreCrystal_alpha3_3_ending.gbc` (starts in Judecca with the story flags of the end, every Pokémon in the PC, the Pokédex complete and the player named Chris). The two test ROMs are for looking and not for judging balance.

## What changed

The early game soft lock is fixed. Tackle itself was never the problem, since the engine already gave it about 95 percent. Wild foes such as Pidgey spammed Sand-Attack and stacked accuracy drops until nothing hit. Tackle is now 40 power and 100 accuracy, Pidgey learns Gust before Sand-Attack, and wild foes and trainer AI no longer pile on accuracy drops or evasion boosts past one stage.

Finnegan is no longer Lance. He has his own distorted humanoid picture and overworld figure, and he is fought on the rim of a burning volcano in a summit room with lava and lava edge blocks, not in a gym.

Buildings were reworked in four steps. Every wall piece now has a version for each of the four directions and the corners where they meet are new blocks, all composed from existing cells so the five tilesets gained blocks but no tiles. Doors used to sit under the roof post in the far corner of the front, and now the front runs window, door, window, window, so the door stands one bay in. Some houses are townhouses of three rows with a double door in the middle and a hall of six by six blocks inside. The last plaza of Tithe is built around a cathedral with two bell towers and a rose window, and beside it stand a rectory, a parish school and an almshouse with their own people and text, so the Parish no longer reads as one building. The way into each area is flanked by that area's signs and a second row of trees.

Streets differ from each other now. Every street gets a landscape type from a per area sequence (river with a causeway, lakeshore, two lakes, ruined hamlet, forest in the wild areas, avenue, canal and park in the city areas). Sixteen streets hold a hut in a glade with a room, a single dweller and one item given once, which is the start of giving the player something to find. A hut test walks in, takes the gift and walks out.

The layout runs sideways. One run of lanes in each act is turned a quarter turn, east or west, and a small bend map before and after joins it to the road that runs north. Corridors, trainers, glades, pond edges and rails turn with it, and the building fronts are picked again so they still face the street. The audits pass, and the god mode walker walked all five areas through the turns.

Dialogue repeats less. About 475 new lines for lane trainers, new lines for interiors, plaza givers and the forty five Purgatorio recluses, and 140 more lines for the glade hermits and hut dwellers, drawn from per area decks so no line is spoken twice before the pool is used up. The variety audit passes in every category (hermits 14.9 percent repeating against a limit of 20, which the bends had pushed to 37 before the new lines).

## Sprites

The 93 generated creatures were rebuilt. Every creature now stands on one ground line so size differences between stages show. A stage 3 form fills 76 percent of its picture and a stage 4 form 97 percent. Eyes have nine moods set per species (angry, sly, tired, round, addled, blank, hollow, slit and dot), at least four pixels wide, and veterans such as Kingpin carry a scar. Posture follows the mood for two legged and four legged creatures, so tired ones slouch and alert ones stand tall, and the creatures that share a body plan are turned at different angles so their silhouettes differ. Stray dither pixels are cleaned from the outlines. The rules and the code that follows them are in `docs/SPRITE_RULES.md`.

Chris, the player, is new. He is a scruffy man with tired eyes in a red jacket with a duffel over one shoulder and a ball in his hand. The overworld sheet, the front picture, the trainer card picture and the battle back picture all come from one design in `tools/hardcore/art/player.py`. I looked at him walking in all four directions in the emulator.

## What is not done or only partly done

The sprites are still generated placeholders. About fifteen of the two legged creatures share one body, and the angles and postures help but do not make them different animals. Cat and dog heads look alike from the front, so Kingpin looks like a bulldog with a coin on its head. Some palettes are garish, Alleycat most of all. Kingpin measures about 3.8 times the area of Meowth but only about twice its length, because four times the length would not fit the 56 pixel picture. Typhoneus and Hellhound use imported author art and ignore the mood tables. Kris, the female player, still has the vanilla art, and so do the trainer class battle pictures I did not redraw.

The sideways layout is a first step. Only one run per act turns, the plazas and the cathedral are never rotated, and the roads do not fork or loop back yet, so the world is closer to Hoenn's bends than to Sinnoh's crossings. The overworld walk shows the geometry works but I have not played it as a player would.

The Parish is a cathedral with three buildings beside it, but there is no narthex, and the Commune gate gets signs and tree rows, not new art, and its gate hall inside is unchanged. Doubled doors exist only on townhouses and the cathedral.

You said the game still had leftover discontinuities and was a broken mess, and I never learned which ones. The continuity audit, the reachability audit and the walks find none, which means the problems you saw are of a kind I do not yet test for. One or two concrete examples from your playtest would let me turn them into checks.

## How it was checked

The combined pass ran 54 steps. Fifty two passed on the first run. The two failures were a Steiner block test that assumed a free cell beside the street mouth where a townhouse now stands, and the hermit repeat limit described above. The test now approaches from below the trigger row and passes with the same fight, payment and exit, and the hermit audit passes with the new lines. The real ROM builds and its opening test passes. The god mode walker passed Areas 1 to 5 with zero problems, after one planner fix (it visited a hut before the gate that stands at the street entrance). The reachability audit finds all 340 generated maps reachable and the continuity audit finds no problems. Areas 4 and 5 were walked before the last text and sprite commits, which changed no map geometry.

## Next

The remaining design work I would do next is more places and secrets to find, since you said the game has a lot to fight but nothing to explore, forks and loops in the road, and a gate hall for the Commune. The battle engine pass still waits for your word that testing of this build is done.
