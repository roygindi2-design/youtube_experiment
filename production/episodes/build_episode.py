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
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])
stage = sys.argv[2]
s = json.loads((d / "spec.json").read_text())
sid, STYLE = s["id"], s["style"]
LAND = s.get("orientation") == "landscape"  # long-form 16:9
KF_RES, CLIP_RES = ("1280x720", "960x544") if LAND else ("720x1280", "544x960")
FRAME = "Wide 16:9 frame." if LAND else "Vertical 9:16 frame."
SONG = ("preschool children's song, cheerful warm female lead vocal singing in Latin American Spanish with Mexican pronunciation, "
        "simple sing-along melody, ukulele, xylophone, glockenspiel, soft hand claps, light kick drum, {bpm} bpm, bright, happy, "
        "very clear lyrics, every word sung clearly, starts singing right away")
ACT = ("Smooth natural motion with a clear purposeful action; every character keeps the same face, body and clothes; "
       "exactly the characters described and no extra characters; objects keep their shape; no camera zoom, no morphing.")

tasks = []
if stage == "design":
    for k in (() if s.get("reuse_mama") or "mama_lock" not in s else (1, 2, 3, 4)):  # reuse_mama: production/characters/mama_master.jpg
        tasks.append({"id": f"{sid}_mama_s{k}", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4,
                      "seed": 300 + k, "video_prompt_type": "KI",
                      "prompt": STYLE + "Character design sheet, full body, front three-quarter view, standing on a plain soft pastel "
                                "background: the mother of the baby elephant in the reference image, drawn in exactly the same 3D style. "
                                + s["mama_lock"] + " Only one character, friendly and warm.",
                      "inputs": {"image_refs": ["tito_master.jpg"]}})
    hero = s.get("hero")
    for k in ((1, 2, 3, 4) if hero and hero.get("design") else ()):  # new series hero: design sheet candidates, no refs
        tasks.append({"id": f"{sid}_hero_s{k}", "model_type": "flux2_klein_4b", "resolution": "720x1280", "num_inference_steps": 4,
                      "seed": 500 + k, "prompt": STYLE + "Character design sheet, full body, front three-quarter view, on a plain soft "
                                                        "pastel background: " + s["lock"] + " Only one character, friendly and cute."})
    for name, prompt in s["locations"].items():
        for k in (1, 2):
            tasks.append({"id": f"{sid}_loc_{name}_s{k}", "model_type": "flux2_klein_4b", "resolution": KF_RES,
                          "num_inference_steps": 4, "seed": 400 + k, "prompt": STYLE + prompt})
    for k in range(1, 1 + s.get("song_takes", 6)):
        tasks.append({"id": f"{sid}_song_s{k}", "model_type": "ace_step_v1_5_turbo_lm_1_7b", "prompt": s["lyrics"],
                      "alt_prompt": SONG.format(bpm=s["bpm"]), "duration_seconds": s.get("song_seconds", 26), "seed": k, "num_inference_steps": 8,
                      "custom_settings": {"bpm": s["bpm"], "language": "es", "keyscale": "C major", "timesignature": 4}})
elif stage in ("shots", "kf"):
    stage_kf_only = stage == "kf"
    picks = json.loads((d / "picks.json").read_text())
    for shot, frame, motion, loc, chars, seeds in s["shots"]:
        hero = s.get("hero", {"master": "tito_master.jpg", "who": "The baby elephant", "one": "Only one elephant in the picture."})
        # director mode: the location image is a reference ONLY for wide establishing shots; other shots get their own
        # camera angle from the text, so the model does not copy the same composition into every frame (Roy 20.10)
        use_loc = (not s.get("director")) or frame.lower().startswith("wide")
        refs = ([picks["locations"][loc]] if use_loc else []) + [picks.get("hero", hero["master"])] + ([picks["mama"]] if "mama" in chars else [])
        nth = (lambda k: ["first", "second", "third"][k - 1 - (0 if use_loc else 1)])
        who = (hero["who"] + f" from the {nth(2)} reference image, exactly the same character design: " + s["lock"])
        if "mama" in chars:
            who += (f" Mamá Elefanta from the {nth(3)} reference image, exactly the same character design: " + s["mama_lock"]
                    + " Exactly two elephants in the picture: the small baby and his taller mother.")
        else:
            who += " " + hero["one"]
        place = s["locations"][loc].split(". Nobody")[0]
        setting = (f" Setting, exactly the place from the first reference image: {place}. " if use_loc else
                   " Setting: " + re.sub(r"vertical 9:16 composition, |wide 16:9 composition, |camera [^:]*: ", "", place) + ". ")
        for kseed in ((101, 202) if s.get("director") else (101,)):
            tasks.append({"id": f"{sid}_{shot}_kf" + ("" if kseed == 101 else f"{kseed}"), "model_type": "flux2_klein_4b", "resolution": KF_RES,
                          "num_inference_steps": 4, "seed": kseed, "video_prompt_type": "KI",
                          "prompt": STYLE + frame + " " + who + setting + FRAME, "inputs": {"image_refs": refs}})
        if stage_kf_only:
            continue
        for seed in (7, 19, 31)[:seeds]:
            tasks.append({"id": f"{sid}_clip_{shot}_s{seed}", "model_type": "ti2v_2_2_fastwan", "prompt": STYLE + motion + " " + ACT,
                          "resolution": CLIP_RES, "video_length": 97, "num_inference_steps": 3, "guidance_scale": 1, "flow_shift": 3,
                          "seed": seed, "after": {"image_start": f"{sid}_{shot}_kf"}})
out = d / f"job_{stage}.json"
out.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
print(out, len(tasks), "tasks")
