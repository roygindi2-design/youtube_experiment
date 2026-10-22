"""Find blinks/winks (and other 'there and back' pops) in clips.

    python3 research/blink_scan.py <clip.mp4> [...]

A blink is a small spot that changes and then returns: frame t differs from both t-k and t+k while t-k and t+k
look alike. Score per 16x16 tile = min(|t - (t-k)|, |t - (t+k)|) - |(t-k) - (t+k)|; prints time ranges where the max
tile score is high (with tile position). Heuristic for picking clean stretches — the final say is the eye.
"""
import sys, cv2, numpy as np

K, T, THR = 5, 16, 18.0

def frames(f):
    cap = cv2.VideoCapture(f); fps = cap.get(cv2.CAP_PROP_FPS) or 24; out = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        g = cv2.GaussianBlur(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), (5, 5), 0).astype(np.float32)
        out.append(g)
    return fps, out

def tiles(a):
    h, w = a.shape
    return a[:h // T * T, :w // T * T].reshape(h // T, T, w // T, T).mean(axis=(1, 3))

def scan(f):
    fps, fr = frames(f); res = []
    for t in range(K, len(fr) - K):
        a, b, c = fr[t - K], fr[t], fr[t + K]
        s = np.minimum(tiles(np.abs(b - a)), tiles(np.abs(b - c))) - tiles(np.abs(a - c))
        y, x = np.unravel_index(np.argmax(s), s.shape)
        res.append((t, float(s.max()), int(x * T), int(y * T)))
    return fps, res

if __name__ == "__main__":
    for f in sys.argv[1:]:
        fps, res = scan(f); rng = []
        for t, s, x, y in res:
            if s < THR: continue
            if rng and t - rng[-1][1] <= 3:
                rng[-1][1] = t; rng[-1][2] = max(rng[-1][2], s)
            else:
                rng.append([t, t, s, x, y])
        print(f.split("/")[-1].replace("tito_ep4_halloween_clip_", ""),
              " ".join(f"{a/fps:.2f}-{b/fps:.2f}(x{s:.0f}@{x},{y})" for a, b, s, x, y in rng) or "clean")
