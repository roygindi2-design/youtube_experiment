"""Edit for long-form episode 1 (Tito, "Cada juguete a su casita"), 1920x1080, hard cuts only.

    python production/longform/make_edit_ep1.py <clips_dir> <song.wav> <outro_narration.wav> <out.mp4> [--alt SHOT=seed ...]

Cuts sit on the lyric lines (word times from Whisper on the chosen take, lf_song_s3: 117 BPM, vocals end 121.5 s).
Choruses reuse the dance shots with the OTHER seed, so the same clip never plays twice.
Clips are 97 frames (4.04 s). Longer slots slow the clip to >= 0.8x and freeze the last clean frame for the rest.
Writes edit_ep1.json next to the output; assemble with production/assemble.py.
"""
import json
import sys
from pathlib import Path

CLIP = 97 / 24
SKIP = 0.06  # frame 0 is the raw keyframe (brighter): skip it, no flash at the cut
# (start, end, shot, seed) — seed "a" = 7, "b" = 19
CUTS = [  # (start, end, shot, seed[, {"in": s, "until": s}]) — picks after visual QC of all 48 clips (2026-10-19)
    (0.0, 4.4, "L01", "a"), (4.4, 8.7, "L03", "a"),                                  # Intro: ¡Uy! / ¡Vamos a ordenar!
    (8.7, 12.5, "L05", "b"), (12.5, 16.5, "L06", "b"),                               # V1 red (L05 s7: ball merges into trunk; L06 s7: face squish at 2.6 s)
    (16.5, 20.5, "L07", "a"), (20.5, 24.1, "L09", "a"), (24.1, 28.5, "L08", "a"), (28.5, 32.4, "L12", "a"),  # C1
    (32.4, 36.5, "L10", "a"), (36.5, 40.5, "L11", "a"),                              # V2 blue
    (40.5, 44.5, "L20", "a"), (44.5, 48.0, "L02", "b"), (48.0, 52.4, "L07", "b"), (52.4, 56.6, "L12", "b"),  # C2 (L09 s19: toys vanish)
    (56.6, 59.6, "L13", "a"), (59.6, 61.6, "L14", "b"),                              # V3 yellow gag (L14 s7: duck vanishes)
    (61.6, 64.5, "L15", "b", {"in": 1.2}),                                           # duck vanishes in the first second: start after
    (64.5, 66.4, "L16", "a", {"until": 1.4}), (66.4, 72.5, "L17", "a"),            # L16: overall straps vanish after 1.5 s
    (72.5, 74.4, "L18", "a", {"until": 1.9}), (74.4, 76.6, "L18", "b", {"in": 2.0}),  # V4 green: blocks vanish mid-clip -> match cut
    (76.6, 80.4, "L19", "a"),
    (80.4, 84.5, "L21", "a"), (84.5, 88.4, "L08", "b"), (88.4, 92.6, "L04", "a"), (92.6, 96.8, "L22", "a"),  # C3
    (96.8, 100.5, "L03", "b"), (100.5, 104.1, "L22", "b"),                           # Outro: Rojo, azul...
    (104.1, 108.4, "L20", "b"), (108.4, 112.1, "L21", "b"), (112.1, 116.4, "L17", "b"), (116.4, 121.5, "L23", "a"),  # C4
    (121.5, 127.2, "L23", "b"),                                                      # Narration: goodbye wave (L24 ball vanishes)
]
SEED = {"a": 7, "b": 19}
LINES = [  # (start, end, text) for the Spanish CC track
    (0.0, 1.6, "¡Uy!"), (1.8, 4.3, "¡Qué desorden!"), (5.4, 7.6, "¡Vamos a ordenar!"),
    (8.8, 12.0, "La pelota roja, ¿dónde va?"), (12.6, 15.4, "¡A la caja roja, ya está!"),
    (16.6, 24.0, "Cada juguete a su casita, ¡uno, dos, tres!"), (24.2, 30.6, "Cada juguete a su casita, ¡qué bonito es!"),
    (32.4, 36.0, "El carrito azul, ¿dónde va?"), (36.6, 39.4, "¡A la caja azul, ya está!"),
    (40.5, 47.6, "Cada juguete a su casita, ¡uno, dos, tres!"), (47.9, 54.6, "Cada juguete a su casita, ¡qué bonito es!"),
    (56.6, 61.2, "El patito amarillo… ¿aquí?"), (61.6, 63.6, "¡No, no, no!"),
    (64.5, 70.4, "¡A la caja amarilla, sí señor!"),
    (72.5, 76.2, "Los bloques verdes, ¿dónde van?"), (76.6, 79.4, "¡A la caja verde, ya están!"),
    (80.4, 88.0, "Cada juguete a su casita, ¡uno, dos, tres!"), (88.4, 94.6, "Cada juguete a su casita, ¡qué bonito es!"),
    (96.8, 99.4, "Rojo, azul, amarillo y verde,"), (99.6, 103.4, "¡todo en su lugar!"),
    (104.1, 111.8, "Cada juguete a su casita, ¡uno, dos, tres!"), (112.1, 118.6, "Cada juguete a su casita, ¡qué bonito es!"),
    (121.8, 123.8, "¡Muy bien! Todo en su lugar."), (124.0, 126.8, "¡Hasta la próxima, amiguitos!"),
]
NARR_AT = 121.8


def main():
    clips, song, narr, out = sys.argv[1:5]
    alt = dict(a.split("=") for a in sys.argv[sys.argv.index("--alt") + 1:]) if "--alt" in sys.argv else {}
    shots = []
    for cut in CUTS:
        start, end, sid, sd = cut[:4]
        x = cut[4] if len(cut) > 4 else {}
        seed = int(alt.get(f"{sid}{sd}", SEED[sd]))
        dur = round(end - start, 3)
        t0 = x.get("in", SKIP)
        usable = x.get("until", CLIP) - t0
        speed = 1.0 if dur <= usable else max(0.8, round(usable / dur, 3))
        s = {"file": f"{clips}/lf_clip_{sid}_s{seed}.mp4", "in": t0, "dur": dur, "speed": speed,
             "src_len": round(min(usable, dur * speed), 3), "shot": f"{sid}@{seed}"}
        if usable / speed < dur:
            s["hold"] = round(dur - usable / speed + 0.1, 3)
        shots.append(s)
    edit = {"out": out, "fps": 30, "size": [1920, 1080], "burn_captions": False,
            "song": {"file": song, "start": 0.0, "gain_db": -1},
            "shots": shots,
            "sfx": [{"file": narr, "at": NARR_AT, "gain_db": 2}],
            "lines": [{"start": a, "end": b, "words": [[w, a, b] for w in t.split()]} for a, b, t in LINES]}
    p = Path(out).with_name("edit_ep1.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(edit, ensure_ascii=False, indent=1))
    print(p, round(sum(s["dur"] for s in shots), 2), "s,", len(shots), "shots")


if __name__ == "__main__":
    main()
