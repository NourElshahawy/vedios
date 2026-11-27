#!/bin/bash
# Wan 2.2 clip (480x832 @16fps) → 1080x1920 @30fps: motion-compensated 16→32 interpolation, played at 30 (6% slower,
# cinematic), lanczos upscale, light sharpen, film grain, warm-neutral grade.  usage: tools/post_wan.sh in.mp4 out.mp4
ffmpeg -y -loglevel error -i "$1" -vf "minterpolate=fps=32:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=PTS*32/30,fps=30,\
scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.6,\
eq=contrast=1.04:saturation=0.94,noise=alls=7:allf=t,format=yuv420p" -r 30 -an -c:v libx264 -crf 14 -preset medium "$2"
