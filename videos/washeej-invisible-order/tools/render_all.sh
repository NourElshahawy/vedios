#!/bin/bash
# Renders every graphics element to ProRes (+ H.264 preview). Run from production/.
cd "$(dirname "$0")/.."; T=/tmp/claude-0/frames; mkdir -p $T
job(){ node tools/render.js gfx/$1.html $T/$2 $3 $4 $5 $6 30 "$7" && tools/encode.sh $T/$2 $2 $6 && rm -rf $T/$2; }
job GFX_00_capsule_label GFX_00_capsule_label 1.5 900 300 1 &
job GFX_04_sent_ne_received GFX_04_sent_ne_received 4 1080 1920 1 &
job GFX_08_endcard GFX_08_endcard 6.5 1080 1920 0 &
wait
job GFX_03_phone_ui GFX_03_phone_ui 5 1170 2532 0 &
job GFX_05_dashboard GFX_05_dashboard_empty 6 1920 1200 0 mode=empty &
job GFX_05_dashboard GFX_05_dashboard_arrive 5 1920 1200 0 mode=arrive &
wait
job GFX_06_journey GFX_06_journey 13 1080 1920 1
job GFX_01_prompt_screen GFX_01_prompt_screen 2.5 1920 1200 0
