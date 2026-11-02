# Sprite status of the new species

97 new species: 2 imported from author sprites, 12 generated placeholders, 2 hand coded, 81 still reusing a vanilla sprite.

## How to hand over a sprite

Put the finished front sprite at `tools/hardcore/sprites/imports/<species>.png` (lower case name, for example `typhoneus.png`) and, if you have
it, the back sprite at `imports/<species>_back.png`.  Pixel art at any size is fine (an integer upscale such as 3x is undone), with a transparent
or empty background.  The importer picks two colours from the image, keeps white and black, and shrinks it to the 56x56 front (48x48 back) picture
of the Game Boy Color.  Without a back sprite the front is mirrored as a stand-in.  Palette colours can be overridden in `sprites/recipes.py`.

| # | species | stage | types | picture | base sprite |
|---|---|---|---|---|---|
| 27 | ELDERWOOD | 4 | GHOST/GRASS | reused sprite of MEGANIUM | MEGANIUM |
| 28 | CALDERA | 4 | DARK/FIRE | reused sprite of TYPHLOSION | TYPHLOSION |
| 45 | DEATHROLL | 4 | DARK/WATER | reused sprite of FERALIGATR | FERALIGATR |
| 50 | OVERGROWN | 4 | DARK/GRASS | reused sprite of VENUSAUR | VENUSAUR |
| 51 | EMBERWYRM | 4 | DRAGON/FIRE | generated placeholder | CHARIZARD |
| 83 | IRONCLAD | 4 | STEEL/WATER | reused sprite of BLASTOISE | BLASTOISE |
| 84 | SENTINEL | 3 | NORMAL | reused sprite of FURRET | FURRET |
| 85 | PANOPTICON | 4 | DARK/NORMAL | reused sprite of FURRET | FURRET |
| 100 | PROFESSOWL | 3 | FLYING/PSYCHIC_TYPE | reused sprite of NOCTOWL | NOCTOWL |
| 101 | EMERITUS | 4 | FLYING/PSYCHIC_TYPE | reused sprite of NOCTOWL | NOCTOWL |
| 102 | PLAGUERAT | 3 | DARK/NORMAL | reused sprite of RATICATE | RATICATE |
| 103 | RATKING | 4 | DARK | reused sprite of RATICATE | RATICATE |
| 106 | RAVENOUS | 4 | DARK/FLYING | generated placeholder | PIDGEOT |
| 107 | CINDERWING | 4 | BUG/FIRE | reused sprite of BUTTERFREE | BUTTERFREE |
| 108 | BEEHEMOTH | 4 | BUG/POISON | generated placeholder | BEEDRILL |
| 114 | DANDELION | 4 | FAIRY/GRASS | reused sprite of JUMPLUFF | JUMPLUFF |
| 115 | DREADBEAK | 3 | DARK/FLYING | reused sprite of FEAROW | FEAROW |
| 118 | DOOMTALON | 4 | DARK/FLYING | reused sprite of FEAROW | FEAROW |
| 119 | KINGCOBRA | 3 | DARK/POISON | generated placeholder | ARBOK |
| 122 | BASILISK | 4 | DRAGON/POISON | reused sprite of ARBOK | ARBOK |
| 125 | MEGAWATT | 4 | ELECTRIC | reused sprite of RAICHU | RAICHU |
| 126 | MOONQUEEN | 4 | FAIRY/PSYCHIC_TYPE | reused sprite of CLEFABLE | CLEFABLE |
| 127 | SOPORIFIC | 4 | FAIRY/NORMAL | reused sprite of WIGGLYTUFF | WIGGLYTUFF |
| 128 | MATRIARCH | 4 | FAIRY/GROUND | reused sprite of NIDOQUEEN | NIDOQUEEN |
| 131 | TYRANT | 4 | DARK/GROUND | reused sprite of NIDOKING | NIDOKING |
| 132 | NOSFERATU | 4 | DARK/FLYING | reused sprite of CROBAT | CROBAT |
| 133 | BELLADONNA | 4 | GRASS/POISON | reused sprite of BELLOSSOM | BELLOSSOM |
| 134 | MAWBLOOM | 4 | DARK/GRASS | reused sprite of VICTREEBEL | VICTREEBEL |
| 135 | CORDYCEPS | 3 | BUG/GHOST | reused sprite of PARASECT | PARASECT |
| 136 | SPOREKING | 4 | BUG/GHOST | reused sprite of PARASECT | PARASECT |
| 138 | CANDLEMOTH | 3 | BUG/FIRE | reused sprite of VENOMOTH | VENOMOTH |
| 139 | PYREMOTH | 4 | BUG/FIRE | reused sprite of VENOMOTH | VENOMOTH |
| 140 | SILKFANG | 3 | BUG/DARK | reused sprite of ARIADOS | ARIADOS |
| 141 | WEBWEAVER | 4 | BUG/DARK | reused sprite of ARIADOS | ARIADOS |
| 142 | ALLEYCAT | 3 | DARK | reused sprite of PERSIAN | PERSIAN |
| 143 | KINGPIN | 4 | DARK/NORMAL | reused sprite of PERSIAN | PERSIAN |
| 144 | MIGRAINE | 3 | PSYCHIC_TYPE/WATER | reused sprite of GOLDUCK | GOLDUCK |
| 145 | ANEURYSM | 4 | PSYCHIC_TYPE | reused sprite of GOLDUCK | GOLDUCK |
| 146 | BERSERKER | 3 | FIGHTING | reused sprite of PRIMEAPE | PRIMEAPE |
| 150 | ANGERILLA | 4 | DARK/FIGHTING | reused sprite of PRIMEAPE | PRIMEAPE |
| 151 | TITANFIST | 4 | FIGHTING/STEEL | generated placeholder | MACHAMP |
| 165 | OMNISCIENT | 4 | PSYCHIC_TYPE | reused sprite of ALAKAZAM | ALAKAZAM |
| 166 | MONOLITH | 4 | GROUND/ROCK | generated placeholder | GOLEM |
| 170 | ADAMANTIX | 3 | GROUND/STEEL | reused sprite of STEELIX | STEELIX |
| 171 | SKYSCRAPER | 4 | DRAGON/STEEL | generated placeholder | STEELIX |
| 175 | HELLHOUND | 3 | DARK/FIRE | IMPORTED front, mirrored back placeholder | ARCANINE |
| 176 | GATEHOUND | 4 | DARK/FIRE | generated placeholder | ARCANINE |
| 177 | KITSUNE | 3 | FAIRY/FIRE | reused sprite of NINETALES | NINETALES |
| 178 | FOXFIRE | 4 | FAIRY/FIRE | reused sprite of NINETALES | NINETALES |
| 185 | UNICORN | 3 | FAIRY/FIRE | reused sprite of RAPIDASH | RAPIDASH |
| 186 | DREADSTEED | 4 | FAIRY/FIRE | generated placeholder | RAPIDASH |
| 190 | HELLBOUND | 3 | DARK/FIRE | reused sprite of HOUNDOOM | HOUNDOOM |
| 191 | PERDITION | 4 | DARK/FIRE | reused sprite of HOUNDOOM | HOUNDOOM |
| 192 | BLACKSHEEP | 4 | DARK/ELECTRIC | reused sprite of AMPHAROS | AMPHAROS |
| 193 | MAGNETRON | 3 | ELECTRIC/STEEL | reused sprite of MAGNETON | MAGNETON |
| 194 | SOLENOID | 4 | ELECTRIC/STEEL | reused sprite of MAGNETON | MAGNETON |
| 195 | MAINFRAME | 3 | NORMAL/STEEL | reused sprite of PORYGON2 | PORYGON2 |
| 196 | ALGORITHM | 4 | PSYCHIC_TYPE/STEEL | reused sprite of PORYGON2 | PORYGON2 |
| 197 | APPARITION | 4 | DARK/GHOST | generated placeholder | GENGAR |
| 198 | BONEKEEPER | 3 | GHOST/GROUND | reused sprite of MAROWAK | MAROWAK |
| 199 | OSSUARY | 4 | GHOST/GROUND | reused sprite of MAROWAK | MAROWAK |
| 200 | SLUDGELORD | 3 | DARK/POISON | reused sprite of MUK | MUK |
| 201 | SUPERFUND | 4 | POISON | reused sprite of MUK | MUK |
| 202 | MIASMA | 3 | GHOST/POISON | reused sprite of WEEZING | WEEZING |
| 203 | PANDEMIC | 4 | DARK/POISON | reused sprite of WEEZING | WEEZING |
| 204 | WARHORN | 3 | GROUND/ROCK | reused sprite of RHYDON | RHYDON |
| 205 | BEHEMOTH | 4 | GROUND/STEEL | reused sprite of RHYDON | RHYDON |
| 206 | CLEAVER | 3 | BUG/STEEL | reused sprite of SCIZOR | SCIZOR |
| 207 | HEADSMAN | 4 | BUG/STEEL | reused sprite of SCIZOR | SCIZOR |
| 209 | CTHUSPAWN | 3 | DARK/POISON | own art (hand coded) | TENTACRUEL |
| 210 | CTHULUDON | 4 | DARK/POISON | own art (hand coded) | TENTACRUEL |
| 211 | POLIWRAITH | 4 | GHOST/WATER | reused sprite of POLIWRATH | POLIWRATH |
| 213 | AMNESIAC | 3 | PSYCHIC_TYPE/WATER | reused sprite of SLOWBRO | SLOWBRO |
| 214 | OBLIVION | 4 | DARK/PSYCHIC_TYPE | reused sprite of SLOWBRO | SLOWBRO |
| 215 | TUSKDRIFT | 3 | ICE/WATER | reused sprite of DEWGONG | DEWGONG |
| 216 | FROSTSIREN | 4 | FAIRY/ICE | reused sprite of DEWGONG | DEWGONG |
| 217 | CRYOCLAM | 3 | ICE/WATER | reused sprite of CLOYSTER | CLOYSTER |
| 218 | ABYSSHELL | 4 | DARK/ICE | reused sprite of CLOYSTER | CLOYSTER |
| 219 | CARAPACE | 3 | ROCK/WATER | reused sprite of KINGLER | KINGLER |
| 222 | CARCINIZE | 4 | STEEL/WATER | generated placeholder | KINGLER |
| 223 | NEBULON | 3 | PSYCHIC_TYPE/WATER | reused sprite of STARMIE | STARMIE |
| 224 | SUPERNOVA | 4 | FIRE/PSYCHIC_TYPE | reused sprite of STARMIE | STARMIE |
| 225 | MAELDRA | 4 | DRAGON/WATER | reused sprite of KINGDRA | KINGDRA |
| 226 | RAGECARP | 3 | DRAGON/WATER | reused sprite of GYARADOS | GYARADOS |
| 227 | WORLDEATER | 4 | DRAGON/WATER | reused sprite of GYARADOS | GYARADOS |
| 231 | TIDEBELLY | 3 | FAIRY/WATER | reused sprite of AZUMARILL | AZUMARILL |
| 232 | BEACHBALL | 4 | FAIRY/WATER | reused sprite of AZUMARILL | AZUMARILL |
| 234 | NARCOLEPT | 3 | PSYCHIC_TYPE | reused sprite of HYPNO | HYPNO |
| 235 | SANDMAN | 4 | DARK/PSYCHIC_TYPE | reused sprite of HYPNO | HYPNO |
| 236 | PLACEBO | 3 | FAIRY | reused sprite of BLISSEY | BLISSEY |
| 237 | HOSPICE | 4 | FAIRY/GHOST | reused sprite of BLISSEY | BLISSEY |
| 239 | MAMMOTH | 3 | GROUND/ICE | reused sprite of PILOSWINE | PILOSWINE |
| 240 | ICEAGE | 4 | GROUND/ICE | reused sprite of PILOSWINE | PILOSWINE |
| 241 | FROSTBITE | 3 | ICE/PSYCHIC_TYPE | reused sprite of JYNX | JYNX |
| 243 | RIMEQUEEN | 4 | FAIRY/ICE | reused sprite of JYNX | JYNX |
| 244 | WYRMKING | 4 | DRAGON/FLYING | generated placeholder | DRAGONITE |
| 245 | TYPHONEUS | 4 | DARK/ROCK | IMPORTED front, mirrored back placeholder | TYRANITAR |
