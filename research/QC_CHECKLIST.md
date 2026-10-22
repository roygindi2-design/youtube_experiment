# רשימת בדיקה של החוקר — כל סרטון, פעמיים (keyframes + עריכה סופית)
**כלל:** כל אי-דיוק שרואים = FAIL עם בקשת תיקון (Roy, 21.10). עוברים על כל הרשימה; הכלים: `research/glitch_scan.py` (קפיצות מקומיות) + `production/frame_sheet.py --fps 2` (כל הסרטון) + זום על כל אינטראקציה.

## 1. פנים ועיניים
- עיניים "קופצות": מצמוץ/קריצה של פריים אחד, עין אחת נסגרת, אישונים שמשנים גודל.
- עין שמצוירת מעל החדק או מופיעה דרכו (סדר שכבות שגוי בסיבוב ראש).
- הבעות מעוותות או לא מתאימות לגיל: פה פתוח עם שיניים, עיניים עקומות, פרצוף "מתוח".
- פרצופים על חפצים או אוכל שלא תוכננו (לימונים, מנורה, צלחת).

## 2. גוף ואנטומיה
- **איברים שמתחברים:** יד שמתמזגת לחדק, חדק שמתמזג לחפץ, אצבעות שנעלמות לתוך מזלג.
- מספר אצבעות / ידיים / רגליים / אוזניים / עיניים לא נכון; איבר נוסף או חסר.
- חדק שמשנה אורך או עובי בתוך השוט; גוף שמשנה גודל.
- דמות שמשנה צבע (אמא אפור-לבנדר, טיטו כחול-אבקה, רוחיטו אדום).

## 3. חפצים
- **חפץ שנעלם או "נאכל" בתוך השוט** (צלחת, מזלג, צעצוע) — או מופיע פתאום.
- חפץ שמתמזג ביד או בפנים כשהוא מוחזק מולם (צלחת מול הפנים).
- חפץ שמשנה צורה, גודל או צבע בין פריימים; אוכל שנשאר מלא אחרי שאכלו / מתרוקן בלי סיבה.
- נוזלים קפואים (splash כמו פסל), מים שלא זורמים ממקור.

## 4. המשכיות וסיפור
- קפיצה בין שוטים: במיטה ← עומד, בגדים, מנורה דולקת/כבויה, שעת יום.
- הפואנטה נחשפת לפני הזמן (הינשוף בחלון לפני "¿Qué es eso?").
- השוט לא מראה את מה שהשורה בשיר אומרת באותו רגע (סנכרון).
- דמות כפולה, דמות שנעלמת מהפריים.

## 5. טכני
- חיתוך קצר מ-0.5 ש', פריים שחור/מהבהב בחיתוך, קליפ שקופא.
- טקסט מקושקש, לוגו או סימן מים; כתוביות שלא היו אמורות להיות.
- רקע שמשתנה או "זוחל" בתוך שוט.

## כללי כתיבה שמונעים את זה (לתסריטים שלי)
- **חפץ מוחזק — רק ביד או רק בחדק, ומפורש:** "holds the fork in his right hand, his trunk curled up away from it". לא שניהם יחד.
- **אכילה = שני שוטים:** לפני (מרים לפה) ואחרי (לועס). אף פעם לא "נוגס והחפץ קטן" בתוך שוט אחד.
- חפצים לצד הגוף או מעל הראש — לא מול הפנים.
- עיניים: "Both eyes stay open and calm…"; חיוך עדין עם פה סגור; החדק מתחת לפה בסיבוב ראש.
- בשוט השאלה רק רמז; הפתרון בשוט הבא.

## 6. Motion (added 22.10 after Roy's review — a frame sheet cannot catch these; WATCH the video at 1x and run research/motion_check.py)
- [ ] NO ping-pong/boomerang anywhere (frames going forward then backward = looks stuck).
- [ ] No piece shorter than 1.5 s of the same shot chopped back-to-back (flicker).
- [ ] No frozen hold > 2 s (characters must breathe/move; static prop shots ≤ 2 s).
- [ ] Walking = really travels: street/houses move, or the character crosses the frame. No walking in place.
- [ ] Trunk hangs down below the mouth, never curls onto the cheek/face.
- [ ] Natural slow blink = OK; eye pop/jump/flicker = FAIL.

## 7. Logic & physics — "does this make sense to a 3-year-old?" (Roy 22.10)
Walking vs. in place
- [ ] WALKING / RUNNING = the world changes: houses/street pass by (camera tracks), or he crosses the frame and ends somewhere else. Legs moving while the background stays put = FAIL.
- [ ] Happy/excited on the spot is fine AND preferred for "in place" moments: jumping for joy, clapping, a little dance, bouncing. If the line has no destination, use a joy action, not a walk.
- [ ] Feet touch the ground; no sliding/skating feet; landing after a jump.
Cause → effect
- [ ] Order is logical: knock → (pause) → door opens; door is CLOSED before the knock; candy falls only after it is offered.
- [ ] Gravity: things fall DOWN and stay where they land (candy stays in the bucket), nothing floats.
- [ ] What you hold stays in your hand; nothing passes through bodies, doors, or buckets.
Continuity of state
- [ ] Amounts only change for a reason: bucket empty → some → full; it only goes down when he shares.
- [ ] Same place = same look: the door you knock on = the door that opens; same houses, colors, night, moon.
- [ ] Scale stays the same: mouse smaller than Tito, door sizes fit the characters.
- [ ] Costumes/props are the same from shot to shot (hat, bucket, stem, colors).
Story & feeling
- [ ] What is sung is on screen at that moment (e.g. "toc, toc, toc" = 3 knocks; "¡Flap, flap!" = wings flap).
- [ ] Characters look at what they react to (eye line), and at each other when they talk.
- [ ] The face matches the line: sad when the mouse has no candy, happy when sharing. No worried brows in happy moments.
- [ ] Nobody appears or disappears without a reason (a door, an entrance, a cut to a new place).

## 8. Sync (22.10)
- [ ] research/sync_check.py: cuts on the beat ≥80%; the main action of each shot on a beat; sound words match the picture at that moment.
