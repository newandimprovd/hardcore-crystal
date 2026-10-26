; Hardcore mode: trainer death, bodies and looting.
; Everything here only runs once EVENT_KILLER_REVEALED is set.
; NOTE: text_asm blocks run inline in the text engine, which keeps the tilemap
; cursor in bc. Every text_asm block here must preserve bc and return hl = next text.

TrainerDeathScript::
	pause 10
	playsound SFX_FAINT
	earthquake 10
	waitsfx
	callasm HC_MakeCorpse
	reloadmap
	callasm HC_RespawnCorpse
	callasm HC_PrepareDeath
	opentext
	writetext HC_DeathText
	waitbutton
	closetext
	pause 10
	opentext
	writetext HC_LootText
	waitbutton
	closetext
	callasm HC_CountKill
	checkevent EVENT_HC_REVEAL_PENDING
	iftrue HC_RevealAftermath
	callasm HC_CheckStory ; kill 200, the rival and the final boss run story scripts (engine/hardcore/story.asm)
	iffalse .NoStory
	farsjump HC_StoryDispatch
.NoStory:
	end

FirstKillRevealScript::
	setevent EVENT_KILLER_REVEALED
	setevent EVENT_HC_REVEAL_PENDING
	special FadeOutMusic
	sjump TrainerDeathScript

HC_RevealAftermath:
	clearevent EVENT_HC_REVEAL_PENDING
	pause 30
	opentext
	writetext HC_RevealText1
	waitbutton
	writetext HC_RevealText2
	waitbutton
	writetext HC_RevealText3
	waitbutton
	writetext HC_RevealText4
	waitbutton
	closetext
	pause 30
	playsound SFX_ELEVATOR_END
	earthquake 30
	waitsfx
	opentext
	writetext HC_RevealText5
	waitbutton
	writetext HC_RevealText6
	waitbutton
	closetext
	special RestartMapMusic
	end

DeadTrainerTalkScript::
	opentext
	writetext HC_BodyText
	waitbutton
	closetext
	end

HC_DeathText:
	text_ram wStringBuffer3
	text_start
	line "@"
	text_ram wStringBuffer1
	text " is dead."

	para "Cause of death:"
	line "@"
	text_asm
	push bc
	call HC_PickCause
	pop bc
	ret

HC_BodyText:
	text_asm
	push bc
	ld b, HC_NUM_BODIES
	call HC_RandMod
	ld hl, HC_BodyTable
	call HC_GetTableEntry
	pop bc
	ret

HC_LootText:
	text "<PLAYER> searched"
	line "the body and found"
	cont "¥@"
	text_asm
	push bc
	call HC_RollLoot
	pop bc
	ld hl, .Amount
	ret

.Amount:
	text_decimal hMoneyTemp, 3, 6
	text ".@"
	text_asm
	push bc
	ld b, HC_NUM_FLAVORS
	call HC_RandMod
	ld hl, HC_FlavorTable
	call HC_GetTableEntry
	pop bc
	ret

HC_PickCause:
	ld b, HC_NUM_CAUSES
	call HC_RandMod
	ld hl, HC_CauseTable
	; fallthrough

HC_GetTableEntry:
; hl = table of text pointers, a = index. Returns the pointer in hl.
	ld e, a
	ld d, 0
	add hl, de
	add hl, de
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ret

HC_CountKill:
	ld hl, wHCKillCount
	ld a, [hl]
	inc a
	ld [hli], a
	ret nz
	inc [hl]
	ret

HC_RandMod:
; a = random number in [0, b)
.retry
	call Random
.sub
	cp b
	jr c, .done
	sub b
	jr .sub
.done
	ret

HC_RollLoot:
; Give the player 100 to 610 dollars and leave the amount in hMoneyTemp.
	call Random
	ld c, a
	ld b, 0
	sla c
	rl b
	ld a, c
	add 100
	ld c, a
	ld a, b
	adc 0
	ld b, a
	xor a
	ldh [hMoneyTemp], a
	ld a, b
	ldh [hMoneyTemp + 1], a
	ld a, c
	ldh [hMoneyTemp + 2], a
	ld de, wMoney
	ld bc, hMoneyTemp
	farcall GiveMoney
	ret

HC_PrepareDeath:
; wStringBuffer3 = trainer class, wStringBuffer1 = trainer name
	ld a, [wTempTrainerClass]
	ld c, a
	farcall GetTrainerClassName
	ld hl, wStringBuffer1
	ld de, wStringBuffer3
	ld bc, TRAINER_CLASS_NAME_LENGTH
	call CopyBytes
	ld a, [wTempTrainerID]
	ld b, a
	ld a, [wTempTrainerClass]
	ld c, a
	farcall GetTrainerName
	ret

HC_MakeCorpse:
; Turn the trainer we just beat into a body.
	ldh a, [hLastTalked]
	ld [wScriptVar], a
	call GetMapObject
	ld hl, MAPOBJECT_SPRITE
	add hl, bc
	ld [hl], SPRITE_CORPSE
	ld hl, MAPOBJECT_MOVEMENT
	add hl, bc
	ld [hl], SPRITEMOVEDATA_STILL
	ld hl, MAPOBJECT_TYPE
	add hl, bc
	ld a, [hl]
	and MAPOBJECT_TYPE_MASK
	or PAL_NPC_RED << 4
	ld [hl], a
	ret

HC_RespawnCorpse:
; The live object struct still has the old sprite, so rebuild it from the
; map object. Must run after reloadmap so the corpse gfx is already loaded.
	ld a, [wScriptVar]
	call DeleteObjectStruct
	ld a, [wScriptVar]
	call UnmaskCopyMapObjectStruct
	farcall _UpdateSprites
	ret

HC_ConvertDeadTrainers::
; Called whenever a map's object events are loaded.
; Beaten trainers are bodies once the killer has been revealed.
	ld de, EVENT_KILLER_REVEALED
	ld b, CHECK_FLAG
	call EventFlagAction
	ld a, c
	and a
	ret z
	ld a, 1
	ld de, wMap1Object
.loop
	push af
	push de
	ld hl, MAPOBJECT_SPRITE
	add hl, de
	ld a, [hl]
	and a
	jr z, .next
	ld hl, MAPOBJECT_TYPE
	add hl, de
	ld a, [hl]
	and MAPOBJECT_TYPE_MASK
	cp OBJECTTYPE_TRAINER
	jr nz, .next
	ld hl, MAPOBJECT_SCRIPT_POINTER
	add hl, de
	ld a, [hli]
	ld h, [hl]
	ld l, a
	push de
	ld a, [wMapScriptsBank]
	call GetFarWord
	ld d, h
	ld e, l
	ld b, CHECK_FLAG
	call EventFlagAction
	pop de
	ld a, c
	and a
	jr z, .next
	ld hl, MAPOBJECT_SPRITE
	add hl, de
	ld [hl], SPRITE_CORPSE
	ld hl, MAPOBJECT_MOVEMENT
	add hl, de
	ld [hl], SPRITEMOVEDATA_STILL
	ld hl, MAPOBJECT_TYPE
	add hl, de
	ld a, [hl]
	and MAPOBJECT_TYPE_MASK
	or PAL_NPC_RED << 4
	ld [hl], a
.next
	pop de
	ld hl, MAPOBJECT_LENGTH
	add hl, de
	ld d, h
	ld e, l
	pop af
	inc a
	cp NUM_OBJECTS
	jr nz, .loop
	ret

INCLUDE "data/hardcore/death_causes.asm"
INCLUDE "data/hardcore/reveal_text.asm"
