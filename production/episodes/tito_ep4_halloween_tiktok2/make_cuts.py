"""Cut list for the Halloween TikTok 2 "¿Quién es? 👀" (Roy 24.10, Weave cap 180). Native 9:16, built to LOOP:
frame 0 = Tito big + already knocking (bright), the last shot = Tito looking at the viewer, back to the knock.
Audio = the episode master from 11.049 (a beat, "¡Toc, toc, toc!") for 26 beats (14.18 s) -> ends right before "¡Dulce Halloween!".
    python production/episodes/tito_ep4_halloween_tiktok2/make_cuts.py && python production/edit_cuts.py <cuts.json>
"""
import json
from pathlib import Path

D = Path(__file__).parent
H = D.parent / "tito_ep4_halloween"
WV = D.parents[1] / "review" / "tiktok2_weave"
B = 60 / 110
# clean windows (5 fps check): knock eyes close 2.2-2.4 (blink) and 3.6-4.4 (ear on the door); loop eyes closed 1.2-2.4 + blink 3.8
W = {"KNOCK@0": (0.05, 3.5), "KITTEN@0": (0.05, 4.96), "BAT@0": (0.05, 4.96), "LOOP@0": (4.0, 5.0)}
plan = [("KNOCK@0", 7), ("KITTEN@0", 9), ("BAT@0", 8), ("LOOP@0", 2)]
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
for k, n in (("KNOCK_s0", "knock_kling.mp4"), ("KITTEN_s0", "kitten_kling.mp4"), ("BAT_s0", "bat_kling.mp4"), ("LOOP_s0", "loop_kling.mp4")):
    l = src / f"t_{k}.mp4"
    if l.is_symlink() or l.exists():
        l.unlink()
    l.symlink_to((WV / n).resolve())
out = {"out": str(D / "build" / "tito_ep4_halloween_tiktok2.mp4"), "song": str(H / "assets" / "song.wav"), "song_start": 11.049,
       "fade_out": 0.15, "size": [1080, 1920], "clips": str(src / "t_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts, end", t)
