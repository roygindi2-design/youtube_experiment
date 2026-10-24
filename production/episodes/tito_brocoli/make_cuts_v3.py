"""Cut list for tito_brocoli v2 (Roy 23.10 fixes). Base = the v1 plan (make_cuts.py), song take s2, 110 bpm, first beat 0.34 s.
Fixes: R1/R2 front-facing NO-NO (v2 takes); chorus x3 with a different take of each move per chorus (each take max 2x);
K4 = Mamá pats with her hand (v2/fix takes) + the toucan cutaway copying the dance at the end of each K4 line;
the extra K1 at 86.3 -> G1 cutaway, the C1 repeat at 142.5 -> the clean-up shot; MO (carrot to the monkey) +
MO2 (plate into the basket) before the outro, in the old O1 slot. v1 clips = 5.0 s (shots_v1), v2 clips = 4.0 s (shots_v2, shots_fix).
    python production/episodes/tito_brocoli/make_cuts_v2.py && python production/edit_cuts.py production/episodes/tito_brocoli/cuts_v3.json
"""
import json
import os
from pathlib import Path

D = Path(__file__).parent
BEAT0, BEAT, END = 0.34, 60 / 110, 150.0
snap = lambda t: t if t in (0.0, END) else round(BEAT0 + round((t - BEAT0) / BEAT) * BEAT, 3)
K4B = os.environ.get("K4B", "K4f@43")   # chorus-2 K4 take (fix job)
K4C = os.environ.get("K4C", "K4f@43")   # chorus-3 K4 take
MO2 = os.environ.get("MO2", "MO2f@19")
MO2B = os.environ.get("MO2B", "TUv2@19")
# token -> (in, until)
W = {"I1@7": (0.05, 4.99), "I2@19": (0.05, 3.6), "I2@7": (0.05, 3.0), "Q@7": (0.05, 4.99), "Q@19": (0.05, 4.99),
     "G1@7": (0.05, 4.99), "G1@19": (0.05, 4.99), "G2@19": (0.05, 4.99), "G2@7": (0.05, 4.99),
     "K1@57": (0.05, 4.99), "K1@31": (0.05, 4.99), "K1v2@97": (0.05, 4.0),
     "K2v2@7": (0.05, 4.0), "K2v2@19": (0.05, 4.0), "K2v2@31": (0.05, 4.0),
     "K3@7": (0.05, 4.99), "K3@19": (0.05, 4.99), "K3v2@97": (0.05, 3.5), "K3v2@83": (0.05, 3.0), "K3v2@83b": (1.0, 3.0),
     "K4v2@19": (0.05, 3.2), "K4f@43": (0.05, 4.0), "K4f@57": (0.05, 4.0),
     "TUv2@7": (0.05, 4.0), "TUv2@19": (0.05, 4.0),
     "R1v2@7": (0.05, 4.0), "R2v2@7": (0.05, 4.0), "C1@43": (0.05, 4.99), "C1@31": (0.05, 4.99), "C2@19": (0.05, 4.99),
     "R3@7": (0.05, 4.99), "T1@7": (0.05, 4.99), "T1@19": (0.05, 4.99), "T2@7": (0.05, 4.99), "T3@7": (0.05, 4.99),
     "MOv2@7": (0.05, 1.6), "MO2f@7": (0.05, 4.0), "MO2f@19": (0.05, 4.0), "MO2f@31": (0.05, 4.0),
     "O1@57": (2.4, 4.99), "O2@19": (0.05, 4.99), "O2@7": (0.05, 4.99)}
# (start, [(token, beats or None=rest), ...])
# v3 (Roy 24.10, researcher deep QC §12): Kling walk in ONE G1 slot, other G1 slots = different shots; Kling rocket in one
# rocket slot; eye-closed stretches trimmed; T3 starts past the trunk touch; ending = ONE approach + Mamá's pat + clean-up
WV = D.parents[1] / "review" / "brocoli_weave"
ROCKET = "C1K@0" if (WV / "rocket_kling.mp4").exists() else "C1@43c"
W.update({"G1K@0": (0.05, 4.96), "C1K@0": (0.05, 1.15), "C1K@0b": (3.3, 4.94), "C1@57": (0.05, 1.69), "C1@43": (0.05, 2.78), "C1@43c": (0.05, 4.99), "G2v2@97": (0.05, 1.7), "G2@7": (2.0, 3.9),
          "K3@7b": (0.05, 1.15), "K1v2@83": (0.05, 1.7), "R2v2@7": (0.05, 4.0), "Q@19": (0.05, 2.24), "Q@7b": (0.8, 1.95),
          "C2@19": (0.05, 2.3), "K1v2@97": (0.05, 4.0), "C2@19b": (2.9, 4.99), "K4f@57": (0.05, 2.4), "Q@19b": (3.4, 4.99),
          "T3@7": (0.5, 4.99), "K4v2@19b": (0.05, 3.2), "MO2f@19": (0.05, 1.7), "K3v2@97": (0.05, 3.5)})
plan = [(0.0, [("I1@7", None)]), (5.72, [("I2@19", None)]), (9.3, [("I2@7", None)]), (12.06, [("R1v2@7", None)]),
        (15.16, [("Q@7", None)]), (17.76, [("G1K@0", None)]), (22.46, [("G2@19", None)]),
        (27.0, [("G2v2@97", 3), ("G2@7", 3), ("K3@7b", None)]),
        (31.6, [("K1@57", None)]), (34.2, [("K2v2@7", None)]), (37.6, [("K3@7", None)]), (42.3, [("K4v2@19", 6), ("TUv2@7", None)]),
        (47.0, [("K3v2@97", 6), ("K1v2@83", None)]),
        (52.0, [("R2v2@7", None)]), (53.96, [("Q@19", 4), ("Q@7b", None)]), (56.86, [("C1@43", 5), ("C1K@0b", None)]),  # Kling rocket: only the closed-mouth start + the fly-off (open-mouth laugh 1.4-3.2 cut)
        (61.68, [("C2@19", 4), ("K1v2@97", None)]), (66.3, [("C1K@0", 2), ("C1@57", 3), ("C2@19b", None)]),
        (70.88, [("K1@31", None)]), (73.36, [("K2v2@19", None)]), (76.4, [("K3@19", None)]), (81.58, [(K4B, 7), ("TUv2@19", None)]),
        (86.3, [("K4f@57", 3), ("Q@19b", None)]),
        (89.5, [("R3@7", None)]), (94.02, [("T1@7", None)]), (98.44, [("T2@7", None)]), (103.58, [("T3@7", None)]),
        (107.85, [("K1v2@97", None)]), (111.68, [("K2v2@31", None)]), (114.7, [("K3v2@97", 5), ("K3v2@83", None)]), (119.76, [(K4C, 7), ("TUv2@7", None)]),
        (124.7, [("MOv2@7", 3), ("K3v2@83b", None)]), (128.62, [("O2@19", None)]), (133.3, [("K4v2@19b", 5), ("MO2f@19", None)]), (138.0, [("T1@19", None)]),
        (142.5, [(MO2B, None)]), (147.0, [("K3@19", None)]), (150.0, None)]
plan = [(snap(t), p) for t, p in plan]
cuts, bad, uses = [], [], {}
for (a, pieces), (b, _) in zip(plan, plan[1:]):
    t = a
    for n, (tok, beats) in enumerate(pieces):
        e = b if beats is None else round(t + beats * BEAT, 3)
        i, u = W[tok]
        need = e - t
        if (u - i) < 0.85 * need - 1e-6:
            bad.append(f"{tok} {t}-{e}: needs {need:.2f}s, take has {u - i:.2f}s")
        real = tok[:-1] if tok[-1] in "bc" and "@" in tok and not tok[-1].isdigit() else tok  # "...b" = a second window of the same take
        cuts.append([round(t, 3), round(e, 3), real, {"in": i, "until": round(min(u, i + need), 3)}])
        uses[real] = uses.get(real, 0) + 1
        t = e
over = {k: v for k, v in uses.items() if v > 2}
row = [f"{a[2]} @ {a[0]}" for a, b in zip(cuts, cuts[1:]) if a[2] == b[2]]
if row:
    raise SystemExit(f"same take twice in a row: {row}")
if bad or over:
    raise SystemExit("problems:\n  " + "\n  ".join(bad) + (f"\n  >2x: {over}" if over else ""))
src = D / "build" / "v2src"
src.mkdir(parents=True, exist_ok=True)
for k2, n2 in (("G1K_s0", "G1_kling.mp4"), ("C1K_s0", "rocket_kling.mp4")):
    if (WV / n2).exists():
        l = src / f"{k2}.mp4"
        if l.is_symlink() or l.exists():
            l.unlink()
        l.symlink_to((WV / n2).resolve())
for d, tag, pre in ((D / "shots_v1", "", "bro_clip1_"), (D / "shots_v2", "v2", "bro_clip2_"), (D / "shots_fix", "f", "bro_clip2_")):
    for f in d.glob(pre + "*.mp4"):
        sid, seed = f.stem[len(pre):].rsplit("_s", 1)
        l = src / f"{sid}{tag}_s{seed}.mp4"
        if l.is_symlink() or l.exists():
            l.unlink()
        l.symlink_to(f.resolve())
out = {"out": str(D / "build" / "tito_brocoli_v3.mp4"), "song": str(D / "assets" / "song.wav"), "size": [1920, 1080],
       "clips": str(src) + "/", "cuts": cuts}
(D / "cuts_v3.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts; uses >1:", {k: v for k, v in uses.items() if v > 1})
