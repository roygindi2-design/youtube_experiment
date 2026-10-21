"""Long-form scan: which LONG kids videos (Spanish, MX) win now — length, structure, chapters, outlier vs channel.

    LF_QUERIES="q1|q2" LF_TAG=name python3 research/longform_scan.py [days=90] [duration=medium|long]

Writes research/market/longform_<date>_<tag>.json (+ .md). Reads chapters (timestamps) from descriptions.
YouTube Data API key from env. Cost: 100 units per query + small.
"""
import datetime as dt, json, os, re, statistics as st, sys
from pathlib import Path
import requests

KEY = os.environ.get("YOUTUBE_API_KEY") or os.environ.get("youtube_api_key")
API = "https://www.googleapis.com/youtube/v3/"
OUT = Path(__file__).resolve().parent / "market"
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 90
DUR = sys.argv[2] if len(sys.argv) > 2 else "medium"
Q = os.environ.get("LF_QUERIES", "canciones infantiles|cuentos infantiles|hábitos para niños|camión de bomberos para niños").split("|")
TAG = os.environ.get("LF_TAG", "general")


def get(ep, **p):
    r = requests.get(API + ep, params={**p, "key": KEY}, timeout=30)
    r.raise_for_status()
    return r.json()


def secs(d):
    m = re.fullmatch(r"P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def chapters(desc):
    ts = re.findall(r"(?m)^\s*\(?((?:\d{1,2}:)?\d{1,2}:\d{2})\)?\s*[-–|]?\s*(.+)$", desc or "")
    out = []
    for t, name in ts:
        p = [int(x) for x in t.split(":")]
        out.append([p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1], name.strip()[:60]])
    return out if len(out) >= 3 and out[0][0] == 0 else []


now = dt.datetime.now(dt.timezone.utc)
after = (now - dt.timedelta(days=DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
ids = set()
for q in Q:
    r = get("search", part="id", q=q, type="video", videoDuration=DUR, order="viewCount", publishedAfter=after,
            regionCode="MX", relevanceLanguage="es", maxResults=50, safeSearch="strict")
    ids |= {i["id"]["videoId"] for i in r.get("items", [])}
vids = []
ids = sorted(ids)
for k in range(0, len(ids), 50):
    vids += get("videos", part="snippet,statistics,contentDetails,status", id=",".join(ids[k:k + 50])).get("items", [])
cids = sorted({v["snippet"]["channelId"] for v in vids})
chans, med = {}, {}
for k in range(0, len(cids), 50):
    for c in get("channels", part="contentDetails,statistics", id=",".join(cids[k:k + 50])).get("items", []):
        chans[c["id"]] = c
for cid, c in chans.items():
    try:
        last = [i["contentDetails"]["videoId"] for i in get("playlistItems", part="contentDetails",
                playlistId=c["contentDetails"]["relatedPlaylists"]["uploads"], maxResults=10).get("items", [])]
        vs = get("videos", part="statistics", id=",".join(last)).get("items", [])
        med[cid] = st.median([int(v["statistics"].get("viewCount", 0)) for v in vs]) if vs else 0
    except requests.HTTPError:
        med[cid] = 0
rows = []
for v in vids:
    s = v["snippet"]; views = int(v["statistics"].get("viewCount", 0))
    age = max((now - dt.datetime.fromisoformat(s["publishedAt"].replace("Z", "+00:00"))).total_seconds() / 86400, 1)
    m = med.get(s["channelId"]) or 0
    ch = chapters(s.get("description", ""))
    rows.append({"id": v["id"], "title": s["title"], "channel": s["channelTitle"], "lang": s.get("defaultAudioLanguage"),
                 "subs": int(chans.get(s["channelId"], {}).get("statistics", {}).get("subscriberCount", 0) or 0),
                 "views": views, "views_per_day": round(views / age), "age_days": round(age, 1),
                 "outlier": round(views / m, 1) if m else None, "duration_s": secs(v["contentDetails"]["duration"]),
                 "mfk": v["status"].get("madeForKids"), "chapters": ch, "n_chapters": len(ch),
                 "desc": s.get("description", "")[:600]})
rows = [r for r in rows if r["views"] >= 20000]
rows.sort(key=lambda r: -r["views_per_day"])
stamp = f"{now:%Y-%m-%d}_{TAG}"
OUT.mkdir(exist_ok=True)
(OUT / f"longform_{stamp}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
md = [f"# Long-form scan {stamp} ({DUR}, {DAYS} days, {len(Q)} queries, {len(rows)} videos ≥20K)", "",
      "| views/day | ×channel | min | chapters | MFK | channel | title |", "|---|---|---|---|---|---|---|"]
md += [f"| {r['views_per_day']:,} | ×{r['outlier']} | {r['duration_s'] / 60:.1f} | {r['n_chapters']} | {'✓' if r['mfk'] else ''} | {r['channel'][:20]} | {r['title'][:80].replace('|', '/')} |" for r in rows[:40]]
(OUT / f"longform_{stamp}.md").write_text("\n".join(md) + "\n")
print("\n".join(md[:30]))
