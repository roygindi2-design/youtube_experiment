# "¿Cómo hace? — Bebé y Mamá, con Tito" (24.10, Roy) — TikTok breakout test + YouTube full song
Why (research/22): SKZ went from 2K → 653K → 1.5M once it found "baby animal → small REAL sound → mamá → big REAL sound": a job for the parent (the kid learns and imitates), a predictable call→response rhythm, pastel solid backgrounds, a cute character big at frame 0, sound ≤1 s, a clean loop.
Roy's twist: it's a SONG that ASKS the child, the real sounds are part of the song, and **Tito is the host**, so TikTok viewers meet Tito and follow him to YouTube.
Rights: original melody + lyrics (NOT Old MacDonald / La Granja de Zenón). Animal audio = CC0 only (production/sfx/animals/LICENSES.md). Elephant toots = our own ACE-Step sfx.

## Funnel
- **YouTube (destination):** the full song, ~2:00, 8 pairs + Tito & Mamá. Ready BEFORE the TikTok goes up, so there's somewhere to send people.
- **TikTok (bait):** ~50 s cut: intro + 3 pairs + the Tito & Mamá finale. One TikTok per episode (template §יא).
  - Burned-in end text "🎵 La canción completa con Tito → YouTube: Cantilandia TV", plus the link in bio.

## Look (Tito's world, not generic AI animals)
- **Style:** the soft clay-toy 3D look of production/characters/tito_master.jpg. Rounded, matte, big glossy eyes, pink cheeks.
- **Animals:** in the same style, as if they lived in Tito's world: chunky, simple shapes, no realistic fur.
- **Background:** one solid pastel per pair (mint / peach / lilac / sky blue / butter yellow), with a soft floor shadow only. That's SKZ's winning backdrop and also Tito's master backdrop.
- **Tito:** canon outfit: blue elephant, yellow overalls with orange buttons, blue tuft on his head.
- **Mamá:** canon: lilac polka-dot dress, white apron, yellow flower.
- **QC rules baked in:**
  - Eyes open (except a ≤0.3 s blink).
  - Mamá animals walk in from the RIGHT only and stop: one direction.
  - No props, no touching between characters, no trunks near faces.
  - Every character fully visible and big in frame.

## Song: 110 bpm, 4/4, cheerful kids' pop (marimba, ukulele, claps); voice = warm female kid-show singer + kids' chorus on the answers
Each pair = 6 bars (~13 s). The same frame repeats so toddlers learn it after one pair:
| bar | sung | on screen |
|---|---|---|
| 1 | "**[Bebé] chiquitito, ¿cómo haces tú?**" | the baby animal, big, centered, looks at the camera |
| 2 | *(music drops to a soft pad: the child answers)* → **REAL baby sound** on beat 3 | the baby makes its sound (mouth/beak moves) |
| 3 | "**¡[sonido] x3! ¡Muy bien, [bebé]!**" (kids' chorus) | cut: **Tito** close-up imitating it with his trunk raised, giggling with eyes open |
| 4 | "**¿Y su mamá? ¿Cómo hace? ¡A ver!**" | the baby looks to the right; the mamá walks in from the right and stops beside it |
| 5 | *(soft pad)* → **REAL mamá sound** on beat 3 | the mamá makes the big sound; the baby looks up at her |
| 6 | "**¡[sonido]! ¡Así hace mamá!**" | both side by side, happy, a small bounce |

### TikTok cut (~50 s)
| time | what |
|---|---|
| 0.0–1.6 | **HOOK.** Frame 0: Tito CLOSE-UP on mint, already acting: trunk cupped to his ear, eyes wide. At 0.3 s a REAL chick "pío" off-screen; Tito's eyes dart right, surprised. Text 0–3 s: "¿Tu peque sabe cómo hace cada animal? 🐣🐑🐶" |
| 1.6–14.7 | **Pair 1: pollito / gallina** (peach). Sounds "¡Pío, pío, pío!" / "¡Co, co, co!". Audio: CC0 #13 chicks, #14 hen |
| 14.7–27.8 | **Pair 2: ovejita / oveja** (sky blue). "¡Beee!" / "¡Beee!" (deep). Audio: CC0 #3 lamb calling its mother, #4 ewe answering (a real pair) |
| 27.8–40.9 | **Pair 3: perrito / perrita** (butter yellow). "¡Guau, guau!" (tiny) / "¡Guau, guau!" (big). Audio: CC0 #17 small dog, #16 big dog |
| 40.9–51 | **Finale: Tito / Mamá** (lilac). Bar 1 "Y Tito chiquitito, ¿cómo haces tú?" → Tito raises his trunk: a small "tu-tu-tuuu!" (our sfx). Bar 4 "¿Y su mamá?" → Mamá walks in from the right, stops BESIDE him (no contact) → big "¡TUUU!". Bar 6 "¡Así hace mamá!" → both trumpet together, trunks up and away from each other's faces. End text 47–51 s: "🎵 La canción completa con Tito → YouTube: Cantilandia TV" |
| loop | the last bar's chord resolves into the intro → Tito cups his ear again |

### YouTube full song (~2:00)
The same intro + 8 pairs, in this order:
1. pollito
2. ovejita
3. perrito
4. gatito
5. patito
6. cerdito
7. becerrito
8. chivito

Then the Tito & Mamá finale and an outro chorus "¡Bebé y mamá, todos a cantar!".
- Pairs without a real baby recording: the baby = the adult CC0 clip pitched up +5…+7 semitones (CC0 allows edits).
- Roy picks the final sound per animal from the listening pack.

## Parent-voice text and caption
- **Caption (search-first, Spanish):** "SONIDOS DE ANIMALES PARA NIÑOS 🐣🐑🐶 | ¿Cómo hace el pollito? | Canción infantil con Tito el elefante | Bebé y mamá | Aprende los sonidos de los animales"
- **Hashtags:** set B (Spanish) + 2 from set A (research/18 A/B still running).
- **Pinned comment idea:** "¿Cuál animal quieres la próxima vez? 👇" (it worked for SKZ: "which animal next?").

## Production (no Weave: our RunPod pipeline, needs Roy's OK for GPU spend)
- **Keyframes:** Klein 4B with tito_master / mama_master refs. Single centered characters on solid pastel = the easiest shots we have, no hands or props.
- **Clips:** Wan 2.2 i2v, 5 s each, minimal motion: walk-in, beak/mouth open, bounce.
  - TikTok cut ≈ 14 clips; full YouTube ≈ 30 clips (the Tito imitation shots can repeat with different expressions).
- **Song:** ACE-Step with `[instrumental]` tags on bars 2 and 5.
  - Generate 6 takes. research/sync_check + an energy-gap detector pick the take whose breaks land on bars 2/5.
  - Fallback: duck the music −8 dB under the real sound for 1.2 s.
  - Real sounds mixed so they're clearly the star: −3 dB under the vocal peak, loudness-matched (pack already normalized).
- **QC:** the §12 full pass at 8 fps per character. The sound must hit when the mouth/beak opens (±80 ms).
