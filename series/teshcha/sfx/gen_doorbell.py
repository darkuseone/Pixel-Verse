"""Soviet electronic «bird» doorbell (звонок-соловей): the real thing was a tone generator, so we model it: a run of short
warbling chirps (pitch sweeps ~1.3–2.6 kHz with vibrato), soft sine timbre, small-speaker band-pass, a little hallway echo.
  python3 gen_doorbell.py  -> doorbell_bird.mp3"""
import subprocess, pathlib
import numpy as np
SR = 44100
HERE = pathlib.Path(__file__).resolve().parent


def chirp(f0, f1, dur, vib=0.0):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * (t / dur) ** 0.7 + vib * np.sin(2 * np.pi * 38 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(1, t / 0.006) * np.exp(-t / (dur * 0.9)) * np.minimum(1, (dur - t) / 0.01)
    return (np.sin(ph) + 0.18 * np.sin(2 * ph)) * env


def phrase():
    out = []
    pat = [(2200, 1500, 0.07, 60), (2300, 1600, 0.07, 60), (2400, 1700, 0.07, 60), (1500, 2500, 0.09, 90),
           (2500, 1400, 0.12, 120), (1800, 2200, 0.06, 40), (1800, 2200, 0.06, 40), (2100, 1300, 0.16, 150)]
    for f0, f1, d, v in pat:
        out.append(chirp(f0, f1, d, v)); out.append(np.zeros(int(0.025 * SR)))
    return np.concatenate(out)


buf = np.concatenate([phrase(), np.zeros(int(0.18 * SR)), phrase(), np.zeros(int(0.35 * SR))])
buf = buf / np.abs(buf).max() * 0.7
raw = HERE / 'doorbell_bird.f32'
buf.astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', str(raw), '-af',
                'highpass=f=500,lowpass=f=4200,aecho=0.8:0.5:35|70:0.25|0.12,loudnorm=I=-20:TP=-3', '-ac', '2', '-b:a', '160k',
                str(HERE / 'doorbell_bird.mp3')], check=True)
raw.unlink()
print(HERE / 'doorbell_bird.mp3')
