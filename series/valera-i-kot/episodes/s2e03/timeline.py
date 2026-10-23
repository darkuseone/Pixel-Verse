"""S02E03 «Сорок банок» — timing for video (s2e03.py) and audio (mix.py). Built from BEATS like the movies:
  ('L', key, shot)   a line (voice/s2e03_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'valera-i-kot'
EP = 's2e03'
FPS = 30
MASTER = 0.68
VEP = 's2e03_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
MUFFLE = 'lowpass=f=1500,volume=1.3'
SEPIA = 'aecho=0.8:0.6:60:0.25,highpass=f=200'
VFX = {}
X = f'series/{SLUG}/sfx/'

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(v1='одному?!', z1='вернёшь.', c1='девятнадцатого.', t1='тридцать.', n1='графику.', v3='забивал!', v4='пять?!',
            v5='вернёте!', v6='природе.', c3='Пишите.', l1='Вареньице.')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'v1', 'hook'), ('L', 'z1', 'zina'), ('L', 'c1', 'cat_top'), ('L', 't1', 'shop'), ('L', 'n1', 'nina'),
    ('L', 'v3', 'buried'), ('L', 'v4', 'label'), ('L', 'v5', 'flashback'), ('L', 'v6', 'whisper'),
    ('L', 'c3', 'cat_log'), ('L', 'l1', 'lyuba'), ('P', 0.5, 'loop'),
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


TWIST = first('label')['t0']
T0 = {s['name']: s['t0'] for s in SHOTS}

SFX = [
    (X + 'jars_clink_crate.mp3', 0.0, 0.9), (S + 'doorbell_soviet_trill.mp3', 0.0, 0.25),
    (S + 'stairs_run.mp3', T0['zina'] + 0.2, 0.25),
    (X + 'jars_clink_crate.mp3', T0['cat_top'] + 0.3, 0.4),
    (S + 'shop_bell.mp3', T0['shop'], 0.35), (S + 'cash_register.mp3', T0['shop'] + 2.2, 0.4),
    (S + 'stamp.mp3', T0['nina'] + 1.6, 0.6),
    (S + 'junk_avalanche.mp3', T0['buried'] - 0.1, 0.8), (X + 'jars_clink_crate.mp3', T0['buried'] + 0.4, 0.9),
    (S + 'record_scratch.mp3', TWIST, 0.4), (S + 'heartbeat_slow.mp3', TWIST + 0.3, 0.45),
    (S + 'vhs_rewind.mp3', T0['flashback'] - 0.05, 0.4),
    (X + 'jar_lid_pop.mp3', T0['whisper'] + 0.3, 0.9), (S + 'carrot_crunch.mp3', T0['cat_log'] + 0.2, 0.7),
    (S + 'pencil_scribble.mp3', T0['cat_log'] + 1.6, 0.6),
    (S + 'doorbell_soviet_trill.mp3', T0['lyuba'] - 0.2, 0.3), (S + 'junk_avalanche.mp3', T0['loop'], 0.8),
]

BEDS = [
    (S + 'amb_flat_winter.mp3', 7.8, 0.0, T0['shop'], 0.3, False),
    (MUS + 'theme_panelka_15s.mp3', 14.6, 0.0, TWIST, 0.2, True),
    (S + 'amb_grocery_store.mp3', 7.8, T0['shop'], T0['nina'], 0.3, False),
    (S + 'amb_office_night.mp3', 7.8, T0['nina'], T0['buried'], 0.25, False),
    (MUS + 'new_year_15s.mp3', 14.6, T0['flashback'], T0['whisper'], 0.22, False),
    (MUS + 'operation_sneaky_15s.mp3', 14.6, T0['whisper'], DUR, 0.18, True),
    (S + 'amb_flat_winter.mp3', 7.8, T0['buried'], DUR, 0.3, False),
]
VGAIN = {'valera': 1.5, 'cat': 1.55, 'zina': 1.45, 'tamara': 1.45, 'nina': 1.45, 'lyuba': 1.45}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
