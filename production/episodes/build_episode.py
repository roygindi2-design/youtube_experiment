"""Build RunPod task lists for a story episode in two stages (design first, then shots).

    python production/episodes/build_episode.py <episode_dir> design   # -> <dir>/job_design.json
    python production/episodes/build_episode.py <episode_dir> shots    # -> <dir>/job_shots.json (needs <dir>/picks.json)

spec.json fields: id, lyrics, bpm, style, lock (Tito), mama_lock, locations{name: prompt}, shots[[id, frame, motion, loc, chars, seeds]].
design: Mamá candidates (Klein 4B with Tito's master as style reference), 2 seeds per location image, 6 song takes.
picks.json (written after visual review): {"mama": "<file>.jpg", "locations": {"patio": "<file>.jpg", ...}}; the picked files
are uploaded as inputs. Keyframes use refs [location, tito_master, (mama)] and describe each location explicitly
(no "room" word for outdoor places, no negations: QC_RULES.md prompt lessons). Clips: image_start = keyframe, N seeds.
"""
import json
import sys
from pathlib import Path

d = Path(sys.argv[1])
stage = sys.argv[2]
s = json.loads((d / "spec.json").read_text())
sid, STYLE = s["id"], s["style"]
SONG = ("preschool children's song, cheerful warm female lead vocal singing in Latin American Spanish with Mexican pronunciation, "
        "simple sing-along melody, ukulele, xylophone, glockenspiel, soft hand claps, light kick drum, {bpm} bpm, bright, happy, "
        "very clear lyrics, every word sung clearly, starts singing right away")
ACT = ("Smooth natural motion with a clear purposeful action; every character keeps the same face, body and clothes; "
       "exactly the characters described and no extra characters; objects keep their shape; no camera zoom, no morphing.")

tasks = []
if stage == "design":
    for k in (() if s.get("reuse_mama") else (1, 2, 3, 4)):  # reuse_mama: production/characters/mama_master.jpg
        tasks.append({"id": f"{sid}_mama_s{k}", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4,
                      "seed": 300 + k, "video_prompt_type": "KI",
                      "prompt": STYLE + "Character design sheet, full body, front three-quarter view, standing on a plain soft pastel "
                                "background: the mother of the baby elephant in the reference image, drawn in exactly the same 3D style. "
                                + s["mama_lock"] + " Only one character, friendly and warm.",
                      "inputs": {"image_refs": ["tito_master.jpg"]}})
    for name, prompt in s["locations"].items():
        for k in (1, 2):
            tasks.append({"id": f"{sid}_loc_{name}_s{k}", "model_type": "flux2_klein_4b", "resolution": "720x1280",
                          "num_inference_steps": 4, "seed": 400 + k, "prompt": STYLE + prompt})
    for k in range(1, 1 + s.get("song_takes", 6)):
        tasks.append({"id": f"{sid}_song_s{k}", "model_type": "ace_step_v1_5_turbo_lm_1_7b", "prompt": s["lyrics"],
                      "alt_prompt": SONG.format(bpm=s["bpm"]), "duration_seconds": 26, "seed": k, "num_inference_steps": 8,
                      "custom_settings": {"bpm": s["bpm"], "language": "es", "keyscale": "C major", "timesignature": 4}})
elif stage == "shots":
    picks = json.loads((d / "picks.json").read_text())
    for shot, frame, motion, loc, chars, seeds in s["shots"]:
        refs = [picks["locations"][loc], "tito_master.jpg"] + ([picks["mama"]] if "mama" in chars else [])
        who = ("The baby elephant from the second reference image, exactly the same character design: " + s["lock"])
        if "mama" in chars:
            who += (" Mamá Elefanta from the third reference image, exactly the same character design: " + s["mama_lock"]
                    + " Exactly two elephants in the picture: the small baby and his taller mother.")
        else:
            who += " Only one elephant in the picture."
        place = s["locations"][loc].split(". Nobody")[0]
        tasks.append({"id": f"{sid}_{shot}_kf", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4,
                      "seed": 101, "video_prompt_type": "KI",
                      "prompt": STYLE + who + f" Setting, exactly the place from the first reference image: {place}. " + frame + " Vertical 9:16 frame.",
                      "inputs": {"image_refs": refs}})
        for seed in (7, 19, 31)[:seeds]:
            tasks.append({"id": f"{sid}_clip_{shot}_s{seed}", "model_type": "ti2v_2_2_fastwan", "prompt": STYLE + motion + " " + ACT,
                          "resolution": "544x960", "video_length": 97, "num_inference_steps": 3, "guidance_scale": 1, "flow_shift": 3,
                          "seed": seed, "after": {"image_start": f"{sid}_{shot}_kf"}})
out = d / f"job_{stage}.json"
out.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
print(out, len(tasks), "tasks")
