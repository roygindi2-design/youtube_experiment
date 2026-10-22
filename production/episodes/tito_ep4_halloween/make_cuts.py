"""Cut list for tito_ep4_halloween (v7, after Roy's motion review 22.10).

Rules (research/QC_CHECKLIST.md §6): NO ping-pong, every piece = one continuous forward pass of one take,
slow-down only to >= 0.85x (edit_cuts refuses lower), static holds <= 2 s, no piece < 1.5 s.
Long sung lines and the instrumental breaks get a cutaway (EST street, WALK across the frame) instead of a loop.
Line starts are 0.15 s before the first sung word of song take s2 (assets/song_words.json); C3 starts a little
late on the long lines so one 5 s take covers them at >= 0.85x.

    python production/episodes/tito_ep4_halloween/make_cuts.py && python production/edit_cuts.py <cuts.json>
"""
import json
from pathlib import Path

D = Path(__file__).parent
plan = [(0.0, "H01"), (2.4, "H02"), (6.4, "WALK"),
        (10.9, "D1"), (14.7, "Q"), (16.85, "V1"), (21.0, "BKT"),
        (23.9, "C1"), (28.1, "C2"), (32.9, "C3"), (38.6, "C4"), (43.2, "WALK2"),
        (45.15, "D2"), (47.5, "Q2"), (52.1, "V2"), (54.65, "BKT2"),
        (58.85, "C1"), (63.0, "C2"), (67.55, "C3"), (73.25, "C4"), (78.0, "WALK"),
        (83.0, "M1"), (88.7, "M2"), (91.3, "M3"), (94.2, "M4"),
        (97.9, "C1"), (102.2, "C2"), (106.8, "C3"), (112.35, "C4"), (117.0, "M4b"), (122.0, "WALK2"),
        (124.0, "O1"), (128.25, "O2"), (134.0, "C1"), (138.5, "M4"), (144.3, "O2c"), (150.0, None)]
# shot -> (clip id, seed, in, until) — the window is the usable part of the take (eye pops / morphs cut out)
TAKE = json.loads((D / "takes_v7.json").read_text())

cuts, bad = [], []
for (a, sh), (b, _) in zip(plan, plan[1:]):
    sid, seed, i, u = TAKE[sh]
    need = b - a
    if (u - i) / need < 0.85 - 1e-6:
        bad.append(f"{sh} {a}-{b}: needs {need:.2f}s, take has {u - i:.2f}s (min {need * 0.85:.2f}s)")
    until = min(u, i + need)  # use only what the slot needs (no slow-down when the take is long enough)
    cuts.append([a, b, f"{sid}@{seed}", {"in": i, "until": round(until, 3)}])
if bad:
    raise SystemExit("takes too short:\n  " + "\n  ".join(bad))
out = {"out": str(D / "build" / "tito_ep4_halloween.mp4"), "song": str(D / "assets" / "song.wav"), "size": [1920, 1080],
       "clips": str(D / "shots" / "tito_ep4_halloween_clip_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts")
