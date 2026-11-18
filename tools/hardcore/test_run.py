#!/usr/bin/env python3
"""The running animation and the pace of the player's steps, in the emulator.
Walking takes 16 frames per tile and running (hold B) 8.  A run shows the leaning poses (FACING_RUN_*) and nothing else: the two strides alternate every four
frames without a single frame of the walking pose in between (the old animation fell back to it for two frames at every tile boundary, a flicker).  Letting go
stands the player up at once.
usage: test_run.py TESTROM     (any test ROM that starts the player on open ground with four free tiles to the left and right)"""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(600, exit=True)
os.environ.setdefault("WALK_GOD", "1")
from test_walk import Walker, const_table  # noqa: E402

wk = Walker(sys.argv[1])
t, pb = wk.t, wk.t.pb
bad = []
K = const_table("constants/map_object_constants.asm")
RUN = {K["FACING_RUN_LEFT_0"], K["FACING_RUN_LEFT_1"], K["FACING_RUN_RIGHT_0"], K["FACING_RUN_RIGHT_1"]}


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


def facing():
    return t.mem("wPlayerStruct", 0x0D)  # OBJECT_FACING


def hold(direction, frames, run):
    """Hold a direction (and B for a run) for `frames` frames; give the facing byte of every frame and the frames at which the tile changed."""
    pb.button(direction, 3)
    t.tick(24)  # turn to face it
    if run:
        pb.button_press("b")
    pb.button_press(direction)
    seq, steps, last, lastf = [], [], wk.raw_state()[1:], None
    for f in range(frames):
        pb.tick()
        seq.append(facing())
        s = wk.raw_state()[1:]
        if s != last:
            if lastf is not None:
                steps.append(f - lastf)
            lastf, last = f, s
    pb.button_release(direction)
    if run:
        pb.button_release("b")
    return seq, steps


def runs(seq):
    out, n = [], 1
    for a, b in zip(seq, seq[1:]):
        if a == b:
            n += 1
        else:
            out.append(n)
            n = 1
    return out + [n]


seq, steps = hold("left", 70, False)
check("walking: 16 frames per tile", steps and set(steps) == {16}, str(steps))
t.tick(40)
seq, steps = hold("left", 70, True)
check("running: 8 frames per tile", steps and set(steps) == {8}, str(steps))
body = seq[10:-8]
check("running: only running poses (no walking frame between tiles)", set(body) <= RUN, " ".join(f"{x:02x}" for x in sorted(set(body))))
r = runs(body)[1:-1]
check("running: the strides alternate every four frames", r and set(r) == {4}, str(r))
for _ in range(30):
    pb.tick()
check("letting go stands the player up", facing() not in RUN and facing() < 0x10, f"{facing():02x}")
t.tick(30)
seq, steps = hold("right", 100, True)
check("running right: 8 frames per tile", steps and set(steps) == {8}, str(steps))
body = seq[10:-8]
check("running right: only running poses and four-frame strides", set(body) <= RUN and set(runs(body)[1:-1]) == {4}, str(runs(body)))

print("PASS" if not bad else "FAIL " + ", ".join(bad))
sys.exit(0 if not bad else 1)
