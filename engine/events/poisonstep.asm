HC_HealStep:
; HEAL CHARM: every four steps each living party member regains 1 HP and 1/128 of its maximum.
	ld a, HEAL_CHARM
	call HC_HasCharm
	ret nc
	ld a, [wPartyCount]
	and a
	ret z
	ld c, a
	ld hl, wPartyMon1HP
.loop
	push bc
	push hl
	ld a, [hli]
	ld d, a
	ld a, [hld]
	ld e, a ; de = HP, hl = HP high byte
	or d
	jr z, .next ; the fainted stay fainted
	push hl
	inc hl
	inc hl ; MON_MAXHP follows MON_HP
	ld a, [hli]
	ld b, a
	ld c, [hl] ; bc = maximum HP
	pop hl
	ld a, c
	rlca ; carry = bit 7 of the low byte
	ld a, b
	rla ; a = maximum HP / 128
	inc a
	add e
	ld e, a
	jr nc, .added
	inc d
.added
	ld a, e
	sub c
	ld a, d
	sbc b
	jr c, .store ; still below the maximum
	ld d, b
	ld e, c
.store
	ld a, d
	ld [hli], a
	ld [hl], e
.next
	pop hl
	ld de, PARTYMON_STRUCT_LENGTH
	add hl, de
	pop bc
	dec c
	jr nz, .loop
	ret

DoPoisonStep::
	call HC_HealStep
	ld a, [wPartyCount]
	and a
	jr z, .no_faint

	xor a
	ld c, wPoisonStepDataEnd - wPoisonStepData
	ld hl, wPoisonStepData
.loop_clearPoisonStepData
	ld [hli], a
	dec c
	jr nz, .loop_clearPoisonStepData

	xor a
	ld [wCurPartyMon], a
.loop_check_poison
	call .DamageMonIfPoisoned
	jr nc, .not_poisoned
; the output flag is stored in c, copy it to [wPoisonStepPartyFlags + [wCurPartyMon]]
; and set the corresponding flag in wPoisonStepFlagSum
	ld a, [wCurPartyMon]
	ld e, a
	ld d, 0
	ld hl, wPoisonStepPartyFlags
	add hl, de
	ld [hl], c
	ld a, [wPoisonStepFlagSum]
	or c
	ld [wPoisonStepFlagSum], a

.not_poisoned
	ld a, [wPartyCount]
	ld hl, wCurPartyMon
	inc [hl]
	cp [hl]
	jr nz, .loop_check_poison

	ld a, [wPoisonStepFlagSum]
	and %10
	jr nz, .someone_has_fainted
	ld a, [wPoisonStepFlagSum]
	and %01
	jr z, .no_faint
	call .PlayPoisonSFX
	xor a
	ret

.someone_has_fainted
	ld a, BANK(.Script_MonFaintedToPoison)
	ld hl, .Script_MonFaintedToPoison
	call CallScript
	scf
	ret

.no_faint
	xor a
	ret

.DamageMonIfPoisoned:
; check if mon is poisoned, return if not
	ld a, MON_STATUS
	call GetPartyParamLocation
	ld a, [hl]
	and 1 << PSN
	ret z

; check if mon is already fainted, return if so
	ld a, MON_HP
	call GetPartyParamLocation
	ld a, [hli]
	ld b, a
	ld c, [hl]
	or c
	ret z

; do 1 HP damage
	dec bc
	ld [hl], c
	dec hl
	ld [hl], b

; check if mon has fainted as a result of poison damage
	ld a, b
	or c
	jr nz, .not_fainted

; the mon has fainted, reset its status, set carry, and return %10
	ld a, MON_STATUS
	call GetPartyParamLocation
	ld [hl], 0
	ld c, %10
	scf
	ret

.not_fainted
; set carry and return %01
	ld c, %01
	scf
	ret

.PlayPoisonSFX:
	ld de, SFX_POISON
	call PlaySFX
	ld b, $2
	predef LoadPoisonBGPals
	call DelayFrame
	ret

.Script_MonFaintedToPoison:
	callasm .PlayPoisonSFX
	opentext
	callasm .CheckWhitedOut
	iffalse .whiteout
	closetext
	end

.whiteout
	farsjump OverworldWhiteoutScript

.CheckWhitedOut:
	xor a
	ld [wCurPartyMon], a
	ld de, wPoisonStepPartyFlags
.party_loop
	push de
	ld a, [de]
	and %10
	jr z, .mon_not_fainted
	ld c, HAPPINESS_POISONFAINT
	farcall ChangeHappiness
	farcall GetPartyNickname
	ld hl, .PoisonFaintText
	call PrintText

.mon_not_fainted
	pop de
	inc de
	ld hl, wCurPartyMon
	inc [hl]
	ld a, [wPartyCount]
	cp [hl]
	jr nz, .party_loop
	predef CheckPlayerPartyForFitMon
	ld a, d
	ld [wScriptVar], a
	ret

.PoisonFaintText:
	text_far _PoisonFaintText
	text_end

.PoisonWhiteoutText: ; unreferenced
	text_far _PoisonWhiteoutText
	text_end
