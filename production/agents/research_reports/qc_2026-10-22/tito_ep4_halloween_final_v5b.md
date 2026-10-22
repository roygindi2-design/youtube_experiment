# QC #4b — tito_ep4_halloween v5: MOTION review (Roy's notes 22.10 + research/motion_check.py)

Roy watched the episode and found what my frame-sheet QC missed: boomerang (ping-pong) loops, frozen moments, walking in place, a weird trunk. A still frame sheet cannot show these — I added research/motion_check-style analysis (per-segment loop count) and these are now FAIL rules.

## Verdict: FAIL — motion problems (in addition to the 2 fixes in _v5.md)

### A. Ping-pong / boomerang (looks "stuck") — segments where frames repeat back and forth
(loop-frame count per segment, 30 fps; >5 = visible)
| start s | len | shot | loop frames |
|---|---|---|---|
| 0.0 | 6.4 | H01 | 38 |
| 10.8 | 3.7 | D1 | 22 |
| 16.7 | 3.6 | V1 | 31 |
| 27.8 / 62.4 / 101.3 | 4.2 | C2 | 23–26 |
| 32.0 / 66.6 / 105.5 | 6.3 | C3 | 36–41 |
| 40.3 / 74.7 / 113.5 | 3.1–4.1 | C4 walk | 13–20 |
| 44.7 | 4.2 | D2 hand | 11 |
| 48.9 | 2.7 | Q | 10 |
| 77.8 | 6.1 | Q (instrumental) | 46 |
| 83.9 | 4.0 | M1 | 9 |
| 120.2 / 138.1 | 1.6 | M4 | 9 |
| 122.9 | 4.2 | O1 | 21 |
**Rule from now: NO ping-pong at all.** Fill a long line with: a longer clean take, a 2nd take/seed of the same shot, a different angle (cutaway), or speed 0.85–0.9x. A natural slow blink is OK (Roy's complaint was eye *pops/jumps*, not real blinks) — so windows can be longer.

### B. M4 chopped into 0.8 s pieces (93.4–97.0, 117.0–122.9, 134.8–140.8) → flicker/jumpy. Use one continuous 3–4 s take.

### C. Frozen / almost no motion
| time | shot | motion |
|---|---|---|
| 20.2–23.6, 54.1–58.3 | BKT bucket | static 3–4 s after the candy lands |
| 87.9–93.4 | M2/M3 | very low |
| 127.1–134.8, 140.8–148.7 | O2 | ~8 s each, Tito and mouse barely move |
Fix: shorter holds (≤2 s) or a take with gentle motion (waving, mouse skipping away, leaves falling, camera slow push-in).

### D. Walking in place — C1 and C4: Tito "walks" but the street doesn't move.
Fix: prompt "camera slowly tracking backwards as he walks toward the camera, houses passing by on both sides", or walk ACROSS the frame (left→right) so he really travels.

### E. Trunk — C1 dance (23.6–27.8, 58.3–62.4, 97.0–101.3): the trunk curls UP and sticks to his left cheek (Roy's screenshot). Spec rule: trunk hangs down below the mouth, never touches the face. Re-take C1.

(Roy's other screenshot — bat with one bat ear + one elephant ear — was v4; v5 already has a real bat ✅.)

Order of work (deadline 24.10 15:00 UTC): C1, C4 (in 3 choruses ×3 = biggest screen time) → O2 → H01/V1/D1/Q → M4/BKT → C2/C3 → O1.
