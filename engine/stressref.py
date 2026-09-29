"""Stress check against reference takes. Generate the same line twice with the stress mark on each candidate
syllable (same voice/tags), then compare a take to both: DTW-align on MFCC (what is said), then measure the
distance of the prosody (loudness + pitch) along the path. The take is closer to the reference with its stress.
  python3 engine/stressref.py take.mp3 ref_right.mp3 ref_wrong.mp3"""
import sys
import numpy as np
from stress import pcm, SR

HOP, WIN = 160, 400


def feats(path):
    x = pcm(path)
    n = 1 + (len(x) - WIN) // HOP
    fr = np.stack([x[i * HOP:i * HOP + WIN] for i in range(n)]) * np.hamming(WIN)
    spec = np.abs(np.fft.rfft(fr, 512)) ** 2
    f = np.linspace(0, SR / 2, spec.shape[1])
    mel = lambda hz: 2595 * np.log10(1 + hz / 700)
    edges = np.interp(np.linspace(mel(60), mel(7600), 28), mel(f), f)
    fb = np.stack([np.clip(np.minimum((f - a) / (b - a), (c - f) / (c - b)), 0, None) for a, b, c in zip(edges, edges[1:], edges[2:])])
    lm = np.log(spec @ fb.T + 1e-9)
    k = np.arange(26)
    dct = np.cos(np.pi / 26 * (k[:, None] + 0.5) * np.arange(13)[None, :])
    mfcc = lm @ dct
    mfcc -= mfcc.mean(0)
    en = 10 * np.log10((fr ** 2).mean(1) + 1e-9)
    pit = np.zeros(n)
    for i in range(n):
        w = fr[i] - fr[i].mean()
        if en[i] < en.max() - 30: continue
        ac = np.correlate(w, w, 'full')[WIN - 1:]
        lo, hi = SR // 450, SR // 70
        j = lo + int(np.argmax(ac[lo:hi]))
        if ac[j] > 0.35 * ac[0]: pit[i] = SR / j
    keep = en > en.max() - 35                                        # trim silence
    idx = np.where(keep)[0]
    s = slice(idx[0], idx[-1] + 1)
    en = en[s] - en[s].max()
    p = pit[s]
    lp = np.where(p > 0, np.log(np.maximum(p, 1)) - np.log(np.median(p[p > 0])), np.nan)
    return mfcc[s], en, lp


def dtw(a, b):
    D = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1))
    n, m = D.shape
    C = np.full((n + 1, m + 1), np.inf); C[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            C[i, j] = D[i - 1, j - 1] + min(C[i - 1, j], C[i, j - 1], C[i - 1, j - 1])
    i, j, path = n, m, []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        k = np.argmin([C[i - 1, j - 1], C[i - 1, j], C[i, j - 1]])
        if k == 0: i, j = i - 1, j - 1
        elif k == 1: i -= 1
        else: j -= 1
    return path[::-1]


def prosody_dist(t, r):
    (ma, ea, pa), (mb, eb, pb) = t, r
    path = dtw(ma, mb)
    de = np.mean([abs(ea[i] - eb[j]) for i, j in path])
    dp = [abs(pa[i] - pb[j]) for i, j in path if not (np.isnan(pa[i]) or np.isnan(pb[j]))]
    return de / 6.0 + (np.mean(dp) / 0.12 if dp else 0.0)


if __name__ == '__main__':
    t, ok, bad = (feats(p) for p in sys.argv[1:4])
    d_ok, d_bad = prosody_dist(t, ok), prosody_dist(t, bad)
    print(sys.argv[1].split('/')[-1], f'right {d_ok:.2f}  wrong {d_bad:.2f}  ->', 'RIGHT' if d_ok < d_bad else 'WRONG',
          f'(refs apart: {prosody_dist(ok, bad):.2f})')
