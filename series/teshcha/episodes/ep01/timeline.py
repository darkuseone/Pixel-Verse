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
    (S + 'doorbell_soviet.mp3', 0.0, 0.25), (S + 'door_open_creak.mp3', 0.05, 0.7),
    (S + 'dog_tags_shiver.mp3', 0.5, 0.5),
    (S + 'bag_thud_jars.mp3', T0['raisa_door'] + 0.3, 0.8),
    (S + 'lift_doors_open.mp3', T0['raisa_door'] + 1.0, 0.7),
    (S + 'bags_slide_pile.mp3', T0['raisa_door'] + 1.6, 1.0),
    (S + 'armchair_springs.mp3', T0['manly'] + 0.05, 0.9),
    (S + 'wet_floor_squeak.mp3', T0['raisa_chair'] + 1.4, 0.5),
    (S + 'slippers_shuffle.mp3', T0['run'] - 0.2, 0.8),
    (S + 'phone_call_tone.mp3', T0['phone'] + 0.0, 0.35),
    (S + 'keys_jingle.mp3', TWIST + 0.15, 0.6),
    (S + 'twist_hit.mp3', TWIST + 0.05, 0.9), (S + 'vinyl_scratch.mp3', TWIST, 0.5),
    (S + 'twist_hit.mp3', T0['nagod'], 0.4),
    (S + 'teeth_chatter_man.mp3', T0['teeth'], 0.75), (S + 'campbed_creak.mp3', T0['teeth'] + 0.1, 0.5),
    (S + 'blanket_rustle.mp3', T0['pusya2'] + 0.1, 0.7),
    (S + 'doorbell_soviet.mp3', T0['bell'], 0.55),
    (S + 'teeth_chatter_man.mp3', T0['loop'] + 0.2, 0.4),
]

BEDS = [
    (S + 'amb_stairwell.mp3', 7.8, 0.0, T0['manly'], 2.6, False),
    (MUS + 'sitcom_theme_15s.mp3', 15.0, 0.0, TWIST, 0.2, True),
    (S + 'amb_flat_tv.mp3', 7.8, T0['manly'], T0['phone'], 2.4, False),
    (S + 'amb_stairwell.mp3', 7.8, T0['phone'], T0['teeth'], 2.6, False),
    (MUS + 'sitcom_uhoh_15s.mp3', 15.0, TWIST + 0.5, DUR, 0.22, True),
    (S + 'amb_balcony_wind.mp3', 7.8, T0['teeth'], T0['pusya2'], 0.5, False),
    (S + 'amb_flat_tv.mp3', 7.8, T0['pusya2'], T0['loop'], 2.4, False),
    (S + 'amb_balcony_wind.mp3', 7.8, T0['loop'], DUR, 0.45, False),
]
VGAIN = {'tolik': 1.45, 'raisa': 1.45, 'pusya': 1.6, 'sveta': 1.45}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
