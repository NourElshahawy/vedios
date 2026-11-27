#!/usr/bin/env python3
"""Procedural, royalty-free sound design for the film (no music by client decision).
Writes audio/sfx/<name>.wav (48 kHz stereo). Every sound is synthesized here — no samples, no licences.
usage: python3 tools/make_sfx.py"""
import numpy as np, wave, os
SR = 48000
R = np.random.default_rng(7)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audio', 'sfx'); os.makedirs(OUT, exist_ok=True)
t_ = lambda d: np.arange(int(d * SR)) / SR

def save(name, x, width=0.25):
    x = np.asarray(x, np.float64); x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    d = int(SR * 0.0006 * width / 0.25)   # tiny Haas offset for width
    L = x; Rr = np.concatenate([np.zeros(d), x[:len(x) - d]]) if d else x
    st = np.stack([L, Rr], 1); st[-int(SR * .01):] *= np.linspace(1, 0, int(SR * .01))[:, None]
    with wave.open(os.path.join(OUT, name + '.wav'), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())

def onepole_lp(x, fc):
    fc = np.broadcast_to(np.asarray(fc, float), x.shape); a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y
def bandsweep(x, f0, f1):   # crude moving band-pass: LP(f_hi) - LP(f_lo)
    f = np.geomspace(f0, f1, len(x)); return onepole_lp(x, f * 1.6) - onepole_lp(x, f / 1.6)
def env(n, a, r, curve=3.0):
    e = np.ones(n); ai = int(a * SR); e[:ai] = np.linspace(0, 1, ai) ** 2
    ri = int(r * SR); e[-ri:] *= np.linspace(1, 0, ri) ** curve; return e
def pink(n):
    w = R.standard_normal(n); f = np.fft.rfft(w); k = np.arange(len(f)); k[0] = 1; return np.fft.irfft(f / np.sqrt(k), n)
def brown(n): return np.cumsum(R.standard_normal(n)) * 0.02
def ks(freq, dur, bright=0.5, decay=0.996):   # Karplus-Strong plucked string (the Washeej thread)
    n = int(dur * SR); p = int(SR / freq); buf = R.uniform(-1, 1, p) * bright + onepole_lp(R.uniform(-1, 1, p), 2500) * (1 - bright)
    y = np.zeros(n)
    for i in range(n):
        y[i] = buf[i % p]; buf[i % p] = decay * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return y
def bell(freqs, amps, dur, dec):
    t = t_(dur); return sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in zip(freqs, amps, dec))

# --- whooshes -------------------------------------------------------------------------
n = int(1.3 * SR); save('tunnel_whoosh', bandsweep(pink(n), 300, 2400) * env(n, .5, .5) + onepole_lp(brown(n), 120) * .6 * env(n, .3, .6))
n = int(.55 * SR); save('crash_zoom_whoosh', bandsweep(pink(n), 500, 6000) * env(n, .4, .1, 1.5))
n = int(1.2 * SR); x = bandsweep(pink(n), 1800, 400); save('fpv_pass', x * env(n, .45, .55))
n = int(.9 * SR); x = bandsweep(pink(n), 2500, 300) * env(n, .15, .6); save('reverse_swoosh_release', x[::-1])
n = int(.9 * SR); save('glass_pass', bandsweep(pink(n), 1500, 4000) * env(n, .35, .45) + bell([3150, 4720], [.15, .1], .9, [.25, .2]))
# --- impact: muffled glass thud (not an explosion) ------------------------------------
t = t_(1.8); thud = np.sin(2 * np.pi * (48 + 30 * np.exp(-t * 25)) * t) * np.exp(-t * 3.2)
glass = bell([2130, 3410, 5230, 7020], [.25, .2, .14, .08], 1.8, [.5, .35, .25, .15])
burst = onepole_lp(R.standard_normal(len(t)), 3000) * np.exp(-t * 40) * .5
save('impact_glass_thud', thud * 1.4 + glass + burst)
# --- tape rewind (cold open → story start) --------------------------------------------
t = t_(.35); f = 900 * np.exp(-t * 6) + 120; ph = 2 * np.pi * np.cumsum(f) / SR
save('tape_rewind', (np.sign(np.sin(ph)) * .3 + bandsweep(pink(len(t)), 3000, 400)) * env(len(t), .02, .12))
# --- digital assemble: soft precise ticks --------------------------------------------
x = np.zeros(int(1.1 * SR))
for k, ti in enumerate(np.sort(R.uniform(0, .95, 14))):
    i = int(ti * SR); s = bell([1800 + 140 * k], [1], .12, [.03]); x[i:i + len(s)] += s[:len(x) - i] * (.4 + .6 * R.random())
save('digital_assemble', x)
# --- UI --------------------------------------------------------------------------------
save('ui_success_chime', np.concatenate([bell([1318.5, 2637], [1, .3], .25, [.12, .06]), np.zeros(0)])[:int(.25 * SR)].tolist() +
     bell([1975.5, 3951], [1, .3], .9, [.35, .15]).tolist())
x = np.zeros(int(3.0 * SR))
for ti in np.sort(R.uniform(0, 2.7, 22)):
    i = int(ti * SR); f = R.choice([880, 988, 1175, 1319, 1568]); s = bell([f, f * 2], [1, .25], .18, [.05, .03])
    x[i:i + len(s)] += s * (.3 + .7 * ti / 2.7)
save('notifications_swarm', x)
# --- time freeze (bullet time) -------------------------------------------------------
n = int(.8 * SR); sw = onepole_lp(pink(n), np.geomspace(200, 6000, n)) * np.linspace(0, 1, n) ** 3
save('time_freeze_suck', np.concatenate([sw, bell([60], [2.0], .5, [.18])]))
# --- capsule launch ------------------------------------------------------------------
t = t_(.8); ph = 2 * np.pi * np.cumsum(260 * np.exp(t * 2.2)) / SR
save('capsule_launch', np.sin(ph) * .35 * env(len(t), .05, .5) + bandsweep(pink(len(t)), 600, 5000) * env(len(t), .2, .4))
# --- room tone for the silence -----------------------------------------------------------
n = int(2.2 * SR); save('room_tone_low', onepole_lp(brown(n), 90) * env(n, .2, .8))
# --- the Washeej thread: warm plucked string family ------------------------------------
save('thread_pluck_warm', ks(196, 1.8, .35, .997) + .5 * ks(293.7, 1.8, .3, .996))
x = ks(98, .9, .7, .99); creak = onepole_lp(R.standard_normal(len(x)), 900) * (np.sin(2 * np.pi * 31 * t_(.9)) > .6) * .4
save('thread_snag', x + creak)
k1 = ks(392, .3, .4, .993); k2 = ks(523.3, .5, .4, .994)
save('thread_knot_tie', np.concatenate([k1, k2]) + np.concatenate([np.zeros(len(k1)), bandsweep(pink(len(k2)), 2000, 5000) * .15 * env(len(k2), .02, .3)]))
seg = [ks(f, .22, .35, .995) for f in (196, 247, 294, 392, 494, 587)]
x = np.zeros(int(1.6 * SR))
for i, s in enumerate(seg):
    o = int(i * .2 * SR); x[o:o + len(s)] += s
save('thread_run_rise', x)
save('order_arrive_ding', bell([784, 1176, 1568, 2352], [1, .35, .5, .12], 1.4, [.6, .4, .3, .15]))
print('wrote', len(os.listdir(OUT)), 'sfx to', OUT)
