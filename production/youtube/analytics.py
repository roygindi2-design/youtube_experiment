"""Channel analytics snapshot -> research/analytics/ + dashboard.

    python production/youtube/analytics.py            # one snapshot (run on a schedule)

Data sources:
  - YouTube Data API (scope youtube.readonly): live counters per video (views, likes, comments).
  - YouTube Analytics API (scope yt-analytics.readonly, needs the newer consent): per-video views,
    watch time, average view duration / percentage, and the audience-retention curve
    (audienceWatchRatio by elapsedVideoTimeRatio). Retention for seconds 0-5 is derived from it.
    Analytics data lags ~24-48 h and is empty for very new / tiny videos.
  - NOT available in any public API: the Shorts "viewed vs swiped away" split (Studio only).
Outputs:
  research/analytics/snapshots/<UTC timestamp>.json   raw snapshot
  research/analytics/latest.json                      same, stable name
  dashboard.html                                      the ANALYTICS block between markers is replaced
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import yt  # noqa: E402
from googleapiclient.discovery import build  # noqa: E402
from googleapiclient.errors import HttpError  # noqa: E402

OUT = ROOT / "research" / "analytics"


def iso_seconds(d):
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else None


def main():
    creds = yt.creds()
    data = build("youtube", "v3", credentials=creds)
    ch = data.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = [i["contentDetails"]["videoId"] for i in
           data.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50).execute().get("items", [])]
    vids = data.videos().list(part="snippet,statistics,status,contentDetails", id=",".join(ids)).execute().get("items", []) if ids else []
    now = dt.datetime.now(dt.timezone.utc)
    snap = {"taken": now.strftime("%Y-%m-%d %H:%M UTC"), "channel": {"title": ch["snippet"]["title"], "id": ch["id"],
            "subscribers": int(ch["statistics"].get("subscriberCount", 0)), "views": int(ch["statistics"].get("viewCount", 0)),
            "videos": int(ch["statistics"].get("videoCount", 0))}, "videos": [], "analytics_api": "ok"}
    has_analytics = "https://www.googleapis.com/auth/yt-analytics.readonly" in (creds.scopes or [])
    ya = build("youtubeAnalytics", "v2", credentials=creds) if has_analytics else None
    if not has_analytics:
        snap["analytics_api"] = "missing scope yt-analytics.readonly (re-consent needed)"
    for v in vids:
        pub = v["snippet"]["publishedAt"][:10]
        row = {"id": v["id"], "title": v["snippet"]["title"], "published": pub, "privacy": v["status"]["privacyStatus"],
               "duration_s": iso_seconds(v["contentDetails"]["duration"]),
               "views": int(v["statistics"].get("viewCount", 0)), "likes": int(v["statistics"].get("likeCount", 0)),
               "comments": int(v["statistics"].get("commentCount", 0))}
        if ya:
            try:
                q = dict(ids="channel==MINE", startDate=pub, endDate=now.strftime("%Y-%m-%d"), filters=f"video=={v['id']}")
                r = ya.reports().query(metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage", **q).execute()
                if r.get("rows"):
                    row.update(dict(zip([h["name"] for h in r["columnHeaders"]], r["rows"][0])))
                rr = ya.reports().query(dimensions="elapsedVideoTimeRatio", metrics="audienceWatchRatio,relativeRetentionPerformance", **q).execute()
                curve = [(x[0], x[1]) for x in rr.get("rows", [])]
                row["retention_curve"] = curve
                if curve and row["duration_s"]:
                    first5 = [w for t, w in curve if t * row["duration_s"] <= 5.0]
                    row["retention_0_5s"] = round(min(first5), 3) if first5 else None
            except HttpError as e:
                row["analytics_error"] = f"{e.status_code}: {str(e.content)[:160]}"
        snap["videos"].append(row)
    (OUT / "snapshots").mkdir(parents=True, exist_ok=True)
    name = now.strftime("%Y%m%dT%H%MZ")
    (OUT / "snapshots" / f"{name}.json").write_text(json.dumps(snap, ensure_ascii=False, indent=1))
    (OUT / "latest.json").write_text(json.dumps(snap, ensure_ascii=False, indent=1))
    dash = ROOT / "dashboard.html"
    if dash.exists():
        html = dash.read_text()
        block = "/*ANALYTICS*/" + json.dumps({k: snap[k] for k in ("taken", "channel", "analytics_api")} |
                                              {"videos": [{k: x.get(k) for k in ("id", "title", "privacy", "duration_s", "views", "likes",
                                                                                   "averageViewPercentage", "averageViewDuration", "retention_0_5s")}
                                                          for x in snap["videos"]]}, ensure_ascii=False) + "/*END*/"
        html = re.sub(r"/\*ANALYTICS\*/.*?/\*END\*/", lambda _: block, html, flags=re.S)
        dash.write_text(html)
    print(json.dumps({k: snap[k] for k in ("taken", "channel", "analytics_api")}, ensure_ascii=False))
    for x in snap["videos"]:
        print(x["id"], x["privacy"], "views", x["views"], "likes", x["likes"], "avg%", x.get("averageViewPercentage"), "ret0-5", x.get("retention_0_5s"))


if __name__ == "__main__":
    main()
