# Special encounters

Budget (tools/hardcore/areas/counts.py, checked by battle_budget.py): 500 mandatory trainers, everything else is special and counted apart, all battles together at most 650.
Today: 500 mandatory + 15 bosses + 31 scripted duels (30 duelists, Bruno) + 58 in Purgatorio = 604, **46 slots free**.

## Built (first batch, 30 duelists)
Six named duelists per area, one in each of the plazas 1 to 6 (areas/specials.py). They are scripted duels, so they are not part of the 500: you talk to them, answer yes or no,
fight once with a team of their own (the area's theme, level following the plaza's place in the area), and the first win pays a vitamin or PP Up.
They count as kills like bosses do (the counter and the tidal wave at kill 400 do not care who died). They are optional, so the shortest path (rival's fall at kill 412) is unchanged.

| Area | Duelists (class) |
| --- | --- |
| Tithe | FR GRIFT (priest), SGT SLOW (cop), BIG SAL (thug, "Kabbalah, totally different bees"), MS LEDGER (accountant), DEAN DRIP (banker), BRO HUSH (deacon) |
| Grove | AUNT KALE (granny), DRUM DAN (drummer), SEER MOSS (shaman), NANA BIRD (birder), FERN FRY (forager), GRAN OAK (elder) |
| Axiom | UNIT 7 (bot cop), DR MADD (mad doctor), MATCH-9 (matchmaker), AGENT ZED (executive), CASE 44 (caseworker), WARDEN-3 (warden bot) |
| Lotus | MR SUNNY (resort manager), DIVE DAVE (lifeguard), NURSE NIL (clinician), LAZY LEO (beach bum), MS MOJITO (waiter), AMNESIA (forgotten one) |
| Dis | JUDGE HOLE (judge), MAG PYRE (magistrate), HAG HEX (hag), JEST ERR (jester), WARDEN KIM (warden), SPEC TER (spectre) |

Names follow the Pokemon way (two words run together, a pun that tells you what the thing is). The same rule names the fountains, the shops and the gift-givers.

## Proposed for the 46 free slots (not built, waiting for approval)
| # | Encounter | Where | Why |
| --- | --- | --- | --- |
| 8 | **Rival duels**: one in front of every area's second plaza except Area 4 (that is the crater fight) and one more in Cherrygrove after Timmy | Areas 1 to 3, Cherrygrove | the rival has no presence between the start and the crater |
| 5 | **Kabbalist Mafia** (capo and four enforcers, cartoonish and incompetent) | Tithe, around TithePlaza2 | the Crowley chain (his chasers, then the bees) |
| 3 | **Yakuza boss and two lieutenants** | Tithe, mid-city | the shaggy-dog chain, the bees |
| 1 | **Crowley** as the Shaman, a duel after the confession, reward BUFFTAIL | Grove, the Amphitheater | the only fight of the Crowley quest |
| 4 | **Amphitheater elders** (the women who watch from the side lines, the joke is theirs) | Grove | keeps the quest's tone, no fight shown in the ritual |
| 2 | **Hassan-i Sabbah** and his Assassin | Axiom, behind the gene farm | warns about Dajjal, fights if asked |
| 4 | **Gene farm wardens** | Axiom, the farm | the colour of the area's horror |
| 3 | **Robot Mayor's bodyguards** | Axiom, the mayor's hall | before the mayor's boss room |
| 1 | **Cioran**, the sleepless man, a duel he does not want | Lotus | sleepless, bitter, funny |
| 4 | **Grief clinic doctors** | Lotus, the basement city | the subscription to forgetting |
| 3 | **Basement city staff** | Lotus | the people who live under the beaches |
| 4 | **Dis gatekeepers** (the four who do not let you in) | Dis, outside the walls | the entrance |
| 3 | **Cocytus ice wardens** | Dis, Lake Cocytus | between the walls and Judecca |
| 1 | **Steiner**, once, if asked: he answers with a team of the area's strongest | Purgatorio, near the Abyss | the lore's clinician |

That is 46. Any of them can be dropped or traded; each is one entry in areas/specials.py (name, class, sprite, three lines of text) plus a place.

## What the author needs to decide
1. Are the named duelists optional (as built) or should some of them block a door? Optional means nobody has to fight them, mandatory means the kill order changes.
2. Do the real-name characters (Crowley, Sabbah, Cioran, Steiner) fight at all, or only talk? Built so far: they only talk, except Bruno.
3. Keep the rival fights to four or add one per area?
