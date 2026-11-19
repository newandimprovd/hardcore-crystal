Reference ROM study tools (alpha 3.1 to 3.2 study pass).

- `boot.py`: opens a ROM in PyBoy headless (`boot("c16" | "grandia" | "van")`), `press`, `shot`.
- `drive.py`: key sequences, save states, `sheet` (contact sheets), `pos` (player map/x/y, valid for crystal16-bit only: wMapGroup at $dc64 in bank 1).
- `tilestats.py`: `analyze(pb)` reads the visible background (map, attributes, both VRAM banks) and returns unique tiles,
  unique pixel tiles after flip folding, unique 2x2 groups, palettes used, flipped cells, sprite count and colours on screen.

The scripts keep the reference ROM paths of the session that made them. Change `ROMS` in `boot.py` for another checkout.
Findings and ideas are in `docs/REFERENCE_STUDY.md`.
