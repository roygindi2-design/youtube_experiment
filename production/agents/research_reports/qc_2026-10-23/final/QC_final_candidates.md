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
