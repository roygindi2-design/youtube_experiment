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
# v2 (researcher §12): kitten eyes squint shut + fangs 0.6-2.6 -> only 2.62-4.96; the TikTok gets one 4-beat bar shorter
# (21 beats, 11.45 s). Audio = master beats 20-23 (11.049-13.231, "¡Toc, toc, toc! ¿Quién…") + beats 28.. (from 15.413,
# "¿Quién es? ¿Un gatito con sombrero? ¡Miau!…"): a whole bar is dropped, so the beat phase and the music stay seamless.
W["KITTEN@0"] = (2.62, 4.96)
plan = [("KNOCK@0", 7), ("KITTEN@0", 5), ("BAT@0", 7), ("LOOP@0", 2)]
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
import subprocess
wav = D / "build" / "vsrc" / "audio_splice.wav"  # vsrc/ is gitignored (generated)
BEAT0 = 0.14
a0, a1, b0 = BEAT0 + 20 * B, BEAT0 + 24 * B, BEAT0 + 28 * B
b1 = b0 + t - (a1 - a0)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(H / "assets" / "song.wav"), "-filter_complex",
                f"[0]atrim={a0:.4f}:{a1 + 0.02:.4f},asetpts=PTS-STARTPTS[a];[0]atrim={b0:.4f}:{b1 + 0.5:.4f},asetpts=PTS-STARTPTS[b];"
                "[a][b]acrossfade=d=0.02:c1=tri:c2=tri[o]", "-map", "[o]", str(wav)], check=True)
out = {"out": str(D / "build" / "tito_ep4_halloween_tiktok2.mp4"), "song": str(wav), "song_start": 0.0,
       "fade_out": 0.15, "size": [1080, 1920], "clips": str(src / "t_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts, end", t)
