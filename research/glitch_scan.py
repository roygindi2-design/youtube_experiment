"""Find sudden local changes (eye 'pops', parts appearing through the trunk, face warps) in the USED part of each clip.

    python3 research/glitch_scan.py <edit.json> <out_dir> [top=16]

For every shot in the edit (file, in, dur): every frame, dense optical flow from the previous frame, warp it, and
take the max residual over 24x24 tiles (a small region that changed without moving = something popped).
Writes <out_dir>/events.json and contact sheets: each row = previous | suspect | next frame + a 3x zoom of the tile.
Heuristic for the researcher's visual review — final say is the eye.
"""
import json, sys
from pathlib import Path
import cv2, numpy as np

edit, out = Path(sys.argv[1]), Path(sys.argv[2]); top = int(sys.argv[3]) if len(sys.argv) > 3 else 16
out.mkdir(parents=True, exist_ok=True)
e = json.loads(edit.read_text()); seen = {}; events = []
for k, sh in enumerate(e["shots"]):
    f = sh["file"]; key = (f, round(sh.get("in", 0), 2))
    if key in seen or not Path(f).exists(): continue
    seen[key] = 1
    cap = cv2.VideoCapture(f); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    a, b = sh.get("in", 0), sh.get("in", 0) + sh.get("dur", 4) * sh.get("speed", 1)
    frames = []; i = int(a * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    while True:
        ok, fr = cap.read()
        if not ok: break
        t = i / fps; i += 1
        if t > b: break
        if a <= t: frames.append((t, cv2.resize(fr, (640, int(fr.shape[0] * 640 / fr.shape[1]))) if fr.shape[1] > 640 else fr))
    scores = []
    for j in range(1, len(frames)):
        p = cv2.cvtColor(frames[j - 1][1], cv2.COLOR_BGR2GRAY); c = cv2.cvtColor(frames[j][1], cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(p, c, None, 0.5, 3, 21, 3, 5, 1.1, 0)
        h, w = p.shape; gx, gy = np.meshgrid(np.arange(w), np.arange(h))
        warped = cv2.remap(p, (gx - flow[..., 0]).astype(np.float32), (gy - flow[..., 1]).astype(np.float32), cv2.INTER_LINEAR)
        res = cv2.absdiff(warped, c).astype(np.float32)
        T = 24; tiles = res[:h // T * T, :w // T * T].reshape(h // T, T, w // T, T).mean(axis=(1, 3))
        y, x = np.unravel_index(np.argmax(tiles), tiles.shape)
        scores.append((float(tiles.max()), float(np.median(tiles)), j, int(x * T), int(y * T)))
    if not scores: continue
    mm = np.median([s[1] for s in scores]) + 1e-6
    scores = [s for s in scores if s[1] < 4 * mm]  # drop scene cuts (whole frame changes)
    if not scores: continue
    med = np.median([s[0] for s in scores]) + 1e-6
    for s in sorted(scores, reverse=True)[:2]:
        events.append({"shot": Path(f).name, "slot": k, "t": round(frames[s[2]][0], 2), "peak": round(s[0], 1),
                       "rel": round(s[0] / med, 2), "x": s[3], "y": s[4], "file": f, "j": s[2]})
events.sort(key=lambda r: -r["rel"])
(out / "events.json").write_text(json.dumps(events, indent=1))
rows = []
for ev in events[:top]:
    cap = cv2.VideoCapture(ev["file"]); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    tgt = int(round(ev["t"] * fps)); imgs = []; sc0 = cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 640 if cap.get(cv2.CAP_PROP_FRAME_WIDTH) > 640 else 1
    ev = {**ev, "x": int(ev["x"] * sc0), "y": int(ev["y"] * sc0)}
    for d in (-1, 0, 1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(tgt + d, 0)); ok, fr = cap.read()
        imgs.append(fr if ok else np.zeros_like(imgs[-1]))
    H = 220; sc = H / imgs[1].shape[0]
    small = [cv2.resize(im, (int(im.shape[1] * sc), H)) for im in imgs]
    x0, y0 = max(ev["x"] - 36, 0), max(ev["y"] - 36, 0)
    crop = imgs[1][y0:y0 + 96, x0:x0 + 96]; crop = cv2.resize(crop, (H, H), interpolation=cv2.INTER_NEAREST)
    cv2.rectangle(small[1], (int(x0 * sc), int(y0 * sc)), (int((x0 + 96) * sc), int((y0 + 96) * sc)), (0, 0, 255), 2)
    row = np.hstack(small + [crop])
    cv2.putText(row, f"{ev['shot'][:28]} t={ev['t']} x{ev['rel']}", (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    rows.append(row)
W = max(r.shape[1] for r in rows)
rows = [np.pad(r, ((0, 0), (0, W - r.shape[1]), (0, 0))) for r in rows]
for k in range(0, len(rows), 6):
    cv2.imwrite(str(out / f"sheet_{k // 6}.jpg"), np.vstack(rows[k:k + 6]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(len(events), "events; top:", [(ev["shot"][-14:], ev["t"], ev["rel"]) for ev in events[:top]])
