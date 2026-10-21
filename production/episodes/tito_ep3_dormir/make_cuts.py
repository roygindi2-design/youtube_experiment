"""Cut list for tito_ep3_dormir from the sung line starts of song take s1 (assets/song_words.json).
Each line = one shot (spec 'sequence'); a slot longer than 4.6 s plays the clip forward and then backward (boomerang),
because the editor refuses freezes and slow-downs below 0.85x.   python .../make_cuts.py [seeds.json]"""
import json, sys
from pathlib import Path
D = Path(__file__).parent
seeds = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
# (start, shot) — starts are 0.15 s before the first sung word of the line
plan = [(0.0, "N01"), (9.25, "N02"), (11.85, "N03"), (15.15, "N04"), (17.65, "N05"), (20.15, "N06"),
        (24.55, "K1"), (28.35, "K2"), (33.65, "K3"), (38.35, "K4"),
        (43.25, "N07"), (47.85, "N04"), (50.15, "N09"), (53.05, "N10"),
        (56.35, "K1"), (60.75, "K2"), (66.15, "K3"), (70.85, "K4"),
        (76.65, "N11"), (80.35, "N12"), (82.65, "N13"), (84.75, "N14"),
        (89.55, "K1"), (93.25, "K2"), (98.15, "K3"), (103.45, "K4"),
        (107.85, "N15"), (111.95, "N10"), (115.55, "N16"),
        (124.65, "K1"), (129.05, "K2"), (134.05, "K3"), (139.35, "K4"),
        (143.75, "N16"), (150.0, None)]
# QC 21.10 (frame review): usable length of a take, where the clip breaks after that point
LIMIT = {"N04v2": 2.4, "K4v2": 2.6, "N13v2": 2.7, "N11": 2.4, "N12": 1.9}
# square (736x736) clips in 16:9: where to put the crop window, or show the whole frame (fit)
FRAMING = {"N10": {"in": 0.6}, "N13v2": {"in": 0.5}, "N16v2": {"in": 0.4}, "N03": {"fit": True}, "K1": {"crop_y": 0.25}, "N04": {"crop_y": 0.4}, "N05": {"crop_y": 0.4}, "N06": {"crop_y": 0.3},
           "N12": {"crop_y": 0.45}, "N15": {"crop_y": 0.45}}
# v2 (21.10 night, Roy: eyes/faces): re-made shots, 16:9, picked by glitch_scan + eye review
V2 = {"N16", "N01", "N04", "N06", "K1", "K2", "K3", "K4", "N07", "N13", "N14", "N15"}
plan = [(t, (sh + "v2" if sh in V2 else sh) if sh else None) for t, sh in plan]
cuts, use = [], {}
for (a, sh), (b, _) in zip(plan, plan[1:]):
    n = use[sh] = use.get(sh, 0) + 1
    seed = seeds.get(f"{sh}#{n}", seeds.get(sh, 7))
    tok = f"{sh}@{seed}"
    lim = LIMIT.get(sh)
    if lim and lim + 0.01 < b - a <= lim / 0.86:  # a little slower instead of a tiny backward piece
        cuts.append([a, b, tok, {"until": lim + 0.06}])
    elif lim and b - a > lim + 0.01:  # forward up to the limit, then back (boomerang)
        m = round(a + lim, 2)
        cuts += [[a, m, tok, {"until": lim + 0.06}], [m, b, tok, {"reverse": True, "in": round(lim + 0.06 - (b - m), 2), "until": lim + 0.06}]]
    elif b - a <= 4.6:
        cuts.append([a, b, tok])
    elif b - a > 7.8:  # forward, backward, forward again
        m1, m2 = round(a + 3.9, 2), round(a + 7.8, 2)
        cuts += [[a, m1, tok], [m1, m2, tok, {"reverse": True, "in": 0.06}], [m2, b, tok]]
    else:
        m = round(a + min(3.9, (b - a) / 2 + 0.6), 2)
        cuts.append([a, m, tok])
        cuts.append([m, b, tok, {"reverse": True, "in": round(4.0 - (b - m) * 1.0, 2) if b - m < 3.9 else 0.06}])
out = {"out": str(D / "build" / "tito_ep3_song.mp4"), "song": str(D / "assets" / "song.wav"), "size": [1920, 1080],
       "clips": str(D / "shots" / "clipF_"), "cuts": cuts}
for c in cuts:
    fr = FRAMING.get(c[2].split("@")[0])
    if fr:
        if len(c) == 3:
            c.append({})
        c[3].update(fr)
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts")
