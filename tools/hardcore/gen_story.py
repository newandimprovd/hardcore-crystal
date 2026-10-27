#!/usr/bin/env python3
"""Hardcore Crystal story text generator (stage 3): the first-kill reveal narration."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from textgen import emit_text

ROOT = Path(__file__).resolve().parents[2]

REVEAL = [
    "<PLAYER> looked at the body. Then at <PLAYER>'s own hands. Then at the POKé BALL, "
    "which had been smiling the whole time.",

    "A memory arrived. Then another. Then all of them, like a drawer of knives falling open "
    "in a very quiet kitchen.",

    "Every route. Every trainer. Every handshake after the battle that lasted slightly too long.",

    "<PLAYER> was never a trainer who beat other trainers. <PLAYER> was a trainer who stopped them. "
    "For good. As a hobby.",

    "Somewhere far away, the map noticed, and quietly stopped being the map.",

    "From now on every trainer you beat will die. Kills are counted. Try to enjoy the number.",
]


STORY = {
    # kill 200 (the Monsignor): the radio
    "TidalText1": "A radio on the desk crackled to life, the way radios do at funerals.",
    "TidalText2": "BULLETIN: A tidal wave has struck NEW BARK TOWN. Officials describe the town as ruined and slightly destroyed.",
    "TidalText3": "PROF. ELM's lab has reportedly entered a new relationship with the sea. The professor is unavailable for comment, but his hat was found.",
    "TidalText4": "Police ask anyone with information about the many bodies along the road to please keep it to themselves.",
    "TidalText5": "<PLAYER> switched the radio off. Home was a long walk back now. It was also, in all likelihood, a pond.",
    # kill 800 (the rival): the stolen POKéMON, the maids, the crater
    "RivalText1": "A POKé BALL had rolled out of the rival's coat and stopped against <PLAYER>'s shoe. It was warm. It had been stolen from PROF. ELM's lab so long ago that it no longer felt guilty.",
    "RivalText3": "The stolen POKéMON looked at <PLAYER>, at the body, at the wine-colored carpet, and decided not to ask.",
    "RivalText4": "The mansion's staff had been standing very still, the way staff do when the boss is on the floor. A maid in a very small apron set down her tray.",
    "RivalText5": "'Welcome home,' she said, with the warmth of someone who had updated her CV about four minutes ago.",
    "RivalText6": "The house, the wine cellar and a large number of pending legal problems now belonged to <PLAYER>.",
    "RivalText7": "Somewhere a radio said: NEW BARK TOWN is now a crater. A portal has opened at its center. Officials describe it as 'a lot'.",
    "RivalText8": "The POKéMON had to go home to PROF. ELM. Home was a crater. It was still home.",
    # the crater portal
    "PortalText1": "A swirl of unfinished weather hangs in the crater. It hums like a fridge that has seen things.",
    "PortalAsk": "Step into the swirl?",
    "PortalGo": "<PLAYER> stepped in. The world folded politely.",
    "PortalNo": "<PLAYER> stepped back. The swirl waited. It has all the time there is.",
    "PortalClosed": "Nothing here but wet ground and a very strong smell of the sea.",
    # Elm on the rim of the crater, before the end
    "ElmText1": "ELM: <PLAYER>! I got out in time. The lab did not. Neither did my hat. The hat was a loss.",
    "ElmText2": "ELM: That swirl opened the night the town went. Things walk out of it. Things walk into it. Nobody comes back the same, except the hat.",
    "ElmText3": "ELM: You carry my stolen POKéMON? Fully grown, it would return the lab to me in spirit. Bring it back once it has finished evolving.",
    "ElmText4": "ELM: Whatever is on the other side of that swirl, it is why this happened. The nice kind of 'why'. The old-man kind.",
    # the final boss falls (Area 5): the player wakes on the crater rim
    "FinnText1": "FINNEGAN's dream ended in the middle of a sentence, as dreams about the end of the world are required to.",
    "FinnText2": "The ice of JUDECCA let go of everything it was holding. For a moment that included <PLAYER>.",
    "FinnText3": "Then it was wet ground, crater air and a very large sky. NEW BARK TOWN. Behind <PLAYER> the swirl had stopped humming.",
    "FinnText4": "PROF. ELM was waiting on the rim of the crater. He was holding a hat. It was not the same hat.",
    # Elm after the final boss: the starter has to be fully evolved and in the party
    "ElmEnd1": "ELM: <PLAYER>. The swirl stopped humming. Whatever was on the other side has finished its sentence.",
    "ElmEndNot": "ELM: Where is my POKéMON? The stolen one. It has to be fully grown and it has to be with you. Come back when it is. I'll be here. I have a crater to sit on.",
    "ElmEnd2": "ELM: There it is. Fully grown. It looks at me the way it did when it was small. With suspicion and forgiveness, in that order.",
    "ElmEnd3": "ELM: I used to hand these out to hopeful kids. You were one of them, once. I think. The records are wet.",
    "ElmEnd4": "ELM: Keep it. A lab is only a crater with paperwork. Go home, <PLAYER>. The house on the hill is yours. The maids will have made the bed.",
    "ElmEnd5": "<PLAYER> walked home. It was a long walk. Somewhere behind, a hat was lowered, and a town did not applaud.",
    "ElmDone": "ELM: The lab will be rebuilt. With a moat. Come by any time, if there is a time.",
}


def main():
    out = ["; Generated by tools/hardcore/gen_story.py. Do not edit by hand.\n"]
    for i, t in enumerate(REVEAL, 1):
        out.append(emit_text(f"HC_RevealText{i}", t))
    (ROOT / "data/hardcore/reveal_text.asm").write_text("\n".join(out))
    print("reveal text written:", len(REVEAL), "blocks")
    out = ["; Generated by tools/hardcore/gen_story.py. Do not edit by hand.\n"]
    for name, text in STORY.items():
        out.append(emit_text("HC_" + name, text))
    (ROOT / "data/hardcore/story_text.asm").write_text("\n".join(out))
    print("story text written:", len(STORY), "blocks")


if __name__ == "__main__":
    main()
