# ישיבת אסטרטגיה — כל 4 שעות (אוטומטי)

מטרה: ערוץ מצליח. צפיות, שימור, מנויים, ובסוף הכנסה. בכל ישיבה בודקים איפה אנחנו, חושבים איך לצמוח מהר יותר, ומחליטים על המהלכים הבאים. כל ישיבה מתועדת ביומן שבסוף הקובץ.

## סדר יום קבוע
1. **מצב העסק (5 דק').**
   - מריצים `analytics.py`.
   - בודקים לכל סרטון: צפיות ולייקים, ושימור ואחוז צפייה כשיש.
   - משווים לישיבה הקודמת: מה עלה, מה תקוע.
   - כסף: `rp.py balance`. ההוצאה היומית ב-RunPod מוגבלת ל-$5 ליום.
2. **השוק (5 דק').**
   - קוראים `research/market/latest.md`.
   - קוראים את ה-outliers האחרונים ומסתכלים על דפי הפריימים (`frames_<date>`).
   - שאלה: מה חדש שפורץ? פורמט, נושא, אורך, עולם?
3. **סיעור מוחות (10 דק').** לפחות 5 רעיונות חדשים: נושא, Hook או עלילה, מגובים בנתון. למשל:
   - סדרה (טיטו + דמות קבועה)
   - נושא עונתי (Día de Muertos, חגים)
   - שיר מוכר בעיבוד שלנו
   - אורך 11–15 שניות
   - שער עם כותרת
   - סרטון ארוך שמחבר כמה Shorts
   - פלייליסטים
   מדרגים כל רעיון לפי סיכוי × עלות × סיכון, ובוחרים 1–2 להפקה.
4. **מה למדנו.**
   - לקח אחד לפחות נכנס ל-LESSONS בדשבורד.
   - אם יש כלל שצריך לשנות, משנים אותו ב-PIPELINE / QC_RULES / WORLDS.
5. **מהלכים (ביצוע).**
   - **תור ריק:** כותבים spec + תיק לסרטון הבא, מעבירים את `preflight.py produce` ומפעילים הפקה ב-RunPod.
   - **סרטון שעבר QC וממתין:** מעלים, אם עברו לפחות 3 שעות מההעלאה הקודמת ונבדקו הנתונים שלה.
   - מקסימום 4 העלאות ביום.
6. **דיווח ל-Roy:** 5 שורות קצרות בעברית — מצב, מה למדנו, מה הוחלט, מה רץ, מה צריך ממנו.

## גבולות שהישיבה לא חוצה
- אין שירותים בתשלום חדשים בלי אישור Roy. RunPod עד $5 ליום.
- לא מוחקים סרטונים. גרסה פגומה הופכים ל-Unlisted.
- כל הפקה והעלאה עוברת `preflight.py`. אין קיצורי דרך.
- רק מודלים בעלי רישיון מסחרי (Klein 4B, Z-Image, Wan 2.2 5B, ACE-Step, Qwen3-TTS).
- סודות נשארים רק במשתני סביבה.
- החלטות גדולות מסומנות "צריך את Roy" ולא מבוצעות לבד. למשל: שינוי מדיניות המסך הנקי, דמות חדשה קבועה, הוצאה מעל התקציב.

## יומן ישיבות
<!-- כל ישיבה מוסיפה בלוק: תאריך/שעה · מצב (מספרים) · 5 רעיונות + ציון · החלטות · מה הופעל -->

### ישיבה 1 — 20.10.2026 12:48 UTC (15:48 ישראל)
**מצב:**
- 5 סרטונים ציבוריים, 20 צפיות בסך הכול, 0 מנויים.
- מוביל: gxH1p0Sp59g (מגדל) עם 8 צפיות. B (HxAYv-GieDM) עם 3 צפיות שעתיים אחרי העלאה.
- אין עדיין שימור (פיגור של 48 שעות).
- RunPod: $47.99 (היום: $2.0 מתוך $5).
- רץ עכשיו: tito_bano, שלב השוטים, 35/40.

**שוק:**
- הרגל ×4.6, אוכל ×4.0 (סריקת 14 ימים).
- outliers ברחצה: Morphle ×2,992, Tom 30.7 מיליון, Kael ×622.
- outliers בידיים: Lunito ×7,941, More Good Stories 36 מיליון.

**סיעור מוחות (סיכוי / עלות / סיכון → ציון):**
1. **"¡ALTO, Tito! ¿Y tus manos?"** — שטיפת ידיים לפני אוכל, עם אמא, בעולם של מטבח או פיקניק. 9/2/2 → **9** ✅ הבא אחרי הרחצה.
2. **"Tito no quiere dormir"** — יער קסום בלילה עם גחליליות (Gracioso Bebé ×1,715). 7/2/3 → 7. אחרי הידיים.
3. **עונתי: Halloween / Día de Muertos.** 31.10–2.11 הוא שיא חיפושים במקסיקו. צבעים עם דלעות וקלאוואריטס, בטון מתוק ולא מפחיד. 7/2/4 → 6.5. להפקה עד 27.10. צריך לבדוק רגישות תרבותית.
4. **אוסף ארוך (3–5 דקות) מכל ה-Shorts כשיהיו 8 ומעלה.** זמן צפייה ופלייליסט. 6/1/2 → 6. בעוד שבוע.
5. **פריים ראשון = שער עם כותרת גדולה** (Lunito, More Good Stories). 6/1/5 → **צריך את Roy** (מתנגש בכלל "מסך נקי").

**לקח:** הנתונים מהערוץ שלנו עדיין קטנים מדי להסקת מסקנות (2–8 צפיות לסרטון). ההחלטות נשענות על נתוני השוק (outliers ו-frames) עד שיהיו נתוני שימור.

**החלטות:**
- tito_bano: QC מלא והעלאה.
- הסרטון הבא: spec + תיק ל-"¡ALTO, Tito! ¿Y tus manos?".
- לשבוע הבא: עונתי (Halloween) עד 27.10.

**ממתין ל-Roy:** בדיקה של שער עם כותרת בסרטון אחד.

### החלטות של Roy — 20.10.2026 16:15 ישראל
- **ניסוי שער עם כותרת: אושר לסרטון אחד.**
  - איך: כותרת צהובה גדולה עם קו מתאר כהה ב-1.2 השניות הראשונות. נקבע ב-`title_card` שב-edit.json, והכלי `assemble.py` מצייר אותה.
  - איפה: הסרטון הבא, "¡ALTO, Tito! ¿Y tus manos?". אחריו חוזרים למסך נקי עד שיש נתונים.
  - מדד: שימור ב-0–5 שניות וצפיות אחרי 3 ו-48 שעות, מול "¡Tito no se quiere bañar!" (אותה שיטה, בלי כותרת).
- **הגדרות הערוץ:**
  - הוגדר: שפת ברירת מחדל ספרדית (es), תיאור ערוץ בספרדית ומילות מפתח.
  - **המדינה: IL** (Roy אישר 20.10). זה "Country of residence" של בעל הערוץ, לצורך מונטיזציה ומס. לא משפיע על הקהל — השפה, התיאור והתגיות בספרדית קובעים למי YouTube מציג.
  - **Handle:** Roy אישר שינוי. אפשר רק דרך Studio (לא API). מומלץ `@CantilandiaTV` (פנוי).
  - **כתוביות:** אין צורך בכלל (Roy 20.10) — לא צרובות ולא CC.
  - **שער כותרת:** Roy ביקש עיצוב איכותי (הראשון היה "מעפן") → production/title_card.py עם אנימציה. ניסוי ב-tito_manos.
  - כל הסרטונים כבר ב-es/es, קטגוריה Music, Made for Kids.

### בדיקת +3h — רחצה (20.10 16:14 UTC)
- **DxxmhZrbspY ("¡Tito no se quiere bañar!")**: 8 צפיות, 0 לייקים אחרי 3 שעות. Shorts קודמים באותו גיל: 0–3 (B: 3). הכי טוב שלנו ב-3 שעות.
- **לקח:** שיטת הסיפור (2 דמויות, 2 מיקומים, לופ) מתחילה טוב יותר, אבל 8 צפיות זה עדיין לא "פריצה". מכריעים לפי שימור 0–5 ש' ב-48 שעות.
- **מה הוחלט/בוצע:** "¡ALTO, Tito! ¿Y tus manos?" עלה ב-15:32 (Roy: להעלות ברגע שמוכן). סדרה חדשה Rojito (רכבים, ×38.8) — עיצוב מוכן, שוטים ב-00:05 UTC.

### ישיבה 2 — 20.10.2026 16:47 UTC (19:47 ישראל)
**מצב:** 7 סרטונים ציבוריים, 35 צפיות (ישיבה 1: 20), 0 מנויים. רחצה 8 צפיות ב-+3h (שיא). ידיים (SMMKda9GxPM, עם שער כותרת) 3 צפיות אחרי 75 דקות. אין עדיין שימור. RunPod $46.63 — היום $4.26/$5, לכן אין הפקה נוספת היום.
**שוק:** סריקת Halloween (92 Shorts, 80 ערוצים): MFK מנצחים = הרגל+תחפושת (Nick and Poli "Brush Your Fangs" 8.5M ×362), שיר דלעת (863K ×310), Minituns Halloween 2.3M. טרנד "La Calabaza" (×3,885, ×808) — שיר מוגן, לא משתמשים. סריקת פורמטים לסדרה 2: רכבים ×38.8 מול חיות ×7.4.
**סיעור מוחות (סיכוי/עלות/סיכון → ציון):**
1. **Tito Halloween: תחפושת דלעת + צחצוח שיניים** — 9/2/2 → **9** ✅ (עונתי, 11 ימים ל-31.10)
2. Rojito פרק 2: "Rojito atascado en el barro" (Car Wheel ×589, 9.6M) — 8/2/2 → 8 (אחרי שנראה את פרק 1)
3. Tito no quiere dormir (Gracioso Bebé ×1,715) — 7/2/3 → 7
4. קומפילציה ארוכה "Hábitos con Tito" (רחצה+ידיים+Halloween) — 6/1/2 → 6 (כשיהיו 3 הרגלים)
5. Rojito Halloween (רכבים + דלעות) — 7/2/3 → 6.5 (אם Rojito 1 מצליח)
**לקח:** שיטת הסיפור פותחת טוב יותר (8 מול 0–3 ב-+3h), אבל אין עדיין פריצה. מעלים מהר (Roy) ומודדים שימור ב-48h.
**החלטות:** tito_halloween — spec + תיק + preflight עברו. עיצוב (Klein + שיר) רץ באותו pod של שוטי Rojito ב-00:05 UTC (תקציב יום חדש), שוטים מיד אחרי.
**ממתין ל-Roy:** שם הערוץ ב-Studio ("Cantilandia").

### החלטת Roy — 20.10 20:52 ישראל
- **חריגת תקציב RunPod מאושרת להיום בלבד** (~$7.5–8 במקום $5): הפקה מיידית של 3 פרקי Rojito + Halloween. מחר חוזרים ל-$5.
- **L1 = פרק ארוך 2 של טיטו** (2–3 דק'): יום שלם — רחצה, ידיים, שיניים.

### ישיבה 3 — 20.10.2026 20:47 UTC (23:47 ישראל)
**מצב:** 8 סרטונים ציבוריים. רחצה 11 (+3 מאז ישיבה 2, לייק ראשון), מגדל 10, ידיים 5 (+3h: 3 — פחות מרחצה 8; השער לא עזר בינתיים), Rojito 1 (gCaM5FcbPpY) עלה 21:50 ישראל. אין עדיין שימור. RunPod $44.06 — היום ~$6.8 (Roy אישר חריגה היום).
**שוק:** סריקה 18:57 — הרגלים ×20.9 (קפץ מ-×4.6), אוכל ×4.0, צבעים ×0.37. מחזק: Halloween-שיניים, סדרת ההרגלים.
**סיעור מוחות:**
1. להשלים את התור (Halloween, Rojito 2–3) — 9/1/2 → **9** ✅ רץ עכשיו
2. פרק ארוך 2 "Un día con Tito" — 8/2/2 → 8 ✅ מחר (תקציב יום חדש)
3. Tito "a dormir" Short (שינה: Biper 34.6M) — 8/2/2 → 8 — הבא בתור
4. Rojito "lava sus ruedas"/הרגל לרכבים — 7/2/2 → 7
5. קומפילציה "Hábitos con Tito" כשיהיו 4 הרגלים — 6/1/2 → 6
**לקח:** pod עמד בטל ~שעה כי לא הייתה המתנה עם התראה → כל שלב GPU חייב המתנת רקע עם התראה + השקת השוטים במקביל לבחירת שירים (לא תלויים).
**החלטות:** שוטים ל-3 Shorts רצים (90 משימות). פרק ארוך — מחר. העלאות: Halloween / Rojito 2 / Rojito 3 ברגע שעוברים QC.

### ישיבה 4 — 21.10.2026 00:46 UTC (03:46 ישראל) — ראשונה עם סוכן החוקר
**מצב:** 9 ציבוריים. רחצה 13, ידיים 11, מגדל 10, פרק 1 5 (2 לייקים), גרביים 5. Rojito צבעים + בוץ עלו הלילה (0 עדיין). RunPod $42.75, יום חדש ($5).
**מהחוקר:** 5 תסריטים (עיר-רכבים NuNu, ספגטי/נימוסים, פח+ברווז, פחד מצל, הצלת חתלתול). ממצא חם: נימוסי אוכל +14M בפחות מ-12 שעות.
**החלטות:** עיצוב לכל 5 + keyframes ל-Halloween ול-Rojito 1 → קליפים היום ל-Halloween, ciudad, mesa, ruedas. tito_ep2 (ארוך) — אם יישאר תקציב.
**צריך את Roy:** נושא סיר/שירותים — מאשר טון?

### ישיבה 5 — 21.10.2026 04:46 UTC (07:46 ישראל)
**מצב:** 13 ציבוריים. רחצה 16, ידיים 13, מגדל 10, פרק 1 6, גרביים 5. **4 החדשים (צבעים, בוץ, Halloween, Rojito 1 v2) — 0 צפיות** ב-1–6 שעות; תקינים טכנית. RunPod $40.25 (היום ~$2.5).
**מהחוקר:** ריצה 4 — תיקוני IP ואורך שיר; 3 תסריטים חדשים (arena, brocoli, paraguas). ממצא: "צבעים בתוך הרגל" ×301 קפץ פי 2.5.
**החלטות:** היום עלו 4 (מקסימום) + 2 מתוזמנים (עיר 08:10, ספגטי 10:10 — מתוך ה-4). פרק ארוך — מחר 03:20. GPU: שירים 32 ש' + keyframes ל-dormir/basura/rescate → קליפים → העלאות מחר.
**לבדוק:** 0 צפיות לחדשים — בדיקה ב-+12h (14:40 ישראל); אם נשאר — Roy בודק בסטודיו.

### ישיבה 6 — 21.10.2026 08:46 UTC (11:46 ישראל)
**מצב:** 15 ציבוריים. **6 החדשים (צבעים, בוץ, Halloween, Rojito 1 v2, עיר, ספגטי) — 0 צפיות**; גם הישנים קפואים מ-~03:00 UTC (רחצה 16, ידיים 13, מגדל 10). חשד: המונה הציבורי לא מתעדכן — ביקשתי מ-Roy מסך "Realtime" בסטודיו. RunPod $39.63 (היום ~$3.1).
**מהחוקר:** ריצה 6 — סריקות צבע+הרגל, VS, שינה; outliers: Bibiberry "Where Is My Color" (רכבים) ×2,367, Gracioso Bebé שינה ×1,750 (מאמת את tito_dormir), Yes! Neo "Cold VS Hot" 43.5M. תסריט חדש tito_frio_calor; dormir D1 תוקן.
**החלטות:** GPU: D1 חדש ל-dormir + עיצוב ל-arena/brocoli/paraguas/frio_calor; קליפים ל-dormir אחרי סטוריבורד → מחר (סלוט רביעי). מחר: פרק ארוך 03:20, basura 05:30, rescate 07:30, dormir.
**צריך את Roy:** מסך Realtime מהסטודיו.

### ⏸ החלטת Roy — 21.10.2026 ~12:00 ישראל: עוצרים הפקה, רק ניתוח
- GPU כובה (g6 בוטל לפני שעשה משהו). 3 העלאות מתוזמנות (ארוך, basura, rescate) הושבתו — לא נמחקו, אפשר להפעיל מחדש.
- ישיבת 4 השעות → ישיבת ניתוח בלבד. משיכת נתונים כל 6 שעות ממשיכה.

### עדכון Roy — 21.10 ~15:45 ישראל
- Roy העלה **ידנית** מאפליקציית YouTube (מיקום מקסיקו): tito_basura (G-gSjH36CLA, 12:27 UTC) ו-rojito_rescate (vMMAiXfyiOg, 12:42 UTC). ההעלאות המתוזמנות נמחקו.
- tito_ep2 הוכן להעלאה ידנית ע"י Roy (production/youtube/MANUAL_tito_ep2.md). לא מעלים דרך ה-API. GPU עדיין מושהה.
- **ניסוי חדש (מקרי):** ידני מהאפליקציה + מיקום מקסיקו מול API — לבדוק אם החשיפה שונה.

### ישיבת ניתוח 7 — 21.10.2026 12:47 UTC (15:47 ישראל)
**נתונים:** rescate (ידני) 2, basura (ידני) 1, ספגטי 4, צבעים-Rojito 1, פרק 1 8 (2 לייקים); עיר, Rojito 1 v2, Halloween, בוץ — 0. ישנים ללא שינוי (רחצה 16, ידיים 13, מגדל 10). Analytics API — עדיין שורות ריקות (השהיה).
**מהחוקר (ריצות 7–8):** רוב הצפיות עד היום היו של Roy עצמו; ניתוח 0-צפיות ב-research/12; מעקב אורגני ב-research/analytics/organic_watch.json.
**השערות:** (1) ערוץ חדש — חשיפה נמוכה בימים הראשונים (ממוצע ~5 ימים/6 סרטונים עד פריצה); (2) ההעלאות הידניות קיבלו 1–2 צפיות בשעה הראשונה מול 0 ב-API — מוקדם מדי, ייתכן שהצפיות של Roy.
**חריגה מאושרת:** Roy אישר GPU לתיקון tito_ep2 בלבד (5 שוטים חדשים: השכמה, זריחה, קפיצה לבוץ, פנים מבוץ, פיג'מה). אין סרטונים חדשים.
**תנאי לחידוש הפקה:** צפיות אורגניות ראשונות (לא של Roy) על ההעלאות הידניות ב-+24h, או החלטת Roy.

### ישיבת ניתוח 8 — 21.10.2026 16:48 UTC (19:48 ישראל) — ניתוח בלבד
**נתונים (מול ישיבה 7, 12:47 UTC):**
- ידני מהאפליקציה: basura (G-gSjH36CLA) 1→**4**; rescate (vMMAiXfyiOg) 2→**4**, אבל **עכשיו private** (uploadStatus processed, בלי סיבת דחייה). לא אנחנו שינינו — לשאול את Roy.
- API מהלילה: ספגטי 4→7, צבעים-Rojito 1, עיר / Halloween / בוץ / Rojito 1 v2 — עדיין 0.
- פרק 1 (-cqaCh6sL5U) 8→10. ישנים קפואים: רחצה 16, ידיים 14, מגדל 10, גרביים 5, צבעים 4.
- Analytics API: עדיין ריק (יום / מקור תנועה / מדינה / שימור). פיגור רגיל של 48–72 שעות.
**פילוחים (מדגם קטן מאוד — כיוון בלבד):**
- ידני מול API: 4+4 ב-4 שעות מול 0,0,0,0,1,7 בהעלאות API מהלילה → **תמיכה חלשה** בהשערה שידני מקבל חשיפה.
- סיפור (רחצה 16, ידיים 14) מול סגנון ישן (מגדל 10, גרביים 5, צבעים 4, סידור 2) → סיפור טוב יותר, תמיכה חלשה.
- שער כותרת: ידיים 14 מול רחצה 16 → **אין יתרון**.
- מטא-דאטה בסגנון NuNu: עיר 0 → אין ראיה.
- Tito מול Rojito: Tito (2–16) מעל Rojito (0–8) → Rojito חלש בינתיים.
**השערות:** (1) ערוץ חדש = חשיפה נמוכה — **נתמכת** (כל סרטון נעצר אחרי הצפיות הראשונות). (2) ידני > API — תמיכה חלשה, צריך 24h. (3) סיפור > ישן — תמיכה חלשה. (4) שער כותרת — לא עוזר. (5) Rojito — חלש מ-Tito.
**מה יצדיק חידוש הפקה:** basura מגיע ל-10+ צפיות עד 22.10 13:00 UTC (+24h) בלי צפיות של Roy, או ש-Analytics מראה תנועה מ-Shorts feed / Browse. אז: **ראשון tito_ep2** (מוכן, Roy מעלה ידנית), אחריו הפקת tito_ep3_dormir.
**פתוח ל-Roy:** למה rescate הפך ל-private?

### Analysis meeting 9 — 21.10.2026 20:47 UTC (23:47 Israel) — analysis only
**Data (vs meeting 8, 16:48 UTC):** basura 4 (=), rescate 4 (still private), spaghetti 7 (=), bath 16, hands 14. **Counts went down:** episode 1 11→4, tower 10→7, socks 5→3 — YouTube removed views it doesn't count (most likely Roy's/ours). The real organic baseline is lower than we thought.
**Analytics API:** still empty; a `video` + averageViewPercentage query without a filter is refused — needs `filters=video==ID` per video (fix for the next pull).
**Hypotheses:** (1) manual vs API — no change in 4 hours, still not proven. (2) Story > old style — still holds (16/14 vs 2–7). (3) Low exposure for a new channel — supported; the view deduction strengthens it.
**Production (Roy approved ep3):** tito_ep3_dormir is in final assembly; physics/trunk QC found and fixed: the Hook shadow, a curtain at the window, square frames that were being cropped. bano/mesa/basura/halloween/torre are out of "más canciones" (trunk/physics). The researcher's note (an N12 segment of 0.3 s) — being fixed.
**Resume condition:** unchanged. Roy uploads ep3 manually; we measure 24 hours.

### Analysis meeting 10 — 22.10.2026 00:47 UTC (03:47 Israel) — analysis only
**Note:** this routine still says "production paused", but Roy since restarted production (ep3 approved, Halloween ep4 is NOW with deadline 24.10 18:00 IL). This meeting only analyzes; it does not touch the Halloween work.
**YouTube (vs meeting 9, 20:47 UTC): no change.** basura 4, rescate 4 (still private), spaghetti 7, bath 16, hands 14, tower 7, episode 1 4. Channel total 5 counted views, 0 subscribers.
**Analytics API:** first retention numbers arrived (averageViewPercentage): tower Short 168% (loops/rewatches), episode 1 12.5%, two other videos 15–24%. Daily views / traffic sources still empty. Tiny samples — direction only.
**TikTok (Roy's screenshot):** the same pool video (tito_basura) has **356 views on TikTok vs 4 on YouTube**, audience Central America (Nicaragua 38%, Honduras 29%, El Salvador 17%), adults 35+ (parents and grandparents).
**Hypotheses:**
1. New YouTube channel = almost no exposure — **strongly supported** (nothing moves for 12+ hours).
2. The content itself does not get views — **rejected**: TikTok shows it from the first video.
3. Manual vs API upload on YouTube — no difference (both stuck at 4).
4. Story > old style — still holds weakly (16/14 vs 2–7). Long episode retention 12.5% is low; the Short loop (168%) works.
**What justifies continuing:** TikTok, not YouTube, is the place where we see reach now. Continue Halloween (deadline), and post every finished video on TikTok too, with captions for parents. On YouTube: the first organic movement on any video, or Analytics traffic from the Shorts feed.
**Order:** Halloween ep4 (in production) → ep3 dormir (sent to Roy, waiting for the research check) → ep2.

### Analysis meeting 11 — 22.10.2026 04:46 UTC (07:46 Israel) — analysis only
**Note:** production is running again by Roy's decision (Halloween ep4 clips are rendering now, deadline 24.10 18:00 IL). This meeting only analyzes.
**Data (vs meeting 10, 00:47 UTC):** almost no change per video: hands 14→15; basura 4, rescate 4 (private), spaghetti 7, bath 16, episode 1 4. **The channel total jumped 5→80 views** — the per-video sum is ~100, so YouTube updated the channel counter (after removing uncounted views), not new traffic. 0 subscribers.
**Analytics API:** retention unchanged (tower Short 168%, episode 1 12.5%, others 15–24%). Daily views / traffic sources still empty.
**Hypotheses:** no change from meeting 10 — new YouTube channel = almost no exposure (supported); content is fine (TikTok 356 views on the same video); manual vs API — no difference.
**What justifies more effort on YouTube:** the first organic movement on a new upload, or traffic data from the Shorts feed. Until then: finish Halloween, post on TikTok and YouTube together.
**Order:** Halloween ep4 (clips rendering) → ep3 fixes (research QC 22.10: black first frame, lamp face, dark hook, giraffe shadow, window figure) → ep2 fixes (teeth, overalls in bath, red hand prop).

### Analysis meeting 12 — 22.10.2026 08:47 UTC (11:47 Israel) — analysis only
**Data (vs meeting 11, 04:46 UTC):** no change at all — bath 16, hands 15, spaghetti 7, tower 7, basura 4, rescate 4 (private), episode 1 4. Channel 80 views, 0 subscribers. Retention unchanged (tower 168%, episode 1 12.5%); daily views/traffic sources still empty.
**Hypotheses:** unchanged — a new YouTube channel gets almost no exposure (supported: ~36 h with no movement); content works on TikTok (356 views on the same video).
**Production (Roy's own decision, running):** Halloween ep4. Roy watched v5 and found motion problems (ping-pong loops, frozen holds, walking in place, trunk on the cheek) → v7 is being rebuilt with 5 s takes, no loops, and real walking (camera tracking). Rules added to research/QC_CHECKLIST.md §6–7.
**Process note:** some pushes were silently rejected (v6 never reached origin); fixed, and every push is now checked with git ls-remote.
**What would justify more YouTube effort:** first organic movement after the Halloween upload (holiday search demand), or traffic data from the Shorts feed. Order: Halloween ep4 (v7) → ep3 fixes → ep2 fixes.

### Analysis meeting 13 — 22.10.2026 12:49 UTC (15:49 Israel) — analysis only
**Data (vs meeting 12, 08:47 UTC):** no change — bath 16, hands 15, spaghetti 7, tower 7, basura 4, rescate 4 (private), episode 1 4. Channel 80 views, 0 subscribers; the channel now shows 13 videos (was 14 — one is no longer counted as public/listed). Retention unchanged (tower 168%, episode 1 12.5%); daily/traffic still empty.
**Research (11-research-log, 12:05):** Halloween proof — Plim Plim "¡Veo, Veo Colores en Halloween! 🎃🚪 Juego de Puertas Sorpresa" 2.38M in 8 days (same doors + surprise mechanic as ours); question titles win; healthy-teeth angle (Doctora Sophia 9.4M) fits our toothbrush ending. Search peaks in the last week of October → 24.10 upload is late but inside the peak; Shorts 25–27.10 are the main push.
**Hypotheses:** unchanged — new YouTube channel ≈ no exposure (supported, ~40 h flat); TikTok is where reach exists now.
**Production (Roy's decision, running):** Halloween v8b (beat-synced cuts, new ending, C1 trunk fix) + 3 Shorts building; ep2 v3c pushed (QC pending) + TikTok cut A. A frame-rounding bug in assemble.py was found and fixed (cuts drifted up to 0.35 s off the beat).
**What would justify more YouTube effort:** first organic movement on the Halloween upload (holiday search demand). Order: Halloween (24.10) → ep2 → ep3 rebuild (design bible).

### Analysis meeting 14 — 22.10.2026 16:50 UTC (19:50 Israel) — analysis only
**Data (vs meeting 13, 12:49 UTC):** ep2 "¡Buenos días, Tito!" (nWPm2InSAJo, uploaded 13:15 UTC public, Made for Kids) = 1 view after 3.5 h. All other videos unchanged (bath 16, hands 15, spaghetti 7, tower 7, basura 4, episode 1 4); channel 80 views (the API count lags; research log saw 82), 0 subscribers. Retention still only for tower (168%) and episode 1 (12.5%).
**Hypotheses:** "new YouTube channel ≈ no exposure" strongly supported — even a finished, QC-passed long episode with NuNu-style metadata gets ~0 impressions in its first hours. Content quality is not the bottleneck on YouTube right now; distribution is (TikTok package #1 sent today).
**Production (Roy's decisions):** Halloween FINAL + 3 Shorts delivered to Roy for the 24.10 upload; ep3 rebuild v3 in QC (4 fixes in progress: K1 trunk mask, N06 shadow, N09 window, N16 butterfly).
**What would justify more YouTube effort:** first impressions on ep2 or Halloween (24.10, peak search week). Next check: ep2 views/impressions at +24 h.

### Analysis meeting 15 — 22.10.2026 20:47 UTC (23:47 Israel) — analysis only
**Data (vs meeting 14, 16:50 UTC):** views flat (channel 77 by the API, 0 subscribers; ep2 nWPm2InSAJo 2 views after 7.5 h). NEW: YouTube Analytics now returns retention for 4 videos — Short "bath" (DxxmhZrbspY) avg 73% watched, Short "tower" (gxH1p0Sp59g) 115% (re-watched), Short "hands" (SMMKda9GxPM) 31%, episode 1 (-cqaCh6sL5U) 21%.
**What it says:** among the Shorts, the ones with one clear action + payoff (bath, tower) hold viewers 2–4× better than "hands" (a song montage). The long episode loses most viewers early (21%) — the hook/first 15 s matters most for the long format. Small samples (13–16 views), so direction only.
**Hypotheses:** distribution is still the bottleneck (unchanged); new, weak signal: "one action + payoff" Shorts retain better than montage Shorts → fits the director-mode / START→ACTION→END rules now used in every episode.
**Production (Roy's decisions):** Halloween + ep3 with Roy (In Review); tito_brocoli: 19 keyframes passed, clips done, song (8 takes) + 2 re-takes rendering.
**Next:** check ep2 at +24 h; Halloween goes up 24.10.
