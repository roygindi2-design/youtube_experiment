"""Edit for a Tito Short (one shot per lyric line), 1080x1920, hard cuts only, clean picture + .es.srt.

    python production/pilots/make_short_edit.py <spec.json> <clips_dir> <song_scores.json> <out.mp4>
        [--plan "1:A1 2:A2 5a:A5 5b:A3@19 ... tail:A8@7:2.5"] [--seed A1=19 ...] [--extra A3='{"until":2.1}']

--plan maps lyric lines to shots (default: line i -> shot i). "5a"/"5b" split line 5 at its middle sung word,
so a long chorus line gets two short shots instead of a long freeze. "@19" picks the seed. "tail:SHOT@seed:dur"
adds a closing shot after the last line.

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
SKIP = 0.06  # frame 0 of a generated clip is the raw keyframe (brighter): skipping it avoids a 1-frame flash at the cut


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
    plan = args[args.index("--plan") + 1].split() if "--plan" in args else [f"{i + 1}:{sid}" for i, sid in enumerate(shots_ids)]

    # align lyric words to the sung (Whisper) words
    want = [(li, w) for li, l in enumerate(lyric_lines) for w in l.split()]
    heard = take["words"]
    sm = difflib.SequenceMatcher(None, [norm(w) for _, w in want], [norm(w[0]) for w in heard], autojunk=False)
    t_of = {}
    for b in sm.get_matching_blocks():
        for k in range(b.size):
            t_of[b.a + k] = (heard[b.b + k][1], heard[b.b + k][2])
    starts, ends, words_t = [], [], []
    for li in range(len(lyric_lines)):
        idx = [i for i, (l, _) in enumerate(want) if l == li]
        ts = [t_of[i] for i in idx if i in t_of]
        if not ts:
            sys.exit(f"line {li + 1} not found in the sung take: {lyric_lines[li]}")
        starts.append(min(t[0] for t in ts))
        ends.append(max(t[1] for t in ts))
        words_t.append(sorted(t[0] for t in ts))
    lead = round(max(0.0, starts[0] - 0.15), 3)  # cut the silent song intro: the hook must land in second 0
    starts = [t - lead for t in starts]
    ends = [t - lead for t in ends]
    words_t = [[t - lead for t in w] for w in words_t]

    # segments: (start, end, shot, seed)
    segs, tail = [], None
    for tok in plan:
        key, shot = tok.split(":", 1)
        if key == "tail":
            sh, dur = shot.rsplit(":", 1)
            tail = (sh, float(dur))
            continue
        li = int(key.rstrip("ab")) - 1
        a = starts[li] - 0.12 if li else 0.0
        b = (starts[li + 1] - 0.12) if li + 1 < len(lyric_lines) else ends[li] + TAIL
        if key[-1] in "ab":
            mid = (starts[li] + ends[li]) / 2
            split = min(words_t[li], key=lambda t: abs(t - mid)) - 0.12
            a, b = (a, split) if key[-1] == "a" else (split, b)
        segs.append([max(0.0, a), b, shot])
    segs.sort(key=lambda x: x[0])
    for k in range(len(segs) - 1):  # contiguous: each shot runs until the next cut
        segs[k][1] = segs[k + 1][0]
    if tail:
        sh, dur = tail
        segs.append([segs[-1][1], segs[-1][1] + dur, sh])
    cuts = [round(sg[0], 3) for sg in segs] + [round(segs[-1][1], 3)]

    shots = []
    for i, (a, b, tok) in enumerate(segs):
        sid, seed = (tok.split("@") + [None])[:2]
        seed = int(seed) if seed else seeds.get(sid, 7)
        dur = round(b - a, 3)
        x = extras.get(f"{sid}@{seed}", extras.get(sid, {}))
        start = x.get("in", SKIP)
        usable = x.get("until", CLIP) - start
        speed = 1.0 if usable >= dur else max(0.8, round(usable / dur, 3))
        s = {"file": f"{clips}/{spec['id']}_clip_{sid}_s{seed}.mp4", "in": start, "dur": dur,
             "speed": speed, "src_len": round(min(usable, dur * speed), 3), "shot": f"{sid}@{seed}"}
        if usable / speed < dur:
            s["hold"] = round(dur - usable / speed + 0.1, 3)
        if i == 0:
            s["punch"] = {"to": 1.25, "dur": 0.45, "cx": 0.5, "cy": 0.32, "settle": 1.15, "shake": 10}
        s.update({k: v for k, v in x.items() if k in ("punch", "frame")})
        shots.append(s)
    lines = []
    for li, l in enumerate(lyric_lines):
        nxt = starts[li + 1] - 0.05 if li + 1 < len(lyric_lines) else cuts[-1]
        end = min(ends[li] + 0.6, nxt)
        lines.append({"start": round(max(0, starts[li] - 0.1), 3), "end": round(end, 3), "words": [[w, starts[li], end] for w in l.split()]})
    edit = {"out": out, "fps": 30, "size": [1080, 1920], "burn_captions": False,
            "song": {"file": take["file"], "start": lead, "gain_db": 0}, "shots": shots, "sfx": [], "lines": lines}
    p = Path(out).with_suffix(".edit.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(edit, ensure_ascii=False, indent=1))
    print(p, "total", cuts[-1], "s")
    for x in shots:
        print(f'  {x["shot"]:8s} dur {x["dur"]:5.2f} speed {x["speed"]} hold {x.get("hold", 0)}')


if __name__ == "__main__":
    main()
