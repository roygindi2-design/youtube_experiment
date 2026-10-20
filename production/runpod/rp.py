"""RunPod control: run a WanGP task list (same format as the Kaggle jobs) on a rented GPU pod.

    python production/runpod/rp.py balance
    python production/runpod/rp.py up <name> [--gpu "NVIDIA GeForce RTX 4090"]   # create pod, wait for the agent
    python production/runpod/rp.py run <name> <tasks.json> [<input files> ...]    # upload runner + inputs, start the job
    python production/runpod/rp.py status <name>
    python production/runpod/rp.py fetch <name> <local_dir>                      # download work/out/* + manifest
    python production/runpod/rp.py down <name>                                    # TERMINATE the pod (stops billing)
    python production/runpod/rp.py list

Secrets: the RunPod API key comes from env runpod_key and is never written to disk or sent to the pod.
The pod only gets a random per-pod AGENT_TOKEN (stored in ~/.config/yt-kids/runpod_<name>.json, chmod 600).
Billing runs from `up` until `down`: always call down when the job is fetched.
"""
import base64
import json
import os
import secrets
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
KEY = os.environ.get("runpod_key") or os.environ.get("RUNPOD_API_KEY")
REST = "https://rest.runpod.io/v1"
STATE = Path(os.environ.get("YT_KIDS_HOME", Path.home() / ".config" / "yt-kids"))
IMAGE = "runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04"
CLOUDS = ("SECURE",)  # 2026-10-20: 6 community hosts in a row failed torch CUDA init ("CUDA unknown error"); secure worked
GPUS = ["NVIDIA GeForce RTX 4090", "NVIDIA RTX PRO 4500 Blackwell", "NVIDIA GeForce RTX 5090", "NVIDIA RTX A6000",
        "NVIDIA A40", "NVIDIA L40", "NVIDIA L40S", "NVIDIA RTX 6000 Ada Generation"]  # image needs CUDA >= 12.8 drivers


def H():
    return {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def state(name, data=None):
    f = STATE / f"runpod_{name}.json"
    if data is not None:
        STATE.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(data))
        os.chmod(f, 0o600)
    return json.loads(f.read_text())


def agent(name):
    s = state(name)
    return f"https://{s['pod_id']}-8000.proxy.runpod.net", {"X-Token": s["token"]}


def balance():
    r = requests.post("https://api.runpod.io/graphql", headers=H(), timeout=30,
                      json={"query": "query { myself { clientBalance currentSpendPerHr } }"}).json()
    print(json.dumps(r["data"]["myself"]))


def cuda_ok(name):
    """Bad hosts exist (2026-10-20: an L40S pod failed torch.cuda init). Test before running a job."""
    url, hdr = agent(name)
    test = "import torch; torch.zeros(1).cuda(); print('CUDA_OK', torch.cuda.get_device_name(0))"
    for _ in range(5):
        try:
            if requests.post(url + "/run", headers=hdr, json={"name": "cudatest", "cmd": ["python3", "-c", test]}, timeout=60).ok:
                break
        except requests.RequestException:
            pass
        time.sleep(5)
    for _ in range(30):
        time.sleep(4)
        try:
            j = requests.get(url + "/status", headers=hdr, timeout=60).json()["jobs"].get("cudatest")
            if j and j["returncode"] is not None:
                return j["returncode"] == 0 and "CUDA_OK" in j["log_tail"]
        except (requests.RequestException, ValueError):
            pass
    return False


def up(name, gpu=None, wait_min=40):
    t0 = time.time()
    for attempt in range(40):
        try:
            up_once(name, gpu)
        except SystemExit as e:  # no capacity right now: retry every 2 min
            if time.time() - t0 > wait_min * 60:
                raise
            print("no capacity, retry in 2 min", flush=True)
            time.sleep(120)
            continue
        if cuda_ok(name):
            print("cuda ok", flush=True)
            return
        print("bad GPU host, terminating and retrying", flush=True)
        down(name)
        if time.time() - t0 > wait_min * 60:
            break
    sys.exit("no healthy GPU pod in time")


def up_once(name, gpu=None):
    token = secrets.token_urlsafe(24)
    code = base64.b64encode((HERE / "agent.py").read_bytes()).decode()
    last = None
    for cloud in CLOUDS:
        body = {"name": f"cantilandia-{name}", "imageName": IMAGE, "gpuTypeIds": [gpu] if gpu else GPUS, "gpuCount": 1,
                "cloudType": cloud, "containerDiskInGb": 120, "volumeInGb": 0, "ports": ["8000/http"],
                "env": {"AGENT_TOKEN": token, "AGENT_B64": code},
                "dockerStartCmd": ["bash", "-c", "echo $AGENT_B64 | base64 -d > /agent.py && exec python3 /agent.py"]}
        r = requests.post(f"{REST}/pods", headers=H(), json=body, timeout=60)
        if r.ok:
            pod = r.json()
            break
        last = f"{cloud}: {r.status_code} {r.text[:300]}"
        print("create failed", last, flush=True)
    else:
        sys.exit(f"could not create pod ({last})")
    state(name, {"pod_id": pod["id"], "token": token, "created": time.time(), "gpu": pod.get("machine", {}).get("gpuTypeId", gpu)})
    print("pod", pod["id"], "cost/hr", pod.get("costPerHr"), flush=True)
    url, hdr = agent(name)
    for i in range(90):  # up to ~15 min for image pull + start
        try:
            r = requests.get(url + "/status", headers=hdr, timeout=20)
            if r.ok and r.headers.get("Content-Type", "").startswith("application/json") and "gpu" in r.json():
                print("agent ready:", r.json()["gpu"], "disk", r.json()["disk_free_gb"], "GB", flush=True)
                return
        except (requests.RequestException, ValueError):  # the proxy serves a placeholder page until the agent is up
            pass
        time.sleep(10)
    sys.exit("agent did not come up; run `down` to stop billing")


def upload(name, local, remote):
    url, hdr = agent(name)
    for attempt in range(8):  # RunPod's proxy returns sporadic 404/502 while a pod settles
        with open(local, "rb") as f:
            r = requests.put(f"{url}/upload/{remote}", headers=hdr, data=f, timeout=600)
        if r.ok:
            return
        time.sleep(10)
    r.raise_for_status()


def run(name, tasks_file, *inputs):
    tasks = json.loads(Path(tasks_file).read_text())
    body = (HERE.parent / "kaggle" / "runner_template.py").read_text().replace("__TASKS_JSON__", json.dumps(tasks, ensure_ascii=False))
    tmp = STATE / f"runner_{name}.py"
    tmp.write_text(body)
    upload(name, tmp, "runner.py")
    for f in inputs:
        upload(name, f, f"input/{Path(f).name}")
    url, hdr = agent(name)
    # git clone of Wan2GP was very slow on one pod (~50 KB/s) while plain HTTPS ran at 100+ MB/s: fetch the zip instead
    prep = ("mkdir -p /workspace/temp && cd /workspace/temp && [ -d Wan2GP ] || (curl -sL -o w.zip "
            "https://codeload.github.com/deepbeepmeep/Wan2GP/zip/refs/heads/main && python3 -c \"import zipfile;"
            "zipfile.ZipFile('w.zip').extractall('.')\" && mv WanGP-main Wan2GP && rm w.zip)")
    for attempt in range(8):
        if requests.post(url + "/run", headers=hdr, json={"name": "prep", "cmd": ["bash", "-c", prep]}, timeout=60).ok:
            break
        time.sleep(10)
    for _ in range(60):
        time.sleep(5)
        try:
            if requests.get(url + "/status", headers=hdr, timeout=60).json()["jobs"]["prep"]["returncode"] is not None:
                break
        except (requests.RequestException, ValueError, KeyError):
            pass
    env = {"RUNNER_WORK": "/workspace/work", "RUNNER_TEMP": "/workspace/temp", "RUNNER_INPUT": "/workspace/input"}
    for attempt in range(8):
        r = requests.post(url + "/run", headers=hdr, json={"name": "job", "cmd": ["python3", "/workspace/runner.py"], "env": env}, timeout=60)
        if r.ok:
            break
        time.sleep(10)
    r.raise_for_status()
    print("started", r.json(), "tasks", len(tasks))


def status(name):
    url, hdr = agent(name)
    s = requests.get(url + "/status", headers=hdr, timeout=60).json()
    try:
        m = json.loads(requests.get(url + "/file/work/manifest.json", headers=hdr, timeout=60).content)
        done = [t for t in m["tasks"] if t.get("status") == "ok"]
        print(json.dumps({"stages": [x["stage"] for x in m["stages"]], "ok": len(done), "failed": [t["id"] for t in m["tasks"] if t.get("status") not in ("ok", "running")], "running": [t["id"] for t in m["tasks"] if t.get("status") == "running"],
                          "gpu": s["gpu"], "returncode": s["jobs"].get("job", {}).get("returncode")}, ensure_ascii=False))
    except Exception:
        print(json.dumps({"gpu": s["gpu"], "jobs": {k: {"rc": v["returncode"], "tail": v["log_tail"][-600:]} for k, v in s["jobs"].items()}}, ensure_ascii=False))


def fetch(name, local):
    url, hdr = agent(name)
    out = Path(local)
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_bytes(requests.get(url + "/file/work/manifest.json", headers=hdr, timeout=120).content)
    files = requests.get(url + "/ls/work/out", headers=hdr, timeout=60).json()["files"]
    for f in files:
        dest = out / f["name"]
        if dest.exists() and dest.stat().st_size == f["size"]:
            continue
        for attempt in range(4):
            r = requests.get(f"{url}/file/work/out/{f['name']}", headers=hdr, timeout=600)
            if r.ok and len(r.content) == f["size"]:
                dest.write_bytes(r.content)
                break
            time.sleep(3)
    print("fetched", len(files), "files to", out)


def down(name):
    s = state(name)
    r = requests.delete(f"{REST}/pods/{s['pod_id']}", headers=H(), timeout=60)
    print("terminate", s["pod_id"], r.status_code, f"(ran {round((time.time() - s['created']) / 3600, 2)} h)")


def list_pods():
    for p in requests.get(f"{REST}/pods", headers=H(), timeout=60).json():
        print(p["id"], p.get("name"), p.get("desiredStatus"), p.get("costPerHr"))


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "up":
        up(args[0], args[args.index("--gpu") + 1] if "--gpu" in args else None)
    else:
        {"balance": balance, "run": run, "status": status, "fetch": fetch, "down": down, "list": list_pods}[cmd](*args)
