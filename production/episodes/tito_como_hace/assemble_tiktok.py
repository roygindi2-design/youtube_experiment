"""Assemble the "¿Cómo hace?" TikTok cut (researcher plan 24.10): audio = mix_tiktok_cut_v2 (80.08 s); picture =
MiniMax clip WINDOWS (researcher-passed) placed so the mouth/beak-open frame lands on its real sound (mix_map.json),
plus Nano Banana stills animated in the edit (3% push-in + a 4-frame 1.00->1.04->1.00 squash-bounce on every other beat,
anchored at the bottom). 1080x1920, 30 fps; clips: lanczos upscale + light unsharp, 24->30 by frame duplication.
    python assemble_tiktok.py <mix.wav> <out.mp4>
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

D = Path(__file__).parent
WV = D.parents[1] / "review" / "como_hace_weave"
FPS, W, H = 30, 1080, 1920
mix_wav, out_mp4 = sys.argv[1:3]
M = json.load(open(D / "mix_map.json"))
BEAT = M["beat"]
GRID0 = 1.93  # first tracked beat of the accompaniment (inserts are whole bars, so the grid stays in phase)
ev = {p["pair"]: p for p in M["pairs"]}
# clip windows (clip time) + the mouth-open onset inside it (measured 12-24 fps)
CL = {"P1a": (0.30, 1.55, 0.66), "P2a": (2.60, 2.95, 2.82), "P3a": (1.30, 1.70, 1.35), "F1": (0.75, 2.75, 1.10),
      "P1b": (1.90, 3.00, 1.96), "P2b": (0.00, 1.50, 0.20), "P3b": (0.30, 1.50, 0.55)}
INS = [p["insert_song_t"] for p in M["pairs"]]


def out_t(song_t):  # song time -> output time
    return song_t + sum(4 * BEAT for s in INS if s < song_t)


Q = {"patito": 4.0, "gatito": 20.9, "ratoncito": 38.7, "elefantito": 55.8}          # "<animal> chiquitito"
ANS = {"patito": 8.5, "gatito": 25.3, "ratoncito": 42.6, "elefantito": 58.5}        # the sung answer
MQ = {"patito": 12.1, "gatito": 29.4, "ratoncito": 46.4, "elefantito": 63.6}        # "¿Y su mamá?"
KF = {"patito": ("P1a_kf2", "T1_kf2", "P1b_kf"), "gatito": ("P2a_kf", "T2_kf", "P2b_kf"),
      "ratoncito": ("P3a_kf", "T3_kf2", "P3b_kf"), "elefantito": ("F1_kf2", "F1_kf2", "F2_kf3")}
CLIP = {"patito": ("P1a", "P1b"), "gatito": ("P2a", "P2b"), "ratoncito": ("P3a", "P3b"), "elefantito": ("F1", None)}
END = M["duration"]
seg = [("clip", "H1", 0.0, 1.15, 0.25, 1.0), ("clip", "H1", 1.15, 4.0, 1.70, 1.0)]  # (kind, src, out0, out1, in, speed)
order = ["patito", "gatito", "ratoncito", "elefantito"]
for n, a in enumerate(order):
    e = ev[a]
    q0, ins, bs, ans, mq, ms = out_t(Q[a]), e["insert_out_t"], e["baby_sound_out_t"], out_t(ANS[a]) + 4 * BEAT, out_t(MQ[a]) + 4 * BEAT, e["mama_sound_out_t"]
    nxt = out_t(Q[order[n + 1]]) if n < 3 else None
    kq, kt, km = KF[a]
    cb, cm = CLIP[a]
    w0, w1, on = CL[cb]
    c0 = bs - (on - w0)
    c1 = min(c0 + (w1 - w0), ans if a != "elefantito" else mq)
    seg += [("still", kq, q0, c0), ("clip", cb, c0, c1, w0, 1.0)]
    if c1 < ans:
        seg.append(("still", kq, c1, ans))
    seg.append(("still", kt, max(c1, ans), mq))
    if cm:
        w0, w1, on = CL[cm]
        d0 = ms - (on - w0)
        d1 = d0 + (w1 - w0)
        seg += [("still", km, mq, d0), ("clip", cm, d0, d1, w0, 1.0), ("still", km, d1, nxt)]
    else:  # finale: F2 window 1.25-2.4 at 0.8x on Mamá's TUUU, then the recap montage of the three pair windows
        f0 = ms - 0.25
        f1 = f0 + 1.15 / 0.8
        r = (END - f1) / 3
        seg += [("still", km, mq, f0), ("clip", "F2", f0, f1, 1.25, 0.8),
                ("clip", "P1b", f1, f1 + r, 1.90, 1.0), ("clip", "P2b", f1 + r, f1 + 2 * r, 0.0, 1.0),
                ("clip", "P3b", f1 + 2 * r, END, 0.30, 1.0)]


def fr(t):
    return int(round(t * FPS))


def still_frames(img, a, b):
    im = Image.open(WV / f"{img}.jpg").convert("RGB")
    base = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
    n = fr(b) - fr(a)
    for i in range(n):
        t = (fr(a) + i) / FPS
        z = 1 + 0.03 * i / max(1, n - 1)
        k = (t - GRID0) / BEAT
        if int(round(k)) % 2 == 0:
            d = abs(k - round(k)) * BEAT * FPS  # frames from the beat
            z *= 1 + 0.04 * max(0, 1 - d / 2)
        w, h = int(base.width * z), int(base.height * z)
        s = base.resize((w, h), Image.BILINEAR)
        x = (w - W) // 2
        y = h - H - max(0, (base.height - H) // 2)  # anchored at the bottom
        y = max(0, min(h - H, y))
        yield np.asarray(s.crop((x, y, x + W, y + H)), dtype=np.uint8)


with tempfile.TemporaryDirectory() as td:
    parts, log = [], []
    for i, s in enumerate(seg):
        kind, src, a, b = s[:4]
        n = fr(b) - fr(a)
        if n <= 0:
            continue
        p = Path(td) / f"s{i:03d}.mp4"
        enc = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-frames:v", str(n), str(p)]
        if kind == "clip":
            w0, sp = s[4], s[5]
            vf = f"setpts=PTS/{sp},scale=-2:{H}:flags=lanczos,crop={W}:{H},unsharp=5:5:0.4:5:5:0.0,fps={FPS}"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{w0:.3f}", "-i", str(WV / f"{src}_minimax.mp4"), "-vf", vf, "-an", *enc], check=True)
        else:
            pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                                   "-i", "-", *enc], stdin=subprocess.PIPE)
            for f in still_frames(src, a, b):
                pr.stdin.write(f.tobytes())
            pr.stdin.close()
            pr.wait()
        parts.append(p)
        log.append({"kind": kind, "src": src, "out": [round(a, 3), round(b, 3)], "frames": n})
    lst = Path(td) / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", mix_wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "alimiter=limit=0.84:level=false", "-shortest", "-movflags", "+faststart", out_mp4], check=True)
sync = []
for a in order:
    e = ev[a]
    cb, cm = CLIP[a]
    for c, t in ((cb, e["baby_sound_out_t"]), (cm, e["mama_sound_out_t"])):
        if not c:
            continue
        sg = next(s for s in seg if s[0] == "clip" and s[1] == c and s[2] <= t <= s[3])
        pic = fr(sg[2]) / FPS + (CL[c][2] - sg[4])
        sync.append({"event": f"{a}/{c}", "sound_t": t, "mouth_open_picture_t": round(pic, 3), "offset_ms": round((pic - t) * 1000)})
json.dump({"segments": log, "sync": sync}, open(D / "assemble_log.json", "w"), indent=1)
print(json.dumps(sync, indent=1))
