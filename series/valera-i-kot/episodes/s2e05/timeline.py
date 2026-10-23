"""S02E05 «Посыпано» — timing for video (s2e05.py) and audio (mix.py). Built from BEATS like the movies:
  ('L', key, shot)   a line (voice/s2e05_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'valera-i-kot'
EP = 's2e05'
FPS = 30
MASTER = 0.68
VEP = 's2e05_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
MUFFLE = 'lowpass=f=1500,volume=1.3'
SEPIA = 'aecho=0.8:0.6:60:0.25,highpass=f=200'
VFX = {}
X = f'series/{SLUG}/sfx/'

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(v1='посыпано?!', l1='тулуп.', c1='открыт.', v2='святое!', z1='герой!', v3='посыпал!', n1='УК.', v4='спас!',
            n2='графику.', c2='Пишите.')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'v1', 'hook'), ('L', 'l1', 'judges'), ('L', 'c1', 'cat_tea'), ('L', 'v2', 'sand'), ('L', 'z1', 'sanding'),
    ('P', 1.3, 'medal'), ('L', 'v3', 'sign'), ('L', 'n1', 'fine'), ('L', 'v4', 'protest'), ('L', 'n2', 'nina2'),
    ('P', 1.6, 'slip'), ('L', 'c2', 'cat_log'), ('P', 0.6, 'loop'),
]
PAD = 0.1
SHOTS, VOICE = [], []
t = 0.0
for b in BEATS:
    if b[0] == 'L':
        k = b[1]; d = CLIP[k] + PAD
        VOICE.append((k, VEP, k, round(t + 0.02, 3), 0.0, CLIP[k], LINES[k][0], _cap(k)))
        SHOTS.append(dict(name=b[2], t0=t, t1=t + d, key=k))
    else:
        d = b[1]; SHOTS.append(dict(name=b[2], t0=t, t1=t + d))
    t += d
DUR = round(t, 3)
CUTS = [s['t0'] for s in SHOTS]
NAMES = [s['name'] for s in SHOTS]


def first(name):
    return next(s for s in SHOTS if s['name'] == name)


TWIST = first('fine')['t0']
T0 = {s['name']: s['t0'] for s in SHOTS}

SFX = [
    (X + 'ice_slip_fall.mp3', 0.0, 0.8), (S + 'whoosh.mp3', 0.2, 0.5), (S + 'snow_crawl.mp3', 0.1, 0.4),
    (S + 'crowd_cheer_short.mp3', T0['judges'] + 0.1, 0.12),
    (S + 'kettle_whistle.mp3', T0['cat_tea'], 0.12),
    (S + 'boots_stomp.mp3', T0['sand'] + 0.1, 0.5), (S + 'bucket_clang.mp3', T0['sand'] + 0.6, 0.45),
    (X + 'sand_scatter.mp3', T0['sanding'], 0.5), (X + 'sand_scatter.mp3', T0['sanding'] + 1.6, 0.4), (S + 'snow_steps.mp3', T0['sanding'], 0.4),
    (S + 'brass_fanfare_short.mp3', T0['medal'], 0.3),
    (S + 'paper_unroll.mp3', T0['sign'] + 0.2, 0.4),
    (S + 'record_scratch.mp3', TWIST, 0.4), (S + 'receipt_printer.mp3', TWIST + 0.6, 0.45), (S + 'paper_crumple_slap.mp3', TWIST + 2.3, 0.4),
    (S + 'stamp.mp3', T0['nina2'] + 1.6, 0.5),
    (S + 'store_doors_cold.mp3', T0['slip'], 0.35), (X + 'ice_slip_fall.mp3', T0['slip'] + 0.35, 0.9), (S + 'sad_trombone.mp3', T0['slip'] + 0.9, 0.25),
    (S + 'pencil_scribble.mp3', T0['cat_log'] + 0.4, 0.6),
    (X + 'ice_slip_fall.mp3', T0['loop'], 0.8),
]

BEDS = [
    (S + 'amb_winter_yard.mp3', 7.8, 0.0, T0['cat_tea'], 0.4, False),
    (MUS + 'theme_panelka_15s.mp3', 14.6, 0.0, TWIST, 0.2, True),
    (S + 'amb_flat_winter.mp3', 7.8, T0['cat_tea'], T0['sand'], 0.35, False),
    (S + 'amb_winter_yard.mp3', 7.8, T0['sand'], T0['cat_log'], 0.35, False),
    (MUS + 'operation_sneaky_15s.mp3', 14.6, TWIST + 0.4, DUR, 0.18, True),
    (S + 'amb_flat_winter.mp3', 7.8, T0['cat_log'], DUR, 0.3, False),
]
VGAIN = {'valera': 1.5, 'cat': 1.55, 'zina': 1.45, 'lyuba': 1.45, 'nina': 1.45}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
