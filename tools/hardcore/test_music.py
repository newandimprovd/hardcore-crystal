#!/usr/bin/env python3
"""Plays each original song (gen_music.py) in the emulator with sound on, records the audio and checks it numerically:
   - it makes sound and is quiet most of the time (the brief: silent Lavender-Town style),
   - it never clips, and its pitches stay in the range the song was written for,
   - after one loop it comes round again exactly (the loudness envelope at lag = loop length matches the start),
   - inside a loop no stretch repeats (the envelope does not match itself at any shorter lag, so it is not boring).
Also writes a mono WAV and a spectrogram PNG per song into OUTDIR for listening and looking.
usage: test_music.py OUTDIR KEY=ROM [KEY=ROM ...]   (each ROM is a testbuild.sh ROM started on a map that plays that song, e.g. KEY=ROAD)"""
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
from gbtest import T  # noqa: E402
import gen_music  # noqa: E402

out = sys.argv[1]
roms = dict(a.split("=", 1) for a in sys.argv[2:])
os.makedirs(out, exist_ok=True)

# song ids: MUSIC_NONE is 0 and every `const MUSIC_` of constants/music_constants.asm counts one; the generated block follows the include
ids, n = {}, 0
for line in open(os.path.join(ROOT, "constants", "music_constants.asm")):
    s = line.strip()
    if s.startswith("const MUSIC_"):
        ids[s.split()[1]] = n
        n += 1
    elif "hc_music_constants" in s:
        for song in gen_music.SONGS:
            ids["MUSIC_HC_" + song["key"]] = n
            n += 1

SENT = 0x23E6
bad = []


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


def record(song, rom, seconds):
    """Boots the test ROM (it starts a new game on a map that plays this song), checks the map picked the song and records the audio."""
    t = T(rom, sound=True)
    pb = t.pb
    for i in range(900):  # past the title screen and into the map
        pb.button("a" if i % 2 else "start", 4)
        pb.tick(20, False)
        if t.mem("wMapGroup") and t.mem("wXCoord"):
            break
    pb.tick(180, False)
    playing = t.mem("wMusicID")
    check(f"{song['key']}: the map plays it", playing == ids["MUSIC_HC_" + song["key"]], f"wMusicID {playing}, wanted {ids['MUSIC_HC_' + song['key']]}")
    base = t.sym["wChannel1MusicAddress"][1]
    stride = t.sym["wChannel2"][1] - t.sym["wChannel1"][1]

    def pointers():
        return [pb.memory[base + c * stride] + 256 * pb.memory[base + c * stride + 1] for c in range(3)]

    loop_frames = int(round(gen_music.loop_seconds(song) * 60))
    f0 = 600
    chunks, p0, p1 = [], None, None
    for f in range(int(seconds * 60)):
        pb.tick(1, False)
        chunks.append(pb.sound.ndarray.astype(np.int16).copy())
        if f == f0:
            p0 = pointers()
        if f == f0 + loop_frames:
            p1 = pointers()
    t.stop()
    # the engine reads each channel's stream with its own pointer: one loop later every pointer must be at the same note again
    check(f"{song['key']}: every channel is back at the same note after one loop", all(abs(a - b) <= 3 for a, b in zip(p0, p1)),
          f"{[hex(x) for x in p0]} -> {[hex(x) for x in p1]}")
    return np.concatenate(chunks)  # (samples, 2) at 48000 Hz, signed 8 bit


def spectrogram(x, rate, path):
    from PIL import Image
    win = rate // 4
    cols = len(x) // win
    img = np.zeros((128, cols), dtype=np.float32)
    freqs = np.fft.rfftfreq(win, 1 / rate)
    edges = np.geomspace(40, 4000, 129)
    for c in range(cols):
        seg = (x[c * win:(c + 1) * win] - x[c * win:(c + 1) * win].mean()) * np.hanning(win)
        mag = np.abs(np.fft.rfft(seg))
        for r in range(128):
            m = (freqs >= edges[r]) & (freqs < edges[r + 1])
            if m.any():
                img[r, c] = mag[m].max()
    img = np.log1p(img)
    img = (255 * img / max(img.max(), 1e-9)).astype(np.uint8)[::-1]
    Image.fromarray(img).resize((min(cols * 2, 1600), 256), Image.NEAREST).save(path)


for song in gen_music.SONGS:
    if song["key"] not in roms:
        continue
    total_units = gen_music.SECTION * len(song["prog"])
    loop = gen_music.loop_seconds(song)
    secs = loop + 70
    a = record(song, roms[song['key']], secs)
    mono = a.mean(axis=1) if a.ndim == 2 else a.astype(np.float32)
    rate = 48000
    name = song["key"]
    # the first moments are the engine starting; the pyboy buffer is 8 bit, centred on 0
    with wave.open(os.path.join(out, name + ".wav"), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes((mono * 256).astype(np.int16).tobytes())
    spectrogram(mono[: rate * min(int(secs), 240)], rate, os.path.join(out, name + ".png"))
    # loudness per half second
    hop = rate // 2
    env = np.array([mono[i:i + hop].std() for i in range(0, len(mono) - hop, hop)])
    peak = np.abs(a).max()
    base = np.percentile(env, 10)
    quiet = float((env < 1.5 * base).mean())
    check(f"{name}: makes sound", env.max() > 0.5, f"max rms {env.max():.2f}")
    check(f"{name}: no clipping", peak < 120, f"peak {peak}")
    check(f"{name}: sparse, with long stretches of near-silence", quiet > 0.2, f"{quiet:.0%} of half-seconds within 1.5x of the quietest tenth (rms {base:.2f}, median {np.median(env):.2f}, max {env.max():.2f})")
    # no repeat inside a loop: compare 100 half-seconds (50 s) windows at every shorter lag of whole sections
    sec_len = int(round(gen_music.SECTION * gen_music.unit_frames(song) / 60.0 * 2))
    worst = 0.0
    seg = env[8:8 + 60]
    for k in range(1, len(song["prog"])):
        o = env[8 + k * sec_len:8 + k * sec_len + 60]
        if len(o) == len(seg) and seg.std() > 0 and o.std() > 0:
            worst = max(worst, float(np.corrcoef(seg, o)[0, 1]))
    check(f"{name}: sections differ from each other", worst < 0.9, f"worst section-lag corr {worst:.2f}")
    # pitch: the strongest frequency of every half second that is loud enough
    freqs = np.fft.rfftfreq(hop, 1 / rate)
    peaks = []
    for i in range(0, len(mono) - hop, hop):
        if mono[i:i + hop].std() > 0.35 * env.max():
            seg = mono[i:i + hop] - mono[i:i + hop].mean()
            mag = np.abs(np.fft.rfft(seg * np.hanning(hop)))
            peaks.append(freqs[1 + mag[1:].argmax()])
    if peaks:
        print(f"     {name}: loud-moment pitches {min(peaks):.0f}..{max(peaks):.0f} Hz, median {np.median(peaks):.0f}", flush=True)
    check(f"{name}: loop {int(loop // 60)}:{int(loop % 60):02d}", loop > 150, "long enough")

print("FAILED:" if bad else "all music checks pass", bad if bad else "")
sys.exit(1 if bad else 0)
