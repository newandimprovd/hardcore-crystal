"""Text objects for generated maps."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from textgen import emit_text, wrap_pages, esc  # noqa: E402


class Text:
    def __init__(self, s):
        self.s = s

    def emit(self, label):
        return emit_text(label, self.s)


def pool_asm(label, items, owner):
    """A text pool: a text_asm entry point that picks one entry from a table by trainer class and id,
    then the table and the texts. Needs its own copy of the picker so it stays in its own bank."""
    n = len(items)
    o = [f"{label}::", "\ttext_asm", "\tpush bc", f"\tld hl, {label}_Table", f"\tld b, {n}",
         "\tld a, [wTempTrainerID]", "\tld c, a", "\tadd a", "\tadd a", "\tadd c", "\tld c, a",
         "\tld a, [wTempTrainerClass]", "\tswap a", "\tadd c",
         f".mod_{label}", "\tcp b", f"\tjr c, .got_{label}", "\tsub b", f"\tjr .mod_{label}",
         f".got_{label}", "\tld e, a", "\tld d, 0", "\tadd hl, de", "\tadd hl, de", "\tld a, [hli]",
         "\tld h, [hl]", "\tld l, a", "\tpop bc", "\tret", "", f"{label}_Table:"]
    for i in range(n):
        o.append(f"\tdw {label}_{i}")
    o.append("")
    for i, t in enumerate(items):
        o.append(emit_text(f"{label}_{i}", t))
    return "\n".join(o) + "\n"
