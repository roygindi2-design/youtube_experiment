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
        "id": "tito_s4_helado", "hook": "giant_object", "bpm": 120, "food": True, "room_seed": 9,
        "world": "outdoors on a sunny tropical beach with golden sand, turquoise sea and palm trees, wide open blue sky all around, open air",
        "title": "¡Un helado GIGANTE de colores! 🍦🐘 | Aprende los colores con Tito #Shorts",
        "room": "A sunny tropical beach, vertical 9:16 composition, camera at child eye level: soft golden sand, gentle turquoise "
                "sea and small waves in the background, two palm trees, a striped beach umbrella, clear blue sky with fluffy clouds. "
                "On the sand stands a GIANT ice cream cone, taller than a child, with three huge scoops stacked: a red strawberry "
                "scoop at the bottom, a yellow banana scoop in the middle and a brown chocolate scoop on top. The scoops are "
                "plain smooth ice cream, like real ice cream in a shop. Nobody is on the beach.",
        "lyrics": "[Intro]\n¡Uy! ¡Un helado gigante!\n[Verse]\nBola roja, ¡fresa!\nBola amarilla, ¡plátano!\nBola café, ¡chocolate!\n"
                  "[Chorus]\nHelado de colores, ¡mmm, qué rico!\n[Outro]\n¡Uno, dos, tres! ¡Mmm!",
        "shots": [
            ("H1", "Low angle medium shot: the baby elephant stands next to the giant ice cream cone on the beach that towers over him, he looks up at it with a huge surprised open-mouth smile, ears raised.",
             "The baby elephant looks up at the giant ice cream, his ears lift in surprise and his eyes sparkle. Static camera."),
            ("H2", "Medium close-up: the baby elephant points his trunk at the huge red strawberry scoop of the giant ice cream, happy face.",
             "The baby elephant points at the red scoop with his trunk and nods happily. Static camera."),
            ("H3", "Medium shot: the baby elephant stands beside the same giant three-scoop ice cream cone and looks up at its huge yellow banana middle scoop, delighted smile.",
             "The baby elephant looks at the yellow scoop and smiles, his ears flap gently. Static camera."),
            ("H4", "Medium shot: the baby elephant stands beside the giant three-scoop ice cream cone, which is taller than him, and stretches his trunk up toward the brown chocolate scoop on the very top, eyes wide.",
             "The baby elephant stretches his trunk up toward the brown scoop and giggles. Static camera."),
            ("H5", "Medium shot: the baby elephant hugs himself with joy on the beach in front of the giant ice cream, eyes closed, blissful 'mmm' smile.",
             "The baby elephant sways happily side to side with his eyes closed, smiling. Static camera."),
            ("H6", "Wide shot: the baby elephant dances on the sand next to the giant three-color ice cream cone, ears flapping, one foot raised.",
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
    {  # habit + food + giant object: the strongest combination in the 2026-10-20 market scan
        "id": "tito_s4_frutas", "hook": "giant_food_habit", "bpm": 118, "food": True,
        "world": "outdoors in a sunny green garden with grass, flowers, a white fence and a rainbow in the wide open blue sky, open air",
        "title": "¡A lavar las frutas gigantes! 🍎🍌🍐 | Aprende los colores con Tito #Shorts",
        "room": "A sunny green garden, vertical 9:16 composition, camera at child eye level: soft green grass, colorful flowers, "
                "a small apple tree and a little white fence, a soft rainbow in the blue sky. On the grass stands a big round shallow "
                "wooden tub full of clear water and soft white soap bubbles. Floating in the tub: a GIANT shiny red apple, a GIANT "
                "yellow banana and a GIANT green pear, each fruit as big as a toddler. Plain real fruit. Nobody is in the garden.",
        "lyrics": "[Intro]\n¡Splash! ¡Frutas gigantes!\n[Verse]\n¿Las lavamos? ¡Sí, sí, sí!\nManzana roja, ¡splash, splash!\n"
                  "Plátano amarillo, ¡splash, splash!\nPera verde, ¡splash, splash!\n[Outro]\n¡Limpias y ricas! ¡Mmm!",
        "shots": [
            ("F1", "Medium shot: the baby elephant stands next to the big tub of bubbly water with a GIANT red apple, a GIANT yellow banana and a GIANT green pear floating in it, he gasps with a huge surprised smile, ears raised.",
             "Soft bubbles float up from the tub, the giant fruits bob gently in the water, the baby elephant's ears lift in surprise. Static camera."),
            ("F2", "Medium shot: the baby elephant sprays water from his trunk onto the GIANT red apple floating in the bubbly tub, water drops sparkle.",
             "A gentle stream of water sprays from the baby elephant's trunk onto the red apple, droplets sparkle. Static camera."),
            ("F3", "Medium shot: the GIANT yellow banana floats in the bubbly water, the baby elephant laughs next to the tub, soap bubbles around.",
             "The banana bobs gently in the water, soap bubbles drift up, the baby elephant laughs. Static camera."),
            ("F4", "Medium shot: the GIANT green pear floats in the bubbly tub, the baby elephant sprays a little water on it from his trunk.",
             "A gentle stream of water from the trunk splashes the pear, bubbles drift up. Static camera."),
            ("F5", "Wide shot: the three GIANT clean shiny fruits, a red apple, a yellow banana and a green pear, stand in a row on the grass, sparkling, the baby elephant claps next to them.",
             "Little sparkles twinkle on the clean fruits, the baby elephant claps happily. Static camera."),
            ("F6", "Medium shot: the baby elephant hugs the GIANT shiny red apple with both arms, eyes closed, blissful 'mmm' smile.",
             "The baby elephant hugs the giant apple and sways gently with a happy smile. Static camera."),
            ("F7", "Medium shot: the baby elephant dances happily on the grass next to the tub of bubbly water, soap bubbles floating around him.",
             "The baby elephant dances gently side to side, bubbles float around. Static camera."),
        ],
    },
]


def tasks_for(s):
    sid = s["id"]
    out = [{"id": f"{sid}_room", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4, "seed": s.get("room_seed", 7),
            "prompt": STYLE + s["room"]}]
    for k in range(1, 6):
        out.append({"id": f"{sid}_song_s{k}", "model_type": "ace_step_v1_5_turbo_lm_1_7b", "prompt": s["lyrics"],
                    "alt_prompt": SONG_STYLE.format(bpm=s["bpm"]), "duration_seconds": 30, "seed": k, "num_inference_steps": 8,
                    "custom_settings": {"bpm": s["bpm"], "language": "es", "keyscale": "C major", "timesignature": 4}})
    for shot, frame, motion in s["shots"]:
        out.append({"id": f"{sid}_{shot}_kf", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4,
                    "seed": 101, "video_prompt_type": "KI",
                    "prompt": STYLE + "The baby elephant from the second reference image, exactly the same character design, same "
                              "colors and same features: " + LOCK + (f" Setting: {s['world']}, exactly the place from the first reference image. " if s.get("world") else " Setting: the room from the first reference image. ") + frame +
                              " Only one elephant in the picture." + (" The food is plain, smooth and realistic, like real food." if s.get("food") else "") + " Vertical 9:16 frame.",
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
        spec = {"id": s["id"], "hook": s["hook"], "world": s.get("world"), "story": s.get("story", []), "style": STYLE, "lock": LOCK, "title": s["title"], "room": s["room"],
                "lyrics": s["lyrics"], "shots": [list(x) for x in s["shots"]]}
        (d / f"{s['id']}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
    a = tasks_for(SHORTS[0]) + tasks_for(SHORTS[1])
    b = tasks_for(SHORTS[2])
    (ROOT / "production/jobs/jobS4_sprint_a.json").write_text(json.dumps(a, ensure_ascii=False, indent=1))
    (ROOT / "production/jobs/jobS4_sprint_b.json").write_text(json.dumps(b, ensure_ascii=False, indent=1))
    print("job a:", len(a), "tasks; job b:", len(b), "tasks")
    # round 2 (after keyframe review): helado re-render (keep its songs) + frutas (habit+food+giant)
    by = {x["id"]: x for x in SHORTS}
    r2 = [t for t in tasks_for(by["tito_s4_helado"]) if "_song_" not in t["id"]] + [t for t in tasks_for(by["tito_s4_frutas"]) if "_song_" not in t["id"]]
    (ROOT / "production/jobs/jobS5_helado_fix_frutas.json").write_text(json.dumps(r2, ensure_ascii=False, indent=1))
    print("round 2:", len(r2), "tasks")


if __name__ == "__main__":
    main()
