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

## 9. Lesson 22.10 (Roy caught the C1 trunk): check the trunk at ≥5 fps for the WHOLE slot of every Tito shot, especially the dance/chorus shots (they repeat ×3 + in every Short). Never accept "trunk OK" from the producer's note without looking. A hook/S-curl in front of the face = FAIL.

## 10. Story & life (Roy 23.10)
- [ ] Background life in every shot (nothing frozen behind the characters).
- [ ] No floating limbs: an arm/hand entering from the frame edge without a body = FAIL (unless clearly a close-up of a held object with the arm attached to a visible body).
- [ ] Props attached correctly: a bucket/bag is HELD (by a hand/handle), never glued to the body.
- [ ] Repetition: the same take max 2× (count from the cut list); otherwise it feels like a loop, even without ping-pong.
- [ ] Profile/turn shots: both eyes + trunk stay readable; a turn that loses an eye or the trunk = FAIL.
- [ ] Two characters touching: trunks/faces must not merge.
- [ ] The story is readable without sound: setup → problem → reveals → punchline; the moral moment is big and clear.

## 11. Natural actions (Roy 23.10)
- A transfer between characters (candy, food, a toy) is done BY HAND: take it in the hand → give it / put it in. Never pour or tip one container into another, never objects streaming through the air — it reads as fake.
- QC asks for every hand action: "would a real child do it this way?" If not, FAIL — even when the frames are technically clean.
- **Walk direction (Roy 23.10):** a walk must go ONE way. For every walking shot, check the character's size/position at 0.5 s steps (a timestamped strip): toward the camera = it only grows; away = only shrinks; sideways = x only moves one way. Any reversal (forward → back) = slow boomerang = FAIL, even when motion_check reports 0 ping-pong.

## 12. FULL-PASS PROTOCOL (Roy 23.10 — "find ALL the defects")
Misses this week that Roy caught: the candy POUR (unnatural), an eye-roll (Tito VM2), a hop that hung 2.4 s in the air, a bucket that vanished from his hand, a mouse that looked "odd", hands not really held, a walk that went forward then back. Rule from now on: no "PASS" until EVERY item below is done for EVERY second of the video.
1. **Per-character pass at 8 fps, every second** (not samples): one strip per character. For each frame: both eyes (open/closed/rolling up/smeared), mouth, trunk (where, touching what), each hand (holding what, attached to the arm), feet (on the ground?), costume/props present.
2. **Prop tracking:** list every prop (buckets, candies, cape…) and who holds it; check it is present + in the right hand in every frame; it may only change hands on screen.
3. **Physics:** jumps — airborne ≤ 0.6 s, up then down; falling objects fall down and land inside/on something; no hovering, no objects in the air without a reason; walks — measure size/x every 0.25 s, one direction only.
4. **Eyes rule:** any eye-roll, half-closed sleepy look, white eye, or face smear = FAIL (except a natural blink ≤ 0.2 s).
5. **Contact:** "holding hands / giving / hugging" must show real contact (fingers/paw wrapped), not just near each other.
6. **The 'would a real child do this?' pass:** watch each shot as a story beat: is the action natural, does it read in 1 second, does anything look strange or fake? If I have to explain it, FAIL.
7. **Real-speed pass:** a full contact sheet at 2 fps of the whole video PLUS the 8 fps strips — both, every time, for the episode AND every Short/TikTok cut.
8. **Report every doubt** to Roy as a doubt, never round it up to PASS.

### Lessons from Roy, 24.10 (Mamá TikTok keyframes)
- A trunk touching or near the other character's face or mouth in a kiss or hug = FAIL ("looks like his trunk is in Mamá's mouth"). Kisses and hugs: trunks hang down and away from faces.
- A costume gag must keep the FACE and BOTH EARS visible. A head hidden inside a costume / a missing ear = FAIL, even if the gag "reads".
- An action that must be read from a single still frame (a dodge) needs the RESULT visible: distance plus empty air. A pose alone isn't enough.
- "Borderline" = FAIL. Don't pass borderline frames to Roy.

### Lessons 24.10 (como_hace)
- i2v prompts that compare to an animal ("flap like wings", "paws like a cat") make the model ADD the animal part (feathers, paw pads) = a body change → FAIL. Describe the human gesture only ("elbows bent, hands flapping at his sides").
- Mouth-sync animal shots: MiniMax H3 > Kling 2.5 Turbo (clean openings, fewer eye closures).
- Pair shots: start with the mamá already in place beside the baby (turn + sound) instead of a walk-in.
