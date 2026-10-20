"""Code-synthesised music loops for the «Мазутыч» movie (0 credits): chip-noir detective theme and a chase loop.
  python3 gen_music.py   -> noir_detective_16s.mp3, chase_surf_12s.mp3, valve_hero_12s.mp3 (seamless loops)"""
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


def noir():
    """slow swing walking bass in D minor, brushes, vibraphone minor-9 chords, a muted-trumpet motif: 8 bars @ 120 bpm = 16 s"""
    bpm = 120; b = 60 / bpm; L = 8 * 4 * b
    buf = np.zeros(int(L * SR))
    walk = ['D2', 'F2', 'A2', 'C3', 'G2', 'A#2', 'D3', 'A#2', 'A2', 'C#3', 'E3', 'G2', 'D2', 'E2', 'F2', 'A2',
            'D2', 'F2', 'A2', 'C3', 'G2', 'A#2', 'D3', 'A#2', 'A1', 'A2', 'G2', 'E2', 'D2', 'A1', 'C#2', 'A1']
    for i, n in enumerate(walk): add(buf, tone(hz(n), b * 0.95, 'bass', d=0.25, s=0.25, r=0.04), i * b, 0.9)
    chords = [['F3', 'A3', 'C4', 'E4'], ['A#3', 'D4', 'F4', 'A4'], ['G3', 'A#3', 'C#4', 'E4'], ['F3', 'A3', 'C4', 'E4']]
    for bar in range(8):
        ch = chords[(bar // 2) % 4]
        for k, n in enumerate(ch):
            add(buf, tone(hz(n), 1.6, 'vib', a=0.003, d=0.5, s=0.15, r=0.3), bar * 4 * b + 1.5 * b + k * 0.015, 0.24)
    for i in range(32):                                                    # brushes: swing 8ths
        add(buf, brush(seed=i), i * b, 0.30)
        add(buf, brush(seed=100 + i), i * b + b * 0.66, 0.16)
        if i % 2 == 1: add(buf, snare(seed=i) * 0.4, i * b, 0.25)
    motif = [('A4', 0.0, 1.5), ('C5', 1.5, 0.5), ('A#4', 2.0, 1.0), ('A4', 3.0, 0.66), ('G4', 3.66, 0.34), ('A4', 4.0, 3.0),
             ('D5', 16.0, 1.5), ('C5', 17.5, 0.5), ('A#4', 18.0, 1.0), ('G4', 19.0, 0.66), ('E4', 19.66, 0.34), ('D4', 20.0, 3.0)]
    for n, st, du in motif: add(buf, tone(hz(n), du * b, 'muted', a=0.03, d=0.4, s=0.6, r=0.12), st * b, 0.38)
    save(buf, 'noir_detective_16s', lp=7000)


def chase():
    """fast surf-chip chase in E minor: pulse bass ostinato, square lead, kick/snare, 8 bars @ 160 bpm = 12 s"""
    bpm = 160; b = 60 / bpm; L = 8 * 4 * b
    buf = np.zeros(int(L * SR))
    riff = ['E2', 'E2', 'G2', 'E2', 'A2', 'E2', 'A#2', 'B2']
    for i in range(64):
        add(buf, tone(hz(riff[i % 8]), b * 0.45, 'pulse', d=0.08, s=0.4, r=0.02), i * b / 2, 0.35)
    for i in range(32):
        add(buf, kick(), i * b, 0.9 if i % 2 == 0 else 0.0)
        if i % 2 == 1: add(buf, snare(seed=i), i * b, 0.6)
        add(buf, hat(seed=i), i * b + b / 2, 0.25)
    lead = ['B4', 'B4', 'D5', 'E5', 'G5', 'F#5', 'E5', 'D5', 'B4', 'A4', 'B4', 'D5', 'E5', 'E5', 'E5', 'E5']
    for i, n in enumerate(lead):
        add(buf, tone(hz(n), b * 0.9, 'square', d=0.15, s=0.5, r=0.05), 16 * b + i * b, 0.12)
    save(buf, 'chase_surf_12s', lp=9000)


def hero():
    """slow heroic brass swell in C (the valve), timpani rolls: 6 bars @ 90 bpm = 16 s"""
    bpm = 90; b = 60 / bpm; L = 6 * 4 * b
    buf = np.zeros(int(L * SR))
    prog = [['C3', 'G3', 'C4', 'E4'], ['A2', 'E3', 'A3', 'C4'], ['F2', 'C3', 'F3', 'A3'], ['G2', 'D3', 'G3', 'B3'],
            ['F2', 'C3', 'F3', 'A3'], ['G2', 'D3', 'G3', 'D4']]
    for bar, ch in enumerate(prog):
        for n in ch: add(buf, tone(hz(n), 4 * b, 'brass', a=0.5, d=1.0, s=0.8, r=0.4), bar * 4 * b, 0.12)
        for k in range(16): add(buf, kick(0.2) * (0.3 + 0.7 * k / 16), bar * 4 * b + k * b / 4, 0.25)
    mel = [('G4', 0, 2), ('C5', 2, 2), ('E5', 4, 3), ('D5', 7, 1), ('C5', 8, 2), ('A4', 10, 2), ('F4', 12, 3), ('A4', 15, 1),
           ('G4', 16, 4), ('B4', 20, 4)]
    for n, st, du in mel: add(buf, tone(hz(n), du * b, 'brass', a=0.08, d=0.6, s=0.8, r=0.2), st * b, 0.2)
    save(buf, 'valve_hero_16s', lp=8000)


if __name__ == '__main__':
    noir(); chase(); hero()
