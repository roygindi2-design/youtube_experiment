"""Burn a short title into a vertical video for TikTok (Roy 23.10: text in the video, nothing to edit in the app).
    python production/tiktok_text.py <in.mp4> <out.mp4> "¿Qué hará Tito?" [--start 0] [--until 2.5] [--y 0.20]
White Lilita One (OFL), thick dark-purple outline + soft shadow, centered, top third, fades out over 0.3 s.
Emoji (e.g. 👀) are drawn in colour from Noto Color Emoji; --start > 0 fades the text in over 0.3 s.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = Path(__file__).resolve().parent / "fonts" / "LilitaOne-Regular.ttf"

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out"); ap.add_argument("text")
ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--until", type=float, default=2.5); ap.add_argument("--y", type=float, default=0.20)
ap.add_argument("--size", type=int, default=104)
a = ap.parse_args()
W, H = 1080, 1920
font = ImageFont.truetype(str(FONT), a.size)
EMOJI = Path("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")
is_emoji = lambda ch: ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF
text = "".join(ch for ch in a.text if not is_emoji(ch) and ch != "\ufe0f").rstrip()
emojis = [ch for ch in a.text if is_emoji(ch)]
l, t, r, b = font.getbbox(text)
tw, th = r - l, b - t
egap, esz = int(a.size * 0.25), int(a.size * 1.05)
full = tw + (egap + esz) * len(emojis)
x, y = (W - full) // 2 - l, int(H * a.y) - th // 2 - t
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).text((x + 6, y + 10), text, font=font, fill=(20, 0, 40, 170), stroke_width=14, stroke_fill=(20, 0, 40, 170))
img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(10)))
ImageDraw.Draw(img).text((x, y), text, font=font, fill=(255, 255, 255, 255), stroke_width=12, stroke_fill=(70, 20, 110, 255))
ex = x + l + tw + egap
for ch in emojis:  # Noto Color Emoji is a bitmap font: draw at its native 109 px, then scale
    ef = ImageFont.truetype(str(EMOJI), 109)
    e = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(e).text((0, 0), ch, font=ef, embedded_color=True)
    e = e.crop(e.getbbox()).resize((esz, esz), Image.LANCZOS)
    img.alpha_composite(e, (ex, int(H * a.y) - esz // 2))
    ex += esz + egap
with tempfile.TemporaryDirectory() as td:
    png = Path(td) / "t.png"
    img.save(png)
    fin = f"fade=t=in:st={a.start}:d=0.3:alpha=1," if a.start > 0 else ""
    f = (f"[1:v]format=rgba,{fin}fade=t=out:st={a.until - 0.3}:d=0.3:alpha=1[t];"
         f"[0:v][t]overlay=0:0:enable='between(t,{a.start},{a.until})',format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.inp, "-loop", "1", "-t", str(a.until + 0.1), "-i", str(png),
                    "-filter_complex", f, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                    "-c:a", "copy", "-movflags", "+faststart", a.out], check=True)
print("done", a.out)
