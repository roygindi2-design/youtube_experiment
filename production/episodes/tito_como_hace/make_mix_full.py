"""TikTok-cut mix of "¿Cómo hace?" (researcher 24.10): song take b1 + ONE inserted bar (4 beats of Demucs no_vocals, the
4 beats right before) after each BABY question, the REAL baby sound on beat 2 of that bar; the REAL mamá sound on the
beat after "¡A ver!" with the music ducked -8 dB for 0.9 s. Insert points = the quietest VOCAL beat between the end of the
question and the sung answer (beat-tracked accompaniment, ~112 bpm), so the bar phase is kept.
Sounds: CC0 FSD50K (production/sfx/animals/LICENSES.md): duck 416893 (#8; baby = +6 st), cat 110010 (#19, kitten) /
418153 (#18, mamá), mouse 397651 (#24, baby, +3 st) / 143125 (#23, mamá). Elephant toots = synthesized here (ours).
    python make_mix_full.py <htdemucs dir with vocals.wav + no_vocals.wav> <fsd dir with <id>.wav> <beats.npy> <out.wav> <map.json>
"""
import json
import sys
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

SR = 44100
D = Path(__file__).parent
sep, fsd, beats_f, out_wav, out_map = sys.argv[1:6]
song, _ = librosa.load(D / "song_b1.wav", sr=SR, mono=True)
acc, _ = librosa.load(Path(sep) / "no_vocals.wav", sr=SR, mono=True)
voc, _ = librosa.load(Path(sep) / "vocals.wav", sr=SR, mono=True)
beats = np.load(beats_f)
BEAT = float(np.median(np.diff(beats)))


def clip(id_, a, b, st=0.0, peak=0.7):
    y, _ = librosa.load(Path(fsd) / f"{id_}.wav", sr=SR, mono=True)
    y = y[int(a * SR):int(b * SR)]
    if st:
        y = librosa.effects.pitch_shift(y, sr=SR, n_steps=st)
    n = int(0.01 * SR)
    y[:n] *= np.linspace(0, 1, n)
    y[-n:] *= np.linspace(1, 0, n)
    return y / (np.abs(y).max() + 1e-9) * peak


def toot(notes, base, peak=0.6):
    out = []
    for dur in notes:
        t = np.arange(int(dur * SR)) / SR
        f = base * (1 + 0.012 * np.sin(2 * np.pi * 6 * t))  # a little vibrato
        ph = 2 * np.pi * np.cumsum(f) / SR
        w = sum(np.sin(k * ph) / k for k in range(1, 7))  # brassy saw-ish
        env = np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.06)
        out += [w * env, np.zeros(int(0.06 * SR))]
    y = np.concatenate(out)
    return y / np.abs(y).max() * peak


# (name, question end, sung answer start, "¡A ver!" end, baby sound, mamá sound) in SONG time (b1 Whisper map)
PAIRS = [
    ("patito", 6.6, 8.5, 15.6, clip("416893", 0.68, 1.40, 6)[: int(0.5 * SR)], clip("416893", 0.68, 1.40)),
    ("gatito", 23.7, 25.3, 32.7, clip("110010", 0.12, 0.80, 2), clip("418153", 16.50, 17.35)),
    ("ratoncito", 40.9, 42.6, 49.9, clip("397651", 0.30, 0.95, 3), clip("143125", 7.33, 7.60, 0, 0.6)),
    ("elefantito", 57.9, 58.5, 67.0, toot([0.16, 0.16, 0.26], 520), toot([0.9], 260, 0.75)),
]
env = librosa.feature.rms(y=voc, frame_length=2048, hop_length=512)[0]
et = librosa.frames_to_time(np.arange(len(env)), sr=SR, hop_length=512)


def quiet_beat(a, b):
    cand = [x for x in beats if a - 0.15 <= x <= b + 0.05] or [min(beats, key=lambda x: abs(x - (a + b) / 2))]
    return float(min(cand, key=lambda x: env[np.searchsorted(et, x)]))


xf = int(0.015 * SR)


def join(a, b):
    r = np.linspace(0, 1, xf)
    return np.concatenate([a[:-xf], a[-xf:] * (1 - r) + b[:xf] * r, b[xf:]])


pieces, events, shift, last = [], [], 0.0, 0.0
for name, qe, ans, aver, baby, mama in PAIRS:
    ins = quiet_beat(qe, ans)
    pieces += [song[int(last * SR):int(ins * SR)], acc[int((ins - 4 * BEAT) * SR):int(ins * SR)]]
    events.append({"pair": name, "insert_song_t": round(ins, 3), "insert_out_t": round(ins + shift, 3),
                   "baby_sound_out_t": round(ins + shift + BEAT, 3), "baby": baby})
    shift += 4 * BEAT
    mt = float(min([x for x in beats if x >= aver] or [aver]))
    events[-1].update({"mama_sound_song_t": round(mt, 3), "mama_sound_out_t": round(mt + shift, 3), "mama": mama})
    last = ins
pieces.append(song[int(last * SR):])
mix = pieces[0]
for p in pieces[1:]:
    mix = join(mix, p)
g = np.ones(len(mix))
for e in events:
    a, b = int((e["mama_sound_out_t"] - 0.1) * SR), int((e["mama_sound_out_t"] + 0.8) * SR)
    r = int(0.08 * SR)
    g[a:b] = np.minimum(g[a:b], 10 ** (-8 / 20))
    g[a - r:a] = np.minimum(g[a - r:a], np.linspace(1, 10 ** (-8 / 20), r))
    g[b:b + r] = np.minimum(g[b:b + r], np.linspace(10 ** (-8 / 20), 1, r))
mix *= g
for e in events:
    for k, t in (("baby", "baby_sound_out_t"), ("mama", "mama_sound_out_t")):
        s = int(e[t] * SR)
        mix[s:s + len(e[k])] += e[k][: len(mix) - s]
mix /= max(1.0, np.abs(mix).max() / 0.98)
sf.write(out_wav, mix, SR)
for e in events:
    e.pop("baby"), e.pop("mama")
json.dump({"bpm": round(60 / BEAT, 2), "beat": round(BEAT, 4), "duration": round(len(mix) / SR, 2), "pairs": events},
          open(out_map, "w"), indent=1)
print(json.dumps(json.load(open(out_map)), indent=1))
