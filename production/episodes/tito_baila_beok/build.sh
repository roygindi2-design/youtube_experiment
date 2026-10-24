#!/bin/bash
# Be OK TikTok (researcher §12: deliver 0.0-8.4 of the Motion Control clip, one shot, SILENT; Roy adds "Be OK" in the app)
cd /home/user/youtube_experiment || exit 1
B=production/episodes/tito_baila_beok; mkdir -p $B/build
ffmpeg -v error -y -i production/review/tiktok_beok/beok_motion.mp4 -t 8.4 -vf "scale=1080:1920:flags=lanczos,setsar=1" -an \
  -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p $B/build/beok_trim.mp4
python production/tiktok_text.py $B/build/beok_trim.mp4 $B/build/t1.mp4 "Mi peque a las 6 AM: ☀️💃" --until 2.8 --y 0.13 --size 80
python production/tiktok_text.py $B/build/t1.mp4 $B/build/t2.mp4 "Yo después de dormir 3 horas: 🧟" --start 2.8 --until 5.6 --y 0.13 --size 62
python production/tiktok_text.py $B/build/t2.mp4 production/deliver/tito_baila_beok_tiktok.mp4 "…pero así, todo está bien 🥹" --start 5.6 --until 8.4 --y 0.13 --size 76
ffmpeg -v error -y -i production/deliver/tito_baila_beok_tiktok.mp4 -vf scale=720:1280 -c:v libx264 -crf 26 -an production/review/tito_baila_beok_tiktok_review.mp4
