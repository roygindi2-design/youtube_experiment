"""20 s mix test (researcher 24.10): intro + the duck pair of song take b1, with ONE inserted bar of accompaniment-only
(Demucs htdemucs no_vocals, the bar right before) after the baby question, the REAL baby quack on beat 2 of that bar,
and the REAL mamá quack in the gap after "¡A ver!" with the music ducked -8 dB.
Beat grid from librosa on the accompaniment: ~112.3 bpm, bars at 4.09, 6.22, 8.36, ... (song time).
CC0: FSD50K 416893 "Duck_Hyde_park" (Apheo), production/sfx/animals/LICENSES.md #8. Baby = the same quack pitched +6 st.
    python production/episodes/tito_como_hace/make_mix_test.py <no_vocals.wav> <416893.wav> <out.wav>
"""
import sys
import numpy as np
import librosa
import soundfile as sf

SR = 44100
D = __import__("pathlib").Path(__file__).parent
song, _ = librosa.load(D / "song_b1.wav", sr=SR, mono=True)
acc, _ = librosa.load(sys.argv[1], sr=SR, mono=True)
q, _ = librosa.load(sys.argv[2], sr=SR, mono=True)
BEAT = 60 / 112.3
BAR = 4 * BEAT
ins_at = 8.36                      # bar start, right before the sung answer "¡Cuac, cuac, cuac!"
mama_at = 15.86                    # the beat after "¡A ver!" (15.3), before the sung "¡Cuac, cuac!" (17.0)
end_song = 18.0                    # song time where the test stops (after "…mamá pata" starts)
xf = int(0.015 * SR)


def seg(y, a, b):
    return y[int(a * SR):int(b * SR)].copy()


def join(a, b):
    r = np.linspace(0, 1, xf)
    return np.concatenate([a[:-xf], a[-xf:] * (1 - r) + b[:xf] * r, b[xf:]])


quack = seg(q, 0.68, 1.40)
quack = quack / (np.abs(quack).max() + 1e-9) * 0.7
baby = librosa.effects.pitch_shift(quack, sr=SR, n_steps=6)[: int(0.5 * SR)]
part1 = seg(song, 0, ins_at)
pause = seg(acc, ins_at - BAR, ins_at)
part2 = seg(song, ins_at, end_song)
mix = join(join(part1, pause), part2)
# baby quack on beat 2 of the inserted bar
t_b = int((ins_at + BEAT) * SR)
mix[t_b:t_b + len(baby)] += baby * 0.9
# mamá quack in the gap, music ducked -8 dB around it
t_m = ins_at + BAR + (mama_at - ins_at)
a, b = int((t_m - 0.1) * SR), int((t_m + 1.1) * SR)
g = np.ones(len(mix))
g[a:b] = 10 ** (-8 / 20)
ramp = int(0.08 * SR)
g[a - ramp:a] = np.linspace(1, g[a], ramp)
g[b:b + ramp] = np.linspace(g[a], 1, ramp)
mix *= g
s = int(t_m * SR)
mix[s:s + len(quack)] += quack
fade = int(0.3 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)
mix /= max(1.0, np.abs(mix).max() / 0.98)
sf.write(sys.argv[3], mix, SR)
print("out", round(len(mix) / SR, 2), "s; baby quack at", round(ins_at + BEAT, 2), "mamá quack at", round(t_m, 2))
