"""Check an episode spec against research/EPISODE_TEMPLATE.md. Exit 1 on any error.
    python3 research/template_check.py production/episodes/<id>/spec.json
"""
import json, re, sys
s = json.load(open(sys.argv[1])); E = []; W = []
shots = {x[0]: x for x in s["shots"]}; seq = s.get("sequence", [])
sec = []; cur = None
for l in s["lyrics"].splitlines():
    if l.startswith("["): cur = l.strip("[]")
    elif l.strip(): sec.append((cur, l.strip()))
if s.get("orientation") != "landscape": E.append("orientation must be landscape (long episode)")
if not 140 <= s.get("song_seconds", 0) <= 160: E.append("song_seconds must be 140–160")
if len(sec) != 28: E.append(f"lyrics must have 28 sung lines (found {len(sec)})")
names = [c for c, _ in sec]
if [n for n in dict.fromkeys(names)] != ["Intro", "Verse 1", "Chorus", "Verse 2", "Verse 3", "Outro"]: E.append(f"sections order wrong: {list(dict.fromkeys(names))}")
ch = [l for c, l in sec if c == "Chorus"]
if len(ch) != 12 or not (ch[0:4] == ch[4:8] == ch[8:12]): E.append("chorus must be the same 4 lines x3")
if len(seq) != 28: E.append(f"sequence must have 28 entries (found {len(seq)})")
if set(shots) - set(seq): E.append(f"shots not used in sequence: {sorted(set(shots) - set(seq))}")
if set(seq) - set(shots): E.append(f"sequence uses unknown shots: {sorted(set(seq) - set(shots))}")
if len(seq) == 28:
    chs = [seq[i:i + 4] for i in (6, 14, 22)]
    if not (chs[0] == chs[1] == chs[2]): E.append(f"chorus shots must be identical x3: {chs}")
    if seq[3] != seq[11]: E.append("question shot (line 2 of verses 1–2) must be the same shot")
    for a, b in zip(seq, seq[1:]):
        if a == b: E.append(f"same shot twice in a row: {a}")
wide = [k for k, x in shots.items() if x[1].lower().startswith("wide")]
if wide != [seq[0]] if seq else True: W.append(f"only the first shot should start with 'Wide' (found {wide})")
for k, x in shots.items():
    f, m = x[1], x[2]; fl = f.lower()
    if "CENTER of the frame" not in f: E.append(f"{k}: frame must end with the CENTER rule")
    if re.search(r"\b(laugh|laughing|laughs|grin|teeth)\b", fl) and "closed" not in fl: E.append(f"{k}: no laughing/grin/teeth")
    hand_only = "hand" in fl and "face" not in fl and "eyes" not in fl and not fl.startswith("medium")
    if not hand_only and ("close-up" in fl or "medium" in fl) and ("baby elephant" in fl or "mamá" in fl or "kitten" in fl or "bat" in fl or "mouse" in fl) \
       and "Both eyes stay open" not in m and not re.search(r"eyes (closed|slowly close|close)", fl + m.lower()): E.append(f"{k}: motion needs the stable-eyes sentence")
    if "baby elephant" in fl and "trunk" not in fl and "hand" not in fl: W.append(f"{k}: say where Tito's trunk is")
    if re.search(r"in his trunk|with his trunk", fl) and re.search(r"\bhand", fl): E.append(f"{k}: object held by trunk AND hand")
    if re.search(r"splash(es|ing)? (flying|up around)|frozen", fl): E.append(f"{k}: frozen splash in frame")
    if not ("START" in m and "ACTION" in m and "END" in m): E.append(f"{k}: motion must be written as START → ACTION → END (research/17-motion-and-acting.md)")
    if re.search(r"\byawn", m.lower()) and "no yawn" not in m.lower(): E.append(f"{k}: no open-mouth yawn (use SLEEPY face)")
    if re.search(r"\b(bites|eats|takes a bite|swallows)\b", m.lower()): E.append(f"{k}: eating inside a shot (object vanishes) — split into 2 shots")
for k in (seq[2], seq[10]) if len(seq) > 10 else ():
    if re.search(r"\b(reveal|is a|it is)\b", shots[k][1].lower()): W.append(f"{k}: clue shot may reveal the answer")
import os
sp = os.path.join(os.path.dirname(sys.argv[1]), "SCRIPT.md")
if os.path.exists(sp):
    t = open(sp).read()
    for h in ("## Design bible", "## Habit beat"):
        if h not in t: E.append(f"SCRIPT.md missing section '{h}' (research/16-design-and-habits.md)")
    for sub in ("Environment", "Palette", "Costume", "Supporting", "Background life", "Hero props"):
        if "## Design bible" in t and sub.lower() not in t.split("## Design bible")[1][:6000].lower(): E.append(f"Design bible missing '{sub}'")
for w in W: print("⚠", w)
for e in E: print("✗", e)
print("TEMPLATE OK" if not E else f"TEMPLATE FAILED ({len(E)})"); sys.exit(1 if E else 0)
