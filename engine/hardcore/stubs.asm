; Hardcore Crystal: scripts that vanilla map files used to export. The maps are gone (tools/hardcore/stub_maps.py), the engine
; code for their key items is still linked, so these end immediately.

SECTION "Hardcore Stubs", ROMX

BasementDoorScript::
CardKeySlotScript::
WateredWeirdTreeScript::
	end

; Link, mobile, tower, trainer rankings and roaming code of the vanilla battle engine. Nothing reaches these, they end at once.
Function100da5::
Function100dd8::
StartMobileInactivityTimer::
Mobile_PrintOpponentBattleMessage::
Mobile_PartyMenuSelect::
Mobile_LoadBattleMenu::
MobileBattleMonMenu::
Mobile_MoveSelectionScreen::
BattleTowerText::
_LinkBattleSendReceiveAction::
ShowLinkBattleParticipants::
_ShowLinkBattleParticipants::
DetermineLinkBattleResult::
BackupGSBallFlag::
StubbedTrainerRankings_AddToBattlePayouts::
StubbedTrainerRankings_Battles::
StubbedTrainerRankings_ColosseumDraws::
StubbedTrainerRankings_ColosseumLosses::
StubbedTrainerRankings_ColosseumWins::
StubbedTrainerRankings_HookedEncounters::
StubbedTrainerRankings_LinkBattles::
StubbedTrainerRankings_TrainerBattles::
StubbedTrainerRankings_WildBattles::
UpdateRoamMons::
GivePokerusAndConvertBerries::
	ret
