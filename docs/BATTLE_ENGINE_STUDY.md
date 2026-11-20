# Battle engine study

Done after alpha 3.1 as preparation for the battle engine version. Nothing in the game changed. Measurements come from our own ROM in the emulator
(`tools/hardcore/refstudy/aimeasure.py`). Statements about Showdown, Foul Play, Technical Machine, pokeemerald-expansion and Polished Crystal come from the pages listed under Sources,
read through a page summarizer, not from the full source code. Inferences are marked as inferences.

## 1. What our engine is today

- The battle code is vanilla Crystal with our changes on top. The damage path is the cartridge's. I compared it with the Gen 2 rules of Showdown's `data/mods/gen2/scripts.ts`
  and the parts I compared agree. These are the 997 cap plus 2 (our `MAX_DAMAGE 999`, `MIN_DAMAGE 2`) and the 85 to 100 percent variance (Showdown multiplies by 217 to 255 over 255,
  ours redraws until a byte is at least 85 percent+1, which is 217 too). STAB handling and the burn and paralysis stat effects exist in our source too, but I did not compare their exact values
  or the stat rollover line by line.
  Our changes are the per-move physical or special lookup (`GetMoveCategory`), the type chart with Fairy, the 39 Showdown move replacements, the 70/30 experience share and the paid healing.
- There is no ability system, no natures, no Tera, no EV rework. Gen 2 has held items, weather, Spikes and DVs, which we keep.
- The trainer AI is the vanilla layered scorer. Ten layers (Basic, Setup, Types, Offensive, Smart, Opportunist, Aggressive, Cautious, Status, Risky) add to or subtract from a score per move,
  and the lowest score wins with ties broken at random. Which layers run is a 16 bit flag word per trainer class (158 rows in `data/trainers/attributes.asm`, 39 of them use Basic, Setup, Smart, Aggressive, Cautious, Status and Risky).
  `AI_Smart` has 82 per-effect labels (some share code) for Toxic, Reflect, Encore, Perish Song and so on.
  `AI_Aggressive` calls the real battle damage commands (`AIDamageCalc` runs `EnemyAttackDamage`, `BattleCommand_DamageCalc` and `BattleCommand_Stab`), so the AI sees exact damage with the player's real stats.
- Switching is a separate rule set (`switch.asm`). It scores a switch from the moves the player has already used (`wPlayerUsedMoves`) against the enemy's types,
  looks for a mon with a super effective move or a resist, and rolls a chance. There is no lookahead, no idea of who outspeeds whom beyond the damage layer, no plan across turns.
- 27 `BUG:` markers remain in the battle code (core 9, effect commands 9, AI items 4, AI redundant 2, AI scoring 3). pret documents the bugs in `docs/bugs_and_glitches.md`.
  The AI ones include Mean Look encouraged while its own mon is badly poisoned, Full Heal not curing confusion, Nightmare, Future Sight and a false assumption about `CheckTypeMatchup`.
  Showdown's Gen 2 mod models several cartridge quirks on purpose (the 1 in 256 failure of 100 percent secondaries, the Present glitch), so "fix every bug" and "match Showdown" are two different goals.

## 2. Measured on our ROM

Setup. A test ROM with the player at level 14, the rival fight on the Tithe junction stem, hooks on `AIChooseMove`, `AIDamageCalc` and its two call sites.
Clock is completed frames times 70224 plus the scanline counter times 456. The game's own VBlank counter was read at the same hooks as a second opinion.

| quantity | samples | result |
|---|---|---|
| one `AIDamageCalc` (the real damage routine for one move) | 4 | 93,024 to 103,512 cycles, median 98,724 (about 1.4 frames). VBlank counter agrees with 1 to 2 frames |
| `AIChooseMove` for a mon with two damaging moves, all layers | 2 | 338,352 and 346,104 cycles (about 4.9 frames). VBlank counter says 5 |
| `AIDamageCalc` calls inside one `AIChooseMove` | 2 | 2 and 2 |

Caveats. Few samples, one fight, one ROM. The numbers include the VBlank interrupt handler time that runs during those frames. I had expected the damage routine to cost a few thousand cycles
and it costs roughly twenty times that, so I trust the number only because two independent clocks agree. I did not find out why it is so slow, the likely suspects are the chain of
`callfar` hops, the stat fetch and the multiply and divide helpers.

Space. The real ROM has 531,014 bytes unallocated, 2,426 in bank 0 and 528,588 spread over 92 banks, which is 25 percent of 2 MB. Unallocated work RAM is about 8 KB in total but split over banks (WRAM0 96, WRAMX1 156, WRAMX2 3696, WRAMX3 997, WRAMX5 3073 bytes),
which matters more than the ROM figure for any search that needs scratch space.

## 3. What the references do

**Pokemon Showdown simulator (Gen 2 mod).** Actions go into a queue sorted by an `order` number (switches 103 before moves 200, residuals 300), then `priority` lowest first, then speed highest first.
Speed ties are shuffled with the battle's PRNG. Effects hook into events (the pkmn engine write-up calls the generic handler search "the slowest part" of Showdown).
The Gen 2 mod models: stat stages with floors, 999 cap, accuracy out of 255, crit chances out of 256 by stage, crits ignoring unfavourable stages and screens, multi-hit weights (2, 2, 2, 3, 3, 3, 4, 5),
a single status roll on the last hit, flinch immunity for sleeping and frozen targets.

**pkmn engine (the fast reimplementation).** Written for speed, no strings, no allocation, every generation separate, cartridge behaviour by default and Showdown behaviour behind a switch.
For us the transferable lessons are the data-oriented layout and keeping each rule set separate.

**Foul Play (Showdown bot).** Monte Carlo tree search with decoupled UCT for simultaneous moves, a hand-written evaluation function at the leaves instead of rollouts, root parallelism, lines searched to depth 10 and more.
Damage rolls are grouped, rolls that cause a faint stay separate and non-fainting rolls are averaged into one branch. Hidden information is handled by set prediction from usage statistics, scraped teams and replays,
sampled per decision, and by inference from what is observed (damage taken, move order, weather duration, item reveals). Its author calls set prediction as important as the search.
Earlier versions used expectiminimax, exhaustive search stopped at about 5 turns, and the author found it impractical.

**Technical Machine (older bot, 2010 thread).** Expectiminimax with alpha-beta pruning, three players (the AI, the foe and a chance player), team and set prediction from usage statistics, evaluation as team score minus foe score,
mixed Nash equilibrium play planned but not built. The author said his early evaluation numbers were "probably within an order of magnitude of being correct".

**pokeemerald-expansion AI flags (a modern ROM hack engine).** It splits the AI into flags a trainer can combine. Move scoring: check bad move, check viability, try to faint (OHKO first, priority moves when slower), try to 2HKO,
prefer highest damage, setup first turn, stall, risky, conservative, HP aware, PP stall prevention. Switching: smart switching with listed triggers (cannot hit a Wonder Guard target, Perish Song, Yawn, bad matchup at half HP or more,
a teammate that absorbs the expected attack, no useful move) and deliberate failure rates, plus smart mon choices after a faint (trapper, then revenge killer by speed and KO math, then good matchup with a super effective move, then good matchup).
Prediction flags (predict switch with a 50 percent failure rate, predict incoming mon, predict move by assuming the player picks what the AI would). Knowledge flags from omniscient to ASSUME_STAB and guessed status moves.
Party strategy flags (sequence switching, ace pokemon, randomised switch-in, shuffled party order). This is the closest published design to what "trainers with strategies" means in a hack.

**Showdown random battle sets and roles (team design).** A mon is built in a fixed order, species, role, moves, ability, item. Roles such as Fast Attacker, Setup Sweeper, Wallbreaker, Bulky Attacker, Bulky Support and Fast Support force moves
(setup for setup roles, recovery for bulky roles, a STAB attack for every attacker). Team level rules reject too many shared weaknesses or types and limit hazard setters and removers to one each. Gen 2 has an extra Thief User role.
This is a ready made vocabulary for authoring trainer parties and for checking them.

**Polished Crystal (a GBC hack that rebuilt the mechanics).** Its changelog shows what the hardware and a 2 MB class ROM can carry. Abilities and natures, the physical and special split, modern EV rules, held item effects, Gen VII style
move and status changes, battle styles set, switch and predict for the player, and a long tail of fixes. On the AI side its changelog lists only damage calculation improvements, teleport use,
trainers getting random abilities and Battle Tower sets, so the trainer AI itself stayed a scoring system. A Showdown-grade trainer AI on this hardware has no finished example I could find.

## 4. What fits on a Game Boy Color (reasoning, with the measured numbers)

A frame is 70,224 cycles. One second is 60 frames, about 4.2 million cycles. A thinking pause of up to about ten frames is invisible because the text and animations already take longer. Half a second is tolerable if it hides behind a text box.

- Using the engine's own damage commands inside a search is too slow. At about 99,000 cycles each, 40 or so evaluations fit in a second. A search over four moves each for both sides is already 16 pairs, two evaluations per pair.
- A dedicated damage estimator is the key piece. It would read cached stats and a precomputed matchup row, skip variance and crits, and return an expected and a maximum damage.
  My target of 5,000 cycles is an assumption, not a measurement. At that cost several hundred estimates fit in a second, which supports a 1 ply or 2 ply search on one versus one positions, not a Foul Play style tree.
  It must be tested against the real damage routine on thousands of random cases, and against Showdown's Gen 2 damage on the same cases.
- Foul Play's approach (thousands of simulations, depth 10 and more, parallel threads, set sampling) is out of reach on this CPU. This is an inference from its published design and the budget above, the article gives no iteration counts.
- The practical route to "Showdown level" play is the pokeemerald-expansion route. Authored sets and roles carry the strategy, a flag based scorer plays it (KO aware move choice, revenge killer choice after a faint,
  trapper and setup logic, HP awareness), and a small lookahead settles close calls. Foul Play's hidden information machinery is not needed when the trainer's own party is fixed and known to the author.
- ROM space is not the constraint, 518 KB are free. Scratch work RAM is.

## 5. Options, cheapest first

1. **Decide the ruleset and build a conformance suite.** (Decided on 20 November 2026, see section 6. The author chose modern rules, so the text below describes the option that was not taken.) Recommended target was Gen 2 rules plus our changes, because Showdown's `gen2` mod is a complete executable specification of the engine we already have.
   Differential test our damage and turn order against it. Decide per quirk whether to match the cartridge or fix it. Cost, test tooling and a bug triage of the 27 markers.
2. **Scorer upgrade.** Fix the documented AI bugs, add KO awareness with speed (try to faint), HP awareness, setup first turn logic with a sanity check, a revenge killer and trapper aware replacement choice, ace and sequence flags per trainer,
   and a rule that the AI uses only what a player could know (used moves, visible types) with no omniscient exception (decided, see section 6). Estimated a few KB of code and cycles within the current 5 frame range.
3. **Estimator based lookahead.** Add the compact damage estimator and a 1 ply expectimax over my moves and switches against the player's best known reply, with fixed sets as the strategy layer. Cycle budget about 10 frames, tested by tournament.
4. **Authored strategies.** Each trainer party gets roles per mon (Showdown role names), a flag word, and checks from the random battle team rules (shared weaknesses, one hazard setter, a revenge killer in the back).
   This is a data and tooling job and it is where "every checkpoint special" actually comes from.
5. **Tournament harness.** The headless emulator can run AI against AI at unlimited speed. Measure win rate of each tier against the baseline on fixed teams, and keep it in `verify_all.sh`.
   Not tried yet, so I do not know the throughput.

## 6. Decisions

Decided by the author on 20 November 2026.
- Rules. Battles should feel like a Gen 8 game. Rules, move effects and Showdown effects match the modern games, and animations may stay simplified. This replaces the Gen 2 plus our changes option of section 5.
- Scope limit. No new mechanics. The work is to modify the current moveset and the existing rules to modern behaviour, not to add systems such as Dynamax. My reading, not yet confirmed by the author, is that abilities, natures and an IV and EV rework are also out, because they would be new systems.
  That keeps the party structure and saves compatible. If the author wants any of them, the plan below has to be redone.
- Cartridge quirks. Fixed. Modern games have neither the 1 in 256 failure of 100 percent secondaries nor the Present glitch.
- Trainer AI plays fair. It uses only what a player could know, such as moves already used, visible types and revealed items. Nobody is omniscient, so the omniscient flag of option 2 is not built.
- Thinking pause. At most 12 frames, for every trainer. Measured today, `AIChooseMove` takes about 5 frames and one `AIDamageCalc` about 1.4 frames.
- Assumed, not asked. Our own type chart, the Fairy type, four stage evolution lines and the 39 Showdown move replacements stay.
- Timing. Nothing is rebuilt and no engine work starts until the author has finished testing the 3.1 ROM and says so.

What this means for the plan. This is inference from section 1 and has not been measured on our code.
- The test oracle is Showdown's current generation damage rules and move data, used for differential tests of the rules and of every modified move.
- Rules to modernise are critical hits, burn, paralysis, confusion, sleep length, weather duration, Protect decay, the order of damage modifiers, the 999 damage cap, and any entry hazard that the moveset contains.
- Moves are the bulk of the work. Each current move gets its modern damage, accuracy, PP, priority, secondary effect chance and category, in the same way as the 39 replacements already done.
- The AI follows options 2 to 4 of section 5 with the fair play rule and a 12 frame budget. A one ply lookahead is only affordable inside 12 frames if the damage estimator reaches its target cost, which is still an assumption.
- Space is less of a worry than I wrote earlier, because nothing new has to be stored per Pokemon.

## 7. What this study did not cover

- Grandia's battle system. I never reached a fight in Grandia (see `docs/REFERENCE_STUDY.md`).
- crystal16-bit's battle code. It plays like vanilla in the places I saw and I did not read its source.
- Showdown's event system and Foul Play's evaluation function from the code. I read descriptions and one mirrored script, not the repositories.
- Cycle exact timing. The clock resolves about 456 cycles and I have two or four samples.
- Throughput of AI against AI in the emulator, and the real speed of any estimator, both unbuilt.

## Sources
- Foul Play: https://pmariglia.github.io/posts/foul-play
- pokeemerald-expansion AI flags: https://rh-hideout.github.io/pokeemerald-expansion/tutorials/ai_flags.html
- pkmn engine design: https://github.com/pkmn/engine/blob/main/docs/DESIGN.md
- Showdown battle queue (mirror): https://huggingface.co/spaces/PShowdown/Pokemon_server/blob/b7d0d2801893debbf9eea9e414e90a3f974f10c4/sim/battle-queue.ts
- Showdown Gen 2 mod scripts (mirror): https://huggingface.co/spaces/PShowdown/Pokemon_server/blob/main/data/mods/gen2/scripts.ts
- Showdown random battle roles: https://www.smogon.com/forums/threads/gen-9-random-battle-roles-information-and-code-explanation.3712694/
- Technical Machine thread: https://www.smogon.com/forums/threads/technical-machine-a-pokemon-ai.69021/post-2556758
- Polished Crystal changelog: https://github.com/Rangi42/polishedcrystal/blob/master/CHANGELOG.md
- pret bugs and glitches list: `docs/bugs_and_glitches.md` in this repo
