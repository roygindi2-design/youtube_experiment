# QC 25.10: rhythm and odd parts (Roy: "not exactly in rhythm, odd parts, fit the music to the picture")

## Be OK (deliver/tito_baila_beok_tiktok.mp4, md5 7c605cff): FAIL
- **Root cause of "not in rhythm":** the file is silent, and the "Be OK" sound is added in the app. Nobody can line the dance up with it. The app's start point is arbitrary, and the dance has no steady tempo (hit gaps 0.27 to 0.67 s, mixing 150 bpm and 100 bpm).
- **Odd part:** at 2.8–5.4 s Tito turns to profile and then half-back, with a twisted head and foot shuffles. It reads as a glitch, not a dance move.
- **End:** 7.9–8.4 s, hands on mouth, then he stands still while the text fades. The energy drops at the loop point.
- **Fix (v2, edit only, 0 credits):**
  - Cut the turn.
  - Retime every hit (motion minimum = pose extreme) to land exactly on a beat of OUR song "¡Buenos días, Tito! ¡Ya salió el sol!" (tito_ep2, 112 bpm, song 2.438→8.986 = 12 beats; morning lyric = the 6 AM joke).
  - Source interpolated to 120 fps so the 0.7–1.2× retime stays smooth.
  - Music burned in; sync is guaranteed.
  - Script: episodes/tito_baila_beok/beat_warp.py.

## M1 Halloween (deliver/tito_ep4_halloween_tiktok_m1.mp4, md5 829098ec): FAIL, recommend drop
- **Frozen hook:** frame 0–0.5 s is effectively frozen (motion 0.2 vs 2.0 average). Shot 1 runs 3.8 s with almost no action, which is the exact pattern that lost 55% by 0:02.
- **Continuity break at the cut (3.82 s):** Tito jumps from big and centered to small at the left. His trunk goes from short to long, and the costume from a big pumpkin to a small one. It reads as a different character.
- **Music vs picture:** no move lands on the 110 bpm beat. The only event is the cut.
- **No edit-only fix:** shot 1 has no motion to retime, and shot 2 alone is 3.3 s of weak action. Drop it, or re-render with a matching design (credits, Roy's call).

## Decision (Roy 25.10)
- M1: dropped, per the recommendation. Not posted, no re-render.
- Be OK v2: waiting for Roy's review.
