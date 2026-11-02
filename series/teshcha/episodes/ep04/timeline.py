"""E04 «Шапку надень!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'teshcha'
EP = 'ep04'
FPS = 30
LUFS = -14.0
VEP = 'ep04_t'
S = f'series/{SLUG}/sfx/'
MUS = f'series/{SLUG}/music/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(r1='надень!', t1='год!', r2='менингит!', t2='мужик!', r3='шапке!', t3='свобода!', l1='звонила.', b1='шапку,', t4='видит?!',
            p1='помогло.')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'r1', 'hook'), ('L', 't1', 'tolik_mad'), ('L', 'r2', 'meningit'), ('L', 't2', 'muzhik'), ('L', 'r3', 'hatdown'),
    ('L', 't3', 'yard'), ('P', 0.8, 'bus'), ('L', 'l1', 'twist'), ('L', 'b1', 'babki'), ('L', 't4', 'inhat'), ('P', 1.0, 'sms'),
    ('L', 'p1', 'button'), ('P', 0.45, 'loop'),
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
TWIST = T0['twist']

SFX = [
    (C + 'cloth_rustle.mp3', 0.05, 0.7), (C + 'zipper.mp3', T0['tolik_mad'] + 0.2, 0.4),
    (C + 'slipper_steps.mp3', T0['meningit'] + 0.1, 0.35),
    (C + 'cloth_rustle.mp3', T0['hatdown'] + 0.05, 0.8), (C + 'boing_cartoon.mp3', T0['hatdown'] + 0.15, 0.35),
    (C + 'whoosh_1.mp3', T0['yard'] - 0.1, 0.5), (C + 'snow_steps.mp3', T0['yard'], 0.6, 0.0, 2.0),
    (C + 'cloth_rustle.mp3', T0['yard'] + 1.4, 0.6), (C + 'zipper.mp3', T0['yard'] + 2.6, 0.5),
    (C + 'car_arrive_stop.mp3', T0['bus'] - 2.6, 0.9, 4.0, 9.0), (C + 'bus_horn.mp3', T0['bus'] + 0.05, 0.5),
    (C + 'sliding_door_open.mp3', TWIST - 0.1, 0.8), (S + 'twist_hit.mp3', TWIST, 0.6), (C + 'vinyl_scratch.mp3', TWIST, 0.35),
    (C + 'gong_strong.mp3', T0['babki'] + 0.02, 0.18),
    (C + 'sms_message.mp3', T0['sms'] + 0.05, 0.8),
    (C + 'small_dog_bark.mp3', T0['button'] + 2.9, 0.2),
    (C + 'rimshot_joke.mp3', T0['loop'] - 0.05, 0.55),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_shoe_shop.mp3', 59.5, 0.0, T0['yard'], 0.8, True, VOICE_DIP),
    (C + 'wind_whistle.mp3', 12.0, T0['yard'], T0['twist'] + 0.4, 0.5, False),
    (CM + 'komiku_fetch_contest.mp3', 59.5, T0['yard'] + 0.2, DUR, 0.75, True, VOICE_DIP),
]
VGAIN = {'tolik': 1.85, 'raisa': 2.2, 'pusya': 2.3, 'sveta': 2.0, 'lyusya': 2.3, 'babki': 2.2}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
