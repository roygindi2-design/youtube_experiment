"""Cut list for tito_brocoli v1 (long episode, song take s2, 110 bpm, first beat 0.34 s — measured on assets/song.wav).
Rules (QC_CHECKLIST §6–7, as Halloween v8 / ep3 v3): no ping-pong, each piece = one forward pass of one 5 s take, >= 0.85x,
cuts snapped to the beat grid. Line starts = Whisper word times of take s2 (assets/song_words.json).
Long lines (crunch 9 s, thanks 10 s, the outro 21 s) are split across two takes / cutaways.
    python production/episodes/tito_brocoli/make_cuts.py && python production/edit_cuts.py production/episodes/tito_brocoli/cuts.json
"""
import json
from pathlib import Path

D = Path(__file__).parent
plan = [(0.0, "I1"), (5.72, "I2a"), (9.3, "I2b"), (12.06, "R1"), (15.16, "Q"), (17.76, "G1"), (22.46, "G2a"), (27.0, "G2b"),
        (31.6, "K1"), (34.2, "K2"), (37.6, "K3"), (42.3, "K4"), (47.0, "G1b"),
        (52.54, "R2"), (53.96, "Qb"), (56.86, "C1"), (61.68, "C2"), (66.3, "C1b"),
        (70.88, "K1b"), (73.36, "K2"), (76.4, "K3b"), (81.58, "K4"), (86.3, "K1"),
        (89.5, "R3"), (94.02, "T1"), (98.44, "T2"), (103.58, "T3"),
        (108.94, "K1"), (111.68, "K2"), (114.7, "K3"), (119.76, "K4"),
        (124.7, "O1a"), (125.8, "O1b"), (128.62, "O2"), (133.3, "O2b"), (138.0, "T1b"), (142.5, "C1"), (147.0, "K3b"), (150.0, None)]
# shot -> (shot id, seed, in, until): clean window of the take (frame review 22.10)
TAKE = {"I1": ("I1", 7, 0.05, 4.99), "I2a": ("I2", 19, 0.05, 3.6), "I2b": ("I2", 7, 0.05, 3.0),
        "R1": ("R1", 7, 0.05, 4.99), "Q": ("Q", 7, 0.05, 4.99), "Qb": ("Q", 19, 0.05, 4.99),
        "G1": ("G1", 7, 0.05, 4.99), "G1b": ("G1", 19, 0.05, 4.99), "G2a": ("G2", 19, 0.05, 4.99), "G2b": ("G2", 7, 0.05, 4.99),
        "K1": ("K1", 19, 0.05, 4.99), "K1b": ("K1", 7, 0.05, 4.99), "K2": ("K2", 19, 0.05, 3.0),
        "K3": ("K3", 7, 0.05, 4.99), "K3b": ("K3", 19, 0.05, 4.99), "K4": ("K4", 7, 0.05, 4.99),
        "R2": ("R2", 7, 0.05, 3.6), "C1": ("C1", 43, 0.05, 4.99), "C1b": ("C1", 31, 0.05, 4.99), "C2": ("C2", 19, 0.05, 4.99),
        "R3": ("R3", 7, 0.05, 4.99), "T1": ("T1", 7, 0.05, 4.99), "T1b": ("T1", 19, 0.05, 4.99), "T2": ("T2", 7, 0.05, 4.99),
        "T3": ("T3", 7, 0.05, 4.99), "O1a": ("O1", 7, 0.05, 1.15), "O1b": ("O1", 57, 2.4, 4.99),
        "O2": ("O2", 19, 0.05, 4.99), "O2b": ("O2", 7, 0.05, 4.99)}
BEAT0, BEAT, END = 0.34, 60 / 110, 150.0
snap = lambda t: t if t in (0.0, END) else round(BEAT0 + round((t - BEAT0) / BEAT) * BEAT, 3)
plan = [(snap(t), sh) for t, sh in plan]
cuts, bad = [], []
for (a, sh), (b, _) in zip(plan, plan[1:]):
    sid, seed, i, u = TAKE[sh]
    need = b - a
    if (u - i) < 0.85 * need - 1e-6:
        bad.append(f"{sh} {a}-{b}: needs {need:.2f}s, take has {u - i:.2f}s")
    cuts.append([a, b, f"{sid}@{seed}", {"in": i, "until": round(min(u, i + need), 3)}])
if bad:
    raise SystemExit("takes too short:\n  " + "\n  ".join(bad))
out = {"out": str(D / "build" / "tito_brocoli.mp4"), "song": str(D / "assets" / "song.wav"), "size": [1920, 1080],
       "clips": str(D / "shots_v1" / "bro_clip1_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts")
