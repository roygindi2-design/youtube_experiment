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
# walking-in-place hint: per segment, centre motion vs background (top band + side strips) motion
import cv2 as _c
cuts = [0] + [i for i in range(1, n) if diff[i] > 13] + [n]
wip = []
for a, b in zip(cuts[:-1], cuts[1:]):
    if b - a < 15: continue
    cen = []; bg = []
    for i in range(a + 2, b, 3):
        fl = _c.calcOpticalFlowFarneback(fr[i-2].astype(np.uint8), fr[i].astype(np.uint8), None, 0.5, 2, 9, 2, 5, 1.1, 0)
        m = np.linalg.norm(fl, axis=2)
        cen.append(m[14:50, 30:66].mean()); bg.append(np.concatenate([m[:12].ravel(), m[:, :14].ravel(), m[:, -14:].ravel()]).mean())
    c, g = float(np.mean(cen)), float(np.mean(bg))
    if c > 0.35 and g < 0.08 * 1 + 0.15 * c:   # character moves a lot, background almost frozen
        wip.append((round(a/fps, 1), round((b-a)/fps, 1), round(c, 2), round(g, 2)))
res["in_place_candidates"] = wip
# ping-pong per segment: a moving frame that matches a frame 0.2-3 s earlier in the same shot
pp = []
for a, b in zip(cuts[:-1], cuts[1:]):
    cnt = 0
    for i in range(a + 9, b):
        if diff[i] <= 0.4: continue
        for k in range(6, min(90, i - a)):
            if np.mean(np.abs(fr[i] - fr[i-k])) < 0.5 * diff[i]:
                cnt += 1; break
    if cnt > 5: pp.append((round(a/fps, 1), round((b-a)/fps, 1), cnt))
res["pingpong_segments"] = pp
print("ping-pong segments (start, len, loop frames) — any = FAIL:", pp)
print("in-place candidates (start, len, centre, bg) — check: if the line is a WALK this is FAIL; joy/dance in place is OK:", wip)
if len(sys.argv) > 2: json.dump(res, open(sys.argv[2], "w"), indent=1)
