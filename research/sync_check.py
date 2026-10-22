"""Music ↔ picture sync check for a final edit.
usage: python3 research/sync_check.py <video.mp4> [bpm]
Reports: cuts on the beat (±100 ms), movement peaks on the beat, and the worst off-beat cuts.
Goal (EPISODE_TEMPLATE §ז): ≥80% of cuts on a beat, ≥50% of movement peaks within ±120 ms of a beat.
"""
import sys, subprocess, tempfile, os, numpy as np, cv2, librosa
v = sys.argv[1]; bpm = float(sys.argv[2]) if len(sys.argv) > 2 else None
wav = os.path.join(tempfile.mkdtemp(), "a.wav")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", v, "-ac", "1", "-ar", "22050", wav], check=True)
y, sr = librosa.load(wav, sr=22050)
# fixed grid: our songs are generated at an exact bpm → find the bpm/phase that best fits the onsets
oe = librosa.onset.onset_strength(y=y, sr=sr); tt = librosa.times_like(oe, sr=sr); best = None
for b in (np.arange(bpm - 1, bpm + 1.01, 0.05) if bpm else np.arange(90, 130, 0.1)):
    per = 60 / b
    for ph in np.arange(0, per, 0.01):
        idx = np.searchsorted(tt, np.arange(ph, tt[-1], per)); idx = idx[idx < len(oe)]
        sc = oe[idx].mean()
        if best is None or sc > best[0]: best = (sc, b, ph)
_, tempo, phase = best; beats = np.arange(phase, tt[-1], 60 / tempo)
print(f"beat grid: {tempo:.2f} bpm, first beat {phase:.2f} s (use these to snap cuts)")
cap = cv2.VideoCapture(v); fps = cap.get(cv2.CAP_PROP_FPS); prev = None; d = []
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (96, 54)).astype(np.float32)
    d.append(0.0 if prev is None else float(np.mean(np.abs(g - prev)))); prev = g
d = np.array(d); t = np.arange(len(d)) / fps
ci = [i for i in range(1, len(d)) if d[i] > 18 and d[i-1] <= 18]
cuts = t[ci]
near = lambda x, tol: np.min(np.abs(beats - x)) <= tol if len(beats) else False
cut_ok = [near(c, 0.10) for c in cuts]
# movement peaks: local maxima of smoothed motion (excluding cuts) that stand out
m = d.copy(); m[d > 18] = 0
ms = np.convolve(m, np.ones(3) / 3, "same")
peaks = [i for i in range(2, len(ms) - 2) if ms[i] == max(ms[i-2:i+3]) and ms[i] > np.percentile(ms, 75)]
pk_ok = [near(t[i], 0.12) for i in peaks]
print(f"tempo≈{float(np.atleast_1d(tempo)[0]):.1f} bpm, beats {len(beats)}")
print(f"cuts on beat: {sum(cut_ok)}/{len(cuts)} = {100*np.mean(cut_ok) if cut_ok else 0:.0f}%  (goal ≥80%)")
print(f"movement peaks on beat: {sum(pk_ok)}/{len(peaks)} = {100*np.mean(pk_ok) if pk_ok else 0:.0f}%  (goal ≥50%; random ≈ {100*min(1,0.24*len(beats)/max(t[-1],1)):.0f}%)")
off = sorted([(float(np.min(np.abs(beats - c))), round(float(c), 2)) for c in cuts], reverse=True)[:8]
print("worst off-beat cuts (offset s, at s):", [(round(a, 2), b) for a, b in off])
