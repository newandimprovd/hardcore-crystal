; item ids
; indexes for:
; - ItemNames (see data/items/names.asm)
; - ItemDescriptions (see data/items/descriptions.asm)
; - ItemAttributes (see data/items/attributes.asm)
; - ItemEffects (see engine/items/item_effects.asm)
	const_def
	const NO_ITEM
	const MASTER_BALL
	const ULTRA_BALL
	const GREAT_BALL
	const POKE_BALL
	const TOWN_MAP
	const MOON_STONE
	const ANTIDOTE
	const BURN_HEAL
	const ICE_HEAL
	const AWAKENING
	const PARLYZ_HEAL
	const FULL_RESTORE
	const MAX_POTION
	const HYPER_POTION
	const SUPER_POTION
	const POTION
	const ESCAPE_ROPE
	const REPEL
	const MAX_ELIXER
	const HP_UP
	const PROTEIN
	const IRON
	const CARBOS
	const LUCKY_PUNCH
	const CALCIUM
	const RARE_CANDY
	const X_ACCURACY
	const METAL_POWDER
	const NUGGET
	const FULL_HEAL
	const REVIVE
	const MAX_REVIVE
	const GUARD_SPEC
	const SUPER_REPEL
	const MAX_REPEL
	const DIRE_HIT
	const FRESH_WATER
	const SODA_POP
	const LEMONADE
	const X_ATTACK
	const X_DEFEND
	const X_SPEED
	const X_SPECIAL
	const ITEMFINDER
	const EXP_SHARE
	const PP_UP
	const ETHER
	const MAX_ETHER
	const ELIXER
	const S_S_TICKET
	const MYSTERY_EGG
	const MOOMOO_MILK
	const PSNCUREBERRY
	const SOFT_SAND
	const SHARP_BEAK
	const PRZCUREBERRY
	const BURNT_BERRY
	const ICE_BERRY
	const POISON_BARB
	const KINGS_ROCK
	const BITTER_BERRY
	const MINT_BERRY
	const RED_APRICORN
	const TINYMUSHROOM
	const BIG_MUSHROOM
	const SILVERPOWDER
	const BLU_APRICORN
	const YLW_APRICORN
	const GRN_APRICORN
	const CLEANSE_TAG
	const MYSTIC_WATER
	const TWISTEDSPOON
	const WHT_APRICORN
	const BLACKBELT_I
	const BLK_APRICORN
	const PNK_APRICORN
	const BLACKGLASSES
	const PINK_BOW
	const STICK
	const NEVERMELTICE
	const MAGNET
	const MIRACLEBERRY
	const PEARL
	const BIG_PEARL
	const EVERSTONE
	const SPELL_TAG
	const RAGECANDYBAR
	const MIRACLE_SEED
	const THICK_CLUB
	const FOCUS_BAND
	const ENERGYPOWDER
	const ENERGY_ROOT
	const HEAL_POWDER
	const HARD_STONE
	const LUCKY_EGG
	const STARDUST
	const STAR_PIECE
	const PASS
	const CORKBOARD
	const CHAINSAW
	const JET_SKI
	const CHARCOAL
	const BERRY_JUICE
	const CROWBAR
	const FLASHLIGHT
	const METAL_COAT
	const OUTBOARD
	const GRAPPLE_HOOK
	const SLEDGEHAMMER
	const BASEBALL_BAT
	const MYSTERYBERRY
	const DRAGON_SCALE
	const BERSERK_GENE
	const SHOVEL
	const GETAWAY_CAR
	const TRUMPET
	const HEAVY_BALL
	const LEVEL_BALL
	const LURE_BALL
	const FAST_BALL
	const LIGHT_BALL
	const FRIEND_BALL
	const MOON_BALL
	const LOVE_BALL
	const POLKADOT_BOW
	const BERRY
	const GOLD_BERRY
	const PARK_BALL
	const LEFTOVERS
	const QUICK_CLAW
	const SCOPE_LENS
	const AMULET_COIN
	const BRIGHTPOWDER
	const SMOKE_BALL
	const ITEM_B3
	const ITEM_BE
DEF NUM_ITEMS EQU const_value - 1

DEF __tmhm_value__ = 1

MACRO add_tmnum
	DEF \1_TMNUM EQU __tmhm_value__
	DEF __tmhm_value__ += 1
ENDM

MACRO add_tm
; Defines three constants:
; - TM_\1: the item id, starting at $bf
; - \1_TMNUM: the learnable TM/HM flag, starting at 1
; - TM##_MOVE: alias for the move id, equal to the value of \1
	const TM_\1
	DEF TM{02d:__tmhm_value__}_MOVE = \1
	add_tmnum \1
ENDM

; see data/moves/tmhm_moves.asm for moves
DEF TM01 EQU const_value
	add_tm DYNAMICPUNCH
	add_tm HEADBUTT
	add_tm CURSE
	add_tm ROLLOUT
	const ITEM_C3
	add_tm ROAR
	add_tm TOXIC
	add_tm ZAP_CANNON
	add_tm ROCK_SMASH
	add_tm PSYCH_UP
	add_tm HIDDEN_POWER
	add_tm SUNNY_DAY
	add_tm SWEET_SCENT
	add_tm SNORE
	add_tm BLIZZARD
	add_tm HYPER_BEAM
	add_tm ICY_WIND
	add_tm PROTECT
	add_tm RAIN_DANCE
	add_tm GIGA_DRAIN
	add_tm ENDURE
	add_tm FRUSTRATION
	add_tm SOLARBEAM
	add_tm IRON_TAIL
	add_tm DRAGONBREATH
	add_tm THUNDER
	add_tm EARTHQUAKE
	add_tm RETURN
	add_tm DIG
	const ITEM_DC
	add_tm PSYCHIC_M
	add_tm SHADOW_BALL
	add_tm MUD_SLAP
	add_tm DOUBLE_TEAM
	add_tm ICE_PUNCH
	add_tm SWAGGER
	add_tm SLEEP_TALK
	add_tm SLUDGE_BOMB
	add_tm SANDSTORM
	add_tm FIRE_BLAST
	add_tm SWIFT
	add_tm DEFENSE_CURL
	add_tm THUNDERPUNCH
	add_tm DREAM_EATER
	add_tm DETECT
	add_tm REST
	add_tm ATTRACT
	add_tm THIEF
	add_tm STEEL_WING
	add_tm FIRE_PUNCH
	add_tm FURY_CUTTER
	add_tm NIGHTMARE
DEF NUM_TMS EQU __tmhm_value__ - 1

MACRO add_hm
; Defines three constants:
; - HM_\1: the item id, starting at $f3
; - \1_TMNUM: the learnable TM/HM flag, starting at 51
; - HM##_MOVE: alias for the move id, equal to the value of \1
	const HM_\1
	DEF HM_VALUE = __tmhm_value__ - NUM_TMS
	DEF HM{02d:HM_VALUE}_MOVE = \1
	add_tmnum \1
ENDM

DEF HM01 EQU const_value
	add_hm CUT
	add_hm FLY
	add_hm SURF
	add_hm STRENGTH
	add_hm FLASH
	add_hm WHIRLPOOL
	add_hm WATERFALL
DEF NUM_HMS EQU __tmhm_value__ - NUM_TMS - 1

MACRO add_mt
; Defines two constants:
; - \1_TMNUM: the learnable TM/HM flag, starting at 58
; - MT##_MOVE: alias for the move id, equal to the value of \1
	DEF MT_VALUE = __tmhm_value__ - NUM_TMS - NUM_HMS
	DEF MT{02d:MT_VALUE}_MOVE = \1
	add_tmnum \1
ENDM

DEF MT01 EQU const_value
	add_mt FLAMETHROWER
	add_mt THUNDERBOLT
	add_mt ICE_BEAM
DEF NUM_TUTORS = __tmhm_value__ - NUM_TMS - NUM_HMS - 1

DEF NUM_TM_HM_TUTOR EQU NUM_TMS + NUM_HMS + NUM_TUTORS


DEF USE_SCRIPT_VAR EQU $00
DEF ITEM_FROM_MEM  EQU $ff

; leftovers from red
DEF SAFARI_BALL    EQU $08 ; MOON_STONE
DEF MOON_STONE_RED EQU $0a ; BURN_HEAL
DEF FULL_HEAL_RED  EQU $34 ; X_SPEED
