"""Dense frame sheet for the mandatory visual QC review (QC_RULES.md).

    python production/frame_sheet.py <video.mp4> <out.jpg> [--fps 6] [--cols 8] [--width 200] [--start 0] [--end 999]

Every sampled frame is labeled with its time, so a glitch can be traced back to the exact shot and second.
"""
import argparse

import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("out")
ap.add_argument("--fps", type=float, default=6)
ap.add_argument("--cols", type=int, default=8)
ap.add_argument("--width", type=int, default=200)
ap.add_argument("--start", type=float, default=0)
ap.add_argument("--end", type=float, default=1e9)
a = ap.parse_args()

cap = cv2.VideoCapture(a.video)
src_fps = cap.get(cv2.CAP_PROP_FPS) or 24
step = max(1, round(src_fps / a.fps))
tiles, i = [], 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    t = i / src_fps
    if a.start <= t <= a.end and i % step == 0:
        h = int(f.shape[0] * a.width / f.shape[1])
        f = cv2.resize(f, (a.width, h), interpolation=cv2.INTER_AREA)
        cv2.rectangle(f, (0, 0), (62, 18), (0, 0, 0), -1)
        cv2.putText(f, f"{t:.2f}", (3, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        tiles.append(f)
    i += 1
if not tiles:
    raise SystemExit("no frames")
while len(tiles) % a.cols:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[r:r + a.cols]) for r in range(0, len(tiles), a.cols)]
cv2.imwrite(a.out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(a.out, len(tiles), "tiles")
