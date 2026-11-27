#!/bin/bash
# QA on a master: specs, loudness, unintended freezes/black, cut list, contact sheet.  usage: tools/qa.sh renders/<master>.mp4
F=$1; O=renders/qa; mkdir -p $O; B=$(basename "$F" .mp4)
echo "== SPECS (expect h264 high, 1080x1920, 30/1, yuv420p, aac 48k)"
ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels -show_entries format=duration -of compact "$F"
echo "== LOUDNESS (target -14 LUFS / TP <= -1)"
ffmpeg -nostats -i "$F" -af ebur128=peak=true -f null - 2>&1 | grep -A20 "Summary" | grep -E "I:|LRA:|Peak:"
echo "== FREEZES > 0.5s (allowed: S03C 16.4-19.2 bullet time, S04B 22.4-26.0 barrier, END hold after 55.5)"
ffmpeg -nostats -i "$F" -vf freezedetect=n=0.002:d=0.5 -map 0:v -f null - 2>&1 | grep -oE "freeze_(start|end): [0-9.]+" | paste - - 
echo "== BLACK > 0.1s"
ffmpeg -nostats -i "$F" -vf blackdetect=d=0.1:pix_th=0.06 -an -f null - 2>&1 | grep -oE "black_start:[0-9.]+ black_end:[0-9.]+"
echo "== CUTS"
ffmpeg -nostats -i "$F" -vf "select='gt(scene,0.35)',showinfo" -an -f null - 2>&1 | grep -oE "pts_time:[0-9.]+" | tr '\n' ' '; echo
ffmpeg -y -loglevel error -i "$F" -vf "fps=1,scale=216:384,tile=10x6" -frames:v 1 $O/${B}_contact.png && echo "contact sheet: $O/${B}_contact.png"
