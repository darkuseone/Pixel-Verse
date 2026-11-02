"""E03 «Ещё тарелочку!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'teshcha'
EP = 'ep03'
FPS = 30
LUFS = -14.0
VEP = 'ep03_t'
S = f'series/{SLUG}/sfx/'
MUS = f'series/{SLUG}/music/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(r1='тарелочку!', t1='пятую', r2='горячее.', t2='диете!', r3='хлеба.', t3='выручай.', r4='добавки!', p1='Толик.',
            s1='поправился!', r5='кормила,')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'r1', 'hook'), ('L', 't1', 'tolik_full'), ('L', 'r2', 'hot'), ('L', 't2', 'diet'), ('L', 'r3', 'olivier'),
    ('L', 't3', 'under'), ('P', 0.35, 'peek'), ('L', 'r4', 'twist'), ('L', 'p1', 'ball'), ('L', 's1', 'sveta'), ('L', 'r5', 'button'),
    ('P', 0.45, 'loop'),
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
    (C + 'bottle_clink.mp3', 0.05, 0.5), (C + 'bottle_clink.mp3', 0.45, 0.4),
    (C + 'chair_creak.mp3', T0['tolik_full'] + 0.2, 0.5),
    (C + 'bottle_clink.mp3', T0['hot'] + 0.4, 0.6), (C + 'canvas_bag_drop.mp3', T0['hot'] + 0.5, 0.4),
    (C + 'bottle_clink.mp3', T0['olivier'] + 0.6, 0.6), (C + 'boing_cartoon.mp3', T0['olivier'] + 1.0, 0.25),
    (C + 'cloth_rustle.mp3', T0['under'] + 0.1, 0.7),
    (C + 'whoosh_3.mp3', T0['peek'], 0.6),
    (S + 'twist_hit.mp3', TWIST + 0.0, 0.6), (C + 'boing_cartoon.mp3', TWIST + 0.05, 0.6), (C + 'vinyl_scratch.mp3', TWIST, 0.35),
    (C + 'small_dog_bark.mp3', T0['ball'] + 3.6, 0.25),
    (C + 'door_apartment_open.mp3', T0['sveta'] - 0.2, 0.5), (C + 'keys_on_table.mp3', T0['sveta'] + 0.3, 0.5),
    (C + 'rimshot_joke.mp3', T0['loop'] - 0.05, 0.55),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_mandolin.mp3', 59.5, 0.0, TWIST, 0.8, True, VOICE_DIP),
    (CM + 'komiku_weekly_fair.mp3', 59.5, TWIST + 0.3, DUR, 0.8, True, VOICE_DIP),
]
VGAIN = {'tolik': 1.85, 'raisa': 2.2, 'pusya': 2.3, 'sveta': 2.0}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
