"""Code-synthesised music for «Land of the Fee» (0 credits): «Freedom on a Budget» — a cheap kazoo marching band (tuba oom-pah, snare
rudiments, cymbal, kazoo lead with a nasal buzz), an original jaunty march in B-flat, seamless loop.
  python3 gen_music.py   -> freedom_kazoo_16s.mp3"""
import subprocess, pathlib
import numpy as np

SR = 44100
HERE = pathlib.Path(__file__).resolve().parent
N = {n: i for i, n in enumerate(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])}


def hz(note):
    name, octv = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((N[name] + 12 * (octv + 1) - 69) / 12)


def env(n, a=0.005, d=0.1, s=0.6, r=0.05, sus=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a)
    e = np.where(t > a, s + (1 - s) * np.exp(-(t - a) / d), e)
    rel = np.clip((n / SR - t) / r, 0, 1)
    return e * rel


def tone(f, dur, kind='sine', **ek):
    n = int(dur * SR); t = np.arange(n) / SR
    if kind == 'sine': w = np.sin(2 * np.pi * f * t)
    elif kind == 'bass':                                                    # plucked upright: sine + soft 2nd harmonic, thump
        w = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 8)
    elif kind == 'vib':                                                     # vibraphone-ish FM bell with tremolo
        w = np.sin(2 * np.pi * f * t + 1.2 * np.exp(-t * 6) * np.sin(2 * np.pi * f * 4 * t)) * (1 + 0.25 * np.sin(2 * np.pi * 5.5 * t))
    elif kind == 'square':
        w = np.sign(np.sin(2 * np.pi * f * t)) * 0.6 + 0.4 * np.sin(2 * np.pi * f * t)
    elif kind == 'pulse':
        w = ((t * f) % 1 < 0.25).astype(float) * 2 - 1
    elif kind == 'brass':                                                   # saw-ish with slow attack brightness
        w = sum(np.sin(2 * np.pi * f * k * t) / k * min(1, 1.2 / k + 0.2) for k in range(1, 7))
        w *= 1 - 0.3 * np.exp(-t * 10)
    elif kind == 'muted':                                                   # muted trumpet: band-limited saw with wah
        br = 0.5 + 0.5 * np.sin(2 * np.pi * 3 * t)
        w = sum(np.sin(2 * np.pi * f * k * t) / k * (br if k > 2 else 1) for k in range(1, 6))
    return w * env(n, **ek)


def noise(dur, hp=True, seed=0):
    r = np.random.default_rng(seed); x = r.standard_normal(int(dur * SR))
    if hp: x = np.diff(x, prepend=0)
    return x


def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if i < len(buf): buf[i:j] += x[:j - i] * g
    if i + len(x) > len(buf):                                               # wrap the tail -> seamless loop
        k = i + len(x) - len(buf); buf[:k] += x[len(x) - k:] * g


def kick(dur=0.3):
    t = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 12)


def snare(dur=0.18, seed=1):
    t = np.arange(int(dur * SR)) / SR
    return (noise(dur, seed=seed) * 0.6 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 22)


def brush(dur=0.12, seed=2):
    t = np.arange(int(dur * SR)) / SR
    return noise(dur, seed=seed) * np.exp(-t * 30) * 0.5


def hat(dur=0.05, seed=3):
    t = np.arange(int(dur * SR)) / SR
    return noise(dur, seed=seed) * np.exp(-t * 90)


def save(buf, name, lp=None):
    buf = buf / (np.abs(buf).max() + 1e-9) * 0.85
    raw = HERE / f'{name}.f32'
    buf.astype(np.float32).tofile(raw)
    af = 'aecho=0.8:0.6:60|130:0.25|0.15'
    if lp: af += f',lowpass=f={lp}'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', str(raw), '-af', af,
                    '-ac', '2', '-b:a', '160k', str(HERE / f'{name}.mp3')], check=True)
    raw.unlink()
    print(HERE / f'{name}.mp3')


def kazoo(f, dur, vib=5.5, **ek):
    """kazoo: buzzy band-limited saw, nasal formant-ish emphasis on harmonics 3-5, wobbly vibrato, a little breath noise"""
    n = int(dur * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * f * t + 0.012 * f / vib * np.sin(2 * np.pi * vib * t) * 2 * np.pi
    w = sum(np.sin(k * ph) / k * (1.8 if 3 <= k <= 5 else 1.0) for k in range(1, 10))
    w = np.tanh(w * 1.6)
    w += noise(dur, seed=int(f)) * 0.05
    return w * env(n, **ek)


def tuba(f, dur, **ek):
    n = int(dur * SR); t = np.arange(n) / SR
    w = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) + 0.2 * np.sin(6 * np.pi * f * t)
    return np.tanh(w * 1.3) * env(n, **ek)


def cymbal(dur=0.6, seed=7):
    t = np.arange(int(dur * SR)) / SR
    x = noise(dur, seed=seed); x = np.diff(x, prepend=0)
    return x * np.exp(-t * 6) * 0.35


def march(name='freedom_kazoo_16s', low=1.0, kz=0.30, lp=7500):
    """8 bars of 4/4 @ 120 bpm = 16 s: B-flat major oom-pah, snare drags, kazoo tune (original), glockenspiel-ish answer"""
    bpm = 120; b = 60 / bpm; L = 8 * 4 * b
    buf = np.zeros(int(L * SR))
    roots = [('A#1', 'F2'), ('A#1', 'F2'), ('D#2', 'A#2'), ('A#1', 'F2'), ('F1', 'C2'), ('A#1', 'F2'), ('F1', 'C2'), ('A#1', 'F2')]
    chords = [['D4', 'F4', 'A#4'], ['D4', 'F4', 'A#4'], ['D#4', 'G4', 'A#4'], ['D4', 'F4', 'A#4'], ['C4', 'F4', 'A4'], ['D4', 'F4', 'A#4'],
              ['C4', 'D#4', 'A4'], ['D4', 'F4', 'A#4']]
    for bar in range(8):
        r1, r2 = roots[bar]
        for beat in range(4):
            t0 = (bar * 4 + beat) * b
            if beat % 2 == 0:
                add(buf, tuba(hz(r1 if beat == 0 else r2), b * 0.8, a=0.01, d=0.2, s=0.5, r=0.05), t0, 0.55 * low)
                add(buf, tone(hz(r1 if beat == 0 else r2) / 2, b * 0.9, 'sine', a=0.01, d=0.3, s=0.6, r=0.05), t0, 0.35 * (low - 1.0))
            else:
                for n in chords[bar]: add(buf, tone(hz(n), b * 0.35, 'brass', a=0.005, d=0.08, s=0.3, r=0.03), t0, 0.06)
            add(buf, snare(seed=bar * 4 + beat) * 0.8, t0 + (b / 2 if beat % 2 else 0), 0.35 if beat % 2 else 0.18)
            add(buf, snare(0.08, seed=200 + bar * 4 + beat) * 0.5, t0 + b * 0.75, 0.12)
        add(buf, kick(0.35), bar * 4 * b, 0.6 * low)
        if low > 1.0: add(buf, kick(0.3), bar * 4 * b + 2 * b, 0.45 * low)
        if bar % 4 == 3:
            for k in range(8): add(buf, snare(0.06, seed=300 + k) * 0.6, bar * 4 * b + 3 * b + k * b / 8, 0.10 + 0.03 * k)
            add(buf, cymbal(), (bar + 1) * 4 * b % L, 0.5)
    tune = [('F4', 0, 0.75), ('F4', 0.75, 0.25), ('A#4', 1, 1), ('D5', 2, 1), ('A#4', 3, 1),
            ('C5', 4, 0.75), ('A#4', 4.75, 0.25), ('A4', 5, 1), ('G4', 6, 1), ('F4', 7, 1),
            ('G4', 8, 0.75), ('A4', 8.75, 0.25), ('A#4', 9, 1), ('D#5', 10, 1), ('D5', 11, 1),
            ('C5', 12, 2), ('F4', 14, 1), ('F4', 15, 1),
            ('F4', 16, 0.75), ('F4', 16.75, 0.25), ('A#4', 17, 1), ('D5', 18, 1), ('F5', 19, 1),
            ('D#5', 20, 0.75), ('D5', 20.75, 0.25), ('C5', 21, 1), ('A4', 22, 1), ('F4', 23, 1),
            ('G4', 24, 1), ('D#5', 25, 1), ('D5', 26, 1), ('C5', 27, 1),
            ('A#4', 28, 2.5), ('F4', 30.5, 0.5), ('A#4', 31, 0.5)]
    for n, st, du in tune: add(buf, kazoo(hz(n), du * b * 0.95, a=0.02, d=0.3, s=0.75, r=0.06), st * b, kz)
    for n, st in (('D6', 2.5), ('F6', 6.5), ('D#6', 10.5), ('C6', 14.5), ('D6', 18.5), ('A5', 22.5), ('D#6', 26.5), ('D6', 30.5)):
        add(buf, tone(hz(n), 0.4, 'vib', a=0.002, d=0.15, s=0.05, r=0.1), st * b, 0.10)
    save(buf, name, lp=lp)


if __name__ == '__main__':
    march()
    march('freedom_kazoo_v2_16s', low=1.6, kz=0.22, lp=6000)      # earshot pass 30.10.2026: body in the low end, softer mids
