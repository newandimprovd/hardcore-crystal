# Hardcore Crystal, alpha 3.1 (the fix pass on your alpha 3 playtest list)

ROMs: `HardcoreCrystal_alpha3_1.gbc` (the game), `HardcoreCrystal_alpha3_1_sampler.gbc` (starts on Tithe Plaza 1, level 100 CTHULUDON, kills revealed, key items in the
bag) and `HardcoreCrystal_alpha3_1_ending.gbc` (starts in Judecca with the story flags of the end). The two test ROMs are for looking, not for judging balance.
This file has spoilers on purpose, it is for the author.

## Your 15 points, one by one

1. **Move names missing and B not going back.** The move box crashed back to the title screen. Cause: a pruned stub (`MobileTextBorder`) sat in a ROMX bank and a plain `call` from
   bank 0 landed in the wrong bank. The routine is back in `home/battle.asm`. The battle screens test (`test_battle_ui.py`) now opens the box, reads the move names and the
   category line, presses B and checks that the menu is back, then uses a move.
2. **Cherrygrove nurse.** She says exactly what the base game nurse says. A hole in the script made the "cash up front" line follow every heal. Cherrygrove is the only free
   POKeCENTER, Tithe Lowtown and everything else charge 4 per level of your best POKeMON plus 20 (test: 68 for a level 12). `test_nurse.py` plays both centers by key presses.
   (I first read your point 13 the wrong way round and made Lowtown free. That is reverted.)
3. **Running.** Hold B and the player now leans into the stride: head pushed forward and legs trailing in the side views, head tucked down a pixel in the front and back views.
   The side views alternate the walking legs with the standing legs twice per tile. There is no new sprite art, the poses shear the existing tiles
   (`data/sprites/facings.asm`, `FacingRun*`), so no tile space is spent. Any walking sprite that takes fast steps in a cutscene uses the same poses.
4. **Frame rate.** I found no lag. Walking takes exactly 16 frames per tile and running 8, on every map I measured. What I did find is a flicker: the old run animation fell
   back to the walking pose for two frames at every tile boundary, which at a tile every 8 frames is a visible stutter. That is fixed and the strides now alternate evenly
   every four frames (`test_run.py` checks both). If the speed itself still feels wrong, tell me whether it is walking or running, I left both at the original rates.
5. **Opening text of a battle.** It was showing the switch-out text. Fixed, and the battle screens test reads the opening line of a wild fight and checks it.
6. **The rival's team.** Every rival team now ends with the starter that opposes yours (Chikorita line, Cyndaquil line or Totodile line, in the right stage for his level).
   Checked in the emulator on the first duel.
7. **Purgatorio entrance.** The mountain is a full plateau that fills the top of the screen with a rim, and the cave mouth is cut into the rim, like the entrance of Dark Cave.
8. **Joyce.** He walks up to you after Mr. POKeMON's house, nobody has to find him. He has his own sprite now, top hat and spectacles.
9. **What James says.** The first meeting is short and confused: where is he, who is Mr. POKeMON, how did he get here. The rest of what he knows is kept for the later talk
   (the later talk is what sets his Corkboard lore, the opening test checks it).
10. **Lull charm.** Using it from the bag switches it off and on, with a line saying which way it went. It starts on. Tested on the engine routine and on the item script.
11. **Mr. POKeMON.** Vanilla gentleman sprite, a few lines about himself only (he thinks his manifestation is a good thing and says nothing against the children who love him),
    the CORKBOARD and the POKeDEX, then he leaves.
12. **Cutscenes you cannot skip.** The road pulls you into the house (the first step onto the road, nobody asked), Mr. POKeMON's scene runs on arrival, you are walked out and
    Joyce's scene runs on the road. Both run by themselves. Technical note: the engine ignores trigger tiles on the tile a warp lands on, so both scenes are re-entry scripts that
    the previous map queues right before the warp.
13. **Pokecenter costs.** See point 2.
14. **Steiner.** He stands in the street at the top of Tithe Plaza 1 and the first step toward it starts the fight, nobody asks. The plaza has a side corridor that
    could have walked around a trigger row, so the trigger row is the corridor cell right under the street mouth and a model test (`test_forced.py`) proves that the street is
    unreachable without crossing it. After the fight he steps aside and the exit opens.
15. **Steiner's battle picture.** It was borrowed from Professor Oak. It is a suited executive now (`PIC_FROM["steiner"] = "executive_m"`).

## What is tested, and how
`tools/hardcore/verify_all.sh` builds the real ROM and every test ROM and runs everything, one line each, in `/home/claude/scratch/verify/summary.txt`. New in 3.1:
`test_opening.py` (rival, forced house, both cutscenes, Joyce talk), `test_forced.py`, `test_nurse.py`, `test_battle_ui.py`, `test_run.py`; `test_purg.py`, `test_named.py` and
`test_charms.py` follow the new flows and the Lull switch.

## Known gaps (honest list)
- Only Steiner at Tithe Plaza 1 is a forced fight. The other key bearers (Crowley in Tithe 4, Steiner's second meeting in the Grove, Sabbah twice in Axiom, Cioran twice in
  Lotus, Crowley at the Grove amphitheater) still wait to be talked to, but each one blocks the exit of his plaza until you hold his key item, so none of them can be skipped.
  Say if you want all of them to stop you the way Steiner does.
- The run is a shear of the walking sprites, not new art. Drawn run frames (arms pumping, a real lean) would need extra sprite tiles for every character, so I did not spend
  them without asking.
- Mr. POKeMON's house and Joyce's walk were played through by the test, but I have not judged the timing by eye on a real device, only on screenshots.
- `crystal16-bit.gbc` (your reference for the next version) has not been mined yet. Battle engine and AI work is not in this version.
