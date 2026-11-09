FieldMoveJumptableReset:
	xor a
	ld hl, wFieldMoveData
	ld bc, wFieldMoveDataEnd - wFieldMoveData
	call ByteFill
	ret

FieldMoveJumptable:
	ld a, [wFieldMoveJumptableIndex]
	rst JumpTable
	ld [wFieldMoveJumptableIndex], a
	bit JUMPTABLE_EXIT_F, a
	jr nz, .okay
	and a
	ret

.okay
	and JUMPTABLE_INDEX_MASK
	scf
	ret

GetPartyNickname:
; write wCurPartyMon nickname to wStringBuffer1-3
	ld hl, wPartyMonNicknames
	ld a, BOXMON
	ld [wMonType], a
	ld a, [wCurPartyMon]
	call GetNickname
	call CopyName1
; copy text from wStringBuffer2 to wStringBuffer3
	ld de, wStringBuffer2
	ld hl, wStringBuffer3
	call CopyName2
	ret

CheckEngineFlag:
; Hardcore edit: badges no longer gate field moves.
; Always report the flag as set (no carry).
	xor a
	ret

CheckBadge:
; Check engine flag a (ENGINE_ZEPHYRBADGE thru ENGINE_EARTHBADGE)
; Display "Badge required" text and return carry if the badge is not owned
	call CheckEngineFlag
	ret nc
	ld hl, .BadgeRequiredText
	call MenuTextboxBackup ; push text to queue
	scf
	ret

.BadgeRequiredText:
	text_far _BadgeRequiredText
	text_end

CheckPartyMove:
; Hardcore edit: field moves come from key items, not from #MON.
; Check if the player owns the key item that stands in for move d.
; Returns carry if the item is missing.
	ld hl, FieldMoveKeyItems
.loop
	ld a, [hli]
	cp -1
	jr z, .no
	cp d
	jr z, .found
	inc hl
	jr .loop

.found
	ld a, [hl]
	ld [wCurItem], a
	ld hl, wNumItems
	call CheckItem
	jr nc, .no
	xor a
	ld [wCurPartyMon], a ; the lead #MON is the one pictured
	ret

.no
	scf
	ret

FieldMoveKeyItems:
	db CUT,        CHAINSAW
	db SURF,       JET_SKI
	db STRENGTH,   CROWBAR
	db FLASH,      FLASHLIGHT
	db WHIRLPOOL,  OUTBOARD
	db WATERFALL,  GRAPPLE_HOOK
	db ROCK_SMASH, SLEDGEHAMMER
	db HEADBUTT,   BASEBALL_BAT
	db DIG,        SHOVEL
	db FLY,        GETAWAY_CAR
	db -1

FieldMoveFailed:
	ld hl, .CantUseItemText
	call MenuTextboxBackup
	ret

.CantUseItemText:
	text_far _CantUseItemText
	text_end

CutFunction:
	call FieldMoveJumptableReset
.loop
	ld hl, .Jumptable
	call FieldMoveJumptable
	jr nc, .loop
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.Jumptable:
	dw .CheckAble
	dw .DoCut
	dw .FailCut

.CheckAble:
	ld de, ENGINE_HIVEBADGE
	call CheckBadge
	jr c, .nohivebadge
	call CheckMapForSomethingToCut
	jr c, .nothingtocut
	ld a, $1
	ret

.nohivebadge
	ld a, JUMPTABLE_EXIT
	ret

.nothingtocut
	ld a, $2
	ret

.DoCut:
	ld hl, Script_CutFromMenu
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.FailCut:
	ld hl, CutNothingText
	call MenuTextboxBackup
	ld a, JUMPTABLE_EXIT
	ret

UseCutText:
	text_far _UseCutText
	text_end

CutNothingText:
	text_far _CutNothingText
	text_end

CheckMapForSomethingToCut:
	; Does the collision data of the facing tile permit cutting?
	call GetFacingTileCoord
	ld c, a
	push de
	farcall CheckCutCollision
	pop de
	jr nc, .fail
	; Get the location of the current block in wOverworldMapBlocks.
	call GetBlockLocation
	ld c, [hl]
	; See if that block contains something that can be cut.
	push hl
	ld hl, CutTreeBlockPointers
	call CheckOverworldTileArrays
	pop hl
	jr nc, .fail
	; Save the Cut field move data
	ld a, l
	ld [wCutWhirlpoolOverworldBlockAddr], a
	ld a, h
	ld [wCutWhirlpoolOverworldBlockAddr + 1], a
	ld a, b
	ld [wCutWhirlpoolReplacementBlock], a
	ld a, c
	ld [wCutWhirlpoolAnimationType], a
	xor a
	ret

.fail
	scf
	ret

Script_CutFromMenu:
	refreshmap
	special UpdateTimePals

Script_Cut:
	callasm GetPartyNickname
	writetext UseCutText
	refreshmap
	callasm CutDownTreeOrGrass
	closetext
	end

CutDownTreeOrGrass:
	ld hl, wCutWhirlpoolOverworldBlockAddr
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld a, [wCutWhirlpoolReplacementBlock]
	ld [hl], a
	xor a
	ldh [hBGMapMode], a
	call LoadOverworldTilemapAndAttrmapPals
	call UpdateSprites
	call DelayFrame
	ld a, [wCutWhirlpoolAnimationType]
	ld e, a
	farcall OWCutAnimation
	call BufferScreen
	call GetMovementPermissions
	call UpdateSprites
	call DelayFrame
	call LoadStandardFont
	ret

CheckOverworldTileArrays:
	; Input: c contains the tile you're facing
	; Output: Replacement tile in b and effect on wild encounters in c, plus carry set.
	;         Carry is not set if the facing tile cannot be replaced, or if the tileset
	;         does not contain a tile you can replace.

	; Dictionary lookup for pointer to tile replacement table
	push bc
	ld a, [wMapTileset]
	ld de, 3
	call IsInArray
	pop bc
	jr nc, .nope
	; Load the pointer
	inc hl
	ld a, [hli]
	ld h, [hl]
	ld l, a
	; Look up the tile you're facing
	ld de, 3
	ld a, c
	call IsInArray
	jr nc, .nope
	; Load the replacement to b
	inc hl
	ld b, [hl]
	; Load the animation type parameter to c
	inc hl
	ld c, [hl]
	scf
	ret

.nope
	xor a
	ret

INCLUDE "data/collision/field_move_blocks.asm"

FlashFunction:
	call .CheckUseFlash
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.CheckUseFlash:
	ld de, ENGINE_ZEPHYRBADGE
	farcall CheckBadge
	jr c, .nozephyrbadge
	ld a, [wTimeOfDayPalset]
	cp DARKNESS_PALSET
	jr nz, .notadarkcave
	call UseFlash
	ld a, JUMPTABLE_EXIT | $1
	ret

.notadarkcave
	call FieldMoveFailed
	ld a, JUMPTABLE_EXIT
	ret

.nozephyrbadge
	ld a, JUMPTABLE_EXIT
	ret

UseFlash:
	ld hl, Script_UseFlash
	jp QueueScript

Script_UseFlash:
	refreshmap
	special UpdateTimePals
	writetext UseFlashTextScript
	callasm BlindingFlash
	closetext
	end

UseFlashTextScript:
	text_far _BlindingFlashText
	text_asm
	call WaitSFX
	ld de, SFX_FLASH
	call PlaySFX
	call WaitSFX
	ld hl, .BlankText
	ret

.BlankText:
	text_end

SurfFunction:
	call FieldMoveJumptableReset
.loop
	ld hl, .Jumptable
	call FieldMoveJumptable
	jr nc, .loop
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.Jumptable:
	dw .TrySurf
	dw .DoSurf
	dw .FailSurf
	dw .AlreadySurfing

.TrySurf:
	ld de, ENGINE_FOGBADGE
	call CheckBadge
	jr c, .nofogbadge
	ld a, [wPlayerState]
	cp PLAYER_SURF
	jr z, .alreadyfail
	cp PLAYER_SURF_PIKA
	jr z, .alreadyfail
	call GetFacingTileCoord
	call GetTilePermission
	cp WATER_TILE
	jr nz, .cannotsurf
	call CheckDirection
	jr c, .cannotsurf
	farcall CheckFacingObject
	jr c, .cannotsurf
	ld a, $1
	ret
.nofogbadge
	ld a, JUMPTABLE_EXIT
	ret
.alreadyfail
	ld a, $3
	ret
.cannotsurf
	ld a, $2
	ret

.DoSurf:
	call GetSurfType
	ld [wSurfingPlayerState], a
	call GetPartyNickname
	ld hl, SurfFromMenuScript
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.FailSurf:
	ld hl, CantSurfText
	call MenuTextboxBackup
	ld a, JUMPTABLE_EXIT
	ret

.AlreadySurfing:
	ld hl, AlreadySurfingText
	call MenuTextboxBackup
	ld a, JUMPTABLE_EXIT
	ret

SurfFromMenuScript:
	special UpdateTimePals

UsedSurfScript:
; BUG: Surfing directly across a map connection does not load the new map (see docs/bugs_and_glitches.md)
	writetext UsedSurfText ; "used SURF!"
	waitbutton
	closetext

	callasm .stubbed_fn

	readmem wSurfingPlayerState
	writevar VAR_MOVEMENT

	special UpdatePlayerSprite
	special PlayMapMusic
; step into the water (slow_step DIR, step_end)
	special SurfStartStep
	applymovement PLAYER, wMovementBuffer
	end

.stubbed_fn
	ret

UsedSurfText:
	text_far _UsedSurfText
	text_end

CantSurfText:
	text_far _CantSurfText
	text_end

AlreadySurfingText:
	text_far _AlreadySurfingText
	text_end

GetSurfType:
; Surfing on Pikachu uses an alternate sprite.
; This is done by using a separate movement type.

	ld a, [wCurPartyMon]
	ld e, a
	ld d, 0
	ld hl, wPartySpecies
	add hl, de

	ld a, [hl]
	cp PIKACHU
	ld a, PLAYER_SURF_PIKA
	ret z
	ld a, PLAYER_SURF
	ret

CheckDirection:
; Return carry if a tile permission prevents you
; from moving in the direction you're facing.

; Get player direction
	ld a, [wPlayerDirection]
	and %00001100 ; bits 2 and 3 contain direction
	rrca
	rrca
	ld e, a
	ld d, 0
	ld hl, .Directions
	add hl, de

; Can you walk in this direction?
	ld a, [wTilePermissions]
	and [hl]
	jr nz, .quit
	xor a
	ret

.quit
	scf
	ret

.Directions:
	db FACE_DOWN
	db FACE_UP
	db FACE_LEFT
	db FACE_RIGHT

TrySurfOW::
; Checking a tile in the overworld.
; Return carry if fail is allowed.

; Don't ask to surf if already fail.
	ld a, [wPlayerState]
	cp PLAYER_SURF_PIKA
	jr z, .quit
	cp PLAYER_SURF
	jr z, .quit

; Must be facing water.
	ld a, [wFacingTileID]
	call GetTilePermission
	cp WATER_TILE
	jr nz, .quit

; Check tile permissions.
	call CheckDirection
	jr c, .quit

	ld de, ENGINE_FOGBADGE
	call CheckEngineFlag
	jr c, .quit

	ld d, SURF
	call CheckPartyMove
	jr c, .quit

	call GetSurfType
	ld [wSurfingPlayerState], a
	call GetPartyNickname

	ld a, BANK(AskSurfScript)
	ld hl, AskSurfScript
	call CallScript

	scf
	ret

.quit
	xor a
	ret

AskSurfScript:
	opentext
	writetext AskSurfText
	yesorno
	iftrue UsedSurfScript
	closetext
	end

AskSurfText:
	text_far _AskSurfText
	text_end

FlyFunction:
	call FieldMoveJumptableReset
.loop
	ld hl, .Jumptable
	call FieldMoveJumptable
	jr nc, .loop
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.Jumptable:
	dw .TryFly
	dw .DoFly
	dw .FailFly

.TryFly:
	ld de, ENGINE_STORMBADGE
	call CheckBadge
	jr c, .nostormbadge
	call GetMapEnvironment
	call CheckOutdoorMap
	jr z, .outdoors
	jr .indoors

.outdoors
	xor a
	ldh [hMapAnims], a
	call LoadStandardMenuHeader
	call ClearSprites
	farcall _FlyMap
	ld a, e
	cp -1
	jr z, .illegal
	cp NUM_SPAWNS
	jr nc, .illegal

	ld [wDefaultSpawnpoint], a
	call CloseWindow
	ld a, $1
	ret

.nostormbadge
	ld a, JUMPTABLE_EXIT | $2
	ret

.indoors
	ld a, $2
	ret

.illegal
	call CloseWindow
	call WaitBGMap
	ld a, JUMPTABLE_EXIT
	ret

.DoFly:
	ld hl, .FlyScript
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.FailFly:
	call FieldMoveFailed
	ld a, JUMPTABLE_EXIT | $2
	ret

.FlyScript:
	refreshmap
	callasm HideSprites
	special UpdateTimePals
	callasm FlyFromAnim
	callasm SkipUpdateMapSprites
	loadvar VAR_MOVEMENT, PLAYER_NORMAL
	newloadmap MAPSETUP_FLY
	callasm FlyToAnim
	special WaitSFX
	callasm .ReturnFromFly
	end

.ReturnFromFly:
	farcall RespawnPlayer
	call DelayFrame
	call UpdatePlayerSprite
	farcall LoadOverworldFont
	ret

WaterfallFunction:
	call .TryWaterfall
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.TryWaterfall:
	ld de, ENGINE_RISINGBADGE
	farcall CheckBadge
	ld a, JUMPTABLE_EXIT
	ret c
	call CheckMapCanWaterfall
	jr c, .failed
	ld hl, Script_WaterfallFromMenu
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.failed
	call FieldMoveFailed
	ld a, JUMPTABLE_EXIT
	ret

CheckMapCanWaterfall:
	ld a, [wPlayerDirection]
	and $c
	cp FACE_UP
	jr nz, .failed
	ld a, [wTileUp]
	call CheckWaterfallTile
	jr nz, .failed
	xor a
	ret

.failed
	scf
	ret

Script_WaterfallFromMenu:
	refreshmap
	special UpdateTimePals

Script_UsedWaterfall:
	callasm GetPartyNickname
	writetext .UseWaterfallText
	waitbutton
	closetext
	playsound SFX_BUBBLEBEAM
.loop
	applymovement PLAYER, .WaterfallStep
	callasm .CheckContinueWaterfall
	iffalse .loop
	end

.CheckContinueWaterfall:
	xor a
	ld [wScriptVar], a
	ld a, [wPlayerTileCollision]
	call CheckWaterfallTile
	ret z
	ld a, $1
	ld [wScriptVar], a
	ret

.WaterfallStep:
	turn_waterfall UP
	step_end

.UseWaterfallText:
	text_far _UseWaterfallText
	text_end

TryWaterfallOW::
	ld d, WATERFALL
	call CheckPartyMove
	jr c, .failed
	ld de, ENGINE_RISINGBADGE
	call CheckEngineFlag
	jr c, .failed
	call CheckMapCanWaterfall
	jr c, .failed
	ld a, BANK(Script_AskWaterfall)
	ld hl, Script_AskWaterfall
	call CallScript
	scf
	ret

.failed
	ld a, BANK(Script_CantDoWaterfall)
	ld hl, Script_CantDoWaterfall
	call CallScript
	scf
	ret

Script_CantDoWaterfall:
	jumptext .HugeWaterfallText

.HugeWaterfallText:
	text_far _HugeWaterfallText
	text_end

Script_AskWaterfall:
	opentext
	writetext .AskWaterfallText
	yesorno
	iftrue Script_UsedWaterfall
	closetext
	end

.AskWaterfallText:
	text_far _AskWaterfallText
	text_end

EscapeRopeFunction:
	call FieldMoveJumptableReset
	ld a, $1
	jr EscapeRopeOrDig

DigFunction:
	call FieldMoveJumptableReset
	ld a, $2

EscapeRopeOrDig:
	ld [wEscapeRopeOrDigType], a
.loop
	ld hl, .DigTable
	call FieldMoveJumptable
	jr nc, .loop
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.DigTable:
	dw .CheckCanDig
	dw .DoDig
	dw .FailDig

.CheckCanDig:
	call GetMapEnvironment
	cp CAVE
	jr z, .incave
	cp DUNGEON
	jr z, .incave
.fail
	ld a, $2
	ret

.incave
	ld hl, wDigWarpNumber
	ld a, [hli]
	and a
	jr z, .fail
	ld a, [hli]
	and a
	jr z, .fail
	ld a, [hl]
	and a
	jr z, .fail
	ld a, $1
	ret

.DoDig:
	ld hl, wDigWarpNumber
	ld de, wNextWarp
	ld bc, 3
	call CopyBytes
	call GetPartyNickname
	ld a, [wEscapeRopeOrDigType]
	cp $2
	jr nz, .escaperope
	ld hl, .UsedDigScript
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.escaperope
	ld hl, .UsedEscapeRopeScript
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.FailDig:
	ld a, [wEscapeRopeOrDigType]
	cp $2
	jr nz, .failescaperope
	ld hl, .CantUseDigText
	call MenuTextbox
	call WaitPressAorB_BlinkCursor
	call CloseWindow

.failescaperope
	ld a, JUMPTABLE_EXIT
	ret

.UseDigText:
	text_far _UseDigText
	text_end

.UseEscapeRopeText:
	text_far _UseEscapeRopeText
	text_end

.CantUseDigText:
	text_far _CantUseDigText
	text_end

.UsedEscapeRopeScript:
	refreshmap
	special UpdateTimePals
	writetext .UseEscapeRopeText
	sjump .UsedDigOrEscapeRopeScript

.UsedDigScript:
	refreshmap
	special UpdateTimePals
	writetext .UseDigText

.UsedDigOrEscapeRopeScript:
	waitbutton
	closetext
	playsound SFX_WARP_TO
	applymovement PLAYER, .DigOut
	loadvar VAR_MOVEMENT, PLAYER_NORMAL
	newloadmap MAPSETUP_DOOR
	playsound SFX_WARP_FROM
	applymovement PLAYER, .DigReturn
	end

.DigOut:
	step_dig 32
	hide_object
	step_end

.DigReturn:
	show_object
	return_dig 32
	step_end

TeleportFunction:
	call FieldMoveJumptableReset
.loop
	ld hl, .Jumptable
	call FieldMoveJumptable
	jr nc, .loop
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.Jumptable:
	dw .TryTeleport
	dw .DoTeleport
	dw .FailTeleport

.TryTeleport:
	call GetMapEnvironment
	call CheckOutdoorMap
	jr z, .CheckIfSpawnPoint
	jr .nope

.CheckIfSpawnPoint:
	ld a, [wLastSpawnMapGroup]
	ld d, a
	ld a, [wLastSpawnMapNumber]
	ld e, a
	farcall IsSpawnPoint
	jr nc, .nope
	ld a, c
	ld [wDefaultSpawnpoint], a
	ld a, $1
	ret

.nope
	ld a, $2
	ret

.DoTeleport:
	call GetPartyNickname
	ld hl, .TeleportScript
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.FailTeleport:
	ld hl, .CantUseTeleportText
	call MenuTextboxBackup
	ld a, JUMPTABLE_EXIT
	ret

.TeleportReturnText:
	text_far _TeleportReturnText
	text_end

.CantUseTeleportText:
	text_far _CantUseTeleportText
	text_end

.TeleportScript:
	refreshmap
	special UpdateTimePals
	writetext .TeleportReturnText
	pause 60
	refreshmap
	closetext
	playsound SFX_WARP_TO
	applymovement PLAYER, .TeleportFrom
	loadvar VAR_MOVEMENT, PLAYER_NORMAL
	newloadmap MAPSETUP_TELEPORT
	playsound SFX_WARP_FROM
	applymovement PLAYER, .TeleportTo
	end

.TeleportFrom:
	teleport_from
	step_end

.TeleportTo:
	teleport_to
	step_end

StrengthFunction:
	call .TryStrength
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.TryStrength:
	ld de, ENGINE_PLAINBADGE
	call CheckBadge
	jr c, .Failed
	jr .UseStrength

.Failed:
	ld a, JUMPTABLE_EXIT
	ret

.UseStrength:
	ld hl, Script_StrengthFromMenu
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

SetStrengthFlag:
	ld hl, wFieldMoveFlags
	set FIELDMOVE_STRENGTH_ACTIVE_F, [hl]
	ld a, [wCurPartyMon]
	ld e, a
	ld d, 0
	ld hl, wPartySpecies
	add hl, de
	ld a, [hl]
	ld [wStrengthSpecies], a
	call GetPartyNickname
	ret

Script_StrengthFromMenu:
	refreshmap
	special UpdateTimePals

Script_UsedStrength:
	callasm SetStrengthFlag
	writetext .UseStrengthText
	pause 3
	writetext .MoveBoulderText
	closetext
	end

.UseStrengthText:
	text_far _UseStrengthText
	text_end

.MoveBoulderText:
	text_far _MoveBoulderText
	text_end

AskStrengthScript:
	callasm TryStrengthOW
	iffalse .AskStrength
	ifequal $1, .DontMeetRequirements
	sjump .AlreadyUsedStrength

.DontMeetRequirements:
	jumptext BouldersMayMoveText

.AlreadyUsedStrength:
	jumptext BouldersMoveText

.AskStrength:
	opentext
	writetext AskStrengthText
	yesorno
	iftrue Script_UsedStrength
	closetext
	end

AskStrengthText:
	text_far _AskStrengthText
	text_end

BouldersMoveText:
	text_far _BouldersMoveText
	text_end

BouldersMayMoveText:
	text_far _BouldersMayMoveText
	text_end

TryStrengthOW:
	ld d, STRENGTH
	call CheckPartyMove
	jr c, .nope

	ld de, ENGINE_PLAINBADGE
	call CheckEngineFlag
	jr c, .nope

	ld hl, wFieldMoveFlags
	bit FIELDMOVE_STRENGTH_ACTIVE_F, [hl]
	jr z, .already_using

	ld a, 2
	jr .done

.nope
	ld a, 1
	jr .done

.already_using
	xor a

.done
	ld [wScriptVar], a
	ret

WhirlpoolFunction:
	call FieldMoveJumptableReset
.loop
	ld hl, .Jumptable
	call FieldMoveJumptable
	jr nc, .loop
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

.Jumptable:
	dw .TryWhirlpool
	dw .DoWhirlpool
	dw .FailWhirlpool

.TryWhirlpool:
	ld de, ENGINE_GLACIERBADGE
	call CheckBadge
	jr c, .noglacierbadge
	call TryWhirlpoolMenu
	jr c, .failed
	ld a, $1
	ret

.failed
	ld a, $2
	ret

.noglacierbadge
	ld a, JUMPTABLE_EXIT
	ret

.DoWhirlpool:
	ld hl, Script_WhirlpoolFromMenu
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.FailWhirlpool:
	call FieldMoveFailed
	ld a, JUMPTABLE_EXIT
	ret

UseWhirlpoolText:
	text_far _UseWhirlpoolText
	text_end

TryWhirlpoolMenu:
	call GetFacingTileCoord
	ld c, a
	push de
	call CheckWhirlpoolTile
	pop de
	jr c, .failed
	call GetBlockLocation
	ld c, [hl]
	push hl
	ld hl, WhirlpoolBlockPointers
	call CheckOverworldTileArrays
	pop hl
	jr nc, .failed
	; Save the Whirlpool field move data
	ld a, l
	ld [wCutWhirlpoolOverworldBlockAddr], a
	ld a, h
	ld [wCutWhirlpoolOverworldBlockAddr + 1], a
	ld a, b
	ld [wCutWhirlpoolReplacementBlock], a
	ld a, c
	ld [wCutWhirlpoolAnimationType], a
	xor a
	ret

.failed
	scf
	ret

Script_WhirlpoolFromMenu:
	refreshmap
	special UpdateTimePals

Script_UsedWhirlpool:
	callasm GetPartyNickname
	writetext UseWhirlpoolText
	refreshmap
	callasm DisappearWhirlpool
	closetext
	end

DisappearWhirlpool:
	ld hl, wCutWhirlpoolOverworldBlockAddr
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld a, [wCutWhirlpoolReplacementBlock]
	ld [hl], a
	xor a
	ldh [hBGMapMode], a
	call LoadOverworldTilemapAndAttrmapPals
	ld a, [wCutWhirlpoolAnimationType]
	ld e, a
	farcall PlayWhirlpoolSound
	call BufferScreen
	call GetMovementPermissions
	ret

TryWhirlpoolOW::
	ld d, WHIRLPOOL
	call CheckPartyMove
	jr c, .failed
	ld de, ENGINE_GLACIERBADGE
	call CheckEngineFlag
	jr c, .failed
	call TryWhirlpoolMenu
	jr c, .failed
	ld a, BANK(Script_AskWhirlpoolOW)
	ld hl, Script_AskWhirlpoolOW
	call CallScript
	scf
	ret

.failed
	ld a, BANK(Script_MightyWhirlpool)
	ld hl, Script_MightyWhirlpool
	call CallScript
	scf
	ret

Script_MightyWhirlpool:
	jumptext .MayPassWhirlpoolText

.MayPassWhirlpoolText:
	text_far _MayPassWhirlpoolText
	text_end

Script_AskWhirlpoolOW:
	opentext
	writetext AskWhirlpoolText
	yesorno
	iftrue Script_UsedWhirlpool
	closetext
	end

AskWhirlpoolText:
	text_far _AskWhirlpoolText
	text_end

HeadbuttFunction:
	call TryHeadbuttFromMenu
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

TryHeadbuttFromMenu:
	call GetFacingTileCoord
	call CheckHeadbuttTreeTile
	jr nz, .no_tree

	ld hl, HeadbuttFromMenuScript
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.no_tree
	call FieldMoveFailed
	ld a, JUMPTABLE_EXIT
	ret

UseHeadbuttText:
	text_far _UseHeadbuttText
	text_end

HeadbuttNothingText:
	text_far _HeadbuttNothingText
	text_end

HeadbuttFromMenuScript:
	refreshmap
	special UpdateTimePals

HeadbuttScript:
	callasm GetPartyNickname
	writetext UseHeadbuttText

	refreshmap
	callasm ShakeHeadbuttTree

	callasm TreeMonEncounter
	iffalse .no_battle
	closetext
	randomwildmon
	startbattle
	reloadmapafterbattle
	end

.no_battle
	writetext HeadbuttNothingText
	waitbutton
	closetext
	end

TryHeadbuttOW::
	ld d, HEADBUTT
	call CheckPartyMove
	jr c, .no

	ld a, BANK(AskHeadbuttScript)
	ld hl, AskHeadbuttScript
	call CallScript
	scf
	ret

.no
	xor a
	ret

AskHeadbuttScript:
	opentext
	writetext AskHeadbuttText
	yesorno
	iftrue HeadbuttScript
	closetext
	end

AskHeadbuttText:
	text_far _AskHeadbuttText
	text_end

RockSmashFunction:
	call TryRockSmashFromMenu
	and JUMPTABLE_INDEX_MASK
	ld [wFieldMoveSucceeded], a
	ret

TryRockSmashFromMenu:
	call GetFacingObject
	jr c, .no_rock
	ld a, d
	cp SPRITEMOVEDATA_SMASHABLE_ROCK
	jr nz, .no_rock

	ld hl, RockSmashFromMenuScript
	call QueueScript
	ld a, JUMPTABLE_EXIT | $1
	ret

.no_rock
	call FieldMoveFailed
	ld a, JUMPTABLE_EXIT
	ret

GetFacingObject:
	farcall CheckFacingObject
	jr nc, .fail

	ldh a, [hObjectStructIndex]
	call GetObjectStruct
	ld hl, OBJECT_MAP_OBJECT_INDEX
	add hl, bc
	ld a, [hl]
	ldh [hLastTalked], a
	call GetMapObject
	ld hl, MAPOBJECT_MOVEMENT
	add hl, bc
	ld a, [hl]
	ld d, a
	and a
	ret

.fail
	scf
	ret

RockSmashFromMenuScript:
	refreshmap
	special UpdateTimePals

RockSmashScript:
	callasm GetPartyNickname
	writetext UseRockSmashText
	closetext
	special WaitSFX
	playsound SFX_STRENGTH
	earthquake 84
	applymovementlasttalked MovementData_RockSmash
	disappear LAST_TALKED

	callasm RockMonEncounter
	readmem wTempWildMonSpecies
	iffalse .done
	randomwildmon
	startbattle
	reloadmapafterbattle
.done
	end

MovementData_RockSmash:
	rock_smash 10
	step_end

UseRockSmashText:
	text_far _UseRockSmashText
	text_end

TryCutOW::
	ld d, CUT
	call CheckPartyMove
	jr c, .cant_cut

	ld de, ENGINE_HIVEBADGE
	call CheckEngineFlag
	jr c, .cant_cut

	ld a, BANK(AskCutScript)
	ld hl, AskCutScript
	call CallScript
	scf
	ret

.cant_cut
	ld a, BANK(CantCutScript)
	ld hl, CantCutScript
	call CallScript
	scf
	ret

AskCutScript:
	opentext
	writetext AskCutText
	yesorno
	iffalse .declined
	callasm .CheckMap
	iftrue Script_Cut
.declined
	closetext
	end

.CheckMap:
	xor a
	ld [wScriptVar], a
	call CheckMapForSomethingToCut
	ret c
	ld a, TRUE
	ld [wScriptVar], a
	ret

AskCutText:
	text_far _AskCutText
	text_end

CantCutScript:
	jumptext CanCutText

CanCutText:
	text_far _CanCutText
	text_end
