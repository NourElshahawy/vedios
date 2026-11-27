#!/usr/bin/env python3
"""Join S06A + S06B + S06C into the one-take shots/S06.mp4 (13.2s) with short hidden dissolves.
usage: python3 tools/stitch_s06.py [--a 4.6] [--b 5.6] [--c 3.4] [--x 0.2]   (seconds used from each clip)"""
import subprocess,sys,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
arg=lambda k,d: float(sys.argv[sys.argv.index(k)+1]) if k in sys.argv else d
a,b,c,x=arg('--a',4.6),arg('--b',5.6),arg('--c',3.4),arg('--x',0.2)
N="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,setsar=1,format=yuv420p"
f=[os.path.join(R,'shots',n+'.mp4') for n in ('S06A','S06B','S06C')]
fc=(f"[0:v]trim=0:{a},setpts=PTS-STARTPTS,{N}[a];[1:v]trim=0:{b},setpts=PTS-STARTPTS,{N}[b];[2:v]trim=0:{c},setpts=PTS-STARTPTS,{N}[c];"
    f"[a][b]xfade=transition=dissolve:duration={x}:offset={a-x}[ab];[ab][c]xfade=transition=dissolve:duration={x}:offset={a+b-2*x},format=yuv420p[v]")
subprocess.run(["ffmpeg","-y","-loglevel","error",*sum([["-i",i] for i in f],[]),"-filter_complex",fc,"-map","[v]","-c:v","libx264","-crf","14",os.path.join(R,'shots','S06.mp4')],check=True)
print("wrote shots/S06.mp4", round(a+b+c-2*x,2),"s (timeline needs 13.2)")
