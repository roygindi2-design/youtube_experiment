"""Objective accent check for Spanish TTS / sung samples.

    python production/accent_check.py <audio files...>  > report.json

For each file:
  - Whisper (faster-whisper small, language=es) transcript: is it intelligible?
  - Phoneme recognizer (facebook/wav2vec2-xlsr-53-espeak-cv-ft, IPA output) counts of
    θ ("th", Spain) versus s, and ʎ versus ʝ/j (yeísmo). Latin American Spanish should have ~0 θ.
The phoneme model is multilingual and imperfect: treat single θ hits as noise, a pattern as signal.
"""
import json
import sys

import librosa
import torch
from faster_whisper import WhisperModel
from transformers import AutoModelForCTC, AutoProcessor

PM = "facebook/wav2vec2-xlsr-53-espeak-cv-ft"
proc = AutoProcessor.from_pretrained(PM)
model = AutoModelForCTC.from_pretrained(PM).eval()
whisper = WhisperModel("small", device="cpu", compute_type="int8")


def phonemes(path):
    y, _ = librosa.load(path, sr=16000, mono=True)
    out = []
    for i in range(0, len(y), 16000 * 20):
        chunk = y[i:i + 16000 * 20]
        if len(chunk) < 1600:
            continue
        with torch.no_grad():
            logits = model(proc(chunk, sampling_rate=16000, return_tensors="pt").input_values).logits
        out.append(proc.batch_decode(torch.argmax(logits, dim=-1))[0])
    return " ".join(out)


res = []
for f in sys.argv[1:]:
    segs, _ = whisper.transcribe(librosa.load(f, sr=16000, mono=True)[0], language="es", beam_size=5)
    text = " ".join(s.text.strip() for s in segs)
    ph = phonemes(f)
    toks = ph.split()
    res.append({
        "file": f.split("/")[-1], "transcript": text, "phonemes": ph,
        "theta": sum(t.count("θ") for t in toks), "s": sum(t.count("s") for t in toks),
        "lambda_ll": sum(t.count("ʎ") for t in toks), "yeismo_j": sum(t.count("ʝ") + t.count("j") for t in toks),
    })
    print(json.dumps(res[-1], ensure_ascii=False), file=sys.stderr, flush=True)
print(json.dumps(res, ensure_ascii=False, indent=1))
