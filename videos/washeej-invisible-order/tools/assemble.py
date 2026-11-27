#!/usr/bin/env python3
"""
WASHEEJ — The Invisible Order · final conform.

Builds the 9:16 master from generated shots + rendered graphics + audio, driven by timeline.json.

  python3 tools/assemble.py --check      # list what is missing / too short, change nothing
  python3 tools/assemble.py              # build the master MP4 (fails if any shot is missing or short)
  python3 tools/assemble.py --slates     # INTERNAL timing check only: missing shots become labelled black slates.
                                         # Output is named *_SLATES_NOT_FOR_DELIVERY.mp4 and must never be published.

Rules enforced on purpose:
  * A missing or too-short shot is an error. The script never pads with a freeze frame or a zoom on a still.
  * Intentional freezes (S03C bullet time, S04B barrier) must come from the generated footage itself.
"""
import json, os, subprocess, sys, glob, shutil, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "timeline.json"), encoding="utf-8"))
FPS, W, H = TL["fps"], TL["width"], TL["height"]
SLATES = "--slates" in sys.argv
CHECK = "--check" in sys.argv
WORK = os.path.join(tempfile.gettempdir(), "washeej_conform")
os.makedirs(WORK, exist_ok=True)


def p(*a): return os.path.join(ROOT, *a)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd) + "\n" + r.stderr[-3000:])
    return r


def duration(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return 0.0


def shot_source(s):
    if s.get("source_file"): return p(s["source_file"])
    sid = s.get("source", s["id"])
    for cand in (f"shots/{sid}_comp.mp4", f"shots/{sid}_comp.mov", f"shots/{sid}.mp4", f"shots/{sid}.mov"):
        if os.path.exists(p(cand)): return p(cand)
    return None


NORM = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
        f"fps={FPS},setsar=1,format=yuv420p")

shots = TL["shots"]
problems = []
for i, s in enumerate(shots):
    need = s["end"] - s["start"]
    nxt = shots[i + 1] if i + 1 < len(shots) else None
    if nxt and nxt.get("xfade_in"): need += nxt["xfade_in"]
    s["_need"] = need
    if s.get("special") == "rewind":
        src = shot_source(shots[0]); need_src = shots[0]["end"] - shots[0]["start"] + shots[0].get("trim_in", 0)
    else:
        src = shot_source(s); need_src = need + s.get("trim_in", 0)
    s["_src"] = src
    if not src:
        problems.append(f"MISSING  {s['id']:5s} ({s['scene']}) needs {need_src:.2f}s")
    elif duration(src) + 1e-3 < need_src / s.get("speed", 1.0):
        problems.append(f"SHORT    {s['id']:5s} has {duration(src):.2f}s, needs {need_src:.2f}s — regenerate/extend, do not freeze-pad")

if CHECK or (problems and not SLATES):
    print("\n".join(problems) or "All shots present and long enough.")
    sys.exit(1 if problems else 0)

segs = []
for i, s in enumerate(shots):
    out = os.path.join(WORK, f"{i:02d}_{s['id']}.mp4"); need = s["_need"]
    if not s["_src"]:
        txt = f"MISSING {s['id']} - {s['scene']}".replace(":", " ")
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=0x1a1012:s={W}x{H}:r={FPS}:d={need}",
             "-vf", f"drawtext=text='{txt}':fontcolor=0xfed7b8:fontsize=44:x=(w-tw)/2:y=(h-th)/2,format=yuv420p",
             "-c:v", "libx264", "-crf", "18", out])
        segs.append(out); continue
    if s.get("special") == "rewind":
        d0 = shots[0]["end"] - shots[0]["start"]; t0 = shots[0].get("trim_in", 0)
        vf = (f"trim={t0}:{t0+d0},setpts=PTS-STARTPTS,reverse,setpts=PTS*{need/d0:.4f},{NORM},tmix=frames=4:weights='1 1 1 1',"
              f"drawbox=c=0xfed7b8@0.55:t=fill:enable='lt(n,2)'")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", s["_src"], "-vf", vf, "-t", f"{need}", "-an", "-r", str(FPS),
             "-c:v", "libx264", "-crf", "14", out])
        segs.append(out); continue
    inputs = ["-ss", f"{s.get('trim_in', s.get('from', 0))}", "-i", s["_src"]]
    sp = s.get("speed", 1.0)
    fc = f"[0:v]setpts=(PTS-STARTPTS)/{sp},{NORM}[v0]"; last = "v0"
    for k, ov in enumerate(s.get("overlays", [])):
        inputs += ["-ss", f"{ov.get('from', 0)}", "-i", p(ov["file"])]
        off = ov["at"] - s["start"]
        fc += (f";[{k+1}:v]format=yuva444p10le,scale={W}:{H},setpts=PTS-STARTPTS+{off}/TB[o{k}]"
               f";[{last}][o{k}]overlay=eof_action=pass:enable='gte(t,{off})'[v{k+1}]")
        last = f"v{k+1}"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc + f";[{last}]format=yuv420p[vout]",
         "-map", "[vout]", "-t", f"{need}", "-an", "-r", str(FPS), "-c:v", "libx264", "-crf", "14", out])
    segs.append(out)

# picture: concat, with optional crossfade into a shot flagged xfade_in (the end card)
xf = [(i, s) for i, s in enumerate(shots) if s.get("xfade_in")]
listf = os.path.join(WORK, "list.txt")
cut = xf[0][0] if xf else len(segs)
open(listf, "w").write("".join(f"file '{f}'\n" for f in segs[:cut]))
main = os.path.join(WORK, "main.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listf, "-c", "copy", main])
picture = main
if xf:
    i, s = xf[0]
    picture = os.path.join(WORK, "picture.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", main, "-i", segs[i], "-filter_complex",
         f"[0:v][1:v]xfade=transition=fade:duration={s['xfade_in']}:offset={s['start']},format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-crf", "14", picture])

# audio
TOT = TL["duration"]; ain = []; fc = []; mix = []
lines = TL["vo"]["lines"]
line_files = [p("audio/vo", f"{l['id']}.wav") for l in lines]
if all(os.path.exists(f) for f in line_files):
    for l, f in zip(lines, line_files):
        ain += ["-i", f]; n = len(ain) // 2 - 1
        fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(l['start']*1000)}:all=1[vo{n}]"); mix.append(f"[vo{n}]")
elif os.path.exists(p(TL["vo"]["single_file"])):
    ain += ["-i", p(TL["vo"]["single_file"])]
    fc.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(TL['vo']['single_offset']*1000)}:all=1[vo0]"); mix.append("[vo0]")
else:
    print("WARNING: no voiceover found (audio/vo.wav or audio/vo/V*.wav) — master will have no narration")
vo_bus = None
if mix:
    fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,apad=whole_dur={TOT},asplit=2[vob][vosc]"); vo_bus = "[vob]"
M = TL["music"]
if os.path.exists(p(M["file"])):
    ain += ["-i", p(M["file"])]; n = len(ain) // 2 - 1
    pts = M["automation"]; expr = f"pow(10,{pts[-1]['db']}/20)"
    for a, b in reversed(list(zip(pts, pts[1:]))):
        seg = f"pow(10,({a['db']}+({b['db']}-{a['db']})*(t-{a['t']})/{max(b['t']-a['t'],1e-3)})/20)"
        expr = f"if(lt(t,{b['t']}),{seg},{expr})"
    fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{TOT},volume='{expr}':eval=frame[mus0]")
    if vo_bus:
        fc.append("[mus0][vosc]sidechaincompress=threshold=0.04:ratio=3:attack=25:release=350[mus]")
    else:
        fc.append("[mus0]anull[mus]")
    mix_music = "[mus]"
else:
    print("WARNING: audio/music.wav missing"); mix_music = None
    if vo_bus: fc.append("[vosc]anullsink")
sfx_tags = []
for k, e in enumerate(TL["sfx"]):
    f = p(e["file"])
    if not os.path.exists(f): continue
    ain += ["-i", f]; n = len(ain) // 2 - 1
    fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={e['db']}dB,adelay={int(e['t']*1000)}:all=1[s{k}]")
    sfx_tags.append(f"[s{k}]")
missing_sfx = sorted({e["file"] for e in TL["sfx"] if not os.path.exists(p(e["file"]))})
if missing_sfx: print("WARNING: missing SFX:", ", ".join(missing_sfx))
buses = [b for b in [vo_bus, mix_music] if b] + sfx_tags
final = p("renders", "WASHEEJ_InvisibleOrder_9x16_1080x1920_30fps" + ("_SLATES_NOT_FOR_DELIVERY" if SLATES else "") + ".mp4")
if buses:
    fc.append(f"{''.join(buses)}amix=inputs={len(buses)}:normalize=0,atrim=0:{TOT}[mixed]")
    mixed = os.path.join(WORK, "mix.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", *ain, "-filter_complex", ";".join(fc), "-map", "[mixed]", mixed])
    L = TL["loudness"]
    r = subprocess.run(["ffmpeg", "-i", mixed, "-af", f"loudnorm=I={L['integrated_lufs']}:TP={L['true_peak_db']}:LRA=9:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm=I={L['integrated_lufs']}:TP={L['true_peak_db']}:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", picture, "-i", mixed, "-af", ln + ",aresample=48000",
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-crf", "16", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart",
         "-t", f"{TOT}", final])
else:
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", picture, "-c:v", "libx264", "-profile:v", "high", "-crf", "16",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-t", f"{TOT}", final])
print("wrote", final)
if problems: print("\n".join(problems))
