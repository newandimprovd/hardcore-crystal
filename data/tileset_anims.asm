MACRO tileframe
	if _NARG == 2
		dw \2 ; argument
	else
		dw 0
	endc
	dw \1 ; function
ENDM

Tileset0Anim:
	tileframe AnimateWaterTile,        vTiles2 tile $14
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe AnimateWaterPalette
	tileframe WaitTileAnimation
	tileframe AnimateFlowerTile
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe StandingTileFrame8
	tileframe DoneTileAnimation

TilesetJohtoAnim:
	tileframe AnimateWaterTile,        vTiles2 tile $14
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe AnimateWaterPalette
	tileframe WaitTileAnimation
	tileframe AnimateFlowerTile
	tileframe AnimateWhirlpoolTile,    WhirlpoolFrames1
	tileframe AnimateWhirlpoolTile,    WhirlpoolFrames2
	tileframe AnimateWhirlpoolTile,    WhirlpoolFrames3
	tileframe AnimateWhirlpoolTile,    WhirlpoolFrames4
	tileframe WaitTileAnimation
	tileframe StandingTileFrame8
	tileframe DoneTileAnimation

TilesetEliteFourRoomAnim:
	tileframe AnimateLavaBubbleTile2
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe AnimateLavaBubbleTile1
	tileframe WaitTileAnimation
	tileframe StandingTileFrame8
	tileframe DoneTileAnimation

TilesetCaveAnim:
	tileframe ReadTileToAnimBuffer,    vTiles2 tile $14
	tileframe FlickeringCaveEntrancePalette
	tileframe ScrollTileRightLeft,     wTileAnimBuffer
	tileframe FlickeringCaveEntrancePalette
	tileframe WriteTileFromAnimBuffer, vTiles2 tile $14
	tileframe FlickeringCaveEntrancePalette
	tileframe AnimateWaterPalette
	tileframe FlickeringCaveEntrancePalette
	tileframe ReadTileToAnimBuffer,    vTiles2 tile $40
	tileframe FlickeringCaveEntrancePalette
	tileframe ScrollTileDown,          wTileAnimBuffer
	tileframe FlickeringCaveEntrancePalette
	tileframe ScrollTileDown,          wTileAnimBuffer
	tileframe FlickeringCaveEntrancePalette
	tileframe ScrollTileDown,          wTileAnimBuffer
	tileframe FlickeringCaveEntrancePalette
	tileframe WriteTileFromAnimBuffer, vTiles2 tile $40
	tileframe FlickeringCaveEntrancePalette
	tileframe DoneTileAnimation

TilesetTitheAnim: ; HC-ART
TilesetGroveAnim: ; HC-ART
TilesetAxiomAnim: ; HC-ART
TilesetLotusAnim: ; HC-ART
TilesetDisAnim: ; HC-ART
TilesetHouseAnim:
TilesetPlayersHouseAnim:
TilesetPokecenterAnim:
TilesetGateAnim:
TilesetLabAnim:
TilesetMartAnim:
TilesetMansionAnim:
TilesetPlayersRoomAnim:
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe WaitTileAnimation
	tileframe DoneTileAnimation
