# התבנית המדויקת של פרק Cantilandia (מה שהוגדר עם Roy, 21–22.10.2026)
**כל פרק חייב לעבור את `python3 research/template_check.py production/episodes/<id>/spec.json` (0 שגיאות) ואת `production/preflight.py produce`.**

## א. מבנה
1. **פרק ארוך 16:9** (`orientation: landscape`): שיר-סיפור חדש ~2:30 (`song_seconds` 140–160, `bpm` 104–112) + "más canciones" (קומפילציה) → 8–12 דק', ובהמשך 20+.
2. **השיר:** Intro (2 שורות) → 3 בתים × 4 שורות → אותו פזמון × 3 (4 שורות זהות) → Outro (2 שורות) = **28 שורות**.
3. **כל בית = תעלומה עצמאית:** שורה 1 רמז (שוט שמראה רק את הרמז) → שורה 2 שאלה לצופה (אותו שוט "Q" בבתים 1–2) → שורה 3 חשיפה + מילת צליל → שורה 4 תגמול שרואים.
4. **בית 3 = הצמיחה או המוסר** (הדמות עושה לבד / משתפת) — מגשים את שורת הפזמון.
5. **הפזמון = אותם 4 שוטים בכל פעם** (טקס שהילד צופה מראש ומחקה): תנועה + נימוס/רגש + המסר + המשך.
6. **`sequence`** = 28 מזהי שוטים, ו**כל שוט ב-`shots` מופיע ב-sequence**.

## ב. כללי שוט (QC_CHECKLIST)
- כל frame מתחיל בזווית וגודל מפורשים; אין שני שוטים רצופים באותה זווית וגודל; רק השוט הראשון מתחיל ב-"Wide".
- כל frame נגמר ב-"The main action is in the CENTER of the frame."
- כל motion עם דמות בתקריב או מדיום: "Both eyes stay open and calm with the same gentle expression the whole time."
- טיטו: "his trunk curled down below his mouth"; תחפושת או בגדים מתוארים בכל שוט.
- חפץ מוחזק: ביד אחת מפורשת **או** בחדק, לא שניהם; לא מול הפנים; אכילה או העברה = נופל מלמעלה או שני שוטים — אף פעם לא נעלם.
- אסור: "laughing", "big grin", "teeth", splash קפוא ב-frame, פרצוף על אוכל או חפץ (חוץ מדלעות Halloween).
- שוט הרמז (שורה 1) ושוט השאלה לא מראים את התשובה.

## ג. מסר וסנכרון
- מסר אחד או שניים, מודגמים בתמונה, אחד מהם בפזמון. מילת צליל על השיא הוויזואלי. חיתוך אחד לשורה, אף חיתוך מתחת ל-0.5 ש'.

## ד. פרסום (חלק מה-Linear לפני In Review)
- כותרת פרק = השאלה + "+ Más Canciones Infantiles"; תיאור: שאלה, סיפור, פרקים (timestamps), מילים מלאות.
- 3 Shorts — "פותרים אחד, פותחים את הבא"; כותרת = שאלה + #shorts; תיאור: שאלה + "▶️ Capítulo completo: <link>".
- TikTok: אותו Short, כיתוב להורים, האשטגים, קישור ליוטיוב, תווית AI.
- תמונה ממוזערת: הרמז הכי מסקרן (צל / דלת סגורה) + פנים של טיטו.

## Motion rules (22.10)
- No ping-pong/boomerang. Lines longer than a clean take → second seed, another angle, or 0.85–0.9x speed.
- Walking shots: "camera slowly tracking backwards as he walks, houses passing by" or walking across the frame.
- Holds ≤ 2 s; every shot has gentle motion.
- Movement choice per line: going somewhere → real walk (tracking camera / crossing the frame); staying → joy action (jump, clap, bounce, dance). Never a walk cycle in place.
- Every shot description must pass QC_CHECKLIST §7 (logic & physics) before it goes to the producer.

## ה. Design bible + Habit beat (Roy 22.10 — required, see research/16-design-and-habits.md)
Every SCRIPT.md must have, BEFORE the timeline:
- `## Design bible`, with: Environment (8–12 set items per location), Palette & light, Costumes (fit the moment), Supporting characters (design sheet), Background life (2–3 per location), Hero props.
- `## Habit beat`: one small good-habit moment (1 shot or 1 prop action), rotated: handwashing / teeth / gracias / sharing / tidying / water.
The set items and costumes must also appear in spec.json (locations + shot frames + lock/continuity), not only in the SCRIPT.

## ו. Acting (Roy 22.10 — research/17-motion-and-acting.md)
- Every shot's motion = START pose → ACTION (on which beat) → END pose; + secondary motion; + what stays still. Use the named moves (TUUU, HAPPY BOUNCE, SWAY, CLAP-CLAP, FREEZE, JUMP FOR JOY, NO-NO, THUMBS-UP, PEEKABOO, REAL WALK…) and faces (HAPPY SQUINT, SURPRISE O, CURIOUS, PROUD, SLEEPY…).
- Chorus = one signature dance (4 named moves, one per line) ×3. Each verse: ≥1 big-body moment + ≥1 meaning gesture.
- One main action per 5 s clip. No open-mouth laugh/yawn.

## ז. Music ↔ picture sync (Roy 22.10 — research/sync_check.py)
- Every cut lands ON a beat (song bpm grid; ±0.1 s). Goal ≥80% of cuts (v7 was 40% = random).
- Each shot's main action peak (knock, trunk up, bow, landing, wave) lands on a beat, ideally the sound-word beat (¡toc! ¡Miau! ¡Flap! ¡Tuuu! ¡Toma!).
- In the script, every shot's ACTION names its beat ("on beat 1 of the line", "on ¡toc!"). The editor slides the in-point inside the clean window to hit it.
- Run `python3 research/sync_check.py <mp4> <bpm>` before sending a review copy.

## ח. Life, story and hidden values (Roy 23.10)
- Every shot has background life written in the motion ("Background life: …"): animals, leaves, water, lanterns… The environment is never static. Roy: "the moving environment looks amazing".
- 1–2 environment characters (a toucan, a monkey, birds…) react or copy the dance in cutaways (spec field `cutaways`, listed with where they go in the edit).
- Each verse: Tito moves more, with a big-body move + a meaning gesture (move library).
- One HIDDEN value per episode, shown and never preached: caring for nature (clean up, don't pick flowers, water a plant) or helping others (share, help a friend). It sits in an action, not in the lyrics.
- The key emotional moment (sharing / helping) gets its own 3–4 shot mini-scene with BOTH characters whole in frame. Never a floating arm or a hand-only insert for the key moment.
- The same take max 2× in an episode; chorus repeats use the same move with different takes.
- QC: the story check = setup → problem → 3 tries/reveals → punchline/moral visible on screen.

## ט. Deep world + shot bible (Roy 23.10 — required for every new script)
Every SCRIPT.md must also have:
1. **World design — deep:** 2–3 zones of the place (each with props, colors, textures), the light arc (time of day / weather change), the background life list, the supporting characters' looks (a table when there are several, e.g. 4 mushroom types / 4 wheels), and the hero's relation to the place.
2. **Shot bible table:** per shot — face (eyes, eyebrows, mouth), hands/body, environment, why kids watch.
3. **Sequence & punchline:** the event chain in 4–6 steps, the big punchline, and the 3–5 most grabbing moments (thumbnail / Shorts candidates).
Rule: always expand a little — each pass adds detail that makes the video cooler and more professional. The spec.json locations and frames must carry the same details.

## י. Native vertical Short (Roy 23.10 — required)
Verticals are NOT cropped from the 16:9 master (too close, cut characters). Every episode gets one native 9:16 Short (~30–40 s, the strongest story beat, the episode's own audio slice with cuts on the master's beat grid): a separate `production/episodes/<id>_vshort/spec.json` with orientation "portrait", every frame composed for 9:16 (characters whole and large). The same file goes to YouTube Shorts + TikTok. Template: tito_ep4_halloween_vshort.
