# QC — final candidates (commit 4cbce6d), 23.10

## Halloween v9 review — FAIL (1 issue, 2 slots)
- Auto: 0 ping-pong, 0 static, cuts on beat 40/40 = 100%, 0 black. ✓
- Slot 133.78–138.69 (M4v9 s19 + s31): Tito + the mouse together, sharing, candies, both faces OK. **PASS** (hw_slot_pass.jpg).
- **BKT = BKTv9b s31 at 21.41 and 54.69 — FAIL** (hw_bkt_legs_smoke.jpg, hw_bkt_costume_lost.jpg):
  1. ~21.8–22.6: grey smoke wisps rise from his feet, the legs turn half-transparent.
  2. The bucket handle runs up INTO the trunk/mouth (looks like he bites the handle).
  3. ~23.6–23.9: the pumpkin costume vanishes — a bare blue belly, the face smudged, one eye blurred.
  4. The bucket merges with the costume (orange on orange, one blob) in several frames.
  Fix: render the BKTv9b clip with other seeds (7/19/43/97) and pick one with no smoke, the handle in his HANDS below the trunk, and the costume kept the whole time; or replace both slots with a cutaway (the D2 door / candy-bowl shot) if no seed passes. Then I re-check at 5 fps.

## Brocoli v2 review — FAIL (small, trim-level)
- Auto: 0 ping-pong, 0 static, 0 black. Sync 63% by the tool; I accept the explanation (42 real cuts on the 110 bpm grid, the extra hits are in-clip motion).
- R1 12.06 / R2 52.54: front-facing, both eyes, trunk OK. **PASS**.
- K4 42.3 (and the same fix take at 81.6/119.8): Mamá's trunk rests on Tito's head, the two trunks stay apart, Tito's trunk down. **PASS** (bro_k4_pass.jpg).
- MO 124.7–126.0 (carrot to the monkey): **PASS**.
- **MO2 ~127.5–128.6 — FAIL**: Tito's trunk lies down on the plate rim and merges with it as the plate goes to the basket (bro_mo2_trunk_plate.jpg). Fix: end MO2 at ~127.4 (before the trunk reaches the plate) and fill the rest with the TU toucan cutaway or the next take.
- **~126.9–127.0 — FAIL (1–2 frames)**: a red-white smeared butterfly flashes at the right edge (bro_butterfly_flash.jpg). Fix: it falls inside the MO→MO2 area: shift that cut so the flash frames are out, or trim them.

## Brocoli v2 review r2 (d460d09) — FAIL (one slot)
- Auto clean (0 ping-pong, 0 static, 0 black). The butterfly flash is gone ✓, MO 124.7–126.0 still PASS.
- **The new v1 O1 s57 tail ~127.2–128.4 — FAIL** (bro_r2_o1tail_fail.jpg): the green leaf from Tito's bib is printed on the plate (the plate merges with the bib), and at the end the trunk tip lies inside the plate again.
- Fix: no plate close-up in this slot. Fill ~126.0–128.6 with a clip with no plate/trunk contact: a TU toucan seed not used yet (s7 and s19 are each already at 2×), or a reaction/wide shot (e.g. G1 another seed). Then send r3 for a 5 fps look.

## Halloween v9 c44c2b8 (BKTv9c s97) — FAIL, trim-level
- Auto clean (0 ping-pong/static/black, 40/40 on the beat). No smoke, the costume stays on, the bucket stays a separate shape ✓.
- **FAIL:** the trunk goes down INTO the bucket, crosses the rim and sits in the candies (hw_bktv9c_trunk_in_bucket.jpg): ~21.9–23.5 and ~55.2–57.1. The start (trunk above) and the end (trunk lifted out) are clean.
- Fix (no new render): keep BKT s97 only before and after the trunk dip, and put a ~1.6–1.9 s cutaway in the middle, cut on the beat (110 bpm grid): the candy bowl / D2 door neighbour, or the bat at the door. Slot 1: BKT 21.41→~21.95 | cutaway | BKT ~23.6→end. Slot 2: BKT 54.69→~55.23 | another cutaway take | BKT ~57.1→end. Each cutaway take ≤2×.
- Shorts A/B contain the same BKT → re-cut them from the fixed master.
- Short C (sharing scene): pour + bucket in frame ✓; at ~11–14 s the mouse is half outside the right edge (minor): shift the crop toward the mouse there if Tito still fits. Short A ends on the D2 knock cliffhanger ✓; Short B ends on the mouse with the empty bucket ✓.

## Brocoli v2 r3 (103de51) — PASS
- 126.3–128.6 K3 v2 s83 joy: clean (no plate, no trunk contact).
- Full 2 fps pass + zooms: no new issues. Minor: the bib icon is an orange in the tomato close-up (100–103.5), a leaf elsewhere. Not blocking.
- Next: deliver copy + Shorts A/B/C + TikTok A → my QC → Roy.

## Brocoli v2 Shorts (2bf55b4)
- Auto (all 4): 0 ping-pong, 0 static, 0 black; 1080x1920.
- Short A (ends on R2): PASS. Short B (ends on R3): PASS. TikTok A (refusal → broccoli forest, 13 s): PASS.
- **Short C — FAIL (one shot):** ~16–20 s, Mamá hands Tito the plate: the pan between them leaves a floating blue arm with no body in frame (~17 s), then Tito's head half behind Mamá's trunk, both faces cut (bro_shortC_plate_crop_fail.jpg). Fix: hold the crop still on Tito for this shot (his whole head + the plate arriving, x≈0.35–0.40), no pan. Minor: the K3 joy close-up (~37 s) loses the raised arms in the vertical crop — acceptable.
- Short C re-cut (ca96c88): the plate shot held at x0.38 — Tito's whole head, his arm attached and reaching to the plate, no floating limbs, no pan. **PASS.** All 4 brocoli verticals PASS.

## Halloween v9 35d27b7 (BKT trim with BOWL cutaways)
- Auto clean (0 ping-pong/static/black, 44/44 on the beat). Slot 1 (21.41–24.14): PASS — the bowl cutaway hides the trunk dip, the s97 end keeps both hands on the bucket.
- ~56.0: a falling autumn leaf crosses the bowl shot (2 frames, slightly smeared) — reads as a leaf, OK.
- **Slot 2 tail ~57.9–59.05 (s97 2.85–4.0) — FAIL:** Tito opens his arms out to the sides and the bucket stays stuck on his tummy with no hand holding it (= Roy's "glued bucket") (hw_slot2_tail_glued_bucket.jpg). Fix: end the s97 tail at 2.85 like slot 1 (hands still on the bucket), and fill the remaining ~1.15 s by extending the BOWL s7 cutaway or with another clean take, cut on the beat.

## Halloween v10 M3 keyframe (49c2800) — FAIL (both)
- Trunk: clear of the candies in both (alt better: trunk higher, tip above the wrist) ✓. Bucket set down ✓, mouse holds its empty bucket ✓.
- **FAIL:** Tito's hands are mittens (no fingers), so the candies look GLUED to the side of the hand, not held (hw_m3_v10_kf_hand.jpg). The hand is also high and off to the left edge of the yellow bucket, not over its opening.
- Fix (natural for mitten hands): **palm UP, a few candies RESTING on the open palm**, the hand low (about a hand's width above the rim) and centered over the yellow bucket's opening; the mouse holds the bucket up with both paws. Motion: on '¡Toma!' he tilts his palm and the candies slide off into the bucket; his hand returns to his knee. Trunk curled down against his chest, nowhere near the hand.
- Round 2 (ad85370): **PASS.** Palm up, 3 candies resting on the open palm (natural), the hand low over the left half of the yellow bucket's opening; trunk curled against his chest, far from the hand; his bucket on the ground; the mouse holds its empty bucket with both paws. Clip QC focus: every candy lands INSIDE the yellow bucket (none outside, none floating), the trunk never reaches the hand/candies, the hand stays one shape (no melting), the mouse's paws stay on the bucket.

## Halloween M3 v10 clips (ed9dd60) — all 4 FAIL
- s43 (hw_m3v10_s43_fail.jpg): the palm with the candies is at the mouse's HEAD height, far above the yellow bucket; ~1.4 s the trunk swoops down onto the hand (trunk + arm merge); the candies fall in front of the mouse and onto the ground — NOT into the bucket. Even 0.05–1.2 shows no giving.
- s19: the trunk slides down along the arm to the palm from ~0.5 s and touches the candies. s7/s31 FAIL (producer).
- Root cause: Wan pulls the trunk to any hand action near the face; the keyframe hand was too high.
- **Fix = an insert shot (no trunk in frame):** M3 slot 90.69–93.96 = M3a: s43 0.05–1.0 (Tito holds out his palm with the candies, smiling — before the trunk moves) + **M3i (new):** a close-up INSERT at the bucket's height: only Tito's powder-blue hand (palm up, 3 wrapped candies) above the mouse's small yellow bucket held by its grey paws; motion: the palm tilts and the candies slide into the bucket one after another, landing inside; ~2.2 s. No face, no trunk in the frame. Then M4 as before.

## M3i insert clips + h2 keyframes (23.10 ~16:00)
- **Vertical m3i_v s31 — PASS, window 1.2–4.0 s:** the palm moves over the bucket, tilts, the candies drop straight IN and stay in the bucket; the empty palm opens above; the paw holds the rim. 0–1.0 s FAIL (an orange candy flies through the sky) → never use before 1.2.
- v s7 FAIL: candies arc sideways, one hovers in the air ~1 s and bounces back up out of the bucket. v s19/s43 FAIL (producer).
- **16:9 m3i_h2 kf2 — FAIL (continuity):** Tito's body at the left edge is plain blue — NO pumpkin costume; the mouse at the right has a white body — NO yellow star costume. kf0/kf1 FAIL (producer).
- Fix: re-roll h2 with "only Tito's powder-blue hand and forearm entering from the LEFT edge (nothing else of him); the mouse's grey arm in its YELLOW star costume sleeve from the RIGHT, its paw on the rim; the mouse's face partly visible at the right edge above its yellow star costume; the palm low, right above the middle of the bucket". h0 clips: not needed.
