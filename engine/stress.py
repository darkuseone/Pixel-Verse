"""Stress check for generated Russian lines: for one word, per-vowel duration, loudness and pitch from Scribe character
timestamps. The stressed vowel is usually the longest + loudest + highest (phrase-final words stretch every vowel, so
look at loudness/pitch there).  python3 engine/stress.py file.mp3 WORD [WORD ...]"""
import subprocess, sys
import numpy as np
from stt import transcribe

SR = 16000


def pcm(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def f0(x):
    """median pitch (Hz) of a short chunk by autocorrelation (70..400 Hz), 0 if unvoiced"""
    if len(x) < 400: return 0.0
    out = []
    for i in range(0, len(x) - 400, 160):
        w = x[i:i + 400] - x[i:i + 400].mean()
        if np.sqrt((w ** 2).mean()) < 0.01: continue
        ac = np.correlate(w, w, 'full')[399:]
        lo, hi = SR // 400, SR // 70
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.3 * ac[0]: out.append(SR / k)
    return float(np.median(out)) if out else 0.0


def check(path, words):
    d = transcribe(path, gran='character')
    x = pcm(path)
    res = {}
    for w in d.get('words', []):
        key = w['text'].lower().strip('.,!?…—«»"')
        if w.get('type') != 'word' or key not in [q.lower() for q in words]: continue
        rows = []
        for c in w.get('characters', []):
            if c['text'].lower() not in 'аеёиоуыэюя': continue
            seg = x[int(c['start'] * SR):int(c['end'] * SR)]
            db = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-6) if len(seg) else -99
            rows.append((c['text'], round(c['end'] - c['start'], 2), round(float(db), 1), round(f0(seg))))
        res[key] = rows
    return res


if __name__ == '__main__':
    for k, rows in check(sys.argv[1], sys.argv[2:]).items():
        print(sys.argv[1].split('/')[-1], k, '  '.join(f'{v}:{d}s/{db}dB/{p}Hz' for v, d, db, p in rows))
