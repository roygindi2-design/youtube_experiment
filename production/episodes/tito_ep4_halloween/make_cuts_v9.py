"""Cut list for tito_ep4_halloween v9 (Roy 23.10 fixes).

Base = the delivered v8c cut list (cuts.json). Unchanged slots are cut straight from the v8c master
(production/deliver/tito_ep4_halloween.mp4, "MASTER", graded=True so assemble does not grade twice).
Changed slots use the new v9 clips (shots_v9/, picks in shots_v9_review.md). Every split point is on the
110 bpm beat grid (first beat 0.14 s); each piece is one forward pass, >= 0.85x; each take max 2x.
BKT: until the new BKT keyframe/clip exists, its 2 slots stay MASTER (researcher fallback 23.10).

    python production/episodes/tito_ep4_halloween/make_cuts_v9.py && python production/edit_cuts.py <cuts_v9.json>
"""
import json
import os
from pathlib import Path

D = Path(__file__).parent
ROOT = D.parents[2]
B = 60 / 110
v8 = json.loads((D / "cuts.json").read_text())["cuts"]
BKT_NEW = os.environ.get("BKT", "BKTv9c@97:0.05:4.0,BKTv9c@97:0.05:4.0")  # e.g. "BKTv9b@7:0.05:4.0,BKTv9b@19:0.05:4.0" once the new clip exists


def piece(tok, i, u):
    return (tok, {"in": i, "until": u})


# v8c slot start -> list of (token, opts, beats) ; beats=None for the last piece (fills the rest of the slot)
REPL = {
    27.958: [("C2v9@31", 0.05, 3.323, 6), ("C2v9@7", 0.05, 1.686, None)],      # chorus 1 "¡gracias!"
    45.413: [("D2v9@31", 0.05, 2.232, None)],                                   # knock on the bat's door
    62.867: [("C2v9@19", 1.5, 4.0, 5), ("C2v9@31", 0.05, 2.232, None)],         # chorus 2
    88.504: [("M2v9@7", 0.05, 1.91, 4), ("M3v10@43", 0.05, 1.0, 2), ("M3ih@43", 0.6, 3.0, None)],  # v10: palm out, then the hand-to-bucket insert (Roy: no pour)        # sees the empty bucket -> pours on ¡Toma!
    91.231: [],                                                                 # (M3 slot absorbed above)
    93.958: [("M4v9@31", 0.05, 3.868, None)],                                   # the mouse jumps for joy
    102.14: [("C2v9@7", 0.05, 2.0, 4), ("C2v9@19", 1.5, 4.0, None)],           # chorus 3
    128.322: [("O2v9@7", 0.05, 3.323, 6), ("O2v9@31", 0.05, 2.232, None)],      # walk away together
    133.776: [("M4v9@19", 1.4, 3.9, 5), ("M4v9@31", 2.0, 3.9, None)],         # outro stays "together" (researcher QC 23.10)
    143.595: [("O2v9@31", 0.6, 3.9, None)],
    147.413: [("O2v9@7", 1.7, 4.0, None)],
}
if BKT_NEW:
    # BKTv9c s97: the trunk dips into the bucket ~0.5-2.2 s -> start | candy-bowl cutaway | end (researcher QC 23.10)
    REPL[21.413] = [("BKTv9c@97", 0.05, 0.6, 1), ("BOWLv9@31", 0.05, 1.7, 3), ("BKTv9c@97", 2.3, 2.9, None)]
    REPL[54.685] = [("BKTv9c@97", 0.05, 0.6, 1), ("BOWLv9@7", 0.05, 3.4, 6), ("BKTv9c@97", 2.35, 2.85, None)]  # tail ends at 2.85: arms open after it (glued bucket)

starts = [c[0] for c in v8]
cuts = []
for k, (a, b, tok, o) in enumerate(v8):
    key = next((s for s in REPL if abs(s - a) < 1e-3), None)
    if key is None:
        cuts.append([a, b, "MASTER@0", {"in": a, "until": b, "graded": True}])
        continue
    plan = REPL[key]
    if not plan:
        continue
    # the M2+M3 pair spans two v8 slots
    end = v8[k + 1][1] if key == 88.504 else b
    t = a
    for n, (tk, i, u, beats) in enumerate(plan):
        e = end if beats is None or n == len(plan) - 1 else round(t + beats * B, 3)
        cuts.append([round(t, 3), e, tk, {"in": i, "until": u}])
        t = e
src = D / "build" / "v9src"
src.mkdir(parents=True, exist_ok=True)
pre = "tito_ep4_halloween_clip_"
links = {f"{pre}MASTER_s0.mp4": D / "assets" / "v8c_master.mp4"}
for f in (D / "shots_v9").glob(f"{pre}*.mp4"):
    links[f.name] = f
for f in (D / "shots_r4").glob("m3i_h3_clip_s*.mp4"):
    links[f"{pre}M3ih_s{f.stem.rsplit('_s', 1)[1]}.mp4"] = f
for n, target in links.items():
    l = src / n
    if l.is_symlink() or l.exists():
        l.unlink()
    l.symlink_to(target.resolve())
uses = {}
for c in cuts:
    if c[2] != "MASTER@0":
        uses[c[2]] = uses.get(c[2], 0) + 1
uses = {k: (v + 1) // 2 if k == "BKTv9c@97" else v for k, v in uses.items()}  # start+end of one slot = one use
over = {k: v for k, v in uses.items() if v > 2}
if over:
    raise SystemExit(f"take used more than 2x: {over}")
out = {"out": str(D / "build" / "tito_ep4_halloween_v9.mp4"), "song": str(D / "assets" / "song.wav"), "size": [1920, 1080],
       "clips": str(src / pre), "cuts": cuts}
(D / "cuts_v9.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts; new-take uses:", uses)
