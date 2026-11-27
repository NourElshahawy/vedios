#!/bin/bash
# Blender render (540x960) → 1080x1920 with bloom (burgundy-tinted halo around the peach light), grain.
# usage: tools/post_cgi.sh in.mp4 out.mp4
ffmpeg -y -loglevel error -i "$1" -filter_complex "[0:v]scale=1080:1920:flags=lanczos,format=gbrp,split[a][b];\
[b]curves=all='0/0 0.55/0 1/1',gblur=sigma=26,colorchannelmixer=rr=1.0:gg=0.55:bb=0.5[g];\
[a][g]blend=all_mode=screen:all_opacity=0.85,noise=alls=6:allf=t,format=yuv420p[v]" -map "[v]" -c:v libx264 -crf 14 "$2"
