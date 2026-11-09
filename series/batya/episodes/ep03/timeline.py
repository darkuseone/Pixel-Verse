"""E03 «КОВЁР — НА СНЕГ!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'batya'
EP = 'ep03'
FPS = 30
LUFS = -14.0
VEP = 'ep03_t'
S = f'series/{SLUG}/sfx/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(b1='снег', t3='контент.', s1='тысячи.', b2='бесплатный!', b3='чистят!', t2='промёрз.', b4='лезет!', i1='не', b5='Химчистка?',
            s2='двойному', b6='бесплатно')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper(), 1) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'b1', 'hook'), ('L', 's1', 'offer'), ('L', 'b2', 'scorn'), ('L', 'b3', 'beat'),
    ('L', 't2', 'frost'), ('L', 'b4', 'twist'), ('L', 'i1', 'window'), ('L', 'b5', 'call'), ('L', 's2', 'tariff'), ('L', 't3', 'content'),
    ('L', 'b6', 'button'),
    ('P', 0.3, 'loop'),
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
    (C + 'snow_steps.mp3', 0.0, 0.3), (C + 'canvas_bag_drop.mp3', 0.4, 0.3), (C + 'wind_whistle.mp3', 0.0, 0.1),
    (C + 'phone_key_click.mp3', T0['frost'] + 0.05, 0.4),
    (C + 'snow_steps.mp3', T0['offer'], 0.25), (C + 'cloth_rustle.mp3', T0['offer'] + 1.8, 0.3),
    (C + 'cloth_rustle.mp3', T0['scorn'] + 1.4, 0.3),
    (C + 'canvas_bag_drop.mp3', T0['beat'] + 0.2, 0.35), (C + 'canvas_bag_drop.mp3', T0['beat'] + 0.9, 0.35),
    (C + 'canvas_bag_drop.mp3', T0['beat'] + 1.6, 0.35),
    (C + 'wind_whistle.mp3', T0['frost'], 0.25),
    (C + 'vinyl_scratch.mp3', TWIST + 0.05, 0.35), (C + 'anvil_clank.mp3', TWIST + 0.2, 0.15),
    (C + 'phone_dial_tone.mp3', T0['call'] - 0.3, 0.15),
    (C + 'rimshot_joke.mp3', T0['button'] - 0.1, 0.25),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_shoe_shop.mp3', 59.5, 0.0, TWIST, 0.5, True, VOICE_DIP),
    (CM + 'komiku_fetch_contest.mp3', 41.5, TWIST + 0.25, DUR, 0.5, True, VOICE_DIP),
]
VGAIN = {'batya': 2.0, 'tema': 2.1, 'ira': 2.1, 'sosed': 2.0}
VNORM = -16.0        # every line levelled to -16 LUFS before the mix (owner 09.11: voices were quiet under music and SFX)

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
