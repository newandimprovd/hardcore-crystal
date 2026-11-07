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
	; Most people die quietly. Bosses get their own last words, about one in seven of the rest a line of dry commentary.
	callasm HC_DeathMode
	ifequal 0, .Loot
	ifequal 1, .Random
	scall HC_UniqueDeathScript
	pause 10
	sjump .Loot
.Random:
	opentext
	writetext HC_DeathText
	waitbutton
	closetext
	pause 10
.Loot:
	opentext
	writetext HC_LootText
	waitbutton
	closetext
	; About one body in four also carries something useful. What it carries gets better the higher the count climbs.
	callasm HC_RollItemDrop
	ifequal 0, .NoDrop
	getitemname STRING_BUFFER_3, USE_SCRIPT_VAR
	giveitem ITEM_FROM_MEM
	iffalse .NoDrop ; bag full: the item stays on the body
	opentext
	writetext HC_ItemDropText
	waitbutton
	closetext
.NoDrop:
	callasm HC_CountKill
	checkevent EVENT_HC_REVEAL_PENDING
	iftrue HC_RevealAftermath
	callasm HC_CheckStory ; the tidal wave kill, the rival and the final boss run story scripts (engine/hardcore/story.asm)
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
	text_ram wStringBuffer1
	text_start
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
	text "<PLAYER> took"
	line "¥@"
	text_asm
	push bc
	call HC_RollLoot
	pop bc
	ld hl, .Amount
	ret

.Amount:
	text_decimal hMoneyTemp, 3, 6
	text " off the body.@"
	text_asm
	push bc
	ld b, 5
	call HC_RandMod
	and a
	jr nz, .no_flavor
	ld b, HC_NUM_FLAVORS
	call HC_RandMod
	ld hl, HC_FlavorTable
	call HC_GetTableEntry
	pop bc
	ret

.no_flavor
	pop bc
	ld hl, .End
	ret

.End:
	text_end ; a text_asm block hands back a text *command*, so this is TX_END, not the in-string <DONE>

HC_ItemDropText:
	text "Pockets held:"
	line "@"
	text_ram wStringBuffer3
	text_end

HC_RollItemDrop:
; wScriptVar = an expendable item for the kill count reached so far, or 0 for nothing (about 1 body in 4).
; The kill counter is already past this kill's predecessor, so the tiers are 0 to HC_DROP_TIER1-1, up to HC_DROP_TIER2-1, up to HC_DROP_TIER3-1 and beyond (areas/counts.py).
	call Random
	cp 64
	jr c, .drop
	xor a
	ld [wScriptVar], a
	ret

.drop
	ld hl, wHCKillCount
	ld a, [hli]
	ld c, a
	ld b, [hl] ; bc = kills
	ld d, 0 ; tier
	ld a, c
	sub LOW(HC_DROP_TIER1)
	ld a, b
	sbc HIGH(HC_DROP_TIER1)
	jr c, .tier_done
	inc d
	ld a, c
	sub LOW(HC_DROP_TIER2)
	ld a, b
	sbc HIGH(HC_DROP_TIER2)
	jr c, .tier_done
	inc d
	ld a, c
	sub LOW(HC_DROP_TIER3)
	ld a, b
	sbc HIGH(HC_DROP_TIER3)
	jr c, .tier_done
	inc d
.tier_done
	ld a, d
	add a
	add a
	add a ; 8 items per tier
	ld e, a
	ld d, 0
	ld hl, HC_ItemDropTable
	add hl, de
	push hl
	ld b, 8
	call HC_RandMod
	pop hl
	ld e, a
	ld d, 0
	add hl, de
	ld a, [hl]
	ld [wScriptVar], a
	ret

HC_ItemDropTable:
; tier 0: the first hundred
	db POTION, POTION, ANTIDOTE, POKE_BALL, POKE_BALL, PARLYZ_HEAL, REPEL, AWAKENING
; tier 1
	db SUPER_POTION, POTION, GREAT_BALL, POKE_BALL, BURN_HEAL, ICE_HEAL, SUPER_REPEL, REVIVE
; tier 2
	db SUPER_POTION, HYPER_POTION, GREAT_BALL, ULTRA_BALL, FULL_HEAL, REVIVE, ETHER, MAX_REPEL
; tier 3
	db HYPER_POTION, MAX_POTION, ULTRA_BALL, FULL_HEAL, MAX_REVIVE, ELIXER, DIRE_HIT, X_ATTACK

HC_DeathMode:
; wScriptVar: 0 = the trainer dies quietly, 1 = a random line, 2 + n = the unique last words of row n of HC_UniqueDeathTable
	ld a, [wTempTrainerClass]
	ld b, a
	ld hl, HC_UniqueDeathTable
	ld c, 2
.loop
	ld a, BANK(HC_UniqueDeathTable)
	call GetFarByte
	inc hl
	cp -1
	jr z, .random
	cp b
	jr z, .unique
	inc c
	jr .loop

.unique
	ld a, c
	ld [wScriptVar], a
	ret

.random
	call Random
	cp 36 ; about one in seven
	ld a, 1
	jr c, .store
	xor a
.store
	ld [wScriptVar], a
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
