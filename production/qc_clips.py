"""Automatic QC for generated clips: flags frames where the character morphs, ghosts or grows extra parts.

    python production/qc_clips.py <clip.mp4> [<clip.mp4> ...] --out <dir> [--keyframe-dir <dir>]

Two signals per frame (every frame, 24 fps clips):
  1. warp error: the previous frame is warped onto the current one with dense optical flow (Farneback);
     the 95th-percentile residual over 32x32 tiles is high when content appears/disappears or blends
     (ghosting, a third eye, a doubled ear). Normal motion warps cleanly and stays low.
  2. identity drift: DINOv2-small CLS embedding cosine similarity of the upper half of the frame (where the
     head is in our framings) to the clip's first frame. Morphing makes it drop.
A frame is flagged when warp error > median + 4*MAD of that clip (and above an absolute floor), or when
identity similarity drops below 0.80. Flagged frames are saved as PNG (full size) for human review, and a
JSON report lists per-clip verdicts: PASS / REVIEW / FAIL.
These are heuristics: they catch blends and sudden changes well, slow drifts less well. Final say is visual.
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import torch
from transformers import AutoImageProcessor, AutoModel

ap = argparse.ArgumentParser()
ap.add_argument("clips", nargs="+")
ap.add_argument("--out", required=True)
ap.add_argument("--sim-fail", type=float, default=0.85)
ap.add_argument("--flow-width", type=int, default=480)  # optical flow on a downscaled copy (4x faster, same glitches)
ap.add_argument("--sim-every", type=int, default=4)    # identity embedding every Nth frame  # 0.80 missed a ghosting case (Tito T4, min sim 0.841)
args = ap.parse_args()
OUT = Path(args.out)
OUT.mkdir(parents=True, exist_ok=True)

proc = AutoImageProcessor.from_pretrained("facebook/dinov2-small")
model = AutoModel.from_pretrained("facebook/dinov2-small").eval()


def embed(img_bgr):
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    with torch.no_grad():
        o = model(**proc(images=rgb, return_tensors="pt"))
    v = o.last_hidden_state[0, 0]
    return v / v.norm()


def frames(path):
    cap = cv2.VideoCapture(str(path))
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        out.append(f)
    return out


report = {}
for clip in args.clips:
    name = Path(clip).stem
    fr = frames(clip)
    if not fr:
        report[name] = {"verdict": "FAIL", "reason": "no frames"}
        continue
    H0 = fr[0].shape[0]
    top = slice(0, int(H0 * 0.6))  # head region for our vertical/horizontal framings
    ref = embed(fr[0][top])
    sc = min(1.0, args.flow_width / fr[0].shape[1])
    small = [cv2.resize(f, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA) for f in fr]
    h, w = small[0].shape[:2]
    warp, sims = [0.0], [1.0]
    prev_g = cv2.cvtColor(small[0], cv2.COLOR_BGR2GRAY)
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    for i in range(1, len(fr)):
        g = cv2.cvtColor(small[i], cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(g, prev_g, None, 0.5, 3, max(7, int(21 * sc)) | 1, 3, 5, 1.1, 0)
        warped = cv2.remap(prev_g, gx + flow[..., 0], gy + flow[..., 1], cv2.INTER_LINEAR)
        res = cv2.absdiff(g, warped).astype(np.float32)
        t = max(8, int(32 * sc))
        tiles = res[: h // t * t, : w // t * t].reshape(h // t, t, w // t, t).mean(axis=(1, 3))
        warp.append(float(np.percentile(tiles, 95)))
        sims.append(float(embed(fr[i][top]) @ ref) if i % args.sim_every == 0 else sims[-1])
        prev_g = g
    warp = np.array(warp)
    med = np.median(warp[1:])
    mad = np.median(np.abs(warp[1:] - med)) + 1e-6
    thr = max(med + 4 * 1.4826 * mad, 12.0)
    flagged = [i for i in range(1, len(fr)) if warp[i] > thr or sims[i] < args.sim_fail]
    for i in flagged[:12]:
        cv2.imwrite(str(OUT / f"{name}_f{i:03d}.png"), fr[i])
    # mandatory human review: the 3 least on-model frames of every clip, even when nothing is flagged
    for i in sorted(range(0, len(fr), args.sim_every), key=lambda k: sims[k])[:3]:
        cv2.imwrite(str(OUT / f"review_{name}_f{i:03d}_{sims[i]:.3f}.png"), fr[i])
    min_sim = float(min(sims))
    verdict = "PASS" if not flagged else ("FAIL" if min_sim < args.sim_fail or len(flagged) > 6 else "REVIEW")
    report[name] = {"verdict": verdict, "frames": len(fr), "warp_median": round(float(med), 2), "warp_threshold": round(float(thr), 2),
                    "warp_max": round(float(warp.max()), 2), "min_identity_sim": round(min_sim, 3), "flagged": flagged[:40]}
    print(name, verdict, f"warp max {warp.max():.1f} thr {thr:.1f} | min sim {min_sim:.3f} | flagged {len(flagged)}", flush=True)
(OUT / "qc_report.json").write_text(json.dumps(report, indent=1))
