"""E01 «Я к вам на недельку!» (v2, 02.11.2026) — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'teshcha'
EP = 'ep01'
FPS = 30
LUFS = -14.0
VEP = 'ep01_t'
S = f'series/{SLUG}/sfx/'
MUS = f'series/{SLUG}/music/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(r1='недельку!', t1='денёчек!', t2='мужик!', r3='помыла.', t3='недельку!', s1='год.', t4='спать', r4='воздух!',
            p2='моё.', r5='Люся.')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'r1', 'hook'), ('L', 't1', 'tolik_cu'), ('L', 'r2', 'raisa_door'), ('L', 't2', 'manly'), ('L', 'r3', 'raisa_chair'),
    ('P', 0.2, 'run'), ('L', 't3', 'phone'), ('L', 's1', 'reveal'), ('L', 't4', 'nagod'), ('P', 0.45, 'teeth'), ('L', 'r4', 'balcony'),
    ('L', 'p2', 'pusya2'), ('P', 0.35, 'bell'), ('L', 'r5', 'lyusya'), ('L', 't5', 'loop'),
]
PAD = 0.07
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
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [s['name'] for s in SHOTS]
T0 = {s['name']: s['t0'] for s in SHOTS}
T1 = {s['name']: s['t1'] for s in SHOTS}
TWIST = T0['reveal']

SFX = [
    (S + 'doorbell_bird.mp3', 0.0, 0.6, 0.0, 1.15), (C + 'door_apartment_open.mp3', 0.15, 0.5),
    (C + 'canvas_bag_drop.mp3', T0['raisa_door'] + 0.3, 0.9), (C + 'bottle_clink.mp3', T0['raisa_door'] + 0.35, 0.35),
    (S + 'lift_doors_open.mp3', T0['raisa_door'] + 1.0, 0.5),
    (S + 'bags_slide_pile.mp3', T0['raisa_door'] + 1.6, 0.8),
    (C + 'chair_creak.mp3', T0['manly'] + 0.05, 0.9), (C + 'chair_creak.mp3', T0['manly'] + 0.35, 0.6),
    (C + 'floor_squeak.mp3', T0['raisa_chair'] + 1.35, 0.8),
    (C + 'slipper_steps.mp3', T0['run'] - 0.3, 0.6, 0.0, 0.8),
    (C + 'phone_dial_tone.mp3', T0['phone'] + 0.0, 0.25, 0.0, 1.2),
    (C + 'keys_lock.mp3', TWIST + 0.2, 0.5, 0.0, 1.2),
    (S + 'twist_hit.mp3', TWIST + 0.05, 0.8), (C + 'vinyl_scratch.mp3', TWIST, 0.4),
    (C + 'whoosh_3.mp3', T0['nagod'], 0.6),
    (C + 'teeth_chatter.mp3', T0['teeth'], 0.9),
    (C + 'cloth_rustle.mp3', T0['pusya2'] + 0.1, 0.9),
    (S + 'doorbell_bird.mp3', T0['bell'] - 0.15, 0.75),
    (C + 'teeth_chatter.mp3', T0['loop'] + 0.1, 0.5),
]

BEDS = [
    (CM + 'ukulele_loop.mp3', 8.3, 0.0, TWIST, 1.3, True),
    (CM + 'sad_orchestral.mp3', 59.5, TWIST + 0.6, DUR, 1.2, True),
    (C + 'wind_inside_1.mp3', 11.5, T0['teeth'], T0['pusya2'], 0.8, False),
    (C + 'wind_inside_1.mp3', 11.5, T0['loop'], DUR, 0.7, False),
]
VGAIN = {'tolik': 1.45, 'raisa': 1.95, 'pusya': 2.1, 'sveta': 1.7}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
