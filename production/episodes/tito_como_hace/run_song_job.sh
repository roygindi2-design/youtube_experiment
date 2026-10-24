#!/bin/bash
# preflight LOCALLY first (no pod if it fails) -> up -> run -> wait -> fetch -> ALWAYS down (trap). Usage: bash run_song_job.sh
cd /home/user/youtube_experiment || exit 1
N=comohace
SPEC=production/episodes/tito_como_hace/spec.json
python production/preflight.py produce $SPEC || { echo "preflight failed: no pod started"; exit 1; }
trap 'python production/runpod/rp.py down $N' EXIT
python production/runpod/rp.py up $N || exit 1
python production/runpod/rp.py run $N production/jobs/job_como_hace_song.json --specs $SPEC || exit 1
for i in $(seq 1 90); do
  sleep 60
  S=$(python production/runpod/rp.py status $N 2>&1 | tail -1); echo "$(date +%H:%M) $S"
  echo "$S" | grep -q '"returncode": [0-9]' && break
done
python production/runpod/rp.py fetch $N production/episodes/tito_como_hace/song_takes
