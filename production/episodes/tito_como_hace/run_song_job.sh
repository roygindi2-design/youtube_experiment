#!/bin/bash
# up -> run -> wait -> fetch -> ALWAYS down (trap), so the pod never idles. Usage: bash run_song_job.sh
cd /home/user/youtube_experiment || exit 1
N=comohace
trap 'python production/runpod/rp.py down $N' EXIT
python production/runpod/rp.py up $N || exit 1
python production/runpod/rp.py run $N production/jobs/job_como_hace_song.json || exit 1
for i in $(seq 1 90); do
  sleep 60
  S=$(python production/runpod/rp.py status $N 2>&1 | tail -1); echo "$(date +%H:%M) $S"
  echo "$S" | grep -q '"returncode": [0-9]' && break
done
python production/runpod/rp.py fetch $N production/episodes/tito_como_hace/song_takes
