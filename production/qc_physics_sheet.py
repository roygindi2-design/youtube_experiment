"""Physics/trunk QC sheet: frames every <step> seconds with timestamps, tiled, for eye review.
    python production/qc_physics_sheet.py <video> <out_prefix> [step=0.5] [cols=8]
Writes <out_prefix>_N.jpg pages (48 frames each). Look for: trunk vanishing/shrinking, frozen liquids,
liquid without a source, objects morphing, extra limbs/characters, clothes in the bath."""
import subprocess, sys
v, out = sys.argv[1], sys.argv[2]
step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 8
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v]))
per = cols * 6
page, t = 0, 0.0
while t < dur:
    span = min(per * step, dur - t)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-t", f"{span:.2f}", "-i", v, "-vf",
                    f"fps=1/{step},scale=300:-1,drawtext=text='%{{pts\\:hms\\:{t:.2f}}}':fontcolor=yellow:fontsize=16:x=3:y=3:box=1:boxcolor=black@0.5,tile={cols}x6",
                    "-frames:v", "1", f"{out}_{page}.jpg"], check=True)
    page += 1; t += per * step
print(page, "pages")
