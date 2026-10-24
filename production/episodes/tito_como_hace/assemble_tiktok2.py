"""v2 of the "¿Cómo hace?" TikTok (researcher 24.10: v1 was ~68 s of stills -> retention FAIL). Rules:
every CLEAN second of each clip is used (forward only), the sound-sync windows keep their exact placement, any gap is
filled by alternating a still (<= 1.9 s hold) with forward idle windows of the clips; no still hold > 2.0 s.
Clean windows (8 fps checks): P1a 0.30-5.18 | P1b 0.55-5.18 | P2a 0.05-2.95, 3.95-5.18 (fangs 2.9-3.7 out) |
P2b 0.0-3.3 | P3a 0.05-1.15, 1.30-2.45, 2.65-5.18 (winks out) | P3b 0.3-3.5 | H1 0.25-1.4, 1.7-5.0 | F1 0.75-5.18 |
F2 1.25-2.4 only (0.8x).
    python assemble_tiktok2.py <mix.wav> <out.mp4> [--no-mouse]   (--no-mouse = v1b: the ratón pair cut on bar lines)
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image

D = Path(__file__).parent
WV = D.parents[1] / "review" / "como_hace_weave"
FPS, W, H = 30, 1080, 1920
mix_wav, out_mp4 = sys.argv[1:3]
NO_MOUSE = "--no-mouse" in sys.argv
M = json.load(open(D / "mix_map.json"))
BEAT, GRID0 = M["beat"], 1.93
ev = {p["pair"]: dict(p) for p in M["pairs"]}
INS = [p["insert_song_t"] for p in M["pairs"]]


def out_t(song_t):
    return song_t + sum(4 * BEAT for s in INS if s < song_t)


Q = {"patito": 4.0, "gatito": 20.9, "ratoncito": 38.7, "elefantito": 55.8}
ANS = {"patito": 8.5, "gatito": 25.3, "ratoncito": 42.6, "elefantito": 58.5}
MQ = {"patito": 12.1, "gatito": 29.4, "ratoncito": 46.4, "elefantito": 63.6}
T = {k: {"q": out_t(Q[k]), "ans": out_t(ANS[k]), "mq": out_t(MQ[k]),  # out_t already counts this pair's own insert
         "bs": ev[k]["baby_sound_out_t"], "ms": ev[k]["mama_sound_out_t"]} for k in Q}
END = M["duration"]
order = ["patito", "gatito", "ratoncito", "elefantito"]
y, sr = sf.read(mix_wav)
if NO_MOUSE:  # cut [ratón question, elefantito question) on the beat grid: a whole number of bars keeps the bar phase
    g = lambda t: GRID0 + round((t - GRID0) / BEAT) * BEAT
    a = g(T["ratoncito"]["q"] - 0.15)
    b = a + round((g(T["elefantito"]["q"] - 0.15) - a) / (4 * BEAT)) * 4 * BEAT
    cut = b - a
    xf = int(0.02 * sr)
    ia, ib = int(a * sr), int(b * sr)
    r = np.linspace(0, 1, xf)[:, None] if y.ndim > 1 else np.linspace(0, 1, xf)
    y = np.concatenate([y[:ia], y[ia:ia + xf] * (1 - r) + y[ib:ib + xf] * r, y[ib + xf:]])
    mix_wav = str(Path(out_mp4).with_suffix(".wav"))
    sf.write(mix_wav, y, sr)
    order.remove("ratoncito")
    for k in T["elefantito"]:
        T["elefantito"][k] -= cut
    END -= cut
    print("v1b: cut", round(a, 3), "->", round(b, 3), f"({cut:.3f} s = {cut / (4 * BEAT):.2f} bars), new end {END:.2f}")
for i, k in enumerate(order):
    T[k]["next"] = T[order[i + 1]]["q"] if i + 1 < len(order) else None

P = {  # baby sync (clip, in, out, onset), baby idle windows, answer clip (under the sung answer), T still, stills, mamá sync
    # pools: q = before the baby sync, a = baby sync -> "¿Y su mamá?", m = "¿Y su mamá?" -> mamá sync, n = after -> next pair
    "patito": dict(baby=("P1a", 0.30, 1.55, 0.66), ansclip=("P1a", 2.9, 4.66), T="T1_kf2", kb="P1a_kf2", km="P1b_kf",
                   mama=("P1b", 0.55, 5.18, 1.96), q=["P1a_kf2", ("P1a", 3.6, 5.18)], a=["T1_kf2", "P1a_kf2"],
                   m=["P1b_kf", "T1_kf2"], n=["P1b_kf", "T1_kf2"]),
    "gatito": dict(baby=("P2a", 0.05, 2.95, 2.82), ansclip=None, T="T2_kf", kb="P2a_kf", km="P2b_kf",
                   mama=("P2b", 0.0, 3.3, 0.2), q=["P2a_kf", "T2_kf"], a=["T2_kf", ("P2a", 3.95, 5.18), "P2a_kf"],
                   m=["P2b_kf", ("P2a", 0.05, 2.5)], n=["P2b_kf", "T2_kf"]),
    "ratoncito": dict(baby=("P3a", 1.30, 2.45, 1.35), ansclip=None, T="T3_kf2", kb="P3a_kf", km="P3b_kf",
                      mama=("P3b", 0.3, 3.5, 0.55), q=["P3a_kf", ("P3a", 0.05, 1.15)], a=["T3_kf2", ("P3a", 2.65, 5.18), "P3a_kf"],
                      m=["P3b_kf", ("P3a", 2.65, 5.18)], n=["P3b_kf", "T3_kf2"]),
    "elefantito": dict(baby=("F1", 0.75, 5.18, 1.10), ansclip=None, T="F1_kf2", kb="F1_kf2", km="F2_kf3", mama=None,
                       q=["F1_kf2", ("H1", 2.0, 5.0)], a=["F1_kf2", ("F1", 0.75, 2.75)], m=["F2_kf3", "F1_kf2"], n=[]),
}
seg = []  # (kind, src, out0, out1, clip_in, speed)


def fill(a, b, pool):
    """alternate stills (<= 1.9 s) and forward idle windows over [a, b); never the same source twice in a row"""
    pool = [list(p) if isinstance(p, tuple) else p for p in pool]
    t, i = a, 0
    last = seg[-1][1] if seg else None
    while b - t > 1e-3:
        live = [p for p in pool if isinstance(p, str) or p[2] - p[1] > 0.3]
        if not live:
            break
        cand = [p for p in live if (p if isinstance(p, str) else p[0]) != last] or live
        p = cand[i % len(cand)]
        rem = b - t
        if isinstance(p, str):
            d = min(1.9, rem)
            if 0 < rem - d < 0.35:
                d = rem if rem <= 2.0 else rem - 0.35
            seg.append(("still", p, t, t + d))
            last = p
        else:
            d = min(p[2] - p[1], rem)
            if 0 < rem - d < 0.35 and rem <= p[2] - p[1] + 0.35:
                d = min(rem, p[2] - p[1])
            seg.append(("clip", p[0], t, t + d, p[1], 1.0))
            p[1] += d
            last = p[0]
        t += d
        i += 1


seg += [("clip", "H1", 0.0, 1.15, 0.25, 1.0), ("clip", "H1", 1.15, 4.0, 1.70, 1.0)]
for k in order:
    p, t = P[k], T[k]
    c, w0, w1, on = p["baby"]
    c0 = t["bs"] - (on - w0)
    c1 = c0 + (w1 - w0)
    fill(t["q"], c0, p["q"])
    seg.append(("clip", c, c0, c1, w0, 1.0))
    if k == "elefantito":
        fill(c1, t["mq"], p["a"])
        f0 = t["ms"] - 0.25
        f1 = f0 + 1.15 / 0.8
        fill(t["mq"], f0, p["m"])
        seg.append(("clip", "F2", f0, f1, 1.25, 0.8))
        recap = [("P1b", 1.9), ("P2b", 0.0)] + ([("P3b", 0.3)] if "ratoncito" in order else [])
        r = (END - f1) / len(recap)
        for j, (rc, ri) in enumerate(recap):
            seg.append(("clip", rc, f1 + j * r, f1 + (j + 1) * r, ri, 1.0))
        break
    if p["ansclip"]:
        ac, a0, a1 = p["ansclip"]
        fill(c1, t["ans"], p["a"])
        e = min(t["ans"] + (a1 - a0), t["mq"])
        seg.append(("clip", ac, t["ans"], e, a0, 1.0))
        fill(e, t["mq"], p["a"])
    else:
        fill(c1, t["mq"], p["a"])
    mc, m0, m1, mon = p["mama"]
    d0 = t["ms"] - (mon - m0)
    d1 = min(d0 + (m1 - m0), t["next"])
    fill(t["mq"], d0, p["m"])
    seg.append(("clip", mc, d0, d1, m0, 1.0))
    fill(d1, t["next"], p["n"])


def fr(x):
    return int(round(x * FPS))


def still_frames(img, a, b):
    im = Image.open(WV / f"{img}.jpg").convert("RGB")
    base = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
    n = fr(b) - fr(a)
    for i in range(n):
        t = (fr(a) + i) / FPS
        z = 1 + 0.03 * i / max(1, n - 1)
        kk = (t - GRID0) / BEAT
        if int(round(kk)) % 2 == 0:
            z *= 1 + 0.04 * max(0, 1 - abs(kk - round(kk)) * BEAT * FPS / 2)
        w, h = int(base.width * z), int(base.height * z)
        s = base.resize((w, h), Image.BILINEAR)
        x = (w - W) // 2
        yy = max(0, min(h - H, h - H - max(0, (base.height - H) // 2)))
        yield np.asarray(s.crop((x, yy, x + W, yy + H)), dtype=np.uint8)


with tempfile.TemporaryDirectory() as td:
    parts, log = [], []
    for i, s in enumerate(seg):
        kind, src, a, b = s[:4]
        n = fr(b) - fr(a)
        if n <= 0:
            continue
        pth = Path(td) / f"s{i:03d}.mp4"
        enc = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-frames:v", str(n), str(pth)]
        if kind == "clip":
            vf = f"setpts=PTS/{s[5]},scale=-2:{H}:flags=lanczos,crop={W}:{H},unsharp=5:5:0.4:5:5:0.0,fps={FPS}"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s[4]:.3f}", "-i", str(WV / f"{src}_minimax.mp4"), "-vf", vf, "-an", *enc], check=True)
        else:
            pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *enc],
                                  stdin=subprocess.PIPE)
            for f in still_frames(src, a, b):
                pr.stdin.write(f.tobytes())
            pr.stdin.close()
            pr.wait()
        parts.append(pth)
        log.append({"kind": kind, "src": src, "out": [round(a, 3), round(b, 3)], "dur": round(b - a, 3),
                    **({"in": round(s[4], 3), "speed": s[5]} if kind == "clip" else {})})
    (Path(td) / "list.txt").write_text("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(Path(td) / "list.txt"), "-i", mix_wav, "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "alimiter=limit=0.84:level=false", "-shortest",
                    "-movflags", "+faststart", out_mp4], check=True)
sync = []
for k in order:
    for key, which in (("bs", "baby"), ("ms", "mama")):
        cl = P[k][which]
        if not cl:
            continue
        sg = next(s for s in seg if s[0] == "clip" and s[1] == cl[0] and s[2] - 1e-6 <= T[k][key] <= s[3] and s[4] <= cl[3])
        pic = fr(sg[2]) / FPS + (cl[3] - sg[4])
        sync.append({"event": f"{k}/{cl[0]}", "sound_t": round(T[k][key], 3), "picture_t": round(pic, 3), "offset_ms": round((pic - T[k][key]) * 1000)})
still_t = sum(l["dur"] for l in log if l["kind"] == "still")
summary = {"duration": round(END, 2), "still_seconds": round(still_t, 2), "clip_seconds": round(END - still_t, 2),
           "max_still_hold": max(l["dur"] for l in log if l["kind"] == "still"),
           "min_segment": min(l["dur"] for l in log), "same_src_in_a_row": sum(a["src"] == b["src"] and a["kind"] == b["kind"] == "still" for a, b in zip(log, log[1:])),
           "sync": sync}
json.dump({"summary": summary, "segments": log}, open(Path(out_mp4).with_suffix(".log.json"), "w"), indent=1)
print(json.dumps(summary, indent=1))
