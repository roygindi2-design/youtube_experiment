"""Burn a short title into a vertical video for TikTok (Roy 23.10: text in the video, nothing to edit in the app).
    python production/tiktok_text.py <in.mp4> <out.mp4> "¿Qué hará Tito?" [--until 2.5] [--y 0.20]
White Lilita One (OFL), thick dark-purple outline + soft shadow, centered, top third, fades out over 0.3 s.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = Path(__file__).resolve().parent / "fonts" / "LilitaOne-Regular.ttf"

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out"); ap.add_argument("text")
ap.add_argument("--until", type=float, default=2.5); ap.add_argument("--y", type=float, default=0.20)
ap.add_argument("--size", type=int, default=104)
a = ap.parse_args()
W, H = 1080, 1920
font = ImageFont.truetype(str(FONT), a.size)
l, t, r, b = font.getbbox(a.text)
tw, th = r - l, b - t
x, y = (W - tw) // 2 - l, int(H * a.y) - th // 2 - t
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).text((x + 6, y + 10), a.text, font=font, fill=(20, 0, 40, 170), stroke_width=14, stroke_fill=(20, 0, 40, 170))
img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(10)))
ImageDraw.Draw(img).text((x, y), a.text, font=font, fill=(255, 255, 255, 255), stroke_width=12, stroke_fill=(70, 20, 110, 255))
with tempfile.TemporaryDirectory() as td:
    png = Path(td) / "t.png"
    img.save(png)
    f = (f"[1:v]format=rgba,fade=t=out:st={a.until - 0.3}:d=0.3:alpha=1[t];"
         f"[0:v][t]overlay=0:0:enable='lte(t,{a.until})',format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.inp, "-loop", "1", "-t", str(a.until + 0.1), "-i", str(png),
                    "-filter_complex", f, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                    "-c:a", "copy", "-movflags", "+faststart", a.out], check=True)
print("done", a.out)
