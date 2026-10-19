"""Long-form episode, stage L2: one video clip per shot from ONE chosen keyframe (image_start only).

    python production/longform/build_l2.py <keyframes_dir> <dataset_dir>

- Copies the chosen keyframe of every shot into the Kaggle dataset folder as lf_kf_<shot>.jpg.
- Writes production/jobs/jobL2a_tito_ep1.json (shots 1-12) and jobL2b (13-24): 2 seeds per shot,
  calm-motion suffix, no camera moves (QC_RULES.md). Two kernels so each stays under the 3 h limit.
Keyframe picks come from a visual review of both candidates per shot (2026-10-19):
two-elephant frames (L11_s101, both L21) are rejected; L21 reuses the clean dance frame L20_s202.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP = json.loads((ROOT / "production/longform/tito_ep1.json").read_text())
PICKS = {"L01": "L01_s101", "L02": "L02_s202", "L03": "L03_s101", "L04": "L04_s101", "L05": "L05_s101",
         "L06": "L06_s202", "L07": "L07_s101", "L08": "L08_s101", "L09": "L09_s202", "L10": "L10_s202",
         "L11": "L11_s202", "L12": "L12_s202", "L13": "L13_s101", "L14": "L14_s101", "L15": "L15_s202",
         "L16": "L16_s101", "L17": "L17_s202", "L18": "L18_s101", "L19": "L19_s101", "L20": "L20_s101",
         "L21": "L20_s202", "L22": "L22_s101", "L23": "L23_s101", "L24": "L24_s101"}
CALM = ("Small, calm, smooth movements; the character's head stays steady and stays the same single character; "
        "only one elephant; no fast motion, no camera zoom, no morphing.")
SEEDS = (7, 19)


def motion(text):
    text = re.sub(r"(Slow push-in|Slow pull-out|Camera [^.]*|Static camera)\.?", "", text).strip()
    return f"{text} Static camera. {CALM}"


def main():
    kdir, ddir = Path(sys.argv[1]), Path(sys.argv[2])
    tasks = []
    for s in EP["shots"]:
        sid = s["id"]
        shutil.copy(kdir / f"lf_{PICKS[sid]}.jpg", ddir / f"lf_kf_{sid}.jpg")
        for seed in SEEDS:
            tasks.append({"id": f"lf_clip_{sid}_s{seed}", "model_type": "ti2v_2_2_fastwan",
                          "prompt": EP["style"] + motion(s["motion"]), "negative_prompt": EP["vneg"],
                          "resolution": "960x544", "video_length": 97, "num_inference_steps": 3,
                          "guidance_scale": 1, "flow_shift": 3, "seed": seed,
                          "inputs": {"image_start": f"lf_kf_{sid}.jpg"}})
    half = len(tasks) // 2
    for name, part in (("jobL2a_tito_ep1.json", tasks[:half]), ("jobL2b_tito_ep1.json", tasks[half:])):
        (ROOT / "production/jobs" / name).write_text(json.dumps(part, ensure_ascii=False, indent=1))
        print(name, len(part))


if __name__ == "__main__":
    main()
