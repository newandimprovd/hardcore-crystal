TalkToTrainerScript::
	faceplayer
	trainerflagaction CHECK_FLAG
	iftrue .AlreadyBeaten
	loadtemptrainer
	encountermusic
	sjump StartBattleWithMapTrainerScript

.AlreadyBeaten:
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
	checkevent EVENT_KILLER_REVEALED
	iftrue TrainerDeathScript
	; Hardcore: the first trainer ever beaten is TIMMY in Cherrygrove, and that is the reveal.
	sjump FirstKillRevealScript

AlreadyBeatenTrainerScript:
	scripttalkafter
