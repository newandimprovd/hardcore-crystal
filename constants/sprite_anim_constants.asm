; sprite_anim_struct members (see macros/ram.asm)
rsreset
DEF SPRITEANIMSTRUCT_INDEX           rb ; 0
DEF SPRITEANIMSTRUCT_FRAMESET_ID     rb ; 1
DEF SPRITEANIMSTRUCT_ANIM_SEQ_ID     rb ; 2
DEF SPRITEANIMSTRUCT_TILE_ID         rb ; 3
DEF SPRITEANIMSTRUCT_XCOORD          rb ; 4
DEF SPRITEANIMSTRUCT_YCOORD          rb ; 5
DEF SPRITEANIMSTRUCT_XOFFSET         rb ; 6
DEF SPRITEANIMSTRUCT_YOFFSET         rb ; 7
DEF SPRITEANIMSTRUCT_DURATION        rb ; 8
DEF SPRITEANIMSTRUCT_DURATIONOFFSET  rb ; 9
DEF SPRITEANIMSTRUCT_FRAME           rb ; a
DEF SPRITEANIMSTRUCT_JUMPTABLE_INDEX rb ; b
DEF SPRITEANIMSTRUCT_VAR1            rb ; c
DEF SPRITEANIMSTRUCT_VAR2            rb ; d
DEF SPRITEANIMSTRUCT_VAR3            rb ; e
DEF SPRITEANIMSTRUCT_VAR4            rb ; f
DEF SPRITEANIMSTRUCT_LENGTH EQU _RS
DEF NUM_SPRITE_ANIM_STRUCTS EQU 10 ; see wSpriteAnimationStructs

; wSpriteAnimDict keys (see wram.asm)
; UnusedSpriteAnimGFX indexes (see data/sprite_anims/unused_gfx.asm)
	const_def
	const SPRITE_ANIM_DICT_DEFAULT      ; 0
	const_skip 4                        ; unused
	const SPRITE_ANIM_DICT_TEXT_CURSOR  ; 5
	const SPRITE_ANIM_DICT_GS_SPLASH    ; 6
	const SPRITE_ANIM_DICT_SLOTS        ; 7
	const SPRITE_ANIM_DICT_ARROW_CURSOR ; 8
DEF NUM_SPRITE_ANIM_GFX EQU const_value

; wSpriteAnimDict size (see wram.asm)
DEF NUM_SPRITEANIMDICT_ENTRIES EQU 10

; SpriteAnimObjects indexes (see data/sprite_anims/objects.asm)
	const_def
	const SPRITE_ANIM_OBJ_PARTY_MON                 ; 00
	const SPRITE_ANIM_OBJ_NAMING_SCREEN_CURSOR      ; 02
	const SPRITE_ANIM_OBJ_RED_WALK                  ; 0a
	const SPRITE_ANIM_OBJ_POKEGEAR_ARROW            ; 0d
	const SPRITE_ANIM_OBJ_EVOLUTION_BALL_OF_LIGHT   ; 13
	const SPRITE_ANIM_OBJ_LEAF                      ; 16
	const SPRITE_ANIM_OBJ_CUT_TREE                  ; 17
	const SPRITE_ANIM_OBJ_FLY_LEAF                  ; 18
	const SPRITE_ANIM_OBJ_HEADBUTT                  ; 1b
	const SPRITE_ANIM_OBJ_BLUE_WALK                 ; 1e
DEF NUM_SPRITE_ANIM_OBJS EQU const_value

; DoSpriteAnimFrame.Jumptable indexes (see engine/sprite_anims/functions.asm)
	const_def
	const SPRITE_ANIM_FUNC_NULL                      ; 00
	const SPRITE_ANIM_FUNC_PARTY_MON                 ; 01
	const SPRITE_ANIM_FUNC_PARTY_MON_SWITCH          ; 02
	const SPRITE_ANIM_FUNC_PARTY_MON_SELECTED        ; 03
	const SPRITE_ANIM_FUNC_NAMING_SCREEN_CURSOR      ; 05
	const SPRITE_ANIM_FUNC_POKEGEAR_ARROW            ; 0f
	const SPRITE_ANIM_FUNC_REVEAL_NEW_MON            ; 13
	const SPRITE_ANIM_FUNC_CUT_LEAVES                ; 15
	const SPRITE_ANIM_FUNC_FLY_FROM                  ; 16
	const SPRITE_ANIM_FUNC_FLY_LEAF                  ; 17
	const SPRITE_ANIM_FUNC_FLY_TO                    ; 18
DEF NUM_SPRITE_ANIM_FUNCS EQU const_value

; SpriteAnimFrameData indexes (see data/sprite_anims/framesets.asm)
	const_def
	const SPRITE_ANIM_FRAMESET_00                        ; 00
	const SPRITE_ANIM_FRAMESET_PARTY_MON                 ; 01
	const SPRITE_ANIM_FRAMESET_PARTY_MON_WITH_ITEM       ; 03
	const SPRITE_ANIM_FRAMESET_TEXT_ENTRY_CURSOR         ; 08
	const SPRITE_ANIM_FRAMESET_TEXT_ENTRY_CURSOR_BIG     ; 09
	const SPRITE_ANIM_FRAMESET_RED_WALK                  ; 11
	const SPRITE_ANIM_FRAMESET_STILL_CURSOR              ; 12
	const SPRITE_ANIM_FRAMESET_EVOLUTION_BALL_OF_LIGHT   ; 19
	const SPRITE_ANIM_FRAMESET_LEAF                      ; 1d
	const SPRITE_ANIM_FRAMESET_CUT_TREE                  ; 1e
	const SPRITE_ANIM_FRAMESET_HEADBUTT                  ; 25
	const SPRITE_ANIM_FRAMESET_BLUE_WALK                 ; 2d
DEF NUM_SPRITE_ANIM_FRAMESETS EQU const_value

; SpriteAnimOAMData indexes (see data/sprite_anims/oam.asm)
	const_def
	const SPRITE_ANIM_OAMSET_RED_WALK_1                  ; 00
	const SPRITE_ANIM_OAMSET_RED_WALK_2                  ; 01
	const SPRITE_ANIM_OAMSET_TEXT_ENTRY_CURSOR           ; 20
	const SPRITE_ANIM_OAMSET_TEXT_ENTRY_CURSOR_BIG       ; 21
	const SPRITE_ANIM_OAMSET_STILL_CURSOR                ; 2f
	const SPRITE_ANIM_OAMSET_EVOLUTION_BALL_OF_LIGHT_1   ; 3a
	const SPRITE_ANIM_OAMSET_EVOLUTION_BALL_OF_LIGHT_2   ; 3b
	const SPRITE_ANIM_OAMSET_PARTY_MON_WITH_ITEM_1       ; 3f
	const SPRITE_ANIM_OAMSET_PARTY_MON_WITH_ITEM_2       ; 40
	const SPRITE_ANIM_OAMSET_LEAF                        ; 4f
	const SPRITE_ANIM_OAMSET_TREE_1                      ; 50
	const SPRITE_ANIM_OAMSET_CUT_TREE_2                  ; 51
	const SPRITE_ANIM_OAMSET_CUT_TREE_3                  ; 52
	const SPRITE_ANIM_OAMSET_CUT_TREE_4                  ; 53
	const SPRITE_ANIM_OAMSET_HEADBUTT_TREE_2             ; 5b
	const SPRITE_ANIM_OAMSET_BLUE_WALK_1                 ; 63
	const SPRITE_ANIM_OAMSET_BLUE_WALK_2                 ; 64
DEF NUM_SPRITE_ANIM_OAMSETS EQU const_value

assert NUM_SPRITE_ANIM_OAMSETS <= FIRST_OAM_CMD, \
	"SPRITE_ANIM_OAMSET_* constants overlap oam*_command constants"
