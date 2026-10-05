"""Quality check for SFX before they go into the library or a mix (rule 05.10.2026: no harsh «MIDI» hiss).
  python3 engine/sfxcheck.py file1.mp3 [file2.mp3 ...]
Prints the share of energy above 6 kHz, spectral flatness (1 = white noise), spectral centroid, envelope crest (transients) and RMS.
Verdict HARSH when HF>6k > 0.6 and crest < 2.5 (a flat, steady hiss): run it through EQ (lowpass ~5 kHz) or replace it."""
import sys, subprocess, numpy as np
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '44100', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
for p in sys.argv[1:]:
    x = load(p)
    n = 4096; hop = 2048
    frames = [x[i:i + n] * np.hanning(n) for i in range(0, len(x) - n, hop)]
    S = np.abs(np.fft.rfft(np.array(frames), axis=1)) ** 2 + 1e-12
    f = np.fft.rfftfreq(n, 1 / 44100)
    hf = S[:, f > 6000].sum() / S.sum()
    flat = np.mean(np.exp(np.mean(np.log(S[:, (f > 200) & (f < 16000)]), axis=1)) / np.mean(S[:, (f > 200) & (f < 16000)], axis=1))
    env = np.sqrt(np.convolve(x * x, np.ones(441) / 441, 'same'))
    crest = env.max() / (env.mean() + 1e-9)
    cent = (S * f).sum(axis=1).mean() / S.sum(axis=1).mean()
    rms = 20 * np.log10(np.sqrt(np.mean(x * x)) + 1e-9)
    verdict = 'HARSH' if hf > 0.6 and crest < 2.5 else 'ok'
    print(f'{p.split("/")[-1]:32s} dur={len(x)/44100:5.2f}s  HF>6k={hf:5.2f}  flat={flat:5.2f}  centroid={cent:6.0f}Hz  crest={crest:5.1f}  rms={rms:6.1f}dB  {verdict}')
