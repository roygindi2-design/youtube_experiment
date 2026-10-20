"""Market analyst: what is breaking out in Spanish toddler Shorts right now, by format. Writes a Hebrew-labelled report.

    python research/market_scan.py [days=14]

Runs research/recent_shorts.py (YouTube Data API, ~1,000 quota units), keeps Made-for-Kids Shorts, tags each one with
formats (colores, gigante/sorpresa, pregunta, dónde-está, animales, hábito, canción, juego), and ranks formats by median
views/day. Output: research/market/<UTC date>.md + .json, and research/market/latest.md.
Use it before writing each video's dossier (production/dossiers/<id>.md): the 3 reasons must cite these numbers.
"""
import datetime as dt
import json
import re
import statistics as st
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "market"
DAYS = sys.argv[1] if len(sys.argv) > 1 else "14"

FORMATS = {
    "colores": r"color",
    "gigante/sorpresa": r"gigante|sorpresa|m[aá]gic|misterio",
    "pregunta (¿)": r"¿",
    "dónde está / escondite": r"d[oó]nde est|escond|cuc[uú]|peek",
    "animales": r"animal|perr|gat|vaca|pollit|elefant|pat[oi]|dinosaur|tibur",
    "hábito": r"diente|manos|ba[nñ]o|dormir|comer|limpi|orden",
    "canción": r"canci[oó]n|canciones|cantar",
    "juego / reto": r"juego|jugar|reto|desaf|adivina|encuentra|puedes",
    "comida": r"helado|fruta|comida|jugo|pastel|dulce|caramel",
}


def main():
    raw = subprocess.run([sys.executable, str(ROOT / "recent_shorts.py"), DAYS], capture_output=True, text=True, check=True).stdout
    vids = [v for v in json.loads(raw) if v["mfk"]]
    now = dt.datetime.now(dt.timezone.utc)
    rows = []
    for name, pat in FORMATS.items():
        hit = [v["views_per_day"] for v in vids if re.search(pat, v["title"], re.I)]
        miss = [v["views_per_day"] for v in vids if not re.search(pat, v["title"], re.I)]
        if hit and miss:
            rows.append((name, len(hit), round(st.median(hit)), round(st.median(miss)), round(st.median(hit) / max(1, st.median(miss)), 2)))
    rows.sort(key=lambda r: -r[4])
    dur = {}
    for a, b in [(0, 20), (20, 30), (30, 45), (45, 62)]:
        g = [v["views_per_day"] for v in vids if a <= v["duration_s"] < b]
        if g:
            dur[f"{a}-{b}s"] = (len(g), round(st.median(g)))
    top = vids[:15]
    md = [f"# סריקת שוק — Shorts לפעוטות בספרדית ({now:%Y-%m-%d %H:%M} UTC, {DAYS} ימים אחרונים)", "",
          f"{len(vids)} Shorts מסומנים Made for Kids. מדד: צפיות ליום (views/age).", "",
          "## פורמטים: חציון צפיות ליום עם/בלי", "", "| פורמט | n | עם | בלי | יחס |", "|---|---|---|---|---|"]
    md += [f"| {r[0]} | {r[1]} | {r[2]:,} | {r[3]:,} | ×{r[4]} |" for r in rows]
    md += ["", "## אורך", "", "| אורך | n | חציון צפיות ליום |", "|---|---|---|"]
    md += [f"| {k} | {n} | {m:,} |" for k, (n, m) in dur.items()]
    md += ["", "## 15 המובילים עכשיו", "", "| צפיות ליום | אורך | ערוץ | כותרת |", "|---|---|---|---|"]
    md += [f"| {v['views_per_day']:,} | {v['duration_s']}s | {v['channel'][:24]} | {v['title'][:90].replace('|', '/')} |" for v in top]
    md += ["", "_הערה: מתאם, לא סיבתיות. ערוץ אחד חזק יכול להטות פורמט שלם — בודקים את רשימת המובילים לפני מסקנה._"]
    OUT.mkdir(exist_ok=True)
    stamp = now.strftime("%Y-%m-%d")
    (OUT / f"{stamp}.md").write_text("\n".join(md) + "\n")
    (OUT / "latest.md").write_text("\n".join(md) + "\n")
    (OUT / f"{stamp}.json").write_text(json.dumps({"formats": rows, "duration": dur, "videos": vids}, ensure_ascii=False, indent=1))
    print("\n".join(md[:20]))


if __name__ == "__main__":
    main()
