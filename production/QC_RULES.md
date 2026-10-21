# כללי QC לווידאו (מחייבים מ-19.10.2026)

נכתבו אחרי גליץ' ב-Short הרשמי של טיטו: בקליפ T4 הופיעו כפילות רפאים, עין שלישית ואוזן כפולה.

1. **רק חיתוכים חדים (Hard Cut) בין שוטים.**
   - אסור Crossfade, Dissolve או Morph.
   - `production/assemble.py` מחבר קליפים ב-concat בלבד.
2. **קליפ אחד = פריים פתיחה אחד.**
   - Wan 2.2 מקבל `image_start` בלבד.
   - אסור לתת לו פריים סיום עם זווית ראש אחרת, כדי שלא ימזג שני פריימים.
3. **תנועה עדינה.**
   - הפרומפט מסתיים ב: "Small, calm, smooth movements; the character's head stays steady… no fast motion, no camera zoom, no morphing".
   - תנועה מהירה (דחיפה, ריצה, סיבוב) היא הגורם העיקרי לגליצ'ים.
4. **שני Seeds לכל שוט**, ובחירה של הנקי מביניהם.
5. **בדיקה אוטומטית** (`production/qc_clips.py`):
   - שגיאת עיוות זרימה (optical flow) לכל פריים.
   - דמיון זהות (DINOv2) לפריים הראשון. סף 0.85.
6. **בדיקה ויזואלית חובה, גם כשהבדיקה האוטומטית עוברת.**
   - שלושת הפריימים הרחוקים ביותר מהדמות בכל קליפ.
   - דף פריימים צפוף (4–10 פריימים לשנייה, חיתוך על הראש) של הסרטון הסופי.
   - הבדיקה האוטומטית לבדה פספסה את T4.
7. **אם יש גליץ' בקליפ:**
   - **עדיף:** ייצור מחדש של השוט.
   - **תיקון זמני:** להשתמש רק בחלק הנקי (`until`), ואז להקפיא את הפריים הנקי האחרון עם זום איטי (`hold_speed`).
8. **אין העלאה בלי מעבר בסעיפים 5 ו-6.**
   - אם מתגלה גליץ' בסרטון שכבר פורסם: מעלים גרסה מתוקנת, והפגומה עוברת ל-Unlisted. לא מוחקים.

## לקחים מ-Short 2 (גרביים), 2026-10-19
- **פריים 0 של כל קליפ** הוא פריים המפתח הגולמי, והוא בהיר יותר מהשאר. בחיתוך חד הוא נראה כהבזק. כלי ההרכבה מדלגים עליו תמיד (`SKIP = 0.06`).
- **חפצים שנעלמים** (גרביים נעלמים מהידיים) הם גליץ' בדיוק כמו עין שלישית. משתמשים רק בחלק שלפני ההיעלמות (`until`) או בחלק שאחריו, כשהחפץ כבר לא בתמונה (`in`).
- **שינוי גוף** (האוברול נעלם, החדק הופך לקרן) פוסל את הקליפ מיד, גם אם הפנים נשארות דומות. ה-QC האוטומטי לבד לא מספיק, וחובה לבדוק את כל הגוף בדף הפריימים.
- **שורה ארוכה מ-4 שניות**: מפצלים אותה לשני שוטים (`--plan 5a/5b`) במקום להקפיא, ומשתמשים ב-seed השני של שוט אחר.
- **שוט שנכשל בשני ה-seeds**: מחליפים בשוט נקי אחר שמתאים לשורה. רק אם אין כזה, מייצרים מחדש.

## לקחים מכתיבת פרומפטים (20.10, ספרינט)
- **בלי שלילות בפרומפט.** "no faces and no eyes" הוסיף עיניים לכדורי הגלידה, כי המודל נתפס למילים. כותבים רק מה כן רוצים: "plain smooth ice cream, like real ice cream in a shop".
- **מקום פתוח לא קוראים "room".** "the room from the first reference image" החזיר את הפריימים לתוך חדר, גם כשתמונת העולם הייתה חוף. בפריים מתארים את המקום במפורש: "outdoors on a sunny beach…, wide open blue sky".
- **מסתכלים על תמונת העולם ועל פריימי המפתח לפני הקליפים.** בעיה בפריים מפתח עוברת לכל הקליפים שנבנים ממנו.

## לקחים מ-tito_manos (20.10)
- **תקריבים ב-FastWan:** בחצי השנייה הראשונה יש "קפיצה" מה-keyframe לתנועה (QC מסמן דמיון 0.80–0.83). פתרון: `--extra 'SHOT@seed={"in":0.5}'`. נבדק ויזואלית.
- **שוט רחב עם שתי דמויות ליד כיור/רהיט:** טיטו יוצא קטן ונראה "בתוך" הכיור. לפעולות ידיים כותבים תקריב בגובה החזה ("camera very close … at chest height").
- **"Paint swirls down the drain"** בשוט רחב = צבע נשפך לרצפה. בתקריב עם "swirls into the white sink basin" יצא מערבולת קשת יפה בכיור.
- **pkill -f עם תבנית שמופיעה בפקודה עצמה הורג את ה-shell.** לולאות המתנה לא מחפשות `pgrep -f qc_clips.py` (מתאים לעצמן).

## לקח מרכזי מ-Roy (20.10 22:40): "לא קורה כלום, אותה תמונה, רק זז לצדדים"
- **הסיבה:** תמונת המיקום שימשה כ-ref בכל keyframe → המודל העתיק את אותה זווית מצלמה לכל השוטים. הפעולה (גלגלים נופלים/מתחלפים) נכתבה במילים אבל לא נראתה בתמונה.
- **"מצב במאי" (`"director": true` ב-spec):** ref של המיקום רק לשוט רחב פותח; בשאר השוטים זווית מצלמה מפורשת בטקסט (מהצד, מלמעלה, מאחור, תקריב קיצוני על פרט). התיאור של השוט ראשון בפרומפט. 2 seeds ל-keyframe.
- **שלב חובה — סטוריבורד:** לפני קליפים מסתכלים על כל ה-keyframes בשורה. כל פריים חייב להראות שינוי מצב שרואים בלי סאונד (צבע אחר, בוץ↔נקי, מים, חפץ חדש), ואין שני פריימים רצופים באותה זווית+גודל. אם אין — כותבים מחדש לפני שמוציאים כסף על קליפים.
- **מצב משתנה כתוב בפריים עצמו בהדגשה:** "now completely BRIGHT BLUE all over" — עבד (בגרסה 1 הרכב נשאר אדום).

## Liquids and physics (Roy 21.10: "the bath and the puddle look like a still picture")
- **Never put a splash in the keyframe.** A frozen splash in the start image stays frozen like a sculpture for the whole clip. The keyframe shows the moment BEFORE (in the air above a calm puddle / hands raised over the water); the motion prompt makes the splash happen: "splashes up in droplets that arc and fall back down", "ripple rings spread across the surface", "foam wobbles and sloshes".
- **Water must flow from a source:** hand washing = at the sink with a stream of water from the tap, not a pile of foam on a table.
- **Bath = no clothes.** In bath shots replace the overalls from the lock with "bare powder-blue skin, his overalls hang on a hook on the wall".
- **A static closing shot (sleeping) needs life:** breathing blanket, head turning, moon blinking, stars twinkling.
- **New QC check:** after QC, look at 4 frames (0.2/1.2/2.2/3.2 s) of every water/foam/mud shot — if the liquid has the same shape in all 4, that's FAIL.

## Physics/trunk review sheet (Roy 21.10: "check trunk, water, liquids and physics thoroughly")
- Tool: `python production/qc_physics_sheet.py <video> <out_prefix> 0.5 10` → a frame every 0.5 s with a timestamp. Mandatory for every final video and every video that goes into a compilation.
- Check every frame for:
  1. **Trunk** — Tito AND Mamá: the trunk is present and keeps its length (Mamá has a long trunk; a "human" face = FAIL).
  2. **Liquids** — moving (drops fall, ripples, foam wobbles), with a visible source (tap / carton), not a frozen column.
  3. **Gravity** — nothing floats without support (a block above the head, a carton beside the bin).
  4. **Bath** — no clothes.
  5. **Mirror / reflection** — the reflection is the same character.
- Found in the review of 21.10 (already-published Shorts): bano (bath in overalls), manos (foam with no water), mesa (Mamá without a trunk, pasta column to the floor), halloween (Mamá without a trunk, trunk merged into the pumpkin, different reflection), torre (floating block).

## Square frames in a 16:9 episode (21.10, ep3)
- Klein 4B with character references (KI) ignores `resolution` and returns 960x960 → the clip comes out 736x736, and the 16:9 crop cuts 44% of the height (in ep3 the giraffe's head and Tito disappeared from the Hook).
- **Mandatory check after keyframes:** `ffprobe` on every pick; if it's not 1280x720, choose per shot `crop_y` (crop window) or `fit` (whole frame + blurred sides) in the cut list. Same check for ep2 (it was square too).

## Eyes and faces (Roy 21.10 at night: "eyes that jump, a giraffe with odd eyes, Tito's eye visible through the trunk")
- **Mandatory before QC sign-off:** `python3 research/glitch_scan.py <edit.json> <out> 24` + review of the top 18 events. A one-frame blink/wink in a close-up = cut before it or use a different take.
- When choosing a take: run glitch_scan on all candidates (fake edit.json with every clip), pick the lowest max(rel), then eye review.
- Prompts: front-on face, small movements, "his eyes stay closed the whole time" for sleep, "a soft sweet smile with his mouth closed" (no open laughing), no big head turns (the trunk crosses the eye).
- Toys: a plush toy = "two tiny round black button eyes sewn on" (stable). A toy vehicle that isn't a character = "no face". A lamp keeps coming out with eyes in Klein — accept it as a cute object, or use a different seed.
- Character in a 16:9 frame: the 16:9 location image as the first ref → Klein returns 1280x720 (without it, it returns a square).
