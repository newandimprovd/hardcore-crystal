GameFreakPresents_NextScene:
	ld hl, wJumptableIndex
	inc [hl]
	ret

GameFreakLogoSpriteAnim:
	ld hl, SPRITEANIMSTRUCT_JUMPTABLE_INDEX
	add hl, bc
	ld e, [hl]
	ld d, 0
	ld hl, .scenes
	add hl, de
	add hl, de
	ld a, [hli]
	ld h, [hl]
	ld l, a
	jp hl

.scenes:
	dw GameFreakLogo_Init
	dw GameFreakLogo_Bounce
	dw GameFreakLogo_Ditto
	dw GameFreakLogo_Transform
	dw GameFreakLogo_Done

GameFreakLogo_Init:
	ld hl, SPRITEANIMSTRUCT_JUMPTABLE_INDEX
	add hl, bc
	inc [hl]
	ret

GameFreakLogo_Bounce:
; Bounce with a height of 0C, 0C / 48 times.
; By default, this is twice, with a height of 96 pixels and 48 pixels.
; Sine offset starts at 48 (32+32/2, or pi+pi/2), so it starts at the maximum
; value of the sine wave (i.e. the top of the screen).

	ld hl, SPRITEANIMSTRUCT_VAR1 ; jump height
	add hl, bc
	ld a, [hl]
	and a
	jr z, .done

; Load the sine offset, make sure it doesn't reach the negative part of the wave
	ld d, a
	ld hl, SPRITEANIMSTRUCT_VAR2 ; sine offset
	add hl, bc
	ld a, [hl]
	and $3f ; full circle = 2*pi = 2*32
	cp 32
	jr nc, .no_negative
	add 32
.no_negative

	ld e, a
	farcall BattleAnim_Sine_e ; e = d * sin(e * pi/32)
	ld hl, SPRITEANIMSTRUCT_YOFFSET
	add hl, bc
	ld [hl], e

; Decrement the sine offset
	ld hl, SPRITEANIMSTRUCT_VAR2 ; sine offset
	add hl, bc
	ld a, [hl]
	dec [hl]
	and $1f ; a%32 == 0
	ret nz

; If the ditto's reached the ground, decrement the jump height and play the sfx
	ld hl, SPRITEANIMSTRUCT_VAR1 ; jump height
	add hl, bc
	ld a, [hl]
	sub 48
	ld [hl], a
	ld de, SFX_DITTO_BOUNCE
	call PlaySFX
	ret

.done
	ld hl, SPRITEANIMSTRUCT_JUMPTABLE_INDEX
	add hl, bc
	inc [hl]
	ld hl, SPRITEANIMSTRUCT_VAR2
	add hl, bc
	ld [hl], 0
	ld de, SFX_DITTO_POP_UP
	call PlaySFX
	ret

GameFreakLogo_Ditto:
; Wait a little, then start transforming
	ld hl, SPRITEANIMSTRUCT_VAR2 ; frame count
	add hl, bc
	ld a, [hl]
	cp 32
	jr nc, .start_transform
	inc [hl]
	ret

.start_transform
	ld hl, SPRITEANIMSTRUCT_JUMPTABLE_INDEX
	add hl, bc
	inc [hl]
	ld hl, SPRITEANIMSTRUCT_VAR2
	add hl, bc
	ld [hl], 0
	ld de, SFX_DITTO_TRANSFORM
	call PlaySFX
	ret

GameFreakLogo_Transform:
	ld hl, SPRITEANIMSTRUCT_VAR2 ; frame count
	add hl, bc
	ld a, [hl]
	cp 64
	jr z, .done
	inc [hl]

; Fade ditto's palettes while it's transforming
	srl a
	srl a
	ld e, a
	ld d, 0
	ld hl, GameFreakDittoPaletteFade
	add hl, de
	add hl, de
	ldh a, [rWBK]
	push af
	ld a, BANK(wOBPals2)
	ldh [rWBK], a
	ld a, [hli]
	ld [wOBPals2 + 12], a
	ld a, [hli]
	ld [wOBPals2 + 13], a
	pop af
	ldh [rWBK], a
	ld a, TRUE
	ldh [hCGBPalUpdate], a
	ret

.done
	ld hl, SPRITEANIMSTRUCT_JUMPTABLE_INDEX
	add hl, bc
	inc [hl]
	call GameFreakPresents_NextScene
GameFreakLogo_Done:
	ret

GameFreakDittoPaletteFade:
INCLUDE "gfx/splash/ditto_fade.pal"

GameFreakLogoGFX:
INCBIN "gfx/splash/gamefreak_presents.1bpp"
INCBIN "gfx/splash/gamefreak_logo.1bpp"
