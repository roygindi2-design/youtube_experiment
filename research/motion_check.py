"""Find boomerang/ping-pong loops, frozen moments, and repeated frames in a final edit.
usage: python3 research/motion_check.py <video.mp4> [out.json]
- repeat: frame t looks almost identical to a NON-adjacent frame 0.3-3 s earlier (ping-pong / loop)
- static: <1 px-level motion for >=1.0 s
"""
import sys, json, cv2, numpy as np
v = sys.argv[1]; cap = cv2.VideoCapture(v); fps = cap.get(cv2.CAP_PROP_FPS)
fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (96, 54)).astype(np.float32))
n = len(fr); diff = [0.0] + [float(np.mean(np.abs(fr[i] - fr[i-1]))) for i in range(1, n)]
# scene cuts
cut = [i for i in range(1, n) if diff[i] > 18]
seg_start = lambda i: max([c for c in cut if c <= i] or [0])
rep = []
for i in range(n):
    s = seg_start(i); best = None
    for k in range(int(0.3*fps), int(3*fps)):
        j = i - k
        if j < s: break
        d = float(np.mean(np.abs(fr[i] - fr[j])))
        if d < 0.6 and diff[i] > 0.3:  # moving now, yet same as an earlier frame = loop back
            best = (j, d); break
    if best: rep.append(i)
# group into events
def groups(idx):
    out = []
    for i in idx:
        if out and i - out[-1][1] <= 2: out[-1][1] = i
        else: out.append([i, i])
    return [(round(a/fps, 2), round(b/fps, 2)) for a, b in out if b - a >= 3]
static = [i for i in range(1, n) if diff[i] < 0.25]
st = [(a, b) for a, b in groups(static) if b - a >= 1.0]
res = {"fps": fps, "frames": n, "cuts": [round(c/fps, 2) for c in cut],
       "loop_events": groups(rep), "static_events": st}
print("loop/ping-pong events:", len(res["loop_events"])); print(res["loop_events"])
print("static >=1s:", st)
if len(sys.argv) > 2: json.dump(res, open(sys.argv[2], "w"), indent=1)
