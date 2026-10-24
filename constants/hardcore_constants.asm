; Hardcore Crystal constants

; Trainer ids at or above this value are generated trainers: their parties and names live in
; separate ROM banks (data/hardcore/gen_trainer_data.asm, written by tools/hardcore/gen_areas.py).
; Ids below it are the vanilla parties in data/trainers/parties.asm.
DEF HC_GEN_ID_BASE EQU 128
