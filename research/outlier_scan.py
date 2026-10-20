"""Outlier scan: which kids' Shorts beat THEIR OWN channel's normal by the most (format wins, not brand size).

    python research/outlier_scan.py [days=60]

1. Many searches (Spanish toddler topics), Shorts only, published in the last N days, region MX.
2. For every channel found: its last 10 uploads -> median views (the channel's "normal").
3. Outlier score = video views / channel median. Small channel + huge score = the format/hook worked.
Writes research/market/outliers_<date>.md + .json. YouTube Data API key from env; ~2-3k quota units.
"""
import datetime as dt
import json
import os
import re
import statistics as st
import sys
from pathlib import Path

import requests

KEY = os.environ.get("YOUTUBE_API_KEY") or os.environ.get("youtube_api_key")
API = "https://www.googleapis.com/youtube/v3/"
OUT = Path(__file__).resolve().parent / "market"
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 60
QUERIES_ENV = os.environ.get("OUTLIER_QUERIES")  # e.g. "hora del baño canción|no se quiere bañar" for a niche study
QUERIES = QUERIES_ENV.split("|") if QUERIES_ENV else ["canciones infantiles", "canciones para bebés", "aprende los colores", "canciones para niños", "videos para bebés",
           "dibujos animados para niños", "canción infantil animales", "hábitos para niños canción", "lavarse las manos canción",
           "cepillarse los dientes canción", "canción para dormir bebé", "números para niños", "frutas para niños",
           "elefante canción infantil", "sorpresa niños colores", "bebé aprende", "nursery rhymes español", "cuentos infantiles cortos"]


def get(ep, **p):
    r = requests.get(API + ep, params={**p, "key": KEY}, timeout=30)
    r.raise_for_status()
    return r.json()


def secs(d):
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def videos(ids):
    out = []
    for k in range(0, len(ids), 50):
        out += get("videos", part="snippet,statistics,contentDetails,status", id=",".join(ids[k:k + 50])).get("items", [])
    return out


now = dt.datetime.now(dt.timezone.utc)
after = (now - dt.timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
ids = set()
for q in QUERIES:
    r = get("search", part="id", q=q, type="video", videoDuration="short", order="viewCount", publishedAfter=after,
            regionCode="MX", relevanceLanguage="es", maxResults=50, safeSearch="strict")
    ids |= {i["id"]["videoId"] for i in r.get("items", [])}
cands = [v for v in videos(sorted(ids)) if secs(v["contentDetails"]["duration"]) <= 61]
chan_ids = sorted({v["snippet"]["channelId"] for v in cands})
chans = {}
for k in range(0, len(chan_ids), 50):
    for c in get("channels", part="contentDetails,statistics,snippet", id=",".join(chan_ids[k:k + 50])).get("items", []):
        chans[c["id"]] = c
medians = {}
for cid, c in chans.items():
    pl = c["contentDetails"]["relatedPlaylists"]["uploads"]
    try:
        last = [i["contentDetails"]["videoId"] for i in get("playlistItems", part="contentDetails", playlistId=pl, maxResults=10).get("items", [])]
        views = [int(v["statistics"].get("viewCount", 0)) for v in videos(last)]
        medians[cid] = st.median(views) if views else 0
    except requests.HTTPError:
        medians[cid] = 0
rows = []
for v in cands:
    cid = v["snippet"]["channelId"]
    views = int(v["statistics"].get("viewCount", 0))
    med = medians.get(cid) or 0
    subs = int(chans.get(cid, {}).get("statistics", {}).get("subscriberCount", 0) or 0)
    pub = dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
    rows.append({"id": v["id"], "title": v["snippet"]["title"], "channel": v["snippet"]["channelTitle"], "subs": subs,
                 "views": views, "channel_median": int(med), "outlier": round(views / med, 1) if med else None,
                 "duration_s": secs(v["contentDetails"]["duration"]), "age_days": round((now - pub).total_seconds() / 86400, 1),
                 "mfk": v["status"].get("madeForKids"), "lang": v["snippet"].get("defaultAudioLanguage")})
rows = [r for r in rows if r["outlier"] and r["views"] >= 50_000]
rows.sort(key=lambda r: -r["outlier"])
OUT.mkdir(exist_ok=True)
stamp = now.strftime("%Y-%m-%d")
TAG = os.environ.get("OUTLIER_TAG", "")
stamp = f"{stamp}_{TAG}" if TAG else stamp
(OUT / f"outliers_{stamp}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
md = [f"# Outliers — Shorts לילדים שעקפו את הנורמה של הערוץ שלהם ({stamp}, {DAYS} ימים, {len(QUERIES)} חיפושים, {len(cands)} Shorts, {len(chans)} ערוצים)", "",
      "outlier = צפיות הסרטון / חציון 10 הסרטונים האחרונים של הערוץ. ערוץ קטן עם outlier גבוה = הפורמט עבד, לא המותג.", "",
      "| ×ערוץ | צפיות | מנויים | אורך | MFK | ערוץ | כותרת |", "|---|---|---|---|---|---|---|"]
md += [f"| ×{r['outlier']} | {r['views']:,} | {r['subs']:,} | {r['duration_s']}s | {'✓' if r['mfk'] else ''} | {r['channel'][:22]} | {r['title'][:85].replace('|', '/')} |" for r in rows[:40]]
(OUT / f"outliers_{stamp}.md").write_text("\n".join(md) + "\n")
print("\n".join(md[:45]))
