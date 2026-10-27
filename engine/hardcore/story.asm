; Hardcore Crystal story: kill milestones, the rival's fall, the New Bark Town portal, endings.
; Everything here lives in one ROMX section ("Hardcore Story"); TrainerDeathScript reaches it with farsjump.

HC_CheckStory:
; After a kill: wScriptVar = 0 nothing happens, 1 = this was kill 200, otherwise the kind of the story boss that
; was just beaten (2 = the rival, 3 = the final boss), looked up by trainer class and id in HC_StoryBosses.
	ld hl, HC_StoryBosses
.loop
	ld a, [hli]
	cp -1
	jr z, .milestone
	ld b, a
	ld a, [hli]
	ld c, a
	ld a, [hli]
	ld d, a
	ld a, [wTempTrainerClass]
	cp b
	jr nz, .loop
	ld a, [wTempTrainerID]
	cp c
	jr nz, .loop
	ld a, d
	ld [wScriptVar], a
	ret

.milestone
	ld hl, wHCKillCount
	ld a, [hli]
	cp LOW(200)
	jr nz, .none
	ld a, [hl]
	cp HIGH(200)
	jr nz, .none
	ld a, 1
	ld [wScriptVar], a
	ret

.none
	xor a
	ld [wScriptVar], a
	ret

HC_StoryDispatch::
	ifequal 1, HC_Milestone200
	ifequal 2, HC_RivalFalls
	ifequal 3, HC_FinnFalls
	end

HC_Milestone200:
	setevent EVENT_HC_TIDAL_WAVE
	pause 20
	opentext
	writetext HC_TidalText1
	waitbutton
	writetext HC_TidalText2
	waitbutton
	writetext HC_TidalText3
	waitbutton
	writetext HC_TidalText4
	waitbutton
	writetext HC_TidalText5
	waitbutton
	closetext
	end

HC_RivalFalls:
	setevent EVENT_HC_RIVAL_FELL
	pause 20
	opentext
	writetext HC_RivalText1
	waitbutton
	checkevent EVENT_GOT_TOTODILE_FROM_ELM
	iftrue .Meganium ; the player took TOTODILE, so the rival had CHIKORITA
	checkevent EVENT_GOT_CHIKORITA_FROM_ELM
	iftrue .Typhlosion ; the player took CHIKORITA, so the rival had CYNDAQUIL
	getmonname STRING_BUFFER_3, FERALIGATR ; the player took CYNDAQUIL, so the rival had TOTODILE
	writetext HC_RivalGotText
	playsound SFX_CAUGHT_MON
	waitsfx
	waitbutton
	givepoke FERALIGATR, 75
	sjump .Back

.Meganium:
	getmonname STRING_BUFFER_3, MEGANIUM
	writetext HC_RivalGotText
	playsound SFX_CAUGHT_MON
	waitsfx
	waitbutton
	givepoke MEGANIUM, 75
	sjump .Back

.Typhlosion:
	getmonname STRING_BUFFER_3, TYPHLOSION
	writetext HC_RivalGotText
	playsound SFX_CAUGHT_MON
	waitsfx
	waitbutton
	givepoke TYPHLOSION, 75
.Back:
	setevent EVENT_HC_STOLEN_BACK
	writetext HC_RivalText3
	waitbutton
	writetext HC_RivalText4
	waitbutton
	writetext HC_RivalText5
	waitbutton
	writetext HC_RivalText6
	waitbutton
	writetext HC_RivalText7
	waitbutton
	writetext HC_RivalText8
	waitbutton
	closetext
	setevent EVENT_HC_CRATER
	setevent EVENT_HC_ELM_AT_RIM
	end

HC_RivalGotText:
	text "<PLAYER> took back"
	line "@"
	text_ram wStringBuffer3
	text "."
	done

HC_FinnFalls:
; The final boss is dead: the player wakes on the rim of the New Bark Town crater where PROF. ELM waits.
	setevent EVENT_HC_FINN_FELL
	pause 20
	opentext
	writetext HC_FinnText1
	waitbutton
	writetext HC_FinnText2
	waitbutton
	writetext HC_FinnText3
	waitbutton
	writetext HC_FinnText4
	waitbutton
	closetext
	special FadeOutToWhite
	playsound SFX_WARP_TO
	waitsfx
	warp NEW_BARK_TOWN, 10, 10
	end

; New Bark Town after the rival fell -----------------------------------------------------------

HC_PortalScript::
	checkevent EVENT_HC_CRATER
	iffalse .Closed
	opentext
	writetext HC_PortalText1
	waitbutton
	writetext HC_PortalAsk
	yesorno
	iffalse .No
	writetext HC_PortalGo
	waitbutton
	closetext
	special FadeOutToWhite
	playsound SFX_WARP_TO
	waitsfx
	warp DIS_GATE, 4, 6
	end

.No:
	writetext HC_PortalNo
	waitbutton
	closetext
	end

.Closed:
	end

HC_ElmRimScript::
	faceplayer
	opentext
	checkevent EVENT_HC_ENDED
	iftrue .Ended
	checkevent EVENT_HC_FINN_FELL
	iftrue .AfterFinn
	writetext HC_ElmText1
	waitbutton
	writetext HC_ElmText2
	waitbutton
	writetext HC_ElmText3
	waitbutton
	writetext HC_ElmText4
	waitbutton
	closetext
	end

.Ended:
	writetext HC_ElmDone
	waitbutton
	closetext
	end

.AfterFinn:
	writetext HC_ElmEnd1
	waitbutton
	; the stolen POKéMON was the rival's starter: its fully evolved form has to be in the party
	checkevent EVENT_GOT_TOTODILE_FROM_ELM
	iftrue .WantElderwood ; the player took TOTODILE, the rival had CHIKORITA
	checkevent EVENT_GOT_CHIKORITA_FROM_ELM
	iftrue .WantCaldera ; the player took CHIKORITA, the rival had CYNDAQUIL
	setval DEATHROLL ; the player took CYNDAQUIL, the rival had TOTODILE
	sjump .Check

.WantElderwood:
	setval ELDERWOOD
	sjump .Check

.WantCaldera:
	setval CALDERA
.Check:
	special FindPartyMonThatSpecies
	iftrue .TheEnd
	writetext HC_ElmEndNot
	waitbutton
	closetext
	end

.TheEnd:
	writetext HC_ElmEnd2
	waitbutton
	writetext HC_ElmEnd3
	waitbutton
	writetext HC_ElmEnd4
	waitbutton
	writetext HC_ElmEnd5
	waitbutton
	closetext
	setevent EVENT_HC_ENDED
	halloffame ; saves, hall of fame, credits; Continue then spawns in the mansion bedroom (intro_menu.asm)
	end

INCLUDE "data/hardcore/story_bosses.asm"
INCLUDE "data/hardcore/story_text.asm"
