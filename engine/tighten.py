"""Tighten TTS takes: trim leading/trailing silence, shrink inner pauses, optional tempo per speaker.
  python3 engine/tighten.py <slug> <ep>       # voice/<ep>/*.mp3 -> voice/<ep>_t/*.mp3 (+ bounds json)
Config in series/<slug>/voice/<ep>/tighten.json (optional):
  {"tempo": {"dale": 1.06}, "gap": 0.10, "keep": {"e2": 0.30}, "tempo_key": {"f3": 1.15}}   # keep: per-line pause to keep (seconds);
                                                                                           # tempo_key: per-line tempo (wins over the speaker's)
The tightened clips are what timeline.py / mix.py use (a=0, b=dur), so captions and lip-flap stay in sync."""
import json, subprocess, sys
import numpy as np
import paths as P

SR = 44100
THR = 0.035


def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def envelope(a, hop=0.01, win=0.03):
    h, n = int(SR * hop), int(SR * win)
    e = np.array([np.sqrt(np.mean(a[i:i + n] ** 2) + 1e-12) for i in range(0, max(1, len(a) - n), h)])
    return e / (e.max() + 1e-9)


def tighten(a, gap, minsil=0.20, pad=0.03):
    """returns spliced float32 audio; inner pauses longer than minsil shrink to `gap`"""
    e = envelope(a); v = e > THR
    idx = np.nonzero(v)[0]
    if len(idx) == 0: return a
    segs = []; s = idx[0]; last = idx[0]
    for i in idx[1:]:
        if (i - last) * 0.01 > minsil:
            segs.append((s, last)); s = i
        last = i
    segs.append((s, last))
    out = []; fade = int(SR * 0.006)
    for k, (s, e_) in enumerate(segs):
        x = a[max(0, int((s * 0.01 - pad) * SR)):int((e_ * 0.01 + 0.06) * SR)].copy()
        x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
        out.append(x)
        if k + 1 < len(segs): out.append(np.zeros(int(SR * gap), np.float32))
    return np.concatenate(out)


def write_mp3(x, path, tempo=1.0):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-']
    if abs(tempo - 1) > 1e-3: cmd += ['-af', f'atempo={tempo}']
    cmd += ['-c:a', 'libmp3lame', '-b:a', '192k', str(path)]
    subprocess.run(cmd, input=x.tobytes(), check=True)


def run(slug, ep):
    base = P.series(slug) / 'voice'
    cfg = json.load(open(base / ep / 'tighten.json')) if (base / ep / 'tighten.json').exists() else {}
    L = json.load(open(base / ep / 'lines.json'))
    dst = base / f'{ep}_t'; dst.mkdir(exist_ok=True)
    total = 0
    for k, (who, txt) in L.items():
        a = load(base / ep / f'{k}.mp3')
        x = tighten(a, cfg.get('keep', {}).get(k, cfg.get('gap', 0.10)))
        tempo = cfg.get('tempo_key', {}).get(k, cfg.get('tempo', {}).get(who, 1.0))
        write_mp3(x, dst / f'{k}.mp3', tempo)
        d = len(x) / SR / tempo; total += d
        print(f'{k:3s} {who:6s} {len(a) / SR:5.2f}s -> {d:5.2f}s')
    print('total %.1fs' % total)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
