"""Halloween dance TikTok: beat-lock MC2 to the chorus (researcher 25.10).
Music = tito_ep4_halloween song 20.319 s + 20 beats, rubberband tempo x1.0909 (110 -> 120 bpm, beat 0.5 s) = build/audio_120.wav.
Anchors = dance hits (motion minima) of MC2_raw, chosen by a small DP so every anchor lands on a beat and every
segment plays at 0.7-0.97x. Source = MC2 interpolated to 120 fps in two parts (A: 0-4.4 s, B: 4.2-8.4 s).
    python warp.py <A120.mp4> <B120.mp4> <out_silent.mp4>
"""
import subprocess
import sys

A_SRC, B_SRC, OUT = sys.argv[1:4]
W, H, FIN, FOUT, BEAT, B_OFF, SPLIT = 1080, 1920, 120, 30, 0.5, 4.2, 4.3
HITS = [0.2, 0.6, 0.87, 1.33, 1.7, 2.3, 2.67, 3.17, 3.53, 3.87, 4.3, 4.73, 5.13, 5.5, 5.9, 6.27, 6.97, 7.33, 7.8, 8.17]
PATH = [(0, 1), (1, 2), (3, 2), (5, 1), (6, 2), (8, 2), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 2), (16, 2), (18, 1), (19, 0)]
segs, b = [], 0
for (i, n), (j, _) in zip(PATH, PATH[1:]):
    segs.append((HITS[i], HITS[j], b * BEAT, (b + n) * BEAT))
    b += n
for s in segs:
    print(f"src {s[0]:.2f}-{s[1]:.2f} -> {s[2]:.2f}-{s[3]:.2f}  {(s[1] - s[0]) / (s[3] - s[2]):.2f}x")
n_out = int(round(b * BEAT * FOUT))
src_t = []
for k in range(n_out):
    t = k / FOUT
    s = next((s for s in segs if s[2] <= t < s[3]), segs[-1])
    src_t.append(s[0] + (t - s[2]) / (s[3] - s[2]) * (s[1] - s[0]))


def reader(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                            stdout=subprocess.PIPE)


enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FOUT),
                        "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", OUT],
                       stdin=subprocess.PIPE)
size = W * H * 3
cur_part, dec, idx, frame = None, None, -1, None
for t in src_t:  # monotonic
    part, off = ("A", 0.0) if t < SPLIT else ("B", B_OFF)
    if part != cur_part:
        if dec:
            dec.kill()
        dec, idx, cur_part = reader(A_SRC if part == "A" else B_SRC), -1, part
    want = int(round((t - off) * FIN))
    while idx < want:
        buf = dec.stdout.read(size)
        if len(buf) < size:
            break
        frame, idx = buf, idx + 1
    enc.stdin.write(frame)
enc.stdin.close()
enc.wait()
dec.kill()
print("frames", n_out)
