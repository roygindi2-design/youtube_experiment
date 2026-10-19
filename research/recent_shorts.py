"""Fresh pull: Spanish toddler Shorts published in the last N days, ranked by views per day.

    python research/recent_shorts.py [days=14] > research/data/recent_shorts.json

Uses the YouTube Data API key from env (youtube_api_key / YOUTUBE_API_KEY); the key is never printed or saved.
Cost: ~100 units per search query + 1 per 50 videos (daily quota 10,000).
"""
import datetime as dt
import json
import os
import re
import sys

import requests

KEY = os.environ.get("YOUTUBE_API_KEY") or os.environ.get("youtube_api_key")
API = "https://www.googleapis.com/youtube/v3/"
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 14
QUERIES = ["canciones infantiles #shorts", "canciones para bebés", "aprende los colores niños", "canciones para niños shorts",
           "videos para bebés", "¿dónde está? niños", "cucú bebé", "canción infantil animales", "colores para niños shorts"]


def get(ep, **p):
    r = requests.get(API + ep, params={**p, "key": KEY}, timeout=30)
    r.raise_for_status()
    return r.json()


def secs(d):
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


now = dt.datetime.now(dt.timezone.utc)
after = (now - dt.timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
ids = set()
for q in QUERIES:
    r = get("search", part="id", q=q, type="video", videoDuration="short", order="viewCount", publishedAfter=after,
            regionCode="MX", relevanceLanguage="es", maxResults=50, safeSearch="strict")
    ids |= {i["id"]["videoId"] for i in r.get("items", [])}
ids = sorted(ids)
out = []
for k in range(0, len(ids), 50):
    r = get("videos", part="snippet,statistics,contentDetails,status", id=",".join(ids[k:k + 50]))
    for v in r.get("items", []):
        d = secs(v["contentDetails"]["duration"])
        if d > 61:
            continue
        pub = dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
        age = max((now - pub).total_seconds() / 86400, 0.25)
        views = int(v["statistics"].get("viewCount", 0))
        out.append({"id": v["id"], "title": v["snippet"]["title"], "channel": v["snippet"]["channelTitle"],
                    "published": v["snippet"]["publishedAt"], "hour_utc": pub.hour, "age_days": round(age, 1),
                    "duration_s": d, "views": views, "views_per_day": round(views / age),
                    "likes": int(v["statistics"].get("likeCount", 0)), "mfk": v["status"].get("madeForKids"),
                    "lang": v["snippet"].get("defaultAudioLanguage")})
out.sort(key=lambda x: -x["views_per_day"])
print(json.dumps(out, ensure_ascii=False, indent=1))
