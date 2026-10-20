"""Preflight gate: the research and rules that must be done BEFORE a video is produced or uploaded.

    python production/preflight.py produce <spec.json> [<spec.json> ...]   # before any GPU job (rp.py run calls this)
    python production/preflight.py upload  <upload_meta.json>              # before publishing (yt.py upload calls this)

Exit code 0 = pass. Anything missing prints a Hebrew/English reason and blocks.

produce checks (per spec):
  1. Market data is fresh (<= 3 days): research/market/latest.md and outliers_*.json. If stale, runs the scans.
  2. Visual study of winners exists for the latest outliers (research/market/frames_<date>/).
  3. Dossier production/dossiers/<id>.md exists with 3 numbered reasons, and every reason cites data
     (a multiplier like ×4.6 / x7941, or a views/day number) — research-backed, not opinion.
  4. World: spec["world"] is set and differs from the last 4 entries in production/registry.json.
  5. Story-first: spec["story"] has 4-8 beats (problem -> try -> fix -> reward) and lyrics lines >= beats - 1.
  6. Shot variety: at least 2 close-ups, 1 wide shot, and at least 2 different camera framings.
upload checks:
  - dossier exists for the video id, QC sign-off file exists (production/qc/<id>.md with "PASS"),
    meta is madeForKids + has captions + no burned captions flag issues.
Registry: production/registry.json lists published videos {id, spec, world, youtube_id, date}. Updated after upload.
"""
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "research" / "market"
REG = ROOT / "production" / "registry.json"
FAIL = []


def fail(msg):
    FAIL.append(msg)
    print("✗", msg)


def ok(msg):
    print("✓", msg)


def age_days(p):
    return (dt.datetime.now().timestamp() - p.stat().st_mtime) / 86400


def market_fresh():
    latest = MARKET / "latest.md"
    outs = sorted(MARKET.glob("outliers_*.json"))
    if not latest.exists() or age_days(latest) > 3:
        print("… market scan is stale, running research/market_scan.py")
        subprocess.run([sys.executable, str(ROOT / "research" / "market_scan.py"), "14"], check=False, capture_output=True)
    if not outs or age_days(outs[-1]) > 3:
        print("… outlier scan is stale, running research/outlier_scan.py")
        subprocess.run([sys.executable, str(ROOT / "research" / "outlier_scan.py"), "60"], check=False, capture_output=True)
        outs = sorted(MARKET.glob("outliers_*.json"))
    if (MARKET / "latest.md").exists() and age_days(MARKET / "latest.md") <= 3:
        ok("market scan fresh")
    else:
        fail("market scan missing/stale (research/market_scan.py)")
    if outs and age_days(outs[-1]) <= 3:
        ok(f"outlier scan fresh ({outs[-1].name})")
    else:
        fail("outlier scan missing/stale (research/outlier_scan.py)")
    frames = sorted(MARKET.glob("frames_*"))
    if frames and age_days(frames[-1]) <= 3 and list(frames[-1].glob("sheet_*.jpg")):
        ok(f"visual study of winners exists ({frames[-1].name}) — review it before writing the script")
    else:
        print("… running research/watch_frames.py (visual study sheets)")
        subprocess.run([sys.executable, str(ROOT / "research" / "watch_frames.py")], check=False, capture_output=True)
        frames = sorted(MARKET.glob("frames_*"))
        (ok if frames else fail)("visual study sheets " + ("created: review them" if frames else "missing (research/watch_frames.py)"))


def dossier(vid):
    n0 = len(FAIL)
    p = ROOT / "production" / "dossiers" / f"{vid}.md"
    if not p.exists():
        return fail(f"{vid}: dossier missing ({p.relative_to(ROOT)}) — write 3 data-backed reasons first")
    t = p.read_text()
    reasons = re.findall(r"^\s*(\d)\.\s+(.+?)(?=^\s*\d\.\s|^##|\Z)", t, re.M | re.S)
    if len(reasons) < 3:
        return fail(f"{vid}: dossier needs 3 numbered reasons (found {len(reasons)})")
    for num, body in reasons[:3]:
        if not re.search(r"[×x]\s?\d|\d[\d,.]*\s?(?:מיליון|אלף|k|K|M)|\d{3,}", body):
            fail(f"{vid}: reason {num} cites no number from the research (outlier ×, views/day)")
    if len(FAIL) == n0:
        ok(f"{vid}: dossier with 3 data-backed reasons")


def registry():
    return json.loads(REG.read_text()) if REG.exists() else []


def produce(specs):
    market_fresh()
    recent_worlds = [r.get("world") for r in registry()[-4:]]
    for f in specs:
        s = json.loads(Path(f).read_text())
        vid = s["id"]
        dossier(vid)
        w = s.get("world")
        if not w:
            fail(f"{vid}: spec has no 'world' (production/WORLDS.md)")
        elif w in recent_worlds:
            fail(f"{vid}: world '{w}' was used in the last 4 videos")
        else:
            ok(f"{vid}: world '{w[:60]}' is new")
        story = s.get("story") or []
        lines = [l for l in s.get("lyrics", "").splitlines() if l.strip() and not l.startswith("[")]
        if not 4 <= len(story) <= 8:
            fail(f"{vid}: 'story' needs 4-8 beats (problem -> try -> fix -> reward), found {len(story)}")
        elif len(lines) < len(story) - 1:
            fail(f"{vid}: lyrics ({len(lines)} lines) don't cover the story beats ({len(story)})")
        else:
            ok(f"{vid}: story-first ({len(story)} beats, {len(lines)} lyric lines)")
        # story rules (research/09-story-patterns.md, Roy 20.10: plot + punchline, a new experiment every video)
        patterns = ("trick_why", "lesson_consequence", "guess_interactive", "rescue_mission", "mystery", "overcome_fear")
        if s.get("pattern") not in patterns:
            fail(f"{vid}: 'pattern' must be one of {patterns}")
        for k in ("moral", "twist", "opening", "experiment", "continuity"):
            if not s.get(k):
                fail(f"{vid}: missing '{k}' (research/09-story-patterns.md)")
        recent_open = [r.get("opening") for r in registry()[-3:]]
        if s.get("opening") and s["opening"] in recent_open:
            fail(f"{vid}: opening '{s['opening']}' was used in the last 3 videos — try something new")
        frames = [(x[1] if isinstance(x, (list, tuple)) else x.get("frame", "")).lower() for x in s.get("shots", [])]
        close = sum(("close-up" in f or "close up" in f) for f in frames)
        wide = sum("wide" in f for f in frames)
        kinds = {k for f in frames for k in ("extreme close-up", "close-up", "medium", "wide", "low angle", "over-the-shoulder", "top-down") if k in f}
        if close >= 2 and wide >= 1 and len(kinds) >= 2:
            ok(f"{vid}: shot variety ({close} close-ups, {wide} wide, {len(kinds)} framings)")
        else:
            fail(f"{vid}: shot variety too low ({close} close-ups, {wide} wide, framings {sorted(kinds)})")


def upload(meta_file):
    m = json.loads(Path(meta_file).read_text())
    vid = Path(m["file"]).stem
    dossier(vid)
    qc = ROOT / "production" / "qc" / f"{vid}.md"
    if not qc.exists() or "PASS" not in qc.read_text():
        fail(f"{vid}: QC sign-off missing (production/qc/{vid}.md with PASS after auto + visual review)")
    else:
        ok(f"{vid}: QC sign-off PASS")
    if not m.get("madeForKids", False):
        fail("madeForKids must be true")
    # 2026-10-20 Roy: no captions needed at all (no burned text, no CC track)
    series = json.loads((ROOT / "production/youtube/series.json").read_text()) if (ROOT / "production/youtube/series.json").exists() else {}
    if not m.get("series") or any(k not in series for k in m["series"]):
        fail(f"meta 'series' must list at least one series key from production/youtube/series.json ({', '.join(series)})")
    if not FAIL:
        ok("upload checks passed")


if __name__ == "__main__":
    mode, args = sys.argv[1], sys.argv[2:]
    produce(args) if mode == "produce" else upload(args[0])
    if FAIL:
        print(f"\nPREFLIGHT FAILED ({len(FAIL)}) — fix before {mode}.")
        sys.exit(1)
    print(f"\nPREFLIGHT OK — {mode} allowed.")
