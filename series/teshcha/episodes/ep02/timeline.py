"""E02 «Сделай потише!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'teshcha'
EP = 'ep02'
FPS = 30
LUFS = -14.0
VEP = 'ep02_t'
S = f'series/{SLUG}/sfx/'
MUS = f'series/{SLUG}/music/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(t1='громкость!', r1='сериал!', t3='морозилку.', r3='запасной', p1='слышу.', t4='мужик!', r4='ЖЕНАТ!', t5='телевизора!',
            r5='погромче?')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 't1', 'hook'), ('L', 'r1', 'tv_raisa'), ('L', 't3', 'freezer'), ('L', 'r3', 'spare'), ('L', 't4', 'headphones'),
    ('L', 'r4', 'twist'), ('P', 0.9, 'bang'), ('L', 'p1', 'pusya'), ('L', 't5', 'panic'), ('L', 'r5', 'button'), ('P', 0.5, 'loop'),
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
    (C + 'whoosh_1.mp3', 0.0, 0.3),
    (C + 'cloth_rustle.mp3', 0.15, 0.8),
    (C + 'slipper_steps.mp3', T0['freezer'] + 0.0, 0.6, 0.0, 1.0),
    (C + 'fridge_door.mp3', T0['freezer'] + 0.5, 0.8), (C + 'freezer_close.mp3', T0['freezer'] + 1.6, 0.9),
    (C + 'phone_key_click.mp3', T0['spare'] + 1.6, 0.9), (C + 'phone_key_click.mp3', T0['spare'] + 1.75, 0.9),
    (C + 'cloth_rustle.mp3', T0['headphones'] + 0.2, 0.8),
    (S + 'twist_hit.mp3', TWIST + 0.0, 0.7), (C + 'vinyl_scratch.mp3', TWIST, 0.35),
    (C + 'anvil_clank.mp3', T0['bang'] + 0.0, 0.6), (C + 'anvil_clank.mp3', T0['bang'] + 0.28, 0.7), (C + 'anvil_clank.mp3', T0['bang'] + 0.55, 0.8),
    (C + 'door_knock.mp3', T0['bang'] + 0.1, 0.8), (C + 'door_knock.mp3', T0['pusya'] + 0.1, 0.5),
    (C + 'rimshot_joke.mp3', T0['loop'] - 0.05, 0.55),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (C + 'wind_inside_1.mp3', 11.5, 0.0, T0['tv_raisa'], 0.6, False),
    (CM + 'komiku_fetch_contest.mp3', 41.5, 0.0, TWIST, 0.8, True, VOICE_DIP),
    (CM + 'komiku_mandolin.mp3', 59.5, TWIST + 0.4, DUR, 0.8, True, VOICE_DIP),
]
VGAIN = {'tolik': 1.85, 'raisa': 2.2, 'pusya': 2.3, 'sveta': 2.0}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
