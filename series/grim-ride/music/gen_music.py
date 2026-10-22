"""Code-synthesised loops for the «Grim Ride» movie (0 credits), on the synth helpers of series/mazutych/music/gen_music.py.
  python3 gen_music.py  -> loop_waltz_12s.mp3 (the time loop: music-box waltz), race_12s.mp3 (the final race), porch_16s.mp3 (tender ending)"""
import sys, pathlib, importlib.util
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mz', HERE.parents[1] / 'mazutych' / 'music' / 'gen_music.py')
mz = importlib.util.module_from_spec(spec); spec.loader.exec_module(mz)
mz.HERE = HERE
SR, hz, tone, add, kick, snare, hat, brush = mz.SR, mz.hz, mz.tone, mz.add, mz.kick, mz.snare, mz.hat, mz.brush


def waltz():
    """spooky music-box waltz in D minor, 3/4 @ 120 bpm, 8 bars = 12 s; a ticking clock on every beat"""
    b = 0.5; L = 8 * 3 * b
    buf = np.zeros(int(L * SR))
    bass = ['D2', 'A1', 'A#1', 'A1', 'D2', 'F2', 'G2', 'A1']
    up = [['F3', 'A3'], ['E3', 'A3'], ['F3', 'A#3'], ['E3', 'C#4'], ['F3', 'A3'], ['A3', 'C4'], ['G3', 'A#3'], ['E3', 'C#4']]
    for bar in range(8):
        add(buf, tone(hz(bass[bar]), b * 0.9, 'bass', d=0.3, s=0.2, r=0.05), bar * 3 * b, 0.8)
        for k in (1, 2):
            for n in up[bar]: add(buf, tone(hz(n), b * 0.6, 'vib', d=0.15, s=0.1, r=0.05), bar * 3 * b + k * b, 0.13)
    mel = [('A5', 0, 1), ('D6', 1, 1), ('C6', 2, 1), ('A#5', 3, 2), ('A5', 5, 1), ('G5', 6, 1), ('A5', 7, 1), ('E5', 8, 1),
           ('F5', 9, 2), ('E5', 11, 1), ('D5', 12, 1), ('F5', 13, 1), ('A5', 14, 1), ('D6', 15, 2), ('C#6', 17, 1),
           ('D6', 18, 1), ('A5', 19, 1), ('F5', 20, 1), ('E5', 21, 2), ('C#5', 23, 1)]
    for n, st, du in mel: add(buf, tone(hz(n), du * b * 0.95, 'vib', a=0.002, d=0.35, s=0.05, r=0.2), st * b, 0.3)
    for i in range(24):                                                       # tick-tock
        t = np.arange(int(0.03 * SR)) / SR
        clk = np.sin(2 * np.pi * (2400 if i % 2 else 1800) * t) * np.exp(-t * 300)
        add(buf, clk, i * b, 0.18)
    mz.save(buf, 'loop_waltz_12s', lp=8000)


def race():
    """fast spooky surf race in A minor @ 168 bpm, 8 bars ~ 11.4 s: pulse bass, organ-square lead, drums"""
    bpm = 168; b = 60 / bpm; L = 8 * 4 * b
    buf = np.zeros(int(L * SR))
    riff = ['A2', 'A2', 'C3', 'A2', 'D3', 'A2', 'D#3', 'E3']
    for i in range(64): add(buf, tone(hz(riff[i % 8]), b * 0.45, 'pulse', d=0.08, s=0.4, r=0.02), i * b / 2, 0.33)
    for i in range(32):
        add(buf, kick(), i * b, 0.9 if i % 2 == 0 else 0.4)
        if i % 2 == 1: add(buf, snare(seed=i), i * b, 0.6)
        add(buf, hat(seed=i), i * b + b / 2, 0.25)
    lead = ['E5', 'E5', 'G5', 'A5', 'C6', 'B5', 'A5', 'G5', 'E5', 'D5', 'E5', 'G5', 'A5', 'A5', 'C6', 'A5',
            'E5', 'E5', 'G5', 'A5', 'C6', 'D6', 'E6', 'D6', 'C6', 'B5', 'A5', 'G5', 'A5', 'A5', 'A5', 'A5']
    for i, n in enumerate(lead): add(buf, tone(hz(n), b * 0.9, 'square', d=0.15, s=0.5, r=0.05), i * b, 0.11)
    mz.save(buf, 'race_12s', lp=9000)


def porch():
    """tender porch ending in F major @ 80 bpm, 4 bars of 4 = 12 s: soft vib chords + a music-box tune"""
    b = 0.75; L = 4 * 4 * b
    buf = np.zeros(int(L * SR))
    prog = [['F3', 'A3', 'C4', 'E4'], ['D3', 'F3', 'A3', 'C4'], ['A#2', 'D3', 'F3', 'A3'], ['C3', 'E3', 'G3', 'A#3']]
    for bar, ch in enumerate(prog):
        add(buf, tone(hz(ch[0]) / 2, 4 * b, 'bass', d=0.8, s=0.3, r=0.3), bar * 4 * b, 0.6)
        for k, n in enumerate(ch): add(buf, tone(hz(n), 3.6 * b, 'vib', a=0.01, d=0.9, s=0.2, r=0.4), bar * 4 * b + k * 0.03, 0.14)
    mel = [('C5', 0, 1), ('A4', 1, 1), ('F5', 2, 2), ('E5', 4, 1), ('D5', 5, 1), ('A4', 6, 2), ('D5', 8, 1), ('C5', 9, 1),
           ('A#4', 10, 2), ('A4', 12, 1), ('G4', 13, 1), ('C5', 14, 2)]
    for n, st, du in mel: add(buf, tone(hz(n), du * b * 0.95, 'vib', a=0.003, d=0.5, s=0.1, r=0.3), st * b, 0.28)
    mz.save(buf, 'porch_12s', lp=7000)


if __name__ == '__main__':
    waltz(); race(); porch()
