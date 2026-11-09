"""E04 «412 КВТ?! КТО НЕ ВЫКЛЮЧИЛ СВЕТ?!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'batya'
EP = 'ep04'
FPS = 30
LUFS = -14.0
VEP = 'ep04_t'
S = f'series/{SLUG}/sfx/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(b1='двенадцать?!', b2='сам!', t1='двенадцатом.', i1='ничего', b4='крутится!', t2='гудит?', b5='запас!', t3='Лещ.',
            b6='свежий!', i2='старше')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper(), 1) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'b1', 'hook'), ('L', 'b2', 'bulbs'), ('L', 't1', 'dark'), ('L', 'i1', 'candle'), ('L', 'b4', 'meter'),
    ('L', 't2', 'twist'), ('L', 'b5', 'hug'), ('L', 't3', 'bream'), ('L', 'b6', 'fresh'), ('L', 'i2', 'button'),
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
    (C + 'phone_key_click.mp3', 0.0, 0.3), (C + 'vinyl_scratch.mp3', 0.15, 0.2),
    (S + 'bulb_unscrew.mp3', T0['bulbs'] + 0.2, 0.25), (S + 'bulb_unscrew.mp3', T0['bulbs'] + 1.9, 0.25),
    (C + 'zipper.mp3', T0['bulbs'] + 2.9, 0.12),
    (C + 'phone_key_click.mp3', T0['dark'] + 0.1, 0.3),
    (C + 'chair_creak.mp3', T0['candle'] + 0.2, 0.25),
    (S + 'freezer_hum.mp3', T0['candle'] + 0.4, 0.05), (C + 'slipper_steps.mp3', T0['meter'], 0.3), (S + 'freezer_hum.mp3', T0['meter'] + 0.6, 0.08),
    (C + 'door_apartment_open.mp3', TWIST - 0.1, 0.3), (C + 'vinyl_scratch.mp3', TWIST + 0.05, 0.35), (S + 'freezer_hum.mp3', TWIST + 0.1, 0.22),
    (S + 'freezer_hum.mp3', T0['hug'], 0.12), (C + 'cloth_rustle.mp3', T0['hug'] + 0.2, 0.3),
    (C + 'freezer_close.mp3', T0['bream'] - 0.05, 0.3), (C + 'anvil_clank.mp3', T0['bream'] + 0.5, 0.12),
    (C + 'rimshot_joke.mp3', T0['button'] - 0.1, 0.25),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_mandolin.mp3', 59.5, 0.0, TWIST, 0.5, True, VOICE_DIP),
    (CM + 'komiku_weekly_fair.mp3', 59.5, TWIST + 0.25, DUR, 0.5, True, VOICE_DIP),
]
VGAIN = {'batya': 2.0, 'tema': 2.1, 'ira': 2.1, 'sosed': 2.0}
VNORM = -16.0        # every line levelled to -16 LUFS before the mix (owner 09.11: voices were quiet under music and SFX)

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
