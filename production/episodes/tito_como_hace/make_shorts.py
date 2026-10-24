"""4 per-animal TikToks (researcher 24.10: our own data says viewers leave at 6-8 s, so cut 12-16 s units).
Each = hook (H1 2.0-3.07: Tito's eyes dart to the side, 2 beats) over the intro's "¡Escucha!" tail with the animal's
REAL baby sound at 0.3 s, then the pair from the v2 master (picture + mix), cut on the beat grid, 0.15 s fades.
    python make_shorts.py <v2_raw.mp4> <mix_v2.wav>
"""
import json
import subprocess
import sys
from pathlib import Path

D = Path(__file__).parent
ROOT = D.parents[2]
v2, mix = sys.argv[1:3]
M = json.load(open(D / "mix_map.json"))
B, G0 = M["beat"], 1.93
ev = {p["pair"]: p for p in M["pairs"]}
INS = [p["insert_song_t"] for p in M["pairs"]]
out_t = lambda s: s + sum(4 * B for x in INS if x < s)
g = lambda t: G0 + round((t - G0) / B) * B
# pair start (question) and end (after "¡Así hace mamá…!" / the F2 toot) in output time
SPAN = {"patito": (out_t(4.0), out_t(19.0) + 0.9), "gatito": (out_t(20.9), out_t(36.1) + 0.9),
        "ratoncito": (out_t(38.7), out_t(53.2) + 0.9), "elefantito": (out_t(55.8), 77.02)}
TXT = {"patito": "¿Cómo hace el patito? 🐣", "gatito": "¿Cómo hace el gatito? 🐱",
       "ratoncito": "¿Cómo hace el ratoncito? 🐭", "elefantito": "¿Cómo hace Tito? 🐘"}
hook_a1 = g(4.0 - 0.15)
hook_a0 = hook_a1 - 2 * B
run = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
B_ = D / "build"
res = {}
for k, (a, b) in SPAN.items():
    s0, s1 = g(a - 0.15), g(b)
    bs = ev[k]["baby_sound_out_t"]
    hd = 2 * B
    # hook picture + body picture
    run("-ss", "2.0", "-i", str(ROOT / "production/review/como_hace_weave/H1_minimax.mp4"), "-t", f"{hd:.3f}",
        "-vf", "scale=-2:1920:flags=lanczos,crop=1080:1920,unsharp=5:5:0.4:5:5:0.0,fps=30", "-an",
        "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(B_ / f"sh_{k}_hook.mp4"))
    run("-ss", f"{s0:.3f}", "-i", v2, "-t", f"{s1 - s0:.3f}", "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
        "-r", "30", str(B_ / f"sh_{k}_body.mp4"))
    # audio: intro tail + the baby's real sound at 0.3 s (taken from the mix at its onset) -> the pair slice; fades on bar edges
    fc = (f"[0]atrim={hook_a0:.4f}:{hook_a1:.4f},asetpts=PTS-STARTPTS[h];"
          f"[0]atrim={bs:.4f}:{bs + 0.6:.4f},asetpts=PTS-STARTPTS,volume=0.8,adelay=300|300[bb];"
          "[h][bb]amix=inputs=2:duration=first:normalize=0[hk];"
          f"[0]atrim={s0:.4f}:{s1:.4f},asetpts=PTS-STARTPTS[p];"
          f"[hk][p]acrossfade=d=0.02:c1=tri:c2=tri,afade=t=in:d=0.15,"
          f"afade=t=out:st={hd + (s1 - s0) - 0.17:.3f}:d=0.15,alimiter=limit=0.84:level=false[o]")
    wav = B_ / f"sh_{k}.wav"
    run("-i", mix, "-filter_complex", fc, "-map", "[o]", str(wav))
    lst = B_ / f"sh_{k}.txt"
    lst.write_text(f"file '{B_ / f'sh_{k}_hook.mp4'}'\nfile '{B_ / f'sh_{k}_body.mp4'}'\n")
    raw = B_ / f"sh_{k}_raw.mp4"
    run("-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
        "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(raw))
    dur = hd + (s1 - s0)
    t1 = B_ / f"sh_{k}_t1.mp4"
    out = ROOT / f"production/deliver/tito_como_hace_tiktok_{k}.mp4"
    tt = str(ROOT / "production/tiktok_text.py")
    subprocess.run([sys.executable, tt, str(raw), str(t1), TXT[k], "--until", "2.5", "--y", "0.14", "--size", "74"], check=True, capture_output=True)
    subprocess.run([sys.executable, tt, str(t1), str(out), "Más con Tito → YouTube 🐘", "--start", f"{dur - 2.5:.2f}",
                    "--until", f"{dur - 0.05:.2f}", "--y", "0.14", "--size", "64"], check=True, capture_output=True)
    res[k] = {"master_span": [round(s0, 3), round(s1, 3)], "duration": round(dur, 2),
              "baby_sound_t": round(hd + bs - s0, 3), "mama_sound_t": round(hd + ev[k]["mama_sound_out_t"] - s0, 3)}
json.dump(res, open(D / "shorts_map.json", "w"), indent=1)
print(json.dumps(res, indent=1))
