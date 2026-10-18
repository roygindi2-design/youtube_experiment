"""
YouTube Data API research: Spanish-language toddler/kids market (Mexico / LATAM).

Usage:
    python research/yt_latam_kids.py collect   # calls the API (cached on disk, safe to re-run)
    python research/yt_latam_kids.py analyze   # builds tables + research/data/analysis.json

The API key is read from the environment (YOUTUBE_API_KEY or youtube_api_key)
or from a .env file in the repo root. It is never written to disk.
"""
import datetime as dt
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CACHE = DATA / "cache"
API = "https://www.googleapis.com/youtube/v3/"

TODAY = dt.datetime(2026, 10, 18, tzinfo=dt.timezone.utc)
WINDOW_START = TODAY - dt.timedelta(days=730)          # last 2 years
BREAKOUT_SINCE = TODAY - dt.timedelta(days=365 * 3)    # channels created in last 3 years

REGION = "MX"
LANG = "es"

# Broad queries: generic words with no topic in them. Used for the "unbiased" check of themes.
BROAD_QUERIES = [
    "para niños", "infantil", "videos para niños", "videos infantiles", "para bebés",
    "videos para bebés", "canciones infantiles", "música para niños", "caricaturas para niños",
    "dibujos animados para niños", "niños", "bebés", "kids español", "videos para niños pequeños",
]
# Format/genre queries: still not about a specific topic, but name a format.
FORMAT_QUERIES = [
    "canciones para niños", "canciones para bebés", "rondas infantiles", "cuentos para niños",
    "historias para niños", "educativo para niños", "aprende con", "canción infantil",
    "juguetes", "animados para niños", "videos para niños en español",
]
# Searches with no keyword at all, per category: the least biased source we have.
NOQ_CATEGORIES = {"1": "Film & Animation", "10": "Music", "24": "Entertainment", "27": "Education", None: "Any"}

PAGES_PER_QUERY = 2
quota_used = 0


def api_key():
    k = os.environ.get("YOUTUBE_API_KEY") or os.environ.get("youtube_api_key")
    env = ROOT.parent / ".env"
    if not k and env.exists():
        for line in env.read_text().splitlines():
            if line.strip().upper().startswith("YOUTUBE_API_KEY="):
                k = line.split("=", 1)[1].strip().strip('"\'')
    if not k:
        sys.exit("Missing YOUTUBE_API_KEY")
    return k


COST = {"search": 100, "videos": 1, "channels": 1, "playlistItems": 1}


def call(endpoint, **params):
    """GET with a disk cache keyed by params (key excluded), so re-runs cost nothing."""
    global quota_used
    params = {k: v for k, v in params.items() if v is not None}
    h = hashlib.sha1(json.dumps([endpoint, params], sort_keys=True).encode()).hexdigest()[:16]
    f = CACHE / f"{endpoint}_{h}.json"
    if f.exists():
        return json.loads(f.read_text())
    for attempt in range(4):
        r = requests.get(API + endpoint, params={**params, "key": api_key()}, timeout=30)
        if r.status_code == 200:
            break
        err = r.json().get("error", {})
        reason = (err.get("errors") or [{}])[0].get("reason", "")
        if reason in ("quotaExceeded", "dailyLimitExceeded"):
            raise SystemExit(f"Quota exhausted after ~{quota_used} units. Re-run tomorrow; cache is kept.")
        if r.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        raise RuntimeError(f"{endpoint} {r.status_code}: {err.get('message')}")
    quota_used += COST[endpoint]
    data = r.json()
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False))
    return data


def search_videos(q, category, label):
    out, token = [], None
    for _ in range(PAGES_PER_QUERY):
        d = call("search", part="snippet", type="video", order="viewCount", maxResults=50,
                 regionCode=REGION, relevanceLanguage=LANG, q=q, videoCategoryId=category,
                 publishedAfter=WINDOW_START.strftime("%Y-%m-%dT%H:%M:%SZ"), pageToken=token)
        out += [(i["id"]["videoId"], label) for i in d.get("items", [])]
        token = d.get("nextPageToken")
        if not token:
            break
    return out


def batched(ids, n=50):
    ids = list(ids)
    for i in range(0, len(ids), n):
        yield ids[i:i + n]


def fetch_videos(ids):
    rows = []
    for b in batched(ids):
        d = call("videos", part="snippet,contentDetails,statistics,status,topicDetails", id=",".join(b), maxResults=50)
        rows += d.get("items", [])
    return rows


def fetch_channels(ids):
    rows = []
    for b in batched(ids):
        d = call("channels", part="snippet,statistics,contentDetails,status,brandingSettings", id=",".join(b), maxResults=50)
        rows += d.get("items", [])
    return rows


def collect():
    DATA.mkdir(exist_ok=True)
    hits = []
    for q in BROAD_QUERIES:
        hits += search_videos(q, None, "broad:" + q)
    for q in FORMAT_QUERIES:
        hits += search_videos(q, None, "format:" + q)
    for cat, name in NOQ_CATEGORIES.items():
        hits += search_videos(None, cat, "noq:" + name)
    print(f"search hits: {len(hits)}, quota so far ~{quota_used}")

    sources = defaultdict(set)
    for vid, label in hits:
        sources[vid].add(label)
    videos = fetch_videos(sources)
    for v in videos:
        v["_sources"] = sorted(sources[v["id"]])
    (DATA / "videos_raw.json").write_text(json.dumps(videos, ensure_ascii=False))

    ch_ids = {v["snippet"]["channelId"] for v in videos if v["status"].get("madeForKids")}
    channels = fetch_channels(ch_ids)
    (DATA / "channels_raw.json").write_text(json.dumps(channels, ensure_ascii=False))

    # Breakout channels: created in last 3 years. Pull their latest 50 uploads.
    recent = [c for c in channels if parse_t(c["snippet"]["publishedAt"]) >= BREAKOUT_SINCE]
    uploads = {}
    for c in recent:
        pl = c["contentDetails"]["relatedPlaylists"]["uploads"]
        d = call("playlistItems", part="contentDetails", playlistId=pl, maxResults=50)
        uploads[c["id"]] = [i["contentDetails"]["videoId"] for i in d.get("items", [])]
    up_videos = fetch_videos({v for vs in uploads.values() for v in vs})
    (DATA / "breakout_uploads_raw.json").write_text(json.dumps({"map": uploads, "videos": up_videos}, ensure_ascii=False))
    print(f"videos: {len(videos)}, channels: {len(channels)}, breakout channels: {len(recent)}, quota this run ~{quota_used}")


# ---------------- analysis ----------------

def parse_t(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso_dur(s):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    if not m:
        return None
    d, h, mi, se = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def to_df(items):
    rows = []
    for v in items:
        s, st, cd = v["snippet"], v.get("statistics", {}), v["contentDetails"]
        pub = parse_t(s["publishedAt"])
        views = int(st.get("viewCount", 0))
        age = max((TODAY - pub).days, 1)
        rows.append(dict(
            id=v["id"], title=s["title"], channel=s["channelTitle"], channel_id=s["channelId"],
            published=pub, age_days=age, duration_s=iso_dur(cd.get("duration")),
            views=views, views_per_day=views / age,
            likes=int(st["likeCount"]) if "likeCount" in st else None,
            comments=int(st["commentCount"]) if "commentCount" in st else None,
            mfk=bool(v["status"].get("madeForKids")),
            audio_lang=s.get("defaultAudioLanguage") or "", meta_lang=s.get("defaultLanguage") or "",
            category=s.get("categoryId"), tags=s.get("tags", []), definition=cd.get("definition"),
            caption=cd.get("caption"), licensed=cd.get("licensedContent"),
            sources=v.get("_sources", []),
            title_len=len(s["title"]), title_has_emoji=bool(re.search(r"[\U0001F300-\U0001FAFF☀-➿]", s["title"])),
            weekday=pub.strftime("%a"), hour_utc=pub.hour,
        ))
    return pd.DataFrame(rows)


SPANISH_HINT = re.compile(r"\b(para|niños|niñas|bebés|bebes|canción|canciones|infantil|infantiles|los|las|el|la|de|y|con|en|aprende|cuento|cuentos)\b", re.I)


def is_spanish(r):
    for l in (r.audio_lang, r.meta_lang):
        if l:
            return l.lower().startswith("es")
    return bool(SPANISH_HINT.search(r.title))


BUCKETS = [(0, 60, "≤1 דק' (Shorts)"), (60, 120, "1–2 דק'"), (120, 240, "2–4 דק'"), (240, 360, "4–6 דק'"),
           (360, 900, "6–15 דק'"), (900, 1800, "15–30 דק'"), (1800, 3600, "30–60 דק'"), (3600, 10 ** 9, "60+ דק'")]


def bucket(s):
    for lo, hi, name in BUCKETS:
        if lo <= s < hi:
            return name
    return None


STOP = set("""de la el los las y en con para por un una del al a o que se su sus es lo mas más tu te mi
me nos le les como este esta son muy the and for of to in kids video videos niños niñas infantil infantiles
canciones canción cancion para bebés bebes bebé bebe español espanol spanish songs song nursery rhymes
dibujos animados caricaturas música musica aprende learn compilation compilación recopilación minutos min
hd 4k new nuevo nueva episodio ep capitulo capítulo full mix""".split())

# Theme dictionary (Spanish stems). Counts are reported next to raw word counts so the dictionary can be checked.
THEMES = {
    "חיות": r"animal|perr|gat|vaca|pollit|pato|granja|leon|león|elefant|mono|pez|peces|tibur|dinosaur|oso|conej|caball|cerdit|ranita|rana|pájar|pajar|abeja|araña|ardilla|jirafa|tigre|zoo",
    "צבעים": r"\bcolor|colores",
    "מספרים/ספירה": r"número|numero|\bcontar|cuenta hasta|\b1 al 10|uno dos tres",
    "אותיות/ABC": r"\babc\b|abecedario|letras|vocales|alfabeto",
    "ריקוד/תנועה": r"bail|danza|dance|mueve|moverse|salta|aplaud|cabeza hombros|freeze|congela",
    "שגרות והרגלים": r"baño|bañ|dormir|duerme|cepill|dientes|lava|comer|comida|vegetal|verdura|ir al baño|pañal|orinal|vacuna|doctor|médic|enferm|aseo|buenos hábitos|hábito|recoger|ordenar",
    "רגשות/התנהגות": r"emocion|emoción|triste|feliz|enojad|miedo|celos|compart|perdón|por favor|gracias|amigos",
    "משפחה": r"mamá|mama|papá|papa|familia|herman|abuel|bebé nuevo",
    "כלי רכב": r"carro|coche|camion|camión|tren|autobús|autobus|bus\b|avión|avion|bombero|policía|policia|excavadora|tractor|monster truck",
    "צעצועים/משחק": r"juguete|juguetes|slime|plastilina|play doh|unboxing|sorpresa|huevo sorpresa|muñec|lego",
    "חגים ועונות": r"navidad|halloween|cumpleaños|feliz cumpleaños|día de muertos|reyes|pascua|invierno|verano|lluvia",
    "שיר ערש/רגוע": r"cuna|arrull|dormir bebé|relaj|calma|lullaby|nana\b|música para dormir",
    "מפלצות/הפחדה עדינה": r"monstru|fantasma|bruja|zombie|miedo",
    "נסיכות/פנטזיה": r"princes|unicornio|sirena|hada|dragón|dragon|magia|mágic",
    "גוף ובריאות": r"cuerpo|partes del cuerpo|boo boo|pupa|herida|curita",
}


def words(text):
    return re.findall(r"[a-záéíóúñü0-9]+", text.lower())


def theme_table(df):
    rows = []
    total_views = df.views.sum()
    for th, rx in THEMES.items():
        pat = re.compile(rx, re.I)
        m = df.apply(lambda r: bool(pat.search(r.title + " " + " ".join(r.tags))), axis=1)
        sub = df[m]
        rows.append(dict(theme=th, videos=len(sub), share_videos=len(sub) / len(df),
                         share_views=sub.views.sum() / total_views if total_views else 0,
                         median_views=sub.views.median() if len(sub) else 0,
                         median_vpd=sub.views_per_day.median() if len(sub) else 0))
    return pd.DataFrame(rows).sort_values("share_views", ascending=False)


def word_lift(df, field="title", min_count=8):
    """Words that appear more in the top quartile (views/day) than in the bottom quartile."""
    q75, q25 = df.views_per_day.quantile(.75), df.views_per_day.quantile(.25)
    top, bot = df[df.views_per_day >= q75], df[df.views_per_day <= q25]

    def cnt(d):
        c = Counter()
        for _, r in d.iterrows():
            txt = r.title if field == "title" else " ".join(r.tags)
            c.update(set(w for w in words(txt) if w not in STOP and len(w) > 2))
        return c
    ct, cb, call_ = cnt(top), cnt(bot), cnt(df)
    rows = []
    for w, n in call_.items():
        if n < min_count:
            continue
        pt, pb = ct[w] / max(len(top), 1), cb[w] / max(len(bot), 1)
        rows.append(dict(word=w, n=n, top_rate=pt, bottom_rate=pb, lift=(pt + .01) / (pb + .01)))
    return pd.DataFrame(rows).sort_values("n", ascending=False)


def analyze():
    videos = json.loads((DATA / "videos_raw.json").read_text())
    channels = json.loads((DATA / "channels_raw.json").read_text())
    br = json.loads((DATA / "breakout_uploads_raw.json").read_text())

    df_all = to_df(videos)
    df_all = df_all[df_all.published >= WINDOW_START]
    out = {"collected_videos": len(df_all), "made_for_kids": int(df_all.mfk.sum())}
    df = df_all[df_all.mfk].copy()
    df["spanish"] = df.apply(is_spanish, axis=1)
    out["mfk_spanish"] = int(df.spanish.sum())
    out["mfk_lang_breakdown"] = df.audio_lang.replace("", "(none)").value_counts().head(10).to_dict()
    df = df[df.spanish].copy()
    df["bucket"] = df.duration_s.apply(bucket)
    df["like_rate"] = df.likes / df.views.where(df.views > 0)
    df.to_csv(DATA / "kids_es_videos.csv", index=False)

    # 1. Top performers
    top = df.sort_values("views", ascending=False).head(100)
    out["top100"] = top[["title", "channel", "views", "duration_s", "published", "views_per_day"]].assign(
        published=lambda x: x.published.dt.date.astype(str)).to_dict("records")
    out["top100_summary"] = dict(
        median_views=float(top.views.median()), min_views=int(top.views.min()), max_views=int(top.views.max()),
        median_duration_min=float(top.duration_s.median() / 60),
        distinct_channels=int(top.channel_id.nunique()),
        top5_channels_share_of_views=float(top.groupby("channel").views.sum().nlargest(5).sum() / top.views.sum()),
        top_channels=top.groupby("channel").views.agg(["count", "sum"]).sort_values("sum", ascending=False).head(15).reset_index().to_dict("records"),
    )

    # 2. Duration
    g = df.groupby("bucket")
    dur = pd.DataFrame(dict(videos=g.size(), share_videos=g.size() / len(df), share_views=g.views.sum() / df.views.sum(),
                            median_views=g.views.median(), median_vpd=g.views_per_day.median(),
                            median_like_rate=g.like_rate.median()))
    order = [b[2] for b in BUCKETS]
    dur = dur.reindex([o for o in order if o in dur.index])
    out["duration"] = dur.reset_index().to_dict("records")
    t100 = df.nlargest(100, "views").bucket.value_counts()
    out["duration_top100"] = t100.reindex([o for o in order if o in t100.index]).to_dict()

    # 3. Themes + words
    out["themes_all"] = theme_table(df).to_dict("records")
    broad = df[df.sources.apply(lambda s: any(x.startswith(("broad:", "noq:")) for x in s))]
    out["themes_broad_only"] = theme_table(broad).to_dict("records")
    out["broad_only_n"] = len(broad)
    out["themes_top100"] = theme_table(df.nlargest(100, "views")).to_dict("records")
    wl = word_lift(df)
    out["title_words_top"] = wl.head(40).to_dict("records")
    out["title_words_high_lift"] = wl[wl.n >= 15].sort_values("lift", ascending=False).head(20).to_dict("records")
    out["tag_words_top"] = word_lift(df, "tags").head(30).to_dict("records")
    out["videos_with_tags_share"] = float((df.tags.str.len() > 0).mean())

    # 4. Channels
    ch = pd.DataFrame([dict(id=c["id"], title=c["snippet"]["title"], created=parse_t(c["snippet"]["publishedAt"]),
                            country=c["snippet"].get("country"), subs=int(c["statistics"].get("subscriberCount", 0)),
                            total_views=int(c["statistics"].get("viewCount", 0)), video_count=int(c["statistics"].get("videoCount", 0)))
                       for c in channels])
    ch["age_days"] = (TODAY - ch.created).dt.days.clip(lower=1)
    ch["views_per_day_lifetime"] = ch.total_views / ch.age_days
    pool_views = df.groupby("channel_id").views.sum()
    ch["views_in_sample"] = ch.id.map(pool_views).fillna(0)
    es_ids = set(df.channel_id)
    ch = ch[ch.id.isin(es_ids)]
    out["channels_n"] = len(ch)
    out["channel_country"] = ch.country.fillna("(none)").value_counts().head(12).to_dict()
    out["channel_created_year"] = ch.created.dt.year.value_counts().sort_index().to_dict()
    out["views_share_by_channel_age"] = {
        "created ≤2018": float(ch[ch.created.dt.year <= 2018].views_in_sample.sum() / ch.views_in_sample.sum()),
        "2019–2022": float(ch[ch.created.dt.year.between(2019, 2022)].views_in_sample.sum() / ch.views_in_sample.sum()),
        "2023+": float(ch[ch.created.dt.year >= 2023].views_in_sample.sum() / ch.views_in_sample.sum()),
    }
    out["channels_top_by_sample_views"] = ch.nlargest(20, "views_in_sample")[["title", "created", "country", "subs", "total_views", "video_count"]].assign(
        created=lambda x: x.created.dt.date.astype(str)).to_dict("records")

    bo = ch[ch.created >= BREAKOUT_SINCE].sort_values("total_views", ascending=False)
    upv = to_df(br["videos"]) if br["videos"] else pd.DataFrame()
    rows = []
    for _, c in bo.head(15).iterrows():
        vids = upv[upv.channel_id == c.id] if len(upv) else upv
        r = dict(title=c.title, created=str(c.created.date()), country=c.country, subs=c.subs, total_views=c.total_views,
                 video_count=c.video_count, views_per_day_lifetime=c.views_per_day_lifetime)
        if len(vids):
            span = (vids.published.max() - vids.published.min()).days or 1
            r.update(recent_uploads=len(vids), uploads_per_week=len(vids) / span * 7,
                     median_duration_min=float(vids.duration_s.median() / 60),
                     share_shorts=float((vids.duration_s <= 60).mean()),
                     median_views_recent=float(vids.views.median()),
                     best_titles=vids.nlargest(3, "views").title.tolist())
        rows.append(r)
    out["breakout_channels"] = rows
    out["breakout_count"] = len(bo)
    out["breakout_over_100M_views"] = int((bo.total_views >= 1e8).sum())

    # Extra parameters
    out["extras"] = dict(
        shorts_share_videos=float((df.duration_s <= 60).mean()),
        shorts_share_views=float(df[df.duration_s <= 60].views.sum() / df.views.sum()),
        comments_disabled_share=float(df.comments.isna().mean()),
        median_like_rate=float(df.like_rate.median()),
        title_emoji_share_top100=float(df.nlargest(100, "views").title_has_emoji.mean()),
        title_emoji_share_all=float(df.title_has_emoji.mean()),
        median_title_len_top100=float(df.nlargest(100, "views").title_len.median()),
        median_title_len_all=float(df.title_len.median()),
        hd_share=float((df.definition == "hd").mean()),
        weekday_top100=df.nlargest(100, "views").weekday.value_counts().to_dict(),
        publish_hour_utc_top100=df.nlargest(100, "views").hour_utc.value_counts().sort_index().to_dict(),
        category=df.category.value_counts().to_dict(),
        views_by_publish_quarter=df.groupby(df.published.dt.to_period("Q").astype(str)).views.agg(["count", "median"]).reset_index().to_dict("records"),
    )
    (DATA / "analysis.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("collected_videos", "made_for_kids", "mfk_spanish", "channels_n", "breakout_count")}, ensure_ascii=False))


if __name__ == "__main__":
    {"collect": collect, "analyze": analyze}[sys.argv[1] if len(sys.argv) > 1 else "analyze"]()
