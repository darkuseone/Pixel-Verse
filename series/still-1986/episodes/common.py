"""Shared helpers for «STILL 1986» episodes E02+ (timeline lines with measured durations, faces, close-ups, clipped actors).
Audio rule (owner 12.11.2026, after the pilot): voices loud and clear, music low (bed <= 0.14, VGAIN >= 2.0, no echo on voices)."""
import sys, pathlib, subprocess, math, functools
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
import paths as P
from props import v86kit as K, v86cast as C, mimic as M

SLUG = 'still-1986'
TAB = (C.XTRA, C.EXPR)
VGAIN = {'vince': 1.9, 'fran': 2.3, 'rey': 2.3, 'tiffany': 2.2, 'diaz': 2.2, 'gary': 2.1, 'roofe': 2.0}
VFX = {'fran': 'highpass=f=110', 'roofe': 'highpass=f=180,lowpass=f=7500'}
MUSIC = 'series/still-1986/music/synth_theme_phone.mp3'
MUSIC_DIP = 'equalizer=f=1500:t=q:w=1.6:g=-9'


@functools.lru_cache(None)
def dur(ep, key):
    f = P.series(SLUG) / 'voice' / f'{ep}_t' / f'{key}.mp3'
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout) - 0.02


def seq(items, start=0.0, gap=0.10):
    """items: (key, who, text) | (key, who, text, extra_pause_before) | (key, who, text, pause, src_ep); -> VOICE rows, end time"""
    out, t = [], start
    for it in items:
        key, who, text = it[:3]
        t += it[3] if len(it) > 3 else 0.0
        src = it[4] if len(it) > 4 else EP
        d = dur(src, key)
        out.append((key + ('' if src == EP else '_' + src), f'{src}_t', key, round(t, 2), 0.0, round(d, 2), who, text))
        t += d + gap
    return out, round(t - gap, 2)


EP = 'ep02'


def at(VOICE, vid):
    for r in VOICE:
        if r[0] == vid: return r[3]
    raise KeyError(vid)


def end(VOICE, vid):
    for r in VOICE:
        if r[0] == vid: return round(r[3] + r[5] - r[4], 2)
    raise KeyError(vid)


class Faces:
    def __init__(s, epi, tracks):
        s.epi = epi
        s.F = {who: M.Face(tr, TAB, seed=i * 3 + 1) for i, (who, tr) in enumerate(tracks.items())}

    def __call__(s, who, t, base=(0.7, 0.0), **kw):
        m = M.mouth(s.epi.talk, who, t)
        F = s.F[who]
        return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


class Clip:
    """draw an actor only inside a world rectangle (a person behind a booth window / inside a cab)"""
    direct = True

    def __init__(s, act, rect):
        s.a, s.rect = act, rect

    def __call__(s, big, v, lt):
        tmp = big.copy()
        s.a(tmp, v, lt)
        x0, y0 = v.opt(s.rect[0], s.rect[1]); x1, y1 = v.opt(s.rect[2], s.rect[3])
        x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(big.shape[1], int(x1)), min(big.shape[0], int(y1))
        if x0 < x1 and y0 < y1: big[y0:y1, x0:x1] = tmp[y0:y1, x0:x1]
        s.last = getattr(s.a, 'last', None)


def cu(name, light, fn, t, cx, cy, Z, head, s, kw, flip=False, blur=7, fx_=None, back=(), front=(), kick=(0, 0), rim=None, bokeh=True):
    """close-up: hero's head pinned at output `head`, s output px per sprite px, background softly out of focus"""
    v = K.V(name, cx, cy, Z)
    a = K.A(fn, *K.wpt(v, *head), s, pin='head', t=t, flip=flip, **({'rim': rim} if rim else {}), **kw)
    a.near = 0.995
    def pre(big, _): big[:] = K.blur(big, blur)
    return K.shot(name, light, cx, cy, Z, acts=list(back) + [a] + list(front), focus=0.99, dof_k=0, pre=pre, fx_=fx_, t=t, kick=kick,
                  bokeh_=bokeh), a, v


def overlay_scaled(big, img, x, y, k=1.0):
    from PIL import Image
    import overlays as O
    if k != 1.0: img = np.array(Image.fromarray(img).resize((int(img.shape[1] * k), int(img.shape[0] * k)), Image.NEAREST))
    O.overlay(big, img, int(x), int(y), 1.0)
    return img.shape


def beds(DUR, amb, music=True, t_cut=None):
    b = [(amb, 8.0, 0.0, DUR, 0.40, True)]
    if music:
        if t_cut:
            b += [(MUSIC, 15.0, 0.0, t_cut, 0.14, True, MUSIC_DIP), (MUSIC, 15.0, t_cut + 0.6, DUR, 0.14, True, MUSIC_DIP)]
        else:
            b.append((MUSIC, 15.0, 0.0, DUR, 0.14, True, MUSIC_DIP))
    return b
