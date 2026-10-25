# TikTok: "¡Tito baila en Halloween!" (Roy approved 25.10: Halloween dance, 170 Weave credits)

**Goal:** TikTok views before 31.10. One shot of Tito in his pumpkin costume dancing a real kid's dance (motion transfer), every hit on the beat of OUR Halloween chorus, music burned in.

**Why (data):**
1. Character dances are the competitor outliers: Hugo el burrito dance 4.3M views / 88K shares (research/22 §F).
2. Our best TikTok so far is ≤12 s: TikTok2 11.46 s got 20.4% full and 8.3 s average. Halloween v1 at 28 s got 4.6–5.7% (research/18).
3. Halloween search and feed peak 25–31.10.
4. Be OK v2 proved the pipeline: motion transfer + beat warp, 0 extra credits for the edit.

## Pipeline (same as Be OK v2)
1. **Keyframe** (Nano Banana, 3.5 cr; up to 2 tries = 7). Spec:
   - Vertical 9:16. Tito full body, centered, his height about 45% of the frame, with headroom and floor room for the jumps.
   - Same design as the Halloween episode, ref kf/pick_C1.jpg: blue baby elephant, big pink-lined ears, short trunk, round orange pumpkin costume on the body with a green stem cap on his head.
   - **Arms and legs free and visible.** Face and both ears fully visible.
   - Standing, facing the camera, arms relaxed at his sides, happy, eyes open.
   - Halloween village street at night: moon, string lanterns, glowing jack-o'-lanterns at the sides, a few leaves on the ground.
   - No bucket, no other characters. Static camera.
2. **Motion Control** (Kling Motion Control V3.0 Pro, ~164 cr; character_orientation "video"):
   - Image = the keyframe.
   - Driving = Pexels 7697117, 0–10 s (free commercial use, edits OK, no attribution). Vertical 1080×1920 at 30 fps, one boy, full body, front-facing.
   - Moves: a running jump-in, kicks, leg swings, then footwork with arm swings. 0–3 s is the most energetic part (motion 5–6 vs 2.5 later).
   - Hits every ~0.37 s on average (measured).
3. **Edit** (0 cr), episodes/tito_baila_beok/beat_warp.py adapted:
   - Detect hits (motion minima) on the GENERATED clip.
   - Interpolate the clip to 120 fps.
   - Retime so every strong hit (jump landings, kick ends) lands on a beat of the Halloween master (production/episodes/tito_ep4_halloween/assets/song.wav, 108–110 bpm).
   - Speed range 0.75–1.3×. Cut any segment that needs more.
   - Music = the chorus "¡Dulce, dulce, Halloween! … ¡Gracias, gracias, qué feliz!" (song ≈20.4–30.3 s; snap both ends to beats; words: assets/song_words.json).
   - Frame 0 = Tito already moving with the chorus downbeat (no intro).
   - Length 8–10 s; loop-friendly end (cut mid-move on a beat).
   - Text, burned in, Lilita (production/tiktok_text.py), top, 2 lines max, on beat boundaries:
     - 0–~3 s: "Mi peque cuando escucha 'Halloween' 🎃💃"
     - Then: "…y no lo para nadie 😅"
4. **Total credits:** 7 + 164 = 171 at most. Within Roy's 170 approval only if the first keyframe passes; a 2nd keyframe try needs a 1-credit OK from Roy.

## QC (strict, research/QC_CHECKLIST.md + 25.10 rhythm rules), any visible defect = FAIL
- Same design all through: trunk length, ears, costume size and stem cap. No extra legs or arms on kicks and jumps, and no limbs merging into the pumpkin.
- Face and both ears visible the whole time. Eyes open (blinks OK, no long closures).
- The motion in frame 0–0.5 s is ≥ the clip average.
- Every strong hit is on a beat (±1 frame). Music burned in.
- No turn to profile or back with a twisted head (the Be OK v1 glitch). Cut such parts on a beat.
- No ghosting from the interpolation (check full-resolution frames at the fastest kicks).

## Caption (Spanish, parents)
"¡Así baila Tito cuando llega Halloween! 🎃💃 ¿Tu peque también se emociona así? 👇 Canción completa en YouTube: Cantilandia TV #halloween #mamás #bebés #crianza #toddler"

## Rights
- Driving video: Pexels license.
- Music: our own song.
- No trending commercial sound burned in. Roy may add one in-app at low volume only if he wants; the burned-in sync stays primary.
