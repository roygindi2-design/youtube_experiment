"""Cut a vertical Short (1080x1920) out of a 16:9 episode master.

    python production/make_short.py <master.mp4> <out.mp4> <in> <out_t> [range:mode ...]

Default framing = center crop (x center 0.5). Extra ranges override it:
    16.70-20.83:x0.47        center crop with the crop centre at x=0.47 of the frame width
    77.47-82.43:pan0.40-0.60 crop centre moves linearly from x=0.40 to x=0.60 over the range
    88.10-90.67:fit          whole 16:9 frame scaled to 1080 wide, over a blurred zoomed copy (no black bars)
Times are master times. Audio = the master audio of the same span. No text, no fades.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

W, H = 1080, 1920


def vf(mode, dur):
    if mode == "fit":
        return ("split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.06[bg];"
                "[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2")
    if mode.startswith("pan"):
        x0, x1 = (float(v) for v in mode[3:].split("-"))
        cx = f"({x0}+({x1}-{x0})*t/{dur:.3f})"
    else:
        cx = mode[1:] if mode.startswith("x") else "0.5"
    # scale the 16:9 frame to 1920 tall (3413 wide), then crop a 1080-wide window around cx
    return f"scale=-2:1920,crop=1080:1920:x='min(max(iw*{cx}-540\\,0)\\,iw-1080)':y=0"


def main():
    master, out, a, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    rules = []
    for r in sys.argv[5:]:
        span, mode = r.split(":")
        s, e = (float(v) for v in span.split("-"))
        rules.append((max(s, a), min(e, b), mode))
    rules.sort()
    pieces, t = [], a
    for s, e, m in rules:
        if s > t + 1e-3:
            pieces.append((t, s, "x0.5"))
        pieces.append((s, e, m))
        t = e
    if b > t + 1e-3:
        pieces.append((t, b, "x0.5"))
    tmp = Path(tempfile.mkdtemp())
    lst = []
    for k, (s, e, m) in enumerate(pieces):
        p = tmp / f"p{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{e - s:.3f}", "-i", master,
                        "-vf", vf(m, e - s) + ",fps=30,setsar=1", "-an", "-c:v", "libx264", "-preset", "slow",
                        "-crf", "17", "-pix_fmt", "yuv420p", str(p)], check=True)
        lst.append(f"file '{p}'")
        print(f"  {s:7.2f}-{e:7.2f} {m}")
    (tmp / "list.txt").write_text("\n".join(lst))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
                    "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", master, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print("done", out, round(b - a, 2), "s")


if __name__ == "__main__":
    main()
