"""Generic WanGP task runner for a free Kaggle T4 kernel.

The local build script (production/kaggle/build_job.py) replaces __TASKS_JSON__ with a list of tasks
and pushes this file as a private Kaggle script kernel. Each task is a WanGP settings dict plus:
  id          output file name (no extension)
  inputs      optional {setting_name: "<attached dataset file name>"}; resolved from /kaggle/input
  after       optional id of an earlier task whose first output is passed as a setting
              ({"after": {"image_start": "popo_master_s1"}})
Special task kinds (field "kind"): "kokoro" runs Kokoro TTS (pip) instead of WanGP.

Outputs land in /kaggle/working/out/<id>.<ext> and manifest.json records status, timing and errors.
Every task is isolated: one failure never stops the others.
"""
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

WORK = Path("/kaggle/working")
TEMP = Path("/kaggle/temp")
REPO = TEMP / "Wan2GP"
OUT = WORK / "out"
RAW = TEMP / "raw"
MANIFEST = WORK / "manifest.json"
INPUT = Path("/kaggle/input")
T0 = time.time()

TASKS = json.loads(r'''__TASKS_JSON__''')


def load():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"stages": [], "tasks": []}


M = load()


def save():
    WORK.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(M, indent=1, ensure_ascii=False))


def stage(name, **info):
    M["stages"].append({"stage": name, "t": round(time.time() - T0), **info})
    save()
    print(f"[stage] {name} {info}", flush=True)


def sh(cmd):
    print("$", cmd if isinstance(cmd, str) else " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, shell=isinstance(cmd, str), check=True)


def find_input(name):
    hits = list(INPUT.rglob(name)) if INPUT.exists() else []
    if not hits:
        raise FileNotFoundError(f"input {name} not found under {INPUT}")
    return str(hits[0])


def install():
    gpu = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                         capture_output=True, text=True)
    if gpu.returncode != 0 or not gpu.stdout.strip():
        raise RuntimeError("no GPU")
    stage("gpu", gpus=gpu.stdout.strip().splitlines())
    for d in (OUT, RAW, TEMP / "data" / "ckpts", TEMP / "data" / "loras", TEMP / "cache"):
        d.mkdir(parents=True, exist_ok=True)
    if not REPO.exists():
        sh(["git", "clone", "--depth", "1", "https://github.com/deepbeepmeep/Wan2GP.git", str(REPO)])
    for name in ("ckpts", "loras"):
        link = REPO / name
        if link.is_dir() and not link.is_symlink():
            shutil.rmtree(link)
        if not link.exists():
            link.symlink_to(TEMP / "data" / name, target_is_directory=True)
    sh("apt-get install -y -qq ffmpeg libsndfile1 libportaudio2 espeak-ng libglib2.0-0 libgl1 > /dev/null 2>&1 || true")
    import torch
    import torchvision
    pins = [f"torch=={torch.__version__.split('+')[0]}", f"torchvision=={torchvision.__version__.split('+')[0]}"]
    try:
        import torchaudio
        pins.append(f"torchaudio=={torchaudio.__version__.split('+')[0]}")
    except Exception:
        pass
    (TEMP / "constraints.txt").write_text("\n".join(pins) + "\n")
    sh([sys.executable, "-m", "pip", "install", "-q", "--no-cache-dir", "-r", str(REPO / "requirements.txt"),
        "-c", str(TEMP / "constraints.txt")])
    tk = REPO / "preprocessing" / "matanyone" / "tools" / "interact_tools.py"
    if tk.exists():
        tk.write_text(tk.read_text().replace("TkAgg", "Agg"))
    stage("installed", torch=torch.__version__)


def outputs_of(task_id):
    return sorted(str(p) for p in OUT.glob(f"{task_id}.*")) + sorted(str(p) for p in OUT.glob(f"{task_id}__*"))


def record(task, fn):
    rec = {"id": task["id"], "settings": {k: v for k, v in task.items() if k != "id"}, "status": "running"}
    M["tasks"].append(rec)
    save()
    t = time.time()
    try:
        files = fn()
        kept = []
        for i, src in enumerate(files):
            suffix = Path(src).suffix.lower()
            dest = OUT / (f"{task['id']}{suffix}" if i == 0 else f"{task['id']}__{i}{suffix}")
            shutil.copy2(src, dest)
            kept.append(f"out/{dest.name}")
        rec.update(status="ok", files=kept)
    except Exception:
        rec.update(status="failed", error=traceback.format_exc()[-2500:])
    rec["seconds"] = round(time.time() - t, 1)
    save()
    print(f"[task] {task['id']} {rec['status']} {rec['seconds']}s", flush=True)


def stage_wangp():
    sys.path.insert(0, str(REPO))
    os.chdir(REPO)
    from shared.api import init

    session = init(root=REPO, output_dir=RAW, cli_args=["--profile", "4", "--attention", "sdpa"])
    stage("wangp_session")
    for task in TASKS:
        if task.get("kind", "wangp") != "wangp":
            continue
        settings = {k: v for k, v in task.items() if k not in ("id", "kind", "inputs", "after")}
        try:
            for key, name in (task.get("inputs") or {}).items():
                if isinstance(name, list):
                    settings[key] = [find_input(n) for n in name]
                else:
                    settings[key] = find_input(name)
            for key, ref in (task.get("after") or {}).items():
                refs = ref if isinstance(ref, list) else [ref]
                paths = []
                for r in refs:
                    got = outputs_of(r)
                    if not got:
                        raise RuntimeError(f"dependency {r} produced no output")
                    paths.append(got[0])
                settings[key] = paths if isinstance(ref, list) else paths[0]
            for key in [k for k in settings if k.endswith("_extra")]:  # append to a list setting
                base = key[: -len("_extra")]
                extra = settings.pop(key)
                settings[base] = list(settings.get(base) or []) + (extra if isinstance(extra, list) else [extra])
        except Exception:
            M["tasks"].append({"id": task["id"], "status": "skipped", "error": traceback.format_exc()[-1500:]})
            save()
            continue

        def run(settings=settings):
            result = session.submit_task(settings).result()
            files = [str(f) for f in (getattr(result, "generated_files", None) or [])]
            if not getattr(result, "success", False) or not files:
                raise RuntimeError(json.dumps(getattr(result, "errors", None), default=str)[:2000])
            return files

        record(task, run)
    stage("wangp_done")


def stage_kokoro():
    tasks = [t for t in TASKS if t.get("kind") == "kokoro"]
    if not tasks:
        return
    sh([sys.executable, "-m", "pip", "install", "-q", "--no-deps", "kokoro", "misaki", "soundfile", "loguru", "espeakng-loader", "num2words", "addict"])
    import types
    sys.modules.setdefault("spacy", types.ModuleType("spacy"))
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline
    from misaki import espeak

    pipe = KPipeline(lang_code="e")
    default_g2p = pipe.g2p
    for task in tasks:
        def run(task=task):
            pipe.g2p = espeak.EspeakG2P(language=task.get("espeak", "es")) if task.get("espeak") else default_g2p
            chunks, phon = [], []
            for result in pipe(task["text"], voice=task.get("voice", "ef_dora"), speed=task.get("speed", 1.0)):
                chunks.append(result.audio.cpu().numpy() if hasattr(result.audio, "cpu") else result.audio)
                phon.append(result.phonemes)
            path = RAW / f"{task['id']}.wav"
            sf.write(path, np.concatenate(chunks), 24000)
            (RAW / f"{task['id']}.txt").write_text("\n".join(phon))
            return [str(path), str(RAW / f"{task['id']}.txt")]

        record(task, run)
    stage("kokoro_done")


if __name__ == "__main__":
    me = globals().get("__file__")
    env = dict(os.environ, HF_HOME=str(TEMP / "cache" / "hf"), XDG_CACHE_HOME=str(TEMP / "cache"), MPLBACKEND="Agg")
    if len(sys.argv) > 1 and sys.argv[1] in ("--wangp", "--kokoro"):
        try:
            stage_wangp() if sys.argv[1] == "--wangp" else stage_kokoro()
        except Exception:
            stage("failed", where=sys.argv[1], error=traceback.format_exc()[-3000:])
            sys.exit(1)
        sys.exit(0)
    try:
        install()
    except Exception:
        stage("failed", where="install", error=traceback.format_exc()[-3000:])
        sys.exit(1)
    for flag in ("--kokoro", "--wangp"):
        if me and Path(me).exists():
            subprocess.run([sys.executable, me, flag], env=env)
        else:
            os.environ.update(env)
            try:
                stage_wangp() if flag == "--wangp" else stage_kokoro()
            except Exception:
                stage("failed", where=flag, error=traceback.format_exc()[-3000:])
    M = load()
    stage("finished", ok=sum(1 for t in M["tasks"] if t.get("status") == "ok"), total=len(M["tasks"]))
