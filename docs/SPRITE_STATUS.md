# Sprite status of the new species

97 new species: 2 imported from author sprites, 93 generated placeholders, 2 hand coded, 0 still reusing a vanilla sprite.

## How to hand over a sprite

Put the finished front sprite at `tools/hardcore/sprites/imports/<species>.png` (lower case name, for example `typhoneus.png`) and, if you have
it, the back sprite at `imports/<species>_back.png`.  Pixel art at any size is fine (an integer upscale such as 3x is undone), with a transparent
or empty background.  The importer picks two colours from the image, keeps white and black, and shrinks it to the 56x56 front (48x48 back) picture
of the Game Boy Color.  Without a back sprite the front is mirrored as a stand-in.  Palette colours can be overridden in `sprites/recipes.py`.

| # | species | stage | types | picture | base sprite |
|---|---|---|---|---|---|
| 27 | ELDERWOOD | 4 | GHOST/GRASS | generated placeholder | MEGANIUM |
| 28 | CALDERA | 4 | DARK/FIRE | generated placeholder | TYPHLOSION |
| 45 | DEATHROLL | 4 | DARK/WATER | generated placeholder | FERALIGATR |
| 50 | OVERGROWN | 4 | DARK/GRASS | generated placeholder | VENUSAUR |
| 51 | EMBERWYRM | 4 | DRAGON/FIRE | generated placeholder | CHARIZARD |
| 83 | IRONCLAD | 4 | STEEL/WATER | generated placeholder | BLASTOISE |
| 84 | SENTINEL | 3 | NORMAL | generated placeholder | FURRET |
| 85 | PANOPTICON | 4 | DARK/NORMAL | generated placeholder | FURRET |
| 100 | PROFESSOWL | 3 | FLYING/PSYCHIC_TYPE | generated placeholder | NOCTOWL |
| 101 | EMERITUS | 4 | FLYING/PSYCHIC_TYPE | generated placeholder | NOCTOWL |
| 102 | PLAGUERAT | 3 | DARK/NORMAL | generated placeholder | RATICATE |
| 103 | RATKING | 4 | DARK | generated placeholder | RATICATE |
| 106 | RAVENOUS | 4 | DARK/FLYING | generated placeholder | PIDGEOT |
| 107 | CINDERWING | 4 | BUG/FIRE | generated placeholder | BUTTERFREE |
| 108 | BEEHEMOTH | 4 | BUG/POISON | generated placeholder | BEEDRILL |
| 114 | DANDELION | 4 | FAIRY/GRASS | generated placeholder | JUMPLUFF |
| 115 | DREADBEAK | 3 | DARK/FLYING | generated placeholder | FEAROW |
| 118 | DOOMTALON | 4 | DARK/FLYING | generated placeholder | FEAROW |
| 119 | KINGCOBRA | 3 | DARK/POISON | generated placeholder | ARBOK |
| 122 | BASILISK | 4 | DRAGON/POISON | generated placeholder | ARBOK |
| 125 | MEGAWATT | 4 | ELECTRIC | generated placeholder | RAICHU |
| 126 | MOONQUEEN | 4 | FAIRY/PSYCHIC_TYPE | generated placeholder | CLEFABLE |
| 127 | SOPORIFIC | 4 | FAIRY/NORMAL | generated placeholder | WIGGLYTUFF |
| 128 | MATRIARCH | 4 | FAIRY/GROUND | generated placeholder | NIDOQUEEN |
| 131 | TYRANT | 4 | DARK/GROUND | generated placeholder | NIDOKING |
| 132 | NOSFERATU | 4 | DARK/FLYING | generated placeholder | CROBAT |
| 133 | BELLADONNA | 4 | GRASS/POISON | generated placeholder | BELLOSSOM |
| 134 | MAWBLOOM | 4 | DARK/GRASS | generated placeholder | VICTREEBEL |
| 135 | CORDYCEPS | 3 | BUG/GHOST | generated placeholder | PARASECT |
| 136 | SPOREKING | 4 | BUG/GHOST | generated placeholder | PARASECT |
| 138 | CANDLEMOTH | 3 | BUG/FIRE | generated placeholder | VENOMOTH |
| 139 | PYREMOTH | 4 | BUG/FIRE | generated placeholder | VENOMOTH |
| 140 | SILKFANG | 3 | BUG/DARK | generated placeholder | ARIADOS |
| 141 | WEBWEAVER | 4 | BUG/DARK | generated placeholder | ARIADOS |
| 142 | ALLEYCAT | 3 | DARK | generated placeholder | PERSIAN |
| 143 | KINGPIN | 4 | DARK/NORMAL | generated placeholder | PERSIAN |
| 144 | MIGRAINE | 3 | PSYCHIC_TYPE/WATER | generated placeholder | GOLDUCK |
| 145 | ANEURYSM | 4 | PSYCHIC_TYPE | generated placeholder | GOLDUCK |
| 146 | BERSERKER | 3 | FIGHTING | generated placeholder | PRIMEAPE |
| 150 | ANGERILLA | 4 | DARK/FIGHTING | generated placeholder | PRIMEAPE |
| 151 | TITANFIST | 4 | FIGHTING/STEEL | generated placeholder | MACHAMP |
| 165 | OMNISCIENT | 4 | PSYCHIC_TYPE | generated placeholder | ALAKAZAM |
| 166 | MONOLITH | 4 | GROUND/ROCK | generated placeholder | GOLEM |
| 170 | ADAMANTIX | 3 | GROUND/STEEL | generated placeholder | STEELIX |
| 171 | SKYSCRAPER | 4 | DRAGON/STEEL | generated placeholder | STEELIX |
| 175 | HELLHOUND | 3 | DARK/FIRE | IMPORTED front, mirrored back placeholder | ARCANINE |
| 176 | GATEHOUND | 4 | DARK/FIRE | generated placeholder | ARCANINE |
| 177 | KITSUNE | 3 | FAIRY/FIRE | generated placeholder | NINETALES |
| 178 | FOXFIRE | 4 | FAIRY/FIRE | generated placeholder | NINETALES |
| 185 | UNICORN | 3 | FAIRY/FIRE | generated placeholder | RAPIDASH |
| 186 | DREADSTEED | 4 | FAIRY/FIRE | generated placeholder | RAPIDASH |
| 190 | HELLBOUND | 3 | DARK/FIRE | generated placeholder | HOUNDOOM |
| 191 | PERDITION | 4 | DARK/FIRE | generated placeholder | HOUNDOOM |
| 192 | BLACKSHEEP | 4 | DARK/ELECTRIC | generated placeholder | AMPHAROS |
| 193 | MAGNETRON | 3 | ELECTRIC/STEEL | generated placeholder | MAGNETON |
| 194 | SOLENOID | 4 | ELECTRIC/STEEL | generated placeholder | MAGNETON |
| 195 | MAINFRAME | 3 | NORMAL/STEEL | generated placeholder | PORYGON2 |
| 196 | ALGORITHM | 4 | PSYCHIC_TYPE/STEEL | generated placeholder | PORYGON2 |
| 197 | APPARITION | 4 | DARK/GHOST | generated placeholder | GENGAR |
| 198 | BONEKEEPER | 3 | GHOST/GROUND | generated placeholder | MAROWAK |
| 199 | OSSUARY | 4 | GHOST/GROUND | generated placeholder | MAROWAK |
| 200 | SLUDGELORD | 3 | DARK/POISON | generated placeholder | MUK |
| 201 | SUPERFUND | 4 | POISON | generated placeholder | MUK |
| 202 | MIASMA | 3 | GHOST/POISON | generated placeholder | WEEZING |
| 203 | PANDEMIC | 4 | DARK/POISON | generated placeholder | WEEZING |
| 204 | WARHORN | 3 | GROUND/ROCK | generated placeholder | RHYDON |
| 205 | BEHEMOTH | 4 | GROUND/STEEL | generated placeholder | RHYDON |
| 206 | CLEAVER | 3 | BUG/STEEL | generated placeholder | SCIZOR |
| 207 | HEADSMAN | 4 | BUG/STEEL | generated placeholder | SCIZOR |
| 209 | CTHUSPAWN | 3 | DARK/POISON | own art (hand coded) | TENTACRUEL |
| 210 | CTHULUDON | 4 | DARK/POISON | own art (hand coded) | TENTACRUEL |
| 211 | POLIWRAITH | 4 | GHOST/WATER | generated placeholder | POLIWRATH |
| 213 | AMNESIAC | 3 | PSYCHIC_TYPE/WATER | generated placeholder | SLOWBRO |
| 214 | OBLIVION | 4 | DARK/PSYCHIC_TYPE | generated placeholder | SLOWBRO |
| 215 | TUSKDRIFT | 3 | ICE/WATER | generated placeholder | DEWGONG |
| 216 | FROSTSIREN | 4 | FAIRY/ICE | generated placeholder | DEWGONG |
| 217 | CRYOCLAM | 3 | ICE/WATER | generated placeholder | CLOYSTER |
| 218 | ABYSSHELL | 4 | DARK/ICE | generated placeholder | CLOYSTER |
| 219 | CARAPACE | 3 | ROCK/WATER | generated placeholder | KINGLER |
| 222 | CARCINIZE | 4 | STEEL/WATER | generated placeholder | KINGLER |
| 223 | NEBULON | 3 | PSYCHIC_TYPE/WATER | generated placeholder | STARMIE |
| 224 | SUPERNOVA | 4 | FIRE/PSYCHIC_TYPE | generated placeholder | STARMIE |
| 225 | MAELDRA | 4 | DRAGON/WATER | generated placeholder | KINGDRA |
| 226 | RAGECARP | 3 | DRAGON/WATER | generated placeholder | GYARADOS |
| 227 | WORLDEATER | 4 | DRAGON/WATER | generated placeholder | GYARADOS |
| 231 | TIDEBELLY | 3 | FAIRY/WATER | generated placeholder | AZUMARILL |
| 232 | BEACHBALL | 4 | FAIRY/WATER | generated placeholder | AZUMARILL |
| 234 | NARCOLEPT | 3 | PSYCHIC_TYPE | generated placeholder | HYPNO |
| 235 | SANDMAN | 4 | DARK/PSYCHIC_TYPE | generated placeholder | HYPNO |
| 236 | PLACEBO | 3 | FAIRY | generated placeholder | BLISSEY |
| 237 | HOSPICE | 4 | FAIRY/GHOST | generated placeholder | BLISSEY |
| 239 | MAMMOTH | 3 | GROUND/ICE | generated placeholder | PILOSWINE |
| 240 | ICEAGE | 4 | GROUND/ICE | generated placeholder | PILOSWINE |
| 241 | FROSTBITE | 3 | ICE/PSYCHIC_TYPE | generated placeholder | JYNX |
| 243 | RIMEQUEEN | 4 | FAIRY/ICE | generated placeholder | JYNX |
| 244 | WYRMKING | 4 | DRAGON/FLYING | generated placeholder | DRAGONITE |
| 245 | TYPHONEUS | 4 | DARK/ROCK | IMPORTED front, mirrored back placeholder | TYRANITAR |
