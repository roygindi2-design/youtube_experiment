"""Edit for a Tito Short (one shot per lyric line), 1080x1920, hard cuts only, clean picture + .es.srt.

    python production/pilots/make_short_edit.py <spec.json> <clips_dir> <song_scores.json> <out.mp4> [--seed A1=19 ...] [--extra A3='{"until":2.1}']

- spec.json: production/pilots/tito_s2_calcetines.json / tito_s3_torre.json (8 shots, 8 lyric lines).
- song_scores.json: output of production/pick_song.py; the first (best) take is used, with its Whisper word times.
- Lyric line i is sung over shot i; every cut sits just before the line's first sung word.
- Clips: <clips_dir>/<spec id>_clip_<shot>_s<seed>.mp4 (seed 7 by default; pick the clean seed after QC with --seed).
- Shot 1 gets the thumb-stop hook (fast push-in at second 0). Slots longer than a clip play at >= 0.8x and
  freeze the last clean frame (no blending, ever).
"""
import difflib
import json
import re
import sys
from pathlib import Path

CLIP = 97 / 24
TAIL = 1.6  # seconds after the last sung word


def norm(w):
    return re.sub(r"[^a-záéíóúñü]", "", w.lower())


def main():
    spec_f, clips, scores_f, out = sys.argv[1:5]
    args = sys.argv[5:]
    seeds = {}
    extras = {}
    for i, a in enumerate(args):
        if a == "--seed":
            k, v = args[i + 1].split("=")
            seeds[k] = int(v)
        if a == "--extra":
            k, v = args[i + 1].split("=", 1)
            extras[k] = json.loads(v)
    spec = json.loads(Path(spec_f).read_text())
    take = json.loads(Path(scores_f).read_text())[0]
    lyric_lines = [l for l in spec["lyrics"].splitlines() if l.strip() and not l.startswith("[")]
    shots_ids = [s[0] if isinstance(s, list) else s["id"] for s in spec["shots"]]
    assert len(lyric_lines) == len(shots_ids), "one lyric line per shot"

    # align lyric words to the sung (Whisper) words
    want = [(li, w) for li, l in enumerate(lyric_lines) for w in l.split()]
    heard = take["words"]
    sm = difflib.SequenceMatcher(None, [norm(w) for _, w in want], [norm(w[0]) for w in heard], autojunk=False)
    t_of = {}
    for b in sm.get_matching_blocks():
        for k in range(b.size):
            t_of[b.a + k] = (heard[b.b + k][1], heard[b.b + k][2])
    starts, ends = [], []
    for li in range(len(lyric_lines)):
        idx = [i for i, (l, _) in enumerate(want) if l == li]
        ts = [t_of[i] for i in idx if i in t_of]
        if not ts:
            sys.exit(f"line {li + 1} not found in the sung take: {lyric_lines[li]}")
        starts.append(min(t[0] for t in ts))
        ends.append(max(t[1] for t in ts))
    cuts = [0.0] + [round(max(0.0, t - 0.12), 3) for t in starts[1:]] + [round(ends[-1] + TAIL, 3)]

    shots = []
    for i, sid in enumerate(shots_ids):
        dur = round(cuts[i + 1] - cuts[i], 3)
        x = extras.get(sid, {})
        start = x.get("in", 0.0)
        usable = x.get("until", CLIP) - start
        speed = 1.0 if usable >= dur else max(0.8, round(usable / dur, 3))
        s = {"file": f"{clips}/{spec['id']}_clip_{sid}_s{seeds.get(sid, 7)}.mp4", "in": start, "dur": dur,
             "speed": speed, "src_len": round(min(usable, dur * speed), 3)}
        if usable / speed < dur:
            s["hold"] = round(dur - usable / speed + 0.1, 3)
        if i == 0:
            s["punch"] = {"to": 1.25, "dur": 0.45, "cx": 0.5, "cy": 0.32, "settle": 1.15, "shake": 10}
        s.update({k: v for k, v in x.items() if k in ("punch", "frame")})
        shots.append(s)
    lines = []
    for li, l in enumerate(lyric_lines):
        end = min(ends[li] + 0.6, cuts[li + 1] + (TAIL if li == len(lyric_lines) - 1 else 0))
        lines.append({"start": round(max(0, starts[li] - 0.1), 3), "end": round(end, 3), "words": [[w, starts[li], end] for w in l.split()]})
    edit = {"out": out, "fps": 30, "size": [1080, 1920], "burn_captions": False,
            "song": {"file": take["file"], "start": 0.0, "gain_db": 0}, "shots": shots, "sfx": [], "lines": lines}
    p = Path(out).with_suffix(".edit.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(edit, ensure_ascii=False, indent=1))
    print(p, "total", cuts[-1], "s; durs", [x["dur"] for x in shots], "speeds", [x["speed"] for x in shots])


if __name__ == "__main__":
    main()
