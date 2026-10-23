"""Cut list for the native vertical Halloween Short (1080x1920). Audio = the Halloween song 83.049-116.867 (33.8 s);
every cut on the 110 bpm grid (83.049 is a beat of the master). Takes from the researcher's QC 23.10 (QC_vshort_kf_v1.md).
Each take max 2x, speed >= 0.85x, one forward pass per piece.
    python production/episodes/tito_ep4_halloween_vshort/make_cuts.py && python production/edit_cuts.py <cuts.json>
"""
import json
from pathlib import Path

D = Path(__file__).parent
H = D.parent / "tito_ep4_halloween"
B = 60 / 110
W = {"VM1@31": (0.05, 4.0), "VM1@19": (0.2, 1.6), "VM2@7": (0.05, 1.5), "M3iv@31": (1.2, 4.0),
     "VM4@19": (0.05, 4.0), "VM4@19b": (1.2, 4.0), "VM4@31": (0.05, 4.0), "VM4@7": (0.05, 4.0),
     "VC1@7": (0.05, 4.0), "VC1@31": (0.05, 1.6), "VC2@43": (0.05, 3.3), "VC4@7": (0.05, 3.0)}
# (token, beats); None = until the slot end
plan = [("VM1@31", 7), ("VM1@19", 3),                     # 0-5.455 the sad mouse
        ("VM2@7", 3),                                     # he kneels, sets his bucket down
        ("M3iv@31", 5), ("VM4@19", 2),                    # the hand-to-bucket insert, then both happy
        ("VM4@31", 7),                                    # the mouse jumps for joy
        ("VC1@7", 8),                                     # chorus: each with its own bucket
        ("VC2@43", 6), ("VC1@31", 3),                     # the polite bow
        ("VM4@19b", 5), ("VM4@7", 5),                     # joy (was VC3: trunk/bucket fails)
        ("VC1@31", 2), ("VC4@7", None)]                   # they walk away together
END = 33.818
cuts, t, uses, bad = [], 0.0, {}, []
for tok, beats in plan:
    e = END if beats is None else round(t + beats * B, 3)
    i, u = W[tok]
    real = tok.rstrip("b") if tok.endswith("b") else tok
    need = e - t
    if (u - i) < 0.85 * need - 1e-6:
        bad.append(f"{tok} {t:.3f}-{e:.3f} needs {need:.2f}s has {u - i:.2f}s")
    cuts.append([round(t, 3), e, real, {"in": i, "until": round(min(u, i + need), 3)}])
    uses[real] = uses.get(real, 0) + 1
    t = e
over = {k: v for k, v in uses.items() if v > 2}
if bad or over or abs(t - END) > 1e-6:
    raise SystemExit(f"problems: {bad} {over} end={t}")
src = D / "build" / "vsrc"
src.mkdir(parents=True, exist_ok=True)
files = {f.stem.replace("vshort_clip_", ""): f for f in list((D / "shots").glob("vshort_clip_*.mp4")) + list((H / "shots_r4").glob("vshort_clip_*.mp4"))}
files["M3iv_s31"] = H / "shots_m3i" / "m3i_v_clip_s31.mp4"
for k, f in files.items():
    l = src / f"v_{k}.mp4"
    if l.is_symlink() or l.exists():
        l.unlink()
    l.symlink_to(f.resolve())
out = {"out": str(D / "build" / "tito_ep4_halloween_vshort.mp4"), "song": str(H / "assets" / "song.wav"), "song_start": 83.049,
       "size": [1080, 1920], "clips": str(src / "v_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts", uses)
