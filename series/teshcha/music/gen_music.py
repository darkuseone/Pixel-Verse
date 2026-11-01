"""Code-synthesised loops for «Тёща на недельку» (0 credits): a bouncy 90s family-sitcom theme and a sneaky post-twist variant.
Synth helpers are shared with series/mazutych/music/gen_music.py (tone/env/add/save); harmony, tempo and timbres are our own.
  python3 gen_music.py   -> sitcom_theme_15s.mp3, sitcom_uhoh_15s.mp3 (seamless loops)"""
import importlib.util, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('mz', HERE.parents[1] / 'mazutych' / 'music' / 'gen_music.py')
M = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(M)
M.HERE = HERE
SR, hz, tone, add, save, brush, kick, snare, hat = M.SR, M.hz, M.tone, M.add, M.save, M.brush, M.kick, M.snare, M.hat


def reed(f, dur, **ek):
    """clarinet/bassoon-ish: odd harmonics, slight vibrato"""
    n = int(dur * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * f * t + 0.004 * np.sin(2 * np.pi * 5.2 * t) * f
    w = sum(np.sin(ph * k) / k for k in (1, 3, 5, 7))
    return w * M.env(n, **ek)


def piano(f, dur, **ek):
    n = int(dur * SR); t = np.arange(n) / SR
    w = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3) + 0.2 * np.sin(6 * np.pi * f * t) * np.exp(-t * 6)
    return w * M.env(n, **ek)


def theme():
    """F major, 128 bpm, 8 bars = 15 s: oom-pah bassoon, piano off-beats, brushes, cheeky clarinet tune"""
    b = 60 / 128; L = 32 * b
    buf = np.zeros(int(L * SR))
    prog = [('F2', ['A3', 'C4', 'F4']), ('C2', ['G3', 'C4', 'E4']), ('D2', ['A3', 'D4', 'F4']), ('A#1', ['A#3', 'D4', 'F4']),
            ('F2', ['A3', 'C4', 'F4']), ('G2', ['A#3', 'D4', 'G4']), ('C2', ['A#3', 'C4', 'E4']), ('C2', ['G3', 'C4', 'E4'])]
    for bar, (bs, ch) in enumerate(prog):
        t0 = bar * 4 * b
        for k in range(4):                                                  # oom (root) pah (fifth) on the beats
            nt = bs if k % 2 == 0 else bs[:-1] + str(int(bs[-1]) + 1)
            add(buf, reed(hz(nt), b * 0.6, a=0.01, d=0.12, s=0.5, r=0.05), t0 + k * b, 0.34)
            for n in ch: add(buf, piano(hz(n), b * 0.4, a=0.002, d=0.15, s=0.2, r=0.08), t0 + k * b + b / 2, 0.08)
            add(buf, brush(seed=bar * 4 + k), t0 + k * b, 0.22)
            add(buf, hat(seed=bar * 8 + k), t0 + k * b + b / 2, 0.12)
    mel = [('C5', 0, 0.5), ('A4', 0.5, 0.5), ('F4', 1, 1), ('G4', 2, 0.5), ('A4', 2.5, 0.5), ('C5', 3, 1),
           ('E5', 4, 0.5), ('D5', 4.5, 0.5), ('C5', 5, 0.5), ('G4', 5.5, 0.5), ('C5', 6, 2),
           ('D5', 8, 0.5), ('C5', 8.5, 0.5), ('A4', 9, 1), ('F4', 10, 0.5), ('G4', 10.5, 0.5), ('A#4', 11, 1),
           ('A4', 12, 0.5), ('G4', 12.5, 0.5), ('F4', 13, 1), ('E4', 14, 0.5), ('G4', 14.5, 0.5), ('C5', 15, 1),
           ('C5', 16, 0.5), ('A4', 16.5, 0.5), ('F4', 17, 1), ('G4', 18, 0.5), ('A4', 18.5, 0.5), ('C5', 19, 1),
           ('D5', 20, 0.5), ('A#4', 20.5, 0.5), ('G4', 21, 1), ('A#4', 22, 0.5), ('D5', 22.5, 0.5), ('G5', 23, 1),
           ('F5', 24, 0.5), ('E5', 24.5, 0.5), ('D5', 25, 0.5), ('C5', 25.5, 0.5), ('A#4', 26, 1), ('G4', 27, 1),
           ('E4', 28, 1), ('G4', 29, 0.5), ('C5', 29.5, 0.5), ('E5', 30, 2)]
    for n, st, du in mel: add(buf, reed(hz(n), du * b * 0.92, a=0.02, d=0.2, s=0.7, r=0.06), st * b, 0.16)
    save(buf, 'sitcom_theme_15s', lp=7500)


def uhoh():
    """after the twist: D minor creeping pizzicato bassoon + tick-tock wood, 8 bars @ 128 bpm"""
    b = 60 / 128; L = 32 * b
    buf = np.zeros(int(L * SR))
    line = ['D2', 'F2', 'A2', 'F2', 'C#2', 'E2', 'A2', 'E2', 'D2', 'F2', 'A2', 'C3', 'A#2', 'A2', 'G2', 'E2']
    for i in range(32):
        add(buf, reed(hz(line[i % 16]), b * 0.35, a=0.005, d=0.08, s=0.2, r=0.04), i * b, 0.4)
        add(buf, hat(0.04, seed=i), i * b + b / 2, 0.18)
        if i % 4 == 3: add(buf, kick(0.2), i * b, 0.4)
    for bar in range(8):
        for k, n in enumerate(['D4', 'F4', 'A4'] if bar % 2 == 0 else ['C#4', 'E4', 'A4']):
            add(buf, piano(hz(n), b * 1.8, a=0.002, d=0.4, s=0.1, r=0.2), bar * 4 * b + 2 * b + k * 0.02, 0.07)
    save(buf, 'sitcom_uhoh_15s', lp=6500)


if __name__ == '__main__':
    theme(); uhoh()
