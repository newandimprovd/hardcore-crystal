# Special encounters

Budget (tools/hardcore/areas/counts.py, checked by battle_budget.py): 500 mandatory trainers, everything else is special and counted apart, all battles together at most 650.
Today: 500 mandatory + 15 bosses + 49 scripted duels (30 duelists, Bruno, 13 named duels, 5 rival fights) + 58 in Purgatorio = **622, 28 slots free**.

All special duels are **scripted** (`loadtrainer`, `startbattle`, `reloadmapafterbattle`), never trainer objects. The trainer-death engine only reacts to trainer objects, so
**nobody dies in these duels and none of them counts as a kill**: the 500 kills, the tidal wave at kill 400 and the crater at 412 are unchanged. Every one of them
asks first (yes or no), fights once with a team of its own, and pays on the first win. Levels follow the place in the game (the area's range at the plaza's position).

## The named characters (areas/named.py, texts in areas/named_text.py)
The characters keep their names and each speaks his own historical doctrine of the end of the world and of the ghosts (eschatology, hauntology, theodicy). The main story
all of them circle: the merging of the digital and the physical as an eschatological principle, seen as the Teleoplexic Entity, Finnegan, the Dajjal, Mr. POKeMON and Ahriman.
The real world began melding with fantasy when Satoshi Tajiri saw a Japanese jewel beetle, a manifestation of Ahriman (the Kabbalist mafia and the Yakuza smuggled the crate).

### Key bearers (mandatory): they hand over the key items that replace the HMs, the way Steven and Cynthia do
The road does not go on until the prize is in the bag: a coordinate trigger across the exit of the plaza sends the player one step back with a hint.

| Where | Who | Prize | Doctrine |
| --- | --- | --- | --- |
| Tithe plaza 1 | Steiner | CHAINSAW | Lucifer and Ahriman, the incarnation of Ahriman in the West, the Balance |
| Tithe plaza 4 | Crowley (chased by the crowd) | CROWBAR | Thelema, the Aeon of the Child, Choronzon sends him smuggling |
| Grove, Amphitheater | Crowley | JET SKI | the Abyss, the Algerian desert, Finnegan in millions of soft heads |
| Grove plaza 4 | Steiner | BASEBALL BAT | the mirror jail of belief, Finnegan dreamed the key, the dead are unfinished |
| Axiom plaza 1 | Hasan-i Sabbah | FLASHLIGHT | zahir and batin, ta'wil, ta'lim, the robots as pure zahir |
| Axiom plaza 4 | Hasan-i Sabbah | SLEDGEHAMMER | the Qiyama (resurrection as the lifting of the veil, paradise as knowledge, hell as ignorance), the one-eyed Dajjal who sees only the zahir |
| Lotus plaza 1 | Cioran | GRAPPLE HOOK | the voice at three in the morning, the bungling demiurge, theodicy as the defence of the accused |
| Lotus plaza 4 | Cioran | SHOVEL | history as decay, the dead are what the present is made of |

The bosses no longer carry the key items (area 5's boss still drops the GETAWAY CAR). Each gate says what it needs, nothing says where to find it: the game guides, it does not handhold.

### Optional later encounters: they complete the CORKBOARD
Each pays RARE CANDY or PP UP once and pins one page. With every page pinned (the whole board, including Joyce, Bruno, the grave and the post) the board shows a last page: **THE BOARD IS FULL**.

| Where | Who | Level | Doctrine |
| --- | --- | --- | --- |
| Axiom plaza 6 | Suhrawardi | plaza 6 | the Philosophy of Illumination, the world of images, the Occidental exile |
| Lotus plaza 6 | Steiner | plaza 6 | the tightrope of the Balance, leave the era with plumbing |
| Dis plaza 6 | Mulla Sadra | plaza 6 | substantial motion, the soul rises in the body it earned, the Fire may cool |
| Purgatorio hub | Steiner | 40 | karma as a ledger of the dead, give the thing a face and a name |
| Purgatorio hub | Abd al-Jabbar | 46 | the five Mu'tazili principles, the position between two positions, God owes His creatures the best |

Joyce (the junction, he hands over the CORKBOARD, Vico's cycles and the Wake as resurrection), Bruno (Purgatorio Landing, infinite worlds, teleoplexy), Satoshi (Grove) and Mr. POKeMON keep their talks.

### The rival: about six fights
One initial (the Tithe junction, level 5, two creatures, in the stem of the road: nobody reaches Joyce, the house or the cave without it), one in the stem of plaza 2 in each of Areas 1 to 3,
one in the Purgatorio hub once the Axiom mouth is open (RIVAL2, level 56), and the last one in the mansion: **the boss fight that kills him**. He stands in the street, the whole width
of it is a trigger, and he walks off the map after the fight. Teams follow a theme of their own (dark, normal, fighting, fire, ghost, steel).

## The 30 generic duelists (areas/specials.py)
Six per area, one in each of the plazas 1 to 6 (optional, a vitamin or a PP Up on the first win). Names follow the Pokemon way (two words run together, a pun that tells you what the thing is).

| Area | Duelists (class) |
| --- | --- |
| Tithe | FR GRIFT (priest), SGT SLOW (cop), BIG SAL (thug, "Kabbalah, totally different bees"), MS LEDGER (accountant), DEAN DRIP (banker), BRO HUSH (deacon) |
| Grove | AUNT KALE (granny), DRUM DAN (drummer), SEER MOSS (shaman), NANA BIRD (birder), FERN FRY (forager), GRAN OAK (elder) |
| Axiom | UNIT 7 (bot cop), DR MADD (mad doctor), MATCH-9 (matchmaker), AGENT ZED (executive), CASE 44 (caseworker), WARDEN-3 (warden bot) |
| Lotus | MR SUNNY (resort manager), DIVE DAVE (lifeguard), NURSE NIL (clinician), LAZY LEO (beach bum), MS MOJITO (waiter), AMNESIA (forgotten one) |
| Dis | JUDGE HOLE (judge), MAG PYRE (magistrate), HAG HEX (hag), JEST ERR (jester), WARDEN KIM (warden), SPEC TER (spectre) |

## Tests
`test_named.py ROM block` (the guarded exit, the duel, the prize), `test_named.py ROM rival` (the first rival fight), the area walks (`walk_all.sh`, they win every key duel with a `give:` goal),
`test_purg.py` (the hub duels).
