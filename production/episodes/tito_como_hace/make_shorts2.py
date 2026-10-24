"""4 per-animal TikToks, v2 (Roy 24.10: "looks stuck, not in rhythm, music not smooth, stills look terrible"):
ZERO stills; native 24 fps (no frame duplication); every picture cut ON a beat of the accompaniment grid; ONE continuous
slice of mix v3 per short with 0.25 s fades; lanczos upscale only. The real-sound sync clips keep their exact placement
(cut-in on the first beat after their clean start, in-point = onset - (sound - beat)). Filler motion between syncs =
forward clean windows (each window used <= 2x), slowed to >= 0.85x only if needed.
    python make_shorts2.py <mix_v3.wav> [patito gatito ratoncito elefantito]
"""
import json
import math
import subprocess
import sys
from pathlib import Path

D = Path(__file__).parent
ROOT = D.parents[2]
WV = ROOT / "production/review/como_hace_weave"
mix = sys.argv[1]
which = sys.argv[2:] or ["patito", "gatito", "ratoncito", "elefantito"]
M = json.load(open(D / "mix_map.json"))
B, G0, FPS = M["beat"], 1.93, 24
ev = {p["pair"]: p for p in M["pairs"]}
INS = [p["insert_song_t"] for p in M["pairs"]]
out_t = lambda s: s + sum(4 * B for x in INS if x < s)
up = lambda t: G0 + math.ceil((t - G0) / B - 1e-6) * B     # first beat >= t
dn = lambda t: G0 + math.floor((t - G0) / B + 1e-6) * B    # last beat <= t
# shorts: slice start (question), syncs (clip, clean_in, clean_out, onset, sound_t, speed), fillers before/between/after
S = {
    "patito": dict(start=out_t(4.0), end=None, text="¿Cómo hace el patito? 🐣",
        plan=[["H1", 0.25, 1.40], ["H1", 1.70, 5.00],
              ("P1a", 0.30, 5.18, 0.66, ev["patito"]["baby_sound_out_t"], 1.0),
              ["P1a", 2.90, 5.18], ["H1", 2.00, 5.00],
              ("P1b", 0.55, 5.18, 1.96, ev["patito"]["mama_sound_out_t"], 1.0)]),
    "gatito": dict(start=out_t(20.9), end=None, text="¿Cómo hace el gatito? 🐱",
        plan=[["H1", 0.25, 1.40], ["H1", 1.70, 5.00],
              ("P2a", 0.05, 2.95, 2.82, ev["gatito"]["baby_sound_out_t"], 1.0),
              ["P2a", 3.95, 5.18], ["B1", 0.30, 5.00], ["H1", 2.00, 5.00], ["P2a", 0.05, 2.50],
              ("P2b", 0.00, 3.30, 0.20, ev["gatito"]["mama_sound_out_t"], 1.0)]),
    "ratoncito": dict(start=out_t(38.7), end=None, text="¿Cómo hace el ratoncito? 🐭",
        plan=[["H1", 0.25, 1.40], ["H1", 1.70, 5.00],
              ("P3a", 1.30, 2.45, 1.35, ev["ratoncito"]["baby_sound_out_t"], 1.0),
              ["P3a", 2.65, 5.18], ["B1", 0.30, 5.00], ["H1", 2.00, 5.00], ["P3a", 0.05, 1.15],
              ("P3b", 0.30, 3.50, 0.55, ev["ratoncito"]["mama_sound_out_t"], 1.0)]),
    "elefantito": dict(start=out_t(55.8), end=None, text="¿Cómo hace Tito? 🐘",
        plan=[["H1", 0.25, 1.40], ["H1", 1.70, 5.00],
              ("F1", 0.75, 5.18, 1.10, ev["elefantito"]["baby_sound_out_t"], 1.0),
              ["H1", 2.00, 5.00], ["B1", 0.30, 5.00], ["F1", 0.75, 3.00],
              ("F2", 1.25, 2.40, 1.50, ev["elefantito"]["mama_sound_out_t"] + 0.0, 0.8)]),
}


def plan_short(k):
    s = S[k]
    t0 = up(s["start"] - 0.15) - B  # one beat of lead-in before the question
    cuts, pending, t = [], [], t0
    for item in s["plan"]:
        if isinstance(item, list):
            pending.append(item)
            continue
        c, ci, co, on, snd, sp = item
        b0 = up(snd - (on - ci) / sp)            # first beat where the clean window has begun
        b1 = dn(snd + (co - on) / sp)            # last beat inside the clean window
        gap = b0 - t
        # fillers: whole beats each, proportional to their length; speed >= 0.85
        tot = sum(f[2] - f[1] for f in pending)
        if gap > 1e-6:
            if tot < 0.85 * gap - 1e-6:
                raise SystemExit(f"{k}: {gap:.2f}s of picture needed before {c}, only {tot:.2f}s of clean motion (>=0.85x)")
            nb = round(gap / B)
            alloc = [max(1, round(nb * (f[2] - f[1]) / tot)) for f in pending]
            while sum(alloc) > nb:
                alloc[alloc.index(max(alloc))] -= 1
            while sum(alloc) < nb:
                i = max(range(len(pending)), key=lambda j: (pending[j][2] - pending[j][1]) - alloc[j] * B)
                alloc[i] += 1
            for f, n in zip(pending, alloc):
                d = n * B
                spd = min(1.0, (f[2] - f[1]) / d)
                if spd < 0.85 - 1e-6:
                    raise SystemExit(f"{k}: filler {f} would need {spd:.2f}x")
                cuts.append(dict(src=f[0], out0=t, out1=t + d, cin=f[1], speed=round(spd, 3), sync=None))
                t += d
        pending = []
        cin = on - (snd - b0) * sp
        cuts.append(dict(src=c, out0=b0, out1=b1, cin=cin, speed=sp, sync=snd))
        t = b1
    end = t
    return t0, end, cuts


run = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
BD = D / "build"
report = {}
for k in which:
    t0, end, cuts = plan_short(k)
    parts = []
    for i, c in enumerate(cuts):
        n = round((c["out1"] - t0) * FPS) - round((c["out0"] - t0) * FPS)
        p = BD / f"s2_{k}_{i:02d}.mp4"
        run("-ss", f"{c['cin']:.4f}", "-i", str(WV / f"{c['src']}_minimax.mp4"), "-vf",
            f"setpts=PTS/{c['speed']},scale=-2:1920:flags=lanczos,crop=1080:1920,fps={FPS}", "-an",
            "-frames:v", str(n), "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), str(p))
        parts.append(p)
    lst = BD / f"s2_{k}.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    dur = end - t0
    wav = BD / f"s2_{k}.wav"
    run("-i", mix, "-af", f"atrim={t0:.4f}:{end:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.25,afade=t=out:st={dur - 0.25:.3f}:d=0.25", str(wav))
    raw = BD / f"s2_{k}_raw.mp4"
    run("-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
        "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(raw))
    tt = str(ROOT / "production/tiktok_text.py")
    t1 = BD / f"s2_{k}_t1.mp4"
    out = ROOT / f"production/deliver/tito_como_hace_tiktok_{k}.mp4"
    subprocess.run([sys.executable, tt, str(raw), str(t1), S[k]["text"], "--until", "2.5", "--y", "0.14", "--size", "74"], check=True, capture_output=True)
    subprocess.run([sys.executable, tt, str(t1), str(out), "Más con Tito → YouTube 🐘", "--start", f"{dur - 2.5:.2f}", "--until",
                    f"{dur - 0.05:.2f}", "--y", "0.14", "--size", "64"], check=True, capture_output=True)
    rows = []
    for c in cuts:
        beat = (c["out0"] - G0) / B
        row = {"src": c["src"], "t": round(c["out0"] - t0, 3), "dur": round(c["out1"] - c["out0"], 3), "clip_in": round(c["cin"], 3),
               "speed": c["speed"], "cut_beat_err_ms": round((round((c["out0"] - t0) * FPS) / FPS - (c["out0"] - t0) + (beat - round(beat)) * B) * 1000)}
        if c["sync"]:
            on = next(x[3] for x in S[k]["plan"] if isinstance(x, tuple) and x[0] == c["src"])
            pic = round((c["out0"] - t0) * FPS) / FPS + (on - c["cin"]) / c["speed"]
            row["sync_offset_ms"] = round((pic - (c["sync"] - t0)) * 1000)
        rows.append(row)
    report[k] = {"master_slice": [round(t0, 3), round(end, 3)], "duration": round(dur, 2), "cuts": rows}
    print(k, round(dur, 2), "s,", len(cuts), "cuts")
mp = D / "shorts2_map.json"
old = json.load(open(mp)) if mp.exists() else {}
old.update(report)
json.dump(old, open(mp, "w"), indent=1)
