"""Build and push a Kaggle kernel from runner_template.py + a tasks JSON file.

    python production/kaggle/build_job.py <job-name> <tasks.json> [--dataset roygindi/<slug>]

Auth: KAGGLE_API_TOKEN (or KAGGLE_USERNAME/KAGGLE_KEY) from the environment. Never written to disk.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    name, tasks_file = sys.argv[1], Path(sys.argv[2])
    dataset = sys.argv[sys.argv.index("--dataset") + 1] if "--dataset" in sys.argv else None
    tasks = json.loads(tasks_file.read_text())
    body = (HERE / "runner_template.py").read_text().replace("__TASKS_JSON__", json.dumps(tasks, ensure_ascii=False))
    out = HERE / "build" / name
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.py").write_text(body)
    meta = {
        "id": f"roygindi/{name}", "title": name, "code_file": f"{name}.py", "language": "python",
        "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
        "dataset_sources": [dataset] if dataset else [], "kernel_sources": [], "competition_sources": [],
        "machine_shape": "NvidiaTeslaT4",
    }
    (out / "kernel-metadata.json").write_text(json.dumps(meta, indent=1))
    subprocess.run(["kaggle", "kernels", "push", "-p", str(out), "--accelerator", "NvidiaTeslaT4", "--timeout", "10800"], check=True)


if __name__ == "__main__":
    main()
