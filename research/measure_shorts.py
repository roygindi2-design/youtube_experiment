#!/usr/bin/env python3
"""Measure toddler YouTube Shorts (local .mp4 files) - nothing is estimated.

Usage:
    python3 measure_shorts.py VIDEO_DIR OUT_JSON [--frames FRAMES_DIR] [--model small]

For every VIDEO_DIR/<youtube_id>.mp4 it measures:
  - duration, resolution, fps (ffprobe)
  - scene cuts (ffmpeg select='gt(scene,0.3)',showinfo): timestamps, cuts/10s, avg shot length, first cut
  - audio (librosa): tempo + beat confidence, half/double check vs onset rate,
    first strong onset, RMS curve (0.5s bins), silent lead-in, music/voice start
  - speech (faster-whisper, es, word timestamps, CPU int8): first word, words,
    distinct words, words/sec, most repeated line + count, timeline of lines
  - hook second = min(first strong onset, first word, first cut) + each component
  - loop: similarity of first vs last frame (mean abs diff + global SSIM on 64x114 gray)
  - 3 frames (0.5s, middle, end) saved as small JPGs for visual inspection
Media files must stay outside the repo (copyright).
"""
import argparse, json, re, subprocess, sys, collections
from pathlib import Path
import numpy as np


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)])
    j = json.loads(out.stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {"duration_s": round(float(j["format"]["duration"]), 2),
            "width": v["width"], "height": v["height"],
            "fps": round(float(num) / float(den), 2),
            "vertical": v["height"] > v["width"]}


def scene_cuts(path, duration, thr=0.3):
    r = run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"])
    cuts = [round(float(t), 2) for t in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    bounds = [0.0] + cuts + [duration]
    shots = np.diff(bounds)
    return {"threshold": thr, "cut_times_s": cuts, "n_cuts": len(cuts),
            "cuts_per_10s": round(len(cuts) / duration * 10, 2),
            "avg_shot_s": round(float(np.mean(shots)), 2),
            "median_shot_s": round(float(np.median(shots)), 2),
            "first_cut_s": cuts[0] if cuts else None}


def extract_wav(path, wav):
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", "16000", str(wav)])


def audio_features(wav):
    import librosa
    y, sr = librosa.load(str(wav), sr=22050, mono=True)
    dur = len(y) / sr
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units="time")
    onset_rate = len(onsets) / dur if dur else 0
    # beat confidence: mean onset strength on beats / mean overall
    conf = float(np.mean(onset_env[beats]) / (np.mean(onset_env) + 1e-9)) if len(beats) else 0.0
    # tempogram alternatives (half / double) - report autocorr strength of each
    ac = librosa.autocorrelate(onset_env, max_size=onset_env.size)
    hop_t = 512 / sr
    def ac_at(bpm):
        lag = int(round(60.0 / bpm / hop_t))
        return float(ac[lag] / ac[0]) if 0 < lag < len(ac) else None
    alt = {f"{b:.0f}": ac_at(b) for b in (tempo / 2, tempo, tempo * 2) if 40 <= b <= 260}
    # first strong onset: first onset whose strength >= 50% of the 95th percentile
    times = librosa.times_like(onset_env, sr=sr)
    strong_thr = 0.5 * np.percentile(onset_env, 95)
    strong = [t for t in onsets if onset_env[np.argmin(abs(times - t))] >= strong_thr]
    # RMS in 0.5 s bins, dB relative to max
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    rt = librosa.times_like(rms, sr=sr, hop_length=512)
    db = librosa.amplitude_to_db(rms, ref=np.max(rms) + 1e-12)
    bins = []
    for b in np.arange(0, dur, 0.5):
        m = (rt >= b) & (rt < b + 0.5)
        bins.append(round(float(np.mean(db[m])), 1) if m.any() else None)
    sound_idx = np.where(db > -30)[0]
    sound_start = float(rt[sound_idx[0]]) if len(sound_idx) else None
    return {"tempo_bpm": round(tempo, 1), "beat_confidence": round(conf, 2),
            "tempo_alternatives_autocorr": alt,
            "onset_rate_per_s": round(onset_rate, 2),
            "onsets_per_beat": round(onset_rate / (tempo / 60), 2) if tempo else None,
            "first_onset_s": round(float(onsets[0]), 2) if len(onsets) else None,
            "first_strong_onset_s": round(float(strong[0]), 2) if strong else None,
            "sound_start_s_(>-30dB)": round(sound_start, 2) if sound_start is not None else None,
            "silent_lead_in": bool(sound_start is not None and sound_start > 0.3),
            "rms_db_0.5s_bins": bins,
            "last_0.5s_rms_db": bins[-1] if bins else None}


_model = None
def transcribe(wav, model_name):
    global _model
    from faster_whisper import WhisperModel
    if _model is None:
        _model = WhisperModel(model_name, device="cpu", compute_type="int8")
    import librosa  # pass a float array: avoids PyAV version issues inside faster-whisper
    audio16, _ = librosa.load(str(wav), sr=16000, mono=True)
    segs, _ = _model.transcribe(audio16, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
    lines, words = [], []
    for s in segs:
        lines.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
        for w in (s.words or []):
            words.append({"t": round(w.start, 2), "w": w.word.strip()})
    norm = lambda t: re.sub(r"[^\wáéíóúñü ]", "", t.lower()).strip()
    toks = [norm(w["w"]) for w in words if norm(w["w"])]
    line_counts = collections.Counter(norm(l["text"]) for l in lines if norm(l["text"]))
    # repeated n-grams (3-6 words) as a chorus proxy
    best = (None, 0)
    for n in (6, 5, 4, 3):
        c = collections.Counter(tuple(toks[i:i + n]) for i in range(len(toks) - n + 1))
        if c:
            g, k = c.most_common(1)[0]
            if k >= 2 and k * n > best[1] * len((best[0] or "").split()):
                best = (" ".join(g), k)
    top_line = line_counts.most_common(1)[0] if line_counts else (None, 0)
    return {"first_word_s": words[0]["t"] if words else None,
            "last_word_s": words[-1]["t"] if words else None,
            "n_words": len(toks), "n_distinct_words": len(set(toks)),
            "top_words": collections.Counter(toks).most_common(5),
            "most_repeated_line": top_line[0], "most_repeated_line_count": top_line[1],
            "most_repeated_phrase": best[0], "most_repeated_phrase_count": best[1],
            "timeline": lines}


def gray_frame(path, t, w=64, h=114):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(max(t, 0)), "-i", str(path),
                        "-frames:v", "1", "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                       capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    return a[: w * h].reshape(h, w).astype(float) if a.size >= w * h else None


def ssim_global(a, b):
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ma, mb = a.mean(), b.mean()
    va, vb = a.var(), b.var()
    cov = ((a - ma) * (b - mb)).mean()
    return float(((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2)))


def loop_check(path, duration):
    f0, f1 = gray_frame(path, 0.0), gray_frame(path, duration - 0.1)
    if f0 is None or f1 is None:
        return {"error": "frame grab failed"}
    mad = float(np.mean(np.abs(f0 - f1)))
    s = ssim_global(f0, f1)
    return {"first_last_mean_abs_diff": round(mad, 1), "first_last_ssim": round(s, 3),
            "loops_visually": bool(s > 0.8 and mad < 20)}


def save_frames(path, duration, outdir, vid):
    outdir.mkdir(parents=True, exist_ok=True)
    res = []
    for tag, t in (("a_0.5s", 0.5), ("b_mid", duration / 2), ("c_end", duration - 0.2)):
        f = outdir / f"{vid}_{tag}.jpg"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", str(t), "-i", str(path),
             "-frames:v", "1", "-vf", "scale=-2:480", "-q:v", "4", str(f)])
        res.append(str(f))
    return res


def measure(path, frames_dir, model):
    vid = path.stem
    m = {"id": vid}
    m.update(probe(path))
    d = m["duration_s"]
    m["cuts"] = scene_cuts(path, d)
    wav = path.with_suffix(".wav")
    extract_wav(path, wav)
    m["audio"] = audio_features(wav)
    m["speech"] = transcribe(wav, model)
    comps = {"first_strong_onset_s": m["audio"]["first_strong_onset_s"],
             "first_word_s": m["speech"]["first_word_s"],
             "first_cut_s": m["cuts"]["first_cut_s"]}
    vals = [v for v in comps.values() if v is not None]
    m["hook"] = {"definition": "earliest of first strong audio onset, first word, first scene cut",
                 "hook_s": min(vals) if vals else None, **comps}
    sp = m["speech"]
    if sp["first_word_s"] is not None and sp["last_word_s"] is not None and sp["last_word_s"] > sp["first_word_s"]:
        sp["words_per_s_sung_span"] = round(sp["n_words"] / (sp["last_word_s"] - sp["first_word_s"]), 2)
    sp["words_per_s_total"] = round(sp["n_words"] / d, 2)
    m["loop"] = loop_check(path, d)
    if frames_dir:
        m["frames"] = save_frames(path, d, Path(frames_dir), vid)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_dir"); ap.add_argument("out_json")
    ap.add_argument("--frames"); ap.add_argument("--model", default="small")
    a = ap.parse_args()
    vids = sorted(Path(a.video_dir).glob("*.mp4"))
    if not vids:
        sys.exit("no .mp4 files found")
    res = []
    for p in vids:
        print("measuring", p.name, file=sys.stderr)
        res.append(measure(p, a.frames, a.model))
    Path(a.out_json).write_text(json.dumps({"videos": res}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
