# 11 — יומן מחקר (סוכן מחקר ותסריטים, כל שעתיים)

### ריצה 1 — 20.10.2026 23:00 UTC
**מה נסרק:**
- סריקת שוק (14 ימים) ו-outliers כללית — טריות מ-22:48 UTC (לא הורצו שוב).
- **סריקות נישה (ערים/שינה/הצלה) נכשלו: מכסת Search של YouTube API נגמרה להיום** (429 "Search Queries per day"). מתאפסת ~07:00 UTC. הסריקות הבאות לא ירוצו במקביל (3 במקביל = שריפת מכסה).
- במקום זה: איחוד 6 סריקות היום (כללי, serie2, bano, manos, halloween, clasicos) = 672 Shorts, 131 עם MFK + ≥200K + ≥×50.
- **צפייה:** 12 מנצחים (`research/market/frames_2026-10-20_estudio/`, `story_study_2026-10-20_estudio.json` — כותרות, תיאורים, תגיות).

**Top 5 outliers רלוונטיים (MFK):**
| ×ערוץ | צפיות | אורך | ערוץ | כותרת |
|---|---|---|---|---|
| ×3,604 | 25.7M | 20s | Milo Kids (18.3K מנויים) | No Littering Good Manners |
| ×1,715 | 2.87M | 22s | Gracioso Bebé | No Quiero Dormir Solo |
| ×1,382 | 44.4M | 19s | NursyTots (47.7K) | Don't Throw Garbage on the Road |
| ×928 | 34.8M | 16s | Biper y sus Amigos | ¡Qué día tan especial! A dormir |
| ×665 | 8.6M | 17s | Singaroo KIDS | Sing Along with Construction Vehicles |

**מה רואים במנצחים (פריימים + תיאורים):**
- **Singaroo (×665, ×162):** פשוט מאוד — קלף צעצוע + שם הרכב, אותו רכב חוזר פעמיים (פזמון). 17–18 ש'. גרסת "Guess & Sing" = אותו תוכן כמשחק ניחוש. → מבנה חוזר עם צליל לכל רכב מספיק; לא צריך עלילה מסובכת.
- **KORIRI (×450):** כבאית/משטרה/אמבולנס, כל אחד עם הצליל שלו ("Wee-woo! Nee-naw!") בתיאור ובשיר. רכבי חירום = צלילים.
- **Milo Kids / NursyTots (×3,604 / ×1,382 / ×214):** פריים 1 = ילד במכונית זורק שקית מהחלון. אחר כך תקריב פנים מודאגות, ושוטר עם משרוקית מלמד. 17–20 ש'. 3D בסגנון Cocomelon, אותה טכנולוגיה כמו שלנו. התיאור מספר את כל העלילה.
- **Gracioso Bebé (×1,715):** ילד אמיתי מתחת לשמיכה; רפאים-סדין בחלון ועיניים מתחת למיטה (פחד → התגברות). "vencer el miedo a la oscuridad" בתיאור.
- **Biper (×928):** ילד עם טאבלט בלילה, לא רוצה לישון → ארוחה משפחתית. פנים בתקריב.
- **VocaVoca (2.1M צפיות ליום):** דמויות ממיינות זבל לפחים צבעוניים, משאית זבל. זבל = נושא חם עכשיו.

**מה משותף למנצחים:** (1) הטעות/הבעיה היא פריים 1, לא הקדמה. (2) תקריב רגשי אחד (מודאג/מפחד). (3) מבוגר-מורה שמראה ולא נוזף. (4) 16–22 ש'. (5) התיאור מספר את העלילה במשפט אחד עם צלילים.

**חדש מאז הסריקות הקודמות:** "לא לזרוק זבל" הוא ה-outlier הגבוה ביותר שמצאנו (×3,604) ועדיין אין לו גרסה ספרדית חזקה (El Tren Ñam-Ñam: ×0.3–×3.9 בלבד). שינה — שני outliers באותו ערוץ (×1,715, ×427) = הנושא עובד שוב ושוב.

**כללים חדשים (1–3):**
1. **הטעות בשנייה 0, באמצע תנועה** (זריקה באוויר, צל על הקיר, צפירה) — לא הקמת מקום.
2. **בשיר "X hace Y", כל הדמויות הצדדיות צריכות את ה-hero בפריים** (הבילדר תמיד מוסיף את Rojito/Tito כ-ref) → לכתוב "over-the-shoulder/at the edge of the picture" ולהתאים את `hero.one`.
3. **סריקות נישה — אחת-אחת ועם מעט חיפושים** (2–3 שאילתות), כדי לא לשרוף את מכסת ה-Search היומית.

**תסריטים:** rojito_ciudad, tito_dormir, tito_basura → `script_ready` (preflight produce עבר).

### תוספת — 21.10.2026 (בקשת Roy): rojito_rescate
- תסריט "¡Rojito al rescate del gatito!" — rescue_mission (דפוס ראשון מסוגו), עולם חווה/מטע תפוחים. preflight עבר.
- **בדיקת ספרדית לכל 4 התסריטים:** "resbaladilla" (מקסיקו) במקום "tobogán" (ספרד); תוקנו סימני פיסוק: ¡ כפול בתוך שורה (rojito_ciudad) ו-"Tito, ¿dónde va la basura?" (tito_basura).
- **כלל:** מילת צליל באמצע משפט בלי ¡ נוסף ("hace nii-noo"); פנייה בשם לפני סימן השאלה.

### ריצה 2 — 21.10.2026 00:05 UTC (מתוזמנת)
**מה נסרק:** סריקת שוק טרייה (22:48, פחות מ-6 שעות) — לא הורצה שוב. **Search עדיין חסום** (מכסה יומית, מתאפסת ~07:00 UTC). במקום זה **סריקת תנופה חדשה (momentum):** משכתי מחדש את הצפיות של 180 ה-outliers החזקים מאתמול (videos.list, זול) ומדדתי כמה כל אחד גדל מאז הסריקה של 20.10 → `research/market/momentum_2026-10-21.json`. צפייה: 12 העולים הכי מהר (`frames_2026-10-21_momentum`, `story_study_2026-10-21_momentum.json`).

**Top 5 לפי צמיחה מאז אתמול:**
| גדל ב- | ×ערוץ | אורך | ערוץ | כותרת |
|---|---|---|---|---|
| +7.08M | ×63 | 31s | El Tren Ñam-Ñam | ¡Boo Olvidó sus Modales en la Mesa! |
| +6.94M | ×166 | 41s | VocaVoca | My First Mealtime Routine: Wash, Eat, Tidy Up |
| +3.93M (+13.7%) | ×26 | 47s | Doctora Sophia | ¡Vamos a Cepillar el Diente Gigante! |
| +3.26M | ×301 | 27s | Doctora Sophia | Colores con Globos de Agua / Cepíllate los Dientes |
| +2.49M | ×200 | 34s | Doctora Sophia | Baby Need to Go Potty (Big and Small) |

**מה משותף:** (1) **ארוחה/נימוסים/שיניים/סיר** — הרגלי גוף ואוכל, לא צבעים. (2) **פריים 0 = פרצוף מוגזם או שימוש מצחיק לא נכון** (ספגטי על הפנים, סיר על הראש כמו כובע — Bacinica ×32). (3) **חפץ מדבר** (סיר-מכונית, מברשת-שיניים מורה) — כמו הפח שלנו ב-tito_basura. (4) 27–47 ש' — הסרטונים שעולים מהר היום ארוכים יותר מה-outliers של אתמול (16–22 ש').

**חדש מאז הריצה הקודמת:** נימוסי אוכל הם הנושא הכי חם עכשיו (+14M לשני סרטונים ב-<12 שעות). **שירותים/סיר** — גדל (+2.5M, +305K), נושא שעוד לא נגענו בו.

**כללים חדשים:**
1. **מדד תנופה בכל ריצה:** משיכה חוזרת של הצפיות של ה-outliers (videos.list) = מה חם *עכשיו*, גם כשה-Search חסום.
2. **"שימוש מצחיק לא נכון" כפתיחה** (ספגטי בחדק, סיר על הראש) — בעיה + צחוק בשנייה 0.

**תסריטים:** tito_mesa (ספגטי עם החדק) → script_ready. כל 5 התסריטים שלי עוברים preflight מול ה-registry המעודכן (barro פורסם).
**רעיון הבא:** "Tito y la bacinica" (סיר) — צריך בדיקת טון מול Roy? נושא רגיש-גבולי אבל נפוץ מאוד בערוצי ילדים; אכתוב אם אין התנגדות.

### ריצה 3 — 21.10.2026 02:05 UTC (מתוזמנת)
**מצב:** המפיק לקח את כל 5 התסריטים שלי להפקה (in_production) → 0 מוכנים שלי. משוב `_review_2026-10-21.md`: אין שינויים נדרשים; ללמוד: לפצל פעולה מורכבת לשני שוטים, לא שני רכבים-דמויות באותו פריים; נושא הסיר — רק אחרי Roy. `song_takes` ירד ל-8.
**מה נסרק:** Search עדיין חסום (מכסה). **תנופה של שעתיים** (00:15→02:05, 1.84 ש') על 180 outliers → `momentum_2026-10-21_0215.json`.

**Top 5 לפי צפיות לשעה עכשיו:**
| לשעה | ×ערוץ | ערוץ | כותרת |
|---|---|---|---|
| 456K | ×63 | El Tren Ñam-Ñam | ¡Boo Olvidó sus Modales en la Mesa! |
| 280K | ×166 | VocaVoca | My First Mealtime Routine |
| 217K | ×26 | Doctora Sophia | ¡Vamos a Cepillar el Diente Gigante! |
| 141K | ×41 | El Tren Ñam-Ñam | Crayón Gris Travieso VS. Lápices de Colores |
| 93K | ×23 | El Tren Ñam-Ñam | ¿Qué Disfraz de Halloween Elegirás? |

**מה משותף/חדש:** אותם מובילים כמו לפני שעתיים — הטרנד יציב (ארוחה, שיניים, "ענק"). חדש: **"VS" / יריבות** (Crayón Gris VS Lápices ×41, 141K לשעה) ו**לשטוף צעצועים מלוכלכים** (Bebefinn ×55).
**כללים:** (1) חשיפה הדרגתית ברמזים (סנפיר ← זנב ← הכול) — כל פריים כותב במפורש מה רואים ומה עוד מוסתר. (2) "בדיחת גוף של הדמות" (חדק-קשית, אוזניים-מטרייה) = טוויסט שרק הדמות שלנו יכולה — לחזור עליו.
**תסריטים חדשים (script_ready, preflight עבר):** rojito_arena (mystery, חוף), tito_brocoli (סירוב → ענק ביער ברוקולי, ג'ונגל), tito_paraguas (שיתוף בגשם, אוזניים-מטרייה).
**רעיון הבא:** "VS" — "¿Dulce o fruta?" / Rojito VS. מכונית אפורה (Crayón Gris ×41).

### ריצה 4 — 21.10.2026 04:05 UTC (מתוזמנת)
**מצב:** rojito_ciudad ו-tito_mesa ב-QC; dormir/basura/rescate בהפקה. **+3h של colores/barro: 0 צפיות**; הישנים עם סיפור ממשיכים לעלות (רחצה 16, ידיים 13). משוב חדש ב-`_general.md`: (1) `song_seconds` 30–34 לשיר של 8 שורות, טוויסט עד ~20 ש'; (2) **IP** — רכבת כחולה עם פרצוף יצאה "תומס"; לבדוק כל דמות חד-פעמית מול דמויות מוכרות; (3) רוטב אדום על הפנים = נראה כמו דם; (4) חפץ מול הפנים מתמזג איתן.
**מה נסרק:** Search עדיין חסום. תנופה (02:06→04:06):
| לשעה (לפני שעתיים) | ×ערוץ | כותרת |
|---|---|---|
| 522K (280K) | ×166 | VocaVoca — My First Mealtime Routine |
| 495K (456K) | ×63 | El Tren Ñam-Ñam — Modales en la Mesa |
| 291K (217K) | ×26 | Doctora Sophia — Diente Gigante |
| 230K (141K) | ×41 | El Tren Ñam-Ñam — Crayón Gris VS Lápices |
| 204K (81K) | ×301 | Doctora Sophia — Colores con Globos de Agua / Cepíllate los Dientes |
**חדש:** הכול מאיץ (ערב במקסיקו). "צבעים + הרגל" (גלובוסים של מים + צחצוח) קפץ פי 2.5 — צבעים לבד חלש (×0.37), אבל צבעים בתוך הרגל עובד.
**שיפורי תסריטים (שלב 6):** rojito_arena — הצב כתום-אפרסק עם נקודות צהובות (צב ירוק מחייך = Crush מ"נמו"); tito_paraguas — האפרוח הצהוב שאומר "pío, pío" הוחלף בארנבון אפור (קרוב מדי ל-"El Pollito Pío"); לשלושתם `song_seconds: 32`. preflight עבר.
**כללים:** (1) **בדיקת IP לכל דמות חד-פעמית** לפני כתיבה: צבע + פרצוף + צליל מול Thomas, Crush, Pollito Pío, Paw Patrol, Tayo, Robocar Poli. (2) **אוכל על הפנים = נקודות כתומות קטנות**, לא "covered".
**רעיון הבא (כשהמכסה חוזרת):** "צבעים בתוך הרגל" — טיטו ממלא בלוני מים צבעוניים בחדק ובסוף רוחץ את עצמו (×301) + פורמט VS.

### ריצה 5 — 21.10.2026 06:06 UTC (מתוזמנת)
**טיפול במשוב קודם:** `tito_dormir` → `needs_rewrite` (D1 בלי צל). **סיבה שמצאתי:** D1 התחיל ב-"Wide shot", ולכן במצב במאי קיבל את תמונת המיקום (חדר ריק) כ-ref והעתיק אותה. D4, בלי ref של מיקום, צייר צל ג'ירפה ענק וברור. **תיקון:** D1 מתחיל עכשיו ב-"Low angle from the foot of the bed…", בלי ref מיקום; הצל הענק בסגול כהה הוא הנושא, וטיטו קטן בפינה → `script_revised`.
**כלל חדש (חשוב):** **אם ה-Hook/הפעולה המרכזית נמצאים בשוט הרחב הראשון, אל תפתח אותו ב-"Wide"** — ה-ref של המיקום הריק "בולע" את הפעולה. שוט רחב = הקמת מקום בלבד, או שהפעולה מתוארת בשוט עם זווית מפורשת.
**שאלת המפיק — 0 צפיות לחדשים:** בדקתי ב-API את 7 הסרטונים: כולם `processed`, `public`, MFK, בלי חסימת אזור, אודיו es. אין תקלה טכנית. אין לי נתון שוק על "זמן עד צפייה ראשונה" (ה-API לא נותן היסטוריה). השערות: (1) הצפיות המוקדמות של הישנים (3–8 ב-+3h) הגיעו כנראה מצפייה שלנו ושל Roy; (2) פיד ה-Shorts בודק ערוצים חדשים באיחור של 12–48 שעות (research/06b, vidIQ: "views often arrive days later"); (3) 6–7 העלאות ב-12 שעות — YouTube אומר שתדירות לא משנה, אבל זה לא מוכח לערוץ בן יומיים. **המלצה:** Roy יבדוק ב-Studio → Analytics → "Viewed vs. swiped away" ו-impressions לסרטון אחד חדש; אם יש impressions ו-swipe גבוה — זו בעיית Hook, לא הפצה.
**תנופה (04:08→06:10):** VocaVoca ארוחה 493K/h, נימוסים 342K/h (יורד), **צבעים בבלוני מים + צחצוח ×301 — 251K/h (עולה, 3 מדידות ברצף)**, Diente Gigante 220K/h, Crayón Gris VS 209K/h, Puerta Misteriosa (אוכל → צבעים) 119K/h (עולה).
**Search חוזר ~07:00 UTC** → הריצה הבאה (08:04): סריקות נישה (צבעים+הרגל, VS, שינה, הצלה), אחת-אחת.

### ריצה 6 — 21.10.2026 08:05 UTC (מתוזמנת) — Search חזר
**מה נסרק:** סריקת שוק (14 ימים, 114 MFK) + 3 סריקות נישה ברצף, 3 שאילתות כל אחת: `colhabito` (צבעים + הרגל), `versus` (VS/הפכים), `dormir`. צפייה ב-12 המובילים: `frames_2026-10-21_estudio2`, `story_study_2026-10-21_estudio2.json`.
**שוק:** הרגל ×12.19 (ירד מ-×20.87, עדיין ראשון), אוכל ×4.14, שיר ×1.19, צבעים ×0.38, "dónde está" ×0.28.

**Top 5 outliers חדשים (MFK):**
| ×ערוץ | צפיות | אורך | ערוץ | כותרת |
|---|---|---|---|---|
| ×2,367 | 2.67M | 40s | Bibiberry | Let's Color My Cars / Where Is My Color Song |
| ×1,750 | 3.35M | 22s | Gracioso Bebé | Hora de Dormir Sin Miedo |
| ×500 | 3.0M | 53s | RoboSquad Melodies | Where Is My Color |
| ×288 | 334M | 27s | Doctora Sophia | Colores con Globos de Agua / Cepíllate los Dientes |
| ×143 | 43.5M | 39s | Yes! Neo | Cold VS Hot Challenge / Healthy Habits |

**מה רואים:** Bibiberry — כבאית/משטרה/אמבולנס עם משפטי הצלה ("I'm here to save the day") → רכבי הצלה שוב. Yes! Neo — פריים 0 מפוצל: ילד קפוא בקרח מול ילדה מעלה אדים, אחר כך שתי אמבטיות (קרח מול אש), קשת בסוף. Doctora Sophia — שיניים בצבעים (Azul, Rojo) מתלכלכות מבלוני מים בטעם פירות ואז מצחצחות. Gracioso Bebé — כבר 3 outliers על שינה/פחד (×1,750, ×1,496, ×376): **הנושא של tito_dormir מאומת שוב.**
**חדש:** "Where is my color" עם רכבים (×2,367) ו-VS של הרגלים (×143, 43.5M).
**כללים:** (1) **מצב קיצוני הפוך פעמיים** (קפוא ↔ לוהט) = Hook + אמצע חזקים. (2) כלל מריצה 5 נשמר: הפעולה המרכזית לא בשוט שמתחיל ב-"Wide".
**תסריטים:** חדש — **tito_frio_calor** (קר מול חם, chamarra) → script_ready. בתור שלי: arena, brocoli, paraguas, frio_calor (+ dormir revised).
**רעיון הבא:** Rojito "¿Dónde está mi color?" (Bibiberry ×2,367) — רוחיטו הופך אפור ומוצא את האדום; לבדוק שזה לא חוזר על rojito_colores.

### החלטת Roy — 21.10.2026 ~09:00 UTC
- אין עדיין נתוני Studio ("Viewed vs swiped"). הסרטונים החדשים לא מגיעים לקהל בכלל (0 צפיות).
- **מחכים כמה ימים ובודקים שוב** — ייתכן שלוקח זמן עד שערוץ חדש נכנס להפצה. לא משנים כיוון בגלל 0 צפיות עד אז.
- **מה אני עושה בינתיים:** ממשיך מחקר ותסריטים כרגיל. בכל ריצה אבדוק בנתונים (`research/analytics/latest.json`) מתי מגיעות הצפיות הראשונות לכל סרטון חדש, ואתעד את זמן ההגעה כדי שנדע מה נורמלי לערוץ שלנו.

### נתוני Studio מ-Roy — 21.10.2026 ~09:30 UTC (צילום מסך, Shorts, 28 יום)
- **70 צפיות** בסך הכול ב-Shorts (כרטיס שני: 42, כנראה צפיות מעורבות). הקפיצה כולה מ-20.10.
- **"המשיכו לצפות" 65.6% מול "החליקו" 34.4%.** הנתון לא רע, אבל המדגם קטן מאוד.
- מוביל: "¡Tito no se quiere bañar!" — 16.
- **Roy: "יכול להיות שרוב הצפיות זה בכלל אני."** סביר: 70 צפיות על 13 סרטונים, ו-Roy צפה בכל סרטון אחרי העלאה. זה מסביר גם למה הישנים קיבלו 3–8 צפיות ב-+3h והחדשים (שכבר לא נצפו ע"י Roy) קיבלו 0.
- **מסקנה:** ה-65.6% כנראה משקף בעיקר את Roy, לא את הקהל. אין עדיין נתון אמיתי על ה-Hook שלנו.
- **לבדיקה ב-Studio:** קהל → מיקום גיאוגרפי (ישראל = Roy; מקסיקו/לטינו = קהל אמיתי); מקור תנועה → "פיד Shorts" + חשיפות (impressions).
- **המלצה:** לא לצפות בסרטונים מחשבון הערוץ / מישראל בימים הקרובים, כדי שהנתונים יהיו נקיים.

### ריצה 7 — 21.10.2026 10:05 UTC — ניתוח בלבד (ההפקה מושהית ע"י Roy)
- **ניתוח מלא:** `research/12-zero-views-analysis.md`. המונה לא תקוע (API 76 ≈ Studio 70); כמעט כל הצפיות של Roy; מ-20.10 22:34 UTC אף סרטון לא קיבל צפייה אורגנית.
- **39 ערוצים חדשים מהשוק** (`new_channels_2026-10-21.json`): לערוצים קטנים חציון 5 ימים ו-6 סרטונים עד להיט ראשון (10K+). Lunito (הכי דומה לנו) — 47/64/51 צפיות בשלושת הראשונים, להיט ברביעי אחרי 8 ימים.
- **מעקב חדש:** `research/analytics/organic_watch.json` — צילום צפיות לכל סרטון בכל ריצה, כדי לתפוס את הצפייה האורגנית הראשונה.
- **בלי תסריטים חדשים** (לפי ההשהיה). 5 תסריטים מוכנים בתור.

### ריצה 8 — 21.10.2026 12:07 UTC — ניתוח בלבד
- מעקב: ספגטי 0→2 (הראשון שזז מאז ש-Roy הפסיק לצפות), צבעים 1, השאר קפואים.
- Lunito: רוב 14 הסרטונים הראשונים 28–64 צפיות; פריצות בודדות (#4 21K, ה-Short הראשון 35K). עדכון ב-research/12.

### Roy — 21.10.2026 ~13:00 UTC: ניסוי העלאה ידנית
- Roy העלה **ידנית מאפליקציית YouTube**, עם מיקום מקסיקו: **tito_basura** ו-**rojito_rescate** (כותרת ותיאור מ-`production/youtube/upload_<id>.json`). **לא להעלות אותם שוב דרך ה-API.**
- הניסוי: האם העלאה ידנית מקבלת צפיות אורגניות, כשכל ההעלאות דרך ה-API על 0–2. Roy לא צופה בהם.
- Roy מבקש מהמפיק להכין את הפרק הארוך (tito_ep2), ואותו מעלים ידנית באותה דרך.

### 21.10.2026 ~14:30 UTC — שינוי כיוון (Roy): פרקים ארוכים קודם, Shorts מהם, סרטון אחד ביום
- סריקות ארוכות חדשות (`research/longform_scan.py`): 20–40 דק' — חציון 38 אלף צפיות ליום (הכי גבוה); כותרת "+ más" פי 1.9.
- המוביל בספרדית: Monito y Canciones (3D AI, הרגלים) — 79.5 מיליון בשיר החיתול, 903 אלף ליום.
- הצעת פורמט מלאה: `research/14-longform-format.md`. הפרק הראשון המוצע: "Tito no puede dormir".

### 21.10.2026 ~15:00 UTC — Roy אישר: פרק ארוך ראשון
- **tito_ep3_dormir** — "¿Qué es eso? ¡Tito no puede dormir! + Más Canciones Infantiles". 16:9, שיר ~2:30 (3 בתים + אותו פזמון ×3), 20 שוטים ייחודיים, ואחריו קומפילציה (8–10 דק'). 3 Shorts ייגזרו ממנו. preflight עבר → script_ready (עדיפות 1).
- tito_dormir (Short) הוחלף על ידי הפרק הזה.

### ריצה 9 — 21.10.2026 14:08 UTC
- **ניסוי העלאה ידנית — סימן ראשון חיובי:** rescate (vMMAiXfyiOg) 4 צפיות ו-basura (G-gSjH36CLA) 2 צפיות, כשעה וחצי אחרי ההעלאה (Roy לא צופה). ההעלאות דרך ה-API מאתמול בלילה: 0–1. ספגטי עלה ל-7 (+5). עדיין מדגם קטן — ממשיכים לעקוב.
- **יושמו כללי נוזלים חדשים** (`_general.md`): בלי splash קפוא ב-keyframe (paraguas U1/U7, frio_calor F7, arena A3), ושוטי שינה עם תנועה (ep3 K4/N16). preflight עבר.

### ריצה 10 — 21.10.2026 16:06 UTC
- מעקב: rescate 4 (+0), basura 2 (+0), ספגטי 7 (+0), ruedas v2 1 (+1). סה"כ 70. אחרי הצפיות הראשונות, אין צמיחה בשעתיים האחרונות.
- המפיק מתקן את tito_ep2 לפי הערות Roy (פיזיקה של מים, חדק). Roy יעלה אותו ידנית מחר (המלצה: סרטון אחד ביום, ולתת לניסוי הידני 24 שעות).
- תור: 5 תסריטים מוכנים (ep3_dormir בעדיפות 1). אין משוב חדש לחוקר.

### ריצה 11 — 21.10.2026 18:06 UTC
- **rescate (vMMAiXfyiOg) — private.** ב-16:06 עוד היה ציבורי (4 צפיות). עכשיו לא מופיע ב-API הציבורי. המפיק ראה private ב-16:48, בלי סיבת דחייה, ואנחנו לא שינינו. **שאלה ל-Roy:** האם שינה בטעות באפליקציה? אם לא — לבדוק ב-Studio אם יש הודעה (זכויות יוצרים / מדיניות).
- מעקב: basura 2→**4**, פרק 1 8→**11**. סה"כ 75 (בלי rescate).
- סריקת שוק 18:06: הרגל ×12.17, אוכל ×4.44, שיר ×1.53, צבעים ×0.34 — יציב.
- המפיק התחיל עיצוב ל-tito_ep3_dormir + compile_mas.py ל-"más canciones".

### ריצה 12 — 21.10.2026 20:05 UTC
- מעקב: אין שינוי (סה"כ 75). rescate עדיין private.
- **בדיקת סנכרון של ep3 (build/tito_ep3_song.edit.json):** סדר השוטים תואם ל-`sequence` בדיוק (3 בתים, פזמון K1–K4 ×3, N04 חוזר). שתי הערות למפיק:
  1. N12 כולל מקטע של **0.3 ש'** (in 1.76) — חיתוך קצר מדי, ייראה כקפיצה. עדיף להאריך את המקטע הקודם, או לנגן את N12 לאט יותר.
  2. **N08 (שמיכה רועדת) לא בשימוש** — טעות שלי: כתבתי שוט שלא נכנס ל-sequence. **כלל חדש:** כל שוט ב-`shots` חייב להופיע ב-`sequence` (בודק לפני script_ready).

### 21.10.2026 ~21:00 UTC — בדיקה ויזואלית לבקשת Roy (עיניים קופצות, עין דרך החדק, פרצופים מעוותים)
- כלי חדש `research/glitch_scan.py` (שינוי מקומי חד בין פריימים בחלק שנכנס לעריכה). ep2: 56 אירועים — רובם מצמוץ/קריצה של פריים אחד; E20 — עין מעל החדק; E14 — קריצה + שיניים.
- ep3 keyframes: N07 חושף את הינשוף מוקדם; K2/K3 טיטו עומד בפזמון (קפיצת המשכיות); N02 מנורה עם עיניים.
- דוח מלא: `production/agents/research_reports/qc_2026-10-21/REVIEW.md`. 4 כללי פרומפט חדשים (עיניים יציבות, חדק מתחת לפה, חיוך עדין, בלי לחשוף את התשובה בשוט השאלה).

### ריצה 13 — 21.10.2026 22:05 UTC
- המפיק הכין מחדש את ה-keyframes של ep3 אחרי הדוח שלי: ג'ירפה עם עיני כפתור, משאית בלי פרצוף, תנועות רגועות יותר.
- **יושמו כללי הפנים** על 4 התסריטים בתור (arena, brocoli, paraguas, frio_calor): "Both eyes stay open and calm…" בתקריבים ובשוטי מדיום; "laughing / big grin" → "smiling sweetly with his mouth closed". preflight עבר.
- מעקב: סה"כ 76 (פרק 1: 11→12). rescate עדיין private.

### Roy — 21.10.2026 ~23:15 UTC: הביקורת שלי הייתה מקלה מדי
- tito_mesa נדחה ל-TikTok: "יש בו מלא אי-דיוקים". כמעט כל הסרטונים שהועלו לא עברו ביקורת ותיקונים.
- **כלל חדש:** לטיקטוק רק סרטונים **חדשים** שעברו את תהליך הביקורת, כולל התיקונים. כל אי-דיוק שרואים = FAIL, לא "הערה קלה". אם אין סרטון מוכן — לא שולחים.

### Roy — 21.10 ~23:40 UTC: עוד דוגמאות לאי-דיוקים
- צלחת שנראית כאילו נאכלת / נעלמת; יד שמחוברת בצורה מוזרה לחדק כשהוא מחזיק מזלג עם החדק.
- נכתבה רשימת בדיקה מלאה `research/QC_CHECKLIST.md` (פנים, אנטומיה ואיברים שמתמזגים, חפצים שנעלמים, המשכיות, טכני) + כללי כתיבה. tito_brocoli תוקן: חפצים רק בידיים, החדק בצד, אכילה בשני שוטים.

### 22.10.2026 ~00:30 UTC — מחקר "רגע מסקרן" (בקשת Roy)
- Bebefinn ES: 19 מתוך 50 העלאות הם Shorts (חציון 2.5 מיליון מול 759 אלף לסרטון ארוך). כל Short הוא קטע של פרק ~3:20, ובתיאור: שאלה + קישור לפרק. Monito, Diana y Roma ו-TimoBoy — בלי Shorts.
- השיטה שלנו: "פותרים אחד, פותחים את הבא". תוכנית Shorts v2 ל-ep3 נכתבה ב-SCRIPT.md. פירוט: `research/15-teaser-strategy.md`.

### 22.10.2026 ~01:00 UTC — פרק Halloween (Roy: "מאוד אהבתי להתמקד בליל כל הקדושים")
- סריקה `longform_2026-10-21_halloween`: Wheels on the Halloween Bus 284K/day ×275; Babanana Dulces de Halloween 167K/day ×114; Pinkfong Sombras 141K/day.
- **tito_ep4_halloween** — "¡Toc, toc! ¿Quién es? 🎃" — 3 דלתות (חתלתול, עטלף, עכבר בלי סוכריות ← טיטו משתף). עדיפות 1, דדליין: פרק עד 27.10. preflight עבר; כל 18 השוטים בשימוש.
- תוקן באג ב-longform_scan.py (סרטון בלי duration).

### TikTok — Roy, 22.10.2026 (צילום מסך)
- סרטון הבריכה (tito_basura): **356 צפיות** ב-TikTok, מול ~4 ב-YouTube. 2 עוקבים, 5 לייקים.
- **מיקומים:** ניקרגואה 37.7%, הונדורס 28.6%, אל סלבדור 17.2%, ישראל 6.1%, ארה"ב 3.2%, קוסטה ריקה 1.9%, גואטמלה 1.2%. **קהל = מרכז אמריקה**, לא מקסיקו.
- **גילאים:** מבוגרים (35–44: 19%, 45–54: 9%, 55+: 6%) → ב-TikTok ההורים והסבים צופים.
- **מה זה אומר:** יש חשיפה ב-TikTok כבר מהסרטון הראשון. כיתובים ב-TikTok כותבים להורים ("para tus peques"). הספרדית — ניטרלית-מקסיקנית מתאימה גם למרכז אמריקה.
- **Roy:** תהליך חדש ב-Linear — לכל פרק משימה; כשהפרק עבר את כל הבדיקות שלי ויש תוכנית פרסום (כותרות ותיאורים ל-YouTube ול-TikTok), אני מסמן "מוכן ל-Roy".

### Roy — 22.10.2026 ~01:30 UTC
- **בלי יום המתים. כן לחג המולד** (כתיבה עד 25.11).
- **דדליין לפרק Halloween: 24.10, 18:00 שעון ישראל.** זה הפרק היחיד שבעבודה עכשיו.
- **תבנית מדויקת + בודק אוטומטי:** `research/EPISODE_TEMPLATE.md` + `research/template_check.py`. ep4 Halloween: תוקנו BKT (כפה בשוט שחוזר גם עם העטלף), V1/V2 (סוכריות בקערה), O2 (חדק). TEMPLATE OK + preflight OK. ep3 (כבר בהפקה, נכתב לפני התבנית) — 7 שוטים בלי כלל העיניים → לבדוק בביקורת.
- **לוח עבודה יומי קבוע** + שלב **"כתיבה ומחקר"** ב-Linear (Todo) — נוסף להוראות.

### Roy — 22.10.2026 ~01:45 UTC: בקרה על הסטודיו
- `production/agents/STUDIO_WORKFLOW.md` — תפקידים, סדר העבודה, זרימת פרק, כללים לשני הסוכנים.
- `queue.json`: שדות "now" (Halloween, דדליין 24.10 18:00 ישראל) ו-"next" (ep3, ואז ep2). ב-Linear: "▶ NOW" ו-"⏭ NEXT" בכותרות, ותקציר הפרויקט מראה NOW / NEXT / Ready.
- כשמשימה עוברת ל-In Review: התראה ל-Roy + קבצים.
- נשלחה הודעה לסשן של המפיק (priority "later" — לא עוצרת אותו) עם כל ההנחיות.

## Run 2026-10-22 06:05 UTC
- Momentum (videos.list): VocaVoca mealtime 659K/h, El Tren Ñam-Ñam manners 517K/h, Halloween costume 116K/h → manners/mealtime + Halloween both hot. Data: research/market/momentum_2026-10-22_0630.json
- QC #2 Halloween final edit (review mp4 v3): FAIL, 4 fixes (H02 squint + full bucket + extra object; 78–84s same; C1 feet smear; ending must be O2). Report: production/agents/research_reports/qc_2026-10-22/tito_ep4_halloween_final.md. Sent to producer.
- glitch_scan: seek + downscale + scene-cut filter.
- TikTok: nothing new reviewed → no package.

## Run 2026-10-22 08:05 UTC
- Halloween QC: v4 FAIL (3 fixes) → v5 FAIL (2 small: D2 door ≠ V2 door; M4 mouse sprout). Reports qc_2026-10-22/tito_ep4_halloween_final_v4.md, _v5.md. Producer re-taking. Linear ENG-14 commented.
- Organic watch 08:05: total 77 views across 14 Shorts, +1 since 00:05 (flat). All public. Confirms: old Shorts are not being pushed; the next growth test is the Halloween long episode + its Shorts.
- TikTok: no new reviewed video → nothing sent.

## Run 2026-10-22 10:05 UTC — algorithm research slot: Halloween titles (last 60 days, es)
Data: research/market/halloween_titles_2026-10-22.json
- **Closest proof for our episode:** Plim Plim "¡Veo, Veo Colores en Halloween! 🎃🚪 Juego de Puertas Sorpresa" — 2.38M views in 8 days, 3:08 long. Same mechanic as ours: doors + surprise guess.
- Question titles win: Pinkfong "¿Qué Hay en la Oscuridad?😱" 1.74M, "¿Dónde Está Mi Mamá?😭" 5.0M; Babanana "¡Aventura de Dulces de Halloween!" 3.1M.
- Healthy/teeth angle: Doctora Sophia "Dulces de Halloween vs Comida Saludable | Cepíllate los Dientes" 9.4M (Short) → our O1 toothbrush ending fits; use it in a Short caption.
- Title pattern: [question/exclamation] + 🎃🚪 + [game word: sorpresa/adivina] + "| Canciones Infantiles / Halloween para Niños".
- Draft episode title: "¿Quién está detrás de la puerta? 🎃🚪 ¡Dulce o truco con Tito! | Canciones Infantiles de Halloween"
- Timing: most Halloween winners were uploaded 26.9–14.10, and search peaks in the last week of October → our 24.10 upload is late but inside the peak week. Shorts on 25–27.10 are the main push.
- Status: Halloween v7 edit + ep2 v3 edit are in progress (producer); no new review copy yet. TikTok: nothing new reviewed.

## Run 2026-10-22 12:05 UTC (TikTok slot)
- Done since 10:05: research 17 (move/face library), 18 (TikTok lessons + vidIQ scan), sync_check.py; QC Halloween v7 (2 fixes → v8 has them + all cuts on the beat), QC ep2 v3/v3b (ep2 v3c in progress: white towel + beat snap done).
- Waiting: Halloween v8 review copy + 3 Shorts (not on origin yet; asked the producer).
- TikTok 12:00: no new reviewed video → nothing sent (rule: only new reviewed videos). The first package = Halloween Short A after QC.

## Run 2026-10-22 16:05 UTC
- Delivered: ep2 published (nWPm2InSAJo, 1 view after 3 h); Halloween FINAL + 3 Shorts sent to Roy (ENG-14 In Review); TikTok package #1 (ep2 handwashing) sent.
- ep3 keyframes v3: 3 fixes done → all 19 PASS; the producer is making clips.
- Organic: total 82 (+5; HxAYv-GieDM 4→8).

## Run 2026-10-22 18:05 UTC (TikTok + refine slot)
- ep3 FINAL + 3 Shorts + TikTok cut delivered to Roy (ENG-15 In Review).
- Refined: tito_brocoli → long episode v2 (28 lines, 19 shots, 3 pretend worlds: broccoli forest / carrot rocket / bouncy tomatoes, verse 3 = he tries by himself; habit beat = handwashing; design bible + START→ACTION→END). template_check + preflight OK. → queue NOW.
- TikTok: packages for ep2 + ep3 are with Roy; Halloween Shorts start 25.10.

## Run 2026-10-22 20:05 UTC
- brocoli: all 19 keyframes PASS (after 4 Mamá/I2 fixes); clips rendering. Waiting on Roy: Halloween (ENG-14) + ep3 (ENG-15) in In Review.

## Run 2026-10-23 08:05 UTC
- Halloween v9: 21 clips done, picks QC'd (M3 pour, O2 walk OK); BKT keyframe re-make pending (fallback: the v8 BKT). Review copy ETA ~11–12 UTC. Brocoli v2: 25 clips on main, producer reviewing.
- Scripts written overnight: rojito_arena v2 (Ruedas Locas), tito_paraguas v2 (Súper Tito), tito_frio_calor v2 (Puertas Mágicas), all template + preflight OK, waiting for Roy's OK.
- GPU balance .67 (Roy).

## Run 2026-10-23 10:05 UTC
- QC: Halloween v9 final candidate FAIL (BKTv9b s31: leg smoke, handle in the trunk, costume vanishes; the sharing slot PASS) → producer rendering BKTv9c (4 seeds). Brocoli v2 r1 → r2: K4/R1/R2/MO PASS; r2 O1 tail FAIL (bib leaf printed on the plate, trunk in the plate) → asked for TU/G1 fill.
- Scripts: deep pass (World design — deep, Shot bible, Sequence & punchline) on frio_calor, rojito_arena, tito_paraguas; new template §ט.
- Market scan (14 d): "hábito" titles ×36 vs without; comida ×5.7; colores ×0.34 (saturated).
- Outlier scan vehicles_rescue (60 d), top 5: Brigada Kids "Gato atrapado en un árbol" rescue 5.0M ×1698; Car Wheel Español "¿Qué figura necesita el camión de bomberos?" 5.6M ×200; RoboSquad "Superhero Bath Song" 1.8M ×202; Car Wheel "Autobús escolar — ruedas de formas extrañas" 5.0M ×181; Car Wheel "rueda con la forma equivocada" 2.3M ×81.
- Common: one clear problem in second 0 (a kitten stuck, a wrong wheel), a choice the kid answers, tactile color bursts (ball pools), 20–40 s Shorts.
- Rules: (1) the rescue problem goes in the title + thumbnail; (2) one tactile eye-candy burst per episode; (3) habit words in the title pay ×36.
- Applied: rojito_arena v2.3 (K1 ball burst, kitten-first title).

## Run 2026-10-23 12:05 UTC
- Delivered today: brocoli v2 + Halloween v9 (episode + 3 Shorts + TikTok each), QC PASS, both with Roy (ENG-14/ENG-18 In Review), waiting for his upload OK. GPU off ($4.75).
- Own channel: 83 views / 16 videos / 0 subs (+3 since 22.10 20:00). ep3 QFLm2ZcK8-w 1 view, Short A AsGbWnPNnAU 0 views after 4 h — still no organic push.
- Outlier scan hero_rain (60 d), top: Doctora Sophia "La Puerta Misteriosa de Colores" 238.7M ×180; Bebefinn "Equipo de Superhéroes, Vamos a Ayudar!" 20.2M ×55; Hokie Pokie "Cuando Papá Superhéroe No Está" 3.3M ×94; Niños Chaka "¡Un Amigo Superhéroe Ayuda a los Niños!" 1.88M ×190; RoboSquad "Superhero Bath Song" 1.83M ×198.
- Common: a visible transformation moment (spin + light burst into the hero costume), then quick small rescues; door = mystery + choice.
- Rules: (1) every hero episode gets a transformation flash shot (thumbnail frame); (2) door/mystery titles with a question.
- Applied: tito_paraguas v2.3 (H2 sparkle transformation), tito_frio_calor v2.3 (evidence + title/thumbnail). Fixed outlier_scan.py crash on videos without a duration (live/upcoming).

## Run 2026-10-23 14:05 UTC
- Waiting on Roy: upload OK for Halloween v9 + brocoli v2 (both delivered, QC PASS); a pick for the next episode (rojito_arena / tito_frio_calor / tito_paraguas / navidad). GPU off.
- Own channel: 83 views / 16 videos; ep2 nWPm2InSAJo 3, ep3 QFLm2ZcK8-w 1, Short A 0 — flat.
- Navidad scan (30 d): only Mundo Canticuentos (9.4M subs) posting villancico Shorts, best ×6.2 (85K). The season hasn't started for smaller channels → no outliers yet. Plan stays: Navidad episode ready by ~15.11, upload ~20–25.11, Shorts in December (2025 scan: the peak is 1–24.12).
- Rule: do not spend GPU on Navidad before Roy picks it; the evergreen concepts (Rojito ×1698 rescue, doors 238M) come first.

## Run 2026-10-23 16:05 UTC (production slot)
- Roy stopped the Halloween upload (14:20): the candy POUR looked unnatural → v10 hand-to-bucket. Clips failed twice (Wan pulls the trunk to the hand; candies landed outside) → solution = an INSERT close-up (hand + bucket only): vertical m3i_v s31 PASS (1.2–4.0); 16:9 insert keyframe re-roll pending (costume continuity).
- Roy: cropped verticals look too close → native 9:16 vertical Short approved (tito_ep4_halloween_vshort, 8 shots); keyframes QC'd (5 PASS, VM4/VC2/VC3 derived from passed frames).
- Rules added: QC §11 natural actions (hand transfers only, "would a real child do this?"); template §י native vertical Short; inserts are the fix when a character's face/trunk keeps interfering with a hand action.
- Channel: flat (see numbers). GPU balance ~$3.60.

## Run 2026-10-23 18:05 UTC
- Halloween v10 (hand-to-bucket insert) + the native vertical Short delivered to Roy (QC PASS, ENG-14 In Review); waiting for his upload OK + the Short A/B decision. Brocoli v2 waiting for his OK too. GPU $2.67.
- Script work: rojito_arena got its native vertical Short plan (§י): the ladder/kitten axis is naturally vertical — hook = the star-wheel kangaroo hops.
- 20:05: native vertical Short plans added to tito_frio_calor (beach jacket gag hook) and tito_paraguas (transformation hook). Still waiting for Roy (Halloween v10 + vertical Short upload OK, brocoli, next episode pick).
- 22:05: waiting for Roy (Halloween v10b + vertical option A upload OK; O2 jump-cut decision). Research only; no production actions (Roy: approval for every step).

## Run 2026-10-24 02:05 UTC
- Delivered overnight: Halloween v10b published (Eo_PHQrLDs0); Halloween TikTok (burned-in text) + vertical with Roy; brocoli v3b (Kling forest + rocket, §12 full pass) delivered, waiting for Roy's upload OK. Weave 227.5/230 used.
- Process changes (Roy): no Shorts — one TikTok per episode; QC §12 full-pass protocol; hashtag A/B rotation on TikTok.
- tito_frio_calor v3: the "mixed-up door" punchline (all weathers at once → clothes tower → rainbow party with the friends); stays in the plan, not in production.
- 04:05: waiting for Roy (brocoli v3b upload OK; next-episode pick). No production actions.
- 06:05: still waiting for Roy (brocoli upload OK, next episode). No production actions.
- 08:05: waiting for Roy. No production actions.
- 24.10 ~08:30: Roy: brocoli v3b approved as is (no changes), upload ON HOLD until he says. Status report sent (analyst meetings stopped after 22.10 20:47).
- 10:05 (24.10): TikTok2 '¿Quién es?' (Weave 161/180) in final edit fix (kitten squint cut, ~11.5 s). TikTok analytics logged (research/18). Brocoli on hold (Roy).
- 12:05 (24.10): TikTok2 delivered to Roy (QC PASS, 11.45 s, hashtag set B). Waiting for TikTok analytics at +24 h for both Halloween TikToks. Brocoli on hold.
- 14:05 (24.10): research 21 (TikTok winners decoded) done; waiting for Roy (Tito&Mamá micro-moment scripts?, TikTok analytics +24 h).
- 18:05 (24.10): research/22 competitor evolution (SKZ 2K→1.5M via "learn animal sounds" + baby/mamá pairs; YumYum flat at ~700 over 107 posts). New concept approved by Roy: "¿Cómo hace? Bebé y Mamá con Tito" (episodes/tito_como_hace/SCRIPT.md): a song that asks the child, REAL CC0 animal sounds (FSD50K per-clip license verified, production/sfx/animals/LICENSES.md; Roy approved both packs), cast = Tito's existing friends (ducks, kitten, mouse; owl, monkey for the YouTube full song). Waiting on Roy: Weave cap (550 Kling vs a MiniMax test first) + a server OK for the ACE-Step song. Mamá TikToks: M1 §12 FAIL as built (kiss trunk-on-face 0.75 s, eyes 0.33 s, set/bucket jump) → edit fix A (end at 7.09) requested; M2 → recommend drop. Weave 402.5/410.
- 20:05 (24.10): Be OK dance TikTok delivered (Kling Motion Control from Pexels 6940483, 8.4 s silent; Roy adds the sound in-app; QC PASS, energy moderate). The Halloween costume dance is parked (the MiniMax test was weak). como_hace: song take b1 (the only one of 12 passing the name/sound gate) + Demucs-built pauses + CC0 sounds → mix v2 80 s PASS (sounds +3…+7 dB over the bed, no silent tail); next = mamá designs + the MiniMax/Kling A/B. New research: Hugo el burrito (dance 4.3M / 88K shares; compilations 11.2M), trend lists Oct 2026 (Be OK, Ramalama costume walk). Weave: dance 191/250, como_hace 0/550.
- 22:05 (24.10) daily summary: como_hace in production (MiniMax won the A/B vs Kling: clean beak sync, fewer eye closures). Passed clips: P1a, P1b, P2a, P2b, P3a, P3b (with sync windows). Tito imitation i2v failed (laughs, eyes, a hands→paws body change) → T-shots become edit-animated stills (0 cr). Remaining: H1 + F1 + the F2 eye fix + F2 (~108.5) → ~494/550. Lessons: MiniMax > Kling for mouth-sync animal shots; i2v adds feathers/paws when the prompt says "like a duck/cat" → describe the human gesture, never the animal part; mamá "already in place" beats a walk-in. Be OK TikTok delivered (with Roy to post). Awaiting TikTok analytics from Roy.
- 00:05 (25.10): como_hace shorts v2 on HOLD (my QC): B1 filler grew paw pads; idle clips too static (near-freezes 0.3–0.5 s, H1 reused as filler) → the same "stuck" feel Roy rejected. Root cause = low-motion source clips; Weave 532/550. Options put to Roy: (a) ~4 dynamic clips per animal (waddle/hop/pounce, ~140/animal) or (b) pause the format and push the short formats that work (≤12 s: Be OK, M1). Kept: native 24 fps, beat-locked cuts, mix v3.
- 02:05 (25.10): waiting for Roy (como_hace: dynamic clips vs pause; posting Be OK + M1). No production actions.
- 04:05 (25.10): still waiting for Roy. No production actions.
- 06:05 (25.10) market scan (135 MFK Spanish toddler Shorts, 14 days):
  - comida ×8.4 (n=4, small sample).
  - gigante/sorpresa ×2.1.
  - 20–30 s is the strongest length on YouTube Shorts (40.7K views/day median); TikTok rule stays ≤12 s.
  - Rhythm QC (Roy refused both TikToks): Be OK v1 FAIL (silent, so the in-app sound can't sync; side-turn glitch). M1 FAIL (frozen hook; Tito's design changes at the cut).
  - Be OK v2 built by me (hits beat-warped onto our "Buenos días, Tito", 6.6 s, 0 credits), waiting for Roy's review. Roy DROPPED M1.
  - New QC rule: a dance clip must ship with its music burned in and hits on the beat (±1 frame); silent + in-app sound = FAIL.
- 25.10 (after 06:05): Roy posted Be OK on TikTok (v2, beat-synced). Ask for +24 h analytics. Compare with TikTok2 (8.3 s avg, 20.4% full).
- 25.10 ~07:30: Halloween dance TikTok (10 s, beat-locked, own chorus) posted by Roy. Weave 331.5. Pending: +24 h analytics for Be OK v2 and the Halloween dance.
- 08:05 (25.10): waiting for the +24 h TikTok analytics (Be OK v2, Halloween dance). No production actions.
- 25.10 ~10:20: Halloween dance YouTube Short uploaded with Roy's OK: https://youtube.com/shorts/_6ztnDmAFyg (MFK, links Eo_PHQrLDs0). Check at +48 h: views, Shorts-feed share, related-video traffic to the episode.
- Roy's screenshot of YouTube "trends for you" (Shorts sounds, 25.10):
  - Gangnam Style (PSY) 754K Shorts
  - Paparazzi 180K
  - Goo Goo Muck (the Wednesday dance) 141K
  - my sweetie (Jersey Club) 30K
  - Dame Hombro 12K
  - Ya Habebna 7.9K
  Candidates for Tito: Gangnam Style (the famous horse dance, kid-safe) and Goo Goo Muck (the Wednesday dance, spooky = Halloween).
  These are commercial songs: never burned in, only added in-app by Roy (YouTube's Shorts audio library). The rhythm lesson still applies: timing must be planned to the song's bpm and a known start point.
- 10:05 (25.10) algorithm question: can made-for-kids Shorts use commercial songs from YouTube's Shorts audio library? A web search found nothing conclusive (only 2020 COPPA reports that YouTube Music disabled features on 'made for kids' songs). Practical test: Roy opens the Shorts editor on the channel and checks whether 'Add sound' offers Gangnam Style. Waiting for Roy (Gangnam Style dance script?) and for the TikTok +24 h analytics.
- 12:05 (25.10): Halloween dance Short _6ztnDmAFyg at +2 h: 3 views, 1 like. The Halloween episode Eo_PHQrLDs0 has 5 views in total. Too early; re-check at +48 h. Waiting for Roy (TikTok analytics; Gangnam Style script yes/no; the Shorts-editor sound check).
- 14:05 (25.10): Short _6ztnDmAFyg 9 views at +4 h; episode Eo_PHQrLDs0 6 (+1). Still waiting for Roy (TikTok analytics, Gangnam Style yes/no).
- 16:05 (25.10): Short 9 views at +6 h (flat since 14:05), episode 6. No new input from Roy. Waiting.
- 18:05 (25.10): Short 9 / episode 6 (flat). No new input from Roy.
