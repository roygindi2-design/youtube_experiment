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
