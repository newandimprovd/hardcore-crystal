SECTION "Evolutions and Attacks", ROMX

; Evos+attacks data structure:
; - Evolution methods:
;    * db EVOLVE_LEVEL, level, species
;    * db EVOLVE_ITEM, used item, species
;    * db EVOLVE_TRADE, held item (or -1 for none), species
;    * db EVOLVE_HAPPINESS, TR_* constant (ANYTIME, MORNDAY, NITE), species
;    * db EVOLVE_STAT, level, ATK_*_DEF constant (LT, GT, EQ), species
; - db 0 ; no more evolutions
; - Learnset (in increasing level order):
;    * db level, move
; - db 0 ; no more level-up moves

INCLUDE "data/pokemon/evos_attacks_pointers.asm"

BulbasaurEvosAttacks:
	db EVOLVE_LEVEL, 25, IVYSAUR
	db 0 ; no more evolutions
	db 1, TACKLE
	db 4, GROWL
	db 7, LEECH_SEED
	db 10, RAZOR_LEAF
	db 15, POISONPOWDER
	db 15, SLEEP_POWDER
	db 25, SWEET_SCENT
	db 32, GROWTH
	db 39, SYNTHESIS
	db 46, SOLARBEAM
	db 0 ; no more level-up moves

IvysaurEvosAttacks:
	db EVOLVE_LEVEL, 50, VENUSAUR
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, LEECH_SEED
	db 10, RAZOR_LEAF
	db 15, POISONPOWDER
	db 15, SLEEP_POWDER
	db 29, SWEET_SCENT
	db 38, GROWTH
	db 47, SYNTHESIS
	db 56, SOLARBEAM
	db 0 ; no more level-up moves

VenusaurEvosAttacks:
	db EVOLVE_LEVEL, 75, OVERGROWN
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, LEECH_SEED
	db 1, RAZOR_LEAF
	db 15, POISONPOWDER
	db 15, SLEEP_POWDER
	db 29, SWEET_SCENT
	db 41, GROWTH
	db 53, SYNTHESIS
	db 65, SOLARBEAM
	db 0 ; no more level-up moves

CharmanderEvosAttacks:
	db EVOLVE_LEVEL, 25, CHARMELEON
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, GROWL
	db 7, EMBER
	db 13, SAND_ATTACK
	db 19, RAGE
	db 25, SCARY_FACE
	db 31, FLAMETHROWER
	db 37, SLASH
	db 43, DRAGONBREATH
	db 49, FIRE_SPIN
	db 0 ; no more level-up moves

CharmeleonEvosAttacks:
	db EVOLVE_LEVEL, 50, CHARIZARD
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, GROWL
	db 1, EMBER
	db 13, SAND_ATTACK
	db 20, RAGE
	db 27, SCARY_FACE
	db 34, FLAMETHROWER
	db 41, SLASH
	db 48, DRAGONBREATH
	db 55, FIRE_SPIN
	db 0 ; no more level-up moves

CharizardEvosAttacks:
	db EVOLVE_LEVEL, 75, EMBERWYRM
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, GROWL
	db 1, EMBER
	db 1, SAND_ATTACK
	db 20, RAGE
	db 27, SCARY_FACE
	db 34, FLAMETHROWER
	db 36, WING_ATTACK
	db 44, SLASH
	db 54, DRAGONBREATH
	db 64, FIRE_SPIN
	db 0 ; no more level-up moves

SquirtleEvosAttacks:
	db EVOLVE_LEVEL, 25, WARTORTLE
	db 0 ; no more evolutions
	db 1, TACKLE
	db 4, TAIL_WHIP
	db 7, WATER_GUN
	db 10, WITHDRAW
	db 18, BITE
	db 23, RAPID_SPIN
	db 28, PROTECT
	db 33, RAIN_DANCE
	db 40, SKULL_BASH
	db 47, HYDRO_PUMP
	db 0 ; no more level-up moves

WartortleEvosAttacks:
	db EVOLVE_LEVEL, 50, BLASTOISE
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, TAIL_WHIP
	db 1, WATER_GUN
	db 10, WITHDRAW
	db 19, BITE
	db 25, RAPID_SPIN
	db 31, PROTECT
	db 37, RAIN_DANCE
	db 45, SKULL_BASH
	db 53, HYDRO_PUMP
	db 0 ; no more level-up moves

BlastoiseEvosAttacks:
	db EVOLVE_LEVEL, 75, IRONCLAD
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, TAIL_WHIP
	db 1, WATER_GUN
	db 1, WITHDRAW
	db 19, BITE
	db 25, RAPID_SPIN
	db 31, PROTECT
	db 42, RAIN_DANCE
	db 55, SKULL_BASH
	db 68, HYDRO_PUMP
	db 0 ; no more level-up moves

CaterpieEvosAttacks:
	db EVOLVE_LEVEL, 25, METAPOD
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, STRING_SHOT
	db 12, TWINEEDLE
	db 0 ; no more level-up moves

MetapodEvosAttacks:
	db EVOLVE_LEVEL, 50, BUTTERFREE
	db 0 ; no more evolutions
	db 1, HARDEN
	db 25, TWINEEDLE
	db 0 ; no more level-up moves

ButterfreeEvosAttacks:
	db EVOLVE_LEVEL, 75, CINDERWING
	db 0 ; no more evolutions
	db 1, CONFUSION
	db 13, POISONPOWDER
	db 14, STUN_SPORE
	db 15, SLEEP_POWDER
	db 18, SUPERSONIC
	db 23, WHIRLWIND
	db 28, GUST
	db 34, PSYBEAM
	db 40, SAFEGUARD
	db 50, TWINEEDLE
	db 0 ; no more level-up moves

WeedleEvosAttacks:
	db EVOLVE_LEVEL, 25, KAKUNA
	db 0 ; no more evolutions
	db 1, POISON_STING
	db 1, STRING_SHOT
	db 12, TWINEEDLE
	db 0 ; no more level-up moves

KakunaEvosAttacks:
	db EVOLVE_LEVEL, 50, BEEDRILL
	db 0 ; no more evolutions
	db 1, HARDEN
	db 25, TWINEEDLE
	db 25, SLUDGE_BOMB
	db 0 ; no more level-up moves

BeedrillEvosAttacks:
	db EVOLVE_LEVEL, 75, BEEHEMOTH
	db 0 ; no more evolutions
	db 1, TACKLE
	db 15, FOCUS_ENERGY
	db 20, TWINEEDLE
	db 25, RAGE
	db 30, PURSUIT
	db 35, POISON_STING
	db 40, AGILITY
	db 0 ; no more level-up moves

PidgeyEvosAttacks:
	db EVOLVE_LEVEL, 25, PIDGEOTTO
	db 0 ; no more evolutions
	db 1, TACKLE
	db 5, SAND_ATTACK
	db 9, GUST
	db 15, QUICK_ATTACK
	db 21, WHIRLWIND
	db 29, WING_ATTACK
	db 37, AGILITY
	db 47, MIRROR_MOVE
	db 0 ; no more level-up moves

PidgeottoEvosAttacks:
	db EVOLVE_LEVEL, 50, PIDGEOT
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, SAND_ATTACK
	db 1, GUST
	db 15, QUICK_ATTACK
	db 23, WHIRLWIND
	db 33, WING_ATTACK
	db 43, AGILITY
	db 55, MIRROR_MOVE
	db 0 ; no more level-up moves

PidgeotEvosAttacks:
	db EVOLVE_LEVEL, 75, RAVENOUS
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, SAND_ATTACK
	db 1, GUST
	db 1, QUICK_ATTACK
	db 23, WHIRLWIND
	db 33, WING_ATTACK
	db 46, AGILITY
	db 61, MIRROR_MOVE
	db 0 ; no more level-up moves

RattataEvosAttacks:
	db EVOLVE_LEVEL, 25, RATICATE
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, TAIL_WHIP
	db 7, QUICK_ATTACK
	db 13, HYPER_FANG
	db 20, FOCUS_ENERGY
	db 27, PURSUIT
	db 0 ; no more level-up moves

RaticateEvosAttacks:
	db EVOLVE_LEVEL, 50, PLAGUERAT
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, TAIL_WHIP
	db 1, QUICK_ATTACK
	db 13, HYPER_FANG
	db 20, SCARY_FACE
	db 30, PURSUIT
	db 0 ; no more level-up moves

SpearowEvosAttacks:
	db EVOLVE_LEVEL, 25, FEAROW
	db 0 ; no more evolutions
	db 1, WING_ATTACK
	db 1, GROWL
	db 7, LEER
	db 13, TACKLE
	db 25, PURSUIT
	db 31, MIRROR_MOVE
	db 37, DRILL_PECK
	db 43, AGILITY
	db 0 ; no more level-up moves

FearowEvosAttacks:
	db EVOLVE_LEVEL, 50, DREADBEAK
	db 0 ; no more evolutions
	db 1, WING_ATTACK
	db 1, GROWL
	db 1, LEER
	db 1, TACKLE
	db 26, PURSUIT
	db 32, MIRROR_MOVE
	db 40, DRILL_PECK
	db 47, AGILITY
	db 0 ; no more level-up moves

EkansEvosAttacks:
	db EVOLVE_LEVEL, 25, ARBOK
	db 0 ; no more evolutions
	db 1, WRAP
	db 1, LEER
	db 9, POISON_STING
	db 15, BITE
	db 23, GLARE
	db 29, SCREECH
	db 37, SLUDGE
	db 43, HAZE
	db 0 ; no more level-up moves

ArbokEvosAttacks:
	db EVOLVE_LEVEL, 50, KINGCOBRA
	db 0 ; no more evolutions
	db 1, WRAP
	db 1, LEER
	db 1, POISON_STING
	db 1, BITE
	db 25, GLARE
	db 33, SCREECH
	db 43, SLUDGE
	db 51, HAZE
	db 0 ; no more level-up moves

PikachuEvosAttacks:
	db EVOLVE_LEVEL, 50, RAICHU
	db 0 ; no more evolutions
	db 1, THUNDERSHOCK
	db 1, GROWL
	db 6, TAIL_WHIP
	db 8, THUNDER_WAVE
	db 11, QUICK_ATTACK
	db 15, DOUBLE_TEAM
	db 20, BODY_SLAM
	db 26, THUNDERBOLT
	db 33, AGILITY
	db 41, THUNDER
	db 50, LIGHT_SCREEN
	db 0 ; no more level-up moves

RaichuEvosAttacks:
	db EVOLVE_LEVEL, 75, MEGAWATT
	db 0 ; no more evolutions
	db 1, THUNDERSHOCK
	db 1, TAIL_WHIP
	db 1, QUICK_ATTACK
	db 1, THUNDERBOLT
	db 0 ; no more level-up moves

ElderwoodEvosAttacks:
	db 0 ; no more evolutions
	db 23, SYNTHESIS
	db 31, BODY_SLAM
	db 41, LIGHT_SCREEN
	db 51, SAFEGUARD
	db 61, SOLARBEAM
	db 75, SHADOW_SNEAK
	db 75, GIGA_DRAIN
	db 80, SHADOW_BALL
	db 85, ENERGY_BALL
	db 90, NIGHT_SHADE
	db 0 ; no more level-up moves

CalderaEvosAttacks:
	db 0 ; no more evolutions
	db 21, QUICK_ATTACK
	db 31, FLAME_WHEEL
	db 45, SWIFT
	db 60, FLAMETHROWER
	db 75, FAINT_ATTACK
	db 75, FLARE_BLITZ
	db 80, NIGHT_SLASH
	db 85, FIRE_BLAST
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

NidoranFEvosAttacks:
	db EVOLVE_LEVEL, 25, NIDORINA
	db 0 ; no more evolutions
	db 1, GROWL
	db 1, TACKLE
	db 8, SCRATCH
	db 12, DOUBLE_KICK
	db 17, POISON_STING
	db 23, TAIL_WHIP
	db 30, BITE
	db 0 ; no more level-up moves

NidorinaEvosAttacks:
	db EVOLVE_LEVEL, 50, NIDOQUEEN
	db 0 ; no more evolutions
	db 1, GROWL
	db 1, TACKLE
	db 8, SCRATCH
	db 12, DOUBLE_KICK
	db 19, POISON_STING
	db 27, TAIL_WHIP
	db 36, BITE
	db 0 ; no more level-up moves

NidoqueenEvosAttacks:
	db EVOLVE_LEVEL, 75, MATRIARCH
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, SCRATCH
	db 1, DOUBLE_KICK
	db 1, TAIL_WHIP
	db 23, BODY_SLAM
	db 50, SLUDGE_BOMB
	db 50, DIG
	db 0 ; no more level-up moves

NidoranMEvosAttacks:
	db EVOLVE_LEVEL, 25, NIDORINO
	db 0 ; no more evolutions
	db 1, LEER
	db 1, TACKLE
	db 12, DOUBLE_KICK
	db 17, POISON_STING
	db 23, FOCUS_ENERGY
	db 38, HORN_DRILL
	db 0 ; no more level-up moves

NidorinoEvosAttacks:
	db EVOLVE_LEVEL, 50, NIDOKING
	db 0 ; no more evolutions
	db 1, LEER
	db 1, TACKLE
	db 12, DOUBLE_KICK
	db 19, POISON_STING
	db 27, FOCUS_ENERGY
	db 46, HORN_DRILL
	db 0 ; no more level-up moves

NidokingEvosAttacks:
	db EVOLVE_LEVEL, 75, TYRANT
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, DOUBLE_KICK
	db 1, POISON_STING
	db 23, THRASH
	db 50, DIG
	db 0 ; no more level-up moves

ClefairyEvosAttacks:
	db EVOLVE_LEVEL, 50, CLEFABLE
	db 0 ; no more evolutions
	db 1, POUND
	db 1, GROWL
	db 4, ENCORE
	db 8, SING
	db 13, DOUBLESLAP
	db 19, MINIMIZE
	db 25, FAIRY_WIND
	db 26, DEFENSE_CURL
	db 34, METRONOME
	db 43, MOONLIGHT
	db 53, LIGHT_SCREEN
	db 0 ; no more level-up moves

ClefableEvosAttacks:
	db EVOLVE_LEVEL, 75, MOONQUEEN
	db 0 ; no more evolutions
	db 1, SING
	db 1, DOUBLESLAP
	db 1, METRONOME
	db 1, MOONLIGHT
	db 50, FAIRY_WIND
	db 0 ; no more level-up moves

VulpixEvosAttacks:
	db EVOLVE_LEVEL, 25, NINETALES
	db 0 ; no more evolutions
	db 1, EMBER
	db 1, TAIL_WHIP
	db 7, QUICK_ATTACK
	db 13, ROAR
	db 19, CONFUSE_RAY
	db 25, SAFEGUARD
	db 31, FLAMETHROWER
	db 37, FIRE_SPIN
	db 0 ; no more level-up moves

NinetalesEvosAttacks:
	db EVOLVE_LEVEL, 50, KITSUNE
	db 0 ; no more evolutions
	db 1, EMBER
	db 1, QUICK_ATTACK
	db 1, CONFUSE_RAY
	db 1, SAFEGUARD
	db 43, FIRE_SPIN
	db 0 ; no more level-up moves

JigglypuffEvosAttacks:
	db EVOLVE_LEVEL, 50, WIGGLYTUFF
	db 0 ; no more evolutions
	db 1, SING
	db 4, DEFENSE_CURL
	db 9, POUND
	db 14, DISABLE
	db 19, ROLLOUT
	db 24, DOUBLESLAP
	db 25, FAIRY_WIND
	db 29, REST
	db 34, BODY_SLAM
	db 39, DOUBLE_EDGE
	db 0 ; no more level-up moves

WigglytuffEvosAttacks:
	db EVOLVE_LEVEL, 75, SOPORIFIC
	db 0 ; no more evolutions
	db 1, SING
	db 1, DISABLE
	db 1, DEFENSE_CURL
	db 1, DOUBLESLAP
	db 50, FAIRY_WIND
	db 0 ; no more level-up moves

ZubatEvosAttacks:
	db EVOLVE_LEVEL, 25, GOLBAT
	db 0 ; no more evolutions
	db 1, LEECH_LIFE
	db 6, SUPERSONIC
	db 12, BITE
	db 12, SLUDGE_BOMB
	db 19, CONFUSE_RAY
	db 27, WING_ATTACK
	db 36, MEAN_LOOK
	db 46, HAZE
	db 0 ; no more level-up moves

GolbatEvosAttacks:
	db EVOLVE_LEVEL, 50, CROBAT
	db 0 ; no more evolutions
	db 1, SCREECH
	db 1, LEECH_LIFE
	db 1, SUPERSONIC
	db 12, BITE
	db 19, CONFUSE_RAY
	db 25, SLUDGE_BOMB
	db 30, WING_ATTACK
	db 42, MEAN_LOOK
	db 55, HAZE
	db 0 ; no more level-up moves

OddishEvosAttacks:
	db EVOLVE_LEVEL, 25, GLOOM
	db 0 ; no more evolutions
	db 1, ABSORB
	db 7, SWEET_SCENT
	db 14, POISONPOWDER
	db 16, STUN_SPORE
	db 18, SLEEP_POWDER
	db 23, SLUDGE
	db 32, MOONLIGHT
	db 39, PETAL_DANCE
	db 0 ; no more level-up moves

GloomEvosAttacks:
	db EVOLVE_LEVEL, 50, BELLOSSOM
	db 0 ; no more evolutions
	db 1, ABSORB
	db 1, SWEET_SCENT
	db 1, POISONPOWDER
	db 16, STUN_SPORE
	db 18, SLEEP_POWDER
	db 24, SLUDGE
	db 35, MOONLIGHT
	db 44, PETAL_DANCE
	db 0 ; no more level-up moves

DeathrollEvosAttacks:
	db 0 ; no more evolutions
	db 21, BITE
	db 28, SCARY_FACE
	db 38, SLASH
	db 47, SCREECH
	db 58, HYDRO_PUMP
	db 75, WATERFALL
	db 80, CRUNCH
	db 85, AQUA_TAIL
	db 90, NIGHT_SLASH
	db 0 ; no more level-up moves

ParasEvosAttacks:
	db EVOLVE_LEVEL, 25, PARASECT
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 7, STUN_SPORE
	db 13, POISONPOWDER
	db 19, LEECH_LIFE
	db 25, SPORE
	db 31, SLASH
	db 37, GROWTH
	db 43, GIGA_DRAIN
	db 0 ; no more level-up moves

ParasectEvosAttacks:
	db EVOLVE_LEVEL, 50, CORDYCEPS
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, STUN_SPORE
	db 1, POISONPOWDER
	db 19, LEECH_LIFE
	db 28, SPORE
	db 37, SLASH
	db 46, GROWTH
	db 55, GIGA_DRAIN
	db 0 ; no more level-up moves

VenonatEvosAttacks:
	db EVOLVE_LEVEL, 25, VENOMOTH
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, DISABLE
	db 1, FORESIGHT
	db 9, SUPERSONIC
	db 17, CONFUSION
	db 20, POISONPOWDER
	db 25, LEECH_LIFE
	db 28, STUN_SPORE
	db 33, PSYBEAM
	db 36, SLEEP_POWDER
	db 41, PSYCHIC_M
	db 0 ; no more level-up moves

VenomothEvosAttacks:
	db EVOLVE_LEVEL, 50, CANDLEMOTH
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, DISABLE
	db 1, FORESIGHT
	db 1, SUPERSONIC
	db 17, CONFUSION
	db 20, POISONPOWDER
	db 25, LEECH_LIFE
	db 28, STUN_SPORE
	db 31, GUST
	db 36, PSYBEAM
	db 42, SLEEP_POWDER
	db 52, PSYCHIC_M
	db 0 ; no more level-up moves

OvergrownEvosAttacks:
	db 0 ; no more evolutions
	db 29, SWEET_SCENT
	db 41, GROWTH
	db 53, SYNTHESIS
	db 65, SOLARBEAM
	db 75, FAINT_ATTACK
	db 75, GIGA_DRAIN
	db 80, NIGHT_SLASH
	db 85, ENERGY_BALL
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

EmberwyrmEvosAttacks:
	db 0 ; no more evolutions
	db 20, RAGE
	db 27, SCARY_FACE
	db 34, FLAMETHROWER
	db 36, WING_ATTACK
	db 44, SLASH
	db 54, DRAGONBREATH
	db 64, FIRE_SPIN
	db 75, FLARE_BLITZ
	db 80, DRAGON_PULSE
	db 85, FIRE_BLAST
	db 90, OUTRAGE
	db 0 ; no more level-up moves

MeowthEvosAttacks:
	db EVOLVE_LEVEL, 25, PERSIAN
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, GROWL
	db 11, BITE
	db 20, PAY_DAY
	db 28, FAINT_ATTACK
	db 35, SCREECH
	db 46, SLASH
	db 0 ; no more level-up moves

PersianEvosAttacks:
	db EVOLVE_LEVEL, 50, ALLEYCAT
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, GROWL
	db 1, BITE
	db 20, PAY_DAY
	db 29, FAINT_ATTACK
	db 38, SCREECH
	db 53, SLASH
	db 0 ; no more level-up moves

PsyduckEvosAttacks:
	db EVOLVE_LEVEL, 25, GOLDUCK
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 5, TAIL_WHIP
	db 10, DISABLE
	db 16, CONFUSION
	db 23, SCREECH
	db 31, PSYCH_UP
	db 50, HYDRO_PUMP
	db 0 ; no more level-up moves

GolduckEvosAttacks:
	db EVOLVE_LEVEL, 50, MIGRAINE
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, TAIL_WHIP
	db 1, DISABLE
	db 1, CONFUSION
	db 23, SCREECH
	db 31, PSYCH_UP
	db 58, HYDRO_PUMP
	db 0 ; no more level-up moves

MankeyEvosAttacks:
	db EVOLVE_LEVEL, 25, PRIMEAPE
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, LEER
	db 9, DOUBLE_KICK
	db 27, FOCUS_ENERGY
	db 33, SEISMIC_TOSS
	db 39, CROSS_CHOP
	db 45, SCREECH
	db 51, THRASH
	db 0 ; no more level-up moves

PrimeapeEvosAttacks:
	db EVOLVE_LEVEL, 50, BERSERKER
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, LEER
	db 1, DOUBLE_KICK
	db 1, RAGE
	db 27, FOCUS_ENERGY
	db 36, SEISMIC_TOSS
	db 45, CROSS_CHOP
	db 54, SCREECH
	db 63, THRASH
	db 0 ; no more level-up moves

GrowlitheEvosAttacks:
	db EVOLVE_LEVEL, 25, ARCANINE
	db 0 ; no more evolutions
	db 1, BITE
	db 1, ROAR
	db 9, EMBER
	db 18, LEER
	db 26, TAKE_DOWN
	db 34, FLAME_WHEEL
	db 42, AGILITY
	db 50, FLAMETHROWER
	db 0 ; no more level-up moves

ArcanineEvosAttacks:
	db EVOLVE_LEVEL, 50, HELLHOUND
	db 0 ; no more evolutions
	db 1, ROAR
	db 1, LEER
	db 1, TAKE_DOWN
	db 1, FLAME_WHEEL
	db 50, EXTREMESPEED
	db 0 ; no more level-up moves

PoliwagEvosAttacks:
	db EVOLVE_LEVEL, 25, POLIWHIRL
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 7, HYPNOSIS
	db 19, DOUBLESLAP
	db 25, RAIN_DANCE
	db 31, BODY_SLAM
	db 37, BELLY_DRUM
	db 43, HYDRO_PUMP
	db 0 ; no more level-up moves

PoliwhirlEvosAttacks:
	db EVOLVE_LEVEL, 50, POLIWRATH
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 1, HYPNOSIS
	db 19, DOUBLESLAP
	db 27, RAIN_DANCE
	db 35, BODY_SLAM
	db 43, BELLY_DRUM
	db 51, HYDRO_PUMP
	db 0 ; no more level-up moves

PoliwrathEvosAttacks:
	db EVOLVE_LEVEL, 75, POLIWRAITH
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 1, HYPNOSIS
	db 1, DOUBLESLAP
	db 1, SUBMISSION
	db 51, LOCK_ON
	db 0 ; no more level-up moves

AbraEvosAttacks:
	db EVOLVE_LEVEL, 25, KADABRA
	db 0 ; no more evolutions
	db 1, TELEPORT
	db 12, CONFUSION
	db 0 ; no more level-up moves

KadabraEvosAttacks:
	db EVOLVE_LEVEL, 50, ALAKAZAM
	db 0 ; no more evolutions
	db 1, TELEPORT
	db 1, KINESIS
	db 1, CONFUSION
	db 18, DISABLE
	db 21, PSYBEAM
	db 26, RECOVER
	db 31, FUTURE_SIGHT
	db 38, PSYCHIC_M
	db 45, REFLECT
	db 0 ; no more level-up moves

AlakazamEvosAttacks:
	db EVOLVE_LEVEL, 75, OMNISCIENT
	db 0 ; no more evolutions
	db 1, TELEPORT
	db 1, KINESIS
	db 1, CONFUSION
	db 18, DISABLE
	db 21, PSYBEAM
	db 26, RECOVER
	db 31, FUTURE_SIGHT
	db 38, PSYCHIC_M
	db 45, REFLECT
	db 0 ; no more level-up moves

MachopEvosAttacks:
	db EVOLVE_LEVEL, 25, MACHOKE
	db 0 ; no more evolutions
	db 1, DOUBLE_KICK
	db 1, LEER
	db 7, FOCUS_ENERGY
	db 19, SEISMIC_TOSS
	db 25, FORESIGHT
	db 31, VITAL_THROW
	db 37, CROSS_CHOP
	db 43, SCARY_FACE
	db 49, SUBMISSION
	db 0 ; no more level-up moves

MachokeEvosAttacks:
	db EVOLVE_LEVEL, 50, MACHAMP
	db 0 ; no more evolutions
	db 1, DOUBLE_KICK
	db 1, LEER
	db 1, FOCUS_ENERGY
	db 19, SEISMIC_TOSS
	db 25, FORESIGHT
	db 34, VITAL_THROW
	db 43, CROSS_CHOP
	db 52, SCARY_FACE
	db 61, SUBMISSION
	db 0 ; no more level-up moves

MachampEvosAttacks:
	db EVOLVE_LEVEL, 75, TITANFIST
	db 0 ; no more evolutions
	db 1, DOUBLE_KICK
	db 1, LEER
	db 1, FOCUS_ENERGY
	db 19, SEISMIC_TOSS
	db 25, FORESIGHT
	db 34, VITAL_THROW
	db 43, CROSS_CHOP
	db 52, SCARY_FACE
	db 61, SUBMISSION
	db 0 ; no more level-up moves

BellsproutEvosAttacks:
	db EVOLVE_LEVEL, 25, WEEPINBELL
	db 0 ; no more evolutions
	db 1, RAZOR_LEAF
	db 6, GROWTH
	db 11, WRAP
	db 15, SLEEP_POWDER
	db 17, POISONPOWDER
	db 19, STUN_SPORE
	db 23, SLUDGE
	db 30, SWEET_SCENT
	db 45, BODY_SLAM
	db 0 ; no more level-up moves

WeepinbellEvosAttacks:
	db EVOLVE_LEVEL, 50, VICTREEBEL
	db 0 ; no more evolutions
	db 1, RAZOR_LEAF
	db 1, GROWTH
	db 1, WRAP
	db 15, SLEEP_POWDER
	db 17, POISONPOWDER
	db 19, STUN_SPORE
	db 24, SLUDGE
	db 33, SWEET_SCENT
	db 54, BODY_SLAM
	db 0 ; no more level-up moves

VictreebelEvosAttacks:
	db EVOLVE_LEVEL, 75, MAWBLOOM
	db 0 ; no more evolutions
	db 1, RAZOR_LEAF
	db 1, SLEEP_POWDER
	db 1, SWEET_SCENT
	db 0 ; no more level-up moves

TentacoolEvosAttacks:
	db EVOLVE_LEVEL, 25, TENTACRUEL
	db 0 ; no more evolutions
	db 1, POISON_STING
	db 6, SUPERSONIC
	db 12, TACKLE
	db 19, SLUDGE
	db 25, BUBBLEBEAM
	db 30, WRAP
	db 36, BARRIER
	db 43, SCREECH
	db 49, HYDRO_PUMP
	db 0 ; no more level-up moves

TentacruelEvosAttacks:
	db EVOLVE_LEVEL, 50, CTHUSPAWN
	db 0 ; no more evolutions
	db 1, POISON_STING
	db 1, SUPERSONIC
	db 1, TACKLE
	db 19, SLUDGE
	db 25, BUBBLEBEAM
	db 30, WRAP
	db 38, BARRIER
	db 47, SCREECH
	db 55, HYDRO_PUMP
	db 0 ; no more level-up moves

GeodudeEvosAttacks:
	db EVOLVE_LEVEL, 25, GRAVELER
	db 0 ; no more evolutions
	db 1, TACKLE
	db 6, DEFENSE_CURL
	db 11, ROCK_THROW
	db 16, MAGNITUDE
	db 21, SELFDESTRUCT
	db 26, HARDEN
	db 31, ROLLOUT
	db 36, EARTHQUAKE
	db 41, EXPLOSION
	db 0 ; no more level-up moves

GravelerEvosAttacks:
	db EVOLVE_LEVEL, 50, GOLEM
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, DEFENSE_CURL
	db 1, ROCK_THROW
	db 16, MAGNITUDE
	db 21, SELFDESTRUCT
	db 27, HARDEN
	db 34, ROLLOUT
	db 41, EARTHQUAKE
	db 48, EXPLOSION
	db 0 ; no more level-up moves

GolemEvosAttacks:
	db EVOLVE_LEVEL, 75, MONOLITH
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, DEFENSE_CURL
	db 1, ROCK_THROW
	db 1, MAGNITUDE
	db 21, SELFDESTRUCT
	db 27, HARDEN
	db 34, ROLLOUT
	db 41, EARTHQUAKE
	db 48, EXPLOSION
	db 0 ; no more level-up moves

PonytaEvosAttacks:
	db EVOLVE_LEVEL, 25, RAPIDASH
	db 0 ; no more evolutions
	db 1, TACKLE
	db 4, GROWL
	db 8, TAIL_WHIP
	db 13, EMBER
	db 19, HEADBUTT
	db 26, FIRE_SPIN
	db 34, TAKE_DOWN
	db 43, AGILITY
	db 53, FIRE_BLAST
	db 0 ; no more level-up moves

RapidashEvosAttacks:
	db EVOLVE_LEVEL, 50, UNICORN
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, TAIL_WHIP
	db 1, EMBER
	db 19, HEADBUTT
	db 26, FIRE_SPIN
	db 34, TAKE_DOWN
	db 47, AGILITY
	db 61, FIRE_BLAST
	db 0 ; no more level-up moves

SlowpokeEvosAttacks:
	db EVOLVE_LEVEL, 25, SLOWBRO
	db 0 ; no more evolutions
	db 1, CURSE
	db 1, TACKLE
	db 6, GROWL
	db 15, WATER_GUN
	db 20, CONFUSION
	db 29, DISABLE
	db 34, HEADBUTT
	db 43, AMNESIA
	db 48, PSYCHIC_M
	db 0 ; no more level-up moves

SlowbroEvosAttacks:
	db EVOLVE_LEVEL, 50, AMNESIAC
	db 0 ; no more evolutions
	db 1, CURSE
	db 1, TACKLE
	db 1, GROWL
	db 1, WATER_GUN
	db 20, CONFUSION
	db 29, DISABLE
	db 34, HEADBUTT
	db 37, WITHDRAW
	db 46, AMNESIA
	db 54, PSYCHIC_M
	db 0 ; no more level-up moves

MagnemiteEvosAttacks:
	db EVOLVE_LEVEL, 25, MAGNETON
	db 0 ; no more evolutions
	db 1, TACKLE
	db 6, THUNDERSHOCK
	db 11, SUPERSONIC
	db 12, METAL_CLAW
	db 16, SWIFT
	db 21, THUNDER_WAVE
	db 27, LOCK_ON
	db 39, SCREECH
	db 45, ZAP_CANNON
	db 0 ; no more level-up moves

MagnetonEvosAttacks:
	db EVOLVE_LEVEL, 50, MAGNETRON
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, THUNDERSHOCK
	db 1, SUPERSONIC
	db 1, SWIFT
	db 21, THUNDER_WAVE
	db 25, METAL_CLAW
	db 27, LOCK_ON
	db 35, TRI_ATTACK
	db 43, SCREECH
	db 53, ZAP_CANNON
	db 0 ; no more level-up moves

IroncladEvosAttacks:
	db 0 ; no more evolutions
	db 25, RAPID_SPIN
	db 31, PROTECT
	db 42, RAIN_DANCE
	db 55, SKULL_BASH
	db 68, HYDRO_PUMP
	db 75, METAL_CLAW
	db 75, WATERFALL
	db 80, IRON_HEAD
	db 85, AQUA_TAIL
	db 90, FLASH_CANNON
	db 0 ; no more level-up moves

SentinelEvosAttacks:
	db EVOLVE_LEVEL, 75, PANOPTICON
	db 0 ; no more evolutions
	db 28, BODY_SLAM
	db 38, REST
	db 48, AMNESIA
	db 50, SLASH
	db 55, TRI_ATTACK
	db 60, HYPER_BEAM
	db 0 ; no more level-up moves

PanopticonEvosAttacks:
	db 0 ; no more evolutions
	db 28, BODY_SLAM
	db 38, REST
	db 48, AMNESIA
	db 50, SLASH
	db 55, TRI_ATTACK
	db 60, HYPER_BEAM
	db 75, FAINT_ATTACK
	db 75, NIGHT_SLASH
	db 80, DARK_PULSE
	db 85, CRUNCH
	db 0 ; no more level-up moves

SeelEvosAttacks:
	db EVOLVE_LEVEL, 25, DEWGONG
	db 0 ; no more evolutions
	db 1, HEADBUTT
	db 5, GROWL
	db 12, AQUA_JET
	db 16, AURORA_BEAM
	db 21, REST
	db 32, TAKE_DOWN
	db 37, ICE_BEAM
	db 48, SAFEGUARD
	db 0 ; no more level-up moves

DewgongEvosAttacks:
	db EVOLVE_LEVEL, 50, TUSKDRIFT
	db 0 ; no more evolutions
	db 1, HEADBUTT
	db 1, GROWL
	db 1, AURORA_BEAM
	db 21, REST
	db 25, AQUA_JET
	db 32, TAKE_DOWN
	db 43, ICE_BEAM
	db 60, SAFEGUARD
	db 0 ; no more level-up moves

GrimerEvosAttacks:
	db EVOLVE_LEVEL, 25, MUK
	db 0 ; no more evolutions
	db 1, TOXIC
	db 1, POUND
	db 5, HARDEN
	db 10, DISABLE
	db 16, SLUDGE
	db 23, MINIMIZE
	db 31, SCREECH
	db 40, ACID_ARMOR
	db 50, SLUDGE_BOMB
	db 0 ; no more level-up moves

MukEvosAttacks:
	db EVOLVE_LEVEL, 50, SLUDGELORD
	db 0 ; no more evolutions
	db 1, TOXIC
	db 1, POUND
	db 1, HARDEN
	db 23, MINIMIZE
	db 31, SCREECH
	db 37, DISABLE
	db 45, SLUDGE
	db 45, ACID_ARMOR
	db 60, SLUDGE_BOMB
	db 0 ; no more level-up moves

ShellderEvosAttacks:
	db EVOLVE_LEVEL, 25, CLOYSTER
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, WITHDRAW
	db 9, SUPERSONIC
	db 17, AURORA_BEAM
	db 25, PROTECT
	db 33, LEER
	db 41, CLAMP
	db 49, ICE_BEAM
	db 0 ; no more level-up moves

CloysterEvosAttacks:
	db EVOLVE_LEVEL, 50, CRYOCLAM
	db 0 ; no more evolutions
	db 1, WITHDRAW
	db 1, SUPERSONIC
	db 1, AURORA_BEAM
	db 1, PROTECT
	db 25, AQUA_JET
	db 33, SPIKES
	db 41, DOUBLESLAP
	db 0 ; no more level-up moves

GastlyEvosAttacks:
	db EVOLVE_LEVEL, 25, HAUNTER
	db 0 ; no more evolutions
	db 1, HYPNOSIS
	db 1, SCRATCH
	db 8, CONFUSE_RAY
	db 13, MEAN_LOOK
	db 16, CURSE
	db 21, NIGHT_SHADE
	db 33, DREAM_EATER
	db 36, DESTINY_BOND
	db 0 ; no more level-up moves

HaunterEvosAttacks:
	db EVOLVE_LEVEL, 50, GENGAR
	db 0 ; no more evolutions
	db 1, HYPNOSIS
	db 1, SCRATCH
	db 1, CONFUSE_RAY
	db 13, MEAN_LOOK
	db 16, CURSE
	db 21, NIGHT_SHADE
	db 39, DREAM_EATER
	db 48, DESTINY_BOND
	db 0 ; no more level-up moves

GengarEvosAttacks:
	db EVOLVE_LEVEL, 75, APPARITION
	db 0 ; no more evolutions
	db 1, HYPNOSIS
	db 1, SCRATCH
	db 1, CONFUSE_RAY
	db 13, MEAN_LOOK
	db 16, CURSE
	db 21, NIGHT_SHADE
	db 39, DREAM_EATER
	db 48, DESTINY_BOND
	db 0 ; no more level-up moves

OnixEvosAttacks:
	db EVOLVE_LEVEL, 25, STEELIX
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, SCREECH
	db 10, BIND
	db 12, DIG
	db 14, ROCK_THROW
	db 23, HARDEN
	db 27, RAGE
	db 36, SANDSTORM
	db 40, BODY_SLAM
	db 0 ; no more level-up moves

DrowzeeEvosAttacks:
	db EVOLVE_LEVEL, 25, HYPNO
	db 0 ; no more evolutions
	db 1, POUND
	db 1, HYPNOSIS
	db 10, DISABLE
	db 18, CONFUSION
	db 25, HEADBUTT
	db 31, TOXIC
	db 36, MEDITATE
	db 40, PSYCHIC_M
	db 43, PSYCH_UP
	db 45, FUTURE_SIGHT
	db 0 ; no more level-up moves

HypnoEvosAttacks:
	db EVOLVE_LEVEL, 50, NARCOLEPT
	db 0 ; no more evolutions
	db 1, POUND
	db 1, HYPNOSIS
	db 1, DISABLE
	db 1, CONFUSION
	db 25, HEADBUTT
	db 33, TOXIC
	db 40, MEDITATE
	db 49, PSYCHIC_M
	db 55, PSYCH_UP
	db 60, FUTURE_SIGHT
	db 0 ; no more level-up moves

KrabbyEvosAttacks:
	db EVOLVE_LEVEL, 25, KINGLER
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 5, LEER
	db 12, TACKLE
	db 16, HARDEN
	db 23, HEADBUTT
	db 27, GUILLOTINE
	db 34, PROTECT
	db 41, CRABHAMMER
	db 0 ; no more level-up moves

KinglerEvosAttacks:
	db EVOLVE_LEVEL, 50, CARAPACE
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 1, LEER
	db 1, TACKLE
	db 16, HARDEN
	db 23, HEADBUTT
	db 27, GUILLOTINE
	db 38, PROTECT
	db 49, CRABHAMMER
	db 0 ; no more level-up moves

ProfessowlEvosAttacks:
	db EVOLVE_LEVEL, 75, EMERITUS
	db 0 ; no more evolutions
	db 25, REFLECT
	db 33, TAKE_DOWN
	db 41, CONFUSION
	db 50, WING_ATTACK
	db 50, DRILL_PECK
	db 55, ZEN_HEADBUTT
	db 57, DREAM_EATER
	db 60, BRAVE_BIRD
	db 65, PSYCHO_CUT
	db 0 ; no more level-up moves

EmeritusEvosAttacks:
	db 0 ; no more evolutions
	db 25, REFLECT
	db 33, TAKE_DOWN
	db 41, CONFUSION
	db 50, WING_ATTACK
	db 50, DRILL_PECK
	db 55, ZEN_HEADBUTT
	db 57, DREAM_EATER
	db 60, BRAVE_BIRD
	db 65, PSYCHO_CUT
	db 75, HURRICANE
	db 80, PSYCHIC_M
	db 0 ; no more level-up moves

PlagueratEvosAttacks:
	db EVOLVE_LEVEL, 75, RATKING
	db 0 ; no more evolutions
	db 20, SCARY_FACE
	db 30, PURSUIT
	db 50, BODY_SLAM
	db 50, SLASH
	db 55, FAINT_ATTACK
	db 60, TRI_ATTACK
	db 65, CRUNCH
	db 0 ; no more level-up moves

RatkingEvosAttacks:
	db 0 ; no more evolutions
	db 20, SCARY_FACE
	db 30, PURSUIT
	db 50, BODY_SLAM
	db 50, SLASH
	db 55, FAINT_ATTACK
	db 60, TRI_ATTACK
	db 65, CRUNCH
	db 75, DARK_PULSE
	db 80, NIGHT_SLASH
	db 0 ; no more level-up moves

CuboneEvosAttacks:
	db EVOLVE_LEVEL, 25, MAROWAK
	db 0 ; no more evolutions
	db 1, GROWL
	db 5, TAIL_WHIP
	db 9, BONEMERANG
	db 13, HEADBUTT
	db 17, LEER
	db 21, FOCUS_ENERGY
	db 29, RAGE
	db 33, FALSE_SWIPE
	db 37, THRASH
	db 41, BONE_RUSH
	db 0 ; no more level-up moves

MarowakEvosAttacks:
	db EVOLVE_LEVEL, 50, BONEKEEPER
	db 0 ; no more evolutions
	db 1, GROWL
	db 1, TAIL_WHIP
	db 1, BONEMERANG
	db 1, HEADBUTT
	db 17, LEER
	db 21, FOCUS_ENERGY
	db 32, RAGE
	db 39, FALSE_SWIPE
	db 46, THRASH
	db 53, BONE_RUSH
	db 0 ; no more level-up moves

RavenousEvosAttacks:
	db 0 ; no more evolutions
	db 23, WHIRLWIND
	db 33, WING_ATTACK
	db 46, AGILITY
	db 61, MIRROR_MOVE
	db 75, FAINT_ATTACK
	db 75, BRAVE_BIRD
	db 80, NIGHT_SLASH
	db 85, HURRICANE
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

CinderwingEvosAttacks:
	db 0 ; no more evolutions
	db 23, WHIRLWIND
	db 28, GUST
	db 34, PSYBEAM
	db 40, SAFEGUARD
	db 50, TWINEEDLE
	db 75, FIRE_FANG
	db 75, BUG_BUZZ
	db 80, FLARE_BLITZ
	db 85, MEGAHORN
	db 90, FIRE_BLAST
	db 0 ; no more level-up moves

BeehemothEvosAttacks:
	db 0 ; no more evolutions
	db 20, TWINEEDLE
	db 25, RAGE
	db 30, PURSUIT
	db 35, POISON_STING
	db 40, AGILITY
	db 75, BUG_BUZZ
	db 80, POISON_JAB
	db 85, MEGAHORN
	db 90, GUNK_SHOT
	db 0 ; no more level-up moves

KoffingEvosAttacks:
	db EVOLVE_LEVEL, 25, WEEZING
	db 0 ; no more evolutions
	db 1, TOXIC
	db 1, TACKLE
	db 9, SLUDGE
	db 17, SELFDESTRUCT
	db 25, SAND_ATTACK
	db 33, HAZE
	db 41, EXPLOSION
	db 45, DESTINY_BOND
	db 0 ; no more level-up moves

WeezingEvosAttacks:
	db EVOLVE_LEVEL, 50, MIASMA
	db 0 ; no more evolutions
	db 1, TOXIC
	db 1, TACKLE
	db 1, SLUDGE
	db 1, SELFDESTRUCT
	db 25, SAND_ATTACK
	db 33, HAZE
	db 44, EXPLOSION
	db 51, DESTINY_BOND
	db 0 ; no more level-up moves

RhyhornEvosAttacks:
	db EVOLVE_LEVEL, 25, RHYDON
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, TAIL_WHIP
	db 12, ROCK_SLIDE
	db 13, HEADBUTT
	db 31, SCARY_FACE
	db 37, HORN_DRILL
	db 49, TAKE_DOWN
	db 55, EARTHQUAKE
	db 0 ; no more level-up moves

RhydonEvosAttacks:
	db EVOLVE_LEVEL, 50, WARHORN
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, TAIL_WHIP
	db 1, HEADBUTT
	db 25, ROCK_SLIDE
	db 31, SCARY_FACE
	db 37, HORN_DRILL
	db 54, TAKE_DOWN
	db 65, EARTHQUAKE
	db 0 ; no more level-up moves

ChanseyEvosAttacks:
	db EVOLVE_LEVEL, 25, BLISSEY
	db 0 ; no more evolutions
	db 1, POUND
	db 4, FAIRY_WIND
	db 5, GROWL
	db 9, TAIL_WHIP
	db 9, DRAIN_KISS
	db 13, SOFTBOILED
	db 17, DOUBLESLAP
	db 23, MINIMIZE
	db 29, SING
	db 35, SLASH
	db 41, DEFENSE_CURL
	db 49, LIGHT_SCREEN
	db 57, DOUBLE_EDGE
	db 0 ; no more level-up moves

DandelionEvosAttacks:
	db 0 ; no more evolutions
	db 22, LEECH_SEED
	db 33, STRING_SHOT
	db 44, MEGA_DRAIN
	db 50, WING_ATTACK
	db 75, FAIRY_WIND
	db 75, DRAIN_KISS
	db 75, GIGA_DRAIN
	db 80, DAZZLE_GLEAM
	db 85, ENERGY_BALL
	db 90, MOONBLAST
	db 0 ; no more level-up moves

DreadbeakEvosAttacks:
	db EVOLVE_LEVEL, 75, DOOMTALON
	db 0 ; no more evolutions
	db 26, PURSUIT
	db 32, MIRROR_MOVE
	db 40, DRILL_PECK
	db 47, AGILITY
	db 50, WING_ATTACK
	db 55, FAINT_ATTACK
	db 60, BRAVE_BIRD
	db 65, CRUNCH
	db 0 ; no more level-up moves

HorseaEvosAttacks:
	db EVOLVE_LEVEL, 25, SEADRA
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 8, SAND_ATTACK
	db 15, LEER
	db 29, TWISTER
	db 36, AGILITY
	db 43, HYDRO_PUMP
	db 0 ; no more level-up moves

SeadraEvosAttacks:
	db EVOLVE_LEVEL, 50, KINGDRA
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 1, SAND_ATTACK
	db 1, LEER
	db 29, TWISTER
	db 40, AGILITY
	db 51, HYDRO_PUMP
	db 0 ; no more level-up moves

DoomtalonEvosAttacks:
	db 0 ; no more evolutions
	db 26, PURSUIT
	db 32, MIRROR_MOVE
	db 40, DRILL_PECK
	db 47, AGILITY
	db 50, WING_ATTACK
	db 55, FAINT_ATTACK
	db 60, BRAVE_BIRD
	db 65, CRUNCH
	db 75, HURRICANE
	db 80, DARK_PULSE
	db 85, NIGHT_SLASH
	db 0 ; no more level-up moves

KingcobraEvosAttacks:
	db EVOLVE_LEVEL, 75, BASILISK
	db 0 ; no more evolutions
	db 25, GLARE
	db 33, SCREECH
	db 43, SLUDGE
	db 50, FAINT_ATTACK
	db 50, SLUDGE_BOMB
	db 51, HAZE
	db 55, CRUNCH
	db 60, POISON_JAB
	db 65, NIGHT_SLASH
	db 0 ; no more level-up moves

StaryuEvosAttacks:
	db EVOLVE_LEVEL, 25, STARMIE
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, HARDEN
	db 7, WATER_GUN
	db 13, RAPID_SPIN
	db 19, RECOVER
	db 25, SWIFT
	db 31, BUBBLEBEAM
	db 37, MINIMIZE
	db 43, LIGHT_SCREEN
	db 50, HYDRO_PUMP
	db 0 ; no more level-up moves

StarmieEvosAttacks:
	db EVOLVE_LEVEL, 50, NEBULON
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, RAPID_SPIN
	db 1, RECOVER
	db 1, BUBBLEBEAM
	db 25, CONFUSION
	db 37, CONFUSE_RAY
	db 0 ; no more level-up moves

BasiliskEvosAttacks:
	db 0 ; no more evolutions
	db 25, GLARE
	db 33, SCREECH
	db 43, SLUDGE
	db 50, FAINT_ATTACK
	db 50, SLUDGE_BOMB
	db 51, HAZE
	db 55, CRUNCH
	db 60, POISON_JAB
	db 65, NIGHT_SLASH
	db 75, DRAGONBREATH
	db 75, TOXIC
	db 80, DRAGON_PULSE
	db 85, GUNK_SHOT
	db 90, OUTRAGE
	db 0 ; no more level-up moves

ScytherEvosAttacks:
	db EVOLVE_LEVEL, 25, SCIZOR
	db 0 ; no more evolutions
	db 1, QUICK_ATTACK
	db 1, LEER
	db 6, FOCUS_ENERGY
	db 12, PURSUIT
	db 12, TWINEEDLE
	db 18, FALSE_SWIPE
	db 24, AGILITY
	db 30, WING_ATTACK
	db 36, SLASH
	db 42, SWORDS_DANCE
	db 48, DOUBLE_TEAM
	db 0 ; no more level-up moves

JynxEvosAttacks:
	db EVOLVE_LEVEL, 50, FROSTBITE
	db 0 ; no more evolutions
	db 1, POUND
	db 1, SCRATCH
	db 1, LOVELY_KISS
	db 1, ICY_WIND
	db 21, DOUBLESLAP
	db 25, ICE_PUNCH
	db 25, CONFUSION
	db 35, MEAN_LOOK
	db 41, BODY_SLAM
	db 51, PERISH_SONG
	db 57, BLIZZARD
	db 0 ; no more level-up moves

MegawattEvosAttacks:
	db 0 ; no more evolutions
	db 75, THUNDER_FANG
	db 75, WILD_CHARGE
	db 80, THUNDER
	db 85, THUNDERBOLT
	db 0 ; no more level-up moves

MoonqueenEvosAttacks:
	db 0 ; no more evolutions
	db 50, FAIRY_WIND
	db 75, CONFUSION
	db 75, PLAY_ROUGH
	db 80, PSYCHO_CUT
	db 85, DAZZLE_GLEAM
	db 90, PSYCHIC_M
	db 0 ; no more level-up moves

SoporificEvosAttacks:
	db 0 ; no more evolutions
	db 50, FAIRY_WIND
	db 75, BODY_SLAM
	db 75, PLAY_ROUGH
	db 80, TRI_ATTACK
	db 85, DAZZLE_GLEAM
	db 90, HYPER_BEAM
	db 0 ; no more level-up moves

MatriarchEvosAttacks:
	db 0 ; no more evolutions
	db 23, BODY_SLAM
	db 50, SLUDGE_BOMB
	db 50, DIG
	db 75, FAIRY_WIND
	db 75, DRAIN_KISS
	db 75, EARTH_POWER
	db 80, DAZZLE_GLEAM
	db 85, MAGNITUDE
	db 90, MOONBLAST
	db 0 ; no more level-up moves

MagikarpEvosAttacks:
	db EVOLVE_LEVEL, 25, GYARADOS
	db 0 ; no more evolutions
	db 1, SPLASH
	db 12, AQUA_JET
	db 15, TACKLE
	db 30, FLAIL
	db 0 ; no more level-up moves

GyaradosEvosAttacks:
	db EVOLVE_LEVEL, 50, RAGECARP
	db 0 ; no more evolutions
	db 1, THRASH
	db 20, BITE
	db 25, DRAGONBREATH
	db 25, WING_ATTACK
	db 30, LEER
	db 35, TWISTER
	db 40, HYDRO_PUMP
	db 45, RAIN_DANCE
	db 50, HYPER_BEAM
	db 0 ; no more level-up moves

TyrantEvosAttacks:
	db 0 ; no more evolutions
	db 23, THRASH
	db 50, DIG
	db 75, FAINT_ATTACK
	db 75, EARTH_POWER
	db 80, NIGHT_SLASH
	db 85, MAGNITUDE
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

NosferatuEvosAttacks:
	db 0 ; no more evolutions
	db 30, WING_ATTACK
	db 42, MEAN_LOOK
	db 55, HAZE
	db 75, FAINT_ATTACK
	db 75, NIGHT_SLASH
	db 80, BRAVE_BIRD
	db 85, DARK_PULSE
	db 90, HURRICANE
	db 0 ; no more level-up moves

BelladonnaEvosAttacks:
	db 0 ; no more evolutions
	db 55, SOLARBEAM
	db 75, SLUDGE_BOMB
	db 75, GIGA_DRAIN
	db 80, GUNK_SHOT
	db 85, ENERGY_BALL
	db 90, TOXIC
	db 0 ; no more level-up moves

MawbloomEvosAttacks:
	db 0 ; no more evolutions
	db 75, RAZOR_LEAF
	db 75, FAINT_ATTACK
	db 75, ENERGY_BALL
	db 80, NIGHT_SLASH
	db 85, WOOD_HAMMER
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

CordycepsEvosAttacks:
	db EVOLVE_LEVEL, 75, SPOREKING
	db 0 ; no more evolutions
	db 28, SPORE
	db 37, SLASH
	db 46, GROWTH
	db 50, TWINEEDLE
	db 50, SHADOW_SNEAK
	db 50, X_SCISSOR
	db 55, GIGA_DRAIN
	db 55, SHADOW_CLAW
	db 60, BUG_BUZZ
	db 65, SHADOW_BALL
	db 0 ; no more level-up moves

SporekingEvosAttacks:
	db 0 ; no more evolutions
	db 28, SPORE
	db 37, SLASH
	db 46, GROWTH
	db 50, TWINEEDLE
	db 50, SHADOW_SNEAK
	db 50, X_SCISSOR
	db 55, GIGA_DRAIN
	db 55, SHADOW_CLAW
	db 60, BUG_BUZZ
	db 65, SHADOW_BALL
	db 75, MEGAHORN
	db 80, NIGHT_SHADE
	db 0 ; no more level-up moves

PorygonEvosAttacks:
	db EVOLVE_LEVEL, 25, PORYGON2
	db 0 ; no more evolutions
	db 1, GROWL
	db 1, TACKLE
	db 1, GROWTH
	db 9, AGILITY
	db 12, PSYBEAM
	db 20, RECOVER
	db 24, MEDITATE
	db 32, LOCK_ON
	db 36, TRI_ATTACK
	db 44, ZAP_CANNON
	db 0 ; no more level-up moves

CandlemothEvosAttacks:
	db EVOLVE_LEVEL, 75, PYREMOTH
	db 0 ; no more evolutions
	db 20, POISONPOWDER
	db 25, LEECH_LIFE
	db 28, STUN_SPORE
	db 31, GUST
	db 36, PSYBEAM
	db 42, SLEEP_POWDER
	db 50, FIRE_FANG
	db 50, TWINEEDLE
	db 52, PSYCHIC_M
	db 55, FLAMETHROWER
	db 60, X_SCISSOR
	db 65, FLARE_BLITZ
	db 0 ; no more level-up moves

PyremothEvosAttacks:
	db 0 ; no more evolutions
	db 20, POISONPOWDER
	db 25, LEECH_LIFE
	db 28, STUN_SPORE
	db 31, GUST
	db 36, PSYBEAM
	db 42, SLEEP_POWDER
	db 50, FIRE_FANG
	db 50, TWINEEDLE
	db 52, PSYCHIC_M
	db 55, FLAMETHROWER
	db 60, X_SCISSOR
	db 65, FLARE_BLITZ
	db 75, MEGAHORN
	db 80, FIRE_BLAST
	db 85, BUG_BUZZ
	db 0 ; no more level-up moves

SilkfangEvosAttacks:
	db EVOLVE_LEVEL, 75, WEBWEAVER
	db 0 ; no more evolutions
	db 25, LEECH_LIFE
	db 34, SCRATCH
	db 50, FAINT_ATTACK
	db 50, TWINEEDLE
	db 53, AGILITY
	db 55, CRUNCH
	db 60, X_SCISSOR
	db 63, PSYCHIC_M
	db 65, NIGHT_SLASH
	db 0 ; no more level-up moves

WebweaverEvosAttacks:
	db 0 ; no more evolutions
	db 25, LEECH_LIFE
	db 34, SCRATCH
	db 50, FAINT_ATTACK
	db 50, TWINEEDLE
	db 53, AGILITY
	db 55, CRUNCH
	db 60, X_SCISSOR
	db 63, PSYCHIC_M
	db 65, NIGHT_SLASH
	db 75, MEGAHORN
	db 80, DARK_PULSE
	db 85, BUG_BUZZ
	db 0 ; no more level-up moves

AlleycatEvosAttacks:
	db EVOLVE_LEVEL, 75, KINGPIN
	db 0 ; no more evolutions
	db 20, PAY_DAY
	db 29, FAINT_ATTACK
	db 38, SCREECH
	db 50, CRUNCH
	db 53, SLASH
	db 55, NIGHT_SLASH
	db 60, DARK_PULSE
	db 0 ; no more level-up moves

KingpinEvosAttacks:
	db 0 ; no more evolutions
	db 20, PAY_DAY
	db 29, FAINT_ATTACK
	db 38, SCREECH
	db 50, CRUNCH
	db 53, SLASH
	db 55, NIGHT_SLASH
	db 60, DARK_PULSE
	db 75, TRI_ATTACK
	db 80, HYPER_BEAM
	db 85, BODY_SLAM
	db 0 ; no more level-up moves

MigraineEvosAttacks:
	db EVOLVE_LEVEL, 75, ANEURYSM
	db 0 ; no more evolutions
	db 23, SCREECH
	db 31, PSYCH_UP
	db 50, CONFUSION
	db 50, AQUA_JET
	db 55, ZEN_HEADBUTT
	db 58, HYDRO_PUMP
	db 60, WATERFALL
	db 65, PSYCHO_CUT
	db 0 ; no more level-up moves

AneurysmEvosAttacks:
	db 0 ; no more evolutions
	db 23, SCREECH
	db 31, PSYCH_UP
	db 50, CONFUSION
	db 50, AQUA_JET
	db 55, ZEN_HEADBUTT
	db 58, HYDRO_PUMP
	db 60, WATERFALL
	db 65, PSYCHO_CUT
	db 75, PSYCHIC_M
	db 0 ; no more level-up moves

BerserkerEvosAttacks:
	db EVOLVE_LEVEL, 75, ANGERILLA
	db 0 ; no more evolutions
	db 27, FOCUS_ENERGY
	db 36, SEISMIC_TOSS
	db 45, CROSS_CHOP
	db 50, BRICK_BREAK
	db 54, SCREECH
	db 55, SUBMISSION
	db 60, DRAIN_PUNCH
	db 63, THRASH
	db 65, FOCUS_BLAST
	db 0 ; no more level-up moves

DratiniEvosAttacks:
	db EVOLVE_LEVEL, 25, DRAGONAIR
	db 0 ; no more evolutions
	db 1, WRAP
	db 1, LEER
	db 8, THUNDER_WAVE
	db 15, TWISTER
	db 22, DRAGONBREATH
	db 29, BODY_SLAM
	db 36, AGILITY
	db 43, SAFEGUARD
	db 50, OUTRAGE
	db 57, HYPER_BEAM
	db 0 ; no more level-up moves

DragonairEvosAttacks:
	db EVOLVE_LEVEL, 50, DRAGONITE
	db 0 ; no more evolutions
	db 1, WRAP
	db 1, LEER
	db 1, THUNDER_WAVE
	db 1, TWISTER
	db 22, DRAGONBREATH
	db 29, BODY_SLAM
	db 38, AGILITY
	db 47, SAFEGUARD
	db 56, OUTRAGE
	db 65, HYPER_BEAM
	db 0 ; no more level-up moves

DragoniteEvosAttacks:
	db EVOLVE_LEVEL, 75, WYRMKING
	db 0 ; no more evolutions
	db 1, WRAP
	db 1, LEER
	db 1, THUNDER_WAVE
	db 1, TWISTER
	db 22, DRAGONBREATH
	db 29, BODY_SLAM
	db 38, AGILITY
	db 47, SAFEGUARD
	db 55, WING_ATTACK
	db 61, OUTRAGE
	db 75, HYPER_BEAM
	db 0 ; no more level-up moves

AngerillaEvosAttacks:
	db 0 ; no more evolutions
	db 27, FOCUS_ENERGY
	db 36, SEISMIC_TOSS
	db 45, CROSS_CHOP
	db 50, BRICK_BREAK
	db 54, SCREECH
	db 55, SUBMISSION
	db 60, DRAIN_PUNCH
	db 63, THRASH
	db 65, FOCUS_BLAST
	db 75, FAINT_ATTACK
	db 75, NIGHT_SLASH
	db 80, DARK_PULSE
	db 85, CRUNCH
	db 0 ; no more level-up moves

TitanfistEvosAttacks:
	db 0 ; no more evolutions
	db 25, FORESIGHT
	db 34, VITAL_THROW
	db 43, CROSS_CHOP
	db 52, SCARY_FACE
	db 61, SUBMISSION
	db 75, METAL_CLAW
	db 75, DRAIN_PUNCH
	db 80, IRON_HEAD
	db 85, FOCUS_BLAST
	db 90, FLASH_CANNON
	db 0 ; no more level-up moves

ChikoritaEvosAttacks:
	db EVOLVE_LEVEL, 25, BAYLEEF
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 8, RAZOR_LEAF
	db 12, REFLECT
	db 15, POISONPOWDER
	db 22, SYNTHESIS
	db 29, BODY_SLAM
	db 36, LIGHT_SCREEN
	db 43, SAFEGUARD
	db 50, SOLARBEAM
	db 0 ; no more level-up moves

BayleefEvosAttacks:
	db EVOLVE_LEVEL, 50, MEGANIUM
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, RAZOR_LEAF
	db 1, REFLECT
	db 15, POISONPOWDER
	db 23, SYNTHESIS
	db 31, BODY_SLAM
	db 39, LIGHT_SCREEN
	db 47, SAFEGUARD
	db 55, SOLARBEAM
	db 0 ; no more level-up moves

MeganiumEvosAttacks:
	db EVOLVE_LEVEL, 75, ELDERWOOD
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, RAZOR_LEAF
	db 1, REFLECT
	db 15, POISONPOWDER
	db 23, SYNTHESIS
	db 31, BODY_SLAM
	db 41, LIGHT_SCREEN
	db 51, SAFEGUARD
	db 61, SOLARBEAM
	db 0 ; no more level-up moves

CyndaquilEvosAttacks:
	db EVOLVE_LEVEL, 25, QUILAVA
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, LEER
	db 6, SAND_ATTACK
	db 12, EMBER
	db 19, QUICK_ATTACK
	db 27, FLAME_WHEEL
	db 36, SWIFT
	db 46, FLAMETHROWER
	db 0 ; no more level-up moves

QuilavaEvosAttacks:
	db EVOLVE_LEVEL, 50, TYPHLOSION
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, LEER
	db 1, SAND_ATTACK
	db 12, EMBER
	db 21, QUICK_ATTACK
	db 31, FLAME_WHEEL
	db 42, SWIFT
	db 54, FLAMETHROWER
	db 0 ; no more level-up moves

TyphlosionEvosAttacks:
	db EVOLVE_LEVEL, 75, CALDERA
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, LEER
	db 1, SAND_ATTACK
	db 1, EMBER
	db 21, QUICK_ATTACK
	db 31, FLAME_WHEEL
	db 45, SWIFT
	db 60, FLAMETHROWER
	db 0 ; no more level-up moves

TotodileEvosAttacks:
	db EVOLVE_LEVEL, 25, CROCONAW
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, LEER
	db 7, RAGE
	db 13, WATER_GUN
	db 20, BITE
	db 27, SCARY_FACE
	db 35, SLASH
	db 43, SCREECH
	db 52, HYDRO_PUMP
	db 0 ; no more level-up moves

CroconawEvosAttacks:
	db EVOLVE_LEVEL, 50, FERALIGATR
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, LEER
	db 1, RAGE
	db 13, WATER_GUN
	db 21, BITE
	db 28, SCARY_FACE
	db 37, SLASH
	db 45, SCREECH
	db 55, HYDRO_PUMP
	db 0 ; no more level-up moves

FeraligatrEvosAttacks:
	db EVOLVE_LEVEL, 75, DEATHROLL
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, LEER
	db 1, RAGE
	db 1, WATER_GUN
	db 21, BITE
	db 28, SCARY_FACE
	db 38, SLASH
	db 47, SCREECH
	db 58, HYDRO_PUMP
	db 0 ; no more level-up moves

SentretEvosAttacks:
	db EVOLVE_LEVEL, 25, FURRET
	db 0 ; no more evolutions
	db 1, TACKLE
	db 5, DEFENSE_CURL
	db 11, QUICK_ATTACK
	db 17, SCRATCH
	db 25, BODY_SLAM
	db 33, REST
	db 41, AMNESIA
	db 0 ; no more level-up moves

FurretEvosAttacks:
	db EVOLVE_LEVEL, 50, SENTINEL
	db 0 ; no more evolutions
	db 1, SCRATCH
	db 1, DEFENSE_CURL
	db 1, QUICK_ATTACK
	db 28, BODY_SLAM
	db 38, REST
	db 48, AMNESIA
	db 0 ; no more level-up moves

HoothootEvosAttacks:
	db EVOLVE_LEVEL, 25, NOCTOWL
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 6, FORESIGHT
	db 11, WING_ATTACK
	db 16, HYPNOSIS
	db 22, REFLECT
	db 28, TAKE_DOWN
	db 34, CONFUSION
	db 48, DREAM_EATER
	db 0 ; no more level-up moves

NoctowlEvosAttacks:
	db EVOLVE_LEVEL, 50, PROFESSOWL
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, FORESIGHT
	db 1, WING_ATTACK
	db 16, HYPNOSIS
	db 25, REFLECT
	db 33, TAKE_DOWN
	db 41, CONFUSION
	db 57, DREAM_EATER
	db 0 ; no more level-up moves

OmniscientEvosAttacks:
	db 0 ; no more evolutions
	db 21, PSYBEAM
	db 26, RECOVER
	db 31, FUTURE_SIGHT
	db 38, PSYCHIC_M
	db 45, REFLECT
	db 75, ZEN_HEADBUTT
	db 80, PSYCHO_CUT
	db 85, CONFUSION
	db 0 ; no more level-up moves

MonolithEvosAttacks:
	db 0 ; no more evolutions
	db 21, SELFDESTRUCT
	db 27, HARDEN
	db 34, ROLLOUT
	db 41, EARTHQUAKE
	db 48, EXPLOSION
	db 75, ANCIENTPOWER
	db 80, EARTH_POWER
	db 85, POWER_GEM
	db 90, MAGNITUDE
	db 0 ; no more level-up moves

SpinarakEvosAttacks:
	db EVOLVE_LEVEL, 25, ARIADOS
	db 0 ; no more evolutions
	db 1, POISON_STING
	db 1, STRING_SHOT
	db 6, SCARY_FACE
	db 11, TACKLE
	db 17, NIGHT_SHADE
	db 23, LEECH_LIFE
	db 30, SCRATCH
	db 45, AGILITY
	db 53, PSYCHIC_M
	db 0 ; no more level-up moves

AriadosEvosAttacks:
	db EVOLVE_LEVEL, 50, SILKFANG
	db 0 ; no more evolutions
	db 1, POISON_STING
	db 1, STRING_SHOT
	db 1, SCARY_FACE
	db 1, TACKLE
	db 17, NIGHT_SHADE
	db 25, LEECH_LIFE
	db 34, SCRATCH
	db 53, AGILITY
	db 63, PSYCHIC_M
	db 0 ; no more level-up moves

CrobatEvosAttacks:
	db EVOLVE_LEVEL, 75, NOSFERATU
	db 0 ; no more evolutions
	db 1, SCREECH
	db 1, LEECH_LIFE
	db 1, SUPERSONIC
	db 12, BITE
	db 19, CONFUSE_RAY
	db 30, WING_ATTACK
	db 42, MEAN_LOOK
	db 55, HAZE
	db 0 ; no more level-up moves

AdamantixEvosAttacks:
	db EVOLVE_LEVEL, 75, SKYSCRAPER
	db 0 ; no more evolutions
	db 23, HARDEN
	db 25, METAL_CLAW
	db 25, DIG
	db 27, RAGE
	db 36, SANDSTORM
	db 40, BODY_SLAM
	db 49, CRUNCH
	db 50, BULLET_PUNCH
	db 55, EARTHQUAKE
	db 60, IRON_HEAD
	db 65, EARTH_POWER
	db 0 ; no more level-up moves

SkyscraperEvosAttacks:
	db 0 ; no more evolutions
	db 23, HARDEN
	db 25, METAL_CLAW
	db 25, DIG
	db 27, RAGE
	db 36, SANDSTORM
	db 40, BODY_SLAM
	db 49, CRUNCH
	db 50, BULLET_PUNCH
	db 55, EARTHQUAKE
	db 60, IRON_HEAD
	db 65, EARTH_POWER
	db 75, DRAGONBREATH
	db 75, FLASH_CANNON
	db 80, DRAGON_PULSE
	db 85, OUTRAGE
	db 90, DRAGON_CLAW
	db 0 ; no more level-up moves

PichuEvosAttacks:
	db EVOLVE_LEVEL, 25, PIKACHU
	db 0 ; no more evolutions
	db 1, THUNDERSHOCK
	db 1, CHARM
	db 6, TAIL_WHIP
	db 8, THUNDER_WAVE
	db 11, SWEET_KISS
	db 0 ; no more level-up moves

CleffaEvosAttacks:
	db EVOLVE_LEVEL, 25, CLEFAIRY
	db 0 ; no more evolutions
	db 1, POUND
	db 1, CHARM
	db 4, ENCORE
	db 4, FAIRY_WIND
	db 8, SING
	db 9, DRAIN_KISS
	db 13, SWEET_KISS
	db 0 ; no more level-up moves

IgglybuffEvosAttacks:
	db EVOLVE_LEVEL, 25, JIGGLYPUFF
	db 0 ; no more evolutions
	db 1, SING
	db 1, CHARM
	db 4, DEFENSE_CURL
	db 4, FAIRY_WIND
	db 9, POUND
	db 9, DRAIN_KISS
	db 14, SWEET_KISS
	db 0 ; no more level-up moves

HellhoundEvosAttacks:
	db EVOLVE_LEVEL, 75, GATEHOUND
	db 0 ; no more evolutions
	db 50, EXTREMESPEED
	db 50, FIRE_FANG
	db 50, FAINT_ATTACK
	db 50, FLAMETHROWER
	db 55, CRUNCH
	db 60, FLARE_BLITZ
	db 65, NIGHT_SLASH
	db 0 ; no more level-up moves

GatehoundEvosAttacks:
	db 0 ; no more evolutions
	db 50, EXTREMESPEED
	db 50, FIRE_FANG
	db 50, FAINT_ATTACK
	db 50, FLAMETHROWER
	db 55, CRUNCH
	db 60, FLARE_BLITZ
	db 65, NIGHT_SLASH
	db 75, FIRE_BLAST
	db 80, DARK_PULSE
	db 0 ; no more level-up moves

KitsuneEvosAttacks:
	db EVOLVE_LEVEL, 75, FOXFIRE
	db 0 ; no more evolutions
	db 43, FIRE_SPIN
	db 50, FAIRY_WIND
	db 50, DRAIN_KISS
	db 50, FIRE_FANG
	db 55, PLAY_ROUGH
	db 60, FLAMETHROWER
	db 65, DAZZLE_GLEAM
	db 0 ; no more level-up moves

FoxfireEvosAttacks:
	db 0 ; no more evolutions
	db 43, FIRE_SPIN
	db 50, FAIRY_WIND
	db 50, DRAIN_KISS
	db 50, FIRE_FANG
	db 55, PLAY_ROUGH
	db 60, FLAMETHROWER
	db 65, DAZZLE_GLEAM
	db 75, FIRE_BLAST
	db 80, MOONBLAST
	db 85, FLARE_BLITZ
	db 0 ; no more level-up moves

MareepEvosAttacks:
	db EVOLVE_LEVEL, 25, FLAAFFY
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 9, THUNDERSHOCK
	db 16, THUNDER_WAVE
	db 23, STRING_SHOT
	db 30, LIGHT_SCREEN
	db 37, THUNDER
	db 0 ; no more level-up moves

FlaaffyEvosAttacks:
	db EVOLVE_LEVEL, 50, AMPHAROS
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, THUNDERSHOCK
	db 18, THUNDER_WAVE
	db 27, STRING_SHOT
	db 36, LIGHT_SCREEN
	db 45, THUNDER
	db 0 ; no more level-up moves

AmpharosEvosAttacks:
	db EVOLVE_LEVEL, 75, BLACKSHEEP
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, GROWL
	db 1, THUNDERSHOCK
	db 1, THUNDER_WAVE
	db 27, STRING_SHOT
	db 30, THUNDERPUNCH
	db 42, LIGHT_SCREEN
	db 57, THUNDER
	db 0 ; no more level-up moves

BellossomEvosAttacks:
	db EVOLVE_LEVEL, 75, BELLADONNA
	db 0 ; no more evolutions
	db 1, ABSORB
	db 1, SWEET_SCENT
	db 1, STUN_SPORE
	db 1, PETAL_DANCE
	db 55, SOLARBEAM
	db 0 ; no more level-up moves

MarillEvosAttacks:
	db EVOLVE_LEVEL, 25, AZUMARILL
	db 0 ; no more evolutions
	db 1, TACKLE
	db 3, DEFENSE_CURL
	db 4, FAIRY_WIND
	db 6, TAIL_WHIP
	db 9, DRAIN_KISS
	db 10, WATER_GUN
	db 15, ROLLOUT
	db 21, BUBBLEBEAM
	db 28, DOUBLE_EDGE
	db 36, RAIN_DANCE
	db 0 ; no more level-up moves

AzumarillEvosAttacks:
	db EVOLVE_LEVEL, 50, TIDEBELLY
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, DEFENSE_CURL
	db 1, TAIL_WHIP
	db 1, WATER_GUN
	db 15, ROLLOUT
	db 25, BUBBLEBEAM
	db 25, FAIRY_WIND
	db 36, DOUBLE_EDGE
	db 48, RAIN_DANCE
	db 0 ; no more level-up moves

UnicornEvosAttacks:
	db EVOLVE_LEVEL, 75, DREADSTEED
	db 0 ; no more evolutions
	db 26, FIRE_SPIN
	db 34, TAKE_DOWN
	db 47, AGILITY
	db 50, FAIRY_WIND
	db 50, DRAIN_KISS
	db 50, FIRE_FANG
	db 55, PLAY_ROUGH
	db 60, FLAMETHROWER
	db 61, FIRE_BLAST
	db 65, DAZZLE_GLEAM
	db 0 ; no more level-up moves

DreadsteedEvosAttacks:
	db 0 ; no more evolutions
	db 26, FIRE_SPIN
	db 34, TAKE_DOWN
	db 47, AGILITY
	db 50, FAIRY_WIND
	db 50, DRAIN_KISS
	db 50, FIRE_FANG
	db 55, PLAY_ROUGH
	db 60, FLAMETHROWER
	db 61, FIRE_BLAST
	db 65, DAZZLE_GLEAM
	db 75, FLARE_BLITZ
	db 80, MOONBLAST
	db 0 ; no more level-up moves

HoppipEvosAttacks:
	db EVOLVE_LEVEL, 25, SKIPLOOM
	db 0 ; no more evolutions
	db 1, SPLASH
	db 5, SYNTHESIS
	db 5, TAIL_WHIP
	db 10, TACKLE
	db 12, WING_ATTACK
	db 13, POISONPOWDER
	db 15, STUN_SPORE
	db 17, SLEEP_POWDER
	db 20, LEECH_SEED
	db 25, STRING_SHOT
	db 30, MEGA_DRAIN
	db 0 ; no more level-up moves

SkiploomEvosAttacks:
	db EVOLVE_LEVEL, 50, JUMPLUFF
	db 0 ; no more evolutions
	db 1, SPLASH
	db 1, SYNTHESIS
	db 1, TAIL_WHIP
	db 1, TACKLE
	db 13, POISONPOWDER
	db 15, STUN_SPORE
	db 17, SLEEP_POWDER
	db 22, LEECH_SEED
	db 25, WING_ATTACK
	db 29, STRING_SHOT
	db 36, MEGA_DRAIN
	db 0 ; no more level-up moves

JumpluffEvosAttacks:
	db EVOLVE_LEVEL, 75, DANDELION
	db 0 ; no more evolutions
	db 1, SPLASH
	db 1, SYNTHESIS
	db 1, TAIL_WHIP
	db 1, TACKLE
	db 13, POISONPOWDER
	db 15, STUN_SPORE
	db 17, SLEEP_POWDER
	db 22, LEECH_SEED
	db 33, STRING_SHOT
	db 44, MEGA_DRAIN
	db 50, WING_ATTACK
	db 0 ; no more level-up moves

HellboundEvosAttacks:
	db EVOLVE_LEVEL, 75, PERDITION
	db 0 ; no more evolutions
	db 20, BITE
	db 30, FAINT_ATTACK
	db 41, FLAMETHROWER
	db 50, NIGHT_SLASH
	db 52, CRUNCH
	db 55, FIRE_FANG
	db 60, DARK_PULSE
	db 65, FLARE_BLITZ
	db 0 ; no more level-up moves

PerditionEvosAttacks:
	db 0 ; no more evolutions
	db 20, BITE
	db 30, FAINT_ATTACK
	db 41, FLAMETHROWER
	db 50, NIGHT_SLASH
	db 52, CRUNCH
	db 55, FIRE_FANG
	db 60, DARK_PULSE
	db 65, FLARE_BLITZ
	db 75, FIRE_BLAST
	db 0 ; no more level-up moves

BlacksheepEvosAttacks:
	db 0 ; no more evolutions
	db 27, STRING_SHOT
	db 30, THUNDERPUNCH
	db 42, LIGHT_SCREEN
	db 57, THUNDER
	db 75, FAINT_ATTACK
	db 75, THUNDERBOLT
	db 80, NIGHT_SLASH
	db 85, WILD_CHARGE
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

MagnetronEvosAttacks:
	db EVOLVE_LEVEL, 75, SOLENOID
	db 0 ; no more evolutions
	db 21, THUNDER_WAVE
	db 25, METAL_CLAW
	db 27, LOCK_ON
	db 35, TRI_ATTACK
	db 43, SCREECH
	db 50, THUNDER_FANG
	db 53, ZAP_CANNON
	db 55, BULLET_PUNCH
	db 60, THUNDERBOLT
	db 65, IRON_HEAD
	db 0 ; no more level-up moves

SolenoidEvosAttacks:
	db 0 ; no more evolutions
	db 21, THUNDER_WAVE
	db 25, METAL_CLAW
	db 27, LOCK_ON
	db 35, TRI_ATTACK
	db 43, SCREECH
	db 50, THUNDER_FANG
	db 53, ZAP_CANNON
	db 55, BULLET_PUNCH
	db 60, THUNDERBOLT
	db 65, IRON_HEAD
	db 75, THUNDER
	db 80, FLASH_CANNON
	db 85, WILD_CHARGE
	db 0 ; no more level-up moves

MainframeEvosAttacks:
	db EVOLVE_LEVEL, 75, ALGORITHM
	db 0 ; no more evolutions
	db 20, RECOVER
	db 24, DEFENSE_CURL
	db 32, LOCK_ON
	db 36, TRI_ATTACK
	db 44, ZAP_CANNON
	db 50, METAL_CLAW
	db 50, BODY_SLAM
	db 55, BULLET_PUNCH
	db 60, SLASH
	db 65, IRON_HEAD
	db 0 ; no more level-up moves

AlgorithmEvosAttacks:
	db 0 ; no more evolutions
	db 20, RECOVER
	db 24, DEFENSE_CURL
	db 32, LOCK_ON
	db 36, TRI_ATTACK
	db 44, ZAP_CANNON
	db 50, METAL_CLAW
	db 50, BODY_SLAM
	db 55, BULLET_PUNCH
	db 60, SLASH
	db 65, IRON_HEAD
	db 75, CONFUSION
	db 75, PSYCHO_CUT
	db 80, FLASH_CANNON
	db 85, PSYCHIC_M
	db 90, ZEN_HEADBUTT
	db 0 ; no more level-up moves

ApparitionEvosAttacks:
	db 0 ; no more evolutions
	db 21, NIGHT_SHADE
	db 39, DREAM_EATER
	db 48, DESTINY_BOND
	db 75, FAINT_ATTACK
	db 75, SHADOW_CLAW
	db 80, NIGHT_SLASH
	db 85, SHADOW_BALL
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

BonekeeperEvosAttacks:
	db EVOLVE_LEVEL, 75, OSSUARY
	db 0 ; no more evolutions
	db 21, FOCUS_ENERGY
	db 32, RAGE
	db 39, FALSE_SWIPE
	db 46, THRASH
	db 50, SHADOW_SNEAK
	db 50, DIG
	db 53, BONE_RUSH
	db 55, SHADOW_CLAW
	db 60, EARTHQUAKE
	db 65, SHADOW_BALL
	db 0 ; no more level-up moves

OssuaryEvosAttacks:
	db 0 ; no more evolutions
	db 21, FOCUS_ENERGY
	db 32, RAGE
	db 39, FALSE_SWIPE
	db 46, THRASH
	db 50, SHADOW_SNEAK
	db 50, DIG
	db 53, BONE_RUSH
	db 55, SHADOW_CLAW
	db 60, EARTHQUAKE
	db 65, SHADOW_BALL
	db 75, MAGNITUDE
	db 80, NIGHT_SHADE
	db 85, EARTH_POWER
	db 0 ; no more level-up moves

SludgelordEvosAttacks:
	db EVOLVE_LEVEL, 75, SUPERFUND
	db 0 ; no more evolutions
	db 23, MINIMIZE
	db 31, SCREECH
	db 37, DISABLE
	db 45, SLUDGE
	db 45, ACID_ARMOR
	db 50, FAINT_ATTACK
	db 50, POISON_JAB
	db 55, CRUNCH
	db 60, SLUDGE_BOMB
	db 60, GUNK_SHOT
	db 65, NIGHT_SLASH
	db 0 ; no more level-up moves

SuperfundEvosAttacks:
	db 0 ; no more evolutions
	db 23, MINIMIZE
	db 31, SCREECH
	db 37, DISABLE
	db 45, SLUDGE
	db 45, ACID_ARMOR
	db 50, FAINT_ATTACK
	db 50, POISON_JAB
	db 55, CRUNCH
	db 60, SLUDGE_BOMB
	db 60, GUNK_SHOT
	db 65, NIGHT_SLASH
	db 75, TOXIC
	db 0 ; no more level-up moves

MiasmaEvosAttacks:
	db EVOLVE_LEVEL, 75, PANDEMIC
	db 0 ; no more evolutions
	db 25, SAND_ATTACK
	db 33, HAZE
	db 44, EXPLOSION
	db 50, SLUDGE_BOMB
	db 50, SHADOW_SNEAK
	db 50, POISON_JAB
	db 51, DESTINY_BOND
	db 55, SHADOW_CLAW
	db 60, GUNK_SHOT
	db 65, SHADOW_BALL
	db 0 ; no more level-up moves

PandemicEvosAttacks:
	db 0 ; no more evolutions
	db 25, SAND_ATTACK
	db 33, HAZE
	db 44, EXPLOSION
	db 50, SLUDGE_BOMB
	db 50, SHADOW_SNEAK
	db 50, POISON_JAB
	db 51, DESTINY_BOND
	db 55, SHADOW_CLAW
	db 60, GUNK_SHOT
	db 65, SHADOW_BALL
	db 75, FAINT_ATTACK
	db 75, TOXIC
	db 80, NIGHT_SLASH
	db 85, DARK_PULSE
	db 90, CRUNCH
	db 0 ; no more level-up moves

WarhornEvosAttacks:
	db EVOLVE_LEVEL, 75, BEHEMOTH
	db 0 ; no more evolutions
	db 25, ROCK_SLIDE
	db 31, SCARY_FACE
	db 37, HORN_DRILL
	db 50, DIG
	db 54, TAKE_DOWN
	db 55, ANCIENTPOWER
	db 60, EARTH_POWER
	db 65, EARTHQUAKE
	db 65, POWER_GEM
	db 0 ; no more level-up moves

BehemothEvosAttacks:
	db 0 ; no more evolutions
	db 25, ROCK_SLIDE
	db 31, SCARY_FACE
	db 37, HORN_DRILL
	db 50, DIG
	db 54, TAKE_DOWN
	db 55, ANCIENTPOWER
	db 60, EARTH_POWER
	db 65, EARTHQUAKE
	db 65, POWER_GEM
	db 75, METAL_CLAW
	db 75, MAGNITUDE
	db 80, IRON_HEAD
	db 85, FLASH_CANNON
	db 90, BULLET_PUNCH
	db 0 ; no more level-up moves

CleaverEvosAttacks:
	db EVOLVE_LEVEL, 75, HEADSMAN
	db 0 ; no more evolutions
	db 24, AGILITY
	db 25, TWINEEDLE
	db 30, METAL_CLAW
	db 36, SLASH
	db 42, SWORDS_DANCE
	db 48, DOUBLE_TEAM
	db 50, X_SCISSOR
	db 55, BULLET_PUNCH
	db 60, BUG_BUZZ
	db 65, IRON_HEAD
	db 0 ; no more level-up moves

HeadsmanEvosAttacks:
	db 0 ; no more evolutions
	db 24, AGILITY
	db 25, TWINEEDLE
	db 30, METAL_CLAW
	db 36, SLASH
	db 42, SWORDS_DANCE
	db 48, DOUBLE_TEAM
	db 50, X_SCISSOR
	db 55, BULLET_PUNCH
	db 60, BUG_BUZZ
	db 65, IRON_HEAD
	db 75, MEGAHORN
	db 80, FLASH_CANNON
	db 0 ; no more level-up moves

SteelixEvosAttacks:
	db EVOLVE_LEVEL, 50, ADAMANTIX
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, SCREECH
	db 10, BIND
	db 14, ROCK_THROW
	db 23, HARDEN
	db 25, METAL_CLAW
	db 25, DIG
	db 27, RAGE
	db 36, SANDSTORM
	db 40, BODY_SLAM
	db 49, CRUNCH
	db 0 ; no more level-up moves

CthuspawnEvosAttacks:
	db EVOLVE_LEVEL, 75, CTHULUDON
	db 0 ; no more evolutions
	db 25, BUBBLEBEAM
	db 30, WRAP
	db 38, BARRIER
	db 47, SCREECH
	db 50, FAINT_ATTACK
	db 50, SLUDGE_BOMB
	db 50, CRUNCH
	db 55, HYDRO_PUMP
	db 55, POISON_JAB
	db 60, NIGHT_SLASH
	db 65, GUNK_SHOT
	db 0 ; no more level-up moves

CthuludonEvosAttacks:
	db 0 ; no more evolutions
	db 25, BUBBLEBEAM
	db 30, WRAP
	db 38, BARRIER
	db 47, SCREECH
	db 50, FAINT_ATTACK
	db 50, SLUDGE_BOMB
	db 50, CRUNCH
	db 55, HYDRO_PUMP
	db 55, POISON_JAB
	db 60, NIGHT_SLASH
	db 65, GUNK_SHOT
	db 75, DARK_PULSE
	db 80, TOXIC
	db 0 ; no more level-up moves

PoliwraithEvosAttacks:
	db 0 ; no more evolutions
	db 51, LOCK_ON
	db 75, AQUA_JET
	db 75, SHADOW_SNEAK
	db 75, AQUA_TAIL
	db 80, SHADOW_BALL
	db 85, HYDRO_PUMP
	db 90, NIGHT_SHADE
	db 0 ; no more level-up moves

ScizorEvosAttacks:
	db EVOLVE_LEVEL, 50, CLEAVER
	db 0 ; no more evolutions
	db 1, QUICK_ATTACK
	db 1, LEER
	db 6, FOCUS_ENERGY
	db 12, PURSUIT
	db 18, FALSE_SWIPE
	db 24, AGILITY
	db 25, TWINEEDLE
	db 30, METAL_CLAW
	db 36, SLASH
	db 42, SWORDS_DANCE
	db 48, DOUBLE_TEAM
	db 0 ; no more level-up moves

AmnesiacEvosAttacks:
	db EVOLVE_LEVEL, 75, OBLIVION
	db 0 ; no more evolutions
	db 20, CONFUSION
	db 29, DISABLE
	db 34, HEADBUTT
	db 37, WITHDRAW
	db 46, AMNESIA
	db 50, AQUA_JET
	db 50, WATERFALL
	db 54, PSYCHIC_M
	db 55, ZEN_HEADBUTT
	db 60, AQUA_TAIL
	db 65, PSYCHO_CUT
	db 0 ; no more level-up moves

OblivionEvosAttacks:
	db 0 ; no more evolutions
	db 20, CONFUSION
	db 29, DISABLE
	db 34, HEADBUTT
	db 37, WITHDRAW
	db 46, AMNESIA
	db 50, AQUA_JET
	db 50, WATERFALL
	db 54, PSYCHIC_M
	db 55, ZEN_HEADBUTT
	db 60, AQUA_TAIL
	db 65, PSYCHO_CUT
	db 75, FAINT_ATTACK
	db 75, NIGHT_SLASH
	db 80, DARK_PULSE
	db 85, CRUNCH
	db 0 ; no more level-up moves

TuskdriftEvosAttacks:
	db EVOLVE_LEVEL, 75, FROSTSIREN
	db 0 ; no more evolutions
	db 21, REST
	db 25, AQUA_JET
	db 32, TAKE_DOWN
	db 43, ICE_BEAM
	db 50, WATERFALL
	db 55, ICE_FANG
	db 60, SAFEGUARD
	db 60, AQUA_TAIL
	db 65, ICE_SHARD
	db 0 ; no more level-up moves

FrostsirenEvosAttacks:
	db 0 ; no more evolutions
	db 21, REST
	db 25, AQUA_JET
	db 32, TAKE_DOWN
	db 43, ICE_BEAM
	db 50, WATERFALL
	db 55, ICE_FANG
	db 60, SAFEGUARD
	db 60, AQUA_TAIL
	db 65, ICE_SHARD
	db 75, FAIRY_WIND
	db 75, DRAIN_KISS
	db 75, BLIZZARD
	db 80, DAZZLE_GLEAM
	db 85, MOONBLAST
	db 90, PLAY_ROUGH
	db 0 ; no more level-up moves

CryoclamEvosAttacks:
	db EVOLVE_LEVEL, 75, ABYSSHELL
	db 0 ; no more evolutions
	db 25, AQUA_JET
	db 33, SPIKES
	db 41, DOUBLESLAP
	db 50, ICE_FANG
	db 50, WATERFALL
	db 55, ICE_SHARD
	db 60, AQUA_TAIL
	db 65, ICE_BEAM
	db 0 ; no more level-up moves

AbysshellEvosAttacks:
	db 0 ; no more evolutions
	db 25, AQUA_JET
	db 33, SPIKES
	db 41, DOUBLESLAP
	db 50, ICE_FANG
	db 50, WATERFALL
	db 55, ICE_SHARD
	db 60, AQUA_TAIL
	db 65, ICE_BEAM
	db 75, FAINT_ATTACK
	db 75, BLIZZARD
	db 80, NIGHT_SLASH
	db 85, DARK_PULSE
	db 90, CRUNCH
	db 0 ; no more level-up moves

CarapaceEvosAttacks:
	db EVOLVE_LEVEL, 75, CARCINIZE
	db 0 ; no more evolutions
	db 23, HEADBUTT
	db 27, GUILLOTINE
	db 38, PROTECT
	db 49, CRABHAMMER
	db 50, ROCK_SLIDE
	db 50, AQUA_JET
	db 55, ANCIENTPOWER
	db 60, WATERFALL
	db 65, POWER_GEM
	db 0 ; no more level-up moves

SwinubEvosAttacks:
	db EVOLVE_LEVEL, 25, PILOSWINE
	db 0 ; no more evolutions
	db 1, TACKLE
	db 10, ICY_WIND
	db 12, DIG
	db 19, ENDURE
	db 28, TAKE_DOWN
	db 37, MIST
	db 46, BLIZZARD
	db 55, AMNESIA
	db 0 ; no more level-up moves

PiloswineEvosAttacks:
	db EVOLVE_LEVEL, 50, MAMMOTH
	db 0 ; no more evolutions
	db 1, TACKLE
	db 1, ICY_WIND
	db 1, ENDURE
	db 25, DIG
	db 28, TAKE_DOWN
	db 42, MIST
	db 56, BLIZZARD
	db 70, AMNESIA
	db 0 ; no more level-up moves

CarcinizeEvosAttacks:
	db 0 ; no more evolutions
	db 23, HEADBUTT
	db 27, GUILLOTINE
	db 38, PROTECT
	db 49, CRABHAMMER
	db 50, ROCK_SLIDE
	db 50, AQUA_JET
	db 55, ANCIENTPOWER
	db 60, WATERFALL
	db 65, POWER_GEM
	db 75, METAL_CLAW
	db 75, HYDRO_PUMP
	db 80, IRON_HEAD
	db 85, AQUA_TAIL
	db 90, FLASH_CANNON
	db 0 ; no more level-up moves

NebulonEvosAttacks:
	db EVOLVE_LEVEL, 75, SUPERNOVA
	db 0 ; no more evolutions
	db 25, CONFUSION
	db 37, CONFUSE_RAY
	db 50, AQUA_JET
	db 50, WATERFALL
	db 55, ZEN_HEADBUTT
	db 60, AQUA_TAIL
	db 65, PSYCHO_CUT
	db 0 ; no more level-up moves

SupernovaEvosAttacks:
	db 0 ; no more evolutions
	db 25, CONFUSION
	db 37, CONFUSE_RAY
	db 50, AQUA_JET
	db 50, WATERFALL
	db 55, ZEN_HEADBUTT
	db 60, AQUA_TAIL
	db 65, PSYCHO_CUT
	db 75, FIRE_FANG
	db 75, PSYCHIC_M
	db 80, FLARE_BLITZ
	db 85, FIRE_BLAST
	db 90, FLAMETHROWER
	db 0 ; no more level-up moves

MaeldraEvosAttacks:
	db 0 ; no more evolutions
	db 29, TWISTER
	db 40, AGILITY
	db 51, HYDRO_PUMP
	db 75, WATERFALL
	db 80, DRAGON_CLAW
	db 85, AQUA_TAIL
	db 90, DRAGON_PULSE
	db 0 ; no more level-up moves

RagecarpEvosAttacks:
	db EVOLVE_LEVEL, 75, WORLDEATER
	db 0 ; no more evolutions
	db 20, BITE
	db 25, DRAGONBREATH
	db 25, WING_ATTACK
	db 30, LEER
	db 35, TWISTER
	db 40, HYDRO_PUMP
	db 45, RAIN_DANCE
	db 50, HYPER_BEAM
	db 50, AQUA_JET
	db 55, DRAGON_CLAW
	db 60, WATERFALL
	db 65, DRAGON_PULSE
	db 0 ; no more level-up moves

WorldeaterEvosAttacks:
	db 0 ; no more evolutions
	db 20, BITE
	db 25, DRAGONBREATH
	db 25, WING_ATTACK
	db 30, LEER
	db 35, TWISTER
	db 40, HYDRO_PUMP
	db 45, RAIN_DANCE
	db 50, HYPER_BEAM
	db 50, AQUA_JET
	db 55, DRAGON_CLAW
	db 60, WATERFALL
	db 65, DRAGON_PULSE
	db 75, AQUA_TAIL
	db 80, OUTRAGE
	db 0 ; no more level-up moves

HoundourEvosAttacks:
	db EVOLVE_LEVEL, 25, HOUNDOOM
	db 0 ; no more evolutions
	db 1, LEER
	db 1, EMBER
	db 7, ROAR
	db 13, SLUDGE
	db 20, BITE
	db 27, FAINT_ATTACK
	db 35, FLAMETHROWER
	db 43, CRUNCH
	db 0 ; no more level-up moves

HoundoomEvosAttacks:
	db EVOLVE_LEVEL, 50, HELLBOUND
	db 0 ; no more evolutions
	db 1, LEER
	db 1, EMBER
	db 7, ROAR
	db 13, SLUDGE
	db 20, BITE
	db 30, FAINT_ATTACK
	db 41, FLAMETHROWER
	db 52, CRUNCH
	db 0 ; no more level-up moves

KingdraEvosAttacks:
	db EVOLVE_LEVEL, 75, MAELDRA
	db 0 ; no more evolutions
	db 1, WATER_GUN
	db 1, SAND_ATTACK
	db 1, LEER
	db 29, TWISTER
	db 40, AGILITY
	db 51, HYDRO_PUMP
	db 0 ; no more level-up moves

TidebellyEvosAttacks:
	db EVOLVE_LEVEL, 75, BEACHBALL
	db 0 ; no more evolutions
	db 25, BUBBLEBEAM
	db 25, FAIRY_WIND
	db 36, DOUBLE_EDGE
	db 48, RAIN_DANCE
	db 50, AQUA_JET
	db 55, DRAIN_KISS
	db 60, WATERFALL
	db 65, PLAY_ROUGH
	db 0 ; no more level-up moves

BeachballEvosAttacks:
	db 0 ; no more evolutions
	db 25, BUBBLEBEAM
	db 25, FAIRY_WIND
	db 36, DOUBLE_EDGE
	db 48, RAIN_DANCE
	db 50, AQUA_JET
	db 55, DRAIN_KISS
	db 60, WATERFALL
	db 65, PLAY_ROUGH
	db 75, HYDRO_PUMP
	db 80, MOONBLAST
	db 85, AQUA_TAIL
	db 90, DAZZLE_GLEAM
	db 0 ; no more level-up moves

Porygon2EvosAttacks:
	db EVOLVE_LEVEL, 50, MAINFRAME
	db 0 ; no more evolutions
	db 1, GROWL
	db 1, TACKLE
	db 1, GROWTH
	db 9, AGILITY
	db 12, PSYBEAM
	db 20, RECOVER
	db 24, DEFENSE_CURL
	db 32, LOCK_ON
	db 36, TRI_ATTACK
	db 44, ZAP_CANNON
	db 0 ; no more level-up moves

NarcoleptEvosAttacks:
	db EVOLVE_LEVEL, 75, SANDMAN
	db 0 ; no more evolutions
	db 25, HEADBUTT
	db 33, TOXIC
	db 40, MEDITATE
	db 49, PSYCHIC_M
	db 50, CONFUSION
	db 55, PSYCH_UP
	db 55, ZEN_HEADBUTT
	db 60, FUTURE_SIGHT
	db 60, PSYCHO_CUT
	db 0 ; no more level-up moves

SandmanEvosAttacks:
	db 0 ; no more evolutions
	db 25, HEADBUTT
	db 33, TOXIC
	db 40, MEDITATE
	db 49, PSYCHIC_M
	db 50, CONFUSION
	db 55, PSYCH_UP
	db 55, ZEN_HEADBUTT
	db 60, FUTURE_SIGHT
	db 60, PSYCHO_CUT
	db 75, FAINT_ATTACK
	db 75, NIGHT_SLASH
	db 80, DARK_PULSE
	db 85, CRUNCH
	db 0 ; no more level-up moves

PlaceboEvosAttacks:
	db EVOLVE_LEVEL, 75, HOSPICE
	db 0 ; no more evolutions
	db 23, SING
	db 25, FAIRY_WIND
	db 28, SLASH
	db 33, DEFENSE_CURL
	db 40, LIGHT_SCREEN
	db 47, DOUBLE_EDGE
	db 50, DRAIN_KISS
	db 55, PLAY_ROUGH
	db 60, DAZZLE_GLEAM
	db 65, MOONBLAST
	db 0 ; no more level-up moves

HospiceEvosAttacks:
	db 0 ; no more evolutions
	db 23, SING
	db 25, FAIRY_WIND
	db 28, SLASH
	db 33, DEFENSE_CURL
	db 40, LIGHT_SCREEN
	db 47, DOUBLE_EDGE
	db 50, DRAIN_KISS
	db 55, PLAY_ROUGH
	db 60, DAZZLE_GLEAM
	db 65, MOONBLAST
	db 75, SHADOW_SNEAK
	db 75, SHADOW_BALL
	db 80, NIGHT_SHADE
	db 85, SHADOW_CLAW
	db 0 ; no more level-up moves

SmoochumEvosAttacks:
	db EVOLVE_LEVEL, 25, JYNX
	db 0 ; no more evolutions
	db 1, POUND
	db 1, SCRATCH
	db 9, SWEET_KISS
	db 13, ICY_WIND
	db 21, CONFUSION
	db 25, SING
	db 33, MEAN_LOOK
	db 37, PSYCHIC_M
	db 45, PERISH_SONG
	db 49, BLIZZARD
	db 0 ; no more level-up moves

MammothEvosAttacks:
	db EVOLVE_LEVEL, 75, ICEAGE
	db 0 ; no more evolutions
	db 25, DIG
	db 28, TAKE_DOWN
	db 42, MIST
	db 50, ICE_FANG
	db 55, EARTHQUAKE
	db 56, BLIZZARD
	db 60, ICE_SHARD
	db 65, EARTH_POWER
	db 70, AMNESIA
	db 0 ; no more level-up moves

IceageEvosAttacks:
	db 0 ; no more evolutions
	db 25, DIG
	db 28, TAKE_DOWN
	db 42, MIST
	db 50, ICE_FANG
	db 55, EARTHQUAKE
	db 56, BLIZZARD
	db 60, ICE_SHARD
	db 65, EARTH_POWER
	db 70, AMNESIA
	db 75, ICE_BEAM
	db 80, MAGNITUDE
	db 0 ; no more level-up moves

FrostbiteEvosAttacks:
	db EVOLVE_LEVEL, 75, RIMEQUEEN
	db 0 ; no more evolutions
	db 21, DOUBLESLAP
	db 25, ICE_PUNCH
	db 25, CONFUSION
	db 35, MEAN_LOOK
	db 41, BODY_SLAM
	db 50, ICE_FANG
	db 51, PERISH_SONG
	db 55, ZEN_HEADBUTT
	db 57, BLIZZARD
	db 60, ICE_SHARD
	db 65, PSYCHO_CUT
	db 0 ; no more level-up moves

BlisseyEvosAttacks:
	db EVOLVE_LEVEL, 50, PLACEBO
	db 0 ; no more evolutions
	db 1, POUND
	db 4, GROWL
	db 7, TAIL_WHIP
	db 10, SOFTBOILED
	db 13, DOUBLESLAP
	db 18, MINIMIZE
	db 23, SING
	db 25, FAIRY_WIND
	db 28, SLASH
	db 33, DEFENSE_CURL
	db 40, LIGHT_SCREEN
	db 47, DOUBLE_EDGE
	db 0 ; no more level-up moves

RimequeenEvosAttacks:
	db 0 ; no more evolutions
	db 21, DOUBLESLAP
	db 25, ICE_PUNCH
	db 25, CONFUSION
	db 35, MEAN_LOOK
	db 41, BODY_SLAM
	db 50, ICE_FANG
	db 51, PERISH_SONG
	db 55, ZEN_HEADBUTT
	db 57, BLIZZARD
	db 60, ICE_SHARD
	db 65, PSYCHO_CUT
	db 75, FAIRY_WIND
	db 75, DRAIN_KISS
	db 75, ICE_BEAM
	db 80, DAZZLE_GLEAM
	db 85, MOONBLAST
	db 90, PLAY_ROUGH
	db 0 ; no more level-up moves

WyrmkingEvosAttacks:
	db 0 ; no more evolutions
	db 22, DRAGONBREATH
	db 29, BODY_SLAM
	db 38, AGILITY
	db 47, SAFEGUARD
	db 55, WING_ATTACK
	db 61, OUTRAGE
	db 75, HYPER_BEAM
	db 75, DRAGON_PULSE
	db 80, BRAVE_BIRD
	db 85, DRAGON_CLAW
	db 90, HURRICANE
	db 0 ; no more level-up moves

TyphoneusEvosAttacks:
	db 0 ; no more evolutions
	db 22, ROCK_SLIDE
	db 29, THRASH
	db 38, SCARY_FACE
	db 47, CRUNCH
	db 61, EARTHQUAKE
	db 75, HYPER_BEAM
	db 75, POWER_GEM
	db 80, NIGHT_SLASH
	db 85, STONE_EDGE
	db 90, DARK_PULSE
	db 0 ; no more level-up moves

LarvitarEvosAttacks:
	db EVOLVE_LEVEL, 25, PUPITAR
	db 0 ; no more evolutions
	db 1, BITE
	db 1, LEER
	db 8, SANDSTORM
	db 15, SCREECH
	db 22, ROCK_SLIDE
	db 29, THRASH
	db 36, SCARY_FACE
	db 43, CRUNCH
	db 50, EARTHQUAKE
	db 57, HYPER_BEAM
	db 0 ; no more level-up moves

PupitarEvosAttacks:
	db EVOLVE_LEVEL, 50, TYRANITAR
	db 0 ; no more evolutions
	db 1, BITE
	db 1, LEER
	db 1, SANDSTORM
	db 1, SCREECH
	db 22, ROCK_SLIDE
	db 29, THRASH
	db 38, SCARY_FACE
	db 47, CRUNCH
	db 56, EARTHQUAKE
	db 65, HYPER_BEAM
	db 0 ; no more level-up moves

TyranitarEvosAttacks:
	db EVOLVE_LEVEL, 75, TYPHONEUS
	db 0 ; no more evolutions
	db 1, BITE
	db 1, LEER
	db 1, SANDSTORM
	db 1, SCREECH
	db 22, ROCK_SLIDE
	db 29, THRASH
	db 38, SCARY_FACE
	db 47, CRUNCH
	db 61, EARTHQUAKE
	db 75, HYPER_BEAM
	db 0 ; no more level-up moves
