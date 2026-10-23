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
W = {"VM1@31": (0.05, 4.0), "VM1@7": (0.05, 1.5), "VM2@7": (0.05, 1.5), "M3iv@31": (1.2, 4.0),
     "VM4@19": (0.05, 4.0), "VM4@19b": (1.2, 4.0), "VM4@31": (0.05, 4.0), "VM4@7": (0.05, 4.0),
     "VC1@7": (0.05, 4.0), "VC1@31": (0.05, 1.6), "VC2@43": (0.05, 3.3), "VC4@7": (0.05, 3.0)}
# Roy option A (23.10): shorter, every take ONCE, all at 1.0x (each take trimmed down to whole beats), no repeats
W["M3iv@31"] = (1.2, 3.95)
plan = [("VM1@31", 7), ("VM2@7", 2), ("M3iv@31", 5), ("VM4@31", 7), ("VC1@7", 7), ("VC2@43", 5), ("VC4@7", 5)]
cuts, t, uses, bad = [], 0.0, {}, []
for tok, beats in plan:
    e = round(t + beats * B, 3)
    i, u = W[tok]
    need = e - t
    if (u - i) < need - 1e-6:
        bad.append(f"{tok} {t:.3f}-{e:.3f} needs {need:.2f}s has {u - i:.2f}s (1.0x only)")
    cuts.append([round(t, 3), e, tok, {"in": i, "until": round(i + need, 3)}])
    uses[tok] = uses.get(tok, 0) + 1
    t = e
END = t
over = {k: v for k, v in uses.items() if v > 1}
if bad or over:
    raise SystemExit(f"problems: {bad} {over}")
src = D / "build" / "vsrc"
src.mkdir(parents=True, exist_ok=True)
files = {f.stem.replace("vshort_clip_", ""): f for f in list((D / "shots").glob("vshort_clip_*.mp4")) + list((H / "shots_r4").glob("vshort_clip_*.mp4"))}
files["M3iv_s31"] = H / "shots_m3i" / "m3i_v_clip_s31.mp4"
for k, f in files.items():
    l = src / f"v_{k}.mp4"
    if l.is_symlink() or l.exists():
        l.unlink()
    l.symlink_to(f.resolve())
out = {"out": str(D / "build" / "tito_ep4_halloween_vshort.mp4"), "song": str(H / "assets" / "song.wav"), "song_start": 83.049, "fade_out": 0.5,
       "size": [1080, 1920], "clips": str(src / "v_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts", uses)
