#!/bin/bash
# encode.sh <framesdir> <name> <alpha:0|1>  -> renders/<name>.mov (ProRes 4444 alpha or ProRes 422HQ) + renders/preview/<name>.mp4
set -e; F=$1; N=$2; A=$3; R=/home/user/washeej/production/renders; mkdir -p $R/preview
if [ "$A" = 1 ]; then
 ffmpeg -y -loglevel error -framerate 30 -i $F/f_%04d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -alpha_bits 16 $R/$N.mov
 ffmpeg -y -loglevel error -framerate 30 -i $F/f_%04d.png -f lavfi -i "color=c=0x17110f:s=$(ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=s=x:p=0 $F/f_0000.png)" -filter_complex "[1][0]overlay=shortest=1,format=yuv420p" -c:v libx264 -crf 16 -preset medium $R/preview/$N.mp4
else
 ffmpeg -y -loglevel error -framerate 30 -i $F/f_%04d.png -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le $R/$N.mov
 ffmpeg -y -loglevel error -framerate 30 -i $F/f_%04d.png -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p -movflags +faststart $R/preview/$N.mp4
fi
echo done $N
