#!/usr/bin/env python3
"""Composite floating UI cards (alpha PNGs) onto a shot: staggered entrances, slow push toward camera, soft depth blur.
usage: python3 tools/float_cards.py <shot.mp4> <out.mp4> <cards.json>
cards.json: [{"png": "...", "x": 640, "y": 120, "w": 420, "t_in": 0.2, "depth": 0.6}, ...]   (x,y = top-left in output px)
depth 0..1: far cards are smaller-growing and slightly blurred; near cards grow faster (sense of closing in)."""
import cv2, json, sys, subprocess, numpy as np, os, tempfile
shot, out, spec = sys.argv[1:4]; cards = json.load(open(spec))
cap = cv2.VideoCapture(shot); fps = cap.get(cv2.CAP_PROP_FPS) or 30; W, H = int(cap.get(3)), int(cap.get(4))
imgs = [cv2.imread(c["png"], cv2.IMREAD_UNCHANGED) for c in cards]
tmp = tempfile.mkdtemp(); wr = cv2.VideoWriter(os.path.join(tmp, 'o.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H))
ease = lambda x: 1 - (1 - min(max(x, 0), 1)) ** 3
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    t = i / fps; f = f.astype(np.float32)
    for c, im in zip(cards, imgs):
        a = ease((t - c["t_in"]) / 0.35)
        if a <= 0: continue
        grow = 1 + (0.03 + 0.05 * c.get("depth", .5)) * max(0, t - c["t_in"])
        w = int(c["w"] * grow * (0.92 + 0.08 * a)); h = int(im.shape[0] * w / im.shape[1])
        s = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA)
        if c.get("depth", .5) < .4: s = cv2.GaussianBlur(s, (0, 0), 1.6)
        cx = c["x"] + c["w"] / 2 + (c["x"] + c["w"] / 2 - W / 2) * 0.015 * max(0, t - c["t_in"]); cy = c["y"] + (1 - a) * 30
        x0, y0 = int(cx - w / 2), int(cy)
        xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
        if xb <= xa or yb <= ya: continue
        sub = s[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32)
        al = sub[..., 3:4] / 255 * a * 0.94
        f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - al) + sub[..., :3] * al
    # the room cools and darkens as the pressure builds
    k = min(1, t / 3.0); f = f * (1 - 0.12 * k); f[..., 0] *= 1 + 0.06 * k; f[..., 2] *= 1 - 0.05 * k
    wr.write(np.clip(f, 0, 255).astype(np.uint8)); i += 1
wr.release()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, 'o.mp4'), "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", out], check=True)
print("wrote", out, i, "frames")
