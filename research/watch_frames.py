"""Visual study of winning Shorts: 4 public frames per video (cover, 25%, 50%, 75%) from YouTube's thumbnail CDN.

    python research/watch_frames.py [outliers.json] [n=24]

Takes the latest research/market/outliers_*.json (Made-for-Kids, >=200k views), writes contact sheets to
research/market/frames_<date>/sheet_<k>.jpg for visual review before writing a dossier.
The video files themselves can't be fetched from this server (YouTube blocks it); we do not work around that.
"""
import datetime as dt
import io
import json
import sys
from pathlib import Path

import requests
from PIL import Image, ImageDraw

M = Path(__file__).resolve().parent / "market"
src = Path(sys.argv[1]) if len(sys.argv) > 1 else sorted(M.glob("outliers_*.json"))[-1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 24
rows = [r for r in json.loads(src.read_text()) if r.get("mfk") and r["views"] >= 200_000][:n]
out = M / f"frames_{dt.date.today():%Y-%m-%d}"
out.mkdir(parents=True, exist_ok=True)
W, H = 240, 180
for g in range(0, len(rows), 6):
    sheet = Image.new("RGB", (W * 4, (H + 16) * 6), "black")
    d = ImageDraw.Draw(sheet)
    for i, r in enumerate(rows[g:g + 6]):
        y = i * (H + 16)
        d.text((3, y + 2), f"#{g + i + 1} x{r['outlier']} {r['views'] // 1000}k {r['duration_s']}s | {r['channel'][:18]} | {r['title'][:70]}", fill="yellow")
        for k, name in enumerate(["hqdefault", "hq1", "hq2", "hq3"]):
            try:
                img = requests.get(f"https://i.ytimg.com/vi/{r['id']}/{name}.jpg", timeout=30).content
                sheet.paste(Image.open(io.BytesIO(img)).convert("RGB").resize((W, H)), (k * W, y + 16))
            except Exception:
                pass
    sheet.save(out / f"sheet_{g // 6}.jpg", quality=85)
(out / "videos.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
print(out, len(rows), "videos")
