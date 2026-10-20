"""Designed title card (kids-channel style) rendered as a transparent PNG, animated by assemble.py.

    python production/title_card.py "¡Tito no se|quiere bañar!" out.png [--accent 2]

Look: chunky rounded font (Lilita One, OFL), vertical gradient fill (sunny yellow -> orange), thin white inner outline,
thick deep-purple outer outline, soft drop shadow, slight tilt, a few glossy bubbles and sparkles around it.
"|" separates lines. --accent N colors line N (1-based) with a sky-blue gradient for contrast.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
FONT = ROOT / "fonts" / "LilitaOne-Regular.ttf"
PURPLE = (43, 22, 92, 255)
GRAD_WARM = ((255, 236, 92), (255, 150, 28))
GRAD_COOL = ((140, 226, 255), (40, 140, 245))


def gradient(size, top, bottom):
    w, h = size
    g = Image.new("RGBA", size)
    px = g.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (255,)
        for x in range(w):
            px[x, y] = c
    return g


def text_mask(line, font, pad):
    l, t, r, b = font.getbbox(line)
    m = Image.new("L", (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(m).text((pad - l, pad - t), line, font=font, fill=255)
    return m


def dilate(mask, px):
    return mask.filter(ImageFilter.MaxFilter(px * 2 + 1)) if px > 0 else mask


def render_line(line, size, cool=False):
    font = ImageFont.truetype(str(FONT), size)
    pad = int(size * 0.32)
    core = text_mask(line, font, pad)
    inner = dilate(core, max(3, size // 26))          # white inner outline
    outer = dilate(inner, max(8, size // 9))          # thick purple outline
    W, H = core.size
    img = Image.new("RGBA", (W, H + size // 10), (0, 0, 0, 0))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (20, 8, 50, 140))
    shadow.paste(sh, (0, size // 12), outer)
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(size // 18)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(Image.new("RGBA", (W, H), PURPLE), (0, 0), outer)
    layer.paste(Image.new("RGBA", (W, H), (255, 255, 255, 255)), (0, 0), inner)
    top, bottom = GRAD_COOL if cool else GRAD_WARM
    layer.paste(gradient((W, H), top, bottom), (0, 0), core)
    # glossy highlight on the upper part of the letters
    gloss = Image.new("L", (W, H), 0)
    ImageDraw.Draw(gloss).rectangle([0, 0, W, int(H * 0.42)], fill=70)
    gloss = ImageChops.multiply(gloss, core)
    layer.paste(Image.new("RGBA", (W, H), (255, 255, 255, 255)), (0, 0), gloss)
    img.alpha_composite(layer, (0, 0))
    return img


def bubble(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 235, 255, 120), outline=(255, 255, 255, 230), width=max(3, r // 6))
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.15, cy - r * 0.25], fill=(255, 255, 255, 220))


def sparkle(d, cx, cy, r, color=(255, 246, 170, 255)):
    pts = []
    for k in range(8):
        a = math.pi / 4 * k
        rr = r if k % 2 == 0 else r * 0.32
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=color, outline=(255, 255, 255, 255))


def render(text, out, width=1080, accent=None, size=150):
    lines = [l.strip() for l in text.split("|")]
    imgs = [render_line(l, size, cool=(accent == i + 1)) for i, l in enumerate(lines)]
    for i, im in enumerate(imgs):  # shrink a line that is too wide
        if im.width > width * 0.96:
            s2 = int(size * width * 0.96 / im.width)
            imgs[i] = render_line(lines[i], s2, cool=(accent == i + 1))
    gap = -int(size * 0.28)
    H = sum(im.height for im in imgs) + gap * (len(imgs) - 1) + 120
    canvas = Image.new("RGBA", (width, H), (0, 0, 0, 0))
    y = 50
    for im in imgs:
        canvas.alpha_composite(im, ((width - im.width) // 2, y))
        y += im.height + gap
    d = ImageDraw.Draw(canvas)
    bubble(d, int(width * 0.08), int(H * 0.30), 30)
    bubble(d, int(width * 0.93), int(H * 0.62), 38)
    bubble(d, int(width * 0.86), int(H * 0.16), 18)
    sparkle(d, int(width * 0.14), int(H * 0.80), 34)
    sparkle(d, int(width * 0.90), int(H * 0.30), 24)
    canvas = canvas.rotate(-3, resample=Image.BICUBIC, expand=False)
    canvas.save(out)
    return out


if __name__ == "__main__":
    acc = int(sys.argv[sys.argv.index("--accent") + 1]) if "--accent" in sys.argv else None
    print(render(sys.argv[1], sys.argv[2], accent=acc))
