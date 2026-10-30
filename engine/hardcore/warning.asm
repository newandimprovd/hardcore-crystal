; Shown once at the start of a new game (see NewGame in engine/menus/intro_menu.asm).

HC_AdultWarning::
	call ClearTilemap
	hlcoord 0, 0
	ld b, 13
	ld c, 18
	call Textbox
	hlcoord 1, 2
	ld de, .Text
	call PlaceString
	hlcoord 18, 17
	ld [hl], '▼'
	call WaitBGMap
	call WaitPressAorB_BlinkCursor
	call ClearTilemap
	ret

.Text:
	db   "ADULTS ONLY!"
	db   "<NEXT><NEXT>Crude humor and"
	db   "<NEXT>mature themes."
	db   "<NEXT><NEXT>Players 18 and up."
	db   "@"
