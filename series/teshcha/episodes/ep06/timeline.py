"""E06 «Тёща уезжает!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'teshcha'
EP = 'ep06'
FPS = 30
LUFS = -14.0
VEP = 'ep06_t'
S = f'series/{SLUG}/sfx/'
MUS = f'series/{SLUG}/music/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {'tolik_echo': 'aecho=0.8:0.6:220|440:0.35|0.2'}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(r1='домой.', t1='Ура!', t2='мужик!', t3='недельку?', r2='купила!', p1='моё.', s1='мама!', t4='Навсегда?!')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'r1', 'hook'), ('L', 't1', 'dance'), ('L', 't2', 'chair'), ('P', 1.1, 'days'), ('L', 't3', 'call'), ('P', 0.6, 'twist'),
    ('L', 'r2', 'hole'), ('L', 'p1', 'pusya'), ('L', 's1', 'sveta'), ('L', 't4', 'cry'), ('P', 0.5, 'loop'),
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
    (C + 'canvas_bag_drop.mp3', 0.1, 0.5), (C + 'suitcase.mp3', 1.2, 0.4),
    (C + 'door_apartment_close.mp3', T0['dance'] - 0.1, 0.6), (C + 'boing_cartoon.mp3', T0['dance'] + 0.6, 0.3),
    (C + 'boing_cartoon.mp3', T0['dance'] + 1.4, 0.25),
    (C + 'chair_creak.mp3', T0['chair'] + 0.1, 0.6), (C + 'phone_key_click.mp3', T0['chair'] + 1.2, 0.6),
    (C + 'whoosh_3.mp3', T0['days'], 0.5), (C + 'fridge_door.mp3', T0['days'] + 0.2, 0.5),
    (C + 'phone_dial_tone.mp3', T0['call'] - 0.1, 0.25, 0.0, 1.2),
    (C + 'jackhammer.mp3', TWIST, 0.7, 0.0, 1.6), (S + 'twist_hit.mp3', TWIST + 0.5, 0.5), (C + 'anvil_clank.mp3', TWIST + 0.55, 0.3),
    (C + 'jackhammer.mp3', T0['hole'] + 2.6, 0.35, 0.0, 0.8),
    (C + 'chair_creak.mp3', T0['pusya'] + 0.1, 0.4),
    (C + 'door_apartment_open.mp3', T0['sveta'] - 0.15, 0.5),
    (C + 'rimshot_joke.mp3', T0['loop'] - 0.05, 0.55),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_weekly_fair.mp3', 59.5, 0.0, T0['chair'] + 0.2, 0.8, True, VOICE_DIP),
    (CM + 'komiku_shoe_shop.mp3', 59.5, T0['days'], TWIST, 0.75, True, VOICE_DIP),
    (CM + 'komiku_fetch_contest.mp3', 59.5, T0['hole'], DUR, 0.8, True, VOICE_DIP),
]
VGAIN = {'tolik': 1.85, 'raisa': 2.2, 'pusya': 2.3, 'sveta': 2.0, 'lyusya': 2.3, 'babki': 2.2, 'raisa_vm': 2.4, 'tolik_echo': 1.85}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
