"""Assemble a pilot Short: shot clips + song + SFX + karaoke captions -> 1080x1920 MP4.

    python production/assemble.py production/pilots/<name>/edit.json

edit.json:
{
  "out": "production/pilots/popo/pilot.mp4",
  "fps": 30,
  "song": {"file": "...wav", "start": 0.0, "gain_db": -1},
  "shots": [{"file": "...mp4", "in": 0.0, "dur": 3.2, "speed": 1.0}, ...],   # played in order
  "sfx": [{"file": "...wav", "at": 0.0, "gain_db": -6}, ...],
  "lines": [{"start": 1.0, "end": 3.0, "words": [["¿Listos?", 1.0, 1.6], ["¡A", 1.7, 1.9], ["cepillar!", 1.9, 2.8]]}],
  "font": "Fredoka", "font_file": "production/fonts/Fredoka.ttf",
  "colors": {"text": "#FFFFFF", "active": "#FFD23F", "outline": "#3B2A6B"},
  "caption_y": 0.78,
  "title_card": null
}
Shots are scaled/cropped to 1080x1920 (lanczos), concatenated, trimmed to the song length.
Captions are ASS karaoke (active word changes color), rendered by libass (left-to-right).
Loudness: final mix normalized to -14 LUFS (YouTube reference), true peak -1 dB.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd):
    print("$", " ".join(map(str, cmd))[:300], flush=True)
    subprocess.run(cmd, check=True)


def ass_color(hex_rgb, alpha="00"):
    h = hex_rgb.lstrip("#")
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}"


def ass_time(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def build_ass(e, path):
    c = e.get("colors", {})
    font = e.get("font", "Fredoka")
    y = int(1920 * (1 - e.get("caption_y", 0.78)))
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: K,{font},{e.get('font_size', 96)},{ass_color(c.get('active', '#FFD23F'))},{ass_color(c.get('text', '#FFFFFF'))},{ass_color(c.get('outline', '#3B2A6B'))},&H64000000,1,0,0,0,100,100,0,0,1,{e.get('outline', 9)},3,2,60,60,{y},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    rows = []
    for line in e.get("lines", []):
        parts, cursor = [], line["start"]
        for word, ws, we in line["words"]:
            gap = max(0.0, ws - cursor)
            if gap > 0.005:
                parts.append(f"{{\\k{int(round(gap * 100))}}}")
            parts.append(f"{{\\kf{max(1, int(round((we - ws) * 100)))}}}{word} ")
            cursor = we
        pop = "{\\fscx92\\fscy92\\t(0,120,\\fscx100\\fscy100)}"
        rows.append(f"Dialogue: 0,{ass_time(line['start'])},{ass_time(line['end'])},K,,0,0,0,,{pop}{''.join(parts).strip()}")
    Path(path).write_text(head + "\n".join(rows) + "\n", encoding="utf-8")


def main():
    e = json.loads(Path(sys.argv[1]).read_text())
    fps = e.get("fps", 30)
    out = Path(e["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    parts = []
    for i, s in enumerate(e["shots"]):
        p = tmp / f"s{i:02d}.mp4"
        speed = s.get("speed", 1.0)
        vf = (f"setpts=PTS/{speed},scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
              f"crop=1080:1920,fps={fps},eq=saturation=1.12:contrast=1.04,unsharp=5:5:0.6,format=yuv420p")
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(s.get("in", 0)), "-i", s["file"], "-t", str(s["dur"] * speed),
             "-an", "-vf", vf, "-t", str(s["dur"]), "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(p)])
        parts.append(p)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    video = tmp / "video.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)])
    total = sum(s["dur"] for s in e["shots"])

    # audio mix: song + sfx at their times
    inputs, filters, labels = [], [], []
    song = e["song"]
    inputs += ["-ss", str(song.get("start", 0)), "-i", song["file"]]
    filters.append(f"[0:a]volume={song.get('gain_db', 0)}dB,afade=t=out:st={total - 0.4}:d=0.4[a0]")
    labels.append("[a0]")
    for j, fx in enumerate(e.get("sfx", []), start=1):
        inputs += ["-i", fx["file"]]
        ms = int(fx["at"] * 1000)
        filters.append(f"[{j}:a]volume={fx.get('gain_db', -6)}dB,adelay={ms}|{ms}[a{j}]")
        labels.append(f"[a{j}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{total},"
                   f"loudnorm=I=-14:TP=-1:LRA=11[aout]")
    audio = tmp / "audio.wav"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "[aout]",
         "-ar", "48000", str(audio)])

    ass = tmp / "captions.ass"
    build_ass(e, ass)
    fontsdir = str(Path(e.get("font_file", "production/fonts/x")).resolve().parent)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
         "-vf", f"subtitles={ass}:fontsdir={fontsdir}", "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(fps),
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(total), str(out)])
    print("done", out, round(total, 2), "s")


if __name__ == "__main__":
    main()
