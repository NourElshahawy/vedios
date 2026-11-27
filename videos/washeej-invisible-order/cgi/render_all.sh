#!/bin/bash
# Renders every other frame (15 fps) and motion-interpolates back to 30 fps. Resumable (existing frames are skipped).
cd "$(dirname "$0")/.."
for s in S04B S00 S04A S03D S06; do
  [ -f cgi/$s.done ] && continue
  python3 cgi/scene.py $s --res 540 --samples 14 --step 2 2>&1 | grep -E "Traceback|Error:|DONE" || continue
  ffmpeg -y -loglevel error -framerate 15 -pattern_type glob -i "cgi/frames/$s/f_*.png" \
    -vf "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,format=yuv420p" -c:v libx264 -crf 12 cgi/$s.mp4 \
    && touch cgi/$s.done && echo "rendered $s $(date +%T)"
done
