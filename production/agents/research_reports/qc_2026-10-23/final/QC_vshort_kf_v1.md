# QC — Halloween vertical Short keyframes v1 (63507a4), 23.10

| shot | pick | verdict | note |
|---|---|---|---|
| VM1 | kf0 | PASS | sad mouse, EMPTY bucket, moon + lanterns; kf2 = backup |
| VM2 | kf0 | PASS | Tito's jack-o-lantern bucket with candies in his hand by the handle, the mouse's bucket empty, both whole |
| VM3 | kf0 | PASS (conditional) | palm up with candies, the mouse's bucket EMPTY ✓; the trunk tip curls just above the palm (no contact) and the hand is beside the mouse's head, not over the bucket. Motion must add: "he moves his open palm down over the middle of the yellow bucket, then tilts it". Clip QC: any trunk contact with candies / a candy landing outside = FAIL. kf1/kf2/kf3 FAIL (candy already in the bucket / trunk on the palm). |
| VM4 | — | all FAIL (bucket swap, mouse in a pumpkin costume) | **No new keyframe:** start VM4 from the LAST FRAME of the best VM3 clip (i2v), motion: "the mouse hugs its yellow bucket with the candies and jumps for joy once; Tito, kneeling, claps twice; both HAPPY SQUINT". Keeps who-holds-what exactly. |
| VC1 | kf1 | PASS | Tito's jack-o-lantern bucket in his hand, the mouse's bucket WITH candies (kf0's mouse bucket reads empty) |
| VC2 | — | all FAIL | Tito's bucket is a plain orange pail with no jack-o-lantern face, pressed against the costume (orange on orange = the "glued bucket"), the mouse's bucket empty. **Fix:** use VC1 kf1 as the VC2 start frame (same buckets), motion: "they turn to each other and each bow their head once on '¡gracias!'". |
| VC3 | — | all FAIL | the trunk tip at/on the candy in every one (+ Tito's bucket missing). **Fix:** re-roll: "Tito holds ONE wrapped candy in his open LEFT hand at chest height, held out to the side toward the mouse, far below his trunk; his trunk curled down against his chest; his jack-o-lantern bucket in his RIGHT hand by the handle"; or start from VC1 kf1 with the motion "each lifts one candy from their own bucket and shows it". |
| VC4 | kf0 | PASS | walking together from behind, both buckets in hand, both whole; kf1 = backup |

## Vertical clips (picks, 7405c02) — 3 fps + zooms
| clip | verdict | usable |
|---|---|---|
| VM1 s31 | PASS | 0.05–4.0 (sad → looks up; leaves falling). Slot is 5.455 s → add VM1 s19 0.2–1.6 (before its smear at 2.0) |
| VM2 s7 | PARTIAL | 0.05–1.5 only (standing, caring face). From ~1.6 he kneels INTO the mouse: his cheek overlaps the mouse's head, the trunk hangs in front of the mouse's face → FAIL after 1.5 |
| VM3 s31 | FAIL | the trunk tip lies on the candies on his palm from ~0.4 s → drop VM3; its slot = the vertical insert m3i_v s31 1.2–4.0 (2.8 s, ×0.86 speed to fill 3.27 s, or + 0.45 s of VM2 s7 0.05–0.5 before it) |
| VC1 s7 | PASS | 0.05–4.0 (dance, own buckets, candies in the mouse's) |
| VC1 s31 | PARTIAL | 0.05–1.6 (later Tito's bucket goes in front of his costume) |
| VC2 s43 | PASS 0.05–3.3 | ~3.6–4.0 FAIL: a huge orange leaf/smear crosses the left of the frame |
| VC3 s97/s111/s127 | all FAIL | Tito's orange jack-o-lantern bucket morphs into a YELLOW bucket (= the mouse's) and goes up to his trunk |
| VC4 s7 | PASS 0.05–3.0 | walking away together; after ~3.3 Tito's head turns into an odd shape |

Edit plan (33.8 s, cuts on the master's beat times): VM1 s31 + s19 → VM2 s7 (0.05–1.5, the rest of the slot = the first 0.7 s of the insert) → m3i_v s31 1.2–4.0 → VM4 (new seed A) → VC1 s7 → VC2 s43 0.05–3.3 + VC1 s31 0.05–1.6 → VC3 slot = VM4 seed B (another take) + VC1 s7 2.5–4.0 (2nd use) → VC4 s7 0.05–3.0 + VC1 s31 (≤2 uses). Every take ≤2×; slow-down never below ×0.85.
