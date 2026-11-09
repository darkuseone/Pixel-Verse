"""E05 «7 ЛИШНИХ БОЛТОВ?!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'batya'
EP = 'ep05'
FPS = 30
LUFS = -14.0
VEP = 'ep05_t'
S = f'series/{SLUG}/sfx/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(b1='болтов?!', t1='пятницу.', b2='слабых!', i1='вверх', b3='дизайн!', b5='влитой!', k1='второй', b4='Второй?!',
            t2='этой', b6='пять', i2='Восьмой')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper(), 1) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'b1', 'hook'), ('L', 't1', 'flash'), ('L', 'b2', 'tear'), ('L', 'i1', 'door'), ('L', 'b3', 'design'), ('L', 'b5', 'slap'),
    ('L', 'k1', 'twist'), ('L', 'b4', 'second'), ('L', 't2', 'manual'), ('L', 'b6', 'again'), ('L', 'i2', 'button'),
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
    (C + 'keys_on_table.mp3', 0.0, 0.25), (C + 'vinyl_scratch.mp3', 0.15, 0.2),
    (C + 'whoosh_1.mp3', T0['flash'], 0.3), (C + 'phone_key_click.mp3', T0['flash'] + 0.1, 0.3),
    (C + 'cloth_rustle.mp3', T0['tear'] + 0.6, 0.45), (C + 'cloth_rustle.mp3', T0['tear'] + 1.1, 0.45),
    (C + 'chair_creak.mp3', T0['door'] + 0.3, 0.3),
    (C + 'floor_squeak.mp3', T0['slap'] + 0.2, 0.3), (C + 'chair_creak.mp3', T0['slap'] + 0.5, 0.4), (C + 'boing_cartoon.mp3', T0['slap'] + 0.9, 0.15),
    ('series/teshcha/sfx/doorbell_bird.mp3', TWIST - 0.15, 0.2), (C + 'vinyl_scratch.mp3', TWIST + 0.05, 0.35),
    (C + 'canvas_bag_drop.mp3', TWIST + 0.6, 0.3),
    (C + 'suitcase.mp3', T0['manual'] + 0.2, 0.25),
    (C + 'zipper.mp3', T0['again'] + 0.3, 0.15),
    (C + 'anvil_clank.mp3', T0['button'] + 0.5, 0.12), (C + 'rimshot_joke.mp3', T0['button'] + 1.1, 0.2),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_shoe_shop.mp3', 59.5, 0.0, TWIST, 0.5, True, VOICE_DIP),
    (CM + 'komiku_fetch_contest.mp3', 41.5, TWIST + 0.25, DUR, 0.5, True, VOICE_DIP),
]
VGAIN = {'batya': 2.0, 'tema': 2.1, 'ira': 2.1, 'sosed': 2.0, 'kurier': 2.0}
VNORM = -16.0        # every line levelled to -16 LUFS before the mix (owner 09.11: voices were quiet under music and SFX)

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
