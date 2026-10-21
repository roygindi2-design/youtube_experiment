"""Long episode = new song-story + '+ más canciones' compilation of earlier Tito videos (16:9, 1920x1080).

    python production/longform/compile_mas.py <plan.json>

plan.json: {"out": "<file>.mp4", "items": [{"title": "...", "file": "<mp4>"}, ...]}
Vertical (9:16) videos are placed in the center over a blurred, darkened copy of themselves.
Each item is loudness-normalized to -14 LUFS, and a short fade in/out joins them.
Writes <out> and <out>.chapters.txt (YouTube chapter lines for the description).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())


def size(f):
    w, h = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0", f]).decode().strip().split(",")
    return int(w), int(h)


plan = json.loads(Path(sys.argv[1]).read_text())
tmp = Path(tempfile.mkdtemp())
parts, chapters, t = [], [], 0.0
for i, it in enumerate(plan["items"]):
    f, d = it["file"], dur(it["file"])
    w, h = size(f)
    fade = f"fade=t=in:st=0:d=0.3,fade=t=out:st={d - 0.3:.2f}:d=0.3"
    if h > w:  # vertical Short -> center over blurred background
        vf = (f"[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,"
              f"eq=brightness=-0.12[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,setsar=1,fps=30,{fade}[v]")
    else:
        vf = f"[0:v]scale=1920:1080,setsar=1,fps=30,{fade}[v]"
    out = tmp / f"p{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-filter_complex",
                    vf + f";[0:a]loudnorm=I=-14:TP=-1:LRA=11,aresample=48000,afade=t=in:d=0.3,afade=t=out:st={d - 0.3:.2f}:d=0.3[a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{d:.3f}", str(out)], check=True)
    parts.append(out)
    chapters.append(f"{int(t // 60)}:{int(t % 60):02d} {it['title']}")
    t += dur(str(out))
lst = tmp / "list.txt"
lst.write_text("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart",
                plan["out"]], check=True)
Path(plan["out"] + ".chapters.txt").write_text("\n".join(chapters) + "\n")
print("done", plan["out"], f"{t:.1f} s")
print("\n".join(chapters))
