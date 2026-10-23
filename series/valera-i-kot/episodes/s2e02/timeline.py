"""S02E02 «Восемь утра» — timing for video (s2e02.py) and audio (mix.py). Built from BEATS like the movies:
  ('L', key, shot)   a line (voice/s2e02_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'valera-i-kot'
EP = 's2e02'
FPS = 30
MASTER = 0.62
VEP = 's2e02_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
MUFFLE = 'lowpass=f=1500,volume=1.3'
VFX = {'zina': MUFFLE}
X = f'series/{SLUG}/sfx/'

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(v1='Суббота!', c1='год.', v2='армии!', g1='Чего?!', v3='уставу!', g2='полку!', v4='плацу!', z1='утра!', v5='Чего?!',
            c2='рекорд.')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'v1', 'hook'), ('L', 'c1', 'cat_pot'), ('P', 2.0, 'morse'), ('P', 1.6, 'notice'),
    ('L', 'v2', 'march'), ('L', 'g1', 'door'), ('L', 'v3', 'v_shout'), ('L', 'g1', 'door2'),
    ('L', 'g2', 'shelf'), ('L', 'v4', 'drill'), ('L', 'z1', 'zina'), ('L', 'v5', 'deaf'),
    ('L', 'c2', 'cat_sill'), ('P', 0.6, 'loop'),
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


TWIST = first('shelf')['t0']
T0 = {s['name']: s['t0'] for s in SHOTS}

SFX = [
    (X + 'hammer_drill_wall.mp3', 0.0, 0.75), (X + 'alarm_bell_old.mp3', 0.0, 0.35), (X + 'plaster_crumble.mp3', 0.3, 2.5),
    (X + 'plaster_crumble.mp3', T0['cat_pot'] + 0.2, 2.5),
    (X + 'mop_knock_ceiling.mp3', T0['morse'], 3.0), (X + 'drill_bursts.mp3', T0['morse'] + 0.9, 0.6),
    (S + 'paper_unroll.mp3', T0['notice'], 0.35),
    (S + 'stairs_run.mp3', T0['march'], 0.45), (S + 'police_whistle.mp3', T0['march'] + 0.7, 0.3),
    (X + 'steel_door_open.mp3', T0['door'] - 0.1, 2.5), (X + 'drill_bursts.mp3', T0['door2'] - 0.05, 0.3),
    (S + 'record_scratch.mp3', TWIST, 0.4), (S + 'tape_measure.mp3', TWIST + 0.8, 0.5),
    (X + 'hammer_drill_wall.mp3', T0['drill'], 0.55), (X + 'plaster_crumble.mp3', T0['drill'] + 0.4, 2.5),
    (X + 'mop_knock_ceiling.mp3', T0['zina'] - 0.05, 3.0),
    (S + 'pencil_scribble.mp3', T0['cat_sill'] + 0.4, 0.6),
    (X + 'hammer_drill_wall.mp3', T0['loop'], 0.8),
]

BEDS = [
    (S + 'amb_flat_winter.mp3', 7.8, 0.0, T0['march'], 0.35, False),
    (MUS + 'theme_panelka_15s.mp3', 14.6, 0.0, TWIST, 0.2, True),
    (S + 'amb_basement.mp3', 7.8, T0['march'], TWIST, 0.2, False),
    (MUS + 'operation_sneaky_15s.mp3', 14.6, TWIST + 0.3, DUR, 0.2, True),
    (S + 'amb_flat_winter.mp3', 7.8, T0['cat_sill'], DUR, 0.35, False),
]
VGAIN = {'valera': 1.5, 'cat': 1.55, 'gena': 1.45, 'zina': 1.45}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
