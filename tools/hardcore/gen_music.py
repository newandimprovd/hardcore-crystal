#!/usr/bin/env python3
"""Eight original ambient songs, composed by rules and written as pokecrystal music assembly.

The brief: a long, quiet, Lavender-Town-style loop that does not get boring.  So every song is a slow modal piece
with a few sparse voices and lots of silence, 3 to 4 minutes long before it comes round again, and every phrase in it is
derived from a small motif by transformations chosen with a seeded random generator, so no bar repeats.  Three channels:
  channel 1 (pulse)  the foreground: bell-like phrases, or regular ticks, or a few lone notes
  channel 2 (pulse)  a slow pad: one note at a time rolling through the tones of the current chord
  channel 3 (wave)   a drone or toll on the root of the current chord, an octave below where the pulses would sound it
All three follow the same chord plan, section by section, so whatever the dice do they stay in one harmony.

Writes (deterministic):  audio/hc_music.asm  audio/hc_music_pointers.asm  constants/hc_music_constants.asm  docs/MUSIC.md
Usage:  python3 tools/hardcore/gen_music.py [--report]
"""
import os
import random
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
NAMES = ["C_", "C#", "D_", "D#", "E_", "F_", "F#", "G_", "G#", "A_", "A#", "B_"]
SPEED = 12  # the engine multiplies it with the note length: a unit lasts SPEED * tempo / 256 frames (larger tempo = SLOWER, "tempo is effectively length")
TIME = 2  # units per beat: the phrases below are written in beats of about half a second, the engine's units are about a quarter second
SECTION = 48 * TIME  # units per section
MAX_NOTE = 16  # the engine counts a note in a byte of frames: SPEED * 16 * tempo / 256 must stay below 256 frames (4.2 seconds)


def unit_frames(song):
    return SPEED * song["tempo"] / 256.0


def loop_seconds(song):
    return SECTION * len(song["prog"]) * unit_frames(song) / 60.0


def pitch(scale, root, base_oct, degree):
    """Absolute pitch (octave * 12 + semitone) of a scale degree; degrees outside 0..len-1 wrap into other octaves."""
    o, i = divmod(degree, len(scale))
    return base_oct * 12 + root + scale[i] + 12 * o


# ---------------------------------------------------------------------------------------------- the songs
# root: pitch class of the key note; scale: semitones; prog: chord root (scale degree) of each section;
# ch1/ch2/ch3: style names (see below); density: rest multiplier per section (bigger = sparser)
SONGS = [
    dict(key="ROAD", label="HcRoad", name="The Road", tempo=280, root=9, scale=[0, 3, 5, 7, 10],
         prog=[0, 0, 2, 0, 3, 0, 2, 4], density=[1.0, 1.3, 0.8, 1.5, 1.0, 1.2, 0.9, 1.4],
         ch1="bells", ch2="pad", ch3="drone", bell_oct=4, pad_oct=3, bass_oct=2, duty1=2, duty2=1, wave=1,
         motifs=[[(0, 3), (2, 2), (1, 5)], [(0, 2), (-1, 2), (0, 2), (2, 6)], [(3, 4), (2, 2), (0, 6)]],
         pan1=(False, True), pan2=(True, False), vib2=(8, 3, 4),
         use="the Crossroads and the lone trail north of Cherrygrove",
         mood="wind over a road nobody maintains"),
    dict(key="TITHE", label="HcTithe", name="The Tithe", wavevol=2, tempo=300, root=2, scale=[0, 2, 3, 5, 7, 9, 10],
         prog=[0, 0, 4, 0, 3, 0, 5, 4], density=[1.0, 1.4, 0.9, 1.2, 1.0, 1.6, 0.8, 1.3],
         ch1="bells", ch2="pad", ch3="toll", bell_oct=4, pad_oct=3, bass_oct=2, duty1=0, duty2=2, wave=2,
         motifs=[[(0, 4), (3, 4)], [(0, 3), (4, 3), (2, 6)], [(4, 3), (3, 3), (2, 3), (0, 7)]],
         pan1=(True, True), pan2=(False, True), vib2=(10, 2, 5),
         use="the Tithe: Lowtown, Midtown and the Parish",
         mood="a church bell tolling over an accounting office"),
    dict(key="GROVE", label="HcGrove", name="The Grove", tempo=270, root=7, scale=[0, 2, 4, 5, 7, 9, 10],
         prog=[0, 3, 0, 4, 0, 5, 3, 0], density=[1.0, 0.8, 1.2, 0.9, 1.4, 0.8, 1.1, 1.5],
         ch1="bells", ch2="pad", ch3="drone", bell_oct=4, pad_oct=3, bass_oct=2, duty1=1, duty2=2, wave=3,
         motifs=[[(0, 2), (1, 2), (2, 4)], [(2, 2), (4, 2), (3, 2), (2, 6)], [(0, 3), (2, 3), (4, 3), (2, 5)]],
         pan1=(True, False), pan2=(False, True), vib2=(6, 2, 3),
         use="the Grove: the Commune, the Orchard and the Great Hearth",
         mood="warm, a little too warm, a drone that hums along"),
    dict(key="AXIOM", label="HcAxiom", name="The Axiom", wavevol=2, tempo=262, root=0, scale=[0, 2, 4, 6, 8, 10],
         prog=[0, 0, 3, 0, 2, 0, 4, 0], density=[1.0, 1.2, 0.9, 1.1, 1.0, 1.3, 0.8, 1.2],
         ch1="ticks", ch2="pad", ch3="pulse", bell_oct=5, pad_oct=3, bass_oct=2, duty1=0, duty2=2, wave=0,
         motifs=[[(0, 1)]], period=7, bass_period=5,
         pan1=(True, False), pan2=(False, True), vib2=(0, 0, 0),
         use="Axiom: the Outskirts, Central and the Mayoralty",
         mood="a machine that counts in sevens while the bass counts in fives"),
    dict(key="LOTUS", label="HcLotus", name="The Lotus", tempo=320, root=0, scale=[0, 2, 4, 6, 7, 9, 11],
         prog=[0, 1, 0, 3, 0, 4, 1, 0], density=[1.2, 1.0, 1.4, 0.9, 1.3, 1.0, 1.5, 0.9],
         ch1="bells", ch2="pad", ch3="drone", bell_oct=4, pad_oct=3, bass_oct=2, duty1=2, duty2=0, wave=2, shimmer=True,
         motifs=[[(0, 5), (2, 3), (4, 8)], [(4, 3), (2, 3), (1, 3), (0, 7)], [(0, 3), (3, 3), (5, 3), (4, 6)]],
         pan1=(False, True), pan2=(True, False), vib2=(4, 3, 3),
         use="Lotus: the Coast, the Boardwalk and the Hilltop",
         mood="a lounge singer who left a long time ago"),
    dict(key="DIS", label="HcDis", name="The City of Dis", wavevol=2, tempo=330, root=4, scale=[0, 1, 4, 5, 7, 8, 10],
         prog=[0, 0, 1, 0, 5, 0, 1, 0], density=[1.0, 1.5, 1.0, 1.8, 0.9, 1.4, 1.1, 1.6],
         ch1="bells", ch2="clash", ch3="drone", bell_oct=3, pad_oct=3, bass_oct=2, duty1=3, duty2=0, wave=1, shimmer=True,
         motifs=[[(0, 4), (1, 4), (0, 8)], [(0, 3), (3, 3), (1, 3), (0, 7)], [(4, 2), (3, 2), (1, 2), (0, 9)]],
         pan1=(True, True), pan2=(True, False), vib2=(2, 4, 4),
         use="Dis: the City, Lake Cocytus and Judecca",
         mood="a low furnace and a semitone that will not resolve"),
    dict(key="PURGATORIO", label="HcPurgatorio", name="The Terraces", tempo=290, root=2, scale=[0, 2, 4, 6, 7, 9, 11],
         prog=[0, 1, 2, 3, 4, 3, 2, 0], density=[1.0, 1.0, 1.0, 1.1, 1.2, 1.0, 1.0, 1.3],
         ch1="bells", ch2="pad", ch3="drone", bell_oct=4, pad_oct=3, bass_oct=2, duty1=2, duty2=1, wave=1, climb=True,
         motifs=[[(0, 3), (1, 3)], [(0, 2), (1, 2), (2, 4)], [(0, 3), (2, 3), (1, 6)]],
         pan1=(False, True), pan2=(True, False), vib2=(8, 2, 4),
         use="PURGATORIO: the threshold, the terraces and Nick's Landing",
         mood="every phrase climbs one step higher than the last, then the section starts again at the bottom"),
    dict(key="ABYSS", label="HcAbyss", name="The Abyss", tempo=330, root=1, scale=[0, 1, 3, 5, 7, 8, 10],
         prog=[0, 0, 0, 1, 0, 0, 0, 0], density=[2.2, 2.6, 2.0, 2.4, 2.8, 2.2, 2.0, 2.6],
         ch1="rare", ch2="pad", ch3="drone", bell_oct=5, pad_oct=2, bass_oct=2, duty1=2, duty2=1, wave=2,
         motifs=[[(0, 6), (3, 8)], [(0, 5), (-1, 9)]],
         pan1=(True, True), pan2=(True, True), vib2=(14, 2, 2),
         use="the Abyss, the bottom of PURGATORIO",
         mood="almost silence, and something very large breathing in it"),
]


# ---------------------------------------------------------------------------------------------- composing
class Voice:
    """Collects (start, length, pitch, vol, fade) events of one channel, in engine units; pitch None is a rest."""

    def __init__(self, sustain=False):
        self.ev = []
        self.sustain = sustain  # a long note is re-struck every MAX_NOTE units instead of being cut short

    def add(self, start, length, p, vol, fade):
        assert length >= 1
        self.ev.append((start, length, p, vol, fade))

    def clean(self, total):
        """Sort, clip overlaps, split or cap long notes at MAX_NOTE units and the end at `total`."""
        out, t = [], 0
        for s, n, p, v, f in sorted(self.ev):
            s = max(s, t)
            n = min(n, total - s)
            if n < 1 or s >= total:
                continue
            if self.sustain:
                k = 0
                while k < n:
                    m = min(MAX_NOTE, n - k)
                    out.append((s + k, m, p, v, f))
                    k += m
            else:
                out.append((s, min(n, MAX_NOTE), p, v, f))
            t = s + n
        return out


def compose(song):
    rng = random.Random("hc-music-" + song["key"])
    sc, root = song["scale"], song["root"]
    secs = len(song["prog"])
    total = SECTION * secs
    v1, v2, v3 = Voice(), Voice(sustain=True), Voice(sustain=True)
    state = {"phrase": 0}

    def B(beats):  # beats -> units
        return int(round(beats * TIME))

    top = 6 * 12  # the highest note (C7): anything above is folded down an octave, not clipped to a repeated pitch

    def cap(p):
        return p - 12 if p > top else p

    for si, r in enumerate(song["prog"]):
        base = si * SECTION
        dens = song["density"][si % len(song["density"])]
        chord = [r, r + 2, r + 4]
        if song["ch2"] == "clash":
            chord = [r, r + 1, r + 4, r + 1]
        # ----------------------------------------------------------------- channel 3: drone / toll / pulse
        bass = pitch(sc, root, song["bass_oct"], r)
        if song["ch3"] == "drone":
            fifth_end = si % 3 == 2
            v3.add(base, SECTION - (B(16) if fifth_end else 0), bass, 1, 0)
            if fifth_end:
                v3.add(base + SECTION - B(16), B(16), pitch(sc, root, song["bass_oct"], r + 4), 1, 0)
        elif song["ch3"] == "toll":
            t = B(rng.choice([0, 2, 5]))
            while t < SECTION - B(3):
                v3.add(base + t, B(3), bass, 1, 0)
                t += B(rng.choice([10, 12, 13, 15]))
        elif song["ch3"] == "pulse":
            per = song["bass_period"]
            t = 0
            while t < SECTION:
                if rng.random() < 0.8:
                    v3.add(base + t, 2, bass if rng.random() < 0.8 else pitch(sc, root, song["bass_oct"], r + 2), 1, 0)
                t += per
        # ----------------------------------------------------------------- channel 2: the pad
        t = B(rng.choice([0, 2, 3]))
        k = 0
        while t < SECTION - B(4):
            d = chord[k % len(chord)] if rng.random() < 0.8 else chord[rng.randrange(len(chord))]
            n = min(B(rng.choice([6, 8, 10, 12])), SECTION - t)
            vol = 3 if song["key"] == "ABYSS" else rng.choice([4, 5])
            v2.add(base + t, n, pitch(sc, root, song["pad_oct"], d), vol, 0)
            t += n + max(1, int(B(rng.choice([1, 2, 3])) * dens))
            k += 1
        # ----------------------------------------------------------------- channel 1: the foreground
        style = song["ch1"]
        if style == "bells":
            t = int(B(rng.choice([2, 4, 8])) * dens)
            while t < SECTION - B(8):
                m = rng.choice(song["motifs"])
                start = r + rng.choice([0, 0, 2, 4, 7])
                if song.get("climb"):
                    start = r + state["phrase"] % 8
                    state["phrase"] += 1
                notes = list(m)
                if rng.random() < 0.3 and len(notes) > 2:
                    notes = notes[:-1] + [(notes[-1][0], notes[-1][1] + 3)]  # a held last note
                if rng.random() < 0.25:
                    notes = [(-d, n) for d, n in notes]  # inversion
                if rng.random() < 0.2:
                    notes = notes[::-1]
                stretch = rng.choice([1, 1, 1, 2])
                vol = rng.choice([8, 9, 10, 11])
                for d, n in notes:
                    n = n * stretch if n < 8 else n
                    v1.add(base + t, B(n), cap(pitch(sc, root, song["bell_oct"], start + d)), vol, rng.choice([4, 5, 6]))
                    t += B(n)
                t += int(B(rng.choice([6, 9, 12, 16, 20])) * dens)
        elif style == "ticks":
            per = song["period"]  # in units: the machine counts in sevens
            t = 1
            walk = r + 7
            while t < SECTION:
                if rng.random() < 0.7:
                    walk = min(max(walk + rng.choice([-1, 0, 1, 2]), r + 3), r + 11)
                    v1.add(base + t, 1, cap(pitch(sc, root, song["bell_oct"], walk)), rng.choice([8, 10]), 7)
                    if rng.random() < 0.2:
                        v1.add(base + t + 1, 1, cap(pitch(sc, root, song["bell_oct"], walk + 2)), 7, 7)
                t += per
        elif style == "rare":
            if si % 2 == 0 or rng.random() < 0.3:
                t = B(rng.randrange(6, 20))
                m = rng.choice(song["motifs"])
                for d, n in m:
                    v1.add(base + t, B(n), cap(pitch(sc, root, song["bell_oct"], r + d)), 5, 7)
                    t += B(n) + B(1)
    return total, [v.clean(total) for v in (v1, v2, v3)]


# ---------------------------------------------------------------------------------------------- rendering
def render_channel(num, song, events, total):
    lab = f"Music_{song['label']}_Ch{num}"
    o = [f"{lab}:"]
    if num == 1:
        o += [f"\ttempo {song['tempo']}", "\tvolume 7, 7"]
    pan = song["pan1"] if num == 1 else song["pan2"] if num == 2 else (True, True)
    o.append(f"\tstereo_panning {'TRUE' if pan[0] else 'FALSE'}, {'TRUE' if pan[1] else 'FALSE'}")
    if num == 1:
        o += [f"\tduty_cycle {song['duty1']}", "\tvibrato 12, 1, 4", f"\tnote_type {SPEED}, 9, 5"]
    elif num == 2:
        o += [f"\tduty_cycle {song['duty2']}", f"\tnote_type {SPEED}, 5, 0"]
        if song["vib2"][0]:
            o.append("\tvibrato %d, %d, %d" % song["vib2"])
        if song.get("shimmer"):
            o.append("\tduty_cycle_pattern 0, 2, 1, 2")
    else:
        o += [f"\tnote_type {SPEED}, {song.get('wavevol', 3)}, {song['wave']}", "\tvibrato 20, 1, 3"]
    o.append("\trest 16")  # a breath before the first sound
    o.append(".mainloop:")
    cur_oct, cur_env, t = None, None, 0

    def rests(n):
        while n > 0:
            k = min(16, n)
            o.append(f"\trest {k}")
            n -= k

    for s, n, p, vol, fade in events:
        rests(s - t)
        oc, pc = divmod(p, 12)
        assert 1 <= oc <= 8, (song["key"], p)
        if oc != cur_oct:
            o.append(f"\toctave {oc}")
            cur_oct = oc
        env = (vol, fade)
        if env != cur_env and num != 3:
            o.append(f"\tvolume_envelope {vol}, {fade}")
            cur_env = env
        o.append(f"\tnote {NAMES[pc]}, {n}")
        t = s + n
    rests(total - t)
    o.append("\tsound_loop 0, .mainloop")
    return o


def build():
    out = ["; Generated by tools/hardcore/gen_music.py. Do not edit by hand.", "", 'SECTION "Songs HC", ROMX', ""]
    info = []
    for song in SONGS:
        total, chans = compose(song)
        out += [f"Music_{song['label']}:", "\tchannel_count 3"]
        for i in (1, 2, 3):
            out.append(f"\tchannel {i}, Music_{song['label']}_Ch{i}")
        out.append("")
        for i, ev in enumerate(chans, 1):
            out += render_channel(i, song, ev, total) + [""]
        assert SPEED * MAX_NOTE * song["tempo"] < 256 * 256, song["key"]
        info.append((song, total, loop_seconds(song), [len(e) for e in chans]))
    return "\n".join(out), info


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


def main():
    asm, info = build()
    write("audio/hc_music.asm", asm)
    write("constants/hc_music_constants.asm",
          "; Generated by tools/hardcore/gen_music.py. Do not edit by hand.\n" + "".join(f"\tconst MUSIC_HC_{s['key']}\n" for s, *_ in info))
    write("audio/hc_music_pointers.asm",
          "; Generated by tools/hardcore/gen_music.py. Do not edit by hand.\n" + "".join(f"\tdba Music_{s['label']}\n" for s, *_ in info))
    rows = ["# Original music", "",
            "Eight ambient songs composed by rules (`tools/hardcore/gen_music.py`, seeded, deterministic). Three channels, long loops, "
            "lots of silence. Every phrase is a transformation of a small motif, so no bar repeats within a loop.", "",
            "| Constant | Song | Key / mode | Loop | Where |", "|---|---|---|---|---|"]
    for s, total, secs, counts in info:
        rows.append(f"| `MUSIC_HC_{s['key']}` | {s['name']} | {NAMES[s['root']].strip('_')} / {len(s['scale'])} tones {s['scale']} | "
                    f"{int(secs // 60)}:{int(secs % 60):02d} | {s['use']} |")
    rows += ["", "Moods:", ""] + [f"- **{s['name']}**: {s['mood']}." for s, *_ in info]
    write("docs/MUSIC.md", "\n".join(rows) + "\n")
    if "--report" in sys.argv:
        for s, total, secs, counts in info:
            print(f"{s['key']:11s} units {total:4d}  {secs:6.1f}s  notes ch1/ch2/ch3 {counts}")


if __name__ == "__main__":
    main()
