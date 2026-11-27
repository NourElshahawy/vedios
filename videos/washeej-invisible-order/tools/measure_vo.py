#!/usr/bin/env python3
"""Print speech islands in the recorded VO so real line times can replace the estimates in timeline.json.
usage: python3 tools/measure_vo.py audio/vo.wav [offset_on_timeline=1.20]"""
import subprocess,sys,re
f=sys.argv[1]; off=float(sys.argv[2]) if len(sys.argv)>2 else 1.20
e=subprocess.run(["ffmpeg","-i",f,"-af","silencedetect=n=-38dB:d=0.22","-f","null","-"],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",e)]; se=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",e)]
d=float(re.search(r"Duration: (\d+):(\d+):([\d.]+)",e).groups()[2])+60*int(re.search(r"Duration: (\d+):(\d+)",e).group(2))
starts=[0.0]+se; ends=ss+[d]
for i,(a,b) in enumerate(zip(starts,ends)):
    if b-a>0.15: print(f"island {i:2d}: {a+off:6.2f} → {b+off:6.2f}  ({b-a:.2f}s)")
