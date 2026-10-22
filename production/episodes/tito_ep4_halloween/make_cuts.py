"""Cut list for tito_ep4_halloween from the sung line starts of song take s2 (assets/song_words.json).

Each lyric line = one shot (spec 'sequence'). Every take is used only inside its CLEAN window (no blink, wink,
teeth or morph — frame review 22.10, 24 frames per take); a slot longer than the window plays it forward and
backward (ping-pong), because the editor refuses freezes and slow-downs below 0.85x.

    python production/episodes/tito_ep4_halloween/make_cuts.py && python production/edit_cuts.py <cuts.json>
"""
import json
from pathlib import Path

D = Path(__file__).parent
# (start, shot) — 0.15 s before the first sung word of each line (song s2 word times)
plan = [(0.0, "H01"), (6.4, "H01b"),
        (10.9, "D1"), (14.7, "Q"), (16.85, "V1"), (20.5, "BKT"),
        (23.9, "C1"), (28.1, "C2"), (32.45, "C3"), (38.85, "C4"),
        (45.15, "D2"), (49.4, "Q"), (52.1, "V2"), (54.65, "BKT"),
        (58.85, "C1"), (63.0, "C2"), (67.25, "C3"), (73.5, "C4"), (78.5, "Q"),
        (84.65, "M1"), (88.7, "M2"), (91.3, "M3"), (94.2, "M4"),
        (97.9, "C1"), (102.2, "C2"), (106.5, "C3"), (112.6, "C4"), (118.0, "M4"),
        (124.0, "O1"), (128.25, "O2"), (136.0, "M4"), (142.0, "O2"), (150.0, None)]
# take and clean window [in, until] in seconds of the 97-frame clip (4.04 s)
TAKE = {"H01": ("H01", 19, 0.06, 1.6), "H01b": ("H01", 7, 0.06, 2.5), "H02": ("H02", 19, 0.06, 2.25), "D1": ("D1", 7, 0.06, 2.1),
        "Q": ("Q", 7, 0.06, 2.1), "V1": ("V1", 7, 0.06, 4.0), "BKT": ("BKT", 19, 0.06, 2.8),
        "C1": ("C1", 31, 0.06, 4.0), "C2": ("C2", 7, 2.4, 4.0), "C3": ("C3", 7, 0.06, 4.0),
        "C4": ("C4", 19, 0.06, 4.0), "D2": ("D2", 19, 0.06, 4.0), "V2": ("V2", 7, 0.06, 1.25),
        "M1": ("M1", 7, 0.06, 4.0), "M2": ("M2", 7, 0.06, 1.0), "M3": ("M3", 19, 0.06, 4.0),
        "M4": ("M4", 31, 0.06, 2.0), "O1": ("O1", 7, 0.06, 1.25), "O2": ("O2", 7, 0.06, 1.0)}
over = D / "takes.json"  # later re-picks (redo takes) without touching this file
if over.exists():
    TAKE.update({k: tuple(v) for k, v in json.loads(over.read_text()).items()})


def pingpong(a, b, tok, i, u, sp=1.0):
    """Fill [a, b] with forward/backward passes over the clean window [i, u]."""
    out, t, pos, fwd = [], a, i, True
    while b - t > 1e-6:
        room = ((u - pos) if fwd else (pos - i)) / sp  # slot time the picture can run before it turns
        d = round(min(b - t, room), 3)
        rest = b - t - d
        if 1e-6 < rest < 0.5:  # avoid a tiny last piece: turn earlier so the last pass is at least 0.5 s
            d = round(d - (0.5 - rest), 3)
        if d < 0.5 and b - t > d + 1e-6:  # the window end is too close: turn now with what is left
            d = round(min(room, b - t), 3)
        if fwd:
            out.append([round(t, 3), round(t + d, 3), tok, {"in": round(pos, 3), "until": round(pos + d * sp, 3)}])
            pos += d * sp
        else:
            out.append([round(t, 3), round(t + d, 3), tok, {"reverse": True, "in": round(pos - d * sp, 3), "until": round(pos, 3)}])
            pos -= d * sp
        t += d; fwd = not fwd
    return out


SPEED = {"C1": 0.86}  # QC 22.10 (research): feet smear on the fast dance steps -> play the dance a little slower
cuts = []
for (a, sh), (b, _) in zip(plan, plan[1:]):
    sid, seed, i, u = TAKE[sh]
    cuts += pingpong(a, b, f"{sid}@{seed}", i, u, SPEED.get(sh, 1.0))
cuts[-1][1] = 150.0
out = {"out": str(D / "build" / "tito_ep4_halloween.mp4"), "song": str(D / "assets" / "song.wav"), "size": [1920, 1080],
       "clips": str(D / "shots" / "tito_ep4_halloween_clip_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts")
