"""Pick the best generated song take: Whisper transcript vs. the intended lyrics.

    python production/pick_song.py <lyrics.json|txt> <song.wav> [<song.wav> ...] --out scores.json

Score = share of lyric words (in order) that Whisper heard (difflib matching blocks), so a take that
skips lines or mumbles scores low. Word timestamps are saved too: they drive the edit and the SRT.
"""
import argparse
import difflib
import json
import re
from pathlib import Path

import librosa
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("lyrics")
ap.add_argument("songs", nargs="+")
ap.add_argument("--out", required=True)
args = ap.parse_args()

src = Path(args.lyrics).read_text()
if args.lyrics.endswith(".json"):
    src = json.loads(src)["lyrics"]
lyric_lines = [l for l in src.splitlines() if l.strip() and not l.startswith("[")]


def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-záéíóúñü ]", " ", t)
    return t.split()


want = norm(" ".join(lyric_lines))
model = WhisperModel("small", device="cpu", compute_type="int8")
res = []
for f in args.songs:
    y = librosa.load(f, sr=16000, mono=True)[0]
    segs, _ = model.transcribe(y, language="es", beam_size=5, word_timestamps=True, initial_prompt=" ".join(lyric_lines[:4]))
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in (s.words or [])]
    heard = norm(" ".join(w[0] for w in words))
    sm = difflib.SequenceMatcher(None, want, heard, autojunk=False)
    score = sum(b.size for b in sm.get_matching_blocks()) / max(1, len(want))
    res.append({"file": f, "score": round(score, 3), "duration": round(len(y) / 16000, 1),
                "transcript": " ".join(w[0] for w in words), "words": words})
    print(Path(f).name, round(score, 3), round(len(y) / 16000, 1), "s", flush=True)
res.sort(key=lambda r: -r["score"])
Path(args.out).write_text(json.dumps(res, ensure_ascii=False, indent=1))
print("best:", res[0]["file"])
