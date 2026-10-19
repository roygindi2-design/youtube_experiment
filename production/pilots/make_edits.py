"""Write edit.json for both pilots (consumed by production/assemble.py).

Times below are in the ORIGINAL song (ACE-Step output); the song is sped up by TEMPO (atempo),
so every time is divided by TEMPO. Word times come from Whisper on the chosen song take; caption
text uses the intended lyrics (Whisper mis-heard a few sung words, e.g. "cajito" for "carrito").
"""
import json
import sys
from pathlib import Path

TEMPO = 1.06
CLIP_LEN = 97 / 24  # generated clip length (s)
CLIPS = Path(sys.argv[1])  # folder with clip_<shot>.mp4
SFX = Path(sys.argv[2])    # CC0 sound library folder
ROOT = Path(__file__).resolve().parent


def s(t):
    return round(t / TEMPO, 3)


def lines(spec):
    out = []
    for words, end in spec:
        ws = [[w, s(t)] for w, t in words]
        rows = []
        for i, (w, t) in enumerate(ws):
            nxt = ws[i + 1][1] if i + 1 < len(ws) else s(end)
            rows.append([w, t, round(min(nxt, t + 0.9), 3)])
        out.append({"start": round(ws[0][1] - 0.15, 3), "end": s(end), "words": rows})
    return out


def shots(bounds, extras=None):
    extras = extras or {}
    out = []
    for sid, a, b in bounds:
        dur = round(s(b) - s(a), 3)
        x = extras.get(sid, {})
        start = x.get("in", 0.0)
        speed = round(min(1.0, (CLIP_LEN - start) / dur), 3)
        out.append({"file": str(CLIPS / f"clip_{sid}.mp4"), "in": start, "dur": dur, "speed": speed, "shot": sid,
                    **{k: v for k, v in x.items() if k != "in"}})
    return out


POPO = {
    "shots": shots([("P1", 0, 2.9), ("P2", 2.9, 5.9), ("P2b", 5.9, 8.9), ("P3", 8.9, 13.3), ("P4", 13.3, 16.9),
                    ("P5", 16.9, 21.0), ("P6", 21.0, 25.8), ("P7", 25.8, 29.5), ("P8", 29.5, 34.6)]),
    "lines": lines([
        ([("¡Aaah!", 0.05)], 2.2),
        ([("¿Listos?", 2.96), ("¡A", 4.16), ("cepillar!", 5.02)], 6.4),
        ([("Un", 8.94), ("poquito", 9.4), ("de", 9.78), ("pasta,", 10.48), ("¡mira", 11.5), ("qué", 11.88), ("color!", 12.18)], 13.1),
        ([("Muevo", 13.32), ("el", 13.92), ("cepillo", 14.3), ("con", 15.12), ("mucho", 15.76), ("amor.", 16.38)], 16.9),
        ([("Arriba", 16.96), ("y", 17.86), ("abajo,", 18.38), ("¡cepi,", 19.08), ("cepi,", 20.12), ("cepi!", 20.56)], 21.05),
        ([("Adelante", 21.08), ("y", 21.6), ("atrás,", 22.4), ("¡dientes", 23.2), ("con", 24.0), ("brillo!", 24.54)], 25.6),
        ([("Enjuago,", 25.84), ("¡ya", 27.4), ("terminé!", 28.46)], 29.4),
        ([("¡Sonrisa", 29.58), ("brillante!", 32.1)], 34.2),
    ]),
    "sfx": [("bubble", 0.0, -9), ("pop", 3.6, -10), ("pluck", 9.6, -12), ("sparkle", 24.5, -10), ("sparkle", 30.2, -9),
            ("pop", 33.0, -8)],
    "colors": {"text": "#FFFFFF", "active": "#FFD23F", "outline": "#5B3B9C"},
}

TITO = {
    "shots": shots([("T1", 0, 3.6), ("T2", 3.6, 8.3), ("T3", 8.3, 12.7), ("T4", 12.7, 16.1), ("T5", 16.1, 20.4),
                    ("T5b", 20.4, 24.1), ("T6", 24.1, 28.3), ("T7", 28.3, 31.3), ("T8", 31.3, 34.1)],
                   {  # polish v2: thumb-stop hook + keep moving mouths out of focus while the song sings
                       "T1": {"punch": {"to": 1.32, "dur": 0.45, "cx": 0.5, "cy": 0.30, "settle": 1.20, "shake": 12}},
                       "T6": {"frame": {"zoom": 1.10, "cx": 0.5, "cy": 0.62}},   # favour the duck + eyes, trunk covers mouth
                       "T7": {"in": 1.4, "frame": {"zoom": 1.10, "cx": 0.72, "cy": 0.55}},  # skip the open-mouth start, favour the box
                   }),
    "lines": lines([
        ([("¡Uy!", 0.05)], 1.8),
        ([("¡Qué", 2.58), ("desorden!", 3.48), ("¡A", 4.16), ("ordenar!", 5.26)], 6.6),
        ([("La", 8.38), ("pelota", 8.96), ("roja,", 9.58), ("a", 10.5), ("la", 11.04), ("caja", 11.22), ("roja.", 11.64)], 12.6),
        ([("El", 12.74), ("carrito", 13.06), ("azul,", 13.56), ("a", 14.1), ("la", 14.54), ("caja", 14.66), ("azul.", 15.64)], 16.1),
        ([("Cada", 16.2), ("juguete", 17.0), ("a", 17.6), ("su", 17.8), ("casita,", 17.96), ("¡uno,", 18.86), ("dos,", 19.36), ("tres!", 19.68)], 20.4),
        ([("Cada", 20.46), ("juguete", 21.0), ("a", 21.58), ("su", 21.8), ("casita,", 22.0), ("¡qué", 22.8), ("bonito", 22.98), ("es!", 23.42)], 24.1),
        ([("El", 24.22), ("patito", 24.62), ("amarillo…", 25.42), ("¿aquí?", 26.42), ("¡No!", 27.1)], 28.6),
        ([("¡A", 29.44), ("la", 30.14), ("caja", 30.56), ("amarilla!", 31.34)], 33.6),
    ]),
    "sfx": [("whoosh-quick", 0.0, -8), ("thud", 0.15, -10), ("thud", 0.55, -12), ("thud", 0.9, -13), ("ding", 11.7, -12), ("ding", 15.7, -12),
            ("ding", 18.9, -14), ("ding", 19.4, -14), ("ding", 19.7, -14), ("question", 26.3, -10), ("success-soft", 31.5, -10)],
    "colors": {"text": "#FFFFFF", "active": "#FFD23F", "outline": "#1F4E8C"},
    "pill": {"color": "#0E1F3D", "opacity": 0.72, "pad": 18},
}

for name, e in (("popo", POPO), ("tito", TITO)):
    total = sum(x["dur"] for x in e["shots"])
    edit = {
        "out": str(ROOT / "build" / f"pilot_{name}.mp4"), "fps": 30,
        "song": {"file": str(ROOT / "build" / f"song_{name}.wav"), "start": 0.0, "gain_db": 0},
        "shots": e["shots"],
        "sfx": [{"file": str(SFX / f"{n}.wav"), "at": s(t), "gain_db": g} for n, t, g in e["sfx"] if s(t) < total],
        "lines": e["lines"], "font": "Fredoka", "font_file": str(ROOT.parent / "fonts" / "Fredoka.ttf"),
        "font_size": 84, "outline": 8, "colors": e["colors"], "caption_y": 0.70,
        **({"pill": e["pill"]} if e.get("pill") else {}),
    }
    (ROOT / f"edit_{name}.json").write_text(json.dumps(edit, ensure_ascii=False, indent=1))
    print(name, "total", round(total, 2), "s; speeds", [x["speed"] for x in e["shots"]])
