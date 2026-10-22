"""Cut list for tito_ep3_dormir v3 (rebuild 22.10, design bible + moon pajamas).
Rules (research/QC_CHECKLIST.md §6, Halloween v8): NO ping-pong, each piece = one forward pass of one 5 s take,
slow-down only to >= 0.85x, cuts snapped to the song's beat grid (107 bpm, first beat 0.11 s — measured on assets/song.wav).
Slots longer than one take (opening 9.25 s, the N16 endings) are split across two different takes.
Line starts = 0.15 s before the first sung word of song take s1 (assets/song_words.json).
    python production/episodes/tito_ep3_dormir/make_cuts.py && python production/edit_cuts.py production/episodes/tito_ep3_dormir/cuts.json
"""
import json
from pathlib import Path

D = Path(__file__).parent
plan = [(0.0, "N01a"), (4.6, "N01b"), (9.25, "N02"), (11.85, "N03"), (15.15, "N04"), (17.65, "N05"), (21.98, "N06"),
        (24.55, "K1"), (28.35, "K2"), (33.65, "K3"), (38.35, "K4"),
        (43.25, "N07"), (47.85, "N04"), (50.58, "N09"), (51.7, "N10"),
        (56.35, "K1"), (60.75, "K2"), (66.15, "K3"), (70.85, "K4"),
        (76.65, "N11"), (80.35, "N12"), (82.65, "N13"), (84.75, "N14"),
        (89.55, "K1"), (93.25, "K2"), (98.15, "K3"), (103.45, "K4"),
        (107.85, "N15"), (111.95, "N10"), (115.55, "N16"), (120.2, "K4"),
        (124.65, "K1"), (129.05, "K2"), (134.05, "K3"), (139.35, "K4"),
        (143.75, "K4"), (146.9, "N16"), (150.0, None)]
# shot -> (shot id, seed, in, until): the clean window of the take (checked frame by frame 22.10)
TAKE = {"N01a": ("N01", 31, 0.05, 4.99), "N01b": ("N01", 43, 0.05, 4.99), "N02": ("N02", 19, 0.05, 3.0),
        "N03": ("N03", 7, 0.05, 4.99), "N04": ("N04", 19, 0.05, 2.8), "N05": ("N05", 19, 0.05, 4.99),
        "N06": ("N06", 31, 0.05, 2.8), "K1": ("K1", 43, 0.05, 4.99), "K2": ("K2", 19, 0.05, 4.99),
        "K3": ("K3", 19, 0.05, 4.99), "K4": ("K4", 19, 0.05, 4.99), "N07": ("N07", 43, 0.05, 4.99),
        "N09": ("N09", 19, 0.05, 1.3), "N10": ("N10", 7, 0.05, 4.99), "N11": ("N11", 19, 0.05, 4.0),
        "N12": ("N12", 7, 0.05, 4.99), "N13": ("N13", 19, 0.05, 4.99), "N14": ("N14", 7, 0.05, 4.99),
        "N15": ("N15", 43, 0.05, 4.99), "N16": ("N16", 43, 0.05, 4.99)}
BEAT0, BEAT, END = 0.11, 60 / 107, 150.0
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
out = {"out": str(D / "build" / "tito_ep3_song_v3.mp4"), "song": str(D / "assets" / "song.wav"), "size": [1920, 1080],
       "clips": str(D / "shots_v3" / "ep3_clip3_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts")
