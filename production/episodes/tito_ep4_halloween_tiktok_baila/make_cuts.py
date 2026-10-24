"""TikTok "¡No me cabe… y BAILA!" (Roy 24.10; SCRIPT.md). 9:16 loop: STUCK -> POP -> a hard cut on the chorus drop into the
DANCE clip (Kling i2v from review/tiktok_baila/dance_first_frame.jpg = m1_s2_fl @ 3.30, the POP out point) -> loop.
Audio: master beats 0-11 (0.14-6.685, the intro) + from beat 44 (24.14 = "¡Dulce! ¡Dulce, Halloween!", where the
energy comes back after the "¡Dulce o truco!" breakdown). 12 + 44 are both bar starts, so the bar phase holds.
A synthesized POP (no samples needed) on the cut STUCK -> POP. Without the dance clip it builds the 12-beat draft only.
    python production/episodes/tito_ep4_halloween_tiktok_baila/make_cuts.py && python production/edit_cuts.py <cuts.json>
"""
import json
import subprocess
from pathlib import Path

D = Path(__file__).parent
H = D.parent / "tito_ep4_halloween"
WM = D.parents[1] / "review" / "tiktok_mama_weave"
WB = D.parents[1] / "review" / "tiktok_baila"
B, BEAT0 = 60 / 110, 0.14
import os
DANCE = WB / os.environ.get("DANCE", "dance_kling.mp4")
DANCE_BEATS = int(os.environ.get("DANCE_BEATS", 18))  # 18 = 9.82 s of a 10 s clip; ends mid back-wiggle -> loop
W = {"STUCK@0": (0.05, 3.32), "POP@0": (0.05, 3.32), "DANCE@0": (0.05, 0.05 + DANCE_BEATS * B)}
plan = [("STUCK@0", 6), ("POP@0", 6)] + ([("DANCE@0", DANCE_BEATS)] if DANCE.exists() else [])
cuts, t = [], 0.0
for tok, beats in plan:
    e = round(t + beats * B, 3)
    i, u = W[tok]
    need = e - t
    if (u - i) < 0.85 * need - 1e-6:
        raise SystemExit(f"{tok} needs {need:.2f}s, has {u - i:.2f}s")
    cuts.append([round(t, 3), e, tok, {"in": i, "until": round(min(u, i + need), 3)}])
    t = e
src = D / "build" / "vsrc"
src.mkdir(parents=True, exist_ok=True)
for k, f in (("STUCK_s0", WM / "m1_s1_fl.mp4"), ("POP_s0", WM / "m1_s2_fl.mp4"), ("DANCE_s0", DANCE)):
    l = src / f"b_{k}.mp4"
    if l.is_symlink() or l.exists():
        l.unlink()
    if f.exists():
        l.symlink_to(f.resolve())
# audio: intro beats 0-11 + chorus from beat 44, a 20 ms crossfade on the beat; + the POP at the STUCK->POP cut
a0, a1, c0 = BEAT0, BEAT0 + 12 * B, BEAT0 + 44 * B
c1 = c0 + max(0.0, t - 12 * B) + 0.5
wav = src / "audio.wav"
pop_at = 6 * B
FX = D.parents[1] / "sfx" / "foley"  # CC0 (LICENSES.md there)
# foley (researcher 24.10): 3 short costume squeaks on the STUCK wiggles (-12 dB), the POP on the cut with the music ducked
# -4 dB for 150 ms, a toddler giggle right after the POP (-6 dB)
squeaks = [(0.75, "fsd_128331.wav", 0.10), (1.85, "fsd_128332.wav", 0.20), (2.70, "fsd_128316.wav", 0.40)]
fx_in = [x for t_, f, _ in squeaks for x in ("-i", str(FX / f))] + ["-i", str(FX / "fsd_416702.wav")]
music = (f"[0]atrim={a0:.4f}:{a1 + 0.02:.4f},asetpts=PTS-STARTPTS[a];"
         + (f"[0]atrim={c0:.4f}:{c1:.4f},asetpts=PTS-STARTPTS[c];[a][c]acrossfade=d=0.02:c1=tri:c2=tri[m0];" if DANCE.exists() else "[a]anull[m0];")
         + f"[m0]aformat=sample_rates=44100:channel_layouts=stereo,volume='if(between(t,{pop_at:.3f},{pop_at + 0.15:.3f}),0.63,1)':eval=frame[m];")
fx = ""
for n, (at, _, ss) in enumerate(squeaks, start=1):
    ms = int(at * 1000)
    fx += f"[{n}]atrim={ss}:{ss + 0.30},asetpts=PTS-STARTPTS,afade=t=out:st=0.22:d=0.08,aformat=sample_rates=44100:channel_layouts=stereo,volume=-12dB,adelay={ms}|{ms}[s{n}];"
g = len(squeaks) + 1
gms = int((pop_at + 0.25) * 1000)
pms = int(pop_at * 1000)
fx += (f"[{g}]aformat=sample_rates=44100:channel_layouts=stereo,volume=-6dB,adelay={gms}|{gms}[g];"
       "aevalsrc='0.55*sin(2*PI*(700-5500*t)*t)*exp(-38*t)+0.25*(random(0)-0.5)*exp(-120*t)':s=44100:d=0.12,"
       f"aformat=channel_layouts=stereo,adelay={pms}|{pms}[p];")
mix = "[m]" + "".join(f"[s{n}]" for n in range(1, len(squeaks) + 1)) + f"[g][p]amix=inputs={len(squeaks) + 3}:duration=first:normalize=0[o]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(H / "assets" / "song.wav"), *fx_in, "-filter_complex", music + fx + mix,
                "-map", "[o]", str(wav)], check=True)
out = {"out": str(D / "build" / os.environ.get("OUT", "tito_ep4_halloween_tiktok_baila.mp4")), "song": str(wav), "song_start": 0.0, "fade_out": 0.0 if DANCE.exists() else 0.15,
       "size": [1080, 1920], "clips": str(src / "b_"), "cuts": cuts}
(D / "cuts.json").write_text(json.dumps(out, indent=1))
print(len(cuts), "cuts, end", t, "(draft, no dance clip yet)" if not DANCE.exists() else "")
