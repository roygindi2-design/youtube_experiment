"""Snap every cut of cuts_v3.json to the song's beat grid (111 bpm, first beat 0.41 s; research/sync_check.py).
Each slot keeps its take; 'until' is re-derived from the new slot length (max = the take's end), >= 0.85x enforced.
    python production/episodes/tito_ep2/snap_cuts.py && python production/edit_cuts.py production/episodes/tito_ep2/cuts_v3.json"""
import json
from pathlib import Path
P = Path(__file__).parent / "cuts_v3.json"
B0, B = 0.41, 60 / 111
END = 87.9
c = json.loads(P.read_text()); cuts = c["cuts"]
snap = lambda t: t if t in (0.0, END) else round(B0 + round((t - B0) / B) * B, 3)
bounds = [snap(x[0]) for x in cuts] + [END]
import math
bounds[-2] = round(B0 + math.ceil((cuts[-1][0] - B0) / B) * B, 3)  # the last take (E18N, 4.93 s) cannot cover the earlier beat
bad = []
for k, x in enumerate(cuts):
    a, b = bounds[k], bounds[k + 1]
    tmax = 4.99 if "shots_v3" in x[2] else 4.0
    o = x[3]; i = o.get("in", 0.06)
    need = b - a
    if (tmax - i) < 0.85 * need - 1e-6:
        bad.append(f"{x[2]} {a}-{b}: needs {need:.2f}s, has {tmax - i:.2f}s")
    x[0], x[1] = a, b; o["until"] = round(min(tmax, i + need), 3)
if bad:
    raise SystemExit("\n".join(bad))
P.write_text(json.dumps(c, indent=1)); print(len(cuts), "cuts snapped")
