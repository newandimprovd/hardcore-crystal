#!/usr/bin/env python3
"""Death presentation text generator.

Writes data/hardcore/death_causes.asm (included at the end of engine/hardcore/trainer_death.asm, same bank as the script):
  HC_CauseNN / HC_CauseTable  random "cause of death" lines (shown rarely, see HC_DeathMode)
  HC_FlavorNN / HC_FlavorTable what else the body had (shown rarely)
  HC_BodyNN / HC_BodyTable    what happens when the player talks to a corpse
  HC_UniqueDeathScript         script branches: a boss class gets its own dying words (farwritetext, text lives in "Hardcore Death Texts")
and data/hardcore/death_unique.asm (the unique texts in their own floating ROMX section, plus the class table HC_UniqueDeathTable).

Tone (alpha 1 feedback): most people die quietly (no text), the few lines that exist are dry, adult and a little cruel, never repeated for
every kill."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W = 18  # text box columns

# --- random causes: continue the sentence "<NAME> ..." -------------------------------------------------------------
CAUSES = [
    "bled out at the side of the road. Nobody slowed down.",
    "died owing money to people who do not forgive.",
    "was loved by no one in particular, and it showed.",
    "stopped. The rest is paperwork.",
    "died in the middle of a sentence.",
    "met the only honest thing in Johto. It was you.",
    "looked at the sky and asked for a reason. There was none.",
    "will be missed by a landlord.",
    "died the way they lived. Poorly, and in public.",
    "prayed. Something answered. It was you.",
    "had a family. Do not think about it.",
    "died believing they were the main character.",
    "was an extra. This was their one scene.",
    "wanted a good death. This was not one.",
    "was eleven days from a promotion.",
    "went down swinging. The swing missed.",
    "made peace with it. You did not ask.",
    "left behind a loan and an unlocked door.",
    "died without ever being touched by anyone kind.",
    "was never going to leave Johto alive anyway.",
    "had a will. Nobody will read it.",
    "exhaled, and did not inhale.",
    "was somebody's whole world. For a while.",
    "died a virgin. The grass does not judge. You do.",
    "died thinking about somebody else's wife.",
    "kept a ring in a pocket. Someone else wears it now.",
    "died with their trousers on. The real tragedy.",
    "was told it gets better. It did not.",
    "tried to say your name. Got the first letter.",
    "died holding a phone with no messages.",
    "had plans for Sunday.",
    "begged. It did not help. It rarely does.",
    "died happy. That was the worst part.",
    "was a good person, probably. Hard to tell now.",
    "did not believe in anything. Now they believe in the ground.",
    "was just doing their job. So are you.",
    "got what the world gives to everyone eventually. Early.",
    "died exactly as significant as everyone else.",
    "forgave you. You did not need it.",
    "asked if it would hurt. It did, briefly.",
]

# --- loot extras (1 in 5 kills) ----------------------------------------------------------------------------------
FLAVORS = [
    "Also a photo of someone smiling. Not the owner.",
    "The rest was IOUs.",
    "A lottery ticket. Losing.",
    "A note that said sorry mom. Unsent.",
    "A condom. Unopened. Expired.",
    "A phone number written on a palm.",
    "A key to a door you will never find.",
    "Half a sandwich. You ate it.",
    "A prayer card. The saint had been scratched out.",
    "A wedding photo. Not their wedding.",
    "A receipt for something expensive. Unpaid.",
    "A list titled THINGS TO DO. Item one was crossed out. It was living.",
    "Nothing else. Not even a reason.",
    "A child's drawing of a stick figure holding a stick figure.",
    "A membership card. The club had already closed.",
    "Three vitamins and a lot of regret.",
]

# --- bodies (talking to a corpse) ---------------------------------------------------------------------------------
BODIES = [
    "Still dead.",
    "It has nothing more to say.",
    "<PLAYER> poked the body. It did not poke back.",
    "The body is cooling. So is the conversation.",
    "Flies have started to arrive. They are polite about it.",
    "Somebody will be looking for this one tonight.",
    "A good listener, finally.",
    "It looks smaller than it did when it was angry.",
    "There is nothing here that is not already yours.",
    "<PLAYER> felt something. It passed.",
    "This one still has its shoes on. Take them off later.",
    "Dead people do not owe you anything. It is the only thing you have in common.",
    "The eyes are open. They are not looking at you. That is a relief.",
    "Not even a last word. A rare kindness.",
    "It will not hold a grudge. It does not have the equipment.",
    "You could say a few words. You decide to use that time better.",
]

# --- unique last words: boss class -> text --------------------------------------------------------------------------
UNIQUE = [
    ("T_DEACON", "The DEACON looked up from the floor. Bless you, he said. Bless the collection. He died counting."),
    ("T_COPCHIEF", "CHIEF BRAD said he had a pension. He said it twice. The second time he meant it as a prayer."),
    ("T_MONSIGNOR", "The MONSIGNOR smiled with the half of his face that still worked. The cathedral forgives everything, he said. It has a large budget."),
    ("G_REEVE", "REEVE OTTO coughed. There are no locks in the Grove, he said. Should have been a clue. Then he had no more clues to give."),
    ("G_ELDRESS", "ELDER FERN took your hand and held it. We fed you, she said. It was the one thing we got right."),
    ("G_MATRIARCH", "The MATRIARCH said she had expected you sooner. She said a lot of things after that. Nobody wrote them down."),
    ("U_MADDOC", "DR AXIOM: Remarkable. The subject kills without a hypothesis. He asked for a notebook. There was not enough time."),
    ("U_WARDBOT", "IRONWARDEN's voice slowed. Citizen. Love. Is not. In the. Budget. The lights went out of its eyes in order, left first."),
    ("U_MAYOR", "THE MAYOR hissed. Every death is a rounding error, it said. It rounded itself down to zero."),
    ("L_CLINICIAN", "DR LETHE said you could forget all of this by Friday. We have a treatment. She forgot to bill you."),
    ("L_MANAGER", "MGR KAI asked you to rate your experience. He did not wait for the rating."),
    ("D_WARDEN", "The GATEKEEPER put the key in your hand and died on his feet. The gate had never been locked."),
    ("D_DEMON", "The BETRAYER laughed from the bottom of the ice. You think I am the worst one down here, he said."),
]


def wrap(s, first=W):
    words, lines, cur = s.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        width = len(cand.replace("<PLAYER>", "xxxxxxx").replace("#", "#"))
        if width <= (first if not lines else W):
            cur = cand
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def block(label, s, kind="text", first=W, para_start=False):
    """kind 'text': starts with `text`, continues with `cont`; kind 'flavor': starts with text_start + para; kind 'para': paragraph per 3 lines."""
    ls = wrap(s, first)
    out = [f"{label}:"]
    if kind == "flavor":
        out.append("\ttext_start")
        out.append(f'\tpara "{ls[0]}"')
        if len(ls) > 1:
            out.append(f'\tline "{ls[1]}"')
        for l in ls[2:]:
            out.append(f'\tcont "{l}"')
    elif kind == "story":
        # a long passage: pages of two lines (text, line, para, line, ...)
        out.append(f'\ttext "{ls[0]}"')
        for i, l in enumerate(ls[1:], 1):
            out.append(f'\t{"line" if i % 2 == 1 else "para"} "{l}"')
    else:
        out.append(f'\ttext "{ls[0]}"')
        for l in ls[1:]:
            out.append(f'\tcont "{l}"')
    out.append("\tdone")
    return "\n".join(out) + "\n"


def main():
    o = ["; generated by gen_death.py. Do not edit by hand.", ""]
    for i, c in enumerate(CAUSES):
        o.append(block(f"HC_Cause{i:02d}", c))
    o.append("HC_CauseTable:")
    o += [f"\tdw HC_Cause{i:02d}" for i in range(len(CAUSES))]
    o.append(f"DEF HC_NUM_CAUSES EQU {len(CAUSES)}\n")
    for i, c in enumerate(FLAVORS):
        o.append(block(f"HC_Flavor{i:02d}", c, "flavor"))
    o.append("HC_FlavorTable:")
    o += [f"\tdw HC_Flavor{i:02d}" for i in range(len(FLAVORS))]
    o.append(f"DEF HC_NUM_FLAVORS EQU {len(FLAVORS)}\n")
    for i, c in enumerate(BODIES):
        o.append(block(f"HC_Body{i:02d}", c))
    o.append("HC_BodyTable:")
    o += [f"\tdw HC_Body{i:02d}" for i in range(len(BODIES))]
    o.append(f"DEF HC_NUM_BODIES EQU {len(BODIES)}\n")
    # unique death branches (script commands, same bank as the death script)
    o.append("HC_UniqueDeathScript:")
    o.append("; called with scall; wScriptVar = 2 + index in HC_UniqueDeathTable; `end` returns to the caller")
    for i, (cls, _) in enumerate(UNIQUE):
        o.append(f"\tifequal {2 + i}, .u{i}")
    o.append("\tend")
    for i, (cls, _) in enumerate(UNIQUE):
        o.append(f".u{i}\n\topentext\n\tfarwritetext HC_UniqueDeath{i:02d}\n\twaitbutton\n\tclosetext\n\tend")
    o.append("")
    (ROOT / "data/hardcore/death_causes.asm").write_text("\n".join(o) + "\n")

    u = ["; generated by gen_death.py. Do not edit by hand.", "", 'SECTION "Hardcore Death Texts", ROMX', ""]
    u.append("HC_UniqueDeathTable:  ; trainer class, one row per unique death; the row number + 2 is the wScriptVar value")
    for cls, _ in UNIQUE:
        u.append(f"\tdb {cls}")
    u.append("\tdb -1\n")
    for i, (cls, t) in enumerate(UNIQUE):
        u.append(block(f"HC_UniqueDeath{i:02d}", t, "story"))
    (ROOT / "data/hardcore/death_unique.asm").write_text("\n".join(u) + "\n")
    print("causes", len(CAUSES), "flavors", len(FLAVORS), "bodies", len(BODIES), "unique", len(UNIQUE))


if __name__ == "__main__":
    main()
