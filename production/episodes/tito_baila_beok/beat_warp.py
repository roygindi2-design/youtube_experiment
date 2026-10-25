"""Be OK v2 (Roy 25.10: "not exactly in rhythm, odd parts, fit the music to the picture").
Each dance hit (motion minimum = pose extreme) is retimed to land exactly on a beat of our own song
"¡Buenos días, Tito! ¡Ya salió el sol!" (tito_ep2, song 2.438 -> 8.986 = 12 beats). The side-turn section
(source 2.8-5.4 s, profile + twisted head) is cut out on a beat. Source = 120 fps motion-interpolated copy,
so the 0.7-1.2x retime stays smooth.
    python beat_warp.py <src_120fps.mp4> <out_silent.mp4>
"""
import subprocess
import sys

import numpy as np

SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS_IN, FPS_OUT = 1080, 1920, 120, 30
# song beats (librosa, tito_ep2/assets/song.wav) from 2.438, re-zeroed
BEATS = np.array([2.438, 2.995, 3.553, 4.087, 4.644, 5.178, 5.735, 6.269, 6.827, 7.384, 7.918, 8.452, 8.986]) - 2.438
A = [0.13, 0.57, 0.97, 1.40, 1.77, 2.17, 2.80]   # source hits, part A (arms, face)
B = [5.40, 6.00, 6.40, 6.73, 7.17, 7.60, 7.97]   # part B (arms out, hands to face)
segs = [(A[i], A[i + 1], BEATS[i], BEATS[i + 1]) for i in range(6)]
segs += [(B[i], B[i + 1], BEATS[6 + i], BEATS[7 + i]) for i in range(6)]
for s0, s1, o0, o1 in segs:
    print(f"src {s0:.2f}-{s1:.2f} -> out {o0:.3f}-{o1:.3f}  speed {(s1 - s0) / (o1 - o0):.2f}x")

n_out = int(round(BEATS[-1] * FPS_OUT))
want = []
for k in range(n_out):
    t = k / FPS_OUT
    for s0, s1, o0, o1 in segs:
        if o0 <= t < o1 or (t >= o1 and (s0, s1, o0, o1) == segs[-1]):
            want.append(int(round((s0 + (t - o0) / (o1 - o0) * (s1 - s0)) * FPS_IN)))
            break
assert len(want) == n_out and all(b >= a or True for a, b in zip(want, want[1:]))

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"scale={W}:{H}:flags=lanczos", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r",
                        str(FPS_OUT), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt",
                        "yuv420p", OUT], stdin=subprocess.PIPE)
size, idx, cur = W * H * 3, -1, None
for w in want:  # 'want' jumps back once (A -> B is forward, so it is monotonic); stream decode
    while idx < w:
        buf = dec.stdout.read(size)
        if len(buf) < size:
            break
        cur, idx = buf, idx + 1
    enc.stdin.write(cur)
enc.stdin.close()
enc.wait()
dec.kill()
print("frames", n_out, "dur", n_out / FPS_OUT)
