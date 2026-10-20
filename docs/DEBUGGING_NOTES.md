# Debugging notes for the Crystal hack

How to find where code lives
1. grep the disassembly for the script command or label (for example Script_reloadmap, TextCommand_START_ASM, AddOutdoorSprites) and read the whole routine before editing.
2. Confirm the real address in the built .sym file (bank:address label) so emulator hooks can target it.
3. In the emulator dump WRAM, VRAM and OAM (wMap1Object, wUsedSprites, wObjectStructs, tile data at 0x8000) to see what the engine actually holds.

How to trace a bug in PyBoy 2.7
- Use pb.hook_register(bank, addr, callback, ctx). The bank must be an integer. Use 0 for home code below 0x4000 and the real bank above 0x4000.
- Hook RunScriptCommand (bank 0x25) and print wScriptBank, wScriptPos and the byte there to log every script command in order.
- Hook suspect routines (HC_PrepareDeath, GetTrainerName, TextCommand_START_ASM) and compare which ones fire. The last one that fired is where the bug is.
- Put faulthandler.dump_traceback_later(N, exit=True) at the top of test scripts so a stalled tick reports instead of hanging.
- A tick that never returns usually means the game wrote garbage (bad text pointer or bad cursor), not that the emulator is broken.

Test builds
- Build a copy with RGBASMFLAGS containing -D _TESTMODE. It generates test_config.asm, spawns on the target map and gives a ready party and key items. Keep the real build untouched.
- Screenshot sheets (every press) make text bugs obvious. Zoom screenshots 4x for sprite bugs.

Bug catalogue
- text_asm blocks run inline in the text engine. bc is the tilemap cursor and must be preserved (push bc / pop bc). Return with hl pointing at the next text.
- A string before text_asm or text_ram needs an explicit "@" terminator, otherwise PlaceString runs on into code bytes.
- Bare para, line and cont bytes are only valid inside a string. Start such blocks with text_start.
- Outdoor maps load a fixed OutdoorSprites list per map group, not the map objects. A new sprite must be added in AddOutdoorSprites (done for SPRITE_CORPSE when the killer is revealed).
- reloadmap does not rebuild object structs. After changing a map object, DeleteObjectStruct then UnmaskCopyMapObjectStruct on it.
- Species IDs are one byte. IDs 1 to 251 are used, $fc is skipped and $fd is EGG.
