"""Cut-list editor: every shot starts on an exact word time of the song, so the lyric and the picture match (research/10).

    python production/edit_cuts.py <cuts.json>      -> writes <out>.edit.json for production/assemble.py

cuts.json: {"out": ".../x.mp4", "song": "assets/song.wav", "clips": "<dir>/<prefix>", "cuts": [[start, end, "C1@19", {opts}], ...]}
opts: "in" (seconds into the clip), "reverse": true (play the clip backwards = a 'boomerang' back to its first frame,
used instead of a freeze). Refuses any shot that would need a freeze frame or a slow-down below 0.85x (Roy 20.10).
"""
import json
import sys
from pathlib import Path

CLIP = 97 / 24


def main():
    c = json.loads(Path(sys.argv[1]).read_text())
    shots, bad = [], []
    for a, b, tok, *rest in c["cuts"]:
        o = rest[0] if rest else {}
        sid, seed = tok.split("@")
        dur = round(b - a, 3)
        start = o.get("in", 0.06)
        usable = o.get("until", CLIP) - start
        speed = 1.0 if usable >= dur else round(usable / dur, 3)
        if speed < 0.85:
            bad.append(f"{tok} {a}-{b}: needs {dur:.2f}s, clip has {usable:.2f}s -> split the slot")
        s = {"file": f"{c['clips']}{sid}_s{seed}.mp4", "in": start, "dur": dur, "speed": speed,
             "src_len": round(min(usable, dur * speed), 3), "shot": tok}
        if o.get("reverse"):
            s["reverse"] = True
        shots.append(s)
    if bad:
        sys.exit("refused (would freeze or crawl):\n  " + "\n  ".join(bad))
    for x, y in zip(c["cuts"], c["cuts"][1:]):
        if abs(x[1] - y[0]) > 1e-6:
            sys.exit(f"gap/overlap between {x[2]} and {y[2]}")
    edit = {"out": c["out"], "fps": 30, "size": [1080, 1920], "burn_captions": False,
            "song": {"file": c["song"], "start": c.get("song_start", 0.0), "gain_db": 0}, "shots": shots, "sfx": c.get("sfx", []), "lines": []}
    p = Path(c["out"]).with_suffix(".edit.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(edit, ensure_ascii=False, indent=1))
    print(p, "total", round(sum(s["dur"] for s in shots), 2), "s")
    for s in shots:
        print(f"  {s['shot']:9s} {s['dur']:5.2f}s x{s['speed']}{' REV' if s.get('reverse') else ''}")


if __name__ == "__main__":
    main()
