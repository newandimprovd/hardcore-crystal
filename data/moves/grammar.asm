; Used by GetMoveGrammar (see engine/battle/used_move_text.asm)
; Each move is given an identifier for what usedmovetext to use (0-4).
; Made redundant in English localization, where all are just "[mon]<LINE>used [move]!"

MoveGrammar:
; 0: originally "[mon]は<LINE>[move]を　つかった！" ("[mon]<LINE>used [move]!")
	db SWORDS_DANCE
	db GROWTH
	db STRENGTH
	db HARDEN
	db MINIMIZE
	db FLASH_CANNON
	db WITHDRAW
	db DEFENSE_CURL
	db ENERGY_BALL
	db AQUA_JET
	db ICE_FANG
	db FLASH
	db SPLASH
	db ACID_ARMOR
	db BONEMERANG
	db REST
	db X_SCISSOR
	db SUBSTITUTE
	db SHADOW_SNEAK
	db SNORE
	db PROTECT
	db SPIKES
	db ENDURE
	db ROLLOUT
	db SWAGGER
	db SLEEP_TALK
	db HIDDEN_POWER
	db PSYCH_UP
	db EXTREMESPEED
	db 0 ; end set

; 1: originally "[mon]は<LINE>[move]した！" ("[mon]<LINE>did [move]!")
	db RECOVER
	db TELEPORT
	db BIDE
	db SELFDESTRUCT
	db AMNESIA
	db FLAIL
	db 0 ; end set

; 2: originally "[mon]は<LINE>[move]を　した！" ("[mon]<LINE>did [move]!")
	db MEDITATE
	db AGILITY
	db MIMIC
	db DOUBLE_TEAM
	db POISON_JAB
	db TRANSFORM
	db STRUGGLE
	db SCARY_FACE
	db 0 ; end set

; 3: originally "[mon]の<LINE>[move]　こうげき！" ("[mon]'s<LINE>[move] attack!")
	db POUND
	db SCRATCH
	db FAIRY_WIND
	db WING_ATTACK
	db FLY
	db BIND
	db FIRE_FANG
	db WOOD_HAMMER
	db WRAP
	db THRASH
	db TAIL_WHIP
	db LEER
	db BITE
	db GROWL
	db ROAR
	db SING
	db BRAVE_BIRD
	db ABSORB
	db STRING_SHOT
	db EARTHQUAKE
	db FISSURE
	db DIG
	db TOXIC
	db SCREECH
	db METRONOME
	db THUNDER_FANG
	db CLAMP
	db BULLET_PUNCH
	db PSYCHO_CUT
	db STONE_EDGE
	db SLASH
	db BUG_BUZZ
	db NIGHTMARE
	db CURSE
	db FORESIGHT
	db CHARM
	db ATTRACT
	db ROCK_SMASH
	db 0 ; end set

; 4: originally "[mon]の<LINE>[move]!" ("[mon]'s<LINE>[move]!")
; Any move not listed above uses this grammar.
	db -1 ; end
