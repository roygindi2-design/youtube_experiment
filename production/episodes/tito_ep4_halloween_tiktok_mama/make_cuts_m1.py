"""TikTok M1 "¡No me cabe!" (Roy 24.10). Native 9:16, ~11 s, loop: stuck in the costume -> Mamá tugs it down, arms pop
up -> forehead kiss (short) + bucket up -> back to the stuck shot. Audio = the episode master from beat 0 (0.14 s), 20 beats.
s1/s2 = Kling first+last-frame re-renders (eyes stay open); s3 = the K3 clip from 1.18 (the kiss beat kept <= 0.4 s).
    python production/episodes/tito_ep4_halloween_tiktok_mama/make_cuts_m1.py && python production/edit_cuts.py <cuts_m1.json>
"""
import json
from pathlib import Path

D = Path(__file__).parent
H = D.parent / "tito_ep4_halloween"
WV = D.parents[1] / "review" / "tiktok_mama_weave"
B = 60 / 110
W = {"STUCK@0": (0.05, 3.87), "POP@0": (0.05, 3.32), "KISS@0": (1.18, 5.0)}
plan = [("STUCK@0", 7), ("POP@0", 6), ("KISS@0", 7)]
cuts, t = [], 0.0
for tok, beats in plan:
    e = round(t + beats * B, 3)
    i, u = W[tok]
    need = e - t
    if (u - i) < 0.85 * need - 1e-6:
        raise SystemExit(f"{tok} needs {need:.2f}s, has {u - i:.2f}s")
    cuts.append([round(t, 3), e, tok, {"in": i, "until": round(min(u, i + need), 3)}])
    t = e
src = D / "build" / "vsrc"
src.mkdir(parents=True, exist_ok=True)
for k, n in (("STUCK_s0", "m1_s1_fl.mp4"), ("POP_s0", "m1_s2_fl.mp4"), ("KISS_s0", "m1_s3_kling.mp4")):
    l = src / f"m1_{k}.mp4"
    if l.is_symlink() or l.exists():
        l.unlink()
    l.symlink_to((WV / n).resolve())
out = {"out": str(D / "build" / "tito_ep4_halloween_tiktok_m1.mp4"), "song": str(H / "assets" / "song.wav"), "song_start": 0.14,
       "fade_out": 0.15, "size": [1080, 1920], "clips": str(src / "m1_"), "cuts": cuts}
(D / "cuts_m1.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts, end", t)
