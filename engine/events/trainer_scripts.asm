TalkToTrainerScript::
	faceplayer
	trainerflagaction CHECK_FLAG
	iftrue .AlreadyBeaten
	loadtemptrainer
	encountermusic
	sjump StartBattleWithMapTrainerScript

.AlreadyBeaten:
	callasm HC_IsSafeGroup
	iftrue AlreadyBeatenTrainerScript ; PURGATORIO: nobody dies, the beaten stay standing and talk
	checkevent EVENT_KILLER_REVEALED
	iftrue DeadTrainerTalkScript
	sjump AlreadyBeatenTrainerScript

SeenByTrainerScript::
	loadtemptrainer
	encountermusic
	showemote EMOTE_SHOCK, LAST_TALKED, 30
	callasm TrainerWalkToPlayer
	applymovementlasttalked wMovementBuffer
	writeobjectxy LAST_TALKED
	faceobject PLAYER, LAST_TALKED
	sjump StartBattleWithMapTrainerScript

StartBattleWithMapTrainerScript:
	opentext
	trainertext TRAINERTEXT_SEEN
	waitbutton
	closetext
	loadtemptrainer
	startbattle
	reloadmapafterbattle
	trainerflagaction SET_FLAG
	loadmem wRunningTrainerBattleScript, -1
	callasm HC_IsSafeGroup
	iftrue HC_SafeTrainerDone ; PURGATORIO: a plain fight, no death and no kill count
	checkevent EVENT_KILLER_REVEALED
	iftrue TrainerDeathScript
	; Hardcore: the first trainer ever beaten is TIMMY in Cherrygrove, and that is the reveal.
	sjump FirstKillRevealScript

AlreadyBeatenTrainerScript:
	scripttalkafter

HC_SafeTrainerDone:
	end

HC_IsSafeGroup:
; wScriptVar = 1 in the PURGATORIO map group (see engine/hardcore/trainer_death.asm for the rest of the death rules).
	ld a, [wMapGroup]
	cp MAPGROUP_PURG
	ld a, 0
	jr nz, .store
	inc a
.store
	ld [wScriptVar], a
	ret
