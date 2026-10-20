"""Tiny HTTP agent that runs inside a RunPod pod (stdlib only). Started by the pod's docker start command.

Every request needs header X-Token == $AGENT_TOKEN (a random value made per pod by rp.py; not a RunPod key).
  PUT  /upload/<path>      write the body to /workspace/<path>
  POST /run                body {"name": "...", "cmd": ["python3", ...], "env": {...}} -> background process, log in /workspace/logs/<name>.log
  GET  /status             {"jobs": {name: {"pid", "returncode", "log_tail"}}, "gpu": nvidia-smi line, "disk_free_gb"}
  GET  /ls/<dir>           file list (name, size) under /workspace/<dir>
  GET  /file/<path>        download /workspace/<path>
Served on port 8000, reached from outside through RunPod's HTTPS proxy: https://<podId>-8000.proxy.runpod.net
"""
import json
import os
import shutil
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path("/workspace")
TOKEN = os.environ["AGENT_TOKEN"]
JOBS = {}


def safe(rel):
    p = (ROOT / rel).resolve()
    if ROOT.resolve() not in p.parents and p != ROOT.resolve():
        raise PermissionError(rel)
    return p


class H(BaseHTTPRequestHandler):
    def _ok(self, obj=None, body=None, ctype="application/json"):
        data = body if body is not None else json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _auth(self):
        if self.headers.get("X-Token") != TOKEN:
            self.send_response(403)
            self.end_headers()
            return False
        return True

    def do_PUT(self):
        if not self._auth():
            return
        p = safe(self.path.split("/upload/", 1)[1])
        p.parent.mkdir(parents=True, exist_ok=True)
        n = int(self.headers.get("Content-Length", 0))
        with open(p, "wb") as f:
            while n > 0:
                chunk = self.rfile.read(min(n, 1 << 20))
                f.write(chunk)
                n -= len(chunk)
        self._ok({"saved": str(p), "bytes": p.stat().st_size})

    def do_POST(self):
        if not self._auth():
            return
        req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        (ROOT / "logs").mkdir(parents=True, exist_ok=True)
        log = open(ROOT / "logs" / f"{req['name']}.log", "ab")
        proc = subprocess.Popen(req["cmd"], stdout=log, stderr=subprocess.STDOUT, cwd=str(ROOT),
                                env=dict(os.environ, **req.get("env", {})))
        JOBS[req["name"]] = proc
        self._ok({"started": req["name"], "pid": proc.pid})

    def do_GET(self):
        if not self._auth():
            return
        if self.path == "/status":
            jobs = {}
            for name, proc in JOBS.items():
                logf = ROOT / "logs" / f"{name}.log"
                tail = logf.read_bytes()[-1500:].decode(errors="replace") if logf.exists() else ""
                jobs[name] = {"pid": proc.pid, "returncode": proc.poll(), "log_tail": tail}
            gpu = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu", "--format=csv,noheader"],
                                 capture_output=True, text=True).stdout.strip()
            self._ok({"jobs": jobs, "gpu": gpu, "disk_free_gb": round(shutil.disk_usage(ROOT).free / 1e9, 1)})
        elif self.path.startswith("/ls/"):
            d = safe(self.path[4:])
            files = [{"name": str(p.relative_to(d)), "size": p.stat().st_size} for p in sorted(d.rglob("*")) if p.is_file()] if d.exists() else []
            self._ok({"files": files})
        elif self.path.startswith("/file/"):
            p = safe(self.path[6:])
            self._ok(body=p.read_bytes(), ctype="application/octet-stream")
        else:
            self._ok({"ok": True})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()
