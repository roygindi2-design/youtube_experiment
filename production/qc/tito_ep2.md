# QC sign-off: tito_ep2 — "Un día con Tito" (פרק ארוך 2, 16:9, 88 ש') — 21.10.2026
- מצב במאי: 36 keyframes → 18 נבחרו; 36 קליפים 960x544. עריכה לפי זמני מילים; השיר (s8, Whisper 0.93) קוצר: 3.2–86.5 + 115.4–120 ("¡Buenas noches, a soñar!") — בלי 30 ש' של כלי ריק.
- QC אוטומטי: FAIL ב-E01 (טיטו רץ למצלמה), E08 (בוץ), E12/E18@7 — נבחרו seeds נקיים / נבדק ויזואלית. בלי הקפאות; חזרות = ניגון לאחור.
- מבנה: בוקר (ידיים, ארוחה) → אמבטיה (בוץ, בועות, מגבת) → שיניים → לילה (סיפור, נשיקה, שינה) → פזמון אחרון עם חזרה על כל ההרגלים.
**PASS**

## Fix v2 — 21.10.2026 (Roy approved GPU for this episode)
- 5 new shots: E19 wake-up (s19), E20 sunrise (s19), E21 mud jump (s7, 2 s), E22 muddy face (s7, 2 s), E23 pajamas with Mamá (s19, instrumental 55.8–59.8).
- Auto QC: E20 s19 PASS; others REVIEW/FAIL by metric → high-res strips checked by eye: no morphs, no extra characters, character consistent. E23 s7 rejected (glow flash on trunk).
- Opening now matches lyric "¡Buenos días, Tito! ¡Ya salió el sol!"; mud shots match "Barro en las orejas…".
- Final: 1920x1080, h264+aac, no subtitle stream, 87.9 s. **Not uploaded via API — Roy uploads manually.**

## Fix v3 — physics (Roy 21.10: "bath and mud puddle look like a still picture")
- Replaced: E04 → E04N (real sink, running water into the basin), E21 → E21F (full Wan 2.2 5B, 30 steps: splash rises and falls, puddle ripples), E09 → E09F (full model, edited keyframe: no overalls, water spray falls back), E10 → E10N (no overalls, bubbles float away), E18 → E18N (moon closes eyes, Tito sleeps; no morph).
- Measured motion (optical flow, bottom third): mud 0.58 → 2.52, bath 0.38 → 1.27, sink 0.96 → 1.30.
- Lesson: the full (non-distilled) Wan 2.2 5B gives much better liquid physics than FastWan; use it for splash/water shots (≈4 min/clip on 4090).
- Final: 1920x1080, no subtitle stream, 87.9 s. Not uploaded via API.

## Fix v4 — trunk (Roy 21.10: "in the towel-dance shot his trunk just disappears")
- Both old E12 takes (FastWan) shrank the trunk to a small nose for ~2 s. All 3 new FastWan takes did the same.
- Replaced with E12F (full Wan 2.2 5B, motion prompt says the trunk stays visible and swings) at 38.3–39.8 (in 2.5) and 51.8–55.8. Trunk visible in every frame.
- Whole episode scanned at 2 fps: no other trunk loss.
- Lesson: FastWan tends to "lose" the trunk in dance/turn shots; use the full model for character dance shots too.
