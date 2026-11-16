# Hardcore Crystal, alpha 3 (test build, not a release)

ROM: `HardcoreCrystal_alpha3.gbc` (2 MB, Game Boy Color, MBC3 with battery, built from the `hardcore-crystal` branch on pret/pokecrystal).
Runs in any GBC emulator (mGBA, SameBoy, BGB) or on a flash cart. Adults only. This file has spoilers on purpose, it is for the author.

Two extra ROMs exist only to sample content without playing 500 fights first. Both are test builds (a level 100 CTHULUDON, the story flags the start
would have set, the key items, a Pokegear and the map card in the bag). Do not judge balance on them.
- `HardcoreCrystal_alpha3_sampler.gbc` starts on Tithe Plaza 1, kills already revealed, all the key items in the bag.
- `HardcoreCrystal_alpha3_ending.gbc` starts in Judecca with the story flags of the end. Walk to FINNEGAN, win, and the Hall of Fame and the credits follow.

## What alpha 3 adds to alpha 1 and 2
1. **Eight original songs** (`tools/hardcore/gen_music.py`, `docs/MUSIC.md`): The Road, The Tithe, The Grove, The Axiom, The Lotus, The City of Dis, The Terraces and The Abyss.
   Each loops between about 2:35 and 3:20 and is mostly silence with a drone and a few bells, written to be left on. New Bark Town and Cherrygrove keep Crystal's own sound.
2. **A real map of the world.** Mom no longer hands over the Pokegear. Bruno (Giordano Bruno, the last duel at Nick's Landing at the top of Purgatorio) gives you the
   Pokegear and the map card together once he is beaten, so in a normal run the map arrives late. The map shows the five areas, Purgatorio and Nick's Landing instead
   of Johto and Kanto. The sampler ROMs start with both, so look at it there.
3. **A shorter first-kill reveal.** Three short lines, a shake, the counter starts. The speech is gone.
4. **Credits.** After the staff of the original game: Hardcore Crystal, a total conversion; story and direction (placeholder: THE AUTHOR, change it in
   `data/credits_strings.asm`); co-creator CLAUDE (Anthropic); built on the pret pokecrystal disassembly; in loving memory of TIMMY and 499 others.
5. **Thirty hidden people.** Twelve hermits wait in the glades of the five areas and give a present for nothing: six **charms** (key items with a permanent effect: more
   experience, more money from bodies, a better catch rate, more drops, a trickle of healing while walking, fewer wild fights) and six stat items. Eighteen more hermits
   live in Purgatorio and give stat items after a fight. Full list in `docs/CHARMS.md`.
6. **Debates.** In every plaza two townsfolk stand facing each other and argue about philosophy, sex and money (35 pairs, one per plaza, nothing graphic).
7. **FINNEGAN's wake.** Some trainers in every area belong to a cult that believes dying by your hands is a glorious afterlife. They are eager for the fight and say so,
   before and after.

Everything from alpha 2 is still in: 500 mandatory trainers plus 15 bosses, 49 scripted duels (not kills) and 58 in Purgatorio; the tidal wave at kill 400, the rival's
fall and the crater, Purgatorio and the Abyss, the named characters and their key items, the corkboard, the normal ending. Battle budget 622 of 650.

## Things worth trying first
- Open the Pokegear map on the sampler ROM. Does the map read well, does the cursor land on the right places, is the area name right on every landmark?
- Stand in each area for a few minutes with the sound on. Does the music stay out of the way? Is any song irritating or too loud against the sound effects?
- Find a glade hermit and take a charm. Does the effect show without being told? Can you find all twelve by walking?
- Talk to the debaters and cultists in two areas. Is the humour landing, is there too much or too little of it?
- Run the credits (ending ROM) and read the new block.

## Known gaps (expected)
- Battle engine and AI work is the next version, nothing of it is in alpha 3.
- Art: about 81 of the 95 new species still use tinted vanilla sprites, trainer battle pictures for the named classes are recoloured vanilla ones, there is no run sprite art.
- The credits say THE AUTHOR where your name goes.
- Purgatorio has 58 trainers (60 planned), and 12 kills lie between the tidal wave (400) and the crater (412).
- Trainer teams are generated and still repeat across a lane. Hardcore balance (late-area one-shots, Destiny Bond lines) is untested.
- Parts of this build (reveal text, credits wording, charms, hermit lines, debates, cult lines, songs) were rewritten after a machine reset, so the wording differs
  from the draft the plan was made from. Everything else was replayed from the saved history.

## How it was checked
`tools/hardcore/verify_all.sh` builds the real ROM and every test ROM and runs all tests: text widths, names, wild tables, battle budget, roster, move categories, intro,
charms (64 checks), credits (screens read from the tilemap, order and width), the reveal, whiteout, the Pokegear map, wild fights, the story milestones, gates, named duels,
Purgatorio and the ending, plus `test_music.py` (eight songs recorded in the emulator and measured) and the five full area walks (`walk_all.sh`).
The test harness (PyBoy) gained two fixes: button presses are held for varying lengths so menus never phase-lock, and it recovers when the emulator locks after a hook.
