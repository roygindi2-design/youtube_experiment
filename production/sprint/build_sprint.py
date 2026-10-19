"""Sprint 2026-10-20: three hook-test Shorts (one hook variable each), spec files + Kaggle jobs.

    python production/sprint/build_sprint.py

Writes production/sprint/<id>.json (spec for make_short_edit.py) and two Kaggle job files:
  production/jobs/jobS4_sprint_a.json  (helado + color)   production/jobs/jobS4_sprint_b.json  (cucu)
Rules from QC_RULES.md baked in: one image_start per clip, calm motion, 2 seeds, only one elephant,
objects never held in hands (vanishing objects were the #1 glitch), no camera moves.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = json.loads((ROOT / "production/pilots/tito_s3_torre.json").read_text())
STYLE, LOCK = BASE["style"], BASE["lock"]
CALM = ("Small, calm, smooth movements; the character's head stays steady and stays the same single character; "
        "only one elephant; every object stays in its place and keeps its shape; no fast motion, no camera zoom, no morphing.")
SONG_STYLE = ("preschool children's song, cheerful warm female lead vocal singing in Latin American Spanish with Mexican "
              "pronunciation, simple sing-along melody, ukulele, xylophone, glockenspiel, soft hand claps, light kick drum, "
              "{bpm} bpm, bright, happy, very clear lyrics, every word sung clearly")

SHORTS = [
    {  # hook: GIANT surprise object at second 0 (pattern of the current #1 breakout format)
        "id": "tito_s4_helado", "hook": "giant_object", "bpm": 120,
        "title": "¡Un helado GIGANTE de colores! 🍦🐘 | Aprende los colores con Tito #Shorts",
        "room": "Bright sunny kids playroom, vertical 9:16 composition, camera at child eye level, light wooden floor, round "
                "pastel-pink rug, big window with soft daylight. In the center of the room stands a GIANT ice cream cone, "
                "taller than a child, with three huge scoops stacked: a red strawberry scoop at the bottom, a yellow banana "
                "scoop in the middle and a brown chocolate scoop on top. No characters, no animals, no faces, no people.",
        "lyrics": "[Intro]\n¡Uy! ¡Un helado gigante!\n[Verse]\nBola roja, ¡fresa!\nBola amarilla, ¡plátano!\nBola café, ¡chocolate!\n"
                  "[Chorus]\nHelado de colores, ¡mmm, qué rico!\n[Outro]\n¡Uno, dos, tres! ¡Mmm!",
        "shots": [
            ("H1", "Low angle medium shot: the baby elephant stands next to the giant ice cream cone that towers over him, he looks up at it with a huge surprised open-mouth smile, ears raised.",
             "The baby elephant looks up at the giant ice cream, his ears lift in surprise and his eyes sparkle. Static camera."),
            ("H2", "Medium close-up: the baby elephant points his trunk at the huge red strawberry scoop of the giant ice cream, happy face.",
             "The baby elephant points at the red scoop with his trunk and nods happily. Static camera."),
            ("H3", "Medium close-up: the baby elephant looks up at the huge yellow banana scoop of the giant ice cream, delighted smile.",
             "The baby elephant looks at the yellow scoop and smiles, his ears flap gently. Static camera."),
            ("H4", "Medium close-up: the baby elephant reaches his trunk toward the huge brown chocolate scoop on top of the giant ice cream, eyes wide.",
             "The baby elephant stretches his trunk up toward the brown scoop and giggles. Static camera."),
            ("H5", "Medium shot: the baby elephant hugs himself with joy in front of the giant ice cream, eyes closed, blissful 'mmm' smile.",
             "The baby elephant sways happily side to side with his eyes closed, smiling. Static camera."),
            ("H6", "Wide shot: the baby elephant dances next to the giant three-color ice cream cone, ears flapping, one foot raised.",
             "The baby elephant dances gently side to side next to the giant ice cream. Static camera."),
            ("H7", "Medium close-up: the baby elephant has a small dab of pink strawberry ice cream on the tip of his trunk, he looks at it cross-eyed and laughs.",
             "The baby elephant looks at the ice cream on his trunk and laughs. Static camera."),
        ],
    },
    {  # hook: SOUND BURST at 0.0 s (Tito's trumpet) + one bright moving object; no eye-contact stare, no boxes/unboxing
        "id": "tito_s4_color", "hook": "sound_burst", "bpm": 116,
        "title": "¡Tuuu! Los colores con Tito 🐘🎈 | Rojo, azul y amarillo #Shorts",
        "room": "Bright cozy kids playroom, vertical 9:16 composition, camera at child eye level, light wooden floor, round "
                "pastel-pink rug, big window with soft daylight. On the rug lie a shiny red ball and a yellow rubber duck, and "
                "a blue balloon on a string floats above the rug. No characters, no animals, no faces, no people.",
        "lyrics": "[Intro]\n¡Tuuu! ¡Tuuu! ¡Colores!\n[Verse]\n¡Rojo, rojo, la pelota!\n¡Azul, azul, el globo!\n"
                  "¡Amarillo, amarillo, el patito!\n[Outro]\n¡Tuuu! ¡Muy bien!",
        "shots": [
            ("C1", "Medium shot: the baby elephant raises his trunk high and trumpets joyfully, ears spread wide, eyes closed with joy.",
             "The baby elephant trumpets with his trunk raised high, his ears flutter. Static camera."),
            ("C2", "Medium shot: a shiny red ball bounces on the pink rug next to the baby elephant, he watches it with delight.",
             "The red ball bounces gently up and down on the rug, the baby elephant follows it with his eyes. Static camera."),
            ("C3", "Medium shot: a blue balloon on a string floats above the baby elephant, he looks up at it with wonder.",
             "The blue balloon sways gently in the air, the baby elephant looks up and smiles. Static camera."),
            ("C4", "Medium shot: the baby elephant claps happily next to a yellow rubber duck sitting on the rug.",
             "The baby elephant claps his hands happily, the duck stays on the rug. Static camera."),
            ("C5", "Wide shot: the baby elephant dances on the rug next to the red ball, the yellow duck and the floating blue balloon.",
             "The baby elephant dances gently side to side, ears flapping. Static camera."),
            ("C6", "Medium shot: the baby elephant raises his trunk high and trumpets again, very happy, ears spread wide.",
             "The baby elephant trumpets with his trunk raised high. Static camera."),
        ],
    },
    {  # hook: peekaboo / search game ("¿Dónde está?") — the child finds Tito
        "id": "tito_s4_cucu", "hook": "peekaboo_search", "bpm": 112,
        "title": "¿Dónde está Tito? 🙈 ¡Cucú! | Canción de escondite para bebés #Shorts",
        "room": "Bright cozy kids bedroom, vertical 9:16 composition, camera at child eye level, light wooden floor, round "
                "pastel-pink rug, a long soft yellow curtain hanging by the window, a fluffy light-blue blanket on the rug, "
                "a small toy chest. No characters, no animals, no faces, no people.",
        "lyrics": "[Intro]\n¿Dónde está Tito? ¿Dónde está?\n[Verse]\n¿Detrás de la cortina? ¡Cucú! ¡Aquí está!\n"
                  "¿Debajo de la manta? ¡Cucú! ¡Aquí está!\n[Chorus]\n¡Cucú, cucú, te veo yo!\n[Outro]\n¡Cucú! ¡Adiós!",
        "shots": [
            ("P1", "Medium shot: the long yellow curtain by the window, a big round elephant ear and a small blue foot of the baby elephant peek out from behind it.",
             "The curtain sways very gently, the elephant ear wiggles behind it. Static camera."),
            ("P2", "Medium shot: the baby elephant peeks out from behind the yellow curtain with a huge happy smile, looking into the camera.",
             "The baby elephant leans out a little from behind the curtain and smiles at the camera. Static camera."),
            ("P3", "Medium shot: a fluffy light-blue blanket on the rug with a round elephant-shaped lump under it and a pink-and-blue ear sticking out.",
             "The blanket rises and falls gently as if breathing, the ear wiggles. Static camera."),
            ("P4", "Medium shot: the baby elephant sits on the rug with the light-blue blanket over his back like a cape, his face visible, laughing into the camera.",
             "The baby elephant laughs and wiggles his ears. Static camera."),
            ("P5", "Close-up: the baby elephant covers his eyes with both hands, playing peekaboo with the viewer.",
             "The baby elephant slowly lowers his hands from his eyes and smiles at the camera. Static camera."),
            ("P6", "Close-up: the baby elephant laughs with delight looking straight into the camera, ears up.",
             "The baby elephant giggles and his ears bounce gently. Static camera."),
            ("P7", "Medium shot: the baby elephant waves goodbye at the camera with one hand, big smile.",
             "The baby elephant waves goodbye with one hand. Static camera."),
        ],
    },
]


def tasks_for(s):
    sid = s["id"]
    out = [{"id": f"{sid}_room", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4, "seed": 7,
            "prompt": STYLE + s["room"]}]
    for k in range(1, 6):
        out.append({"id": f"{sid}_song_s{k}", "model_type": "ace_step_v1_5_turbo_lm_1_7b", "prompt": s["lyrics"],
                    "alt_prompt": SONG_STYLE.format(bpm=s["bpm"]), "duration_seconds": 30, "seed": k, "num_inference_steps": 8,
                    "custom_settings": {"bpm": s["bpm"], "language": "es", "keyscale": "C major", "timesignature": 4}})
    for shot, frame, motion in s["shots"]:
        out.append({"id": f"{sid}_{shot}_kf", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4,
                    "seed": 101, "video_prompt_type": "KI",
                    "prompt": STYLE + "The baby elephant from the second reference image, exactly the same character design, same "
                              "colors and same features: " + LOCK + " Setting: the room from the first reference image. " + frame +
                              " Only one elephant in the picture. Vertical 9:16 frame.",
                    "after": {"image_refs": [f"{sid}_room"]}, "inputs": {"image_refs_extra": "tito_master.jpg"}})
    for shot, frame, motion in s["shots"]:
        for seed in (7, 19):
            out.append({"id": f"{sid}_clip_{shot}_s{seed}", "model_type": "ti2v_2_2_fastwan", "prompt": STYLE + motion + " " + CALM,
                        "resolution": "544x960", "video_length": 97, "num_inference_steps": 3, "guidance_scale": 1,
                        "flow_shift": 3, "seed": seed, "after": {"image_start": f"{sid}_{shot}_kf"}})
    return out


def main():
    d = ROOT / "production/sprint"
    for s in SHORTS:
        spec = {"id": s["id"], "hook": s["hook"], "style": STYLE, "lock": LOCK, "title": s["title"], "room": s["room"],
                "lyrics": s["lyrics"], "shots": [list(x) for x in s["shots"]]}
        (d / f"{s['id']}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
    a = tasks_for(SHORTS[0]) + tasks_for(SHORTS[1])
    b = tasks_for(SHORTS[2])
    (ROOT / "production/jobs/jobS4_sprint_a.json").write_text(json.dumps(a, ensure_ascii=False, indent=1))
    (ROOT / "production/jobs/jobS4_sprint_b.json").write_text(json.dumps(b, ensure_ascii=False, indent=1))
    print("job a:", len(a), "tasks; job b:", len(b), "tasks")


if __name__ == "__main__":
    main()
